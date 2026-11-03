"""Cong thu 5: DB THAT phai khop schema khai bao.

Vi sao can: pg_migrate dung CREATE TABLE IF NOT EXISTS. Bang da ton tai thi
lenh BO QUA trong im lang, ma van in "da ap N cau DDL" — bao THANH CONG trong
khi ap THIEU. Da gap that 2026-08-26: them FK run_id, chay migration, bao
thanh cong, FK khong he duoc them.
"""

import os

import psycopg
import pytest

from fls.db.pg_verify import so_sanh_voi_db

pytestmark = pytest.mark.pg

DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def test_db_that_khop_schema_khai_bao(conn):
    lech = so_sanh_voi_db(conn)
    assert not lech, "DB that lech schema khai bao: " + " | ".join(lech)


def test_verify_bat_duoc_cot_bi_thieu(conn):
    """Chung minh cong song: bo mot cot khoi DB roi xem verify co bat khong."""
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
