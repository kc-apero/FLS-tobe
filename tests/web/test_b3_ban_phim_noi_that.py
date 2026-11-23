# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ Ban phim co NOI vao `document` that ⛔ khong.

⛔⛔⛔ **Ba cong da xanh trong khi `0/9` phim dung duoc tren trinh duyet.**
   `phim()` cai du 9 phim, dung hanh vi — va `F01G.phim` chi duoc goi tu
   **hai dong cua chinh bo test**. Trong ca `fls/web/` ⛔ khong mot
   `addEventListener('keydown', ...)` nao tro toi no.

⭐⭐ **Bai thu voi tay VAO goi thu ma san pham phai voi tay RA noi.** ⇒ Bai
   nay **⛔ KHONG goi `F01G.phim`**. No **BAN mot su kien** qua `_ban`
   *(`khung_node.py`)* va do phan ung — dung duong mot nguoi go phim di.

⭐ Day la lan thu **ba** cung mot hinh dang sai lam trong ba ngay:
     ① khuon thu tu nhet `ST.dong`   ⇒ che mat *"⛔ chua ai goi cua"*
     ② khuon thu goi thang `phim`     ⇒ che mat *"⛔ chua ai noi ban phim"*
     ③ khuon thu goi thang `tim_focus` ⇒ che mat *"⛔ chua ai nghe o tim"*
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

#: ⚠ `screen on` — man dang BAT. Bai `test_phim_KHONG_an_vao_man_khac` dung
#: dung vo nay nhung bo chu `on` di.
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


def _hang(ma: str, tien: str = "1000.00") -> dict:
    """⚠ Ten CO Y la chu cai dau — tep nay la mot **ban se ra ngoai kho**."""
    return {"pm_line_id": ma, "the": {
        "ma_lenh": ma, "trang_thai": "chua_gan", "trang_thai_nhan": "Chưa gán",
        "trang_thai_mau": "", "loai_phieu": "Regular", "noi_dung": "TT " + ma,
        "so_tien": tien, "curr": "USD", "nguoi_nhan": "S. INC.",
        "so_chung_tu": None, "phap_nhan": "SGO2", "ngan_hang": "OCBC",
        "tai_khoan": "••4001", "cdt": "CVL | VisionLab", "nhom_du_truong": []}}


def _dat() -> str:
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [_hang("PM1-1"), _hang("PM2-1"), _hang("PM3-1")],
                      "next_cursor": None}}, ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};')


# ── ⓐ ⭐⭐⭐ NGUOI go phim thi man phai phan ung ─────────────────────────

def test_MUI_XUONG_di_chuyen_con_tro_khi_NGUOI_go_phim():
    """⛔ ⛔ Khong goi `F01G.phim` — ban mot `keydown` that."""
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " const truoc = F01G.ST.tro;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return {truoc, sau: F01G.ST.tro};",
              tep=TEP, vo=VO)
    assert r["truoc"] == 0
    assert r["sau"] == 1, (
        "⛔⛔ Gõ `↓` mà con trỏ ⛔ KHÔNG nhúc nhích — bàn phím ⛔ chưa nối vào "
        "`document`. Hàm `phim()` **có tồn tại** ⛔ không phải là nó **có chạy**.")


def test_MUI_PHAI_mo_lenh_dang_tro():
    r = _chay(_dat()
              + "_TRA['/queue/lenh/PM1-1/itl-candidates'] = {data: {ung_vien: []}};"
              "_TRA['/queue/lenh/PM1-1/so'] = {data: {ung_vien: []}};"
              " await F01G.mo_man();"
              " _ban('keydown', {key: 'ArrowRight'});"
              " await new Promise(r => setTimeout(r, 0));"
              " return F01G.ST.mo;",
              tep=TEP, vo=VO)
    assert r == "PM1-1", f"⛔ `→` ⛔ không mở lệnh đang trỏ, `ST.mo` = {r!r}"


# ── ⓑ ⭐⭐ MOT listener tren `document` nghe phim cua MOI man ───────────

def test_phim_KHONG_an_vao_man_khac_dang_bat():
    """⛔⛔ `man_f02.js` da phai dat dung phep chan nay.

    Thieu no thi go `j` o man `F02` se **doi lenh chi** o mot man ⛔ khong ai
    dang nhin — va man ay se lang le doi trang thai sau lung nguoi dung.
    """
    vo_tat = VO.replace("man.className = 'screen on';",
                        "man.className = 'screen';")
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " const truoc = F01G.ST.tro;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return {truoc, sau: F01G.ST.tro};",
              tep=TEP, vo=vo_tat)
    assert r["sau"] == r["truoc"], (
        "⛔⛔ Màn ⛔ KHÔNG bật mà vẫn ăn phím — nó đang **cướp bàn phím** của "
        "màn khác")


# ── ⓒ ⭐ NOI DUNG MOT LAN ──────────────────────────────────────────────

def test_noi_DUNG_MOT_lan_du_mo_man_nhieu_luot():
    """⛔ `mo_man` chay **moi lan doi tab** ⇒ ⛔ khong co co thi moi luot them
    mot listener, va mot cu go `↓` se nhay **n** buoc."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_man(); await F01G.mo_man();"
              " F01G.ST.tro = 0;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return F01G.ST.tro;",
              tep=TEP, vo=VO)
    assert r == 1, f"⛔ nối **{r}** lần — một cú `↓` nhảy **{r}** bước"
