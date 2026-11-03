# -*- coding: utf-8 -*-
"""Phep thu cho `tools/tien_do.py::dem_dong` — *"dem HET vat lieu"*.

⛔⛔⛔ **Vi sao tep nay ton tai.** `dem_dong` ban dau chi `glob("*.py")` o
**dung mot tang**, nen module `web` — **bon man hinh**, viet bang `.js` trong
`fls/web/tep/` — bi dem la **265 dong** *(chi `phuc_vu.py`)* thay vi **hon
6.000**. Bang tien do vi the in ra `web  265 dong  ·  333 test`: **nhieu bai
thu hon dong ma**, mot dieu vo ly nam trong tai lieu **da duoc cong so song
GHIM** — nen cong ⛔ khong bat, no **bao ve** con so sai suot 7 ngay.

★ Luat cho moi phep dem sau: **mot phep dem phai phu HET vat lieu cua thu no
  dem**. `fls.web` ⛔ khong phai *"mot tep Python"*.
"""
from __future__ import annotations

from tools.tien_do import DUOI_MA, dem_dong


def test_WEB_phai_gom_ca_MAN_HINH_khong_chi_tep_python():
    """⛔ Bai nay DO tren ban `glob("*.py")` mot tang: no tra ~265."""
    dong, nfile, _ = dem_dong("web")
    # ⭐ Nguong ⛔ khong phai con so chinh xac *(ma con doi)* — no la con so
    #   **⛔ khong the dat duoc** neu phep dem bo qua `fls/web/tep/`.
    assert dong > 3000, f"web chi {dong} dong ⇒ phep dem dang bo qua `tep/`"
    assert nfile >= 10, f"web chi {nfile} tep ⇒ ⛔ chua de quy vao `tep/`"


def test_MODULE_THUAN_PYTHON_khong_bi_doi():
    """⭐ Phep sua ⛔ khong duoc lam phong cac module ⛔ khong co tep JS.

    Neu `DUOI_MA` lo them `.json`/`.md` thi `db` *(co tep khai)* se phong len
    trong im lang — va mot con so phong len van **khop** sau khi
    `va_so_song.py` va, dung nhu `265` da khop suot 7 ngay.
    """
    for ma, tran in (("contract", 200), ("canon", 600), ("xuat", 600)):
        dong, _, _ = dem_dong(ma)
        assert 0 < dong < tran, f"{ma} = {dong} dong, vuot tran {tran}"


def test_DUOI_MA_chi_gom_MA_khong_gom_DU_LIEU():
    assert {".py", ".js"} <= DUOI_MA
    # ⛔ `.json` la du lieu, `.md` la van ban — dem chung vao *"dong ma"* lam
    #   con so phong len vo nghia.
    assert not ({".json", ".md", ".csv", ".xlsx"} & DUOI_MA)


def test_MODULE_KHONG_TON_TAI_tra_ve_KHONG_chu_khong_NO():
    assert dem_dong("khong_he_co_module_nay") == (0, 0, 0)


def test_KHONG_dem_pycache():
    """`__pycache__` chua `.py` ⛔ khong phai ma nguoi viet.

    ⚠ `rglob("*")` de quy nen no **se** gap `__pycache__` — va cac tep `.pyc`
      thi ⛔ khong co duoi `.py`, nhung mot ngay nao do ai do them `.py` sinh
      ra vao do thi phep dem se **im lang phong len**.
    """
    dong, nfile, _ = dem_dong("db")
    dong2, nfile2, _ = dem_dong("db")
    assert (dong, nfile) == (dong2, nfile2)
    assert nfile < 40, f"db {nfile} tep — nghi ⛔ dang dem ca tep sinh ra"
