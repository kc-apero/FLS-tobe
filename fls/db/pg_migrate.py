"""Ap di tru Postgres. Forward-only, co so thu tu, co so ghi.

  export PG_DSN='postgresql://fls:fls@localhost:5433/fls'
  python -m fls.db.pg_migrate --status     # da ap gi, con thieu gi
  python -m fls.db.pg_migrate --dry-run    # in cau lenh con thieu, khong can DB
  python -m fls.db.pg_migrate              # ap that, xong tu chay pg_verify
  python -m fls.db.pg_migrate --adopt-baseline   # DB da co san schema dung: chi ghi so

⭐ Sau khi ap, runner TU CHAY pg_verify. Lech la NO. Day la cho noi hai nguon
su that: schema.py (trang thai mong doi) va migrations/ (duong di toi do).
"""

from __future__ import annotations

import argparse
import os
import sys

from fls.db.migration_runner import (
    LEDGER,
    LEDGER_DDL,
    MIGRATIONS,
    cau_lenh,
    checksum_of,
    con_thieu,
    da_ap,
    kiem_lich_su,
)


def ap(conn) -> list[int]:
    """Ap moi migration con thieu, tung cai mot giao dich. Tra danh sach da ap."""
    with conn.cursor() as cur:
        cur.execute(LEDGER_DDL)
        cu = da_ap(cur)
    sai = kiem_lich_su(cu, MIGRATIONS)
    if sai:
        raise RuntimeError("so ghi di tru khong khop code:\n  " + "\n  ".join(sai))

    xong: list[int] = []
    for m in con_thieu(cu):
        with conn.cursor() as cur:
            for c in cau_lenh(m.sql):
                cur.execute(c)
            cur.execute(
                f"INSERT INTO {LEDGER} (version, name, checksum) VALUES (%s,%s,%s)",
                (m.version, m.name, checksum_of(m.sql)))
        xong.append(m.version)
    return xong


def _in_trang_thai(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(LEDGER_DDL)
        cu = da_ap(cur)
    for m in MIGRATIONS:
        dau = "da ap  " if m.version in cu else "THIEU  "
        print(f"  {dau} {m.version:04d}_{m.name}")
    sai = kiem_lich_su(cu, MIGRATIONS)
    for s in sai:
        print(f"  ⛔ {s}", file=sys.stderr)
    return 1 if sai else 0


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--status", action="store_true")
    a.add_argument("--adopt-baseline", action="store_true",
                   help="DB da co san schema dung: chi ghi vao so, khong chay lai DDL")
    args = a.parse_args()

    if args.dry_run:
        for m in MIGRATIONS:
            print(f"-- {m.version:04d}_{m.name}\n{m.sql}")
        return 0

    dsn = os.environ.get("PG_DSN")
    if not dsn:
        print("thieu PG_DSN", file=sys.stderr)
        return 2
    import psycopg
    from fls.db.pg_verify import so_sanh_voi_db

    with psycopg.connect(dsn, autocommit=True) as conn:
        if args.status:
            return _in_trang_thai(conn)

        if args.adopt_baseline:
            lech = so_sanh_voi_db(conn)
            if lech:
                print("⛔ khong nhan baseline: DB dang LECH schema khai bao:",
                      file=sys.stderr)
                for m in lech:
                    print(f"  - {m}", file=sys.stderr)
                return 1
            with conn.cursor() as cur:
                cur.execute(LEDGER_DDL)
                for m in MIGRATIONS:
                    cur.execute(
                        f"INSERT INTO {LEDGER} (version, name, checksum) "
                        "VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                        (m.version, m.name, checksum_of(m.sql)))
            print(f"da ghi {len(MIGRATIONS)} migration vao so (khong chay lai DDL)")
            return 0

        xong = ap(conn)
        print(f"da ap {len(xong)} migration: {xong}" if xong else "khong co gi de ap")
        lech = so_sanh_voi_db(conn)

    if lech:
        print(f"⛔ ap xong nhung DB VAN LECH schema khai bao ({len(lech)} cho) — "
              "thieu migration?", file=sys.stderr)
        for m in lech:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print("pg_verify: khop")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
