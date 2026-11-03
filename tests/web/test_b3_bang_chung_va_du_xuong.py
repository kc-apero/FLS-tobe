# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ Hai lop bao ve cua cot **Dien giai**.

⛔⛔ Hop dong `§6.2` viet thang: ***"⛔ Khong dung tooltip lam loi duy nhat"***.
   Truoc ban va nay, tooltip **LA** loi duy nhat: `white-space:nowrap` ＋
   `title`, ⛔ khong `đủ ↓`, ⛔ khong `<mark>`, va token `--evi-bg` khai o
   `tokens.css` roi **dung 0 lan** trong ca kho.

⭐ Dien giai la **bang chung duy nhat** cua `4.145/8.387` = **49%** cuon so.

⚠ **Mot gioi han phai noi ra:** DOM gia ⛔ khong dan trang, nen bai nay **tu
  dat** `scrollHeight`／`clientHeight`. No do duoc **LUAT** *(chi moi `đủ ↓`
  khi that su bi cat)*, ⛔ **khong** do duoc con so that — cai do chi trinh
  duyet that tra loi duoc (`NFR-I10`).
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
THE = {"ma_lenh": "PM1-1", "trang_thai": "chua_gan",
       "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
       "loai_phieu": "Regular", "noi_dung": "TT S.", "so_tien": "1000.00",
       "curr": "USD", "nguoi_nhan": "S. INC.", "so_chung_tu": "1026946429",
       "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
       "cdt": "CVL | VisionLab", "nhom_du_truong": []}

UV = {"itl_id": 42, "doc_date": "2026-09-18", "doc_no": "1026946429",
      "dien_giai": "CARD 1026946429 SENSORTOWER 1000.00 THANH TOAN",
      "amount": "1000.00", "chieu": "co", "curr": "USD",
      "nguon": {"tk": "PO2", "bank": "OCBC", "curr": "USD", "le": "SGO2"},
      "bac": "ma", "lech": None,
      "khoa_to": ["1026946429", "SENSORTOWER", "1000.00"]}


def _dat(uv=None) -> str:
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [{"pm_line_id": "PM1-1", "the": THE}],
                      "next_cursor": None}}, ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};'
        "_TRA['/queue/lenh/PM1-1/itl-candidates'] = "
        "  {data: {ung_vien: " + json.dumps(uv or [UV], ensure_ascii=False) + "}};")


def _mo(them: str, uv=None) -> str:
    return (_dat(uv) + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
            + them)


# ── ⓐ ⭐⭐ BANG CHUNG duoc TO ────────────────────────────────────────────

def test_BANG_CHUNG_duoc_TO_trong_dien_giai():
    r = _chay(_mo(" return document.querySelectorAll('.dg')[0].innerHTML;"),
              tep=TEP, vo=VO)
    assert "<mark>1026946429</mark>" in r, (
        f"⛔ số chứng từ **trùng đúng** ⛔ không được tô. innerHTML = {r!r}")
    assert "<mark>1000.00</mark>" in r, "⛔ số tiền khớp tuyệt đối ⛔ không được tô"
    assert "<mark>SENSORTOWER</mark>" in r, "⛔ tên bên nhận ⛔ không được tô"


def test_KHONG_co_khoa_thi_KHONG_to_gi():
    """⛔ Cua tra `khoa_to: []` nghia la *"⛔ khong co gi dang to"* — man
    ⛔ khong duoc tu nghi ra mot khoa nao."""
    r = _chay(_mo(" return document.querySelectorAll('.dg')[0].innerHTML;",
                  uv=[dict(UV, khoa_to=[])]), tep=TEP, vo=VO)
    assert "<mark" not in r, r


def test_KHOA_lot_khong_lam_NO_man():
    """⛔ Mot khoa mang ky tu regex *(`(`, `[`, `*`)* ⛔ khong duoc lam sap ca
    man — do la duong mot chuoi tu **sao ke ngan hang** di vao."""
    r = _chay(_mo(" return document.querySelectorAll('.dg')[0].innerHTML;",
                  uv=[dict(UV, khoa_to=["CARD (x[*"])]), tep=TEP, vo=VO)
    assert isinstance(r, str)


# ── ⓑ ⭐⭐⭐ THOAT truoc, TO sau ────────────────────────────────────────

def test_dien_giai_duoc_THOAT_truoc_khi_to():
    """⛔⛔ `dien_giai` la chu **tu sao ke ngan hang**, tuc chu ⛔ khong ai
    kiem soat. Ghep thang vao `innerHTML` la **mo mot duong chen the**."""
    uv = dict(UV, dien_giai="<img src=x onerror=1> 1026946429",
              khoa_to=["1026946429"])
    r = _chay(_mo(" return document.querySelectorAll('.dg')[0].innerHTML;",
                  uv=[uv]), tep=TEP, vo=VO)
    assert "<img" not in r, f"⛔⛔ thẻ lạ lọt nguyên vào màn: {r!r}"
    assert "&lt;img" in r, r
    assert "<mark>1026946429</mark>" in r, "⛔ thoát xong thì ⛔ không tô được nữa"


# ── ⓒ ⭐⭐⭐ `đủ ↓` CHI hien khi THAT SU bi cat ────────────────────────

def test_DU_XUONG_hien_khi_BI_CAT_va_AN_khi_khong():
    """⛔⛔ Hop dong doi do `scrollHeight` **sau khi da dan trang**, ⛔ khong
    doan theo so ky tu — be rong cot doi theo man nen mot nguong ky tu se
    **vua sai ca hai chieu**.

    ⛔ Mot loi moi hien ra khi ⛔ khong co gi de mo la mot loi moi **day
      nguoi ta thoi tin moi loi moi**.
    """
    r = _chay(_mo(" const d0 = document.querySelectorAll('.dg')[0];"
                  " d0._scrollHeight = 40; d0._clientHeight = 18;"
                  " F01G.soat_cat();"
                  " const bi_cat = document.querySelectorAll('.doc-du')[0].style.display;"
                  " d0._scrollHeight = 18; F01G.soat_cat();"
                  " const vua = document.querySelectorAll('.doc-du')[0].style.display;"
                  " return {bi_cat, vua};"), tep=TEP, vo=VO)
    assert r["bi_cat"] == "inline-block", "⛔ bị cắt mà ⛔ không mời `đủ ↓`"
    assert r["vua"] == "none", (
        "⛔ ⛔ không bị cắt mà vẫn mời `đủ ↓` — một lời mời vô nghĩa **dạy "
        "người ta thôi tin mọi lời mời**")


def test_bam_DU_XUONG_thi_dong_CAO_THEM_va_bo_kep():
    r = _chay(_mo(" const dong = document.querySelectorAll('.cand')[0];"
                  " const nut = document.querySelectorAll('.doc-du')[0];"
                  # ⭐ Ban qua NUT NGOAI — `.doc-du` la mot `span`, ⛔ khong co
                  #   listener rieng. Dung duong mot cu bam that di.
                  " dong._nghe.click[0]({target: nut});"
                  " return {lop_dg: document.querySelectorAll('.dg')[0].className,"
                  "         lop_dong: document.querySelectorAll('.cand')[0].className,"
                  "         nhan: document.querySelectorAll('.doc-du')[0].textContent,"
                  "         chon: F01G.ST.ung_vien_chon};"), tep=TEP, vo=VO)
    assert "clamp" not in r["lop_dg"], "⛔ bấm `đủ ↓` mà chữ vẫn bị kẹp một dòng"
    assert "rong" in r["lop_dong"], "⛔ dòng ⛔ không cao thêm"
    assert "thu gọn" in r["nhan"], r["nhan"]
    assert r["chon"] is None, (
        "⛔⛔ Bấm **mở rộng chữ** mà kéo theo **chọn ứng viên** — hai ý định "
        "khác nhau bị gộp làm một cú")


# ── ⓓ ⛔⛔⛔ NUT LONG NUT la HTML ⛔ KHONG hop le ───────────────────────

def test_KHONG_co_NUT_nao_nam_TRONG_mot_NUT():
    """⛔⛔⛔ `.cand` **DA la mot `<button>`**. Mot `<button>` nua ben trong no
    la HTML **⛔ khong hop le** — trinh duyet that ⛔ khong xu ly duoc nut
    trong, con DOM gia thi cho chay **ngon lanh**.

    ⭐⭐ Day dung la lop loi ma mot **khuon thu ⛔ KHONG THE** bat: no ⛔ khong
       phan tich HTML, no chi dung cay the. ⇒ Phai do o **ma nguon**.

    ⭐ Ban dung da giai dung cho nay: `<span class="mo" role="button"
      tabindex="0" data-mo=…>` ＋ bat click o **nut ngoai** qua `closest`.
    """
    import io
    import pathlib
    import re
    js = (pathlib.Path(__file__).resolve().parents[2]
          / "fls" / "web" / "tep" / "man_f01_ghep.js")
    ma = io.open(js, encoding="utf-8").read()
    ma = re.sub(r"/\*[\s\S]*?\*/", "", ma)
    ma = re.sub(r"(?m)^\s*//.*$", "", ma)
    than = ma[ma.index("function ve_ung_vien"):]
    than = than[:than.index("\n  function ")]
    # ⛔⛔ **Bai nay BAO OAN HAI lan truoc khi do dung thu.**
    #    ① Quet `'button'` ⇒ bat chinh **nut GOC** cua dong *(`.cand`)*.
    #    ② Dem `<= 1` ⇒ van bat `setAttribute('type', 'button')` va
    #       `setAttribute('role', 'button')` — hai **gia tri thuoc tinh**,
    #       ⛔ khong phai hai the.
    # ⭐⭐ Cung mot hinh dang sai lam **lan thu nam**: do CHU thay vi do
    #   **thu se chay**. ⇒ Do dung **phep TAO THE**: `o('button', …)` va
    #   `TP.el(… 'button' …)`. Dong ung vien la mot the ⇒ **mot** la dung.
    tao = re.findall(r"(?:TP\.el|\bo)\s*\([^)]*?['\"]button['\"]", than)
    assert len(tao) <= 1, (
        f"⛔⛔ `ve_ung_vien` **dựng** {len(tao)} thẻ `button`, mà dòng ứng viên "
        'bản thân **đã là một** `<button class="cand">` ⇒ có nút **nằm trong** '
        "nút. HTML ⛔ không hợp lệ, và trình duyệt thật ⛔ không xử lý được nút "
        'trong. Dùng `span` kèm `role="button"` ＋ `tabindex`, bắt click ở nút '
        f"NGOÀI qua `closest` — đúng khuôn bản dựng. Thấy: {tao}")


# ── ⓔ ⭐ token `--evi-bg` phai duoc DUNG ───────────────────────────────

def test_token_evi_bg_duoc_DUNG_that():
    """⛔ Mot token khai ma dung `0` lan la mot token **⛔ khong ton tai**."""
    import io
    import pathlib
    css = (pathlib.Path(__file__).resolve().parents[2]
           / "fls" / "web" / "tep" / "hinh.css")
    assert "--evi-bg" in io.open(css, encoding="utf-8").read(), (
        "⛔ `--evi-bg` khai ở `tokens.css` mà ⛔ không dùng ở đâu")
