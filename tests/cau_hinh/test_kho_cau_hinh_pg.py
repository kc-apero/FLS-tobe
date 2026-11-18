# -*- coding: utf-8 -*-
"""`C5` — kho config CHỈ-THÊM có phiên bản *(`fls/repo/cau_hinh_repo.py`, di trú `0027`)*
trên **PG THẬT**.

⛔⛔ Chép khuôn `fls_khai_cot` *(di trú `0016` + `fls/repo/khai_cot.py`)*: chỉ-thêm ·
   `phien_ban` · thời điểm `luc` do **MÁY** đặt · đủ-hoặc-không trong MỘT giao dịch ·
   ⛔ bản mặc định · lỗi *"nguồn lạ"* `BangLa` ≠ *"chưa khai"* `ChuaKhai` *(hai câu
   dẫn người dùng đi hai đường sửa khác nhau — `khai_cot.py` khối đầu tệp)*.

⭐ Nạp đọc **ảnh DT2/DT3** ở `tests/fixture/cau_hinh/` qua đường **TRUYỀN VÀO**
   *(AC-6b: ⛔ đọc tệp tĩnh đi cùng gói)*. Kho chỉ lưu khoá cần cho tuyến.

⚠ Kho `fls_test` **DÙNG CHUNG** giữa các bài, và bảng config là **chỉ-THÊM** *(trigger
   chặn `DELETE`/`TRUNCATE`)* ⇒ ⛔ dọn được giữa bài. Nên các bài đo **mức tăng** phiên
   bản so với mốc chụp ở ĐẦU bài *(⛔ hằng "phiên bản 1")*: kho mới dựng thì mốc = 0 ⇒
   lần nạp đầu là phiên bản **1** *(đúng AC-1)*, và luật *"⛔ ghi đè"* vẫn đo được.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import psycopg
import pytest

from fls.cau_hinh import fx
from fls.db.kho import dsn_test
from fls.repo import cau_hinh_repo as chr

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
CAU_HINH = GOC / "tests" / "fixture" / "cau_hinh"
ANH_IX_FX = CAU_HINH / "ix_fx.json"
ANH_ATL = CAU_HINH / "atl_cay.json"
ANH_MM = CAU_HINH / "mapping_master_cfg.json"

# ⭐ `thang_dau` của ẢNH thật — khai ở khuôn `ix_fx` *(cùng hằng với C1, ⛔ bản chép)*;
#   dòng `202306` đứng TRƯỚC nó ⇒ **lạc**.
THANG_DAU_IX_FX = 202401


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _max_phien(conn, bang: str) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT coalesce(max(phien_ban), 0) FROM fls_cau_hinh_ban "
                    "WHERE bang = %s", (bang,))
        return int(cur.fetchone()[0])


# ── C5-B1 · nạp `ix_fx.json` thật ⇒ phiên bản mới; đọc trả 37 dòng, lạc 202306 ───────
def test_C5_B1_nap_ix_fx_that_phien_ban_moi_va_doc_37_dong_lac_202306(conn):
    v0 = _max_phien(conn, fx.BANG)
    ban = chr.nap_ix_fx(conn, str(ANH_IX_FX), actor="ke.toan.thu",
                        thang_dau=THANG_DAU_IX_FX)
    assert ban.phien_ban == v0 + 1
    if v0 == 0:
        assert ban.phien_ban == 1, "⛔ kho mới ⇒ lần nạp đầu là phiên bản 1 (AC-1)"
    assert ban.bang == fx.BANG and ban.actor == "ke.toan.thu"
    # ⭐ `luc` do MÁY đặt — ⛔ người gọi truyền vào *(khuôn `khai_cot` ⓒ)*.
    assert ban.luc is not None

    b = chr.doc_fx(conn)
    assert len(b.ky) == 37, f"⛔ mong 37 dòng, đo {len(b.ky)}"
    assert [m for m in b.lac] == [202306], b.lac
    assert b.thieu == () and b.trung == (), (b.thieu, b.trung)


# ── C5-B2 · nạp lại cùng ảnh ⇒ phiên bản MỚI, checksum trùng ⇒ `khong_doi`, ⛔ đè ───
def test_C5_B2_nap_lai_cung_anh_phien_ban_moi_khong_doi_KHONG_de_ban_cu(conn):
    b1 = chr.nap_ix_fx(conn, str(ANH_IX_FX), actor="ai.do", thang_dau=THANG_DAU_IX_FX)
    assert b1.khong_doi is False or b1.phien_ban > 1  # lần đầu của phiên này có thể khác

    b2 = chr.nap_ix_fx(conn, str(ANH_IX_FX), actor="ai.do", thang_dau=THANG_DAU_IX_FX)
    assert b2.phien_ban == b1.phien_ban + 1, "⛔ nạp lại ⇒ phiên bản MỚI (chỉ-thêm)"
    assert b2.checksum == b1.checksum
    assert b2.khong_doi is True, "⛔ checksum trùng ⇒ khong_doi = true"

    # ⛔ ⛔ ghi đè bản cũ: cả hai phiên bản còn NGUYÊN trong kho.
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang = %s "
                    "AND phien_ban IN (%s, %s)", (fx.BANG, b1.phien_ban, b2.phien_ban))
        assert cur.fetchone()[0] == 2


def test_C5_doc_luon_tra_phien_ban_MOI_NHAT(conn):
    b1 = chr.nap_ix_fx(conn, str(ANH_IX_FX), actor="a", thang_dau=THANG_DAU_IX_FX)
    b2 = chr.nap_ix_fx(conn, str(ANH_IX_FX), actor="b", thang_dau=THANG_DAU_IX_FX)
    assert b2.phien_ban > b1.phien_ban
    assert chr.doc_fx.__module__  # smoke
    # đọc generic phải chỉ về bản mới nhất
    ban = chr._doc_ban(conn, fx.BANG)
    assert ban.phien_ban == b2.phien_ban and ban.actor == "b"


# ── AC-5 · kho RỖNG (chưa nạp) ⇒ `ChuaKhai` có TÊN, ≠ `BangLa` ───────────────────────
def test_AC5_chua_nap_thi_ChuaKhai_co_ten_KHONG_la_BangLa(conn):
    """Một `bang` HỢP LỆ mà ⛔ ai nạp ⇒ `ChuaKhai` *(409)*. ⛔ rơi về ảnh tĩnh,
    ⛔ trả bản mặc định *(khuôn `khai_cot` ⓓ)*.

    ⚠ `fls_test` dùng chung ⇒ `IX.FX`/`IX.HD` có thể đã có bản. Đo trên một `bang`
       HỢP LỆ **chưa dùng tới** trong bộ test: `IX.PER` *(pháp nhân — chưa bước nào
       nạp)*. Mẫu số `Đ3`: khẳng định nó RỖNG trước khi kết luận.
    """
    assert "IX.PER" in chr.BANG_HOP_LE
    assert _max_phien(conn, "IX.PER") == 0, "⛔ tiền đề: IX.PER chưa ai nạp"
    with pytest.raises(chr.ChuaKhai) as e:
        chr._doc_ban(conn, "IX.PER")
    assert e.value.ma == "FLS-CAUHINH-CHUA-KHAI"
    assert not isinstance(e.value, chr.BangLa)


def test_AC5_bang_LA_thi_BangLa_co_ten_KHONG_ChuaKhai(conn):
    """Một `bang` ⛔ trong danh mục config ⇒ `BangLa` *(404)* — câu KHÁC `ChuaKhai`.
    *"⛔ có nguồn ấy"* ≠ *"có nguồn, chưa ai khai"*."""
    with pytest.raises(chr.BangLa) as e:
        chr._doc_ban(conn, "IX.KHONG_CO_THAT")
    assert e.value.ma == "FLS-CAUHINH-BANG-LA"
    assert not isinstance(e.value, chr.ChuaKhai)
    # chiều ghi cũng chặn nguồn lạ TRƯỚC khi chạm kho.
    with pytest.raises(chr.BangLa):
        chr.nap(conn, "IX.KHONG_CO_THAT", [("k", 1)], nguon="x", actor="y")


# ── khuôn `khai_cot`: actor BẮT BUỘC, thời điểm do MÁY ─────────────────────────────
def test_actor_bat_buoc(conn):
    with pytest.raises(chr.LoiCauHinh):
        chr.nap(conn, fx.BANG, [("202401", {"USD": "1"})], nguon="x", actor="  ")


def test_du_hoac_khong_mot_giao_dich_khoa_trung_trong_mot_ban_BI_CHAN(conn):
    """`UNIQUE(ban_id, khoa)` — một khoá hai lần trong MỘT phiên bản là hai câu trả
    lời cho một câu hỏi *(cùng luật `fls_khai_cot` `(source_id, version, truong)`)*."""
    with pytest.raises((psycopg.errors.UniqueViolation, chr.LoiCauHinh)):
        chr.nap(conn, "IX.PER", [("A", 1), ("A", 2)], nguon="x", actor="z")


# ── AC-6b · HD + Mapping Master đọc từ kho; MM chỉ lưu khoá cần (⛔ bảng phụ `tho`) ──
def test_AC6b_nap_hd_va_doc_cay_74_nut_6_nhom(conn):
    chr.nap_ix_hd(conn, str(ANH_ATL), actor="ke.toan")
    cay = chr.doc_hd(conn)
    assert len(cay.nut) == 74
    assert cay.nhom == ("HDO", "HDH", "HDAP", "HDT", "HDC", "HDCI")
    assert len(cay.goc) == 37
    theo_ma = {n.ma: n for n in cay.nut}
    assert theo_ma["CAC"].cha == "OPC" and theo_ma["CAC"].cap == 2
    assert cay.con_cua("OPC") == ("CAC", "COS")


def test_AC6b_nap_mm_chi_luu_hd_code_KHONG_bang_phu_tho(conn):
    """AC-6b: ảnh MM gói mang bảng phụ `tho` *(84 hàng, 51 hàng có chuỗi ≥ 6 chữ số)*
    mà tuyến ⛔ đọc. Kho **chỉ** lưu khoá cần cho tuyến *(`hd_code`)* ⇒ ⛔ một ô nào
    của `tho` lọt vào `fls_cau_hinh_dong`."""
    anh = json.loads(ANH_MM.read_text(encoding="utf-8"))
    assert "phu" in anh and "tho" in anh["phu"], "⛔ tiền đề: ảnh MM có bảng phụ tho"

    ban = chr.nap_mapping_master(conn, str(ANH_MM), actor="ke.toan")
    mm = chr.doc_mm(conn)
    assert len(mm.ma) == 73
    assert "GI" in mm.ma and "NCF" not in mm.ma  # NCF chỉ có ở ATL
    assert mm.nguon == str(ANH_MM)

    # ⛔ KHÔNG lưu giá trị của bảng phụ `tho`: đếm số dòng của phiên bản vừa ghi =
    #   73 *(hd_code)*, ⛔ 73 + 84.
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_dong WHERE ban_id = "
                    "(SELECT ban_id FROM fls_cau_hinh_ban WHERE bang = %s AND "
                    "phien_ban = %s)", (chr.BANG_MM, ban.phien_ban))
        assert cur.fetchone()[0] == 73, "⛔ MM lưu ĐÚNG 73 hd_code, ⛔ bảng phụ tho"


def test_AC6b_hd_va_mm_la_HAI_bang_config_RIENG(conn):
    """Cây ATL *(`IX.HD`)* và Mapping Master *(`IX.HD · IX.ORG`)* phiên bản ĐỘC LẬP."""
    assert chr.BANG_HD == "IX.HD" and chr.BANG_MM == "IX.HD · IX.ORG"
    assert chr.BANG_HD in chr.BANG_HOP_LE and chr.BANG_MM in chr.BANG_HOP_LE
