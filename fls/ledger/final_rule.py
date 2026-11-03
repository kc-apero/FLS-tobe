"""Luat cua bay khoi trong so ITL Ledge — dang HAM THUAN.

Cong thuc THAT, doc tu file `ITL … 2/2 (ADJUSTED)` > `ITL Ledge`, xac nhan o
**ba dong khac nhau** (10, 11, 5000) va **giong het nhau o ca bay khoi**:

  V = if(or(S="Need to manual input", len(S)=0), U, S)     <- Final = f(S, U)
  Z = if(or(W="Need to manual input", len(W)=0), Y, W)
  ...

⚠ NGHIA LA: `Final` phu thuoc `Classifying` va **`MID`**, ⛔ KHONG phu thuoc
`Manual input`. `Manual input` chi vao `Final` GIAN TIEP qua `MID`.

★ Hai buoc, ⛔ khong duoc gop:
    buoc 1  MID   = f(Classifying, Manual input, MAC DINH CUNG cua khoi)
    buoc 2  Final = f(Classifying, MID)

Ban dau module nay gop hai buoc thanh `tinh_final(classifying, manual)`. Chay
tren du lieu THAT (584 dong thang 3/2026) thi **6/7 khoi khop, khoi 7 lech
521/584**. Doi sang dung cong thuc `Final = f(Classifying, MID)` thi
**4.088/4.088 o khop 100%** tren ca bay khoi. Do la cach lo nay bi bat.

★★ MAC DINH CUNG la **MOT hang RIENG cho TUNG KHOI**, ⛔ khong phai mot hang
dung chung. `DD-I06` chi doc cong thuc cua khoi 1 roi suy rong ra ca bay khoi —
sai. Bang chung do tren **9.219 dong** o `MAC_DINH_THEO_KHOI`.

⚠ CHUA XAC NHAN DUOC: cot `MID` trong ban .xlsx **khong con cong thuc** (chi con
gia tri) nen luat `tinh_mid` duoi day lay tu `DD-I06`, doc tren file song ngay
24/08. Phai doc lai LIVE voi `valueRenderOption=FORMULA` truoc khi tin
(`GAP-ORA-05`).
"""

from __future__ import annotations

from dataclasses import dataclass

KHONG_TRA_LOI = "Need to manual input"
CO_INPUT_HERE = "Input here"

# (ten cot parity, ten cot noi that) — dung thu tu khoi 1..5 cua so ITL Ledge
NAM_KHOI: tuple[tuple[str, str], ...] = (
    ("hd", "hd_thyt"),                 # khoi 1 · Budget Code (HDCode)  · S T U V
    ("pay_type", "pay_type_thyt"),     # khoi 2 · Loai giao dich        · W X Y Z
    ("cdt1", "cdt1_thyt"),             # khoi 3 · Chu du toan (CDT1)    · AA AB AC AD
    ("svc_start", "svc_start_thyt"),   # khoi 4 · Bat dau dung dich vu  · AE AF AG AH
    ("svc_end", "svc_end_thyt"),       # khoi 5 · Ket thuc dung dich vu · AI AJ AK AL
)
# Khoi 6-7 ngoai hop dong P&L nhung VAN len man hinh (QD-owner-0824)
HAI_KHOI_NGOAI: tuple[tuple[str, str], ...] = (
    ("id_payee", "id_payee_thyt"),     # khoi 6 · Ma doi tac · AM AN AO AP
    ("invoice", "invoice_thyt"),       # khoi 7 · Hoa don    · AQ AR AS AT
)
BAY_KHOI: tuple[tuple[str, str], ...] = NAM_KHOI + HAI_KHOI_NGOAI

TEN_KHOI: frozenset[str] = frozenset(a for a, _ in NAM_KHOI)
TEN_BAY_KHOI: frozenset[str] = frozenset(a for a, _ in BAY_KHOI)

# Mac dinh cung cua TUNG khoi. Do truc tiep tren 9.219 dong cua `ITL Ledge`:
# voi moi khoi, thu tap gia tri `Final` o nhung dong con co co `Input here`.
#   khoi 1 hd          297/297     'OGA | GAC - Other'
#   khoi 2 pay_type    179/179     'Thanh toán (Regular)'
#   khoi 3 cdt1      1.222/1.222   'SHQ2 | Headquarters2'
#   khoi 4 svc_start    22         KHONG phai hang — 202512 x8 · 202508 x4 · 202509 x3 …
#   khoi 5 svc_end      22         KHONG phai hang — y nhu khoi 4
#   khoi 6 id_payee  1.642/1.642   'VD0'
#   khoi 7 invoice   6.573/6.582   'Nợ hoá đơn'   (9 dong con lai: rong)
MAC_DINH_THEO_KHOI: dict[str, str | None] = {
    "hd": "OGA | GAC - Other",
    "pay_type": "Thanh toán (Regular)",
    "cdt1": "SHQ2 | Headquarters2",
    "svc_start": None,   # chua suy duoc luat — GAP-ORA-06
    "svc_end": None,     # chua suy duoc luat — GAP-ORA-06
    "id_payee": "VD0",
    "invoice": "Nợ hoá đơn",
}


@dataclass(frozen=True)
class KetQuaFinal:
    parity: str | None      # y nhu so, KE CA cho may gan mac dinh
    thyt: str | None        # None o cho may tu bia
    may_tu_bia: bool


def _sach(v: str | None) -> str:
    return "" if v is None else str(v).strip()


def may_khong_tra_loi(classifying: str | None) -> bool:
    """Dieu kien re nhanh cua ca hai buoc: S rong HOAC S = 'Need to manual input'."""
    s = _sach(classifying)
    return s == KHONG_TRA_LOI or len(s) == 0


def tinh_final(classifying: str | None, mid: str | None) -> str | None:
    """Buoc 2 — tai hien NGUYEN VAN `=if(or(S=…, len(S)=0), U, S)`.

    ⛔ Doi so thu hai la `MID`, KHONG phai `Manual input`.
    Da doi soat: **4.088/4.088 o khop 100%** tren 584 dong thang 3/2026, ca bay khoi.
    """
    if may_khong_tra_loi(classifying):
        return _sach(mid) or None
    return _sach(classifying)


def tinh_mid(classifying: str | None, manual: str | None,
             mac_dinh: str | None) -> str | None:
    """Buoc 1 — luat `MID` theo `DD-I06`:

        U = if(T="" va S<>"Need to manual input", S,
               if(T="Input here", <MAC DINH CUNG cua khoi>, T))

    ⚠ Chua xac nhan duoc offline (cot `MID` khong con cong thuc) — `GAP-ORA-05`.
    """
    s, t = _sach(classifying), _sach(manual)
    if not t and s != KHONG_TRA_LOI:
        return s or None
    if t == CO_INPUT_HERE:
        return mac_dinh          # None neu khoi chua suy duoc mac dinh
    return t or None


def dung_khoi(ten_khoi: str, classifying: str | None, manual: str | None,
              mid: str | None = None) -> KetQuaFinal:
    """Ket qua mot khoi, tach `parity` (khop so) khoi `thyt` (so that).

    `mid` khai bao ⇒ **che do oracle**: dung `MID` cua so, dam bao parity.
    `mid` = None   ⇒ **che do tu sinh**: suy `MID` bang `tinh_mid`.

    ★★ CHO NOI THAT — ca thiet ke cot song song:
      may tu bia (o con co `Input here`) ⇒ `parity` VAN mang gia tri
      (khop so 100% tung o — `QD-ITL-35`) nhung `thyt = None` + `may_tu_bia = True`
      ⇒ `work_status='UNMAPPED'`, vao hang cho (`INV-I16`).

    ⚠ `AUD-12`: `thyt` CHI bien gia tri MAY TU BIA thanh None.
       ⛔ KHONG BAO GIO cham gia tri nguoi go — input trong sheet la SSOT.
    """
    if ten_khoi not in TEN_BAY_KHOI:
        raise ValueError(f"khoi khong thuoc 7 khoi cua so: {ten_khoi!r}")
    u = mid if mid is not None else tinh_mid(
        classifying, manual, MAC_DINH_THEO_KHOI[ten_khoi])
    parity = tinh_final(classifying, u)
    tu_bia = _sach(manual) == CO_INPUT_HERE and may_khong_tra_loi(classifying)
    return KetQuaFinal(parity, None if tu_bia else parity, tu_bia)
