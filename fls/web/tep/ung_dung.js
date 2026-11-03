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

  // ⭐ Ve LUC MO, ⛔ khong ve san ca sau man luc khoi dong: moi man la mot
  //   phep doc THAT tren kho, va mot man ⛔ chua ai mo ⛔ khong nen ton mot
  //   luot hoi kho. ⚠ Ban khai o MOT cho — them man moi thi them **mot dong**,
  //   ⛔ khong them mot nhanh `if` nua *(bon nhanh `if` la bon cho de quen)*.
  const VE_KHI_MO = {
    // ⭐ `ve_man` chu ⛔ khong `ve`: man `F01` nay co HAI LAN
    //   (`GAP-SCR-14`), va `ve_man` la cho ve thanh chuyen lan.
    'man-f01': { than: '#than-f01', ve: () => F01.ve_man() },
    // ⭐ Man GAN LENH CHI (`QĐ-ITL-148`) — neo vao `#ghep-goc`.
    /* ⭐ `mo_man` chứ ⛔ KHÔNG `ve`: `ve()` chỉ **vẽ lại thứ đang cầm**, nên
       gọi nó ở đây làm màn hiện *"Hàng chờ đã sạch."* trước khi hỏi sổ một
       câu nào. Đúng lỗi đã sống suốt `B3` mà cả hai cổng ⛔ không thấy. */
    'man-ghep': { than: '#ghep-goc', ve: () => F01G.mo_man() },
    'man-f02': { than: '#than-f02', ve: () => F02.ve() },
    // ⭐ `F04` neo vao `#f04-chon` *(o cua trang thai ①)*, ⛔ khong mot the
    //   `#than-f04` — man nay co **nam khoi**, ⛔ khong phai mot than duy nhat.
    'man-f04': { than: '#nap-chon', ve: () => F04.ve() }
  };

  /* ⭐ Mo mot man **tu ma khac** — `F04` bam *"Mo hang cho"* thi phai sang
     `F01` that, ⛔ khong chep lai logic doi tab o hai cho. */
  function mo(id) {
    const b = document.querySelector('.tabs button[data-s="' + id + '"]');
    if (b) b.click();
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
        const m = VE_KHI_MO[b.dataset.s];
        if (m && !TP.$(m.than).textContent.trim()) m.ve();
      };
    });
  }

  window.UD = { mo: mo };

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
