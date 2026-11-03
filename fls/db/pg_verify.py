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


# ⭐ Them 27/08: truoc day `pg_verify` ⛔ KHONG so khoa chinh / UNIQUE, nen mot
# khoa KHAI ma khong AP se di qua im lang. Cung ho voi lo da sinh ra cong nay
# (`CREATE TABLE IF NOT EXISTS` bo qua trong im lang), chi khac truc.
_Q_KHOA = """
SELECT tc.constraint_type, kcu.column_name, kcu.ordinal_position, tc.constraint_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON kcu.constraint_name = tc.constraint_name
 AND kcu.table_schema = tc.table_schema
WHERE tc.constraint_type IN ('PRIMARY KEY', 'UNIQUE')
  AND tc.table_schema = %s AND tc.table_name = %s
ORDER BY tc.constraint_name, kcu.ordinal_position
"""


def _khoa_trong_db(cur, ten_bang: str, schema: str
                   ) -> tuple[tuple[str, ...], set[tuple[str, ...]]]:
    """Tra (cac cot khoa chinh, tap cac khoa UNIQUE) — theo DUNG THU TU cot.

    Thu tu quan trong: `PRIMARY KEY (a, b)` va `(b, a)` cho ra chi muc khac
    nhau, nen coi chung bang nhau la bo qua mot cho lech that.
    """
    cur.execute(_Q_KHOA, (schema, ten_bang))
    theo_rb: dict[str, tuple[str, list[str]]] = {}
    for loai, cot, _, ten_rb in cur.fetchall():
        theo_rb.setdefault(ten_rb, (loai, []))[1].append(cot)
    pk: tuple[str, ...] = ()
    uq: set[tuple[str, ...]] = set()
    for loai, cot in theo_rb.values():
        if loai == "PRIMARY KEY":
            pk = tuple(cot)
        else:
            uq.add(tuple(cot))
    return pk, uq


def _lech_khoa(cur, t: Table, schema: str) -> list[str]:
    pk_db, uq_db = _khoa_trong_db(cur, t.name, schema)

    pk_khai = t.pk_cols or tuple(c.name for c in t.columns if c.pk)
    uq_khai = {tuple(k) for k in t.unique_keys}
    uq_khai |= {(c.name,) for c in t.columns if c.unique}

    ra: list[str] = []
    if tuple(pk_khai) != pk_db:
        ra.append(f"{t.name}: khoa chinh khai {list(pk_khai)}, DB {list(pk_db)}")
    for k in sorted(uq_khai - uq_db):
        ra.append(f"{t.name}: UNIQUE khai bao co, DB THIEU  ({list(k)})")
    for k in sorted(uq_db - uq_khai):
        # Khoa chinh cung sinh mot chi muc unique — ⛔ khong tinh la la
        if k != pk_db:
            ra.append(f"{t.name}: UNIQUE trong DB, khai bao KHONG co  ({list(k)})")
    return ra


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
        ra += _lech_khoa(cur, t, schema)
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
