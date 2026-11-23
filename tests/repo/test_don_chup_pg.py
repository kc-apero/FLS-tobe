"""`A2` — DỌN ẢNH CHỤP. `QĐ-ITL-115`.

⛔⛔⛔ **Điều kiện của owner là một câu ĐO ĐƯỢC, ⛔ không phải một khoảng thời
   gian:** *"lý do giữ dòng thô là để chứng minh một bút toán đến TỪ ĐÂU ⇒ ảnh
   ⛔ không bút toán nào trỏ tới thì nó ⛔ không chứng minh gì"*.

⇒ Nên bài đắt nhất ở đây ⛔ **không phải** *"xoá đúng 30 ngày"* — nó là
  `test_anh_DA_NAP_song_sot_du_GIA_bao_nhieu`. Một phép dọn xoá mất một ảnh
  **đã được nạp** sẽ làm lô ấy **mất căn cứ**, và ⛔ không gì báo: `fls_itl` vẫn
  đủ dòng, `fls_run` vẫn còn, chỉ có `chup_id` trỏ vào **hư không**.

★ Và ba bài còn lại canh ba cách phép dọn **hỏng theo hướng ngược lại**:
  ⓐ dọn mà ⛔ không xoá gì *(cổng chung #7 — chưa biết nó có sống)*;
  ⓑ báo cáo chỉ nói vế XOÁ ⇒ ⛔ không ai duyệt được;
  ⓒ `giu_ngay = 0` ⇒ NỔ *(nó sẽ xoá cả ảnh vừa chụp xong đang chờ người bấm)*.
"""
from __future__ import annotations

import uuid

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import chup as ch
from fls.repo.don_chup import GIU_NGAY, do_don, don_anh_chup

pytestmark = pytest.mark.pg

ACTOR = "cron@fls"


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


@pytest.fixture()
def nguon(conn):
    return conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s,'PM') RETURNING source_id",
        ("PM don " + _hex(),)).fetchone()[0]


def _anh(conn, nguon: int, *, tuoi_ngay: int, da_nap: bool) -> int:
    """Một ảnh lằn `PM` với **tuổi đặt tay**, tuỳ chọn có một lần nạp trỏ tới.

    ⚠ Lùi `doc_luc` bằng một câu `UPDATE` **của bài kiểm**, ⛔ không phải của
      `fls/` — tầng ảnh chụp bị cổng quét mã nguồn cấm mọi câu sửa, và cổng ấy
      ⛔ không được nới chỉ để dựng một kho bài.
    """
    a = ch.ghi_chup_pm(conn, spreadsheet_id="SID-" + _hex(), actor="dev",
                       source_id=nguon, khai_version=1)
    conn.execute("UPDATE fls_chup SET doc_luc = now() -"
                 " make_interval(days => %s) WHERE chup_id = %s",
                 (tuoi_ngay, a.chup_id))
    if da_nap:
        conn.execute(
            "INSERT INTO fls_run (run_id, contract_version, canon_version,"
            " mapping_version, chup_id) VALUES (%s,'v1.0','v1.0','v1.0',%s)",
            (f"NAP-2000-01-01-DON{_hex()}", a.chup_id))
    return a.chup_id


def _con(conn, cid: int) -> bool:
    return conn.execute("SELECT count(*) FROM fls_chup WHERE chup_id=%s",
                        (cid,)).fetchone()[0] == 1


# ── ⭐⭐⭐ ẢNH ĐÃ NẠP: ⛔ KHÔNG BAO GIỜ bị xoá ────────────────────────────
def test_anh_DA_NAP_song_sot_du_GIA_bao_nhieu(conn, nguon):
    """⭐⭐⭐ **Bài đắt nhất của mốc `A2`.**

    Ảnh **999 ngày** tuổi — gấp hơn **33 lần** ngưỡng — mà có một lần nạp trỏ
    tới thì nó **⛔ KHÔNG được xoá**. Nếu xoá, lô ấy mất căn cứ và ⛔ không gì
    báo: `fls_itl` vẫn đủ dòng, `fls_run` vẫn còn, chỉ `chup_id` trỏ vào hư
    không.
    """
    gia_da_nap = _anh(conn, nguon, tuoi_ngay=999, da_nap=True)
    gia_bo_khong = _anh(conn, nguon, tuoi_ngay=999, da_nap=False)

    kq = don_anh_chup(conn, actor=ACTOR)
    assert _con(conn, gia_da_nap) is True, \
        "⛔⛔ ĐÃ XOÁ một ảnh ĐÃ ĐƯỢC NẠP — lô ấy vừa mất căn cứ"
    assert _con(conn, gia_bo_khong) is False
    assert kq["so_da_xoa"] >= 1


def test_anh_CON_MOI_khong_bi_xoa_du_KHONG_ai_dung(conn, nguon):
    """⭐ Ảnh mới chụp mà ⛔ chưa ai nạp là **chuyện bình thường** — nhịp mỗi
    giờ sinh 12 ảnh/ngày, và 11 trong 12 sẽ ⛔ không ai nạp. Xoá ngay là xoá
    đúng cái ảnh kế toán đang chuẩn bị bấm nhận."""
    moi = _anh(conn, nguon, tuoi_ngay=GIU_NGAY - 1, da_nap=False)
    don_anh_chup(conn, actor=ACTOR)
    assert _con(conn, moi) is True


def test_xoa_CA_BA_bang__khong_de_lai_dong_mo_coi(conn, nguon):
    """⛔ Xoá `fls_chup` mà để `fls_chup_nguon` lại là để lại một dòng trỏ vào
    hư không — và khoá ngoại sẽ **NỔ** ngay câu xoá thứ ba, giữa giao dịch."""
    cid = _anh(conn, nguon, tuoi_ngay=99, da_nap=False)
    assert conn.execute("SELECT count(*) FROM fls_chup_nguon WHERE chup_id=%s",
                        (cid,)).fetchone()[0] == 1
    kq = don_anh_chup(conn, actor=ACTOR)
    assert kq["so_nguon_da_xoa"] >= 1
    assert conn.execute("SELECT count(*) FROM fls_chup_nguon WHERE chup_id=%s",
                        (cid,)).fetchone()[0] == 0
    assert _con(conn, cid) is False


# ── phép ĐO ─────────────────────────────────────────────────────────────
def test_do_don_KHONG_xoa_mot_dong_nao(conn, nguon):
    """⛔ `do_don` là phép **CHỈ ĐO**. Một công cụ mà phép *"xem trước"* của nó
    cũng xoá là một công cụ ⛔ không ai dám chạy."""
    cid = _anh(conn, nguon, tuoi_ngay=99, da_nap=False)
    d = do_don(conn)
    assert cid in [x["chup_id"] for x in d["se_xoa"]]
    assert _con(conn, cid) is True


def test_bao_cao_noi_CA_HAI_VE__xoa_va_GIU_kem_ly_do(conn, nguon):
    """⛔⛔ Một báo cáo chỉ nói *"xoá 40"* là một báo cáo ⛔ không ai duyệt được:
    người đọc ⛔ không biết phép dọn có đúng đầu vào ⛔ không.

    ⇒ Phải nói **cả ba** con số của vế GIỮ, và chúng phải **tách theo LÝ DO**:
      giữ vì **đã nạp** *(vĩnh viễn)* ↔ giữ vì **còn mới** *(sẽ xoá sau)*.
    """
    _anh(conn, nguon, tuoi_ngay=999, da_nap=True)
    _anh(conn, nguon, tuoi_ngay=1, da_nap=False)
    _anh(conn, nguon, tuoi_ngay=99, da_nap=False)
    d = do_don(conn)
    assert d["giu_vi_da_nap"] >= 1
    assert d["giu_vi_con_moi"] >= 1
    assert d["so_se_xoa"] >= 1
    # ⭐ Ba vế cộng lại = tổng — ⛔ không dòng nào rơi ra ngoài phép phân loại
    assert (d["giu_vi_da_nap"] + d["giu_vi_con_moi"] + d["so_se_xoa"]
            == d["tong_anh"])
    # ⛔ Và mỗi ảnh sẽ xoá phải nêu **CHÍNH NÓ**, ⛔ không chỉ một con số
    for x in d["se_xoa"]:
        assert x["chup_id"] and x["doc_luc"] and x["lan"]


def test_giu_ngay_0_thi_NO(conn):
    """⛔ `0` nghĩa là *xoá mọi ảnh chưa nạp NGAY HÔM NAY* — kể cả ảnh vừa chụp
    xong đang chờ người bấm nhận. Nó ⛔ không phải một lựa chọn hợp lệ."""
    with pytest.raises(ValueError) as e:
        do_don(conn, giu_ngay=0)
    assert str(GIU_NGAY) in str(e.value)


def test_thieu_actor_thi_NO(conn):
    with pytest.raises(ValueError):
        don_anh_chup(conn, actor="  ")


def test_khong_co_gi_de_xoa_thi_bao_0_chu_khong_NO(conn, nguon):
    """⛔ Một lượt dọn ⛔ không xoá gì là một lượt **THÀNH CÔNG**. Nổ ở đây sẽ
    làm nhịp cron báo sự cố mỗi ngày trong 30 ngày đầu."""
    _anh(conn, nguon, tuoi_ngay=1, da_nap=False)
    kq = don_anh_chup(conn, actor=ACTOR, giu_ngay=100000)
    assert kq["so_da_xoa"] == 0 and kq["actor"] == ACTOR
