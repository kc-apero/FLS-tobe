# -*- coding: utf-8 -*-
"""`C9` — `GET /api/fls/v1/config/ven` qua MÁY THẬT + cổng bảng tuyến
*(ISP 3.1.2 · Step 21 · `WO-172`)*. 42 dòng Block 1 đọc từ KHO, ⛔ gõ cứng."""
from __future__ import annotations

from collections import Counter
import contextlib
import http.client
import json
import os
import threading
import time
from pathlib import Path

import pytest

import psycopg

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.api.xu_ly import HAM
from fls.cau_hinh import vendor
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c9-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/ven"
BANG_KHO = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
NGUON = "bai-test-c9:ISP-3.1.2-Step21"
KHOA_DATA = {"bang", "nguon", "so_dong", "dong", "nhan_rieng", "cdt1"}
ANH = GOC / "tests" / "fixture" / "cau_hinh" / "ix_ven.json"
ANH_CDT = GOC / "tests" / "fixture" / "cau_hinh" / "cdt_correct.json"


@pytest.fixture(scope="module", autouse=True)
def _nap():
    """Nạp `IX.VEN` vào kho TEST từ ảnh DT8 *(⛔ gõ cứng ở mã)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(ANH), duong_cdt1=str(ANH_CDT), actor="bo-test-c9", nguon=NGUON)
    yield


@pytest.fixture(scope="module")
def may():
    """Máy THẬT trên cổng hệ điều hành chọn, kết nối CHỈ ĐỌC vào kho TEST.

    ⚠ Tuyến này ⛔ chạm kho, nhưng `cua.dung_may` **đòi** một đường đọc bị PostgreSQL
      chặn ghi và cửa mở kết nối cho MỌI tuyến ⇒ bài cần PG thật *(⛔ mock kho)*.
    """
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
def test_C9_GET_config_ven_200_42_dong_5_nhan_7_cdt1_TU_KHO(may):
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r
    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.VEN" and d["nguon"] == NGUON
    assert d["so_dong"] == len(d["dong"]) == 359           # DT9b: 4 sổ — GI 42 · OMC 89 · SC 93 · PS 135
    assert Counter(x["so"] for x in d["dong"]) == {"GI": 42, "OMC": 89, "SC": 93, "PS": 135}
    assert d["nhan_rieng"] == ["Max", "VD341", "VD428", "VD444", "VD62"], d["nhan_rieng"]
    assert len(d["cdt1"]) == 7, d["cdt1"]
    assert {x["cach_tinh"] for x in d["dong"]} == set(d["nhan_rieng"]) | {"thường"}
    d0 = d["dong"][0]
    assert d0 == {"thu_tu": 1, "dong_sheet": "4", "No": "1", "vendor": "VD341",
                  "network": "Admob", "account": "Admob Trananhlinh", "pct": "1",
                  "cashin_month": 1, "cashin_day": 23, "cach_tinh": "VD341",
                  "so": "GI"}, d0                                   # DT9b: CHỈ THÊM trường `so`
    assert r["meta"]["data_status"] == "flash" and r["meta"]["run_id"] is None, r["meta"]


@pytest.mark.pg
def test_C9_tuyen_doc_TU_KHO_khong_go_cung(may):
    """Nạp THÊM bản khác *(nguồn lạ)* ⇒ tuyến trả đúng bản mới nhất; cuối bài nạp lại ảnh."""
    nguon_la = NGUON + ":nguon-la"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_ven(c, str(ANH), duong_cdt1=str(ANH_CDT), actor="bo-test-c9",
                       nguon=nguon_la)
    try:
        ma, r = _goi(may, DUONG)
        assert ma == 200 and r["data"]["nguon"] == nguon_la, (ma, r)
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as c:
            chc.nap_ix_ven(c, str(ANH), duong_cdt1=str(ANH_CDT), actor="bo-test-c9",
                           nguon=NGUON)


@pytest.mark.pg
def test_C9_run_id_thi_400_khuon_C1(may):
    ma, r = _goi(may, f"{DUONG}?run_id=NAP-2026-01-01-X")
    assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (ma, r)


@pytest.mark.pg
def test_C9_khong_the_401_va_POST_405(may):
    ma, r = _goi(may, DUONG, co_the=False)
    assert ma == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED", (ma, r)
    ma, r = _goi(may, DUONG, phuong_thuc="POST")
    assert ma == 405 and r["error"]["code"] == "FLS-METHOD", (ma, r)


def test_C9_bang_tuyen_khai_MOT_tuyen_KHO_chi_doc_va_soi_XANH():
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
    assert any(v.startswith("fls.repo.cau_hinh_repo.") for v in x[0]["vet"]), x[0]["vet"]


def _nem(exc):
    def _f(_conn):
        raise exc
    return _f


@pytest.mark.parametrize("exc,ma,http_", [
    (chc.ChuaKhai("kho rong"), "FLS-CAUHINH-CHUA-KHAI", 409),
    (chc.BangLa("nguon la"), "FLS-CAUHINH-BANG-LA", 404),
    (chc.BanHong("ban hong"), "FLS-CAUHINH-BAN-HONG", 500),
])
def test_C9_handler_cau_hinh_ven_dich_loi_CO_TEN(monkeypatch, exc, ma, http_):
    from fls.api import bao, xu_ly
    monkeypatch.setattr(chc, "doc_ven", _nem(exc))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.cau_hinh_ven(_yc())
    assert e.value.ma == ma and bao.MA_LOI[ma][0] == http_
