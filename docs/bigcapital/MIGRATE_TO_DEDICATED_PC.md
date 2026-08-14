# Migrate Bigcapital host: VirtualBox VM (laptop) → dedicated desktop PC

**Status: planned, not started.** We develop and run production on the laptop's
VirtualBox Ubuntu VM only **for now**. Once a dedicated desktop PC is
available, the whole Docker stack moves there unchanged — same Compose files,
same fork images, same Cloudflare Tunnel hostname. This is a locked decision;
see the hosting tables in [ARCHITECTURE.md](../ARCHITECTURE.md),
[README.md](README.md), and [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md).

## Why this move is needed (not just "nice to have")

On 2026-08-14 the laptop VM crashed and rebooted 3 times in ~18 hours. Kernel
logs showed multi-CPU `soft lockup` / RCU stalls right before each crash —
the signature of the **Windows host sleeping/suspending under the running
VM**, not a Bigcapital or Docker bug. A laptop that sleeps, updates, or gets
closed is not a real server. A dedicated always-on desktop removes this
failure class entirely (see [RESILIENCE.md](../../deploy/bigcapital/RESILIENCE.md)
for the interim mitigations while we're still on the laptop).

## Trigger to start this migration

Start this migration when **any** of these is true:
- Dedicated desktop hardware is racked/set up and reachable on the network, or
- The laptop VM has another instability incident after the interim
  mitigations in `RESILIENCE.md` (Windows sleep disabled, VM autostart) are
  already in place, or
- You explicitly ask to proceed.

Nothing here happens automatically — this doc is the plan, execution is a
separate, explicitly-requested step.

## Pre-flight on the new desktop

1. Install Ubuntu Server (or same distro/version as the current VM) directly
   on the desktop — no VirtualBox layer needed since it's already dedicated
   hardware.
2. Install Docker + Compose plugin, same versions as documented in
   [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md) prerequisites.
3. Install `cloudflared` and register it to the **same** tunnel
   (`astrans-dms`) as a new connector — Cloudflare tunnels support multiple
   connectors, so both boxes can briefly run side by side during cutover.
4. `git clone` the fork (`Astrans-Global/bigcapital`, branch `astrans-main`)
   to `/home/<user>/bigcapital-src` (or wherever `BIGCAPITAL_SRC` should
   point — keep it an **absolute path**, see the note below).
5. Copy `/opt/bigcapital/*.yml`, `.env` (secrets — transfer securely, don't
   commit), and `deploy/bigcapital/systemd/*` from the VM to the new host's
   `/opt/bigcapital`.

## The BIGCAPITAL_SRC lesson (do not repeat)

`docker-compose.fork-build.yml` resolves its build context from
`${BIGCAPITAL_SRC:-./bigcapital-src}` — a path **relative to
`/opt/bigcapital`** if the env var isn't set. On the VM this silently
resolved to a non-existent `/opt/bigcapital/bigcapital-src` and took the
**entire** stack down on every reboot until fixed on 2026-08-14. On the new
host:

1. Set `BIGCAPITAL_SRC=/home/<user>/bigcapital-src` (absolute path) in
   `/opt/bigcapital/.env` **before** the first boot.
2. Verify with `docker compose --file docker-compose.prod.yml --file
   docker-compose.minio.yml --file docker-compose.fork-build.yml --file
   docker-compose.restart.yml config` — confirm `context:` resolves to a real
   path, not a dangling relative one.
3. Test the actual boot path once with `sudo systemctl restart
   bigcapital.service` and confirm `systemctl is-active` reports `active
   (exited)` with `status=0/SUCCESS`, not a failed build.

## Build/bring-up on the new host

1. Build the fork images locally on the new host (same as VM):
   ```bash
   cd ~/bigcapital-src
   docker build -f packages/server/Dockerfile -t astrans/bigcapital-server:local .
   docker build -f packages/webapp/Dockerfile -t astrans/bigcapital-webapp:local .
   ```
2. `cd /opt/bigcapital && docker compose --file docker-compose.prod.yml --file
   docker-compose.minio.yml --file docker-compose.fork-build.yml --file
   docker-compose.restart.yml up -d`
3. Confirm all containers healthy, `curl -I http://127.0.0.1:8088/` → `200`.

## Data cutover (MySQL + MinIO)

1. Freeze writes on the VM briefly (maintenance page or just pick a quiet
   moment — this is an internal tool, not 24/7 customer-facing).
2. `mysqldump` all `bigcapital_system` + `bigcapital_tenant_*` databases on
   the VM; copy the dump to the new host; restore.
3. Sync/copy the MinIO data volume (uploaded logos, attachments) to the new
   host's MinIO volume.
4. Bring up the new host's stack pointed at the restored data; verify login,
   a sample invoice, and the item/customer lists match the VM.

## Cutover

1. In Cloudflare Zero Trust → Tunnel `astrans-dms`, remove the VM's
   connector (or just stop `cloudflared` on the VM) so all traffic routes to
   the new desktop's connector.
2. Verify `https://books.astransdms.xyz` serves from the new host (check
   response headers / a harmless log line unique to the new box).
3. Keep the VM's stack stopped but intact for a few days as a rollback path
   before decommissioning it.

## Rollback

If anything is wrong post-cutover: restart `cloudflared` + `bigcapital.service`
on the VM (data hasn't diverged yet since writes were frozen), and stop the
new host's connector. Investigate before retrying.

## Post-migration cleanup

- Update `ARCHITECTURE.md`, `README.md`, `DEPLOY_COOLIFY.md` hosting tables:
  "Now" becomes the dedicated PC, delete the "Later" column.
- Decommission the VM (or repurpose it as a spare/staging box).
- Re-run the `RESILIENCE.md` reboot checklist against the new host, update
  its "Windows host (required)" section since it won't apply anymore.
