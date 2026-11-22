# -*- coding: utf-8 -*-
"""`C10` — lõi THUẦN `IX.DRV` *(ISP 3.1.2 · Step 29 · `WO-295`)*. Ảnh DT10 `ix_drv.json`: 238 ô số ·
146 ô thiếu CÓ TÊN · Σ7 CDT1 = 1 ở 34 tổng. Ô thiếu ⇒ `DRV_THIEU`, ⛔ `0`, ⛔ ô cứng H1000."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from fls.cau_hinh import driver as dv

GOC = Path(__file__).resolve().parents[2]
ANH = json.loads((GOC / "tests/fixture/cau_hinh/ix_drv.json").read_text(encoding="utf-8"))


def _bang(anh=ANH):
    cap = dv.dung_tu_anh(anh)
    return dv.kiem([{"khoa": k, **v} for k, v in cap], nguon="anh")


def _c(o):
    return o["chu"] if isinstance(o, dict) else o


def test_C10_mau_so_truoc_238_o_so_146_o_thieu_34_tong():
    # Đ3: mẫu số ≠ 0 TRƯỚC khi so
    b = _bang()
    assert b.so_o_so() == dv.MONG_O_SO == 238
    assert len(b.thieu) == dv.MONG_O_THIEU == 146
    assert len(b.luoi) == 21 and len(b.nb_le) == 304


def test_C10_B1_driver_cua_NOEM_SHQ1_202503_bang_anh():
    b = _bang()
    r = next(x for x in ANH["dong"] if _c(x["driver"]) == "NOEM" and _c(x["cdt1"]) == "SHQ1")
    assert dv.driver_cua(b, "NOEM", "SHQ1", 202503) == float(r["m03"])


def test_C10_B1_238_238_o_so_khop_anh():
    b, dem = _bang(), 0
    for r in ANH["dong"]:
        for i in range(1, 13):
            v = r[f"m{i:02d}"]
            if v is not None:
                assert b.driver_cua(_c(r["driver"]), _c(r["cdt1"]), 202500 + i) == float(v)
                dem += 1
    assert dem == 238


def test_C10_B2_146_o_thieu_nem_DRV_THIEU_co_ten():
    b, dem = _bang(), 0
    for r in ANH["phu"]["o_thieu"]["dong"]:
        loai, cdt1, th = _c(r["driver"]), _c(r["cdt1"]), int(_c(r["thang"]))
        with pytest.raises(dv.DrvThieu) as e:
            b.driver_cua(loai, cdt1, th)
        x = e.value
        assert (x.loai, x.cdt1, x.thang, x.ly) == (loai, cdt1, th, _c(r["ly_do"]))
        assert x.ma == "DRV_THIEU" and str(th) in str(x) and cdt1 in str(x)
        dem += 1
    assert dem == 146


@pytest.mark.parametrize("loai,cdt1", [("NOEM", "SHQ1"), ("GI_PE", "CVL"), ("GI_PM", "COR")])
def test_C10_B2_thang_2026_DRV_THIEU_khong_0_khong_o_cung(loai, cdt1):
    b = _bang()
    with pytest.raises(dv.DrvThieu) as e:
        b.driver_cua(loai, cdt1, 202603)
    assert "2026" in e.value.ly and "H1000" not in str(e.value) and "A4289" not in str(e.value)


def test_C10_B2_GI_202501_va_CMN_va_NB_LE_thieu_co_ly_do_khac_nhau():
    b = _bang()
    ly = set()
    for a in [("GI_PE", "CVL", 202501), ("NOEM", "CMN", 202507), ("NB_LE", "SHQ1", 202504)]:
        with pytest.raises(dv.DrvThieu) as e:
            b.driver_cua(*a)
        ly.add(e.value.ly)
    assert len(ly) == 3
    # NOEM 202501 CÓ số (chỉ GI thiếu 202501)
    assert b.driver_cua("NOEM", "CVL", 202501) > 0


def test_C10_loi_ten_loai_la_cdt1_la_thang_hong():
    b = _bang()
    for a, ma in [(("XX", "CVL", 202503), "DRV_LA"), (("NOEM", "ZZZ", 202503), "DRV_LA"),
                  (("NOEM", "CVL", 202513), "KY_HONG"), (("NOEM", "CVL", "202503"), "KY_HONG"),
                  (("NOEM", "CVL", True), "KY_HONG")]:
        with pytest.raises(dv.LoiDRV) as e:
            b.driver_cua(*a)
        assert e.value.ma == ma, a


def test_C10_AC4_NB_LE_co_duong_doc_rieng_From_To():
    b = _bang()
    r = ANH["phu"]["nb_le"]["dong"][0]
    assert b.nb_le_cua(_c(r["from"]), _c(r["to"]), 202511) == float(r["m11"]) == 0.376
    with pytest.raises(dv.LoiDRV) as e:
        b.nb_le_cua("NOPE", "All", 202501)
    assert e.value.ma == "DRV_LA"
    with pytest.raises(dv.DrvThieu):
        b.nb_le_cua(_c(r["from"]), _c(r["to"]), 202601)


def test_C10_dem_mong_hai_chieu_thieu_va_thua():
    a = copy.deepcopy(ANH)
    a["phu"]["o_thieu"]["dong"].pop()
    with pytest.raises(dv.LoiDRV):
        dv.dung_tu_anh(a)
    a = copy.deepcopy(ANH)
    a["dong"][0]["m01"] = "0.1"
    with pytest.raises(dv.LoiDRV):
        dv.dung_tu_anh(a)


def test_C10_kiem_o_null_khong_co_o_thieu_va_o_so_co_o_thieu_deu_do():
    cap = dv.dung_tu_anh(ANH)
    d = [{"khoa": k, **v} for k, v in cap]
    for sua in ("null", "thua"):
        x = copy.deepcopy(d)
        if sua == "null":
            x[0]["m05"] = None
        else:
            x.append({"khoa": dv.khoa_thieu("NOEM", "CVL", 202503), "ly_do": "thừa"})
        with pytest.raises(dv.LoiDRV):
            dv.kiem(x, nguon="t")


def test_C10_kiem_tong_7_CDT1_khac_1_do_va_rong_do():
    d = [{"khoa": k, **v} for k, v in dv.dung_tu_anh(ANH)]
    d[14]["m03"] += 1e-6     # NOEM CVL
    with pytest.raises(dv.LoiDRV) as e:
        dv.kiem(d, nguon="t")
    assert "Σ7" in str(e.value)
    with pytest.raises(dv.LoiDRV):
        dv.kiem([], nguon="t")


def test_C10_tong_34_Sigma_7_CDT1_bang_1_tren_anh():
    b, n = _bang(), 0
    for loai in dv.LOAI_SO:
        for i in range(1, 13):
            v = [b.luoi[(loai, c)][f"m{i:02d}"] for c in dv.CDT1_LUOI]
            if all(x is not None for x in v):
                assert abs(sum(v) - 1) <= 1e-9
                n += 1
    assert n == dv.MONG_TONG == 34
