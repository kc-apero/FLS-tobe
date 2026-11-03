"""Di tru tren PG that. Cong quan trong nhat: test_migration_toi_dung_schema.

Do la cho noi hai nguon su that — schema.py (trang thai mong doi) va
fls/db/migrations/ (duong di). Thieu no thi hai nguon se troi khoi nhau.
"""

import os

import psycopg
import pytest

from fls.db import pg_migrate
from fls.db.migration_runner import LEDGER, MIGRATIONS, checksum_of, kiem_lich_su
from fls.db.pg_verify import so_sanh_voi_db

pytestmark = pytest.mark.pg

DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")


@pytest.fixture()
def schema_trong():
    """Mot schema PG rong, tu don sau khi xong."""
    ten = "thu_" + os.urandom(4).hex()
    with psycopg.connect(DSN, autocommit=True) as c:
        with c.cursor() as cur:
            cur.execute(f'CREATE SCHEMA "{ten}"')
            cur.execute(f'SET search_path TO "{ten}"')
        try:
            yield c, ten
        finally:
            with c.cursor() as cur:
                cur.execute(f'DROP SCHEMA "{ten}" CASCADE')


def test_migration_toi_dung_schema_khai_bao(schema_trong):
    """★ CONG NOI: schema trong -> ap het migration -> pg_verify PHAI xanh.

    Neu ai them cot vao schema.py ma quen viet migration, cong nay do.
    """
    conn, ten = schema_trong
    ap = pg_migrate.ap(conn)
    assert ap == [m.version for m in MIGRATIONS], ap
    lech = so_sanh_voi_db(conn, schema=ten)
    assert not lech, "migration khong toi dung schema khai bao: " + " | ".join(lech)


def test_ap_lai_khong_lam_gi_them(schema_trong):
    conn, _ = schema_trong
    pg_migrate.ap(conn)
    assert pg_migrate.ap(conn) == [], "ap lan 2 phai khong con gi de ap"


def test_so_ghi_luu_dung_checksum(schema_trong):
    conn, _ = schema_trong
    pg_migrate.ap(conn)
    with conn.cursor() as cur:
        cur.execute(f"SELECT version, name, checksum FROM {LEDGER} ORDER BY version")
        hang = cur.fetchall()
    assert [h[0] for h in hang] == [m.version for m in MIGRATIONS]
    for (v, ten, cks), m in zip(hang, MIGRATIONS):
        assert ten == m.name and cks == checksum_of(m.sql)


def test_sua_migration_da_ap_thi_NO(schema_trong):
    """⛔ Sua file da deploy = lich su khac nhau giua cac moi truong."""
    conn, _ = schema_trong
    pg_migrate.ap(conn)
    with conn.cursor() as cur:
        cur.execute(f"UPDATE {LEDGER} SET checksum = 'gia' WHERE version = 1")
    with pytest.raises(RuntimeError, match="DA BI SUA"):
        pg_migrate.ap(conn)


def test_kiem_lich_su_bat_migration_bien_mat():
    lech = kiem_lich_su({999: "abc"}, MIGRATIONS)
    assert lech and "KHONG con trong code" in lech[0]


def test_cot_them_vao_schema_ma_quen_migration_thi_verify_DO(schema_trong):
    """Chung minh cong noi song: gia lap "quen viet migration"."""
    from fls.db.model import Column
    from fls.db.schema import TABLES

    conn, ten = schema_trong
    pg_migrate.ap(conn)
    goc = TABLES["fls_le"]
    gia = dict(TABLES)
    gia["fls_le"] = type(goc)(
        name=goc.name, kind=goc.kind, erd_entity=goc.erd_entity,
        island_reason=goc.island_reason, view_sql=goc.view_sql,
        columns=goc.columns + (Column("cot_quen_migration", "text"),))
    lech = so_sanh_voi_db(conn, tables=gia, schema=ten)
    assert any("cot_quen_migration" in m for m in lech), lech
