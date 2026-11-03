/* ═══════════════════════════════════════════════════════════════════════
   man_f02.js — SO ITL. Luoi quet + drawer doi soat. Buoc `B5` cua `DEV-12`.

   ⛔⛔ **Man dat nhat cua ca chang, va day la ba cho dat.**

     ⓐ **Tam hanh vi Sheets** (`06_SCREEN_SPEC` §1). Thieu mot dong la ke toan
       **ve Sheets** va ca FLS thanh rac. Co che da co mui thu chung minh chay
       duoc tren **38.896 o** *(`QĐ-ITL-66`)* — o day la **port co che ay**,
       ⛔ khong viet lai, ⛔ khong them mot thu vien nao.
     ⓑ **Luu theo LO** (`GAP-SCR-07`) — mot dong trong spec, ca mot co che o
       day. Xem khoi `_bay()`.
     ⓒ **Drawer doi soat**: nguon noi gi vs nguoi go gi (`QĐ-ITL-35`) — hai
       thu nay ⛔ KHONG duoc tron.

   ⭐ Tieu de cot den TU `cot.js` *(sinh tu `fls/api/cot_so.py`)*. ⛔ Trong tep
   nay ⛔ khong mot ten cot tieng Viet nao go tay — co cong quet.

   ⭐ **Vung PHAN BO 🔒 nay VE DUOC** *(03/09)* — hai cot tren luoi + mot khoi
   trong drawer, suy o **may chu** bang `fls/ledger/allocate.py`. ⛔ Truoc do
   toi ghi *"⛔ khong cua nao mang no"* va **do la mot cau chua do**: luat
   `suy_allocate` da co, `fls_mapping_master` da co **73 ma** trong kho — thieu
   duy nhat mot phep gan o tang doc. ⇒ Man ⛔ khong con phai xin loi vi mot o
   trong.

   ⚠⚠ **Hai cho man nay CO Y ⛔ khong ve, va no NOI RA thay vi de trong:**
     · **Hai nguoi sua mot o** — cua ghi ⛔ **KHONG** phat hien duoc *(do o
       `GAP-SCR-09`)*. Man lam duoc mot phep **kiem truoc khi ghi**, va no la
       mot phep kiem, ⛔ khong phai mot bao dam.
     · **`id_payee` / `invoice`** ⛔ khong co tren luoi — cua `GET /ledger`
       ⛔ khong tra hai truong do. Chung go o **drawer**.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F02 = (function () {

  /* ⓼ Gom lo: 2,5 giay khong go them thi ban di. Con so nay tu rang buoc da
     do — load-job APPEND **~2–4s/lan** ⇒ ⛔ cam ghi moi o mot lan. */
  const CHO_MS = 2500;
  const TRANG = 200;

  const ST = {
    dong: [],           // dong dang hien (theo thu tu luoi)
    theo_id: new Map(), // itl_id -> dong
    con_tro: null,
    o: null,            // o dang chon (`<td>`)
    lich: [],           // ⓸ ngan xep hoan tac
    cho: new Map(),     // "itl:field" -> {itl_id, field, gia_tri, cu, td}
    hen: null,
    dang_bay: false,
    ly_do: '',
    hong: [],           // o cua lo truoc ⛔ khong luu duoc
    loc: '',            // chu dang loc (giu lai de nut UNMAPPED cong vao)
    chi_unmapped: false, // nut "chi UNMAPPED" (`FLS-Wireframe` §`s-f02`)
    // ⭐⭐ HAI CHE DO — owner chot 03/09 khi doi chieu voi `FLS-Wireframe`.
    //   `quet` = luoi 9 cot CHI DOC, **panel la cho sua** (dung wireframe).
    //   `go`   = luoi du 25 cot, **go thang tren luoi** (8 hanh vi §1 song).
    // ⛔ Mac dinh la `quet` vi do la layout owner chi ra; `go` cach mot cu bam.
    che_do: 'quet'
  };

  // ⭐ Chin cot cua che do QUET — lay tu `FLS-Wireframe.html` §`s-f02`
  //   *(itl_id · Ngay · Dien giai · So tien · TK · LE · HDCode · Trang thai)*.
  // ⚠ **Mot cho lech co y, va no phai noi ra:** wireframe ve **mot** cot
  //   *"So tien"*; so THAT tach **PS No** va **PS Co**, va gop hai cot ay lam
  //   mot la mot phep **tinh** cua man hinh — man ⛔ khong duoc tinh tien.
  //   ⇒ Giu hai cot. Va chung deu la cot DA KHAI trong `cot_so.py`, nen cong
  //   #15 van soi duoc; mot cot bia ra o day se lam cong ay do.
  /* ⛔⛔ `cdt1` tung bi **thieu o day** (bat duoc 04/09). `06_SCREEN_SPEC`
     §3 khai luoi Quet **10 cot** va CO `CDT1`; toi lam **9**.

     ⭐ Ly do no phai co: no la mot trong **5 truong engine P&L doc**, va do
     tren kho THAT (10.030 dong) thi **6.694 dong — hai phan ba so — ⛔ chua
     co `cdt1`**, gan nhu **y het `hd`** *(6.691, lech 3 dong)*. ⇒ Bay `hd` ma
     giau `cdt1` la mot lua chon **tuy tien**: hai cot cung mot muc do do dang.

     ⚠ Ban dau toi ghi o day *"1.210 o, gap hon BON lan cot ke tiep"* — chep
     lai tu `_GUIDE_04` (19/08) qua mot bao cao. **Do lai thi sai**: chinh tep
     xuat 26/08 dem `501`, con kho that thi `cdt1` **⛔ khong he** dan dau —
     `id_payee` 9.600 va `invoice` 8.608 deu tren no. Quyet dinh van dung, ly
     do thi phai sua. */
  const COT_QUET = ['itl_id', 'doc_date', 'memo', 'ps_no', 'ps_co', 'acct',
                    'le', 'hd', 'cdt1', 'work_status'];

  // ⭐ Bang cot cua che do dang xem. ⛔ `COT_QUET` chi **loc** bang that theo
  //   thu tu wireframe — no ⛔ khong tao ra mot cot nao ⇒ cong #15 van do duoc.
  const COT_DU = () => (window.FLS_COT || []);
  const COT = () => (ST.che_do === 'quet'
    ? COT_QUET.map(f => COT_DU().find(k => k.truong === f)).filter(Boolean)
    : COT_DU());
  const quet = () => ST.che_do === 'quet';
  // ⛔ Con so "N o go duoc" SUY tu bang cot, ⛔ khong go tay: `QĐ-ITL-64` da ha
  // 10 → 7 mot lan, va mot con so go tay se ke lai con so cu mai mai.
  const GO_TREN_LUOI = () => COT_DU().filter(k => k.go);
  const cho_ghi = () => !!(window.FLS_PHIEN || {}).cho_ghi;

  function _khoa(itl_id, field) { return itl_id + ':' + field; }

  /* ═══ ve khung ══════════════════════════════════════════════════════ */

  function ve(o) {
    o = o || TP.$('#than-f02');
    return TT.chay(
      o,
      () => FLS.doc('/ledger', { limit: TRANG }),
      (d, meta, dich) => _ve(d, meta, dich),
      {
        so_dong: 12,
        la_rong: d => !d || !d.rows || d.rows.length === 0,
        rong: {
          tieu_de: 'Sổ ITL trống trong phạm vi này',
          than: 'Phạm vi đang xem là <b>lần nạp thật</b>. Sổ rỗng không '
              + 'phải lỗi — nó có nghĩa là <b>chưa lần nạp nào chạy</b>, hay '
              + 'lần nạp đã chạy không có dòng nào. Hai chuyện khác nhau, '
              + 'và màn không đoán thay.'
        }
      });
  }

  function _ve(d, meta, o) {
    ST.dong = d.rows || [];
    // ⛔⛔ `next_cursor`, ⛔ KHONG `cursor` — cung cai bay da mac o `F01`
    // (`GAP-SPEC-02`): tham so GUI LEN ten la `cursor`, truong TRA VE ten la
    // `next_cursor`. Doc nham thi nut "Xem thêm" ⛔ khong bao gio hien.
    ST.con_tro = d.next_cursor || null;
    ST.theo_id = new Map(ST.dong.map(x => [x.itl_id, x]));
    o.textContent = '';
    o.appendChild(_thanh(meta));
    // ⭐⭐ **MASTER–DETAIL — day la layout `FLS-Wireframe.html` §`s-f02` chot:**
    //   *"**Quet** ben trai, bam mot dong → **chi tiet doi soat truot ra ben
    //   phai** (dong VAN trong tam mat)"*.
    //
    // ⛔⛔ Ban `B5` dau tien toi lam ngan keo bang `HT.mo` — mot **hop che kin
    //   man**. Chay thi dung, nhung no **pha dung cai cau wireframe ghi trong
    //   ngoac**: hop che mat cai luoi ⇒ ke toan mat cho minh dang dung, va moi
    //   lan doi soat mot dong la mot lan **ra khoi** danh sach roi **quay lai
    //   tim cho cu**. Owner mo man ngay 03/09 va noi *"day khong phai layout
    //   toi mong muon"* — dung cho.
    // ⇒ Panel la mot **cot ben phai**, `sticky`, va luoi **⛔ khong bi che**.
    const bo = TP.el('div', 'f02-wrap');
    bo.id = 'so-wrap';
    bo.appendChild(_the_luoi());
    const ben = TP.el('div');
    ben.id = 'so-ben';
    bo.appendChild(ben);
    o.appendChild(bo);
    o.appendChild(_ghi_chu());
    _noi_ban_phim();
  }

  /* ── thanh dieu khien: loc view · O LY DO · trang thai luu ──────────── */
  function _thanh(meta) {
    const c = TP.el('div', 'card');
    const p = TP.el('div', 'pad stack');

    const h1 = TP.el('div', 'row');
    h1.style.alignItems = 'center';

    const loc = TP.el('input', 'inp');
    loc.placeholder = 'lọc cách nhìn (gõ để ẩn dòng không khớp)…';
    loc.style.minWidth = '260px';
    loc.oninput = () => _loc(loc.value);
    h1.appendChild(loc);

    // ⭐ `FLS-Wireframe.html` §`s-f02` co **hai** dieu khien canh nhau trong
    //   mot `.band`: o loc + nut **"chi UNMAPPED"**. Nut nay la duong ngan
    //   nhat tu *"co 200 dong"* den *"co 37 dong CAN toi"*.
    const nut = TP.el('button', 'b tiny', 'chỉ UNMAPPED');
    nut.id = 'so-chi-unmapped';
    nut.title = 'Chỉ hiện dòng CHƯA ai gán. Đây là phép lọc CÁCH NHÌN — '
              + 'nó ẩn dòng, không đổi một ký tự dữ liệu nào.';
    nut.onclick = function () {
      ST.chi_unmapped = !ST.chi_unmapped;
      if (ST.chi_unmapped) nut.classList.add('pri');
      else nut.classList.remove('pri');
      nut.setAttribute('aria-pressed', ST.chi_unmapped ? 'true' : 'false');
      _loc();
    };
    h1.appendChild(nut);

    /* ⭐⭐ CONG TAC QUET ↔ GO — owner chot 03/09 sau khi doi chieu wireframe.

       ⛔⛔ **Vi sao PHAI la hai che do, ⛔ khong phai chon mot.** `FLS-Wireframe`
       §`s-f02` ve mot **luoi quet** ⛔ khong o nao go duoc, moi phep sua nam
       trong panel. Nhung `06_SCREEN_SPEC` §1 la mot **danh sach nghiem thu
       cung**: tam hanh vi Sheets *(dan vung · keo xuong · hoan tac · di bang
       ban phim)* chi song duoc khi go **tren luoi**. ⇒ Bo mot trong hai la
       **lat mot cam ket da chot** — nen may ⛔ khong duoc tu chon, va owner
       chon **ca hai co cong tac**.

       ⚠ Doi che do **⛔ khong dung** dot go dang cho: `ST.cho` giu nguyen, nen
       nhung o vua go van bay theo dung hen 2,5 giay.                        */
    const ct = TP.el('span', 'chip');
    ct.id = 'so-che-do';
    ct.title = 'Quét = lưới 9 cột chỉ-đọc, sửa trong panel bên phải '
             + '(FLS-Wireframe §s-f02).\nGõ = lưới đủ 25 cột, gõ thẳng trên ô '
             + '8 hành vi Sheets (06_SCREEN_SPEC §1).';
    const _ve_ct = function () {
      ct.textContent = quet() ? '▤ Quét · lưới chỉ-đọc'
                              : '✎ Gõ · lưới sửa được';
      ct.className = quet() ? 'chip info' : 'chip signed';
    };
    ct.onclick = function () {
      ST.che_do = quet() ? 'go' : 'quet';
      _ve_ct();
      // ⛔ Ve lai CA man: doi che do la doi bang cot, ma tieu de/o/lop dong
      //   cung deu suy tu bang cot.
      const bo = TP.$('#so-wrap');
      if (bo) {
        const cu = bo.children[0];
        const moi = _the_luoi();
        bo.removeChild(cu);
        bo.insertBefore(moi, bo.children[0]);
        if (_dang_xem !== null) _danh_dau(_dang_xem);
      }
      _loc();
      if (_dang_xem !== null) { const i = _dang_xem; _dang_xem = null;
                               mo_drawer(i); }
    };
    _ve_ct();
    h1.appendChild(ct);

    h1.appendChild(TP.el('span', 'spacer'));
    h1.appendChild(TP.el('span', 'muted',
      TP.chip_niem_tin((meta || {}).data_status || 'flash')
      + ' <span style="font-size:12px">' + ST.dong.length + ' dòng'
      + (ST.con_tro ? ' còn nữa' : ' hết') + '</span>'));
    p.appendChild(h1);

    /* ⭐⭐ O LY DO — va vi sao no nam NGAY TREN luoi chu ⛔ khong trong mot
       hop hien ra luc luu.

       `INV-I16` doi **moi phep ghi phai co ly do** *(cua ghi NO neu thieu —
       da do)*. Nhung §1 hanh vi 8 doi **⛔ khong co nut Luu**. Hai dieu ay
       dung nhau: hoi ly do moi lan ban lo la mot cai nut Luu doi ten.

       ⇒ Ke toan noi ly do **MOT LAN** cho ca dot go, va no **nam thay tren
       man suot dot** de ⛔ khong bao gio thanh mot cau cu ky ma khong ai
       thay. Doi viec thi sua o nay. ⛔ Man ⛔ KHONG tu dat mot ly do mac dinh
       kieu *"sua tren luoi F02"* — mot ly do khong noi gi la mot ly do gia,
       va no lam hong dung cai `AUD-1` dung ra de giu. */
    const h2 = TP.el('div', 'note');
    h2.style.margin = '0';
    h2.innerHTML =
      '<div style="font-size:12px;margin-bottom:6px"><b>Lý do của đợt '
      + 'sửa này</b> — đi kèm <b>mọi</b> ô bạn gõ, vào nhật ký. Máy '
      + 'không tự đặt lý do thay bạn.</div>';
    const ip = TP.el('input', 'inp');
    ip.id = 'so-ly-do';
    ip.style.width = '100%';
    ip.placeholder = 'ví dụ: đối soát tháng 8 theo bảng PM của Thương';
    ip.value = ST.ly_do;
    ip.oninput = () => {
      ST.ly_do = ip.value.trim();
      /* ⛔⛔ **Loi that.** Truoc day cho nay chi goi `_tt()` (ve lai dong
         trang thai). Nhung duong di THAT la: go vai o → lo bay → cua **NO vi
         thieu ly do** → man chi vao o nay → nguoi go ly do vao → **⛔ va roi
         ⛔ khong co gi xay ra nua**. May cham hen gio ⛔ khong duoc dat lai,
         nen may o kia nam vang **vo han**; dong tab di hop la **mat sach**,
         ma trang ⛔ khong co mot loi nhac nao.
         ⇒ Dien ly do xong thi **hen lai ngay** — nhung chi khi con o cho, ⛔
         khong thi moi phim go vao o ly do lai danh thuc mot lo rong. */
      if (ST.cho.size) _hen(); else _tt();
    };
    h2.appendChild(ip);
    p.appendChild(h2);

    const tt = TP.el('div', '');
    tt.id = 'so-tt';
    tt.style.fontSize = '12px';
    p.appendChild(tt);

    if (!cho_ghi()) {
      const n = TP.el('div', 'note warn');
      n.style.margin = '0';
      n.innerHTML = '<b>Cửa đang ở chế độ CHỈ ĐỌC</b> — mọi ô đều không '
        + 'gõ được. Đây không phải hỏng: máy chủ chạy không có cửa ghi, '
        + 'nên không một phép sửa nào chạm được vào sổ thật.';
      p.appendChild(n);
    }

    c.appendChild(p);
    return c;
  }

  function _tt(chu, lop) {
    const o = TP.$('#so-tt');
    if (!o) return;
    if (chu === undefined) {
      const n = ST.cho.size;
      chu = n ? (n + ' ô chờ lưu…') : 'chưa sửa gì';
      lop = n ? 'warn' : '';
      if (n && !ST.ly_do)
        chu = '' + n + ' ô CHƯA lưu — còn thiếu lý do ở ô trên';
    }
    o.className = lop === 'warn' ? 'chip warn'
                : lop === 'crit' ? 'chip crit'
                : lop === 'ok' ? 'chip ok' : 'muted';
    o.textContent = chu;
  }

  /* ── luoi ───────────────────────────────────────────────────────────── */
  function _the_luoi() {
    const c = TP.el('div', 'card');
    // ⭐ Hai chip nay lay tu `hien_vat/FLS-Demo-Dong.html` — ban demo dong ma
    // owner da xem. Chip 🔒 tra loi truoc mot cau ke toan se hoi *"sao toi
    // ⛔ khong go duoc hai cot cuoi"*; chip tu-luu tra loi *"da luu chua"* ma
    // ⛔ khong can mot nut Luu.
    const hd = TP.el('header', '',
      '<h3>Sổ ITL · ' + GO_TREN_LUOI().length + ' ô gõ được</h3>'
      + '<span class="chip lock" title="Ba ô vùng PHÂN BỔ do MÁY suy từ '
      + 'Mapping Master. Người không gõ được (QĐ-ITL-64).">'
      + 'vùng phân bổ = máy suy</span>'
      // ⭐ Chip nay o TREN luoi. Cau chi dan cu nam duoi luoi — tuc sau
      // hang tram dong — nen thuc te ⛔ khong ai doc tới.
      + '<span class="chip info" title="Ngăn kéo ĐỐI SOÁT của một dòng: 36 cột '
      + 'canon · nguồn nói gì vs người gõ gì · vùng phân bổ · nhật ký bút '
      + 'toán + các lần ĐẢO. Lưới KHÔNG bị che — dòng vẫn trong tầm mắt.">'
      + '▸ bấm một dòng → chi tiết trượt ra bên phải</span>'
      + '<span class="spacer"></span>'
      + '<span class="muted" style="font-size:12px">'
      + '<span class="mono">GET /ledger</span></span>');
    c.appendChild(hd);

    const w = TP.el('div', 'gwrap');
    const t = TP.el('table', 'g');
    t.id = 'so-luoi';

    const th = TP.el('thead');
    const tr = TP.el('tr');
    COT().forEach(function (k) {
      const e = TP.el('th', _lop_cot(k, true));
      // ⭐ Tieu de den tu `cot.js`. `title` noi NGUON cua chinh cai ten do —
      // ke toan hoi "cot nay la cot nao trong so" thi ⛔ khong phai di hoi ai.
      e.title = k.nhan + '\nnguồn tên: ' + k.nguon
              + (k.vi_sao ? '\n' + k.vi_sao : '');
      // ⭐⭐ Cot canon PHAI mang CHU CAI truoc ten. Bon cot `AH..AK` deu ten
      //   *"MID I DoubleCheck LE"* va `W/X` trung `AB/AC` ⇒ chi hien TEN thi
      //   bon tieu de giong het nhau va ⛔ khong ai biet cot nao la cot nao.
      e.textContent = (k.canon ? k.canon + ' · ' : '') + k.nhan
                    + (k.go && !quet() ? ' ✎' : '');
      tr.appendChild(e);
    });
    th.appendChild(tr);
    t.appendChild(th);

    const tb = TP.el('tbody');
    ST.dong.forEach(r => tb.appendChild(_hang(r)));
    t.appendChild(tb);
    w.appendChild(t);
    c.appendChild(w);

    // ⭐ Dai giai thich BA MAU — lay tu demo dong. ⛔ Mot o doi mau ma
    // ⛔ khong ai noi mau do nghia gi la mot o gay lo, ⛔ khong phai mot o
    // truyen tin.
    const ch = TP.el('div', 'pad');
    ch.style.borderTop = '1px solid var(--line)';
    ch.innerHTML =
      '<span class="muted" style="font-size:12px">Gõ vào <b>ô viền xanh</b> → ô '
      + 'đổi <b style="color:var(--warn)">vàng (chưa lưu)</b> → sau <b>2,5 '
      + 'giây</b> thành <b style="color:var(--good)">xanh (đã lưu)</b>. '
      + 'Ô <b style="color:var(--warn)">nền vàng chữ nghiêng</b> = <b>chưa ai '
      + 'gán</b>; ô <b>nền xám</b> = <b>chỉ đọc</b>. '
      + '<b>Bấm cột đầu</b> để mở ngăn kéo đối soát.</span>';
    c.appendChild(ch);

    if (ST.con_tro) {
      const f = TP.el('div', 'pad');
      const b = TP.el('button', 'b', 'Xem thêm ' + TRANG + ' dòng');
      b.onclick = async function () {
        b.disabled = true;
        try {
          const kq = await FLS.doc('/ledger',
            { limit: TRANG, cursor: ST.con_tro });
          const them = kq.data.rows || [];
          ST.dong = ST.dong.concat(them);
          them.forEach(x => ST.theo_id.set(x.itl_id, x));
          ST.con_tro = kq.data.next_cursor || null;
          them.forEach(x => tb.appendChild(_hang(x)));
          if (!ST.con_tro) f.textContent = 'hết sổ —';
          else b.disabled = false;
        } catch (e) {
          b.disabled = false;
          HT.mo('không lấy thêm được',
                '<div class="note crit">' + TP.chu(e.cau || e.message)
                + '</div>', [['Đóng', null]]);
        }
      };
      f.appendChild(b);
      c.appendChild(f);
    }
    return c;
  }

  function _lop_cot(k, la_dau) {
    const l = [];
    if (k.khoa === 1) l.push('f1');
    // ⛔ Che do QUET **⛔ khong** dong cung cot thu hai. `khoa=2` la `memo`, ma
    //   o che do quet `memo` nam thu BA ⇒ neo no bang `left:var(--khoa-1)` se
    //   lam no **de len** cot Ngay. Luoi quet chi 9 cot nen phan lon man ⛔
    //   khong phai cuon ngang; dong cung mot cot la du.
    if (k.khoa === 2 && !quet()) l.push('f2');
    if (k.kieu === 'tien' || k.kieu === 'so') l.push('r');
    if (la_dau && k.go && !quet()) l.push('edit-h');
    return l.join(' ');
  }

  function _hang(r) {
    const tr = TP.el('tr');
    tr.dataset.itl = r.itl_id;
    const khoa_ky = r.period_state === 'locked';
    COT().forEach(function (k) {
      const td = TP.el('td', _lop_cot(k, false));
      td.dataset.cot = k.truong;
      td.dataset.itl = r.itl_id;
      const v = r[k.truong];

      // ⭐ O go duoc — nhung CHI khi ca ba dieu deu dung.
      // ⛔ Che do QUET: ⛔ KHONG o nao tren luoi go duoc — sua nam trong panel
      //   (`FLS-Wireframe.html` §`s-f02`, owner chot 03/09).
      const go = k.go && cho_ghi() && !khoa_ky && !quet();
      if (k.go && !quet()) {
        if (go) td.classList.add('edit');
        else {
          td.classList.add('ro');
          // ⛔ Noi VI SAO o nay ⛔ khong go duoc. Mot o mo di ma khong giai
          // thich la mot o nguoi ta bam mai roi tuong may hong.
          td.title = khoa_ky
            ? 'Kỳ đã CHỐT — không ghi được, kể cả với force (`INV-I13`)'
            : 'Cửa đang ở chế độ CHỈ ĐỌC';
          if (khoa_ky) td.classList.add('badge-lock');
        }
      } else {
        td.classList.add('ro');
      }

      // ⭐⭐ Hai o PHAN BO 🔒 — BA ca, va ca thu ba la mot BAY da do duoc.
      if (k.truong === 'alloc_cfa2' || k.truong === 'alloc_method') {
        td.classList.add('ro');
        _o_phan_bo(td, k, r);
        tr.appendChild(td);
        return;
      }
      if (k.go && (v === null || v === undefined || v === '')) {
        // ⛔ ⛔ Khong de TRONG: o trong va o "chua ai gan" trong giong het
        // nhau, ma y nghia khac han (`INV-I16`).
        td.classList.add('unmapped');
        td.textContent = 'chưa gán';
      } else if (k.truong === 'work_status') {
        /* ⭐⭐ **Cot nay dang in TU VUNG CUA MAY ra cho ke toan doc.**
           Gia tri that trong kho la `UNMAPPED` / `ok` — do la ten trang thai
           trong bang, ⛔ khong phai tieng Viet. Cung lop loi voi `DOC_NO` va
           `CURR` da bat hom qua: man hinh **noi lai ten bien** khi no dang
           co mot cau tieng Viet de noi.

           ⭐ Va hinh thuc theo ban thiet ke: *da phan loai* la tin **tot**
           (`✓`, xanh); *chua phan loai* la **binh than** (nen nhat), ⛔ khong
           bao dong — vi do la trang thai cua **76,6%** cuon so.             */
        td.textContent = '';
        const xong = String(v || '') === 'ok';
        td.appendChild(TP.el('span', 'chip ' + (xong ? 'ok' : 'lock'),
          xong ? '✓ đã phân loại' : 'chưa phân loại'));
      } else {
        td.textContent = _hien(k, v, r.curr);
      }
      if (k.kieu === 'tien' && Number(v) < 0) td.classList.add('neg');
      if (k.khoa === 2) {
        td.title = String(v === null || v === undefined ? '' : v);
        td.style.maxWidth = 'var(--khoa-2)';
        td.style.overflow = 'hidden';
        td.style.textOverflow = 'ellipsis';
      }
      tr.appendChild(td);
    });
    // ⭐ Bam cot khoa thu nhat ⇒ mo drawer. ⛔ Khong bam ca dong: mot cu bam
    // vao o go duoc phai la mot cu chon o, ⛔ khong phai mo mot ngan keo che
    // mat cai luoi.
    //
    // ⛔⛔ **Va no phai TRONG NHU bam duoc — day la mot khuyet tat da do
    //    duoc, ⛔ khong phai mot y thich.** Ban dau o nay chi co
    //    `cursor:pointer`: mot dau hieu **chi hien ra khi chuot da o dung
    //    tren o**, nen no ⛔ khong tra loi duoc cau *"o day co gi bam duoc
    //    khong"*. Chu giai CO noi, nhung no la mot dong 12px **nam DUOI** mot
    //    cai luoi dai ⇒ owner mo man ngay 03/09 va hoi *"sao ⛔ khong co
    //    panel cho tung giao dich"* — trong khi panel **van o do va van
    //    chay**. ⭐ Mot tinh nang ⛔ khong ai tim thay thi bang **⛔ khong
    //    co**, va do la mot cau hoi cua **hinh dang**, ⛔ khong phai cua ma.
    // ⇒ Ba dau hieu, va cả ba **thay duoc khi CHUA bam gi**: chu `⊞` trong o ·
    //   lop `mo-duoc` *(gach chan + mau accent)* · `title` noi ngan keo co gi.
    //   ⚠ Chu `⊞` la **chu**, nen bo test doc duoc no; neu chi de CSS lo thi
    //   dau hieu ay **bien mat trong im lang** ma ⛔ khong cong nao thay.
    const o1 = tr.cells[0];
    o1.classList.add('mo-duoc');
    o1.title = 'Bấm dòng này để mở chi tiết ĐỐI SOÁT bên phải — 36 cột canon '
             + 'nguồn nói gì vs người gõ gì · vùng phân bổ · nhật ký bút '
             + 'toán. Lưới KHÔNG bị che.';
    o1.textContent = '▸ ' + o1.textContent;
    // ⚠ ⛔ Khong con `stopPropagation`: bam vao cot dau **cung la** bam vao
    //   dong, va ca hai deu dan tới cung mot cho. Duong bam thuc su nam o
    //   `_noi_ban_phim` — mot cho, cho MOI o, dung nhu wireframe *(dong nao
    //   cung bam duoc, ⛔ khong phai rieng mot o)*.
    o1.onclick = () => mo_drawer(r.itl_id);
    return tr;
  }

  /* ⛔⛔ **Ba ca, va man ⛔ khong duoc chua ca nao cho dep.**

       ⓐ co gia tri  ⇒ hien
       ⓑ `#N/A`      ⇒ hien **đúng `#N/A`**. No la mot CAU TRA LOI — *"dong nay
                       ⛔ khong tra duoc `hd` trong danh mục"* — ⛔ khong phai
                       mot loi, va ⛔ khong phai rong. Doi no thanh `—` la nuot
                       mat dung cai thong tin ke toan can (`INV-I16`).
       ⓒ **`0`**     ⇒ hien **đúng chữ `0`**, kem cau giai thich. Day la **bay
                       `VLOOKUP`**: o `Mapping Master!L` rong THAT thi Sheets
                       tra ve `0`, va `0 <> ""` la DUNG ⇒ so that dang hien `0`.
                       ⛔ Chua cho dep o day la lam man hinh noi khac so.       */
  function _o_phan_bo(td, k, r) {
    const na = !!r.alloc_na;
    const v = r[k.truong];
    if (na) {
      /* ⭐⭐ Lop `na` — ⛔ **KHONG dung lai `unmapped`**. Truoc hom nay hai
         thu nay dung chung mot lop nen chung trong **y het nhau**, trong khi
         chung khac han: `chưa gán` la *"⛔ chua ai gan"* *(viec cho NGUOI)*,
         con `#N/A` la *"may da tra va ⛔ khong ra"* *(cau tra loi cua MAY)*.
         ⇒ Rang buoc #3 cua ban thiet ke: hai thu ay phai ve **khac nhau**. */
      td.classList.add('na');
      td.textContent = '';
      td.appendChild(TP.el('span', '', '#N/A'));
      td.title = 'không tra được mã hợp đồng này trong Mapping Master. '
               + 'Đây là một CÂU TRẢ LỜI, không phải một lỗi — và sổ thật '
               + 'cũng đang hiện đúng #N/A ở đây.';
      return;
    }
    if (k.truong === 'alloc_method' && String(v) === '0') {
      td.classList.add('badge-lock');
      td.textContent = '0';
      td.title = 'BẪY VLOOKUP: ô Method của danh mục RỖNG, nên Sheets trả '
               + 'về 0. Sổ thật đang hiện đúng số 0 ở đây — màn không '
               + 'chữa cho đẹp.';
      return;
    }
    td.textContent = (v === null || v === undefined || v === '') ? '—' : v;
    td.title = 'MÁY suy từ Chủ dự toán + Mã hợp đồng + Mapping Master. '
             + 'Người không gõ được ô này (QĐ-ITL-64).';
  }

  /* ⭐ `curr` = tien te CUA CHINH DONG ay *(`WO-022` §5b ⓔ)* — o tien in
     theo so le cua no, ⛔ doan. */
  function _hien(k, v, curr) {
    if (v === null || v === undefined || v === '') return '—';
    if (k.kieu === 'tien') return TP.tien(v, curr);
    if (k.kieu === 'so') return TP.so(v);
    if (k.truong === 'is_flash') return v ? 'nháp' : 'đã đối soát';
    return String(v);
  }

  /* ═══ ⭐⭐ SO TIEN CUA MOT DONG ══════════════════════════
     ⛔⛔ **Loi that** (mot ke toan doc man 04/09, ⛔ da kiem lai bang may tren
     so THAT): phep do cu la *"o nao KHONG RONG"* — ma so `0` thi ⛔ **khong
     rong**. So goc dien **CA HAI** cot, mot cot bang `0` *(`_GUIDE_04`)*, nen:

       · **3.141 dong** `Có` co `ps_no = 0` ⇒ may lay `0` lam so tien va gan
         dau am ⇒ hien **`−0`**: so tien **boc hoi** khoi dau panel;
       · **489 dong** `Nợ` co `ps_co = 0` ⇒ `ps_co` "khong rong" ⇒ hien **sai
         dau** (am).

     **3.630 / 10.030 dong = 36%.** ⚠ Va no ⛔ **khong nhin thay duoc** tren
     man: 5.105 dong con lai co o **trong that** nen hien dung — nhin mot vai
     dong bat ky thi moi thu binh thuong.

     ⭐ Luat: mot ve chi **co tien** khi no ⛔ khong rong VA **khac 0**.
     `Nợ` = vao (duong) · `Có` = ra (am). */
  function _co_tien(v) {
    return v !== null && v !== undefined && v !== '' && Number(v) !== 0;
  }
  function _so_tien(r) {
    if (!r) return { tri: null, am: false, canh: '' };
    const no = _co_tien(r.ps_no), co = _co_tien(r.ps_co);
    /* ⛔⛔ CA HAI ve khac 0: may ⛔ **KHONG chon ho mot ve**. Do la mot dong
       bat thuong that su, va chon ho la dung lai cai loi vua chua — chi khac
       la lan nay chon **im lang**. ⇒ Khai ra, dung `INV-I16`.
       ⚠ Do tren so that hom nay: **0 dong**. Nhung mot nhanh "hom nay khong
       xay ra" van phai co cau tra loi, ⛔ khong duoc de roi xuong nhanh khac. */
    if (no && co) {
      return { tri: null, am: false,
               canh: 'CẢ HAI vế khác 0 — Nợ ' + TP.tien(r.ps_no, r.curr)
                     + ' Có ' + TP.tien(r.ps_co, r.curr)
                     + '. Máy không chọn hộ' };
    }
    if (no) return { tri: r.ps_no, am: false, canh: '' };
    if (co) return { tri: r.ps_co, am: true, canh: '' };
    return { tri: null, am: false, canh: '' };
  }

  /* ═══ tam hanh vi §1 ════════════════════════════════════════════════ */

  /* ⭐⭐ TOA DO CHAY TREN DONG DANG HIEN, ⛔ khong phai dong trong BANG.
     ⛔⛔ **Loi that** (mot ke toan doc man 04/09): `_loc` chi **giau** dong
     (`tr.style.display='none'`), con toa do lai dem theo **thu tu trong bang**.
     Nen khi dang bat mot bo loc — dung cach dung ma chinh man khuyen khich:

       · mui ten xuong nhay vao mot dong **AN** ⇒ con tro bien mat khoi mat;
       · `Ctrl+D` chep tu **dong an ngay tren**, ⛔ khong phai dong dang nhin;
       · **dan mot vung thi gia tri roi vao nhung dong ⛔ khong ai nhin thay**,
         va man van bao *"dan 20 o"* nhu binh thuong.

     ⇒ Do la kieu sai **⛔ khong ai biet cho toi khi bao cao lech**, va so la
     **chi-them** (`INV-I08`) nen chua duoc thi phai **dao**, ⛔ khong xoa.

     ⭐ Chua o **hai ham nay** chu ⛔ khong o tung cho goi: moi phep di / chep /
     dan deu di qua chung, nen chua mot lan la chua het. Chua o cho goi thi
     lan sau them mot phep moi la lop loi quay lai. */
  function _hang_hien() {
    const t = TP.$('#so-luoi');
    if (!t || !t.tBodies[0]) return [];
    return Array.prototype.filter.call(t.tBodies[0].rows,
      tr => tr.style.display !== 'none');
  }
  function _o_tai(r, c) {
    const h = _hang_hien();
    const tr = r >= 0 && r < h.length ? h[r] : null;
    return tr ? tr.cells[c] : null;
  }
  /* ⚠ Tra `-1` khi o dang chon **⛔ khong con hien** (bo loc vua giau no).
     Nguoi goi phai dung lai — di tiep tu mot cho ⛔ khong nhin thay duoc la
     dung lai cai loi vua chua. */
  function _toa_do(td) {
    return [_hang_hien().indexOf(td.parentNode), td.cellIndex];
  }

  function _chon(td) {
    if (!td) return;
    if (ST.o) ST.o.classList.remove('chon');
    ST.o = td;
    td.classList.add('chon');
    td.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }

  function _go_duoc(td) { return td && td.classList.contains('edit'); }

  /* ⭐ Dat mot gia tri vao o. Tra `true` neu co thay doi THAT. */
  function _dat(td, v) {
    if (!_go_duoc(td)) return false;
    const cu = td.classList.contains('unmapped') ? '' : td.textContent;
    if (cu === v) return false;
    td.classList.remove('unmapped', 'da-luu');
    td.textContent = v === '' ? 'chưa gán' : v;
    if (v === '') td.classList.add('unmapped');
    td.classList.add('chua-luu');
    ST.lich.push({ td: td, cu: cu });
    const k = _khoa(td.dataset.itl, td.dataset.cot);
    ST.cho.set(k, { itl_id: Number(td.dataset.itl), field: td.dataset.cot,
                    gia_tri: v, cu: cu, td: td });
    _hen();
    return true;
  }

  function _hen() {
    _tt();
    clearTimeout(ST.hen);
    ST.hen = setTimeout(_bay, CHO_MS);
  }

  function _loc(q) {
    // ⓹ Loc CACH NHIN — an dong, ⛔ khong doi mot ky tu du lieu nao.
    if (q !== undefined) ST.loc = (q || '').trim().toLowerCase();
    const s = ST.loc || '';
    const t = TP.$('#so-luoi');
    if (!t) return;
    let n = 0;
    for (const tr of t.tBodies[0].rows) {
      const d = ST.theo_id.get(Number(tr.dataset.itl)) || {};
      // ⭐ Nut "chi UNMAPPED" cua `FLS-Wireframe.html` §`s-f02`. ⛔ No la mot
      //   phep loc CACH NHIN nua, ⛔ khong phai mot cua rieng: cong hai dieu
      //   kien lai, nen go chu VA bat nut la giao nhau — dung nhu wireframe
      //   (hai dieu khien nam canh nhau trong cung mot `.band`).
      const co = (!s || tr.textContent.toLowerCase().includes(s))
              && (!ST.chi_unmapped || d.work_status === 'UNMAPPED');
      tr.style.display = co ? '' : 'none';
      if (co) n++;
    }
    _tt(s || ST.chi_unmapped
        ? ('hiện ' + n + '/' + ST.dong.length + ' dòng') : undefined);
  }

  let _da_noi = false;
  function _noi_ban_phim() {
    if (_da_noi) return;
    _da_noi = true;

    document.addEventListener('click', function (e) {
      const td = e.target.closest && e.target.closest('#so-luoi td');
      if (!td) return;
      _chon(td);
      // ⭐ Va bam mot O **cung la** bam mot DONG ⇒ chi tiet truot ra ben phai
      //   (`FLS-Wireframe.html` §`s-f02`). Hai viec nay ⛔ khong danh nhau nua:
      //   panel nam **canh** luoi, nen chon o va mo chi tiet cung luc la mot
      //   hanh vi, ⛔ khong phai hai.
      // ⚠ ⛔ KHONG noi vao ban phim: mui len/xuong di qua 200 dong se thanh
      //   200 luot goi cua. Bam la mot y dinh, mui la mot cu quet.
      const tr = td.parentNode;
      if (tr && tr.dataset && tr.dataset.itl) mo_drawer(Number(tr.dataset.itl));
    });

    // ⭐⭐ **Bam DUP de mo o.** Demo dong (`FLS-Demo-Dong.html`) dat mot
    // `<input>` san trong MOI o go duoc, nen nguoi dung chuot bam mot cai la
    // go duoc ngay. Ban dau toi chi mo o khi nguoi **go mot ky tu** — kip
    // Sheets, nhung no bo roi nguoi dung CHUOT: bam vao o roi ⛔ khong thay gi
    // xay ra, va man trong nhu **chi-doc**.
    //
    // ⚠ Van ⛔ khong dat `<input>` san o moi o: luoi 200 dong × 5 o go duoc =
    // **1.000 o nhap** cung luc, va do la thu de lam cham dung cai man ma ke
    // toan quet hang tram dong. ⇒ Mo theo yeu cau — ca ban phim LAN chuot.
    document.addEventListener('dblclick', function (e) {
      const td = e.target.closest && e.target.closest('#so-luoi td');
      if (td && _go_duoc(td)) { _chon(td); _mo_o(td); }
    });

    document.addEventListener('keydown', function (e) {
      // ⛔⛔ `WO-023` `(a)` *(`BA-06` v4.11 `ⓕ1`)*: hop `HT` dang mo ⇒ phim
      //    ⛔ thuoc ve luoi sau lung. Ban truoc: `Ctrl+Z` hoan tac mot o luoi
      //    trong khi nguoi dang doc hop *"Ô này đã vào sổ rồi"* — chinh hop ma
      //    `Ctrl+Z` vua mo. Xem luat ⓓ dau `hop_thoai.js`.
      if (typeof HT !== 'undefined' && HT.nuot_phim && HT.nuot_phim(e)) return;
      const td = ST.o;
      if (!td || !document.body.contains(td)) return;
      if (!TP.$('#man-f02').classList.contains('on')) return;
      const [r, c] = _toa_do(td);
      // ⛔ O dang chon vua bi bo loc giau ⇒ **dung lai**. Moi phim tu day se
      //    roi vao mot dong ⛔ khong ai nhin thay.
      if (r < 0 && e.key !== 'Escape') { _tt('ô đang chọn không còn hiện '
        + 'bấm vào một ô đang thấy', 'warn'); e.preventDefault(); return; }

      /* ⓸ Hoan tac */
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
        const b = ST.lich.pop();
        if (b) {
          // ⛔ Hoan tac chi keo lai o TREN MAN. Neu o do da BAY vao so roi thi
          // ⛔ khong con la hoan tac — no la mot but toan moi, va man noi thang.
          const k = _khoa(b.td.dataset.itl, b.td.dataset.cot);
          if (ST.cho.has(k)) {
            b.td.textContent = b.cu === '' ? 'chưa gán' : b.cu;
            b.td.classList.toggle('unmapped', b.cu === '');
            ST.cho.delete(k);
            b.td.classList.remove('chua-luu');
            _hen();
          } else {
            HT.mo('Ô này đã vào sổ rồi',
              '<div class="note warn">Ô <b>' + TP.chu(b.td.dataset.cot)
              + '</b> của dòng <b>' + TP.chu(b.td.dataset.itl)
              + '</b> đã được ghi vào sổ. Sổ là <b>chỉ thêm</b> '
              + '(<span class="mono">INV-I08</span>) nên <b>không có phép '
              + 'hoàn tác</b> — muốn đổi thì <b>đảo bút toán</b> trong ngăn '
              + 'kéo của dòng, và lần đảo ấy cũng là một dòng trong sổ.</div>',
              [['Mở ngăn kéo dòng này', () => {
                mo_drawer(Number(b.td.dataset.itl)); return true; }],
               ['Đóng', null]]);
          }
          _chon(b.td);
        }
        e.preventDefault();
        return;
      }
      /* ⓷ Keo xuong — lay gia tri o NGAY TREN */
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'd') {
        const tren = _o_tai(r - 1, c);
        if (tren) _dat(td, tren.classList.contains('unmapped')
                            ? '' : tren.textContent);
        e.preventDefault();
        return;
      }
      if (e.ctrlKey || e.metaKey || e.altKey) return;

      /* ⓵ Dieu huong ban phim */
      const di = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1],
                   ArrowRight: [0, 1], Enter: [1, 0], Tab: [0, 1] }[e.key];
      if (di) {
        const b = (e.key === 'Tab' && e.shiftKey) ? [0, -1] : di;
        _chon(_o_tai(r + b[0], c + b[1]) || td);
        e.preventDefault();
        return;
      }
      /* Go de sua ngay — ⛔ khong can bam dup (kip Sheets) */
      if (e.key.length === 1 && _go_duoc(td)) {
        _mo_o(td, e.key);
        e.preventDefault();
        return;
      }
      if (e.key === 'Backspace' && _go_duoc(td)) {
        _dat(td, '');
        e.preventDefault();
      }
    });

    /* ⓶ Dan MOT VUNG — tach theo tab/xuong dong roi rai tu o dang chon */
    document.addEventListener('paste', function (e) {
      const td = ST.o;
      if (!td || !TP.$('#man-f02').classList.contains('on')) return;
      if (!document.body.contains(td)) return;
      const txt = (e.clipboardData || window.clipboardData).getData('text');
      const bang = txt.replace(/\r/g, '').split('\n').filter(x => x !== '')
                      .map(x => x.split('\t'));
      const [r0, c0] = _toa_do(td);
      if (r0 < 0) {
        _tt('ô đang chọn không còn hiện — chưa dán gì', 'warn');
        e.preventDefault();
        return;
      }
      let n = 0, bo = 0, tran = 0;
      bang.forEach((hang, i) => hang.forEach((v, j) => {
        const x = _o_tai(r0 + i, c0 + j);
        // ⛔⛔ `tran` = o roi RA NGOAI vung dang hien. Truoc day chung bi bo
        //    **im lang**: dan 20 gia tri vao 6 dong con lai thi 14 gia tri
        //    bien mat ma man van bao *"dan 20 o"*. ⇒ Phai dem va phai noi.
        if (!x) { tran++; return; }
        if (_dat(x, v)) n++;
        else if (!_go_duoc(x)) bo++;
      }));
      // ⛔ Noi ca so o BI BO. Dan 20 o ma chi 6 o vao duoc, im lang, la cach
      // chac chan nhat de mot bang gia tri bi lech mot cot ma ⛔ khong ai biet.
      _tt('dán ' + n + ' ô'
          + (bo ? '  ' + bo + ' ô không gõ được, đã bỏ' : '')
          + (tran ? '  ' + tran + ' ô TRÀN khỏi vùng đang hiện, đã bỏ' : ''),
          (bo || tran) ? 'warn' : '');
      e.preventDefault();
    });
  }

  /* O nhap that — de go duoc nhieu ky tu, dan, sua. */
  function _mo_o(td, ky_tu) {
    const cu = td.classList.contains('unmapped') ? '' : td.textContent;
    const ip = TP.el('input');
    ip.value = ky_tu === undefined ? cu : ky_tu;
    td.textContent = '';
    td.appendChild(ip);
    ip.focus();
    ip.setSelectionRange(ip.value.length, ip.value.length);
    let xong = false;
    const dong = function (nhan) {
      if (xong) return;
      xong = true;
      const v = ip.value.trim();
      td.textContent = cu === '' ? 'chưa gán' : cu;
      td.classList.toggle('unmapped', cu === '');
      if (nhan) _dat(td, v);
      _chon(td);
    };
    ip.onblur = () => dong(true);
    ip.onkeydown = function (e) {
      e.stopPropagation();
      if (e.key === 'Enter' || e.key === 'Tab') {
        dong(true);
        const [r, c] = _toa_do(td);
        _chon(_o_tai(e.key === 'Enter' ? r + 1 : r,
                     e.key === 'Enter' ? c : c + 1) || td);
        e.preventDefault();
      } else if (e.key === 'Escape') {
        dong(false);
        e.preventDefault();
      }
    };
  }

  /* ═══ ⓼ LUU THEO LO — `GAP-SCR-07` ══════════════════════════════════
     ⛔⛔ **Ba ca loi spec doi, va cach xu tung ca. ⛔ Khong ca nao duoc im.**

     ⓐ **Go tiep khi lo dang bay.** Lo duoc **rut ra** khoi `ST.cho` truoc khi
       bay, nen mot o go them trong luc ay vao **lo sau**. Va neu lo dang bay
       that bai, o hong chi quay lai hang cho khi nguoi **chua** go de len no
       — phim moi nhat cua nguoi luon thang.

     ⓑ **Mang dut giua chung.** Lo di **tuan tu**, va **dung ngay** o o hong.
       Nhung o con lai **giu nguyen mau CHUA LUU** va quay lai hang cho. Man
       noi **dung nhung o nao chua vao so** — ⛔ khong mot cai bang "loi mang"
       chung chung, vi ke toan can biet **go lai o nao**.

     ⓒ **Hai nguoi sua mot o.** ⛔⛔ Cua ghi **KHONG** phat hien duoc viec nay:
       `ghi_but_toan` chi so gia tri go voi **nguon** va **goi y cua may**,
       ⛔ khong so voi **but toan cua nguoi khac** — nen nguoi sau **ghi de
       nguoi truoc trong im lang**. Da do, mo `GAP-SCR-09`.
       ⇒ Man lam duoc dieu no lam duoc: **hoi lai cua NGAY TRUOC khi ghi**
       (`GET .../fields/{field}`) va so voi anh chup luc tai dong. Lech thi
       **dung lai va noi ten nguoi kia**. ⚠ Day la mot phep **KIEM**, ⛔ khong
       phai mot bao dam: van con mot khe hep giua phep hoi va phep ghi. Khep
       han khe do la viec cua **cua**, ⛔ khong phai cua man hinh.        */

  async function _bay() {
    if (ST.dang_bay || ST.cho.size === 0) return;
    if (!cho_ghi()) { _tt('cửa chỉ đọc — không lưu', 'crit'); return; }
    if (!ST.ly_do) {
      // ⛔ Dung lai, ⛔ khong bia mot ly do. Va chi ro cho phai dien.
      _tt();
      const ip = TP.$('#so-ly-do');
      if (ip) { ip.focus(); ip.style.borderColor = 'var(--warn)'; }
      return;
    }
    ST.dang_bay = true;
    const lo = [...ST.cho.values()];   // ⓐ RUT ra: o go them di vao lo sau
    ST.cho.clear();
    _tt('đang lưu ' + lo.length + ' ô…', 'warn');

    const hong = [];
    let xong = 0;
    for (const o of lo) {
      try {
        await _ghi_mot_o(o);
        o.td.classList.remove('chua-luu');
        o.td.classList.add('da-luu');
        xong++;
      } catch (e) {
        hong.push({ o: o, e: e });
        break;                          // ⓑ DUNG ngay, ⛔ khong ban tiep
      }
    }
    // O chua kip bay + o hong ⇒ quay lai hang cho, TRU khi nguoi da go de len.
    const con = lo.slice(xong);
    con.forEach(function (o) {
      const k = _khoa(o.itl_id, o.field);
      if (!ST.cho.has(k)) ST.cho.set(k, o);   // ⓐ phim moi nhat thang
      o.td.classList.add('chua-luu');
    });
    ST.dang_bay = false;

    if (hong.length) {
      ST.hong = con;
      const e = hong[0].e;
      // ⭐ Hai cau chuyen khac nhau ⇒ hai hop khac nhau.
      if (e.nguoi_khac !== undefined) _bao_nguoi_khac(hong[0].o, e, con);
      else _bao_hong(e, con);
      _tt('' + con.length + ' ô CHƯA vào sổ', 'crit');
    } else {
      _tt('đã lưu ' + xong + ' ô (một lô)', 'ok');
      setTimeout(() => {
        [...document.querySelectorAll('td.da-luu')]
          .forEach(x => x.classList.remove('da-luu'));
      }, 4000);
    }
    // ⭐ Sau MOI lo luu — ke ca lo hong nua phan — ban nho cua panel da cu.
    //   Panel dang mo phai doc lai, khong thi no noi so cu ngay canh cai o
    //   vua doi mau xanh.
    if (_dang_xem !== null) _lam_moi(_dang_xem);
  }

  async function _ghi_mot_o(o) {
    // ⓒ Hoi lai cua NGAY TRUOC khi ghi.
    const truoc = (await FLS.doc(
      '/ledger/' + o.itl_id + '/fields/' + o.field)).data;
    const dong = ST.theo_id.get(o.itl_id) || {};
    // Anh chup luc TAI dong: luc do o nay co but toan tay nao chua?
    // `GET /ledger` ⛔ khong mang `adj_id`, nen moc so sanh la gia tri.
    // ⭐ Doc thang `tay` — gia tri NGUOI KHAC da go — chu ⛔ khong suy tu
    // chuoi `value_source`: mot phep so chuoi la mot phep so se hong lang le
    // neu tang duoi doi ten trang thai.
    const tay = truoc.tay;
    const lech = tay !== null && tay !== undefined
               && String(tay) !== String(dong[o.field] || '')
               && String(tay) !== String(o.cu);
    if (lech) {
      // ⛔⛔ **⛔ Khong dung lai ma loi `FLS-CONFLICT-SOURCE` cho ca nay.**
      // Bo test bat duoc: dung chung ma thi man hien cau cua cai ma do —
      // *"gia tri ban go khac voi gia tri NGUON dang co"* — trong khi that ra
      // no khac voi **but toan cua mot NGUOI KHAC**. Cung mot chu "khac", hai
      // cau chuyen khac han: mot ben la *"so goc noi khac"*, mot ben la
      // *"Thuong vua go o nay 10 phut truoc"*. Ke toan xu hai ca ay khac nhau,
      // nen man ⛔ khong duoc ke nham chuyen.
      const e = new FLS.LoiCua(
        'FLS-CONFLICT-SOURCE', 409,
        'ô này đã có người khác gõ sau lúc bạn mở màn', null, '');
      e.nguoi_khac = tay;
      throw e;
    }
    try {
      await FLS.ghi('/ledger/' + o.itl_id + '/adjust',
        { field: o.field, value: o.gia_tri, reason: ST.ly_do });
    } catch (e) {
      if (e.ma !== 'FLS-CONFLICT-SOURCE') throw e;
      // `US-025` — he KEU khi go khac nguon. Hoi NGUOI, ⛔ khong tu `force`.
      const dong_y = await _hoi_ghi_de(o, e);
      if (!dong_y) throw e;
      await FLS.ghi('/ledger/' + o.itl_id + '/adjust',
        { field: o.field, value: o.gia_tri, reason: dong_y, force: true });
    }
  }

  function _hoi_ghi_de(o, e) {
    return new Promise(function (xong) {
      const khac = e.khac || {};
      const dong = Object.entries(khac).map(([k, v]) =>
        '<tr><td class="ro">' + TP.chu(k === 'nguon' ? 'sổ gốc nói'
                                     : 'máy gợi ý') + '</td><td><b>'
        + TP.chu(v) + '</b></td></tr>').join('');
      HT.mo('Giá trị bạn gõ KHÁC cái đang có',
        '<div class="note warn">Dòng <b>' + o.itl_id + '</b> · ô <b>'
        + TP.chu(o.field) + '</b></div>'
        + '<table style="margin:10px 0"><tbody>' + dong
        + '<tr><td class="ro">bạn gõ</td><td><b>' + TP.chu(o.gia_tri)
        + '</b></td></tr></tbody></table>'
        + '<div class="note">Ghi đè không xoá gì cả — sổ <b>chỉ thêm</b>, '
        + 'giá trị cũ vẫn đọc lại được trong nhật ký. Nhưng <b>phải nói vì '
        + 'sao</b> bạn tin số của mình hơn (<span class="mono">US-025</span>).'
        + '</div>'
        + '<div style="margin-top:8px"><input class="inp" id="so-de" '
        + 'style="width:100%" placeholder="vì sao ghi đè…"></div>',
        [['Ghi đè', function () {
            const v = (TP.$('#so-de').value || '').trim();
            if (!v) { TP.$('#so-de').style.borderColor = 'var(--warn)';
                      return false; }
            xong(v);
          }, { pri: true, danger: true }],
         ['Để nguyên, không ghi', function () { xong(null); }]]);
    });
  }

  /* ⓒ Hop RIENG cho ca "hai nguoi sua mot o". ⛔ Khong gop vao `_bao_hong`:
     o day ⛔ khong co gi hong ca — chi la **hai nguoi cung lam mot viec**, va
     cau tra loi la mot cuoc noi chuyen, ⛔ khong phai mot lan bam "Thử lại". */
  function _bao_nguoi_khac(o, e, con) {
    HT.mo('Ô này đã có NGƯỜI KHÁC gõ',
      '<div class="note warn">Dòng <b>' + o.itl_id + '</b> · ô <b>'
      + TP.chu(o.field) + '</b></div>'
      + '<table style="margin:10px 0"><tbody>'
      + '<tr><td class="ro">trên sổ bây giờ</td><td><b>'
      + TP.chu(e.nguoi_khac) + '</b></td></tr>'
      + '<tr><td class="ro">bạn định gõ</td><td><b>' + TP.chu(o.gia_tri)
      + '</b></td></tr></tbody></table>'
      + '<div class="note">Máy <b>chưa ghi gì cả</b> — cả lô dừng ở đây, và '
      + '<b>' + con.length + ' ô</b> vẫn <b>viền vàng</b> trên lưới. Máy '
      + 'không tự chọn giúp: đây là <b>hai người cùng làm một việc</b>, và '
      + 'cách ra là <b>hỏi nhau</b>, không phải bấm lại.</div>'
      + '<div class="note warn">Phép kiểm này là một phép <b>kiểm</b>, '
      + 'không phải một <b>bảo đảm</b>: cửa ghi <b>không</b> phát hiện được '
      + 'việc hai người sửa một ô (<span class="mono">GAP-SCR-09</span>), nên '
      + 'vẫn còn một khe hẹp giữa lúc màn hỏi và lúc màn ghi.</div>',
      [['Lấy giá trị của họ', function () {
          o.td.classList.remove('chua-luu', 'unmapped');
          o.td.textContent = e.nguoi_khac;
          ST.cho.delete(_khoa(o.itl_id, o.field));
          const r = ST.theo_id.get(o.itl_id);
          if (r) r[o.field] = e.nguoi_khac;
          _tt();
        }, { pri: true }],
       ['Giữ số của tôi, để tôi hỏi lại họ', null]]);
  }

  function _bao_hong(e, con) {
    const ds = con.map(o => '<li>dòng <b>' + o.itl_id + '</b> · ô <b>'
      + TP.chu(o.field) + '</b> → "' + TP.chu(o.gia_tri) + '"</li>').join('');
    HT.mo('Lô lưu DỪNG giữa chừng',
      '<div class="note crit"><b>' + TP.chu(e.cau || e.message) + '</b>'
      + (e.lam_gi ? '<br>' + TP.chu(e.lam_gi) : '') + '</div>'
      + '<div style="margin-top:10px"><b>' + con.length
      + ' ô dưới đây CHƯA vào sổ</b> — chúng vẫn <b>viền vàng</b> trên '
      + 'lưới:</div><ul style="margin:6px 0 0 18px">' + ds + '</ul>'
      + '<div class="note" style="margin-top:10px">Chúng không mất: bấm '
      + '<b>Thử lại</b>, hay gõ tiếp rồi để máy tự lưu sau 2,5 giây.</div>',
      [['Thử lại ngay', function () { _bay(); }, { pri: true }],
       ['Đóng', null]]);
  }

  /* ═══ DRAWER doi soat ═══════════════════════════════════════════════ */

  /* ── ⭐ Panel BEN PHAI, ⛔ khong phai hop che man ────────────────────────
     `FLS-Wireframe.html` §`s-f02`: `.f02-wrap.split` = `minmax(0,1fr) 430px`,
     panel `sticky` va chia lam hai vung — `.dfixed` **⛔ khong cuon** (so tien
     + dien giai, de doc luc nao cung thay dang xem dong nao) va `.dscroll`
     (bay nhom). ⭐ Vung `.dfixed` ve **NGAY**, tu dong da co san tren luoi ⇒
     panel ⛔ khong bao gio la mot khung trong trong luc doi cua tra loi.       */

  let _dang_xem = null;             // itl_id dang mo — ⛔ khong mo lai chinh no
  const _nho = new Map();           // itl_id -> [d, nk]

  function _cac_hang() {
    const t = TP.$('#so-luoi');
    const ra = [];
    if (!t || !t.tBodies || !t.tBodies[0]) return ra;
    const rs = t.tBodies[0].rows;
    for (let i = 0; i < rs.length; i++) ra.push(rs[i]);
    return ra;
  }

  function _danh_dau(itl_id) {
    _cac_hang().forEach(function (tr) {
      const la = String(tr.dataset.itl) === String(itl_id);
      if (la) tr.classList.add('chon');
      else tr.classList.remove('chon');
    });
  }

  function dong_drawer() {
    _dang_xem = null;
    const bo = TP.$('#so-wrap');
    const ben = TP.$('#so-ben');
    if (bo) bo.classList.remove('split');
    if (ben) ben.textContent = '';
    _danh_dau(null);
  }

  function _vo_panel(itl_id, r) {
    const p = TP.el('div', 'drawerp');
    p.id = 'so-panel';
    // ⚠⚠ Dung `createElement` cho **tung manh** cua thanh tieu de, ⛔ KHONG
    //   dat mot chuoi `innerHTML` roi `appendChild` cai nut vao sau. Tron hai
    //   cach lai thi **mat chu**: `innerHTML` xoa het con, va khi da co con
    //   thi `textContent` chi con doc con ⇒ chu *"Đối soát · dòng 101"* bien
    //   mat. Bo test bat duoc, va no bat dung — mot bang chung nua rang phai
    //   **ve that** roi moi doc, ⛔ khong doc ma bang mat.
    const hd = TP.el('header');
    const h = TP.el('h3', '', 'Đối soát · dòng ' + itl_id);
    h.style.margin = '0';
    h.style.fontSize = '13px';
    hd.appendChild(h);
    if (r && r.is_flash) {
      const f = TP.el('span', 'chip flash', 'flash');
      f.title = 'Số NHÁP — chưa đối soát xong';
      hd.appendChild(f);
    }
    hd.appendChild(TP.el('span', 'spacer'));
    const x = TP.el('button', 'b tiny', 'Đóng');
    x.onclick = dong_drawer;
    hd.appendChild(x);
    p.appendChild(hd);

    // ⭐ Vung ⛔ KHONG CUON — wireframe goi la `.dfixed`. No tra loi cau
    //   *"toi dang doi soat dong nao"* ke ca khi da cuon xuong cuoi nhat ky.
    const co = TP.el('div', 'dfixed');
    const t = _so_tien(r);
    const st = TP.el('div', 'dstrip');
    st.id = 'so-dai-tien';
    /* ⭐⭐ CA HAI ve khac 0 ⇒ hien **ca hai so**, ⛔ khong chon ho mot ve.
       ⛔ Truoc day cho nay hien `—` cong mot chip canh bao dai — tuc la con
       so **bien mat** dung luc no dang bat thuong nhat. Hien ca hai la cach
       duy nhat trung thuc: may ⛔ khong biet ve nao, va no noi ra bang cach
       **cho xem ca hai**, ⛔ khong bang mot dau gach. */
    if (t.canh) {
      st.appendChild(TP.el('span', 'amt doi',
        'Nợ ' + TP.tien(r.ps_no, r.curr) + ' Có ' + TP.tien(r.ps_co, r.curr)));
    } else {
      st.appendChild(TP.el('span', 'amt' + (t.am ? ' neg' : ''),
        t.tri === null ? '0' : (t.am ? '−' : '+') + TP.tien(t.tri, r.curr)));
    }
    st.appendChild(TP.el('span', 'muted', TP.chu(r ? (r.curr || '') : '')));
    /* ⭐ Chip HUONG tien — chu, ⛔ khong chi dau `+`/`−`. Rang buoc #9 cua ban
       thiet ke: mau *(va dau)* ⛔ khong bao gio la thu DUY NHAT cho mot nghia.
       ⚠ Bon ca, va ca thu tu *(⛔ khong ve nao co tien)* la ca **that**: so
       goc dien ca hai cot va mot cot bang `0`. */
    st.appendChild(TP.el('span', 'chip',
      t.canh ? 'cả hai vế có tiền'
             : (t.tri === null ? 'không vế nào có tiền'
                               : (t.am ? 'tiền ra' : 'tiền vào'))));
    st.appendChild(TP.el('span', 'spacer'));
    const ng = TP.el('span', 'mono muted', TP.chu(r ? (r.doc_date || '') : ''));
    ng.style.fontSize = '12px';
    st.appendChild(ng);
    co.appendChild(st);

    /* ⭐⭐ NHAN lay TU BAN KHAI, ⛔ khong go tay — rang buoc #12 cua ban thiet
       ke, va no la rang buoc **da bat mot loi that** hom qua *(panel in ra
       `DOC_NO` · `CURR` · `LE_PAYER`)*.

       ⛔⛔ Va toi vua **tai pham chinh no**: ban dau nam o duoi day go tay
       `'Tài khoản'` · `'LE'` · `'Pháp nhân thanh toán'`. Bo test bat duoc, va
       no bat **dung**: go tay thi mai kia so doi ten cot, digest van hien ten
       cu va ⛔ khong phep thu nao do.

       ⚠ Panel doc `COT_DU()` *(bang **DAY DU**)*, ⛔ khong phai `COT()` — che
       do quyet dinh **luoi bay bao nhieu cot**, no ⛔ khong duoc quyet dinh
       **mot o ten la gi**. */
    const _nhan = function (f) {
      const k = COT_DU().find(x => x.truong === f);
      return k ? k.nhan : f;
    };

    /* ⭐ `doc_no` xuong dong RIENG: do that, no dai toi **40** ky tu va co ca
       ma nhu `FT26230301024824` — nhet chung dong voi ngay thi mot trong hai
       bi day xuong hay bi cat. */
    const sct = TP.el('div', 'dref');
    const o_sct = TP.el('div', 'o dai');
    o_sct.appendChild(TP.el('span', 'k', TP.chu(_nhan('doc_no'))));
    o_sct.appendChild(TP.el('span', 'v', TP.chu(r ? (r.doc_no || '—') : '—')));
    sct.appendChild(o_sct);
    co.appendChild(sct);

    /* ⭐ Kieu chu cua `Diễn giải` den TU BAN KHAI (`van`), ⛔ khong go tay o
       CSS: hai cho khai cung mot su that thi mot ngay chung se lech. */
    const k_memo = COT_DU().find(x => x.truong === 'memo');
    co.appendChild(TP.el('div', 'dmemo' + (k_memo && k_memo.van ? ' van' : ''),
      TP.chu(r ? (r.memo || '') : '')));

    /* ═══ ⭐⭐ BA O THAM CHIEU — khoi `①` cu, ⛔ hoa tan vao day ═══════════
       ⛔⛔ Truoc do chung la mot **khoi rieng** nam **TREN** khoi 7 o go duoc.
       Nhung ke toan mo panel ra la de **go**; chung tu chi de **tra**. ⇒ Dua
       chung vao vung ⛔ KHONG CUON: cuon xuong o thu bay **van con thay** tai
       khoan va phap nhan de doi chieu. Ke toan xin dung dieu nay.

       ⚠ Ba o nay deu la cot cua **luoi** nen chung co san trong `r` — panel
       ⛔ khong phai cho cua don le. Do la ly do chung ve duoc **ngay**, truoc
       khi `GET /ledger/{id}` tra ve.                                        */
    const ref = TP.el('div', 'dref');
    ref.id = 'so-digest';
    [['acct', true], ['le', false], ['le_payer', false]
    ].forEach(function (x) {
      const f = x[0];
      const o = TP.el('div', 'o' + (x[1] ? ' dai' : ''));
      o.appendChild(TP.el('span', 'k', TP.chu(_nhan(f))));
      const g = r ? r[f] : '';
      const v = g === null || g === undefined || g === '' ? '' : String(g);
      /* ⭐ Kieu chu theo **BAN KHAI** (`van`), ⛔ khong theo do dai gia tri —
         mot luat chu cho ca panel. Ba o nay deu la **ma** nen chung deu chu
         may; nhung phep chon PHAI di qua ban khai, ⛔ khong duoc doan o day. */
      const k = COT_DU().find(y => y.truong === f);
      const lop = (k && k.van ? 'v van' : 'v') + (v === '' ? ' rong' : '');
      o.appendChild(TP.el('span', lop, v === '' ? 'chưa gán' : TP.chu(v)));
      ref.appendChild(o);
    });
    co.appendChild(ref);

    /* ⭐ `US-032` — phan bi phep THU HEP cat ra ⛔ khong bi **giau**.
       ⛔⛔ 1.225 / 1.304 cap lech la hai cot **⛔ khong cung tu vung**, nen
       chung ⛔ khong bat bang bao. Nhung *"⛔ khong bat bang bao"* ⛔ khong
       duoc bien thanh *"⛔ khong noi gi"* — do dung la cai `INV-I16` cam.
       ⇒ Chung xuong mot dong ghi chu ngay duoi o, nho va binh than. */
    if (r && String(r.le || '').trim() && String(r.le_payer || '').trim()
        && String(r.le).trim() !== String(r.le_payer).trim()) {
      const g = TP.el('div', 'src');
      g.id = 'so-le-khac';
      g.style.padding = '0 13px 9px';
      g.textContent = 'Hai ô trên khác nhau. Máy chỉ báo KIỂM TRA khi cả hai '
        + 'đều là mã pháp nhân; ngoài ra thì đây là ghi chú để đối chiếu.';
      co.appendChild(g);
    }
    p.appendChild(co);
    // ⭐ Cho san cho DAI PHAN QUYET — no can `d` *(cua don le)* nen chi dien
    //   duoc sau khi cua tra loi. Cho phai co SAN de dai khong nhay chen giua
    //   khi no den.
    const pq = TP.el('div', 'pq cho');
    pq.id = 'so-phan-quyet';
    pq.innerHTML = '<span class="muted" style="font-size:11.5px">'
                 + 'đang đếm việc của dòng này…</span>';
    p.appendChild(pq);
    return p;
  }

  /* ═══ ⭐⭐ HUONG 1 · DAI PHAN QUYET ═══════════════════════════════════
     ⛔⛔ **Van de no giai.** Hom nay ke toan phai **cuon het panel** — 57 dong
     nhan–gia tri cong bon bang, khoang **2,3 man hinh** — moi biet dong dang mo
     **co viec gi chua xong**. ⇒ Cau hoi dau tien cua moi dong *("dong nay co
     can toi khong")* la cau **dat nhat** de tra loi.

     ⭐ Dai nay ⛔ khong phai trang tri: **moi chip la mot phep DEM**, va bam vao
     no thi nhay thang xuong dung nhom. ⛔ Mot chip ⛔ khong dem duoc thi
     ⛔ khong duoc ve — mot con so bia ra o cho de nhat nhin la cho te nhat.  */
  function _dem_viec(d, nk) {
    const go = ['hd', 'pay_type', 'cdt1', 'svc_start', 'svc_end']
      .concat(window.FLS_GO_DRAWER || []);
    const co = (v) => v !== null && v !== undefined && v !== '';
    let chua = 0, doan = 0;
    go.forEach(function (f) {
      const tay = (d.sua_tay || {})[f];
      if (tay && co(tay.value_after)) return;         // nguoi da chot
      if (co(d[f])) return;                           // so goc co noi
      // ⚠ Con lai: hoac may goi y *(⛔ chua ai xac nhan)*, hoac ⛔ khong gi ca.
      //   Hai ca nay KHAC NHAU va ⛔ khong duoc gop — mot ben la "co so nhung
      //   chua ai chiu trach nhiem", mot ben la "⛔ khong co gi".
      if (co(d[f + '_thyt'])) doan++;
      else chua++;
    });
    return {
      chua: chua, doan: doan,
      moi_noi: (d.moi_noi || []).length,
      but_toan: (d.but_toan || []).length,
      nhat_ky: (nk || []).length,
      chot: d.period_state === 'locked',
      alloc_na: !!d.alloc_na,
      xong: !!d.da_xong
    };
  }

  /* ═══ ⭐⭐ MOT bang `KIEM TRA`, roi MOT dong trang thai ═══════
     ⛔⛔ **Cho nay tung la mot dai TAM chip.** Dai ay ⛔ khong sai — moi chip
     la mot phep dem that — nhung no bay tam tin hieu **cung mot luc** va
     **cung mot trong luong**, nen mat ⛔ khong biet nhin dau truoc. Cong voi
     111 dau `⛔` quanh do thi thanh dung cai ke toan goi la *"kho nhin"*.

     ⭐ Luat cua ban thiet ke: **toi da MOT bang bao moi panel**, danh cho thu
     **it, hiem va that**. `chua phan loai` ⛔ **KHONG** thuoc nhom do — do la
     trang thai cua **76,6%** cuon so *(7.682 / 10.030 dong)*. Ve no bang mau
     bao dong thi man hinh luc nao cung dang keu, va khi co chuyen that thi
     ⛔ khong con nac nao cao hon de dung.

     ⚠ **Cai bi mat khi bo dai chip: phep NHAY xuong nhom.** Do la mot mat
     that. Bu lai bang viec **xep lai thu hang** — khoi 7 o go duoc nay nam
     ngay duoi dong trang thai, nen cho can den nhat ⛔ khong con phai nhay. */
  function _ve_phan_quyet(p, d, nk) {
    const o = p.querySelector ? p.querySelector('#so-phan-quyet') : null;
    if (!o) return null;
    const v = _dem_viec(d, nk);
    o.textContent = '';
    o.className = 'pq-vo';

    const kt = _viec_kiem(d);
    if (kt.length) {
      const b = TP.el('div', 'kt');
      b.id = 'so-kiem-tra';
      b.appendChild(TP.el('span', 'nhan', 'KIỂM TRA'));
      if (kt.length === 1) {
        b.appendChild(TP.el('div', '', TP.chu(kt[0])));
      } else {
        const ul = TP.el('ul');
        kt.forEach(x => ul.appendChild(TP.el('li', '', TP.chu(x))));
        b.appendChild(ul);
      }
      o.appendChild(b);
    }

    /* ⭐ Dong trang thai. ⛔ ⛔ Khong bao gio de RONG: mot dong rong trong
       y het *"chua tinh xong"*, ma that ra la *"dong nay sach"*. */
    const tt = TP.el('div', 'tt-dong');
    tt.id = 'so-trang-thai';
    if (!v.chua && !v.doan && !v.alloc_na) {
      tt.classList.add('xong');
      tt.textContent = '✓ Đã phân loại'
        + (v.moi_noi ? ' · ' + v.moi_noi + ' lệnh chi đã ghép'
                     : ' · chưa ghép lệnh chi');
    } else {
      const m = [];
      if (v.chua) m.push('còn ' + v.chua + ' ô trống');
      if (v.doan) m.push(v.doan + ' ô máy gợi ý, chưa ai xác nhận');
      if (v.alloc_na) m.push('phân bổ tra không ra');
      tt.textContent = 'Chưa phân loại — ' + m.join(', ')
        + '. Việc đang chờ, không phải sự cố.';
    }
    o.appendChild(tt);
    return v;
  }

  /* ═══ ⭐⭐ BA VIEC DANG BANG BAO — va CHI ba ═════════════
     ⛔⛔ **Mot bang bao chi dang gia bang do HIEM cua no.** Nen ham nay la mot
     ban khai **dong**: them mot dong vao day la lam moi dong khac nhat di, va
     phai kem **con so do duoc** ve tan so.

     ⚠⚠ **`US-032` da phai THU HEP, va day la ly do.** Ban thiet ke viet luat
     la `le != le_payer`. Do that tren kho: luat ay bao tren **1.304 dong
     (13%)** — ke toan gap bang do **mot tren tam dong**, tuc la ta vua tai
     tao dung cai *"kho nhin"* vua cat.

     ⭐ Nguyen nhan: hai cot ⛔ **khong noi cung mot tu vung**. `le` co **23**
     gia tri, `le_payer` co **16**, trung nhau **44%**; `le` con chua `Cash
     Treasury`, `CN`, `HGO1` — thu ⛔ **khong bao gio** xuat hien o `le_payer`.
     **1.225 / 1.304** bao la kieu ay: so **tao voi cam**, ⛔ khong phai lech
     phap nhan.

     ⇒ Chi bao khi **ca hai** gia tri thuoc **tu vung CHUNG** (`FLS_LE_CHUNG`,
     sinh o `tools/chay_cua.py`). Do lai: **79 dong (0,8%)**, va moi cap con lai
     la hai **ma phap nhan that, khac nhau** (`SGO2` vs `VVOS`). Do moi la *"it,
     hiem, that"*.

     ⚠ Phan bi cat ra ⛔ khong bi **giau**: `_o_le_lech` ghi no xuong ngay duoi
     o `Phap nhan thanh toan` trong digest — `INV-I16`.

     ⭐ `0,8%` la con so **cua hom nay**. Doi luat thi phai **do lai**. */
  function _viec_kiem(d) {
    const ra = [];

    /* ⓐ Ca hai ve tien khac 0. Do that hom nay: **0 dong**. Nhung mot nhanh
       "⛔ khong xay ra" van phai co cau tra loi — de roi xuong nhanh khac thi
       no se **chon ho trong im lang**, dung cai loi vua chua. */
    if (_co_tien(d.ps_no) && _co_tien(d.ps_co))
      ra.push('Cả hai vế Nợ và Có đều khác 0 — máy không chọn hộ một vế. '
            + 'Cần người xác định đây là tiền vào hay tiền ra.');

    // ⓑ Ky da CHOT ⇒ ⛔ khong o nao go duoc, ke ca voi `force` (`INV-I13`).
    if (d.period_state === 'locked')
      ra.push('Kỳ của dòng này đã CHỐT — không ô nào gõ được, kể cả khi '
            + 'bật ghi đè. Muốn sửa thì phải mở lại kỳ.');

    // ⓒ `US-032` — luat THU HEP, xem chu thich tren.
    if (_le_lech(d))
      ra.push('LE khác Pháp nhân thanh toán: ' + String(d.le).trim()
            + ' và ' + String(d.le_payer).trim()
            + ' — hai mã pháp nhân khác nhau trên cùng một dòng. '
            + 'Cần đối chiếu sổ gốc.');

    return ra;
  }

  /* ⭐ `US-032` — phep so CHI ap khi hai gia tri **cung tu vung**.
     ⚠ Day la phep do **CO SO SANH DUOC KHONG**, ⛔ khong phai phep do **DUNG
     SAI** ⇒ no ⛔ khong pham `INV-I18`: no ⛔ khong dung du lieu de **cuong
     che** mot gia tri, no dung du lieu de biet hai o co cung **don vi do** hay
     khong. */
  function _le_lech(d) {
    const a = String(d.le || '').trim(), b = String(d.le_payer || '').trim();
    if (!a || !b || a === b) return false;
    const ch = window.FLS_LE_CHUNG || [];
    return ch.indexOf(a) >= 0 && ch.indexOf(b) >= 0;
  }

  function _than_vao(p, noi_dung) {
    const s = TP.el('div', 'dscroll');
    // ⚠ `noi_dung` co the la mot chuoi *(luc dang doc / luc bao loi)* hay mot
    //   **mang THE** *(than that — vi nhom ② mang o nhap)*.
    if (typeof noi_dung === 'string') s.innerHTML = noi_dung;
    else noi_dung.forEach(x => s.appendChild(x));
    p.appendChild(s);
    return s;
  }

  /* ⭐ Xoa ban nho cua MOT dong roi ve lai — dung sau moi phep GHI.
     ⛔ Thieu ham nay thi panel se noi so cu: mot lop lech **im lang**, va no
     im lang o dung cho te nhat *(vua ghi xong, dang nhin de kiem)*. */
  /* ⭐ *"Dang co nguoi go o nao trong panel"* — `null` la ⛔ khong ai.
     ⚠ Mot lan ve lai bi hoan thi ⛔ khong duoc **quen**: no phai chay khi
     nguoi ta roi o. Bo quen la panel noi **so cu** ngay canh o vua doi mau
     xanh — dung cai lop lech `_lam_moi` sinh ra de chan. */
  let _go_panel = null;
  let _cho_lam_moi = null;

  function _lam_moi(itl_id) {
    _nho.delete(itl_id);
    if (_dang_xem !== itl_id) return;
    // ⛔⛔ ⛔ KHONG dung lai panel khi con nguoi dang go trong no — do la cach
    //   con tro bien mat giua chung mot ma. Hoan lai toi luc ho roi o.
    if (_go_panel !== null) { _cho_lam_moi = itl_id; return; }
    _dang_xem = null;
    mo_drawer(itl_id);
  }

  async function mo_drawer(itl_id) {
    const ben = TP.$('#so-ben');
    if (!ben) return;
    // ⛔ Bam lai dung dong dang mo ⇒ ⛔ KHONG goi cua lan nua. Quet bang chuot
    //   la bam nhieu, va moi cu bam mot luot goi cua la mot man cham dan.
    if (_dang_xem === itl_id) return;
    _dang_xem = itl_id;

    const bo = TP.$('#so-wrap');
    if (bo) bo.classList.add('split');
    _danh_dau(itl_id);

    const r = ST.theo_id.get(itl_id) || null;
    ben.textContent = '';
    const p = _vo_panel(itl_id, r);
    ben.appendChild(p);

    const cu = _nho.get(itl_id);
    if (cu) {
      _than_vao(p, _than_drawer(cu[0], cu[1]));
      _ve_phan_quyet(p, cu[0], cu[1]);
      return;
    }

    const s = _than_vao(p, '<div class="muted">đang đọc sổ…</div>');
    let d, nk;
    try {
      d = (await FLS.doc('/ledger/' + itl_id)).data;
      nk = (await FLS.doc('/journal', { itl_id: itl_id })).data.rows || [];
    } catch (e) {
      // ⛔⛔ Loi ve **TRONG panel**, ⛔ khong bat ra mot hop che man: nguoi dung
      //   dang o giua mot cu quet, va mot hop che kin man vi mot dong doc
      //   ⛔ khong duoc la mot cu ngat viec.
      if (_dang_xem !== itl_id) return;
      // ⚠ Cung ly do voi thanh tieu de: **⛔ khong** `innerHTML` roi
      //   `appendChild`. Cau bao loi di vao mot the CON, roi nut la mot the
      //   con thu hai.
      s.textContent = '';
      s.appendChild(TP.el('div', 'note crit',
        '<b>' + TP.chu(e.cau || e.message || e) + '</b>'
        + (e.lam_gi ? '<br>' + TP.chu(e.lam_gi) : '')));
      const b = TP.el('button', 'b tiny pri', 'Thử lại');
      b.onclick = function () { _dang_xem = null; mo_drawer(itl_id); };
      s.appendChild(b);
      return;
    }
    _nho.set(itl_id, [d, nk]);
    // ⛔ Nguoi da bam sang dong khac trong luc cho ⇒ ⛔ khong ve de len panel
    //   cua dong ho dang xem. Day la mot cuoc dua da co that o `F01`.
    if (_dang_xem !== itl_id) return;
    s.textContent = '';
    _than_drawer(d, nk).forEach(x => s.appendChild(x));
    // ⭐ HUONG 1 — dai phan quyet chi dien duoc SAU khi cua tra loi.
    _ve_phan_quyet(p, d, nk);
  }

  /* ⭐ Mot the NHOM co MA — de dai phan quyet nhay toi duoc. */
  function _the_nhom(ma, ten) {
    const b = TP.el('div', 'grp');
    b.id = ma;
    b.appendChild(TP.el('div', 't', ten));
    return b;
  }

  function _the_ma(ma, html) {
    const b = TP.el('div', '', html);
    b.id = ma;
    return b;
  }

  /* ═══ ⑦ Nhật ký — ô THÀNH + ô NGUỒN đọc theo `value_source` ═══════════
     ⭐ `BA-06` v4.8 dòng *"F02 · nhật ký trong drawer"* · `BA-10` v0.8
       `DT-I14` *"Nhật ký của bản đảo — đọc thế nào"* · `KQ-007 F-1`.

     ⛔⛔ **Lỗi đã đo, ⛔ lo xa** *(`KQ-007`, kho TEST, dòng `P1`)*: bỏ ghép
       đảo **mọi** lớp gợi ý máy, và bản đảo ghi nhật ký `value_after = NULL`
       *(luật GHI ⛔ đổi — `NULL` nghĩa "lớp này hết hiệu lực")*. Bảng cũ in
       nguyên ô **trống** ⇒ dòng cuối của ô `hd` đọc thành *"HD-A → (trống)"*
       ngay dưới dòng người vừa gõ `HD-NGUOI` ⇒ người đọc từ trên xuống
       **tưởng giá trị mình gõ đã mất**. Thật ra gợi ý máy **⛔ bao giờ** là
       Final *(`QĐ-ITL-149`)* nên rút nó ⛔ đổi Final.
       ⇒ Màn nói đúng điều ấy: *"rút gợi ý"*, ⛔ một ô trống.

     ⛔ Nhãn nguồn: chỉ **hai** mã có nhãn người đọc. Mã khác *(hay rỗng)* ⇒
       in **nguyên mã** — ⛔ đoán nhãn cho một mã chưa ai khai *(spec nói thẳng)*.
     ⚠ Spec viết *"máy gợi ý · ⛔ đổi Final"*; tệp này nằm trong luật ký hiệu
       *(`test_luat_ky_hieu_man_hinh.py` — `⛔` cấm trong VĂN BẢN)* ⇒ chữ trơn
       *"không đổi Final"* *(`WO-008` Rủi ro 1)*.
     ⚠ ~~Ca **nhánh 8** *(`sua_tay` cũ dưới giá trị người)* vẫn in trống với
       nguồn *"người sửa"* — spec v4.8 **chấp nhận** *(sổ thật 0, tập đóng)*.~~
       ⛔⛔ *(đính chính `WO-023` `(f)` — `BA-06` v4.12, `KQ-025 F-3`)* câu
       *"chấp nhận · tập đóng"* **sai**: nút `Đảo` ở ⑥ có trên **mọi** bút toán
       ⛔ phải bản đảo ⇒ tập **mở**; đo `KQ-025` *(8099, chuột thật)*: người gõ
       `HD-NGUOI-C` rồi `Đảo` ⇒ ⑦ in `HD-NGUOI-C → (trống) · người sửa` —
       **y hệt** một cú người xoá ô, trong khi Final lùi về lớp dưới.
     ⭐ v4.12: cửa `GET /journal` trả `la_ban_dao` *(`BA-07` v3.6)* ⇒ ô
       **thành** theo bảng ⓐ…ⓔ *(xem `_nk_thanh`)*; cột **nguồn** ⛔ đổi. */
  const NHAN_NGUON_NK = { may_goi_y: 'máy gợi ý · không đổi Final',
                          sua_tay: 'người sửa' };

  function _nk_nguon(ma) {
    return Object.prototype.hasOwnProperty.call(NHAN_NGUON_NK, ma)
      ? NHAN_NGUON_NK[ma] : TP.chu(ma);
  }

  /* ⭐ `BA-06` v4.12 dòng *"F02 · nhật ký"* — bảng ⓐ…ⓔ:
       ⓐ bản đảo ∧ `may_goi_y` ⇒ *"rút gợi ý"* *(như v4.8 — ⛔ đổi)*
       ⓑ bản đảo ∧ `sua_tay`   ⇒ chữ mờ *"đảo — giá trị này hết hiệu lực"*
       ⓒ ⛔ bản đảo ∧ `sua_tay` ∧ `value_after` rỗng ⇒ chữ mờ *"xoá ô"*
       ⓓ còn lại ⇒ như v4.8 *(giá trị đậm / *"gợi ý: X"*)*
       ⓔ cửa ⛔ trả `la_ban_dao` *(thiếu / `null`)* ⇒ như hôm nay — ⛔ đoán.
     ⚠ ⛔ in *"Final về <giá trị>"*: đảo một giá trị người **⛔ nằm trên cùng**
       *(gõ A rồi B, đảo A)* thì Final **⛔ đổi** — câu *"hết hiệu lực"* luôn
       đúng, câu về Final thì ⛔. ⛔ So `value_after` rỗng để đoán bản đảo: cú
       xoá ô **cũng** rỗng — đúng lỗi `KQ-025 F-3`. */
  function _nk_thanh(x) {
    const v = x.value_after;
    const rong = v === null || v === undefined || v === '';
    const dao = x.la_ban_dao;
    if (x.value_source === 'may_goi_y') {
      return rong || dao === true ? '<span class="muted">rút gợi ý</span>'
                                  : 'gợi ý: <b>' + TP.chu(v) + '</b>';
    }
    if (x.value_source === 'sua_tay' && dao === true)
      return '<span class="muted">đảo — giá trị này hết hiệu lực</span>';
    if (x.value_source === 'sua_tay' && dao === false && rong)
      return '<span class="muted">xoá ô</span>';
    return '<b>' + TP.chu(v) + '</b>';
  }

  function _nhom(ten, html) {
    return '<div class="grp"><div class="t">' + ten + '</div>' + html + '</div>';
  }

  /* ═══ ĐỦ 38 CỘT cua so goc ════════════════════════════════════════════
     ⛔⛔ **Cua VAN LUON tra ve chung — man chi ⛔ khong ve.** `GET /ledger/{id}`
     tra `canon`: mot mang **38 phan tu**, dung thu tu `A..AL` cua so. Man cu
     doc **chin** o trong nhom ①, va cai chu giai cua chinh no thi hua *"36 cot
     canon"* ⇒ mot **loi hua** nua ⛔ khong co gi phia sau, cung lop voi dau
     `✎` o nhom ②.

     ⭐ **Phai hien CHU CAI ben canh ten.** Bon o `AH..AK` deu ten *"MID I
     DoubleCheck LE"*, va `W/X` trung ten voi `AB/AC`. Neu chi hien TEN thi
     bon o giong het nhau va ⛔ khong ai biet o nao la o nao — dung khuyet tat
     so 1 ma `fls/canon/spec.py` canh, va da co mot bai kiem giu no.

     ⚠ Hai o `Z`/`AA` **TRONG co y** trong khuon. Van liet ke chung, ghi ro
     *"(ô trống trong khuôn)"*: bo di thi nguoi doi chieu se dem lech vi tri. */
  /* ═══ ⭐⭐ HUONG 4 · XEP DOI O NGAN ═══════════════════════════════════
     Phan lon gia tri trong panel la **ma ngan** — `VGOH`, `PM02279`, mot ngay,
     mot trang thai. Chung dang chiem tron mot dong **430 diem** moi cai, phi
     gan nua be ngang.

     ⚠ **Nguong 18 ky tu ⛔ khong phai mot con so tuy hung.** Cot nhan chiem
     150px, con lai ~265px cho gia tri o kho `mono` 12px ⇒ vua chung **28** ky
     tu; chia doi con **~13**. Lay **18** de mot ma 16–18 ky tu ⛔ khong bi cat:
     no van vua mot dong khi xep doi *(o co `overflow-wrap`)*, con dai hon thi
     tra ve nguyen dong. ⛔ Man ⛔ khong duoc **cat** chu — mot ma bi cat mot
     ky tu la mot ma sai.                                                     */
  const NGAN = 18;

  function _o_doi(nhan, v, ghi, van) {
    const o = TP.el('div', 'o');
    o.appendChild(TP.el('span', 'k', nhan));
    /* ⭐ `van` = o nay la van xuoi ⇒ chu thuong. Moi o khac chu may. Co nay
       den tu ban khai `VAN_XUOI` (`fls/api/cot_so.py`) — ⛔ khong doan o day,
       va ⛔ khong doan theo do dai gia tri (do dung la loi cu). */
    const g = TP.el('span', van ? 'v van' : 'v',
      v === null || v === undefined || v === ''
        ? '<span class="rong">—</span>' : TP.chu(v));
    o.appendChild(g);
    if (ghi) o.appendChild(TP.el('div', 'src', ghi));
    return o;
  }

  /* ⭐ Xep mot danh sach `[nhan, gia tri, ghi chu]` — o NGAN vao luoi hai cot,
     o DAI tra ve nguyen dong. ⛔ May tu chon theo do dai, ⛔ khong khai tay
     tung o: khai tay thi mot ngay nao do so that dai ra ma ban khai dung yen. */
  function _xep(bo, ds) {
    let doi = null;
    ds.forEach(function (x) {
      const v = x[1] === null || x[1] === undefined ? '' : String(x[1]);
      if (v.length <= NGAN && !x[2]) {
        if (!doi) { doi = TP.el('div', 'doi'); bo.appendChild(doi); }
        doi.appendChild(_o_doi(x[0], v, '', x[3]));
      } else {
        doi = null;
        const f = TP.el('div', 'fld');
        f.appendChild(TP.el('div', '', x[0]));
        const p = TP.el('div', x[3] ? 'van' : '');
        p.appendChild(TP.el('div', '',
          v === '' ? '<span class="muted">—</span>' : TP.chu(v)));
        if (x[2]) p.appendChild(TP.el('div', 'src', x[2]));
        f.appendChild(p);
        bo.appendChild(f);
      }
    });
  }

  /* ═══ ⭐⭐ HUONG 2 · GAP O RONG, NHUNG DEM RA ═══════════════════════════
     ⛔⛔ Do tren **200 dong that**: `5.130 / 5.400` o canon la **RONG (95%)**.
     Nghia la khoi *"du 38 cot"* gan nhu toan dau gach, va no day moi thu dang
     doc xuong duoi hai man.

     ⭐⭐ **Va day la cho de sai nhat cua ca ba huong:** an ma ⛔ KHONG DEM la
     vi pham `INV-I16` — nguoi doc se tuong so chi co 7 cot. ⇒ Dong gap **phai
     mang con so**, va bam vao no thi bung ra du.                            */
  function _khoi_canon(d) {
    const bo = TP.el('div');
    const ds = window.FLS_CANON || [];
    const v = d.canon || [];
    if (!ds.length || !v.length) {
      bo.appendChild(TP.el('div', 'pad', '<span class="muted">'
        + (!ds.length
           ? 'không có bản khai khuôn canon '
             + '(<span class="mono">cot.js</span>)'
           : 'cửa không trả cột <span class="mono">canon</span> cho dòng '
             + 'này')
        + '</span>'));
      return bo;
    }
    const co = [], rong = [];
    ds.forEach(function (k, i) {
      const o = v[i];
      const nhan = '<span class="mono muted">' + k.letter + '</span> '
                 + (k.nhan ? TP.chu(k.nhan)
                           : '<span class="muted">(ô trống trong khuôn)</span>');
      (o === null || o === undefined || o === '' ? rong : co)
        .push([nhan, o, '', k.van]);
    });
    _xep(bo, co);

    if (rong.length) {
      const g = TP.el('div', 'gapfold');
      g.id = 'so-gap-canon';
      const bung = TP.el('div');
      let mo = false;
      const _ve = function () {
        g.textContent = '';
        g.appendChild(TP.el('span', 'mono', mo ? '⊟' : '⊞'));
        g.appendChild(TP.el('span', '',
          (mo ? 'thu lại ' : 'bấm để xem ')
          + '<b class="mono">' + rong.length + '</b> ô trống'));
        const ten = rong.map(x => x[0].split('</span> ')[0]
                                     .replace('<span class="mono muted">', ''))
                        .join(' · ');
        const c = TP.el('span', 'chip', TP.chu(ten));
        c.style.marginLeft = 'auto';
        c.title = 'Các vị trí đang trống: ' + ten;
        g.appendChild(c);
      };
      g.onclick = function () {
        mo = !mo;
        bung.textContent = '';
        if (mo) _xep(bung, rong);
        _ve();
      };
      _ve();
      bo.appendChild(g);
      bo.appendChild(bung);
    }
    return bo;
  }

  function _o_fld(nhan, v, ghi) {
    return '<div class="fld"><div>' + TP.chu(nhan) + '</div><div>'
      + (v === null || v === undefined || v === '' ? '<span class="muted">—'
         + '</span>' : TP.chu(v))
      + (ghi ? '<div class="src">' + ghi + '</div>' : '') + '</div></div>';
  }

  function _than_drawer(d, nk) {
    const c = COT();
    /* ⛔⛔ LOI THAT (owner bat 04/09, anh chup che do QUET): ban tra ten nay
       tung dung `COT()` — bang **da loc theo che do**. O che do Quet no chi
       con **9 cot**, nen ba o cua panel ⛔ khong tra duoc ten va roi ve nhanh
       du phong `|| f` ⇒ man in ra **ten truong trong may**:

           `DOC_NO`  `CURR`  `LE_PAYER`

       trong khi ten tieng Viet DA CO SAN trong ban khai (`Số chứng từ` ·
       `Đơn vị tiền tệ` · `Pháp nhân thanh toán`). Doi sang che do Go thi
       chung lai dung ⇒ **cung mot o, hai cai ten**, va ⛔ khong ai duoc bao.

       ⚠ No con hong hon mot cai ten: thieu ban khai thi `kieu` cung roi ve
       `'chu'`, nen `curr`/`le_payer` *(kieu `chip`)* bi ve **sai hinh**.

       ⇒ Panel doc bang **DAY DU** (`COT_DU`). Panel ⛔ khong phai cai luoi:
       che do quyet dinh **luoi bay bao nhieu cot**, no ⛔ khong duoc quyet
       dinh **mot o ten la gi**.                                             */
    const tat_ca = COT_DU();
    const ten = {};
    tat_ca.forEach(k => { ten[k.truong] = k.nhan; });

    // ① Chung tu — doc. ⭐ HUONG 4: o NGAN xep doi, o DAI tra ve nguyen dong.
    const g1 = ['doc_date', 'doc_no', 'memo', 'curr', 'ps_no', 'ps_co',
                'acct', 'le', 'le_payer'].map(function (f) {
      const k = tat_ca.find(x => x.truong === f) || { kieu: 'chu' };
      return [ten[f] || f, _hien(k, d[f], d.curr), '', k.van];
    });

    // ② Bay o SUA — nguon noi gi vs nguoi go gi. ⇒ dung `_nhom_go` (the THAT,
    //    ⛔ khong phai chuoi) vi o che do QUET day la **cho sua**.

    // ③ PHAN BO 🔒 — ba o, MAY suy. Nguoi ⛔ khong go duoc (`QĐ-ITL-64`).
    const na = !!d.alloc_na;
    /* ⭐⭐ BA trang thai, BA hinh — rang buoc #3 cua ban thiet ke.
       ⛔⛔ Truoc do `#N/A` ve bang mau **canh bao** (trong nhu mot **loi**, ma
       no la mot **cau tra loi**), con o rong ve bang `—` xam (trong y het
       *"⛔ chua ai gan"*, ma that ra la *"may ⛔ chua ghi gi"*). Hai thu khac
       han bi ve gan giong nhau, va **ca hai bi ve sai loai**. */
    const _pb = function (v) {
      if (na)
        return '<span class="na-o mono">#N/A</span>'
             + '<div class="src">máy tra không ra — đây là câu trả lồi</div>';
      if (v === null || v === undefined || v === '')
        return '<span class="pb-rong">rỗng — máy chưa ghi gì</span>';
      return TP.chu(v);
    };
    let g3 = '<div class="fld"><div>Chủ dự toán · CFA1</div><div>'
        + _pb(d.alloc_cfa1) + '</div></div>'
        + '<div class="fld"><div>Phân bổ CFA2</div><div>'
        + _pb(d.alloc_cfa2) + '</div></div>'
        + '<div class="fld"><div>Cách phân bổ</div><div>'
        + (na ? _pb(null)
             : (String(d.alloc_method) === '0'
                ? '<span class="mono">0</span><div class="src need">bẫy '
                  + '<span class="mono">VLOOKUP</span>: ô <b>Method</b> của '
                  + 'danh mục <b>RỖNG</b>, nên Sheets trả về <b>0</b>. Sổ thật '
                  + 'cũng đang hiện đúng <b>0</b> — màn không chữa cho đẹp.'
                  + '</div>'
                : TP.chu(d.alloc_method)))
        + '</div></div>';
    g3 += '<div class="pad"><div class="note' + (na ? ' warn' : '')
        + '" style="margin:0">'
        + (na
           ? '<b>Không tra được mã hợp đồng <span class="mono">'
             + TP.chu(d.hd || '(trống)') + '</span></b> trong <b>Mapping '
             + 'Master</b>. Đây là một <b>câu trả lời</b>, không phải một '
             + 'lỗi — và sổ thật cũng đang hiện <span class="mono">#N/A</span> '
             + 'ở đây (<span class="mono">INV-I16</span>).'
           : 'Ba ô này <b>MÁY suy</b> từ <b>Chủ dự toán</b> + <b>Mã hợp '
             + 'đồng</b> + <b>Mapping Master</b> cột K/L. Người <b>không '
             + 'gõ được</b>: <span class="mono">QĐ-ITL-64</span> đã đưa cả ba '
             + 'ra khỏi tập trường gõ được, vì trên sheet chúng là <b>công '
             + 'thức</b> — quyết định phân bổ nằm ở <b>danh mục</b>, không '
             + 'ở dòng sổ.')
        + '</div></div>';

    // ④ Hoa don — chip N tep, va ca "ten tro" (`GAP-SCR-08`).
    let g4;
    const hoa = d.invoice;
    if (!hoa) {
      g4 = '<div class="pad"><span class="muted">chưa có hoá đơn</span></div>';
    } else {
      const tep = String(hoa).split(/[,;\n]/).map(x => x.trim())
                             .filter(x => x !== '');
      g4 = '<div class="pad">' + tep.map(function (t) {
        const co_link = /^https?:\/\//i.test(t);
        return co_link
          ? '<a class="chip info" href="' + TP.chu(t)
            + '" target="_blank" rel="noreferrer">📎 tệp</a> '
          // ⛔ Ten tro ⇒ chip XAM + noi thang, ⛔ KHONG mot chip bam duoc
          // ma bam vao ⛔ khong di dau (`GAP-SCR-08`).
          : '<span class="chip lock" title="chỉ có TÊN tệp, không có '
            + 'link — cần người bổ sung (GAP-SCR-08)">📄 ' + TP.chu(t)
            + ' không mở được</span> ';
      }).join('') + '</div>';
    }

    // ⑤ Moi noi lenh chi.
    const mn = (d.moi_noi || []);
    const bo = (d.moi_noi_da_bo || []);
    let g5 = '<div class="pad">';
    g5 += mn.length
      ? '<table><thead><tr><th>lệnh chi</th><th class="r">tiền</th>'
        + '<th>hình</th><th class="r">lần</th></tr></thead><tbody>'
        + mn.map(x => '<tr><td class="mono">' + TP.chu(x.pm_line_id)
            /* ⭐ Moi noi CUNG tien te voi dong so: cua ghep tu choi khac
               tien te *(`ghi_tay.ghep_lenh` ⓔ `KhacTienTe`)* ⇒ `d.curr`. */
            + '</td><td class="r">' + TP.tien(x.amount, d.curr) + '</td><td>'
            + TP.chu(x.hinh) + '</td><td class="r">' + TP.so(x.lan)
            + '</td></tr>').join('') + '</tbody></table>'
      : '<span class="muted">chưa ghép lệnh chi nào</span>';
    if (bo.length)
      g5 += '<div class="note" style="margin-top:9px">Dòng này đã <b>bỏ '
          + 'ghép ' + bo.length + ' lần</b> — sổ giữ nguyên lịch sử, không '
          + 'lần nào biến mất.</div>';
    g5 += '</div>';

    // ⑥ But toan + nut DAO.
    const bt = (d.but_toan || []);
    let g6 = '<div class="pad">';
    g6 += bt.length
      ? '<table><thead><tr><th>#</th><th>ô</th><th>giá trị</th><th>ai</th>'
        + '<th></th></tr></thead><tbody>'
        + bt.map(x => '<tr><td class="mono">' + x.adj_id + '</td><td>'
            + TP.chu(x.field) + '</td><td>' + TP.chu(x.value_after)
            + '</td><td class="muted">' + TP.chu(x.actor) + '</td><td>'
            + (x.reversal_of ? '<span class="chip lock">bản đảo của #'
                 + x.reversal_of + '</span>'
               : '<button class="b tiny" data-dao="' + x.adj_id
                 /* ⭐ `WO-023` `(g)`: lớp của **chính** bút toán *(⛔ suy theo
                    ô — ô có thể mang gợi ý máy **dưới** giá trị người)* */
                 + '" data-nguon="' + TP.chu(x.nguon == null ? '' : x.nguon)
                 + '">Đảo</button>')
            + '</td></tr>').join('') + '</tbody></table>'
      : '<span class="muted">chưa ai gõ tay ô nào của dòng này</span>';
    g6 += '</div>';

    // ⑦ Nhat ky — `AUD-1` bay truong.
    let g7 = '<div class="pad">';
    g7 += nk.length
      ? '<table><thead><tr><th>lúc</th><th>ô</th><th>từ</th><th>thành</th>'
        + '<th>ai</th><th>nguồn</th><th>vì sao</th></tr></thead><tbody>'
        + nk.map(x => '<tr><td class="mono">'
            + TP.chu(String(x.at).slice(0, 16)) + '</td><td>'
            + TP.chu(x.field) + '</td><td class="muted">'
            + TP.chu(x.value_before) + '</td><td>'
            + _nk_thanh(x) + '</td><td>' + TP.chu(x.actor)
            + '</td><td class="muted">' + _nk_nguon(x.value_source)
            + '</td><td>' + TP.chu(x.reason) + '</td></tr>').join('')
        + '</tbody></table>'
      : '<span class="muted">nhật ký trống — chưa ai sửa dòng này</span>';
    g7 += '</div>';

    const ban = d.da_xong
      ? '<div class="note ok">Dòng này <b>đã được bấm xong</b> bởi <b>'
        + TP.chu(d.da_xong.actor) + '</b> lúc '
        + TP.chu(String(d.da_xong.at).slice(0, 16)) + '.</div>'
      : '';

    setTimeout(function () {
      document.querySelectorAll('[data-dao]').forEach(function (b) {
        b.onclick = () => _dao(Number(b.dataset.dao), d.itl_id, b.dataset.nguon);
      });
    }, 0);

    // ⚠⚠ Tra ve **mot mang THE**, ⛔ khong phai mot chuoi. Nhom ② co o nhap
    //   that, ma mot `<input>` sinh ra tu `innerHTML` thi ⛔ khong noi duoc
    //   `oninput` vao — no se trong nhu go duoc va **⛔ khong luu gi ca**.
    // ⭐ Moi nhom mang MOT MA — dai phan quyet bam vao chip thi nhay thang
    //   xuong dung nhom. ⛔ Mot chip ⛔ khong dan di dau la mot chip noi doi
    //   ve chinh viec no lam duoc.
    /* ═══ ⭐⭐ THU TU CAC KHOI — xep lai theo THU HANG (04/09) ════════════
       ⛔⛔ **Truoc do bay khoi nang ngang nhau**, va khoi 7 o go duoc nam
       **THU BA** — sau hai khoi **chi doc**, trong do co khoi *"du 38 cot"*
       voi **95% o rong**. Ke toan mo panel ra la de **go 7 o**; sau khoi kia
       la de **tra khi can**. Ban thiet ke goi day la loi thu ba.

       ⇒ Thu tu moi:
         ① khoi PHAN LOAI *(7 o go duoc)*  — ⭐ **ly do panel ton tai**
         ② Phan bo *(may suy)*
         ③ Moi noi lenh chi
         ④ Hoa don
         ⑤ But toan tay
         ⑥ So goc 38 cot *(gap lai, xuong CUOI)*
         ⑦ Nhat ky

       ⚠ **Khoi `① Chứng từ` cu ⛔ BIEN MAT khoi day** — ⛔ khong phai bi xoa:
       ca **chin** o cua no da nam trong **digest** *(vung ⛔ khong cuon)*, nen
       giu lai o day la hien **hai lan cung mot du lieu**, va ke toan se hoi
       *"cai nao dung"* — mot cau hoi man hinh tu tao ra.
       ⇒ `g1` van tinh o tren *(no re)*, nhung ⛔ khong con duoc ve. */
    const ra = [];
    if (ban) ra.push(TP.el('div', '', ban));

    ra.push(_nhom_go(d, ten, c));
    ra.push(_the_ma('so-nhom-3', _nhom(
      /* ⭐ The chu thay dau `🔒` da bi cat. Mau `--info` **kem chu** —
         mau ⛔ khong bao gio la thu DUY NHAT cho mot nghia (rang buoc #9). */
      '② PHÂN BỔ <span class="the-may">máy suy — không gõ được</span>',
      g3)));
    ra.push(_the_ma('so-nhom-5', _nhom('③ Mối nối lệnh chi', g5)));
    ra.push(_the_ma('so-nhom-4', _nhom('④ Hoá đơn', g4)));
    ra.push(_the_ma('so-nhom-6', _nhom('⑤ Bút toán tay', g6)));

    // ⭐⭐ ĐỦ 38 CỘT — xuong CUOI, o rong gap lai *(co DEM)*: 95% o canon rong.
    const n1b = _the_nhom('so-nhom-1b',
      '⑥ Sổ gốc · <b>38 cột</b> · <span class="muted">chỉ đọc — '
      + 'nguyên văn ô sổ</span>');
    n1b.appendChild(_khoi_canon(d));
    ra.push(n1b);

    ra.push(_the_ma('so-nhom-7',
      _nhom('⑦ Nhật ký · <span class="mono">AUD-1</span>', g7)));
    return ra;
  }

  /* ═══ ② BAY O GO DUOC — va o che do QUET day la CHO SUA ═══════════════
     ⛔⛔ **Truoc hom nay nhom nay noi doi mot cach im lang:** moi nhan deu co
     dau `✎` *(va hai o con ghi "chi o day")*, nhung ⛔ **khong mot o nhap
     nao** — ⇒ hai truong `id_payee` · `invoice` **⛔ khong sua duoc o BAT KY
     dau** trong ca san pham, du bang tuyen va `TRUONG_GHI` deu noi chung sua
     duoc. Mot dau `✎` ⛔ khong co gi phia sau la mot **loi hua**, ⛔ khong
     phai mot tinh nang.

     ⭐ Ba nguon cua **cung mot o** van phai phan biet duoc *(`QĐ-ITL-35`)* —
     phep sua ⛔ khong duoc xoa cau *"so goc noi gi"*: no nam ngay duoi o nhap.

     ⚠ **⛔ Chua co danh muc de chon.** `FLS-Wireframe` ve mot o bam-de-chon
     lay tu danh muc; cua `GET /catalog` **⛔ chua ai dac ta** (`GAP-SPEC-01`,
     dang chan `B6`). ⇒ O day la **go chu**, va man **noi thang dieu do** chu
     ⛔ khong ve mot o chon rong roi de ke toan bam vao mot cai ⛔ khong mo. */
  function _nhom_go(d, ten, c) {
    const bo = TP.el('div', 'grp');
    bo.id = 'so-nhom-2';
    const sua_o_day = quet();          // che do GO thi sua tren luoi
    bo.appendChild(TP.el('div', 't',
      '② Bảy ô gõ được · <span class="muted">'
      + (sua_o_day ? '<b>sửa Ở ĐÂY</b> — lưới đang chỉ-đọc'
                   : 'nguồn nói gì vs người gõ gì · <b>sửa trên lưới</b>')
      + '</span>'));
    const khoa_ky = d.period_state === 'locked';

    ['hd', 'pay_type', 'cdt1', 'svc_start', 'svc_end']
      .concat(window.FLS_GO_DRAWER || []).forEach(function (f) {
      const chi_o_day = (window.FLS_GO_DRAWER || []).includes(f);
      const tay = (d.sua_tay || {})[f];
      const may = d[f + '_thyt'];
      const nguon = d[f];
      let v, src;
      if (tay) {
        v = tay.value_after;
        src = '<b>người gõ</b> · ' + TP.chu(tay.actor) + ' · '
            + TP.chu(String(tay.at).slice(0, 16));
      } else if (nguon !== null && nguon !== undefined && nguon !== '') {
        v = nguon; src = 'sổ gốc nói';
      } else if (may !== null && may !== undefined && may !== '') {
        v = may; src = '<span class="need">máy gợi ý — chưa ai xác nhận'
                     + '</span>';
      } else {
        v = ''; src = '<span class="need">UNMAPPED — máy không suy được'
                    + '</span>';
      }

      const fld = TP.el('div', 'fld');
      fld.dataset.o = f;
      fld.appendChild(TP.el('div', '', (ten[f] || f) + ' ✎'
        + (chi_o_day ? ' <span class="muted">(chỉ ở đây)</span>' : '')));
      const phai = TP.el('div');
      // ⭐ Go duoc khi: cua cho ghi · ky CHUA chot · va (che do quet HAY o nay
      //   ⛔ khong co cot tren luoi).
      if (cho_ghi() && !khoa_ky && (sua_o_day || chi_o_day)) {
        // ⚠ `_trang_bi` co the tra ve mot the **KHAC** (`pay_type` la
        //   `<select>`) ⇒ phai lay cai duoc tra ve, ⛔ khong dung lai
        //   cai vua tao.
        let ip = TP.el('input', 'inp');
        ip.id = 'so-go-' + f;
        ip.value = v === null || v === undefined ? '' : String(v);
        ip.placeholder = 'chưa gán — gõ vào đây';
        /* ⭐⭐ Trang bi **SAU khi da gan gia tri tho**, va lay cai duoc TRA VE.
           ⛔ Hai rang buoc nguoc chieu nhau ep dung thu tu nay:
             · o KY can phep doi `YYYYMM → YYYY-MM`, ma co `dataset.ky` lai do
               chinh `_trang_bi` dat ⇒ phep doi phai nam TRONG no;
             · `_o_dong` (`pay_type`) phai **DOC duoc gia tri dang co** de biet
               no co nam trong danh sach khong ⇒ gia tri phai co TRUOC.
           Mot thu tu khac se lam mot trong hai o hong **im lang**: o KY hien
           **trong** *(trong y het "⛔ chua ai gan")*, hay o DONG nhay ve muc
           dau roi ghi cai muc ay vao so. */
        ip = _trang_bi(ip, f, phai);
        // ⛔⛔ Truyen CA HAI moc, va chung **khac nhau**:
        //   `hien` = cai o dang HIEN *(co the la goi y cua may)* — dung de
        //     biet nguoi co doi gi khong;
        //   `goc`  = cai **SO** dang noi — dung lam `cu` gui len cua.
        //   Lay goi y cua may lam `cu` la khai mot gia tri **chua tung o
        //   trong so**, va phep so "co nguoi khac go chua" se lech theo.
        /* ⛔⛔ **Loi that** (ke toan bat 04/09). Truoc day cho nay la
           `oninput` — **moi phim mot lan hen gio**. Ma go mot ma nhu
           `SHQ2 | Headquarters2` la **20 ky tu** va nguoi ta co **ngung giua
           chung de tra bang ma**. Ngung 2,5 giay ⇒ may **ghi nua chu** vao so,
           roi `_lam_moi` **dung lai ca panel** ⇒ o nhap bi dung moi, **con tro
           mat**, va phim tiep theo roi vao cho ⛔ khong con ai nhan.

           ⛔ Hau qua ⛔ khong phai phien: **so la chi-them** (`INV-I08`) nen
           gia tri cut **o lai vinh vien**, va nhat ky `AUD-1` — thu dua ra khi
           co nguoi hoi *"ai doi so nay"* — day gia tri cut. ⚠ Va che do
           **Quet la mac dinh**, ma o Quet thi **chi sua duoc trong panel** ⇒
           day la **loi lam viec chinh**, ⛔ khong phai mot goc khuat.

           ⇒ Ghi khi **roi o** hay bam **Enter** — dung nhu o tren luoi
           (`_mo_o` von da lam vay). `onchange` cua trinh duyet ban dung hai
           luc do va **chi khi gia tri that su doi**. */
        const _ghi = function () {
          _dat_panel(fld, d.itl_id, f,
                     ip.dataset.ky ? _ky_vao_so(ip.value) : ip.value,
                     v === null || v === undefined ? '' : String(v),
                     nguon === null || nguon === undefined ? ''
                       : String(nguon));
        };
        ip.onchange = _ghi;
        ip.onkeydown = function (e) {
          if (e && e.key === 'Enter') { _ghi(); if (ip.blur) ip.blur(); }
        };
        /* ⭐ Danh dau *"dang co nguoi go trong panel"* — xem `_lam_moi`. */
        ip.onfocus = function () { _go_panel = f; };
        ip.onblur = function () {
          if (_go_panel === f) _go_panel = null;
          if (_cho_lam_moi !== null) {
            const x = _cho_lam_moi; _cho_lam_moi = null; _lam_moi(x);
          }
        };
        phai.appendChild(ip);
      } else {
        phai.appendChild(TP.el('div', '',
          v === '' ? '<span class="muted">—</span>' : TP.chu(v)));
      }
      phai.appendChild(TP.el('div', 'src', src
        + (khoa_ky ? ' <b>kỳ đã CHỐT</b>' : '')
        + (!cho_ghi() ? ' <b>cửa đang CHỈ ĐỌC</b>' : '')));
      fld.appendChild(phai);
      bo.appendChild(fld);
    });

    /* ⚠ Loi nhac nay **thu hep lai 04/09**: `hd` NAY DA CO goi y that
       *(anh chup `fls_mapping_master`, bom luc khoi dong — xem `_trang_bi`)*,
       va hai o `svc_*` da co o chon thang. ⛔ Nhung **bon o con lai** thi van
       ⛔ khong co danh muc, va `GET /catalog` van la `GAP-SPEC-01`. ⇒ Sua cau
       chu cho **dung pham vi**, ⛔ khong xoa no: xoa la man im lang ve mot cho
       van con thieu. */
    if (quet())
      bo.appendChild(TP.el('div', 'note', '<b>Bốn ô còn lại chưa có '
        + 'danh mục để chọn.</b> <span class="mono">hd</span> đã có gợi ý '
        + '(ảnh chụp danh mục trong kho) và hai ô kỳ đã có ô chọn tháng; '
        + 'nhưng <b>loại giao dịch · chủ dự toán · mã đối tác · hoá đơn</b> '
        + 'thì vẫn <b>gõ chữ</b> — cửa '
        + '<span class="mono">GET /catalog</span> <b>chưa ai đặc tả</b> '
        + '(<span class="mono">GAP-SPEC-01</span>). Màn không vẽ một ô '
        + 'chọn rỗng để bấm vào rồi không mở ra gì.'));
    return bo;
  }

  /* ⭐ Dat mot gia tri tu PANEL vao dung cai hang cho ma luoi dang dung.
     ⛔ ⛔ Khong lam mot duong luu thu hai: mot duong thu hai la mot noi thu hai
     de quen `ly_do`, quen dung-o-o-hong, quen hoi lai cua truoc khi ghi. */
  /* ═══ ⭐⭐ TRANG BI cho mot o go: goi y · khuon · loi nhac ══════════════
     ⛔⛔ Truoc hom nay ca **7 o sua duoc** deu la o go chu **tran** — ⛔ khong
     goi y, ⛔ khong kiem khuon. Ma cua ghi cung ⛔ khong kiem gi ⇒ mot ma go
     nham vao so **nhu that**.

     ⚠ **Hai o `svc_*` ⛔ KHONG phai NGAY** du ten cot doc la *"Thoi diem bat
     dau su dung dich vu"*. Do that: **99,8%** gia tri la `YYYYMM` — mot **KY**.
     Toi tung de xuat dat o chon NGAY o day; do la de xuat **sai**, va no chi
     lo ra khi **do du lieu that** thay vi doc ten cot. Dat o chon ngay la ghi
     `2024-12-01` vao cho so cho doi `202412`. ⇒ chon **THANG**.              */
  const DM_HD = () => (window.FLS_DM_HD || []);

  /* ⭐ So giu `YYYYMM`; o chon thang cua trinh duyet noi `YYYY-MM`. Hai phep
     doi nay la CAU NOI duy nhat giua hai khuon ay. ⛔ Doi o cho khac nua thi
     mot ngay nao do mot cho se quen doi, va `2024-12` se vao so. */
  const _ky_ra_o = (v) => (/^\d{6}$/.test(String(v || ''))
    ? String(v).slice(0, 4) + '-' + String(v).slice(4) : '');
  const _ky_vao_so = (v) => (/^\d{4}-\d{2}$/.test(String(v || ''))
    ? String(v).replace('-', '') : String(v || ''));

  const DM_SUY = (f) => ((window.FLS_DM_SUY || {})[f] || []);

  /* ⭐ Nhung muc chi khac nhau o HOA-THUONG. Do that tren kho: `id_payee` co
     **3 nhom** nhu vay *(vi du `Vd0` va `vd0`)*. ⛔ May ⛔ KHONG tu chon mot
     ben — chon la may quyet dinh cach viet nao dung, ma do la viec cua NGUOI.
     ⇒ Chi **danh dau** de nguoi nhin thay cai lon xon ay. */
  function _trung_hoa_thuong(ds) {
    const dem = {};
    ds.forEach(function (x) {
      const k = String(x).toLowerCase();
      dem[k] = (dem[k] || 0) + 1;
    });
    return ds.filter(x => dem[String(x).toLowerCase()] > 1);
  }

  /* ⭐ Mot `<datalist>` dung chung theo ma — ⛔ khong dung mot the moi moi lan
     mo panel, ⛔ khong thi `<body>` day dan cac ban sao giong het nhau. */
  function _datalist(id, ds) {
    if (document.querySelector('#' + id)) return id;
    const dl = TP.el('datalist');
    dl.id = id;
    ds.forEach(function (m) {
      const o = TP.el('option');
      o.value = m;
      dl.appendChild(o);
    });
    document.body.appendChild(dl);
    return id;
  }

  /* ⚠⚠ Cau chu cho ba o SUY. No **phai** noi *"suy tu ... dang dung"* va ⛔
     **khong duoc** goi la *"danh muc"*: mot danh sach suy tu du lieu thi ⛔
     **khong dua ra duoc gia tri chua ai dung**, va no **dua luon ca loi go cua
     nguoi truoc**. Goi no la danh muc la noi qua ve thu no biet.
     ⇒ Khac han o `hd`: cho ay CO mot ban khai that (73 ma). */
  function _noi_suy(phai, ds, mo) {
    const t = _trung_hoa_thuong(ds);
    phai.appendChild(TP.el('div', 'src',
      'suy từ <b>' + ds.length + ' giá trị đang dùng</b> trong sổ — '
      + '<b>không</b> phải danh mục'
      + (mo ? ', <b>gõ giá trị mới cũng được</b>'
            : ', <b>không</b> nhận giá trị ngoài danh sách')
      + (t.length ? '. <b>' + t.length + ' mục</b> chỉ khác nhau '
                  + '<b>hoa-thường</b> — máy không chọn hộ' : '')));
  }

  /* ═══ ⭐ O DONG — `pay_type` (owner 04/09: ⛔ KHONG cho dien moi) ═══════
     ⛔⛔ **Bay o day, va no im lang:** neu gia tri dang co ⛔ **khong** nam
     trong danh sach thi mot `<select>` se nhay ve muc dau tien, roi lan
     `onchange` dau tien **ghi cai muc ay vao so** — mot dong bi doi gia tri
     **ma ⛔ khong ai bam gi ca**.
     ⇒ Gia tri la thi **giu lai lam mot muc**, danh dau `⚠ ngoai danh sach`,
     va noi ra ben duoi. ⛔ May ⛔ khong bao gio tu doi. */
  function _o_dong(ip, f, phai) {
    const ds = DM_SUY(f);
    if (!ds.length) { _noi_suy(phai, ds, false); return ip; }
    const sl = TP.el('select', 'inp');
    sl.id = ip.id;
    const hien = (ip.value === undefined || ip.value === null)
      ? '' : String(ip.value);
    const co = ds.indexOf(hien) >= 0;
    const dat = function (v, chu) {
      const o = TP.el('option', '', chu === undefined ? v : chu);
      o.value = v;
      sl.appendChild(o);
    };
    dat('', 'chưa gán —');
    if (hien !== '' && !co) dat(hien, hien + '  ngoài danh sách');
    ds.forEach(function (v) { dat(v); });
    sl.value = hien;
    _noi_suy(phai, ds, false);
    if (hien !== '' && !co) {
      phai.appendChild(TP.el('div', 'src need',
        'giá trị đang có <b>không</b> nằm trong danh sách — máy giữ '
        + 'nguyên nó, <b>không</b> tự đổi'));
    }
    return sl;
  }

  /* ⭐⭐ Trang bi mot o go, va **TRA VE the se dung**: `pay_type` la o DONG nen
     no la mot the KHAC han (`<select>`), ⛔ khong phai cai `<input>` duoc dua
     vao. ⇒ Cho goi PHAI lay cai duoc tra ve.

     ⚠ Bon quyet dinh cua owner (04/09) ⇒ **bon kieu o**, va chung ⛔ khong
     duoc trong giong nhau: mot o **dong** ma trong y het mot o **mo** thi ke
     toan se go vao roi moi biet no ⛔ khong nhan. */
  function _trang_bi(ip, f, phai) {
    if (f === 'svc_start' || f === 'svc_end') {
      // ⭐ `type=month` cho ra `YYYY-MM`; so can `YYYYMM` ⇒ bo dau gach khi
      //   ghi, va nap nguoc lai khi hien. Phep doi nam **mot cho**.
      ip.type = 'month';
      ip.dataset.ky = '1';
      // ⚠ O chon thang **⛔ khong nhan** `202412` — no se im lang bo trong,
      //   ma mot o trong o day trong y het *"⛔ chua ai gan"*.
      ip.value = _ky_ra_o(ip.value);
      return ip;
    }
    if (f === 'pay_type') return _o_dong(ip, f, phai);       // ⛔ DONG
    if (f === 'cdt1' || f === 'id_payee') {                  // ⭐ MO
      const suy = DM_SUY(f);
      if (suy.length) ip.setAttribute('list', _datalist('dm-' + f, suy));
      _noi_suy(phai, suy, true);
      return ip;
    }
    if (f !== 'hd') return ip;            // `invoice` — go tay (owner chot)
    const ds = DM_HD();
    if (!ds.length) {
      /* ⛔⛔ Danh muc RONG ⇒ cua cung ⛔ khong kiem duoc (`_kiem_gia_tri`).
         ⭐ Cho rong ay phai **nhin thay duoc o dung cho no co nghia**: ⛔ khong
         de ke toan tuong minh dang duoc kiem trong khi ⛔ khong ai kiem ca. */
      phai.appendChild(TP.el('div', 'src need',
        'chưa có danh mục mã hợp đồng trong kho ⇒ cửa ghi '
        + '<b>không kiểm</b> được giá trị bạn gõ'));
      return ip;
    }
    ip.setAttribute('list', _datalist('dm-hd', ds));
    /* ⭐ Noi ro day la **ANH CHUP**, ⛔ khong phai danh muc song — va noi ca
       LUC chup. Mot danh sach ⛔ khong noi tuoi cua no la mot danh sach nguoi
       ta se tin qua muc. */
    phai.appendChild(TP.el('div', 'src',
      'gõ để lọc trong <b>' + ds.length + ' mã</b> · ảnh chụp lúc '
      + TP.chu(window.FLS_DM_LUC || '?') + ' Master đổi thì phải khởi '
      + 'động lại cửa'));
    return ip;
  }

  function _dat_panel(fld, itl_id, field, v, hien, goc) {
    const k = _khoa(itl_id, field);
    if (v === hien) { ST.cho.delete(k); fld.classList.remove('chua-luu');
                      _tt(); return false; }
    const cu = goc;
    fld.classList.remove('da-luu');
    fld.classList.add('chua-luu');
    ST.cho.set(k, { itl_id: itl_id, field: field, gia_tri: v, cu: cu,
                    td: fld });
    _hen();
    return true;
  }

  /* ⭐⭐ `WO-023` `(g)` *(`BA-06` v4.12 dòng *"F02 · hoàn tác"*, `KQ-025
     F-4`)* — hộp nói hậu quả theo **LỚP** của bút toán bị đảo *(`nguon` của
     **chính** bút toán, `GET /ledger/{itl_id}` `but_toan[].nguon` — `BA-07`
     v3.6)*. ⛔⛔ Bản trước nói *"Sau khi đảo, giá trị lùi về bút toán trước
     đó, hay về giá trị của sổ gốc…"* cho **mọi** bút toán — kể cả gợi ý
     máy, nơi đảo **⛔ đổi Final** *(`QĐ-ITL-149`; tầm **4.424** nút trên sổ
     thật)*. Chữ **nguyên văn** bảng ⓐ…ⓒ; mã lạ ⇒ in mã, ⛔ đoán. */
  function _hau_qua_dao(adj_id, nguon) {
    if (nguon === 'may_goi_y') return ['Rút gợi ý máy #' + adj_id,
      'Đây là gợi ý của máy, không phải giá trị người đã chốt. Rút nó '
      + '<b>không đổi Final</b> — Final vẫn là giá trị người đã gõ, hay giá '
      + 'trị của sổ gốc.'];
    if (nguon === 'sua_tay') return ['Đảo bút toán #' + adj_id,
      'Giá trị này hết hiệu lực. Nếu nó đang là Final thì Final lùi về giá '
      + 'trị người gõ trước đó, hay về giá trị của sổ gốc nếu không còn.'];
    return ['Đảo bút toán #' + adj_id,
      'Bút toán này hết hiệu lực. Máy chưa biết nó thuộc lớp nào ('
      + TP.chu(nguon ? nguon : '—') + ') nên không nói trước Final sẽ ra sao '
      + '— mở nhật ký sau khi đảo để xem.'];
  }

  function _dao(adj_id, itl_id, nguon) {
    const [tieu_de, hau_qua] = _hau_qua_dao(adj_id, nguon);
    HT.mo(tieu_de,
      '<div class="note">Đảo <b>không xoá</b> gì cả — nó <b>thêm một dòng '
      + 'nữa</b> trỏ ngược lại (<span class="mono">SM-I03</span> · '
      + '<span class="mono">INV-I08</span>). ' + hau_qua + '</div>'
      + '<div style="margin-top:8px"><input class="inp" id="so-dao" '
      + 'style="width:100%" placeholder="vì sao đảo…"></div>',
      [['Đảo', async function () {
          const v = (TP.$('#so-dao').value || '').trim();
          if (!v) { TP.$('#so-dao').style.borderColor = 'var(--warn)';
                    return false; }
          try {
            await FLS.ghi('/adjustments/' + adj_id + '/reverse', { reason: v });
          } catch (e) { HT.loi_trong_hop(e); return false; }
          // ⛔⛔ Phai **XOA ban nho** roi **buoc mo lai**. Ban nho la thu lam
          //   panel nhanh, va no cung la thu lam panel **noi so cu** ngay sau
          //   khi vua dao mot but toan — dung luc ke toan can thay ket qua.
          _lam_moi(itl_id);
        }, { pri: true, danger: true }],
       ['Thôi', null]]);
  }

  /* ── ghi chu cuoi man: noi ra ba cho CO Y ⛔ khong ve ────────────────── */
  function _ghi_chu() {
    const d = TP.el('div', 'note warn');
    d.innerHTML =
      '<b>Hai chỗ màn này CỐ Ý không vẽ</b>, và nói ra thay vì để '
      + 'trống:<ul style="margin:6px 0 0 18px">'
      + '<li><b>Hai người sửa một ô</b> — cửa ghi <b>không</b> phát hiện '
      + 'được (<span class="mono">GAP-SCR-09</span>). Màn có hỏi lại cửa ngay '
      + 'trước khi ghi, nhưng đó là một phép <b>kiểm</b>, không phải một '
      + '<b>bảo đảm</b>.</li>'
      + '<li><b>' + TP.chu((window.FLS_GO_DRAWER || []).join(' · '))
      + '</b> không có trên lưới — cửa <span class="mono">GET /ledger</span> '
      + 'không trả hai trường đó. Chúng gõ ở <b>ngăn kéo</b>.</li></ul>';
    return d;
  }

  // ⭐ `_loc` + `_dat` lo ra de bo test **bam duoc** hai hanh vi ay ma
  // ⛔ khong phai gia lap mot su kien `input` cua trinh duyet.
  // ⚠ `_lam_moi` lo ra CHO BO TEST: canh huong *"lo bay xong trong luc
  //   nguoi ta dang go"* la mot canh huong **thoi gian**, va cach duy
  //   nhat de do no ma ⛔ khong phai cho 2,5 giay that la goi thang.
  // ⚠ `_dao` lo ra CHO BO TEST *(`WO-023` `(g)`)*: nut `Đảo` dung tu
  //   `innerHTML` + gan `onclick` trong `setTimeout` ⇒ DOM gia ⛔ phan tich
  //   HTML nen ⛔ bam duoc. Bai doc `data-nguon` cua tung nut trong HTML ⑥
  //   roi goi `_dao` voi **dung** ba tham so nut se goi; Chrome bam nut that.
  return { ve, mo_drawer, dong_drawer, _bay, _loc, _dat, _lam_moi, _dao, ST };
})();
