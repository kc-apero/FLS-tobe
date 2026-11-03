/* ═══════════════════════════════════════════════════════════════════════
   hop_thoai.js — hộp xác nhận + drawer. Dùng chung cho `F01` và `F02`.

   ⛔⛔ **Một hộp xác nhận ở đây ⛔ KHÔNG phải một cái phanh cho vui.** Sau
   `QĐ-ITL-27` ⛔ không còn vai hậu kiểm, nên **câu chữ trong hộp là lớp giải
   thích cuối cùng** trước khi một dòng đi vào sổ vĩnh viễn. ⇒ Hộp phải nói
   **cái gì sắp xảy ra**, ⛔ không phải *"bạn có chắc không?"*.

   ★ Ba luật, và cả ba đều đến từ một quyết định đã ghi:
     ⓐ Nút chính **⛔ không bao giờ là nút mặc định của bàn phím** khi thao tác
       ⛔ không lùi được — người ta gõ `Enter` theo quán tính.
     ⓑ Hàm xác nhận trả `false` ⇒ hộp **ở nguyên**. Nhờ vậy ô lý do bắt buộc
       *(`Mở lại` — `QĐ-ITL-71`)* ⛔ không thể bị bỏ qua bằng cách bấm nhanh.
     ⓒ `Esc` và bấm ra ngoài **đóng hộp**, và đóng hộp luôn là **⛔ KHÔNG làm
       gì** — ⛔ không có đường nào ra khỏi hộp mà lại ghi vào sổ.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const HT = (function () {

  let dang_mo = null;      // {đóng}

  function _khung() {
    let s = document.getElementById('scrim');
    if (!s) {
      s = TP.el('div', 'scrim');
      s.id = 'scrim';
      s.innerHTML = '<div class="dlg" role="dialog" aria-modal="true">'
        + '<header id="dlg-t"></header>'
        + '<div class="body" id="dlg-b"></div>'
        + '<div class="foot" id="dlg-f"></div></div>';
      document.body.appendChild(s);
      s.addEventListener('click', e => { if (e.target === s) dong(); });
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && dang_mo) dong();
      });
    }
    return s;
  }

  function dong() {
    const s = document.getElementById('scrim');
    if (s) s.classList.remove('on');
    dang_mo = null;
  }

  /* `nut` = [[nhãn, hàm|null, {pri, danger}], …]
     Hàm trả `false` ⇒ ⛔ KHÔNG đóng (ô bắt buộc còn trống).
     Hàm trả Promise ⇒ nút khoá lại trong lúc chờ, ⛔ không bấm được hai lần. */
  function mo(tieu_de, than, nut) {
    const s = _khung();
    TP.$('#dlg-t').textContent = tieu_de;
    TP.$('#dlg-b').innerHTML = than;
    const f = TP.$('#dlg-f');
    f.textContent = '';
    nut.forEach(function (n) {
      const [nhan, ham, tuy] = [n[0], n[1], n[2] || {}];
      const b = TP.el('button', 'b' + (tuy.pri ? ' pri' : '')
                                   + (tuy.danger ? ' danger' : ''), nhan);
      b.onclick = async function () {
        if (!ham) return dong();
        // ⛔ Khoá cả hàng nút: bấm hai lần là hai bút toán, và sổ ⛔ không xoá
        // được cái thứ hai.
        [...f.children].forEach(x => { x.disabled = true; });
        let ra;
        try {
          ra = await ham();
        } finally {
          [...f.children].forEach(x => { x.disabled = false; });
        }
        if (ra !== false) dong();
      };
      f.appendChild(b);
    });
    s.classList.add('on');
    dang_mo = { dong };
    // ⛔ Đưa con trỏ vào ô nhập ĐẦU TIÊN nếu có — ⛔ không vào nút, để `Enter`
    // theo quán tính ⛔ không kích hoạt một thao tác không lùi được.
    const o = TP.$('#dlg-b input, #dlg-b textarea');
    if (o) o.focus();
    return { dong };
  }

  /* Khối lỗi trong hộp — dùng khi cửa trả `409`/`422` giữa chừng. */
  function loi_trong_hop(e) {
    const o = TP.$('#dlg-b');
    if (!o) return;
    const d = TP.el('div', 'note crit');
    d.innerHTML = '<b>' + TP.chu(e.cau || e.message) + '</b>'
      + (e.lam_gi ? '<br>' + TP.chu(e.lam_gi) : '')
      + (e.chi_tiet ? '<div class="mono" style="font-size:11px;margin-top:5px">'
                    + TP.chu(e.chi_tiet) + '</div>' : '');
    o.appendChild(d);
    o.scrollTop = o.scrollHeight;
  }

  return { mo, dong, loi_trong_hop };
})();
