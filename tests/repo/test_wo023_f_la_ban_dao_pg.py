# -*- coding: utf-8 -*-
"""`WO-023` `(f)` ⓐ · `BA-07` **v3.6** — `doc_nhat_ky` trả **`la_ban_dao`** *(boolean)*
= có một `fls_adjustment` cùng `(itl_id, field, at, actor)` với `reversal_of IS
NOT NULL` *(`fls_journal` ⛔ có cột trỏ bút toán; `_them` chèn hai dòng **trong
một giao dịch** nên `at` trùng)*.

⛔⛔ Lỗi gốc *(`KQ-025 F-3`)*: màn `F02` ⑦ in bản đảo giá trị **người** `X →
(trống) · người sửa` — **y hệt** cú người xoá ô.

⭐ Gọi **hàm thật** `ghi_tay.*` + `doc_bao_cao.doc_nhat_ky` trên **kho TEST**
*(`assert current_database()`)* — ⛔ dựng lại SQL tay *(`11` §6: "đo quan hệ thì
gọi hàm thật")*. Ca **đảo rồi xoá cùng ô** có mặt để phép nối thiếu `at` *(chỉ
`itl_id, field, actor`)* **ĐỎ**.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import doc_bao_cao as dbc
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import mot_lan_nap

pytestmark = pytest.mark.pg

AI = "lan@apero.vn"


@pytest.fixture()
def ca():
    c = psycopg.connect(dsn_test(), autocommit=True)
    assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
    run = "NAP-2000-01-01-T23F" + uuid.uuid4().hex[:6].upper()
    c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
              " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    itl = c.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, curr, ps_co, work_status)"
        " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,'{}','VND',%s,"
        " 'UNMAPPED') RETURNING itl_id",
        (uuid.uuid4().hex, run, D("1000"))).fetchone()[0]
    yield c, mot_lan_nap(run), itl
    c.close()


def _nk(c, pv, itl, field):
    return [(r["value_after"], r["value_source"], r["la_ban_dao"])
            for r in dbc.doc_nhat_ky(c, pv, itl) if r["field"] == field]


def test_AC8_go_roi_DAO__ban_dao_la_ban_dao_TRUE__cu_go_FALSE(ca):
    c, pv, itl = ca
    k = gt.ghi_but_toan(c, pv, itl, "invoice", "INV-X", actor=AI, reason="go")
    gt.dao_but_toan(c, pv, k.adj_id, actor=AI, reason="dao")
    assert _nk(c, pv, itl, "invoice") == [("INV-X", "sua_tay", False),
                                          (None, "sua_tay", True)]


def test_AC8_DAO_roi_XOA_cung_o__cu_xoa_la_ban_dao_FALSE(ca):
    """⭐ Ca bắt phép nối **thiếu `at`**: cùng `(itl_id, field, actor)` có
    **cả** bản đảo lẫn cú xoá ô ⇒ nối thiếu `at` in *"đảo"* cho cú xoá ⇒ ĐỎ."""
    c, pv, itl = ca
    k = gt.ghi_but_toan(c, pv, itl, "invoice", "INV-Y", actor=AI, reason="go")
    gt.dao_but_toan(c, pv, k.adj_id, actor=AI, reason="dao")
    gt.ghi_but_toan(c, pv, itl, "invoice", "INV-Z", actor=AI, reason="go 2")
    gt.ghi_but_toan(c, pv, itl, "invoice", None, actor=AI, reason="xoa o",
                    force=True)
    assert _nk(c, pv, itl, "invoice") == [
        ("INV-Y", "sua_tay", False), (None, "sua_tay", True),
        ("INV-Z", "sua_tay", False), (None, "sua_tay", False)]


def test_AC8_MOI_dong_nhat_ky_co_la_ban_dao_kieu_BOOL(ca):
    c, pv, itl = ca
    gt.ghi_but_toan(c, pv, itl, "cdt1", "C-1", actor=AI, reason="go")
    gt.ghi_but_toan(c, pv, itl, "invoice", "INV-1", actor=AI, reason="go")
    rows = dbc.doc_nhat_ky(c, pv, itl)
    assert len(rows) == 2, rows
    assert all(type(r["la_ban_dao"]) is bool for r in rows), rows
