/* ═══════════════════════════════════════════════════════════════════════
   ung_dung.js — khoi dong vo man hinh.

   ★ Ba viec: ⓐ do phien vao thanh tren · ⓑ chon man · ⓒ ⭐ che do GIA LAP de
   **xem duoc ca bon trang thai** ma ⛔ khong phai tat may chu.

   ⛔⛔ **Che do gia lap ⛔ KHONG BAO GIO sinh ra mot con so.** No chi lam cho
   cua **rong**, **hong**, hay **cham**. Ly do: mot man hinh co the bia so la
   mot man hinh se bia so nham vao mot ngay nao do, va ke toan ⛔ khong co cach
   nao biet. ⇒ Ba che do, va ca ba deu chi bo bot, ⛔ khong them.
   ⚠ Va khi bat, mot **thanh do** nam ngang dau trang noi thang no dang gia lap.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

(function () {

  const GIA_LAP = {
    rong: {
      ten: 'CỬA TRẢ RỖNG',
      lam: () => Promise.resolve({ data: null, meta: {} })
    },
    loi: {
      ten: 'CỬA TRẢ LỖI',
      lam: () => Promise.reject(
        new FLS.LoiCua('FLS-INTERNAL', 500, 'lỗi giả do chế độ giả lập',
                       null, 'gia-lap'))
    },
    mat_ket_noi: {
      ten: 'MẤT KẾT NỐI',
      lam: () => Promise.reject(
        new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'ngắt giả do chế độ giả lập'))
    },
    tai: {
      ten: 'ĐANG TẢI MÃI',
      lam: () => new Promise(() => { })   // ⛔ khong bao gio xong — de nhin ⓐ
    }
  };

  function bat_gia_lap(ten) {
    const g = GIA_LAP[ten];
    if (!g) return null;
    // ⛔ Thay CA `doc` lan `ghi`: mot che do gia lap chi ne duong doc se lam
    // nguoi thu tuong duong ghi da duoc thu.
    FLS.doc = g.lam;
    FLS.ghi = g.lam;
    FLS.goi = g.lam;
    return g;
  }

  function ve_thanh_gia_lap(g, ten) {
    const d = TP.el('div', 'gia-lap');
    d.setAttribute('role', 'alert');
    d.innerHTML = '⛔ MÀN ĐANG Ở CHẾ ĐỘ GIẢ LẬP · ' + TP.chu(g.ten) +
      ' — ⛔ KHÔNG một con số nào trên màn là số thật. ' +
      'Bỏ <span class="mono">?gia_lap=' + TP.chu(ten) +
      '</span> khỏi địa chỉ để về màn thật.';
    document.body.insertBefore(d, document.body.firstChild);
  }

  function do_phien() {
    const p = window.FLS_PHIEN || {};
    const t = TP.$('#p-nguoi');
    if (t) t.textContent = p.actor
      ? 'kế toán · ' + p.actor
      : '⛔ chưa biết ai đang làm';
    const n = TP.$('#p-nap');
    if (n) n.textContent = p.pham_vi || 'phạm vi: lần nạp thật';
    const c = TP.$('#p-cua');
    if (c) c.textContent = p.cho_ghi ? 'cửa: ĐỌC + GHI' : 'cửa: CHỈ ĐỌC';
  }

  function chon_man() {
    const nut = document.querySelectorAll('.tabs button');
    nut.forEach(function (b) {
      b.onclick = function () {
        nut.forEach(x => x.setAttribute('aria-pressed',
                                        x === b ? 'true' : 'false'));
        document.querySelectorAll('section.screen').forEach(
          s => s.classList.toggle('on', s.id === b.dataset.s));
        window.scrollTo({ top: 0 });
        // ⛔ Vẽ LÚC MỞ, ⛔ không vẽ sẵn cả bốn màn lúc khởi động: hàng chờ là
        // một phép đọc thật trên kho, và một màn ⛔ chưa ai mở ⛔ không nên tốn
        // một lượt hỏi kho.
        if (b.dataset.s === 'man-f01' && !TP.$('#than-f01').textContent.trim())
          F01.ve();
        if (b.dataset.s === 'man-f02' && !TP.$('#than-f02').textContent.trim())
          F02.ve();
      };
    });
  }

  function khoi_dong() {
    const q = new URLSearchParams(window.location.search);
    const ten = q.get('gia_lap');
    if (ten) {
      const g = bat_gia_lap(ten);
      if (g) ve_thanh_gia_lap(g, ten);
      else console.warn('⛔ chế độ giả lập không biết:', ten,
                        '— các chế độ có:', Object.keys(GIA_LAP));
    }
    do_phien();
    chon_man();
    F03.ve(TP.$('#than-f03'), TP.$('#than-phu'));
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', khoi_dong);
  else khoi_dong();
})();
