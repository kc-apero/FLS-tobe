# -*- coding: utf-8 -*-
"""Cong kiem bo tai lieu ITL — bien 5 luat GIAY cua `07_CHANGE_CONTROL` §7
thanh mot lenh chay duoc.

    python docs/ITL/_tools/kiem_tai_lieu.py

Nam phep kiem, moi phep sinh ra tu MOT lo da xay ra that:

  K1 · version header vs changelog
       ⛔ `08_MIGRATION_ROADMAP` header dung o `v0.1` trong khi changelog da
       len `v0.4` — ba lan bump chi ghi o changelog. Moi file tro tay den do
       deu trich sai version, va khong cai gi bao gi.

  K2 · so luong CR khop giua `00_MASTER_INDEX` va `07_CHANGE_CONTROL` §5
       ⛔ So CR tung ghi "chua co CR nao" suot HAI NGAY trong khi `CR#1` da
       dong va `CR#2` da mo roi dong — ca hai chi song o master index va o
       ma nguon. Day dung la `07_CHANGE_CONTROL` §7 luat 2.

  K3 · bang markdown lech cot
       ⛔ 8 dong trong `06_ORCHESTRATOR_DASHBOARD` vo cot vi dau `|` TRAN
       trong o (`P100 | Cash Ledger`, `Copy of R | VND_HotBonus`, `R | …`).
       Bang van "trong nhu bang", chi la cac o dich sang mot cot — nen mat
       thuong doc qua ma khong thay. Mot dong con THIEU HAN 2 o.

  K4 · CR dong ma khong co chung cu do duoc
       `07_CHANGE_CONTROL` §7 luat 3. "Da xu ly" ⛔ khong phai chung cu.

  K5 · ⛔ KHONG tai lieu nao duoc ghi mot NGAY CHUA XAY RA
       ⛔ Ca dot `P4`+`P5` (27/08 13:56-17:49 theo `git log`) bi dan ngay
       **28/08** o **54 cho** tren 16 file — ke ca header `06_DASHBOARD`,
       header `07_CHANGE_CONTROL`, va so quyet dinh `QĐ-ITL-59/60`. Bon phep
       kiem tren van XANH suot, vi ⛔ khong phep nao trong so do KIEM NGAY.
       Dang ke vi nhat ky doi cua `tien_do.py` la **bang chung** cho tung buoc
       phan tram: ghi sai ngay thi mat luon thu tu nhan qua — ma o dot do
       chinh thu tu ay la cai da bat duoc 3 cong do gia.
       Kem mot he qua do duoc: cau *"khung xem song duoc MOT NGAY"* thanh
       sai — no song **1 gio 48 phut**.
       ⛔ **K5 do gi va KHONG do gi** (cong chung #7): no CHI soi **dong
       duong-dan-chung** — header, dong changelog, dong so QĐ / so CR — va CHI
       dang `YYYY-MM-DD`. ⛔ Hai thu no **KHONG** do duoc, khai ra chu khong
       de nguoi doc tu suy: ⓐ dang ngan `dd/mm` (thieu nam nen khong phan biet
       duoc "27/08 da qua" voi mot moc ke hoach that trong tuong lai) ⓑ ngay
       nam trong **cau van thuong**. ⇒ mot dot dan sai ngay CHI o hai cho do
       van di qua duoc K5.
       ⛔⛔ **Va K5 tung XANH GIA ngay trong buoi dung no.** Lan dien tap dau
       toi dat ngay tuong lai vao **dong 4 cua `06_DASHBOARD`** — dung o da
       lech that — va cong van **XANH**: mau header doi dung chu
       `**Cap nhat:**`, con file that ghi `**Cap nhat lan cuoi:**`. Cong bo
       sot **dung cai o no sinh ra de canh**. Nay mau cho phep co chu giua
       nhan va dau `:`, va ca **4 nhanh** da dien tap thay DO: ngay tuong lai
       o **header**, o **dong so QĐ**, o **dong changelog**, va nhanh **san
       toi thieu** (mau vo ⇒ do, ⛔ khong xanh).

⛔ Mac dinh KHONG DAT: thieu file, doc khong duoc, hay khong tim thay bang
CR nao thi la DO — ⛔ khong phai "khong thay loi nen xanh" (cong chung #7).
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import re
import sys

# Console Windows mac dinh cp1252 KHONG ma hoa noi tieng Viet co dau lan emoji.
# Khong ep UTF-8 thi cong DAT ca 5 phep van chet o dong `print` cuoi va tra
# exit=1 => bao SAI. Da tra gia dung loi nay mot lan o `check_plan_docs.py`
# (FPA-T4): mot cong bao sai te hon khong co cong, vi no con mua them su tin
# tuong. Dat NGAY sau `import sys`, truoc moi lenh in.
try:                                    # py>=3.7
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:                        # pragma: no cover
    pass

GOC = pathlib.Path(__file__).resolve().parent.parent
MASTER = GOC / "00_MASTER_INDEX.md"
CHANGE = GOC / "01_Orchestrator" / "07_CHANGE_CONTROL.md"

_PIPE_THOAT = "\\|"
_TACH_CR = re.compile(r"^\| \*\*`(CR#[0-9A-Za-z-]+)`\*\*")
_SEP = re.compile(r"^\|[\s:|-]+\|$")


def _cot(dong: str) -> int:
    """Dem cot cua mot hang bang. ⛔ Dau `\\|` da thoat KHONG tinh la vach cot."""
    return dong.replace(_PIPE_THOAT, "\x00").count("|")


def _so(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


# ---------------------------------------------------------------- K1
def k1_version(files: list[pathlib.Path]) -> list[str]:
    loi = []
    for f in files:
        t = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"\*\*Version:\*\*\s*v?([0-9]+\.[0-9]+)", t)
        if not m:
            continue
        # ⭐ Sua 2026-09-07: mau cu doi dau `(` DINH LIEN sau so, nen no MU voi
        # kieu viet `- **v0.17** *(2026-09-04, ...)*:` — dau `*` in nghieng chen
        # vao giua. Bon tep BA that su CO muc changelog v0.17/v2.0/v0.4/v0.8 ma
        # cong van bao "THIEU muc changelog": mot DO GIA tren 4/5 loi K1.
        # ⛔ Bai hoc: cong nay do CHUOI, khong do NGHIA — sua CONG, ⛔ khong sua
        # tai lieu cho vua mot phep do sai (`R-A5`).
        cl = re.findall(r"^[-*]\s*[*_]*v?([0-9]+\.[0-9]+)[*_]*\s*[*_]*\(",
                        t, re.M)
        if not cl:
            continue
        cao = max(cl, key=_so)
        head = m.group(1)
        if _so(cao) > _so(head):
            loi.append(f"{f.relative_to(GOC)}: header v{head} "
                       f"< changelog v{cao} — bump khong toi header")
        elif _so(head) > _so(cao):
            # ⭐ Them 27/08: K1 truoc day soi MOT CHIEU. Chieu nay bat duoc mot lo
            # THAT ngay hom ay: mot script va tai lieu dung `str.replace` voi mau
            # KHONG TON TAI — Python bo qua trong IM LANG, nen `03_Dev/03` len
            # header v1.9 ma muc changelog v1.9 **khong bao gio duoc them**.
            loi.append(f"{f.relative_to(GOC)}: header v{head} "
                       f"> changelog v{cao} — THIEU muc changelog cho v{head}")
    return loi


# ---------------------------------------------------------------- K2
def k2_so_cr() -> list[str]:
    if not MASTER.exists() or not CHANGE.exists():
        return ["thieu 00_MASTER_INDEX.md hoac 07_CHANGE_CONTROL.md"]
    a = {m.group(1) for m in map(_TACH_CR.match,
                                 MASTER.read_text(encoding="utf-8").split("\n"))
         if m}
    b = {m.group(1) for m in map(_TACH_CR.match,
                                 CHANGE.read_text(encoding="utf-8").split("\n"))
         if m}
    if not a and not b:
        # ⛔ khong phai "sach": la chua do duoc gi ca
        return ["khong tim thay CR nao o CA HAI file — cong nay chua do duoc gi"]
    if a != b:
        chi_mi = sorted(a - b)
        chi_cc = sorted(b - a)
        return [f"so CR lech: chi o MASTER_INDEX={chi_mi} · "
                f"chi o CHANGE_CONTROL={chi_cc}"]
    return []


# ---------------------------------------------------------------- K3
def k3_bang(files: list[pathlib.Path]) -> tuple[list[str], int]:
    loi, dem = [], 0
    for f in files:
        d = f.read_text(encoding="utf-8", errors="replace").split("\n")
        i = 0
        while i < len(d):
            s = d[i].lstrip("> ").strip()
            if (s.startswith("|") and i + 1 < len(d)
                    and _SEP.match(d[i + 1].lstrip("> ").strip())):
                n = _cot(s)
                dem += 1
                j = i + 2
                while j < len(d) and d[j].lstrip("> ").strip().startswith("|"):
                    r = d[j].lstrip("> ").strip()
                    if _cot(r) != n:
                        loi.append(f"{f.relative_to(GOC)}:{j + 1} "
                                   f"cot {_cot(r) - 1} != {n - 1}  {r[:60]}")
                    j += 1
                i = j
            else:
                i += 1
    return loi, dem


# ---------------------------------------------------------------- K4
def k4_cr_dong_co_chung_cu() -> list[str]:
    if not CHANGE.exists():
        return ["thieu 07_CHANGE_CONTROL.md"]
    loi = []
    for dong in CHANGE.read_text(encoding="utf-8").split("\n"):
        m = _TACH_CR.match(dong)
        if not m:
            continue
        # ⭐ Sua 2026-09-07: truoc day K4 soi chu "DONG" tren CA DONG, nen mot CR
        # con MO ma trong cau co nhac den viec dong (vi du `CR#10` dan luat §7:
        # "cam dong CR khong co chung cu") bi bat nham. Khai bao trang thai song
        # o O CUOI — ca 11 CR da dong deu ghi "DONG" o do. ⇒ Chi doc O CUOI de
        # biet CR co dong khong; van tim chung cu tren CA DONG.
        # ⛔ Day la siet CHAT hon, ⛔ khong phai noi long: mot CR ghi "DONG" o o
        # trang thai thi van bi doi chung cu nhu cu.
        o = [x.strip() for x in dong.split("|")]
        trang_thai = o[-2] if len(o) >= 3 else dong
        if "ĐÓNG" not in trang_thai.upper():
            continue
        # chung cu = co it nhat mot con so do duoc, hay tro tay den test/cong
        co_so = re.search(r"\**[0-9][0-9.,]*\**\s*(?:phép thử|test|ô|dòng|%)", dong)
        co_tro = re.search(r"`[a-z_]+\.py`|`tests?/|migration\s*`?0", dong)
        if not (co_so or co_tro):
            loi.append(f"{m.group(1)} ghi DONG ma khong co chung cu do duoc "
                       f"(khong con so, khong tro tay den test/cong/migration)")
    return loi


# ---------------------------------------------------------------- K5
_NGAY_ISO = re.compile(r"(?<![0-9])(20[0-9]{2})-([01][0-9])-([0-3][0-9])(?![0-9])")

# ⛔ K5 CHI soi DONG DUONG DAN CHUNG, khong soi ca file. Ly do do duoc: lan
# chay dau K5 quet moi dong va DO ngay — 30 loi, **ca 30 la do GIA**: chung la
# ngay trong DU LIEU MA TAI LIEU TRICH DAN (`09/13/2025` la o cua so ke toan,
# `06/10/2026` la cot ngay cuoi cua so tien 644 cot). Mot phep kiem khong phan
# biet duoc "ngay CUA tai lieu" voi "ngay TRONG du lieu tai lieu dan ra" thi no
# ⛔ khong do dung thu can do. ⇒ thu hep vao dung 4 loai dong mang duong dan
# chung cua du an, va bo han dang `dd/mm/yyyy` (thieu nam thi khong the biet
# `27/08` la da qua hay la mot moc ke hoach that trong tuong lai).
_DONG_DAU_VET = (
    re.compile(r"\*\*(?:Version|Cập nhật|Ngày)[^*]{0,24}\*\*"),          # header
    re.compile(r"^\s*[-*]\s*\*\*?v[0-9]+\.[0-9]+"),                     # changelog
    re.compile(r"^\|\s*\*\*`?(?:QĐ-|CR#)"),                              # so QĐ / so CR
)
# Neu so o ngay soi duoc tut duoi nguong nay thi cong DO — vi nghia la 3 mau
# tren da vo, va mot cong "khong tim thay gi de do" ⛔ khong duoc phep xanh.
_SAN_TOI_THIEU = 60


def k5_khong_ngay_tuong_lai(files: list[pathlib.Path]) -> tuple[list[str], int]:
    """⛔ Khong dong duong-dan-chung nao duoc ghi mot ngay CHUA XAY RA.

    Tra ve (loi, so O NGAY da soi) — con so thu hai la de cong phai chung minh
    no DO duoc gi, chu khong phai "quet 60 file roi khong thay loi".
    """
    hom_nay = _dt.date.today()
    loi: list[str] = []
    dem = 0
    for f in files:
        try:
            noi_dung = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:                                   # pragma: no cover
            loi.append(f"{f.name}: doc khong duoc ({e})")
            continue
        for so_dong, dong in enumerate(noi_dung.splitlines(), 1):
            if not any(m.search(dong) for m in _DONG_DAU_VET):
                continue
            for m in _NGAY_ISO.finditer(dong):
                dem += 1
                y, mo, d = (int(x) for x in m.groups())
                try:
                    ngay = _dt.date(y, mo, d)
                except ValueError:
                    loi.append(f"{f.name}:{so_dong} `{m.group(0)}` "
                               f"⛔ KHONG PHAI NGAY CO THAT")
                    continue
                if ngay > hom_nay:
                    loi.append(f"{f.name}:{so_dong} `{m.group(0)}` "
                               f"⛔ NGAY CHUA XAY RA (hom nay {hom_nay})")
    if dem < _SAN_TOI_THIEU:
        loi.append(f"⛔ chi soi duoc {dem} o ngay (< {_SAN_TOI_THIEU}) — 3 mau "
                   f"dong duong-dan-chung co le da vo; cong DO vi ⛔ khong do "
                   f"duoc gi, khong phai vi 'khong thay loi'")
    return loi, dem


# ---------------------------------------------------------------- K6
# ⛔⛔⛔ **K6 sinh ra tu MOT LOI THAT, va loi ay SONG 7 NGAY ma khong ai thay.**
#
# Do 17/09: `QĐ-ITL-128` duoc khai o **HAI** dong, cho **HAI** quyet dinh khac
# han nhau *(17/09 mo lai `QĐ-ITL-92` · 10/09 soi ba lop)*. Ca sổ chỉ **mot** ma
# bi trung — nhung mot ma trung la du: tu do tro di, cau *"theo `QĐ-ITL-128`"*
# co **hai** cau tra loi, va nguoi doc ⛔ khong co cach nao biet minh dang doc
# cai nao.
#
# ⭐ Va phep do nay chay trong **mot giay**. No ⛔ khong ton tai suot 7 ngay
#   ⛔ khong phai vi kho, ma vi ⛔ khong ai nghi den — dung ly do ma moi cong
#   trong repo nay duoc dung.
#
# ⛔ K6 soi **dong KHAI** *(dong bang bat dau bang `| **\`QĐ-ITL-N\`**`)*, ⛔
#   khong soi moi lan **TRICH**. Mot ma duoc trich 5 cho la binh thuong; duoc
#   **khai** 2 lan moi la loi. Nham hai thu nay se cho ra mot cong do GIA
#   thuong truc.
RE_KHAI_QD = re.compile(r"^\|\s*\*\*`(QĐ-ITL-\d+)`\*\*")


def k6_ma_quyet_dinh_khong_trung(md: list[pathlib.Path]) -> tuple[list[str], int]:
    """⛔ MOT ma quyet dinh ⛔ khong duoc khai hai lan **trong SO QUYET DINH**.

    ⛔⛔ **CHI soi `00_MASTER_INDEX.md`, va do la mot su THU HEP CO Y — lan
    chay dau K6 quet moi `.md` va DO ngay: 3 loi, va **ca 3 la oan**.**
    Chung nam o `Ra-soat-Cau-truc-R-va-ERD.md`, trong mot bang **TRICH DAN**
    *(`| Quyet dinh | Noi dung | He qua |`)* tinh co dung **cung khuon dong**
    voi so quyet dinh.

    ⭐ Trich mot ma o nhieu cho la **viec binh thuong va DANG KHUYEN KHICH**;
      chi **KHAI** hai lan moi la loi. Nham hai thu ay cho ra mot cong keu sai
      **thuong truc** — va mot cong keu sai la mot cong nguoi ta se **go ra**.

    ⇒ So quyet dinh la **MOT cho duy nhat**: `00_MASTER_INDEX.md`. Neu mai sau
      co so thu hai, them no vao day **co y thuc**, ⛔ dung noi rong ra ca kho.
    """
    thay: dict[str, list[str]] = {}
    so = [p for p in md if p.name == "00_MASTER_INDEX.md"]
    if not so:
        return ["⛔ ⛔ khong tim thay `00_MASTER_INDEX.md` — K6 ⛔ KHONG do duoc "
                "gi, va 'khong do duoc' la DO, ⛔ khong phai 'khong thay loi'"], 0
    for p in so:
        for i, dong in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            m = RE_KHAI_QD.match(dong)
            if m:
                thay.setdefault(m.group(1), []).append(
                    f"{p.relative_to(GOC)}:{i}")
    loi = [f"{ma} duoc KHAI {len(cho)} lan: {' · '.join(cho)}"
           for ma, cho in sorted(thay.items()) if len(cho) > 1]
    return loi, len(thay)


def main() -> int:
    md = sorted(GOC.rglob("*.md"))
    if not md:
        print("⛔ KHONG DOC DUOC FILE .md NAO — cong DO (mac dinh khong dat)")
        return 1

    e1 = k1_version(md)
    e2 = k2_so_cr()
    e3, so_bang = k3_bang(md)
    e4 = k4_cr_dong_co_chung_cu()
    # K5 soi ca .html: ban ve kien truc cung mang ngay, va no cung bi dan sai.
    e5, so_ngay = k5_khong_ngay_tuong_lai(md + sorted(GOC.rglob("*.html")))
    e6, so_qd = k6_ma_quyet_dinh_khong_trung(md)

    print(f"quet {len(md)} file .md · {so_bang} bang markdown\n")
    for ten, loi, do_duoc in (
        ("K1 version header vs changelog", e1, f"{len(md)} file"),
        ("K2 so CR khop 2 file          ", e2, "MASTER_INDEX vs 07 §5"),
        ("K3 bang markdown khong lech   ", e3, f"{so_bang} bang"),
        ("K4 CR dong co chung cu do duoc", e4, "07 §5"),
        ("K5 khong ngay CHUA XAY RA     ", e5, f"{so_ngay} o ngay"),
        ("K6 ma QD khong bi cap hai lan ", e6, f"{so_qd} ma"),
    ):
        dau = "OK " if not loi else "⛔ "
        print(f"{dau}{ten}  (da do: {do_duoc})")
        for x in loi:
            print(f"     - {x}")

    tong = len(e1) + len(e2) + len(e3) + len(e4) + len(e5) + len(e6)
    print()
    if tong:
        print(f"⛔ CONG TAI LIEU KHONG DAT — {tong} loi")
        return 1
    print("✅ cong tai lieu DAT — va no da do duoc that "
          f"({len(md)} file, {so_bang} bang, {so_ngay} o ngay, {so_qd} ma QD), "
          "khong chi 'khong thay loi'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
