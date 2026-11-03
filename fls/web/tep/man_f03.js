/* ═══════════════════════════════════════════════════════════════════════
   man_f03.js — man **Cong hom nay**.

   ⚠ O `B2` day moi la **bo xuong**: no goi DUNG MOT cua that (`GET /gates`) va
   ve ba muc do cua mot cong. Phan con lai cua `F03` *(do phu hang cho theo tien
   te · nut xuat bao cao tuan)* la viec cua `B3`.
   ⇒ Cai `B2` phai chung minh la: **mot vong tron** — vo → goi cua that → bon
     trang thai deu ve duoc.

   ⭐⭐ **O quan trong nhat cua ca man nay la o `dat = null`.** No ⛔ khong duoc
   trong giong DAT. Mot cong xanh vi **⛔ khong do gi** nguy hon mot cong do —
   do la luat so mot cua du an, va o day no la mot lop CSS (`.gate.unk`).
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F03 = (function () {

  /* Ba muc do — ⛔ BA, ⛔ khong phai hai. */
  function _muc(dat) {
    if (dat === true)  return { lop: 'pass', chu: '✓ ĐẠT' };
    if (dat === false) return { lop: 'fail', chu: '✗ KHÔNG ĐẠT' };
    return { lop: 'unk', chu: '— ⛔ KHÔNG ĐO ĐƯỢC' };
  }

  function _the_cong(c) {
    const m = _muc(c.dat);
    const d = TP.el('div', 'gate ' + m.lop);
    d.innerHTML =
      '<div class="k">' + TP.chu(c.ten || c.ma) + '</div>' +
      '<div class="st">' + m.chu + '</div>' +
      '<div class="muted" style="font-size:12px">' +
        (c.nhan ? TP.chu(c.nhan) : '') +
        (c.da_do ? ' <span class="mono">' + TP.chu(c.da_do) + '</span>' : '') +
        (c.ly_do ? '<div style="margin-top:3px">' + TP.chu(c.ly_do) + '</div>'
                 : '') +
      '</div>';
    return d;
  }

  function _ve(data, meta, o) {
    const luoi = TP.el('div', 'grid4');
    (data.cong || []).forEach(c => luoi.appendChild(_the_cong(c)));
    o.appendChild(luoi);

    /* ⛔⛔ Dong tom PHAI noi ca ba con so. Mot man noi "2/2 xanh" trong khi
       bon cong khac chua he do la mot con so noi doi (`xu_ly.cong`). */
    const tom = TP.el('div', 'note');
    const chua = Number(data.chua_do_duoc || 0);
    tom.innerHTML =
      TP.chip('ok', data.dat + ' đạt') + ' ' +
      TP.chip('crit', data.khong_dat + ' không đạt') + ' ' +
      TP.chip('lock', chua + ' ⛔ chưa đo được') +
      (chua > 0
        ? '<div style="margin-top:7px">⭐ <b>' + chua + ' cổng chưa từng đo '
        + 'được.</b> Đó ⛔ không phải “đạt” — cổng chưa từng thấy đỏ là cổng '
        + 'chưa biết có sống.</div>'
        : '');
    o.appendChild(tom);

    if (meta && meta.data_status) {
      const c = TP.el('div', 'hint');
      c.innerHTML = 'Độ tin của số trên màn: ' +
                    TP.chip_niem_tin(meta.data_status) +
                    (meta.pham_vi ? ' <span class="muted">· phạm vi '
                      + TP.chu(meta.pham_vi) + '</span>' : '');
      o.appendChild(c);
    }
  }

  function ve_cong(o) {
    return TT.chay(o,
      () => FLS.doc('/gates'),
      _ve,
      {
        so_dong: 4,
        la_rong: d => !d || !d.cong || d.cong.length === 0,
        rong: {
          icon: '⛔',
          tieu_de: 'Máy không khai một cổng nào',
          cau: 'Đây ⛔ không phải tin tốt — nó nghĩa là ⛔ không có gì đang '
             + 'canh sổ. Báo người dựng hệ.'
        }
      });
  }

  /* ══ ĐỘ PHỦ HÀNG CHỜ THEO TIỀN TỆ ═══════════════════════════════════════
     ⛔⛔ **⛔ Không có dòng "tổng".** Cộng hai đơn vị tiền tệ ra một con số là
     đúng cái sai đã đẻ ra con số *"310 dòng phủ 90% tiền"* (thật ra **799**).
     Bảng này để **mỗi tiền tệ một dòng**, và ⛔ không có hàng cuối cùng.     */

  /* ⭐⭐ Ô "⛔ KHÔNG ĐO ĐƯỢC" — cùng luật với cổng `dat = null`.
     `so_dong_phu = null` nghĩa là Σ tiền của tiền tệ đó bằng 0, nên câu hỏi
     *"xem bao nhiêu dòng thì qua N% tiền"* ⛔ không có nghĩa. ⛔ Vẽ `0` ở đây
     là nói *"xem 0 dòng là đủ"* — một câu **sai mà nghe như tin tốt**. */
  function _o_phu(r, muc) {
    if (r.so_dong_phu === null || r.so_dong_phu === undefined) {
      return '<td class="r"><span class="chip lock" title="Σ tiền của tiền tệ '
           + 'này bằng 0 nên câu hỏi ⛔ không có nghĩa">— ⛔ không đo được'
           + '</span></td>';
    }
    const lech = (r.so_dong_trong_danh_sach !== null
                  && r.so_dong_trong_danh_sach !== r.so_dong_phu)
      ? ' <span class="faint" title="Danh sách hàng chờ lọc theo luỹ kế ≤ '
        + TP.chu(muc) + '% nên hiện ' + TP.so(r.so_dong_trong_danh_sach)
        + ' dòng. Cột này trả lời câu khác: bao nhiêu dòng thì ĐỦ CHẠM '
        + TP.chu(muc) + '%.">(danh sách hiện '
        + TP.so(r.so_dong_trong_danh_sach) + ')</span>'
      : '';
    return '<td class="r"><b>' + TP.so(r.so_dong_phu) + '</b> dòng'
         + ' <span class="muted">⇒ ' + TP.chu(r.pct_that) + '%</span>'
         + lech + '</td>';
  }

  function _ve_phu(data, meta, o) {
    const hang = data.theo_tien_te || [];
    const muc = data.muc_pct;
    const b = TP.el('table');
    b.innerHTML =
      '<thead><tr><th>Tiền tệ</th><th class="r">Dòng chờ</th>' +
      '<th class="r">% tổng dòng</th><th class="r">Σ tiền chờ</th>' +
      '<th class="r">Xem tới đây thì qua ' + TP.chu(muc) +
      '% tiền</th></tr></thead><tbody>' +
      hang.map(r =>
        '<tr><td>' + TP.chu(r.curr || '(⛔ chưa có đơn vị tiền)') + '</td>' +
        '<td class="r">' + TP.so(r.so_dong_cho) + '</td>' +
        '<td class="r">' + TP.chu(r.pct_dong) + '%</td>' +
        '<td class="r">' + TP.tien(r.tien_cho) + '</td>' +
        _o_phu(r, muc) + '</tr>'
      ).join('') + '</tbody>';
    o.appendChild(b);

    const g = TP.el('div', 'note');
    g.innerHTML =
      '⭐ <b>⛔ Không có dòng “tổng”</b>. Cộng hai đơn vị tiền tệ ra một con số '
      + 'là vô nghĩa, và chính cái sai đó từng đẻ ra con số <i>“310 dòng phủ '
      + '90% tiền”</i> khi thật ra cần <b>799</b>. '
      + 'Cột cuối đọc là: <i>xem bao nhiêu dòng đầu thì đã nhìn qua '
      + TP.chu(muc) + '% số tiền đang chờ</i>, kèm <b>phần trăm thật</b> tại '
      + 'dòng đó ⇒ nhãn ⛔ không thể nói quá.';
    o.appendChild(g);
  }

  function ve_phu(o) {
    return TT.chay(o,
      () => FLS.doc('/queue/coverage'),
      _ve_phu,
      {
        so_dong: 4,
        la_rong: d => !d || !d.theo_tien_te || d.theo_tien_te.length === 0,
        rong: {
          icon: '✓',
          tieu_de: 'Hàng chờ rỗng',
          cau: 'Đây là màn đẹp nhất của cả hệ: ⛔ không còn dòng nào chờ ai '
             + 'trả lời.'
        }
      });
  }

  function ve(o_cong, o_phu) {
    // ⛔ Hai cửa gọi ĐỘC LẬP: một cửa hỏng ⛔ không được kéo cả màn xuống. Mỗi
    // khối tự mang bốn trạng thái của nó.
    return Promise.all([ve_cong(o_cong), ve_phu(o_phu)]);
  }

  return { ve, ve_cong, ve_phu, _muc, _o_phu };
})();
