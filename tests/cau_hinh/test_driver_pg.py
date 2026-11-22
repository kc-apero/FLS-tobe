# -*- coding: utf-8 -*-
"""`C10-B1/B2` — nạp `IX.DRV` từ ảnh DT10 vào KHO config chỉ-thêm trên PG THẬT *(ISP 3.1.2 · Step 29
· `WO-295`)*; khứ hồi kho 238/238; 146 ô thiếu ném `DRV_THIEU` CÓ TÊN."""
from __future__ import annotations

import json
from pathlib import Path

import psycopg
import pytest

from fls.cau_hinh import driver as dv
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chc

pytestmark = pytest.mark.pg
GOC = Path(__file__).resolve().parents[2]
ANH_P = GOC / "tests/fixture/cau_hinh/ix_drv.json"
ANH = json.loads(ANH_P.read_text(encoding="utf-8"))


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _c(o):
    return o["chu"] if isinstance(o, dict) else o


def test_C10_B1_nap_khu_hoi_kho_238_238_khop_anh(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban WHERE bang='IX.DRV'")
        v0 = int(cur.fetchone()[0])
    ban = chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")
    assert ban.phien_ban == v0 + 1 and ban.bang == "IX.DRV"
    b = chc.doc_drv(conn)
    assert b.so_o_so() == 238                       # mẫu số ≠ 0 (Đ3)
    dem = 0
    for r in ANH["dong"]:
        for i in range(1, 13):
            v = r[f"m{i:02d}"]
            if v is not None:
                assert chc.driver_cua(conn, _c(r["driver"]), _c(r["cdt1"]), 202500 + i) == float(v)
                dem += 1
    assert dem == 238
    assert chc.driver_cua(conn, "NOEM", "SHQ1", 202503) == float(
        next(x for x in ANH["dong"] if _c(x["driver"]) == "NOEM" and _c(x["cdt1"]) == "SHQ1")["m03"])


def test_C10_B2_146_o_thieu_tu_kho_nem_DRV_THIEU(conn):
    chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")
    dem = 0
    for r in ANH["phu"]["o_thieu"]["dong"]:
        with pytest.raises(dv.DrvThieu) as e:
            chc.driver_cua(conn, _c(r["driver"]), _c(r["cdt1"]), int(_c(r["thang"])))
        assert e.value.ly == _c(r["ly_do"])
        dem += 1
    assert dem == 146
    with pytest.raises(dv.DrvThieu):
        chc.driver_cua(conn, "NOEM", "SHQ1", 202603)


def test_C10_AC4_nb_le_khu_hoi_kho(conn):
    chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")
    b = chc.doc_drv(conn)
    r = ANH["phu"]["nb_le"]["dong"][0]
    assert b.nb_le_cua(_c(r["from"]), _c(r["to"]), 202511) == 0.376 and len(b.nb_le) == 304


def test_C10_nap_chi_them_phien_ban_moi_va_khong_doi(conn):
    a = chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")
    b = chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")
    assert b.phien_ban == a.phien_ban + 1 and b.khong_doi is True


def test_C10_nap_ban_hong_bi_chan_truoc_khi_ghi(conn):
    cap = dv.dung_tu_anh(ANH)
    cap[0][1]["m02"] = 5.0                  # Σ7 ≠ 1 + ngoài [0,1]
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang='IX.DRV'")
        n0 = cur.fetchone()[0]
    with pytest.raises(dv.LoiDRV):
        chc.nap(conn, "IX.DRV", cap, nguon="bẩn", actor="bo-test-c10")
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang='IX.DRV'")
        assert cur.fetchone()[0] == n0


def test_C10_doc_chua_nap_la_ChuaKhai_hoac_ban_hong_la_BanHong(conn):
    with conn.cursor() as cur:        # SQL tay: bản hỏng (thiếu cột) — chỉ-thêm, bản mới nhất
        cur.execute("INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
                    "SELECT 'IX.DRV', coalesce(max(phien_ban),0)+1, 'sql-tay', 'x', 'bo-test-c10' "
                    "FROM fls_cau_hinh_ban WHERE bang='IX.DRV' RETURNING ban_id")
        bid = cur.fetchone()[0]
        cur.execute("INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) VALUES (%s,'NOEM|CVL','{}')",
                    (bid,))
    with pytest.raises(chc.BanHong):
        chc.doc_drv(conn)
    chc.nap_ix_drv(conn, str(ANH_P), actor="bo-test-c10")      # bản tốt kế tiếp thắng
    assert chc.doc_drv(conn).so_o_so() == 238
