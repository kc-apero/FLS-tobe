"""Cong NGUOI BAM "XONG" (`GAP-JOIN-06` — owner chot 2026-08-28, `QĐ-ITL-71`).

★★ **Lo nay dong o day, ghi lai cho nguoi doc sau.** `fls_itl.work_status` bi
**dong bang luc nap** (`fls/ledger/build.py`) va ⛔ KHONG co gi tinh lai — moi
cua ghi deu ⛔ khong dung vao `fls_itl` (dung `INV-I08`). ⇒ Ke toan chua xong du
5 truong hop dong cua mot dong thi dong ay **VAN nam trong hang cho, mai mai**.

⚠ Do 28/08 tren kho that: **0 dong bi mac** *(vong ghi chua tung chay tren so
that)* ⇒ day la **co che thieu, chua phai thiet hai**. Nhung no hien ra **ngay
dau tien** ke toan dung man hinh.

★ **Owner chot: NGUOI BAM XONG**, ⛔ khong phai may tu nha khi thay du 5 truong.
  Can cu la NGHIEP VU: may tu nha thi ke toan **mat cho danh dau viec dang lam
  do**; nguoi bam thi hang cho dai hon nhung **dung y nguoi**.

★ Bai o day chan:
    ⓐ bam xong ⇒ dong **roi hang cho**, va ⛔ khong o nao cua `fls_itl` doi
    ⓑ bam hai lan ⛔ khong thanh hai su kien, nhung ⛔ khong im lang
    ⓒ **mo lai** duoc, va mo lai cung la **THEM** su kien (⛔ khong xoa)
    ⓓ ly do **TUY Y** khi du truong · **BAT BUOC** khi con thieu / ky da chot
    ⓔ ky da chot **VAN bam xong duoc** — CO Y, xem ly do o bai tuong ung
    ⓕ dong da xong ⛔ khong day % luy ke cua cac dong con lai
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import doc_bao_cao as bc
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import mot_lan_nap

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "ke-toan@apero.vn"

COT_PHAI_GIU = ("hd", "hd_thyt", "pay_type", "cdt1", "svc_start", "svc_end",
                "id_payee", "invoice", "work_status", "period_state",
                "raw_frozen", "pm_hinh")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    r = "NAP-2000-01-01-X" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _pv(run: str):
    """⚠ Pham vi bo GON vao DUNG lan nap cua bai nay.

    ⛔ Dung `chi_nap_that()` o day thi hang cho gom ca 10.030 dong that + moi
    dong bia cua moi bai khac ⇒ bai se do vi mot ly do ⛔ khong lien quan.
    """
    return mot_lan_nap(run)


def _dong_cho(conn, run: str, tien: str, *, du_truong: bool = False,
              ky: str = "open") -> int:
    """Mot dong UNMAPPED. `du_truong=True` ⇒ ca 5 truong hop dong co gia tri."""
    cot = ("content_key, source_system, source_sheet, source_row, run_id,"
           " contract_version, canon_version, mapping_version, raw_frozen,"
           " canon, doc_no, curr, ps_no, work_status, period_state")
    gt_ = ("%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
           "'FT-X',%s,%s,'UNMAPPED',%s")
    ts = [uuid.uuid4().hex, uuid.uuid4().int % 100000, run, "VND", D(tien), ky]
    if du_truong:
        cot += ", hd, pay_type, cdt1, svc_start, svc_end"
        gt_ += ",'FNS | X','Transfer','SHQ2 | HQ2','2026-01','2026-01'"
    return conn.execute(
        f"INSERT INTO fls_itl ({cot}) VALUES ({gt_}) RETURNING itl_id", ts
    ).fetchone()[0]


def _anh_so(conn, itl_id: int) -> tuple:
    return conn.execute(
        f"SELECT {', '.join(COT_PHAI_GIU)} FROM fls_itl WHERE itl_id=%s",
        (itl_id,)).fetchone()


def _hang_cho(conn, run: str) -> list[int]:
    return [d["itl_id"] for d in bc.doc_hang_cho(conn, _pv(run)).dong]


# ────────────────────────────────────────── ⓐ roi hang cho
def test_bam_xong_thi_dong_ROI_hang_cho__va_so_KHONG_doi_mot_o(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    assert _hang_cho(conn, run) == [i]
    truoc = _anh_so(conn, i)

    ra = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert ra["da_co"] is False and ra["ghi_de_ket_luan_may"] is False

    assert _hang_cho(conn, run) == [], "⛔ dong da bam xong VAN trong hang cho"
    assert _anh_so(conn, i) == truoc, "⛔⛔ `fls_itl` BI DOI khi bam xong"
    # ⭐ Dong so van con nguyen trong kho — roi hang cho ⛔ khong phai bi xoa.
    assert conn.execute("select count(*) from fls_itl where itl_id=%s",
                        (i,)).fetchone()[0] == 1


def test_phep_DEM_hang_cho_cung_tru__hai_cho_khong_duoc_lech(conn):
    """⛔ `doc_hang_cho` va `dem_hang_cho` la HAI cau SQL khai cung mot luat —
    neu chi sua mot cho thi man hinh se hien *"con 1 dong"* tren mot danh sach
    RONG, va ⛔ khong ai biet tin cai nao."""
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    assert [d["so_dong"] for d in bc.dem_hang_cho(conn, _pv(run))] == [1]
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert bc.dem_hang_cho(conn, _pv(run)) == []


def test_dong_da_xong_KHONG_day_phan_tram_luy_ke_cua_dong_khac(conn):
    """⛔⛔ Vi sao dieu kien phai nam TRONG cau con, ⛔ khong loc o dau ra.

    Hang cho xep theo **% luy ke tien**. Neu loc o dau ra thi mot dong da xong
    van tham gia phep cong ⇒ moi dong con lai bi day % len, va con so *"xem toi
    day la phu 90% tien"* sai ma ⛔ khong ai thay. Cung mot lop loi voi `CR#4`.
    """
    run = _run(conn)
    to = _dong_cho(conn, run, "900.00", du_truong=True)
    nho = _dong_cho(conn, run, "100.00", du_truong=True)
    d = {x["itl_id"]: x for x in bc.doc_hang_cho(conn, _pv(run)).dong}
    assert d[to]["luy_ke_pct"] == D("90.00") and d[nho]["luy_ke_pct"] == D("100.00")

    gt.danh_dau_xong(conn, _pv(run), to, actor=ACTOR)
    d = {x["itl_id"]: x for x in bc.doc_hang_cho(conn, _pv(run)).dong}
    assert list(d) == [nho]
    assert d[nho]["luy_ke_pct"] == D("100.00"), (
        "⛔ dong da xong van tham gia phep cong % — dieu kien bi loc o dau ra")


# ────────────────────────────────────────── ⓑ bam hai lan
def test_bam_HAI_lan_khong_thanh_hai_su_kien__va_noi_AI_da_bam(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    a = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    b = gt.danh_dau_xong(conn, _pv(run), i, actor="ke-toan-2@apero.vn")
    assert b["da_co"] is True and b["evt_id"] == a["evt_id"]
    assert b["boi"] == ACTOR and b["luc"] is not None, (
        "bam lan hai phai noi AI da bam va LUC NAO — ⛔ khong im lang")
    assert conn.execute(
        "select count(*) from fls_queue_event where itl_id=%s and evt_type='done'",
        (i,)).fetchone()[0] == 1


# ────────────────────────────────────────── ⓒ mo lai
def test_MO_LAI_thi_dong_ve_hang_cho__va_su_kien_cu_VAN_con(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    x = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert _hang_cho(conn, run) == []

    ra = gt.mo_lai(conn, _pv(run), i, actor="ke-toan-2@apero.vn",
                   reason="thieu hoa don, chua xong")
    assert ra["mo_lai_cua"] == x["evt_id"] and ra["xong_boi"] == ACTOR
    assert _hang_cho(conn, run) == [i], "⛔ mo lai ma dong ⛔ khong ve hang cho"
    # ⭐ Mo lai la THEM: ca hai su kien van nam trong so.
    assert conn.execute(
        "select count(*) from fls_queue_event where itl_id=%s"
        " and evt_type in ('done','reopen')", (i,)).fetchone()[0] == 2


def test_bam_XONG_lai_sau_khi_mo_lai__su_kien_MOI_NHAT_thang(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    gt.mo_lai(conn, _pv(run), i, actor=ACTOR, reason="mo lai da")
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert _hang_cho(conn, run) == []
    assert conn.execute("select count(*) from fls_da_xong where itl_id=%s",
                        (i,)).fetchone()[0] == 1


def test_MO_LAI_mot_dong_CHUA_tung_xong_thi_bi_TU_CHOI(conn):
    """⛔ Cau tra loi phai KHAC *"da xong"*: man hinh ve hai nut khac nhau."""
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    with pytest.raises(gt.ChuaXong):
        gt.mo_lai(conn, _pv(run), i, actor=ACTOR, reason="mo lai")


def test_MO_LAI_khong_ly_do_thi_bi_TU_CHOI(conn):
    """⛔ Khac `done`: dong nay da co NGUOI ket luan la xong, keo lai la **lat
    ket luan cua nguoi khac**."""
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    for xau in ("", "  ", None):
        with pytest.raises(gt.ThieuLyDo):
            gt.mo_lai(conn, _pv(run), i, actor=ACTOR, reason=xau)
    assert _hang_cho(conn, run) == []


# ────────────────────────────────── ⓓ ly do: tuy y vs BAT BUOC
def test_KHONG_doi_ly_do_khi_con_thieu__owner_da_bo_hang_rao(conn):
    """⛔⛔ **Bai nay khoa mot chieu QUAY LAI, ⛔ khong khoa mot tinh nang.**

    Ban dau toi bat ly do khi bam *xong* tren mot dong con thieu truong, lap
    luan: *"luc do nguoi dang ghi de ket luan cua may"* (`INV-I16`). Owner bo
    hang rao ay (2026-08-28, nguyen van *"ko can ghi ly do"*, `QĐ-ITL-72`).

    ★ Va lap luan cua owner vung hon: **mot cai o ly do bi BAT BUOC thi no
      thanh mot cai o RAC** — nguoi ta go mot chu roi bam, va tu do ⛔ khong ai
      doc cot ay nua. Mot cot ly do toan chu "x" **te hon** mot cot ly do
      TRONG, vi cot trong con **thanh that**.

    ⇒ Bai nay ton tai vi lap luan cu **nghe rat hop ly**, nen rat de co nguoi
      "chua" bang cach bat ly do lai. Ho se do o day, va doc duoc vi sao.
    """
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00")          # ⛔ khong truong nao
    ra = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)   # ⛔ khong reason
    assert _hang_cho(conn, run) == [], (
        "⛔ owner da chot: bam xong ⛔ KHONG can ly do, ke ca khi con thieu")
    # ⭐ Nhung phep DO thi GIU: man hinh van biet dong nay xong ma con thieu gi.
    assert ra["ghi_de_ket_luan_may"] is True
    assert set(ra["thieu_truong"]) == set(gt.TRUONG_HOP_DONG)


def test_DU_truong_thi_ly_do_TUY_Y(conn):
    """⛔ Bat ly do cho thao tac pho bien nhat la mot cai ma sat ⛔ khong thu
    duoc gi: nguoi ta se go bua mot chu roi bam."""
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)      # ⛔ khong reason
    assert _hang_cho(conn, run) == []


def test_gia_tri_NGUOI_GO_cung_tinh_la_DU_truong(conn):
    """⭐ *"Du truong"* phai tinh theo gia tri **HIEU LUC** — nguon HAY nguoi go.

    ⛔ Neu chi doc cot nguon thi mot dong ke toan vua go day 5 truong van bi
    doi ly do, va ho se ⛔ khong hieu vi sao.
    """
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    conn.execute("update fls_itl set hd=NULL where itl_id=%s", (i,))
    a = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert a["thieu_truong"] == ["hd"], "chua go thi phai bao la thieu `hd`"
    gt.mo_lai(conn, _pv(run), i, actor=ACTOR, reason="thu lai")

    gt.ghi_but_toan(conn, _pv(run), i, "hd", "FNS | Nguoi go",
                    actor=ACTOR, reason="dien hd", force=True)
    b = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert b["thieu_truong"] == [], (
        "⛔ gia tri NGUOI GO phai duoc tinh la DU — neu chi doc cot nguon thi "
        "mot dong ke toan vua go day 5 truong van bi bao la thieu")
    assert b["ghi_de_ket_luan_may"] is False
    assert _hang_cho(conn, run) == []


# ────────────────────────────────── ⓔ ky da chot: CHO, co y
def test_ky_DA_CHOT_van_bam_xong_duoc__va_KHONG_can_ly_do(conn):
    """⛔⛔ Cua nay CO Y **khac** moi cua ghi khac (`INV-I13` chan ky da chot).

    Ly do: ky da chot thi ke toan ⛔ khong sua duoc gia tri nao. Neu cung
    ⛔ khong danh dau xong duoc thi nhung dong ay **nam trong hang cho vinh vien
    ma ⛔ khong ai lam gi duoc** — hang cho tu bien thanh rac, va mot hang cho
    day rac thi ⛔ khong ai doc nua.

    ⚠ Owner xac nhan CA HAI dieu (2026-08-28): ky da chot **duoc** bam xong,
      va **⛔ khong can ly do** (`QĐ-ITL-72`).
    """
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True, ky="locked")
    ra = gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)   # ⛔ khong reason
    assert ra["ky_da_chot"] is True and ra["thieu_truong"] == []
    assert _hang_cho(conn, run) == []


def test_ngoai_pham_vi_thi_KHONG_bam_duoc(conn):
    with pytest.raises(gt.NgoaiPhamVi):
        gt.danh_dau_xong(conn, _pv(_run(conn)), 999_999_999, actor=ACTOR)


def test_thieu_actor_thi_NO(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    with pytest.raises(gt.LoiGhi):
        gt.danh_dau_xong(conn, _pv(run), i, actor="  ")


# ────────────────────────────────── phep dem "xong DU con thieu"
def test_dem_xong_DU_con_thieu__va_KHONG_ly_do_phai_bang_0(conn):
    """⛔⛔ Mot cai cua "cho" ma ⛔ khong ai dem thi som muon thanh **duong tat
    de lam sach hang cho**: bam xong het, hang cho ve 0, va ⛔ khong con dau vet
    nao noi rang hang nghin dong da bi dong ma chua ai tra loi."""
    run = _run(conn)
    du = _dong_cho(conn, run, "500.00", du_truong=True)
    thieu = _dong_cho(conn, run, "400.00")
    gt.danh_dau_xong(conn, _pv(run), du, actor=ACTOR)
    gt.danh_dau_xong(conn, _pv(run), thieu, actor=ACTOR)

    d = bc.dem_xong_du_thieu(conn, _pv(run))
    assert d["xong_du_con_thieu"] == 1, (
        "chi dong CON THIEU duoc dem — dong du truong ⛔ khong tinh")
    # ⚠ Tu `QĐ-ITL-72` ly do ⛔ khong con bat buoc, nen `khong_ly_do` la mot
    # con so BINH THUONG (⛔ khong phai mot lo) — no chi noi *"bao nhieu dong
    # duoc dong ma khong ai giai thich"*, de ai muon soi thi soi.
    assert d["khong_ly_do"] == 1


def test_MO_LAI_thi_khong_con_bi_dem(conn):
    run = _run(conn)
    i = _dong_cho(conn, run, "400.00")
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    assert bc.dem_xong_du_thieu(conn, _pv(run))["xong_du_con_thieu"] == 1
    gt.mo_lai(conn, _pv(run), i, actor=ACTOR, reason="doi y, con thieu that")
    assert bc.dem_xong_du_thieu(conn, _pv(run))["xong_du_con_thieu"] == 0


def test_drawer_HIEN_trang_thai_xong__ai_bam_va_luc_nao(conn):
    """⛔ Mot dong "xong" ma man hinh ⛔ khong noi ai bam va luc nao thi nut do
    la mot cai nut ⛔ khong ai chiu trach nhiem."""
    run = _run(conn)
    i = _dong_cho(conn, run, "1000.00", du_truong=True)
    assert bc.doc_mot_dong(conn, _pv(run), i)["da_xong"] is None
    gt.danh_dau_xong(conn, _pv(run), i, actor=ACTOR)
    x = bc.doc_mot_dong(conn, _pv(run), i)["da_xong"]
    assert x is not None and x["actor"] == ACTOR and x["at"] is not None
