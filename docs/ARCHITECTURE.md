# Architecture rules (Astrans Global DMS)

## Single-system model (locked)

There is **one system**: a maintained source fork of [Bigcapital](https://github.com/bigcapitalhq/bigcapital), built into our own `bigcapital-server` / `bigcapital-webapp` Docker images. Phase 1 distribution-operations features (item price-lots, GRN VAT handling, pending/reserved/invoiced/delivered invoice workflow, per-area numbering, customer risk grading, Secondary P&L, Delivery Prep, VAT/Non-VAT invoice output) are built as native modules and screens inside that fork's existing Items / Customers / Bills / Sales-Invoices code, not as a separate app.

There is no separate "Astrans DMS" Next.js application. That earlier scaffold (Vercel + Supabase) and the later iframe/`/ops`-overlay attempt have both been retired; see git tags `pre-ops-phase1` and `pre-phase1-fork-buildout` if either needs to be inspected.

Details: [bigcapital/DMS_SCOPE.md](bigcapital/DMS_SCOPE.md) · [bigcapital/EVENT_POSTING_MATRIX.md](bigcapital/EVENT_POSTING_MATRIX.md)

## Hosting

| Layer | Now | Later |
|-------|-----|--------|
| Bigcapital fork (server + webapp + MySQL/Redis) | VirtualBox Ubuntu + Docker; Cloudflare Tunnel (`books.astransdms.xyz`) | Dedicated PC, same compose |
| Coolify UI | `astransdms.xyz` | Same pattern |
| Oracle Cloud paid shapes | **Forbidden** | Forever forbidden |

Bigcapital runtime includes **MySQL/MariaDB + Redis** (+ Gotenberg for PDF rendering). Redis/MySQL stay private on the VM, never exposed publicly.

## Accounting / VAT

- Currency: **LKR**
- COA: [bigcapital/CHART_OF_ACCOUNTS.md](bigcapital/CHART_OF_ACCOUNTS.md)
- VAT decision **1B**: bookkeeping VAT first; Sri Lanka schedules next — [bigcapital/VAT_SL_1B.md](bigcapital/VAT_SL_1B.md)
- DMS operational events (GRN, invoice Delivered, etc.) post into Bigcapital's own ledger per [bigcapital/EVENT_POSTING_MATRIX.md](bigcapital/EVENT_POSTING_MATRIX.md) — there is no external API hop, since the operational screens live inside Bigcapital itself.

## Build/deploy rules

1. All Phase 1 work lands as real source changes in the Bigcapital fork (migrations, Nest modules, React screens) — not runtime DOM patches or dist-file swaps.
2. Prefer short/batched integration jobs (no unpaid Oracle Cloud workarounds).
3. Secrets in env files only; never commit `.env`.
4. Code on GitHub: `Astrans-Global/Astrans-Global-DMS` (this repo holds docs + deploy/ops tooling; the Bigcapital fork itself lives in its own repo/branch referenced from `deploy/bigcapital/`).

## Do not

1. Rebuild a separate GL/P&L/BS application outside the Bigcapital fork.
2. Expose MySQL/Redis ports to the public internet.
3. Upgrade to paid OCI / non-Always-Free shapes.
4. Reintroduce the iframe/`/ops` overlay pattern — Phase 1 screens must be native to the fork.
