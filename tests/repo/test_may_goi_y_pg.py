# -*- coding: utf-8 -*-
"""MAY GOI Y `hd`/`cdt1` luc TU GHEP — va no ⛔ KHONG duoc lan sang cho NGUOI.

⛔⛔⛔ **Vi sao bo bai nay ton tai — lo that, do duoc, `2026-09-18`.**

Duong ghep **TAY** (`ghi_tay.ghep_lenh`) da suy `hd`/`cdt1` tu dong lenh tu
`28/08`. Duong ghep **TU DONG** (`chay_nap.chen_moi_noi`) thi ⛔ **khong** —
no chen moi noi roi thoi. Do tren kho that `18/09`:

    `fls_itl`  8.387 dong  ·  `hd` **0**  ·  `cdt1` **0**  ·  ca hai `*_thyt` **0**
    dong lenh  3.772       ·  co `hd` **3.767** (99,9%)  ·  co `cdt1` **3.763**
    dong so DA ghep 2.222  ⇒ suy duoc `hd` **2.219** · `cdt1` **2.217**
    ⚠ va **10** dong so co N dong lenh noi HAI `hd` KHAC NHAU

⇒ Cau tra loi **da nam san trong kho**, chi la ⛔ khong ai bac cau.

⛔⛔ **Nhung bac cau THANG thi pham `INV-I16`, va day la cho de truot nhat.**
`fls_adjustment` *(bang GIA TRI)* ⛔ **khong co** cot nguon; `value_source` chi
song o `fls_journal` *(so NHAT KY)*. Ma khung xem tra loi cau *"o nay dang la
gi"* — `fls_sua_tay` — doc **bang gia tri**.

    ⇒ Mot goi y cua MAY ghi thang vao do se hien ra **y het** mot con so
      NGUOI da chot, va ⛔ khong cho nao phan biet duoc.

⭐ Owner chot **phuong an B** *(18/09)* ⇒ **`INV-I21`** *(`BA-11` v0.13)*:
  *"gia tri phai tu noi duoc **ai** noi no, va lan MAY ⛔ khong duoc chay vao
  lan NGUOI"* — `INV-I16` ha xuong tang KHO. Cu the: them cot **`nguon`**
  vao bang gia tri,
  `fls_sua_tay` **giu nguyen nghia cu** *(chi gia tri NGUOI chot)*, va goi y
  cua may di loi rieng — `fls_may_goi_y`.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.db.kho import dsn_test
from fls.db.schema import TABLES
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "ke-toan@apero.vn"
LY_DO = "ghep tay tu man F01"


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    r = "NAP-2000-01-01-G" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-X',%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, curr,
         D(tien))).fetchone()[0]


def _lenh(conn, run: str, *ds: tuple) -> None:
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, x[0].split("-")[0], x[0], D(x[1]), x[2], x[3], None,
               x[4], x[5], ref_tho=None) for i, x in enumerate(ds)])


# ───────────────────────────────── ⓐ ban khai + kho
def test_ban_khai_fls_adjustment_CO_cot_nguon():
    """⛔ Bang GIA TRI phai tu noi duoc *"ai noi con so nay"*.

    ⛔⛔ Khong co cot nay thi cau tra loi chi nam o `fls_journal`, va moi cho
       doc gia tri *(`fls_sua_tay`, `_hieu_luc`, man hinh)* deu **⛔ khong biet**
       minh dang cam goi y cua may hay quyet dinh cua nguoi.
    """
    ten = {c.name for c in TABLES["fls_adjustment"].columns}
    assert "nguon" in ten, (
        "⛔ `fls_adjustment` thieu cot `nguon`. Do `18/09`: `value_source` chi "
        "co o `fls_journal`, ma `fls_sua_tay` doc `fls_adjustment` ⇒ goi y cua "
        "MAY se hien y het quyet dinh cua NGUOI (`INV-I16`).")


def test_kho_THAT_co_cot_nguon_va_NOT_NULL(conn):
    r = conn.execute(
        "select data_type, is_nullable from information_schema.columns"
        " where table_name='fls_adjustment' and column_name='nguon'").fetchone()
    assert r is not None, "⛔ kho thieu cot `fls_adjustment.nguon`"
    assert r[0] == "text"
    assert r[1] == "NO", (
        "⛔ `nguon` phai `NOT NULL`: mot but toan ⛔ khong biet ai noi la dung "
        "cai trang thai cot nay sinh ra de xoa.")


def test_kho_THAT_co_khung_xem_may_goi_y(conn):
    r = conn.execute("select table_name from information_schema.views"
                     " where table_name='fls_may_goi_y'").fetchone()
    assert r is not None, (
        "⛔ thieu khung xem `fls_may_goi_y`. Goi y cua may phai co **loi rieng**: "
        "nhet chung vao `fls_sua_tay` la doi nghia cua mot khung xem ma "
        "**8 cho trong `bang_tuyen.py` dang doc**.")


# ───────────────────────────────── ⓑ ranh gioi MAY ↔ NGUOI
def test_goi_y_cua_MAY_khong_lot_vao_fls_sua_tay(conn):
    """⭐⭐⭐ Bai QUAN TRONG NHAT cua tep nay.

    `fls_sua_tay` tra loi cau *"NGUOI da chot gi"*. Mot goi y cua may lot vao
    day la may **tra loi thay nguoi** — dung thu `INV-I16` cam, va la ve THU
    NHAT cua `INV-I21`.
    """
    from fls.repo.may_ghep import ghi_goi_y_may

    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run, ("PM90-1", "100.00", "VND", "Approve", "HD-M", "CDT-M"))
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,'PM90-1',%s,'A',%s)",
                 (i, D("100.00"), run))

    ra = ghi_goi_y_may(conn, itl_id=i,
                       lenh=[{"pm_line_id": "PM90-1", "hd": "HD-M",
                              "cdt1": "CDT-M"}], run_pm=run)
    assert {x["field"] for x in ra["but_toan"]} == {"hd", "cdt1"}

    tay = conn.execute("select count(*) from fls_sua_tay where itl_id=%s",
                       (i,)).fetchone()[0]
    assert tay == 0, (
        f"⛔⛔ {tay} goi y cua MAY da lot vao `fls_sua_tay` — khung xem ay "
        f"⛔ CHI duoc chua gia tri NGUOI chot (`INV-I16`).")

    may = conn.execute("select field, value_after from fls_may_goi_y"
                       " where itl_id=%s order by field", (i,)).fetchall()
    assert may == [("cdt1", "CDT-M"), ("hd", "HD-M")]


def test_NGUOI_go_van_vao_fls_sua_tay__khong_bi_loc_nham(conn):
    """⛔ Phep loc moi ⛔ KHONG duoc cat nham duong cu.

    ⛔⛔ **Viet lai 01/10 (`WO-003`, `QĐ-ITL-149`).** Ten cu
    `test_ghep_TAY_van_vao_fls_sua_tay__khong_bi_loc_nham` lay **cu ghep tay**
    lam *"duong nguoi"*: *"ghep TAY phai van hien o `fls_sua_tay` — nguoi da
    chot that"*. Owner lat dung tien de ay: *"Máy gợi ý"* — nguoi bam `Gan`
    chon DONG LENH, ⛔ go `hd`/`cdt1` (`INV-I21` v0.14).
    ⭐ Lo goc giu: phep loc `nguon` ⛔ duoc cat nham **duong NGUOI GO** — nay
      duong ay la `ghi_but_toan` (`/adjust`). Va cu ghep tay di dung lan MAY.
    """
    run = _run(conn)
    i = _dong_bank(conn, run, "50.00")
    _lenh(conn, run, ("PM91-1", "50.00", "VND", "Approve", "HD-T", "CDT-T"))
    gt.ghep_lenh(conn, chi_nap_that(), i, ["PM91-1"], actor=ACTOR, reason=LY_DO)
    assert conn.execute("select count(*) from fls_sua_tay where itl_id=%s",
                        (i,)).fetchone()[0] == 0,         "⛔ cu ghep TAY lot vao lan NGUOI (`QĐ-ITL-149`)"
    gt.ghi_but_toan(conn, chi_nap_that(), i, "hd", "HD-NGUOI", actor=ACTOR,
                    reason="nguoi chot")
    r = conn.execute("select field, value_after from fls_sua_tay"
                     " where itl_id=%s order by field", (i,)).fetchall()
    assert r == [("hd", "HD-NGUOI")], (
        "⛔ gia tri NGUOI go phai van hien o `fls_sua_tay` — nguoi da chot that.")


def test_moi_but_toan_NGUOI_GO_mang_sua_tay__but_toan_GHEP_mang_may_goi_y(conn):
    """⛔⛔ **Viet lai 01/10** — ten cu `test_moi_but_toan_TAY_deu_mang_nguon_
    sua_tay` coi but toan cua cu GHEP tay la *"tay"*. `QĐ-ITL-149` lat tien
    de ay. Lo goc giu: **moi but toan tu noi dung AI noi no** — nguoi go ⇒
    `sua_tay`, may suy (ke ca trong cu ghep nguoi bam) ⇒ `may_goi_y`."""
    run = _run(conn)
    i = _dong_bank(conn, run, "50.00")
    _lenh(conn, run, ("PM92-1", "50.00", "VND", "Approve", "HD-T", "CDT-T"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PM92-1"], actor=ACTOR,
                      reason=LY_DO)
    gt.ghi_but_toan(conn, chi_nap_that(), i, "invoice", "HD-001", actor=ACTOR,
                    reason="nguoi go")
    r = dict(conn.execute("select evt_id is not null, array_agg(distinct nguon)"
                          " from fls_adjustment where itl_id=%s"
                          " group by 1", (i,)).fetchall())
    assert ra["evt_id"] and r == {True: ["may_goi_y"], False: ["sua_tay"]}, r


# ───────────────────────────────── ⓒ `INV-I16` — may phai DUNG
def test_N_dong_lenh_noi_N_thu__MAY_khong_chon_va_khai_ra(conn):
    """⭐⭐ Do that: **10** dong so co hai `hd` khac nhau. May ⛔ khong duoc chon.

    ⛔ Lay dong dau tien la mot dap an **trong hop ly** — va do la cai nguy
      hiem cua no: ⛔ khong ai nghi ngo mot con so co ve dung.
    """
    from fls.repo.may_ghep import ghi_goi_y_may

    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    _lenh(conn, run,
          ("PM93-1", "60.00", "VND", "Approve", "HD-A", "CDT-X"),
          ("PM93-2", "40.00", "VND", "Approve", "HD-B", "CDT-X"))
    for ln, t in (("PM93-1", "60.00"), ("PM93-2", "40.00")):
        conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount,"
                     " hinh, run_id) VALUES (%s,%s,%s,'B',%s)", (i, ln, D(t), run))

    ra = ghi_goi_y_may(conn, itl_id=i, lenh=[
        {"pm_line_id": "PM93-1", "hd": "HD-A", "cdt1": "CDT-X"},
        {"pm_line_id": "PM93-2", "hd": "HD-B", "cdt1": "CDT-X"}], run_pm=run)
    assert ra["khong_suy_duoc"] == ["hd"]
    assert [x["field"] for x in ra["but_toan"]] == ["cdt1"], \
        "cdt1 hai dong dong y nen VAN duoc goi y"
    con = conn.execute("select count(*) from fls_may_goi_y where itl_id=%s"
                       " and field='hd'", (i,)).fetchone()[0]
    assert con == 0, "⛔ `hd` lech nhau ma may van ghi mot gia tri"


def test_may_KHONG_de_len_gia_tri_NGUOI_da_chot(conn):
    """⭐⭐⭐ Nguoi chot roi thi may ⛔ KHONG duoc goi y de len nua.

    ⛔ Neu khong, mot lan nap lai se **lat ket luan cua nguoi** trong im lang —
      va lan nap chay theo nhip gio (`8h–19h`, toi 12 lan/ngay), ⛔ khong ai
      ngoi xem. Ve THU HAI cua `INV-I21`.
    """
    from fls.repo.may_ghep import ghi_goi_y_may

    run = _run(conn)
    i = _dong_bank(conn, run, "50.00")
    _lenh(conn, run, ("PM94-1", "50.00", "VND", "Approve", "HD-T", "CDT-T"))
    # ⚠ Viet lai 01/10 (`WO-003`): ban cu dung `ghep_lenh` de dat *"NGUOI da
    #   chot"* — tu `QĐ-ITL-149` cu ghep chi de lai GOI Y. Nguoi chot = go qua
    #   `ghi_but_toan`. Lo goc cua bai giu nguyen.
    for f, v in (("hd", "HD-T"), ("cdt1", "CDT-T")):
        gt.ghi_but_toan(conn, chi_nap_that(), i, f, v, actor=ACTOR,
                        reason="nguoi chot")

    ra = ghi_goi_y_may(conn, itl_id=i, lenh=[
        {"pm_line_id": "PM94-1", "hd": "HD-KHAC", "cdt1": "CDT-KHAC"}],
        run_pm=run)
    assert ra["but_toan"] == [], "⛔ may goi y de len o NGUOI da chot"
    assert ra["nguoi_da_chot"] == ["cdt1", "hd"]
    r = conn.execute("select value_after from fls_sua_tay where itl_id=%s"
                     " and field='hd'", (i,)).fetchone()
    assert r == ("HD-T",), "⛔ gia tri nguoi chot BI DOI"


def test_so_KHONG_doi_mot_o_sau_khi_may_goi_y(conn):
    """`INV-I08` + `QĐ-ITL-35`: goi y la **them dong**, ⛔ khong sua so."""
    from fls.repo.may_ghep import ghi_goi_y_may

    cot = ("hd", "hd_thyt", "cdt1", "cdt1_thyt", "work_status", "pm_hinh")
    run = _run(conn)
    i = _dong_bank(conn, run, "50.00")
    _lenh(conn, run, ("PM95-1", "50.00", "VND", "Approve", "HD-M", "CDT-M"))
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,'PM95-1',%s,'A',%s)", (i, D("50.00"), run))
    truoc = conn.execute(
        f"select {', '.join(cot)} from fls_itl where itl_id=%s", (i,)).fetchone()

    ghi_goi_y_may(conn, itl_id=i, lenh=[
        {"pm_line_id": "PM95-1", "hd": "HD-M", "cdt1": "CDT-M"}], run_pm=run)

    sau = conn.execute(
        f"select {', '.join(cot)} from fls_itl where itl_id=%s", (i,)).fetchone()
    assert sau == truoc, "⛔⛔ `fls_itl` BI DOI — goi y phai la THEM DONG"
