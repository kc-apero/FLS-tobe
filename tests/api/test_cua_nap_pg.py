# -*- coding: utf-8 -*-
"""Nhóm **NẠP** *(`BA-07` §4b)* CHẠY THẬT qua HTTP.

⛔ Bộ bài này ⛔ **không gọi hàm xử lý trực tiếp**: một bài gọi hàm Python ⛔ không
đi qua đề `Authorization`, ⛔ không đi qua phép chọn kết nối, ⛔ không đi qua vỏ
bọc `{data, error, meta}`. Mà `CR#11` đòi *một CỬA VÀO*, ⛔ không phải một hàm.

⭐ Bài đắt nhất ở đây: `test_XEM_TRUOC_KHONG_ghi_mot_dong_nao` — đó là cả lý do
   *xem trước* phải là **một tuyến RIÊNG**, ⛔ không phải một cờ.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import threading
import time
import uuid

import psycopg
import pytest

from fls.adapters.sao_ke import SAU_TRUONG
from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo.nguon_dai import ghi_dai

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-cua-nap-dai-hon-ba-muoi-hai-ky-tu-that-nhe"
AI = "ke.toan@apero.vn"
V = cua.bang_tuyen.TIEN_TO


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@contextlib.contextmanager
def _may():
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    def mo_doc():
        @contextlib.contextmanager
        def mo():
            c = noi_chi_doc(dsn_test())
            try:
                yield c
            finally:
                c.close()
        return mo

    def mo_ghi():
        @contextlib.contextmanager
        def mo():
            c = psycopg.connect(dsn_test(), autocommit=True)
            try:
                yield c
            finally:
                c.close()
        return mo()

    m = None
    try:
        m = cua.dung_may(mo_doc(), cong=0, mo_ghi=mo_ghi)
        threading.Thread(target=m.serve_forever, daemon=True).start()
        yield m
    finally:
        if m is not None:
            m.shutdown()
            m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


@pytest.fixture()
def may():
    with _may() as m:
        yield m


def _goi(may, duong: str, *, pt: str = "POST", than: dict | None = None
         ) -> tuple[int, dict]:
    c = http.client.HTTPConnection(*may.server_address, timeout=15)
    de = {"Authorization": "Bearer " + the.dong_the(
        {"sub": AI, "exp": int(time.time()) + 300}, KHOA.encode())}
    body = json.dumps(than).encode() if than is not None else None
    if body is not None:
        de["Content-Type"] = "application/json"
    try:
        c.request(pt, duong, body=body, headers=de)
        r = c.getresponse()
        d = r.read()
        return r.status, (json.loads(d) if d else {})
    finally:
        c.close()


@pytest.fixture()
def nguon():
    """Một `fls_source` RIÊNG, ⛔ CHƯA có bản khai — **nhưng ĐÃ có dải đọc**.

    ⛔⛔ Dải đọc *(bản khai THỨ HAI, `GAP-KHAI-01`)* phải có sẵn, vì `S10` là
       hạng **`CHẶN`**: ⛔ chưa thu dải ⇒ ⛔ **không biết FLS có đang đọc đúng
       cột ⛔ không** ⇒ ⛔ 0 dòng được vào sổ. Đó là **cố ý**, ⛔ không phải một
       chỗ phiền: đọc nhầm cột là **sai tiền**, và cách chữa chỉ là chạy
       `tools/nap_nguon_dai.py --that` một lần.

    ⭐ Dải ở đây khớp `_khai_du()` *(`Date`=0 `Debit`=3 `Credit`=4)* nên `S10`
      xanh; bài `test_S10_LECH_thi_chan_ca_lo` dựng lại ca lệch.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_source (source_key, src_type) "
                    "VALUES (%s,'Bank') RETURNING source_id",
                    ("R | HTTP" + _hex(),))
        sid = cur.fetchone()[0]
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ghi_dai(c, sid, {"Date": "!A3:A", "Debit": "!D3:D", "Credit": "!E3:E"},
                danh_muc="BankAccountList")
    return sid


def _khai_du(cot_ngay: int = 0) -> dict[str, int]:
    return {t: i + cot_ngay for i, t in enumerate(SAU_TRUONG)}


def _dong(ngay="25/01/2026", mota="x", te="VND", no=1000, co="", ma="FT001"):
    return [ngay, mota, te, no, co, ma]


def _dem_so(run_id: str) -> int:
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE run_id = %s", (run_id,))
        return int(cur.fetchone()[0])


# ────────────────────────────────────────────────────── ① ghi bản khai
def test_ghi_ban_khai_qua_HTTP(may, nguon):
    ma, d = _goi(may, f"{V}/sources/{nguon}/khai-cot",
                 than={"cot": _khai_du()})
    assert ma == 200, d
    assert d["data"]["version"] == 1
    assert d["data"]["actor"] == AI, "⛔ `actor` phải đến TỪ THẺ"


def test_ghi_khai_THIEU_truong_thi_422(may, nguon):
    k = _khai_du()
    del k["Credit"]
    ma, d = _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": k})
    assert ma == 422 and d["error"]["code"] == "FLS-KHAI-THIEU", d


def test_ghi_khai_cho_NGUON_KHONG_CO_thi_404(may):
    ma, d = _goi(may, f"{V}/sources/999999999/khai-cot",
                 than={"cot": _khai_du()})
    assert ma == 404 and d["error"]["code"] == "FLS-NGUON-LA", d


def test_sua_khai_la_THEM_version_moi(may, nguon):
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    ma, d = _goi(may, f"{V}/sources/{nguon}/khai-cot",
                 than={"cot": _khai_du(cot_ngay=10)})
    assert ma == 200 and d["data"]["version"] == 2, d


# ─────────────────────────────────────────────────────── ② xem trước
def test_XEM_TRUOC_KHONG_ghi_mot_dong_nao(may, nguon):
    """⭐⭐ Cả lý do *xem trước* là một **tuyến RIÊNG**, ⛔ không phải một cờ.

    Hai việc khác nhau về **hậu quả** thì ⛔ không được khác nhau bằng **một
    chữ trong thân yêu cầu**: một cờ `?that=true` gõ thiếu là **ghi thật khi
    định thử**.
    """
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl")
        truoc = int(cur.fetchone()[0])

    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": nguon, "dong": [_dong(), _dong(ma="B")]})
    assert ma == 200, d
    bb = d["data"]
    assert bb["so_dong_vao"] == 2 and bb["so_dong_ra"] == 2
    assert bb["se_ghi"] is True

    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl")
        assert int(cur.fetchone()[0]) == truoc, "⛔ XEM TRƯỚC ĐÃ GHI VÀO SỔ"


def test_bien_ban_du_9_luat_va_MOI_luat_deu_co_da_do(may, nguon):
    """⛔⛔ `da_do` ⛔ **KHÔNG được vắng mặt** *(`BA-07` §4b ⓷)*.

    Luật nền của cả hai cổng: **đo được `0` thứ ⇒ ⛔ KHÔNG ĐẠT**. Một biên bản
    chỉ nói *"đạt"* mà ⛔ không nói **đã đo bao nhiêu** là biên bản ⛔ không đọc
    được — và luật này **đã cứu một lần thật** *(`L6` cổng #17 báo đo `0`)*.
    """
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    _ma, d = _goi(may, f"{V}/nap/xem-truoc",
                  than={"source_id": nguon, "dong": [_dong()]})
    luat = d["data"]["luat"]
    # ⚠ **8 → 9 ngày 08/09**, và ⛔ không phải nới cổng: `S10` *(`GAP-KHAI-01`)*
    #   là một luật **THÊM**, hạng `CHẶN` — nó so **hai bản khai** của cùng một
    #   phép ánh xạ *(dòng 1 của sheet ↔ `Range_*` của danh mục)*.
    assert len(luat) == 9, [k["ten"] for k in luat]
    assert any(k["ten"].startswith("S10") for k in luat), (
        "⛔ bien ban THIEU han S10 — mot bien ban 8 dong xanh doc y het mot "
        "bien ban ⛔ khong co luat ay, va nguoi doc ⛔ khong the biet")
    assert all("da_do" in k for k in luat)
    assert all(k["hang"] in ("CHAN", "CO", "CANH") for k in luat)


def test_nguon_CHUA_KHAI_thi_409_chu_KHONG_404(may, nguon):
    """⚠ **409 ⛔ không phải 404** *(`BA-07` §4b ⓺)*: nguồn **có tồn tại**, chỉ
    là ⛔ chưa ai khai cách đọc nó. Hai câu dẫn đi **hai đường sửa khác nhau**."""
    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": nguon, "dong": [_dong()]})
    assert ma == 409 and d["error"]["code"] == "FLS-KHAI-KHONG-CO", d


def test_nguon_LA_thi_404(may):
    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": 999999999, "dong": [_dong()]})
    assert ma == 404 and d["error"]["code"] == "FLS-NGUON-LA", d


# ───────────────────────────────────────────────────────────── ③ nạp
def test_NAP_that_vao_so_va_tra_CUNG_bien_ban(may, nguon):
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    run = "NAP-2026-01-05-HTTP" + _hex(4)
    ma, d = _goi(may, f"{V}/nap",
                 than={"source_id": nguon, "run_id": run,
                       "dong": [_dong(), _dong(ma="B")]})
    assert ma == 200, d
    bb = d["data"]
    assert bb["run_id"] == run and bb["vao_so"] == 2
    assert len(bb["luat"]) == 9, "⛔ nạp phải trả CÙNG biên bản với xem trước"
    assert _dem_so(run) == 2


def test_NAP_HAI_LAN_qua_HTTP_KHONG_nhan_doi(may, nguon):
    """⭐ Cùng bất biến với tầng kho, nhưng đo **qua cửa** — vì đó là chỗ kế
    toán thật sự bấm."""
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    run = "NAP-2026-01-05-HTTP" + _hex(4)
    than = {"source_id": nguon, "run_id": run,
            "dong": [_dong(), _dong(ma="B"), _dong(ma="C")]}
    _goi(may, f"{V}/nap", than=than)
    ma, d = _goi(may, f"{V}/nap", than=than)
    assert ma == 200, d
    assert d["data"]["trung"] == 3 and d["data"]["vao_so"] == 0
    assert _dem_so(run) == 3, "⛔ SỔ ĐÃ NHÂN ĐÔI QUA CỬA HTTP"


def test_run_id_SAI_HINH_thi_400_va_KHONG_ghi(may, nguon):
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    ma, d = _goi(may, f"{V}/nap",
                 than={"source_id": nguon, "run_id": "lo-bay",
                       "dong": [_dong()]})
    assert ma == 400, d
    assert _dem_so("lo-bay") == 0


def test_KHONG_co_PUT_hay_DELETE_o_nhom_NAP(may, nguon):
    """⛔ Sổ chỉ-thêm *(`INV-I08`)* — nạp nhầm thì **nạp bản đúng rồi đảo**,
    ⛔ không xoá. Cửa phải trả **405**, ⛔ không phải 404 *(đường CÓ tồn tại)*."""
    for pt in ("PUT", "DELETE", "PATCH"):
        ma, d = _goi(may, f"{V}/nap", pt=pt, than={"source_id": nguon})
        assert ma == 405, (pt, ma, d)


def test_than_yeu_cau_SAI_KHUON_thi_400(may, nguon):
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    for than in ({"source_id": nguon}, {"source_id": nguon, "dong": "x"},
                 {"source_id": nguon, "dong": ["khong-phai-danh-sach"]}):
        ma, d = _goi(may, f"{V}/nap/xem-truoc", than=than)
        assert ma == 400, (than, ma, d)


def test_NGAY_MO_HO_thi_ca_LO_bi_tu_choi_va_KHONG_ghi_gi(may, nguon):
    """⛔⛔ **Khoá hành vi HIỆN TẠI, và nói thẳng nó CHƯA đủ tốt.**

    `25/01/2026` chỉ có **một** cách đọc *(⛔ không có tháng 25)*. Nhưng
    `05/01/2026` đọc được **hai** cách, và tầng sổ **TỪ CHỐI ĐOÁN** — đúng
    `QĐ-ITL-17`: sổ thật có **93% dòng bị hoán ngày↔tháng**, và một phép đoán ở
    đây là **~181 tỷ sai kỳ**.

    ⚠ **Nhưng hôm nay MỘT ô mơ hồ giết CẢ LÔ** *(400, ⛔ 0 dòng vào sổ)*. An
      toàn — nhưng với một lô **8.345 dòng** thì nó **⛔ không dùng được**: kế
      toán ⛔ không có đường nào đi tiếp ngoài việc sửa tay tệp gốc.

    ⭐ Cái ĐÚNG là: dòng ấy vào **`fls_reject` với lý do CÓ TÊN**, và lô **đi
      tiếp** — cùng thang thuốc với ô lỗi `#REF!`. Đó là `GAP-NAP-02`, và nó
      thuộc tầng `ledger`, ⛔ không phải chuyện vá ở tầng cửa.

    ⇒ Bài này khoá hành vi hiện tại để nó ⛔ **không đổi trong im lặng** — đổi
      thì phải đọc đoạn này và đóng `GAP-NAP-02` một cách có chủ đích.
    """
    _goi(may, f"{V}/sources/{nguon}/khai-cot", than={"cot": _khai_du()})
    run = "NAP-2026-01-05-MOHO" + _hex(4)
    ma, d = _goi(may, f"{V}/nap",
                 than={"source_id": nguon, "run_id": run,
                       "dong": [_dong(ma="A"), _dong(ngay="05/01/2026", ma="B")]})
    # ⭐ Lô ĐI TIẾP: dòng đọc được vào sổ, dòng mơ hồ vào `fls_reject`.
    assert ma == 200, d
    assert d["data"]["vao_so"] == 1, d["data"]
    assert _dem_so(run) == 1, "⛔ dòng đọc được PHẢI vào sổ"

    # ⛔⛔ Và mối lo GỐC của bài này vẫn được canh: ⛔ không dòng nào rơi im
    #    lặng. Dòng bị loại phải nằm trong `fls_reject` **kèm lý do CÓ TÊN**.
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT source_row, reason FROM fls_reject WHERE run_id=%s",
                    (run,))
        r = cur.fetchall()
    assert len(r) == 1, r
    assert "mo ho" in r[0][1], (
        "⛔ vào `fls_reject` mà lý do ⛔ không nói *vì sao* thì vẫn ⛔ không ai "
        "biết phải sửa gì — đúng cái `400` cũ, chỉ đổi chỗ nằm")


def test_KHAI_thu_tu_thi_dong_MO_HO_VAO_SO(may, nguon):
    """⭐⭐⭐ Nửa còn lại của `QĐ-ITL-113`: vào `fls_reject` là **chưa xong**.

    Bài trên chứng minh lô ⛔ không còn bị giết. Bài này chứng minh **1.894
    dòng thật được CỨU** — bằng bản khai, ⛔ không bằng một phép đoán.

    ⛔⛔ Và nó đo cả **chiều ngược**: cùng chuỗi `05/01/2026`, hai bản khai cho
       **hai ngày khác nhau**. Nếu bài chỉ hỏi *"vào sổ được ⛔ không"* thì nó
       sẽ xanh cả khi máy **đoán bừa** — tính chất thật phải canh là *"bản khai
       QUYẾT ĐỊNH kết quả"*.
    """
    ra = {}
    for tt, mong in (("mdy", "2026-05-01"), ("dmy", "2026-01-05")):
        ma, k = _goi(may, f"{V}/sources/{nguon}/khai-cot",
                     than={"cot": _khai_du(), "thu_tu": tt})
        assert ma == 200, k
        assert k["data"]["thu_tu"] == tt, k["data"]

        run = "NAP-2026-01-05-KHAI" + _hex(4)
        ma, d = _goi(may, f"{V}/nap",
                     than={"source_id": nguon, "run_id": run,
                           "dong": [_dong(ngay="05/01/2026", ma="B" + _hex(3))]})
        assert (ma, d["data"]["vao_so"]) == (200, 1), d
        with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
            cur.execute("SELECT doc_date FROM fls_itl WHERE run_id=%s", (run,))
            ra[tt] = cur.fetchone()[0].isoformat()
        assert ra[tt] == mong, (tt, ra[tt], mong)
    assert ra["mdy"] != ra["dmy"], ra


def test_thu_tu_LA_thi_cua_tra_400__khong_am_tham_bo_qua(may, nguon):
    """⛔ Nhận `DMY` rồi lặng lẽ coi là `None` = **đổi câu trả lời của người**.

    Kế toán bấm khai `dmy`, cửa ghi `NULL`, và ngày mơ hồ vẫn bị loại — mà
    trên màn thì **trông như đã khai xong**.
    """
    for tt in ("DMY", "d/m/y", "dd/mm/yyyy", "", 1):
        ma, d = _goi(may, f"{V}/sources/{nguon}/khai-cot",
                     than={"cot": _khai_du(), "thu_tu": tt})
        assert ma == 400, (tt, ma, d)


def test_XEM_TRUOC_chay_tren_ket_noi_bi_KHO_CHAN_GHI(may, nguon):
    """⭐⭐⭐ *"Xem trước ⛔ không ghi"* ⛔ **KHÔNG phải một lời hứa trong mã** —
    nó là thứ **chính cái kho từ chối**.

    Tuyến này khai `ghi=False`, nên `cua.py` cấp cho nó **kết nối chỉ-đọc**;
    PostgreSQL tự từ chối mọi phép ghi trên đó. ⇒ Dù ai đó lỡ viết một câu
    `INSERT` vào đường xem-trước, nó **⛔ không chạy được**.

    ⚠ Và đây đúng là chỗ vừa lộ ra một **cặp bị dính vào nhau** trong mã cửa:
      nó coi *"đọc thân yêu cầu"* ⟺ *"có ghi"*. `xem-truoc` **đọc cả một lô**
      trong thân mà ⛔ **không ghi gì** — cách chữa SAI là khai nó `ghi=True`
      cho "dễ", vì làm thế nó sẽ được cấp **kết nối GHI** và mất đúng cái đặc
      điểm khiến nó tồn tại.
    """
    import fls.api.bang_tuyen as bt

    t = next(x for x in bt.BANG_TUYEN if x.duong.endswith("/nap/xem-truoc"))
    assert t.ghi is False, "⛔ xem-truoc mà khai `ghi=True` ⇒ được cấp kết nối GHI"
    assert t.bang_ghi == (), "⛔ xem-truoc khai `bang_ghi` — nó ⛔ không ghi gì"
    assert t.can_than is True, "⛔ ⛔ không đọc được thân thì ⛔ không soát được gì"


# ═════════════════════════════════════════════════════════════════════════
# `S10` ở cửa — `GAP-KHAI-01`. Hai bài dưới đây khoá **hành vi CHẶN**, thứ
# ⛔ chưa bài nào của tệp này từng chạm tới.
# ═════════════════════════════════════════════════════════════════════════

def _nguon_khong_dai():
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_source (source_key, src_type) "
                    "VALUES (%s,'Bank') RETURNING source_id",
                    ("R | KhongDai" + _hex(),))
        return cur.fetchone()[0]


def test_CHUA_THU_DAI_thi_S10_bao_CHUA_DO_va_CHAN_ca_lo(may):
    """⛔⛔ ⛔ Chưa thu dải ⇒ ⛔ **không biết FLS có đang đọc đúng cột ⛔ không**.

    ⭐ Hạng `CHẶN` ở đây là **cố ý**: đọc nhầm cột là **sai tiền**, ⛔ không
      phải một khuyết tật có sẵn của kế toán. Và cách chữa chỉ là chạy
      `tools/nap_nguon_dai.py --that` **một lần**.

    ⛔ Thông báo phải nói **chạy lệnh nào**, ⛔ không chỉ nói *"chưa đo"*.
    """
    sid = _nguon_khong_dai()
    _goi(may, f"{V}/sources/{sid}/khai-cot", than={"cot": _khai_du()})
    _ma, d = _goi(may, f"{V}/nap/xem-truoc",
                  than={"source_id": sid, "dong": [_dong()]})
    bb = d["data"]
    s10 = next(k for k in bb["luat"] if k["ten"].startswith("S10"))
    assert not s10["dat"] and s10["da_do"] == 0
    assert "nap_nguon_dai" in s10["thong_diep"], (
        "⛔ thong bao ⛔ khong noi CHAY LENH NAO: %s" % s10["thong_diep"])
    assert s10["ten"] in bb["chan"], "⛔ S10 do ma lo ⛔ KHONG bi chan"
    assert bb["se_ghi"] is False


def test_S10_LECH_thi_chan_ca_lo_va_NAP_tra_422_kem_bien_ban(may):
    """⛔⛔ Ca nguy nhất: **hai bản khai trỏ hai cột khác nhau**.

    ⭐⭐ Bài này cũng là bài đầu tiên đi qua đường **`422` kèm biên bản** — và
      chính nó làm lộ ra rằng khoá `bien_ban` ⛔ **chưa từng được khai** trong
      `bao.KHOA_THEM`, nên đường ấy sẽ **NỔ `KeyError`** ngay lần đầu có một
      lô thật bị chặn. Một nhánh lỗi ⛔ chưa ai đi qua là một nhánh **chưa
      biết có chạy**.
    """
    sid = _nguon_khong_dai()
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        # khai dòng 1 nói `Debit` ở cột 3; danh mục nói cột 5 ⇒ LỆCH
        ghi_dai(c, sid, {"Date": "!A3:A", "Debit": "!F3:F", "Credit": "!E3:E"},
                danh_muc="BankAccountList")
    _goi(may, f"{V}/sources/{sid}/khai-cot", than={"cot": _khai_du()})

    _ma, d = _goi(may, f"{V}/nap/xem-truoc",
                  than={"source_id": sid, "dong": [_dong()]})
    s10 = next(k for k in d["data"]["luat"] if k["ten"].startswith("S10"))
    assert not s10["dat"], "⛔ hai ban khai LECH ma S10 van xanh"
    assert "Debit" in s10["thong_diep"], (
        "⛔ ⛔ khong noi LECH O TRUONG NAO: %s" % s10["thong_diep"])
    assert d["data"]["se_ghi"] is False

    run = "NAP-2026-01-05-S10" + _hex(4)
    ma, d2 = _goi(may, f"{V}/nap",
                  than={"source_id": sid, "run_id": run, "dong": [_dong()]})
    assert ma == 422 and d2["error"]["code"] == "FLS-SOAT-CHAN", d2
    assert d2["error"].get("bien_ban"), (
        "⛔ noi 'bi chan' ma ⛔ KHONG kem bien ban — nguoi dung phai doan")
    assert _dem_so(run) == 0, "⛔ lo bi CHAN ma van co dong vao so"
