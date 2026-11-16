"""Khuôn đóng băng `cdt_correct` — bảng CDT Correct *(P&L Report, cột `BR:BS`)* → `IX.ORG`.

    python tools/dong_bang_sheet.py cdt_correct <bản_thô.json> --mong 13
        ⇒ tests/fixture/cau_hinh/cdt_correct.json

AP v3.1.2 §3.2.1 hàng `IX.ORG`: *"CDT Correct 18 dòng, mặc định SHQ2 · P&L BR11:BS28"*; §3.2.4:
*"CDT Correct BR11:BS28, mặc định SHQ2 — CDT lạ rơi im lặng về SHQ2"*. Bảng chuẩn hoá giá trị
CDT gặp ở nguồn *(cột `BR`, vd `CMN_Management`)* về **CDT1 chuẩn** *(cột `BS`, vd
`SHQ1 | Headquarters1`)*; tiêu đề ở `BR10` = `'Chủ dự toán (CDT1)'`.

⛔⛔ **`mong` = 13, ⛔ 18** *(quyết định ⑪ của `WO-106`, orchestrator đo 16/11)*. "18 dòng
(BR11:BS28)" của ISP/AP là khoảng Ô; đọc lại `BR8:BS32` thì API trả 16 phần tử cho 25 hàng hỏi
*(hàng 8·9 rỗng + tiêu đề + 13)* ⇒ `BR24:BS32` RỖNG. **13 = dòng có dữ liệu ở `BR11:BS23`**.

Bản thô đã ở hình `{cot, dong}` *(orchestrator đặt tên hai cột `cdt_nguon` · `cdt1_chuan` — tiêu
đề sheet chỉ có MỘT ô `BR10` cho cả hai)* ⇒ khuôn ⛔ cần `chuan_bi`. Hai cột đều CHỮ, ⛔ được
rỗng: một dòng `cdt1_chuan` rỗng chính là đường *"rơi im lặng về SHQ2"* mà AP gọi tên.

⛔ **thiếu/lạc ⛔ áp dụng** cho bảng ÁNH XẠ *(⛔ có dải như tháng của `ix_fx`)*. Khuôn ⛔ bịa
nghĩa: ⛔ đòi bảng *đóng* *(mọi `cdt1_chuan` tự ánh xạ về chính nó)* — nguồn 16/11 ⛔ đóng
*(`SHQ1 | Headquarters1`, `ASA | Super App` chỉ xuất hiện ở cột chuẩn)*, và việc ấy là của C8.
Cổng của bảng này = `--mong` + khoá ⛔ trùng/hỏng + ô ⛔ rỗng/⛔ chữ — phần CHUNG của công cụ.
⛔ PII: toàn mã đơn vị *(orchestrator ghi ở bản thô)*.
"""
from __future__ import annotations

from typing import Any

BANG = "IX.ORG"
#: Tên cột ĐÚNG như bản thô orchestrator đưa *(C8 ánh xạ khi nạp)*.
KHOA = "cdt_nguon"
KIEU_KHOA = "ma"
COT = ("cdt1_chuan",)
KIEU_COT = {"cdt1_chuan": "chu"}
RA = "tests/fixture/cau_hinh/cdt_correct.json"


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """⛔ áp dụng *(xem docstring)* — trả rỗng, và `dai` NÓI vì sao, ⛔ im lặng."""
    return {"thieu": [], "lac": [],
            "dai": "⛔ áp dụng — bảng ánh xạ ⛔ có dải; cổng = --mong + khoá + ô (công cụ)"}
