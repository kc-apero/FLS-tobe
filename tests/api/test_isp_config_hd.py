# -*- coding: utf-8 -*-
"""`C4-B4` — `GET /api/fls/v1/config/hd` qua **MÁY THẬT** + hai cổng bảng tuyến
*(ISP 3.1.2 · Step 11 · `C4` · `WO-122`)*.

⛔ Bài HTTP ⛔ gọi hàm xử lý trực tiếp *(cùng lý do `tests/api/test_isp_config_fx.py`)*:
   tuyến phải chứng minh *"dữ liệu ra được qua HTTP"* — qua đề `Authorization`, qua
   định tuyến, qua vỏ `{data, error, meta}`.

⭐⭐ **Tuyến TĨNH thứ HAI của bảng tuyến** *(C1 là thứ nhất — `GET /config/fx`)*. Nó
   đọc **HAI** ảnh tĩnh `ix_hd_cay.json` *(ATL, 74)* + `ix_mapping_master.json`
   *(MM, 73)* ⇒ khai `nguon_tinh=(…ATL…, …MM…)`. Hai cổng phải hiểu điều đó **mà ⛔
   nới cho tuyến khác** *(`test_isp_config_fx.py` giữ các bài Đ5 chung của cơ chế)*.

⛔ Trả **CẢ HAI số** `74 (ATL)` · `73 (MM)` + `chenh_mapping_master = ['NCF']` —
   ⛔ hoà giải *(ràng buộc WO-122; `BG-107`)*.
"""
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
from fls.cau_hinh import hd
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c4-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/hd"
# ⭐⭐ `C5` (`WO-142`): tuyến đọc **KHO** *(hai bảng config)* — ⛔ còn ảnh tĩnh. Ảnh
#    DT3 nạp vào `fls_test` ở `_nap` *(đường TRUYỀN VÀO)*.
BANG_KHO = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
ANH_ATL = GOC / "tests" / "fixture" / "cau_hinh" / "atl_cay.json"
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"
NGUON_ATL = "tests/fixture/cau_hinh/atl_cay.json"
NGUON_MM_ANH = "tests/fixture/cau_hinh/mapping_master_cfg.json"
# Chuỗi MẪU đúng khuôn đường nguồn tĩnh — ảnh đã GỠ; dùng cho bài canh GATE SYNTHETIC.
NGUON_TINH = "fls/cau_hinh/tinh/ix_hd_cay.json"
NGUON_MM = "fls/cau_hinh/tinh/ix_mapping_master.json"
KHOA_DATA = {"bang", "nguon", "nguon_mm", "so_atl", "so_mapping_master",
             "chenh_mapping_master", "goc", "nhom", "nut"}
KHOA_NUT = {"ma", "ten", "cha", "cap", "nhom", "dong_sheet", "con_cua", "la"}


@pytest.fixture(scope="module", autouse=True)
def _nap():
    """Nạp ảnh DT3 *(ATL + Mapping Master)* vào kho TEST TRƯỚC khi máy đọc."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_hd(c, str(ANH_ATL), actor="bo-test-c5-hd", nguon=NGUON_ATL)
        chc.nap_mapping_master(c, str(ANH_MM), actor="bo-test-c5-hd",
                               nguon=NGUON_MM_ANH)
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


# ── C4-B4 · qua HTTP ──────────────────────────────────────────────────────
@pytest.mark.pg
def test_C4_B4_GET_config_hd_200_DUNG_hop_dong(may):
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r

    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.HD"
    assert d["nguon"] == NGUON_ATL and d["nguon_mm"] == NGUON_MM_ANH

    # ⭐ CẢ HAI số + chênh — ⛔ hoà giải.
    assert d["so_atl"] == 74, d["so_atl"]
    assert d["so_mapping_master"] == 73, d["so_mapping_master"]
    assert d["chenh_mapping_master"] == ["NCF"], d["chenh_mapping_master"]

    assert len(d["nut"]) == 74, f"⛔ mong 74 nút, đo {len(d['nut'])}"
    assert len(d["goc"]) == 37, f"⛔ mong 37 gốc, đo {len(d['goc'])}"
    assert d["nhom"] == ["HDO", "HDH", "HDAP", "HDT", "HDC", "HDCI"], d["nhom"]

    for n in d["nut"]:
        assert set(n) == KHOA_NUT, f"⛔ lệch hợp đồng nút: {sorted(set(n) ^ KHOA_NUT)}"
    theo_ma = {n["ma"]: n for n in d["nut"]}
    # con_cua / la đúng — đo nút cụ thể *(`Đ3`)*.
    assert theo_ma["OPC"]["con_cua"] == ["CAC", "COS"]
    assert theo_ma["OPC"]["la"] is False
    assert theo_ma["GI"]["la"] is True and theo_ma["GI"]["cha"] is None
    assert theo_ma["CAC"]["cha"] == "OPC" and theo_ma["CAC"]["cap"] == 2

    # số TĨNH ⛔ được khoác nhãn đã đối soát/đã ký (`INV-I14`).
    assert r["meta"]["data_status"] == "flash", r["meta"]
    assert r["meta"]["run_id"] is None, r["meta"]


@pytest.mark.pg
def test_C4_B4_run_id_o_tuyen_TINH_thi_400_KHONG_khoac_pham_vi_lan_nap(may):
    """Ảnh TĨNH ⛔ theo lần nạp *(cùng `C1-R1-07`)* ⇒ `?run_id=` ⇒ `400`, ⛔ trả cây
    khoác phạm vi lần nạp. `Đ5` chiều kia: lượt trơn vẫn `200`."""
    ma, r = _goi(may, f"{DUONG}?run_id=NAP-2026-01-01-X")
    assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (ma, r)
    assert r["data"] is None, r
    ma, r = _goi(may, DUONG)
    assert ma == 200 and r["meta"]["run_id"] is None, (ma, r["meta"])


@pytest.mark.pg
def test_C4_B4_khong_the_thi_401_cua_san_co(may):
    ma, r = _goi(may, DUONG, co_the=False)
    assert ma == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED", (ma, r)
    assert r["data"] is None


@pytest.mark.pg
def test_C4_B4_chi_GET__POST_cung_duong_la_405(may):
    """Cây IX.HD **chỉ đọc** — kho config là `C5`, một tuyến KHÁC."""
    ma, r = _goi(may, DUONG, phuong_thuc="POST")
    assert ma == 405 and r["error"]["code"] == "FLS-METHOD", (ma, r)


# ── C4-B4 · bảng tuyến + `soi_bang_tuyen` ─────────────────────────────────
def _tuyen_hd() -> list[bt.Tuyen]:
    return [t for t in bt.BANG_TUYEN if t.duong == DUONG]


def test_C4_B4_bang_tuyen_khai_DUNG_MOT_tuyen_KHO_chi_doc():
    """⭐⭐ `C5`: tuyến đọc KHO ⇒ `bang=(ban, dong)`, GO `nguon_tinh`."""
    ds = _tuyen_hd()
    assert len(ds) == 1, f"⛔ mong đúng 1 tuyến {DUONG}, đo {len(ds)}"
    t = ds[0]
    assert t.phuong_thuc == "GET" and not t.ghi and t.bang_ghi == ()
    assert tuple(t.bang) == BANG_KHO, f"⛔ C5 đọc kho config, mà khai {t.bang}"
    assert t.nguon_tinh == (), f"⛔ GO `nguon_tinh` khi đổi sang kho: {t.nguon_tinh}"
    assert t.ham in HAM, f"⛔ hàm `{t.ham}` chưa ghi danh ở `HAM`"
    assert bt.kiem_bang_tuyen() == []


def test_C4_B4_soi_bang_tuyen_XANH_SQL_cham_DUNG_hai_bang_kho():
    """`soi`: SQL thật của `cay_hd` chạm ĐÚNG hai bảng kho đã khai, và phép đo BÁM tới
    `fls.repo.cau_hinh_repo` *(⛔ tập rỗng — Đ3)*."""
    loi, do = sbt.soi()
    assert loi == [], "⛔ bản khai lệch SQL:\n  - " + "\n  - ".join(loi)
    ban = [x for x in do if x["duong"] == DUONG]
    assert len(ban) == 1, f"⛔ `soi` đo {len(ban)} lần tuyến {DUONG}"
    x = ban[0]
    assert x["khai"] == sorted(BANG_KHO) and x["that"] == sorted(BANG_KHO), x
    assert x["thieu"] == [] and x["thua"] == [], x
    assert any(v.startswith("fls.repo.cau_hinh_repo.") for v in x["vet"]), (
        f"⛔ phép đo ⛔ bám tới tầng kho config: {x['vet']}")


# ── ⛔ `Đ5` — GATE `nguon_tinh` *(phòng thủ tuyến tĩnh tương lai)* qua tuyến SYNTHETIC ─
def test_C4_Đ5_nguon_tinh_sai_tep_thi_soi_DO():
    """Tuyến tĩnh SYNTHETIC khai một ảnh ⛔ có thật ⇒ `soi` bắt *(`C5` ⛔ còn tuyến
    tĩnh THẬT; dùng hàm `cay_hd` nay ĐỌC KHO ⇒ `soi` cũng bắt SQL thật — cả hai câu)*."""
    t = bt.Tuyen("GET", DUONG, "cay_hd", (),
                 nguon_tinh=(NGUON_TINH, "fls/cau_hinh/tinh/khong_co_that.json"))
    loi, _ = sbt.soi((t,))
    assert any("khong_co_that.json" in x and "co that" in x for x in loi), loi


def test_C4_Đ5_khai_CA_bang_LAN_nguon_tinh_thi_kiem_DO():
    """Luật *"tuyến TĨNH hay tuyến KHO, ⛔ cả hai"* — tuyến SYNTHETIC."""
    t = bt.Tuyen("GET", DUONG, "cay_hd", ("fls_itl",),
                 nguon_tinh=(NGUON_TINH, NGUON_MM))
    loi = bt.kiem_bang_tuyen((t,))
    assert any("CUNG `bang`" in x for x in loi), loi


def test_C4_Đ5_tuyen_tinh_ma_ham_DOC_KHO_thi_HAI_cong_DO():
    """`Đ5`: tuyến tĩnh SYNTHETIC với hàm ĐỌC KHO `so` ⇒ `kiem` bắt `conn`, `soi`
    bắt SQL thật chạm `fls_itl`."""
    t = bt.Tuyen("GET", f"{V}/x", "so", (), nguon_tinh=(NGUON_TINH,))
    assert any("conn" in x and "`so`" in x for x in bt.kiem_bang_tuyen((t,))), (
        bt.kiem_bang_tuyen((t,)))
    assert any("nguon_tinh" in x and "fls_itl" in x for x in sbt.soi((t,))[0])


# ── AC-5 · kho RỖNG ⇒ handler `cay_hd` dịch `ChuaKhai`→409, `BangLa`→404 ────────────
def _nem(exc):
    def _f(_conn):
        raise exc
    return _f


def test_AC5_handler_cay_hd_dich_ChuaKhai_409_va_BangLa_404(monkeypatch):
    """AC-5: kho RỖNG ⇒ `cay_hd` NỔ lỗi **có TÊN**, ⛔ rơi về ảnh tĩnh. `ChuaKhai`→
    `409` ≠ `BangLa`→`404`. Stub ranh giới repo *(⛔ mock kho — hai loại lỗi đã chứng
    ở kho thật `tests/cau_hinh/test_kho_cau_hinh_pg.py`)*."""
    from fls.api import bao, xu_ly
    yc = xu_ly.YeuCau(conn=None, pv=xu_ly.pham_vi_cua_yeu_cau({}), q={}, tham={})

    monkeypatch.setattr(chc, "doc_hd", _nem(chc.ChuaKhai("kho rỗng")))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.cay_hd(yc)
    assert e.value.ma == "FLS-CAUHINH-CHUA-KHAI" and bao.MA_LOI[e.value.ma][0] == 409

    monkeypatch.setattr(chc, "doc_hd", _nem(chc.BangLa("nguồn lạ")))
    with pytest.raises(xu_ly.LoiCua) as e2:
        xu_ly.cay_hd(yc)
    assert e2.value.ma == "FLS-CAUHINH-BANG-LA" and bao.MA_LOI[e2.value.ma][0] == 404
