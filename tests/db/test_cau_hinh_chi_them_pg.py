# -*- coding: utf-8 -*-
"""`C5-B3` — `fls_cau_hinh_ban` / `fls_cau_hinh_dong` là kho **CHỈ-THÊM** trên PG THẬT
*(di trú `0027`)*.

⛔⛔ Cùng luật `fls_itl` *(`INV-I03`/`INV-I08`, di trú `0001`/`0015`)*: một câu
   `UPDATE`/`DELETE` lên bảng config là một đường **viết lại lịch sử** — sửa config =
   **nạp phiên bản mới**, ⛔ sửa bản cũ. Trigger phải NỔ với **TÊN** *(luật `S0-R1-04`:
   phép chặn đỏ in nguyên nhân đọc được trong một dòng)*, ⛔ `ValueError` trơn.

⛔ Bài `tests/db/test_schema_*` chỉ đọc **bản khai Python** — một trigger khai mà ⛔ ap
   xuống kho thì bản khai vẫn xanh còn kho vẫn cho `UPDATE`. ⇒ Bài này **chạm kho thật**.
"""
import os

import psycopg
import pytest

from fls.db.kho import dsn_test

pytestmark = pytest.mark.pg

DSN = dsn_test()
BANG = "IX.FX"


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _mot_ban(cur) -> tuple[int, int]:
    """Một `(ban_id, dong_id)` riêng cho mỗi bài — ⛔ dùng chung."""
    ver = int(os.urandom(4).hex(), 16) % 2_000_000_000 + 1
    cur.execute(
        "INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
        "VALUES (%s,%s,'nguon-thu','ck-thu','thu') RETURNING ban_id",
        (BANG, ver))
    bid = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
        "VALUES (%s,'202401',%s) RETURNING dong_id",
        (bid, '{"USD": "1"}'))
    did = cur.fetchone()[0]
    return bid, did


def test_luc_do_MAY_dat_khong_truyen_vao(conn):
    """`luc` NOT NULL DEFAULT now() — máy đặt, như `fls_khai_cot.hieu_luc_tu`."""
    with conn.cursor() as cur:
        bid, _ = _mot_ban(cur)
        cur.execute("SELECT luc FROM fls_cau_hinh_ban WHERE ban_id = %s", (bid,))
        assert cur.fetchone()[0] is not None


def test_UPDATE_ban_BI_CHAN_co_TEN(conn):
    with conn.cursor() as cur:
        bid, _ = _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e:
            cur.execute("UPDATE fls_cau_hinh_ban SET nguon = 'x' WHERE ban_id = %s",
                        (bid,))
        assert "INV-I08" in str(e.value) and "fls_cau_hinh_ban" in str(e.value)


def test_DELETE_ban_BI_CHAN_co_TEN(conn):
    with conn.cursor() as cur:
        bid, _ = _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e:
            cur.execute("DELETE FROM fls_cau_hinh_ban WHERE ban_id = %s", (bid,))
        assert "INV-I08" in str(e.value)


def test_UPDATE_dong_BI_CHAN_co_TEN(conn):
    with conn.cursor() as cur:
        _, did = _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e:
            cur.execute("UPDATE fls_cau_hinh_dong SET gia_tri = %s WHERE dong_id = %s",
                        ('{"USD": "999"}', did))
        assert "INV-I08" in str(e.value) and "fls_cau_hinh_dong" in str(e.value)


def test_DELETE_dong_BI_CHAN_co_TEN(conn):
    with conn.cursor() as cur:
        _, did = _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e:
            cur.execute("DELETE FROM fls_cau_hinh_dong WHERE dong_id = %s", (did,))
        assert "INV-I08" in str(e.value)


def test_TRUNCATE_BI_CHAN(conn):
    """⛔ Bẫy `0015`: `INV-I03` chặn `DELETE` nhưng ⛔ `TRUNCATE`. Bảng config đóng
    luôn lỗ ấy — trigger `BEFORE TRUNCATE` NỔ *(dựng lại kho TEST đi đường
    `DROP DATABASE`)*.

    ⚠ `TRUNCATE` bảng con `fls_cau_hinh_dong` *(⛔ ai tham chiếu nó)* ⇒ trigger
       là thứ DUY NHẤT chặn. Bảng cha `fls_cau_hinh_ban` một mình thì FK đã chặn
       *(`FeatureNotSupported`)*, nên đo `TRUNCATE … CASCADE` để trigger của nó
       chạy TRƯỚC khi xoá."""
    with conn.cursor() as cur:
        _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e1:
            cur.execute("TRUNCATE fls_cau_hinh_dong")
        assert "INV-I08" in str(e1.value)
    with conn.cursor() as cur:
        _mot_ban(cur)
        with pytest.raises(psycopg.errors.RaiseException) as e2:
            cur.execute("TRUNCATE fls_cau_hinh_ban CASCADE")
        assert "INV-I08" in str(e2.value)


def test_UNIQUE_bang_phien_ban(conn):
    """Hai bản cùng `(bang, phien_ban)` là hai nguồn sự thật ⇒ `UNIQUE` chặn."""
    ver = int(os.urandom(4).hex(), 16) % 2_000_000_000 + 1
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_cau_hinh_ban (bang,phien_ban,nguon,checksum,"
                    "actor) VALUES (%s,%s,'n','c','a')", (BANG, ver))
        with pytest.raises(psycopg.errors.UniqueViolation):
            cur.execute("INSERT INTO fls_cau_hinh_ban (bang,phien_ban,nguon,"
                        "checksum,actor) VALUES (%s,%s,'n','c','a')", (BANG, ver))


def test_dong_FK_ban_KHONG_co_that_BI_CHAN(conn):
    with conn.cursor() as cur:
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            cur.execute("INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
                        "VALUES (%s,'k',%s)", (10**15, '{}'))


# ══ Vòng sửa sau R1 (KQ-144) ══════════════════════════════════════════════════════
def test_C5R1_05_luc_xap_xi_now_KHONG_phai_hang_chet(conn):
    """GHI NHẬN `C5-R1-05`: giết R1-M24 *(`DEFAULT now()` → `'2000-01-01'` ⇒ `luc`
    thành hằng CHẾT mà bài `is not None` ⛔ bắt)*. `luc` do MÁY đặt ⇒ phải XẤP XỈ
    `now()` của chính kho *(cùng chiều `fls_khai_cot.hieu_luc_tu`)*."""
    with conn.cursor() as cur:
        bid, _ = _mot_ban(cur)
        cur.execute("SELECT luc, now() FROM fls_cau_hinh_ban WHERE ban_id = %s", (bid,))
        luc, bay_gio = cur.fetchone()
    assert abs((bay_gio - luc).total_seconds()) < 300, (luc, bay_gio)


def test_C5R1_06_pg_verify_BAT_khi_trigger_bi_TAT(conn):
    """GHI NHẬN `C5-R1-06`: chủ bảng *(⛔ superuser)* `ALTER TABLE … DISABLE TRIGGER`
    rồi UPDATE/DELETE — một LỐI VÒNG qua `INV-I08`. ⛔ sửa quyền ở bước này; chỉ đòi
    `pg_verify` **BẮT** mọi trigger người dùng bị TẮT *(Đ5 hai chiều: tắt ⇒ đỏ, bật
    lại ⇒ ⛔ đỏ nhầm)*."""
    from fls.db import pg_verify
    tt = "trg_fls_cau_hinh_dong_chi_them"

    def _tat_trong_lech():
        return [x for x in pg_verify.so_sanh_voi_db(conn) if tt in x and "TAT" in x]

    assert _tat_trong_lech() == [], "⛔ tiền đề: trigger đang BẬT"
    with conn.cursor() as cur:
        cur.execute(f"ALTER TABLE fls_cau_hinh_dong DISABLE TRIGGER {tt}")
    try:
        assert _tat_trong_lech(), "⛔ pg_verify ⛔ bắt trigger bị TẮT"
    finally:
        with conn.cursor() as cur:
            cur.execute(f"ALTER TABLE fls_cau_hinh_dong ENABLE TRIGGER {tt}")
    assert _tat_trong_lech() == [], "⛔ bật lại ⇒ ⛔ còn đỏ"
