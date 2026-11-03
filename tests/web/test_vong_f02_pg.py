"""⛔ CONG RA cua `B5` — ca vong `F02` chay THAT qua HTTP tren kho THAT.

`test_luoi_f02_hanh_vi.py` va `test_lo_luu_f02.py` hoi *"man hinh lam dung
khong"* tren mot cua **gia**. Bai nay hoi cau con lai: *"cai cua ma man hinh
goi co that su tra nhu the khong"* — va no chay tren PostgreSQL that, qua HTTP
that, voi the that.

⛔⛔ **Vi sao phai co ca hai.** O `B4` bo test bat **ba loi that**, va ca ba
den tu cung mot cho: tin dac ta `BA-06` §8 thay vi **do cua** *(`GAP-SPEC-02`)*.
Cai im lang nhat la `cursor` vs `next_cursor` — man hinh se trong nhu **het
danh sach** trong khi con 2.937 dong. Mot bo test chi chay tren cua gia
⛔ **khong bao gio** bat duoc lop loi ay: cua gia tra dung cai ten ma nguoi viet
test **tuong** la dung.

⇒ Bai cuoi tep nay *(`test_ten_truong_man_F02_doc_deu_CO_THAT`)* ghim **tung
ten truong** ma `man_f02.js` doc, tren **cau tra loi that**.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import re
import threading
import time
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.web import phuc_vu as pv

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-vong-f02-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "lan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


def _chen(cur, run, *, curr, hd=None, hd_thyt=None, ky="open", doc_no="FT-F02"):
    cur.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version,"
        " mapping_version, raw_frozen, canon, doc_no, curr, ps_co,"
        " work_status, doc_date, hd, hd_thyt, period_state)"
        " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,"
        "'[]'::jsonb,%s,%s,%s,'UNMAPPED','2026-08-01',%s,%s,%s)"
        " RETURNING itl_id",
        (uuid.uuid4().hex, run, doc_no, curr, D("1000000.00"), hd, hd_thyt,
         ky))
    return cur.fetchone()[0]


@pytest.fixture()
def du_lieu():
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        tt = "F" + uuid.uuid4().hex[:5].upper()      # ⛔ tien te RIENG moi lan
        run = f"NAP-2000-01-01-F2{uuid.uuid4().hex[:6].upper()}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        trong = _chen(cur, run, curr=tt)                     # ⛔ chua gan gi
        co_nguon = _chen(cur, run, curr=tt, hd="HD-SO-GOC")  # so goc da noi
        co_may = _chen(cur, run, curr=tt, hd_thyt="HD-MAY")  # may goi y
        khoa = _chen(cur, run, curr=tt, ky="locked")         # ky DA CHOT
    return {"run": run, "tt": tt, "trong": trong, "nguon": co_nguon,
            "may": co_may, "khoa": khoa}


@contextlib.contextmanager
def _may():
    @contextlib.contextmanager
    def mo_doc():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    @contextlib.contextmanager
    def mo_ghi():
        conn = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(mo_doc, cong=0, mo_ghi=mo_ghi)
        threading.Thread(target=m.serve_forever, daemon=True).start()
        yield m
    finally:
        if m is not None:
            m.shutdown()
            m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


@pytest.fixture()
def may():
    with _may() as m:
        yield m


def _goi(may, duong, *, pt="GET", than=None):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {"Authorization": "Bearer " + the.dong_the(
        {"sub": AI, "exp": int(time.time()) + 300}, KHOA.encode())}
    body = json.dumps(than).encode() if than is not None else None
    if body is not None:
        de["Content-Type"] = "application/json"
    try:
        c.request(pt, duong, body=body, headers=de)
        r = c.getresponse()
        d = r.read()
        return r.status, (json.loads(d) if d else {})
    finally:
        c.close()


def _gia_tri(may, itl, truong="hd"):
    """⛔ Hoi CHINH cua ma man hinh doc, ⛔ khong hoi thang kho."""
    ma, r = _goi(may, f"{V}/ledger/{itl}/fields/{truong}")
    assert ma == 200, r
    return r["data"]["gia_tri"], r["data"]["value_source"]


# ══ ⓐ GO → VAO SO → NHAT KY ══════════════════════════════════════════════
def test_go_mot_o_thi_vao_so_va_de_lai_VET_du_bay_truong(may, du_lieu):
    itl = du_lieu["trong"]
    assert _gia_tri(may, itl) == (None, "UNMAPPED")

    ma, r = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-MOI",
                       "reason": "đối soát tháng 8 theo bảng PM"})
    assert ma == 200, r
    assert r["data"]["adj_id"] and r["data"]["jrn_id"]
    assert _gia_tri(may, itl) == ("HD-MOI", "sua_tay")

    ma, n = _goi(may, f"{V}/journal?itl_id={itl}")
    assert ma == 200
    dong = n["data"]["rows"]
    assert len(dong) == 1
    # `AUD-1`: **bay truong**. Thieu mot cai la mot vet ⛔ khong doc duoc.
    from fls.repo.ghi_tay import BAY_TRUONG
    for t in BAY_TRUONG:
        assert t in dong[0], f"nhat ky thieu truong {t!r}"
    assert dong[0]["actor"] == AI
    assert dong[0]["reason"] == "đối soát tháng 8 theo bảng PM"


def test_go_LAI_cung_gia_tri_thi_KHONG_thanh_but_toan_thu_hai(may, du_lieu):
    """⛔ Mot cai nut bi bam hai lan ⛔ khong duoc thanh hai but toan.

    ⚠ Va day cung la mot cho **MAT thong tin**, khai ra: neu ai co y *"xac
    nhan lai"* cung gia tri thi lan xac nhan do ⛔ khong vao so.
    """
    itl = du_lieu["trong"]
    t = {"field": "hd", "value": "HD-X", "reason": "lần 1"}
    ma, a = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST", than=t)
    assert ma == 200
    ma, b = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={**t, "reason": "lần 2"})
    assert ma == 200
    assert b["data"]["da_co"] is True
    assert b["data"]["adj_id"] == a["data"]["adj_id"]
    ma, n = _goi(may, f"{V}/journal?itl_id={itl}")
    assert len(n["data"]["rows"]) == 1


def test_ghi_ma_KHONG_noi_vi_sao_thi_bi_CHAN(may, du_lieu):
    """`INV-I16` — va man hinh dua vao dieu nay: o ly do la mot cai phanh
    THAT, ⛔ khong phai mot o trang tri."""
    ma, r = _goi(may, f"{V}/ledger/{du_lieu['trong']}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-Y"})
    # ⚠ **400 chu ⛔ khong 422**: tang cua chan truoc *(`thieu \`reason\``)* nen
    # `ThieuLyDo` cua tang ghi *(422 `FLS-UNMAPPED-HIDDEN`)* ⛔ khong bao gio
    # toi. Hai ma cho cung mot loi choi — ⛔ khong sua o day, chi **ghim** lai:
    # man hinh phai hieu ca hai, va `goi_cua.CAU` co ca hai.
    assert ma == 400, r
    assert r["error"]["code"] == "FLS-BAD-REQUEST"


def test_truong_LA_thi_400_va_cau_bao_TU_SUY_ra_so_truong(may, du_lieu):
    ma, r = _goi(may, f"{V}/ledger/{du_lieu['trong']}/fields/cdt1_cfa2")
    assert ma == 400
    # ⚠ Con so trong thong bao phai SUY tu tap thuc — cau nay tung ghi "10
    # truong" roi liet ke 7.
    ct = r["error"]["detail"]
    n = int(re.search(r"chi (\d+) truong", ct).group(1))
    ds = re.search(r"\[(.*)\]", ct).group(1).split(", ")
    assert n == len(ds) == 7, ct


# ══ ⓑ `US-025` — GO KHAC NGUON thi HE KEU ════════════════════════════════
def test_go_khac_SO_GOC_thi_409_va_noi_ra_gia_tri_kia(may, du_lieu):
    itl = du_lieu["nguon"]
    ma, r = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-TOI-GO", "reason": "x"})
    assert ma == 409, r
    assert r["error"]["code"] == "FLS-CONFLICT-SOURCE"
    # ⭐ Man hinh ve bang so sanh tu `khac` — nen no PHAI co, va PHAI mang
    # gia tri kia chu ⛔ khong chi mot cau chu.
    assert r["error"]["khac"] == {"nguon": "HD-SO-GOC"}
    assert _gia_tri(may, itl) == ("HD-SO-GOC", "nguon")   # ⛔ chua ghi gi


def test_go_khac_GOI_Y_CUA_MAY_cung_409(may, du_lieu):
    """⛔ `QĐ-ITL-35`: goi y cua may ⛔ khong duoc lang le bi de len."""
    ma, r = _goi(may, f"{V}/ledger/{du_lieu['may']}/adjust", pt="POST",
                 than={"field": "hd", "value": "KHAC", "reason": "x"})
    assert ma == 409
    assert r["error"]["khac"] == {"may_goi_y": "HD-MAY"}


def test_force_KEM_ly_do_thi_ghi_duoc_va_gia_tri_cu_VAN_doc_lai_duoc(
        may, du_lieu):
    itl = du_lieu["nguon"]
    ma, r = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-TOI-GO", "force": True,
                       "reason": "PM đã xác nhận lại 03/09"})
    assert ma == 200, r
    assert _gia_tri(may, itl) == ("HD-TOI-GO", "sua_tay")
    # ⭐ So la **chi them**: gia tri cu ⛔ khong mat.
    ma, n = _goi(may, f"{V}/journal?itl_id={itl}")
    assert n["data"]["rows"][0]["value_before"] == "HD-SO-GOC"
    assert n["data"]["rows"][0]["value_source"] == "nguon"


# ══ ⓒ DAO BUT TOAN — gia tri LUI VE ══════════════════════════════════════
def test_dao_but_toan_thi_gia_tri_LUI_VE_so_goc(may, du_lieu):
    itl = du_lieu["nguon"]
    ma, r = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-SAI", "force": True,
                       "reason": "gõ nhầm"})
    assert ma == 200
    adj = r["data"]["adj_id"]
    assert _gia_tri(may, itl) == ("HD-SAI", "sua_tay")

    ma, r = _goi(may, f"{V}/adjustments/{adj}/reverse", pt="POST",
                 than={"reason": "đảo lại vì gõ nhầm dòng"})
    assert ma == 200, r
    # ⭐ Lui ve gia tri cua SO GOC, ⛔ khong ve rong.
    assert _gia_tri(may, itl) == ("HD-SO-GOC", "nguon")

    # ⛔ Dao ⛔ KHONG xoa: ca hai but toan van con trong drawer.
    ma, d = _goi(may, f"{V}/ledger/{itl}")
    bt = d["data"]["but_toan"]
    assert len(bt) == 2
    assert [x["reversal_of"] for x in bt] == [None, adj]


def test_dao_MOT_BAN_DAO_thi_bi_chan(may, du_lieu):
    itl = du_lieu["trong"]
    ma, r = _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
                 than={"field": "hd", "value": "A", "reason": "x"})
    adj = r["data"]["adj_id"]
    ma, r = _goi(may, f"{V}/adjustments/{adj}/reverse", pt="POST",
                 than={"reason": "y"})
    dao = r["data"]["adj_id"]
    ma, r = _goi(may, f"{V}/adjustments/{dao}/reverse", pt="POST",
                 than={"reason": "z"})
    assert ma == 422, r


# ══ ⓓ KY DA CHOT — ⛔ khong ghi duoc, KE CA voi `force` ═══════════════════
def test_ky_DA_CHOT_thi_khong_ghi_duoc_ke_ca_voi_force(may, du_lieu):
    for than in ({"field": "hd", "value": "A", "reason": "x"},
                 {"field": "hd", "value": "A", "reason": "x", "force": True}):
        ma, r = _goi(may, f"{V}/ledger/{du_lieu['khoa']}/adjust", pt="POST",
                     than=than)
        assert ma == 409, r
        assert r["error"]["code"] == "FLS-LOCKED-PERIOD"


def test_man_hinh_DOC_DUOC_ky_da_chot_TRUOC_khi_cho_go(may, du_lieu):
    """⭐ Man ⛔ khong duoc de ke toan go xong roi moi bao *"ky da chot"*.

    Ca hai duong ma luoi doc — `GET /ledger` va `.../fields/{f}` — deu phai
    mang `period_state`.
    """
    ma, r = _goi(may, f"{V}/ledger/{du_lieu['khoa']}/fields/hd")
    assert r["data"]["period_state"] == "locked"
    # ⛔ Phan trang KHOA: dat con tro ngay TRUOC dong can xem. Keo
    # `?limit=500` tu dau kho thi bon dong cua bai nay nam ngoai trang dau,
    # va bai se do vi mot ly do ⛔ khong lien quan gi den dieu no hoi.
    ma, r = _goi(may, f"{V}/ledger?limit=10&cursor={du_lieu['khoa'] - 1}")
    d = [x for x in r["data"]["rows"] if x["itl_id"] == du_lieu["khoa"]][0]
    assert d["period_state"] == "locked"


# ══ ⓔ ⛔ CUA CHI DOC thi moi duong ghi cua `F02` deu 405 ══════════════════
def test_che_do_chi_doc_thi_moi_duong_ghi_cua_F02_tra_405(du_lieu):
    @contextlib.contextmanager
    def mo_doc():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(mo_doc, cong=0, mo_ghi=None)   # ⛔ ⛔ KHONG cua ghi
        threading.Thread(target=m.serve_forever, daemon=True).start()
        i = du_lieu["trong"]
        for duong, than in (
                (f"{V}/ledger/{i}/adjust", {"field": "hd", "value": "A",
                                            "reason": "x"}),
                (f"{V}/adjustments/1/reverse", {"reason": "x"})):
            ma, r = _goi(m, duong, pt="POST", than=than)
            assert ma == 405, (duong, ma, r)
        # ⭐ Va duong DOC van chay — che do chi doc ⛔ khong phai la tat may.
        assert _goi(m, f"{V}/ledger?limit=1")[0] == 200
    finally:
        if m is not None:
            m.shutdown()
            m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


# ══ ⭐⭐ GHIM TEN TRUONG — lop loi da mac BA LAN o `B4` ═══════════════════
def test_ten_truong_man_F02_doc_deu_CO_THAT(may, du_lieu):
    """⛔⛔ Doc `man_f02.js` **thay vi** liet ke bang tay: mot danh sach go tay
    o day se **troi** khoi man hinh, va luc do cong nay canh mot man hinh
    ⛔ khong con ton tai.
    """
    itl = du_lieu["trong"]
    _goi(may, f"{V}/ledger/{itl}/adjust", pt="POST",
         than={"field": "hd", "value": "A", "reason": "x"})

    ma, r = _goi(may, f"{V}/ledger?limit=1")
    assert set(r["data"]) >= {"rows", "next_cursor", "count"}
    ma, d = _goi(may, f"{V}/ledger/{itl}")
    ma, f = _goi(may, f"{V}/ledger/{itl}/fields/hd")
    ma, n = _goi(may, f"{V}/journal?itl_id={itl}")

    co = {
        "dong": set(d["data"]),
        "fields": set(f["data"]),
        "nhat_ky": set(n["data"]["rows"][0]),
        "but_toan": set(d["data"]["but_toan"][0]),
    }
    # Nhung truong `man_f02.js` doc thang tu cau tra loi.
    doi = {
        "dong": {"itl_id", "canon", "sua_tay", "moi_noi", "moi_noi_da_bo",
                 "but_toan", "da_xong", "invoice", "id_payee",
                 "hd_thyt", "pay_type_thyt", "cdt1_thyt", "svc_start_thyt",
                 "svc_end_thyt"},
        "fields": {"gia_tri", "value_source", "nguon", "may", "tay", "adj_id",
                   "period_state", "work_status"},
        "nhat_ky": {"at", "field", "value_before", "value_after", "actor",
                    "value_source", "reason"},
        "but_toan": {"adj_id", "field", "value_after", "actor", "reversal_of"},
    }
    for k, v in doi.items():
        thieu = sorted(v - co[k])
        assert not thieu, f"⛔ `{k}` thieu truong man hinh doc: {thieu}"

    # ⭐ Va chieu NGUOC. ⚠ Nhung chi tren nhung truong man hinh **that su
    # doc** — ⛔ khong phai ca `doi` o tren.
    #
    # ⛔⛔ Hai danh sach nay KHAC NHAU, va su khac ay la co that: cua
    # `.../fields/{f}` mang ca `nguon` lan `may`, nhung drawer suy hai thu do
    # tu chinh dong *(`d[f]` va `d[f + '_thyt']`)* nen no ⛔ khong doc hai
    # truong ay. Gop hai danh sach lam mot thi hoac cong bat mot loi ⛔ khong
    # co that, hoac phai noi long den muc ⛔ khong con bat duoc gi.
    with open(os.path.join(pv.THU_MUC, "man_f02.js"), encoding="utf-8") as f2:
        ma_nguon = f2.read()
    dung = ({"tay", "gia_tri"} | doi["nhat_ky"]
            | {"sua_tay", "moi_noi", "but_toan", "da_xong", "next_cursor"})
    for t in dung:
        assert re.search(r"[.\['\"]" + t + r"[.\]'\"]?", ma_nguon), (
            f"⛔ `{t}` ⛔ khong con duoc `man_f02.js` doc — cong nay dang canh "
            f"mot man hinh ⛔ khong con ton tai")


def test_cursor_cua_LEDGE_cung_ten_next_cursor_nhu_hang_cho(may, du_lieu):
    """⛔⛔ Dung cai bay da mac o `B4` *(`GAP-SPEC-02`)*: tham so **gui len**
    ten la `cursor`, truong **tra ve** ten la `next_cursor`.

    Doc nham thi nut *"Xem thêm"* ⛔ **khong bao gio hien** — man hinh trong
    y het **het so**, va ⛔ khong mot thong bao nao.
    """
    ma, r = _goi(may, f"{V}/ledger?limit=1")
    assert "next_cursor" in r["data"] and "cursor" not in r["data"]
    con = r["data"]["next_cursor"]
    assert con, "kho thu phai co hon 1 dong de bai nay co nghia"
    ma, r2 = _goi(may, f"{V}/ledger?limit=1&cursor={con}")
    assert ma == 200
    assert r2["data"]["rows"][0]["itl_id"] != r["data"]["rows"][0]["itl_id"]
