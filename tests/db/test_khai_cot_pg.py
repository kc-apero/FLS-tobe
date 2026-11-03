# -*- coding: utf-8 -*-
"""`fls_khai_cot` tren PG THAT — di tru `0016` co thuc su ap duoc ba luat khong.

⛔⛔ Bai o `test_schema_khai_cot.py` chi doc **BAN KHAI trong Python**. Mot khoa
   khai ma ⛔ khong ap xuong kho thi ban khai van xanh con kho van nhan hai dong
   trung — dung lo da sinh ra `pg_verify` (26/08: `CREATE TABLE IF NOT EXISTS`
   bo qua trong im lang). ⇒ Cac bai duoi day **cham kho that**.
"""
import os

import psycopg
import pytest

from fls.db.kho import dsn_test

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, ⛔ KHONG phai kho that.
DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _mot_nguon(cur) -> int:
    """Mot dong `fls_source` rieng cho moi bai — ⛔ khong dung chung."""
    khoa = "R | Thu" + os.urandom(4).hex()
    cur.execute("INSERT INTO fls_source (source_key, src_type) "
                "VALUES (%s, 'Bank') RETURNING source_id", (khoa,))
    return cur.fetchone()[0]


def _khai(cur, sid: int, ver: int, truong: str, cot: int) -> int:
    cur.execute("INSERT INTO fls_khai_cot (source_id, version, truong, cot, actor) "
                "VALUES (%s,%s,%s,%s,'thu') RETURNING khai_id",
                (sid, ver, truong, cot))
    return cur.fetchone()[0]


def test_ghi_va_doc_lai_duoc_mot_ban_khai_du_sau_truong(conn):
    from fls.adapters.sao_ke import SAU_TRUONG
    with conn.cursor() as cur:
        sid = _mot_nguon(cur)
        for i, t in enumerate(SAU_TRUONG):
            _khai(cur, sid, 1, t, i)
        cur.execute("SELECT truong, cot FROM fls_khai_cot "
                    "WHERE source_id = %s AND version = 1 ORDER BY cot", (sid,))
        assert cur.fetchall() == [(t, i) for i, t in enumerate(SAU_TRUONG)]


def test_luat_a_CHI_THEM_hai_version_cung_ton_tai(conn):
    """Ngan hang doi mau sao ke ⇒ khai MOI. Khai CU phai con nguyen.

    ⭐ Day la luat lam cho cau *"dong nap thang truoc doc bang khai nao"* con
      tra loi duoc. Neu khai cu bi de len thi cau ay mat cau tra loi.
    """
    with conn.cursor() as cur:
        sid = _mot_nguon(cur)
        _khai(cur, sid, 1, "Debit", 3)
        _khai(cur, sid, 2, "Debit", 7)      # ngan hang chen them mot cot
        cur.execute("SELECT version, cot FROM fls_khai_cot "
                    "WHERE source_id = %s AND truong = 'Debit' ORDER BY version",
                    (sid,))
        assert cur.fetchall() == [(1, 3), (2, 7)], (
            "⛔ khai v1 phai con NGUYEN sau khi co v2 — sua de la viet lai lich su")


def test_KHOA_chan_hai_ban_khai_cho_cung_mot_truong_trong_cung_version(conn):
    """⛔ Hai dong `(nguon, version, 'Debit')` la **hai cau tra loi** cho cung
    mot cau hoi ⇒ tang doc phai CHON, va chon la doan."""
    with conn.cursor() as cur:
        sid = _mot_nguon(cur)
        _khai(cur, sid, 1, "Debit", 3)
        with pytest.raises(psycopg.errors.UniqueViolation):
            _khai(cur, sid, 1, "Debit", 4)


def test_khoa_KHONG_chan_cung_truong_o_nguon_KHAC(conn):
    """⛔ Khoa phai la (nguon, version, truong) — ⛔ khong phai (version, truong).

    60 sao ke deu co truong `Debit`; mot khoa quen `source_id` se **chan sheet
    thu hai** va bo test van xanh neu chi bao gio thu MOT nguon.
    """
    with conn.cursor() as cur:
        a, b = _mot_nguon(cur), _mot_nguon(cur)
        _khai(cur, a, 1, "Debit", 3)
        _khai(cur, b, 1, "Debit", 3)        # ⛔ phai di qua duoc


def test_source_id_khong_co_that_thi_BI_CHAN(conn):
    """Ban khai cua mot nguon ⛔ khong ton tai la mot ban khai **mo coi**."""
    with conn.cursor() as cur:
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            _khai(cur, 10**15, 1, "Debit", 3)


def test_fls_run_khai_id_nhan_NULL(conn):
    """⭐ `R-A1`: lo co TRUOC bang khai thi `khai_id` la NULL — ⛔ khong bia."""
    rid = "r-null-" + os.urandom(4).hex()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version, "
                    "mapping_version) VALUES (%s,'v1.1','v1.0','v1.0')", (rid,))
        cur.execute("SELECT khai_id FROM fls_run WHERE run_id = %s", (rid,))
        assert cur.fetchone() == (None,)


def test_fls_run_khai_id_bia_ra_thi_BI_CHAN(conn):
    """⛔ Nullable ⛔ KHONG co nghia la muon ghi gi cung duoc."""
    rid = "r-bia-" + os.urandom(4).hex()
    with conn.cursor() as cur:
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            cur.execute("INSERT INTO fls_run (run_id, contract_version, "
                        "canon_version, mapping_version, khai_id) "
                        "VALUES (%s,'v1.1','v1.0','v1.0',%s)", (rid, 10**15))


def test_di_bo_tu_DONG_SO_ve_toi_NGUON(conn):
    """⭐⭐ Day la thu ca migration `0016` sinh ra de co: mot duong lineage
    **di bo duoc** tu mot dong so ve toi sao ke goc va cach doc no.

        fls_itl.run_id → fls_run.khai_id → fls_khai_cot.source_id → fls_source

    ⛔ Truoc `0016`, `fls_source` la mot DAO: mot manifest ma ⛔ khong dong so
       nao tro toi duoc. Bai nay la **bang chung dao do da noi lien**.
    """
    tag = os.urandom(4).hex()
    with conn.cursor() as cur:
        sid = _mot_nguon(cur)
        kid = _khai(cur, sid, 1, "Debit", 3)
        cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version, "
                    "mapping_version, khai_id) VALUES (%s,'v1.1','v1.0','v1.0',%s)",
                    (f"r-{tag}", kid))
        cur.execute("INSERT INTO fls_le (le_code, le_name) VALUES ('SGO1','SGO1') "
                    "ON CONFLICT DO NOTHING")
        cur.execute("""
            INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                                 run_id, contract_version, canon_version,
                                 mapping_version, canon)
            VALUES (%s,'P100','R | Thu',1,%s,'v1.1','v1.0','v1.0','[]'::jsonb)
            RETURNING itl_id""", (f"ck-{tag}", f"r-{tag}"))
        iid = cur.fetchone()[0]

        cur.execute("""
            SELECT s.source_key, k.truong, k.cot
            FROM fls_itl i
            JOIN fls_run r      ON r.run_id    = i.run_id
            JOIN fls_khai_cot k ON k.khai_id   = r.khai_id
            JOIN fls_source s   ON s.source_id = k.source_id
            WHERE i.itl_id = %s""", (iid,))
        hang = cur.fetchall()
    assert hang and hang[0][1:] == ("Debit", 3), (
        "⛔ ⛔ khong di bo duoc tu dong so ve toi nguon — duong lineage dut")
