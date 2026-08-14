# Bigcapital workstream (Astrans)

Accounting core = **Bigcapital** (self-hosted). Distribution ops = **Astrans DMS**.

## Locked decisions

- VAT: **1B** (see [VAT_SL_1B.md](VAT_SL_1B.md)) — bookkeeping first, SL schedules next  
- Host now: VirtualBox Ubuntu + Coolify / Docker (`astransdms.xyz`)  
- Host later: dedicated PC — see [MIGRATE_TO_DEDICATED_PC.md](MIGRATE_TO_DEDICATED_PC.md) for the plan  
- Ledger: event-based stock + money ([EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md))  

## Doc index

| Doc | Purpose |
|-----|---------|
| [SOURCE_MATERIALS.md](SOURCE_MATERIALS.md) | BS/TB captures, VAT accounts, event list |
| [CHART_OF_ACCOUNTS.md](CHART_OF_ACCOUNTS.md) | Target COA + opening balance rules |
| [CONFIGURE_COA_RUNBOOK.md](CONFIGURE_COA_RUNBOOK.md) | Click-path after first Bigcapital login |
| [opening-balances.template.csv](opening-balances.template.csv) | Cutover worksheet |
| [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md) | Install Bigcapital on the VM |
| [MIGRATE_TO_DEDICATED_PC.md](MIGRATE_TO_DEDICATED_PC.md) | Plan: move host from laptop VM to dedicated PC |
| [EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md) | DMS → Bigcapital postings |
| [DMS_SCOPE.md](DMS_SCOPE.md) | What each system owns |
| [../ops/PHASE1.md](../ops/PHASE1.md) | Phase 1 ops (lots, statuses, 4410, VAT print) |
| [VAT_SL_1B.md](VAT_SL_1B.md) | Sri Lanka VAT roadmap |
| [Astrans-Books-Accounting-Guide.pdf](Astrans-Books-Accounting-Guide.pdf) | How Books handles accounting (examples + DMS posting) |

## Deploy helper

[../../deploy/bigcapital/](../../deploy/bigcapital/)
