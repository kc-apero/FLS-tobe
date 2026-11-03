# -*- coding: utf-8 -*-
"""Phep thu cho TRUC THU HAI — `khau` nghiep vu (17/09).

⛔⛔ **Cai dang thu ⛔ khong phai "ban ve dep".** Ban ve nay tra loi cau owner
hoi — *"entity thuoc module nghiep vu nao"* — nen thu that su la:

  ⓐ **moi** thuc the co mot khau *(thieu mot cai = owner ⛔ khong tra loi duoc)*;
  ⓑ thu tu `Ⓐ→Ⓑ→Ⓒ` **chac chan**, ⛔ khong phu thuoc bo xep hang cua mermaid;
  ⓒ mui ten tren ban ve nay ⛔ **KHONG** phai khoa ngoai — tron hai loai la
     cach chac chan nhat de nguoi doc tin mot quan he ⛔ khong ton tai.

⭐ Va tat ca phai **⛔ khong gia duoc**: `khau` la mot truong cua ban khai, va
   cong `--kiem` NO khi ban ve lech no.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import pytest

from tools import sinh_ban_do_tang as B


# ────────────────────────────── ban khai ──────────────────────────────
def test_MOI_thuc_the_deu_khai_KHAU():
    """⭐⭐ Owner hoi *"entity thuoc module nao"*. Mot bang ⛔ khong khai `khau`
    la mot bang ⛔ KHONG tra loi duoc cau ay — va no bien mat im lang."""
    bang = B.doc_bang()
    assert bang, "⛔ ⛔ khong doc duoc bang nao — phep trich da hong"
    thieu = sorted(b.name for b in bang if not getattr(b, "khau", ""))
    assert not thieu, f"⛔ {len(thieu)} bang ⛔ khong khai `khau`: {thieu}"


def test_moi_KHAU_khai_deu_co_THAT__va_nguoc_lai():
    co = {b.khau for b in B.doc_bang()}
    khai = {m for m, _, _, _ in B.KHAU}
    assert not (co - khai), f"⛔ khau co that ma ⛔ khong khai: {sorted(co - khai)}"
    assert not (khai - co), f"⛔ khau khai ma RONG: {sorted(khai - co)}"


def test_KHAU_khep_ve_tong_so_bang():
    """Mot phep phan loai ⛔ khong cong ve tong la mot phep ⛔ khong kiem duoc."""
    bang = B.doc_bang()
    tong = sum(sum(1 for b in bang if b.khau == m) for m, _, _, _ in B.KHAU)
    # ⭐ `23` → `24`: them khung xem `fls_may_goi_y` (migration `0025`,
    #   `QĐ-ITL-143`) — **toi biet minh vua them mot thuc the**
    # ⭐ `24` → `25`: them khung xem `fls_dien_giai` (migration `0026`,
    #   `QĐ-ITL-145`) — **toi biet minh vua them mot thuc the**
    assert tong == len(bang) == 25, f"⛔ {tong} ≠ {len(bang)}"


def test_NO_khi_mot_bang_MOI_chua_khai_khau(monkeypatch):
    """⛔ Cong chua tung thay DO la cong chua biet co song. Pha co chu dich."""
    that = B.doc_bang()

    class _Gia:
        def __init__(self, b):
            for k in ("name", "columns", "tang", "kind", "erd_entity",
                      "pk_cols", "unique_keys", "island_reason"):
                setattr(self, k, getattr(b, k, None))
            self.khau = ""

    monkeypatch.setattr(B, "doc_bang", lambda: [_Gia(that[0])] + that[1:])
    with pytest.raises(SystemExit) as e:
        B.sinh_khau()
    assert "khau" in str(e.value)


def test_pm_line_thuoc_khau_GHEP_du_khau_NAP_la_thu_GHI_no():
    """⭐⭐ Ghim **luat gan**: theo VIEC NO PHUC VU, ⛔ khong theo ai ghi no.

    `fls_pm_line` do duong nap (`lo_nap`) GHI, nhung no ton tai de man GHEP
    dung. Gan theo *"ai ghi"* se keo ca `fls_queue_event` ve khau `A` — trong
    khi do la **bang viec cua NGUOI**. Doi luat thi bai nay phai DO truoc.
    """
    b = {x.name: x for x in B.doc_bang()}
    assert b["fls_pm_line"].khau == "B-ghep"
    assert b["fls_queue_event"].khau == "V-viec"
    assert b["fls_itl"].khau == "S-so"


# ────────────────────────────── ban ve mermaid ────────────────────────
def test_CHUOI_dung_thu_tu_khai__A_roi_B_roi_C():
    """⭐⭐ Thu tu la CAU TRA LOI cua owner. No phai **chac chan**."""
    ve = B.sinh_khau()
    canh = re.findall(r"^  (\w+) ==> (\w+)$", ve, re.M)
    mong = [(B._sg(a), B._sg(c))
            for a, c in zip(B._CHUOI, B._CHUOI[1:])]
    assert canh == mong, f"⛔ chuoi dong chay lech: {canh} ≠ {mong}"
    assert len(B._CHUOI) == 3, "⛔ owner hoi BA khau — chuoi phai la 3"


def test_VI_TRI_subgraph_dung_thu_tu_khai():
    ve = B.sinh_khau()
    thay = re.findall(r"subgraph (\w+)\[", ve)
    mong = [B._sg(m) for m, _, _, _ in B.KHAU]
    assert thay == mong, f"⛔ thu tu dai lech ban khai: {thay}"


def test_ban_ve_KHAU_khong_mang_MOT_canh_khoa_ngoai_nao():
    """⛔⛔ Mui ten o day la DONG CHAY, ⛔ khong phai FK.

    Tron hai loai mui ten tren mot ban ve la cach nguoi doc tin mot quan he
    ⛔ khong ton tai. Bai nay canh dung dieu do: **⛔ khong canh nao noi hai
    TEN BANG**, moi canh phai noi hai **dai**.
    """
    ve = B.sinh_khau()
    ten_bang = {b.name for b in B.doc_bang()}
    for dong in ve.splitlines():
        m = re.match(r"^  (\w+) (==>|-\.->) (\w+)$", dong)
        if not m:
            continue
        assert m.group(1) not in ten_bang and m.group(3) not in ten_bang, (
            f"⛔ canh noi TEN BANG ⇒ doc nham thanh khoa ngoai: {dong!r}")


def test_VIEC_la_DICH_chu_khong_phai_NGUON():
    """⚠ `V -.-> B` lam hang cho xep **TRUOC** Ⓑ ⇒ ban ve tu noi doi ve thu tu.

    Va nghia cung nguoc: Ⓑ/Ⓒ **day viec vao** hang cho, ⛔ khong nguoc lai.
    """
    ve = B.sinh_khau()
    v = B._sg("V-viec")
    assert f"  {B._sg('B-ghep')} -.-> {v}" in ve
    assert f"  {B._sg('C-sua')} -.-> {v}" in ve
    assert f"  {v} -.->" not in ve, "⛔ VIEC dang la NGUON — sai ca nghia lan xep hang"


def test_subgraph_va_end_can_nhau():
    ve = B.sinh_khau()
    assert ve.count("subgraph ") == sum(
        1 for l in ve.splitlines() if l.strip() == "end")


# ────────────────────────────── ban ve SVG ────────────────────────────
def test_SVG_KHAU_hop_le_va_TU_CHUA():
    """⛔ Toi ⛔ khong nhin duoc ban ve minh sinh ra ⇒ bai nay thay doi mat."""
    svg = B.sinh_svg_khau(B.doc_bang())
    ET.fromstring(svg)
    for xau in ("<script", "onload", "<foreignObject", "<image", "@import"):
        assert xau not in svg, f"⛔ SVG mang {xau!r} — ⛔ khong con tu chua"
    # ⚠ `url(#mk)` tro toi `<defs>` **cung tep** — trinh duyet ⛔ khong tai gi.
    #   Ban dau toi cam ca `url(` va bai DO ngay: dung lop *"phep do qua tho"*
    #   da tung bat nham `xmlns` o ban do tang. Chi cam dia chi **ra ngoai**.
    goi = re.findall(r'(?:href|src)\s*=\s*"[^"]*"|url\(\s*[\'"]?https?:', svg)
    assert not goi, f"⛔ SVG tai tai nguyen ngoai: {goi[:3]}"


def test_HINH_HOC_khong_TRAN_khung_va_khong_CHONG_nhau():
    svg = B.sinh_svg_khau(B.doc_bang())
    g = ET.fromstring(svg)
    vb = [float(x) for x in g.get("viewBox").split()]
    rong, cao = vb[2], vb[3]
    o = []
    for r in g.iter("{http://www.w3.org/2000/svg}rect"):
        x, y = float(r.get("x", 0)), float(r.get("y", 0))
        w, h = float(r.get("width")), float(r.get("height"))
        if w >= rong:                       # nen trang
            continue
        assert x >= 0 and y >= 0 and x + w <= rong + 0.5 and y + h <= cao + 0.5, \
            f"⛔ o TRAN khung: ({x},{y},{w},{h}) ngoai {rong}×{cao}"
        o.append((x, y, w, h))
    assert len(o) >= 23 + 6, f"⛔ chi thay {len(o)} o — thieu dai hay thieu chip"


def test_DAI_VIEC_chi_trai_duoi_B_va_C__be_rong_LA_phat_bieu():
    """⭐⭐ *"Cat ngang Ⓑ va Ⓒ"* duoc ve bang **BE RONG**, ⛔ khong bang mui ten.

    Neu dai `VIEC` bat dau o le trai thi ban ve dang noi *"cat ngang ca ba"* —
    mot cau **SAI**, va sai theo kieu ⛔ khong ai phat hien.
    """
    svg = B.sinh_svg_khau(B.doc_bang())
    g = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    dai = {}
    for el in g.iter(ns + "rect"):
        x, w = float(el.get("x", 0)), float(el.get("width"))
        if el.get("rx") == "10":
            dai.setdefault(round(x), []).append(w)
    x_b = B._KM + (B._KW + B._KG)
    assert x_b in dai, f"⛔ ⛔ khong thay dai nao bat dau o x cua Ⓑ ({x_b})"
    assert B._KM in dai, "⛔ ⛔ khong thay dai nao bat dau o le trai"
    phai = B._KM + 3 * B._KW + 2 * B._KG
    assert max(dai[x_b]) == pytest.approx(phai - x_b), \
        "⛔ dai VIEC ⛔ khong keo het toi bien phai cua Ⓒ"


def test_BO_TRI_tat_dinh__hai_lan_sinh_ra_HAI_BAN_GIONG_HET():
    b = B.doc_bang()
    assert B.sinh_svg_khau(b) == B.sinh_svg_khau(b)
    assert B.sinh_khau() == B.sinh_khau()


# ────────────────────────────── ban trong tai lieu ────────────────────
def test_BON_ban_ve_KHOP_ban_khai():
    """⭐ Cong that, dat trong bo test de mot cu `pytest` cung bat."""
    bang = B.doc_bang()
    ve_k = B.sinh_khau()
    assert B.MMD_KHAU.exists(), "⛔ thieu `ERD-KHAU.mmd`"
    assert B.MMD_KHAU.read_text(encoding="utf-8") == ve_k, \
        "⛔ `ERD-KHAU.mmd` lech — chay `python tools/sinh_ban_do_tang.py`"
    txt = B.DOC.read_text(encoding="utf-8")
    m = B.KHOI_KHAU.search(txt)
    assert m, "⛔ `BA-05` mat vung KHAU"
    assert m.group(0).rstrip("\n") == B.khoi_khau_md(bang, ve_k).rstrip("\n"), \
        "⛔ vung KHAU trong `BA-05` lech ban khai"


def test_khoi_TANG_phai_dung_TRUOC_vung_KHAU():
    """⛔⛔ Hai khoi cung la `flowchart`; phep thay khoi TANG an **cai dau
    tien**. Doi cho hai khoi ⇒ ghi de nham, va ⛔ khong gi bao."""
    txt = B.DOC.read_text(encoding="utf-8")
    assert B.KHOI.search(txt).start() < txt.index(B.MOC_DAU)


def test_MA_TRAN_tang_x_khau_cong_ve_dung_25():
    md = B.ma_tran_md(B.doc_bang())
    tong = re.findall(r"\*\*(\d+)\*\*", md.splitlines()[-1])
    assert tong[-1] == "25", f"⛔ ma tran ⛔ khong khep ve 25: {tong}"
    # ⭐ `23` → `24`: them khung xem `fls_may_goi_y` (migration `0025`,
    #   `QĐ-ITL-143`) — **toi biet minh vua them mot thuc the**
    # ⭐ `24` → `25`: them khung xem `fls_dien_giai` (migration `0026`,
    #   `QĐ-ITL-145`) — **toi biet minh vua them mot thuc the**
    assert sum(int(x) for x in tong[:-1]) == 25


def test_BANG_khau_liet_ke_DU_25_thuc_the():
    md = B.bang_khau_md(B.doc_bang())
    # ⭐ `23` → `24`: them khung xem `fls_may_goi_y` (migration `0025`,
    #   `QĐ-ITL-143`) — **toi biet minh vua them mot thuc the**
    # ⭐ `24` → `25`: them khung xem `fls_dien_giai` (migration `0026`,
    #   `QĐ-ITL-145`) — **toi biet minh vua them mot thuc the**
    assert md.count("| `fls_") == 25, "⛔ bang thieu thuc the"
