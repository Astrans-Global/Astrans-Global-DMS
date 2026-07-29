# Bigcapital workstream (Astrans)

Accounting core = **Bigcapital** (self-hosted). Distribution ops = **Astrans DMS**.

## Locked decisions

- VAT: **1B** (see [VAT_SL_1B.md](VAT_SL_1B.md)) — bookkeeping first, SL schedules next  
- Host now: VirtualBox Ubuntu + Coolify / Docker (`astransdms.xyz`)  
- Host later: dedicated PC  
- Ledger: event-based stock + money ([EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md))  

## Doc index

| Doc | Purpose |
|-----|---------|
| [SOURCE_MATERIALS.md](SOURCE_MATERIALS.md) | BS/TB captures, VAT accounts, event list |
| [CHART_OF_ACCOUNTS.md](CHART_OF_ACCOUNTS.md) | Target COA + opening balance rules |
| [CONFIGURE_COA_RUNBOOK.md](CONFIGURE_COA_RUNBOOK.md) | Click-path after first Bigcapital login |
| [opening-balances.template.csv](opening-balances.template.csv) | Cutover worksheet |
| [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md) | Install Bigcapital on the VM |
| [EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md) | DMS → Bigcapital postings |
| [DMS_SCOPE.md](DMS_SCOPE.md) | What each system owns |
| [VAT_SL_1B.md](VAT_SL_1B.md) | Sri Lanka VAT roadmap |

## Deploy helper

[../../deploy/bigcapital/](../../deploy/bigcapital/)
