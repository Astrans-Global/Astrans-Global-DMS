#!/usr/bin/env python3
"""Patch transformToForm in index-C4jBpDeP.js so Preferences (and similar forms)
can hydrate from camelCase API metadata into snake_case form defaults.

useCurrentOrganization() camelCases responses; stock Preferences General still
uses snake_case field names. Without this bridge, fiscal_year/date_format/etc
stay empty and look like they never saved.

SAFE RULES:
- Do NOT change index.html / do NOT add ?v= to the Vite entry script.
- Mount only this index file (+ nginx). Never rename PrivatePages imports.
"""
from __future__ import annotations

import argparse
from pathlib import Path

OLD = (
    "transformToForm=(it,dt)=>_$5.pickBy(it,(ft,pt)=>"
    "ft!==null&&Object.keys(dt).includes(pt));"
)

NEW = (
    "transformToForm=(it,dt)=>{"
    "if(!it||!dt)return{};"
    "const keys=Object.keys(dt);"
    "const src={...it};"
    "const pairs=["
    '["baseCurrency","base_currency"],'
    '["fiscalYear","fiscal_year"],'
    '["dateFormat","date_format"],'
    '["taxNumber","tax_number"],'
    '["primaryColor","primary_color"],'
    '["logoKey","logo_key"],'
    '["logoUri","logo_uri"],'
    '["tenantId","tenant_id"]'
    "];"
    "for(const[camel,snake]of pairs){"
    "if(keys.includes(snake)&&(src[snake]===undefined||src[snake]===null)&&src[camel]!=null)src[snake]=src[camel];"
    "if(keys.includes(camel)&&(src[camel]===undefined||src[camel]===null)&&src[snake]!=null)src[camel]=src[snake];"
    "}"
    'if(src.address&&typeof src.address==="object"&&!Array.isArray(src.address)){'
    "const a={...src.address};"
    "if((a.postal_code===undefined||a.postal_code===null)&&a.postalCode!=null)a.postal_code=a.postalCode;"
    "if((a.postalCode===undefined||a.postalCode===null)&&a.postal_code!=null)a.postalCode=a.postal_code;"
    "if((a.state_province===undefined||a.state_province===null)&&a.stateProvince!=null)a.state_province=a.stateProvince;"
    "if((a.stateProvince===undefined||a.stateProvince===null)&&a.state_province!=null)a.stateProvince=a.state_province;"
    "src.address=a;"
    "}"
    "return _$5.pickBy(src,(ft,pt)=>ft!==null&&keys.includes(pt));"
    "};"
    "/*astrans-ttf-1*/"
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    args = ap.parse_args()
    text = args.src.read_text(encoding="utf-8", errors="surrogateescape")
    if OLD not in text:
        raise SystemExit("expected transformToForm one-liner not found")
    if text.count(OLD) != 1:
        raise SystemExit(f"expected exactly 1 occurrence, found {text.count(OLD)}")
    out = text.replace(OLD, NEW)
    if "/*astrans-ttf-1*/" not in out:
        raise SystemExit("patch marker missing")
    if OLD in out:
        raise SystemExit("old one-liner still present")
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    args.dst.write_text(out, encoding="utf-8", errors="surrogateescape")
    print(f"OK wrote {args.dst} ({len(out)} bytes, delta {len(out)-len(text)})")


if __name__ == "__main__":
    main()
