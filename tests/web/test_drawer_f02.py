"""⛔ CONG: chi tiet DOI SOAT cua `F02` phai la mot **COT BEN PHAI**, va luoi
**⛔ KHONG duoc bi che**.

⛔⛔ **Vi sao bai nay ton tai — hai cau hoi cua owner trong cung mot ngay.**

  ⓐ *"Trong demo dong co panel hien ra cho tung giao dich de ke toan adjust,
    tai sao trong version nay ⛔ khong co?"* ⇒ Do lai: panel **VAN O DO va van
    chay** *(`mo_drawer`, hai cua tra `200`)*, nhung ⛔ **KHONG mot phep thu nao
    tung mo no** *(`grep drawer tests/web` ra **0** bai)*. Theo luat so mot cua
    du an — *"cong chua tung thay do la cong chua biet co song"* — thi truoc bai
    nay ca ngan keo ay la **ma chay ma ⛔ khong ai chung minh duoc**. Va duong
    vao thi vo hinh: chi co `cursor:pointer`, mot dau hieu **chi hien khi chuot
    da o dung tren o**.

  ⓑ *"Day khong phai layout toi mong muon, doc `FLS-Wireframe.html` de hieu."*
    ⇒ Doc `§s-f02`: **`.f02-wrap.split` = `minmax(0,1fr) 430px`**, va cau chot
    nam trong ngoac cua chinh wireframe: *"bam mot dong → chi tiet doi soat
    **truot ra ben phai** (**dong van trong tam mat**)"*.
    ⛔⛔ Ban `B5` dau lam bang `HT.mo` — mot **hop che kin man**. No **chay
    dung** va **sai layout**: hop che mat cai luoi ⇒ moi lan doi soat mot dong
    la mot lan **ra khoi** danh sach roi **quay lai tim cho cu**. ⭐ Mot cai
    hop dung chuc nang van la mot cau tra loi sai cho cau hoi *"ke toan quet
    the nao"*.

★ Va day la lop khuyet tat ma **⛔ khong mot bai test nao truoc do co the bat**:
ca 15 bai `test_luoi_f02_hanh_vi` deu xanh, vi chung kiem **hanh vi cua o**, ⛔
khong kiem **hinh cua man**. ⇒ Nen bai nay kiem dung thu do duoc cua layout:
luoi va panel la **hai o CANH nhau trong mot bo**, ⛔ khong phai mot cai de len
cai kia.

⚠ Bai nay ⛔ khong the kiem *"430px co du rong khong"* hay *"truot co muot
khong"* — do la cau cua `B7 · UAT`.
"""
from __future__ import annotations

import json
import re

from tests.web.khung_node import DONG, _VE, _chay, can_node

# ⭐ Mot dong DAY DU cua cua `GET /ledger/{id}` — ⛔ khong phai dong luoi.
#   Cua don le tra **36 cot canon + moi noi + but toan**, nen dong mau phai
#   mang du cac truong ma `_than_drawer` doc; thieu la bo test dang thu mot
#   panel KHAC panel that.
DONG_DAY = {
    "itl_id": 101, "doc_date": "2026-08-01", "doc_no": "FT-A",
    "memo": "chi A", "curr": "VND", "ps_no": None, "ps_co": "1000000.00",
    "acct": "R | x", "le": "VVOT", "le_payer": None,
    "hd": None, "pay_type": None, "cdt1": "SHQ2 | HQ2",
    "svc_start": None, "svc_end": None,
    "id_payee": None, "invoice": None,
    "hd_thyt": "APR-2026-001",          # ⭐ may goi y — ⛔ chua ai xac nhan
    "sua_tay": {"pay_type": {"value_after": "Dich vu", "actor": "lan@apero.vn",
                             "at": "2026-08-02T09:15:00"}},
    "work_status": "UNMAPPED", "pm_hinh": None, "is_flash": True,
    "period_state": "open", "run_id": "NAP-1", "source_system": "RAW",
    "source_sheet": "L1", "source_row": 1,
    # ⛔ Ca ⓒ cua `fls/ledger/allocate.py`: ⛔ khong tra duoc `hd`.
    "alloc_cfa1": "SHQ2 | HQ2", "alloc_cfa2": "#N/A", "alloc_method": "#N/A",
    "alloc_can_phan_bo": False, "alloc_na": True,
    "canon": [], "moi_noi": [], "da_bo": [], "but_toan": [],
}

# ⭐ `HT.mo` bi thay bang mot cai BAY: neu man con mo hop che de hien chi tiet
#   thi bay nay bat duoc — day chinh la lop loi owner vua chi ra.
_DAT_CUA = """
  _TRA['/ledger/101'] = {data: %s};
  _TRA['/journal'] = {data: {rows: []}};
  const hop = [];
  HT.mo = (t, b, n) => { hop.push([t, b]); return {dong(){}}; };
  HT.loi_trong_hop = e => { hop.push(['LOI', String(e && e.message || e)]); };
""" % json.dumps(DONG_DAY, ensure_ascii=False)

_BAM = """
  _ban('click', {target: than.rows[0].cells[3]});
  await new Promise(r => setTimeout(r, 0));
  await new Promise(r => setTimeout(r, 0));
  await new Promise(r => setTimeout(r, 0));
"""


# ── ⓑ LAYOUT: panel la mot COT BEN PHAI ───────────────────────────────────
@can_node
def test_panel_la_mot_COT_BEN_PHAI_chu_khong_phai_hop_che_man():
    """⭐⭐ Bai chot layout `FLS-Wireframe.html` §`s-f02`.

    Ba dieu phai dung cung luc, va **thieu mot la sai layout**:
      ⓐ bo `#so-wrap` mang lop **`split`** *(CSS bien no thanh hai cot)*
      ⓑ panel `#so-panel` nam **TRONG** `#so-ben` — mot **o em** canh luoi
      ⓒ ⛔ **⛔ KHONG mot lan `HT.mo`** nao — tuc ⛔ khong co hop che man
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const bo = document.querySelector('#so-wrap');
      const ben = document.querySelector('#so-ben');
      return {lop_bo: bo ? bo.className : '(⛔ khong co #so-wrap)',
              co_panel: !!document.querySelector('#so-panel'),
              panel_trong_ben: !!(ben && ben.querySelector('#so-panel')),
              luoi_con_do: !!document.querySelector('#so-luoi'),
              so_hop: hop.length};
    """)
    assert "split" in ra["lop_bo"], ra["lop_bo"]
    assert ra["co_panel"], "⛔ ⛔ khong ve panel nao"
    assert ra["panel_trong_ben"], (
        "⛔ panel ⛔ KHONG nam trong `#so-ben` ⇒ no ⛔ khong phai cot ben phai")
    assert ra["luoi_con_do"], "⛔⛔ luoi bi thay mat — dong ⛔ khong con trong "\
                              "tam mat, dung cai wireframe cam"
    assert ra["so_hop"] == 0, (
        "⛔⛔ man dang mo HOP CHE MAN de hien chi tiet — dung lop loi owner chi "
        f"ra ngay 03/09. So lan goi `HT.mo`: {ra['so_hop']}")


@can_node
def test_truoc_khi_bam_thi_KHONG_co_panel_va_bo_khong_split():
    """⛔ Panel mo san la mot man **mat mot phan ba chieu ngang** cho mot dong
    ⛔ khong ai chon. Luoi la viec chinh; panel la viec **theo yeu cau**."""
    ra = _chay(_DAT_CUA + _VE + """
      const bo = document.querySelector('#so-wrap');
      return {lop: bo.className, co_panel: !!document.querySelector('#so-panel')};
    """)
    assert "split" not in ra["lop"], ra["lop"]
    assert not ra["co_panel"]


@can_node
def test_dong_dang_chon_duoc_danh_dau_va_bam_dong_khac_thi_doi():
    """⭐ *"Dong van trong tam mat"* chi co nghia neu nguoi ta **thay duoc**
    dong nao dang mo. Va chi **mot** dong duoc danh dau."""
    ra = _chay(_DAT_CUA + """
      _TRA['/ledger/102'] = {data: Object.assign({}, %s, {itl_id: 102})};
    """ % json.dumps(DONG_DAY, ensure_ascii=False) + _VE + _BAM + """
      const sau_bam_1 = [than.rows[0].className, than.rows[1].className];
      _ban('click', {target: than.rows[1].cells[3]});
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {mot: sau_bam_1,
              hai: [than.rows[0].className, than.rows[1].className]};
    """)
    assert "chon" in ra["mot"][0] and "chon" not in ra["mot"][1], ra["mot"]
    assert "chon" not in ra["hai"][0] and "chon" in ra["hai"][1], ra["hai"]


@can_node
def test_bam_dong_nao_cung_duoc_khong_rieng_cot_dau():
    """⛔ Wireframe noi *"bam mot **dong**"*, ⛔ khong phai *"bam mot **o**"*.
    Ban truoc chi cot dau moi mo duoc — mot duong vao **hep hon dieu da chot**.
    """
    ra = _chay(_DAT_CUA + _VE + """
      // ⭐ Bam vao o DIEN GIAI (cot 2) — mot o chi-doc giua luoi.
      _ban('click', {target: than.rows[0].cells[2]});
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {co_panel: !!document.querySelector('#so-panel'),
              lop: document.querySelector('#so-wrap').className};
    """)
    assert ra["co_panel"], "⛔ bam giua luoi ⛔ khong mo duoc chi tiet"
    assert "split" in ra["lop"]


@can_node
def test_bam_LAI_dung_dong_dang_mo_thi_KHONG_goi_cua_lan_nua():
    """⛔ Quet bang chuot la bam nhieu. Moi cu bam mot luot goi cua la mot man
    **cham dan theo so lan dung** — va cai cham do ⛔ khong ai nhin thay trong
    mot bai test hanh vi."""
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const lan_1 = _GOI.filter(g => g[1] === '/ledger/101').length;
      _ban('click', {target: than.rows[0].cells[1]});
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {lan_1: lan_1,
              lan_2: _GOI.filter(g => g[1] === '/ledger/101').length};
    """)
    assert ra["lan_1"] == 1, ra
    assert ra["lan_2"] == 1, f"⛔ goi cua {ra['lan_2']} lan cho cung mot dong"


@can_node
def test_nut_Dong_dua_luoi_ve_NGUYEN_chieu_ngang():
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      F02.dong_drawer();
      // ⚠ ⛔ Khong hoi `querySelector('#so-panel')`: khung DOM gia giu mot so
      //   tay chieu theo `id` va ⛔ khong bo khi the bi go ⇒ no se tra ve mot
      //   the DA CHET. Hoi thang cho chua: no con con nao khong.
      const ben = document.querySelector('#so-ben');
      return {lop: document.querySelector('#so-wrap').className,
              con_lai: ben.children.length,
              dong_con_chon: than.rows[0].className};
    """)
    assert "split" not in ra["lop"], ra["lop"]
    assert ra["con_lai"] == 0, f"⛔ panel van con {ra['con_lai']} the"
    assert "chon" not in ra["dong_con_chon"]


# ── ⓐ NOI DUNG panel — no phai la panel THAT ──────────────────────────────
@can_node
def test_panel_mang_du_BAY_NHOM_khong_thieu_nhom_nao():
    """⛔ Thieu mot nhom thi panel **trong nhu day du** — ⛔ khong o dau bao."""
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    # ⭐ Thu tu XEP LAI 04/09: khoi 7 o go duoc len **dau**, so goc 38 cot
    #    xuong **cuoi**. Khoi `① Chứng từ` cu ⛔ khong con — chin o cua no
    #    nay nam trong **digest**, giu lai la hien hai lan cung mot du lieu.
    for nhom in ("Bảy ô gõ được", "PHÂN BỔ", "Mối nối lệnh chi",
                 "Hoá đơn", "Bút toán tay", "Sổ gốc", "Nhật ký"):
        assert nhom in ra, f"⛔ panel THIEU nhom {nhom!r}"
    # ⛔⛔ Va chin o chung tu PHAI con nguyen — o digest. Bo khoi cu ma
    #    ⛔ khong kiem cho nay thi mot ngay chung **bien mat** ma bai van xanh.
    for o in ("Tài khoản", "Pháp nhân thanh toán", "Số chứng từ"):
        assert o in ra, f"⛔ digest THIEU o {o!r} sau khi bo khoi ①"


@can_node
def test_vung_KHONG_CUON_ve_NGAY_truoc_khi_cua_tra_loi():
    """⭐⭐ Wireframe chia panel lam hai: `.dfixed` *(⛔ khong cuon)* va
    `.dscroll`. Vung `.dfixed` chi can **dong da co tren luoi**, nen no ve
    duoc **ngay** ⇒ panel ⛔ khong bao gio la mot khung trong trong luc doi.

    ⛔ Bai nay ⛔ khong `await` gi ca — do la ca diem.
    """
    ra = _chay(_DAT_CUA + _VE + """
      _ban('click', {target: than.rows[0].cells[1]});
      const p = document.querySelector('#so-panel');
      return {co: !!p,
              co_dfixed: !!(p && p.querySelector('.dfixed')),
              chu: p ? p.textContent : ''};
    """)
    assert ra["co"] and ra["co_dfixed"], ra
    assert "1.000.000" in ra["chu"], f"⛔ mat so tien: {ra['chu'][:120]!r}"
    assert "chi A" in ra["chu"], "⛔ mat dien giai"
    assert "101" in ra["chu"]


@can_node
def test_panel_noi_ro_NGUON_noi_gi_vs_NGUOI_go_gi():
    """⭐⭐ Day la ly do panel ton tai (`QĐ-ITL-35`), ⛔ khong phai "xem cho du
    cot": ba nguon cua **cung mot o** phai phan biet duoc.

    ⓐ nguoi go  ⇒ ten nguoi + luc go
    ⓑ so goc noi ⇒ *"so goc noi"*
    ⓒ may goi y  ⇒ *"⛔ chua ai xac nhan"* — ⛔ KHONG duoc trong nhu mot gia
      tri da chot, vi luc ay ke toan se **doi soat voi mot con so may doan**.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-hd');
      return {chu: document.querySelector('#so-panel').textContent,
              // ⚠ O che do QUET, gia tri nam trong O NHAP ⇒ ⛔ khong doc duoc
              //   bang `textContent`. Doc ca hai cho.
              go_hd: ip ? ip.value : '(⛔ khong co o nhap)'};
    """)
    assert "người gõ" in ra["chu"] and "lan@apero.vn" in ra["chu"]
    assert "sổ gốc nói" in ra["chu"]
    assert ra["go_hd"] == "APR-2026-001", (
        f"⛔ mat goi y cua may trong o nhap: {ra['go_hd']!r}")
    assert "chưa ai xác nhận" in ra["chu"], (
        "⛔ goi y cua MAY dang trong nhu mot gia tri DA CHOT")
    # ⛔ Ca ⓒ cua vung phan bo: `#N/A` la mot **cau tra loi** (`INV-I16`).
    assert "#N/A" in ra["chu"] and "Mapping Master" in ra["chu"]


@can_node
def test_cua_NO_thi_loi_nam_TRONG_panel_chu_khong_bat_ra_hop_che_man():
    """⛔ Nguoi dung dang o giua mot cu quet. Mot hop che kin man vi **mot dong
    doc ⛔ khong duoc** thi ⛔ khong phai mot loi bao — no la mot cu **ngat
    viec**."""
    ra = _chay("""
      _TRA['/ledger/101'] = {no: {message: 'kho khong tra loi', cau: 'kho '
        + 'khong tra loi', lam_gi: 'thu lai sau'}};
      _TRA['/journal'] = {data: {rows: []}};
      const hop = [];
      HT.mo = (t, b, n) => { hop.push([t, b]); return {dong(){}}; };
      HT.loi_trong_hop = e => { hop.push(['LOI', '']); };
    """ + _VE + _BAM + """
      const p = document.querySelector('#so-panel');
      return {chu: p ? p.textContent : '(⛔ khong co panel)',
              so_hop: hop.length};
    """)
    assert ra["so_hop"] == 0, (
        f"⛔ bat ra hop che man khi mot dong doc loi ({ra['so_hop']} lan)")
    assert "kho khong tra loi" in ra["chu"], ra["chu"][:200]
    assert "Thử lại" in ra["chu"], "⛔ ⛔ khong co duong di tiep"


# ── duong vao phai TRONG NHU bam duoc ─────────────────────────────────────
@can_node
def test_dong_co_dau_hieu_bam_duoc_thay_duoc_khi_chua_bam_gi():
    """⛔⛔ Bai bat dung khuyet tat owner bat duoc ngay `03/09`.

    ⚠ *"Trong co de thay khong"* la cau cua `B7 · UAT` — bai nay ⛔ khong tra
    loi duoc. No chi khoa dieu **do duoc**: dau hieu phai la **chu**, ⛔ khong
    phai mot hinh do CSS ve — vi mot dau hieu chi song trong CSS thi **bien
    mat trong im lang**, ⛔ khong cong nao thay.
    """
    ra = _chay(_VE + """
      const o = than.rows[0].cells[0];
      return {lop: o.className, chu: o.textContent, title: o.title || ''};
    """)
    assert "mo-duoc" in ra["lop"], ra["lop"]
    assert ra["chu"].startswith("▸ "), (
        f"⛔ mat dau hieu `▸` — {ra['chu']!r}. `cursor:pointer` mot minh ⛔ "
        f"KHONG du: no chi hien khi chuot DA o tren o")
    assert "101" in ra["chu"], "⛔ dau hieu da an mat so dong"
    assert "ĐỐI SOÁT" in ra["title"], ra["title"]


@can_node
def test_chi_dan_nam_TREN_luoi_chu_khong_chi_o_duoi():
    """⛔⛔ Cau chi dan CU van con — nhung no nam **duoi** mot cai luoi dai, tuc
    sau hang tram dong. ⇒ Tren thuc te ⛔ khong ai doc toi, va owner hoi
    *"sao ⛔ khong co panel"*. Bai nay khoa: chi dan phai co o **ca hai** cho.
    """
    ra = _chay("""
      await F02.ve();
      const the = document.querySelector('#than-f02');
      const hd = the.querySelectorAll('header')[0];
      return {tren: hd.innerHTML || hd.textContent,
              ca_the: the.textContent};
    """)
    assert "trượt ra bên phải" in ra["tren"], (
        "⛔ chi dan ⛔ KHONG co o thanh tieu de — cho duy nhat nguoi doc THAY "
        "truoc khi cuon")
    assert "Bấm cột đầu" in ra["ca_the"] or "bấm một dòng" in ra["ca_the"], (
        "⛔ mat luon chu giai duoi luoi")


# ── nut "chi UNMAPPED" cua wireframe ──────────────────────────────────────
@can_node
def test_nut_chi_UNMAPPED_an_dong_da_gan_va_CONG_voi_o_loc():
    """⭐ `FLS-Wireframe.html` §`s-f02` co **hai** dieu khien canh nhau: o loc
    chu + nut **"chi UNMAPPED"**. Ban truoc chi co o loc chu.

    ⛔ Va hai dieu khien phai **CONG** nhau *(giao nhau)*, ⛔ khong phai cai sau
    xoa cai truoc — nguoi ta bat nut roi go them chu de thu hep, chu ⛔ khong
    phai de mo rong lai.
    """
    ra = _chay(_DAT_CUA + _VE + """
      const dong_hien = () => {
        let n = 0;
        for (let i = 0; i < than.rows.length; i++)
          if (than.rows[i].style.display !== 'none') n++;
        return n;
      };
      const truoc = dong_hien();
      document.querySelector('#so-chi-unmapped').onclick();
      const sau = dong_hien();
      F02._loc('chi C');
      const cong = dong_hien();
      document.querySelector('#so-chi-unmapped').onclick();
      return {truoc: truoc, sau: sau, cong: cong, sau_tat: dong_hien()};
    """)
    # ⭐ Ba dong mau: 101/102 `UNMAPPED`, 103 cung `UNMAPPED` *(ky da chot)*.
    assert ra["truoc"] == 3, ra
    assert ra["sau"] == 3, ra
    # ⛔ Cong voi chu "chi C" ⇒ chi con dong 103.
    assert ra["cong"] == 1, f"⛔ hai phep loc ⛔ khong cong nhau: {ra}"
    # ⛔ Tat nut ma van con chu loc ⇒ van la 1, ⛔ khong bat lai ca ba.
    assert ra["sau_tat"] == 1, f"⛔ tat nut da xoa luon o loc chu: {ra}"


# ── ⭐⭐ CONG TAC QUET ↔ GO (owner chot 03/09) ─────────────────────────────
@can_node
def test_mac_dinh_la_che_do_QUET_luoi_9_cot_va_KHONG_o_nao_go_duoc():
    """⭐ Layout owner chi ra: `FLS-Wireframe.html` §`s-f02` — mot **luoi
    quet** ⛔ khong o nao go duoc, moi phep sua nam trong panel.

    ⚠ **Chin cot, ⛔ khong phai tam.** Wireframe ve **mot** cot *"So tien"*;
    so THAT tach **PS No** / **PS Co**, va gop hai cot ay lam mot la mot phep
    **tinh** cua man hinh. ⛔ Man ⛔ khong duoc tinh tien.
    """
    ra = _chay(_VE + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const ten = []; for (let i=0;i<h.length;i++) ten.push(h[i].textContent);
      const lop = []; for (let i=0;i<than.rows[0].cells.length;i++)
        lop.push(than.rows[0].cells[i].className);
      return {so_cot: h.length, ten: ten, lop: lop,
              co_but: ten.filter(x => x.indexOf('✎') >= 0).length};
    """)
    # ⛔ 9 → **10** ngay 04/09: `cdt1` tung bi thieu, ma `06_SCREEN_SPEC` §3
    #   khai luoi Quet CO no — va so goc dem **1.210 o** phai dien o cot ay,
    #   gap hon BON lan cot ke tiep. Con so o day ⛔ khong go tay: no la do
    #   dai `COT_QUET`.
    assert ra["so_cot"] == 10, ra["ten"]
    assert ra["ten"][0].startswith("Số dòng ITL")
    assert "Diễn giải" in ra["ten"][2]
    assert ra["co_but"] == 0, (
        f"⛔ che do QUET van khoe dau `✎` tren tieu de: {ra['ten']}")
    assert not any("edit" in x for x in ra["lop"]), (
        f"⛔⛔ che do QUET van co o GO DUOC tren luoi: {ra['lop']}")


@can_node
def test_bam_cong_tac_thi_sang_che_do_GO_du_cot_va_o_go_duoc_tro_lai():
    """⛔ Cong tac phai **that su doi bang cot**, ⛔ khong chi doi cai nhan."""
    ra = _chay(_VE + """
      const truoc = luoi.children.filter(c=>c.tagName==='THEAD')[0]
                        .rows[0].cells.length;
      document.querySelector('#so-che-do').onclick();
      const l2 = document.querySelector('#so-luoi');
      const h2 = l2.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const lop = []; const r0 = l2.tBodies[0].rows[0];
      for (let i=0;i<r0.cells.length;i++) lop.push(r0.cells[i].className);
      return {truoc: truoc, sau: h2.length,
              nhan: document.querySelector('#so-che-do').textContent,
              so_o_go: lop.filter(x => x.indexOf('edit') >= 0).length};
    """)
    # ⭐ 9 (quet) → **52** (go): 25 cot nen + 27 vi tri canon.
    assert ra["truoc"] == 10 and ra["sau"] == 52, ra
    assert "Gõ" in ra["nhan"], ra["nhan"]
    assert ra["so_o_go"] == 5, (
        f"⛔ che do GO phai co dung 5 o go duoc tren luoi, dang co "
        f"{ra['so_o_go']}")


@can_node
def test_che_do_QUET_thi_panel_LA_CHO_SUA_va_go_vao_do_thi_VAO_HANG_CHO():
    """⭐⭐ *"Panel la cho sua"* phai la mot **phep ghi that**, ⛔ khong phai
    mot o nhap de cho dep.

    ⛔⛔ Va day la lo cu: truoc hom nay moi nhan trong nhom ② deu co dau `✎`
    *(hai o con ghi "chi o day")* nhung ⛔ **khong mot o nhap nao** ⇒ hai truong
    `id_payee`·`invoice` ⛔ **khong sua duoc o BAT KY dau** trong ca san pham.
    Mot dau `✎` ⛔ khong co gi phia sau la mot **loi hua**.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-cdt1');
      ip.value = 'SHQ1 | HQ1';
      // ⚠ `onchange` chu ⛔ KHONG `oninput`: tu 04/09 o trong panel ghi khi
      //   **roi o / Enter**, ⛔ khong theo tung phim. Mot bai goi `oninput`
      //   la mot bai dang thu **hanh vi da bi bo di co chu y**.
      ip.onchange();
      const cho = [];
      F02.ST.cho.forEach(v => cho.push([v.itl_id, v.field, v.gia_tri, v.cu]));
      // ⚠ Khung DOM gia chi hieu `[thuoc-tinh]`, ⛔ khong hieu
      //   `[thuoc-tinh=gia-tri]` ⇒ di len theo cay: input → o phai → `.fld`.
      return {co_o_nhap: !!ip, cho: cho,
              o: ip.parentNode.parentNode.dataset.o,
              lop: ip.parentNode.parentNode.className};
    """)
    assert ra["co_o_nhap"]
    assert ra["cho"] == [[101, "cdt1", "SHQ1 | HQ1", "SHQ2 | HQ2"]], ra["cho"]
    assert ra["o"] == "cdt1", ra
    assert "chua-luu" in ra["lop"], (
        f"⛔ o vua go trong panel ⛔ khong doi mau CHUA LUU: {ra['lop']}")


@can_node
def test_hai_o_CHI_SUA_DUOC_O_PANEL_luon_co_o_nhap_ke_ca_che_do_GO():
    """⛔⛔ `id_payee` va `invoice` ⛔ **khong co cot tren luoi** *(cua
    `GET /ledger` ⛔ khong tra chung)*. ⇒ Neu panel ⛔ khong cho go thi chung
    ⛔ khong sua duoc **o dau ca** — trong khi bang tuyen va `TRUONG_GHI` deu
    noi chung sua duoc. Do la mot lech giua **ban khai** va **san pham**."""
    ra = _chay(_DAT_CUA + """
      F02.ST.che_do = 'go';
    """ + _VE + _BAM + """
      return {payee: !!document.querySelector('#so-go-id_payee'),
              invoice: !!document.querySelector('#so-go-invoice'),
              hd: !!document.querySelector('#so-go-hd'),
              chu: document.querySelector('#so-panel').textContent};
    """)
    assert ra["payee"] and ra["invoice"], ra
    # ⛔ O che do GO thi `hd` sua TREN LUOI ⇒ panel ⛔ khong duoc co o nhap thu
    #   hai cho cung mot o: hai o nhap cho mot gia tri la hai nguon su that.
    assert not ra["hd"], "⛔ che do GO ma panel VAN co o nhap `hd` — hai cho go "\
                         "cho cung mot o"
    assert "sửa trên lưới" in ra["chu"]


@can_node
def test_panel_NOI_RA_rang_chua_co_danh_muc_de_chon():
    """⛔ Wireframe ve mot o **bam-de-chon** lay tu danh muc. Cua
    `GET /catalog` ⛔ **chua ai dac ta** (`GAP-SPEC-01`) ⇒ o day la **go chu**.

    ⭐ Man phai **noi ra**. Ve mot o chon rong roi de ke toan bam vao mot cai
    ⛔ khong mo la lop loi te nhat: no trong nhu mot tinh nang hong, chu ⛔
    khong phai mot tinh nang chua co.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    assert "GAP-SPEC-01" in ra and "chưa ai đặc tả" in ra, ra[:300]


@can_node
def test_doi_che_do_KHONG_lam_mat_o_dang_cho_luu():
    """⛔ Doi cach nhin ⛔ khong duoc lam mat viec dang lam. Mot o vua go ma
    bien mat vi nguoi ta bam nham cong tac la mot **mat du lieu im lang**."""
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-cdt1');
      ip.value = 'SHQ1 | HQ1'; ip.onchange();
      const truoc = F02.ST.cho.size;
      document.querySelector('#so-che-do').onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {truoc: truoc, sau: F02.ST.cho.size};
    """)
    assert ra["truoc"] == 1 and ra["sau"] == 1, ra


# ── ⭐⭐ DU 38 COT cua so goc (cau hoi 1 cua owner, 03/09) ─────────────────
@can_node
def test_panel_hien_DU_38_COT_canon_chu_khong_phai_chin_o():
    """⛔⛔ **Cua VAN LUON tra ve chung — man chi ⛔ khong ve.**

    `GET /ledger/{id}` tra `canon`: mang **38 phan tu** dung thu tu `A..AL`.
    Man cu doc **chin** o trong nhom ①, trong khi chu giai cua chinh no hua
    *"36 cot canon"* ⇒ mot **loi hua** ⛔ khong co gi phia sau — cung lop voi
    dau `✎` cua nhom ②.
    """
    dong = dict(DONG_DAY)
    dong["canon"] = [f"v{i}" for i in range(38)]
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      const hop = [];
      HT.mo = (t, b, n) => { hop.push([t, b]); return {dong(){}}; };
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    for i in (0, 12, 25, 37):
        assert f"v{i}" in ra, f"⛔ thieu gia tri canon vi tri {i}"
    assert "38 cột" in ra


@can_node
def test_khoi_canon_mang_CHU_CAI_vi_BON_o_trung_ten_nhau():
    """⭐ `AH`·`AI`·`AJ`·`AK` deu ten *"MID I DoubleCheck LE"*, va `W/X` trung
    ten voi `AB/AC`. Chi hien TEN thi bon o giong het nhau va ⛔ khong ai biet
    o nao la o nao — dung khuyet tat so 1 ma `fls/canon/spec.py` canh."""
    dong = dict(DONG_DAY)
    dong["canon"] = [f"v{i}" for i in range(38)]
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    for chu in ("AH", "AI", "AJ", "AK", "AB", "AC"):
        assert f'>{chu}</span>' in ra, f"⛔ mat chu cai {chu}"
    assert "ô trống trong khuôn" in ra, (
        "⛔ hai o `Z`/`AA` TRONG co y bi bo di ⇒ nguoi doi chieu se dem lech "
        "vi tri")


@can_node
def test_cua_KHONG_tra_canon_thi_NOI_RA_chu_khong_hien_khoi_rong():
    """⛔ Mot khoi rong trong y het *"dong nay ⛔ khong co du lieu"*. Hai
    chuyen khac han: **cua ⛔ khong tra** vs **so ⛔ khong co**."""
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    assert "không trả cột" in ra, ra[-400:]


# ══ HUONG 1 · DAI PHAN QUYET ══════════════════════════════════════════════
# ⛔⛔ Owner chot 03/09 sau khi xem ban ban y tuong: lam **1 → 4 → 2**.
#
# Van de no giai: ke toan phai **cuon het panel** — 57 dong nhan-gia tri cong
# bon bang, ~2,3 man hinh — moi biet dong dang mo **co viec gi chua xong**.

@can_node
def test_h1_dai_phan_quyet_DEM_dung_so_o_chua_gan_va_o_may_doan():
    """⭐⭐ Hai ca nay **KHAC NHAU va ⛔ khong duoc gop**:

      ⓐ *"⛔ chua ai gan"* — ⛔ khong co gi ca
      ⓑ *"may doan, ⛔ chua ai xac nhan"* — **co mot con so**, nhung ⛔ chua ai
        chiu trach nhiem ve no

    Gop hai ca lam mot thi ke toan se doi soat voi mot con so may doan ma
    tuong la so da chot — dung lop loi `INV-I16` chan.
    """
    dong = dict(DONG_DAY)
    # `hd` rong + co goi y may        ⇒ "may doan" = 1
    # `cdt1` co gia tri that          ⇒ ⛔ khong tinh
    # `pay_type` co `sua_tay`         ⇒ ⛔ khong tinh
    # `svc_start`·`svc_end`·`id_payee`·`invoice` rong han ⇒ "chua gan" = 4
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: [{at:'2026-08-02T09:15', field:'hd',
        value_before:null, value_after:'A', actor:'lan@apero.vn',
        value_source:'UNMAPPED', reason:'x'}]}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      const o = document.querySelector('#so-phan-quyet');
      return {chu: o.textContent, lop: o.className};
    """)
    # ── ⭐ VIET LAI 04/09 theo ban thiet ke ────────────────────────────
    # ⛔⛔ Dai TAM chip bi **cat** — no bay tam tin hieu cung mot luc va cung
    #    mot trong luong. Nhung **phep DEM thi giu nguyen**: hai ca duoi day
    #    van phai **tach**, va do la ca ly do bai nay ton tai.
    assert "còn 4 ô trống" in ra["chu"], ra["chu"]
    assert "1 ô máy gợi ý, chưa ai xác nhận" in ra["chu"], ra["chu"]
    # ⭐ Va cau chu phai noi ro day la **viec dang cho**, ⛔ khong phai su co —
    #    76,6% cuon so o dung trang thai nay.
    assert "không phải sự cố" in ra["chu"], ra["chu"]
    assert "cho" not in ra["lop"], "⛔ vung van dang o trang thai 'dang dem'"


@can_node
def test_h1_dong_SACH_thi_dai_noi_ro_KHONG_CON_VIEC_chu_khong_de_rong():
    """⛔⛔ Mot dai RONG trong y het *"chua tinh xong"*, ma that ra la *"dong
    nay sach"*. Hai chuyen khac han, va cai im lang thi nguy hon."""
    dong = dict(DONG_DAY)
    for f in ("hd", "pay_type", "cdt1", "svc_start", "svc_end",
              "id_payee", "invoice"):
        dong[f] = "co roi"
    dong["sua_tay"] = {}
    dong["hd_thyt"] = None
    dong["alloc_na"] = False
    dong["moi_noi"] = [{"pm_line_id": "PM1", "amount": "1", "hinh": "A",
                        "lan": 1}]
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      const o = document.querySelector('#so-phan-quyet');
      const t = document.querySelector('#so-trang-thai');
      return {chu: o.textContent, lop: t ? t.className : '(⛔ khong co)',
              kt: !!document.querySelector('#so-kiem-tra')};
    """)
    assert "xong" in ra["lop"], ra["lop"]
    assert "Đã phân loại" in ra["chu"], ra["chu"]
    assert "1 lệnh chi đã ghép" in ra["chu"], ra["chu"]
    assert "chưa gán" not in ra["chu"], ra["chu"]
    # ⭐ Va mot dong SACH thi ⛔ khong duoc keo theo bang bao nao.
    assert not ra["kt"], "⛔ dong sach ma van bat bang KIEM TRA"


# ══ ⭐⭐ LUAT BANG BAO — thay bai "moi chip dan di dau" (04/09) ═══════════
#
# ⛔⛔ **Bai cu giu mot tinh chat that:** *"mot chip ⛔ khong dan di dau la mot
# chip noi doi ve chinh viec no lam duoc"*. Nhung ca **dai chip** da bi cat
# theo ban thiet ke — no bay tam tin hieu cung mot luc va cung mot trong luong.
# ⚠ **Cai mat that su la phep NHAY xuong nhom**, va no duoc bu bang viec xep
# lai thu hang: khoi 7 o go duoc nay nam ngay duoi dong trang thai.
#
# ⇒ Tinh chat can canh BAY GIO khac han, va no la tinh chat **quan trong hon**:
# mot bang bao chi dang gia bang **do HIEM** cua no.


@can_node
def test_dong_binh_thuong_thi_KHONG_co_bang_bao_nao():
    """⭐⭐ **7.682 / 10.030 dong (76,6%)** dang o trang thai `chua phan loai`.

    ⛔⛔ Neu trang thai ay keo theo mot bang bao thi man hinh **luc nao cung
    dang keu**, va khi co chuyen THAT thi ⛔ khong con nac nao cao hon de dung.
    Do dung la cai ke toan goi la *"kho nhin"* — va cat 111 dau `⛔` ma van de
    bang bao noi len o day thi ⛔ khong chua duoc gi.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return {kt: !!document.querySelector('#so-kiem-tra'),
              tt: (document.querySelector('#so-trang-thai') || {}).textContent};
    """)
    assert not ra["kt"], (
        "⛔ mot dong `chua phan loai` binh thuong ma van bat bang KIEM TRA — "
        "trang thai cua 76,6% cuon so ⛔ khong duoc ve bang mau bao dong")
    assert "Chưa phân loại" in (ra["tt"] or ""), ra


def _bang_bao(**doi):
    """Ve panel voi mot dong da sua, tra ve chu trong bang bao (hay `None`)."""
    dong = dict(DONG_DAY)
    dong.update(doi)
    return _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      const b = document.querySelector('#so-kiem-tra');
      return {co: !!b, chu: b ? b.textContent : null,
              so_bang: document.querySelectorAll('.kt').length};
    """)


@can_node
def test_ca_hai_ve_tien_khac_0_thi_BAT_bang_bao():
    """⭐ Do that hom nay: **0 dong**. Mot nhanh *"⛔ khong xay ra"* van phai
    co cau tra loi — de roi xuong nhanh khac thi no **chon ho trong im lang**.
    """
    ra = _bang_bao(ps_no="100.00", ps_co="200.00")
    assert ra["co"], "⛔ ca hai ve khac 0 ma ⛔ khong bang bao nao"
    assert "không chọn hộ" in ra["chu"], ra["chu"]


@can_node
def test_ky_da_CHOT_thi_BAT_bang_bao():
    """`INV-I13` — ky chot thi ⛔ khong o nao go duoc, ke ca voi `force`."""
    ra = _bang_bao(period_state="locked")
    assert ra["co"], "⛔ ky da chot ma man ⛔ khong noi gi"
    assert "CHỐT" in ra["chu"], ra["chu"]


@can_node
def test_US_032_chi_bao_khi_hai_ma_CUNG_TU_VUNG():
    """⭐⭐ **Luat nay da phai THU HEP, va con so la ly do.**

    Ban thiet ke viet luat la `le != le_payer`. Do tren kho that: luat ay bao
    tren **1.304 dong (13%)** — ke toan gap bang do **mot tren tam dong**.

    ⛔⛔ Nguyen nhan: hai cot ⛔ **khong noi cung mot tu vung**. `le` co 23 gia
    tri, `le_payer` co 16, trung nhau **44%**; `le` con chua `Cash Treasury`,
    `CN`, `HGO1` — thu ⛔ khong bao gio xuat hien o `le_payer`. **1.225/1.304**
    bao la kieu ay: so **tao voi cam**.

    ⇒ Chi bao khi ca hai thuoc **tu vung CHUNG**. Do lai: **79 dong (0,8%)**.
    """
    dat = "window.FLS_LE_CHUNG = ['SGO2','VVOS','VGOH'];\n"

    # ⓐ hai ma phap nhan THAT, khac nhau ⇒ BAO
    ra = _chay(dat + ("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dict(DONG_DAY, le="SGO2", le_payer="VVOS"),
                     ensure_ascii=False)) + _VE + _BAM + """
      const b = document.querySelector('#so-kiem-tra');
      return b ? b.textContent : null;
    """)
    assert ra and "SGO2" in ra and "VVOS" in ra, (
        "⛔ hai ma phap nhan that khac nhau ma ⛔ khong bao: %r" % (ra,))

    # ⓑ `le` la mot nhan ⛔ KHONG thuoc tu vung chung ⇒ ⛔ KHONG bao
    ra2 = _chay(dat + ("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dict(DONG_DAY, le="Cash Treasury", le_payer="VGOH"),
                     ensure_ascii=False)) + _VE + _BAM + """
      const b = document.querySelector('#so-kiem-tra');
      return b ? b.textContent : null;
    """)
    assert ra2 is None, (
        "⛔ bao tren mot cap ⛔ KHONG cung tu vung (`Cash Treasury` ⛔ khong "
        "phai ma phap nhan) — day dung la 1.225 bao gia da cat: %r" % (ra2,))


@can_node
def test_toi_da_MOT_bang_bao_moi_panel():
    """⛔⛔ **Mot bang bao chi dang gia bang do HIEM cua no.** Hai bang do canh
    nhau thi ca hai deu nhat di — va do la duong cu quay lai.

    ⭐ Nhieu viec cung luc thi gop vao **mot** bang, moi viec mot dong.
    """
    ra = _bang_bao(ps_no="100.00", ps_co="200.00", period_state="locked")
    assert ra["so_bang"] == 1, (
        "⛔ co %s bang bao tren mot panel — luat la toi da MOT"
        % ra["so_bang"])
    assert "không chọn hộ" in ra["chu"] and "CHỐT" in ra["chu"], (
        "⛔ gop mot bang ma lam MAT mot viec: %r" % (ra["chu"],))



# ══ HUONG 4 · XEP DOI O NGAN ══════════════════════════════════════════════
# ══ ⭐⭐ CHIN O CHUNG TU — nay o DIGEST, ⛔ khong con la mot khoi ═════
#
# ⛔⛔ Sau khi xep lai thu hang (04/09), khoi `① Chứng từ` ⛔ **khong bi xoa**:
# ca chin o cua no nam trong **digest** — vung `.dfixed` ⛔ **khong cuon**. Do la
# dieu ke toan xin: cuon xuong go o thu bay **van con thay** ngay, tien, tai
# khoan de doi chieu.
#
# ⚠ Hai bai duoi day doi **cho soi**, ⛔ **khong ha yeu cau**: chin o van phai
# du, va o dai van ⛔ khong duoc bi **cat**.


@can_node
def test_chin_o_chung_tu_deu_o_DIGEST_va_DIGEST_khong_cuon():
    """⭐⭐ Tinh chat that su: **⛔ khong o nao bi mat**, va chung nam o vung
    ⛔ khong cuon.

    ⛔⛔ Bo khoi `①` ma ⛔ khong canh cho nay thi mot ngay chin o ay **bien
    mat** va panel van trong nhu day du — dung kieu mat **im lang** ma ca bo
    phep thu nay ton tai de chan.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const co = document.querySelector('.dfixed');
      const dg = document.querySelector('#so-digest');
      return {co: !!co, chu: co ? co.textContent : '',
              so_o: dg ? dg.children.length : 0};
    """)
    assert ra["co"], "⛔ ⛔ khong co vung `.dfixed`"
    # chin o: tien (No+Co) · tien te · huong · ngay · so chung tu · dien giai
    #         · tai khoan · LE · phap nhan thanh toan
    for o in ("VND", "2026-08-01", "R | x", "Số chứng từ",
              "Tài khoản", "Pháp nhân thanh toán"):
        assert o in ra["chu"], f"⛔ digest THIEU {o!r}: {ra['chu'][:200]!r}"
    assert ra["so_o"] == 3, (
        f"⛔ ba o tham chieu (tai khoan · LE · phap nhan) phai du, dang co "
        f"{ra['so_o']}")


@can_node
def test_gia_tri_DAI_trong_digest_KHONG_BI_CAT():
    """⛔⛔ Mot ma bi cat mot ky tu la **mot ma sai**, va no trong nhu mot ma
    dung. Do that: `acct` dai toi **35** ky tu, `doc_no` toi **40**, `Diễn giải`
    toi **134**. ⇒ Digest phai tra ve gia tri **nguyen van**, phep thu gon la
    viec cua CSS *(`overflow-wrap`)*, ⛔ khong phai cua JS.
    """
    dai_acct = "R | 687160325201_OCBC USD_SGO2xx"      # 35 ky tu
    dai_no = "FT26230301024824-0099-2026-08-0001"       # 40 ky tu
    # ⚠⚠ Digest doc **DONG TREN LUOI** (`ST.theo_id`), ⛔ **khong** phai cau
    #   tra loi cua `GET /ledger/{id}`. Doi cau tra loi don le thi bai se do
    #   **mot thu khac** voi thu no dinh do — da vap dung cho nay hai lan.
    g = dict(DONG[0])
    g["acct"], g["doc_no"] = dai_acct, dai_no
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('.dfixed').textContent;
    """, dong=[g])
    assert dai_acct in ra, f"⛔ `acct` 35 ky tu bi CAT: {ra[:200]!r}"
    assert dai_no in ra, f"⛔ `doc_no` 40 ky tu bi CAT: {ra[:200]!r}"


# ══ HUONG 2 · GAP O RONG, CO DEM ══════════════════════════════════════════
@can_node
def test_h2_o_RONG_duoc_gap_lai_va_dong_gap_MANG_CON_SO():
    """⛔⛔ **Cho de sai nhat cua ca ba huong.** An ma ⛔ KHONG DEM la vi pham
    `INV-I16` — nguoi doc se tuong so chi co 7 cot.

    ⇒ Dong gap phai mang con so, va con so ay phai la con so THAT.
    """
    dong = dict(DONG_DAY)
    # 38 vi tri: `v0` · `v3` · `v10` co gia tri ⇒ **35** o trong.
    canon = [None] * 38
    canon[0] = "v0"
    canon[3] = "v3"
    canon[10] = "v10"
    dong["canon"] = canon
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      const g = document.querySelector('#so-gap-canon');
      return g.textContent;
    """)
    assert "35" in ra, f"⛔ dong gap ⛔ khong noi dung so o trong: {ra!r}"
    assert "ô trống" in ra


@can_node
def test_h2_bam_vao_dong_gap_thi_BUNG_RA_du_o_trong():
    """⭐ Gap ⛔ khong phai xoa. Bam mot cai la thay du — bam lan nua thi thu
    lai."""
    dong = dict(DONG_DAY)
    canon = [None] * 38
    canon[0] = "v0"
    dong["canon"] = canon
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      const n = document.querySelector('#so-nhom-1b');
      const dem = () => n.textContent.length;
      const truoc = dem();
      const g = document.querySelector('#so-gap-canon');
      g.onclick();
      const mo = dem();
      const chu_mo = g.textContent;
      g.onclick();
      return {truoc: truoc, mo: mo, thu: dem(), chu_mo: chu_mo};
    """)
    assert ra["mo"] > ra["truoc"], "⛔ bam vao dong gap ⛔ khong bung ra gi"
    assert ra["thu"] == ra["truoc"], "⛔ bam lan hai ⛔ khong thu lai duoc"
    assert "thu lại" in ra["chu_mo"], ra["chu_mo"]


@can_node
def test_h2_dong_KHONG_co_o_rong_nao_thi_KHONG_ve_dong_gap():
    """⛔ Mot dong gap ghi *"0 ô trống"* la mot dong vo nghia chiem cho."""
    dong = dict(DONG_DAY)
    dong["canon"] = [f"v{i}" for i in range(38)]
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
      return !!document.querySelector('#so-gap-canon');
    """)
    assert ra is False


# ══ ⭐⭐ MOT LUAT CHU + BE RONG ══════════════════════════════════════════════
# ⛔⛔ Owner 04/09: *"Bo font chua nhat quan, trong lon xon kho nhin"* va
# *"khu vuc panel dang nho"*.
#
# ⭐ Do lai thi no ⛔ **khong** lon xon ngau nhien: panel dang chon **kieu chu ·
# hoa-thuong · cach xep** theo **DO DAI gia tri**. Cung mot loai nhan, gia tri
# ngan thi ra `Đ V TIỀN TỆ` *(hoa, chu may)*; gia tri dai thi ra `Tài khoản`
# *(thuong, chu thuong)*. Voi nguoi doc thi hai bo mat ay la ngau nhien.
#
# ⇒ Luat moi: **hinh thuc di theo o do LA GI, ⛔ khong theo gia tri dai ngan.**


@can_node
def test_nhan_trong_panel_KHONG_BAO_GIO_la_ten_truong_trong_may():
    """⛔⛔ **Loi that owner bat duoc tren anh chup.** Panel tung in ra

        `DOC_NO`   `CURR`   `LE_PAYER`

    trong khi ten tieng Viet **da co san** trong ban khai. Nguyen nhan: ban tra
    ten dung `COT()` — bang **da loc theo che do**; o che do Quet no chi con
    **9 cot**, nen ba o nay roi ve nhanh du phong `|| f` va in ra ten truong.

    ⭐ Doi che do thi chung lai **dung** ⇒ cung mot o, **hai cai ten**, va ⛔
    khong ai duoc bao. Do dung la kieu sai `INV-I16` chan: **im lang**.
    """
    # ⭐ Soi **digest** — sau khi xep lai thu hang (04/09), ba o ma loi cu
    #    de dau vet (`doc_no` · `curr` · `le_payer`) nay nam o day.
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('.dfixed').textContent;
    """)
    for xau in ("DOC_NO", "CURR", "LE_PAYER", "doc_no", "curr", "le_payer"):
        assert xau not in ra, f"⛔ panel in ra ten truong trong may: {xau!r}"
    # ⚠ `Đơn vị tiền tệ` ⛔ KHONG con nhan: theo ban thiet ke, don vi tien
    #   nam **ngay canh so tien** (`−1.500.000 VND`) nen mot nhan la chu thua.
    #   ⇒ Kiem gia tri co mat, con nhan thi kiem o hai o CO nhan.
    for ten in ("Số chứng từ", "Tài khoản", "Pháp nhân thanh toán"):
        assert ten in ra, f"⛔ thieu ten that: {ten!r}"
    assert "VND" in ra, "⛔ don vi tien bien mat khoi digest"


@can_node
def test_hai_CHE_DO_cho_panel_CUNG_MOT_bo_ten():
    """⭐ Che do quyet dinh **luoi bay bao nhieu cot**. No ⛔ khong duoc quyet
    dinh **mot o ten la gi** — day la cho lop loi cu chui vao."""
    # ⚠⚠ Soi `.dfixed`, ⛔ **KHONG** soi ca panel. Tieu de khoi 7 o go duoc
    #   **CO Y khac nhau** giua hai che do *("sua O DAY" vs "sua tren luoi")*,
    #   nen so ca panel thi hai che do **luon khac** — va bai se do vi mot ly
    #   do ⛔ khong lien quan gi den TEN O. Digest la cho mang ten o.
    doc = lambda m: _chay((                       # noqa: E731
        "F02.ST.che_do = '%s';" % m) + _DAT_CUA + _VE + _BAM + """
      return document.querySelector('.dfixed').textContent;
    """)
    assert doc("quet") == doc("go")


@can_node
def test_chu_MAY_hay_chu_THUONG_do_BAN_KHAI_quyet_dinh_chu_khong_do_do_dai():
    """⭐⭐ **MOT LUAT CHU cho ca panel**, va day la cho canh no.

    ⛔⛔ **Loi cu:** panel chon kieu chu theo **DO DAI gia tri**. Cung mot
    nhan, gia tri ngan thi ra chu may, gia tri dai thi ra chu thuong — voi
    nguoi doc thi no trong nhu **ngau nhien**, va do dung la cai owner goi la
    *"lon xon"*.

    ⇒ Luat: **hinh thuc di theo o do LA GI**, va cai *"la gi"* den tu **ban
    khai** `VAN_XUOI` (`fls/api/cot_so.py`) — ⛔ khong phai mot phong doan o
    tang man hinh.

    ⚠ 04/09: cho soi doi sang **digest** *(chin o chung tu nay nam o do)*, va
    `Diễn giải` ⛔ khong con la mot cap nhan–gia tri: no la mot doan van rieng
    (`.dmemo`). Nhung co `van` thi **van phai den tu ban khai** — co y giu, vi
    truoc do lop CSS tung tu dat chu thuong, tuc la mot **nguon su that thu
    hai**.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const co = document.querySelector('.dfixed');
      const cap = [];
      const di = function (x) {
        const l = String(x.className || '').split(' ');
        if (l.indexOf('o') >= 0 && x.children.length >= 2)
          cap.push([x.children[0].textContent, x.children[1].textContent,
                    String(x.children[1].className || '')]);
        for (let i = 0; i < (x.children || []).length; i++) di(x.children[i]);
      };
      di(co);
      const m = co.querySelector('.dmemo');
      return {cap: cap, memo_lop: m ? String(m.className) : null,
              memo_chu: m ? m.textContent : null};
    """)
    ten = {x[0]: x for x in ra["cap"]}

    # ⓐ `Diễn giải` la VAN XUOI theo ban khai ⇒ phai mang co `van`
    assert ra["memo_lop"] is not None, "⛔ ⛔ khong co o `Diễn giải` trong digest"
    assert "van" in ra["memo_lop"], (
        "⛔ `Diễn giải` ⛔ khong mang co `van` — co nay PHAI den tu ban khai "
        "`VAN_XUOI`, ⛔ khong phai tu mot lop CSS go tay: %r"
        % (ra["memo_lop"],))

    # ⓑ ma DAI — van phai la chu may (⛔ khong `van`)
    assert "Tài khoản" in ten, f"⛔ thieu o `Tài khoản`: {list(ten)}"
    assert ten["Tài khoản"][1].startswith("R |"), ten["Tài khoản"]
    assert "van" not in ten["Tài khoản"][2], (
        f"⛔ mot MA DAI bi dat chu thuong: {ten['Tài khoản']}")

    # ⓒ ma NGAN — cung la chu may. ⭐ Hai ca ⓑⓒ canh nhau moi chung minh
    #    duoc phep chon ⛔ **khong** theo do dai.
    assert "LE" in ten, f"⛔ thieu o `LE`: {list(ten)}"
    assert "van" not in ten["LE"][2], ten["LE"]

@can_node
def test_ban_khai_van_xuoi_di_kem_TUNG_O_chu_khong_phai_mot_danh_sach_o_man():
    """⛔ Neu man hinh tu giu danh sach *"o nao la van xuoi"* thi no se lech voi
    ban khai — hai ban khai cho mot su that. ⇒ co `van` phai **di theo o**."""
    ra = _chay(_DAT_CUA + _VE + """
      return {cot: (window.FLS_COT || []).filter(k => k.van).map(k => k.nhan),
              canon: (window.FLS_CANON || []).filter(k => k.van)
                       .map(k => k.letter)};
    """)
    assert ra["cot"] == ["Diễn giải"], ra["cot"]
    assert ra["canon"] == ["C"], ra["canon"]


# ══ ⭐ BE RONG — con so 430 phai song tiep, lam SAN ═════════════════════════
def test_430px_van_con_do_lam_SAN_chu_khong_bi_xoa_khi_noi_rong_panel():
    """⛔⛔ **Cho de mat nhat khi noi rong.** `430px` ⛔ khong phai mot con so
    thiet ke tuy y: `06_SCREEN_SPEC` §2 khai no **cho `B7 · UAT` tra loi co du
    hay khong** *(`GAP-SCR-03`)*. Thay no bang mot con so moi la **vut mat cau
    hoi** — va vut mot cach im lang, vi man se trong dep hon.

    ⇒ Noi rong bang `clamp(san, 30vw, tran)`: man hep thi panel **y het hom
    nay**, man rong thi no lon ra. Cau hoi UAT van con nguyen.
    """
    from pathlib import Path
    tep = Path(__file__).resolve().parents[2] / "fls" / "web" / "tep"
    tok = (tep / "tokens.css").read_text(encoding="utf-8")
    hinh = (tep / "hinh.css").read_text(encoding="utf-8")

    assert "--panel-san:430px" in tok, "⛔ con so SAN 430px ⛔ khong con trong ban khai"
    assert "clamp(var(--panel-san)" in hinh.replace("\n", "").replace("  ", ""), \
        "⛔ panel ⛔ khong con lay 430px lam SAN"
    # ⛔ ⛔ khong duoc quay lai mot con so cung — do la cai owner vua keu nho
    assert "minmax(0,1fr) 430px" not in hinh, "⛔ panel lai bi dong cung"
    # ⚠ Trang cung phai het khoa cung — do that: man 1894px, trang khoa 1440
    assert "max-width:var(--trang-tran)" in hinh, "⛔ trang lai bi go so cung"


# ══ ⛔⛔ SO TIEN TREN DAU PANEL ═════════════════════════════════════════════
# Mot ke toan (agent dong vai, doc `_GUIDE_04`) bat duoc 04/09; ⛔ da kiem lai
# bang may **tren so THAT** truoc khi tin.
#
# So goc dien **CA HAI** cot Nợ/Có, mot cot bang `0` — `_GUIDE_04` co vi du
# nguyen van *(`E PS Nợ 4312802240.0` · `F PS Có 0.0`)*. Phep do cu la *"o nao
# KHONG RONG"*, ma so `0` thi ⛔ **khong rong** ⇒ do tren `fls_itl` (10.030
# dong):
#
#   · **3.141** dong `Có` co `ps_no = 0`  ⇒ hien **`−0`**: so tien BOC HOI
#   · **489**   dong `Nợ` co `ps_co = 0`  ⇒ hien **sai dau** (am)
#   ⇒ **3.630 / 10.030 = 36%**
#
# ⚠ Va no ⛔ **khong nhin thay duoc**: 5.105 dong con lai co o **trong that**
# nen hien dung ⇒ mo vai dong bat ky thi moi thu binh thuong.


def _tien(no, co):
    """Ve panel cho mot dong LUOI co `ps_no`/`ps_co` cho truoc.

    ⚠ Dai so tien doc **dong tren luoi** (`ST.theo_id`), ⛔ **khong** phai cau
    tra loi cua `GET /ledger/{id}`. Nen phep do phai doi **dong luoi** — doi
    cau tra loi don le thi bai se do mot thu khac voi thu no dinh do.
    """
    g = dict(DONG[0])
    g["ps_no"], g["ps_co"] = no, co
    return _chay(_DAT_CUA + _VE + _BAM + """
      const a = document.querySelector('#so-panel .amt');
      return {so: a.textContent, am: a.className.indexOf('neg') >= 0,
              dai: document.querySelector('#so-dai-tien').textContent};
    """, dong=[g])


@can_node
def test_dong_CO_co_PS_No_bang_KHONG_van_phai_hien_du_so_tien():
    """⛔⛔ **3.141 dong** roi vao day. Truoc: `0` "khong rong" ⇒ may lay `0`
    lam so tien va gan dau am ⇒ **`−0`**. So tien bien mat khoi cho de nhin
    nhat cua panel, ma dong van trong **binh thuong**."""
    ra = _tien("0.00", "1500000000.00")
    assert "1.500.000.000" in ra["so"], f"⛔ so tien boc hoi: {ra}"
    assert ra["am"], "⛔ dong `Có` phai la RA (am)"


@can_node
def test_dong_NO_co_PS_Co_bang_KHONG_van_phai_hien_dau_DUONG():
    """⛔ **489 dong**. Truoc: `ps_co = 0` "khong rong" ⇒ gan dau **am** cho
    mot dong **Nợ**. Con so thi dung, cai **dau** thi nguoc."""
    ra = _tien("3115456600.00", "0.00")
    assert "3.115.456.600" in ra["so"], ra
    assert not ra["am"], f"⛔ dong `Nợ` bi gan dau am: {ra}"


@can_node
def test_ca_hai_ve_khac_KHONG_thi_may_KHONG_duoc_chon_ho():
    """⭐⭐ Do tren so that hom nay: **0 dong**. Nhung mot nhanh *"hom nay ⛔
    khong xay ra"* van phai co cau tra loi — de roi xuong nhanh khac thi no
    se **chon ho trong im lang**, dung cai loi vua chua."""
    ra = _tien("100.00", "200.00")

    # ⭐⭐ **Bai nay MANH LEN 04/09 theo ban thiet ke.** Truoc do man hien mot
    #    dau `—` cong mot chip canh bao dai — tuc la con so **bien mat** dung
    #    luc no bat thuong nhat, va ke toan phai di tim o khac de biet dong nay
    #    bao nhieu tien. Nay hien **CA HAI ve**: may van ⛔ khong chon ho, va
    #    no noi ra bang cach **cho xem ca hai**, ⛔ khong bang mot dau gach.
    assert "100" in ra["so"] and "200" in ra["so"], (
        f"⛔ mot ve bi giau: {ra['so']!r}")
    assert "Nợ" in ra["so"] and "Có" in ra["so"], (
        f"⛔ hien hai so ma ⛔ khong noi ve nao la ve nao: {ra['so']!r}")
    assert not ra["am"], (
        f"⛔ may da chon mot huong tien: {ra}")
    assert "cả hai vế có tiền" in ra["dai"], (
        f"⛔ dai ⛔ khong noi ra tinh trang nay: {ra['dai']!r}")


@can_node
def test_o_TRONG_THAT_van_chay_dung_nhu_cu():
    """⭐ **5.105 dong** dang chay dung. Mot phep chua ma lam do cho dang dung
    thi ⛔ khong phai mot phep chua."""
    ra = _tien(None, "1000000.00")
    assert "1.000.000" in ra["so"] and ra["am"], ra


# ══ ⭐⭐ BA VIEC KE TOAN XEP UU TIEN (04/09) ════════════════════════════════
# Ca ba deu la **mat viec** hay **rac vinh vien**, ⛔ khong phai chuyen tham my.


@can_node
def test_o_panel_KHONG_ghi_theo_tung_phim_ma_ghi_khi_ROI_O():
    """⛔⛔ Go mot ma nhu `SHQ2 | Headquarters2` la **20 ky tu**, va nguoi ta
    **ngung giua chung de tra bang ma**. Neu o ghi theo tung phim thi ngung
    2,5 giay la may **ghi nua chu vao so** — ma so la **chi-them**
    (`INV-I08`) nen gia tri cut **o lai vinh vien**, va nhat ky `AUD-1` — thu
    dua ra khi co nguoi hoi *"ai doi so nay"* — day gia tri cut.

    ⚠ Che do **Quet la mac dinh**, ma o Quet thi **chi sua duoc trong panel**
    ⇒ day la **loi lam viec chinh**, ⛔ khong phai mot goc khuat.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-cdt1');
      // go **nua chu** — dung canh nguoi ta ngung lai de tra ma
      ip.value = 'SHQ2 | Headquar';
      const giua = F02.ST.cho.size;
      // go not, roi ROI O
      ip.value = 'SHQ2 | Headquarters2';
      ip.onchange();
      const xong = [];
      F02.ST.cho.forEach(v => xong.push(v.gia_tri));
      return {giua: giua, xong: xong};
    """)
    assert ra["giua"] == 0, "⛔ nua chu da vao hang cho ghi"
    assert ra["xong"] == ["SHQ2 | Headquarters2"], ra


@can_node
def test_panel_KHONG_bi_dung_lai_khi_con_nguoi_dang_go_trong_no():
    """⛔ Ve lai panel giua luc dang go la **mat con tro** — o nhap bi dung
    moi, va phim tiep theo roi vao cho ⛔ khong con ai nhan.

    ⭐ Nhung **⛔ khong duoc QUEN** lan ve lai ay: hoan no toi luc nguoi ta roi
    o. Bo quen thi panel noi **so cu** ngay canh o vua doi mau xanh — dung cai
    lop lech `_lam_moi` sinh ra de chan.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-cdt1');
      ip.onfocus();
      const cu = document.querySelector('#so-panel');
      F02._lam_moi(101);
      const trong_luc_go = document.querySelector('#so-panel') === cu;
      ip.onblur();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {trong_luc_go: trong_luc_go,
              sau_khi_roi: document.querySelector('#so-panel') !== cu};
    """)
    assert ra["trong_luc_go"], "⛔ panel bi dung lai duoi tay nguoi dang go"
    assert ra["sau_khi_roi"], "⛔ lan ve lai bi QUEN — panel se noi so cu"


@can_node
def test_go_LY_DO_xong_thi_lo_dang_treo_duoc_HEN_LAI():
    """⛔⛔ Duong di THAT: go vai o → lo bay → cua **NO vi thieu ly do** → man
    chi vao o ly do → nguoi go ly do vao → **⛔ va roi ⛔ khong co gi xay ra
    nua**. May o kia nam vang **vo han**; dong tab di hop la **mat sach**, ma
    trang ⛔ khong co mot loi nhac nao."""
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-cdt1');
      ip.value = 'SHQ1 | HQ1'; ip.onchange();
      clearTimeout(F02.ST.hen); F02.ST.hen = null;   // gia lap: lo da NO
      const ly = document.querySelector('#so-ly-do');
      ly.value = 'đối soát tháng 8'; ly.oninput();
      return {cho: F02.ST.cho.size, hen: F02.ST.hen !== null};
    """)
    assert ra["cho"] == 1, ra
    assert ra["hen"], "⛔ go ly do xong ⛔ khong hen lai — o nam vang vo han"


@can_node
def test_luoi_QUET_co_cot_CHU_DU_TOAN():
    """⛔ `06_SCREEN_SPEC` §3 khai luoi Quet **10 cot** va **CO** `CDT1`.

    ⭐ Do tren kho THAT (10.030 dong): **6.694 dong — hai phan ba so — ⛔ chua
    co `cdt1`**, gan nhu **y het `hd`** *(6.691)*. ⇒ Bay `hd` ma giau `cdt1` la
    mot lua chon **tuy tien**.

    ⚠ Ban dau bai nay ghi *"1.210 o, gap hon BON lan cot ke tiep"* — mot con
    so chep qua hai lop *(`_GUIDE_04` 19/08 → bao cao)* ma ⛔ khong ai do lai.
    Do lai thi **sai**: `cdt1` ⛔ khong he dan dau. Quyet dinh dung, ly do sai.
    """
    ra = _chay(_VE + """
      const th = document.querySelector('#so-luoi')
                   .children.filter(c => c.tagName === 'THEAD')[0];
      return th.rows[0].cells.map(c => c.textContent);
    """)
    assert any("Chủ dự toán" in x for x in ra), ra
    assert len(ra) == 10, ra


# ══ ⭐⭐ GOI Y + KHUON cho o go (04/09) ═════════════════════════════════════
# Truoc hom nay ca **7 o sua duoc** deu la o go chu TRAN.


@can_node
def test_o_hd_co_GOI_Y_tu_danh_muc_va_noi_ro_do_la_ANH_CHUP():
    """⭐ Danh muc **da nam san trong kho** *(`fls_mapping_master`)*, va cua doc
    so **da doc bang ay** ⇒ ⛔ khong can duong ong moi.

    ⚠ Nhung no la **anh chup luc khoi dong**, ⛔ khong phai danh muc song. Mot
    danh sach ⛔ khong noi tuoi cua no la mot danh sach nguoi ta se tin qua muc
    ⇒ o phai noi ca **so ma** lan **luc chup**.
    """
    ra = _chay("window.FLS_DM_HD = ['HD-A','HD-B','NB'];"
               "window.FLS_DM_LUC = '2026-09-04 10:00';"
               + _DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-hd');
      const dl = document.querySelector('#dm-hd');
      return {list: ip.getAttribute('list'),
              n: dl ? dl.children.length : 0,
              chu: ip.parentNode.textContent};
    """)
    assert ra["list"] == "dm-hd", ra
    assert ra["n"] == 3, ra
    assert "3 mã" in ra["chu"], ra["chu"]
    assert "2026-09-04 10:00" in ra["chu"], ra["chu"]


@can_node
def test_danh_muc_RONG_thi_man_NOI_RA_rang_cua_khong_kiem_duoc():
    """⛔⛔ Danh muc rong ⇒ cua ghi cung ⛔ khong kiem duoc. Cho rong ay phai
    **nhin thay duoc o dung cho no co nghia** — ⛔ khong de ke toan tuong minh
    dang duoc kiem trong khi ⛔ khong ai kiem ca."""
    ra = _chay("window.FLS_DM_HD = [];" + _DAT_CUA + _VE + _BAM + """
      const ip = document.querySelector('#so-go-hd');
      // ⚠ `undefined` bi JSON **bo mat khoa** ⇒ bai do vi `KeyError`
      //   chu ⛔ khong phai vi man sai. Ep ve chuoi.
      return {list: ip.getAttribute('list') || '',
              chu: ip.parentNode.textContent};
    """)
    assert not ra["list"], ra
    assert "chưa có danh mục" in ra["chu"], ra["chu"]
    assert "không</b> kiểm" in ra["chu"] or "không kiểm" in ra["chu"], ra["chu"]


@can_node
def test_hai_o_KY_la_o_chon_THANG_chu_khong_phai_o_chon_NGAY():
    """⛔⛔ Ten cot doc la *"Thoi diem bat dau su dung dich vu"* nen rat de
    tuong la NGAY. Do that: **99,8%** gia tri la `YYYYMM` — mot **KY**.

    ⚠ Chinh toi da de xuat *"o chon ngay"* cho hai o nay, va no chi lo ra khi
    **do du lieu that** thay vi doc ten cot. Dat o chon ngay o day la ghi
    `2024-12-01` vao cho so cho doi `202412`.
    """
    ra = _chay(_DAT_CUA + _VE + _BAM + """
      const a = document.querySelector('#so-go-svc_start');
      const b = document.querySelector('#so-go-svc_end');
      return [a.type, b.type];
    """)
    assert ra == ["month", "month"], ra


@can_node
def test_KY_doi_qua_lai_dung_giua_so_va_o_chon_thang():
    """⭐ So giu `YYYYMM`, o chon thang noi `YYYY-MM`. Phep doi phai chay **ca
    hai chieu**: nap sai thi o **trong**, ma mot o trong o day trong y het
    *"⛔ chua ai gan"*; ghi sai thi `2024-12` vao so."""
    d = dict(DONG_DAY)
    d["svc_start"] = "202412"
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(d, ensure_ascii=False)) + _VE + _BAM + """
      const ip = document.querySelector('#so-go-svc_start');
      const nap = ip.value;                    // so -> o
      ip.value = '2025-03'; ip.onchange();     // o  -> so
      let ghi = null;
      F02.ST.cho.forEach(v => { if (v.field === 'svc_start') ghi = v.gia_tri; });
      return {nap: nap, ghi: ghi};
    """)
    assert ra["nap"] == "2024-12", f"⛔ nap tu so vao o SAI: {ra}"
    assert ra["ghi"] == "202503", f"⛔ ghi tu o vao so SAI: {ra}"


# ══ ⭐⭐ BON QUYET DINH CUA OWNER cho BON O CON LAI (04/09) ═════════════════
#   · loai giao dich → suy tu danh sach dang dung, ⛔ KHONG cho dien moi
#   · chu du toan    → suy tu danh sach dang dung, CHO dien moi
#   · ma doi tac     → suy tu danh sach dang dung, CHO dien moi
#   · hoa don        → go tay
#
# ⚠⚠ Ba danh sach dau **SUY TU DU LIEU DANG DUNG**, ⛔ khong phai danh muc —
# khac han `hd` (73 ma, co ban khai that). Hai cho hong da do duoc: no ⛔ khong
# dua ra duoc gia tri **chua ai dung**, va no **dua luon ca loi go cua nguoi
# truoc** *(`id_payee` co **3 nhom** chi khac hoa-thuong)*.

_SUY = ("window.FLS_DM_SUY = {pay_type: ['Thanh toán (Regular)', 'Thu tiền'],"
        " cdt1: ['SHQ2 | Headquarters2', 'COR | TeraSofts'],"
        " id_payee: ['Vd0', 'vd0', 'HAKO']};")


@can_node
def test_loai_giao_dich_la_o_DONG_va_KHONG_go_chu_duoc():
    """⭐ Owner chot: ⛔ **khong** cho dien moi ⇒ mot o **chon**, ⛔ khong phai
    mot o go co goi y. Mot o dong ma trong y het mot o mo thi ke toan se go
    vao roi **moi biet** no ⛔ khong nhan."""
    ra = _chay(_SUY + _DAT_CUA + _VE + _BAM + """
      const o = document.querySelector('#so-go-pay_type');
      return {the: o.tagName,
              muc: o.children.map(function (x) { return x.value; })};
    """)
    assert ra["the"] == "SELECT", ra
    # ⭐ Muc dau la "— chua gan —" (rong) ⇒ **bo gan duoc**, ⛔ khong bi ket.
    # ⚠ `Dich vu` la gia tri DANG CO cua dong mau *(mot but toan tay)*, va no
    #   nam NGOAI danh sach ⇒ no duoc **giu lai lam mot muc**. Do dung la co
    #   che mot bai duoi kiem ky; o day chi ghi nhan la no CO mat.
    assert ra["muc"] == ["", "Dich vu", "Thanh toán (Regular)", "Thu tiền"], ra


@can_node
def test_gia_tri_NGOAI_danh_sach_thi_GIU_NGUYEN_chu_may_KHONG_tu_doi():
    """⛔⛔ **Bẫy im lặng nhất của một ô chọn.** Neu gia tri dang co ⛔ khong nam
    trong danh sach thi `<select>` se nhay ve muc dau tien, roi lan `onchange`
    dau tien **ghi cai muc ay vao so** — mot dong bi doi gia tri **ma ⛔ khong
    ai bam gi ca**."""
    d = dict(DONG_DAY)
    d["pay_type"] = "MOT LOAI CU DA BO"
    d["sua_tay"] = {}
    ra = _chay(_SUY + ("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(d, ensure_ascii=False)) + _VE + _BAM + """
      const o = document.querySelector('#so-go-pay_type');
      return {gia: o.value, n: o.children.length,
              chu: o.parentNode.textContent};
    """)
    assert ra["gia"] == "MOT LOAI CU DA BO", f"⛔ may TU DOI gia tri: {ra}"
    assert ra["n"] == 4, ra          # rong + gia tri la + 2 muc
    assert "ngoài danh sách" in ra["chu"], ra["chu"]


@can_node
def test_chu_du_toan_va_ma_doi_tac_la_o_MO_co_goi_y():
    """⭐ Owner chot: **cho dien moi** ⇒ o go co goi y *(`<datalist>`)*, ⛔ khong
    phai o chon — mot o chon se lam mot chu du toan **moi lap** thanh ⛔ khong
    nhap duoc."""
    ra = _chay(_SUY + _DAT_CUA + _VE + _BAM + """
      const a = document.querySelector('#so-go-cdt1');
      const b = document.querySelector('#so-go-id_payee');
      return {a_the: a.tagName, a_list: a.getAttribute('list') || '',
              b_the: b.tagName, b_list: b.getAttribute('list') || '',
              a_n: (document.querySelector('#dm-cdt1') || {children: []})
                     .children.length};
    """)
    assert ra["a_the"] == "INPUT" and ra["b_the"] == "INPUT", ra
    assert ra["a_list"] == "dm-cdt1" and ra["b_list"] == "dm-id_payee", ra
    assert ra["a_n"] == 2, ra


@can_node
def test_man_goi_dung_ten_no_la_SUY_chu_KHONG_goi_la_danh_muc():
    """⛔⛔ Mot danh sach suy tu du lieu thi ⛔ **khong dua ra duoc gia tri chua
    ai dung**, va no **dua luon ca loi go cua nguoi truoc**. Goi no la *"danh
    muc"* la **noi qua ve thu no biet** — va ke toan se tin theo."""
    ra = _chay(_SUY + _DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-go-cdt1').parentNode.textContent;
    """)
    assert "suy từ" in ra and "2 giá trị đang dùng" in ra, ra
    assert "không</b> phải danh mục" in ra or "không phải danh mục" in ra, ra
    assert "gõ giá trị mới cũng được" in ra, ra


@can_node
def test_muc_chi_khac_HOA_THUONG_thi_man_DANH_DAU_chu_may_KHONG_chon_ho():
    """⭐ Do that: `id_payee` co **3 nhom** chi khac hoa-thuong *(`Vd0`/`vd0`)*.
    ⛔ May ⛔ **khong** duoc gop hay bo bot mot ben — chon la may quyet dinh
    cach viet nao dung, ma do la viec cua NGUOI. ⇒ chi **danh dau**."""
    ra = _chay(_SUY + _DAT_CUA + _VE + _BAM + """
      return {payee: document.querySelector('#so-go-id_payee')
                       .parentNode.textContent,
              cdt1: document.querySelector('#so-go-cdt1')
                      .parentNode.textContent,
              n: document.querySelector('#dm-id_payee').children.length};
    """)
    assert "hoa-thường" in ra["payee"], ra["payee"]
    assert "2 mục" in ra["payee"], ra["payee"]
    # ⛔ ⛔ KHONG bo bot mot ben: ca `Vd0` lan `vd0` deu con trong danh sach
    assert ra["n"] == 3, ra
    # ⭐ `cdt1` sach ⇒ ⛔ khong duoc doi mot loi nhac ⛔ khong co that
    assert "hoa-thường" not in ra["cdt1"], ra["cdt1"]


@can_node
def test_hoa_don_van_la_o_GO_TAY_khong_goi_y_gi():
    """⭐ Owner chot: **gõ tay**. ⛔ Man ⛔ khong duoc tu bay mot goi y o day —
    them mot danh sach ⛔ khong ai yeu cau la them mot thu de tin nham."""
    ra = _chay(_SUY + _DAT_CUA + _VE + _BAM + """
      const o = document.querySelector('#so-go-invoice');
      return {the: o.tagName, list: o.getAttribute('list') || '',
              chu: o.parentNode.textContent};
    """)
    assert ra["the"] == "INPUT" and ra["list"] == "", ra
    assert "suy từ" not in ra["chu"], ra["chu"]


@can_node
def test_khoi_PHAN_BO_ve_BA_trang_thai_KHAC_NHAU():
    """⭐⭐ Rang buoc #3: **o rong**, **`#N/A`** va **co gia tri** la ba
    chuyen khac han, va man phai ve chung **khac nhau**.

    ⛔⛔ Truoc 04/09: `#N/A` ve bang mau **canh bao** ⇒ trong nhu mot **loi**,
    ma no la mot **cau tra loi**; o rong ve bang `—` xam ⇒ trong y het *"⛔
    chua ai gan"*, ma that ra la *"may ⛔ chua ghi gi vao day"*. Hai thu khac
    han bi ve gan giong nhau, va **ca hai bi ve sai loai**.

    ⚠ Bai nay so **HINH**, ⛔ khong so su ton tai — ba trang thai deu "hien
    ra mot cai gi", nen mot phep kiem *"co chu khong"* se xanh mai mai.
    """
    def ve(**doi):
        dong = dict(DONG_DAY)
        dong.update(doi)
        return _chay(("""
          _TRA['/ledger/101'] = {data: %s};
          _TRA['/journal'] = {data: {rows: []}};
          HT.mo = () => ({dong(){}});
        """ % json.dumps(dong, ensure_ascii=False)) + _VE + _BAM + """
          const n = document.querySelector('#so-nhom-3');
          return {chu: n.textContent, ma: n.innerHTML};
        """)

    # ⓐ `#N/A` — vien dut, va NOI RA rang day la mot cau tra loi
    a = ve(alloc_na=True, alloc_cfa1="", alloc_cfa2="#N/A",
           alloc_method="#N/A")
    assert "na-o" in a["ma"], (
        "⛔ `#N/A` ⛔ khong mang hinh rieng (`na-o`) — no se trong giong o rong")
    assert "câu trả lồi" in a["chu"], a["chu"][:200]

    # ⓑ o RONG — hinh KHAC han ⓐ
    b = ve(alloc_na=False, alloc_cfa1="", alloc_cfa2="", alloc_method="")
    assert "pb-rong" in b["ma"], (
        "⛔ o rong ⛔ khong mang hinh rieng (`pb-rong`)")
    assert "na-o" not in b["ma"], (
        "⛔ o RONG dang dung hinh cua `#N/A` — hai thu khac han")
    assert "máy chưa ghi gì" in b["chu"], b["chu"][:200]

    # ⓒ CO gia tri — ⛔ khong mang ca hai hinh kia
    c = ve(alloc_na=False, alloc_cfa1="SHQ2 | Headquarters2",
           alloc_cfa2="CDT1", alloc_method="RATE")
    assert "SHQ2 | Headquarters2" in c["chu"], c["chu"][:200]
    assert "na-o" not in c["ma"] and "pb-rong" not in c["ma"], (
        "⛔ o CO gia tri dang mang hinh cua o rong hay `#N/A`")

    # ⭐ Va tieu de phai noi ro ba o nay ⛔ KHONG go duoc — bang CHU, ⛔ khong
    #    chi bang mau (rang buoc #9).
    #
    # ⚠⚠ **Phep kiem dau tien o day QUA LONG, va phep chung-minh-do bat duoc.**
    #    No chi tim chuoi `"không gõ được"` trong `textContent` — ma cau ay
    #    **cung co** trong doan ghi chu o chan khoi. ⇒ Bo han the chu o tieu de
    #    thi bai van XANH. ⇒ Phai soi dung **cai the** (`the-may`), va soi ca
    #    chu trong no: mot the chi co mau ma ⛔ khong co chu thi pham rang buoc
    #    #9 *(mau ⛔ khong bao gio la thu DUY NHAT cho mot nghia)*.
    assert "the-may" in c["ma"], (
        "⛔ tieu de khoi PHAN BO ⛔ khong co the chu `the-may` — ba o may suy "
        "se trong y het ba o nguoi go duoc")
    the = re.search(r'class="the-may"[^>]*>([^<]*)<', c["ma"])
    assert the and the.group(1).strip(), (
        "⛔ the `the-may` RONG CHU — chi con mau cho nghia, pham rang buoc #9")
    assert "không gõ được" in the.group(1), the.group(1)
