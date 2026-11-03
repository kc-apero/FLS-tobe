"""Cot `Classifying` suy tu canon — va cai bay hai cap cot TRUNG TEN.

⚠ Toan bo module `classifying.py` ra doi de tra mot mon no: `ledge_spec.py` khai
bay cot `Classifying` la KHONG LUU vi *"suy lai duoc tu <cot canon>"* — ma
`<cot canon>` la mot **cho trong**. Loi hua khong co dia chi thi khong the do,
va khong do duoc thi khong biet no dung hay sai.

Hien vat: `tests/fixture/classifying_vs_canon.json` — 9.845 dong ghep duoc giua
`[Master] ITL Ledge` va `Transaction Mapping L1` **doc live 2026-08-26**.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fls.ledger.classifying import (VI_TRI_CHET, VI_TRI_CLASSIFYING,
                                    classifying, khoi_tu_canon, la_o_loi,
                                    ten_canon)
from fls.ledger.final_rule import KHONG_TRA_LOI, TEN_BAY_KHOI

HIEN_VAT = Path(__file__).resolve().parents[1] / "fixture" / "classifying_vs_canon.json"
CHECKSUM = "7226ef112dbd00f7"
DONG_MONG_DOI = 9845
TOI_THIEU_O = 60_000        # cong #7: chung minh DA DO DUOC GI, khong chi "khong thay loi"


@pytest.fixture(scope="module")
def hv() -> dict:
    d = json.loads(HIEN_VAT.read_text(encoding="utf-8"))
    bang = d["bang_gia_tri"]
    cot = {t: i for i, t in enumerate(d["cot"])}
    khoi = d["khoi"]
    hang = []
    for r in d["dong"]:
        hang.append({
            "dong_so": r[0], "dong_canon": r[1],
            # ⛔ giu theo VI TRI canon, ⛔ khong theo TEN KHOI: hien vat khong duoc
            # dong bang chinh ban do ma no dang dung de kiem.
            "canon": {p: bang[r[cot[f"canon_pos_{p}"]]] for p in d["vi_tri_giu"]},
            "cls": {t: bang[r[cot[f"cls_{t}"]]] for t in khoi},
        })
    return {"meta": d, "hang": hang, "khoi": khoi}


def _canon(h: dict, ten_khoi: str):
    """Tra ban do luc CHAY — be ban do la cong lon DO ngay."""
    return h["canon"][VI_TRI_CLASSIFYING[ten_khoi]]


# ---- luat, dang don vi -----------------------------------------------------

def test_o_loi_thanh_Need_to_manual_input():
    assert classifying("#N/A") == KHONG_TRA_LOI
    assert classifying("#REF!") == KHONG_TRA_LOI
    assert classifying("#N/A (Did not find value '' in VLOOKUP)") == KHONG_TRA_LOI


def test_o_RONG_GIU_RONG__khong_thanh_Need_to_manual_input():
    """★ Khac biet nho nhat cua ca module, va la cho de sai nhat.

    `iferror` chi bat O LOI. O rong di qua nguyen ven. Do tren du lieu that:
    luat "rong -> Need to manual input" khop 84,87% o khoi `invoice`
    (1.490 o lech) — xem `test_luat_A_...` duoi day.
    """
    assert classifying(None) is None
    assert classifying("") is None
    assert classifying("   ") is None


def test_gia_tri_thuong_di_qua_nguyen_van():
    assert classifying("OGA | GAC - Other") == "OGA | GAC - Other"
    assert classifying(" Thanh toán (Regular) ") == "Thanh toán (Regular)"
    assert classifying(202509) == "202509"        # ky dang so -> chuoi, khong .0
    assert classifying(202509.0) == "202509"


def test_bay_khoi_deu_co_dia_chi__khong_con_cho_trong():
    assert set(VI_TRI_CLASSIFYING) == TEN_BAY_KHOI
    assert len(set(VI_TRI_CLASSIFYING.values())) == 7      # khong khoi nao dung chung o
    assert "AB" in ten_canon("svc_start") and "AC" in ten_canon("svc_end")


def test_khoi_tu_canon_de_TRONG_o_nguoi_go():
    """Lan nap dau chua ai go gi ⇒ Manual = None ⇒ `dung_khoi` che do TU SINH."""
    from fls.canon.row import CanonRow
    o = [None] * 38
    o[18], o[7], o[27] = "OGA | GAC - Other", "#N/A", 202509
    k = khoi_tu_canon(CanonRow.from_list(o))
    assert set(k) == TEN_BAY_KHOI
    assert k["hd"] == ("OGA | GAC - Other", None)
    assert k["pay_type"] == (KHONG_TRA_LOI, None)
    assert k["svc_start"] == ("202509", None)
    assert k["cdt1"] == (None, None)
    assert all(v[1] is None for v in k.values())


# ---- cong tren DU LIEU THAT ------------------------------------------------

def test_hien_vat_dung_ban_da_do(hv):
    m = hv["meta"]
    assert m["checksum_noi_dung"] == CHECKSUM
    assert m["so_dong_ghep"] == len(hv["hang"]) == DONG_MONG_DOI
    assert m["so_dong_so"] == 9967
    # cong #7 ⓑ: ty le ghep phai cong bo, va phai du cao de ket luan co nghia
    assert m["so_dong_ghep"] / m["so_dong_so"] > 0.98


def test_BAY_KHOI_khop_100_PHAN_TRAM_tung_o(hv):
    """★★ Cong chinh: `Classifying` cua so == `iferror(<o canon>, NTMI)`.

    68.915 o · 7/7 khoi · **100,0000%** · 0 o lech.
    """
    khop = tong = 0
    lech: list[tuple] = []
    for h in hv["hang"]:
        for t in hv["khoi"]:
            tong += 1
            mong = classifying(_canon(h, t))
            co = h["cls"][t]
            co = classifying(co) if not la_o_loi(co) else co
            if mong == co:
                khop += 1
            elif len(lech) < 5:
                lech.append((h["dong_so"], t, _canon(h, t), h["cls"][t]))
    assert tong >= TOI_THIEU_O, f"chi do {tong} o — khong du de ket luan"
    assert (khop, tong) == (tong, 68_915), f"lech: {lech}"


def test_CAP_COT_TRUNG_TEN__lay_sai_thi_do_70_PHAN_TRAM(hv):
    """⚠⚠ Cong nay ton tai de ghi lai mot cai bay, va no DA THAY DO that.

    Khuon canon co HAI cap cot **trung ten y het**:
        W  · X  "Thoi diem bat dau/ket thuc su dung dich vu"
        AB · AC "Thoi diem bat dau/ket thuc su dung dich vu"

    Chon theo TEN thi rat de lay `W`/`X` — va `W`/`X` la cap **100% `#N/A` CO
    CHU Y** (`QD-ITL-51`). Lay sai thi `svc_start`/`svc_end` cua CA SO thanh
    `Need to manual input`: hang cho phong len, ⛔ khong cong nao do.

    Phep thu do CA HAI cap: cap dung 100%, cap chet ~70,4%.
    """
    for t in ("svc_start", "svc_end"):
        dung = sum(1 for h in hv["hang"]
                   if classifying(_canon(h, t)) == classifying(h["cls"][t]))
        chet = sum(1 for h in hv["hang"]
                   if classifying(h["canon"][VI_TRI_CHET[t]]) == classifying(h["cls"][t]))
        n = len(hv["hang"])
        assert dung == n, f"{t}: cap dung phai 100%, do duoc {dung}/{n}"
        assert 0.69 < chet / n < 0.71, f"{t}: cap chet {chet}/{n}"
    # va cap chet PHAI toan o loi — do la ly do no chet
    n_loi = sum(1 for h in hv["hang"]
                if la_o_loi(h["canon"][VI_TRI_CHET["svc_start"]]))
    assert n_loi / len(hv["hang"]) > 0.94, "cap W/X khong con la cap #N/A?"
    assert VI_TRI_CHET == {"svc_start": 22, "svc_end": 23}


def test_luat_A_rong_thanh_NTMI_la_SAI__do_duoc_bao_nhieu(hv):
    """⛔ Ghi lai bien the BI LOAI, kem con so — de khong ai "sua lai" ve luat A.

    Luat A: o rong CUNG thanh `Need to manual input`. Do that:
      invoice 8.355/9.845 (84,87%) · svc_start 9.302 · svc_end 9.296 · hd 9.842
    """
    def luat_A(v):
        return KHONG_TRA_LOI if (la_o_loi(v) or not str(v or "").strip()) else classifying(v)

    do = {}
    for t in hv["khoi"]:
        do[t] = sum(1 for h in hv["hang"]
                    if luat_A(_canon(h, t)) == classifying(h["cls"][t]))
    n = len(hv["hang"])
    assert do["invoice"] == 8355, do["invoice"]
    assert do["svc_start"] == 9302 and do["svc_end"] == 9296
    assert do["hd"] == 9842 and do["cdt1"] == 9839
    assert do["pay_type"] == n and do["id_payee"] == n   # hai khoi nay khong phan biet
    assert sum(do.values()) < 7 * n, "luat A phai SAI o dau do, khong thi 2 luat trung nhau"
