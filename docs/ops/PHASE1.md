# Phase 1 — Astrans ops (DMS) + Books ledger

Ops system of record = **Astrans DMS**.  
Statutory books = **Bigcapital**, posted only on **GRN** and **Delivered**.

Reset point: git tag `pre-ops-phase1` (`3e92fee`). Revert: `git checkout pre-ops-phase1`.

## Secondary P&L

VAT-inclusive nets:

```text
lot_net  = lot_list × (1 − lot_discount%)
sell_net = sell_list × (1 − sell_discount%)
line_pnl = qty × (sell_net − lot_net)
invoice_pnl = sum(line_pnl)
```

Example: lot 100 @ 10% (net 90), sell 5 × 120 @ 10% (net 108) → **+90**, not +40.

Green = profit, red = loss. Report filters: warehouse, area, date range. Show invoice numbers, line/invoice P&L, and total.

## Statutory posting (Delivered)

Customer owes **sell** amount. Inventory leaves at **lot** cost. Difference cannot vanish.

| | Debit | Credit |
|--|-------|--------|
| AR | what customer owes (VAT-incl / VAT-excl+VAT as configured) | |
| Sales | | lot net (ex-VAT equivalent as Books tax setup requires) |
| Inventory / COGS | COGS at lot cost | Inventory at lot cost |
| VAT output | | output VAT on the **sell** tax base (always stored) |
| **4410 Selling price variance** | loss | gain (`invoice_pnl`) |

Commission income is **phase 2** (supplier cheque). Do not mix into this posting.

Pending / Reserved / Invoiced: **no GL**.

## VAT

- Settings: VAT % (default 18).
- GRN: enter VAT-**excluded** prices; persist lots as VAT-**included** net cost.
- New VAT-incl net for same item + warehouse → **new lot**.
- Every delivered invoice **stores** VAT internally (header + lines) for later 1B filing.
- Print: TIN present → VAT invoice (ex-VAT lines, VAT shown on total). No TIN → Non-VAT print (VAT-incl unit prices, no VAT line). **Same grand total.**

## Invoice numbers

`YYMMM_ASTRANS{QQ}_{XXXXX}` e.g. `26AUG_ASTRANS01_10001`.

- Per-area `QQ` and sequence starting at **10001**.
- Assigned at **Invoiced** (or at **Delivered** if skipped).
- Revert from Invoiced **burns** the number; next Invoiced gets a new one.

## Status pipeline

| Status | Number | Stock | GL |
|--------|--------|-------|----|
| Pending | no | none | no |
| Reserved | no | reserved ↑ (float = real − reserved) | no |
| Invoiced | yes | stays reserved | no |
| Delivered | yes; user sets invoice date | real ↓, reserved ↓ | post once |

Max **10** item rows. Editable until Delivered. After Delivered, phase 1 allows reverse+repost; hard lock after payment + bank rec is **phase 2**.

## Lots / GRN

Line: VAT-excl list, line discount %. Optional bill-header extra discount **allocated proportionally into lot net** (documented default). Then × (1 + VAT%).

Each lot: `real_qty`, `reserved_qty`, `float_qty = real − reserved`.

## Customers

Start **Category B**. A–D engine needs **cleared** payments (not PDC received). Phase 1: status stays B unless a test “mark settled (cleared)” stub is used. Unpaid delivered invoices show on the invoice screen.

## Books adapter

Idempotent `external_id`. Store Bigcapital document ids on DMS GRN / delivered invoice. Failures do not invent silent journals.
