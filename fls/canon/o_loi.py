"""O loi cua Google Sheets — mot ban khai DUY NHAT cho ca he.

⚠ VI SAO MODULE NAY RA DOI. Luat cu la `v.startswith("#")` va no nam **BON ban
sao** (`adapters/bank`, `ledger/classifying`, `oracle/tu_soi`, `tools/…`). Lan
nap THAT dau tien tren nguon day du bat duoc gia:

    dong 20 · cot goc C ('Dien giai') la o loi: ##LAI NHAP VON#

`##LAI NHAP VON#` la **ke toan GO TAY**, khong phai o loi. Luat cu nem **7 giao
dich that** vao `fls_reject` — va ly do ghi trong so se la *"o loi"*, tuc mot ly
do SAI: khong ai di tim mot cong thuc khong ton tai.

⇒ O loi la mot **tap DONG, dem duoc**, khong phai "chuoi bat dau bang #".

★ Bay gio la MOT ban khai. Bon ban sao mot luat la bon co hoi de chung lech nhau,
va cai lech se im lang: dong bi loai o tang nay, duoc giu o tang kia.
"""

from __future__ import annotations

from typing import Any

# Tap dong. `#N/A` con co dang dai `#N/A (Did not find value '' in VLOOKUP…)`
# nen so bang PREFIX, ⛔ khong so bang ==.
MA_LOI: tuple[str, ...] = (
    "#N/A", "#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#NULL!", "#NUM!",
    "#ERROR!", "#GETTING_DATA",
)


def la_o_loi(v: Any) -> bool:
    """True khi o mang MOT MA LOI cua Sheets. ⛔ Khong phai "bat dau bang #"."""
    if not isinstance(v, str):
        return False
    s = v.strip()
    return any(s == m or s.startswith(m + " ") or s.startswith(m + "(")
               for m in MA_LOI)


def ma_loi_cua(v: Any) -> str | None:
    """Ma loi (de dem theo loai), hoac None."""
    if not isinstance(v, str):
        return None
    s = v.strip()
    for m in MA_LOI:
        if s == m or s.startswith(m + " ") or s.startswith(m + "("):
            return m
    return None
