"""Đ5-a · Do TRONG TAI SO DU — `2. CCR` dong **226** `DIF = Treasury − Accounting`.

⭐⭐ **Vi sao dong nay quan trong hon moi dong khac trong bo AS-IS.**
   Ca lan nhap *(bank + quy)* co dung **MOT** thuoc do dung/sai: cuoi ngay, so
   du **Treasury** *(ngan hang bao)* phai bang so du **Accounting** *(so ke
   toan cong ra)*. Bo tai lieu ghi luat ay la *"`DIF = 0` dung tung dong"* va
   xep bac `K0` — **⛔ chua ai do lan nao**, vi ⛔ chua co quyen doc. Owner chia
   quyen 2026-09-07.

── Hinh dang that (do duoc 2026-09-07) ────────────────────────────────────
   `2. CCR`  229 dong × 655 cot · **mot cot = MOT NGAY** (tu `31-Dec-24`)
      dong  5 = NGAY          dong 6..9 = ty gia USD/SGD/HKD
      dong 30 = `EBTS` Ending Cash Balance **TREASURY**, chi tiet o 32..123
      dong 125= `EBA`  Ending Cash Balance **ACCOUNTING**, tong o **127**
      dong 226= `DIF`  = `Σ(32..123 quy VND) − 127`   *(doc duoc tu cong thuc)*

⛔⛔ **BA CAI BAY o phep do nay, mac ca ba deu ra so SAI to.**

   ⓵ **Dem tho thi 412/644 o "khac 0"** — nghe nhu tham hoa. Nhung phan lon la
      **BUI DAU PHAY DONG** *(`1.52587890625e-05` = 2⁻¹⁶)*, sinh ra tu chinh
      phep nhan ty gia cua bang tinh, ⛔ **khong phai tien**. => Phai phan loai
      theo **DO LON**, moc la **dung sai da chot 1.000 VND** (`QĐ-ITL-57`).

   ⓶ **49 ngay vuot dung sai** — cung sai. Mot lech keo dai qua nhieu ngay la
      **MOT su kien**, ⛔ khong phai N su kien. Gom lai chi con **2**.

   ⓷ ⛔⛔ **Va ca hai con so tren van con sai, vi TEP NAY LA BAN CHUP.**
      `Bank Transactions` va `Cash Ledger Transactions` trong chinh no **dung
      o 19-Aug-2026**, trong khi `P100` song chay toi 6-Sep-2026. Nhung cot
      ngay thi **dung san toi 6-Oct-2026** va o nao cung co so, vi cong thuc
      **chuyen tiep** gia tri hom truoc (`WJ32 = WI32`).
      ⇒ Mo tep ra hom nay se thay **cot cua NGAY HOM NAY day so** — va nhung
      so ay **19 ngay tuoi**. Cai *"lech 9,53 ty keo dai 48 ngay"* chinh la
      **DUOI DONG CUNG** cua ban chup, ⛔ khong phai tien mat.
      ⇒ Cong cu nay **tu tim ngay song cuoi** roi **cat duoi** truoc khi dem.

── Luat rut ra ────────────────────────────────────────────────────────────
   Mot bang tinh co cot dung san cho tuong lai + cong thuc chuyen tiep thi no
   **⛔ khong bao gio trong nhu da cu**. Cung ho voi `#N/A` trong nhu "da day"
   (`Đ4-a`). ⇒ **Moi cua doc phai tra TUOI cua so, ⛔ khong chi tra so.**

⛔ Pham vi doc (`QĐ-ITL-95`): doc **so tien**, khac `Đ3`/`Đ4-a`. Nhung chi doc
   **hai dong tong** (`127`, `226`) + dong ngay + cot ngay cua hai so giao
   dich. ⛔ Khong doc 92 dong so du chi tiet, ⛔ khong doc mot giao dich nao.

Chay:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_trong_tai.py
"""
from __future__ import annotations

import datetime
import sys
import urllib.parse

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from tools.do_hinh_dang import API, _goi, token, ty_le  # noqa: E402

SID = "1axCTQ8GA2YO-QVL8pSoDZ0843J0XZp06pSmYcl8xS-Q"
BANG, DONG_NGAY, DONG_KT, DONG_DIF = "2. CCR", 5, 127, 226
SO_GIAO_DICH = ("Bank Transactions", "Cash Ledger Transactions")

# `QĐ-ITL-57` — dung sai 1.000 VND tuyet doi. Dung chung MOT thuoc voi phan
# con lai cua bo, ⛔ khong tu nghi ra nguong moi.
DUNG_SAI = 1000.0
BUI = 1.0                                   # duoi 1 dong ⇒ ⛔ khong the la tien
GOC = datetime.date(1899, 12, 30)           # goc so seri cua bang tinh


def doc(rng: str, render: str, tok: str, theo_cot: bool = False):
    u = (API + SID + "/values/" + urllib.parse.quote(rng)
         + "?valueRenderOption=" + render
         + ("&majorDimension=COLUMNS" if theo_cot else ""))
    return _goi(u, tok, giay=240).get("values", [])


def ngay_song_cuoi(tok) -> datetime.date:
    """Ngay MOI NHAT that su co giao dich trong chinh tep nay.

    ⛔ ⛔ Khong duoc lay cot cuoi cua `2. CCR`: cot ngay dung san toi tuong lai
    va o nao cung co so nho cong thuc chuyen tiep. Tuoi that phai hoi **so
    giao dich**, ⛔ khong hoi **bang tong hop**."""
    ra = []
    for s in SO_GIAO_DICH:
        v = doc("'%s'!A3:A" % s, "UNFORMATTED_VALUE", tok, theo_cot=True)
        so = [x for x in (v[0] if v else []) if isinstance(x, (int, float))]
        if so:
            ra.append(GOC + datetime.timedelta(days=int(max(so))))
    if not ra:
        raise SystemExit("⛔ khong xac dinh duoc tuoi cua tep")
    return max(ra)


def main() -> int:
    tok = token()
    tho = doc("'%s'!A1:ZZ%d" % (BANG, DONG_DIF), "UNFORMATTED_VALUE", tok)
    ngay_so = doc("'%s'!A%d:ZZ%d" % (BANG, DONG_NGAY, DONG_NGAY),
                  "UNFORMATTED_VALUE", tok)[0]
    dif = tho[DONG_DIF - 1]
    kt = tho[DONG_KT - 1]

    song = ngay_song_cuoi(tok)
    hom_nay = datetime.date.today()
    print("=" * 74)
    print("TUOI CUA TEP  (hoi SO GIAO DICH, ⛔ khong hoi bang tong hop)")
    print("  giao dich moi nhat trong tep : %s" % song)
    print("  hom nay                      : %s" % hom_nay)
    print("  ⛔ TEP CU  %d ngay" % (hom_nay - song).days)

    def d(i):
        x = ngay_so[i] if i < len(ngay_so) else ""
        return (GOC + datetime.timedelta(days=int(x))
                if isinstance(x, (int, float)) and x else None)

    so = [(i, dif[i]) for i in range(len(dif))
          if isinstance(dif[i], (int, float)) and d(i)]
    trong_ky = [(i, x) for i, x in so if d(i) <= song]
    duoi = [(i, x) for i, x in so if d(i) > song]

    print()
    print("=" * 74)
    print("CAT DUOI DONG CUNG")
    print("  cot co so           : %d  (%s → %s)"
          % (len(so), d(so[0][0]), d(so[-1][0])))
    print("  ⭐ ngay CO du lieu   : %d  (→ %s)" % (len(trong_ky), song))
    print("  ⛔ duoi DONG CUNG    : %d ngay — cot dung san cho tuong lai,"
          % len(duoi))
    print("     cong thuc chuyen tiep so hom truoc ⇒ TRONG nhu da cu.")
    if duoi:
        print("     (dem ca duoi nay thi 'lech' phong tu 1 ngay len %d ngay)"
              % (len(duoi) + 1))

    khong = [p for p in trong_ky if p[1] == 0]
    bui = [p for p in trong_ky if 0 < abs(p[1]) < BUI]
    giua = [p for p in trong_ky if BUI <= abs(p[1]) < DUNG_SAI]
    vuot = [p for p in trong_ky if abs(p[1]) >= DUNG_SAI]

    print()
    print("=" * 74)
    print("PHAN LOAI THEO DO LON — chi tren %d ngay CO du lieu" % len(trong_ky))
    for nhan, ds, ghi in (
        ("= 0 dung tung dong", khong, "luat GIU tuyet doi"),
        ("bui dau phay dong  ", bui, "< 1 VND — ⛔ KHONG phai tien"),
        ("trong dung sai     ", giua, "< 1.000 VND (`QĐ-ITL-57`)"),
        ("⛔ VUOT dung sai    ", vuot, ">= 1.000 VND"),
    ):
        print("  %s : %4d ngay (%5.1f%%)  %s"
              % (nhan, len(ds),
                 ty_le(len(ds), len(trong_ky), 0.0, 100.0, nhan), ghi))

    dat = len(khong) + len(bui) + len(giua)
    print()
    print("  ⇒ NGAY DAT luat : %d / %d = %.1f%%"
          % (dat, len(trong_ky),
             ty_le(dat, len(trong_ky), 0.0, 100.0, "ngay dat")))

    print()
    print("=" * 74)
    print("KET LUAN")
    print("  ⛔ Luat ghi trong tai lieu — *\"`DIF = 0` DUNG TUNG DONG\"* — SAI")
    print("     nhu da ghi: %d/%d ngay mang bui dau phay dong khac 0. Doi"
          % (len(bui), len(trong_ky)))
    print("     'dung tung dong' tren mot bang co NHAN TY GIA la bat kha.")
    print("     Luat dung phai la  |DIF| < 1.000 VND  (`QĐ-ITL-57`).")
    print()
    print("  ⭐ Va theo thuoc DUNG thi trong tai **GIU**: %d/%d ngay dat,"
          % (dat, len(trong_ky)))
    print("     va ⛔ KHONG mot ngay nao roi vao khoang giua 1 va 1.000 VND")
    print("     ⇒ phan bo **sach**: hoac la bui, hoac la ty.")
    if vuot:
        print()
        print("  ⛔ %d ngay vuot dung sai:" % len(vuot))
        for i, x in sorted(vuot, key=lambda p: -abs(p[1]))[:10]:
            cach = (song - d(i)).days
            print("     %s  %20s VND   %s"
                  % (d(i), format(x, ",.0f"),
                     "⚠ la NGAY CUOI cua tep — nhieu kha nang chua chot xong"
                     if cach == 0 else ""))
    print()
    print("  ⛔⛔ `GAP-ORA-09` ⛔ CHUA dong: tep nay la BAN CHUP %d ngay tuoi."
          % (hom_nay - song).days)
    print("      Trong tai chi do duoc tren du lieu den %s. Muon cong SONG" % song)
    print("      thi phai co ban A-CCR **dang chay**, ⛔ khong phai ban sao.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
