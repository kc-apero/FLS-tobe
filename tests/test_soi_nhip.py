# -*- coding: utf-8 -*-
"""Phep thu cho `tools/soi_nhip.py::do_khong_chac` — luat *"moi gio co dung"*.

⛔ Cac bai nay ⛔ KHONG goi PowerShell va ⛔ khong mo kho: chung kiem **phan
LUAT** tren mot ban ghi bo hen gio dung dang `dict`. Khai ra chu ⛔ khong de
nguoi doc tu suy — phan *doc that* nam o `doc_bo_hen_gio()`, Windows-only.

⛔⛔⛔ **Cai chung chan, va no da xay ra that.** `soi_nhip.py` ban dau **IN**
con so `so_luot_hut` roi in ngay duoi mot dong `✅ Bo hen gio CO CHAY` va tra
ma `0`. Tuc cong cu **da co** con so noi *"nhip bo 3 luot"* va van ket luan
xanh: mot con so nam canh mot ket luan ⛔ khong doc no. ⇒ Moi bai duoi day
ghim mot ly do KHONG CHAC phai **noi ra duoc**, ⛔ khong chi in ra.
"""
from __future__ import annotations

from tools.soi_nhip import do_khong_chac

# ⭐ Ban ghi CHAC CHAN: may tu thuc, chay ca khi rut dien, ⛔ khong bi giet,
#   ⛔ khong luot nao hut. Moi bai duoi lay ban nay roi **pha dung mot o**.
CHAC = {
    "so_luot_hut": 0,
    "danh_thuc_may": True,
    "chay_khi_pin": True,
    "giet_khi_rut_dien": False,
    "chay_bu_khi_hut": True,
}


def test_BAN_GHI_CHAC_CHAN_thi_RONG():
    assert do_khong_chac(CHAC) == []


def test_CO_LUOT_HUT_thi_phai_NOI_RA():
    ly = do_khong_chac({**CHAC, "so_luot_hut": 3})
    assert len(ly) == 1
    # ⭐ Con so phai co trong cau — mot cau *"co luot hut"* ⛔ khong noi duoc
    #   la 3 luot hay 300 luot, va hai cai do la hai muc do khac nhau.
    assert "3" in ly[0]
    assert "HUT" in ly[0]


def test_MAY_NGU_thi_phai_NOI_RA():
    ly = do_khong_chac({**CHAC, "danh_thuc_may": False})
    assert len(ly) == 1
    assert "WakeToRun" in ly[0]


def test_RUT_DIEN_KHONG_CHAY_thi_phai_NOI_RA():
    ly = do_khong_chac({**CHAC, "chay_khi_pin": False})
    assert len(ly) == 1
    assert "DisallowStartIfOnBatteries" in ly[0]


def test_BI_GIET_GIUA_DUONG_thi_phai_NOI_RA():
    ly = do_khong_chac({**CHAC, "giet_khi_rut_dien": True})
    assert len(ly) == 1
    assert "StopIfGoingOnBatteries" in ly[0]


def test_NHIEU_LY_DO_thi_NOI_HET_khong_dung_o_cai_dau():
    """⛔ Mot ham tra `str | None` se **che** ba ly do con lai.

    Do la vi sao no tra `list`: hom 10/09 ban ghi that co **BON** ly do cung
    luc *(3 luot hut · ⛔ khong danh thuc · ⛔ khong chay khi pin · bi giet khi
    rut dien)*, va bao cao chi mot ly do se lam nguoi doc di sua mot thu roi
    tuong da xong.
    """
    ly = do_khong_chac({"so_luot_hut": 3, "danh_thuc_may": False,
                        "chay_khi_pin": False, "giet_khi_rut_dien": True,
                        "chay_bu_khi_hut": True})
    assert len(ly) == 4


def test_THIEU_KHOA_thi_KHONG_bao_oan():
    """⛔ Ban ghi thieu khoa *(may khong phai Windows, hay `Get-ScheduledTask`
    doi ten truong)* ⛔ KHONG duoc bien thanh mot loi bia ra.

    ⭐ Phep kiem la `is False` / `is True`, ⛔ khong phai `not ...` — voi
      `None` thi `not None` la `True` va cong se **bao oan** rang may ⛔ khong
      danh thuc, trong khi su that la **⛔ khong do duoc**.
    """
    assert do_khong_chac({}) == []
    assert do_khong_chac({"danh_thuc_may": None, "chay_khi_pin": None,
                          "giet_khi_rut_dien": None}) == []


# ── ve do TU KHO: `gio_trong` ───────────────────────────────────────────
def test_GIO_TRONG_tu_kho_cung_lam_no_KHONG_CHAC():
    """⭐⭐⭐ Ve nay do TU KHO nen no **chay tren moi may** — khac ba cai dat
    va `so_luot_hut`, ca bon deu phai hoi API cua Windows.

    ⚠ Va no do MOT THU KHAC: `so_luot_hut` noi *"bo hen gio ⛔ khong chay"*,
      con `gio_trong` noi *"kho ⛔ KHONG CO ANH"*. Hai ve **co the lech** —
      bo hen gio chay ma `can_chup` bo luot dung thi `so_luot_hut = 0` va
      `gio_trong = 0`. Giu ca hai vi chung ⛔ khong thay nhau duoc.
    """
    ly = do_khong_chac(CHAC, {"gio_trong": {"Bank": 3, "PM": 5}})
    assert len(ly) == 2
    assert "Bank" in ly[0] and "3" in ly[0]
    assert "PM" in ly[1] and "5" in ly[1]


def test_GIO_TRONG_bang_0_thi_KHONG_bao():
    assert do_khong_chac(CHAC, {"gio_trong": {"Bank": 0, "PM": 0}}) == []


def test_THIEU_kho_thi_van_chay_khong_NO():
    """⛔ `kho=None` la duong goi cu — no ⛔ khong duoc NO, va cung ⛔ khong
    duoc **bia** ra mot ly do."""
    assert do_khong_chac(CHAC) == []
    assert do_khong_chac(CHAC, {}) == []


def test_HAU_QUA_dat_TRUOC_NGUYEN_NHAN():
    """⭐ Nguoi doc can thay *"kho thieu 3 gio anh"* TRUOC *"WakeToRun=False"*
    — mot ten co trong PowerShell ⛔ khong noi len dieu gi da mat."""
    ly = do_khong_chac({**CHAC, "danh_thuc_may": False},
                       {"gio_trong": {"Bank": 3}})
    assert len(ly) == 2
    assert "GIO TRONG" in ly[0]
    assert "WakeToRun" in ly[1]
