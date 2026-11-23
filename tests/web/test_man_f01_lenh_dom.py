# -*- coding: utf-8 -*-
"""⛔⛔ **CỔNG RA của `GAP-SCR-14` ở tầng MÀN HÌNH** — lằn LỆNH CHI của `F01`.

`QĐ-ITL-122` là một quyết định về **câu hỏi nào được hỏi**, nên cổng ra của nó
⛔ **không** nằm ở tầng kho: nó nằm ở chỗ kế toán **đọc**. Bốn câu:

  ⓐ ⭐⭐⭐ **Lằn mặc định là lằn LỆNH CHI.** Nếu mặc định vẫn là lằn dòng tiền
    thì quyết định của chủ sổ **⛔ không đến được người dùng** — mã đúng, màn
    hình vẫn hỏi câu cũ, và ⛔ không cổng nào ở tầng dưới thấy điều đó.
  ⓑ **Lằn cũ ⛔ KHÔNG bị xoá.** Nó là đường duy nhất để ghi lý do · hoãn · bỏ
    ghép · bấm xong — bốn việc `QĐ-ITL-71`/`72` đã chốt và ⛔ không có ở phía
    lệnh chi.
  ⓒ **`so_dong_phu = null` phải vẽ *"⛔ không đo được"*, ⛔ không phải `0`.**
    Vẽ `0` nói *"xem 0 dòng là đủ"* — một câu **sai**.
  ⓓ **Phép CẮT phải hiện ra.** Cắt mà im là một mặc định im lặng
    *(`INV-I16`)*: người gõ tưởng danh sách đầy đủ và kết luận *"⛔ không có
    dòng tiền nào khớp"*.

★ Cửa được **giả lập** — câu hỏi ở đây là *"màn vẽ đúng ⛔ không"*. Câu *"cửa
  trả đúng ⛔ không"* là việc của `tests/api/test_cua_lenh_cho_pg.py`.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay, can_node

# ⭐ Hình số CỐ Ý giống kho thật 09/09: `1.345` dòng chờ · `510` phiếu · và
#   **69** dòng phủ 90% tiền. Một bộ số tròn trịa sẽ ⛔ không lộ ra chuyện màn
#   vẽ con số nào ở đâu.
_TOM = {"theo_tien_te": [
    {"curr": "USD", "so_dong": 700, "so_phieu": 314, "tien": "133538092.79",
     "so_dong_duyet": 538, "so_dong_chua_duyet": 162,
     "so_dong_phu": 4, "pct_that": "90.00"},
    {"curr": "VND", "so_dong": 590, "so_phieu": 365,
     "tien": "62008251838.74", "so_dong_duyet": 484,
     "so_dong_chua_duyet": 106, "so_dong_phu": 60, "pct_that": "90.06"},
    # ⭐⭐ Σ tiền = 0 ⇒ *"phủ bao nhiêu % tiền"* ⛔ KHÔNG CÓ NGHĨA ⇒ `null`.
    {"curr": "HKD", "so_dong": 2, "so_phieu": 2, "tien": "0",
     "so_dong_duyet": 2, "so_dong_chua_duyet": 0,
     "so_dong_phu": None, "pct_that": None},
]}

# ⭐ `G5` — hình dạng CỐ Ý giống kho thật 11/09, vì ba khuyết tật layout chỉ
#   lộ ra trên đúng hình dạng ấy:
#     · `hd`/`cdt1` là chuỗi `CODE | Tên người đọc` *(đo: 55 ký tự)*
#     · `SL-1` là phiếu **nhiều dòng** — 1.088/1.553 (**70,1%**) dòng chờ là vậy
#     · `SL-2` **⛔ không** có dấu `|` ở `cdt1` — **9** dòng thật như thế
_LUOI = {"rows": [
    {"pm_line_id": "PML-A", "pm_slip_id": "SL-1", "ref_tho": "FT2519001",
     "ref_canon": "FT2519001", "amount": "50000000", "curr": "VND",
     "status": "Approve", "hd": "HCC | Head Count Cost",
     "cdt1": "CSM | SuperMinds", "source_row": 11,
     "tien": "50000000", "duyet": True, "hang": 1, "luy_ke_pct": "62.50",
     "phieu_tong": 3, "phieu_cho": 2, "ro": "may", "tu_chung": True},
    {"pm_line_id": "PML-B", "pm_slip_id": "SL-2", "ref_tho": "FT2519002",
     "ref_canon": "FT2519002", "amount": "30000000", "curr": "VND",
     "status": "Reject", "hd": None, "cdt1": "NB", "source_row": 12,
     "tien": "30000000", "duyet": False, "hang": 2, "luy_ke_pct": "100.00",
     "phieu_tong": 1, "phieu_cho": 1, "ro": "nguoi", "tu_chung": False},
], "next_cursor": None, "count": 2}

_UV = {
    "dong_lenh": {"pm_line_id": "PML-A", "pm_slip_id": "SL-1",
                  "ref_tho": "FT2519001", "ref_canon": "FT2519001",
                  "amount": "50000000", "curr": "VND", "status": "Approve",
                  "hd": "HD-01", "cdt1": "CDT-A", "source_row": 11},
    "dung_sai": "1000",
    # ⭐⭐ `WO-022` vòng 3 *(`KQ-029` `F-1`)*: ứng viên theo **khuôn `⓵`**
    #   `BA-07 §4h` — khuôn cửa trả từ `23/09` *(`man_ghep.khuon_ung_vien`)*.
    #   ⛔ Trước: khuôn **hàng thô** `tien`/`lech_tuyet_doi`/`memo`/`le`/
    #   `work_status` mà cửa ⛔ còn trả ⇒ bài xanh trên một cửa ⛔ tồn tại.
    #   Khuôn này **có canh**: khoá ⊆ khoá cửa thật *(`test_wo022_v3…KHUON_THU…`)*.
    "ung_vien": [
        {"itl_id": 9001, "doc_date": "2026-08-03", "doc_no": "FT2519001",
         "dien_giai": "chuyen tien nha cung cap", "amount": "50000000",
         "chieu": "co", "curr": "VND", "nguon": None, "bac": "ma",
         "lech": None},
        {"itl_id": 9002, "doc_date": "2026-08-04", "doc_no": "FT2519999",
         "dien_giai": "khoan khac", "amount": "50000000",
         "chieu": "co", "curr": "VND", "nguon": None, "bac": "tien",
         "lech": "0"},
    ],
    # ⭐⭐ CẮT — và cửa KHAI RA mình đã cắt
    "bi_cat": True,
    "tong_cung_tien_te": 2987,
    "canh_bao": "",
    "anh_pm": "NAP-2026-09-09-PM2DEAB588",
    "pham_vi": "chi lan nap that",
}

VO_F01 = """
const man = d.document.createElement('section'); man.id = 'man-f01';
man.className = 'screen on';
const than = d.document.createElement('div'); than.id = 'than-f01';
man.appendChild(than);
d.body.appendChild(man);

// ⚠ Khung hop thoai dung san — `dom_gia.js` co y ⛔ KHONG phan tich HTML, nen
//   `HT.mo` se NO ngay dong dau neu ba o nay ⛔ chua ton tai. Cung gioi han da
//   ghi o `test_man_f01_lo_dom.py`.
const scrim = d.document.createElement('div'); scrim.id = 'scrim';
for (const id of ['dlg-t', 'dlg-b', 'dlg-f']) {
  const e = d.document.createElement('div'); e.id = id; scrim.appendChild(e);
}
d.body.appendChild(scrim);
const inp = d.document.createElement('input'); inp.id = 'o-vi-sao-l';
d.body.appendChild(inp);
"""

TEP = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
       "man_f01_lenh.js", "man_f01.js"]


def _ve(kich_ban: str, *, tra: dict | None = None, phien=None):
    dat = {"/queue/lenh-cho/summary": {"data": _TOM},
           "/queue/lenh-cho?limit=50&curr=VND": {"data": _LUOI},
           "/queue/lenh/PML-A/itl-candidates": {"data": _UV}}
    dat.update(tra or {})
    mo = "".join(
        "_TRA[%s] = %s;\n" % (json.dumps(k), json.dumps(v, ensure_ascii=False))
        for k, v in dat.items())
    return _chay(mo + kich_ban, tep=TEP, vo=VO_F01, phien=phien)


# ── ⓐ⭐⭐⭐ LẰN MẶC ĐỊNH ─────────────────────────────────────────────────
@can_node
def test_LAN_MAC_DINH_la_lan_LENH_CHI():
    """⭐⭐⭐ **Câu cổng của `GAP-SCR-14`.**

    Nếu mặc định vẫn là lằn dòng tiền thì quyết định của chủ sổ **⛔ không đến
    được người dùng**: mã đúng, cửa đúng, mà màn hình **vẫn hỏi câu cũ** — và
    ⛔ không một cổng nào ở tầng dưới thấy điều đó.
    """
    r = _ve("return F01.ST.lan;")
    assert r == "lenh", (
        f"⛔⛔ lằn mặc định là {r!r} — màn vẫn đang hỏi phía dòng tiền")


@can_node
def test_thanh_lan_co_DU_HAI_lan__lan_cu_KHONG_bi_xoa():
    """⛔ Lằn cũ là đường **duy nhất** để ghi lý do · hoãn · bỏ ghép · bấm
    xong. Xoá nó là cắt bốn hành động `QĐ-ITL-71`/`72` đã chốt."""
    r = _ve("F01.ve_man();"
            " return [...document.querySelectorAll('button')]"
            ".map(b => b.textContent)"
            ".filter(x => x.indexOf('Theo ') === 0);")
    assert len(r) == 2, r
    assert any("LỆNH CHI" in x for x in r), r
    assert any("dòng tiền" in x for x in r), r


@can_node
def test_bam_sang_lan_cu_thi_ST_doi():
    r = _ve("F01.ve_man();"
            " const b = [...document.querySelectorAll('button')].find("
            "x => x.textContent.indexOf('Theo dòng tiền') === 0);"
            " b.onclick(); return F01.ST.lan;")
    assert r == "tien"


# ── ⓒ⭐⭐ `null` ⛔ KHÔNG được vẽ thành `0` ───────────────────────────────
@can_node
def test_so_dong_phu_NULL_ve_KHONG_DO_DUOC_chu_khong_ve_0():
    """⭐⭐ Σ tiền = 0 ⇒ câu *"xem mấy dòng là phủ 90% tiền"* **⛔ không có
    nghĩa**. Vẽ `0` ở đây nói *"xem 0 dòng là đủ"* — một câu **sai**, và nó
    sai theo hướng **nguy hiểm**: kế toán bỏ qua cả tiền tệ ấy."""
    r = _ve("const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_tom(o); return o.textContent;")
    assert "không đo được" in r, r
    # ⭐ và hai tiền tệ đo được thì vẽ CON SỐ
    # ⚠ `textContent` cua khung gia tra lai **chuoi HTML da gan** cho
    #   nhung o dung `innerHTML` ⇒ phep do o day la phep do CHUOI, va no
    #   phai mang ca the `</b>`. Ghi ro de ⛔ khong ai "don" no thanh sai.
    assert "<b>4</b> ⇒ 90.00%" in r, r
    assert "<b>60</b> ⇒ 90.06%" in r, r


@can_node
def test_chan_man_KHONG_co_dong_TONG_va_NOI_RO_vi_sao():
    r = _ve("const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_tom(o); return o.textContent;")
    assert "Không có dòng “tổng”" in r, r
    assert "USD" in r and "VND" in r and "HKD" in r, r


@can_node
def test_chan_man_TACH_dong_chua_duyet_thanh_mot_cau_rieng():
    """⛔⛔ Gộp `162 + 106 = 268` dòng chưa duyệt vào *"việc còn lại"* là đưa
    cho kế toán một danh sách họ **⛔ không làm được gì với nó** — cửa ghép đòi
    `force` kèm lý do."""
    r = _ve("const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_tom(o); return o.textContent;")
    assert "268" in r, r
    assert "không phải việc" in r, r


# ── lưới ────────────────────────────────────────────────────────────────
@can_node
def test_luoi_ve_TRANG_THAI_va_RONG_la_khong_biet():
    r = _ve("F01L.ST.curr = 'VND';"
            " const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_luoi(o); return o.textContent;")
    assert "FT2519001" in r and "FT2519002" in r, r
    assert "Approve" in r and "Reject" in r, r


# ── ⓓ⭐⭐ phép CẮT phải hiện ra ──────────────────────────────────────────
@can_node
def test_drawer_KHAI_RA_da_CAT_danh_sach():
    """⭐⭐ Cắt mà im là một **mặc định im lặng** *(`INV-I16`)*: người gõ tưởng
    danh sách là đầy đủ và kết luận *"⛔ không có dòng tiền nào khớp"*."""
    r = _ve("F01L.ST.curr = 'VND';"
            " const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_luoi(o);"
            " const b = [...document.querySelectorAll('button')]"
            ".find(x => x.textContent === 'Duyệt');"
            " await b.onclick();"
            " return document.querySelector('#dlg-b').innerHTML;")
    assert "bị CẮT" in r or "CẮT" in r, r
    assert "2.987" in r, r
    assert "mã khớp" in r, r


@can_node
def test_drawer_ghim_TIEN_LENH_va_DUNG_SAI():
    r = _ve("F01L.ST.curr = 'VND';"
            " const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_luoi(o);"
            " const b = [...document.querySelectorAll('button')]"
            ".find(x => x.textContent === 'Duyệt');"
            " await b.onclick();"
            " return document.querySelector('#dlg-b').innerHTML;")
    assert "dung sai" in r, r
    assert "50.000.000" in r, r


@can_node
def test_TEN_BAC_giong_lan_dong_tien_tung_chu():
    """⛔ Hai lằn phải nói **cùng một từ** cho **cùng một ý**. Đổi tên ở một
    phía sẽ làm người đọc tưởng đây là hai thang đo khác nhau.

    ⭐ *(`WO-032` (d) — viết lại, **giữ nguyên lo gốc**)*: `BA-07` **v3.7**
      §4h ⓹ thêm bậc thứ năm `khac_tien_te` **chỉ** cửa `/so` sinh, và
      `WO-032` đòi `F01L.BAC` có mục ấy *(⛔ rơi về `cung_tien_te`)*. Bốn bậc
      **chung** với lằn dòng tiền vẫn phải **y từng chữ** *(lo gốc)*; mục thứ
      năm đứng **sau** và mang đúng tên hợp đồng."""
    r = _ve("return [Object.keys(F01L.BAC),"
            " Object.values(F01L.BAC).map(x => x[1])];")
    assert r[0][:4] == ["ma", "tien", "gan_tien", "cung_tien_te"], r
    assert r[1][:4] == ["mã khớp", "tiền khớp", "gần tiền", "cùng tiền tệ"], r
    assert r[0][4:] == ["khac_tien_te"] and r[1][4:] == ["khác tiền tệ"], r
