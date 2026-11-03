# -*- coding: utf-8 -*-
"""Phep thu cho cong so song (`tools/kiem_so_song.py`) — cong chung #13.

⛔ Cac bai nay kiem **phan LUAT** (phep so thuan) va **phan KHAI** (danh sach
muc), ⛔ KHONG kiem viec do that: do that can kho PostgreSQL + `git` + bo tai
lieu nam ngoai repo. Khai ra chu ⛔ khong de nguoi doc tu suy.

Cai chung chan:
  · mot mau khop 0 lan (van doi chu, mau vo) ma cong van XANH
  · mot mau khop nhieu lan ma cong tuong minh dang so voi dung mot cho
  · mot muc khai thieu/thua gia tri so voi so nhom cua mau
"""
from __future__ import annotations

import collections
import re

import pytest

from tools.kiem_so_song import Muc, kiem_mot, vn


# ─────────────────────────────────────────────────────── luat ⓐ: DUNG mot lan
def test_KHOP_DUNG_MOT_LAN_va_dung_so_thi_DAT():
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    assert kiem_mot("... `pg_verify` khớp 15 bảng/view ...", m) == []


def test_KHOP_dung_mot_lan_nhung_LECH_so_thi_DO():
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    loi = kiem_mot("khớp 14 bảng/view", m)
    assert len(loi) == 1
    assert "`14`" in loi[0] and "`15`" in loi[0] and "LỆCH" in loi[0]


def test_KHOP_KHONG_LAN_NAO_thi_DO_chu_KHONG_xanh():
    """⛔ Day la nhanh de bi bo qua nhat: mau vo thi 'khong thay loi'."""
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    loi = kiem_mot("cau van da doi, khong con chu nao khop", m)
    assert len(loi) == 1
    assert "khop 0 lan" in loi[0] and "khong do duoc" in loi[0]


def test_KHOP_HAI_LAN_thi_DO_vi_khong_biet_dang_so_voi_cho_nao():
    m = Muc("thu", "f.md", r"\*\*(\d+) kept\*\*", ("7",))
    loi = kiem_mot("**7 kept** ... roi noi khac lai **7 kept**", m)
    assert len(loi) == 1 and "khop 2 lan" in loi[0]


def test_MAU_NHIEU_NHOM_bao_dung_nhom_nao_lech():
    m = Muc("thu", "f.md", r"\*\*([\d.]+) mối nối\*\* \*\(([\d.]+) dòng\)\*",
            ("2.745", "2.427"))
    loi = kiem_mot("**2.745 mối nối** *(2.336 dòng)*", m)
    assert len(loi) == 1 and "nhom 2" in loi[0]
    assert kiem_mot("**2.745 mối nối** *(2.427 dòng)*", m) == []


def test_KHAI_THIEU_GIA_TRI_so_voi_so_nhom_thi_DO():
    """Mot muc khai 1 gia tri cho mau 2 nhom = loi cua NGUOI khai, phai DO."""
    m = Muc("thu", "f.md", r"(\d+) va (\d+)", ("1",))
    loi = kiem_mot("1 va 2", m)
    assert len(loi) == 1 and "nhom" in loi[0]


# ─────────────────────────────────────────────────────── dinh dang so kieu VN
@pytest.mark.parametrize("n,cho", [(0, "0"), (19, "19"), (1200, "1.200"),
                                   (10030, "10.030"), (1234567, "1.234.567")])
def test_dinh_dang_so_kieu_tai_lieu(n, cho):
    assert vn(n) == cho


# ─────────────────────────────────────────────────────── phan KHAI co lanh manh
def test_MOI_MAU_DICH_DUOC_va_so_nhom_khop_so_gia_tri_khai():
    """⛔ Khong chay duoc phep do that thi it nhat phai biet DANH SACH lanh.

    Bai nay chan mot lo that: sua mau ma quen sua so gia tri khai (hay nguoc
    lai) — luc do cong se DO voi ly do 'so nhom' tren MOI lan chay, tuc la
    khong con canh duoc gi.
    """
    from tools.kiem_so_song import khai

    # ⛔ Danh sach khoa CO Y ⛔ khong go tay: go tay thi bai nay do moi lan
    # cong them mot con so do duoc (da xay ra ngay trong buoi dung no —
    # `test_ngoai`). `defaultdict` de bai nay canh dung thu no sinh ra de canh:
    # mau vs so gia tri khai. Khoa go sai se no `KeyError` o lan chay THAT,
    # to va ngay lap tuc.
    may = collections.defaultdict(lambda: "0")

    class _Gia:
        """Tra version gia — bai nay ⛔ khong doc bo tai lieu that."""

        def __truediv__(self, _):
            return self

        def exists(self):
            return True

        def read_text(self, **_):
            return "**Version:** v9.9"

        # ⭐ Them 2026-08-28: `khai()` nay con DEM chinh bo tai lieu (so file
        # `.md` + so hien vat — xem `dem_bo_tai_lieu`). Bai nay ⛔ khong doc bo
        # that, nen tra so gia; no chi kiem MAU vs SO NHOM, ⛔ khong kiem gia tri.
        def is_dir(self):
            return True

        def rglob(self, _):
            return iter(range(99))

        def iterdir(self):
            return iter(range(9))

    muc = khai(may, _Gia())
    assert len(muc) >= 25, "danh sach phep so bi teo di"
    for m in muc:
        r = re.compile(m.mau)              # dich duoc, khong thi nem loi ngay
        assert r.groups == len(m.gia), (
            f"{m.ten}: mau co {r.groups} nhom nhung khai {len(m.gia)} gia tri")
        assert m.ten and m.file
