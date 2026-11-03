"""Cua GHI (`P5`) CHAY THAT qua HTTP.

⛔ Bo bai nay ⛔ khong goi ham xu ly truc tiep: cai `P5` phai chung minh la
*"nguoi go duoc qua HTTP va de lai vet"*, va mot bai goi ham Python ⛔ khong di
qua de `Authorization`, khong di qua phep chon ket noi, khong di qua vo boc.

★ Bai quan trong nhat: `test_duong_DOC_khong_bao_gio_dung_ket_noi_GHI` — no khoa
dieu lam cho `P5` ⛔ khong lam yeu `P4` mot chut nao.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-cua-ghi-dai-hon-ba-muoi-hai-ky-tu-that"
AI = "ke.toan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def du_lieu():
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        run = f"NAP-2000-01-01-HTTP{_hex()}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        la = f"T-{uuid.uuid4().hex[:8]}"
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (la,))
        ra = {"run": run, "run_la": la}
        for ten, r, them in (("trong", run, {}),
                             ("co_nguon", run, {"hd": "HD-NGUON"}),
                             ("chot", run, {"period_state": "locked"}),
                             ("ngoai", la, {})):
            co = {"content_key": uuid.uuid4().hex, "source_system": "RAW",
                  "source_sheet": "L1", "source_row": 1, "run_id": r,
                  "contract_version": "v1.0", "canon_version": "v1.0",
                  "mapping_version": "v1.0", "raw_frozen": False,
                  "canon": "{}", "curr": "VND", "ps_co": D("1000"),
                  "work_status": "UNMAPPED", **them}
            cur.execute(f"INSERT INTO fls_itl ({', '.join(co)}) VALUES ("
                        + ", ".join(["%s"] * len(co)) + ") RETURNING itl_id",
                        list(co.values()))
            ra[ten] = cur.fetchone()[0]
    return ra


def _mo_doc():
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()
    return mo


class DemMo:
    """Ham mo ket noi GHI, co DEM — de chung minh duong doc ⛔ khong dung no."""

    def __init__(self) -> None:
        self.lan = 0

    def __call__(self):
        @contextlib.contextmanager
        def mo():
            self.lan += 1
            conn = psycopg.connect(dsn_test(), autocommit=True)
            try:
                yield conn
            finally:
                conn.close()
        return mo()


@contextlib.contextmanager
def _may(mo_ghi=None):
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = None
    try:
        m = cua.dung_may(_mo_doc(), cong=0, mo_ghi=mo_ghi)
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
def dem_ghi():
    return DemMo()


@pytest.fixture()
def may(dem_ghi):
    with _may(mo_ghi=dem_ghi) as m:
        # ⚠ `dung_may()` DA goi duong ghi mot lan de kiem no ⛔ khong phai ket
        # noi chi-doc. Do la dung — nen phai dat lai mo dem ve 0, khong thi
        # bai duoi bao "duong doc da dung ket noi ghi" **sai**.
        dem_ghi.lan = 0
        yield m


@pytest.fixture()
def may_chi_doc():
    with _may(mo_ghi=None) as m:
        yield m


def _the(sub: str = AI, giay: int = 300) -> str:
    return the.dong_the({"sub": sub, "exp": int(time.time()) + giay},
                        KHOA.encode())


def _goi(may, duong: str, *, pt: str = "GET", than: dict | None = None,
         the_gui: str | None = "", ct: str = "application/json",
         tho: bytes | None = None) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de: dict[str, str] = {}
    if the_gui is not None:
        de["Authorization"] = f"Bearer {the_gui or _the()}"
    body = tho if tho is not None else (
        json.dumps(than).encode() if than is not None else None)
    if body is not None:
        de["Content-Type"] = ct
    try:
        c.request(pt, duong, body=body, headers=de)
        r = c.getresponse()
        d = r.read()
        return r.status, (json.loads(d) if d else {})
    finally:
        c.close()


# ── ⭐ bat bien lam cho P5 khong lam yeu P4 ──────────────────────────────
def test_duong_DOC_khong_bao_gio_dung_ket_noi_GHI(may, dem_ghi, du_lieu):
    """⭐⭐ Ket noi do BANG TUYEN chon, ⛔ khong do ham xu ly chon.

    Du may dang mo nhom ghi, moi duong `GET` van chay tren ket noi **bi
    PostgreSQL chan ghi**. Nho vay `P5` ⛔ khong lam yeu dieu *"cua doc khong
    ghi duoc"* cua `P4` mot chut nao.
    """
    for d in (f"{V}/ledger?limit=5", f"{V}/queue?limit=5", f"{V}/gates",
              f"{V}/ledger/{du_lieu['trong']}"):
        ma, _ = _goi(may, d)
        assert ma == 200, d
    assert dem_ghi.lan == 0, "duong doc da dung ket noi GHI"

    ma, _ = _goi(may, f"{V}/queue/{du_lieu['trong']}/reason", pt="POST",
                 than={"reason": "cho doi tac"})
    assert ma == 200 and dem_ghi.lan == 1


def test_che_do_CHI_DOC_thi_moi_duong_ghi_tra_405(may_chi_doc, du_lieu):
    """`mo_ghi=None` ⇒ khai tuong minh la cua chi doc, ⛔ khong am tham cho ghi."""
    ma, ra = _goi(may_chi_doc, f"{V}/ledger/{du_lieu['trong']}/adjust",
                  pt="POST", than={"field": "hd", "value": "X", "reason": "r"})
    assert ma == 405 and "CHI DOC" in ra["error"]["detail"]


# ── the ─────────────────────────────────────────────────────────────────
def test_POST_khong_co_the_thi_401(may, du_lieu):
    ma, _ = _goi(may, f"{V}/queue/{du_lieu['trong']}/reason", pt="POST",
                 than={"reason": "r"}, the_gui=None)
    assert ma == 401


def test_actor_lay_TU_THE_khong_tu_than_yeu_cau(may, du_lieu):
    """⛔⛔ `AUD-1`: nhat ky ma nguoi goi tu khai `actor` thi vo nghia.

    Va khi ai gui `actor` thi phai **NO**, ⛔ khong am tham bo qua: mot cai nut
    gui `actor` roi thay no bi bo qua la mot ky vong sai da hinh thanh.
    """
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['trong']}/adjust", pt="POST",
                  than={"field": "hd", "value": "X", "reason": "r",
                        "actor": "giam.doc@apero.vn"})
    assert ma == 400 and "actor" in ra["error"]["detail"]

    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['trong']}/adjust", pt="POST",
                  than={"field": "hd", "value": "X", "reason": "co ly do"},
                  the_gui=_the(sub="nguoi.that@apero.vn"))
    assert ma == 200 and ra["data"]["actor"] == "nguoi.that@apero.vn"


# ── than yeu cau ────────────────────────────────────────────────────────
@pytest.mark.parametrize("mo_ta,mong,kw", [
    ("khong than", 400, {}),
    ("khong phai JSON", 400, {"tho": b"khong phai json"}),
    ("khong phai doi tuong", 400, {"tho": b"[1,2,3]"}),
    ("sai Content-Type", 400, {"than": {"reason": "r"}, "ct": "text/plain"}),
    # ⛔ 413, ⛔ khong phai 400: may TU CHOI ma ⛔ khong doc het than — doc het
    # la lam dung cai viec ma gioi han nay dung ra de tranh.
    ("than qua to", 413, {"tho": b'{"reason":"' + b"x" * 70000 + b'"}'}),
])
def test_than_yeu_cau_sai_thi_bi_TU_CHOI(may, du_lieu, mo_ta, mong, kw):
    """⛔ Mac dinh la TU CHOI. Mot phep ghi doan y nguoi goi la mot phep ghi
    ⛔ khong truy duoc ve sau."""
    ma, ra = _goi(may, f"{V}/queue/{du_lieu['trong']}/reason", pt="POST", **kw)
    assert ma == mong, f"{mo_ta}: {ma} {ra}"


def test_thieu_LY_DO_thi_400(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['trong']}/adjust", pt="POST",
                  than={"field": "hd", "value": "X"})
    assert ma == 400 and "reason" in ra["error"]["detail"]


# ── adjust ──────────────────────────────────────────────────────────────
def test_go_mot_truong_va_no_ra_o_LAN_DOC_SAU(may, du_lieu):
    i = du_lieu["trong"]
    ma, ra = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                  than={"field": "cdt1", "value": "CDT-X",
                        "reason": "theo hop dong 2026"})
    assert ma == 200 and ra["data"]["adj_id"] and ra["data"]["jrn_id"]
    assert ra["data"]["value_source"] == "UNMAPPED"

    ma, ra = _goi(may, f"{V}/ledger/{i}")
    assert ra["data"]["sua_tay"]["cdt1"]["value_after"] == "CDT-X"
    # ⛔ Cot nguon van RONG — nguoi go ⛔ khong de len cot nguon.
    assert ra["data"]["cdt1"] is None

    ma, ra = _goi(may, f"{V}/journal?itl_id={i}")
    assert ma == 200 and len(ra["data"]["rows"]) == 1
    assert ra["data"]["rows"][0]["actor"] == AI


def test_go_khac_NGUON_thi_409_va_noi_nguon_dang_la_gi(may, du_lieu):
    """`US-025`: he **KEU**. Va no phai noi **nguon dang la gi**, khong thi man
    hinh khong the hoi *"ghi de khong?"* mot cach tu te."""
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['co_nguon']}/adjust", pt="POST",
                  than={"field": "hd", "value": "HD-KHAC", "reason": "r"})
    assert ma == 409 and ra["error"]["code"] == "FLS-CONFLICT-SOURCE"
    assert ra["error"]["khac"]["nguon"] == "HD-NGUON"
    assert ra["error"]["gia_tri_go"] == "HD-KHAC"


def test_force_thi_ghi_duoc(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['co_nguon']}/adjust?force=true",
                  pt="POST", than={"field": "hd", "value": "HD-KHAC",
                                   "reason": "hoa don xac nhan khac"})
    assert ma == 200 and ra["data"]["value_before"] == "HD-NGUON"


def test_ky_da_chot_thi_409_LOCKED(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['chot']}/adjust?force=true",
                  pt="POST", than={"field": "hd", "value": "X", "reason": "r"})
    assert ma == 409 and ra["error"]["code"] == "FLS-LOCKED-PERIOD"


def test_dong_ngoai_pham_vi_thi_404(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['ngoai']}/adjust", pt="POST",
                  than={"field": "hd", "value": "X", "reason": "r"})
    assert ma == 404 and ra["error"]["code"] == "FLS-NOT-FOUND"


def test_truong_ngoai_10_thi_400(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['trong']}/adjust", pt="POST",
                  than={"field": "ps_no", "value": "9", "reason": "r"})
    assert ma == 400


def test_cua_hoi_NGUON_NOI_GI_truoc_khi_go(may, du_lieu):
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['co_nguon']}/fields/hd")
    assert ma == 200
    assert ra["data"]["nguon"] == "HD-NGUON"
    assert ra["data"]["value_source"] == "nguon"
    assert ra["data"]["work_status"] == "UNMAPPED"


# ── dao but toan ────────────────────────────────────────────────────────
def test_dao_but_toan_qua_HTTP_lui_ve_gia_tri_truoc(may, du_lieu):
    i = du_lieu["trong"]
    _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
         than={"field": "hd", "value": "A", "reason": "1"})
    ma, ra = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                  than={"field": "hd", "value": "B", "reason": "2"})
    adj = ra["data"]["adj_id"]
    ma, ra = _goi(may, f"{V}/adjustments/{adj}/reverse", pt="POST",
                  than={"reason": "go sai"})
    assert ma == 200 and ra["data"]["dao_cua"] == adj
    ma, ra = _goi(may, f"{V}/ledger/{i}/fields/hd")
    assert ra["data"]["gia_tri"] == "A"


# ── hang cho ────────────────────────────────────────────────────────────
def test_hoan_lan_thu_BA_doi_mau_va_KHONG_leo_cap(may, du_lieu):
    i = du_lieu["trong"]
    for n in range(1, 4):
        ma, ra = _goi(may, f"{V}/queue/{i}/defer", pt="POST",
                      than={"until": "2026-09-30", "reason": f"cho lan {n}"})
        assert ma == 200 and ra["data"]["so_lan_hoan"] == n
    assert ra["data"]["doi_mau"] is True
    # ⛔ Lan thu tu VAN ghi duoc — `QĐ-ITL-24`: luong nay khong co cap tren.
    ma, ra = _goi(may, f"{V}/queue/{i}/defer", pt="POST",
                  than={"until": "2026-10-31", "reason": "cho nua"})
    assert ma == 200 and ra["data"]["so_lan_hoan"] == 4


def test_hoan_khong_co_HAN_thi_400(may, du_lieu):
    ma, ra = _goi(may, f"{V}/queue/{du_lieu['trong']}/defer", pt="POST",
                  than={"reason": "cho"})
    assert ma == 400


def test_ly_do_ra_duoc_o_hang_cho(may, du_lieu):
    i = du_lieu["trong"]
    ma, _ = _goi(may, f"{V}/queue/{i}/reason", pt="POST",
                 than={"reason": "cho ke toan doi tac tra loi"})
    assert ma == 200
    ma, ra = _goi(may, f"{V}/queue?run_id={du_lieu['run']}&limit=50")
    d = {x["itl_id"]: x for x in ra["data"]["rows"]}
    assert d[i]["reason"] == "cho ke toan doi tac tra loi"


# ── ⛔ so khong doi mot o nao ────────────────────────────────────────────
def test_sau_MOI_phep_ghi_qua_HTTP_so_van_khong_doi_mot_o(may, du_lieu):
    i = du_lieu["co_nguon"]
    cot = ("hd, hd_thyt, pay_type, cdt1, svc_start, svc_end, id_payee,"
           " invoice, work_status,"
           " period_state, raw_frozen, is_flash")
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        truoc = c.execute(f"select {cot} from fls_itl where itl_id=%s",
                          (i,)).fetchone()
    _goi(may, f"{V}/ledger/{i}/adjust?force=true", pt="POST",
         than={"field": "hd", "value": "HD-TAY", "reason": "r"})
    _goi(may, f"{V}/queue/{i}/reason", pt="POST", than={"reason": "r"})
    _goi(may, f"{V}/queue/{i}/defer", pt="POST",
         than={"until": "2026-09-30", "reason": "r"})
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        sau = c.execute(f"select {cot} from fls_itl where itl_id=%s",
                        (i,)).fetchone()
    assert truoc == sau, "co o trong fls_itl bi doi qua cua HTTP"
