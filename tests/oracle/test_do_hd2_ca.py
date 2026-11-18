"""H4 — `tools/do_hd2.py --goi WP-C2`: parity CA.GL ↔ đáp án 406 mọi kỳ *(ISP 3.1.2 · Step 13)*.

Bài dẫn từ mục 6 + 8 của Step 13 *(WO-132)*:
  · **H4-B1** — chạy WP-C2 trên ảnh thật: số ô so > 0 và = số ô ĐÁP ÁN so được; cả 8 cột BM…BT
    khớp trong dung sai; lệch CÓ TÊN đúng MONG *(6 hàng thiếu D · 4 hàng itl_id #N/A · kỳ vắng 406
    · 0 tháng thiếu tỷ giá)*; 0 lệch NGOÀI tên.
  · **H4-B2** — đáp án RỖNG ⇒ ĐỎ `0 ô` *(Đ3: mẫu số 0 là KẾT QUẢ)*.
  · **H4-B3** — MONG lệch khai TRƯỚC; khác ⇒ ĐỎ CẢ HAI CHIỀU *(Đ5)*: (a) một ô lệch NGOÀI tên ⇒
    ĐỎ; (b) tập lệch-có-tên THỰC ≠ MONG ⇒ ĐỎ.

⭐ Số dư đầu kỳ gõ tay ở hàng 24 *(5 ô — `SoDuDau`)* được GIEO từ ảnh đầu vào; thiếu nó thì BM·BN·
BQ·BT lệch ~56.84e9 bVND từ ds24 *(đo 18/11)* — bài B1 chứng cả 8 cột về 0 nhờ gieo.
"""
from __future__ import annotations

import pathlib
import sys
from decimal import Decimal as D

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))

from tools import do_hd2  # noqa: E402


# ── trợ giúp dựng ảnh nhỏ cho B2/B3 (hình y ảnh đóng băng thật) ──────────────────

def _chu(s):
    return {"chu": s}


def _hang_vao(ds, ky, itl, d, e, f):
    return {"dong_sheet": str(ds), "ky": str(ky), "itl_id": _chu(itl),
            "D": (_chu(d) if d is not None else None),
            "E": (str(e) if e is not None else None),
            "F": (str(f) if f is not None else None)}


def _hang_dap_an(ds, ky, itl, d, **cot):
    r = {"dong_sheet": str(ds), "ky": str(ky), "itl_id": _chu(itl),
         "D": (_chu(d) if d is not None else None)}
    for c in ("BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT"):
        r[c] = (str(cot[c]) if cot.get(c) is not None else None)
    return r


def _anh_vao(dong, so_du_dau=()):
    return {"dong": dong, "phu": {"itl_id_lech": {"dong": []},
                                  "so_du_dau": {"dong": list(so_du_dau)}}}


def _fx(thang=(202501,)):
    return {t: {"USD": D("25000"), "SGD": D("18000"), "COP": D("6"),
                "VND": D("1"), "HKD": D("3200")} for t in thang}


# ── H4-B1 · ảnh thật ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def tq_that():
    return do_hd2.chay_wp_c2()


def test_H4_B1_so_o_so_lon_hon_0_va_bang_so_o_dap_an_so_duoc(tq_that):
    assert tq_that.tong_o > 0
    assert tq_that.tong_o == tq_that.so_o_dap_an_so_duoc, (
        tq_that.tong_o, tq_that.so_o_dap_an_so_duoc)


def test_H4_B1_ca_8_cot_khop_trong_dung_sai(tq_that):
    assert tq_that.khop == tq_that.tong_o, f"{tq_that.tong_o - tq_that.khop} ô lệch ngoài tên"
    assert tq_that.lech == [], tq_that.lech[:5]
    assert tq_that.phan_xu.dat, tq_that.phan_xu.mot_dong


def test_H4_B1_lech_co_ten_dung_MONG(tq_that):
    lct = tq_that.lech_co_ten
    assert sorted(lct["thieu_tien_te_D"]) == list(do_hd2.MONG_THIEU_D)
    assert sorted(lct["itl_id_na"]) == list(do_hd2.MONG_ITL_NA)
    assert set(lct["ky_vang_406"]) == {str(k) for k in do_hd2.MONG_KY_VANG}
    # 0 tháng thiếu tỷ giá trong dải so được — Đ3: khai mẫu số (số tháng đã phủ)
    assert lct["thang_thieu_ty_gia"] == []
    assert tq_that.mau_so_thang > 0


# ── H4-B2 · đáp án rỗng ⇒ ĐỎ 0 ô (Đ3) ───────────────────────────────────────────

def test_H4_B2_dap_an_rong_thi_DO_0_o():
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", None, 1000)])
    tq = do_hd2.so_sanh(vao, {"dong": []}, _fx(), {202501: 1}, do_hd2.mong_mac_dinh())
    assert tq.tong_o == 0
    assert not tq.phan_xu.dat
    assert any("0" in l for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


# ── H4-B3 · MONG khai trước; khác ⇒ ĐỎ cả hai chiều (Đ5) ─────────────────────────

def test_H4_B3a_mot_o_lech_NGOAI_ten_thi_DO():
    # VND Nợ 1000 @ rate 1 ⇒ BO = 1000/1e9 = 1e-6; đáp án CỐ TÌNH ghi sai BO.
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000999"), BP=0, BQ=D("0.000001"),  # BO sai (0.000999 ≠ 1e-6)
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, do_hd2.mong_mac_dinh())
    assert not tq.phan_xu.dat
    assert tq.lech, "phải có ít nhất một ô lệch ngoài tên"
    assert any(x["cot"] == "BO" for x in tq.lech)


def test_H4_B3b_tap_lech_co_ten_KHAC_mong_thi_DO():
    # dữ liệu khớp sạch, 0 lệch có tên; nhưng MONG đòi 1 hàng thiếu D ⇒ lệch mong ⇒ ĐỎ.
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000001"), BP=0, BQ=D("0.000001"),
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    mong = do_hd2.Mong(thieu_D=(999,), itl_na=(), ky_vang={}, thang_thieu_ty_gia=(),
                       dung_sai=do_hd2.DungSai())
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, mong)
    assert not tq.phan_xu.dat
    assert any("thieu_tien_te_D" in l or "lệch có tên" in l or "mong" in l.lower()
               for l in tq.phan_xu.ly_do), tq.phan_xu.ly_do


def test_H4_B1_THIEU_gieo_so_du_dau_thi_DO_tu_ds24():
    """⭐ Chứng cổng: số dư đầu kỳ GÕ TAY là load-bearing. Bỏ `so_du_dau` khỏi ảnh đầu vào ⇒
    BM·BN·BQ·BT lệch từ ds24 *(đo 18/11: ~56.84e9 bVND)* ⇒ hàng NGHÌN ô lệch NGOÀI tên ⇒ ĐỎ.
    *(Đ5: phá nguồn → chạy → xem nó cắn; ảnh trả nguyên vì đọc bản sao.)*"""
    vao = do_hd2.nap_anh(do_hd2.ANH_DAU_VAO)
    vao["phu"] = dict(vao["phu"])
    vao["phu"]["so_du_dau"] = {"dong": []}            # ⛔ gieo số dư đầu kỳ
    tq = do_hd2.so_sanh(vao, do_hd2.nap_anh(do_hd2.ANH_DAP_AN), do_hd2.nap_fx(),
                        do_hd2.nap_phan_bo(), do_hd2.mong_mac_dinh())
    assert not tq.phan_xu.dat
    assert len(tq.lech) > 1000, len(tq.lech)
    assert all(int(x["dong_sheet"]) >= 24 for x in tq.lech)      # khớp sạch TRƯỚC ds24
    assert {x["cot"] for x in tq.lech} <= {"BM", "BN", "BQ", "BT"}  # chỉ cột lũy kế/đánh giá lại


def test_H4_B3_khop_sach_khi_dung_mong_thi_DAT():
    """Chiều DƯƠNG của Đ5: khớp sạch + lệch-có-tên = mong ⇒ ĐẠT (cổng ⛔ xanh mù)."""
    vao = _anh_vao([_hang_vao(10, 202501, "ITL#1", "VND", 1000, None)])
    da = [_hang_dap_an(10, 202501, "ITL#1", "VND", BM=1000, BN=D("0.00000004"),
                       BO=D("0.000001"), BP=0, BQ=D("0.000001"),
                       BR=D("0.00000004"), BS=0, BT=D("0.00000004"))]
    mong = do_hd2.Mong(thieu_D=(), itl_na=(), ky_vang={}, thang_thieu_ty_gia=(),
                       dung_sai=do_hd2.DungSai())
    tq = do_hd2.so_sanh(vao, {"dong": da}, _fx(), {202501: 1}, mong)
    assert tq.phan_xu.dat, tq.phan_xu.mot_dong
    assert tq.tong_o == 8 and tq.khop == 8
