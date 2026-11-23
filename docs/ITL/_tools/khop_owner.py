# -*- coding: utf-8 -*-
"""`C1` — BANG DOI CHIEU GOC cua cuoc audit *(lo trinh `_AUDIT_ALIGNMENT_ROADMAP`)*.

    python docs/ITL/_tools/khop_owner.py          # sinh bang vao lo trinh
    python docs/ITL/_tools/khop_owner.py --kiem   # CHI kiem (cong CI)

⭐⭐⭐ **Moi phep mot dong, BON cot:** *phat bieu* · **TAI LIEU** noi gi ·
**MA NGUON** noi gi · **KHO** noi gi. Ba cot sau **doc thang tu nguon**,
⛔ khong mot o nao go tay — vi mot bang go tay chinh la thu vua drift.

⛔⛔ **CHUAN o day KHONG phai "bon phat bieu cua owner".** Owner chot 17/09
   *(`Q1`)*: chuan la **bo ERD cua he ggsheet hien co**. ⇒ Cac con so trong
   `CHUAN` deu do tu 5 tep RAW, va moi con so mang theo **xuat xu**.

⛔⛔⛔ **Vi sao `CHUAN` la ban khai DONG BANG, ⛔ khong doc lai `.xlsx` moi lan:**
   ⓐ tep nguon nam **ngoai repo** va bi `gitignore` *(chung mang ten nguoi)*
     ⇒ mot cong doc chung se **DO tren moi may khac**;
   ⓑ doc 26 MB x 5 tep la **phut**, ⛔ khong phai giay;
   ⓒ va day dung khuon da co: `pm_join.PM_TIEU_DE_MONG_DOI` cung la mot
     **hop dong nguon dong bang**, duoc `kiem_tieu_de_pm` **NO TO khi lech**.
   ⇒ Doi `CHUAN` thi phai **do lai va ghi xuat xu**, ⛔ khong sua cho vua.

⭐⭐ **`mong` — vi sao moi phep khai TRUOC ket qua mong doi.**
   Phan lon cac phep o day dang **LECH**, va do la *muc dich* cua cuoc audit.
   Mot cong chi bao "co lech" thi no **xanh mai mai** va ⛔ khong ai biet khi
   nao mot cho da duoc sua — hoac te hon, khi nao mot cho **dang khop bi lam
   hong**. ⇒ Cong NO khi ket qua **khac `mong`**, ca hai chieu:
     · sua duoc mot cho  ⇒ **DO** ⇒ buoc nguoi sua **ghi lai** vao ban khai;
     · mot cho dang khop vo ⇒ **DO** ngay.

⛔ **Phep ⛔ KHONG DO DUOC la DO, ⛔ khong phai "khong thay lech".**
   Kho tat, tep mat, mau khop `0` hoac `>=2` lan — deu NO. Mot cong
   "khong tim thay gi de do" ⛔ khong duoc phep xanh *(bai nay da can that
   o `K5`: 30 bao thi ca 30 la do gia, va o `kiem_so_song`: mau khop 4 lan)*.
"""
from __future__ import annotations

import argparse
import io
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Callable

GOC = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(GOC))

from fls.adapters import pm_join                              # noqa: E402
from fls.canon import spec as canon_spec                      # noqa: E402
from fls.db import schema as db_schema                        # noqa: E402
from fls.db.kho import dsn_that, noi_chi_doc                  # noqa: E402
from fls.repo import chup as repo_chup                        # noqa: E402

TAI_LIEU = GOC / "docs" / "ITL"
LO_TRINH = TAI_LIEU / "_AUDIT_ALIGNMENT_ROADMAP.md"
MOC_DAU = "<!-- SINH-KHOP:BAT-DAU -->"
MOC_CUOI = "<!-- SINH-KHOP:KET-THUC -->"


# ==========================================================================
# ⭐ BAN KHAI CHUAN — do tu 5 tep RAW ngay 2026-09-17. Moi dong mang XUAT XU.
# ==========================================================================
CHUAN: dict[str, tuple[object, str]] = {
    # khoa: (gia tri, xuat xu)
    "so_duong_vao": (3, "`P100 _ Bank Transactions` + `P100 _ Cash Ledger` + "
                        "`PM_Unpivot` — owner `Q2` 17/09: di nho mot duong vao"),
    "so_thuc_the_lenh": (3, "`A _ PAY100 _ PM11 Entry Data`: `PE_Unpivot` · "
                            "`PI_Unpivot` · `PM_Unpivot` — owner `Q2`"),
    "pm_co_ten": (28, "`A _ PAY100 _ PM11 Entry Data` tab `PM_Unpivot`, "
                      "tieu de hang 2: 29 vi tri, 28 co ten"),
    # ⭐ 8 → 14 ngay 17/09: owner chot dua `PE`/`PI` len cot CO KIEU ⇒ hop
    #   dong cot mo them 6 vi tri. **Da do lai ca 14** tren
    #   `A _ PAY100 _ PM11 Entry Data` tab `PM_Unpivot` hang 2: **lech 0**.
    "pm_hop_dong": (14, "`pm_join.PM_TIEU_DE_MONG_DOI` — do lai ca 14 vi "
                        "tri voi ban ngoai kho 17/09: lech 0"),
    "canon_vi_tri": (38, "`ITL … File 1_2` tab `Transaction Mapping L1`, "
                         "tieu de hang 3: 38 vi tri"),
    "canon_co_ten": (36, "cung tren — 36 o co ten (`Z`/`AA` trong)"),
    # ⛔⛔ SUA 17/09 — con so cu o day la `69` va no LA MOT PHEP DO QUA THO
    #   cua chinh toi: `69` la BE RONG hang (ke ca duoi rong). So cot CO TEN
    #   dem tren **hang 7 + hang 8** *(hang 8 la ten cot con cua cac khoi 4
    #   cot — `BA-05 §DD-I04` da khai)* la **64** ⇒ con so `64 cot` cua bo
    #   tai lieu **DUNG**, va cai sai la phep do cua toi.
    "ledge_co_ten": (64, "`ITL Ledge` hang 7+8: 64 cot co ten "
                         "(be rong hang la 69, ⛔ ke ca duoi rong)"),
    "luoi_f02": (52, "`fls/api/cot_so.BANG_COT` — do THANG tu ma"),
    "luoi_nen": (24, "`BANG_COT` khong mang `canon=`"),
    "luoi_canon": (28, "`BANG_COT` mang `canon=` (tu `CANON_LEN_LUOI`)"),
    "adjust_so_dai": (7, "`ITL Ledge` hang 1 `ADJUSTMENT ZONE` — 7 dai, "
                         "hang 3 co dung 7 bo dem `# Input here`"),
    "so_khau": (3, "owner `Q1` 17/09: «ITL (1/2)» la BUOC ⛔ khong phai module"),
    "ten_tep_asis": (("File 1_2", "File 2_2"),
                     "ten module cua owner CHINH LA ten tep AS-IS"),
}


def chuan(k: str) -> object:
    return CHUAN[k][0]


# ==========================================================================
class LoiDo(Exception):
    """Phep ⛔ KHONG do duoc — ⛔ khong phai 'khong thay lech'."""


@dataclass
class Ket:
    tai_lieu: str
    ma_nguon: str
    kho: str
    khop: bool
    # ⭐ `WO-011 T6 ⓒ` — so TUYET DOI in ra **man** *(stdout)*, ⛔ vao khoi
    #   `SINH-KHOP`. Khoi chi mang **quan he**: no phai ⛔ doi khi chi co mot
    #   anh moi cung noi dung *(`KQ-010 F-3` — cot `kho` cua `B3`/`B4` in
    #   `196.480` = so dong tren **moi** anh ⇒ `--kiem` DO moi gio nhip chup)*.
    man: str = ""


@dataclass
class Phep:
    ma: str
    nhom: str
    cau: str
    chuan_: str
    fn: Callable[["Boi"], Ket]
    mong: bool
    ghi_chu: str = ""
    ket: Ket | None = field(default=None, repr=False)


class Boi:
    """Ba nguon doc MOT lan, dung cho moi phep."""

    def __init__(self, conn) -> None:
        self.conn = conn
        self.md: dict[pathlib.Path, str] = {
            p: p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(TAI_LIEU.rglob("*.md"))
        }
        if len(self.md) < 60:
            raise LoiDo(f"chi doc duoc {len(self.md)} tep .md — san toi thieu 60")
        self.bang = [v for v in vars(db_schema).values()
                     if hasattr(v, "columns") and hasattr(v, "khau")
                     and hasattr(v, "name")]
        if not self.bang:
            raise LoiDo("⛔ khong trich duoc bang nao tu `schema.py`")

    # ---- tai lieu ----
    def dem(self, mau: str, chi_tep: str | None = None) -> int:
        n = 0
        for p, s in self.md.items():
            if chi_tep and p.name != chi_tep:
                continue
            n += s.count(mau)
        return n

    def dem_tep(self, mau: str) -> int:
        return sum(1 for s in self.md.values() if mau in s)

    # ---- kho ----
    def so(self, sql: str, ts: tuple | list | None = None) -> int:
        with self.conn.cursor() as c:
            c.execute(sql, ts)
            r = c.fetchone()
        if r is None or r[0] is None:
            raise LoiDo(f"cau hoi kho ⛔ khong tra ve gi: {sql[:60]}")
        return int(r[0])


# ==========================================================================
# CAC PHEP
# ==========================================================================
# ⭐⭐ `WO-023` `(e)` *(`KQ-021 F-4` · `KQ-025 F-1`, khuon `WO-011 T6 ⓒ`)*: o
#   **tai lieu** cua khoi `SINH-KHOP` chi mang **QUAN HE** *(co / ⛔ co)*, ⛔ so
#   dem chu. ⛔⛔ Truoc: `B5` in so lan *"de xuat"*+*"goi y"* cua `BA-06`
#   *(`49 → 50` sau v4.10)*, `C3` in so lan *"7 truong"* *(chinh to `BG-024`
#   lam `59 → 60`)* ⇒ **moi** lan `fls-ba` sua `BA-06` hay ai viet mot phieu la
#   `--kiem` DO lai ma ⛔ co gi sai — cung lop `KQ-010 F-3` *(`B3`/`B4` in so
#   dong anh)*. ⇒ So dem ra **man** *(`Ket.man`)*; khoi chi mang `co`/`⛔ co`.
#   ⭐ So dem **tu MA** *(`len(BANG_COT)`, `CANON_COLS`)* **giu** trong khoi —
#   no ⛔ troi khi nguoi viet phieu. `mong` cua moi phep ⛔ doi.
def _co(n: int) -> str:
    """Quan he cho khoi `SINH-KHOP` — ⛔ chu so nao *(`AC-5`)*."""
    return "co" if n > 0 else "⛔ khong co"


def _t1(b: Boi) -> Ket:
    k = sorted({x.khau for x in b.bang if x.khau in ("A-nap", "B-ghep", "C-sua")})
    return Ket(tai_lieu="—", ma_nguon=f"{len(k)} khau chuoi: {', '.join(k)}",
               kho="—", khop=len(k) == chuan("so_khau"))


def _t2(b: Boi) -> Ket:
    """⛔⛔ Phep nay BAT MOT CAU SAI CUA CHINH TOI, trong vong vai phut.

    Ban dau toi khai `mong=False` kem cau *"bo tai lieu ⛔ chua bao gio doc
    TEN TEP nhu mot loi khai"*. Cong ra **KHOP** ⇒ doi trang thai ⇒ NO.
    Do that: `BA-05` dong **39** va **130** khai **dung ca hai ten tep**,
    kem tab va so hang tieu de. Cau cua toi **SAI**, ⛔ khong phai cong sai.
    ⇒ `mong=True`, va giu chu thich nay lam **bia**.
    """
    n = sum(b.dem_tep(t) for t in chuan("ten_tep_asis"))
    # ⛔ Tru chinh lo trinh nay — no la BIEN BAN, ⛔ khong phai mot tep KHAI.
    rieng = sum(1 for t in chuan("ten_tep_asis") if t in b.md.get(LO_TRINH, ""))
    n -= rieng
    return Ket(tai_lieu=f"tep KHAI ten tep AS-IS (⛔ tru lo trinh): {_co(n)}",
               ma_nguon="—", kho="—", khop=n > 0,
               man=f"{n} tep KHAI ten tep AS-IS (⛔ tru lo trinh)")


def _t3(b: Boi) -> Ket:
    """⭐⭐ TU DIEN TEN — mot khau dang mang BA BO TEN.

    ⛔⛔ Ban dau phep nay do *"ten tep co mang so khau khong"* (`HAI_TAC_VU`)
    va doi no **bien mat**. Owner chot 17/09: ten CHUAN la **ten tac vu** ⇒
    ten tep ay **DANG DUNG**, ⛔ khong phai loi. Phep do cu **do sai thu**.

    ⭐ Nay no do **BANG CHUNG DUONG** (`Đ2`): moi khau chuoi phai co ten o
    **ca ba xuat xu** *(tai lieu · loi owner · ten tep AS-IS)* trong ban khai
    `TU_DIEN_TEN`, va bang sinh ra phai **co mat** trong tai lieu. Hoi *"cau
    NOI da co chua"*, ⛔ khong hoi *"ten cu con khong"*.
    """
    import importlib.util as _u                                # noqa: PLC0415
    sp = _u.spec_from_file_location("_sbd", GOC / "tools" / "sinh_ban_do_tang.py")
    m = _u.module_from_spec(sp)
    sp.loader.exec_module(m)
    chuoi = {k for k, _, loai, _ in m.KHAU if loai == "chuoi"}
    thieu = []
    for xx in m.XUAT_XU_BAT_BUOC:
        phu = {k for _, x, ks, _ in m.TU_DIEN_TEN if x == xx for k in ks}
        if not chuoi <= phu:
            thieu.append(f"{xx}: thieu {sorted(chuoi - phu)}")
    co_bang = b.dem("| Tên đang lưu hành | Xuất xứ | Khâu |") > 0
    return Ket(tai_lieu=("bang tu dien CO trong tai lieu" if co_bang
                         else "⛔ tai lieu ⛔ KHONG co bang tu dien"),
               ma_nguon=f"{len(m.TU_DIEN_TEN)} ten · "
                        + ("du ca 3 xuat xu" if not thieu
                           else "⛔ " + " · ".join(thieu)),
               kho="—", khop=not thieu and co_bang)


def _a1(b: Boi) -> Ket:
    n_ma = len(repo_chup.LAN)
    n_kho = b.so("select count(distinct src_type) from fls_source "
                 "where src_type in ('Bank','Cash','PM')")
    return Ket(tai_lieu="—", ma_nguon=f"`chup.LAN` = {n_ma} ({', '.join(repo_chup.LAN)})",
               kho=f"{n_kho} loai nguon", khop=n_ma == chuan("so_duong_vao") == n_kho)


def _a2(b: Boi) -> Ket:
    n = b.so("select count(*) from fls_chup where lan = 'Cash'")
    return Ket(tai_lieu="—", ma_nguon="`Cash` co trong `LAN`",
               kho=f"{n} anh chup lan `Cash`", khop=n > 0)


def _b1(b: Boi) -> Ket:
    """⭐⭐ `G-MOD-3` — ⛔ KHONG hoi *"da dat kieu du chua"* (do la `B6`), hoi
    *"co cot nao ROI khoi CA BA ro khong"*. Mot cot roi la mot **LO IM
    LANG**: no vao `tho` roi nam do, ⛔ khong ai biet no ton tai."""
    dat = {pm_join.PM_TIEU_DE_MONG_DOI[v] for v in pm_join.PM_COT.values()}
    cam = set(pm_join.PM_COT_RIENG_TU)
    chua = set(pm_join.PM_COT_CHUA_DAT_KIEU)
    n_kho = b.so("select count(distinct k) from fls_pm_line, "
                 "lateral json_object_keys(tho) k")
    vu_tru = n_kho + len(cam)
    roi = vu_tru - len(dat | cam | chua)
    return Ket(tai_lieu="—",
               ma_nguon=f"{len(dat)} dat kieu + {len(cam)} cam + {len(chua)} "
                        f"khai-chua-dat = {len(dat | cam | chua)}",
               kho=f"vu tru {vu_tru} cot · **{roi} cot roi khoi moi ro**",
               khop=roi == 0 and vu_tru == chuan("pm_co_ten"))


def _b6(b: Boi) -> Ket:
    """⛔ Tach rieng khoi `B1` **co y**: `B1` xanh nghia la *khong con lo im
    lang*, ⛔ KHONG nghia la *da du truong*. Gop hai cau vao mot dong la
    cach de nhat de mot khoang trong bien mat sau mot dau tick."""
    n = len(pm_join.PM_COT)
    chua = len(pm_join.PM_COT_CHUA_DAT_KIEU)
    return Ket(tai_lieu="—",
               ma_nguon=f"{n}/{chuan('pm_co_ten')} cot nguon da doc co kieu",
               kho=f"{chua} cot con nam trong `tho`, chua co kieu",
               khop=chua == 0)


def _b2(b: Boi) -> Ket:
    n = len(pm_join.PM_TIEU_DE_MONG_DOI)
    thieu = [k for k in pm_join.PM_COT.values()
             if k not in pm_join.PM_TIEU_DE_MONG_DOI]
    if thieu:
        raise LoiDo(f"`PM_COT` co vi tri ⛔ khong co tieu de mong doi: {thieu}")
    return Ket(tai_lieu="—",
               ma_nguon=f"{n}/{chuan('pm_hop_dong')} vi tri khop AS-IS tung ky tu",
               kho="—", khop=n == chuan("pm_hop_dong"))


def _anh_hieu_luc(b: Boi) -> str:
    """`run_id` cua ANH PM HIEU LUC — goi **chinh** `anh_pm_hieu_luc`.

    ⛔⛔ **Vi sao (`WO-011 T6 ⓑ`, `KQ-010 F-3`).** `B3`/`B4` tung dem tren **moi**
    anh `fls_pm_line` *(01/10: **66** anh — **196.480** dong co `tho`)*. Anh
    chup la ban chep lai CA sheet ⇒ moi gio nhip chup them ~3.820 dong y het
    ⇒ con so trong khoi `SINH-KHOP` doi ⇒ `--kiem` so ca khoi chu ⇒ **DO moi
    gio ma ⛔ ai lam sai** — bao dong keu moi gio la bao dong ⛔ ai nghe.
    ⭐ Cau hoi cua hai phep la *"lenh chi HOM NAY co cha khong"* ⇒ do tren anh
      ma moi cua doc dang dung. ⛔ Cau SQL thu hai: cung ham ma phep ghep dung.
    """
    from fls.repo.anh_pm import anh_pm_hieu_luc               # noqa: PLC0415
    from fls.repo.pham_vi import chi_nap_that                 # noqa: PLC0415

    r = anh_pm_hieu_luc(b.conn, chi_nap_that())
    if r is None:
        raise LoiDo("⛔ ⛔ co anh PM hieu luc nao — phep se XANH tren TAP RONG")
    return r


def _b3(b: Boi) -> Ket:
    """⭐ Owner chot 17/09: *"PE/PI **cot CO KIEU** trong `fls_pm_line`, chua
    can lam bang rieng"*. ⇒ Chuan ⛔ KHONG con la *"2 bang rieng"* — no la
    **5 cot co kieu**, va phep nay do ca **ban khai** lan **kho**.

    ⭐ 02/10 (`WO-011 T6`): kho do tren **anh hieu luc**; dem **dong** co cha
    *(⛔ `count(pe_line) + count(pi_line)` — mot dong hai cha bi dem hai lan)*.
    Cot `kho` in **quan he** *(moi dong · mot phan · khong dong nao)*, so in
    ra man. `khop` ⛔ doi *(`n > 0`)*."""
    khai = {c.name for c in b.bang
            if c.name == "fls_pm_line" for c in c.columns}
    co = sorted(x for x in ("pe_slip", "pe_line", "pe_loai",
                            "pi_slip", "pi_line") if x in khai)
    r = _anh_hieu_luc(b)
    n = b.so("select count(*) from fls_pm_line where run_id = %s"
             " and (pe_line is not null or pi_line is not null)", (r,))
    tong = b.so("select count(*) from fls_pm_line where run_id = %s", (r,))
    kho = ("moi dong anh PM hieu luc co cha PE hoac PI" if 0 < n == tong
           else "⛔ chi MOT PHAN dong anh PM hieu luc co cha PE hoac PI" if n
           else "⛔ KHONG dong nao trong anh PM hieu luc co cha PE hoac PI")
    return Ket(tai_lieu="—",
               ma_nguon=f"{len(co)}/5 cot co kieu"
                        + (f" ({', '.join(co)})" if co else " — ⛔ khong co"),
               kho=kho, khop=len(co) == 5 and n > 0,
               man=f"anh `{r}`: {n}/{tong} dong co cha PE hoac PI")


def _b4(b: Boi) -> Ket:
    """⭐ 02/10 (`WO-011 T6`): do tren **anh hieu luc** — xem `_anh_hieu_luc`."""
    r = _anh_hieu_luc(b)
    ngoai = b.so("""
        with x as (select (tho->>'ID PELine') pe, (tho->>'ID PILine') pi
                   from fls_pm_line where tho is not null and run_id = %s)
        select count(*) from x
        where (pe is not null and pi is not null) or (pe is null and pi is null)""",
                 (r,))
    tong = b.so("select count(*) from fls_pm_line where tho is not null"
                " and run_id = %s", (r,))
    if tong == 0:
        raise LoiDo("⛔ 0 dong co `tho` trong anh hieu luc — phep phan hoach "
                    "se XANH tren TAP RONG")
    return Ket(tai_lieu="—", ma_nguon="⛔ ⛔ khong CHECK nao canh",
               kho=("0 ngoai le trong anh PM hieu luc" if ngoai == 0
                    else "⛔ CO ngoai le trong anh PM hieu luc (so o man)"),
               khop=ngoai == 0,
               man=f"anh `{r}`: {ngoai} ngoai le / {tong:,} dong co `tho`"
                   .replace(",", "."))


# ⭐ Tep BA SONG dac ta co che de xuat cua man ghep. Mot cho khai, de bai thu
#   va phep do doc cung mot ten.
TEP_B5 = "06_SCREEN_SPEC.md"


def _b5(b: Boi) -> Ket:
    """⛔⛔ **Sua 01/10 (`WO-001 T4`, `Ra-soat` `R-5`) — phep nay hoi MOT TEP DA
    CHET.** Ban cu dem *"de xuat"* + *"goi y"* trong `12_BA_MAN_GHEP_PM.md`;
    tep ay la **BIA** tu 18/09 *(`12:7`, `CR#12` — "⛔ KHONG con la dac ta
    song")* ⇒ phep **lech mai** du co che de xuat da duoc dac ta o cho khac.
    ⭐ Ban song: `BA-06 §4` *(trong ra sao — bang 4 bac ung vien)*. Neo lai ve
    `06_SCREEN_SPEC.md`.
    ⛔ Tep neo ⛔ co trong bo tai lieu ⇒ `LoiDo` *(⛔ "0 lan" — dem tren mot tep
    ⛔ ton tai la xanh/do tren TAP RONG)*.
    """
    tep = [p for p in b.md if p.name == TEP_B5]
    if len(tep) != 1:
        raise LoiDo(f"tep neo `{TEP_B5}` khop {len(tep)} tep — phai DUNG 1")
    dx, gy = b.dem("đề xuất", TEP_B5), b.dem("gợi ý", TEP_B5)
    n = dx + gy
    # ⚠ Ten tep neo ⛔ vao o *(no mang chu so — `AC-5` doi o `B5` **0** chu
    #   so)*; o noi bang ten vai `BA`, ten tep ra **man**.
    return Ket(tai_lieu=f"tep spec man hinh (`BA` man) nhac co che de xuat: {_co(n)}",
               ma_nguon="—", kho="—", khop=n > 0,
               man=f"`{TEP_B5}`: «đề xuất» {dx} + «gợi ý» {gy} = {n} lan")


def _c1(b: Boi) -> Ket:
    vt, ten = len(canon_spec.CANON_COLS), len(canon_spec.CANON_36)
    return Ket(tai_lieu="—", ma_nguon=f"`CANON_COLS` {vt} vi tri · `CANON_36` {ten} ten",
               kho="—",
               khop=(vt, ten) == (chuan("canon_vi_tri"), chuan("canon_co_ten")))


def _c2(b: Boi) -> Ket:
    """⛔⛔ Phep nay TUNG SAI — no do `so lan xuat hien chu "64 cot"` va coi
    moi lan la mot loi. Do lai tren AS-IS: `ITL Ledge` co **64** cot CO TEN
    ⇒ tai lieu **DUNG**. ⇒ Nay no so **CON SO** voi **chuan do duoc**."""
    n = b.dem("64 cột")
    return Ket(tai_lieu=f"«64 cột» co trong tai lieu: {_co(n)}",
               ma_nguon="—", kho="—",
               khop=n > 0 and chuan("ledge_co_ten") == 64,
               man=f"«64 cột» xuat hien {n} lan")


def _c3(b: Boi) -> Ket:
    n = b.dem("7 trường")
    return Ket(tai_lieu=f"«7 trường» co trong tai lieu: {_co(n)}", ma_nguon="—",
               kho="—", khop=n > 0, man=f"«7 trường» xuat hien {n} lan")


def _c4(b: Boi) -> Ket:
    """⛔⛔⛔ Phep nay TUNG SAI NANG NHAT, va no la mot bai hoc rieng.

    Ban dau: *dem so lan chu "52 cot" xuat hien, chuan = 0*. Doc lai **19**
    cho thi **18 la BIEN BAN** *(so quyet dinh, changelog, mo ta mot GAP,
    ghi ve NGUYEN MAU 748x52)* — o do **so cu la DUNG**, va xoa chung la
    **viet lai lich su**. Cho thu 19 (`06_SCREEN_SPEC:606`) la cau noi ve
    HIEN TAI. ⇒ Do thang o ma: `len(BANG_COT)` = **52**. Tai lieu **DUNG**,
    va `GAP-SPEC-03` *(«that ra 23»)* **da cu**.
    ⇒ Nay phep so **HAI NGUON**, ⛔ khong dem chu — dung khuon cong #13.
    """
    from fls.api import cot_so                             # noqa: PLC0415
    n_ma = len(cot_so.BANG_COT)
    n_td = b.dem("52 cột")
    return Ket(tai_lieu=f"khai «52 cột» (phan lon la BIEN BAN): {_co(n_td)}",
               ma_nguon=f"`len(BANG_COT)` = {n_ma}", kho="—",
               khop=n_ma == chuan("luoi_f02") and n_td > 0,
               man=f"«52 cột» {n_td} cho")


def _c7(b: Boi) -> Ket:
    """Tong DUNG ma cach CONG SAI — hai phep cong cung ra `52`."""
    from fls.api import cot_so                             # noqa: PLC0415
    nen = len([x for x in cot_so.BANG_COT if not getattr(x, "canon", None)])
    cn = len(cot_so.BANG_COT) - nen
    # ⛔⛔⛔ BAN DAU PHEP NAY DEM CHUOI `"38 cot canon"` va doi no = 0.
    #   No LECH mai — vi cau **DINH CHINH** cung phai trich lai chuoi sai ay
    #   de noi *"cho nay tung ghi the"*. ⇒ Dung **CHINH LOP LOI** ma `C4` vua
    #   day toi hoc: **phep dem chu ⛔ khong phan biet duoc KHAI voi BIEN BAN**.
    # ⇒ Doi sang **bang chung DUONG**: tai lieu phai KHAI dung cach cong, va
    #   ma phai dong y. ⛔ Khong hoi "chuoi sai con khong" — hoi "cau DUNG co
    #   chua".
    a, c = b.dem("24 cột nền"), b.dem("28 vị trí canon")
    co = min(a, c)
    return Ket(tai_lieu=f"khai «24 nen + 28 canon»: {_co(co)}",
               ma_nguon=f"{nen} nen + {cn} canon", kho="—",
               khop=co > 0 and (nen, cn) == (chuan("luoi_nen"),
                                             chuan("luoi_canon")),
               man=f"«24 cột nền» {a} · «28 vị trí canon» {c} ⇒ min {co} cho")


def _c5(b: Boi) -> Ket:
    """Ve **COT SO** — `fls_itl.memo`.

    ⛔⛔ **Tach 01/10 (`WO-001 T4`, `Ra-soat` `R-6`).** Phep cu hoi *"`Dien giai`
    co trong SO"* va tra `0/8.387` ⇒ cau *"⛔ KHONG co trong kho — moi co che de
    xuat ⛔ do duoc"*. Tu 18/09 *(`QĐ-ITL-145`, migration `0026`)* dien giai
    **DA** co trong kho — o khung xem `fls_dien_giai` *(xem `C5b`)*, ⛔ o cot.
    Mot phep cho hai cau ⇒ cau dung cho **cot**, sai cho **kho**. ⇒ Tach hai ve;
    ve nay giu dung cau hep cua no: cot `memo` van rong *(`INV-I08` — ⛔ `UPDATE`
    duoc; `content_key` ⛔ chua dien giai ⇒ nap lai bi bo qua vi trung)*.
    """
    co = b.so("select count(memo) from fls_itl")
    tong = b.so("select count(*) from fls_itl")
    if tong == 0:
        raise LoiDo("⛔ so RONG — moi phep tren `fls_itl` se xanh gia")
    return Ket(tai_lieu="—", ma_nguon="`memo` = cot `C` cua canon",
               kho=f"{co}/{tong} dong co `memo`", khop=co > 0)


def _c5b(b: Boi) -> Ket:
    """Ve **KHUNG XEM** — `fls_dien_giai` *(migration `0026`, `QĐ-ITL-145`)*.

    ⭐ Do 01/10: **8.366** dong co dien giai / so **8.387**. Dong ⛔ co dien giai
    thi VANG khoi khung xem *(xem chu thich `schema._V_DIEN_GIAI`)* ⇒ dem
    `count(*)` cua khung xem la dem **dong CO chu**.

    ⛔⛔ **Sua 02/10 (`WO-011 T6 ⓒ`) — phep nay TROI THEO ANH, da do.** Khung
       xem noi moi dong so voi anh Bank **moi nhat** cua dung nguon ⇒ con so
       doi moi khi nhip chup mot anh Bank co chu khac o dong cu: `8.366` *(khoi
       01/10 khuya)* ⇒ `8.370` *(02/10 sang, ⛔ ai lam gi)*. Khoi `SINH-KHOP` in
       con so ay ⇒ `--kiem` DO theo nhip, cung lop `B3`/`B4` *(`KQ-010 F-3`)*.
    ⭐ Cot `kho` nay in **quan he** dung voi dieu kien `khop` *(`co > 0` — ⛔
      them nguong nao)*; so tuyet doi ra **man**. `mong` ⛔ doi.
    """
    co = b.so("select count(*) from fls_dien_giai")
    tong = b.so("select count(*) from fls_itl")
    if tong == 0:
        raise LoiDo("⛔ so RONG — moi phep tren `fls_itl` se xanh gia")
    return Ket(tai_lieu="—", ma_nguon="`fls_dien_giai` = so ⋈ anh chup moi nhat",
               kho=("CO dong so mang `Dien giai` (so o man)" if co
                    else "⛔ KHONG dong so nao mang `Dien giai`"),
               khop=co > 0, man=f"{co}/{tong} dong so co `Dien giai`")


def _c6(b: Boi) -> Ket:
    a = b.so("select count(*) from fls_adjustment")
    j = b.so("select count(*) from fls_journal")
    return Ket(tai_lieu="—", ma_nguon="—",
               kho=f"`fls_adjustment` {a} · `fls_journal` {j}", khop=a + j > 0)


def _c8(b: Boi) -> Ket:
    """⭐⭐ Ranh gioi MAY ↔ NGUOI, do THANG tren hai khung xem.

    ⛔⛔ `C6` noi *"khau sua da chay"* — no ⛔ **khong** noi ai viet. Tu
    `QĐ-ITL-143` hai cau ay **tach han**: may ghi `nguon='may_goi_y'`
    (vao `fls_may_goi_y`), nguoi ghi `'sua_tay'` (vao `fls_sua_tay`).
    Mot con so `fls_sua_tay > 0` nghia la **co nguoi that da chot mot o**
    — moc ma `BA-14` dang cho.

    ⛔⛔ **Sua 02/10 (`WO-011 T6 ⓐ`, `QĐ-ITL-150 ⓐ`, `KQ-010 F-2 ⓓ`).** Ban cu
       dem **moi** dong `fls_sua_tay` — trong khi owner chot *"UAT ⛔ BAO GIO
       tinh la nguoi that cho **bat ky** cong *nguoi da lam* nao"*, va mot cong
       cu kiem *(`verify_sua_duoc_gi.py`)* cung ghi `sua_tay` nhan danh mot ten
       may. Hom nay `fls_sua_tay` = **0** tren so that *(4 dong UAT 01/10 da
       dao het)* nen cau cu chua sai — no sai **lan dau** co mot cu UAT ⛔ dao.
    ⭐ Nguoi da chot = dong `fls_sua_tay` co `actor` ⛔ thuoc `ACTOR_MAY` **va**
      ly do ⛔ UAT — cung **mot** luat voi moc `B` *(so `danh_muc_actor`)*.
    ⭐ Ly do doc o **`fls_journal.reason`**, ⛔ qua `fls_adjustment.evt_id`:
      cu sua tay o luoi `F02` *(`ghi_but_toan`)* ghi `evt_id = NULL` — chi cu
      ghep moi co su kien. Con `fls_journal` thi **moi** duong ghi deu qua
      `ghi_tay._them`, chen but toan + nhat ky trong **mot** giao dich ⇒ cung
      `(itl_id, field, actor, at)` *(`at` = `now()` cua giao dich)*. Do 02/10
      tren so that: **4/4** dong `sua_tay` noi dung **1** dong nhat ky.
    ⚠ Dong ⛔ noi duoc nhat ky nao ⇒ ⛔ biet ly do ⇒ **tinh la nguoi** *(chieu
      cong DO de co nguoi nhin, ⛔ chieu im — `Đ5`)*.
    """
    from fls.repo import danh_muc_actor as dm                 # noqa: PLC0415

    may = b.so("select count(*) from fls_may_goi_y")
    tay = b.so(
        "select count(*) from fls_sua_tay s"
        f" where {dm.sql_ngoai_may('s.actor')}"
        " and not exists (select 1 from fls_journal j"
        "  where j.itl_id = s.itl_id and j.field = s.field"
        "    and j.actor = s.actor and j.at = s.at"
        f"    and {dm.sql_la_uat('j.reason')})")
    return Ket(tai_lieu="`0` — ⛔ chua ai go", ma_nguon="`may_ghep` vs `ghi_tay`",
               kho=f"may goi y {may} · NGUOI chot {tay} "
                   "(⛔ dem may + UAT)", khop=tay == 0)


PHEP: tuple[Phep, ...] = (
    Phep("T1", "truc", "So khau chuoi cua he", "`3` — owner `Q1`", _t1, True),
    Phep("T2", "truc", "Tai lieu KHAI ten tep AS-IS",
         "`File 1_2` · `File 2_2`", _t2, True,
         "⭐ cong bat mot cau SAI cua toi — `BA-05` dong 39 + 130 khai du"),
    Phep("T3", "truc", "⭐ TU DIEN TEN — moi khau co ten o CA BA xuat xu",
         "`3`/3 xuat xu", _t3, True,
         "⭐ owner chot 17/09: ten CHUAN la ten TAC VU ⇒ ⛔ KHONG doi ten tep"),
    Phep("A1", "Ⓐ nap", "So duong vao nap", "`3`", _a1, True),
    Phep("A2", "Ⓐ nap", "Lan `Cash` da co anh chup", "`>=1`", _a2, False,
         "lan khai ma RONG ⇒ moi cong do phu xanh gia"),
    Phep("B1", "Ⓑ ghep", "⭐ `G-MOD-3` — ⛔ KHONG cot nao ROI khoi ba ro",
         "`0` cot roi", _b1, True,
         "nguon them cot ⇒ DO cho den khi co nguoi phan loai + ghi ly do"),
    Phep("B6", "Ⓑ ghep", "Da DAT KIEU du truong `PM_Unpivot` chua",
         "`28`/28", _b6, False,
         "⛔ tach khoi `B1`: het lo im lang ⛔ KHONG nghia la du truong"),
    Phep("B2", "Ⓑ ghep", "Hop dong tieu de PM khop AS-IS", "`8`", _b2, True),
    Phep("B3", "Ⓑ ghep", "`PE`/`PI` co COT CO KIEU trong `fls_pm_line`",
         "`5` cot", _b3, True,
         "⭐ owner chot 17/09 — chua can bang rieng; migration `0023`"),
    Phep("B4", "Ⓑ ghep", "Dong lenh chi co DUNG MOT cha `PE|PI`",
         "`0` ngoai le", _b4, True, "bat bien ung vien ⇒ `CHECK`"),
    # ⭐ `mong` False ⇒ True 01/10 (`WO-001 T4`, `R-5`): ⛔ phai "da sua" —
    #   co che de xuat **da dac ta** o `BA-06 §4` tu 18/09; phep cu doc nham
    #   tep BIA `12`. Neo lai ⇒ KHOP.
    Phep("B5", "Ⓑ ghep", "Tep BA man ghep dac ta co che DE XUAT",
         "`>=1`", _b5, True,
         "⭐ neo lai 01/10: `BA-06` (⛔ `12` — BIA tu 18/09, `R-5`)"),
    Phep("C1", "Ⓒ ITL", "Khuon canon khop `Transaction Mapping L1`",
         "`38` vi tri · `36` ten", _c1, True),
    Phep("C2", "Ⓒ ITL", "So cot co ten cua `ITL Ledge`",
         "`64` (hang 7+8)", _c2, True,
         "⭐ `64` cua tai lieu DUNG — `69` cua toi la phep do qua tho"),
    Phep("C3", "Ⓒ ITL", "So truong adjust", "`7` dai", _c3, True),
    Phep("C4", "Ⓒ ITL", "So cot luoi `F02`: tai lieu vs MA",
         "`52` = `len(BANG_COT)`", _c4, True,
         "⭐ `GAP-SPEC-03` «that ra 23» DA CU — do lai 17/09"),
    Phep("C7", "Ⓒ ITL", "CACH CONG ra `52` ma tai lieu khai",
         "`24` nen + `28` canon", _c7, True,
         "⭐ SUA 17/09 — tong tung DUNG ma cach cong SAI; hai phep cong "
         "cung ra 52 nen ⛔ khong ai bat duoc"),
    # ⭐ Tach 01/10 (`WO-001 T4`, `R-6`): `C5` = COT so *(mong LECH — dung,
    #   cot `memo` van rong)* · `C5b` = KHUNG XEM *(mong KHOP — `QĐ-ITL-145`)*.
    #   ⛔ Doi ma sang tien to moi (`R-7`) — cho owner, ⛔ thuoc phieu nay.
    Phep("C5", "Ⓒ ITL", "`Dien giai` co trong COT so `fls_itl.memo`", "`>0`",
         _c5, False,
         "cot rong tu nap 10/09 — `INV-I08` ⛔ cho `UPDATE`; xem `C5b`"),
    Phep("C5b", "Ⓒ ITL", "`Dien giai` co trong KHO (khung xem `fls_dien_giai`)",
         "`>0`", _c5b, True,
         "⭐ co tu 18/09 (`QĐ-ITL-145`, migration `0026`) — tin hieu ghep "
         "giau nhat nay DO DUOC"),
    # ⭐⭐⭐ `2026-09-18` — phep nay DOI TRANG THAI, va do la mot TIN VUI:
    #    `QĐ-ITL-143` cho duong MAY ghep goi y `hd`/`cdt1` ⇒ khau sua co
    #    **4.424** but toan dau tien *(2.209 `hd` · 2.215 `cdt1`)*.
    # ⚠ Nhung `mong=True` o day noi mot cau HEP hon ve truoc: khau sua
    #    **da chay**, ⛔ chua co nghia **NGUOI da go**. Ca 4.424 but toan
    #    deu mang `nguon='may_goi_y'` va `fls_sua_tay` van **0** —
    #    xem `C8`.
    Phep("C6", "Ⓒ ITL", "Khau adjust da chay lan nao", "`>=1`", _c6, True,
         "⭐ DAT 18/09 — 4.424 but toan GOI Y cua may (`QĐ-ITL-143`)"),
    # ⭐⭐ Phep MOI: ranh gioi MAY ↔ NGUOI. Cai nay la thu dang canh —
    #    `C6` chi noi *"co but toan"*, no ⛔ khong noi **ai** viet.
    Phep("C8", "Ⓒ ITL", "⭐ NGUOI da chot o nao chua", "`0` — chua ai",
         _c8, True,
         "⛔ `fls_sua_tay` van 0: may GOI Y, nguoi CHOT — `INV-I16`"),
)


# ==========================================================================
def chay() -> tuple[list[Phep], list[str]]:
    loi: list[str] = []
    with noi_chi_doc(dsn_that()) as conn:
        b = Boi(conn)
        for p in PHEP:
            try:
                p.ket = p.fn(b)
            except LoiDo as e:
                loi.append(f"{p.ma} ⛔ KHONG DO DUOC — {e}")
            except Exception as e:                       # noqa: BLE001
                loi.append(f"{p.ma} ⛔ VO — {type(e).__name__}: {e}")
    return list(PHEP), loi


def _o(v: object) -> str:
    """Mot O bang markdown.

    ⛔⛔ **Dau `|` TRAN trong o lam VO CA BANG**, va mat thuong ⛔ khong thay
    — bang van trong nhu bang, chi la cac o **dich sang mot cot**. Lop loi
    nay da can that: `8` dong o `06_ORCHESTRATOR_DASHBOARD` *(`R | …`)*, va
    vua can lai **ngay o may sinh nay** *(o `PE|PI`, cong `K3` bat)*.
    ⇒ Thoat o **CHO SINH**, ⛔ khong doi ten truong cho vua phep do.
    """
    return str(v).replace("|", r"\|").replace("\n", " ")


def bang_md(ps: list[Phep]) -> str:
    d = [MOC_DAU, "",
         "| # | Khâu | Phát biểu | CHUẨN *(ERD ggsheet)* | Tài liệu | Mã nguồn | Kho | |",
         "|---|---|---|---|---|---|---|:--:|"]
    for p in ps:
        k = p.ket
        if k is None:
            d.append(f"| `{p.ma}` | {p.nhom} | {p.cau} | {p.chuan_} | "
                     f"⛔ | ⛔ | ⛔ | ⛔ |")
            continue
        dau = "✅" if k.khop else "⛔"
        cau = _o(p.cau) + (f" *({_o(p.ghi_chu)})*" if p.ghi_chu else "")
        d.append(f"| `{p.ma}` | {_o(p.nhom)} | {cau} | {_o(p.chuan_)} "
                 f"| {_o(k.tai_lieu)} | {_o(k.ma_nguon)} | {_o(k.kho)} "
                 f"| {dau} |")
    xong = [p for p in ps if p.ket]
    khop = sum(1 for p in xong if p.ket and p.ket.khop)
    d += ["",
          f"**{khop}/{len(xong)} khớp · {len(xong) - khop} lệch.** "
          "⛔ Bảng này **sinh bằng máy** — ⛔ không một ô nào gõ tay. "
          "Đổi một con số `CHUẨN` thì phải **đo lại và ghi xuất xứ** "
          "*(`docs/ITL/_tools/khop_owner.py`)*.",
          "", MOC_CUOI]
    return "\n".join(d)


def bom(khoi: str) -> bool:
    s = LO_TRINH.read_text(encoding="utf-8")
    i, j = s.find(MOC_DAU), s.find(MOC_CUOI)
    if i < 0 or j < 0:
        raise SystemExit(f"⛔ ⛔ ⛔ KHONG thay moc trong {LO_TRINH.name} — "
                         f"can ca `{MOC_DAU}` va `{MOC_CUOI}`")
    moi = s[:i] + khoi + s[j + len(MOC_CUOI):]
    if moi == s:
        return False
    LO_TRINH.write_text(moi, encoding="utf-8")
    return True


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--kiem", action="store_true",
                    help="CHI kiem, ⛔ khong ghi")
    a = ap.parse_args()

    ps, loi = chay()
    khoi = bang_md(ps)

    print("C1 · BANG DOI CHIEU GOC — audit alignment\n")
    xau: list[str] = list(loi)
    for p in ps:
        if p.ket is None:
            continue
        thuc = p.ket.khop
        if thuc != p.mong:
            xau.append(
                f"{p.ma} ⛔ DOI TRANG THAI: mong "
                f"{'KHOP' if p.mong else 'LECH'}, do duoc "
                f"{'KHOP' if thuc else 'LECH'} — "
                + ("mot cho DANG KHOP vua vo" if p.mong else
                   "⭐ mot cho DA DUOC SUA ⇒ ghi lai `mong` trong ban khai"))
        print(f"  {'✅' if thuc else '⛔'} {p.ma:<3} {p.cau}")
        if p.ket.man:
            # ⭐ so tuyet doi — ra MAN, ⛔ vao khoi (`WO-011 T6 ⓒ`)
            print(f"        · {p.ket.man}")

    n = sum(1 for p in ps if p.ket and p.ket.khop)
    m = sum(1 for p in ps if p.ket)
    print(f"\n  ⇒ {n}/{m} khop · {m - n} lech   "
          f"(da do {m}/{len(ps)} phep)")

    if a.kiem:
        s = LO_TRINH.read_text(encoding="utf-8")
        i, j = s.find(MOC_DAU), s.find(MOC_CUOI)
        if i < 0 or j < 0:
            xau.append("⛔ lo trinh ⛔ khong co moc `SINH-KHOP`")
        elif s[i:j + len(MOC_CUOI)] != khoi:
            xau.append("⛔ khoi trong lo trinh LECH voi ban sinh lai "
                       "⇒ chay lai ⛔ khong co `--kiem`")
    else:
        print("  · lo trinh:", "DA GHI" if bom(khoi) else "khong doi")

    if xau:
        print("\n⛔ ⛔ CONG NO:")
        for e in xau:
            print("   ·", e)
        return 1
    print("\n✅ cong `C1` DAT — bang khop ban khai, "
          f"va no da do duoc that ({m} phep tren 3 nguon)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
