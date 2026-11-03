"""Khoa NHIEU COT trong khuon khai bao — dong `GAP-DB-P0-03`.

⛔⛔ Truoc 27/08 khuon `fls/db/model.py` chi khai duoc khoa MOT cot. Hai hau qua
that, khong phai gia dinh:

  ⓵ `fls_reject` khong co `UNIQUE(run_id, source_row)` o tang kho. Lop chan trung
    duy nhat la `WHERE NOT EXISTS` trong cau INSERT — va no DA hong: mot lan
    chay lai nhan ban thanh **76 dong cho 19 dong loai that**.
  ⓶ `fls_pm_link` (mot dong so -> N dong lenh) **khong the khai noi**, nen 27
    dong hinh `B` phai vao hang cho kem ly do co ten thay vi dau duoc.

★ Va cong `pg_verify` truoc day ⛔ KHONG so khoa chinh / UNIQUE, nen mot khoa
KHAI ma khong AP se di qua im lang — cung benh voi lo da sinh ra chinh cong do
(`CREATE TABLE IF NOT EXISTS` bo qua trong im lang), chi khac truc.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.db.model import Column as C
from fls.db.model import Table, kiem_khai_bao
from fls.db.pg_verify import so_sanh_voi_db
from fls.db.render import render_ddl
from fls.db.schema import TABLES


# ------------------------------------------------------------------ sinh DDL
def test_khoa_chinh_nhieu_cot_ra_rang_buoc_muc_bang():
    t = Table(name="thu", columns=(C("a", "text", null=False),
                                   C("b", "text", null=False)),
              pk_cols=("a", "b"))
    ddl = render_ddl(t)
    assert "CONSTRAINT thu_pk PRIMARY KEY (a, b)" in ddl
    # ⛔ khong duoc gan PRIMARY KEY vao tung cot
    assert "a text NOT NULL," in ddl and "a text NOT NULL PRIMARY KEY" not in ddl


def test_unique_nhieu_cot_ra_rang_buoc_muc_bang():
    t = Table(name="thu", columns=(C("a", "text"), C("b", "int")),
              unique_keys=(("a", "b"),))
    assert "CONSTRAINT thu_a_b_uq UNIQUE (a, b)" in render_ddl(t)


def test_THU_TU_cot_trong_khoa_duoc_giu():
    """`PK (a, b)` va `PK (b, a)` cho ra chi muc KHAC nhau — thu tu la mot phan
    cua bản khai, ⛔ khong duoc sap lai cho 'dep'."""
    t = Table(name="thu", columns=(C("a", "text", null=False),
                                   C("b", "text", null=False)),
              pk_cols=("b", "a"))
    assert "PRIMARY KEY (b, a)" in render_ddl(t)


def test_view_khai_khoa_la_LOI():
    t = Table(name="v_thu", kind="view", view_sql="SELECT 1",
              columns=(C("a", "text"),), pk_cols=("a",))
    assert any("là VIEW mà khai khoá" in m for m in kiem_khai_bao(t))


# ------------------------------------------------------------------ tu mau thuan
def test_khai_khoa_HAI_CHO_la_LOI():
    """⛔ Khai o ca cot lan bang la dung cai benh khuon nay chua: hai ban su that."""
    t = Table(name="thu", columns=(C("a", "text", null=False, pk=True),
                                   C("b", "text", null=False)),
              pk_cols=("a", "b"))
    loi = kiem_khai_bao(t)
    assert any("khoá chính khai HAI CHỖ" in m for m in loi), loi


def test_pk_cols_tro_toi_cot_KHONG_TON_TAI_la_LOI():
    t = Table(name="thu", columns=(C("a", "text"),), pk_cols=("a", "khong_co"))
    assert any("không có cột đó" in m for m in kiem_khai_bao(t))


def test_unique_keys_MOT_cot_la_LOI():
    """Mot cot thi khai `unique=True` ngay o cot — dung tao cho khai thu hai."""
    t = Table(name="thu", columns=(C("a", "text"),), unique_keys=(("a",),))
    assert any("chỉ MỘT cột" in m for m in kiem_khai_bao(t))


def test_MOI_bang_that_deu_khai_bao_SACH():
    """Cong: khong bang nao trong `schema.py` tu mau thuan."""
    loi = [m for t in TABLES.values() for m in kiem_khai_bao(t)]
    assert not loi, loi


# ------------------------------------------------------------------ hai bang that
def test_fls_pm_link_khoa_BA_cot_va_LY_DO_doi_khoa():
    """⛔⛔ Khoa DA DOI 2026-08-28 (`QĐ-ITL-69`, migration `0013`).

    ★ **Bai nay giu LY DO, ⛔ khong chi giu hinh dang khoa.** Khoa cu
    `(itl_id, pm_line_id)` doc ra la *"mot dong so noi voi mot dong lenh nhieu
    nhat MOT lan trong DOI"*. Nghe hop ly, va no da dung mot ngay — cho den khi
    mo duong **BO MOI NOI**: viec pho bien nhat sau khi bo la **ghep lai dung
    dong lenh ay** (bo vi chia tien sai, ⛔ khong phai vi chon sai dong), va
    khoa cu chan viec do bang mot loi TRUNG KHOA ma ke toan ⛔ khong hieu.

    ⇒ Khoa chinh la `link_id` (**mot LAN ghep**), khoa duy nhat la
      `(itl_id, pm_line_id, lan)`. Bat bien cu ⛔ khong mat — no chi hep dung
      pham vi that: **mot lan ghep** la duy nhat, ⛔ khong phai mot doi.
    """
    t = TABLES["fls_pm_link"]
    assert t.pk_cols == ("link_id",), (
        "moi noi phai co danh tinh RIENG: khong co no thi ⛔ khong bo duoc mot "
        "moi noi ma khong xoa dong nao (`INV-I08`)")
    assert ("itl_id", "pm_line_id", "lan") in t.unique_keys, (
        "mat khoa nay thi hai moi noi y het nhau cung LAN cung vao duoc kho")
    assert {c.name for c in t.columns} >= {"link_id", "lan"}


def test_fls_reject_co_UNIQUE_run_source_row():
    """Dong `GAP-DB-P0-03`: chan trung o TANG KHO, khong chi trong cau INSERT."""
    assert ("run_id", "source_row") in TABLES["fls_reject"].unique_keys


# ------------------------------------------------------------------ cong doi chieu
@pytest.mark.pg
def test_pg_verify_BAT_DUOC_khoa_bi_bo():
    """⭐ Cong phai thay do: bo khoa trong kho thi `pg_verify` phai bao.

    Chay tren kho TEST (co DDL that), ⛔ khong pha kho that.
    """
    # ⚠ Nan nhan DOI 2026-08-28: khoa chinh cua `fls_pm_link` gio ⛔ KHONG
    # con drop duoc — `fls_pm_unlink.link_id` co FK tro vao no, va PostgreSQL
    # tu chan. Do la mot rang buoc MANH HON cai bai nay do, nhung no lam bai
    # nay ⛔ khong the tu tay pha nua ⇒ chuyen sang `fls_pm_unlink`.
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert so_sanh_voi_db(c) == [], "kho test phai khop truoc khi thu pha"
        c.execute("ALTER TABLE fls_pm_unlink DROP CONSTRAINT fls_pm_unlink_pk")
        try:
            lech = so_sanh_voi_db(c)
            assert any("khoa chinh khai" in m and "fls_pm_unlink" in m
                       for m in lech), lech
        finally:
            c.execute("ALTER TABLE fls_pm_unlink ADD CONSTRAINT "
                      "fls_pm_unlink_pk PRIMARY KEY (unlink_id)")
        assert so_sanh_voi_db(c) == []


@pytest.mark.pg
def test_pg_verify_BAT_DUOC_unique_bi_bo():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        c.execute("ALTER TABLE fls_reject DROP CONSTRAINT fls_reject_run_id_source_row_uq")
        try:
            lech = so_sanh_voi_db(c)
            assert any("UNIQUE khai bao co, DB THIEU" in m for m in lech), lech
        finally:
            c.execute("ALTER TABLE fls_reject ADD CONSTRAINT "
                      "fls_reject_run_id_source_row_uq UNIQUE (run_id, source_row)")
