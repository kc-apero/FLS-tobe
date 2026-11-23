# -*- coding: utf-8 -*-
"""`fls/repo/nguon_dai.py` trên PG THẬT — bản khai **THỨ HAI** (`GAP-KHAI-01`).

⭐ Cổng: chạy lại công cụ thu ⇒ **⛔ 0 dòng rác**; danh mục đổi ⇒ **thêm dòng**,
   ⛔ **không sửa dòng cũ**.
"""
import os

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo.nguon_dai import BA_TRUONG, LoiDai, cot_tu_dai, doc_dai, ghi_dai

pytestmark = pytest.mark.pg

DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _nguon(conn) -> int:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_source (source_key, src_type) "
                    "VALUES (%s,'Bank') RETURNING source_id",
                    ("R | Dai" + os.urandom(5).hex(),))
        return cur.fetchone()[0]


DAI = {"Date": "!L3:L", "Debit": "!M3:M", "Credit": "!N3:N"}


# ── phép bóc dải ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("s,mong", [
    ("!L3:L", 11), ("!M3:M", 12), ("!N3:N", 13),
    ("!A3:A", 0), ("!AA3:AA", 26), ("L3:L", 11), ("!$L$3:$L", 11),
])
def test_boc_dai_ra_dung_cot(s, mong):
    assert cot_tu_dai(s) == mong, "⛔ %r phai ra cot %d" % (s, mong)


@pytest.mark.parametrize("s", ["", "   ", "!L3:N", "linh tinh", None])
def test_dai_KHONG_suy_duoc_thi_tra_None_chu_KHONG_doan(s):
    """⛔⛔ Đo 08/09: `R | CNC` và `R | Pingpong` có **6 ô `Range_*` RỖNG**.

    Đoán một cột cho ô rỗng là **tự bịa một hợp đồng đọc**, và `S10` sẽ báo
    *"khớp"* trên một thứ ⛔ chưa ai khai.
    """
    assert cot_tu_dai(s) is None


# ── tầng kho ───────────────────────────────────────────────────────────────

def test_ghi_roi_doc_lai_ra_dung(conn):
    sid = _nguon(conn)
    b = ghi_dai(conn, sid, DAI, danh_muc="BankAccountList")
    assert b is not None
    assert b.cot == {"Date": 11, "Debit": 12, "Credit": 13}
    assert b.tho == DAI
    assert b.danh_muc == "BankAccountList"
    assert doc_dai(conn, sid).cot == b.cot


def test_CHUA_THU_bao_gio_thi_tra_None_chu_KHONG_no(conn):
    """⛔ *"Chưa thu"* ⛔ không phải một lỗi — nó là một **trạng thái**."""
    assert doc_dai(conn, _nguon(conn)) is None


def test_GHI_LAI_y_het_thi_KHONG_de_dong_rac(conn):
    """⭐ Cổng chính: chạy lại công cụ thu ⇒ **⛔ 0 dòng rác**.

    ⛔⛔ Đây đúng cái bẫy đã cắn thật ở `ghi_khai` ngày 08/09: phép ghi rụng
       mất trường ⇒ phép so **luôn khác** ⇒ **mỗi lần chạy một `version` rác,
       mãi mãi**, mà ⛔ không cổng nào báo.
    """
    sid = _nguon(conn)
    ghi_dai(conn, sid, DAI, danh_muc="BankAccountList")
    for _ in range(3):
        assert ghi_dai(conn, sid, DAI, danh_muc="BankAccountList") is None
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_nguon_dai WHERE source_id = %s",
                    (sid,))
        assert cur.fetchone()[0] == 3, "⛔ co dong RAC"


def test_DANH_MUC_DOI_la_THEM_dong_cu_KHONG_doi_mot_o(conn):
    """⛔ Chỉ-thêm. Một lần nạp tháng trước phải giải thích được bằng
    **cái đã đọc lúc ấy**."""
    sid = _nguon(conn)
    ghi_dai(conn, sid, DAI, danh_muc="BankAccountList")
    with conn.cursor() as cur:
        cur.execute("SELECT dai_id, truong, cot, dai_tho FROM fls_nguon_dai"
                    " WHERE source_id = %s ORDER BY dai_id", (sid,))
        cu = cur.fetchall()

    moi = dict(DAI, Debit="!P3:P")
    b = ghi_dai(conn, sid, moi, danh_muc="BankAccountList")
    assert b is not None and b.cot["Debit"] == 15

    with conn.cursor() as cur:
        cur.execute("SELECT dai_id, truong, cot, dai_tho FROM fls_nguon_dai"
                    " WHERE source_id = %s ORDER BY dai_id", (sid,))
        sau = cur.fetchall()
    assert sau[:len(cu)] == cu, "⛔ dong CU da bi doi — vi pham chi-THEM"
    assert len(sau) == len(cu) + 3


def test_o_RONG_van_GHI_va_giu_cot_NULL(conn):
    """⛔ Ô rỗng phải **vào kho** với `cot = NULL`, ⛔ không bị bỏ qua.

    Bỏ qua thì nguồn ấy **biến mất khỏi `S10`** — đúng lớp lỗi `S8` đã cắn:
    cái vắng mặt vắng mặt **lần thứ hai**, trong im lặng.
    """
    sid = _nguon(conn)
    b = ghi_dai(conn, sid, {"Date": "", "Debit": "", "Credit": ""},
                danh_muc="Cash Ledger List")
    assert b is not None
    assert b.cot == {t: None for t in BA_TRUONG}
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_nguon_dai"
                    " WHERE source_id = %s AND cot IS NULL", (sid,))
        assert cur.fetchone()[0] == 3


def test_ten_truong_la_thi_NO(conn):
    with pytest.raises(LoiDai):
        ghi_dai(conn, _nguon(conn), {"Date": "!A3:A", "Reference number": "!B3:B"},
                danh_muc="BankAccountList")


def test_THIEU_danh_muc_thi_NO(conn):
    """⛔ Phải nói dải này đọc từ **bảng nào** — hai lằn có hai bảng."""
    with pytest.raises(LoiDai):
        ghi_dai(conn, _nguon(conn), DAI, danh_muc="  ")


def test_nguon_KHONG_co_that_thi_NO(conn):
    with pytest.raises(LoiDai):
        ghi_dai(conn, 999_999_999, DAI, danh_muc="BankAccountList")
