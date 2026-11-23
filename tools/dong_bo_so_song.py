# -*- coding: utf-8 -*-
"""DONG BO so trong tai lieu theo phep do cua `tools/kiem_so_song.py`.

    python tools/dong_bo_so_song.py            # xem truoc, ⛔ KHONG ghi
    python tools/dong_bo_so_song.py --ghi      # ghi that

⛔⛔⛔ **Vi sao cong cu nay ton tai, va vi sao no ⛔ KHONG phai mot phep
   quet-thay.**

Ngay 10/09 toi dong bo tai lieu bang `sed`-kieu quet-thay `3.464` → `3.487`
tren ca bo. No **pha mot con so THAT** o `Ket-qua-Phan-loai-4-loai-o.md`, noi
`3.464` la **so dong cua mot sheet xung dot Google** — mot con so ⛔ khong lien
quan gi, tinh co trung. Phai `git checkout` de cuu.

⇒ Bai hoc ⛔ **khong** phai *"dung sua tai lieu bang may"*. No la:
  ***"dung sua bang MOT CHUOI — sua bang chinh BAN KHAI da noi con so ay o
  DAU"***.

★ Cong `kiem_so_song` **da co** ban khai ay: moi `Muc` mang `file` + `mau`
  *(bieu thuc chinh quy khop **DUNG MOT LAN**)* + `gia` *(gia tri MAY do)*.
  Cong cu nay:

    ⓐ chay dung `khai()` cua cong — ⛔ khong dung mot danh sach thu hai;
    ⓑ voi moi muc LECH, thay **dung tung NHOM bat duoc**, giu nguyen moi
       ky tu ngoai nhom *(ke ca dau cau, dam, khoang trang)*;
    ⓒ **BO QUA** muc khop `0` hay `>=2` lan — do la luc cong noi *"toi ⛔
       khong biet minh dang so voi cho nao"*, va sua mu o day dung la cai
       loi 10/09.

⛔ Va no ⛔ **khong** dong duoc muc nao sau khi chay: cong van la cong, chay
  lai `kiem_so_song` de biet ket qua. Cong cu nay chi **soan**, ⛔ khong phan
  quyet.

⚠⚠ **Cai no ⛔ KHONG lam, va phai lam bang TAY:** doi mot con so ⛔ khong sua
   duoc **cau van quanh no**. Vi du: so dong `6.617 → 8.387` vi so **duoc dung
   lai** `10/09` — cau *"sau khi nap tang `R |`"* van dung, nhung cau *"1.772
   dong bi loai vi ngay mo ho"* thi **da sai** *(chung da vao so o luot bu)*.
   Cong cu nay sua **con so**; ⛔ **nguoi** sua **cau**.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from tools.kiem_so_song import (TAI_LIEU_MAC_DINH as GOC_TL,  # noqa: E402
                                do_may, khai)


def _thay_theo_nhom(khop: re.Match, gia: tuple[str, ...]) -> str:
    """Chuoi da khop, voi **tung nhom** thay bang gia tri may.

    ⛔ Di **tu phai sang trai** — thay tu trai lam moi `span` phia sau lech di
      so ky tu vua doi, va cac nhom sau se ghi **nham cho**.

    ⛔⛔⛔ **`span(i)` la vi tri trong CA TEP, ⛔ KHONG phai trong chuoi da
       khop** — nen phai tru `khop.start()`. Ban dau toi quen phep tru ay, va
       **ban xem truoc ⛔ khong he lo ra**: no chi in `nhom i: cu → moi`, tuc
       no in **y dinh** chu ⛔ khong in **ket qua**.

       ⇒ Bai hoc: mot ban *"xem truoc"* ma ⛔ khong in **dung cai se duoc
         ghi** thi no ⛔ khong phai mot ban xem truoc — no la mot loi hua.
         Nay ham nay tra **chuoi ket qua that**, va nguoi goi in chinh no.
    """
    ra = khop.group(0)
    goc = khop.start()
    for i in range(len(gia), 0, -1):
        a, b = khop.span(i)
        if a < 0:
            continue
        ra = ra[:a - goc] + gia[i - 1] + ra[b - goc:]
    return ra


def soan(ghi: bool) -> int:
    may = do_may()
    muc = khai(may, GOC_TL)
    theo_file: dict[str, list] = {}
    for m in muc:
        theo_file.setdefault(m.file, []).append(m)

    doi = bo_qua = 0
    for ten_file, ds in sorted(theo_file.items()):
        f = GOC_TL / ten_file
        if not f.exists():
            print(f"⛔ ⛔ khong thay {ten_file}")
            continue
        goc = f.read_text(encoding="utf-8")
        moi = goc
        for m in ds:
            khop = list(re.finditer(m.mau, moi))
            if len(khop) != 1:
                # ⛔ Cong da noi no ⛔ khong do duoc — ⛔ KHONG sua mu o day.
                print(f"  ⏭ BO QUA {m.ten}: mau khop {len(khop)} lan")
                bo_qua += 1
                continue
            k = khop[0]
            if len(k.groups()) != len(m.gia):
                print(f"  ⏭ BO QUA {m.ten}: so nhom ⛔ khong khop so gia tri")
                bo_qua += 1
                continue
            if tuple(k.groups()) == tuple(m.gia):
                continue
            cu, thay = k.group(0), _thay_theo_nhom(k, m.gia)
            moi = moi[:k.start()] + thay + moi[k.end():]
            # ⛔ In **dung cai se duoc ghi**, ⛔ khong in y dinh. Mot ban xem
            #   truoc chi in "nhom 1: a → b" se **giau** mot loi cat chuoi —
            #   va no da giau that mot lan, 11/09.
            print(f"  ✎ {m.ten}\n      CU  : {cu[:130]}\n"
                  f"      MOI : {thay[:130]}")
            doi += 1
        if moi != goc:
            if ghi:
                f.write_text(moi, encoding="utf-8")
            print(f"{'✅ da ghi' if ghi else '(xem truoc)'} {ten_file}")
    print(f"\n{doi} muc soan · {bo_qua} muc BO QUA (cong ⛔ khong do duoc)")
    if not ghi:
        print("⛔ ⛔ CHUA GHI — them `--ghi` de ghi that")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ghi", action="store_true", help="ghi that vao tai lieu")
    return soan(p.parse_args().ghi)


if __name__ == "__main__":
    raise SystemExit(main())
