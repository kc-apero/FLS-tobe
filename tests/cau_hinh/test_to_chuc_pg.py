# -*- coding: utf-8 -*-
"""`C8-B2` — CDT lạ ⇒ sự kiện hàng chờ `CDT_LA` thấy ở `GET /queue` *(PG THẬT)*.

⛔ Kho config chỉ-thêm ⇒ bài đo **mức tăng** *(khuôn `test_kho_cau_hinh_pg`)*.
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
from pathlib import Path

import psycopg
import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chr

pytestmark = pytest.mark.pg

ANH = Path(__file__).resolve().parents[2] / "tests" / "fixture" / "cau_hinh"
KHOA = "khoa-thu-cua-C8-to-chuc-dai-hon-ba-muoi-hai-ky-tu-that"
V = cua.bang_tuyen.TIEN_TO


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


@pytest.fixture()
def itl(conn):
    """Một dòng sổ UNMAPPED trong một lần chạy riêng."""
    run = "NAP-2000-03-01-C8" + uuid.uuid4().hex[:6].upper()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                    " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version, mapping_version,"
            " raw_frozen, canon, doc_no, curr, ps_co, work_status) VALUES "
            "(%s,'RAW','L1',801,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,%s,'VND',%s,"
            "'UNMAPPED') RETURNING itl_id",
            (uuid.uuid4().hex, run, "REF-C8-" + uuid.uuid4().hex[:5], D(1_000_000)))
        return run, cur.fetchone()[0]


def _nap(conn):
    return chr.nap_ix_org(conn, str(ANH / "cdt_correct.json"),
                          str(ANH / "mapping_master_cfg.json"), actor="c8@test")


def _dem(conn, itl_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_queue_event WHERE itl_id=%s"
                    " AND evt_type='CDT_LA'", (itl_id,))
        return cur.fetchone()[0]


@pytest.fixture()
def may():
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    @contextlib.contextmanager
    def doc():
        c = noi_chi_doc(dsn_test())
        try:
            yield c
        finally:
            c.close()

    @contextlib.contextmanager
    def ghi():
        c = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield c
        finally:
            c.close()
    m = cua.dung_may(doc, cong=0, mo_ghi=ghi)
    threading.Thread(target=m.serve_forever, daemon=True).start()
    try:
        yield m
    finally:
        m.shutdown()
        m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


def _queue(may, run):
    c = http.client.HTTPConnection(*may.server_address, timeout=20)
    de = {"Authorization": "Bearer " + the.dong_the(
        {"sub": "ke.toan@apero.vn", "exp": int(time.time()) + 300}, KHOA.encode())}
    try:
        c.request("GET", f"{V}/queue?run_id={run}&limit=100", headers=de)
        r = c.getresponse()
        return r.status, json.loads(r.read())["data"]
    finally:
        c.close()


def test_C8_B2_CDT_la_ghi_DUNG_MOT_su_kien_va_thay_o_queue(conn, itl, may):
    run, itl_id = itl
    _nap(conn)
    r = chr.cdt_cua_ghi(conn, itl_id, "XYZ", actor="c8@test")
    assert r.la is True and r.cdt1 is None            # ⛔ SHQ2
    assert _dem(conn, itl_id) == 1
    s, d = _queue(may, run)
    assert s == 200
    dong = [x for x in d["rows"] if x["itl_id"] == itl_id]
    assert len(dong) == 1                              # Đ3: tập KHÔNG rỗng
    assert "XYZ" in (dong[0]["cdt_la"] or "")


def test_C8_B1_CDT_biet_thi_0_su_kien(conn, itl):
    _, itl_id = itl
    _nap(conn)
    r = chr.cdt_cua_ghi(conn, itl_id, "SHQ2_Headquarters2", actor="c8@test")
    assert (r.cdt1, r.la) == ("SHQ2 | Headquarters2", False)
    assert _dem(conn, itl_id) == 0


def test_CDT_la_hai_lan_van_MOT_su_kien(conn, itl):
    _, itl_id = itl
    _nap(conn)
    chr.cdt_cua_ghi(conn, itl_id, "XYZ", actor="c8@test")
    chr.cdt_cua_ghi(conn, itl_id, "XYZ", actor="c8@test")
    assert _dem(conn, itl_id) == 1


def test_dong_KHONG_la_khong_co_cdt_la_o_queue(conn, itl, may):
    run, itl_id = itl
    s, d = _queue(may, run)
    dong = [x for x in d["rows"] if x["itl_id"] == itl_id]
    assert s == 200 and len(dong) == 1 and dong[0]["cdt_la"] is None


def test_kho_chua_nap_thi_ChuaKhai_KHONG_roi_SHQ2(conn, itl, monkeypatch):
    _, itl_id = itl

    def _chua(_c, _b):
        raise chr.ChuaKhai("x")
    monkeypatch.setattr(chr, "_doc_ban", _chua)
    with pytest.raises(chr.ChuaKhai):
        chr.cdt_cua_ghi(conn, itl_id, "SHQ2_Headquarters2", actor="c8@test")


def test_nap_ix_org_chi_them_va_ban_moi(conn):
    a = _nap(conn)
    b = _nap(conn)
    assert b.phien_ban == a.phien_ban + 1 and b.khong_doi is True
    ks = [k for k, _ in b.dong]
    assert sum(k.startswith("cdt:") for k in ks) == 13
    assert sum(k.startswith("tk:") for k in ks) == 59
