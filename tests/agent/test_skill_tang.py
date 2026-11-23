# -*- coding: utf-8 -*-
"""WO-329 AC-1 · AC-2 · AC-6 — bộ skill có số thứ tự; checksum prompt trong THẺ = máy tính; tầng gói agent."""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from fls.agent import skill as sk
from fls.agent.chuoi import AGENT

GOC = Path(__file__).resolve().parents[2]
THE = {"A1_RI": "A1_RI.md", "A2_PR_MAP": "A2_PR_MAP.md", "A3_SI_ITL": "A3_SI_ITL.md", "A4_AUDITOR": "A4_AUDITOR.md"}
CAM = ("fls.db", "fls.repo", "fls.api", "fls.web", "psycopg")


@pytest.mark.parametrize("ag", [a.ma for a in AGENT])
def test_bo_skill_04_skill_so_lien(ag):
    assert [s.so for s in sk.nap_bo(ag)] == [1, 2, 3, 4]


def test_so_nhay_hoac_trung__LoiBoSkill(tmp_path):
    goc = sk.THU_MUC / "A1_RI"
    tm = tmp_path / "X"
    tm.mkdir()
    (tm / "01_a.md").write_text((goc / "01_nguon_bank.md").read_text(encoding="utf-8"), encoding="utf-8")
    (tm / "03_b.md").write_text((goc / "02_nguon_fps.md").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(sk.LoiBoSkill, match="nhảy"):
        sk.nap_bo("X", tmp_path)


@pytest.mark.parametrize("ag", [a.ma for a in AGENT])
def test_the_agent_ghi_dung_checksum_prompt(ag):
    van = (GOC / "docs" / "ITL" / "06_Agent" / THE[ag]).read_text(encoding="utf-8")
    m = re.findall(r"checksum prompt[^`]*`([0-9a-f]{16})`", van)
    assert m == [sk.checksum_prompt(ag)], "sửa prompt mà chưa sửa thẻ (hoặc ngược lại)"


def _nhap(van: str) -> set[str]:
    ra = set()
    for n in ast.walk(ast.parse(van)):
        if isinstance(n, ast.Import):
            ra |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            ra.add(n.module)
    return ra


def _vi_pham(van: str) -> set[str]:
    return {m for m in _nhap(van) if any(m == c or m.startswith(c + ".") for c in CAM)}


def test_tang_fls_agent_KHONG_biet_kho_tuyen():
    tep = sorted((GOC / "fls" / "agent").glob("*.py"))
    assert len(tep) >= 9                                       # Đ3: tập quét ⛔ rỗng
    assert {p.name: _vi_pham(p.read_text(encoding="utf-8")) for p in tep if _vi_pham(p.read_text(encoding="utf-8"))} == {}


def test_tang__phep_quet_CO_RANG():
    assert _vi_pham("from fls.repo import doc_bao_cao\nimport psycopg\n") == {"fls.repo", "psycopg"}
