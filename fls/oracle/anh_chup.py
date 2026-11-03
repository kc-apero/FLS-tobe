"""Anh chup DONG BANG cua so goc — hien vat de doi chieu, khong phai ban tam.

`checksum` co mot yeu cau nghe la nguoc: no phai KHONG doi khi `run_id`/ngay
chup doi, va KHONG doi khi thu tu doc doi. Ly do: cong "chup 2 lan cach nhau
-> checksum khop" (DoD 5.6) chi co nghia neu checksum do NOI DUNG, khong do
hoan canh. Ma noi dung thi phai doc tang dan / cat lat — nen thu tu la ngau
nhien, khong duoc tinh vao.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping


@dataclass(frozen=True)
class AnhChup:
    run_id: str
    ngay: date
    nguon: str
    dong: tuple[Mapping[str, Any], ...]

    def checksum(self) -> str:
        """sha256 cua noi dung, doc lap voi thu tu doc va voi lan chay.

        ⛔ Anh chup rong thi NO TO. Tra checksum cua rong la cach mot luot doc
        that bai bien thanh mot hien vat trong "hop le" — dung kieu loi im lang
        ma ca he nay dung de chan.
        """
        if not self.dong:
            raise ValueError("anh chup rong: khong co dong nao de bang bam")
        van = sorted(
            json.dumps(d, ensure_ascii=False, sort_keys=True, default=str)
            for d in self.dong)
        h = hashlib.sha256(self.nguon.encode("utf-8"))
        for v in van:
            h.update(b"\x1f")
            h.update(v.encode("utf-8"))
        return h.hexdigest()
