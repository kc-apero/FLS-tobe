# -*- coding: utf-8 -*-
"""`C8` · `IX.ORG` *(ISP 3.1.2 Step 22 · `WO-176`)* — phần ĐƠN VỊ: ảnh DT3 → `ToChuc`.

Đ4 — mỗi số nói NÓ ĐẾM GÌ *(đo 18/11 trên ảnh đóng băng, KHÁC số ISP ghi)*:
  · `13` dòng ảnh CDT Correct *(ISP ghi `18` — `18` là vùng `BR11:BS28` của sheet, ảnh
    chỉ giữ `13` hàng có ô)*; `7` CDT1 **chuẩn khác nhau** *(ISP ghi `8` — `CMN` chỉ
    là nhãn NGUỒN, chuẩn hoá về `SHQ1`)*;
  · `69` hàng TK `R |` của bảng phụ `tho` = `59` pháp nhân + `8` nhãn `CN` + `2` `Cash
    Treasury` *(hai loại sau ⛔ vào kho: `CN` có số TK cá nhân, `Cash Treasury` ⛔ phải
    pháp nhân — `INV-I10`)*.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fls.cau_hinh import to_chuc

GOC = Path(__file__).resolve().parents[2]
ANH = GOC / "tests" / "fixture" / "cau_hinh"


def _kho() -> to_chuc.ToChuc:
    return to_chuc.doc_anh(
        (ANH / "cdt_correct.json").read_text(encoding="utf-8"),
        (ANH / "mapping_master_cfg.json").read_text(encoding="utf-8"),
        nguon="anh-dt3")


def test_C8_B1_CDT_nguon_ve_CDT1_dung_va_KHONG_la():
    k = _kho()
    r = to_chuc.cdt_cua(k, "SHQ2_Headquarters2")
    assert (r.cdt1, r.la) == ("SHQ2 | Headquarters2", False)
    r = to_chuc.cdt_cua(k, "CMN_Management")
    assert (r.cdt1, r.la) == ("SHQ1 | Headquarters1", False)
    assert to_chuc.cdt_cua(k, "CAH_Astronex").cdt1 == "CAH | Astronex"


def test_C8_B1_TK_ve_LE_qua_Mapping_Master():
    k = _kho()
    assert to_chuc.le_cua(k, "R | 854666_TCB USD_VGOH") == "VGOH"
    assert to_chuc.le_cua(k, "R | 542666_TCB USD_VISIONLAB") == "VVOV"
    assert to_chuc.le_cua(k, "R | 000_KHONG_CO") is None       # ⛔ đoán


def test_C8_B2_CDT_la_KHONG_roi_ve_SHQ2():
    r = to_chuc.cdt_cua(_kho(), "XYZ")
    assert r.la is True and r.cdt1 is None          # ⛔ 'SHQ2 | Headquarters2'


def test_CDT_da_la_chuan_thi_khong_la():
    # 'SHQ1 | Headquarters1' chỉ là cột ĐÍCH của ảnh, ⛔ phải 'lạ'
    assert to_chuc.cdt_cua(_kho(), "SHQ1 | Headquarters1").la is False


def test_so_dem_dung_nhan_Đ4():
    k = _kho()
    assert len(k.cdt) == 13                                   # dòng CDT Correct
    assert len(set(k.cdt.values())) == 7                      # CDT1 chuẩn khác nhau
    assert len(k.tk_le) == 59                                 # TK → pháp nhân
    assert {"CN", "Cash Treasury"}.isdisjoint(k.tk_le.values())
    assert len(set(k.tk_le.values())) == 19                   # pháp nhân khác nhau


def _hang_khong_phai_phap_nhan() -> list[str]:
    """TK của các hàng nhãn `CN`/`Cash Treasury` **đọc từ chính ảnh DT3 lúc chạy** —
    ⛔ chép số TK vào bài *(`C8-R1-01`: bài canh riêng tư ⛔ chứa dữ liệu riêng tư)*."""
    d = json.loads((ANH / "mapping_master_cfg.json").read_text(encoding="utf-8"))
    ra = []
    for r in d["phu"]["tho"]["dong"]:
        a, b = to_chuc._chu(r.get("A")), to_chuc._chu(r.get("B"))
        if a and a.startswith("R | ") and to_chuc.ma_le(b) in {"CN", "Cash Treasury"} \
                and a != to_chuc._AN_DANH:
            ra.append(a)
    return ra


def test_RIENG_TU_khong_TK_ca_nhan_vao_kho():
    k = _kho()
    cam = _hang_khong_phai_phap_nhan()
    assert len(cam) >= 4, len(cam)          # Đ3: mẫu số ≠ 0 *(ảnh có sẵn 4 + 2 hàng)*
    assert not set(cam) & set(k.tk_le)
    assert not any("an_danh" in t or t.endswith("_CN") for t in k.tk_le)


def _mm(*hang: tuple[str, str]) -> str:
    return json.dumps({"dong": [], "phu": {"tho": {"dong": [
        {"A": {"chu": "R | " + t}, "B": {"chu": le}} for t, le in hang]}}})


def test_TK_TRUNG_la_loi_co_ten():
    # TK GIẢ — ⛔ số thật
    with pytest.raises(to_chuc.LoiToChuc) as e:
        to_chuc.doc_tk_le(_mm(("GIA_01_X", "VGOH"), ("GIA_01_X", "VVOV")), nguon="x")
    assert e.value.ma == to_chuc.TK_TRUNG


def test_TK_RONG_la_loi_co_ten():
    with pytest.raises(to_chuc.LoiToChuc) as e:
        to_chuc.doc_tk_le(_mm(("GIA_02_X", "CN")), nguon="x")
    assert e.value.ma == to_chuc.TK_RONG


def test_RONG_la_loi_co_ten():
    van = '{"bang":"IX.ORG","dong":[]}'
    mm = (ANH / "mapping_master_cfg.json").read_text(encoding="utf-8")
    with pytest.raises(to_chuc.LoiToChuc) as e:
        to_chuc.doc_anh(van, mm, nguon="x")
    assert e.value.ma == to_chuc.CDT_RONG


def test_JSON_hong_va_khoa_trung_la_loi_co_ten():
    mm = (ANH / "mapping_master_cfg.json").read_text(encoding="utf-8")
    with pytest.raises(to_chuc.LoiToChuc) as e:
        to_chuc.doc_anh("{khong json", mm, nguon="x")
    assert e.value.ma == to_chuc.ORG_HONG
    trung = ('{"bang":"IX.ORG","dong":['
             '{"cdt_nguon":{"chu":"A"},"cdt1_chuan":{"chu":"B"}},'
             '{"cdt_nguon":{"chu":"A"},"cdt1_chuan":{"chu":"C"}}]}')
    with pytest.raises(to_chuc.LoiToChuc) as e:
        to_chuc.doc_anh(trung, mm, nguon="x")
    assert e.value.ma == to_chuc.CDT_TRUNG
