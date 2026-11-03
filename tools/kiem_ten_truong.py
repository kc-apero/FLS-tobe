# -*- coding: utf-8 -*-
"""Cong `G1` — MOT TEN cho mot truong tren MOI man hinh (`BA-12 §1`).

    python tools/kiem_ten_truong.py          # 0 = dat · 1 = co ten la

⛔⛔⛔ **Vi sao cong nay ton tai.** Do 11/09 tren chinh ma man hinh:

    GGSheet `PM_Unpivot` cot 25  ->  "Reference number"
    Sao ke ngan hang             ->  "Reference number"   ← CUNG ten
    `man_f01_lenh.js:174`        ->  "Ma tham chieu"      ← ten thu ba
    `man_f01_lenh.js:248`        ->  "So chung tu"        ← ten thu tu
    `man_f01.js:150`             ->  "So chung tu"

⇒ **Hai ten cho mot truong, cach nhau 74 dong, trong CUNG mot tep.** Ke toan
  doc "Ma tham chieu" o luoi va "So chung tu" o bang ung vien cua **cung mot
  ngan keo**, roi ket luan chung la hai thu khac nhau. Do ⛔ khong phai bat
  tien — do la mot cho de **hieu sai du lieu**.

★ **Cong nay quet CA thu muc, ⛔ khong go tay danh sach tep.** Mot man hinh
  moi mai sau go lai chu cu se **DO ngay**, ⛔ khong cho ai nho ra luat nay.

⚠ ⛔ Cong ⛔ **khong** cam chu `ref` trong MA (`ref_tho`/`ref_canon` la hai
  **trang thai** cua cung truong — tho va da chuan hoa — va chung phai giu
  ten ay trong kho). No chi cam cac chuoi ay xuat hien lam **nhan cho nguoi
  doc**, tuc trong mot chuoi tieng Viet co dau.
"""
from __future__ import annotations

import pathlib
import re
import sys

GOC = pathlib.Path(__file__).resolve().parent.parent
MAN = GOC / "fls" / "web" / "tep"

# ⛔ Ten DUNG — mot ban khai, ⛔ khong rai rac trong ma.
TEN_DUNG = "Số chứng từ"

# ⛔ Ban DEN: nhung cach goi khac cho CUNG truong `Reference number`.
#   Them mot dong o day khi bat duoc mot ten la moi.
TEN_LA: tuple[str, ...] = (
    "Mã tham chiếu",
    "Ma tham chieu",
    "Số tham chiếu",
    "Mã chứng từ",
)

# ⛔ Chi soi tep man hinh. `.py` cua tang kho duoc phep noi `ref_canon`.
DUOI = (".js", ".html", ".css")


def soi(thu_muc: pathlib.Path = MAN) -> list[str]:
    """Danh sach loi. Rong = dat."""
    if not thu_muc.is_dir():
        raise SystemExit(f"⛔ khong do duoc: ⛔ khong thay {thu_muc}")
    loi: list[str] = []
    tep = [t for t in sorted(thu_muc.rglob("*")) if t.suffix in DUOI]
    if not tep:
        raise SystemExit(
            f"⛔ quet duoc 0 tep trong {thu_muc} — xanh tren tap RONG la "
            f"CHUA DO, ⛔ khong phai dat")
    for t in tep:
        for i, dong in enumerate(t.read_text(encoding="utf-8").splitlines(), 1):
            for la in TEN_LA:
                if la in dong:
                    loi.append(
                        f"{t.relative_to(GOC)}:{i}: goi truong "
                        f"`Reference number` la {la!r} — ten dung la "
                        f"{TEN_DUNG!r} (`BA-12 §1`)")
    return loi


def dem_ten_dung(thu_muc: pathlib.Path = MAN) -> int:
    """⛔ Bao nhieu cho DANG dung ten dung — de cong ⛔ khong xanh vi RONG."""
    return sum(
        1
        for t in thu_muc.rglob("*") if t.suffix in DUOI
        for d in t.read_text(encoding="utf-8").splitlines()
        if TEN_DUNG in d)


def main() -> int:
    loi = soi()
    n = dem_ten_dung()
    for x in loi:
        print("⛔ " + x)
    if loi:
        print(f"\n⛔ {len(loi)} cho goi sai ten truong")
        return 1
    if not n:
        print(f"⛔ ⛔ khong tim thay MOT cho nao dung {TEN_DUNG!r} — cong nay "
              f"dang xanh tren tap RONG, tuc no ⛔ chua do gi")
        return 1
    print(f"✅ ten truong THONG NHAT — {n} cho dung {TEN_DUNG!r}, "
          f"⛔ 0 ten la (quet {len(TEN_LA)} bien the)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
