# -*- coding: utf-8 -*-
"""`WO-037` — ca dựng chung trên **kho TEST** cho bài cửa `tests/api/test_wo037_*`
và bài màn `tests/web/test_wo037_*` *(cùng luật `ca_wo032.py`: thân vẽ màn đi ra
từ **cửa HTTP thật**; ⛔ một khoá do bài đặt)*.

Tiền + mã **ngẫu nhiên** mỗi lần *(kho TEST phình — ⛔ `TRUNCATE`)*.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm


def _tien(conn, run, nguon, so, tien, curr, doc):
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW',%s,%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, nguon, so, run, doc, curr, D(tien))).fetchone()[0]


def dung_ca_wo037(conn) -> dict:
    """Sáu lệnh VND trong **một** lần nạp *(kho TEST)*:

      `K` mã `cK` ↔ dòng **USD** mã `cK` *(⛔ dòng VND mã ấy)* ⇒ rổ `nguoi`
          — hình `PM00329-1` sổ thật *(`AC-1` · `AC-8`)*
      `W` mã `cW` ↔ dòng **USD** mã `cW`; bài **thêm** dòng VND mã `cW` giữa
          chừng ⇒ lệnh về rổ `may` *(`AC-1` chiều ngược)*
      `S` mã `cS` ↔ dòng mang tiền tệ `' vnd '` *(khoảng trắng)* ⇒ **cùng**
          VND ⇒ rổ `may` *(`AC-1` · `F-1` cùng hàm `ma_tien_te`)*
      `Y` mã `cY` ↔ USD mã `cY` *(`itl_id` nhỏ)* · VND mã `cY` *(`itl_id` lớn,
          lệch **5.000** — ngoài dung sai ⇒ ⛔ `tu_chung` ⇒ hiện ở chip `Chưa gán`)* ·
          VND ⛔ mã, **đúng** số tiền *(bậc `tien`)* *(`AC-3`)*
      `M` mã `cM` ↔ dòng VND mã `cM` lệch **+5.000** *(ngoài dung sai ghép
          tay ⇒ ⛔ `tu_chung`)* ⇒ rổ `may`, chip `Chưa gán` *(hồi quy ô `đề xuất:`)*
      `G` ⛔ mã chung ↔ **mối nối** tới dòng USD mã **khác** *(chèn như
          `chay_nap.chen_moi_noi` — cửa ghi tay ném `KhacTienTe`)* *(`AC-4`)*
    """
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T37" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    tien = {k: random.randint(1_000, 8_999) * 100 + i
            for i, k in enumerate("KWSYGM")}
    doc = {k: "FT37" + k + h for k in "KWSYGM"}
    usd, vnd = "R | 987654321_OCBC USD_K37" + h, "R | 123456789_VPB VND_K37" + h
    i = {}
    i["K"] = _tien(conn, run, usd, 1, f"{tien['K']}.00", "USD", doc["K"])
    i["W"] = _tien(conn, run, usd, 2, f"{tien['W']}.00", "USD", doc["W"])
    i["S"] = _tien(conn, run, vnd, 3, f"{tien['S']}.00", " vnd ", doc["S"])
    # ⚠ Thứ tự chèn = thứ tự `itl_id`: USD **trước** ⇒ `itl_id` **nhỏ hơn** —
    #   xếp theo `itl_id` *(mã hôm nay)* đặt USD lên đầu ⇒ `AC-3` ĐỎ.
    i["Y_usd"] = _tien(conn, run, usd, 4, f"{tien['Y']}.00", "USD", doc["Y"])
    i["Y_vnd"] = _tien(conn, run, vnd, 5, f"{tien['Y'] + 5000}.00", "VND", doc["Y"])
    i["Y_tien"] = _tien(conn, run, vnd, 6, f"{tien['Y']}.00", "VND", "FT37Z" + h)
    i["G"] = _tien(conn, run, usd, 7, f"{tien['G']}.00", "USD", "FT37Q" + h)
    i["M"] = _tien(conn, run, vnd, 9, f"{tien['M'] + 5000}.00", "VND", doc["M"])
    lenh = {k: "P" + k + "7" + h[:5] + "-1" for k in "KWSYGM"}
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + n, lenh[k].split("-")[0], lenh[k], D(f"{tien[k]}.00"), "VND",
               "Approve", canon_ref(doc[k]), "HD-K37", "C-K37", ref_tho=doc[k])
        for n, k in enumerate("KWSYGM")])
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i["G"], lenh["G"], D(f"{tien['G']}.00"), run))
    return {"run": run, "h": h, "doc": doc, "lenh": lenh, "tien": tien,
            "i": i, "nguon_vnd": vnd}


def dung_ca_wo037_v2(conn) -> dict:
    """`WO-037` **vòng 2** — bốn lệnh VND trong **một** lần nạp *(kho TEST)*,
    đủ để băng `F01L` có **cả ba** con số `a` · `b` · `c` khác `0`:

      `K` mã `cK` ↔ dòng **USD** mã `cK` ⇒ rổ `nguoi`, nhánh khớp mã chỉ khác
          tiền tệ ⇒ đếm vào `nguoi_khac_tien_te` *(`b`)*
      `N` ⛔ số chứng từ ⇒ rổ `nguoi` *(`a`)*
      `T` ⛔ số chứng từ, số tiền `X` ↔ dòng tiền **⛔ mã khớp** tiền tệ
          `' vnd '` *(khoảng trắng + chữ thường)*, đúng số tiền `X` ⇒ rổ
          `nguoi` *(`a`)*; `itl-candidates` của `T` phải có dòng ấy ở bậc
          `tien` *(`AC-14` — SQL vế sổ `btrim`)*
      `M` mã `cM` ↔ dòng VND mã `cM` lệch **+5.000** *(ngoài dung sai ⇒ ⛔
          `tu_chung`)* ⇒ rổ `may` ⛔ tự chứng *(`c`)*

    Mong ở `/lenh-cho/ro`: `may 1 · nguoi 3 · khong 0 · tu_chung 0 · tong 4 ·
    nguoi_khac_tien_te 1` ⇒ `a = 2 · b = 1 · c = 1`.
    """
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T38" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    tien = {k: random.randint(1_000, 8_999) * 100 + i
            for i, k in enumerate("KNTM")}
    doc = {"K": "FT38K" + h, "M": "FT38M" + h, "N": None, "T": None}
    usd, vnd = "R | 987654321_OCBC USD_K38" + h, "R | 123456789_VPB VND_K38" + h
    i = {}
    i["K"] = _tien(conn, run, usd, 1, f"{tien['K']}.00", "USD", doc["K"])
    i["T"] = _tien(conn, run, vnd, 2, f"{tien['T']}.00", " vnd ", "FT38V" + h)
    i["M"] = _tien(conn, run, vnd, 3, f"{tien['M'] + 5000}.00", "VND", doc["M"])
    lenh = {k: "P" + k + "8" + h[:5] + "-1" for k in "KNTM"}
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + n, lenh[k].split("-")[0], lenh[k], D(f"{tien[k]}.00"), "VND",
               "Approve", canon_ref(doc[k]), "HD-K38", "C-K38", ref_tho=doc[k])
        for n, k in enumerate("KNTM")])
    return {"run": run, "h": h, "doc": doc, "lenh": lenh, "tien": tien, "i": i}
