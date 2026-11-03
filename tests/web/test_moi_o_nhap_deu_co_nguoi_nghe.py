# -*- coding: utf-8 -*-
"""⛔ Cong: moi O NHAP trong vo deu phai co **nguoi nghe**.

⛔⛔⛔ **Bon lo cung mot hinh dang trong ba ngay, va ⛔ khong cong nao bat:**

  ① `ST.dong`          — ⛔ khong ai goi cua nap danh sach
  ② `F01G.phim`        — `9` phim viet du, ⛔ khong ai dang ky `keydown`
  ③ `#ghep-tim`        — o nhap co trong vo, ⛔ khong ai nghe `input`
  ④ `itl_id_da_gan`    — doc mot khoa **⛔ khong ai sinh ra**

⭐⭐ Goc chung: **bai thu voi tay VAO goi thu ma san pham phai voi tay RA
   noi.** Cong nay do **chieu con lai** — mot phan tu **ton tai trong vo** thi
   phai co it nhat mot doan ma cham toi no; va mot **o NHAP** thi phai co ai
   **NGHE** no hoac **DOC gia tri** cua no.

⭐⭐⭐ **Mot o nhap chi duoc nhay vao ma ⛔ khong duoc doc con TE HON mot o
   ⛔ khong co:** no **MOI** nguoi ta go, roi ⛔ khong lam gi ca. Do dung la
   `#ghep-tim` tu `21/09` den `22/09`.

⛔ Cong nay **⛔ khong thay duoc** mot cong CHAY *(no van la phep quet chu)*.
  No la **luoi thua**: bat cho **QUEN HAN**. Con *"noi nhung noi sai"* thi
  phai la mot bai chay — nhu `test_b3_ban_phim_noi_that.py`.
"""
from __future__ import annotations

import io
import os
import re

from fls.web import phuc_vu as pv

VO = os.path.join(pv.THU_MUC, "index.html")

#: ⭐ CHI soi the **nhan tuong tac**. Mot `<div id=…>` la mot cai neo de ve
#: vao, ⛔ khong phai mot thu doi phan ung.
THE_TUONG_TAC = re.compile(
    r"<(input|select|textarea)\b[^>]*\bid=[\"']([^\"']+)[\"']", re.I)

#: ⭐ Ban TRANG. Them mot ten vao day la khai *"o nay CO Y ⛔ khong ai nghe"*,
#: va no phai co **ly do viet ngay canh**.
MIEN_TRU: dict[str, str] = {}


def _doc(duong: str) -> str:
    return io.open(duong, encoding="utf-8").read()


def _js() -> str:
    """⭐ Gop **moi** tep `.js` duoc phuc vu — mot o co the duoc nghe tu bat ky
    man nao, va `ung_dung.js` la vo dung chung."""
    return "\n".join(
        _doc(os.path.join(pv.THU_MUC, t))
        for t in sorted(os.listdir(pv.THU_MUC)) if t.endswith(".js"))


def _o_nhap() -> list[str]:
    return [ma for _, ma in THE_TUONG_TAC.findall(_doc(VO))
            if ma not in MIEN_TRU]


def test_vo_that_su_CO_o_nhap_de_soi():
    """⛔ Neu `index.html` ⛔ khong con o nhap nao thi hai bai duoi **xanh vi
    ⛔ khong co gi** — va mot cong nhu the ⛔ khong canh gi.

    ⭐ Do `22/09`: vo co **1** o nhap mang `id` — `#ghep-tim`. ⚠ Con so nay
      **nho**, va do chinh la ly do lo ay song duoc ba ngay: mot o duy nhat
      thi ⛔ khong ai thay no thieu khi doc luot qua.
    ⛔ Nguong la `>= 1`, ⛔ khong phai mot con so to hon do toi **tu dat**:
      mot nguong ⛔ khong do duoc se do vi mot ly do ⛔ khong lien quan.
    """
    assert len(_o_nhap()) >= 1, _o_nhap()


def test_moi_o_nhap_trong_vo_deu_co_ma_cham_toi():
    js = _js()
    mo_coi = [ma for ma in _o_nhap() if ma not in js]
    assert mo_coi == [], (
        "⛔⛔ Ô nhập có trong vỏ mà ⛔ KHÔNG một dòng JS nào chạm tới — nó sẽ "
        "hiện ra, gõ được, và ⛔ không làm gì:\n  " + "\n  ".join(mo_coi))


def test_o_nhap_KHONG_duoc_chi_duoc_FOCUS_ma_KHONG_duoc_NGHE():
    """⛔⛔ Dung lo cua `#ghep-tim`: no duoc `focus()` boi phim `/` va **⛔ khong
    ai nghe** ⇒ nhay vao duoc, go duoc, va ⛔ khong gi xay ra."""
    js = _js()
    xau = []
    for ma in _o_nhap():
        if ma not in js:
            continue    # da bao o bai tren — ⛔ khong bao hai lan mot loi
        # ⭐ Co ai nghe `input`/`change`/`keydown`, hay **doc `.value`** cua no?
        #   ⚠ Chap nhan ca hai khuon: gan thang len the *(`t.addEventListener`)*
        #     va **uy quyen** o `document` *(`t.id !== 'ghep-tim'`)*.
        gan = re.search(
            r"['\"]#?" + re.escape(ma) + r"['\"][\s\S]{0,900}?"
            r"(addEventListener\s*\(\s*['\"](?:input|change|keydown|keyup)|"
            r"\.oninput|\.onchange|\.value\b)", js)
        if not gan:
            xau.append(ma)
    assert xau == [], (
        "⛔ Ô nhập ⛔ không ai NGHE và ⛔ không ai ĐỌC giá trị — một ô chỉ được "
        "nhảy vào mà ⛔ không được đọc **tệ hơn** một ô ⛔ không có, vì nó MỜI "
        "người ta gõ:\n  " + "\n  ".join(xau))


# ── ⛔⛔ PHA CO CHU DICH: cong phai DO ─────────────────────────────────────

def test_cong_DO_khi_mot_o_nhap_mo_coi():
    """⭐ Mot cong ⛔ chua bao gio thay mau do la mot cong ⛔ chua ai do."""
    gia_vo = '<input id="o-khong-ai-nghe" placeholder="x">'
    assert THE_TUONG_TAC.findall(gia_vo) == [("input", "o-khong-ai-nghe")]
    assert "o-khong-ai-nghe" not in _js()


def test_cong_KHONG_bao_dong_gia_voi_the_KHONG_tuong_tac():
    """⛔ Mot cong keu vi mot `<div>` la mot cong nguoi ta se **go ra**."""
    assert THE_TUONG_TAC.findall('<div id="ghep-goc"></div>') == []
    assert THE_TUONG_TAC.findall('<section id="man-ghep">') == []
