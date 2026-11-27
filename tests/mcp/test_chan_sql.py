"""Lớp chặn ỨNG DỤNG `fls.mcp.chan_sql` — thuần (⛔ kho). Bộ đột biến chạy QUA KHO ở `test_chan_sql_dot_bien.py`."""
from __future__ import annotations

import pytest

from fls.mcp import chan_sql

DUOC = [
    "select 1",
    "SELECT * FROM fls_itl WHERE memo LIKE '%delete%' AND doc_no = 'drop table x'",
    "with a as (select 1 x) select * from a;",
    "select $$; insert into x$$ as s, E'it''s \\' ; update' as e",
    "select 1 -- ; delete from x\n",
    "select /* drop /* lồng */ table */ 1",
    "select current_setting('statement_timeout')",
    "select count(*) filter (where curr = 'VND') from fls_itl",
    "SELECT \"run_id\" FROM fls_run",
    "select offset_x from (select 1 as offset_x) t",       # `set` trong tên ⇒ ⛔ bắt nhầm (\b)
]

CHAN = [
    ("", "RONG"),
    ("insert into fls_run values (1)", "KHONG_PHAI_SELECT"),
    ("select 1; select 2", "NHIEU_CAU"),
    ("select 1;; ", "NHIEU_CAU"),
    ("with x as (delete from fls_itl returning *) select * from x", "TU_KHOA_CAM"),
    ("select * into t_moi from fls_run", "TU_KHOA_CAM"),
    ("select set_config('transaction_read_only','off',true)", "HAM_CAM"),
    ("select \"set_config\"('a','b',false)", "HAM_CAM"),
    ("select pg_catalog.pg_sleep(10)", "HAM_CAM"),
    ("select pg_advisory_lock(1)", "HAM_CAM"),
    ("select pg_read_file('/etc/passwd')", "HAM_CAM"),
    ("select lo_import('/etc/passwd')", "HAM_CAM"),
    ("select nextval('s')", "HAM_CAM"),
    ("select * from fls_itl for update", "TU_KHOA_CAM"),
    ("select * from fls_itl for share", "KHOA_DONG"),
    ("select U&\"\\0073et_config\"('a','b',false)", "UNICODE_ESCAPE"),
    ("select 'chưa đóng", "CHUOI_HO"),
    ("select /* chưa đóng", "CHU_THICH_HO"),
    ("select $a$ chưa đóng", "CHUOI_HO"),
    ("select 1 /**/; DELETE FROM fls_itl", "NHIEU_CAU"),
    ("explain analyze select 1", "KHONG_PHAI_SELECT"),
    ("x" * (chan_sql.DAI_TOI_DA + 1), "QUA_DAI"),
]


@pytest.mark.parametrize("sql", DUOC)
def test_cau_doc_vo_hai_DI_QUA(sql):
    c = chan_sql.kiem(sql)
    assert c.tu_dau in ("SELECT", "WITH")
    assert not c.sql.rstrip().endswith(";")


@pytest.mark.parametrize("sql,ma", CHAN)
def test_cau_bi_CHAN_voi_ma_CO_TEN(sql, ma):
    with pytest.raises(chan_sql.SqlBiChan) as e:
        chan_sql.kiem(sql)
    assert e.value.ma == ma, str(e.value)


def test_dem_mong_hai_chieu():
    """`Đ5` — khai `mong`: 10 câu đi qua · 22 câu bị chặn. Thêm/bớt một câu là phải sửa con số."""
    assert (len(DUOC), len(CHAN)) == (10, 22)
