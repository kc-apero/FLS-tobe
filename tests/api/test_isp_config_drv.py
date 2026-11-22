# -*- coding: utf-8 -*-
"""`C10` — `GET /api/fls/v1/config/drv` qua MÁY THẬT + cổng bảng tuyến *(ISP 3.1.2 · Step 29 ·
`WO-295`)*. Luật đọc từ KHO, ⛔ gõ cứng; cờ `bat` luôn `false` *(D2)*; ⛔ tuyến bật cờ."""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
from pathlib import Path

import psycopg
import pytest

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.api.xu_ly import HAM
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c10-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/drv"
BANG_KHO = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
NGUON = "bai-test-c11:ISP-3.1.2-Step25"
KHOA_DATA = {"bang", "nguon", "so_o_so", "so_o_thieu", "loai", "cdt1", "luoi", "o_thieu",
             "o_thieu_theo_ly_do", "nb_le_so_dong"}
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "ix_drv.json"


@pytest.fixture(scope="module", autouse=True)
def _nap():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_drv(c, str(ANH_MM), actor="bo-test-c11", nguon=NGUON)
    yield


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


def _the_song(giay: int = 300) -> str:
    return the.dong_the({"sub": "ke.toan.thu@vi-du.invalid",
                         "exp": int(time.time()) + giay, "vai": ["ke_toan"]},
                        KHOA.encode())


def _goi(may, duong: str, *, phuong_thuc: str = "GET",
         co_the: bool = True) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {"Authorization": f"Bearer {_the_song()}"} if co_the else {}
    try:
        c.request(phuong_thuc, duong, headers=de)
        r = c.getresponse()
        than = r.read()
        return r.status, json.loads(than) if than else {}
    finally:
        c.close()


def _yc():
    from fls.api import xu_ly
    return xu_ly.YeuCau(conn=None, pv=xu_ly.pham_vi_cua_yeu_cau({}), q={}, tham={})



@pytest.mark.pg
def test_C10_GET_config_drv_200_238_so_146_thieu_TU_KHO(may):
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r
    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.DRV" and d["nguon"] == NGUON
    assert d["so_o_so"] == 238 and d["so_o_thieu"] == 146 and d["nb_le_so_dong"] == 304
    assert sorted(d["o_thieu_theo_ly_do"].values()) == [14, 36, 96], d["o_thieu_theo_ly_do"]
    assert len(d["luoi"]) == 21 and r["meta"]["data_status"] == "flash"
    noem = [x for x in d["luoi"] if (x["loai"], x["cdt1"]) == ("NOEM", "SHQ1")][0]
    assert noem["thang"]["202503"] > 0


@pytest.mark.pg
def test_C10_loc_loai_ky_va_tham_so_hong_400(may):
    ma, r = _goi(may, f"{DUONG}?loai=NOEM&ky=202503")
    d = r["data"]
    assert ma == 200 and len(d["luoi"]) == 7 and d["so_o_so"] == 7 and d["so_o_thieu"] == 1, d["so_o_thieu"]
    assert d["o_thieu"][0]["cdt1"] == "CMN" and d["o_thieu"][0]["thang"] == 202503
    for q in ("loai=XX", "ky=202513", "ky=abc"):
        ma, r = _goi(may, f"{DUONG}?{q}")
        assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (q, ma)


@pytest.mark.pg
def test_C10_run_id_thi_400_khuon_C1(may):
    ma, r = _goi(may, f"{DUONG}?run_id=NAP-2026-01-01-X")
    assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (ma, r)


@pytest.mark.pg
def test_C10_tuyen_doc_TU_KHO_khong_go_cung(may):
    nguon_la = NGUON + ":nguon-la"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_drv(c, str(ANH_MM), actor="bo-test-c10", nguon=nguon_la)
    try:
        ma, r = _goi(may, DUONG)
        assert ma == 200 and r["data"]["nguon"] == nguon_la, (ma, r)
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as c:
            chc.nap_ix_drv(c, str(ANH_MM), actor="bo-test-c10", nguon=NGUON)


@pytest.mark.pg
def test_C10_khong_the_401_POST_405_va_KHONG_co_tuyen_ghi(may):
    ma, r = _goi(may, DUONG, co_the=False)
    assert ma == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED", (ma, r)
    for pt in ("POST", "PUT", "PATCH", "DELETE"):
        ma, r = _goi(may, DUONG, phuong_thuc=pt)
        assert ma == 405 and r["error"]["code"] == "FLS-METHOD", (pt, ma, r)
    assert [(t.phuong_thuc, t.duong) for t in bt.BANG_TUYEN if "/drv" in t.duong] == [("GET", DUONG)]


def test_C10_bang_tuyen_khai_MOT_tuyen_KHO_chi_doc_va_soi_XANH():
    ds = [t for t in bt.BANG_TUYEN if t.duong == DUONG]
    assert len(ds) == 1, f"⛔ mong đúng 1 tuyến {DUONG}, đo {len(ds)}"
    t = ds[0]
    assert t.phuong_thuc == "GET" and not t.ghi and t.bang_ghi == ()
    assert tuple(t.bang) == BANG_KHO and t.nguon_tinh == (), (t.bang, t.nguon_tinh)
    assert t.ham in HAM and bt.kiem_bang_tuyen() == []
    loi, do = sbt.soi()
    assert loi == [], "⛔ bản khai lệch SQL:\n  - " + "\n  - ".join(loi)
    x = [x for x in do if x["duong"] == DUONG]
    assert len(x) == 1 and x[0]["that"] == sorted(BANG_KHO), x


def _nem(exc):
    def _f(_conn):
        raise exc
    return _f


@pytest.mark.parametrize("exc,ma,http_", [
    (chc.ChuaKhai("kho rong"), "FLS-CAUHINH-CHUA-KHAI", 409),
    (chc.BangLa("nguon la"), "FLS-CAUHINH-BANG-LA", 404),
    (chc.BanHong("ban hong"), "FLS-CAUHINH-BAN-HONG", 500),
])
def test_C10_handler_cau_hinh_drv_dich_loi_CO_TEN(monkeypatch, exc, ma, http_):
    from fls.api import bao, xu_ly
    monkeypatch.setattr(chc, "doc_drv", _nem(exc))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.cau_hinh_drv(_yc())
    assert e.value.ma == ma and bao.MA_LOI[ma][0] == http_
