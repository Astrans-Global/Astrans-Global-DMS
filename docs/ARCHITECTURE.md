# Architecture rules (portable v1)

These rules keep Astrans Global DMS easy to move off Vercel/Supabase later (home PC or VPS + Coolify) without a rewrite.

## Do

1. **Postgres-first** — All core DMS state (inventory ledger, orders, customers, stock movements) lives in PostgreSQL tables/migrations under `supabase/migrations/`.
2. **Supabase client patterns** — Use `@/lib/supabase/server`, `client`, and `admin` (service role only on the server).
3. **Next.js App Router** — UI + API routes in `src/app`. Prefer server components + route handlers like Astrans Tasks.
4. **Cron-friendly jobs** — Background work must finish within Vercel function limits. Use:
   - Vercel Cron hitting `/api/cron/...`
   - Or a user-triggered “Run job” button that processes a **batch** and returns quickly
5. **Env-based config** — No hardcoded project URLs or secrets.
6. **Code on GitHub** — Source of truth for the program; DB backups are separate (see BACKUP.md).

## Do not (v1)

1. **No Redis** in v1 — no always-on queue workers.
2. **No long-running route-optimization daemons** — if needed, design as batched/cron chunks or defer until self-hosted.
3. **No Vercel-only proprietary data stores** as the system of record (KV/Blob OK only as disposable cache, not ledger).
4. **No paid Oracle Cloud shapes** — see `.cursor/rules/oracle-always-free-only.mdc`. Oracle VM work is paused.

## Hosting now vs later

| Now | Later if limits bite |
|-----|----------------------|
| Vercel Hobby | Same Next.js app on Coolify / Node on home PC or VPS |
| Supabase Postgres | `pg_dump` / restore into self-hosted Postgres |
| Supabase Auth/Storage | Re-point or migrate with a planned cutover |

## Testing while building

| Mode | How |
|------|-----|
| Local | `npm run dev` + `.env.local` → Supabase |
| Preview | Vercel Preview URL per push |
| Production | Vercel production domain for pilots |

No home PC or Oracle VM required to develop or demo.
