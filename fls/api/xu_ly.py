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

from fls.adapters.pm_join import canon_ref
from fls.repo import do_mau_so as dms
from fls.repo import doc_bao_cao as bc
from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg
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
    # ⭐⭐ `reason` TUY Y (`BA-07` v3.4 `§4h ⓼`, `QĐ-ITL-149` — owner: *"bo yeu
    #   cau ly do cho cu Ghep"*). Truoc 01/10 dong nay goi `_chu(…)` BAT BUOC
    #   ⇒ than man gui `{pm_line_ids:[…]}` bi **400** — nut `Gan` tren may that
    #   ⛔ bao gio ghi duoc (`KQ-002 F-1`). Van kiem KIEU (`bat_buoc=False`);
    #   thieu thi `ghep_lenh` dien ly do mac dinh co nhan o TANG REPO.
    try:
        return gt.ghep_lenh(yc.conn, yc.pv, i, ds, actor=yc.actor,
                            reason=_chu(yc.than, "reason", bat_buoc=False),
                            force=_co(yc.q, yc.than, "force")), "flash"
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e


def mau_so(yc: YeuCau):
    """`B0` — MAU SO cua tac vu ① + doi chieu hai cau *"chua ghep"*.

    ⛔⛔ **Vi sao con so nay phai co mot CUA chu ⛔ khong chi mot cong cu.** Moi
    ty le do phu tu 27/08 den nay deu chia cho **10.030** *(ca so)*, va con so
    ay di vao bang dieu khien, vao tep moc, vao ban ve. Neu phep do dung chi
    song trong mot lenh terminal thi ban do man hinh se **tiep tuc** in mot ty
    le do tren mau so sai — im lang, va ⛔ khong ai doi chieu.

    ⭐⭐⭐ **Va tu 09/09 no cho luon `phia_pm` (`QĐ-ITL-122`).** Owner chot
    chieu do la **`Trans` map vao `PM`**, va *"⛔ ko can question cac Trans
    khong duoc map"* ⇒ mau so THAT la so **DONG LENH CHI**. Hai con so nam
    **cung mot cua**, co y: neu man hinh phai goi hai cua de hoi *"con bao
    nhieu viec"* thi som muon no chi goi **mot** cai, va no se chon cai
    ⛔ khong dung.
    """
    d = dms.do_mau_so(yc.conn, yc.pv)
    return dict(d, phia_pm=dms.do_phu_pm(yc.conn, yc.pv)), "flash"


def tu_chung_ds(yc: YeuCau):
    """`B2` — danh sach dong **TU CHUNG** *(cua ghep LO nhan duoc ngay)*.

    ⛔ Duong nay ⛔ khong ghi gi. Va no tra **ca ly do TU CHOI** cho nhung dong
    co ma ma ⛔ khong tu chung: mot man hinh chi thay *"68 dong ghep duoc"* ma
    ⛔ khong thay *"584 dong co ma ma 516 dong bi tu choi vi sao"* la mot man
    hinh **an di dung phan viec con lai**.
    """
    d = dms.ds_tu_chung(yc.conn, yc.pv)
    return {
        "tu_chung": [{"itl_id": i, "pm_line_ids": v}
                     for i, v in sorted(d["tu_chung"].items())],
        "khong": [{"itl_id": i, "ly_do": v, "cau": dms.LY_DO_KHONG_TU_CHUNG[v]}
                  for i, v in sorted(d["khong"].items())],
        "so_dong_xet": d["so_dong_xet"],
        "vi_sao": d["vi_sao"],
        "pham_vi": d["pham_vi"],
    }, "flash"


def ghep_lo(yc: YeuCau):
    """⭐⭐⭐ `B2` — ghep **CA LO**, va **CHI** dong TU CHUNG (`QĐ-ITL-118`).

    ⛔⛔ **Than yeu cau ⛔ KHONG nhan `pm_line_ids`** — cung luat voi cua khai
    thu tu LO (`QĐ-ITL-117`): may **do lai phia may chu** roi ghep dung cai no
    do ra. Neu nguoi goi dua san dong lenh thi cu bam LO tro thanh **N phep
    ghep tay ⛔ khong ai xem** — va luc do no ⛔ khong con la "tu chung", no la
    "tin loi nguoi goi".

    ⛔ **Tu choi CA LO** neu co bat ky dong ⛔ khong tu chung: mot cu bam LO
    ⛔ khong duoc ghep **mot phan** roi de nguoi doan xem phan nao da chay.
    """
    ds = yc.than.get("itl_ids")
    if not isinstance(ds, list) or not ds:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "than phai co `itl_ids` la MOT DANH SACH ⛔ khong rong. ⛔ Cua nay "
            "⛔ KHONG nhan `pm_line_ids`: no do lai phia may chu roi ghep dung "
            "cai no do ra — xem `GET /queue/tu-chung`")
    if yc.than.get("pm_line_ids") is not None:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "⛔ cua LO ⛔ KHONG nhan `pm_line_ids` — muon tu chi dinh dong "
            "lenh thi dung `POST /queue/{itl_id}/match` cho TUNG dong")
    if _co(yc.q, yc.than, "force"):
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "⛔ cua LO ⛔ KHONG bao gio nhan `force`: `force` la cach nguoi ghi "
            "de ket luan cua may cho MOT dong co ly do cu the (`ghep_lenh` ⓖ) "
            "— rai no len ca lo la bo cong duyet cho N dong bang mot cu bam")
    try:
        so = [int(x) for x in ds]
    except (TypeError, ValueError) as e:
        raise LoiCua("FLS-BAD-REQUEST",
                     f"`itl_ids` phai la so nguyen: {ds[:5]}") from e

    # ⛔⛔ `reason` **BAT BUOC** o cua LO — GIU NGUYEN co y (`BA-07 §4h ⓼`,
    #   `WO-003`): owner chi noi ve **cu Ghep tren man**; cua lo ⛔ co nguoi
    #   chon dong (`§4g ⓓ`). ⚠ `ghep_lenh` nay tu dien ly do mac dinh khi
    #   rong, nhung o day ly do ⛔ bao gio rong (co hau to `· ghep LO…`) — nen
    #   phep chan PHAI dung o tang cua. Noi luat nay ⇒ bai
    #   `tests/api/test_cua_ghep_lo_pg.py::test_cua_LO_thieu_ly_do_VAN_400…` DO.
    reason = _chu(yc.than, "reason")
    d = dms.ds_tu_chung(yc.conn, yc.pv, itl_ids=so)
    xau = sorted(set(so) - set(d["tu_chung"]))
    if xau:
        raise LoiCua(
            "FLS-GHEP-KHONG-TU-CHUNG",
            f"{len(xau)} trong {len(so)} dong ⛔ KHONG tu chung ⇒ ⛔ khong ghep "
            f"mot dong nao. Xem `khac.dong` de biet tung dong vuong cong nao",
            # ⛔ `khac` la khoa DUY NHAT `bao.KHOA_THEM` cho phep cho phan cau
            #    truc — ⛔ khong tu them khoa moi o day: cong `dong_goi_loi` NO
            #    ngay, va no NO dung ("mot truong noi bo di ra ngoai trong im
            #    lang la mot cho ro").
            khac={
                "dong": [{"itl_id": i,
                          "ly_do": ("ngoai_pham_vi_hay_da_noi"
                                    if i in d["ngoai"] else
                                    d["khong"].get(
                                        i, "khong_co_ung_vien_bac_ma")),
                          "cau": dms.LY_DO_KHONG_TU_CHUNG.get(
                              d["khong"].get(i, ""), "")}
                         for i in xau[:50]],
                "so_dong_xau": len(xau), "so_dong_yeu_cau": len(so),
                # ⚠ Khai ra khi danh sach bi CAT: mot man hinh hien 50 dong ma
                #    ⛔ khong biet con 500 dong nua la mot man hinh noi doi.
                "con_bi_cat": max(0, len(xau) - 50)})

    # ⛔⛔ MOT giao dich cho ca lo: `ghep_lenh` tu mo giao dich con (savepoint),
    # nen mot dong no la CA LO lui. Ghep nua vo la trang thai ⛔ khong ai doc
    # duoc — cung ly le voi cua nap LO va cua khai thu tu LO.
    ket: list[dict[str, Any]] = []
    try:
        with yc.conn.transaction():
            for i, pm in sorted(d["tu_chung"].items()):
                kq = gt.ghep_lenh(
                    yc.conn, yc.pv, i, pm, actor=yc.actor,
                    reason=f"{reason} · ghep LO tu chung (`QĐ-ITL-118`)")
                ket.append({"itl_id": i, "pm_line_ids": pm,
                            "tien_bank": kq["tien_bank"],
                            "tong_lenh": kq["tong_lenh"],
                            "evt_id": kq["evt_id"],
                            "but_toan": kq["but_toan"]})
    except gt.LoiGhi as e:
        raise _dich_loi_ghi(e) from e
    return {"so_dong_yeu_cau": len(so), "so_dong_da_ghep": len(ket),
            "so_moi_noi": sum(len(x["pm_line_ids"]) for x in ket),
            "dong": ket, "pham_vi": yc.pv.mo_ta()}, "flash"


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
    # ⭐⭐ `reason` TUY Y — `BA-07 §4h ⓻ⓑ` da khai tu v3.0, `§4h ⓼` v3.4 thong
    #   nhat. Nut `Bo gan` gui `{}` ⇒ truoc 01/10 la **400** (`KQ-002 F-1`).
    try:
        return gt.bo_moi_noi(yc.conn, yc.pv, i, actor=yc.actor,
                             reason=_chu(yc.than, "reason", bat_buoc=False)
                             ), "flash"
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
    # ⭐⭐⭐ `B0` do lai MAU SO + `B2` ghep CA LO (`QĐ-ITL-118`)
    "mau_so": mau_so, "tu_chung_ds": tu_chung_ds, "ghep_lo": ghep_lo,
    # hang cho: NGUOI bam xong (`QĐ-ITL-71`)
    "xong": xong, "mo_lai": mo_lai,
}


# ⭐⭐⭐ NHOM NAP (`CR#11` task `4`, `BA-07` §4b) — cua VAO dau tien cua he.
#
# ⚠ Ba ham nay o `fls/api/nap_cua.py` chu ⛔ khong o day: chung goi sang
#   `fls.adapters` + `fls.kiem` — hai tang ma moi ham `P4`/`P5` o tep nay
#   ⛔ khong he cham. Tron chung vao day lam **do thi phu thuoc cua tep nay**
#   rong ra cho mot nhom ⛔ khong lien quan gi den phep DOC va phep SUA.
#
# ⛔ Import DAT O CUOI, ⛔ khong o dau tep: `nap_cua` import nguoc ve day
#   (`LoiCua`, `YeuCau`, hai ham doc tham so) ⇒ dat o dau la VONG IMPORT.
#
# ⭐ Va viec ba ham nay o mot tep KHAC vua lam lo ra mot **diem mu cua cong**
#   `tools/soi_bang_tuyen.py`: no neo cung vao `fls.api.xu_ly` de bat dau bam
#   do thi goi ⇒ mot ham o tep khac se duoc do la **cham 0 bang**. Da va: cong
#   nay bat dau tu **dung tep ham that su o**.
from fls.api import nap_cua  # noqa: E402

HAM.update({"ghi_khai": nap_cua.ghi_khai, "xem_truoc": nap_cua.xem_truoc,
            "nap": nap_cua.nap,
            # ⭐⭐ Nhom ANH CHUP (`QĐ-ITL-110`, task `9d`) — bon cua ma man
            #    `F04` can va truoc 08/09 ⛔ KHONG TON TAI. `BA-07` §4c.
            "nguon_ds": nap_cua.nguon_ds,
            "khai_cua_nguon": nap_cua.khai_cua_nguon,
            "chup_ds": nap_cua.chup_ds,
            "chup_mot": nap_cua.chup_mot,
            "thu_tu_ds": nap_cua.thu_tu_ds,
            "ghi_thu_tu": nap_cua.ghi_thu_tu,
            # ⭐ khai thu tu CA LO — CHI nguon TU CHUNG (`QĐ-ITL-117`)
            "khai_thu_tu_lo": nap_cua.khai_thu_tu_lo,
            # ⭐ NAP CA LO (`QĐ-ITL-111`/`112`)
            "lo_xem_truoc": nap_cua.lo_xem_truoc,
            "lo_nap": nap_cua.lo_nap})


# ══ ⭐⭐⭐ `GAP-SCR-14` — HANG CHO PHIA LENH CHI (09/09) ══
#
# ⛔⛔⛔ **Ba cua nay lam mot viec: doi CAU HOI cua man ghep.**
#
# Owner chot *"`Trans` map vao `PM`; ⛔ ko can question cac Trans khong duoc
# map"* *(`QĐ-ITL-122`)*. Do tren bang tuyen cung ngay: **10** cua khoa
# `itl_id`, ⛔ **0** cua khoa dong lenh ⇒ he ⛔ **khong co duong nao** hoi
# *"lenh chi nao ⛔ chua tim duoc tien"*, tuc **dung cau hoi cua viec**.
#
# ★ Hai con so cua cung mot kho, doc canh nhau:
#   · hoi phia TIEN : **5.684** dong chua noi · **799** dong de phu 90% tien
#   · hoi phia LENH : **1.345** dong chua co tien · ⭐ **69** dong de phu 90%
#
# ⇒ **69** thay vi **799**: chenh **11,6 lan**, va cung mot du lieu.
#
# ⛔⛔ **Va ba cua nay ⛔ KHONG mo mot duong GHI thu hai.** Phep ghep van la
#    `POST /queue/{itl_id}/match` — mot chuyen. Man hinh phia lenh chi chi
#    **doi thu tu hoi**: chon dong lenh truoc, roi chon dong tien, roi goi
#    **dung cai cua ghi cu**. Mo duong ghi thu hai se lam cong quet ma nguon
#    *(chi-mot-cho-ghi-tay)* do — dung nhu no phai do.
def lenh_cho(yc: YeuCau):
    """Dong lenh chi **⛔ CHUA tim duoc tien**, xep theo tien trong TUNG te.

    `?duyet=1` chi lay dong `Approve`; `?duyet=0` chi lay dong ⛔ chua duyet.
    ⛔ **Mac dinh HIEN CA HAI** — an dong ⛔ chua duyet theo mac dinh la mot
    **mac dinh im lang** *(`INV-I16`)*: ke toan biet phieu ay ton tai, ⛔ khong
    thay no, va se ket luan **he mat du lieu**.
    """
    tho = str(yc.q.get("duyet", "")).strip()
    if tho and tho not in ("0", "1"):
        raise LoiCua("FLS-BAD-REQUEST",
                     f"`duyet={tho}` phai la `0` hay `1`")
    ro = str(yc.q.get("ro", "")).strip()
    tc = str(yc.q.get("tu_chung", "")).strip()
    if tc and tc not in ("0", "1"):
        raise LoiCua("FLS-BAD-REQUEST",
                     f"`tu_chung={tc}` phai la `0` hay `1`")
    if tc and not ro:
        # ⛔ `tu_chung` chi co nghia TRONG ro `may`. Nhan im lang mot bo loc
        #    ⛔ khong lam gi la de nguoi doc tin mot danh sach **⛔ khong phai
        #    cai ho vua yeu cau** (`INV-I16`).
        raise LoiCua("FLS-BAD-REQUEST",
                     "`tu_chung` chi dung kem `ro=may`")
    try:
        if ro:
            t = lc.doc_lenh_cho_theo_ro(
                yc.conn, yc.pv, ro,
                tu_chung=(None if not tc else tc == "1"),
                con_tro=yc.q.get("cursor") or None,
                limit=_so_nguyen(yc.q, "limit"))
        else:
            t = lc.doc_lenh_cho(
                yc.conn, yc.pv, curr=yc.q.get("curr") or None,
                chi_duyet=(None if not tho else tho == "1"),
                den_pct=_thap_phan(yc.q, "den_pct"),
                con_tro=yc.q.get("cursor") or None,
                limit=_so_nguyen(yc.q, "limit"))
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    # ⭐ `G2` — gan RO cho tung dong (`BA-12 §2`). ⛔ Lam o day chu ⛔ khong de
    #   man hinh tu suy: phep chia doi `canon_ref` tren CA HAI ve, va mot ban
    #   thu hai bang JS se lech **dung o cho no hay lech nhat**.
    lc.xep_ro(t.dong, lc.chi_muc_ma(yc.conn, yc.pv),
              lc.tap_tu_chung(yc.conn, yc.pv))
    # ⭐ SAU `xep_ro` — no la cho sinh ra `ung_vien_itl` va `ma_canon`, tuc hai
    #   thu `_gan_gd` can. Goi truoc thi hang van ⛔ chua co gi de nam.
    _gan_gd(t.dong, yc.conn, yc.pv)
    # ⭐⭐ `22/09` — moi hang mang them `the`: khuon **11 truong** cua man ghep.
    #
    # ⛔⛔ **Vi sao THEM chu ⛔ khong THAY.** Lan `F01` cu doc thang
    #    `pm_line_id`/`tho`/`ro`/`vi_sao`/`hang`/`luy_ke_pct` — bo chung di la
    #    pha mot man dang chay de phuc vu mot man moi. ⭐ Va vi sao ⛔ khong mot
    #    cua RIENG: hai cua tra cung mot danh sach voi hai hinh dang la hai ban
    #    su that, va chung se lech.
    #
    # ⭐ Phep anh xa nam o TANG DOC (`man_ghep.khuon_the_lenh`) chu ⛔ khong o
    #   day va tuyet ⛔ khong o JS: **6/11** truong cua the chi song trong tui
    #   `tho`, khoa theo **ten cot cua Google Sheets** — thu da doi ten roi.
    for d in t.dong:
        d["the"] = mg.khuon_the_lenh(d)
    _gd_vao_the(t.dong)
    return _trang_ra(t), "flash"


# ⭐⭐⭐ Cot `Giao dich da gan` · `So tien GD` · `Bac` cua **BANG SO**.
#
# ⛔⛔ Ban dung co **hai view**: bang so `12` cot khi ⛔ chua mo lenh nao, va
#    rail ＋ ban lam viec khi da mo. Ba cot cuoi cua bang can **giao dich**
#    cua tung dong — ma ca hai cua danh sach chi tra **ID**
#    *(`ung_vien_itl = [47298]`, `itl_da_gan = [28338]`)*.
#
# ⭐ ⇒ **MOT** truy van cho ca trang *(`lc.gd_theo_itl`)*, ⛔ khong `738` luot.
#
# ⭐⭐ Va **bac tinh o day** chu ⛔ khong o JS: phep chia bac dung `canon_ref`
#   — mot ban thu hai bang JS se lech **dung o cho no hay lech nhat**
#   *(da do: `regexp` trong SQL lech **17,9%** so voi `canon_ref`)*.
def _gan_gd(dong, conn, pv):
    """Them `gd` cho tung hang: giao dich **da gan**, hoac **de xuat dau**.

    ⛔ `None` la mot **cau tra loi** — *"dong nay ⛔ chua co giao dich nao"*.
      Thieu khoa la *"FLS ⛔ khong biet"*, va hai cau ay khac nhau (`INV-I16`).
    """
    can: dict[str, int] = {}
    # ⭐⭐ `gd_ds` — **MOI** dong tien da gan, ⛔ khong chi dong dau.
    #    ⛔⛔ Do `23/09` tren `2.219` lenh da gan: **`23` (1,0%)** gan nhieu
    #       hon mot dong tien, nhieu nhat **`7`**. Mot `1,0%` la co de **⛔
    #       khong bay hop thoai xac nhan** (`QĐ-ITL-148 ⓔ`) — ⛔ **khong**
    #       phai co de **giau mat sau dong tien**: hien dong dau va im ve
    #       `6` dong con lai thi cua dang **noi sai** ve mot phep gan that.
    #    ⭐ Gia: tap `id` tang tu ~`500` len ~`505` moi trang — **mot** truy
    #      van van la **mot**.
    chum: dict[str, list[int]] = {}
    for d in dong:
        da = d.get("itl_da_gan") or []
        ds = da or d.get("ung_vien_itl") or []
        if ds:
            can[d["pm_line_id"]] = ds[0]
        if da:
            chum[d["pm_line_id"]] = list(da)
    moi_id = set(can.values())
    for v in chum.values():
        moi_id.update(v)
    kho = lc.gd_theo_itl(conn, pv, moi_id)
    for d in dong:
        i = can.get(d["pm_line_id"])
        r = kho.get(i) if i is not None else None
        if r is None:
            d["gd"] = None
            continue
        try:
            u = _khuon_gd(r, d)
        except ValueError as e:
            # ⛔⛔ **MOT dong hong ⛔ KHONG duoc lam sap ca trang.** `tach_nguon`
            #    NO khi `source_sheet` sai khuon — dung the, do la `INV-I16` o
            #    tang doc. ⛔ Nhung o day ta dang dung **mot danh sach**, va
            #    mot ngoai le se tra `500` cho ca trang ⇒ ke toan mat **ca
            #    738 dong** vi mot dong.
            # ⭐ `loi_nguon` da la mot trong **ba duong ra** cua `DUONG_RA` —
            #   no la mot trang thai da co ten, ⛔ khong phai mot cho vá.
            d["gd"] = {"loi_nguon": str(e), "itl_id": r.get("itl_id")}
            continue
        # ⭐ `da_gan` phan biet *"da chot"* voi *"may de xuat"* — hai thu
        #   ⛔ KHONG duoc trong giong nhau (`§6.3` cua hop dong).
        u["da_gan"] = bool(d.get("itl_da_gan"))
        d["gd"] = u
        # ⭐ `gd_ds` chi co mat khi dong lenh **da gan** — voi mot dong
        #   ⛔ chua gan, `ung_vien_itl` la **de xuat cua may** (toi `20`
        #   dong), va cho ca `20` vao day la tron *"da chot"* voi *"may
        #   doan"* — dung thu `§6.3` cam.
        ids = chum.get(d["pm_line_id"])
        if ids:
            d["gd_ds"] = [x for x in (_mot_gd(kho.get(i), d) for i in ids)
                          if x is not None]


def _mot_gd(r, d):
    """Mot hang ITL ⇒ khuon ung vien, hoac `None` neu ⛔ khong doc duoc.

    ⛔ Cung phep **⛔ khong lam sap ca trang** nhu `_gan_gd`: mot dong hong
      trong mot chum `7` dong ⛔ khong duoc lam mat `6` dong kia.
    """
    if r is None:
        return None
    try:
        u = _khuon_gd(r, d)
    except ValueError as e:
        return {"loi_nguon": str(e), "itl_id": r.get("itl_id")}
    u["da_gan"] = True
    return u


def _khuon_gd(r, d):
    """Một phần tử `gd` / `gd_ds` — ⭐ **ĐÚNG khuôn `⓵`**, đủ trường.

    ⭐⭐ `BA-07` **v3.7** §4h ⓵' *(`KQ-031` `F-2` + `F-3`, `WO-032` (b)(c))*:
      ⓐ `lech` so với dòng lệnh **của chính thẻ** *(`d.amount`/`d.curr`)* bằng
         **cùng** hàm `mg.lech_ung_vien` mà ba cửa kia dùng — trước: ép `None`
         ở **mọi** dòng;
      ⓑ `khoa_to` — **cùng** `mg.khoa_bang_chung(thẻ lệnh, ứng viên)` mà
         `_gan_khoa_to` gắn cho hai cửa ứng viên. Trước: sổ thật **0 / 768**
         `gd` mang khoá ⇒ khối *"✓ Đang gán với giao dịch"* `F01G.ve_dang_gan`
         ⛔ bao giờ tô `<mark>` bằng chứng — và bài màn của khối ấy **tự
         nhét** `khoa_to` *(lần thứ ba của lớp *"khuôn thử tự nhét"*)*.
    ⛔ Một khuôn *"rút gọn cho danh sách"*: màn có **một** hàm vẽ bằng chứng,
      và nó ⛔ được biết thân đến từ cửa nào.
    """
    u = mg.khuon_ung_vien(dict(r, bac=_bac(d, r)), lenh=d)
    u["khoa_to"] = mg.khoa_bang_chung(mg.khuon_the_lenh(d), u)
    return u


def _gd_vao_the(dong):
    """⭐ `gd` phai nam **TRONG** `the` — man doc `the`, ⛔ khong doc hang tho.

    ⛔⛔ Bai thu bat duoc: man lay `r.the` roi bo phan con lai cua hang ⇒ `gd`
       **roi mat tren duong**, va ba cot cuoi cua bang so ⛔ khong bao gio co
       gi de ve. ⭐ Sua o CUA chu ⛔ khong o JS: mot phep ghep o man la mot
       ban su that thu hai ve *"mot hang gom nhung gi"*.
    """
    for d in dong:
        if isinstance(d.get("the"), dict):
            d["the"]["gd"] = d.get("gd")
            if d.get("gd_ds") is not None:
                d["the"]["gd_ds"] = d["gd_ds"]
            # ⭐⭐ `WO-037` *(`BA-06` v4.16 §4.5 — câu thứ sáu; `HOI-038` phương
            #   án B)*: lệnh khớp mã **chỉ** ở tiền tệ khác ⇒ `gd = null` *(máy
            #   ⛔ đề xuất cặp cửa ghi từ chối)* ⇒ ô `Giao dịch đã gán` in **câu
            #   `vi_sao` của cửa**. Màn đọc `the`, ⛔ hàng thô *(cùng lý do `gd`
            #   ở trên)* ⇒ chở câu ấy vào `the`.
            #   ⛔⛔ **CHỈ CÓ** ở nhánh ấy, vắng ở mọi hàng khác *(cùng kiểu
            #   `loi_nguon` / `dien_giai_vi_sao`)*: chép `vi_sao` cho **mọi**
            #   hàng thì **532** lệnh ⛔ số chứng từ *(sổ thật 02/10)* đổi câu
            #   *"— chưa chọn"* — `BA-06` v4.16 *"⛔ đổi năm câu kia"*, `WO-037`
            #   chỉ đếm **84** ô đổi. Quyết ở **Python** *(hỏi đúng nhánh của
            #   `xep_ro`)*, ⛔ để JS so chuỗi câu.
            if d.get("gd") is None and lc.la_khop_ma_chi_khac_tien_te(d):
                d["the"]["vi_sao"] = d.get("vi_sao")


def _bac(d, r):
    """Bac cua mot giao dich so voi dong lenh — cung ten hai chieu.

    ⭐⭐ `WO-037` *(`BA-07` v3.9 §4h ⓵ dòng `bac`)* — thứ tự chia **giống hệt**
      cửa `/so` *(`man_ghep.so_theo_lenh`)*: `ma` *(khớp mã, **mọi** tiền tệ)*
      › **khác tiền tệ** ⇒ `khac_tien_te` › `tien` › `cung_tien_te`.
      ⓐ `KQ-036 F-2`: nhánh cuối cũ trả `cung_tien_te` cho **mọi** dòng còn
         lại — kể cả dòng USD dưới lệnh VND ⇒ chip *"④ cùng đơn vị tiền"* cạnh
         `lech = null` *(lỗi `(d)` của `WO-032` sống ở cửa thứ hai)*. Sổ thật
         02/10: **0 / 2.262** mối nối khác tiền tệ ⇒ ca biên *(mối nối dựng
         ngoài cửa ghi — bộ nạp `chen_moi_noi`)*.
      ⓑ `KQ-036 F-1`: so tiền tệ bằng **cùng** `mg.ma_tien_te` *(`trim` + chữ
         hoa)* mà `lech_ung_vien` dùng — bản cũ `str(curr).upper()` ⛔ `trim`
         ⇒ `' vnd '` ↔ `VND` lệch `0` mà bậc `cung_tien_te`. Bài quét
         `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py` cấm mọi phép so
         `.upper() ==` trong tệp này.
    """
    if d.get("ma_canon") and canon_ref(r.get("doc_no")) == d["ma_canon"]:
        return "ma"
    if mg.ma_tien_te(r.get("curr")) != mg.ma_tien_te(d.get("curr")):
        return "khac_tien_te"
    try:
        if Decimal(str(r.get("tien"))) == Decimal(str(d.get("amount"))):
            return "tien"
    except (InvalidOperation, TypeError, ValueError):
        pass
    return "cung_tien_te"


def lenh_da_gan(yc: YeuCau):
    """Dong lenh chi **DA** tim duoc tien — bu cua `/queue/lenh-cho`.

    ⛔⛔ `GAP-API-08`: truoc cua nay, `/queue/lenh-cho` loc cung
       `NOT EXISTS (fls_moi_noi)` nen he ⛔ **khong co duong nao** hoi *"lenh
       chi nao DA co tien"* — va nua *"da gan"* cua man ghep chet theo day
       chuyen.

    ⭐ Moi hang mang `itl_da_gan[]` — mot **DANH SACH**: `23/2.219 = 1,0%`
      lenh gan nhieu hon mot dong tien.
    """
    try:
        t = lc.doc_lenh_da_gan(
            yc.conn, yc.pv,
            con_tro=yc.q.get("cursor") or None,
            limit=_so_nguyen(yc.q, "limit"))
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    # ⭐⭐ `WO-032` vòng 2 `(i)` *(`BA-07` v3.8 §4h ⓵', `HOI-033`)*: gắn mã
    #   dòng lệnh **TRƯỚC** `_gan_gd` — `_bac` đọc `ma_canon` để chia bậc `ma`.
    #   ⛔ Thiếu dòng này *(trước 02/10)*: cửa này ⛔ chạy `xep_ro` nên ⛔ bao
    #   giờ có `ma_canon` ⇒ sổ thật **0 / 2.262** mối nối khớp số chứng từ
    #   được trả `ma`, chip *"✓ Đang gán"* `①` **0 / 2.219** lệnh.
    #   ⛔ Gọi `canon_ref` thẳng ở đây là bản thứ hai — dùng **cùng** hàm của
    #   `xep_ro`.
    lc.gan_ma_canon(t.dong)
    _gan_gd(t.dong, yc.conn, yc.pv)
    for d in t.dong:
        d["the"] = mg.khuon_the_lenh(d)
    _gd_vao_the(t.dong)
    return _trang_ra(t), "flash"


def lenh_cho_ro(yc: YeuCau):
    """Dem dong lenh cho theo **RO** — `may` · `nguoi` · `khong` (`BA-12 §2`).

    ⛔⛔ **Vi sao la mot cua RIENG chu ⛔ khong nhet vao `/lenh-cho/summary`.**
       Cai kia dem theo **don vi tien te** *(`QĐ-ITL-58`)*, cai nay dem theo
       **ai tra loi duoc**. Gop hai truc vao mot cua se ra mot bang hai chieu
       ma ⛔ khong ai hoi, va lam ca hai kho doc.

    ⭐ Tra ca `tong` de nguoi doc **cong lai duoc**: ba ro phai khep ve `tong`.
      Mot bang phan loai ⛔ khong cong ve tong la mot bang ⛔ khong kiem duoc.
    """
    try:
        return lc.dem_theo_ro(yc.conn, yc.pv), "flash"
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e


def mot_dong_lenh(yc: YeuCau):
    """**Toan bo** mot dong lenh chi — 8 truong + ca 28 cot THO + ca phieu.

    ⛔ `404` neu ⛔ khong co, **cung mot cau** cho *"khong ton tai"* va *"ngoai
      pham vi"* — noi ra su khac biet la ro thong tin ve cai kho.
    """
    pid = yc.tham.get("pm_line_id") or ""
    d = lc.doc_mot_dong_lenh(yc.conn, yc.pv, pid)
    if d is None:
        raise LoiCua("FLS-NOT-FOUND",
                     f"pm_line_id={pid!r} ngoai {yc.pv.mo_ta()}")
    return d, "flash"


def lenh_cho_tom(yc: YeuCau):
    """Chan man phia lenh chi — **theo tung tien te**, ⛔ khong co dong "tong".

    ⭐ Tra ca `so_dong_duyet` va `so_dong_chua_duyet`: hai loai viec **khac
      nhau**, va mot con so gop lai se lam ke toan tuong ho con **1.345** viec
      trong khi phan ho lam duoc chi la **1.070**.
    """
    tho = str(yc.q.get("muc_pct", "")).strip()
    try:
        muc = Decimal(tho) if tho else Decimal(90)
    except InvalidOperation:
        raise LoiCua("FLS-BAD-REQUEST",
                     f"`muc_pct={tho}` khong phai mot so") from None
    try:
        return {"theo_tien_te": lc.dem_lenh_cho(yc.conn, yc.pv, muc)}, "flash"
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e


# ⭐⭐ Bo khoa **BANG CHUNG** — to cai gi trong dien giai sao ke.
#
# ⛔⛔ Gan o TANG CUA chu ⛔ khong o `lenh_cho.py`: `man_ghep` DA nhap
#    `lenh_cho`, nen goi nguoc lai la mot **vong nhap** — va cong
#    `import-linter` se do ngay. Hai cua deu tra cung khuon
#    `{dong_lenh, ung_vien}`, nen mot ham dung chung o day la du.
#
# ⛔ Va **⛔ khong** de JS tu tinh: bo tu rac la mot **luat nghiep vu**
#   *(tu nao la ten phap ly vo nghia khi doi chieu)*, ⛔ khong phai mot meo
#   hien thi. De o JS thi ⛔ khong bai thu Python nao cham toi no.
def _gan_khoa_to(d):
    """Them `khoa_to[]` cho tung ung vien. ⛔ Sua tai cho, tra lai chinh `d`."""
    if not isinstance(d, dict) or not d.get("ung_vien"):
        return d
    lenh = d.get("dong_lenh")
    if not lenh:
        return d
    the = mg.khuon_the_lenh(lenh)
    for u in d["ung_vien"]:
        u["khoa_to"] = mg.khoa_bang_chung(the, u)
    return d


def ung_vien_tien(yc: YeuCau):
    """Dong TIEN ung vien cho MOT dong lenh — chieu NGUOC cua `ung_vien`.

    ⛔ Duong nay ⛔ khong ghi gi. Bon bac **soi guong** chieu thuan
      *(`ma`/`tien`/`gan_tien`/`cung_tien_te`)*, va ten bac giu **y nguyen** de
      hai man hinh noi **cung mot tu** cho cung mot y.
    """
    ma = str(yc.tham.get("pm_line_id", "")).strip()
    if not ma:
        raise LoiCua("FLS-BAD-REQUEST", "thieu `pm_line_id`")
    d = lc.ung_vien_itl(yc.conn, yc.pv, ma,
                        n=_so_nguyen(yc.q, "limit") or bc.UNG_VIEN_MAC_DINH)
    if d is None:
        raise LoiCua("FLS-NOT-FOUND",
                     f"pm_line_id={ma!r} ⛔ khong co trong anh chup hieu luc "
                     f"cua {yc.pv.mo_ta()}")
    # ⭐⭐⭐ **NAN KHUON** — truoc `23/09` cua nay tra **hang THO** tu SQL
    #    (`tien` · `ps_no` · `ps_co` · `source_sheet`) trong khi man doc
    #    `amount` · `chieu` · `nguon` ⇒ **hai cot rong**, va `khop_dung_tien`
    #    so `Number(undefined)` ⇒ **MOI ung vien deu thanh "lech"** ⇒ nut
    #    `Gan` luon di duong canh bao. Mot phep khop DUNG trinh bay nhu SAI.
    # ⛔⛔ Bai thu cu song sot vi no chi hoi `bac` va `itl_id` — dung **hai
    #    khoa ma hang tho TINH CO cung co**.
    # ⭐ `/so` (Toan so) **da** nan khuon tu truoc ⇒ hai cua nuoi **mot** ham
    #   ve ma noi **hai** thu tieng.
    # ⭐ `WO-032`: `lech` tính lại bằng `mg.lech_ung_vien` so với `dong_lenh`
    #   *(mọi bậc — trước: bậc `ma` luôn `null`)*.
    d["ung_vien"] = [mg.khuon_ung_vien(u, lenh=d["dong_lenh"])
                     for u in d.get("ung_vien", [])]
    return _gan_khoa_to(d), "flash"


# ⭐⭐⭐ `GAP-SCR-14` — ghi danh ba cua PHIA LENH CHI.
#
# ⛔⛔ **Ba ham nay dinh nghia SAU so dang ky `HAM` o tren, nen chung phai
#    duoc `update` vao — va cong `soi_bang_tuyen` da bat dung dieu do o lan
#    chay dau: *"⛔ khong co ham `lenh_cho`"* × 3.** Ham **ton tai** trong
#    module *(`hasattr` = True)* nhung **⛔ chua duoc ghi danh** ⇒ ba tuyen se
#    la ba duong **404 im lang** neu chi doc `hasattr` ma tin.
#    ⇒ Cong ay do vi no soi **so dang ky**, ⛔ khong soi module.
#    ⭐ Và nó bắt lại **đúng lần nữa** ngày `11/09`: thêm `lenh_cho_ro`
#      *(`G2`)*, quên dòng dưới đây, cổng đỏ ngay với cùng một câu. Một bài
#      học nằm trong chú thích ⛔ **không** ngăn được lần sau — **cổng** thì có.
def so_theo_lenh(yc: YeuCau):
    """TOAN SO nhin tu MOT dong lenh — `QĐ-ITL-148` · `BA-07 §4h ⓹`.

    ⭐⭐ Voi lenh may ⛔ khong tim duoc ung vien nao *(**768** dong)*, day la
      duong duy nhat de nguoi lam tiep ⇒ man **⛔ khong bao gio la ngo cut**.
    """
    ma = str(yc.tham.get("pm_line_id", "")).strip()
    if not ma:
        raise LoiCua("FLS-BAD-REQUEST", "thieu `pm_line_id`")
    d = mg.so_theo_lenh(yc.conn, yc.pv, ma, q=yc.q.get("q"),
                        n=_so_nguyen(yc.q, "limit") or mg.SO_MAC_DINH)
    if not d:
        raise LoiCua("FLS-NOT-FOUND",
                     f"pm_line_id={ma!r} ⛔ khong co trong anh chup hieu luc "
                     f"cua {yc.pv.mo_ta()}")
    # ⭐ CA HAI cua ung vien deu phai mang `khoa_to` — man ⛔ khong duoc biet
    #   *"dang o che do Toan so hay khong"* de quyet co to bang chung hay khong.
    return _gan_khoa_to(d), "flash"


def chum_moi_noi(yc: YeuCau):
    """Cac dong lenh mot cu `Bo gan` se go — ⭐ **KEM TEN**.

    ⛔ Cua `unmatch` bo **TOAN BO** moi noi cua dong tien *(`QĐ-ITL-69`)*.
      Owner chot `21/09`: **giu cua, MAN noi ra thiet hai**.
    ⭐ Do: chi **25/2.222 = 1,1%** dong tien mang chum ⇒ man **chi hoi o `1,1%`
      ca ay**; hoi ca `2.222` lan la cach nhanh nhat day nguoi ta bam `OK`
      ⛔ khong doc.
    """
    i = _so_nguyen(yc.tham, "itl_id")
    if i is None:
        raise LoiCua("FLS-BAD-REQUEST", "thieu `itl_id`")
    ds = mg.chum_cua_dong_tien(yc.conn, yc.pv, i)
    return {"itl_id": i, "dong_lenh": ds, "so_dong": len(ds),
            "can_hoi": len(ds) > 1}, "flash"


HAM.update({"lenh_cho": lenh_cho, "lenh_cho_tom": lenh_cho_tom,
            "lenh_cho_ro": lenh_cho_ro, "ung_vien_tien": ung_vien_tien,
            "mot_dong_lenh": mot_dong_lenh,
            "so_theo_lenh": so_theo_lenh, "chum_moi_noi": chum_moi_noi,
            # ⭐ `GAP-API-08` — tuyen 40. ⛔ Quen dong nay la mot duong
            #   **404 im lang**, va cong `soi_bang_tuyen` da bat dung
            #   loi ay **hai lan** roi.
            "lenh_da_gan": lenh_da_gan})
