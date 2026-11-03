"""Dung lai ngay tu ban `.xlsx` bi doc sai bang chu — va CHAN khi khong chac.

★ Van de. Ban `[Master] ITL_Ledge_raw.xlsx` (owner dan 2026-08-26 17:55) mang du
lieu MOI NHAT — 9.967 dong, 23 ky, day den 2026-08 — nhung cot ngay hong:
**5.580 o dang CHUOI + 4.387 o dang NGAY ma 100% co `ngay <= 12`**. Ngay that thi
~61% phai vuot 12, nen ca tap "kieu ngay" do la tap bi HOAN thang<->ngay.

★★ Nhung do ky ra mot dieu quan trong: **hai tap BU TRU HOAN TOAN**.

    o dang CHUOI: phan tu 2 > 12  ->  5.580 / 5.580   (100%)
    o dang NGAY : ngay > 12       ->      0 / 4.387   (  0%)

Chi mot co che giai thich duoc: may doc `M/D/YYYY` duoi bang chu `D/M/Y` —

    D > 12   => khong the la thang => DE LAI DANG CHUOI   (nguyen ven, doc duoc)
    D <= 12  => doc duoc nhung HOAN thang<->ngay          (hoan lai duoc)

⇒ **TUNG O quyet dinh duoc**, khong phai suy luan tren tap. Do la ly do module
nay ton tai thay vi mot cau "chac la hoan".

⚠ CHUNG MINH bang doi chieu doc lap: dung lai het roi so phan bo ky voi ban
SACH (`ITL Ledge` trong file ADJUSTED, 9.219 o ngay nguyen kieu) —
**21/23 ky khop CHINH XAC, lech 0**. Hai ky con lai `[Master]` co NHIEU hon
(2026-07: 686 vs 425 · 2026-08: 487 vs 0) — dung khoang hut da khai truoc do.

⛔ Va module nay KHONG BAO GIO doan. Ba cho no NO TO:
  ① o dang chuoi ma phan tu 2 <= 12  -> khong biet dau la thang => NO
  ② o dang ngay ma `ngay > 12`       -> khong thuoc tap bi hoan => NO
  ③ ca tap khong bu tru              -> `kiem_bu_tru` tra ly do, ⛔ khong sua
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

_MDY = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{4})")


class NgayMoHo(ValueError):
    """O ngay khong tu quyet dinh duoc. ⛔ Khong doan — INV-I16."""


@dataclass(frozen=True)
class BuTru:
    chuoi_ro: int          # o chuoi co phan tu 2 > 12  -> chac chan M/D/Y
    chuoi_mo_ho: int       # o chuoi co phan tu 2 <= 12 -> KHONG quyet dinh duoc
    ngay_hoan: int         # o kieu ngay co ngay <= 12  -> thuoc tap bi hoan
    ngay_ro: int           # o kieu ngay co ngay > 12   -> KHONG bi hoan
    khong_doc_duoc: int

    @property
    def bu_tru(self) -> bool:
        """Hai tap bu tru hoan toan ⇒ tung o quyet dinh duoc."""
        return self.chuoi_mo_ho == 0 and self.ngay_ro == 0

    def ly_do(self) -> str:
        if self.bu_tru:
            return ""
        v = []
        if self.chuoi_mo_ho:
            v.append(f"{self.chuoi_mo_ho} o chuoi co ca hai phan tu <= 12 "
                     f"(khong biet dau la thang)")
        if self.ngay_ro:
            v.append(f"{self.ngay_ro} o kieu ngay co ngay > 12 "
                     f"(khong thuoc tap bi hoan)")
        return " · ".join(v)


def kiem_bu_tru(o: Iterable[Any]) -> BuTru:
    """Do truoc khi dung lai. ⛔ Khong bu tru thi ⛔ khong duoc dung `doc_ngay`."""
    cr = cm = nh = nr = kd = 0
    for v in o:
        if v is None or (isinstance(v, str) and not v.strip()):
            continue
        if isinstance(v, (datetime, date)):
            d = v.date() if isinstance(v, datetime) else v
            if d.day > 12:
                nr += 1
            else:
                nh += 1
            continue
        m = _MDY.fullmatch(str(v).strip())
        if not m:
            kd += 1
        elif int(m.group(2)) > 12:
            cr += 1
        else:
            cm += 1
    return BuTru(cr, cm, nh, nr, kd)


def doc_ngay(v: Any) -> date:
    """Mot o -> `date`. ⛔ Khong quyet dinh duoc thi NO, khong tra gia tri gan dung.

    ⚠ Chi dung sau khi `kiem_bu_tru(...).bu_tru` la True cho CA COT.
    """
    if isinstance(v, (datetime, date)):
        d = v.date() if isinstance(v, datetime) else v
        if d.day > 12:
            raise NgayMoHo(
                f"o kieu ngay {d.isoformat()} co ngay > 12 nen KHONG thuoc tap "
                f"bi hoan — hoan lai la lam sai mot o dang dung")
        try:
            return date(d.year, d.day, d.month)      # hoan lai thang <-> ngay
        except ValueError as e:
            raise NgayMoHo(f"hoan lai {d.isoformat()} khong ra ngay hop le: {e}") from e
    m = _MDY.fullmatch(str(v).strip()) if v is not None else None
    if not m:
        raise NgayMoHo(f"khong doc duoc o ngay: {v!r}")
    thang, ngay, nam = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if ngay <= 12:
        raise NgayMoHo(
            f"o chuoi {v!r} co ca hai phan tu <= 12 — khong biet dau la thang")
    try:
        return date(nam, thang, ngay)
    except ValueError as e:                  # 31/31/2026, 2/30/2026...
        raise NgayMoHo(f"o chuoi {v!r} khong phai ngay hop le: {e}") from e
