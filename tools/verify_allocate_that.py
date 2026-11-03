"""Cong SONG cho vung ALLOCATE: phep suy co that su tra loi tren KHO THAT khong.

  python tools/verify_allocate_that.py

⛔ Chi DOC kho. ⛔ Khong ghi mot dong nao.

★★ **Vi sao script nay ton tai.** `QĐ-ITL-65` bo nam cot vung ALLOCATE khoi kho
voi mot loi hua: *"vung phan bo se hien lai nhu mot PHEP TINH"*. Mot loi hua
⛔ khong phai mot phep do. Script nay do:

  ⓐ bao nhieu dong so tra duoc `hd` trong `fls_mapping_master`, va bao nhieu
    ⛔ khong (⇒ sheet se hien `#N/A` o CA HAI o)
  ⓑ bao nhieu dong ra co `Need to Allocate to CFA2`
  ⓒ bao nhieu dong ra o `Method` la **`0`** — con so cua **bay `VLOOKUP`**, thu
    ma hom qua con la *"mot phep do chua chay"* (`GAP-ALLOC-01`)

⚠ Va no ⛔ KHONG bao "dat/khong dat" cho ⓐ: mot ty le tra duoc thap co the la
  **trang thai dung** *(nhieu dong so con `hd` UNMAPPED — dung viec cua hang
  cho)*. Dat nguong o day la bia ra mot cai cong khong ai chot.
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg                                                    # noqa: E402

from fls.db.kho import dsn_that                                   # noqa: E402
from fls.ledger.allocate import (CO_CAN_PHAN_BO, KHONG_TRA_DUOC,  # noqa: E402
                                 suy_allocate)
from fls.repo.nap_mapping import TRUONG                           # noqa: E402


def main() -> int:
    with psycopg.connect(dsn_that(), autocommit=True) as c:
        mm = {
            str(r[0]).strip().lower(): dict(zip(TRUONG, r))
            for r in c.execute(
                f"SELECT {', '.join(TRUONG)} FROM fls_mapping_master").fetchall()
        }
        print(f"danh muc: {len(mm)} ma `hd`")
        if not mm:
            print("⛔ bang `fls_mapping_master` RONG — chay "
                  "`tools/nap_mapping_master.py --ghi` truoc")
            return 1

        # `hd` hieu luc = nguoi go (`fls_sua_tay`) neu co, khong thi cot nguon.
        dong = c.execute(
            "SELECT i.itl_id, COALESCE(s.value_after, i.hd) AS hd, i.cdt1"
            "  FROM fls_itl i"
            "  LEFT JOIN fls_sua_tay s ON s.itl_id = i.itl_id AND s.field='hd'"
        ).fetchall()

    dem = collections.Counter()
    method = collections.Counter()
    thieu = collections.Counter()
    for _i, hd, cdt1 in dong:
        k = (str(hd).strip().lower() if hd is not None else "")
        d = mm.get(k)
        v = suy_allocate(cdt1, hd, d)
        if v.khong_tra_duoc:
            dem["khong_tra_duoc"] += 1
            thieu[(str(hd).strip() if hd else "(rong)")] += 1
        else:
            dem["tra_duoc"] += 1
            dem["can_phan_bo"] += int(v.can_phan_bo)
            method[v.method] += 1

    n = len(dong)
    print(f"\ndong so: {n}")
    print(f"  tra duoc `hd` trong danh muc : {dem['tra_duoc']:>6} "
          f"({100 * dem['tra_duoc'] / n:.1f}%)")
    print(f"  ⛔ khong tra duoc ({KHONG_TRA_DUOC:<5})      : "
          f"{dem['khong_tra_duoc']:>6} "
          f"({100 * dem['khong_tra_duoc'] / n:.1f}%)")
    print(f"  co {CO_CAN_PHAN_BO!r:<28}: {dem['can_phan_bo']:>6}")

    print("\no `Method` ra gi (chi tren dong tra duoc):")
    for v, c2 in method.most_common(10):
        ghi = ("  ⇐ BAY `VLOOKUP`: o `L` RONG nen Sheets cho `0`, "
               "⛔ khong 'No need'") if v == "0" else ""
        print(f"  {v!r:20} {c2:>6}{ghi}")

    print("\n5 gia tri `hd` ⛔ khong tra duoc, theo so dong:")
    for v, c2 in thieu.most_common(5):
        print(f"  {v!r:44} {c2:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
