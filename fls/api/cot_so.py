"""BANG COT cua luoi `F02` — khai **mot lan**, sinh ra ca tieu de ca cong kiem.

★ Cung khuon voi `fls/db/model.py`, `fls/api/bang_tuyen.py`, `fls/web/phuc_vu.py`:
mot ban khai duy nhat, hai dau ra. O day la (tieu de tieng Viet cho man hinh +
cong doi chieu voi cua that).

⛔⛔ **Vi sao tep nay ton tai, thay vi go 23 tieu de vao `man_f02.js`.**
`DEV-12 · B5` doi *"tieu de tieng Viet lay tu khuon canon — mot nguon duy nhat,
⛔ khong go lai"*. Neu go tay o tang man hinh thi ngay so doi ten mot cot, man
hinh van hien ten cu — va **⛔ khong mot phep thu nao do**. Ke toan doc ten cu,
doi chieu voi so that mang ten moi, va lech ay ⛔ khong bao gio no ra.

★ **Hai nguon ten, ⛔ khong phai mot** — va day la mot phep do, ⛔ khong phai
mot lua chon:
  ⓐ `fls/oracle/ledge_spec.COT_LUU` — **18 cot** cua `ITL Ledge` (so DAU RA ma
    ke toan mo hang ngay). Day la nguon dung cho moi cot co mat trong so ay.
  ⓑ `fls/canon/spec.CANON_COLS` — **38 vi tri** cua khuon dau vao. Dung cho cot
    co trong canon ma ⛔ khong co trong Ledge (`le_payer` = canon `L`).
  ⓒ Con lai la **cua rieng FLS** (danh tinh · lineage · trang thai). Chung
    ⛔ khong co ten o dau ca, nen moi cot nhu the **PHAI noi vi sao** — o
    `vi_sao`. Mot ten tu bia ma ⛔ khong ai giai thich la mot ten se troi.

⚠⚠ **Ban ve `FLS-Design-P6` phac tieu de NGAN hon** *(`Mã hợp đồng` thay
`Budget Code · Final`)*. Toi giu ten cua **so that**, ⛔ khong lay ban phac:
ban ve la nguon cua **hinh dang** *(owner chot 03/09)*, ⛔ khong phai nguon cua
**tu vung du lieu**. Dat mot ten thu hai cho cung mot cot la tao ra hai tu vung,
va sau vai thang ⛔ khong ai con biet cot nao la cot nao.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from fls.canon.spec import CANON_COLS
from fls.oracle.ledge_spec import COT_LUU

# ⛔ Kieu o. Ban TRANG — man hinh chi biet nhung kieu nay, gap kieu la thi
# `kiem_bang_cot` NO chu ⛔ khong ve dai.
KIEU_O: frozenset[str] = frozenset({
    "so",     # so nguyen, canh phai, `tabular-nums`
    "tien",   # tien — chuoi, ⛔ KHONG BAO GIO `float`; am thi do
    "ngay",   # ISO `YYYY-MM-DD`
    "chu",    # chuoi
    "chip",   # gia tri it lua chon ⇒ ve thanh chip
})

# 5 truong nguoi go duoc **ngay tren luoi**. ⛔ Day KHONG phai ca 7 truong cua
# `TRUONG_GHI`: `id_payee` va `invoice` ⛔ khong co trong cau tra loi cua
# `GET /ledger` *(chung chi ra o `GET /ledger/{id}`)*, nen tren luoi
# ⛔ **khong co o de go** — chung go o **drawer**. Khai ro o day de ⛔ khong ai
# doc "7 truong go duoc" roi di tim hai o khong ton tai.
GO_TREN_LUOI: tuple[str, ...] = ("hd", "pay_type", "cdt1", "svc_start",
                                 "svc_end")
GO_O_DRAWER: tuple[str, ...] = ("id_payee", "invoice")

# ⭐⭐ O nao la VAN XUOI (dat chu `sans`) — moi o CON LAI dat chu may (`mono`).
#
# ⛔⛔ Vi sao mac dinh la `mono` chu ⛔ khong phai `sans`: day la mot cuon SO.
# Gan het gia tri o day la **ma** — `FT24295070629325` · `R | 24138888_TCB` ·
# `VVOT` · mot ngay · mot so tien. Ma dat chu may thi cac ky tu **thang cot**,
# nen mot ky tu bi doi **nhin ra duoc**; dat chu thuong thi ⛔ khong.
#
# ⛔ Va vi sao ban khai nay khoa theo **TEN** chu ⛔ khong theo ten truong: cung
# mot o xuat hien o HAI bang — `BANG_COT` *(qua `nhan_cua`)* va `CANON_COLS`
# *(qua `.name`)*. Khoa theo ten thi **mot** ban khai phuc vu ca hai; khoa theo
# truong thi phai khai hai lan, va hai ban khai roi se lech.
#
# ⚠ `kieu` ⛔ KHONG dung duoc cho viec nay: **38/52** cot mang kieu `"chu"` —
# no la thung chua tat ca, gom ca van xuoi lan ma. Do that, ⛔ khong phong doan.
VAN_XUOI: frozenset[str] = frozenset({"Diễn giải"})

# ⭐⭐ Truong cua tra ma CO Y ⛔ khong lam mot cot tren luoi — **kem ly do**.
#
# ⛔⛔ Cong `kiem_bang_cot` doi **moi** truong cua tra phai duoc khai, vi mot
# truong ⛔ khong ai khai se bi luoi **giau trong im lang**. Nhung co nhung
# truong that su ⛔ khong nen len luoi *(co bat/tat, gia tri lap lai cot khac)*.
# ⇒ Chung nam o day, va **moi cai phai noi vi sao** — de "⛔ khong len luoi" la
# mot **quyet dinh doc duoc**, ⛔ khong phai mot cho bo quen.
KHONG_LEN_LUOI: dict[str, str] = {
    "alloc_cfa1": "no LAP LAI y het cot `Chủ dự toán · Final` (`cfa1` = `cdt1` "
                  "theo dinh nghia cua `suy_allocate`). Hai cot giong het nhau "
                  "canh nhau lam nguoi doc tuong may dang noi hai dieu",
    "alloc_can_phan_bo": "CO bat/tat, ⛔ khong phai gia tri de doc. No da nam "
                         "TRONG chu cua o `CFA2 🔒` (`Need to Allocate to "
                         "CFA2` hay ten don vi)",
    "alloc_na": "CO *\"⛔ khong tra duoc `hd`\"*. No quyet dinh **cach ve** hai "
                "o phan bo (`#N/A`), ⛔ khong phai mot cot rieng",
}


@dataclass(frozen=True)
class Cot:
    truong: str            # ten truong TRONG cau tra loi cua `GET /ledger`
    kieu: str
    # ⭐ Nguon cua TEN. Dung MOT trong hai, hay ⛔ khong cai nao (thi phai co
    # `vi_sao`). ⛔ Khong bao gio ca hai — hai nguon cho mot ten la hai su that.
    ledge: str = ""        # chu cai trong `ITL Ledge` (`COT_LUU`)
    canon: str = ""        # chu cai trong khuon canon (`CANON_COLS`)
    nhan: str = ""         # ⭐ ⛔ KHONG go tay khi co `ledge`/`canon` — cong dien
    vi_sao: str = ""       # BAT BUOC khi ⛔ khong co nguon ten
    go: bool = False       # nguoi go duoc ngay tren luoi?
    khoa: int = 0          # 1 = cot dong cung thu nhat · 2 = thu hai · 0 = cuon


# ── Bang cot cua luoi. Thu tu o day LA thu tu tren man hinh. ──────────────
#
# ⭐ Hai cot dau **dong cung** khi cuon ngang — lay dung theo ban ve
# `FLS-Design-P6` *(`f1` = `itl_id`, `f2` = `Diễn giải`)*. Tong be rong
# **346px** *(96 + 250)* la con so `06_SCREEN_SPEC` §2 khai va **cho UAT xac
# nhan co du hay khong** — ⛔ khong phai con so da nghiem thu.
BANG_COT: tuple[Cot, ...] = (
    Cot("itl_id", "so", khoa=1,
        nhan="Số dòng ITL",
        vi_sao="danh tinh RIENG cua FLS (`INV-I04a` sequence dong bang) — "
               "⛔ khong co trong canon lan Ledge. Ke toan can no de goi ten "
               "mot dong khi hoi nhau"),
    Cot("memo", "chu", ledge="C", khoa=2),
    Cot("doc_date", "ngay", ledge="A"),
    Cot("doc_no", "chu", ledge="B"),
    Cot("curr", "chip", ledge="D"),
    Cot("ps_no", "tien", ledge="E"),
    Cot("ps_co", "tien", ledge="F"),
    Cot("acct", "chu", ledge="G"),
    Cot("le", "chip", ledge="P"),
    Cot("le_payer", "chip", canon="L"),
    # ── 5 o GO DUOC ────────────────────────────────────────────────────
    Cot("hd", "chu", ledge="V", go=True),
    Cot("pay_type", "chu", ledge="Z", go=True),
    Cot("cdt1", "chu", ledge="AD", go=True),
    Cot("svc_start", "ngay", ledge="AH", go=True),
    Cot("svc_end", "ngay", ledge="AL", go=True),
    # ── ⭐ vung PHAN BO 🔒 — MAY suy, nguoi ⛔ khong go duoc (`QĐ-ITL-64`) ──
    #
    # ⛔⛔ Ba o nay tung ⛔ **khong ve duoc** *(⛔ khong cua nao mang chung)* va
    # man phai noi thang dieu do. Nay cua `GET /ledger` mang chung — suy o
    # **may chu** bang `fls/ledger/allocate.py`, mot ban duy nhat.
    #
    # ⚠ `Method` co the hien dung chu **`0`**, va do la **cau tra loi dung**:
    # o `Mapping Master!L` rong that thi `VLOOKUP` cua Sheets cho `0`. ⛔ Dung
    # chua cho dep — xem `fls/ledger/allocate.py`.
    Cot("alloc_cfa2", "chu",
        nhan="Phân bổ CFA2 🔒",
        vi_sao="MAY suy tu `cdt1` + `hd` + `Mapping Master` cot K "
               "(`fls/ledger/allocate.py`). ⛔ Khong co trong so nao ca: no la "
               "mot phep TINH, va nguoi ⛔ khong go duoc (`QĐ-ITL-64` da dua "
               "ba o vung ALLOCATE RA KHOI tap truong go duoc)"),
    Cot("alloc_method", "chu",
        nhan="Cách phân bổ 🔒",
        vi_sao="MAY suy tu `Mapping Master` cot L. ⛔ Khong go duoc, cung ly do "
               "voi `alloc_cfa2`"),
    # ── trang thai + lineage ───────────────────────────────────────────
    Cot("work_status", "chip", ledge="BK"),
    Cot("pm_hinh", "chip",
        nhan="Hình ghép lệnh chi",
        vi_sao="`A`/`B`/`C` — HINH cua phep ghep, do `fls/adapters/pm_join.py` "
               "suy ra. ⛔ Khong phai mot cot cua so nao: no la ket qua cua "
               "mot phep ghep da qua cong Σ"),
    Cot("is_flash", "chip",
        nhan="Số nháp (chưa đối soát)",
        vi_sao="co niem tin cua rieng FLS — `flash` la so **chua** ai doi soat. "
               "⛔ Khong co trong so goc vi so goc ⛔ khong phan biet"),
    Cot("period_state", "chip",
        nhan="Kỳ",
        vi_sao="`open`/`locked` — trang thai KY cua FLS (`INV-I13`). Ky da chot "
               "thi ⛔ khong o nao go duoc, ke ca voi `force`"),
    Cot("run_id", "chu",
        nhan="Lần nạp",
        vi_sao="lineage `INV-I12`. ⛔ Khong co trong so: no tra loi *'con so "
               "nay den tu lan keo nao'*"),
    Cot("source_system", "chu",
        nhan="Hệ nguồn",
        vi_sao="lineage `INV-I05` — `RAW` hay `ADJUSTED`"),
    Cot("source_sheet", "chu",
        nhan="Sheet nguồn",
        vi_sao="lineage `INV-I05` — ten sheet trong tep nguon"),
    Cot("source_row", "so",
        nhan="Dòng nguồn",
        vi_sao="lineage `INV-I05` — so dong trong sheet nguon. ⛔ Khong phai "
               "`itl_id`: hai lan nap cho ra hai `itl_id` khac nhau tren cung "
               "mot dong nguon"),
)

# ⭐⭐ 27 VI TRI CANON LEN LUOI — owner chot 2026-09-03 (*"bang So ITL can du
#    cac truong thong tin"*).
#
# ⛔⛔ **Va no lat mot quyet dinh cu dat tren mot con so CHUA AI DO.**
#    `doc_bao_cao._COT_SO` ghi ly do bo `canon` khoi danh sach: *"36 cot jsonb
#    × 500 dong la mot cau tra ve **vai MB**"*. Do that tren 10.030 dong:
#    trung binh **393 byte/dong**, dong nang nhat **1.970**. ⇒ 500 dong ~
#    **192 KB**, ⛔ **khong phai vai MB** — sai 10–20 lan. Cung lop voi *"52
#    cot"* va *"~64 cot"* ma du an da bat truoc do.
#
# ⚠⚠ **HAI HE TOA DO — cho de nham nhat trong ca tep nay.** Chu cai o day la
#    cua **ITL-CANON** *(khuon DAU VAO, 38 vi tri)*; con `ledge=` o tren la
#    cua **ITL Ledge** *(so DAU RA, 64 cot)*. Vi du `canon S` = *Budget Code
#    (HDCode)* la **o nguon nguyen van**, con `hd` *(ledge V)* la gia tri
#    **Final** — da qua phan loai va co the da co nguoi go tay de len. Hai thu
#    KHAC NHAU, va ke toan can ca hai de doi soat.
#
# ⛔ **⛔ Khong lay 9 vi tri A·B·C·D·E·F·G·L·AG** — chung la chinh cac cot nen
#    da co tren luoi *(`doc_date`, `doc_no`, `memo`, `curr`, `ps_no`, `ps_co`,
#    `acct`, `le_payer`, `le`)*. Lay nua la **hai cot cung mot du lieu**, va
#    ke toan se hoi *"cai nao dung"* — mot cau hoi man hinh tu tao ra.
CANON_LEN_LUOI: tuple[str, ...] = (
    "H", "I", "J", "K", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "AB", "AC", "AD", "AE", "AF", "AH", "AI", "AJ", "AK", "AL",
)

BANG_COT = BANG_COT + tuple(
    # ⛔ `nhan` de TRONG co y: ten den TU `CANON_COLS` qua `nhan_cua`, nen mot
    #    lan BA doi ten trong tu dien du lieu la man doi theo. Go tay o day thi
    #    cong `kiem_bang_cot` bao DO.
    Cot(f"canon_{x}", "chu", canon=x) for x in CANON_LEN_LUOI)


def _ten_ledge() -> dict[str, tuple[str, str]]:
    """`chu cai` → `(ten, truong)` tu `COT_LUU`."""
    return {c.letter: (c.name, c.di_dau) for c in COT_LUU}


def _ten_canon() -> dict[str, str]:
    return {c.letter: c.name for c in CANON_COLS}


def nhan_cua(c: Cot) -> str:
    """Ten hien tren tieu de. ⭐ Suy TU NGUON khi co nguon."""
    if c.ledge:
        return _ten_ledge()[c.ledge][0]
    if c.canon:
        return _ten_canon()[c.canon]
    return c.nhan


def kiem_bang_cot(bang: tuple[Cot, ...] | None = None,
                  truong_cua: tuple[str, ...] | None = None) -> list[str]:
    """⛔ Cong. Rong = dat. ⛔ Khong bao gio tra "OK" — tra danh sach vi pham.

    `truong_cua` = tap truong cua that tra ve *(do o `tests/`, ⛔ khong o day —
    `fls.api` ⛔ khong duoc biet tang kho)*. Truyen vao thi cong doi chieu **hai
    chieu**: ⛔ khong cot nao khai ma cua ⛔ khong tra, ⛔ khong truong nao cua
    tra ma bang ⛔ khong khai.

    ⚠⚠ Chieu thu hai moi la chieu quan trong: neu mai kia cua them mot truong
    ma ⛔ khong ai khai o day, luoi se **giau no trong im lang** — dung cai
    "mac dinh im lang" ma `INV-I16` cam.
    """
    if bang is None:
        bang = BANG_COT
    loi: list[str] = []
    ledge, canon = _ten_ledge(), _ten_canon()

    thay: set[str] = set()
    for c in bang:
        if c.truong in thay:
            loi.append(f"trung cot: {c.truong}")
        thay.add(c.truong)
        if c.kieu not in KIEU_O:
            loi.append(f"{c.truong} kieu {c.kieu!r} chua khai trong KIEU_O")
        if c.ledge and c.canon:
            loi.append(f"{c.truong} khai CA HAI nguon ten (`ledge={c.ledge}` + "
                       f"`canon={c.canon}`) — hai nguon cho mot ten la hai su "
                       f"that; chon mot")
        if c.ledge:
            if c.ledge not in ledge:
                loi.append(f"{c.truong} tro toi Ledge cot {c.ledge!r} — "
                           f"⛔ khong co trong `COT_LUU`")
            else:
                ten, di_dau = ledge[c.ledge]
                # ⭐⭐ Doi chieu CA ten CA day noi: mot cot lay ten cua `V` ma
                # thuc ra cho `cdt1` la mot tieu de dat nham dong.
                if di_dau != c.truong:
                    loi.append(
                        f"{c.truong} lay ten Ledge cot {c.ledge!r}, nhung cot "
                        f"do di vao truong {di_dau!r} — tieu de dat nham cho")
                if c.nhan and c.nhan != ten:
                    loi.append(
                        f"{c.truong} go tay nhan {c.nhan!r} trong khi nguon "
                        f"noi {ten!r} — ⛔ khong go lai ten da co nguon")
        elif c.canon:
            if c.canon not in canon:
                loi.append(f"{c.truong} tro toi canon cot {c.canon!r} — "
                           f"⛔ khong co trong `CANON_COLS`")
            elif c.nhan and c.nhan != canon[c.canon]:
                loi.append(f"{c.truong} go tay nhan {c.nhan!r} trong khi canon "
                           f"noi {canon[c.canon]!r}")
        else:
            # ⛔ ⛔ Khong nguon ⇒ PHAI co ca `nhan` LAN `vi_sao`.
            if not c.nhan:
                loi.append(f"{c.truong} ⛔ khong co nguon ten ma cung ⛔ khong "
                           f"co `nhan` — cot se hien tieu de RONG")
            if not c.vi_sao.strip():
                loi.append(
                    f"{c.truong} dat ten RIENG ma ⛔ khong noi vi sao — mot ten "
                    f"tu bia khong ai giai thich la mot ten se troi")
        if c.go and c.truong not in GO_TREN_LUOI:
            loi.append(f"{c.truong} khai `go=True` ma ⛔ khong nam trong "
                       f"`GO_TREN_LUOI` {GO_TREN_LUOI}")
        if c.khoa not in (0, 1, 2):
            loi.append(f"{c.truong} khoa={c.khoa} — chi 0/1/2")

    thieu_go = [t for t in GO_TREN_LUOI
                if not any(c.truong == t and c.go for c in bang)]
    if thieu_go:
        loi.append(f"truong go duoc ma bang ⛔ khong khai `go=True`: {thieu_go} "
                   f"— o se hien nhu CHI-DOC, va ⛔ khong ai biet no go duoc")
    for so_khoa in (1, 2):
        n = sum(1 for c in bang if c.khoa == so_khoa)
        if n != 1:
            loi.append(f"co {n} cot khai `khoa={so_khoa}` — phai dung 1")
    # Cot dong cung phai nam DAU bang, ⛔ khong thi `left:` cua CSS sai cho.
    if len(bang) >= 2 and [bang[0].khoa, bang[1].khoa] != [1, 2]:
        loi.append("hai cot dong cung phai la hai cot DAU TIEN cua bang — "
                   "CSS neo chung bang `left:0` va `left:var(--khoa-1)`")

    for t, ly_do in KHONG_LEN_LUOI.items():
        if t in thay:
            loi.append(f"{t} vua nam trong `BANG_COT` vua khai `KHONG_LEN_LUOI`"
                       f" — mot truong ⛔ khong the vua len luoi vua khong")
        if not ly_do.strip():
            loi.append(f"{t} khai `KHONG_LEN_LUOI` ma ⛔ khong noi vi sao — "
                       f"mot cho bo quen va mot quyet dinh trong y het nhau")

    if truong_cua is not None:
        cua = set(truong_cua)
        thua = sorted(thay - cua)
        # ⭐ Truong khai `KHONG_LEN_LUOI` la **da duoc khai**, nen no ⛔ khong
        #   tinh la "cua tra ma bang khong biet".
        thieu = sorted(cua - thay - set(KHONG_LEN_LUOI))
        if thua:
            loi.append(f"bang khai cot ma cua ⛔ khong tra: {thua} — luoi se "
                       f"hien cot RONG suot doi")
        if thieu:
            loi.append(f"cua tra truong ma bang ⛔ khong khai: {thieu} — luoi "
                       f"se GIAU chung trong im lang (`INV-I16`)")
    return loi


def than_js() -> bytes:
    """Sinh `cot.js` — ⭐ **cho** cua bang cot, ⛔ khong phai noi khai ra no.

    ⛔ NO neu bang vi pham: mot man hinh nhan bang cot hong se ve mot luoi
    thieu cot **ma trong nhu day du**.
    """
    loi = kiem_bang_cot()
    if loi:
        raise RuntimeError("⛔ bang cot vi pham:\n  - " + "\n  - ".join(loi))
    cot = [{"truong": c.truong, "nhan": nhan_cua(c), "kieu": c.kieu,
            # ⭐ `van` = o nay la van xuoi ⇒ man dat chu `sans`. Moi o
            # khac dat chu may. Xem ban khai `VAN_XUOI` phia tren.
            "van": nhan_cua(c) in VAN_XUOI,
            # ⭐ Chu cai canon di THEO cot ra man hinh. ⛔ Thieu no thi **bon**
            # tieu de `AH..AK` giong het nhau *("MID I DoubleCheck LE")* va
            # `W/X` trung `AB/AC` ⇒ ke toan ⛔ khong biet cot nao la cot nao.
            "canon": c.canon,
            "go": c.go, "khoa": c.khoa,
            "nguon": (f"ITL Ledge · {c.ledge}" if c.ledge
                      else f"canon · {c.canon}" if c.canon
                      else "FLS"),
            "vi_sao": c.vi_sao}
           for c in BANG_COT]
    # ⭐ 38 vi tri canon cho **drawer** — bam mot dong thi xem duoc nguyen van
    # khuon dau vao. ⚠ Bon cot `AH..AK` TRUNG TEN nhau va `W/X` trung `AB/AC`
    # ⇒ drawer PHAI hien **chu cai** ben canh ten, ⛔ khong thi hai o giong het
    # nhau va ⛔ khong ai biet o nao la o nao (`fls/canon/spec.py` khuyet tat 1).
    canon = [{"letter": c.letter, "nhan": c.name, "nhom": c.group,
              "van": c.name in VAN_XUOI}
             for c in CANON_COLS]
    return ("// ⛔ SINH TU `fls/api/cot_so.py` luc chay — ⛔ khong go tay tep\n"
            "// nay. Ten cot den tu `oracle/ledge_spec.COT_LUU` va\n"
            "// `canon/spec.CANON_COLS`; cong `kiem_bang_cot` canh hai chieu.\n"
            "window.FLS_COT = " + json.dumps(cot, ensure_ascii=False) + ";\n"
            "window.FLS_CANON = " + json.dumps(canon, ensure_ascii=False)
            + ";\n"
            "window.FLS_GO_DRAWER = "
            + json.dumps(list(GO_O_DRAWER), ensure_ascii=False) + ";\n"
            ).encode("utf-8")
