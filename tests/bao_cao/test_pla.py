"""H8 *(ISP 3.1.2 · Step 39 · `WO-277`)* — bài ĐƠN VỊ của `fls/bao_cao/pla.py` *(SO.PLA1 · SO.PLA3)*.

  · **H8-B1 / AC-1** — PL start `2025-03-15` → end `2025-08` ⇒ TOÀN BỘ số vào `2025-03-01` *(D4 A, qua
    `ky.ngay_ghi_nhan` của C6 — dùng lại, ⛔ chép)*; luật B ⇒ `LUAT_CHUA_KY` *(⛔ chia đều)*.
  · `AH` *(yyyymm)* rỗng / tháng ∉ 1…12 ⇒ lỗi CÓ TÊN *(⛔ hoá 0, ⛔ tràn tháng như `DATE` của Sheets)*.
  · HR: năm PL theo luật AS-IS của `BM` *(2024 chỉ tháng 11·12, còn lại 2025)*.
  · KPI theo công thức CHÉO hàng của TỪNG tab *(dấu HR ngược)*; `NPC` = Σ hậu tố của `NP`; HR KPI
    chỉ cột đầu. PM+HR cộng theo KHOÁ — ⛔ vị trí *(AC-5)*.
"""
from __future__ import annotations

import dataclasses
from datetime import date
from decimal import Decimal as D

import pytest

from fls.bao_cao import pla
from fls.bao_cao.cfa import DongCFA
from fls.cau_hinh import ky
from fls.cau_hinh.hd import CayHD, NutHD

_G0 = date(1899, 12, 30)


def _s(d: date) -> int:
    return (d - _G0).days


# ── H8-B1 · D4 A ─────────────────────────────────────────────────────────────────

def test_H8_B1_PL_start_15_03_den_08_toan_bo_vao_01_03():
    # dịch vụ PL start 2025-03-15 → end 2025-08: luật A dồn TOÀN BỘ về 2025-03-01 (⛔ chia 6 tháng)
    assert pla.ngay_pl(ky.LUAT_A, date(2025, 3, 15), date(2025, 8, 31)) == _s(date(2025, 3, 1))
    dong = [DongCFA(ngay=pla.ngay_pl(ky.LUAT_A, date(2025, 3, 15), date(2025, 8, 31)), le=None,
                    hd="GI | GI", musd_no=D("6"), musd_co=D(0))]
    cay = CAY
    truc = list(range(_s(date(2025, 3, 1)), _s(date(2025, 8, 31)) + 1))
    kq = pla.pla_daily(dong, cay, truc, ("GROUP",), pla.CONG_THUC_PM)
    co_so = {k: v for k, v in kq.la.items() if v}                          # lá — KPI kéo theo GI
    assert co_so == {("GROUP", "GI", _s(date(2025, 3, 1))): D("6")}       # ⛔ 1/6 mỗi tháng


def test_H8_B1_luat_B_chia_deu_bi_tu_choi_co_ten():
    with pytest.raises(ky.LoiKy) as e:
        pla.ngay_pl(ky.LUAT_B, date(2025, 3, 15), date(2025, 8, 31))
    assert e.value.ma == ky.LUAT_CHUA_KY


@pytest.mark.parametrize("ah, ma", [(None, pla.AH_RONG), ("", pla.AH_RONG), (202527, pla.AH_LA),
                                    (202514, pla.AH_LA), (45962, pla.AH_LA), (262601, pla.AH_LA), ("abc", pla.AH_LA)])
def test_AH_rong_hoac_la_thi_loi_CO_TEN_khong_tran_thang(ah, ma):
    with pytest.raises(pla.LoiNgayPL) as e:
        pla.ngay_pl_tu_yyyymm(ky.LUAT_A, ah)
    assert e.value.ma == ma


def test_AH_hop_le_qua_C6_ngay_1():
    assert pla.ngay_pl_tu_yyyymm(ky.LUAT_A, 202503) == _s(date(2025, 3, 1))
    assert pla.ngay_pl_tu_yyyymm(ky.LUAT_A, "202410") == _s(date(2024, 10, 1))


@pytest.mark.parametrize("bk, bl, mong", [(11, 2024, date(2024, 11, 1)), (12, 2024, date(2024, 12, 1)),
                                          (3, 2024, date(2025, 3, 1)), (6, 2025, date(2025, 6, 1))])
def test_HR_nam_PL_theo_luat_AS_IS_cua_BM(bk, bl, mong):
    assert pla.ngay_pl_hr(ky.LUAT_A, bk, bl) == _s(mong)


# ── KPI · NPC · cột đầu HR · trong ─────────────────────────────────────────────────

def _cay(*cap) -> CayHD:
    return CayHD(nguon="bai", nut=tuple(NutHD(ma=m, ten=m, cha=c, cap=1, nhom="HDO", dong_sheet=str(i),
                                              thu_tu=i) for i, (m, c) in enumerate(cap)))


#: Cây rút gọn đủ mọi mã mà `CONG_THUC_PM/HR` nhắc tới.
_MA = ("GI", "OPC", "CAC", "MAC", "OMC", "MC", "OTMC", "COT", "COS", "PS", "API", "SC", "LC", "DC", "CSO",
       "GAC", "OGA", "CDC", "CXP", "ITE", "CFI", "LMN", "OMN", "NIS", "INT", "PIT", "COM", "DEP", "NB",
       "TAC", "CIT", "AR", "EBITDA", "EBIT", "EBT", "NP", "NPC", "NCF", "NCFO", "CRO", "COO", "NCFI", "CRI",
       "COI", "NCFF", "CRF", "COF", "CFO", "PL2", "PL3", "PL4", "PL5", "PL6", "PL7", "PL8")
_CHA = {"CAC": "OPC", "COS": "OPC", "MAC": "CAC", "COT": "CAC", "OMC": "MAC", "MC": "MAC", "OTMC": "MAC",
        **{m: "COS" for m in ("PS", "API", "SC", "LC", "DC", "CSO")}, "OGA": "GAC", "CXP": "CDC",
        "CRO": "NCFO", "COO": "NCFO", "CRI": "NCFI", "COI": "NCFI", "CRF": "NCFF", "COF": "NCFF",
        "CFO": "NCFF"}
CAY = _cay(*((m, _CHA.get(m)) for m in _MA))


def _d(t, ma, x, le=None):
    return DongCFA(ngay=t, le=le, hd=f"{ma} | {ma}", musd_no=D(x), musd_co=D(0))


DONG = [_d(1, "GI", 10), _d(1, "OMC", -3), _d(2, "OGA", -2), _d(3, "GI", 5), _d(2, "CIT", -1),
        _d(3, "TAC", -4)]


def test_KPI_cheo_hang_PM_va_tong_theo_cay():
    o = pla.pla_daily(DONG, CAY, [1, 2, 3], ("GROUP",), pla.CONG_THUC_PM).o
    g = lambda m, t: o[("GROUP", m, t)]  # noqa: E731
    assert (g("MAC", 1), g("CAC", 1), g("OPC", 1)) == (D(-3), D(-3), D(-3))      # tong = Σ con
    assert g("EBITDA", 1) == D(7) and g("EBITDA", 2) == D(-2)                    # GI + OPC + GAC
    assert g("NP", 2) == D(-3) and g("PL8", 3) == D(1)                           # PL8 = PL7 + TAC (hàng 57)
    assert g("COO", 3) == D(-4) and g("NCFO", 3) == D(1)                         # NCFO = CRO + COO
    # NPC = sum(G67:67) ⇒ Σ HẬU TỐ của NP: [7, −3, 5] ⇒ [9, 2, 5]
    assert [g("NP", t) for t in (1, 2, 3)] == [D(7), D(-3), D(5)]
    assert [g("NPC", t) for t in (1, 2, 3)] == [D(9), D(2), D(5)]
    assert g("AR", 1) == 0                                                       # trong


def test_KPI_HR_dau_NGUOC_chi_cot_dau_va_TAC_CIT_khong_cong_thuc():
    o = pla.pla_daily(DONG, CAY, [1, 2, 3], ("GROUP",), pla.CONG_THUC_HR).o
    g = lambda m, t: o[("GROUP", m, t)]  # noqa: E731
    assert g("EBITDA", 1) == D(10) - D(-3)                    # GI − OPC − GAC
    assert g("EBITDA", 2) == 0 and g("NPC", 2) == 0           # chỉ cột đầu
    assert g("CIT", 2) == 0 and g("TAC", 3) == 0              # GROUP HR ⛔ công thức
    assert g("COO", 2) == D(-2)                               # CRO/COO… mọi cột, dấu +


def test_PM_HR_cong_THEO_KHOA_KPI_tinh_lai_khong_cong_KPI():
    hr_dong = [_d(1, "OMC", 2), _d(2, "GI", 1)]
    pm = pla.pla_daily(DONG, CAY, [1, 2, 3], ("GROUP",), pla.CONG_THUC_PM)
    hr = pla.pla_daily(hr_dong, CAY, [1, 2, 3], ("GROUP",), pla.CONG_THUC_HR)
    ph = pla.pla_pm_hr_daily(pm, hr, CAY, ("GROUP",))
    assert ph.o[("GROUP", "OMC", 1)] == D(-1)                                     # lá cộng
    assert ph.o[("GROUP", "EBITDA", 1)] == D(10) + D(-1)                         # công thức 418 trên lá cộng
    assert ph.o[("GROUP", "EBITDA", 1)] != pm.o[("GROUP", "EBITDA", 1)] + hr.o[("GROUP", "EBITDA", 1)]


def test_AC5_cong_theo_VI_TRI_sai_khi_thu_tu_luoi_khac_theo_khoa_dung():
    a = {("G", "X", 1): D(1), ("G", "X", 2): D(2)}
    b = {("G", "X", 2): D(20), ("G", "X", 1): D(10)}                   # cùng khoá, KHÁC thứ tự
    assert pla.cong_theo_khoa(a, b, list(a)) == {("G", "X", 1): D(11), ("G", "X", 2): D(22)}
    vi_tri = dict(zip(a, (x + y for x, y in zip(a.values(), b.values()))))
    assert vi_tri != pla.cong_theo_khoa(a, b, list(a))
    with pytest.raises(KeyError):
        pla.cong_theo_khoa(a, {("G", "X", 1): D(1)}, list(a))          # thiếu khoá ⇒ ⛔ hoá 0


def test_YHQM_cuon_la_roi_tinh_lai_KPI_NPC_hau_to_tren_ky():
    s = _s(date(2025, 3, 1))
    dong = [_d(s, "GI", 4), _d(s + 31, "GI", 6)]                     # 03-01 · 04-01
    dl = pla.pla_daily(dong, CAY, [s, s + 31], ("GROUP",), pla.CONG_THUC_PM)
    y = pla.pla_yhqm(dl, CAY, ("GROUP",), pla.CONG_THUC_PM)
    g = lambda m, k: y.o[("GROUP", m, k)]  # noqa: E731
    assert (g("GI", "2025"), g("GI", "2025Q1"), g("GI", "2025Q2"), g("GI", "2025M04")) == (10, 4, 6, 6)
    assert g("EBITDA", "2025") == 10
    assert g("NPC", "2025M12") == 0 and g("NPC", "2025M04") == 6 and g("NPC", "2025") == 10 + 10 + 4 + 6 + 4 + 6     # Y + H1 + Q1 + Q2 + M03 + M04


def test_khoi_CDT_va_khoi_DU_SHQ2_bang_GROUP_tru_tong_CDT():
    """`cdt`: dòng mang mã khối CDT ở `le` *(GL `AD` · HR `BP`)*; khối dư = GROUP − Σ khối CDT *(công thức SHQ2)*."""
    dong = [_d(1, "GI", 10), _d(1, "GI", 4), _d(1, "GI", 1)]
    cdt = [dataclasses.replace(dong[0], le="CVL"), dataclasses.replace(dong[1], le="COR"),
           dataclasses.replace(dong[2], le=None)]                                   # nhãn CDT lạ ⇒ chỉ GROUP
    kq = pla.pla_daily(dong, CAY, [1], ("GROUP",), pla.CONG_THUC_PM, cdt=(cdt, ("CVL", "COR"), "SHQ2"))
    g = lambda k: kq.o[(k, "GI", 1)]  # noqa: E731
    assert (g("GROUP"), g("CVL"), g("COR"), g("SHQ2")) == (15, 10, 4, 1)
    assert kq.o[("SHQ2", "EBITDA", 1)] == 1 and kq.khoi == ("GROUP", "CVL", "COR", "SHQ2")


def test_HR_chi_khoi_GROUP_dau_nguoc_khoi_khac_dau_PM_moi_cot():
    dong = [_d(1, "GI", 10, le="SGO2"), _d(1, "OMC", -3, le="SGO2"), _d(2, "GI", 2, le="SGO2")]
    kq = pla.pla_daily(dong, CAY, [1, 2], ("GROUP", "SGO2"), pla.CONG_THUC_HR)
    assert kq.o[("GROUP", "EBITDA", 1)] == 13 and kq.o[("SGO2", "EBITDA", 1)] == 7     # GROUP − · SGO2 +
    assert kq.o[("GROUP", "EBITDA", 2)] == 0 and kq.o[("SGO2", "EBITDA", 2)] == 2      # chỉ cột đầu chỉ GROUP
