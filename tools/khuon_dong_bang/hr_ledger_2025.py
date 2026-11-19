"""Khuôn đóng băng `hr_ledger_2025` — ĐẦU VÀO Y2025 của sổ HR *(ISP 3.1.2 · DT6c · `WO-249` AC-1)*.

    python tools/dong_bang_sheet.py hr_ledger_2025 <bản_thô.json> --mong 10105
        ⇒ tests/fixture/dau_vao/hr_ledger_2025.json

⭐ **MỞ RỘNG `hr_ledger_2024`** *(⛔ chép)*: GỌI `chuan_bi_chung`/`thieu_lac_chung` của khuôn 2024 — cùng 9 cột
`A·D·E·F·G·H·S·T·AG`, cùng cách che, cùng khoá `dong_sheet` *(PIT `+100000`)*; ảnh 2024 giữ TỪNG BYTE.

⭐ **Nguồn** file GỐC `H1000 Ledger (APERO-HR Allocate HD_FS1)` id `1YEyGxBYXaa6n4dX9_rWXoFn6NgJStTP2DKJd64ZAoD4`
*(CHỈ-ĐỌC)* — hai tab: `1.3 Ledger NIS/INT/COM 2025` *(7.585 hàng, hàng 4…7588)* · `1.3 Ledger PIT 2025`
*(2.520 hàng)*. Đo 19/11: cột `A` là serial NGÀY ở **10.105/10.105** *(0 hàng rỗng · 0 hàng có nội dung mà thiếu
ngày)*; kỳ NIS 2025-01…2025-12 · PIT 2025-04 · 07 · 10 *(quý)*.

⛔ **KHÔNG đọc tab `… 2026`** *(đo 19/11)*: NIS 2026 có 588 hàng ở kỳ **2026-10 · 2026-11** *(0 hàng 2026-01)*; PIT 2026
có 293 hàng mà cột `A` ⛔ phải số ngày. ⇒ kỳ 2026-01 của `gl_hr_408` **KHÔNG có đầu vào** ở file nguồn.

⭐ Khác Y2024 *(đo 19/11, mỗi số đếm MỘT vật)*: **9** ô `F` của tab NIS là số LẺ *(phân bổ chia — `gl_hr_408` cũng giữ
phần lẻ)* ⇒ `cho_so_le=True`, Σ bằng `Decimal`; **1** ô `LE = #N/A` *(hàng sheet NIS 7430)* ⇒ nới tập đóng LE thêm
`#N/A`, cổng ĐẾM RIÊNG `MONG_LE_NA = 1`; **9** ô `H` mang số tài khoản ⇒ CHE về `R` *(`MONG_H_R = 9`)*.

⛔⛔ **Riêng tư** như `hr_ledger_2024`: ⛔ `B` Số chứng từ · `C` Diễn giải · `I·J·K` · `M…R`; lời lỗi ⛔ in giá trị.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from decimal import Decimal
from typing import Any

_P = pathlib.Path(__file__).resolve().parent / "hr_ledger_2024.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang_hr_ledger_2024", _P)
_y24 = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _y24
if not hasattr(_y24, "chuan_bi_chung"):
    _spec.loader.exec_module(_y24)

BANG = "HR.Ledger.2025"
KHOA = _y24.KHOA
KIEU_KHOA = _y24.KIEU_KHOA
COT = _y24.COT
KIEU_COT = _y24.KIEU_COT
RA = "tests/fixture/dau_vao/hr_ledger_2025.json"
PHU_MONG = {"tong_ky": 15}

TABS = ("1.3 Ledger NIS/INT/COM 2025", "1.3 Ledger PIT 2025")
TEN_TAB = {TABS[0]: "NIS", TABS[1]: "PIT"}
COT_THO = _y24.COT_THO
TIEU_DE = _y24.TIEU_DE
CHU = _y24.CHU
#: Tập đóng như 2024, LE nới `#N/A` *(đếm riêng — `MONG_LE_NA`)*.
TAP_DONG = {**_y24.TAP_DONG, "le": tuple(_y24.TAP_DONG["le"]) + ("#N/A",)}

#: Đ5 — đo 19/11 *(hàng sheet có ngày, theo tab × kỳ; tổng 7.585 + 2.520 = 10.105)*.
MONG_TAB_KY = {("NIS", 202501): 225, ("NIS", 202502): 668, ("NIS", 202503): 629, ("NIS", 202504): 579,
               ("NIS", 202505): 365, ("NIS", 202506): 916, ("NIS", 202507): 850, ("NIS", 202508): 767,
               ("NIS", 202509): 912, ("NIS", 202510): 868, ("NIS", 202511): 478, ("NIS", 202512): 328,
               ("PIT", 202504): 462, ("PIT", 202507): 835, ("PIT", 202510): 1223}
#: Đ5 — Σ PS Có *(cột F, VND, `Decimal` dạng chuỗi — có phần lẻ)* mỗi kỳ, gộp hai tab.
MONG_F_KY = {202501: "321317500", 202502: "5745812541", 202503: "5971078533", 202504: "7967090891",
             202505: "6623088442", 202506: "7642967845.363", 202507: "9712306163.707232147",
             202508: "7862221681", 202509: "8241418295", 202510: "11751792973", 202511: "7356669375",
             202512: "7332731464"}
MONG_H_R = 9
MONG_LE_NA = 1


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    return _y24.chuan_bi_chung(tho, tabs_mong=TABS, ten_tab=TEN_TAB, nam="2025", cho_so_le=True)


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    return _y24.thieu_lac_chung(dong, mong_tab_ky=MONG_TAB_KY,
                                mong_f_ky={k: Decimal(v) for k, v in MONG_F_KY.items()}, mong_h_r=MONG_H_R,
                                tap_dong=TAP_DONG, nam="2025", mong_le_na=MONG_LE_NA)
