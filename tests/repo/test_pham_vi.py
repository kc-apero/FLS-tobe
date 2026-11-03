"""PHAM VI doc — ⛔ khong co mac dinh, va `ca_kho` phai viet ly do.

★ Bo bai nay canh dung cai duong ma 194 dong dau test da di: mot cau doc khong
mang pham vi. Xem `fls/repo/pham_vi.py`.
"""
from __future__ import annotations

import pathlib

import pytest

from fls.repo import pham_vi as pv
from fls.repo.kho_sach import HINH_RUN_THAT


def test_khong_co_pham_vi_MAC_DINH():
    """⛔ `PhamVi()` khong goi duoc — thieu doi so la NO ngay luc goi, ⛔ khong
    im lang tro thanh "ca kho"."""
    with pytest.raises(TypeError):
        pv.PhamVi()                                       # type: ignore[call-arg]


def test_kieu_la_thi_NO():
    with pytest.raises(ValueError, match="khong biet"):
        pv.PhamVi(kieu="tat_ca")


def test_ca_kho_KHONG_ly_do_thi_NO():
    """⛔ Doc ca kho la doc ca dau test. Bat buoc viet ra vi sao."""
    with pytest.raises(ValueError, match="LY DO"):
        pv.ca_kho("")
    with pytest.raises(ValueError, match="LY DO"):
        pv.ca_kho("   ")
    assert pv.ca_kho("soi kho sau khi don").kieu == "ca_kho"


def test_mot_lan_nap_thieu_run_id_thi_NO():
    with pytest.raises(ValueError, match="run_id"):
        pv.mot_lan_nap("")


def test_pham_vi_khac_khong_nhan_run_id():
    with pytest.raises(ValueError, match="khong nhan run_id"):
        pv.PhamVi(kieu="nap_that", run_id="NAP-2026-08-27-RAW")


# ── menh de SQL ───────────────────────────────────────────────────────────
def test_ban_trang_dung_DUNG_mau_cua_kho_sach():
    """★ Mot nguon su that: mau `run_id` khai o `kho_sach`, cau SQL dung lai."""
    sql, ts = pv.chi_nap_that().dieu_kien("i.run_id")
    assert sql == "i.run_id ~ %s"
    assert ts == [HINH_RUN_THAT.pattern]


def test_mot_lan_nap_GIAO_voi_ban_trang_khong_thay_the():
    """⛔ Truyen `?run_id=` cua mot lan test thi cau doc tra RONG, ⛔ khong tra
    dong test ra. Neu menh de chi con `run_id = %s` thi cua doc co mot duong
    vong qua ban trang chi bang mot tham so URL."""
    sql, ts = pv.mot_lan_nap("NAP-2026-08-27-RAW").dieu_kien("i.run_id")
    assert sql.count("~") == 1, f"mat ban trang: {sql}"
    assert "i.run_id = %s" in sql
    assert ts == [HINH_RUN_THAT.pattern, "NAP-2026-08-27-RAW"]


def test_ca_kho_la_TRUE_khong_tham_so():
    assert pv.ca_kho("thu").dieu_kien() == ("TRUE", [])


def test_bi_danh_cot_duoc_ap_dung():
    sql, _ = pv.chi_nap_that().dieu_kien("r.run_id")
    assert sql.startswith("r.run_id")


# ── cong quet ma nguon ────────────────────────────────────────────────────
def test_tang_CUA_khong_duoc_GOI_ca_kho():
    """⛔⛔ Cong. `fls/api/**` ⛔ khong duoc co duong nao doc ca kho — do la
    dung duong dau test di ra man hinh. Cong nay quet MA NGUON vi mot loi hua
    trong tai lieu la mot loi hua khong ai kiem.

    ⚠ Quet bang `ast` chu ⛔ khong bang `in`: mot cau ghi chu *"⛔ khong co
    `ca_kho`"* la dung chinh sach ma se lam mot phep quet chuoi bao dong. Cong
    bao dong lien tuc la cong sap bi go ra.
    """
    import ast

    goc = pathlib.Path(__file__).resolve().parents[2] / "fls" / "api"
    xau: list[str] = []
    for f in sorted(goc.rglob("*.py")):
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for n in ast.walk(cay):
            ten = None
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    ten = n.func.id
                elif isinstance(n.func, ast.Attribute):
                    ten = n.func.attr
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    if a.name == "ca_kho":
                        xau.append(f"{f.name}:{n.lineno}: import ca_kho")
            if ten == "ca_kho":
                xau.append(f"{f.name}:{n.lineno}: goi ca_kho()")
    assert xau == [], "tang cua goi/import ca_kho: " + " · ".join(xau)
