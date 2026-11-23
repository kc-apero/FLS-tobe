# -*- coding: utf-8 -*-
"""`WO-042 (c)` · `AC-10` — **một** tập ký tự trắng đi **đầu-cuối** qua cửa
HTTP thật trên **kho TEST**: rổ · `itl-candidates` *(SQL)* · cửa GHI cùng coi
một mã tiền tệ dính ký tự trắng biên là **một** mã.

⛔⛔ Lỗi gốc *(`KQ-041 F-2`)*: ba vế, ba tập — rổ `xep_ro` *(Python
`str.strip()` 29)* · ba bậc tiền + `tong_cung_tien_te` *(SQL `btrim` 4)* · cửa
ghi `ghep_lenh` *(Python `str.strip()` 29, ⛔ `U+FEFF`)*. Một lệnh có thể nằm ở
rổ này mà cửa ghi nói khác.

Ca `tests/web/ca_wo042.dung_ca_wo042` *(một lần nạp mới — ảnh PM hiệu lực của
máy thử là đúng bốn lệnh ấy)*:
  ① lệnh `A` *(VND, ⛔ mã, `X`)* ↔ dòng chưa nối `curr = NBSP + 'VND'` ⛔ mã
     khớp, đúng `X` ⇒ `itl-candidates` có dòng ấy **bậc `tien`**; và
     `tong_cung_tien_te` = số dòng chưa nối trong phạm vi mà
     `ma_tien_te(curr) == 'VND'` — **oracle Python** đếm, ⛔ một bản SQL
     *(`BG-040` yếu #4: phía mong là một bản SQL thì mã và bài cùng trôi)*.
  ② lệnh `B` *(`curr = BOM + 'VND'`, mã `cB`)* ↔ dòng VND mã `cB` ⇒ rổ `may`
     *(⛔ `nguoi` khác tiền tệ)*.
  ③ cửa GHI `POST /queue/{itl_id}/match` cặp `B` ⇒ `200` *(⛔ `KhacTienTe`)* —
     **ghi kho TEST**.

⛔ Chiều ĐỎ đã chạy trên mã khi nhận *(`fls/**` = `3c13ce3`)*: ghi trong `BG`.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.canon.tien_te import ma_tien_te
from fls.db.kho import dsn_test
from fls.repo.kho_sach import HINH_RUN_THAT
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo042 import BOM, NBSP, dung_ca_wo042
from tests.web.test_vong_f02_pg import V, _goi, _may

pytestmark = pytest.mark.pg


@pytest.fixture(scope="module")
def ca42():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo042(c)
    with _may() as m:
        yield ca, m


def test_AC10_1_dong_NBSP_VND_vao_BAC_TIEN_va_dem_cung_te_THEO_ma_tien_te(ca42):
    ca, m = ca42
    uv = goi_ok(m, f"/queue/lenh/{ca['lenh']['A']}/itl-candidates?limit=50")["data"]
    x = [u for u in uv["ung_vien"] if u["itl_id"] == ca["i"]["A"]]
    print(f"WO-042 AC-10 ① · A: {[(u['bac'], repr(u['curr'])) for u in uv['ung_vien'][:3]]}"
          f" · tong_cung_tien_te {uv['tong_cung_tien_te']}")
    assert x, "⛔ dòng NBSP+VND đúng số tiền ⛔ ở danh sách ứng viên"
    assert x[0]["bac"] == "tien", x[0]
    assert x[0]["curr"] == NBSP + "VND", "⛔ không đo được: kho đã gỡ NBSP"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        te = [r[0] for r in c.execute(
            "SELECT i.curr FROM fls_itl i WHERE i.run_id ~ %s"
            "   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)",
            (HINH_RUN_THAT.pattern,)).fetchall()]
    mong = sum(1 for t in te if ma_tien_te(t) == "VND")
    ngoai_4 = sum(1 for t in te if ma_tien_te(t) == "VND"
                  and t.strip(" \t\r\n").upper() != "VND")
    print(f"WO-042 AC-10 ① · oracle Python {mong} / {len(te)} dòng chưa nối; "
          f"trong đó luật SQL cũ (4 ký tự) bỏ sót {ngoai_4}")
    assert ngoai_4 > 0, "⛔ không đo được: kho TEST ⛔ có dòng biên ngoài 4 ký tự"
    assert uv["tong_cung_tien_te"] == mong, (uv["tong_cung_tien_te"], mong)


def test_AC10_2_lenh_BOM_VND_khop_ma_dong_VND_vao_RO_MAY(ca42):
    ca, m = ca42
    ro = goi_ok(m, "/queue/lenh-cho/ro")["data"]
    may = goi_ok(m, "/queue/lenh-cho?ro=may&limit=500")["data"]["rows"]
    nguoi = goi_ok(m, "/queue/lenh-cho?ro=nguoi&limit=500")["data"]["rows"]
    b = ca["lenh"]["B"]
    print(f"WO-042 AC-10 ② · /ro {ro} · B ở may {b in {r['pm_line_id'] for r in may}}")
    assert b in {r["pm_line_id"] for r in may}, "⛔ lệnh BOM+VND ⛔ ở rổ may"
    assert b not in {r["pm_line_id"] for r in nguoi}
    assert ro["nguoi_khac_tien_te"] == 0, ro


def test_AC10_3_cua_GHI_nhan_cap_BOM_VND_khong_KhacTienTe(ca42):
    """⚠ **Ghi kho TEST** *(một mối nối, `reason` mang `WO-042`)*."""
    ca, m = ca42
    ma, r = _goi(m, f"{V}/queue/{ca['i']['B']}/match", pt="POST",
                 than={"pm_line_ids": [ca["lenh"]["B"]],
                       "reason": "WO-042 AC-10 bai thu - kho TEST"})
    print(f"WO-042 AC-10 ③ · POST match B ⇒ {ma} {str(r)[:160]}")
    assert ma == 200, r
    assert [x["pm_line_id"] for x in r["data"]["moi_noi"]] == [ca["lenh"]["B"]]
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        assert c.execute("SELECT curr FROM fls_pm_line WHERE pm_line_id = %s",
                         (ca["lenh"]["B"],)).fetchone()[0] == BOM + "VND"
