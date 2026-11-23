# -*- coding: utf-8 -*-
"""Đ6 · Bang chung rang bay luat `nguon_song` **DO DUOC**.

⭐⭐ **Vi sao bo bai nay ton tai.** Cong `tools/kiem_nguon_song.py` doc Google
   Sheets **song**. Mot cong doc mang thi ⛔ **khong the tu chung minh no do
   duoc** — muon thay no do thi phai **lam hong so that**. ⇒ Luat tach ra
   thanh ham **thuan**, va o day moi luat co **ba ca**:

     · ca XANH   — du lieu dung
     · ca DO     — du lieu hong, cong PHAI do
     · ca RONG   — ⛔ khong do duoc gi, cong PHAI do *(⛔ khong duoc xanh)*

⛔⛔ Ca RONG la ca quan trong nhat, va no co tien le that trong nha: hai cong
   `RUN_ATOMIC` xanh suot **hai thang** tren **28 vi pham**, vi chung loc
   `IS NOT NULL` tren chinh cot chung canh ⇒ **chua tung co kha nang do**.
"""
from __future__ import annotations

import pytest

from fls.kiem import nguon_song as ns

SAU = dict.fromkeys(ns.SAU_TRUONG, 0)


# ── L1 ─────────────────────────────────────────────────────────────────────
def test_l1_xanh():
    kq = ns.l1_ban_khai_du_6({"R | A": dict(SAU), "R | B": dict(SAU)})
    assert kq.xanh and kq.da_do == 2


def test_l1_DO_khi_thieu_mot_truong():
    thieu = {k: v for k, v in SAU.items() if k != "Reference number"}
    kq = ns.l1_ban_khai_du_6({"R | A": dict(SAU), "R | B": thieu})
    assert not kq.xanh
    assert "Reference number" in kq.thong_diep


def test_l1_DO_khi_rong():
    assert not ns.l1_ban_khai_du_6({}).xanh


# ── L2 ─────────────────────────────────────────────────────────────────────
def test_l2_xanh_va_sheet_rong_KHONG_phai_loi():
    # `R | C` rong ca hai dau = tai khoan da mo ma chua dung ⇒ ⛔ khong phai loi
    kq = ns.l2_nhap_bang_gop({"R | A": 10, "R | B": 5, "R | C": 0},
                             {"R | A": 10, "R | B": 5})
    assert kq.xanh and kq.da_do == 2


def test_l2_DO_khi_gop_thieu_dong():
    kq = ns.l2_nhap_bang_gop({"R | A": 10}, {"R | A": 9})
    assert not kq.xanh and "nhap 10/gop 9" in kq.thong_diep


def test_l2_DO_khi_gop_KHONG_he_co_tai_khoan():
    kq = ns.l2_nhap_bang_gop({"R | A": 10}, {})
    assert not kq.xanh


def test_l2_DO_khi_rong():
    assert not ns.l2_nhap_bang_gop({"R | C": 0}, {}).xanh


# ── L3 ─────────────────────────────────────────────────────────────────────
def test_l3_xanh():
    assert ns.l3_xuat_xu_hop_le({"R | A": 3}, {"R | A", "R | B"}).xanh


def test_l3_DO_khi_co_xuat_xu_la():
    kq = ns.l3_xuat_xu_hop_le({"R | A": 3, "R | LA": 1}, {"R | A"})
    assert not kq.xanh and "R | LA" in kq.thong_diep


def test_l3_DO_khi_rong():
    assert not ns.l3_xuat_xu_hop_le({}, {"R | A"}).xanh


# ── L4 ─────────────────────────────────────────────────────────────────────
def test_l4_xanh():
    assert ns.l4_khoa_khong_mat_vi_kieu(3412, 3412, 10194).xanh


def test_l4_DO_khi_mat_vi_kieu():
    # dung con so THAT cua ban dau `Đ4-a` truoc khi doc tho: 1.468 dong
    kq = ns.l4_khoa_khong_mat_vi_kieu(3412, 3412 - 1468, 10194)
    assert not kq.xanh and "1468" in kq.thong_diep


def test_l4_DO_khi_rong():
    assert not ns.l4_khoa_khong_mat_vi_kieu(0, 0, 0).xanh


# ── L5 ─────────────────────────────────────────────────────────────────────
def test_l5_xanh_bui_dau_phay_dong_KHONG_phai_lech():
    # `1.52587890625e-05` = 2^-16, sinh tu phep nhan ty gia — ⛔ khong phai tien
    kq = ns.l5_lech_trong_dung_sai(
        {"a": 0.0, "b": 1.52587890625e-05, "c": -7.6e-06, "d": 302187656.0},
        bo_qua="d")
    assert kq.xanh and kq.da_do == 3


def test_l5_DO_khi_mot_muc_vuot():
    kq = ns.l5_lech_trong_dung_sai({"a": 0.0, "b": -9527063847.0, "c": 0.0})
    assert not kq.xanh and "-9,527,063,847" in kq.thong_diep


def test_l5_DO_khi_bo_qua_het_sach():
    assert not ns.l5_lech_trong_dung_sai({"a": 0.0}, bo_qua="a").xanh


# ── L6 ─────────────────────────────────────────────────────────────────────
def test_l6_xanh():
    kq = ns.l6_num_la_thu_tu(["FT1", "FT2", "FT1", "FT1"], [1, 1, 2, 3])
    assert kq.xanh and kq.da_do == 4


def test_l6_DO_khi_thu_tu_sai():
    kq = ns.l6_num_la_thu_tu(["FT1", "FT1"], [1, 1])
    assert not kq.xanh and "ghi 1, phai 2" in kq.thong_diep


def test_l6_bo_qua_o_TRONG_chu_khong_coi_la_dung():
    # o `Num` trong thi ⛔ khong tinh — nhung neu **moi** o deu trong thi
    # ⛔ khong do duoc gi ⇒ phai DO
    assert not ns.l6_num_la_thu_tu(["FT1", "FT2"], ["", ""]).xanh


def test_l6_DO_khi_rong():
    assert not ns.l6_num_la_thu_tu([], []).xanh


# ── L7 ─────────────────────────────────────────────────────────────────────
def test_l7_xanh():
    assert ns.l7_cau_bang_ban_goc(8338, 8338).xanh


@pytest.mark.parametrize("n_cau", [8340, 8336])
def test_l7_DO_khi_lech_ca_HAI_chieu(n_cau):
    """⛔ Cau **thua** dong cung dang ngo y het cau **thieu** dong: ca hai deu
    nghia la phep doi khuon ⛔ khong con la anh mot-doi-mot."""
    assert not ns.l7_cau_bang_ban_goc(8338, n_cau).xanh


def test_l7_DO_khi_rong():
    assert not ns.l7_cau_bang_ban_goc(0, 0).xanh


# ── luat chung ─────────────────────────────────────────────────────────────
def test_MOI_luat_deu_DO_khi_do_duoc_0_thu():
    """⛔⛔ Xanh tren tap RONG la **chua do**, ⛔ khong phai **dat**."""
    rong = [
        ns.l1_ban_khai_du_6({}),
        ns.l2_nhap_bang_gop({}, {}),
        ns.l3_xuat_xu_hop_le({}, set()),
        ns.l4_khoa_khong_mat_vi_kieu(0, 0, 0),
        ns.l5_lech_trong_dung_sai({}),
        ns.l8_co_doi_soat({}, {}),
        ns.l9_danh_muc_khop_sheet({}, set()),
        ns.l6_num_la_thu_tu([], []),
        ns.l7_cau_bang_ban_goc(0, 0),
    ]
    assert len(rong) == 9
    for kq in rong:
        assert not kq.xanh, kq.ten
        assert kq.da_do == 0, kq.ten


# ── L8 ─────────────────────────────────────────────────────────────────────
ACT = {"a": "Active", "b": "Active", "c": "Closed"}


def test_l8_xanh_va_BO_QUA_tai_khoan_da_dong():
    kq = ns.l8_co_doi_soat({"a": True, "b": True, "c": False}, ACT)
    assert kq.xanh and kq.da_do == 2      # `c` Closed ⇒ ⛔ khong xet


def test_l8_DO_khi_mot_tai_khoan_Active_lech():
    kq = ns.l8_co_doi_soat({"a": True, "b": False, "c": True}, ACT)
    assert not kq.xanh and "b" in kq.thong_diep


def test_l8_O_TRONG_tren_tai_khoan_Active_la_DO_chu_khong_phai_bo_qua():
    """⛔ Phep kiem ⛔ khong chay thi ⛔ khong duoc coi la dat."""
    kq = ns.l8_co_doi_soat({"a": True, "b": None, "c": True}, ACT)
    assert not kq.xanh


def test_l8_DO_khi_khong_co_tai_khoan_Active_nao():
    assert not ns.l8_co_doi_soat({"c": True}, {"c": "Closed"}).xanh


# ── L9 ─────────────────────────────────────────────────────────────────────
def test_l9_xanh():
    kq = ns.l9_danh_muc_khop_sheet({"a": "R | A", "b": "R | B"},
                                   {"R | A", "R | B", "R | C"})
    assert kq.xanh and kq.da_do == 2


def test_l9_DO_khi_danh_muc_tro_toi_sheet_KHONG_ton_tai():
    kq = ns.l9_danh_muc_khop_sheet({"a": "R | A", "b": "R | MA"}, {"R | A"})
    assert not kq.xanh and "R | MA" in kq.thong_diep


def test_l9_DO_khi_rong():
    assert not ns.l9_danh_muc_khop_sheet({}, {"R | A"}).xanh
