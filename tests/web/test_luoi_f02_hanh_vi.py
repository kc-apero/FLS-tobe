"""⛔⛔ CONG SO 1 cua ca chang `P6`: **tam hanh vi §1 chay THAT tren `F02`**.

`06_SCREEN_SPEC` §1 goi day la *"danh sach nghiem thu **cung**"* va noi thang
hau qua neu thieu mot dong: **ke toan ve Sheets va toan bo FLS thanh rac**.
`DEV-12` §5 dat no la cong so **1** cua ca chang.

⇒ Nen bai nay ⛔ **khong doc ma bang mat**. No dung mot cai DOM toi thieu
*(`dom_gia.js`)*, nap **dung tep man hinh that**, roi **bam phim** va **dan**
nhu nguoi — va soi cai luoi sau do.

★ Cua duoc **gia lap** *(`FLS.doc`/`FLS.ghi` bi thay)*: bai nay hoi *"man hinh
lam dung khong"*, ⛔ khong phai *"cua tra dung khong"* — cau sau la viec cua
`test_vong_f02_pg.py`, chay tren kho THAT qua HTTP THAT.

⛔ Ba thu bai nay ⛔ KHONG kiem duoc *(va vi the con nam o `B7 · UAT`)*: dong
cung khi cuon · **346px** co du · cam giac khi go. Xem dau `dom_gia.js`.
"""
from __future__ import annotations

import os

from fls.web import phuc_vu as pv
# ⭐ Tam hanh vi §1 song o **che do GO**. Xem `khung_node._VE_GO`.
from tests.web.khung_node import DONG, _chay, _o, can_node
from tests.web.khung_node import _VE_GO as _VE


# ── man ve duoc truoc da ─────────────────────────────────────────────────
@can_node
def test_luoi_ve_du_52_cot_va_tieu_de_den_TU_NGUON():
    ra = _chay(_VE + """
      const th = luoi.children.filter(c => c.tagName === 'THEAD')[0];
      return {cot: th.rows[0].cells.map(c => c.textContent),
              dong: than.rows.length};
    """)
    assert ra["dong"] == 3
    # ⛔ Con so nay ⛔ khong go tay: no la do dai `BANG_COT`. Them mot cot ma
    # quen doi day thi bai DO — dung y muon.
    from fls.api.cot_so import BANG_COT
    # ⭐ 25 → **52** ngay 2026-09-03: owner chot *"bang So ITL can du cac
    #   truong thong tin"* ⇒ them **27 vi tri canon** chua co cot nen
    #   (`cot_so.CANON_LEN_LUOI`). ⛔ Quyet dinh cu bo `canon` khoi danh sach
    #   dat tren mot con so CHUA AI DO (*"vai MB"*); do that ra **393 byte/
    #   dong** ⇒ 500 dong ~ 192 KB.
    assert len(ra["cot"]) == len(BANG_COT) == 52
    # ⭐ Ten den tu `ITL Ledge` — ⛔ khong phai chu go tay trong `man_f02.js`.
    assert ra["cot"][0] == "Số dòng ITL"
    assert ra["cot"][1] == "Diễn giải"
    assert "Budget Code · Final ✎" in ra["cot"]
    assert sum(1 for x in ra["cot"] if x.endswith(" ✎")) == 5
    # ⛔⛔ Bon cot `AH..AK` TRUNG TEN het nhau ⇒ tieu de PHAI mang chu cai,
    #   ⛔ khong thi bon cot giong het nhau tren man.
    assert "AH · MID I DoubleCheck LE" in ra["cot"]
    assert "AK · MID I DoubleCheck LE" in ra["cot"]
    assert sum(1 for x in ra["cot"] if "MID I DoubleCheck LE" in x) == 4


@can_node
def test_o_go_duoc_TRONG_KHAC_o_chi_doc_va_o_chua_gan():
    """⛔⛔ Dung lop loi owner bat trong **30 giay** o mui thu 27/08."""
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      const o = than.rows[0].cells[i];
      return {lop: o.className, chu: o.textContent,
              ro: than.rows[0].cells[3].className};
    """)
    assert "edit" in ra["lop"]
    # ⛔ O chua ai gan ⛔ khong duoc trong nhu o rong (`INV-I16`).
    assert "unmapped" in ra["lop"] and ra["chu"] == "chưa gán"
    assert "ro" in ra["ro"] and "edit" not in ra["ro"]


@can_node
def test_ky_DA_CHOT_thi_moi_o_cua_dong_do_la_chi_doc():
    """`INV-I13` — va man phai NOI VI SAO, ⛔ khong chi mo di."""
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      const o = than.rows[2].cells[i];
      return {lop: o.className, vi_sao: o.title};
    """)
    assert "edit" not in ra["lop"] and "ro" in ra["lop"]
    assert "CHỐT" in ra["vi_sao"]


@can_node
def test_cua_CHI_DOC_thi_khong_o_nao_go_duoc_va_man_NOI_RA():
    ra = _chay(_VE + """
      return {edit: document.querySelectorAll('td.edit').length,
              than: than0.textContent};
    """.replace("than0", "document.querySelector('#than-f02')"),
        phien={"actor": "lan@apero.vn", "cho_ghi": False})
    assert ra["edit"] == 0
    assert "CHỈ ĐỌC" in ra["than"]


# ═══ TAM HANH VI §1 ══════════════════════════════════════════════════════

@can_node
def test_hanh_vi_1_dieu_huong_ban_phim():
    """Tab · Enter · bon mui ten — ⛔ khong roi tay khoi ban phim."""
    ra = _chay(_VE + f"""
      const goc = {_o(0, 0)};
      F02.ST.o = goc; goc.classList.add('chon');
      const di = [];
      const bam = k => {{ _PHIM(k); di.push([F02.ST.o.parentNode.rowIndex - 1,
                                             F02.ST.o.cellIndex]); }};
      bam('ArrowRight'); bam('ArrowDown'); bam('Tab'); bam('Enter');
      bam('ArrowLeft'); bam('ArrowUp');
      return di;
    """.replace("_PHIM(k)", "_ban('keydown', {key:k, preventDefault(){}, "
                            "stopPropagation(){}})"),)
    assert ra == [[0, 1], [1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]


@can_node
def test_hanh_vi_1b_khong_di_ra_ngoai_luoi():
    """⛔ Mui ten o mep ⇒ dung yen, ⛔ khong NO, ⛔ khong nhay vong."""
    ra = _chay(_VE + f"""
      const goc = {_o(0, 0)};
      F02.ST.o = goc;
      _ban('keydown', {{key:'ArrowUp', preventDefault(){{}},
                        stopPropagation(){{}}}});
      _ban('keydown', {{key:'ArrowLeft', preventDefault(){{}},
                        stopPropagation(){{}}}});
      return [F02.ST.o.parentNode.rowIndex - 1, F02.ST.o.cellIndex];
    """)
    assert ra == [0, 0]


@can_node
def test_hanh_vi_2_dan_MOT_VUNG():
    """Dan 2×2 tu o dang chon — va **noi so o BI BO** neu roi vao o chi-doc."""
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      F02.ST.o = than.rows[0].cells[i];
      _ban('paste', {clipboardData:{getData:()=> 'HD-1\\tTT-1\\nHD-2\\tTT-2'},
                     preventDefault(){}, stopPropagation(){}});
      return {a: than.rows[0].cells[i].textContent,
              b: than.rows[0].cells[i+1].textContent,
              c: than.rows[1].cells[i].textContent,
              d: than.rows[1].cells[i+1].textContent,
              cho: F02.ST.cho.size,
              tt: document.querySelector('#so-tt').textContent};
    """)
    assert [ra["a"], ra["b"], ra["c"], ra["d"]] == \
        ["HD-1", "TT-1", "HD-2", "TT-2"]
    assert ra["cho"] == 4
    assert "dán 4 ô" in ra["tt"]


@can_node
def test_hanh_vi_2b_dan_vao_o_chi_doc_thi_NOI_RA_so_o_bi_bo():
    """⛔⛔ Dan 4 o ma chi 2 o vao duoc, **im lang**, la cach chac chan nhat de
    mot bang gia tri bi lech mot cot ma ⛔ khong ai biet."""
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Kết thúc DV'));
      F02.ST.o = than.rows[0].cells[i];      // o go duoc CUOI CUNG
      _ban('paste', {clipboardData:{getData:()=> 'X\\tY\\tZ'},
                     preventDefault(){}, stopPropagation(){}});
      return document.querySelector('#so-tt').textContent;
    """)
    assert "dán 1 ô" in ra
    assert "2 ô không gõ được, đã bỏ" in ra


@can_node
def test_hanh_vi_3_keo_xuong():
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      const tren = than.rows[0].cells[i];
      F02.ST.o = tren;
      _ban('keydown', {key:'H', preventDefault(){}, stopPropagation(){}});
      // o vua mo la mot `<input>`; dong no lai bang cach dat thang
      F02.ST.o = than.rows[1].cells[i];
      tren.children = []; tren._txt = 'HD-TREN';
      tren.classList.remove('unmapped');
      _ban('keydown', {key:'d', ctrlKey:true, preventDefault(){},
                       stopPropagation(){}});
      return {duoi: than.rows[1].cells[i].textContent,
              lop: than.rows[1].cells[i].className};
    """)
    assert ra["duoi"] == "HD-TREN"
    assert "chua-luu" in ra["lop"]


@can_node
def test_hanh_vi_4_hoan_tac_khi_o_CHUA_vao_so():
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Chủ dự toán'));
      const o = than.rows[0].cells[i];
      F02.ST.o = o;
      _ban('paste', {clipboardData:{getData:()=> 'CDT-X'},
                     preventDefault(){}, stopPropagation(){}});
      const giua = {chu: o.textContent, cho: F02.ST.cho.size};
      _ban('keydown', {key:'z', ctrlKey:true, preventDefault(){},
                       stopPropagation(){}});
      return {giua: giua,
              sau: {chu: o.textContent, cho: F02.ST.cho.size,
                    lop: o.className}};
    """)
    assert ra["giua"] == {"chu": "CDT-X", "cho": 1}
    # ⭐ Hoan tac keo lai ca gia tri LAN trang thai "chua luu".
    assert ra["sau"]["chu"] == "chưa gán" and ra["sau"]["cho"] == 0
    assert "chua-luu" not in ra["sau"]["lop"]
    assert "unmapped" in ra["sau"]["lop"]


@can_node
def test_hanh_vi_5_loc_CACH_NHIN_khong_doi_du_lieu():
    ra = _chay(_VE + """
      const truoc = than.rows.map(r => r.cells[1].textContent);
      F02._loc('chi B');
      const an = than.rows.map(r => r.style.display);
      F02._loc('');
      return {truoc: truoc, an: an,
              sau: than.rows.map(r => r.cells[1].textContent),
              hien: than.rows.map(r => r.style.display)};
    """)
    assert ra["an"] == ["none", "", "none"]
    # ⛔ Du lieu ⛔ KHONG doi mot ky tu nao — chi CACH NHIN doi.
    assert ra["sau"] == ra["truoc"] == ["chi A", "chi B", "chi C"]
    assert ra["hien"] == ["", "", ""]


@can_node
def test_hanh_vi_6_hai_cot_khoa_duoc_danh_dau_de_dong_cung():
    """⚠ Bai nay kiem **ma**, ⛔ khong kiem hinh: `position:sticky` la chuyen
    cua trinh duyet. *"346px co du khong"* la cau hoi cua `B7 · UAT`."""
    ra = _chay(_VE + """
      const th = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      return {th: [th[0].className, th[1].className],
              td: [than.rows[0].cells[0].className,
                   than.rows[0].cells[1].className]};
    """)
    assert "f1" in ra["th"][0] and "f2" in ra["th"][1]
    assert "f1" in ra["td"][0] and "f2" in ra["td"][1]


@can_node
def test_hanh_vi_7_so_kieu_ke_toan():
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent === 'PS Có');
      return {chu: than.rows[0].cells[i].textContent,
              lop: than.rows[0].cells[i].className,
              th: h[i].className};
    """)
    assert ra["chu"].replace(" ", ".").replace(",", ".") == "1.000.000"
    assert "r" in ra["lop"] and "r" in ra["th"]


@can_node
def test_hanh_vi_8_luu_khong_can_bam_va_KHONG_co_nut_Luu():
    """⭐⭐ `§1-8`: *"Sheets ⛔ khong co nut Luu; app co nut Luu la da thua"*."""
    ra = _chay(_VE + """
      document.querySelector('#so-ly-do').value = 'đối soát tháng 8';
      F02.ST.ly_do = 'đối soát tháng 8';
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      F02.ST.o = than.rows[0].cells[i];
      _ban('paste', {clipboardData:{getData:()=> 'HD-9'},
                     preventDefault(){}, stopPropagation(){}});
      _TRA['/ledger/101/fields/hd'] = {data: {gia_tri: null,
                                              value_source: 'UNMAPPED'}};
      _TRA['/ledger/101/adjust'] = {data: {adj_id: 7, jrn_id: 7}};
      await F02._bay();                      // ⛔ ⛔ khong ai bam nut nao
      return {goi: _GOI.filter(g => g[1].includes('101')),
              lop: than.rows[0].cells[i].className,
              cho: F02.ST.cho.size,
              tt: document.querySelector('#so-tt').textContent};
    """)
    assert ra["cho"] == 0
    assert "da-luu" in ra["lop"] and "chua-luu" not in ra["lop"]
    assert "đã lưu 1 ô" in ra["tt"]
    # ⭐ Ly do di KEM but toan — `INV-I16`.
    ghi = [g for g in ra["goi"] if g[0] == "ghi"]
    assert len(ghi) == 1
    assert ghi[0][2] == {"field": "hd", "value": "HD-9",
                         "reason": "đối soát tháng 8"}


@can_node
def test_khong_co_mot_nut_LUU_nao_tren_man():
    """⛔ Doc ma nguon: mot chu "Lưu" tren mot `<button>` la da thua §1-8."""
    with open(os.path.join(pv.THU_MUC, "man_f02.js"), encoding="utf-8") as f:
        ma = f.read()
    import re
    nut = re.findall(r"TP\.el\('button'[^)]*'([^']*)'\)", ma)
    assert not any(x.strip().lower().startswith("lưu") for x in nut), nut


# ── ⭐ hai o PHAN BO 🔒 — ba ca, ⛔ khong ca nao duoc "chua cho dep" ───────
_PB = """
  const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
  const i2 = h.findIndex(c => c.textContent.startsWith('Phân bổ CFA2'));
  const im = h.findIndex(c => c.textContent.startsWith('Cách phân bổ'));
"""


def _dong_pb(**th):
    d = dict(DONG[0])
    d.update(th)
    return [d]


@can_node
def test_o_phan_bo_LA_CHI_DOC_va_noi_ro_may_suy(): 
    ra = _chay(_VE + _PB + """
      return {lop: than.rows[0].cells[i2].className,
              vi_sao: than.rows[0].cells[i2].title,
              th: h[i2].className};
    """, dong=_dong_pb(alloc_cfa2="SHQ2 | HQ2", alloc_method="No need",
                       alloc_na=False, alloc_cfa1="SHQ2 | HQ2",
                       alloc_can_phan_bo=False))
    assert "ro" in ra["lop"] and "edit" not in ra["lop"]
    # ⛔ Tieu de cot phan bo ⛔ KHONG duoc mang dau ✎ cua o go duoc.
    assert "edit-h" not in ra["th"]
    assert "MÁY suy" in ra["vi_sao"] and "QĐ-ITL-64" in ra["vi_sao"]


@can_node
def test_o_phan_bo_hien_dung_N_A_chu_KHONG_phai_dau_gach():
    """⭐⭐ `#N/A` la mot **CAU TRA LOI**, ⛔ khong phai o rong.

    Doi no thanh `—` la nuot mat dung cai thong tin ke toan can: *"dong nay
    ⛔ khong tra duoc ma hop dong trong danh muc"* (`INV-I16`).
    """
    ra = _chay(_VE + _PB + """
      return {cfa2: than.rows[0].cells[i2].textContent,
              method: than.rows[0].cells[im].textContent,
              lop: than.rows[0].cells[i2].className,
              vi_sao: than.rows[0].cells[i2].title};
    """, dong=_dong_pb(alloc_cfa2="#N/A", alloc_method="#N/A", alloc_na=True,
                       alloc_cfa1="", alloc_can_phan_bo=False))
    assert ra["cfa2"] == "#N/A" and ra["method"] == "#N/A"
    assert ra["cfa2"] != "—"
    assert "CÂU TRẢ LỜI" in ra["vi_sao"]

    # ── day la cho bai nay MANH LEN 04/09 ──────────────────────────────
    # ⭐⭐ `#N/A` phai ve **KHAC** o `chưa gán`. Truoc do ca hai dung chung lop
    #    `unmapped` nen chung trong **y het nhau** tren man, trong khi chung
    #    khac han: `chưa gán` = *"⛔ chua ai gan"* *(viec cho NGUOI)*; `#N/A` =
    #    *"may da tra va ⛔ khong ra"* *(cau tra loi cua MAY)*.
    # ⇒ Rang buoc #3 cua ban thiet ke. Bai cu chi doi "co lop `unmapped`" nen
    #    no van **XANH** trong ca thang hai o trong giong nhau.
    assert "na" in ra["lop"].split()
    assert "unmapped" not in ra["lop"].split(), (
        "o `#N/A` dang dung lai lop cua o `chưa gán` — hai thu se trong "
        "giong het nhau")


@can_node
def test_o_Method_bang_0_hien_dung_chu_0_va_NOI_RA_bay_VLOOKUP():
    """⚠⚠ O `Mapping Master!L` rong THAT ⇒ Sheets tra `0`. So that dang hien
    `0`, nen man cung phai hien `0` — kem cau giai thich."""
    ra = _chay(_VE + _PB + """
      return {method: than.rows[0].cells[im].textContent,
              vi_sao: than.rows[0].cells[im].title};
    """, dong=_dong_pb(alloc_cfa2="SHQ2 | HQ2", alloc_method="0",
                       alloc_na=False, alloc_cfa1="SHQ2 | HQ2",
                       alloc_can_phan_bo=False))
    assert ra["method"] == "0"
    assert "VLOOKUP" in ra["vi_sao"]


@can_node
def test_dai_giai_thich_ba_mau_CO_tren_man():
    """⛔ Mot o doi mau ma ⛔ khong ai noi mau do nghia gi la mot o gay lo."""
    ra = _chay(_VE + """
      return document.querySelector('#than-f02').textContent;
    """)
    for c in ('vàng (chưa lưu)', 'xanh (đã lưu)', 'chưa ai gán', 'chỉ đọc'):
        assert c in ra, c
    assert 'vùng phân bổ = máy suy' in ra


# ══ ⛔⛔ LOC + PHIM = GIA TRI ROI VAO DONG DANG AN ══════════════════════════
# Mot ke toan (agent dong vai, doc `_GUIDE_04`) bat duoc 04/09; ⛔ da kiem lai
# bang may truoc khi tin.
#
# `_loc` chi **giau** dong (`tr.style.display='none'`), con toa do lai dem theo
# **thu tu trong BANG**. ⇒ Khi dang bat mot bo loc — **dung cach dung ma chinh
# man khuyen khich** (nut *"chi UNMAPPED"*) — thi mui ten, `Ctrl+D` va phep dan
# deu roi vao nhung dong ⛔ **khong ai nhin thay**, ma man van bao *"dan 20 o"*.
#
# ⛔ So la **chi-them** (`INV-I08`) ⇒ chua duoc thi phai **dao**, ⛔ khong xoa.

_BA_DONG = [dict(x) for x in DONG]
_BA_DONG[0]["memo"] = "khop mot"
# ⚠ Chu o giua PHAI ⛔ khong chua chuoi loc. Lan dau toi lay "GIAU
#   giua" — ma "giua" **CO** chua "giu" ⇒ ⛔ khong dong nao bi giau, va
#   ba bai duoi se **xanh RONG**: chung se dang do mot canh huong ⛔
#   khong ton tai. ⭐ Do dung la vi sao bai `test_bo_loc_giau_dung_dong_
#   giua` dung ngay tren — no la cai NEO, va chinh no bat duoc loi nay.
_BA_DONG[1]["memo"] = "BO QUA"
_BA_DONG[2]["memo"] = "khop ba"
# ⚠ Dong thu ba cua bo mau chung co **ky DA CHOT** ⇒ moi o cua no la
#   chi-doc (`INV-I13`). Ba bai duoi can mot dong **go duoc** o duoi cung,
#   nen ban SAO nay mo ky ra. ⛔ Bo mau chung giu nguyen — no dang canh
#   mot chuyen khac.
_BA_DONG[2]["period_state"] = "open"
_LOC = "F02._loc('khop');"


@can_node
def test_bo_loc_giau_dung_dong_giua():
    """⭐ Neo cua ba bai duoi: neu phep loc ⛔ khong giau dong giua thi ca ba
    bai kia **xanh rong** — chung se dang do mot canh huong ⛔ khong ton tai."""
    ra = _chay(_VE + _LOC + """
      return than.rows.map(tr => tr.style.display);
    """, dong=_BA_DONG)
    assert ra == ["", "none", ""], ra


@can_node
def test_mui_ten_xuong_NHAY_QUA_dong_bi_giau():
    """⛔ Truoc day mui ten dap vao dong **AN** ⇒ con tro **bien mat khoi mat**
    ma ban phim van an, va phim tiep theo go vao mot dong ⛔ khong ai thay."""
    ra = _chay(_VE + _LOC + f"""
      _ban('click', {{target: {_o(0, 10)}}});
      _ban('keydown', {{key: 'ArrowDown', preventDefault(){{}}}});
      const o = document.querySelector('td.chon');
      return {{itl: o.parentNode.dataset.itl, an: o.parentNode.style.display}};
    """, dong=_BA_DONG)
    # ⚠ DOM gia tra `dataset` nguyen kieu (so), trinh duyet that tra CHUOI
    #   ⇒ so bang `str()` de bai chay dung o ca hai noi.
    assert str(ra["itl"]) == "103", (
        f"⛔ con tro dap vao dong bi giau: {ra}")
    assert ra["an"] != "none"


@can_node
def test_ctrl_D_chep_tu_dong_DANG_THAY_chu_khong_tu_dong_bi_giau():
    """⛔⛔ Day la cho **im lang nhat**: `Ctrl+D` noi la *"lay o ngay tren"*, ma
    *"ngay tren"* khi dang loc phai la **dong dang thay o tren**, ⛔ khong phai
    mot dong da bi giau di."""
    ra = _chay(_VE + _LOC + f"""
      _ban('click', {{target: {_o(0, 10)}}});
      F02._dat({_o(0, 10)}, 'TU-DONG-DANG-THAY');
      _ban('click', {{target: {_o(2, 10)}}});
      _ban('keydown', {{key: 'd', ctrlKey: true, preventDefault(){{}}}});
      return {_o(2, 10)}.textContent;
    """, dong=_BA_DONG)
    assert ra == "TU-DONG-DANG-THAY", f"⛔ chep tu dong bi giau: {ra!r}"


@can_node
def test_dan_TRAN_khoi_vung_dang_hien_thi_PHAI_NOI_ra_bao_nhieu_o_mat():
    """⛔⛔ Dan 3 gia tri khi chi con **2 dong dang hien**: gia tri thu ba
    ⛔ **khong duoc bien mat im lang**.

    ⭐ Truoc day man dem `n` (so o vao duoc) roi bao *"dan 2 o"* — mot cau
    **dung tung chu ma sai y**: nguoi doc vua dan 3 va thay mot con so binh
    thuong, ⛔ khong co gi bao la mot gia tri da roi ra ngoai.
    """
    ra = _chay(_VE + _LOC + f"""
      _ban('click', {{target: {_o(0, 10)}}});
      _ban('paste', {{clipboardData: {{getData: () =>
                       ['A','B','C'].join(String.fromCharCode(10))}},
                     preventDefault(){{}}}});
      return {{tt: document.querySelector('#so-tt').textContent,
              d1: {_o(0, 10)}.textContent, d3: {_o(2, 10)}.textContent,
              giua: {_o(1, 10)}.textContent}};
    """, dong=_BA_DONG)
    assert ra["d1"] == "A" and ra["d3"] == "B", ra
    assert ra["giua"] != "B", f"⛔ gia tri roi vao dong BI GIAU: {ra}"
    assert "TRÀN" in ra["tt"], f"⛔ o thu ba mat IM LANG: {ra['tt']!r}"
