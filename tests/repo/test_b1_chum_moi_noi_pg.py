# -*- coding: utf-8 -*-
"""`B1` — CHUM moi noi: nut `Bo gan` ⛔ KHONG duoc go trong im lang.

⭐⭐⭐ `QĐ-ITL-148 ③` · `2026-09-21`. Owner chot: **giu cua, MAN noi ra thiet hai**.

── Vi sao co bai nay ────────────────────────────────────────────────────

Cua `POST /queue/{itl_id}/unmatch` *(`QĐ-ITL-69`)* bo **TOAN BO** moi noi cua
mot dong tien va **⛔ khong nhan `pm_line_ids`** — bo le mot cap lam
`Σ moi noi ≠ tien bank`, dung trang thai cong `SIGMA_MOI_NOI` dung ra de bat.

⛔ Nhung thiet ke `21/09` ve nut `Bo gan` tren **the lenh chi**, tuc bo **MOT
  cap**. Va `C8` *«Doi sang giao dich da chon»* cung la bo mot cap roi noi lai.

── ⭐ Phep do THU NHO van de rat nhieu ─────────────────────────────────

    dong tien da co moi noi        2.222
    ⭐ mang CHUM (>1 moi noi)          25  = **1,1%**
    chum lon nhat                      10  dong lenh tren mot dong tien
    moi noi nam trong mot chum         65 / 2.262 = 2,9%

⇒ **Cua dung nguyen. MAN phai noi ra thiet hai** — va chi o `1,1%` ca ay.

⛔⛔ **⛔ KHONG hoi o ca hai ca *"cho chac"*:** mot hop thoai bat **2.222** lan
   de dung **25** lan la cach nhanh nhat **day nguoi ta bam `OK` ⛔ khong doc**
   — va khi ay no ⛔ khong con can duoc gi o dung `25` lan can can.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo import man_ghep
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "b1-chum@fls"
LY_DO = "bai thu B1 — chum moi noi"


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    r = "NAP-2000-01-01-C" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-C',%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, curr,
         D(tien))).fetchone()[0]


def _lenh(conn, run: str, *ds: tuple) -> None:
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, x[0].split("-")[0], x[0], D(x[1]), x[2], x[3], None,
               x[4], x[5], ref_tho=None) for i, x in enumerate(ds)])


def _ca_MOT_cap(conn) -> tuple[int, str]:
    run = _run(conn)
    i = _dong_bank(conn, run, "1000000.00")
    _lenh(conn, run, ("PM90-1", "1000000.00", "VND", "Approve",
                      "FNS | Facilities", "SHQ2 | HQ2"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM90-1"], actor=ACTOR, reason=LY_DO)
    return i, "PM90-1"


def _ca_CHUM_ba_cap(conn) -> tuple[int, list[str]]:
    """Mot dong tien om BA dong lenh — hinh dang cua `25` dong that."""
    run = _run(conn)
    i = _dong_bank(conn, run, "3000000.00")
    ma = ["PM91-1", "PM91-2", "PM91-3"]
    _lenh(conn, run, *[(m, "1000000.00", "VND", "Approve",
                        "FNS | Facilities", "SHQ2 | HQ2") for m in ma])
    gt.ghep_lenh(conn, chi_nap_that(), i, ma, actor=ACTOR, reason=LY_DO)
    return i, ma


# ── ⓐ cua tra ve DANH SACH, ⛔ khong mot con so ─────────────────────────

def test_chum_cua_MOT_cap_tra_ve_DUNG_MOT_dong_lenh(conn):
    i, ma = _ca_MOT_cap(conn)
    r = man_ghep.chum_cua_dong_tien(conn, chi_nap_that(), i)
    assert [x["pm_line_id"] for x in r] == [ma]


def test_chum_BA_cap_tra_ve_DU_BA__va_KEM_TEN(conn):
    """⭐⭐ Man phai liet ke **TEN tung dong lenh** sap bi go.

    ⛔ Mot con so *"se go 3 moi noi"* ⛔ khong du: nguoi dung can biet **dong
       nao**, vi ho chi dinh dong toi **mot** trong so do.
    """
    i, ma = _ca_CHUM_ba_cap(conn)
    r = man_ghep.chum_cua_dong_tien(conn, chi_nap_that(), i)
    assert sorted(x["pm_line_id"] for x in r) == sorted(ma)
    for x in r:
        assert x.get("amount") is not None, "⛔ thieu so tien ⇒ nguoi doc ⛔ khong nhan ra dong"
        assert x.get("curr"), "⛔ thieu don vi tien"


# ── ⓑ ⭐ khi nao MAN phai hoi ───────────────────────────────────────────

def test_MOT_cap_thi_KHONG_phai_hoi(conn):
    """⛔⛔ `2.197/2.222` ca. Hoi o day la hoi thua **2.197** lan."""
    i, _ = _ca_MOT_cap(conn)
    assert man_ghep.can_hoi_truoc_khi_bo_gan(conn, chi_nap_that(), i) is False


def test_CHUM_thi_PHAI_hoi(conn):
    """⭐ `25/2.222` = 1,1% ca — va o day mot nut im lang go tuot ca chum."""
    i, _ = _ca_CHUM_ba_cap(conn)
    assert man_ghep.can_hoi_truoc_khi_bo_gan(conn, chi_nap_that(), i) is True


def test_dong_tien_CHUA_NOI_thi_KHONG_co_chum(conn):
    run = _run(conn)
    i = _dong_bank(conn, run, "500000.00")
    assert man_ghep.chum_cua_dong_tien(conn, chi_nap_that(), i) == []
    assert man_ghep.can_hoi_truoc_khi_bo_gan(conn, chi_nap_that(), i) is False
