# -*- coding: utf-8 -*-
"""Đo: trong 7.329 dòng CHƯA ghép, bao nhiêu dòng **TỰ CHỨNG**?

⛔⛔ **Gọi HÀM THẬT (`ung_vien_pm`), ⛔ không dựng lại SQL bằng tay.** Chính
   `doc_bao_cao.py` ghi: *"mã tham chiếu được chuẩn hoá BÊN PYTHON rồi mới so —
   ⛔ không viết lại `canon_ref` bằng SQL: hai bản chuẩn hoá là hai bản sự
   thật, và bản SQL sẽ lệch dần trong im lặng"*. Một phép quét dựng bằng tay ở
   đây sẽ **báo oan cùng lượt** — đúng bài học đã ghi.

"TỰ CHỨNG" = có **đúng MỘT** ứng viên bậc `ma` *(khớp mã tham chiếu)* mà ứng
viên ấy **chưa bị ghép** cho dòng khác. Đó là tập mà một cửa ghép LÔ có thể
nhận **mà ⛔ không chọn hộ ai cái gì**.
"""
import sys
import collections
import psycopg

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

from fls.repo.doc_bao_cao import ung_vien_pm            # noqa: E402
from fls.repo.pham_vi import chi_nap_that               # noqa: E402

PV = chi_nap_that()
DSN = "postgresql://fls:fls@localhost:5433/fls"

c = psycopg.connect(DSN)
with c.cursor() as cur:
    cur.execute("""
        SELECT i.itl_id FROM fls_itl i
         WHERE NOT EXISTS (SELECT 1 FROM fls_moi_noi m
                            WHERE m.itl_id = i.itl_id)
         ORDER BY i.itl_id""")
    chua = [r[0] for r in cur.fetchall()]
print("dong CHUA ghep:", len(chua))

nhom = collections.Counter()
tu_chung = []
for k, i in enumerate(chua):
    d = ung_vien_pm(c, PV, i, n=50)
    if d is None:
        nhom["ngoai pham vi"] += 1
        continue
    uv = d["ung_vien"]
    if not uv:
        nhom["a · ⛔ KHONG co ung vien nao"] += 1
        continue
    ma = [x for x in uv if x["bac"] == "ma" and not x["da_ghep"]]
    if len(ma) == 1:
        nhom["b · TU CHUNG (dung 1 ung vien bac `ma`)"] += 1
        tu_chung.append(i)
    elif len(ma) > 1:
        nhom["c · nhieu ung vien bac `ma` — nguoi phai chon"] += 1
    else:
        tien = [x for x in uv if x["bac"] == "tien" and not x["da_ghep"]]
        if len(tien) == 1:
            nhom["d · 1 ung vien khop TIEN (⛔ khong khop ma)"] += 1
        elif tien:
            nhom["e · nhieu ung vien khop TIEN"] += 1
        else:
            nhom["f · chi cung tien te / gan tien ⇒ ⛔ khong tu chung"] += 1
    if k % 1500 == 0 and k:
        print("  ... %d/%d" % (k, len(chua)))

print()
tong = sum(nhom.values())
for a, b in sorted(nhom.items()):
    print("%-52s %6d  %5.1f%%" % (a, b, 100 * b / tong))
print("-" * 68)
print("%-52s %6d" % ("TONG", tong))
print()
print("⇒ Cua ghep LO co the nhan ngay:", len(tu_chung), "dong")
