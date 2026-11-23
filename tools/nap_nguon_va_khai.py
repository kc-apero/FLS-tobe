# -*- coding: utf-8 -*-
"""`P7` task `7` — nạp **nguồn** + **bản khai `v1`** vào kho.

    Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/nap_nguon_va_khai.py
           thêm `--that` để ghi vào **kho THẬT** *(⛔ không có thì ghi kho TEST)*

⭐⭐ **Một "nguồn" ⛔ KHÔNG phải một tài khoản — nó là một DÒNG CHẢY sao kê có
   MỘT bố cục cột.** Đo được 2026-09-08:

     · bên **ngân hàng** hai thứ trùng nhau *(1 tài khoản = 1 sheet)*;
     · bên **quỹ** thì ⛔ KHÔNG: `R | CNC` có **4** dòng danh mục cùng trỏ vào,
       `R | Pingpong` có **3** ⇒ **7 quỹ đổ chung vào 2 dòng chảy**.

   ⇒ Coi nguồn = tài khoản thì ta tạo **7 tờ hướng dẫn cho 2 bố cục** — bảy bản
     sao của một sự thật, và ngày nào đó chúng lệch nhau. Bản khai ánh xạ cột
     là thuộc tính của **dòng chảy**, ⛔ không phải của chủ tài khoản.

⛔⛔ **Và vì thế công cụ này ⛔ KHÔNG đụng vào danh mục tài khoản** — thứ đang
   mang **ba khuyết tật đã đo** *(`GAP-KT-01..04`)*: 2 lỗi gõ thừa một ký tự ·
   1 dòng trỏ tới sheet `R | PO BGO1` ⛔ không tồn tại *(lệch **42,16 triệu**)* ·
   5 dòng `Active` ⛔ không có tên tài khoản. ⇒ Nạp từ **sheet có thật**, nên ba
   lỗi ấy **⛔ không được bê sang hệ mới**. Chúng là việc của **kế toán**, và
   FLS ⛔ **không tự sửa hộ** *(`QĐ-ITL-34`, `R-A4`)*.

   ⚠ Cái ta **chưa** làm: bảng *"tài khoản nào thuộc dòng chảy nào"*. Nó là một
     bảng KHÁC, làm **sau khi** kế toán sửa — ⛔ không nhét vào đây.

★ **`source_key` = ĐÚNG tên sheet**, ⛔ không thêm tiền tố. Vì chính danh mục
  của kế toán đã trỏ tới dòng chảy **bằng tên sheet** *(`BankAccountList` cột
  3)*; dùng cùng một chuỗi thì bảng ánh xạ tương lai **nối thẳng được**, ⛔ không
  cần một phép dịch — mà mọi phép dịch là một chỗ để lệch len vào. Đổi lại ta
  **phải** kiểm trùng tên giữa hai sổ, và ⛔ **NỔ** nếu trùng.

⭐ **Chạy lại ⛔ không đẻ ra `version` mới nếu bản khai ⛔ không đổi.** Bản khai
  chỉ được ghi thêm khi nó **thật sự khác** bản đang hiệu lực — đúng luật ⓐ
  *(chỉ-thêm)* mà ⛔ không biến mỗi lần chạy thành một dòng rác.

⛔ `QĐ-ITL-92`: chỉ đọc **tên sheet + dòng 1**. ⛔ Không đọc `Description`,
  ⛔ không đọc một ô dữ liệu nào, ⛔ không in nội dung ô.
"""
from __future__ import annotations

import sys

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

import psycopg  # noqa: E402

from fls.adapters.sao_ke import (SAU_TRUONG, BanKhaiHong,  # noqa: E402
                                 doc_ban_khai, kiem_ban_khai)
from fls.db.kho import dsn_that, dsn_test  # noqa: E402
from fls.repo.khai_cot import KhongCoKhai, doc_khai, ghi_khai  # noqa: E402
from tools.do_bat_bien_ngam import BANK, QUY  # noqa: E402
from tools.do_danh_muc_nguon import ten_r  # noqa: E402
from tools.do_hinh_dang import dong_dau, token  # noqa: E402

# ⛔ `src_type` lấy đúng bộ giá trị đã khai ở `fls/db/schema.py`
#    (`Bank|Cash|CCR|Platform|Mapping`) — ⛔ không đặt tên mới.
SO = (("Bank", BANK), ("Cash", QUY))

# ⭐ Ai khai. Nói THẲNG là máy, ⛔ không mượn tên một người — một bản khai ký
#    tên người mà người ấy chưa hề nhìn thấy nó là một chữ ký GIẢ, và cột
#    `actor` sẽ mất nghĩa ngay từ dòng đầu tiên.
#    ⇒ Kế toán xác nhận lúc tải tệp lần đầu sẽ sinh **`version` mang tên họ**;
#      *"đã xác nhận"* = *"có một bản khai mang tên người thật"*. ⛔ Không cần
#      thêm cột trạng thái nào (chuyện của màn hình — task `8`).
MAY = "máy · trích dòng 1 (QĐ-ITL-105)"


def thu_thap(tok: str) -> dict[str, tuple[str, dict[str, int]]]:
    """→ `{tên sheet: (src_type, bản khai)}` cho **mọi** sheet `R |` của 2 sổ.

    ⛔ NỔ nếu hai sổ có sheet **trùng tên**: `source_key` là khoá duy nhất, nên
    trùng tên nghĩa là hai dòng chảy khác nhau bị nhập làm một — và bản khai
    của cái này sẽ được dùng để đọc tiền của cái kia.
    """
    ra: dict[str, tuple[str, dict[str, int]]] = {}
    for loai, sid in SO:
        ten = sorted(ten_r(sid, tok))
        hdr = dong_dau(sid, ten, tok, n=1)
        for s in ten:
            if s in ra:
                raise SystemExit(
                    "⛔ sheet TRÙNG TÊN giữa hai sổ: %r (%s và %s). "
                    "`source_key` là khoá duy nhất ⇒ hai dòng chảy sẽ bị nhập "
                    "làm một, và bản khai của cái này dùng để đọc tiền của cái "
                    "kia." % (s, ra[s][0], loai))
            d = hdr.get(s) or [[]]
            ra[s] = (loai, doc_ban_khai(d[0] if d else []))
    return ra


def nap(conn, thu: dict[str, tuple[str, dict[str, int]]]) -> dict[str, int]:
    dem = {"nguon_moi": 0, "nguon_da_co": 0, "khai_v1": 0, "khai_moi": 0,
           "khai_giu": 0, "thieu_truong": 0}
    for s in sorted(thu):
        loai, khai = thu[s]
        # ⛔⛔ **Hỏi ĐÚNG câu, ⛔ không đếm độ dài.** Bản trước viết
        #    `len(khai) != len(SAU_TRUONG)` — đúng chừng nào bản khai **chỉ**
        #    có 6 trường. `QĐ-ITL-108` cho lằn quỹ khai thêm `Legal Entity`
        #    và `CDT` ⇒ một bản khai **8 trường ĐỦ CẢ 6** bị con số `8 != 6`
        #    gạt ra, và thông báo in `thiếu []` — **⛔ không thiếu gì mà vẫn
        #    bị loại**. ⇒ Gọi **đúng hàm kiểm** của tầng adapter, ⛔ không
        #    viết một phép kiểm thứ hai bằng phép đếm.
        try:
            kiem_ban_khai(s, khai)
        except BanKhaiHong:
            # ⛔ ⛔ KHÔNG nạp một phần. Báo tên sheet + trường thiếu rồi bỏ qua
            #    — nhưng **đếm**, để con số cuối cùng ⛔ không nói dối.
            print("  ⛔ %-46s thiếu %s"
                  % (s, sorted(set(SAU_TRUONG) - set(khai))))
            dem["thieu_truong"] += 1
            continue

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO fls_source (source_key, src_type) VALUES (%s,%s)"
                " ON CONFLICT (source_key) DO NOTHING RETURNING source_id",
                (s, loai))
            r = cur.fetchone()
            if r is None:
                dem["nguon_da_co"] += 1
                cur.execute("SELECT source_id FROM fls_source"
                            " WHERE source_key = %s", (s,))
                sid = cur.fetchone()[0]
            else:
                dem["nguon_moi"] += 1
                sid = r[0]

        try:
            cu = doc_khai(conn, sid)
        except KhongCoKhai:
            ghi_khai(conn, sid, khai, actor=MAY)
            dem["khai_v1"] += 1
            continue
        # ⭐ Chạy lại mà bản khai ⛔ không đổi ⇒ ⛔ KHÔNG đẻ `version` mới.
        if cu.cot == khai:
            dem["khai_giu"] += 1
        else:
            b = ghi_khai(conn, sid, khai, actor=MAY)
            dem["khai_moi"] += 1
            print("  ⭐ %-46s bố cục ĐỔI ⇒ khai v%d" % (s, b.version))
    return dem


def main() -> int:
    that = "--that" in sys.argv
    tok = token()
    thu = thu_thap(tok)

    print("=" * 78)
    print("NẠP NGUỒN + BẢN KHAI — kho %s" % ("THẬT" if that else "TEST"))
    print("=" * 78)
    for loai, _ in SO:
        n = sum(1 for v in thu.values() if v[0] == loai)
        du = sum(1 for v in thu.values()
                 if v[0] == loai and not set(SAU_TRUONG) - set(v[1]))
        them = sum(1 for v in thu.values()
                   if v[0] == loai and len(v[1]) > len(SAU_TRUONG))
        print("  %-6s sheet `R |` : %3d   · khai đủ 6 trường: %3d"
              "   · khai THÊM (LE/CDT): %2d" % (loai, n, du, them))

    dsn = dsn_that() if that else dsn_test()
    with psycopg.connect(dsn, autocommit=True) as conn:
        dem = nap(conn, thu)

    print("-" * 78)
    for k, nhan in (("nguon_moi", "nguồn MỚI vào `fls_source`"),
                    ("nguon_da_co", "nguồn đã có sẵn"),
                    ("khai_v1", "bản khai `v1` mới ghi"),
                    ("khai_moi", "⭐ bản khai `version` mới (bố cục ĐỔI)"),
                    ("khai_giu", "bản khai giữ nguyên (⛔ không đổi)"),
                    ("thieu_truong", "⛔ sheet THIẾU trường — ⛔ không nạp")):
        print("  %-42s : %3d" % (nhan, dem[k]))

    tong = dem["khai_v1"] + dem["khai_moi"] + dem["khai_giu"]
    print("-" * 78)
    print("  ⇒ %d/%d dòng chảy có bản khai trong kho" % (tong, len(thu)))
    if not that:
        print("\n(kho TEST — thêm `--that` để ghi vào kho THẬT)")
    print("\n⛔ Công cụ này ⛔ KHÔNG đụng danh mục tài khoản: nó đang mang 3")
    print("   khuyết tật đã đo (`GAP-KT-01..04`). Bảng *tài khoản ↔ dòng chảy*")
    print("   là việc SAU, và 3 lỗi ấy là việc của KẾ TOÁN.")
    return 1 if dem["thieu_truong"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
