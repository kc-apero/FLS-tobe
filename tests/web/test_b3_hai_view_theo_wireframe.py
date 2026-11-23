# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ HAI VIEW, dung wireframe: **bang so** ⇄ **rail ＋ ban lam viec**.

Hop dong `§4`: *"Chua mo lenh nao: mot bang so day du chiem toan bo be ngang.
Da mo: bang thu ve rail `clamp(300px,26vw,380px)`, phan con lai la ban lam
viec."*

⛔⛔ **Man `21/09`→`22/09` chi co MOT view** — luon la rail ＋ ban lam viec, ke
   ca khi ⛔ chua chon gi. Tuc luc mo man, phan lon be ngang la mot cau *"Chon
   mot lenh chi ben trai"*, con danh sach bi nen vao mot cot `380px` **⛔ khong
   du cho** cho `Ngay`·`Loai`·`CDT`·`So CT`.

⭐ Bang cho nguoi **QUET** ca tram dong; rail cho nguoi **dang lam mot dong**.
  Hai viec khac nhau ⇒ hai hinh. Bai nay canh cho chung ⛔ khong nhap lai lam
  mot — va do la thu **da xay ra mot lan**.
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

#: ⚠ Ten CO Y la chu cai dau — tep nay la mot **ban se ra ngoai kho**.
def _the(ma, **doi):
    t = {"ma_lenh": ma, "ngay": "18/09", "trang_thai": "chua_gan",
         "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
         "loai_phieu": "Regular", "noi_dung": "TT " + ma, "so_tien": "990.00",
         "curr": "USD", "nguoi_nhan": "S. INC.", "so_chung_tu": "CT88213",
         "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
         "cdt": "CVL | VisionLab", "nhom_du_truong": []}
    t.update(doi)
    return t


GD_DA_GAN = {"itl_id": 42, "doc_date": "18/09/2026", "doc_no": "CT88213",
             "dien_giai": "FUNDS TRF TT 1OR606160155C01", "amount": "990.00",
             "curr": "USD", "chieu": "co", "bac": "ma", "lech": None,
             "nguon": {"tk": "••4001", "bank": "OCBC", "curr": "USD",
                       "le": "SGO2"},
             "da_gan": True}
GD_DE_XUAT = dict(GD_DA_GAN, da_gan=False, bac="gan_tien")


def _dat(rows) -> str:
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": rows, "next_cursor": None}},
            ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};')


def _hang(ma, gd=None, **doi):
    """⭐ `gd` nam **TRONG** `the` — dung khuon cua that tra.

    ⛔⛔ Ban dau khuon gia nay dat `gd` o **tang hang**, va bai thu DO: man doc
       `r.the` roi bo phan con lai ⇒ `gd` **roi mat tren duong**. Loi that nam
       o cua *(da vá: `_gd_vao_the`)*, nhung khuon gia cung phai **soi dung
       ban that** — mot khuon gia sai hinh thi bai thu do mot man ⛔ khong ton
       tai.
    """
    return {"pm_line_id": ma, "the": dict(_the(ma, **doi), gd=gd)}


# ── ⓐ ⭐⭐⭐ VIEW ① — ⛔ chua mo lenh nao ⇒ BANG SO ─────────────────────

def test_CHUA_mo_lenh_nao_thi_ve_BANG_SO_chu_KHONG_rail():
    r = _chay(_dat([_hang("PM1-1"), _hang("PM2-1")])
              + " await F01G.mo_man();"
              " return {bang: document.querySelectorAll('.mtable').length,"
              "         rail: document.querySelectorAll('.rail').length,"
              "         dong: document.querySelectorAll('.mtable .mrow').length};",
              tep=TEP, vo=VO)
    assert r["bang"] == 1, (
        "⛔⛔ ⛔ Chưa mở lệnh nào mà ⛔ KHÔNG có bảng sổ — hợp đồng `§4` đòi "
        "**một bảng đầy đủ chiếm toàn bộ bề ngang**")
    assert r["rail"] == 0, (
        "⛔ Rail hiện khi ⛔ chưa mở lệnh nào — nó nén danh sách vào `380px` "
        "và **⛔ không đủ chỗ** cho `Ngày`·`Loại`·`CDT`·`Số CT`")
    assert r["dong"] == 2


def test_BANG_co_DU_MUOI_MOT_cot():
    """⛔ Bo mot cot la bo mot cau hoi ke toan dang hoi — va ⛔ khong ai thay
    minh mat cau nao. ⇒ So cot phai duoc **mot bai thu** giu lai.

    ⚠ `23/09` owner bo cot `Bac` *(`12`⇒`11`)* — mot **quyet dinh**, ⛔ khong
      mot lan truot. Bac van song tren tung dong ung vien (`①②③④`), dung cho
      nguoi **dang chon**; bai `test_BAC_VAN_CON_tren_dong_ung_vien` giu no.
      ⛔ Con so o day doi theo owner, ⛔ **khong** theo ban dung."""
    r = _chay(_dat([_hang("PM1-1")])
              + " await F01G.mo_man();"
              " return {khai: F01G.COT_BANG.length,"
              "         dau: document.querySelector('.mhead').children.length,"
              "         o: document.querySelectorAll('.mtable .mrow')[0]"
              "             .children.length};",
              tep=TEP, vo=VO)
    assert r["khai"] == 11, f"⛔ khai **{r['khai']}** cột, phải có **11**"
    assert r["dau"] == 11, f"⛔ hàng tiêu đề có **{r['dau']}** ô"
    assert r["o"] == 11, (
        f"⛔⛔ Một dòng có **{r['o']}** ô mà tiêu đề có **11** — lưới sẽ "
        "**trượt cột** và mọi con số đọc sang nhãn bên cạnh")


# ── ⓑ ⭐⭐ VIEW ② — mo mot lenh ⇒ rail ＋ ban lam viec ─────────────────

def test_MO_mot_lenh_thi_doi_sang_RAIL_va_BO_bang():
    r = _chay(_dat([_hang("PM1-1"), _hang("PM2-1")])
              + "_TRA['/queue/lenh/PM1-1/itl-candidates'] = {data: {ung_vien: []}};"
              "_TRA['/queue/lenh/PM1-1/so'] = {data: {ung_vien: []}};"
              " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " return {bang: document.querySelectorAll('.mtable').length,"
              "         rail: document.querySelectorAll('.rail').length,"
              "         rrow: document.querySelectorAll('.rrow').length,"
              "         work: document.querySelectorAll('.work').length};",
              tep=TEP, vo=VO)
    assert r["bang"] == 0, "⛔ bảng vẫn còn khi đã mở vùng ghép"
    assert r["rail"] == 1 and r["work"] == 1
    assert r["rrow"] == 2, "⛔ rail ⛔ không chở đủ dòng"


def test_RAIL_moi_muc_co_BA_DONG_dung_ban_dung():
    """⭐ `l0` *(ngày · mã · loại ∣ chip TT)* / `l1` *(nội dung ∣ tiền)* / `cdt`.

    ⛔ Bản `22/09` chỉ có **3 mục một dòng** ⇒ mất `Ngày`, `Loại`, chip trạng
    thái và `CDT` — người đang ghép phải **mở từng dòng ra mới biết dòng nào
    đáng mở**.
    """
    r = _chay(_dat([_hang("PM1-1")])
              + "_TRA['/queue/lenh/PM1-1/itl-candidates'] = {data: {ung_vien: []}};"
              "_TRA['/queue/lenh/PM1-1/so'] = {data: {ung_vien: []}};"
              " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const x = document.querySelectorAll('.rrow')[0];"
              " return {l0: x.querySelectorAll('.l0').length,"
              "         l1: x.querySelectorAll('.l1').length,"
              "         cdt: x.querySelectorAll('.cdt').length,"
              "         ngay: x.querySelectorAll('.d').length,"
              "         chip: x.querySelectorAll('.chip').length};",
              tep=TEP, vo=VO)
    assert r["l0"] == 1 and r["l1"] == 1 and r["cdt"] == 1, r
    assert r["ngay"] == 1, "⛔ rail mất cột **Ngày**"
    assert r["chip"] == 2, (
        f"⛔ rail phải có **2** chip *(loại ＋ trạng thái)*, đếm được {r['chip']}")


# ── ⓒ ⭐⭐ O `Giao dich da gan` noi NAM cau khac nhau ──────────────────

def test_DE_XUAT_va_DA_CHOT_KHONG_duoc_trong_giong_nhau():
    """⛔⛔ `§6.3` cua hop dong: *"de xuat ≠ da gan"* phai doc duoc **bang
    hinh**, ⛔ khong bang chu nho."""
    r = _chay(_dat([_hang("PM1-1", GD_DA_GAN, trang_thai="da_gan"),
                    _hang("PM2-1", GD_DE_XUAT)])
              + " await F01G.mo_man();"
              " const g = document.querySelectorAll('.gd');"
              " return {lop: [g[0].className, g[1].className],"
              "         chu: [g[0].textContent, g[1].textContent]};",
              tep=TEP, vo=VO)
    assert "de-xuat" not in r["lop"][0], "⛔ dòng ĐÃ CHỐT bị vẽ như đề xuất"
    assert "de-xuat" in r["lop"][1], "⛔ dòng ĐỀ XUẤT trông y hệt dòng đã chốt"
    assert "đề xuất:" in r["chu"][1] and "đề xuất:" not in r["chu"][0]


def test_KHONG_GAN_DUOC_noi_RO_vi_sao_chu_KHONG_de_trong():
    """⭐ `768` dòng. ⛔ Một ô trống ở đây đọc y hệt *"⛔ chưa ai xem"*."""
    r = _chay(_dat([_hang("PM1-1", None, trang_thai="khong_gan_duoc")])
              + " await F01G.mo_man();"
              " return document.querySelectorAll('.mtable .mrow')[0].textContent;",
              tep=TEP, vo=VO)
    assert "sổ không có số tiền này" in r, r


def test_LOI_NGUON_noi_ra_chu_KHONG_lam_SAP_bang():
    """⛔⛔ `tach_nguon` **NÉM** khi `source_sheet` sai khuôn — đúng ở tầng
    đọc. ⛔ Nhưng ở một **danh sách**, một ngoại lệ sẽ trả `500` cho cả trang
    ⇒ kế toán mất **cả `738` dòng** vì **một** dòng."""
    r = _chay(_dat([_hang("PM1-1", {"loi_nguon": "khuôn lạ", "itl_id": 9})])
              + " await F01G.mo_man();"
              " return {dong: document.querySelectorAll('.mtable .mrow').length,"
              "         chu: document.querySelectorAll('.mtable .mrow')[0].textContent};",
              tep=TEP, vo=VO)
    assert r["dong"] == 1, "⛔ một dòng hỏng làm **mất cả bảng**"
    assert "không đọc được nguồn" in r["chu"], r["chu"]


# ── ⓓ ⭐ Cau goi y phim DOI theo view ─────────────────────────────────

def test_cau_goi_y_phim_DOI_theo_view():
    """⛔ Một câu đứng yên sẽ nói **sai đúng một nửa** số lần người ta đọc."""
    kb = (_dat([_hang("PM1-1")])
          + "_TRA['/queue/lenh/PM1-1/itl-candidates'] = {data: {ung_vien: []}};"
          "_TRA['/queue/lenh/PM1-1/so'] = {data: {ung_vien: []}};"
          " await F01G.mo_man();"
          " const a = document.querySelector('.goi-phim').textContent;"
          " await F01G.mo_lenh('PM1-1');"
          " const b = document.querySelector('.goi-phim').textContent;"
          " return {a, b};")
    r = _chay(kb, tep=TEP, vo=VO)
    assert "mở vùng ghép" in r["a"], r["a"]
    assert "về bảng sổ" in r["b"], r["b"]
    assert r["a"] != r["b"]
