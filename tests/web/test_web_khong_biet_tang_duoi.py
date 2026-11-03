"""⛔ `fls.web` ⛔ khong duoc voi xuong tang duoi — moc CHAT hon luat thu 8.

Rang buoc `import-linter` so 8 cam `fls.web` cham `repo`/`db`/`canon`/`ledger`/
`oracle`/`adapters` *(`DEV-12` §3)*. Bai nay ghim mot moc **chat hon**: hom nay
`fls.web` ⛔ khong import **bat cu gi** trong `fls` — ke ca `fls.api`.

⛔⛔ **Vi sao ghim moc chat hon cai luat.** Neu mai sau ai do them
`from fls.api import bao` vao `fls/web/`, `import-linter` van XANH *(luat 8 cho
phep goi `api`)* va ⛔ khong ai dung lai de hoi. Nhung do la mot buoc doi
huong that: tu *"man hinh la mot NGUOI GOI nhu moi nguoi goi khac, di qua HTTP"*
sang *"man hinh la mot phan cua may chu"*. Buoc do co the dung — nhung no phai
duoc **nhin thay**, chu ⛔ khong tron vao mot dong `import`.
"""
from __future__ import annotations

import ast
import os

import pytest

import fls.web

GOC_WEB = os.path.dirname(os.path.abspath(fls.web.__file__))


def _tep_python() -> list[str]:
    return sorted(
        os.path.join(GOC_WEB, n) for n in os.listdir(GOC_WEB)
        if n.endswith(".py"))


def _cac_import(duong: str) -> set[str]:
    with open(duong, encoding="utf-8") as f:
        cay = ast.parse(f.read(), filename=duong)
    ra: set[str] = set()
    for n in ast.walk(cay):
        if isinstance(n, ast.Import):
            ra.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            ra.add(n.module)
    return ra


@pytest.mark.parametrize("tep", _tep_python())
def test_khong_import_gi_trong_fls(tep):
    la = {m for m in _cac_import(tep)
          if m == "fls" or m.startswith("fls.")}
    assert la == set(), (
        f"⛔ {os.path.basename(tep)} import {sorted(la)}. Hom nay `fls.web` la "
        f"mot NGUOI GOI di qua HTTP, ⛔ khong phai mot phan cua may chu. "
        f"Neu doi huong that thi sua bai nay TRUOC, ⛔ dung sua le.")


@pytest.mark.parametrize("tep", _tep_python())
def test_khong_cham_driver_DB(tep):
    assert "psycopg" not in _cac_import(tep)


def test_bai_nay_that_su_doc_duoc_import(tmp_path):
    """⛔ Neu `_cac_import` tra rong voi moi thu thi hai bai tren xanh **vi ⛔
    khong doc duoc gi**, ⛔ khong phai vi sach."""
    t = tmp_path / "gia.py"
    t.write_text("import psycopg\nfrom fls.repo import ghi_tay\n",
                 encoding="utf-8")
    assert _cac_import(str(t)) == {"psycopg", "fls.repo"}


def test_co_it_nhat_mot_tep_python_de_quet():
    assert len(_tep_python()) >= 2, "⛔ ⛔ khong co tep nao de quet"
