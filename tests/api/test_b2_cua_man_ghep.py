# -*- coding: utf-8 -*-
"""`B2` — CUA cua man GAN LENH CHI: khuon `ung_vien[]` + hai tuyen moi.

⭐⭐⭐ `QĐ-ITL-148` · dac ta `BA-07 §4h`.

⛔⛔ **Cho te nhat duoc lap:** `§4g ⓹` khai `itl-candidates` tra `ung_vien[]`
   roi **dung** — **`0`** truong. Nguoi dung ban dung ⛔ khong co gi de nhan
   ngoai mot chuoi, nen ho **CAT CHUOI hien thi** de lay lai cau truc:

       meta = "18/09 · OCBC · ••4001 · SGO2 · CT#88213"
       parts = meta.split(" · ")        ⇒ cau truc GIA

   ⇒ Khuon duoi day la thu thay the no.
"""
from __future__ import annotations

import datetime as dt
from decimal import Decimal as D

import pytest

from fls.api.bang_tuyen import BANG_TUYEN
from fls.api.xu_ly import HAM
from fls.repo import man_ghep

MUOI_TRUONG = ("itl_id", "doc_date", "doc_no", "dien_giai", "amount",
               "chieu", "curr", "nguon", "bac", "lech")


#: ⭐ `WO-032`: dòng lệnh của cửa — `khuon_ung_vien` tính `lech` so với nó.
_LENH = {"amount": D("990.00"), "curr": "USD"}


def _tho(**kw):
    """Mot hang ung vien THO nhu `lenh_cho.ung_vien_itl` dang tra."""
    d = {"itl_id": 4242, "doc_date": dt.date(2026, 9, 18), "doc_no": "CT#88213",
         "curr": "USD", "tien": D("990.00"), "bac": "ma",
         "lech_tuyet_doi": None, "source_sheet": "R | PO2_OCBC USD_SGO2",
         "ps_no": None, "ps_co": D("990.00"), "dien_giai": "Card charge (OPENAI)"}
    d.update(kw)
    return d


# ── ⓐ khuon `ung_vien[]` — **10** truong ────────────────────────────────

def test_khuon_co_DU_MUOI_truong():
    r = man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)
    assert tuple(r) == MUOI_TRUONG, tuple(r)


def test_nguon_la_OBJECT_chu_KHONG_phai_chuoi():
    """⛔⛔ Ban dung cat chuoi hien thi de lay lai `bank`/`tk`/`le`.

    ⭐ Mot chuoi da ghep roi thi tang duoi **⛔ khong the** bo bot cot khi man
      hep — ma luat hy sinh cot *(Nguon → So CT → ⛔ khong bao gio Dien giai)*
      doi dung dieu do.
    """
    r = man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)
    assert r["nguon"] == {"tk": "••", "bank": "OCBC", "curr": "USD",
                          "le": "SGO2"} or isinstance(r["nguon"], dict)
    assert isinstance(r["nguon"], dict), "⛔ `nguon` van la chuoi"
    assert set(r["nguon"]) == {"tk", "bank", "curr", "le"}


def test_nguon_giu_tai_khoan_THE_nguyen_ven():
    r = man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)
    assert r["nguon"]["tk"] == "PO2", "⛔ `PO2` la tai khoan THE, ⛔ khong cat"


def test_nguon_so_dai_thi_che_con_4_so_cuoi():
    r = man_ghep.khuon_ung_vien(_tho(source_sheet="R | 358468128_VPB VND_VGOH"), lenh=_LENH)
    assert r["nguon"]["tk"] == "••8128"


def test_chieu_duoc_TINH_chu_KHONG_lay_tu_cot_nao():
    assert man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)["chieu"] == "co"
    assert man_ghep.khuon_ung_vien(
        _tho(ps_no=D("990.00"), ps_co=None), lenh=_LENH)["chieu"] == "no"


def test_itl_id_CO_trong_khuon_nhung_la_de_GUI_LAI_khong_phai_de_HIEN():
    """⭐ `UI-F8` cam `*_id` len man. Cua **phai** tra — man **⛔ khong in**.

    ⇒ Ranh gioi la *"cua tra ≠ man in"* (`QĐ-ITL-142`), ⛔ khong phai bo truong.
    """
    assert "itl_id" in man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)


# ── ⓑ `dien_giai` — `null` mang HAI nghia ───────────────────────────────

def test_dien_giai_CO_chu_thi_KHONG_kem_vi_sao():
    r = man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)
    assert r["dien_giai"] == "Card charge (OPENAI)"
    assert r.get("dien_giai_vi_sao") is None


def test_dien_giai_RONG_khac_CHUA_NOI_DUOC():
    """⛔⛔ Do `21/09`: **3** dong noi duoc ma ⛔ khong chu · **26** dong ⛔ khong
    noi duoc. Gop hai thu thanh mot `null` la dung thu `INV-I16` cam.
    """
    a = man_ghep.khuon_ung_vien(_tho(dien_giai=None, noi_duoc=True), lenh=_LENH)
    b = man_ghep.khuon_ung_vien(_tho(dien_giai=None, noi_duoc=False), lenh=_LENH)
    assert a["dien_giai"] is None and b["dien_giai"] is None
    assert a["dien_giai_vi_sao"] == "rong"
    assert b["dien_giai_vi_sao"] == "chua_noi_duoc"
    assert a["dien_giai_vi_sao"] != b["dien_giai_vi_sao"], (
        "⛔ *'giao dich nay ⛔ khong co noi dung'* va *'FLS ⛔ chua doc duoc'* "
        "la HAI cau khac nhau")


# ── ⓒ do lech ─────────────────────────────────────────────────────────

def test_khop_tuyet_doi_thi_lech_la_KHONG_null_ma_0():
    """⭐ *(`WO-032` — viết lại theo `BA-07` **v3.7** §4h ⓵, lo gốc **giữ**:
    *"khớp tuyệt đối thì cửa nói gì ở `lech`"*)*. ⛔ Bản cũ ghim `None` theo
    chữ v3.6 *"`null` khi khớp tuyệt đối"* — `BA-07` v3.7 **gạch** câu ấy:
    khớp tuyệt đối ⇒ **`0`**; `null` chỉ còn nghĩa *"⛔ so được"* *(khác tiền
    tệ / thiếu số)*. Lý do đổi ở changelog v3.7: `null` ở bậc `ma` che **338 /
    448** lệch thật *(`KQ-031 F-2`)*."""
    assert man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)["lech"] == D("0")


def test_lech_tien_thi_CO_so():
    """⭐ `WO-032`: `lech` = `|amount ứng viên − amount lệnh|` *(tính bằng
    `lech_ung_vien`, ⛔ còn đọc `lech_tuyet_doi` của SQL)* — ở **mọi** bậc."""
    for bac in ("ma", "gan_tien"):
        r = man_ghep.khuon_ung_vien(_tho(bac=bac),
                                    lenh={"amount": D("1002.40"), "curr": "USD"})
        assert r["lech"] == D("12.40"), (bac, r["lech"])


def test_lech_KHAC_TIEN_TE_hay_THIEU_SO_thi_null():
    """⭐ `BA-07` v3.7: `null` ⇔ ⛔ so được. ⛔ Hai đơn vị ⛔ trừ nhau
    *(`QĐ-ITL-62`)*: `990 USD` ↔ lệnh `990 VND` ⇒ `None`, ⛔ `0`."""
    k = man_ghep.khuon_ung_vien
    assert k(_tho(), lenh={"amount": D("990"), "curr": "VND"})["lech"] is None
    assert k(_tho(), lenh={"amount": None, "curr": "USD"})["lech"] is None
    assert k(_tho(curr=None), lenh=_LENH)["lech"] is None
    # ⭐ so mã sau `trim` + chữ hoa — một luật ở mọi cửa *(`WO-032` Rủi ro 2)*
    assert k(_tho(curr=" usd "), lenh=_LENH)["lech"] == D("0")


# ── ⓓ hai tuyen moi — **35 → 37** ───────────────────────────────────────

def _tuyen(duong: str):
    return [t for t in BANG_TUYEN if t.duong.endswith(duong)]


def test_tuyen_36_TRA_CUU_TOAN_SO_co_mat():
    """⭐ Loi thoat ngo cut cua **768** dong — ⛔ khong phai tinh nang phu."""
    t = _tuyen("/queue/lenh/{pm_line_id}/so")
    assert t, "⛔ thieu tuyen tra cuu TOAN SO"
    assert t[0].phuong_thuc == "GET"
    assert t[0].ham in HAM, f"⛔ ham `{t[0].ham}` ⛔ chua duoc ghi danh"


def test_tuyen_37_CHUM_co_mat():
    t = _tuyen("/queue/{itl_id}/chum")
    assert t, "⛔ thieu tuyen CHUM ⇒ man ⛔ khong noi ra duoc thiet hai"
    assert t[0].phuong_thuc == "GET"
    assert t[0].ham in HAM, f"⛔ ham `{t[0].ham}` ⛔ chua duoc ghi danh"


def test_hai_tuyen_moi_KHONG_GHI_gi():
    for d in ("/queue/lenh/{pm_line_id}/so", "/queue/{itl_id}/chum"):
        t = _tuyen(d)[0]
        assert not t.bang_ghi, f"⛔ `{d}` la cua DOC, ⛔ khong duoc ghi"


@pytest.mark.parametrize("duong", ["/queue/lenh/{pm_line_id}/so",
                                   "/queue/{itl_id}/chum"])
def test_tuyen_moi_khai_du_bang_no_cham(duong):
    """⭐ `soi_bang_tuyen` doi moi tuyen khai **cac bang no cham**."""
    assert _tuyen(duong)[0].bang, "⛔ thieu ban khai bang"


# ── ⓖ ⭐⭐ `source_sheet` sai khuon: NOI RA, ⛔ khong NEM ────────────────

def test_KHUON_source_sheet_sai_thi_NOI_RA_chu_KHONG_nem():
    """⛔⛔⛔ `tach_nguon` **NEM** khi `source_sheet` sai khuon — dung o tang
    doc: may ⛔ khong duoc doan (`INV-I16`).

    ⛔ Nhung `khuon_ung_vien` chay tren **tung dong cua mot DANH SACH**, va
      mot ngoai le o day tra `500` cho **ca trang** ⇒ ke toan mat **50 ung
      vien** vi **mot**. Da vap dung loi nay o cua danh sach lenh chi `22/09`.

    ⭐ `nguon=None` ＋ `loi_nguon` — mot trang thai **da co ten** o `DUONG_RA`.
      Va no **giu lai** `dien_giai` va `amount`, tuc nguoi ta van doc duoc
      **bang chung** du ⛔ khong biet dong tien ay tu tai khoan nao.
    """
    r = man_ghep.khuon_ung_vien(_tho(source_sheet="L1"), lenh=_LENH)
    assert r["nguon"] is None
    assert "L1" in r["loi_nguon"]
    # ⭐ Bang chung ⛔ KHONG duoc mat theo
    assert r["amount"] == D("990.00")
    assert r["dien_giai"] == "Card charge (OPENAI)"


def test_KHUON_source_sheet_DUNG_thi_KHONG_co_loi_nguon():
    """⛔ Mot khoa `loi_nguon` luon co mat *(du la `None`)* se day tang tren
    vao thoi quen **kiem gia tri thay vi kiem su ton tai** — va hai phep kiem
    ay lech nhau o dung ca `null`."""
    r = man_ghep.khuon_ung_vien(_tho(), lenh=_LENH)
    assert isinstance(r["nguon"], dict)
    assert "loi_nguon" not in r
