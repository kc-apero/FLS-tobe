from datetime import date

import pytest

from fls.canon.row import CanonRow
from fls.ledger.build import NgucCanh, content_key, dung_dong

NC = NgucCanh(run_id="r1", contract_version="v1.0", canon_version="v1.0",
              mapping_version="v1.0", source_system="P100", source_sheet="Bank")


def _row():
    v = [None] * 38
    v[0], v[1], v[2], v[3] = date(2026, 1, 31), "CT-1", "chuyen tien", "VND"
    v[4], v[5], v[6] = 0, 1000, "1121"
    return CanonRow.from_list(v)


def test_sau_phep_chep_BASE_giu_nguyen_van():
    d = dung_dong(_row(), 7, NC)
    assert d["doc_date"] == date(2026, 1, 31)
    assert (d["doc_no"], d["memo"], d["curr"]) == ("CT-1", "chuyen tien", "VND")
    assert (d["ps_no"], d["ps_co"], d["acct"]) == (0, 1000, "1121")


def test_lineage_va_ba_version_khong_bao_gio_NULL():
    d = dung_dong(_row(), 7, NC)
    for k in ("source_system", "source_sheet", "source_row", "run_id",
              "contract_version", "canon_version", "mapping_version"):
        assert d[k] not in (None, ""), k
    assert d["source_row"] == 7


def test_khong_tu_gan_itl_id():
    """INV-I04a: itl_id do SEQUENCE cua DB cap, lop so KHONG duoc tu danh so."""
    assert "itl_id" not in dung_dong(_row(), 1, NC)


def test_canon_luu_du_38_o():
    assert len(dung_dong(_row(), 1, NC)["canon"]) == 38


def test_content_key_tat_dinh_va_doi_khi_thanh_phan_doi():
    a = content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)
    assert a == content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)
    assert a != content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 1)
    assert a != content_key("Cash", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)


def test_hai_dong_trung_noi_dung_phai_khac_khoa_nho_seq_trung():
    """281 dong trung + 103 dong khong co so chung tu => khoa noi dung MOT MINH
    khong du lam danh tinh (DD-I05)."""
    d0 = dung_dong(_row(), 1, NC, seq_trung=0)
    d1 = dung_dong(_row(), 2, NC, seq_trung=1)
    assert d0["content_key"] != d1["content_key"]


def test_content_key_KHONG_dung_source_row():
    """source_row la vi tri dong — dua vao khoa la tai lap dung loi AS-IS."""
    a = dung_dong(_row(), 1, NC)["content_key"]
    b = dung_dong(_row(), 999, NC)["content_key"]
    assert a == b, "content_key khong duoc phu thuoc vi tri dong"


def test_work_status_UNMAPPED_khi_may_tu_bia():
    from fls.ledger.final_rule import CO_INPUT_HERE, KHONG_TRA_LOI, MAC_DINH_CUNG
    d = dung_dong(_row(), 1, NC, khoi={"hd": (KHONG_TRA_LOI, CO_INPUT_HERE)})
    assert d["hd"] == MAC_DINH_CUNG and d["hd_thyt"] is None
    assert d["work_status"] == "UNMAPPED"


def test_work_status_ok_khi_khong_co_gi_bia():
    d = dung_dong(_row(), 1, NC, khoi={"hd": ("NB | Noi bo", "")})
    assert d["hd"] == "NB | Noi bo" and d["hd_thyt"] == "NB | Noi bo"
    assert d["work_status"] == "ok"


def test_khoi_ten_la_khong_thuoc_5_khoi_thi_NO():
    with pytest.raises(ValueError, match="khong thuoc 5 khoi"):
        dung_dong(_row(), 1, NC, khoi={"khong_co_that": ("a", "b")})


def test_khoi_khong_khai_thi_de_None_khong_bia():
    d = dung_dong(_row(), 1, NC)
    for a, b in (("hd", "hd_thyt"), ("cdt1", "cdt1_thyt")):
        assert d[a] is None and d[b] is None


def test_dong_bi_LOAI_thi_NO_khong_am_tham_dung_dong():
    """Dong sai kieu phai vao fls_reject, KHONG duoc dung thanh dong so."""
    v = [None] * 38
    v[0] = "rac khong doc duoc"
    with pytest.raises(ValueError, match="khong the dung dong"):
        dung_dong(CanonRow.from_list(v), 1, NC)


def test_le_lay_tu_canon_AG_khong_phai_tu_cot_trung_ten():
    """le = canon AG (vi tri 32) 'LE'. AH-AK la 4 cot trung ten, KHONG dung."""
    v = [None] * 38
    v[0], v[3], v[4], v[5], v[6] = date(2026, 1, 31), "VND", 0, 1000, "1121"
    v[32] = "SGO1"
    v[33] = "KHONG-DUOC-LAY"
    d = dung_dong(CanonRow.from_list(v), 1, NC)
    assert d["le"] == "SGO1"
