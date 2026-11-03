"""Cac ham xu ly cua `P4` (doc) + `P5` (ghi). ⛔ **Khong luat nghiep vu o day.**

`03_Dev/03` §5.8 ①: *"router mong, ⛔ khong chua luat — luat o `ledger`/`canon`"*.
Nen moi ham o day chi lam ba viec: doc tham so, goi `fls.repo.*`, don hinh dang
cho JSON. Neu mot ham o day bat dau tinh toan gi thi phep tinh do dat sai cho.

★ Pham vi khong phai tham so cua nguoi goi. Nguoi goi ⛔ khong duoc chon doc
ca kho — `pham_vi_cua_yeu_cau` chi tra hai kha nang: ban trang, hay mot lan nap
CU THE (van qua ban trang). Xem `pham_vi.py`.

★★ **`actor` den TU THE, ⛔ khong tu than yeu cau.** Ham ghi lay `yc.actor` —
tang cua da boc no ra tu the truoc khi goi. Neu de nguoi goi tu khai `actor`
trong than yeu cau thi nhat ky khong con la nhat ky (`AUD-1`), va sau khi
`QĐ-ITL-27` khai tu vai nguoi hau kiem thi do la **lop kiem soat duy nhat con
lai**.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Callable

from fls.repo import doc_bao_cao as bc
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import PhamVi, chi_nap_that, mot_lan_nap


class LoiCua(Exception):
    """Loi mang san ma cua `bao.MA_LOI` + phan `them` de tra ra ngoai."""

    def __init__(self, ma: str, chi_tiet: str = "", **them: Any) -> None:
        super().__init__(ma)
        self.ma = ma
        self.chi_tiet = chi_tiet
        self.them = them


@dataclass(frozen=True)
class YeuCau:
    """Moi thu mot ham xu ly duoc phep biet. ⛔ Khong hon."""

    conn: Any
    pv: PhamVi
    q: dict[str, str]
    tham: dict[str, str]
    actor: str = ""
    than: dict[str, Any] = field(default_factory=dict)


def pham_vi_cua_yeu_cau(q: dict[str, str]) -> PhamVi:
    """⛔ Chi hai kha nang. `?run_id=` la giao voi ban trang, khong thay the no.

    ⛔ ⛔ Khong co `?pham_vi=ca_kho`. Doc ca kho la viec cua cong cu soi kho,
    ⛔ khong bao gio la viec cua mot cua HTTP — day la duong ma 194 dong dau
    test se di ra man hinh.
    """
    run = (q.get("run_id") or "").strip()
    return mot_lan_nap(run) if run else chi_nap_that()


# ── boc tham so ───────────────────────────────────────────────────────────
def _so_nguyen(nguon: dict[str, Any], ten: str) -> int | None:
    v = nguon.get(ten)
    v = "" if v is None else str(v).strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        raise LoiCua("FLS-BAD-REQUEST", f"{ten}={v!r} khong phai so nguyen") from None


def _bat_buoc_int(tham: dict[str, str], ten: str) -> int:
    try:
        return int(tham[ten])
    except (KeyError, ValueError):
        raise LoiCua("FLS-BAD-REQUEST", f"{ten} phai la so nguyen") from None


def _thap_phan(q: dict[str, str], ten: str) -> Decimal | None:
    v = (q.get(ten) or "").strip()
    if not v:
        return None
    try:
        return Decimal(v)
    except InvalidOperation:
        raise LoiCua("FLS-BAD-REQUEST", f"{ten}={v!r} khong phai so") from None


def _chu(than: dict[str, Any], ten: str, *, bat_buoc: bool = True) -> str:
    v = than.get(ten)
    if v is None:
        v = ""
    if not isinstance(v, (str, int, float)):
        raise LoiCua("FLS-BAD-REQUEST", f"`{ten}` phai la chuoi")
    v = str(v).strip()
    if bat_buoc and not v:
        raise LoiCua("FLS-BAD-REQUEST", f"thieu `{ten}`")
    return v


def _co(q: dict[str, str], than: dict[str, Any], ten: str) -> bool:
    """Co bat/tat: nhan tu ca URL lan than. ⛔ Chi `true`/`1` la bat."""
    v = str(q.get(ten, than.get(ten, ""))).strip().lower()
    return v in {"true", "1", "yes"}


def _co_flash(dong: list[dict[str, Any]]) -> str:
    """⛔ Mac dinh `flash`. Chi len `reconciled` khi CHUNG MINH duoc ca trang
    da khong con co flash — va trang rong thi ⛔ khong chung minh duoc gi."""
    if not dong or any(d.get("is_flash", True) for d in dong):
        return "flash"
    return "reconciled"


def _trang_ra(t: bc.Trang) -> dict[str, Any]:
    return {"rows": t.dong, "next_cursor": t.con_tro, "count": len(t.dong)}


def _dich_loi_ghi(e: gt.LoiGhi) -> LoiCua:
    """Loi tang ghi → ma HTTP. ⛔ Ma nam o tang ghi, ⛔ khong doan lai o day."""
    return LoiCua(e.ma, str(e), **e.them)


# ── P4 · doc ──────────────────────────────────────────────────────────────
def so(yc: YeuCau):
    try:
        t = bc.doc_so(yc.conn, yc.pv, period=yc.q.get("period") or None,
                      le=yc.q.get("le") or None,
                      status=yc.q.get("status") or None,
                      con_tro=yc.q.get("cursor") or None,
                      limit=_so_nguyen(yc.q, "limit"))
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    return _trang_ra(t), _co_flash(t.dong)


def mot_dong(yc: YeuCau):
    i = _bat_buoc_int(yc.tham, "itl_id")
    d = bc.doc_mot_dong(yc.conn, yc.pv, i)
    if d is None:
        # ⛔ Cung mot cau tra loi cho "khong co" va "co nhung ngoai pham vi".
        raise LoiCua("FLS-NOT-FOUND", f"itl_id={i} ngoai {yc.pv.mo_ta()}")
    return d, _co_flash([d])


def hang_cho(yc: YeuCau):
    try:
        t = bc.doc_hang_cho(yc.conn, yc.pv, curr=yc.q.get("curr") or None,
                            den_pct=_thap_phan(yc.q, "den_pct"),
                            con_tro=yc.q.get("cursor") or None,
                            limit=_so_nguyen(yc.q, "limit"))
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    return _trang_ra(t), "flash"


def hang_cho_tom(yc: YeuCau):
    # ⛔ Tra danh sach theo tung tien te, ⛔ khong co dong "tong".
    return {"theo_tien_te": bc.dem_hang_cho(yc.conn, yc.pv)}, "flash"


def do_phu(yc: YeuCau):
    """Do phu hang cho theo TUNG tien te (`P6·B3`).

    `?muc_pct=` mac dinh **90**. ⛔ Gia tri la ⇒ `400`, ⛔ khong am tham quay ve
    90: mot man hinh hoi *"phu 150 phan tram can may dong"* dang hoi nham, va
    tra ve con so cua 90 thi ⛔ khong ai biet cau hoi da bi doi.
    """
    tho = str(yc.q.get("muc_pct", "")).strip()
    try:
        muc = Decimal(tho) if tho else Decimal(90)
    except InvalidOperation:
        raise LoiCua("FLS-BAD-REQUEST",
                     f"`muc_pct={tho}` khong phai mot so") from None
    try:
        hang = bc.do_phu_hang_cho(yc.conn, yc.pv, muc)
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    # ⛔⛔ ⛔ Khong co dong "tong" — cong hai don vi tien te ra mot con so la vo
    # nghia (`dem_hang_cho`). Va `muc_pct` tra ra CUNG, de man hinh noi duoc no
    # dang ve muc NAO thay vi ngam dinh 90 tren nhan.
    return {"muc_pct": str(muc), "theo_tien_te": hang}, "flash"


def nhat_ky(yc: YeuCau):
    i = _so_nguyen(yc.q, "itl_id")
    if i is None:
        raise LoiCua("FLS-BAD-REQUEST", "thieu ?itl_id=")
    return {"rows": bc.doc_nhat_ky(yc.conn, yc.pv, i)}, "flash"


def cong(yc: YeuCau):
    c = bc.doc_cong(yc.conn, yc.pv)
    ra = [{"ma": x.ma, "ten": x.ten, "dat": x.dat, "nhan": x.nhan,
           "da_do": x.da_do, "ly_do": x.ly_do} for x in c]
    return {"cong": ra,
            "dat": sum(1 for x in c if x.dat is True),
            "khong_dat": sum(1 for x in c if x.dat is False),
            # ⛔ Con so nay PHAI ra cung cho: mot man hinh noi "2/2 xanh" trong
            # khi 4 cong ke toan chua he do la con so noi doi.
            "chua_do_duoc": sum(1 for x in c if x.dat is None)}, "flash"


# ── P5 · ghi ──────────────────────────────────────────────────────────────
def truoc_khi_go(yc: YeuCau):
    """*"Nguon noi gi"* — man hinh goi TRUOC khi cho nguoi go (`US-025`)."""
    i = _bat_buoc_int(yc.tham, "itl_id")
    try:
        t = gt.truoc_khi_go(yc.conn, yc.pv, i, yc.tham.get("field", ""))
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    d = t.pop("dong")
    t["period_state"] = d["period_state"]
    t["work_status"] = d["work_status"]
    return t, "flash"


def sua(yc: YeuCau):
    """Nguoi go mot trong 10 truong. `409` neu khac nguon ma chua `force`."""
    i = _bat_buoc_int(yc.tham, "itl_id")
    truong = _chu(yc.than, "field")
    # `value` duoc phep RONG (xoa gia tri), nen ⛔ khong dung `_chu` bat buoc.
    gia_tri = yc.than.get("value")
    if gia_tri is not None and not isinstance(gia_tri, (str, int, float)):
        raise LoiCua("FLS-BAD-REQUEST", "`value` phai la chuoi hay so")
    gia_tri = None if gia_tri is None else str(gia_tri)
    try:
        k = gt.ghi_but_toan(yc.conn, yc.pv, i, truong, gia_tri,
                            actor=yc.actor, reason=_chu(yc.than, "reason"),
                            force=_co(yc.q, yc.than, "force"))
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    return {"adj_id": k.adj_id, "jrn_id": k.jrn_id, "da_co": k.da_co,
            "value_before": k.value_before, "value_source": k.value_source,
            "actor": yc.actor}, "flash"


def dao(yc: YeuCau):
    """Dao but toan = THEM mot dong. ⛔ Khong sua, ⛔ khong xoa (`INV-I08`)."""
    a = _bat_buoc_int(yc.tham, "adj_id")
    try:
        k = gt.dao_but_toan(yc.conn, yc.pv, a, actor=yc.actor,
                            reason=_chu(yc.than, "reason"))
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    return {"adj_id": k.adj_id, "jrn_id": k.jrn_id, "dao_cua": a,
            "value_before": k.value_before, "actor": yc.actor}, "flash"


def ly_do(yc: YeuCau):
    i = _bat_buoc_int(yc.tham, "itl_id")
    try:
        k = gt.ghi_ly_do(yc.conn, yc.pv, i, reason=_chu(yc.than, "reason"),
                         actor=yc.actor)
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    return {"evt_id": k.evt_id, "actor": yc.actor}, "flash"


def hoan(yc: YeuCau):
    """Hoan CO HAN. ⛔ Khong leo cap — lan thu ba chi DOI MAU tren man hinh."""
    i = _bat_buoc_int(yc.tham, "itl_id")
    try:
        k = gt.ghi_hoan(yc.conn, yc.pv, i, den_ngay=_chu(yc.than, "until"),
                        reason=_chu(yc.than, "reason"), actor=yc.actor)
        lan = gt.dem_hoan(yc.conn, i)
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    return {"evt_id": k.evt_id, "so_lan_hoan": lan,
            # ⛔ Man hinh doi mau, ⛔ khong ai bi bao cao len cap tren
            # (`QĐ-ITL-24`: khong co cap tren trong luong nay).
            "doi_mau": lan >= 3, "actor": yc.actor}, "flash"


def ung_vien(yc: YeuCau):
    """Ung vien ghep lenh cho MOT dong so (`OP-02`, `QĐ-ITL-48`).

    ⛔ Duong nay ⛔ khong ghi gi — no chi **hien de nguoi chon**. Phep ghep that
    la mot duong `POST` rieng, va Σ duoc cong lai o do.
    """
    i = _bat_buoc_int(yc.tham, "itl_id")
    d = bc.ung_vien_pm(yc.conn, yc.pv, i, n=_so_nguyen(yc.q, "limit")
                       or bc.UNG_VIEN_MAC_DINH)
    if d is None:
        raise LoiCua("FLS-NOT-FOUND", f"itl_id={i} ngoai {yc.pv.mo_ta()}")
    return d, "flash"


def ghep(yc: YeuCau):
    """Ghep tay mot dong so voi N dong lenh chi (`OP-02`, `QĐ-ITL-48`).

    ⛔ `actor` den TU THE, ⛔ khong tu than yeu cau — cua da chan `actor` trong
    than bang `400` truoc khi vao day.
    """
    i = _bat_buoc_int(yc.tham, "itl_id")
    ds = yc.than.get("pm_line_ids")
    if not isinstance(ds, list):
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "than phai co `pm_line_ids` la MOT DANH SACH ma DONG lenh — ⛔ khong "
            "phai ma PHIEU: 526 phieu mang 2–36 reference khac nhau, ghep vao "
            "phieu thi may phai tu chon dong nao (`CR#6`)")
    try:
        return gt.ghep_lenh(yc.conn, yc.pv, i, ds, actor=yc.actor,
                            reason=_chu(yc.than, "reason"),
                            force=_co(yc.q, yc.than, "force")), "flash"
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e


def bo_ghep(yc: YeuCau):
    """Bo TOAN BO moi noi cua mot dong so (`GAP-JOIN-05`, `QĐ-ITL-69`).

    ⛔ Than yeu cau CHI co `reason` — ⛔ khong co danh sach dong lenh de bo le.
    Bo le mot trong N moi noi lam `Σ moi noi != tien bank`, tuc **tao ra dung
    cai trang thai sai** ma cong `SIGMA_MOI_NOI` dung ra de bat. Muon doi mot
    dong lenh thi: bo ca chum -> ghep lai.
    """
    i = _bat_buoc_int(yc.tham, "itl_id")
    if yc.than.get("pm_line_ids") is not None:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "⛔ duong nay ⛔ khong nhan `pm_line_ids`: no bo TOAN BO moi noi cua "
            "dong. Bo le mot moi noi lam Σ lech tien bank ⇒ tao ra mot trang "
            "thai sai (`QĐ-ITL-69`). Muon doi mot dong lenh: bo ca chum roi "
            "ghep lai")
    try:
        return gt.bo_moi_noi(yc.conn, yc.pv, i, actor=yc.actor,
                             reason=_chu(yc.than, "reason")), "flash"
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e


def xong(yc: YeuCau):
    """NGUOI bam **xong** ⇒ dong roi hang cho (`QĐ-ITL-71`).

    ⚠ `reason` **tuy y** o day — cua tang kho tu doi ly do khi con thieu truong
    hay ky da chot. ⛔ Khong bat ly do o TANG CUA: bat o day thi thao tac pho
    bien nhat (bam xong mot dong da du) cung phai go mot cau, va nguoi ta se go
    bua mot chu roi bam — mot cai ma sat khong thu duoc gi.
    """
    i = _bat_buoc_int(yc.tham, "itl_id")
    try:
        return gt.danh_dau_xong(yc.conn, yc.pv, i, actor=yc.actor,
                                reason=yc.than.get("reason")), "flash"
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e


def mo_lai(yc: YeuCau):
    """Mo lai mot dong da bam xong. `reason` **BAT BUOC** (`QĐ-ITL-71`)."""
    i = _bat_buoc_int(yc.tham, "itl_id")
    try:
        return gt.mo_lai(yc.conn, yc.pv, i, actor=yc.actor,
                         reason=_chu(yc.than, "reason")), "flash"
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e


HAM: dict[str, Callable[[YeuCau], Any]] = {
    # P4 · doc
    "so": so, "mot_dong": mot_dong, "hang_cho": hang_cho,
    "hang_cho_tom": hang_cho_tom, "nhat_ky": nhat_ky, "cong": cong,
    "do_phu": do_phu,
    # P5 · ghi
    "truoc_khi_go": truoc_khi_go, "sua": sua, "dao": dao,
    "ly_do": ly_do, "hoan": hoan,
    # ghep lenh
    "ung_vien": ung_vien, "ghep": ghep, "bo_ghep": bo_ghep,
    # hang cho: NGUOI bam xong (`QĐ-ITL-71`)
    "xong": xong, "mo_lai": mo_lai,
}
