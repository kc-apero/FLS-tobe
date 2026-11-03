# -*- coding: utf-8 -*-
"""`F04` chặng 2 — **CỔNG SOÁT MỘT LẦN NẠP**, đo trên nguồn SỐNG.

⭐⭐ **Đây là thứ kế toán ⛔ KHÔNG có hôm nay.** Chặng `Run` của trang tính gom
   60 sheet lại và ⛔ **không nói gì cả**: dòng hỏng vẫn vào, mã bị hạ kiểu vẫn
   vào, trùng vẫn vào. Cổng này chạy **8 luật** *(`fls/kiem/soat_nap.py`)* trên
   **chính lô dữ liệu vừa nạp**, ⛔ không phải trên sheet — nên nó trả lời được
   câu *"lô này có sạch ⛔ không?"* **TRƯỚC** khi có ai bấm đẩy.

⛔⛔ **Ba hạng — và ⛔ ĐỪNG đọc nhầm nó thành nới cổng** *(`R-A5`)*:
     `CHAN` = **lỗi của FLS** ⇒ đỏ **và chặn** *(mã thoát ≠ 0)*.
     `CO`   = **khuyết tật có sẵn trong sổ kế toán** ⇒ đỏ, **báo to**, ⛔ không
              chặn — vì những dòng ấy là **tiền thật**, vứt đi là vi phạm
              *"⛔ 0 dòng rơi im lặng"*; chúng thuộc về **hàng chờ có lý do**.
     `CANH` = hiện sạch, giữ để bắt trôi.

⛔ Công cụ này ⛔ **KHÔNG GHI** gì cả. Cú ghi thật là chặng 3, và chặng 3
   **chặn ở owner** *(`GAP-PLAN-05`)*.

Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/soat_nap_sao_ke.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.kiem import soat_nap as sn  # noqa: E402
from tools.do_bat_bien_ngam import BANK, cot  # noqa: E402
from tools.do_hinh_dang import token  # noqa: E402
from tools.nap_sao_ke import nap, ten_sheet_r  # noqa: E402

# `BankAccountList` cot 3 = ten sheet `R |` ma danh muc khai (`QĐ-ITL-101`).
DM_SHEET, DM_COT_TEN, DM_VUNG = "BankAccountList", 3, "'BankAccountList'!A3:V"

BIEU = {sn.CHAN: "CHAN", sn.CO_: "CO  ", sn.CANH: "CANH"}


def danh_muc(tok: str) -> set[str]:
    v = cot(BANK, DM_VUNG, tok, "UNFORMATTED_VALUE")
    c = v[DM_COT_TEN] if DM_COT_TEN < len(v) else []
    return {str(x).strip() for x in c if str(x).strip()}


def main() -> int:
    tok = token()
    ten_r = ten_sheet_r(BANK, tok)
    # ⛔ Doc danh muc **TRUOC** lot nap lon. Lan chay dau tien no dung sau, va
    #    `429` giet dung no ⇒ mat luon `S8` sau khi da tra gia doc ca 60 sheet.
    #    Viec re va co the hong thi lam **truoc** viec dat.
    dm = danh_muc(tok)
    rows, theo, _ = nap(BANK, tok, ten_r)

    kq = [
        sn.s1_ba_duong_can(theo),
        # ⛔ Truyen tap sheet DA NAP (`theo` co du 60), ⛔ KHONG suy tu `rows`:
        #    sheet ra 0 dong van phai bi soi (xem docstring `s8`).
        sn.s8_xuat_xu_co_trong_danh_muc(set(theo), dm),
        sn.s2_co_tien_thi_phai_co_ma(rows),
        sn.s3_moi_dong_phai_co_tien(rows),
        sn.s4_moi_dong_phai_co_tien_te(rows),
        sn.s7_dong_trung_hoan_toan(rows),
        sn.s5_ma_khong_bi_ha_kieu(rows),
        sn.s6_mot_sheet_mot_kieu_ngay(rows),
    ]

    W = 74
    # ⚠ `S6` bao "50 sheet" trong khi nap 60 — ⛔ ĐỪNG de con lech ay im lang:
    #    10 sheet ra **0 dong** = tai khoan da mo ma chua dung. ⛔ Khong phai
    #    loi (cung ly do voi `L2` cua cong #17), nhung phai NOI RA, vi mot
    #    con so tut tu 60 xuong 50 ma khong ai giai thich thi lan sau se bi
    #    doc nham thanh "mat 10 sheet".
    rong = sorted(t for t, x in theo.items() if x[1] == 0)

    print("=" * W)
    print("`F04` CHANG 2 · SOAT MOT LAN NAP — %d sheet · %d dong"
          % (len(ten_r), len(rows)))
    print("   (%d sheet ra 0 dong = tai khoan da mo chua dung ⇒ %d sheet "
          "co mat trong phep dem theo-sheet)" % (len(rong), len(ten_r) - len(rong)))
    print("=" * W)
    for k in kq:
        print("%-4s %-5s %-46s %s"
              % (BIEU[k.hang], "OK" if k.xanh else "⛔ ⛔",
                 k.ten[:46], k.thong_diep))

    chan = sn.chan_lai(kq)
    co = [k for k in kq if k.hang == sn.CO_ and not k.xanh]
    canh = [k for k in kq if k.hang == sn.CANH and not k.xanh]

    print()
    if chan:
        print("⛔⛔ CHAN — **loi cua FLS**, lo nay ⛔ KHONG duoc di tiep:")
        for k in chan:
            print("     · %s" % k.ten)
    else:
        print("✅ ⛔ KHONG co loi nao CUA FLS — lo nay nap SACH.")

    if co:
        print()
        print("⛔ CO — **khuyet tat co san trong so ke toan** (⛔ khong chan):")
        for k in co:
            print("     · %s" % k.thong_diep)
        print("   ⇒ Nhung dong nay la TIEN THAT ⇒ vao **hang cho co ly do**,")
        print("     ⛔ KHONG duoc bo. Va sua la viec cua **ke toan**.")

    if canh:
        print()
        print("⚠ CANH — guard vua troi, xem ngay:")
        for k in canh:
            print("     · %s" % k.thong_diep)

    print()
    print("Tong: %d/%d luat xanh · CHAN %d · CO %d · CANH %d"
          % (sum(1 for k in kq if k.xanh), len(kq),
             len(chan), len(co), len(canh)))
    return 1 if chan else 0


if __name__ == "__main__":
    sys.exit(main())
