"""Cong ANH CHUP dong lenh chi (`fls_pm_line`) — dong `GAP-API-04` duong (a).

⛔⛔ Vi sao bang nay ton tai: bo nap doc dong lenh tu Google Sheets **luc chay roi
khong luu lai gi**. Sau khi nap, kho biet *"dong so nay noi voi dong lenh
`PM00030-2`"* nhung ⛔ khong biet **dong lenh do la gi** — nen thao tac GHEP TAY o
man `F01` (`QĐ-ITL-48`) ⛔ khong the co danh sach ung vien.

★ Bai chinh chay tren **HIEN VAT DA DO** (`pm_join.json`, checksum ghim), ⛔ khong
tren dau vao tu bia — cong chung #8.

★★ Va bai quan trong nhat o day ⛔ khong phai "chen duoc" ma la **anh chup MOI
KHONG DE LEN anh CU**: neu nap lai de len, ta vua bien mot anh chup thanh mot
"danh muc lenh chi" — tuc ban su that thu hai, dung cai benh khuon `fls/db/` chua.
"""
from __future__ import annotations

import json
import uuid
from decimal import Decimal as D
from pathlib import Path

import psycopg
import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm

pytestmark = pytest.mark.pg

HIEN_VAT = Path(__file__).resolve().parents[1] / "fixture" / "pm_join.json"
DSN = dsn_test()


@pytest.fixture(scope="module")
def pm_that() -> list[DongPM]:
    """3.703 dong lenh THAT — giu ca ma THO lan ma da chuan hoa."""
    d = json.loads(HIEN_VAT.read_text(encoding="utf-8"))
    return [DongPM(x["dong"], x["slip"], x["line"],
                   D(x["tien"]) if x["tien"] else None, x["cur"], x["status"],
                   canon_ref(x["ref_tho"]), x["hd"] or None, x["cdt1"] or None,
                   ref_tho=x["ref_tho"] or None)
            for x in d["pm"]]


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    """Mot lan nap co HINH DANG THAT nhung nam **nam 2000**.

    ⚠ Hinh dang phai that (`NAP-yyyy-mm-dd-NGUON`) vi cua doc loc pham vi bang
    HINH DANG `run_id`. Nam **2000** la thu duy nhat con phan biet duoc dau test
    voi dong that, nen cong `kiem_kho` ⛔ khong bi mu — xem `fls/repo/kho_sach.py`.
    """
    r = "NAP-2000-01-01-T" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _nc(run: str) -> NgucCanh:
    return NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "Transaction Mapping L1")


# ------------------------------------------------------- chen ca lat that
def test_chup_duoc_CA_3703_dong_lenh_that(conn, pm_that):
    """★ Ca lat that vao kho, ⛔ khong mat dong nao."""
    run = _run(conn)
    n = chen_dong_pm(conn, _nc(run), pm_that)
    assert n == 3703, f"phai chup 3.703 dong, duoc {n}"
    r = conn.execute(
        "select count(*), count(distinct pm_slip_id), count(ref_canon),"
        " count(*) filter (where status='Approve'),"
        " count(*) filter (where status is null)"
        " from fls_pm_line where run_id=%s", (run,)).fetchone()
    # Cac con so nay DA DO tren hien vat, ⛔ khong phai mong doi tu suy:
    #   3.703 dong · 1.468 phieu · 530 dong khong co ma
    #   status: Approve 3.347 · RONG 251 · Reject 105
    assert r[0] == 3703
    assert r[1] == 1468, f"phai 1.468 phieu, do duoc {r[1]}"
    assert r[2] == 3703 - 530, f"ma chuan hoa phai 3.173, do duoc {r[2]}"
    assert r[3] == 3347
    assert r[4] == 251, "status RONG phai la NULL — ⛔ khong bien thanh chuoi rong"


def test_giu_CA_HAI_dang_ma__tho_va_da_chuan_hoa(conn, pm_that):
    """⛔ Chi giu ban da chuan hoa thi be `canon_ref` di ma cong van XANH.

    Day la cai bay da mac mot lan voi hien vat `Classifying`. Nen bai nay doi
    phai co **it nhat mot dong** ma hai ban KHAC nhau — neu khong thi cot
    `ref_tho` chi la ban sao, va cong nay khong chung minh gi.
    """
    run = _run(conn)
    chen_dong_pm(conn, _nc(run), pm_that)
    khac = conn.execute(
        "select count(*) from fls_pm_line where run_id=%s"
        " and ref_tho is not null and ref_canon is not null"
        " and ref_tho <> ref_canon", (run,)).fetchone()[0]
    assert khac > 0, ("⛔ khong dong nao co ma THO khac ma CHUAN HOA ⇒ cot "
                      "`ref_tho` khong chung minh duoc gi")


# ------------------------------------------------- anh chup KHONG de len nhau
def test_ANH_CHUP_MOI_khong_de_len_anh_CU(conn, pm_that):
    """★★ Bai quan trong nhat cua bang nay.

    Nap lai nguon la mot `run_id` KHAC ⇒ hai anh chup nam **canh nhau**. Neu de
    len nhau thi bang nay thanh "danh muc lenh chi" — mot ban su that thu hai,
    va ⛔ khong ai truy lai duoc *"luc ghep, dong lenh do dang la gi"*.
    """
    lat = pm_that[:50]
    r1, r2 = _run(conn), _run(conn)
    chen_dong_pm(conn, _nc(r1), lat)
    # anh chup thu hai: CUNG dong lenh nhung tien DOI (nguon da doi that)
    doi = [DongPM(x.dong_sheet, x.slip, x.line,
                  (x.tien or D(0)) + D("1.00"), x.cur, x.status, x.ref,
                  x.hd, x.cdt1, ref_tho=x.ref_tho) for x in lat]
    chen_dong_pm(conn, _nc(r2), doi)

    hai = conn.execute(
        "select run_id, count(*), sum(amount) from fls_pm_line"
        " where run_id in (%s,%s) group by run_id order by run_id", (r1, r2)
    ).fetchall()
    assert len(hai) == 2, "hai lan nap phai cho HAI anh chup"
    assert hai[0][1] == hai[1][1] == 50
    assert hai[0][2] != hai[1][2], "hai anh chup phai giu HAI so tien khac nhau"


def test_chup_lai_CUNG_mot_lan_nap_KHONG_nhan_doi(conn, pm_that):
    """Chay lai cung `run_id` (nap lai giua duong) thi bo qua, ⛔ khong nhan ban."""
    run = _run(conn)
    lat = pm_that[:30]
    assert chen_dong_pm(conn, _nc(run), lat) == 30
    assert chen_dong_pm(conn, _nc(run), lat) == 30, "chay lai ⛔ khong duoc nhan doi"


def test_chup_lai_KHONG_de_len_gia_tri_cu_cua_CUNG_lan_nap(conn, pm_that):
    """⛔ `DO NOTHING`, ⛔ KHONG `DO UPDATE` — cung tinh than `INV-I08`."""
    run = _run(conn)
    x = pm_that[0]
    chen_dong_pm(conn, _nc(run), [x])
    chen_dong_pm(conn, _nc(run), [DongPM(
        x.dong_sheet, x.slip, x.line, D("999999.99"), x.cur, x.status, x.ref,
        "HD-BIA", "CDT-BIA", ref_tho=x.ref_tho)])
    r = conn.execute("select amount, hd from fls_pm_line where run_id=%s",
                     (run,)).fetchone()
    assert r[0] == x.tien, "gia tri cu bi ghi de — anh chup ⛔ khong duoc sua tai cho"
    assert r[1] != "HD-BIA"


# ------------------------------------------------------------ dong thieu ma
def test_dong_KHONG_co_ID_PMLine_bi_BO_va_KHONG_im_lang(conn, capsys):
    """⛔ Bo thi phai NOI RA bao nhieu dong bi bo (`INV-I16`).

    Mot dong lenh khong co ma dong thi ⛔ khong ghep vao dau duoc — nhung *"co
    bao nhieu dong nhu the"* la con so nguoi doc can biet.
    """
    run = _run(conn)
    n = chen_dong_pm(conn, _nc(run), [
        DongPM(3, "PM1", "PM1-1", D("10"), "VND", "Approve", "R1"),
        DongPM(4, "PM1", "", D("20"), "VND", "Approve", "R2"),
        DongPM(5, "PM1", "   ", D("30"), "VND", "Approve", "R3"),
    ])
    assert n == 1, "hai dong khong co ma dong phai bi BO"
    assert "BO 2 dong khong co `ID PMLine`" in capsys.readouterr().out


def test_khong_co_dong_lenh_nao_thi_khong_chen_gi(conn):
    assert chen_dong_pm(conn, _nc(_run(conn)), []) == 0
