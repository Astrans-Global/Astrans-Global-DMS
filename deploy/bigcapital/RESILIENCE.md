# Astrans Books — keep online for end users

Goal: `https://books.astransdms.xyz` survives PC reboot, VM restart, and DNS glitches without SSH.

## What fails (Error 1033)

Cloudflare **1033** = tunnel offline. Common causes on this setup:

1. Windows host asleep / VirtualBox VM not running  
2. `cloudflared` crash-loop (often bad router DNS)  
3. Bigcapital containers stopped (`restart: on-failure` does **not** restart clean `Exited (0)` stops)

## Hardening already designed for the VM

Install once on the Ubuntu VM (see `install-resilience.sh`):

| Piece | Role |
|--------|------|
| `docker-compose.restart.yml` | `restart: unless-stopped` on all long-running services |
| `branding/docker-compose.branding.yml` | White-label tab/favicon/login marks (see `branding/README.md`) |
| `bigcapital.service` | `docker compose up -d` on boot |
| `astrans-books-watchdog.timer` | Every 2 minutes: fix DNS file if missing, restart tunnel if down, compose up if `:8088` unhealthy |
| `/etc/systemd/resolved.conf.d/astrans-dns.conf` | Prefer `1.1.1.1` / `8.8.8.8` over flaky router DNS |
| `systemd/cloudflared-override.conf` | Force tunnel `http2` (QUIC flaps through VirtualBox NAT) + `Restart=always` |
| `docker-compose.webapp-patch.yml` | **Nginx only** (cache/SW). Do not remount hashed `index`/`PrivatePages`/`UserForm` SPA chunks |

## Reboot checklist (verified 2026-08-07: public branded login back in ~80s)

After `sudo reboot` (or host restart), everything should recover by itself:

1. **~0–60s** — VM boots, Docker starts all containers (`restart: unless-stopped` + `bigcapital.service`).
2. **~15–20s after boot** — `cloudflared` registers 4 connections over **http2** (check: `journalctl -u cloudflared -b | grep Registered`).
3. **~60–90s** — `https://books.astransdms.xyz/auth/login` returns the branded page; API (`/api/auth/meta`) may take ~30s more while `bigcapital-server` warms up.
4. Nothing to do in the browser: HTML is `no-store`, the inject file is versioned, and `/service-worker.js` returns **410** so stale service workers self-unregister.

If it is still down after ~3 minutes:

```bash
ssh -p 2222 astrans@127.0.0.1
systemctl is-active docker cloudflared bigcapital.service astrans-books-watchdog.timer
sudo systemctl restart cloudflared          # tunnel (Cloudflare error 1033/530)
sudo systemctl start bigcapital.service     # containers (502 from edge)
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8088/   # expect 200
```

The watchdog timer runs every 2 minutes and does the same repairs automatically.

## Windows host (required)

Tunnel + Books live **inside** the VM. If Windows is off or the VM is stopped, the public site dies.

1. **Keep the PC awake** when Books must be online (or move later to a small always-on PC — still Always Free / no paid OCI).  
2. **Autostart VirtualBox VM** after Windows login/boot:

```bat
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setproperty autostartdbpath "C:\Program Files\Oracle\VirtualBox\autostart"
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Astrans-Ubuntu" --autostart-enabled on --autostart-delay 30
```

Then install/enable **VirtualBox Autostart** (Oracle docs / `VBoxAutostartSvc`) so the VM starts without opening the GUI.

3. Optional: Windows Task Scheduler at logon → start `Astrans-Ubuntu` headless:

```bat
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "Astrans-Ubuntu" --type headless
```

## Quick health check (from Windows)

```bat
curl -I https://books.astransdms.xyz
ssh -p 2222 astrans@127.0.0.1 "systemctl is-active cloudflared; curl -s -o NUL -w %%{http_code} http://127.0.0.1:8088/"
```

Expect tunnel `active` and local `200`.

## What Coolify is for

Optional control panel. Books reliability does **not** depend on Coolify; it depends on **VM up + cloudflared + compose**.
