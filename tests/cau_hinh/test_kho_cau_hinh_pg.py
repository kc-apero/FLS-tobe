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
from datetime import datetime, timezone
from pathlib import Path

import psycopg
import pytest

from fls.cau_hinh import fx, hd
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


BANG_MAU_CHUA_NAP = "IX.MAU_CHUA_NAP"   # `bang` GIẢ — ⛔ bước nào nạp (C10 đã dùng hết 11 tên thật)


# ── AC-5 · kho RỖNG (chưa nạp) ⇒ `ChuaKhai` có TÊN, ≠ `BangLa` ───────────────────────
def test_AC5_chua_nap_thi_ChuaKhai_co_ten_KHONG_la_BangLa(conn, monkeypatch):
    """Một `bang` HỢP LỆ mà ⛔ ai nạp ⇒ `ChuaKhai` *(409)*. ⛔ rơi về ảnh tĩnh,
    ⛔ trả bản mặc định *(khuôn `khai_cot` ⓓ)*.

    ⚠ `fls_test` dùng chung ⇒ `IX.FX`/`IX.HD` có thể đã có bản. Đo trên một `bang`
       HỢP LỆ **chưa dùng tới** trong bộ test: `IX.DRV` *(chưa bước nào nạp)*.
       ⛔ `IX.DRV` ⛔ ai được GHI ở bộ này *(C9-R1-01: bài khác nạp vào đây thì tiền đề
       dưới đỏ theo THỨ TỰ chạy)* — `test_C5R1_05` dùng `IX.ALR`. `IX.PER`
       từng là mẫu này — `C6` *(WO-152)* nạp nó nên đổi sang `IX.DRV`. Mẫu số `Đ3`:
       khẳng định nó RỖNG trước khi kết luận.
    """
    # ⭐ `C10` (`WO-295`) nạp `IX.DRV` ⇒ CẢ 11 `bang` hợp lệ đều đã có người nạp *(`IX.TMP`: C13)*.
    #   ⇒ mẫu là một `bang` GIẢ thêm vào danh mục bằng `monkeypatch` — ⛔ tên thật nào cũng sẽ có
    #   bản; kho ⛔ có `CHECK` miền `bang` (di trú 0027) nên hỏi nó trả 0 dòng thật.
    monkeypatch.setattr(chr, "BANG_HOP_LE", chr.BANG_HOP_LE | {BANG_MAU_CHUA_NAP})
    assert BANG_MAU_CHUA_NAP in chr.BANG_HOP_LE
    assert _max_phien(conn, BANG_MAU_CHUA_NAP) == 0, "⛔ tiền đề: bảng mẫu chưa ai nạp"
    with pytest.raises(chr.ChuaKhai) as e:
        chr._doc_ban(conn, BANG_MAU_CHUA_NAP)
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


# ══ Vòng sửa sau R1 (KQ-144) ══════════════════════════════════════════════════════
#
# Bốn NÊN SỬA + hai GHI NHẬN của `KQ-144` *(sổ: docs/ITL/04_Test/review/
# SO_PHAT_HIEN_ISP-3.1_C5.md)*. Mỗi bài GHI đột biến R1 nó giết *(Đ5: cổng mới được
# chứng minh ĐỎ — phá nguồn, chạy, xem cắn, trả nguyên)*.
def _dem(conn, bang: str) -> tuple[int, int]:
    """`(#ban, #dong)` của một `bang` — đo MỨC, ⛔ hằng *(kho dùng chung, chỉ-thêm)*."""
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_cau_hinh_ban WHERE bang = %s", (bang,))
        nb = int(cur.fetchone()[0])
        cur.execute("SELECT count(*) FROM fls_cau_hinh_dong d JOIN fls_cau_hinh_ban b "
                    "ON b.ban_id = d.ban_id WHERE b.bang = %s", (bang,))
        nd = int(cur.fetchone()[0])
    return nb, nd


# ── C5-R1-02 · MM canh NỘI DUNG `gia_tri` *(tập khoá)*, ⛔ chỉ đếm hàng ────────────
def test_C5R1_02_MM_gia_tri_DUNG_tap_khoa_hd_code_thu_tu_KHONG_bang_phu_tho(conn):
    """Giết R1-M8′ *(ghi thêm `"tho": anh["phu"]["tho"]` vào MỖI `gia_tri` — vẫn 73
    hàng ⇒ bài đếm hàng SỐNG)*. AC-6b: kho **chỉ** lưu khoá cần cho tuyến ⇒ tập khoá
    của mỗi `gia_tri` phải ĐÚNG `{hd_code, thu_tu}`, và `gia_tri::text` ⛔ mang `tho`.
    `Đ3`: 73 hàng *(tập ⛔ rỗng)* rồi mới kết luận."""
    anh = json.loads(ANH_MM.read_text(encoding="utf-8"))
    assert "tho" in anh.get("phu", {}), "⛔ tiền đề: ảnh MM có bảng phụ tho"
    ban = chr.nap_mapping_master(conn, str(ANH_MM), actor="ke.toan")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT khoa, gia_tri, gia_tri::text FROM fls_cau_hinh_dong WHERE ban_id = "
            "(SELECT ban_id FROM fls_cau_hinh_ban WHERE bang = %s AND phien_ban = %s)",
            (chr.BANG_MM, ban.phien_ban))
        hang = cur.fetchall()
    assert len(hang) == 73, f"⛔ MM lưu ĐÚNG 73 hd_code, đo {len(hang)}"
    for khoa, gt, gt_text in hang:
        assert set(gt) == {"hd_code", "thu_tu"}, (khoa, sorted(gt))
        assert "tho" not in gt_text, (khoa, gt_text)


# ── C5-R1-03 · "đủ-hoặc-không" ĐẾM hai bảng trước/sau nạp HỎNG giữa chừng ──────────
def test_C5R1_03_du_hoac_khong_DEM_hai_bang_quanh_nap_hong_giua_chung(conn, monkeypatch):
    """Giết R1-M7 *(`with conn.transaction()` → `if True:` trên kết nối autocommit ⇒
    bản DỞ — một `fls_cau_hinh_ban`, 0 `_dong` — thành bản MỚI NHẤT)*. Nạp một `cap`
    QUA được phép kiểm nội dung nhưng NỔ khi ghi dòng *(`gia_tri` chứa `set` ⛔
    serialize ⇒ `json.dumps` NÉM `TypeError` SAU khi `ban` đã INSERT)* ⇒ `(ban, dong)`
    trước = sau. `Đ5`: ⛔ chỉ `raises`, mà ĐẾM hai bảng."""
    # ⭐ `C10`: `IX.DRV` nay có bản thật ⇒ đếm trên `bang` mẫu GIẢ *(nạp HỎNG ⇒ giữ rỗng)*.
    bang = BANG_MAU_CHUA_NAP
    monkeypatch.setattr(chr, "BANG_HOP_LE", chr.BANG_HOP_LE | {bang})
    truoc = _dem(conn, bang)
    with pytest.raises(TypeError):
        chr.nap(conn, bang, [("A", {"ok": 1}), ("B", {"xau": {1, 2}})],
                nguon="x", actor="z")
    assert _dem(conn, bang) == truoc, (
        f"⛔ nạp hỏng giữa chừng để lại bản DỞ: trước {truoc}, sau {_dem(conn, bang)}")


# ── C5-R1-04 · `nap` công khai KIỂM nội dung TRƯỚC khi ghi *(kho chỉ-thêm ⛔ lùi)* ──
def test_C5R1_04_nap_TU_CHOI_ban_FX_RONG_truoc_khi_ghi(conn):
    """Kho chỉ-thêm ⛔ có đường lùi ⇒ một bản RỖNG thành bản mới nhất ⛔ xoá được.
    `nap(IX.FX, [])` ⇒ lỗi CÓ TÊN *(khuôn ⓑ)*, và ⛔ ghi phiên bản mới."""
    v0 = _max_phien(conn, fx.BANG)
    with pytest.raises((chr.LoiCauHinh, fx.LoiFX)):
        chr.nap(conn, fx.BANG, [], nguon="x", actor="z")
    assert _max_phien(conn, fx.BANG) == v0, "⛔ bản rỗng ⇒ KHÔNG ghi phiên bản mới"


def test_C5R1_04_nap_TU_CHOI_hd_ban_BAN_truoc_khi_ghi(conn):
    """Ảnh HD thiếu trường *(chỉ `ten`)* ⇒ `nap` NỔ `LoiHD` CÓ TÊN *(⛔ ghi rồi mới
    KeyError lúc ĐỌC)*, và ⛔ tăng phiên bản."""
    v0 = _max_phien(conn, chr.BANG_HD)
    with pytest.raises(hd.LoiHD):
        chr.nap(conn, chr.BANG_HD, [("ZZ", {"ten": "x"})], nguon="x", actor="z")
    assert _max_phien(conn, chr.BANG_HD) == v0


def test_C5R1_04_tai_dung_fx_ban_RONG_ra_LoiFX():
    """Lõi đọc `_fx_tu_cap([])` ⇒ `fx.LoiFX` *(thang_dau=None)* — kiểm cả lúc ĐỌC."""
    with pytest.raises(fx.LoiFX):
        chr._fx_tu_cap([], nguon="x")


def test_C5R1_04_tai_dung_hd_ban_BAN_ra_LoiHD_khong_KeyError():
    """`_hd_tu_cap` dựng lại CAP bằng `.get()` + `hd.kiem` ⇒ bản thiếu `cha` ra
    `LoiHD` *(có TÊN)*, ⛔ `KeyError: 'cha'` *(nguyên nhân 500 FLS-INTERNAL ở R1)*."""
    with pytest.raises(hd.LoiHD):
        chr._hd_tu_cap([("ZZ", {"ten": "x"})], nguon="x")


def test_C5R1_04_doc_hd_ban_HONG_ra_BanHong_CO_TEN_khong_KeyError(monkeypatch):
    """Nếu LỠ có bản bẩn trong kho *(ghi thẳng SQL, ⛔ qua `nap`)*, `doc_hd` phải ra
    `BanHong` *(mã `FLS-CAUHINH-BAN-HONG`)*, ⛔ `KeyError`. Bơm `_doc_ban` trả một bản
    thiếu trường ⇒ ⛔ đầu độc `fls_test` dùng chung bằng một bản bẩn THẬT."""
    hong = chr.BanCauHinh(bang=chr.BANG_HD, phien_ban=9_999, nguon="x", checksum="x",
                          luc=datetime(2026, 1, 1, tzinfo=timezone.utc), actor="x",
                          khong_doi=False, dong=(("ZZ", {"ten": "x"}),))
    monkeypatch.setattr(chr, "_doc_ban", lambda _c, _b: hong)
    with pytest.raises(chr.BanHong) as e:
        chr.doc_hd(None)
    assert e.value.ma == "FLS-CAUHINH-BAN-HONG"


# ── C5-R1-05 · GHI NHẬN: `khong_doi` so bản LIỀN TRƯỚC *(⛔ bản đầu)* ───────────────
def test_C5R1_05_khong_doi_so_ban_LIEN_TRUOC_khong_phai_ban_DAU(conn):
    """Giết R1-M4 *(`khong_doi` so với bản ĐẦU thay bản kề trước ⇒ SỐNG khi nạp < 3
    lần)*. Nạp A, B, A: bản thứ ba KHÁC bản kề trước *(B)* ⇒ `khong_doi=False`; chỉ so
    bản ĐẦU *(A)* mới nhầm thành True."""
    # ⭐ C11 (WO-180): `IX.ALR` nay CÓ kiểm riêng ⇒ bản mẫu `{"v": …}` bị `LoiLuatPB` chặn TRƯỚC khi
    #   ghi. Đổi sang `IX.TMP`: bang HỢP LỆ, CHƯA có kiểm riêng, ⛔ ai nạp / đo rỗng — grep `tests/`
    #   + `fls/` + `tools/` `IX.TMP`: 0 dòng ngoài danh mục `BANG_HOP_LE` ⇒ bài này là người ghi
    #   DUY NHẤT *(bước nào sau nạp `IX.TMP` thật ⇒ phải đổi bảng mẫu lần nữa — `C9-R1-01`)*.
    bang = "IX.TMP"
    A = [("x", {"v": "1"})]
    B = [("x", {"v": "2"})]
    chr.nap(conn, bang, A, nguon="n", actor="a")
    b2 = chr.nap(conn, bang, B, nguon="n", actor="a")
    b3 = chr.nap(conn, bang, A, nguon="n", actor="a")
    assert b2.khong_doi is False, "⛔ B khác A ⇒ khong_doi=False"
    assert b3.khong_doi is False, (
        "⛔ A(3) khác B(2) kề trước ⇒ False; chỉ so bản ĐẦU (A) mới nhầm True")
