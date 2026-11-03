"""`KQ-002 · F-4` — ghép TAY phải ghi ảnh lệnh chi vào `run_pm`, ⛔ vào `run_id`.

⛔⛔ **Đo được 01/10/2026 trên kho THẬT** *(chỉ đọc)*: `fls_pm_link` có
**`0/2.263`** dòng mang `run_pm`. Dòng duy nhất sinh SAU migration `0024`
*(cú UAT `link_id 163562`, `itl_id 27728`, `hinh='T'`, 01/10)* mang:

    run_id = 'NAP-2026-10-01-PM0BE98A9F'   ← ảnh LỆNH CHI
    run_pm = NULL

⇒ Đúng cái **hai nghĩa** mà `0024` dựng `run_pm` ra để xoá *(`run_id`: 2.262
dòng = lần NẠP, 1 dòng = ảnh PM)*, và nó trái ba chỗ khai:
  · `fls/db/migrations/0024_moi_noi_neo_anh_pm.sql` chú thích cột:
    *"NULL = mối nối sinh trước 2026-09-18"* — dòng này sinh 01/10.
  · `docs/ITL/02_BA/05_DATA_DICTIONARY_ERD.md:891` — *"`run_id` trỏ run GHÉP …
    thêm cột `run_pm`"*.
  · `tests/db/test_moi_noi_neo_anh_pm.py` đo *"dòng nào ĐÃ khai `run_pm` thì
    …"* — tập ấy **rỗng** (`Đ3`) nên bài xanh mà ⛔ đo gì.
Gốc: `fls/repo/ghi_tay.py:676` `INSERT … (…, run_id, lan)` với giá trị `run_pm`.
Đ1: `grep "INSERT INTO fls_pm_link" fls tools` = **2** chỗ *(`chay_nap.py:277`,
`ghi_tay.py:676`)*, ⛔ chỗ nào ghi cột `run_pm`.
"""
from __future__ import annotations

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_ghep_lenh_pg import (ACTOR, LY_DO, _dong_bank, _lenh,
                                          _run, conn)  # noqa: F401

pytestmark = pytest.mark.pg


# (KQ-002 F-4: `ghi_tay` ghi anh PM vao `run_id`, `run_pm` NULL)
# ✅ KQ-005 (fls-test 01/10): go dau xfail — WO-003 da va (ma 48fb68f), do lai do tren c1fb250 + xanh tren 4b2b2e8.
def test_ghep_TAY_ghi_anh_lenh_chi_vao_run_pm(conn):  # noqa: F811
    run = _run(conn)
    i = _dong_bank(conn, run, "5000.00", "USD")
    _lenh(conn, run, ("PMKQ2-1", "5000.00", "USD", "Approve",
                      "NB | Noi bo", "CAH | X"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, ["PMKQ2-1"],
                      actor=ACTOR, reason=LY_DO)
    anh = ra["run_id"]                     # ảnh PM hiệu lực mà phép ghép đã dùng
    assert anh, "⛔ không đo được: phép ghép ⛔ trả ảnh PM"
    run_pm, = conn.execute(
        "SELECT run_pm FROM fls_pm_link WHERE itl_id=%s", (i,)).fetchone()
    assert run_pm == anh, (
        f"⛔⛔ mối nối TAY ⛔ ghi `run_pm` (= {run_pm!r}, mong {anh!r}) — "
        "`run_id` lại mang hai nghĩa (migration 0024)")
