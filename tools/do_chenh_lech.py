"""Đ3 · Do CHENH giua tang NHAP (67 sheet `R |`) va tang GOP (`Bank
Transactions`) — doc SONG, va **phan loai duoc**, ⛔ khong chi dem duoc.

⭐⭐ **Vi sao phep do nay lam duoc, trong khi `Đ1` chi dem duoc.**
   Cot `G = Source` cua `Bank Transactions` ghi **ten dung sheet `R |`** ma
   moi dong den tu do. ⇒ Tang gop **tu khai xuat xu tung dong**. Chenh vi the
   ⛔ khong con la mot so 7.294 mo, ma tach duoc **theo tung tai khoan**.

⭐ **Va dong 1 cua `Bank Transactions` la mot BO DEM SONG** (`8331` ref /
   `8339` source). Sheet **tu khai** so dong that cua no — nen ta co mot cach
   doi chung phep dem cua MINH voi phep dem cua CHINH cai so.

⛔⛔ **Tien de cu phai do lai truoc.** Hai so `16.625 → 9.331` cua `Đ1` deu
   den tu **ban chup offline** (tuoi 31–48 ngay, va ban xuat `.xlsx` co **5
   khuyet tat da ghi**). So voi ban chup thi mot lech tim duoc co the la
   *"FLS sai"*, cung co the la *"so da doi sau khi chup"* — hai thu do trong
   y het nhau. ⇒ `Đ3` do lai **ca hai dau** tren nguon SONG truoc khi phan
   loai bat cu cai gi.

── Pham vi doc (`QĐ-ITL-92`) ──────────────────────────────────────────────
   Cong cu nay buoc phai doc **o du lieu**, khac `Đ2` (chi metadata + tieu
   de). No doc **dung ba cot**:
       · `Date`              — de thu gia thuyet *"bo loc ngay"*
       · `Reference number`  — khoa doi sanh, la ma giao dich cua ngan hang
       · `Source`            — xuat xu, chi co o tang gop
   ⛔ Co Y ⛔ KHONG doc `Description` — cot duy nhat co the mang PII (ten
   nguoi, noi dung chuyen khoan). ⛔ Khong doc so tien: `Đ3` do **SO DONG**;
   phan TIEN de danh cho buoc sau.
   ⛔ Khong in noi dung o nao ra man hinh — chi in **so dem** va **ten sheet**.

Chay:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_chenh_lech.py
"""
from __future__ import annotations

import re
import sys
import urllib.parse
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from tools.do_hinh_dang import (  # noqa: E402
    API, _goi, doc_ban_khai, dong_dau, meta, token,
)

SID = "1zJA0MyS8u4_EC6HimREQT6RM3-DDGnBZSRa3HQsfOn8"

# `Bank Transactions`: dong 1 = bo dem, dong 2 = tieu de, dong 3+ = du lieu
GOP = "Bank Transactions"
GOP_NGAY, GOP_REF, GOP_NGUON = 0, 5, 6      # A · F · G
DONG_DAU_DL = 3                              # ca hai tang deu bat dau o dong 3


def chu_cot(i: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA."""
    s = ""
    i += 1
    while i:
        i, d = divmod(i - 1, 26)
        s = chr(65 + d) + s
    return s


def doc_cot(sid, dai, tok, tu_dong=DONG_DAU_DL, render="FORMATTED_VALUE",
            tho=False):
    """batchGet nhieu COT roi le. `dai` = [(ten_sheet, chi_so_cot), ...].

    ⛔⛔ **`render` ⛔ KHONG duoc de mac dinh cho cot MA.** Doc ma bang
    `FORMATTED_VALUE` thi Sheets tra ky hieu khoa hoc (`1.23E+15`) cho
    nhung ma so dai dang kieu SO, va **1.468 ma gop lai thanh 294** — mot
    lech HOAN TOAN GIA do chinh phep doc sinh ra. Da mac dung bay nay o
    ban dau `Đ3`. Cot NGAY thi nguoc lai: phai `FORMATTED_VALUE`, vi tho
    la so seri.

    ⭐⭐⭐ **`tho=True` — them 2026-09-08, va no VA MOT LO CUA CHINH GHI CHU
       TREN.** `QĐ-ITL-102` ⓶ khai cai bay *"`doc_cot` ep moi o ve chuoi"* la
       **"da va tan noi"**. Do lai ngay 08/09 tren mot anh chup THAT
       *(8.368 dong)*: **100% o la `str`** — ke ca voi
       `render="UNFORMATTED_VALUE"`.

       ⇒ Cu va ay chi doi **`render`** *(het ky hieu khoa hoc)*, no ⛔ **khong
         he** bo phep `str(x)` o dong duoi. Tuc **trieu chung** duoc chua, con
         **nguyen nhan** thi ⛔ khong — va cau *"da va tan noi"* trong tai lieu
         **⛔ khong dung**.

    ⚠ **Vi sao ⛔ KHONG doi mac dinh.** `str().strip()` la thu **9 cong cu
      hien co** dang dua vao *(chung so chuoi voi chuoi)*. Doi mac dinh la doi
      hanh vi cua ca 9 duong mot luot de phuc vu **mot** duong moi. ⇒ Duong
      moi phai **noi ra** rang no can o tho.

    ⛔ `tho=True` **giu nguyen kieu JSON** cua Sheets: so la so, chuoi la
      chuoi. Bat buoc cho lan ANH CHUP (`QĐ-ITL-110`) — mot anh chup ep kieu
      la mot anh chup **⛔ khong con la anh chup**.
    """
    ra = {}
    for i in range(0, len(dai), 60):
        lat = dai[i:i + 60]
        q = "&".join(
            "ranges=" + urllib.parse.quote(
                "'%s'!%s%d:%s" % (s, chu_cot(c), tu_dong, chu_cot(c)))
            for s, c in lat)
        d = _goi(API + sid + "/values:batchGet?" + q
                 + "&majorDimension=COLUMNS&valueRenderOption=" + render,
                 tok, giay=180)
        for khoa, kq in zip(lat, d.get("valueRanges", [])):
            v = kq.get("values", [])
            o = v[0] if v else []
            ra[khoa] = list(o) if tho else [str(x).strip() for x in o]
    return ra


def nam_cua(s: str):
    """Rut NAM tu mot o ngay da dinh dang.

    ⛔ Co y ⛔ KHONG doan dinh dang ngay/thang: `Đ3` chi can NAM de thu gia
    thuyet *"bo loc ngay"*, va NAM la phan duy nhat ⛔ khong bi anh huong boi
    cai bay hoan ngay↔thang da ghi o `itl-date-daymonth-swap`.
    """
    m = re.search(r"(19|20)\d{2}", s)
    return m.group(0) if m else None


def main() -> int:
    tok = token()
    d = meta(SID, tok)
    sh = {s["properties"]["title"]: s["properties"]["gridProperties"]
          for s in d["sheets"]}
    ten_r = sorted(t for t in sh if t.startswith("R |"))

    # ── 0 · bo dem SONG ma CHINH cai so tu khai (dong 1 cua tang gop)
    d1 = dong_dau(SID, [GOP], tok, n=2)[GOP]
    tu_khai = [str(x).strip() for x in d1[0]] if d1 else []
    print("=" * 74)
    print("0 · BO DEM SONG do CHINH cai so tu khai (dong 1 tang gop)")
    print("    ref = %s   ·   source = %s"
          % (tu_khai[GOP_REF] if len(tu_khai) > GOP_REF else "?",
             tu_khai[GOP_NGUON] if len(tu_khai) > GOP_NGUON else "?"))

    # ── 1 · TANG GOP: dem that + nhom theo xuat xu
    g = doc_cot(SID, [(GOP, GOP_NGAY), (GOP, GOP_NGUON)], tok)
    g_ngay = g[(GOP, GOP_NGAY)]
    g_ng = g[(GOP, GOP_NGUON)]
    # ⛔ ma phai doc THO — xem ghi chu o `doc_cot`
    g_ref = doc_cot(SID, [(GOP, GOP_REF)], tok,
                    render="UNFORMATTED_VALUE")[(GOP, GOP_REF)]
    n = max(len(g_ngay), len(g_ref), len(g_ng))

    def o(v, i):
        return v[i] if i < len(v) else ""

    co_gi = [i for i in range(n) if o(g_ngay, i) or o(g_ref, i) or o(g_ng, i)]
    co_ngay = [i for i in co_gi if o(g_ngay, i)]
    cut = [i for i in co_gi if not o(g_ngay, i)]
    theo_nguon = Counter(o(g_ng, i) for i in co_ngay)
    nam_gop = Counter(nam_cua(o(g_ngay, i)) or "?" for i in co_ngay)

    print()
    print("=" * 74)
    print("1 · TANG GOP `%s`" % GOP)
    print("    luoi khai              : %6d dong" % sh[GOP]["rowCount"])
    print("    co CHUT du lieu        : %6d" % len(co_gi))
    print("    co NGAY = dong THAT    : %6d" % len(co_ngay))
    print("    ⛔ dong CUT (⛔ khong ngay): %5d" % len(cut))
    print("    xuat xu khac nhau      : %6d" % len(theo_nguon))
    print("    theo NAM: %s"
          % "  ".join("%s=%d" % kv for kv in sorted(nam_gop.items())))

    # ── 2 · TANG NHAP: ban khai -> cot Date -> dem dong that
    bang = dong_dau(SID, ten_r, tok, n=2)
    khai = {t: doc_ban_khai(bang.get(t, [])) for t in ten_r}
    can = [(t, khai[t]["Date"]) for t in ten_r if "Date" in khai[t]]
    cot = doc_cot(SID, can, tok)

    nhap = {}
    nam_nhap = Counter()
    for t, ci in can:
        v = [x for x in cot[(t, ci)] if x]
        nhap[t] = len(v)
        for x in v:
            nam_nhap[nam_cua(x) or "?"] += 1
    luoi_nhap = sum(sh[t]["rowCount"] for t in ten_r)

    print()
    print("=" * 74)
    print("2 · TANG NHAP — %d sheet `R |`" % len(ten_r))
    print("    luoi khai              : %6d dong" % luoi_nhap)
    print("    co NGAY = dong THAT    : %6d" % sum(nhap.values()))
    print("    theo NAM: %s"
          % "  ".join("%s=%d" % kv for kv in sorted(nam_nhap.items())))

    # ── 3 · PHAN LOAI (`Đ-4`: lech phai PHAN LOAI duoc, ⛔ khong chi dem duoc)
    tong_nhap, tong_gop = sum(nhap.values()), len(co_ngay)
    print()
    print("=" * 74)
    print("3 · PHAN LOAI CHENH   %d nhap  ->  %d gop   (lech %+d)"
          % (tong_nhap, tong_gop, tong_gop - tong_nhap))

    b_dem = (luoi_nhap - tong_nhap) + (sh[GOP]["rowCount"] - tong_gop)
    print()
    print("  B1 · DEM KHAC DON VI (o LUOI vs dong THAT) : %6d o ma" % b_dem)
    print("       neu dem bang LUOI o mot dau va bang DONG o dau kia thi mot")
    print("       phan cua 'chenh' ⛔ khong phai dong nao ca.")

    chet = sorted(t for t in nhap if nhap[t] and not theo_nguon.get(t))
    print()
    print("  B2 · NGUON CHET — co dong o tang NHAP, ⛔ 0 dong len tang GOP")
    print("       %d sheet · %d dong" % (len(chet), sum(nhap[t] for t in chet)))
    for t in chet:
        print("         ⛔ %-46s %5d" % (t, nhap[t]))

    la = sorted(x for x in theo_nguon if x not in nhap)
    print()
    print("  B3 · XUAT XU LA — co o tang GOP, ⛔ khong ung sheet `R |` nao")
    print("       %d xuat xu · %d dong"
          % (len(la), sum(theo_nguon[x] for x in la)))
    for x in la[:15]:
        print("         ⛔ %-46s %5d" % ((x[:46] or "(TRONG)"), theo_nguon[x]))

    hut, du = [], []
    for t in sorted(nhap):
        if t in chet:
            continue
        dl = theo_nguon.get(t, 0) - nhap[t]
        if dl < 0:
            hut.append((t, dl))
        elif dl > 0:
            du.append((t, dl))
    print()
    print("  B4 · LECH TUNG TAI KHOAN (ca hai dau deu co dong)")
    print("       %d sheet HUT (nhap > gop) : %d dong"
          % (len(hut), -sum(x for _, x in hut)))
    for t, dl in sorted(hut, key=lambda x: x[1])[:15]:
        print("         ⛔ %-46s %+5d  (nhap %d / gop %d)"
              % (t, dl, nhap[t], theo_nguon.get(t, 0)))
    print("       %d sheet DU (gop > nhap)  : %d dong"
          % (len(du), sum(x for _, x in du)))
    for t, dl in sorted(du, key=lambda x: -x[1])[:15]:
        print("         ⚠ %-46s %+5d  (nhap %d / gop %d)"
              % (t, dl, nhap[t], theo_nguon.get(t, 0)))

    khop = [t for t in nhap if t not in chet and theo_nguon.get(t) == nhap[t]]
    print()
    print("  B5 · KHOP DUNG TUNG DONG : %d sheet · %d dong"
          % (len(khop), sum(nhap[t] for t in khop)))

    rong = sorted(t for t in nhap if not nhap[t])
    print()
    print("  B6 · SHEET `R |` RONG ca hai dau : %d" % len(rong))
    for t in rong:
        print("         · %s  (luoi %d)" % (t, sh[t]["rowCount"]))

    # ── 4 · ⭐ CUNG SO LUONG ⛔ CHUA PHAI CUNG NHUNG DONG AY.
    #        So bang TAP KHOA `Reference number` — day moi la phep chung minh.
    print()
    print("=" * 74)
    print("4 · DOI TAP KHOA `Reference number` (⛔ khong chi doi so dem)")
    can_ref = [(t, khai[t]["Reference number"]) for t in ten_r
               if "Reference number" in khai[t] and nhap.get(t)]
    cr = doc_cot(SID, can_ref, tok, render="UNFORMATTED_VALUE")
    ref_nhap = Counter()
    for t, ci in can_ref:
        ref_nhap.update(x for x in cr[(t, ci)] if x)
    ref_gop = Counter(o(g_ref, i) for i in co_ngay if o(g_ref, i))

    thieu = ref_nhap - ref_gop          # co o NHAP, ⛔ khong len GOP
    thua = ref_gop - ref_nhap           # co o GOP, ⛔ khong co o NHAP
    print("    ma o tang NHAP : %6d (%d ma khac nhau)"
          % (sum(ref_nhap.values()), len(ref_nhap)))
    print("    ma o tang GOP  : %6d (%d ma khac nhau)"
          % (sum(ref_gop.values()), len(ref_gop)))
    print("    ⛔ NHAP co, GOP ⛔ khong : %d" % sum(thieu.values()))
    print("    ⛔ GOP co, NHAP ⛔ khong : %d" % sum(thua.values()))

    # ── 5 · Suc khoe cua chinh cai KHOA (`INV-I04b` se dua vao no)
    khong_ma = len(co_ngay) - sum(ref_gop.values())
    trung = {k: v for k, v in ref_gop.items() if v > 1}
    print()
    print("=" * 74)
    print("5 · SUC KHOE KHOA DOI SANH — `INV-I04b` se dua vao dung cot nay")
    print("    ⛔ dong CO ngay nhung ⛔ KHONG co ma : %d" % khong_ma)
    print("    ⛔ ma bi TRUNG : %d ma / %d dong"
          % (len(trung), sum(trung.values())))
    print("       (⛔ khong in ma — chi dem. Cot `Check trùng` cua chinh sheet")
    print("        rat co the dang lam dung phep dem nay.)")

    # ── 6 · ⛔⛔ Tong ma BANG NHAU nhung so ma KHAC NHAU thi LECH.
    #        => ma bi DOI tren duong di. Phan loai theo tung tai khoan, roi
    #        theo DANG chu (⛔ khong in noi dung ma).
    print()
    print("=" * 74)
    print("6 · MA BI DOI TREN DUONG DI — phan loai")
    theo_sheet = {}
    for t, ci in can_ref:
        theo_sheet[t] = Counter(x for x in cr[(t, ci)] if x)
    gop_theo_sheet = {}
    for i in co_ngay:
        if o(g_ref, i):
            gop_theo_sheet.setdefault(o(g_ng, i), Counter())[o(g_ref, i)] += 1

    xau = []
    for t, cn in theo_sheet.items():
        cg = gop_theo_sheet.get(t, Counter())
        lech = sum((cn - cg).values())
        if lech:
            xau.append((lech, t, cn, cg))
    xau.sort(reverse=True, key=lambda x: x[0])
    print("    %d / %d tai khoan co ma lech · tong %d dong"
          % (len(xau), len(theo_sheet), sum(x[0] for x in xau)))

    def dang(s: str) -> str:
        """Dang chu cua mot ma: chu->A, so->9, con lai giu nguyen."""
        return re.sub(r"9{3,}", "9…", re.sub(r"[0-9]", "9",
                                             re.sub(r"[A-Za-z]", "A", s)))[:18]

    for lech, t, cn, cg in xau[:8]:
        dn = Counter(dang(k) for k in (cn - cg).elements())
        dg = Counter(dang(k) for k in (cg - cn).elements())
        print("      ⛔ %-44s %4d dong" % (t[:44], lech))
        print("           nhap: %s" % ("  ".join(
            "%s×%d" % kv for kv in dn.most_common(3)) or "—"))
        print("           gop : %s" % ("  ".join(
            "%s×%d" % kv for kv in dg.most_common(3)) or "—"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
