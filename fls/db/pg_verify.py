"""So sanh DB THAT voi schema khai bao. Lech thi bao to, khong im lang.

Vi sao can: pg_migrate dung CREATE TABLE IF NOT EXISTS + CREATE OR REPLACE VIEW.
Bang da ton tai thi lenh BO QUA — van in "da ap N cau DDL" nhu the thanh cong,
trong khi cot/FK moi KHONG he duoc them. Gap that 2026-08-26 khi them FK run_id.

  python -m fls.db.pg_verify     # 0 = khop, 1 = lech (in tung dong lech)
"""

from __future__ import annotations

import os
import sys

from fls.db.model import Table
from fls.db.schema import TABLES

_Q_COT = """
SELECT column_name, is_nullable
FROM information_schema.columns
WHERE table_schema = %s AND table_name = %s
"""

_Q_FK = """
SELECT kcu.column_name, ccu.table_name, ccu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON kcu.constraint_name = tc.constraint_name
JOIN information_schema.constraint_column_usage ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = %s AND tc.table_name = %s
"""


def _lech_mot_bang(cur, t: Table, schema: str) -> list[str]:
    cur.execute(_Q_COT, (schema, t.name))
    that = {r[0]: (r[1] == "YES") for r in cur.fetchall()}
    if not that:
        return [f"{t.name}: KHONG TON TAI trong DB"]

    ra: list[str] = []
    for c in t.columns:
        if c.name not in that:
            ra.append(f"{t.name}.{c.name}: khai bao co, DB THIEU")
        elif t.kind == "table" and that[c.name] != c.null:
            ra.append(f"{t.name}.{c.name}: null khai bao={c.null}, DB={that[c.name]}")
    for ten in set(that) - {c.name for c in t.columns}:
        ra.append(f"{t.name}.{ten}: DB co, khai bao KHONG co")

    if t.kind == "table":
        cur.execute(_Q_FK, (schema, t.name))
        fk_that = {f"{a}->{b}.{c}" for a, b, c in cur.fetchall()}
        fk_khai = {f"{c.name}->{c.fk}" for c in t.columns if c.fk}
        for f in fk_khai - fk_that:
            ra.append(f"{t.name}: FK khai bao co, DB THIEU  ({f})")
        for f in fk_that - fk_khai:
            ra.append(f"{t.name}: FK trong DB, khai bao KHONG co  ({f})")
    return ra


def so_sanh_voi_db(conn, tables: dict[str, Table] | None = None,
                   schema: str = "public") -> list[str]:
    """Tra ve danh sach cho lech. Rong = khop."""
    ra: list[str] = []
    with conn.cursor() as cur:
        for name in sorted(tables if tables is not None else TABLES):
            ra += _lech_mot_bang(cur, (tables or TABLES)[name], schema)
    return ra


def main() -> int:
    dsn = os.environ.get("PG_DSN")
    if not dsn:
        print("thieu PG_DSN", file=sys.stderr)
        return 2
    import psycopg
    with psycopg.connect(dsn) as conn:
        lech = so_sanh_voi_db(conn)
    if not lech:
        print(f"khop: {len(TABLES)} bang/view dung nhu khai bao")
        return 0
    print(f"LECH {len(lech)} cho giua DB that va schema khai bao:", file=sys.stderr)
    for m in lech:
        print(f"  - {m}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
