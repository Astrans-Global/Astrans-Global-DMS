"""Fix aging report dynamicColumns matchers for snake_case API keys.

Stock matchers only look for customerName/vendorName/agingPeriod/current/total.
Live API columns often keep snake_case (customer_name, …), so cond() falls
through and raw columns crash DataTable.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "dynamicColumns-YeaCR-J-.js"
MARKER = "/*astrans-aging-cols-1*/"

# Also add id on name/current builders so react-table is happy even without Qt patch.
OLD_K = (
    "const a=s=>\"cells[\".concat(s,\"].value\"),"
    "k=o((s,e)=>({key:e.key,Header:e.label,accessor:a(e.cellIndex),sticky:\"left\",width:240,textOverview:!0})),"
    "h=o((s,e)=>{const r=a(e.cellIndex);return{key:e.key,Header:e.label,accessor:r,className:e.key,width:n(s,r,{minWidth:120}),align:i.Right,money:!0}}),"
)

NEW_K = (
    f"const a=s=>\"cells[\".concat(s,\"].value\"),{MARKER}"
    "k=o((s,e)=>({id:e.key,key:e.key,Header:e.label,accessor:a(e.cellIndex),sticky:\"left\",width:240,textOverview:!0})),"
    "h=o((s,e)=>{const r=a(e.cellIndex);return{id:e.key,key:e.key,Header:e.label,accessor:r,className:e.key,width:n(s,r,{minWidth:120}),align:i.Right,money:!0}}),"
)

OLD_MATCH = (
    "return y(t(c([\"key\"],\"total\"),r),t(c([\"key\"],\"current\"),d),"
    "t(c([\"key\"],\"customerName\"),l),t(c([\"key\"],\"vendorName\"),l),t(c([\"key\"],\"agingPeriod\"),m))(e)}"
)

NEW_MATCH = (
    "return y("
    "t(c([\"key\"],\"total\"),r),t(c([\"key\"],\"current\"),d),"
    "t(c([\"key\"],\"customerName\"),l),t(c([\"key\"],\"customer_name\"),l),"
    "t(c([\"key\"],\"vendorName\"),l),t(c([\"key\"],\"vendor_name\"),l),"
    "t(c([\"key\"],\"agingPeriod\"),m),t(c([\"key\"],\"aging_period\"),m)"
    ")(e)}"
)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / NAME
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print("already patched")
        return
    if OLD_K not in text:
        raise SystemExit("expected k/h builders not found")
    if OLD_MATCH not in text:
        raise SystemExit("expected cond matchers not found")
    out = text.replace(OLD_K, NEW_K, 1).replace(OLD_MATCH, NEW_MATCH, 1)
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"patched {path} (+{len(out) - len(text)} bytes)")


if __name__ == "__main__":
    main()
