"""Cong: lan doc co DU khong? — mot lat hop le van co the THIEU GIA TRI.

★★ VI SAO CONG NAY RA DOI. Lan nap 2026-08-27 ghi **257 gia tri `svc_start`
IT HON** so voi chinh du lieu do khi tinh lai offline. Va do lai thi:

    doc lai ca sheet theo HANG, hai lan cach nhau vai gio: **0 o khac nhau**
    cot canon `AB` co gia tri: 2.370 (ca hai lan) · `AC`: 2.364 (ca hai lan)
    tinh offline tu ban da luu: `svc_start` co gia tri **2.368**
    ma trong kho sau lan nap:                          **2.111**

⇒ So **khong doi**. Lat doc **hop le** — dung so cot, dung so dong, khong loi
HTTP, khong ngoai le. Nhung **257 o ve rong**, va **khong cai gi bao gi**.

⚠ Co che: GIA THUYET, ⛔ chua chung minh. Cot `AB`/`AC` lay tu tab
`[Importrange]PI_Unpivot`; khi `IMPORTRANGE` con dang nap, Sheets tra o **rong**
thay vi bao loi. Cung ho voi `GAP-ORA-08`. Bang chung phu: trong duoi so
(dong ≥ 7784) cot `hd` (canon `S`, tu `PM_Unpivot`) ve **551 gia tri** binh
thuong, con `svc_*` (tu `PI_Unpivot`) chi con **21/278**. Tuc **mot tab am, mot
tab lanh** — ⛔ khong phai ca lat bi cat.

★ Vi sao cac cong cu da co KHONG bat duoc:
  · cong hinh dang (`kiem_header`) — header van dung, no khong doc du lieu
  · cong bon duong               — dung so DONG, khong ai mat dong nao
  · cong Σ tien                  — `svc_*` khong phai tien
  · `pg_verify`                  — so schema, khong so du lieu
Ca bon deu hoi *"co thay loi khong"*. ⇒ Dung ho cong thu 7: **cong phai chung
minh no DA DO DUOC GI**.

⇒ Luat: sau khi doc ca lat, **doc lai vai cot then chot bang mot cau rieng** roi
so SO O CO GIA TRI. Hai lan doc doc lap kho long sai giong nhau; lech thi ⛔
KHONG GHI. Do la mot cau HTTP cho mot cot — re hon nhieu lan mat 257 o im lang.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PhanXuDocDu:
    dat: bool
    ly_do: tuple[str, ...] = ()
    da_do: tuple[str, ...] = ()

    def bao(self) -> str:
        dau = "DAT" if self.dat else "KHONG DAT"
        v = f"cong doc-du: {dau}"
        if self.da_do:
            v += "\n  da do: " + " · ".join(self.da_do)
        if self.ly_do:
            v += "\n  ⛔ " + "\n  ⛔ ".join(self.ly_do)
        return v


@dataclass
class DemCot:
    """So o CO GIA TRI cua mot cot, do hai lan doc doc lap."""
    ten: str
    lan_lat: int          # dem tu lat doc theo HANG
    lan_cot: int          # dem tu cau doc rieng theo COT
    toi_thieu: int = 0    # nguong san, 0 = khong dat nguong


def danh_gia(dem: list[DemCot], dong_doc: int, dong_toi_thieu: int
             ) -> PhanXuDocDu:
    """⛔ Mac dinh KHONG DAT. Chi dat khi chung minh duoc CA BA.

    ⓐ co doc that: du so dong · ⓑ hai lan doc KHOP tung cot · ⓒ khong cot nao
    tut duoi nguong san da khai.
    """
    ly_do: list[str] = []
    da_do: list[str] = []

    if not dem:
        return PhanXuDocDu(False, ("khong do cot nao — cong nay chua do gi",))

    if dong_doc < dong_toi_thieu:
        ly_do.append(f"chi doc {dong_doc} dong, duoi nguong {dong_toi_thieu}")
    da_do.append(f"{dong_doc} dong")

    for c in dem:
        da_do.append(f"{c.ten}={c.lan_lat}")
        if c.lan_lat != c.lan_cot:
            ly_do.append(
                f"cot {c.ten}: doc theo HANG duoc {c.lan_lat} o co gia tri, doc "
                f"theo COT duoc {c.lan_cot} — lech {c.lan_lat - c.lan_cot}. "
                f"Mot trong hai lan doc THIEU, ⛔ khong biet lan nao ⇒ khong ghi")
        if c.toi_thieu and c.lan_lat < c.toi_thieu:
            ly_do.append(
                f"cot {c.ten}: {c.lan_lat} o co gia tri, duoi nguong san "
                f"{c.toi_thieu} — nguon thieu hoac lan doc thieu")

    return PhanXuDocDu(not ly_do, tuple(ly_do), tuple(da_do))


# Nguong san cho cac cot then chot, do 2026-08-27 tren nguon that.
# ⚠ Day la SAN, khong phai gia tri dung: nguon lon dan nen so o chi tang.
# ⛔ Ai ha con so nay xuong de "cho qua" thi dang tat cong.
NGUONG_SAN: dict[str, int] = {
    "S · Budget Code (hd)":   3_300,     # do 3.344
    "H · Payment Type":       3_300,     # do 3.344
    "T · CDT1":               3_300,     # do 3.339
    "AB · svc_start":         2_300,     # do 2.370  <- cot da mat 257 o im lang
    "AC · svc_end":           2_300,     # do 2.364  <- cot da mat 257 o im lang
    "Y · ID Payee":             400,     # do 430
}
