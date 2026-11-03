# -*- coding: utf-8 -*-
"""ĐO thứ tự ngày của một nguồn — thuần, ⛔ không kho, ⛔ không mạng.

⭐⭐⭐ **Module này ⛔ KHÔNG QUYẾT ĐỊNH gì. Nó chỉ ĐẾM.** `QĐ-ITL-113` đặt quyền
   ấn định kỳ kế toán **ở NGƯỜI**: máy **đề xuất kèm bằng chứng**, kế toán
   **bấm khai** *(→ `fls_khai_cot.thu_tu`, có `version` + `actor`)*.

   ⇒ Nên hàm ở đây trả về **BẰNG CHỨNG**, ⛔ không trả về *"thứ tự của nguồn
     này là X"*. Cái tên `de_xuat` cố ý ⛔ **không** phải `thu_tu`.

── Vì sao cần đo, và vì sao ⛔ KHÔNG được đoán ─────────────────────────────

Đo 2026-09-08 trên ảnh chụp thật `chup_id 23719` *(60 nguồn, 8.368 dòng)*:

    ô `Date` là SỐ *(seri Google — ⛔ không mơ hồ)* : 4.175
    ô `Date` là CHUỖI                              : 4.193
    ⛔ MƠ HỒ *(cả hai phần ≤ 12)*                   : ⛔ **1.894 = 22,6%**
    ⇒ trải trên                                     : ⛔ **29/60 nguồn**

⭐⭐ **Và phép đo LẬT đúng cái mặc định mà ai cũng sẽ chọn:**

    nguồn suy được thứ tự từ CHÍNH NÓ  : 29/29
    ⛔ nguồn MÂU THUẪN                  : ⛔ 0
    nguồn chắc chắn **`dmy`** (kiểu VN) : ⛔⛔ **0**
    nguồn chắc chắn **`mdy`**           : ⭐ **29/29**
    nguồn trộn cả ngày-số lẫn ngày-chuỗi: ⛔ 0/50 *(⇒ luật `S6` đứng)*

⇒ Một mặc định `dmy` *"vì đây là Việt Nam"* sẽ **hoán ngày↔tháng trên 1.894
  dòng** — đúng lớp lỗi `QĐ-ITL-17` *(93% dòng từng bị hoán, ~181 tỷ sai kỳ)*.
  Các nguồn ấy là **OCBC Singapore** và **TCB USD**: sao kê nước ngoài,
  `mm/dd/yyyy` là **ĐÚNG**.

⭐ Một nguồn ĐỘC LẬP xác nhận: `tools/dung_lai_bank_transactions.py` ghi
  *"chuỗi ở đây là `mm/dd/yyyy` — đọc được từ chính `Bank Transactions`"*. Hai
  phép đo độc lập, cùng kết luận.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, NamedTuple

# ⛔ Cùng lớp chuỗi mà `canon.validate._DMY` nhận — nếu hai biểu thức lệch
#    nhau thì màn hình sẽ **đề xuất cho những dòng mà sổ ⛔ không hề coi là mơ
#    hồ**, và ngược lại. ⇒ Ta ⛔ không viết bản thứ hai: nhập từ đúng chỗ ấy.
from fls.canon.validate import _DMY as _RE_DMY  # noqa: F401

_DMY = _RE_DMY

# Thứ tự hợp lệ — ⛔ KHÔNG chép lại ở đây, nhập từ chỗ khai (`repo.khai_cot`)
# thì sẽ phạm hợp đồng tầng *(`fls.kiem` ⛔ không được biết `fls.repo`)*. ⇒
# khai ở đây, và `repo.khai_cot` **nhập từ đây**.
DMY, MDY = "dmy", "mdy"
THU_TU_HOP_LE = (DMY, MDY)


class BangChung(NamedTuple):
    """Bằng chứng thứ tự ngày của MỘT nguồn. ⛔ Không phải một kết luận.

    ⛔⛔ **Mọi ô đều bắt buộc, kể cả ô `0`.** Một bằng chứng nói *"đề xuất
       `mdy`"* mà ⛔ không nói **đã soi bao nhiêu dòng** là một bằng chứng ⛔
       không đọc được — đúng luật `da_do` của biên bản 9 luật.
    """

    so_dong: int          # tong so dong da soi
    o_so: int             # o `Date` la SO (seri) — ⛔ khong bao gio mo ho
    o_chuoi: int          # o `Date` la chuoi dang d/m/y hay m/d/y
    chac_dmy: int         # >= 1 dong co phan DAU > 12  ⇒ chac chan `dmy`
    chac_mdy: int         # >= 1 dong co phan HAI  > 12  ⇒ chac chan `mdy`
    mo_ho: int            # ca hai phan <= 12 ⇒ ⛔ KHONG doc duoc neu chua khai

    @property
    def mau_thuan(self) -> bool:
        """⛔ Có CẢ hai bằng chứng ⇒ nguồn trộn hai kiểu ngày trong một sheet.

        Đo 08/09: **0/60** nguồn như thế. Nhưng ⛔ không được suy ra là *"⛔
        không thể xảy ra"* — nếu xảy ra thì máy phải **⛔ KHÔNG đề xuất gì**,
        vì lúc ấy ⛔ không có một thứ tự nào đúng cho cả nguồn.
        """
        return bool(self.chac_dmy and self.chac_mdy)

    @property
    def de_xuat(self) -> str | None:
        """`'dmy'` | `'mdy'` | `None`. ⛔ `None` ⛔ KHÔNG phải một mặc định.

        `None` ở đây có nghĩa **⛔ không có bằng chứng nào** *(hoặc bằng chứng
        mâu thuẫn)* ⇒ màn hình phải nói thẳng *"⛔ máy ⛔ không đề xuất được"*,
        ⛔ **không** được lặng lẽ điền `dmy`.
        """
        if self.mau_thuan:
            return None
        if self.chac_mdy:
            return MDY
        if self.chac_dmy:
            return DMY
        return None

    @property
    def can_khai(self) -> bool:
        """Nguồn này **có cần** một bản khai `thu_tu` ⛔ không?

        ⛔ Chỉ khi nó **thật sự có dòng mơ hồ**. Một nguồn toàn ngày-số
        *(21/50 nguồn đo được)* thì `thu_tu` ⛔ **không có nghĩa gì**, và đòi
        kế toán khai nó là bắt họ trả lời một câu ⛔ không tồn tại.
        """
        return self.mo_ho > 0


def do_mot_nguon(o_cua_cac_dong: Iterable[Any]) -> BangChung:
    """Đếm bằng chứng trên các giá trị ô `Date` của MỘT nguồn.

    ⛔ Nhận **giá trị ô**, ⛔ không nhận `dict` dòng — để nó dùng được cho cả
      ảnh chụp *(`fls_chup_dong.o['Date']`)* lẫn một lát thô đọc trực tiếp.
    """
    so = chuoi = dmy = mdy = mo_ho = n = 0
    for v in o_cua_cac_dong:
        n += 1
        # ⛔ `bool` la con cua `int` trong Python ⇒ `True` se lot thanh mot seri.
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            so += 1
            continue
        if not isinstance(v, str):
            continue
        m = _DMY.match(v.strip())
        if not m:
            continue
        chuoi += 1
        a, b, _y = (int(x) for x in m.groups())
        if a > 12:
            dmy += 1
        elif b > 12:
            mdy += 1
        else:
            mo_ho += 1
    return BangChung(so_dong=n, o_so=so, o_chuoi=chuoi,
                     chac_dmy=dmy, chac_mdy=mdy, mo_ho=mo_ho)


def cau_bang_chung(bc: BangChung) -> str:
    """Bằng chứng → một câu cho NGƯỜI đọc. ⛔ Không phải một lời khuyên.

    ⛔⛔ Câu này phải nói ra **con số**, ⛔ không chỉ nói *"nên chọn `mdy`"*.
       Một cái nút kèm lời khuyên mà ⛔ không kèm phép đo là một cái nút sẽ
       được bấm mà ⛔ không ai đọc — và lúc ấy *"người ấn định"* chỉ còn là
       một câu trong tài liệu.
    """
    if not bc.can_khai:
        if bc.o_so and not bc.o_chuoi:
            return ("%d/%d dòng có ô `Date` là SỐ (seri) ⇒ ⛔ không dòng nào "
                    "mơ hồ, ⛔ không cần khai" % (bc.o_so, bc.so_dong))
        return "⛔ 0 dòng mơ hồ trong %d dòng ⇒ ⛔ không cần khai" % bc.so_dong
    if bc.mau_thuan:
        return ("⛔⛔ MÂU THUẪN: %d dòng chắc chắn `dmy` VÀ %d dòng chắc chắn "
                "`mdy` trong cùng một nguồn ⇒ ⛔ máy ⛔ KHÔNG đề xuất được — "
                "một thứ tự cho cả nguồn sẽ làm sai nửa còn lại"
                % (bc.chac_dmy, bc.chac_mdy))
    if bc.de_xuat is None:
        return ("⛔ %d/%d dòng mơ hồ và ⛔ KHÔNG một dòng nào có phần > 12 ⇒ "
                "⛔ máy ⛔ không có bằng chứng nào. Kế toán phải tự biết nguồn "
                "này đọc thế nào" % (bc.mo_ho, bc.so_dong))
    return ("%d dòng chắc chắn `%s` · ⛔ 0 dòng chắc chắn `%s` ⇒ %d dòng mơ hồ "
            "đọc được theo `%s`"
            % (bc.chac_mdy if bc.de_xuat == MDY else bc.chac_dmy, bc.de_xuat,
               DMY if bc.de_xuat == MDY else MDY, bc.mo_ho, bc.de_xuat))
