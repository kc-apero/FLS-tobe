# -*- coding: utf-8 -*-
"""⛔ 70,1% dòng chưa ghép **⛔ không có ứng viên khớp MÃ nào**. Vì sao?

Ba khả năng, và chúng dẫn tới **ba việc khác nhau hoàn toàn**:
  ⓐ dòng tiền ⛔ **không có** số chứng từ  ⇒ ⛔ không khoá nào để ghép
  ⓑ có số chứng từ nhưng `canon_ref` trả `None` ⇒ **bộ chuẩn hoá** thiếu khuôn
  ⓒ có mã chuẩn hoá được, mà **⛔ không dòng PM nào mang mã ấy** ⇒ thiếu **dữ
     liệu PM** *(đúng nửa đang ĐÓNG BĂNG 13 ngày)*, ⛔ không phải thiếu mã

⇒ Nếu ⓒ chiếm phần lớn thì việc đầu tiên của tác vụ ① **⛔ không phải** dựng
  cửa ghép lô — mà là **mốc `A3`: nạp PM cho mới**.
"""
import sys
import collections
import psycopg

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

from fls.adapters.pm_join import canon_ref              # noqa: E402

c = psycopg.connect("postgresql://fls:fls@localhost:5433/fls")
with c.cursor() as cur:
    cur.execute("""
        SELECT i.itl_id, i.doc_no, i.run_id FROM fls_itl i
         WHERE NOT EXISTS (SELECT 1 FROM fls_moi_noi m
                            WHERE m.itl_id = i.itl_id)""")
    chua = cur.fetchall()

    # ⛔ Chuan hoa CA hai ve bang CUNG mot ham — bai hoc `_khoa` ngay 08/09:
    #   mot cong so hai ve bang hai luat la mot cong ⛔ chua biet no do gi.
    cur.execute("SELECT ref_canon, run_id FROM fls_pm_line")
    pm = cur.fetchall()

pm_ma = collections.defaultdict(set)          # ref_canon -> {run_id}
for r, run in pm:
    if r:
        pm_ma[r].add(run)
pm_moi_ma = set(pm_ma)
print("dong PM:", len(pm), "· ma canon KHAC NHAU:", len(pm_moi_ma))
print("dong CHUA ghep:", len(chua))
print()

g = collections.Counter()
vi_du = collections.defaultdict(list)
for i, doc_no, run in chua:
    if doc_no is None or not str(doc_no).strip():
        g["a · ⛔ KHONG co so chung tu"] += 1
        continue
    ma = canon_ref(doc_no)
    if not ma:
        g["b · co so chung tu ma `canon_ref` tra None"] += 1
        if len(vi_du["b"]) < 6:
            vi_du["b"].append(doc_no)
        continue
    if ma not in pm_moi_ma:
        g["c · ma chuan hoa duoc ma ⛔ KHONG PM nao mang"] += 1
        if len(vi_du["c"]) < 6:
            vi_du["c"].append((doc_no, ma))
        continue
    if run not in pm_ma[ma]:
        g["d · PM CO ma ay nhung o LAN NAP khac"] += 1
        if len(vi_du["d"]) < 6:
            vi_du["d"].append((doc_no, ma, run, sorted(pm_ma[ma])))
        continue
    g["e · PM co ma ay, CUNG lan nap ⇒ le ra ghep duoc"] += 1

tong = sum(g.values())
for a, b in sorted(g.items()):
    print("%-50s %6d  %5.1f%%" % (a, b, 100 * b / tong))
print("-" * 66)
print("%-50s %6d" % ("TONG", tong))
for k in ("b", "c", "d"):
    if vi_du[k]:
        print("\nvi du nhom %s:" % k)
        for x in vi_du[k]:
            print("   ", x)
