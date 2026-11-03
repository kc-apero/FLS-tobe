"""Cong quet MA NGUON: ⛔ khong file test nao duoc tu tro vao kho THAT.

⛔⛔ **Vi sao can cong nay, khong chi can sua 5 file.** Sua 5 file la sua *lan
nay*. Nguoi viet file test PG **thu sau** rat de go lai dung dong cu:

    DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")

va o nhiem quay lai **trong im lang** — vi test van xanh, chi co so ban them.
Day dung ho voi lo *"luat o-loi tung nam BON ban sao"*: sua ban sao khong bang
lam cho ban sao moi **khong the ton tai**.

⇒ Luat: trong `tests/`, duong duy nhat toi mot kho la `fls.db.kho`.
Ngoai le duy nhat: chinh hai file cong nay.
"""
from __future__ import annotations

import pathlib
import re

GOC = pathlib.Path(__file__).resolve().parent.parent          # tests/
TEN_KHO_THAT = "fls"

# File duoc phep noi ten kho that / doc bien moi truong truc tiep
NGOAI_LE = {
    "db/test_kho.py",                              # kiem chinh chan cung do
    "db/test_khong_ai_tro_lai_kho_that.py",        # file nay
}

# `postgresql://.../fls` hay `postgres://.../fls` — ten kho that o cuoi
_DSN_THAT = re.compile(r"postgres(?:ql)?://[^\s\"']*/" + TEN_KHO_THAT + r"(?![\w-])")
_DOC_BIEN = re.compile(r"""environ(?:\.get)?\(\s*["']PG_DSN["']""")


def _cac_file_test() -> list[tuple[str, str]]:
    ra = []
    for p in sorted(GOC.rglob("*.py")):
        rel = p.relative_to(GOC).as_posix()
        if rel in NGOAI_LE:
            continue
        ra.append((rel, p.read_text(encoding="utf-8")))
    return ra


def test_khong_file_test_nao_ghi_cung_dia_chi_kho_that():
    xau = [rel for rel, t in _cac_file_test() if _DSN_THAT.search(t)]
    assert not xau, (
        "cac file test viet cung dia chi kho THAT: " + ", ".join(xau)
        + " — dung `from fls.db.kho import dsn_test` thay vi go DSN. "
        "Day la co che da lam 1.204 dong dau test lan vao `fls_itl` 27/08."
    )


def test_khong_file_test_nao_doc_PG_DSN_truc_tiep():
    """`PG_DSN` la bien cua kho THAT. Test doc no truc tiep = tro vao so."""
    xau = [rel for rel, t in _cac_file_test() if _DOC_BIEN.search(t)]
    assert not xau, (
        "cac file test doc `PG_DSN` truc tiep: " + ", ".join(xau)
        + " — kho cua test lay tu `fls.db.kho.dsn_test()`, no NO neu tro vao "
        "kho that."
    )


def test_cong_nay_that_su_quet_duoc_gi():
    """⛔ Cong chung #7: quet 0 file thi la CHUA DO DUOC GI, khong phai 'sach'."""
    files = _cac_file_test()
    assert len(files) >= 20, f"chi quet duoc {len(files)} file test — nghi ngo"
    assert any("psycopg" in t for _, t in files), "khong thay file test PG nao"
