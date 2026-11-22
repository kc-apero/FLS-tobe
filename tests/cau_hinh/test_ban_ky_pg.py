# -*- coding: utf-8 -*-
"""`C13` *(`WO-257`, ISP 3.1.2 · Step 36)* — `IX.TMP`: bản báo cáo KÝ có phiên bản.

AC-1…AC-5 qua MÁY THẬT + kho TEST. Kho chỉ-thêm ⇒ ⛔ dọn được ⇒ mỗi bài chọn một `{ky}`
**CHƯA có bản nào** *(`_ky_moi`)* và nội dung ngẫu nhiên ⇒ chạy lại được, ⛔ cạn kỳ.
⛔ Đưa bản KHÔNG có tuyến *(§4i chỉ GET + POST sign)*: bài gọi hàm `chc.dua_ban_ky`.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import random
import threading
import time
import uuid

import psycopg
import pytest

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc

KHOA = "khoa-thu-cua-bo-test-isp-c13-dai-hon-ba-muoi-hai-ky-tu-ok"
V = bt.TIEN_TO
NGUOI = "ke.toan.c13@vi-du.invalid"


def _the(sub: str = NGUOI) -> str:
    return the.dong_the({"sub": sub, "exp": int(time.time()) + 300,
                         "vai": ["ke_toan"]}, KHOA.encode())


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


def _goi(may, duong, *, pt="GET", than=None, the_=True):
    c = http.client.HTTPConnection(*may.server_address, timeout=10)
    de = {}
    if the_:
        de["Authorization"] = f"Bearer {_the()}"
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


def _get(may, ky):
    return _goi(may, f"{V}/report/snapshot/{ky}")


def _ky(may, ky, **than):
    return _goi(may, f"{V}/report/snapshot/{ky}/sign", pt="POST", than=than)


def _conn():
    return psycopg.connect(dsn_test(), autocommit=True)


def _ky_moi() -> int:
    """Một `yyyymm` hợp lệ mà kho TEST chưa có bản nào (Đ3: mẫu số được kiểm)."""
    with _conn() as c:
        for _ in range(200):
            k = random.randint(2000, 2099) * 100 + random.randint(1, 12)
            if not chc.doc_ban_ky(c, k):
                return k
    raise AssertionError("hết kỳ trống ở kho test")


def _noi_dung(**khac) -> dict:
    return {"ky": "x", "o": {"A1": uuid.uuid4().hex, "B2": 12.5, "C3": None}, **khac}


# ── AC-1 · C13-B1 ────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C13_B1_dua_ban_roi_ky_201_va_GET_thay_phien_ban_1_da_ky_nguoi_ky_tu_THE(may):
    ky = _ky_moi()
    st, r = _get(may, ky)
    assert st == 200 and r["data"]["ban"] == []                 # mẫu số: kỳ có, chưa bản
    with _conn() as c:
        b = chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
    assert b.phien_ban == 1 and b.trang_thai == "chua_ky"
    st, r = _ky(may, ky)
    assert st == 201, r
    d = r["data"]
    assert d["ky"] == ky and d["phien_ban"] == 1 and d["trang_thai"] == "da_ky"
    assert d["actor"] == NGUOI
    st, r = _get(may, ky)
    assert st == 200
    ds = r["data"]["ban"]
    assert len(ds) == 1
    v1 = ds[0]
    assert v1["phien_ban"] == 1 and v1["trang_thai"] == "da_ky"
    assert len(v1["checksum"]) == 64 and v1["checksum"] == b.checksum
    assert v1["actor"] == NGUOI and v1["ky_luc"]                # người ký TỪ THẺ, mốc do máy


# ── AC-2 · C13-B2 ────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C13_B2_ban_moi_khac_MOT_o_thanh_phien_ban_2_chua_ky_va_phien_ban_1_giu_NGUYEN(may):
    ky = _ky_moi()
    nd1 = _noi_dung()
    with _conn() as c:
        chc.dua_ban_ky(c, ky, nd1, actor="engine.h14")
    assert _ky(may, ky)[0] == 201
    with _conn() as c:
        truoc = chc.doc_ban_ky(c, ky)
        nd_truoc = chc.doc_noi_dung_ban_ky(c, ky, 1)
        nd2 = json.loads(json.dumps(nd1))
        nd2["o"]["B2"] = 12.6                                    # đổi ĐÚNG một ô
        b2 = chc.dua_ban_ky(c, ky, nd2, actor="engine.h14")
        sau = chc.doc_ban_ky(c, ky)
        nd_sau = chc.doc_noi_dung_ban_ky(c, ky, 1)
    assert b2.phien_ban == 2 and b2.trang_thai == "chua_ky" and not b2.khong_doi
    assert len(truoc) == 1 and len(sau) == 2
    assert sau[0] == truoc[0]                                    # checksum · người ký · mốc ký
    assert json.dumps(nd_sau, sort_keys=True) == json.dumps(nd_truoc, sort_keys=True)
    assert sau[1].checksum != sau[0].checksum
    st, r = _get(may, ky)
    assert [x["trang_thai"] for x in r["data"]["ban"]] == ["da_ky", "chua_ky"]
    assert "actor" not in r["data"]["ban"][1]                    # chưa ký ⛔ người ký


# ── AC-3 ─────────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C13_AC3_ban_TRUNG_checksum_ban_moi_nhat_KHONG_sinh_phien_ban():
    ky = _ky_moi()
    nd = _noi_dung()
    with _conn() as c:
        b1 = chc.dua_ban_ky(c, ky, nd, actor="engine.h14")
        so_truoc = len(chc.doc_ban_ky(c, ky))
        nd_khac_thu_tu = {k: nd[k] for k in reversed(list(nd))}  # khoá đảo thứ tự ⇒ cùng checksum
        b1b = chc.dua_ban_ky(c, ky, nd_khac_thu_tu, actor="engine.h14")
        assert so_truoc == 1 and len(chc.doc_ban_ky(c, ky)) == 1
        assert b1b.phien_ban == 1 and b1b.khong_doi and b1b.checksum == b1.checksum
        # đã ký rồi đưa lại CÙNG số ⇒ vẫn ⛔ phiên bản mới, và vẫn `da_ky`
        chc.ky_ban(c, ky, actor=NGUOI)
        b1c = chc.dua_ban_ky(c, ky, nd, actor="engine.h14")
        assert b1c.phien_ban == 1 and b1c.trang_thai == "da_ky" and b1c.khong_doi
        assert len(chc.doc_ban_ky(c, ky)) == 1
        # đổi rồi QUAY LẠI số cũ ⇒ so với bản MỚI NHẤT (khác) ⇒ sinh phiên bản 3
        nd2 = {**nd, "them": 1}
        assert chc.dua_ban_ky(c, ky, nd2, actor="engine.h14").phien_ban == 2
        assert chc.dua_ban_ky(c, ky, nd, actor="engine.h14").phien_ban == 3


def test_C13_checksum_TAT_DINH_tren_json_chuan_hoa():
    from fls.cau_hinh import ban_ky
    a = {"x": 1, "o": {"b": 2, "a": [1, 2]}}
    b = {"o": {"a": [1, 2], "b": 2}, "x": 1}
    assert ban_ky.checksum(a) == ban_ky.checksum(b) and len(ban_ky.checksum(a)) == 64
    assert ban_ky.checksum(a) != ban_ky.checksum({**a, "x": 2})
    assert ban_ky.checksum({"v": "Việt"}) == ban_ky.checksum(json.loads('{"v":"Vi\\u1ec7t"}'))
    for xau in ({}, [], "x", None, {"d": object()}):             # rỗng · không phải JSON ⇒ nổ có tên
        with pytest.raises(ban_ky.LoiBanKy):
            ban_ky.checksum(xau)


# ── AC-4 ─────────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C13_AC4_ky_lai_409_actor_trong_than_400_ky_hong_400_ky_chua_co_ban_404(may):
    ky = _ky_moi()
    # kỳ CHƯA có bản ⇒ 404 + câu
    st, r = _ky(may, ky)
    assert st == 404 and r["error"]["code"] == "FLS-NOT-FOUND", r
    assert str(ky) in r["error"]["detail"] and "chưa có bản" in r["error"]["detail"]
    with _conn() as c:
        chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
    # `actor` trong thân ⇒ 400 (cửa sẵn có), kho ⛔ thêm dòng, bản vẫn chưa ký
    st, r = _ky(may, ky, actor="ke.toan.gia@vi-du.invalid")
    assert st == 400, r
    assert _get(may, ky)[1]["data"]["ban"][0]["trang_thai"] == "chua_ky"
    assert _ky(may, ky)[0] == 201
    with _conn() as c:
        truoc = c.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang='IX.TMP'").fetchone()[0]
    assert truoc >= 2                                            # Đ3: mẫu số ≠ 0
    st, r = _ky(may, ky)                                         # phiên bản mới nhất đã ký
    assert st == 409 and r["error"]["code"] == "FLS-CAUHINH-DA-KY", r
    assert str(ky) in r["error"]["detail"] and NGUOI in r["error"]["detail"]
    with _conn() as c:
        sau = c.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang='IX.TMP'").fetchone()[0]
    assert sau == truoc
    for hong in ("2025-12", "20251", "202513", "abcdef"):
        st, r = _ky(may, hong)
        assert st == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (hong, r)
        assert _get(may, hong)[0] == 400
    st, r = _goi(may, f"{V}/report/snapshot/{ky}/sign", pt="POST", the_=False)
    assert st == 401
    assert _goi(may, f"{V}/report/snapshot/{ky}?run_id=T-abc")[0] == 400   # ⛔ phạm vi lần nạp


# ── AC-5 ─────────────────────────────────────────────────────────────────────
@pytest.mark.pg
def test_C13_AC5_chi_them_UPDATE_DELETE_dong_ban_da_ky_bi_CHAN_bang_cua_0027():
    ky = _ky_moi()
    with _conn() as c:
        chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
        chc.ky_ban(c, ky, actor=NGUOI)
        ids = [r[0] for r in c.execute(
            "SELECT ban_id FROM fls_cau_hinh_ban WHERE bang='IX.TMP' AND nguon IN (%s,%s)",
            (f"ban:{ky}", f"ky:{ky}")).fetchall()]
        assert len(ids) == 2                                      # mẫu số: 1 bản + 1 chữ ký
        for sql in ("UPDATE fls_cau_hinh_ban SET actor='gia' WHERE ban_id=%s",
                    "DELETE FROM fls_cau_hinh_ban WHERE ban_id=%s",
                    "UPDATE fls_cau_hinh_dong SET gia_tri='1'::jsonb WHERE ban_id=%s",
                    "DELETE FROM fls_cau_hinh_dong WHERE ban_id=%s"):
            for i in ids:
                with pytest.raises(psycopg.Error, match="INV-I08"):
                    c.execute(sql, (i,))
        assert [x.trang_thai for x in chc.doc_ban_ky(c, ky)] == ["da_ky"]
        # ⛔ di trú mới: bảng dùng lại là của 0027
        assert c.execute("SELECT to_regclass('fls_cau_hinh_ban') IS NOT NULL").fetchone()[0]


# ── AC-6 (khai tuyến) ────────────────────────────────────────────────────────
def test_C13_AC6_bang_tuyen_hai_tuyen_khai_dung_bang_ghi_va_KHONG_cham_fls_itl():
    g = next(x for x in bt.BANG_TUYEN
             if x.phuong_thuc == "GET" and x.duong == f"{V}/report/snapshot/{{ky}}")
    p = next(x for x in bt.BANG_TUYEN
             if x.phuong_thuc == "POST" and x.duong == f"{V}/report/snapshot/{{ky}}/sign")
    assert not g.ghi and p.ghi is True and p.http_ok == 201
    assert p.bang_ghi == ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
    assert "fls_itl" not in p.bang and "fls_itl" not in g.bang
    # ⛔ tuyến ghi THỨ BA: đưa bản là hàm, §4i chỉ có GET + POST sign
    assert [x.duong for x in bt.BANG_TUYEN if "/report/snapshot" in x.duong
            and x.phuong_thuc == "POST"] == [p.duong]


# ── `C13-R1-01` · checksum == checksum của nội dung ĐỌC LẠI từ kho ────────────
# R1 đo lệch 2/7 mẫu số: `1e22` (float → jsonb numeric → đọc ra int) và `-0.0` (→ `0.0`).
MAU_SO_R1 = (1.0, 0.1 + 0.2, 1e-7, 10 ** 30, 12.50, 1e22, -0.0)


@pytest.mark.pg
def test_C13_R1_01_checksum_bang_checksum_cua_noi_dung_DOC_LAI_tren_7_mau_so_cua_R1():
    from fls.cau_hinh import ban_ky
    assert len(MAU_SO_R1) == 7                                   # Đ3: mẫu số của phép đo
    khop = 0
    with _conn() as c:
        for x in MAU_SO_R1:
            ky = _ky_moi()
            b = chc.dua_ban_ky(c, ky, {"o": {"v": x}, "id": uuid.uuid4().hex}, actor="engine.h14")
            doc = chc.doc_noi_dung_ban_ky(c, ky, 1)
            assert ban_ky.checksum(doc) == b.checksum, (x, doc)
            khop += 1
    assert khop == 7


# ── `C13-R1-02` · ký SONG SONG: mỗi kỳ đúng 1 `201`, còn lại `409` ────────────
KY_SONG_SONG, LUONG = 5, 8


def _chay_song_song(viec, n):
    """`n` luồng cùng xuất phát (rào) ⇒ danh sách kết quả; luồng nổ ⇒ ghi lỗi (⛔ nuốt)."""
    rao, kq = threading.Barrier(n), []

    def chay(i):
        rao.wait()
        try:
            kq.append(viec(i))
        except Exception as e:                                   # noqa: BLE001
            kq.append(("LOI", repr(e)))

    ts = [threading.Thread(target=chay, args=(i,)) for i in range(n)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return kq


def _so_su_kien_ky(ky):
    with _conn() as c:
        return c.execute("SELECT count(*) FROM fls_cau_hinh_ban "
                         "WHERE bang='IX.TMP' AND nguon=%s", (f"ky:{ky}",)).fetchone()[0]


@pytest.mark.pg
def test_C13_R1_02_ky_SONG_SONG_5_ky_x_8_luong_moi_ky_dung_1_201_con_lai_409_dung_1_ban_ky(may):
    for _ in range(KY_SONG_SONG):
        ky = _ky_moi()
        with _conn() as c:
            chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
        kq = _chay_song_song(lambda i: _ky(may, ky)[0], LUONG)
        assert len(kq) == LUONG                                  # mẫu số: đủ 8 phản hồi
        assert sorted(kq) == [201] + [409] * (LUONG - 1), kq
        assert _so_su_kien_ky(ky) == 1
        ds = chc.doc_ban_ky(_conn(), ky)
        assert [(b.phien_ban, b.trang_thai) for b in ds] == [(1, "da_ky")]


@pytest.mark.pg
def test_C13_R1_02_dua_ban_SONG_SONG_cung_noi_dung_dung_1_phien_ban_va_khac_noi_dung_ra_phien_ban_lien_tuc():
    ky = _ky_moi()
    nd = _noi_dung()

    def dua(i):
        with _conn() as c:
            return chc.dua_ban_ky(c, ky, nd, actor="engine.h14").phien_ban

    kq = _chay_song_song(dua, LUONG)
    assert kq == [1] * LUONG, kq                                 # 1 bản · 7 lần `khong_doi`
    ky2 = _ky_moi()

    def dua_khac(i):
        with _conn() as c:
            return chc.dua_ban_ky(c, ky2, _noi_dung(i=i), actor="engine.h14").phien_ban

    kq = _chay_song_song(dua_khac, LUONG)
    assert sorted(kq) == list(range(1, LUONG + 1)), kq           # phiên bản KHÔNG trùng số
    with _conn() as c:
        assert [b.phien_ban for b in chc.doc_ban_ky(c, ky2)] == list(range(1, LUONG + 1))


# ── `C13-R1-02` bổ sung (`WO-299`, C13b) · giá trị TRẢ VỀ đúng bản vừa chèn/ký ──
def _chen_xen_sau_khoi_giao_dich(monkeypatch, ky):
    """Ép đua TẤT ĐỊNH: ngay lúc `dua_ban_ky`/`ky_ban` đọc `_sk_ban_ky` mà kết nối của nó
    KHÔNG còn trong giao dịch *(= SAU khối giữ khoá advisory)*, một kết nối KHÁC chèn bản
    `n+1`. Mã đọc-trong-khoá ⇒ ⛔ có điểm ấy ⇒ không bị chèn. Trả `da_chen` *(mẫu số: đếm lần chèn)*."""
    goc = chc._sk_ban_ky
    da_chen: list[int] = []

    def moc(conn, k):
        if (k == ky and not da_chen
                and conn.info.transaction_status == psycopg.pq.TransactionStatus.IDLE):
            da_chen.append(1)
            with _conn() as c2:
                chc.dua_ban_ky(c2, ky, _noi_dung(luong_khac=1), actor="engine.luong.khac")
        return goc(conn, k)

    monkeypatch.setattr(chc, "_sk_ban_ky", moc)
    return da_chen


@pytest.mark.pg
def test_C13B_AC2_dua_ban_ky_tra_DUNG_ban_vua_chen_du_luong_khac_chen_n_cong_1_ngay_sau_khoi_giao_dich(monkeypatch):
    ky = _ky_moi()
    with _conn() as c:
        a = chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")      # v1
    nd2 = _noi_dung()
    da_chen = _chen_xen_sau_khoi_giao_dich(monkeypatch, ky)
    with _conn() as c:
        b = chc.dua_ban_ky(c, ky, nd2, actor="engine.h14")
    monkeypatch.undo()
    assert a.phien_ban == 1
    assert (b.phien_ban, b.checksum) == (2, chc.ban_ky.checksum(nd2)), b   # ⛔ bản 3 của luồng khác
    if da_chen:                          # mã cũ có điểm giữa ⇒ luồng khác chèn ⇒ kho có 3 bản
        assert len(chc.doc_ban_ky(_conn(), ky)) == 3
    else:                                # mã mới đọc trong khoá ⇒ ⛔ có điểm giữa: kho 2 bản
        assert len(chc.doc_ban_ky(_conn(), ky)) == 2


@pytest.mark.pg
def test_C13B_AC1_ky_ban_tra_DUNG_ban_vua_ky_du_luong_khac_chen_n_cong_1_ngay_sau_khoi_giao_dich(monkeypatch):
    ky = _ky_moi()
    with _conn() as c:
        a = chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
    _chen_xen_sau_khoi_giao_dich(monkeypatch, ky)
    with _conn() as c:
        d = chc.ky_ban(c, ky, actor=NGUOI)
    monkeypatch.undo()
    assert (d.phien_ban, d.checksum, d.trang_thai) == (1, a.checksum, "da_ky"), d


@pytest.mark.pg
def test_C13B_AC1_dua_ban_ky_trung_checksum_van_tra_khong_doi_dung_ban():
    ky = _ky_moi()
    nd = _noi_dung()
    with _conn() as c:
        a = chc.dua_ban_ky(c, ky, nd, actor="engine.h14")
        b = chc.dua_ban_ky(c, ky, nd, actor="engine.h14")
    assert (b.phien_ban, b.checksum, b.khong_doi) == (1, a.checksum, True)


# ── `C13-R1-03` · ký phiên bản ≥ 2 ───────────────────────────────────────────
@pytest.mark.pg
def test_C13_R1_03_ky_v1_dua_v2_ky_ra_201_phien_ban_2_GET_hai_da_ky_ky_lan_3_409(may):
    ky = _ky_moi()
    with _conn() as c:
        a = chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
    st, r = _ky(may, ky)
    assert st == 201 and r["data"]["phien_ban"] == 1 and r["data"]["checksum"] == a.checksum
    with _conn() as c:
        b = chc.dua_ban_ky(c, ky, _noi_dung(), actor="engine.h14")
    assert b.phien_ban == 2 and b.checksum != a.checksum
    st, r = _ky(may, ky)
    assert st == 201, r
    assert r["data"]["phien_ban"] == 2 and r["data"]["checksum"] == b.checksum
    ds = _get(may, ky)[1]["data"]["ban"]
    assert [(x["phien_ban"], x["trang_thai"]) for x in ds] == [(1, "da_ky"), (2, "da_ky")]
    assert [x["checksum"] for x in ds] == [a.checksum, b.checksum]
    st, r = _ky(may, ky)
    assert st == 409 and r["error"]["code"] == "FLS-CAUHINH-DA-KY", r
    assert "phiên bản 2" in r["error"]["detail"] and NGUOI in r["error"]["detail"]
    assert _so_su_kien_ky(ky) == 2
