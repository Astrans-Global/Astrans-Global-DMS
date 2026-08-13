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

## White-label (Astrans / resale) — retired

`branding/` (the `inject.template.js` runtime overlay + `docker-compose.branding.yml`)
is **retired as of the 2026-08-13 cutover**. Branding (title, favicons, manifest,
logo, mail templates/subjects) now lives natively in the source fork
(`bigcapital-fork/packages/webapp/index.html`, `public/*`, `packages/server/static/*`).
Don't re-add the branding overlay to the compose command — edit the fork source instead.

## Source fork (live in production)

Bigcapital is forked at `https://github.com/Astrans-Global/bigcapital`, branch
`astrans-main`. As of 2026-08-13, `books.astransdms.xyz` runs images built
from this fork (`astrans/bigcapital-server:local`, `astrans/bigcapital-webapp:local`)
— **not** `bigcapitalhq/*:latest`. The old runtime patch overlays
(`docker-compose.server-patch.yml`, `docker-compose.webapp-patch.yml`,
`branding/docker-compose.branding.yml`) have been dropped from the live compose
command; their fixes (branding, mail templates, item/subcategory fields) now
live natively in the fork's source. Phase 1 features still being built
(lots, invoice workflow, Secondary P&L, etc.) are added directly to the fork.

To rebuild and redeploy after pulling new fork commits:

```bash
cd ~/bigcapital-src && git pull origin astrans-main
docker build -f packages/server/Dockerfile -t astrans/bigcapital-server:local .
docker build -f packages/webapp/Dockerfile -t astrans/bigcapital-webapp:local .
cd /opt/bigcapital
# Apply any new tenant migrations first (safe/additive, review before running on real data):
docker compose -f docker-compose.prod.yml -f docker-compose.minio.yml \
  -f docker-compose.restart.yml -f docker-compose.fork-build.yml \
  run --rm --no-deps server node packages/server/dist/cli.js tenants:migrate:latest
# Then recreate server/webapp with the new images:
docker compose -f docker-compose.prod.yml -f docker-compose.minio.yml \
  -f docker-compose.restart.yml -f docker-compose.fork-build.yml \
  up -d --no-build
```

`docker-compose.server-patch.yml` and `docker-compose.webapp-patch.yml` (and the
`branding/` folder) are kept in this repo only as historical reference — they are
no longer part of the live compose command.
