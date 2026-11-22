# -*- coding: utf-8 -*-
"""`C11-B1` — nạp `IX.ALR` từ ảnh Mapping Master DT3 vào KHO config chỉ-thêm trên PG THẬT
*(ISP 3.1.2 · Step 25 · `WO-180`)*.

⭐ Nguồn là ẢNH DT3 `mapping_master_cfg.json` *(đường TRUYỀN VÀO)*: bảng `fls_mapping_master`
   của cụm đo **0 dòng** *(Đ3 — bảng ấy chỉ có dữ liệu khi có lần nạp Sheets; ⛔ xanh trên rỗng)*.
Số đo trên ảnh *(mỗi số một nhãn — Đ4)*: **21** mã có `method_cfa2` *(+ 2 mã có `need` mà RỖNG method)*;
mong **17** HD có luật = 4 `H1000 Ledger` + 8 `By GI` + 5 `By NOEM`; 4 mã `X Ledger` ngoài luật."""
from __future__ import annotations

from pathlib import Path

import psycopg
import pytest

from fls.cau_hinh import luat_pb as lp
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chc

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
ANH_MM = GOC / "tests" / "fixture" / "cau_hinh" / "mapping_master_cfg.json"


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _max(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban WHERE bang=%s",
                    (lp.BANG,))
        return int(cur.fetchone()[0])


def _nap(conn, **kw):
    kw.setdefault("tu_ky", 202501)
    return chc.nap_ix_alr(conn, str(ANH_MM), actor="bo-test-c11", **kw)


def test_C11_B1_nap_17_luat_4_8_5_H1000_khong_qua_allocate_100pct_bat_false(conn):
    v0 = _max(conn)
    ban = _nap(conn)
    assert ban.phien_ban == v0 + 1 and ban.bang == "IX.ALR"
    b = chc.doc_alr(conn)
    assert len(b.luat) == 17, len(b.luat)                    # đếm HD CÓ LUẬT (⛔ 21 mã có method)
    dem = {}
    for x in b.luat:
        dem[x.phuong_phap] = dem.get(x.phuong_phap, 0) + 1
    assert dem == {lp.H1000: 4, lp.BY_GI: 8, lp.BY_NOEM: 5}, dem
    h = [x for x in b.luat if x.phuong_phap == lp.H1000]
    assert len(h) == 4 and all(x.khong_qua_allocate for x in h)                     # Q3
    assert not any(x.khong_qua_allocate for x in b.luat if x.phuong_phap != lp.H1000)
    assert len(b.luat) > 0 and all(x.bat is False for x in b.luat)                  # D2 100%
    assert {x.hd for x in h} == {"NIS", "INT", "PIT", "COM"}, sorted(x.hd for x in h)


def test_C11_B2_B3_tren_kho_THAT_OFR_cua_CAH_va_by_GI_driver_PE(conn):
    _nap(conn)
    b = chc.doc_alr(conn)
    assert b.luat_cua("OFR", 202503, cdt1="CAH").phuong_phap is None
    assert b.luat_cua("OFR", 202503, cdt1="SHQ2").phuong_phap == lp.BY_NOEM
    assert b.luat_cua("LC", 202503).driver == "PE"
    assert b.luat_cua("LC", 202412) is None                  # trước `tu_ky` khai ở lần nạp
    assert b.luat_cua("GI", 202503) is None                  # 4 mã `X Ledger` ngoài luật


def test_C11_nap_lai_cung_anh_khong_doi_checksum_va_phien_ban_chi_them(conn):
    a = _nap(conn)
    b = _nap(conn)
    assert b.phien_ban == a.phien_ban + 1 and b.khong_doi and a.checksum == b.checksum
    c = _nap(conn, tu_ky=202507)                             # tu_ky khác ⇒ nội dung khác
    assert c.khong_doi is False and c.checksum != b.checksum


def test_C11_nap_tu_ky_la_gia_tri_CAU_HINH_phai_hop_le(conn):
    v0 = _max(conn)
    for bad in (None, 202513, "202501", 1):
        with pytest.raises(lp.LoiLuatPB):
            _nap(conn, tu_ky=bad)
    assert _max(conn) == v0


def test_C11_nap_ban_bao_ve_kiem_TRUOC_khi_ghi(conn):
    v0 = _max(conn)
    with pytest.raises(chc.LoiCauHinh):
        chc.nap(conn, lp.BANG, [], nguon="x", actor="bo-test-c11")                 # rỗng
    with pytest.raises(lp.LoiLuatPB):                                              # D2: bat=True
        chc.nap(conn, lp.BANG, [("G00@202501", {"hd": "G00", "tu_ky": 202501,
                "nhan_mm": "By GI", "bat": True, "ngoai_le": []})],
                nguon="x", actor="bo-test-c11")
    with pytest.raises(lp.LoiLuatPB):                                              # khoá lệch giá trị
        chc.nap(conn, lp.BANG, [("G00@202507", {"hd": "G00", "tu_ky": 202501,
                "nhan_mm": "By GI", "bat": False, "ngoai_le": []})],
                nguon="x", actor="bo-test-c11")
    assert _max(conn) == v0, "⛔ bản hỏng lọt vào kho chỉ-thêm"


def test_C11_ban_ghi_thang_SQL_hong_doc_ra_BanHong_CO_TEN(conn):
    _nap(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban),0)+1 FROM fls_cau_hinh_ban WHERE bang=%s",
                    (lp.BANG,))
        ver = cur.fetchone()[0]
        cur.execute("INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
                    "VALUES (%s,%s,'sql-tay','x','bo-test-c11') RETURNING ban_id",
                    (lp.BANG, ver))
        ban_id = cur.fetchone()[0]
        cur.execute("INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
                    "VALUES (%s,'G00@202501','{\"bat\": true}'::jsonb)", (ban_id,))
    with pytest.raises(chc.BanHong) as e:
        chc.doc_alr(conn)
    assert e.value.ma == "FLS-CAUHINH-BAN-HONG"
    _nap(conn)                       # phục hồi: bản TỐT kế tiếp thắng (kho chỉ-thêm)
    assert len(chc.doc_alr(conn).luat) == 17


def test_C11_R1_01_hieu_luc_TICH_LUY_qua_hai_lan_nap_202501_roi_202507(conn):
    """`C11-R1-01` — kịch bản R1: nạp `tu_ky=202501` rồi `202507` ⇒ đọc theo KỲ, ⛔ chỉ bản mới."""
    _nap(conn, tu_ky=202501)
    _nap(conn, tu_ky=202507)
    b = chc.doc_alr(conn)
    assert {x.tu_ky for x in b.luat} == {202501, 202507}, "⛔ tích luỹ: cả hai mốc phải còn"
    assert len(b.luat) == 34, len(b.luat)                    # 17 HD × 2 mốc (đếm dòng luật)
    cu = b.luat_cua("LC", 202503)
    assert cu is not None and cu.tu_ky == 202501 and cu.phuong_phap == lp.BY_GI
    assert b.luat_cua("LC", 202508).tu_ky == 202507          # mới nhất có tu_ky ≤ kỳ
    assert b.luat_cua("LC", 202412) is None
    assert b.luat_cua("OFR", 202503, cdt1="CAH").tu_ky == 202501
    _nap(conn, tu_ky=202507)                                 # nạp lại mốc cũ ⇒ ⛔ nhân đôi
    assert len(chc.doc_alr(conn).luat) == 34


# ── Vòng sửa R1 `H12` *(`KQ-293`)* — bật cờ 2025 CÓ KÝ qua KHO *(phiên bản MỚI, ⛔ sửa bản cũ)* ──────────
#   ⚠ Kho config TÍCH LUỸ *(`C11-R1-01`)* ⇒ một bản bật cờ đã COMMIT sẽ làm mọi bài C11 chạy sau thấy `bat=True`
#   *(bài `…_100pct_bat_false`)*. Bài ở đây chạy trong MỘT giao dịch rồi ROLLBACK *(`nap` lồng ⇒ savepoint)*.
TEP_KY = GOC / "tests" / "fixture" / "cau_hinh" / "ix_alr_2025_bat.json"


@pytest.fixture()
def conn_lui():
    with psycopg.connect(dsn_test()) as c:          # ⛔ autocommit ⇒ cuối bài rollback
        yield c
        c.rollback()


def test_H12_R1_ky_bat_2025__phien_ban_MOI_actor_nguoi_ky_ban_cu_nguyen(conn_lui):
    c = conn_lui
    _nap(c, tu_ky=202501)
    truoc = chc._doc_ban(c, lp.BANG)
    ban = chc.ky_bat_ix_alr(c, str(TEP_KY), actor="KhanhCQ")
    assert ban.phien_ban == truoc.phien_ban + 1 and ban.actor == "KhanhCQ" and ban.nguon.startswith("ky:")
    with c.cursor() as cur:                                      # bản cũ NGUYÊN *(chỉ-thêm)*
        cur.execute("SELECT count(*) FROM fls_cau_hinh_dong d JOIN fls_cau_hinh_ban b USING (ban_id) "
                    "WHERE b.bang = %s AND b.phien_ban = %s", (lp.BANG, truoc.phien_ban))
        assert cur.fetchone()[0] == len(truoc.dong) >= 17          # kho tích luỹ: ≥ 17 (mốc khác của bài C11)
    b = chc.doc_alr(c)
    assert sum(1 for x in b.luat if x.bat) == 13 and {x.nguoi_ky for x in b.luat if x.bat} == {"KhanhCQ"}
    assert b.luat_cua("LC", 202501).bat is False and b.luat_cua("LC", 202502).bat is True
    assert b.luat_cua("OFR", 202503, cdt1="CAH").phuong_phap is None
    assert b.luat_cua("REC", 202601).bat is False
    assert not any(x.bat for x in b.luat if x.phuong_phap == lp.H1000)
    _nap(c, tu_ky=202501)                     # nạp lại MM sau ký ⇒ chữ ký ⛔ mất — kể cả dòng CÙNG khoá `HCC@202501`
    b2 = chc.doc_alr(c)
    assert b2.luat_cua("LC", 202502).bat is True and b2.luat_cua("HCC", 202501).bat is True
    assert b2.luat_cua("HCC", 202501).nguoi_ky == "KhanhCQ" and sum(1 for x in b2.luat if x.bat) == 13


@pytest.mark.parametrize("actor", ["", "nguoi-khac", "KhanhCQ@x.vn"])
def test_H12_R1_ky_bat__actor_phai_DUNG_nguoi_ky(conn_lui, actor):
    c = conn_lui
    _nap(c, tu_ky=202501)
    v0 = _max(c)
    with pytest.raises(chc.LoiCauHinh):
        chc.ky_bat_ix_alr(c, str(TEP_KY), actor=actor)
    assert _max(c) == v0

