"""Cong kho THAT: chi duoc chua dong cua lan nap THAT.

    python tools/kiem_kho.py            # soi kho THAT
    python tools/kiem_kho.py --test     # soi kho TEST (de doi chieu)

Tra 1 neu khong dat. Xem `fls/repo/kho_sach.py` de biet vi sao cong nay co.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import psycopg                                                    # noqa: E402

from fls.db.kho import dsn_test, dsn_that, ten_kho                 # noqa: E402
from fls.repo.kho_sach import kiem                                 # noqa: E402


def main() -> int:
    la_test = "--test" in sys.argv
    dsn = dsn_test() if la_test else dsn_that()
    print(f"kho: {ten_kho(dsn)!r}  ({'TEST' if la_test else 'THAT'})")

    if la_test:
        # ⛔ Kho TEST DAY dau test la dung — cong nay ⛔ khong phan xu o day.
        # Mot cong bao "do" cho trang thai MONG DOI la cong keu oan, va cong
        # keu oan thi lan sau khong ai doc no nua.
        from fls.repo.kho_sach import do as dem_run
        with psycopg.connect(dsn, autocommit=True) as c:
            for d in dem_run(c):
                print(f"  {d.bang:12s} {d.tong:6d} dong · {len(d.theo_run)} run")
        print("  (chi bao cao — kho TEST co dau test la DUNG)")
        return 0

    with psycopg.connect(dsn, autocommit=True) as c:
        px = kiem(c)
    print(px.bao())

    if not px.dat:
        print("\n⛔ Don dep ⛔ KHONG bang `DELETE` len `fls_itl` (INV-I08 "
              "append-only).\n   Duong dung: **dung lai kho** — "
              "`python tools/dung_lai_kho.py --that` (DDL drop/create) roi nap lai.")
    return 0 if px.dat else 1


if __name__ == "__main__":
    sys.exit(main())
