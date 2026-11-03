/* ═══════════════════════════════════════════════════════════════════════
   trang_thai.js — ⭐ KHUON 4 TRANG THAI, dung chung cho moi man.

   ⛔⛔ **Vi sao mot khuon chung.** `DEV-12` §3: *"Rong va loi ⛔ khong duoc la
   'chua lam'"*. Neu moi man tu ung bien thi man nay ve mot cai vong quay, man
   kia de trang, man thu ba hien `undefined` — va **man de trang la nguy nhat**:
   ke toan doc no thanh *"⛔ khong con viec"* trong khi that ra **may chua hoi
   duoc kho**.

   ⇒ Bon trang thai la BON, ⛔ khong phai *"co du lieu"* va *"chua co"*:
      ⓐ dang tai  — may **dang** hoi
      ⓑ rong      — may **da** hoi, va cau tra loi la **⛔ khong co gi**
      ⓒ loi       — may hoi **hong**  ⇒ ⛔ TUYET DOI khong duoc trong giong ⓑ
      ⓓ mac dinh  — co du lieu that

   ★ `chay()` ep ca bon: goi mot ham lay du lieu roi tu chon trang thai. Man
   hinh ⛔ khong duoc tu goi `fetch` roi tu ve — no goi `chay()`.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const TT = (function () {

  function _sach(o) { o.textContent = ''; return o; }

  /* ⓐ DANG TAI */
  function tai(o, so_dong) {
    const n = so_dong || 4;
    const d = _sach(o);
    const w = document.createElement('div');
    w.className = 'tt-tai';
    w.setAttribute('aria-busy', 'true');
    for (let i = 0; i < n; i++) {
      const s = document.createElement('div');
      s.className = 'sk';
      // Do dai le nhau de no trong giong DONG CHU dang cho, ⛔ khong giong
      // mot thanh tien trinh — no ⛔ khong biet bao lau nua.
      s.style.width = (58 + ((i * 37) % 40)) + '%';
      w.appendChild(s);
    }
    d.appendChild(w);
  }

  /* ⓑ RONG — phai noi RO la **da hoi roi** */
  function rong(o, tuy) {
    const t = tuy || {};
    const d = _sach(o);
    const w = document.createElement('div');
    w.className = 'tt-rong';
    w.innerHTML =
      '<span class="icon">' + (t.icon || '✓') + '</span>' +
      '<b>' + TP.chu(t.tieu_de || 'Không có dòng nào') + '</b>' +
      (t.cau ? '<div style="margin-top:5px">' + TP.chu(t.cau) + '</div>' : '');
    d.appendChild(w);
  }

  /* ⓒ LOI — ⛔ khong duoc trong giong RONG */
  function loi(o, e, thu_lai) {
    const d = _sach(o);
    const w = document.createElement('div');
    w.className = 'tt-loi';
    w.setAttribute('role', 'alert');
    w.innerHTML =
      '<div class="ma">' + TP.chu(e.ma || 'LỖI') +
        (e.http ? ' · HTTP ' + e.http : '') + '</div>' +
      '<div class="cau"><b>' + TP.chu(e.cau || e.message) + '</b>' +
        (e.lam_gi ? '<br>' + TP.chu(e.lam_gi) : '') + '</div>' +
      (e.chi_tiet
        ? '<div class="muted mono" style="font-size:11px">' +
          TP.chu(e.chi_tiet) + '</div>' : '') +
      (e.request_id
        ? '<div class="faint mono" style="font-size:11px;margin-top:4px">mã ' +
          'yêu cầu ' + TP.chu(e.request_id) + '</div>' : '');
    d.appendChild(w);
    if (thu_lai) {
      const b = document.createElement('button');
      b.className = 'b';
      b.style.marginTop = '10px';
      b.textContent = 'Thử lại';
      b.onclick = thu_lai;
      w.appendChild(b);
    }
  }

  /* ── ⭐ ep ca bon trang thai ──────────────────────────────────────────
     `lay`    : ham async tra `{data, meta}`
     `ve`     : ham ve du lieu that vao `o`
     `la_rong`: ham noi du lieu co rong khong (mac dinh: mang do dai 0)      */
  async function chay(o, lay, ve, tuy) {
    const t = tuy || {};
    tai(o, t.so_dong);
    let kq;
    try {
      kq = await lay();
    } catch (e) {
      loi(o, e, function () { chay(o, lay, ve, tuy); });
      return null;
    }
    const la_rong = t.la_rong
      ? t.la_rong(kq.data)
      : (Array.isArray(kq.data) ? kq.data.length === 0 : !kq.data);
    if (la_rong) { rong(o, t.rong); return kq; }
    _sach(o);
    ve(kq.data, kq.meta, o);
    return kq;
  }

  return { tai, rong, loi, chay };
})();
