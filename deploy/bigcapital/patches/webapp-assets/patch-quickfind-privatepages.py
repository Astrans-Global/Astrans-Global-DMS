"""Fix Quick Find blank screen in PrivatePages-H5aUufvf.js.

Stock bug:
1) default resource type uses typo L.CUSTOMR (undefined) instead of L.CUSTOMER
2) _E(data) assumes data.items always exists — after a bad/empty search response
   typing re-renders yE → _E(undefined) → Cannot read properties of undefined (reading 'map')
   and React unmounts #root (blank screen).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "PrivatePages-H5aUufvf.js"
MARKER = "/*astrans-quickfind-1*/"

STOCK = ROOT / NAME
BACKUP = ROOT / f"{NAME}.stock"


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else STOCK
    if not src.is_file():
        raise SystemExit(f"missing {src}")

    text = src.read_text(encoding="utf-8", errors="strict")
    if MARKER in text:
        print("already patched")
        STOCK.write_text(text, encoding="utf-8", newline="\n")
        return

    if "L.CUSTOMR" not in text:
        raise SystemExit("expected L.CUSTOMR typo not found")
    if text.count("L.CUSTOMR") != 1:
        raise SystemExit(f"unexpected L.CUSTOMR count={text.count('L.CUSTOMR')}")

    old_e = (
        "function _E(e){const t=lc(e._type,\"itemSelect\");"
        "return e.items.map(n=>({...t?t(n):{},_type:e._type}))}"
    )
    new_e = (
        f"function _E(e){{{MARKER}"
        "if(!e||!Array.isArray(e.items))return[];"
        "const t=lc(e._type,\"itemSelect\");"
        "return e.items.map(n=>({...t?t(n):{},_type:e._type}))}"
    )
    if old_e not in text:
        raise SystemExit("expected _E one-liner not found")

    out = text.replace("L.CUSTOMR", "L.CUSTOMER", 1).replace(old_e, new_e, 1)
    if MARKER not in out:
        raise SystemExit("marker missing after patch")
    if "L.CUSTOMR" in out:
        raise SystemExit("CUSTOMR still present")

    if not BACKUP.exists():
        shutil.copy2(src, BACKUP)
        print(f"backed up stock -> {BACKUP.name}")

    STOCK.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {STOCK} ({STOCK.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
