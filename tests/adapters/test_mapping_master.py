"""Cong bo nap `Mapping Master` — bang QUYET DINH PHAN BO (`GAP-ALLOC-01`).

★★ **Vi sao bo nap nay ton tai.** `QĐ-ITL-65` bo nam cot vung ALLOCATE khoi kho
voi ly do *"suy lai duoc tu `hd` + `fls_mapping_master`"*. Phep suy da co
(`ledger/allocate.py`), nhung bang tra **0 dong** ⇒ phep suy luon tra `#N/A`.
Mot loi hua treo la mot lo, ⛔ khong phai mot viec con lai.

★ Bai o day chan ba lop, va lop nao cung tung sap o mot bo nap nao trong du an:

    ⓐ **DIA CHI** — cat sai dong dau thi phep dem *tu khop voi chinh no* ma van
      sai. Chinh toi mac 28/08: cat tu dong 4 ra `52 -> 53` va `coa1 0 -> 1`.
    ⓑ **RONG ⛔ khong duoc thanh CHUOI RONG** — vi `ledger/allocate.py` phan
      biet hai cai do thanh `"0"` va `"No need"`, dung theo Sheets.
    ⓒ **LOAI phai co TEN** — ma trung, o loi: ⛔ khong bo im (`ACC-4`).
"""
from __future__ import annotations

import pytest

from fls.adapters.mapping_master import COT, DONG_DAU, TRUONG, doc_cot, tom_tat
from fls.ledger.allocate import CO_KHONG_CAN, suy_allocate

# ── Mot tab GIA co dung hinh dang that: header dong 3, nhan phu 4-6, du lieu 7+
HEADER = {
    "H": ["", "", "", "HD Code", "", ""],
    "I": ["", "", "COA1", "#REF! (Please use a desktop…)", "", ""],
    "J": ["", "", "COA2", "", "", ""],
    "K": ["", "", "Need to Allocate to CFA2", "", "", ""],
    "L": ["", "", "Method to Allocate to CFA2", "", "", ""],
    "M": ["", "", "Code HR Allocate", "", "", ""],
}


def _tab(*dong: tuple) -> dict[str, list]:
    """`dong` = (H, I, J, K, L, M) cho tung dong DU LIEU (tu dong 7)."""
    ra = {c: list(v) for c, v in HEADER.items()}
    for d in dong:
        for c, v in zip("HIJKLM", d):
            ra[c].append(v)
    return ra


# ─────────────────────────────────────────────────── ⓐ dia chi
def test_DIA_CHI_khoa_cung__dong_dau_la_7_va_sau_cot():
    """⛔ Doi dia chi la doi mot dong o MOT cho — va phai co y."""
    assert DONG_DAU == 7, (
        "du lieu `Mapping Master` bat dau dong 7 (do 2026-08-28): header dong "
        "3, nhan phu 4-6. Con so 7 nay trung khit neo `V7:V` cua ba cong thuc "
        "ALLOCATE")
    assert list(COT) == ["H", "I", "J", "K", "L", "M"]
    assert TRUONG == ("hd_code", "coa1", "coa2", "need_cfa2", "method_cfa2",
                      "code_hr")


def test_BA_DONG_HEADER_khong_vao_kho():
    """⛔⛔ Bai da bat loi THAT cua toi. Cat tu dong 4 thi `H4='HD Code'` thanh
    mot ma `hd`, va `J4='#REF!…'` thanh mot gia tri `coa2` — hai rac vao kho,
    va phep dem VAN tu khop nen ⛔ khong ai thay."""
    dong, loai = doc_cot(_tab(("GI | Gross Inflow", "", "", "", "GI Ledger", "")))
    assert [d.hd_code for d in dong] == ["GI | Gross Inflow"]
    assert loai == []
    # ⭐ Va dong sheet phai la 7 — de ai doi soat con mo dung dong tren sheet.
    assert dong[0].dong_sheet == 7

    # ⛔ Cat tu dong 4 (nhu toi da lam) thi rac vao kho:
    sai, _l = doc_cot(_tab(("GI | Gross Inflow", "", "", "", "GI Ledger", "")),
                      dong_dau=4)
    assert "HD Code" in [d.hd_code for d in sai], (
        "bai nay phai chung minh duoc rang cat sai dong thi CO rac — neu khong "
        "thi no ⛔ khong do gi")


# ─────────────────────────────────────────────────── ⓑ rong vs chuoi rong
def test_O_RONG_thanh_None__va_None_lam_Method_ra_0_dung_nhu_SHEETS():
    """⛔⛔ Bay `VLOOKUP`: o rong -> Sheets cho `0`, ⛔ khong `"No need"`.

    Neu bo nap luu `""` thay vi `None` thi `allocate` se cho `"No need"` va
    lech han voi sheet that — o **52 trong 73 ma** (do 28/08).
    """
    dong, _l = doc_cot(_tab(("OPC | Operating Cost", "", "", "", "", "")))
    d = dong[0]
    assert d.method_cfa2 is None and d.need_cfa2 is None
    assert suy_allocate("SHQ2 | HQ2", d.hd_code, d).method == "0"


def test_CHUOI_RONG_THAT_moi_cho_No_need():
    """★ `"No need"` chi xuat hien khi o that su chua mot CHUOI RONG."""
    assert suy_allocate("X", "HD", {"need_cfa2": None, "method_cfa2": ""}
                        ).method == CO_KHONG_CAN


def test_DAU_CACH_khong_phai_gia_tri():
    """⛔ `"   "` la mot o nguoi go nham, ⛔ khong phai mot phuong phap."""
    dong, _l = doc_cot(_tab(("HD | X", "  ", "", "   ", "  ", "")))
    assert dong[0].method_cfa2 is None and dong[0].coa1 is None


# ─────────────────────────────────────────────────── ⓒ loai co TEN
def test_ma_TRUNG_thi_giu_dong_DAU_va_LOAI_dong_sau_KEM_LY_DO():
    """`VLOOKUP` lay dong DAU, nen dong sau ⛔ khong bao gio duoc dung — giu no
    la giu mot ban su that thu hai."""
    dong, loai = doc_cot(_tab(
        ("GI | Gross Inflow", "", "", "Need to Allocate to CFA2", "GI Ledger", ""),
        ("GI | Gross Inflow", "", "", "", "By NOEM", ""),
    ))
    assert [d.hd_code for d in dong] == ["GI | Gross Inflow"]
    assert dong[0].method_cfa2 == "GI Ledger", "phai giu dong DAU"
    assert len(loai) == 1
    assert loai[0].dong_sheet == 8
    assert "TRUNG voi dong 7" in loai[0].ly_do


def test_O_LOI_o_cot_khoa_thi_LOAI_kem_ly_do():
    dong, loai = doc_cot(_tab(("#REF!", "", "", "", "", ""),
                              ("HD | That", "", "", "", "", "")))
    assert [d.hd_code for d in dong] == ["HD | That"]
    assert len(loai) == 1 and "O LOI" in loai[0].ly_do


def test_dong_TRONG_thi_bo_IM__khong_tinh_la_loai():
    """⛔ Tab co 4.464 dong ma chi ~73 dong co du lieu; coi 4.391 dong trong la
    *"bi loai"* thi bao cao thanh rac va ⛔ khong ai doc no nua."""
    dong, loai = doc_cot(_tab(("HD | A", "", "", "", "", ""),
                              ("", "", "", "", "", ""),
                              ("", "", "", "", "", ""),
                              ("HD | B", "", "", "", "", "")))
    assert [d.hd_code for d in dong] == ["HD | A", "HD | B"]
    assert loai == []
    assert [d.dong_sheet for d in dong] == [7, 10]


def test_THIEU_mot_cot_thi_NO_ngay__khong_lang_le_de_None():
    with pytest.raises(ValueError, match="thieu cot"):
        doc_cot({"H": [], "K": [], "L": []})


# ─────────────────────────────────────────────────── tom tat
def test_tom_tat_dem_dung_va_method_rong_la_con_so_dong_GAP_ALLOC_01():
    dong, _l = doc_cot(_tab(
        ("A", "", "", "Need to Allocate to CFA2", "GI Ledger", "MC"),
        ("B", "", "", "Need to Allocate to CFA2", "", ""),
        ("C", "", "", "", "", ""),
    ))
    t = tom_tat(dong)
    assert t["ma"] == 3
    assert t["can_phan_bo"] == 2
    assert t["co_phuong_phap"] == 1
    assert t["method_rong"] == 2
    assert t["co_code_hr"] == 1
    assert t["co_coa1"] == 0 and t["co_coa2"] == 0
