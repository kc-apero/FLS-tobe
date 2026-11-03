"""⛔⛔ `GAP-SCR-07` — **LUU THEO LO**: mot dong trong spec, ca mot co che.

`06_SCREEN_SPEC` §1b khai thang: *"'luu khong can bam' — mot dong. ⛔ La CA
MOT co che: go tiep khi lo truoc dang bay · mang dut giua chung · hai nguoi sua
mot o. Ba ca loi tren **chua duoc dac ta** ⇒ `GAP-SCR-04`"*. `DEV-12 · B5` giao
viec giai o day.

⇒ Ba ca do la ba nhom bai duoi day, **cong them** hai rang buoc ⛔ khong duoc
quen: ⓐ ⛔ **khong ly do thi ⛔ khong ghi** *(`INV-I16`)*, ⓑ ⛔ **cua chi doc
thi ⛔ khong ghi**.

⭐ Va cong ra cua `B5` *(`DEV-12`)* la mot cau do duoc: *"go 20 dong lien tuc
⛔ khong mat mot o nao; **rut mang giua luc luu** thi man hinh noi **ro o nao
chua luu**, ⛔ khong im lang"*. Hai bai cuoi tep nay la dung hai cau ay.
"""
from __future__ import annotations

# ⭐ Bo bai nay chay o **che do GO** — luu theo lo bat dau tu mot cu go
#   TREN LUOI. ⛔ O che do `quet` luoi la chi-doc, nen day se la mot bo
#   test do mot man KHAC.
from tests.web.khung_node import _VE_GO as _VE, _chay, can_node

# Dat mot o cua dong 101 va mot o cua dong 102 vao hang cho.
_HAI_O = _VE + """
  F02.ST.ly_do = 'đối soát tháng 8';
  const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
  const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
  const a = than.rows[0].cells[i], b = than.rows[1].cells[i];
  F02._dat(a, 'HD-A'); F02._dat(b, 'HD-B');
  _TRA['/ledger/101/fields/hd'] = {data:{gia_tri:null, value_source:'UNMAPPED'}};
  _TRA['/ledger/102/fields/hd'] = {data:{gia_tri:null, value_source:'UNMAPPED'}};
"""


# ── ⛔ hai cai phanh ──────────────────────────────────────────────────────
@can_node
def test_KHONG_ly_do_thi_KHONG_mot_but_toan_nao_bay():
    """⭐⭐ `INV-I16`: mot gia tri khong noi vi sao la mot gia tri ⛔ khong truy
    duoc. ⛔ Man ⛔ KHONG duoc tu dat mot ly do mac dinh."""
    ra = _chay(_HAI_O + """
      F02.ST.ly_do = '';
      await F02._bay();
      return {ghi: _GOI.filter(g => g[0] === 'ghi').length,
              cho: F02.ST.cho.size,
              tt: document.querySelector('#so-tt').textContent};
    """)
    assert ra["ghi"] == 0
    # ⭐ Va hai o ⛔ KHONG mat — chung con nguyen trong hang cho.
    assert ra["cho"] == 2
    assert "thiếu lý do" in ra["tt"]


@can_node
def test_cua_CHI_DOC_thi_lo_KHONG_bay():
    ra = _chay(_VE + """
      F02.ST.ly_do = 'x';
      F02.ST.cho.set('101:hd', {itl_id:101, field:'hd', gia_tri:'H',
                                cu:'', td: than.rows[0].cells[0]});
      await F02._bay();
      return {ghi: _GOI.filter(g => g[0] === 'ghi').length,
              tt: document.querySelector('#so-tt').textContent};
    """, phien={"actor": "lan@apero.vn", "cho_ghi": False})
    assert ra["ghi"] == 0
    assert "chỉ đọc" in ra["tt"]


# ── ca ⓐ · GO TIEP KHI LO DANG BAY ───────────────────────────────────────
@can_node
def test_ca_a_go_tiep_trong_luc_lo_dang_bay_thi_vao_LO_SAU():
    """⛔ Phim moi ⛔ khong duoc roi vao lo dang bay *(no se bay voi gia tri
    CU)*, va cung ⛔ khong duoc mat."""
    ra = _chay(_HAI_O + """
      // Cua ghi treo lai cho den khi bo test tha ra.
      let tha;
      const treo = new Promise(r => { tha = r; });
      FLS.ghi = function (duong, t) {
        _GOI.push(['ghi', duong, t]);
        return treo.then(() => ({data:{adj_id:1}, meta:{}}));
      };
      const bay = F02._bay();
      // ⭐ Trong luc lo dang bay: go them mot o NUA.
      const c = than.rows[0].cells[i + 1];      // pay_type cua dong 101
      _TRA['/ledger/101/fields/pay_type'] =
        {data:{gia_tri:null, value_source:'UNMAPPED'}};
      F02._dat(c, 'TT-MOI');
      const giua = F02.ST.cho.size;
      tha(); await bay;
      return {giua: giua, con: [...F02.ST.cho.keys()],
              ghi: _GOI.filter(g => g[0]==='ghi').map(g => g[2].field)};
    """)
    # ⛔ O go them ⛔ khong nam trong lo dang bay…
    assert ra["giua"] == 1
    assert ra["ghi"] == ["hd", "hd"]
    # …va no ⛔ khong mat: no doi lo sau.
    assert ra["con"] == ["101:pay_type"]


@can_node
def test_ca_a_go_DE_LEN_o_dang_bay_thi_phim_MOI_NHAT_thang():
    """⛔⛔ O hong quay lai hang cho — nhung neu nguoi da go de len chinh o ay
    thi ⛔ KHONG duoc de gia tri cu **de nguoc lai** len phim moi."""
    ra = _chay(_HAI_O + """
      HT.mo = () => ({dong(){}});
      let tha; const treo = new Promise(r => { tha = r; });
      FLS.doc = function (duong) {
        _GOI.push(['doc', duong, null]);
        return treo.then(() => { throw new FLS.LoiCua(
          'FLS-MAT-KET-NOI', 0, 'rút mạng'); });
      };
      const bay = F02._bay();
      F02._dat(a, 'HD-MOI-NHAT');          // go de len chinh o dang bay
      tha();
      try { await bay; } catch (e) {}
      return {cho: [...F02.ST.cho.entries()].map(x => [x[0], x[1].gia_tri])};
    """)
    d = dict(ra["cho"])
    # ⛔ Khoa la `itl:field` — khoa chi bang `field` thi hai dong khac nhau
    # de len nhau, va bai kiem se doc nham o.
    assert d["101:hd"] == "HD-MOI-NHAT", ra["cho"]
    assert d["102:hd"] == "HD-B"


# ── ca ⓑ · MANG DUT GIUA CHUNG ───────────────────────────────────────────
@can_node
def test_ca_b_mang_dut_thi_man_NOI_RO_o_nao_chua_luu():
    """⭐⭐ Cong ra cua `B5`: *"rut mang giua luc luu thi man hinh noi RO o nao
    chua luu, ⛔ khong im lang"*.

    ⛔ Mot cai bang *"loi mang"* chung chung la ⛔ khong du: ke toan can biet
    **go lai o nao**, va o day co hai o thi mot o da vao so roi.
    """
    ra = _chay(_HAI_O + """
      const hop = [];
      HT.mo = (t, b, n) => { hop.push([t, b]); return {dong(){}}; };
      let lan = 0;
      const ghi_that = FLS.ghi;
      FLS.ghi = function (duong, t) {
        lan++;
        if (lan === 2) return Promise.reject(
          new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'rút mạng'));
        return ghi_that(duong, t);
      };
      await F02._bay();
      return {hop: hop, cho: [...F02.ST.cho.keys()],
              lop_a: a.className, lop_b: b.className,
              tt: document.querySelector('#so-tt').textContent};
    """)
    # ⛔ O thu nhat DA vao so; o thu hai thi CHUA — va hai o phai trong khac nhau.
    assert "da-luu" in ra["lop_a"] and "chua-luu" not in ra["lop_a"]
    assert "chua-luu" in ra["lop_b"]
    assert ra["cho"] == ["102:hd"]
    assert "1 ô CHƯA vào sổ" in ra["tt"]
    # ⭐ Va hop thoai phai goi TEN o do ra, ⛔ khong noi "co loi".
    assert ra["hop"], "⛔ man ⛔ khong mo mot hop nao — do dung la 'im lang'"
    tieu_de, than = ra["hop"][0]
    assert "DỪNG giữa chừng" in tieu_de
    assert "102" in than and "hd" in than and "HD-B" in than


@can_node
def test_ca_b_lo_DUNG_NGAY_chu_khong_ban_tiep_cac_o_sau():
    """⛔ Mang dut ma van ban tiep 18 o nua la 18 lan cho **cung mot loi**, va
    man se mat cai co hoi noi *"dung o nao"*."""
    ra = _chay(_VE + """
      F02.ST.ly_do = 'x';
      HT.mo = () => ({dong(){}});
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      for (const r of [0, 1, 2]) {
        F02.ST.cho.set(r + ':hd', {itl_id: 100+r, field:'hd', gia_tri:'H',
                                   cu:'', td: than.rows[r].cells[i]});
        _TRA['/ledger/' + (100+r) + '/fields/hd'] =
          {data:{gia_tri:null, value_source:'UNMAPPED'}};
      }
      FLS.ghi = function (duong, t) {
        _GOI.push(['ghi', duong, t]);
        return Promise.reject(new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'rút mạng'));
      };
      await F02._bay();
      return {ghi: _GOI.filter(g => g[0]==='ghi').length,
              cho: F02.ST.cho.size};
    """)
    assert ra["ghi"] == 1, "⛔ lo ⛔ khong dung lai — no ban het ca ba o"
    assert ra["cho"] == 3


# ── ca ⓒ · HAI NGUOI SUA MOT O ───────────────────────────────────────────
@can_node
def test_ca_c_o_da_co_nguoi_khac_go_thi_DUNG_LAI_va_noi_ten_gia_tri_kia():
    """⛔⛔ Cua ghi **KHONG** phat hien duoc viec nay *(`GAP-SCR-09`)* — no chi
    so gia tri go voi **nguon** va **goi y cua may**, ⛔ khong so voi **but
    toan cua nguoi khac**.

    ⇒ Man lam duoc phep no lam duoc: **hoi lai cua ngay truoc khi ghi**. Bai
    nay ghim rang phep hoi ay **co that** va no **dung lo lai**.
    """
    ra = _chay(_HAI_O + """
      const hop = [];
      HT.mo = (t, b) => { hop.push([t, b]); return {dong(){}}; };
      // ⭐ `tay` = gia tri NGUOI KHAC da go. Cua that tra dung truong nay —
      // `test_vong_f02_pg.py` ghim dieu do tren cau tra loi THAT.
      _TRA['/ledger/101/fields/hd'] = {data:{gia_tri:'HD-CUA-THUONG',
                                             tay:'HD-CUA-THUONG',
                                             value_source:'sua_tay'}};
      await F02._bay();
      return {hop: hop, ghi: _GOI.filter(g => g[0]==='ghi').length,
              cho: [...F02.ST.cho.keys()]};
    """)
    assert ra["ghi"] == 0, "⛔ da ghi de len nguoi khac"
    assert ra["cho"] == ["101:hd", "102:hd"]
    # ⭐⭐ Bo test nay bat duoc mot loi THAT: ban dau man dung lai ma
    # `FLS-CONFLICT-SOURCE` cho ca nay, nen no hien cau cua ma do — *"khac voi
    # gia tri NGUON"* — trong khi that ra o bi **mot NGUOI KHAC** go. Hai cau
    # chuyen khac han, va ke toan xu chung khac nhau ⇒ hai hop rieng.
    tieu_de, than = ra["hop"][0]
    assert "NGƯỜI KHÁC" in tieu_de, tieu_de
    assert "HD-CUA-THUONG" in than
    assert "nguồn" not in than.lower().replace("nguồn nói", "")
    # ⚠ Va hop phai KHAI RA rang day chi la mot phep KIEM.
    assert "GAP-SCR-09" in than


@can_node
def test_ca_c_phep_hoi_lai_cua_LA_CO_THAT_truoc_MOI_but_toan():
    """⚠ Neu ai do bo phep hoi nay di *(no ton mot vong goi cho moi o)* thi bai
    nay DO — va do la dieu dung: bo no la bo **lop kiem duy nhat** giua hai
    nguoi cung sua mot o."""
    ra = _chay(_HAI_O + """
      await F02._bay();
      return _GOI.map(g => g[0] + ' ' + g[1]);
    """)
    assert ra == [
        "doc /ledger",
        "doc /ledger/101/fields/hd", "ghi /ledger/101/adjust",
        "doc /ledger/102/fields/hd", "ghi /ledger/102/adjust",
    ], ra


# ── `US-025` · go KHAC NGUON thi HOI NGUOI, ⛔ khong tu `force` ───────────
@can_node
def test_khac_nguon_thi_HOI_NGUOI_chu_khong_tu_dong_ghi_de():
    ra = _chay(_HAI_O + """
      const hop = [];
      HT.mo = (t, b, n) => {
        hop.push([t, b]);
        // ⚠ Chi bam trong hop GHI DE — xem ghi chu o bai duoi.
        if (t.includes('KHÁC')) n[1][1]();
        return {dong(){}};
      };
      let lan = 0;
      FLS.ghi = function (duong, t) {
        _GOI.push(['ghi', duong, t]);
        if (++lan === 1) return Promise.reject(new FLS.LoiCua(
          'FLS-CONFLICT-SOURCE', 409, 'khac nguon', {nguon: 'HD-SO-GOC'}));
        return Promise.resolve({data:{}, meta:{}});
      };
      await F02._bay();
      return {hop: hop, ghi: _GOI.filter(g => g[0]==='ghi').map(g => g[2])};
    """)
    assert len(ra["ghi"]) == 1, "⛔ da tu `force` ma ⛔ khong hoi ai"
    assert "force" not in ra["ghi"][0]
    assert "HD-SO-GOC" in ra["hop"][0][1]
    assert "US-025" in ra["hop"][0][1]


@can_node
def test_nguoi_dong_y_ghi_de_thi_gui_force_KEM_ly_do_RIENG():
    """⭐ Ly do cua phep ghi de la mot ly do **khac** ly do cua dot — no tra
    loi cau *"vi sao ban tin so cua minh hon so goc"*."""
    ra = _chay(_HAI_O + """
      // ⚠ Chi bam nut cua hop GHI DE. `_bao_hong` co nut dau la "Thử lại
      // ngay" — bam no vo dieu kien la mot vong lap vo tan *(da mac: node het
      // bo nho)*, va ⛔ khong nguoi nao bam nhu the.
      HT.mo = (t, b, n) => {
        if (!t.includes('KHÁC')) return {dong(){}};
        const o = document.createElement('input');
        o.id = 'so-de'; o.value = 'PM đã xác nhận lại 03/09';
        document.body.appendChild(o);
        n[0][1]();                      // nguoi bam "Ghi de"
        return {dong(){}};
      };
      let lan = 0;
      FLS.ghi = function (duong, t) {
        _GOI.push(['ghi', duong, t]);
        if (++lan === 1) return Promise.reject(new FLS.LoiCua(
          'FLS-CONFLICT-SOURCE', 409, 'khac nguon', {nguon: 'HD-SO-GOC'}));
        return Promise.resolve({data:{}, meta:{}});
      };
      await F02._bay();
      return _GOI.filter(g => g[0]==='ghi').map(g => g[2]);
    """)
    assert len(ra) == 3          # 101 lan 1 (409) · 101 lan 2 (force) · 102
    assert ra[1]["force"] is True
    assert ra[1]["reason"] == "PM đã xác nhận lại 03/09"
    assert ra[0]["reason"] == "đối soát tháng 8"


@can_node
def test_ghi_de_ma_KHONG_noi_vi_sao_thi_hop_KHONG_dong():
    """⛔ Ham xac nhan tra `false` ⇒ hop **o nguyen**. Nho vay o ly do bat
    buoc ⛔ khong the bi bo qua bang cach bam nhanh (`hop_thoai.js` luat ⓑ)."""
    ra = _chay(_HAI_O + """
      let tra;
      HT.mo = (t, b, n) => {
        if (!t.includes('KHÁC')) return {dong(){}};
        const o = document.createElement('input');
        o.id = 'so-de'; o.value = '   ';          // ⛔ chi toan khoang trang
        document.body.appendChild(o);
        tra = n[0][1]();
        n[1][1]();                                 // roi "De nguyen"
        return {dong(){}};
      };
      FLS.ghi = () => Promise.reject(new FLS.LoiCua(
        'FLS-CONFLICT-SOURCE', 409, 'khac nguon', {nguon: 'X'}));
      await F02._bay();
      return tra;
    """)
    assert ra is False


# ── ⭐ cong ra cua `B5`: 20 dong lien tuc ⛔ khong mat mot o nao ──────────
@can_node
def test_go_20_o_lien_tuc_KHONG_mat_mot_o_nao():
    dong = [
        {"itl_id": 200 + i, "doc_date": "2026-08-01", "doc_no": f"FT-{i}",
         "memo": f"chi {i}", "curr": "VND", "ps_no": None,
         "ps_co": "1000.00", "acct": "R", "le": "V", "le_payer": None,
         "hd": None, "pay_type": None, "cdt1": None, "svc_start": None,
         "svc_end": None, "work_status": "UNMAPPED", "pm_hinh": None,
         "is_flash": True, "period_state": "open", "run_id": "N",
         "source_system": "RAW", "source_sheet": "L1", "source_row": i}
        for i in range(20)
    ]
    ra = _chay(_VE + """
      F02.ST.ly_do = 'gõ 20 dòng liên tục';
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
      for (let r = 0; r < 20; r++) {
        F02._dat(than.rows[r].cells[i], 'HD-' + r);
        _TRA['/ledger/' + (200+r) + '/fields/hd'] =
          {data:{gia_tri:null, value_source:'UNMAPPED'}};
      }
      const truoc = F02.ST.cho.size;
      await F02._bay();
      const ghi = _GOI.filter(g => g[0]==='ghi');
      return {truoc: truoc, ghi: ghi.length,
              gt: ghi.map(g => g[2].value),
              con: F02.ST.cho.size,
              chua_luu: document.querySelectorAll('td.chua-luu').length};
    """, dong=dong)
    assert ra["truoc"] == 20 and ra["ghi"] == 20 and ra["con"] == 0
    assert ra["chua_luu"] == 0
    assert ra["gt"] == [f"HD-{i}" for i in range(20)]
