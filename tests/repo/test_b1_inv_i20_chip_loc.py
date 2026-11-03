# -*- coding: utf-8 -*-
"""`B1` — `INV-I20`: DICH CUOI ⛔ KHONG duoc tron vao VIEC.

⭐⭐⭐ `QĐ-ITL-148` · `2026-09-21`. Bai nay ton tai vi mot phep do:

    ⛔⛔ `INV-I20` — bat bien **TRUNG TAM** cua man `SCR-F01` — co **`0`** tep
       test nao goi ten no, trong khi `INV-I16` co **`45`**.

    ⇒ Cong nghiem thu `G-a` *(danh sach mac dinh `738`, ⛔ khong `1.553`)*
      **TRUOT** tren ban dung `21/09` — va ⛔ **khong cong may nao bao**, don
      gian vi ⛔ khong bai nao hoi cau ay.

── Ban dung sai o dau ───────────────────────────────────────────────────

Ban dung co **BA** chip: `Chua gan` / `Da gan` / `Tat ca`, trong do
`Chua gan` = *moi dong ⛔ khong phai da gan* ⇒ no **gop ca `768` dong ⛔ khong
gan duoc** vao viec hang ngay.

⛔ `INV-I20` noi mot dong roi hang cho bang **BA** duong, va `768` dong ay la
  **DICH CUOI** — noi mot dong **ROI** hang cho, ⛔ khong phai noi ai do ngoi
  lam. ⇒ Thieu **chip thu tu**, va do la thieu **mot KHAI NIEM**, ⛔ khong
  phai thieu mot cu bam.

── Do tren kho THAT `21/09` ─────────────────────────────────────────────

    nguoi                535
    may · ⛔ khong tu chung  203     ⇒ ⭐ viec that = **738**
    may · tu chung         47
    ⛔ khong               768     ⇒ **DICH CUOI**, ⛔ khong nut hanh dong nao
    ─────────────────────────
    tong               1.553
"""
from __future__ import annotations

import pytest

from fls.repo import man_ghep
from fls.repo.lenh_cho import RO_KHONG, RO_MAY, RO_NGUOI


def _d(ro: str, tu_chung: bool = False) -> dict:
    return {"ro": ro, "tu_chung": tu_chung}


# ── bon chip, ⛔ khong ba ────────────────────────────────────────────────

def test_co_DUNG_BON_chip_loc():
    """⛔ Ban dung co ba. Chip thu tu la mot KHAI NIEM, ⛔ khong mot cu bam."""
    assert set(man_ghep.CHIP) == {
        "chua_gan", "da_gan", "khong_gan_duoc", "tat_ca"}, sorted(man_ghep.CHIP)


def test_chip_mac_dinh_la_CHUA_GAN():
    assert man_ghep.CHIP_MAC_DINH == "chua_gan"


# ── ⭐ dich cuoi ⛔ KHONG lot vao viec ────────────────────────────────────

def test_dong_KHONG_GAN_DUOC_KHONG_lot_vao_chip_chua_gan():
    """⭐⭐⭐ Day la `G-a`. `768` dong nay ⛔ khong phai viec cua ai."""
    d = _d(RO_KHONG)
    assert man_ghep.chip_cua_dong(d) == "khong_gan_duoc"
    assert not man_ghep.thuoc_chip(d, "chua_gan"), (
        "⛔ dong `⛔ khong gan duoc` dang lot vao chip `Chua gan` ⇒ danh sach "
        "mac dinh thanh `1.553` thay vi `738`. Do la DICH CUOI (`INV-I20`), "
        "⛔ khong phai viec.")


@pytest.mark.parametrize("ro,tu_chung", [
    (RO_NGUOI, False),   # 535 — ⛔ chua co so chung tu
    (RO_MAY, False),     # 203 — khop ma, lech tien
    (RO_MAY, True),      # 47  — tu chung, chi can gat
])
def test_ba_loai_VIEC_THAT_deu_vao_chip_chua_gan(ro, tu_chung):
    assert man_ghep.thuoc_chip(_d(ro, tu_chung), "chua_gan")


def test_chip_TAT_CA_om_ca_dich_cuoi():
    """⭐ `Tat ca` la loi thoat: ⛔ khong duoc GIAU `768` dong khoi moi loi vao."""
    assert man_ghep.thuoc_chip(_d(RO_KHONG), "tat_ca")


# ── ⭐ ba duong ra, ⛔ khong bon ─────────────────────────────────────────

def test_mot_dong_co_DUNG_BA_duong_ra():
    """⚰ Nut `Xong` KHAI TU `21/09` (`QĐ-ITL-148 ④`).

    Ly do goc cua `QĐ-ITL-71` la *"cho danh dau viec dang lam do"* — thiet ke
    moi **giai bai ay bang cach khac** *(gan xong **tu nhay** sang lenh chua
    gan ke tiep)*, nen trang thai *"dang lam do"* ⛔ khong con ton tai de ma
    danh dau.
    """
    assert man_ghep.DUONG_RA == ("ghep_duoc", "khong_gan_duoc", "loi_nguon"), (
        man_ghep.DUONG_RA)


def test_KHONG_co_duong_ra_ten_XONG():
    assert "xong" not in {x.lower() for x in man_ghep.DUONG_RA}
    assert "done" not in {x.lower() for x in man_ghep.DUONG_RA}
