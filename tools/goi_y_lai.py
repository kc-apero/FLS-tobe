# -*- coding: utf-8 -*-
"""GOI Y BU cho cac moi noi MAY da tao TRUOC khi `QĐ-ITL-143` ra doi.

    python tools/goi_y_lai.py            # xem truoc, ⛔ KHONG ghi
    python tools/goi_y_lai.py --ghi      # ghi that

⛔⛔⛔ **Vi sao cong cu nay PHAI co, va toi suyt quen no.**

`chay_nap._goi_y_sau_ghep` chi chay tren `can_chen` — **moi noi sinh ra TRONG
lan nap do**. Nap lai cung nguon thi dong da vao so truoc se bi bo qua vi trung
`content_key` (`itl_id is None`), nen no ⛔ **khong bao gio** di qua duong goi y.

  ⇒ **2.262** moi noi may da tao truoc `18/09` se ⛔ **khong bao gio** duoc goi y,
    va con so `2.219` ma toi hua voi owner se ⛔ khong bao gio xuat hien.

⚠ **Day ⛔ KHONG phai backfill "bia du lieu".** Phep suy la **DUNG mot phep**
  (`may_ghep.suy_hd_cdt1`) dung chung voi duong tay va duong nap; ket qua mang
  `nguon='may_goi_y'` nen no ⛔ **khong** vao `fls_sua_tay` — no van chi la mot
  **loi de nghi**, cho nguoi gat. ⛔ Khac han `0024`, cho ma toi **tu choi**
  backfill: o day ⛔ khong co gi phai **doan**, gia tri nam san trong dong lenh.

⛔ Va no ⛔ KHONG de len o NGUOI da chot — `ghi_goi_y_may` kiem `fls_sua_tay`
  truoc moi o. Do `18/09`: `fls_adjustment` co **0** dong, nen lan chay dau
  ⛔ khong the va ai; phep kiem van o day cho nhung lan sau.
"""
from __future__ import annotations

import argparse
import sys

import psycopg

from fls.db.kho import dsn_that
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that

# ⛔ Doc moi noi CON HIEU LUC (`fls_moi_noi`), ⛔ khong doc `fls_pm_link`: bang
#   goc giu ca nhung moi noi DA BO, va goi y cho mot moi noi da bo la de nghi
#   mot thu nguoi ta vua go ra.
# ⛔⛔ `fls_pm_line` co khoa chinh GHEP DOI `(run_id, pm_line_id)` — noi bang
#   `pm_line_id` DON se phong len dung bang SO ANH PM (do 18/09: 22,0 lan).
#   ⇒ `DISTINCT ON (pm_line_id) ... ORDER BY run_id DESC` lay ban MOI NHAT.
_SQL = """
WITH pml AS (
  SELECT DISTINCT ON (p.pm_line_id) p.pm_line_id, p.hd, p.cdt1
    FROM fls_pm_line p
   WHERE {dk}
   ORDER BY p.pm_line_id, p.run_id DESC
)
SELECT n.itl_id, n.pm_line_id, m.hd, m.cdt1
  FROM fls_moi_noi n
  JOIN pml m USING (pm_line_id)
 ORDER BY n.itl_id, n.pm_line_id
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", action="store_true", help="ghi that")
    a = ap.parse_args(argv)

    pv = chi_nap_that()
    dk, ts = pv.dieu_kien("p.run_id")
    with psycopg.connect(dsn_that(), autocommit=True) as conn:
        rows = conn.execute(_SQL.format(dk=dk), ts).fetchall()
        gom: dict[int, list[dict[str, object]]] = {}
        for itl_id, line, hd, cdt1 in rows:
            gom.setdefault(itl_id, []).append(
                {"pm_line_id": line, "hd": hd, "cdt1": cdt1})

        dem = {"dong": 0, "but_toan": 0, "khong_suy_duoc": 0,
               "nguoi_da_chot": 0, "da_dung_roi": 0}
        for itl_id, lenh in sorted(gom.items()):
            if not a.ghi:
                # ⛔ Xem truoc thi ⛔ KHONG goi ham ghi — no mo giao dich.
                from fls.repo.may_ghep import suy_hd_cdt1
                suy, khong = suy_hd_cdt1(lenh)
                dem["dong"] += 1 if suy else 0
                dem["but_toan"] += len(suy)
                dem["khong_suy_duoc"] += len(khong)
                continue
            ra = ghi_goi_y_may(conn, itl_id=itl_id, lenh=lenh)
            if ra["but_toan"]:
                dem["dong"] += 1
                dem["but_toan"] += len(ra["but_toan"])
            dem["khong_suy_duoc"] += len(ra["khong_suy_duoc"])
            dem["nguoi_da_chot"] += len(ra["nguoi_da_chot"])

        print(f"moi noi con hieu luc : {len(rows)}")
        print(f"dong so cham toi     : {len(gom)}")
        print(f"dong duoc goi y      : {dem['dong']}")
        print(f"but toan goi y       : {dem['but_toan']}")
        print(f"⚠ truong KHONG suy duoc: {dem['khong_suy_duoc']}  "
              f"(N dong lenh noi N thu — `INV-I16`)")
        if a.ghi:
            print(f"o NGUOI da chot (bo qua): {dem['nguoi_da_chot']}")
            print("✅ da ghi")
        else:
            print("⛔ CHUA GHI — them `--ghi` de ghi that")
    return 0


if __name__ == "__main__":
    sys.exit(main())
