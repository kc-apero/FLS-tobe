"""Cong: kho THAT chi duoc chua dong cua lan nap THAT.

⛔⛔ **Vi sao cong nay ra doi, 2026-08-27.** Dem `fls_itl` ra **11.177 dong**
trong khi moi tai lieu ghi **9.973**. Truy ra: nam file test PG lay MAC DINH
dung dia chi kho that, nen mot lenh `pytest` tron **ghi thang vao so**:

    fls_itl   : 9.973 THAT + **1.204 dau test**   (1.285.475.949 tien BIA
                                                   canh 1.214 ty tien that)
    fls_reject:    19 THAT + **  106 dau test**
    fls_run   :     1 THAT + **227 lan chay test**
    hang cho  : 7.625 THAT + **  194 dau test**

★ Con so trong tai lieu **van dung** — chung duoc tinh CO LOC theo lan nap.
Cho hong la **khong gi bat buoc phai loc**, va `P4` (cua doc) + `P6` (man `F01`)
doc dung bang nay ⇒ **man dau tien ke toan nhin thay se co 194 dong bia trong
danh sach viec phai lam**, khong cong nao bao gi.

**Luat la BAN TRANG, khong phai ban den.** Mot lan nap la THAT khi `run_id`
khop `HINH_RUN_THAT`; moi thu khac trong kho that la **vi pham**. Ban den
(*"loai cai gi ra"*) se hong ngay lan sau co mot tien to test moi.

⛔ Cong **mac dinh KHONG DAT** (cong chung #7): dem duoc 0 dong ⇒ **DO**, vi
*"khong do duoc gi"* ⛔ khong phai *"sach"*. Va no **in ra da do duoc gi**.

⚠ Cong nay ⛔ KHONG don dep. Don dau test la viec cua **dung lai kho** (DDL
drop/create database) — ⛔ khong bao gio bang mot cau `DELETE` len `fls_itl`
(`INV-I08` append-only).
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field

# `NAP-<yyyy>-<mm>-<dd>-<NGUON>` — vd `NAP-2026-08-27-RAW`
HINH_RUN_THAT = re.compile(r"^NAP-\d{4}-\d{2}-\d{2}-[A-Z0-9]+$")

# Ba bang mang `run_id`. Thieu mot bang o day = mot cho khong ai canh.
BANG_CO_RUN: tuple[str, ...] = ("fls_itl", "fls_reject", "fls_run")

# Duoi nguong nay thi cong coi nhu CHUA DO DUOC GI (khong phai "sach").
DONG_TOI_THIEU = 1_000


# ⭐ NGAY trong `run_id` phai hop ly. Them 27/08, va ly do rat cu the:
#
# Cua doc `P4` loc theo pham vi bang **HINH DANG** `run_id` (mot cau SQL `~`
# khong goi duoc ham Python), nen moi bai test can thay dong cua minh qua pham
# vi *"chi lan nap that"* deu phai dat mot `run_id` HINH DANG THAT. Neu chi co
# ban trang hinh dang thi tu day tro di **dau test trong y nhu lan nap that**,
# va cong nay MU dung cai no sinh ra de bat.
#
# ⇒ Them mot phep kiem **chi o tang cong** (Python, khong vao SQL): ngay phai
#   nam trong khoang song cua so. So bat dau 2024-10-21; de bien 2024-01-01.
#   Bo test dung nam **2000** ⇒ qua duoc pham vi (hinh dang dung) nhung ⛔
#   KHONG qua duoc cong kho sach. Do la cho phan biet duy nhat con lai.
NGAY_SOM_NHAT = _dt.date(2024, 1, 1)


def ngay_cua_run(run_id: str | None) -> _dt.date | None:
    """Ngay nhung trong `run_id`, hay `None` neu khong doc duoc."""
    m = HINH_RUN_THAT.match(run_id or "")
    if not m:
        return None
    try:
        return _dt.date.fromisoformat(run_id[4:14])
    except ValueError:
        return None


def ngay_hop_ly(run_id: str | None, hom_nay: _dt.date | None = None) -> bool:
    """Ngay trong `run_id` co nam trong khoang song cua so khong.

    ⛔ Phep kiem nay CHI dung o cong kho sach, ⛔ khong dung lam pham vi doc:
    pham vi phai dien dat duoc bang mot cau SQL, va mot cau SQL khong goi duoc
    ham nay.
    """
    ng = ngay_cua_run(run_id)
    if ng is None:
        return False
    return NGAY_SOM_NHAT <= ng <= (hom_nay or _dt.date.today()) + _dt.timedelta(days=1)


def la_run_that(run_id: str | None) -> bool:
    """⛔ Ban TRANG: chi `NAP-yyyy-mm-dd-NGUON` moi la lan nap that."""
    return bool(run_id) and bool(HINH_RUN_THAT.match(run_id or ""))


@dataclass(frozen=True)
class DemBang:
    """So dong theo tung `run_id` trong MOT bang."""

    bang: str
    theo_run: tuple[tuple[str | None, int], ...]

    @property
    def tong(self) -> int:
        return sum(n for _, n in self.theo_run)

    @property
    def la(self) -> tuple[tuple[str | None, int], ...]:
        """Cac run KHONG phai lan nap that."""
        return tuple((r, n) for r, n in self.theo_run if not la_run_that(r))

    @property
    def dong_la(self) -> int:
        return sum(n for _, n in self.la)


@dataclass(frozen=True)
class PhanXu:
    dat: bool
    ly_do: tuple[str, ...] = field(default_factory=tuple)
    da_do: tuple[str, ...] = field(default_factory=tuple)

    def bao(self) -> str:
        dong = [("✅ KHO SACH" if self.dat else "⛔ KHO KHONG SACH")]
        if self.da_do:
            dong.append("  da do: " + " · ".join(self.da_do))
        for x in self.ly_do:
            dong.append("  - " + x)
        return "\n".join(dong)


def danh_gia(dem: list[DemBang], dong_toi_thieu: int = DONG_TOI_THIEU) -> PhanXu:
    """⛔ Mac dinh KHONG DAT. Chi dat khi chung minh duoc CA BA dieu.

    ⓐ da dem that (>= `dong_toi_thieu` dong o `fls_itl`)
    ⓑ da soi du ca `BANG_CO_RUN` — thieu mot bang la mot cho khong ai canh
    ⓒ khong bang nao chua dong cua run la
    """
    ly_do: list[str] = []
    da_do = tuple(f"{d.bang}={d.tong}" for d in dem)

    da_soi = {d.bang for d in dem}
    thieu = [b for b in BANG_CO_RUN if b not in da_soi]
    if thieu:
        ly_do.append(f"chua soi bang: {', '.join(thieu)} — ⛔ khong duoc noi 'ca kho'")

    itl = next((d for d in dem if d.bang == "fls_itl"), None)
    if itl is None:
        ly_do.append("khong do duoc fls_itl — ⛔ khong do duoc gi thi KHONG DAT")
    elif itl.tong < dong_toi_thieu:
        ly_do.append(f"fls_itl chi co {itl.tong} dong < nguong {dong_toi_thieu} "
                     f"⇒ chua do duoc gi (⛔ khong phai 'sach')")

    # ⭐ Ngay trong `run_id` phai hop ly — bat dau test mang hinh dang that
    # (vd `NAP-2000-01-01-THU`) di qua duoc pham vi doc nhung ⛔ khong qua duoc
    # cong nay.
    for d in dem:
        ngay_xau = [(r, n) for r, n in d.theo_run
                    if la_run_that(r) and not ngay_hop_ly(r)]
        if ngay_xau:
            ct = ", ".join(f"{r!r}×{n}" for r, n in ngay_xau[:5])
            ly_do.append(f"{d.bang}: {sum(n for _, n in ngay_xau)} dong co "
                         f"`run_id` dung hinh dang ma NGAY vo ly ({ct}) — so "
                         f"bat dau {NGAY_SOM_NHAT}, khong the co lan nap truoc do")

    for d in dem:
        if d.dong_la:
            chi_tiet = ", ".join(f"{r!r}×{n}" for r, n in d.la[:5])
            them = " …" if len(d.la) > 5 else ""
            ly_do.append(f"{d.bang}: {d.dong_la} dong cua {len(d.la)} run KHONG "
                         f"phai lan nap that ({chi_tiet}{them})")

    return PhanXu(dat=not ly_do, ly_do=tuple(ly_do), da_do=da_do)


def do(conn) -> list[DemBang]:
    """Dem `run_id` tren kho dang mo. ⛔ Chi DOC, khong ghi gi."""
    dem: list[DemBang] = []
    for bang in BANG_CO_RUN:
        rows = conn.execute(
            f"select run_id, count(*) from {bang} group by 1 order by 2 desc"
        ).fetchall()
        dem.append(DemBang(bang=bang, theo_run=tuple((r, int(n)) for r, n in rows)))
    return dem


def kiem(conn, dong_toi_thieu: int = DONG_TOI_THIEU) -> PhanXu:
    return danh_gia(do(conn), dong_toi_thieu)
