# -*- coding: utf-8 -*-
"""`WO-045` — ca dựng chung trên **kho TEST** cho bài màn `tests/web/test_wo045_*`
*(cùng luật `ca_wo032.py` / `ca_wo037.py` / `ca_wo042.py`: thân vẽ màn đi ra từ
**cửa HTTP thật**; ⛔ một khoá do bài đặt)*.

⭐ Phiếu này đổi **lượt nào được vẽ** *(`BA-06` v4.19 `§4.5 ⓦ` ①)* và **nút nào
bị khoá thừa** ở chế độ chỉ đọc *(② )* — nên ca cần hai thứ mà các ca trước
⛔ có:

  ⓐ **hai lệnh có hai tập ứng viên RỜI nhau** *(`A` USD ↔ `B` VND)* — để một
     ứng viên của lệnh trước lọt xuống dưới lệnh đang mở là **thấy được tên
     nó** *(`itl_id` chỉ có ở `A`)*, ⛔ chỉ thấy tổng lệch. Bài kiểm tập rời
     **trước** khi tin *(`Đ3`)*.
  ⓑ **một rổ dài hơn MỘT trang** `limit=50` của `F01L` *(`khong`: **55** lệnh
     mang số chứng từ ⛔ dòng tiền nào mang)* — để `Xem thêm` có trang kế thật
     *(`next_cursor` do **cửa** cấp, ⛔ bài bịa)*.

Ngoài ra: `N` ⛔ số chứng từ ⇒ rổ `nguoi` *(rổ thứ hai của `AC-4`)* · `T` khớp
đúng mã + tiền ⇒ **tự chứng** *(để nút `Ghép N dòng tự chứng` của `F01` ⛔ bị
khoá vì `0 dòng` — `AC-6` phải thấy nó khoá vì **chỉ đọc**)*.

Tiền + mã **ngẫu nhiên** mỗi lần *(kho TEST phình — ⛔ `TRUNCATE`)*.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm
from tests.web.ca_wo037 import _tien

#: số lệnh rổ `khong` — **> 50** *(trang `F01L`)* để có đúng hai trang
SO_KHONG = 55


def dung_ca_wo045(conn) -> dict:
    """Một lần nạp *(kho TEST)*:

      `A` USD mã `cA` ↔ dòng **USD** mã `cA`, lệch **+50%** *(ngoài dung sai ⇒
          rổ `may` ⛔ tự chứng ⇒ chip `Chưa gán`)*
      `B` VND mã `cB` ↔ dòng **VND** mã `cB`, lệch **+5.000** *(như trên)*
      `N` VND ⛔ số chứng từ ⇒ rổ `nguoi`
      `T` VND mã `cT` ↔ dòng VND mã `cT` **đúng** số tiền ⇒ rổ `may` **tự chứng**
      `K00`…`K54` VND mang mã ⛔ dòng tiền nào mang ⇒ rổ `khong` *(55 > 50)*

    Trả `{run, h, doc, lenh, tien, i, khong}`; `doc` = số chứng từ **dòng
    tiền** *(`AC-3` gõ chúng vào ô tìm)*.
    """
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T45" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    tien = {k: random.randint(1_000, 8_999) * 100 + i
            for i, k in enumerate("ABNT")}
    doc = {"A": "FT45A" + h, "B": "FT45B" + h, "N": None, "T": "FT45T" + h}
    vnd = "R | 123456789_VPB VND_K45" + h
    usd = "R | 987654321_OCBC USD_K45" + h
    i = {}
    i["A"] = _tien(conn, run, usd, 1, f"{tien['A'] * 3 // 2}.00", "USD", doc["A"])
    i["B"] = _tien(conn, run, vnd, 2, f"{tien['B'] + 5000}.00", "VND", doc["B"])
    i["T"] = _tien(conn, run, vnd, 3, f"{tien['T']}.00", "VND", doc["T"])
    # ⓒ ⚠ *(đính chính `WO-023` `(j)` — `KQ-050 F-4`)* ~~lằn **dòng tiền**
    #   `F01` chỉ hỏi lần nạp **mới nhất**~~ — **sai**: cửa `/queue` đọc
    #   `chi_nap_that` = **mọi** lần nạp `NAP-yyyy-mm-dd-…` *(`pham_vi.py:80`,
    #   `xu_ly.pham_vi_cua_yeu_cau`)*; số đo 05/10 *("ca chỉ có 3 dòng tiền ⇒
    #   `/queue?curr=VND` **2** hàng")* là của một kho TEST **gần rỗng** lúc ấy,
    #   ⛔ của phạm vi. Bài `AC-7` lằn tiền nay hỏi cửa với `?run_id=<ca.run>`
    #   *(`test_wo045_…::_pham_vi_ca`)* ⇒ phạm vi **là** lần nạp này. Vẫn thêm
    #   **55** dòng tiền VND ⛔ mã nào khớp để `Xem thêm` của `F01` có trang kế
    #   thật trong **chính** lần nạp *(`AC-7`)*.
    i["Q"] = [_tien(conn, run, vnd, 100 + j,
                    f"{random.randint(1_000, 8_999) * 1000}.00", "VND",
                    f"FT45Q{j:02d}{h}") for j in range(SO_KHONG)]
    lenh = {k: "P" + k + "5" + h[:5] + "-1" for k in "ABNT"}
    te = {"A": "USD", "B": "VND", "N": "VND", "T": "VND"}
    dong = [DongPM(3 + n, lenh[k].split("-")[0], lenh[k], D(f"{tien[k]}.00"),
                   te[k], "Approve", canon_ref(doc[k]), "HD-K45", "C-K45",
                   ref_tho=doc[k])
            for n, k in enumerate("ABNT")]
    khong = []
    for j in range(SO_KHONG):
        ma = f"PK{j:02d}{h[:5]}-1"
        so_ct = f"FT45K{j:02d}{h}"
        khong.append(ma)
        dong.append(DongPM(10 + j, ma.split("-")[0], ma,
                           D(f"{random.randint(1_000, 8_999) * 100}.00"), "VND",
                           "Approve", canon_ref(so_ct), "HD-K45", "C-K45",
                           ref_tho=so_ct))
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), dong)
    return {"run": run, "h": h, "doc": doc, "lenh": lenh, "tien": tien, "i": i,
            "khong": khong}
