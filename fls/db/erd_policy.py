"""Chinh sach cong ERD: doc BA nao la doi chieu, bang nao duoc phep khong noi FK."""

from __future__ import annotations

import pathlib

BA_ERD_DOC = pathlib.Path(
    __file__).resolve().parents[2] / "docs" / "05_DATA_DICTIONARY_ERD.md"

# Bang KHONG noi FK voi fls_itl. Moi ten o day PHAI co island_reason trong schema.
#
# GAP-ERD-P0-01 DA DONG 2026-08-26 (owner chot): them FK fls_itl.run_id -> fls_run.run_id.
# fls_run va fls_reject NOI LIEN fls_itl tu day, da bo khoi danh sach nay (4 -> 2).
# Truoc do go sai run_id thi dong so mat lineage trong im lang, trai INV-I05.
ERD_ISLANDS: frozenset[str] = frozenset({
    "fls_mapping_master",   # tra theo gia tri hd; hd co the UNMAPPED nen khong FK duoc
    "fls_source",           # manifest pipeline, khong gan dong nao
    "fls_migration",        # so ghi di tru — ha tang, khong gan dong so nao (GAP-DB-P0-02)
})
