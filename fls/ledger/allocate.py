# -*- coding: utf-8 -*-
"""Vung ALLOCATE cua `ITL Ledge` — BA cot, va ca ba SUY LAI DUOC.

Owner dua nguyen van ba cong thuc 2026-08-28. Chep lai o day vi day la SSOT
cua phep suy, ⛔ khong dien giai lai bang loi:

    AU  =ArrayFormula(AD7:AD)

    AV  =ArrayFormula(if(VLOOKUP(V7:V,{'[Importrange]Mapping Master'!H:H,
                                       '[Importrange]Mapping Master'!K:K},2,FALSE)
                         ="Need to Allocate to CFA2",
                         "Need to Allocate to CFA2",
                         AU7:AU))

    AW  =ArrayFormula(if(VLOOKUP(V7:V,{'[Importrange]Mapping Master'!H:H,
                                       '[Importrange]Mapping Master'!L:L},2,FALSE)<>"",
                         VLOOKUP(V7:V,{...L:L},2,FALSE),
                         "No need"))

Doc ra ba dieu, va ca ba deu doi mo hinh:

  ⓐ **`AU` (CFA1) la BAN SAO cua `AD`** — ma `AD` = *Chu du toan · Final* =
    `cdt1`. ⇒ Luu `cdt1_cfa1` thanh mot cot rieng la **hai ban su that** cho
    cung mot gia tri. Dung benh `=L130` cua so P100: mot cong thuc guong chiem
    o, roi ai cung tuong do la mot con so doc lap.

  ⓑ **Quyet dinh phan bo ⛔ KHONG nam o `ITL Ledge`** — no nam o
    **`Mapping Master`** cot `K` *(can phan bo khong)* va `L` *(phuong phap)*,
    tra theo **`V` = `hd`** *(Budget Code · Final)*. `ITL Ledge` chi **hien lai**.
    ⇒ FLS da co bang `fls_mapping_master(need_cfa2, method_cfa2)`, nen ba cot
    kia **suy lai duoc 100%**, ⛔ khong can luu.

  ⓒ **Hai cot tron CO voi GIA TRI trong cung mot o.** `"Need to Allocate to
    CFA2"` ⛔ khong phai mot ma CDT; `"No need"` ⛔ khong phai mot phuong phap.
    Nhet ca hai vao mot cot text thi som muon co nguoi doc **co** thanh **gia
    tri** — nen o day **tach ra**: `can_phan_bo` la mot co rieng.

⛔⛔ HAI BAY NGU NGHIA CUA SHEETS ma toi ⛔ CHUA do duoc (khai ra, ⛔ khong de
tu suy — can mot lan doc `Mapping Master` that moi chot):

  ⚠ `=` trong Sheets so chuoi **KHONG phan biet hoa thuong**. Nen
    `"need to allocate to cfa2"` o `Mapping Master` **VAN khop**. Python thi
    phan biet. ⇒ o day so **khong phan biet hoa thuong** de bam theo sheet;
    ⛔ nhung neu owner muon chat hon thi phai doi o CA HAI ben.

  ⚠⚠ `VLOOKUP` tra ve mot **o RONG** thi Sheets cho ra **`0`** *(so khong)*,
    ⛔ khong phai `""`. Luc do `<>""` la **DUNG** ⇒ cot `Method` se ra **`0`**
    chu ⛔ khong ra `"No need"`. ⇒ `"No need"` chi xuat hien khi `Mapping
    Master` that su co mot o chua chuoi rong. Ham nay giu **dung** hanh vi ay
    *(xem `_rong_kieu_sheets`)*, va con so *"bao nhieu dong ra `0`"* la mot
    phep do **chua chay** — `GAP-ALLOC-01`.

⛔ Va mot lech dia chi phai noi ra: ba cong thuc neo `AD7:AD` / `V7:V` /
`AU7:AU` — tuc du lieu bat dau **dong 7**. Ban khai nguon cua FLS
(`oracle.nguon.SO_GOC_ADJUSTED.dong_dau`) noi **dong 10**. Hai con so ⛔ khong
the cung dung; neu sai thi moi phep so lech **3 dong** trong im lang.
"""
from __future__ import annotations

import dataclasses
from typing import Any

# Hai chuoi CO — chep dung nguyen van tu cong thuc, ⛔ khong viet lai.
CO_CAN_PHAN_BO = "Need to Allocate to CFA2"
CO_KHONG_CAN = "No need"

# `VLOOKUP(...,FALSE)` khong tim thay khoa ⇒ Sheets cho `#N/A`. ⛔ Giu nguyen,
# ⛔ khong bien thanh rong: mot `#N/A` la *"khong tra duoc"*, con rong la
# *"tra duoc va no rong"* — hai chuyen khac nhau (`INV-I16`).
KHONG_TRA_DUOC = "#N/A"


@dataclasses.dataclass(frozen=True)
class VungAllocate:
    """Ba o cua vung ALLOCATE + mot CO tach rieng."""

    cfa1: str
    cfa2: str
    method: str
    can_phan_bo: bool
    # ⛔ True khi `hd` ⛔ khong co trong `Mapping Master` ⇒ ca hai o la `#N/A`.
    khong_tra_duoc: bool


def _rong_kieu_sheets(v: Any) -> bool:
    """`<>""` cua Sheets: CHI chuoi rong la rong.

    ⛔ Mot o RONG that thi `VLOOKUP` tra `0`, va `0 <> ""` la **DUNG** — nen
    `0` ⛔ KHONG duoc coi la rong o day. Mot dau cach cung ⛔ khong rong.
    """
    return v is not None and isinstance(v, str) and v == ""


def _khop_co(v: Any) -> bool:
    """So voi chuoi CO theo dung kieu Sheets: ⛔ KHONG phan biet hoa thuong."""
    return isinstance(v, str) and v.strip().lower() == CO_CAN_PHAN_BO.lower()


def suy_allocate(cdt1: Any, hd: Any, mm: Any) -> VungAllocate:
    """Suy ba o tu `cdt1` *(AD)* + `hd` *(V)* + mot dong `Mapping Master`.

    `mm` la `None` khi ⛔ khong tra duoc `hd` — hay mot doi tuong/dict co
    `need_cfa2` va `method_cfa2` *(= cot `K` va `L`)*.
    """
    cfa1 = "" if cdt1 is None else str(cdt1)

    if mm is None or hd is None or str(hd).strip() == "":
        # ⛔ Khong tra duoc: sheet hien `#N/A` o CA HAI o. ⛔ Khong bia gia tri,
        # ⛔ khong roi ve `cfa1` — vi cong thuc chi roi ve `AU` khi VLOOKUP
        # THANH CONG ma tra ve mot gia tri khac chuoi co.
        return VungAllocate(cfa1=cfa1, cfa2=KHONG_TRA_DUOC,
                            method=KHONG_TRA_DUOC, can_phan_bo=False,
                            khong_tra_duoc=True)

    lay = (mm.get if isinstance(mm, dict) else lambda k: getattr(mm, k, None))
    need = lay("need_cfa2")
    method = lay("method_cfa2")

    can = _khop_co(need)

    # AW — ba nhanh, va nhanh dau la BAY da khai o dau file:
    if method is None:
        # ⚠⚠ O `Mapping Master!L` RONG THAT: `VLOOKUP` cua Sheets tra ve **`0`**,
        # va `0 <> ""` la **DUNG** ⇒ o `Method` hien **`0`**, ⛔ KHONG phai
        # `"No need"`. Giu dung hanh vi ay vi thuoc chuan la CHINH O SHEET;
        # ⛔ khong "chua cho dep" o day roi lech parity.
        ra_method = "0"
    elif _rong_kieu_sheets(method):
        ra_method = CO_KHONG_CAN
    else:
        ra_method = str(method)

    return VungAllocate(
        cfa1=cfa1,
        # AV: co thi hien CO, ⛔ khong thi roi ve AU (= cfa1 = cdt1)
        cfa2=CO_CAN_PHAN_BO if can else cfa1,
        method=ra_method,
        can_phan_bo=can,
        khong_tra_duoc=False)
