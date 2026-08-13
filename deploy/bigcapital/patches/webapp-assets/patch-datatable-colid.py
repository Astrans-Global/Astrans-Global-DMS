"""Harden react-table column normalizer Qt() in index-C4jBpDeP.js.

Financial report APIs return columns as {key, label, cellIndex}. Some report
mappers only match camelCase keys, so raw columns reach Qt() without id/Header/
accessor and the SPA error-boundary blanks the page.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "index-C4jBpDeP.js"
MARKER = "/*astrans-colid-1*/"

OLD = "function Qt(Nt){var Ft=Nt.id,Gt=Nt.accessor,Yt=Nt.Header;if(typeof Gt==\"string\"){"
NEW = (
    "function Qt(Nt){var Ft=Nt.id,Gt=Nt.accessor,Yt=Nt.Header;"
    f"{MARKER}"
    "if(!Yt&&typeof Nt.label==\"string\"){Yt=Nt.label;Nt.Header=Yt}"
    "if(!Ft&&typeof Nt.key==\"string\")Ft=Nt.key;"
    "if(Gt==null&&Nt.cellIndex!=null)Gt=\"cells[\".concat(Nt.cellIndex,\"].value\");"
    "if(Gt==null&&typeof Nt.key==\"string\")Gt=Nt.key;"
    "if(typeof Gt==\"string\"){"
)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / NAME
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print("already patched")
        return
    if text.count(OLD) != 1:
        raise SystemExit(f"expected exactly one Qt header, found {text.count(OLD)}")
    out = text.replace(OLD, NEW, 1)
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"patched {path} (+{len(out) - len(text)} bytes)")


if __name__ == "__main__":
    main()
