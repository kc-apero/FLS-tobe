"""Khuôn đóng băng `atl_cay` — cây HD của sheet ATL → `IX.HD` *(mã · tên · cha · cấp · nhóm)*.

    python tools/dong_bang_sheet.py atl_cay <bản_thô.json> --mong 74
        ⇒ tests/fixture/cau_hinh/atl_cay.json

Nguồn: `'Report I PLA3 Y H Q M | PM + HR | ATL'!A7:F90` *(P&L Report)*. AP v3.1.2 §3.2.1 hàng
`IX.HD`: *"mã · tên · cha · cấp L1–L4 · nhóm — 74 dòng ở cây ATL, 6 nhóm (§3.2.5)"*.

⭐ **Bản thô = LƯỚI Ô của SA** *(`DT3-R1-03` — orchestrator chốt 17/11)*. Hợp đồng:
`{spreadsheet_id, nguon, doc_luc, cach_doc, values: [[ô,…],…]}` — `values` là lưới THEO HÀNG,
hàng đầu = dòng sheet `dau` của vùng, ô theo chữ cái cột `A`=0 … `F`=5. ⛔ hình `{A, cap_cot, o}`
*(đó là quy ước của MỘT phiên đọc 16/11, ⛔ nội dung ô — bản thô phải mang HÌNH DẠNG của nguồn)*.
Mỗi hàng được phân loại từ CHÍNH các ô *(⛔ nhãn dựng sẵn)*:

  · **Dòng MÃ**    — ĐÚNG MỘT ô trong `B…E` có `" | "` *(= `MÃ | Tên`)*; cột ấy cho **CẤP**
                     *(`B`⇒L1 · `C`⇒L2 · `D`⇒L3 · `E`⇒L4)*; ô `F` *(Period)* LẶP nhãn ấy *(canh)*.
                     Cột `A` *(số mUSD)* ⛔ vào ảnh — khuôn chỉ lấy CẤU TRÚC.
  · **Tiêu đề NHÓM** — ô `B` khớp `[A-Z][A-Z0-9]*` *(mã)*, ô `C` khác rỗng, ⛔ `" | "` nào, `D·E`
                     rỗng. ⚠ Ở sheet tiêu đề nhóm là **HAI ô** `B` *(mã)* · `C` *(tên)* — ⛔ chuỗi
                     `MÃ|Tên` *(`DT3-R1-03`: quy ước bản thô cũ, ⛔ hình dạng sheet)*.
  · **Dòng TRỐNG**  — `B…E` đều rỗng *(sheet hàng 35)*.

⭐⭐ **Biên dư** *(`DT3-R1-02` · Đ5)*. Sau dòng dữ liệu CUỐI *(mã/tiêu đề nhóm cuối)*, vùng còn
ô canh `CHECK ZONE` + hàng rỗng — khuôn ⛔ đếm chúng, chỉ ĐÒI vùng đọc `!A<dau>:F<cuoi>` có
`cuoi` **>** dòng sheet của dòng dữ liệu cuối. Khác *(dữ liệu chạm `cuoi`)* ⇒ TỪ CHỐI exit 2:
nguồn thêm một dòng mã dưới đáy mà vùng đọc vừa khít thì dòng ấy ⛔ bao giờ tới công cụ *(lỗi
mất-dòng-im-lặng mà `cdt_correct` từng dính)*. Dòng `khac` *(ô canh)* chỉ được nằm SAU dữ liệu
— nằm giữa bảng ⇒ TỪ CHỐI *(rác lọt bảng)*.

⭐⭐ **`cha` suy từ thụt cột, TRONG nhóm** *(hàm `chuan_bi`)*: duyệt theo thứ tự sheet với một
NGĂN XẾP; gặp dòng mã cấp `k` ⇒ bỏ khỏi ngăn mọi dòng cấp ≥ `k` ⇒ `cha` = đỉnh ngăn *(⛔ còn ⇒
gốc, `cha = null`)*. Tiêu đề nhóm XOÁ ngăn *(cây mới)*; dòng trống ⛔ đụng ngăn *(đo: dòng trống
35 nằm giữa `CDC` L1 và `CXP` L2 — `CXP` là con `CDC`)*. Phép này ⛔ bao giờ hỏng: cấp nhảy
*(L1 → L3)* thì `cha` là dòng cấp NHỎ HƠN gần nhất, và `cap` giữ nguyên ⇒ C4 thấy
`cap(con) ≠ cap(cha) + 1` và gọi tên lỗi. ⛔ Kiểm cha–con · chu trình ở đây *(ISP: "Loại trừ —
kiểm cha–con, chu trình (BE-CF · C4)")*; khuôn chỉ GHI ĐÚNG quan hệ thụt cột của sheet. Đo
17/11: ⛔ dòng nào nhảy cấp *(bài `test_DT3_B1_cay_ATL_cha_va_cap_…`)*.

⭐ **6 nhóm là `mong`, ⛔ suy** — `NHOM` khai MỘT chỗ ở đây, căn cứ AP v3.1.2 §3.2.5 *(bảng
"nhóm · cấp L1 → L4": `HDO · HDH · HDAP · HDT · HDC · HDCI`)*. Cổng:
  · bảng phụ `nhom` *(dòng tiêu đề)* đếm bằng `PHU_MONG` ⇒ 5 hay 7 tiêu đề là ĐỎ;
  · bảng phụ `dong_trong` mong **1** *(đo)* — thêm/bớt dòng trống là bố cục sheet đã đổi;
  · `thieu_lac`: nhóm khai mà ⛔ dòng mã nào ⇒ **thiếu** ⇒ ĐỎ; dòng mã thuộc nhóm ⛔ khai ⇒
    `ValueError` ⇒ ĐỎ. ⛔ **lạc** nào: thứ tự nhóm là dữ liệu, ảnh giữ `dong_sheet`.

⭐ **Phân bố CẤP là `mong`** *(`DT3-R1-06` · Đ5)* — `MONG_CAP` khai số dòng mỗi cấp L1…L4
*(đo 17/11: 37 · 23 · 11 · 3 = 74)*. `thieu_lac` so phân bố thật với `MONG_CAP` ⇒ đổi bố cục cấp
*(vd `MAC` L3 → L2)* làm **cổng ĐỎ**, ⛔ chỉ pytest *(checksum + `cap(cha)`)* bắt. R1 đo: cổng chỉ
canh TỔNG 74 thì `MAC` L3→L2 qua `[ĐẠT]`.

⛔ **Hai định nghĩa dòng PL** *(cây ATL ↔ Mapping Master)* đóng băng NGUYÊN, ⛔ hoà giải — C12 xử
*(đo 17/11: Mapping Master ⛔ có `NCF`, và `CXA` đứng sau `CDC` thay vì dưới `GAC`)*. ⛔ PII:
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
#: ⭐ Phân bố cấp L1…L4 đo 17/11 *(`DT3-R1-06` · Đ5 — khác ⇒ cổng ĐỎ)*. Tổng = 74 = `--mong`.
MONG_CAP = {"1": 37, "2": 23, "3": 11, "4": 3}

_VUNG = re.compile(r"!([A-Z]+)(\d+):([A-Z]+)(\d+)")
_MA_NHOM = re.compile(r"[A-Z][A-Z0-9]*")
_TACH = " | "


def _dong_dau(nguon: str) -> tuple[int, int]:
    """Vùng đọc khai trong `nguon` *(`…'!A7:F90`)* → (dòng đầu, dòng cuối). Khuôn hiểu ĐÚNG một
    bố cục: bắt đầu ở cột `A` ⇒ khác ⇒ TỪ CHỐI, ⛔ đánh số dòng sheet sai im lặng."""
    v = _VUNG.findall(nguon)
    if len(v) != 1 or v[0][0] != "A":
        raise ValueError(f"`nguon` phải khai ĐÚNG một vùng `!A<n>:<cột><m>` — thấy {len(v)} "
                         f"vùng{'' if len(v) != 1 else ', ⛔ bắt đầu ở cột A'}")
    return int(v[0][1]), int(v[0][3])


def _o(h: list, idx: int) -> str | None:
    """Ô chuỗi đã strip của lưới *(cột `idx`)*, hay `None` *(ô số · rỗng · thiếu)*."""
    x = h[idx] if idx < len(h) else None
    return x if isinstance(x, str) and x.strip() else None


def _loai(h: list) -> tuple[str, int | None]:
    """Phân loại một hàng lưới từ CHÍNH ô `B…E` → (`ma`|`nhom`|`trong`|`khac`, cột nhãn)."""
    nhan = [j for j in range(1, 5) if _o(h, j) and _TACH in _o(h, j)]   # B…E có " | "
    if len(nhan) == 1:
        return "ma", nhan[0]
    if not nhan and _o(h, 1) and _MA_NHOM.fullmatch(_o(h, 1)) and _o(h, 2) \
            and not _o(h, 3) and not _o(h, 4):
        return "nhom", None
    if not any(_o(h, j) for j in range(1, 5)):
        return "trong", None
    return "khac", None


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Lưới ô SA → bảng `[ma, ten, cha, cap, nhom, dong_sheet]` + bảng phụ `nhom` · `dong_trong`.
    ⛔ Lời lỗi mang giá trị ô — chỉ dòng sheet *(⛔ PII ở nguồn này, nhưng công cụ in lời khuôn:
    giữ thói quen)*."""
    dau, cuoi = _dong_dau(tho["nguon"])
    luoi = tho.get("values")
    if not isinstance(luoi, list) or not luoi:
        raise ValueError("`values` phải lưới ô *(danh sách hàng)* khác rỗng")
    rong = 6                                       # A…F
    for i, h in enumerate(luoi):
        if not isinstance(h, list) or len(h) > rong:
            raise ValueError(f"dòng sheet {dau + i}: hàng phải danh sách ≤ {rong} ô A…F")

    phan = [_loai(h) for h in luoi]
    du_lieu = [i for i, (lo, _) in enumerate(phan) if lo in ("ma", "nhom")]
    if not du_lieu:
        raise ValueError("lưới ⛔ có dòng mã hay tiêu đề nhóm nào")
    cuoi_dl = du_lieu[-1]
    if dau + cuoi_dl >= cuoi:                      # BIÊN DƯ (DT3-R1-02)
        raise ValueError(f"vùng đọc `!A{dau}:F{cuoi}` ⛔ dư hàng sau dữ liệu — dòng dữ liệu cuối ở "
                         f"sheet {dau + cuoi_dl} chạm đáy vùng ⇒ thêm một dòng mã dưới đáy sẽ ⛔ tới "
                         "công cụ; đọc rộng thêm vài hàng")

    dong: list[list[Any]] = []
    nhom: list[dict[str, Any]] = []
    trong: list[dict[str, Any]] = []
    ngan: list[tuple[int, str]] = []              # (cấp, mã) — ngăn xếp tổ tiên trong nhóm
    nhom_hien: str | None = None
    for i in range(cuoi_dl + 1):
        r = dau + i
        lo, col = phan[i]
        h = luoi[i]
        if lo == "khac":
            raise ValueError(f"dòng sheet {r}: ô B…E ⛔ thuộc dạng nào *(dòng mã `MÃ | Tên` · "
                             "tiêu đề nhóm · trống)* — rác giữa bảng")
        if lo == "trong":
            trong.append({"dong_sheet": r})
            continue
        if lo == "nhom":
            nhom_hien = _o(h, 1)
            nhom.append({"ma": _o(h, 1), "ten": _o(h, 2), "dong_sheet": r})
            ngan = []
            continue
        nhan = _o(h, col)                          # lo == "ma"
        if _o(h, 5) != nhan:
            raise ValueError(f"dòng sheet {r}: ô F phải LẶP nhãn `MÃ | Tên` của dòng mã")
        ma, ten = (x.strip() for x in nhan.split(_TACH, 1))
        if not ma or not ten:
            raise ValueError(f"dòng sheet {r}: `MÃ | Tên` thiếu mã hoặc tên")
        if nhom_hien is None:
            raise ValueError(f"dòng sheet {r}: dòng mã đứng TRƯỚC tiêu đề nhóm đầu tiên")
        cap = col                                  # B=1 … E=4 ⇒ L1…L4
        while ngan and ngan[-1][0] >= cap:
            ngan.pop()
        dong.append([ma, ten, ngan[-1][1] if ngan else None, cap, nhom_hien, r])
        ngan.append((cap, ma))

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"nhom": nhom, "dong_trong": trong},
        "ghi_chu": (
            f"Cây ATL (lưới SA, vùng {dau}…{cuoi}): dữ liệu hết ở dòng sheet {dau + cuoi_dl}, "
            f"biên dư tới {cuoi} (DT3-R1-02 — hàng sau là ô canh/rỗng, ⛔ đếm). {len(dong)} dòng "
            f"mã + {len(nhom)} tiêu đề nhóm (bảng phụ `nhom`, hai ô B·C ở sheet) + {len(trong)} "
            "dòng trống (bảng phụ `dong_trong`). Cột A (số mUSD) ⛔ vào ảnh — chỉ CẤU TRÚC. cap = "
            "cột nhãn B…E (B⇒L1…E⇒L4); cha = dòng mã gần nhất phía trên cấp nhỏ hơn, TRONG nhóm "
            "(tiêu đề nhóm xoá ngăn, dòng trống ⛔ đụng); ⛔ kiểm cha–con (C4)."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Nhóm của các dòng mã ↔ `NHOM`: thiếu = nhóm khai mà ⛔ dòng mã nào; nhóm ⛔ khai ⇒
    `ValueError`. Và phân bố CẤP ↔ `MONG_CAP` *(`DT3-R1-06`)*: lệch ⇒ vào `thieu` ⇒ cổng ĐỎ.
    ⛔ lạc *(thứ tự nhóm là dữ liệu — xem docstring)*."""
    co = []
    for d in dong:
        n = d.get("nhom")
        g = n.get("chu") if isinstance(n, dict) else None
        if g not in co:
            co.append(g)
    la = [g for g in co if g not in NHOM]
    if la:
        raise ValueError(f"{len(la)} nhóm ⛔ khai ở NHOM (AP v3.1.2 §3.2.5): {la}")
    dem_cap: dict[Any, int] = {}
    for d in dong:
        c = d.get("cap")
        dem_cap[c] = dem_cap.get(c, 0) + 1
    lech_cap = [f"cấp {k} {dem_cap.get(k, 0)}≠{v}" for k, v in MONG_CAP.items()
                if dem_cap.get(k, 0) != v]
    return {"thieu": [g for g in NHOM if g not in co] + lech_cap, "lac": [],
            "dai": f"{len(NHOM)} nhóm {list(NHOM)} · AP §3.2.5; cấp mong {MONG_CAP} (DT3-R1-06)"}
