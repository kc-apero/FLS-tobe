"""Khuôn đóng băng `atl_cay` — cây HD của sheet ATL → `IX.HD` *(mã · tên · cha · cấp · nhóm)*.

    python tools/dong_bang_sheet.py atl_cay <bản_thô.json> --mong 74
        ⇒ tests/fixture/cau_hinh/atl_cay.json

Nguồn: `'Report I PLA3 Y H Q M | PM + HR | ATL'!A7:F88` *(P&L Report — hàng 6 là tiêu đề
`L1 · L2 · L3 · L4 · Period`)*. AP v3.1.2 §3.2.1 hàng `IX.HD`: *"mã · tên · cha · cấp L1–L4 ·
nhóm — 74 dòng ở cây ATL, 6 nhóm (§3.2.5)"*.

⭐ **Bản thô ⛔ ở hình `{cot, dong}`** — orchestrator đưa mỗi hàng là `{A, cap_cot, o}`:
  · `A`       — số mUSD ĐÃ ĐỊNH DẠNG *(một chữ số lẻ, chuỗi hiển thị)* ⇒ ⛔ vào ảnh. Khuôn chỉ lấy
                CẤU TRÚC; giá trị lấy lại bằng `effectiveValue` khi làm đáp án *(bước khác)*.
  · `cap_cot` — nhãn nằm ở cột nào trong `B…E` *(0…3)* ⇒ **cấp = cap_cot + 1** *(L1…L4)*.
  · `o`       — nhãn. Ba dạng, đo 16/11 trên 81 hàng:
      `MÃ | Tên`   *(có dấu cách quanh `|`)*  ⇒ dòng MÃ                       — **74**
      `MÃ|Tên`     *(⛔ dấu cách)*            ⇒ dòng TIÊU ĐỀ NHÓM *(cột 0)*   — **6**
      `""`                                    ⇒ dòng TRỐNG *(sheet hàng 35)* — **1**
    Dạng khác ⇒ TỪ CHỐI *(⛔ đoán)*. ⚠ Cột `F` *(Period)* lặp tên mã ⇒ orchestrator ⛔ đưa.

⭐⭐ **`cha` suy từ thụt cột, TRONG nhóm** *(hàm `chuan_bi`)*: duyệt theo thứ tự sheet với một
NGĂN XẾP; gặp dòng mã cấp `k` ⇒ bỏ khỏi ngăn mọi dòng cấp ≥ `k` ⇒ `cha` = đỉnh ngăn *(⛔ còn ⇒
gốc, `cha = null`)*. Tiêu đề nhóm XOÁ ngăn *(cây mới)*; dòng trống ⛔ đụng ngăn *(đo: dòng trống
35 nằm giữa `CDC` L1 và `CXP` L2 — `CXP` là con `CDC`)*. Phép này ⛔ bao giờ hỏng: cấp nhảy
*(L1 → L3)* thì `cha` là dòng cấp NHỎ HƠN gần nhất, và `cap` giữ nguyên ⇒ C4 thấy
`cap(con) ≠ cap(cha) + 1` và gọi tên lỗi. ⛔ Kiểm cha–con · chu trình ở đây *(ISP: "Loại trừ —
kiểm cha–con, chu trình (BE-CF · C4)")*; khuôn chỉ GHI ĐÚNG quan hệ thụt cột của sheet. Đo
16/11: ⛔ dòng nào nhảy cấp *(bài `test_DT3_B1_cay_ATL_cha_va_cap_…`)*.

⭐ **6 nhóm là `mong`, ⛔ suy** — `NHOM` khai MỘT chỗ ở đây, căn cứ AP v3.1.2 §3.2.5 *(bảng
"nhóm · cấp L1 → L4": `HDO · HDH · HDAP · HDT · HDC · HDCI`)*. Cổng:
  · bảng phụ `nhom` *(dòng tiêu đề)* đếm bằng `PHU_MONG` ⇒ 5 hay 7 tiêu đề là ĐỎ;
  · `thieu_lac`: nhóm khai mà ⛔ dòng mã nào ⇒ **thiếu** ⇒ ĐỎ; dòng mã thuộc nhóm ⛔ khai ⇒
    ⛔ đo được *(`ValueError`)* ⇒ ĐỎ. ⛔ **lạc** nào: thứ tự nhóm là dữ liệu, ảnh giữ `dong_sheet`.
  · bảng phụ `dong_trong` mong **1** *(đo)* — thêm/bớt dòng trống là bố cục sheet đã đổi, mọi
    `dong_sheet` phía sau trượt theo ⇒ người phải nhìn.

⛔ **Hai định nghĩa dòng PL** *(cây ATL ↔ Mapping Master)* đóng băng NGUYÊN, ⛔ hoà giải — C12 xử
*(đo 16/11: Mapping Master ⛔ có `NCF`, và `CXA` đứng sau `CDC` thay vì dưới `GAC`)*. ⛔ PII:
toàn mã/tên dòng HD.
"""
from __future__ import annotations

import re
from typing import Any

BANG = "IX.HD"
KHOA = "ma"
KIEU_KHOA = "ma"
COT = ("ten", "cha", "cap", "nhom", "dong_sheet")
#: `cap` · `dong_sheet` là SỐ *(cột ⛔ khai)*; gốc ⛔ cha ⇒ `cha` được rỗng.
KIEU_COT = {"ten": "chu", "cha": "chu?", "nhom": "chu"}
RA = "tests/fixture/cau_hinh/atl_cay.json"

#: ⭐ 6 nhóm của AP v3.1.2 §3.2.5, THỨ TỰ như AP — khai MỘT chỗ *(xem docstring)*.
NHOM = ("HDO", "HDH", "HDAP", "HDT", "HDC", "HDCI")
PHU_MONG = {"nhom": len(NHOM), "dong_trong": 1}

_VUNG = re.compile(r"!([A-Z]+)(\d+):([A-Z]+)(\d+)")
_TIEU_DE = re.compile(r"([A-Z][A-Z0-9]*)\|(\S.*)")
_TACH = " | "


def _dong_dau(nguon: str) -> tuple[int, int]:
    """Vùng đọc khai trong `nguon` *(`…'!A7:F88`)* → (dòng đầu, dòng cuối). Khuôn hiểu ĐÚNG một
    bố cục: bắt đầu ở cột `A` ⇒ khác ⇒ TỪ CHỐI, ⛔ đánh số dòng sheet sai im lặng."""
    v = _VUNG.findall(nguon)
    if len(v) != 1 or v[0][0] != "A":
        raise ValueError(f"`nguon` phải khai ĐÚNG một vùng `!A<n>:<cột><m>` — thấy {len(v)} "
                         f"vùng{'' if len(v) != 1 else ', ⛔ bắt đầu ở cột A'}")
    return int(v[0][1]), int(v[0][3])


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Hàng `{A, cap_cot, o}` → bảng `[ma, ten, cha, cap, nhom, dong_sheet]` + bảng phụ
    `nhom` · `dong_trong`. ⛔ Lời lỗi mang giá trị ô — chỉ dòng sheet *(⛔ PII ở nguồn này, nhưng
    công cụ in lời khuôn ra màn hình: giữ thói quen)*."""
    dau, cuoi = _dong_dau(tho["nguon"])
    hang = tho.get("dong")
    if not isinstance(hang, list) or not hang:
        raise ValueError("`dong` phải danh sách hàng khác rỗng")
    if dau + len(hang) - 1 > cuoi:
        raise ValueError(f"{len(hang)} hàng > vùng đọc {dau}…{cuoi}")

    dong: list[list[Any]] = []
    nhom: list[dict[str, Any]] = []
    trong: list[dict[str, Any]] = []
    ngan: list[tuple[int, str]] = []          # (cấp, mã) — ngăn xếp tổ tiên trong nhóm
    nhom_hien: str | None = None
    for i, h in enumerate(hang):
        r = dau + i                           # dòng sheet
        if not isinstance(h, dict) or set(h) != {"A", "cap_cot", "o"}:
            raise ValueError(f"dòng sheet {r}: hàng phải đúng ba khoá A · cap_cot · o")
        cc, o = h["cap_cot"], h["o"]
        if type(cc) is not int or not 0 <= cc <= 3 or not isinstance(o, str):
            raise ValueError(f"dòng sheet {r}: cap_cot phải số nguyên 0…3, o phải chuỗi")
        if not o.strip():
            trong.append({"dong_sheet": r})
            continue
        m = _TIEU_DE.fullmatch(o.strip())
        if m:
            if cc != 0:
                raise ValueError(f"dòng sheet {r}: tiêu đề nhóm ⛔ ở cột L1 (cap_cot {cc})")
            nhom_hien = m.group(1)
            nhom.append({"ma": m.group(1), "ten": m.group(2).strip(), "dong_sheet": r})
            ngan = []
            continue
        if _TACH not in o:
            raise ValueError(f"dòng sheet {r}: nhãn ⛔ thuộc dạng nào (`MÃ | Tên` · `MÃ|Tên` · "
                             "trống)")
        ma, ten = (x.strip() for x in o.split(_TACH, 1))
        if not ma or not ten:
            raise ValueError(f"dòng sheet {r}: `MÃ | Tên` thiếu mã hoặc tên")
        if nhom_hien is None:
            raise ValueError(f"dòng sheet {r}: dòng mã đứng TRƯỚC tiêu đề nhóm đầu tiên")
        cap = cc + 1
        while ngan and ngan[-1][0] >= cap:
            ngan.pop()
        dong.append([ma, ten, ngan[-1][1] if ngan else None, cap, nhom_hien, r])
        ngan.append((cap, ma))

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"nhom": nhom, "dong_trong": trong},
        "ghi_chu": (
            f"Cây ATL đọc {len(hang)} hàng (dòng sheet {dau}…{dau + len(hang) - 1}) = {len(dong)} "
            f"dòng mã + {len(nhom)} tiêu đề nhóm (bảng phụ `nhom`) + {len(trong)} dòng trống "
            "(bảng phụ `dong_trong`). Cột A (số mUSD đã định dạng) ⛔ vào ảnh — chỉ CẤU TRÚC. "
            "cap = cap_cot + 1 (L1…L4); cha = dòng mã gần nhất phía trên có cấp nhỏ hơn, TRONG "
            "nhóm (tiêu đề nhóm xoá ngăn, dòng trống ⛔ đụng); ⛔ kiểm cha–con (C4)."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Nhóm của các dòng mã ↔ `NHOM`: thiếu = nhóm khai mà ⛔ dòng mã nào; nhóm ⛔ khai ⇒
    ⛔ đo được *(`ValueError`)*. ⛔ lạc *(xem docstring)*."""
    co = []
    for d in dong:
        n = d.get("nhom")
        g = n.get("chu") if isinstance(n, dict) else None
        if g not in co:
            co.append(g)
    la = [g for g in co if g not in NHOM]
    if la:
        raise ValueError(f"{len(la)} nhóm ⛔ khai ở NHOM (AP v3.1.2 §3.2.5): {la}")
    return {"thieu": [g for g in NHOM if g not in co], "lac": [],
            "dai": f"{len(NHOM)} nhóm khai {list(NHOM)} · AP v3.1.2 §3.2.5"}
