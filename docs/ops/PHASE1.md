# Phase 1 — Astrans ops (DMS) + Books ledger

Ops system of record = **Astrans DMS**.  
Statutory books = **Bigcapital**, posted only on **GRN** and **Delivered**.

Reset point: git tag `pre-ops-phase1` (`3e92fee`). Revert: `git checkout pre-ops-phase1`.

## Secondary P&L

Ex-VAT nets (VAT is a pass-through tax, not trading profit, so it's excluded
from both sides of the comparison — see "Statutory posting" below for how
the VAT-inclusive customer/GL amounts still balance separately):

```text
lot_net  = lot_list × (1 − lot_discount%)
sell_net = sell_list × (1 − sell_discount%)
line_pnl = qty × (sell_net − lot_net)
invoice_pnl = sum(line_pnl)
```

Example: lot 100 @ 10% (net 90), sell 5 × 120 @ 10% (net 108) → **+90**, not +40.

Green = profit, red = loss. Report filters: warehouse, area, date range.
Shows one row per **Delivered** invoice only (Pending/Reserved/Invoiced
aren't real sales yet), with invoice P&L and a grand total.

Implemented (server): `sale_invoice_line_pnls` (one row per lot-picked
invoice line: `lot_net_per_unit`, `sell_net_per_unit`, `quantity`,
`line_pnl`), `RecordSaleInvoiceLinePnlService` (recomputes/replaces a
Delivered invoice's rows — `sell_net_per_unit` reuses
`computeItemPriceLotUnitCosts`, the same header-discount-allocation math as
the GRN side, just applied to the invoice's own header discount instead of
the bill's), `SaleInvoiceWriteLinePnlSubscriber` (same
delivered/created-delivered/edited-while-delivered/deleted gating as the
lot-reservation subscriber), `GET /api/reports/secondary-pnl` (filters:
`warehouseId`, `areaId`, `dateFrom`, `dateTo`; joins to the invoice, its
customer, and the customer's area). Implemented (webapp): Reports → Astrans
DMS → Secondary P&L page (`SecondaryPnl.tsx`), green/red P&L cells, totals
footer.

## Delivery Prep

Worklist screen for what still needs to go out on the vans -- **not** a
report on finished sales (that's Secondary P&L above, Delivered-only); this
one defaults to showing **Pending + Reserved** invoices (the ones not yet
out the door) and lets you also tick in Invoiced if you need it. **Delivered
invoices never show here, full stop** -- they've already gone out, there's
nothing left to prep, so "Delivered" isn't even offered as a Status
tick-box option, and the server excludes `dmsStatus = 'delivered'`
unconditionally (not just "whenever the Status filter happens to leave it
unticked"). This also excludes pre-Phase-1 invoices with no `dmsStatus` set
at all, since those are treated as already-Delivered (see "Status
pipeline" below, "Existing invoices").
Read-only: ticking invoices here has zero effect on their status, stock, or
the ledger -- it only feeds the totals panel below the table so warehouse
staff can see how many of each item (and total litres) to pull for whatever
they've ticked.

Filters: Warehouse (single-pick), Area (single-pick), Route City (tick-box,
pick any number), Status (tick-box: Pending/Reserved/Invoiced only, pick any
number, defaults to Pending+Reserved ticked), invoice date range. Route
City's option list narrows to the selected Area's cities once an Area is
picked (same cascading behaviour as the customer form), and ticked Route
Cities are cleared whenever the Area changes since they'd no longer make
sense.

Totals panel: quantity per item across every currently-ticked invoice, plus
each item's litres (`quantity × item.pack_size_litres` -- items with no
pack size set still count toward quantity, just not litres) and a grand
total litres figure. Recalculates live as tick-boxes change; nothing is
saved.

Implemented (server): `GET /api/delivery-prep/invoices` (filters:
`warehouseId`, `areaId`, `routeCityId` comma-list, `dmsStatus` comma-list,
`dateFrom`, `dateTo` -- joins `sales_invoices` to `contacts`,
`customer_areas`, `customer_route_cities`, `warehouses`; read-only, no new
tables), `GET /api/delivery-prep/totals?invoiceIds=1,2,3` (sums
`items_entries.quantity` grouped by item for the given invoice ids,
multiplies by `items.pack_size_litres` for the litres figure).
Implemented (webapp): Sales → Delivery Prep (`DeliveryPrep.tsx`), route
`/delivery-prep`; the Route City / Status tick-box dropdowns are a small
reusable `CheckboxMultiSelectFilter` (a `Popover` + `Menu` of `MenuItem`s
with `shouldDismissPopover={false}` so ticking one option doesn't close the
dropdown) in `DeliveryPrep/components.tsx`; the invoice table uses the
existing `DataTable` `selectionColumn` tick-box-column feature (also used by
the Invoices list's bulk-select) rather than anything new.

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
- **Every invoice is always calculated/posted internally as VAT-inclusive**
  (subtotal + VAT = total), regardless of whether the customer is
  VAT-registered. "Non-VAT invoice" vs. "VAT invoice" is purely a **print
  format** choice made at PDF/Excel output time (see "Invoice numbers" and
  the future `invoice_templates` task) — not a different internal
  calculation:
  - Every invoice line's stored `rate` is always the VAT-**excluded** list
    price (same as the item price-lot it was sold from); VAT is always
    added once, on the invoice subtotal, via the single invoice-level tax
    rate below.
  - **VAT invoice** print (customer has TIN): shows that same VAT-excluded
    unit price as-is, with VAT broken out as a separate total line.
  - **Non-VAT invoice** print (no customer TIN): unit price is **grossed
    up** for display (`rate × (1 − discount%) × (1 + vat%)`), VAT is not
    broken out — the printed grand total is identical either way.
  - Accounts Payable/Receivable, COGS and Customer Due always use the
    VAT-inclusive figure, independent of which print format was used.
- The Invoice form has the same single **invoice-level "Tax rate"
  selector** in the totals footer as the Bill form (dropdown of the org's
  saved Tax Rates, stamped onto every line under the hood) — never a
  per-line tax rate, and the "Amounts are" picker is likewise replaced with
  a static "Exclusive of Tax" notice. Mirrors the Bill-side reasoning
  exactly (see `ComputeItemPriceLotCost.ts` assumptions).
- Bills always compute tax as **exclusive-of-tax** — Bigcapital's own
  "Amounts are" inclusive/exclusive picker (present on Estimates/Credit
  Notes) is replaced on the Bill and Invoice forms with a static "Exclusive
  of Tax" notice; it is not user-editable, because switching to
  inclusive-of-tax would desync `ComputeItemPriceLotCost.ts`, which always
  assumes an exclusive-tax line.
- `sale_invoice_vat_records` (one row per **Delivered** invoice:
  `sale_invoice_id`, `invoice_no`, `invoice_date`, `customer_id`,
  `is_vat_customer` — snapshot of whether the customer had a TIN at
  delivery time, `vat_rate_percent`, `taxable_amount`, `vat_amount`) is the
  output-VAT mirror of `bill_vat_records`, kept in sync by
  `RecordSaleInvoiceVatFromInvoiceService` on invoice
  delivered/created-delivered/edited-while-delivered/deleted. Only
  Delivered invoices are recorded (Pending/Reserved/Invoiced aren't real
  sales yet).
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

- Per-area `QQ` (`customer_areas.invoice_number_code`, resolved from the
  invoice's **customer's** area -- there's no separate Area field on the
  invoice itself) and sequence starting at **10001**
  (`customer_areas.next_invoice_number`), never reset/padded beyond that.
- `YYMMM` is always **today's** date -- the date the number is actually
  generated -- not necessarily the same as the Invoice Date fixed later at
  Delivered.
- `invoice_no` is **left blank** through Pending/Reserved (Bigcapital's own
  `sales_invoices` auto-increment setting is no longer used for new
  invoices -- see "Gotcha" below). Assigned at **Invoiced** (or at
  **Delivered** if Invoiced was skipped).
- Revert from Invoiced back to Pending/Reserved **burns** the number (blanks
  `invoice_no`, sequence does not roll back); next Invoiced/Delivered gets a
  new one. Invoiced -> Delivered keeps the same number.
- Errors if the customer has no Area, or the Area has no `invoice_number_code`
  set yet, at the moment a number would be assigned.

Implemented (server): `GenerateSaleInvoiceNumberService`
(`assignNumberIfMissing` / `burnNumber`, both transactional and row-locking
the area to avoid two invoices racing for the same sequence number), called
from `InvoiceDmsStatusService.setStatus` on every status transition.
`CommandSaleInvoiceDTOTransformer` no longer calls Bigcapital's
`SaleInvoiceIncrement`/`AutoIncrementOrdersService` nor requires
`invoiceNo` to be present -- both are effectively dormant for Sale Invoices
now (kept registered/untouched to avoid breaking DI, just unused).
Implemented (webapp): `InvoiceFormInvoiceNumberField` is now a read-only
display (was a free-text/auto-increment field) showing the assigned number
or an italic "Assigned automatically once moved to \"Invoiced\"" hint while
blank.

## Status pipeline

| Status | Number | Stock | GL |
|--------|--------|-------|----|
| Pending | no | none | no |
| Reserved | no | reserved ↑ (float = real − reserved) | no |
| Invoiced | yes | stays reserved | no |
| Delivered | yes; user sets invoice date | real ↓, reserved ↓ | post once |

Max **10** item rows. Editable until Delivered. After Delivered, phase 1 allows reverse+repost; hard lock after payment + bank rec is **phase 2**.

Implemented (server): `sales_invoices.dms_status` column (own field, layered
on top of Bigcapital's native `delivered_at`, which still gates GL/inventory
posting), `item_price_lot_reservations` table (mirrors
`item_price_lot_receipts` for the sell side), `InvoiceLotReservationService`
(reserve/release/consume, blocks oversell against a lot's `float_qty`),
`InvoiceDmsStatusService` + `PUT /api/sale-invoices/:id/dms-status`
(Reserved/Invoiced hold stock via reservations; Delivered drives Bigcapital's
own native deliver action so GL/inventory post exactly as they already do),
`InvoiceLotReservationSyncSubscriber` (keeps reservations/`dms_status`/the
invoice number in sync on invoice edit/delete/native-deliver -- Bigcapital's
own "Save and Deliver" button can reach `deliveredAt` directly on **create**
or on an **edit** of an existing Pending/Reserved/Invoiced invoice, bypassing
`InvoiceDmsStatusService` entirely; this subscriber detects both cases and
runs the exact same reserve → consume → assign-number → sync-status sequence
so a Delivered invoice can never end up without a number or with stock not
actually decremented, no matter which button delivered it). Implemented
(webapp): a "Status: ..." button + "Move to..." menu in the invoice form's
top bar (see "Changing an invoice's DMS status" below for exactly where) and
a DMS Status column on the invoice list, both wired to that endpoint.
Invoice numbering now uses the real per-area `YYMMM_ASTRANSQQ_XXXXX` format
-- see "Invoice numbers" above (no longer Bigcapital's plain
auto-numbering).

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
read endpoint (`item_id`/`warehouse_id`/`exclude_invoice_id` filters — the
last adds an invoice's own active holds back into `float_qty` so re-opening
it doesn't look more constrained than it really is). Also `bill_vat_records`
(see "VAT" above) via `RecordBillVatFromBillService`, same event set.

Implemented (webapp): invoice-line price-lot picker (`ItemsEntriesTable`
gains an opt-in "Price lot" column, invoices-only via `enablePriceLots`;
picking a lot fills in that line's price/discount from the lot's own values,
still editable after, and records `item_price_lot_id` on the line). Picker
and stock-hold quantities are scoped to the invoice's own selected
warehouse.

## Customers

Start **Category B** (`risk_category`, default `B`, one of A/B/C/D). A–D engine
needs **cleared** payments (not PDC received). Phase 1: status stays B unless
a test "mark settled (cleared)" stub is used. Unpaid delivered invoices show
on the invoice screen.

### Areas & Route Cities

New taxonomies, same pattern as Item Categories/Subcategories (own list page
+ dialog, quick "+ create" from any select that uses them):

- **Area**: `name` (unique), `invoice_number_code` (2 letters/digits, unique —
  the `QQ` in `YYMMM_ASTRANSQQ_XXXXX`, stored now for later invoice-numbering
  wiring), `next_invoice_number` (default `10001`, stored now, not yet
  consumed). Managed at Contacts → Areas.
- **Route City**: `name`, belongs to exactly one **Area** (`area_id`), unique
  per area. Managed at Contacts → Route Cities; the customer form's Route
  City dropdown is filtered to the currently-selected Area and resets
  whenever the Area changes.
- Both are **required** fields on every customer (Area first, then Route
  City). A route city can't be assigned to a customer under a different area
  than its own (server-side consistency check).
- Deleting an Area/Route City is blocked while it still has route
  cities/customers attached.

Implemented (server): `customer_areas` + `customer_route_cities` tables,
`CustomerAreaModule` / `CustomerRouteCityModule` (full CRUD, uniqueness +
dependency validation), `contacts.area_id` / `contacts.route_city_id` foreign
keys. Implemented (webapp): `CustomerAreasList` / `CustomerRouteCitiesList`
pages + form dialogs, `CustomerAreaSelect` / `CustomerRouteCitySelect`
cascading dropdowns (with inline "+ create" like the Tax Rate picker), wired
into the customer form.

### Extended customer profile

Added directly to the existing `contacts` table (customers and vendors share
it, but these fields are customer-facing only for now):

- **Call Name** — this *is* Bigcapital's existing `display_name` field, just
  relabelled on the customer form/list (the name that prints on invoices).
  There's no separate "Contact Person" field — the existing Salutation +
  First/Last Name fields cover that.
- **Customer Code** — auto-generated on create as `{AreaCode}-{seq}` (e.g.
  `QQ-0001`), one running sequence per Area (`customer_areas.next_customer_number`,
  independent of the invoice-number sequence). Read-only on the form; never
  accepted from the client, always stamped server-side inside the same
  transaction as the insert.
- **Phone 1 / Phone 2** — Bigcapital's existing `work_phone` / `personal_phone`
  fields, relabelled (both optional). The separate phone fields on the
  Billing/Shipping address sections were removed (redundant with these).
- **VAT / TIN Number** (`tin_number`) — optional, must be exactly 9 digits
  when provided; also determines VAT vs non-VAT invoice printing (see "VAT"
  above).
- **Address line 3** (`billing_address3` / `shipping_address3`) — third line
  added alongside Bigcapital's existing address line 1/2 fields, both
  billing and shipping. Shipping address has a "Same as billing address"
  checkbox that mirrors + locks the shipping fields to the billing ones
  while ticked (webapp-only convenience, not a stored field).

No backfill was needed — the customers list was empty at rollout time, so
Area/Route City are enforced as required from the very first customer
created.

## Books adapter

Idempotent `external_id`. Store Bigcapital document ids on DMS GRN / delivered invoice. Failures do not invent silent journals.

## Gotcha: DTO field naming (server)

The global `SerializeInterceptor` (`packages/server/src/common/interceptors/serialize.interceptor.ts`)
already rewrites every incoming request body/query key from snake_case to
camelCase **before** `ValidationPipe`/`class-transformer` binds the DTO. New
DTO fields must therefore just be named in plain camelCase
(`areaId: number`) — **never** add `@Expose({ name: 'area_id' })` to "bridge"
snake_case, since by that point the snake_case key no longer exists and the
field will silently come back `undefined`. This exact mistake broke Route
City creation and Item category/subcategory/pack-size assignment for a
while (fixed 2026-08-17) — don't reintroduce it.

## Gotcha: Sale Invoice numbering is no longer Bigcapital's auto-increment

The `sales_invoices` settings group (`next_number` / `number_prefix` /
`auto_increment`, Settings → Sales → Invoices) and its
`SaleInvoiceIncrement` / `AutoIncrementOrdersService` plumbing still exist
and still get bumped on every invoice create (`SaleInvoiceAutoIncrementSubscriber`)
but are otherwise **dead** for Sale Invoices — don't be misled by that
settings screen still being there, or by that counter still incrementing.
The real number now always comes from `GenerateSaleInvoiceNumberService`
(see "Invoice numbers"). If a customer has no Area, or their Area has no
`invoice_number_code` set, moving an invoice to Invoiced/Delivered fails
loudly (`CUSTOMER_HAS_NO_AREA` / `AREA_MISSING_INVOICE_CODE`) rather than
silently falling back to the old numbering.

## Gotcha: the Warehouse picker needs Bigcapital's "Warehouses" feature turned on

Bigcapital ships multi-warehouse support behind a per-org on/off switch
(`features.warehouses` setting, default **off**). While it's off, the
Warehouse selector is hidden everywhere (Bill/Invoice top bar included) —
this is stock Bigcapital behaviour, not an Astrans DMS bug, but it means a
brand-new org (like this one) needs a one-time, in-app activation step
before the invoice-lot picker/reservations (which are scoped to the
invoice's own warehouse) become usable: **Preferences → Warehouses →
Activate** (creates a "Primary" warehouse automatically). No code/deploy
involved. Same on/off switch also independently gates the Branches
selector, unrelated to Astrans DMS.

## Note: there is no separate "Area" field on the invoice itself

Area only lives on the **customer** (required at customer-create time — see
"Areas & Route Cities" above); the invoice resolves it from
`invoice.customer.area` purely to pick the right `invoice_number_code` at
Invoiced/Delivered (see "Invoice numbers"). Nothing is stored on the invoice
for Area.

The invoice form does have an **Area filter** dropdown next to the customer
picker (added 2026-08-18) — but it's webapp-only convenience, not a form
field: picking an Area there just narrows the Customer dropdown's option
list to that Area's customers, to make a long customer list quicker to
search; it's not submitted with the invoice and has no server-side effect.
Implemented (webapp): `InvoiceFormAreaFilter` in
`InvoiceFormHeaderFields.tsx` (local `useState`, filters the `customers`
array on `customer.area_id` before handing it to `CustomersSelect`).

## Changing an invoice's DMS status (Pending/Reserved/Invoiced/Delivered)

The "Status: ..." button lives in the invoice form's **top bar**, top-right
(next to the Warehouse/Branch pickers if those features are on) — click it
to open a menu of the other statuses to move to (see "Status pipeline"
above for what each transition does). It only becomes clickable once the
invoice has been saved at least once (brand-new/unsaved invoices show a
disabled "Status: Pending" button, since there's no invoice id yet to call
the status endpoint against) and is permanently disabled once the invoice
is **Delivered** (that transition is final in phase 1). This control used
to live in a small bar above the item entries table, which was easy to
miss — moved into the top bar 2026-08-18 for visibility. Implemented
(webapp): `InvoiceDmsStatusControl`, mounted from `InvoiceFormTopBar`.

## Renaming a warehouse (including "Primary")

Right-clicking a warehouse box under **Preferences → Warehouses** always
opened an Edit/Delete/Make Primary context menu (including for "Primary"
itself — nothing stops the primary warehouse's `name` from being edited,
Bigcapital just doesn't call it out anywhere), but right-click is not
discoverable, so a small "..." button was added to the top-right corner of
every warehouse box (2026-08-18) that opens the same menu on a normal
click. Implemented (webapp): `WarehousesGridItemBox` /
`WarehouseContextMenu` in `Preferences/Warehouses/components.tsx`.
