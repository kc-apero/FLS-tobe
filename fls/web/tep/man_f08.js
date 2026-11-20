/* ═══════════════════════════════════════════════════════════════════════
   man_f08.js — màn **Cấu hình** (`SCR-F08`, ISP 3.1.2 Step 18 · `F4`).

   ⭐ Bảng tỷ giá `IX.FX` đọc từ `GET /config/fx` (`F4`) + ⭐ **nút `Ký tháng`**
   (ISP 3.1.2 Step 37 · `F5`, `WO-253`): bấm ⇒ HỘP XÁC NHẬN (`hop_thoai.js`, ⛔ hộp
   mới) nêu tháng + số sắp niêm phong ⇒ xác nhận ⇒ `POST /config/fx/{yyyymm}/sign`
   ⇒ vẽ lại: dòng hiện 'đã ký · người ký · ngày', nút khoá. ⛔ Thân POST RỖNG: người
   ký lấy TỪ THẺ ở cửa (`C7` — gửi `actor` là 400). ⛔ Huỷ ký, ⛔ phân quyền theo vai
   (`O11`). Ký Daily Report 3 (`F7`) vẫn là việc của bước sau.
   ⛔ Nút chỉ ở dòng SẠCH (có số, ⛔ TRÙNG, ⛔ LẠC): ký một tháng trùng/lạc là niêm
   phong một số mà màn chính nó đang gắn cờ.

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

  /* ⭐ Ngày ký = 10 ký tự đầu của `ky_luc` (ISO do MÁY đặt) — ⛔ tự đổi múi giờ. */
  function _ngay(ky_luc) { return String(ky_luc || '').slice(0, 10); }

  function _ky_o(ky, nhan, ve_lai) {
    const td = document.createElement('td');
    td.className = 'o-ky';
    if (!ky) return td;
    const da = ky.trang_thai === 'da_ky';
    if (da) {
      const c = document.createElement('span');
      c.className = 'da-ky';
      c.textContent = 'đã ký · ' + (ky.actor || '?') + ' · ' + _ngay(ky.ky_luc);
      td.appendChild(c);
    } else if (nhan.length) {
      return td;                         // TRÙNG/LẠC ⇒ ⛔ nút (xem đầu tệp)
    }
    const b = document.createElement('button');
    b.className = 'b nut-ky';
    b.type = 'button';
    b.textContent = 'Ký tháng';
    b.dataset.ky = String(ky.yyyymm);   // ⛔ `data-thang`: bài F4 đếm dòng theo nó
    b.disabled = da;                     // sau ký: nút KHOÁ, ⛔ ký lại từ màn
    if (!da) b.onclick = () => _hoi_ky(ky, ve_lai);
    td.appendChild(b);
    return td;
  }

  /* ⭐ Hộp xác nhận nói CÁI SẼ XẢY RA (`hop_thoai.js`: câu chữ là lớp giải thích cuối).
     Nút chính ⛔ là mặc định của bàn phím (hộp tự lo). Lỗi cửa ⇒ chữ tiếng Việt
     TRONG hộp (`loi_trong_hop`, qua `goi_cua.js`), hộp ở nguyên (`return false`). */
  function _hoi_ky(ky, ve_lai) {
    const t = String(ky.yyyymm);
    const so = TIEN_TE.map(te => te + ' <b>' + TP.chu(TP.so(ky[te])) + '</b>').join(' · ');
    HT.mo('Ký tháng tỷ giá ' + t,
      '<p>Ký <b>' + TP.chu(t) + '</b> là niêm phong tỷ giá của tháng này: ' + so + '.</p>'
      + '<p>Số tháng này đổi sau khi ký thì phải ký lại bằng số mới; màn ⛔ có nút huỷ ký. '
      + 'Người ký lấy từ thẻ đăng nhập của anh/chị.</p>',
      [['Huỷ', null],
       ['Ký tháng ' + t, async function () {
          try {
            // ⛔ `actor` trong thân: người ký do cửa lấy TỪ THẺ (C7).
            await FLS.ghi('/config/fx/' + t + '/sign', {});
          } catch (e) {
            HT.loi_trong_hop(e);
            // F5-R1-02 (`KQ-255`): `409` = NGƯỜI KHÁC đã ký giữa chừng ⇒ màn sau lưng
            // hộp còn nói 'chưa ký'. Tải lại từ cửa (chữ lỗi trong hộp giữ nguyên).
            if (e && e.http === 409) ve_lai(t);
            return false;
          }
          ve_lai(t);
          return true;
        }, { pri: true }]]);
  }

  function _hang(thang, ky, nhan, ve_lai) {
    const tr = document.createElement('tr');
    tr.dataset.thang = String(thang);
    tr.appendChild(_o(String(thang), 'mono'));
    TIEN_TE.forEach(te => tr.appendChild(_o(ky ? String(TP.so(ky[te])) : '—', 'r')));
    const tt = document.createElement('td');
    nhan.forEach(k => { tt.appendChild(_chip(k)); });
    tr.appendChild(tt);
    tr.appendChild(_ky_o(ky, nhan, ve_lai));
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
      '<th>Trạng thái</th><th>Ký</th></tr></thead>';
    const tb = document.createElement('tbody');
    hang.forEach(h => {
      const nhan = [];
      if (!h.ky) nhan.push('CHAN');
      if (trung.has(h.thang)) nhan.push('TRUNG');
      if (lac.has(h.thang)) nhan.push('LAC');
      tb.appendChild(_hang(h.thang, h.ky, nhan, t => _ve_lai(o, t)));
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
      '<div class="muted" style="margin-top:6px">Ký tháng tỷ giá: bấm <b>Ký tháng</b> '
      + 'ở dòng chưa ký, xác nhận trong hộp. Ký xong ⛔ huỷ được.</div>';
    o.appendChild(tom);

    if (meta && meta.data_status) {
      const c = TP.el('div', 'hint');
      c.innerHTML = 'Độ tin của số trên màn: ' +
                    TP.chip_niem_tin(meta.data_status);
      o.appendChild(c);
    }
  }

  /* ⭐ F5-R1-01 (`KQ-255`): `TT.chay` xoá ô rồi vẽ khung chờ ⇒ trang co lại ⇒ cuộn về
     đầu, dòng vừa ký ra khỏi khung nhìn (đo: `scrollY` 554 → 0). Nhớ `scrollY`, vẽ xong
     thì trả lại; rồi đưa TIÊU ĐIỂM về dòng vừa ký (nút của nó đã khoá nên ⛔ nhận
     tiêu điểm ⇒ lấy chính `tr`). Hộp còn mở (ca `409`) ⇒ ⛔ giật tiêu điểm khỏi hộp. */
  async function _ve_lai(o, thang) {
    const y = window.scrollY;
    await ve(o);
    window.scrollTo(0, y);
    const s = document.getElementById('scrim');
    if (s && s.classList.contains('on')) return;
    const tr = o.querySelector('tr[data-thang="' + String(thang) + '"]');
    if (tr) { tr.tabIndex = -1; tr.focus({ preventScroll: true }); }
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
