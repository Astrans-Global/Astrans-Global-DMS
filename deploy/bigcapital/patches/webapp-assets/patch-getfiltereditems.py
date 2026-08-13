"""Guard Blueprint getFilteredItems when Select/MultiSelect items is undefined.

Customize Report drawers pass customers/items from async context; if that list is
still undefined, QueryList crashes: Cannot read properties of undefined (reading 'filter').
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "index-C4jBpDeP.js"
MARKER = "/*astrans-filteritems-1*/"

OLD = (
    "function getFilteredItems(it,dt){var ft=dt.items,pt=dt.itemPredicate,"
    "mt=dt.itemListPredicate;"
)
NEW = (
    f"function getFilteredItems(it,dt){{{MARKER}"
    "var ft=dt.items||[],pt=dt.itemPredicate,mt=dt.itemListPredicate;"
)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / NAME
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print("already patched")
        return
    if text.count(OLD) != 1:
        raise SystemExit(f"expected one getFilteredItems header, found {text.count(OLD)}")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
    print(f"patched {path}")


if __name__ == "__main__":
    main()
