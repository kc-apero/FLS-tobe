# -*- coding: utf-8 -*-
"""Phép ĐO thứ tự ngày — `QĐ-ITL-113`. Thuần, ⛔ không kho.

⛔⛔ **Câu quan trọng nhất ở đây ⛔ KHÔNG phải *"đề xuất có đúng ⛔ không"*, mà
   là *"máy có biết LÚC NÀO PHẢI IM ⛔ không"***. Một phép đề xuất luôn trả ra
   một giá trị là một phép **đoán khoác áo phép đo** — và `QĐ-ITL-17` đã đo cái
   giá của nó: 93% dòng bị hoán ngày↔tháng, ~181 tỷ sai kỳ.
"""
from __future__ import annotations

from fls.kiem.thu_tu_ngay import (DMY, MDY, cau_bang_chung, do_mot_nguon)


def _do(*v):
    return do_mot_nguon(v)


# ───────────────────────────────────────────── ⓐ đếm đúng từng loại bằng chứng
def test_phan_dau_lon_hon_12_la_bang_chung_dmy():
    bc = _do("25/08/2026", "13/01/2026")
    assert (bc.chac_dmy, bc.chac_mdy, bc.mo_ho) == (2, 0, 0)
    assert bc.de_xuat == DMY


def test_phan_hai_lon_hon_12_la_bang_chung_mdy():
    bc = _do("08/25/2026", "01/13/2026")
    assert (bc.chac_dmy, bc.chac_mdy, bc.mo_ho) == (0, 2, 0)
    assert bc.de_xuat == MDY


def test_ca_hai_phan_nho_hon_13_la_MO_HO__khong_tinh_la_bang_chung():
    bc = _do("03/01/2026", "08/03/2026", "12/12/2026")
    assert (bc.chac_dmy, bc.chac_mdy, bc.mo_ho) == (0, 0, 3)
    assert bc.de_xuat is None, "⛔ ⛔ không bằng chứng nào ⇒ PHẢI im"
    assert bc.can_khai is True


def test_o_SO_la_seri_Google__KHONG_BAO_GIO_mo_ho():
    """⭐ 4.175/8.368 ô `Date` đo được là SỐ ⇒ nửa lô ⛔ không có vấn đề gì."""
    bc = _do(45586, 46000.0, 45900)
    assert (bc.o_so, bc.o_chuoi, bc.mo_ho) == (3, 0, 0)
    assert bc.can_khai is False


def test_True_KHONG_bi_dem_thanh_mot_seri():
    """⛔ `bool` là con của `int` trong Python — `True` sẽ lọt thành seri 1."""
    assert _do(True, False).o_so == 0


# ─────────────────────────────────────── ⓑ ⭐⭐ máy phải biết lúc nào PHẢI IM
def test_MAU_THUAN_thi_may_KHONG_de_xuat_gi():
    """⛔⛔ Nguồn có CẢ hai bằng chứng ⇒ ⛔ không thứ tự nào đúng cho cả nguồn.

    Đo 08/09: **0/60** nguồn như thế. ⛔ Nhưng ⛔ không được suy ra *"⛔ không
    thể xảy ra"* — nếu xảy ra mà máy vẫn chọn một bên thì nó **làm sai nửa còn
    lại trong im lặng**.
    """
    bc = _do("25/08/2026", "08/25/2026", "03/01/2026")
    assert bc.mau_thuan is True
    assert bc.de_xuat is None
    assert "MÂU THUẪN" in cau_bang_chung(bc)


def test_KHONG_dong_mo_ho_nao_thi_KHONG_CAN_khai():
    """⛔ Đòi kế toán khai một nguồn ⛔ không mơ hồ là bắt trả lời câu ⛔ không có.

    21/50 nguồn đo được là toàn ngày-số ⇒ `thu_tu` của chúng ⛔ vô nghĩa.
    """
    bc = _do("25/08/2026", 45586)
    assert bc.mo_ho == 0 and bc.can_khai is False
    assert "⛔ không cần khai" in cau_bang_chung(bc)


def test_o_RONG_va_rac_KHONG_lam_hong_phep_dem():
    bc = _do("", None, "khong-phai-ngay", "2026-08-25", "03/01/2026")
    # ⛔ `2026-08-25` (ISO) ⛔ không khớp `_DMY` ⇒ ⛔ không tính vào `o_chuoi`
    assert (bc.so_dong, bc.o_chuoi, bc.mo_ho) == (5, 1, 1)


# ───────────────────────────────────────────── ⓒ câu bằng chứng phải CÓ SỐ
def test_cau_bang_chung_LUON_neu_con_so__khong_chi_khuyen():
    """⛔⛔ Một cái nút kèm lời khuyên mà ⛔ không kèm phép đo là một cái nút
    sẽ được bấm mà ⛔ không ai đọc — lúc ấy *"người ấn định"* chỉ là một câu
    trong tài liệu."""
    bc = _do("08/25/2026", "08/25/2026", "03/01/2026")
    c = cau_bang_chung(bc)
    assert "2" in c and "1" in c, c
    assert MDY in c and DMY in c, "⛔ phải nêu CẢ hai để người so được"


# ────────────────────── ⓓ ⭐⭐⭐ ghim lại chính PHÉP ĐO đã ra quyết định 113
def test_tai_lap_dung_hinh_dang_da_do_tren_29_nguon_that():
    """⭐ Hình dạng bằng chứng của `R | PO2_OCBC USD_SGO2` — nguồn nặng nhất.

    Đo 08/09 trên ảnh chụp thật: **905** dòng mơ hồ · **1.263** dòng chắc chắn
    `mdy` · ⛔ **0** dòng chắc chắn `dmy` · **2.168** dòng chuỗi · ⛔ **0** ô số.

    ⛔ Bài này ⛔ không đọc kho *(nó thuần)* — nó dựng lại **đúng tỉ lệ ấy** và
      đòi phép đo cho ra cùng một kết luận. Nếu ai đổi luật đề xuất, bài này
      sẽ nói ngay rằng **quyết định `QĐ-ITL-113` ⛔ không còn đứng**.
    """
    v = ["08/25/2026"] * 1263 + ["08/03/2026"] * 905
    bc = do_mot_nguon(v)
    assert (bc.so_dong, bc.o_so, bc.o_chuoi) == (2168, 0, 2168)
    assert (bc.chac_mdy, bc.chac_dmy, bc.mo_ho) == (1263, 0, 905)
    assert bc.mau_thuan is False
    assert bc.de_xuat == MDY, (
        "⛔ 1.263 dòng làm chứng `mdy` và ⛔ 0 dòng làm chứng `dmy` mà máy ⛔ "
        "không đề xuất `mdy` thì phép đo này ⛔ không dùng được vào việc gì")
