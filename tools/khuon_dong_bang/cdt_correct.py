"""Khuôn đóng băng `cdt_correct` — bảng CDT Correct *(P&L Report, cột `BR:BS`)* → `IX.ORG`.

    python tools/dong_bang_sheet.py cdt_correct <bản_thô.json> --mong 13
        ⇒ tests/fixture/cau_hinh/cdt_correct.json

AP v3.1.2 §3.2.1 hàng `IX.ORG`: *"CDT Correct 18 dòng, mặc định SHQ2 · P&L BR11:BS28"*; §3.2.4:
*"CDT Correct BR11:BS28, mặc định SHQ2 — CDT lạ rơi im lặng về SHQ2"*. Bảng chuẩn hoá giá trị
CDT gặp ở nguồn *(cột `BR`, vd `CMN_Management`)* về **CDT1 chuẩn** *(cột `BS`, vd
`SHQ1 | Headquarters1`)*; tiêu đề ở `BR10` = `'Chủ dự toán (CDT1)'` *(ngoài vùng đọc)*.

⭐ **Bản thô = LƯỚI Ô của SA** *(`DT3-R1-03`)*: `{spreadsheet_id, nguon, doc_luc, cach_doc, values}`,
`values` theo HÀNG — mỗi hàng là hai ô `BR`·`BS`. Khuôn đặt tên hai cột `cdt_nguon`·`cdt1_chuan`
*(tiêu đề sheet chỉ có MỘT ô `BR10` cho cả hai)*. Hai cột đều CHỮ, ⛔ được rỗng: một dòng
`cdt1_chuan` rỗng chính là đường *"rơi im lặng về SHQ2"* mà AP gọi tên ⇒ cổng ĐỎ *(⛔ TỪ CHỐI —
nguồn dùng được, chỉ sai)*.

⛔⛔ **`mong` = 13, ⛔ 18** *(quyết định ⑪ của `WO-106`, orchestrator đo)*. "18 dòng (BR11:BS28)"
của ISP/AP là khoảng Ô; đọc lại `BR11:BS32` thì API trả **13** hàng *(hàng rỗng đuôi bị cắt)* ⇒
`BR24:BS32` RỖNG. **13 = dòng có dữ liệu ở `BR11:BS23`**.

⭐⭐ **Biên dư** *(`DT3-R1-02` · Đ5 — lỗi ĐÃ XẢY RA)*. Vùng đọc khai trong `nguon` phải CÓ hàng
dư sau dữ liệu: `cuoi` của `!BR<dau>:BS<cuoi>` **>** dòng sheet của hàng dữ liệu cuối *(= `dau`
+ số hàng về − 1, vì API cắt hàng rỗng đuôi)*. Khác *(vùng vừa khít dữ liệu, vd `BR11:BS23` cho
13 hàng)* ⇒ TỪ CHỐI exit 2: nguồn thêm một dòng CDT ở `BR24` thì ⛔ bao giờ tới công cụ và cổng
`[ĐẠT]` im lặng *(R1 đo: exit 0)*. ⇒ orchestrator đọc `BR11:BS32`.

⛔ **thiếu/lạc ⛔ áp dụng** cho bảng ÁNH XẠ *(⛔ có dải như tháng của `ix_fx`)*. Khuôn ⛔ bịa
nghĩa: ⛔ đòi bảng *đóng* *(mọi `cdt1_chuan` tự ánh xạ về chính nó)* — nguồn ⛔ đóng
*(`SHQ1 | Headquarters1`, `ASA | Super App` chỉ ở cột chuẩn)*, việc ấy là của C8. Cổng của bảng
này = biên dư *(chuan_bi)* + `--mong` + khoá ⛔ trùng/hỏng + ô ⛔ rỗng/⛔ chữ *(công cụ)*.
⛔ PII: toàn mã đơn vị.
"""
from __future__ import annotations

import re
from typing import Any

BANG = "IX.ORG"
#: Tên cột ĐÚNG như quy ước *(C8 ánh xạ khi nạp)* — `BR` = khoá, `BS` = chuẩn.
KHOA = "cdt_nguon"
KIEU_KHOA = "ma"
COT = ("cdt1_chuan",)
KIEU_COT = {"cdt1_chuan": "chu"}
RA = "tests/fixture/cau_hinh/cdt_correct.json"

_VUNG = re.compile(r"!([A-Z]+)(\d+):([A-Z]+)(\d+)")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Lưới ô SA `BR:BS` → bảng `[cdt_nguon, cdt1_chuan]`. ĐÒI biên dư *(`DT3-R1-02`)*.
    ⛔ Lời lỗi mang giá trị ô — chỉ dòng sheet."""
    v = _VUNG.findall(tho["nguon"])
    if len(v) != 1 or v[0][0] != "BR" or v[0][2] != "BS":
        raise ValueError(f"`nguon` phải khai ĐÚNG một vùng `!BR<a>:BS<b>` — CDT Correct ở cột "
                         f"BR:BS, thấy {len(v)} vùng")
    dau, cuoi = int(v[0][1]), int(v[0][3])
    luoi = tho.get("values")
    if not isinstance(luoi, list) or not luoi:
        raise ValueError("`values` phải lưới ô *(danh sách hàng)* khác rỗng")
    for i, h in enumerate(luoi):
        if not isinstance(h, list) or len(h) > 2:
            raise ValueError(f"dòng sheet {dau + i}: hàng phải danh sách ≤ 2 ô (BR · BS)")
    if dau + len(luoi) - 1 >= cuoi:                 # BIÊN DƯ (DT3-R1-02)
        raise ValueError(f"vùng đọc `!BR{dau}:BS{cuoi}` ⛔ dư hàng sau dữ liệu — {len(luoi)} hàng "
                         f"về chạm đáy vùng (dòng {dau + len(luoi) - 1}) ⇒ dòng CDT thêm dưới đáy "
                         "sẽ ⛔ tới công cụ; đọc rộng thêm vài hàng")

    dong = [[h[0] if len(h) > 0 else None, h[1] if len(h) > 1 else None] for h in luoi]
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (f"CDT Correct: lưới SA {len(luoi)} hàng (vùng BR{dau}:BS{cuoi}); biên dư tới "
                    f"{cuoi} (DT3-R1-02 — vùng > dữ liệu). Cột BR = {KHOA}, BS = {COT[0]}; tiêu đề "
                    "BR10 ngoài vùng. ⛔ bảng đóng (C8)."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """⛔ áp dụng *(xem docstring)* — trả rỗng, và `dai` NÓI vì sao, ⛔ im lặng."""
    return {"thieu": [], "lac": [],
            "dai": "⛔ áp dụng — bảng ánh xạ ⛔ có dải; cổng = biên dư + --mong + khoá + ô (công cụ)"}
