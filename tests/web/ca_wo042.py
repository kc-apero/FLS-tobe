# -*- coding: utf-8 -*-
"""`WO-042` — ca dựng chung trên **kho TEST** cho bài cửa `tests/api/test_wo042_*`
và bài màn `tests/web/test_wo042_*` *(cùng luật `ca_wo032.py` / `ca_wo037.py`:
thân vẽ màn đi ra từ **cửa HTTP thật**; ⛔ một khoá do bài đặt)*.

Tiền + mã **ngẫu nhiên** mỗi lần *(kho TEST phình — ⛔ `TRUNCATE`)*.

⚠ Ký tự trắng biên viết bằng `chr(<điểm mã>)`, ⛔ bằng chuỗi thoát trong
nguồn: công cụ soạn tệp của phiên AI từng **dịch** chuỗi thoát thành ký tự
thật *(vô hình)* — `fls/canon/tien_te.py` ghi lại lần ấy.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm
from tests.web.ca_wo037 import _tien

NBSP = chr(0x00A0)
BOM = chr(0xFEFF)


def dung_ca_wo042(conn) -> dict:
    """Bốn lệnh trong **một** lần nạp *(kho TEST)*:

      `S` mã `cS` ↔ dòng VND mã `cS` **đúng** số tiền ⇒ rổ `may`, **tự chứng**
          *(`t > 0` — `note ok` ⓑ của `F01L` chỉ hiện khi có)*
      `M` mã `cM` ↔ dòng VND mã `cM` lệch **+5.000** *(ngoài dung sai ⇒ ⛔
          tự chứng)* ⇒ rổ `may` ⛔ tự chứng *(`c > 0` — ghi chú ⓐ, nhãn ⓒ)*
      `A` ⛔ số chứng từ, VND, số tiền `X` ↔ dòng tiền **⛔ mã khớp** tiền tệ
          `NBSP + 'VND'`, đúng `X` ⇒ `itl-candidates` của `A` phải có dòng ấy
          ở bậc `tien` *(`AC-10` vế ①; mã hôm nay: SQL `btrim` bốn ký tự ⛔ gỡ
          NBSP ⇒ dòng ⛔ có)*
      `B` lệnh tiền tệ `BOM + 'VND'`, mã `cB` ↔ dòng VND mã `cB` đúng số tiền
          ⇒ rổ `may` *(`AC-10` vế ②; mã hôm nay: `str.strip()` ⛔ gỡ `U+FEFF`
          ⇒ `nguoi` khác tiền tệ)*; cửa ghi `/match` cặp ấy ⇒ ⛔ `KhacTienTe`
          *(vế ③)*

    Mong *(mã mới)* ở `/lenh-cho/ro`: `may 3 · tu_chung 2 *(S, B)* · nguoi 1
    *(A)* · nguoi_khac_tien_te 0 · tong 4` ⇒ `c = 1`.
    """
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T42" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    tien = {k: random.randint(1_000, 8_999) * 100 + i
            for i, k in enumerate("SMAB")}
    doc = {"S": "FT42S" + h, "M": "FT42M" + h, "A": None, "B": "FT42B" + h}
    vnd = "R | 123456789_VPB VND_K42" + h
    i = {}
    i["S"] = _tien(conn, run, vnd, 1, f"{tien['S']}.00", "VND", doc["S"])
    i["M"] = _tien(conn, run, vnd, 2, f"{tien['M'] + 5000}.00", "VND", doc["M"])
    i["A"] = _tien(conn, run, vnd, 3, f"{tien['A']}.00", NBSP + "VND", "FT42Z" + h)
    i["B"] = _tien(conn, run, vnd, 4, f"{tien['B']}.00", "VND", doc["B"])
    lenh = {k: "P" + k + "9" + h[:5] + "-1" for k in "SMAB"}
    te_lenh = {"S": "VND", "M": "VND", "A": "VND", "B": BOM + "VND"}
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + n, lenh[k].split("-")[0], lenh[k], D(f"{tien[k]}.00"),
               te_lenh[k], "Approve", canon_ref(doc[k]), "HD-K42", "C-K42",
               ref_tho=doc[k])
        for n, k in enumerate("SMAB")])
    da = conn.execute("SELECT pm_line_id, curr FROM fls_pm_line WHERE run_id = %s",
                      (run,)).fetchall()
    assert dict(da)[lenh["B"]] == BOM + "VND", ("⛔ kho gỡ BOM lúc nạp — ca vô "
                                                "nghĩa", da)
    return {"run": run, "h": h, "doc": doc, "lenh": lenh, "tien": tien, "i": i}
