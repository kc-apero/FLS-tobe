# -*- coding: utf-8 -*-
"""CONG: moi NUT tren man hinh phai co mot dong THUYET MINH trong `BA-13`.

    python tools/kiem_thuyet_minh.py

⛔⛔⛔ **Vi sao cong nay ton tai — va no ⛔ khong phai de "tai lieu cho dep".**

`BA-03` (user story) da gia **BA LAN trong im lang**, va ca ba lan deu lo ra
theo **dung mot cach**: owner hoi.

    28/08  thieu 2 thao tac   (bo ghep · bam xong)
    09/09  thieu CA LAN NAP   (SCR-F04 + 9 cua + 4 bang kho)
    14/09  thieu CA LAN LENH CHI (+ ba ro · duyet lo · bang PM du truong)

★ Nguyen nhan la **CAU TRUC**, ⛔ khong phai quen: `BA-06`/`BA-07` duoc cap
  nhat **moi dot** vi **ma cham vao chung** — con `BA-03` thi ⛔ **khong co
  mot phep do nao** buoc no theo. ⇒ Mot tai lieu ⛔ khong co cong canh se
  gia, va no gia **im lang**, va no chi lo ra khi co nguoi tinh co hoi.

⇒ Cong nay la phep do ay, dat o cho **hep nhat ma do duoc**: mot NUT.

★ **Luat, va no co MOT chieu:**

  ⓐ Moi nhan nut doc duoc tu `fls/web/tep/man_*.js` phai **xuat hien** trong
    `docs/ITL/02_BA/13_THUYET_MINH_MAN_HINH.md`. Them nut ma ⛔ khong giai
    thich no ⇒ **NO**.
  ⓑ ⛔ **Chieu nguoc lai ⛔ KHONG bi canh.** Tai lieu duoc phep noi ve mot nut
    **⛔ CHUA CO** — do dung la cach no khai ra khoang trong *(`⛔` trong
    bang)*. Bat tai lieu chi duoc noi ve cai da co la bat no **thoi lam
    dac ta**.

⛔⛔ **Xanh tren tap RONG = CHUA DO.** Neu ⛔ khong doc duoc mot nhan nut nao
   thi phep trich da hong *(doi cach dung nut, doi ten tep…)* — va mot cong
   bao "dat" luc ay la mot cong **noi doi**. ⇒ NO khi so nhan = 0.

⚠ **Cai cong nay ⛔ KHONG lam:** no ⛔ khong biet dong thuyet minh co **DUNG**
   hay ⛔ khong. No chi biet **co hay ⛔ khong co**. Mot dong sai van qua duoc
   — cung lop voi `kiem_so_song` canh **SO** ma ⛔ khong canh **CAU**
   (`GAP-DOC-08`). ⇒ Ghi ra day de ⛔ khong ai doc mau xanh nay thanh
   *"tai lieu da dung"*.
"""
from __future__ import annotations

import pathlib
import re
import sys

GOC = pathlib.Path(__file__).resolve().parent.parent
MAN = GOC / "fls" / "web" / "tep"
BA = GOC / "docs" / "ITL" / "02_BA"

# ⛔⛔⛔ **HAI ban, va ca hai deu bi canh — ⛔ khong phai mot.**
#
# Owner yeu cau dua phan thuyet minh vao **ca ban ve HTML** (14/09), nen cung
# mot noi dung nay song o **hai cho**: tep `.md` *(doc bang mat, grep duoc)*
# va tep `.html` *(ban ve owner mo ra duyet)*.
#
# ⚠ Hai ban sao cua cung mot su that thi **ban ⛔ khong ai canh se muc**, va
#   no muc **im lang** — dung hinh benh `BA-03` da mac ba lan. ⇒ Cong nay
#   doi nhan nut co mat o **CA HAI**, va noi ro **thieu o ban nao**.
#
# ⛔ Day ⛔ **khong** phai lua chon dep nhat. Dep nhat la **mot nguon duy
#   nhat** roi sinh ra ban kia. Nhung sinh HTML tu Markdown la them mot buoc
#   dung, va buoc ay se **hong trong im lang** khi ⛔ khong ai chay no ⇒ chon
#   cach **do duoc ngay**: hai tep, mot cong, ⛔ khong buoc dung nao.
TL = (BA / "13_THUYET_MINH_MAN_HINH.md",
      BA / "Artifacts" / "Ban-ve-TOBE-Man-Ghep-PM.html")

# Nhan nut doc duoc o BA cach man hinh nay dung nut:
#   ⓐ `_nut('Nhan', …)`            — nut tren luoi
#   ⓑ `TP.el('button', 'lop', 'Nhan')` — nut dung tay
#   ⓒ `[['Nhan', ham]]`            — nut trong hop thoai (`HT.mo`)
MAU = (
    re.compile(r"_nut\(\s*'([^']{2,40})'"),
    re.compile(r"TP\.el\(\s*'button'\s*,\s*'[^']*'\s*,\s*'([^']{2,40})'"),
    re.compile(r"\[\s*'([^']{2,40})'\s*,\s*(?:null|async\s+function|function)"),
)

# ⛔ Nhan sinh RA LUC CHAY (ghep chuoi) ⇒ ⛔ khong trich duoc nguyen van.
#   Khai o day **kem ten ham sinh ra no**, de danh sach nay ⛔ khong thanh
#   mot cho giau nut: moi dong phai tra loi duoc *"ai sinh ra no"*.
DONG_SINH: dict[str, str] = {
    "Duyệt": "man_f01_lenh.js::_viec_cua_dong",
    "Mở để chia": "man_f01_lenh.js::_viec_cua_dong",
    "Tra tiền": "man_f01_lenh.js::_viec_cua_dong",
    "Xem vì sao": "man_f01_lenh.js::_viec_cua_dong",
    "Duyệt cả": "man_f01_lenh.js::_ve_viec (ghep so dong)",
    "Bắt đầu tra": "man_f01_lenh.js::_ve_viec",
    "Hiện ĐỦ các cột của GGSheet": "man_f01_lenh.js::_nut_du_cot",
    "← Chỉ 2 cột nhận diện": "man_f01_lenh.js::_nut_du_cot",
}

# Nut **ky thuat**, ⛔ khong phai thao tac nghiep vu. Chung van phai co mat
# trong tai lieu — nhung o mot dong gop, nen mien phep doi tung cai.
KY_THUAT = {"Đóng", "Thôi", "Thử lại", "Thử lại ngay", "Xem thêm"}


def doc_nhan() -> dict[str, set[str]]:
    """`{nhan: {tep…}}` — doc tu MA, ⛔ khong tu mot danh sach go tay."""
    ra: dict[str, set[str]] = {}
    for f in sorted(MAN.glob("man_*.js")):
        s = f.read_text(encoding="utf-8")
        for mau in MAU:
            for m in mau.finditer(s):
                nhan = m.group(1).strip()
                if nhan:
                    ra.setdefault(nhan, set()).add(f.name)
    for nhan, o in DONG_SINH.items():
        ra.setdefault(nhan, set()).add(o.split("::")[0])
    return ra


def chay() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    thieu_tep = [t for t in TL if not t.exists()]
    if thieu_tep:
        for t in thieu_tep:
            print(f"⛔ ⛔ khong thay {t.relative_to(GOC)}")
        return 1
    ban = {t.name: t.read_text(encoding="utf-8") for t in TL}
    nhan = doc_nhan()

    # ⛔⛔ Xanh tren tap RONG = CHUA DO.
    if not nhan:
        print("⛔ ⛔ KHONG doc duoc mot nhan nut nao tu `fls/web/tep/man_*.js`.")
        print("   Phep trich da hong — va mot cong bao 'dat' luc nay la mot")
        print("   cong NOI DOI. Sua `MAU` trong tep nay.")
        return 1

    # `{nhan: [ban thieu…]}` — noi ro thieu o BAN NAO, ⛔ khong chi "thieu".
    thieu: dict[str, list[str]] = {}
    for n in sorted(nhan):
        vang = [ten for ten, noi_dung in ban.items() if n not in noi_dung]
        if vang:
            thieu[n] = vang
    print(f"nut doc duoc tu ma : {len(nhan)}")
    print(f"  · trich nguyen van: {len(nhan) - len(DONG_SINH)}")
    print(f"  · sinh luc chay   : {len(DONG_SINH)} (khai trong `DONG_SINH`)")
    print(f"  · nut ky thuat    : {len(KY_THUAT & set(nhan))}")
    print(f"ban phai mang du    : {len(TL)}")
    for t in TL:
        print(f"  · {t.name}")
    if thieu:
        print(f"\n⛔ {len(thieu)} nut ⛔ KHONG co dong thuyet minh:")
        for n, vang in thieu.items():
            o = ", ".join(sorted(nhan[n]))
            print(f"     ⛔ {n!r}  (man: {o})  ⇒ thieu o: {', '.join(vang)}")
        print("\n⇒ Them mot dong cho moi nut tren, o MOI ban con thieu. Mot")
        print("  nut ma ⛔ khong ai giai thich duoc thi cau hoi dung la *\"no")
        print("  con can ⛔ khong\"*, ⛔ khong phai *\"viet gi vao day\"*.")
        return 1
    print(f"\n✅ CONG THUYET MINH DAT — {len(nhan)}/{len(nhan)} nut co mat "
          f"trong CA {len(TL)} ban")
    print("⚠ Cong nay chi biet nut CO duoc nhac den, ⛔ KHONG biet dong ay "
          "co DUNG hay khong.")
    return 0


if __name__ == "__main__":
    raise SystemExit(chay())
