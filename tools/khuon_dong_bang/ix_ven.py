"""Khuôn đóng băng `ix_ven` — ẢNH IX.VEN Block 1 *(Vendor & Network Mapping, PD 503)* + cột
`cach_tinh` *(ISP 3.1.2 · DT8 · `WO-147` AC-1)*.

    python tools/dong_bang_sheet.py ix_ven <bản_thô.json> --mong 36
        ⇒ tests/fixture/cau_hinh/ix_ven.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.2.2 *(IX.VEN)* · §3.2.4 *(dòng "block 7 dòng CDT1 … block
36 dòng MID3" và "VD341 · VD444 · VD428 · 'Max' · VD62 tính riêng")* · §3.4.1 PD 503. `Vendor &
Network Mapping` *(sổ GI · OMC)* có **Block 1 = 36 dòng** *(vùng `M:S` hàng sheet 4–39)* ánh xạ
`Vendor ↔ Network ↔ Account ↔ %`; script `MappingBlock2.gs` nhân **× 7 CDT1**. Năm nhóm vendor
*(VD341 · VD444 · VD428 · 'Max' · VD62)* **tính riêng gõ cứng trong công thức** của CFA1/MID *(PD
504 "VD444 · VD341 · VD428 · 'Max' tính riêng")* ⇒ engine TO-BE *(H10)* phải đọc từ config, ⛔ gõ
lại. Bước C9 nạp ảnh này; H9/H10 tiêu thụ cột `cach_tinh`.

Hợp đồng bản thô *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI SA của `M:S`**,
hình `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day")` — bảy
    cột Block 1 *(M No/Vendor · N Vendor ID · O Network · P Account · Q % · R Cash-in +Month · S
    Cash-in Day)*. ⛔ cột nào khác — vùng đọc CHỈ `M:S` *(⛔ phủ cột PII/khác)*.
  · `values` = **36 hàng** *(sheet 4…39)* theo thứ tự sheet, mỗi hàng 7 ô.
  · `dong_dau_sheet` = **4** *(Block 1 bắt đầu hàng sheet 4; hàng 3 là tiêu đề)*.

⭐ **Hai quyết định của bước** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **`cach_tinh` = NHÃN phép tính riêng, SUY tại `chuan_bi`** *(⛔ đọc từ sheet — AP khai 5 nhóm
    ở §3.2.4, ⛔ ở một cột)*. Mỗi hàng:
      · Network `O == 'Max'` ⇒ `'Max'` *(Max Mediation gộp 1/12 — 12 hàng sheet 10–21)*;
      · ngược lại Vendor `N ∈ {VD341, VD444, VD428, VD62}` ⇒ chính mã ấy;
      · ngược lại `'thường'`.
    Network đi TRƯỚC *(VD62 nằm cả dưới Max hàng 21 lẫn đứng riêng hàng 34 — hàng 21 thuộc gộp
    Max)*. Đo 18/11 trên 36 hàng: **5** nhãn ≠ `thường` = `{Max, VD341, VD428, VD444, VD62}`
    *(Max 12 · VD341 6 · VD444 8 · VD428 3 · VD62 1 · thường 6)*.

  ② **Cổng = `thieu_lac`** *(Đ5: khai `mong`, NO cả hai chiều)*. Tập nhãn ≠ `thường` PHẢI đúng
    `{Max, VD341, VD428, VD444, VD62}`. Thiếu một nhãn *(vendor đổi mã ⇒ lọt)* hoặc thừa một nhãn
    *(mã lạ hoá đặc biệt)* ⇒ `thieu` ⇒ ĐỎ. `lac` = 5 nhãn ấy *(ghi nhận, ⛔ đỏ)*.
"""
from __future__ import annotations

from typing import Any

BANG = "IX.VEN"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
#: Thứ tự cột ảnh = khoá `dong_sheet` + 7 cột Block 1 + `cach_tinh` *(①)*. ⛔ thêm cột.
COT = ("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day", "cach_tinh")
#: `vendor` = mã CHỮ ⛔ rỗng · `network`/`account` = chữ HOẶC rỗng *(hàng 32–39 trống)* · `pct` =
#: số HOẶC rỗng · `cach_tinh` = nhãn CHỮ ⛔ rỗng *(luôn có — 'thường' hay nhãn riêng)*. `No`/
#: `cashin_month`/`cashin_day` ⛔ khai ⇒ `so` *(strict — đo 36/36 ô số)*.
KIEU_COT = {"vendor": "chu", "network": "chu?", "account": "chu?", "pct": "so?", "cach_tinh": "chu"}
RA = "tests/fixture/cau_hinh/ix_ven.json"

#: Cột của LƯỚI bản thô — vị trí cố định *(vùng `M:S`)*.
COT_THO = ("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day")
DONG_DAU_SHEET = 4
#: ⭐ 5 nhóm vendor tính riêng *(AP §3.2.2/§3.2.4; đo 18/11 — để bài ghim: khác tập ⇒ ĐỎ)*.
NHOM_RIENG = ("VD341", "VD428", "VD444", "VD62")   # 4 theo Vendor ID; 'Max' theo Network
NET_MAX = "Max"
MONG_RIENG = frozenset({"Max", "VD341", "VD428", "VD444", "VD62"})


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _cach_tinh(network: Any, vendor: Any) -> str:
    """Nhãn phép tính riêng của một hàng *(①)*. Network 'Max' đi TRƯỚC Vendor ID."""
    if isinstance(network, str) and network.strip() == NET_MAX:
        return NET_MAX
    if isinstance(vendor, str) and vendor.strip() in NHOM_RIENG:
        return vendor.strip()
    return "thường"


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI `M:S` → bảng `{dong_sheet, No, vendor, network, account, pct, cashin_*, cach_tinh}`.
    ⛔ lời lỗi mang giá trị ô *(cột `account` là Tên tài khoản — owner GIỮ, nhưng ⛔ in ra)*;
    `ValueError` ⇒ TỪ CHỐI."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(vùng M:S Block 1)*")
    dau = tho.get("dong_dau_sheet")
    if dau != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET} *(Block 1 từ hàng sheet 4)*")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng Block 1 ⛔ rỗng")

    dong: list[list[Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ M:S)*")
        No, vendor, network, account, pct, cm, cd = h
        if _rong(vendor):
            raise ValueError(f"hàng {i + 1}: cột Vendor ID *(N)* RỖNG — Block 1 mỗi hàng phải có mã")
        ds = DONG_DAU_SHEET + i
        # ô rỗng ("" | null) chuẩn hoá về null *(ảnh tất định)*.
        row = [ds, No,
               vendor.strip() if isinstance(vendor, str) else vendor,
               None if _rong(network) else network,
               None if _rong(account) else account,
               None if _rong(pct) else pct,
               cm, cd,
               _cach_tinh(network, vendor)]
        dong.append(row)

    rieng = sorted({r[8] for r in dong if r[8] != "thường"})
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"Block 1 = {len(dong)} hàng *(sheet {DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1})* "
            f"vùng M:S; MappingBlock2.gs nhân × 7 CDT1 *(C9/H9 tiêu thụ)*. Cột `cach_tinh` SUY "
            f"*(⛔ đọc từ sheet)*: Network 'Max' ⇒ 'Max', ngược lại Vendor ∈ {list(NHOM_RIENG)} ⇒ "
            f"chính mã, ngược lại 'thường'. {len(rieng)} nhãn riêng = {rieng} *(mong "
            f"{sorted(MONG_RIENG)}; khác ⇒ cổng ĐỎ)*. Cột `account` = Tên tài khoản *(owner GIỮ "
            f"11/09 — chỉ 'Email Address' bị cấm)*. ⛔ mang cột ngoài M:S."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng NHÓM RIÊNG *(②)*: tập nhãn `cach_tinh` ≠ 'thường' ↔ `MONG_RIENG`.

    `thieu` = nhãn trong `MONG_RIENG` mà ảnh KHÔNG có **+** nhãn ảnh CÓ mà ⛔ thuộc `MONG_RIENG`
    *(cả hai chiều — Đ5)*; khớp hết ⇒ `thieu = []`. `lac` = 5 nhãn mong *(ghi nhận, ⛔ đỏ)*.
    """
    thuc = {d["cach_tinh"]["chu"] for d in dong
            if isinstance(d.get("cach_tinh"), dict) and d["cach_tinh"]["chu"] != "thường"}
    thieu = sorted((MONG_RIENG - thuc) | (thuc - MONG_RIENG))
    lac = sorted(MONG_RIENG)
    return {
        "thieu": thieu,
        "lac": lac,
        "dai": (f"{len(thuc & MONG_RIENG)}/{len(MONG_RIENG)} nhóm riêng khớp · "
                f"thiếu {sorted(MONG_RIENG - thuc)} · thừa {sorted(thuc - MONG_RIENG)} · "
                f"'Max' theo Network, 4 mã theo Vendor ID"),
    }
