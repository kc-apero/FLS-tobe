/* ═══════════════════════════════════════════════════════════════════════
   goi_cua.js — ⭐ CHO DUY NHAT trong ca man hinh goi cua API.

   ⛔⛔ **Vi sao mot cho duy nhat.** `DEV-12` §3: *"⛔ Khong `fetch` rai rac: ma
   loi `409`/`422` phai dich MOT CHO thanh cau tieng Viet"*. Neu moi man tu
   dich thi cung mot ma se co bon cau khac nhau, va cau nao dung la tuy man
   nao duoc viet sau — dung lop loi ma ca bo tai lieu nay dung ra de chua.

   ⚠ Bai `tests/web/test_goi_cua_phu_het_ma_loi.py` doc `fls/api/bao.py` roi
   quet tep nay: **moi ma trong `MA_LOI` phai co mot cau tieng Viet o day**.
   ⇒ Ai them mot ma loi o tang cua ma quen man hinh se lam bai do **DO**, chu
   ⛔ khong de man hinh hien mot cau vo nghia cho ke toan.

   ★ Tep nay ⛔ khong biet mot man hinh nao. No tra ve du lieu hay **nem** mot
   `LoiCua` — man hinh quyet dinh ve gi.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const FLS = (function () {

  const GOC = '/api/fls/v1';

  /* ── Cau tieng Viet cho tung ma loi ────────────────────────────────────
     `cau`   : noi cho KE TOAN, ⛔ khong dung tu ky thuat.
     `lam_gi`: viec nguoi doc lam duoc ngay. Rong = ⛔ khong tu lam duoc.
     ⛔ Ma nao ⛔ khong co o day thi ham `dich` NEM — ⛔ khong am tham cho qua. */
  const CAU = {
    /* — tu `fls/api/bao.py` · MA_LOI — */
    'FLS-CONFLICT-SOURCE': {
      cau: 'Giá trị bạn gõ khác với giá trị nguồn đang có.',
      lam_gi: 'Xem giá trị nguồn rồi chọn: giữ nguồn, hay ghi đè kèm lý do.'
    },
    'FLS-LOCKED-PERIOD': {
      cau: 'Kỳ này đã chốt — không ghi thêm được nữa.',
      lam_gi: 'Vẫn bấm “Xong” được. Muốn sửa số thì phải mở lại kỳ.'
    },
    'FLS-CONTRACT-DRIFT': {
      cau: 'Máy đọc sổ ra khác với bản khai cột — số trên màn có thể lệch.',
      lam_gi: '⛔ Đừng dùng số này. Báo người dựng hệ.'
    },
    'FLS-DQ-FAILED': {
      cau: 'Cổng kiểm chất lượng không đạt nên máy chặn phép ghi này.',
      lam_gi: 'Mở màn “Cổng hôm nay” xem cổng nào đỏ.'
    },
    'FLS-UNMAPPED-HIDDEN': {
      cau: 'Chỗ này đang là “chưa gán” — máy không nhận một giá trị cứng đè lên.',
      lam_gi: 'Gõ giá trị thật, hay để nguyên “chưa gán”.'
    },
    'FLS-ACCR-UNREADABLE': {
      cau: 'Không đọc được kết quả đối soát tiền mặt.',
      lam_gi: 'Thử lại sau. Nếu vẫn vậy thì báo người dựng hệ.'
    },
    'FLS-UNAUTHORIZED': {
      cau: 'Phiên làm việc đã hết hạn.',
      lam_gi: 'Tải lại trang để mở phiên mới.'
    },
    'FLS-NOT-FOUND': {
      cau: 'Không tìm thấy dòng này — hoặc nó nằm ngoài lần nạp đang xem.',
      lam_gi: 'Kiểm tra lại mã dòng.'
    },
    'FLS-BAD-REQUEST': {
      cau: 'Máy không hiểu yêu cầu vừa gửi.',
      lam_gi: 'Xem lại ô vừa gõ. Nếu không rõ thì báo người dựng hệ.'
    },
    'FLS-METHOD': {
      cau: 'Việc này chưa mở trên cửa đang chạy.',
      lam_gi: 'Cửa có thể đang ở chế độ chỉ đọc.'
    },
    'FLS-TOO-LARGE': {
      cau: 'Nội dung gửi lên quá lớn.',
      lam_gi: 'Rút ngắn lý do rồi thử lại.'
    },
    'FLS-INTERNAL': {
      cau: 'Máy gặp lỗi bên trong.',
      lam_gi: 'Báo người dựng hệ kèm mã yêu cầu ở dưới.'
    },

    /* — ⭐ hai ma SINH O MAN HINH, ⛔ khong den tu cua. Khai o day de man
         hinh ⛔ khong bao gio phai hien mot cau vo danh. — */
    'FLS-MAT-KET-NOI': {
      cau: 'Không nối được tới máy chủ FLS.',
      lam_gi: 'Kiểm tra máy chủ còn chạy không, rồi tải lại trang.'
    },
    'FLS-TRA-LOI-LA': {
      cau: 'Máy chủ trả về thứ màn hình không đọc được.',
      lam_gi: 'Báo người dựng hệ.'
    }
  };

  /* ⛔ Ma sinh o man hinh — bai kiem phu ma loi bo qua nhom nay khi doi chieu
     nguoc *(chung ⛔ khong co trong `bao.py`, va do la dung)*. */
  const MA_TU_MAN_HINH = ['FLS-MAT-KET-NOI', 'FLS-TRA-LOI-LA'];

  class LoiCua extends Error {
    constructor(ma, http, chi_tiet, khac, request_id) {
      const c = CAU[ma];
      super(c ? c.cau : ma);
      if (!c) {
        // ⛔ Mot ma ⛔ khong khai la mot lo hong, ⛔ khong phai mot truong hop
        // hiem. Ne no bang cach hien chinh ma thi ke toan doc mot chuoi ky
        // thuat va ⛔ khong biet lam gi.
        console.error('⛔ mã lỗi chưa khai câu tiếng Việt:', ma);
      }
      this.ma = ma;
      this.http = http;
      this.cau = c ? c.cau : 'Lỗi chưa được mô tả: ' + ma;
      this.lam_gi = c ? c.lam_gi : '';
      this.chi_tiet = chi_tiet || '';
      this.khac = khac || null;          // `409` cho biet nguon dang la gi
      this.request_id = request_id || '';
    }
  }

  function the() {
    const p = window.FLS_PHIEN || {};
    return p.the || '';
  }

  function dia_chi(duong, q) {
    const u = new URL(GOC + duong, window.location.origin);
    if (q) for (const [k, v] of Object.entries(q)) {
      if (v !== null && v !== undefined && v !== '') u.searchParams.set(k, v);
    }
    return u.toString();
  }

  /* ── goi mot cua ──────────────────────────────────────────────────────
     Tra `{data, meta}`. ⛔ NEM `LoiCua` khi that bai — ⛔ khong bao gio tra
     mot doi tuong rong de man hinh tuong la "khong co du lieu". Rong va loi
     la HAI trang thai khac nhau (`DEV-12` §3).                            */
  async function goi(duong, tuy = {}) {
    const pt = tuy.phuong_thuc || 'GET';
    const co_than = pt !== 'GET';
    let r;
    try {
      r = await fetch(dia_chi(duong, tuy.q), {
        method: pt,
        headers: Object.assign(
          { 'Authorization': 'Bearer ' + the() },
          co_than ? { 'Content-Type': 'application/json' } : {}),
        body: co_than ? JSON.stringify(tuy.than || {}) : undefined,
        cache: 'no-store'
      });
    } catch (e) {
      throw new LoiCua('FLS-MAT-KET-NOI', 0, String(e && e.message || e));
    }

    let j;
    try {
      j = await r.json();
    } catch (e) {
      throw new LoiCua('FLS-TRA-LOI-LA', r.status,
                       'thân trả về không phải JSON');
    }
    if (!j || typeof j !== 'object' || !('data' in j)) {
      throw new LoiCua('FLS-TRA-LOI-LA', r.status,
                       'thân JSON thiếu khoá `data`');
    }
    const meta = j.meta || {};
    if (j.error) {
      throw new LoiCua(j.error.code, r.status, j.error.detail,
                       j.error.khac, meta.request_id);
    }
    if (!r.ok) {
      // ⛔ HTTP hong ma than ⛔ khong khai loi ⇒ ⛔ khong coi la thanh cong.
      throw new LoiCua('FLS-TRA-LOI-LA', r.status,
                       'mã HTTP ' + r.status + ' mà thân không khai lỗi');
    }
    return { data: j.data, meta: meta };
  }

  const doc = (duong, q) => goi(duong, { q: q });
  const ghi = (duong, than, q) =>
    goi(duong, { phuong_thuc: 'POST', than: than, q: q });

  return { GOC, CAU, MA_TU_MAN_HINH, LoiCua, goi, doc, ghi, the };
})();
