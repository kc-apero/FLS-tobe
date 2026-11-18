"""ĐẦU VÀO H5 · `cfa1_dau_vao` — dòng sổ ITL Ledge 18/11 → LE · HD Final · ngày · tiền *(WO-168)*.

Bản thô ⛔ nằm trong repo *(mang tài khoản/bank ở cột G — chỉ để tách LE)* ⇒ ảnh thật kiểm bằng
**checksum ghim + khẳng định trường**; ca phá dựng LƯỚI TỔNG HỢP *(⛔ số thật)*.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys
from decimal import Decimal

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))
from fls.oracle.anh_chup import AnhChup  # noqa: E402
from tools.khuon_dong_bang import cfa1_dau_vao as M  # noqa: E402

ANH = GOC / "tests" / "fixture" / "dap_an" / "cfa1_dau_vao.json"
MONG = 12590
CHECKSUM = "9ea323cb88dc357f"
LE_DO = ['ASTRONEX', 'BGO2', 'CN', 'Coretap', 'HGO1', 'HGO2', 'HGO6', 'HIEPNV', 'HOATT', 'MGO1',
         'Nextwist', 'SGO2', 'SONNH', 'SUPERMINDS', 'TERASOFTS', 'TPCI', 'UGO2', 'VGC1', 'VGO1',
         'VGOH', 'VISIONLAB', 'VOOA', 'VOOL', 'VOON']   # 24 LE đo 18/11; ⛔ có GROUP · SGO1
LOI_LE = {'0_gach_co_tien_to': 806, '1_gach_co_tien_to': 1331}   # 2.137 dòng lỗi khuôn
HD_NGOAI = {('rong', None): 1, ('ngoai_atl', 'GAC - Other'): 1, ('ngoai_atl', 'Server Cost'): 7,
            ('ngoai_atl', 'ofR'): 1, ('ngoai_atl', 'oga'): 4}   # 14 dòng, 5 nhóm


def _chu(x):
    return x["chu"] if isinstance(x, dict) else x


@pytest.fixture(scope="module")
def anh():
    return json.loads(ANH.read_text(encoding="utf-8"))


def _checksum_lai(a):
    phu = tuple({"phu": t, "dong": r} for t in sorted(a.get("phu", {})) for r in a["phu"][t]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(a["ngay_dong_bang"]),
                   nguon=a["nguon"], dong=tuple(a["dong"]) + phu).checksum()[:16]


# ── AC-1 ────────────────────────────────────────────────────────────────
def test_AC1_12590_dong_lien_tuc_checksum_tai_tinh(anh):
    assert anh["so_dong"] == MONG == len(anh["dong"]) and anh["cong"]["dat"] is True
    assert [int(r["dong_sheet"]) for r in anh["dong"]] == list(range(10, 10 + MONG))
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM
    assert anh["cot"] == ["itl_id", "ngay", "le", "hd_final", "tien_te", "ps_no", "ps_co"]


def test_AC1_ngay_ISO_tien_2_so_le_tien_te_dong(anh):
    for r in anh["dong"]:
        datetime.date.fromisoformat(_chu(r["ngay"]))
        for c in ("ps_no", "ps_co"):
            if r[c] is not None:
                assert re.fullmatch(r"-?\d+\.\d{2}", r[c])
        assert _chu(r["tien_te"]) in (None, "USD", "SGD", "VND", "HKD", "COP")


# ── AC-2 ────────────────────────────────────────────────────────────────
def test_AC2_tap_LE_do_duoc_va_dem_loi_khuon(anh):
    les = sorted({_chu(r["le"]) for r in anh["dong"] if r["le"] is not None})
    assert les == LE_DO
    loi = {_chu(r["nhom"]): int(r["so_dong"]) for r in anh["phu"]["le_loi_khuon"]["dong"]}
    assert loi == LOI_LE
    assert sum(loi.values()) == sum(1 for r in anh["dong"] if r["le"] is None)


def test_AC2_HD_ngoai_ATL_dem_va_khai(anh):
    got = {(_chu(r["nhom"]), _chu(r["hd"])): int(r["so_dong"]) for r in anh["phu"]["hd_ngoai_atl"]["dong"]}
    assert got == HD_NGOAI
    atl = M._ma_atl()
    assert len(atl) == 74
    n = sum(1 for r in anh["dong"] if r["hd_final"] is None or _chu(r["hd_final"]) not in atl)
    assert n == sum(got.values())


# ── AC-4 · PII ──────────────────────────────────────────────────────────
def test_AC4_anh_khong_mang_PII(anh):
    moi = set(anh["cot"]) | {anh["khoa"]} | {k for b in anh["phu"].values() for r in b["dong"] for k in r}
    assert not ({"Số chứng từ", "Diễn giải", "Email Address", "B", "C", "G", "tk", "bank",
                 "Tài khoản"} & moi)
    van = ANH.read_text(encoding="utf-8")
    assert not re.search(r"OCBC|_SGO2 |\bR \| ", van)


def _luoi(**ghi_de):
    h = [10, "11/18/2026", "USD", "1,234.5", "", "R | PO2_OCBC USD_SGO2", "ITL#1", "GI | Gross Inflow"]
    return {"nguon": "t", "doc_luc": "2026-11-18", "cach_doc": "t", "dong_dau_sheet": 10,
            "cot": list(M.COT_THO), "values": [h]}


def test_AC4_chuan_bi_bo_G_va_tach_LE_chuan_hoa_ngay_tien():
    b = M.chuan_bi(_luoi())
    assert b["dong"] == [[10, "ITL#1", "2026-11-18", "SGO2", "GI", "USD", Decimal("1234.50"), None]]
    assert "OCBC" not in json.dumps(b, ensure_ascii=False, default=str)


def test_AC4_tu_choi_cot_ngoai_danh_sach():
    t = _luoi()
    t["cot"] = ["dong_sheet", "A", "B", "C", "D", "E", "F", "G", "R", "V"]
    with pytest.raises(ValueError):
        M.chuan_bi(t)


def test_AC2_loi_khuon_le_null_va_dem_nhom_khong_doan():
    t = _luoi()
    t["values"][0][5] = "SECRETBANK_KHONGKHUON"
    b = M.chuan_bi(t)
    assert b["dong"][0][3] is None
    assert b["phu"]["le_loi_khuon"] == [{"nhom": "1_gach_khong_tien_to", "so_dong": 1}]
    assert "SECRET" not in json.dumps(b, ensure_ascii=False, default=str)


def test_AC2_hd_ngoai_atl_va_rong_dem_rieng():
    t = _luoi()
    t["values"] += [[11, "11/18/2026", "USD", "1", "", "R | A_B USD_SGO2", "ITL#2", "ZZZ | La"],
                    [12, "11/18/2026", "USD", "1", "", "R | A_B USD_SGO2", "ITL#3", ""]]
    p = M.chuan_bi(t)["phu"]["hd_ngoai_atl"]
    assert {(x["nhom"], x["hd"]): x["so_dong"] for x in p} == {("ngoai_atl", "ZZZ"): 1, ("rong", None): 1}


def test_AC4_thieu_lac_do_ngay_hong_va_tien_te_la_loi_khong_in_gia_tri():
    t = _luoi()
    t["values"][0][1] = "xx"
    t["values"][0][2] = "PIIVALUE"
    b = M.chuan_bi(t)
    assert b["dong"][0][2] is None
    r = M.thieu_lac([{"dong_sheet": "10", "ngay": None, "tien_te": {"chu": "PIIVALUE"}}])
    assert r["thieu"] == ["ngay_khong_doc@10", "tien_te_la@10"]
    assert "PIIVALUE" not in json.dumps(r)


def test_AC4_ca_pha_ngay_MM_DD_khong_tran_thang():
    t = _luoi()
    t["values"][0][1] = "13/18/2026"          # tháng 13 ⇒ ⛔ đọc được
    assert M.chuan_bi(t)["dong"][0][2] is None
