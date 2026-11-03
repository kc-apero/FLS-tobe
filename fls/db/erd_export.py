"""Sinh hien vat ERD tu schema. Offline, khong cham DB.

  python -m fls.db.erd_export            # in ra man hinh
  python -m fls.db.erd_export --write    # ghi ERD-CONTRACT.json + .mmd
"""

from __future__ import annotations

import argparse
import json
import pathlib

from fls.db.render import render_erd_json, render_erd_mermaid
from fls.db.schema import TABLES

_ROOT = pathlib.Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    js = json.dumps(render_erd_json(TABLES), indent=2, ensure_ascii=False) + "\n"
    mmd = render_erd_mermaid(TABLES)
    if args.write:
        (_ROOT / "ERD-CONTRACT.json").write_text(js, encoding="utf-8", newline="\n")
        (_ROOT / "ERD-CONTRACT.mmd").write_text(mmd, encoding="utf-8", newline="\n")
        print("da ghi ERD-CONTRACT.json + ERD-CONTRACT.mmd")
    else:
        print(js)
        print(mmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
