"""Dung lai ngay tu ban .xlsx doc sai bang chu — va nhung cho phai NO."""
from __future__ import annotations

from datetime import date, datetime

import pytest

from fls.oracle.ngay_xlsx import NgayMoHo, doc_ngay, kiem_bu_tru


# ---- o dang CHUOI: chac chan M/D/YYYY khi phan tu 2 > 12 ------------------

def test_chuoi_MDY_ro_rang_thi_doc_dung():
    assert doc_ngay("10/21/2024") == date(2024, 10, 21)
    assert doc_ngay(" 3/31/2026 ") == date(2026, 3, 31)
    assert doc_ngay("12/25/2025") == date(2025, 12, 25)


def test_chuoi_ca_hai_phan_tu_duoi_12_thi_NO__khong_doan():
    """⛔ `3/5/2026` — 3 thang 5 hay 5 thang 3? Khong biet thi khong doan."""
    with pytest.raises(NgayMoHo, match="khong biet dau la thang"):
        doc_ngay("3/5/2026")
    with pytest.raises(NgayMoHo):
        doc_ngay("12/12/2026")


def test_chuoi_rac_thi_NO():
    for v in ("", "hom qua", "2026-03-01", "1/2", None, "31/31/2026"):
        with pytest.raises(NgayMoHo):
            doc_ngay(v)


# ---- o dang NGAY: ca tap bi hoan, hoan lai ---------------------------------

def test_o_kieu_ngay_duoc_hoan_lai_thang_va_ngay():
    """May doc `4/12/2026` (4 thang 12) thanh 12 thang 4 => hoan lai."""
    assert doc_ngay(date(2026, 12, 4)) == date(2026, 4, 12)
    assert doc_ngay(datetime(2026, 9, 3, 0, 0)) == date(2026, 3, 9)


def test_o_kieu_ngay_co_ngay_lon_hon_12_thi_NO():
    """⛔ O nay KHONG thuoc tap bi hoan — hoan lai la lam sai mot o dang dung."""
    with pytest.raises(NgayMoHo, match="KHONG thuoc tap bi hoan"):
        doc_ngay(date(2026, 3, 25))


def test_hoan_lai_hai_lan_thi_ve_cho_cu():
    """Tinh chat kiem tra duoc: hoan la mot phep doi xung."""
    d = date(2026, 12, 4)
    assert doc_ngay(doc_ngay(d)) == d


# ---- cong BU TRU: dieu kien duoc phep dung `doc_ngay` cho ca cot -----------

def test_bu_tru_khi_hai_tap_khong_chong_nhau():
    o = ["10/21/2024", "11/30/2025", date(2026, 12, 4), date(2026, 9, 3)]
    bt = kiem_bu_tru(o)
    assert bt.bu_tru and bt.ly_do() == ""
    assert (bt.chuoi_ro, bt.ngay_hoan) == (2, 2)
    assert (bt.chuoi_mo_ho, bt.ngay_ro) == (0, 0)


def test_KHONG_bu_tru_khi_con_o_chuoi_mo_ho():
    bt = kiem_bu_tru(["10/21/2024", "3/5/2026"])
    assert not bt.bu_tru
    assert "khong biet dau la thang" in bt.ly_do()


def test_KHONG_bu_tru_khi_co_o_ngay_that():
    """Cot lan ca ngay THAT va ngay bi hoan => ⛔ khong duoc dung mot luat chung."""
    bt = kiem_bu_tru(["10/21/2024", date(2026, 3, 25)])
    assert not bt.bu_tru
    assert "ngay > 12" in bt.ly_do()


def test_bo_qua_o_trong_khong_tinh_vao_hai_tap():
    bt = kiem_bu_tru([None, "", "   ", "10/21/2024"])
    assert (bt.chuoi_ro, bt.chuoi_mo_ho, bt.khong_doc_duoc) == (1, 0, 0)
    assert bt.bu_tru


def test_o_khong_doc_duoc_duoc_DEM_chu_khong_bi_bo_qua():
    bt = kiem_bu_tru(["10/21/2024", "hom qua", "2026-03-01"])
    assert bt.khong_doc_duoc == 2


# ---- so THAT tren file owner vua dan -------------------------------------

def test_con_so_do_tren_file_Master_dung_nhu_da_cong_bo():
    """Khoa lai con so lam can cu cho ca quyet dinh: hai tap BU TRU 100%.

    Neu ban .xlsx sau nay doi co che (vi du bat dau lan ngay that), test nay
    khong bat duoc — nhung `kiem_bu_tru` chay trong pipeline se bat. Day chi la
    ban ghi lai con so da do ngay 2026-08-26.
    """
    DO_THAT = {"chuoi_ro": 5580, "chuoi_mo_ho": 0,
               "ngay_hoan": 4387, "ngay_ro": 0}
    assert DO_THAT["chuoi_mo_ho"] == 0 and DO_THAT["ngay_ro"] == 0
    assert DO_THAT["chuoi_ro"] + DO_THAT["ngay_hoan"] == 9967
