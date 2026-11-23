"""`IX.TMP` — **bản báo cáo KÝ có phiên bản** *(ISP 3.1.2 · Step 36 · `C13` · `WO-257`)*.

Phần THUẦN: kiểm `{ky}` + **checksum** nội dung bản. Đọc/ghi kho là việc của
`fls/repo/cau_hinh_repo.py` *(`.importlinter` hợp đồng 10: tầng này ⛔ biết kho)*.

⭐ **Checksum = sha256 của JSON CHUẨN HOÁ** *(khoá sắp xếp · `ensure_ascii=False` ·
dấu phân cách `,`/`:` không khoảng trắng · UTF-8)* ⇒ tất định, ⛔ phụ thuộc thứ tự khoá.
Nội dung phải là **JSON thuần** *(object không rỗng; `Decimal`/`datetime`/… ⇒ `LoiBanKy`
— ⛔ `default=str` âm thầm đổi kiểu rồi đọc lại ra số khác)*.

⭐ **`{ky}` = `yyyymm`** *(năm 2000…2099 · tháng 01…12 · 6 chữ số ASCII)* — cùng quy ước
`C7` `config/fx/{yyyymm}/sign`; ⛔ dạng `2025-12`.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from decimal import Decimal
from typing import Any, Mapping

BANG = "IX.TMP"
_KY = re.compile(r"(20[0-9]{2})(0[1-9]|1[0-2])", re.ASCII)


class LoiBanKy(ValueError):
    """`{ky}` hỏng hay nội dung bản ⛔ phải JSON thuần — **400** ở cửa."""


def kiem_ky(ky: Any) -> int:
    """`yyyymm` hợp lệ ⇒ `int`; ngược lại `LoiBanKy` có tên giá trị. ⛔ nhận `bool`."""
    if isinstance(ky, bool) or not isinstance(ky, (int, str)):
        raise LoiBanKy(f"ky={ky!r} ⛔ phải yyyymm (int hay chuỗi 6 chữ số)")
    s = str(ky).strip()
    if not _KY.fullmatch(s):
        raise LoiBanKy(f"ky={ky!r} ⛔ đúng khuôn yyyymm (năm 2000…2099 · tháng 01…12)")
    return int(s)


def _so_khu_hoi(x: Any) -> Any:
    """Đưa `float` về ĐÚNG giá trị mà `jsonb` trả lại *(`C13-R1-01`)*: kho lưu số kiểu
    `numeric` ⇒ `1e22` đọc ra `int` `10**22` · `-0.0` đọc ra `0.0` *(numeric ⛔ có số 0 âm)*.
    Băm bản CHƯA khứ hồi thì checksum niêm phong ≠ checksum của nội dung đọc lại.
    Cách HẸP: chỉ đổi `float` hữu hạn *(`bool`/`int`/chuỗi/`null` giữ nguyên; `nan`/`inf` để
    `json.dumps(allow_nan=False)` nổ như cũ)*. ⚠ `1` và `1.0` VẪN là hai checksum khác
    nhau *(kho giữ `1.0`)* — engine H14 phải ổn định kiểu số."""
    if isinstance(x, float) and math.isfinite(x):
        d = Decimal(repr(x))
        if d == 0:
            d = abs(d)
        return json.loads(format(d, "f"))
    if isinstance(x, Mapping):
        return {k: _so_khu_hoi(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_so_khu_hoi(v) for v in x]
    return x


def chuan_hoa(noi_dung: Mapping[str, Any]) -> str:
    """Chuỗi JSON chuẩn hoá của một bản. Rỗng/không-object/không-JSON ⇒ `LoiBanKy`."""
    if not isinstance(noi_dung, Mapping) or not noi_dung:
        raise LoiBanKy("nội dung bản ⛔ phải một object JSON KHÔNG rỗng (các ô của báo cáo)")
    try:
        return json.dumps(_so_khu_hoi(noi_dung), sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as e:
        raise LoiBanKy(f"nội dung bản ⛔ phải JSON thuần (số · chuỗi · bool · null · "
                       f"mảng · object): {e}") from e


def checksum(noi_dung: Mapping[str, Any]) -> str:
    """sha256 hex (64 ký tự) của `chuan_hoa(noi_dung)` mã hoá UTF-8."""
    return hashlib.sha256(chuan_hoa(noi_dung).encode("utf-8")).hexdigest()
