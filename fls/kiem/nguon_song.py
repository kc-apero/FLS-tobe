# -*- coding: utf-8 -*-
"""Đ6 · BAY LUAT ve nguon AS-IS — **thuan**, ⛔ khong dung mang.

⭐⭐ **Vi sao tach ra khoi cong.** Nam phep do `Đ2`–`Đ5-b` deu doc **song** qua
   Sheets API. Mot cong doc mang thi ⛔ **khong the chung minh la no DO duoc**
   — muon thay no do thi phai lam hong so that. ⇒ Tach: **luat** o day *(thuan,
   vao ra la du lieu)*, **doc song** o `tools/kiem_nguon_song.py`, va **bang
   chung do duoc** o `tests/kiem/test_nguon_song.py` *(chay offline, moi luat
   co mot ca DO that)*.

⛔⛔ **Luat chung cua ca bay: DO DUOC 0 THU thi ⛔ KHONG DAT.**
   Da co tien le that trong nha: hai cong `RUN_ATOMIC` xanh suot hai thang
   tren **28 vi pham**, vi chung loc `IS NOT NULL` tren chinh cot chung canh
   ⇒ **chua tung co kha nang do**. Xanh tren tap rong la **chua do**, ⛔ khong
   phai **dat**. Nen moi luat o day tra ve ca `da_do`, va `da_do == 0` la DO.

Bay luat, moi luat la mot cau khang dinh ve cai SO — ⛔ khong phai ve FLS:

  `L1` moi sheet `R |` khai DU 6 truong o dong 1          (`Đ2`)
  `L2` tang NHAP = tang GOP, theo TUNG tai khoan          (`Đ3`)
  `L3` moi dong tang gop co xuat xu ung mot sheet `R |`   (`Đ3`)
  `L4` ⛔ KHONG dong nao mat vi KIEU O                     (`Đ4-a`)
  `L5` `|DIF| < 1.000 VND` moi ngay co du lieu            (`Đ5-a`)
  `L6` `Num` = THU TU lan xuat hien cua ma                 (`Đ5-b`)
  `L7` `_Filter` co dung bang so dong ban goc              (`Đ5-b`)
  `L8` co doi soat cua KE TOAN phai TRUE, tung tai khoan   (`QĐ-ITL-101`)
  `L9` moi tai khoan `Active` co sheet `R |` that          (`QĐ-ITL-101`)
"""
from __future__ import annotations

from collections import Counter
from typing import NamedTuple

# `QĐ-ITL-57` — dung sai ghep 1.000 VND tuyet doi. ⛔ Khong tu nghi nguong moi.
DUNG_SAI_VND = 1000.0

# ⭐ Sau truong ma dong 1 cua moi sheet `R |` phai khai.
# ⛔ **Khai o DUNG MOT cho** — `fls/adapters/sao_ke.py`. Go lai danh sach nay
#    o day la tao **ban sao thu hai cua mot luat**, dung cai ma
#    `tests/canon/test_o_loi.py` da bat duoc mot lan trong phien nay.
from fls.adapters.sao_ke import SAU_TRUONG  # noqa: F401


class KetQua(NamedTuple):
    ten: str
    dat: bool
    da_do: int          # ⛔ 0 ⇒ ⛔ KHONG dat, du ⛔ khong thay loi nao
    thong_diep: str

    @property
    def xanh(self) -> bool:
        return self.dat and self.da_do > 0


def _rong(ten: str, gi: str) -> KetQua:
    return KetQua(ten, False, 0, "⛔ do duoc 0 %s — xanh tren tap RONG la "
                                 "CHUA DO, ⛔ khong phai dat" % gi)


# ── L1 ─────────────────────────────────────────────────────────────────────
def l1_ban_khai_du_6(khai: dict[str, dict[str, int]]) -> KetQua:
    """`khai` = {ten_sheet: {ten_truong: chi_so_cot}} doc tu **dong 1**."""
    ten = "L1 · ban khai dong 1 du 6 truong"
    if not khai:
        return _rong(ten, "sheet `R |`")
    thieu = {s: sorted(set(SAU_TRUONG) - set(k)) for s, k in khai.items()
             if set(SAU_TRUONG) - set(k)}
    if thieu:
        vd = "; ".join("%s thieu %s" % (s, t)
                       for s, t in sorted(thieu.items())[:3])
        return KetQua(ten, False, len(khai),
                      "⛔ %d/%d sheet ⛔ khong khai du 6 truong — %s"
                      % (len(thieu), len(khai), vd))
    n = len(khai)
    return KetQua(ten, True, n, "%d/%d sheet khai du 6" % (n, n))


# ── L2 ─────────────────────────────────────────────────────────────────────
def l2_nhap_bang_gop(nhap: dict[str, int], gop: dict[str, int]) -> KetQua:
    """`nhap` = {sheet `R |`: so dong that}, `gop` = {xuat xu: so dong}.

    ⛔ Sheet RONG ca hai dau ⛔ khong phai loi — tai khoan da mo ma chua dung.
    """
    ten = "L2 · tang NHAP = tang GOP theo tung tai khoan"
    co = {s: n for s, n in nhap.items() if n}
    if not co:
        return _rong(ten, "tai khoan co dong")
    lech = {s: (n, gop.get(s, 0)) for s, n in co.items() if gop.get(s, 0) != n}
    if lech:
        vd = "; ".join("%s nhap %d/gop %d" % (s, a, b)
                       for s, (a, b) in sorted(lech.items())[:3])
        return KetQua(ten, False, len(co),
                      "⛔ %d/%d tai khoan LECH — %s" % (len(lech), len(co), vd))
    return KetQua(ten, True, len(co),
                  "%d tai khoan khop dung tung dong (%d dong)"
                  % (len(co), sum(co.values())))


# ── L3 ─────────────────────────────────────────────────────────────────────
def l3_xuat_xu_hop_le(gop: dict[str, int], ten_sheet: set[str]) -> KetQua:
    ten = "L3 · moi dong gop co xuat xu ung mot sheet `R |`"
    if not gop:
        return _rong(ten, "dong o tang gop")
    la = {x: n for x, n in gop.items() if x not in ten_sheet}
    if la:
        return KetQua(ten, False, sum(gop.values()),
                      "⛔ %d xuat xu LA / %d dong — %s"
                      % (len(la), sum(la.values()),
                         ", ".join(sorted(la)[:3])))
    return KetQua(ten, True, sum(gop.values()),
                  "%d dong, %d xuat xu, tat ca hop le"
                  % (sum(gop.values()), len(gop)))


# ── L4 ─────────────────────────────────────────────────────────────────────
def l4_khoa_khong_mat_vi_kieu(m_chuoi: int, m_kieu: int, tong: int) -> KetQua:
    """⛔ Trong Sheets, `VLOOKUP` mot SO vao cot CHU thi ⛔ khong khop va ⛔
    khong bao loi. `m_chuoi − m_kieu` = so dong mat **chi vi kieu o**."""
    ten = "L4 · ⛔ khong dong nao mat vi KIEU O"
    if tong <= 0:
        return _rong(ten, "khoa ben trai")
    mat = m_chuoi - m_kieu
    if mat:
        return KetQua(ten, False, tong,
                      "⛔ %d dong mat CHI VI kieu o (%.2f%% cua %d)"
                      % (mat, 100.0 * mat / tong, tong))
    return KetQua(ten, True, tong,
                  "0 dong mat vi kieu o (ghep %d/%d)" % (m_chuoi, tong))


# ── L5 ─────────────────────────────────────────────────────────────────────
def l5_lech_trong_dung_sai(lech: dict[str, float],
                           bo_qua: str = "") -> KetQua:
    """`lech` = {nhan: so lech VND}. `bo_qua` = mot nhan bi loai khoi phep kiem.

    ⚠ **Doi NGUON 2026-09-07 (`QĐ-ITL-101`).** Ban dau luat nay doc dong `226`
    cua `2. CCR` — mot con so TONG toan cong ty, tren mot **ban chup chet**.
    Owner chot ⛔ khong theo duoi ban `A-CCR` song ma **tan dung du lieu hien
    co** ⇒ luat chuyen sang `P100 ▸ BankAccountList` / `Cash Ledger List`, noi
    lech duoc tinh **TUNG TAI KHOAN** tu du lieu **song**:
        phia SAO KE = `SUMIFS(INDIRECT($D&Range_Debit), …)`  <- doc thang `R |`
        phia SO     = `SUMIFS('Bank Transactions'!D:D, …$G:$G, $D)`
    ⭐ Manh hon han ban cu: **N la co thay vi 1 con so**, va **song** thay vi
    chup. `bo_qua` giu lai vi ban cu can loai "ngay cuoi chua chot xong".
    """
    ten = "L5 · |lech| < 1.000 VND tung tai khoan"
    xet = {d: v for d, v in lech.items() if d != bo_qua}
    if not xet:
        return _rong(ten, "tai khoan do duoc")
    vuot = {d: v for d, v in xet.items() if abs(v) >= DUNG_SAI_VND}
    if vuot:
        d, v = max(vuot.items(), key=lambda p: abs(p[1]))
        return KetQua(ten, False, len(xet),
                      "⛔ %d/%d VUOT dung sai — nang nhat %s: %s VND"
                      % (len(vuot), len(xet), d, format(v, ",.0f")))
    return KetQua(ten, True, len(xet),
                  "%d tai khoan, tat ca trong dung sai" % len(xet))


# ── L6 ─────────────────────────────────────────────────────────────────────
def l6_num_la_thu_tu(ma: list[str], num: list) -> KetQua:
    """`Num` phai bang **lan thu may** ma ay xuat hien, dem tu tren xuong."""
    ten = "L6 · `Num` = THU TU lan xuat hien cua ma"
    thay: Counter = Counter()
    ok = sai = 0
    dau_sai = ""
    for i, m in enumerate(ma):
        if not m:
            continue
        thay[m] += 1
        v = num[i] if i < len(num) else ""
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        if int(v) == thay[m]:
            ok += 1
        else:
            sai += 1
            dau_sai = dau_sai or "dong %d: ghi %d, phai %d" % (
                i + 1, int(v), thay[m])
    if ok + sai == 0:
        return _rong(ten, "dong co ma va co `Num`")
    if sai:
        return KetQua(ten, False, ok + sai,
                      "⛔ %d/%d dong SAI thu tu — %s" % (sai, ok + sai, dau_sai))
    return KetQua(ten, True, ok, "%d/%d dong dung thu tu" % (ok, ok))


# ── L7 ─────────────────────────────────────────────────────────────────────
def l7_cau_bang_ban_goc(n_goc: int, n_cau: int) -> KetQua:
    """`Bank Transactions_Filter` ⛔ khong phai bo LOC — no la **cai CAU** doi
    khuon bank → khuon so ke toan ⇒ no phai co **dung bang** so dong ban goc.
    """
    ten = "L7 · cai cau `_Filter` bang dung ban goc"
    if n_goc <= 0:
        return _rong(ten, "dong ban goc")
    if n_cau != n_goc:
        return KetQua(ten, False, n_goc,
                      "⛔ ban goc %d ⇔ cau %d (lech %+d)"
                      % (n_goc, n_cau, n_cau - n_goc))
    return KetQua(ten, True, n_goc, "ca hai deu %d dong" % n_goc)


# ── L8 ─────────────────────────────────────────────────────────────────────
def l8_co_doi_soat(co: dict[str, object], trang_thai: dict[str, str]) -> KetQua:
    """⭐⭐ **Day la LUAT CUA CHINH KE TOAN, ⛔ khong phai luat toi nghi ra.**

    `BankAccountList` co san hai cot `=J3=M3` va `=K3=M3` — **so tong No/Co
    doc thang tu sheet `R |` (SAO KE)** voi **so tong o `Bank Transactions`
    (SO)**, cho **TUNG tai khoan**. Cong nay chi **doc lay** ket qua ay.

    ⛔ `co` = {ten tai khoan: True/False/None}. `None` *(o trong)* tren mot tai
    khoan `Active` la **DO**, ⛔ khong phai bo qua: phep kiem ⛔ khong chay thi
    ⛔ khong duoc coi la dat. Tai khoan `Closed`/`InActive` thi bo qua.
    """
    ten = "L8 · co doi soat cua ke toan phai TRUE (tung tai khoan)"
    xet = {k: v for k, v in co.items()
           if trang_thai.get(k, "").strip().lower() == "active"}
    if not xet:
        return _rong(ten, "tai khoan `Active`")
    sai = sorted(k for k, v in xet.items() if v is not True)
    if sai:
        return KetQua(ten, False, len(xet),
                      "⛔ %d/%d tai khoan `Active` ⛔ KHONG khop — %s"
                      % (len(sai), len(xet), ", ".join(sai[:4])))
    return KetQua(ten, True, len(xet),
                  "%d tai khoan `Active`, tat ca khop" % len(xet))


# ── L9 ─────────────────────────────────────────────────────────────────────
def l9_danh_muc_khop_sheet(bang_sheet: dict[str, str],
                           co_that: set[str]) -> KetQua:
    """Moi tai khoan `Active` trong danh muc phai co **sheet `R |` that**.

    ⛔ Sinh ra tu mot cau do do duoc ma ⛔ chua ai hoi: danh muc co **69** dong,
    workbook co **60** sheet `R |`, va **50** sheet co du lieu. Cot
    `Account Status` giai phan lon *(`Closed` 10 · `InActive` 5)* — nhung
    phan con lai thi phai **do**, ⛔ khong duoc doan.
    """
    ten = "L9 · moi tai khoan `Active` co sheet `R |` that"
    if not bang_sheet:
        return _rong(ten, "tai khoan `Active`")
    thieu = sorted(k for k, s in bang_sheet.items() if s not in co_that)
    if thieu:
        return KetQua(ten, False, len(bang_sheet),
                      "⛔ %d/%d tai khoan `Active` ⛔ khong co sheet — %s"
                      % (len(thieu), len(bang_sheet),
                         ", ".join(bang_sheet[k] for k in thieu[:3])))
    return KetQua(ten, True, len(bang_sheet),
                  "%d tai khoan `Active` deu co sheet" % len(bang_sheet))
