"""Cot `Classifying` cua bay khoi — suy tu CANON, ⛔ khong luu lai.

★ Vi sao module nay ton tai. `ledge_spec.py` khai bay cot `Classifying` la
KHONG LUU voi ly do *"suy lai duoc: Classifying = iferror(<cot canon>, 'Need to
manual input')"*. ⛔ `<cot canon>` la mot **CHO TRONG** — mot loi hua khong co
dia chi. Module nay dien dia chi vao, va **do tren du lieu that** truoc khi tin.

★★ CACH CHON DIA CHI: ⛔ khong doan. Do 2026-08-26 tren 9.845 dong ghep duoc
giua `[Master] ITL Ledge` va `Transaction Mapping L1` **doc live** — thu MOI ung
vien cho tung khoi roi de so lieu tu chon:

    khoi         ung vien       khop
    hd           canon S      100,0000%   <- chon
    pay_type     canon H      100,0000%   <- chon
    cdt1         canon T      100,0000%   <- chon
    svc_start    canon AB     100,0000%   <- chon
                 canon W       70,4114%
    svc_end      canon AC     100,0000%   <- chon
                 canon X       70,4114%
    id_payee     canon Y      100,0000%   <- chon
    invoice      canon AD     100,0000%   <- chon

⇒ **68.915 o · 7/7 khoi · 100,0000%**, 0 o lech.

⚠⚠ BAY DA TRANH DUOC. Ten cot cua canon `W`/`X` va `AB`/`AC` **GIONG HET NHAU**
(*"Thoi diem bat dau/ket thuc su dung dich vu"*). Neu chon theo TEN thi rat de
lay `W`/`X` — va `W`/`X` la cap **100% `#N/A` CO CHU Y** (`QD-ITL-51`: duong
lenh chi vs duong hoa don). Lay sai cap thi `svc_start`/`svc_end` cua **ca so**
thanh `Need to manual input`, va cai sai do **khong lam do bat cu cong nao** —
no chi lam hang cho phong len va khong ai biet vi sao. Con so 70,4114% la ban
ghi cua chinh cai bay do.

★★★ LUAT `iferror` — do duoc HAI BIEN THE, chi mot dung:
    luat A  o loi HOAC o rong  -> 'Need to manual input'
    luat B  CHI o loi          -> 'Need to manual input', o rong GIU RONG

Luat A khop 84,87%-99,97% tuy khoi; **luat B khop 100,0000% ca bay khoi**.
⇒ `iferror` **khong** bien o rong thanh gi ca. Doc lai cong thuc thi hien nhien,
nhung khac biet nay an 1.490 o o khoi `invoice` — va neu ta viet luat A thi
`work_status` cua 1.490 dong se sai.
"""

from __future__ import annotations

from typing import Any

from fls.canon.o_loi import la_o_loi
from fls.canon.row import CanonRow
from fls.canon.spec import CANON_COLS
from fls.ledger.final_rule import KHONG_TRA_LOI, TEN_BAY_KHOI

# khoi -> VI TRI trong khuon CANON (0-based). ⛔ Dia chi la VI TRI, khong phai
# TEN: bon cap ten trung nhau trong khuon nay (xem docstring).
VI_TRI_CLASSIFYING: dict[str, int] = {
    "hd":        18,   # canon S  · Budget Code (HDCode)
    "pay_type":   7,   # canon H  · Loai giao dich (Payment Type)
    "cdt1":      19,   # canon T  · Chu du toan (CDT1)
    "svc_start": 27,   # canon AB · ⚠ KHONG phai W (100% #N/A, QD-ITL-51)
    "svc_end":   28,   # canon AC · ⚠ KHONG phai X
    "id_payee":  24,   # canon Y  · Ma doi tac (ID Payee)
    "invoice":   29,   # canon AD · File dinh kem: Hoa don
}

# Cap chet CO CHU Y — giu lai de cong chan duoc viec ai do "sua" sang day.
VI_TRI_CHET: dict[str, int] = {"svc_start": 22, "svc_end": 23}   # canon W · X

assert set(VI_TRI_CLASSIFYING) == TEN_BAY_KHOI, "phai phu dung bay khoi cua so"




def _sach(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v).strip()


def classifying(v: Any) -> str | None:
    """`=iferror(<o canon>, "Need to manual input")` — nguyen van.

    ⛔ O RONG giu rong, khong thanh `Need to manual input` (luat B, xem docstring).
    """
    if la_o_loi(v):
        return KHONG_TRA_LOI
    return _sach(v) or None


def khoi_tu_canon(row: CanonRow) -> dict[str, tuple[str | None, None]]:
    """Mot dong canon -> `khoi` cho `dung_dong`, o NGUOI GO de trong.

    Tra `(Classifying, Manual input=None)`: lan nap dau tien chua co ai go gi.
    ⇒ `dung_khoi` chay **che do tu sinh** (`MID` suy bang `tinh_mid`), ⛔ khong
    phai che do oracle. Do la dung — che do oracle chi dung khi DO thuoc chuan.
    """
    return {ten: (classifying(row.at(pos)), None)
            for ten, pos in VI_TRI_CLASSIFYING.items()}


def ten_canon(ten_khoi: str) -> str:
    """Chu cai + ten cot canon — de thong bao loi doc duoc, khong phai so tran."""
    c = CANON_COLS[VI_TRI_CLASSIFYING[ten_khoi]]
    return f"{c.letter} ({c.name})"
