# Astrans → Bigcapital Chart of Accounts

Base currency: **LKR**  
Sources: Balance Sheet 2024-07-28 + Trial Balance FY 2021/22 screenshots.

Use this as the setup checklist inside Bigcapital after first login.

## Account type mapping

| Astrans type | Bigcapital type | Notes |
|--------------|-----------------|-------|
| Fixed Asset | Fixed asset | Vehicles, furniture, plant, IT |
| Bank / Cash | Bank / cash | One account per bank ledger + petty cash |
| Inventory Asset | Inventory / other current asset | Link to inventory module |
| AR | Accounts receivable | Control account |
| AP | Accounts payable | Control account |
| Staff Loan / WHT / VAT Paid | Other current asset | Tax recoverables |
| Director Current Accounts | Long-term liability (or equity-related) | Keep named per director |
| Share Capital (by person) | Equity | Split capital accounts |
| Retained Earnings / Net Income | Equity | Net Income usually system-derived |
| VAT Control | Other current liability / tax | Can flip sign by period |
| Sales / Commission / Interest | Income | Split revenue streams if needed |
| COGS | Cost of goods sold | Linked to inventory costing |
| Operating expenses | Expense | Recreate full list from TB |

## Target COA list (starter — expand to match live books)

Suggested codes are placeholders; renumber to match accountant preference.

### Assets

| Code | Name | Type |
|------|------|------|
| 1100 | Motor Vehicle - Toyota Corolla | Fixed asset |
| 1110 | Motor Vehicles - LC PL | Fixed asset |
| 1200 | Fixture & Furniture | Fixed asset |
| 1210 | Office Furniture (Old) | Fixed asset |
| 1220 | Office Furniture (New) | Fixed asset |
| 1300 | IT Equipment | Fixed asset |
| 1400 | Plant & Machinery | Fixed asset |
| 1500 | Inventory Asset | Inventory |
| 1600 | Account Receivable | AR |
| 1700 | Staff Loan | Other current asset |
| 1800 | WHT Receivable | Other current asset |
| 1810 | VAT Paid (Input VAT) | Other current asset |
| 1820 | Income Tax (CP) | Other current asset |
| 1900 | Hatton National Bank - 34375 | Bank |
| 1910 | Nations Trust Bank - 200070264082 | Bank |
| 1911 | Nations Trust Bank - 100070015453 | Bank |
| 1912 | Nations Trust Bank - 15540 | Bank |
| 1913 | Nations Trust Bank - 200070119095 | Bank |
| 1920 | Peoples Bank | Bank |
| 1930 | Seylan Bank | Bank |
| 1940 | Petty cash Lahiru | Cash |
| 1941 | Daily Cash / Cash in hand | Cash |

### Liabilities

| Code | Name | Type |
|------|------|------|
| 2100 | Account Payables | AP |
| 2200 | Director Current Account - Nimanda | Long-term liability |
| 2210 | Director Current Account - Ravindu Nimans | Long-term liability |
| 2300 | VAT Control Account | Other current liability / tax |

### Equity

| Code | Name | Type |
|------|------|------|
| 3100 | Share Capital - Nimanda | Equity |
| 3110 | Share Capital - Ravindu Nimans | Equity |
| 3120 | Share Capital - Sisira | Equity |
| 3200 | Retained Earnings | Equity |
| 3300 | Other Reserves | Equity |
| 3400 | Profit and Loss Account | Equity (legacy / mapping) |

### Income

| Code | Name | Type |
|------|------|------|
| 4100 | Sales Income | Income |
| 4110 | Sale / Commission | Income |
| 4120 | Commission | Income |
| 4200 | Revenue - Spare Parts | Income |
| 4210 | Revenue - Service | Income |
| 4300 | Interest Income | Income |
| 4400 | Other Income | Income |

### Cost & expenses

| Code | Name | Type |
|------|------|------|
| 5100 | Cost of Goods Sold | COGS |
| 6100 | Salaries | Expense |
| 6200 | Consulting Fees | Expense |
| 6210 | Audit Fee | Expense |
| 6300 | Bank Charges | Expense |
| 6400 | Electricity | Expense |
| 6410 | Internet | Expense |
| 6420 | Water | Expense |
| 6430 | Telephone | Expense |
| 6500 | Printing | Expense |
| 6510 | Repairs | Expense |
| 6600 | Vehicle Fuel | Expense |
| 6700 | Travel / Selling & Distribution | Expense |
| 6800 | Rent | Expense |

## Opening balances (cutover template)

At go-live, pick a **cutover date**, export a fresh TB from the old system, and fill:

| Code | Account | Debit | Credit | Source |
|------|---------|-------|--------|--------|
| | | | | Paste from cutover TB |

Rules:

1. Debits must equal credits.  
2. Prefer the **latest** TB for money balances; BS screenshot is structural proof.  
3. Inventory quantity/cost must match warehouse count on cutover night.  
4. Do **not** import Net Income as an opening balance if Bigcapital derives it — use Retained Earnings instead.

## VAT account setup (bookkeeping + path to 1B)

### Phase A (immediate, bookkeeping)

- Tax rate: Sri Lanka VAT (confirm current %, e.g. 18%)  
- Sales invoices → output VAT → VAT Control  
- Purchase bills → input VAT → VAT Paid / VAT Control (match accountant’s preferred netting)  
- Keep **WHT Receivable** as a balance-sheet recoverable  

### Phase B (1B filing pack — after books live)

- VAT return schedule views (output, input, net payable/refundable)  
- Export for accountant / RAMIS-oriented columns  
- SSCL only if confirmed applicable  

## Setup order inside Bigcapital

1. Organization currency **LKR**  
2. Create COA accounts above  
3. Configure tax rates + tax accounts  
4. Create warehouses / items (inventory)  
5. Load opening balances  
6. Verify Trial Balance and Balance Sheet structure  
