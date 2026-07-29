# Source materials — Astrans books + events

Decisions locked for this workstream:

| Decision | Choice |
|----------|--------|
| VAT depth | **1B** — invoice VAT + control accounts **and** Sri Lanka VAT return/schedules in-app (v1 target; bookkeeping VAT first, filing pack next) |
| Hosting now | **Oracle VirtualBox** Ubuntu VM + Coolify (`astransdms.xyz`) |
| Hosting later | Separate dedicated PC (same Coolify/Docker pattern) |
| Ledger model | Event-based for **stock and money** |

## Source reports (captured)

| File | What it is |
|------|------------|
| [source/balance-sheet-2024-07-28.png](source/balance-sheet-2024-07-28.png) | Balance Sheet as of **2024-07-28** (Total Assets = Equity+Liabilities = 246,074,822.16) |
| [source/trial-balance-fy2021-22.png](source/trial-balance-fy2021-22.png) | Trial Balance **01/04/2021–31/03/2022** (Debits = Credits = 214,011,733.00) |

These are screenshots from the **current** operating system (not yet Astrans Bigcapital). They define the COA shape we must recreate.

## VAT-related accounts seen in source

| Account | Role |
|---------|------|
| VAT Control Account | Net VAT position (negative on BS as of 2024-07-28 → receivable-style position) |
| VAT Paid | Input VAT (seen on TB) |
| WHT Receivable | Withholding tax recoverable |
| Income Tax (CP) | Corporate tax advance / CP (TB) |

## Core daily events that must affect stock and/or money

Minimum event list for Astrans DMS → Bigcapital posting (see [EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md)):

1. Sale confirmed / invoice issued  
2. Customer collection / payment received  
3. Purchase / supplier bill recorded  
4. Supplier payment made  
5. Stock issued to van/route/warehouse  
6. Stock returned  
7. Expense recorded  
8. Manual journal / adjustment  
9. Bank transfer / cash movement  

## Still needed from ops (fill when known)

- [ ] Exact current VAT rate(s) and whether SSCL applies  
- [ ] TIN / VAT registration number for invoice footer  
- [ ] Preferred cutover date for opening balances  
- [ ] Full bank account list with codes (BS shows some; TB period differs — reconcile at cutover)  

## Related docs

- [CHART_OF_ACCOUNTS.md](CHART_OF_ACCOUNTS.md) — target Bigcapital COA + opening-balance template  
- [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md) — stand up Bigcapital on the VM  
- [EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md) — DMS event → accounting/stock postings  
- [DMS_SCOPE.md](DMS_SCOPE.md) — what stays in Bigcapital vs Astrans DMS  
