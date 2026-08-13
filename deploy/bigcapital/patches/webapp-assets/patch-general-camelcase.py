#!/usr/bin/env python3
"""Patch Preferences General form: snake_case field names -> camelCase.

Why: useCurrentOrganization() enables client camelCase transform, so metadata
is baseCurrency/fiscalYear/dateFormat/taxNumber. Stock General still bound
snake_case, so those fields stayed empty and looked unsaved.

Safe deploy rules:
- Mount ONLY this hashed file (General-CydUBvrk.js).
- Never put ?v= on /assets/index-*.js (breaks Vite module graph / login).
- Never remount index-*.js or PrivatePages-*.js.
"""
from __future__ import annotations

import argparse
from pathlib import Path

REPLACEMENTS = [
    ('name:"base_currency"', 'name:"baseCurrency"'),
    ('name:"fiscal_year"', 'name:"fiscalYear"'),
    ('name:"date_format"', 'name:"dateFormat"'),
    ('name:"tax_number"', 'name:"taxNumber"'),
    ('name:"address.postal_code"', 'name:"address.postalCode"'),
    ('name:"address.state_province"', 'name:"address.stateProvince"'),
    ("base_currency:E()", "baseCurrency:E()"),
    ("fiscal_year:E()", "fiscalYear:E()"),
    ("date_format:E()", "dateFormat:E()"),
    ("tax_number:E()", "taxNumber:E()"),
    (
        'base_currency:"",language:"",fiscal_year:"",date_format:"",timezone:"",tax_number:""',
        'baseCurrency:"",language:"",fiscalYear:"",dateFormat:"",timezone:"",taxNumber:""',
    ),
]

MUST_KEEP = [
    'X.get("base_currency")',
    'X.get("fiscal_year")',
    'X.get("date_format")',
    'id:"select_base_currency"',
    'id:"select_fiscal_year"',
    'id:"select_date_format"',
]

MUST_GONE = [
    'name:"base_currency"',
    'name:"fiscal_year"',
    'name:"date_format"',
    'name:"tax_number"',
    'name:"address.postal_code"',
    'name:"address.state_province"',
]


def patch(text: str) -> str:
    for old, new in REPLACEMENTS:
        if old not in text:
            raise SystemExit(f"missing expected pattern: {old!r}")
        text = text.replace(old, new)
    for bad in MUST_GONE:
        if bad in text:
            raise SystemExit(f"still present after patch: {bad!r}")
    for keep in MUST_KEEP:
        if keep not in text:
            raise SystemExit(f"i18n key accidentally removed: {keep!r}")
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    args = ap.parse_args()
    src = args.src.read_text(encoding="utf-8", errors="surrogateescape")
    out = patch(src)
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    args.dst.write_text(out, encoding="utf-8", errors="surrogateescape")
    print(f"OK wrote {args.dst} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
