"""⛔⛔ CONG QUET MA NGUON: chi MOT file duoc ghi thao tac cua nguoi.

Sau khi `QĐ-ITL-16` bo buoc duyet va `QĐ-ITL-27` khai tu vai nguoi hau kiem,
**nhat ky la lop kiem soat duy nhat con lai**. Mot duong ghi khong sinh nhat ky
⛔ khong phai *"thieu mot tinh nang"* — no la **mot lo trong lop kiem soat cuoi
cung**.

★ Cung ho voi bai da co: *"luat o-loi tung co BON ban sao"*. Cach chua ⛔ khong
phai sua tung ban sao ma la **lam cho ban sao moi khong the ton tai**.

⚠ Quet bang `ast` chu ⛔ khong bang `in`: docstring cua chinh file nay nhac ten
cac bang, va mot cong bao dong vi doc chinh ghi chu cua no la cong sap bi go ra.
"""
from __future__ import annotations

import ast
import pathlib

# ⭐ `fls_pm_unlink` (them 2026-08-28) vao day chu ⛔ KHONG vao
# `PM_LINK_HAI_CHO`: no ⛔ khong co duong ghi tu bo nap — **may ⛔ khong bao gio
# tu bo mot moi noi**. Bo moi noi la mot quyet dinh cua NGUOI (`QĐ-ITL-69`), nen
# dung MOT cho ghi, va mot file thu hai ghi vao no la mot duong go moi noi
# ⛔ khong qua nhat ky.
BANG_CHI_MOT_CHO: frozenset[str] = frozenset({
    "fls_adjustment", "fls_journal", "fls_queue_event", "fls_pm_unlink"})
CHO_DUY_NHAT = "ghi_tay.py"

# ⛔⛔ `fls_pm_link` la mot ca RIENG, va no phai duoc khai rieng chu ⛔ khong nhet
# vao `BANG_CHI_MOT_CHO`. Ly do: bang nay co **HAI** duong ghi hop phap, va chung
# khac ban chat:
#   · `chay_nap.py`  — MAY ghep luc nap (hinh `A`/`B`/`C`, cong Σ tu dong)
#   · `ghi_tay.py`   — NGUOI ghep tay o man `F01` (hinh `T`, `QĐ-ITL-48`)
# Nhet vao danh sach mot-cho thi bai se do o `chay_nap.py`, va cach "chua" de nhat
# la go cong ra. ⇒ khai HAI file, va van chan file thu BA.
PM_LINK_HAI_CHO: frozenset[str] = frozenset({"chay_nap.py", "ghi_tay.py"})
GOC = pathlib.Path(__file__).resolve().parents[2] / "fls"


def _cau_sql(cay: ast.AST) -> list[tuple[int, str]]:
    """Moi HANG CHUOI trong ma nguon, kem so dong. ⛔ Khong doc ghi chu.

    Bat ca chuoi noi bang `+` va f-string, vi mot cau `INSERT` ghep tu hai manh
    la cach de nhat de di qua mot phep quet.
    """
    ra: list[tuple[int, str]] = []
    for n in ast.walk(cay):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            ra.append((n.lineno, n.value))
        elif isinstance(n, ast.JoinedStr):
            ghep = "".join(v.value for v in n.values
                           if isinstance(v, ast.Constant)
                           and isinstance(v.value, str))
            ra.append((n.lineno, ghep))
    return ra


# ⛔⛔ Phep khop phai bat dau bang DONG TU SQL, ⛔ khong phai "co chua".
#
# Ban dau toi viet `"update " in t` — va bai `test_ghi_tay_KHONG_ghi_vao_so`
# **do ngay**, vi chinh docstring cua `dao_but_toan` co cau *"⛔ KHONG `UPDATE
# state` cua dong cu"*. Tuc la cong bao dong vi doc dung cai ghi chu noi rang
# viec do bi cam. Mot cong bao dong nhu the thi nguoi ta go cong chu khong sua ma.
_DONG_TU = ("insert into", "update", "delete from")


def _cau(s: str) -> str:
    return " ".join(s.lower().split())


def _la_ghi(s: str, bang: str) -> bool:
    c = _cau(s)
    return any(c.startswith(f"{tu} {bang}") for tu in _DONG_TU)


def _la_sua_hay_xoa(s: str) -> bool:
    c = _cau(s)
    return c.startswith("update ") or c.startswith("delete from")


def test_chi_ghi_tay_duoc_ghi_vao_ba_bang_mang_vet():
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name == CHO_DUY_NHAT:
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            for bang in BANG_CHI_MOT_CHO:
                if _la_ghi(s, bang):
                    xau.append(f"{f.relative_to(GOC)}:{dong} ghi vao {bang}")
    assert xau == [], (
        "chi `fls/repo/ghi_tay.py` duoc ghi vao " + str(sorted(BANG_CHI_MOT_CHO))
        + " — de lop kiem soat cuoi cung khong co lo: " + " · ".join(xau))


def test_ghi_tay_that_su_co_ghi_vao_ba_bang_do():
    """⛔ Cong chung #7: chung minh phep quet DA DO DUOC GI.

    Neu ⓐ cong chi kiem *"khong ai khac ghi"* va ⓑ ban than `ghi_tay.py` cung
    khong ghi, thi cong xanh ma **khong co gi duoc bao ve** — dung cai bay
    *"khong do gi thi tat nhien khong thay loi"*.
    """
    f = GOC / "repo" / CHO_DUY_NHAT
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    thay = {b for _d, s in _cau_sql(cay) for b in BANG_CHI_MOT_CHO
            if _la_ghi(s, b)}
    assert thay == BANG_CHI_MOT_CHO, f"ghi_tay.py chi ghi vao {sorted(thay)}"


def test_fls_pm_link_chi_duoc_ghi_o_HAI_cho_da_khai():
    """⛔ Moi noi lenh chi chi sinh ra o HAI cho: bo nap (may) va cua ghi (nguoi).

    Mot cho thu ba ghi vao bang nay nghia la co moi noi **khong qua cong Σ** —
    va bat bien `Σ moi noi = tien dong bank` la thu duy nhat lam bang noi nay
    dang tin.
    """
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name in PM_LINK_HAI_CHO:
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            if _la_ghi(s, "fls_pm_link"):
                xau.append(f"{f.relative_to(GOC)}:{dong}")
    assert xau == [], (
        "chi " + str(sorted(PM_LINK_HAI_CHO)) + " duoc ghi vao `fls_pm_link`: "
        + " · ".join(xau))


def test_CA_HAI_cho_do_that_su_co_ghi_vao_fls_pm_link():
    """⛔ Cong chung #7: neu ca hai file deu KHONG ghi thi bai tren xanh ma
    ⛔ khong bao ve gi. Doi tung file phai THAT SU co cau ghi."""
    thieu = []
    for ten in sorted(PM_LINK_HAI_CHO):
        f = GOC / "repo" / ten
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        if not any(_la_ghi(s, "fls_pm_link") for _d, s in _cau_sql(cay)):
            thieu.append(ten)
    assert thieu == [], f"khai la cho ghi ma ⛔ khong ghi: {thieu}"


def test_ghi_tay_KHONG_ghi_vao_so_va_KHONG_sua_but_toan_cu():
    """⛔ `INV-I08`: ⛔ khong `UPDATE`/`DELETE` o BAT KY dau trong tang ghi —
    ke ca len `fls_adjustment`. Dao la **them mot dong**."""
    f = GOC / "repo" / CHO_DUY_NHAT
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = []
    for dong, s in _cau_sql(cay):
        if _la_sua_hay_xoa(s):
            xau.append(f"{dong}: {s[:70]}")
        if _cau(s).startswith("insert into fls_itl"):
            xau.append(f"{dong}: ghi vao SO — {s[:70]}")
    assert xau == [], "tang ghi co cau sua/xoa: " + " · ".join(xau)
