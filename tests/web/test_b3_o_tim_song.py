# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐ O tim giao dich co SONG ⛔ khong.

⛔⛔ `#ghep-tim` co trong vo tu `21/09` va trong ca `fls/web/` no xuat hien
   dung **hai** cho: dong khai o `index.html`, va `tim_focus()` nhay vao no.
   ⛔ Khong mot `oninput` nao ⇒ `ST.tim` **vinh vien** `''`, va cua
   `/queue/lenh/{pm}/so?q=` — da cai day du o `man_ghep.py` — **⛔ chua bao
   gio duoc goi voi mot chu nao**.

⭐⭐ Mot o nhap **chi duoc nhay vao ma ⛔ khong duoc doc** con **te hon** mot o
   ⛔ khong co: no **MOI** nguoi ta go, roi ⛔ khong lam gi ca.

⭐ Bai nay ban su kien `input` **that**, ⛔ khong gan thang `ST.tim`.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
man.className = 'screen on';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"

UV = {"itl_id": 42, "doc_date": "2026-09-18", "doc_no": "1026946429",
      "dien_giai": "Card charge OPENAI", "amount": "1000.00", "chieu": "co",
      "curr": "USD", "nguon": {"tk": "PO2", "bank": "OCBC", "curr": "USD",
                               "le": "SGO2"}, "bac": "ma", "lech": None}

#: ⚠ Ten CO Y la chu cai dau — tep nay la mot **ban se ra ngoai kho**.
THE = {"ma_lenh": "PM1-1", "trang_thai": "chua_gan",
       "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
       "loai_phieu": "Regular", "noi_dung": "TT PM1-1", "so_tien": "1000.00",
       "curr": "USD", "nguoi_nhan": "S. INC.", "so_chung_tu": None,
       "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
       "cdt": "CVL | VisionLab", "nhom_du_truong": []}


def _dat() -> str:
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [{"pm_line_id": "PM1-1", "the": THE}],
                      "next_cursor": None}}, ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};'
        "_TRA['/queue/lenh/PM1-1/itl-candidates'] = "
        "  {data: {ung_vien: " + json.dumps([UV], ensure_ascii=False) + "}};"
        "_TRA['/queue/lenh/PM1-1/so?q=OPENAI'] = "
        "  {data: {ung_vien: " + json.dumps([UV], ensure_ascii=False) + "}};")


# ── ⓐ ⭐⭐⭐ GO thi cua PHAI duoc goi kem chu ────────────────────────────

def test_GO_vao_o_tim_thi_cua_SO_duoc_goi_kem_chu():
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI';"
              " _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 60));"
              " return {tim: F01G.ST.tim,"
              "         duong: _GOI.filter(g => g[0] === 'doc').map(g => g[1])};",
              tep=TEP, vo=VO)
    assert r["tim"] == "OPENAI", (
        f"⛔⛔ Gõ vào ô tìm mà `ST.tim` vẫn {r['tim']!r} — ô tìm ⛔ chưa nối")
    assert "/queue/lenh/PM1-1/so?q=OPENAI" in r["duong"], (
        f"⛔ cửa tra sổ ⛔ không được gọi kèm chữ. Đã gọi: {r['duong']}")


# ── ⓑ ⭐⭐ GO = bat TOAN SO (loi bat bang tay ma `§8` doi) ───────────────

def test_GO_bat_san_TOAN_SO():
    """⭐ Day cung la **loi bat Toan so bang tay** ma hop dong `§8` doi va man
    hien ⛔ khong co — `ST.toan_so` moi chi TU bat khi `ung_vien` rong."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const truoc = F01G.ST.toan_so;"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI'; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 60));"
              " return {truoc, sau: F01G.ST.toan_so};",
              tep=TEP, vo=VO)
    assert r["truoc"] is False and r["sau"] is True


# ── ⓒ ⭐⭐ GO NHANH chi goi cua MOT lan ─────────────────────────────────

def test_GO_NHANH_chi_goi_cua_MOT_lan():
    """⛔⛔ ⛔ Khong cho tre thi go `OPENAI` = **6** luot goi cua, va luot ve
    sau co the tra loi **TRUOC** luot ve truoc ⇒ danh sach nhap nhay roi
    **dung lai o ket qua cua mot chuoi chu DA CU**."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " const n0 = _GOI.length;"
              " for (const c of ['O','OP','OPE','OPEN','OPENA','OPENAI']) {"
              "   t.value = c; _ban('input', {target: t}); }"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 80));"
              " return _GOI.slice(n0).filter(g => g[1].indexOf('/so') >= 0).length;",
              tep=TEP, vo=VO)
    assert r == 1, f"⛔ gõ 6 ký tự ⇒ **{r}** lượt gọi cửa, phải là **1**"


# ── ⓓ ⭐ XOA HET chu ⇒ co duong LUI ────────────────────────────────────

def test_XOA_HET_chu_thi_ve_lai_ung_vien_MAY_de_xuat():
    """⛔ Xoa het ma van o Toan so la **⛔ khong co duong lui**."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI'; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 60));"
              " t.value = ''; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 60));"
              " return {tim: F01G.ST.tim, toan_so: F01G.ST.toan_so};",
              tep=TEP, vo=VO)
    assert r["tim"] == "" and r["toan_so"] is False
