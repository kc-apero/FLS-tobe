# -*- coding: utf-8 -*-
"""`F04` chặng 2 — **ĐO TRƯỚC KHI VIẾT LUẬT**: một lần nạp thật lộ ra những gì?

⭐⭐ **Vì sao có bước đo này.** Chặng 1 chứng minh FLS dựng ra **ĐÚNG** thứ mà
   cú đẩy đang chở *(8.338/8.338)*. Nhưng *"dựng đúng"* ⛔ **không** phải giá
   trị của chặng 2. Giá trị của chặng 2 là:

       *"FLS bắt được cái gì mà chặng `Run` của trang tính ⛔ KHÔNG bắt?"*

   ⇒ ⛔ **Không được đoán** danh sách ấy rồi viết luật. Phải **đo trước**, rồi
   chỉ viết luật cho những gì **thật sự có mặt** *(`Đ-5`: ⛔ cấm lấp bằng suy
   đoán)*. Bài học `Đ2`: phép kiểm đầu tiên tôi viết ở đó **mã hoá giả định
   của tôi** và báo oan 8 sheet.

⛔ **Công cụ này ⛔ KHÔNG GHI gì cả** — nó chỉ đọc và đếm.

⛔⛔ **`QĐ-ITL-92` — ⛔ KHÔNG đọc cột `Description`.** Đó là cột duy nhất có thể
   mang thông tin cá nhân. Ở đây chỉ đọc **5/6** trường đã khai *(`Date` ·
   `Currency` · `Debit` · `Credit` · `Reference number`)*, và ⛔ **không in ra
   nội dung ô nào** — chỉ in **số đếm** và **hình dạng**.

Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_soat_nap.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.adapters.sao_ke import (TRUONG_DOC_DUOC, chuyen,  # noqa: E402
                                 doc_ban_khai)
from fls.adapters.sao_ke import I_CO, I_MA, I_NGAY, I_NO, I_TE  # noqa: E402
from fls.canon.o_loi import ma_loi_cua  # noqa: E402
from tools.do_bat_bien_ngam import BANK  # noqa: E402
from tools.do_chenh_lech import doc_cot  # noqa: E402
from tools.do_hinh_dang import dong_dau, meta, token  # noqa: E402

# ⛔ `QĐ-ITL-92`: doc 5/6 truong da khai — ⛔ BO `Description`.
#    ⛔ Khai o `sao_ke`, ⛔ khong go lai (mot ban khai cho ca he).
DOC = TRUONG_DOC_DUOC

RE_SERI = re.compile(r"^\d+(\.0+)?$")
RE_NGAY_CHUOI = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")
RE_MA_FLOAT = re.compile(r"^\d+\.0+$")


def _hinh_ngay(x) -> str:
    """Ngay o day mang **hinh dang** nao? ⛔ Khong doi, chi phan loai."""
    if isinstance(x, bool):
        return "bool"
    if isinstance(x, (int, float)):
        return "seri"
    s = str(x).strip()
    if RE_SERI.match(s):
        return "seri-chuoi"          # so seri bi `doc_cot` ep ve chuoi
    if RE_NGAY_CHUOI.match(s):
        return "chuoi mm/dd/yyyy"
    return "khac"


def _co_tien(no, co) -> bool:
    for v in (no, co):
        s = str(v).strip()
        if s and s not in ("0", "0.0"):
            return True
    return False


def main() -> int:
    tok = token()
    d = meta(BANK, tok)
    ten_r = sorted(s["properties"]["title"] for s in d["sheets"]
                   if s["properties"]["title"].startswith("R |"))
    hdr = dong_dau(BANK, ten_r, tok, n=1)

    dem = Counter()
    tong = {"vao": 0, "ra": 0, "rong": 0, "loi": 0}
    hinh_ngay = Counter()
    ngay_theo_sheet: dict[str, Counter] = {}
    ma_float: Counter = Counter()
    ma_rong_co_tien = 0
    khong_tien = 0
    khong_te = 0
    loai_o_loi: Counter = Counter()
    ca_hai_chieu = 0
    khoa: Counter = Counter()

    for t in ten_r:
        d1 = (hdr.get(t) or [[]])[0]
        khai = doc_ban_khai(d1)
        can = sorted({khai[k] for k in DOC if k in khai})
        if not can:
            print("⛔ %s ⛔ khong khai gi" % t)
            return 1
        c = doc_cot(BANK, [(t, i) for i in can], tok,
                    render="UNFORMATTED_VALUE")
        n = max((len(c[(t, i)]) for i in can), default=0)
        hang = [[(c[(t, i)][k] if k < len(c[(t, i)]) else "")
                 if i in can else ""
                 for i in range(max(can) + 1)] for k in range(n)]

        # dem o loi trong VUNG DOC (truoc khi adapter loai)
        for h in hang:
            for i in can:
                m = ma_loi_cua(h[i] if i < len(h) else "")
                if m:
                    loai_o_loi[m] += 1

        # ⛔ Cong cu nay CO Y van doc dong 1: no la phep do tren SHEET,
        #    ⛔ khong phai duong nap. Duong nap doc KHO (`nap_sao_ke`).
        ra, st = chuyen(t, khai, hang, dem)
        for k in tong:
            tong[k] += getattr(st, k)

        cnt = Counter()
        for r in ra:
            cnt[_hinh_ngay(r[I_NGAY])] += 1
            ma = str(r[I_MA]).strip()
            if RE_MA_FLOAT.match(ma):
                ma_float[t] += 1
            no, co = r[I_NO], r[I_CO]
            if not _co_tien(no, co):
                khong_tien += 1
            elif _co_tien(no, "") and _co_tien("", co):
                ca_hai_chieu += 1
            if not ma and _co_tien(no, co):
                ma_rong_co_tien += 1
            if not str(r[I_TE]).strip():
                khong_te += 1
            khoa[(t, str(r[I_NGAY]).strip(), ma,
                  str(no).strip(), str(co).strip())] += 1
        hinh_ngay.update(cnt)
        ngay_theo_sheet[t] = cnt

    trung_that = {k: v for k, v in khoa.items() if v > 1}

    # ── in ra
    W = 74
    print("=" * W)
    print("MOT LAN NAP THAT — %d sheet `R |`" % len(ten_r))
    print("=" * W)
    print("  vao %d → ra %d · rong %d · loi %d   (tong khop: %s)"
          % (tong["vao"], tong["ra"], tong["rong"], tong["loi"],
             "OK" if tong["ra"] + tong["rong"] + tong["loi"] == tong["vao"]
             else "⛔"))

    print()
    print("① HINH DANG NGAY — cung mot cot, nhieu kieu")
    for k, v in hinh_ngay.most_common():
        print("     %-20s %6d dong" % (k, v))
    tron = [t for t, c in ngay_theo_sheet.items() if len(c) > 1]
    print("     ⇒ %d/%d sheet TRON tu 2 kieu ngay tro len"
          % (len(tron), len(ten_r)))

    print()
    print("② MA bi ha xuong kieu `float` (duoi `.0`)")
    print("     %d dong tren %d sheet" % (sum(ma_float.values()), len(ma_float)))
    for t, v in ma_float.most_common(5):
        print("     %-42s %4d" % (t[:42], v))

    print()
    print("③ O LOI trong vung doc")
    if loai_o_loi:
        for m, v in loai_o_loi.most_common():
            print("     %-14s %6d o" % (m, v))
    else:
        print("     (khong co)")

    print()
    print("④ DONG co van de ve NOI DUNG")
    print("     ⛔ khong co tien (No=Co=rong/0) : %d" % khong_tien)
    print("     ⛔ co tien ma ⛔ khong co MA     : %d" % ma_rong_co_tien)
    print("     ⛔ khong co don vi TIEN TE       : %d" % khong_te)
    print("     ghi CA HAI chieu No va Co        : %d" % ca_hai_chieu)

    print()
    print("⑤ MA LAP LAI (Num > 1) — phep chong trung cua AS-IS")
    lap = {m: v for m, v in dem.items() if v > 1}
    print("     %d ma xuat hien >1 lan · %d dong lien quan"
          % (len(lap), sum(lap.values())))
    if lap:
        cao = sorted(lap.items(), key=lambda kv: -kv[1])[:3]
        print("     cao nhat: %s" % ", ".join("×%d" % v for _, v in cao))

    print()
    print("⑥ DONG TRUNG HOAN TOAN (xuat xu+ngay+ma+No+Co) — ⛔ KHONG tinh `Num`")
    print("     %d khoa trung · %d dong lien quan"
          % (len(trung_that), sum(trung_that.values())))
    print("     ⚠ So no dinh cau *'281 dong trung ca SoCT+No+Co+Te'* o `§3`")
    print("       la mot phep dem KHAC — ⛔ khong duoc gop hai con so lam mot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
