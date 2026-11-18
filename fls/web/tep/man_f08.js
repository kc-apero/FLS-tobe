/* ═══════════════════════════════════════════════════════════════════════
   man_f08.js — màn **Cấu hình** (`SCR-F08`, ISP 3.1.2 Step 18 · `F4`).

   ⭐ Mới có MỘT vùng: bảng tỷ giá `IX.FX` **CHỈ ĐỌC** từ `GET /config/fx`.
   ⛔ KHÔNG có nút nào: vùng ký tháng (`F5`) và ký Daily Report 3 (`F7`) là việc
   của bước sau — `06_SCREEN_SPEC.md` §9 ⓑ giữ chỗ, ⛔ không đoán trước.

   ⛔⛔ Ba nhãn bất thường lấy THẲNG từ ba mảng của cửa (`thieu[]` · `trung[]` ·
   `lac[]`) — màn ⛔ tự suy tháng nào thiếu/lạc (spec §9: "màn **đọc**, ⛔ tự
   suy"). Tháng THIẾU không có hàng trong `ky[]` ⇒ màn vẽ một hàng riêng cho
   nó, để tháng mất **⛔ biến mất im lặng** (`AP §3.2.4`: thiếu tháng ⇒ SUMIFS = 0
   ⇒ mất số không báo). Tháng TRÙNG: ⛔ không cộng, ⛔ không chọn hộ một dòng —
   hiện CẢ HAI hàng, mỗi hàng một nhãn.
   ⛔ Màu chỉ qua lớp `chip ok|warn|crit` (token ở `tokens.css`) — ⛔ hex gõ tay.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F08 = (function () {

  const TIEN_TE = ['USD', 'SGD', 'COP', 'VND', 'HKD'];

  /* Ba nhãn — mỗi nhãn một lớp chip có sẵn, ⛔ màu riêng. */
  const NHAN = {
    CHAN: { lop: 'crit', chu: 'CHẶN',
            ghi: 'Thiếu tháng này trong bảng tỷ giá ⇒ SUMIFS = 0 ⇒ mất số '
               + 'không báo.' },
    TRUNG: { lop: 'warn', chu: 'TRÙNG',
             ghi: 'Hai dòng cùng một tháng ⇒ cộng đôi. Màn ⛔ cộng và ⛔ chọn '
                + 'hộ một dòng.' },
    LAC: { lop: 'warn', chu: 'LẠC',
           ghi: 'Tháng nằm ngoài dải 202401…202612.' }
  };

  /* ⭐ Dựng bằng `createElement`, ⛔ chuỗi HTML: nhãn phải là NÚT DOM riêng để
     bài (và đọc màn) đếm được từng nhãn. */
  function _chip(k) {
    const n = NHAN[k];
    const c = document.createElement('span');
    c.className = 'chip nhan-fx ' + n.lop;
    c.title = n.ghi;
    c.textContent = n.chu;
    return c;
  }

  function _tap(a) { return new Set((a || []).map(String)); }

  function _o(chu, lop) {
    const td = document.createElement('td');
    if (lop) td.className = lop;
    td.textContent = chu;
    return td;
  }

  function _hang(thang, ky, nhan) {
    const tr = document.createElement('tr');
    tr.dataset.thang = String(thang);
    tr.appendChild(_o(String(thang), 'mono'));
    TIEN_TE.forEach(te => tr.appendChild(_o(ky ? String(TP.so(ky[te])) : '—', 'r')));
    const tt = document.createElement('td');
    nhan.forEach(k => { tt.appendChild(_chip(k)); });
    tr.appendChild(tt);
    return tr;
  }

  function _ve(data, meta, o) {
    const thieu = _tap(data.thieu), trung = _tap(data.trung), lac = _tap(data.lac);
    const hang = [];
    (data.ky || []).forEach(k => hang.push({ thang: String(k.yyyymm), ky: k }));
    thieu.forEach(t => hang.push({ thang: t, ky: null }));
    // `sort` ổn định ⇒ hai dòng trùng một tháng giữ thứ tự của cửa.
    hang.sort((a, b) => a.thang < b.thang ? -1 : a.thang > b.thang ? 1 : 0);

    const b = TP.el('table');
    b.innerHTML =
      '<thead><tr><th>Tháng</th>' +
      TIEN_TE.map(te => '<th class="r">' + te + '</th>').join('') +
      '<th>Trạng thái</th></tr></thead>';
    const tb = document.createElement('tbody');
    hang.forEach(h => {
      const nhan = [];
      if (!h.ky) nhan.push('CHAN');
      if (trung.has(h.thang)) nhan.push('TRUNG');
      if (lac.has(h.thang)) nhan.push('LAC');
      tb.appendChild(_hang(h.thang, h.ky, nhan));
    });
    b.appendChild(tb);
    // F4-R1-01 (`KQ-162`): bảng 7 cột rộng 474 px > màn 390 px ⇒ trang tràn ngang.
    // Bọc trong `.ngang` (hinh.css:504, có sẵn) ⇒ cuộn TRONG khung, ⛔ cả trang.
    const kn = TP.el('div', 'ngang');
    kn.appendChild(b);
    o.appendChild(kn);

    const tom = TP.el('div', 'note');
    tom.innerHTML =
      TP.chip('ok', hang.length + ' dòng') + ' ' +
      TP.chip(thieu.size ? 'crit' : 'lock', thieu.size + ' CHẶN') + ' ' +
      TP.chip(trung.size ? 'warn' : 'lock', trung.size + ' TRÙNG') + ' ' +
      TP.chip(lac.size ? 'warn' : 'lock', lac.size + ' LẠC') +
      '<div class="muted" style="margin-top:6px">Bảng chỉ đọc — ký tháng '
      + 'tỷ giá <b>chưa xây</b> (bước sau).</div>';
    o.appendChild(tom);

    if (meta && meta.data_status) {
      const c = TP.el('div', 'hint');
      c.innerHTML = 'Độ tin của số trên màn: ' +
                    TP.chip_niem_tin(meta.data_status);
      o.appendChild(c);
    }
  }

  function ve(o) {
    return TT.chay(o, () => FLS.doc('/config/fx'), _ve, {
      so_dong: 6,
      la_rong: d => !d || !d.ky || (d.ky.length === 0
                                   && (d.thieu || []).length === 0),
      rong: {
        icon: '⛔',
        tieu_de: 'Bảng tỷ giá ⛔ có dòng nào',
        cau: 'Đây ⛔ không phải tin tốt — nghĩa là cửa trả bảng rỗng.'
      }
    });
  }

  return { ve };
})();
