"""Khuôn đóng băng `ix_ven` — ẢNH IX.VEN Block 1 *(Vendor & Network Mapping, PD 503)* + cột
`cach_tinh` *(ISP 3.1.2 · DT8 · `WO-147` AC-1)*.

    python tools/dong_bang_sheet.py ix_ven <bản_thô.json> --mong 42
        ⇒ tests/fixture/cau_hinh/ix_ven.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.2.2 *(IX.VEN)* · §3.2.4 *(dòng "block 7 dòng CDT1 … block
36 dòng MID3" và "VD341 · VD444 · VD428 · 'Max' · VD62 tính riêng")* · §3.4.1 PD 503. `Vendor &
Network Mapping` *(sổ GI · OMC)* có **Block 1 = 42 dòng liền** *(vùng `M:S` hàng sheet 4–45;
AP ghi "36" = hàng 4–39 ⇒ **errata**, vòng sửa `DT8-R1-01`)* ánh xạ
`Vendor ↔ Network ↔ Account ↔ %`; script `MappingBlock2.gs` nhân **× 7 CDT1**. Năm nhóm vendor
*(VD341 · VD444 · VD428 · 'Max' · VD62)* **tính riêng gõ cứng trong công thức** của CFA1/MID *(PD
504 "VD444 · VD341 · VD428 · 'Max' tính riêng")* ⇒ engine TO-BE *(H10)* phải đọc từ config, ⛔ gõ
lại. Bước C9 nạp ảnh này; H9/H10 tiêu thụ cột `cach_tinh`.

Hợp đồng bản thô *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI SA của `M:S`**,
hình `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day")` — bảy
    cột Block 1 *(M No/Vendor · N Vendor ID · O Network · P Account · Q % · R Cash-in +Month · S
    Cash-in Day)*. ⛔ cột nào khác — vùng đọc CHỈ `M:S` *(⛔ phủ cột PII/khác)*.
  · `values` = **42 hàng** *(sheet 4…45)* theo thứ tự sheet, mỗi hàng 7 ô.
  · `dong_dau_sheet` = **4** *(Block 1 bắt đầu hàng sheet 4; hàng 3 là tiêu đề)*.

⭐ **Hai quyết định của bước** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **`cach_tinh` = NHÃN phép tính riêng, SUY tại `chuan_bi`** *(⛔ đọc từ sheet — AP khai 5 nhóm
    ở §3.2.4, ⛔ ở một cột)*. Mỗi hàng:
      · Network `O == 'Max'` ⇒ `'Max'` *(Max Mediation gộp 1/12 — 12 hàng sheet 10–21)*;
      · ngược lại Vendor `N ∈ {VD341, VD444, VD428, VD62}` ⇒ chính mã ấy;
      · ngược lại `'thường'`.
    Network đi TRƯỚC *(VD62 nằm cả dưới Max hàng 21 lẫn đứng riêng hàng 34 — hàng 21 thuộc gộp
    Max)*. Đo 18/11 trên **42 dòng**: **5** nhãn ≠ `thường` = `{Max, VD341, VD428, VD444, VD62}`
    *(số DÒNG mỗi nhãn: Max 12 · **VD341 12** · VD444 8 · VD428 3 · VD62 1 · thường 6 = 42)*.
    ⭐ `DT8-R1-01`: bản đầu cắt ở 36 dòng theo số AP ⇒ `VD341` chỉ `No` 1–6 trong khi nguồn
    **liền tiếp** hàng 40–45 *(`VD341` `No` 7–12, ⛔ hàng trống ngăn)* và `MID1` dùng tới `No` 12.
    Đo vùng `M3:S50`: hàng 46–50 **0** ô có dữ liệu ⇒ dải liền kết thúc ở hàng 45.

  ② **Cổng = `thieu_lac`** *(Đ5: khai `mong`, NO cả hai chiều)*. Tập nhãn ≠ `thường` PHẢI đúng
    `{Max, VD341, VD428, VD444, VD62}`. Thiếu một nhãn *(vendor đổi mã ⇒ lọt)* hoặc thừa một nhãn
    *(mã lạ hoá đặc biệt)* ⇒ `thieu` ⇒ ĐỎ. `lac` = 5 nhãn ấy *(ghi nhận, ⛔ đỏ)*.
"""
from __future__ import annotations

import re
from typing import Any

BANG = "IX.VEN"
KHOA = "dong_sheet"
KIEU_KHOA = "so_dong_sheet"      # DT9b: GI = `4`…`45` (NGUYÊN); OMC/SC/PS = `<SO>!<hàng>`
#: Thứ tự cột ảnh = khoá `dong_sheet` + 7 cột Block 1 + `cach_tinh` *(①)*. ⛔ thêm cột.
COT = ("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day", "cach_tinh", "so")
#: `vendor` = mã CHỮ ⛔ rỗng · `network`/`account` = chữ HOẶC rỗng *(hàng 32–39 trống)* · `pct` =
#: số HOẶC rỗng · `cach_tinh` = nhãn CHỮ ⛔ rỗng *(luôn có — 'thường' hay nhãn riêng)*. `No`/
#: `cashin_month`/`cashin_day` ⛔ khai ⇒ `so` *(strict — đo 36/36 ô số)*.
KIEU_COT = {"vendor": "chu", "network": "chu?", "account": "chu?", "pct": "so?", "cach_tinh": "chu",
            "so": "chu"}
RA = "tests/fixture/cau_hinh/ix_ven.json"

#: Cột của LƯỚI bản thô — vị trí cố định *(vùng `M:S`)*.
COT_THO = ("No", "vendor", "network", "account", "pct", "cashin_month", "cashin_day")
#: ⭐ DT9b: lưới nhiều sổ = 7 cột Block 1 + `so` *(GI · OMC · SC · PS)* + `hang` *(số hàng sheet ≥ 4 CỦA sổ ấy)*.
#: Lưới 7 cột cũ *(DT8)* vẫn đọc được = sổ GI, hàng `4 + i`. ⛔ `account` của OMC/SC/PS đọc *(tên người /
#: số TK)*; ⛔ `network` của SC/PS *(cột tên, ⛔ nhãn kênh)* — phiên DATA đưa `null`, khuôn ⛔ ép.
COT_THO9 = (*COT_THO, "so", "hang")
SO_HOP_LE = ("GI", "OMC", "SC", "PS")
_MA_VENDOR = re.compile(r"VD[0-9]+", re.ASCII)
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
    nhieu_so = cot_tho == list(COT_THO9)
    if cot_tho != list(COT_THO) and not nhieu_so:
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(Block 1 một sổ GI)* hoặc "
                         f"{list(COT_THO9)} *(nhiều sổ — DT9b)*")
    dau = tho.get("dong_dau_sheet")
    if dau != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET} *(Block 1 từ hàng sheet 4)*")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng Block 1 ⛔ rỗng")

    rong_cot = len(COT_THO9) if nhieu_so else len(COT_THO)
    dong: list[list[Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != rong_cot:
            raise ValueError(f"hàng {i + 1} phải {rong_cot} ô *(đủ {'M:S + so + hang' if nhieu_so else 'M:S'})*")
        No, vendor, network, account, pct, cm, cd = h[:7]
        so, hang = ("GI", DONG_DAU_SHEET + i) if not nhieu_so else (h[7], h[8])
        if so not in SO_HOP_LE:
            raise ValueError(f"hàng {i + 1}: `so` ⛔ thuộc {list(SO_HOP_LE)}")
        if isinstance(hang, bool) or not isinstance(hang, int) or hang < DONG_DAU_SHEET:
            raise ValueError(f"hàng {i + 1}: `hang` phải số nguyên ≥ {DONG_DAU_SHEET}")
        if _rong(vendor):
            raise ValueError(f"hàng {i + 1}: cột Vendor ID RỖNG — Block 1 mỗi hàng phải có mã")
        if not isinstance(vendor, str) or not _MA_VENDOR.fullmatch(vendor.strip()):
            raise ValueError(f"hàng {i + 1}: cột vendor ⛔ phải MÃ `VD<số>` *(⛔ tên — PII; ⛔ in giá trị ô)*")
        if so != "GI" and not _rong(account):
            raise ValueError(f"hàng {i + 1}: `account` ⛔ đọc ở sổ {so} *(tên người / số TK — DT9b)*")
        if so in ("SC", "PS") and not _rong(network):
            raise ValueError(f"hàng {i + 1}: `network` ⛔ đọc ở sổ {so} *(cột tên — DT9b)*")
        # ô rỗng ("" | null) chuẩn hoá về null *(ảnh tất định)*.
        row = [hang if so == "GI" else f"{so}!{hang}", No,
               vendor.strip(),
               None if _rong(network) else network,
               None if _rong(account) else account,
               None if _rong(pct) else pct,
               cm, cd,
               _cach_tinh(network, vendor), so]
        dong.append(row)

    rieng = sorted({r[8] for r in dong if r[8] != "thường"})
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"Block 1 = {len(dong)} hàng liền *(sheet {DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1}; "
            f"AP ghi 36 = hàng 4–39 ⇒ errata, DT8-R1-01)* vùng M:S; MappingBlock2.gs nhân × 7 CDT1 *(C9/H9 tiêu thụ)*. Cột `cach_tinh` SUY "
            f"*(⛔ đọc từ sheet)*: Network 'Max' ⇒ 'Max', ngược lại Vendor ∈ {list(NHOM_RIENG)} ⇒ "
            f"chính mã, ngược lại 'thường'. {len(rieng)} nhãn riêng = {rieng} *(mong "
            f"{sorted(MONG_RIENG)}; khác ⇒ cổng ĐỎ)*. Cột `account` = Tên tài khoản *(owner GIỮ "
            f"11/09 — chỉ 'Email Address' bị cấm)*. ⛔ mang cột ngoài M:S. "
            f"DT9b: cột `so` ∈ {list(SO_HOP_LE)} — đếm DÒNG theo sổ "
            f"{ {x: sum(1 for r in dong if r[9] == x) for x in SO_HOP_LE} }; khoá `dong_sheet` GI = số hàng, "
            f"sổ khác = `<SO>!<hàng>`; OMC/SC/PS ⛔ đọc `account`, SC/PS ⛔ đọc `network`."),
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
