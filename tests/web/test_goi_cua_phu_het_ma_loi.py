"""⛔ Cong BAT CAU: moi ma loi cua tang cua phai co mot cau tieng Viet.

⛔⛔ **Vi sao cong nay ton tai.** `QĐ-ITL-27` khai tu vai hau kiem ⇒ nguoi doc
cau bao loi la **nguoi duy nhat** con lai trong vong. Neu tang cua them mot ma
ma man hinh quen, ke toan se thay mot chuoi nhu `FLS-DQ-FAILED` va ⛔ khong biet
lam gi — va cai ho lam la **bo qua**.

★ Cong nay bat qua HAI ngon ngu: doc `MA_LOI` trong `fls/api/bao.py` (Python)
roi doi chieu voi `CAU` trong `goi_cua.js` (JavaScript). ⛔ Khong co bo kiem
kieu nao lam duoc viec do, nen phai la mot bai test.
"""
from __future__ import annotations

import os
import re

from fls.api import bao
from fls.web import phuc_vu as pv

GOI_CUA = os.path.join(pv.THU_MUC, "goi_cua.js")


def _doc_js() -> str:
    with open(GOI_CUA, encoding="utf-8") as f:
        return f.read()


def _ma_trong_js(chu: str) -> set[str]:
    """Lay cac khoa `'FLS-...':` — tuc ma DA CO mot cau, ⛔ khong phai ma chi
    duoc nhac toi trong mot dong ghi chu."""
    return set(re.findall(r"^\s*'(FLS-[A-Z-]+)'\s*:\s*\{", chu, re.M))


def _ma_tu_man_hinh(chu: str) -> set[str]:
    khoi = re.search(r"MA_TU_MAN_HINH\s*=\s*\[(.*?)\]", chu, re.S)
    return set(re.findall(r"'(FLS-[A-Z-]+)'", khoi.group(1))) if khoi else set()


def test_moi_ma_loi_cua_cua_deu_co_cau_tieng_viet():
    thieu = set(bao.MA_LOI) - _ma_trong_js(_doc_js())
    assert thieu == set(), (
        f"⛔ {sorted(thieu)} co trong `bao.MA_LOI` ma ⛔ khong co cau tieng Viet "
        f"trong `goi_cua.js`. Ke toan se doc chuoi ma va ⛔ khong biet lam gi.")


def test_khong_cau_thua_nao_ngoai_hai_ma_sinh_o_man_hinh():
    """Chieu nguoc: mot cau cho mot ma ⛔ khong ton tai la mot cau chet."""
    js = _doc_js()
    thua = _ma_trong_js(js) - set(bao.MA_LOI) - _ma_tu_man_hinh(js)
    assert thua == set(), (
        f"⛔ {sorted(thua)} co cau trong `goi_cua.js` ma ⛔ khong co trong "
        f"`bao.MA_LOI` va cung ⛔ khong khai trong `MA_TU_MAN_HINH`")


def test_hai_ma_sinh_o_man_hinh_that_su_khong_den_tu_cua():
    js = _doc_js()
    tu_man = _ma_tu_man_hinh(js)
    assert tu_man, "⛔ `MA_TU_MAN_HINH` rong hay doc khong ra"
    assert tu_man & set(bao.MA_LOI) == set(), (
        "⛔ mot ma vua khai la 'sinh o man hinh' vua co trong `bao.MA_LOI` — "
        "mot trong hai cho dang noi doi")


def test_moi_cau_deu_co_du_hai_phan():
    """`cau` (chuyen gi) + `lam_gi` (lam gi tiep). Mot cau thieu ve sau la mot
    cau lam nguoi doc **dung lai**, va dung lai nghia la bo qua."""
    js = _doc_js()
    khoi = re.findall(
        r"'(FLS-[A-Z-]+)'\s*:\s*\{(.*?)\}", js, re.S)
    thieu = [ma for ma, than in khoi
             if "cau:" not in than or "lam_gi:" not in than]
    assert thieu == [], f"⛔ cau cho {thieu} thieu `cau` hay `lam_gi`"


# ── ⛔⛔ PHA CO CHU DICH: cong phai DO ─────────────────────────────────────
def test_cong_DO_khi_cua_them_ma_ma_man_hinh_quen(monkeypatch):
    monkeypatch.setitem(bao.MA_LOI, "FLS-MA-MOI-TINH", (418, "ma vua them"))
    thieu = set(bao.MA_LOI) - _ma_trong_js(_doc_js())
    assert "FLS-MA-MOI-TINH" in thieu


def test_cong_DO_khi_man_hinh_giu_mot_cau_CHET(monkeypatch):
    js_gia = _doc_js().replace(
        "    'FLS-UNAUTHORIZED': {",
        "    'FLS-DA-KHAI-TU': {\n      cau: 'x', lam_gi: 'y'\n    },\n"
        "    'FLS-UNAUTHORIZED': {")
    thua = _ma_trong_js(js_gia) - set(bao.MA_LOI) - _ma_tu_man_hinh(js_gia)
    assert thua == {"FLS-DA-KHAI-TU"}
