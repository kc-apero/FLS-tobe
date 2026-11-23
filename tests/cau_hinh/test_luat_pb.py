# -*- coding: utf-8 -*-
"""`C11` — `IX.ALR`: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT *(ISP 3.1.2 · Step 25 ·
`WO-180`; AP v3.1.2 §3.2.2 IX.ALR · §3.2.5 · D2 · D3 · Q3)*. Lõi THUẦN `fls/cau_hinh/luat_pb.py`
— dữ liệu TỔNG HỢP ở đây *(⛔ giá trị thật)*; số đo trên ảnh THẬT ở `test_luat_pb_pg.py`.

Mỗi số nói NÓ ĐẾM GÌ *(Đ4)*: **17** = HD có luật *(4 `H1000 Ledger` + 8 `By GI` + 5 `By NOEM`)*;
4 mã `GI/OMC/PS/SC Ledger` là sổ nền tảng *(MID3)* ⇒ KHÔNG phải luật của IX.ALR.
"""
from __future__ import annotations

import pytest

from fls.cau_hinh import ky as ky_mod
from fls.cau_hinh import luat_pb as lp

NGUON = "bai-test-c11"
NEED = "Need to Allocate to CFA2"


def _mm(*, gi=8, noem=5, h=4, ledger=("GI", "OMC", "PS", "SC")):
    """Dòng Mapping Master TỔNG HỢP: mã `OFR` nằm trong nhóm NOEM *(ngoại lệ CAH)*."""
    r = []
    for i in range(gi):
        r.append({"hd_code": f"G{i:02d} | gi {i}", "need_cfa2": NEED, "method_cfa2": "By GI"})
    for i in range(noem):
        ma = "OFR" if i == 0 else f"N{i:02d}"
        r.append({"hd_code": f"{ma} | noem {i}", "need_cfa2": NEED, "method_cfa2": "By NOEM"})
    for i in range(h):
        r.append({"hd_code": f"H{i:02d} | h1000 {i}", "need_cfa2": NEED,
                  "method_cfa2": "H1000 Ledger"})
    for m in ledger:
        r.append({"hd_code": f"{m} | nen tang", "need_cfa2": NEED, "method_cfa2": f"{m} Ledger"})
    r.append({"hd_code": "X1 | khong can", "need_cfa2": None, "method_cfa2": None})
    return r


def _bang(tu_ky=202501, **kw) -> lp.BangALR:
    return lp.kiem(lp.dung_tu_mm(_mm(**kw), tu_ky=tu_ky), nguon=NGUON)


def _dong(**o):
    d = {"hd": "G00", "tu_ky": 202501, "nhan_mm": "By GI", "bat": False, "ngoai_le": []}
    d.update(o)
    return d


# ── C11-B2 · HD OFR của CAH ⛔ by NOEM (ngoại lệ AP §3.2.5) ──────────────────────────
def test_C11_B2_OFR_cua_CAH_khong_by_NOEM():
    b = _bang()
    cah = b.luat_cua("OFR", 202503, cdt1="CAH")
    assert cah is not None and cah.phuong_phap is None and cah.driver is None, cah
    assert cah.ngoai_le == "CAH" and cah.bat is False


def test_C11_B2_OFR_cua_CDT1_khac_van_by_NOEM():
    khac = _bang().luat_cua("OFR", 202503, cdt1="SHQ2")      # ⛔ chỉ CAH được miễn
    assert khac is not None and khac.phuong_phap == lp.BY_NOEM and khac.ngoai_le is None, khac


def test_C11_B2_OFR_khong_khai_cdt1_thi_loi_CO_TEN_khong_doan():
    with pytest.raises(lp.LoiLuatPB) as e:
        _bang().luat_cua("OFR", 202503)
    assert e.value.ma == lp.CAN_CDT1, e.value


def test_C11_B2_HD_NOEM_khac_khong_can_cdt1():
    r = _bang().luat_cua("N01", 202503)                      # ⛔ ngoại lệ chỉ của OFR
    assert r is not None and r.phuong_phap == lp.BY_NOEM


# ── C11-B3 · by GI ⇒ driver = PE (D3) ────────────────────────────────────────────────
def test_C11_B3_by_GI_driver_la_PE():
    r = _bang().luat_cua("G03", 202501)
    assert r.phuong_phap == lp.BY_GI and r.driver == "PE" == lp.DRIVER_BY_GI, r
    assert _bang().luat_cua("N01", 202501).driver == "NOEM"


def test_C11_B1_PM_H1000_mang_khong_qua_allocate_Q3():
    b = _bang()
    h = [b.luat_cua(f"H{i:02d}", 202501) for i in range(4)]
    assert all(x.phuong_phap == lp.H1000 and x.khong_qua_allocate and x.driver is None for x in h)
    assert not any(b.luat_cua(f"G{i:02d}", 202501).khong_qua_allocate for i in range(8))


# ── Đếm mong + cờ TẮT (D2) ────────────────────────────────────────────────────────────
def test_C11_B1_17_luat_4_8_5_100_phan_tram_bat_false():
    b = _bang()
    assert len(b.luat) == 17, len(b.luat)                    # ⛔ 21: 4 mã `X Ledger` ở ngoài
    dem = {}
    for x in b.luat:
        dem[x.phuong_phap] = dem.get(x.phuong_phap, 0) + 1
    assert dem == {lp.BY_GI: 8, lp.BY_NOEM: 5, lp.H1000: 4}, dem
    assert len(b.luat) > 0 and all(x.bat is False for x in b.luat)    # mẫu số ≠ 0 (Đ3)
    assert b.luat_cua("GI", 202501) is None                  # sổ nền tảng ⛔ luật IX.ALR


@pytest.mark.parametrize("kw", [dict(gi=7), dict(gi=9), dict(noem=4), dict(h=5)],
                         ids=["thieu-gi", "thua-gi", "thieu-noem", "thua-h1000"])
def test_C11_nap_tu_MM_so_luat_lech_MONG_thi_no_ca_hai_chieu(kw):
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.dung_tu_mm(_mm(**kw), tu_ky=202501)
    assert e.value.ma == lp.ALR_HONG and "mong" in str(e.value), e.value


def test_C11_nap_tu_MM_nhan_phuong_phap_la_thi_no():
    mm = _mm()
    mm.append({"hd_code": "ZZ | la", "need_cfa2": NEED, "method_cfa2": "By Moi"})
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.dung_tu_mm(mm, tu_ky=202501)
    assert "By Moi" in str(e.value)


def test_C11_nap_tu_MM_co_phuong_phap_ma_khong_need_thi_no():
    mm = _mm()
    mm[0]["need_cfa2"] = None
    with pytest.raises(lp.LoiLuatPB):
        lp.dung_tu_mm(mm, tu_ky=202501)


def test_C11_nap_tu_MM_rong_thi_no_khong_xanh_tren_tap_rong():
    with pytest.raises(lp.LoiLuatPB):
        lp.dung_tu_mm([], tu_ky=202501)


def test_C11_nap_tu_MM_khong_co_OFR_thi_no_vi_ngoai_le_tro_vao_hu_vo():
    mm = [r for r in _mm() if not r["hd_code"].startswith("OFR")]
    mm.append({"hd_code": "N99 | noem", "need_cfa2": NEED, "method_cfa2": "By NOEM"})
    with pytest.raises(lp.LoiLuatPB):
        lp.dung_tu_mm(mm, tu_ky=202501)


# ── D2: cờ ⛔ bật được qua nạp ────────────────────────────────────────────────────────
def test_C11_D2_bat_true_trong_ban_nap_thi_LoiLuatPB():
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([_dong(bat=True)], nguon=NGUON)
    assert "bat" in str(e.value) and "D2" in str(e.value)


@pytest.mark.parametrize("v", [0, "false", None, 1])
def test_C11_D2_bat_phai_dung_bool_False(v):
    with pytest.raises(lp.LoiLuatPB):
        lp.kiem([_dong(bat=v)], nguon=NGUON)


# ── Hiệu lực theo kỳ ──────────────────────────────────────────────────────────────────
def test_C11_hieu_luc_theo_ky_chon_ban_gan_nhat_khong_sau_ky():
    b = lp.kiem([_dong(tu_ky=202501, nhan_mm="By GI"),
                 _dong(tu_ky=202507, nhan_mm="By NOEM")], nguon=NGUON)
    assert b.luat_cua("G00", 202412) is None                 # chưa hiệu lực
    assert b.luat_cua("G00", 202501).phuong_phap == lp.BY_GI
    assert b.luat_cua("G00", 202506).phuong_phap == lp.BY_GI
    assert b.luat_cua("G00", 202507).phuong_phap == lp.BY_NOEM
    assert b.luat_cua("G00", 203001).phuong_phap == lp.BY_NOEM
    assert b.luat_cua("G00", 202507).tu_ky == 202507


def test_C11_ky_nhan_ca_so_yyyymm_lan_Ky():
    b = _bang()
    k = ky_mod.Ky(nam=2025, nua=1, quy=1, thang=3)
    assert b.luat_cua("G00", k) == b.luat_cua("G00", 202503)


@pytest.mark.parametrize("ky", [None, True, 2025, 202513, 202500, "202503", 20250301])
def test_C11_ky_hong_thi_loi_CO_TEN(ky):
    with pytest.raises(lp.LoiLuatPB) as e:
        _bang().luat_cua("G00", ky)
    assert e.value.ma == lp.KY_HONG


def test_C11_HD_khong_co_luat_tra_None_khong_no():
    assert _bang().luat_cua("KHONG_CO", 202503) is None


# ── Kiểm hình khi nạp ─────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("sua,chua", [
    (dict(nhan_mm="By Gi"), "nhan_mm"),                      # ⛔ phân biệt hoa thường
    (dict(hd=""), "hd"),
    (dict(tu_ky=202513), "tu_ky"),
    (dict(tu_ky="202501"), "tu_ky"),
    (dict(ngoai_le="CAH"), "ngoai_le"),
    (dict(ngoai_le=[""]), "ngoai_le"),
    (dict(ngoai_le=["CAH", "CAH"]), "ngoai_le"),
])
def test_C11_kiem_tung_truong_co_ly_do_ten_truong(sua, chua):
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([_dong(**sua)], nguon=NGUON)
    assert chua in str(e.value), e.value


def test_C11_kiem_cot_la_va_thieu_cot_va_trung_khoa_va_rong():
    for bad in ([dict(_dong(), la=1)], [{"hd": "G00"}], [_dong(), _dong()], [], ["x"]):
        with pytest.raises(lp.LoiLuatPB):
            lp.kiem(bad, nguon=NGUON)


def test_C11_kiem_gom_MOI_ly_do_khong_chi_ly_do_dau():
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([_dong(bat=True), _dong(hd="G01", nhan_mm="x")], nguon=NGUON)
    assert len(e.value.ly_do) >= 2, e.value.ly_do


# ── Bẫy VLOOKUP của `allocate.py` còn nguyên (⛔ IX.ALR đổi nó) ──────────────────────
def test_C11_bay_VLOOKUP_o_Method_rong_van_hien_0_khong_phai_No_need():
    from fls.ledger import allocate
    r = allocate.suy_allocate("SHQ2", "X", {"need_cfa2": "Need to Allocate to CFA2",
                                           "method_cfa2": None})
    assert r.method == "0" and r.method != allocate.CO_KHONG_CAN


# ── C11-R1-03 · cdt1 rỗng = THIẾU · ngoai_le chỉ ở HD AP khai ─────────────────────────
@pytest.mark.parametrize("cdt", ["", "   ", "\t"])
def test_C11_R1_03_cdt1_rong_hay_khoang_trang_coi_nhu_THIEU_CAN_CDT1(cdt):
    with pytest.raises(lp.LoiLuatPB) as e:
        _bang().luat_cua("OFR", 202503, cdt1=cdt)
    assert e.value.ma == lp.CAN_CDT1, e.value                # ⛔ trả By NOEM (đoán)


def test_C11_R1_03_cdt1_that_van_chay_sau_khi_siet_rong():
    b = _bang()
    assert b.luat_cua("OFR", 202503, cdt1="CAH").phuong_phap is None
    assert b.luat_cua("OFR", 202503, cdt1="SHQ2").phuong_phap == lp.BY_NOEM


@pytest.mark.parametrize("nhan,hd", [("By GI", "G00"), ("H1000 Ledger", "G00"),
                                     ("By NOEM", "G00"), ("By NOEM", "ZZZ")])
def test_C11_R1_03_ngoai_le_o_HD_ma_AP_khong_khai_thi_loi_CO_TEN(nhan, hd):
    with pytest.raises(lp.LoiLuatPB) as e:
        lp.kiem([_dong(hd=hd, nhan_mm=nhan, ngoai_le=["CAH"])], nguon=NGUON)
    assert "ngoai_le" in str(e.value) and hd in str(e.value), e.value


def test_C11_R1_03_ngoai_le_dung_HD_va_CDT1_AP_khai_van_qua():
    b = lp.kiem([_dong(hd="OFR", nhan_mm="By NOEM", ngoai_le=["CAH"])], nguon=NGUON)
    assert b.luat[0].ngoai_le_cdt1 == ("CAH",)
    lp.kiem([_dong(hd="OFR", nhan_mm="By NOEM", ngoai_le=[])], nguon=NGUON)   # rỗng luôn được
