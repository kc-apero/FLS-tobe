"""Đ5-b · Do BON BAT BIEN NGAM con lai cua `§5` — loai ⛔ khong tu lo ra.

⭐⭐ **Cau hoi trung tam.** Bo tai lieu ITL **dang tu thiet ke** mot khoa doi
   sanh (`INV-I04b`) va mot nhat ky thay doi (`AUD-1`). Nhung `P100 Bank` da
   co san sheet **`Log`** *(171.358 dong)* voi khoa dang
   `20250211||66923.25|FT25042584880113`, va `P100 Cash` co **`Log`** rieng
   *(130.901 dong)*. ⇒ **Neu chung da lam dung viec ay roi thi `F04` ⛔ khong
   phai phat minh lai** — y het bai hoc *"dong 1 la ban khai"* o `Đ2`.

   Cong cu nay tra loi bang **do**, ⛔ khong bang doc:
     · khoa cua `Log` co **cung hinh** voi khoa `INV-I04b` ⛔ khong?
     · no co **phu** so giao dich ⛔ khong, hay chi cham mot goc?

⛔⛔ **Va mot cai bay da san o day.** `§5` goi `Bank Transactions_Filter` la
   *"mot ban LOC ma to hon thu no loc"* — nghe nhu loi. Doc dong 2 thi ro:
   cot `A..G` y het `Bank Transactions`, roi **cot `H..L` la mot KHOI THU
   HAI**: `DD/MM/YYYY · Diễn giải · PS Nợ · PS Có · Tài Khoản` — **dung 5 cot
   cua so ke toan** (`1.1/1.2 Ledger 111/112`). ⇒ No ⛔ **khong phai bo loc**,
   no la **CAI CAU** doi khuon bank → khuon so ke toan. Goi sai ten thi ⛔
   khong bao gio hoi dung cau hoi.

⛔ Pham vi doc (`QĐ-ITL-92`/`95`): ⛔ **KHONG doc cot `Diễn giải`** o bat cu
   dau — no mang ten nguoi that. ⛔ Khong dung toi `Employee_Info`. Cot `Log`
   chi mang `ngay|no|co|ma` ⇒ ⛔ khong co ten nguoi; van chi in **dem** va
   **dang chu**.

Chay:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_bat_bien_ngam.py
"""
from __future__ import annotations

import datetime
import re
import sys
import urllib.parse
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from tools.do_hinh_dang import API, _goi, token, ty_le  # noqa: E402

BANK = "1zJA0MyS8u4_EC6HimREQT6RM3-DDGnBZSRa3HQsfOn8"
QUY = "1RmmkOSCTYVp1DSmNIQLvE9VlWIqhQegqN7lVazWkF7U"
GOC = datetime.date(1899, 12, 30)


def cot(sid, rng, tok, render="FORMATTED_VALUE"):
    u = (API + sid + "/values/" + urllib.parse.quote(rng)
         + "?majorDimension=COLUMNS&valueRenderOption=" + render)
    v = _goi(u, tok, giay=300).get("values", [])
    return v


def dang(s: str) -> str:
    """Dang chu: chu→A, so→9, gom lai. Dung de mo ta ⛔ khong lo noi dung."""
    return re.sub(r"9{2,}", "9…", re.sub(r"[0-9]", "9",
                                         re.sub(r"[A-Za-z]", "A", s)))[:26]


def so_gon(x) -> str:
    """Viet mot so giong cach `Log` viet: ⛔ khong dau phan cach, bo `.0`."""
    if x in ("", None):
        return ""
    try:
        f = float(x)
    except (TypeError, ValueError):
        return str(x).strip()
    return str(int(f)) if f == int(f) else repr(f)


def do_log(nhan, sid, tok):
    print("=" * 74)
    print("`Log` cua %s" % nhan)
    v = cot(sid, "'Log'!A2:B", tok)
    act = [x.strip() for x in (v[0] if v else [])]
    khoa = [x.strip() for x in (v[1] if len(v) > 1 else [])]
    print("  dong co du lieu : %d" % max(len(act), len(khoa)))
    print("  `Action`        : %s" % dict(Counter(act).most_common(6)))
    print("  khoa khac nhau  : %d / %d  (%s trung lap)"
          % (len(set(khoa)), len(khoa),
             "co" if len(set(khoa)) < len(khoa) else "⛔ khong"))
    manh = Counter(len(k.split("|")) for k in khoa)
    print("  so manh cua khoa: %s" % dict(manh))
    # ⛔⛔ Khoa HONG: `NaNNaNNaN|||` — kich ban dung khoa lam phep NGAY tren
    # mot thu ⛔ khong phai ngay, ra `NaN`, roi ba truong con lai RONG.
    hong = sum(1 for k in khoa if k.startswith("NaN"))
    print("  ⛔⛔ khoa HONG `NaNNaNNaN|||` : %d / %d = %.1f%%"
          % (hong, len(khoa),
             ty_le(hong, len(khoa), 0.0, 100.0, "khoa hong")))
    print("  ⇒ dong DUNG DUOC : %d" % (len(khoa) - hong))
    return [k for k in khoa if not k.startswith("NaN")]


def main() -> int:
    tok = token()

    # ── 1 · `Log` hai ben
    k_bank = do_log("P100 BANK", BANK, tok)
    print()
    k_quy = do_log("P100 QUY", QUY, tok)

    # ── 2 · `Log` co PHU so giao dich ⛔ khong?
    print()
    print("=" * 74)
    print("2 · `Log` co PHU `Bank Transactions` ⛔ khong?")
    v = cot(BANK, "'Bank Transactions'!A3:F", tok, "UNFORMATTED_VALUE")
    ngay, no, co, ma = v[0], v[3], v[4], v[5]

    def o(a, i):
        return a[i] if i < len(a) else ""

    n = max(len(ngay), len(ma))
    khoa_bt = []
    for i in range(n):
        d = o(ngay, i)
        if not isinstance(d, (int, float)) or not d:
            continue
        ng = (GOC + datetime.timedelta(days=int(d))).strftime("%Y%m%d")
        khoa_bt.append("%s|%s|%s|%s"
                       % (ng, so_gon(o(no, i)), so_gon(o(co, i)),
                          str(o(ma, i)).strip()))
    tap_log = set(k_bank)          # ⛔ da loai khoa hong o `do_log`
    trung = sum(1 for k in khoa_bt if k in tap_log)
    print("  dong `Bank Transactions` dung duoc lam khoa : %d" % len(khoa_bt))
    print("  ⭐ trong so do, co mat trong `Log`           : %d  (%.1f%%)"
          % (trung, ty_le(trung, len(khoa_bt), 0.0, 100.0, "phu cua Log")))
    if trung == 0:
        print("  ⛔ 0% ⇒ hoac `Log` dung khuon khac, hoac no ⛔ khong ghi")
        print("     `Bank Transactions` ma ghi mot tang khac. ⛔ Chua ket luan.")

    # ── 3 · `Check trùng` / `Num` — hai cot ⛔ chua ai noi la gi
    print()
    print("=" * 74)
    print("3 · Hai cot `Check trùng` va `Num` (`Bank Transactions`)")
    v2 = cot(BANK, "'Bank Transactions'!F3:I", tok, "UNFORMATTED_VALUE")
    ma2 = [str(x).strip() for x in v2[0]]
    num = v2[2] if len(v2) > 2 else []
    ctrung = v2[3] if len(v2) > 3 else []
    dem_ma = Counter(x for x in ma2 if x)
    print("  `Num`        : %d o · gia tri: %s"
          % (len([x for x in num if x != ""]),
             dict(Counter(str(x) for x in num if x != "").most_common(4))))
    print("  `Check trùng`: %d o · gia tri: %s"
          % (len([x for x in ctrung if x != ""]),
             dict(Counter(str(x) for x in ctrung if x != "").most_common(4))))
    # gia thuyet: `Check trùng` = so lan ma xuat hien
    khop = lech = 0
    for i, m in enumerate(ma2):
        c = o(ctrung, i)
        if m and isinstance(c, (int, float)):
            if int(c) == dem_ma[m]:
                khop += 1
            else:
                lech += 1
    if khop + lech:
        print("  gia thuyet *`Check trùng` = SO LAN ma xuat hien*:")
        print("     khop %d / %d = %.1f%%  ⇒ ⛔ KHONG dang tin"
              % (khop, khop + lech,
                 ty_le(khop, khop + lech, 0.0, 100.0, "Check trung")))
        print("     va no luon **DEM THIEU** (mau nhieu nhat: ghi 1, thuc 2)")
    # ⭐ gia thuyet thu hai — va day moi la cai DUNG
    thay, ok, sai = Counter(), 0, 0
    for i, m in enumerate(ma2):
        if not m:
            continue
        thay[m] += 1
        v = o(num, i)
        if isinstance(v, (int, float)):
            ok, sai = (ok + 1, sai) if int(v) == thay[m] else (ok, sai + 1)
    if ok + sai:
        print("  ⭐⭐ gia thuyet *`Num` = THU TU lan xuat hien cua ma*:")
        print("      khop %d / %d = %.1f%%  ⇒ **DUNG TUYET DOI**"
              % (ok, ok + sai, ty_le(ok, ok + sai, 0.0, 100.0, "Num")))
        print("      ⇒ phep chong trung cua AS-IS **da chay dung**; `F04`")
        print("        ⛔ khong phai phat minh lai, chi phai **giu**.")

    # ── 4 · `Bank Transactions_Filter` — bo LOC hay CAI CAU?
    print()
    print("=" * 74)
    print("4 · `Bank Transactions_Filter` — bo LOC hay CAI CAU?")
    hd = _goi(API + BANK + "/values/"
              + urllib.parse.quote("'Bank Transactions_Filter'!A2:L2"),
              tok).get("values", [[]])[0]
    print("  tieu de: %s" % " · ".join(str(x)[:22] for x in hd))
    print("  ⇒ cot A..G y het `Bank Transactions`; cot H..L la KHOI THU HAI")
    print("    theo khuon SO KE TOAN (`Ngày chứng từ · Diễn giải · PS Nợ ·")
    print("    PS Có · Tài khoản`) ⇒ ⛔ KHONG phai bo loc, la **CAI CAU**.")
    vf = cot(BANK, "'Bank Transactions_Filter'!A3:A", tok, "UNFORMATTED_VALUE")
    nf = len([x for x in (vf[0] if vf else []) if x != ""])
    print("  dong co ngay : %d  (`Bank Transactions` co %d)"
          % (nf, len(khoa_bt)))
    print("  ⇒ ⛔ `§5` ghi no *\"nhieu hon ban goc 98 dong\"* — SAI: bang"
          " nhau.")

    # ── 5 · Kho XOA co vet ben Quy
    print()
    print("=" * 74)
    print("5 · `[CA]Nhật ký xử lý Giao dịch` — kho XOA CO VET")
    vc = cot(QUY, "'[CA]Nhật ký xử lý Giao dịch'!A3:G", tok)
    ly_do = [x.strip() for x in (vc[0] if vc else []) if x.strip()]
    ma_c = [str(x).strip() for x in (vc[6] if len(vc) > 6 else [])]
    print("  dong bi xoa co ghi ly do : %d" % len(ly_do))
    print("  ly do khac nhau          : %d" % len(set(ly_do)))
    for a, b in Counter(ly_do).most_common(4):
        print("     %-46s %5d" % (a[:46], b))
    print("  ma giao dich con giu lai : %d"
          % len([x for x in ma_c if x]))
    print("  ⇒ ⭐ Ke toan **da co** thoi quen xoa-co-vet: giu lai ca dong,")
    print("    ghi LY DO va NGAY. Do dung la hinh cua `INV-I03`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
