# Astrans Global DMS

Distribution Management System for Astrans.

**Repo:** [Carlin-Fernando/Astrans-Global-DMS](https://github.com/Carlin-Fernando/Astrans-Global-DMS)

**Hosting path (now):** Next.js on **Vercel Hobby** + **Supabase** free tier — same model as Astrans Tasks.  
**Later:** Measure free-tier usage after v1; stay, upgrade Supabase, or migrate to home PC / VPS + Coolify if needed.

## Quick start (local test)

1. Install deps: `npm install`
2. Copy env: `copy .env.example .env.local` (Windows) and fill Supabase keys (see [docs/SETUP.md](docs/SETUP.md))
3. Run: `npm run dev`
4. Open [http://localhost:3000](http://localhost:3000)
5. Health check: [http://localhost:3000/api/health](http://localhost:3000/api/health)

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Local development |
| `npm run build` | Production build |
| `npm run start` | Run production build locally |
| `npm run lint` | ESLint |

## Docs

- [docs/SETUP.md](docs/SETUP.md) — Supabase + Vercel wiring
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Portable design rules (Postgres-first, no Redis in v1)
- [docs/BACKUP.md](docs/BACKUP.md) — Backup habit
- [docs/LIMITS_AND_MIGRATION.md](docs/LIMITS_AND_MIGRATION.md) — Decision checkpoint after v1

## Status

Phase 1 skeleton only (no full DMS features yet). Oracle Always Free VM work is paused (capacity); do not create paid OCI resources.
