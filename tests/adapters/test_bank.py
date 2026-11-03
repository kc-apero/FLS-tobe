"""Adapter B — sau dieu kien xong cua DoD 5.7, moi cai mot test."""
from __future__ import annotations

import pytest

from fls.adapters.bank import (NguonDoiHinhDang, ThongKe, dong_rong, dung_canon,
                               kiem_header, nap)
from fls.canon.row import SO_VI_TRI
from fls.canon.spec import CANON_COLS, pos_of

HEADER = [c.name for c in CANON_COLS]


def _hang(**kw) -> list:
    """Mot dong hop le toi thieu: 7 cot goc + LE + No."""
    o = [None] * SO_VI_TRI
    o[0], o[1], o[2] = 46082, "975205104", "Card charge"
    o[3], o[5], o[6] = "USD", 660.6, "R | PO2_OCBC USD_S"
    o[pos_of("AG")], o[pos_of("AL")] = "VVOT", 1
    for k, v in kw.items():
        o[pos_of(k)] = v
    return o


# ---- ④ nguon doi hinh dang thi NO TO ---------------------------------------

def test_header_dung_thi_khong_no():
    kiem_header(HEADER)


def test_doi_TEN_mot_cot_thi_NO_TO():
    xau = list(HEADER)
    xau[0] = "Ngay chung tu"                 # bo dau
    with pytest.raises(NguonDoiHinhDang, match="lech ten"):
        kiem_header(xau)


def test_them_mot_cot_thi_NO_TO():
    with pytest.raises(NguonDoiHinhDang):
        kiem_header(HEADER + ["Cot moi ai do vua them"])


def test_doi_THU_TU_hai_cot_thi_NO_TO():
    """Doi cho la loi nguy nhat: tong van khop, moi o deu ve sai cho."""
    xau = list(HEADER)
    xau[4], xau[5] = xau[5], xau[4]          # PS No <-> PS Co
    with pytest.raises(NguonDoiHinhDang):
        kiem_header(xau)


def test_hai_cot_TRONG_Z_AA_phai_van_trong_trong_header():
    xau = list(HEADER)
    xau[pos_of("Z")] = "ai do vua dat ten cho cot trong"
    with pytest.raises(NguonDoiHinhDang):
        kiem_header(xau)


def test_bon_cot_TRUNG_TEN_khong_lam_kiem_header_nham():
    """AH-AK trung ten het nhau — doi chieu theo VI TRI nen van phat hien duoc."""
    xau = list(HEADER)
    xau[pos_of("AH")] = "MID I DoubleCheck LE x"
    with pytest.raises(NguonDoiHinhDang, match="AH"):
        kiem_header(xau)


# ---- ⑥ thieu truong => trong CO KIEM SOAT, khong bia ------------------------

def test_dong_ngan_hon_38_thi_pad_bang_None_khong_bia_gia_tri():
    row, ly_do = dung_canon([46082, "975205104", "x", "USD", None, 660.6,
                             "R | acc"])
    assert ly_do == [] and row is not None
    assert len(row) == SO_VI_TRI
    assert row.by_letter("AG") is None       # ⛔ khong bia "VVOT"


def test_dong_dai_hon_38_thi_cat_dung_38_vi_tri():
    row, _ = dung_canon(_hang() + ["thua", "thua"])
    assert row is not None and len(row) == SO_VI_TRI


# ---- R-ORA-07a / 07c -------------------------------------------------------

def test_R_ORA_07a_o_loi_o_nua_mapping_thanh_None_chu_khong_bi_loai():
    row, ly_do = dung_canon(_hang(W="#N/A (Did not find value)",
                                  H="#N/A", S="#N/A"))
    assert ly_do == [], ly_do
    assert row is not None
    assert row.by_letter("W") is None and row.by_letter("S") is None


def test_R_ORA_07c_Z_va_AA_luon_None_nhung_VAN_giu_vi_tri():
    row, _ = dung_canon(_hang(Z="rac", AA="rac"))
    assert row is not None
    assert row.by_letter("Z") is None and row.by_letter("AA") is None
    assert len(row) == SO_VI_TRI


def test_o_loi_o_COT_GOC_thi_LOAI_va_ly_do_CO_TEN():
    row, ly_do = dung_canon(_hang(C="#REF!"))
    assert row is None
    assert len(ly_do) == 1 and "C" in ly_do[0] and "#REF!" in ly_do[0]


def test_nhieu_cot_goc_loi_thi_bao_HET_chu_khong_dung_o_cai_dau():
    _row, ly_do = dung_canon(_hang(B="#N/A", C="#REF!", AG="#VALUE!"))
    assert len(ly_do) == 3


# ---- ③ ba duong luon can ---------------------------------------------------

def test_dong_rong_duoc_nhan_ra():
    assert dong_rong([None] * SO_VI_TRI)
    assert dong_rong(["", "", "", "", "", "", ""])
    assert not dong_rong(_hang())


def test_ba_duong_can_va_khong_dong_nao_roi_im_lang():
    tho = [_hang(), _hang(C="#REF!"), [None] * SO_VI_TRI, _hang(W="#N/A")]
    ra, loai, tk = nap(tho, header=HEADER)
    assert (tk.vao, tk.ra, tk.loai, tk.rong) == (4, 2, 1, 1)
    assert tk.can() and tk.tong() == len(tho)
    assert len(ra) == 2 and len(loai) == 1


def test_dong_bi_loai_mang_so_dong_THAT_cua_sheet():
    """Ly do khong co dia chi thi ke toan khong tim duoc dong ma sua."""
    _ra, loai, _tk = nap([_hang(), _hang(C="#REF!")])
    assert loai[0][0] == 6            # dong_dau=5, phan tu thu 2 => dong 6


def test_dong_DUOC_GIU_cung_mang_so_dong_THAT__lineage_INV_I05():
    """★ `source_row` la mot phan cua lineage. Thieu no thi tang ghi phai TU
    DANH SO — va tu danh so la dung lai loi AS-IS (id bam vi tri dong).

    Dong trong o giua KHONG duoc lam lech so dong cua dong sau no.
    """
    ra, _loai, _tk = nap([_hang(), [None] * SO_VI_TRI, _hang(), _hang(C="#REF!"),
                          _hang()])
    assert [i for i, _ in ra] == [5, 7, 9]


def test_thong_ke_lech_thi_can_False():
    assert not ThongKe(vao=10, ra=5, loai=2, rong=2).can()


# ---- ⑤ idempotent + ② khong bien doi gia tri -------------------------------

def test_chay_hai_lan_cho_ket_qua_Y_HET():
    tho = [_hang(), _hang(C="#REF!"), _hang(W="#N/A")]
    a = nap(tho, header=HEADER)
    b = nap(tho, header=HEADER)
    assert [(i, r.vals) for i, r in a[0]] == [(i, r.vals) for i, r in b[0]]
    assert a[1] == b[1] and a[2] == b[2]


def test_gia_tri_duoc_CHEP_NGUYEN_khong_chuan_hoa():
    """Cong ra P2 la parity 100% tung o — moi phep lam sach o day la mot cho do."""
    row, _ = dung_canon(_hang(B="  975205104  ", D="usd"))
    assert row is not None
    assert row.by_letter("B") == "  975205104  "     # ⛔ khong strip
    assert row.by_letter("D") == "usd"               # ⛔ khong upper
    assert row.by_letter("F") == 660.6               # ⛔ khong lam tron


def test_nap_khong_header_thi_bo_qua_phep_kiem_hinh_dang():
    ra, _loai, tk = nap([_hang()])
    assert len(ra) == 1 and tk.can()
