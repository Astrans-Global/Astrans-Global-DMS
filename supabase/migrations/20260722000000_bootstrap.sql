-- Astrans Global DMS — initial schema placeholder
-- Apply in Supabase SQL editor or via CLI after the project exists.
-- Keep all core DMS state in Postgres so we can migrate off Supabase later.

create extension if not exists "pgcrypto";

-- Example bootstrap table (safe to keep; real domain tables come in later migrations)
create table if not exists public.app_meta (
  key text primary key,
  value text not null,
  updated_at timestamptz not null default now()
);

insert into public.app_meta (key, value)
values ('schema_bootstrap', 'astrans-global-dms-v0')
on conflict (key) do update set value = excluded.value, updated_at = now();
