# -*- coding: utf-8 -*-
"""`KQ-046` *(kiểm `BG-044` — `WO-042`)* · `F-1` `NHE` → `BA`: phép so tiền tệ
**thứ chín** — chiều **ngược** *(dòng tiền → ứng viên lệnh)* — vẫn ở luật cũ.

⭐ Cách tìm *(`fls-test` 05/10, `Đ1` — grep `fls/` mọi chỗ SQL đụng `curr`)*:
`BA-07` v3.11 §4g đòi **một** tập `TAP_TRANG_TIEN_TE` cho **mọi** phép so tiền
tệ; `WO-042` kiểm kê *"Python 6 · SQL 2 · JS 2"*. Dev làm đủ cả mười. Nhưng
`fls/repo/doc_bao_cao.py::_SQL_UNG_VIEN` *(hàm `ung_vien_pm` — cửa
`/so/{itl_id}/pm-candidates`, lằn *Theo dòng tiền* `F01` `_drawer_ghep`)* so
**ba** lần `upper(l.curr) = s.cur` *(`:309` · `:310` · `:317`)* — ⛔ `btrim`
nào cả. Vế dòng tiền `s.cur` đã là `ma_tien_te(...)` *(`WO-042` sửa `:377`)*,
vế lệnh thì ⛔ ⇒ một dòng lệnh `curr = NBSP + 'VND'` / `BOM + 'VND'` cùng đúng
số tiền với một dòng tiền `VND` ⇒ chiều thuận *(`itl-candidates`)*, rổ, và
**cửa GHI** `ghep_lenh` đều coi là cùng `VND` *(`BG-044` `AC-10` ③: `POST
/match` cặp `BOM+VND` ⇒ `200`)*, còn chiều ngược ⛔ hiện lệnh ấy **ở bậc nào
cả** *(điều kiện `WHERE … OR upper(l.curr) = s.cur` loại luôn)*.

Lỗi gốc có từ trước `WO-042` *(`0f6f054`)*; `WO-042` ⛔ sinh ra nó nhưng đổi
vế dòng tiền sang tập 30 mà ⛔ đổi vế lệnh ⇒ nay **hai** tập *(30 ⟷ 0)* trong
**một** câu SQL. Sổ thật hôm nay **0** ca *(`fls_pm_line.curr` mang ký tự của
tập ở mép **0 / 276.028** — `BG-044` `AC-11`, `KQ-046` đo lại)* ⇒ `NHE`.
Gửi **`BA`**: kiểm kê phạm vi `WO-042` / `BA-07` v3.11 bỏ sót chỗ này
*(⛔ lỗi Dev — Dev làm đúng danh sách được giao)*.

⛔ Ghi **kho TEST** *(fixture — `assert current_database()`)*.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.api import xu_ly
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.doc_bao_cao import ung_vien_pm
from fls.repo.man_ghep import ma_tien_te
from tests.web.ca_wo037 import _tien

pytestmark = pytest.mark.pg

#: `curr` của dòng LỆNH; dòng tiền đi cặp luôn là `'VND'` sạch
CA = ["VND", " vnd ", chr(0xA0) + "VND", chr(0xFEFF) + "VND", "VND" + chr(0x85),
      chr(0x3000) + "VND", chr(0x200B) + "VND"]


@pytest.fixture(scope="module")
def ca46():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        h = uuid.uuid4().hex[:8].upper()
        run = "NAP-2000-01-01-T46" + h[:6]
        c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                  " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        goc = random.randint(10_000, 89_999) * 1000
        nguon = "R | 123456789_VPB VND_K46" + h
        ca = []
        for k, x in enumerate(CA):
            tien = goc + 11 * k + 5
            itl = _tien(c, run, nguon, k + 1, f"{tien}.00", "VND", f"FT46Z{h}{k:02d}")
            ca.append({"x": x, "tien": tien, "itl": itl, "lenh": f"PK46{h[:5]}{k:02d}-1"})
        chen_dong_pm(c, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
            DongPM(3 + k, a["lenh"].split("-")[0], a["lenh"], D(f"{a['tien']}.00"),
                   a["x"], "Approve", None, "HD-K46", "C-K46", ref_tho=None)
            for k, a in enumerate(ca)])
        da = dict(c.execute("SELECT pm_line_id, curr FROM fls_pm_line WHERE run_id = %s",
                            (run,)).fetchall())
        assert [da[a["lenh"]] for a in ca] == CA, "⛔ kho đổi curr lúc nạp — ca vô nghĩa"
    return ca


def _do(ca):
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        ra = []
        for a in ca:
            r = ung_vien_pm(c, pv, a["itl"], n=200)
            assert r is not None, f"⛔ không đo được: itl {a['itl']} ngoài phạm vi"
            x = [u for u in r["ung_vien"] if u["pm_line_id"] == a["lenh"]]
            ra.append((a["x"], bool(x) and x[0]["bac"] == "tien",
                       ma_tien_te(a["x"]) == "VND"))
    return ra


def test_CANH_chieu_nguoc_ca_thuong_vao_BAC_TIEN(ca46):
    """Mỏ neo xanh: `'VND'` vào bậc `tien`; `U+200B` *(ngoài tập)* ⛔ vào."""
    ra = {x: (co, m) for x, co, m in _do(ca46)}
    print(f"KQ-046 F-1 mỏ neo · {[(repr(x), v) for x, v in ra.items()]}")
    assert ra["VND"] == (True, True), ra
    assert ra[chr(0x200B) + "VND"] == (False, False), ra


@pytest.mark.xfail(strict=True, reason="KQ-046 F-1 (NHE → BA): doc_bao_cao."
                   "_SQL_UNG_VIEN so upper(l.curr) = s.cur — vế lệnh ⛔ btrim "
                   "TAP_TRANG_TIEN_TE (BA-07 v3.11) ⇒ chiều ngược ⛔ thấy lệnh "
                   "mà cửa ghi nhận")
def test_F1_chieu_nguoc_ung_vien_pm_BANG_ma_tien_te(ca46):
    ra = _do(ca46)
    lech = [(repr(x), co, m) for x, co, m in ra if co != m]
    print(f"KQ-046 F-1 · {[(repr(x), co, m) for x, co, m in ra]}")
    assert sum(1 for _, _, m in ra if m) >= 5, "⛔ không đo được: oracle ⛔ coi ca biên là VND"
    assert not lech, f"⛔ chiều ngược (SQL upper trần) ≠ ma_tien_te: {lech}"
