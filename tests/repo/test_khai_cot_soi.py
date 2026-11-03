# -*- coding: utf-8 -*-
"""Phép soi bản khai — thuần hàm, ⛔ không chạm kho.

⭐ Mọi bài ở đây soi **TRƯỚC KHI CHẠM KHO**. Đó là chỗ đúng: một bản khai hỏng
   bị chặn ở tầng ghi thì kho ⛔ **không bao giờ** phải chứa nó, còn chặn ở tầng
   đọc thì nó **đã nằm trong kho rồi** — và giữa hai lúc ấy có thể đã có người
   nạp một lô tiền.
"""
import pytest

from fls.adapters.sao_ke import SAU_TRUONG
from fls.repo.khai_cot import LoiKhai, _soi_khai


def _du() -> dict[str, int]:
    return {t: i for i, t in enumerate(SAU_TRUONG)}


def test_ban_khai_du_thi_di_qua():
    assert _soi_khai(_du()) == _du()


def test_ten_truong_LA_thi_NO_chu_KHONG_bo_qua():
    """⛔⛔ Bỏ qua tên lạ là biến **một lỗi gõ** thành **một trường thiếu**.

    `{'Credit ': 4}` *(thừa dấu cách)* mà lặng lẽ bỏ qua thì thông báo sẽ là
    *"thiếu `Credit`"* — và người ta đi sửa **nhầm chỗ**, đúng cái sheet họ vừa
    khai đủ.
    """
    x = _du()
    x["Creditt"] = 9
    with pytest.raises(LoiKhai, match="tên trường lạ"):
        _soi_khai(x)


def test_cot_AM_thi_NO():
    x = _du()
    x["Debit"] = -1
    with pytest.raises(LoiKhai, match="âm"):
        _soi_khai(x)


def test_cot_KHONG_phai_so_nguyen_thi_NO():
    x = _du()
    x["Debit"] = "3"
    with pytest.raises(LoiKhai, match="SỐ NGUYÊN"):
        _soi_khai(x)


def test_cot_la_BOOL_thi_NO():
    """⛔⛔ `bool` là **con của `int`** trong Python.

    ⛔ Không có nhánh riêng thì `True` lọt qua thành **cột 1** — một bản khai
    trỏ sai cột mà ⛔ không lỗi nào nổ. Đây là loại lỗi ⛔ không ai đọc code mà
    thấy được.
    """
    x = _du()
    x["Debit"] = True
    with pytest.raises(LoiKhai, match="SỐ NGUYÊN"):
        _soi_khai(x)


def test_cot_bang_0_van_HOP_LE():
    """⛔ `0` là cột **đầu tiên**, ⛔ không phải *"chưa khai"*. Một phép kiểm viết
    `if not cot:` sẽ loại đúng cột `A` của mọi sheet."""
    x = _du()
    x["Date"] = 0
    assert _soi_khai(x)["Date"] == 0


def test_HAI_truong_cung_tro_MOT_cot_van_di_qua():
    """⚠ Ghi lại **một chỗ CỐ Ý ⛔ không chặn**, để nó ⛔ không bị coi là bỏ sót.

    `sao_ke.doc_ban_khai()` đọc dòng 1 thật cũng ⛔ **không thể** sinh ra tình
    huống này *(một ô mang một số)*, nên chặn ở đây là chặn một thứ ⛔ chưa ai
    đo thấy. ⇒ Theo `R-A1`: ⛔ không bịa ra một luật cho một hình dạng ⛔ chưa
    quan sát được. Bao giờ đo thấy thì mở một quyết định, ⛔ không vá lặng lẽ.
    """
    x = _du()
    x["Credit"] = x["Debit"]
    assert _soi_khai(x)["Credit"] == x["Debit"]
