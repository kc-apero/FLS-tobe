"""Khuôn đóng băng `gi_mid1` — ĐÁP ÁN MID1 của GI *(`CFA2 | MID 1 | GI Allocated Ledger`, PD
505)* *(ISP 3.1.2 · DT8 · `WO-147` AC-2 · AC-3 · AC-4)*.

    python tools/dong_bang_sheet.py gi_mid1 <bản_thô.json> --mong 2856
        ⇒ tests/fixture/dap_an/gi_mid1.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.4.1 PD 505. MID1 là bước phân bổ GI đầu: mỗi dòng CFA1
*(Vendor × tháng × No)* **chia 7 CDT1** *(block 7 dòng gõ cứng — PD 505)*, mang `PE Amount` theo
CDT1. Ảnh đóng băng các dòng phân bổ ấy *(khoá `dong_sheet`)* để H9/H10 đối chiếu, bỏ MỌI cột PII
*(vùng đọc ⛔ phủ `A:C` = Ngày/Số chứng từ/Diễn giải · `G` Tài khoản · `N:O` File đính kèm)*.

Hợp đồng bản thô *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI SA bảy cột
KHÔNG PII** `D,J,K,Q,M,R,T,U,V`, hình `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot,
values}`:
  · `cot` = `("D","J","K","Q","M","R","T","U","V")` — `D` Đơn vị tiền tệ · `J` Chủ dự toán *(CDT1)* ·
    `K` Thời điểm bắt đầu *(yyyymm)* · `Q` No Transactions Per Vendor · `M` Mã đối tác *(Vendor
    ID)* · `R` ITL ID · `T` PE Amount *(allocate)* ·
    `U` MID · `V` Final *(đáp án MID của nguồn — `so!`, ④)*.
  · `values` = hàng dữ liệu sheet *(10…)* theo thứ tự; `dong_dau_sheet` = **10**.

⭐ **Ba quyết định của bước** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **Lọc hàng THẬT, đếm hàng ĐỆM** *(AC-5: ⛔ bỏ sót im lặng)*. Đo 18/11: **2.856** hàng có Vendor
    ID *(M)* ⇒ dòng phân bổ thật; **4.494** hàng ĐỆM *(M rỗng — đuôi công thức, mọi cột KHÁC cũng
    rỗng)*. `chuan_bi` giữ 2.856 hàng *(khoá `dong_sheet` = hàng sheet thật)*, khai 4.494 ở bảng
    phụ `dem` *(vào checksum)* và đòi mọi cột của chúng RỖNG *(bằng chứng ⛔ phải dòng phân bổ)*.

  ② **`R` ITL ID: `#N/A` GHI NGUYÊN + ĐẾM** *(AC-3 · `DT5-R1-04`)*. Đo 18/11: **176** hàng `R` =
    `#N/A (Did not find value '…' in VLOOKUP…)` *(VLOOKUP ⛔ tra được)* · 232 hàng `ITL#…` · 2.448
    rỗng. `R` = `chu?` *(chuỗi lỗi giữ NGUYÊN trong cột, ⛔ hoá 0)*; 176 hàng `#N/A` liệt kê ở bảng
    phụ `itl_id_loi` *(dong_sheet + chuỗi thô; mong 176 — khác ⇒ ĐỎ)*.

  ③ **Cổng `mã ∈ tập tham chiếu` ĐO TRÊN TẬP ĐẦY ĐỦ** *(AC-4 · `DT5-R1-01`: ⛔ tập con thưa)* =
    `thieu_lac`. MỌI hàng: `cdt1 (J) ∈ CDT1_7` · `vendor (M)` khớp `VD[0-9]+` · `itl_id (R)` khớp
    `ITL#[0-9]+` HOẶC lỗi Sheets HOẶC rỗng. Một mã lạ *(Diễn giải lạc cột, CDT1 sai)* ⇒ `thieu`
    ⇒ ĐỎ. MONG lệch = 0.

  ④ **`U`/`V` = `so!` + PHÂN BỐ lỗi ghim** *(vòng sửa `DT8-R1-04` · `AC-3`)*. Đo 18/11 trên **2.856
    hàng ảnh** *(⛔ cả lưới: `U` toàn lưới còn 4.636 `#DIV/0!` ở 4.494 hàng ĐỆM ⇒ ngoài ảnh)*:
    `U` = 946 số · 372 rỗng · `#VALUE!` **754** · `#DIV/0!` **784**; `V` = 1.178 số · 165 rỗng ·
    `#VALUE!` **733** · `#DIV/0!` **780**. `#REF!` = 0, `#N/A` = 0 ở `U`/`V` *(⇒ câu "U3 `#REF!`"
    của ISP ⛔ khớp nguồn — errata)*. `LOI_MONG` khai PHÂN BỐ theo LOẠI lỗi *(Đ5: đổi loại giữ
    nguyên tổng cũng ĐỎ)*.
"""
from __future__ import annotations

import re
from typing import Any

from fls.canon.o_loi import la_o_loi      # ô lỗi = tập ĐÓNG, 1 bản khai *(⛔ so bằng tiền tố '#')*

BANG = "PD.505"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("currency", "cdt1", "thang", "no", "vendor", "itl_id", "pe", "u", "v")
#: `currency`/`cdt1`/`vendor` = chữ ⛔ rỗng · `itl_id` = chữ HOẶC rỗng *(giữ `#N/A` thô — ②)* ·
#: `pe` = số HOẶC rỗng *(77 hàng PE rỗng — đo 18/11)*. `thang`/`no` ⛔ khai ⇒ `so` strict.
KIEU_COT = {"currency": "chu", "cdt1": "chu", "vendor": "chu", "itl_id": "chu?", "pe": "so?",
            "u": "so!", "v": "so!"}
#: Đ5 *(④)*: PHÂN BỐ lỗi `U`/`V` MONG *(đo 18/11, 2.856 hàng ảnh)* — khác ⇒ ĐỎ cả tổng LẪN loại.
LOI_MONG = {"u": {"#VALUE!": 754, "#DIV/0!": 784}, "v": {"#VALUE!": 733, "#DIV/0!": 780}}
RA = "tests/fixture/dap_an/gi_mid1.json"
#: Bảng phụ: `dem` *(1 dòng — số hàng đệm ①)* · `itl_id_loi` *(176 hàng `#N/A` ②)*.
PHU_MONG = {"dem": 1, "itl_id_loi": 176}

COT_THO = ("D", "J", "K", "Q", "M", "R", "T", "U", "V")
DONG_DAU_SHEET = 10
#: ⭐ 7 CDT1 — tập tham chiếu ĐÓNG *(đo 18/11: MID1 408 hàng/CDT1 × 7; khác ⇒ ĐỎ — AC-4)*.
CDT1_7 = frozenset({
    "SHQ2 | Headquarters2", "CVL | VisionLab", "COR | TeraSofts", "SHQ1 | Headquarters1",
    "CSM | SuperMinds", "CAH | Astronex", "ASA | Super App"})
VENDOR_RE = re.compile(r"VD[0-9]+")
ITL_ID_RE = re.compile(r"ITL#[0-9]+")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI `D,J,K,Q,M,R,T` → bảng hàng phân bổ thật + bảng phụ `dem`/`itl_id_loi` *(①②)*.
    ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒ TỪ CHỐI."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(cột KHÔNG PII; ⛔ phủ A:C,G,N:O)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng MID1 ⛔ rỗng")

    dong: list[list[Any]] = []
    so_dem = 0
    itl_loi: list[dict[str, Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ D,J,K,Q,M,R,T,U,V)*")
        d_tt, cdt1, thang, no, vendor, itl, pe, u, v = h
        ds = DONG_DAU_SHEET + i
        if _rong(vendor):                      # hàng ĐỆM — cột phân bổ phải rỗng (①)
            # `U`/`V` ở hàng đệm ⛔ kiểm *(đo: 4.636 `#DIV/0!` của `U` nằm ở đây — ngoài ảnh, ④)*.
            # `D` *(Đơn vị tiền tệ)* có thể còn 'USD' do công thức *(đo 18/11: 2.565/4.494)* —
            #   bằng chứng hàng đệm là 5 cột PHÂN BỔ rỗng: cdt1 · thang · no · itl · pe.
            if not all(_rong(x) for x in (cdt1, thang, no, itl, pe)):
                raise ValueError(f"hàng {i + 1}: Vendor ID rỗng nhưng cột phân bổ CÓ giá trị — "
                                 "⛔ phải hàng đệm; ⛔ dám bỏ")
            so_dem += 1
            continue
        if la_o_loi(itl):                      # ô lỗi Sheets *(tập đóng — ⛔ "#…" gõ tay)*
            itl_loi.append({"dong_sheet": ds, "itl_id_tho": itl})
        dong.append([ds, d_tt, cdt1, thang, no, vendor,
                     None if _rong(itl) else itl, None if _rong(pe) else pe,
                     None if _rong(u) else u, None if _rong(v) else v])

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {
            "dem": [{"so_dong": so_dem, "mo_ta": "hàng đệm đuôi công thức (Vendor ID rỗng, mọi cột rỗng)"}],
            "itl_id_loi": sorted(itl_loi, key=lambda x: x["dong_sheet"]),
        },
        "ghi_chu": (
            f"{len(dong)} hàng phân bổ MID1 *(có Vendor ID)*, khoá dong_sheet; {so_dem} hàng đệm "
            f"*(bảng phụ `dem`)*. Mỗi hàng chia 7 CDT1 mang PE Amount (T) + MID (U) · Final (V) dạng `so!` *(lỗi giữ nguyên, phân bố ghim ở `loi_mong`)*. `R` ITL ID giữ `#N/A` "
            f"thô *(⛔ hoá 0)*; {len(itl_loi)} hàng `#N/A` ở bảng phụ `itl_id_loi` *(mong 176)*. "
            f"Cổng `mã ∈ tập tham chiếu` *(cdt1 ∈ 7 CDT1 · vendor VD… · itl_id ITL#…/lỗi/rỗng)* "
            f"ĐO TRÊN {len(dong)} hàng ở `thieu_lac`. ⛔ mang cột A:C (Ngày/Số CT/Diễn giải) · G "
            f"(Tài khoản) · N:O (File đính kèm) — PII."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng `mã ∈ tập tham chiếu` ĐO TRÊN TẬP ĐẦY ĐỦ *(③ · AC-4)*.

    `thieu` = nhãn vi phạm *(`cdt1_la@ds` · `vendor_la@ds` · `itl_la@ds`)*; MONG = 0. Tập rỗng ⇒
    `ValueError` *(Đ3)*. `lac` = [].
    """
    if not dong:
        raise ValueError("0 hàng phân bổ — mẫu số 0, ⛔ nền xanh (Đ3)")

    def chu(d: dict, c: str) -> str | None:
        v = d.get(c)
        return v["chu"] if isinstance(v, dict) else None

    vp: list[str] = []
    for d in dong:
        ds = d["dong_sheet"]
        cdt1 = chu(d, "cdt1")
        if cdt1 not in CDT1_7:
            vp.append(f"cdt1_la@{ds}")
        vendor = chu(d, "vendor")
        if not (isinstance(vendor, str) and VENDOR_RE.fullmatch(vendor)):
            vp.append(f"vendor_la@{ds}")
        itl = d.get("itl_id")
        if itl is not None:                    # rỗng cho phép; chữ phải ITL#… hoặc lỗi Sheets
            s = itl["chu"] if isinstance(itl, dict) else None
            if not (isinstance(s, str) and (ITL_ID_RE.fullmatch(s) or la_o_loi(s))):
                vp.append(f"itl_la@{ds}")
    return {
        "thieu": sorted(vp),
        "lac": [],
        "dai": (f"mã ∈ tập tham chiếu trên {len(dong)} hàng *(ĐẦY ĐỦ — ⛔ tập con)*: "
                f"cdt1 ∈ {len(CDT1_7)} CDT1 · vendor VD… · itl_id ITL#…/lỗi/rỗng · vi phạm {len(vp)}"),
    }
