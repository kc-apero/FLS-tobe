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
               vua_xong: new Map(), moi_noi: new Map(), het: false };

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
        TP.tien(r.tien) + '</div></div>';
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
      '<td class="r">' + TP.tien(r.tien) + '</td>' +
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
    const b = TP.el('table');
    b.innerHTML =
      '<thead><tr><th class="r">Hạng</th><th>Mã dòng</th><th>Số chứng từ</th>' +
      '<th>Diễn giải</th><th class="r">Tiền</th><th class="r">% luỹ kế</th>' +
      '<th>Pháp nhân</th><th>Việc</th></tr></thead><tbody></tbody>';
    const tb = b.querySelector('tbody');
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
      b2.onclick = () => _xem_them(o);
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

  async function _xem_them(o) {
    try {
      const kq = await FLS.doc('/queue', {
        curr: ST.curr, den_pct: ST.den_pct, cursor: ST.con_tro, limit: 50 });
      const them = kq.data.rows || [];
      ST.dong = ST.dong.concat(them);
      ST.con_tro = kq.data.next_cursor || null;
      o.textContent = '';
      _ve_luoi({ rows: ST.dong, next_cursor: ST.con_tro }, kq.meta, o);
    } catch (e) {
      TT.loi(o, e, () => ve_luoi(o));
    }
  }

  function ve_luoi(o) {
    return TT.chay(o,
      () => FLS.doc('/queue', { curr: ST.curr, den_pct: ST.den_pct,
                                limit: 50 }),
      _ve_luoi,
      {
        so_dong: 8,
        la_rong: d => !d || !(d.rows || []).length,
        rong: { icon: '✓', tieu_de: 'Không còn dòng nào ở mức lọc này',
                cau: 'Đổi tiền tệ hay bỏ mức phủ để xem tiếp.' }
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
    const bank = Number(d.dong_so.tien);
    const uv = d.ung_vien || [];

    const hang = uv.map((u, i) =>
      '<tr><td><input type="checkbox" data-i="' + i + '" data-a="'
      + TP.chu(u.amount) + '"></td>'
      + '<td class="mono">' + TP.chu(u.pm_line_id) + '</td>'
      + '<td>' + TP.chip(BAC[u.bac] ? BAC[u.bac][0] : 'lock',
                         BAC[u.bac] ? BAC[u.bac][1] : u.bac) + '</td>'
      + '<td class="r">' + TP.tien(u.amount) + '</td>'
      + '<td>' + TP.chu(u.status || '—') + '</td>'
      + '<td>' + (Number(u.da_ghep) > 0
                  ? TP.chip('warn', 'đã ghép nơi khác') : '') + '</td></tr>'
    ).join('');

    HT.mo('Ghép lệnh · dòng ' + r.itl_id,
      '<div class="note" style="margin-top:0"><b>Dòng tiền (ghim):</b> '
      + '<span class="num">' + TP.tien(bank) + '</span> '
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
      + '<input class="inp" id="o-vi-sao" style="max-width:none;margin-top:9px" '
      + 'placeholder="vì sao ghép cặp này — BẮT BUỘC, vào nhật ký…">'
      + '<div class="note" id="sig" style="margin-bottom:0"></div>',
      [['Thôi', null],
       ['Ghép', async function () {
         const ck = [...document.querySelectorAll(
           '#dlg-b input[type=checkbox]:checked')];
         const ma = ck.map(c => uv[Number(c.dataset.i)].pm_line_id);
         // ⛔ Cửa ĐÒI `reason` (`_chu` bắt buộc). ⚠ `BA-06` §8 ⛔ không nói —
         // đây là chỗ đặc tả lệch code, đã ghi `GAP-SPEC-02`.
         const v = (TP.$('#o-vi-sao').value || '').trim();
         if (!v) { TP.$('#o-vi-sao').focus(); return false; }
         try {
           const kq = await FLS.ghi('/queue/' + r.itl_id + '/match',
                                    { pm_line_ids: ma, reason: v });
           ST.moi_noi.set(r.itl_id, ma.length);
           _bao_ghep(r, kq.data);
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ve();
       }, { pri: true }]]);

    /* ── Σ ba con số, tính lại mỗi lần tích ─────────────────────────────
       ⛔⛔ Nút mờ + **câu giải thích hiện sẵn**, ⛔ không giấu trong tooltip:
       người dùng phải biết **vì sao** ⛔ không bấm được, ⛔ không phải đoán. */
    const ds = Number(d.dung_sai);
    function _tinh() {
      const ck = [...document.querySelectorAll(
        '#dlg-b input[type=checkbox]:checked')];
      const tong = ck.reduce((s, c) => s + Number(c.dataset.a), 0);
      const lech = tong - bank;
      const ok = ck.length > 0 && Math.abs(lech) <= ds;
      const sig = TP.$('#sig');
      sig.className = 'note ' + (ok ? 'ok' : 'crit');
      sig.innerHTML =
        'Σ dòng lệnh <b class="num">' + TP.tien(tong) + '</b> · tiền bank '
        + '<b class="num">' + TP.tien(bank) + '</b> · lệch '
        + '<b class="num">' + TP.tien(lech) + '</b> · dung sai '
        + '<b class="num">' + TP.tien(ds) + '</b><br>'
        + (ok
           ? TP.chip('ok', 'khớp — cho ghép')
           : TP.chip('crit', '⛔ lệch quá dung sai')
             + ' <span class="muted">Máy sẽ trả <b>422</b> và <b>GIỮ chưa '
             + 'gán</b> — ⛔ không chia bừa phần lệch cho các dòng lệnh '
             + '(<span class="mono">INV-I16</span>).</span>');
      const b = [...document.querySelectorAll('#dlg-f button')].pop();
      if (b) b.disabled = !ok;
    }
    document.querySelectorAll('#dlg-b input[type=checkbox]')
      .forEach(c => c.addEventListener('change', _tinh));
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
      + '<input class="inp" id="o-vi-sao" style="max-width:none" '
      + 'placeholder="vì sao bỏ — BẮT BUỘC…">',
      [['Thôi', null],
       ['Bỏ cả chùm', async function () {
         const v = (TP.$('#o-vi-sao').value || '').trim();
         if (!v) { TP.$('#o-vi-sao').focus(); return false; }
         let kq;
         try {
           kq = await FLS.ghi('/queue/' + r.itl_id + '/unmatch',
                              { reason: v });
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ST.moi_noi.delete(r.itl_id);
         _bao_bo_ghep(kq.data);
         ve();
       }, { danger: true, pri: true }]]);
  }

  /* ⭐⭐ `bo_qua` = thứ máy **⛔ KHÔNG rút lại** vì NGƯỜI đã gõ tay lên ô ấy.
     Nó **phải hiện**: nếu giấu, kế toán tưởng bỏ ghép đã dọn sạch mọi thứ. */
  function _bao_bo_ghep(k) {
    const dao = k.but_toan_dao || [];
    const bo = k.bo_qua || [];
    setTimeout(() => HT.mo('Đã bỏ ghép',
      '<div class="note ok" style="margin-top:0">Đã bỏ <b>'
      + TP.so((k.da_bo || []).length) + '</b> mối nối. Sổ giữ nguyên lịch sử.'
      + (k.ve_hang_cho ? ' Dòng <b>quay về hàng chờ</b>.' : '') + '</div>'
      + (dao.length
         ? '<div class="note">↩ <b>Đã đảo ' + dao.length + ' bút toán</b> mà '
           + 'chính phép ghép suy ra: <span class="mono">'
           + TP.chu(dao.map(x => x.truong || x.field || x).join(', '))
           + '</span></div>' : '')
      + (bo.length
         ? '<div class="note warn" style="margin-bottom:0">⚠ <b>⛔ KHÔNG đảo '
           + bo.length + ' ô</b> — <b>người</b> đã gõ tay lên đó sau khi ghép: '
           + '<span class="mono">'
           + TP.chu(bo.map(x => x.truong || x.field || x).join(', '))
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

  function ve() {
    const o = TP.$('#than-f01');
    if (!o) return;
    o.textContent = '';
    const tom = TP.el('div');
    o.appendChild(tom);
    ve_tom(tom);
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

  return { ve, ST, _o_hoan, _bao_xong, _bao_bo_ghep };
})();
