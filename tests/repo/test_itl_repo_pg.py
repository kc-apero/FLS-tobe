import os
import uuid
from datetime import date

import psycopg
import pytest

from fls.db.kho import dsn_test

from fls.canon.row import CanonRow
from fls.ledger.build import NgucCanh, dung_dong
from fls.repo.itl_repo import chen, chen_mot

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, KHONG phai kho that. `dsn_test()` NO neu no tro vao kho
# that — xem `fls/db/kho.py`: bo test tung ghi 1.204 dong vao `fls_itl`.
DSN = dsn_test()
NC = NgucCanh("r1", "v1.0", "v1.0", "v1.0", "P100", "Bank")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                        " mapping_version) VALUES ('r1','v1.0','v1.0','v1.0')"
                        " ON CONFLICT DO NOTHING")
        yield c


def _p(ngay: date, no: str, seq: int = 0):
    v = [None] * 38
    v[0], v[1], v[3], v[4], v[5], v[6] = ngay, no, "VND", 0, 1000, "1121"
    return dung_dong(CanonRow.from_list(v), seq + 1, NC, seq_trung=seq)


def test_CHEN_LUI_NGAY_KHONG_LAM_DOI_ID_CUA_DONG_NAO(conn):
    """★★ Cong quan trong nhat P1.

    AS-IS dung ="ITL#"&ROW() tren bang da SORT theo ngay => chen mot dong lui
    ngay danh so lai TOAN BO phia duoi. Do la goc cua 1.356 dong FALSE o vung
    AUDIT (DD-I05).
    """
    lo = uuid.uuid4().hex[:8]
    ids = chen(conn, [_p(date(2026, 3, 1), f"{lo}-a"),
                      _p(date(2026, 3, 2), f"{lo}-b"),
                      _p(date(2026, 3, 3), f"{lo}-c")])
    assert len(set(ids)) == 3

    lui = chen_mot(conn, _p(date(2026, 1, 1), f"{lo}-lui"))

    with conn.cursor() as cur:
        cur.execute("SELECT itl_id FROM fls_itl WHERE doc_no = ANY(%s) ORDER BY doc_no",
                    ([f"{lo}-a", f"{lo}-b", f"{lo}-c"],))
        sau = [r[0] for r in cur.fetchall()]
    assert sau == sorted(ids), "chen lui ngay DA LAM DOI id — dung loi AS-IS"
    assert lui > max(ids), "id cap theo thu tu VAO SO, khong theo ngay"


def test_id_khong_bam_thu_tu_ngay(conn):
    """Dong ngay som nhat co the co id LON nhat — day la dieu DUNG."""
    lo = uuid.uuid4().hex[:8]
    a = chen_mot(conn, _p(date(2026, 12, 31), f"{lo}-cuoi-nam"))
    b = chen_mot(conn, _p(date(2026, 1, 1), f"{lo}-dau-nam"))
    assert b > a


def test_content_key_trung_bi_chan_o_DB(conn):
    p = _p(date(2026, 2, 2), uuid.uuid4().hex[:8])
    chen_mot(conn, p)
    with pytest.raises(psycopg.errors.UniqueViolation):
        chen_mot(conn, dict(p))


def test_repo_khong_phat_UPDATE_hay_DELETE_len_fls_itl():
    """INV-I08: ghi la THEM. Quet ma nguon, khong doan."""
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[2] / "fls" / "repo" / "itl_repo.py"
    t = src.read_text(encoding="utf-8").upper()
    assert "UPDATE FLS_ITL" not in t
    assert "DELETE FROM FLS_ITL" not in t


def test_chen_lo_rong_khong_no_va_khong_ghi_gi(conn):
    assert chen(conn, []) == []


def test_ghi_du_38_o_canon_va_doc_lai_dung_vi_tri(conn):
    lo = uuid.uuid4().hex[:8]
    v = [None] * 38
    v[0], v[1], v[3], v[4], v[5], v[6] = date(2026, 5, 5), lo, "VND", 0, 500, "1121"
    v[33], v[34], v[35], v[36] = "ah", "ai", "aj", "ak"
    iid = chen_mot(conn, dung_dong(CanonRow.from_list(v), 1, NC))
    with conn.cursor() as cur:
        cur.execute("SELECT canon FROM fls_itl WHERE itl_id = %s", (iid,))
        canon = cur.fetchone()[0]
    assert len(canon) == 38
    assert canon[33:37] == ["ah", "ai", "aj", "ak"], "4 cot trung ten bi de len nhau"


def test_run_id_khong_ton_tai_thi_bi_chan(conn):
    """FK run_id (GAP-ERD-P0-01) — go sai run la chan ngay, khong mat lineage."""
    nc = NgucCanh("RUN-KHONG-CO", "v1.0", "v1.0", "v1.0", "P100", "Bank")
    v = [None] * 38
    v[0], v[1], v[3], v[4], v[5], v[6] = date(2026, 6, 6), uuid.uuid4().hex[:8], "VND", 0, 1, "1121"
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        chen_mot(conn, dung_dong(CanonRow.from_list(v), 1, nc))
