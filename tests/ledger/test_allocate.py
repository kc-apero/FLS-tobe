# -*- coding: utf-8 -*-
"""Vung ALLOCATE: phep suy phai bam DUNG ba cong thuc owner dua 2026-08-28.

⛔ Cac bai nay ⛔ KHONG kiem "cai gi dep" — chung kiem **parity voi Sheets**.
Cho nao Sheets lam mot chuyen la lung thi bai test giu dung chuyen la lung ay,
va noi ro trong docstring, ⛔ khong "chua cho dep" roi lech thuoc chuan.
"""
from __future__ import annotations

from fls.ledger.allocate import (CO_CAN_PHAN_BO, CO_KHONG_CAN, KHONG_TRA_DUOC,
                                 suy_allocate)


def test_CFA1_la_BAN_SAO_cua_cdt1__khong_phai_mot_gia_tri_doc_lap():
    """`AU = ArrayFormula(AD7:AD)` — `AD` = `Chu du toan · Final` = `cdt1`."""
    for cdt1 in ("AHD", "HQ1", "", "COC"):
        assert suy_allocate(cdt1, "HD1", {"need_cfa2": "", "method_cfa2": "x"}).cfa1 == cdt1


def test_CO_can_phan_bo__thi_CFA2_hien_CO_va_co_duoc_TACH_RA():
    r = suy_allocate("AHD", "HD1",
                     {"need_cfa2": CO_CAN_PHAN_BO, "method_cfa2": "By NOEM"})
    assert r.cfa2 == CO_CAN_PHAN_BO
    assert r.can_phan_bo is True, "⛔ co phai TACH ra khoi gia tri, ⛔ khong de nguoi doc tu doan"
    assert r.method == "By NOEM"


def test_KHONG_can_phan_bo__thi_CFA2_ROI_VE_CFA1():
    """Cong thuc: `if(... = "Need to Allocate to CFA2", ..., AU7:AU)`."""
    r = suy_allocate("AHD", "HD1", {"need_cfa2": "", "method_cfa2": ""})
    assert r.cfa2 == "AHD" and r.can_phan_bo is False


def test_BAY_1__Sheets_so_chuoi_KHONG_phan_biet_hoa_thuong():
    """⚠ `=` cua Sheets ⛔ khong phan biet hoa thuong; Python thi co.

    Neu `Mapping Master` go `"need to allocate to cfa2"` thi tren sheet o do
    **VAN** ra co. Mot ban Python so `==` se cho ra **khac sheet** ⇒ parity do.
    """
    r = suy_allocate("AHD", "HD1",
                     {"need_cfa2": "need to allocate to CFA2", "method_cfa2": "x"})
    assert r.can_phan_bo is True and r.cfa2 == CO_CAN_PHAN_BO


def test_BAY_2__o_RONG_that_cho_ra_0_chu_KHONG_phai_No_need():
    """⚠⚠ `VLOOKUP` tra ve o RONG thi Sheets cho **`0`**, va `0 <> ""` la DUNG.

    ⇒ `"No need"` **chi** xuat hien khi o do chua mot **chuoi rong**, ⛔ khong
    phai khi o do trong. Bai nay khoa ca hai nhanh de dung ai "don" mot trong
    hai roi lam lech parity.
    """
    assert suy_allocate("AHD", "HD1",
                        {"need_cfa2": "", "method_cfa2": None}).method == "0"
    assert suy_allocate("AHD", "HD1",
                        {"need_cfa2": "", "method_cfa2": ""}).method == CO_KHONG_CAN


def test_KHONG_TRA_DUOC_thi_CA_HAI_o_la_NA__khong_bia_va_khong_roi_ve_CFA1():
    """`VLOOKUP(...,FALSE)` khong thay khoa ⇒ `#N/A`, ⛔ khong phai rong.

    ⛔ Va ⛔ KHONG duoc roi ve `AU`: cong thuc chi roi ve `AU` khi VLOOKUP
    **thanh cong** ma tra ve mot gia tri khac chuoi co. Lan giua hai chuyen do
    la bien *"khong tra duoc"* thanh *"da tra duoc va bang CDT1"*.
    """
    r = suy_allocate("AHD", "HD-LA", None)
    assert r.cfa2 == KHONG_TRA_DUOC and r.method == KHONG_TRA_DUOC
    assert r.khong_tra_duoc is True and r.cfa1 == "AHD"
    assert r.can_phan_bo is False


def test_hd_RONG_thi_cung_KHONG_TRA_DUOC():
    for hd in (None, "", "   "):
        r = suy_allocate("AHD", hd, {"need_cfa2": CO_CAN_PHAN_BO, "method_cfa2": "x"})
        assert r.khong_tra_duoc is True, f"hd={hd!r}"


def test_nhan_ca_dict_LAN_doi_tuong__vi_kho_tra_ve_doi_tuong():
    class Dong:
        need_cfa2 = CO_CAN_PHAN_BO
        method_cfa2 = "By Headcount"

    r = suy_allocate("AHD", "HD1", Dong())
    assert r.cfa2 == CO_CAN_PHAN_BO and r.method == "By Headcount"


def test_BA_CONG_THUC_duoc_chep_NGUYEN_VAN_trong_docstring():
    """⛔ Cong nay chan viec dien giai lai cong thuc bang loi roi lech dan.

    Phep suy chi dung khi con so trong `Mapping Master` va cong thuc tren sheet
    con dung nhu the. Nen NGUYEN VAN phai nam trong ma nguon, ⛔ khong chi nam
    trong mot tin nhan.
    """
    import fls.ledger.allocate as m

    d = m.__doc__ or ""
    for manh in ("ArrayFormula(AD7:AD)",
                 "'[Importrange]Mapping Master'!K:K",
                 "'[Importrange]Mapping Master'!L:L",
                 '"Need to Allocate to CFA2"',
                 '"No need"'):
        assert manh in d, f"docstring thieu nguyen van: {manh}"
