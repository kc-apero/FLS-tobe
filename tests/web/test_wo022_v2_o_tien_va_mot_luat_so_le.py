# -*- coding: utf-8 -*-
"""`WO-022` **vòng 2** — ô tiền theo ngân sách ký tự · một luật số lẻ · dung sai
in = dung sai so *(`BA-06` **v4.13** §5b ⓒ · ⓕ · ⓘ; `TL-026` của `HOI-026`)*.

⛔⛔ **Vì sao vòng 2 tồn tại — lỗi spec ĐÃ ĐO, ⛔ lo xa** *(`HOI-026`, Chrome
1440×900 máy `8099` kho TEST)*: `AC-7` vòng 1 tin *"`11.742.361.787 VND` 18 ký tự
**đã vừa**"*. Ở **bảng danh sách lệnh** *(`.mcols`, cột `Số tiền` `108px`)* nó
**⛔ vừa**: chữ `131,8px` > ô `108px` ⇒ in `11.742.361.78…` — **426 / 2.721**
lệnh VND cắt **từ trước** `WO-022`, **27** lệnh ngoại tệ cắt **vì** `WO-022`
*(`2.259.942,94 US`)*; và cột `Số tiền GD` `116px` cắt **383 / 8.387** giá trị sổ
*(`TL-026` — `HOI` chưa nêu)*. Kèm hai chỗ `fls-dev` tự khai yếu ở `BG-027`:
#1 hai nhánh số lẻ **bất đối xứng** *(mã lạ `100,5` · VND `,80`)* · #4 dung sai
in `617,29` cạnh phép so `61728` xu.

⭐ Mọi bài nạp tệp **THẬT** *(`thanh_phan.js`, `hop_thoai.js`, màn, `hinh.css`,
`tokens.css`)* — ⛔ định nghĩa `TP.tien` giả, ⛔ ghim bề rộng / cỡ chữ / vị trí
cột bằng hằng *(cổng phải **đọc** chúng, `AC-10`)*. Chiều ĐỎ ghi ở docstring và
**đã chạy thật** trên `HEAD` vòng 1 *(`a7fd01f` — `BG`)*.
"""
from __future__ import annotations

import json
import math
import os
import re

from fls.web import phuc_vu as pv
from tests.web.khung_node import _chay, can_node
from tests.web.test_js_chay_duoc import _chay as _chay_thuan
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo022_tien_theo_tien_te import (CAY, TEP_F01_HOP,
                                                    _hop_ghep_nhieu_dong)

THU_MUC = pv.THU_MUC

# ═══ §5b ⓘ · NGÂN SÁCH bề rộng ô tiền ═════════════════════════════════════
#: ⭐ Ngân sách ký tự của một ô tiền *(`TL-026`: chuỗi ô in dài nhất trên sổ
#: thật hôm nay = **18** — lệnh `103.950.000,00 USD` · sổ `11.742.361.787 VND`)*.
#: ⛔⛔ Đây là **khai của spec** *(`BA-06` §5b ⓘ)*, ⛔ một tham số để nới: bài
#: `AC-11` *(tệp `_pg`)* đỏ khi dữ liệu vượt nó ⇒ việc của `fls-ba` tính lại
#: ⓘ, ⛔ sửa số ở đây cho xanh.
NGAN_SACH_KY_TU = 18
#: Bề ngang **một** ký tự `--mono`, theo **em**, ở phông **rộng nhất** của
#: chuỗi `--mono` *(`IBM Plex Mono` 0,600em — `fls/web` ⛔ có `@font-face` ⇒
#: chữ ra phông cài trên máy; `Cascadia Mono` 0,586 · `Consolas` 0,550 —
#: `TL-026`)*.
EM_MONO_RONG_NHAT = 0.6
#: Hai cột tiền của bảng danh sách lệnh — **khoá** trong `COT_BANG`
#: *(`man_f01_ghep.js`)*, ⛔ số thứ tự *(chèn một cột là trượt vị trí)*.
KHOA_COT_TIEN = ("so_tien", "gd_tien")


def _doc(ten: str) -> str:
    with open(os.path.join(THU_MUC, ten), encoding="utf-8") as f:
        return f.read()


def _bo_chu_thich_css(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _tach_vet(gia_tri: str) -> list[str]:
    """`62px minmax(160px,1fr) 104px` ⇒ `['62px', 'minmax(160px,1fr)', '104px']`
    — tách theo khoảng trắng **ngoài** ngoặc *(⛔ `split()`: `minmax(160px, 1fr)`
    có khoảng trắng bên trong thì vỡ thành hai vệt)*."""
    ra, sau, sau_ngoac = [], "", 0
    for ch in gia_tri.strip():
        if ch == "(":
            sau_ngoac += 1
        elif ch == ")":
            sau_ngoac -= 1
        if ch.isspace() and sau_ngoac == 0:
            if sau:
                ra.append(sau)
            sau = ""
        else:
            sau += ch
    if sau:
        ra.append(sau)
    return ra


def vet_mcols(css: str) -> list[str]:
    """Các vệt `grid-template-columns` của **đúng một** luật `.mcols{…}`.
    ⛔ Gặp 0 hay ≥ 2 luật ⇒ nổ *(`Đ5` — phép ⛔ đo được là ĐỎ)*."""
    luat = re.findall(r"(?<![\w-])\.mcols\s*\{([^}]*)\}", _bo_chu_thich_css(css))
    assert len(luat) == 1, f"⛔ không đo được: {len(luat)} luật `.mcols` (mong 1)"
    m = re.findall(r"grid-template-columns\s*:\s*([^;]+)", luat[0])
    assert len(m) == 1, f"⛔ không đo được: {len(m)} `grid-template-columns`"
    return _tach_vet(m[0])


def fs_than(tokens: str) -> float:
    """`--fs-than` **đọc** từ `tokens.css` *(đơn vị `px` — chữ khác ⇒ nổ)*."""
    m = re.findall(r"--fs-than\s*:\s*([0-9.]+)px\s*;", _bo_chu_thich_css(tokens))
    assert len(m) == 1, f"⛔ không đo được: {len(m)} khai `--fs-than` px"
    return float(m[0])


def khoa_cot_bang(js: str) -> list[str]:
    """Khoá từng cột của `COT_BANG` theo **thứ tự** — đọc nguồn
    `man_f01_ghep.js`, ⛔ ghim."""
    m = re.search(r"const COT_BANG\s*=\s*\[(.*?)\];", js, flags=re.S)
    assert m, "⛔ không đo được: `COT_BANG` vắng khỏi man_f01_ghep.js"
    khoa = re.findall(r"\[\s*'([^']*)'\s*,", m.group(1))
    assert khoa, "⛔ không đo được: `COT_BANG` 0 cột"
    return khoa


def soat_o_tien(css: str, tokens: str, js: str) -> list[str]:
    """⭐ Cổng `AC-10` — trả danh sách **lỗi** *(rỗng = đạt)*. Tách ra hàm để
    chiều ĐỎ chạy được trên **nguồn đã phá** mà ⛔ đụng tệp thật."""
    vet, khoa = vet_mcols(css), khoa_cot_bang(js)
    loi = []
    if len(vet) != len(khoa):
        # ⛔ Chèn một cột vào `COT_BANG` mà ⛔ chèn vệt ⇒ mọi cột sau trượt
        #   sang vệt của cột bên cạnh — đúng lớp *"thẳng hàng mà đọc sai"*.
        loi.append(f"`.mcols` {len(vet)} vệt ≠ `COT_BANG` {len(khoa)} cột")
        return loi
    can = math.ceil(NGAN_SACH_KY_TU * EM_MONO_RONG_NHAT * fs_than(tokens))
    for k in KHOA_COT_TIEN:
        if k not in khoa:
            loi.append(f"⛔ không đo được: cột `{k}` vắng khỏi `COT_BANG`")
            continue
        v = vet[khoa.index(k)]
        m = re.fullmatch(r"([0-9.]+)px", v)
        if not m:
            loi.append(f"cột `{k}` vệt `{v}` ⛔ phải px cố định "
                       f"(`GAP-SCR-29` — cột thẳng hàng)")
        elif float(m.group(1)) < can:
            loi.append(f"cột `{k}` `{v}` < {can}px = ceil({NGAN_SACH_KY_TU} × "
                       f"{EM_MONO_RONG_NHAT} × {fs_than(tokens)})")
    return loi


def test_AC10_hai_cot_tien_mcols_du_NGAN_SACH_18_ky_tu():
    """⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: `108px` / `116px` < `135` ⇒ ĐỎ
    *(hai lỗi — cả hai cột)*."""
    css, tok, js = _doc("hinh.css"), _doc("tokens.css"), _doc("man_f01_ghep.js")
    khoa = khoa_cot_bang(js)
    print("WO-022 AC-10 · fs_than =", fs_than(tok), "· vi tri",
          {k: khoa.index(k) + 1 for k in KHOA_COT_TIEN}, "· vet",
          {k: vet_mcols(css)[khoa.index(k)] for k in KHOA_COT_TIEN})
    assert soat_o_tien(css, tok, js) == []


def test_AC10_cong_CAN__108px__fs_13px__chen_cot_khong_chen_vet():
    """`Đ5`: ba chiều ĐỎ của `WO` chạy trên **nguồn thật đã phá** *(trong bộ
    nhớ)*, ⛔ trên chuỗi tự dựng — cổng phải cắn cả ba, và nguồn thật phải
    xanh *(nếu không, bài này chứng minh ⛔ gì)*."""
    css, tok, js = _doc("hinh.css"), _doc("tokens.css"), _doc("man_f01_ghep.js")
    assert soat_o_tien(css, tok, js) == []
    khoa = khoa_cot_bang(js)
    vet = vet_mcols(css)
    i = khoa.index("so_tien")
    # ① trả `108px` cho cột `Số tiền`
    vet_cu = list(vet)
    vet_cu[i] = "108px"
    luat = re.search(r"\.mcols\s*\{[^}]*\}", css).group(0)
    css_108 = css.replace(luat, ".mcols{grid-template-columns:"
                          + " ".join(vet_cu) + "}")
    assert any("so_tien" in x for x in soat_o_tien(css_108, tok, js))
    # ② `--fs-than` lên `13px` ⇒ 18 × 0,6 × 13 = 140,4 > 136
    tok_13 = re.sub(r"--fs-than\s*:\s*[0-9.]+px", "--fs-than:13px", tok)
    assert tok_13 != tok
    assert len(soat_o_tien(css, tok_13, js)) == 2, soat_o_tien(css, tok_13, js)
    # ③ chèn một cột trước `Số tiền` trong `COT_BANG` mà ⛔ chèn vệt
    js_chen = js.replace("['so_tien', 'Số tiền', 'mr']",
                         "['moi', 'Mới'], ['so_tien', 'Số tiền', 'mr']", 1)
    assert js_chen != js
    assert soat_o_tien(css, tok, js_chen), "⛔ cổng ⛔ cắn cột chèn thiếu vệt"
    # ④ vệt co giãn thay px cố định
    vet_gian = list(vet)
    vet_gian[i] = "minmax(140px,1fr)"
    css_gian = css.replace(luat, ".mcols{grid-template-columns:"
                           + " ".join(vet_gian) + "}")
    assert any("px cố định" in x for x in soat_o_tien(css_gian, tok, js))


def test_AC10_tach_vet_khong_vo_minmax_co_khoang_trang():
    assert _tach_vet("62px minmax(160px, 1fr)  104px") == [
        "62px", "minmax(160px, 1fr)", "104px"]


def test_AC12_luoi_an_toan_o_tien_bang_lenh_NOWRAP_va_ELLIPSIS_trong_css():
    """§5b ⓘ: chuỗi **vượt** ngân sách ⇒ `…` + `title`, ⛔ cắt im lặng. Lưới an
    toàn đặt trên **lớp ô đã có** *(`.mcell.r` của `.mtable` — chỉ hai cột tiền
    dùng `oc('r', …)`)*, ⛔ lớp mới. Chrome đo `textOverflow` thật ở `AC-12`
    *(`BG`)*; bài này chặn ai đó gỡ luật CSS mà ⛔ mở Chrome.

    ⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: `.mcell.r` chỉ có `text-align` ⇒ ĐỎ."""
    css = _bo_chu_thich_css(_doc("hinh.css"))
    luat = re.findall(r"([^{}]+)\{([^}]*)\}", css)
    o_tien = [than for chon, than in luat
              if any(re.fullmatch(r"\.mtable\s+\.mcell\.r", c.strip())
                     for c in chon.split(","))]
    assert len(o_tien) >= 1, "⛔ không có luật `.mtable .mcell.r`"
    gop = ";".join(o_tien)
    assert re.search(r"white-space\s*:\s*nowrap", gop), gop
    assert re.search(r"text-overflow\s*:\s*ellipsis", gop), gop
    js = _doc("man_f01_ghep.js")
    # chỉ HAI ô của bảng dùng lớp `r` — thêm ô thứ ba là kéo lưới an toàn
    # sang một cột ⛔ phải tiền mà ⛔ ai biết
    assert len(re.findall(r"oc\('r',", js)) == 2


@can_node
def test_AC12_o_tien_bang_lenh_mang_TITLE_dung_chuoi_in():
    """`title` = **đúng** chuỗi ô in *(`TP.tien(v, curr) + ' ' + curr`)* ở
    **cả hai** cột tiền — chuỗi > 18 ký tự đọc được khi di chuột, ⛔ mất.

    ⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: ô ⛔ có `title` ⇒ ĐỎ."""
    dong = [{"ma_lenh": "PWV-1", "noi_dung": "chi lon", "so_tien":
             "100000000000.00", "curr": "VND", "trang_thai": "chua",
             "trang_thai_nhan": "chưa gán", "trang_thai_mau": "",
             "loai_phieu": "PM", "ngay": "2026-09-30", "cdt": "CVL",
             "so_chung_tu": "UNC1",
             "gd": {"da_gan": True, "dien_giai": "x", "amount": "11742361787.00",
                    "curr": "VND", "doc_date": "2026-09-30"}}]
    r = _chay("""
      F01G.ST.dong = %s;
      const b = F01G.ve_bang();
      const hang = b.querySelectorAll('.mrow');
      const o = hang[0].children.filter(c => /(^| )r( |$)/.test(c.className));
      return o.map(c => ({title: c.getAttribute('title'),
                          chu: c.textContent}));
    """ % json.dumps(dong, ensure_ascii=False), tep=TEP_F01, vo=VO_F01)
    assert r == [
        {"title": "100.000.000.000 VND", "chu": "100.000.000.000 VND"},
        {"title": "11.742.361.787 VND", "chu": "11.742.361.787 VND"}], r


# ═══ AC-13 · §5b ⓒ v4.13 — MỘT luật số lẻ cho mọi mã ═══════════════════════
#: ⭐ Nguyên văn bảng `AC-13` *(⛔ thêm, ⛔ bớt)*.
CA_AC13 = [
    (("100.50", "20"), "100,50"),       # thay ca thứ 10 của `AC-1`
    (("100", "20"), "100"),
    (("12.5", "20"), "12,50"),
    (("0.5", None), "0,50"),
    (("1306103.8", "VND"), "1.306.103,80"),
    (("1306103.80", "VND"), "1.306.103,80"),
]


@can_node
def test_AC13_mot_luat_so_le_SAU_ca_dung_tung_byte():
    """⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: mã vòng 1 cắt số 0 đuôi nhánh mã
    lạ ⇒ `100,5` · `12,5` · `0,5` ⇒ ĐỎ. Mã lạ cố định 2 ⇒ `100,00` ĐỎ; mã lạ làm
    tròn về 0 lẻ ⇒ `101` ĐỎ."""
    ra = _chay_thuan(["thanh_phan.js"], "[" + ",".join(
        "TP.tien(%s, %s)" % (json.dumps(v), json.dumps(c))
        for (v, c), _m in CA_AC13) + "]")
    assert len(ra) == len(CA_AC13) == 6, f"⛔ không đo được: {len(ra)} ca"
    sai = [(CA_AC13[i][0], CA_AC13[i][1], ra[i]) for i in range(len(ra))
           if ra[i] != CA_AC13[i][1]]
    assert sai == [], "⛔ (vào, mong, ra): " + repr(sai)


@can_node
def test_AC13_ma_LA_va_THIEU_cung_luat_ma_trong_bang_so_le_0():
    """Luật chung ⓐ+ⓑ+ⓒ: mã lạ / thiếu ⇒ bảng coi là **0** — ⇒ in **y hệt**
    VND *(mã trong bảng có số lẻ 0)* trên **mọi** giá trị. Đo **quan hệ**,
    ⛔ chỉ sáu ca: một nhánh riêng cho mã lạ lệch VND ở bất kỳ giá trị nào
    là ĐỎ."""
    ra = _chay_thuan(["thanh_phan.js"], """(() => {
      const v = ['0', '0.5', '0.05', '1', '-1.5', '-0.40', '100.50', '12.25',
                 '1234567.8', '1234567.89', '1306103.80', '-0.00', 7, 66923.25,
                 '0.10', '999999999999.99'];
      return v.map(x => [String(x), TP.tien(x, 'VND'), TP.tien(x, '20'),
                         TP.tien(x, null), TP.tien(x, undefined),
                         TP.tien(x, ''), TP.tien(x, ' xyz ')]);
    })()""")
    lech = [r for r in ra if len(set(r[1:])) != 1]
    assert len(ra) == 16
    assert lech == [], "⛔ (giá trị, VND, '20', null, undefined, '', xyz): " \
        + repr(lech)


# ═══ AC-14 · §5b ⓕ v4.13 — dung sai IN = dung sai đem SO ═══════════════════
@can_node
def test_AC14_F01_hop_GHEP_dung_sai_617_285_in_617_28_va_so_cung_so():
    """⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: in `TP.tien(d.dung_sai, cur)` ⇒
    `617,29` cạnh phép so `61728` xu ⇒ ĐỎ."""
    vuot = _hop_ghep_nhieu_dong(["617.29"], "0.00", curr="VND", ds="617.285")
    ok = _hop_ghep_nhieu_dong(["617.28"], "0.00", curr="VND", ds="617.285")
    for r in (vuot, ok):
        assert 'dung sai <b class="num">617,28</b>' in r["sig"], r["sig"]
        assert "617,29</b><br>" not in r["sig"], r["sig"]
    assert 'lệch <b class="num">617,29</b>' in vuot["sig"], vuot["sig"]
    assert "crit" in vuot["lop"] and vuot["ghep_khoa"] is True, vuot
    assert 'lệch <b class="num">617,28</b>' in ok["sig"], ok["sig"]
    assert "khớp — cho ghép" in ok["sig"] and ok["ghep_khoa"] is False, ok


@can_node
def test_AC14_F01_hop_GHEP_dung_sai_1000_in_1_000():
    r = _hop_ghep_nhieu_dong(["1000.00"], "0.00", curr="VND", ds="1000")
    assert 'dung sai <b class="num">1.000</b>' in r["sig"], r["sig"]
    assert "khớp — cho ghép" in r["sig"], r["sig"]


#: Thân ứng viên **tự nhét** của bài `AC-14` hộp *Tìm tiền* — bài ấy chỉ hỏi
#: dòng *"dung sai Σ"* *(phép IN một chuỗi `dung_sai` bất kỳ như `617.285` —
#: ⛔ phép tính dung sai của cửa)* nên vẫn nhét thân. ⭐ Vì thế khuôn này **có
#: canh**: khoá mỗi ứng viên phải ⊆ khoá cửa thật *(`test_wo022_v3…KHUON_THU…`)*.
#: ⛔ Trước `WO-022` vòng 3 *(`KQ-029` `F-1`)*: `tien`/`lech_tuyet_doi`/`memo`
#: — khuôn hàng thô cửa ⛔ còn trả từ `23/09`.
UV_V2 = {"ung_vien": [{"itl_id": 9, "bac": "gan_tien", "amount": "100.00",
                       "curr": "VND", "lech": "0", "doc_no": "FT",
                       "dien_giai": "x"}]}


def _hop_tim_tien(ds: str, curr: str = "VND") -> str:
    """Hộp *Tìm tiền* **thật** của `F01L` *(`_drawer_tim_tien`)* — trả HTML
    thân hộp."""
    uv = [dict(u, curr=curr) for u in UV_V2["ung_vien"]]
    return _chay(CAY + """
      _TRA['/queue/lenh/PWV-1/itl-candidates'] = {data: {
        dung_sai: %s, ung_vien: %s, bi_cat: false}};
      _TRA['/queue/lenh/PWV-1'] = {no: {cau: 'x'}};
      await F01L._drawer_tim_tien({pm_line_id: 'PWV-1', amount: '100.00',
                                   curr: %s});
      return document.getElementById('dlg-b').innerHTML;
    """ % (json.dumps(ds), json.dumps(uv), json.dumps(curr)),
                 tep=TEP_F01, vo=VO_F01)


@can_node
def test_AC14_F01L_hop_TIM_TIEN_dong_goi_y_dung_sai_617_28():
    """⛔ Chiều ĐỎ *(đã chạy trên `a7fd01f`)*: `TP.tien(d.dung_sai, r.curr)` ⇒
    `617,29` ⇒ ĐỎ."""
    h = _hop_tim_tien("617.285")
    assert "dung sai Σ cho tiền tệ này: <b>617,28</b>" in h, h
    assert "617,29" not in h, h
    h2 = _hop_tim_tien("1000")
    assert "dung sai Σ cho tiền tệ này: <b>1.000</b>" in h2, h2


#: ⭐ Mọi tệp màn **đọc** trường cửa `dung_sai` — `BG` liệt kê từng chỗ in
#: *(Phạm vi (g))*. Một tệp mới đọc `dung_sai` ⇒ bài dưới ĐỎ ⇒ người thêm phải
#: viết bài hành vi `AC-14` cho chỗ in mới rồi mới thêm tên vào đây.
TEP_DOC_DUNG_SAI = ["man_f01.js", "man_f01_lenh.js"]


def test_AC14_moi_tep_doc_dung_sai_DA_LIET_KE_va_doi_xu_bang_SAN():
    """`grep` mọi chỗ đọc `dung_sai` trong `fls/web/tep/*.js`: tập tệp = đúng
    danh sách đã có bài hành vi *(`AC-14` ở trên — hộp *Ghép lệnh* `F01` ·
    hộp *Tìm tiền* `F01L`)*, và mỗi tệp đổi dung sai sang xu bằng **sàn**.

    ⚠ Bài này ⛔ thay bài hành vi — nó chỉ bắt **chỗ in MỚI** chưa có bài.
    ⛔ Chiều ĐỎ: thêm `TP.tien(d.dung_sai, …)` vào một tệp màn khác ⇒ ĐỎ."""
    tep = sorted(t for t in os.listdir(THU_MUC) if t.endswith(".js"))
    doc = [t for t in tep if re.search(r"\bdung_sai\b", _doc(t))]
    print("WO-022 AC-14 · tep doc dung_sai =", doc)
    assert doc, "⛔ không đo được: 0 tệp đọc `dung_sai`"
    assert doc == TEP_DOC_DUNG_SAI, doc
    for t in doc:
        assert re.search(r"TP\.xu\([^()]*dung_sai[^()]*'san'\)|"
                         r"TP\.xu\(\s*ds\s*,\s*'san'\)", _doc(t)), t
