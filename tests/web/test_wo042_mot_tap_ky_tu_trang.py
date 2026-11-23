# -*- coding: utf-8 -*-
"""`WO-042 (c)` · `BA-07` v3.11 §4g — **MỘT** tập ký tự trắng
`TAP_TRANG_TIEN_TE` *(30)* cho **mọi** phép so tiền tệ: Python · SQL · JS.

⛔⛔ Lỗi gốc *(`KQ-041 F-2`)*: bốn tập khác nhau — Python `str.strip()` **29**
· SQL `btrim(…, E' \\t\\r\\n')` **4** · JS `String.trim()` **25**. PG thật, 6
chuỗi biên ⇒ SQL giữ nguyên, Python ra mã sạch — lệch **6 / 6**.

Ba phần:
  `AC-8` — tập = `{c : c.isspace()} ∪ {U+FEFF}` *(so tập)*; mỗi ký tự `x` của
           tập: `x + 'vnd' + x` ⇒ `'VND'` ở **cả ba** ngôn ngữ *(30 / 30)*;
           `U+200B` ⇒ cả ba **giữ** *(⛔ gỡ)*; tập JS đọc từ nguồn = tập Python.
           ⭐ Mỗi vế tự chứng **chiều ĐỎ** ngay trong bài: luật **cũ** của vế
           ấy chạy trên cùng 30 ca phải hỏng **đúng** số ca `WO-042` khai
           *(SQL 26 · JS 5 · Python 1)* — một bài ⛔ phân biệt được luật cũ với
           luật mới là một bài ⛔ đo gì *(`Đ5`)*.
  `AC-9` — quét `fls/`: `.strip().upper()` chỉ còn định nghĩa `ma_tien_te`
           ＋ `canon/spec.py` *(chữ cột, ⛔ tiền tệ)*; `trim().toUpperCase()`
           trong `fls/web/` **0**; mọi `btrim(i.curr` mang `%(tap)s`, chuỗi
           `E' \\t\\r\\n'` **0**. Tự chứng: chèn một mẫu vào bản sao ⇒ bắt **1**.
  `AC-11` *(một nửa)* — sổ THẬT chỉ đọc: `curr` mang ký tự của tập ở mép
           ⇒ `fls_itl` **0 / N**, `fls_pm_line` **0 / N** *(in mẫu số — `Đ3`)*.

⚠ Ký tự biên dựng bằng `chr(<điểm mã>)` *(Python)* / `String.fromCharCode`
*(JS)*, ⛔ chuỗi thoát trong nguồn — xem `fls/canon/tien_te.py`.
"""
from __future__ import annotations

import ast
import glob
import os
import re
import sys

import psycopg
import pytest

from fls.canon.tien_te import TAP_TRANG_TIEN_TE, ma_tien_te
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc
from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg
from tests.web.khung_node import _chay, can_node

GOC = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "fls"))
ZWSP = chr(0x200B)
#: ⭐ phía **mong** độc lập: tính từ bảng Unicode của Python lúc chạy
MONG = {chr(i) for i in range(sys.maxunicode + 1) if chr(i).isspace()} | {chr(0xFEFF)}
#: luật SQL **cũ** *(`WO-037` vòng 2)* — để tự chứng chiều ĐỎ
SQL_CU = " \t\r\n"


def _ca(x: str) -> str:
    return x + "vnd" + x


# ═══ AC-8 ⓘ — tập ══════════════════════════════════════════════════════════

def test_AC8_TAP_dung_30_ky_tu_bang_isspace_cong_BOM():
    assert len(TAP_TRANG_TIEN_TE) == 30, len(TAP_TRANG_TIEN_TE)
    assert len(set(TAP_TRANG_TIEN_TE)) == 30, "⛔ ký tự lặp trong tập"
    assert set(TAP_TRANG_TIEN_TE) == MONG, (
        sorted(hex(ord(c)) for c in set(TAP_TRANG_TIEN_TE) ^ MONG))
    assert ZWSP not in TAP_TRANG_TIEN_TE


def test_AC8_ten_cu_man_ghep_la_CUNG_mot_ham():
    """`mg.ma_tien_te` *(mọi chỗ gọi cũ)* là **cùng đối tượng** — ⛔ bản hai."""
    assert mg.ma_tien_te is ma_tien_te
    assert mg.TAP_TRANG_TIEN_TE is TAP_TRANG_TIEN_TE


# ═══ AC-8 ⓘⓘ ⓘⓘⓘ — Python ═══════════════════════════════════════════════════

def test_AC8_PYTHON_30_tren_30_va_GIU_U200B():
    hong = [hex(ord(x)) for x in TAP_TRANG_TIEN_TE if ma_tien_te(_ca(x)) != "VND"]
    assert not hong, hong
    assert ma_tien_te(_ca(ZWSP)) == _ca(ZWSP).upper(), "⛔ gỡ U+200B"
    # ⭐ chiều ĐỎ của luật Python cũ *(`str.strip()` trần)*: hỏng đúng U+FEFF
    cu = [hex(ord(x)) for x in TAP_TRANG_TIEN_TE if _ca(x).strip().upper() != "VND"]
    assert cu == ["0xfeff"], cu
    assert ma_tien_te(None) == "" and ma_tien_te("") == "" and ma_tien_te(" ") == ""


# ═══ AC-8 — PG kho TEST *(chỉ SELECT biểu thức, ⛔ chạm bảng)* ═══════════════

@pytest.mark.pg
def test_AC8_PG_30_tren_30_tham_so_TU_HANG_va_GIU_U200B():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"

        def sql(x: str, tap: str) -> str:
            return c.execute("SELECT upper(btrim(%s::text, %s::text))",
                             (x, tap)).fetchone()[0]

        hong = [hex(ord(x)) for x in TAP_TRANG_TIEN_TE
                if sql(_ca(x), TAP_TRANG_TIEN_TE) != "VND"]
        giu = sql(_ca(ZWSP), TAP_TRANG_TIEN_TE)
        cu = [x for x in TAP_TRANG_TIEN_TE if sql(_ca(x), SQL_CU) != "VND"]
    assert not hong, hong
    assert giu == _ca(ZWSP).upper(), "⛔ PG gỡ U+200B"
    # ⭐ chiều ĐỎ *(WO `AC-8`)*: SQL giữ `E' \t\r\n'` ⇒ hỏng **26 / 30**
    assert len(cu) == 26, len(cu)


@pytest.mark.pg
def test_AC8_SQL_lenh_cho_HAI_cau_cung_doc_tham_so_tap():
    """Hai câu SQL so tiền tệ của `itl-candidates` đọc `%(tap)s` *(⛔ chuỗi
    gõ lại)*, và lời gọi truyền **chính** hằng — đọc nguồn lời gọi."""
    sql = lc._SQL_ITL_UNG_VIEN + lc._SQL_DEM_CUNG_TE
    assert sql.count("upper(btrim(i.curr, %(tap)s))") == 2, sql
    src = open(os.path.join(GOC, "repo", "lenh_cho.py"), encoding="utf-8").read()
    assert src.count('"tap": TAP_TRANG_TIEN_TE') == 2, "⛔ tham số tap ⛔ từ hằng"


# ═══ AC-8 — JS *(node, `TP` thật)* ═════════════════════════════════════════

_JS = """
  const ma = %(ma)s;
  const ca = x => String.fromCharCode(x) + 'vnd' + String.fromCharCode(x);
  return {tap: Array.from(TP.TAP_TRANG_TIEN_TE).map(c => c.charCodeAt(0)),
          hong: ma.filter(x => TP.ma_te(ca(x)) !== 'VND'),
          cu: ma.filter(x => ca(x).trim().toUpperCase() !== 'VND'),
          zw: TP.ma_te(ca(0x200B)) === ca(0x200B).toUpperCase(),
          rong: [TP.ma_te(null), TP.ma_te(undefined), TP.ma_te('')],
          tien_usd: TP.tien('100', String.fromCharCode(0x85) + 'usd')};
"""


@can_node
def test_AC8_JS_cung_tap_30_tren_30_va_TP_tien_doc_no():
    ma = sorted(ord(c) for c in TAP_TRANG_TIEN_TE)
    r = _chay(_JS % {"ma": ma}, tep=["thanh_phan.js", "goi_cua.js"], vo="")
    assert sorted(r["tap"]) == ma, "⛔ tập JS ≠ tập Python"
    assert len(r["tap"]) == 30
    assert r["hong"] == [], [hex(x) for x in r["hong"]]
    assert r["zw"] is True, "⛔ JS gỡ U+200B"
    assert r["rong"] == ["", "", ""]
    # ⭐ chiều ĐỎ *(WO `AC-8`)*: `trim()` hỏng U+0085 · U+001C…U+001F
    assert sorted(r["cu"]) == [0x1C, 0x1D, 0x1E, 0x1F, 0x85], r["cu"]
    # ⭐ `TP.tien` đọc **cùng** hàm: USD sau U+0085 vẫn là USD ⇒ bảng số lẻ
    #   **2** ⇒ `100,00`. Luật cũ `trim()` coi là mã lạ ⇒ bảng `0` ⇒ `100`.
    assert r["tien_usd"] == "100,00", r["tien_usd"]


# ═══ AC-9 — quét `fls/` ═══════════════════════════════════════════════════

#: chỗ **được phép** mang `.strip().upper()` — tên hàm bao quanh, kèm lý do
DUOC_PHEP = {
    ("canon/tien_te.py", "ma_tien_te"): "định nghĩa — `strip(TAP_TRANG_TIEN_TE)`",
    ("canon/spec.py", "pos_of"): "chữ CỘT của Sheets, ⛔ tiền tệ",
}


def _strip_upper(duong: str) -> list[tuple[str, int]]:
    """`[(hàm bao quanh, dòng)]` của mọi `<x>.strip(…).upper()` — đọc `ast`
    ⇒ chú thích ⛔ tính, chuỗi ⛔ tính."""
    src = open(duong, encoding="utf-8").read()
    cay = ast.parse(src)
    cha: dict[int, str] = {}
    for f in ast.walk(cay):
        if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(f):
                cha.setdefault(id(n), f.name)
    ra = []
    for n in ast.walk(cay):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "upper"
                and isinstance(n.func.value, ast.Call)
                and isinstance(n.func.value.func, ast.Attribute)
                and n.func.value.func.attr == "strip"):
            ra.append((cha.get(id(n), "<module>"), n.lineno))
    return ra


def _tep_py() -> list[str]:
    tep = glob.glob(os.path.join(GOC, "**", "*.py"), recursive=True)
    assert len(tep) > 50, f"⛔ không đo được: chỉ thấy {len(tep)} tệp"
    return tep


def test_AC9_QUET_strip_upper_chi_con_DANH_SACH_CHO_PHEP():
    thay = {}
    for p in _tep_py():
        rel = os.path.relpath(p, GOC).replace("\\", "/")
        for ham, dong in _strip_upper(p):
            thay[(rel, ham)] = dong
    print("WO-042 AC-9 · strip().upper():", thay)
    assert set(thay) == set(DUOC_PHEP), (
        "⛔ phép chuẩn hoá mã viết riêng — gọi `ma_tien_te`:\n"
        + "\n".join(f"{k[0]}:{v} ({k[1]})" for k, v in thay.items()
                    if k not in DUOC_PHEP)
        + f"\n⛔ hoặc chỗ cho phép đã đi: {set(DUOC_PHEP) - set(thay)}")


def test_AC9_QUET_bat_duoc_mau_trong_BAN_SAO(tmp_path):
    """⭐ Tự chứng *(`Đ5`)*: chèn `(x or "").strip().upper()` vào **bản sao**
    `ghi_tay.py` ⇒ bắt **1**; bản gốc **0**."""
    p = os.path.join(GOC, "repo", "ghi_tay.py")
    assert _strip_upper(p) == []
    t = tmp_path / "ghi_tay_sao.py"
    t.write_text(open(p, encoding="utf-8").read()
                 + "\n\ndef _xau(x):\n    return (x or \"\").strip().upper()\n",
                 encoding="utf-8")
    assert _strip_upper(str(t)) == [("_xau", _strip_upper(str(t))[0][1])]


_CHU_THICH_JS = re.compile(r"/\*.*?\*/|//[^\n]*", re.S)


def test_AC9_QUET_JS_khong_trim_toUpperCase():
    tep = glob.glob(os.path.join(GOC, "web", "tep", "*.js"))
    assert len(tep) > 5, tep
    xau = []
    for p in tep:
        src = _CHU_THICH_JS.sub("", open(p, encoding="utf-8").read())
        xau += [f"{os.path.basename(p)} · {m.group(0)}"
                for m in re.finditer(r"trim\(\)\s*\.\s*toUpperCase\(\)", src)]
    assert not xau, xau
    # tự chứng: mẫu cũ của `thanh_phan.js:192` bị bắt
    assert re.search(r"trim\(\)\s*\.\s*toUpperCase\(\)",
                     "String(c).trim().toUpperCase();")


def _chuoi_khong_docstring(duong: str) -> list[tuple[int, str]]:
    cay = ast.parse(open(duong, encoding="utf-8").read())
    doc = set()
    for n in ast.walk(cay):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef)) and n.body:
            d = n.body[0]
            if isinstance(d, ast.Expr) and isinstance(d.value, ast.Constant):
                doc.add(id(d.value))
    return [(n.lineno, n.value) for n in ast.walk(cay)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in doc]


def test_AC9_QUET_SQL_btrim_i_curr_MANG_tham_so_tap():
    cu = "E' " + "\\t\\r\\n'"
    co, xau = 0, []
    for p in _tep_py():
        for dong, s in _chuoi_khong_docstring(p):
            if cu in s:
                xau.append(f"{os.path.relpath(p, GOC)}:{dong} · chuỗi tập cũ")
            for m in re.finditer(r"btrim\(\s*i\.curr\s*,\s*(%\(tap\)s|[^)]*)\)", s):
                co += 1
                if m.group(1).strip() != "%(tap)s":
                    xau.append(f"{os.path.relpath(p, GOC)}:{dong} · {m.group(0)}")
    assert co == 2, f"⛔ không đo được / số chỗ đổi: {co}"
    assert not xau, xau


# ═══ AC-11 *(một nửa)* — sổ THẬT chỉ đọc: ⛔ dòng nào mang ký tự của tập ở mép ═

@pytest.mark.pg
def test_AC11_SO_THAT_khong_curr_nao_mang_ky_tu_cua_TAP_o_mep():
    with noi_chi_doc(dsn_that()) as c:
        assert c.execute("SHOW default_transaction_read_only").fetchone()[0] == "on"
        ra = {}
        for bang in ("fls_itl", "fls_pm_line"):
            n, mep = c.execute(
                f"SELECT count(*), count(*) FILTER (WHERE curr IS NOT NULL AND"
                f" btrim(curr, %s) <> curr) FROM {bang}",
                (TAP_TRANG_TIEN_TE,)).fetchone()
            ra[bang] = (mep, n)
    print("WO-042 AC-11 · curr mang ký tự của tập ở mép (chạm / mẫu số):", ra)
    for bang, (mep, n) in ra.items():
        assert n > 0, f"⛔ không đo được: {bang} rỗng (Đ3)"
        assert mep == 0, (bang, mep, n)
