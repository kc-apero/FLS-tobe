"""Khuôn đóng băng `mid3_total` — ĐẦU VÀO của lá `GI · OMC · PS · SC` khối CDT ở ATL = hàng `TOTAL <yyyymm>` của bốn tab
`CFA2 | MID 3 | {GI,OMC,SC,PS} Platform Data Ledger` *(sổ `[COPY] Report I General Ledger | P&L Report`, id
`19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g`)* *(ISP 3.1.2 · DT13 · `WO-319` · `BG-292` §"Cần ảnh ①")*.

    python tools/dong_bang_sheet.py mid3_total <bản_thô.json> --mong 39
        ⇒ tests/fixture/dau_vao/mid3_total.json

⭐ **Vì sao.** ATL *(`Report I PLA3 Y H Q M | PM + HR | ATL`)* lấy lá khối CDT của `GI · OMC · PS · SC` từ hàng `TOTAL yyyymm` cột PM
theo CDT `T·V·X·Z·AB·AD` ÷ 10⁶ *(× −1 trừ GI)* — H12 đo khớp GI 66/66 · OMC 60/60 · SC 54/54 · PS 51/54. Ảnh `{gi,omc,sc,ps}_mid3`
đã đóng băng **⛔ mang hàng TOTAL** *(44 hàng ⛔ khoá `vendor/tháng`, ⛔ cột A)* ⇒ engine ⛔ dựng được lá. Đây là bản đóng băng **CHỈ các hàng
TOTAL** *(cột A khớp ĐÚNG `TOTAL <6 số>` ⇒ giữ; mọi giá trị khác của cột A = `Số chứng từ` ⛔ PII ⇒ ⛔ đọc vào ảnh)*.

⛔⛔ **Bản đồ cột bằng tiêu đề TRƯỚC** *(hàng 7–8 của tab; đo 22/11 cả 4 tab giống hệt ở `O…AD`)*: `O` `PE Amount` · `P` `PM Amount` ·
`S…AD` = 6 CDT × (`PE Amount`, `PM Amount`) theo thứ tự `CVL · COR · SHQ1 · CSM · CAH · ASA`. ⛔ `A…N` (Số chứng từ · Diễn giải · Tài khoản ·
Budget Code · Chủ dự toán · … · ID Payee · File đính kèm) và `Q·R` *(ngày)*. Hợp đồng bản thô *(phiên cloud, khoá SA chỉ-đọc, ⛔ commit)* —
⛔ chỉ MỘT dải hàng TOTAL: `{nguon, doc_luc, cach_doc, tieu_de, values}`; `tieu_de` = `{tab: [ô hàng 7 `O,P,S…AD` ×14, ô hàng 8 ×14]}`;
`values` = `[[tab, hàng_sheet, nhãn, O, P, S…AD]…]`.
"""
from __future__ import annotations

import re
from decimal import Decimal
from typing import Any

BANG = "DAU_VAO.MID3_TOTAL"
KHOA = "so_dong_sheet"
KIEU_KHOA = "so_dong_sheet"
RA = "tests/fixture/dau_vao/mid3_total.json"
TAB = ("GI", "OMC", "SC", "PS")
CDT = ("cvl", "cor", "shq1", "csm", "cah", "asa")
COT = ("tab", "thang", "pe", "pm", *[f"{c}_{k}" for c in CDT for k in ("pe", "pm")])
KIEU_COT = {"tab": "chu", "thang": "so", **{c: "so" for c in COT[2:]}}
PHU_MONG = {"tieu_de": 4 * 28}
_NHAN = re.compile(r"TOTAL ?([0-9]{4})(0[1-9]|1[0-2])")

#: tiêu đề hàng 7 *(`O,P` + 12 cột `S…AD` — tên CDT lặp 2 lần)* và hàng 8 *(`PE/PM Amount`)* — ⭐ BẢN ĐỒ CỘT bằng tiêu đề.
H7 = ("PE Amount", "PM Amount", *[x for t in ("CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1", "CSM | SuperMinds",
                                              "CAH | Astronex", "ASA | Super App") for x in (t, t)])
H8 = ("", "", *("PE Amount", "PM Amount") * 6)
#: ⭐ Đ5 — đo 22/11 rồi khai; khác ⇒ ĐỎ cả hai chiều. Số hàng TOTAL theo tab · tháng đầu/cuối.
MONG: dict[str, Any] = {
    "hang": {"GI": 11, "OMC": 10, "SC": 9, "PS": 9},
    "thang": {"GI": ("202502", "202512"), "OMC": ("202503", "202512"), "SC": ("202504", "202512"), "PS": ("202504", "202512")},
    "o_so": 39 * 14,
}


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    th, V = tho.get("tieu_de"), tho.get("values")
    if not isinstance(th, dict) or sorted(th) != sorted(TAB):
        raise ValueError(f"`tieu_de` phải khai đủ 4 tab {list(TAB)}")
    for t in TAB:
        h = th[t]
        if not (isinstance(h, list) and len(h) == 2 and [str(x).strip() for x in h[0]] == list(H7)
                and [str(x).strip() for x in h[1]] == list(H8)):
            raise ValueError(f"tab {t}: tiêu đề hàng 7–8 `O,P,S…AD` ⛔ đúng bản đồ cột đã đo")
    if not isinstance(V, list) or not V:
        raise ValueError("`values` phải danh sách hàng TOTAL ⛔ rỗng (Đ3)")
    dong: list[list[Any]] = []
    for i, h in enumerate(V):
        if not (isinstance(h, list) and len(h) == 3 + 14):
            raise ValueError(f"hàng {i + 1} phải 17 ô *(tab, hàng sheet, nhãn, 14 số)*")
        t, hs, nhan, *so = h
        m = _NHAN.fullmatch(str(nhan).strip()) if isinstance(nhan, str) else None
        if t not in TAB or not isinstance(hs, int) or hs < 1 or not m:
            raise ValueError(f"hàng {i + 1}: tab/hàng/nhãn ⛔ hợp lệ *(nhãn ⛔ in — chỉ nhận `TOTAL <yyyymm>`)*")
        dong.append([f"{t}!{hs}", t, int(m.group(1) + m.group(2)), *so])
    return {"cot": ["so_dong_sheet", *COT], "dong": dong,
            "phu": {"tieu_de": [{"tab": t, "hang": hh, "o": o, "gia_tri": g}
                                for t in TAB for hh, row in ((7, th[t][0]), (8, th[t][1]))
                                for o, g in zip(("O", "P", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"), row)]},
            "ghi_chu": (f"{len(dong)} hàng `TOTAL <yyyymm>` của 4 tab `CFA2 | MID 3 | {{GI,OMC,SC,PS}} Platform Data Ledger` × 14 cột số "
                        "(O PE · P PM · S…AD 6 CDT × PE/PM). ⛔ cột A khác nhãn TOTAL (Số chứng từ) · ⛔ A…N · Q·R. Hàng sheet ở khoá `<TAB>!<hàng>`.")}


def _u(v: Any) -> Any:
    return v["chu"] if isinstance(v, dict) else v


def do(dong: list[dict[str, Any]]) -> dict[str, Any]:
    hang = {t: sum(1 for d in dong if _u(d["tab"]) == t) for t in TAB}
    thang = {}
    for t in TAB:
        ms = sorted(str(d["thang"]) for d in dong if _u(d["tab"]) == t)
        thang[t] = (ms[0], ms[-1]) if ms else None
    o_so = sum(1 for d in dong for c in COT[2:] if d[c] is not None and not isinstance(d[c], dict))
    return {"hang": hang, "thang": thang, "o_so": o_so}


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng *(Đ5 hai chiều)*. Tập rỗng ⇒ `ValueError` *(Đ3)*; tab thiếu/thừa hàng, tháng lệch, ô ⛔ số ⇒ `thieu`."""
    if not dong:
        raise ValueError("0 hàng TOTAL — mẫu số 0, ⛔ nền xanh (Đ3)")
    d = do(dong)
    thieu = [f"{k}: đo {d[k]} ≠ mong {m}" for k, m in MONG.items() if d[k] != m]
    thang = [(_u(x["tab"]), x["thang"]) for x in dong]
    if len(set(thang)) != len(thang):
        thieu.append("thang_trung")
    return {"thieu": thieu, "lac": [],
            "dai": f"{len(dong)} hàng TOTAL · {d['hang']} · ô số {d['o_so']} (mong {MONG['o_so']})"}
