# Limits & migration decision checkpoint

Use this **after v1 works** and you have real (or pilot) usage — not before building.

## Measure

| Metric | Free-ish ceiling (approx.) | Your number | Notes |
|--------|----------------------------|-------------|--------|
| Database size | ~500 MB (Supabase free) | | Dashboard → Database |
| File storage | ~1 GB (Supabase free) | | Dashboard → Storage |
| Auth MAU | Free plan limit | | Usually fine for internal staff |
| Slow/failed API routes | Vercel Hobby timeouts | | Watch cron & heavy reports |
| Need always-on workers / Redis? | Not on Hobby | yes/no | Route optimization intensity |

Fill this table with Cursor after a pilot week.

## Decision

Pick **one**:

1. **Stay** — Vercel + Supabase free is enough.  
2. **Upgrade Supabase only** — keep Vercel; pay for DB/storage headroom.  
3. **Migrate** — move Next.js + Postgres to home PC or ~$5 VPS + Coolify; keep GitHub deploy flow.

## Migration sketch (if option 3)

1. Provision host (home PC Ubuntu or VPS) + Coolify (or Docker Compose).
2. Create Postgres; restore latest dump.
3. Deploy same Next.js app; set env to new DB (or self-hosted Supabase stack).
4. Point DNS / Cloudflare; verify login + ledger.
5. Freeze writes on old Supabase; final dump; cut over.

App code should not need a rewrite if ARCHITECTURE.md rules were followed.

## Oracle note

Oracle Always Free Ampere remains a possible future host **if** Singapore capacity appears. Do not create paid OCI shapes. Account can stay idle.
