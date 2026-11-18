"""ĐẦU VÀO GI cho cổng WP-C4a của H9 — `WO-204` (DT8b): khoá Vendor/tháng của MID3 + ảnh CFA1 GI.

    python tools/dong_bang_sheet.py gi_mid3 <tho_mid3.json> --mong 253   # + cột `vendor` `thang`
    python tools/dong_bang_sheet.py gi_cfa1 <tho_cfa1.json> --mong 408   # PD 504 → dau_vao/gi_cfa1.json

Đo 18/11 *(khoá SA chỉ-đọc, mỗi số một nhãn — Đ4)*:
  · MID3 `H` = Vendor ID · `F` = tháng `yyyymm` *(`G` = `F` trên 253/253 ⇒ ⛔ lấy)*; `K L M` *(LE ·
    No · ITL ID)* RỖNG cả 264 hàng ⇒ MID3 ⛔ có ITL ID. **209** hàng mang khoá *(19 Vendor × 11 tháng)*,
    **44** hàng tổng ⛔ khoá.
  · CFA1 `'CFA1 | GI Platform Data Ledger'` 408 hàng *(sheet 10…417)* = 36 hàng/tháng × 9 *(202502…
    202510)* + 42 × 2 *(202511 · 202512)*; Σ `T` theo (Vendor, tháng) = MID3 `O` trên **209/209**.
  · Vendor THƯỜNG (VD58 · VD61 · VD113 · VD336): **44** Vendor-tháng, PE ≠ 0 = **0** · O ≠ 0 = **0** ·
    P *(`S` số)* ≠ 0 = **0**; 28/44 Vendor-tháng có `S` = chữ `Need to manual input` *(⛔ hoá 0)*.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal

import pytest

from tests.du_lieu.test_dap_an_gi import (ANH, F, _chay, _checksum_lai, _chu, _doc, _viet_luoi)

CFA1 = F / "dau_vao" / "gi_cfa1.json"
COT_CFA1_THO = ["M", "K", "Q", "T", "S", "R"]
THUONG = {"VD58", "VD61", "VD113", "VD336"}
#: số dòng theo tháng *(Đ5 hai chiều)* — 9 tháng × 36 + 2 tháng × 42 = 408.
MONG_THANG = {**{t: 36 for t in range(202502, 202511)}, 202511: 42, 202512: 42}
#: sha256[:16] của các cột CŨ của gi_mid3 *(thu_tu · dong_sheet · 14 cột số)* trước DT8b — AC-1 "đúng từng byte".
SHA_COT_CU_MID3 = "285b413dab10123d"


def _cfa1():
    return _doc(CFA1)


def _luoi_cfa1(anh: dict) -> list[list]:
    return [[_chu(r["vendor"]), _chu(r["thang"]), _chu(r["no"]), _chu(r["pe"]),
             _chu(r["pm"]) if _chu(r["pm"]) is not None else _chu(r["pm_ghi_chu"]),
             _chu(r["itl_id"])] for r in anh["dong"]]


# ══ AC-1 · MID3 thêm khoá Vendor + tháng ════════════════════════════════════════

def test_AC1_mid3_cot_cu_dung_tung_byte_va_them_vendor_thang():
    anh = _doc(ANH["gi_mid3"])
    cu = ["thu_tu", "dong_sheet", "pe", "pm", "cvl_pe", "cvl_pm", "cor_pe", "cor_pm", "shq1_pe",
          "shq1_pm", "csm_pe", "csm_pm", "cah_pe", "cah_pm", "asa_pe", "asa_pm"]
    assert anh["cot"][-2:] == ["vendor", "thang"] and anh["cot"][:-2] == cu[2:]
    h = hashlib.sha256(json.dumps([[r.get(c) for c in cu] for r in anh["dong"]],
                                  ensure_ascii=False).encode()).hexdigest()[:16]
    assert h == SHA_COT_CU_MID3, "14 cột số + khoá cũ ⛔ đổi byte nào"


def test_AC1_mid3_khoa_209_hang_co_khoa_44_hang_tong():
    anh = _doc(ANH["gi_mid3"])
    co = [(_chu(r["vendor"]), _chu(r["thang"])) for r in anh["dong"] if _chu(r["vendor"])]
    assert len(co) == 209 and len(set(co)) == 209          # 19 × 11, ⛔ trùng
    assert sum(1 for r in anh["dong"] if _chu(r["vendor"]) is None and _chu(r["thang"]) is None) == 44
    assert len({v for v, _ in co}) == 19 and sorted({int(t) for _, t in co}) == list(range(202502, 202513))
    assert all(re.fullmatch(r"VD[0-9]+", v) for v, _ in co)
    assert {v for v, _ in co} >= THUONG
    assert "ITL ID" in anh["ghi_chu_khuon"] and "RỖNG" in anh["ghi_chu_khuon"]   # lý do ⛔ có ITL ID


def test_AC1_mid3_PHA_vendor_la_thi_DO_va_khong_in_gia_tri(tmp_path):
    anh = _doc(ANH["gi_mid3"])
    from tests.du_lieu.test_dap_an_gi import _luoi, COT_THO
    luoi = _luoi("gi_mid3", anh)
    luoi[30][16] = "Nguyễn Văn Bí Mật"                    # hàng có khoá: tên người lọt vào cột Vendor
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid3"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid3", str(bt), "--mong", "253", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "vendor_la@" in kq.stdout, (kq.stdout[-500:], kq.stderr[-300:])
    assert "Bí Mật" not in kq.stdout + kq.stderr


def test_AC1_mid3_PHA_mat_thang_o_hang_co_vendor_thi_DO(tmp_path):
    anh = _doc(ANH["gi_mid3"])
    from tests.du_lieu.test_dap_an_gi import _luoi, COT_THO
    luoi = _luoi("gi_mid3", anh)
    luoi[30][17] = None
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_THO["gi_mid3"], dong_dau=10, values=luoi)
    kq = _chay("gi_mid3", str(bt), "--mong", "253", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "thang_thieu@" in kq.stdout, (kq.stdout[-500:], kq.stderr[-300:])


# ══ AC-2 · ảnh CFA1 GI (PD 504) ═════════════════════════════════════════════════

def test_AC2_anh_cfa1_checksum_cong_dat_va_dem_dong():
    anh = _cfa1()
    assert anh["bang"] == "PD.504" and anh["so_dong"] == 408
    assert anh["cong"]["dat"] is True, anh["cong"]["ly_do"]
    assert anh["cot"] == ["vendor", "thang", "no", "pe", "pm", "pm_ghi_chu", "itl_id"]
    assert anh["checksum_noi_dung"] == _checksum_lai(anh)


def test_AC2_dong_theo_thang_khop_MONG():
    anh = _cfa1()
    dem = Counter(int(_chu(r["thang"])) for r in anh["dong"])
    assert dict(dem) == MONG_THANG and sum(dem.values()) == 408


def test_AC2_PM_chu_Need_to_manual_input_khong_hoa_0():
    anh = _cfa1()
    pm_chu = [r for r in anh["dong"] if _chu(r["pm_ghi_chu"]) is not None]
    assert len(pm_chu) == 176 and all(_chu(r["pm"]) is None for r in pm_chu)
    assert {_chu(r["pm_ghi_chu"]) for r in pm_chu} == {"Need to manual input"}
    assert sum(1 for r in anh["dong"] if _chu(r["pm"]) == "0") == 232       # 232 + 176 = 408
    assert Counter(_chu(r["itl_id"])[:3] for r in anh["dong"]) == {"ITL": 232, "Ko ": 176}


def test_AC2_tai_tao_dung_tung_byte(tmp_path):
    anh = _cfa1()
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_CFA1_THO, dong_dau=10, values=_luoi_cfa1(anh))
    ra = tmp_path / "ra.json"
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-900:], kq.stderr[-400:])
    assert ra.read_bytes() == CFA1.read_bytes()


def test_AC2_PHA_doi_thang_cua_mot_dong_thi_DO_hai_chieu(tmp_path):
    """Tổng 408 giữ nguyên, nhưng 202502 còn 35 · 202503 thành 37 ⇒ cổng theo tháng ĐỎ (Đ5)."""
    anh = _cfa1()
    luoi = _luoi_cfa1(anh)
    i = next(k for k, h in enumerate(luoi) if h[1] == "202502")
    luoi[i][1] = "202503"
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_CFA1_THO, dong_dau=10, values=luoi)
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "thang_lech@202502" in kq.stdout, (kq.stdout[-600:], kq.stderr[-300:])


def test_AC2_PHA_tap_rong_la_DO_khong_xanh(tmp_path):
    anh = _cfa1()
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_CFA1_THO, dong_dau=10, values=[])
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 2, (kq.stdout[-400:], kq.stderr[-400:])


def test_AC2_doi_chieu_sigma_PE_theo_vendor_thang_bang_O_cua_MID3_209_tren_209():
    """Hai nguồn độc lập *(CFA1 ΣT ↔ MID3 O)* khớp từng Vendor-tháng — mẫu số **209** ⛔ rỗng (Đ3)."""
    c = _cfa1()
    tong = defaultdict(Decimal)
    for r in c["dong"]:
        tong[(_chu(r["vendor"]), _chu(r["thang"]))] += Decimal(_chu(r["pe"]))
    m = _doc(ANH["gi_mid3"])
    o = {(_chu(r["vendor"]), _chu(r["thang"])): Decimal(_chu(r["pe"]))
         for r in m["dong"] if _chu(r["vendor"])}
    assert len(o) == 209 and set(tong) == set(o)
    assert sum(1 for k in o if abs(tong[k] - o[k]) < Decimal("0.001")) == 209


def test_AC3_mau_so_WP_C4a_vendor_thuong_la_44_va_TOAN_0():
    """KẾT QUẢ *(Đ3, ⛔ nền)*: 44 Vendor-tháng thường; PE ≠ 0 = 0 · O ≠ 0 = 0 · P ≠ 0 = 0."""
    c = _cfa1()
    pe, pm = defaultdict(Decimal), defaultdict(Decimal)
    chu_pm = set()
    for r in c["dong"]:
        v = _chu(r["vendor"])
        if v not in THUONG:
            continue
        k = (v, _chu(r["thang"]))
        pe[k] += Decimal(_chu(r["pe"]))
        pm[k] += Decimal(_chu(r["pm"]) or 0)
        if _chu(r["pm_ghi_chu"]):
            chu_pm.add(k)
    m = _doc(ANH["gi_mid3"])
    o = {(_chu(r["vendor"]), _chu(r["thang"])): Decimal(_chu(r["pe"]))
         for r in m["dong"] if _chu(r["vendor"]) in THUONG}
    assert len(pe) == len(o) == 44
    assert (sum(1 for x in pe.values() if x != 0), sum(1 for x in o.values() if x != 0),
            sum(1 for x in pm.values() if x != 0), len(chu_pm)) == (0, 0, 0, 28)


# ══ AC-4 · PII ══════════════════════════════════════════════════════════════════

def test_AC4_cfa1_anh_0_cot_cam():
    anh = _cfa1()
    assert "0 trùng" in anh["khong_mang_PII"] and "PM_COT_RIENG_TU" in anh["khong_mang_PII"]
    assert not any(k in c.lower() for c in anh["cot"] for k in ("email", "diễn giải", "tài khoản", "số chứng từ"))


def test_AC4_cfa1_PHA_email_bi_tu_choi_va_loi_khong_in_gia_tri(tmp_path):
    anh = _cfa1()
    luoi = [[*h, "ai@do.vn"] for h in _luoi_cfa1(anh)]
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=[*COT_CFA1_THO, "Email Address"], dong_dau=10, values=luoi)
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 2 and "PM_COT_RIENG_TU" in kq.stderr and "ai@do.vn" not in kq.stderr


def test_AC4_cfa1_PHA_ten_nguoi_o_cot_vendor_thi_DO_khong_in_gia_tri(tmp_path):
    anh = _cfa1()
    luoi = _luoi_cfa1(anh)
    luoi[5][0] = "Trần Thị Bí Mật"
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=COT_CFA1_THO, dong_dau=10, values=luoi)
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 1 and "vendor_la@" in kq.stdout, (kq.stdout[-500:], kq.stderr[-300:])
    assert "Bí Mật" not in kq.stdout + kq.stderr


def test_AC4_cfa1_PHA_cot_la_trong_luoi_bi_tu_choi(tmp_path):
    """Lưới đọc nhầm cột PII *(vd `B` Số CT)* ⇒ `cot` ⛔ đúng whitelist ⇒ TỪ CHỐI."""
    anh = _cfa1()
    bt = _viet_luoi(tmp_path / "tho.json", anh, cot=["M", "K", "Q", "T", "S", "B"], dong_dau=10,
                    values=_luoi_cfa1(anh))
    kq = _chay("gi_cfa1", str(bt), "--mong", "408", "--ra", str(tmp_path / "ra.json"))
    assert kq.returncode == 2, (kq.stdout[-300:], kq.stderr[-300:])
