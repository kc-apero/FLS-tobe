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
    /* ⭐ `WO-023` `(d)` *(`BA-06` v4.11 `ⓕ4` · `BA-07` v3.5 §5)*: ba chuyện
       từng mượn mã ngay trên ⇒ màn nói *"giá trị bạn gõ khác…"* cho một cú
       ghép chồng / bỏ gán dòng đã bị bỏ / mở lại dòng chưa xong. Chữ
       **nguyên văn** `ⓕ4` *(bài `test_wo023_cd_…` đọc chính spec)*. */
    'FLS-DA-GHEP': {
      cau: 'Giao dịch này đã được gán với lệnh khác rồi.',
      lam_gi: 'Tải lại để thấy lệnh đang gán; muốn đổi thì Bỏ gán trước rồi gán lại.'
    },
    'FLS-KHONG-CON-MOI-NOI': {
      cau: 'Giao dịch này không còn gán với lệnh nào — có thể vừa có người bỏ gán trước bạn.',
      lam_gi: 'Tải lại lệnh để thấy trạng thái thật. Không cần làm gì thêm.'
    },
    'FLS-CHUA-XONG': {
      cau: 'Dòng này chưa từng được bấm Xong — không có gì để mở lại.',
      lam_gi: 'Dòng vẫn ở hàng chờ; làm tiếp như bình thường.'
    },
    'FLS-LOCKED-PERIOD': {
      cau: 'Kỳ này đã chốt — không ghi thêm được nữa.',
      lam_gi: 'Vẫn bấm “Xong” được. Muốn sửa số thì phải mở lại kỳ.'
    },
    'FLS-CONTRACT-DRIFT': {
      cau: 'Máy đọc sổ ra khác với bản khai cột — số trên màn có thể lệch.',
      lam_gi: '⛔ Đừng dùng số này. Báo người dựng hệ.'
    },
    // ── ⭐ Nhóm NẠP (`CR#11`). Mỗi câu phải nói NGƯỜI ĐỌC LÀM GÌ TIẾP,
    //    ⛔ không chỉ nói cái gì sai — một câu chỉ tả lỗi thì kế toán bỏ qua.
    'FLS-NGUON-LA': {
      cau: 'Không có nguồn nào mang mã đó.',
      lam_gi: 'Chọn lại nguồn trong danh sách — ⛔ đừng gõ tay số nguồn.'
    },
    'FLS-KHAI-KHONG-CO': {
      // ⚠ CỐ Ý khác hẳn câu trên: nguồn CÓ, chỉ là chưa ai khai cách đọc nó.
      //    Hai câu giống nhau sẽ đẩy người ta đi sai đường sửa.
      cau: 'Nguồn này có, nhưng chưa ai khai cột nào là gì cho nó.',
      lam_gi: 'Khai cột một lần cho nguồn này, rồi nạp lại. Máy ⛔ không đoán '
        + 'vị trí cột — đoán sai một cột là sai tiền.'
    },
    'FLS-KHAI-THIEU': {
      cau: 'Bản khai còn thiếu trường — máy ⛔ không nạp một phần.',
      lam_gi: 'Chỉ đủ cả 6 trường mới đi tiếp được. Thiếu một cột mà vẫn nạp '
        + 'thì cột mất có thể chính là cột tiền.'
    },
    'FLS-SOAT-CHAN': {
      cau: 'Biên bản soát có luật hạng CHẶN đỏ ⇒ ⛔ không một dòng nào vào sổ.',
      lam_gi: 'Đọc dòng đỏ trong biên bản. Hạng CHẶN là lỗi của HỆ, ⛔ không '
        + 'phải lỗi tệp của anh/chị — báo cho người dựng hệ.'
    },
    // ── ⭐⭐ Nhóm ẢNH CHỤP (`QĐ-ITL-110`). HAI câu, ⛔ KHÔNG một — cùng lý do
    //    `FLS-NGUON-LA` và `FLS-KHAI-KHONG-CO` phải khác nhau: chúng dẫn người
    //    đọc đi HAI đường sửa khác nhau.
    'FLS-CHUP-KHONG-CO': {
      cau: 'Không có lần đọc nào mang mã đó.',
      lam_gi: 'Chọn lại lần đọc trong danh sách — ⛔ đừng gõ tay số.'
    },
    // ⭐⭐ `QĐ-ITL-117` — cu bam gop **tu choi CA LO**, va cau nay phai noi
    //    ra **duong di tiep**: nguon ⛔ khong tu chung thi khai TUNG nguon.
    //    ⛔ Mot cau chi noi *"khong dat"* se lam nguoi ta bam lai lan nua.
    'FLS-THU-TU-KHONG-TU-CHUNG': {
      cau: 'Có nguồn mà dữ liệu của nó ⛔ không tự nói ra được cách đọc ngày '
        + '(hoặc nói khác với bản khai đang có) ⇒ cả lô bị từ chối, ⛔ không '
        + 'một bản khai nào được ghi.',
      lam_gi: 'Đọc câu bằng chứng của những nguồn được nêu tên, rồi ấn định '
        + 'thứ tự cho TỪNG nguồn ấy ở bảng dưới. Cú bấm gộp chỉ nhận nguồn '
        + 'mà chính dữ liệu của nó đã loại trừ được một cách đọc.'
    },
    // ⭐⭐ `QĐ-ITL-118` — cú bấm ghép LÔ **từ chối CẢ LÔ**. Và câu này ⛔ KHÔNG
    //    được dừng ở *"không tự chứng"*: bốn cổng của phép ghép dẫn người đọc
    //    đi **bốn đường sửa khác nhau**, nên câu phải chỉ về `ly_do` từng dòng.
    'FLS-GHEP-KHONG-TU-CHUNG': {
      cau: 'Trong lô có dòng mà máy ⛔ không tự kết luận được là ghép vào lệnh '
        + 'chi nào ⇒ cả lô bị từ chối, ⛔ không một mối nối nào được ghi.',
      lam_gi: 'Xem cột “lý do” của những dòng được nêu tên: khác tiền tệ, hay '
        + 'lệnh chi đã bị ghép cho dòng khác, hay lệnh chi chưa được duyệt, '
        + 'hay số tiền lệch ngoài dung sai. Bốn thứ ấy sửa bốn đường khác '
        + 'nhau — và dòng nào cần người chọn thì ghép TỪNG dòng ở màn hàng chờ.'
    },
    'FLS-CHUP-KHONG-NGUON': {
      // ⚠ CỐ Ý khác câu trên: lần đọc CÓ, nguồn CÓ, chỉ là lần đọc ấy
      //    ⛔ không hề đọc nguồn này. Gộp hai câu thì người ta gõ lại đúng cái
      //    mã vừa thất bại.
      cau: 'Lần đọc này có, nhưng nó ⛔ không đọc nguồn anh/chị đang chọn.',
      lam_gi: 'Bấm “Đọc lại” cho nguồn ấy, rồi nạp từ lần đọc mới. ⛔ Đừng nạp '
        + 'từ một lần đọc ⛔ không có nguồn đó — sẽ ⛔ không có dòng nào.'
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
    },
    /* ⭐ `WO-023` `(c)` *(`BA-06` v4.11 `ⓕ3`)* — lượt **GHI** quá hạn chờ.
       ⛔⛔ Câu **⛔ được** nói *"chưa xảy ra"*: lượt đã gửi, máy chủ có thể
       **đã** ghi xong mà câu trả lời chưa về. */
    'FLS-HET-GIO': {
      cau: 'Máy chưa trả lời sau 30 giây — chưa biết lượt ghi đã vào sổ hay chưa.',
      lam_gi: 'Tải lại để xem trạng thái thật trước khi bấm lại.'
    }
  };

  /* ⛔ Ma sinh o man hinh — bai kiem phu ma loi bo qua nhom nay khi doi chieu
     nguoc *(chung ⛔ khong co trong `bao.py`, va do la dung)*. */
  const MA_TU_MAN_HINH = ['FLS-MAT-KET-NOI', 'FLS-TRA-LOI-LA', 'FLS-HET-GIO'];

  /* ⭐⭐ `WO-023` `(c)` *(`BA-06` v4.11 `ⓕ3`)* — hạn chờ cửa **GHI**, **một**
     hằng *(bài đặt được giá trị nhỏ: `FLS.HAN_CHO.ghi_ms = 40`)*. Vì sao: hộp
     đang chờ cửa **⛔ đóng** được *(`ⓕ2`)* ⇒ thiếu hạn thì một lượt ghi treo
     nhốt người trong hộp **mãi** *(đo 02/10: `fls/web/tep` **0** dòng
     `timeout` — `fetch` trần)*. `30 s` ≈ **3,7 lần** lượt cửa chậm nhất đã đo
     *(một lượt **đọc** `lenh-cho` **8,16 s** — `KQ-021`)*.
     ⛔ Hạn chờ cho cửa **đọc** *(⛔ trong lượt này)*. ⛔ Tự thử lại lượt ghi:
     ghi ⛔ biết kết quả rồi gửi lần nữa = có thể ghi **hai** lần. ⛔ Huỷ
     `fetch` *(⛔ `AbortController`)*: lượt đã gửi ⛔ huỷ được ở máy chủ —
     huỷ phía màn chỉ làm mất câu trả lời thật nếu nó về muộn. */
  const HAN_CHO = { ghi_ms: 30000 };

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
    if (pt === 'GET') return _goi(duong, tuy, pt);
    let hen = null;
    const het = new Promise(function (_, no) {
      const ms = HAN_CHO.ghi_ms;
      hen = setTimeout(function () {
        no(new LoiCua('FLS-HET-GIO', 0, 'quá ' + (ms / 1000) + ' s chưa có trả lời — '
                      + pt + ' ' + duong));
      }, ms);
    });
    try {
      /* ⭐ `race` gắn trình bắt cho **cả hai** lời hứa ⇒ lượt thật về muộn
         *(kể cả lỗi)* ⛔ thành lỗi chưa bắt. */
      return await Promise.race([_goi(duong, tuy, pt), het]);
    } finally {
      clearTimeout(hen);
    }
  }

  async function _goi(duong, tuy, pt) {
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

  return { GOC, CAU, MA_TU_MAN_HINH, HAN_CHO, LoiCua, goi, doc, ghi, the };
})();
