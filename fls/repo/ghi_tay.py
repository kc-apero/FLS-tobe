"""Cho DUY NHAT ghi thao tac cua NGUOI vao kho (`P5`).

⛔⛔ **Vi sao mot cho duy nhat, va co cong quet ma nguon ep nhu the.**
`QĐ-ITL-16` bo buoc duyet, `QĐ-ITL-27` khai tu vai nguoi hau kiem ⇒ **nhat ky la
cho kiem soat DUY NHAT con lai**. Mot duong ghi khong sinh nhat ky khong phai
*"thieu mot tinh nang"* — no la **mot lo trong lop kiem soat cuoi cung**.

⇒ Moi phep ghi o day di qua `_them()`: no chen **but toan + nhat ky trong CUNG
mot giao dich**, va nhat ky **bat buoc du 7 truong**. Co bai quet ma nguon chan
moi cau `INSERT INTO fls_adjustment|fls_journal|fls_queue_event` nam ngoai file
nay.

★ **Ba luat cua tang nay:**

  ⓐ **THEM, khong SUA.** ⛔ Khong cau `UPDATE`/`DELETE` nao — ke ca len
    `fls_adjustment`. Dao mot but toan la **them mot dong** co `reversal_of`.
    ⛔ KHONG doi `state` cua dong cu: doi trang thai tai cho thi so nhat ky
    khong con la so nhat ky.
  ⓑ **⛔ Khong ghi vao `fls_itl`.** Gia tri nguoi go song trong
    `fls_adjustment`; *"gia tri hien tai"* la khung xem `fls_sua_tay`. Day la
    cho sua mot lech cua `BA-07` §3 — xem migration `0010`.
  ⓒ **`actor` do NGUOI GOI truyen vao, va no phai den TU THE.** Tang cua lay
    `actor` tu the roi dua xuong; ⛔ khong ham nao o day nhan `actor` tu than
    yeu cau.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Sequence

from fls.adapters.pm_join import TY_LE_GHEP_TAY, dung_sai_ghep_tay
from fls.repo.pham_vi import PhamVi

# ── 7 truong nguoi duoc go (`BA-07` §3, `QĐ-owner-0824` + `QĐ-ITL-64`) ──
#
# ⛔⛔ 10 -> 7 ngay 2026-08-28 (`QĐ-ITL-64`). Owner tra loi thang:
# *"ho ko sua [vung ALLOCATE], chi sua cac truong da liet ke truoc do"*.
# ⇒ Ba truong vung ALLOCATE (`cdt1_cfa1` `cdt1_cfa2` `alloc_method`) RA KHOI
# tap nay. Chung ⛔ khong phai cho nguoi go: tren sheet ca ba la **CONG THUC**
# (owner dua nguyen van — xem `fls/ledger/allocate.py`), va quyet dinh phan bo
# nam o **Mapping Master** cot K/L chu ⛔ khong o dong so.
#
# ★ Vi sao viec nay dang mot quyet dinh rieng chu khong phai mot dong sua nho:
# mot truong nam trong tap nay la mot truong **cua duong ghi CHAP NHAN**. De
# ba truong may-suy o day thi som muon co nguoi go de len mot con so may tinh
# ra, va tu do ⛔ khong ai phan biet duoc "may suy dung" voi "nguoi da sua" —
# dung cai `QĐ-ITL-35` dung ra de chan o cot `*_thyt`.
#
# ⭐ NAM truong nay vao hop dong P&L: co cot `*_thyt` song song va co parity.
TRUONG_HOP_DONG: tuple[str, ...] = (
    "hd", "pay_type", "cdt1", "svc_start", "svc_end")
# HAI truong ngoai hop dong: sua duoc nhung ⛔ khong vao P&L.
TRUONG_NGOAI: tuple[str, ...] = ("id_payee", "invoice")
TRUONG_GHI: frozenset[str] = frozenset(TRUONG_HOP_DONG + TRUONG_NGOAI)

# ⛔ Ban TRANG. Ten truong di vao cau SQL nen ⛔ khong duoc nhan bat cu gi ngoai
# danh sach nay — day la cho duy nhat mot chuoi tu ngoai co the cham ten cot.
assert len(TRUONG_GHI) == 7            # `QĐ-ITL-64`: 10 -> 7

# `AUD-1`: nhat ky PHAI du bay truong. Thieu mot cai la mot vet khong doc duoc.
BAY_TRUONG: tuple[str, ...] = (
    "itl_id", "field", "value_before", "value_after", "actor", "at",
    "value_source")

# Nguon cua gia tri DANG co truoc khi nguoi go. ⛔ Khong bao gio de rong:
# `INV-I16` — may khong suy duoc thi noi thang la khong suy duoc.
NGUON_SO = "nguon"          # cot Final cua so goc co gia tri
NGUON_MAY = "may_goi_y"     # chi co goi y `*_thyt`
NGUON_TAY = "sua_tay"       # da co nguoi go truoc do
NGUON_TRONG = "UNMAPPED"    # ca ba deu rong — may KHONG suy duoc


class LoiGhi(Exception):
    """Goc cua moi loi tang ghi. Mang san `ma` de tang cua dich ra HTTP."""

    ma = "FLS-DQ-FAILED"

    def __init__(self, thong_diep: str, **them: Any) -> None:
        super().__init__(thong_diep)
        self.them = them


class NgoaiPhamVi(LoiGhi):
    ma = "FLS-NOT-FOUND"


class TruongLa(LoiGhi):
    ma = "FLS-BAD-REQUEST"


class ThieuLyDo(LoiGhi):
    """⛔ `INV-I16`: ghi mot gia tri ma khong noi vi sao la mot gia tri khong
    truy duoc. Ly do la **bat buoc**, ⛔ khong phai tuy chon."""

    ma = "FLS-UNMAPPED-HIDDEN"


class KyDaChot(LoiGhi):
    ma = "FLS-LOCKED-PERIOD"


class KhacNguon(LoiGhi):
    """`US-025`: he **KEU** khi nguoi go khac nguon. Can `force` + ly do."""

    ma = "FLS-CONFLICT-SOURCE"


class MaLa(LoiGhi):
    """⛔⛔ Ma hop dong ⛔ KHONG co trong `Mapping Master`.

    ⭐ Vi sao chan duoc: do that tren kho — danh muc co **73 ma**, va **0** ma
    `hd` trong so nam ngoai no. Nghia la danh muc nay **co tham quyen**, ⛔ chu
    ⛔ khong phai mot danh sach goi y.

    ⛔⛔ Va vi sao `force` ⛔ **KHONG** vuot qua duoc: `force` sinh ra cho ca
    *"go khac nguon"* — mot bat dong giua hai cau tra loi **deu co that**. Mot
    ma ⛔ khong ton tai thi ⛔ khong phai bat dong, no la **mot cai ⛔ khong co**.
    Cho `force` di qua la bien phep kiem thanh mot loi nhac bo qua duoc.

    ⚠ Nhung phep chan phai **noi duoc buoc tiep theo**: neu ma vua duoc lap
    ben `Mapping Master` that thi ban khai cua FLS dang **cu**, va ke toan bi
    chan ma ⛔ khong biet vi sao. ⇒ Loi mang ca so ma dang giu va **ten cong cu
    nap lai**.
    """

    ma = "FLS-UNKNOWN-CODE"


class KhuonLa(LoiGhi):
    """⛔ Gia tri sai KHUON *(vi du ky dich vu phai la `YYYYMM`)*.

    ⚠ Hai o `svc_start`/`svc_end` **⛔ khong phai NGAY** du ten cot doc la
    *"Thoi diem bat dau su dung dich vu"* — do that: **99,8%** gia tri la
    `YYYYMM`, tuc la mot **KY**. Dat mot o chon ngay o day la ghi
    `2024-12-01` vao cho so cho doi `202412`.
    """

    ma = "FLS-BAD-FORMAT"


# ── ghep lenh (`OP-02`, `QĐ-ITL-48`) ─────────────────────────────────────
class DaGhep(LoiGhi):
    """Dong so nay DA co moi noi. ⛔ Khong them moi noi vao mot dong da ghep:
    lam the la pha bat bien `Σ moi noi = tien dong bank`."""

    ma = "FLS-CONFLICT-SOURCE"


class ChuaXong(LoiGhi):
    """⛔ Mo lai mot dong ⛔ chua tung duoc bam xong. Cau tra loi phai KHAC
    *"da xong"*: man hinh ve hai nut khac nhau cho hai trang thai."""

    ma = "FLS-CONFLICT-SOURCE"


class ThieuLyDoGhiDe(LoiGhi):
    """⛔⛔ **KHONG con duoc nem tu 2026-08-28** — owner bo hang rao ly do khi
    bam *xong* (`QĐ-ITL-72`, nguyen van *"ko can ghi ly do"*).

    ★ Giu lop nay lai CO Y, ⛔ khong xoa: no la **cai bia mo** cua mot hang rao
      da co roi bo, va co bai test khoa dung chieu ay
      (`test_KHONG_doi_ly_do_khi_con_thieu__owner_da_bo_hang_rao`). Neu mai co
      ai "chua" bang cach bat ly do lai thi ho se thay ten lop nay va doc duoc
      **vi sao no da bi bo**, thay vi phat minh lai lap luan cu.
    """

    ma = "FLS-DQ-FAILED"


class KhongCoMoiNoi(LoiGhi):
    """⛔ Bo mot thu ⛔ khong ton tai. Cau tra loi phai KHAC `DaGhep`: mot dong
    chua ghep va mot dong da ghep la hai trang thai, va man hinh ve hai nut
    khac nhau."""

    ma = "FLS-CONFLICT-SOURCE"


class DongLenhLa(LoiGhi):
    """Ma dong lenh khong nam trong anh chup CUA LAN NAP do."""

    ma = "FLS-BAD-REQUEST"


class KhacTienTe(LoiGhi):
    """⛔ Cong hai so khac don vi ra mot con so **trong hinh** nhung vo nghia —
    va neu no tinh co bang nhau thi ta vua ghep sai ma khong cong nao do.
    Cung luat voi hinh `E` cua bo nap (199 dong that)."""

    ma = "FLS-DQ-FAILED"


class LechTong(LoiGhi):
    """⛔ `Σ dong lenh != tien dong bank` ⇒ **giu UNMAPPED**, ⛔ khong chia bua."""

    ma = "FLS-DQ-FAILED"


class ChuaDuyet(LoiGhi):
    """Dong lenh co `status` ⛔ khong phai `Approve`. Can `force` + ly do."""

    ma = "FLS-DQ-FAILED"


@dataclass(frozen=True)
class KetQuaGhi:
    adj_id: int | None
    jrn_id: int | None
    evt_id: int | None = None
    da_co: bool = False
    value_before: str | None = None
    value_source: str = ""


# ── doc trang thai truoc khi ghi ─────────────────────────────────────────
def _dong_trong_pham_vi(conn, pv: PhamVi, itl_id: int) -> dict[str, Any]:
    """⛔ NO neu dong khong ton tai HAY ngoai pham vi. Cung mot cau tra loi cho
    ca hai — cua ghi ⛔ khong duoc tiet lo rang mot dong ngoai pham vi ton tai."""
    dk, ts = pv.dieu_kien("i.run_id")
    cot = ", ".join(f"i.{c}" for c in TRUONG_GHI)
    thyt = ", ".join(f"i.{c}_thyt" for c in TRUONG_HOP_DONG)
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT i.itl_id, i.period_state, i.work_status, {cot}, {thyt}"
            f" FROM fls_itl i WHERE i.itl_id = %s AND {dk}", [itl_id, *ts])
        r = cur.fetchone()
        if r is None:
            raise NgoaiPhamVi(f"itl_id={itl_id} khong co hay ngoai {pv.mo_ta()}")
        ten = [d.name for d in cur.description]
    return dict(zip(ten, r))


def _hieu_luc(conn, itl_id: int, field: str) -> tuple[str | None, int | None]:
    with conn.cursor() as cur:
        cur.execute("SELECT value_after, adj_id FROM fls_sua_tay"
                    " WHERE itl_id = %s AND field = %s", (itl_id, field))
        r = cur.fetchone()
    return (None, None) if r is None else (r[0], r[1])


def truoc_khi_go(conn, pv: PhamVi, itl_id: int, field: str) -> dict[str, Any]:
    """Gia tri dang co + no den TU DAU. Man hinh dung de hien *"nguon noi X"*."""
    if field not in TRUONG_GHI:
        # ⚠ Con so trong thong bao PHAI suy tu tap thuc, ⛔ khong go tay: cau
        # nay tung ghi "chi 10 truong" roi liet ke 7 (QĐ-ITL-64 ha 10->7) — mot
        # thong bao tu mau thuan lam nguoi doc nghi may dang hong.
        raise TruongLa(f"truong {field!r} ⛔ khong duoc go — chi "
                       f"{len(TRUONG_GHI)} truong: {sorted(TRUONG_GHI)}")
    d = _dong_trong_pham_vi(conn, pv, itl_id)
    tay, adj_id = _hieu_luc(conn, itl_id, field)
    nguon = d.get(field)
    may = d.get(f"{field}_thyt") if field in TRUONG_HOP_DONG else None
    if tay is not None:
        gia_tri, tu = tay, NGUON_TAY
    elif nguon is not None:
        gia_tri, tu = nguon, NGUON_SO
    elif may is not None:
        gia_tri, tu = may, NGUON_MAY
    else:
        gia_tri, tu = None, NGUON_TRONG
    return {"dong": d, "gia_tri": gia_tri, "value_source": tu,
            "nguon": nguon, "may": may, "tay": tay, "adj_id": adj_id}


# ── CHO DUY NHAT ghi ─────────────────────────────────────────────────────
def _them(conn, *, itl_id: int, field: str, value_before: str | None,
          value_after: str | None, actor: str, value_source: str,
          reason: str, reversal_of: int | None = None,
          state: str = "posted", evt_id: int | None = None) -> tuple[int, int]:
    """Chen but toan + nhat ky **trong CUNG mot giao dich**. ⛔ Cho duy nhat.

    ⛔ Neu hai cau nay khong cung mot giao dich thi se co luc kho co but toan
    ma **khong co vet ai lam** — dung cai lop kiem soat cuoi cung nay dung ra
    de chan.
    """
    if not (reason or "").strip():
        raise ThieuLyDo(
            "⛔ moi phep ghi phai co LY DO (`INV-I16`): mot gia tri khong noi "
            "vi sao la mot gia tri khong truy duoc")
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor` — nhat ky khong biet ai lam thi vo nghia")
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO fls_adjustment (itl_id, field, value_after, state,"
                " reversal_of, actor, evt_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                " RETURNING adj_id",
                (itl_id, field, value_after, state, reversal_of, actor,
                 evt_id))
            adj_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO fls_journal (itl_id, field, value_before,"
                " value_after, actor, value_source, reason)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING jrn_id",
                (itl_id, field, value_before, value_after, actor,
                 value_source, reason))
            jrn_id = cur.fetchone()[0]
    return adj_id, jrn_id


def _them_su_kien(conn, *, itl_id: int, evt_type: str, actor: str,
                  reason: str | None, defer_until: Any = None) -> int:
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor`")
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fls_queue_event (itl_id, evt_type, reason,"
            " defer_until, actor) VALUES (%s,%s,%s,%s,%s) RETURNING evt_id",
            (itl_id, evt_type, reason, defer_until, actor))
        return cur.fetchone()[0]


# ── bon thao tac ─────────────────────────────────────────────────────────
KY_KHUON = re.compile(r"\A\d{4}(0[1-9]|1[0-2])\Z")
O_KY: frozenset[str] = frozenset({"svc_start", "svc_end"})


def _kiem_gia_tri(conn, field: str, value: str | None) -> None:
    """⛔ NO neu gia tri ⛔ khong hop le. ⭐ O RONG luon di qua.

    ⚠ **O rong ⛔ khong phai mot gia tri sai — no la phep BO GAN.** Chan no la
    cat mat duong lui: ke toan gan nham roi thi ⛔ khong xoa lai duoc.
    """
    v = "" if value is None else str(value).strip()
    if v == "":
        return

    if field in O_KY and not KY_KHUON.match(v):
        raise KhuonLa(
            f"{field}={v!r} ⛔ khong dung khuon KY `YYYYMM` (vi du `202412`). "
            f"⚠ O nay la mot **KY**, ⛔ khong phai mot NGAY — 99,8% dong trong "
            f"so dang dung khuon ay.")

    if field == "hd":
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM fls_mapping_master WHERE hd_code = %s",
                        (v,))
            if cur.fetchone() is not None:
                return
            cur.execute("SELECT count(*) FROM fls_mapping_master")
            co_bao_nhieu = cur.fetchone()[0]
            # ⛔⛔ **DANH MUC RONG ⇒ may ⛔ KHONG BIET, ⛔ chu ⛔ khong phai
            #   "moi ma deu sai".** Chan het moi phep ghi vi ban khai chua
            #   duoc nap la mot cai may noi *"sai"* trong khi y no la *"toi
            #   ⛔ khong biet"* — dung cai lan lon ma `INV-I16` sinh ra de
            #   chan (`UNMAPPED` ⛔ khong phai mot gia tri).
            # ⭐ Cho di qua, nhung cho **RONG phai nhin thay duoc** o cho no
            #   co nghia: man hinh noi thang *"⛔ chua co danh muc"* ngay canh
            #   o go, ⛔ khong de nguoi ta tuong minh dang duoc kiem.
            if co_bao_nhieu == 0:
                return
            # ⭐ Truoc khi NO, soi xem co ma nao chi khac HOA-THUONG. Khoa
            #   `hd_code` phan biet hoa thuong, con phep tra cua Sheets thi
            #   ⛔ khong ⇒ nguoi go rat de gap dung cho nay, va mot cau
            #   *"⛔ khong co ma nay"* se lam ho di tim mot thu van dang o do.
            cur.execute("SELECT hd_code FROM fls_mapping_master"
                        " WHERE lower(hd_code) = lower(%s)", (v,))
            gan = cur.fetchone()
            n = co_bao_nhieu
        if gan is not None:
            raise MaLa(f"⛔ khong co ma {v!r} trong danh muc — nhung CO "
                       f"{gan[0]!r} (chi khac hoa-thuong). Y ban la ma do?")
        raise MaLa(
            f"⛔ khong co ma hop dong {v!r} trong `Mapping Master`. Danh muc "
            f"FLS dang giu **{n} ma**. ⚠ Neu ma nay vua duoc lap ben so goc "
            f"thi ban khai cua FLS dang CU — chay "
            f"`python tools/nap_mapping_master.py --ghi` de nap lai, roi go "
            f"lai. ⛔ `force` ⛔ khong vuot qua duoc phep kiem nay.")


def ghi_but_toan(conn, pv: PhamVi, itl_id: int, field: str,
                 value: str | None, *, actor: str, reason: str,
                 force: bool = False) -> KetQuaGhi:
    """Nguoi go mot gia tri. ⛔ NO neu khac nguon ma chua `force` (`US-025`).

    ★ **Lap lai cung gia tri thi ⛔ khong chen dong thu hai** (`da_co=True`).
    Ly do: mot cai nut bi bam hai lan ⛔ khong duoc thanh hai but toan — nhung
    day cung la mot cho MAT thong tin, khai ra: neu ai co y *"xac nhan lai"*
    cung gia tri thi lan xac nhan do ⛔ khong vao so.
    """
    t = truoc_khi_go(conn, pv, itl_id, field)
    d = t["dong"]

    # `INV-I13`: ky da chot thi ⛔ khong ghi, ke ca co `force`.
    if d["period_state"] == "locked":
        raise KyDaChot(f"itl_id={itl_id} nam trong ky da CHOT — ⛔ khong ghi "
                       f"duoc, ke ca voi force")

    if t["gia_tri"] == value and t["tay"] is not None:
        return KetQuaGhi(adj_id=t["adj_id"], jrn_id=None, da_co=True,
                         value_before=t["gia_tri"],
                         value_source=t["value_source"])

    # `US-025`: he KEU khi go khac nguon hay khac goi y cua may.
    khac = []
    if t["nguon"] is not None and t["nguon"] != value:
        khac.append(("nguon", t["nguon"]))
    if t["may"] is not None and t["may"] != value:
        khac.append(("may_goi_y", t["may"]))
    if khac and not force:
        raise KhacNguon(
            f"gia tri go ({value!r}) khac gia tri dang co — "
            + " · ".join(f"{k}={v!r}" for k, v in khac)
            + ". Muon ghi de thi phai gui `force=true` VA ly do",
            khac={k: v for k, v in khac}, gia_tri_go=value)

    # ⭐⭐ KIEM GIA TRI — dat SAU phep `force` co y: `force` giai quyet mot
    #   **bat dong**, con hai phep duoi giai quyet mot **gia tri ⛔ khong hop
    #   le**. Hai chuyen khac han, va cai thu hai thi ⛔ khong ai duoc bo qua.
    _kiem_gia_tri(conn, field, value)

    adj_id, jrn_id = _them(
        conn, itl_id=itl_id, field=field, value_before=t["gia_tri"],
        value_after=value, actor=actor, value_source=t["value_source"],
        reason=reason)
    return KetQuaGhi(adj_id=adj_id, jrn_id=jrn_id,
                     value_before=t["gia_tri"], value_source=t["value_source"])


def dao_but_toan(conn, pv: PhamVi, adj_id: int, *, actor: str,
                 reason: str) -> KetQuaGhi:
    """Dao mot but toan = **them mot dong** tro toi no (`SM-I03`, `INV-I08`).

    ⛔ Khong `UPDATE state` cua dong cu, ⛔ khong `DELETE`. Sau khi dao, gia tri
    hieu luc tu dong lui ve but toan truoc do — hay ve gia tri nguon neu khong
    con but toan nao.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT itl_id, field, value_after, reversal_of"
                    " FROM fls_adjustment WHERE adj_id = %s", (adj_id,))
        r = cur.fetchone()
    if r is None:
        raise NgoaiPhamVi(f"khong co but toan adj_id={adj_id}")
    itl_id, field, value_cu, la_ban_dao = r
    if la_ban_dao is not None:
        raise LoiGhi(f"adj_id={adj_id} da la mot BAN DAO — ⛔ khong dao mot ban dao")
    with conn.cursor() as cur:
        cur.execute("SELECT adj_id FROM fls_adjustment WHERE reversal_of = %s",
                    (adj_id,))
        if cur.fetchone():
            raise LoiGhi(f"adj_id={adj_id} da bi dao truoc do")

    # ⛔ Kiem pham vi + ky chot TRUOC khi ghi.
    d = _dong_trong_pham_vi(conn, pv, itl_id)
    if d["period_state"] == "locked":
        raise KyDaChot(f"itl_id={itl_id} nam trong ky da CHOT")

    moi_id, jrn_id = _them(
        conn, itl_id=itl_id, field=field, value_before=value_cu,
        value_after=None, actor=actor, value_source=NGUON_TAY, reason=reason,
        reversal_of=adj_id, state="reversed")
    return KetQuaGhi(adj_id=moi_id, jrn_id=jrn_id, value_before=value_cu,
                     value_source=NGUON_TAY)


def ghi_ly_do(conn, pv: PhamVi, itl_id: int, *, reason: str,
              actor: str) -> KetQuaGhi:
    """Cot LY DO cua hang cho (`US-039`) — day la cot `US-045` dem."""
    if not (reason or "").strip():
        raise ThieuLyDo("⛔ ly do rong thi khong phai mot ly do")
    _dong_trong_pham_vi(conn, pv, itl_id)
    return KetQuaGhi(adj_id=None, jrn_id=None,
                     evt_id=_them_su_kien(conn, itl_id=itl_id,
                                          evt_type="reason", actor=actor,
                                          reason=reason))


def ghi_hoan(conn, pv: PhamVi, itl_id: int, *, den_ngay: Any, reason: str,
             actor: str) -> KetQuaGhi:
    """Hoan CO HAN (`US-040`). ⛔ Khong leo cap — `QĐ-ITL-24`: khong co cap tren.

    ⭐ Lan hoan thu ba **doi mau tren man hinh**, ⛔ khong bao cho ai. Nen ham
    nay tra `so_lan_hoan` de man hinh tu doi mau, va ⛔ khong chan lan thu ba:
    chan lai la dung mot cai bo may khong co nguoi thu hai de xu ly.
    """
    if not (reason or "").strip():
        raise ThieuLyDo("⛔ hoan phai noi vi sao hoan")
    if not den_ngay:
        raise TruongLa("⛔ hoan phai co HAN (`until`) — hoan vo han la bo qua")
    _dong_trong_pham_vi(conn, pv, itl_id)
    evt = _them_su_kien(conn, itl_id=itl_id, evt_type="defer", actor=actor,
                        reason=reason, defer_until=den_ngay)
    return KetQuaGhi(adj_id=None, jrn_id=None, evt_id=evt)


# ── GHEP LENH BANG TAY ──────────────────────────────────────────────
#
# ★★ `OP-02` / `QĐ-ITL-48`: **ghep tien voi lenh chi la viec cua ke toan FLS**,
# ⛔ khong day len he lenh chi. Mo duoc tu 27/08 nho anh chup `fls_pm_line`
# (owner chot duong (a) — dong `GAP-API-04`).
#
# ⛔⛔ **VA DAY LA MOT CHO SUA DAC TA, ⛔ khong phai lam theo dac ta.** `BA-07` §2
# viet than yeu cau la `{pm_id}` — tuc ghep vao mot **PHIEU**. So lieu lat cau do:
# do tren 3.703 dong lenh that, `reference` va tien song o **DONG**, va **526
# phieu mang 2–36 reference KHAC NHAU**. Ghep vao phieu thi may buoc phai **tu
# chon dong nao trong phieu** — do la **may quyet thay nguoi** (`INV-I16`), dung
# thu ca tang nay dung ra de chan. ⇒ than yeu cau la **danh sach ma DONG**
# (`CR#6`).
#
# ★ Thu tu cac phep kiem la CO CHU Y, va giong thu tu cua bo nap:
#   ⓐ dong co trong pham vi khong        -> 404 (⛔ cung cau tra loi voi "khong co")
#   ⓑ ky da chot chua                    -> 409, ⛔ ke ca `force`
#   ⓒ dong nay DA ghep chua              -> 409 kem moi noi dang co
#   ⓓ ma dong lenh co trong ANH CHUP cua CHINH lan nap do khong -> 400
#   ⓔ **TIEN TE** khop khong             -> 422  (kiem TRUOC Σ)
#   ⓕ **Σ** khop khong                   -> 422 kem ba con so
#   ⓖ `status` cua dong lenh co la `Approve` khong -> 422 tru khi `force`
# Chi khi ca bay dat moi ghi — va ghi trong MOT giao dich.
_HINH_TAY = "T"


def _tien_dong_so(conn, itl_id: int) -> tuple[Any, str, str]:
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(ps_no,0) + COALESCE(ps_co,0), curr, run_id"
                    " FROM fls_itl WHERE itl_id = %s", (itl_id,))
        r = cur.fetchone()
    return r[0], (r[1] or "").strip().upper(), r[2]


def ghep_lenh(conn, pv: PhamVi, itl_id: int, ma_dong: Sequence[str], *,
              actor: str, reason: str, force: bool = False) -> dict[str, Any]:
    """Ghep MOT dong so voi N dong lenh chi. ⛔ Σ lech thi ⛔ khong ghi gi.

    ⛔ `fls_itl` ⛔ KHONG doi mot o nao (`INV-I08`). Ket qua ghep song o:
      · `fls_pm_link`   — cac moi noi, `hinh = 'T'` (tay)
      · `fls_queue_event` — vet thao tac (ai · luc nao · vi sao)
      · `fls_adjustment` + `fls_journal` — `hd`/`cdt1` **suy tu dong lenh**,
        va CHI khi ca N dong lenh **dong y** mot gia tri khac rong.

    ★ `hd`/`cdt1` la ly do that de ke toan ghep: dong lenh mang chung. Nhung neu
    N dong lenh noi N thu khac nhau thi may ⛔ khong duoc chon — no **khai ra la
    khong suy duoc** (`khong_suy_duoc`), dung `INV-I16`.
    """
    # ⛔⛔ LO THAT bat duoc 27/08 boi chinh bo test: `_them` co kiem ly do nhung
    # no CHI chay khi co `hd`/`cdt1` de ghi, con `_them_su_kien` thi ⛔ khong
    # kiem. ⇒ mot phep ghep khong co ly do van di qua, va vet trong
    # `fls_queue_event` mang `reason` RONG. Kiem o day, TRUOC moi thu khac.
    if not (reason or "").strip():
        raise ThieuLyDo(
            "⛔ phep ghep phai co LY DO (`INV-I16`): mot moi noi khong noi vi "
            "sao la mot moi noi khong truy duoc")
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor` — nhat ky khong biet ai ghep thi vo nghia")
    if not ma_dong:
        raise DongLenhLa("⛔ khong co ma dong lenh nao — ghep vao dau?")
    ma_dong = [str(x).strip() for x in ma_dong if str(x).strip()]
    if len(set(ma_dong)) != len(ma_dong):
        raise DongLenhLa(f"ma dong lenh LAP trong cung mot phep ghep: {ma_dong}")

    d = _dong_trong_pham_vi(conn, pv, itl_id)                        # ⓐ
    if (d.get("period_state") or "").strip() == "locked":            # ⓑ
        raise KyDaChot(f"itl_id={itl_id} thuoc ky DA CHOT — ⛔ `force` cung "
                       f"khong mo duoc ky da chot")

    # ⚠ Doc KHUNG XEM `fls_moi_noi`, ⛔ khong doc `fls_pm_link`: tu migration
    # `0013` bang goc con giu ca nhung moi noi DA BO, nen doc bang goc o day se
    # tra ve *"dong nay da ghep"* cho mot dong vua duoc go — mot cau tra loi
    # sai ma ⛔ khong bao loi.
    dang_co = _moi_noi_hieu_luc(conn, itl_id)
    if dang_co:                                                      # ⓒ
        raise DaGhep(
            f"itl_id={itl_id} DA co {len(dang_co)} moi noi — muon ghep lai thi "
            f"phai BO moi noi cu truoc (`POST .../unmatch`, `QĐ-ITL-69`)",
            khac={"moi_noi": dang_co})

    tien, cur_so, run_id = _tien_dong_so(conn, itl_id)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pm_line_id, amount, curr, status, hd, cdt1, pm_slip_id"
            " FROM fls_pm_line WHERE run_id = %s AND pm_line_id = ANY(%s)",
            (run_id, list(ma_dong)))
        ten = [x.name for x in cur.description]
        lenh = [dict(zip(ten, r)) for r in cur.fetchall()]
    thieu = sorted(set(ma_dong) - {x["pm_line_id"] for x in lenh})
    if thieu:                                                        # ⓓ
        raise DongLenhLa(
            f"{len(thieu)} ma dong lenh ⛔ khong co trong anh chup cua lan nap "
            f"{run_id!r}: {thieu[:5]}", khac={"thieu": thieu})

    te = {(x["curr"] or "").strip().upper() for x in lenh}
    if te != {cur_so}:                                               # ⓔ
        raise KhacTienTe(
            f"dong so la {cur_so!r} nhung dong lenh la {sorted(te)} — ⛔ khong "
            f"cong hai don vi khac nhau",
            khac={"bank": cur_so, "lenh": sorted(te)})

    tong = sum((x["amount"] or Decimal(0) for x in lenh), Decimal(0))
    # `QĐ-ITL-63`: cua TAY doi CA HAI dieu kien (<=1.000 dong VA <=0,5%), lay
    # cai NHO hon — ⛔ khong dung con so cua cua TU DONG.
    tien_d = Decimal(str(tien or 0))
    ds = dung_sai_ghep_tay({cur_so}, tien_d)
    lech = tong - tien_d
    if abs(lech) > ds:                                               # ⓕ
        raise LechTong(
            f"Σ dong lenh {tong} vs tien bank {tien} · lech {lech} "
            f"(dung sai {ds.normalize()} = min(1.000 dong, "
            f"{(TY_LE_GHEP_TAY * 100).normalize()}% cua {tien_d})) "
            "⇒ GIU UNMAPPED, ⛔ khong chia bua",
            khac={"tong_lenh": str(tong), "tien_bank": str(tien),
                  "lech": str(lech), "dung_sai": str(ds),
                  "ty_le": str(TY_LE_GHEP_TAY)})

    chua = [x["pm_line_id"] for x in lenh
            if (x["status"] or "").strip().lower() != "approve"]
    if chua and not force:                                           # ⓖ
        raise ChuaDuyet(
            f"{len(chua)} dong lenh co `status` ⛔ khong phai 'Approve': "
            f"{chua[:5]} — go lai voi `force` kem ly do neu van muon ghep",
            khac={"chua_duyet": chua})

    # ── chia tien: mot dong lenh thi lay tron tien bank; nhieu thi theo `amount`
    if len(lenh) == 1:
        phan = {lenh[0]["pm_line_id"]: Decimal(str(tien or 0))}
    else:
        phan = {x["pm_line_id"]: (x["amount"] or Decimal(0)) for x in lenh}
        du = Decimal(str(tien or 0)) - sum(phan.values(), Decimal(0))
        if du:
            # ⚠ Chenh trong dung sai: don vao phan LON NHAT (phep chon ON DINH,
            # chay lai cho y het) — cung luat voi `chia_tien` cua bo nap.
            k = max(sorted(phan), key=lambda x: phan[x])
            phan[k] += du
    if sum(phan.values(), Decimal(0)) != Decimal(str(tien or 0)):
        raise AssertionError(
            f"⛔ chia tien lech: {sum(phan.values(), Decimal(0))} != {tien}")

    # ── `hd`/`cdt1` suy tu dong lenh: CHI khi ca N dong dong y ──────────
    suy: dict[str, str] = {}
    khong_suy_duoc: list[str] = []
    for f in ("hd", "cdt1"):
        gt = {(x[f] or "").strip() for x in lenh}
        gt.discard("")
        if len(gt) == 1:
            suy[f] = next(iter(gt))
        elif gt:
            khong_suy_duoc.append(f)      # N dong noi N thu — may ⛔ khong chon

    # ── ghi: MOT giao dich cho ca ba viec ─────────────────────
    # ⚠ `lan` = lan ghep thu may cua tung cap (dong so, dong lenh). Ghep lai
    # dung mot dong lenh sau khi da bo la chuyen THUONG, nen phai dem — khoa
    # `(itl_id, pm_line_id, lan)` se chan neu quen (migration `0013`).
    lan_cua = _lan_ke_tiep(conn, itl_id, sorted(phan))

    with conn.transaction():
        # ⚠ Su kien PHAI chen TRUOC: cac but toan suy tu dong lenh mang `evt_id`
        # tro ve day, va do la cach duy nhat phep BO nhan ra chung.
        evt_id = _them_su_kien(
            conn, itl_id=itl_id, evt_type="match", actor=actor,
            reason=(f"{reason} · ghep tay {len(phan)} dong lenh "
                    f"({', '.join(sorted(phan))})"
                    + (" · FORCE chua duyet: " + ",".join(chua) if chua else "")))
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                " run_id, lan) VALUES (%s,%s,%s,%s,%s,%s)",
                [(itl_id, k, v, _HINH_TAY, run_id, lan_cua[k])
                 for k, v in sorted(phan.items())])
        but: list[dict[str, Any]] = []
        for f, v in sorted(suy.items()):
            cu, _adj = _hieu_luc(conn, itl_id, f)
            truoc = cu if cu is not None else d.get(f)
            if (truoc or "") == v:
                continue                  # da dung roi — ⛔ khong them dong rong
            adj_id, jrn_id = _them(
                conn, itl_id=itl_id, field=f, value_before=truoc, value_after=v,
                actor=actor, value_source=NGUON_TAY, evt_id=evt_id,
                reason=f"{reason} · suy tu dong lenh da ghep "
                       f"({', '.join(sorted(phan))})")
            but.append({"field": f, "value_after": v, "adj_id": adj_id,
                        "jrn_id": jrn_id})

    return {
        "itl_id": itl_id, "run_id": run_id, "evt_id": evt_id,
        "moi_noi": [{"pm_line_id": k, "amount": str(v), "hinh": _HINH_TAY}
                    for k, v in sorted(phan.items())],
        "phieu": sorted({x["pm_slip_id"] for x in lenh}),
        "but_toan": but,
        # ⛔ Khai thang thu may KHONG suy duoc (`INV-I16`).
        "khong_suy_duoc": khong_suy_duoc,
        "chua_duyet": chua,
        "tien_bank": str(tien), "tong_lenh": str(tong), "dung_sai": str(ds),
    }


# ── BO MOI NOI (`GAP-JOIN-05`, `QĐ-ITL-69`) ─────────────────────────────
#
# ★★ **Vi sao cua nay ton tai.** Tu 27/08 ke toan ghep duoc tien voi dong lenh,
# nhung ⛔ khong go duoc mot moi noi ghep sai — chinh `ghep_lenh` phai NO ra cau
# *"chua co duong nao lam viec do"*. Mot dong ghep sai vi the la mot dong **chet
# cung**: ⛔ khong go, ⛔ khong ghep lai. Mo man hang cho ma thieu cua nay la
# giao cho ke toan mot cai nut ⛔ khong co duong lui.
#
# ⛔⛔ **Ba quyet dinh thiet ke, va ly do do duoc cua tung cai:**
#
#   ⓐ **BO CA CHUM, ⛔ khong bo le mot moi noi.** Bat bien cua bang noi la
#     `Σ moi noi = tien dong bank` (cong `SIGMA_MOI_NOI`). Bo le mot trong ba
#     moi noi thi Σ con 2/3 tien ⇒ **cong do se do**, va do la mot cai do DUNG:
#     trang thai ay that su sai. ⇒ Cua nay bo **toan bo** moi noi cua dong roi
#     de nguoi ghep lai — ⛔ khong mo duong tao ra mot trang thai sai.
#
#   ⓑ **Dao dung nhung but toan cua CHINH phep ghep, va CHI khi chung con hieu
#     luc.** Phep ghep tu suy `hd`/`cdt1` tu dong lenh; bo moi noi thi **can cu
#     cua phep suy mat**, nen de nguyen la de lai mot gia tri ⛔ khong con nguon
#     — dung thu `INV-I16` cam. Nhung neu sau do **NGUOI da go tay** len dung o
#     ay thi ⛔ KHONG dao: cai dang co hieu luc la gia tri cua NGUOI, va may
#     ⛔ khong duoc dap len no. ⇒ nhung but toan bi bo qua duoc **khai ra**
#     (`bo_qua`), ⛔ khong im lang.
#
#   ⓒ **Ky da CHOT thi ⛔ khong bo, ke ca `force`** — cung luat `INV-I13` voi
#     moi cua ghi khac. Ghep sai trong mot ky da chot la viec cua but toan dieu
#     chinh ky sau, ⛔ khong phai viec sua lai qua khu.
def _moi_noi_hieu_luc(conn, itl_id: int) -> list[dict[str, Any]]:
    """Moi noi DANG CO HIEU LUC. ⛔ Doc khung xem, ⛔ khong doc `fls_pm_link`."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT link_id, pm_line_id, amount, hinh, lan FROM fls_moi_noi"
            " WHERE itl_id = %s ORDER BY pm_line_id", (itl_id,))
        return [{"link_id": r[0], "pm_line_id": r[1], "amount": str(r[2]),
                 "hinh": r[3], "lan": int(r[4])} for r in cur.fetchall()]


def _lan_ke_tiep(conn, itl_id: int, ma_dong: Sequence[str]) -> dict[str, int]:
    """`lan` ke tiep cho tung cap (dong so, dong lenh) — dem CA LICH SU.

    ⛔ Dem tren khung xem la sai: mot moi noi da bo van chiem `lan` cua no
    trong bang goc, nen dem tren khung xem se sinh lai `lan=1` va trung khoa.
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT pm_line_id, MAX(lan) FROM fls_pm_link"
            " WHERE itl_id = %s AND pm_line_id = ANY(%s) GROUP BY pm_line_id",
            (itl_id, list(ma_dong)))
        cu = {r[0]: int(r[1]) for r in cur.fetchall()}
    return {m: cu.get(m, 0) + 1 for m in ma_dong}


def bo_moi_noi(conn, pv: PhamVi, itl_id: int, *, actor: str,
               reason: str) -> dict[str, Any]:
    """Bo TOAN BO moi noi cua mot dong so = **them cac dong bo** (`INV-I08`).

    ⛔ Khong `DELETE`, ⛔ khong `UPDATE`. Sau khi bo, dong tu quay lai hang cho:
    hang cho ⛔ khong doc mot o trang thai nao ma la mot **phep tinh** *(khong
    con moi noi hieu luc)* — xem `doc_bao_cao._SQL_HANG_CHO`.
    """
    if not (reason or "").strip():
        raise ThieuLyDo(
            "⛔ phep BO moi noi phai co LY DO (`INV-I16`): go mot moi noi ma "
            "khong noi vi sao thi ⛔ khong ai biet lan ghep nao dung")
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor` — nhat ky khong biet ai bo thi vo nghia")

    d = _dong_trong_pham_vi(conn, pv, itl_id)                        # ⓐ
    if (d.get("period_state") or "").strip() == "locked":            # ⓑ
        raise KyDaChot(
            f"itl_id={itl_id} thuoc ky DA CHOT — ⛔ khong bo moi noi, ke ca voi "
            f"`force`. Ghep sai trong ky da chot xu bang but toan dieu chinh ky "
            f"sau, ⛔ khong sua lai qua khu")

    moi_noi = _moi_noi_hieu_luc(conn, itl_id)                        # ⓒ
    if not moi_noi:
        raise KhongCoMoiNoi(
            f"itl_id={itl_id} ⛔ khong co moi noi nao dang co hieu luc — "
            f"⛔ khong co gi de bo")

    # ── but toan cua CHINH cac phep ghep cua dong nay, va con hieu luc ──
    with conn.cursor() as cur:
        cur.execute(
            "SELECT a.adj_id, a.field, a.value_after"
            "  FROM fls_adjustment a"
            "  JOIN fls_queue_event e ON e.evt_id = a.evt_id"
            " WHERE a.itl_id = %s AND e.evt_type = 'match'"
            "   AND a.reversal_of IS NULL"
            " ORDER BY a.adj_id", (itl_id,))
        cua_ghep = [{"adj_id": r[0], "field": r[1], "value_after": r[2]}
                    for r in cur.fetchall()]
    con_hieu_luc = {r["adj_id"] for r in cua_ghep}
    if con_hieu_luc:
        with conn.cursor() as cur:
            cur.execute("SELECT adj_id FROM fls_sua_tay WHERE itl_id = %s",
                        (itl_id,))
            dang_dung = {r[0] for r in cur.fetchall()}
        con_hieu_luc &= dang_dung

    se_dao = [x for x in cua_ghep if x["adj_id"] in con_hieu_luc]
    # ⛔ Khai ra thu ⛔ KHONG dao, va noi vi sao — im lang la lo (`INV-I16`).
    bo_qua = [dict(x, vi_sao="⛔ khong con hieu luc: da bi dao, hay NGUOI da go "
                             "tay len o nay sau phep ghep ⇒ may ⛔ khong dap len")
              for x in cua_ghep if x["adj_id"] not in con_hieu_luc]

    ma_dong = sorted(x["pm_line_id"] for x in moi_noi)
    with conn.transaction():
        evt_id = _them_su_kien(
            conn, itl_id=itl_id, evt_type="unmatch", actor=actor,
            reason=(f"{reason} · bo {len(moi_noi)} moi noi "
                    f"({', '.join(ma_dong)})"))
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO fls_pm_unlink (link_id, itl_id, evt_id)"
                " VALUES (%s,%s,%s)",
                [(x["link_id"], itl_id, evt_id) for x in moi_noi])
        da_dao: list[dict[str, Any]] = []
        for x in se_dao:
            moi_id, jrn_id = _them(
                conn, itl_id=itl_id, field=x["field"],
                value_before=x["value_after"], value_after=None, actor=actor,
                value_source=NGUON_TAY, reversal_of=x["adj_id"],
                state="reversed", evt_id=evt_id,
                reason=f"{reason} · dao but toan suy tu phep ghep da bo "
                       f"({', '.join(ma_dong)})")
            da_dao.append({"field": x["field"], "dao_cua": x["adj_id"],
                           "adj_id": moi_id, "jrn_id": jrn_id})

    return {
        "itl_id": itl_id, "evt_id": evt_id,
        "da_bo": [{"pm_line_id": x["pm_line_id"], "amount": x["amount"],
                   "hinh": x["hinh"], "lan": x["lan"], "link_id": x["link_id"]}
                  for x in moi_noi],
        "but_toan_dao": da_dao,
        # ⛔ Nhung but toan cua phep ghep ma cua nay CO Y ⛔ khong dao.
        "bo_qua": bo_qua,
        # ⭐ Sau khi bo, dong tro lai hang cho — ⛔ khong o nao trong `fls_itl`
        #   doi, phep tinh cua hang cho tu thay.
        "ve_hang_cho": True,
    }


# ── NGUOI BAM "XONG" (`GAP-JOIN-06`, `QĐ-ITL-71`) ────────────────────────
#
# ★★ **Owner chot 28/08: NGUOI bam xong**, ⛔ khong phai may tu nha khi thay du
# 5 truong. Can cu la mot cau hoi NGHIEP VU: may tu nha thi ke toan **mat cho
# danh dau viec dang lam do**; nguoi bam thi hang cho dai hon nhung **dung y
# nguoi**.
#
# ⛔⛔ **Lo no dong.** `fls_itl.work_status` bi **dong bang luc nap**, va moi cua
# ghi deu ⛔ khong dung vao `fls_itl` (dung `INV-I08`) ⇒ truoc quyet dinh nay,
# mot dong da chua xong **VAN nam trong hang cho, mai mai**. Do 28/08: **0 dong
# bi mac** *(vong ghi chua tung chay tren so that)* ⇒ **co che thieu, chua phai
# thiet hai** — nhung no hien ra **ngay dau tien** ke toan dung man hinh.
#
# ⇒ ⛔ KHONG mot o nao cua `fls_itl` doi: *"da xong chua"* la mot **PHEP TINH**
#   tren `fls_queue_event` (khung xem `fls_da_xong`, migration `0014`).
#
# ⚠ **Hai cho CO Y de mo, ⛔ khong chan:**
#   ⓐ **Bam xong khi CON THIEU truong** — co the la mot khoan phi bank that su
#     ⛔ khong can 5 truong. ⇒ cho, nhung **ly do BAT BUOC** va so dong nhu the
#     duoc **dem rieng** (`doc_bao_cao.dem_xong_du_thieu`), ⛔ khong lot im lang.
#   ⓑ **Bam xong trong ky DA CHOT** — ⛔ khac moi cua ghi khac, cua nay CHO.
#     Ly do: ky da chot thi ke toan ⛔ khong sua duoc gia tri nao, nen neu cung
#     ⛔ khong danh dau xong duoc thi nhung dong ay **nam trong hang cho vinh
#     vien ma ⛔ khong ai lam gi duoc** — hang cho tu bien thanh rac. Nhung day
#     la mot ngoai le, nen **ly do BAT BUOC**.
def _thieu_truong(conn, itl_id: int, d: dict[str, Any]) -> list[str]:
    """Truong hop dong con RONG theo gia tri HIEU LUC (nguon hay nguoi go)."""
    with conn.cursor() as cur:
        cur.execute("SELECT field, value_after FROM fls_sua_tay"
                    " WHERE itl_id = %s", (itl_id,))
        tay = {r[0]: r[1] for r in cur.fetchall()}
    thieu = []
    for f in TRUONG_HOP_DONG:
        gt = tay.get(f) if tay.get(f) is not None else d.get(f)
        if gt is None or not str(gt).strip():
            thieu.append(f)
    return thieu


def _da_xong(conn, itl_id: int) -> dict[str, Any] | None:
    with conn.cursor() as cur:
        cur.execute("SELECT evt_id, actor, at, reason FROM fls_da_xong"
                    " WHERE itl_id = %s", (itl_id,))
        r = cur.fetchone()
    return None if r is None else {"evt_id": r[0], "actor": r[1], "at": r[2],
                                   "reason": r[3]}


def danh_dau_xong(conn, pv: PhamVi, itl_id: int, *, actor: str,
                  reason: str | None = None) -> dict[str, Any]:
    """NGUOI bam **xong** ⇒ dong roi hang cho. ⛔ Khong o nao cua so doi.

    ★ **`reason` LUON TUY Y** — owner chot 2026-08-28 (*"ko can ghi ly do"*),
    ⛔ ke ca khi dong con thieu truong hay ky da chot. Ly do cua owner vung hon
    ly do cua toi: **mot cai o ly do bi bat buoc thi no thanh mot cai o RAC**
    (nguoi ta go mot chu roi bam), va mot cot ly do toan chu "x" te hon mot cot
    ly do TRONG — vi cot trong con **thanh that**.

    ⇒ Cai giu lai: `actor`/`at` van vao `fls_queue_event`, va **phep DEM**
      `doc_bao_cao.dem_xong_du_thieu` van dem tung dong bam-xong-du-con-thieu.
      Ham nay cung tra `thieu_truong` + `ghi_de_ket_luan_may` de man hinh hien.
    """
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor` — nhat ky khong biet ai bam thi vo nghia")
    d = _dong_trong_pham_vi(conn, pv, itl_id)

    cu = _da_xong(conn, itl_id)
    if cu is not None:
        # ⛔ Bam hai lan ⛔ khong duoc thanh hai su kien — nhung ⛔ khong im lang:
        # tra ve NGUOI da bam va LUC NAO, de man hinh noi duoc.
        return {"itl_id": itl_id, "da_co": True, "evt_id": cu["evt_id"],
                "boi": cu["actor"], "luc": cu["at"], "ly_do_cu": cu["reason"],
                "thieu_truong": _thieu_truong(conn, itl_id, d),
                "ky_da_chot": (d.get("period_state") or "").strip() == "locked"}

    thieu = _thieu_truong(conn, itl_id, d)
    chot = (d.get("period_state") or "").strip() == "locked"

    # ⛔⛔ **KHONG doi ly do — owner chot 2026-08-28, nguyen van: *"ko can ghi ly
    # do"*.** Ban dau toi bat ly do khi con thieu truong hay ky da chot, lap
    # luan la *"luc do nguoi dang ghi de ket luan cua may"* (`INV-I16`). Owner
    # bo hang rao ay.
    #
    # ★ Va lap luan cua owner vung hon lap luan cua toi: **mot cai o ly do bi
    #   bat buoc thi no thanh mot cai o RAC** — nguoi ta go mot chu roi bam, va
    #   tu do khong ai doc cot ay nua. Mot cot ly do toan chu "x" thi te hon mot
    #   cot ly do TRONG, vi cot trong con **thanh that**.
    #
    # ⇒ Cai thay the ⛔ khong phai "khong con gi": vet van du (`actor`/`at` trong
    #   `fls_queue_event`), va **phep DEM** `doc_bao_cao.dem_xong_du_thieu` van
    #   dem tung dong bam-xong-du-con-thieu. Tuc thay doi o day la **bo mot cai
    #   ma sat**, ⛔ khong phai bo mot lop kiem soat.
    evt = _them_su_kien(conn, itl_id=itl_id, evt_type="done", actor=actor,
                        reason=(reason or "").strip() or None)
    return {"itl_id": itl_id, "da_co": False, "evt_id": evt,
            # ⛔ Khai ra: dong nay xong ma VAN thieu truong. Man hinh phai hien.
            "thieu_truong": thieu, "ky_da_chot": chot,
            "ghi_de_ket_luan_may": bool(thieu or chot)}


def mo_lai(conn, pv: PhamVi, itl_id: int, *, actor: str,
           reason: str) -> dict[str, Any]:
    """Mo lai mot dong da bam xong ⇒ **THEM** su kien `reopen`, ⛔ khong xoa.

    ⛔ Ly do la BAT BUOC o day, ⛔ khac voi `done`: mot dong da duoc mot NGUOI
    ket luan la xong, nen keo no tro lai la **lat ket luan cua nguoi khac**.
    """
    if not (reason or "").strip():
        raise ThieuLyDo(
            "⛔ mo lai phai noi vi sao: dong nay da co NGUOI ket luan la xong, "
            "keo no tro lai la lat ket luan cua nguoi khac")
    if not (actor or "").strip():
        raise LoiGhi("⛔ thieu `actor`")
    _dong_trong_pham_vi(conn, pv, itl_id)
    cu = _da_xong(conn, itl_id)
    if cu is None:
        raise ChuaXong(
            f"itl_id={itl_id} ⛔ chua tung duoc bam xong — ⛔ khong co gi de mo "
            f"lai. Dong nay dang o hang cho (hay ⛔ khong thuoc hang cho)")
    evt = _them_su_kien(conn, itl_id=itl_id, evt_type="reopen", actor=actor,
                        reason=reason)
    return {"itl_id": itl_id, "evt_id": evt, "mo_lai_cua": cu["evt_id"],
            "xong_boi": cu["actor"], "xong_luc": cu["at"]}


def dem_hoan(conn, itl_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(defer_count, 0) FROM fls_queue_state"
                    " WHERE itl_id = %s", (itl_id,))
        r = cur.fetchone()
    return 0 if r is None else int(r[0])
