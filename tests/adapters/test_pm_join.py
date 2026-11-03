"""Cong cua adapter A — ghep bank <-> lenh chi PM.

Chin phep thu `T-JOIN-01..09` cua `DEV-10` §5, cong cong tren DU LIEU THAT.

⚠ `T-JOIN-03` cua spec doi *"phieu 3 dong, Σ amount = tien bank ⇒ 3 dong ITL"* —
dung, nhung tien de cua no (*"mot phieu N dong dung CHUNG mot ma"*) **khong tai
lap duoc** tren nguon: 526/1.468 phieu mang 2-36 ma KHAC NHAU. Nen phep thu
duoc viet lai theo dung cai do duoc: **mot MA, N dong PM** — xem
`test_T_JOIN_03_...`.
"""
from __future__ import annotations

import json
from decimal import Decimal as D
from pathlib import Path

import pytest

from fls.adapters.pm_join import (DAY_NGUOI, GHEP_DUOC, PM_DONG_DAU,
                                  PM_DONG_TIEU_DE, PM_TIEU_DE_MONG_DOI,
                                  DongBank, DongPM, NguonPMDoiHinhDang,
                                  canon_ref, chia_tien, kiem_tieu_de_pm,
                                  moi_noi, xep_ca_lat, xep_hinh)

HIEN_VAT = Path(__file__).resolve().parents[1] / "fixture" / "pm_join.json"
CHECKSUM = "6ec10945e6c1636a"
TOI_THIEU_DONG_BANK = 9_000       # cong #7: chung minh DA DO DUOC GI


def _b(dong: int, ref: str | None, tien: str, cur: str = "VND") -> DongBank:
    return DongBank(dong, canon_ref(ref), D(tien), cur)


def _p(dong: int, ref: str | None, tien: str, line: str,
       cur: str = "VND", slip: str = "PM1") -> DongPM:
    return DongPM(dong, slip, line, D(tien), cur, "Approve", canon_ref(ref))


# ---- T-JOIN-01 · T-JOIN-02 · chuan hoa khoa -------------------------------

def test_T_JOIN_01_khoang_trang_va_dau_gach_khong_lam_lech_khoa():
    assert canon_ref("ft25 123-456") == canon_ref("FT25123456") == "FT25123456"
    assert canon_ref(" PC00043/CNCT ") == canon_ref("pc00043_cnct") == "PC00043CNCT"


def test_T_JOIN_02_ma_rong_hoac_chi_co_dau_thi_None__va_None_KHONG_ghep():
    for v in (None, "", "   ", "---", " / . , ", "#N/A", "#REF!"):
        assert canon_ref(v) is None, v
    # va hai ben cung None thi ⛔ khong duoc thanh mot nhom
    nhom, tk = xep_ca_lat([_b(5, None, "100")], [_p(3, None, "100", "L1")])
    assert nhom == [] and tk.khong_co_ma == 1 and tk.can()


def test_canon_ref_dung_lai_so_dang_KHOA_HOC():
    """Ho hong cua DUONG DOC, khong phai cua so: Sheets API tra so chung tu dai
    duoi dang `4.36619E+15`. Khong dung lai thi hai ben cung ma ma khong ghep.
    """
    assert canon_ref("4.36619E+15") == "4366190000000000"
    assert canon_ref(4366190000000000.0) == "4366190000000000"


def test_canon_ref_KHONG_cat_tien_to_bank__GAP_JOIN_01():
    """⛔ Cat tien to la **gop hai lenh khac nhau** — hong nang hon khong ghep."""
    assert canon_ref("FT25008206502507") != canon_ref("FT25008206502508")
    assert canon_ref("EBANKING31/FT25265Y2V60") == "EBANKING31FT25265Y2V60"


# ---- T-JOIN-03 · T-JOIN-04 · cong Σ ---------------------------------------

def test_T_JOIN_03_mot_ma_N_dong_PM_Σ_khop__chia_tien_KHIT():
    n = xep_hinh("R1", [_b(5, "R1", "600")],
                 [_p(3, "R1", "100", "L1"), _p(4, "R1", "200", "L2"),
                  _p(5, "R1", "300", "L3")])
    assert n.hinh == "B" and n.ghep_duoc
    noi = moi_noi(n)
    assert [x[1] for x in noi] == ["L1", "L2", "L3"]      # ⛔ khong bo dong nao
    assert sum(x[2] for x in noi) == D("600")
    assert [x[2] for x in noi] == [D("100"), D("200"), D("300")]


def test_T_JOIN_04_Σ_lech_thi_KHONG_dong_nao_duoc_gan():
    # ⚠ So cu (599 vs 600) nay NAM TRONG dung sai 1.000 VND nen khong con la `F`.
    # Doi len tren nguong de bai nay van kiem dung cai no muon kiem.
    n = xep_hinh("R1", [_b(5, "R1", "598000")],
                 [_p(3, "R1", "100000", "L1"), _p(4, "R1", "500000", "L2")])
    assert n.hinh == "F" and not n.ghep_duoc
    assert "lech" in n.ly_do
    with pytest.raises(ValueError, match="khong ghep duoc"):
        moi_noi(n)


def test_dung_sai_VND_1000__owner_chot_27_08():
    """⭐ `GAP-CR1-01` DA CHOT: dung sai **1.000 VND** (owner, 27/08).

    Truoc do dung sai = 0 va bai nay khoa dieu nguoc lai. Doi lai la dung, vi
    noi nguong la quyet dinh cua **ke toan truong**, ⛔ khong phai cua code.
    Do duoc: dung sai nay cuu **+24 dong** (2.677 -> 2.701).
    """
    trong = xep_hinh("R1", [_b(5, "R1", "1000100.00")],
                     [_p(3, "R1", "1000000.00", "L1")])   # lech 100 <= 1.000
    assert trong.hinh == "A", trong.ly_do
    ngoai = xep_hinh("R2", [_b(6, "R2", "1001001.00")],
                     [_p(4, "R2", "1000000.00", "L2")])   # lech 1.001 > 1.000
    assert ngoai.hinh == "F", ngoai.ly_do
    assert "dung sai 1000" in ngoai.ly_do


def test_dung_sai_GHEP_TAY_lay_cai_NHO_hon_trong_hai_dieu_kien():
    """`QĐ-ITL-63`: cua TAY = min(1.000 dong, 0,5% tien bank).

    Bon moc do duoc, moi moc noi ro dieu kien nao dang chan:
    """
    from decimal import Decimal as _D

    from fls.adapters.pm_join import dung_sai_ghep_tay as f

    # khoan NHO: **ty le** chan (0,5% cua 100 = 0,5 < 1.000)
    assert f({"VND"}, _D("100")) == _D("0.500")
    # moc doi chieu: 200.000 dong la cho hai dieu kien BANG nhau
    assert f({"VND"}, _D("200000")) == _D("1000.000")
    # khoan LON: **con so tuyet doi** chan (0,5% cua 3,7 ty = 18,5 trieu)
    assert f({"VND"}, _D("3691169871")) == _D("1000")
    # ⛔ `QĐ-ITL-62` giu nguyen: ngoai te co dung sai **0** o CA HAI cua
    assert f({"USD"}, _D("1000000")) == _D("0")
    # ⛔ tien bank 0 ⇒ dung sai 0 (chan mac dinh), ⛔ khong mo cua
    assert f({"VND"}, _D("0")) == _D("0")


def test_KHOA_bang_DUNG_SAI_chi_duoc_co_VND():
    """⛔⛔ `QĐ-ITL-62` (2026-08-28): **ngoai te KHONG co dung sai** — owner chot.

    Bai nay ⛔ khong kiem mot gia tri, no khoa **ca cai bang**: them bat ky khoa
    nao ngoai `VND` la doi mot **quyet dinh ke toan**, phai xin owner.

    ★ Vi sao can khoa: truoc 28/08, so `0` o day mang nghia *"chua chot"* — mot
    cho de. Nguoi sau doc code rat de tuong day la viec chua lam xong va "sua
    cho xong" bang cach them `USD: 1000`. Nay `0` mang nghia **da chot**, va
    bai test nay la cho duy nhat noi ra su khac nhau ay bang may.

    Can cu do duoc (so that, 2.701 dong da ghep): moi ca lech ngoai te la **tra
    tung phan**, ⛔ khong ca nao la lam tron ⇒ dung sai ngoai te mo them **0**
    dong ghep, chi mo them rui ro.
    """
    from fls.adapters.pm_join import DUNG_SAI
    assert set(DUNG_SAI) == {"VND"}, (
        "⛔ Them tien te vao DUNG_SAI = doi `QĐ-ITL-62`. Ngoai te ⛔ KHONG co "
        "dung sai: may ⛔ khong duoc tu dong mot ca lech du chi vai xu.")


def test_dung_sai_KHONG_ap_cho_tien_te_CHUA_CHOT():
    """⛔⛔ 1.000 la 1.000 **VND**, ⛔ khong phai "1.000 don vi nao cung duoc".

    1.000 USD ≈ 26 trieu VND. Do tren so that: ap "1.000 don vi" cho moi tien te
    se cho qua **105 ma / 171 dong**, trong do co nhung ca lech **1.100% cua
    chinh giao dich** (lech 660,04 USD tren giao dich 59,96 USD) — do ⛔ khong
    phai phi bank hay lam tron, do la tien KHONG KHOP that.

    ⇒ Ngoai te: dung sai = **0**. Truoc 28/08 la *"chua chot"*; nay la
    **da chot** — `QĐ-ITL-62` dong `GAP-CR1-03`.
    """
    n = xep_hinh("R1", [_b(5, "R1", "100.50", "USD")],
                 [_p(3, "R1", "100.00", "L1", "USD")])
    assert n.hinh == "F", "USD ⛔ khong co dung sai ⇒ lech 0,50 vao hang cho"


def test_NHIEU_tien_te_thi_dung_sai_ve_KHONG():
    """Nhom nhieu tien te ⛔ khong duoc lay dung sai cua mot trong so chung."""
    from fls.adapters.pm_join import dung_sai_cua
    from decimal import Decimal as _D
    assert dung_sai_cua({"VND"}) == _D("1000")
    assert dung_sai_cua({"USD"}) == _D("0")
    assert dung_sai_cua({"VND", "USD"}) == _D("0")
    assert dung_sai_cua(set()) == _D("0")


def test_CHO_HO_da_biet__dung_sai_tuyet_doi_lon_hon_giao_dich_NHO():
    """⚠⚠ CHO HO CO TEN, ⛔ khong an: dung sai **tuyet doi** thi voi giao dich
    NHO no co the lon hon chinh giao dich.

    Vi du duoi: giao dich 500 dong, lenh 1.400 dong — lech 900 <= 1.000 nen luat
    hien tai **CHO GHEP**, du hai so chenh nhau **gan 3 lan**.

    Do tren so that 27/08: **39 dong so** VND co so tien <= 1.000 dong ⇒ voi
    chung dung sai nay bang hoac lon hon ca giao dich. Trong lat da do thi
    ⛔ khong co ca nao THUC SU bi ghep sai vi the (nhom VND <= 1.000 co lech lon
    nhat chi **2,00 dong**), nhung **luat van ho**.

    ⛔ Bai nay ⛔ KHONG sua luat — noi nguong la quyet dinh cua ke toan truong.
    No **ghi cho ho lai** de no khong vo hinh, va de con so 39 co ai canh.
    """
    n = xep_hinh("R1", [_b(5, "R1", "500")], [_p(3, "R1", "1400", "L1")])
    assert n.hinh == "A", "luat hien tai cho qua — day la CHO HO, khong phai loi"


def test_tien_te_KHAC_nhau_bi_bat_TRUOC_phep_cong():
    """★ Thu tu phep kiem la co chu y: cong hai so khac don vi ra mot con so
    **trong hinh** nhung vo nghia — va neu no tinh co bang nhau thi ta vua ghep
    sai ma khong cong nao do. Do that: 199 dong thuoc lop nay.
    """
    n = xep_hinh("R1", [_b(5, "R1", "100", "USD")],
                 [_p(3, "R1", "100", "L1", cur="VND")])
    assert n.hinh == "E" and "USD" in n.ly_do and "VND" in n.ly_do
    assert n.tong_bank() == n.tong_pm()      # so BANG nhau ma van KHONG ghep


def test_tien_te_RONG_mot_ben_KHONG_phai_bang_chung_la_KHAC_nhau():
    """⚠ Toi da dem sai mot nhom khi do nhap: script do coi o tien te RONG la
    *"tien te khac nhau"*. RONG la **khong biet**, ⛔ khong phai **khac**.

    Nen nhom do roi ve `F` (Σ lech) — dung, vi tien do that su lech 240 (phi
    bank). Tren so that co dung **1 nhom** thuoc dien nay: ma `20260708000001`.
    """
    n = xep_hinh("R1", [_b(5, "R1", "100", "")], [_p(3, "R1", "100", "L1", cur="USD")])
    assert n.hinh == "A", "tien te rong bi doc thanh KHAC nhau"
    n2 = xep_hinh("R1", [_b(5, "R1", "101", "")], [_p(3, "R1", "100", "L1", cur="USD")])
    assert n2.hinh == "F"


# ---- T-JOIN-05 · nhieu phieu ----------------------------------------------

def test_T_JOIN_05_N_bank_x_M_PM_thi_KHONG_DOAN_du_Σ_KHOP():
    """★★ Cho tu choi manh nhat cua ca module.

    N×M co nhieu cach chia tien khac nhau ma **deu cong dung** — chon mot cach
    la may quyet thay nguoi (`INV-I16`). Do that: 27 dong.
    """
    n = xep_hinh("R1", [_b(5, "R1", "300"), _b(6, "R1", "300")],
                 [_p(3, "R1", "200", "L1"), _p(4, "R1", "400", "L2")])
    assert n.hinh == "D" and not n.ghep_duoc
    assert n.tong_bank() == n.tong_pm() == D("600")
    assert "nhieu cach chia deu cong dung" in n.ly_do


def test_N_bank_x_1_PM_la_TRA_NHIEU_LAN__ghep_duoc_va_KHONG_chia():
    """Moi dong bank mang so tien CUA CHINH NO, ca N deu tro ve MOT `line_id`."""
    n = xep_hinh("R1", [_b(5, "R1", "400"), _b(6, "R1", "600")],
                 [_p(3, "R1", "1000", "L1")])
    assert n.hinh == "C" and n.ghep_duoc
    assert moi_noi(n) == [(5, "L1", D("400")), (6, "L1", D("600"))]


# ---- T-JOIN-08 · T-JOIN-09 ------------------------------------------------

def test_T_JOIN_09_bon_duong_luon_can__0_dong_roi_im_lang():
    # ⚠ So cu (100 vs 999) nay nam TRONG dung sai 1.000 VND ⇒ doi len.
    bank = [_b(5, "R1", "100000"), _b(6, "R2", "100000"), _b(7, None, "100000"),
            _b(8, "KHONGCO", "100000")]
    pm = [_p(3, "R1", "100000", "L1"), _p(4, "R2", "999000", "L2")]
    nhom, tk = xep_ca_lat(bank, pm)
    assert tk.can(), tk.bao()
    assert tk.dong_bank == 4
    assert tk.khong_co_ma == 1 and tk.khong_thay_ma_PM == 1
    assert tk.ghep_duoc() == 1 and tk.day_nguoi() == 1
    assert {n.hinh for n in nhom} == {"A", "F"}


def test_chay_hai_lan_cho_ket_qua_Y_HET():
    bank = [_b(9, "R2", "5"), _b(5, "R1", "100"), _b(6, "R2", "95")]
    pm = [_p(3, "R1", "100", "L1"), _p(4, "R2", "100", "L2")]
    a = xep_ca_lat(bank, pm)
    b = xep_ca_lat(bank, pm)
    assert [n.hinh for n in a[0]] == [n.hinh for n in b[0]]
    assert [n.ref for n in a[0]] == [n.ref for n in b[0]]
    assert a[1].dong_theo_hinh == b[1].dong_theo_hinh


# ---- chia tien: cho de mat tien le --------------------------------------

def test_chia_tien_KHONG_MAT_MOT_DONG_LE_nao():
    """⚠ Chia theo ty le roi lam tron tung phan thi mat vai dong le — va mat
    tien le trong mot he ke toan la loi khong the giai thich.
    """
    assert sum(chia_tien(D("100.00"), [D(1), D(1), D(1)])) == D("100.00")
    assert sum(chia_tien(D("0.01"), [D(1), D(1)])) == D("0.01")
    assert sum(chia_tien(D("1000000.03"), [D(7), D(11), D(13)])) == D("1000000.03")
    # du don vao phan LON NHAT
    assert chia_tien(D("10.00"), [D(1), D(8)]) == [D("1.11"), D("8.89")]


def test_chia_tien_NO_khi_khong_the_chia():
    with pytest.raises(ValueError, match="khong co phan nao"):
        chia_tien(D("100"), [])
    with pytest.raises(ValueError, match="⛔ khong chia deu"):
        chia_tien(D("100"), [D(0), D(0)])


# ---- ④ nguon doi hinh dang -----------------------------------------------

def test_nguon_PM_doi_ten_mot_cot_thi_NO_TO():
    dung = [""] * 28
    for i, v in PM_TIEU_DE_MONG_DOI.items():
        dung[i] = v
    kiem_tieu_de_pm(dung)                     # khong nem

    doi = list(dung)
    doi[25] = "Reference No."
    with pytest.raises(NguonPMDoiHinhDang, match="vi tri 25"):
        kiem_tieu_de_pm(doi)

    thieu = dung[:20]
    with pytest.raises(NguonPMDoiHinhDang, match="thieu cot"):
        kiem_tieu_de_pm(thieu)


def test_tieu_de_o_dong_2_khong_phai_dong_3():
    """⚠ Toi doc lech mot dong 27/08: mat dong du lieu dau tien VA header thanh
    mot dong du lieu. Khoa lai con so de khong ai "sua" nham.
    """
    assert (PM_DONG_TIEU_DE, PM_DONG_DAU) == (2, 3)


# ---- cong tren DU LIEU THAT ---------------------------------------------

@pytest.fixture(scope="module")
def that() -> dict:
    d = json.loads(HIEN_VAT.read_text(encoding="utf-8"))
    bank = [DongBank(x["dong"], canon_ref(x["ref_tho"]), D(x["tien"]), x["cur"])
            for x in d["bank"]]
    pm = [DongPM(x["dong"], x["slip"], x["line"],
                 D(x["tien"]) if x["tien"] else None, x["cur"], x["status"],
                 canon_ref(x["ref_tho"]), x["hd"] or None, x["cdt1"] or None)
          for x in d["pm"]]
    nhom, tk = xep_ca_lat(bank, pm)
    return {"meta": d, "bank": bank, "pm": pm, "nhom": nhom, "tk": tk}


def test_hien_vat_dung_ban_da_do(that):
    m = that["meta"]
    assert m["checksum_noi_dung"] == CHECKSUM
    assert (m["so_dong_pm"], m["so_dong_bank"]) == (3703, 9992)
    assert len(that["bank"]) >= TOI_THIEU_DONG_BANK


def test_SAU_HINH_DANG_dung_nhu_da_do(that):
    """★★ Cong chinh. Con so nay la con so se len bao cao, nen no bi khoa o day."""
    tk = that["tk"]
    assert tk.can(), tk.bao()
    assert tk.dong_bank == 9992
    assert tk.khong_co_ma == 105
    assert tk.khong_thay_ma_PM == 6532
    # ⭐ Sau khi owner chot dung sai Σ = **1.000 VND** (27/08, `GAP-CR1-01`).
    # Giu ca hai bo so de ai doc cung thay dung sai DOI CAI GI:
    #   dung sai 0     : A 2256 · B 27 · C  80(394 dong) · D 5 · E 119 · F 325(452)
    #   dung sai 1.000 : A 2272 · B 29 · C  82(400 dong) · D 5 · E 119 · F 305(428)
    assert tk.theo_hinh == {"A": 2272, "B": 29, "C": 82, "D": 5, "E": 119, "F": 305}
    assert tk.dong_theo_hinh == {"A": 2272, "B": 29, "C": 400, "D": 27,
                                 "E": 199, "F": 428}


def test_PHEP_GHEP_DUNG_NHO_HON_phep_ghep_dang_dung(that):
    """★★★ Con so phai noi thang, ⛔ khong lam dep.

    AS-IS `VLOOKUP` bao ghep **3.312/9.992 = 33,2%** — nhung khong kiem tien.
    FLS ghep **2.701 = 27,03%** ma khong phai doan, va **654 dong** co ma khop
    nhung tien khong khop thi vao hang cho **kem ly do co ten**.

    ⛔ Day KHONG phai tut lui: 968/3.312 dong ma AS-IS bao "da ghep" thuc ra
    khong khop tien. Day la lan dau con so co nghia.
    """
    tk = that["tk"]
    # 2.677 (dung sai 0) -> 2.701 (dung sai 1.000 VND): **+24 dong**
    assert tk.ghep_duoc() == 2701
    assert tk.day_nguoi() == 654
    assert round(100 * tk.ghep_duoc() / tk.dong_bank, 2) == 27.03
    # so dong AS-IS "ghep duoc" = moi dong tim thay ma PM
    as_is = tk.ghep_duoc() + tk.day_nguoi()
    assert as_is == 3355 and round(100 * as_is / tk.dong_bank, 2) == 33.58


def test_moi_nhom_GHEP_DUOC_deu_ra_moi_noi_CONG_KHIT(that):
    """Tien vao = tien ra, tung nhom. ⛔ Khong nhom nao mat mot dong le."""
    n_noi = 0
    for n in that["nhom"]:
        if not n.ghep_duoc:
            continue
        noi = moi_noi(n)
        n_noi += len(noi)
        assert sum(x[2] for x in noi) == n.tong_bank(), n.ref
        assert all(x[1] for x in noi), f"{n.ref}: co moi noi thieu line_id"
    assert n_noi >= 2701


def test_moi_nhom_DAY_NGUOI_deu_co_LY_DO_bang_chu(that):
    """⛔ Khong duoc phep "khong ghep duoc" ma khong noi vi sao (`ACC-4`)."""
    for n in that["nhom"]:
        if n.ghep_duoc:
            continue
        assert n.hinh in DAY_NGUOI
        assert len(n.ly_do) >= 10, f"{n.ref} hinh {n.hinh}: ly do qua mong"


def test_hinh_D_bi_tu_choi_DU_Σ_KHOP__tren_du_lieu_that(that):
    """Tren so that co dung 5 ma dang N×M voi Σ khop. Ca 5 deu bi tu choi."""
    d = [n for n in that["nhom"] if n.hinh == "D"]
    assert len(d) == 5
    for n in d:
        assert n.tong_bank() == n.tong_pm()          # Σ KHOP
        assert not n.ghep_duoc                        # ma VAN khong ghep
        assert len(n.bank) > 1 and len(n.pm) > 1


def test_ghep_duoc_va_day_nguoi_KHONG_chong_nhau():
    assert not (set(GHEP_DUOC) & set(DAY_NGUOI))
    assert len(GHEP_DUOC) + len(DAY_NGUOI) == 6


# ---- ⛔ NOI RO CAI CHUA LAM, thay vi de nguoi doc tu suy -------------------

def test_BA_TANG_CHUA_LAM__va_ly_do_tung_tang():
    """⛔ Spec `DEV-10` co 6 tang. Module nay lam **T1 · T2 · T5**. Ba tang con
    lai CHUA lam, va day la ly do — ⛔ khong de nguoi doc tu suy la "xong het".

      T0 · dan nhan "khong can lenh chi"  -> chan boi `GAP-ITL-56` (luat 6 nhan
           chua co). ⛔ Tu bia luat nay la tu quyet dinh khoan nao "khong can
           lenh" — quyet dinh ke toan nang nhat cua ca bo.
      T3 · doc ma lenh trong Dien giai    -> chan boi `GAP-ITL-57` (70 hay 158
           dong, 19,57 ty phu thuoc) VA boi luat khong doc cot co the chua ten
           nguoi. Can owner cho phep pham vi doc truoc.
      T4 · nguoi bam Ghep o F01           -> can `fls/api` + `fls/web` (P4·P6).
           Module nay da chuan bi san dau vao cho no: 678 dong `D/E/F` kem
           ly do co ten chinh la hang doi cua T4.

    ⚠ `T-JOIN-06` (T3) va `T-JOIN-07` (match cua nguoi khong bi de) **chua co
    phep thu** — vi chua co gi de thu. Ghi ra day de con so "9 test T-JOIN"
    khong bi doc thanh "9/9 xong".
    """
    LAM = {"T1", "T2", "T5"}
    CHUA = {"T0": "GAP-ITL-56", "T3": "GAP-ITL-57", "T4": "P4·P6"}
    assert LAM & set(CHUA) == set()
    assert len(LAM) + len(CHUA) == 6
