"""⛔ CONG: **ban khai cua bang tuyen** vs **SQL that**. `GAP-API-05`.

  python tools/soi_bang_tuyen.py            # bang doc cho nguoi
  python tools/soi_bang_tuyen.py --json     # de dan vao cong cu khac

⛔⛔ **Vi sao cong nay ton tai — va vi sao no la loai nguy nhat.**

`fls/api/bang_tuyen.py` co san mot cong (`kiem_bang_tuyen`) va no la **cong lon
nhat cua `P4`**: no chan *"⛔ khong duong nao ghi vao `fls_itl`"* (`INV-I08`) va
*"⛔ khong duong nao cham bang ngoai `fls_*`"* (`QĐ-ITL-45`). Nhung no do tren
**BAN KHAI** — cai truong `Tuyen.bang` do **NGUOI GO**. Cau SQL that nam o mot
**tep khac** (`fls/repo/*.py`), va ⛔ **khong gi noi hai cho lai**.

⇒ Ngay `03/09` mot agent kiem doc lap bat duoc: **4 tuyen khai thieu bang**.
  `GET /gates` khai `fls_itl · fls_pm_link · fls_run · fls_reject` trong khi
  `doc_cong` con doc `fls_moi_noi`. Cong van **XANH**.

★★ **Do la "cong xanh vi ⛔ khong do dung thu can do"** — dung luat so mot cua
du an. Va no ⛔ khong the tu lo ra: ban khai va SQL o hai tep, ⛔ khong ai mo hai
tep canh nhau.

⛔⛔ **Va cong nay bat duoc mot thu ma cong cu ⛔ KHONG THE:** mot cau
`INSERT INTO fls_itl` **that** nam trong duong goi cua mot tuyen. Cong cu chi
doc duoc `Tuyen.bang_ghi` — mot dong khai. Neu ai do viet cau `INSERT` do ma
quen sua dong khai thi cong cu **im**, va `INV-I08` *(so la append-only)* bi pha
trong im lang.

── CACH DO ──────────────────────────────────────────────────────────────────
⛔ **Doc TINH, ⛔ khong chay.** Do bang cach chay *(bat `cursor.execute`)* chi
phu nhung duong ma bo test di qua — mot duong ⛔ khong co test se **im lang lot
qua**, tuc lai la mot cong xanh gia nua, chi tinh vi hon.

  ⓐ Tu ten ham cua tuyen → ham trong `fls/api/xu_ly.py`
  ⓑ Bam theo **do thi goi** sang `fls/repo/*` (va bat cu module `fls.*` nao)
  ⓒ Trong moi ham cham toi: gom **moi chuoi** *(⛔ tru docstring)*, **bo chu
    thich SQL** *(`-- …`)*, roi tim `fls_\\w+`
  ⓓ So voi `Tuyen.bang` / `Tuyen.bang_ghi`

⚠ **Phep do nay VUOT** *(over-approximate)*: no gom ca bang chi cham o nhanh
loi. Do la **co y** — khai du hon la khai thieu, vi ban khai la mot **ban do**,
va mot ban do ve thieu duong thi nguy hon mot ban do ve thua.

⚠⚠ **Ba cho phep do nay ⛔ KHONG voi toi**, khai thang chu ⛔ khong lam tron:
  · SQL dung **ten bang ghep tu bien** *(⛔ khong co trong kho nay — da soi)*
  · ham **long trong ham** hay **phuong thuc cua lop** *(chi bam ham muc module)*
  · SQL nam trong **khung xem** — mot khung xem doc bang khac thi phep do nay
    thay khung xem, ⛔ khong thay bang duoi no. Do la **dung**: tuyen cham khung
    xem, ⛔ khong cham bang duoi.
"""
from __future__ import annotations

import ast
import functools
import json
import os
import re
import sys
from dataclasses import dataclass, field

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, GOC)

from fls.api import bang_tuyen                                   # noqa: E402
from fls.api.xu_ly import HAM                                    # noqa: E402

# ⛔ Ban TRANG: chi bam vao cac goi nay. Mot `import` ra ngoai `fls` ⇒ dung.
GOC_GOI = "fls"

BANG = re.compile(r"\bfls_[a-z0-9_]+\b")
CHU_THICH_SQL = re.compile(r"--[^\n]*")
GHI = re.compile(
    r"\bINSERT\s+INTO\s+(fls_[a-z0-9_]+)"
    r"|\bUPDATE\s+(fls_[a-z0-9_]+)"
    r"|\bDELETE\s+FROM\s+(fls_[a-z0-9_]+)", re.I)


# ── doc mot module thanh cay ──────────────────────────────────────────────
@dataclass
class Module:
    ten: str
    cay: ast.Module
    ham: dict[str, ast.FunctionDef] = field(default_factory=dict)
    hang: dict[str, str] = field(default_factory=dict)   # ten -> chuoi
    biet_danh: dict[str, str] = field(default_factory=dict)  # bd -> module
    tu_module: dict[str, str] = field(default_factory=dict)  # ten -> module


def _duong_module(ten: str) -> str | None:
    d = os.path.join(GOC, *ten.split(".")) + ".py"
    return d if os.path.isfile(d) else None


def _chuoi_cua(nut: ast.AST, hang: dict[str, str]) -> str:
    """Gia tri chuoi cua mot bieu thuc, neu suy duoc. ⛔ Khong suy duoc ⇒ ''."""
    if isinstance(nut, ast.Constant) and isinstance(nut.value, str):
        return nut.value
    if isinstance(nut, ast.Name):
        return hang.get(nut.id, "")
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):
        return _chuoi_cua(nut.left, hang) + _chuoi_cua(nut.right, hang)
    if isinstance(nut, ast.JoinedStr):          # f-string: lay phan chu that
        return "".join(_chuoi_cua(p, hang) for p in nut.values)
    if isinstance(nut, ast.FormattedValue):
        return " "                              # cho troc di, ⛔ khong doan
    return ""


@functools.lru_cache(maxsize=64)
def doc_module(ten: str) -> Module | None:
    d = _duong_module(ten)
    if d is None:
        return None
    with open(d, encoding="utf-8") as f:
        cay = ast.parse(f.read(), filename=d)
    m = Module(ten=ten, cay=cay)
    for n in cay.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            m.ham[n.name] = n
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            if n.module == GOC_GOI or n.module.startswith(GOC_GOI + "."):
                for a in n.names:
                    con = f"{n.module}.{a.name}"
                    if _duong_module(con):       # `from fls.repo import x as y`
                        m.biet_danh[a.asname or a.name] = con
                    else:                        # `from fls.x import ham`
                        m.tu_module[a.asname or a.name] = n.module
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name.startswith(GOC_GOI + "."):
                    m.biet_danh[a.asname or a.name] = a.name
    # Hang chuoi muc module — giai theo dung thu tu khai bao (cho phep
    # `_SQL = _CTE + "..."`).
    for n in cay.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            v = _chuoi_cua(n.value, m.hang)
            if v:
                m.hang[n.targets[0].id] = v
    return m


# ── bam theo do thi goi ───────────────────────────────────────────────────
def _goi_trong(ham: ast.FunctionDef, m: Module) -> set[tuple[str, str]]:
    """Cac `(module, ten_ham)` ma `ham` goi toi — trong pham vi `fls`."""
    ra: set[tuple[str, str]] = set()
    for n in ast.walk(ham):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            mod = m.biet_danh.get(f.value.id)
            if mod:
                ra.add((mod, f.attr))
        elif isinstance(f, ast.Name):
            if f.id in m.ham:
                ra.add((m.ten, f.id))
            elif f.id in m.tu_module:
                ra.add((m.tu_module[f.id], f.id))
    return ra


def _chuoi_trong(ham: ast.FunctionDef, m: Module) -> list[str]:
    """Moi chuoi trong than ham — ⛔ TRU docstring va cac chuoi tro tren."""
    ra: list[str] = []
    bo: set[int] = set()
    # ⛔ Docstring cua chinh ham + cua moi khoi long ben trong: chung la VAN,
    # ⛔ khong phai SQL, va chung **co nhac ten bang** (vi du chu thich
    # *"`fls_moi_noi`, ⛔ KHONG `fls_pm_link`"*) ⇒ khong bo thi cong bao do GIA.
    for n in ast.walk(ham):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) \
                and isinstance(n.value.value, str):
            bo.add(id(n.value))
    for n in ast.walk(ham):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                and id(n) not in bo:
            ra.append(n.value)
        elif isinstance(n, ast.Name) and n.id in m.hang:
            ra.append(m.hang[n.id])
    return ra


def sql_cua_tuyen(ten_ham: str) -> tuple[set[str], set[str], list[str]]:
    """`(bang cham, bang GHI, duong da bam)` cho mot ham xu ly."""
    dau = ("fls.api.xu_ly", ten_ham)
    da: set[tuple[str, str]] = set()
    hang_doi = [dau]
    cham: set[str] = set()
    ghi: set[str] = set()
    vet: list[str] = []
    while hang_doi:
        khoa = hang_doi.pop()
        if khoa in da:
            continue
        da.add(khoa)
        ten_m, ten_h = khoa
        m = doc_module(ten_m)
        if m is None or ten_h not in m.ham:
            continue
        vet.append(f"{ten_m}.{ten_h}")
        h = m.ham[ten_h]
        for s in _chuoi_trong(h, m):
            sach = CHU_THICH_SQL.sub(" ", s)
            cham |= set(BANG.findall(sach))
            for g in GHI.finditer(sach):
                ghi.add(next(x for x in g.groups() if x))
        hang_doi += list(_goi_trong(h, m))
    return cham, ghi, sorted(vet)


# ── cong ──────────────────────────────────────────────────────────────────
def soi(bang: tuple = (), do_sql=None) -> tuple[list[str], list[dict]]:
    """⛔ Rong = dat. Tra `(vi pham, bang do)`.

    ⚠ `do_sql` cho phep **bom mot phep do gia** — de bo test chung minh duoc
    nhanh *"co cau `INSERT INTO fls_itl` that"* co DO hay khong. ⛔ Khong co no
    thi nhanh ay ⛔ khong bao gio chay duoc, va mot nhanh chua tung chay la mot
    nhanh chua biet co song.
    """
    bang = bang or bang_tuyen.BANG_TUYEN
    do_sql = do_sql or sql_cua_tuyen
    loi: list[str] = []
    do: list[dict] = []
    for t in bang:
        if t.ham not in HAM:
            loi.append(f"{t.duong}: ⛔ khong co ham `{t.ham}`")
            continue
        cham, ghi, vet = do_sql(t.ham)
        khai = set(t.bang)
        khai_ghi = set(t.bang_ghi)

        thieu = sorted(cham - khai)
        thua = sorted(khai - cham)
        thieu_ghi = sorted(ghi - khai_ghi)

        do.append({"duong": t.duong, "ham": t.ham,
                   "khai": sorted(khai), "that": sorted(cham),
                   "khai_ghi": sorted(khai_ghi), "that_ghi": sorted(ghi),
                   "thieu": thieu, "thua": thua, "vet": vet})

        # ⓐ ⛔⛔ Cai chinh: SQL cham mot bang ma ban khai ⛔ khong noi.
        if thieu:
            loi.append(
                f"{t.phuong_thuc} {t.duong}: SQL cham {thieu} ma `bang` ⛔ "
                f"khong khai — cong `kiem_bang_tuyen` dang canh mot ban do CU")
        # ⓑ ⛔⛔ Va cai cong cu ⛔ KHONG THE thay: mot cau ghi THAT vao so.
        if "fls_itl" in ghi:
            loi.append(
                f"{t.phuong_thuc} {t.duong}: co cau SQL **GHI THAT** vao "
                f"`fls_itl` — `INV-I08` cam. Ban khai ⛔ khong cuu duoc dieu nay")
        # ⓒ Ghi that ma ⛔ khong khai ⇒ mot phep ghi ⛔ khong ai canh.
        if thieu_ghi:
            loi.append(
                f"{t.phuong_thuc} {t.duong}: SQL GHI vao {thieu_ghi} ma "
                f"`bang_ghi` ⛔ khong khai")
        # ⓓ Khai thua: ban do ve mot duong ⛔ khong co that.
        if thua:
            loi.append(
                f"{t.phuong_thuc} {t.duong}: `bang` khai {thua} ma SQL ⛔ "
                f"khong cham — ban do ve mot duong ⛔ khong co")
    return loi, do


def main() -> int:
    loi, do = soi()
    if "--json" in sys.argv:
        print(json.dumps({"loi": loi, "do": do}, ensure_ascii=False, indent=2))
        return 1 if loi else 0

    print(f"soi {len(do)} tuyen · ban khai `Tuyen.bang` vs SQL that\n")
    for d in do:
        co = "⛔" if (d["thieu"] or d["thua"]) else "OK"
        print(f"{co} {d['duong']}")
        if d["thieu"]:
            print(f"     THIEU: {d['thieu']}")
        if d["thua"]:
            print(f"     THUA : {d['thua']}")
    if loi:
        print(f"\n⛔ BAN KHAI LECH SQL — {len(loi)} vi pham:")
        for x in loi:
            print(f"  - {x}")
        return 1
    print("\n✅ ban khai KHOP SQL that o ca " + str(len(do)) + " tuyen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
