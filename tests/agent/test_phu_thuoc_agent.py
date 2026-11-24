# -*- coding: utf-8 -*-
"""`AG2-R1-01` (KQ-357, NẶNG theo orchestrator 24/11): container MỚI dựng từ `requirements.txt` ⇒ `ModuleNotFoundError: google`
ở `dung_be_giu_rieng.py --doc-song`. Bài canh: MỌI `import` bên thứ ba (kể cả nhập muộn trong hàm) của mã agent + công cụ
chạy-thật ⊆ gói khai ở `requirements.txt` (kể cả phần thêm `[extra]` khai đúng).

Đo bằng `ast` (⛔ nhập mô-đun). Mẫu số khai sẵn (Đ3): tập tệp quét ≠ rỗng và tập import bên thứ ba ≠ rỗng.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
REQ = GOC / "requirements.txt"
TEP = sorted({*(GOC / "fls" / "agent").rglob("*.py"), *(GOC / "tools").glob("*voi*.py"),
              GOC / "tools" / "dung_be_giu_rieng.py"})
#: tên mô-đun gốc ⇒ tên gói phân phối (+ extra) phải có trong requirements
GOI = {"anthropic": "anthropic", "google": "google-auth", "requests": "requests", "psycopg": "psycopg", "pytest": "pytest"}
#: phần thêm `anthropic[...]` mà mã dùng: `AnthropicGoogleCloud` ⇒ `google_cloud` · `AnthropicVertex` ⇒ `vertex`
EXTRA_ANTHROPIC = {"AnthropicGoogleCloud": "google_cloud", "AnthropicVertex": "vertex"}
NOI_BO = {"fls", "tools", "tests"} | {p.stem for p in (GOC / "tools").glob("*.py")}


def _req() -> dict[str, set[str]]:
    ra: dict[str, set[str]] = {}
    for d in REQ.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Za-z0-9_.-]+)(?:\[([^\]]*)\])?", d.split("#", 1)[0])
        if m and m.group(1):
            ra[m.group(1).lower()] = {x.strip() for x in (m.group(2) or "").split(",") if x.strip()}
    return ra


def _import_ngoai() -> dict[str, set[str]]:
    """mô-đun gốc bên thứ ba ⇒ tập tệp dùng nó."""
    ra: dict[str, set[str]] = {}
    for p in TEP:
        for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            goc = []
            if isinstance(n, ast.Import):
                goc = [a.name.split(".")[0] for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                goc = [n.module.split(".")[0]]
                if n.module.startswith("google.auth.transport.requests"):
                    goc.append("requests")      # `AuthorizedSession` của google-auth đòi gói `requests` (⛔ tự kéo theo)
            for g in goc:
                if g not in sys.stdlib_module_names and g not in NOI_BO and g != "__future__":
                    ra.setdefault(g, set()).add(str(p.relative_to(GOC)))
    return ra


def test_mau_so_khong_rong():
    assert len(TEP) >= 10, TEP
    assert {"anthropic", "google", "requests"} <= set(_import_ngoai())


def test_moi_import_ben_thu_ba__co_trong_requirements():
    req = _req()
    thieu = {g: sorted(t) for g, t in _import_ngoai().items() if GOI.get(g, g).lower() not in req}
    assert not thieu, f"import bên thứ ba ⛔ khai ở requirements.txt: {thieu}"


def test_extra_anthropic__khop_lop_ma_dung():
    """Mã gọi `sdk.AnthropicGoogleCloud` / `sdk.AnthropicVertex` (nhập muộn qua biến `sdk`) ⇒ extra tương ứng phải khai."""
    van = "\n".join(p.read_text(encoding="utf-8") for p in TEP)
    can = {ex for lop, ex in EXTRA_ANTHROPIC.items() if re.search(rf"\b(sdk|anthropic)\.{lop}\(", van)}
    assert can == {"google_cloud", "vertex"}, can                         # Đ3: mẫu số = 2 lớp mã thật dùng
    assert can <= _req().get("anthropic", set()), _req().get("anthropic")
