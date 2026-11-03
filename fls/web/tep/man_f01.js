/* ═══════════════════════════════════════════════════════════════════════
   man_f01.js — **HÀNG CHỜ**. Việc hằng ngày của kế toán (`BA-06` §4).

   ⭐ Năm hành động mỗi dòng: **lý do · hoãn · ghép · bỏ ghép · xong**.
   ⛔ **⛔ Không có nút xoá trắng** — sổ chỉ được THÊM (`INV-I08`).

   ⛔⛔ **Xếp trong TỪNG tiền tệ, ⛔ không gộp.** Đo được: hàng chờ có
   **USD 4.492 dòng (58%)** vs **VND 2.987**. Gộp lại rồi xếp theo con số thì
   **toàn bộ dòng USD bị dìm xuống dưới** — một khoản 300.000 USD xếp sau một
   khoản 400.000 đồng. Vì vậy màn này **luôn lọc theo một tiền tệ**, và chân
   màn ⛔ **không có dòng "tổng"**.

   ⭐⭐ **`Xong` là cách DUY NHẤT một dòng rời hàng chờ** (`QĐ-ITL-71`) — người
   bấm, ⛔ không phải máy tự nhả. ⛔ **Không đòi lý do** (`QĐ-ITL-72`); nhưng
   nếu dòng còn thiếu trường thì màn **PHẢI nói ra**, ⛔ không im lặng.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F01 = (function () {

  /* Trạng thái của phiên xem — ⛔ chỉ để VẼ, ⛔ không phải nguồn sự thật.
     Mọi con số đều đến từ cửa; đây chỉ nhớ *người vừa làm gì* để màn hình nói
     lại được, và để nút **Mở lại** còn chỗ bấm sau khi dòng đã rời hàng chờ. */
  const ST = { curr: null, den_pct: '', con_tro: null, dong: [],
               vua_xong: new Map(), moi_noi: new Map(), het: false,
               /* ⭐⭐⭐ LẰN nào đang mở. **`'lenh'` là mặc định** — xem
                  `_thanh_lan`. */
               lan: 'lenh' };

  /* ⛔ Ô thân của lằn dòng tiền. `ve()` ghi vào đây, ⛔ không ghi thẳng vào
     `#than-f01` nữa: thanh chuyển lằn nằm ở `#than-f01`, và ghi đè cả ô sẽ
     **xoá mất thanh ấy** sau mỗi hành động. */
  let _than_tien = null;

  const CO_GHI = () => !!(window.FLS_PHIEN || {}).cho_ghi;

  /* ── ⛔ cửa đang CHỈ ĐỌC thì nói TRƯỚC, ⛔ không để người bấm rồi mới báo ── */
  function _chan_ghi(nut) {
    if (CO_GHI()) return false;
    nut.disabled = true;
    nut.title = '⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC. Mọi thao tác ghi bị trả '
              + '405. Khởi động lại máy chủ với --cho-ghi (nó sửa SỔ THẬT).';
    return true;
  }

  function _nut(nhan, lop, ham) {
    const b = TP.el('button', 'b tiny' + (lop ? ' ' + lop : ''), nhan);
    if (!_chan_ghi(b)) b.onclick = ham;
    return b;
  }

  /* ══ ① CHÂN MÀN — theo TỪNG tiền tệ ═══════════════════════════════════ */
  function _ve_tom(data, meta, o) {
    const hang = data.theo_tien_te || [];
    const w = TP.el('div', 'row');
    hang.forEach(function (r) {
      const c = TP.el('div', 'card');
      c.style.flex = '1';
      c.style.minWidth = '190px';
      const chon = ST.curr === r.curr;
      c.innerHTML =
        '<div class="pad"><div class="k">' + TP.chu(r.curr) + '</div>' +
        '<div class="v">' + TP.so(r.so_dong) + '</div>' +
        '<div class="muted" style="font-size:12px">dòng chờ · Σ ' +
        TP.tien(r.tien, r.curr) + '</div></div>';
      const b = TP.el('button', 'b' + (chon ? ' pri' : ''),
                      chon ? 'đang xem' : 'Xem');
      b.style.margin = '0 14px 14px';
      b.onclick = () => { ST.curr = r.curr; ve(); };
      c.appendChild(b);
      w.appendChild(c);
    });
    o.appendChild(w);

    const n = TP.el('div', 'note');
    n.innerHTML =
      '⛔ <b>⛔ Không có ô “tổng”</b> — cộng hai đơn vị tiền tệ ra một con số '
      + 'là vô nghĩa. Và hàng chờ <b>xếp trong TỪNG tiền tệ</b>: gộp lại thì '
      + 'một khoản <b>300.000 USD</b> xếp <b>sau</b> một khoản '
      + '<b>400.000 đồng</b>.';
    o.appendChild(n);
  }

  function ve_tom(o) {
    return TT.chay(o, () => FLS.doc('/queue/summary'), _ve_tom, {
      so_dong: 2,
      la_rong: d => !d || !(d.theo_tien_te || []).length,
      rong: { icon: '✓', tieu_de: 'Hàng chờ rỗng',
              cau: 'Màn đẹp nhất của cả hệ: ⛔ không còn dòng nào chờ ai trả lời.' }
    });
  }

  /* ══ ② LƯỚI ═══════════════════════════════════════════════════════════ */
  function _o_hoan(r) {
    if (!r.defer_until) return '';
    // ⚠ Lần thứ ba ĐỔI MÀU, và ⛔ không báo cho ai (`QĐ-ITL-24`): leo cấp là
    // một cơ chế cần người nhận, mà ⛔ không có vai đó (`QĐ-ITL-27`).
    const lop = Number(r.defer_count || 0) >= 3 ? 'crit' : 'lock';
    return TP.chip(lop, 'hoãn đến ' + TP.chu(r.defer_until)
                        + ' · lần ' + TP.chu(r.defer_count),
                   Number(r.defer_count || 0) >= 3
                     ? 'Đã hoãn từ 3 lần — đổi màu để thấy, ⛔ không báo cho ai '
                       + '(⛔ không có vai nhận báo)'
                     : '');
  }

  function _the_dong(r) {
    const xong = ST.vua_xong.get(r.itl_id);
    const noi = ST.moi_noi.get(r.itl_id);
    const tr = TP.el('tr');
    if (xong) tr.style.opacity = '.55';
    tr.innerHTML =
      '<td class="r">' + (xong ? '—' : TP.so(r.hang)) + '</td>' +
      '<td class="mono">' + TP.chu(r.itl_id) + '</td>' +
      '<td class="mono">' + TP.chu(r.doc_no) + '</td>' +
      '<td>' + TP.chu((r.memo || '').slice(0, 60)) +
        (noi ? ' ' + TP.chip('info', 'đã ghép ' + noi + ' dòng lệnh') : '') +
        (xong ? ' ' + TP.chip('ok', 'đã xong') : '') +
        (r.reason ? ' ' + TP.chip('lock', 'lý do: ' + r.reason.slice(0, 28))
                  : '') +
        ' ' + _o_hoan(r) + '</td>' +
      '<td class="r">' + TP.tien(r.tien, r.curr) + '</td>' +
      '<td class="r">' + TP.chu(r.luy_ke_pct) + '%</td>' +
      '<td class="mono">' + TP.chu(r.le || '—') + '</td>';

    const td = TP.el('td');
    td.style.whiteSpace = 'nowrap';
    if (xong) {
      td.appendChild(_nut('Mở lại', '', () => _mo_lai(r)));
    } else {
      td.appendChild(_nut('Lý do', '', () => _ly_do(r)));
      td.appendChild(_nut('Hoãn', '', () => _hoan(r)));
      td.appendChild(_nut('Ghép', 'pri', () => _drawer_ghep(r)));
      if (noi) td.appendChild(_nut('Bỏ ghép', 'danger', () => _bo_ghep(r)));
      td.appendChild(_nut('Xong', '', () => _xong(r)));
    }
    tr.appendChild(td);
    return tr;
  }

  function _ve_luoi(data, meta, o) {
    ST.dong = data.rows || [];
    // ⛔⛔ `next_cursor`, ⛔ KHONG `cursor`. Tham so GUI LEN ten la `cursor`,
    // truong TRA VE ten la `next_cursor` — hai ten khac nhau, va doc nham thi
    // nut "Xem thêm" ⛔ khong bao gio hien: man hinh trong nhu **het danh
    // sach** trong khi con 2.937 dong. Mot loi **im lang** (`GAP-SPEC-02`).
    ST.con_tro = data.next_cursor || null;
    /* ⭐ `WO-045` ③: bảng dựng bằng **cây thẻ** *(⛔ chuỗi `innerHTML` rồi
       `querySelector('tbody')`)* — cùng thẻ, cùng lớp như bản trước *(⛔
       `TP.bang`: nó thêm lớp `g`, đổi dáng lưới)*. Lý do đo được: DOM giả của
       bộ thử *(`dom_gia.js` — ⛔ phân tích HTML, có chủ ý)* trả `tbody`
       **`null`** ⇒ lưới này **⛔ bài nào vẽ được** — nên lỗi chồng lượt
       `ve_luoi` / `_xem_them` *(`BG-044` `(d)` #10 · #11)* ⛔ bài nào thấy. */
    const b = TP.el('table');
    const dau = TP.el('thead');
    const hd = TP.el('tr');
    [['r', 'Hạng'], [null, 'Mã dòng'], [null, 'Số chứng từ'],
     [null, 'Diễn giải'], ['r', 'Tiền'], ['r', '% luỹ kế'],
     [null, 'Pháp nhân'], [null, 'Việc']].forEach(function (c) {
      const th = TP.el('th', c[0]);
      th.textContent = c[1];
      hd.appendChild(th);
    });
    dau.appendChild(hd);
    const tb = TP.el('tbody');
    b.appendChild(dau);
    b.appendChild(tb);
    ST.dong.forEach(r => tb.appendChild(_the_dong(r)));
    const cuon = TP.el('div', 'scroll');
    cuon.appendChild(b);
    o.appendChild(cuon);

    const chan = TP.el('div', 'pad');
    chan.style.borderTop = '1px solid var(--line)';
    chan.innerHTML =
      '<span class="muted" style="font-size:12px">Đang xem <b>'
      + ST.dong.length + '</b> dòng ' + TP.chu(ST.curr)
      + (ST.den_pct ? ' · tới mức phủ <b>' + TP.chu(ST.den_pct) + '%</b>' : '')
      + '</span> ';
    if (ST.con_tro) {
      const b2 = TP.el('button', 'b tiny', 'Xem thêm');
      b2.onclick = () => _xem_them(o, b2);
      chan.appendChild(b2);
    } else {
      chan.insertAdjacentHTML('beforeend',
        ' ' + TP.chip('lock', 'hết danh sách'));
    }
    o.appendChild(chan);

    /* ⚠⚠ **TUỔI VIỆC — khai thẳng là ⛔ CHƯA ĐO ĐƯỢC.**
       `BA-06` §4 đòi *"in tuổi việc (thanh đổi đỏ quá 3 ngày)"*. ⛔ Không cửa
       nào cấp được *"dòng này vào hàng chờ lúc nào"*: `fls_queue_state` ⛔ không
       có cột ấy. Thứ duy nhất gần giống là **ngày chứng từ** — mà cột đó đã đo
       được là **hoán ngày↔tháng ở 93% dòng**. ⇒ Vẽ một thanh đỏ dựa trên nó là
       **bịa một con số trên một trục đã biết là sai**. */
    const c = TP.el('div', 'note warn');
    c.innerHTML =
      '⚠ <b>⛔ Chưa có cột “tuổi việc”</b> — và đó ⛔ không phải quên. '
      + 'Máy ⛔ không biết một dòng <i>vào hàng chờ lúc nào</i>; thứ gần nhất là '
      + '<b>ngày chứng từ</b>, mà cột đó đã đo được là <b>hoán ngày↔tháng ở '
      + '93% dòng</b>. Vẽ thanh đỏ 3 ngày dựa trên nó là bịa một con số trên '
      + 'một trục <b>đã biết là sai</b>. ⇒ Cần một cột thời điểm thật.';
    o.appendChild(c);
  }

  /* ⭐⭐ `WO-045` ③ *(`BA-06` v4.19 `§4.5 ⓦ` ① — `BG-044` `(d)` #10 · #11)*:
     lượt **mới nhất** của lưới. Bản trước: đổi tiền tệ / mức phủ lúc lưới
     đang tải ⇒ lượt **cũ** về sau ghi `ST.dong` + `ST.con_tro` ⇒ `Xem thêm`
     kế tiếp lật trang của **bộ lọc cũ** dưới bộ lọc mới *(bài `test_AC7_…`
     đỏ trên `db0adae`)*; `Xem thêm` bấm hai lần ⇒ hai `GET` cùng con trỏ ⇒
     hàng trùng. Mỗi `ve()` dựng lại lưới *(lưới cũ rời cây)* = một lượt mới. */
  let _luot_luoi = 0;

  /* ⭐⭐ `WO-051` *(`BA-06` v4.22 `§4.5 ⓦ` ⑦ — `KQ-050 F-1`)*: lượt `Xem thêm`
     có **khung chờ** và lỗi **⛔ xoá lưới**.
     ⛔⛔ Bản trước *(đến `9af99c4`)*: ⓐ bấm ⇒ nút **khoá** mà **⛔ một chữ** —
     trang 2 `VND` sổ thật mất **104,33 s** *(`fls-ba` 05/10)* ⇒ người thấy một
     nút xám **gần hai phút** và kết luận màn treo; ⓑ lượt lỗi ⇒ `TT.loi(o, …)`
     thay **cả** khung `o` ⇒ **50** hàng người đang đọc biến mất theo, và nút
     `Thử lại` của `TT.loi` tải lại **từ trang đầu** *(`ve_luoi`)*, ⛔ trang vừa
     lỗi. Cửa đã nhanh lại *(`doc_bao_cao._SQL_HANG_CHO` — trang 2 `VND`
     **0,021 s**)*, nhưng khung chờ là **lưới an toàn**, ⛔ thay cho sửa cửa
     *(`ⓦ` ⑦: hiện cả khi cửa nhanh — chớp một lần, chấp nhận)*.
     ⭐ Bốn trạng thái của lượt *(bảng `ⓦ` ⑦)*:
       · tải — nút khoá + chữ `Đang tải thêm…` *(lớp `b tiny` như nay — ⛔ lớp
         mới)*; hàng đã có **giữ**; ⛔ lượt thứ hai *(`disabled`)*;
       · có dữ liệu — nối hàng, nút về `Xem thêm` / chip `hết danh sách`
         *(`_ve_luoi` vẽ lại chân lưới — như nay)*;
       · lỗi · mất kết nối — hàng **giữ**; thay nút bằng dòng `⛔ Cửa lỗi:
         <e.cau>` *(khuôn chữ + lớp `banner crit` của `ⓦ` ④ — ⛔ câu mới)* ＋
         nút `Thử lại` lớp `b tiny` ⇒ gọi **lại hàm này** với **cùng**
         `ST.con_tro` *(lượt lỗi ⛔ chạm `ST.con_tro` — nó chỉ đổi khi lượt
         **xanh** về)* ⇒ **đúng** con trỏ vừa lỗi, **một** lượt *(nút `Thử lại`
         cũng khoá trong lúc chờ — cùng luật `disabled`)*;
       · rỗng — ⛔ áp *(nút chỉ có khi cửa trả `next_cursor`)*.
     ⛔ Đếm giây trên nút *(một con số chạy là một lời hứa thời gian máy ⛔ giữ
     được — `ⓦ` ⑦)*. ⛔ Đổi `ve_luoi` / luật lượt `WO-045` *(`_luot_luoi`)*. */
  const CHU_DANG_TAI_THEM = 'Đang tải thêm…';

  async function _xem_them(o, b) {
    /* ⭐ nút khoá trong lúc chờ *(như `F02` `:369`)* ⇒ ⛔ lượt thứ hai */
    if (b) {
      if (b.disabled) return;
      b.disabled = true;
      b.textContent = CHU_DANG_TAI_THEM;
    }
    const luot = _luot_luoi;
    try {
      const kq = await FLS.doc('/queue', {
        curr: ST.curr, den_pct: ST.den_pct, cursor: ST.con_tro, limit: 50 });
      if (luot !== _luot_luoi) return;     /* ⭐ lưới đã đổi lọc */
      const them = kq.data.rows || [];
      ST.dong = ST.dong.concat(them);
      ST.con_tro = kq.data.next_cursor || null;
      o.textContent = '';
      _ve_luoi({ rows: ST.dong, next_cursor: ST.con_tro }, kq.meta, o);
    } catch (e) {
      if (luot !== _luot_luoi) return;
      _loi_xem_them(o, b, e);
    }
  }

  /* Lỗi lượt `Xem thêm` ⇒ hàng **giữ**, nút *(`Xem thêm` hay `Thử lại` vừa
     bấm)* nhường chỗ cho câu lỗi + **một** nút `Thử lại`. Chân lưới = cha của
     nút *(`_ve_luoi` dựng)*; ⛔ tìm được ⇒ thêm vào cuối `o` — vẫn **dưới**
     lưới, ⛔ xoá gì. ⛔ Lớp đánh dấu nào: dòng lỗi cũ đã rời màn lúc bấm `Thử
     lại` *(xem `thu.onclick`)*, nên ở đây chỉ còn **đúng** nút `b` để gỡ —
     ⛔ cần tìm lại bằng bộ chọn *(`ⓦ` ⑦: ⛔ lớp CSS mới)*. */
  function _loi_xem_them(o, b, e) {
    const chan = (b && b.parentNode) || o;
    if (b && b.parentNode) b.parentNode.removeChild(b);
    /* ⚠ `textContent`, ⛔ `innerHTML`: câu lỗi mất kết nối mang **nguyên
       văn** thông điệp của trình duyệt *(`goi_cua.js` `FLS-MAT-KET-NOI`)*. */
    const dong = TP.el('p', 'banner crit');
    dong.textContent = '⛔ Cửa lỗi: '
      + ((e && e.cau) || String(e && e.message || e));
    const thu = TP.el('button', 'b tiny', 'Thử lại');
    thu.onclick = () => {
      /* ⭐ dòng lỗi rời màn **khi** lượt mới bắt đầu — lượt lại lỗi thì
         `_loi_xem_them` vẽ dòng mới thay nó *(⛔ hai dòng lỗi chồng nhau)* */
      if (dong.parentNode) dong.parentNode.removeChild(dong);
      return _xem_them(o, thu);
    };
    chan.appendChild(dong);
    chan.appendChild(thu);
  }

  function ve_luoi(o) {
    const luot = ++_luot_luoi;
    return TT.chay(o,
      () => FLS.doc('/queue', { curr: ST.curr, den_pct: ST.den_pct,
                                limit: 50 }),
      _ve_luoi,
      {
        so_dong: 8,
        la_rong: d => !d || !(d.rows || []).length,
        rong: { icon: '✓', tieu_de: 'Không còn dòng nào ở mức lọc này',
                cau: 'Đổi tiền tệ hay bỏ mức phủ để xem tiếp.' },
        con_hieu_luc: () => luot === _luot_luoi
      });
  }

  /* ══ ③ LÝ DO ═════════════════════════════════════════════════════════ */
  function _ly_do(r) {
    HT.mo('Lý do · dòng ' + r.itl_id,
      '<div class="note">Vì sao dòng này còn nằm trong hàng chờ? Câu trả lời '
      + 'vào <b>nhật ký</b> và vào <b>bộ đếm tuần</b>.</div>'
      + '<div class="note warn" style="margin-bottom:0">⚠ Đây là thước của '
      + '<span class="mono">US-045</span>: <b>4 tuần không ai gõ = cổng đã '
      + 'chết</b>. ⛔ Gõ bừa một chữ làm hỏng đúng cái thước ấy.</div>'
      + '<input class="inp" id="o-ly-do" style="max-width:none;margin-top:9px" '
      + 'placeholder="vì sao dòng này chưa xong…">',
      [['Thôi', null],
       ['Ghi lý do', async function () {
         const v = (TP.$('#o-ly-do').value || '').trim();
         if (!v) { TP.$('#o-ly-do').focus(); return false; }
         try {
           await FLS.ghi('/queue/' + r.itl_id + '/reason', { reason: v });
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ve();
       }, { pri: true }]]);
  }

  /* ══ ④ HOÃN ══════════════════════════════════════════════════════════ */
  function _hoan(r) {
    const lan = Number(r.defer_count || 0);
    HT.mo('Hoãn · dòng ' + r.itl_id,
      '<div class="note">Hoãn <b>CÓ HẠN</b>: đến ngày ấy dòng quay lại hàng '
      + 'chờ. ⛔ Không phải cách để bỏ qua một dòng.</div>'
      + (lan >= 2
         ? '<div class="note crit">⚠ Dòng này đã hoãn <b>' + lan + ' lần</b>. '
           + 'Lần thứ ba <b>đổi màu</b> để nhìn thấy — và ⛔ <b>không báo cho '
           + 'ai</b>, vì ⛔ không có vai nào nhận báo '
           + '(<span class="mono">QĐ-ITL-27</span>).</div>'
         : '')
      + '<div class="fld" style="border:0"><div>Hoãn đến ngày</div>'
      + '<div><input class="inp" id="o-den" type="date"></div></div>'
      + '<input class="inp" id="o-vi-sao" style="max-width:none;margin-top:9px" '
      + 'placeholder="vì sao hoãn — BẮT BUỘC…">',
      [['Thôi', null],
       ['Hoãn', async function () {
         const d = (TP.$('#o-den').value || '').trim();
         if (!d) { TP.$('#o-den').focus(); return false; }
         const v = (TP.$('#o-vi-sao').value || '').trim();
         if (!v) { TP.$('#o-vi-sao').focus(); return false; }
         try {
           await FLS.ghi('/queue/' + r.itl_id + '/defer',
                         { until: d, reason: v });
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ve();
       }, { pri: true }]]);
  }

  /* ══ ⑤ DRAWER GHÉP ════════════════════════════════════════════════════ */
  const BAC = {
    ma:            ['ok',   'mã khớp'],
    tien:          ['info', 'tiền khớp'],
    gan_tien:      ['warn', 'gần tiền'],
    cung_tien_te:  ['lock', 'cùng tiền tệ']
  };

  function _tuoi_anh(a) {
    if (!a || !a.doc_luc_muon_nhat) return '⛔ không biết tuổi ảnh chụp';
    return 'ảnh chụp ' + TP.so(a.so_dong) + ' dòng lệnh · đọc lúc '
         + String(a.doc_luc_muon_nhat).slice(0, 16);
  }

  async function _drawer_ghep(r) {
    let d;
    try {
      d = (await FLS.doc('/queue/' + r.itl_id + '/pm-candidates')).data;
    } catch (e) {
      return HT.mo('Ghép lệnh · dòng ' + r.itl_id,
        '<div class="note crit"><b>' + TP.chu(e.cau) + '</b><br>'
        + TP.chu(e.lam_gi) + '</div>', [['Đóng', null]]);
    }
    /* ⭐⭐ `WO-022` §5b ⓕ: tien bank · Σ · lech · dung sai tinh tren SO
       NGUYEN XU *(`TP.xu`)*, ⛔ `Number` cong thang. Do 02/10: Σ `0.10 +
       0.20` tru bank `0.30` ra `5,55·10⁻¹⁷` ⇒ voi dung sai ngoai te **0**
       *(`QĐ-ITL-62`)* hop **khoa nut Ghep** tren mot chum khop dung tung
       xu. ⛔ `data-a` van mang CHUOI CUA *(ⓖ — ⛔ chuoi da in)*. */
    const cur = d.dong_so.curr;
    const bank = d.dong_so.tien;
    const bank_xu = TP.xu(bank);
    const uv = d.ung_vien || [];

    const hang = uv.map((u, i) =>
      '<tr><td><input type="checkbox" data-i="' + i + '" data-a="'
      + TP.chu(u.amount) + '"></td>'
      + '<td class="mono">' + TP.chu(u.pm_line_id) + '</td>'
      + '<td>' + TP.chip(BAC[u.bac] ? BAC[u.bac][0] : 'lock',
                         BAC[u.bac] ? BAC[u.bac][1] : u.bac) + '</td>'
      + '<td class="r">' + TP.tien(u.amount, u.curr) + '</td>'
      + '<td>' + TP.chu(u.status || '—') + '</td>'
      + '<td>' + (Number(u.da_ghep) > 0
                  ? TP.chip('warn', 'đã ghép nơi khác') : '') + '</td></tr>'
    ).join('');

    HT.mo('Ghép lệnh · dòng ' + r.itl_id,
      '<div class="note" style="margin-top:0"><b>Dòng tiền (ghim):</b> '
      + '<span class="num">' + TP.tien(bank, cur) + '</span> '
      + TP.chu(d.dong_so.curr) + ' — ' + TP.chu((r.memo || '').slice(0, 70))
      + '</div>'
      /* ⭐ TUỔI ảnh chụp — số này là **bản sao**, ⛔ không phải sổ sống. */
      + '<div class="hint">' + TP.chu(_tuoi_anh(d.anh_chup)) + '</div>'
      /* ⭐⭐ Máy KHAI RA hai trục nó ⛔ không xếp được — ⛔ không im lặng để
         người dùng tưởng nó đã cân nhắc ngày và người nhận. */
      + ((d.khong_xep_duoc_theo || []).length
         ? '<div class="note warn">⛔ <b>Máy ⛔ không xếp được theo: '
           + TP.chu((d.khong_xep_duoc_theo || []).join(', ')) + '</b><br>'
           + TP.chu(d.vi_sao) + '</div>' : '')
      + (uv.length
         ? '<table><thead><tr><th></th><th>Dòng lệnh</th><th>Độ khớp</th>'
           + '<th class="r">Tiền lệnh</th><th>Trạng thái</th><th></th></tr>'
           + '</thead><tbody>' + hang + '</tbody></table>'
         : '<div class="note crit">⛔ <b>⛔ Không có ứng viên nào.</b> Ảnh chụp '
           + 'dòng lệnh ⛔ không có dòng nào cùng tiền tệ với dòng này.</div>')
      /* ⭐⭐ `WO-032` (g) *(`QĐ-ITL-149 ⓑ` — owner 01/10: *"bỏ yêu cầu lý do
         cho cú Ghép"*; `BA-07 §4h ⓼`)*: ô **tuỳ ý**; trống ⇒ thân ⛔ mang
         `reason`, tầng repo `ghep_lenh` ghi `LY_DO_MAC_DINH_GHEP` có nhãn
         `(may dien)`. */
      + '<input class="inp" id="o-vi-sao" style="max-width:none;margin-top:9px" '
      + 'placeholder="vì sao ghép cặp này — tuỳ ý — bỏ trống thì máy ghi lý do '
      + 'mặc định…">'
      + '<div class="note" id="sig" style="margin-bottom:0"></div>',
      [['Thôi', null],
       ['Ghép', async function () {
         /* ⚠ `WO-032` `AC-8`: `#dlg-b input` + lọc `type`/`checked` *(⛔ bộ
            chọn `:checked`)* — cùng tập trên trình duyệt, và DOM giả của bộ
            thử đọc được *(như `_tinh` bên dưới đã làm từ `WO-022`)* ⇒ bài DOM
            bấm được **nút thật** để đếm lượt `POST`. */
         const ck = [...document.querySelectorAll('#dlg-b input')]
           .filter(c => c.type === 'checkbox' && c.checked);
         const ma = ck.map(c => uv[Number(c.dataset.i)].pm_line_id);
         // ⛔ Sửa `WO-032` (g): chú thích cũ *"Cửa ĐÒI `reason` (`_chu` bắt
         //   buộc)"* già hơn `WO-003` — từ `BA-07` v3.4 `§4h ⓼` cửa `match` nhận
         //   `reason` **tuỳ ý** *(`xu_ly.ghep` `_chu(…, bat_buoc=False)`)*, thiếu
         //   thì tầng repo điền lý do mặc định `(may dien) …` ⇒ vết ⛔ rỗng.
         //   Nút ⛔ còn chặn khi ô trống *(trước: `if (!v) … return false`)*.
         const v = (TP.$('#o-vi-sao').value || '').trim();
         const than = { pm_line_ids: ma };
         if (v) than.reason = v;
         try {
           const kq = await FLS.ghi('/queue/' + r.itl_id + '/match', than);
           ST.moi_noi.set(r.itl_id, ma.length);
           _bao_ghep(r, kq.data);
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ve();
       }, { pri: true }]]);

    /* ── Σ ba con số, tính lại mỗi lần tích ─────────────────────────────
       ⛔⛔ Nút mờ + **câu giải thích hiện sẵn**, ⛔ không giấu trong tooltip:
       người dùng phải biết **vì sao** ⛔ không bấm được, ⛔ không phải đoán. */
    const ds = d.dung_sai;
    // ⚠ Dung sai doi xu bang SAN *(`TP.xu` che do `'san'`)*: `|lech| <= ds`
    //   ⇔ `|lech_xu| <= san(ds × 100)`. Lam tron len thi man cho ghep mot
    //   lech ma cua ghi tu choi *(`617.285` → `61729`)*.
    const ds_xu = TP.xu(ds, 'san');
    /* ⭐⭐ `WO-022` vong 2 *(`BA-06` v4.13 §5b ⓕ — yeu #4 cua `BG-027`)*: con
       so in canh mot phep so **la** con so da dem so. ⛔ Vong 1 in
       `TP.tien(ds, cur)` *(lam tron nua ra xa: `"617.285"` → `617,29`)* canh
       phep so `61728` xu ⇒ nguoi doc *"lech 617,29 · dung sai 617,29 · ⛔
       lech qua dung sai"*. Tam: dong tien VND dung sai `0,5% × tien` co chu
       so le thu ba **250 / 4.242** *(`TL-026`)*. ⛔ Doi duoc sang xu ⇒ in
       chuoi cua tra *(`TP.tien` in nguyen van da thoat)* — va `_tinh` ⛔ cho
       ghep *(`hong`)*. */
    const ds_in = ds_xu === null ? TP.tien(ds, cur)
                                 : TP.tien(TP.chuoi_xu(ds_xu), cur);
    function _tinh() {
      /* ⚠ Doc o tich qua `#dlg-b input` + loc `type`/`checked` *(⛔ bo chon
         `:checked`)*: cung mot tap tren trinh duyet, va DOM gia cua bo
         thu doc duoc *(`WO-022` `AC-4` — bai DOM bam that).* */
      const ck = [...document.querySelectorAll('#dlg-b input')]
        .filter(c => c.type === 'checkbox' && c.checked);
      const tung = ck.map(c => TP.xu(c.dataset.a));
      const sig = TP.$('#sig');
      if (!sig) return;
      /* ⛔ Mot so ⛔ doi duoc sang xu *(⛔ phai so · vuot thang)* ⇒ ⛔ tinh
         duoc ⇒ ⛔ cho ghep, va NOI ra — ⛔ coi la 0. */
      const hong = bank_xu === null || ds_xu === null
                   || tung.some(x => x === null);
      const tong = hong ? null : tung.reduce((s, x) => s + x, 0);
      const lech = hong ? null : tong - bank_xu;
      const ok = !hong && ck.length > 0 && Math.abs(lech) <= ds_xu;
      sig.className = 'note ' + (ok ? 'ok' : 'crit');
      sig.innerHTML =
        'Σ dòng lệnh <b class="num">'
        + (hong ? '⛔ không tính được' : TP.tien(TP.chuoi_xu(tong), cur))
        + '</b> · tiền bank '
        + '<b class="num">' + TP.tien(bank, cur) + '</b> · lệch '
        + '<b class="num">'
        + (hong ? '—' : TP.tien(TP.chuoi_xu(lech), cur)) + '</b> · dung sai '
        + '<b class="num">' + ds_in + '</b><br>'
        + (ok
           ? TP.chip('ok', 'khớp — cho ghép')
           : TP.chip('crit', '⛔ lệch quá dung sai')
             + ' <span class="muted">Máy sẽ trả <b>422</b> và <b>GIỮ chưa '
             + 'gán</b> — ⛔ không chia bừa phần lệch cho các dòng lệnh '
             + '(<span class="mono">INV-I16</span>).</span>');
      const b = [...document.querySelectorAll('#dlg-f button')].pop();
      if (b) b.disabled = !ok;
    }
    /* ⭐ Nghe tren `#dlg-b` *(su kien `change` noi bot tu o tich)* bang
       `onchange` — GAN DE, ⛔ `addEventListener`: `#dlg-b` song qua moi hop,
       cong don nguoi nghe thi `_tinh` cua hop CU chay lai trong hop moi. */
    const than_hop = TP.$('#dlg-b');
    if (than_hop) than_hop.onchange = _tinh;
    _tinh();
  }

  /* ⭐⭐ Sau khi ghép: nếu máy ⛔ KHÔNG suy được `hd`/`cdt1` thì PHẢI nói.
     ⛔ Im lặng ở đây làm kế toán đọc một phép ghép thành công thành *"đã điền
     xong"*, rồi dòng đó nằm im với ô trống. */
  function _bao_ghep(r, k) {
    const kd = k.khong_suy_duoc || [];
    if (!kd.length) return;
    setTimeout(() => HT.mo('Đã ghép · nhưng máy ⛔ KHÔNG tự điền được',
      '<div class="note warn" style="margin-top:0">⛔ <b>Các dòng lệnh nói '
      + 'nhiều giá trị khác nhau</b> cho: <b>'
      + TP.chu(kd.map(x => x.truong || x).join(', ')) + '</b><br>'
      + 'Máy ⛔ <b>không tự chọn</b> — chọn thay người là máy quyết định thay '
      + 'người (<span class="mono">INV-I16</span>).</div>'
      + '<div class="note">⇒ Mở màn <b>Sổ ITL</b> và gõ tay ô ấy.</div>',
      [['Đã hiểu', null, { pri: true }]]), 60);
  }

  /* ══ ⑥ BỎ GHÉP ═══════════════════════════════════════════════════════ */
  function _bo_ghep(r) {
    HT.mo('Bỏ ghép · dòng ' + r.itl_id,
      '<div class="note warn" style="margin-top:0">⚠ <b>Bỏ CẢ CHÙM mối nối, '
      + '⛔ không bỏ lẻ.</b> Bỏ lẻ làm <b>Σ mối nối ≠ tiền bank</b>, tức tạo ra '
      + 'đúng cái trạng thái sai mà cổng dựng ra để bắt.</div>'
      + '<div class="note ok">⭐ <b>Sổ ⛔ không mất gì.</b> Bỏ mối nối là '
      + '<b>THÊM một dòng</b>; lịch sử mọi lần ghép vẫn đọc lại được, và ghép '
      + 'lại được — kể cả đúng dòng lệnh vừa gỡ (sẽ là <i>lần 2</i>).</div>'
      /* ⭐⭐ `WO-032` (g) *(`QĐ-ITL-149 ⓑ` · `BA-07 §4h ⓼` — `reason` tuỳ ý cho
         **cả** `match` lẫn `unmatch`)*: trống ⇒ thân `{}`, tầng repo
         `bo_moi_noi` ghi `LY_DO_MAC_DINH_BO_GHEP` `(may dien) …`. */
      + '<input class="inp" id="o-vi-sao" style="max-width:none" '
      + 'placeholder="vì sao bỏ — tuỳ ý — bỏ trống thì máy ghi lý do mặc định…">',
      [['Thôi', null],
       ['Bỏ cả chùm', async function () {
         const v = (TP.$('#o-vi-sao').value || '').trim();
         const than = {};
         if (v) than.reason = v;
         let kq;
         try {
           kq = await FLS.ghi('/queue/' + r.itl_id + '/unmatch', than);
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ST.moi_noi.delete(r.itl_id);
         _bao_bo_ghep(kq.data);
         ve();
       }, { danger: true, pri: true }]]);
  }

  /* ⭐⭐ `bo_qua` = thứ máy **⛔ KHÔNG rút lại** vì NGƯỜI đã gõ tay lên ô ấy.
     Nó **phải hiện**: nếu giấu, kế toán tưởng bỏ ghép đã dọn sạch mọi thứ. */
  /* ⭐⭐ `WO-008` *(`BA-06` v4.8, `KQ-007 F-2`/`F-3`)*:

     ⓐ Câu đảo nói theo **Ô**, ⛔ theo bút toán. Từ `WO-003` vòng 2 bỏ ghép đảo
       **mọi lớp** gợi ý ⇒ `but_toan_dao` mang nhiều bút toán **cùng ô**. Bản
       cũ in `dao.map(field).join(', ')` ⇒ dòng B của `KQ-007` *(2 ô)* ra
       *"cdt1, hd, hd, cdt1"* — người đọc đếm được **4 ô**. Nay: mỗi tên ô
       **một lần**, theo thứ tự xuất hiện **đầu tiên**; số bút toán chỉ nói
       khi nó **lớn hơn** số ô *(tức có lớp cũ bị đè)*.
     ⓑ Hàm này là **bản câu DUY NHẤT** của hộp *"Đã bỏ ghép"*: màn ghép
       *(`man_f01_ghep.js::bo_gan`)* gọi lại **chính** nó khi `bo_qua` ⛔ rỗng
       *(`WO-008` Rủi ro 2 — chép câu sang tệp kia là đẻ bản thứ hai sẽ già
       lệch)*. ⇒ Đổi câu ở ĐÂY là đổi cho cả hai màn.
     ⓒ Khối `bo_qua` in thêm **giá trị người** bên cạnh tên ô *(`hd =
       HD-K7B`)* — `WO-008 AC-4` đòi hộp "chứa `hd` và `HD-K7B`"; câu cảnh báo
       giữ nguyên *(`HOI-016`, ⛔ chặn)*. */
  function _o_duy_nhat(ds) {
    const ra = [];
    ds.forEach(function (x) {
      const f = x.truong || x.field || x;
      if (!ra.includes(f)) ra.push(f);
    });
    return ra;
  }

  function _bao_bo_ghep(k) {
    const dao = k.but_toan_dao || [];
    const bo = k.bo_qua || [];
    const o = _o_duy_nhat(dao);
    setTimeout(() => HT.mo('Đã bỏ ghép',
      '<div class="note ok" style="margin-top:0">Đã bỏ <b>'
      + TP.so((k.da_bo || []).length) + '</b> mối nối. Sổ giữ nguyên lịch sử.'
      + (k.ve_hang_cho ? ' Dòng <b>quay về hàng chờ</b>.' : '') + '</div>'
      + (dao.length
         ? '<div class="note">↩ <b>Đã rút gợi ý máy trên ' + o.length
           + ' ô</b> (<span class="mono">' + TP.chu(o.join(', '))
           + '</span>)'
           + (dao.length > o.length
              ? ' · ' + dao.length + ' bút toán, gồm lớp gợi ý cũ bị đè' : '')
           + '</div>' : '')
      + (bo.length
         ? '<div class="note warn" style="margin-bottom:0">⚠ <b>⛔ KHÔNG đảo '
           + bo.length + ' ô</b> — <b>người</b> đã gõ tay lên đó sau khi ghép: '
           + '<span class="mono">'
           + TP.chu(bo.map(x => (x.truong || x.field || x)
                    + (x.value_after != null ? ' = ' + x.value_after : ''))
                      .join(', '))
           + '</span><br>Máy ⛔ không rút lại thứ người đã quyết.</div>'
         : ''),
      [['Đã hiểu', null, { pri: true }]]), 60);
  }

  /* ══ ⑦ XONG ══════════════════════════════════════════════════════════ */
  function _xong(r) {
    HT.mo('Xong · dòng ' + r.itl_id,
      '<div class="note" style="margin-top:0">Đánh dấu dòng này <b>đã xong</b> '
      + '⇒ nó rời hàng chờ. ⛔ <b>Không cần lý do</b> '
      + '(<span class="mono">QĐ-ITL-72</span>).</div>'
      + '<div class="note">⭐ Bấm nhầm thì <b>Mở lại</b> — mở lại là <b>THÊM '
      + 'một sự kiện</b>, ⛔ không xoá gì.</div>',
      [['Thôi', null],
       ['Xong', async function () {
         let kq;
         try {
           kq = await FLS.ghi('/queue/' + r.itl_id + '/done', {});
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ST.vua_xong.set(r.itl_id, kq.data);
         _bao_xong(kq.data);
         ve();
       }, { pri: true }]]);
  }

  /* ⛔⛔ Ba thứ máy trả về mà màn hình **PHẢI nói ra**:
       `da_co`         — ai đã bấm trước, lúc nào (⛔ không báo lỗi)
       `thieu_truong`  — xong MÀ CÒN THIẾU: ⛔ không chặn, nhưng ⛔ không im lặng
       `ky_da_chot`    — kỳ chốt vẫn bấm xong được, cố ý khác `INV-I13` */
  function _bao_xong(k) {
    const thieu = k.thieu_truong || [];
    if (!k.da_co && !thieu.length && !k.ky_da_chot) return;
    setTimeout(() => HT.mo('Đã ghi',
      (k.da_co
        ? '<div class="note" style="margin-top:0">⭐ Dòng này <b>đã được bấm '
          + 'xong từ trước</b> — bởi <b>' + TP.chu(k.boi) + '</b> lúc '
          + TP.chu(String(k.luc || '').slice(0, 16))
          + '. Bấm lại ⛔ không tạo thêm sự kiện.</div>' : '')
      + (thieu.length
         ? '<div class="note warn">⚠ <b>Xong mà còn thiếu: <span class="mono">'
           + TP.chu(thieu.join(', ')) + '</span></b><br>⛔ Máy ⛔ không chặn — '
           + 'nhưng nó <b>đếm riêng</b> những dòng như thế, để nút này ⛔ không '
           + 'thành đường tắt làm sạch hàng chờ.</div>' : '')
      + (k.ky_da_chot
         ? '<div class="note">⭐ <b>Kỳ đã chốt</b> — vẫn bấm xong được, và đó '
           + 'là <b>cố ý</b>: kỳ chốt thì ⛔ không sửa được giá trị nào, nếu '
           + 'cũng ⛔ không đánh dấu xong được thì hàng chờ <b>tự biến thành '
           + 'rác</b>.</div>' : ''),
      [['Đã hiểu', null, { pri: true }]]), 60);
  }

  /* ══ ⑧ MỞ LẠI — lý do BẮT BUỘC ═══════════════════════════════════════ */
  function _mo_lai(r) {
    HT.mo('Mở lại · dòng ' + r.itl_id,
      '<div class="note warn" style="margin-top:0">⚠ <b>Lý do BẮT BUỘC</b> ở '
      + 'đây — khác nút <i>Xong</i>. Dòng này đã có <b>người</b> kết luận là '
      + 'xong; kéo lại là <b>lật kết luận của người khác</b>.</div>'
      + '<input class="inp" id="o-vi-sao" style="max-width:none" '
      + 'placeholder="vì sao mở lại…">',
      [['Thôi', null],
       ['Mở lại', async function () {
         const v = (TP.$('#o-vi-sao').value || '').trim();
         if (!v) { TP.$('#o-vi-sao').focus(); return false; }
         try {
           await FLS.ghi('/queue/' + r.itl_id + '/reopen', { reason: v });
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ST.vua_xong.delete(r.itl_id);
         ve();
       }, { pri: true }]]);
  }

  /* ══ ⑧b GHÉP CẢ LÔ — chỉ dòng TỰ CHỨNG (`B2`, `QĐ-ITL-118`) ══════════
     ⛔⛔ **Khối này PHẢI nói ra con số nhỏ, ⛔ không chỉ con số đẹp.**

     Bản lộ trình `13` §0 ⓵ ghi *"**584** dòng tự chứng ⇒ cửa ghép lô dọn được
     8,0%"*. Phép đo `B0` nói con số ấy là **68 (0,9%)** — nhỏ hơn **8,6 lần**:
     con số cũ đo bằng luật của **danh sách ứng viên**, ⛔ không bằng luật của
     **cửa GHI**. ⇒ Một màn hình chỉ hiện *"68 dòng ghép được"* mà ⛔ không
     hiện *"652 dòng CÓ mã mà 584 bị từ chối vì sao"* sẽ làm người dùng tưởng
     phần còn lại là **⛔ không có việc gì** — trong khi nút thắt thật
     *(**6.577** dòng thiếu dữ liệu lệnh chi)* nằm đúng ở phần bị ẩn.

     ⭐ Nên khối này vẽ **ba thứ cùng lúc**: bấm được bao nhiêu · bị từ chối vì
     bốn cổng nào · và phần việc ⛔ **không** thuộc cửa này.                */
  function _ve_lo(data, meta, o) {
    const tc = data.tu_chung || [];
    const vs = data.vi_sao || {};
    const nut = TP.el('div', 'ctl');
    nut.style.borderRadius = 'var(--bo-the)';
    nut.style.border = '1px solid var(--line)';
    nut.innerHTML =
      '<strong style="font-size:12.5px">Ghép cả lô · chỉ dòng TỰ CHỨNG</strong>'
      + '<span class="muted" style="font-size:12px">máy đo lại phía máy chủ ⇒ '
      + 'nút này ⛔ không gửi dòng lệnh nào</span>';
    const b = TP.el('button', 'b pri',
                    'Ghép ' + TP.so(tc.length) + ' dòng tự chứng');
    b.id = 'lo-nut-ghep';
    if (!tc.length) {
      b.disabled = true;
      b.title = '⛔ ⛔ Không dòng nào tự chứng ⇒ ⛔ không có gì để bấm.';
    } else if (!_chan_ghi(b)) {
      b.onclick = () => _hoi_ghep_lo(tc);
    }
    nut.appendChild(TP.el('span', 'spacer'));
    nut.appendChild(b);
    o.appendChild(nut);

    /* ⛔⛔ Bảng TỪ CHỐI. Bốn lý do ⇒ **bốn đường sửa khác nhau**, nên gộp
       chúng thành một con số *"584 dòng ⛔ không tự chứng"* là bỏ đi đúng phần
       thông tin người đọc cần để đi tiếp. */
    const kh = data.khong || [];
    if (kh.length) {
      const dem = {};
      const cau = {};
      kh.forEach(x => {
        dem[x.ly_do] = (dem[x.ly_do] || 0) + 1;
        cau[x.ly_do] = x.cau;
      });
      const t = TP.el('table');
      t.innerHTML =
        '<thead><tr><th>Dòng CÓ mã mà ⛔ không tự chứng</th>'
        + '<th class="r">Số dòng</th><th>Vì sao — và sửa ở đâu</th></tr>'
        + '</thead><tbody>'
        + Object.keys(dem).sort((a, c) => dem[c] - dem[a]).map(k =>
            '<tr><td class="mono">' + TP.chu(k) + '</td>'
            + '<td class="r"><b>' + TP.so(dem[k]) + '</b></td>'
            + '<td class="muted" style="font-size:12px">'
            + TP.chu(cau[k] || '') + '</td></tr>').join('')
        + '</tbody>';
      o.appendChild(t);
    }

    /* ⭐⭐ Và phần việc ⛔ KHÔNG thuộc cửa này — nói thẳng, ⛔ không ẩn. */
    const g = TP.el('div', 'note warn');
    g.id = 'lo-ghi-chu-nut-that';
    g.innerHTML =
      '⚠ <b>Cửa này ⛔ không phải đòn chính.</b> Trong <b>'
      + TP.so(data.so_dong_xet || 0) + '</b> dòng chưa nối, nó chỉ dọn được '
      + '<b>' + TP.so(tc.length) + '</b>. Nút thắt thật là <b>'
      + TP.so(vs.PM_khong_mang_ma_nay || 0) + ' dòng có mã chuẩn hoá được mà '
      + '⛔ KHÔNG một dòng lệnh chi nào mang mã ấy</b> — tức thiếu <b>dữ liệu '
      + 'lệnh chi</b>, ⛔ không phải thiếu mã và ⛔ không phải thiếu giao diện. '
      + 'Nạp lệnh chi cho mới là việc của mốc <span class="mono">A3</span>.';
    o.appendChild(g);
  }

  function _hoi_ghep_lo(tc) {
    const ids = tc.map(x => x.itl_id);
    const n_noi = tc.reduce((s, x) => s + (x.pm_line_ids || []).length, 0);
    HT.mo('Ghép cả lô · ' + ids.length + ' dòng',
      '<div class="note" style="margin-top:0">Máy sẽ ghép <b>' + ids.length
      + ' dòng</b> thành <b>' + n_noi + ' mối nối</b>. Mỗi dòng đều có đúng '
      + 'một chùm lệnh chi cùng mã tham chiếu, cùng tiền tệ, đã duyệt, và '
      + '<b>Σ đúng bằng tiền bank</b> ⇒ ⛔ máy ⛔ không chọn hộ ai điều gì.</div>'
      + '<div class="note warn">⚠ <b>Một dòng ⛔ không đạt ⇒ CẢ LÔ bị từ chối</b> '
      + 'và ⛔ không một mối nối nào được ghi. ⛔ Không có chế độ “ghép được bao '
      + 'nhiêu thì ghép”.</div>'
      + '<input class="inp" id="o-ly-do-lo" style="max-width:none" '
      + 'placeholder="lý do (bắt buộc — nó vào nhật ký từng dòng)…">',
      [['Thôi', null],
       ['Ghép cả lô', async function () {
         const v = (TP.$('#o-ly-do-lo').value || '').trim();
         if (!v) { TP.$('#o-ly-do-lo').focus(); return false; }
         let kq;
         try {
           kq = await FLS.ghi('/queue/match-lo',
                              { itl_ids: ids, reason: v });
         } catch (e) { HT.loi_trong_hop(e); return false; }
         _bao_ghep_lo(kq.data);
         ve();
       }, { pri: true }]]);
  }

  function _bao_ghep_lo(k) {
    setTimeout(() => HT.mo('Đã ghép cả lô',
      '<div class="note" style="margin-top:0">✓ <b>' + TP.so(k.so_dong_da_ghep)
      + ' dòng</b> · <b>' + TP.so(k.so_moi_noi) + ' mối nối</b>. '
      + 'Mỗi dòng có một sự kiện riêng trong nhật ký ⇒ bỏ ghép được từng dòng.'
      + '</div>'
      + '<div class="note">⭐ Những dòng này rời hàng chờ <b>⛔ không phải</b> '
      + 'vì ai bấm “xong” — nhãn <span class="mono">work_status</span> bị '
      + '<b>đóng băng lúc nạp</b> (<span class="mono">INV-I08</span>) nên nó '
      + 'vẫn nói <span class="mono">UNMAPPED</span>. Đó ⛔ không phải lỗi: '
      + 'nhãn trả lời <i>phân loại</i>, mối nối trả lời <i>đã nối lệnh chi</i> '
      + '— <b>hai câu hỏi khác nhau</b>.</div>',
      [['Đã hiểu', null, { pri: true }]]), 60);
  }

  function ve_lo(o) {
    return TT.chay(o, () => FLS.doc('/queue/tu-chung'), _ve_lo, {
      so_dong: 3,
      /* ⛔ ⛔ KHÔNG coi "0 dòng tự chứng" là RỖNG: khối vẫn phải vẽ, vì đúng
         lúc ấy nó mới cần nói *"việc nằm ở chỗ khác"*. Rỗng chỉ khi cửa
         ⛔ không trả về gì cả. */
      la_rong: d => !d || d.so_dong_xet === undefined,
      rong: {
        icon: '⛔',
        tieu_de: 'Máy ⛔ không đo được tập tự chứng',
        cau: 'Cửa <span class="mono">GET /queue/tu-chung</span> ⛔ không trả '
           + 'lời. Báo người dựng hệ — ⛔ đừng ghép tay bù cho nó.'
      }
    });
  }

  /* ══ ⑨ THANH LỌC + VẼ CẢ MÀN ═════════════════════════════════════════ */
  function _thanh_loc(o) {
    const w = TP.el('div', 'ctl');
    w.style.borderRadius = 'var(--bo-the)';
    w.style.border = '1px solid var(--line)';
    w.innerHTML = '<strong style="font-size:12.5px">Chỉ xem tới mức phủ</strong>';
    const seg = TP.el('span', 'seg');
    [['', 'tất cả'], ['50', '50%'], ['80', '80%'], ['90', '90%']]
      .forEach(function (x) {
        const b = TP.el('button', null, x[1]);
        b.setAttribute('aria-pressed', ST.den_pct === x[0] ? 'true' : 'false');
        b.onclick = () => { ST.den_pct = x[0]; ve(); };
        seg.appendChild(b);
      });
    w.appendChild(seg);
    if (!CO_GHI()) {
      w.insertAdjacentHTML('beforeend',
        '<span class="spacer"></span>'
        + TP.chip('warn', '⛔ cửa đang CHỈ ĐỌC — mọi nút ghi đều mờ',
                  'Khởi động máy chủ với --cho-ghi để mở. Nó sửa SỔ THẬT.'));
    }
    o.appendChild(w);
  }

  /* ══ ⭐⭐⭐ THANH CHUYỂN LẰN (`GAP-SCR-14`) ═══════════════════════════

     ⛔⛔⛔ **Vì sao có hai lằn, và vì sao lằn LỆNH CHI là mặc định.**

     Chủ sổ chốt chiều đo ngày 09/09 (`QĐ-ITL-122`): *"Trans map vào PM. Số
     lượng Trans vốn nhiều hơn PM; không cần question các Trans không được
     map."*

     ⇒ Lằn cũ — **theo dòng tiền** — đang hỏi **7.682** dòng, tức đúng cái câu
     chủ sổ vừa nói là ⛔ **không cần hỏi**. Lằn mới — **theo lệnh chi** —
     hỏi **1.345** dòng, và chỉ **69** dòng trong đó phủ **90% tiền**.

     ⛔ **Nhưng lằn cũ ⛔ KHÔNG bị xoá**, và đó là chủ ý: nó vẫn là đường duy
     nhất để **ghi lý do**, **hoãn**, **bỏ ghép** và **bấm xong** trên một
     dòng tiền cụ thể — bốn việc ⛔ không có mặt ở phía lệnh chi. Xoá nó là
     cắt bốn hành động mà `QĐ-ITL-71`/`72` đã chốt. */
  function _thanh_lan(o) {
    const t = TP.el('div', 'tabs sub');
    /* ⭐ `WO-045` ⑤ *(`BA-06` v4.20 `§4.5 ⓦ` ③, `KQ-046 F-3`)*: `title` ⛔
       mang số đo cứng. Bản trước in *"1.345 dòng lệnh…"* — số đo **09/09**
       gõ vào mã *(sổ thật 05/10 `/lenh-cho/ro` `tong` **1.601**, và ⛔ cùng
       định nghĩa)*; cỡ của việc đã có **ở chính lằn** *(băng `F01L` đọc
       `/ro` mỗi lần vẽ)*. Chuỗi **nguyên văn** spec phương án ⓐ. Chú thích
       bia phía trên *(`7.682` · `1.345` · `69`)* **giữ** — biên bản (`Đ2`). */
    [['lenh', 'Theo LỆNH CHI', 'Lệnh chi đang chờ tiền — câu hỏi của việc '
                               + '(QĐ-ITL-122)'],
     ['tien', 'Theo dòng tiền', 'lằn cũ — nơi ghi lý do · hoãn · bỏ ghép · '
                                + 'bấm xong']
    ].forEach(function (x) {
      const b = TP.el('button', 'b' + (ST.lan === x[0] ? ' pri' : ''), x[1]);
      b.title = x[2];
      b.onclick = function () { ST.lan = x[0]; ve_man(); };
      t.appendChild(b);
    });
    o.appendChild(t);
  }

  /* ⭐ Cửa vào của màn: vẽ thanh lằn rồi giao thân cho đúng một lằn. */
  function ve_man() {
    const g = TP.$('#than-f01');
    if (!g) return;
    g.textContent = '';
    _thanh_lan(g);
    const sub = TP.el('div', 'stack');
    g.appendChild(sub);
    if (ST.lan === 'lenh') { F01L.ve(sub); return; }
    _than_tien = sub;
    ve(sub);
  }

  function ve(_o) {
    const o = _o || _than_tien || TP.$('#than-f01');
    if (!o) return;
    _than_tien = o;
    _luot_luoi++;   /* ⭐ `WO-045`: lưới cũ rời cây ⇒ lượt của nó bị thay */
    o.textContent = '';
    const tom = TP.el('div');
    o.appendChild(tom);
    ve_tom(tom);
    /* ⭐ Khối ghép LÔ nằm TRÊN phần chọn tiền tệ, và ⛔ **không** bị lọc theo
       tiền tệ: tập tự chứng là tập của cả sổ. Đặt nó dưới ô chọn tiền tệ thì
       nó sẽ hiện một con số của cả sổ ngay cạnh một bảng của một tiền tệ —
       hai phạm vi khác nhau đứng cạnh nhau mà ⛔ không nhãn nào nói. */
    const lo = TP.el('div', 'card');
    o.appendChild(lo);
    ve_lo(lo);
    if (!ST.curr) {
      const n = TP.el('div', 'note');
      n.innerHTML = '⇧ <b>Chọn một tiền tệ</b> để xem hàng chờ. ⛔ Màn này '
        + '⛔ không gộp các tiền tệ lại — xem lý do ở trên.';
      o.appendChild(n);
      return;
    }
    _thanh_loc(o);
    const luoi = TP.el('div', 'card');
    o.appendChild(luoi);
    ve_luoi(luoi);
  }

  /* ⭐ `ve_tom` · `_drawer_ghep` mở ra cho bài thử `WO-022` *(`AC-4`/`AC-6`)*
     soi thẳng hộp ghép nhiều dòng — DOM giả ⛔ dựng được lưới *(bảng đi qua
     `innerHTML`)* nên ⛔ có đường bấm `Ghép` từ một dòng. */
  return { ve, ve_man, ST, ve_lo, _o_hoan, _bao_xong, _bao_bo_ghep,
           _bao_ghep_lo, ve_tom, _drawer_ghep,
           /* ⭐ `WO-032` `AC-8` — bài DOM mở **đúng** hộp thật để đếm lượt
              `FLS.ghi` khi ô lý do trống *(Bỏ cả chùm tuỳ ý · Hoãn + Mở lại
              GIỮ bắt buộc)*, ⛔ đi vòng qua cả một lưới. */
           _bo_ghep, _hoan, _mo_lai };
})();
