# -*- coding: utf-8 -*-
"""`IX.ORG` — **tổ chức**: `CDT nguồn → CDT1 chuẩn` + `TK → LE` *(ISP 3.1.2 · Step 22 ·
`C8` · `WO-176`)*. Tầng CONFIG THUẦN: ảnh/bản config được TRUYỀN VÀO, ⛔ biết kho
*(`.importlinter` hợp đồng 10)*; ghi/đọc kho + sự kiện hàng chờ ở `fls/repo/cau_hinh_repo.py`.

⛔⛔ **Vì sao CDT lạ ⛔ được rơi về `SHQ2`.** Sheet NOW tra `CDT Correct` *(`BR11:BS28`)* và
   **mặc định `SHQ2`** khi ⛔ thấy — một CDT gõ sai thành ra **CDT1 của Headquarters2**, im
   lặng, và mọi phân bổ theo tỷ trọng CDT1 chảy sai chỗ. ⇒ `cdt_cua` trả
   `KetQuaCDT(cdt1=None, la=True)`; người gọi *(repo)* ghi sự kiện hàng chờ `CDT_LA`.

⭐ Pháp nhân: **dùng lại** `fls.canon.le.ma_le` *(hai hình dạng mã LE — ⛔ bảng LE mới)*.

⭐ **Đo trên ảnh đóng băng 18/11 — mỗi số NÓI NÓ ĐẾM GÌ** *(`Đ4`; KHÁC số ISP ghi)*:
   `13` dòng ảnh CDT Correct *(ISP: `18` = bề vùng sheet)* · `7` CDT1 chuẩn khác nhau
   *(ISP: `8` — `CMN_Management` chỉ là nhãn NGUỒN, chuẩn hoá về `SHQ1`)* · `69` hàng TK
   `R |` = `59` pháp nhân + `8` nhãn `CN` + `2` `Cash Treasury`.

⛔ **Riêng tư.** Kho CHỈ nhận TK của **pháp nhân**. Loại: hàng `an_danh:tk_ca_nhan` *(DT3
   đã giả danh hoá — ⛔ băm, ⛔ nối: owner quyết)*, nhãn `CN` *(số TK cá nhân)*, `Cash
   Treasury` *(⛔ phải pháp nhân — `INV-I10`)*.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from fls.canon.le import ma_le

BANG = "IX.ORG"
TIEN_TO_CDT = "cdt:"
TIEN_TO_TK = "tk:"
LOAI_SU_KIEN = "CDT_LA"

# Tên lỗi — hằng chuỗi *(luật `S0-R1-04`: một dòng, đọc được)*.
ORG_HONG = "ORG_HONG"
CDT_RONG = "CDT_RONG"
CDT_TRUNG = "CDT_TRUNG"
TK_RONG = "TK_RONG"
TK_TRUNG = "TK_TRUNG"

_TIEN_TO_TK_ANH = "R | "
_AN_DANH = "an_danh:tk_ca_nhan"
_KHONG_PHAI_PHAP_NHAN = frozenset({"CN", "Cash Treasury"})


class LoiToChuc(ValueError):
    """Ảnh/bản `IX.ORG` hỏng. `ma` là một hằng ở trên."""

    def __init__(self, ma: str, ly_do: str) -> None:
        self.ma = ma
        super().__init__(f"⛔ IX.ORG {ma}: " + " ".join(ly_do.split()))


@dataclass(frozen=True)
class ToChuc:
    nguon: str
    cdt: Mapping[str, str]        # CDT nguồn → CDT1 chuẩn
    tk_le: Mapping[str, str]      # TK → mã LE (pháp nhân)


@dataclass(frozen=True)
class KetQuaCDT:
    cdt1: str | None              # None khi lạ — ⛔ KHÔNG BAO GIỜ 'SHQ2 | Headquarters2'
    la: bool


def _chu(o: Any) -> str | None:
    c = o.get("chu") if isinstance(o, Mapping) else o
    return c.strip() if isinstance(c, str) and c.strip() else None


def _tai(van: str, nguon: str) -> Mapping[str, Any]:
    try:
        d = json.loads(van)
    except (ValueError, RecursionError) as e:
        raise LoiToChuc(ORG_HONG, f"{nguon}: JSON hỏng — {e}") from None
    if not isinstance(d, Mapping) or not isinstance(d.get("dong"), list):
        raise LoiToChuc(ORG_HONG, f"{nguon}: ⛔ phải {{dong: [...]}}")
    return d


def doc_cdt_correct(van: str, *, nguon: str) -> tuple[tuple[str, str], ...]:
    """Ảnh CDT Correct ⇒ `(cdt_nguon, cdt1_chuan)` theo thứ tự ảnh."""
    d = _tai(van, nguon)
    cap: list[tuple[str, str]] = []
    for i, r in enumerate(d["dong"], start=1):
        n = _chu(r.get("cdt_nguon")) if isinstance(r, Mapping) else None
        c = _chu(r.get("cdt1_chuan")) if isinstance(r, Mapping) else None
        if n is None or c is None:
            raise LoiToChuc(ORG_HONG, f"{nguon}: dòng {i} thiếu cdt_nguon/cdt1_chuan")
        cap.append((n, c))
    if not cap:
        raise LoiToChuc(CDT_RONG, f"{nguon}: 0 dòng ⇒ ⛔ có gì để tra "
                                  f"*(mọi CDT sẽ thành lạ)*")
    trung = sorted({n for n, _ in cap if [x for x, _ in cap].count(n) >= 2})
    if trung:
        raise LoiToChuc(CDT_TRUNG, f"{nguon}: cdt_nguon trùng {trung}")
    return tuple(cap)


def doc_tk_le(van: str, *, nguon: str) -> tuple[tuple[str, str], ...]:
    """Bảng phụ `tho` của Mapping Master (cột A:B) ⇒ `(tk, ma_le)` — CHỈ pháp nhân."""
    d = _tai(van, nguon)
    phu = d.get("phu")
    tho = phu.get("tho") if isinstance(phu, Mapping) else None
    if not isinstance(tho, Mapping) or not isinstance(tho.get("dong"), list):
        raise LoiToChuc(ORG_HONG, f"{nguon}: thiếu phu.tho.dong")
    cap: list[tuple[str, str]] = []
    for r in tho["dong"]:
        a = _chu(r.get("A")) if isinstance(r, Mapping) else None
        if a is None or a == _AN_DANH or not a.startswith(_TIEN_TO_TK_ANH):
            continue
        le = ma_le(_chu(r.get("B")))
        if le is None or le in _KHONG_PHAI_PHAP_NHAN:
            continue
        cap.append((a, le))
    if not cap:
        raise LoiToChuc(TK_RONG, f"{nguon}: 0 TK pháp nhân")
    trung = sorted({t for t, _ in cap if [x for x, _ in cap].count(t) >= 2})
    if trung:
        raise LoiToChuc(TK_TRUNG, f"{nguon}: TK trùng {trung}")
    return tuple(cap)


def dung(cdt: tuple[tuple[str, str], ...], tk_le: tuple[tuple[str, str], ...],
         *, nguon: str) -> ToChuc:
    return ToChuc(nguon=nguon, cdt=MappingProxyType(dict(cdt)),
                  tk_le=MappingProxyType(dict(tk_le)))


def doc_anh(van_cdt: str, van_mm: str, *, nguon: str) -> ToChuc:
    return dung(doc_cdt_correct(van_cdt, nguon=nguon),
                doc_tk_le(van_mm, nguon=nguon), nguon=nguon)


def cdt_cua(kho: ToChuc, cdt_nguon: object) -> KetQuaCDT:
    """CDT1 chuẩn của một CDT nguồn. Một giá trị đã LÀ CDT1 chuẩn thì ⛔ lạ.
    ⛔ Lạ ⇒ `cdt1=None, la=True` — KHÔNG mặc định `SHQ2`."""
    c = cdt_nguon.strip() if isinstance(cdt_nguon, str) else ""
    if c in kho.cdt:
        return KetQuaCDT(kho.cdt[c], False)
    if c and c in set(kho.cdt.values()):
        return KetQuaCDT(c, False)
    return KetQuaCDT(None, True)


def le_cua(kho: ToChuc, tk: str) -> str | None:
    """Mã LE của một TK pháp nhân; ⛔ có ⇒ `None` *(⛔ đoán)*."""
    return kho.tk_le.get(tk)
