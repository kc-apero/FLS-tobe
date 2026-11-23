# -*- coding: utf-8 -*-
"""Khuôn `Bank Transactions` *(10 cột)* → **ITL-CANON 38 vị trí**.

⭐⭐ **Vì sao có tệp này, và vì sao nó MỎNG đến thế.** Đường nạp `F04` phải đổ
   vào **cùng một** phép ghi với đường cũ *(`fls/repo/chay_nap.py`)* — vì phép
   ghi ấy đang giữ **ba thứ ⛔ không được có bản thứ hai**:

     ⓐ **chống trùng** bằng `content_key` *(`BA-07` §4b ⓹ nói thẳng: ⛔ không
        dựng cơ chế chống trùng thứ hai — hai cơ chế là hai chỗ để lệch nhau)*;
     ⓑ **cổng bốn đường** *(`vào = sổ + loại + rỗng + trùng`)*, kiểm **TRƯỚC**
        khi ghi;
     ⓒ **MỘT giao dịch** cho cả lần nạp.

   ⇒ Việc của tệp này ⛔ **không phải** *"ghi dòng sao kê vào sổ"* — mà là
     **đưa dòng sao kê về đúng hình dạng** để phép ghi ấy nhận. Mọi thứ khác
     nó ⛔ **không làm**.

⛔⛔ **Và nó ⛔ KHÔNG bịa một ô nào.** Sao kê ngân hàng có **6 trường**; canon
   có **38 vị trí**. **32 vị trí còn lại để TRỐNG** — ⛔ không mặc định, ⛔ không
   suy. Đó chính là cơ chế đẻ ra **6.843 ô *"Input here"*** của AS-IS
   *(`GAC-Other`/`Headquarters2`)*: một giá trị mặc định im lặng, sai mà ⛔ không
   ai thấy. Ở đây trống ⇒ `work_status='UNMAPPED'` ⇒ **vào hàng chờ**, tức
   **có người phải trả lời**.

⚠ **`Description` có thể TRỐNG, và đó ⛔ không phải lỗi.** Bộ đọc `R |` của ta
  ⛔ cố ý không đọc trường ấy *(`QĐ-ITL-92` — trường duy nhất có thể mang thông
  tin cá nhân)*. Đường tải tệp thật thì có. ⇒ Hàm này nhận **cả hai**, và ⛔
  không coi thiếu `Description` là dòng hỏng.
"""
from __future__ import annotations

from typing import Any, Iterable, Sequence

# ⭐ `ThongKe` lay tu `adapters/bank` — CUNG mot lop, ⛔ khong dinh nghia
#    mot lop ba-duong thu hai. `chay_nap.chay()` goi `tk.can()` cua no, va hai
#    lop giong nhau y het la hai cho de chung troi khoi nhau.
from fls.adapters.bank import ThongKe
from fls.adapters.sao_ke import (I_CO, I_MA, I_MOTA, I_NGAY, I_NO, I_TE,
                                 KHUON_RA)
from fls.canon.o_loi import la_o_loi
from fls.canon.row import SO_VI_TRI, CanonRow

# ⭐ **MỘT** bản khai vị trí. Nguồn: `03_Dev/04_DB_IMPLEMENTATION` §3 —
#    `A(0)` Ngày chứng từ · `B(1)` Số chứng từ · `C(2)` Diễn giải ·
#    `D(3)` Đơn vị tiền tệ · `E(4)` PS Nợ · `F(5)` PS Có.
#    ⛔ Khai ở đây MỘT lần; ⛔ không ai gõ lại một bộ chỉ số thứ hai.
DO_VAO_CANON: tuple[tuple[int, int], ...] = (
    (0, I_NGAY),      # A  Ngày chứng từ   ← Transaction date
    (1, I_MA),        # B  Số chứng từ     ← Reference number
    (2, I_MOTA),      # C  Diễn giải       ← Description  (có thể TRỐNG)
    (3, I_TE),        # D  Đơn vị tiền tệ  ← Currency
    (4, I_NO),        # E  PS Nợ           ← Debit
    (5, I_CO),        # F  PS Có           ← Credit
)

# Cột nào của sao kê mà là **ô lỗi** thì dòng ấy bị LOẠI *(có lý do CÓ TÊN)*.
# ⛔ Chỉ hai cột này, và đúng hai cột `sao_ke.chuyen()` đã canh — ⛔ không nới
#    ra, ⛔ không thu lại: hai chỗ canh khác nhau thì một dòng sẽ bị loại ở
#    tầng này và được giữ ở tầng kia.
COT_LOI_LA_LOAI: tuple[int, ...] = (I_NGAY, I_MA)


def dung_canon(hang: Sequence[Any]) -> tuple[CanonRow | None, list[str]]:
    """Một dòng khuôn `Bank Transactions` → `(CanonRow, lý do loại)`.

    ⛔ **Không đổi một giá trị nào** — cùng luật với `adapters/bank.py`: mọi
    phép làm sạch ở đây là một chỗ đối chiếu có thể đỏ vì **lỗi của ta**, ⛔
    không phải lỗi của sổ.
    """
    ly_do: list[str] = []
    for i in COT_LOI_LA_LOAI:
        v = hang[i] if i < len(hang) else None
        if la_o_loi(v):
            ly_do.append("cot %r la o loi: %s" % (KHUON_RA[i], v))
    if ly_do:
        return None, ly_do

    o: list[Any] = [None] * SO_VI_TRI
    for pos, i in DO_VAO_CANON:
        v = hang[i] if i < len(hang) else None
        # ⛔ Ô lỗi ở cột ⛔ không-phải-khoá ⇒ `None` CÓ KIỂM SOÁT (`R-ORA-07a`),
        #    ⛔ không loại cả dòng và cũng ⛔ không chở chuỗi `#REF!` vào sổ.
        o[pos] = None if (v is None or la_o_loi(v) or str(v).strip() == "") else v
    return CanonRow.from_list(o), []


def nap(tho: Iterable[Sequence[Any]], header: Sequence[Any] | None = None
        ) -> tuple[list[tuple[int, CanonRow]], list[tuple[int, list[str]]],
                   ThongKe]:
    """Cả lô khuôn `Bank Transactions` → `(dòng canon, dòng bị loại, ba đường)`.

    ⭐ Chữ ký **y hệt** `adapters/bank.nap` — đó là điều kiện để `chay_nap.chay`
      dùng được **cả hai** mà ⛔ không phải biết mình đang chạy lằn nào.

    ⚠ `header` nhận vào nhưng ⛔ **không dùng**: lô này ⛔ không đến từ một
      sheet có hàng tiêu đề — nó đã qua `sao_ke.chuyen()`, nơi hình dạng **đã
      được bản khai ánh xạ cưỡng chế**. Giữ tham số để hai bộ nạp thay nhau
      được; ⛔ **không** bịa ra một phép kiểm tiêu đề thứ hai.

    ⛔ `source_row` ở đây là **chỉ số trong LÔ** *(1-based)*, ⛔ không phải số
      dòng của một trang tính — lô đến từ **một tệp tải lên**, và tệp thì ⛔
      không có *"dòng 5 của sheet"*. Cặp `(source_sheet, source_row)` vẫn là
      một khoá lineage đọc được: *"dòng thứ N của lô nạp từ nguồn ấy"*.
    """
    ra: list[tuple[int, CanonRow]] = []
    loai: list[tuple[int, list[str]]] = []
    vao = rong = 0
    for i, hang in enumerate(tho, start=1):
        vao += 1
        ngay = hang[I_NGAY] if I_NGAY < len(hang) else None
        if ngay is None or str(ngay).strip() == "":
            rong += 1          # đệm của trang tính, ⛔ không phải một dòng
            continue
        row, ly_do = dung_canon(hang)
        if row is None:
            loai.append((i, ly_do))
            continue
        ra.append((i, row))
    return ra, loai, ThongKe(vao=vao, ra=len(ra), rong=rong, loai=len(loai))
