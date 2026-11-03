"""⛔ Cong: ⛔ KHONG mot ma mau nao go tay ngoai `tokens.css`.

`DEV-12` §3 (bang buoc 1): *"⛔ Khong mot ma mau nao go tay trong code man
hinh"*. `BA-06` §7: ve mot he thi giac thu hai la tao **hai ban su that ve mau
va khoang cach** — dung cai benh ca bo tai lieu nay chua o tang so lieu.

⛔⛔ **Cong nay bat mot thu ma mat nguoi ⛔ khong bat duoc.** Mot `#f3cdcd` go
them vao mot tep CSS **trong y het** `var(--crit-line)` tren man hinh — cho den
ngay ai do doi token, va mot cho doi con cho kia thi ⛔ khong.
"""
from __future__ import annotations

import os
import re

import pytest

from fls.web import phuc_vu as pv

# `#abc` · `#aabbcc` · `#aabbccdd` · `rgb(` · `rgba(` · `hsl(` · `hsla(`
MA_MAU = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\s*\(")

# ⛔ Ngoai le DUY NHAT. Ban TRANG — them mot ten vao day la mo them mot ban su
# that ve mau, nen no phai la mot quyet dinh co nguoi ky.
DUOC_CO_MAU: frozenset[str] = frozenset({"tokens.css"})


def _tep_can_quet() -> list[str]:
    return sorted(
        n for n in os.listdir(pv.THU_MUC)
        if os.path.isfile(os.path.join(pv.THU_MUC, n))
        and n not in DUOC_CO_MAU)


# ⚠⚠ **Cong phai bo qua GHI CHU.** Lan chay dau tien no bao do — va ca hai
# bao dong deu la **cau van ta chinh no** *(dong "NO neu thay `#rrggbb`/`rgb(`")*.
# Mot cong keu vi mot dong ghi chu la mot cong nguoi ta se go ra, ⛔ khong phai
# mot cong nguoi ta se nghe.
GHI_CHU = re.compile(r"/\*.*?\*/|^\s*//.*?$|<!--.*?-->", re.S | re.M)


def _bo_ghi_chu(chu: str) -> str:
    # Giu so DONG y nguyen de toa do bao loi con dung.
    return GHI_CHU.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), chu)


def _quet(chu: str) -> list[str]:
    ra = []
    for i, dong in enumerate(_bo_ghi_chu(chu).splitlines(), 1):
        for m in MA_MAU.finditer(dong):
            ra.append(f"dong {i}: {m.group(0)}  |  {dong.strip()[:70]}")
    return ra


@pytest.mark.parametrize("ten", _tep_can_quet())
def test_khong_ma_mau_go_tay(ten):
    with open(os.path.join(pv.THU_MUC, ten), encoding="utf-8") as f:
        thay = _quet(f.read())
    assert thay == [], (
        f"⛔ {ten} co ma mau go tay. Mau chi duoc song o `tokens.css` "
        f"(`BA-06` §7). Thay:\n  " + "\n  ".join(thay))


def test_tokens_css_that_su_CO_mau():
    """⛔ Neu `tokens.css` rong thi cong tren xanh **vi ⛔ khong co gi**."""
    with open(os.path.join(pv.THU_MUC, "tokens.css"), encoding="utf-8") as f:
        thay = _quet(f.read())
    assert len(thay) >= 25, "tokens.css phai la cho CHUA mau, ⛔ khong phai rong"


# ── ⛔⛔ PHA CO CHU DICH: cong phai DO ─────────────────────────────────────
@pytest.mark.parametrize("bay", [
    "td.x{color:#c73a3a}",
    "td.x{color:#fff}",
    ".y{background:rgb(12,34,56)}",
    ".y{background:rgba(20,32,30,.45)}",
    ".z{border-color:hsl(180 40% 50%)}",
    "const mau = '#0e7570';",
])
def test_cong_DO_khi_co_ma_mau(bay):
    assert _quet(bay) != [], f"cong ⛔ khong bat duoc {bay!r}"


@pytest.mark.parametrize("khong_phai_mau", [
    "/* mau la #c73a3a — day la ghi chu */",
    "// dung rgb( o day",
    "<!-- #fff trong ghi chu HTML -->",
    "// #1 quan trong nhat",          # ⚠ `#1` — mot chu so, ⛔ khong phai mau
    "border-radius:var(--bo)",
    ".card{background:var(--surface)}",
])
def test_cong_KHONG_bao_dong_gia(khong_phai_mau):
    assert _quet(khong_phai_mau) == [], (
        f"⛔ bao dong gia voi {khong_phai_mau!r} — mot cong keu sai la mot cong "
        f"se bi go ra")


# ── ⭐⭐ MA PHAN TU ⛔ KHONG DUOC DOC NHAM THANH MAU ────────────────────────
#
# ⛔⛔ Lan chay dau, cong bao do o `#f03` — **ma cua mot the**, ⛔ khong phai mau.
# Va no dung ky thuat: `#f03` la mot ma mau ba chu so hop le *(do)*. Hai thu
# trung hinh nhau thi cong phai **doan**, va mot cong phai doan la mot cong se
# sai. ⇒ Chua bang cach **doi ten the** cho no ⛔ khong bao giờ doc duoc thanh
# mau, chu ⛔ khong bang cach day cong doan gioi hon.
MA_THE = re.compile(r"""\bid=["']([^"']+)["']|getElementById\(['"]([^'"]+)""")


def test_khong_ma_the_nao_doc_duoc_thanh_mau():
    xau: list[str] = []
    for ten in _tep_can_quet():
        with open(os.path.join(pv.THU_MUC, ten), encoding="utf-8") as f:
            for m in MA_THE.finditer(_bo_ghi_chu(f.read())):
                ma = m.group(1) or m.group(2)
                if MA_MAU.match("#" + ma):
                    xau.append(f"{ten}: id={ma!r}")
    assert xau == [], (
        "⛔ ma the doc duoc thanh mau — dat ten khac (vi du `man-f03` thay "
        f"`f03`):\n  " + "\n  ".join(xau))


def test_cong_ma_the_DO_khi_dat_ten_giong_mau():
    assert MA_MAU.match("#f03") and MA_MAU.match("#dde4e3")
    assert not MA_MAU.match("#man-f03")
