"""Cong doc-du: mot lat HOP LE van co the THIEU GIA TRI.

Bai dau tien khoa dung cai vua xay ra: lan nap ghi 257 gia tri `svc_start` it
hon chinh du lieu do, va **khong cai gi bao gi**.
"""
from __future__ import annotations

from fls.oracle.doc_du import NGUONG_SAN, DemCot, danh_gia


def test_DUNG_CAI_VUA_XAY_RA__257_o_mat_im_lang_phai_lam_cong_DO():
    """★★ Bai thu quan trong nhat cua module.

    Lat doc hop le: dung so cot, dung so dong, 0 loi HTTP. Nhung cot `AB` doc
    theo HANG ra 2.111 o co gia tri, doc theo COT ra 2.370. Truoc khi co cong
    nay, nhung o do **di vao kho thanh NULL** ma khong ai biet.

    ⚠ Hai con so canh nhau, dung ca hai cho dung cho: **257** o bi mat TRONG KHO
    (payload tinh duoc 2.368, kho co 2.111), va **259** la lech giua hai lan doc
    (2.370 - 2.111) — hai dong trong so do bi `validate` loai truoc khi vao kho
    nen khong tinh vao 257.
    """
    px = danh_gia([DemCot("AB · svc_start", lan_lat=2111, lan_cot=2370,
                          toi_thieu=2300)],
                  dong_doc=10_100, dong_toi_thieu=9_000)
    assert not px.dat
    assert any("lech -259" in x for x in px.ly_do)
    assert any("duoi nguong san" in x for x in px.ly_do)
    assert "khong ghi" in px.bao()


def test_hai_lan_doc_KHOP_thi_DAT():
    px = danh_gia([DemCot("AB · svc_start", 2370, 2370, 2300),
                   DemCot("S · Budget Code (hd)", 3344, 3344, 3300)],
                  dong_doc=10_100, dong_toi_thieu=9_000)
    assert px.dat and px.ly_do == ()
    assert "10100 dong" in px.bao() and "AB · svc_start=2370" in px.bao()


def test_KHONG_DO_COT_NAO_thi_KHONG_DAT__cong_phai_do_duoc_gi():
    """⛔ Mac dinh KHONG DAT. Mot cong khong do gi thi khong duoc bao DAT — day
    la bai hoc tu lan cong parity NOI DOI (doc 0 dong, in "khop 100%").
    """
    px = danh_gia([], dong_doc=10_100, dong_toi_thieu=9_000)
    assert not px.dat
    assert "chua do gi" in px.ly_do[0]


def test_doc_it_dong_thi_KHONG_DAT_du_hai_lan_doc_khop():
    """Hai lan doc cung THIEU giong nhau van phai bi chan boi nguong so dong."""
    px = danh_gia([DemCot("AB · svc_start", 0, 0)], dong_doc=0,
                  dong_toi_thieu=9_000)
    assert not px.dat
    assert any("chi doc 0 dong" in x for x in px.ly_do)


def test_hai_lan_doc_khop_nhung_TUT_DUOI_SAN_thi_KHONG_DAT():
    """Truong hop that: `IMPORTRANGE` lanh ca hai lan doc. Nguong san bat duoc."""
    px = danh_gia([DemCot("AB · svc_start", 12, 12, 2300)],
                  dong_doc=10_100, dong_toi_thieu=9_000)
    assert not px.dat and any("duoi nguong san 2300" in x for x in px.ly_do)


def test_moi_cot_lech_deu_duoc_KE_RA_rieng__khong_gop_thanh_mot_cau():
    px = danh_gia([DemCot("AB · svc_start", 1, 2370),
                   DemCot("AC · svc_end", 2, 2364)],
                  dong_doc=10_100, dong_toi_thieu=9_000)
    assert len(px.ly_do) == 2
    assert any("AB" in x for x in px.ly_do) and any("AC" in x for x in px.ly_do)


def test_nguong_san_phu_sau_cot_then_chot_va_deu_duoi_so_da_do():
    """⛔ Nguong la SAN, khong phai gia tri dung — nguon lon dan nen so chi tang.

    Va SAN phai THAP HON so da do, khong thi cong do ngay lan chay dau.
    """
    do_that = {"S · Budget Code (hd)": 3344, "H · Payment Type": 3344,
               "T · CDT1": 3339, "AB · svc_start": 2370,
               "AC · svc_end": 2364, "Y · ID Payee": 430}
    assert set(NGUONG_SAN) == set(do_that)
    for k, san in NGUONG_SAN.items():
        assert 0 < san <= do_that[k], f"{k}: san {san} vs do that {do_that[k]}"
