"""Ma phap nhan — hai cot cua nguon mang HAI HINH DANG cho cung mot thu.

★ Do 2026-08-26 tren `Transaction Mapping L1` (9.992 dong, doc live):

    canon AG "LE"                     24 gia tri · ma TRAN     : 'VGOH'
    canon L  "Phap nhan thanh toan"   17 gia tri · 5 ma CO TEN : 'VGOH - APERO HQ'
                                      (6.648 o con lai la o loi)

Cung mot phap nhan, hai hinh. `fls_itl.le` va `fls_itl.le_payer` deu FK toi
`fls_le.le_code`, nen neu chep nguyen thi 'VGOH - APERO HQ' lam VO khoa ngoai —
va cach "sua" de dan nhat la nhet ca hai hinh vao danh muc, tuc mot phap nhan
thanh HAI dong danh muc. Tu do moi bao cao gop theo phap nhan deu tach lam hai
ma khong ai thay.

⇒ Ma la phan TRUOC dau ' - '. ⛔ Khong mat gi: `canon` jsonb giu nguyen van 38
vi tri, nen chuoi goc 'VGOH - APERO HQ' van truy lai duoc.

⚠ 'Cash Treasury' KHONG co ' - ' nen di qua nguyen ven — dung. No la mot nhan
khong-phai-phap-nhan (`INV-I10`), va viec no co phai phap nhan hay khong thi
nguon KHONG noi. ⛔ Khong doan ho nguon: xem `GAP-LE-01`.
"""

from __future__ import annotations

from typing import Any

from fls.canon.o_loi import la_o_loi

TACH = " - "


def ma_le(v: Any) -> str | None:
    """'VGOH - APERO HQ' -> 'VGOH' · 'VGOH' -> 'VGOH' · o loi/rong -> None."""
    if v is None or la_o_loi(v):
        return None
    s = str(v).strip()
    if not s:
        return None
    return s.split(TACH, 1)[0].strip() or None


def ten_le(v: Any) -> str | None:
    """Phan SAU dau ' - ' neu nguon co noi ten, khong thi None.

    ⛔ Khong bia ten: `le_name` de NULL con thanh that hon la lay ma lam ten
    roi ve sau khong ai phan biet duoc "chua biet ten" voi "ten dung la the".
    """
    if v is None or la_o_loi(v):
        return None
    s = str(v).strip()
    return s.split(TACH, 1)[1].strip() or None if TACH in s else None
