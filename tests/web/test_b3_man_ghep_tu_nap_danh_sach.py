# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ Man **TU DI LAY** danh sach, ⛔ khong cho ai dut vao.

⛔⛔⛔ **Bai nay vá mot lo cua cong CHAY MA — cong ma chinh no vua vá mot lo
     cua cong QUET MA.** Ba tang, cung mot hinh dang sai lam.

  ① `test_b3_fe_bam_thiet_ke.py` **quet chu** ⇒ ⛔ khong thay `TP.el` tu bia.
  ② `test_b3_man_ghep_chay_duoc.py` **chay that** ⇒ bat duoc ① …
     ⛔ **nhung no tu nhet `ST.dong` vao truoc khi goi `ve()`**:

         F01G.ST.dong = <du lieu cua bai thu>;   // ← cho hong
         F01G.ve();

  ③ ⇒ Suot ca chang `B3`, `man_f01_ghep.js` **⛔ KHONG HE co mot dong nao nap
     danh sach**. Mo tren trinh duyet that, man luon hien *"Hàng chờ đã sạch."*
     — mot cau **sai** truoc `1.553` dong dang cho.

⭐⭐ **Mot khuon thu cung cap thu ma ban that phai tu di lay thi no CHE MAT
   cho thieu ay.** Bai nay vi the **⛔ KHONG gan `ST.dong`** mot lan nao: no
   chi dat san cua gia, roi bat man **tu goi**.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

#: ⭐ Khuon hang **dung nhu cua that tra** `22/09`: `the` la khuon 11 truong do
#: `fls/repo/man_ghep.py::khuon_the_lenh` dung — ⛔ khong phai mot hinh tuong
#: tuong. Phan con lai cua hang (`ro`, `hang`, `tho`…) giu nguyen de bai nay
#: cung do luon dieu *"man chi doc `the`, ⛔ khong moc `tho`"*.
def _hang(ma, tien="1000.00", curr="USD"):
    return {
        "pm_line_id": ma, "ro": "nguoi", "hang": 1, "amount": tien,
        "tho": {"Tên tài khoản": "⛔ man ⛔ KHONG duoc doc khoa nay"},
        "the": {
            "ma_lenh": ma, "trang_thai": "chua_gan",
            "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
            "loai_phieu": "Regular", "noi_dung": "Thanh toan " + ma,
            "so_tien": tien, "curr": curr, "nguoi_nhan": "S. INC.",
            "so_chung_tu": None, "phap_nhan": "SGO2", "ngan_hang": "OCBC",
            "tai_khoan": "••4001", "cdt": "CVL | VisionLab",
            "nhom_du_truong": [],
        },
    }


D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"
D_KHONG = "/queue/lenh-cho?ro=khong&limit=500"


def _dat(bang) -> str:
    return "".join(
        "_TRA[" + json.dumps(d) + "] = "
        + json.dumps({"data": t}, ensure_ascii=False) + ";"
        for d, t in bang.items())


# ── ⓐ ⭐⭐⭐ man TU GOI CUA, ⛔ khong cho ai dut du lieu ──────────────────

def test_man_TU_GOI_cua_lenh_cho_khi_mo():
    r = _chay(
        _dat({D_NGUOI: {"rows": [_hang("PM1-1")], "next_cursor": None},
              D_MAY: {"rows": [_hang("PM2-1")], "next_cursor": None}})
        + " await F01G.mo_man();"
        " return {duong: _GOI.map(g => g[1]),"
        "         dong: F01G.ST.dong.length,"
        "         rail: document.querySelectorAll('.mrow').length};",
        tep=TEP, vo=VO)
    assert D_NGUOI in r["duong"], (
        "⛔⛔ Man ⛔ KHONG goi cua nao de lay danh sach — do dung la loi da song "
        f"suot chang `B3`. Da goi: {r['duong']}")
    assert r["dong"] == 2, r
    assert r["rail"] == 2, "⛔ danh sach ⛔ khong ra man"


def test_chip_CHUA_GAN_gop_DU_HAI_cua():
    """⭐ Do `22/09` tren kho that: `ro=nguoi` **535** ＋ `ro=may&tu_chung=0`
    **203** = **738** — dung con so `G-a` cua `CR#12`. Thieu mot cua la thieu
    mot phan ba viec, va man **⛔ khong keu** mot tieng nao."""
    r = _chay(
        _dat({D_NGUOI: {"rows": [_hang("PM1-1")], "next_cursor": None},
              D_MAY: {"rows": [_hang("PM2-1")], "next_cursor": None}})
        + " await F01G.mo_man();"
        " return _GOI.filter(g => g[0] === 'doc').map(g => g[1]);",
        tep=TEP, vo=VO)
    assert D_NGUOI in r and D_MAY in r, f"⛔ thieu mot cua: {r}"


# ── ⓑ ⭐⭐ LAT TRANG — cua chan `limit` o 500, ro `khong` co 768 ──────────

def test_LAT_TRANG_den_het_chu_KHONG_dung_o_trang_dau():
    """⛔⛔ Ro `khong` co **768** dong ma cua chan `limit=500` ⇒ lay trang dau
    roi thoi la **mat 268 dong**, va `lenh_ke_tiep` se **im lang dung** giua
    chung. Mot danh sach cut ⛔ khong trong khac gi mot danh sach du."""
    r = _chay(
        _dat({D_KHONG: {"rows": [_hang("PM1-1")], "next_cursor": "c2"},
              D_KHONG + "&cursor=c2": {"rows": [_hang("PM2-1")],
                                       "next_cursor": None}})
        + " await F01G.doi_chip('khong_gan_duoc');"
        " return {dong: F01G.ST.dong.length,"
        "         duong: _GOI.filter(g => g[0] === 'doc').map(g => g[1])};",
        tep=TEP, vo=VO)
    assert r["dong"] == 2, (
        f"⛔⛔ man dung o trang dau — chi cam {r['dong']} dong. {r['duong']}")
    assert D_KHONG + "&cursor=c2" in r["duong"], r["duong"]


# ── ⓒ ⭐⭐⭐ CHIP ⛔ CHUA CO CUA phai NOI RA ──────────────────────────────

def test_chip_KHONG_co_cua_thi_NOI_RA_chu_KHONG_ve_danh_sach_rong():
    """⛔⛔ Chip `Tat ca` la **HOP** cua hai ro, va gop hai cua o man thi con
    so `x/y` se do **man tu cong** — tuc mot **so cua may** (`UI-F8`).
    ⇒ `GAP-SCR-26`, va cho ay den nay van **⛔ chua co cua**.

    ⚠ `22/09`: chip `da_gan` **da co cua** *(tuyen 40)*, nen bai nay chuyen
      sang do chip con lai. ⭐ Mot bai thu do mot cho **da duoc va** thi no
      ⛔ khong con canh gi — no chi con **xanh**.

    ⭐ Mot danh sach rong doc **y het** *"da xong het"*. De man ve mot danh
      sach rong o day la de **may tra loi thay nguoi** (`INV-I16`) — va cau
      tra loi ay **sai**.
    """
    r = _chay(
        " await F01G.doi_chip('tat_ca');"
        " return {goi: _GOI.length, thieu: F01G.ST.thieu_cua,"
        "         chu: document.querySelector('#ghep-goc').textContent,"
        "         rail: document.querySelectorAll('.mrow').length};",
        tep=TEP, vo=VO)
    assert r["thieu"] is True
    assert r["goi"] == 0, "⛔ goi bua mot cua khac de co cai ma ve"
    assert "Chưa có cửa" in r["chu"], r["chu"]
    assert "sạch" not in r["chu"], (
        "⛔⛔ man dang noi *'hàng chờ đã sạch'* trong khi no chi **⛔ chua hoi**")


# ── ⓓ ⭐⭐ CUA LOI ⛔ KHONG duoc trong nhu "da sach" ─────────────────────

def test_cua_LOI_hien_ra_loi_chu_KHONG_hien_hang_cho_da_sach():
    r = _chay(
        "_TRA[" + json.dumps(D_NGUOI) + "] = {no: new Error('kho ⛔ khong tra loi')};"
        " await F01G.mo_man();"
        " return {loi: F01G.ST.loi,"
        "         chu: document.querySelector('#ghep-goc').textContent};",
        tep=TEP, vo=VO)
    assert r["loi"], "⛔ loi bi nuot"
    assert "Cửa lỗi" in r["chu"], r["chu"]
    assert "sạch" not in r["chu"], (
        "⛔⛔ mot cua HONG dang doc nhu mot **thanh tuu**")


# ── ⓔ ⭐⭐ man doc `the`, ⛔ KHONG moc `tho` ─────────────────────────────

def test_man_KHONG_DUOC_moc_ten_cot_Google_Sheets():
    """⛔⛔ **6/11** truong cua the chi song trong tui `tho`, khoa theo **ten
    cot cua sheet**. Neu JS tu moc `tho["Tên tài khoản"]` thi ngay sheet doi
    ten cot, man **im lang** rong mot o — ⛔ khong bai thu nao bat duoc, vi bai
    thu se go y het ten ay. ⇒ Phep anh xa o **tang doc**, va bai nay canh cho
    JS ⛔ khong moc lai.

    ⛔⛔ **Ban dau bai nay quet CHUOI ten cot, va no BAO OAN ngay**: `'Ngân
       hàng'` co trong JS — nhung la mot **nhan hien thi** tren the, ⛔ khong
       phai mot phep moc khoa. Day la lan thu **tu** cung mot hinh dang sai:
       `pay_type` trong chu thich · `#f01-ghep` doc thanh mau · `var(--x)`
       trong cau van ta chinh cong ay.

    ⭐ Do **PHEP TRUY CAP** chu ⛔ dung do **CHUOI**: cai bi cam la *doc tui
      `tho`*, va no co dung mot hinh dang cu phap.
    """
    import io
    import pathlib
    import re
    js = (pathlib.Path(__file__).resolve().parents[2]
          / "fls" / "web" / "tep" / "man_f01_ghep.js")
    ma = io.open(js, encoding="utf-8").read()
    ma = re.sub(r"/\*[\s\S]*?\*/", "", ma)
    ma = re.sub(r"(?m)^\s*//.*$", "", ma)
    xau = [f"dong {ma[:m.start()].count(chr(10)) + 1}: {m.group(0)}"
           for m in re.finditer(r"\.tho\b|\btho\s*\[|\[\s*['\"]tho['\"]\s*\]", ma)]
    assert xau == [], (
        "⛔ JS dang doc tui `tho` — do la ten cot cua Google Sheets. Dua phep "
        "anh xa ve `fls/repo/man_ghep.py::khuon_the_lenh`:\n  "
        + "\n  ".join(xau))


def test_cong_TREN_do_khi_JS_moc_tui_tho():
    """⭐ Mot cong ⛔ chua bao gio thay mau do la mot cong ⛔ chua ai do."""
    import re
    bay = "const ten = r.tho['Tên tài khoản'];"
    assert re.search(r"\.tho\b|\btho\s*\[", bay)
    assert not re.search(r"\.tho\b|\btho\s*\[", "const t = r.the.nguoi_nhan;")
