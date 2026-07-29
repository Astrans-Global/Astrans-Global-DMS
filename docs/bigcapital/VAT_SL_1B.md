# Sri Lanka VAT — decision 1B roadmap

User decision: **1B** — custom Sri Lanka VAT return / schedules inside the app (not only generic tax).

## Phase A (blocking for books go-live)

Already covered by Bigcapital config:

- VAT rate on sales/purchases  
- Postings to VAT Control / VAT Paid  
- Tax liability style summaries for accountant  

Do not block Bigcapital deploy on RAMIS UI.

## Phase B (1B delivery)

Build after COA + day-to-day VAT postings are correct:

1. **VAT Output schedule** — taxable sales, exempt, zero-rated (as applicable), tax amount  
2. **VAT Input schedule** — purchases with recoverable VAT  
3. **Net VAT** — payable / refundable for the period  
4. **Export** — Excel matching accountant worksheet columns  
5. Optional later: SSCL, WHT certificates  

## Accounts already present in Astrans books

- VAT Control Account (BS)  
- VAT Paid (TB)  
- WHT Receivable  

Keep these names in Bigcapital so reports stay familiar.
