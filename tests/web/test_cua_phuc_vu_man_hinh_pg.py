"""Cua CHAY THAT co kem man hinh — cong ra cua `B2`.

⛔ Bo bai nay ⛔ khong goi ham truc tiep: no dung may, goi bang HTTP that. Vi cai
`B2` phai chung minh la *"vo man hinh ra duoc, VA mot cua that goi duoc, tren
cung mot cong"* — mot bai goi ham Python ⛔ khong chung minh dieu do.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time

import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web.than_sinh import than_sinh

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-man-hinh-bo-test-dai-hon-ba-muoi-hai-ky-tu"
V = cua.bang_tuyen.TIEN_TO


@pytest.fixture(scope="module")
def may():
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
        m = cua.dung_may(mo, cong=0, phuc_vu_tep=lam_nguoi_phuc_vu(
            {"the": "THE-GIA-CUA-BO-TEST", "actor": "lan@apero.vn",
             "cho_ghi": False}, than_sinh=than_sinh()))
    except Exception:
        os.environ.pop(the.BIEN_KHOA, None) if cu is None else \
            os.environ.__setitem__(the.BIEN_KHOA, cu)
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


def _the_song(giay: int = 300) -> str:
    return the.dong_the({"sub": "ke.toan@apero.vn",
                         "exp": int(time.time()) + giay,
                         "vai": ["ke_toan"]}, KHOA.encode())


def _goi(may, duong, *, phuong_thuc="GET", the_gui=None):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {"Authorization": f"Bearer {the_gui}"} if the_gui else {}
    try:
        c.request(phuong_thuc, duong, headers=de)
        r = c.getresponse()
        return r.status, dict(r.getheaders()), r.read()
    finally:
        c.close()


# ── ⓐ vo man hinh ra duoc TRUOC the ───────────────────────────────────────
def test_vo_man_hinh_ra_duoc_khong_can_the(may):
    """⛔ Trinh duyet ⛔ khong gan duoc `Authorization` o lan tai trang dau."""
    ma, de, than = _goi(may, "/")
    assert ma == 200
    assert de["Content-Type"].startswith("text/html")
    assert b"<title>FLS" in than


@pytest.mark.parametrize("duong", [
    "/tokens.css", "/hinh.css", "/goi_cua.js", "/trang_thai.js",
    "/thanh_phan.js", "/man_f03.js", "/ung_dung.js", "/phien.js"])
def test_moi_tep_khai_deu_ra_duoc(may, duong):
    ma, _, than = _goi(may, duong)
    assert ma == 200 and than


def test_dau_de_an_toan_co_du(may):
    _, de, _ = _goi(may, "/")
    assert de["Cache-Control"] == "no-store"
    assert de["X-Content-Type-Options"] == "nosniff"
    csp = de["Content-Security-Policy"]
    assert "default-src 'none'" in csp
    assert "script-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


# ── ⓑ ⭐⭐ tep tinh ⛔ KHONG BAO GIO cham vung cua ─────────────────────────
def test_duong_cua_khong_the_bi_mot_tep_tinh_chiem(may):
    """`GET` vao vung cua ⛔ khong co the ⇒ van phai la `401`, ⛔ khong phai HTML."""
    ma, de, than = _goi(may, f"{V}/gates")
    assert ma == 401
    assert de["Content-Type"].startswith("application/json")
    assert json.loads(than)["error"]["code"] == "FLS-UNAUTHORIZED"


def test_duong_la_ngoai_vung_cua_tra_404_JSON(may):
    ma, de, than = _goi(may, "/khong-co-tep-nay.js")
    assert ma == 404
    assert de["Content-Type"].startswith("application/json")
    assert json.loads(than)["error"]["code"] == "FLS-NOT-FOUND"


@pytest.mark.parametrize("duong", [
    "/../pyproject.toml", "/..%2fpyproject.toml", "/../../fls/db/kho.py"])
def test_khong_vuot_ra_khoi_thu_muc_tep(may, duong):
    ma, _, than = _goi(may, duong)
    assert ma in (400, 404)
    assert b"psycopg" not in than and b"[importlinter" not in than


def test_POST_vao_duong_tep_van_di_qua_the(may):
    """⛔ Chi `GET` duoc phuc vu tinh — moi phep ghi van phai co the."""
    ma, de, _ = _goi(may, "/", phuong_thuc="POST")
    assert ma == 401
    assert de["Content-Type"].startswith("application/json")


# ── ⓒ ⭐ MOT VONG TRON: man hinh goi mot cua THAT ─────────────────────────
def test_goi_duoc_mot_cua_that_tren_cung_cong(may):
    ma, de, than = _goi(may, f"{V}/gates", the_gui=_the_song())
    assert ma == 200
    j = json.loads(than)
    assert j["error"] is None
    assert "cong" in j["data"]
    # ⛔ Ba con so phai cung ra — mot man noi "n/n xanh" ma giau so **chua do
    # duoc** la mot con so noi doi (`xu_ly.cong`).
    for k in ("dat", "khong_dat", "chua_do_duoc"):
        assert k in j["data"]
    assert j["meta"]["data_status"] in ("flash", "reconciled", "signed")


# ── ⭐ `B3` · cua DO PHU ───────────────────────────────────────────────────
def test_do_phu_tra_ve_theo_tung_tien_te(may):
    ma, _, than = _goi(may, f"{V}/queue/coverage", the_gui=_the_song())
    assert ma == 200
    d = json.loads(than)["data"]
    assert d["muc_pct"] == "90"
    assert isinstance(d["theo_tien_te"], list)
    # ⛔ ⛔ Khong co khoa nao ten "tong"/"total" — cong hai don vi tien te ra mot
    # con so la vo nghia, va neu cua tra mot con so tong thi cho nao doc no
    # cung se dung.
    assert not ({"tong", "total"} & set(d))
    for r in d["theo_tien_te"]:
        assert set(r) >= {"curr", "so_dong_cho", "tien_cho", "so_dong_phu",
                          "pct_that", "so_dong_trong_danh_sach", "pct_dong"}
        # ⭐ Tien ra JSON la CHUOI (`bao.py`) — ⛔ khong bao gio `float`.
        assert isinstance(r["tien_cho"], str)


def test_do_phu_nhan_muc_pct_khac(may):
    ma, _, than = _goi(may, f"{V}/queue/coverage?muc_pct=50",
                       the_gui=_the_song())
    assert ma == 200 and json.loads(than)["data"]["muc_pct"] == "50"


@pytest.mark.parametrize("muc", ["0", "-5", "101", "abc", "9e9999"])
def test_muc_pct_la_thi_400_chu_KHONG_am_tham_quay_ve_90(may, muc):
    """⛔ Tra so cua 90 cho mot cau hoi khac la doi cau hoi ma ⛔ khong ai biet."""
    ma, _, than = _goi(may, f"{V}/queue/coverage?muc_pct={muc}",
                       the_gui=_the_song())
    assert ma == 400, f"muc_pct={muc} phai bi tu choi"
    assert json.loads(than)["error"]["code"] == "FLS-BAD-REQUEST"


def test_do_phu_van_doi_THE(may):
    ma, _, _ = _goi(may, f"{V}/queue/coverage")
    assert ma == 401
