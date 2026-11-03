"""Bom khoi erDiagram SINH RA vao tai lieu BA. Khong sua ERD bang tay.

  python tools/sync_erd_doc.py docs/05_DATA_DICTIONARY_ERD.md [duong/dan/khac.md ...]

Tim khoi ```mermaid ... erDiagram ... ``` dau tien roi THAY nguyen khoi.
Khong tim thay => bao loi to, khong tu them am tham (INV-I16 tinh than).
"""

from __future__ import annotations

import pathlib
import re
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_MMD = _ROOT / "ERD-CONTRACT.mmd"
_KHOI = re.compile(r"```mermaid\s*\nerDiagram\n.*?```", re.S)


def sync(doc: pathlib.Path, mmd: str) -> bool:
    txt = doc.read_text(encoding="utf-8")
    moi = "```mermaid\n" + mmd.rstrip("\n") + "\n```"
    if not _KHOI.search(txt):
        raise SystemExit(f"KHONG tim thay khoi 'mermaid + erDiagram' trong {doc}")
    ra = _KHOI.sub(lambda _: moi, txt, count=1)
    if ra == txt:
        return False
    doc.write_text(ra, encoding="utf-8", newline="\n")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        raise SystemExit("thieu duong dan tai lieu")
    mmd = _MMD.read_text(encoding="utf-8")
    for p in argv:
        doc = pathlib.Path(p)
        if not doc.is_absolute():
            doc = _ROOT / doc
        print(f"{'da cap nhat' if sync(doc, mmd) else 'khong doi   '} {doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
