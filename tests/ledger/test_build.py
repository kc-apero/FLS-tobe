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
    from fls.ledger.final_rule import (CO_INPUT_HERE, KHONG_TRA_LOI,
                                       MAC_DINH_THEO_KHOI)
    d = dung_dong(_row(), 1, NC, khoi={"hd": (KHONG_TRA_LOI, CO_INPUT_HERE)})
    assert d["hd"] == MAC_DINH_THEO_KHOI["hd"] and d["hd_thyt"] is None
    assert d["work_status"] == "UNMAPPED"


def test_khoi_7_dung_mac_dinh_RIENG_khong_phai_cua_khoi_1():
    from fls.ledger.final_rule import CO_INPUT_HERE, KHONG_TRA_LOI
    d = dung_dong(_row(), 1, NC, khoi={"invoice": (KHONG_TRA_LOI, CO_INPUT_HERE)})
    assert d["invoice"] == "Nợ hoá đơn"
    assert d["invoice_thyt"] is None and d["work_status"] == "UNMAPPED"


def test_che_do_oracle_dung_MID_cua_so():
    """Khai MID => parity bam theo so, khong phu thuoc mac dinh cua FLS."""
    from fls.ledger.final_rule import CO_INPUT_HERE, KHONG_TRA_LOI
    d = dung_dong(_row(), 1, NC,
                  khoi={"hd": (KHONG_TRA_LOI, CO_INPUT_HERE, "GIA TRI CUA SO")})
    assert d["hd"] == "GIA TRI CUA SO" and d["hd_thyt"] is None


def test_work_status_ok_khi_khong_co_gi_bia():
    d = dung_dong(_row(), 1, NC, khoi={"hd": ("NB | Noi bo", "")})
    assert d["hd"] == "NB | Noi bo" and d["hd_thyt"] == "NB | Noi bo"
    assert d["work_status"] == "ok"


def test_khoi_ten_la_khong_thuoc_bay_khoi_thi_NO():
    with pytest.raises(ValueError, match="khong thuoc 7 khoi"):
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


# ---- hang cho: "khong suy duoc" cung phai vao (INV-I16) --------------------

def _khoi_day(cls_hd=None, cls_pt=None, cls_cdt=None, cls_s=None, cls_e=None):
    """Bay khoi DUOC HOI, o nguoi go de trong — y nhu lan nap dau tien."""
    return {"hd": (cls_hd, None), "pay_type": (cls_pt, None), "cdt1": (cls_cdt, None),
            "svc_start": (cls_s, None), "svc_end": (cls_e, None),
            "id_payee": (None, None), "invoice": (None, None)}


def _dong(khoi):
    o = [None] * 38
    o[0], o[1], o[3], o[5], o[6] = "2026-03-01", "CT1", "VND", 1000, "R | x"
    return dung_dong(CanonRow.from_list(o), 5,
                     NgucCanh("r", "v1", "v1", "v1", "RAW", "L1"), khoi=khoi)


def test_khoi_PNL_khong_co_dap_an_thi_vao_HANG_CHO():
    """★★ Lo do duoc o lan nap THAT dau tien 2026-08-26.

    9.973 dong vao so, **6.634 dong khong co `hd`**, hang cho dem duoc **0**.
    Man F01 se hien "khong co viec gi lam" trong khi hai phan ba so chua ai
    tra loi.

    Nguyen nhan: `work_status` chi xet `may_tu_bia` (may gan mac dinh) — tuc chi
    MOT NUA cua `INV-I16`. Nua con lai la *"truong nao may KHONG SUY DUOC"*.
    """
    assert _dong(_khoi_day())["work_status"] == "UNMAPPED"
    assert _dong(_khoi_day(cls_hd="OGA | GAC - Other"))["work_status"] == "UNMAPPED"
    day_du = _khoi_day("OGA | GAC - Other", "Thanh toán (Regular)",
                       "SHQ2 | Headquarters2", "202603", "202603")
    assert _dong(day_du)["work_status"] == "ok"


def test_Need_to_manual_input_la_KHONG_CO_DAP_AN__vao_hang_cho():
    """`Classifying = 'Need to manual input'` + khong ai go ⇒ `Final` None."""
    d = _dong(_khoi_day("Need to manual input", "Thanh toán (Regular)",
                        "SHQ2 | Headquarters2", "202603", "202603"))
    assert d["hd"] is None and d["work_status"] == "UNMAPPED"


def test_khoi_6_7_NGOAI_PNL_khong_tu_minh_day_dong_vao_hang_cho():
    """⚠ Mot quyet dinh NGHIEP VU, khai ra chu khong an.

    `id_payee`/`invoice` thieu tren **95,7%** va **70,5%** dong. Neu chung day
    hang cho thi hang cho luon dai ~9.500 dong va khong ai doc nua. Nen chi 5
    khoi P&L (dung 5 truong cua ITL-CONTRACT) day dong vao hang cho.
    """
    day_du = _khoi_day("OGA | GAC - Other", "Thanh toán (Regular)",
                       "SHQ2 | Headquarters2", "202603", "202603")
    d = _dong(day_du)                      # khoi 6-7 DUOC HOI ma khong co dap an
    assert d["id_payee"] is None and d["invoice"] is None
    assert d["work_status"] == "ok"
