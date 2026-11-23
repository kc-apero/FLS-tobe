# -*- coding: utf-8 -*-
"""Bảo hộ cho phép ĐO — nhỏ, nhưng nó cứu được hai lần rồi."""
from __future__ import annotations


def ty_le(tu: int, mau: int, thap: float, cao: float, nhan: str) -> float:
    """Tính một tỷ lệ, và **NỔ** khi rơi ra ngoài khoảng đã khai trước.

    ⛔⛔ **Vì sao hàm này tồn tại.** `Đ4-a` đếm *"dòng đã ghép được"* bằng phép
    *"ô ⛔ không rỗng"* và ra **10.777 / 10.194 = 105,7%**. Một tỷ lệ ghép
    **⛔ không thể có** — và đó là **dấu hiệu DUY NHẤT** cho thấy phép đếm sai
    *(nó đang đếm cả 7.372 ô `#N/A`)*. ⚠ Nếu con số ấy rơi vào 60–70% thì nó
    đã **trông hợp lý**, và đã đi thẳng vào tài liệu mà ⛔ không ai nghi gì.

    ⇒ Luật: **mọi tỷ lệ phải KHAI KHOẢNG HỢP LỆ TRƯỚC khi tính.** Một phép đo
    ⛔ không tự đỏ được thì nó ⛔ chưa phải một phép đo — nó là một con số.
    """
    if mau <= 0:
        raise ValueError("⛔ %s: mẫu số = %d" % (nhan, mau))
    r = 100.0 * tu / mau
    if not (thap <= r <= cao):
        raise ValueError(
            "⛔⛔ %s = %.1f%% (%d/%d) — NGOÀI khoảng đã khai [%.0f%%, %.0f%%]. "
            "Phép ĐẾM sai trước khi cái SỐ sai." % (nhan, r, tu, mau, thap, cao))
    return r
