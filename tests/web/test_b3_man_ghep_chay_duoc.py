# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ MAN GHEP **CHAY DUOC**, ⛔ khong chi *doc ra co ve dung*.

⛔⛔⛔ **Vi sao bai nay ton tai — no vá mot lo cua chinh cong ben canh.**

`test_b3_fe_bam_thiet_ke.py` bien hop dong thiet ke thanh **phep do tren ma**,
va no lam viec ay tot. ⛔ Nhung ban dau cua `man_f01_ghep.js` goi mot API `TP`
**toi tu bia**:

    toi viet : TP.el('div', {class: 'wh'}, con1, con2)
    that la  : TP.el(the_gi, lop, html)

⇒ Man **⛔ khong the chay mot dong nao**, va no **qua ca 14 phep** cua cong ay
  — vi cong ay **QUET CHU**.

⭐⭐ **Mot cong doc ma ⛔ KHONG thay duoc mot cong chay ma.** Day la lan thu hai
   trong cung mot ngay bai hoc ay hien ra: truoc do
   `test_chieu_KHONG_duoc_suy_tu_pay_type` quet `inspect.getsource()` va **DO**
   vi chinh khoi chu thich *canh bao ve loi* co chua chu ay.

── Bon cau bai nay hoi ─────────────────────────────────────────────────

  ⓐ Man **ve ra duoc** mot danh sach lenh chi.
  ⓑ ⭐ May **⛔ KHONG chon san** mot ung vien nao — ke ca ca may de xuat.
  ⓒ ⭐⭐⭐ `Enter` **⛔ KHONG gan** o ca lech tien; lech phai bam **hai lan**.
  ⓓ ⭐⭐ Truong VANG **hien ra**, ⛔ khong bien mat.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

#: ⭐ `vo` la **JS**, ⛔ khong phai HTML — DOM gia **co y** ⛔ khong phan tich HTML.
#: ⚠ Ten id **⛔ khong duoc** bat dau bang thu doc duoc thanh ma mau: du an da
#:   vap `#f04` va dat quy uoc `nap-*`; day theo dung quy uoc ay (`ghep-*`).
VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""

#: ⛔⛔ **⛔ KHONG dung mot stub RIENG.** Ban dau toi gan `globalThis.FLS = {...}`
#:    va no NO: `goi_cua.js` khai `const FLS` o tam module nen gan vao
#:    `globalThis` ⛔ khong toi duoc no. ⭐ Va khung thu **da co san** co che
#:    gia cua (`_TRA` + `_GOI`) — viet ban thu hai la tao hai ban su that ve
#:    *'cua tra cai gi'*.
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

#: ⭐ Hinh so CO Y giong kho that: mot lenh khop **dung tien**, mot lenh
#: **lech**, va mot dong thieu `Chi nhanh` *(do that: **11,7%** co)*.
DONG = [
    {"ma_lenh": "PM02398-1", "noi_dung": "Thanh toan chi phi Fal.ai",
     "so_tien": "1000.00", "curr": "USD", "trang_thai": "chua",
     "trang_thai_nhan": "chua gan", "trang_thai_mau": "", "loai_phieu": "PM",
     "nguoi_nhan": "SENSORTOWER, INC.", "so_chung_tu": "1026946429",
     "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
     "cdt": "CVL | VisionLab",
     "nhom_du_truong": [{"ten": "Lap lenh", "o": [
         ["Thoi diem", "18/09/2026 09:14"],
         ["Chi nhanh", None],            # ⭐ VANG — phai HIEN ra
         ["Ghi chu", ""]]}]},
    {"ma_lenh": "PM02392-6", "noi_dung": "BHXH T08", "so_tien": "3900000.00",
     "curr": "VND", "trang_thai": "chua", "trang_thai_nhan": "chua gan",
     "trang_thai_mau": "", "loai_phieu": "PM", "nguoi_nhan": "B. C. S. C. G.",
     "so_chung_tu": None, "phap_nhan": "VVOH", "ngan_hang": "BIDV",
     "tai_khoan": "••8128", "cdt": "FNS | Facilities", "nhom_du_truong": []},
]

UV_KHOP = {"itl_id": 4242, "doc_date": "2026-09-18", "doc_no": "1026946429",
           "dien_giai": "Card charge (OPENAI *CHATGPT SUBSCR)",
           "amount": "1000.00", "chieu": "co", "curr": "USD",
           "nguon": {"tk": "PO2", "bank": "OCBC", "curr": "USD", "le": "SGO2"},
           "bac": "ma", "lech": None}
UV_LECH = dict(UV_KHOP, itl_id=4243, amount="987.60", bac="gan_tien",
               lech="12.40", dien_giai=None,
               dien_giai_vi_sao="chua_noi_duoc")


def _kb(them: str, uv=None) -> str:
    """Dung `F01G` voi du lieu san, roi chay `them`."""
    return (
        "_TRA['/queue/lenh/PM02398-1/itl-candidates'] = "
        "  {data: {ung_vien: " + json.dumps(uv or [UV_KHOP]) + "}};"
        "F01G.ST.dong = " + json.dumps(DONG, ensure_ascii=False) + ";"
        + them)


# ── ⓐ man ve ra duoc ───────────────────────────────────────────────────

def test_man_VE_RA_duoc_danh_sach_lenh_chi():
    r = _chay(_kb("F01G.ve();"
                  " return {rail: document.querySelectorAll('.mrow').length,"
                  "         chip: document.querySelectorAll('.chip-loc').length};"),
              tep=TEP, vo=VO)
    assert r["rail"] == 2, r
    assert r["chip"] == 4, f"⛔ phai co **BON** chip loc, do duoc {r['chip']}"


# ── ⓑ ⭐ may ⛔ KHONG chon san ──────────────────────────────────────────

def test_may_KHONG_chon_san_ung_vien_nao():
    """⭐ `INV-I16` o tang ngon tay: may **de xuat**, nguoi **quyet**."""
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " return {chon: F01G.ST.ung_vien_chon,"
                  "         co_chon: document.querySelectorAll('.cand.chon').length};"),
              tep=TEP, vo=VO)
    assert r["chon"] is None, "⛔ may dang chon san mot ung vien"
    assert r["co_chon"] == 0


# ── ⓒ ⭐⭐⭐ chong gat phan xa ──────────────────────────────────────────

def test_ENTER_KHONG_gan_o_ca_lech_tien():
    """⛔⛔ **`45%`** ca ⛔ khong co ung vien khop dung tien.

    Neu `Enter` van gan duoc o day thi man **day nguoi ta gat bua** — va do la
    thu `NFR-I25` sinh ra de chan.
    """
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " F01G.ST.ung_vien_chon = 0;"
                  " F01G.phim({key: 'Enter'});"
                  " return {ghi: _GOI.filter(g => g[0] === 'ghi').length,"
                  "         xac_nhan: F01G.ST.xac_nhan};",
                  uv=[UV_LECH]),
              tep=TEP, vo=VO)
    assert r["ghi"] == 0, "⛔⛔ `Enter` da GAN mot ca LECH TIEN"
    assert r["xac_nhan"] is False, "⛔ `Enter` ⛔ khong duoc mo ca buoc xac nhan"


def test_ENTER_CO_gan_khi_khop_dung_tien():
    """⭐ Cong phai **do ca hai chieu** — cam het thi cung la mot cong sai."""
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " F01G.ST.ung_vien_chon = 0;"
                  " F01G.phim({key: 'Enter'}); await new Promise(r => setTimeout(r, 0));"
                  " return {ghi: _GOI.filter(g => g[0] === 'ghi').length};"),
              tep=TEP, vo=VO)
    assert r["ghi"] == 1, "⛔ `Enter` ⛔ khong gan duoc ca KHOP DUNG TIEN"


def test_lech_tien_phai_bam_HAI_lan():
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " F01G.ST.ung_vien_chon = 0;"
                  " const l = F01G.ST.dong[0];"
                  " await F01G.gan(l);"
                  " const sau1 = {ghi: _GOI.filter(g => g[0] === 'ghi').length,"
                  "               xn: F01G.ST.xac_nhan};"
                  " await F01G.gan(l);"
                  " return {sau1, ghi2: _GOI.filter(g => g[0] === 'ghi').length};",
                  uv=[UV_LECH]),
              tep=TEP, vo=VO)
    assert r["sau1"]["ghi"] == 0, "⛔ lan bam DAU da ghi"
    assert r["sau1"]["xn"] is True, "⛔ ⛔ khong vao trang thai xac nhan"
    assert r["ghi2"] == 1, "⛔ lan bam HAI ⛔ khong ghi"


# ── ⓓ ⭐⭐ truong VANG phai HIEN ───────────────────────────────────────

def test_truong_VANG_HIEN_RA_chu_KHONG_bien_mat():
    """⛔⛔ Ban dung **bo qua** hang khi gia tri rong ⇒ truong vang bien mat
    ⛔ khong mot chu nao — o dung khoi sinh ra de **yen tam ve data**.

    ⭐ Do `21/09`: `tho` co **41 hinh dang**; `Chi nhanh` chi **11,7%**.
    """
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " F01G.ST.du_truong = true; F01G.ve();"
                  " const dd = document.querySelectorAll('dd');"
                  " return {so_o: dd.length,"
                  "         vang: document.querySelectorAll('dd.vang').length};"),
              tep=TEP, vo=VO)
    assert r["so_o"] == 3, (
        f"⛔ khoi bung ve **{r['so_o']}** o, du lieu co **3** ⇒ co o bi GIAU")
    assert r["vang"] == 2, (
        "⛔ hai o VANG (`Chi nhanh` = null · `Ghi chu` = '') phai duoc danh dau")


# ── ⓔ ⭐ dien giai: `null` mang HAI nghia ─────────────────────────────

def test_dien_giai_CHUA_NOI_DUOC_noi_khac_voi_TRONG():
    r = _chay(_kb("await F01G.mo_lenh('PM02398-1');"
                  " const d = document.querySelectorAll('.dg')[0];"
                  " return {lop: d.className, chu: d.textContent};",
                  uv=[UV_LECH]),
              tep=TEP, vo=VO)
    assert "chua_doc" in r["lop"], r
    assert "chưa đọc được" in r["chu"], r["chu"]
