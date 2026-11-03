import json
import pathlib

from fls.db.render import render_erd_json, render_erd_mermaid
from fls.db.schema import TABLES

_ROOT = pathlib.Path(__file__).resolve().parents[2]
JSON_PATH = _ROOT / "ERD-CONTRACT.json"
MMD_PATH = _ROOT / "ERD-CONTRACT.mmd"


def test_g_erd_1_json_khop_code():
    """G-ERD-1: doi schema ma quen sinh lai ERD => do."""
    assert json.loads(JSON_PATH.read_text(encoding="utf-8")) == render_erd_json(TABLES), (
        "ERD-CONTRACT.json lech schema. Chay: python -m fls.db.erd_export --write")


def test_g_erd_1_mermaid_khop_code():
    assert MMD_PATH.read_text(encoding="utf-8") == render_erd_mermaid(TABLES), (
        "ERD-CONTRACT.mmd lech schema. Chay: python -m fls.db.erd_export --write")


def test_erd_json_co_quan_he_fk():
    erd = render_erd_json(TABLES)
    cap = {(r["from"], r["to"]) for r in erd["relations"]}
    assert ("fls_journal", "fls_itl") in cap
    assert ("fls_itl", "fls_le") in cap


import re

from fls.db.erd_policy import BA_ERD_DOC, ERD_ISLANDS


def _entity_trong_doc_BA() -> set[str]:
    """Doc khoi ```mermaid erDiagram trong 05_DATA_DICTIONARY_ERD.md."""
    txt = BA_ERD_DOC.read_text(encoding="utf-8")
    khoi = re.search(r"```mermaid\s*\nerDiagram\n(.*?)```", txt, re.S)
    assert khoi, "khong tim thay khoi erDiagram trong doc BA"
    return set(re.findall(r"^\s{4}(\w+)\s*\{", khoi.group(1), re.M))


def test_g_erd_2_moi_bang_trong_code_deu_co_tren_ERD_BA():
    """Chieu 1: them bang ma quen ve len ERD => do."""
    thieu = set(TABLES) - _entity_trong_doc_BA()
    assert not thieu, f"bang co trong code nhung VANG tren ERD cua BA: {sorted(thieu)}"


def test_g_erd_2_moi_entity_tren_ERD_BA_deu_ton_tai_trong_code():
    """Chieu 2: ERD ve entity khong co thuc => do."""
    du = _entity_trong_doc_BA() - set(TABLES)
    assert not du, f"entity tren ERD cua BA nhung KHONG co trong code: {sorted(du)}"


def test_g_erd_3_moi_bang_toi_duoc_fls_itl_hoac_khai_island():
    """G-ERD-3: khong co bang mo coi lang le."""
    canh: dict[str, set[str]] = {}
    for n, t in TABLES.items():
        if t.kind == "view":
            continue
        canh[n] = {c.fk.split(".")[0] for c in t.columns if c.fk} | {n}
    ke: dict[str, set[str]] = {n: set() for n in canh}
    for n, ds in canh.items():
        for d in ds:
            if d in ke:
                ke[n].add(d)
                ke[d].add(n)
    toi_duoc, hang_doi = set(), ["fls_itl"]
    while hang_doi:
        cur = hang_doi.pop()
        if cur in toi_duoc:
            continue
        toi_duoc.add(cur)
        hang_doi.extend(ke.get(cur, ()))
    mo_coi = set(canh) - toi_duoc
    assert mo_coi <= ERD_ISLANDS, (
        f"bang khong noi voi fls_itl va chua khai island: {sorted(mo_coi - ERD_ISLANDS)}")


def test_g_erd_3_moi_island_phai_co_ly_do_bang_chu():
    for n in ERD_ISLANDS:
        assert TABLES[n].island_reason.strip(), f"{n} khai island nhung khong co ly do"
