"""Cac cau doc cua `P4` tren kho THAT-nhung-la-kho-TEST.

⛔⛔ **Bai quan trong nhat ca file: `test_dong_cua_run_LA_lam_LECH_luy_ke`.**

Do la bai ma khung xem `fls_queue_xep_tien` (migration 0008, bo o 0009) **khong
bao gio viet duoc**: khung xem SQL khong nhan tham so nen phep xep luon chay
tren ca kho, va loc o dau ra ⛔ khong sua duoc mot thu tu da xep sai.

★ Meo lam bai o day: **moi bai tu dat mot don vi tien te RIENG** (`T<HEX>`).
Kho test song qua nhieu lan chay `pytest` nen dong cua lan truoc con nguyen; neu
hai bai dung chung mot tien te thi con so luy ke doi theo THU TU CHAY, va mot
bai nhu the la bai khong dang tin.

★ `run_id` cua bai test co hinh dang THAT (`NAP-2000-01-01-...`) — bat buoc,
vi pham vi loc bang hinh dang. Cho phan biet la **NAM 2000**: cong `kiem_kho`
tu choi moi lan nap truoc `2024-01-01`, nen neu dau test nay lot vao so THAT
thi cong do do, ⛔ khong im lang.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import doc_bao_cao as bc
from fls.repo import kho_sach
from fls.repo.pham_vi import ca_kho, chi_nap_that, mot_lan_nap

pytestmark = pytest.mark.pg


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


def _run(cur, that: bool) -> str:
    """`that=True` ⇒ hinh dang lan nap that (nhung nam 2000, xem docstring)."""
    r = f"NAP-2000-01-01-THU{_hex()}" if that else f"T-{uuid.uuid4().hex[:8]}"
    cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong(cur, run: str, *, curr: str, tien: str,
          status: str = "UNMAPPED", ngay: str | None = None) -> int:
    cur.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, curr, ps_co, work_status, doc_date, doc_no)"
        " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,%s,%s) RETURNING itl_id",
        (uuid.uuid4().hex, run, curr, D(tien), status, ngay,
         f"CT{_hex(6)}"))
    return cur.fetchone()[0]


@pytest.fixture()
def lat(conn):
    """Mot lan nap THAT (3 dong: 100/200/700) + mot lan nap LA (1 dong 1.000.000).

    Ca bon dong cung MOT tien te rieng cua bai nay.
    """
    tt = "T" + _hex(5)
    with conn.cursor() as cur:
        that = _run(cur, True)
        la = _run(cur, False)
        ids = {
            "nho": _dong(cur, that, curr=tt, tien="100"),
            "vua": _dong(cur, that, curr=tt, tien="200"),
            "to": _dong(cur, that, curr=tt, tien="700"),
            "la_khong_lo": _dong(cur, la, curr=tt, tien="1000000"),
        }
    return {"tt": tt, "that": that, "la": la, **ids}


def _theo_id(t: bc.Trang) -> dict[int, dict]:
    return {d["itl_id"]: d for d in t.dong}


# ── pham vi ───────────────────────────────────────────────────────────────
def test_dong_cua_run_LA_khong_ra_so(conn, lat):
    """⛔ Dau test ⛔ khong duoc xuat hien trong so — day la 1.204 dong cua 27/08.

    ⚠⚠ **Ban dau bai nay lay `limit=500` roi kiem "khong co trong 500 dong dau".
    Do la mot bai XANH VI LY DO SAI** — do duoc 27/08 khi co tinh bo phep loc:
    bai van xanh, vi kho test co hang nghin dong nen dong la (`itl_id` 1676) roi
    ra ngoai trang dau. No do phan trang chan, ⛔ khong phai phep loc.

    ⇒ Sua hai chuyen: ⓐ dat con tro **ngay truoc** dong la, de neu phep loc mat
    thi dong do **chac chan** o trong trang · ⓑ do luon chieu nguoc (`ca_kho`)
    de bai **tu chung minh no do duoc gi** (cong chung #7) — mot bai chi kiem
    "khong thay" thi khong phan biet duoc "loc dung" voi "khong doc gi".
    """
    truoc = lat["la_khong_lo"] - 1
    t = bc.doc_so(conn, chi_nap_that(), con_tro=str(truoc), limit=5)
    assert lat["la_khong_lo"] not in _theo_id(t)

    # ⓑ Chieu nguoc: bo pham vi thi dong do CO ra ⇒ phep loc that su dang loc.
    t2 = bc.doc_so(conn, ca_kho("bai kiem: chung minh phep loc co tac dung"),
                   con_tro=str(truoc), limit=5)
    assert lat["la_khong_lo"] in _theo_id(t2), (
        "khong chung minh duoc phep loc co tac dung — bai nay dang xanh vi ly do sai")


def test_dong_cua_run_LA_khong_ra_hang_cho(conn, lat):
    """⛔ Va nhat la khong ra HANG CHO — 194 dong bia trong danh sach viec."""
    t = bc.doc_hang_cho(conn, chi_nap_that(), curr=lat["tt"], limit=500)
    assert lat["la_khong_lo"] not in _theo_id(t)
    assert set(_theo_id(t)) == {lat["nho"], lat["vua"], lat["to"]}


def test_mot_lan_nap_LA_thi_tra_RONG(conn, lat):
    """⛔ `?run_id=T-...` ⛔ khong mo duoc duong vong: pham vi GIAO ban trang."""
    t = bc.doc_so(conn, mot_lan_nap(lat["la"]), limit=10)
    assert t.dong == []


def test_mot_dong_ngoai_pham_vi_tra_None(conn, lat):
    assert bc.doc_mot_dong(conn, chi_nap_that(), lat["la_khong_lo"]) is None
    d = bc.doc_mot_dong(conn, mot_lan_nap(lat["that"]), lat["to"])
    assert d is not None and d["itl_id"] == lat["to"] and "canon" in d


# ── ⛔⛔ bai khung xem KHONG BAO GIO viet duoc ────────────────────────────
def test_dong_cua_run_LA_lam_LECH_luy_ke(conn, lat):
    """⭐⭐ Vi sao phep xep phai CO THAM SO, khong the la mot khung xem.

    Ba dong that: 100 · 200 · 700 ⇒ Σ = 1.000. Dong to nhat phu **70,00%**.

    Them mot dong cua lan nap LA (1.000.000) vao cung tien te:
      · trong pham vi ⇒ hang 1, luy ke **70,00** — dung
      · doc ca kho    ⇒ hang **2**, luy ke **99,97** — sai, va sai IM LANG:
        neu ai loc o DAU RA thi dong la bien khoi danh sach nhung **con so 99,97
        van o lai**, ⛔ khong con dau vet nao giai thich vi sao.
    """
    trong = _theo_id(bc.doc_hang_cho(
        conn, mot_lan_nap(lat["that"]), curr=lat["tt"], limit=50))[lat["to"]]
    assert (trong["hang"], trong["luy_ke_pct"]) == (1, D("70.00"))

    ngoai = _theo_id(bc.doc_hang_cho(
        conn, ca_kho("bai kiem: chung minh dong la lam lech luy ke"),
        curr=lat["tt"], limit=50))[lat["to"]]
    assert ngoai["hang"] == 2
    assert ngoai["luy_ke_pct"] == D("99.97"), ngoai["luy_ke_pct"]
    assert ngoai["luy_ke_pct"] != trong["luy_ke_pct"]


# ── xep theo tien te ──────────────────────────────────────────────────────
def test_xep_TRONG_TUNG_tien_te(conn):
    """⛔⛔ Cho de sai nhat: gop hai tien te thi 400.000 dong xep TREN 300.000 USD.

    Do that 27/08: hang cho co USD 4.492 dong vs VND 2.987; xep theo tong gop
    thi VND at het (872 ty vs 302 trieu USD chua doi ty gia) va toan bo dong USD
    bi dim xuong duoi.
    """
    a, b = "A" + _hex(5), "B" + _hex(5)
    with conn.cursor() as cur:
        r = _run(cur, True)
        usd_to = _dong(cur, r, curr=a, tien="300000")
        usd_nho = _dong(cur, r, curr=a, tien="10")
        vnd_nho = _dong(cur, r, curr=b, tien="400000")
    pv = mot_lan_nap(r)
    v = _theo_id(bc.doc_hang_cho(conn, pv, limit=50))
    assert v[usd_to]["hang"] == 1 and v[usd_nho]["hang"] == 2
    # ⛔ Cai KHONG duoc xay ra: `vnd_nho` (400.000) xep tren `usd_to` (300.000)
    # chi vi con so lon hon. Hai dong o HAI phan vung nen hang doc lap.
    assert v[vnd_nho]["hang"] == 1


def test_moi_tien_te_ket_thuc_o_100_phan_tram(conn, lat):
    t = bc.doc_hang_cho(conn, mot_lan_nap(lat["that"]), limit=500)
    cuoi: dict[str, D] = {}
    for d in t.dong:
        cuoi[d["curr"]] = d["luy_ke_pct"]
    assert cuoi and all(p == D("100.00") for p in cuoi.values()), cuoi


def test_luy_ke_TANG_DAN_theo_hang(conn, lat):
    t = bc.doc_hang_cho(conn, mot_lan_nap(lat["that"]), limit=500)
    pct = [d["luy_ke_pct"] for d in sorted(t.dong, key=lambda x: x["hang"])]
    assert pct == sorted(pct), pct


def test_den_pct_cat_dung_cho(conn, lat):
    """*"Xem toi day la phu 90% tien"* — 700 (70%) + 200 (90%) = hai dong."""
    t = bc.doc_hang_cho(conn, mot_lan_nap(lat["that"]), den_pct=90, limit=50)
    assert {d["itl_id"] for d in t.dong} == {lat["to"], lat["vua"]}


def test_CHI_lay_dong_trong_hang_cho(conn):
    """Dong da `ok` ⛔ khong duoc xuat hien — day la hang cho VIEC, khong phai ca so."""
    tt = "C" + _hex(5)
    with conn.cursor() as cur:
        r = _run(cur, True)
        xong = _dong(cur, r, curr=tt, tien="5000", status="ok")
    t = bc.doc_hang_cho(conn, mot_lan_nap(r), limit=50)
    assert xong not in _theo_id(t)


def test_dem_hang_cho_KHONG_co_dong_tong(conn, lat):
    """⛔ Khong dong "tong": cong hai tien te ra mot con so la con so trong hinh
    ma vo nghia — dung cai sai da tao ra "310 dong phu 90% tien"."""
    d = bc.dem_hang_cho(conn, mot_lan_nap(lat["that"]))
    assert all(x["curr"] for x in d), "co dong khong mang tien te ⇒ nghi la dong tong"
    mine = [x for x in d if x["curr"] == lat["tt"]][0]
    assert mine["so_dong"] == 3 and mine["tien"] == D("1000.00")


# ── phan trang ────────────────────────────────────────────────────────────
def test_phan_trang_khoa_khong_lap_khong_sot(conn, lat):
    p1 = bc.doc_so(conn, mot_lan_nap(lat["that"]), limit=2)
    assert len(p1.dong) == 2 and p1.con_tro is not None
    p2 = bc.doc_so(conn, mot_lan_nap(lat["that"]), limit=2, con_tro=p1.con_tro)
    assert len(p2.dong) == 1 and p2.con_tro is None
    ids = [d["itl_id"] for d in p1.dong + p2.dong]
    assert len(set(ids)) == 3 == len(ids)


def test_limit_bi_chan_tren(conn, lat):
    assert bc._trang(10_000) == bc.TRANG_TOI_DA
    assert bc._trang(None) == bc.TRANG_MAC_DINH
    with pytest.raises(ValueError):
        bc._trang(0)


def test_phan_trang_hang_cho_theo_khoa_doi(conn, lat):
    p1 = bc.doc_hang_cho(conn, mot_lan_nap(lat["that"]), limit=1)
    assert p1.con_tro == f"{lat['tt']}:1"
    p2 = bc.doc_hang_cho(conn, mot_lan_nap(lat["that"]), limit=5,
                         con_tro=p1.con_tro)
    assert [d["hang"] for d in p2.dong] == [2, 3]


# ── nhat ky ───────────────────────────────────────────────────────────────
def test_nhat_ky_ngoai_pham_vi_thi_RONG(conn, lat):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fls_journal (itl_id, field, value_before, value_after,"
            " actor, value_source, reason) VALUES (%s,'hd',NULL,'HD1',"
            "'thu@apero.vn','nguon','thu')", (lat["la_khong_lo"],))
    assert bc.doc_nhat_ky(conn, chi_nap_that(), lat["la_khong_lo"]) == []
    assert len(bc.doc_nhat_ky(conn, ca_kho("bai kiem nhat ky"),
                              lat["la_khong_lo"])) == 1


# ── cong ──────────────────────────────────────────────────────────────────
def test_cong_KHONG_BAO_GIO_toan_xanh(conn, lat):
    """⛔ Bon cong ke toan chua do duoc PHAI luon co mat. Mot man hinh "4/4 cong
    xanh" trong khi chung chua he do la con so noi doi tho nhat cua ca he."""
    c = bc.doc_cong(conn, mot_lan_nap(lat["that"]))
    chua = [x for x in c if x.dat is None]
    assert {x.ma for x in chua} >= {"DIF_BANK", "VI", "DONG_BO",
                                   "FINAL", "BON_DUONG"}
    assert all(x.ly_do for x in chua), "co cong 'chua do duoc' ma khong noi vi sao"


def test_cong_dat_True_ma_khong_noi_DA_DO_GI_thi_NO():
    """Cong chung #7 duoc cuong che bang KIEU, khong bang ky luat."""
    with pytest.raises(ValueError, match="DA DO DUOC GI"):
        bc.Cong(ma="X", ten="x", dat=True)
    bc.Cong(ma="X", ten="x", dat=True, da_do="3 dong")


def test_cong_chua_do_duoc_ma_khong_co_ly_do_thi_NO():
    with pytest.raises(ValueError, match="VI SAO"):
        bc.Cong(ma="X", ten="x", dat=None)


def test_cong_sigma_moi_noi_bat_lech(conn):
    """Σ moi noi != tien dong bank ⇒ cong DO. (`kiem_tong_moi_noi` chan luc ghi;
    cong nay canh tren KHO, vi mot cong chi chay luc ghi la mot cong khong biet
    du lieu da o trong kho co con dung khong.)"""
    tt = "S" + _hex(5)
    with conn.cursor() as cur:
        r = _run(cur, True)
        i = _dong(cur, r, curr=tt, tien="1000", status="ok")
        cur.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                    " run_id) VALUES (%s,'PM-X',999,'A',%s)", (i, r))
    c = {x.ma: x for x in bc.doc_cong(conn, mot_lan_nap(r))}
    assert c["SIGMA_MOI_NOI"].dat is False
    assert "1 dong lech" in c["SIGMA_MOI_NOI"].ly_do


def test_cong_sigma_khop_thi_DAT_va_noi_da_do_gi(conn):
    tt = "K" + _hex(5)
    with conn.cursor() as cur:
        r = _run(cur, True)
        i = _dong(cur, r, curr=tt, tien="1000", status="ok")
        cur.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                    " run_id) VALUES (%s,'PM-Y',600,'B',%s),"
                    " (%s,'PM-Z',400,'B',%s)", (i, r, i, r))
    c = {x.ma: x for x in bc.doc_cong(conn, mot_lan_nap(r))}
    assert c["SIGMA_MOI_NOI"].dat is True
    assert "1 dong co moi noi" == c["SIGMA_MOI_NOI"].da_do


def test_cong_sigma_KHONG_CO_moi_noi_thi_CHUA_DO_DUOC_khong_phai_xanh(conn):
    """⛔ 0 moi noi ⇒ `dat=None`. *"Khong do duoc gi"* ⛔ khong phai *"sach"* —
    dung bai hoc cua `verify_parity_all.py` 26/08."""
    with conn.cursor() as cur:
        r = _run(cur, True)
        _dong(cur, r, curr="Z" + _hex(5), tien="1")
    c = {x.ma: x for x in bc.doc_cong(conn, mot_lan_nap(r))}
    assert c["SIGMA_MOI_NOI"].dat is None
    assert "khong do duoc gi" in c["SIGMA_MOI_NOI"].ly_do


# ── hai bo may regex ──────────────────────────────────────────────────────
@pytest.mark.parametrize("run_id,mong", [
    ("NAP-2026-08-27-RAW", True),
    ("NAP-2026-08-27-ADJUSTED", True),
    ("NAP-2000-01-01-THU12AB", True),
    ("T-abc12345", False),
    ("nap-2026-08-27-raw", False),
    ("NAP-2026-8-27-RAW", False),
    ("NAP-2026-08-27-raw", False),
    ("NAP-2026-08-27-", False),
    ("xNAP-2026-08-27-RAW", False),
    ("NAP-2026-08-27-RAWx ", False),
])
def test_hai_bo_may_regex_hieu_GIONG_nhau(conn, run_id, mong):
    """★ Mau `run_id` khai MOT lan (Python) roi dua nguyen cho PostgreSQL.

    Hai bo may regex khac nhau nen phai doi chieu: neu chung lech thi pham vi
    o tang cong (Python) va pham vi o tang doc (SQL) noi hai chuyen khac nhau —
    va do la loai lech khong ai thay cho tan luc so sai.
    """
    with conn.cursor() as cur:
        cur.execute("select %s ~ %s", (run_id, kho_sach.HINH_RUN_THAT.pattern))
        sql = cur.fetchone()[0]
    assert sql is kho_sach.la_run_that(run_id) is mong, (
        f"{run_id!r}: SQL={sql} Python={kho_sach.la_run_that(run_id)} mong={mong}")


# ── ⛔ khong nhan "khong can lenh chi" ────────────────────────────────────
def test_KHONG_co_nhan_khong_can_lenh_o_bat_ky_dau(conn):
    """`QĐ-ITL-58` bo HAN trang thai giua: `work_status` chi co 2 gia tri.

    Khoa o TANG KHO. Ai them gia tri thu ba thi do — va do la dung, vi them
    nhan *"khong can lenh"* la **may tu dat ra quy dinh** trong khi `QĐ-ITL-56`
    noi **khong co quy dinh nao** de ma hoa.
    """
    co = {r[0] for r in conn.execute(
        "select distinct work_status from fls_itl where work_status is not null")}
    assert co <= {"ok", "UNMAPPED"}, f"co gia tri work_status la: {co}"


# ── ket noi chi doc ───────────────────────────────────────────────────────
def test_la_chi_doc_phan_biet_duoc_hai_loai_ket_noi(conn):
    """Cua doc `P4` tu choi chay neu ket noi con ghi duoc — bai nay chung minh
    phep do phan biet duoc that."""
    from fls.db.kho import noi_chi_doc

    assert bc.la_chi_doc(conn) is False       # ket noi thuong: ghi duoc
    c2 = noi_chi_doc(dsn_test())
    try:
        assert bc.la_chi_doc(c2) is True
    finally:
        c2.close()
