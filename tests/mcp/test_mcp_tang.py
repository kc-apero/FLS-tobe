"""AC-1 · luật tầng `fls.mcp` (AST) + `.mcp.json` của Claude Code cục bộ.

`import-linter` hợp đồng 1 cấm `psycopg`; bài này cấm thêm `fls.db` · `fls.repo` · `fls.web` — kết nối kho
phải được TRUYỀN VÀO (`tools/chay_mcp.py`), như `fls.api`. ⭐ `fls.api` thì ĐƯỢC: `goi_tuyen` dùng lại
`fls.api.xu_ly.HAM` (⛔ viết lại logic tuyến).
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
CAM = ("fls.db", "fls.repo", "fls.web", "psycopg")
TEP = sorted((GOC / "fls" / "mcp").glob("*.py"))


def _nhap(van: str) -> set[str]:
    ra = set()
    for n in ast.walk(ast.parse(van)):
        if isinstance(n, ast.Import):
            ra |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            ra.add(n.module)
    return ra


def test_co_DUNG_6_tep_va_ky_THUAN_stdlib():
    assert [p.name for p in TEP] == ["__init__.py", "chan_sql.py", "cong_cu.py", "ky.py", "may_chu.py", "xac_thuc.py"]
    nhap = _nhap((GOC / "fls" / "mcp" / "ky.py").read_text(encoding="utf-8"))
    assert nhap == {"__future__", "base64", "hashlib", "hmac", "json"}     # Cloud Shell của chủ ⛔ có `mcp`


@pytest.mark.parametrize("p", TEP, ids=lambda p: p.name)
def test_fls_mcp_KHONG_biet_tang_kho(p):
    sai = sorted(m for m in _nhap(p.read_text(encoding="utf-8")) if m.startswith(CAM))
    assert sai == [], f"{p.name} import {sai}"


def test_bai_tang_CAN_khi_co_import_cam():
    """`Đ5`: bài trên phải ĐỎ với một tệp có `import psycopg` / `from fls.db.kho import …`."""
    for van in ("import psycopg\n", "from fls.db.kho import noi_chi_doc\n", "from fls.repo import x\n"):
        assert any(m.startswith(CAM) for m in _nhap(van))


def test_mcp_json_goi_DUNG_chay_mcp_stdio():
    d = json.loads((GOC / ".mcp.json").read_text(encoding="utf-8"))
    s = d["mcpServers"]["fls"]
    assert s["type"] == "stdio" and s["args"][-1] == "tools/chay_mcp.py" and "--http" not in s["args"]
    van = json.dumps(d)
    import re
    assert re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", van) == []   # ⛔ email trong repo (DSN `fls@localhost` ⛔ phải email)
