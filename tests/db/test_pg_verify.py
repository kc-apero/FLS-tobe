"""Cong thu 5: DB THAT phai khop schema khai bao.

Vi sao can: pg_migrate dung CREATE TABLE IF NOT EXISTS. Bang da ton tai thi
lenh BO QUA trong im lang, ma van in "da ap N cau DDL" — bao THANH CONG trong
khi ap THIEU. Da gap that 2026-08-26: them FK run_id, chay migration, bao
thanh cong, FK khong he duoc them.
"""

import psycopg
import pytest

from fls.db.kho import dsn_that, dsn_test, noi_chi_doc
from fls.db.pg_verify import so_sanh_voi_db

pytestmark = pytest.mark.pg

# ⭐ File nay CO Y soi kho THAT (kho phai khop ban khai). Nhung no mo bang
# ket noi **CHI DOC** — PostgreSQL tu tu choi moi phep ghi, nen no ⛔ khong
# the lam ban so nhu 4 file test PG kia tung lam. Xem `fls/db/kho.py`.
DSN = dsn_that()


@pytest.fixture()
def conn():
    """⛔ CHI DOC: moi phep ghi len kho that bi PostgreSQL tu choi."""
    c = noi_chi_doc(DSN)
    try:
        yield c
    finally:
        c.close()


def test_db_that_khop_schema_khai_bao(conn):
    lech = so_sanh_voi_db(conn)
    assert not lech, "DB that lech schema khai bao: " + " | ".join(lech)


@pytest.fixture()
def conn_test():
    """⛔ Kho TEST: bai duoi DUNG BANG THAT (DDL) nen ⛔ khong duoc cham kho that.

    Bat duoc 27/08 boi chinh chot chi-doc phia tren: bai nay tung `CREATE TABLE`
    thang vao kho that ma khong ai thay.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def test_verify_bat_duoc_cot_bi_thieu(conn_test):
    """Chung minh cong song: bo mot cot khoi DB roi xem verify co bat khong."""
    conn = conn_test
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS fls_le_thu_nghiem (le_code text)")
    try:
        from fls.db.model import Column, Table
        gia = {"fls_le_thu_nghiem": Table(
            name="fls_le_thu_nghiem",
            columns=(Column("le_code", "text"), Column("cot_khong_co", "text")))}
        lech = so_sanh_voi_db(conn, tables=gia)
        assert any("cot_khong_co" in m for m in lech), lech
    finally:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS fls_le_thu_nghiem")
