# -*- coding: utf-8 -*-
"""Bo nap `Mapping Master` — bang QUYET DINH PHAN BO, tra theo `hd`.

★★ **Vi sao bang nay phai vao kho.** Ngay 28/08 owner dua nguyen van ba cong
thuc vung `ALLOCATE`, va chung chung minh **quyet dinh phan bo ⛔ khong nam o
so ITL** — no nam o `Mapping Master` cot `K`/`L`, tra theo `hd`. Vi the nam cot
vung ALLOCATE bi **bo khoi khuon kho** (`QĐ-ITL-65`, migration `0012`) va thay
bang mot **phep tinh** (`fls/ledger/allocate.py`).

⛔⛔ Nhung phep tinh do doc `fls_mapping_master`, ma bang ay **0 dong** va ⛔ chua
co bo nap ⇒ tu 28/08 den nay phep suy **luon tra `#N/A`**. Tuc loi hua *"vung
phan bo se hien lai nhu mot phep tinh"* dang treo. File nay tra loi hua do.

★ **DA DO THAT tren nguon** (RAW `Mapping Master`, 2026-08-28) — moi con so duoi
day la so **do duoc**, ⛔ khong phai suy:

  ⓐ Tab `Mapping Master` **nam ngay trong file RAW** *(4.464 x 40)* — nguon
    owner da chot (`QĐ-ITL-50`). ⇒ ⛔ KHONG can mo so ADJUSTED cho viec nay.
    *(So ADJUSTED co tab `[Importrange]Mapping Master` — mot BAN CHIEU, va no
    hep hon goc: 26 cot so voi 40.)*

  ⓑ **Header o dong 3, nhan phu o dong 4–6, du lieu bat dau DONG 7.** Con so
    **7** nay trung khit voi neo `V7:V` cua ba cong thuc ALLOCATE ⇒ hai phep do
    doc lap noi cung mot con so. *(⚠ Va no ⛔ khong lien quan gi den lech
    `dong_dau` 7-vs-8-vs-10 cua tab `ITL Ledge` — do la mot cai khac, van mo.)*

  ⓒ **73 ma `hd`**, ⛔ **0 ma trung**. Vung du lieu ket thuc ~dong 85 *(day la
    ca `PL2..PL8` — cac dong bac thang, cung la ma `hd`)*.

  ⓓ **23 ma co co `Need to Allocate to CFA2`**; 21 ma co phuong phap, tu mot
    tu vung nho: `By GI`(8) · `By NOEM`(5) · `H1000 Ledger`(4) · `GI Ledger` ·
    `OMC Ledger` · `PS Ledger` · `SC Ledger`.

  ⓔ ⭐⭐ **52 trong 73 ma co cot `L` RONG** ⇒ dung cai bay `VLOOKUP` da khai o
    `ledger/allocate.py`: o `Method` cua sheet hien **`0`**, ⛔ KHONG hien
    `"No need"`. Truoc hom nay con so nay la *"mot phep do chua chay"*
    (`GAP-ALLOC-01`); gio no la **52/73**.

  ⓕ ⚠ `COA1`/`COA2` *(cot `I`/`J`)* do tu dong 7 la **0 va 0** — hai cot RONG
    HOAN TOAN. ⇒ Bo nap van doc chung *(khuon kho co hai cot ay)*, nhung ai
    thay chung rong thi ⛔ dung ket luan bo nap sai: **nguon rong**.

  ⛔⛔ **Va mot bai hoc ve phep dem, ghi lai vi no la lo lop tren.** Luot do dau
  cua toi cat tu **dong 4** va ra `method_rong = 53` · `coa1 = 1`. Ca hai deu
  SAI, va sai theo cung mot kieu: dong 4 mang **nhan phu** *(`H4 = 'HD Code'`)*
  va mot **vet cong thuc vo** *(`J4 = '#REF! (Please use a desktop…)'`)*. ⇒ Cat
  dung o dong 7 thi ra **52** va **0**. Ba dong header 4–6 ⛔ khong phai du lieu,
  va mot phep dem lay ca chung thi **tu khop voi chinh no** ma van sai.

⛔ **Mot dieu phai khai ra, ⛔ khong lam im lang:** phep suy phan bo doc bang
  nay **LUC HIEN**, nen sua mot dong `Mapping Master` se doi ca gia tri phan bo
  cua **lich su**. Day ⛔ khong phai mot lo cua FLS — sheet that dang chay dung
  nhu vay (`VLOOKUP` song). Chep lai hanh vi la **dung**; nhung ai muon so phan
  bo dong bang theo ky thi phai mo mot quyet dinh moi, ⛔ khong sua le o day.
"""
from __future__ import annotations

from dataclasses import dataclass

from fls.canon.o_loi import la_o_loi

# ── Dia chi, do duoc 2026-08-28 ──────────────────────────────────────────
TAB = "Mapping Master"
DONG_DAU = 7          # header dong 3 · nhan phu 4-6 · du lieu tu DONG 7

# Cot -> truong cua `fls_mapping_master`. ⛔ Khai o MOT cho; doi nguon la doi
# mot dong, va co bai test khoa dia chi nay.
COT: dict[str, str] = {
    "H": "hd_code",        # dong 3 trong, dong 4 ghi 'HD Code'
    "I": "coa1",           # nhan dong 3 = COA1  (do tu dong 7: RONG het)
    "J": "coa2",           # nhan dong 3 = COA2  (do tu dong 7: RONG het)
    "K": "need_cfa2",      # nhan dong 3 = 'Need to Allocate to CFA2'
    "L": "method_cfa2",    # nhan dong 3 = 'Method to Allocate to CFA2'
    "M": "code_hr",        # nhan dong 3 = 'Code HR Allocate'
}
TRUONG: tuple[str, ...] = tuple(COT.values())


@dataclass(frozen=True)
class DongMM:
    """Mot dong `Mapping Master`. Moi truong ⛔ khong bat buoc, TRU `hd_code`."""

    dong_sheet: int
    hd_code: str
    coa1: str | None = None
    coa2: str | None = None
    need_cfa2: str | None = None
    method_cfa2: str | None = None
    code_hr: str | None = None


@dataclass(frozen=True)
class Loai:
    """Mot dong BI LOAI, kem ly do CO TEN (`ACC-4`). ⛔ Khong loai im lang."""

    dong_sheet: int
    hd_code: str
    ly_do: str


def _sach(v) -> str | None:
    """O -> gia tri luu. Rong hay chi dau cach -> `None`.

    ⛔⛔ **`None` o day KHONG phai "khong biet"** — no la *"o nay rong"*, va do
    la mot CAU TRA LOI co nghia: `ledger/allocate.py` bien `method=None` thanh
    `"0"` dung nhu Sheets lam. Neu doi `None` thanh `""` thi o `Method` se ra
    `"No need"` — **lech han** voi sheet that (xem bay `VLOOKUP`).
    """
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def doc_cot(cot: dict[str, list], *, dong_dau: int = DONG_DAU
            ) -> tuple[list[DongMM], list[Loai]]:
    """Sau cot THO (theo chu cai, tinh tu DONG 1) -> cac dong + cac dong bi loai.

    Ham THUAN: ⛔ khong mang, ⛔ khong kho. Viec doc Sheets nam o
    `tools/nap_mapping_master.py`.

    ★ Thu tu cac phep kiem la CO CHU Y:
      ⓐ ⛔ khong co `hd_code`   -> BO IM (dong trong cua vung 4.464 dong)
      ⓑ `hd_code` la mot O LOI  -> `Loai`, vi mot ma loi ⛔ khong tra duoc
      ⓒ `hd_code` TRUNG         -> `Loai` **ca dong sau**, giu dong dau
    """
    thieu = [c for c in COT if c not in cot]
    if thieu:
        raise ValueError(f"⛔ thieu cot {thieu} — bo nap doc {sorted(COT)}")

    n = max((len(v) for v in cot.values()), default=0)
    ra: list[DongMM] = []
    loai: list[Loai] = []
    da_thay: dict[str, int] = {}

    for k in range(dong_dau - 1, n):
        o = {t: (cot[c][k] if k < len(cot[c]) else None)
             for c, t in COT.items()}
        ma_tho = o["hd_code"]
        ma = _sach(ma_tho)
        if ma is None:
            continue                                              # ⓐ
        if la_o_loi(ma_tho):                                      # ⓑ
            loai.append(Loai(k + 1, str(ma_tho)[:60],
                             "hd_code la O LOI — mot ma loi ⛔ khong tra duoc"))
            continue
        if ma in da_thay:                                         # ⓒ
            loai.append(Loai(
                k + 1, ma,
                f"hd_code TRUNG voi dong {da_thay[ma]} — mot ma hai dong thi "
                f"`VLOOKUP` lay dong DAU, nen dong nay ⛔ khong bao gio duoc "
                f"dung; giu no lai la giu mot ban su that thu hai"))
            continue
        da_thay[ma] = k + 1
        ra.append(DongMM(dong_sheet=k + 1, hd_code=ma,
                         **{t: _sach(v) for t, v in o.items()
                            if t != "hd_code"}))
    return ra, loai


def tom_tat(dong: list[DongMM]) -> dict[str, int]:
    """May con so de doi chieu voi phep do tren nguon — ⛔ khong de trang tri.

    ⭐ `method_rong` la con so dong `GAP-ALLOC-01`: bao nhieu ma se lam o
    `Method` cua sheet hien **`0`** thay vi `"No need"`.
    """
    return {
        "ma": len(dong),
        "can_phan_bo": sum(1 for d in dong if (d.need_cfa2 or "").strip()),
        "co_phuong_phap": sum(1 for d in dong if (d.method_cfa2 or "").strip()),
        "method_rong": sum(1 for d in dong if not (d.method_cfa2 or "").strip()),
        "co_code_hr": sum(1 for d in dong if (d.code_hr or "").strip()),
        "co_coa1": sum(1 for d in dong if (d.coa1 or "").strip()),
        "co_coa2": sum(1 for d in dong if (d.coa2 or "").strip()),
    }
