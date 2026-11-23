# -*- coding: utf-8 -*-
"""⛔⛔ **CỔNG RA của `G5` — LAYOUT lưới ghép lệnh chi** (`BA-12 §4`).

`G5` là chặng cuối của lộ trình `BA-12`, và nó là chặng **dễ trôi thành sở
thích** nhất: *"trang chưa đẹp"* ⛔ không tự nó nói phải sửa cái gì. ⇒ Bốn
khuyết tật `§4` đã được **đo trước khi vẽ**, và bốn bài dưới đây ghim đúng
bốn phép đo ấy — ⛔ không bài nào ghim một lựa chọn thẩm mỹ.

| # | Khuyết tật | Phép đo 11/09 |
|:-:|---|---|
| ① | `Mã HĐ · CĐT` là chuỗi nối **4 phần** | **55** ký tự; mã ≤ **4**; `hd` **31↔31** · `cdt1` **9↔9** ⇒ **song ánh** |
| ② | nút **Tìm tiền** lặp y hệt mọi dòng | **1.553** nút giống nhau ⇒ **0** thông tin |
| ③ | ⛔ không thấy **dòng khác cùng phiếu** | **1.088/1.553 = 70,1%**; phiếu to nhất **44** dòng |
| ④ | `Luỹ kế %` nằm **giữa các cột tiền** | nó là **vị trí trong danh sách**, cùng loại với `#` |

⚠ Bài ở đây đo **cấu trúc cây thẻ**, ⛔ không đo ảnh chụp màn hình: `dom_gia`
  cố ý ⛔ không phân tích HTML, nên mọi thứ soi được phải là thẻ thật.
"""
from __future__ import annotations

from tests.web.khung_node import can_node
from tests.web.test_man_f01_lenh_dom import _ve

_VE_LUOI = ("F01L.ST.curr = 'VND';"
            " const o = document.createElement('div');"
            " document.body.appendChild(o);"
            " await F01L.ve_luoi(o);")


# ── ① chuỗi `CODE | Tên` ⇒ chỉ CODE ──────────────────────────────────────
@can_node
def test_HD_va_CDT_chi_hien_MA_con_TEN_DAY_DU_nam_o_title():
    """⭐⭐ **Cắt mà mất chữ là một mặc định im lặng** (`INV-I16`).

    Phép rút gọn này chỉ hợp lệ vì **song ánh**: `hd` có `31` mã ↔ `31` tên,
    `cdt1` có `9` ↔ `9`. Mã xác định tên **duy nhất** ⇒ bỏ tên khỏi lưới
    ⛔ **không mất một thông tin nào**, nó chỉ dời sang `title`.

    ⛔ Nếu ai đó bỏ `title` đi thì tên biến mất **thật**, và bài này đỏ.
    """
    # ⚠ ⛔ ĐỪNG đọc `o.innerHTML` của cả lưới: `dom_gia` cố ý ⛔ không tuần tự
    #   hoá cây con, nên nó trả **chuỗi rỗng** — một phép đo *"xanh vì ⛔
    #   không đo được gì"*. Đọc **từng ô**, nơi chuỗi đã được gán thẳng.
    r = _ve(_VE_LUOI
            + " return [...o.querySelectorAll('tbody tr')]"
              ".map(tr => [tr.children[5].innerHTML,"
              " tr.children[6].innerHTML]);")
    hd, cdt = r[0]
    assert ">HCC<" in hd, f"⛔ mã `HCC` ⛔ không lên lưới: {hd!r}"
    assert ">CSM<" in cdt, f"⛔ mã `CSM` ⛔ không lên lưới: {cdt!r}"
    # ⛔ tên dài ⛔ KHÔNG được nằm trong chữ của ô…
    assert ">HCC | Head Count Cost<" not in hd, \
        "⛔ vẫn đang đổ cả chuỗi 55 ký tự ra ô"
    # …nhưng PHẢI còn trong tầm với của người đọc
    assert "HCC — Head Count Cost" in hd, "⛔ tên đầy đủ đã BIẾN MẤT khỏi màn"
    assert "CSM — SuperMinds" in cdt, cdt


@can_node
def test_gia_tri_KHONG_co_dau_gach_thi_giu_NGUYEN_VAN():
    """⛔ **9** dòng `cdt1` thật ⛔ không mang dấu `|`. Cắt theo vị trí ký tự
    ở đó là **bịa** — chúng phải hiện nguyên văn.

    ⛔ Và `hd = null` phải ra **một dấu gạch**, ⛔ không phải chữ `"null"` —
      lỗi kinh điển của phép nối chuỗi trong JS.
    """
    r = _ve("return [F01L.ma_ngan('NB'), F01L.ma_ngan(null),"
            " F01L.ma_ngan(''), F01L.ma_ngan('CXA | Product Cost')];")
    assert ">NB<" in r[0], f"⛔ giá trị ⛔ không có dấu `|` bị cắt mất: {r[0]!r}"
    assert "null" not in r[1] and "—" in r[1], r[1]
    assert "—" in r[2], r[2]
    assert ">CXA<" in r[3] and "CXA — Product Cost" in r[3], r[3]


# ── ② động từ theo RỔ ────────────────────────────────────────────────────
@can_node
def test_NUT_noi_dung_tu_THEO_RO_chu_khong_mot_chu_lap_1553_lan():
    """⭐⭐ **Một nút giống hệt nhau trên 1.553 dòng mang 0 thông tin.**

    Cùng một ngăn kéo mở ra — đổi là **chữ trên nút**, và chữ ấy nói đúng
    việc sắp làm. `may`+`tự chứng` ⇒ *Duyệt*; `nguoi` ⇒ *Tra tiền*;
    `khong` ⇒ *Xem vì sao*.
    """
    r = _ve(_VE_LUOI
            + " return [...o.querySelectorAll('td.lam button')]"
              ".map(b => b.textContent);")
    assert r == ["Duyệt", "Tra tiền"], r
    assert len(set(r)) == len(r), "⛔ hai dòng khác rổ mà nút nói cùng một câu"


@can_node
def test_ro_KHONG_BAO_GIO_thi_nut_noi_XEM_VI_SAO_chu_khong_moi_lam():
    """⛔ Rổ *"⛔ không ai trả lời được"* mà nút vẫn mời *"Tìm tiền"* là **mời
    kế toán đi làm một việc đã đo được là vô ích**."""
    r = _ve("return [F01L.viec_cua_dong({ro: 'khong'}),"
            " F01L.viec_cua_dong({ro: 'nguoi'}),"
            " F01L.viec_cua_dong({ro: 'may', tu_chung: true}),"
            " F01L.viec_cua_dong({ro: 'may', tu_chung: false})];")
    assert [x[0] for x in r] == \
        ["Xem vì sao", "Tra tiền", "Duyệt", "Mở để chia"], r


# ── ③ dòng khác của CÙNG PHIẾU ───────────────────────────────────────────
@can_node
def test_PHIEU_NHIEU_DONG_hien_ra_con_phieu_MOT_DONG_thi_KHONG():
    """⭐⭐ `1.088/1.553` = **70,1%** dòng chờ nằm trong phiếu nhiều dòng, và
    phiếu to nhất có **44** dòng ⇒ đây là **phần lớn** danh sách, ⛔ không
    phải một ca hiếm.

    ⛔ Nhưng phiếu **một dòng** thì ⛔ KHÔNG được đeo huy hiệu: một dấu hiệu
      xuất hiện trên **mọi** dòng thì ⛔ không còn là dấu hiệu.
    """
    r = _ve(_VE_LUOI
            + " return [...o.querySelectorAll('tbody tr')]"
              ".map(tr => tr.children[2].innerHTML);")
    assert "2/3" in r[0], f"⛔ phiếu 3 dòng ⛔ không nói ra: {r[0]!r}"
    assert "1/1" not in r[1], f"⛔ phiếu MỘT dòng vẫn đeo huy hiệu: {r[1]!r}"


# ── ④ `Luỹ kế %` ⛔ KHÔNG phải một cột tiền ──────────────────────────────
@can_node
def test_LUY_KE_gop_vao_cot_HANG_chu_KHONG_dung_giua_cac_cot_tien():
    """⭐ `Luỹ kế %` ⛔ không phải thuộc tính **của dòng này** — nó là *"đọc
    tới đây là phủ bao nhiêu % tiền"*, tức **vị trí trong danh sách**, cùng
    loại với `#`. Đứng cạnh `Tiền lệnh` thì nó đọc như một con số tiền.

    ⇒ Gộp vào `#`, và mất hẳn một cột.
    """
    r = _ve(_VE_LUOI
            + " return [[...o.querySelectorAll('thead th')]"
              ".map(t => t.textContent),"
              " [...o.querySelectorAll('tbody tr')][0].children[0].innerHTML];")
    dau, o_hang = r
    assert "Luỹ kế" not in dau, f"⛔ `Luỹ kế` vẫn là một cột riêng: {dau}"
    assert dau.index("Tiền lệnh") + 1 == dau.index("Trạng thái"), \
        f"⛔ còn một cột chen giữa `Tiền lệnh` và `Trạng thái`: {dau}"
    assert "62.50%" in o_hang, f"⛔ luỹ kế ⛔ BIẾN MẤT khỏi màn: {o_hang!r}"


# ── ghim: hai cột đầu + cột VIỆC ─────────────────────────────────────────
@can_node
def test_HAI_COT_DAU_ghim_o_CA_THE_TIEU_DE_lan_the_O():
    """⭐⭐ **Lớp `f1`/`f2` thiếu ở `th` là một lỗi ⛔ không ai thấy tới lúc
    cuộn.** Thân bảng đứng yên còn dòng tiêu đề trôi ngang ⇒ bảng **lệch
    đầu**, và mọi cột đọc sai tên. `TP.bang` trước 11/09 ⛔ không nhận `lop`
    trên tiêu đề — nên bài này canh **cả hai** vế.
    """
    r = _ve(_VE_LUOI
            + " const th = [...o.querySelectorAll('thead th')]"
              ".map(t => t.className);"
            + " const td = [...o.querySelectorAll('tbody tr')][0]"
              ".children; "
            + " return [th.slice(0, 2), [td[0].className, td[1].className]];")
    th, td = r
    assert th[0] == "f1" and th[1] == "f2", f"⛔ tiêu đề ⛔ không ghim: {th}"
    assert "f1" in td[0] and "f2" in td[1], f"⛔ ô ⛔ không ghim: {td}"


@can_node
def test_LUOI_mang_lop_lenh_de_KHONG_dung_be_rong_ghim_cua_F02():
    """⛔ `--khoa-1`/`--khoa-2` ở `tokens.css` là `346px` — con số **đã đo ở
    mũi thử** cho lưới `F02`. Sửa ở đó là đổi luôn `F02`. Lớp `lenh` đặt lại
    hai biến ấy trên **chính bảng này**."""
    r = _ve(_VE_LUOI + " return o.querySelector('table').className;")
    assert "g" in r.split() and "lenh" in r.split(), r
