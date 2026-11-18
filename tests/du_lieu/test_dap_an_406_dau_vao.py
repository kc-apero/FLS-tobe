"""ĐẦU VÀO 406 · `gl_406_dau_vao` — tiền NGUYÊN TỆ E·F + số dư đầu kỳ, cho H4 *(ISP 3.1.2 · WO-132)*.

Ảnh ĐẦU VÀO độc lập *(cột `A·D·E·F·R`, ⛔ phủ `B:C`)* để `tinh_gl` chạy trên dòng sổ THẬT, thay vì
tái dựng `E`/`F` từ `BO`/`BP` của đáp án *(vòng tròn — orchestrator bác)*. Khuôn `gl_406_dau_vao`
*(đóng băng SA chỉ-đọc)* + bảng phụ `so_du_dau` *(5 ô gõ tay hàng 24)*.

Bài: cấu trúc + liên tục + checksum tái tính; ⛔ PII; cross-check `dong_sheet·itl_id·D` với
`gl_406.json` *(0 lệch)*; `so_du_dau` 5 ô công thức VERBATIM + hằng trích *(ghim)*; `itl_id_lech` 4.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))
from fls.oracle.anh_chup import AnhChup  # noqa: E402

ANH = GOC / "tests" / "fixture" / "dap_an" / "gl_406_dau_vao.json"
ANH_406 = GOC / "tests" / "fixture" / "dap_an" / "gl_406.json"
MONG = 7883
CHECKSUM = "9339488011a9358e"

#: 5 ô số dư đầu kỳ GÕ TAY ở hàng 24 — công thức VERBATIM (SA FORMULA) + hằng trích (Đ5: ghim).
SO_DU_DAU_GHIM = {
    "AX24": ("=+1235500+7189", "ton", "USD", "1242689"),
    "BA24": ("=985537", "ton", "SGD", "985537"),
    "BG24": ('=if($D24=BG$9,$E24,"")+6653796781', "ton", "VND", "6653796781"),
    "BQ24": ("=BQ23+BO24-BP24+56842628558/10^9", "bvnd_ton", "", "56.842628558"),
    "BT24": ("=BT23+BR24-BS24+2.267718", "musd_ton", "", "2.267718"),
}
TIEN_TE = ("USD", "SGD", "COP", "VND", "HKD")


@pytest.fixture(scope="module")
def anh():
    return json.loads(ANH.read_text(encoding="utf-8"))


def _chu(x):
    return x["chu"] if isinstance(x, dict) else x


def _checksum_lai(a: dict) -> str:
    """Tính lại bằng CHÍNH `AnhChup` — dòng chính + mọi dòng bảng phụ *(bọc `{"phu","dong"}`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(a.get("phu", {}))
                for r in a["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(a["ngay_dong_bang"]),
                   nguon=a["nguon"], dong=tuple(a["dong"]) + phu).checksum()[:16]


def test_DV_B1_7883_dong_khoa_dong_sheet_lien_tuc(anh):
    assert anh["so_dong"] == MONG == len(anh["dong"])
    assert anh["khoa"] == "dong_sheet" and anh["cong"]["dat"] is True
    ds = [int(r["dong_sheet"]) for r in anh["dong"]]
    assert ds == list(range(10, 10 + MONG)), "dong_sheet phải liên tục 10..7892"


def test_DV_B1_checksum_tai_tinh_khop(anh):
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM


def test_DV_B2_khong_mang_PII_cot_dung(anh):
    assert anh["cot"] == ["ky", "itl_id", "D", "E", "F"]
    moi_khoa = (set(anh["cot"]) | {anh["khoa"]}
                | {k for b in anh.get("phu", {}).values() for r in b["dong"] for k in r})
    assert not ({"Số chứng từ", "Diễn giải", "Email Address", "B", "C"} & moi_khoa)


def test_DV_B2_E_F_so_hoac_rong__D_trong_5_tien_te_hoac_rong(anh):
    thieu_D = 0
    for r in anh["dong"]:
        for c in ("E", "F"):
            v = r[c]
            if v is not None:
                assert not isinstance(v, dict), f"{c} ở {r['dong_sheet']} phải SỐ (⛔ chữ)"
                int(str(v).split(".")[0])            # phải parse được số
        d = _chu(r["D"])
        if d is None:
            thieu_D += 1
        else:
            assert d in TIEN_TE, f"D lạ {d!r} ở {r['dong_sheet']}"
    assert thieu_D == 6                               # 6 hàng thiếu tiền tệ (BO/BP rỗng ở đáp án)


def test_DV_B3_so_du_dau_5_o_cong_thuc_verbatim_va_hang(anh):
    phu = anh["phu"]["so_du_dau"]
    assert phu["mong"] == 5 and phu["so_dong"] == 5
    thuc = {}
    for r in phu["dong"]:
        assert int(_chu(r["ds"])) == 24                # cả 5 ô ở hàng 24
        thuc[_chu(r["o"])] = (_chu(r["cong_thuc"]), _chu(r["vao"]), _chu(r["tien_te"]),
                              _chu(r["hang_so"]))
    assert thuc == SO_DU_DAU_GHIM


#: Lỗi Sheets — TẬP ĐÓNG cho cột R *(H4-R1-04)*: `#N/A ()`, `#REF!`, `#DIV/0!`, …
LOI_SHEETS_RE = re.compile(r"#[A-Z/0-9!?]+( \(\))?")


def test_DV_B4_itl_id_lech_4_hang(anh):
    phu = anh["phu"]["itl_id_lech"]
    assert phu["mong"] == 4 and phu["so_dong"] == 4
    assert sorted(int(_chu(r["dong_sheet"])) for r in phu["dong"]) == [6684, 6836, 7500, 7832]
    for r in phu["dong"]:
        v = _chu(r["itl_id_tho"])
        assert not re.fullmatch(r"ITL#\d+", v)
        # H4-R1-04: cột R MỞ ⇒ phải là LỖI Sheets, ⛔ chuỗi tự do *(PII)* — tập đóng.
        assert LOI_SHEETS_RE.fullmatch(v), f"itl_id_tho ⛔ lỗi Sheets: {v!r}"


# ── H4-R1-04 · khuôn `gl_406_dau_vao` TỪ CHỐI cột R tự do + D đuôi trắng ────────────
from tools.khuon_dong_bang import gl_406_dau_vao as _M  # noqa: E402


def _raw(values):
    """Lưới thô tối thiểu hợp lệ cho `chuan_bi` *(so_du_dau 5 ô hợp lệ, ds liên tục từ 10)*."""
    sdd = [{"o": "AX24", "ds": 24, "cong_thuc": "=1", "vao": "ton", "tien_te": "USD", "hang_so": "1"},
           {"o": "BA24", "ds": 24, "cong_thuc": "=1", "vao": "ton", "tien_te": "SGD", "hang_so": "1"},
           {"o": "BG24", "ds": 24, "cong_thuc": "=1", "vao": "ton", "tien_te": "VND", "hang_so": "1"},
           {"o": "BQ24", "ds": 24, "cong_thuc": "=1", "vao": "bvnd_ton", "tien_te": "", "hang_so": "1"},
           {"o": "BT24", "ds": 24, "cong_thuc": "=1", "vao": "musd_ton", "tien_te": "", "hang_so": "1"}]
    return {"cot": list(_M.COT_THO), "dong_dau_sheet": 10, "values": values, "so_du_dau": sdd}


def test_DV_B4_frame_itl_loi_sheets_hop_le_thi_OK():
    out = _M.chuan_bi(_raw([[10, 45000, "VND", "100", "", "ITL#1"],
                            [11, 45000, "USD", "", "50", "#N/A ()"]]))
    assert [r["itl_id_tho"] for r in out["phu"]["itl_id_lech"]] == ["#N/A ()"]


def test_DV_B4_frame_cot_R_chuoi_tu_do_thi_TU_CHOI():
    """PII *(tên/SĐT)* lạc sang cột R mà vẫn đủ 4 hàng ⇒ phải TỪ CHỐI *(⛔ lọt vào ảnh)*."""
    with pytest.raises(ValueError, match="itl_id_lech"):
        _M.chuan_bi(_raw([[10, 45000, "VND", "100", "", "ITL#1"],
                          [11, 45000, "USD", "", "50", "Nguyen Van A 0912345678"]]))


def test_DV_B4_frame_D_duoi_trang_thi_TU_CHOI():
    """`D = "USD "` *(đuôi trắng)* ⇒ TỪ CHỐI — ⛔ chuẩn hoá ngầm để strip() thấy khớp."""
    with pytest.raises(ValueError, match="trắng"):
        _M.chuan_bi(_raw([[10, 45000, "USD ", "100", "", "ITL#1"]]))


def test_DV_B5_cross_check_voi_gl_406_0_lech():
    """`dong_sheet·itl_id·D` của ảnh đầu vào PHẢI trùng đáp án *(hai lượt đọc, hai vùng cột)*."""
    a = {int(r["dong_sheet"]): r for r in json.loads(ANH.read_text(encoding="utf-8"))["dong"]}
    b = {int(r["dong_sheet"]): r for r in json.loads(ANH_406.read_text(encoding="utf-8"))["dong"]}
    assert set(a) == set(b)
    lech = [ds for ds in a if (_chu(a[ds]["ky"]), _chu(a[ds]["itl_id"]), _chu(a[ds]["D"]))
            != (_chu(b[ds]["ky"]), _chu(b[ds]["itl_id"]), _chu(b[ds]["D"]))]
    assert lech == [], f"{len(lech)} dòng lệch ky/itl_id/D, 5 đầu: {lech[:5]}"


def test_DV_B5_lac_4_ky_vang(anh):
    assert anh["lac"] == ["202605", "202606", "202607", "202608"]
    assert anh["thieu"] == []
