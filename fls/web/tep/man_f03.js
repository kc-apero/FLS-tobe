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
        '<td class="r">' + TP.tien(r.tien_cho, r.curr) + '</td>' +
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

  /* ══ MẪU SỐ của tác vụ ① (`B0`, `QĐ-ITL-118`) ═══════════════════════════
     ⛔⛔ **Vì sao bảng này phải ở đây, cạnh “độ phủ hàng chờ”.**

     Mọi tỷ lệ độ phủ từ 27/08 đến 09/09 đều chia cho **10.030** — cả sổ. Phép
     đo `B0` nói: dòng ghép được **dồn hẳn** về vế `PS Có` *(31,1% so với
     7,8%)* ⇒ đó là **vế của lệnh chi**, và mẫu số thật là **8.246**. Một con
     số đúng chia cho một mẫu số sai là một con số **⛔ không ai kiểm được**,
     nên màn phải hiện **cả hai vế** chứ ⛔ không hiện một tỷ lệ gộp.

     ⭐ Và cột `⛔ chưa nối` ⛔ **không** cùng nghĩa với `UNMAPPED`: nhãn trả
     lời *phân loại*, mối nối trả lời *đã nối lệnh chi*. **Hai câu hỏi khác
     nhau** — và chính chỗ lẫn hai câu ấy đã đẻ ra con số *"lệch 353"*, một
     con số **HIỆU** che đi **1.203** dòng ngược chiều.                       */
  function _ve_mau_so(data, meta, o) {
    const ve = (data.ve || []).filter(r => r.so_dong > 0);
    const b = TP.el('table');
    b.innerHTML =
      '<thead><tr><th>Vế của sổ</th><th class="r">Dòng</th>' +
      '<th class="r">Đã nối lệnh chi</th><th class="r">⛔ Chưa nối</th>' +
      '<th class="r">Độ phủ</th></tr></thead><tbody>' +
      ve.map(r =>
        '<tr><td class="mono">' + TP.chu(r.ve) + '</td>' +
        '<td class="r">' + TP.so(r.so_dong) + '</td>' +
        '<td class="r">' + TP.so(r.da_noi) + '</td>' +
        '<td class="r">' + TP.so(r.chua_noi) + '</td>' +
        '<td class="r"><b>' + TP.chu(r.ty_le_noi_pct) + '%</b></td></tr>'
      ).join('') + '</tbody>';
    o.appendChild(b);

    /* ⭐⭐ Bốn ô của bảng chéo — **mỗi ô một TÊN**, ⛔ không ô nào tên "khác".
       Một ô ⛔ không có tên là một ô ⛔ không ai giải thích được, và nó sẽ được
       đọc thành *"lỗi"* trong lần đọc lại đầu tiên. */
    const L = data.lech || {};
    const n = TP.el('div', 'note');
    n.id = 'ms-lech';
    n.innerHTML =
      '⭐ <b>Hai câu <i>“chưa ghép”</i> ⛔ KHÔNG phải một câu.</b> '
      + '<b>' + TP.so(L.da_noi__nhan_con_UNMAPPED || 0) + '</b> dòng đã nối mà '
      + 'nhãn còn <span class="mono">UNMAPPED</span> '
      + '<span class="muted">(nhãn bị đóng băng lúc nạp — '
      + '<span class="mono">INV-I08</span>)</span>, và <b>'
      + TP.so(L.du_phan_loai__chua_noi || 0) + '</b> dòng đủ phân loại mà '
      + 'chưa nối. Hiệu của chúng là <b>'
      + TP.so(L.hieu_hai_phep_dem || 0) + '</b> — một con số <b>che đi '
      + TP.so(L.tong_dong_bi_che || 0) + ' dòng</b> ngược chiều. '
      + '⛔ Đừng theo dõi cái hiệu ấy.';
    o.appendChild(n);

    const vs = (data.vi_sao || []).filter(r => r.so_dong > 0);
    if (vs.length) {
      const t = TP.el('table');
      t.innerHTML =
        '<thead><tr><th>Vì sao ⛔ chưa nối được</th><th class="r">Cả sổ</th>' +
        '<th class="r">Vế <span class="mono">PS Có</span></th></tr></thead>' +
        '<tbody>' + vs.map(r =>
          '<tr><td class="mono" title="' + TP.chu(r.ly_do) + '">' +
          TP.chu(r.ma) + '</td><td class="r">' + TP.so(r.so_dong) +
          '</td><td class="r">' + TP.so(r.so_dong_ps_co) + '</td></tr>'
        ).join('') + '</tbody>';
      o.appendChild(t);
    }

    const g = TP.el('div', 'hint');
    g.id = 'ms-tu-chung';
    g.innerHTML =
      'Cửa ghép lô nhận ngay <b>' + TP.so(data.tu_chung || 0) + '</b> dòng '
      + '<span class="muted">(màn <b>Hàng chờ</b>)</span> — đó là số của '
      + '<b>cửa GHI</b>, ⛔ không phải của danh sách ứng viên. Hai luật ấy từng '
      + 'lệch <b>8,6 lần</b>.';
    o.appendChild(g);
  }

  function ve_mau_so(o) {
    return TT.chay(o, () => FLS.doc('/queue/mau-so'), _ve_mau_so, {
      so_dong: 4,
      la_rong: d => !d || !d.tong_dong,
      rong: {
        icon: '⛔',
        tieu_de: 'Sổ ⛔ không có dòng nào trong phạm vi lần nạp thật',
        cau: 'Đây ⛔ không phải tin tốt — nó nghĩa là ⛔ chưa nạp gì. '
           + 'Mở màn <b>Nạp sao kê</b>.'
      }
    });
  }

  function ve(o_cong, o_phu) {
    // ⛔ Hai cửa gọi ĐỘC LẬP: một cửa hỏng ⛔ không được kéo cả màn xuống. Mỗi
    // khối tự mang bốn trạng thái của nó.
    // ⛔ Ba cửa gọi ĐỘC LẬP: một cửa hỏng ⛔ không được kéo cả màn xuống.
    const o_ms = TP.$('#than-mau-so');
    return Promise.all([ve_cong(o_cong), ve_phu(o_phu)]
      .concat(o_ms ? [ve_mau_so(o_ms)] : []));
  }

  return { ve, ve_cong, ve_phu, ve_mau_so, _muc, _o_phu };
})();
