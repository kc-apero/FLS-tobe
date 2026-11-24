#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FLS STAGING — NGƯỜI KÝ ký tỷ giá hàng loạt qua TUYẾN API · `STG-R2-02` (vòng sửa sau R2 `KQ-328`).

    # app chạy ở chế độ `ghi` (vao.sh, FLS_STG_CHE_DO=ghi, FLS_STG_ACTOR=<người ký>) rồi, TRÊN CÙNG máy:
    python tools/staging/app/ky_ty_gia.py --cong 8088            # ký mọi tháng IX.FX chưa ký (⛔ tháng LẠC)
    python tools/staging/app/ky_ty_gia.py --cong 8088 --kiem     # chỉ ĐẾM (⛔ ký): ra `đã ký N/M`

Vì sao có lệnh này: D1 — gói HD2 đọc tỷ giá TỪ KHO, tháng chưa ký ⇒ `FX_CHAN`. Bước 04 chỉ NẠP config; ký là việc của
NGƯỜI KÝ trong UAT *(chủ quyết C4: một người ký, một người soát)*. Ký 36 tháng bằng tay bấm từng nút là việc lặp — lệnh này
bấm thay *tay*, ⛔ ký thay *người*:
  · đi qua `POST /config/fx/{yyyymm}/sign` của CỬA *(⛔ SQL, ⛔ gọi `cau_hinh_repo`, ⛔ ghi thẳng bảng)*;
  · `actor` do CỬA lấy từ THẺ *(tên người khởi động app `ghi`)* — lệnh này ⛔ gửi `actor` nào trong thân;
  · thẻ lấy từ `/phien.js` của chính cửa, nghe loopback `127.0.0.1` — ⛔ nhận địa chỉ khác;
  · ký lại một tháng đã ký ⇒ `409` có tên ⇒ ghi nhận "đã có", ⛔ lỗi *(chạy lại được)*.
Thoát `0` = MỌI tháng của `GET /config/fx` đã `da_ky` sau lượt này · `1` = còn tháng chưa ký/lỗi · `2` = sai tham số.
Thẻ ⛔ in ra, ⛔ ghi tệp.
"""
from __future__ import annotations

import argparse
import http.client
import json
import re
import sys

V = "/api/fls/v1"


def _goi(cong: int, duong: str, the: str | None = None, ph: str = "GET") -> tuple[int, bytes]:
    c = http.client.HTTPConnection("127.0.0.1", cong, timeout=30)       # ⛔ chỉ loopback
    try:
        h = {"Authorization": f"Bearer {the}"} if the else {}
        if ph == "POST":                     # cửa đòi thân JSON cho phép ghi; ⛔ `actor` trong thân (cửa từ chối) — thân RỖNG
            h["Content-Type"] = "application/json"
            c.request(ph, duong, body=b"{}", headers=h)
        else:
            c.request(ph, duong, headers=h)
        r = c.getresponse()
        return r.status, r.read()
    finally:
        c.close()


def lay_the(cong: int) -> str:
    """Thẻ như trình duyệt lấy: từ `/phien.js` của cửa."""
    ma, js = _goi(cong, "/phien.js")
    if ma != 200:
        raise SystemExit(f"⛔ /phien.js ⇒ {ma} (app đang chạy ở cổng {cong}? chế độ `ghi`?)")
    m = (re.search(rb'"the"\s*:\s*"([^"]+)"', js) or re.search(rb"'the'\s*:\s*'([^']+)'", js)
         or re.search(rb"([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)", js))
    if not m:
        raise SystemExit("⛔ không thấy thẻ trong /phien.js")
    return m.group(1).decode()


def doc_trang_thai(cong: int, the: str) -> tuple[list[tuple[int, str]], list[int]]:
    """`(ky: [(yyyymm, trang_thai)] ⛔ gồm tháng LẠC, lac: [yyyymm])` — tháng LẠC *(vd 202306)* màn hình ⛔ có nút ký ⇒ ⛔ ký ở đây."""
    ma, than = _goi(cong, f"{V}/config/fx", the)
    if ma != 200:
        raise SystemExit(f"⛔ GET /config/fx ⇒ {ma}: {than[:200]!r} (đã chạy bước 04 nạp IX.FX chưa?)")
    data = json.loads(than)["data"]
    lac = {int(m) for m in data["lac"]}
    return [(int(d["yyyymm"]), d["trang_thai"]) for d in data["ky"] if int(d["yyyymm"]) not in lac], sorted(lac)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ky_ty_gia.py", description="Ký tỷ giá hàng loạt qua tuyến API (actor từ thẻ).")
    p.add_argument("--cong", type=int, required=True, help="cổng cửa app (loopback)")
    p.add_argument("--kiem", action="store_true", help="chỉ đếm, ⛔ ký")
    a = p.parse_args(argv)
    the = lay_the(a.cong)
    ky, lac = doc_trang_thai(a.cong, the)
    chua = [m for m, tt in ky if tt != "da_ky"]
    print(f"tỷ giá IX.FX: {len(ky)} tháng cần ký (dòng GET /config/fx trừ {len(lac)} tháng LẠC {lac}) · đã ký {len(ky) - len(chua)} · chưa ký {len(chua)}")
    if a.kiem:
        return 0 if ky and not chua else 1
    loi = []
    for m in chua:
        ma, than = _goi(a.cong, f"{V}/config/fx/{m}/sign", the, "POST")
        if ma == 201:
            print(f"  ký {m}: 201")
        elif ma == 409:
            print(f"  ký {m}: 409 đã có chữ ký")
        else:
            loi.append(m)
            print(f"  ⛔ ký {m}: {ma} {than[:160]!r}")
    sau, _ = doc_trang_thai(a.cong, the)
    con = [m for m, tt in sau if tt != "da_ky"]
    print(f"══ KÝ: {len(sau) - len(con)}/{len(sau)} tháng đã ký · lỗi {len(loi)} · KẾT: {'ĐẠT' if sau and not con else 'ĐỎ'}")
    return 0 if sau and not con else 1


if __name__ == "__main__":
    sys.exit(main())
