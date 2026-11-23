# -*- coding: utf-8 -*-
"""`F04` chặng 1 — **FLS tự dựng `Bank Transactions` từ 60 sheet `R |`**,
rồi **so từng dòng** với bản sheet đang chạy.

⭐⭐ **Đây là phép chứng minh của `QĐ-ITL-100`.** Owner chốt *FLS thay CÚ ĐẨY*.
   Muốn thay được thì FLS phải **dựng ra đúng thứ** mà cú đẩy đang chở. Công cụ
   này ⛔ không ghi gì cả — nó chỉ **dựng và so**, để trả lời một câu:

       *"FLS có dựng lại được `Bank Transactions` KHÔNG SAI MỘT DÒNG không?"*

⛔ **Đọc cả hai bên bằng CÙNG một cách** *(`UNFORMATTED_VALUE`)*. Bài học `Đ3`:
   đọc một bên đã-định-dạng và một bên thô thì sinh **1.468 dòng lệch GIẢ**.

⛔ Công cụ này ⛔ **KHÔNG GHI** vào bất cứ trang tính nào. Ghi thật là việc
   riêng, cần owner duyệt riêng.

Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/dung_lai_bank_transactions.py
"""
from __future__ import annotations

import datetime
import re
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.adapters.sao_ke import KHUON_RA  # noqa: E402
from tools.do_bat_bien_ngam import BANK  # noqa: E402
from tools.do_chenh_lech import doc_cot  # noqa: E402
from tools.do_hinh_dang import token, ty_le  # noqa: E402
from tools.nap_sao_ke import nap, ten_sheet_r  # noqa: E402

GOP = "Bank Transactions"
I = {c: k for k, c in enumerate(KHUON_RA)}


GOC_NGAY = datetime.date(1899, 12, 30)


def _ngay(x) -> str:
    """Đưa ngày về **một** cách viết, dù nguồn ghi kiểu nào.

    ⛔⛔ **Đây là một PHÉP BIẾN ĐỔI THẬT mà sheet đang làm, ⛔ không phải mẹo so
    sánh.** Đo được: một phần các sheet `R |` giữ ngày là **số sê-ri**, phần
    còn lại giữ là **CHUỖI** *(`07/28/2026`)*; `Bank Transactions` **chuẩn hoá
    hết về ngày**. ⇒ `F04` **phải làm y hệt**, nếu không thì `~5.369` dòng ngày
    chuỗi sẽ trôi *(đúng lớp lỗi đã ghi ở `ITL Ledge`)*.

    ⚠ Chuỗi ở đây là **`mm/dd/yyyy`** — đọc được từ chính `Bank Transactions`
    *(`09/06/2026` = 6 tháng 9)*. ⛔ Không đoán `dd/mm`: sổ này đã có tiền lệ
    **hoán ngày↔tháng** trên 93% dòng, nên đoán sai thứ tự là **sai kỳ**.
    """
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, float)) and x:
        return str(GOC_NGAY + datetime.timedelta(days=int(x)))
    s = str(x).strip()
    # ⛔⛔ `doc_cot` **ép mọi ô về chuỗi** ⇒ một số sê-ri về đây dưới dạng
    #    `"45586"`. Đã vấp đúng bẫy này hai lần *(`Num` ở cổng #17, và ngay ở
    #    đây)*. ⇒ chuỗi toàn chữ số **cũng là** sê-ri.
    if re.match(r"^\d+(\.0+)?$", s):
        return str(GOC_NGAY + datetime.timedelta(days=int(float(s))))
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        thang, ngay, nam = (int(v) for v in m.groups())
        try:
            return str(datetime.date(nam, thang, ngay))
        except ValueError:
            return s
    return s


DEM_MA_FLOAT = Counter()


def _ma(x) -> str:
    """Mã đối sánh. ⛔ Bỏ đuôi `.0` — **và đó ⛔ KHÔNG phải một dung sai.**

    ⛔⛔ Đo được ở `Đ4-a`: **31** mã ở `Bank Transactions` bị lưu kiểu `float`
    *(`4366185033872500.0`)* trong khi sheet `R |` giữ đúng **số nguyên**.
    Tức là **phép nạp của trang tính đang LÀM HỎNG mã**, và bản FLS dựng ra
    **trung thực hơn** bản đang chạy. ⇒ Chuẩn hoá ở đây để phép so nói đúng
    điều nó muốn nói; con số bị chạm được **đếm và báo ra**, ⛔ không giấu.
    """
    s = str(x).strip()
    if re.match(r"^\d+\.0+$", s):
        DEM_MA_FLOAT[s] += 1
        return s.split(".")[0]
    return s


def _tien(x) -> str:
    """Tiền về **MỘT** cách viết, dù nguồn trả số hay chuỗi.

    ⛔⛔ **Bản trước của hàm này KHÔNG ĐỐI XỨNG, và nó chỉ đúng vì một sự tình
       cờ.** Nó viết:

           if not isinstance(x, (int, float)): return str(x).strip()
           return "%.2f" % round(float(x), 2)

       ⇒ số `1240000000` ra `"1240000000.00"`, còn chuỗi `"1240000000"` ra
       `"1240000000"` — **hai khoá khác nhau cho CÙNG một số tiền**.

    ⭐ Nó **chưa bao giờ cắn**, vì `doc_cot` ép **cả hai vế** về chuỗi ⇒ nhánh
      số ⛔ không bao giờ chạy. Ngày 08/09, khi lằn ảnh chụp đọc **ô thô**
      *(`tho=True`)*, một vế thành số và cổng tụt từ **100,00% xuống 24,87%**
      — một phép so **báo oan trên 6.285 dòng đúng**.

    ⇒ Bài học: **một cổng so hai vế mà chuẩn hoá hai vế bằng hai luật khác
      nhau là một cổng ⛔ chưa biết nó đo gì.** Nó xanh vì hai vế cùng hình,
      ⛔ không vì hai vế cùng giá trị.

    ⛔⛔ **RỖNG ⛔ KHÔNG được thành `0.00`** — và đây ⛔ không phải chi tiết nhỏ.
       `QĐ-ITL-83` ghi một **lỗi TIỀN thật trên 3.630/10.030 dòng (36%)** đúng
       vì ai đó coi *"ô ⛔ không rỗng"* là *"có tiền"*, mà số `0` thì ⛔ không
       rỗng. Ở đây là chiều ngược lại: *ô rỗng* và *số 0* là **hai sự thật
       khác nhau**, và một phép so gộp chúng sẽ **giấu** chỗ sheet ghi `0`
       trong khi nguồn để trống.
    """
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, float)):
        return "%.2f" % round(float(x), 2)
    s = str(x).strip()
    if s == "":
        return ""
    try:
        return "%.2f" % round(float(s), 2)
    except ValueError:
        return s


def _khoa(ngay, ma, nguon, no, co) -> tuple:
    """Khoá so sánh. ⛔ Làm tròn tiền về 2 số lẻ — ⛔ không so `float` trần."""
    return (_ngay(ngay), _ma(ma), str(nguon).strip(),
            _tien(no), _tien(co))


def main() -> int:
    tok = token()
    ten_r = ten_sheet_r(BANK, tok)

    # ── 1 · FLS dựng
    # ⭐ Đường nạp nay dung CHUNG voi chang 2 (`tools/nap_sao_ke.py`) — hai
    #    duong nap rieng thi chang 2 se soat mot thu ⛔ khong phai thu chang 1
    #    da chung minh, va cai lech ay se im lang.
    fls, theo, _ = nap(BANK, tok, ten_r)
    tk = {"vao": 0, "ra": 0, "rong": 0, "loi": 0}
    for t in ten_r:
        vao, ra_, rong, loi = theo[t]
        tk["vao"] += vao
        tk["ra"] += ra_
        tk["rong"] += rong
        tk["loi"] += loi

    print("=" * 74)
    print("1 · FLS DỰNG từ %d sheet `R |`" % len(ten_r))
    print("    vào %d dòng → ra **%d** · rỗng %d · lỗi %d   (tổng khớp: %s)"
          % (tk["vao"], tk["ra"], tk["rong"], tk["loi"],
             "✅" if tk["ra"] + tk["rong"] + tk["loi"] == tk["vao"] else "⛔"))

    # ── 2 · sheet đang chạy
    cols = [(GOP, i) for i in range(7)]
    g = doc_cot(BANK, cols, tok, render="UNFORMATTED_VALUE")
    n = max(len(g[(GOP, i)]) for i in range(7))

    def o(i, k):
        v = g[(GOP, i)]
        return v[k] if k < len(v) else ""

    that = [_khoa(o(0, k), o(5, k), o(6, k), o(3, k), o(4, k))
            for k in range(n) if str(o(0, k)).strip()]
    minh = [_khoa(r[I["Transaction date"]], r[I["Reference number"]],
                  r[I["Source"]], r[I["Debit"]], r[I["Credit"]]) for r in fls]

    print()
    print("=" * 74)
    print("2 · SO TỪNG DÒNG với `%s` đang chạy" % GOP)
    print("    sheet đang chạy : %d dòng" % len(that))
    print("    FLS dựng ra     : %d dòng" % len(minh))
    a, b = Counter(that), Counter(minh)
    thieu, thua = a - b, b - a
    print("    ⛔ sheet CÓ, FLS ⛔ không : %d" % sum(thieu.values()))
    print("    ⛔ FLS CÓ, sheet ⛔ không : %d" % sum(thua.values()))
    khop = sum((a & b).values())
    print("    ⭐ KHỚP                  : %d  (%.2f%%)"
          % (khop, ty_le(khop, max(len(that), 1), 0.0, 100.0, "khop")))
    for nhan, ds in (("sheet CÓ, FLS ⛔ không", thieu),
                     ("FLS CÓ, sheet ⛔ không", thua)):
        for k, v in list(ds.items())[:5]:
            print("       ⛔ %-22s %s ×%d" % (nhan, k[:3], v))

    if DEM_MA_FLOAT:
        print()
        print("    ⚠ %d mã bị trang tính lưu kiểu `float` (đuôi `.0`) — bản FLS"
              % sum(DEM_MA_FLOAT.values()))
        print("      dựng ra **trung thực hơn** bản đang chạy (`Đ4-a`).")

    if not thieu and not thua:
        print()
        print("⭐⭐⭐ FLS dựng lại `%s` ⛔ KHÔNG SAI MỘT DÒNG NÀO." % GOP)
        print("     ⇒ `F04` chặng 1 **thay được** chặng `Run` + cú đẩy.")
        return 0
    print()
    print("⛔ ⛔ chưa khớp hết — ⛔ chưa được thay cú đẩy.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
