"""Ba cong tu kiem: nguon con SONG khong? — `G-ORA-LIVE-1/2/3`.

★ Vi sao module nay ton tai. Owner chot ban sao RAW la nguon voi ly do
"y chang ban goc, song" (QD-ITL-50). Do 26/08 dung la vay. Nhung mot ban sao
song hom nay co the CHET thang sau ma **van tra ve so cu trong binh thuong** —
IMPORTRANGE thoi chay khong bao gi. Luat du an: *cong chua tung thay do la cong
chua biet co song*. Nen cam ket "song" phai thanh thu MAY CHAN DUOC.

Ham thuan het: nhan so DA DO, tra ket qua. Viec do nam o `doc.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

NGUONG_NGAY = 45          # ky moi nhat cu hon the => nghi IMPORTRANGE da chet
GHEP_MIN, GHEP_MAX = 0.25, 0.45   # do that 33,5%; tai lieu ghi 33,8%


@dataclass(frozen=True)
class DoDuoc:
    """So do tu mot luot doc. `None` = khong do duoc (⛔ khong coi la 0)."""
    ky_moi_nhat: date | None
    dong_theo_tab: dict[str, int]
    o_loi_theo_tab: dict[str, int]
    ty_le_ghep: float | None


@dataclass(frozen=True)
class KetQuaCong:
    ma: str
    do: bool          # True = DO = chan luot doc
    ly_do: str        # luon co chu khi do (ACC-4)


def cong_1(d: DoDuoc, hom_nay: date) -> KetQuaCong:
    """So con duoc cap nhat khong? Ban sao chet van tra gia tri cu."""
    ma = "G-ORA-LIVE-1"
    if d.ky_moi_nhat is None:
        return KetQuaCong(ma, True, "khong do duoc ky nao trong so")
    cu = (hom_nay - d.ky_moi_nhat).days
    if cu > NGUONG_NGAY:
        return KetQuaCong(
            ma, True,
            f"ky moi nhat {d.ky_moi_nhat.isoformat()} cu {cu} ngay "
            f"(nguong {NGUONG_NGAY}) => nghi IMPORTRANGE da chet")
    return KetQuaCong(ma, False, "")


def cong_2(d: DoDuoc) -> KetQuaCong:
    """Tab nguon con du lieu khong? 0 dong hoac toan o loi => day dut."""
    ma = "G-ORA-LIVE-2"
    if not d.dong_theo_tab:
        return KetQuaCong(ma, True, "khong do duoc tab nguon nao")
    for tab, n in sorted(d.dong_theo_tab.items()):
        if n <= 0:
            return KetQuaCong(ma, True, f"tab {tab} co 0 dong")
        loi = d.o_loi_theo_tab.get(tab, 0)
        if loi >= n:
            return KetQuaCong(ma, True, f"tab {tab} toan o loi ({loi}/{n})")
    return KetQuaCong(ma, False, "")


def cong_3(d: DoDuoc) -> KetQuaCong:
    """Ty le ghep con nam trong khoang thuong thay khong?

    Roi ra ngoai theo CA HAI chieu deu dang nghi: thap = mapping sup;
    cao = dang co gia tri mac dinh duoc san xuat (dung benh cua ban sao ADJUSTED).

    ⚠ R-ORA-07d: cong nay do tren ty le ghep PM, ⛔ KHONG duoc dat nguong
    tren W/X — o do 0% la trang thai DUNG (QD-ITL-51).
    """
    ma = "G-ORA-LIVE-3"
    if d.ty_le_ghep is None:
        return KetQuaCong(ma, True, "khong do duoc ty le ghep")
    if not GHEP_MIN <= d.ty_le_ghep <= GHEP_MAX:
        return KetQuaCong(
            ma, True,
            f"ty le ghep {d.ty_le_ghep:.1%} roi khoi khoang "
            f"{GHEP_MIN:.0%}-{GHEP_MAX:.0%}")
    return KetQuaCong(ma, False, "")


def kiem_song(d: DoDuoc, hom_nay: date) -> tuple[KetQuaCong, ...]:
    """Chay ca ba cong. ⛔ Khong dung o cong dau tien bi do — bao het mot luot."""
    return (cong_1(d, hom_nay), cong_2(d), cong_3(d))


def phai_dung(kq: tuple[KetQuaCong, ...]) -> bool:
    return any(k.do for k in kq)
