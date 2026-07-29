# Bigcapital COA configuration runbook (after install)

Follow after [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md) succeeds and you can log in.

## 1. Organization

- [ ] Company name: Astrans (confirm legal name)
- [ ] Base currency: **LKR**
- [ ] Fiscal year start: confirm with accountant (TB used Apr–Mar)
- [ ] Company TIN / VAT number stored for invoice footer

## 2. Chart of Accounts

Create accounts from [CHART_OF_ACCOUNTS.md](CHART_OF_ACCOUNTS.md).

Minimum must-exist list:

- Inventory Asset  
- Account Receivable  
- Account Payables  
- All bank + petty cash ledgers from BS  
- VAT Control Account  
- VAT Paid (input)  
- WHT Receivable  
- Director current accounts (Nimanda, Ravindu Nimans)  
- Share capital splits  
- Retained Earnings  
- Sales Income / Commission / Other income  
- Cost of Goods Sold  
- Core expense accounts from TB  

## 3. Tax (bookkeeping now → 1B later)

- [ ] Create VAT rate (confirm current SL %)  
- [ ] Map sales tax to VAT Control / output  
- [ ] Map purchase tax to VAT Paid / input  
- [ ] Post a sample sales invoice + purchase bill; verify TB tax lines  
- [ ] Document accountant export process until in-app SL VAT pack lands  

## 4. Inventory

- [ ] Default warehouse(s)  
- [ ] Costing method (FIFO or Average — confirm with accountant)  
- [ ] Inventory asset + COGS accounts linked  

## 5. Opening balances

- [ ] Choose cutover date  
- [ ] Export fresh TB from old system that day  
- [ ] Fill opening balance table in CHART_OF_ACCOUNTS.md  
- [ ] Load into Bigcapital  
- [ ] Prove: new TB debits = credits  
- [ ] Prove: BS total assets = equity + liabilities  

## 6. Smoke tests

| Test | Expected |
|------|----------|
| Sales invoice with VAT | AR + Sales + VAT + COGS/Inventory move |
| Customer payment | Bank up, AR down |
| Purchase bill with stock | Inventory up, AP up, input VAT |
| Vendor payment | AP down, Bank down |
| Warehouse transfer | Locations change; P&L unchanged |

## Opening balance worksheet (CSV)

See [opening-balances.template.csv](opening-balances.template.csv).
