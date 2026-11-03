"""Mot dong ITL-CANON. Bọc tuple 38 phan tu, truy cap THEO VI TRI.

⛔ CO Y khong co as_dict()/by_name(): khuon co 4 cot AH-AK TRUNG TEN het nhau,
luu theo key la MAT COT trong im lang (DD-I01 khuyet tat 1). Chan tu API.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from fls.canon.spec import CANON_COLS, pos_of

SO_VI_TRI = len(CANON_COLS)   # 38


@dataclass(frozen=True)
class CanonRow:
    vals: tuple[Any, ...]

    @classmethod
    def from_list(cls, vals: Sequence[Any]) -> CanonRow:
        """Do dai PHAI dung 38. Tu pad/cat la cach mat cot trong im lang."""
        if len(vals) != SO_VI_TRI:
            raise ValueError(
                f"dong canon phai co dung {SO_VI_TRI} vi tri, nhan {len(vals)}")
        return cls(tuple(vals))

    def __len__(self) -> int:
        return len(self.vals)

    def at(self, pos: int) -> Any:
        if not 0 <= pos < SO_VI_TRI:
            raise ValueError(f"vi tri phai trong 0..{SO_VI_TRI - 1}, nhan {pos}")
        return self.vals[pos]

    def by_letter(self, letter: str) -> Any:
        return self.vals[pos_of(letter)]

    def as_jsonb_list(self) -> list[Any]:
        """Giu nguyen 38 o, ke ca hai o TRONG Z/AA — de vi tri = chi so."""
        return list(self.vals)
