"""Thuoc chuan TU SOI truoc khi duoc dung lam thuoc (DoD 5.6 ②).

So dang song: nguoi co the go mot o GIUA hai lan doc cua may. Dong do khong tu
nhat quan nua (`Final` khong con bang `f(Classifying, MID)`), va neu de lai thi
no se lam cong parity do MA KHONG PHAI LOI CODE. Nen loai khoi thuoc chuan,
⛔ nhung khong loai im lang — moi dong bi loai mang mot ly do CO TEN (ACC-4).

Luat `Final` khong viet lai o day — goi lai `fls.ledger.final_rule` de chi co
MOT ban luat trong ca he.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from fls.canon.o_loi import la_o_loi
from fls.ledger.final_rule import TEN_BAY_KHOI, tinh_final


@dataclass(frozen=True)
class KetQuaSoi:
    giu: bool
    ly_do: str        # "" khi giu




def _sach(v: Any) -> str:
    return "" if v is None else str(v).strip()


def soi_mot_dong(khoi: dict[str, tuple[Any, Any, Any, Any]]) -> KetQuaSoi:
    """`khoi` = {ten_khoi: (Classifying, Manual input, MID, Final)}.

    Thieu mot khoi cung la LOAI — thieu du lieu de soi thi khong the ket luan
    "tu nhat quan", va doan la cach nguon AS-IS sinh ra thung rac GAC-OTH.
    """
    thieu = sorted(TEN_BAY_KHOI - set(khoi))
    if thieu:
        return KetQuaSoi(False, f"thieu khoi de soi: {', '.join(thieu)}")
    for ten in sorted(khoi):
        cls, _man, mid, fin = khoi[ten]
        if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
            continue                    # R-ORA-07a: o loi la cau tra loi
        mong = _sach(tinh_final(_sach(cls) or None, _sach(mid) or None))
        if mong != _sach(fin):
            return KetQuaSoi(
                False,
                f"khoi {ten} khong tu nhat quan: Final={_sach(fin)!r} "
                f"nhung f(Classifying, MID)={mong!r} "
                f"(nghi bi go giua hai lan doc)")
    return KetQuaSoi(True, "")


def soi(dong: Iterable[dict[str, tuple[Any, Any, Any, Any]]]
        ) -> tuple[list[dict], list[tuple[dict, str]]]:
    """Tach hai duong: `giu` vao thuoc chuan, `loai` mang ly do.

    ⛔ Tong hai duong LUON bang tong dong vao — khong dong nao roi im lang.
    """
    giu: list[dict] = []
    loai: list[tuple[dict, str]] = []
    for d in dong:
        kq = soi_mot_dong(d)
        (giu.append(d) if kq.giu else loai.append((d, kq.ly_do)))
    return giu, loai
