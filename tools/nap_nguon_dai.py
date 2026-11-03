# -*- coding: utf-8 -*-
"""`GAP-KHAI-01` — thu **bản khai THỨ HAI** vào kho, rồi chạy `S10`.

    Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/nap_nguon_dai.py
           thêm `--that` để ghi vào **kho THẬT** *(⛔ không có thì ghi kho TEST)*

⛔⛔ **Vì sao có công cụ này.** Hệ có **HAI** bản khai cho cùng một phép ánh xạ:

    ⓐ **dòng 1** mỗi sheet `R |`                → `fls_khai_cot` · **FLS đọc**
    ⓑ `Range_Condition/Debit/Credit` ở danh mục  → `fls_nguon_dai` · **script
       `Run` của trang tính đọc**

Quét `fls/` `tools/` `tests/` ngày 08/09: **0 tham chiếu `Range_`**. Tức bản
khai mà **chính cái máy đang chạy** dùng thì FLS **chưa từng đọc**.

⛔ **Lệch ở đây nguy một cách IM LẶNG:** sửa dòng 1 mà quên danh mục thì FLS và
   trang tính **đọc hai cột khác nhau**, và **cả hai vẫn chạy bình thường** —
   ⛔ không lệnh nào lỗi, ⛔ không dòng nào rơi, số tổng vẫn trông hợp lý.

⛔ `QĐ-ITL-92` / `QĐ-ITL-85`: chỉ đọc **tên sheet + 3 cột dải + trạng thái**.
   ⛔ Không đọc một ô dữ liệu giao dịch nào.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

import psycopg  # noqa: E402

from fls.db.kho import dsn_that, dsn_test  # noqa: E402
from fls.kiem.soat_nap import s10_hai_ban_khai_cung_cot  # noqa: E402
from fls.repo.nguon_dai import COT_DANH_MUC, doc_dai, ghi_dai  # noqa: E402
from tools.do_bat_bien_ngam import BANK, QUY  # noqa: E402
from tools.do_hinh_dang import API, token  # noqa: E402

# ⭐ `(sổ, tên bảng danh mục, cột mang TÊN SHEET)`. Hai lằn **khác đầu cột**:
#    bank có `PT · Bank Name · Bank Account · Bank Sheet`, quỹ có
#    `Source · Bank Sheet · Entity` ⇒ ⛔ không neo theo **số cột**, tra theo
#    **tên tiêu đề**.
SO = ((BANK, "BankAccountList"), (QUY, "Cash Ledger List"))
COT_SHEET = "Bank Sheet"


def api(u: str, tok: str):
    rq = urllib.request.Request(u, headers={"Authorization": "Bearer " + tok})
    with urllib.request.urlopen(rq, timeout=90) as r:
        return json.load(r)


def doc_danh_muc(sid: str, ten: str, tok: str) -> dict[str, dict[str, str]]:
    """→ `{tên sheet: {Date/Debit/Credit: dải thô}}`.

    ⭐ **Dòng ĐẦU TIÊN thắng**, và đó là một lựa chọn có lý do: nhiều tài khoản
      cùng trỏ vào một sheet *(bên quỹ: `R | CNC` có 4 dòng, `R | Pingpong` có
      3)*. Lấy dòng đầu là **đúng cái người đọc bảng nhìn thấy trước**. ⚠ Đo
      08/09: dòng đầu của hai sheet ấy có `Range_*` **RỖNG** — và điều đó phải
      **hiện ra** ở `S10` thành *"⛔ chưa đo được"*, ⛔ không bị một dòng sau
      lặng lẽ lấp vào.
    """
    d = api(f"{API}{sid}/values/"
            + urllib.parse.quote(f"'{ten}'!A1:BZ400")
            + "?valueRenderOption=UNFORMATTED_VALUE", tok)
    rows = d.get("values", [])
    if len(rows) < 2:
        raise SystemExit("⛔ %s: ⛔ không đọc được dòng tiêu đề" % ten)
    hdr = [str(x).strip() for x in rows[1]]
    idx: dict[str, int] = {}
    for c, h in enumerate(hdr):
        if h and h not in idx:
            idx[h] = c
    thieu = [k for k in (COT_SHEET, *COT_DANH_MUC) if k not in idx]
    if thieu:
        raise SystemExit("⛔ %s: danh mục THIẾU cột %s — ⛔ không đoán vị trí"
                         % (ten, thieu))

    def o(r, c):
        return str(r[c]).strip() if c < len(r) else ""

    ra: dict[str, dict[str, str]] = {}
    for r in rows[2:]:
        s = o(r, idx[COT_SHEET])
        if not s.startswith("R |") or s in ra:
            continue
        ra[s] = {tr: o(r, idx[cot]) for cot, tr in COT_DANH_MUC.items()}
    return ra


def main() -> int:
    that = "--that" in sys.argv
    tok = token()

    thu: dict[str, tuple[str, dict[str, str]]] = {}
    for sid, ten in SO:
        for s, dai in doc_danh_muc(sid, ten, tok).items():
            if s in thu:
                raise SystemExit(
                    "⛔ sheet TRÙNG TÊN giữa hai danh mục: %r" % s)
            thu[s] = (ten, dai)

    print("=" * 78)
    print("THU BẢN KHAI THỨ HAI (`Range_*`) — kho %s" % ("THẬT" if that else "TEST"))
    print("=" * 78)
    print("  dòng danh mục có tên sheet `R |`  : %3d" % len(thu))

    dem = {"moi": 0, "giu": 0, "khong_co_nguon": 0}
    khai: dict[str, dict[str, int]] = {}
    dai: dict[str, dict[str, int | None]] = {}

    with psycopg.connect(dsn_that() if that else dsn_test(),
                         autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT source_key, source_id FROM fls_source")
            sid_theo_ten = dict(cur.fetchall())
            cur.execute(
                "SELECT s.source_key, kc.truong, kc.cot FROM fls_khai_cot kc"
                "  JOIN fls_source s USING (source_id)"
                " WHERE kc.version = (SELECT max(version) FROM fls_khai_cot x"
                "                      WHERE x.source_id = kc.source_id)")
            for k, tr, c in cur.fetchall():
                khai.setdefault(k, {})[tr] = c

        for s in sorted(thu):
            ten_dm, tho = thu[s]
            sid = sid_theo_ten.get(s)
            if sid is None:
                dem["khong_co_nguon"] += 1
                continue
            b = ghi_dai(conn, sid, tho, danh_muc=ten_dm)
            if b is None:
                dem["giu"] += 1
                b = doc_dai(conn, sid)
            else:
                dem["moi"] += 1
            if b is not None:
                dai[s] = b.cot

    print("  ghi MỚI (dải đổi, hoặc lần đầu)   : %3d" % dem["moi"])
    print("  giữ nguyên (⛔ không đổi)          : %3d" % dem["giu"])
    print("  ⚠ có trong danh mục, ⛔ không có nguồn trong kho: %3d"
          % dem["khong_co_nguon"])
    print("-" * 78)

    kq = s10_hai_ban_khai_cung_cot(khai, dai)
    print("  %s  %s" % ("⭐ ĐẠT " if kq.xanh else "⛔ KHÔNG ĐẠT", kq.ten))
    print("     đã đo: %d · %s" % (kq.da_do, kq.thong_diep))
    print("=" * 78)
    if not that:
        print("(kho TEST — thêm `--that` để ghi vào kho THẬT)")
    return 0 if kq.xanh else 1


if __name__ == "__main__":
    raise SystemExit(main())
