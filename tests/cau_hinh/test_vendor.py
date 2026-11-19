# -*- coding: utf-8 -*-
"""`C9-B2` — `IX.VEN` lõi kiểm THUẦN *(ISP 3.1.2 · Step 21 · `WO-172`)*: vendor trùng khoá ⇒
lỗi CÓ TÊN; mã `cach_tinh` chỉ là NHÃN, tập 5 nhãn riêng ĐÓNG *(Đ5: `mong`, NO hai chiều)*."""
from __future__ import annotations

import copy

import pytest

from fls.cau_hinh import vendor

CDT1_7 = [f"C{i} | Cdt{i}" for i in range(7)]


def _dong(thu_tu, dong_sheet, vendor_, no, cach, network=None, account=None):
    return {"thu_tu": thu_tu, "dong_sheet": str(dong_sheet), "No": str(no),
            "vendor": vendor_, "network": network, "account": account,
            "pct": "1", "cashin_month": "1", "cashin_day": "23", "cach_tinh": cach}


def _hop_le():
    return [
        _dong(1, 4, "VD341", 1, "VD341", "Admob", "A1"),
        _dong(2, 5, "VD444", 1, "VD444", "Ggplay_store", "A2"),
        _dong(3, 6, "VD428", 1, "VD428"),
        _dong(4, 7, "VD62", 1, "VD62"),
        _dong(5, 8, "VD111", 1, "Max", "Max", "Max Mediation"),
        _dong(6, 9, "VD336", 1, "thường"),
    ]


def _kiem(dong):
    return vendor.kiem(dong, cdt1=CDT1_7, nguon="bai-test")


def test_C9_B2_vendor_trung_khoa_loi_CO_TEN():
    d = _hop_le()
    d.append(_dong(7, 10, "VD341", 1, "VD341"))          # (VD341, No 1) lần hai
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("trùng" in x and "VD341" in x and "No=1" in x for x in e.value.ly_do), e.value.ly_do
    assert "\n" not in str(e.value)                      # luật S0-R1-04: một dòng


def test_C9_B2_dong_sheet_trung_loi_CO_TEN():
    d = _hop_le()
    d[1]["dong_sheet"] = d[0]["dong_sheet"]
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("dong_sheet" in x and "trùng" in x for x in e.value.ly_do), e.value.ly_do


def test_C9_hop_le_nam_nhan_rieng_va_bay_cdt1():
    b = _kiem(_hop_le())
    assert len(b.dong) == 6 and b.nhan_rieng == ("Max", "VD341", "VD428", "VD444", "VD62")
    assert b.cdt1 == tuple(CDT1_7)
    assert {d.cach_tinh for d in b.dong} == set(b.nhan_rieng) | {vendor.NHAN_THUONG}


@pytest.mark.parametrize("bo", ["Max", "VD341", "VD428", "VD444", "VD62"])
def test_C9_thieu_mot_nhan_rieng_DO(bo):
    d = [r for r in _hop_le() if r["cach_tinh"] != bo]
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("thiếu" in x and bo in x for x in e.value.ly_do), e.value.ly_do


def test_C9_nhan_la_thua_DO():
    d = _hop_le()
    d[5]["cach_tinh"] = "VD999"
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("VD999" in x and "cach_tinh" in x for x in e.value.ly_do), e.value.ly_do


@pytest.mark.parametrize("cdt1", [CDT1_7[:6], CDT1_7 + ["C7 | Cdt7"], CDT1_7[:6] + [CDT1_7[0]], []])
def test_C9_cdt1_khong_dung_bay_DO(cdt1):
    with pytest.raises(vendor.LoiVen) as e:
        vendor.kiem(_hop_le(), cdt1=cdt1, nguon="x")
    assert any("CDT1" in x for x in e.value.ly_do), e.value.ly_do


def test_C9_tap_rong_DO_khong_xanh_tren_tap_rong():            # Đ3
    with pytest.raises(vendor.LoiVen) as e:
        _kiem([])
    assert any("0 dòng" in x for x in e.value.ly_do), e.value.ly_do


@pytest.mark.parametrize("truong,gia_tri,lo", [
    ("pct", "0", "pct"), ("pct", "1e2", "pct"), ("pct", True, "pct"), ("pct", 0.5, "pct"),
    ("cashin_month", "13", "cashin_month"), ("cashin_day", "32", "cashin_day"),
    ("cashin_day", "０１", "cashin_day"), ("vendor", None, "vendor"), ("vendor", " ", "vendor"),
    ("No", "", "No"), ("cach_tinh", None, "cach_tinh"),
])
def test_C9_o_hong_NO_co_ten(truong, gia_tri, lo):
    d = copy.deepcopy(_hop_le())
    d[0][truong] = gia_tri
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any(lo in x for x in e.value.ly_do), e.value.ly_do


def test_C9_cot_la_NO():
    d = _hop_le()
    d[0]["email"] = "x@y"
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("cột lạ" in x and "email" in x for x in e.value.ly_do), e.value.ly_do


def test_C9_pct_null_hop_le_nhung_0_la_DO():
    d = _hop_le()
    d[0]["pct"] = None
    assert _kiem(d).dong[0].pct is None


# ══ DT9b (`WO-241`) — cột `so`: GI · OMC · SC · PS trong MỘT bảng ═════════════════════════════
def _them_so(d, so, tien_to=True):
    out = copy.deepcopy(d)
    for r in out:
        r["so"] = so
        if tien_to:
            r["dong_sheet"] = f"{so}!{r['dong_sheet']}"
    return out


def test_DT9b_so_mac_dinh_GI_va_BangVen_theo_so():
    b = _kiem(_hop_le())
    assert {d.so for d in b.dong} == {"GI"}                      # không khai ⇒ GI (bản kho DT8 cũ)
    b2 = _kiem(_hop_le() + _them_so([_dong(1, 4, "VD0", 1, "thường")], "OMC"))
    assert [d.so for d in b2.dong].count("OMC") == 1 and len(b2.dong) == 7
    assert len(b2.theo_so("GI").dong) == 6 and len(b2.theo_so("OMC").dong) == 1
    assert b2.theo_so("GI").nhan_rieng == b2.nhan_rieng and b2.theo_so("GI").cdt1 == b2.cdt1


def test_DT9b_theo_so_tap_rong_hay_so_la_NO():                    # Đ3
    b = _kiem(_hop_le())
    with pytest.raises(vendor.LoiVen) as e:
        b.theo_so("OMC")
    assert any("OMC" in x and "0 dòng" in x for x in e.value.ly_do), e.value.ly_do
    with pytest.raises(vendor.LoiVen):
        b.theo_so("XYZ")


def test_DT9b_cung_vendor_No_o_hai_so_khac_nhau_HOP_LE_cung_so_la_trung():
    ok = _hop_le() + _them_so([_dong(1, 4, "VD336", 1, "thường")], "SC")
    assert len(_kiem(ok).dong) == 7                                # (VD336, No 1) ở GI **và** SC
    xau = ok + _them_so([_dong(2, 5, "VD336", 1, "thường")], "SC")
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(xau)
    assert any("so=SC" in x and "VD336" in x and "trùng" in x for x in e.value.ly_do), e.value.ly_do


@pytest.mark.parametrize("so", ["XYZ", "gi", "", None, 1])
def test_DT9b_so_la_NO_co_ten(so):
    d = copy.deepcopy(_hop_le())
    d[0]["so"] = so
    with pytest.raises(vendor.LoiVen) as e:
        _kiem(d)
    assert any("so=" in x and "GI" in x for x in e.value.ly_do), e.value.ly_do


def test_DT9b_cashin_month_0_hop_le_vi_SC_VD529_cung_thang():
    d = copy.deepcopy(_hop_le())
    d[0]["cashin_month"] = "0"
    assert _kiem(d).dong[0].cashin_month == 0
    d[0]["cashin_month"] = "13"
    with pytest.raises(vendor.LoiVen):
        _kiem(d)
