# DMS event → Bigcapital posting matrix

Contract between **Astrans DMS** (operations) and **Bigcapital** (accounting + inventory valuation).

Every row is an **event ledger** posting: stock and/or money effects.

| # | DMS operational event | Stock effect | Money / GL effect | Bigcapital document / posting |
|---|----------------------|--------------|-------------------|-------------------------------|
| 1 | Sale confirmed (order → invoice) | Decrease inventory (if stock item) | Dr AR (what customer owes); Cr Sales / Inventory / COGS at **lot cost**; Cr VAT Control (output); Dr/Cr **4410 Selling price variance** = Secondary P&L | Sales Invoice (+ inventory COGS) |
| 2 | Customer collection received | None | Dr Bank/Cash; Cr AR | Customer payment / receive payment |
| 3 | Purchase / GRN + supplier bill | Increase inventory | Dr Inventory (or Expense); Dr VAT Paid/input; Cr AP | Purchase bill / bill + inventory receipt |
| 4 | Supplier payment made | None | Dr AP; Cr Bank/Cash | Vendor payment |
| 5 | Stock issued to van / route / branch | Transfer or issue between warehouses | Usually no P&L if pure transfer; inventory locations change | Inventory transfer / warehouse transfer |
| 6 | Stock returned from customer / van | Increase inventory (if restockable) | Reverse or credit-note sales/COGS/VAT as applicable | Credit note + inventory adjustment |
| 7 | Stock write-off / damage | Decrease inventory | Dr Expense / COGS; Cr Inventory | Inventory adjustment + journal if needed |
| 8 | Expense recorded (fuel, rent, salary) | None | Dr Expense; Cr Bank/AP/Cash; VAT if taxable | Expense or bill |
| 9 | Bank / cash transfer | None | Dr Bank A; Cr Bank B | Transfer / journal |
| 10 | Manual adjustment | Optional | Balancing debits/credits | Manual journal |
| 11 | Opening balance load (cutover) | Opening stock qty/value | Opening AR/AP/banks/equity/VAT | Opening balances / opening journal |

## Posting rules (v1)

1. **DMS never posts silently to GL** without a mapped event above.  
2. Prefer **Bigcapital native documents** (invoice, bill, payment, transfer) over raw journals.  
3. Journals are for exceptions only.  
4. VAT: every taxable sale/purchase must carry the configured SL VAT rate and hit VAT accounts.  
5. Idempotency: each DMS event ID posts at most once (store Bigcapital document ID on the DMS event).  

## Integration approach

```text
Astrans DMS event (committed)
  → Adapter validates mapping
  → Bigcapital API / document create
  → Store external_id + status on DMS event
  → Failures go to retry / ops alert queue (batched, short jobs)
```

If Bigcapital API coverage is incomplete for a row, use:

1. Document type that exists, or  
2. Controlled journal with same economic effect, documented in this matrix.

## Out of scope for Bigcapital (ops only in DMS)

- Route planning / salesman beat  
- Van load sheet UX  
- Credit limit enforcement in the field  
- Territory hierarchy screens  
- Delivery scheduling UI  

Those create events that **still** must land in this matrix when stock or money moves.
