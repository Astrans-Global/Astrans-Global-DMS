# White-label Bigcapital product chrome (tab, favicon, login, in-app marks).

## One-file rebrand (for selling to another company)

1. Edit [`brand.json`](brand.json) — product name, description, theme, logo paths.
2. Put logos in `logos/`:
   - `logo-white.png` — used in **dark mode** (white mark; black background OK, it is stripped)
   - `logo-black.png` — used in **light mode** (black mark on transparent)
3. Run:

```bash
python apply-brand.py
```

4. Redeploy webapp with `docker-compose.branding.yml` included (see below).

Do **not** hand-edit `generated/` — it is overwritten by `apply-brand.py`.

## What this covers

- Browser tab title + meta description  
- Favicon / PWA icons  
- Login layout: hide top product logo; bottom mark + product name wordmark, centered  
- Sidebar (expanded + collapsed) product marks via inject (`bigcapital` / `bigcapital-alt`)  
- Light/dark swap: `body.bp4-dark` → white logo, otherwise black logo  
- Theme toggle button (Bigcapital has no built-in theme UI; it only reads OS/`localStorage`)  
- Workspace org-logo crop fix (`object-fit: contain`)  
- Stock paths `bigcapital.svg`, `logo192.png`, `logo512.png`, `manifest.json`

## What it does not cover

- Organization name / invoice logo upload (Preferences → Branding + MinIO)  
- Deep subscription / LemonSqueezy strings inside hashed bundles  

Bigcapital **supports** light and dark CSS, but Preferences has **no Appearance page**. Theme defaults from the OS (`prefers-color-scheme`) or `localStorage.theme`. The brand pack adds a **Light mode / Dark mode** button (bottom-right) so you can switch without DevTools.
## Compose

From `/opt/bigcapital` (or after copying this folder there):

```bash
docker compose \
  -f docker-compose.prod.yml \
  -f docker-compose.minio.yml \
  -f docker-compose.webapp-patch.yml \
  -f docker-compose.server-patch.yml \
  -f docker-compose.restart.yml \
  -f branding/docker-compose.branding.yml \
  up -d --force-recreate webapp
```

Always use `--force-recreate` after regenerating `generated/` so bind mounts pick up replaced files. Do not `rm -rf generated/` while the webapp container is running.

Also keep `MAIL_FROM_NAME` in `.env` aligned with `productNameFull` if you send mail.

## How stale-cache protection works (don't undo these)

- `index.html` → `Cache-Control: no-store` (nginx `patches/webapp-nginx/default.conf`), so browsers always fetch a fresh shell.
- The inject file is **versioned** (`/brand/astrans-inject-<ts>.js`, immutable); a new `apply-brand.py` run creates a new name, so no client can hold a stale one. Legacy `/brand/inject.js` stays `no-store`.
- `/service-worker.js` (and `sw.js`, workbox files) return **410** — old CRA service workers in normal browser profiles self-unregister on their update check. The generated `index.html` also unregisters SWs and clears CacheStorage.
- An inline `<style>` in `index.html` hides stock Bigcapital marks pre-paint, so there is no logo flash while `inject.js` loads.
- Missing `/fonts/*` return **404**, never the SPA HTML.

## Normal Chrome still broken? (one-time reset)

Incognito works but a normal profile doesn’t → that profile still has an old service worker /
HTTP cache. Open this **once** in the broken normal window (close other Books tabs first):

https://books.astransdms.xyz/__astrans_reset

It sends `Clear-Site-Data`, unregisters service workers, then redirects to login. After that,
normal tabs should match Incognito. First plain visit to `/auth/login` also sends a
cookie-gated `Clear-Site-Data` wipe (`astrans_cv=6`).

## SPA mounts (strict)

`docker-compose.webapp-patch.yml` may mount:

- nginx configs (including `no-store` for patched asset filenames)
- `index-C4jBpDeP.js` — `transformToForm` bridge (Preferences General)
- `UserFormDialogContent-B7F4JkNA.js` — edit-user dialog waits for user/roles
  (stock filename only)

Never bind-mount `PrivatePages-*.js` or renamed `UserFormDialogContent-astrans*.js`.
Rebuild the index patch with
`patches/webapp-assets/patch-transform-to-form.py` from stock image file.

**Never** put `?v=` on `/assets/index-*.js` in `index.html` — that breaks the Vite
module graph (login dead, nothing clickable). Version only
`/brand/astrans-inject-*.js`.

## Reboot checklist

See `../RESILIENCE.md` → "Reboot checklist". Short version: reboot the VM, wait ~90s, open
`https://books.astransdms.xyz/auth/login` in a **normal** window — it must show the Astrans
login with no hard refresh. If not, check `systemctl is-active cloudflared bigcapital.service`.
