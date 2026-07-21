# Setup: Supabase + Vercel

You already know this loop from Astrans Tasks. Do these once for Global DMS.

## 1. Supabase (free project)

1. Go to [https://supabase.com](https://supabase.com) and sign in.
2. **New project** — name it `astrans-global-dms` (or similar).
3. Choose a region close to users (e.g. Singapore / Mumbai if offered).
4. Set a strong DB password; store it in your password manager.
5. Wait until the project is ready.
6. Open **Project Settings → API** and copy:
   - Project URL → `NEXT_PUBLIC_SUPABASE_URL`
   - `anon` `public` key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `service_role` `secret` key → `SUPABASE_SERVICE_ROLE_KEY` (server only)
7. Open **SQL Editor**, paste and run:

`supabase/migrations/20260722000000_bootstrap.sql`

## 2. Local env

In this repo:

```powershell
copy .env.example .env.local
```

Paste the three values into `.env.local`. Never commit `.env.local`.

Then:

```powershell
npm run dev
```

Confirm:

- Home page shows Supabase **configured**
- `/api/health` returns `"supabaseConfigured": true`

## 3. GitHub repo

Repo for this DMS:

**https://github.com/Astrans-Global/Astrans-Global-DMS**

Local `origin` should point there. After you change code:

```powershell
git add .
git commit -m "Your message"
git push
```

## 4. Vercel project

1. Go to [https://vercel.com](https://vercel.com) and sign up/in with the **Astrans-Global** GitHub account.
2. **Add New… → Project** → import `Astrans-Global/Astrans-Global-DMS`.
3. Framework: Next.js (auto-detected).
4. **Environment Variables** — add the same keys as `.env.local`:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `CRON_SECRET` (optional but recommended)
5. Deploy.
6. Open the production URL and `/api/health`.

### Preview testing

Every push/PR can get a Preview URL. Use it on your phone like Tasks.

## 5. Cron (optional)

`vercel.json` already registers a daily hit to `/api/cron/health`.  
When you add real jobs, keep them **short** (Hobby timeouts). Protect with `CRON_SECRET`.

## Checklist

- [ ] Supabase project created
- [ ] Bootstrap SQL applied
- [ ] `.env.local` filled; local `/api/health` OK
- [ ] GitHub remote pushed
- [ ] Vercel env vars set; production `/api/health` OK
