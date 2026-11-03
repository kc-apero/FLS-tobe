/* ═══════════════════════════════════════════════════════════════════════
   thanh_phan.js — cac manh dung lai: chip niem tin · so ke toan · chu an toan.

   ★ Lay tu `A-CCR` *(`BA-06` §7 "he thi giac DUNG LAI, ⛔ khong ve lai")*.
   ⛔ Tep nay ⛔ khong goi cua, ⛔ khong biet man nao. No nhan gia tri, tra chuoi
   hay the.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const TP = (function () {

  /* ── ⛔ Chu an toan ───────────────────────────────────────────────────
     ⛔⛔ Cot `memo` (Dien giai) cua so THAT di thang len man hinh, va no chua
     ky tu gi cung duoc. Mot dau `<` ⛔ khong duoc bien thanh the HTML — ⛔
     khong phai vi lo hacker *(so nay o may noi bo)*, ma vi mot dong dien giai
     co `<` se **bien mat mot doan** tren man va ke toan ⛔ khong biet.        */
  function chu(v) {
    if (v === null || v === undefined) return '';
    return String(v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ── ⭐ So kieu ke toan ───────────────────────────────────────────────
     ⛔⛔ Cua tra tien la CHUOI, ⛔ khong phai so (`bao.py`: JSON ⛔ khong noi
     kieu nen may doc bien moi so thanh `float64` truoc khi ai kip chon). Nen
     o day chi **dinh dang de doc**, va gia tri goc van la chuoi.
     ⚠ Ham nay ⛔ khong duoc dung de TINH. Moi phep cong tien phai o may chu. */
  function tien(v) {
    if (v === null || v === undefined || v === '') return '—';
    const n = Number(v);
    if (!isFinite(n)) return chu(v);
    return n.toLocaleString('vi-VN', { maximumFractionDigits: 0 });
  }

  function so(v) {
    if (v === null || v === undefined || v === '') return '—';
    const n = Number(v);
    return isFinite(n) ? n.toLocaleString('vi-VN') : chu(v);
  }

  /* ── ⭐ Chip niem tin — FLS co DUNG ba co (`UI-F1`) ──────────────────── */
  const NIEM_TIN = {
    flash:      { lop: 'flash',  chu: 'flash · chưa chốt',
                  ghi: 'Số chưa đối soát, chưa ký. Đọc để làm việc, ⛔ đừng '
                     + 'mang đi báo cáo.' },
    reconciled: { lop: 'recon',  chu: 'đã đối soát',
                  ghi: 'Đã khớp với nguồn, nhưng chưa ai ký chốt.' },
    signed:     { lop: 'signed', chu: 'đã ký',
                  ghi: 'Kế toán đã ký chốt trên sổ gốc.' }
  };

  function chip_niem_tin(trang_thai) {
    const t = NIEM_TIN[trang_thai];
    if (!t) {
      // ⛔ Mot co la ⛔ khong duoc am tham thanh "flash": mot con so chua doi
      // soat khoac nhan da doi soat la loai sai te nhat cua ca lop bao cao —
      // va chieu nguoc lai cung lam nguoi doc mat niem tin vao so dung.
      return '<span class="chip crit" title="cờ niềm tin lạ: ' + chu(trang_thai)
           + '">⛔ cờ lạ</span>';
    }
    return '<span class="chip ' + t.lop + '" title="' + chu(t.ghi) + '">'
         + chu(t.chu) + '</span>';
  }

  /* ── chip trang thai chung ───────────────────────────────────────────── */
  function chip(lop, noi_dung, ghi_chu) {
    return '<span class="chip ' + lop + '"'
         + (ghi_chu ? ' title="' + chu(ghi_chu) + '"' : '') + '>'
         + chu(noi_dung) + '</span>';
  }

  /* ── the ─────────────────────────────────────────────────────────────── */
  function el(the_gi, lop, html) {
    const e = document.createElement(the_gi);
    if (lop) e.className = lop;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  const $ = s => document.querySelector(s);

  return { chu, tien, so, NIEM_TIN, chip_niem_tin, chip, el, $ };
})();
