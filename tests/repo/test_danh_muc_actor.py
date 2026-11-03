# -*- coding: utf-8 -*-
"""`WO-011 T1`+`T4` — SỔ ACTOR một chỗ, và luật UAT một luật hai mặt.

⛔⛔ **Vì sao bài này tồn tại.** Thước mốc `B` vỡ **ba** lần cùng một kiểu —
*trừ đi cái đã biết là máy* — và cái *đã biết* mỗi lần là **một** chuỗi gõ tay
trong một câu SQL *(xem docstring `fls/repo/danh_muc_actor.py`)*. Đo 01/10 khuya:
mã có **8** actor ⛔ phải người, phép đếm biết **1**.

⭐ Ba chốt, mỗi chốt một chiều ĐỎ *(`Đ5`)*:
  ⓐ bài **quét mã**: mọi hằng chuỗi dạng `…@fls…` / `…@apero.vn` trong `fls/` +
    `tools/` *(⛔ `tests/`)* ⊆ `ACTOR_MAY ∪ ACTOR_DA_THAY` — thêm một hằng
    `"thu-moi@fls"` vào một tệp `tools/` ⇒ ĐỎ;
  ⓑ **⛔ gõ lại**: một hằng **bằng đúng** một actor máy chỉ được có ở **một**
    tệp — chính sổ; mọi chỗ khác **lấy từ** sổ;
  ⓒ sổ máy ghim **đủ** — xoá `nhip@fls` khỏi `ACTOR_MAY` ⇒ ĐỎ *(cả ⓐ lẫn ⓒ)*.
"""
from __future__ import annotations

import ast
import pathlib
import re
import warnings

import pytest

from fls.repo import danh_muc_actor as dm

GOC = pathlib.Path(__file__).resolve().parents[2]
SO = GOC / "fls" / "repo" / "danh_muc_actor.py"
# ⭐ Một actor = phần trước `@` + miền `fls`/`apero.vn` + hậu tố `(…)` tuỳ chọn
#   *(`nhip@fls(tay)`)*. Bắt cả trong câu dài *(docstring, câu SQL)*.
MAU_ACTOR = re.compile(r"[A-Za-z0-9_.+-]+@(?:fls|apero\.vn)(?:\([^)\s'\"`]*\))?")


def _tep_quet() -> list[pathlib.Path]:
    ra = []
    for goc in (GOC / "fls", GOC / "tools"):
        for p in goc.rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts \
                    and p.suffix in {".py", ".cmd", ".js", ".html", ".css",
                                     ".json", ".sql", ".ps1", ".md", ".txt"}:
                ra.append(p)
    assert len(ra) > 50, f"⛔ không đo được: chỉ thấy {len(ra)} tệp (Đ3)"
    return ra


def _hang_chuoi(p: pathlib.Path) -> list[str]:
    """Mọi HẰNG chuỗi của tệp. `.py` đọc bằng `ast` *(⛔ chú thích `#` — chú
    thích ⛔ phải hằng, nó là bia)*; tệp khác đọc nguyên văn."""
    s = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix != ".py":
        # ⚠ Tệp `.cmd`: dòng `rem` là chú thích — ⛔ hằng.
        if p.suffix == ".cmd":
            s = "\n".join(d for d in s.splitlines()
                          if not d.lstrip().lower().startswith("rem"))
        return [s]
    with warnings.catch_warnings():
        # ⚠ vài tệp mang chuỗi `'\|'` cũ — cảnh báo cú pháp ⛔ phải việc của bài này
        warnings.simplefilter("ignore", SyntaxWarning)
        cay = ast.parse(s)
    return [n.value for n in ast.walk(cay)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def test_QUET_MA__moi_hang_actor_trong_fls_tools_THUOC_so():
    """ⓐ — chiều ĐỎ: thêm `"thu-moi@fls"` vào một tệp `tools/` ⇒ bài này ĐỎ."""
    so = dm.ACTOR_MAY | dm.ACTOR_DA_THAY
    la: dict[str, list[str]] = {}
    tong = 0
    for p in _tep_quet():
        for h in _hang_chuoi(p):
            for a in MAU_ACTOR.findall(h):
                tong += 1
                if a not in so:
                    la.setdefault(a, []).append(p.relative_to(GOC).as_posix())
    assert tong > 0, "⛔ không đo được: quét ra 0 actor — mẫu vỡ? (Đ3)"
    assert not la, (
        "⛔ actor ⛔ thuộc sổ nào — khai vào `fls/repo/danh_muc_actor.py` "
        f"(ACTOR_MAY nếu là máy, ACTOR_DA_THAY nếu ⛔ phải máy): {la}")


def test_KHONG_GO_LAI__hang_bang_dung_actor_may_chi_o_SO():
    """ⓑ — `may_ghep.MAY`, `nhip_chup.ACTOR_NHIP`… **lấy từ** sổ, ⛔ gõ lại.

    ⚠ Câu SQL **thuần** của `tools/kiem_so_song.py` *(bài nghiệm thu đọc nó bằng
      `ast`)* mang bản chép danh sách — nhưng nó **chứa** actor trong một câu,
      ⛔ **bằng** actor, nên bài này ⛔ đếm nó; chốt của nó là `_kiem_hang_may`
      *(`HOI-012` câu 2)*.
    """
    go: dict[str, set[str]] = {}
    for p in _tep_quet():
        if p.suffix != ".py":
            continue
        for h in _hang_chuoi(p):
            if h in dm.ACTOR_MAY:
                go.setdefault(h, set()).add(p.relative_to(GOC).as_posix())
    sai = {a: t for a, t in go.items() if t != {"fls/repo/danh_muc_actor.py"}}
    assert set(go) == set(dm.ACTOR_MAY), (
        f"⛔ không đo được: sổ có actor ⛔ ở dạng hằng: {set(dm.ACTOR_MAY) - set(go)}")
    assert not sai, f"⛔ hằng actor máy gõ lại ngoài sổ: {sai}"


def test_hang_cu_LA_hang_cua_so():
    """ⓑ — các tên cũ còn sống *(nhiều chỗ import chúng)* nhưng **trỏ** về sổ."""
    from fls.repo import may_ghep, nhip_chup

    assert may_ghep.MAY is dm.ACTOR_MAY_GHEP
    assert nhip_chup.ACTOR_NHIP is dm.ACTOR_NHIP
    assert nhip_chup.ACTOR_TAY is dm.ACTOR_NHIP_TAY


def test_SO_MAY_du_va_ghim():
    """ⓒ — ghim **đủ** *(`WO-011 AC-1`, sau `HOI-012` câu 1)*. Xoá một tên ⇒ ĐỎ.

    ⚠ `ke-toan@apero.vn` **⛔ ở đây**: nó là actor **người mẫu** của bài nghiệm
      thu `KQ-002` *(`test_DOI_CHUNG…` — một cú bấm người phải đếm được)*; công cụ
      từng mượn nó nay mang tên máy `verify-sua-duoc-gi@fls`.
    """
    assert dm.ACTOR_MAY == {
        "may@fls", "nhip@fls", "nhip@fls(tay)", "dung-lai-so@apero.vn",
        "thu@apero.vn", "cong-ghi@apero.vn", "cong@apero.vn",
        "verify-sua-duoc-gi@fls", "verify-sua-duoc-gi-2@fls"}
    assert "ke-toan@apero.vn" not in dm.ACTOR_MAY
    assert dm.ACTOR_DA_THAY == {"khanhcq@apero.vn"}
    assert not dm.ACTOR_MAY & dm.ACTOR_DA_THAY, "⛔ một actor ở CẢ HAI sổ"


# ══ `T4` — UAT một luật, hai mặt ════════════════════════════════════════════
#
# ⭐ Bảng mẫu `AC-5` + biên. `(reason, mong_la_uat)`.
BANG_UAT = [
    ("UAT 02/10 - thu duong ghi", True),
    ("uat 02/10 - chu thuong", True),
    ("  UAT 02/10 - khoang trang dau", True),
    ("UAT02/10", True),
    ("Uat: thu", True),
    ("UAT", True),
    ("\tUAT 02/10", True),
    ("\nuat-thu", True),
    ("\u00a0UAT 02/10", True),          # NBSP — `[[:space:]]` ⛔ nhận, xem sổ
    ("\u3000UAT", True),
    ("\ufeffuat:", True),
    ("UAT_02", True),
    ("UAT\u0301", True),                # dấu kết hợp ⛔ phải chữ cái
    ("(may dien) ghep tren man - nguoi bam khong ghi ly do", False),
    ("ghi chú UAT 02/10", False),
    ("UATX 02/10", False),
    ("uatx", False),
    ("UATé", False),
    ("UATđ", False),
    ("UATƯ", False),
    ("UAT中", False),
    ("UẤT ức", False),
    ("xUAT 02/10", False),
    ("", False),
    (None, False),
]


@pytest.mark.parametrize("ly_do,mong", BANG_UAT)
def test_la_uat_PYTHON_theo_bang_mau(ly_do, mong):
    assert dm.la_uat(ly_do) is mong


@pytest.mark.pg
def test_la_uat_SQL_TRUNG_Python_tren_CUNG_bang_mau():
    """`AC-5` — **một** hàm, **một** mẩu SQL; gọi cả hai trên cùng bảng mẫu.

    Chiều ĐỎ: mẩu SQL trả về `left(…, 4) <> 'UAT '` ⇒ 3 biến thể đầu lệch;
    `'%UAT%'` ⇒ `'ghi chú UAT …'` lệch; bỏ `coalesce` ⇒ `NULL` lệch.
    """
    import psycopg

    from fls.db.kho import dsn_test

    gia = ", ".join(
        f"({i}, {'NULL' if x is None else dm._chuoi_sql(x)}::text)"
        for i, (x, _m) in enumerate(BANG_UAT))
    cau = (f"SELECT i, {dm.sql_la_uat('r')}, {dm.sql_khong_uat('r')}"
           f" FROM (VALUES {gia}) v(i, r) ORDER BY i")
    with psycopg.connect(dsn_test()) as c:
        kq = c.execute(cau).fetchall()
    assert len(kq) == len(BANG_UAT)
    lech = [(BANG_UAT[i][0], la, dm.la_uat(BANG_UAT[i][0]))
            for i, la, khong in kq
            # ⚠ `khong` phải đúng là `not la` — `NULL` (bỏ `coalesce`) cũng lệch
            if la is not dm.la_uat(BANG_UAT[i][0])
            or khong is not (not dm.la_uat(BANG_UAT[i][0]))]
    assert not lech, f"⛔ SQL ≠ Python (reason, sql, python): {lech}"


@pytest.mark.pg
def test_sql_ngoai_may_loai_DU_so_va_giu_NGUOI():
    import psycopg

    from fls.db.kho import dsn_test

    ds = sorted(dm.ACTOR_MAY) + ["khanhcq@apero.vn", "ke-toan@apero.vn", None]
    gia = ", ".join(f"({'NULL' if a is None else dm._chuoi_sql(a)}::text)"
                    for a in ds)
    with psycopg.connect(dsn_test()) as c:
        n = c.execute(f"SELECT count(*) FROM (VALUES {gia}) v(actor)"
                      f" WHERE {dm.sql_ngoai_may('actor')}").fetchone()[0]
    assert n == 3, f"⛔ mong 3 người (2 actor + NULL), đếm {n}"
