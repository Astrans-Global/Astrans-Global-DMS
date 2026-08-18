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

To rebuild and redeploy after pulling new fork commits, run the one
canonical deploy script (from Windows, VM reachable at `127.0.0.1:2222`):

```bat
python deploy\bigcapital\deploy-fork.py
```

It pulls `astrans-main`, rebuilds both images, recreates `server`+`webapp`
with the correct file list (**never** `branding/docker-compose.branding.yml`
— see "Gotcha" below), and self-checks that every asset the served
`index.html` references actually returns HTTP 200. If your fork commit adds
a tenant migration, run that manually first:

```bash
ssh -p 2222 astrans@127.0.0.1
cd /opt/bigcapital
docker compose -f docker-compose.prod.yml -f docker-compose.minio.yml \
  -f docker-compose.restart.yml -f docker-compose.fork-build.yml \
  run --rm --no-deps server node packages/server/dist/cli.js tenants:migrate:latest
```

`docker-compose.server-patch.yml` and `docker-compose.webapp-patch.yml` (and the
`branding/` folder) are kept in this repo only as historical reference — they are
no longer part of the live compose command.

### Gotcha (2026-08-18 incident): never re-add `branding/docker-compose.branding.yml`

That overlay bind-mounts a stale, hand-generated `index.html` (and
`/brand/*`, `/favicons/*`, `manifest.json`) over whatever the freshly built
webapp image already serves natively. It's fully redundant now — branding
is baked directly into the fork source (`packages/webapp/index.html` +
`packages/webapp/public/*`) and comes out correct, with fresh content
hashes, on every single build. Re-adding the overlay "to fix branding"
instead **shadows** that correct file with an old one still pointing at
the *previous* build's JS/CSS hash filenames — those files no longer exist
after a rebuild, the main bundle 404s, and the whole app renders as a
blank page. This happened for real on 2026-08-18 (someone's ad-hoc deploy
command included the overlay "just in case"); use `deploy-fork.py` instead
of retyping the compose command from memory, precisely to stop this from
happening again.
