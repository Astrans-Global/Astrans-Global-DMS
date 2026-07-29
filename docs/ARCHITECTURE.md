# Architecture rules (Astrans Global DMS)

## Dual-core model (locked)

```text
Astrans DMS (ops)  →  posts events  →  Bigcapital (books + inventory valuation)
```

Details: [bigcapital/DMS_SCOPE.md](bigcapital/DMS_SCOPE.md) · [bigcapital/EVENT_POSTING_MATRIX.md](bigcapital/EVENT_POSTING_MATRIX.md)

## Hosting

| Layer | Now | Later |
|-------|-----|--------|
| Bigcapital | VirtualBox Ubuntu + Docker/Coolify; Cloudflare Tunnel (`books.astransdms.xyz`) | Dedicated PC, same compose |
| Coolify UI | `astransdms.xyz` | Same pattern |
| Astrans DMS Next.js | Develop on Vercel/Supabase or Coolify as needed | Prefer Coolify beside Bigcapital |
| Oracle Cloud paid shapes | **Forbidden** | Forever forbidden |

Bigcapital runtime includes **MySQL/MariaDB + Redis** (+ Gotenberg). That Redis is **only** for the accounting stack on the VM — do not introduce Redis as the DMS system of record.

## Accounting / VAT

- Currency: **LKR**
- COA: [bigcapital/CHART_OF_ACCOUNTS.md](bigcapital/CHART_OF_ACCOUNTS.md)
- VAT decision **1B**: bookkeeping VAT first; Sri Lanka schedules next — [bigcapital/VAT_SL_1B.md](bigcapital/VAT_SL_1B.md)

## DMS application rules

1. Ops workflows live in Astrans DMS (routes, vans, collections UX).  
2. Stock/money truth for books posts into Bigcapital per the event matrix.  
3. Prefer short/batched integration jobs (no unpaid Oracle Cloud workarounds).  
4. Secrets in env files only; never commit `.env`.  
5. Code on GitHub: `Astrans-Global/Astrans-Global-DMS`.

## Do not

1. Rebuild full GL/P&L/BS inside Next.js while Bigcapital is the core.  
2. Expose MySQL/Redis ports to the public internet.  
3. Upgrade to paid OCI / non–Always-Free shapes.  
4. Block go-live books on unfinished RAMIS UI — ship Phase A VAT first.
