"""Cai chan "khong do gi ma bao XANH".

Test dau tien duoi day la test QUAN TRONG NHAT cua module: no khoa dung cai loi
that da xay ra — script parity doc duoc 0 dong, so 0 o, roi in "khop 100%" va
tra PASS.
"""
from __future__ import annotations

from fls.oracle.cong_parity import danh_gia

MONG = 9219       # so dong da do doc lap tren `ITL Ledge`


def test_khong_do_duoc_gi_thi_PHAI_khong_dat():
    """⛔ Loi that 2026-08-26: 0 dong / 0 o ma bao 'khop 100%' + PASS."""
    px = danh_gia(tong_o=0, khop=0, lat_truot=3, dong_doc=0, dong_mong_doi=MONG)
    assert not px.dat
    assert any("khong do duoc gi" in l for l in px.ly_do)
    assert any("lo trong" in l for l in px.ly_do)


def test_luot_doc_day_du_va_khop_het_thi_dat():
    px = danh_gia(tong_o=64533, khop=64533, lat_truot=0, dong_doc=MONG,
                  dong_mong_doi=MONG)
    assert px.dat and px.ly_do == () and px.mot_dong == "DAT"


def test_mot_lat_bi_bo_lai_thi_khong_dat_du_moi_o_deu_khop():
    """Lo trong trong du lieu => khong duoc noi "ca so", du phan doc duoc sach."""
    px = danh_gia(tong_o=50000, khop=50000, lat_truot=1, dong_doc=7000,
                  dong_mong_doi=MONG)
    assert not px.dat and any("lo trong" in l for l in px.ly_do)


def test_hut_dong_qua_nguong_thi_khong_dat():
    """Hut 22 dong im lang tung xay ra that — nen so dong phai duoc doi chieu."""
    px = danh_gia(tong_o=40000, khop=40000, lat_truot=0, dong_doc=4600,
                  dong_mong_doi=MONG)
    assert not px.dat and any("mong doi" in l for l in px.ly_do)


def test_hut_vai_dong_trong_sai_so_thi_van_dat():
    px = danh_gia(tong_o=64000, khop=64000, lat_truot=0, dong_doc=MONG - 20,
                  dong_mong_doi=MONG)
    assert px.dat, px.ly_do


def test_mot_o_lech_la_khong_dat_khong_co_dung_sai():
    px = danh_gia(tong_o=64533, khop=64532, lat_truot=0, dong_doc=MONG,
                  dong_mong_doi=MONG)
    assert not px.dat and any("1/64533 o LECH" in l for l in px.ly_do)


def test_gom_nhieu_ly_do_chu_khong_dung_o_ly_do_dau():
    px = danh_gia(tong_o=10, khop=5, lat_truot=2, dong_doc=10,
                  dong_mong_doi=MONG)
    assert len(px.ly_do) >= 3, px.ly_do


def test_khong_khai_mong_doi_thi_bo_qua_phep_doi_chieu_dong():
    px = danh_gia(tong_o=2000, khop=2000, lat_truot=0, dong_doc=1,
                  dong_mong_doi=0)
    assert px.dat
