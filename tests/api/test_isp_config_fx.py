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
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from tools import soi_bang_tuyen as sbt

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cua-bo-test-isp-c1-dai-hon-ba-muoi-hai-ky-tu"
V = bt.TIEN_TO
DUONG = f"{V}/config/fx"
# ⭐⭐ `C5` (`WO-142`): tuyến đọc **KHO** config chỉ-thêm ⇒ khai hai bảng kho,
#    ⛔ còn `nguon_tinh`. Ảnh thật DT2 nạp vào `fls_test` ở `_nap` *(đường TRUYỀN
#    VÀO)*.
BANG_KHO = ("fls_cau_hinh_ban", "fls_cau_hinh_dong")
ANH_IX_FX = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"
THANG_DAU_IX_FX = 202401        # khai ở khuôn `ix_fx` *(⛔ bản chép — C5 ánh xạ)*
# Chuỗi MẪU đúng khuôn đường nguồn tĩnh — ảnh đã GỠ; dùng cho các bài canh GATE
# `nguon_tinh` *(phòng thủ cho tuyến tĩnh tương lai, tuyến SYNTHETIC cố ý khai sai)*.
NGUON_TINH = "fls/cau_hinh/tinh/ix_fx_mau.json"
KHOA_DATA = {"bang", "nguon", "ky", "thieu", "trung", "lac"}
KHOA_KY = {"yyyymm", "USD", "SGD", "COP", "VND", "HKD", "trang_thai"}


@pytest.fixture(scope="module", autouse=True)
def _nap():
    """Nạp ảnh DT2 `ix_fx.json` vào kho TEST *(đường GHI riêng)* TRƯỚC khi máy đọc.

    ⛔ Kho dùng chung + chỉ-thêm ⇒ ⛔ dọn được; `doc_fx` đọc phiên bản MỚI NHẤT,
       nên nạp ngay trước bộ bài này là đủ để `GET` thấy đúng ảnh *(37 dòng)*.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_fx(c, str(ANH_IX_FX), actor="bo-test-c5-fx",
                      thang_dau=THANG_DAU_IX_FX, nguon="tests/fixture/cau_hinh/ix_fx.json")
    yield


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
    """⭐⭐ `C5` (`WO-142`): số đọc từ **KHO** *(ảnh thật DT2, 37 dòng)* — ⛔ 4 tháng
    tổng hợp như C1. Hợp đồng RA ⛔ đổi."""
    ma, r = _goi(may, DUONG)
    assert ma == 200, (ma, r)
    assert set(r) == {"data", "error", "meta"} and r["error"] is None, r

    d = r["data"]
    assert set(d) == KHOA_DATA, f"⛔ lệch hợp đồng: {sorted(set(d) ^ KHOA_DATA)}"
    assert d["bang"] == "IX.FX"
    assert d["nguon"] == "tests/fixture/cau_hinh/ix_fx.json"

    ky = d["ky"]
    # ⭐ AC-1: ảnh DT2 thật ⇒ **37** dòng *(đo trên ảnh; ⛔ sửa cho khớp — Đ1/Đ4)*.
    assert len(ky) == 37, f"⛔ mong 37 dòng (DT2), đo {len(ky)}"
    for k in ky:
        assert set(k) == KHOA_KY, f"⛔ lệch hợp đồng: {sorted(set(k) ^ KHOA_KY)}"
        # ⛔⛔ Tiền/tỷ giá ra JSON là CHUỖI — `fls/api/bao.py`: JSON ⛔ nói kiểu,
        #    máy đọc biến mọi số thành `float64` trước khi ai kịp chọn.
        for te in ("USD", "SGD", "COP", "VND", "HKD"):
            assert isinstance(k[te], str), (k["yyyymm"], te, k[te])
        assert k["VND"] == "1", (k["yyyymm"], k["VND"])
        assert k["trang_thai"] == "chua_ky", k
    thang = [k["yyyymm"] for k in ky]
    # ⭐ `yyyymm` là SỐ NGUYÊN JSON *(⛔ chuỗi, ⛔ `bool`)* — hợp đồng liên làn với H1.
    assert all(type(m) is int for m in thang), thang
    assert thang == sorted(thang), f"⛔ `ky` theo thứ tự tháng: {thang}"

    # ⭐ AC-1: `lac = [202306]` *(dòng trước `thang_dau` 202401)* — đo trên ảnh.
    assert d["lac"] == [202306], d["lac"]
    assert (d["thieu"], d["trung"]) == ([], [])
    # ⛔ số THẬT chưa ký ⛔ được khoác nhãn đã đối soát/đã ký (`INV-I14`).
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


def test_C1_B4_bang_tuyen_khai_DUNG_MOT_tuyen_KHO_chi_doc():
    """⭐⭐ `C5`: tuyến đọc KHO ⇒ `bang=(ban, dong)`, GO `nguon_tinh`."""
    ds = _tuyen_fx()
    assert len(ds) == 1, f"⛔ mong đúng 1 tuyến {DUONG}, đo {len(ds)}"
    t = ds[0]
    assert t.phuong_thuc == "GET" and not t.ghi and t.bang_ghi == ()
    assert tuple(t.bang) == BANG_KHO, f"⛔ C5 đọc kho config, mà khai {t.bang}"
    assert t.nguon_tinh == (), f"⛔ GO `nguon_tinh` khi đổi sang kho: {t.nguon_tinh}"
    assert t.ham in HAM, f"⛔ hàm `{t.ham}` chưa ghi danh ở `HAM`"
    assert bt.kiem_bang_tuyen() == []


def test_C1_B4_soi_bang_tuyen_XANH_SQL_cham_DUNG_hai_bang_kho():
    """`soi`: SQL thật của `ty_gia` chạm ĐÚNG hai bảng kho đã khai *(⛔ thiếu, ⛔
    thừa)*, và phép đo BÁM tới `fls.repo.cau_hinh_repo` *(⛔ tập rỗng — Đ3)*."""
    loi, do = sbt.soi()
    assert loi == [], "⛔ bản khai lệch SQL:\n  - " + "\n  - ".join(loi)
    ban = [x for x in do if x["duong"] == DUONG]
    assert len(ban) == 1, f"⛔ `soi` đo {len(ban)} lần tuyến {DUONG}"
    x = ban[0]
    assert x["khai"] == sorted(BANG_KHO) and x["that"] == sorted(BANG_KHO), x
    assert x["thieu"] == [] and x["thua"] == [], x
    assert any(v.startswith("fls.repo.cau_hinh_repo.") for v in x["vet"]), (
        f"⛔ phép đo ⛔ bám tới tầng kho config: {x['vet']}")


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
    """GATE `nguon_tinh` *(phòng thủ cho tuyến tĩnh tương lai)* — tuyến SYNTHETIC cố ý
    khai một ảnh ⛔ có thật ⇒ `soi` bắt *(`C5` ⛔ còn tuyến tĩnh THẬT)*."""
    t = bt.Tuyen("GET", DUONG, "ty_gia", (),
                 nguon_tinh=("fls/cau_hinh/tinh/khong_co_that.json",))
    loi, _ = sbt.soi((t,))
    assert any("khong_co_that.json" in x for x in loi), loi


# ══ Vòng sửa sau R1 (`KQ-077`) ══════════════════════════════════════════════
#
# ── C1-R1-02 *(NÊN SỬA)*: ngoại lệ `nguon_tinh` từng NỚI cổng ⓓ ────────────
#
# ⛔⛔ R1 dựng tuyến cố ý khai sai rồi hỏi hai cổng *(bản sao, ⛔ kho)* — trên bản
#    `5582246`: **A** ⇒ `kiem_bang_tuyen` XANH · **B**, **D** ⇒ **cả hai** XANH ·
#    **C** ⇒ `kiem_bang_tuyen` XANH, `soi` **32** câu rác. Ngoại lệ chỉ hỏi *"tệp có
#    tồn tại"* — một câu về **hình**, ⛔ về **sự thật** *(hàm có đọc tệp ấy không)*.
#    Luật phòng tái phạm của R1: *"một ngoại lệ mới của cổng phải có phép canh SỰ
#    THẬT như phép canh cũ, và phải được hỏi lại bằng tuyến CỐ Ý khai sai"*.
def _xau(nhan: str) -> bt.Tuyen:
    """Tuyến cố ý khai sai — **A…D chép nguyên R1** (`KQ-077` §Phép phá), E · A2 thêm."""
    so = next(t for t in bt.BANG_TUYEN if t.ham == "so")
    return {
        # A: hàm ĐỌC KHO khai `bang=()` + một tệp có thật bất kỳ.
        "A": bt.Tuyen("GET", f"{V}/x", "so", (), nguon_tinh=("pyproject.toml",)),
        # A2: khai CẢ bảng kho LẪN nguồn tĩnh — tuyến tĩnh hay tuyến kho, ⛔ cả hai.
        "A2": bt.Tuyen("GET", f"{V}/x", "so", so.bang, nguon_tinh=(NGUON_TINH,)),
        # A3: bản khai TỰ NHẤT QUÁN *(`bang=()`, đường đúng khuôn)* mà hàm đọc kho.
        "A3": bt.Tuyen("GET", f"{V}/x", "so", (), nguon_tinh=(NGUON_TINH,)),
        # B: hàm đúng, tệp có thật nhưng ⛔ phải nguồn của hàm.
        "B": bt.Tuyen("GET", DUONG, "ty_gia", (), nguon_tinh=("CLAUDE.md",)),
        # C: CHUỖI thay tuple — quên dấu phẩy.
        "C": bt.Tuyen("GET", DUONG, "ty_gia", (), nguon_tinh=NGUON_TINH),
        # D: ra ngoài repo.
        "D": bt.Tuyen("GET", DUONG, "ty_gia", (),
                      nguon_tinh=("../../../../../../../../etc/hostname",)),
        # E: thư mục thay cho tệp.
        "E": bt.Tuyen("GET", DUONG, "ty_gia", (), nguon_tinh=("fls/cau_hinh/tinh",)),
    }[nhan]


@pytest.mark.parametrize("nhan", ["A", "A2", "A3", "B", "C", "D", "E"])
def test_R1_02_tuyen_khai_SAI_nguon_tinh_thi_HAI_cong_cung_DO(nhan):
    """Mỗi tuyến cố ý khai sai ⇒ **CẢ HAI** cổng đỏ, câu nói `nguon_tinh`, **một dòng**.

    ⭐ Vì sao đòi CẢ HAI *(⛔ "ít nhất một")*: `kiem_bang_tuyen` chạy lúc DỰNG MÁY
      *(`cua.dung_may`)* — tuyến khai sai ⛔ được lên máy; `soi` chạy ở cổng — nó đo
      SỰ THẬT *(hàm có đọc tệp ấy, có chạm kho)*. Một lớp là một lớp có thể bị gỡ.
    """
    t = _xau(nhan)
    k = [x for x in bt.kiem_bang_tuyen((t,)) if "nguon_tinh" in x]
    s = [x for x in sbt.soi((t,))[0] if "nguon_tinh" in x]
    assert k, f"⛔ {nhan}: `kiem_bang_tuyen` XANH — {bt.kiem_bang_tuyen((t,))}"
    assert s, f"⛔ {nhan}: `soi` XANH — {sbt.soi((t,))[0]}"
    assert all("\n" not in x for x in k + s), k + s


@pytest.mark.parametrize("nhan", ["A", "B", "D", "E"])
def test_R1_02_soi_noi_RO_LUAT_DUONG_bi_pham(nhan):
    """Mỗi nhánh của ⓔ phải có bài của RIÊNG nó: B · D còn đỏ nhờ ⓔ2 *(hàm ⛔ mang
    chuỗi)*, E còn đỏ nhờ *"tệp ⛔ có thật"* — gỡ phép canh luật đường mà ⛔ bài
    nào đổi màu là một nhánh ⛔ ai canh."""
    loi = sbt.soi((_xau(nhan),))[0]
    assert any("sai luat duong" in x for x in loi), loi


def test_R1_02_soi_noi_RO_tep_KHONG_co_that():
    """Như trên, cho nhánh *"tệp ⛔ có thật"* — bài cũ
    `test_cong_soi_DO_khi_nguon_tinh_KHONG_ton_tai` chỉ đòi tên tệp có mặt trong câu,
    mà nay câu ⓔ2 cũng mang tên ấy."""
    t = bt.Tuyen("GET", DUONG, "ty_gia", (),
                 nguon_tinh=("fls/cau_hinh/tinh/khong_co_that.json",))
    loi, _ = sbt.soi((t,))
    assert any("khong_co_that.json" in x and "co that" in x for x in loi), loi


def test_R1_02_C_nguon_tinh_la_CHUOI_thi_MOT_cau_moi_cong_KHONG_32_cau_rac():
    """R1 · C: `soi` cũ lặp trên CHUỖI ⇒ một câu MỖI KÝ TỰ *(32)*. Sai kiểu ⇒ **một**
    câu kiểu mỗi cổng, nói kiểu đo được.

    ⭐⭐ `C5`: hàm `ty_gia` nay ĐỌC KHO ⇒ ⓓ''' *(kiem)* và ⓔ3 *(soi)* THÊM một câu
       *"hàm chạm `conn`/SQL thật"* — ĐÚNG *(tuyến tĩnh ⛔ được đọc kho)*. Bài này đo
       đúng điều nó sinh ra để đo: câu **kiểu** phải là **MỘT** *(⛔ 32 rác)*."""
    t = _xau("C")
    k = [x for x in bt.kiem_bang_tuyen((t,)) if "nguon_tinh" in x and "str" in x]
    s = [x for x in sbt.soi((t,))[0] if "nguon_tinh" in x and "str" in x]
    assert len(k) == 1, k
    assert len(s) == 1, s


def test_R1_02_tuyen_TINH_ma_ham_DOC_KHO_thi_HAI_cong_DO_bang_cau_RIENG():
    """A3 — khai **nhất quán** *(`bang=()`, nguồn tĩnh đúng khuôn)* mà hàm THẬT đọc kho.

    Bản khai ⛔ tự mâu thuẫn ⇒ luật HÌNH ⛔ thấy gì. Hai câu RIÊNG của tuyến tĩnh:
      · `kiem_bang_tuyen` ⓓ''': hàm xử lý gọi tên **`conn`** *(cửa duy nhất tới kho —
        hợp đồng tầng 7)*;
      · `soi` ⓔ3: SQL thật trên đồ thị gọi chạm `fls_itl` — ⛔ chỉ nhờ câu ⓐ cũ
        *("SQL cham … ma `bang` ⛔ khong khai")*, vì ⓐ IM khi bản khai cũng ghi bảng.
    """
    t = _xau("A3")
    assert any("conn" in x and "`so`" in x for x in bt.kiem_bang_tuyen((t,))), (
        bt.kiem_bang_tuyen((t,)))
    loi = sbt.soi((t,))[0]
    assert any("nguon_tinh" in x and "fls_itl" in x for x in loi), loi
    # Đ5 chiều kia: hàm THẬT của tuyến tĩnh ⛔ chạm `conn` ⇒ ⛔ đỏ nhầm.
    assert bt.kiem_bang_tuyen(tuple(_tuyen_fx())) == []


def test_R1_02_kiem_DO_khi_khai_CA_bang_LAN_nguon_tinh_du_ham_SACH():
    """Luật *"tuyến TĨNH hay tuyến KHO, ⛔ cả hai"* phải có bài RIÊNG: với A2 *(hàm
    `so`)* luật `conn` cũng đỏ, nên gỡ luật này ⛔ bài nào đổi màu *(đột biến G2 — đo
    ở vòng sửa)*. Ở đây hàm SẠCH *(`ty_gia`)*: chỉ bản khai sai."""
    t = bt.Tuyen("GET", DUONG, "ty_gia", ("fls_itl",), nguon_tinh=(NGUON_TINH,))
    loi = bt.kiem_bang_tuyen((t,))
    assert any("CUNG `bang`" in x for x in loi), loi


def test_R1_02_ham_cua_tuyen_TINH_KHONG_co_trong_HAM_thi_DO__do_khong_duoc():
    """`Đ5`: ⛔ tìm thấy hàm ⇒ ⛔ đo được nó có chạm `conn` ⇒ ĐỎ, ⛔ "không thấy"."""
    t = bt.Tuyen("GET", f"{V}/x", "ham_khong_co_that", (), nguon_tinh=(NGUON_TINH,))
    assert any("ham_khong_co_that" in x and "do duoc" in x
               for x in bt.kiem_bang_tuyen((t,))), bt.kiem_bang_tuyen((t,))


# ⭐⭐ `C5` (`WO-142`): bài `test_R1_02_soi_do_THAT_thay_ham_ty_gia_mang_chuoi_NGUON_TINH`
#    đã GỠ — tiền đề *"`ty_gia` mang chuỗi `NGUON_TINH` trong đồ thị gọi"* bị bước này
#    **lật** *(handler nay đọc KHO, ⛔ còn đọc tệp tĩnh)*. Phép canh `chuoi_cua_tuyen`
#    vẫn được ⓔ2 dùng cho tuyến tĩnh SYNTHETIC *(bài dưới)*.


def test_R1_02_soi_DO_khi_ham_KHONG_mang_chuoi_khai():
    """GATE ⓔ2 *(tuyến tĩnh SYNTHETIC)*: tuyến khai `nguon_tinh=(X,)` mà ⛔ hàm nào
    trong `vet` mang chuỗi `X` ⇒ bản đồ vẽ một nguồn hàm ⛔ đọc *(`BG-076` yếu #3)*.
    Bơm `do_chuoi` giả trả một đường KHÁC."""
    t = bt.Tuyen("GET", DUONG, "ty_gia", (), nguon_tinh=(NGUON_TINH,))
    loi, _ = sbt.soi((t,), do_chuoi=lambda _ham: {"fls/cau_hinh/tinh/khac.json"})
    assert any("nguon_tinh" in x and NGUON_TINH in x for x in loi), loi


# ── C1-R1-07 *(GHI NHẬN — làm luôn)*: `meta` khai một phạm vi ⛔ được áp ─────
@pytest.mark.pg
def test_R1_07_run_id_o_tuyen_TINH_thi_400_KHONG_tra_so_khoac_pham_vi_lan_nap(may):
    """R1 gọi máy thật `GET /config/fx?run_id=NAP-2026-01-01-X` ⇒ `200` với
    `meta.pham_vi = 'lan nap NAP-2026-01-01-X'` mà `data` **trùng khít** lượt trơn
    *(bảng tĩnh ⛔ theo lần nạp)* ⇒ `meta` *(lời khai VỀ số — `INV-I14`)* nói một phạm
    vi ⛔ được áp. Chọn: **từ chối** `run_id` — xem lý do ở `fls/api/xu_ly.py:ty_gia`.
    """
    ma, r = _goi(may, f"{DUONG}?run_id=NAP-2026-01-01-X")
    assert ma == 400 and r["error"]["code"] == "FLS-BAD-REQUEST", (ma, r)
    assert r["data"] is None, r
    # Đ5 chiều kia: lượt trơn vẫn 200 *(⛔ chặn nhầm mọi lượt gọi)*.
    ma, r = _goi(may, DUONG)
    assert ma == 200 and r["meta"]["run_id"] is None, (ma, r["meta"])


# ── AC-5 · kho RỖNG ⇒ handler dịch `ChuaKhai`→409, `BangLa`→404 *(có TÊN)* ─────────
def _nem(exc):
    def _f(_conn):
        raise exc
    return _f


def test_AC5_handler_dich_ChuaKhai_409_va_BangLa_404_KHONG_roi_ve_anh_tinh(monkeypatch):
    """AC-5: kho RỖNG *(chưa nạp)* ⇒ handler `ty_gia` NỔ lỗi **có TÊN**, ⛔ rơi về ảnh
    tĩnh. Hai câu KHÁC nhau: `ChuaKhai`→`409 FLS-CAUHINH-CHUA-KHAI` *(có bảng, chưa
    nạp)* ≠ `BangLa`→`404 FLS-CAUHINH-BANG-LA` *(nguồn lạ)*.

    ⚠ Kho `fls_test` dùng chung đã có `IX.FX` ⇒ ⛔ dọn được để đo 409 qua máy thật;
      đo THẲNG phép **dịch lỗi** của handler *(stub ranh giới repo, ⛔ mock kho —
      dữ liệu không dự phần)*. Hai loại lỗi đã chứng ở kho thật tại
      `tests/cau_hinh/test_kho_cau_hinh_pg.py`."""
    from fls.api import bao, xu_ly
    yc = xu_ly.YeuCau(conn=None, pv=xu_ly.pham_vi_cua_yeu_cau({}), q={}, tham={})

    monkeypatch.setattr(chc, "doc_fx", _nem(chc.ChuaKhai("kho rỗng")))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.ty_gia(yc)
    assert e.value.ma == "FLS-CAUHINH-CHUA-KHAI" and bao.MA_LOI[e.value.ma][0] == 409

    monkeypatch.setattr(chc, "doc_fx", _nem(chc.BangLa("nguồn lạ")))
    with pytest.raises(xu_ly.LoiCua) as e2:
        xu_ly.ty_gia(yc)
    assert e2.value.ma == "FLS-CAUHINH-BANG-LA" and bao.MA_LOI[e2.value.ma][0] == 404


# ══ Vòng sửa sau R1 (KQ-144) ══════════════════════════════════════════════════════
#
# `C5-R1-04`: một bản `IX.FX` BẨN trong kho *(ghi thẳng SQL, ⛔ qua `nap`)* ⇒ tuyến
# ra lỗi CÓ TÊN, ⛔ `500 FLS-INTERNAL`. Sổ: SO_PHAT_HIEN_ISP-3.1_C5.md.
def test_C5R1_04_handler_ty_gia_BAN_HONG_loi_CO_TEN_khong_500(monkeypatch):
    """`doc_fx` ra `BanHong` ⇒ `ty_gia` dịch `LoiCua FLS-CAUHINH-BAN-HONG` *(500 có
    TÊN)*, ⛔ lọt `except Exception` ⇒ `FLS-INTERNAL` *(R1: `LoiFX` trần ⇒ 500 câm)*."""
    from fls.api import bao, xu_ly
    yc = xu_ly.YeuCau(conn=None, pv=xu_ly.pham_vi_cua_yeu_cau({}), q={}, tham={})
    monkeypatch.setattr(chc, "doc_fx", _nem(chc.BanHong("ban IX.FX hong")))
    with pytest.raises(xu_ly.LoiCua) as e:
        xu_ly.ty_gia(yc)
    assert e.value.ma == "FLS-CAUHINH-BAN-HONG" and bao.MA_LOI[e.value.ma][0] == 500


# ══ Vòng sửa sau R2 (`KQ-078`) ══════════════════════════════════════════════
#
# ⛔⛔ Vì sao khối này tồn tại: R2 đột biến bản sao `59d4a39` — **7** đột biến SỐNG trên
#    bộ 150 bài; ba cái ở hai cổng bảng tuyến là **chốt mà CHÚ THÍCH hứa** nhưng ⛔ bài
#    ghim *(tái phạm đúng luật `C1-R1-04`)*: `!= ()` → truthy ở `kiem_bang_tuyen`
#    *(R2-g1)* và ở `soi` *(R2-s1)* · bỏ đệ quy khối lồng của `_ten_trong_ma` *(R2-g2)*.
#    Thêm hai mép R2 dò ra: luật `conn` đo **một tầng** *(`C1-R2-03` — mẫu số)* và ⓔ
#    chỉ đo **một chiều** *(`C1-R2-04` — Đ5)*. Mỗi bài ghi đột biến nó giết.


# ── C1-R2-02 · chốt chú thích hứa *(GHI NHẬN — làm luôn; bài R2 đề xuất, chép)* ──
@pytest.mark.parametrize("gt", [None, []], ids=["None", "list_rong"])
def test_R2_02a_nguon_tinh_None_hay_RONG_o_tuyen_CO_bang_thi_HAI_cong_DO(gt):
    """`bang_tuyen.py` ⓓ'' hứa *"⛔ `if t.nguon_tinh:` — `None`/`[]` falsy mà vẫn SAI
    KIỂU"* ⇒ giết R2-g1 *(`!= ()` → truthy ở `kiem_bang_tuyen`)* và R2-s1 *(ở `soi`)*.

    Vì sao phải là tuyến **CÓ `bang`**: với `bang=()` luật cũ *"⛔ khai bảng nào"* đỏ
    thay *(`not t.bang and not t.nguon_tinh`)* — chốt `!= ()` ⛔ còn là thứ duy nhất
    đứng giữa. Dưới hai đột biến, tuyến kho `so` + `nguon_tinh=None` ⇒ **cả hai cổng
    XANH** *(R2 đo)*.
    """
    so = next(t for t in bt.BANG_TUYEN if t.ham == "so")
    t = bt.Tuyen("GET", f"{V}/x", "so", so.bang, nguon_tinh=gt)
    assert any("nguon_tinh" in x for x in bt.kiem_bang_tuyen((t,))), (
        bt.kiem_bang_tuyen((t,)))
    assert any("nguon_tinh" in x for x in sbt.soi((t,))[0]), sbt.soi((t,))[0]


def _h_long(yc):
    return (lambda: yc.conn)()          # `conn` CHỈ ở khối lồng


def test_R2_02b_luat_conn_THAY_ca_KHOI_LONG(monkeypatch):
    """`_ten_trong_ma` hứa *"kể cả khối lồng (hàm/lambda/biểu thức sinh)"* ⇒ giết R2-g2
    *(bỏ đệ quy `co_consts`)*: hàm mà tên `conn` chỉ nằm trong một `lambda` vẫn phải
    bị luật ⓓ''' gọi tên."""
    monkeypatch.setitem(HAM, "r2_h_long", _h_long)
    t = bt.Tuyen("GET", f"{V}/x", "r2_h_long", (), nguon_tinh=(NGUON_TINH,))
    assert any("conn" in x for x in bt.kiem_bang_tuyen((t,))), (
        bt.kiem_bang_tuyen((t,)))


# ── C1-R2-03 · luật `conn` đo MỘT tầng — ghim GIỚI HẠN + mẫu số ─────────────────
@pytest.mark.parametrize("ham", ["xem_truoc", "lo_xem_truoc"])
def test_R2_03_ham_trao_NGUYEN_yc_cho_ham_phu_LOT_luat_conn__chi_soi_bat(ham):
    """Giới hạn ĐÃ KHAI của ⓓ''' *(`bang_tuyen.py:_tinh_ma_cham_ket_noi`, `BG-076` yếu
    #1 vòng R1)* — nay **ghim**, ⛔ chỉ khai *(luật `C1-R2-03`)*.

    Mẫu số *(đo trên `HAM` thật, cây vòng sửa R2)*: **3/41** hàm ⛔ gọi tên `conn` ở
    tầng đầu = `ty_gia` *(đúng — tuyến tĩnh)* + **2** hàm ĐỌC KHO `xem_truoc` ·
    `lo_xem_truoc` *(trao nguyên `yc` cho `_dung_lo` / `_soat_lo` ở `nap_cua.py`)* ⇒
    **2** trong **40** hàm còn lại *(41 trừ `ty_gia`)* lọt ⓓ'''. Khai một trong hai
    thành tuyến tĩnh đúng khuôn:
      · `kiem_bang_tuyen` **XANH** — giới hạn; nếu bài này đỏ ở vế ấy vì ⓓ''' đã bám
        được hàm phụ thì đó là TIẾN BỘ: viết lại vế này + câu giới hạn trong mã;
      · `soi` **ĐỎ** bằng câu ⓔ3 *(SQL thật trên cả đồ thị gọi chạm bảng)* — lưới đỡ.
    ⇒ Câu *"CẢ HAI cổng cùng đỏ"* của `test_R1_02_…` đúng cho tập tuyến R1 *(hàm `so`
      gọi tên `conn`)*, ⛔ cho mọi hàm — bài này nói phần còn lại.
    """
    assert ham in HAM, f"⛔ `{ham}` ⛔ còn trong `HAM` — mẫu số đổi, đo lại"
    t = bt.Tuyen("GET", f"{V}/x", ham, (), nguon_tinh=(NGUON_TINH,))
    assert bt.kiem_bang_tuyen((t,)) == [], (
        f"ⓓ''' nay THẤY `{ham}` chạm kho — tiến bộ: viết lại vế này + câu giới hạn ở "
        f"`_tinh_ma_cham_ket_noi`: {bt.kiem_bang_tuyen((t,))}")
    loi = sbt.soi((t,))[0]
    assert any("tuyen `nguon_tinh` ma SQL that cham" in x for x in loi), loi


# ── C1-R2-04 · ⓔ4: đồ thị gọi MANG đường tĩnh mà tuyến ⛔ khai *(Đ5 hai chiều)* ──
@pytest.mark.parametrize("nhan", ["kho_khong_khai", "tinh_khai_thieu"])
def test_R2_04_soi_DO_khi_do_thi_MANG_duong_tinh_ma_tuyen_KHONG_khai(nhan):
    """ⓔ2 đo chiều **khai ⊆ thật** *(đường khai phải có trong đồ thị gọi)*; chiều
    **thật ⊆ khai** ⛔ có tới R2 *(grep `tools/` + `fls/` = 0)*: R2 bơm đường
    `ix_fx_mau.json` vào đồ thị của tuyến kho `so` *(`nguon_tinh=()`)* ⇒ `soi` XANH ·
    `kiem_bang_tuyen` XANH. Hai ca:
      · `kho_khong_khai` — bài R2 đề xuất, chép: tuyến KHO ⛔ khai nguồn tĩnh nào;
      · `tinh_khai_thieu` — tuyến TĨNH khai một tệp mà đồ thị mang thêm tệp thứ hai.
    """
    khac = "fls/cau_hinh/tinh/khac.json"
    if nhan == "kho_khong_khai":
        so = next(t for t in bt.BANG_TUYEN if t.ham == "so")
        t, bom = bt.Tuyen("GET", f"{V}/x", "so", so.bang), NGUON_TINH
    else:
        # ⭐⭐ `C5`: tuyến tĩnh SYNTHETIC *(tuyến tĩnh THẬT đã GỠ)*.
        t, bom = bt.Tuyen("GET", DUONG, "ty_gia", (), nguon_tinh=(NGUON_TINH,)), khac
    that = sbt.sql_cua_tuyen(t.ham)
    loi, _ = sbt.soi((t,), do_sql=lambda _h: that,
                     do_chuoi=lambda h: sbt.chuoi_cua_tuyen(h) | {bom})
    assert any("nguon_tinh" in x and bom in x for x in loi), loi
    assert all("\n" not in x for x in loi), loi


def test_R2_04_e4_KHONG_do_nham_tren_bang_THAT():
    """`Đ5` chiều kia: trên bảng tuyến THẬT ⓔ4 ⛔ đỏ nhầm.

    ⭐⭐ `C5` (`WO-142`): sau khi GỠ hai tuyến tĩnh *(C1 · C4)*, **⛔ tuyến THẬT nào**
       mang chuỗi dưới `fls/cau_hinh/tinh/` trong đồ thị gọi ⇒ tập ⓔ4 so là **RỖNG**
       trên mọi tuyến *(⛔ còn ảnh tĩnh)* — và `soi()` vẫn xanh."""
    from fls.cau_hinh import nguon_tinh
    tien_to = nguon_tinh.THU_MUC + "/"
    mang = {t.duong: sorted(x for x in sbt.chuoi_cua_tuyen(t.ham)
                            if x.startswith(tien_to))
            for t in bt.BANG_TUYEN}
    mang = {k: v for k, v in mang.items() if v}
    assert mang == {}, (
        f"⛔ `C5` GỠ mọi tuyến tĩnh — ⛔ tuyến nào mang đường dưới {tien_to}: {mang}")
    assert sbt.soi()[0] == []
