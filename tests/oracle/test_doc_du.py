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


# Số đo trên nguồn SỐNG 23–24/11 (`WO-352`, quyết chủ 23/11 "CDT1 đo lại sàn"):
# theo HÀNG = theo CỘT ở cả 6 cột. Luật đặt sàn GIỮ NGUYÊN như 27/08 = làm tròn XUỐNG hàng trăm.
DO_SONG_23_11 = {"S · Budget Code (hd)": 3422, "H · Payment Type": 3549,
                 "T · CDT1": 3056, "AB · svc_start": 2525,
                 "AC · svc_end": 2518, "Y · ID Payee": 463}
DO_CU_27_08 = {"S · Budget Code (hd)": 3344, "H · Payment Type": 3344,
               "T · CDT1": 3339, "AB · svc_start": 2370,
               "AC · svc_end": 2364, "Y · ID Payee": 430}


def test_nguong_san_phu_sau_cot_then_chot_va_deu_duoi_so_da_do():
    """⛔ Nguong la SAN, khong phai gia tri dung. SAN phai THAP HON so da do,
    khong thi cong do ngay lan chay dau. So do hien hanh = nguon SONG 23/11."""
    assert set(NGUONG_SAN) == set(DO_SONG_23_11) == set(DO_CU_27_08)
    for k, san in NGUONG_SAN.items():
        assert 0 < san <= DO_SONG_23_11[k], f"{k}: san {san} vs do {DO_SONG_23_11[k]}"


def test_nguong_san_DUNG_LUAT_lam_tron_XUONG_hang_tram_cua_so_do_23_11():
    """Luat 27/08 (3.344 -> 3.300 · 2.370 -> 2.300 · 430 -> 400) GIU NGUYEN:
    san = (so do // 100) * 100, ⛔ doi luat lam tron."""
    for k, do in DO_SONG_23_11.items():
        assert NGUONG_SAN[k] == (do // 100) * 100, k
    assert NGUONG_SAN == {"S · Budget Code (hd)": 3_400, "H · Payment Type": 3_500,
                          "T · CDT1": 3_000, "AB · svc_start": 2_500,
                          "AC · svc_end": 2_500, "Y · ID Payee": 400}


def test_cot_GIAM_so_voi_27_08_la_dung_mot__CDT1_giam_283():
    """⛔ Khong im lang: CDT1 3.339 -> 3.056 (-283) trong khi nguon lon dan.
    Bai nay ghim DANH SACH cot giam — them cot giam thu hai phai doi bai nay."""
    giam = {k: DO_SONG_23_11[k] - DO_CU_27_08[k] for k in DO_SONG_23_11
            if DO_SONG_23_11[k] < DO_CU_27_08[k]}
    assert giam == {"T · CDT1": -283}


def test_CONG_DO_HAI_CHIEU_voi_san_moi__bang_san_DAT__san_tru_1_DO_co_ten_cot():
    for k, san in NGUONG_SAN.items():
        du = [DemCot(c, NGUONG_SAN[c], NGUONG_SAN[c], NGUONG_SAN[c]) for c in NGUONG_SAN]
        assert danh_gia(du, dong_doc=10_100, dong_toi_thieu=9_000).dat, k
        thieu = [DemCot(c, NGUONG_SAN[c] - (c == k), NGUONG_SAN[c] - (c == k),
                        NGUONG_SAN[c]) for c in NGUONG_SAN]
        px = danh_gia(thieu, dong_doc=10_100, dong_toi_thieu=9_000)
        assert not px.dat, k
        assert len(px.ly_do) == 1 and f"cot {k}:" in px.ly_do[0] \
            and f"duoi nguong san {san}" in px.ly_do[0], (k, px.ly_do)


def test_so_do_song_23_11_QUA_cong_voi_san_moi__va_CDT1_3056_khong_con_bi_chan():
    px = danh_gia([DemCot(k, v, v, NGUONG_SAN[k]) for k, v in DO_SONG_23_11.items()],
                  dong_doc=14_265, dong_toi_thieu=9_000)
    assert px.dat, px.ly_do
