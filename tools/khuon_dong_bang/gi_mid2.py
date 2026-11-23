"""Khuôn đóng băng `gi_mid2` — ĐÁP ÁN MID2 của GI *(`CFA2 | MID 2 | GI Allocated Ledger`, PD
506)* + cột `rate` `so!` *(ISP 3.1.2 · DT8 · `WO-147` AC-2 · AC-3 · AC-4)*.

    python tools/dong_bang_sheet.py gi_mid2 <bản_thô.json> --mong 1463
        ⇒ tests/fixture/dap_an/gi_mid2.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.4.1 PD 506. MID2 tính `RATE ALLOCATE = PE_cdt / Σ PE 6
CDT1 theo Vendor-tháng`; MID3 dùng RATE × O / × P. Ảnh đóng băng RATE + PE *(khoá `dong_sheet`)*,
bỏ MỌI cột PII *(vùng đọc ⛔ phủ `A:C` · `G` · `N:O`)*.

Hợp đồng bản thô *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI SA sáu cột
KHÔNG PII** `D,J,K,M,T,AA,U,V`, hình `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot,
values}`:
  · `cot` = `("D","J","K","M","T","AA","U","V")` — `D` Đơn vị tiền tệ · `J` Chủ dự toán *(CDT1)* · `K`
    Thời điểm bắt đầu *(yyyymm)* · `M` Mã đối tác *(Vendor ID)* · `T` PE Amount · `AA` RATE ALLOCATE ·
    `U` MID · `V` Final *(`so!`, ③)*.
  · `values` = hàng dữ liệu sheet *(10…)*; `dong_dau_sheet` = **10**.

⭐ **Hai quyết định của bước** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **`AA` RATE = `so!` *(số HOẶC lỗi Sheets)*** *(AC-3 · `DT5-R1-04`)*. RATE = `PE_cdt / Σ PE` ⇒
    `#DIV/0!` khi Σ PE = 0 *(Vendor-tháng ⛔ doanh thu)*. Đo 18/11: **308** ô `#DIV/0! (Function
    DIVIDE parameter 2 cannot be zero.)` · 1.155 ô số. Ô lỗi GHI NGUYÊN chuỗi + ĐẾM + ghim phân bố
    ở `loi_theo_cot` *(⛔ hoá 0)*; `LOI_MONG = {"rate": 308}` *(Đ5: khác ⇒ ĐỎ cả hai chiều)*.

  ② **Cổng `mã ∈ tập tham chiếu` ĐO TRÊN TẬP ĐẦY ĐỦ** *(AC-4 · `DT5-R1-01`)* = `thieu_lac`. MỌI
    hàng: `cdt1 (J) ∈ CDT1_7` · `vendor (M)` khớp `VD[0-9]+`. Một mã lạ ⇒ `thieu` ⇒ ĐỎ. MONG = 0.
    *(1.463 hàng — đo 18/11: ⛔ hàng đệm, mọi hàng có Vendor ID.)*

  ③ **`U`/`V` = `so!` + PHÂN BỐ lỗi ghim** *(vòng sửa `DT8-R1-04`)*. Đo 18/11 trên 1.463 hàng:
    `U` = 189 rỗng · `#VALUE!` **1.008** · `#DIV/0!` **266** *(0 số)*; `V` y hệt. `#REF!` = 0,
    `#N/A` = 0 ⇒ câu "U3 `#REF!`" của ISP ⛔ khớp nguồn *(errata)*. `LOI_MONG` khai PHÂN BỐ theo
    LOẠI lỗi *(Đ5)*; `rate` giữ tổng 308.
"""
from __future__ import annotations

import re
from typing import Any

BANG = "PD.506"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("currency", "cdt1", "thang", "vendor", "pe", "rate", "u", "v")
#: `currency`/`cdt1`/`vendor` = chữ ⛔ rỗng · `pe` = `so` strict *(đo 1.463/1.463 số)* · `rate` =
#: `so!` *(số HOẶC lỗi Sheets — ①)*. `thang` ⛔ khai ⇒ `so` strict.
KIEU_COT = {"currency": "chu", "cdt1": "chu", "vendor": "chu", "pe": "so", "rate": "so!",
            "u": "so!", "v": "so!"}
RA = "tests/fixture/dap_an/gi_mid2.json"
#: Đ5: số ô lỗi MONG của cột `rate` *(đo 18/11: 308 × `#DIV/0!`)*; khác ⇒ cổng ĐỎ.
LOI_MONG = {"rate": 308, "u": {"#VALUE!": 1008, "#DIV/0!": 266},
            "v": {"#VALUE!": 1008, "#DIV/0!": 266}}

COT_THO = ("D", "J", "K", "M", "T", "AA", "U", "V")
DONG_DAU_SHEET = 10
#: ⭐ 7 CDT1 — tập tham chiếu ĐÓNG *(đo 18/11: MID2 209 hàng/CDT1 × 7; AC-4)*.
CDT1_7 = frozenset({
    "SHQ2 | Headquarters2", "CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1",
    "CSM | SuperMinds", "CAH | Astronex", "ASA | Super App"})
VENDOR_RE = re.compile(r"VD[0-9]+")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI `D,J,K,M,T,AA` → bảng hàng phân bổ MID2. ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒
    TỪ CHỐI. Ô RATE `#DIV/0!` giữ NGUYÊN *(công cụ gắn `so!`)* — ⛔ đổi, ⛔ hoá 0."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(cột KHÔNG PII; ⛔ phủ A:C,G,N:O)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng MID2 ⛔ rỗng")

    dong: list[list[Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ D,J,K,M,T,AA,U,V)*")
        d_tt, cdt1, thang, vendor, pe, rate, u, v = h
        if _rong(vendor):
            raise ValueError(f"hàng {i + 1}: Vendor ID RỖNG — MID2 ⛔ hàng đệm, mỗi hàng phải có mã")
        ds = DONG_DAU_SHEET + i
        dong.append([ds, d_tt, cdt1, thang, vendor, pe, rate,
                     None if _rong(u) else u, None if _rong(v) else v])

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"{len(dong)} hàng phân bổ MID2 *(mỗi hàng có Vendor ID — ⛔ hàng đệm)*, khoá "
            f"dong_sheet. `AA` RATE = `so!`: số HOẶC `#DIV/0!` *(Σ PE = 0)* giữ NGUYÊN + đếm + ghim "
            f"*(mong 308)*; `U`/`V` = `so!` ghim PHÂN BỐ lỗi *(`#VALUE!` 1008 · `#DIV/0!` 266 mỗi cột)*. Cổng `mã ∈ tập tham chiếu` *(cdt1 ∈ 7 CDT1 · vendor VD…)* ĐO TRÊN "
            f"{len(dong)} hàng ở `thieu_lac`. ⛔ mang cột A:C · G · N:O — PII."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng `mã ∈ tập tham chiếu` ĐO TRÊN TẬP ĐẦY ĐỦ *(② · AC-4)*.

    `thieu` = nhãn vi phạm *(`cdt1_la@ds` · `vendor_la@ds`)*; MONG = 0. Tập rỗng ⇒ `ValueError`
    *(Đ3)*. `lac` = [].
    """
    if not dong:
        raise ValueError("0 hàng phân bổ — mẫu số 0, ⛔ nền xanh (Đ3)")

    def chu(d: dict, c: str) -> str | None:
        v = d.get(c)
        return v["chu"] if isinstance(v, dict) else None

    vp: list[str] = []
    for d in dong:
        ds = d["dong_sheet"]
        if chu(d, "cdt1") not in CDT1_7:
            vp.append(f"cdt1_la@{ds}")
        vendor = chu(d, "vendor")
        if not (isinstance(vendor, str) and VENDOR_RE.fullmatch(vendor)):
            vp.append(f"vendor_la@{ds}")
    return {
        "thieu": sorted(vp),
        "lac": [],
        "dai": (f"mã ∈ tập tham chiếu trên {len(dong)} hàng *(ĐẦY ĐỦ)*: cdt1 ∈ {len(CDT1_7)} CDT1 "
                f"· vendor VD… · vi phạm {len(vp)}"),
    }
