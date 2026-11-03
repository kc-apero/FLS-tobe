"""Thuoc chuan phai TU SOI: dong nao khong tu nhat quan thi LOAI (DoD 5.6 ②).

Va R-ORA-07a: o `#N/A` o nua mapping la CAU TRA LOI ("chua ghep"), khong phai loi.
"""
from __future__ import annotations

from fls.oracle.tu_soi import la_o_loi, soi, soi_mot_dong

# Mot dong tu nhat quan: Final = f(Classifying, MID) o ca 7 khoi.
# Thu tu bo bon: (Classifying, Manual input, MID, Final)
DONG_TOT = {
    "hd": ("OGA | GAC - Other", "Input here", "OGA | GAC - Other",
           "OGA | GAC - Other"),
    "pay_type": ("Thanh toan (Regular)", "", "Thanh toan (Regular)",
                 "Thanh toan (Regular)"),
    "cdt1": ("SHQ1 | Headquarters1", "", "SHQ1 | Headquarters1",
             "SHQ1 | Headquarters1"),
    "svc_start": ("Need to manual input", "202603", "202603", "202603"),
    "svc_end": ("Need to manual input", "202603", "202603", "202603"),
    "id_payee": ("VD0", "", "VD0", "VD0"),
    "invoice": ("Need to manual input", "Input here", "No hoa don", "No hoa don"),
}


def test_dong_tu_nhat_quan_thi_giu():
    kq = soi_mot_dong(DONG_TOT)
    assert kq.giu and kq.ly_do == ""


def test_dong_bi_go_giua_hai_lan_doc_thi_LOAI_va_co_ly_do_co_ten():
    xau = dict(DONG_TOT, invoice=("Need to manual input", "Input here",
                                  "No hoa don", "MOT GIA TRI KHAC"))
    kq = soi_mot_dong(xau)
    assert not kq.giu
    assert "invoice" in kq.ly_do


def test_thieu_mot_khoi_thi_LOAI_chu_khong_lang_le_bo_qua():
    thieu = {k: v for k, v in DONG_TOT.items() if k != "cdt1"}
    kq = soi_mot_dong(thieu)
    assert not kq.giu and "cdt1" in kq.ly_do


def test_soi_tach_hai_duong_va_tong_bao_toan():
    xau = dict(DONG_TOT, hd=("A", "", "A", "B"))
    giu, loai = soi([DONG_TOT, xau, DONG_TOT])
    assert len(giu) == 2 and len(loai) == 1
    assert len(giu) + len(loai) == 3          # khong dong nao roi im lang
    assert loai[0][1].strip()                 # co ly do bang chu


def test_la_o_loi_nhan_dung_o_loi_excel():
    for v in ("#N/A", "#N/A (Did not find value)", "#REF!", "#VALUE!"):
        assert la_o_loi(v)
    for v in (None, "", "OGA | GAC - Other", "202603", 0, "No hoa don"):
        assert not la_o_loi(v)


def test_R_ORA_07a_o_loi_khong_lam_dong_bi_loai():
    """`#N/A` la cau tra loi, KHONG phai co so de loai dong khoi thuoc chuan."""
    na = dict(DONG_TOT, svc_start=("#N/A", "", "#N/A", "#N/A"))
    assert soi_mot_dong(na).giu
