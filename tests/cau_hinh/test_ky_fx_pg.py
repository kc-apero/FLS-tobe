# -*- coding: utf-8 -*-
"""`C7` *(`WO-212`, ISP 3.1.2 · Step 33)* — `IX.FX` **ký tháng** + `fx_cua` CHẶN *(D1)*.

C7-B1…B6 qua MÁY THẬT + kho TEST *(⛔ mock kho)*. Kho chỉ-thêm ⇒ ⛔ dọn được, nên mỗi
lần chạy nạp một bản `IX.FX` mà **tỷ giá USD mọi tháng là số NGẪU NHIÊN** — dấu vân
tháng đổi ⇒ lần chạy sau thấy mọi tháng *chưa ký* *(bài chạy lại được, ⛔ cạn tháng)*.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
import uuid
from decimal import Decimal
from pathlib import Path

import psycopg
import pytest

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.cau_hinh import fx
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c7-dai-hon-ba-muoi-hai-ky-tu-ok"
V = bt.TIEN_TO
ANH = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"
BANG_KY = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")


def _the(sub: str = "ke.toan.c7@vi-du.invalid") -> str:
    return the.dong_the({"sub": sub, "exp": int(time.time()) + 300,
                         "vai": ["ke_toan"]}, KHOA.encode())


@pytest.fixture(scope="module", autouse=True)
def _nap(tmp_path_factory):
    """Nạp `IX.FX` với USD NGẪU NHIÊN mỗi tháng ⇒ dấu vân tháng MỚI mỗi lần chạy."""
    anh = json.loads(ANH.read_text(encoding="utf-8"))
    for r in anh["dong"]:
        r["USD"] = str(10000 + uuid.uuid4().int % 90000)
    p = tmp_path_factory.mktemp("c7") / "ix_fx_c7.json"
    p.write_text(json.dumps(anh), encoding="utf-8")
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_fx(c, str(p), actor="bo-test-c7", thang_dau=202401,
                      nguon="tests/cau_hinh/test_ky_fx_pg.py")
    yield


@pytest.fixture(scope="module")
def may():
    @contextlib.contextmanager
    def mo_doc():
        c = noi_chi_doc(dsn_test())
        try:
            yield c
        finally:
            c.close()

    @contextlib.contextmanager
    def mo_ghi():
        c = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield c
        finally:
            c.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    m = cua.dung_may(mo_doc, cong=0, mo_ghi=mo_ghi)
    threading.Thread(target=m.serve_forever, daemon=True).start()
    yield m
    m.shutdown()
    m.server_close()
    if cu is None:
        os.environ.pop(the.BIEN_KHOA, None)
    else:
        os.environ[the.BIEN_KHOA] = cu


def _goi(may, duong, *, pt="GET", than=None, the_=True, tok=None):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {}
    if the_:
        de["Authorization"] = f"Bearer {tok or _the()}"
    b = None
    if than is not None:
        b = json.dumps(than)
        de["Content-Type"] = "application/json"
    try:
        c.request(pt, duong, body=b, headers=de)
        r = c.getresponse()
        raw = r.read()
        return r.status, json.loads(raw) if raw else {}
    finally:
        c.close()


def _ky(may, thang, **kw):
    return _goi(may, f"{V}/config/fx/{thang}/sign", pt="POST", than=kw.pop("than", {}),
                **kw)


def _dong(may, thang):
    st, r = _goi(may, f"{V}/config/fx")
    assert st == 200, r
    return next(d for d in r["data"]["ky"] if d["yyyymm"] == int(thang))


def _so_ban_ky() -> int:
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang = %s",
                    (chc.BANG_KY_FX,))
        return cur.fetchone()[0]


# ── C7-B1 ──────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C7_B1_ky_thang_201_va_GET_thay_da_ky_voi_actor_tu_THE(may):
    assert _dong(may, 202510)["trang_thai"] == "chua_ky"      # mẫu số: có tháng, chưa ký
    st, r = _ky(may, 202510)
    assert st == 201, r
    assert r["error"] is None and r["data"]["yyyymm"] == 202510
    d = _dong(may, 202510)
    assert d["trang_thai"] == "da_ky"
    assert d["actor"] == "ke.toan.c7@vi-du.invalid"
    assert d["ky_luc"]                                          # máy đặt, không rỗng
    # tháng KHÁC không bị niêm phong lây
    assert _dong(may, 202509)["trang_thai"] == "chua_ky"


# ── C7-B2 ──────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C7_B2_ky_lai_409_co_ten_va_kho_KHONG_them_dong(may):
    assert _ky(may, 202508)[0] == 201
    truoc = _so_ban_ky()
    assert truoc >= 1                                           # Đ3: mẫu số ≠ 0
    st, r = _ky(may, 202508, tok=_the("nguoi.khac@vi-du.invalid"))
    assert st == 409 and r["error"]["code"] == "FLS-CAUHINH-DA-KY", r
    assert "202508" in r["error"]["detail"]
    assert _so_ban_ky() == truoc
    assert _dong(may, 202508)["actor"] == "ke.toan.c7@vi-du.invalid"   # người đầu giữ


# ── C7-B3 ──────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C7_B3_fx_cua_CHAN_chua_ky_va_THIEU_han_va_hong():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        with pytest.raises(fx.FxChan) as e:
            chc.fx_cua(c, "202511")                             # có trong IX.FX, chưa ký
        assert e.value.ma == "FX_CHAN" and "202511" in str(e.value)
        with pytest.raises(fx.FxChan) as e2:
            chc.fx_cua(c, "209901")                             # THIẾU hẳn — ⛔ rơi gần nhất
        assert "209901" in str(e2.value)
        with pytest.raises(fx.LoiFX):
            chc.fx_cua(c, "2025-11")                            # yyyymm hỏng ⇒ lỗi có tên
        chc.ky_fx(c, "202511", actor="ai.do@vi-du.invalid")
        t = chc.fx_cua(c, "202511")                             # ký rồi ⇒ trả tỷ giá
        assert set(t) == set(fx.TIEN_TE) and t["VND"] == Decimal(1)
    # ⛔ tháng ngoài IX.FX không ký được
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        with pytest.raises(chc.ThangKhongCo):
            chc.ky_fx(c, "209901", actor="ai.do@vi-du.invalid")


def test_C7_B3_fx_cua_thuan_ky_roi_nhung_TY_GIA_DOI_thi_van_chan():
    ky = tuple(fx.DongFX(m, {**{t: Decimal(1) for t in fx.TIEN_TE}, "USD": Decimal(u)})
               for m, u in ((202510, 25000), (202512, 26000)))
    b = fx.BangFX(nguon="t", ky=ky, thieu=(202511,), trung=(), lac=())
    da_ky = {202510: fx.dau_van_tay(ky[0]), 202512: "dau-cu-khong-khop"}
    assert fx.fx_cua("202510", b, da_ky)["USD"] == Decimal(25000)
    with pytest.raises(fx.FxChan, match="202512"):              # ký rồi, số đổi sau ký
        fx.fx_cua(202512, b, da_ky)
    with pytest.raises(fx.FxChan, match="202511"):              # nằm trong `thieu`
        fx.fx_cua(202511, b, da_ky)
    with pytest.raises(fx.LoiFX):
        fx.fx_cua(True, b, da_ky)


# ── C7-B4 ──────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C7_B4_actor_CHI_tu_the_than_khong_gia_duoc(may):
    truoc = _so_ban_ky()
    # cửa sẵn có TỪ CHỐI `actor` trong thân (400) — ⛔ im lặng bỏ qua; kho ⛔ thêm dòng.
    st, r = _ky(may, 202506, than={"actor": "ke.toan.gia@vi-du.invalid"})
    assert st == 400 and _so_ban_ky() == truoc, (st, r)
    assert _dong(may, 202506)["trang_thai"] == "chua_ky"
    # trường khác trong thân (người ký · mốc) bị BỎ QUA — chữ ký vẫn là của token.
    st, r = _ky(may, 202506, than={"nguoi_ky": "gia", "ky_luc": "2000-01-01T00:00:00Z"})
    assert st == 201, r
    d = _dong(may, 202506)
    assert d["actor"] == "ke.toan.c7@vi-du.invalid"
    assert not d["ky_luc"].startswith("2000-")


# ── C7-B5 ──────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C7_B5_khong_the_hoac_the_hong_401_tu_cua_san_co(may):
    truoc = _so_ban_ky()
    # ⚠ cửa trả 401 TRƯỚC khi đọc thân ⇒ gửi KHÔNG thân *(gửi thân thì máy đóng kết nối
    #   giữa chừng — hành vi sẵn có của cửa, ⛔ lỗi C7)*.
    duong = f"{V}/config/fx/202507/sign"
    st, r = _goi(may, duong, pt="POST", the_=False)
    assert st == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED"
    st, r = _goi(may, duong, pt="POST", tok="rac.rac.rac")
    assert st == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED"
    assert _so_ban_ky() == truoc


@pytest.mark.pg
def test_C7_yyyymm_hong_400_thang_la_404(may):
    st, r = _ky(may, "2025-10")
    assert st == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", r
    st, r = _ky(may, 209901)
    assert st == 404 and r["error"]["code"] == "FLS-NOT-FOUND", r


# ── C7-B6 ──────────────────────────────────────────────────────────────────
def test_C7_B6_bang_tuyen_POST_khai_bang_ghi_va_KHONG_cham_fls_itl():
    t = next(x for x in bt.BANG_TUYEN
             if x.phuong_thuc == "POST" and x.duong == f"{V}/config/fx/{{yyyymm}}/sign")
    assert t.ghi is True and t.http_ok == 201
    assert t.bang_ghi == BANG_KY and "fls_itl" not in t.bang
    assert not bt.kiem_bang_tuyen() if hasattr(bt, "kiem_bang_tuyen") else True


@pytest.mark.pg
def test_C7_B6_kho_chi_them_trigger_0027_giu():
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        for sql in ("UPDATE fls_cau_hinh_ban SET actor = 'x'",
                    "DELETE FROM fls_cau_hinh_ban"):
            with pytest.raises(psycopg.Error, match="INV-I08"):
                cur.execute(sql)
