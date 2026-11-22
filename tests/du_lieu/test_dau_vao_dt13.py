"""ĐẦU VÀO còn thiếu cho WP-C5a · C5b · C5c — `WO-319` *(ISP 3.1.2 · DT13)*: 4 ảnh `tests/fixture/dau_vao/` + đối chiếu dựng lại.

⭐ Số đo 22/11 *(khoá SA chỉ-đọc; mỗi số đếm MỘT vật — Đ4)*:
  | ảnh | nguồn · vùng | dòng ảnh | ô SỐ | phục vụ |
  | `ccr_so_du_ccr` | A-CCR `2. CCR` · A1:ABM240 → 31 ngày 31/10→30/11/2026 | 191 | 5.921 | PD 615 khối CB |
  | `ccr_so_du_cash` | A-CCR `2. CCR Cash` · cùng vùng | 62 | 1.922 | PD 615 khối CB |
  | `ccr_daily_report_2` | A-CCR `5. Daily Report 2` · A1:AR1114 (API trả 958 hàng) | 846 | 25.426 | PD 615 khối mUSD · CM · person GROUP |
  | `mid3_total` | P&L Report 4 tab `CFA2 | MID 3 | {GI,OMC,SC,PS}` · CHỈ hàng `TOTAL <yyyymm>` · cột O,P,S:AD | 39 | 546 | ATL lá `GI·OMC·SC·PS` × 6 CDT |
Bản A-CCR `5. Daily Report 3`: ⛔ ảnh mới — đo 22/11: 35.542/35.542 ô số trùng từng ô ảnh `daily_report_3_gop` *(ghi ở BG-320, ⛔ đo lại được
offline)*.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
DV = GOC / "tests" / "fixture" / "dau_vao"
DA = GOC / "tests" / "fixture" / "dap_an"
KH = GOC / "tools" / "khuon_dong_bang"
TEN = ("ccr_so_du_ccr", "ccr_so_du_cash", "ccr_daily_report_2", "mid3_total", "noem_com_cdt", "sign_off_dau_vao")

#: (số dòng ảnh, ô SỐ ≠ rỗng ở các cột số liệu) — ⭐ Đ5 đo 22/11 rồi khai; khác ⇒ ĐỎ cả hai chiều.
MONG = {"ccr_so_du_ccr": (191, 5921), "ccr_so_du_cash": (62, 1922), "ccr_daily_report_2": (846, 25426),
        "mid3_total": (39, 546), "noem_com_cdt": (9, 108), "sign_off_dau_vao": (94, 13541)}
#: ⭐ checksum TÍNH LẠI từ nội dung rồi ghim.
CHECKSUM = {"ccr_so_du_ccr": "9693d0a529bef99e", "ccr_so_du_cash": "f5822422a91a0f58", "ccr_daily_report_2": "db3ca1baedf59413",
            "mid3_total": "710889dbe81db12f", "noem_com_cdt": "eaa7fd6008a66569", "sign_off_dau_vao": "ef1744caf253f3bd"}
KHOA_ANH = {"ccr_so_du_ccr": "dong_sheet", "ccr_so_du_cash": "dong_sheet", "ccr_daily_report_2": "dong_sheet",
            "mid3_total": "so_dong_sheet", "noem_com_cdt": "dong_sheet", "sign_off_dau_vao": "dong_sheet"}
#: 6 ảnh `dau_vao` CÓ SẴN trước DT13 — đúng từng byte *(AC-2)*.
SHA_CU = {
    "gi_cfa1.json": "74db163e8030967f80ad45c35833ca092fc718efc53baa3ec2eebf2a0e7db808",
    "gl_pl_dau_vao.json": "acc16f1812b65f70adac0172670165960b0eeca4c25460d058b534a305ae4825",
    "hr_ledger_2024.json": "919ef27e3234ad1a16cf6c2972c25ff53e64ad2ee37f8328be37bb10d33762aa",
    "hr_ledger_2025.json": "2d65c4250c5e49ea61cbbe11e2a805933da465a8a77e557994c1c1179e2627a3",
    "hr_pl_dau_vao.json": "ac1a5e9982e708080c6ffa09a2dee1f1ac931ac273bceb18fd9810465130ef9c",
    "noem_com_gag.json": "2cd6f4756b14fc635dcf03096178da91186f64ac94d0f42aa0ff2a5dcdeb01e7",
}
SHA_DONG_BANG_SHEET = "2d8c1724f8403608ffdc1766f148c8c01e22e6da914bb64b701aba4f3cd291c9"


def _doc(ten: str) -> dict:
    return json.loads((DV / f"{ten}.json").read_text(encoding="utf-8"))


def _doc_da(ten: str) -> dict:
    return json.loads((DA / f"{ten}.json").read_text(encoding="utf-8"))


def _checksum_lai(anh: dict) -> str:
    """⭐ TÍNH LẠI checksum từ `dong` + `phu` của CHÍNH tệp ảnh *(⛔ chỉ so chữ ghi sẵn — `DT11-R1-01`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten, b in anh.get("phu", {}).items() for r in b["dong"])
    return AnhChup(run_id=f"dong_bang_sheet:{anh['khuon']}",
                   ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


@pytest.fixture(scope="module", params=TEN)
def bo(request):
    return request.param, _doc(request.param)


def _cot_so(ten: str, a: dict) -> list[str]:
    """Cột SỐ LIỆU của ảnh *(⛔ nhãn)*."""
    if ten.startswith("ccr_so_du"):
        return [c for c in a["cot"] if re.fullmatch(r"d20[0-9]{6}", c)]
    if ten == "sign_off_dau_vao":
        return [c for c in a["cot"] if re.fullmatch(r"[a-z]+_20[0-9]{4}", c)]
    if ten == "noem_com_cdt":
        return [c for c in a["cot"] if re.fullmatch(r"m[0-9]{2}", c)]
    if ten == "ccr_daily_report_2":
        return a["cot"][8:]                                    # g…al *(sau dong_sheet + che_do·khoi·ma·nhan_b…e)*
    return [c for c in a["cot"] if c not in ("tab", "thang")]


def _la_so(v) -> bool:
    return v is not None and not isinstance(v, dict)


def _num(v) -> float:
    return float(v)


# ── AC-2 · số dòng · ô SỐ khai `mong`; checksum TÍNH LẠI ─────────────────────

def test_AC2_anh_dong_o_so_khai_mong_va_cong_dat(bo):
    ten, a = bo
    n, o = MONG[ten]
    assert a["so_dong"] == len(a["dong"]) == n and a["cong"]["dat"] is True and a["cong"]["mong"] == n
    assert o > 0                                                          # Đ3: mẫu số ≠ 0
    so = sum(1 for d in a["dong"] for c in _cot_so(ten, a) if _la_so(d[c]))
    assert so == o
    assert a["thieu"] == [] and a["trung"] == [] and a["khoa_hong"] == [] and a["khoa"] == KHOA_ANH[ten]
    assert a["bang"].startswith(("DAU_VAO.", "NOEM.")) and a.get("o_loi", []) == [] and a["cot_khong_chon"] == []


def test_AC2_checksum_TINH_LAI_tu_noi_dung_khop_ghim(bo):
    ten, a = bo
    assert a["checksum_noi_dung"] == _checksum_lai(a) == CHECKSUM[ten]


@pytest.mark.parametrize("ten", TEN)
def test_AC2_PHA_doi_mot_o_thi_checksum_tinh_lai_DO(ten):
    a = _doc(ten)
    assert _checksum_lai(a) == CHECKSUM[ten]                              # nền XANH trước khi phá
    d = a["dong"][0]
    c = next(c for c in _cot_so(ten, a) if _la_so(d[c]))
    cu = d[c]
    d[c] = str(float(cu) + 1)
    assert _checksum_lai(a) != CHECKSUM[ten]


def test_AC2_anh_cu_va_cong_cu_chung_dung_tung_byte():
    for k, sha in SHA_CU.items():
        assert hashlib.sha256((DV / k).read_bytes()).hexdigest() == sha, k
    assert hashlib.sha256((GOC / "tools" / "dong_bang_sheet.py").read_bytes()).hexdigest() == SHA_DONG_BANG_SHEET
    assert {p.name for p in DV.glob("*.json")} == {*SHA_CU, *(f"{t}.json" for t in TEN)}   # ⛔ ảnh lạ


def test_AC2_khuon_la_tep_rieng_va_tai_dung_than_co_san():
    for ten in TEN:
        assert (KH / f"{ten}.py").is_file()
    assert (KH / "_ccr_so_du.py").is_file()
    # mở rộng khuôn ⛔ chép: `ccr_daily_report_2` NẠP `daily_report_2.py` *(⛔ có `def chuan_bi` riêng)*.
    src = (KH / "ccr_daily_report_2.py").read_text(encoding="utf-8")
    assert "daily_report_2.py" in src and "def chuan_bi" not in src and "chuan_bi = _d2.chuan_bi" in src


def test_AC2_kich_thuoc_anh_duoi_2MB_khong_can_khai(bo):
    ten, _ = bo
    assert (DV / f"{ten}.json").stat().st_size < 2 * 1024 * 1024


# ── AC-4 · PII ─────────────────────────────────────────────────────────────

def test_PII_ccr_chi_nhan_to_chuc_cot_E_ID_Pass_vang_va_ten_nguoi_da_che():
    for ten in ("ccr_so_du_ccr", "ccr_so_du_cash"):
        a = _doc(ten)
        assert a["cot"][:4] == ["thuc_the", "ngan_hang", "tien_te", "loai_tk"] and a["khoa"] == "dong_sheet"   # ⛔ E · G · H(ID) · I(Pass) · J
        van = (DV / f"{ten}.json").read_text(encoding="utf-8")
        for nhan in ("HoangACB", "Hoang"):
            assert nhan not in van
        nhan_cot = [v["chu"] for d in a["dong"] for c in ("thuc_the", "ngan_hang", "tien_te", "loai_tk")
                    for v in [d[c]] if isinstance(v, dict)]
        assert nhan_cot and not [x for x in nhan_cot if re.search(r"[0-9]{8,}", x)]           # Đ3: mẫu số ≠ 0
        assert not [x for x in nhan_cot if "@" in x]
    che = {d["ngan_hang"]["chu"] for d in _doc("ccr_so_du_cash")["dong"]
           if isinstance(d["ngan_hang"], dict) and d["ngan_hang"]["chu"].startswith("TK_CA_NHAN_")}
    assert che == {"TK_CA_NHAN_1"}                                                           # 1 nhãn `R | <tên>` — Đ4: SỐ KHÁC NHAU
    assert not {d["ngan_hang"]["chu"] for d in _doc("ccr_so_du_ccr")["dong"]
                if isinstance(d["ngan_hang"], dict) and d["ngan_hang"]["chu"].startswith("TK_CA_NHAN_")}


def test_PII_mid3_total_chi_hang_TOTAL_va_cot_so_lieu():
    a = _doc("mid3_total")
    assert a["cot"] == ["tab", "thang", "pe", "pm", *[f"{c}_{k}" for c in ("cvl", "cor", "shq1", "csm", "cah", "asa")
                                                       for k in ("pe", "pm")]]
    assert {d["tab"]["chu"] for d in a["dong"]} == {"GI", "OMC", "SC", "PS"}
    assert all(re.fullmatch(r"20[0-9]{2}(0[1-9]|1[0-2])", d["thang"]) for d in a["dong"])
    van = (DV / "mid3_total.json").read_text(encoding="utf-8")
    assert "@" not in van and not re.search(r"[0-9]{8,}[A-Za-z_]", van.replace("TOTAL", ""))       # ⛔ số chứng từ · số TK


# ── AC-3 · dựng lại nhóm ô đáp án *(CHỈ để ĐO — ⛔ đầu vào)* ───────────────────

#: PD 615 khối CB — công thức đọc được 22/11 *(`FORMULA`, CHỈ ĐỌC)*: ô = Σ dấu × `SUMIFS(<tab>!$K<hàng>:<hàng>, hàng 5 = ngày)` ÷ 10^mũ.
#: 46/47 hàng có cùng cấu trúc ở 30 cột `G…AJ`; **hàng 71** ⛔ vào *(cấu trúc ĐỔI giữa các cột: `G` 110+115, `H` 110+111+115)*.
CB_MAP = {
    56: (('2. CCR Cash', 10, 1, 6), ('2. CCR', 10, 1, 6)),
    57: (('2. CCR Cash', 11, 1, 6), ('2. CCR', 11, 1, 6)),
    58: (('2. CCR Cash', 12, 1, 6), ('2. CCR', 12, 1, 6)),
    59: (('2. CCR Cash', 14, 1, 9), ('2. CCR', 14, 1, 9)),
    61: (('2. CCR', 100, 1, 6), ('2. CCR', 101, 1, 6), ('2. CCR', 102, 1, 6)),
    62: (('2. CCR', 99, 1, 6),),
    66: (('2. CCR', 94, 1, 6), ('2. CCR', 95, 1, 6), ('2. CCR', 97, 1, 6)),
    67: (('2. CCR', 93, 1, 6), ('2. CCR', 96, 1, 6)),
    73: (('2. CCR', 111, 1, 6),),
    76: (('2. CCR', 104, 1, 6), ('2. CCR', 105, 1, 6)),
    77: (('2. CCR', 103, 1, 6),),
    81: (('2. CCR Cash', 32, 1, 6),),
    83: (('2. CCR Cash', 33, 1, 6),),
    86: (('2. CCR', 48, 1, 6), ('2. CCR', 49, 1, 6)),
    89: (('2. CCR', 46, 1, 9), ('2. CCR', 47, 1, 9), ('2. CCR', 50, 1, 9)),
    91: (('2. CCR', 54, 1, 6), ('2. CCR', 55, 1, 6)),
    94: (('2. CCR', 52, 1, 9), ('2. CCR', 53, 1, 9)),
    96: (('2. CCR', 42, 1, 6), ('2. CCR', 43, 1, 6)),
    99: (('2. CCR', 40, 1, 9), ('2. CCR', 41, 1, 9)),
    101: (('2. CCR', 60, 1, 6), ('2. CCR', 61, 1, 6)),
    104: (('2. CCR', 58, 1, 9), ('2. CCR', 59, 1, 9)),
    106: (('2. CCR', 66, 1, 6), ('2. CCR', 67, 1, 6)),
    109: (('2. CCR', 64, 1, 9), ('2. CCR', 65, 1, 9)),
    111: (('2. CCR', 107, 1, 6), ('2. CCR', 108, 1, 6), ('2. CCR', 109, 1, 6)),
    116: (('2. CCR', 112, 1, 6),),
    124: (('2. CCR', 113, 1, 6), ('2. CCR', 114, 1, 6)),
    126: (('2. CCR', 75, 1, 9),),
    127: (('2. CCR', 76, 1, 6),),
    129: (('2. CCR', 116, 1, 6),),
    131: (('2. CCR', 78, 1, 9),),
    132: (('2. CCR', 79, 1, 9),),
    134: (('2. CCR', 84, 1, 9),),
    135: (('2. CCR', 85, 1, 6),),
    137: (('2. CCR', 81, 1, 9),),
    138: (('2. CCR', 82, 1, 9),),
    140: (('2. CCR', 117, 1, 6),),
    142: (('2. CCR', 118, 1, 6),),
    144: (('2. CCR', 119, 1, 6),),
    146: (('2. CCR', 120, 1, 6),),
    148: (('2. CCR', 121, 1, 6),),
    150: (('2. CCR', 122, 1, 6),),
    152: (('2. CCR', 123, 1, 6),),
    154: (('2. CCR', 87, 1, 9),),
    155: (('2. CCR', 88, 1, 6),),
    157: (('2. CCR', 90, 1, 9),),
    158: (('2. CCR', 91, 1, 6),),
}
#: 30 cột `G…AJ` của 615 = ngày 01→30/11/2026 *(serial 46327…46356)*; tên cột ảnh `ccr_so_du_*` = `d<yyyymm dd>`.
_G_AJ = ("g h i j k l m n o p q r s t u v w x y z aa ab ac ad ae af ag ah ai aj").split()
_NGAY = {c: "d" + (datetime.date(1899, 12, 30) + datetime.timedelta(days=46327 + k)).strftime("%Y%m%d")
         for k, c in enumerate(_G_AJ)}


def doi_chieu_cb(a_ccr: dict, a_cash: dict, a_615: dict) -> tuple[int, int, list]:
    """→ (ô so được, khớp, lệch). Ô so được = ô 615 là SỐ ở hàng thuộc `CB_MAP` × 30 cột `G…AJ`."""
    anh = {"2. CCR": {int(d["dong_sheet"]): d for d in a_ccr["dong"]},
           "2. CCR Cash": {int(d["dong_sheet"]): d for d in a_cash["dong"]}}
    hang = {int(d["dong_sheet"]): d for d in a_615["dong"]}
    n = ok = 0
    lech = []
    for i, t in CB_MAP.items():
        for c in _G_AJ:
            a = hang[i][c]
            if not _la_so(a):
                continue
            e = 0.0
            for tab, h, dau, mu in t:
                d = anh[tab].get(h)
                v = d[_NGAY[c]] if d is not None else None
                e += dau * (_num(v) if _la_so(v) else 0.0) / 10 ** mu
            n += 1
            if abs(_num(a) - e) <= 1e-9 * max(1.0, abs(e)):
                ok += 1
            else:
                lech.append((i, c))
    return n, ok, lech


def test_AC3_615_khoi_CB_dung_lai_tu_2_CCR_va_2_CCR_Cash():
    a615 = _doc_da("ccr_daily_report")
    n, ok, lech = doi_chieu_cb(_doc("ccr_so_du_ccr"), _doc("ccr_so_du_cash"), a615)
    assert n == 46 * 30 > 0                                               # Đ3: mẫu số TRƯỚC — 46 hàng × 30 ngày, ⛔ 0
    assert ok == 1380 and lech == []
    cb = {int(d["dong_sheet"]) for d in a615["dong"] if (d["phan"] or {}).get("chu", "").startswith("CB I")}
    assert len(cb) == 47 and cb - set(CB_MAP) == {71}                     # hàng 71 ⛔ vào, CÓ TÊN


def test_AC3_PHA_doi_mot_o_nguon_thi_so_khop_DO():
    a615 = _doc_da("ccr_daily_report")
    ccr, cash = _doc("ccr_so_du_ccr"), _doc("ccr_so_du_cash")
    d = next(d for d in ccr["dong"] if int(d["dong_sheet"]) == 40)
    d["d20261115"] = str(float(d["d20261115"]) + 1000)                    # hàng 40 ⇒ ô 615 hàng 99 *(÷10^9 ⇒ lệch 1e-6)*
    n, ok, lech = doi_chieu_cb(ccr, cash, a615)
    assert ok == 1379 and lech == [(99, "u")]


#: A-CCR `5. Daily Report` ← `='5. Daily Report 2'!<cùng cột><hàng + độ lệch>` *(đo 22/11: 21.014 công thức tham chiếu trực tiếp,
#: 100 % cùng cột, độ lệch HẰNG theo khối)*.
OFF_MUSD = {"GROUP": -265, "SGO1": -281, "SGO2": -281, "HGO2": -293, "BGO2": -293}
OFF_CM = -301
_COT_GT = ["f", *_G_AJ, "ak", "al"]


def doi_chieu_dr2(a_dr2: dict, a_615: dict, phan: str, khoi: str, off: int) -> tuple[int, int]:
    dr2 = {int(d["dong_sheet"]): d for d in a_dr2["dong"]}
    n = ok = 0
    for d in a_615["dong"]:
        ph = (d["phan"] or {}).get("chu", "")
        if not (ph.startswith(phan) and (d["khoi"] or {}).get("chu") == khoi):
            continue
        r = dr2.get(int(d["dong_sheet"]) + off)
        for c in _COT_GT:
            if not _la_so(d[c]):
                continue
            n += 1
            if r is not None and _la_so(r[c]) and abs(_num(d[c]) - _num(r[c])) <= 1e-9 * max(1.0, abs(_num(r[c]))):
                ok += 1
    return n, ok


def test_AC3_615_mUSD_5_khoi_va_CM_GROUP_dung_lai_tu_ccr_daily_report_2_khop_het():
    a615, dr2 = _doc_da("ccr_daily_report"), _doc("ccr_daily_report_2")
    tong = khop = 0
    for k, off in OFF_MUSD.items():
        n, ok = doi_chieu_dr2(dr2, a615, "Unit: mUSD", k, off)
        assert n > 0 and ok == n, (k, n, ok)                              # Đ3: mẫu số TRƯỚC
        tong, khop = tong + n, khop + ok
    assert (tong, khop) == (12245, 12245)
    assert doi_chieu_dr2(dr2, a615, "CM Cumulative", "GROUP", OFF_CM) == (2176, 2176)


def test_AC3_615_CM_4_khoi_LE_khop_va_lech_co_ten():
    """4 khối LE: 7.724/8.704 — **980 ô lệch** là ô 615 KHÔNG phải tham chiếu trực tiếp *(hằng/công thức khác; đo `FORMULA`:
    SGO2 2.104/2.176 công thức · SGO1 · HGO2 1.360 · BGO2 1.354)* — ⛔ lỗi nguồn; khai số, ⛔ coi 0."""
    a615, dr2 = _doc_da("ccr_daily_report"), _doc("ccr_daily_report_2")
    ra = {k: doi_chieu_dr2(dr2, a615, "CM Cumulative", k, OFF_CM) for k in ("SGO2", "SGO1", "HGO2", "BGO2")}
    assert ra == {"SGO2": (2176, 2104), "SGO1": (2176, 1814), "HGO2": (2176, 1891), "BGO2": (2176, 1915)}


def test_AC3_PHA_doi_mot_o_dr2_thi_so_khop_DO():
    a615, dr2 = _doc_da("ccr_daily_report"), _doc("ccr_daily_report_2")
    d = next(d for d in dr2["dong"] if d["che_do"]["chu"] == "ngay" and d["khoi"]["chu"] == "GROUP" and _la_so(d["h"]))
    d["h"] = str(float(d["h"]) + 1)
    n, ok = doi_chieu_dr2(dr2, a615, "Unit: mUSD", "GROUP", OFF_MUSD["GROUP"])
    assert (n, ok) == (2325, 2324)


def doi_chieu_mid3(a_m3: dict, atl: dict) -> tuple[int, int, set]:
    """Lá ATL `(khối CDT, mã, <yyyy>M<mm>)` = `PM_cdt(TOTAL <yyyymm>) ÷ 10^6` *(× −1 trừ `GI`)* — BG-292 §"Lá"."""
    from tools import do_hd2_c5a as c5
    g = c5.gia_tri_atl(atl)
    n = ok = 0
    lech = set()
    for d in a_m3["dong"]:
        t, ym = d["tab"]["chu"], d["thang"]
        for c in ("cvl", "cor", "shq1", "csm", "cah", "asa"):
            e = _num(d[f"{c}_pm"]) / 1e6 * (1 if t == "GI" else -1)
            k = (c.upper(), t, f"{ym[:4]}M{ym[4:]}")
            if k not in g:
                continue
            n += 1
            if abs(float(g[k]) - e) <= 1e-9 * max(1.0, abs(e)):
                ok += 1
            else:
                lech.add(k)
    return n, ok, lech


def test_AC3_ATL_la_CDT_GI_OMC_SC_PS_dung_lai_tu_mid3_total():
    atl = _doc_da("atl")
    n, ok, lech = doi_chieu_mid3(_doc("mid3_total"), atl)
    assert n == 39 * 6 > 0                                                # Đ3: mẫu số TRƯỚC — 39 hàng TOTAL × 6 CDT
    assert ok == 231 and lech == {("SHQ1", "PS", "2025M12"), ("CSM", "PS", "2025M12"), ("CAH", "PS", "2025M12")}
    # ⛔ đối chiếu theo từng tab: GI 66/66 · OMC 60/60 · SC 54/54 · PS 51/54 *(H12 `BG-292` đo cùng số)*.
    tong = {t: sum(1 for d in _doc("mid3_total")["dong"] if d["tab"]["chu"] == t) * 6 for t in ("GI", "OMC", "SC", "PS")}
    assert tong == {"GI": 66, "OMC": 60, "SC": 54, "PS": 54}


def test_AC3_PHA_doi_mot_o_mid3_thi_so_khop_DO():
    atl = _doc_da("atl")
    a = _doc("mid3_total")
    d = next(d for d in a["dong"] if d["tab"]["chu"] == "GI")
    d["cvl_pm"] = str(float(d["cvl_pm"]) + 1e6)
    n, ok, lech = doi_chieu_mid3(a, atl)
    assert ok == 230 and len(lech) == 4


def doi_chieu_com(a_com: dict, atl: dict) -> tuple[int, int, set]:
    """PL5 = PL4 − COM(left(nhãn khối,3)) ÷ USD ÷ 10⁶ *(công thức `FORMULA` ATL cột `AG`, đọc 22/11)* ⇒ dựng `PL4 − PL5` từ ảnh
    COM + `ix_fx` rồi so với CHÍNH hiệu ở ATL. Khối = `GROUP` *(nhóm `GAG` — đối chứng cũ)* + 6 khối CDT *(`SHQ` = SHQ1 + SHQ2)*."""
    from tools import do_hd2 as h
    from tools import do_hd2_c5a as c5
    g = c5.gia_tri_atl(atl)
    fx = h.nap_fx()
    ma = {}
    for d in a_com["dong"]:
        ma.setdefault(d["ma"]["chu"], []).append(d)
    n = ok = 0
    lech = set()
    for kh, nhom in (("GROUP", "GAG"), ("CVL", "CVL"), ("COR", "COR"), ("SHQ1", "SHQ"), ("CSM", "CSM"), ("CAH", "CAH"), ("ASA", "ASA")):
        for m in range(1, 13):
            ky = f"2025M{m:02d}"
            if (kh, "PL4", ky) not in g or (kh, "PL5", ky) not in g:
                continue
            com = sum(_num(d[f"m{m:02d}"]) for d in ma[nhom])
            e = com / float(fx[202500 + m]["USD"]) / 1e6
            n += 1
            if abs(float(g[(kh, "PL4", ky)] - g[(kh, "PL5", ky)]) - e) <= 1e-9 * max(1.0, abs(e)):
                ok += 1
            else:
                lech.add((kh, ky))
    return n, ok, lech


def test_AC3_ATL_PL5_khoi_CDT_dung_lai_tu_noem_com_cdt():
    n, ok, lech = doi_chieu_com(_doc("noem_com_cdt"), _doc_da("atl"))
    assert n > 0 and (n, ok) == (84, 84) and lech == set()                # 7 khối × 12 tháng; Đ3: mẫu số TRƯỚC


def test_AC3_PHA_doi_mot_o_com_thi_so_khop_DO():
    a = _doc("noem_com_cdt")
    d = next(d for d in a["dong"] if d["ma"]["chu"] == "CVL")
    d["m03"] = str(float(d["m03"]) + 1e9)
    n, ok, lech = doi_chieu_com(a, _doc_da("atl"))
    assert (n, ok) == (84, 83) and lech == {("CVL", "2025M03")}


# ── Sign off (PD 605) làm ĐẦU VÀO của luỹ kế FS1 *(PD 608)* ───────────────────────────────────────────────────────────
_ENT = ("group", "visionlab", "terasofts", "superminds", "astronex", "ios", "headquarters", "checking")
_CF = json.loads((pathlib.Path(__file__).with_name("dt13_cong_thuc_fs1_sign_off.json")).read_text(encoding="utf-8"))


def _ten_cot_sign_off(letters: str) -> str:
    j = 0
    for ch in letters:
        j = j * 26 + ord(ch) - 64
    j -= 1
    e, k = divmod(j - 10, 24) if j < 178 else (7, j - 179)               # K…FV = 7 thực thể × 24 · FW trống · FX…GU = CHECKING
    if j >= 178:
        k = j - 179
    return f"{_ENT[e]}_{2024 + k // 12}{k % 12 + 1:02d}"


def doi_chieu_fs1(a_so: dict, a_fs1: dict) -> tuple[int, int, dict]:
    """Ô `CM Cumulative` của 608 là `Sign off!<ô> ÷ USD(tháng) ÷ 10⁶ [× −1]` *(`FORMULA` 22/11)* ⇒ dựng từ `sign_off_dau_vao` + `ix_fx`."""
    from tools import do_hd2 as h
    fx = h.nap_fx()
    so = {int(d["dong_sheet"]): d for d in a_so["dong"]}
    hang = {int(d["dong_sheet"]): d for d in a_fs1["dong"]}
    thang = {r["cot"]["chu"].lower(): r["gia_tri"] for r in a_fs1["phu"]["tieu_de"]["dong"] if int(r["dong_sheet"]) == 427}
    n = ok = 0
    theo_khoi: dict[str, list[int]] = {}
    for k, (sr, sg, cots) in _CF["hang608"].items():
        kh, i = k.split("|")
        for c in cots:
            a = hang[int(i)][c]
            if not _la_so(a):
                continue
            x = so[sr][_ten_cot_sign_off(_CF["cot_sign_off"][kh][c].upper())] if sr in so else None
            mo = thang[c]
            mo = int(mo["chu"] if isinstance(mo, dict) else mo)
            e = sg * (_num(x) if _la_so(x) else 0.0) / float(fx[mo]["USD"]) / 1e6
            n += 1
            t = theo_khoi.setdefault(kh, [0, 0])
            t[0] += 1
            if abs(_num(a) - e) <= 1e-9 * max(1.0, abs(e)):
                ok += 1
                t[1] += 1
    return n, ok, theo_khoi


def test_AC3_608_CM_Cumulative_khoi_Sign_off_dung_lai_tu_sign_off_dau_vao_va_ix_fx():
    n, ok, tk = doi_chieu_fs1(_doc("sign_off_dau_vao"), _doc_da("daily_report_3_fs1"))
    assert n > 0 and (n, ok) == (1363, 1363)                              # Đ3: mẫu số TRƯỚC
    assert {k: v[0] for k, v in tk.items()} == {"GROUP": 197, "CVL": 233, "COR": 233, "CSM": 233, "CAH": 233, "ASA": 234}


def test_AC3_PHA_doi_mot_o_sign_off_thi_so_khop_DO():
    a = _doc("sign_off_dau_vao")
    d = next(d for d in a["dong"] if int(d["dong_sheet"]) == 5)
    d["group_202501"] = str(float(d["group_202501"]) + 1e9)
    n, ok, _ = doi_chieu_fs1(a, _doc_da("daily_report_3_fs1"))
    assert (n, ok) == (1363, 1362)


def test_AC2_sign_off_dau_vao_cung_noi_dung_voi_anh_dap_an_605():
    """Hai ảnh CÙNG lưới + CÙNG giá trị *(đo ngày đóng băng: trùng `checksum_noi_dung`)* — ⛔ đầu vào chỉ khác TÊN/ĐƯỜNG DẪN."""
    a, b = _doc("sign_off_dau_vao"), _doc_da("daily_report_3")
    assert a["dong"] == b["dong"] and a["phu"] == b["phu"] and a["checksum_noi_dung"] == b["checksum_noi_dung"]
    assert a["bang"] != b["bang"] and a["bang"].startswith("DAU_VAO.")
