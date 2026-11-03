# -*- coding: utf-8 -*-
"""CHỤP vùng CHUẨN của 60 sheet `R |` vào kho *(`QĐ-ITL-110`, task `9c`)*.

⛔⛔ **Vì sao công cụ này tồn tại — và vì sao nó ⛔ KHÔNG phải một cửa HTTP.**

Màn `F04` phải đọc **vùng CHUẨN**, nhưng phép đọc ấy là phép **đọc Google
Sheets**, và tầng cửa ⛔ **không được** làm việc đó: `import-linter` hợp đồng
`1` cấm `fls.api` chạm `psycopg`, hợp đồng `7` cấm nó biết tầng kho. Mở một
đường mạng trong cửa cũng đúng thứ `QĐ-ITL-110` vừa quyết ⛔ không làm.

⇒ Chụp ở **đây**; `F04` đọc **ảnh chụp**. Ai bấm chụp và theo nhịp nào là
  **`GAP-CHUP-01`**, chặn ở owner — ⛔ tôi ⛔ không tự đặt một nhịp.

★ **Nó dùng lại ĐÚNG một đường đọc** *(`nap_sao_ke.doc_vung_chuan`)* — cùng
  đường mà `nap()` của chặng 1/2 đi. Chạy lại cổng chặng 1 sau cú tách:
  **8.365/8.365 = 100,00%**, ⛔ không lệch một dòng ⇒ ảnh chụp chở **đúng thứ**
  đã được chứng minh.

⛔ **Tệp này ⛔ KHÔNG GHI một ô nào về Google Sheets** *(`QĐ-ITL-34`)*.

⛔ `Description` ⛔ **không được đọc** *(`QĐ-ITL-92`)* — `TRUONG_MAC_DINH` là
   **5/6**, và tầng kho **NỔ** nếu ô nào mang nó.

Chạy:
    python tools/chup_sao_ke.py            # CHỈ ĐO — ⛔ không ghi
    python tools/chup_sao_ke.py --that     # ghi một ảnh chụp vào kho THẬT
    python tools/chup_sao_ke.py --that --kho-test
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import psycopg  # noqa: E402

from fls.db.kho import dsn_test, dsn_that  # noqa: E402
from fls.repo import chup as ch  # noqa: E402
from tools.do_bat_bien_ngam import BANK  # noqa: E402
from tools.do_hinh_dang import token  # noqa: E402
from tools.nap_sao_ke import (TRUONG_MAC_DINH, doc_vung_chuan,  # noqa: E402
                              khai_day_du, ten_sheet_r)

LAN = "Bank"          # ⛔ Lằn quỹ chờ `GAP-CANON-02` (khuôn RA 11 cột)


def main() -> int:
    that = "--that" in sys.argv
    dsn = dsn_test() if "--kho-test" in sys.argv else dsn_that()

    tok = token()
    t0 = time.time()
    ten_r = ten_sheet_r(BANK, tok)
    khai = khai_day_du(ten_r, dsn)
    o_theo, _ = doc_vung_chuan(BANK, tok, ten_r, TRUONG_MAC_DINH,
                               {t: b.cot for t, b in khai.items()})
    giay = round(time.time() - t0, 2)

    nguon = {khai[t].source_id: khai[t].version for t in ten_r}
    dong = [(khai[t].source_id, j, o)
            for t in ten_r for j, o in enumerate(o_theo[t])]

    print("=" * 74)
    print("ĐỌC vùng CHUẨN — %d sheet `R |` · %d dòng · %.2f giây"
          % (len(ten_r), len(dong), giay))
    print("    trường đọc: %s   (⛔ ⛔ không `Description` — QĐ-ITL-92)"
          % list(TRUONG_MAC_DINH))

    # ⭐⭐ In ra nguồn đọc được **0 dòng** — chúng là thứ dễ mất nhất, và cũng
    #    là thứ mà `fls_chup_nguon` sinh ra để giữ.
    rong = sorted(t for t in ten_r if not o_theo[t])
    print("    nguồn ra **0 dòng**: %d%s"
          % (len(rong), ("  " + ", ".join(rong[:5])
                         + ("…" if len(rong) > 5 else "")) if rong else ""))

    if not that:
        print()
        print("⛔ CHỈ ĐO — ⛔ không ghi gì. Thêm `--that` để ghi vào kho.")
        return 0

    with psycopg.connect(dsn, autocommit=True) as conn:
        kq = ch.ghi_chup(conn, spreadsheet_id=BANK, lan=LAN,
                         actor="tools/chup_sao_ke.py", giay=giay,
                         nguon=nguon, dong=dong)

    print()
    print("=" * 74)
    print("⭐ ĐÃ GHI ảnh chụp `chup_id = %d`" % kq.chup_id)
    print("    đọc lúc : %s" % kq.doc_luc)
    print("    nguồn   : %d   (trong đó **%d** nguồn ra 0 dòng — ⭐ vẫn CÓ MẶT)"
          % (kq.so_nguon, sum(1 for n in kq.nguon if n.so_dong == 0)))
    print("    dòng    : %d" % kq.so_dong)
    if kq.so_dong != len(dong) or kq.so_nguon != len(nguon):
        print("⛔ LỆCH giữa cái đọc được và cái kho giữ — ⛔ ĐỪNG dùng ảnh này",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
