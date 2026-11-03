# -*- coding: utf-8 -*-
"""VÁ số trong tài liệu theo **con số MÁY đo** — cặp với `kiem_so_song.py`.

⛔⛔ **Vì sao công cụ này phải tồn tại, và vì sao nó ra đời MUỘN.**

`kiem_so_song.py` *(cổng chung #13)* bắt được **67 phép so** lệch giữa tài liệu
và máy. Nhưng nó chỉ **báo**; việc sửa thì làm **bằng tay**. Đo ngày 08/09: một
đợt code bình thường làm **11 phép so** lệch cùng lúc *(số test · số dòng · hai
chỗ ghim `commit` · `pg_verify` bảng/view · thanh tiến độ…)*.

⛔ **Sửa 11 con số bằng tay là 11 cơ hội gõ sai** — và gõ sai ở đây có một hậu
   quả riêng: cổng sẽ **ĐẠT** *(vì tôi gõ đúng cái máy đo)* trong khi câu văn
   quanh nó ⛔ **không còn đúng**. Đúng lớp lỗi `QĐ-ITL-103`: *một con số đúng
   nằm trong một câu sai*.

★ **Nguyên tắc: ⛔ KHÔNG có bản khai thứ hai.** Tệp này **import** `khai()` và
  `do_may()` của chính cổng, nên nó ⛔ không thể vá một chỗ mà cổng ⛔ không
  canh, và ⛔ không thể canh một chỗ nó ⛔ không vá được.

⛔⛔ **Nó ⛔ KHÔNG sửa CÂU, chỉ sửa SỐ.** Đó là giới hạn thật, khai thẳng:
   cổng canh **CON SỐ**, ⛔ không canh **NGHĨA của con số** *(`GAP-DOC-08`)*.
   Sau khi vá, **vẫn phải đọc lại câu** — một `pg_verify: 23 bảng/view` đúng số
   có thể nằm cạnh chữ *"19 bảng"* ở một câu khác mà máy ⛔ không thấy.

Chạy:
    python tools/va_so_song.py            # CHỈ ĐO — in ra sẽ vá gì, ⛔ không ghi
    python tools/va_so_song.py --that     # ghi vào tài liệu
"""
from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.kiem_so_song import (TAI_LIEU_MAC_DINH, Muc,  # noqa: E402
                                do_may, khai)


def _va_mot(noi_dung: str, m: Muc) -> tuple[str, list[str]]:
    """Thay từng nhóm bắt được bằng giá trị máy. Trả `(nội dung mới, đã đổi)`.

    ⛔ **Thay theo VỊ TRÍ của nhóm, ⛔ không phải `str.replace`.** Một con số
      như `50` xuất hiện hàng chục lần trong một tệp; `replace` sẽ sửa cả những
      chỗ ⛔ không ai đo — tức tự tay tạo ra một cái sai mới ở nơi cổng ⛔ không
      canh.
    """
    khop = list(re.finditer(m.mau, noi_dung))
    if len(khop) != 1:
        return noi_dung, []
    k = khop[0]
    doi: list[str] = []
    # ⛔ Đi từ nhóm CUỐI về ĐẦU: thay từ trước ra sau thì mọi vị trí phía sau
    #   lệch đi đúng bằng độ dài đã đổi.
    for i in range(len(m.gia), 0, -1):
        cu, moi = k.group(i), m.gia[i - 1]
        if cu == moi:
            continue
        a, b = k.span(i)
        noi_dung = noi_dung[:a] + moi + noi_dung[b:]
        doi.append(f"{m.ten} (nhom {i}): `{cu}` → `{moi}`")
    return noi_dung, list(reversed(doi))


def main() -> int:
    that = "--that" in sys.argv
    tai_lieu = TAI_LIEU_MAC_DINH
    may = do_may()
    muc = khai(may, tai_lieu)

    # ⭐ Gom theo FILE rồi vá **một lượt mỗi tệp**: vá từng mục rồi ghi lại
    #   nhiều lần là nhiều cơ hội ghi đè lẫn nhau.
    theo: dict[str, list[Muc]] = {}
    for m in muc:
        theo.setdefault(m.file, []).append(m)

    tong = 0
    for ten in sorted(theo):
        f = tai_lieu / ten
        if not f.exists():
            print("⛔ thieu file %s" % ten)
            continue
        goc = f.read_text(encoding="utf-8")
        s = goc
        doi: list[str] = []
        for m in theo[ten]:
            s, d = _va_mot(s, m)
            doi += d
        if not doi:
            continue
        tong += len(doi)
        print("\n%s — %d cho:" % (ten, len(doi)))
        for d in doi:
            print("   " + d)
        if that:
            f.write_text(s, encoding="utf-8")

    print()
    if not tong:
        print("✅ ⛔ khong co gi phai va — tai lieu dang khop may.")
        return 0
    if that:
        print("⭐ DA VA %d cho. ⛔ Gio DOC LAI CAU quanh moi con so: cong canh"
              " SO, ⛔ khong canh NGHIA (`GAP-DOC-08`)." % tong)
    else:
        print("⛔ CHI DO — ⛔ khong ghi gi (%d cho). Them `--that` de ghi."
              % tong)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
