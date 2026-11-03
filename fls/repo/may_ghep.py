# -*- coding: utf-8 -*-
"""MAY ghep xong thi GOI Y `hd`/`cdt1` — ⛔ khong QUYET.

⭐⭐⭐ `QĐ-ITL-143` · owner chot **phuong an B** `2026-09-18` · chang 1.

── VI SAO TEP NAY TON TAI ──────────────────────────────────────────────
Duong ghep **TAY** (`ghi_tay.ghep_lenh`) suy `hd`/`cdt1` tu dong lenh tu
`28/08`. Duong ghep **TU DONG** (`chay_nap.chen_moi_noi`) thi ⛔ **khong** —
no chen moi noi roi dung. Do tren kho that `18/09` (`pm_line_id` PHAN BIET):

    `fls_itl`        8.387 dong · `hd` **0** · `cdt1` **0** · ca hai `*_thyt` **0**
    dong lenh THAT   3.772      · co `hd` **3.767** (99,9%) · `cdt1` **3.763**
    dong so DA ghep  2.222      ⇒ suy duoc `hd` **2.219** · `cdt1` **2.217**
    ⚠                            **10** dong so co N dong lenh noi HAI `hd` KHAC NHAU

⇒ Cau tra loi **da nam san trong kho**. Tep nay bac cau — va bac **dung cach**.

── HAI DIEU TEP NAY ⛔ KHONG LAM, VA CHUNG LA LY DO NO TON TAI ─────────

⛔⛔ ⓐ **⛔ KHONG ghi vao `fls_sua_tay`.** Khung xem ay tra loi *"NGUOI da chot
   gi"* va `bang_tuyen.py` co **8 tuyen** doc no voi dung nghia ay. But toan o
   day mang `nguon='may_goi_y'`, nen `fls_sua_tay` (loc `nguon='sua_tay'`,
   migration `0025`) ⛔ **khong thay** chung. Man hinh doc `fls_may_goi_y` de
   ve *"may doan X — anh gat ⛔ khong?"*.

⛔⛔ ⓑ **⛔ KHONG de len o NGUOI da chot.** Lan nap chay theo **nhip gio**
   (`8h–19h`, toi **12 lan/ngay**) va ⛔ khong ai ngoi xem. Neu may duoc ghi de
   thi mot lan nap se **lat ket luan cua nguoi trong im lang** — dung thu
   `INV-I16` cam, va lan nay no chay **tu dong**, tuc no lat **hang loat**.

⭐ Va phep suy la **DUNG MOT** phep, dung chung voi duong tay (`suy_hd_cdt1`):
  hai ban sao la hai cho de chung lech nhau, va cai lech ay hien ra duoi dang
  *"ghep tay ra mot so, may nap ra so khac"* — ⛔ khong cong nao bat duoc.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from fls.repo.danh_muc_actor import ACTOR_MAY_GHEP

# ⭐ `loc_goi_y` + `ghi_goi_y` SONG o `ghi_tay` (cho duy nhat ghi) tu `WO-003`:
#   duong TAY goi chung truc tiep — mot `import` trong than ham thi cong
#   `soi_bang_tuyen` (doc TINH, chi bam ham muc module) ⛔ thay bang cham.
from fls.repo.ghi_tay import (NGUON_TAY, _them_su_kien, ghi_goi_y,
                              loc_goi_y)

# ⛔ Dung hai truong nay. `QĐ-ITL-64` ha tap go duoc tu 10 xuong 7, nhung phep
#   suy tu dong lenh chi noi duoc **hai** — dong lenh ⛔ khong mang nam truong kia.
TRUONG_SUY: tuple[str, ...] = ("hd", "cdt1")

# ⛔ `actor` cua may. ⛔ Khong de rong va ⛔ khong muon ten mot nguoi: mot but
#   toan ⛔ khong biet ai lam la mot vet ⛔ khong doc duoc (`AUD-1`).
# ⭐ `WO-011 T1`: chuoi song o SO ACTOR *(`fls/repo/danh_muc_actor.py`)* — mot
#   tien trinh may moi phai khai o do, ⛔ go chuoi o day.
MAY = ACTOR_MAY_GHEP


def suy_hd_cdt1(lenh: Sequence[Mapping[str, Any]]
                ) -> tuple[dict[str, str], list[str]]:
    """`(suy, khong_suy_duoc)` — ⭐ MOT phep, dung chung TAY lan MAY.

    ⭐⭐ **Luat: chi suy khi CA N dong lenh dong y.** N dong noi N thu thi may
       ⛔ **khong chon** — no khai ra la ⛔ khong suy duoc (`INV-I16`).

    ⛔⛔ Lay dong dau tien la mot dap an **trong hop ly**, va do la cai nguy
       hiem cua no: ⛔ khong ai nghi ngo mot con so co ve dung. Do `18/09`:
       **10** dong so roi vao ca nay.
    """
    suy: dict[str, str] = {}
    khong: list[str] = []
    for f in TRUONG_SUY:
        gt = {(x.get(f) or "").strip() for x in lenh}
        gt.discard("")
        if len(gt) == 1:
            suy[f] = next(iter(gt))
        elif gt:
            khong.append(f)
    return suy, khong


def ghi_goi_y_may(conn, *, itl_id: int,
                  lenh: Sequence[Mapping[str, Any]],
                  run_pm: str | None = None) -> dict[str, Any]:
    """Ghi GOI Y cua may cho mot dong so vua duoc may ghep.

    Tra: `but_toan` (da ghi) · `khong_suy_duoc` · ⭐ `nguoi_da_chot`
    (truong may **im lang bo qua** vi da co nguoi quyet).

    ⚠ Goi trong giao dich cua lan nap — ⛔ khong mo giao dich rieng: mot lan
      nap de lai moi noi ma thieu goi y la mot trang thai nua ⛔ khong ai giai
      thich duoc.
    """
    suy, khong_suy_duoc = suy_hd_cdt1(lenh)
    ma = sorted({str(x.get("pm_line_id")) for x in lenh if x.get("pm_line_id")})

    can_ghi, nguoi_da_chot = loc_goi_y(conn, itl_id, suy)
    if not can_ghi:
        return {"itl_id": itl_id, "but_toan": [],
                "khong_suy_duoc": khong_suy_duoc,
                "nguoi_da_chot": nguoi_da_chot}

    evt_id = _them_su_kien(
        conn, itl_id=itl_id, evt_type="match", actor=MAY,
        reason=f"may tu ghep {len(ma)} dong lenh ({', '.join(ma)})")
    but = ghi_goi_y(
        conn, itl_id=itl_id, can_ghi=can_ghi, actor=MAY, evt_id=evt_id,
        reason=f"may suy tu dong lenh da ghep ({', '.join(ma)})"
               + (f" · anh PM {run_pm}" if run_pm else ""))

    return {"itl_id": itl_id, "evt_id": evt_id, "but_toan": but,
            "khong_suy_duoc": khong_suy_duoc,
            "nguoi_da_chot": nguoi_da_chot}


__all__ = ["MAY", "TRUONG_SUY", "ghi_goi_y", "ghi_goi_y_may", "loc_goi_y",
           "suy_hd_cdt1", "NGUON_TAY"]
