# -*- coding: utf-8 -*-
"""`C6` — `IX.PER`: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ *(ISP 3.1.2 · Step 17
· `WO-152` · AP §3.2.1 IX.PER · §3.2.4 · D4)*.

⛔ `ky_cua(ngày)` lấy năm CỦA CHÍNH NGÀY — AS-IS ép 2025 *(AP §3.2.4)*. Ngày đầu cột và luật
   ghi nhận là **config trong KHO** *(`0027`)*, ⛔ gõ cứng ở mã: bài NẠP ngày đầu
   `2024-10-21` *(ISP)* — số ấy là *dữ liệu của bài*, mã ⛔ biết nó.
"""
from __future__ import annotations

from datetime import date

import psycopg
import pytest

from fls.cau_hinh import ky
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chc

NGUON = "bai-test-c6:ISP-3.1.2-Step17"


# ── AC-1 · C6-B1 ─────────────────────────────────────────────────────────────
def test_C6_B1_ky_cua_2026_11_05_la_Y2026_H2_Q4_M11_KHONG_ep_2025():
    k = ky.ky_cua(date(2026, 11, 5))
    assert (k.nam, k.nua, k.quy, k.thang) == (2026, 2, 4, 11), k
    assert (k.nhan_nam, k.nhan_nua, k.nhan_quy, k.nhan_thang) == (
        "Y2026", "H2", "Q4", "M11"), k


@pytest.mark.parametrize("ngay,mong", [
    (date(2026, 1, 1), (2026, 1, 1, 1)), (date(2026, 3, 31), (2026, 1, 1, 3)),
    (date(2026, 4, 1), (2026, 1, 2, 4)), (date(2026, 6, 30), (2026, 1, 2, 6)),
    (date(2026, 7, 1), (2026, 2, 3, 7)), (date(2026, 12, 31), (2026, 2, 4, 12)),
    # C6-R1-01: biên Q3/Q4 (30/09 ↔ 01/10) và 29/02 năm nhuận — đột biến M3, M4 của R1
    (date(2026, 9, 30), (2026, 2, 3, 9)), (date(2026, 10, 1), (2026, 2, 4, 10)),
    (date(2024, 2, 29), (2024, 1, 1, 2)),
])
def test_C6_ky_cua_ranh_gioi_nua_va_quy(ngay, mong):
    k = ky.ky_cua(ngay)
    assert (k.nam, k.nua, k.quy, k.thang) == (mong[0], mong[1], mong[2], mong[3]), k


# ── AC-2 · C6-B2 ─────────────────────────────────────────────────────────────
def test_C6_B2_ky_cua_2024_12_31_la_Y2024_nam_cua_CHINH_du_lieu():
    k = ky.ky_cua(date(2024, 12, 31))
    assert (k.nhan_nam, k.nhan_nua, k.nhan_quy, k.nhan_thang) == (
        "Y2024", "H2", "Q4", "M12"), k


# ── AC-3 · C6-B3 ─────────────────────────────────────────────────────────────
def test_C6_B3_luat_B_chia_deu_bi_tu_choi_co_ten_LUAT_CHUA_KY():
    with pytest.raises(ky.LoiKy) as e:
        ky.chon_luat("B")
    assert e.value.ma == "LUAT_CHUA_KY" == ky.LUAT_CHUA_KY, e.value.ma
    with pytest.raises(ky.LoiKy) as e2:
        ky.ngay_ghi_nhan("B", date(2026, 3, 15), date(2026, 5, 20))
    assert e2.value.ma == "LUAT_CHUA_KY"


def test_C6_B3_chi_luat_A_chay_don_ngay_1_thang_PL_start():
    assert ky.chon_luat("A") == "A"
    assert ky.ngay_ghi_nhan("A", date(2026, 3, 15), date(2026, 5, 20)) == date(2026, 3, 1)
    # ⛔ PL end ⛔ ảnh hưởng luật A — dồn hết về tháng PL start.
    assert ky.ngay_ghi_nhan("A", date(2026, 3, 15), date(2027, 1, 1)) == date(2026, 3, 1)


def test_C6_luat_la_thi_LoiKy_PER_HONG_khong_im_lang_rơi_ve_A():
    with pytest.raises(ky.LoiKy) as e:
        ky.chon_luat("Z")
    assert e.value.ma == "PER_HONG"


# ── AC-4 · lõi kiểm bản config ───────────────────────────────────────────────
def test_C6_kiem_doc_ngay_dau_va_luat_tu_dong_config_KHONG_tu_ma():
    lich = ky.kiem({"ngay_dau": {"ngay": "2031-02-03"}, "luat": {"ma": "A"}},
                   nguon=NGUON)
    assert lich.ngay_dau == date(2031, 2, 3) and lich.luat == "A", lich
    assert lich.nguon == NGUON


@pytest.mark.parametrize("dong", [
    {"luat": {"ma": "A"}},                                       # thiếu ngày đầu
    {"ngay_dau": {"ngay": "2024-10-21"}},                        # thiếu luật
    {"ngay_dau": {"ngay": "21/10/2024"}, "luat": {"ma": "A"}},   # sai khuôn ngày
    {"ngay_dau": {"ngay": "2024-02-30"}, "luat": {"ma": "A"}},   # ngày ⛔ có thật
    {"ngay_dau": "2024-10-21", "luat": {"ma": "A"}},             # sai hình
])
def test_C6_kiem_ban_hong_thi_LoiKy_PER_HONG(dong):
    with pytest.raises(ky.LoiKy) as e:
        ky.kiem(dong, nguon=NGUON)
    assert e.value.ma == "PER_HONG", e.value


def test_C6_kiem_luat_B_trong_ban_thi_LUAT_CHUA_KY():
    with pytest.raises(ky.LoiKy) as e:
        ky.kiem({"ngay_dau": {"ngay": "2024-10-21"}, "luat": {"ma": "B"}}, nguon=NGUON)
    assert e.value.ma == "LUAT_CHUA_KY"


# ── AC-4 · kho THẬT (0027 — ⛔ di trú mới) ───────────────────────────────────
@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _dem(c) -> int:
    with c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang='IX.PER'")
        return int(cur.fetchone()[0])


@pytest.mark.pg
def test_C6_B4_nap_roi_doc_ngay_dau_luat_A_tu_KHO(conn):
    truoc = _dem(conn)
    b = chc.nap_ix_per(conn, actor="bo-test-c6", ngay_dau="2024-10-21",
                       luat="A", nguon=NGUON)
    assert b.bang == "IX.PER" == ky.BANG and _dem(conn) == truoc + 1
    lich = chc.doc_per(conn)
    assert lich.ngay_dau == date(2024, 10, 21) and lich.luat == "A", lich
    assert lich.nguon == NGUON


@pytest.mark.pg
def test_C6_nap_TU_CHOI_luat_B_va_ngay_hong_KHONG_ghi_gi(conn):
    truoc = _dem(conn)
    with pytest.raises(ky.LoiKy) as e:
        chc.nap_ix_per(conn, actor="bo-test-c6", ngay_dau="2024-10-21",
                       luat="B", nguon=NGUON)
    assert e.value.ma == "LUAT_CHUA_KY"
    with pytest.raises(ky.LoiKy):
        chc.nap_ix_per(conn, actor="bo-test-c6", ngay_dau="khong-phai-ngay",
                       luat="A", nguon=NGUON)
    assert _dem(conn) == truoc, "⛔ nạp bị từ chối mà kho vẫn đổi"


@pytest.mark.pg
def test_C6_doc_per_ban_moi_nhat_thang_va_BanHong_khi_ban_bay(conn, monkeypatch):
    chc.nap_ix_per(conn, actor="bo-test-c6", ngay_dau="2024-10-20", luat="A", nguon=NGUON)
    chc.nap_ix_per(conn, actor="bo-test-c6", ngay_dau="2024-10-21", luat="A", nguon=NGUON)
    assert chc.doc_per(conn).ngay_dau == date(2024, 10, 21)
    ban = chc._doc_ban(conn, "IX.PER")
    bay = chc.BanCauHinh(**{**ban.__dict__, "dong": (("luat", {"ma": "A"}),)})
    monkeypatch.setattr(chc, "_doc_ban", lambda _c, _b: bay)
    with pytest.raises(chc.BanHong):
        chc.doc_per(conn)
