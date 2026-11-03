# -*- coding: utf-8 -*-
"""Mã tiền tệ để **SO** — **một** tập ký tự trắng, **một** hàm *(`BA-07` v3.11
§4g, `WO-042 (c)`)*.

⛔⛔ **Bia `KQ-041 F-2`** *(`fls-test` 05/10, PG thật)*: phép so tiền tệ sống ở
**bốn** tập ký tự trắng khác nhau — Python `str.strip()` **29** *(`ma_tien_te`
＋ **6** bản viết tay, kể cả cửa GHI `ghep_lenh`)* · SQL `btrim(…, E' \\t\\r\\n')`
**4** *(`lenh_cho._SQL_ITL_UNG_VIEN` + `_SQL_DEM_CUNG_TE`)* · JS `String.trim()`
**25** *(`TP.tien` + `TP.ma_te`)*. Sáu chuỗi biên *(NBSP `U+00A0` · `\\v` · `\\f`
· `U+3000` · khoảng trắng hẹp · `U+0085` ở mép mã)* ⇒ SQL giữ nguyên, Python ra
mã sạch — lệch **6 / 6**: một dòng `curr = '\\xa0VND'` ⛔ mã khớp thì rổ
*(Python)* coi là VND mà ba bậc tiền *(SQL)* ⛔ bao giờ hiện nó. Sổ thật 05/10
**0** ca *(`fls_itl.curr` ngoài `^[A-Z]{3}$` **0 / 8.387**)* ⇒ sửa vì **một
luật**, ⛔ vì báo động.

⭐ Luật v3.11: tập **`TAP_TRANG_TIEN_TE`** = mọi `c` có `c.isspace()` ở Python
  *(**29**)* ＋ **`U+FEFF`** *(BOM — thứ hay dính nhất khi chép từ CSV / Sheets;
  JS đã gỡ, Python chưa)* = **30**. ⛔ `U+200B` *(khoảng trắng độ rộng 0 — cả ba
  ngôn ngữ hôm nay đều ⛔ gỡ; giữ thế)*. Chữ hoa ⛔ đổi *(`.upper()` / PG
  `upper()` / JS `toUpperCase()` khác nhau ngoài ASCII — sổ thật `curr` ngoài
  `[A-Z0-9]` **0** ⇒ ngoài phạm vi)*.

⭐ Vì sao ở `fls.canon` *(⛔ `fls.repo.man_ghep` như trước)*: `fls.adapters`
  *(`pm_join._cur`)* cũng so tiền tệ, mà hợp đồng nhập số 6 cấm `adapters` biết
  `repo` ⇒ tập phải nằm ở tầng **dưới** cả hai. `canon` là tầng dưới cùng của
  nghiệp vụ *(chuẩn hoá hình dạng dữ liệu)* và ⛔ phụ thuộc gì *(hợp đồng 3)*.
  `fls.repo.man_ghep.ma_tien_te` giữ làm **tên cũ trỏ về đây** — ⛔ bản thứ hai.

Ba vế đọc **cùng** hằng này:
  · Python — `ma_tien_te` *(mọi phép so tiền tệ trong `fls/`)*;
  · SQL — `upper(btrim(i.curr, %(tap)s))`, tham số `tap` = hằng này *(⛔ gõ lại
    chuỗi trong SQL)*;
  · JS — `TP.TAP_TRANG_TIEN_TE` *(`thanh_phan.js`)* là **bản chép** — trình
    duyệt ⛔ nhập được Python; bài `tests/web/test_wo042_mot_tap_ky_tu_trang.py`
    so hai tập **từng ký tự** ⇒ chép lệch một ký tự là ĐỎ.
"""
from __future__ import annotations

from typing import Any

#: ⭐ **30** ký tự, liệt kê **tường minh** theo điểm mã *(⛔ sinh bằng
#: `isspace()` lúc chạy: bảng Unicode của Python đổi theo phiên bản thì tập
#: lặng lẽ đổi theo, còn bản chép JS thì ⛔)* — bài thử so với
#: `{c : c.isspace()} ∪ {U+FEFF}` để biết khi nào hai thứ ấy rời nhau.
#: ⚠ Viết bằng **số điểm mã**, ⛔ bằng ký tự chép vào nguồn: 22 / 30 ký tự
#: này **vô hình** trong trình soạn thảo *(NBSP, BOM, khoảng trắng hẹp…)* —
#: một ký tự trắng gõ thẳng vào chuỗi là một ký tự ⛔ ai đọc được khi rà mã.
TAP_TRANG_TIEN_TE = "".join(map(chr, (
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D,          # tab…CR          (5)
    0x001C, 0x001D, 0x001E, 0x001F,                  # FS GS RS US     (4)
    0x0020,                                          # space           (1)
    0x0085,                                          # NEL             (1)
    0x00A0,                                          # NBSP            (1)
    0x1680,                                          # OGHAM           (1)
    0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005,  # EN QUAD…
    0x2006, 0x2007, 0x2008, 0x2009, 0x200A,          # …HAIR SPACE     (11)
    0x2028, 0x2029,                                  # dòng · đoạn     (2)
    0x202F,                                          # NNBSP           (1)
    0x205F,                                          # MMSP            (1)
    0x3000,                                          # IDEOGRAPHIC     (1)
    0xFEFF,                                          # BOM             (1) ⇒ 30
)))


def ma_tien_te(c: Any) -> str:
    """Mã tiền tệ để **SO** — gỡ `TAP_TRANG_TIEN_TE` ở hai mép + chữ hoa.
    ⛔ `None` / rỗng ⇒ `''`.

    ⭐ Một chỗ cho **mọi** phép so tiền tệ: rổ `xep_ro` · bậc `ma` · `lech`
      khuôn `⓵` · cổng tự chứng `ds_tu_chung` · cửa ghi `ghep_lenh` · ứng viên
      `/so` · `pm_join._cur`. So có gỡ ký tự X ở chỗ này mà ⛔ ở chỗ kia là
      **hai luật** *(`WO-032` Rủi ro 2 · `KQ-036 F-1` · `KQ-041 F-2`)*.
    """
    return str(c or "").strip(TAP_TRANG_TIEN_TE).upper()
