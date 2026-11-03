"""Cua doc CHAY THAT qua HTTP — cong chung #8 ap cho `P4`.

⛔ Bo bai nay ⛔ khong goi ham xu ly truc tiep. No dung may, goi bang HTTP, doc
JSON — vi cai `P4` phai chung minh la *"du lieu ra duoc qua HTTP"*, va mot bai
goi ham Python ⛔ khong chung minh dieu do (khong di qua de `Authorization`,
khong di qua dinh tuyen, khong di qua vo boc).
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

KHOA = "khoa-thu-cua-bo-test-dai-hon-ba-muoi-hai-ky-tu"


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture(scope="module")
def du_lieu():
    """Mot lan nap THAT (hinh dang) + mot lan nap LA, cung mot tien te rieng."""
    tt = "H" + _hex(5)
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        ra = {"tt": tt}
        for ten, hinh in (("that", True), ("la", False)):
            r = (f"NAP-2000-01-01-CUA{_hex()}" if hinh
                 else f"T-{uuid.uuid4().hex[:8]}")
            cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                        " canon_version, mapping_version)"
                        " VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
            ra[ten] = r
        for ten, run, tien in (("to", ra["that"], "900"),
                               ("nho", ra["that"], "100"),
                               ("cua_run_la", ra["la"], "500000")):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
                " doc_date, doc_no) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0',"
                "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)"
                " RETURNING itl_id",
                (uuid.uuid4().hex, run, tt, D(tien), f"CT{_hex(6)}"))
            ra[ten] = cur.fetchone()[0]
    return ra


@pytest.fixture(scope="module")
def may(du_lieu):
    """May THAT tren cong tuy he dieu hanh chon, ket noi CHI DOC vao kho TEST."""
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    try:
        m = cua.dung_may(mo, cong=0)
    except Exception:
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu
        raise
    t = threading.Thread(target=m.serve_forever, daemon=True)
    t.start()
    yield m
    m.shutdown()
    m.server_close()
    if cu is None:
        os.environ.pop(the.BIEN_KHOA, None)
    else:
        os.environ[the.BIEN_KHOA] = cu


def _the_song(giay: int = 300, sub: str = "ke.toan@apero.vn") -> str:
    return the.dong_the({"sub": sub, "exp": int(time.time()) + giay,
                         "vai": ["ke_toan"]}, KHOA.encode())


def _goi(may, duong: str, *, phuong_thuc: str = "GET", the_gui: str | None = "",
         ) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {}
    if the_gui is not None:
        de["Authorization"] = f"Bearer {the_gui or _the_song()}"
    try:
        c.request(phuong_thuc, duong, headers=de)
        r = c.getresponse()
        than = r.read()
        return r.status, json.loads(than) if than else {}
    finally:
        c.close()


V = cua.bang_tuyen.TIEN_TO


# ── the: fail-closed ──────────────────────────────────────────────────────
def test_khong_co_the_thi_401(may):
    ma, ra = _goi(may, f"{V}/ledger", the_gui=None)
    assert ma == 401 and ra["error"]["code"] == "FLS-UNAUTHORIZED"
    assert ra["data"] is None


def test_the_het_han_thi_401(may):
    ma, _ = _goi(may, f"{V}/ledger", the_gui=the.dong_the(
        {"sub": "a@b.c", "exp": int(time.time()) - 5}, KHOA.encode()))
    assert ma == 401


def test_the_ky_bang_khoa_khac_thi_401(may):
    ma, _ = _goi(may, f"{V}/ledger", the_gui=the.dong_the(
        {"sub": "a@b.c", "exp": int(time.time()) + 60}, b"x" * 40))
    assert ma == 401


def test_khong_co_the_thi_KHONG_biet_duong_nao_ton_tai(may):
    """⛔ Cua ⛔ khong duoc de nguoi khong co the do ban do he thong: duong that
    va duong bia phai tra **cung mot** cau tra loi."""
    a, _ = _goi(may, f"{V}/ledger", the_gui=None)
    b, _ = _goi(may, f"{V}/khong-he-co", the_gui=None)
    assert a == b == 401


# ── ⛔ khong duong ghi nao ────────────────────────────────────────────────
@pytest.mark.parametrize("pt", ["PUT", "DELETE", "PATCH", "POST"])
def test_moi_phuong_thuc_SUA_deu_405(may, pt):
    """`P4` la cua DOC. ⛔ Khong co duong nao ghi vao `fls_itl` (`INV-I08`)."""
    ma, ra = _goi(may, f"{V}/ledger", phuong_thuc=pt)
    assert ma == 405 and ra["error"]["code"] == "FLS-METHOD"


def test_duong_khong_co_thi_404(may):
    ma, ra = _goi(may, f"{V}/khong-he-co")
    assert ma == 404 and ra["error"]["code"] == "FLS-NOT-FOUND"


# ── du lieu ra duoc qua HTTP ─────────────────────────────────────────────
def test_so_ra_duoc_va_KHONG_co_dong_cua_run_LA(may, du_lieu):
    """⭐ Loi hua cua `P4`: cua doc **loc theo lan nap ngay tu dau**.

    ⚠⚠ **Bai nay tung XANH VI LY DO SAI, va no do THAT ngay 27/08** — cung dung
    cai benh toi da sua o tang kho ma **quen sua o day**: no lay `?limit=500`
    roi kiem *"dong la khong co trong trang dau"*. Kho test lon dan qua tung
    lan chay `pytest`, nen den `P5` thi chinh **dong cua bai nay** cung roi ra
    ngoai trang dau ⇒ bai do vi mot ly do chang lien quan gi den phep loc.

    ⇒ Sua giong ben kho: ⓐ dat con tro **ngay truoc** dong la, de neu phep loc
    mat thi dong do **chac chan** o trong trang · ⓑ do luon **chieu nguoc**
    (`?run_id=` cua lan nap that) de bai tu chung minh no doc duoc that.
    """
    truoc = du_lieu["cua_run_la"] - 1
    ma, ra = _goi(may, f"{V}/ledger?cursor={truoc}&limit=5")
    assert ma == 200
    assert du_lieu["cua_run_la"] not in {d["itl_id"] for d in ra["data"]["rows"]}

    # ⓑ Chieu nguoc: dong cua lan nap THAT thi ra duoc.
    ma, ra = _goi(may, f"{V}/ledger?run_id={du_lieu['that']}&limit=50")
    ids = {d["itl_id"] for d in ra["data"]["rows"]}
    assert du_lieu["to"] in ids and du_lieu["nho"] in ids
    assert du_lieu["cua_run_la"] not in ids


def test_hang_cho_ra_duoc_kem_hang_va_luy_ke(may, du_lieu):
    ma, ra = _goi(may, f"{V}/queue?run_id={du_lieu['that']}&curr={du_lieu['tt']}")
    assert ma == 200
    d = {x["itl_id"]: x for x in ra["data"]["rows"]}
    assert d[du_lieu["to"]]["hang"] == 1
    assert d[du_lieu["to"]]["luy_ke_pct"] == "90.00"
    assert d[du_lieu["nho"]]["luy_ke_pct"] == "100.00"


def test_tien_ra_ngoai_la_CHUOI(may, du_lieu):
    ma, ra = _goi(may, f"{V}/queue?run_id={du_lieu['that']}&curr={du_lieu['tt']}")
    t = ra["data"]["rows"][0]["tien"]
    assert isinstance(t, str), f"tien ra ngoai la {type(t).__name__}"


def test_mot_dong_cua_run_LA_thi_404_khong_phai_403(may, du_lieu):
    """⛔ `404` chu khong phai `403`: mot `403` noi *"co dong nay nhung anh khong
    duoc xem"* — tuc la tiet lo rang dong do ton tai."""
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['cua_run_la']}")
    assert ma == 404 and ra["error"]["code"] == "FLS-NOT-FOUND"
    ma, ra = _goi(may, f"{V}/ledger/{du_lieu['to']}")
    assert ma == 200 and ra["data"]["itl_id"] == du_lieu["to"]


def test_run_id_cua_lan_nap_LA_thi_tra_RONG(may, du_lieu):
    """⛔ `?run_id=T-...` ⛔ khong mo duoc duong vong ban trang."""
    ma, ra = _goi(may, f"{V}/queue?run_id={du_lieu['la']}")
    assert ma == 200 and ra["data"]["rows"] == []


def test_tham_so_sai_thi_400_khong_phai_500(may):
    ma, ra = _goi(may, f"{V}/ledger?limit=khong-phai-so")
    assert ma == 400 and ra["error"]["code"] == "FLS-BAD-REQUEST"
    ma, ra = _goi(may, f"{V}/journal")
    assert ma == 400 and "itl_id" in ra["error"]["detail"]


def test_cong_ra_duoc_va_KHONG_BAO_GIO_toan_xanh(may):
    ma, ra = _goi(may, f"{V}/gates")
    assert ma == 200
    assert ra["data"]["chua_do_duoc"] >= 5
    ma_cong = {c["ma"] for c in ra["data"]["cong"]}
    assert {"DIF_BANK", "VI", "DONG_BO", "FINAL", "BON_DUONG"} <= ma_cong


def test_hang_cho_tom_khong_co_dong_tong(may, du_lieu):
    ma, ra = _goi(may, f"{V}/queue/summary?run_id={du_lieu['that']}")
    assert ma == 200
    assert all(x["curr"] for x in ra["data"]["theo_tien_te"])


# ── vo boc + de ───────────────────────────────────────────────────────────
def test_vo_boc_du_ba_phan_va_meta_noi_PHAM_VI(may):
    ma, ra = _goi(may, f"{V}/gates")
    assert set(ra) == {"data", "error", "meta"}
    assert ra["meta"]["pham_vi"] == "chi lan nap that"
    assert ra["meta"]["data_status"] == "flash"
    assert ra["meta"]["request_id"]


def test_de_khong_khoe_ten_may_chu(may):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    try:
        c.request("GET", f"{V}/gates",
                  headers={"Authorization": f"Bearer {_the_song()}"})
        r = c.getresponse()
        r.read()
        assert r.getheader("X-Content-Type-Options") == "nosniff"
        assert r.getheader("Cache-Control") == "no-store"
        assert "Python" not in (r.getheader("Server") or "")
    finally:
        c.close()


# ── ⛔ may TU CHOI CHAY khi thieu dieu kien ──────────────────────────────
def test_thieu_khoa_thi_may_TU_CHOI_CHAY(monkeypatch):
    """⛔ Khong co chia khoa thi khong mo cua — ⛔ khong co che do "cho qua"."""
    monkeypatch.delenv(the.BIEN_KHOA, raising=False)

    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    with pytest.raises(RuntimeError, match="thieu FLS_JWT_SECRET"):
        cua.dung_may(mo, cong=0)


def test_ket_noi_con_GHI_DUOC_thi_may_TU_CHOI_CHAY(monkeypatch):
    """⭐⭐ Cua doc tu choi chay tren mot ket noi con ghi duoc.

    Nho vay *"cua doc khong ghi"* la mot dieu **PostgreSQL** cuong che, ⛔ khong
    phai mot loi hua trong tai lieu. Chinh meo nay da bat that mot bai test dang
    `CREATE TABLE` len so that ngay 27/08.
    """
    monkeypatch.setenv(the.BIEN_KHOA, KHOA)

    @contextlib.contextmanager
    def mo_ghi_duoc():
        conn = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield conn
        finally:
            conn.close()

    with pytest.raises(RuntimeError, match="con GHI duoc"):
        cua.dung_may(mo_ghi_duoc, cong=0)
