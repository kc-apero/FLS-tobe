# -*- coding: utf-8 -*-
"""Phep thu cho `tools/dong_bo_so_song.py` — cong cu SOAN so cho tai lieu.

⛔ Cac bai nay ⛔ khong doc bo tai lieu that: chung ghim **phep cat chuoi**,
va do dung la cho da hong.
"""
from __future__ import annotations

import re

from tools.dong_bo_so_song import _thay_theo_nhom


def test_thay_DUNG_NHOM_giu_nguyen_moi_ky_tu_ngoai_nhom():
    """⛔ Phep thay phai la phau thuat: dau cau, dam, khoang trang **nguyen**."""
    s = "ghi **1594 phép thử**, **20.403 dòng** `fls/` cuoi cau"
    k = re.search(r"\*\*(\d+) phép thử\*\*, \*\*([\d.]+) dòng\*\*", s)
    assert _thay_theo_nhom(k, ("1610", "21.269")) == \
        "**1610 phép thử**, **21.269 dòng**"


def test_SPAN_la_vi_tri_trong_CA_TEP_chu_KHONG_trong_chuoi_khop():
    """⛔⛔⛔ **Ghim dung loi toi mac 11/09.**

    `re.Match.span(i)` tra vi tri trong **CA VAN BAN**, ⛔ khong phai trong
    `group(0)`. Ban dau toi cat `group(0)` bang cac `span` tuyet doi ay —
    va **ban xem truoc ⛔ KHONG HE lo ra**, vi no chi in `nhom i: cu → moi`,
    tuc in **y dinh** chu ⛔ khong in **ket qua**.

    ⇒ Bai nay dat cho khop **that sau** trong van ban *(offset lon)*, la ca
      duy nhat lam lo phep tru `khop.start()`. Neu ai do bo phep tru ay, chuoi
      tra ve se **dai ra** va ⛔ khong con la mot phep thay.
    """
    dem = "x" * 5000
    s = dem + "co **10.030 dòng sổ** o day"
    k = re.search(r"\*\*([\d.]+) dòng sổ\*\*", s)
    assert k.start() > 5000, "ca thu phai co offset LON thi moi lo loi"
    ra = _thay_theo_nhom(k, ("8.387",))
    assert ra == "**8.387 dòng sổ**", ra
    assert len(ra) < 30, "⛔ chuoi dai ra ⇒ dang cat bang `span` tuyet doi"


def test_NHIEU_NHOM_thay_tu_PHAI_sang_TRAI():
    """⛔ Thay tu trai lam moi `span` phia sau lech di so ky tu vua doi.

    Ca nay co chu y: nhom 1 **dai ra** *(1 → 4 ky tu)*, nen mot ban thay tu
    trai se ghi nhom 2 **nham cho**.
    """
    s = "co **5 dòng** va **2.745 mối nối** het"
    k = re.search(r"\*\*(\d+) dòng\*\* va \*\*([\d.]+) mối nối\*\*", s)
    assert _thay_theo_nhom(k, ("8.387", "2.262")) == \
        "**8.387 dòng** va **2.262 mối nối**"


def test_KHONG_doi_thi_tra_Y_NGUYEN():
    s = "**1610 phép thử**"
    k = re.search(r"\*\*(\d+) phép thử\*\*", s)
    assert _thay_theo_nhom(k, ("1610",)) == s
