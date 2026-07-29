# Astrans Global DMS

Distribution Management System for Astrans.

**Repo:** [Astrans-Global/Astrans-Global-DMS](https://github.com/Astrans-Global/Astrans-Global-DMS)

## Architecture (current direction)

- **Accounting core:** [Bigcapital](https://github.com/bigcapitalhq/bigcapital) on VirtualBox Ubuntu / Coolify (move to dedicated PC later)  
- **Ops / DMS:** Astrans app + event postings into Bigcapital  
- **Edge:** Cloudflare Tunnel (`astransdms.xyz`, planned `books.astransdms.xyz`)  

See [docs/bigcapital/README.md](docs/bigcapital/README.md).

## Quick start (DMS Next.js skeleton)

1. `npm install`  
2. `copy .env.example .env.local` and fill Supabase keys ([docs/SETUP.md](docs/SETUP.md))  
3. `npm run dev` → [http://localhost:3000](http://localhost:3000)  

## Bigcapital on the VM

Follow [docs/bigcapital/DEPLOY_COOLIFY.md](docs/bigcapital/DEPLOY_COOLIFY.md) and run [deploy/bigcapital/install-on-vm.sh](deploy/bigcapital/install-on-vm.sh) **on the Ubuntu VM**.

Then configure COA: [docs/bigcapital/CONFIGURE_COA_RUNBOOK.md](docs/bigcapital/CONFIGURE_COA_RUNBOOK.md).

## Docs

- [docs/bigcapital/](docs/bigcapital/) — books, COA, deploy, VAT 1B, event matrix, scope  
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — dual-core rules  
- [docs/SETUP.md](docs/SETUP.md) — Supabase + Vercel (DMS skeleton)  
- [docs/BACKUP.md](docs/BACKUP.md) — backups  

## Status

Bigcapital-as-core plan artifacts are in-repo. Run the VM install script to bring Bigcapital up, then complete COA/opening balances inside the UI.
