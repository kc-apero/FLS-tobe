"""ITL-CANON — khuon giao dich chuan. 38 VI TRI (A..AL), 36 TRUONG.

Nguon nguyen van: 02_BA/05_DATA_DICTIONARY_ERD.md v0.7 §DD-I01, doc tu
`ITL I Input Transaction Ledger File 1_2 (RAW).xlsx` > sheet `Transaction Mapping L1`
(header o dong 3).

BA KHUYET TAT DAT TEN cua khuon nay — chep nguyen van, khong sua:
  1. Bon cot AH-AK TRUNG TEN het nhau ("MID I DoubleCheck LE")
     => KHONG THE tham chieu theo ten. Moi thu o day di theo VI TRI.
  2. W/X va AB/AC trung ten ("Thoi diem bat dau/ket thuc su dung dich vu")
     nhung KHAC NGUON (PE vs PI). Tron nham = sai ky ghi nhan P&L.
  3. Hai cot TRONG Z, AA nam giua khuon => 38 vi tri nhung 36 truong.
     Dem sai la lech mapping toan bo.

⚠ CANH BAO HAI HE TOA DO: chu cai A..AL o day la cua ITL-CANON (dau vao).
`ITL Ledge` (dau ra, 64 cot) cung dung chu cai A..AL nhung Y NGHIA KHAC HAN —
vi du AH o canon la mot trong 4 cot trung ten, AH o Ledge la Final khoi 4
(svc_start). Tron hai he la loi LANG, khong no. Hang cua Ledge dat ten LEDGE_*.
"""

from __future__ import annotations

from dataclasses import dataclass

_PE = "[Importrange]PE_Unpivot"
_PI = "[Importrange]PI_Unpivot"
_PM = "[Importrange]PM_Unpivot"
_TO = "Transaction Original"
_MM = "Master Mapping"


@dataclass(frozen=True)
class CanonCol:
    pos: int
    letter: str
    name: str      # "" = vi tri TRONG (Z, AA)
    group: str     # BASE | LINK | CLASS | SVC | PARTY | ""
    source: str


def letter_of(pos: int) -> str:
    """0->A … 25->Z, 26->AA … 37->AL. Khuon chu cai cua bang tinh."""
    if not 0 <= pos <= 37:
        raise ValueError(f"vi tri canon phai trong 0..37, nhan {pos}")
    if pos < 26:
        return chr(ord("A") + pos)
    return "A" + chr(ord("A") + pos - 26)


_TEN: tuple[tuple[str, str, str], ...] = (
    # (name, group, source) — theo dung thu tu vi tri 0..37
    ("Ngày chứng từ", "BASE", _TO),
    ("Số chứng từ", "BASE", _TO),
    ("Diễn giải", "BASE", _TO),
    ("Đơn vị tiền tệ", "BASE", _TO),
    ("PS Nợ", "BASE", _TO),
    ("PS Có", "BASE", _TO),
    ("Tài khoản", "BASE", _TO),
    ("Loại giao dịch (Payment Type)", "LINK", _PM),
    ("ID PELine - Nội dung PE (Advance)", "LINK", _PM),
    ("ID PELine - Nội dung PE (Urgent)", "LINK", _PM),
    ("ID PILine - Nội dung PI", "LINK", _PM),
    ("Pháp nhân thanh toán", "CLASS", _PM),
    ("ID PMSlip", "LINK", _PM),
    ("ID PMLine", "LINK", _PM),
    ("ID PESlip", "LINK", _PM),
    ("ID PELine", "LINK", _PM),
    ("ID PISlip", "LINK", _PM),
    ("ID PILine", "LINK", _PM),
    ("Budget Code (HDCode)", "CLASS", _PM),
    ("Chủ dự toán (CDT1)", "CLASS", _PM),
    ("Chủ dự toán *", "CLASS", _PM),
    ("Status_Final", "CLASS", _PM),
    ("Thời điểm bắt đầu sử dụng dịch vụ", "SVC", _PE),
    ("Thời điểm kết thúc sử dụng dịch vụ", "SVC", _PE),
    ("Mã đối tác (ID Payee)", "PARTY", _PE),
    ("", "", ""),                      # Z  — TRONG
    ("", "", ""),                      # AA — TRONG
    ("Thời điểm bắt đầu sử dụng dịch vụ", "SVC", _PI),
    ("Thời điểm kết thúc sử dụng dịch vụ", "SVC", _PI),
    ("File đính kèm: Hóa đơn", "PARTY", _PI),
    ("File đính kèm: Khác", "PARTY", _PI),
    ("Ghi chú (nếu có)", "PARTY", _PI),
    ("LE", "PARTY", _MM),
    ("MID I DoubleCheck LE", "PARTY", _MM),
    ("MID I DoubleCheck LE", "PARTY", _MM),
    ("MID I DoubleCheck LE", "PARTY", _MM),
    ("MID I DoubleCheck LE", "PARTY", _MM),
    ("No", "PARTY", _MM),
)

CANON_COLS: tuple[CanonCol, ...] = tuple(
    CanonCol(i, letter_of(i), n, g, s) for i, (n, g, s) in enumerate(_TEN))

CANON_36: tuple[CanonCol, ...] = tuple(c for c in CANON_COLS if c.name)

_POS: dict[str, int] = {c.letter: c.pos for c in CANON_COLS}


def pos_of(letter: str) -> int:
    p = _POS.get(letter.strip().upper())
    if p is None:
        raise ValueError(f"chu cai khong thuoc khuon canon A..AL: {letter!r}")
    return p
