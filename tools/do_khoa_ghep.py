"""Đ4-a · Do CAI KHOA cua phep ghep `Mapping L1` — kiem gia thuyet 33,8%.

⭐⭐ **Gia thuyet den tu `Đ3`.** `Đ3` do duoc: **45% ma** o `Bank Transactions`
   luu **kieu SO**, phan con lai kieu CHU. Trong Google Sheets, `VLOOKUP` mot
   **so** vao mot cot **chu** *(hoac nguoc lai)* thi **⛔ KHONG khop** — va no
   ⛔ khong bao loi, chi tra `#N/A` hoac de trong. => Neu hai dau cua phep ghep
   `Mapping L1` lech KIEU, thi mot phan ty le ghep thap **⛔ khong phai do
   thieu du lieu**, ma do **kieu o**.

   Do la mot gia thuyet **co the sai**, va cong cu nay ton tai de **thu no**,
   ⛔ khong phai de xac nhan no. Neu hai dau cung kieu thi gia thuyet **chet**,
   va do cung la mot ket qua.

── Duong ghep that (do duoc 2026-09-07) ───────────────────────────────────
   `Transaction Mapping L1`  cot **1** `Số chứng từ`   *(hdr dong 3, dl dong 4)*
        │  VLOOKUP
        v
   `[Importrange]PM_Unpivot` cot **25** `Reference number` = cot **Z**
                                                     *(hdr dong 2, dl dong 3)*
   Cot 7..21 cua `Mapping L1` la phan **keo ve tu `PM_Unpivot`**; cot **13**
   `ID PMLine` la o de kiem *"dong nay co ghep duoc ⛔ hay khong"*.

── Ba phep dem, va phai phan biet cho ro ──────────────────────────────────
   `M_chuoi`  hai dau co cung ma **neu doi ca hai ve chuoi**  <- **dat duoc**
   `M_kieu`   hai dau co cung ma **VA cung kieu o**           <- **Sheets thay**
   `M_that`   so dong `Mapping L1` thuc su co `ID PMLine`     <- **dang co**
   ⛔⛔ `M_that` PHAI loai `#N/A`. Ban dau toi dem "o ⛔ khong rong" va ra
      **10.777 / 10.194 = 105,7%** — mot ty le **⛔ khong the co**, va do la
      dau hieu duy nhat cho thay phep dem sai. `#N/A` la mot **gia tri hien
      thi**, ⛔ khong phai o trong: co 7.372 o nhu vay. => Ai nhin cot ay bang
      mat se thay no **da day**, trong khi 72% la loi.
   ⇒ `M_chuoi − M_kieu` = so dong **mat CHI VI kieu o**. Do la con so phai bao.

⛔ Pham vi doc: `QĐ-ITL-92` — chi cot **khoa** va cot **ID PMLine**. ⛔ Khong
   doc `Diễn giải` (PII). ⛔ Khong in noi dung ma.

Chay:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_khoa_ghep.py
"""
from __future__ import annotations

import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.canon.o_loi import la_o_loi  # noqa: E402
from tools.do_chenh_lech import doc_cot  # noqa: E402
from tools.do_hinh_dang import meta, token, ty_le  # noqa: E402

SID = "1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E"

L1, L1_KHOA, L1_PMLINE, L1_DONG1 = "Transaction Mapping L1", 1, 13, 4
PM, PM_KHOA, PM_DONG1 = "[Importrange]PM_Unpivot", 25, 3


def kieu_o(x: str) -> str:
    """Sheets se coi o nay la SO hay CHU? Doc bang UNFORMATTED nen mot o so
    tra ve dang `123` / `1.5`, con o chu giu nguyen ky tu."""
    if not x:
        return "trong"
    try:
        float(x)
    except ValueError:
        return "chu"
    return "so"


def lay(sid, sheet, cot, dong1, tok, render):
    return doc_cot(sid, [(sheet, cot)], tok, tu_dong=dong1,
                   render=render)[(sheet, cot)]


def main() -> int:
    tok = token()
    d = meta(SID, tok)
    sh = {s["properties"]["title"]: s["properties"]["gridProperties"]
          for s in d["sheets"]}

    k_l1 = [x for x in lay(SID, L1, L1_KHOA, L1_DONG1, tok,
                           "UNFORMATTED_VALUE") if x]
    k_pm = [x for x in lay(SID, PM, PM_KHOA, PM_DONG1, tok,
                           "UNFORMATTED_VALUE") if x]
    cot13 = lay(SID, L1, L1_PMLINE, L1_DONG1, tok, "FORMATTED_VALUE")
    # ⛔ `#N/A` la GIA TRI hien thi, ⛔ khong phai o trong — xem docstring
    # ⭐ Luat "the nao la o loi" chi co MOT ban khai trong ca he:
    # `fls/canon/o_loi.py`. Ban dau toi go tay lai phep thu tien-to o day va
    # `tests/canon/test_o_loi.py::test_CHI_MOT_BAN_KHAI_trong_ca_he` **do
    # ngay** — dung cai cong ay sinh ra de chan. ⇒ dung ban goc.
    loi13 = [x for x in cot13 if la_o_loi(x)]
    pmline = [x for x in cot13 if x and not la_o_loi(x)]

    print("=" * 74)
    print("DUONG GHEP  `%s`!cot %d  ->  `%s`!cot %d"
          % (L1, L1_KHOA, PM, PM_KHOA))
    print("  `%s` : luoi %d · khoa co gia tri %d"
          % (L1, sh[L1]["rowCount"], len(k_l1)))
    print("  `%s` : luoi %d · khoa co gia tri %d"
          % (PM, sh[PM]["rowCount"], len(k_pm)))

    t_l1 = Counter(kieu_o(x) for x in k_l1)
    t_pm = Counter(kieu_o(x) for x in k_pm)
    print()
    print("=" * 74)
    print("1 · KIEU O cua khoa, HAI DAU")
    print("  ben BANK (`Mapping L1`) : %s" % dict(t_l1))
    print("  ben PM   (`PM_Unpivot`) : %s" % dict(t_pm))

    # tap khoa theo CHUOI (dat duoc) va theo (chuoi, kieu) (Sheets thay)
    pm_chuoi = set(k_pm)
    pm_kieu = {(x, kieu_o(x)) for x in k_pm}
    m_chuoi = sum(1 for x in k_l1 if x in pm_chuoi)
    m_kieu = sum(1 for x in k_l1 if (x, kieu_o(x)) in pm_kieu)
    m_that = len(pmline)

    print()
    print("=" * 74)
    print("2 · BA PHEP DEM")
    print("  M_chuoi  hai dau cung ma neu ep ve CHUOI : %5d  (%.1f%% cua %d)"
          % (m_chuoi, 100.0 * m_chuoi / max(len(k_l1), 1), len(k_l1)))
    print("  M_kieu   cung ma VA cung KIEU (Sheets)   : %5d  (%.1f%%)"
          % (m_kieu, 100.0 * m_kieu / max(len(k_l1), 1)))
    # ⛔ khoang khai TRUOC: mot ty le ghep ⛔ khong the vuot 100%
    print("  M_that   dong that su co `ID PMLine`     : %5d  (%.1f%%)"
          % (m_that, ty_le(m_that, len(k_l1), 0.0, 100.0, "M_that")))
    print("  ⛔ o mang `#N/A` o chinh cot ay            : %5d  (%.1f%% cua %d o)"
          % (len(loi13), 100.0 * len(loi13) / max(len(cot13), 1), len(cot13)))

    print()
    print("=" * 74)
    print("3 · KET LUAN")
    mat_kieu = m_chuoi - m_kieu
    if mat_kieu:
        print("  ⛔⛔ MAT CHI VI KIEU O : %d dong (%.1f%% cua ben bank)"
              % (mat_kieu, 100.0 * mat_kieu / max(len(k_l1), 1)))
        print("      Ma CO o ca hai dau, nhung Sheets ⛔ khong khop vi mot ben")
        print("      la SO con ben kia la CHU. `F04` phai EP VE CHUOI khi nap.")
    else:
        print("  ⭐ GIA THUYET CHET: hai dau ⛔ khong lech kieu o cho nao ma")
        print("     ca hai deu co ma. Ty le ghep thap ⛔ KHONG phai do kieu o —")
        print("     phai tim nguyen nhan khac. Day cung la mot ket qua.")
    print("  · tran cua phep ghep nay la %d — vi `PM_Unpivot` chi co tung ay"
          % len(k_pm))
    print("    ma. Ghep %d/%d = %.1f%% vi the la **gan KICH TRAN**, ⛔ khong"
          % (m_chuoi, len(k_l1), 100.0 * m_chuoi / max(len(k_l1), 1)))
    print("    phai mot phep ghep hong.")
    kho = len(k_l1) - m_chuoi
    print("  · ⛔ ben bank co ma nhung PM ⛔ khong he co : %d dong (%.1f%%)"
          % (kho, 100.0 * kho / max(len(k_l1), 1)))
    print("    => phan nay ⛔ KHONG phai loi ky thuat: giao dich ngan hang that")
    print("       ⛔ chua co de nghi thanh toan tuong ung. Do la NGHIEP VU.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
