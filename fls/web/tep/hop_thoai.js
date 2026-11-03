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
     ⓒ `Esc` / bấm ngoài đóng hộp khi **chưa** có lượt ghi nào đang bay — và
       lúc ấy đóng là **⛔ KHÔNG làm gì** *(`BA-06` v4.11 `ⓕ2` — câu luật đọc
       lại)*. ⛔⛔ Bản trước viết *"`Esc` và bấm ra ngoài đóng hộp, và đóng hộp
       luôn là ⛔ làm gì"* — đúng **trước** khi bấm nút, **sai** sau: khi hàm
       nút đã gửi lượt ghi, đóng hộp ⛔ huỷ được lượt đang bay ⇒ đóng lúc ấy là
       **nói dối**, và câu lỗi cửa sau đó rơi vào `#dlg-b` của hộp **đã đóng**
       *(`KQ-021 F-2`, Chrome `8099`: màn im)*. ⇒ Trong lúc hàng nút khoá chờ
       cửa, `Esc` + bấm nền **bị nuốt**, hộp hiện dòng *"Đang ghi vào sổ — chờ
       máy trả lời."*; cửa trả ⇒ như cũ.

   ★ Và một luật nữa — ⓓ **hộp đang mở là MODAL với bàn phím** *(`ⓕ1`, `KQ-021
     F-1`)*: khi hộp mở, mọi phím tắt của màn sau lưng nằm im, `Esc` **chỉ**
     đóng hộp. Bản trước: trình nghe của màn ⛔ hỏi hộp ⇒ `Esc` đóng hộp **và**
     lệnh; `j` đổi lệnh sau lưng hộp *(hộp `Gỡ cả 2` vẫn gỡ lệnh cũ)*.
     ⇒ Hai nửa, để phép chặn ⛔ phụ thuộc **thứ tự đăng ký** trình nghe:
       · trình nghe phím của hộp nghe ở pha **capture** *(trình duyệt gọi nó
         **trước** mọi trình nghe pha nổi trên `document`, bất kể ai đăng ký
         trước)* và **đánh dấu** sự kiện nó đã nhận *(`e._hop_thoai = true`)*;
       · trình nghe của màn hỏi `HT.nuot_phim(e)` *(hàm **hỏi**, chỉ-đọc —
         ⛔ hàm dựng hộp mới)* rồi thôi: `true` khi hộp **đang** mở **hoặc**
         sự kiện này đã được hộp nhận *(⛔ có dấu thì `Esc` vừa đóng hộp sẽ
         rơi tiếp xuống màn và đóng luôn lệnh)*.
     ⚠ Trình nghe của hộp gắn ở lần `HT.mo` **đầu tiên** — **kể cả** khi
       `#scrim` đã có sẵn *(bản trước chỉ gắn khi `_khung` **tự dựng** `#scrim`
       ⇒ vỏ thử dựng sẵn `#scrim` thì hộp ⛔ có trình nghe `Esc` nào — bài
       `KQ-021` phải chép tay trình nghe ấy)*.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const HT = (function () {

  let dang_mo = null;      // {đóng}
  /* ⭐ `ⓕ2`: hàm nút trả `Promise` chưa xong ⇒ có một lượt ghi **đang bay**.
     Giữ **mã lượt** *(⛔ cờ trần)*: một hộp mới mở trong lúc lượt cũ còn bay
     ⛔ được kế thừa cờ của nó. */
  let _lan = 0, _cho = 0;
  let _da_nghe = false;

  const CAU_CHO = 'Đang ghi vào sổ — chờ máy trả lời.';

  function _nghe(s) {
    if (_da_nghe) return;
    _da_nghe = true;
    s.addEventListener('click', e => { if (e.target === s) dong(); });
    /* ⭐ `ⓓ`/`ⓕ1`: pha **capture** — xem luật ⓓ đầu tệp. */
    document.addEventListener('keydown', e => {
      if (!dang_mo) return;
      e._hop_thoai = true;
      if (e.key === 'Escape') dong();
    }, true);
  }

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
    }
    _nghe(s);
    return s;
  }

  /* ⭐ Đóng **từ người** *(`Esc` · bấm nền · nút ⛔ hàm · nơi gọi ngoài)* —
     ⛔ đóng khi một lượt ghi đang bay *(`ⓕ2`)*. Trả `true` ⇔ đã đóng. */
  function dong() {
    if (_cho && _cho === _lan) return false;
    _dong();
    return true;
  }

  function _dong() {
    const s = document.getElementById('scrim');
    if (s) s.classList.remove('on');
    dang_mo = null;
  }

  /* ⭐ `ⓕ1` — hàm **hỏi** *(chỉ-đọc)* cho trình nghe phím của màn: `true` ⇒
     phím này **⛔** thuộc về màn sau lưng. Nhận sự kiện để bắt cả ca hộp
     **vừa** đóng bằng chính sự kiện này *(`Esc` — dấu `_hop_thoai`)*. */
  function nuot_phim(e) {
    return !!dang_mo || !!(e && e._hop_thoai);
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
        const lan = _lan;
        let ra, dong_cho = null;
        try {
          ra = ham();
          /* ⭐ `ⓕ2`: hàm trả `Promise` ⇒ lượt ghi **đang bay** ⇒ nuốt `Esc` /
             bấm nền + một dòng nói máy đang làm *(lớp `note` — có sẵn)*.
             Hàm đồng bộ ⇒ ⛔ dòng nào *(⛔ chớp chữ cho một việc ⛔ chờ)*. */
          if (ra && typeof ra.then === 'function') {
            _cho = lan;
            const o = TP.$('#dlg-b');
            if (o) {
              dong_cho = TP.el('div', 'note');
              dong_cho.textContent = CAU_CHO;
              o.appendChild(dong_cho);
            }
            ra = await ra;
          }
        } finally {
          if (_cho === lan) _cho = 0;
          if (dong_cho && dong_cho.parentNode)
            dong_cho.parentNode.removeChild(dong_cho);
          [...f.children].forEach(x => { x.disabled = false; });
        }
        if (ra !== false) _dong();
      };
      f.appendChild(b);
    });
    s.classList.add('on');
    _lan++;
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

  return { mo, dong, loi_trong_hop, nuot_phim, CAU_CHO };
})();
