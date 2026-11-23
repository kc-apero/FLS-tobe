# -*- coding: utf-8 -*-
"""`WO-032` **vòng 2** `(i)` — bậc `ma` ở cửa `lenh-da-gan` *(`BA-07` v3.8 §4h ⓵')*.

⛔⛔ Lỗi gốc *(`HOI-033`, `TL-033 ⓐ`)*: `xu_ly._bac` chỉ trả `ma` khi dòng lệnh
mang `ma_canon`; `ma_canon` do `lc.xep_ro` gắn, và `xep_ro` **chỉ** chạy trong
cửa `lenh-cho` ⇒ cửa `lenh-da-gan` ⛔ BAO GIỜ trả `ma`. Sổ thật 02/10 *(chỉ đọc,
gọi hàm thật mọi trang)*: mối nối `gd_ds` khớp số chứng từ **2.262 / 2.262**,
cửa trả `ma` **0** *(`tien` 2.128 · `cung_tien_te` 134)*; khối *"✓ Đang gán"*
*(`gd`, một mỗi lệnh)* chip `①` **0 / 2.219** *(`②` 2.121 · `④` 98)*.

Ba phép đo, ba chiều ĐỎ:
  ① **kho TEST qua HTTP** — ca `B` của `ca_wo032.py` *(đã gán, khớp đúng số CT,
     lệch `500`)* ⇒ `the.gd.bac = 'ma'`, `lech = '500.00'`;
  ② **sổ THẬT, CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, gọi `xu_ly.lenh_da_gan` —
     chính hàm của cửa — **mọi trang**)*: mọi phần tử `gd`/`gd_ds` có
     `canon_ref(ref_tho) == canon_ref(doc_no)` ⇒ `bac = 'ma'`, mẫu số > 0
     *(`Đ3`)*; cửa `lenh-cho` cùng luật *(⛔ hồi quy)*;
  ③ **bài quét nguồn** — **một** chỗ gắn `ma_canon` trong `fls/`, hai cửa danh
     sách cùng đi qua nó *(`(i)`: ⛔ bản thứ hai của phép chia `canon_ref`)*.
"""
from __future__ import annotations

import ast
import os
from collections import Counter
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import canon_ref
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc
from tests.web.ca_wo032 import dung_ca, goi_ca, hang
from tests.web.test_vong_f02_pg import _may

pytestmark = pytest.mark.pg

GOC = os.path.join(os.path.dirname(__file__), "..", "..", "fls")


@pytest.fixture(scope="module")
def ca_da_gan():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    with _may() as m:
        # ⭐ `WO-051` `AC-10`: phạm vi **của ca** — xem `ca_wo032.goi_ca`
        yield ca, goi_ca(m, ca, "/queue/lenh-da-gan?limit=500")["data"]


def _phan_tu(than):
    """`[(khoá, hàng lệnh, phần tử)]` — `gd` và `gd_ds` đếm **riêng** (`Đ4`).
    Phần tử `loi_nguon` ⛔ đủ khuôn ⇒ bỏ *(⛔ có `doc_no`/`bac`)*."""
    ra = []
    for x in than.get("rows") or []:
        th = x.get("the") or {}
        g = th.get("gd")
        if g and "bac" in g:
            ra.append(("gd", x, g))
        for u in th.get("gd_ds") or []:
            if "bac" in u:
                ra.append(("gd_ds", x, u))
    return ra


# ═══ ① kho TEST qua HTTP ═══════════════════════════════════════════════════
def test_AC12_lenh_da_gan_ca_B_khop_so_CT_la_bac_MA_lech_500(ca_da_gan):
    """⛔ Chiều ĐỎ *(mã `363a441`)*: `_bac` thiếu `ma_canon` ⇒ `cung_tien_te`
    *(đúng con số `HOI-033` đo trên kho TEST)* ⇒ ĐỎ."""
    ca, than = ca_da_gan
    x = hang(than, ca["lenh"]["B"])
    g = x["the"]["gd"]
    assert g["itl_id"] == ca["i_b"], g
    assert g["bac"] == "ma", g
    assert str(g["lech"]) == "500.00", g
    assert [u["bac"] for u in x["the"]["gd_ds"]] == ["ma"], x["the"]["gd_ds"]


def test_AC12_lenh_da_gan_MOI_phan_tu_khop_so_CT_la_MA_va_co_ca_MA_lech_khac_0(
        ca_da_gan):
    """Cả trang cửa trả trên kho TEST: khớp mã ⇒ `ma`, 100%; và **≥1** ca bậc
    `ma` lệch ≠ 0 *(chữ `AC-2` ở cửa này — `TL-033 ⓐ`)*."""
    ca, than = ca_da_gan
    ds = _phan_tu(than)
    khop = [(k, x, u) for k, x, u in ds
            if canon_ref(x.get("ref_tho"))
            and canon_ref(u.get("doc_no")) == canon_ref(x.get("ref_tho"))]
    sai = [(k, x["pm_line_id"], u["itl_id"], u["bac"]) for k, x, u in khop
           if u["bac"] != "ma"]
    ma_lech = [u for _k, _x, u in khop
               if u.get("lech") is not None and D(str(u["lech"])) != 0]
    print(f"WO-032 v2 AC-12 · kho TEST lenh-da-gan: {len(ds)} phần tử · khớp "
          f"số CT {len(khop)} · sai bậc {len(sai)} · bậc ma lệch≠0 {len(ma_lech)}")
    assert khop, "⛔ không đo được: 0 phần tử khớp số CT"
    assert not sai, sai
    assert ma_lech, "⛔ không đo được: 0 ca bậc `ma` lệch ≠ 0"


# ═══ ② sổ THẬT — CHỈ ĐỌC, gọi hàm thật mọi trang ═══════════════════════════
def _het_trang(ham, conn, pv):
    from fls.api import xu_ly
    cur, rows = None, []
    while True:
        q = {"limit": "500"}
        if cur:
            q["cursor"] = cur
        out, _ = ham(xu_ly.YeuCau(conn=conn, pv=pv, q=q, tham={}))
        rows += out["rows"]
        cur = out["next_cursor"]
        if not cur:
            return rows


def test_AC12_SO_THAT_chi_doc_moi_moi_noi_khop_so_CT_la_MA_hai_cua_danh_sach():
    """⭐ Mong *(`TL-033`)*: `gd_ds` khớp mã **100%** `ma`, `gd` khớp mã **100%**
    `ma`; mẫu số > 0. Cửa `lenh-cho` cùng luật *(⛔ hồi quy — hôm nay `268 / 268`)*.

    ⛔ Chiều ĐỎ *(mã `363a441`, đo 02/10)*: `lenh-da-gan` `gd_ds` `ma` **0 /
    2.262**, `gd` **0 / 2.219** ⇒ ĐỎ."""
    from fls.api import xu_ly
    with noi_chi_doc(dsn_that()) as c:
        db = c.execute("SELECT current_database()").fetchone()[0]
        ro = c.execute("SHOW default_transaction_read_only").fetchone()[0]
        assert ro == "on", "⛔ kết nối sổ thật PHẢI chỉ đọc"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        do = {}
        for ten, ham in (("lenh-da-gan", xu_ly.lenh_da_gan),
                         ("lenh-cho", xu_ly.lenh_cho)):
            dem = Counter()
            for k, x, u in _phan_tu({"rows": _het_trang(ham, c, pv)}):
                m = canon_ref(x.get("ref_tho"))
                if m and canon_ref(u.get("doc_no")) == m:
                    dem[(k, "khop")] += 1
                    dem[(k, "ma")] += u["bac"] == "ma"
            do[ten] = dem
    for ten, dem in do.items():
        print(f"WO-032 v2 AC-12 · sổ thật ({db}) {ten}: " + " · ".join(
            f"{k} khớp số CT {dem[(k, 'khop')]} / bậc ma {dem[(k, 'ma')]}"
            for k in ("gd", "gd_ds") if dem[(k, "khop")]))
    assert do["lenh-da-gan"][("gd_ds", "khop")] > 0, "⛔ không đo được: 0 mối nối"
    assert do["lenh-da-gan"][("gd", "khop")] > 0, "⛔ không đo được: 0 lệnh"
    assert do["lenh-cho"][("gd", "khop")] > 0, "⛔ không đo được: lenh-cho 0"
    for ten, dem in do.items():
        for k in ("gd", "gd_ds"):
            assert dem[(k, "ma")] == dem[(k, "khop")], (ten, k, dict(dem))


# ═══ ③ quét nguồn — MỘT chỗ gắn `ma_canon` ═════════════════════════════════
def _cay(duong):
    with open(duong, encoding="utf-8") as f:
        return ast.parse(f.read(), duong)


def _cho_gan_ma_canon():
    """Mọi chỗ trong `fls/**/*.py` **đặt** khoá `ma_canon`: `x["ma_canon"] = …`
    · `x.setdefault("ma_canon", …)` · `{"ma_canon": …}` · `dict(ma_canon=…)`
    ⇒ `[(tệp, hàm bao, dòng)]`."""
    ra = []
    for goc, _d, tep in os.walk(GOC):
        for t in tep:
            if not t.endswith(".py"):
                continue
            p = os.path.join(goc, t)
            cay = _cay(p)
            cha = {}
            for n in ast.walk(cay):
                for c in ast.iter_child_nodes(n):
                    cha[c] = n

            def ham_bao(n):
                while n in cha:
                    n = cha[n]
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return n.name
                return None

            def la_khoa(n):
                return isinstance(n, ast.Constant) and n.value == "ma_canon"

            for n in ast.walk(cay):
                trung = False
                if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                    dich = n.targets if isinstance(n, ast.Assign) else [n.target]
                    trung = any(isinstance(d, ast.Subscript) and la_khoa(d.slice)
                                for d in dich)
                elif isinstance(n, ast.Call):
                    trung = (isinstance(n.func, ast.Attribute)
                             and n.func.attr in ("setdefault", "update")
                             and n.args and la_khoa(n.args[0])) or any(
                        k.arg == "ma_canon" for k in n.keywords)
                elif isinstance(n, ast.Dict):
                    trung = any(la_khoa(k) for k in n.keys if k is not None)
                if trung:
                    ra.append((os.path.relpath(p, GOC).replace("\\", "/"),
                               ham_bao(n), n.lineno))
    return ra


def _goi_trong(tep, ham):
    """Tên các hàm được gọi trong thân `ham` của `tep`, **theo thứ tự dòng**."""
    cay = _cay(os.path.join(GOC, tep))
    for n in ast.walk(cay):
        if isinstance(n, ast.FunctionDef) and n.name == ham:
            goi = [(c.lineno, c.func.attr if isinstance(c.func, ast.Attribute)
                    else getattr(c.func, "id", None))
                   for c in ast.walk(n) if isinstance(c, ast.Call)]
            return [t for _l, t in sorted(goi)]
    raise AssertionError(f"⛔ không đo được: {tep}::{ham} ⛔ có")


def test_AC12_MOT_cho_gan_ma_canon_va_HAI_cua_danh_sach_cung_di_qua_no():
    """⛔ Chiều ĐỎ: thêm `d["ma_canon"] = re.sub(…)` ở `xu_ly.lenh_da_gan` *(bản
    `canon_ref` thứ hai)* ⇒ **2** chỗ ⇒ ĐỎ; bỏ lời gọi `gan_ma_canon` khỏi
    `lenh_da_gan` ⇒ ĐỎ *(cùng lúc bài ① ② ĐỎ)*."""
    cho = _cho_gan_ma_canon()
    print(f"WO-032 v2 AC-12 · chỗ đặt khoá `ma_canon` trong fls/: {cho}")
    assert len(cho) == 1, f"⛔ mong MỘT chỗ gắn `ma_canon`, gặp {cho}"
    assert cho[0][:2] == ("repo/lenh_cho.py", "gan_ma_canon"), cho
    # hai cửa danh sách đi qua cùng hàm ấy, và **trước** `_gan_gd`
    da_gan = _goi_trong("api/xu_ly.py", "lenh_da_gan")
    assert "gan_ma_canon" in da_gan and "_gan_gd" in da_gan, da_gan
    assert da_gan.index("gan_ma_canon") < da_gan.index("_gan_gd"), da_gan
    assert "gan_ma_canon" in _goi_trong("repo/lenh_cho.py", "xep_ro")
    cho_ = _goi_trong("api/xu_ly.py", "lenh_cho")
    assert cho_.index("xep_ro") < cho_.index("_gan_gd"), cho_
