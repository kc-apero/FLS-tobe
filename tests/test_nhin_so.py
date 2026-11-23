# -*- coding: utf-8 -*-
"""Phep thu cho cua so DOC (`tools/nhin_so.py`).

⛔ Cac bai nay ⛔ khong cham kho: chung ghim **hai tinh chat** ma mot cong cu
doc so tien that phai giu, va ca hai deu doc duoc tu ma nguon.
"""
from __future__ import annotations

import inspect

from tools import nhin_so


def test_dinh_dang_so_kieu_VN_cham_ngan_nghin_phay_thap_phan():
    assert nhin_so.vn(1234567.5) == "1.234.567,50"
    assert nhin_so.vn(0) == "0,00"
    assert nhin_so.vn(None) == "—"


def test_MO_KET_NOI_bang_duong_CHI_DOC_chu_khong_duong_ghi():
    """⛔⛔ **Day la tinh chat dat nhat cua tep nay.**

    Mot cong cu *"chi de nhin"* mo bang `psycopg.connect(dsn_that())` thi
    ⛔ khong co gi chan mot cau `UPDATE` go nham vao do — va `fls_itl` la
    **append-only** (`INV-I08`). `noi_chi_doc()` bat PostgreSQL **tu tu choi**
    moi phep ghi ⇒ phep chan nam o **tang duoi**, ⛔ khong o ky luat nguoi viet.

    ⇒ Bai nay do **ma nguon**, ⛔ khong do hanh vi: neu ai do doi sang
      `psycopg.connect` thi bai do ngay, ⛔ khong doi den luc co nguoi go nham.
    """
    ma = inspect.getsource(nhin_so.main)
    assert "noi_chi_doc(" in ma
    assert "psycopg.connect" not in inspect.getsource(nhin_so)


def test_14_TRUONG_contract_khai_du_va_KHONG_trung():
    """⛔ Khai thieu mot truong = mot cot rong **⛔ khong ai thay**."""
    assert len(nhin_so.CONTRACT) == 14
    assert len(set(nhin_so.CONTRACT)) == 14
