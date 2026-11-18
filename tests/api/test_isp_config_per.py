# -*- coding: utf-8 -*-
"""`C6-B4` — `GET /api/fls/v1/config/per` qua MÁY THẬT + cổng bảng tuyến
*(ISP 3.1.2 · Step 17 · `WO-152`)*. Ngày đầu + luật đọc từ KHO, ⛔ gõ cứng."""
from __future__ import annotations

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
from fls.cau_hinh import ky
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c6-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/per"
BANG_KHO = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
NGUON = "bai-test-c6:ISP-3.1.2-Step17"
KHOA_DATA = {"bang", "nguon", "ngay_dau", "ky_dau", "luat", "luat_chua_ky"}


@pytest.fixture(scope="module", autouse=True)
def _nap():
    """Nạp `IX.PER` vào kho TEST *(ngày đầu = DỮ LIỆU của bài, ⛔ gõ cứng ở mã)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bo-test-c6", ngay_dau="2024-10-21", luat="A",
                       nguon=NGUON)
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


# ── AC-4 · qua HTTP ───────────────────────────────────────────────────────
@pytest.mark.pg
def test_C6_B4_GET_config_per_200_ngay_dau_va_luat_A_TU_KHO(may):
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r
    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.PER" and d["nguon"] == NGUON
    assert d["ngay_dau"] == "2024-10-21", d["ngay_dau"]
    assert d["luat"] == {"ma": "A", "ten": ky.TEN_LUAT["A"]}, d["luat"]
    assert d["luat_chua_ky"] == ["B"], d["luat_chua_ky"]
    assert d["ky_dau"] == {"nam": 2024, "nua": 2, "quy": 4, "thang": 10}, d["ky_dau"]
    assert r["meta"]["data_status"] == "flash" and r["meta"]["run_id"] is None, r["meta"]


@pytest.mark.pg
def test_C6_R1_02_tuyen_doc_ngay_la_TU_KHO_khong_go_cung(may):
    """`C6-R1-02` *(Đ5)*: nạp THÊM bản ngày LẠ `2024-10-20` ⇒ tuyến trả đúng ngày lạ.
    Gõ cứng ngày ở handler *(M7)* ⇒ ĐỎ. Cuối bài nạp lại `2024-10-21` *(chỉ-THÊM ⇒ bản mới
    nhất lại là 21)* để bài khác trong tệp không bị lệch."""
    nguon_la = NGUON + ":ngay-la"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_per(c, actor="bo-test-c6", ngay_dau="2024-10-20", luat="A",
                       nguon=nguon_la)
    try:
        ma, r = _goi(may, DUONG)
        assert ma == 200, (ma, r)
        d = r["data"]
        assert d["ngay_dau"] == "2024-10-20" and d["nguon"] == nguon_la, d
        assert d["ky_dau"] == {"nam": 2024, "nua": 2, "quy": 4, "thang": 10}, d["ky_dau"]
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as c:
            chc.nap_ix_per(c, actor="bo-test-c6", ngay_dau="2024-10-21", luat="A",
                           nguon=NGUON)
    ma, r = _goi(may, DUONG)
    assert ma == 200 and r["data"]["ngay_dau"] == "2024-10-21", (ma, r)


def test_C6_R1_02_handler_luat_la_TU_KHO_khong_go_cung_A(monkeypatch):
    """`C6-R1-02` *(M8)*: kho khai luật khác `A` ⇒ `luat.ma` phải theo kho. Luật thứ hai
    chưa có thật ⇒ mở tạm một mã trong `TEN_LUAT` *(monkeypatch, tự trả)*."""
    from datetime import date
    from fls.api import xu_ly
    monkeypatch.setitem(ky.TEN_LUAT, "Z", "luat gia cho bai")
    monkeypatch.setattr(chc, "doc_per", lambda _c: ky.LichKy(
        nguon="n", ngay_dau=date(2031, 2, 3), luat="Z"))
    d, _ = xu_ly.cau_hinh_per(_yc())
    assert d["luat"] == {"ma": "Z", "ten": "luat gia cho bai"}, d["luat"]
    assert d["ngay_dau"] == "2031-02-03" and d["ky_dau"]["quy"] == 1, d


@pytest.mark.pg
def test_C6_B4_run_id_thi_400_khuon_C1(may):
    ma, r = _goi(may, f"{DUONG}?run_id=NAP-2026-01-01-X")
    assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (ma, r)
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)


@pytest.mark.pg
def test_C6_B4_khong_the_401_va_POST_405(may):
    ma, r = _goi(may, DUONG, co_the=False)
    assert ma == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED", (ma, r)
    ma, r = _goi(may, DUONG, phuong_thuc="POST")
    assert ma == 405 and r["error"]["code"] == "FLS-METHOD", (ma, r)


def test_C6_B4_bang_tuyen_khai_MOT_tuyen_KHO_chi_doc_va_soi_XANH():
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


# ── kho RỖNG / bản hỏng / luật chưa mở ⇒ lỗi CÓ TÊN ─────────────────────────
def _nem(exc):
    def _f(_conn):
        raise exc
    return _f


def _yc():
    from fls.api import xu_ly
    return xu_ly.YeuCau(conn=None, pv=xu_ly.pham_vi_cua_yeu_cau({}), q={}, tham={})


@pytest.mark.parametrize("exc,ma,http_", [
    (chc.ChuaKhai("kho rong"), "FLS-CAUHINH-CHUA-KHAI", 409),
    (chc.BangLa("nguon la"), "FLS-CAUHINH-BANG-LA", 404),
    (chc.BanHong("ban hong"), "FLS-CAUHINH-BAN-HONG", 500),
])
def test_C6_AC4_handler_cau_hinh_per_dich_loi_CO_TEN(monkeypatch, exc, ma, http_):
    from fls.api import bao, xu_ly
    monkeypatch.setattr(chc, "doc_per", _nem(exc))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.cau_hinh_per(_yc())
    assert e.value.ma == ma and bao.MA_LOI[ma][0] == http_


def test_C6_AC4_handler_luat_chua_ky_dich_loi_CO_TEN(monkeypatch):
    from fls.api import bao, xu_ly
    monkeypatch.setattr(chc, "doc_per", _nem(ky.LoiKy(ky.LUAT_CHUA_KY, "luat B chua mo")))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.cau_hinh_per(_yc())
    assert e.value.ma == "FLS-CAUHINH-LUAT-CHUA-KY" and e.value.ma in bao.MA_LOI
    assert "LUAT_CHUA_KY" in e.value.chi_tiet
