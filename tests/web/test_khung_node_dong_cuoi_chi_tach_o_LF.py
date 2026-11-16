"""`khung_node._chay` đọc **dòng cuối** stdout của `node` — dòng cuối theo
`"\\n"`, ⛔ theo `str.splitlines()`.

⛔⛔ **Lỗi đã cắn** *(rà ISP Step 0, 16/11)*. `str.splitlines()` cắt ở **10**
ký tự đơn *(đo trên cả `0..0x10FFFF`)*; `JSON.stringify` thoát **7** ký tự
dưới `U+0020` nhưng để **TRẦN 3**: `U+0085` (NEL) · `U+2028` · `U+2029`.
`KQ-041` *(`tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py:81`)*
nạp vào kho test một dòng tiền `curr = "VND" + chr(0x85)` với số tiền **ngẫu
nhiên**; lượt nào dòng ấy lọt vào thân cửa mà một bài web in ra, thì
`splitlines()` cắt đôi dòng JSON ⇒ `json.loads` nổ. Đo: `test_wo032_man_cua_that.py`
`::test_AC3_…` + `::test_AC7_…` ĐỎ **1/4** lượt `pytest` toàn bộ ⇒ cổng đường
nền `--duong-nen` báo **đỏ giả**.

⇒ Bài này dựng **thẳng** điều kiện ấy, ⛔ chờ số tiền ngẫu nhiên rơi trúng:
kịch bản in một dòng nhật ký rồi trả một JSON mang ký tự trần — **mong**
`_chay` trả đúng giá trị ấy, từng ký tự.

⛔ Chiều ĐỎ: trả `.splitlines()` vào `khung_node.py` ⇒ **3/3** ca ĐỎ
*(`JSONDecodeError`)*.
"""
from __future__ import annotations

import json

import pytest

from tests.web.khung_node import _chay, can_node

#: 3 ký tự `str.splitlines()` cắt mà `JSON.stringify` để TRẦN *(đo 16/11:
#: `10` ký tự cắt dòng của Python − `7` ký tự `< U+0020` mà JSON thoát)*.
#: ⚠ Viết bằng `chr(<điểm mã>)`, ⛔ ký tự thật trong nguồn — chúng vô hình.
KY_TU_TRAN = [chr(0x85), chr(0x2028), chr(0x2029)]


@can_node
@pytest.mark.parametrize("ky_tu", KY_TU_TRAN,
                         ids=[f"U+{ord(k):04X}" for k in KY_TU_TRAN])
def test_dong_cuoi_mang_ky_tu_ngat_dong_unicode_van_doc_NGUYEN_JSON(ky_tu):
    """Giá trị `node` trả *(sau một dòng nhật ký cũng mang ký tự ấy)* về
    Python **nguyên vẹn** — cùng hình với dòng `KQ-041` nằm trong thân cửa."""
    mong = {"curr": "VND" + ky_tu, "so": "12345000.00",
            "ghi_chu": "giữa" + ky_tu + "chuỗi"}
    ra = _chay("console.log(%s); return %s;"
               % (json.dumps("nhật ký " + ky_tu), json.dumps(mong)))
    assert ra == mong, ra
