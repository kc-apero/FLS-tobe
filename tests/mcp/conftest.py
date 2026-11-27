"""Đồ nghề chung cho bài cổng MCP (`WO-371`).

⭐ Kho: `fls_test` (⛔ kho THẬT — `dsn_test()` nổ nếu trỏ nhầm). Vai đọc: một vai RIÊNG cho bài
`fls_mcp_doc_<pid>` dựng đúng như `tools/staging/sql/02b_phan_quyen.sql` §1 + `02a_quan_tri.sql`
(`GRANT SELECT ON ALL TABLES` · `default_transaction_read_only = on`) — ⛔ SUPERUSER, ⛔ quyền ghi. Vai do
siêu quyền cụm cục bộ tạo (`runuser postgres`, như `tests/staging/ho_tro.py`) và được DỌN khi xong.
Dữ liệu mẫu: một lần nạp `NAP-2000-01-01-M…` riêng (⛔ đụng dòng bài khác) — 3 dòng sổ + 2 dòng lệnh.
"""
from __future__ import annotations

import contextlib
import json
import os
import urllib.parse
import uuid
from decimal import Decimal

import pytest

from fls.db.kho import dsn_test, noi_chi_doc, tao_kho_test

VAI = f"fls_mcp_doc_{os.getpid()}"
MK = "MKGIA-mcp-doc-" + uuid.uuid4().hex[:12]


def _quan_tri(sql: str, kho: str = "postgres") -> str:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "staging"))
    from ho_tro import chay_quan_tri      # skip nếu ⛔ có siêu quyền cục bộ
    return chay_quan_tri(sql, kho)


@pytest.fixture(scope="session")
def kho_mcp():
    import psycopg
    dsn, _ = tao_kho_test()
    p = urllib.parse.urlparse(dsn)
    ten_kho = p.path.lstrip("/")
    _quan_tri(f"DROP ROLE IF EXISTS {VAI}")
    _quan_tri(f"CREATE ROLE {VAI} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD '{MK}'")
    _quan_tri(f"ALTER ROLE {VAI} SET default_transaction_read_only = on")
    _quan_tri(f'GRANT CONNECT ON DATABASE "{ten_kho}" TO {VAI}')
    _quan_tri(f"GRANT USAGE ON SCHEMA public TO {VAI}", ten_kho)
    _quan_tri(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {VAI}", ten_kho)
    _quan_tri(f"GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO {VAI}", ten_kho)
    dsn_doc = urllib.parse.urlunparse(p._replace(netloc=f"{VAI}:{MK}@{p.hostname}:{p.port or 5432}"))

    run = "NAP-2000-01-01-M" + uuid.uuid4().hex[:6].upper()
    itl = []
    with psycopg.connect(dsn, autocommit=True) as c:
        c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version, mapping_version)"
                  " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        for i, (tien, curr) in enumerate([("1500000.00", "VND"), ("2500.50", "USD"), ("700000.00", "VND")]):
            itl.append(c.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row, run_id,"
                " contract_version, canon_version, mapping_version, raw_frozen, canon, doc_no, curr, ps_no,"
                " work_status, period_state) VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,"
                " '{}'::jsonb,%s,%s,%s,'UNMAPPED','open') RETURNING itl_id",
                (uuid.uuid4().hex, 9000 + i, run, f"FT-MCP-{i}", curr, Decimal(tien))).fetchone()[0])
        for i in range(2):
            c.execute("INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, curr, source_row, amount, tho,"
                      " pe_slip, pe_line, pe_loai) VALUES (%s,%s,%s,'VND',%s,%s,%s,%s,%s,'Advance')",
                      (run, f"PML-MCP-{i}", f"PE-MCP-{i}", 100 + i, Decimal("1000000.00"),
                       json.dumps({"ID PMLine": f"PML-MCP-{i}", "Amount": "1000000", "Tên tài khoản": "Thu"}),
                       f"PE-MCP-{i}", f"PML-MCP-{i}"))
    try:
        yield {"dsn": dsn, "dsn_doc": dsn_doc, "vai": VAI, "run": run, "itl": itl}
    finally:
        _quan_tri(f"REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {VAI}", ten_kho)
        _quan_tri(f"REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM {VAI}", ten_kho)
        _quan_tri(f"REVOKE ALL ON SCHEMA public FROM {VAI}", ten_kho)
        _quan_tri(f'REVOKE ALL ON DATABASE "{ten_kho}" FROM {VAI}')
        _quan_tri(f"DROP ROLE IF EXISTS {VAI}")


def mo_doc_vai(dsn_doc: str):
    """Mở kết nối bằng VAI ĐỌC (như `tools/chay_mcp.mo_doc`, nhưng vai riêng của bài)."""
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_doc)
        try:
            yield conn
        finally:
            conn.close()
    return mo


@pytest.fixture()
def nhat_ky():
    return []


@pytest.fixture()
def cong_cu(kho_mcp, nhat_ky):
    from fls.mcp.cong_cu import CauHinh, CongCu
    return CongCu(mo_doc_vai(kho_mcp["dsn_doc"]), CauHinh(han_ms=1_500, toc_do_phut=1000),
                  ghi_nhat_ky=nhat_ky.append)


__all__ = ["dsn_test", "mo_doc_vai"]
