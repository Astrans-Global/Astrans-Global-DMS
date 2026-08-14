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

- Settings: VAT % (default 18, `astrans_ops.default_vat_rate_percent`).
- GRN (Bill) VAT is **one flat rate for the whole bill**, never per line. The
  Bill form has a single **bill-level "Tax rate" selector** in the totals
  footer (same place/behaviour as the bill-level discount %), which is a
  dropdown of the org's existing saved Tax Rates — exactly like the native
  per-line tax rate picker, just chosen once and stamped onto every line
  under the hood so Bigcapital's own tax-rate aggregation/GL posting keeps
  working unmodified. There is deliberately no per-line tax-rate column on
  the Bill form.
- GRN lines are entered as VAT-**excluded** list prices with each line's own
  discount %; the bill can also carry a header-level discount allocated
  proportionally across lines (ex-VAT basis).
- Each item price-lot stores `list_price_excl_vat` + effective `discount_percent`
  (line discount + proportional share of any header discount, collapsed to
  one %) + a `vat_rate_percent` snapshot — **not** a single collapsed net-cost
  figure. `unit_cost_net` (VAT-inclusive, the "lot cost" used for COGS/AP) is
  always *derived* from those three: `list_price_excl_vat × (1 − discount_percent/100) × (1 + vat_rate_percent/100)`,
  rounded to 2dp. Storing price/discount/VAT separately (rather than one net
  number) is what lets both accounting and invoice display come from the
  same row.
- A GRN line only opens a **new lot** when its (list price, discount %, VAT %)
  triple differs from an existing lot for the same item + warehouse;
  otherwise its quantity merges into that lot.
- Every delivered invoice **stores** VAT internally (header + lines) for later 1B filing.
- Invoice unit-price display (same grand total either way — see Secondary P&L formula, which always uses VAT-inclusive `lot_net`/`sell_net`):
  - **Non-VAT invoice** (no customer TIN): unit price = VAT-**inclusive** final price
    (`list_price_excl_vat × (1 − discount%) × (1 + vat%)`), discount shown
    separately; no VAT line.
  - **VAT invoice** (customer has TIN): unit price = VAT-**excluded** final
    price (`list_price_excl_vat × (1 − discount%)`), with VAT computed on the
    bill subtotal and shown as a separate total line.
  - Accounts Payable, COGS and Vendor/Customer Due always use the
    VAT-inclusive figure regardless of which invoice print format is used.
- Bills always compute tax as **exclusive-of-tax** — Bigcapital's own
  "Amounts are" inclusive/exclusive picker (present on Estimates/Invoices/
  Credit Notes) is replaced on the Bill form with a static "Exclusive of
  Tax" notice; it is not user-editable, because switching a bill to
  inclusive-of-tax would desync `ComputeItemPriceLotCost.ts`, which always
  assumes an exclusive-tax GRN line.
- `bill_vat_records` (one row per opened Bill/GRN: `bill_id`, `bill_number`,
  `bill_date`, `vendor_id`, `vat_rate_percent`, `taxable_amount`,
  `vat_amount`) is a purpose-built snapshot table for the future VAT module
  (Sri Lanka 1B input-VAT schedule), kept in sync by
  `RecordBillVatFromBillService` on Bill create/edit/delete. `taxable_amount`
  + `vat_amount` are derived the same way as `unit_cost_net` (single flat
  bill-level rate, net of line + header discounts) — **not** Bigcapital's
  own per-line `tax_amount`, which is computed pre-discount and only drives
  GL/AP posting.

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

Line: VAT-excl list price, line discount %. Optional bill-header extra
discount **allocated proportionally into lot net** (ex-VAT basis). VAT is
never per line — one bill-level tax-rate selection (dropdown of saved Tax
Rates, see "VAT" above) applies to the whole bill; `unit_cost_net` is then
`list_price_excl_vat × (1 − discount%) × (1 + vat%)`.

Each lot: `real_qty`, `reserved_qty`, `float_qty = real − reserved`.

Implemented (server): `item_price_lots` + `item_price_lot_receipts` tables,
`ComputeItemPriceLotCost.ts`, `RecordItemPriceLotsFromBillService`
(subscribes to Bill create/edit/delete events), `GET /api/item-price-lots`
read endpoint. Also `bill_vat_records` (see "VAT" above) via
`RecordBillVatFromBillService`, same event set. Pending: invoice-side lot
picker (`invoice-lot-picker` task).

## Customers

Start **Category B**. A–D engine needs **cleared** payments (not PDC received). Phase 1: status stays B unless a test “mark settled (cleared)” stub is used. Unpaid delivered invoices show on the invoice screen.

## Books adapter

Idempotent `external_id`. Store Bigcapital document ids on DMS GRN / delivered invoice. Failures do not invent silent journals.
