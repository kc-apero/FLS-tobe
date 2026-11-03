"""`INV-I03` phai chan CA `DELETE` LAN `TRUNCATE` — di tru `0015`.

⛔⛔ **Bai nay sinh ra tu mot lo THAT, do duoc truoc khi va (2026-09-07):**
      DELETE   -> BI CHAN  ✅
      TRUNCATE -> ⛔ KHONG bi chan, sau lenh con **0 dong**
    Tuc bat bien "so chi-THEM" — thu duoc trich dan khap bo tai lieu nhu
    **bang chung** rang so ⛔ khong the bi sua — cach su that MOT cau lenh.

★ PostgreSQL ⛔ khong ban trigger DELETE muc DONG khi chay TRUNCATE. Muon chan
  phai khai rieng `BEFORE TRUNCATE … FOR EACH STATEMENT`. Day ⛔ khong phai
  "quen mot dong SQL" — no la mot **lop** loi: mot trigger muc DONG ⛔ khong
  bao gio thay duoc mot lenh muc BANG.
"""
import uuid

import psycopg
import pytest

from fls.db.kho import dsn_test

pytestmark = pytest.mark.pg


def _noi():
    try:
        return psycopg.connect(dsn_test(), connect_timeout=10)
    except Exception as e:                      # noqa: BLE001
        pytest.skip(f"khong noi duoc kho test: {e}")


def test_DELETE_bi_chan():
    """Nhanh von da dung — giu lai de bai nay do CA HAI chieu."""
    with _noi() as c:
        c.autocommit = True
        run = "NAP-2000-01-01-TR" + uuid.uuid4().hex[:6].upper()
        c.execute("INSERT INTO fls_run (run_id, contract_version,"
                  " canon_version, mapping_version) VALUES (%s,'v1.0','v1.0',"
                  "'v1.0')", (run,))
        itl = c.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon)"
            " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',true,"
            "'{}'::jsonb) RETURNING itl_id",
            (uuid.uuid4().hex, uuid.uuid4().int % 100000, run)).fetchone()[0]
        with pytest.raises(psycopg.errors.RaiseException) as e:
            c.execute("delete from fls_itl where itl_id = %s", (itl,))
        assert "INV-I03" in str(e.value)


def test_TRUNCATE_bi_chan():
    """⛔ TRUOC di tru `0015` bai nay DO — da chung minh tren kho that."""
    with _noi() as c:
        with pytest.raises(psycopg.errors.RaiseException) as e:
            c.execute("truncate fls_itl cascade")
        c.rollback()
        loi = str(e.value)
        assert "INV-I03" in loi, loi
        # ⛔ Loi phai chi ra DUONG HOP LE, ⛔ khong chi noi "cam".
        # Mot phep chan ⛔ khong noi duoc buoc tiep theo la mot phep chan
        # se bi ai do di vong qua.
        assert "dung_lai_kho_test" in loi, loi


def test_chan_van_con_sau_khi_ap_lai_di_tru():
    """Di tru chay lai ⛔ khong duoc lam mat phep chan (idempotent)."""
    from fls.db import pg_migrate
    with _noi() as c:
        c.autocommit = True
        pg_migrate.ap(c)
        n = c.execute(
            "select count(*) from pg_trigger "
            "where tgname = 'trg_fls_itl_chan_truncate'").fetchone()[0]
        assert n == 1, f"trigger chan TRUNCATE bien mat sau khi ap lai: {n}"
