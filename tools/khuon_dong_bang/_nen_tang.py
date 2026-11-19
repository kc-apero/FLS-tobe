"""Phần CHUNG của 9 khuôn `{omc,sc,ps}_mid{1,2,3}` *(ISP 3.1.2 · DT9 · `WO-220`)* — ⛔ KHÔNG phải khuôn
*(tên bắt đầu `_` ⇒ `danh_sach_khuon` bỏ qua; mỗi khuôn là một tệp riêng nạp `tao(sổ, mid)`)*.

⭐ **Vì sao.** AP v3.1.2 §3.4.1 PD 508–510: OMC · SC · PS có CÙNG ba tab với GI *(`gi_mid1/2/3`, DT8 +
DT8b)* nên cùng hình ảnh, KHÁC số đo. Bản đầu của `WO-220` chép 9 khuôn; ở đây MỘT thân + bảng
`DO` khai MONG *(Đ5)* theo từng ảnh. ⛔ sửa `tools/dong_bang_sheet.py` *(AC-6)*.

⛔⛔ **PII** *(`CLAUDE.md` Riêng tư)*: chỉ đọc cột khoá + số tiền + cột thượng nguồn. Vùng đọc ⛔ phủ
`A:C` *(Ngày/Số CT/Diễn giải)* · `G` *(Tài khoản)* · `N:O` MID1/2 *(File đính kèm)* · `A:N` MID3.

⭐ **Số đo 19/11** *(khoá SA chỉ-đọc; mỗi số đếm MỘT vật — Đ4; chi tiết ở `BG-221`)*:
  · **MID1** `D,J,K,Q,M,R,T,U,V,F,S` hàng 10…: `F` *(PS Có — `sumifs` Source (Looker))*, `T` =
    `ArrayFormula(F)` ⇒ `f == pe` trên MỌI hàng *(thượng nguồn, ⛔ vòng tròn: 0/116.423 ô công thức MID1 `F,M,Q,R,S,T,U,V` của 3 sổ
    nhắc MID2/MID3)*; `S` *(PM Amount)* = số HOẶC chữ `Need to manual input` ⇒ chữ TÁCH sang
    `pm_ghi_chu`, `pm` rỗng *(⛔ hoá 0 — AC-4)*.
  · **MID2** `D,J,K,M,T,AA,U,V`: `AA` RATE = số HOẶC `#DIV/0!`.
  · **MID3** `O,P,S…AF,H,F`: hàng `O` là SỐ vào ảnh *(hàng tổng-tháng ⛔ khoá `H` + hàng có khoá)*;
    `P` = số HOẶC `Need to manual input`; ô cdt rỗng giữ rỗng. Σ 6 PE_cdt = `O` ĐO LẠI độc lập:
    hàng lệch là NGUỒN *(SC 72)* ⇒ ghi `lac`, khai MONG, ⛔ đỏ nếu đúng số.
  · **Kỳ**: ba sổ chỉ có tháng `202503/04…202512` ⇒ 7 tháng `202603…202609` có **0** dòng ở CẢ BA
    *(AP viết "PS thiếu 03–09/2026" — đo: ⛔ phân biệt PS)*; cổng IN rõ và đỏ nếu một tháng 2026
    lọt vào.
"""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any

from fls.canon.o_loi import la_o_loi      # ô lỗi = tập ĐÓNG, 1 bản khai

KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
DONG_DAU_SHEET = 10
CHU_TAY = "Need to manual input"
CDT1_7 = frozenset({
    "SHQ2 | Headquarters2", "CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1",
    "CSM | SuperMinds", "CAH | Astronex", "ASA | Super App"})
VENDOR_RE = re.compile(r"VD[0-9]+")
ITL_ID_RE = re.compile(r"ITL#[0-9]+")
THANG_RE = re.compile(r"20[0-9]{2}(0[1-9]|1[0-2])")
TOL = Decimal("0.000001")
KY_DOI_CHIEU = tuple(f"2025{m:02d}" for m in range(3, 13))        # kỳ OMC: 202503…202512
THANG_AP_THIEU = tuple(f"2026{m:02d}" for m in range(3, 10))      # AP: "thiếu 03–09/2026" — 7 tháng

COT_THO = {1: ("D", "J", "K", "Q", "M", "R", "T", "U", "V", "F", "S"),
           2: ("D", "J", "K", "M", "T", "AA", "U", "V"),
           3: ("O", "P", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF",
               "H", "F")}
COT_ANH = {
    1: ("currency", "cdt1", "thang", "no", "vendor", "itl_id", "pe", "u", "v", "f", "pm", "pm_ghi_chu"),
    2: ("currency", "cdt1", "thang", "vendor", "pe", "rate", "u", "v"),
    3: ("pe", "pm", "cvl_pe", "cvl_pm", "cor_pe", "cor_pm", "shq1_pe", "shq1_pm", "csm_pe", "csm_pm",
        "cah_pe", "cah_pm", "asa_pe", "asa_pm", "vendor", "thang", "pm_ghi_chu"),
}
KIEU = {
    1: {"currency": "chu", "cdt1": "chu", "vendor": "chu", "itl_id": "chu?", "pe": "so", "u": "so!",
        "v": "so!", "f": "so", "pm": "so?", "pm_ghi_chu": "chu?"},
    2: {"currency": "chu", "cdt1": "chu", "vendor": "chu", "pe": "so", "rate": "so!", "u": "so!",
        "v": "so!"},
    3: {**{c: "so?" for c in COT_ANH[3][1:14]}, "vendor": "chu?", "thang": "so?", "pm_ghi_chu": "chu?",
        "pe": "so"},
}
#: số cột mang SỐ LIỆU đáp án của ảnh *(phạm vi cờ `nguon_nghi_loi`: hàng × cột)*.
COT_DAP_AN = {1: 5, 2: 4, 3: 14}
I_PE3, I_PM3 = (2, 4, 6, 8, 10, 12), (3, 5, 7, 9, 11, 13)

_L10 = {t: 623 for t in KY_DOI_CHIEU}
_T9 = KY_DOI_CHIEU[1:]


def _bang(*cap):
    return {t: n for t, n in zip(_T9, cap)}


#: ⭐ MONG theo ảnh *(Đ5 hai chiều — đo 19/11; đổi nguồn ⇒ ĐỎ ⇒ ghi lại bản khai + đóng băng lại)*.
#: `thang` = dòng/tháng *(MID3: chỉ hàng CÓ khoá)* · `loi` = phân bố ô lỗi `so!` · `pm_chu` = ô PM
#: chữ · `dem` = hàng đệm MID1 · `itl_na` = `R` `#N/A` · `tong`/`ngoai` = MID3 hàng tổng-tháng/ngoài
#: ảnh · `lech_pe` = hàng Σ 6 PE_cdt ≠ O của NGUỒN.
DO = {
    ("omc", 1): dict(thang={t: 623 for t in KY_DOI_CHIEU}, pm_chu=5899, dem=0, itl_na=559,
                     loi={"u": {"#VALUE!": 84, "#DIV/0!": 4836}, "v": {"#VALUE!": 84, "#DIV/0!": 4836}}),
    ("sc", 1): dict(thang={**_bang(427, 427, 427), **{t: 651 for t in _T9[3:]}}, pm_chu=5038, dem=574,
                    itl_na=592, loi={"u": {"#VALUE!": 1314, "#DIV/0!": 2796},
                                     "v": {"#VALUE!": 1314, "#DIV/0!": 2796}}),
    ("ps", 1): dict(thang={t: 945 for t in _T9}, pm_chu=8359, dem=0, itl_na=1069,
                    loi={"u": {"#DIV/0!": 7290}, "v": {"#DIV/0!": 7290}}),
    ("omc", 2): dict(thang={t: 147 for t in KY_DOI_CHIEU},
                     loi={"rate": {"#DIV/0!": 931}, "u": {"#VALUE!": 462, "#DIV/0!": 798},
                          "v": {"#VALUE!": 462, "#DIV/0!": 798}}),
    ("sc", 2): dict(thang={**{t: 63 for t in _T9[:7]}, **{t: 70 for t in _T9[7:]}},
                    loi={"rate": {"#DIV/0!": 273}, "u": {"#DIV/0!": 240, "#VALUE!": 254, "#REF!": 8},
                         "v": {"#DIV/0!": 240, "#VALUE!": 254, "#REF!": 8}}),
    ("ps", 2): dict(thang={t: 371 for t in _T9},
                    loi={"rate": {"#DIV/0!": 3339}, "u": {"#DIV/0!": 2898}, "v": {"#DIV/0!": 2898}}),
    ("omc", 3): dict(thang={t: 89 for t in KY_DOI_CHIEU}, pm_chu=559, tong=10, ngoai=0, lech_pe=0),
    ("sc", 3): dict(thang={**{t: 61 for t in _T9[:3]}, **{t: 93 for t in _T9[3:]}}, pm_chu=490,
                    tong=9, ngoai=10, lech_pe=72),
    ("ps", 3): dict(thang={t: 65 for t in _T9}, pm_chu=439, tong=9, ngoai=1476, lech_pe=0),
}


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _la_so(v: Any) -> bool:
    return isinstance(v, (int, Decimal)) and not isinstance(v, bool)


def _chu(d: dict, c: str) -> str | None:
    v = d.get(c)
    return v["chu"] if isinstance(v, dict) else None


def _dec(v: Any) -> Decimal | None:
    if v is None:
        return Decimal(0)
    try:
        return Decimal(v)
    except (InvalidOperation, TypeError):
        raise ValueError("ô cột đáp án ⛔ phải số") from None


def _pm(v: Any, i: int) -> tuple[Any, Any]:
    """Ô PM → `(pm, ghi_chu)`: số ⇒ `(số, None)` · chữ `Need to manual input` ⇒ `(None, chữ)` ·
    rỗng ⇒ `(None, None)`. Chữ khác ⇒ TỪ CHỐI *(⛔ in giá trị ô)*."""
    if _rong(v):
        return None, None
    if _la_so(v):
        return v, None
    if v == CHU_TAY:
        return None, v
    raise ValueError(f"hàng {i + 1}: ô PM ⛔ phải số/rỗng/'{CHU_TAY}' *(giá trị ⛔ in)*")


def _kiem_thang(dong, mong: dict, co_khoa: bool) -> tuple[list[str], dict[str, int], list[str]]:
    """→ (vi phạm, đếm theo tháng, tháng thiếu so với kỳ đối chiếu). Đ5 hai chiều: tháng thừa,
    thiếu, hay đổi số dòng đều ĐỎ; tháng 2026 lọt vào ĐỎ riêng."""
    vp: list[str] = []
    dem: dict[str, int] = {}
    for d in dong:
        ds, t = d["dong_sheet"], d.get("thang")
        if co_khoa and _chu(d, "vendor") is None:      # hàng tổng-tháng: ⛔ có `thang`
            if t is not None:
                vp.append(f"thang_lech@{ds}")
            continue
        if not (isinstance(t, str) and THANG_RE.fullmatch(t)):
            vp.append(f"thang_la@{ds}")
            continue
        dem[t] = dem.get(t, 0) + 1
    for t in sorted(set(dem) | set(mong)):
        if dem.get(t, 0) != mong.get(t, 0):
            vp.append(f"thang_lech@{t}:{dem.get(t, 0)}≠{mong.get(t, 0)}")
        if t.startswith("2026") and t in dem:
            vp.append(f"thang_2026@{t}")
    return vp, dict(sorted(dem.items())), [t for t in KY_DOI_CHIEU if t not in dem]


def _dai_thang(dem: dict[str, int], thieu: list[str]) -> str:
    ap = sum(1 for t in THANG_AP_THIEU if dem.get(t, 0) == 0)
    return (f"tháng có dòng {len(dem)} *({min(dem)}…{max(dem)})* · thiếu so kỳ đối chiếu "
            f"{KY_DOI_CHIEU[0]}…{KY_DOI_CHIEU[-1]}: {thieu or 'không'} · AP khai thiếu "
            f"{THANG_AP_THIEU[0]}…{THANG_AP_THIEU[-1]}: {ap}/{len(THANG_AP_THIEU)} tháng có 0 dòng "
            f"*(mong {len(THANG_AP_THIEU)}; ⛔ lấp)*")


def tao(so: str, m: int) -> dict[str, Any]:
    """Dựng giao kèo khuôn `<so>_mid<m>` cho `dong_bang_sheet.nap_khuon`."""
    do = DO[(so, m)]
    ten = f"{so}_mid{m}"
    cot_tho, cot_anh = COT_THO[m], COT_ANH[m]
    phu_mong: dict[str, int] = {}
    if m == 1:
        phu_mong = {"dem": 1, "itl_id_loi": do["itl_na"]}
    if m == 3:
        phu_mong = {"ngoai_anh": 1}
    if so == "omc":
        phu_mong["nguon_nghi_loi"] = 1

    def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
        if tho.get("cot") != list(cot_tho):
            raise ValueError(f"`cot` phải đúng {list(cot_tho)} *(cột KHÔNG PII)*")
        if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
            raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
        values = tho.get("values")
        if not isinstance(values, list) or not values:
            raise ValueError(f"`values` phải lưới hàng MID{m} ⛔ rỗng")
        dong: list[list[Any]] = []
        phu: dict[str, Any] = {}
        so_dem = so_ngoai = 0
        itl_loi: list[dict[str, Any]] = []
        for i, h in enumerate(values):
            if not isinstance(h, list) or len(h) != len(cot_tho):
                raise ValueError(f"hàng {i + 1} phải {len(cot_tho)} ô")
            ds = DONG_DAU_SHEET + i
            if m == 1:
                d_tt, cdt1, thang, no, vendor, itl, pe, u, v, f, s = h
                if _rong(vendor):             # hàng ĐỆM: 5 cột phân bổ phải rỗng *(U/V đệm ⛔ kiểm)*
                    if not all(_rong(x) for x in (cdt1, thang, no, itl, pe)):   # F/S/U/V đệm: công thức đuôi, ⛔ kiểm
                        raise ValueError(f"hàng {i + 1}: Vendor ID rỗng nhưng cột phân bổ CÓ giá trị")
                    so_dem += 1
                    continue
                if la_o_loi(itl):
                    itl_loi.append({"dong_sheet": ds, "itl_id_tho": itl})
                pm, ghi = _pm(s, i)
                dong.append([ds, d_tt, cdt1, thang, no, vendor, None if _rong(itl) else itl, pe,
                             None if _rong(u) else u, None if _rong(v) else v, f, pm, ghi])
            elif m == 2:
                d_tt, cdt1, thang, vendor, pe, rate, u, v = h
                if _rong(vendor):
                    raise ValueError(f"hàng {i + 1}: Vendor ID RỖNG — MID2 ⛔ hàng đệm")
                dong.append([ds, d_tt, cdt1, thang, vendor, pe, rate,
                             None if _rong(u) else u, None if _rong(v) else v])
            else:
                if not _la_so(h[0]):          # `O` ⛔ số ⇒ ⛔ vào ảnh *(đếm ở `ngoai_anh`)*
                    so_ngoai += 1
                    continue
                pm, ghi = _pm(h[1], i)
                cdt = [None if _rong(x) else x for x in h[2:14]]
                dong.append([ds, h[0], pm, *cdt, None if _rong(h[16]) else h[16],
                             None if _rong(h[17]) else h[17], ghi])
        if m == 1:
            phu["dem"] = [{"so_dong": so_dem, "mo_ta": "hàng đệm đuôi công thức (Vendor ID rỗng)"}]
            phu["itl_id_loi"] = sorted(itl_loi, key=lambda x: x["dong_sheet"])
        if m == 3:
            phu["ngoai_anh"] = [{"so_dong": so_ngoai, "mo_ta": "hàng O ⛔ là số — ⛔ vào ảnh"}]
        if so == "omc":
            phu["nguon_nghi_loi"] = [{
                "ly_do": ("script OMC copy*Ledger_to_Report_Optimized() lỗi row[45] ngoài 30 cột "
                          "(AP §3.4.1): ⛔ đo được script ⇒ phạm vi = CẬN TRÊN = mọi hàng × mọi cột "
                          "đáp án của ảnh"),
                "hang": len(dong), "cot": COT_DAP_AN[m], "o": len(dong) * COT_DAP_AN[m]}]
        return {"cot": [KHOA, *cot_anh], "dong": dong, "phu": phu,
                "ghi_chu": (f"{len(dong)} hàng MID{m} {so.upper()} *(khoá dong_sheet)*; PM chữ "
                            f"`{CHU_TAY}` tách sang `pm_ghi_chu` *(⛔ hoá 0)*; ô lỗi `so!` giữ "
                            "NGUYÊN + phân bố ghim `LOI_MONG`. ⛔ mang cột PII.")}

    def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
        if not dong:
            raise ValueError("0 hàng đáp án — mẫu số 0, ⛔ nền xanh (Đ3)")
        vp: list[str] = []
        lac: list[str] = []
        dai: list[str] = []
        for d in dong:                                  # mã ∈ tập tham chiếu — TRÊN TẬP ĐẦY ĐỦ
            ds = d["dong_sheet"]
            vendor = _chu(d, "vendor")
            if "cdt1" in d and _chu(d, "cdt1") not in CDT1_7:
                vp.append(f"cdt1_la@{ds}")
            if not (vendor is None and m == 3) and not (
                    isinstance(vendor, str) and VENDOR_RE.fullmatch(vendor)):
                vp.append(f"vendor_la@{ds}")
            if m == 3 and vendor is not None and not VENDOR_RE.fullmatch(vendor):
                vp.append(f"vendor_la@{ds}")
        vp = sorted(set(vp))
        v_thang, dem, thieu_t = _kiem_thang(dong, do["thang"], co_khoa=(m == 3))
        vp += v_thang
        dai.append(_dai_thang(dem, thieu_t))
        if m == 1:
            for d in dong:
                ds = d["dong_sheet"]
                itl = d.get("itl_id")
                if itl is not None and not (isinstance(itl, dict) and (
                        ITL_ID_RE.fullmatch(itl["chu"]) or la_o_loi(itl["chu"]))):
                    vp.append(f"itl_la@{ds}")
                if d["f"] != d["pe"]:
                    vp.append(f"f_khac_pe@{ds}")          # thượng nguồn: T = ArrayFormula(F)
                if d["pm"] is not None and d["pm_ghi_chu"] is not None:
                    vp.append(f"pm_chu_sai@{ds}")
            n_chu = sum(1 for d in dong if d["pm_ghi_chu"] is not None)
            if n_chu != do["pm_chu"]:
                vp.append(f"pm_chu_lech@{n_chu}≠{do['pm_chu']}")
            dai.append(f"f == pe trên {len(dong)} hàng · PM chữ {n_chu}/{len(dong)} ô *(tách cột ghi chú)*")
        if m == 3:
            cot_pe = ("cvl_pe", "cor_pe", "shq1_pe", "csm_pe", "cah_pe", "asa_pe")
            cot_pm = ("cvl_pm", "cor_pm", "shq1_pm", "csm_pm", "cah_pm", "asa_pm")
            n_tong = sum(1 for d in dong if _chu(d, "vendor") is None)
            if n_tong != do["tong"] or n_tong != len(dem):
                vp.append(f"tong_lech@{n_tong}≠{do['tong']}")
            khac_pe = sum(1 for d in dong for c in ("pe", *cot_pe) if _dec(d[c]) != 0)
            khac_pm = sum(1 for d in dong for c in ("pm", *cot_pm)
                          if d[c] is not None and _dec(d[c]) != 0)
            for d in dong:
                ds = d["dong_sheet"]
                if abs(_dec(d["pe"]) - sum((_dec(d[c]) for c in cot_pe), Decimal(0))) > TOL:
                    lac.append(f"dong_sheet@{ds}")
                if d["pm"] is not None and abs(
                        _dec(d["pm"]) - sum((_dec(d[c]) for c in cot_pm), Decimal(0))) > TOL:
                    vp.append(f"sigma_pm_lech@{ds}")
            if len(lac) != do["lech_pe"]:
                vp.append(f"sigma_lech_dem@{len(lac)}≠{do['lech_pe']}")
            mau = len(dong) * 7
            dai.append(f"Σ chia = O/P trên {len(dong)} hàng · hàng PE lệch nguồn {len(lac)} *(mong "
                       f"{do['lech_pe']}; ghi `lac`)* · tổng-tháng {n_tong} *(mong {do['tong']})* · "
                       f"mẫu số từng vế — PE: {khac_pe}/{mau} ô ≠ 0"
                       + (" — vế này chưa đo được trên dữ liệu thật" if khac_pe == 0 else "")
                       + f" · PM: {khac_pm}/{mau} ô ≠ 0"
                       + (" — vế này chưa đo được trên dữ liệu thật" if khac_pm == 0 else ""))
        return {"thieu": vp, "lac": lac, "dai": f"{ten}: " + " · ".join(dai)}

    out: dict[str, Any] = dict(
        BANG=f"PD.508-510.{so.upper()}.MID{m}", KHOA=KHOA, KIEU_KHOA=KIEU_KHOA, COT=cot_anh,
        KIEU_COT=KIEU[m], RA=f"tests/fixture/dap_an/{ten}.json", PHU_MONG=phu_mong,
        chuan_bi=chuan_bi, thieu_lac=thieu_lac)
    if "loi" in do:
        out["LOI_MONG"] = do["loi"]
    return out
