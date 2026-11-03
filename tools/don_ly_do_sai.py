# -*- coding: utf-8 -*-
"""DON cac su kien `reason` do MAY dan NHAM — hau qua cua `GAP-NAP-01`.

    python tools/don_ly_do_sai.py                          # DO, ⛔ khong xoa
    FLS_CHO_GHI_THAT=1 python tools/don_ly_do_sai.py --duyet   # ⛔ XOA THAT

⛔⛔⛔ **Vi sao co mot cong cu rieng thay vi mot cau `DELETE`.**

Mot cau `DELETE FROM fls_queue_event WHERE evt_type='reason'` go trong ba giay
**⛔ khong the noi duoc no dang xoa cai DUNG hay cai SAI**. Va o day cau tra
loi ⛔ khong hien nhien: `fls_queue_event` la bang **VET** — no la cho duy nhat
tra loi cau *"vi sao dong nay nam trong hang cho"*. Xoa nham no la xoa **ly do
lam viec cua ke toan**, ⛔ khong phai xoa rac.

⇒ Tep nay **chung minh** truoc khi xoa, va **NO** neu chung minh ⛔ khong dung.

★ **Loi goc (`GAP-NAP-01`, do 11/09):** `nap_lo` lay **phan quyet CA LO** cua
  bo soat *(`S2 · S3 · S4 · S7`…)* roi dong no len **MOI dong** cua lo — thay
  vi map tung `dong_xau` ve dung `source_row` cua no. Da vá o
  `fls/repo/nap_lo.py::_ly_do_tung_dong`; **108.128 su kien cu** thi van nam.

★ **BA phep chung minh, va ca ba deu la phep DO, ⛔ khong phai suy luan:**

  ⓐ ⭐ **Chu ky cau truc.** Mot ly do THEO DONG ⛔ khong the dan trung **100%**
    so dong. Neu `count(distinct itl_id)` = `count(fls_itl)` thi do dung la
    dau van tay cua mot phan quyet CA LO. Do 11/09: **8.387 / 8.387**.
  ⓑ ⭐⭐ **`S3` tu bac bo chinh no.** `S3` noi *"dong nay ⛔ khong co TIEN"* —
    ma mot dong ⛔ khong co tien thi **⛔ khong bao gio vao duoc `fls_itl`**.
    Do: **77.744/77.744** dong mang nhan `S3` **CO tien**. Sai 100%, va no
    ⛔ khong the sai it hon: nhan nay tu mau thuan.
  ⓒ **`S2` gan nhu vay.** `S2` noi *"co tien ma thieu MA"*; **79.017/79.041**
    dong mang nhan ay **CO ma** *(99,97%)*.

⛔⛔ **Cai tep nay TU CHOI lam:** no ⛔ **khong** xoa neu ⓐ **khong** dung. Vi
   luc ay mot phan su kien co the la ly do THAT *(do ban vá sinh ra, hay do
   NGUOI go vao)*, va no ⛔ **khong** the phan biet duoc tung cai. Chan tay o
   `actor` cung vi le do: tep nay **chi** dung duoc dau cac su kien do MAY
   dan, ⛔ khong bao gio cham cai nguoi viet.

⚠ **Sau khi xoa, so su kien dung la `0` — va do la con so DUNG.** Ban vá
   `_ly_do_tung_dong` **⛔ khong ghi su kien nao** cho dong ⛔ khong luat nao
   cham; tu cach nam trong hang cho den tu `fls_itl.work_status='UNMAPPED'`,
   `fls_queue_state` chi duoc `LEFT JOIN` vao **de lay ly do**. Mot bai thu da
   ghim dieu nay: `test_luat_XANH_HET_thi_KHONG_ai_vao_hang_cho`.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg  # noqa: E402

from fls.db.kho import dsn_that, noi_chi_doc  # noqa: E402
from fls.repo.danh_muc_actor import ACTOR_DUNG_LAI_SO  # noqa: E402

BIEN_CHO_GHI = "FLS_CHO_GHI_THAT"

# ⛔ Chi dau cac su kien do MAY dan. Mot ly do NGUOI go vao ⛔ khong bao gio
#   bi tep nay cham, ke ca khi no trong giong het.
MAY_DAN = ACTOR_DUNG_LAI_SO          # `WO-011 T1` — chuoi song o SO ACTOR

GOC = pathlib.Path(__file__).resolve().parent.parent
KHO_LUU = GOC / "sao_luu"          # ⛔ gitignore — vet nay mang du lieu that


class ChungMinhHong(SystemExit):
    """⛔ Chung minh ⛔ khong dung ⇒ ⛔ KHONG xoa. Do la ca muc dich tep nay."""


def _cong_moi_truong() -> None:
    if os.environ.get(BIEN_CHO_GHI) != "1":
        raise SystemExit(
            f"⛔ thieu {BIEN_CHO_GHI}=1. Cong cu nay XOA VET trong so ke toan "
            f"THAT — no ⛔ khong duoc chay chi vi ai do go dung ten tep.")


def do(conn) -> dict:
    """Ba phep do cua phan chung minh. ⛔ Khong phep nao la suy luan."""
    c = conn.execute
    tong = c("SELECT count(*) FROM fls_queue_event"
             " WHERE evt_type='reason' AND actor=%s", (MAY_DAN,)).fetchone()[0]
    nguoi = c("SELECT count(*) FROM fls_queue_event"
              " WHERE actor<>%s", (MAY_DAN,)).fetchone()[0]
    khac = c("SELECT count(*) FROM fls_queue_event"
             " WHERE evt_type<>'reason'").fetchone()[0]
    # ⓐ chu ky cau truc — ly do THEO DONG ⛔ khong dan trung 100% so dong
    co_vet = c("SELECT count(DISTINCT itl_id) FROM fls_queue_event"
               " WHERE evt_type='reason' AND actor=%s", (MAY_DAN,)).fetchone()[0]
    so_dong = c("SELECT count(*) FROM fls_itl").fetchone()[0]
    # ⓑ `S3` noi "⛔ khong co TIEN" — dem xem bao nhieu dong mang nhan ay CO tien
    s3 = c("SELECT count(*) FILTER (WHERE coalesce(i.ps_no,0)<>0"
           "                           OR coalesce(i.ps_co,0)<>0), count(*)"
           "   FROM fls_queue_event e JOIN fls_itl i USING (itl_id)"
           "  WHERE e.evt_type='reason' AND e.actor=%s"
           "    AND e.reason LIKE '%%S3%%'", (MAY_DAN,)).fetchone()
    # ⓒ `S2` noi "co tien ma thieu MA" — dem xem bao nhieu dong ay CO ma
    s2 = c("SELECT count(*) FILTER (WHERE coalesce(i.doc_no,'')<>''), count(*)"
           "   FROM fls_queue_event e JOIN fls_itl i USING (itl_id)"
           "  WHERE e.evt_type='reason' AND e.actor=%s"
           "    AND e.reason LIKE '%%S2%%'", (MAY_DAN,)).fetchone()
    return {"tong": tong, "nguoi": nguoi, "khac": khac, "co_vet": co_vet,
            "so_dong": so_dong, "s3": s3, "s2": s2}


def vn(n: int) -> str:
    """⛔ Chi CON SO doi dau, ⛔ khong phai ca cau.

    ⚠ Ban dau toi viet `f"...{n:,}".replace(",", ".")` — va no an luon dau
      phay cua **cau van** quanh so *(`` `reason`, actor= `` → `` `reason`.
      actor= ``)*. ⇒ Phep dinh dang phai bo vao **rieng con so**, ⛔ khong
      quet tren chuoi da ghep.
    """
    return f"{n:,}".replace(",", ".")


def _ty(a: int, b: int) -> str:
    ty = f"{a * 100 / b:.2f}".replace(".", ",") if b else ""
    return f"{vn(a)}/{vn(b)}" + (f" ({ty}%)" if b else "")


def in_chung_minh(m: dict) -> bool:
    """In ba phep do. Tra `True` khi **du** chung minh de xoa."""
    print(f"su kien MAY dan (`reason`, actor={MAY_DAN}) : {vn(m['tong'])}")
    print(f"su kien NGUOI go vao                        : {vn(m['nguoi'])}")
    print(f"su kien loai khac (`defer`/`unmatch`/`done`): {vn(m['khac'])}\n")

    ok_a = m["co_vet"] == m["so_dong"] and m["so_dong"] > 0
    print(f"  {'✔' if ok_a else '✘'} ⓐ chu ky CA LO   : "
          f"{_ty(m['co_vet'], m['so_dong'])} dong so mang ly do")
    if not ok_a:
        print("      ⛔ ⛔ KHONG phai 100% ⇒ mot phan su kien CO THE la ly do "
              "THAT ⇒ ⛔ khong xoa mu.")

    s3_dung, s3_tong = m["s3"]
    ok_b = s3_tong > 0 and s3_dung == s3_tong
    print(f"  {'✔' if ok_b else '✘'} ⓑ `S3` tu mau thuan: "
          f"{_ty(s3_dung, s3_tong)} dong bi bao \"⛔ khong co TIEN\" — CO tien")

    s2_dung, s2_tong = m["s2"]
    ok_c = s2_tong > 0 and s2_dung / s2_tong > 0.99
    print(f"  {'✔' if ok_c else '✘'} ⓒ `S2` sai gan het : "
          f"{_ty(s2_dung, s2_tong)} dong bi bao \"thieu MA\" — CO ma")
    return ok_a and ok_b and ok_c


def luu_vet(conn, dich: pathlib.Path) -> int:
    """⛔ Chep CA 108k dong ra `sao_luu/` TRUOC khi xoa.

    ⚠ Day la mot bang **VET**: ke ca khi noi dung sai, viec no **da tung ton
      tai** la mot su that ve he thong. Xoa ma ⛔ khong luu lai la bo mat kha
      nang tra loi cau *"hom ay may da noi gi"*.
    """
    dich.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with dich.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("evt_id", "itl_id", "evt_type", "reason", "actor", "at"))
        cur = conn.execute(
            "SELECT evt_id, itl_id, evt_type, reason, actor, at"
            "  FROM fls_queue_event WHERE evt_type='reason' AND actor=%s"
            "  ORDER BY evt_id", (MAY_DAN,))
        for h in cur:
            w.writerow(h)
            n += 1
    return n


def chay(duyet: bool) -> int:
    print("== DON LY DO MAY DAN NHAM (GAP-NAP-01) ==\n")
    with noi_chi_doc(dsn_that()) as conn:
        m = do(conn)
        du = in_chung_minh(m)
    if not m["tong"]:
        print("\n✅ ⛔ khong con su kien nao cua MAY — da don roi.")
        return 0
    if not du:
        raise ChungMinhHong(
            "\n⛔ ⛔ CHUNG MINH KHONG DU ⇒ ⛔ KHONG xoa. Mot bang VET chi duoc "
            "xoa khi do duoc rang no SAI — ⛔ khong phai khi no PHIEN.")
    print(f"\n⇒ ca ba phep do dat ⇒ {vn(m['tong'])} su kien la RAC do "
          f"`GAP-NAP-01`")
    if not duyet:
        print("\n⛔ ⛔ CHUA XOA — them `--duyet` va "
              f"`{BIEN_CHO_GHI}=1` de xoa that")
        return 0

    _cong_moi_truong()
    ten = f"queue_event_ly_do_sai_{dt.datetime.now():%Y%m%dT%H%M%S}.csv"
    with psycopg.connect(dsn_that(), autocommit=False) as conn:
        n = luu_vet(conn, KHO_LUU / ten)
        print(f"\n💾 da luu vet: sao_luu/{ten} ({vn(n)} dong)")
        xoa = conn.execute(
            "DELETE FROM fls_queue_event WHERE evt_type='reason' AND actor=%s",
            (MAY_DAN,)).rowcount
        if xoa != n:
            conn.rollback()
            raise ChungMinhHong(
                f"⛔ luu {n} ma xoa {xoa} ⇒ so lech ⇒ da HOAN TAC, ⛔ khong xoa")
        conn.commit()
        print(f"🗑  da xoa {vn(xoa)} su kien")

    with noi_chi_doc(dsn_that()) as conn:
        con = conn.execute("SELECT count(*) FROM fls_queue_event").fetchone()[0]
        cho = conn.execute("SELECT count(*) FROM fls_itl"
                           " WHERE work_status='UNMAPPED'").fetchone()[0]
    print(f"\n✅ `fls_queue_event` con {vn(con)} su kien")
    print(f"✅ hang cho van {vn(cho)} dong — tu cach nam trong hang cho den tu")
    print("   `fls_itl.work_status`, ⛔ KHONG tu su kien ⇒ xoa vet ⛔ khong"
          " lam ai bien mat khoi hang cho.")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--duyet", action="store_true",
                   help=f"XOA that (can ca {BIEN_CHO_GHI}=1)")
    return chay(p.parse_args().duyet)


if __name__ == "__main__":
    raise SystemExit(main())
