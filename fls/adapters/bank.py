"""Adapter B — Cash/Bank: `Transaction Mapping L1` -> ITL-CANON 38 vi tri.

Nguon: `nguon.BAN_SAO_RAW` (QD-ITL-50). Header o dong 3, du lieu tu dong **5**
(dong 4 TRONG — off-by-one nay tung nam trong spec v1.0 va lam roi 1 dong).

Sau dieu kien xong cua DoD 5.7, moi cai deu co test:
  ① xuat dung 38 vi tri + provenance      -> `dung_canon`
  ② parity 100% tung o, ⛔ cam dung sai    -> khong bien doi gia tri nao o day
  ③ so dong khop nguon; lech phai PHAN LOAI DUOC -> `ThongKe` ba duong
  ④ nguon doi hinh dang thi NO TO         -> `kiem_header`
  ⑤ idempotent — chay lai khong nhan doi   -> ham thuan, khong trang thai
  ⑥ nguon thieu truong => trong CO KIEM SOAT, ⛔ khong bia (P-ITL-05)

★ Vi sao adapter nay KHONG chuan hoa gia tri. Cong ra cua P2 la "parity 100%
tung o". Moi phep lam sach o day deu la mot cho parity co the do vi LOI CUA TA
chu khong phai loi cua so. Chuan hoa thuoc `canon.validate` (duong LOAI/CHO),
⛔ khong thuoc duong chep.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from fls.canon.o_loi import la_o_loi
from fls.canon.row import SO_VI_TRI, CanonRow
from fls.canon.spec import CANON_COLS
from fls.oracle.nguon import (BAN_SAO_RAW, COT_LOI_LA_LOI_THAT,
                              COT_RONG_CO_Y)


class NguonDoiHinhDang(RuntimeError):
    """④ Nguon doi cot thi NO TO. ⛔ Khong doan, khong am tham bo cot."""


@dataclass(frozen=True)
class ThongKe:
    """③ Ba duong. `tong()` PHAI bang so dong vao — khong dong nao roi im lang."""
    vao: int
    ra: int          # thanh CanonRow
    loai: int        # o loi o cot goc => fls_reject, ly do CO TEN
    rong: int        # dong trong cua sheet (khong phai du lieu)

    def tong(self) -> int:
        return self.ra + self.loai + self.rong

    def can(self) -> bool:
        return self.tong() == self.vao


def kiem_header(hang3: Sequence[Any]) -> None:
    """④ So header cua sheet voi khuon canon. Lech MOT ten la NO TO.

    ⛔ Khong so "gan giong": khuon nay co 4 cot TRUNG TEN va 2 cot TRONG, nen
    doi chieu long tay la mat cot trong im lang.
    """
    thay = [("" if x is None else str(x)).replace("\n", " ").strip()
            for x in hang3]
    thay += [""] * (SO_VI_TRI - len(thay))
    if len(thay) > SO_VI_TRI:
        raise NguonDoiHinhDang(
            f"nguon co {len(thay)} cot, khuon canon co {SO_VI_TRI}")
    lech = [(c.pos, c.letter, c.name, thay[c.pos])
            for c in CANON_COLS if thay[c.pos] != c.name]
    if lech:
        chi_tiet = " · ".join(
            f"{lt}(vi tri {p}): mong {mong!r} thay {co!r}"
            for p, lt, mong, co in lech[:5])
        raise NguonDoiHinhDang(
            f"{len(lech)} cot lech ten so voi ITL-CANON: {chi_tiet}")




def dong_rong(hang: Sequence[Any]) -> bool:
    """Dong trong cua sheet: 7 cot goc BASE deu khong co gi."""
    return all(x in (None, "") for x in list(hang)[:7])


def dung_canon(hang: Sequence[Any]) -> tuple[CanonRow | None, list[str]]:
    """Mot dong tho -> (CanonRow, ly_do_loai). ⛔ Khong doi mot gia tri nao.

    Ba luat cot cua `nguon.py` duoc ap o day:
      COT_LOI_LA_LOI_THAT  o loi => LOAI, ly do CO TEN
      COT_RONG_CO_Y        Z/AA  => luon None, van giu vi tri (R-ORA-07c)
      con lai              `#N/A` => None CO KIEM SOAT (R-ORA-07a), ⛔ khong loai
    """
    o = list(hang)[:SO_VI_TRI]
    o += [None] * (SO_VI_TRI - len(o))          # ⑥ thieu => trong, ⛔ khong bia

    ly_do: list[str] = []
    for pos in sorted(COT_LOI_LA_LOI_THAT):
        if la_o_loi(o[pos]):
            c = CANON_COLS[pos]
            ly_do.append(f"cot goc {c.letter} ({c.name!r}) la o loi: {o[pos]}")
    if ly_do:
        return None, ly_do

    for pos in COT_RONG_CO_Y:
        o[pos] = None
    for pos, v in enumerate(o):
        if la_o_loi(v):
            o[pos] = None                        # R-ORA-07a
    return CanonRow.from_list(o), []


def nap(tho: Iterable[Sequence[Any]], header: Sequence[Any] | None = None
        ) -> tuple[list[tuple[int, CanonRow]], list[tuple[int, list[str]]], ThongKe]:
    """Nap ca lat. Tra (dong canon KEM SO DONG SHEET, dong bi loai kem ly do, ba duong).

    `header` khai bao thi kiem truoc — ⑤ ham thuan, chay lai cho ket qua y het.

    ⚠ Dong duoc giu mang **so dong that cua sheet** y nhu dong bi loai. Ban dau
    chi dong BI LOAI mang so dong; dong duoc GIU thi khong. Nhung `source_row`
    la mot phan cua lineage `INV-I05`/`I12` — thieu no thi tang ghi phai TU DANH
    SO, va tu danh so la dung lai loi AS-IS (`="ITL#"&ROW()` tren bang da SORT).
    """
    if header is not None:
        kiem_header(header)

    ra: list[tuple[int, CanonRow]] = []
    loai: list[tuple[int, list[str]]] = []
    vao = rong = 0
    for i, hang in enumerate(tho):
        vao += 1
        dong_sheet = BAN_SAO_RAW.dong_dau + i
        if dong_rong(hang):
            rong += 1
            continue
        row, ly_do = dung_canon(hang)
        if row is None:
            loai.append((dong_sheet, ly_do))
        else:
            ra.append((dong_sheet, row))
    tk = ThongKe(vao=vao, ra=len(ra), loai=len(loai), rong=rong)
    if not tk.can():
        raise AssertionError(                       # ⛔ khong bao gio duoc xay ra
            f"ba duong khong can: vao {tk.vao} != {tk.tong()} "
            f"(ra {tk.ra} + loai {tk.loai} + rong {tk.rong})")
    return ra, loai, tk
