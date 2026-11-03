"""Chan cung: bo test ⛔ khong cham duoc kho THAT.

Bai quan trong nhat o day la `test_dsn_test_NO_khi_tro_vao_kho_that`: no khoa
dung co che da lam 1.204 dong dau test lan vao `fls_itl` ngay 27/08 — nam file
test PG lay MAC DINH la dia chi kho that.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db import kho


def test_ten_kho_boc_dung_ten():
    assert kho.ten_kho("postgresql://fls:fls@localhost:5433/fls") == "fls"
    assert kho.ten_kho("postgresql://u:p@h:1/fls_test") == "fls_test"
    assert kho.ten_kho("postgresql://u:p@h:1/") == ""


def test_doi_ten_kho_giu_nguyen_phan_con_lai():
    d = kho.doi_ten_kho("postgresql://fls:fls@localhost:5433/fls", "fls_test")
    assert d == "postgresql://fls:fls@localhost:5433/fls_test"


def test_dsn_test_mac_dinh_la_kho_khac_kho_that():
    assert kho.ten_kho(kho.dsn_test()) == kho.TEN_TEST
    assert kho.ten_kho(kho.dsn_test()) != kho.ten_kho(kho.dsn_that())


def test_dsn_test_NO_khi_tro_vao_kho_that(monkeypatch):
    """⛔ Khoa co che da gay ban so: test tro vao kho that.

    Ke ca khi nguoi ta co tinh dat `PG_DSN_TEST = PG_DSN`, duong nay phai NO —
    ⛔ khong duoc lang le chay tiep roi ghi vao so.
    """
    monkeypatch.setenv(kho.BIEN_TEST, "postgresql://fls:fls@localhost:5433/fls")
    with pytest.raises(RuntimeError, match="KHO THAT"):
        kho.dsn_test()


def test_dsn_test_NO_khi_khong_noi_ten_kho(monkeypatch):
    monkeypatch.setenv(kho.BIEN_TEST, "postgresql://fls:fls@localhost:5433/")
    with pytest.raises(RuntimeError, match="khong noi ten kho"):
        kho.dsn_test()


def test_tao_kho_test_TU_CHOI_kho_that():
    with pytest.raises(RuntimeError, match="KHO THAT"):
        kho.tao_kho_test("postgresql://fls:fls@localhost:5433/fls")


@pytest.mark.pg
def test_noi_chi_doc_KHONG_GHI_DUOC_len_kho_that():
    """⭐ Chan o TANG DUOI: PostgreSQL tu tu choi, ⛔ khong dua vao ky luat.

    Bai nay chinh la cai da bat duoc `test_verify_bat_duoc_cot_bi_thieu` dang
    `CREATE TABLE` thang vao kho that ma khong ai thay.
    """
    c = kho.noi_chi_doc(kho.dsn_that())
    try:
        with pytest.raises(psycopg.errors.ReadOnlySqlTransaction):
            c.execute("CREATE TABLE thu_ghi_vao_kho_that (x int)")
        # doc thi van duoc
        assert c.execute("select 1").fetchone()[0] == 1
    finally:
        c.close()
