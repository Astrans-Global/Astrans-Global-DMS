# Scope split — Bigcapital vs Astrans DMS

## Bigcapital owns (accounting core)

Keep these in Bigcapital; do not rebuild them in Next.js unless we abandon Bigcapital later.

- Chart of Accounts  
- Double-entry journals and GL  
- Customers / vendors (financial subledgers)  
- Sales invoices, estimates, credit notes  
- Purchase bills / vendor payments  
- Expenses  
- Inventory item costing (FIFO/average), warehouses at accounting level  
- Bank accounts and reconciliation primitives  
- Tax rates + VAT control postings  
- Financial reports: Trial Balance, Balance Sheet, P&L, GL, AR/AP aging, inventory valuation  
- **Later (1B):** Sri Lanka–oriented VAT schedules / export packs  

## Astrans DMS owns (distribution operations)

Build these in Astrans Global DMS (Coolify-hosted Next.js or companion services):

- Order capture tailored to Astrans workflows  
- Van / route / territory operations  
- Load sheets and delivery runs  
- Field collections workflow and credit control UX  
- Approvals and role flows specific to Astrans  
- Operational stock issue / return screens that emit events  
- Integration adapter that posts into Bigcapital per [EVENT_POSTING_MATRIX.md](EVENT_POSTING_MATRIX.md)  
- Staff-facing dashboards that are ops-first (not accountant-first)  

## Shared concepts

| Concept | System of record | Notes |
|---------|------------------|-------|
| Customer financial balance | Bigcapital AR | DMS may cache for UX |
| Inventory qty by warehouse | Bigcapital inventory (+ DMS ops mirror if needed) | Single writer for cost/qty truth preferred |
| Invoice PDF for tax | Bigcapital (customize layout) | SL company/VAT footer |
| Route assignment | DMS only | No Bigcapital equivalent |

## Screens to keep vs replace

### Keep in Bigcapital (accountant)

- COA, journals  
- Invoices / bills / payments  
- TB / BS / P&L / aging  
- Tax settings  
- Inventory valuation reports  

### Replace / wrap with Astrans DMS UI (operations)

- Day-to-day order entry for vans  
- Collections on the road  
- Stock issue to route  
- Returns processing  
- Approvals  

### Build later (custom)

- Sri Lanka VAT return pack (decision **1B**)  
- SSCL if applicable  
- WHT certificates/schedules beyond receivable balance  

## Hosting notes

| Stage | Where |
|-------|--------|
| Now | VirtualBox Ubuntu + Coolify + Cloudflare tunnel `astransdms.xyz` |
| Later | Dedicated PC, same Coolify/Docker pattern |
| Not now | Paid Oracle Cloud shapes (forbidden by project rule) |

## Success definition

- Accountants use Bigcapital for books and reports  
- Ops staff use Astrans DMS for distribution day-to-day  
- Every stock/money event in DMS appears correctly in Bigcapital  
- VAT on invoices is correct; SL filing pack tracks toward 1B without blocking go-live books  
