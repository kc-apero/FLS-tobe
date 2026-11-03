# -*- coding: utf-8 -*-
"""`WO-023` `(i)` — ca dựng trên **kho TEST** cho bài *"lựa chọn ứng viên `F01G`
gắn theo `itl_id`"* *(`BA-06` **v4.22** `§4.5 ⓦ` ⑥ · `KQ-050 F-3`)*.

⭐ Cùng luật `ca_wo045.py`: thân vẽ màn đi ra từ **cửa HTTP thật**; ⛔ một khoá
do bài đặt. Bài cần **một** lệnh `L` *(VND)* và **bốn** dòng tiền mà mỗi dòng
tìm được **riêng** bằng số chứng từ của nó *(ô tìm `/so?q=` lọc `doc_no ILIKE` —
`man_ghep.py:340`)*, và **cùng nhau** bằng chuỗi ngẫu nhiên `h` *(mọi số chứng
từ đều mang `h`)*:

  `M1` VND mã của `L`, lệch **+5.000** *(ngoài dung sai ghép tay ⇒ `L` ⛔
       `tu_chung` ⇒ hiện ở chip `Chưa gán`; bậc `ma` ⇒ hàng **đầu** của
       `itl-candidates`)*
  `M2` VND ⛔ mã, **đúng** số tiền *(bậc `tien` — `Enter` gán được: chiều ĐỎ
       của ca `Enter` cần một hàng khớp đúng tiền)*
  `M3` VND ⛔ mã, lệch **+500** *(trong dung sai `min(1.000 đ; 0,5%)` — cửa ghi
       **nhận**, `KQ-050` ①; ca lệch ⇒ hai bước xác nhận)*
  `M4` USD ⛔ mã ⇒ **⛔** nằm trong `itl-candidates` của `L` *(bài tự chứng —
       `Đ3`)*; chỉ tìm thấy qua `/so` *(bậc `khac_tien_te`)*

  ＋ lệnh thứ hai `L2` *(cùng mã `M1`, lệch +7.000)* — để phím `j`/`k` có lệnh
  kề *(`(h)` `AC-11`)*.

Tiền + mã **ngẫu nhiên** mỗi lần *(kho TEST phình — ⛔ `TRUNCATE`)*. Tiền
`≥ 300.000` ⇒ `0,5%` ≥ `1.500` ⇒ dung sai là `1.000` ⇒ `M3` *(+500)* lọt.

⚠ Ca **nhỏ** *(4 dòng tiền)*, ⛔ thêm dòng `VND` hàng loạt: kho TEST dùng chung
phạm vi `chi_nap_that` cho **mọi** lần nạp ⇒ một bộ lớn ở đây làm lệch bài
khác đếm phân bố `VND` *(`KQ-050 F-4`)*.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm
from tests.web.ca_wo037 import _tien


def dung_ca_wo023(conn) -> dict:
    """Trả `{run, h, lenh, tien, doc, i}` — `doc[k]` số chứng từ dòng tiền
    `k`, `i[k]` `itl_id` của nó *(`k` ∈ `M1`…`M4`)*."""
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T23" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    a = random.randint(300, 899) * 1000
    tien_itl = {"M1": a + 5000, "M2": a, "M3": a + 500,
                "M4": random.randint(100, 899) * 10 + 7}
    doc = {k: f"FT23{k}{h}" for k in tien_itl}
    vnd = "R | 123456789_VPB VND_K23" + h
    usd = "R | 987654321_OCBC USD_K23" + h
    i = {}
    for n, k in enumerate(tien_itl):
        i[k] = _tien(conn, run, usd if k == "M4" else vnd, n + 1,
                     f"{tien_itl[k]}.00", "USD" if k == "M4" else "VND", doc[k])
    lenh = "PL3" + h[:5] + "-1"
    # ⭐ `(h)` `AC-11`: lệnh **thứ hai** `L2` cùng mã `M1` *(lệch +7.000 ⇒ ⛔
    #   tự chứng ⇒ cũng ở chip `Chưa gán`)* — cửa `/queue/lenh-cho` chỉ đọc
    #   lần nạp **mới nhất** *(`mot_lan_nap`; đo 05/10: ca một lệnh ⇒
    #   `ST.dong` **1** hàng)* ⇒ thiếu `L2` thì phím `j`/`k` ⛔ có lệnh kề.
    lenh2 = "PL4" + h[:5] + "-1"
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"),
                 [DongPM(3, lenh.split("-")[0], lenh, D(f"{a}.00"), "VND",
                         "Approve", canon_ref(doc["M1"]), "HD-K23", "C-K23",
                         ref_tho=doc["M1"]),
                  DongPM(4, lenh2.split("-")[0], lenh2, D(f"{a + 7000}.00"),
                         "VND", "Approve", canon_ref(doc["M1"]), "HD-K23",
                         "C-K23", ref_tho=doc["M1"])])
    return {"run": run, "h": h, "lenh": lenh, "lenh2": lenh2, "tien": a,
            "tien_itl": tien_itl, "doc": doc, "i": i}
