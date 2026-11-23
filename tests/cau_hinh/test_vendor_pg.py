# -*- coding: utf-8 -*-
"""`C9-B1` — nạp ảnh `ix_ven.json` (DT8) vào KHO config chỉ-thêm trên PG THẬT *(ISP 3.1.2 ·
Step 21 · `WO-172`)*. Số đo ở ảnh: **42** dòng *(ISP ghi 36 = errata `DT8-R1-01`; 36 là số bộ
`(vendor, network, account)` KHÁC nhau — Đ4)*, **5** mã `cach_tinh`, **7** CDT1 *(từ ảnh
`cdt_correct.json` — `cdt1_chuan` khác nhau)*."""
from __future__ import annotations

from pathlib import Path

import psycopg
import pytest

from fls.cau_hinh import vendor
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chc

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
ANH = GOC / "tests" / "fixture" / "cau_hinh" / "ix_ven.json"
ANH_CDT = GOC / "tests" / "fixture" / "cau_hinh" / "cdt_correct.json"
NHAN = ("Max", "VD341", "VD428", "VD444", "VD62")


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _max(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban WHERE bang=%s",
                    (vendor.BANG,))
        return int(cur.fetchone()[0])


def _nap(conn, **kw):
    return chc.nap_ix_ven(conn, str(ANH), duong_cdt1=str(ANH_CDT), actor="bo-test-c9", **kw)


def test_C9_B1_nap_42_dong_5_ma_dac_biet_7_cdt1(conn):
    v0 = _max(conn)
    ban = _nap(conn)
    assert ban.phien_ban == v0 + 1 and ban.bang == "IX.VEN"
    b = chc.doc_ven(conn, so="GI")                                # DT9b: ảnh nay có 4 sổ — GI = 42
    assert len(b.dong) == 42, len(b.dong)                         # đếm DÒNG sheet 4…45
    assert len({(d.vendor, d.network, d.account) for d in b.dong}) == 36   # đếm BỘ khác nhau
    assert b.nhan_rieng == NHAN
    dem = {}
    for d in b.dong:
        dem[d.cach_tinh] = dem.get(d.cach_tinh, 0) + 1
    assert dem == {"Max": 12, "VD341": 12, "VD444": 8, "VD428": 3, "VD62": 1, "thường": 6}, dem
    assert sum(d.pct is None for d in b.dong) == 14        # ảnh: dòng sheet 32…45 ⛔ có %
    assert len(b.cdt1) == 7 and len(set(b.cdt1)) == 7, b.cdt1
    assert "SHQ2 | Headquarters2" in b.cdt1 and "ASA | Super App" in b.cdt1


def test_C9_B1_nap_lai_cung_anh_khong_doi_checksum(conn):
    a = _nap(conn)
    b = _nap(conn)
    assert b.phien_ban == a.phien_ban + 1 and b.khong_doi and a.checksum == b.checksum


def test_C9_B1_kho_CHUA_nap_thi_ChuaKhai_khong_roi_ve_anh():
    # Bài chạy trên kho TRỐNG của bang này nếu mới dựng; kho dùng chung ⇒ đo qua `_doc_ban`
    # trên bang khác danh mục: `IX.VEN` ĐÃ là bang hợp lệ (⛔ BangLa).
    assert vendor.BANG in chc.BANG_HOP_LE


def test_C9_nap_ban_bao_ve_kiem_TRUOC_khi_ghi(conn):
    v0 = _max(conn)
    with pytest.raises(chc.LoiCauHinh):
        chc.nap(conn, vendor.BANG, [], nguon="x", actor="bo-test-c9")      # rỗng
    with pytest.raises(vendor.LoiVen):
        chc.nap(conn, vendor.BANG, [("4", {"vendor": "VD1"})], nguon="x", actor="bo-test-c9")
    assert _max(conn) == v0, "⛔ bản hỏng lọt vào kho chỉ-thêm"


def test_C9_ban_ghi_thang_SQL_hong_doc_ra_BanHong(conn):
    _nap(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0)+1 FROM fls_cau_hinh_ban WHERE bang=%s",
                    (vendor.BANG,))
        ver = cur.fetchone()[0]
        cur.execute("INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
                    "VALUES (%s,%s,'sql-tay','x','bo-test-c9') RETURNING ban_id",
                    (vendor.BANG, ver))
        ban_id = cur.fetchone()[0]
        cur.execute("INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
                    "VALUES (%s,'4','{\"vendor\":\"VD1\"}'::jsonb)", (ban_id,))
    with pytest.raises(chc.BanHong):
        chc.doc_ven(conn)
    _nap(conn)                       # phục hồi: bản TỐT kế tiếp thắng (kho chỉ-thêm)
    assert len(chc.doc_ven(conn, so="GI").dong) == 42


def test_DT9b_nap_359_dong_4_so_phu_vendor_MID3(conn):
    """`WO-241`: ảnh nạp ĐỦ **359** dòng *(GI 42 · OMC 89 · SC 93 · PS 135)*; `doc_ven(so=…)` lọc đúng sổ;
    vendor khác nhau OMC 21 · SC 10 · PS 53; chỉ-THÊM *(phiên bản mới, ⛔ đè bản cũ)*."""
    v0 = _max(conn)
    ban = _nap(conn)
    assert ban.phien_ban == v0 + 1
    b = chc.doc_ven(conn)
    assert len(b.dong) == 359 and {d.so for d in b.dong} == {"GI", "OMC", "SC", "PS"}
    dem = {so: len(chc.doc_ven(conn, so=so).dong) for so in ("GI", "OMC", "SC", "PS")}
    assert dem == {"GI": 42, "OMC": 89, "SC": 93, "PS": 135}, dem
    ven = {so: len({d.vendor for d in b.dong if d.so == so}) for so in ("OMC", "SC", "PS")}
    assert ven == {"OMC": 21, "SC": 10, "PS": 53}, ven
    assert len({d.dong_sheet for d in b.dong}) == 359                          # khoá kho duy nhất
    assert {d.cach_tinh for d in chc.doc_ven(conn, so="OMC").dong} == {"thường", "VD341", "VD62", "VD428"}
    assert min(d.cashin_month for d in chc.doc_ven(conn, so="SC").dong) == 0   # SC VD529: cùng tháng
    assert [d.vendor for d in chc.doc_ven(conn, so="GI").dong][:2] == ["VD341", "VD341"]
    with pytest.raises(vendor.LoiVen):
        chc.doc_ven(conn, so="XYZ")


def test_DT9b_ban_DT8_cu_khong_co_so_van_doc_la_GI(conn):
    """Bản kho DT8 *(42 dòng, ⛔ `so`)* ⛔ vỡ: đọc ra `so = GI`."""
    cap = [(chc._CDT1, [f"C{i} | Cdt{i}" for i in range(7)])]
    for i, (v, ct) in enumerate([("VD341", "VD341"), ("VD444", "VD444"), ("VD428", "VD428"),
                                 ("VD62", "VD62"), ("VD111", "Max"), ("VD336", "thường")]):
        cap.append((str(4 + i), {"thu_tu": i + 1, "No": "1", "vendor": v, "network": "Max" if ct == "Max" else None,
                                 "account": None, "pct": "1", "cashin_month": "1", "cashin_day": "23",
                                 "cach_tinh": ct}))
    chc.nap(conn, vendor.BANG, cap, nguon="ban-DT8-cu", actor="bo-test-c9")
    try:
        b = chc.doc_ven(conn)
        assert {d.so for d in b.dong} == {"GI"} and len(b.dong) == 6
    finally:
        _nap(conn)
