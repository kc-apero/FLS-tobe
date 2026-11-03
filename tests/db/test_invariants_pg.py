import os

import psycopg
import pytest

pytestmark = pytest.mark.pg

DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _dam_bao_cha(cur) -> None:
    """fls_le va fls_run la cha FK — phai co truoc khi chen dong so."""
    cur.execute("INSERT INTO fls_le (le_code, le_name) VALUES ('SGO1','SGO1') "
                "ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version, "
                "mapping_version) VALUES ('r1','v1.0','v1.0','v1.0') "
                "ON CONFLICT DO NOTHING")


def _chen_mot_dong(conn, raw_frozen: bool) -> int:
    with conn.cursor() as cur:
        _dam_bao_cha(cur)
        cur.execute("""
            INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                                 run_id, contract_version, canon_version, mapping_version,
                                 raw_frozen, canon)
            VALUES (%s,'P100','Bank',1,'r1','v1.0','v1.0','v1.0',%s,'[]'::jsonb)
            RETURNING itl_id""", (f"k-{raw_frozen}-{os.urandom(4).hex()}", raw_frozen))
        return cur.fetchone()[0]


def test_inv_i03_raw_frozen_thi_cam_update(conn):
    iid = _chen_mot_dong(conn, raw_frozen=True)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("UPDATE fls_itl SET memo='sua' WHERE itl_id=%s", (iid,))


def test_inv_i03_raw_frozen_thi_cam_delete(conn):
    iid = _chen_mot_dong(conn, raw_frozen=True)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fls_itl WHERE itl_id=%s", (iid,))


def test_inv_i04a_itl_id_khong_bao_gio_doi(conn):
    iid = _chen_mot_dong(conn, raw_frozen=False)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("UPDATE fls_itl SET itl_id=%s WHERE itl_id=%s", (iid + 9999, iid))


def test_itl_id_tang_don_khong_trung(conn):
    a = _chen_mot_dong(conn, raw_frozen=False)
    b = _chen_mot_dong(conn, raw_frozen=False)
    assert b > a, "SEQUENCE phai tang don — day la cho fps_id_counter tung sinh id trung"


def test_content_key_trung_thi_bi_chan(conn):
    """Khoa phai SINH MOI moi lan chay.

    Ban trong plan ghim cung content_key='trung' => chay lan 2 tren cung DB thi
    cau INSERT DAU TIEN no, test do vi ly do sai. Test phai chay lai duoc.
    """
    khoa = f"trung-{os.urandom(4).hex()}"
    with conn.cursor() as cur:
        _dam_bao_cha(cur)
        sql = """INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                     run_id, contract_version, canon_version, mapping_version, canon)
                 VALUES (%s,'P100','Bank',1,'r1','v1.0','v1.0','v1.0','[]'::jsonb)"""
        cur.execute(sql, (khoa,))
        with pytest.raises(psycopg.errors.UniqueViolation):
            cur.execute(sql, (khoa,))


def test_gap_erd_p0_01_run_id_la_bo_khong_ton_tai_thi_bi_chan(conn):
    """Owner chot 26/08: go sai run_id phai BI CHAN ngay tang DB.

    Truoc khi co FK, dong nay chen duoc va lineage bien mat trong IM LANG —
    dung cai INV-I05 khong cho phep.
    """
    with conn.cursor() as cur:
        _dam_bao_cha(cur)
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            cur.execute("""
                INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                                     run_id, contract_version, canon_version, mapping_version,
                                     canon)
                VALUES (%s,'P100','Bank',1,'RUN-GO-SAI','v1.0','v1.0','v1.0','[]'::jsonb)
                """, (f"fk-{os.urandom(4).hex()}",))
