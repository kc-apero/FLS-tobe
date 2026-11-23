# -*- coding: utf-8 -*-
"""`tools/nhip_chup.py::khai_rong` — DEM **va** GOI TEN, cat co KHAI.

⛔⛔⛔ Bao cao nhip in `nguon_ra_0_dong: 14` suot tu 09/09 va ⛔ **khong ai
   hanh dong duoc** tren con so ay. Toi viet *"lan Bank chay duoc"* trong khi
   `4` sheet vua khai ra `0` dong — va `14` nam **ngay tren man hinh** luc
   toi viet cau ay. Mot con so dem noi *"co chuyen"*; mot danh sach noi *"di
   xem cai NAO"*.
"""
from __future__ import annotations

from tools.nhip_chup import CAT_TEN_RONG, khai_rong


def test_RONG_thi_khong_bao_gi():
    d = khai_rong([])
    assert d["nguon_ra_0_dong"] == 0
    assert d["ten_nguon_ra_0_dong"] == []
    assert d["con_nua"] == 0


def test_GOI_TEN_chu_khong_chi_DEM():
    d = khai_rong(["a", "b", "c"])
    assert d["nguon_ra_0_dong"] == 3
    assert d["ten_nguon_ra_0_dong"] == ["a", "b", "c"]
    assert d["con_nua"] == 0


def test_CAT_thi_con_so_DEM_van_DUNG():
    """⛔⛔ Mot danh sach bi cat trong im lang la cach bien `40` thanh `10`.

    ⇒ `nguon_ra_0_dong` **⛔ khong** duoc cat theo, va `con_nua` phai noi ro
      phan bi che.
    """
    ten = [f"n{i:02d}" for i in range(40)]
    d = khai_rong(ten)
    assert d["nguon_ra_0_dong"] == 40
    assert len(d["ten_nguon_ra_0_dong"]) == CAT_TEN_RONG
    assert d["con_nua"] == 40 - CAT_TEN_RONG
    # ⭐ Tong luon dung: phan hien + phan che = phan that
    assert len(d["ten_nguon_ra_0_dong"]) + d["con_nua"] == d["nguon_ra_0_dong"]


def test_DUNG_NGUONG_thi_KHONG_bao_con_nua():
    """⛔ `con_nua = 0` khi vua du — mot dong *"con 0 nua"* la mot dong lam
    nguoi doc tuong con thu gi o duoi."""
    d = khai_rong([f"n{i}" for i in range(CAT_TEN_RONG)])
    assert d["con_nua"] == 0
    assert len(d["ten_nguon_ra_0_dong"]) == CAT_TEN_RONG


def test_cat_1_van_dem_dung():
    d = khai_rong(["a", "b", "c"], cat=1)
    assert (d["nguon_ra_0_dong"], d["con_nua"]) == (3, 2)
