"""H1 · tham số tuỳ chọn `so_du_dau` *(H4 · WO-132)* — số dư đầu kỳ gõ tay cộng tại MỘT vị trí dòng.

Mong TÍNH TAY *(⛔ gọi lại công thức mã)*. `so_du_dau` là THAM SỐ TƯỜNG MINH: mặc định ⛔ có ⇒ H1
thuần *(bài H1 cũ ⛔ đụng — ghim ở `test_default_None_y_het_khong_truyen`)*.
"""
from __future__ import annotations

from decimal import Decimal as D

import pytest

from fls.bao_cao.gl import DongGL, SoDuDau, TienTeNgoaiGL, tinh_gl

FX = {202501: {"USD": D("25000"), "SGD": D("18000"), "COP": D("6"), "VND": D("1"),
               "HKD": D("3200")}}


def _hai_dong_vnd():
    return [DongGL(thang=202501, tien_te="VND", no=D("1000"), co=D("0")),
            DongGL(thang=202501, tien_te="VND", no=D("500"), co=D("0"))]


def test_default_None_y_het_khong_truyen():
    """Mặc định `so_du_dau=None` ⇒ KẾT QUẢ y hệt lượt ⛔ truyền *(H1 cũ ⛔ đụng)*."""
    a = tinh_gl(_hai_dong_vnd(), FX)
    b = tinh_gl(_hai_dong_vnd(), FX, so_du_dau=None)
    c = tinh_gl(_hai_dong_vnd(), FX, so_du_dau={})
    assert a == b == c
    assert a[1].ton["USD"] == D("0") and a[1].vnd_ton_all == D("1500")


def test_gieo_ton_ngoai_te_danh_gia_lai_o_BM_va_mang_sang_dong_sau():
    """Gieo USD 200 tại dòng 2 ⇒ tồn USD = 200 *(⛔ VND thay đổi)*; BM đánh giá lại USD×tỷ giá.
    BM2 = tồn VND 1.500 + 200 × 25.000 = 5.001.500; BN2 = 5.001.500 / 25.000 / 10^6 = 0,00020006."""
    sd = {2: SoDuDau(ton_them={"USD": D("200")})}
    k = tinh_gl(_hai_dong_vnd(), FX, so_du_dau=sd)
    assert k[0].ton["USD"] == D("0")               # dòng 1 CHƯA gieo
    assert k[1].ton["USD"] == D("200") and k[1].ton["VND"] == D("1500")
    assert k[1].vnd_ton_all == D("5001500")
    assert k[1].musd_ton_all == D("0.00020006")


def test_gieo_hang_bvnd_va_musd_vao_luy_ke_BQ_BT():
    """`bvnd_ton_them`/`musd_ton_them` cộng vào BQ/BT *(đúng ô `BQ24=…+hằng`, `BT24=…+hằng`)*.
    BQ1 = 1.000/10^9 = 1e-6; BO2 = 500/10^9 = 5e-7 ⇒ BQ2 trước gieo = 1,5e-6; + 5 = 5,0000015.
    BR2 = BO2 / 25.000 × 10^3 = 2e-8; BT1 = BR1 = 1e-6/25.000×10^3 = 4e-8 ⇒ BT2 trước = 6e-8; + 0,2."""
    sd = {2: SoDuDau(ton_them={}, bvnd_ton_them=D("5"), musd_ton_them=D("0.2"))}
    k = tinh_gl(_hai_dong_vnd(), FX, so_du_dau=sd)
    assert k[1].bvnd_ton == D("5.0000015")
    assert k[1].musd_ton == D("0.2") + D("0.00000006")


def test_gieo_tien_te_ngoai_5_cot_thi_nem_TienTeNgoaiGL():
    sd = {1: SoDuDau(ton_them={"EUR": D("100")})}
    with pytest.raises(TienTeNgoaiGL):
        tinh_gl(_hai_dong_vnd(), FX, so_du_dau=sd)


def test_SoDuDau_dong_bang_va_pickle_duoc():
    """Số dư đầu kỳ đi qua ranh giới tiến trình *(cùng lý do `H1-R3-01`)* — `frozen` + pickle."""
    import pickle
    sd = SoDuDau(ton_them={"USD": D("1242689")}, bvnd_ton_them=D("56.842628558"),
                 musd_ton_them=D("2.267718"))
    ban = pickle.loads(pickle.dumps(sd))
    assert ban == sd
