"""ĐẦU VÀO CF · `gl_cf_dau_vao` — dòng sổ GL của BẢN SAO CF report cho H5 *(ISP 3.1.2 · WO-164)*.

Ảnh đóng băng SA chỉ-đọc cột `A·D·E·F·P·R·V` của `'Report I General Ledger'` *(spreadsheet CF
report — chính sheet mà công thức `Report I CFA1 Daily` SUMIFS vào)*; ⛔ phủ `B:C`.

Bài: số dòng + liên tục + checksum tái tính; cột ĐÚNG *(⛔ PII)*; `le` chỉ mang 4 mã LE của CFA1
*(mã khác — có cả TÊN người ở cột P — ⛔ vào ảnh, chỉ ĐẾM ở bảng phụ `le_lop`)*; khuôn TỪ CHỐI lưới sai.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))
from fls.oracle.anh_chup import AnhChup  # noqa: E402
from tools.khuon_dong_bang import gl_cf_dau_vao as _M  # noqa: E402

ANH = GOC / "tests" / "fixture" / "dap_an" / "gl_cf_dau_vao.json"
MONG = 12385


@pytest.fixture(scope="module")
def anh():
    return json.loads(ANH.read_text(encoding="utf-8"))


def _chu(x):
    return x["chu"] if isinstance(x, dict) else x


def _checksum_lai(a: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(a.get("phu", {}))
                for r in a["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(a["ngay_dong_bang"]),
                   nguon=a["nguon"], dong=tuple(a["dong"]) + phu).checksum()[:16]


def test_GLCF_B1_12385_dong_lien_tuc_checksum(anh):
    assert anh["so_dong"] == MONG == len(anh["dong"]) and anh["cong"]["dat"] is True
    assert [int(r["dong_sheet"]) for r in anh["dong"]] == list(range(10, 10 + MONG))
    assert anh["checksum_noi_dung"] == _checksum_lai(anh)


def test_GLCF_B2_cot_dung_khong_PII(anh):
    assert anh["cot"] == ["ngay", "itl_id", "le", "hd_final", "D", "E", "F"]
    moi_khoa = (set(anh["cot"]) | {anh["khoa"]}
                | {k for b in anh.get("phu", {}).values() for r in b["dong"] for k in r})
    assert not ({"Số chứng từ", "Diễn giải", "Email Address", "Tài khoản", "B", "C", "G"} & moi_khoa)


def test_GLCF_B2_le_chi_4_ma_CFA1__lop_dem_du(anh):
    le = [_chu(r["le"]) for r in anh["dong"]]
    assert set(le) <= {None, *_M.LE_CFA1}
    lop = {_chu(r["lop"]): int(r["so_dong"]) for r in anh["phu"]["le_lop"]["dong"]}
    assert sum(lop.values()) == MONG
    assert lop == _M.MONG_LE_LOP
    for m in _M.LE_CFA1:
        assert lop[m] == le.count(m)


def test_GLCF_B2_ngay_trong_dai_D_trong_tien_te(anh):
    ngay = [int(r["ngay"]) for r in anh["dong"]]
    assert min(ngay) == 45586 and max(ngay) == 46337          # 2024-10-21 … 2026-11-11
    d = [_chu(r["D"]) for r in anh["dong"]]
    assert set(d) <= {None, *_M.TIEN_TE} and d.count(None) == 12


def test_GLCF_khuon_tu_choi_cot_sai_va_dong_khong_lien_tuc():
    with pytest.raises(ValueError):
        _M.chuan_bi({"cot": ["dong_sheet", "A", "B", "C"], "dong_dau_sheet": 10, "values": [[10]]})
    hang = [10, 45600, "USD", 1, "", "SGO2", "ITL#1", "GI | Gross Inflow"]
    with pytest.raises(ValueError):
        _M.chuan_bi({"cot": list(_M.COT_THO), "dong_dau_sheet": 10,
                     "values": [hang, [12, *hang[1:]]]})


def test_GLCF_khuon_ma_P_khac_4_LE_khong_vao_anh():
    """Cột P có TÊN người *(đo 18/11)* ⇒ ⛔ vào ảnh: `le = None`, chỉ đếm lớp `khac`."""
    out = _M.chuan_bi({"cot": list(_M.COT_THO), "dong_dau_sheet": 10, "values": [
        [10, 45600, "USD", 1, "", "NGUOIX", "ITL#1", "GI | Gross Inflow"],
        [11, 45600, "USD", 1, "", "SGO2", "ITL#2", "GI | Gross Inflow"]]})
    assert [r[3] for r in out["dong"]] == [None, "SGO2"]
    assert "NGUOIX" not in json.dumps(out, ensure_ascii=False)
