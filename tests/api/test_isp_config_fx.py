# -*- coding: utf-8 -*-
"""`C1-B4` — `GET /api/fls/v1/config/fx` qua **MÁY THẬT** + cổng bảng tuyến
*(ISP 3.1.2 · Step 2 · `C1` · `WO-075`)*.

⛔ Bài HTTP ⛔ gọi hàm xử lý trực tiếp *(cùng lý do `tests/api/test_cua_pg.py`)*:
   tuyến phải chứng minh *"dữ liệu ra được qua HTTP"* — qua đề `Authorization`, qua
   định tuyến, qua vỏ `{data, error, meta}`. Một bài gọi hàm Python ⛔ đi qua cả ba.

⭐ **Hợp đồng nguyên văn** của ISP mục 2/7:
   `{bang:'IX.FX', nguon, ky:[{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}],
     thieu:[yyyymm], trung:[yyyymm], lac:[yyyymm]}` — bài so **TẬP KHOÁ BẰNG**, ⛔
   *"có chứa"*: một khoá thừa cũng là lệch hợp đồng *(`Đ5` — cả hai chiều)*.

⭐⭐ **Tuyến TĨNH đầu tiên của bảng tuyến.** Mọi tuyến trước đều chạm ≥ 1 bảng
   `fls_*`, và `kiem_bang_tuyen` từ chối tuyến *"⛔ khai bảng nào"*. Tuyến này đọc
   một **tệp tĩnh** *(cho tới `C5`)* ⇒ nó khai `nguon_tinh` thay cho `bang`, và hai
   cổng phải hiểu điều đó **mà ⛔ nới cho tuyến khác**:
     · `kiem_bang_tuyen`: ⛔ bảng **và** ⛔ nguồn tĩnh vẫn ĐỎ *(bài cũ
       `test_cong_BAT_duong_khong_khai_bang_nao` giữ nguyên)*; nguồn tĩnh chỉ cho
       `GET` ⛔ ghi;
     · `soi_bang_tuyen`: *"khai 0 bảng = SQL 0 bảng"* là **xanh trên tập rỗng**
       *(`Đ3`)* nếu ⛔ chứng minh phép đo đã THẬT SỰ bám tới hàm ⇒ bài đòi `vet`
       chạm `fls.cau_hinh.fx`, và cổng đòi tệp nguồn tĩnh **có thật**.
"""
from __future__ import annotations

import contextlib
import dataclasses
import http.client
import json
import os
import threading
import time
from pathlib import Path

import pytest

from fls.api import bang_tuyen as bt
from fls.api import cua, the
from fls.api.xu_ly import HAM
from fls.db.kho import dsn_test, noi_chi_doc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c1-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/fx"
# Chép NGUYÊN VĂN ISP mục 3 — ⛔ đọc lại từ `fx.NGUON_TINH`: bài này canh chính
# hằng ấy, và một bài so hằng với chính nó thì ⛔ bao giờ đỏ.
NGUON_TINH = "fls/cau_hinh/tinh/ix_fx_mau.json"
KHOA_DATA = {"bang", "nguon", "ky", "thieu", "trung", "lac"}
KHOA_KY = {"yyyymm", "USD", "SGD", "COP", "VND", "HKD", "trang_thai"}


@pytest.fixture(scope="module")
def may():
    """Máy THẬT trên cổng hệ điều hành chọn, kết nối CHỈ ĐỌC vào kho TEST.

    ⚠ Tuyến này ⛔ chạm kho, nhưng `cua.dung_may` **đòi** một đường đọc bị
      PostgreSQL chặn ghi *(`kiem_truoc_khi_mo`)* và cửa mở kết nối cho MỌI tuyến
      ⇒ bài cần PG thật, ⛔ giả kết nối *(luật dự án: ⛔ mock kho)*.
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


# ── C1-B4 · qua HTTP ──────────────────────────────────────────────────────
@pytest.mark.pg
def test_C1_B4_GET_config_fx_200_DUNG_hop_dong(may):
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r

    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.FX"
    assert d["nguon"] == NGUON_TINH

    ky = d["ky"]
    assert len(ky) == 4, f"⛔ mong 4 tháng tổng hợp, đo {len(ky)}"
    for k in ky:
        assert set(k) == KHOA_KY, f"⛔ lệch hợp đồng: {sorted(set(k) ^ KHOA_KY)}"
        # ⛔⛔ Tiền/tỷ giá ra JSON là CHUỖI — `fls/api/bao.py`: JSON ⛔ nói kiểu,
        #    máy đọc biến mọi số thành `float64` trước khi ai kịp chọn.
        for te in ("USD", "SGD", "COP", "VND", "HKD"):
            assert isinstance(k[te], str), (k["yyyymm"], te, k[te])
        assert k["VND"] == "1", (k["yyyymm"], k["VND"])
        assert k["trang_thai"] == "chua_ky", k
    thang = [k["yyyymm"] for k in ky]
    assert thang == sorted(set(thang)), thang

    assert (d["thieu"], d["trung"], d["lac"]) == ([], [], [])
    # ⛔ số TỔNG HỢP ⛔ được khoác nhãn đã đối soát/đã ký (`INV-I14`).
    assert r["meta"]["data_status"] == "flash", r["meta"]


@pytest.mark.pg
def test_C1_B4_khong_the_thi_401_cua_san_co(may):
    ma, r = _goi(may, DUONG, co_the=False)
    assert ma == 401 and r["error"]["code"] == "FLS-UNAUTHORIZED", (ma, r)
    assert r["data"] is None


@pytest.mark.pg
def test_C1_B4_chi_GET__POST_cung_duong_la_405(may):
    """Bảng tỷ giá C1 **chỉ đọc** — ký tháng là `C7`, một tuyến KHÁC."""
    ma, r = _goi(may, DUONG, phuong_thuc="POST")
    assert ma == 405 and r["error"]["code"] == "FLS-METHOD", (ma, r)


# ── C1-B4 · bảng tuyến + `soi_bang_tuyen` ─────────────────────────────────
def _tuyen_fx() -> list[bt.Tuyen]:
    return [t for t in bt.BANG_TUYEN if t.duong == DUONG]


def test_C1_B4_bang_tuyen_khai_DUNG_MOT_tuyen_tinh_chi_doc():
    ds = _tuyen_fx()
    assert len(ds) == 1, f"⛔ mong đúng 1 tuyến {DUONG}, đo {len(ds)}"
    t = ds[0]
    assert t.phuong_thuc == "GET" and not t.ghi and t.bang_ghi == ()
    assert t.bang == (), f"⛔ C1 ⛔ chạm kho, mà khai {t.bang}"
    assert t.nguon_tinh == (NGUON_TINH,), t.nguon_tinh
    assert t.ham in HAM, f"⛔ hàm `{t.ham}` chưa ghi danh ở `HAM`"
    assert bt.kiem_bang_tuyen() == []


def test_C1_B4_soi_bang_tuyen_XANH_va_THAT_SU_do_tuyen_moi():
    loi, do = sbt.soi()
    assert loi == [], "⛔ bản khai lệch SQL:\n  - " + "\n  - ".join(loi)
    ban = [x for x in do if x["duong"] == DUONG]
    assert len(ban) == 1, f"⛔ `soi` đo {len(ban)} lần tuyến {DUONG}"
    x = ban[0]
    assert x["khai"] == [] and x["that"] == [], x
    # ⛔ `Đ3`: "khai 0 = SQL 0" chỉ là KẾT QUẢ khi phép đo đã bám tới hàm thật.
    assert any(v.startswith("fls.cau_hinh.fx.") for v in x["vet"]), (
        f"⛔ phép đo ⛔ bám tới tầng config — tập rỗng là NỀN, ⛔ kết quả: {x['vet']}")
    assert x["nguon_tinh"] == [NGUON_TINH], x
    assert (GOC / NGUON_TINH).is_file()


# ── ⛔ `Đ5` — cổng mới phải được chứng minh ĐỎ ─────────────────────────────
@pytest.mark.parametrize("phuong_thuc,ghi,bang,bang_ghi", [
    ("POST", False, (), ()),
    ("GET", True, ("fls_journal",), ("fls_journal",)),
])
def test_cong_kiem_bang_tuyen_DO_khi_nguon_tinh_o_tuyen_khong_phai_GET_chi_doc(
        phuong_thuc, ghi, bang, bang_ghi):
    """Ngoại lệ *"⛔ bảng — có nguồn tĩnh"* phải **HẸP**: một tệp tĩnh ⛔ ghi được."""
    xau = (bt.Tuyen(phuong_thuc, f"{V}/x", "x", bang, bang_ghi=bang_ghi,
                    ghi=ghi, nguon_tinh=(NGUON_TINH,)),)
    assert any("nguon_tinh" in x for x in bt.kiem_bang_tuyen(xau)), (
        bt.kiem_bang_tuyen(xau))


def test_cong_soi_DO_khi_nguon_tinh_KHONG_ton_tai():
    t = dataclasses.replace(_tuyen_fx()[0],
                            nguon_tinh=("fls/cau_hinh/tinh/khong_co_that.json",))
    loi, _ = sbt.soi((t,))
    assert any("khong_co_that.json" in x for x in loi), loi
