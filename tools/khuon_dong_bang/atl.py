"""Khuôn đóng băng `atl` — ĐÁP ÁN ATL *(tab `Report I PLA3 Y H Q M | PM + HR | ATL` = PD 606; tab
`Allocation Table` = PD 604)* *(ISP 3.1.2 · Step 27 · DT10 · `WO-196` AC-3 · AC-4)*.

    python tools/dong_bang_sheet.py atl <bản_thô.json> --mong 829
        ⇒ tests/fixture/dap_an/atl.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.4.2 PD 604 · 606 *(SO.PLA3-ATL)*. ATL = P&L SAU phân bổ
theo KRF × kỳ. Nhưng AS-IS **chưa phân bổ**: ô `N1` (và 8 ô cùng hàng) ghi *"Cần add Formula Allocate
(hoặc để trống)"* ⇒ ảnh này là đáp án **khi cờ luật phân bổ TẮT** *(D2)*. Driver 2026 ⛔ có ở nguồn
*(xem `ix_drv`)* ⇒ **ATL 2026 chỉ đối chiếu khi cờ tắt (D2)**.

Nguồn *(`[COPY] Report I General Ledger | P&L Report`)*: tab ATL 1110×196 = cột `A` *(⛔ mang — số
tổng/nhãn)* · `B:F` nhãn `L1 L2 L3 L4 Period` · **10 khối năm × 19 cột** `Y · H1 · H2 · Q1…Q4 ·
M01…M12` *(2024…2033, `G:GJ`)*. **Ảnh chỉ mang 3 năm 2024 · 2025 · 2026 = 57 cột** `G:BK`; 7 khối
2027…2033 *(đo 18/11: 4 khối `#REF!` 84 ô mỗi khối — công thức trỏ khối chưa có)* ⛔ mang.

Hợp đồng bản thô *(phiên cloud DATA, khoá SA chỉ-đọc, ⛔ commit)*: `{nguon, doc_luc, cach_doc, cot,
dong_dau_sheet = 7, values, tieu_de, at604}` — `values` = lưới `B7:BK1110` *(62 cột)*; `tieu_de` =
`{nam, ky}` hàng 5–6 của `G:BK`; `at604` = lưới `C3:O35` của `Allocation Table` *(chỉ để ĐẾM
hàng/tháng — giá trị driver ở `ix_drv`)*.

⭐ **Bốn quyết định** *(mỗi cái một con số đo 18/11 — Đ3/Đ4/Đ5)*:

  ① **Chọn hàng dữ liệu** = hàng sheet `7…1030` có ≥ 1 ô KHÁC RỖNG ở 57 cột kỳ ⇒ **829** hàng *(sheet
    `8…1030`)*. Khối KIỂM *(sheet `1031…1110`, **80** hàng, 560 ô `#VALUE!` + 1.997 ô `TRUE/FALSE`)* ⇒
    bảng phụ `kiem` *(⛔ lẫn vào cột `so!` — bool ⛔ phải số)*. Bài đếm 829 *(`so_dong`)* là Đ4: **hàng
    sheet**, ⛔ KRF; số cột kỳ = 57.

  ② **Ô gạch `-`** = **120** ô *(5 hàng sheet 998–1002: AR · CP1.1 · CP1.2 · CP2 · CP3 × 24 cột = 12
    tháng 2024 + 12 tháng 2026)* — chuỗi `-` là định dạng kế toán của ô rỗng, ⛔ số ⇒ ra RỖNG ở bảng
    chính và được LIỆT KÊ ở bảng phụ `o_gach` *(⛔ mất im lặng)*.

  ③ **Cổng = `thieu_lac` — số hàng CÓ GIÁ TRỊ theo KỲ** *(Đ5, `MONG_KY`)*: với mỗi cột trong 57 cột,
    số hàng ô KHÁC RỖNG *(số hoặc lỗi)*: 2024 = 7×**824** *(Y·H1·H2·Q1…Q4)* + 12×**816** *(M01…M12)*;
    2025 = 19×**824**; 2026 = 7×**824** + 12×**816**. Khác ⇒ `thieu` có tên cột ⇒ ĐỎ *(HAI chiều — thêm
    một ô cũng ĐỎ)*. Tập rỗng ⇒ `ValueError` *(Đ3)*.

  ④ **Lỗi Sheets GHI NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố** *(`DT5-R1-04`)*: 2024 `Y` = **77**
    `#N/A` *(đuôi giải thích ghi nguyên)* · 2024 `Q1…Q4` = **21** `#VALUE!` mỗi cột. Số ô lỗi 161 =
    77 + 84; khối KIỂM thêm 560 `#VALUE!` ở bảng phụ.

⭐ **Bảng phụ** *(vào checksum)*: `kiem` 80 · `o_gach` 120 · `pd604_ky` 3 — số hàng CDT1 CÓ SỐ theo
tháng ở PD 604 *(GI = 0 ở 202501 rồi 7; NOEM = 7 cả 12 tháng — Đ3: `0` ở 202501 là KẾT QUẢ, MID3 ⛔ có
dòng `TOTAL 202501`)*.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

BANG = "SO.PLA3-ATL"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
NAM = (2024, 2025, 2026)
KY = ("y", "h1", "h2", "q1", "q2", "q3", "q4", *[f"m{m:02d}" for m in range(1, 13)])
COT_KY = tuple(f"y{n}_{k}" for n in NAM for k in KY)                 # 57
COT_NHAN = ("l1", "l2", "l3", "l4", "period")
COT = (*COT_NHAN, *COT_KY)
KIEU_COT = {**{c: "chu?" for c in COT_NHAN}, **{c: "so!" for c in COT_KY}}
RA = "tests/fixture/dap_an/atl.json"
PHU_MONG = {"kiem": 80, "o_gach": 120, "pd604_ky": 3}

#: ⭐ Số ô lỗi theo cột *(④ — Đ5: khác ⇒ ĐỎ)*; cột ⛔ khai = 0.
#: ⚠ Công cụ chung đòi KHAI MỌI cột `so!` *(khoá thiếu ⇒ `KeyError` ở dòng tổng kết)* ⇒ 53 cột còn lại
#: khai `0` rõ ràng *(không phải "quên")*.
_LOI_CO = {"y2024_y": {"#N/A": 77}, **{f"y2024_q{q}": {"#VALUE!": 21} for q in range(1, 5)}}
LOI_MONG = {c: _LOI_CO.get(c, 0) for c in COT_KY}

#: ⭐ ③ — số hàng KHÁC RỖNG theo cột, đo 18/11 trên 829 hàng *(đủ 57 cột)*.
_N7, _N12 = 824, 816
MONG_KY: dict[str, int] = {
    **{f"y2024_{k}": (_N7 if i < 7 else _N12) for i, k in enumerate(KY)},
    **{f"y2025_{k}": 824 for k in KY},
    **{f"y2026_{k}": (_N7 if i < 7 else _N12) for i, k in enumerate(KY)},
}

DONG_DAU = 7
DONG_CUOI_CHINH = 1030          # hàng sheet cuối của vùng dữ liệu; 1031…1110 = khối KIỂM
THANG = tuple(f"m{m:02d}" for m in range(1, 13))
DRIVER_604 = (("GI_PE", 5), ("GI_PM", 16), ("NOEM", 28))
CDT1_SHEET = ("CVL", "COR", "CSM", "CAH", "ASA", "SHQ1", "SHQ2")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _hop_le_tieu_de(td: Any) -> None:
    nam, ky = (td or {}).get("nam"), (td or {}).get("ky")
    mong_nam = [n for n in NAM for _ in range(19)]
    mong_ky = []
    for n in NAM:
        mong_ky += [n, "H1", "H2", "Q1", "Q2", "Q3", "Q4", *range(1, 13)]
    if nam != mong_nam or ky != mong_ky:
        raise ValueError("`tieu_de` ⛔ phải 3 khối năm 2024·2025·2026 × (Y H1 H2 Q1…Q4 M1…M12) "
                         "*(hàng 5–6, G:BK)*")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Lưới `B7:BK1110` → bảng 829 hàng + 3 bảng phụ. ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒ TỪ CHỐI."""
    cot = tho.get("cot")
    if not isinstance(cot, list) or cot[:5] != ["L1", "L2", "L3", "L4", "Period"] or len(cot) != 62:
        raise ValueError("`cot` phải 62 tên: `L1 L2 L3 L4 Period` + 57 cột kỳ *(vùng B:BK)*")
    if tho.get("dong_dau_sheet") != DONG_DAU:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU}")
    _hop_le_tieu_de(tho.get("tieu_de"))
    V = tho.get("values")
    if not isinstance(V, list) or len(V) != 1110 - DONG_DAU + 1 \
            or any(not isinstance(h, list) or len(h) != 62 for h in V):
        raise ValueError("`values` phải 1104 hàng × 62 cột *(B7:BK1110)*")

    dong: list[list[Any]] = []
    o_gach: list[dict[str, Any]] = []
    kiem: list[dict[str, Any]] = []
    for i, h in enumerate(V):
        ds = DONG_DAU + i
        if ds > DONG_CUOI_CHINH:
            if any(not _rong(x) for x in h[5:]):
                kiem.append({"dong_sheet": ds, **{c: v for c, v in zip(COT, [None if _rong(x) else x for x in h])}})
            continue
        if not any(not _rong(x) for x in h[5:]):
            continue
        cells = []
        for j, x in enumerate(h[5:]):
            if isinstance(x, str) and x.strip() == "-":
                o_gach.append({"dong_sheet": ds, "cot": COT_KY[j]})
                cells.append(None)
            else:
                cells.append(None if _rong(x) else x)
        dong.append([ds, *[None if _rong(x) else x for x in h[:5]], *cells])
    if not kiem:
        raise ValueError("khối KIỂM 1031…1110 rỗng — mẫu số 0 (Đ3)")

    # ── PD 604: số hàng CDT1 CÓ SỐ theo tháng ──
    at = tho.get("at604")
    if not isinstance(at, dict) or at.get("dong_dau_sheet") != 3 or not isinstance(at.get("values"), list) \
            or len(at["values"]) != 33 or any(not isinstance(h, list) or len(h) != 13 for h in at["values"]):
        raise ValueError("`at604` phải lưới `C3:O35` 33 hàng × 13 cột")
    pd604: list[dict[str, Any]] = []
    for driver, h0 in DRIVER_604:
        cnt = []
        for i in range(12):
            n = 0
            for k, cdt1 in enumerate(CDT1_SHEET):
                row = at["values"][h0 + k - 3]
                if str(row[0]).split("|")[0].strip() != cdt1:
                    raise ValueError(f"`at604` {driver}: hàng {h0 + k} nhãn ⛔ phải CDT1 `{cdt1}`")
                n += 0 if _rong(row[1 + i]) else 1
            cnt.append(n)
        pd604.append({"driver": driver, **{m: c for m, c in zip(THANG, cnt)}})

    return {
        "cot": ["dong_sheet", *COT],
        "dong": dong,
        "phu": {"kiem": kiem, "o_gach": o_gach, "pd604_ky": pd604},
        "ghi_chu": (
            f"ATL 606 = {len(dong)} hàng sheet 8…1030 × 57 cột kỳ (2024·2025·2026 × Y·H1·H2·Q1…Q4·M01…M12; "
            "G:BK) + nhãn L1…L4 · Period (B:F); khối KIỂM 1031…1110 ở bảng phụ `kiem` (80); "
            f"{len(o_gach)} ô gạch `-` ở `o_gach`; PD 604 = số hàng CDT1 có số theo tháng ở `pd604_ky`. AS-IS "
            "CHƯA phân bổ (ô N1 + 8 ô cùng hàng 'Cần add Formula Allocate') ⇒ đáp án đúng khi cờ luật TẮT; "
            "driver 2026 ⛔ có ở nguồn ⇒ ATL 2026 chỉ đối chiếu khi cờ tắt (D2). Cột A (số tổng) · 7 khối "
            "2027…2033 (4 khối #REF! 84 ô mỗi khối) ⛔ mang. Kích thước ảnh ≈ 1,6 MB (< 2 MB, luật DT4-R1-07): 829 hàng × 62 cột + khối KIỂM 80 × 62, mỗi ô một "
            "giá trị đóng băng nguyên chữ số."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng ATL *(③)*: số hàng KHÁC RỖNG theo từng cột kỳ ↔ `MONG_KY` *(Đ5 hai chiều)*.
    Tập rỗng ⇒ `ValueError` *(Đ3)*. `lac` = []."""
    if not dong:
        raise ValueError("0 hàng ATL — mẫu số 0, ⛔ nền xanh (Đ3)")
    thieu = []
    dem: dict[str, int] = {}
    for c in COT_KY:
        n = sum(1 for d in dong if d[c] is not None)
        dem[c] = n
        if n != MONG_KY[c]:
            thieu.append(f"{c}: {n}≠{MONG_KY[c]}")
    theo_nam = {y: (min(dem[f"y{y}_{k}"] for k in KY), max(dem[f"y{y}_{k}"] for k in KY)) for y in NAM}
    return {
        "thieu": thieu,
        "lac": [],
        "dai": (f"{len(dong)} hàng × {len(COT_KY)} cột kỳ · hàng có giá trị theo kỳ (min–max) " +
                " · ".join(f"{y}: {a}–{b}" for y, (a, b) in theo_nam.items()) +
                " · 2026 chỉ đối chiếu khi cờ tắt (D2)"),
    }
