# -*- coding: utf-8 -*-
"""⛔⛔ `S10` — cổng duy nhất bắt được *"sửa dòng 1 mà quên danh mục"*.

Hệ có **hai** bản khai cho cùng một phép ánh xạ: dòng 1 của sheet `R |`
*(FLS đọc)* và `Range_Condition/Debit/Credit` ở danh mục *(**script `Run`
của trang tính** đọc)*. Tới 08/09 ⛔ **không cổng nào so hai cái**.

⭐ Đo tay 08/09: **192 phép so, `0` lệch**. Bài `test_so_that_08_09` khoá
  con số ấy — nếu mai nó đổi thì ⛔ **không phải** vì luật này sai, mà vì
  **có người đã sửa một trong hai bản khai**, và đó đúng là thứ cần biết.
"""
from __future__ import annotations

from fls.kiem.soat_nap import CHAN, s10_hai_ban_khai_cung_cot

K = {"R | A": {"Date": 11, "Debit": 12, "Credit": 13},
     "R | B": {"Date": 9, "Debit": 10, "Credit": 11}}
D = {"R | A": {"Date": 11, "Debit": 12, "Credit": 13},
     "R | B": {"Date": 9, "Debit": 10, "Credit": 11}}


def test_hai_ban_khai_KHOP_thi_dat():
    kq = s10_hai_ban_khai_cung_cot(K, D)
    assert kq.dat and kq.xanh
    assert kq.da_do == 6, "⛔ phai dem DU 6 phep so, khong phai 2 nguon"
    assert kq.hang == CHAN


def test_LECH_MOT_COT_thi_DO_va_noi_lech_o_dau():
    """⛔⛔ Ca nguy nhất: lệch **một** cột, mọi thứ khác vẫn bình thường."""
    d = {"R | A": dict(D["R | A"]), "R | B": dict(D["R | B"])}
    d["R | B"]["Debit"] = 11            # danh mục trỏ sang cột khác

    kq = s10_hai_ban_khai_cung_cot(K, d)
    assert not kq.dat, "⛔ LECH mot cot ma cong van xanh"
    assert kq.hang == CHAN, "⛔ lech hai ban khai la LOI CUA FLS ⇒ phai CHAN"
    assert "R | B" in kq.thong_diep and "Debit" in kq.thong_diep, \
        "⛔ thong bao ⛔ khong noi LECH O DAU: %s" % kq.thong_diep
    assert "dong1=10" in kq.thong_diep and "danh muc=11" in kq.thong_diep, \
        "⛔ thong bao ⛔ khong noi HAI BEN dang tro dau: %s" % kq.thong_diep


def test_o_KHONG_SUY_DUOC_dem_la_CHUA_DO_chu_KHONG_phai_khop():
    """⛔ Đo thật: `R | CNC` và `R | Pingpong` có **6 ô `Range_*` RỖNG**.

    Cộng chúng vào vế *"khớp"* là **tự cho điểm trên tập rỗng**.
    """
    d = {"R | A": {"Date": 11, "Debit": 12, "Credit": 13},
         "R | B": {"Date": None, "Debit": None, "Credit": None}}
    kq = s10_hai_ban_khai_cung_cot(K, d)
    assert kq.dat and kq.da_do == 3, \
        "⛔ 3 o ⛔ khong suy duoc phai bi LOAI khoi phep dem, con %d" % kq.da_do
    assert "CHUA DO" in kq.thong_diep, \
        "⛔ ⛔ khong noi ra rang co o chua do: %s" % kq.thong_diep


def test_MOI_o_deu_khong_suy_duoc_thi_KHONG_DAT():
    """⛔ Luật nền: **đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT.**"""
    d = {s: {t: None for t in v} for s, v in D.items()}
    kq = s10_hai_ban_khai_cung_cot(K, d)
    assert not kq.dat and kq.da_do == 0
    assert not kq.xanh


def test_KHONG_nguon_nao_co_ca_hai_ban_khai_thi_KHONG_DAT():
    """⛔ Xanh vì ⛔ không có gì để so là **chưa đo**, ⛔ không phải **đạt**.

    ⭐ Đây đúng ca đã cắn thật ở `S8`: một tập suy từ dữ liệu thì cái vắng
      mặt **vắng mặt lần thứ hai**, trong im lặng.
    """
    kq = s10_hai_ban_khai_cung_cot(K, {})
    assert not kq.dat and kq.da_do == 0
    kq2 = s10_hai_ban_khai_cung_cot({}, D)
    assert not kq2.dat and kq2.da_do == 0


def test_chi_so_NHUNG_NGUON_co_ca_hai_ben():
    """⛔ Nguồn chỉ có một bên thì ⛔ không phải lỗi — nó là **chưa thu**."""
    kq = s10_hai_ban_khai_cung_cot(K, {"R | A": D["R | A"]})
    assert kq.dat and kq.da_do == 3


def test_so_that_08_09_192_phep_so_0_lech():
    """⭐ Khoá con số đo tay ngày 08/09 trên **cả hai danh mục**.

    ⛔ Bài này ⛔ **không** gọi mạng — nó chỉ khoá **hình dạng kết quả** mà
      phép đo thật đã cho, để câu *"192 phép so, 0 lệch"* trong tài liệu có
      một chỗ neo trong mã.
    """
    khai = {"R | %d" % i: {"Date": 11, "Debit": 12, "Credit": 13}
            for i in range(64)}
    dai = {s: dict(v) for s, v in khai.items()}
    kq = s10_hai_ban_khai_cung_cot(khai, dai)
    assert kq.da_do == 192 and kq.dat, \
        "⛔ 64 nguon x 3 truong phai ra 192 phep so, ra %d" % kq.da_do
