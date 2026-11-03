"""Do HINH DANG THAT cua luoi `F02` — buoc dau cua mui thu `GAP-SCR-03`.

    python tools/do_luoi_f02.py            # kho THAT
    python tools/do_luoi_f02.py --test     # kho test

⛔⛔ **Vi sao phai do TRUOC khi thu thu vien.** `BA-06` §6b viet bai toan la
*"luoi ~64 cot x vai nghin dong, chi 5 cot sua duoc"*. Ba con so do la **uoc
luong tu tai lieu AS-IS**, ⛔ khong phai do tu kho. Va mot mui thu chay tren so
uoc luong thi ket luan cua no cung la uoc luong: neu so dong that gap ba lan uoc
luong thi thu vien "dat" o mui thu se **truot o that**, con neu it hon nhieu thi
ta vua loai mot ung vien vi mot bai toan khong ton tai.

★ Cong nay ⛔ khong ket luan thu vien nao thang. No tra ve **bon con so** ma mui
thu can, va no do tren KHO THAT:

    ⓐ so COT luoi phai cho, va bao nhieu trong so do SUA DUOC
    ⓑ so DONG cua mot lat thuc te (theo ky · theo trang)
    ⓒ **so BYTE** cua goi JSON cho mot trang — day la con so quyet dinh
      *"trang dau tien mat bao lau moi hien"*, va no ⛔ khong suy duoc tu so dong
    ⓓ o RONG chiem bao nhieu — luoi ma 70% o rong thi cam giac dung khac han

⛔ Cong nay ⛔ KHONG do duoc hai thu, va khai ra chu khong de nguoi doc tu suy:
  · **cam giac** (*"co thua Sheets o dau"*) — can LAN/THUONG ngoi go that
  · **thoi gian ve** cua trinh duyet — can mot trinh duyet that
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.canon.spec import CANON_COLS  # noqa: E402
from fls.db.kho import dsn_test, dsn_that  # noqa: E402
from fls.repo.ghi_tay import TRUONG_GHI  # noqa: E402

# 14 truong hop dong + cac cot F02 hien ngoai `canon`.
COT_HOP_DONG = ("itl_id", "doc_date", "doc_no", "curr", "ps_no", "ps_co",
                "le", "acct", "memo", "hd", "pay_type", "cdt1", "svc_start",
                "svc_end")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--trang", type=int, default=200,
                    help="so dong mot trang (mac dinh 200)")
    a = ap.parse_args()
    dsn = dsn_test() if a.test else dsn_that()

    import psycopg

    ra: dict[str, object] = {}
    with psycopg.connect(dsn, autocommit=True) as c:
        # ⓐ so cot
        cot_db = [r[0] for r in c.execute(
            "SELECT column_name FROM information_schema.columns"
            " WHERE table_name = 'fls_itl' ORDER BY ordinal_position").fetchall()]
        so_canon = len(CANON_COLS)
        ra["cot"] = {
            "cot_bang_fls_itl": len(cot_db),
            "cot_canon_trong_jsonb": so_canon,
            # ⛔⛔ Con so nay da doi HAI lan trong mot ngay, va ca hai lan
            # deu co ly do do duoc — chep lai de dung ai tuong la dao qua dao lai:
            #   · **52** (27/08) = 38 canon + 14 hop dong
            #   · **55** (28/08 sang) = +3, vi owner bao luoi thieu `Ma doi tac`
            #     va `Hoa don`; do ky thi ra NAM truong ghi ngoai 14 cot, hai
            #     trong so co ban tho o canon (`Y`,`AD`), con BA thi khong co o
            #     dau ⇒ phai them 3 cot that
            #   · **52** (28/08 chieu) = -3, vi owner dua NGUYEN VAN 3 cong thuc
            #     ⇒ ca ba SUY LAI DUOC va ke toan ⛔ khong sua (`QĐ-ITL-64`) ⇒
            #     bo khoi khuon kho (`QĐ-ITL-65`, migration `0012`).
            # ⇒ Vung phan bo se hien lai nhu mot **phep tinh**, ⛔ khong phai
            #   mot cot cua so.
            "cot_luoi_F02_phai_cho": so_canon + len(COT_HOP_DONG),
            "cot_ghi_khong_co_nha": 0,
            "cot_SUA_DUOC": len(TRUONG_GHI),
        }

        # ⓑ so dong
        tong = c.execute("SELECT count(*) FROM fls_itl").fetchone()[0]
        theo_ky = c.execute(
            "SELECT to_char(doc_date,'YYYY-MM') AS ky, count(*) FROM fls_itl"
            " WHERE doc_date IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 5"
        ).fetchall()
        hang_cho = c.execute(
            "SELECT count(*) FROM fls_itl WHERE work_status='UNMAPPED'"
        ).fetchone()[0]
        ra["dong"] = {
            "ca_so": tong,
            "hang_cho_UNMAPPED": hang_cho,
            "ky_DAY_NHAT": [{"ky": k, "dong": n} for k, n in theo_ky],
            "trang_do": a.trang,
        }

        # ⓒ so BYTE cua mot trang — cot `canon` la jsonb nen no la phan nang nhat
        cot = ", ".join(COT_HOP_DONG) + ", canon"
        hang = c.execute(
            f"SELECT {cot} FROM fls_itl ORDER BY itl_id LIMIT %s", (a.trang,)
        ).fetchall()
        ten = COT_HOP_DONG + ("canon",)
        goi = [dict(zip(ten, r)) for r in hang]
        js = json.dumps(goi, default=str, ensure_ascii=False)
        # va ban CHI 14 cot hop dong (khong mang `canon`) de so
        js_gon = json.dumps(
            [{k: v for k, v in d.items() if k != "canon"} for d in goi],
            default=str, ensure_ascii=False)
        ra["byte"] = {
            "mot_trang_DU_canon": len(js.encode()),
            "mot_trang_KHONG_canon": len(js_gon.encode()),
            "byte_moi_dong_DU": round(len(js.encode()) / max(len(goi), 1)),
            "ca_so_neu_lat_het_DU": round(
                len(js.encode()) / max(len(goi), 1) * tong),
        }

        # ⓓ o RONG
        dem_rong = 0
        dem_o = 0
        for d in goi:
            for k in COT_HOP_DONG:
                dem_o += 1
                if d[k] in (None, ""):
                    dem_rong += 1
            cn = d.get("canon") or {}
            if isinstance(cn, dict):
                for v in cn.values():
                    dem_o += 1
                    if v in (None, ""):
                        dem_rong += 1
        ra["o_rong"] = {
            "o_da_dem": dem_o,
            "o_RONG": dem_rong,
            "pct_RONG": round(100 * dem_rong / max(dem_o, 1), 1),
        }

    # ── in ra cho nguoi doc, ⛔ khong chi tra JSON
    c1 = ra["cot"]
    d1 = ra["dong"]
    b1 = ra["byte"]
    o1 = ra["o_rong"]
    print(f"kho: {dsn.rsplit('/', 1)[-1]}\n")
    print("ⓐ COT")
    print(f"   luoi F02 phai cho : {c1['cot_luoi_F02_phai_cho']} cot"
          f"  ({c1['cot_canon_trong_jsonb']} canon + {len(COT_HOP_DONG)} hop dong"
          f" + {c1['cot_ghi_khong_co_nha']} truong ghi khong co nha)")
    print(f"   SUA DUOC          : {c1['cot_SUA_DUOC']} cot"
          f"  ⇒ {round(100 * c1['cot_SUA_DUOC'] / c1['cot_luoi_F02_phai_cho'])}%")
    print(f"   bang `fls_itl`    : {c1['cot_bang_fls_itl']} cot vat ly\n")
    print("ⓑ DONG")
    print(f"   ca so             : {d1['ca_so']:,}")
    print(f"   hang cho UNMAPPED : {d1['hang_cho_UNMAPPED']:,}")
    for x in d1["ky_DAY_NHAT"]:
        print(f"   ky {x['ky']}        : {x['dong']:,} dong")
    print()
    print(f"ⓒ BYTE (trang {d1['trang_do']} dong)")
    print(f"   du `canon`        : {b1['mot_trang_DU_canon']:,} byte"
          f"  ({b1['byte_moi_dong_DU']:,} byte/dong)")
    print(f"   ⛔ khong `canon`   : {b1['mot_trang_KHONG_canon']:,} byte"
          f"  ({round(100 * b1['mot_trang_KHONG_canon'] / max(b1['mot_trang_DU_canon'], 1))}% cua ban du)")
    print(f"   ca so neu lat het : {b1['ca_so_neu_lat_het_DU']:,} byte"
          f"  ({b1['ca_so_neu_lat_het_DU'] / 1e6:.1f} MB)\n")
    print("ⓓ O RONG")
    print(f"   {o1['o_RONG']:,} / {o1['o_da_dem']:,} o = {o1['pct_RONG']}% RONG\n")

    print("⛔ HAI THU CONG NAY KHONG DO DUOC (khai ra, ⛔ khong de tu suy):")
    print("   · cam giac 'co thua Sheets o dau' — can LAN/THUONG ngoi go that")
    print("   · thoi gian ve cua trinh duyet    — can mot trinh duyet that")
    print()
    print(json.dumps(ra, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
