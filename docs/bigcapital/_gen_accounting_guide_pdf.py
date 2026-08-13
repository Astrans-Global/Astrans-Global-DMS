"""Generate Astrans Books (Bigcapital) accounting guide PDF from project docs."""
from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "Astrans-Books-Accounting-Guide.pdf"


class GuidePDF(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Astrans Books - Accounting Guide (Bigcapital)", align="L")
        self.ln(10)

    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}  |  Internal - Astrans Global DMS", align="C")

    def h1(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(11, 61, 92)
        self.multi_cell(0, 9, text)
        self.ln(2)

    def h2(self, text: str) -> None:
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(11, 61, 92)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def h3(self, text: str) -> None:
        self.ln(1)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def body(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)

    def example_box(self, title: str, lines: list[str]) -> None:
        self.set_x(self.l_margin)
        self.set_fill_color(245, 248, 251)
        self.set_draw_color(11, 61, 92)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(11, 61, 92)
        self.multi_cell(0, 6, title)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        block = "\n".join(lines)
        self.multi_cell(0, 5, block, border=1, fill=True)
        self.ln(2)

    def table(self, headers: list[str], rows: list[list[str]], col_w: list[float]) -> None:
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(11, 61, 92)
        self.set_text_color(255, 255, 255)
        for h, w in zip(headers, col_w):
            self.cell(w, 6, h[:40], border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            if self.get_y() > self.h - 24:
                self.add_page()
                self.set_font("Helvetica", "B", 8)
                self.set_fill_color(11, 61, 92)
                self.set_text_color(255, 255, 255)
                for h, w in zip(headers, col_w):
                    self.cell(w, 6, h[:40], border=1, fill=True)
                self.ln()
                self.set_font("Helvetica", "", 8)
                self.set_text_color(30, 30, 30)
            self.set_fill_color(245, 248, 251) if fill else self.set_fill_color(255, 255, 255)
            self.set_x(self.l_margin)
            for cell, w in zip(row, col_w):
                text = cell.replace("\n", " ")
                if self.get_string_width(text) > w - 2:
                    while self.get_string_width(text + "...") > w - 2 and len(text) > 3:
                        text = text[:-1]
                    text = text + "..."
                self.cell(w, 6, text, border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)


def build() -> Path:
    pdf = GuidePDF(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    # Cover
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(11, 61, 92)
    pdf.ln(20)
    pdf.cell(0, 12, "Astrans Books", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 8, "How Bigcapital Handles Accounting", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(
        0,
        6,
        "Practical guide for Astrans Global (Pvt) Ltd - based on project docs "
        "(CHART_OF_ACCOUNTS, EVENT_POSTING_MATRIX, VAT_SL_1B). Currency: LKR.",
    )
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, "Books URL: https://books.astransdms.xyz", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.h1("1. Big picture")
    pdf.body(
        "Astrans uses two systems on purpose:\n"
        "- Astrans Books (Bigcapital) = accounting core: GL, AR/AP, inventory valuation, VAT postings, reports.\n"
        "- Astrans DMS = distribution ops: routes, vans, collections UX - not a second Trial Balance.\n\n"
        "When stock or money moves in the field, DMS should create an event that posts into Bigcapital "
        "as a real document (invoice, bill, payment, transfer), not a silent spreadsheet."
    )

    pdf.h2("What Bigcapital is good at")
    for b in [
        "Double-entry ledger that stays balanced",
        "Sales invoices, purchase bills, customer/vendor payments",
        "Inventory quantity + value (COGS when you sell stock items)",
        "Tax lines on documents (VAT rate -> VAT accounts)",
        "Financial statements: Trial Balance, P&L, Balance Sheet",
    ]:
        pdf.bullet(b)

    pdf.h2("What belongs in DMS (not rebuilt in Bigcapital screens)")
    for b in [
        "Route planning / salesman beats",
        "Van load sheets and delivery UX",
        "Field credit-limit enforcement UI",
        "Territory hierarchy screens",
    ]:
        pdf.bullet(b)
    pdf.body("Those ops flows still must produce events that hit the posting matrix when stock or money moves.")

    pdf.add_page()
    pdf.h1("2. Chart of Accounts (COA) - the filing system")
    pdf.body(
        "Every posting hits named accounts. Astrans starter COA (from project docs) groups like:"
    )
    pdf.table(
        ["Group", "Examples", "Role"],
        [
            ["Assets", "Inventory, AR, Banks, VAT Paid", "What we own / are owed"],
            ["Liabilities", "AP, VAT Control, Director CA", "What we owe"],
            ["Equity", "Share capital, Retained earnings", "Owners residual"],
            ["Income", "Sales, commission, interest", "Revenue"],
            ["COGS / Expense", "COGS, fuel, rent, salary", "Costs"],
        ],
        [32, 70, 75],
    )
    pdf.body(
        "Rule of thumb: pick the account that matches the economic reality. "
        "Do not invent SL tax accounts casually - keep VAT Control / VAT Paid names familiar to the accountant."
    )

    pdf.h1("3. Double-entry in one sentence")
    pdf.body(
        "Every transaction has at least two sides. Debits must equal credits. "
        "Bigcapital documents build those sides for you when you fill the form correctly."
    )

    pdf.add_page()
    pdf.h1("4. Day-to-day tasks with examples")

    pdf.h2("A) Sell goods on credit (Sales Invoice)")
    pdf.body(
        "Customer takes stock today; pays later. Bigcapital Sales Invoice decreases inventory "
        "(if stock item), raises AR, records sales + output VAT, and posts COGS."
    )
    pdf.example_box(
        "Example - invoice LKR 100,000 + 18% VAT (illustrative rate)",
        [
            "Dr Accounts Receivable ............. 118,000",
            "   Cr Sales ........................ 100,000",
            "   Cr VAT Control (output) .......... 18,000",
            "Dr COGS ............................ (cost of items)",
            "   Cr Inventory .................... (same cost)",
            "",
            "DMS event: Sale confirmed -> Bigcapital Sales Invoice",
        ],
    )

    pdf.h2("B) Collect cash / bank from customer (Receive payment)")
    pdf.body("No stock movement. Clears AR into Bank/Cash.")
    pdf.example_box(
        "Example - customer pays LKR 50,000 to HNB",
        [
            "Dr Hatton National Bank ........... 50,000",
            "   Cr Accounts Receivable ......... 50,000",
            "",
            "DMS event: Customer collection received -> Payment Received",
        ],
    )

    pdf.h2("C) Buy stock from supplier (Bill / GRN)")
    pdf.body("Inventory goes up; we owe the supplier; recoverable input VAT may apply.")
    pdf.example_box(
        "Example - purchase LKR 40,000 + VAT 7,200",
        [
            "Dr Inventory ...................... 40,000",
            "Dr VAT Paid (input) ............... 7,200",
            "   Cr Accounts Payable ............ 47,200",
            "",
            "DMS event: Purchase / GRN + supplier bill -> Bill + inventory",
        ],
    )

    pdf.h2("D) Pay supplier")
    pdf.example_box(
        "Example - pay LKR 47,200 from bank",
        [
            "Dr Accounts Payable ............... 47,200",
            "   Cr Bank ........................ 47,200",
            "",
            "DMS event: Supplier payment made -> Vendor payment",
        ],
    )

    pdf.add_page()
    pdf.h2("E) Move stock to a van / branch (Inventory transfer)")
    pdf.body(
        "Usually no P&L hit if it is only a location change. Inventory leaves Warehouse A and arrives Warehouse B."
    )
    pdf.example_box(
        "Example - 20 cases to Van 03",
        [
            "Stock: Warehouse Main -20 cases",
            "Stock: Van 03 +20 cases",
            "Value: same inventory value (transfer, not sale)",
            "",
            "DMS event: Stock issued to van/route -> Inventory transfer",
        ],
    )

    pdf.h2("F) Customer / van return (Credit note)")
    pdf.body(
        "If goods come back restockable, reverse the sales economics with a credit note "
        "(and inventory increase). Exact VAT/COGS reverse depends on return type."
    )

    pdf.h2("G) Write-off / damage")
    pdf.example_box(
        "Example - damaged stock cost LKR 5,000",
        [
            "Dr Expense / COGS (write-off) ..... 5,000",
            "   Cr Inventory ................... 5,000",
            "",
            "DMS event: Stock write-off -> Inventory adjustment (+ journal if needed)",
        ],
    )

    pdf.h2("H) Operating expense (fuel, rent)")
    pdf.example_box(
        "Example - fuel LKR 12,000 paid from petty cash",
        [
            "Dr Fuel expense ................... 12,000",
            "   Cr Petty cash .................. 12,000",
            "",
            "DMS event: Expense recorded -> Expense / bill",
        ],
    )

    pdf.h2("I) Manual journal (exceptions only)")
    pdf.body(
        "Use for opening balances, rare corrections, or items with no native document. "
        "Still must balance. Prefer invoices/bills/payments whenever possible."
    )

    pdf.add_page()
    pdf.h1("5. DMS event -> Bigcapital posting matrix")
    pdf.body("Contract between ops and books (from EVENT_POSTING_MATRIX.md):")
    pdf.table(
        ["#", "DMS event", "Bigcapital document"],
        [
            ["1", "Sale confirmed", "Sales Invoice (+ COGS)"],
            ["2", "Customer collection", "Payment received"],
            ["3", "Purchase / GRN + bill", "Bill + inventory"],
            ["4", "Supplier payment", "Vendor payment"],
            ["5", "Stock to van/branch", "Inventory transfer"],
            ["6", "Stock return", "Credit note + inventory"],
            ["7", "Write-off / damage", "Inventory adjustment"],
            ["8", "Expense", "Expense / bill"],
            ["9", "Bank/cash transfer", "Transfer / journal"],
            ["10", "Manual adjustment", "Manual journal"],
            ["11", "Opening balances", "Opening journal / OB"],
        ],
        [12, 55, 110],
    )
    pdf.h3("Posting rules (v1)")
    for b in [
        "DMS never posts silently to GL without a mapped event.",
        "Prefer Bigcapital native documents over raw journals.",
        "Journals are for exceptions only.",
        "Taxable sales/purchases must carry VAT rate and hit VAT accounts.",
        "Each DMS event ID posts at most once (store Bigcapital document id).",
    ]:
        pdf.bullet(b)

    pdf.add_page()
    pdf.h1("6. VAT - decision 1B (project rule)")
    pdf.body(
        "Phase A (go-live books): configure VAT rates on sales/purchases; post to "
        "VAT Control / VAT Paid; give the accountant tax liability style summaries. "
        "Do not block deploy on a full RAMIS UI.\n\n"
        "Phase B (later): Sri Lanka VAT output/input schedules, net VAT payable/refundable, "
        "Excel export matching accountant columns. Optional later: SSCL, WHT certificates.\n\n"
        "Keep familiar account names: VAT Control Account, VAT Paid, WHT Receivable."
    )
    pdf.body(
        "Numbers in earlier examples used an illustrative 18% only to show the shape of entries. "
        "Always use the VAT rates configured in Astrans Books for live postings."
    )

    pdf.h1("7. Reports you use in Bigcapital")
    pdf.table(
        ["Report", "Question it answers"],
        [
            ["Trial Balance", "Do all accounts balance this period?"],
            ["Profit & Loss", "Did we make profit? Which income/expense?"],
            ["Balance Sheet", "What do we own/owe on a date?"],
            ["AR / AP aging", "Who owes us / whom we owe, by age"],
            ["Inventory valuation", "Stock qty and value on hand"],
            ["Tax / VAT summaries", "Output vs input for the period (Phase A)"],
        ],
        [45, 132],
    )

    pdf.add_page()
    pdf.h1("8. Click-path cheat sheet (Astrans Books)")
    pdf.h3("Sell")
    pdf.bullet("Sales -> Invoices -> New invoice -> add customer & lines -> publish/deliver as required")
    pdf.h3("Collect")
    pdf.bullet("Sales / Payments received -> apply against invoice(s) -> choose bank/cash account")
    pdf.h3("Buy")
    pdf.bullet("Purchases -> Bills -> New bill -> supplier, items, tax -> receive inventory if needed")
    pdf.h3("Pay supplier")
    pdf.bullet("Purchases / Payments made -> apply to bill(s)")
    pdf.h3("Move stock")
    pdf.bullet("Inventory / Warehouses -> Transfer between warehouses (Main <-> Van)")
    pdf.h3("Expense")
    pdf.bullet("Expenses -> New expense -> category, payment account, tax if any")
    pdf.h3("Check books")
    pdf.bullet("Accounting / Reports -> Trial Balance, P&L, Balance Sheet")

    pdf.h1("9. Users, login, and passwords (ops note)")
    pdf.body(
        "Invite staff from Preferences -> Users (do not use public Sign up - it is disabled). "
        "Forgot password emails go out via configured Gmail SMTP (MAIL_* on the VM). "
        "Invited users do not need Google App Passwords; only the server mail account does."
    )

    pdf.h1("10. Where this comes from")
    for b in [
        "docs/bigcapital/README.md",
        "docs/bigcapital/CHART_OF_ACCOUNTS.md",
        "docs/bigcapital/EVENT_POSTING_MATRIX.md",
        "docs/bigcapital/VAT_SL_1B.md",
        "docs/bigcapital/DMS_SCOPE.md",
        "docs/bigcapital/CONFIGURE_COA_RUNBOOK.md",
    ]:
        pdf.bullet(b)

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(
        0,
        5,
        "This guide explains the economic model Bigcapital uses for Astrans. "
        "It is not a substitute for your chartered accountant on Sri Lanka tax filing.",
    )

    pdf.output(str(OUT))
    return OUT


if __name__ == "__main__":
    path = build()
    print("Wrote", path)
