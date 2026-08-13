# Bigcapital deploy helpers (run on Ubuntu VM)

See full guide: [docs/bigcapital/DEPLOY_COOLIFY.md](../../docs/bigcapital/DEPLOY_COOLIFY.md)

## Quick path

```bash
chmod +x install-on-vm.sh
./install-on-vm.sh
```

Then configure Cloudflare Tunnel hostname `books.astransdms.xyz` → `http://127.0.0.1:8088`.

## Stay online for end users

See [RESILIENCE.md](./RESILIENCE.md) — boot services, watchdog, DNS, and Windows/VirtualBox autostart so Error 1033 does not come back after reboots.

## White-label (Astrans / resale)

See [branding/README.md](./branding/README.md). Edit `branding/brand.json` + logo, run `python branding/apply-brand.py`, include `branding/docker-compose.branding.yml` in compose up.
