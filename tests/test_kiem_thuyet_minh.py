# -*- coding: utf-8 -*-
"""Phep thu cho cong `tools/kiem_thuyet_minh.py`.

⛔⛔ **Cai dang thu ⛔ khong phai "cong chay duoc" — la "cong BAT duoc".**

Mot cong chi bao xanh thi ⛔ khong chung minh duoc gi ve chinh no: no xanh
y het nhau khi **moi thu dung** va khi **phep trich da hong**. ⇒ Cac bai nay
dung cong vao ca **hai** tinh huong.
"""
from __future__ import annotations

import re

from tools import kiem_thuyet_minh as K


def test_TRICH_duoc_nhan_o_CA_BA_cach_dat_nut():
    """Man hinh dat nut theo ba loi khac nhau. Thieu mot loi la **mu mot
    vung man hinh** ma cong van bao xanh."""
    ma = (
        "const a = _nut('Bỏ ghép', 'pri', f);\n"
        "const b = TP.el('button', 'b tiny', 'Xem thêm');\n"
        "HT.mo('t', 'x', [['Đã hiểu', null], ['Ghép', async function () {}]]);"
    )
    thay = set()
    for mau in K.MAU:
        thay |= {m.group(1) for m in mau.finditer(ma)}
    assert thay == {"Bỏ ghép", "Xem thêm", "Đã hiểu", "Ghép"}, thay


def test_MOI_nhan_doc_tu_MA_deu_co_trong_CA_HAI_ban():
    """⭐ Bai nay doc **ma that** va **ca hai ban tai lieu that**.

    ⛔⛔ Cung mot phan thuyet minh song o **hai cho** *(tep `.md` doc bang
       mat, va ban ve `.html` owner mo ra duyet)*. Hai ban sao cua cung mot
       su that thi **ban ⛔ khong ai canh se muc**, va no muc **im lang**.
       ⇒ Bai nay doi nhan co mat o **CA HAI**, va noi ro thieu o ban nao.

    ⭐ Va no da bat that ngay lan chay dau sau khi ban `.html` ra doi:
      **4** nhan bi viet **rut gon** o do *(`Hiện ĐỦ các cột` thay vi
      `Hiện ĐỦ các cột của GGSheet`…)*.
    """
    nhan = K.doc_nhan()
    assert nhan, "⛔ ⛔ khong doc duoc nhan nao — phep trich da hong"
    assert len(K.TL) >= 2, "⛔ cong phai canh CA HAI ban"
    for t in K.TL:
        assert t.exists(), f"⛔ ⛔ khong thay {t}"
        noi_dung = t.read_text(encoding="utf-8")
        thieu = sorted(n for n in nhan if n not in noi_dung)
        assert not thieu, f"⛔ {t.name}: {len(thieu)} nut thieu — {thieu}"


def test_NO_khi_phep_trich_hong__xanh_tren_tap_RONG_la_CHUA_DO():
    """⛔⛔⛔ **Bai dat nhat cua tep nay.**

    Neu ai do doi cach dat nut *(hay doi ten tep man hinh)* thi `doc_nhan()`
    tra **rong** — va mot cong ngay tho se bao **DAT**, vi ⛔ khong nhan nao
    thieu ca. Do la mot cong **noi doi**: no bao *"moi nut da duoc giai
    thich"* trong khi that ra no **⛔ khong nhin thay nut nao**.

    ⇒ `chay()` phai **NO** khi tap nhan rong.
    """
    goc = K.doc_nhan
    K.doc_nhan = lambda: {}                      # type: ignore[assignment]
    try:
        assert K.chay() == 1, "⛔ cong bao DAT tren mot tap RONG"
    finally:
        K.doc_nhan = goc                         # type: ignore[assignment]


def test_NO_khi_mot_nut_MOI_chua_duoc_thuyet_minh():
    """⛔ Day la cong ra that: them nut ma ⛔ khong giai thich ⇒ ⛔ khong qua."""
    goc = K.doc_nhan
    K.doc_nhan = lambda: {**goc(),               # type: ignore[assignment]
                          "Nút Vừa Thêm Chưa Ai Tả": {"man_f01.js"}}
    try:
        assert K.chay() == 1, "⛔ mot nut MOI chua ai ta van qua duoc cong"
    finally:
        K.doc_nhan = goc                         # type: ignore[assignment]


def test_DONG_SINH_moi_dong_phai_noi_duoc_AI_sinh_ra_no():
    """⛔ Danh sach nhan *sinh luc chay* la cho **de giau nut** nhat: nhet
    mot ten vao day la cong thoi hoi ve no. ⇒ Moi dong phai tro ve mot
    **ham co that**, va bai nay kiem dieu do tren ma nguon."""
    assert K.DONG_SINH, "⛔ danh sach rong ⇒ ⛔ khong co gi de kiem"
    for nhan, o in K.DONG_SINH.items():
        tep = o.split("::")[0]
        f = K.MAN / tep
        assert f.exists(), f"⛔ {nhan!r} tro vao tep ⛔ khong co: {tep}"
        ham = re.split(r"::|\s", o.split("::", 1)[-1])[0]
        assert ham in f.read_text(encoding="utf-8"), \
            f"⛔ {nhan!r} khai do {ham!r} sinh ra, ma ⛔ khong thay ham ay"
