"""Cac cau DOC cho cua `P4`. ⛔ Chi doc — khong ham nao o day ghi mot o nao.

★ **Moi ham nhan `PhamVi` lam doi so DAU, khong mac dinh.** Xem `pham_vi.py`:
1.204 dong dau test tung lan vao so that va 194 dong trong so do ngay trong
hang cho. Cho hong khong phai "loc sai" ma la "khong gi bat buoc phai loc".

⛔⛔ **Vi sao phep xep hang cho nam o DAY chu khong con o khung xem
`fls_queue_xep_tien`** (khung xem do dung 27/08, bo 27/08 — migration `0009`):

Khung xem SQL ⛔ khong nhan tham so. Nen no chi co hai duong, va **ca hai deu
sai**:

  ⓐ Khong loc gi (ban dung 27/08) → `hang` va `luy_ke_pct` duoc tinh **truoc**
    khi ai kip loc. Loc o dau ra ⛔ **khong sua duoc thu tu da xep sai**: 194
    dong dau test mang **1.285.475.949** tien bia se day % luy ke cua moi dong
    that lech di, ma ban thanh chung khong con trong danh sach ⇒ **con so sai
    ma khong con dau vet giai thich vi sao**. Day dung la loai sai im lang ca
    he nay dung ra de chan.
  ⓑ Nhet ban trang `NAP-yyyy-mm-dd-NGUON` vao trong khung xem → kho TEST khong
    duoc phep dung `run_id` hinh do (neu dung thi cong `kiem_kho` **mu**: mot
    lan test ghi lan vao so that se trong nhu lan nap that) ⇒ khung xem tra
    **rong** trong moi bai test ⇒ phep xep khong con bai nao do duoc.

⇒ Pham vi phai la **tham so**, nen phep xep phai nam trong mot **cau co tham
so**. Doi lai duoc mot thu khung xem ⛔ khong bao gio kiem duoc: bai
`test_dong_cua_run_LA_khong_lam_lech_luy_ke` — voi khung xem, bai do **khong
viet duoc**.

★ Luat `PARTITION BY curr` giu nguyen (`QĐ-ITL-58`): xep va luy ke **trong tung
tien te**. Gop hai tien te lai la con so trong hinh ma vo nghia — hang cho co
USD 4.492 dong vs VND 2.987, gop lai thi toan bo dong USD bi dim xuong duoi.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from fls.adapters.mapping_master import TRUONG as TRUONG_MM
from fls.adapters.pm_join import canon_ref, dung_sai_ghep_tay
# ⭐ Luat suy vung PHAN BO. ⛔ Mot BAN DUY NHAT, va no o `fls/ledger/` — tang
# doc chi **goi** no. ⛔ Man hinh ⛔ KHONG duoc tu tinh lai: `suy_allocate` co
# hai bay ngu nghia cua Sheets *(o `Method` rong that ⇒ `VLOOKUP` cho **`0`**;
# `#N/A` la "khong tra duoc" chu ⛔ khong phai rong)* va mot ban thu hai bang
# JS se lech o dung hai cho ay.
from fls.canon.spec import CANON_COLS
from fls.ledger.allocate import suy_allocate
# ⚠ Chi lay HANG SO (`TRUONG_HOP_DONG`), ⛔ khong ham ghi nao — luat
# ranh gioi cua `import-linter`: tang doc ⛔ khong duoc goi tang ghi.
from fls.repo.ghi_tay import TRUONG_HOP_DONG
from fls.repo.pham_vi import PhamVi

# `BA-07` §1: trang mac dinh 50, ⛔ toi da 500 — luoi ke toan can trang to hon
# cockpit, nhung mot cau khong gioi han la mot cau co the keo ca so ra.
TRANG_MAC_DINH = 50
TRANG_TOI_DA = 500

# 14 truong hop dong + danh tinh + lineage.
#
# ⛔⛔ **Ban truoc bo `canon` khoi danh sach voi ly do: *"36 cot jsonb × 500
# dong la mot cau tra ve **vai MB** ma man hinh khong dung"*. Con so ay
# ⛔ CHUA AI DO.** Do that 2026-09-03 tren 10.030 dong: `length(canon::text)`
# trung binh **393 byte**, lon nhat **1.970** ⇒ 500 dong ~ **192 KB**, ⛔ khong
# phai vai MB — **sai 10–20 lan**. Va ve *"man hinh khong dung"* thi owner tra
# loi thang ngay 03/09: *"bang So ITL can du cac truong thong tin"*.
#
# ⇒ `canon` **vao danh sach**, va man bung 27 vi tri chua co cot ra luoi
#   (`fls/api/cot_so.CANON_LEN_LUOI`). ⭐ Bai hoc lap lai lan thu ba trong du
#   an nay: mot con so uoc luong nam trong mot chu thich thi **⛔ khong ai do
#   lai**, va no cat mot tinh nang trong im lang.
_COT_SO = (
    "i.itl_id", "i.doc_date", "i.doc_no", "i.memo", "i.curr",
    "i.ps_no", "i.ps_co", "i.acct", "i.le", "i.le_payer",
    "i.hd", "i.pay_type", "i.cdt1", "i.svc_start", "i.svc_end",
    "i.work_status", "i.pm_hinh", "i.is_flash", "i.period_state",
    "i.run_id", "i.source_system", "i.source_sheet", "i.source_row",
    "i.canon",
)


# ⭐⭐ Nam truong `doc_so`/`doc_mot_dong` THEM vao ngoai `_COT_SO` — vung
# PHAN BO suy tu `cdt1` + `hd` + `Mapping Master` *(`QĐ-ITL-70`)*.
#
# ⛔⛔ **Vi sao khai ra thanh mot HANG SO chu ⛔ khong de no an trong ham.**
# Cong `fls/api/cot_so.kiem_bang_cot` doi chieu **hai chieu** giua bang cot cua
# luoi va tap truong cua tra. Neu tap ay phai go tay o cong thi cong dang canh
# mot tam ban do, ⛔ khong canh cua — dung lop hong cua `GAP-API-05`.
TRUONG_ALLOC: tuple[str, ...] = (
    "alloc_cfa1", "alloc_cfa2", "alloc_method", "alloc_can_phan_bo",
    "alloc_na")


def bang_mapping_master(conn) -> dict[str, dict[str, Any]]:
    """Ca danh muc `Mapping Master` thanh mot tra bang, khoa **ha chu**.

    ⛔⛔ **Vi sao doc ca bang chu ⛔ khong `LEFT JOIN` trong cau lay dong so.**
    Khoa `hd_code` la PK **phan biet hoa thuong**, con phep tra cua Sheets thi
    **⛔ khong** *(`VLOOKUP`)*. Nen mot ngay nao do danh muc co ca `NB` va `nb`
    thi mot phep `JOIN` tren `lower()` se **nhan doi dong so** — im lang, va
    `count` cua trang van "dung" vi no dem dong da nhan doi. ⇒ Doc thanh mot
    tra bang: 73 dong, mot cau, va **hai dong cung khoa thi NO ngay**.

    ⚠ NO chu ⛔ khong lay dong dau nhu `VLOOKUP`: lay dong dau la **may tu
    chon** giua hai cau tra loi *(`INV-I16`)*, va o cot phan bo thi hai cau tra
    loi ay ⛔ khong nhat thiet giong nhau.
    """
    with conn.cursor() as cur:
        cur.execute(f"SELECT {', '.join(TRUONG_MM)} FROM fls_mapping_master")
        dong = [dict(zip(TRUONG_MM, r)) for r in cur.fetchall()]
    bang: dict[str, dict[str, Any]] = {}
    for d in dong:
        k = str(d["hd_code"] or "").strip().lower()
        if k in bang:
            raise ValueError(
                f"⛔ `fls_mapping_master` co HAI dong cung ma {k!r} khi bo qua "
                f"hoa/thuong ({bang[k]['hd_code']!r} va {d['hd_code']!r}). "
                f"Phep tra cua Sheets ⛔ khong phan biet hoa thuong, nen may "
                f"⛔ khong biet dong nao la dong dung. Sua danh muc roi chay "
                f"lai `tools/nap_mapping_master.py --ghi`")
        bang[k] = d
    return bang


def _gan_alloc(dong: list[dict[str, Any]],
               mm: dict[str, dict[str, Any]]) -> None:
    """Gan **nam** truong `alloc_*` vao tung dong. Sua TAI CHO."""
    for d in dong:
        hd = d.get("hd")
        k = str(hd or "").strip().lower()
        v = suy_allocate(d.get("cdt1"), hd, mm.get(k))
        d["alloc_cfa1"] = v.cfa1
        d["alloc_cfa2"] = v.cfa2
        d["alloc_method"] = v.method
        d["alloc_can_phan_bo"] = v.can_phan_bo
        # ⛔ `#N/A` la mot CAU TRA LOI *("dong nay ⛔ khong tra duoc `hd`")*,
        # ⛔ khong phai mot loi. Man hinh phai hien dung `#N/A`, ⛔ khong chua
        # cho dep thanh rong — hai chuyen khac nhau (`INV-I16`).
        d["alloc_na"] = v.khong_tra_duoc


# ⭐ 27 vi tri canon di ra luoi. ⛔ Bang chu cai nay la BAN SAO cua
#   `fls/api/cot_so.CANON_LEN_LUOI` — tang kho ⛔ khong duoc import tang cua
#   *(`import-linter` luat 7 di nguoc lai, va mot vong import la mot vong)*.
#   ⇒ Co mot phep thu giu hai ban khong lech; hai ban ma ⛔ khong ai canh thi
#   mot ngay nao do luoi se **thieu mot cot ma trong nhu du**.
CANON_RA_LUOI: tuple[str, ...] = (
    "H", "I", "J", "K", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "AB", "AC", "AD", "AE", "AF", "AH", "AI", "AJ", "AK", "AL",
)
_VI_TRI = {c.letter: c.pos for c in CANON_COLS}


def _gan_canon(dong: list[dict[str, Any]]) -> None:
    """Bung mang `canon` thanh `canon_<chu cai>` roi **bo mang goc**.

    ⭐ Bung o tang kho chu ⛔ khong de man tu cat: cong `kiem_bang_cot` doi
    **moi truong cua tra** phai co mot cot khai san — mot **mang** thi cong ay
    ⛔ khong soi duoc, va 27 cot se di ra man **ngoai tam kiem**.

    ⛔ Bo mang goc di vi neu giu ca hai thi moi dong chay **hai ban** cung mot
    du lieu — dung cai lang phi ma phep do 393 byte/dong vua can nhac.
    """
    for d in dong:
        v = d.pop("canon", None) or []
        for x in CANON_RA_LUOI:
            i = _VI_TRI[x]
            o = v[i] if i < len(v) else None
            # ⛔ `None` giu nguyen `None`: *"o trong"* va *"⛔ khong co o"* la
            # hai chuyen, va man se hien chung khac nhau (`INV-I16`).
            d["canon_" + x] = None if o is None or o == "" else str(o)


def _trang(limit: int | None) -> int:
    """Chan tren CUNG. ⛔ Khong tin con so tu ngoai gui vao."""
    if limit is None:
        return TRANG_MAC_DINH
    n = int(limit)
    if n < 1:
        raise ValueError(f"limit={n} phai >= 1")
    return min(n, TRANG_TOI_DA)


def _dong(cur) -> list[dict[str, Any]]:
    ten = [d.name for d in cur.description]
    return [dict(zip(ten, r)) for r in cur.fetchall()]


@dataclass(frozen=True)
class Trang:
    """Mot trang ket qua + con tro trang sau. `con_tro=None` la het."""

    dong: list[dict[str, Any]]
    con_tro: str | None
    pham_vi: str


# ── so ITL ────────────────────────────────────────────────────────────────
def doc_so(conn, pv: PhamVi, *, period: str | None = None,
           le: str | None = None, status: str | None = None,
           con_tro: str | None = None, limit: int | None = None) -> Trang:
    """Dong `fls_itl` theo pham vi. Phan trang KHOA (keyset) tren `itl_id`.

    ⚠ Phan trang bang `OFFSET` se **bo sot hoac lap dong** khi co lan nap moi
    chen vao giua luc nguoi dang lat trang. `itl_id` la SEQUENCE dong bang
    (`INV-I04a`) nen khoa tren no la thu tu ben.
    """
    n = _trang(limit)
    dk, ts = pv.dieu_kien("i.run_id")
    dieu = [dk]
    if period:
        dieu.append("to_char(i.doc_date, 'YYYY-MM') = %s")
        ts.append(period)
    if le:
        dieu.append("i.le = %s")
        ts.append(le)
    if status:
        dieu.append("i.work_status = %s")
        ts.append(status)
    if con_tro:
        dieu.append("i.itl_id > %s")
        ts.append(int(con_tro))
    sql = (f"SELECT {', '.join(_COT_SO)} FROM fls_itl i WHERE "
           + " AND ".join(dieu) + " ORDER BY i.itl_id LIMIT %s")
    with conn.cursor() as cur:
        cur.execute(sql, [*ts, n + 1])
        dong = _dong(cur)
    con = str(dong[n - 1]["itl_id"]) if len(dong) > n else None
    ra = dong[:n]
    # ⭐ Vung PHAN BO — mot cau cho ca trang, ⛔ khong mot cau moi dong.
    _gan_alloc(ra, bang_mapping_master(conn))
    # ⭐ 27 vi tri canon ra luoi (owner chot 03/09) — xem `_gan_canon`.
    _gan_canon(ra)
    return Trang(dong=ra, con_tro=con, pham_vi=pv.mo_ta())


# ★★ UNG VIEN GHEP LENH — them 2026-08-27, dong `GAP-API-04` duong (a).
#
# ⛔⛔ **Bon BAC CO TEN, ⛔ khong phai mot diem so mo.** Man `F01` can noi duoc
# *"vi sao phieu nay dung dau danh sach"*, va mot con so 0..1 thi ⛔ khong tra loi
# duoc cau do. Nen moi ung vien mang mot **bac** doc len thanh cau:
#
#   `ma`            ma tham chieu KHOP     -> chip xanh, day la ca gan chac
#   `tien`          cung tien te + tien BANG DUNG
#   `gan_tien`      cung tien te + lech <= dung sai cua tien te do
#   `cung_tien_te`  chi cung tien te       -> danh sach de nguoi tu doc
#
# ⛔⛔ **Va day la cho phai noi thang mot GIOI HAN, ⛔ khong de nguoi doc tu suy:**
# `BA-07` §2 mong xep theo *"reference / tien / **ngay** / **payee**"*. Hai truc
# sau ⛔ **KHONG do duoc**: anh chup `fls_pm_line` co y ⛔ khong mang PII (Ten tai
# khoan, So tai khoan) va ⛔ khong mang ngay. ⇒ chi con **hai** truc that. Muon co
# `ngay`/`payee` thi phai **mo pham vi doc nguon** — quyet dinh cua chu so, ⛔
# khong phai cua code (`GAP-JOIN-04`).
#
# ⛔ Dong `Reject` / `status` RONG **VAN hien**, kem `canh_bao`. An chung di la
# **mac dinh im lang** (`INV-I16`): nguoi go se khong hieu vi sao phieu minh biet
# la co thi khong thay trong danh sach.
BAC_UNG_VIEN: tuple[str, ...] = ("ma", "tien", "gan_tien", "cung_tien_te")
UNG_VIEN_MAC_DINH = 20
UNG_VIEN_TOI_DA = 200

_COT_UV = ("l.pm_line_id", "l.pm_slip_id", "l.ref_tho", "l.ref_canon",
           "l.amount", "l.curr", "l.status", "l.hd", "l.cdt1", "l.source_row")


def _canh_bao(status: str | None) -> str:
    """⛔ RONG la KHONG BIET, ⛔ khong phai 'da duyet' (`INV-I16`)."""
    s = (status or "").strip()
    if not s:
        return "status RONG — nguon KHONG NOI da duyet hay chua"
    if s.lower() != "approve":
        return f"status = {s!r} — ⛔ KHONG phai 'Approve'"
    return ""


# ⚠ Ep KIEU cho moi tham so (`::text`, `::numeric`): khong ep thi PostgreSQL
# ⛔ khong suy duoc kieu cua `%(ma)s IS NOT NULL` va NO ngay lan chay dau
# (`IndeterminateDatatype`) — da mac 27/08.
#
# ⚠ Bac tinh MOT LAN trong `q`, roi moi xep o ngoai. Viet lai ca khoi `CASE` lan
# thu hai trong `ORDER BY` la **hai cho khai cung mot luat** — chung se lech.
_SQL_UNG_VIEN = """
WITH s AS (
  SELECT %(ma)s::text AS ma, %(cur)s::text AS cur,
         %(tien)s::numeric AS tien, %(ds)s::numeric AS ds
), q AS (
  SELECT {cot},
         -- ⚠ `fls_moi_noi`, ⛔ KHONG `fls_pm_link`: bang goc giu ca cac moi
         -- noi DA BO (migration `0013`), nen dem tren bang goc se hien mot
         -- dong lenh vua duoc go la **da ghep** va ke toan ⛔ khong ghep lai
         -- duoc — mot cau tra loi sai ma ⛔ khong bao loi.
         (SELECT count(*) FROM fls_moi_noi k
           WHERE k.pm_line_id = l.pm_line_id) AS da_ghep,
         CASE
           WHEN s.ma IS NOT NULL AND l.ref_canon = s.ma            THEN 'ma'
           WHEN upper(l.curr) = s.cur AND l.amount = s.tien         THEN 'tien'
           WHEN upper(l.curr) = s.cur
                AND abs(l.amount - s.tien) <= s.ds                 THEN 'gan_tien'
           ELSE 'cung_tien_te' END AS bac,
         abs(COALESCE(l.amount, 0) - s.tien) AS lech_tuyet_doi
  FROM fls_pm_line l CROSS JOIN s
  WHERE l.run_id = %(run)s
    AND ((s.ma IS NOT NULL AND l.ref_canon = s.ma)
         OR upper(l.curr) = s.cur)
)
SELECT * FROM q
ORDER BY array_position(%(bac)s::text[], q.bac), q.lech_tuyet_doi, q.pm_line_id
LIMIT %(n)s"""


def ung_vien_pm(conn, pv: PhamVi, itl_id: int, n: int = UNG_VIEN_MAC_DINH
                ) -> dict[str, Any] | None:
    """Dong lenh chi ung vien cho MOT dong so. `None` neu dong ngoai pham vi.

    ★ Tra ve **ca TUOI cua anh chup** (`anh_chup`). Cau tra loi cho *"ban luu gia
    di thi sao"* ⛔ khong phai *"no khong gia"* — ma la **noi ra no gia bao nhieu**,
    de nguoi go tu quyet. Man hinh PHAI hien con so nay.

    ⛔ Anh chup lay theo **lan nap CUA CHINH DONG SO do** (`i.run_id`), ⛔ khong
    phai "anh chup moi nhat": mot dong so cua lan nap thang truoc phai duoc ghep
    voi dong lenh **nhu no da la luc do**, khong thi lineage `INV-I05` dut.
    """
    n = max(1, min(int(n), UNG_VIEN_TOI_DA))
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT i.itl_id, i.run_id, i.doc_no, i.curr, i.work_status,"
            " COALESCE(i.ps_no,0) + COALESCE(i.ps_co,0) AS tien"
            f" FROM fls_itl i WHERE i.itl_id = %s AND {dk}", [itl_id, *ts])
        d = _dong(cur)
        if not d:
            return None
        so = d[0]

        cur.execute(
            "SELECT count(*), min(read_at), max(read_at)"
            " FROM fls_pm_line WHERE run_id = %s", (so["run_id"],))
        sl, som, muon = cur.fetchone()

        # ⚠ Ma tham chieu duoc chuan hoa BEN PYTHON roi moi so — ⛔ khong viet lai
        # `canon_ref` bang SQL: hai ban chuan hoa la hai ban su that, va ban SQL
        # se lech dan trong im lang.
        ma = canon_ref(so["doc_no"])
        tien = so["tien"]
        cur_so = (so["curr"] or "").strip().upper()
        # ⛔ Phai dung dung sai cua cua GHEP TAY (`QĐ-ITL-63`), ⛔ khong
        # phai cua ghep tu dong: danh sach nay la danh sach cho NGUOI ghep tay.
        # Neu o day noi `1.000` ma cua chi cho `0,5%` thi man hinh xep mot ung
        # vien vao bac "gan tien" roi cua **tu choi** no — mot cai bay.
        ds = (dung_sai_ghep_tay({cur_so}, Decimal(str(so["tien"] or 0)))
              if cur_so else Decimal(0))

        cur.execute(_SQL_UNG_VIEN.format(cot=", ".join(_COT_UV)),
                    {"ma": ma, "cur": cur_so, "tien": tien, "ds": ds,
                     "run": so["run_id"], "bac": list(BAC_UNG_VIEN), "n": n})
        uv = _dong(cur)

    for x in uv:
        x["canh_bao"] = _canh_bao(x.get("status"))
        x["lech_tien"] = (None if x["amount"] is None
                          else x["amount"] - Decimal(str(tien or 0)))
    return {
        "dong_so": so,
        "ma_da_chuan_hoa": ma,
        "dung_sai": ds,
        "ung_vien": uv,
        # ★ Luat ⓑ: TUOI cua anh chup di kem moi danh sach.
        "anh_chup": {"run_id": so["run_id"], "so_dong": int(sl or 0),
                     "doc_luc_som_nhat": som, "doc_luc_muon_nhat": muon},
        # ⛔ Khai thang thu KHONG do duoc, ⛔ khong de man hinh tu suy.
        "khong_xep_duoc_theo": ["ngay", "payee"],
        "vi_sao": ("anh chup ⛔ khong mang PII va ⛔ khong mang ngay "
                   "(`GAP-JOIN-04`) — muon hai truc do phai mo pham vi doc nguon"),
        "pham_vi": pv.mo_ta(),
    }


def doc_mot_dong(conn, pv: PhamVi, itl_id: int) -> dict[str, Any] | None:
    """Mot dong + 36 cot `canon` + moi noi lenh chi. `None` neu ngoai pham vi.

    ⛔ `None` cho ca hai truong hop *"khong co dong nay"* va *"co nhung ngoai
    pham vi"* — co y: cua doc ⛔ khong duoc de nguoi ngoai pham vi biet dong do
    ton tai.
    """
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT {', '.join(_COT_SO)}, i.canon, i.hd_thyt, i.pay_type_thyt,"
            " i.cdt1_thyt, i.svc_start_thyt, i.svc_end_thyt, i.id_payee,"
            " i.invoice, i.itl_id_sheet, i.content_key, i.created_at,"
            " i.contract_version, i.canon_version, i.mapping_version"
            f" FROM fls_itl i WHERE i.itl_id = %s AND {dk}",
            [itl_id, *ts])
        d = _dong(cur)
        if not d:
            return None
        ra = d[0]
        _gan_alloc([ra], bang_mapping_master(conn))
        # ⚠ Khung xem hieu luc — ⛔ khong phai `fls_pm_link` (co ca moi noi da bo).
        cur.execute(
            "SELECT link_id, pm_line_id, amount, hinh, lan FROM fls_moi_noi"
            " WHERE itl_id = %s ORDER BY pm_line_id", (itl_id,))
        ra["moi_noi"] = _dong(cur)
        # ⭐ Lich su BO moi noi — man hinh phai noi duoc *"dong nay da ghep lai
        #   2 lan"*, ⛔ khong de mot lan go bien mat khong dau vet.
        cur.execute(
            "SELECT u.unlink_id, u.link_id, l.pm_line_id, l.lan, u.at,"
            " e.actor, e.reason"
            "  FROM fls_pm_unlink u"
            "  JOIN fls_pm_link l ON l.link_id = u.link_id"
            "  JOIN fls_queue_event e ON e.evt_id = u.evt_id"
            " WHERE u.itl_id = %s ORDER BY u.unlink_id", (itl_id,))
        ra["moi_noi_da_bo"] = _dong(cur)
        # ⭐ Gia tri NGUOI GO dang co hieu luc. ⛔ KHONG tron vao cac cot nguon
        # o tren: man hinh phai noi duoc *"nguon noi X, nguoi go Y"*, va tron
        # hai thu do lai la lam mat dung cai phan biet ay (`QĐ-ITL-35`).
        cur.execute(
            "SELECT field, value_after, adj_id, actor, at FROM fls_sua_tay"
            " WHERE itl_id = %s ORDER BY field", (itl_id,))
        ra["sua_tay"] = {d["field"]: d for d in _dong(cur)}
        # ⭐ `QĐ-ITL-71`: dong nay da co NGUOI bam xong chua. ⛔ Phai hien,
        # ⛔ khong an: mot dong "xong" ma man hinh ⛔ khong noi ai bam va luc
        # nao thi nut do la mot cai nut khong ai chiu trach nhiem.
        cur.execute(
            "SELECT evt_id, actor, at, reason FROM fls_da_xong"
            " WHERE itl_id = %s", (itl_id,))
        x = _dong(cur)
        ra["da_xong"] = x[0] if x else None
        # Ca lich su but toan (ke ca ban dao) — de drawer dao dung but toan nao.
        cur.execute(
            "SELECT adj_id, field, value_after, state, reversal_of, actor, at"
            " FROM fls_adjustment WHERE itl_id = %s ORDER BY adj_id", (itl_id,))
        ra["but_toan"] = _dong(cur)
    return ra


# ── hang cho, xep theo TIEN ───────────────────────────────────────────────
# ⛔⛔ Pham vi nam TRONG cau con `q`, tuc la TRUOC khi xep hang. Doi cho no ra
# ngoai (loc o dau ra) la loi ⓐ trong docstring dau file: thu tu da xep sai roi.
# ⭐⭐ Khoi `WITH` nay dung CHUNG cho hai cau: danh sach hang cho, va phep do DO
# PHU (`/queue/coverage`). ⛔⛔ Chep no ra lam ban thu hai la khai **cung mot
# luat hang cho o hai cho** — va chinh chu thich ben trong day da canh dieu do
# mot lan roi *(dieu kien `fls_da_xong` phai giong `dem_hang_cho`)*. Hai ban se
# lech, va luc do man hinh se noi *"con N dong"* tren mot danh sach do dai khac.
_CTE_HANG_CHO = """
WITH q AS (
  SELECT i.itl_id, i.doc_date, i.doc_no, i.curr, i.le, i.memo,
         COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien
  FROM fls_itl i
  WHERE i.work_status = 'UNMAPPED' AND {dk}
    -- ⭐⭐ `QĐ-ITL-71`: NGUOI bam xong moi roi hang cho. `work_status` bi DONG
    -- BANG luc nap va ⛔ khong gi tinh lai no (moi cua ghi deu ⛔ khong dung
    -- vao `fls_itl` — `INV-I08`), nen ⛔ khong co dieu kien nay thi mot dong
    -- da chua xong **nam trong hang cho MAI MAI** (`GAP-JOIN-06`).
    -- ⛔⛔ Va no PHAI nam TRONG cau con `q`: hang cho xep theo phan tram luy
    -- ke tien, nen loc o dau ra se de nhung dong da xong **day phan tram cua
    -- moi dong con lai** — cung lop loi voi `CR#4`.
    -- ⚠ Va ⛔ dung viet dau phan tram trong chu thich SQL: psycopg doc no thanh
    --   mot cho dien tham so va NO ngay ("incomplete placeholder") — da mac 28/08.
    AND NOT EXISTS (SELECT 1 FROM fls_da_xong x WHERE x.itl_id = i.itl_id)
), x AS (
  SELECT q.*,
         row_number() OVER w AS hang,
         round(100.0 * SUM(q.tien) OVER (PARTITION BY q.curr
                                         ORDER BY q.tien DESC, q.itl_id
                                         ROWS UNBOUNDED PRECEDING)
               / NULLIF(SUM(q.tien) OVER (PARTITION BY q.curr), 0), 2)
           AS luy_ke_pct
  FROM q
  WINDOW w AS (PARTITION BY q.curr ORDER BY q.tien DESC, q.itl_id)
)
"""

_SQL_HANG_CHO = _CTE_HANG_CHO + """
SELECT x.itl_id, x.doc_date, x.doc_no, x.curr, x.le, x.memo, x.tien,
       x.hang, x.luy_ke_pct,
       s.reason, s.defer_until, s.defer_count
FROM x LEFT JOIN fls_queue_state s ON s.itl_id = x.itl_id
WHERE TRUE {them}
ORDER BY x.curr, x.hang
LIMIT %s
"""

# ⭐⭐ DO PHU — *"xem toi day la phu bao nhieu phan tram TIEN"*.
#
# ⛔⛔ **Vi sao con so nay phai tinh TRONG KHO, ⛔ khong dem o man hinh.** Cach
# dang dung *(`tools/verify_cua_that.py`)* la keo `/queue?den_pct=90&limit=500`
# roi **dem so dong tra ve**. Chan tren cua mot trang la **500**
# (`TRANG_TOI_DA`), nen ngay nao do phu 90% can **hon 500 dong** thi con so ay
# **im lang dung o 500** — no ⛔ khong bao loi, ⛔ khong bao thieu, no chi nho
# di. Hom nay USD can **444** dong: con cach **56 dong** la sai.
# ⇒ Dem bang `count(*)` trong SQL. ⛔ Khong co chan tren nao de cham vao.
# ⛔⛔ **VA mot cau hoi ngu nghia ma bo test lat ra, ⛔ khong phai mot chi tiet
# ky thuat.** *"Xem toi day phu 90 phan tram tien"* co HAI cach doc, va chung
# lech **dung mot dong**:
#   ⓐ so dong co luy ke **<= 90**  — khop danh sach `?den_pct=90` dang co
#   ⓑ so dong **NHO NHAT de luy ke DAT hay VUOT 90** — cau tra loi that cho
#     cau hoi *"toi phai xem bao nhieu dong thi da nhin qua 90 phan tram tien"*
# Vi du do duoc: 9 dong bang nhau ⇒ ⓐ tra **8** *(luy ke 88,89)*, ⓑ tra **9**.
# ⇒ Chon ⓑ, vi ⓐ **NOI QUA**: nhan ghi *"phu 90"* trong khi that ra moi 88,89.
# ⚠ Va tra ra luon `pct_that` — phan tram THAT tai dong ay — de cai nhan ⛔
#   khong the noi doi du chon cach nao: man hinh in *"9 dong ⇒ 100,00 phan tram"*.
#
# ⭐⭐ `so_dong_phu` co the la **NULL**: khi ca hang cho cua mot tien te co Σ
# tien = 0 thi *"phu bao nhieu phan tram tien"* ⛔ khong co nghia. NULL o day la
# **"⛔ khong do duoc"**, va man hinh PHAI ve no khac 0 — dung luat so mot cua
# du an. ⛔ Tra 0 la noi rang *"xem 0 dong la du"*.
_SQL_DO_PHU = _CTE_HANG_CHO + """
, tong AS (SELECT count(*)::int AS n FROM x)
SELECT x.curr,
       count(*)::int  AS so_dong_cho,
       SUM(x.tien)    AS tien_cho,
       min(x.hang) FILTER (WHERE x.luy_ke_pct >= %s)::int  AS so_dong_phu,
       min(x.luy_ke_pct) FILTER (WHERE x.luy_ke_pct >= %s)  AS pct_that,
       count(*) FILTER (WHERE x.luy_ke_pct <= %s)::int
                      AS so_dong_trong_danh_sach,
       round(100.0 * count(*) / NULLIF((SELECT n FROM tong), 0), 1)
                      AS pct_dong
FROM x
GROUP BY x.curr
ORDER BY 2 DESC
"""


def doc_hang_cho(conn, pv: PhamVi, *, curr: str | None = None,
                 den_pct: Decimal | float | None = None,
                 con_tro: str | None = None, limit: int | None = None) -> Trang:
    """Hang cho `UNMAPPED`, xep theo tien GIAM **trong tung tien te**.

    `den_pct` = *"chi lay den khi phu bao nhieu % tien"* — cach mot man hinh noi
    duoc *"xem toi day la phu 90% tien"* ⛔ ma khong can mot quy dinh nao ve
    khoan nao can lenh chi (`QĐ-ITL-56`: khong co quy dinh do).

    Con tro phan trang la `"<tien te>:<hang>"` — khoa doi, vi thu tu la
    (tien te, hang).
    """
    n = _trang(limit)
    dk, ts = pv.dieu_kien("i.run_id")
    them: list[str] = []
    if curr:
        them.append("AND x.curr = %s")
        ts.append(curr)
    if den_pct is not None:
        them.append("AND x.luy_ke_pct <= %s")
        ts.append(Decimal(str(den_pct)))
    if con_tro:
        c, h = con_tro.split(":", 1)
        them.append("AND (x.curr, x.hang) > (%s, %s)")
        ts += [c, int(h)]
    sql = _SQL_HANG_CHO.format(dk=dk, them=" ".join(them))
    with conn.cursor() as cur:
        cur.execute(sql, [*ts, n + 1])
        dong = _dong(cur)
    con = (f"{dong[n - 1]['curr']}:{dong[n - 1]['hang']}"
           if len(dong) > n else None)
    return Trang(dong=dong[:n], con_tro=con, pham_vi=pv.mo_ta())


def do_phu_hang_cho(conn, pv: PhamVi,
                    muc_pct: Decimal | float = 90) -> list[dict[str, Any]]:
    """*"Xem den dong thu may thi da nhin qua `muc_pct` phan tram TIEN"* —
    **theo tung tien te**, ⛔ khong co dong "tong".

    Moi dong tra ve:
      `so_dong_cho` · `tien_cho` — quy mo hang cho cua tien te do
      `so_dong_phu` — ⭐ so dong **nho nhat** de luy ke **dat hay vuot**
                      `muc_pct`. Co the **NULL** = ⛔ **khong do duoc**
                      (Σ tien = 0 ⇒ cau hoi ⛔ khong co nghia)
      `pct_that`    — phan tram THAT tai dong ay ⇒ nhan ⛔ khong the noi qua
      `so_dong_trong_danh_sach` — so dong `?den_pct=<muc>` se hien
                      *(luy ke **<=** muc)*. ⚠ Thuong **it hon `so_dong_phu`
                      dung mot dong**, va do ⛔ khong phai loi: hai cau hoi khac
                      nhau. Tra ca hai de man hinh ⛔ khong phai doan
      `pct_dong`    — ty le so DONG cua tien te nay trong ca hang cho

    ⛔ Cong hai don vi tien te ra mot con so la dung cai sai da de ra con so
    *"310 dong phu 90 phan tram tien"* (that ra **799**) — xem `dem_hang_cho`.

    ⚠ `muc_pct` phai nam trong `(0, 100]`. ⛔ `0` bi tu choi chu ⛔ khong tra ve
    0 dong: mot man hinh hoi *"phu 0 phan tram can may dong"* la mot man hinh
    dang hoi nham, va tra `0` cho no thi ⛔ khong ai biet.
    """
    p = Decimal(str(muc_pct))
    if not (Decimal(0) < p <= Decimal(100)):
        raise ValueError(f"muc_pct={p} phai nam trong (0, 100]")
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        # `p` dung BA lan trong cau (dat/vuot · phan tram that · <= muc).
        cur.execute(_SQL_DO_PHU.format(dk=dk), [*ts, p, p, p])
        return _dong(cur)


def dem_xong_du_thieu(conn, pv: PhamVi) -> dict[str, Any]:
    """Dem cac dong **da bam xong MA van thieu truong hop dong** (`QĐ-ITL-71`).

    ⛔⛔ **Vi sao phai co phep dem nay, va vi sao no ⛔ KHONG phai mot cong.**
    Cua `danh_dau_xong` CO Y cho bam xong khi con thieu truong — co the la mot
    khoan phi bank that su ⛔ khong can 5 truong. Nhung mot cai cua "cho" ma
    ⛔ khong ai dem thi som muon thanh **duong tat de lam sach hang cho**: bam
    xong het, hang cho ve 0, va ⛔ khong con dau vet nao noi rang 4.000 dong da
    bi dong ma chua ai tra loi.

    ⇒ Dem, va **dem kem LY DO** *(cua nay bat buoc ly do khi con thieu)*. ⛔ Va
      ⛔ khong dat nguong: bao nhieu la "nhieu qua" thi ⛔ chua ai chot, va bia
      ra mot cai nguong o day la bia ra mot quyet dinh nghiep vu.
    """
    dk, ts = pv.dieu_kien("i.run_id")
    thieu = " OR ".join(
        f"COALESCE(s_{f}.value_after, i.{f}) IS NULL"
        f" OR btrim(COALESCE(s_{f}.value_after, i.{f})) = ''"
        for f in TRUONG_HOP_DONG)
    noi = " ".join(
        f"LEFT JOIN fls_sua_tay s_{f} ON s_{f}.itl_id = i.itl_id"
        f" AND s_{f}.field = '{f}'" for f in TRUONG_HOP_DONG)
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT count(*)::int AS so_dong,"
            f" count(*) FILTER (WHERE x.reason IS NULL)::int AS khong_ly_do"
            f" FROM fls_itl i JOIN fls_da_xong x ON x.itl_id = i.itl_id {noi}"
            f" WHERE {dk} AND ({thieu})", ts)
        d = _dong(cur)[0]
    return {"xong_du_con_thieu": d["so_dong"],
            # ⭐ PHAI la 0: cua ghi bat buoc ly do khi con thieu. Khac 0 nghia
            # la co duong ghi khac di vao `fls_queue_event` — mot lo.
            "khong_ly_do": d["khong_ly_do"], "pham_vi": pv.mo_ta()}


def dem_hang_cho(conn, pv: PhamVi) -> list[dict[str, Any]]:
    """So dong + Σ tien hang cho **theo tung tien te**. ⛔ Khong co dong "tong".

    Vi sao khong co dong tong: cong hai so khac don vi tien te ra mot con so la
    dung cai sai da tao ra con so *"310 dong phu 90% tien"* (thuc te 799 dong).
    Neu ham nay tra mot con so tong thi cho nao doc no cung se cong lai.
    """
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT i.curr, count(*)::int AS so_dong,"
            " SUM(COALESCE(i.ps_no,0)+COALESCE(i.ps_co,0)) AS tien"
            f" FROM fls_itl i WHERE i.work_status='UNMAPPED' AND {dk}"
            # ⭐ Cung dieu kien voi `_SQL_HANG_CHO` (`QĐ-ITL-71`) — hai cho khai
            # cung mot luat thi chung se lech, nen neu them dieu kien thu ba
            # thi phai gom lai mot cho.
            " AND NOT EXISTS (SELECT 1 FROM fls_da_xong x"
            " WHERE x.itl_id = i.itl_id)"
            " GROUP BY 1 ORDER BY 2 DESC", ts)
        return _dong(cur)


# ── nhat ky ───────────────────────────────────────────────────────────────
def doc_nhat_ky(conn, pv: PhamVi, itl_id: int) -> list[dict[str, Any]]:
    """Nhat ky `AUD-1` cua mot dong. Ngoai pham vi ⇒ rong.

    ⚠ Cau nay **noi qua `fls_itl`** chu khong doc thang `fls_journal`: nhat ky
    khong mang `run_id`, nen doc thang la mot duong khac vong pham vi.
    """
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT j.jrn_id, j.itl_id, j.field, j.value_before, j.value_after,"
            " j.actor, j.at, j.value_source, j.reason"
            " FROM fls_journal j JOIN fls_itl i USING (itl_id)"
            f" WHERE j.itl_id = %s AND {dk} ORDER BY j.at, j.jrn_id",
            [itl_id, *ts])
        return _dong(cur)


# ── cong ──────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Cong:
    """Mot cong. ⛔ `dat=None` la **chua do duoc**, ⛔ KHONG phai "xanh".

    Cong chung #7: *cong phai chung minh no DA DO DUOC GI*. Nen `dat=True` ma
    `da_do` rong la mot loi lap trinh — `__post_init__` NO. Do la cach duy nhat
    chan lai chuyen `verify_parity_all.py` da lam 26/08: doc 0 dong, so 0 o,
    roi in *"dung 100% tung o"* va tra PASS.
    """

    ma: str
    ten: str
    dat: bool | None
    da_do: str = ""
    ly_do: str = ""

    def __post_init__(self) -> None:
        if self.dat is True and not self.da_do.strip():
            raise ValueError(
                f"cong {self.ma}: dat=True ma khong noi DA DO DUOC GI — "
                f"cong chung #7 cam (mot cong khong do gi thi tat nhien "
                f"'khong thay loi')")
        if self.dat is None and not self.ly_do.strip():
            raise ValueError(
                f"cong {self.ma}: chua do duoc thi phai noi VI SAO chua do "
                f"duoc (`INV-I16` — khong mac dinh im lang)")

    @property
    def nhan(self) -> str:
        return {True: "DAT", False: "KHONG DAT", None: "CHUA DO DUOC"}[self.dat]


# Bon cong ke toan cua `BA-07` §2. FLS ⛔ chua do duoc cai nao vi ca bon deu can
# nguon ngoai chua noi vao. ⇒ Khai TUONG MINH la "chua do duoc" kem ly do, ⛔
# khong de chung xuat hien nhu cong xanh, va ⛔ khong an chung di.
_CHUA_DO_DUOC: tuple[tuple[str, str, str], ...] = (
    ("DIF_BANK", "DIF ngan hang (dong 226)",
     "can ket qua A-CCR tren BigQuery — chua noi (`GAP-ORA-05`)"),
    ("VI", "So du vi",
     "can nguon vi/P100 — FLS chi doc `fls_*`, chua co adapter (`QĐ-ITL-45`)"),
    ("DONG_BO", "Dong bo nguon",
     "can bang `fls_source` co du lieu — pipeline chua ghi manifest"),
    ("FINAL", "Luat Final tai hien tung o",
     "cong nay chay ngoai kho tren anh chup so goc"
     " (`fls/oracle/cong_parity.py`), ⛔ khong doc duoc tu mot cau SQL"),
    # ⭐ Them 27/08 sau khi phat hien cong "bon duong" cu la mot phep so vong
    # tron. Bon duong la `vao = so + loai + RONG + TRUNG`, ma **`rong` va
    # `trung` ⛔ khong duoc luu o dau ca** — chung chi ton tai trong bien in ra
    # luc chay `nap_that.py`. ⇒ Tu kho ⛔ khong the tai lap phep can nay.
    # `GAP-API-03`: muon co cong nay thi phai ghi bon con so vao `fls_run`.
    ("BON_DUONG", "Bon duong can nhau (vao = so + loai + rong + trung)",
     "`rong` va `trung` ⛔ khong duoc luu o bang nao — chung chi in ra luc chay"
     " `nap_that.py` roi mat. Tu kho ⛔ khong tai lap duoc phep can (`GAP-API-03`)"),
)


def doc_cong(conn, pv: PhamVi) -> list[Cong]:
    """Cac cong doc duoc tu kho, cong bon cong ke toan khai la **chua do duoc**.

    ⛔ Ham nay ⛔ khong bao gio tra danh sach toan xanh: bon cong `_CHUA_DO_DUOC`
    luon co mat voi `dat=None`. Mot man hinh *"4/4 cong xanh"* trong khi bon
    cong ke toan chua he do la con so noi doi tho nhat cua ca he.
    """
    from fls.repo import kho_sach

    ra: list[Cong] = []

    # ⓐ kho sach — cong nay dung tren KHO DANG MO, khong theo pham vi
    px = kho_sach.kiem(conn)
    if px.da_do:
        ra.append(Cong(ma="KHO_SACH", ten="Kho chi chua dong lan nap that",
                       dat=px.dat, da_do=" · ".join(px.da_do),
                       ly_do=" | ".join(px.ly_do)))
    else:
        ra.append(Cong(
            ma="KHO_SACH", ten="Kho chi chua dong lan nap that", dat=None,
            ly_do="khong dem duoc bang nao — ⛔ khong do duoc gi thi khong "
                  "phai 'sach'"))

    # ⓑ Σ moi noi = tien dong bank (`kiem_tong_moi_noi`, nhung tren KHO)
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*)::int AS so_dong,"
            " count(*) FILTER (WHERE z.s <> z.t)::int AS lech,"
            " COALESCE(SUM(abs(z.s - z.t)), 0) AS tong_lech FROM ("
            "  SELECT l.itl_id, SUM(l.amount) AS s,"
            "         MAX(COALESCE(i.ps_no,0)+COALESCE(i.ps_co,0)) AS t"
            # ⚠ Do tren `fls_moi_noi`: mot dong da bo HET moi noi thi ⛔ khong
            # con trong khung xem ⇒ tu roi khoi phep do (dung — no khong con
            # moi noi nao de can). Do tren `fls_pm_link` thi mot dong vua go
            # van bi cong nay do va bao **DAT** — mot cai xanh GIA.
            "  FROM fls_moi_noi l JOIN fls_itl i USING (itl_id)"
            f"  WHERE {dk} GROUP BY l.itl_id) z", ts)
        d = _dong(cur)[0]
    if d["so_dong"] == 0:
        ra.append(Cong(ma="SIGMA_MOI_NOI", ten="Σ moi noi = tien dong bank",
                       dat=None,
                       ly_do=f"khong co dong nao co moi noi trong {pv.mo_ta()}"
                             f" ⇒ ⛔ khong do duoc gi"))
    else:
        ra.append(Cong(
            ma="SIGMA_MOI_NOI", ten="Σ moi noi = tien dong bank",
            dat=d["lech"] == 0,
            da_do=f"{d['so_dong']} dong co moi noi",
            ly_do=("" if d["lech"] == 0 else
                   f"{d['lech']} dong lech, tong lech {d['tong_lech']}")))

    # ⓒ ⛔⛔ `row_count` cua `fls_run` DEM TU BANG (xem `chay_nap.dong_run`), nen
    # so no voi `count(fls_itl)` la mot **phep so vong tron**: no khong bao gio
    # do duoc gi luc nap. Nhung no **do duoc mot thu khac**: kho co bi doi sau
    # lan nap khong. Voi mot cai so append-only thi con so phai giu nguyen mai
    # mai, nen lech = co ai da doi so bang tay.
    #
    # ⚠ Ban dau toi de cong nay so `row_count` voi `vao_so + loai` roi goi no la
    # *"bon duong can nhau"*. Lan chay that dau tien (27/08) no **DO** — va do
    # la **do GIA**: 10.030 vs 10.030 + 19. Cong thuc tu suy ra tu chu "bon
    # duong" trong tai lieu ma ⛔ khong doc xem cot do THUC SU chua gi.
    dkr, tsr = pv.dieu_kien("r.run_id")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT r.run_id, r.row_count,"
            " (SELECT count(*) FROM fls_itl i WHERE i.run_id=r.run_id)::int"
            "   AS trong_so"
            f" FROM fls_run r WHERE {dkr} ORDER BY r.started_at DESC", tsr)
        runs = _dong(cur)
    if not runs:
        ra.append(Cong(ma="RUN_DEM_KHOP", ten="So dong moi lan nap khong bi doi",
                       dat=None,
                       ly_do=f"khong co lan nap nao trong {pv.mo_ta()}"))
    else:
        xau = [r for r in runs
               if r["row_count"] is not None
               and r["row_count"] != r["trong_so"]]
        ra.append(Cong(
            ma="RUN_DEM_KHOP", ten="So dong moi lan nap khong bi doi",
            dat=not xau, da_do=f"{len(runs)} lan nap",
            ly_do="; ".join(
                f"{r['run_id']}: chot {r['row_count']} != nay {r['trong_so']}"
                f" — co ai doi so sau khi nap (`INV-I08`)" for r in xau)))

    ra += [Cong(ma=m, ten=t, dat=None, ly_do=l) for m, t, l in _CHUA_DO_DUOC]
    return ra


def la_chi_doc(conn) -> bool:
    """Ket noi nay co bi PostgreSQL chan ghi khong?

    ⭐ Dung cho cua doc `P4`: no **tu choi chay** neu ket noi con ghi duoc. Mot
    cua doc chi-doc-vi-quy-uoc la mot cua se ghi vao mot ngay nao do. Chinh meo
    nay (`SET default_transaction_read_only = on`) da bat duoc that mot bai test
    dang `CREATE TABLE` len so that ngay 27/08 — no bat o tang kho, ⛔ khong dua
    vao ky luat nguoi viet.
    """
    with conn.cursor() as cur:
        cur.execute("show default_transaction_read_only")
        return cur.fetchone()[0] == "on"
