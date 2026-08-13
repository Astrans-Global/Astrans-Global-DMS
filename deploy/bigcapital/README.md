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

**Note:** branding is being migrated from this runtime overlay into the source fork
(see below). Once the fork build is live, `branding/` here retires.

## Source fork (Phase 1 buildout)

Bigcapital is forked at `https://github.com/Astrans-Global/bigcapital`, branch
`astrans-main` (pinned near the commit the currently-deployed
`bigcapitalhq/server:latest` / `webapp:latest` images were built from — NOT the
bleeding-edge `develop` branch, which carries in-progress/broken work).

White-label branding (mail templates + subjects, favicon/manifest/title, logo
assets) has been ported into the fork's source at the commit above. Phase 1
features (subcategories, lots, invoice workflow, Secondary P&L, etc.) are being
built natively on this branch instead of as runtime patches.

To build custom images from the fork instead of pulling `bigcapitalhq/*:latest`,
clone the fork next to this repo and compose in `docker-compose.fork-build.yml`:

```bash
git clone -b astrans-main https://github.com/Astrans-Global/bigcapital.git bigcapital-src
BIGCAPITAL_SRC=./bigcapital-src docker compose \
  -f docker-compose.prod.yml -f docker-compose.restart.yml \
  -f docker-compose.fork-build.yml \
  -f branding/docker-compose.branding.yml \
  up -d --build
```

Do this on a staging copy first — swapping the live accounting system's
images is a production cutover and should be tested end-to-end (login,
invoicing, reports, PDF export) before pointing `books.astransdms.xyz` at it.
