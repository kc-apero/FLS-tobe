"""Kiem mot dong canon. Phan biet THIEU voi SAI KIEU — hai duong di khac nhau.

  THIEU thong tin phan loai  -> hang cho, work_status='UNMAPPED' (INV-I16)
  SAI KIEU / thieu thong tin xuong song -> LOAI vao fls_reject, ly do CO TEN (ACC-4)

⛔ Khong ham nao o day tra ve gia tri mac dinh. Khong doc duoc thi NO hoac bao
   ten ly do — bien mat trong im lang la cai du an nay cam.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

from fls.canon.row import CanonRow

# Vi tri trong khuon canon (KHONG phai cua ITL Ledge — xem canh bao o spec.py)
_NGAY, _SO_CT, _CURR, _NO, _CO, _ACCT = 0, 1, 3, 4, 5, 6

_TEN_NGAY = "Ngày chứng từ"
_TEN_NO, _TEN_CO = "PS Nợ", "PS Có"
_TEN_ACCT, _TEN_CURR = "Tài khoản", "Đơn vị tiền tệ"


@dataclass
class KetQua:
    loai: list[str] = field(default_factory=list)   # -> fls_reject
    cho: list[str] = field(default_factory=list)    # -> UNMAPPED

    def sach(self) -> bool:
        return not self.loai and not self.cho


def parse_so(v: Any) -> float | int | None:
    """Chap dinh dang ke toan. Rac thi NO — tra 0 la lam bien mat tien."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    s = unicodedata.normalize("NFKC", str(v)).strip().replace(" ", "")
    s = s.replace("(", "-").replace(")", "")
    if "," in s and "." in s:                       # 1,234,567.89
        s = s.replace(",", "")
    elif s.count(".") > 1:                          # 1.234.567
        s = s.replace(".", "")
    elif s.count(",") > 1:                          # 1,234,567
        s = s.replace(",", "")
    elif "," in s:                                  # 1234,56 kieu VN
        s = s.replace(",", ".")
    try:
        f = float(s)
    except ValueError as e:
        raise ValueError(f"khong doc duoc so: {v!r}") from e
    return int(f) if f.is_integer() else f


# Sheets API voi `valueRenderOption=UNFORMATTED_VALUE` tra o ngay duoi dang SO
# SERI (so ngay ke tu 30/12/1899). ⭐ Day la dang KHONG MO HO duy nhat cua nguon:
# khong co thang/ngay de hoan cho nhau, khong co locale. So voi chuoi "3/5/2026"
# thi seri la dang DE TIN NHAT — nen no duoc doc o day, khong bi coi la "so la".
#
# ⚠ Nhung PHAI CHAN dai: mot o tien (1.894.982.832) hay mot ma so ma lot vao cot
# ngay se thanh mot ngay nam 5-6 trieu ma khong ai thay. Dai cho phep 1954-2074.
SERI_GOC = date(1899, 12, 30)
SERI_MIN, SERI_MAX = 20_000, 63_800

_ISO = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")
_DMY = re.compile(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$")


def _tu_seri(v: int | float) -> date:
    """So seri cua Sheets -> `date`. ⛔ Ngoai dai thi NO, khong tra ngay la."""
    n = float(v)
    if not (SERI_MIN <= n <= SERI_MAX):
        raise ValueError(
            f"so {v!r} o cot ngay nam ngoai dai seri hop le "
            f"[{SERI_MIN}, {SERI_MAX}] (~1954-2074) — khong doc thanh ngay")
    return SERI_GOC + timedelta(days=int(n))


def parse_ngay(v: Any, thu_tu: str | None = None) -> date | None:
    """Chuoi -> date. ⛔ KHONG doan khi dinh dang mo ho.

    Nguon co ~5.369 dong ngay dang CHUOI, va 93% dong tung bi HOAN ngay<->thang
    (~181 ty sai ky). Nen: 03/01/2026 la MO HO => NO, buoc goi ro thu_tu.
    """
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return _tu_seri(v)
    s = str(v).strip()
    if m := _ISO.match(s):
        y, mo, d = (int(x) for x in m.groups())
        return date(y, mo, d)
    if m := _DMY.match(s):
        a, b, y = (int(x) for x in m.groups())
        if thu_tu == "dmy" or (thu_tu is None and a > 12):
            return date(y, b, a)
        if thu_tu == "mdy" or (thu_tu is None and b > 12):
            return date(y, a, b)
        raise ValueError(
            f"ngay mo ho, khong doan: {s!r} — ca hai phan <= 12. "
            "Goi parse_ngay(..., thu_tu='dmy'|'mdy') theo khai bao cua nguon")
    raise ValueError(f"khong doc duoc ngay: {v!r}")


def validate(row: CanonRow, thu_tu: str | None = None) -> KetQua:
    """⭐ `thu_tu` — thứ tự ngày/tháng **do NGUỒN khai** (`QĐ-ITL-113`).

    ⛔⛔ **`None` ⛔ KHÔNG có nghĩa "coi như `dmy`".** Nó có nghĩa *"nguồn này
       ⛔ chưa khai"* ⇒ ngày mơ hồ vẫn **bị loại**, kèm lý do. Đo 08/09 trên
       ảnh chụp thật: **29/29** nguồn có ngày mơ hồ là **`mdy`**, ⛔ **không
       một nguồn nào `dmy`** *(OCBC Singapore, TCB USD — sao kê nước ngoài)*
       ⇒ một mặc định *"vì đây là Việt Nam"* sẽ **hoán ngày↔tháng trên 1.894
       dòng**, đúng lớp lỗi `QĐ-ITL-17` *(~181 tỷ sai kỳ)*.
    """
    kq = KetQua()

    try:
        ngay = parse_ngay(row.at(_NGAY), thu_tu)
    except ValueError as e:
        kq.loai.append(f"{_TEN_NGAY}: không đọc được — {e}")
        ngay = None
    if ngay is None and not any(_TEN_NGAY in x for x in kq.loai):
        kq.loai.append(f"{_TEN_NGAY}: thiếu — không có ngày thì không biết kỳ, "
                       "không thể treo ở hàng chờ")

    tien = []
    for pos, ten in ((_NO, _TEN_NO), (_CO, _TEN_CO)):
        try:
            tien.append(parse_so(row.at(pos)))
        except ValueError as e:
            kq.loai.append(f"{ten}: không đọc được số — {e}")
            tien.append(None)
    if all(x in (None, 0) for x in tien):
        kq.loai.append(f"{_TEN_NO} và {_TEN_CO}: cả hai trống hoặc bằng 0 — "
                       "dòng không mang tiền, không đưa vào sổ")

    for pos, ten in ((_ACCT, _TEN_ACCT), (_CURR, _TEN_CURR)):
        v = row.at(pos)
        if v is None or (isinstance(v, str) and not v.strip()):
            kq.cho.append(f"{ten}: thiếu — vào hàng chờ, UNMAPPED")
    return kq
