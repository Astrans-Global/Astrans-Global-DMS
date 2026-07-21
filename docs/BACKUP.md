# Backups (start early)

Even on Supabase free, treat data as precious.

## Minimum habit

1. **Weekly** (or before any risky migration): export DB from Supabase.
2. Store copies in **two places** (e.g. encrypted drive + cloud folder). Do not keep the only backup on one laptop.

## Supabase dashboard export

1. Supabase → **Project Settings → Database** (or Table Editor / SQL as needed).
2. Use Supabase **backup / download** options available on your plan, or run SQL dumps via CLI when set up.
3. Name files with dates: `astrans-dms-YYYY-MM-DD.sql` (or `.dump`).

## CLI dump (when linked)

After Supabase CLI is linked to the project:

```bash
supabase db dump -f backups/astrans-dms-$(date +%Y%m%d).sql
```

(Windows: pick a dated filename manually.)

## What to back up

| Asset | Where |
|-------|--------|
| App code | GitHub (already) |
| Postgres data | Dump / Supabase backup |
| Storage buckets (files) | Periodic download or sync once used |
| Env secrets | Password manager (not only Discord/chat) |

## Restore drill (once after v1)

Practice restoring a dump into a **throwaway** Supabase project or local Postgres so recovery is not theoretical.
