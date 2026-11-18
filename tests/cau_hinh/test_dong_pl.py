# -*- coding: utf-8 -*-
"""`C12-B1 · B2 · B3` — IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK
*(ISP 3.1.2 · Step 26 · `C12` · `WO-184`)*.

⭐ Giá trị HD là SỐ TỔNG HỢP *(⛔ số thật)*, tay tính ở từng bài. Cây = ảnh DT3 thật
   `atl_cay.json` *(74 nút)*, nạp qua `hd.doc_van_ban`.
⛔ `Đ3`: mọi phép đếm có mẫu số khác 0 *(7 dòng PL · 2 phép CHECK · vế trái ≠ 0)*.
⛔ `Đ5`: mỗi tên lỗi `PL_*` có một bài ép nó.
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from fls.cau_hinh import dong_pl, hd

GOC = Path(__file__).resolve().parents[2]
CAY = hd.doc_van_ban((GOC / "tests/fixture/cau_hinh/atl_cay.json")
                     .read_text(encoding="utf-8"), nguon="atl_cay.json")

# Tổng hợp, tay tính: PL2=1000−100=900 · PL3=900−(30+20+10)=840 · PL4=840−40=800 ·
# PL5=800−50=750 · PL6=750−(10+5+15+20)=700 · PL7=700−(30+20+10)=640 · PL8=640−40=600.
HD_CAN = {"GI": 1000, "OMC": 100, "API": 30, "SC": 20, "LC": 10, "PS": 40,
          "COM": 50, "MC": 10, "OTMC": 5, "DC": 15, "CSO": 20,
          "GAC": 30, "CDC": 20, "ITE": 10, "CIT": 40,
          # CHECK: NIS+INT+PIT+COM = 40+20+15+50 = 125 = CXA+GAH+DC+MC = 60+40+15+10
          "NIS": 40, "INT": 20, "PIT": 15, "CXA": 60, "GAH": 40, "NB": 0}
MONG_PL = {"PL2": 900, "PL3": 840, "PL4": 800, "PL5": 750, "PL6": 700,
           "PL7": 640, "PL8": 600}


# ── C12-B1 ───────────────────────────────────────────────────────────────────
def test_C12_B1_tinh_pl_dung_tay_tinh_ca_7_dong():
    ra = dong_pl.tinh_pl(HD_CAN)
    assert len(MONG_PL) == 7                       # Đ3: mẫu số ≠ 0
    assert ra == MONG_PL, ra


def test_C12_B1_pl2_don_le_la_GI_tru_OMC():
    v = {k: 0 for k in HD_CAN} | {"GI": 7, "OMC": 2}
    assert dong_pl.tinh_pl(v)["PL2"] == 5


def test_C12_B1_dinh_nghia_la_MOT_nguon_va_moi_ma_co_trong_cay_ATL():
    assert tuple(dong_pl.DINH_NGHIA) == tuple(MONG_PL)
    ma = dong_pl.ma_dung(dong_pl.DINH_NGHIA)
    theo = {n.ma for n in CAY.nut}
    assert len(ma) > 0 and ma <= theo, sorted(ma - theo)
    dong_pl.kiem_dinh_nghia(dong_pl.DINH_NGHIA, CAY)          # sạch ⇒ không nổ
    assert {n.nhom for n in CAY.nut if n.ma in MONG_PL} == {"HDCI"}


def test_C12_B1_cu_phap_ngoac_tru_trai_sang_phai_va_dau_unicode():
    ap = dong_pl.tinh_bieu_thuc
    v = {"A": 10, "B": 3, "C": 2}
    assert ap("A - B - C", v) == 5                  # trái→phải, ⛔ A−(B−C)=9
    assert ap("A - (B - C)", v) == 9
    assert ap("A − B + C", v) == 9                  # dấu − Unicode
    assert ap("-(A) + B", v) == -7
    assert ap("(A+B)-C", {"A": Decimal("0.1"), "B": Decimal("0.2"), "C": 0}) == Decimal("0.3")


def test_C12_B1_chenh_dinh_nghia_voi_MM_la_DANH_SACH_cho_owner_khong_tu_hoa_giai():
    ds = dong_pl.CHENH_VOI_MM
    assert len(ds) >= 1
    assert ("PL3", "LC") in {(d, m) for d, m, _ in ds}
    assert "LC" in dong_pl.ma_dung({"PL3": dong_pl.DINH_NGHIA["PL3"]})   # ATL GIỮ LC


# ── C12-B2 · an toàn ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("bt", [
    "__import__('os').system('x')", "__import__", "GI * OMC", "GI / OMC", "GI - ",
    "(GI - OMC", "GI - OMC)", "", "   ", "GI OMC", "1 + 2", "GI; OMC", "GI.x - OMC!",
    "open('f')", "GI ** 2", "[GI]", "GI + + ", "()",
])
def test_C12_B2_cu_phap_la_bi_tu_choi_PL_CU_PHAP(bt):
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.tinh_bieu_thuc(bt, HD_CAN)
    assert dong_pl.PL_CU_PHAP in e.value.ten, (bt, e.value)


def test_C12_B2_ma_la_PL_MA_LA_va_KHONG_goi_ham_nao():
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.tinh_bieu_thuc("GI - XYZ", HD_CAN, CAY)
    assert dong_pl.PL_MA_LA in e.value.ten and "XYZ" in str(e.value)
    nguon = (GOC / "fls/cau_hinh/dong_pl.py").read_text(encoding="utf-8")
    import ast
    goi = {n.func.id for n in ast.walk(ast.parse(nguon))
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert goi and not goi & {"eval", "exec", "compile", "__import__"}, goi   # AST, ⛔ chữ


def test_C12_B2_kiem_dinh_nghia_ma_ngoai_cay_PL_MA_LA_gom_HET_loi():
    xau = {"PL2": "GI - NOPE", "PL3": "PL2 - ", "PL4": "PL3 - ZZZ"}
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.kiem_dinh_nghia(xau, CAY)
    assert {dong_pl.PL_MA_LA, dong_pl.PL_CU_PHAP} <= e.value.ten
    assert len(e.value.loi) == 3, e.value.loi        # NOPE · cú pháp PL3 · ZZZ


def test_C12_B2_chu_trinh_PL_PL_CHU_TRINH():
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.tinh_pl(HD_CAN, {"PL2": "PL3 - OMC", "PL3": "PL2 - API"})
    assert dong_pl.PL_CHU_TRINH in e.value.ten


def test_C12_B2_thieu_gia_tri_HD_PL_THIEU_GIA_TRI_KHONG_im_lang_bang_0():
    v = {k: x for k, x in HD_CAN.items() if k != "OMC"}
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.tinh_pl(v)
    assert dong_pl.PL_THIEU_GIA_TRI in e.value.ten and "OMC" in str(e.value)


# ── C12-B3 · 2 phép CHECK ────────────────────────────────────────────────────
def test_C12_B3_check_tren_so_can_ca_hai_dung():
    kq = dong_pl.check_pl(HD_CAN)
    assert len(kq.phep) == 2
    assert [p.ten for p in kq.phep] == ["NB = 0", "NIS+INT+PIT+COM = CXA+GAH+DC+MC"]
    assert kq.phep[1].trai == kq.phep[1].phai == 125 != 0       # Đ3: vế ≠ 0
    assert all(p.dat for p in kq.phep) and kq.dat and kq.lech == ()


def test_C12_B3_NB_lech_1_bao_dung_phep_NB():
    kq = dong_pl.check_pl({**HD_CAN, "NB": 1})
    assert not kq.dat and kq.lech == ("NB = 0",), kq.lech
    assert kq.phep[0].chenh == 1 and kq.phep[1].dat


def test_C12_B3_ve_phai_lech_1_bao_phep_thu_hai_va_dong_nao():
    kq = dong_pl.check_pl({**HD_CAN, "GAH": 41})            # vế phải 126 ≠ 125
    assert kq.lech == ("NIS+INT+PIT+COM = CXA+GAH+DC+MC",), kq.lech
    p = kq.phep[1]
    assert (p.trai, p.phai, p.chenh) == (125, 126, -1)
    assert kq.phep[0].dat


def test_C12_B3_thieu_gia_tri_CHECK_PL_THIEU_GIA_TRI_khong_xanh_tren_rong():
    with pytest.raises(dong_pl.LoiPL) as e:
        dong_pl.check_pl({"NB": 0})
    assert dong_pl.PL_THIEU_GIA_TRI in e.value.ten
