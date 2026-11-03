"""Luat `Final` cua nam khoi trong so ITL Ledge — dang HAM THUAN.

Doc tu CONG THUC THAT (05_DATA_DICTIONARY_ERD v0.7 §DD-I06, file GOC ADJUSTED):

  S  Classifying  = may tra                       (co the = "Need to manual input")
  T  Manual input = NGUOI GO                      (khoi dau la co "Input here")
  U  MID          = if(T="" va S<>"Need to manual input", S,
                       if(T="Input here", "OGA | GAC - Other", T))   <- MAC DINH CUNG
  V  Final        = if(or(S="Need to manual input", len(S)=0), U, S)

★ `Final` CHI CO THE khac `Classifying` khi `Classifying` rong hoac that bai —
  day la HANG DUNG cua cong thuc, khong phai phat hien thuc nghiem. Ai do ty le
  `Classifying != Final` roi coi la bang chung thi dang do mot dieu tat yeu.

★★ CHO NOI THAT. Khi gia tri den tu MAC_DINH_CUNG:
    - `parity` VAN mang no  => khop so cu 100% tung o (QD-ITL-35)
    - `thyt`   = None       => khong vao parity that
    - `may_tu_bia` = True   => work_status='UNMAPPED', vao hang cho (INV-I16)
  Vua khop so, vua khong noi doi. Day la ly do co cot song song.

⚠ AUD-12: `thyt` CHI bien gia tri MAY TU BIA thanh None.
   ⛔ KHONG BAO GIO cham gia tri nguoi go — input trong sheet la SSOT.
"""

from __future__ import annotations

from dataclasses import dataclass

MAC_DINH_CUNG = "OGA | GAC - Other"
KHONG_TRA_LOI = "Need to manual input"
CO_INPUT_HERE = "Input here"

# (ten cot parity, ten cot noi that) — dung thu tu khoi 1..5 cua so ITL Ledge
NAM_KHOI: tuple[tuple[str, str], ...] = (
    ("hd", "hd_thyt"),                 # khoi 1 · Budget Code (HDCode)   · Final tai V
    ("pay_type", "pay_type_thyt"),     # khoi 2 · Loai giao dich         · Final tai Z
    ("cdt1", "cdt1_thyt"),             # khoi 3 · Chu du toan (CDT1)     · Final tai AD
    ("svc_start", "svc_start_thyt"),   # khoi 4 · Bat dau dung dich vu   · Final tai AH
    ("svc_end", "svc_end_thyt"),       # khoi 5 · Ket thuc dung dich vu  · Final tai AL
)

TEN_KHOI: frozenset[str] = frozenset(a for a, _ in NAM_KHOI)


@dataclass(frozen=True)
class KetQuaFinal:
    parity: str | None      # y nhu so, KE CA cho may gan mac dinh
    thyt: str | None        # None o cho may tu bia
    may_tu_bia: bool


def _sach(v: str | None) -> str:
    return "" if v is None else str(v).strip()


def tinh_final(classifying: str | None, manual: str | None) -> KetQuaFinal:
    """Tai hien dung luat cua so. Xem docstring module ve cho noi that."""
    s, t = _sach(classifying), _sach(manual)
    may_tra_loi = bool(s) and s != KHONG_TRA_LOI

    if may_tra_loi:                       # Final = S
        return KetQuaFinal(s, s, False)
    if t == CO_INPUT_HERE:                # MID thay bang MAC DINH CUNG
        return KetQuaFinal(MAC_DINH_CUNG, None, True)
    if t:                                 # nguoi da go -> ton trong nguyen van
        return KetQuaFinal(t, t, False)
    return KetQuaFinal(None, None, False)  # ca hai rong -> KHONG bia ra gi
