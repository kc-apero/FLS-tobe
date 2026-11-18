"""Khuôn đóng băng `gi_cfa1` — ĐẦU VÀO GI `'CFA1 | GI Platform Data Ledger'` *(PD 504)* cho cổng
WP-C4a của H9 *(ISP 3.1.2 · DT8b · `WO-204` AC-2)*.

    python tools/dong_bang_sheet.py gi_cfa1 <bản_thô.json> --mong 408
        ⇒ tests/fixture/dau_vao/gi_cfa1.json

⭐ **Vì sao có khuôn này.** H9 *(`BG-201`)* dựng `chia_nen_tang` nhưng WP-C4a đo 0/616 ô vì ⛔ có O/P
theo Vendor-tháng: O *(PE Amount)* và P *(PM Amount)* chỉ nằm trong MID3 = ĐÁP ÁN. CFA1 là ĐẦU VÀO
của sổ: mỗi hàng = một giao dịch Vendor × tháng; Σ theo (Vendor, tháng) là O/P đưa vào RATE.

Hợp đồng bản thô = **LƯỚI SA** *(⛔ commit)* `{spreadsheet_id, nguon, doc_luc, cach_doc,
dong_dau_sheet, cot, values}`; `cot` = `("M","K","Q","T","S","R")` — đúng 6 cột KHÔNG PII, hàng sheet 10…417:
  · `M` *Mã đối tác (ID Payee)* = **vendor** · `K` *Thời điểm bắt đầu sử dụng dịch vụ* = **thang**
    `yyyymm` *(`L` = `K` trên 408/408 ⇒ ⛔ lấy)* · `Q` *No Transactions Per Vendor* = **no** ·
    `T` *PE Amount* = **pe** *(`E` PS Nợ = `T` = `U` trên 408/408 ⇒ ⛔ lấy)* · `S` *PM Amount* =
    **pm** · `R` *ITL ID* = **itl_id**.
  · ⛔ mang `A` Ngày CT · `B` Số CT · `C` Diễn giải · `G` Tài khoản · `H` Loại GD · `N/O` File đính
    kèm — PII/ngoài phạm vi. Bản đồ cột lập bằng hàng tiêu đề 7–8 TRƯỚC khi đọc.

⭐ **Ba quyết định** *(mỗi cái một con số đo 18/11 — Đ4)*:
  ① **`S` PM Amount lẫn chữ.** 408 hàng: **232** số `0` · **176** chữ `Need to manual input`
    *(cột `PIC` nhập tay — ⛔ hoá 0)*. Khuôn tách: `pm` = số *(`so?`)* hoặc rỗng; chữ ⇒ `pm_ghi_chu`
    *(`chu?`, chỉ chấp nhận đúng chuỗi ấy)*. ⇒ ⛔ có hàng nào PM ≠ 0: vế P của WP-C4a ở CFA1 = **0** *(kết quả, Đ3)*.
  ② **`R` ITL ID**: **232** `ITL#…` · **176** chữ `Ko tìm thấy` *(= đúng 176 `#N/A` của MID1 — cùng hàng)*;
    giữ NGUYÊN chữ *(⛔ hoá rỗng)*.
  ③ **Cổng `thieu_lac`** *(Đ5 hai chiều; ⛔ in giá trị ô — chỉ nhãn + `dong_sheet`)*: vendor khớp `VD[0-9]+`
    *(`vendor_la@`)* · tháng `yyyymm` hợp lệ *(`thang_la@`)* · `no` ∈ 1…12 *(`no_la@`)* · `pm_ghi_chu` đúng
    chuỗi khai *(`pm_chu_la@`)* · `itl_id` = `ITL#…` hoặc `Ko tìm thấy` *(`itl_la@`)* · **số dòng THEO THÁNG =
    `MONG_THANG`** *(`thang_lech@yyyymm`)* — khác cả hai chiều ⇒ ĐỎ; 9 tháng × 36 + 2 × 42 = 408.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any

BANG = "PD.504"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("vendor", "thang", "no", "pe", "pm", "pm_ghi_chu", "itl_id")
KIEU_COT = {"vendor": "chu", "thang": "so", "no": "so", "pe": "so", "pm": "so?",
            "pm_ghi_chu": "chu?", "itl_id": "chu"}
RA = "tests/fixture/dau_vao/gi_cfa1.json"

COT_THO = ("M", "K", "Q", "T", "S", "R")
DONG_DAU_SHEET = 10
VENDOR_RE = re.compile(r"VD[0-9]+")
THANG_RE = re.compile(r"20[0-9]{2}(0[1-9]|1[0-2])")
ITL_RE = re.compile(r"ITL#[0-9]+")
CHU_PM = "Need to manual input"
CHU_ITL = "Ko tìm thấy"
#: Đ5: số dòng MONG theo tháng *(đo 18/11: 202502…202510 = 36 · 202511 · 202512 = 42)*.
MONG_THANG = {**{str(t): 36 for t in range(202502, 202511)}, "202511": 42, "202512": 42}


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI `M,K,Q,T,S,R` → bảng 408 dòng. ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒ TỪ CHỐI."""
    if tho.get("cot") != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(6 cột KHÔNG PII; ⛔ phủ A:C · G · H · N:O)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng CFA1 ⛔ rỗng")
    dong: list[list[Any]] = []
    n_chu = 0
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ M,K,Q,T,S,R)*")
        vendor, thang, no, pe, pm, itl = h
        pm_so, pm_chu = (None, pm) if isinstance(pm, str) else (pm, None)   # ① chữ → pm_ghi_chu
        n_chu += pm_chu is not None
        dong.append([DONG_DAU_SHEET + i, vendor, thang, no, pe, pm_so, pm_chu, itl])
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"{len(dong)} hàng giao dịch CFA1 GI *(sheet 10…{DONG_DAU_SHEET + len(dong) - 1})*, khoá dong_sheet. "
            f"`PM Amount` (S): số hoặc chữ `{CHU_PM}` — chữ tách sang `pm_ghi_chu` ({n_chu} hàng, ⛔ hoá 0). "
            f"`thang` = K *(Thời điểm bắt đầu sử dụng; L = K)*, `pe` = T *(E = T = U)*. "
            f"⛔ mang cột A:C · G · H · N:O — PII/ngoài phạm vi."),
    }


def _u(v: Any) -> Any:
    return v.get("chu") if isinstance(v, dict) else v


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng ③ *(Đ5 hai chiều)*. Tập rỗng ⇒ `ValueError` *(Đ3)*. `lac` = []."""
    if not dong:
        raise ValueError("0 dòng CFA1 — mẫu số 0, ⛔ nền xanh (Đ3)")
    lech: list[str] = []
    dem = Counter()
    pm_khac0 = pm_chu = pe_khac0 = 0
    for d in dong:
        ds = d["dong_sheet"]
        v, t, no, pm, ghi, itl = (_u(d[c]) for c in ("vendor", "thang", "no", "pm", "pm_ghi_chu", "itl_id"))
        if not isinstance(v, str) or not VENDOR_RE.fullmatch(v):
            lech.append(f"vendor_la@{ds}")
        if not isinstance(t, str) or not THANG_RE.fullmatch(t):
            lech.append(f"thang_la@{ds}")
        else:
            dem[t] += 1
        if not isinstance(no, str) or not (no.isdigit() and 1 <= int(no) <= 12):
            lech.append(f"no_la@{ds}")
        if ghi is not None and ghi != CHU_PM:
            lech.append(f"pm_chu_la@{ds}")
        if not isinstance(itl, str) or not (ITL_RE.fullmatch(itl) or itl == CHU_ITL):
            lech.append(f"itl_la@{ds}")
        pm_chu += ghi is not None
        pm_khac0 += pm is not None and float(pm) != 0
        try:                                       # DT8B-R1-01: chữ ở cột số ⇒ nhãn CÓ TÊN, ⛔ TypeError, ⛔ lộ giá trị
            if isinstance(d["pe"], (dict, bool)):
                raise ValueError
            pe_khac0 += float(d["pe"]) != 0
        except (ValueError, TypeError):
            lech.append(f"pe_la@{ds}")
    for t in sorted(set(dem) | set(MONG_THANG)):
        if dem.get(t, 0) != MONG_THANG.get(t, 0):
            lech.append(f"thang_lech@{t}:{dem.get(t, 0)}≠{MONG_THANG.get(t, 0)}")
    return {
        "thieu": lech,
        "lac": [],
        "dai": (f"{len(dong)} dòng · {len(dem)} tháng *(mong {len(MONG_THANG)})* · dòng/tháng "
                f"{dict(sorted(dem.items()))} · PE ≠ 0: {pe_khac0}/{len(dong)} dòng · PM số ≠ 0: "
                f"{pm_khac0}/{len(dong) - pm_chu} dòng · PM chữ: {pm_chu}/{len(dong)} dòng"),
    }
