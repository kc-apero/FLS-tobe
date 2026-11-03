"""⛔ Cong: ca he chi duoc co **MOT** ban khai mau.

⛔⛔ **Cai nay tung hong that.** Den `2026-09-03`, khoi `:root{…}` ton tai o **ba
cho**: `A-CCR` handoff · `02_BA/Artifacts/FLS-Design-P6.html` · va
`tools/demo_dong.py` *(chep tay vao mot chuoi Python)*. Ba ban sao thi cau *"mau
canh bao la mau gi"* co **ba cau tra loi dung**, va chung se lech — ⛔ khong ai
thay, vi ⛔ khong ai mo ba tep canh nhau.

★ `BA-06` §7 goi ten benh nay: *"ve mot he thi giac thu hai la tao ra hai ban su
that ve mau va khoang cach"*.
"""
from __future__ import annotations

import os
import re

import pytest

from fls.web import phuc_vu as pv

GOC = os.path.dirname(os.path.dirname(pv.THU_MUC))          # …/fls
REPO = os.path.dirname(GOC)                                  # …/FLS
DEMO = os.path.join(REPO, "tools", "demo_dong.py")

# ⚠⚠ Phai doi CO BIEN `--…` ngay sau. Ban dau toi viet `:root\s*\{` cho gon —
# va cong bao do o **chinh dong ghi chu cua no** *(cau "co lai mot khoi
# `:root{` cua rieng no")*. Mot cong keu vi mot dong ghi chu la mot cong nguoi
# ta se go ra, ⛔ khong phai mot cong nguoi ta se nghe.
KHOI_ROOT = re.compile(r":root\s*\{\{?[^}]*?--[A-Za-z]", re.S)


def test_chi_tokens_css_duoc_khai_bien_mau():
    xau = []
    for ten in sorted(os.listdir(pv.THU_MUC)):
        if ten == "tokens.css":
            continue
        d = os.path.join(pv.THU_MUC, ten)
        if not os.path.isfile(d):
            continue
        with open(d, encoding="utf-8") as f:
            if KHOI_ROOT.search(f.read()):
                xau.append(ten)
    assert xau == [], f"⛔ {xau} co khoi `:root{{` rieng — ban su that thu hai"


def test_demo_dong_KHONG_con_ban_sao_mau_rieng():
    """⭐ Bo nao sinh `FLS-Demo-Dong.html` phai DOC `tokens.css`, ⛔ khong chep."""
    with open(DEMO, encoding="utf-8") as f:
        chu = f.read()
    assert not KHOI_ROOT.search(chu), (
        "⛔ `tools/demo_dong.py` co lai mot khoi `:root{` cua rieng no — do la "
        "ban sao thu hai cua bang mau, va no se lech trong im lang")
    assert "_tokens()" in chu, "⛔ demo ⛔ khong doc `tokens.css`"


def test_demo_dong_doc_dung_tep_tokens_that():
    import importlib.util
    import sys

    ten = "demo_dong_de_kiem"
    dac = importlib.util.spec_from_file_location(ten, DEMO)
    m = importlib.util.module_from_spec(dac)
    sys.modules[ten] = m
    try:
        dac.loader.exec_module(m)
    except ImportError as e:                       # psycopg / thu vien thieu
        pytest.skip(f"⛔ khong nap duoc `demo_dong.py`: {e}")
    finally:
        sys.modules.pop(ten, None)

    khoi = m._tokens()
    assert khoi.startswith(":root{") and khoi.rstrip().endswith("}")
    # ⛔ Phai la mau THAT, ⛔ khong phai mot chuoi rong "trong nhu da doc".
    assert "--ink:" in khoi and "--crit:" in khoi
    # ⚠ ⛔ KHONG duoc nhan doi dau ngoac: gia tri chen vao f-string ⛔ khong bi
    #   quet lai, nhan doi se ra `{{` THAT tren man hinh.
    assert "{{" not in khoi and "}}" not in khoi


def test_ban_ve_va_tokens_khong_lech_mau():
    """⭐ Ban ve `FLS-Design-P6.html` la he thi giac chinh (owner chot
    2026-09-03) ⇒ moi mau cua no phai co mat trong `tokens.css`.

    ⛔ Ban ve nam o kho TAI LIEU (repo khac) nen bai nay **bo qua** khi ⛔ khong
    tim thay — nhung ⛔ khong am tham: no bao `skip`, ⛔ khong xanh gia.
    """
    # 2026-09-03: ban ve nay nay o TRONG repo (`docs/ITL/...`) sau khi bo tai lieu
    # ITL chuyen ve day. Truoc do no o repo FIN-ERP canh ben ⇒ test phai `skip`
    # khi khong thay. Nay no CHAC CHAN co: thay `skip` bang `assert`, vi mot test
    # tu bo qua chinh no la mot test khong bao gio do.
    ve = os.path.join(REPO, "docs", "ITL", "02_BA", "Artifacts",
                      "FLS-Design-P6.html")
    assert os.path.isfile(ve), f"⛔ khong thay ban ve tai {ve} — no phai o trong repo"

    ma_mau = re.compile(r"#[0-9a-fA-F]{6}\b")
    with open(ve, encoding="utf-8") as f:
        chu = f.read()
    khoi = chu[chu.index("<style>"):chu.index("</style>")]
    cua_ve = {m.group(0).lower() for m in ma_mau.finditer(khoi)}

    with open(os.path.join(pv.THU_MUC, "tokens.css"), encoding="utf-8") as f:
        cua_ta = {m.group(0).lower() for m in ma_mau.finditer(f.read())}

    thieu = cua_ve - cua_ta
    assert thieu == set(), (
        f"⛔ ban ve dung {sorted(thieu)} ma `tokens.css` ⛔ khong co ⇒ man that "
        f"se ⛔ khong giong ban ve owner da duyet")
