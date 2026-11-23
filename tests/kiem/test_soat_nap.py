# -*- coding: utf-8 -*-
"""`F04` chang 2 · Bang chung rang tam luat `soat_nap` **DO DUOC**.

⭐⭐ Cung ly do voi `test_nguon_song.py`: cong `tools/soat_nap_sao_ke.py` doc
   Google Sheets **song**, nen ⛔ **khong the tu chung minh no do duoc**. ⇒ Luat
   thuan o `fls/kiem/soat_nap.py`, va o day moi luat co **ba ca**:
   XANH · DO-that · RONG *(⛔ khong duoc xanh)*.

⛔⛔ Ca DO cua `S7` la ca quan trong nhat ve **thiet ke**: no chung minh khoa
   trung **⛔ khong chua `Num`**. Neu ai do them `Num` vao khoa, bai
   `test_S7_DO_du_Num_KHAC_nhau` se do — dung nhu y muon.
"""
from __future__ import annotations

from fls.adapters.sao_ke import KHUON_RA
from fls.kiem import soat_nap as sn


def _dong(xuat_xu="R | A", ngay="45586", ma="FT001", no="1000", co="",
          te="VND", num=1) -> list:
    d = [""] * len(KHUON_RA)
    d[sn.NGAY], d[sn.TE], d[sn.NO] = ngay, te, no
    d[sn.CO], d[sn.MA], d[sn.XUAT_XU] = co, ma, xuat_xu
    d[KHUON_RA.index("Num")] = num
    return d


# ── S1 ─────────────────────────────────────────────────────────────────────
def test_S1_xanh():
    kq = sn.s1_ba_duong_can({"R | A": (10, 8, 2, 0), "R | B": (5, 5, 0, 0)})
    assert kq.xanh and kq.da_do == 2 and kq.hang == sn.CHAN


def test_S1_DO_khi_mot_dong_roi_im_lang():
    kq = sn.s1_ba_duong_can({"R | A": (10, 8, 1, 0)})
    assert not kq.xanh and "vao 10" in kq.thong_diep


def test_S1_DO_khi_rong():
    assert not sn.s1_ba_duong_can({}).xanh


# ── S2 ─────────────────────────────────────────────────────────────────────
def test_S2_xanh():
    kq = sn.s2_co_tien_thi_phai_co_ma([_dong(), _dong(ma="FT002")])
    assert kq.xanh and kq.hang == sn.CO_


def test_S2_DO_khi_co_tien_ma_khong_co_ma():
    kq = sn.s2_co_tien_thi_phai_co_ma([_dong(), _dong(ma="")])
    assert not kq.xanh and "1/2" in kq.thong_diep


def test_S2_dong_KHONG_tien_ma_khong_ma_thi_KHONG_pham():
    """⛔ `S2` chi noi ve dong CO TIEN — dong rong la viec cua `S3`."""
    assert sn.s2_co_tien_thi_phai_co_ma([_dong(), _dong(ma="", no="")]).xanh


def test_S2_DO_khi_rong():
    assert not sn.s2_co_tien_thi_phai_co_ma([]).xanh


# ── S3 ─────────────────────────────────────────────────────────────────────
def test_S3_xanh_va_ve_CO_cung_tinh_la_co_tien():
    assert sn.s3_moi_dong_phai_co_tien([_dong(), _dong(no="", co="500")]).xanh


def test_S3_DO_khi_so_0_KHONG_duoc_coi_la_co_tien():
    """⛔⛔ Bay da gap that o `F02`: *"o nao KHONG RONG"* coi `0` la co so."""
    kq = sn.s3_moi_dong_phai_co_tien([_dong(), _dong(no="0", co="0")])
    assert not kq.xanh and "1/2" in kq.thong_diep


def test_S3_DO_khi_rong():
    assert not sn.s3_moi_dong_phai_co_tien([]).xanh


# ── S4 ─────────────────────────────────────────────────────────────────────
def test_S4_xanh():
    assert sn.s4_moi_dong_phai_co_tien_te([_dong(), _dong(te="USD")]).xanh


def test_S4_DO_khi_thieu_tien_te():
    kq = sn.s4_moi_dong_phai_co_tien_te([_dong(), _dong(te="  ")])
    assert not kq.xanh and "1/2" in kq.thong_diep


def test_S4_DO_khi_rong():
    assert not sn.s4_moi_dong_phai_co_tien_te([]).xanh


# ── S5 ─────────────────────────────────────────────────────────────────────
def test_S5_xanh():
    kq = sn.s5_ma_khong_bi_ha_kieu([_dong(ma="4366185033872500")])
    assert kq.xanh and kq.hang == sn.CANH


def test_S5_DO_dung_hinh_ma_Bank_Transactions_dang_hong():
    """Dung **dung** hinh da do o chang 1: `4366185033872500.0`."""
    kq = sn.s5_ma_khong_bi_ha_kieu([_dong(ma="4366185033872500.0")])
    assert not kq.xanh and "`.0`" in kq.thong_diep


def test_S5_DO_khi_rong():
    assert not sn.s5_ma_khong_bi_ha_kieu([]).xanh


# ── S6 ─────────────────────────────────────────────────────────────────────
def test_S6_xanh_hai_sheet_hai_kieu_KHAC_nhau_van_dat():
    """⭐ Luat noi ve **trong MOT sheet**, ⛔ khong doi ca doi hinh giong nhau
    — do song: 4.172 chuoi + 4.166 seri, ma **0/60 sheet tron**."""
    kq = sn.s6_mot_sheet_mot_kieu_ngay(
        [_dong(xuat_xu="R | A", ngay="45586"),
         _dong(xuat_xu="R | B", ngay="07/28/2026")])
    assert kq.xanh and kq.da_do == 2


def test_S6_DO_khi_MOT_sheet_tron_hai_kieu():
    kq = sn.s6_mot_sheet_mot_kieu_ngay(
        [_dong(xuat_xu="R | A", ngay="45586"),
         _dong(xuat_xu="R | A", ngay="07/28/2026")])
    assert not kq.xanh and "R | A" in kq.thong_diep


def test_S6_DO_khi_rong():
    assert not sn.s6_mot_sheet_mot_kieu_ngay([]).xanh


# ── S7 ─────────────────────────────────────────────────────────────────────
def test_S7_xanh():
    assert sn.s7_dong_trung_hoan_toan([_dong(), _dong(ma="FT002")]).xanh


def test_S7_DO_du_Num_KHAC_nhau():
    """⛔⛔ **Bai kiem soat THIET KE.** Hai dong y het, chi khac `Num` — ma
    `Num` do **chinh FLS** sinh. Neu ai do them `Num` vao khoa thi phep kiem
    nay **⛔ khong bao gio do duoc nua**, va bai nay se bat duoc."""
    kq = sn.s7_dong_trung_hoan_toan([_dong(num=1), _dong(num=2)])
    assert not kq.xanh and "1 khoa trung" in kq.thong_diep


def test_S7_khac_XUAT_XU_thi_KHONG_phai_trung():
    """Hai tai khoan cung nhan mot ma la chuyen binh thuong."""
    assert sn.s7_dong_trung_hoan_toan(
        [_dong(xuat_xu="R | A"), _dong(xuat_xu="R | B")]).xanh


def test_S7_DO_khi_rong():
    assert not sn.s7_dong_trung_hoan_toan([]).xanh


# ── S8 ─────────────────────────────────────────────────────────────────────
def test_S8_xanh_va_hang_la_CO_KHONG_phai_CHAN():
    """⛔⛔ Hang nay tung la `CHAN` va do la sai. Lan chay that dau tien cho
    ra **dung hai** ca, va ca hai la **danh muc GO NHAM MOT KY TU** — khuyet
    tat cua ke toan, ⛔ khong phai cua FLS."""
    kq = sn.s8_xuat_xu_co_trong_danh_muc({"R | A"}, {"R | A", "R | B"})
    assert kq.xanh and kq.hang == sn.CO_


def test_S8_DO_khi_xuat_xu_la():
    kq = sn.s8_xuat_xu_co_trong_danh_muc(
        {"R | LA"}, {"R | A"})
    assert not kq.xanh and "R | LA" in kq.thong_diep


def test_S8_DO_bat_dung_hinh_GO_NHAM_MOT_KY_TU_do_song():
    """Dung **dung** hai hinh da do song: danh muc thua `'1'`, thua `'7'`.

    ⭐ Ca nay ton tai de ⛔ **khong ai xep lai `S8` thanh `CHAN`**: no chung
    minh thu ma `S8` bat duoc la **loi go cua nguoi**, ⛔ khong phai loi nap.
    """
    kq = sn.s8_xuat_xu_co_trong_danh_muc(
        {"R | 132000050920_MauBank USD_MGO1",
         "R | PO_Payoneer USD_CGO1"},
        {"R | 1132000050920_MauBank USD_MGO1", "R | PO7_Payoneer USD_CGO1"})
    assert not kq.xanh and kq.hang == sn.CO_
    assert "2/2 sheet nap" in kq.thong_diep


def test_S8_van_soi_duoc_sheet_ra_0_DONG():
    """⛔⛔ **Bai giu dung DIEM MU vua tim duoc.** Ban dau `S8` suy tap nguon
    tu `rows` ⇒ mot sheet la **ra 0 dong** thi ⛔ **bien mat khoi chinh phep
    kiem sinh ra de tim no**: chay that bao **1** trong khi su that la **2**.
    ⇒ `nguon` phai la tap sheet DA NAP, ⛔ khong phai tap suy tu du lieu.
    """
    kq = sn.s8_xuat_xu_co_trong_danh_muc({"R | RONG"}, {"R | A"})
    assert not kq.xanh and "R | RONG" in kq.thong_diep


def test_S8_DO_khi_danh_muc_rong():
    """⛔ Danh muc rong ⇒ ⛔ khong do duoc gi ⇒ ⛔ KHONG duoc xanh."""
    assert not sn.s8_xuat_xu_co_trong_danh_muc({"R | A"}, set()).xanh


# ── luat chung + phan hang ────────────────────────────────────────────────
def test_MOI_luat_deu_DO_khi_do_duoc_0_thu():
    """⛔⛔ Xanh tren tap RONG la **chua do**, ⛔ khong phai **dat**."""
    rong = [
        sn.s1_ba_duong_can({}),
        sn.s2_co_tien_thi_phai_co_ma([]),
        sn.s3_moi_dong_phai_co_tien([]),
        sn.s4_moi_dong_phai_co_tien_te([]),
        sn.s5_ma_khong_bi_ha_kieu([]),
        sn.s6_mot_sheet_mot_kieu_ngay([]),
        sn.s7_dong_trung_hoan_toan([]),
        sn.s8_xuat_xu_co_trong_danh_muc(set(), set()),
    ]
    assert len(rong) == 8
    for kq in rong:
        assert not kq.xanh, kq.ten
        assert kq.da_do == 0, kq.ten


def test_CHI_hang_CHAN_moi_chan_lan_nap():
    """⭐ Phan hang ⛔ KHONG phai noi cong: hang `CO` van **DO**, chi la
    ⛔ khong chan — vi nhung dong ay la **tien that**, vut di la vi pham
    *'⛔ 0 dong roi im lang'*."""
    do_co = sn.s2_co_tien_thi_phai_co_ma([_dong(ma="")])
    do_chan = sn.s1_ba_duong_can({"R | A": (10, 8, 1, 0)})
    assert not do_co.xanh and not do_chan.xanh
    chan = sn.chan_lai([do_co, do_chan])
    assert [k.hang for k in chan] == [sn.CHAN]


def test_MOI_luat_deu_khai_MOT_trong_ba_hang():
    kq = [sn.s1_ba_duong_can({"R | A": (1, 1, 0, 0)}),
          sn.s2_co_tien_thi_phai_co_ma([_dong()]),
          sn.s3_moi_dong_phai_co_tien([_dong()]),
          sn.s4_moi_dong_phai_co_tien_te([_dong()]),
          sn.s5_ma_khong_bi_ha_kieu([_dong()]),
          sn.s6_mot_sheet_mot_kieu_ngay([_dong()]),
          sn.s7_dong_trung_hoan_toan([_dong()]),
          sn.s8_xuat_xu_co_trong_danh_muc({"R | A"}, {"R | A"})]
    assert {k.hang for k in kq} == {sn.CHAN, sn.CO_, sn.CANH}
