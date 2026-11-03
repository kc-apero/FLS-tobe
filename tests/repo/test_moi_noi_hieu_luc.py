"""⛔⛔ CONG QUET MA NGUON: cau hoi *"dong nay dang noi voi dong lenh nao"*
chi duoc tra loi tu khung xem `fls_moi_noi`.

★★ **Vi sao co cong nay.** Tu migration `0013` (`QĐ-ITL-69`), `fls_pm_link` giu
**CA LICH SU** moi lan ghep — ke ca cac moi noi **da bi bo**. Nghia la moi cau
`SELECT ... FROM fls_pm_link` viet sau 2026-08-28 se **im lang tra ve ca nhung
moi noi da go**:

  · man `F01` se hien mot dong lenh vua duoc go la *"da ghep"* ⇒ ke toan
    ⛔ khong ghep lai duoc, va ⛔ khong co loi nao bao
  · cong `SIGMA_MOI_NOI` se do mot dong da go het moi noi va bao **DAT** —
    mot cai **xanh GIA**
  · `ghep_lenh` se tu choi ghep lai voi ly do *"dong nay DA ghep"*

⛔ Ba lo tren ⛔ khong lo nao lam chuong trinh do. Do la ly do phai co mot cong
QUET MA NGUON chu ⛔ khong chi mot bai chay thu: mot cau `SELECT` moi viet o file
thu ba se lot qua moi bai chay thu hien co.

⚠ Cong nay ⛔ KHONG cam doc `fls_pm_link` — no doi **khai ra**. Doc lich su la
viec that (dem `lan`, hien *"da ghep lai 2 lan"*), nen moi cho doc phai co mot
dong o `DOC_LICH_SU` noi **vi sao can LICH SU chu khong phai HIEU LUC**.
"""
from __future__ import annotations

import ast
import pathlib

GOC = pathlib.Path(__file__).resolve().parents[2] / "fls"

# Cho duoc DOC `fls_pm_link` (bang GOC = lich su), kem SO CAU va LY DO.
#
# ⛔ Them mot cau doc bang goc ma ⛔ khong khai o day = cong DO. Va thong bao noi
# thang: neu can *"dang noi voi gi"* thi doc `fls_moi_noi`, ⛔ khong phai sua so
# o day cho het do.
DOC_LICH_SU: dict[str, tuple[int, str]] = {
    "repo/ghi_tay.py": (
        1, "`_lan_ke_tiep` PHAI dem ca lich su: mot moi noi da bo van chiem "
           "`lan` cua no, dem tren khung xem se sinh lai `lan=1` va TRUNG KHOA"),
    "repo/doc_bao_cao.py": (
        1, "lich su BO moi noi — join de hien *'dong nay da ghep lai 2 lan'*; "
           "day dung la cho can LICH SU"),
    # ⭐ Cho nay KHAC ba cho duoi: no ⛔ khong "doc" gi ca — no la **dinh nghia
    #   cua chinh khung xem**. Bat buoc phai co, va phai la cho DUY NHAT loc
    #   lich su thanh hieu luc. Neu mot ngay bai nay bao `schema.py` co HAI cau
    #   thi co nghia da co khung xem thu hai, tuc hai ban su that.
    "db/schema.py": (
        1, "ban khai khung xem `fls_moi_noi` — cho DUY NHAT loc LICH SU "
           "(`fls_pm_link`) thanh HIEU LUC; day la dinh nghia, ⛔ khong phai "
           "mot cho doc thu hai"),
    "repo/chay_nap.py": (
        1, "bo nap dem lai chinh so moi noi no vua chen trong lan nap do "
           "(`run_id`), ⛔ khong phai tra loi 'dang noi voi gi'"),
}


def _chuoi(cay: ast.AST) -> list[tuple[int, str]]:
    ra: list[tuple[int, str]] = []
    for n in ast.walk(cay):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            ra.append((n.lineno, n.value))
        elif isinstance(n, ast.JoinedStr):
            ra.append((n.lineno, "".join(
                v.value for v in n.values
                if isinstance(v, ast.Constant) and isinstance(v.value, str))))
    return ra


def _la_doc(s: str) -> bool:
    """Mot cau DOC bang goc: co `fls_pm_link` va ⛔ khong phai cau `INSERT`.

    ⚠ Khop tren DONG TU, ⛔ khong tren *"co chua"* — cung bai hoc voi
    `test_chi_mot_cho_ghi_tay.py`: chinh ghi chu cua file nhac ten bang, va mot
    cong bao dong vi doc ghi chu cua no la cong sap bi go ra.
    """
    t = " ".join(s.lower().split())
    if "fls_pm_link" not in t:
        return False
    if t.startswith("insert into fls_pm_link"):
        return False
    # ⚠⚠ PHAI co dong tu doc NGAY TRUOC ten bang, ⛔ khong phai *"co chua"*.
    # Ban dau toi viet `"fls_pm_link" in t` va bai do ngay o 10 cho: `schema.py`
    # (ban khai bang) va `api/bang_tuyen.py` (danh sach ten bang duoc phep) —
    # hai cho ⛔ khong doc mot dong du lieu nao. Mot cong do o nhung cho nhu the
    # la cong se bi go ra, ⛔ khong phai cong se duoc sua.
    #
    # ⚠ Cho MU da biet va CHAP NHAN: mot cau bi cat thanh hai manh chuoi ngay
    #   giua `FROM` va ten bang ("... FROM " "fls_pm_link l ...") se lot qua
    #   phep quet nay. Manh BAT DAU bang ten bang KEM alias thi bat duoc; con
    #   khai bao ten tran ("fls_pm_link") thi ⛔ khong tinh. Phep quet chuoi
    #   ⛔ khong bit han duoc, nen lop chan CHINH la cac bai chay that o
    #   `test_bo_moi_noi_pg.py`, va bai nay chi la lop THU HAI.
    return ("from fls_pm_link" in t or "join fls_pm_link" in t
            or t.startswith("fls_pm_link "))


def _dem_theo_file() -> dict[str, list[int]]:
    ra: dict[str, list[int]] = {}
    for f in sorted(GOC.rglob("*.py")):
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        dong = [d for d, s in _chuoi(cay) if _la_doc(s)]
        if dong:
            ra[f.relative_to(GOC).as_posix()] = dong
    return ra


def test_moi_cho_DOC_bang_goc_deu_duoc_KHAI_kem_LY_DO():
    thay = _dem_theo_file()
    chua_khai = {k: v for k, v in thay.items() if k not in DOC_LICH_SU}
    assert not chua_khai, (
        "⛔⛔ cau doc `fls_pm_link` CHUA KHAI: "
        + " · ".join(f"{k}:{v}" for k, v in chua_khai.items())
        + ". Neu can *'dong nay DANG noi voi dong lenh nao'* thi doc khung xem "
          "`fls_moi_noi` — bang goc co ca moi noi DA BO (`QĐ-ITL-69`). Neu that "
          "su can LICH SU thi khai vao `DOC_LICH_SU` kem ly do.")


def test_SO_CAU_doc_bang_goc_dung_nhu_khai():
    """⛔ Khai mot cau ma viet ba cau thi hai cau kia ⛔ khong ai doc lai."""
    thay = _dem_theo_file()
    lech = {k: (len(thay.get(k, [])), n) for k, (n, _l) in DOC_LICH_SU.items()
            if len(thay.get(k, [])) != n}
    assert not lech, (
        "⛔ so cau doc bang goc lech voi ban khai (thay, khai): "
        + " · ".join(f"{k}={v}" for k, v in lech.items()))


def test_MOI_ban_khai_phai_noi_VI_SAO_can_LICH_SU():
    """⛔ Khai ma khong noi vi sao thi la mot cai the thong hanh, ⛔ khong phai
    mot ly do — va nguoi sau se them ten file vao day de cong het do."""
    for k, (_n, ly_do) in DOC_LICH_SU.items():
        assert len(ly_do) > 50, f"{k}: ly do qua ngan de ai doc cung hieu"
        assert any(x in ly_do.lower() for x in ("lich su", "lan", "run_id")), (
            f"{k}: ly do phai noi ro vi sao can LICH SU chu khong phai HIEU LUC")


def test_CUA_GHI_va_CUA_DOC_that_su_dung_khung_xem():
    """⛔ Cong chung #7: neu ⛔ khong file nao dung `fls_moi_noi` thi ba bai tren
    xanh ma khung xem ⛔ khong duoc dung o dau — *"khong do gi thi tat nhien
    khong thay loi"*."""
    dung: dict[str, int] = {}
    for f in sorted(GOC.rglob("*.py")):
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        n = sum(1 for _d, s in _chuoi(cay) if "fls_moi_noi" in s.lower())
        if n:
            dung[f.relative_to(GOC).as_posix()] = n
    assert "repo/ghi_tay.py" in dung, "cua GHI ⛔ khong doc khung xem hieu luc"
    assert "repo/doc_bao_cao.py" in dung, "cua DOC ⛔ khong doc khung xem hieu luc"
