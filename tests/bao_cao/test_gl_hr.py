"""H7 *(ISP 3.1.2 · Step 32 · WO-245)* — CA.GL dòng HR: nhãn HD Final qua `Code HR Allocate` *(IX.HD ·
Mapping Master cột M)* + CDT1 qua `cdt_cua` *(IX.ORG, C8)* — ⛔ SHQ2 mặc định.

⭐ AS-IS `Report I H1000 Ledge (HR Allocate HD) Y2025` cột `V` *(đo trên 407: 9.421 dòng)*: `I` trùng một ô
`code_hr` của Mapping Master ⇒ `hd_code` của dòng ấy; ⛔ trùng *(`PIT` trần · `PI…` · rỗng)* ⇒ mặc định khối
1 `OGA | GAC - Other` *(`fls.ledger.final_rule.MAC_DINH_THEO_KHOI`)* — ĐẾM có tên ở cổng, ⛔ im.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fls.bao_cao.gl import HD_MAC_DINH_HR, CdtLaHR, cdt1_hr, hd_final_hr
from fls.cau_hinh import hd as hd_cfg
from fls.cau_hinh import to_chuc

GOC = Path(__file__).resolve().parents[2]
MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
CDT = GOC / "tests" / "fixture" / "cau_hinh" / "cdt_correct.json"


@pytest.fixture(scope="module")
def code_hr():
    return hd_cfg.doc_code_hr_van_ban(MM.read_text(encoding="utf-8"), nguon=MM.name)


@pytest.fixture(scope="module")
def org():
    return to_chuc.doc_anh(CDT.read_text(encoding="utf-8"), MM.read_text(encoding="utf-8"), nguon="bai-h7")


def test_H7_code_hr_doc_9_ma_tu_Mapping_Master(code_hr):
    # Đ4: 9 = số dòng MM có cột M `Code HR Allocate` ≠ rỗng (đo 19/11) — 5 mã trần + 4 nhãn đủ
    assert len(code_hr) == 9
    assert code_hr["MC"] == "MC | Maketer Cost" and code_hr["NIS | Net Income Staff"] == "NIS | Net Income Staff"
    assert "PIT" not in code_hr and code_hr["PIT | PIT Total"] == "PIT | PIT Total"


def test_H7_code_hr_trung_thi_LoiHD():
    van = json.dumps({"bang": hd_cfg.BANG_MM, "dong": [
        {"hd_code": {"chu": "A | a"}, "code_hr": {"chu": "X"}},
        {"hd_code": {"chu": "B | b"}, "code_hr": {"chu": "X"}}]})
    with pytest.raises(hd_cfg.LoiHD, match="X"):
        hd_cfg.doc_code_hr_van_ban(van, nguon="ca-pha")
    with pytest.raises(hd_cfg.LoiHD):                       # Đ3: 0 mã ⇒ ⛔ có gì để tra
        hd_cfg.doc_code_hr_van_ban(json.dumps({"bang": hd_cfg.BANG_MM, "dong": []}), nguon="rong")


def test_H7_hd_final_hr_ma_tran_nhan_du_va_mac_dinh(code_hr):
    assert hd_final_hr(code_hr, "GAH") == ("GAH | GA HR Cost", False)
    assert hd_final_hr(code_hr, " INT | Insurance Total ") == ("INT | Insurance Total", False)
    for la in ("PIT", "PI01174-2", None, ""):
        assert hd_final_hr(code_hr, la) == (HD_MAC_DINH_HR, True), la
    assert HD_MAC_DINH_HR == "OGA | GAC - Other"


def test_H7_B2_cdt_la_nem_loi_co_ten_KHONG_SHQ2(org):
    assert cdt1_hr(org, "COR_TeraSofts") == "COR | TeraSofts"
    assert cdt1_hr(org, "SHQ2 | Headquarters2") == "SHQ2 | Headquarters2"       # đã chuẩn ⇒ ⛔ lạ
    for la in ("COR_Terasofts", "NIS | Net Income Staff", None, "  "):
        with pytest.raises(CdtLaHR) as e:
            cdt1_hr(org, la)
        assert e.value.ma == to_chuc.LOAI_SU_KIEN == "CDT_LA"
        assert "Headquarters2" not in str(e.value)                            # ⛔ gợi/rơi SHQ2
