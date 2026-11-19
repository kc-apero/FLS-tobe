"""H5 — `fls.bao_cao.cfa.cfa1_daily`: Σ theo (khối LE, HD, ngày) trên cây IX.HD *(ISP 3.1.2 · Step 16)*.

Bài dẫn từ mục 6 + 8 của Step 16 *(WO-164)*:
  · **H5-B1** *(AC-1)* — cây 3 nút `P ← {A, B}` ⇒ ô cha = Σ hai con, do ENGINE tính *(⛔ đọc cha từ
    đâu cả)*; dòng sổ GÁN THẲNG vào nút cha ⇒ ⛔ cộng vào cha *(AS-IS: hàng cha là `=sum(con)`,
    SUMIFS chỉ ở hàng lá)*, đếm ra `dong_nhan_cha`.
  · khối `GROUP` = Σ MỌI dòng *(⛔ lọc LE)*; khối LE = chỉ dòng có `le` đúng mã *(công thức SA 18/11:
    GROUP ⛔ điều kiện cột P; khối LE thêm `P = mã LE`)*.
  · nhãn HD so KHÔNG phân biệt hoa thường *(SUMIFS)*; nhãn ⛔ thuộc cây ⇒ `dong_ngoai_cay`.
  · ngày ngoài trục ⇒ `dong_ngoai_truc` *(⛔ rơi im lặng)*.
"""
from __future__ import annotations

from decimal import Decimal as D

import pytest

from fls.bao_cao.cfa import KHOI_TONG, DongCFA, cfa1_daily
from fls.cau_hinh.hd import CayHD, NutHD


def _cay3() -> CayHD:
    return CayHD(nguon="bai", nut=(
        NutHD(ma="P", ten="Cha", cha=None, cap=1, nhom="HDO", dong_sheet="1", thu_tu=1),
        NutHD(ma="A", ten="Con A", cha="P", cap=2, nhom="HDO", dong_sheet="2", thu_tu=2),
        NutHD(ma="B", ten="Con B", cha="P", cap=2, nhom="HDO", dong_sheet="3", thu_tu=3),
    ))


def _d(ngay, le, hd, no="0", co="0"):
    return DongCFA(ngay=ngay, le=le, hd=hd, musd_no=D(no), musd_co=D(co))


def test_H5_B1_cha_bang_tong_hai_con_do_engine_tinh():
    dong = [_d(1, "SGO2", "A | Con A", no="3"),
            _d(1, "SGO1", "B | Con B", no="5", co="1"),
            _d(2, "SGO2", "B | Con B", co="2")]
    kq = cfa1_daily(dong, _cay3(), ngay=(1, 2), khoi=(KHOI_TONG, "SGO2"))
    o = kq.o
    # lá = Σ Nợ − Σ Có theo (khối, mã, ngày)
    assert o[(KHOI_TONG, "A", 1)] == D("3") and o[(KHOI_TONG, "B", 1)] == D("4")
    # cha = Σ con (engine) — ⛔ có dòng sổ nào nhãn P
    assert o[(KHOI_TONG, "P", 1)] == D("7")
    assert o[(KHOI_TONG, "P", 2)] == D("-2")
    # khối LE chỉ lấy dòng cùng LE
    assert o[("SGO2", "A", 1)] == D("3") and o[("SGO2", "B", 1)] == D("0")
    assert o[("SGO2", "P", 1)] == D("3") and o[("SGO2", "P", 2)] == D("-2")
    # lưới ĐỦ: mọi (khối, mã, ngày) có ô — 2 khối × 3 mã × 2 ngày
    assert len(o) == 12


def test_H5_B1_dong_gan_nut_cha_KHONG_cong_vao_cha_va_duoc_dem():
    dong = [_d(1, None, "A | Con A", no="1"), _d(1, None, "P | Cha", no="100")]
    kq = cfa1_daily(dong, _cay3(), ngay=(1,), khoi=(KHOI_TONG,))
    assert kq.o[(KHOI_TONG, "P", 1)] == D("1")
    assert kq.dong_nhan_cha == [1]


def test_H5_B1_nhan_khong_phan_biet_hoa_thuong__nhan_ngoai_cay_dem_rieng():
    dong = [_d(1, None, "a | con a", no="2"),       # SUMIFS ⛔ phân biệt hoa thường ⇒ vào A
            _d(1, None, "Con A", no="9"),            # thiếu mã ⇒ ⛔ khớp nhãn nào
            _d(1, None, None, no="9")]
    kq = cfa1_daily(dong, _cay3(), ngay=(1,), khoi=(KHOI_TONG,))
    assert kq.o[(KHOI_TONG, "A", 1)] == D("2")
    assert kq.dong_khac_hoa == [0]
    assert kq.dong_ngoai_cay == [1, 2]


def test_H5_B1_ngay_ngoai_truc_dem_rieng_khong_roi_im_lang():
    kq = cfa1_daily([_d(9, None, "A | Con A", no="1")], _cay3(), ngay=(1,), khoi=(KHOI_TONG,))
    assert kq.dong_ngoai_truc == [0]
    assert kq.o[(KHOI_TONG, "A", 1)] == D("0")


def test_H5_AC4_doi_dau_vao_thi_doi_dung_o_la_va_cac_cha():
    """Đầu vào DUY NHẤT là dòng sổ + cây + trục: đổi một dòng ⇒ đúng lá ấy + mọi tổ tiên đổi."""
    goc = [_d(1, "SGO2", "A | Con A", no="1"), _d(1, "SGO2", "B | Con B", no="1")]
    dot = [_d(1, "SGO2", "A | Con A", no="1.5"), goc[1]]
    a = cfa1_daily(goc, _cay3(), ngay=(1,), khoi=(KHOI_TONG, "SGO2")).o
    b = cfa1_daily(dot, _cay3(), ngay=(1,), khoi=(KHOI_TONG, "SGO2")).o
    doi = {k for k in a if a[k] != b[k]}
    assert doi == {(KHOI_TONG, "A", 1), (KHOI_TONG, "P", 1), ("SGO2", "A", 1), ("SGO2", "P", 1)}


def test_H5_khoi_GROUP_phai_dung_dau__khoi_rong_bi_tu_choi():
    with pytest.raises(ValueError):
        cfa1_daily([], _cay3(), ngay=(1,), khoi=())
