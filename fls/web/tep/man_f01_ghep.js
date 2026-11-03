/* ═══════════════════════════════════════════════════════════════════════
   man_f01_ghep.js — màn **GÁN LỆNH CHI ↔ GIAO DỊCH** (`SCR-F01`).

   ⭐⭐⭐ Hợp đồng hình dạng: `Artifacts/Thiet-ke-Man-Gan-Lenh-Chi.md`
        ＋ `BA-06 §4.5` (trông ra sao) · `§4.6` (5 sửa bắt buộc)
        ＋ `BA-13 §A8`  (phản ứng thế nào) · `BA-07 §4h` (cửa)

   ⛔⛔ **Tệp này có HAI cổng canh riêng**, và lý do có cái thứ hai đáng kể:

     ⓐ `tests/web/test_b3_fe_bam_thiet_ke.py` — biến hợp đồng thiết kế thành
        **phép đo trên mã**. Một lời nhắc ⛔ không giữ được gì: `man_f01_lenh.js`
        đi **339 → 735** dòng qua 7 lần sửa và ⛔ không lần nào tổng đi xuống.
        Mỗi lần sửa đều có lý do riêng và đều đúng; cái mất là **hình dạng tổng
        thể**, và nó mất **trong im lặng**.

     ⓑ ⭐⭐ `tests/web/test_b3_man_ghep_chay_duoc.py` — **CHẠY** màn trong DOM
        giả. ⛔⛔ Bản đầu của tệp này gọi một API `TP` **tôi tự bịa**
        (`TP.el(tag, {attrs}, ...con)` trong khi thật là `TP.el(the_gi, lop,
        html)`), và nó **qua cả 14 phép** của cổng ⓐ — vì cổng ấy **quét CHỮ**.
        ⇒ Một cổng đọc mã ⛔ **không thay được** một cổng chạy mã.

   ── BỐN LUẬT ⛔ KHÔNG ĐƯỢC VI PHẠM ────────────────────────────────────

     ① ⭐⭐⭐ `Diễn giải` ⛔ **KHÔNG BAO GIỜ** bị hy sinh khi màn hẹp. Nó là
        **bằng chứng duy nhất** của `4.145/8.387` = **49%** cuốn sổ (nhánh
        nước ngoài, `DT-I13 ⓑ`). Thứ tự bỏ: `Nguồn` → `Số CT` → **hết**.

     ② ⭐⭐ Máy **đề xuất**, người **quyết** (`INV-I16`). ⛔ Không chọn sẵn ứng
        viên nào — kể cả dòng máy đề xuất. `Enter` **bị khoá** ở ca lệch tiền:
        **45%** ca ⛔ không có ứng viên khớp đúng tiền, nên một phím `Enter` dễ
        dãi **dạy người ta gật bừa** (`NFR-I25`).

     ③ ⭐⭐ **Đích cuối ⛔ không phải việc** (`INV-I20`). `768` dòng ⛔ không gán
        được có **chip riêng**, ⛔ không trộn vào `738` dòng việc thật.

     ④ ⭐ Trường **VẮNG** phải hiện ra. `tho` có **41 hình dạng**; `Chi nhánh`
        chỉ **11,7%**, `PE (Urgent)` **0,45%**.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F01G = (function () {

  /* ── hằng số của HỢP ĐỒNG — cổng canh đọc thẳng mấy dòng này ────────── */

  /* ⭐ `UI-F7` — trần **11**, owner nới `9 → 11` ngày 21/09 (`QĐ-ITL-147`).
     ⚠ Trần nới thì **luật ⛔ không nới**: trường thứ 12 vẫn phải **bỏ một**
       hoặc **xin một quyết định nữa**. Một trần đổi được ⛔ không cần ai ký
       thì nó ⛔ không phải trần — và đó đúng là đường `339 → 735` đã đi. */
  const TRUONG_THE = [
    'ma_lenh', 'trang_thai', 'loai_phieu', 'noi_dung', 'so_tien',
    'nguoi_nhan', 'so_chung_tu', 'phap_nhan', 'ngan_hang', 'tai_khoan', 'cdt',
  ];

  /* ⭐⭐⭐ Thứ tự HY SINH cột khi màn hẹp. `dien_giai` ⛔ **KHÔNG** có mặt ở
     đây, và đó là điều cổng canh kiểm. */
  const COT_BO_DUOC = ['nguon', 'doc_no'];

  /* ⭐ Bốn bậc — phân bằng **thứ tự ＋ một ký hiệu tô màu**, ⛔ không bốn chip
     cùng cỡ: bậc ④ chiếm **149/226** ứng viên sẽ **nhuộm hết màn**.
     ⛔ Nghĩa nói **một lần** — ở `title`, ⛔ không lặp thành nhãn mỗi dòng.
     ⭐ *(`WO-032` vòng 2)* ＋ **chú giải** một dòng trên danh sách, chữ sinh
       từ chính bảng này *(`ve_chu_giai`)* — ⛔ `title` là lối **duy nhất**. */
  const BAC = {
    ma:           { k: '①', l: 'khớp số chứng từ', m: 'good' },
    tien:         { k: '②', l: 'đúng số tiền',     m: 'info' },
    gan_tien:     { k: '③', l: 'gần đúng số tiền', m: 'warn' },
    cung_tien_te: { k: '④', l: 'cùng đơn vị tiền', m: '' },
    /* ⭐ `WO-032` *(`BA-07` v3.7 §4h ⓹)*: bậc **chỉ** cửa `/so` *(Toàn sổ)*
       sinh — dòng ⛔ khớp mã, **khác tiền tệ** lệnh. ⛔ Trước: cửa dán
       `cung_tien_te` ⇒ màn nói *"cùng đơn vị tiền"* cho dòng USD cạnh lệnh
       VND *(sổ thật: **3.926 / 6.165** dòng chưa nối với một lệnh VND)*.
       ⛔ Tông mới / lớp CSS mới: `m: ''` như ④ — nghĩa nói ở ký hiệu + `title`. */
    khac_tien_te: { k: '≠', l: 'khác tiền tệ', m: '' },
  };
  const THU_TU_BAC = ['ma', 'tien', 'gan_tien', 'cung_tien_te', 'khac_tien_te'];

  /* ⭐ BỐN chip — bản dựng có ba, và `Chưa gán` của nó gộp cả `768` dòng đích
     cuối vào việc hằng ngày ⇒ danh sách mặc định `1.553` thay vì **738**. */
  const CHIP = [
    ['chua_gan', 'Chưa gán'],
    ['da_gan', 'Đã gán'],
    ['khong_gan_duoc', 'Không gán được'],
    ['tat_ca', 'Tất cả'],
  ];

  const KHONG_CO = '— không có';

  /* ⭐⭐⭐ CHIP → CỬA. ⛔ Đo `22/09` trên lần nạp thật, gọi cửa thật:
       `chua_gan`        `?ro=nguoi` ＋ `?ro=may&tu_chung=0` → **738** ✔ `G-a`
       `khong_gan_duoc`  `?ro=khong`                        → **768** ✔ `INV-I20`
       `da_gan`          ✅ tuyến **40** `/queue/lenh-da-gan` — mở `22/09`.
                         Trước nó, `/queue/lenh-cho` lọc cứng
                         `NOT EXISTS (fls_moi_noi)` nên ⛔ không đường nào hỏi
                         *"lệnh chi nào ĐÃ có tiền"* (`GAP-API-08`).
       `tat_ca`          ⛔ **vẫn chưa có** — nó là **HỢP** của hai rổ, và gộp
                         hai cửa ở màn thì con số `x/y` sẽ do màn tự cộng,
                         tức một **số của máy** (`UI-F8`). ⇒ `GAP-SCR-26`.

     ⛔⛔ `null` ở đây ⛔ **KHÔNG** có nghĩa *"gọi không lọc"*. Nó nghĩa là
        **⛔ chưa có cửa**, và màn phải **NÓI RA** điều đó thay vì vẽ một danh
        sách rỗng — một danh sách rỗng đọc y hệt *"đã xong hết"* (`INV-I16`). */
  const CHIP_CUA = {
    chua_gan: ['ro=nguoi', 'ro=may&tu_chung=0'],
    khong_gan_duoc: ['ro=khong'],
    da_gan: ['@da-gan'],   /* ⭐ tuyến 40 — xem `_duong()` */
    tat_ca: null,          /* ⛔ HỢP của hai rổ — `GAP-SCR-26` */
  };

  /* ⚠ Cửa chặn `limit` ở **500**, mà rổ `khong` có **768** ⇒ **phải** lật
     trang, ⛔ không được lấy trang đầu rồi thôi: `lenh_ke_tiep` đi dọc
     `ST.dong`, nên một danh sách cụt sẽ **im lặng dừng** giữa chừng. */
  /* ⭐⭐ Owner `2.3`: cho chỉnh bề rộng cột lệnh chi. ⛔ Nội dung lệnh chi
     dài ngắn **rất khác nhau** giữa các rổ, nên một bề rộng chạm chết
     (`clamp(300px,26vw,380px)`) vừa cho rổ này sẽ cắt cụt rổ kia.

     ⛔ Nhưng **⛔ không tự do tuyệt đối**: một rail `120px` thì ⛔ không còn
        đọc được mã lệnh nào, và một rail `1200px` thì bàn làm việc ⛔ không
        còn chỗ cho bảy cột giao dịch. Hai đầu đều là *"màn hỏng"*. */
  const RAIL_MIN = 260;
  const RAIL_MAX = 720;

  function chan_rail(px) {
    return Math.max(RAIL_MIN, Math.min(RAIL_MAX, Math.round(px)));
  }

  const TRANG = 500;
  const TRAN_DONG = 3000;   /* ⛔ chặn vòng lật trang chạy vô tận */

  /* ⭐ Chờ **250ms** sau phím cuối rồi mới hỏi cửa. ⛔ Không chờ thì gõ
     `OPENAI` = **6** lượt gọi, và lượt về sau có thể trả lời **TRƯỚC** lượt
     về trước ⇒ danh sách nhấp nháy rồi **dừng ở kết quả của một chuỗi chữ
     đã CŨ** — sai mà trông y hệt đúng. */
  const TRE_TIM = 250;

  const ST = {
    chip: 'chua_gan',
    dong: [], het: false, con_tro: null,
    thieu_cua: false,      /* ⭐ chip này ⛔ chưa có cửa — màn phải nói ra */
    dang_tai: false, loi: null,
    mo: null,
    ung_vien: [], toan_so: false, tim: '',
    /* ⭐ `WO-045` ①: vùng ứng viên có **tải** + **lỗi** riêng — của lượt
       **mới nhất** *(`mo_lenh` / ô tìm)*, ⛔ lẫn với `dang_tai` / `loi` của
       danh sách lệnh. */
    dang_tai_uv: false, loi_uv: null,
    /* ⛔⛔⛔ `WO-023` `(i)` *(`BA-06` v4.22 `§4.5 ⓦ` ⑥ · `KQ-050 F-3`, PO nâng
       `NANG`)*: lựa chọn ứng viên là **`itl_id`** của dòng người bấm, ⛔ chỉ số
       mảng. Bản trước giữ `ung_vien_chon = i` *(chỉ số vào `ST.ung_vien`)* và
       chỉ xoá nó ở **đầu** một lượt *(`mo_lenh` · hẹn giờ ô tìm)*, ⛔ ở **cuối**
       — khi danh sách mới **thay** `ST.ung_vien`. Trong khoảng ấy danh sách cũ
       vẫn trên màn, bấm được ⇒ người bấm hàng `k` của danh sách **cũ**, lượt
       mới về, `k` trỏ một dòng tiền **khác**: màn tô sẵn dòng ấy và `Gán` /
       `Enter` gửi `/queue/<itl người ⛔ chọn>/match` *(bài
       `test_wo023_i_chon_ung_vien_theo_itl.py` — đỏ trên `7e67a09`: một phím
       `Enter` ghi `M2` khi người bấm `M3`; `KQ-050` ① đo cửa ghi **nhận** cặp
       trong dung sai ⇒ dòng người ⛔ chọn vào sổ **chỉ-thêm**)*.
       ⇒ Danh tính = `chon_itl`; `null` = ⛔ KHÔNG chọn sẵn (`INV-I16`). Mỗi lần
       danh sách bị thay *(`_thay_uv` — chỗ **duy nhất** ghi `ST.ung_vien` từ
       một lượt)*: `itl_id` còn ⇒ giữ *(tô đúng hàng ở vị trí mới)*, ⛔ còn ⇒
       `null`; **cả hai** ca `xac_nhan = false`. */
    chon_itl: null,
    xac_nhan: false,       /* ⭐ bước hai của ca lệch tiền */
    /* ⭐ `WO-023` `(h)` ⓐ — cú `Gán` *(khuôn `dang_bo_gan` / `loi_bo_gan`)*:
         `dang_gan` — đang chờ `/match` ⇒ nút `Gán` khoá, `Enter` ⛔ đi đâu
         `loi_gan`  — `{ma, cau, lam_gi, chi_tiet}` dòng lỗi *"Gán chưa xảy ra"* */
    dang_gan: false, loi_gan: null,
    /* ⭐ `ung_vien_chon` giờ là **phái sinh** *(chỉ số của `chon_itl` trong danh
       sách đang có, `null` nếu ⛔ có)* — ⛔ một sự thật thứ hai. Giữ tên cũ vì
       bài thử *(kể cả `tests/nghiem_thu/**` — ⛔ Dev sửa)* đọc nó, và một số
       bài **đặt** nó sau khi tự nạp `ST.ung_vien`: phép đặt chỉ số đổi thành
       đặt `itl_id` của hàng ấy. Mã màn ⛔ đọc/ghi tên này. */
    get ung_vien_chon() {
      if (this.chon_itl == null) return null;
      const i = this.ung_vien.findIndex(u => u && u.itl_id === this.chon_itl);
      return i < 0 ? null : i;
    },
    set ung_vien_chon(i) {
      const u = i == null ? null : this.ung_vien[i];
      this.chon_itl = u ? u.itl_id : null;
    },
    du_truong: false,
    dg_mo: null,           /* ⭐ ứng viên nào đang mở rộng diễn giải */
    tro: 0,
    /* ⛔⛔ Bề rộng rail phải sống ở ĐÂY, ⛔ không trong DOM: `ve()` dựng lại
       **toàn bộ** cây mỗi lần. Đặt thẳng vào phần tử thì kéo xong bấm một
       cái là **nhảy về cũ** — và người ta sẽ tưởng tay kéo hỏng. */
    rail_w: null,
    /* ⭐ Vùng `Bỏ gán` *(`WO-008` vòng 2, `BA-06` v4.10 mục ⓔ)* — sống ở `ST`
       vì `ve()` dựng lại cả cây mỗi lần:
         `dang_bo_gan` — đang chờ `/chum` hoặc `/unmatch` ⇒ nút khoá *(tải)*
         `tin_bo_gan`  — `{ma, itl, so_lenh, loi_doc}` dòng tín hiệu ca ③/④
         `loi_bo_gan`  — `{ma, cau, lam_gi, chi_tiet}` dòng lỗi ca ⑤
       Hai dòng chữ gắn với **mã lệnh**: mở lệnh khác là mất *(spec ③ⓑ)*. */
    dang_bo_gan: false, tin_bo_gan: null, loi_bo_gan: null,
  };

  /* ⭐⭐ Bộ ba trạng thái của lệnh **⛔ gán** — sau một cú bỏ gán `200`, thẻ
     đổi **tại chỗ** sang đúng bộ này *(`BA-06` v4.10 ③ⓐ)*.
     ⛔⛔ Bản gốc là `fls/repo/man_ghep.py::khuon_the_lenh` *(nhánh `itl_da_gan`
        rỗng)*. Đây là **bản thứ hai** — có chủ ý, vì màn ⛔ được tải lại cả
        danh sách chỉ để hỏi ba chữ. Hai bản lệch là lệch **im lặng** ⇒ bài
        `test_AC9_bo_ba_trang_thai_sau_bo_gan__TRUNG_khuon_the_lenh_THAT` gọi
        **hàm thật** của Python rồi so, ⛔ chép hằng vào bài. */
  const BO_BA_CHUA_GAN = {
    trang_thai: 'chua_gan', trang_thai_nhan: 'Chưa gán', trang_thai_mau: '',
  };

  /* ── phép đọc nhỏ ───────────────────────────────────────────────────── */

  const gon = t => String(t == null ? '' : t).split(/\s+/).filter(Boolean).join(' ');

  const THOAT_HTML = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
  const thoat = t => String(t == null ? '' : t)
    .replace(/[&<>"]/g, c => THOAT_HTML[c]);

  /* ⭐⭐ Tô **bằng chứng** trong diễn giải. Bộ khoá do **tầng đọc** tính
     (`man_ghep.khoa_bang_chung`) — bộ **từ rác** là một *luật nghiệp vụ*,
     ⛔ không phải một mẹo hiển thị, nên nó ⛔ không được sống trong JS.

     ⛔⛔ **THOÁT trước, TÔ sau.** `dien_giai` là chữ **từ sao kê ngân hàng**,
        tức chữ ⛔ không ai kiểm soát; ghép thẳng vào `innerHTML` là mở một
        đường chèn thẻ.

     ⭐ Quét **MỘT lượt** bằng một regex hợp nhất — tô lần lượt từng khoá sẽ
       sinh `<mark>` **lồng nhau** và HTML vỡ. Khoá đã được tầng đọc xếp
       **dài trước** để miếng dài thắng. */
  function danh_dau(chu, khoa) {
    const s = thoat(chu);
    if (!khoa || !khoa.length) return s;
    const mau = khoa.map(k => String(k).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    return s.replace(new RegExp('(' + mau.join('|') + ')', 'gi'),
                     '<mark>$&</mark>');
  }

  /* ⭐⭐⭐ Chỉ mời `đủ ↓` khi diễn giải **THẬT SỰ bị cắt** — đo `scrollHeight`
     **sau khi đã dàn trang**, ⛔ không đoán theo số ký tự: bề rộng cột đổi
     theo màn, nên một ngưỡng ký tự sẽ **sai cả hai chiều**.

     ⛔ Một lời mời hiện ra khi ⛔ không có gì để mở là một lời mời **dạy
       người ta thôi tin mọi lời mời**. */
  function soat_cat() {
    const ds = document.querySelectorAll('.cand');
    for (let i = 0; i < ds.length; i++) {
      const dg = ds[i].querySelector('.dg');
      const nut = ds[i].querySelector('.doc-du');
      if (!dg || !nut) continue;
      if (String(dg.className).indexOf('clamp') < 0) {
        nut.style.display = 'inline-block';
        continue;
      }
      nut.style.display = dg.scrollHeight > dg.clientHeight + 1
        ? 'inline-block' : 'none';
    }
  }

  /* ⭐ So tren XU *(`WO-022` §5b ⓕ)*. ⛔ Hai so tien **THIEU** ⛔ phai
     *"khop dung tien"*: ma cu `Number(null) === Number(null)` ⇒ `true` ⇒
     `Enter` gan ngay mot cap ⛔ ai biet bao nhieu tien. */
  function khop_dung_tien(lenh, uv) {
    if (!lenh || !uv) return false;
    const a = TP.xu(uv.amount), b = TP.xu(lenh.so_tien);
    /* ⭐ `WO-032`: so mã bằng **một** phép với hộp *Tìm tiền* *(`TP.ma_te` —
       `trim` + chữ hoa)*; hai mã rỗng ⛔ phải *"cùng tiền tệ"*. */
    return TP.ma_te(uv.curr) !== '' && TP.ma_te(uv.curr) === TP.ma_te(lenh.curr)
        && a !== null && a === b;
  }

  /* ⭐ `WO-032` *(§5b ⓕ)*: hai mã **cùng có** mà **khác nhau** ⇒ cửa ghi sẽ
     TỪ CHỐI *(`KhacTienTe`)*. Một bên thiếu ⇒ `false` — đó là **thiếu số**,
     ⛔ phải *"khác tiền tệ"*. */
  function khac_tien_te(lenh, uv) {
    if (!lenh || !uv) return false;
    const x = TP.ma_te(uv.curr), y = TP.ma_te(lenh.curr);
    return !!x && !!y && x !== y;
  }

  /* ⭐ `nguon` là **object** — một chuỗi đã ghép thì tầng dưới ⛔ không thể bỏ
     bớt cột khi màn hẹp, mà luật hy sinh cột đòi đúng điều đó. */
  function ve_nguon(n) {
    if (!n) return KHONG_CO;
    return [n.bank, n.tk, n.le].filter(Boolean).join(' · ');
  }

  /* ── ba hàm dựng nhỏ — dùng ĐÚNG `TP.el(the_gi, lop, html)` ─────────── */

  function o(the_gi, lop, chu) {
    const e = TP.el(the_gi, lop);
    if (chu !== undefined && chu !== null) e.textContent = String(chu);
    return e;
  }

  function fact(nhan, gt) {
    const e = TP.el('div', 'fact');
    e.appendChild(o('span', 'l', nhan));
    const vang = gt == null || gt === '';
    e.appendChild(o('span', 'v' + (vang ? ' vang' : ''), vang ? KHONG_CO : gt));
    return e;
  }

  function nut(lop, nhan, ham, tat) {
    const b = o('button', 'b ' + lop, nhan);
    b.setAttribute('type', 'button');
    if (tat) b.setAttribute('disabled', 'disabled');
    else b.addEventListener('click', ham);
    return b;
  }

  /* ── thẻ lệnh chi ──────────────────────────────────────────────────── */

  function ve_the(lenh) {
    const t = TP.el('div', 'wh');
    const d1 = TP.el('div', 'wh1');
    d1.appendChild(o('span', 'id', lenh.ma_lenh));
    d1.appendChild(o('span', 'chip ' + (lenh.trang_thai_mau || ''),
                     lenh.trang_thai_nhan));
    d1.appendChild(o('span', 'chip pt', lenh.loai_phieu));
    d1.appendChild(o('span', 'nd', gon(lenh.noi_dung)));
    d1.appendChild(o('span', 'tien', TP.tien(lenh.so_tien, lenh.curr) + ' '
                                     + lenh.curr));
    t.appendChild(d1);

    const g = TP.el('div', 'wh2');
    [['Người nhận', lenh.nguoi_nhan], ['Số chứng từ', lenh.so_chung_tu],
     ['Pháp nhân', lenh.phap_nhan], ['Ngân hàng', lenh.ngan_hang],
     ['Tài khoản', lenh.tai_khoan], ['Chủ dự toán', lenh.cdt]]
      .forEach(x => g.appendChild(fact(x[0], x[1])));
    t.appendChild(g);

    t.appendChild(nut('wide', ST.du_truong ? '▾ Ẩn bớt trường'
                                           : '▸ Xem đủ trường',
      () => { ST.du_truong = !ST.du_truong; ve(); }));
    if (ST.du_truong) t.appendChild(ve_du_truong(lenh));
    return t;
  }

  /* ⭐⭐ Khối *"Xem đủ trường"* — phục vụ **niềm tin vào dữ liệu**, ⛔ không
     phục vụ việc ghép (`QĐ-ITL-144 ⓐ`; owner xác nhận giữ tại chỗ 21/09).

     ⛔⛔ **Vì thế nó ⛔ KHÔNG được giấu trường vắng.** Bản dựng bỏ qua hàng khi
        giá trị rỗng ⇒ trường vắng biến mất ⛔ không một chữ nào — ở đúng nơi
        sinh ra để yên tâm về dữ liệu, *"FLS ⛔ chưa đọc"* và *"dòng này
        ⛔ không có"* thành **y hệt nhau** (`INV-I16`).
     ⭐ Đo `21/09`: **"có khoá" ≡ "có chữ"** ở cả `27` khoá ⇒ ⛔ không có ca
       *chuỗi rỗng*: chỉ cần phân biệt **VẮNG** với **CÓ**. */
  function ve_du_truong(lenh) {
    const k = TP.el('div', 'more');
    /* ⭐⭐ Owner `23/09`: khoi nay **chiem het man** ⇒ ⛔ khong con nhin thay
       danh sach giao dich. Nay no **NOI LEN TREN** — dong lai la moi thu ve
       dung cho cu, ⛔ khong mot pixel nao dich.
       ⛔ Mot lop phu ⛔ KHONG co duong ra la mot cai bay (`INV-I20`): `Esc`
         la duong ra cua nguoi **biet** no ton tai, nen phai co mot nut. */
    k.setAttribute('role', 'dialog');
    k.setAttribute('aria-label', 'Đủ trường của lệnh ' + lenh.ma_lenh);
    const x = o('button', 'dong', '✕');
    x.setAttribute('type', 'button');
    x.setAttribute('aria-label', 'Đóng khối đủ trường');
    x.addEventListener('click', () => { ST.du_truong = false; ve(); });
    k.appendChild(x);
    /* ⭐⭐ Owner `23/09`: *"layout như wireframe"*. ⛔ Bản `22/09` xếp **dọc**
       — `h4`, `dl`, `h4`, `dl`… ⇒ bấm *"Xem đủ trường"* là đẩy toàn bộ phần
       dưới màn xuống gần **một màn hình**, và người ta mất dấu vết chỗ mình
       đang làm. Bản dựng xếp chúng **cạnh nhau**.

       ⛔⛔ Mỗi nhóm phải nằm trong **một khối con riêng**: nếu `h4` và `dl`
          là anh em rời nhau trong lưới, `auto-fit` sẽ đặt **tên nhóm ở cột
          này, giá trị ở cột kia** — và cái nhãn sai đó trông hoàn toàn bình
          thường. */
    const cot = TP.el('div', 'cols');
    (lenh.nhom_du_truong || []).forEach(nh => {
      const khoi = TP.el('div', null);
      khoi.appendChild(o('h4', null, nh.ten));
      const dl = TP.el('dl', 'kv');
      nh.o.forEach(x => {
        dl.appendChild(o('dt', null, x[0]));
        const vang = x[1] == null || x[1] === '';
        dl.appendChild(o('dd', vang ? 'vang' : null, vang ? KHONG_CO : x[1]));
      });
      khoi.appendChild(dl);
      cot.appendChild(khoi);
    });
    k.appendChild(cot);
    return k;
  }

  /* ── ⭐⭐⭐ `C4` · KHỐI ĐANG GÁN ────────────────────────────────────────
     Owner `23/09`: *"tôi muốn các PM đã gán khi bấm vào có hiện thông tin
     Transaction đã map"*. Đây là **`C4`** của hợp đồng *(`BA-06 §4`)*, và
     nó **⛔ chưa bao giờ được làm**.

     ⛔⛔ Trước đó màn chỉ hiện chip `Đã gán` trên thẻ — tức nó nói *"việc
        này xong rồi"* mà ⛔ **không nói xong bằng gì**. Kế toán mở một lệnh
        đã gán ra thì thấy một danh sách `20` ứng viên **do máy đề xuất**,
        và ⛔ không một dấu hiệu nào chỉ ra dòng nào trong số đó *(hoặc dòng
        nào **ngoài** số đó)* đang được gán.

     ⭐ Nền `good` — đây là *"đã chốt"*. Màn đã có một luật màu cho
       *"đã chốt"* ／ *"đề xuất"* *(`§6.3`)*; bịa thêm một màu thứ ba là làm
       mọi cái cũ mất nghĩa. */
  function ve_dang_gan(lenh, g) {
    const k = TP.el('div', 'mblock');
    const h = TP.el('div', 'mh');
    h.appendChild(o('span', null, '✓ Đang gán với giao dịch'));
    /* ⛔⛔ `WO-037` *(`KQ-036 F-3`, `BA-07` v3.9 §4h ⓵ dòng `bac`)*: bậc **lạ**
       ⇒ chip in **nguyên tên** — **cùng** luật `ve_ung_vien` *(`WO-032 (d)`)*.
       ⛔ Trước: `const b = BAC[g.bac]; if (b) {…}` ⇒ bậc màn ⛔ biết **bỏ chip
       im lặng** — khối nói *"đang gán"* mà ⛔ nói gán ở mức nào. Hôm nay ⛔
       bậc lạ nào; luật là để bậc **thứ sáu** ⛔ biến mất khi cửa thêm nó.
       ⚠ Bậc **vắng** *(`loi_nguon` — khuôn ⛔ đủ)* thì ⛔ chip: ⛔ có gì để in. */
    if (g.bac != null) {
      const b = BAC[g.bac] || { k: String(g.bac), l: String(g.bac), m: '' };
      const c = o('span', 'chip ' + (b.m || ''), b.k + ' ' + b.l);
      c.setAttribute('title', b.l);
      h.appendChild(c);
    }
    h.appendChild(o('span', 'sp', ''));
    h.appendChild(nut('', 'bỏ gán', () => bo_gan(lenh), ST.dang_bo_gan));
    k.appendChild(h);

    /* ⭐ Cùng một *"bằng chứng"* thì phải **trông giống nhau** ở mọi chỗ nó
       xuất hiện — ⛔ không một kiểu ở danh sách, một kiểu ở khối đã gán. */
    const dg = TP.el('div', 'mdg');
    if (g.dien_giai) dg.innerHTML = danh_dau(gon(g.dien_giai), g.khoa_to);
    else dg.textContent = g.dien_giai_vi_sao === 'chua_noi_duoc'
      ? '⛔ chưa đọc được nội dung — cột này chưa nối được với sổ'
      : '— giao dịch này không có nội dung';
    k.appendChild(dg);

    const f = TP.el('div', 'mfoot');
    [['ngày', g.doc_date], ['nguồn', ve_nguon(g.nguon)],
     ['số CT', g.doc_no], ['số tiền', TP.tien(g.amount, g.curr) + ' ' + g.curr]]
      .forEach(x => {
        const e = TP.el('span', null);
        e.appendChild(o('span', null, x[0] + ' '));
        e.appendChild(o('b', null, x[1] || KHONG_CO));
        f.appendChild(e);
      });
    if (g.lech != null && Number(g.lech) !== 0)
      f.appendChild(o('span', 'lech', 'lệch ' + TP.tien(g.lech, g.curr) + ' '
                                     + g.curr));
    k.appendChild(f);
    return k;
  }

  /* ⭐⭐⭐ Dòng TỔNG của một chùm — và nó nói **điều mà bậc từng dòng
     ⛔ không nói được**.

     Đo `23/09` trên cửa thật, `PM00001-1`:
         `itl_da_gan = [28338, 28339]`
         `29.211.750` ＋ `40.513.971` = **`69.725.721`** ≡ số tiền lệnh

     ⇒ Chùm ấy là một phép khớp **chính xác ở TỔNG**. ⛔⛔ Nhưng `_bac` tính
       **từng dòng một**, nên cả hai đều ra `cung_tien_te` — **bậc yếu
       nhất**. Màn vẽ hai khối `④` cạnh nhau thì kế toán đọc được *"hai phép
       gán yếu"*, trong khi sự thật là *"một phép gán khớp đúng đến từng
       đồng"*.

     ⭐ Sửa **⛔ không phải ở `_bac`** — bậc của **một** dòng tiền so với
       **một** dòng lệnh vẫn đúng như thế. Sửa ở chỗ **nói ra cái mà từng
       dòng ⛔ không nói được**.

     ⛔ Và chỉ vẽ khi có **hơn một**: tổng của một số là chính nó, nên một
       dòng *"Tổng: 29.211.750"* dưới đúng con số `29.211.750` là một dòng
       ⛔ không nói gì — mà nó sẽ xuất hiện ở **`99,0%`** số lệnh. */
  /* ⭐⭐ `WO-022` §5b ⓕ: Σ va lech tren SO NGUYEN XU — khop ⇔ lech = 0.
     ⛔ Truoc: cong `Number` roi so `< 0.005` *(dung)*, nhung **in** bang ham
     cu ⇒ `Tổng … 1.235 USD — lệch 0 USD` cho mot lech `0,40`. ⚠ Mot so tien
     ⛔ doi duoc sang xu van tinh la 0 *(nhu `Number(x) || 0` cu)* — ⛔ doi
     hanh vi ngoai pham vi phieu. */
  function ve_tong_chum(lenh, ds) {
    let t = 0;
    ds.forEach(g => { t += TP.xu(g.amount) || 0; });
    const can = TP.xu(lenh.so_tien) || 0;
    const lech = t - can;
    const khop = lech === 0;
    const e = TP.el('div', 'mtong' + (khop ? ' khop' : ' lech'));
    e.appendChild(o('b', null, 'Tổng ' + ds.length + ' giao dịch: '
                               + TP.tien(TP.chuoi_xu(t), lenh.curr) + ' '
                               + lenh.curr));
    e.appendChild(o('span', null, khop
      ? ' — khớp đúng số tiền lệnh.'
      : ' — lệch ' + TP.tien(TP.chuoi_xu(Math.abs(lech)), lenh.curr) + ' '
        + lenh.curr + ' so với ' + TP.tien(lenh.so_tien, lenh.curr) + ' '
        + lenh.curr + ' của lệnh.'));
    return e;
  }

  /* ── dòng ứng viên ─────────────────────────────────────────────────── */

  function ve_ung_vien(lenh, uv, i, chi_doc) {
    /* ⛔⛔ `WO-032` *(`BA-07` v3.7 §4h ⓵ dòng `bac`)*: bậc **lạ** ⇒ in
       **nguyên tên**, ⛔ rơi về `cung_tien_te`. ⛔ Trước: `|| BAC.cung_tien_te`
       — một bậc màn ⛔ biết được trình bày thành *"cùng đơn vị tiền"*: nói dối
       **im lặng**, đúng chỗ người dựa vào để quyết gán. */
    const b = BAC[uv.bac] || { k: String(uv.bac), l: String(uv.bac), m: '' };
    /* ⭐ `WO-023` `(i)`: tô theo **`itl_id`**, ⛔ theo vị trí `i` — danh sách
       vừa bị thay thì hàng người bấm có thể đứng ở chỗ khác *(hoặc ⛔ còn)*. */
    const chon = ST.chon_itl != null && uv.itl_id === ST.chon_itl;
    const r = TP.el(chi_doc ? 'div' : 'button',
                    'cand cand-cols' + (chon ? ' chon' : '')
                    + (b.m ? ' ' + b.m : '')
                    + (ST.dg_mo === i ? ' rong' : ''));
    if (!chi_doc) r.setAttribute('type', 'button');
    if (chon) r.setAttribute('aria-current', 'true');

    r.appendChild(o('span', 'rad', ''));
    const tg = o('span', 'tg', b.k);
    tg.setAttribute('title', b.l);          /* ⭐ nghĩa nói MỘT lần */
    r.appendChild(tg);
    r.appendChild(o('span', 'mono ct', uv.doc_no || KHONG_CO));

    /* ⭐⭐⭐ Diễn giải — cột ⛔ KHÔNG BAO GIỜ bị hy sinh.
       ⛔ `null` mang **hai** nghĩa, và màn phải nói **khác nhau**. */
    let chu, lop;
    if (uv.dien_giai) { chu = gon(uv.dien_giai); lop = 'dg'; }
    else if (uv.dien_giai_vi_sao === 'chua_noi_duoc') {
      chu = '⛔ chưa đọc được nội dung — cột này chưa nối được với sổ';
      lop = 'dg chua_doc';
    } else { chu = '— giao dịch này không có nội dung'; lop = 'dg trong'; }
    const mo_rong = ST.dg_mo === i;
    const boc = TP.el('div', 'dgw');
    const dg = TP.el('div', lop + (mo_rong ? '' : ' clamp'));
    /* ⭐ Chỉ diễn giải THẬT mới đi qua `danh_dau`. Hai câu kia là chữ **của
       màn**, ⛔ không phải chữ của sổ — tô bằng chứng lên chúng là vô nghĩa. */
    if (uv.dien_giai) dg.innerHTML = danh_dau(chu, uv.khoa_to);
    else dg.textContent = chu;
    dg.setAttribute('title', chu);
    boc.appendChild(dg);

    /* ⛔⛔⛔ `span`, ⛔ **KHÔNG** `button`: `.cand` **đã là** một `<button>`,
       và **nút lồng nút là HTML ⛔ không hợp lệ** — trình duyệt thật ⛔ không
       xử lý được nút trong. ⚠ Và DOM giả thì cho chạy **ngon lành**, nên chỗ
       này **⛔ không thể** đo bằng một bài chạy; nó được đo bằng
       `test_KHONG_co_NUT_nao_nam_TRONG_mot_NUT` — một phép đọc mã.
       ⭐ `role` ＋ `tabindex` giữ lại phần trợ năng mà thẻ `button` vốn cho. */
    /* ⛔⛔ Ten lop `doc-du`, ⛔ **KHONG** `mo`: `.mrow.mo` DA mang nghia
       *"dong so dang MO"*. Hai nghia khac han dung chung mot ten lop thi
       `querySelectorAll('.mo')` tra **ca hai**, va mot bai thu se lang le do
       nham phan tu — da vap dung o day. */
    const nut_mo = o('span', 'doc-du', mo_rong ? 'thu gọn ↑' : 'đủ ↓');
    nut_mo.setAttribute('role', 'button');
    nut_mo.setAttribute('tabindex', '0');
    nut_mo.dataset.mo = String(i);
    boc.appendChild(nut_mo);
    r.appendChild(boc);

    r.appendChild(o('span', 'mono ngay', uv.doc_date || ''));
    r.appendChild(o('span', 'mono nguon', ve_nguon(uv.nguon)));
    /* ⭐⭐⭐ Huy hiệu `Δ` **đã bỏ**. Đo `23/09` trên `1.761` ứng viên máy
       đề xuất — ánh xạ **một-một** với bậc:

         bậc `cung_tien_te` ④ → Δ **khác 0**   `1.664`
         bậc `ma`           ① → Δ **vắng**       `51`
         bậc `tien`         ② → Δ **= 0**        `46`

       ⇒ `Δ` là một **hàm của bậc**: ⛔ **không một chút tin nào mới**
         (`UI-F9` — một sự thật, một chỗ hiện). Và nó có mặt ở **97,1%**
         dòng, tức ⛔ **không còn là một dấu hiệu** — *một báo động chỉ đáng
         giá bằng độ HIẾM của nó*.
       ⛔⛔ Cái giá: `34px` giữ chỗ trên **mọi** dòng ＋ tới `90px` khi hiện
          (`Δ 1550304.54`) — lấy đúng của cột **Số tiền** và **Nguồn** mà kế
          toán phải đọc; ảnh chụp `23/09` cho thấy `15.000.000…` bị cắt.
          Và `1550304.54` là **khuôn của máy** *(⛔ không dấu phân cách)* lọt
          lên màn của người (`UI-F8`).
       ⭐ Con số ấy ⛔ **không bị vứt** — nó chuyển sang đúng lúc nó **đổi
         một quyết định**: câu xác nhận khi người ta chọn một ứng viên lệch. */
    const p = TP.el('span', 'amt');
    /* ⭐ `WO-032` (f) *(`BA-06` v4.14 §5b ⓘ, `KQ-029 F-3`)*: ô có `ellipsis`
       thì **phải** có `title` = đúng chuỗi in — lưới an toàn khi chuỗi vượt
       ngân sách *(hôm nay **0** dòng)*; ⛔ bao giờ cắt **im lặng**. */
    const chu_tien = TP.tien(uv.amount, uv.curr) + ' ' + uv.curr;
    const o_tien = o('span', null, chu_tien);
    o_tien.setAttribute('title', chu_tien);
    p.appendChild(o_tien);
    p.appendChild(o('small', 'chieu', uv.chieu === 'no' ? 'Nợ' : 'Có'));
    r.appendChild(p);

    if (!chi_doc) r.addEventListener('click', e => {
      /* ⭐ Một cú bấm vào `đủ ↓` là một cú bấm vào **nút ngoài** — uỷ quyền
         qua `closest`, đúng khuôn bản dựng. ⛔⛔ Và nó **⛔ KHÔNG** được kéo
         theo đổi ứng viên đang chọn: *"cho tôi đọc hết câu này"* và *"tôi
         chọn dòng này"* là **hai ý định khác nhau**. */
      if (e && e.target && e.target.closest && e.target.closest('[data-mo]')) {
        ST.dg_mo = ST.dg_mo === i ? null : i;
        ve();
        return;
      }
      /* ⭐ Bấm lại = bỏ chọn, và **xoá cả trạng thái xác nhận đang chờ** —
         ⛔ không để một cú xác nhận trôi sang ứng viên khác. */
      ST.chon_itl = chon ? null : uv.itl_id;
      ST.xac_nhan = false;
      ve();
    });
    return r;
  }

  /* ⭐⭐ Owner `2.4`. Trước `23/09`, **bảy** cột ⛔ không một cái tên nào:
     `CT88210` là số chứng từ hay mã gì? `18/09/2026` là ngày giao dịch hay
     ngày nạp? `OCBC · ••4001 · SGO2` là cái gì? Kế toán **đoán** — và đoán
     thì có lúc đoán sai, ở đúng chỗ ⛔ không được phép sai.

     ⛔⛔ Hàng tiêu đề mang **đúng lớp lưới** `cand-cols` của dòng. Một lưới
        khai riêng cho tiêu đề là **bản sự thật thứ hai** về *"bảng này có
        mấy cột"*, và khi hai bản lệch thì **mọi nhãn đọc sang cột bên
        cạnh** — một lỗi đọc rất thuyết phục vì nó ⛔ không trông như lỗi.
     ⭐ Ô đầu để trống: nó là cột `.rad` *(nút chọn)*, ⛔ không có tên. */
  /* ⭐ Ô tiêu đề mang **cùng lớp** với ô dữ liệu *(`ct` · `ngay` · `nguon`)*
     — luật hy sinh cột phải giấu **cả hai** cùng lúc. Giấu ô dữ liệu mà để
     lại tiêu đề là cách chắc chắn nhất để **mọi nhãn đọc sang cột bên**. */
  const TEN_COT_GD = [
    ['', ''], ['tg', 'Bậc'], ['ct', 'Số CT'], ['', 'Diễn giải sao kê'],
    ['ngay', 'Ngày'], ['nguon', 'Nguồn'], ['r', 'Số tiền'],
  ];

  function ve_dau_gd() {
    const h = TP.el('div', 'chead cand-cols');
    TEN_COT_GD.forEach(c => h.appendChild(o('div', c[0] || null, c[1])));
    return h;
  }

  /* ⭐⭐ Chú giải bậc — `WO-032` vòng 2 `(j)` *(`BA-06` v4.15 §4.5 ⓒ ①,
     `TL-033 ⓑ`)*. Quyết ① nói nghĩa bậc ở *"chú giải ＋ `title`"* từ 21/09,
     và chú giải **⛔ bao giờ được dựng** *(grep `tlegend` ở `fls/web/` +
     `tests/web/` **0**; bản dựng đã duyệt `fls-gan-lenh-chi_10.html:739`
     **có**)* ⇒ **cả năm** ký hiệu `①②③④≠` chỉ đọc được bằng **di chuột** —
     trái quyết ② *("⛔ tooltip ⛔ được là lối duy nhất")*.

     ⛔⛔ Chữ **sinh từ `BAC`**, ⛔ gõ tay: bản dựng gõ tay **bốn** mục — đúng
        lúc `WO-032` thêm mục thứ năm `≠`. Một chú giải gõ tay là **bản sự
        thật thứ hai** về *"có những bậc nào"*, và nó **thiếu im lặng** đúng
        ở bậc mới nhất — bậc người đọc chưa quen nhất.
     ⭐ Duyệt `Object.keys(BAC)` *(⛔ `THU_TU_BAC`)*: một mục có trong `BAC` mà
       quên thêm vào `THU_TU_BAC` vẫn hiện — chú giải nói về **cái màn có thể
       vẽ** *(`ve_ung_vien` tra `BAC`)*, ⛔ về một danh sách thứ tự.
     ⛔ Chữ nằm trong **`textContent`** *(⛔ chỉ `title`)*. Mỗi mục `nowrap`,
       khe giữa các mục được xuống dòng ⇒ khung hẹp thì **gãy dòng**, ⛔ cắt
       *(`AC-13`: ⛔ bị cắt)*. */
  function ve_chu_giai() {
    const c = TP.el('div', 'tlegend');
    Object.keys(BAC).forEach((ten, i) => {
      if (i) c.appendChild(o('span', null, ' · '));
      const m = TP.el('span', null);
      m.appendChild(o('b', null, BAC[ten].k));
      m.appendChild(o('span', null, ' ' + BAC[ten].l));
      c.appendChild(m);
    });
    return c;
  }

  /* ── thanh hành động ───────────────────────────────────────────────── */

  /* ⭐ `WO-023` `(i)` *(`ⓦ` ⑥ hàng `gan` / `Enter` / `ve_thanh`)*: dòng đang
     chọn **tìm theo `itl_id`** trong danh sách đang có; ⛔ thấy ⇒ `null` ⇒
     **0** `POST`, ⛔ đoán. Ba nơi đọc *(`ve_thanh` · `gan` · `Enter`)* đi qua
     **một** hàm — ⛔ ba bản của cùng một phép tra. */
  function _uv_chon() {
    if (ST.chon_itl == null) return null;
    return ST.ung_vien.find(u => u && u.itl_id === ST.chon_itl) || null;
  }

  /* ⭐ `WO-023` `(i)`: chỗ **duy nhất** một lượt *(mới nhất)* ghi danh sách
     ứng viên. `itl_id` đang chọn **còn** ⇒ giữ; ⛔ còn ⇒ `null`. `xac_nhan`
     **luôn** về `false` — cú xác nhận là của một danh sách người **đã nhìn**;
     danh sách đổi ⇒ bấm lại hai lần *(`ⓦ` ⑥)*. */
  function _thay_uv(ds) {
    ST.ung_vien = ds;
    if (ST.chon_itl != null && !ds.some(u => u && u.itl_id === ST.chon_itl))
      ST.chon_itl = null;
    ST.xac_nhan = false;
  }

  function ve_thanh(lenh) {
    const uv = _uv_chon();
    const dung = khop_dung_tien(lenh, uv);
    const da_gan = lenh.trang_thai === 'da_gan';
    const t = TP.el('div', 'act' + (uv && !dung ? ' lech' : ''));

    /* ⭐⭐ Đây là chỗ độ lệch **đổi một quyết định** — và là chỗ duy nhất.
       Trên từng dòng nó là `97,1%` tiếng ồn; ở đây nó là câu hỏi thật:
       *"anh có thật sự muốn gán một dòng lệch bằng này ⛔ không"*. */
    /* ⭐⭐ `WO-032` *(§5b ⓕ · `BA-07` v3.7)*: cửa nay trả `lech` ở **mọi**
       bậc khi cùng tiền tệ ⇒ *"(lệch …)"* hiện cả ở bậc `ma` *(trước: bậc
       `ma` luôn `null` ⇒ nhãn mất phần lệch ở **338 / 448** ứng viên sổ
       thật)*. Khác tiền tệ ⇒ ⛔ một *"(lệch …)"* — hai đơn vị ⛔ trừ nhau. */
    const khac = khac_tien_te(lenh, uv);
    const lech = khac ? ' (khác tiền tệ — cửa ghi sẽ từ chối)'
      : uv && uv.lech != null && Number(uv.lech) !== 0
        ? ' (lệch ' + TP.tien(uv.lech, uv.curr) + ' ' + uv.curr + ')' : '';
    const nhan = ST.xac_nhan && uv
      ? 'Xác nhận gán ' + TP.tien(uv.amount, uv.curr) + ' ' + uv.curr + lech
        + ' ?'
      : (da_gan ? 'Đổi sang giao dịch đã chọn' : 'Gán');
    /* ⭐ `WO-023` `(h)` ⓐ: khoá cả khi cú `Gán` trước còn chờ cửa *(lớp
       "bấm GHI hai lần" — `ⓦ` ① đoạn ⛔ Ngoài, #4 `BG-044` `(d)`)*. */
    t.appendChild(nut(uv && !dung ? 'warn' : 'chinh', nhan,
                      () => gan(lenh), !uv || ST.dang_gan));
    if (ST.xac_nhan)
      t.appendChild(nut('', 'Huỷ', () => { ST.xac_nhan = false; ve(); }));
    if (da_gan) t.appendChild(nut('', 'Bỏ gán', () => bo_gan(lenh),
                                  ST.dang_bo_gan));

    /* ⭐⭐ Câu gợi ý nói **thẳng** rằng `Enter` ⛔ không gán — ⛔ không để người
       dùng tự phát hiện bằng cách bấm rồi ⛔ không thấy gì xảy ra. */
    t.appendChild(o('span', 'goi',
      !uv ? 'Chọn một giao dịch bên trên.'
      : dung ? 'Khớp đúng số tiền — Enter để gán.'
      : khac ? 'Khác tiền tệ — cửa ghi sẽ từ chối cặp này.'
             : 'Số tiền lệch — bấm hai lần để xác nhận, Enter không gán.'));
    ve_dong_gan(lenh, t);
    ve_dong_bo_gan(lenh, t);
    return t;
  }

  /* ⭐ `WO-023` `(h)` ⓐ — dòng lỗi của cú `Gán`, **đúng khuôn** ca ⑤ `Bỏ gán`
     *(`ve_dong_bo_gan` — chữ đậm `<tiền tố> — Cửa lỗi: <cau>` ＋ `lam_gi` ＋
     `chi_tiet` đơn cách)*. Thuộc về **một** lệnh — mở lệnh khác là mất. */
  function ve_dong_gan(lenh, t) {
    const loi = ST.loi_gan;
    if (!loi || loi.ma !== lenh.ma_lenh) return;
    const d = TP.el('div', 'note crit');
    d.setAttribute('style', 'flex:1 1 100%;margin:0');
    /* ⭐ `WO-023` `(c)` — `ⓕ3` *"⛔ được nói chưa xảy ra"* áp **mọi** lượt
       ghi; spec chỉ ghi chữ cho `Bỏ gán` ⇒ `Gán` dùng **cùng khuôn**
       *(`HOI-056` `KHONG_CHAN` — `fls-ba` xác nhận chữ)*. */
    d.appendChild(o('b', null, (loi.ma_loi === 'FLS-HET-GIO'
      ? 'Chưa rõ gán đã xảy ra chưa — ' : 'Gán chưa xảy ra — ')
      + 'Cửa lỗi: ' + loi.cau));
    if (loi.lam_gi) d.appendChild(o('div', null, loi.lam_gi));
    if (loi.chi_tiet) {
      const c = o('div', 'mono', loi.chi_tiet);
      c.setAttribute('style', 'font-size:11px;margin-top:5px');
      d.appendChild(c);
    }
    t.appendChild(d);
  }

  /* ── ba đường ra (`INV-I20`) — ⚰ ⛔ KHÔNG có `Xong` ─────────────────── */

  /* ⭐⭐⭐ `WO-023` `(h)` ⓐ *(`BA-06` v4.21 `§4.5 ⓦ` ⑤ ⓐ — `TL-049`, `BG-048`
     `AC-11`)*. Bản trước `await FLS.ghi(…)` ⛔ `try` và `nut()` gắn `click`
     thẳng ⇒ cửa ghi trả `422` *(cả hai cú `POST` của hai lượt Chrome
     `BG-048`)* ⇒ `Uncaught (in promise) LoiCua`, màn **⛔ một chữ**: nút `Gán`
     vẫn đó, người ⛔ biết lệnh **chưa** gán — đúng lỗ `F-3` của `bo_gan` đã vá
     ở `WO-008` vòng 2. Và nút ⛔ khoá trong lúc chờ ⇒ bấm ba lần là **ba**
     `POST` *(bài `test_wo023_h_…TREO` — đỏ trên `bc5e0bc`: 4 `POST`)*.
     ⇒ Luật: **`gan` ⛔ bao giờ ném.** Khuôn ca ⑤ `Bỏ gán`: dòng lỗi trong khối
       hành động `Gán chưa xảy ra — Cửa lỗi: <e.cau>` ＋ `e.lam_gi`; cờ
       `ST.dang_gan` sống ở `ST` *(⛔ ở nút — `ve()` dựng lại cả cây)*. ⛔ Tự
       thử lại *(`WO-023` `(c)`: ghi ⛔ biết kết quả = có thể ghi hai lần)*.
     ⚠ Ghi **xong** rồi mới đọc lệnh kế *(`lenh_ke_tiep` → `mo_lenh`)*: lượt
       đọc ấy lỗi thì vùng ứng viên **đã** nói *(`ⓦ` ④)* — ⛔ được báo *"Gán
       chưa xảy ra"* cho một cú gán **đã** vào sổ *(cùng lớp `KQ-019 F-4`)*. */
  async function gan(lenh) {
    if (ST.dang_gan) return;
    const uv = _uv_chon();
    if (!uv) return;
    /* ⭐⭐ Ca lệch tiền: **lần một ⛔ KHÔNG ghi**. */
    if (!khop_dung_tien(lenh, uv) && !ST.xac_nhan) {
      ST.xac_nhan = true; ve(); return;
    }
    ST.dang_gan = true; ST.loi_gan = null;
    ve();                                   /* ⭐ vẽ NGAY: nút khoá */
    try {
      await FLS.ghi('/queue/' + uv.itl_id + '/match',
                    { pm_line_ids: [lenh.ma_lenh] });
    } catch (e) {
      ST.dang_gan = false;
      ST.loi_gan = {
        ma: lenh.ma_lenh,
        ma_loi: (e && e.ma) || '',
        cau: (e && (e.cau || e.message)) || String(e),
        lam_gi: (e && e.lam_gi) || '',
        chi_tiet: (e && e.chi_tiet) || '',
      };
      ve();
      return;
    }
    ST.dang_gan = false;
    ST.xac_nhan = false; ST.chon_itl = null;
    await _nguoi_mo(lenh_ke_tiep(lenh.ma_lenh));
  }

  /* ⭐ `WO-023` `(h)` ⓑ *(`ⓦ` ⑤ ⓑ)*: lượt `mo_lenh` do **người** khởi
     *(phím · chuột · ô tìm · gán xong sang lệnh kế)* ⛔ được để lỗi rơi ra
     console. `mo_lenh` **vẫn ném** — `bo_gan` đọc lỗi ấy *("Chưa tải lại được
     giao dịch gợi ý")*. Ở đây: lỗi là của lượt **mới nhất** *(`mo_lenh` lượt
     cũ ⛔ ném)* ⇒ màn **phải** nói nó. `mo_lenh` đổi lệnh đã tự in *(danh
     sách rỗng)*; mở lại **cùng** lệnh thì danh sách cũ còn ⇒ in ở đây —
     ⛔ để danh sách cũ đứng im như thể lượt đã thành. */
  async function _nguoi_mo(p) {
    try { await p; }
    catch (e) {
      if (!ST.loi_uv) { _loi_uv(e); ve(); }
    }
  }

  /* ⭐ `WO-023` `(h)` ⓒ *(`ⓦ` ④ hàng **lỗi**)*: nút `Thử lại` chạy lại
     **đúng** lượt vừa lỗi — ô tìm rỗng ⇒ `mo_lenh(ST.mo)`; có chữ ⇒ tra lại
     **chữ ấy** *(⛔ xoá chữ người đã gõ)*. Một lượt mới theo `ⓥ` *(bộ đếm
     `_luot_uv`)*. */
  function thu_lai_uv() {
    if (!ST.mo) return;
    if (ST.tim) {
      ST.loi_uv = null; ST.dang_tai_uv = true; ve();
      return _luot_chu();
    }
    return _nguoi_mo(mo_lenh(ST.mo));
  }

  /* ⭐ `WO-023` `(h)` ⓔ *(`KQ-050 F-2`)*: một lượt **chữ** *(ô tìm · `Thử
     lại`)*. Lỗi của lượt mới nhất đã được `_tai_toan_so` đặt lên màn
     *(`_loi_uv`)* ⇒ ở đây chỉ vẽ — ⛔ ném tiếp vào trình nghe
     `setTimeout(async …)` *(⛔ ai bắt ⇒ `Uncaught`)*. */
  async function _luot_chu() {
    try { if (await tai_toan_so(ST.mo)) ve(); }
    catch (e) { ve(); }
  }

  /* ⭐⭐ Bỏ gán — cửa `unmatch` bỏ **TOÀN BỘ** mối nối của dòng tiền
     (`QĐ-ITL-69`), nên ở ca có **chùm** màn phải **liệt kê tên** trước.
     ⛔⛔ Và **chỉ** ở ca ấy: đo được **25/2.222 = 1,1%**. Hỏi cả `2.222` lần
        để đúng `25` lần là cách nhanh nhất **dạy người ta bấm OK ⛔ không
        đọc** — khi ấy nó ⛔ không còn cản được gì ở đúng `25` lần cần cản.

     ⭐⭐⭐ `WO-008` **vòng 2** *(`BA-06` v4.10 mục ⓔ — NĂM ca, `KQ-019`
       `F-1`…`F-4`)*. Hàm này từng có **bốn** lỗ, cả bốn đo trên máy `8099`:
       ⓐ `F-1` — hai nhánh hộp gọi hàm `hoi` của `HT` — một hàm `hop_thoai.js`
         **⛔ bao giờ xuất** *(nó trả đúng `{ mo, dong, loi_trong_hop }`)* ⇒
         bỏ gán chùm / đa giao dịch chết ở `TypeError` — **0** hộp, **0**
         lượt `/unmatch`. Sống được từ `45a79e0` vì **mọi** bài màn tự định
         nghĩa hàm `hoi` ấy trong bẫy *(`11` §6 — khuôn thử tự nhét che chỗ thiếu)*.
         ⇒ Cả hai hộp dựng bằng **`HT.mo`**, ⛔ thêm hàm hộp nào: một lớp hộp
           thứ hai phải qua lại ba luật ⓐⓑⓒ của `hop_thoai.js`.
       ⓑ `F-2` — sau `200` chỉ `mo_lenh` ⇒ `ST.dong` ⛔ đổi ⇒ thẻ vẫn
         `Đã gán`, khối *"✓ Đang gán với giao dịch"* còn nguyên, bấm lại ⇒
         `409` im lặng. Với `bo_qua` rỗng *(02/10: **100%** cú bỏ gán —
         `fls_sua_tay` **0**)* người bấm **⛔ một tín hiệu nào**.
       ⓒ `F-3` — `FLS.ghi` ném ⇒ lỗi rơi ra trình nghe `click` *(`nut()`
         ⛔ bọc)* ⇒ `Uncaught (in promise) LoiCua`, màn ⛔ một chữ.
       ⓓ `F-4` — `await mo_lenh` đứng **trước** hộp `bo_qua` ⇒ đọc lại ứng
         viên lỗi là hộp ⛔ mở, dù sổ **đã** ghi.
     ⇒ Luật của bản này: **`bo_gan` ⛔ bao giờ ném.** Mọi lỗi đi thành chữ
       trên màn *(ngoài hộp: `ST.loi_bo_gan` — ca ⑤; trong hộp:
       `HT.loi_trong_hop` — ca ②)*. Và mọi thứ màn **phải nói** sau `200`
       xảy ra **trước** lượt đọc lại *(ca ④)*. */
  async function bo_gan(lenh) {
    /* ⛔⛔⛔ Bản trước đọc `lenh.itl_id_da_gan` — một khoá **⛔ KHÔNG AI SINH
       RA** trong cả kho ⇒ URL thành `/queue/undefined/chum`. Nó sống được vì
       nhánh *"đã gán"* **⛔ chưa bao giờ bật**: cửa duy nhất màn gọi lọc cứng
       `NOT EXISTS (fls_moi_noi)`, nên `trang_thai` vĩnh viễn `chua_gan`.
       ⇒ Một nút chết gọi một URL sai, và ⛔ không cổng nào thấy vì ⛔ không ai
         tới được nó.

       ⭐⭐ Và là **DANH SÁCH**: đo `22/09`, **23/2.219 = 1,0%** lệnh chi gắn
         **nhiều hơn một** dòng tiền. */
    const ds = lenh.itl_da_gan || [];
    if (!ds.length) return;
    /* ⭐ `AC-10` — trạng thái **tải**: một cú bỏ gán đang chờ cửa thì cú thứ
       hai **⛔ đi đâu cả**. Trước vòng 2, lượt thứ hai ra `409` im lặng
       *(`KQ-019`)*. Cờ sống ở `ST` *(⛔ ở phần tử)* vì `ve()` dựng lại cả cây:
       khoá đặt lên nút sẽ mất ở lượt vẽ kế. */
    if (ST.dang_bo_gan) return;
    ST.loi_bo_gan = null;
    if (ds.length > 1) {
      /* ── ca ① · lệnh gắn ≥ 2 dòng tiền ── hộp BÁO, **0** lượt ghi.
         ⛔ Bỏ đại một cái là **đoán thay người** (`INV-I16`). Màn nói ra
         chỗ nó ⛔ không trả lời được, và chỉ đường sang nơi trả lời được. */
      HT.mo('Lệnh này đang gắn ' + ds.length + ' giao dịch',
        '<div class="note" style="margin-top:0">FLS <b>không tự chọn hộ</b> '
        + 'bỏ giao dịch nào. Hãy bỏ gán từ màn <b>Sổ ITL</b>, nơi xem được '
        + 'từng giao dịch một.</div>',
        [['Đã hiểu', null, { pri: true }]]);
      return;
    }
    const itl = ds[0];
    ST.dang_bo_gan = true;
    ve();                                   /* ⭐ vẽ NGAY: nút khoá */
    let chum;
    try {
      chum = ((await FLS.doc('/queue/' + itl + '/chum')) || {}).data || {};
    } catch (e) {
      return _loi_bo_gan(lenh, e);          /* ca ⑤ — `/unmatch` **0** lượt */
    }
    if (chum.can_hoi) {
      /* ── ca ② · chùm ── hộp HỎI; ghi **bên trong** hàm của nút, cùng khuôn
         `F01` ⑥ `_bo_ghep`. Cửa lỗi ⇒ lỗi **trong hộp**, `return false` ⇒
         hộp **ở nguyên** *(luật ⓑ)*. `Thôi` / `Esc` / bấm ra ngoài ⇒ ⛔ làm
         gì *(luật ⓒ)*. Hộp tự khoá hàng nút trong lúc chờ ⇒ trả cờ ngay. */
      ST.dang_bo_gan = false;
      ve();
      const n = chum.so_dong;
      HT.mo('Bỏ gán sẽ gỡ CẢ ' + n + ' lệnh chi',
        '<div class="note warn" style="margin-top:0">Giao dịch <span '
        + 'class="mono">#' + TP.chu(itl) + '</span> đang gắn <b>' + n
        + '</b> lệnh chi. Cửa bỏ gán gỡ <b>cả chùm</b>, không gỡ lẻ:</div>'
        + '<div class="note mono">'
        + (chum.dong_lenh || []).map(d => TP.chu(d.pm_line_id) + ' — '
            + TP.tien(d.amount, d.curr) + ' ' + TP.chu(d.curr)).join('<br>')
        + '</div>'
        + '<div class="note ok">Sổ giữ nguyên lịch sử; gán lại được.</div>',
        [['Thôi', null],
         ['Gỡ cả ' + n, async function () {
           let kq;
           try {
             kq = await FLS.ghi('/queue/' + itl + '/unmatch', {});
           } catch (e) { HT.loi_trong_hop(e); return false; }
           /* ⭐ Ca ③ chạy **SAU** khi hộp này đóng: hộp *"Đã bỏ ghép"* mở
              bằng **chính** `#scrim` — chạy trước thì `dong()` của hộp hỏi
              sẽ đóng luôn hộp báo vừa mở. */
           setTimeout(() => { _sau_bo_gan(lenh, itl, (kq && kq.data) || {}); }, 0);
         }, { danger: true }]]);
      return;
    }
    /* ── ca ③ · một dòng tiền, ⛔ chùm ── ghi ngay, ⛔ hộp hỏi. */
    let kq;
    try {
      kq = await FLS.ghi('/queue/' + itl + '/unmatch', {});
    } catch (e) {
      return _loi_bo_gan(lenh, e);          /* ca ⑤ */
    }
    ST.dang_bo_gan = false;
    await _sau_bo_gan(lenh, itl, (kq && kq.data) || {});
  }

  /* ── ca ⑤ · cửa lỗi NGOÀI hộp ── ⛔ ném, ⛔ banner `ST.loi` *(đó là lỗi
     của **danh sách**, ⛔ của một cú bấm)*. Thẻ **giữ** `Đã gán` — sổ ⛔ ghi
     gì. Ba trường đọc đúng như `HT.loi_trong_hop`: `cau` · `lam_gi` ·
     `chi_tiet`. */
  function _loi_bo_gan(lenh, e) {
    ST.dang_bo_gan = false;
    ST.loi_bo_gan = {
      ma: lenh.ma_lenh,
      ma_loi: (e && e.ma) || '',
      cau: (e && (e.cau || e.message)) || String(e),
      lam_gi: (e && e.lam_gi) || '',
      chi_tiet: (e && e.chi_tiet) || '',
    };
    ve();
  }

  /* ── ca ③ (+ ④) · bỏ gán XONG ──────────────────────────────────────────
     ⓐ Thẻ đổi **tại chỗ** theo `da_bo[]` của **thân trả** — ⛔ theo `lenh`
       đang mở: ở ca chùm cửa gỡ **N** lệnh, và lệnh thứ hai cũng đang nằm
       trong `ST.dong`. ⛔ Tải lại cả danh sách *(≤ 3.000 dòng, mất chỗ đứng —
       luật giữ chỗ `§4.5 ⓣ`)*.
     ⓑ Một **dòng** tín hiệu — ⛔ hộp *(v4.8: hộp chỉ khi `bo_qua` ⛔ rỗng)*.
     ⓒ `bo_qua` ⛔ rỗng ⇒ **chính** hộp *"Đã bỏ ghép"* của `F01`.
     ⓓ Lệnh **ở yên** — ⛔ `lenh_ke_tiep`.
     ⭐ Rồi **mới** đọc lại ứng viên; lượt đọc lỗi ⇒ thêm một dòng, ⛔ nói
       *"bỏ gán lỗi"* — sổ **đã** ghi *(ca ④, `KQ-019 F-4`)*. */
  async function _sau_bo_gan(lenh, itl, than) {
    ST.dang_bo_gan = false;
    const bo = new Set((than.da_bo || []).map(x => x.pm_line_id));
    ST.dong.forEach(d => {
      if (!bo.has(d.ma_lenh)) return;
      d.itl_da_gan = (d.itl_da_gan || []).filter(i => i !== itl);
      if (d.gd_ds) d.gd_ds = d.gd_ds.filter(g => g.itl_id !== itl);
      if (d.gd && d.gd.itl_id === itl) d.gd = (d.gd_ds || [])[0] || null;
      if (!d.itl_da_gan.length) Object.assign(d, BO_BA_CHUA_GAN);
    });
    ST.tin_bo_gan = { ma: lenh.ma_lenh, itl: itl,
                      so_lenh: bo.size, loi_doc: null };
    ve();
    if ((than.bo_qua || []).length) F01._bao_bo_ghep(than);
    /* ⛔ Người đã rời sang lệnh khác trong lúc chờ cửa ⇒ ⛔ kéo họ về. */
    if (ST.mo !== lenh.ma_lenh) return;
    try {
      await mo_lenh(lenh.ma_lenh);
    } catch (e) {
      ST.tin_bo_gan.loi_doc = (e && (e.cau || e.message)) || String(e);
      ve();
    }
  }

  /* ⭐ Hai dòng chữ của vùng `Bỏ gán` trong khối hành động — **một** chỗ vẽ.
     ⛔ Ký hiệu: chỉ `↩` *(đã dùng ở hộp `F01`)* — `BA-06` v4.10. */
  function ve_dong_bo_gan(lenh, t) {
    const RONG = 'flex:1 1 100%;margin:0';
    const tin = ST.tin_bo_gan;
    if (tin && tin.ma === lenh.ma_lenh) {
      const d = o('div', 'note ok',
        '↩ Đã bỏ gán khỏi giao dịch #' + tin.itl + ' — lệnh về '
        + BO_BA_CHUA_GAN.trang_thai_nhan
        + (tin.so_lenh > 1 ? ' · gỡ cả ' + tin.so_lenh + ' lệnh chi' : '')
        + '. Sổ giữ lịch sử.');
      d.setAttribute('style', RONG);
      t.appendChild(d);
      if (tin.loi_doc) {
        const l = o('div', 'note warn',
          'Chưa tải lại được giao dịch gợi ý: ' + tin.loi_doc);
        l.setAttribute('style', RONG);
        t.appendChild(l);
      }
    }
    const loi = ST.loi_bo_gan;
    if (loi && loi.ma === lenh.ma_lenh) {
      const d = TP.el('div', 'note crit');
      d.setAttribute('style', RONG);
      /* ⭐ `WO-023` `(c)` *(`BA-06` v4.11 `ⓕ3`)*: hết giờ ⇒ **⛔ biết** bỏ gán
         đã xảy ra chưa *(lượt có thể đã vào sổ)* ⇒ ⛔ được nói *"chưa xảy
         ra"*. */
      d.appendChild(o('b', null, (loi.ma_loi === 'FLS-HET-GIO'
        ? 'Chưa rõ bỏ gán đã xảy ra chưa — ' : 'Bỏ gán chưa xảy ra — ')
        + 'Cửa lỗi: ' + loi.cau));
      if (loi.lam_gi) d.appendChild(o('div', null, loi.lam_gi));
      if (loi.chi_tiet) {
        const c = o('div', 'mono', loi.chi_tiet);
        c.setAttribute('style', 'font-size:11px;margin-top:5px');
        d.appendChild(c);
      }
      t.appendChild(d);
    }
  }

  async function lenh_ke_tiep(ma) {
    const i = ST.dong.findIndex(d => d.ma_lenh === ma);
    const kt = ST.dong.slice(i + 1).find(d => d.trang_thai !== 'da_gan');
    if (kt) { ST.tro = ST.dong.indexOf(kt); await mo_lenh(kt.ma_lenh); }
    else { ST.mo = null; ve(); }
  }

  /* ── tải ───────────────────────────────────────────────────────────── */

  /* ⛔⛔⛔ **Hàm này ⛔ KHÔNG hề tồn tại cho tới `22/09`** — và cả hai cổng canh
     `B3` đều **xanh** suốt thời gian ấy.

     · Cổng **quét mã** ⛔ không hỏi *"danh sách lấy từ đâu"*.
     · Cổng **chạy mã** ⛔ không thấy, vì khuôn thử **tự nhét `ST.dong`** vào
       trước khi gọi `ve()`.

     ⭐⭐ **Một khuôn thử cung cấp thứ mà bản thật phải tự đi lấy thì nó CHE
       MẤT chỗ thiếu ấy.** Đây là cùng hạng lỗi với `TP.el` tự bịa, chỉ **cao
       hơn một tầng**: lần trước khuôn thử che một API sai, lần này nó che một
       API **⛔ chưa bao giờ được gọi**. Mở trên trình duyệt thật, màn luôn
       hiện *"Hàng chờ đã sạch."* — một câu **sai** trước `1.553` dòng đang chờ.

     ⇒ Bài `test_b3_man_ghep_tu_NAP_danh_sach.py` canh đúng chỗ ấy: nó **⛔ không
       gán `ST.dong`**, nó bắt màn tự gọi cửa. */
  /* ⭐ Hai rổ nằm ở **hai tuyến**, nên một chuỗi truy vấn ⛔ không đủ để gọi
     tên đường. `@da-gan` là một **nhãn**, ⛔ không phải một bộ lọc. */
  function _duong(loc, con_tro) {
    const goc = loc === '@da-gan'
      ? '/queue/lenh-da-gan?'
      : '/queue/lenh-cho?' + loc + '&';
    return goc + 'limit=' + TRANG
         + (con_tro ? '&cursor=' + encodeURIComponent(con_tro) : '');
  }

  /* ⛔⛔⛔ `KQ-041 F-3` `NANG` *(`fls-test` 05/10, 8088 sổ thật chỉ đọc, chuột
     thật — có từ `9ed4d4a` 22/09)*: bấm chip `Đã gán` trong ~1,2 s đầu ⇒ chip
     in **`2955 dòng`** = **2.219** đã gán ＋ **736** chưa gán; bấm lại chip
     đang chọn `Chưa gán` khi đang tải ⇒ **1.472** = 736 × 2. Gốc: mỗi cú bấm mở
     một lượt và gán `ST.dong = []` **mới**, trong khi lượt cũ vẫn đang `await`
     rồi `ST.dong.push(...)` — tức `push` vào **mảng của lượt mới**. `finally`
     của lượt cũ còn tắt cờ tải giữa chừng, `catch` của nó đặt `ST.loi` dưới
     chip mới. ⛔ Bài nào thấy: cửa giả `khung_node` trả lời **ngay** — lần thứ
     tư của lớp *"khuôn thử nhanh hơn đời thật"* *(`KQ-002 F-3` cùng hàm)*.

     ⭐ Luật *(`BA-06` v4.18 `§4.5 ⓥ`)*: lượt **MỚI NHẤT** thắng. Mỗi lượt mang
       một số `_luot`; sau **mỗi** `await` lượt tự hỏi *"mình còn là lượt mới
       nhất ⛔?"* — ⛔ ⇒ bỏ đi **im lặng**: ⛔ ghi `ST.dong`, ⛔ đụng
       `ST.dang_tai` / `ST.loi` / `ST.het` / `ST.con_tro` / `ST.tro`, ⛔ xin
       trang kế tiếp. Hàng gom vào mảng **riêng của lượt** và chỉ đặt vào
       `ST.dong` **một lần**, khi lượt ấy xong mà vẫn là lượt mới nhất ⇒ một
       lượt cũ ⛔ còn đường nào chạm tới danh sách đang hiện.
     ⛔ ⛔ huỷ yêu cầu mạng *(`AbortController`)*: luật chỉ đòi kết quả cũ ⛔
       được dùng; đổi `goi_cua.js` là việc khác *(`WO-042` NGOÀI)*. Yêu cầu đang
       bay vẫn về — và bị bỏ.
     Trả `true` ⇔ lượt này thắng *(người gọi chỉ vẽ lại khi thắng)*. */
  let _luot = 0;

  async function tai_danh_sach() {
    const luot = ++_luot;
    const con_la_moi_nhat = () => luot === _luot;
    const cua = CHIP_CUA[ST.chip];
    ST.dong = []; ST.con_tro = null; ST.het = true; ST.loi = null;
    ST.thieu_cua = !cua;
    if (!cua) {                             /* ⭐ ⛔ KHÔNG gọi bừa một cửa khác */
      ST.dang_tai = false;
      return true;
    }
    ST.dang_tai = true;
    const dong = [];
    let loi = null;
    try {
      for (const loc of cua) {
        let con_tro = null;
        do {
          const d = await FLS.doc(_duong(loc, con_tro));
          if (!con_la_moi_nhat()) return false;   /* ⭐ lượt đã bị thay */
          const than = (d && d.data) || {};
          (than.rows || []).forEach(r => dong.push(the_lenh(r)));
          /* ⚠ `next_cursor` — ⛔ KHÔNG `cursor`. Bộ tài liệu từng khai nhầm
             tên này (`GAP-SPEC-02`); đọc sai một chữ ở đây ra một vòng lật
             trang **⛔ không bao giờ dừng** hoặc dừng ngay dòng 500. */
          con_tro = (d && d.meta && d.meta.next_cursor) || than.next_cursor || null;
        } while (con_tro && dong.length < TRAN_DONG);
      }
    } catch (e) {
      /* ⭐ Lỗi của một lượt đã bị thay ⛔ hiện *(`ⓥ` ①)*: người đang nhìn
         chip **khác**, câu lỗi ấy nói về một danh sách họ đã bỏ. */
      if (!con_la_moi_nhat()) return false;
      /* ⛔ Một lỗi cửa ⛔ KHÔNG được trông như *"hàng chờ đã sạch"*. */
      loi = (e && e.message) || String(e);
    }
    if (!con_la_moi_nhat()) return false;
    if (loi === null) {
      ST.dong = dong;
      ST.het = dong.length < TRAN_DONG;
    }
    ST.loi = loi;
    ST.dang_tai = false;
    ST.tro = 0;
    return true;
  }

  /* ⭐ Hàng thô từ cửa ⇒ thẻ **11 trường**.
     ⛔⛔ Phép ánh xạ THẬT nằm ở `fls/repo/man_ghep.py::khuon_the_lenh` — ở đây
        **⛔ không** được mọc thêm một bản thứ hai đọc `tho["Tên tài khoản"]`:
        đó là tên cột của Google Sheets, và nó **đã đổi** rồi. Hàm này chỉ
        nhận đúng những gì cửa đã gọi tên. */
  function the_lenh(r) {
    return r && r.the ? r.the : r;
  }

  /* ⛔⛔⛔ `KQ-002 F-3` (đo 01/10 trên máy THẬT, `WO-003 (c)`): `mo_man()` và
     `doi_chip()` gọi `ve()` **TRƯỚC** khi `tai_danh_sach()` kịp đặt
     `ST.dang_tai = true` ⇒ lượt vẽ đầu thấy `dong=[]`, `dang_tai=false` ⇒ màn
     nói *"0 dòng (⛔ đã chạm trần 3000) · Hàng chờ đã sạch."* suốt **~2,5–4 s**
     trước **736** lệnh đang chờ — và `?gia_lap=tai` nói thế **mãi mãi**. Nhánh
     `Đang hỏi sổ…` có thật nhưng ⛔ lượt vẽ nào tới được nó.
     ⭐ Vì sao bộ cũ xanh: cửa giả của `khung_node` trả lời **ngay**, nên bài chỉ
       nhìn được trạng thái **sau** tải. Bài nghiệm thu
       `test_kq002_man_ghep_dang_tai_khong_noi_da_sach.py` cho cửa **⛔ bao giờ
       trả lời** rồi nhìn màn.
     ⇒ Đặt cờ **trước** lượt vẽ đầu — và **chỉ** khi sắp hỏi một cửa có thật:
       chip ⛔ có cửa thì ⛔ có gì để tải, nó phải hiện *"⛔ chưa có cửa"*. */
  function _sap_tai() {
    ST.thieu_cua = !CHIP_CUA[ST.chip];
    ST.loi = null;                 /* ⛔ lỗi của lượt TRƯỚC ⛔ được che "đang tải" */
    ST.dang_tai = !ST.thieu_cua;
  }

  async function doi_chip(c) {
    /* ⭐ `ⓥ` ② *(`KQ-041 F-3`: 8088 **1.472** = 736 × 2, mạng **6** `GET`)*:
       bấm lại chip **đang chọn** khi lượt của nó còn đang bay ⇒ ⛔ mở lượt
       mới — **0** `GET` thêm, lượt đang chạy đi tiếp. ⚠ Chỉ khi **đang tải**:
       hết tải *(kể cả lỗi)* bấm lại chip là **tải lại** — đường thử lại của
       danh sách. */
    if (c === ST.chip && ST.dang_tai) return;
    ST.chip = c; ST.mo = null; ST.ung_vien = []; ST.chon_itl = null;
    /* ⭐ `WO-045` ①: lệnh đóng ⇒ lượt ứng viên đang bay của nó bị thay. */
    _luot_uv++; ST.dang_tai_uv = false; ST.loi_uv = null;
    _sap_tai();                /* ⭐ cờ TRƯỚC lượt vẽ đầu — `KQ-002 F-3` */
    ve();                      /* ⭐ vẽ NGAY để khung "đang tải" hiện ra */
    if (await tai_danh_sach()) ve();   /* ⭐ lượt bị thay ⛔ vẽ — `ⓥ` ① */
  }

  /* ⭐ Cửa vào của vỏ — `ung_dung.js` gọi cái này, ⛔ không gọi thẳng `ve()`:
     một màn **vẽ trước khi nạp** là một màn nói *"đã sạch"* khi nó chỉ mới
     **⛔ chưa hỏi**. */
  async function mo_man() {
    _noi_ban_phim();
    _noi_o_tim();
    /* ⭐ `ⓥ` ② ở cửa vào thứ hai *(`WO-042`)*: quay lại tab `②` khi lượt đầu
       chưa xong ⇒ `ST.dong` vẫn rỗng, điều kiện cũ `!ST.dong.length` mở thêm
       một lượt **cùng chip**. ⛔ Mở: lượt đang bay sẽ tự vẽ khi xong. */
    const can_tai = !ST.dong.length && !ST.thieu_cua && !ST.dang_tai;
    if (can_tai) _sap_tai();   /* ⭐ cờ TRƯỚC lượt vẽ đầu — `KQ-002 F-3` */
    ve();
    if (can_tai && await tai_danh_sach()) ve();
  }

  async function mo_lenh(ma) {
    /* ⛔⛔ Đổi sang một lệnh KHÁC ⇒ danh sách ứng viên là **một danh sách
       khác hẳn**. Giữ chỗ cuộn ở đây là mở ra **giữa** một danh sách mới,
       và người ta ⛔ không biết mình đang ở đâu.
       ⇒ Luật: giữ chỗ khi **vẽ lại cùng một cảnh**, về đầu khi **đổi cảnh**. */
    const goc0 = document.querySelector('#ghep-goc');
    const ds0 = goc0 && goc0.querySelector('.cands');
    if (ds0 && ST.mo !== ma) ds0.scrollTop = 0;
    /* ⭐ Dòng tín hiệu / dòng lỗi của `Bỏ gán` thuộc về **một** lệnh —
       mở lệnh khác là mất *(`BA-06` v4.10 ③ⓑ)*. Mở lại **cùng** lệnh *(lượt
       đọc lại ứng viên ngay sau bỏ gán)* thì giữ. */
    const doi = ST.mo !== ma;
    if (doi) { ST.tin_bo_gan = null; ST.loi_bo_gan = null; ST.loi_gan = null; }
    /* ⭐ `WO-023` `(i)` *(`ⓦ` ⑥ dòng cuối)*: đổi sang lệnh **khác** ⇒ bỏ chọn
       *(như nay)*. Mở lại **cùng** lệnh *(xoá ô tìm · đọc lại sau `Bỏ gán`)*
       ⇒ ⛔ bỏ ở đầu lượt: lựa chọn đi theo `itl_id` và được đối chiếu ở
       **cuối** lượt *(`_thay_uv`)* — còn thì giữ, ⛔ còn thì bỏ. */
    if (doi) ST.chon_itl = null;
    ST.mo = ma; ST.xac_nhan = false; ST.tim = '';
    const luot = ++_luot_uv;
    const sau_loi = !!ST.loi_uv;
    ST.loi_uv = null;
    /* ⛔⛔⛔ `WO-045` ① *(`BA-06` v4.19 `§4.5 ⓦ` ① — `BG-044` `(d)` #2)*: đổi
       sang lệnh **khác** ⇒ danh sách cũ là của **lệnh khác**. Bản trước giữ
       nó trong `ST.ung_vien` suốt lúc lệnh mới đang tải: `ST.mo` đã là lệnh
       mới, nên một cú bấm hàng ứng viên *(màn vẽ lại với thẻ lệnh mới ＋ danh
       sách cũ)* rồi `Gán` gửi `itl_id` của lệnh **trước** kèm `ma_lenh` của
       lệnh **đang mở** *(bài `test_AC2_GAN_luc_lenh_moi_DANG_TAI_…` — đỏ trên
       `db0adae`: `/queue/<itl lệnh A>/match {pm_line_ids: [B]}`)*. Cửa ghi
       chặn lệch tiền / khác tệ; một cặp sai **trong dung sai** thì ⛔.
       ⇒ Xoá **ngay**, bật khung *"Đang hỏi sổ…"* trong vùng ứng viên *(trạng
       thái **tải** — `WO-045` bảng Màn hình: "giữ khung chờ tới khi lượt của
       lệnh đang mở xong")*, và vẽ **ngay** để danh sách cũ rời màn. Mở lại
       **cùng** lệnh *(đọc lại sau bỏ gán · xoá ô tìm)* thì giữ danh sách —
       nó là của chính lệnh ấy. */
    if (doi || sau_loi) {
      _thay_uv([]); ST.toan_so = false; ST.dang_tai_uv = true;
      ve();
    }
    /* ⛔ `FLS.doc` tra **phong bi** `{data, meta}` — ⛔ khong tra thang than.
       Ban dau toi doc thang `d.ung_vien` va no **sai ca voi cua that**;
       chi mot bai CHAY moi lo ra. */
    try {
      const d = await FLS.doc('/queue/lenh/' + encodeURIComponent(ma)
                              + '/itl-candidates');
      /* ⭐ `ⓦ` ①: lượt **đã bị thay** *(`j`/`k`/`↓` sang lệnh khác, gõ ô
         tìm)* ⛔ ghi `ST.ung_vien`, ⛔ vẽ — lượt mới nhất thắng. */
      if (luot !== _luot_uv) return;
      _thay_uv(((d && d.data) || {}).ung_vien || []);
      /* ⭐⭐ Máy ⛔ không tìm được ứng viên nào ⇒ **bật sẵn Toàn sổ**. Màn
         ⛔ **không bao giờ** là ngõ cụt — đó là lối ra của `768` dòng. */
      ST.toan_so = ST.ung_vien.length === 0;
      if (ST.toan_so && !(await _tai_toan_so(ma, luot))) return;
    } catch (e) {
      if (luot !== _luot_uv) return;       /* ⭐ lỗi lượt cũ ⛔ hiện */
      ST.dang_tai_uv = false;
      /* Danh sách đã xoá *(đổi lệnh)* ⇒ màn phải **nói** lỗi, ⛔ để khung
         chờ treo mãi. Mở lại **cùng** lệnh ⇒ giữ như nay: danh sách cũ còn,
         người gọi *(`bo_gan` — "Chưa tải lại được giao dịch gợi ý")* nói. */
      if (ST.ung_vien.length === 0) { _loi_uv(e); ve(); }
      throw e;                             /* như nay — người gọi đọc lỗi */
    }
    ST.dang_tai_uv = false;
    ve();
  }

  /* ⭐ `WO-045` ① *(`BG-044` `(d)` #3)*: **một** bộ đếm lượt cho mọi lượt ghi
     `ST.ung_vien` — `mo_lenh` *(trục **lệnh**)* và ô tìm *(trục **chữ**)*
     cùng ghi một danh sách, nên hai trục chung một lượt: gõ chữ khi lệnh vừa
     mở chưa về ⇒ chữ thắng; `j` sang lệnh khác khi chữ còn bay ⇒ lệnh thắng.
     ⛔ Chú thích `TRE_TIM` *(`:129-132`)* đã tự nêu ca *"lượt về sau trả lời
     TRƯỚC"* — trễ 250 ms chỉ **giảm** số lượt bay, ⛔ chặn được ca người gõ,
     dừng quá 250 ms, gõ tiếp *(bài `test_AC3_o_tim_hai_chu_…` — đỏ trên
     `db0adae`: danh sách của chữ **cũ**)*. ⛔ `AbortController` *(`ⓥ`: luật
     chỉ đòi kết quả cũ ⛔ được dùng)*. */
  let _luot_uv = 0;

  function _loi_uv(e) {
    /* ⛔ Một lỗi cửa ⛔ được trông như *"Sổ không có dòng tiền nào"* *(câu
       rỗng của vùng ứng viên)* — hai trạng thái khác nhau, cùng khuôn chữ
       với danh sách `②b` *(`⛔ Cửa lỗi: <câu>`)*. Trước `WO-045` danh sách
       ⛔ bị xoá khi đổi lệnh nên lỗi chỉ ném ra trình nghe phím / bấm *(vẫn
       ném — như nay)*; nay danh sách xoá ngay ⇒ màn phải tự nói. */
    ST.dang_tai_uv = false;
    ST.loi_uv = (e && e.message) || String(e);
    /* ⭐ `WO-023` `(h)` + `(i)`: câu lỗi **thay** danh sách trên màn *(`ve`
       — `loi_uv` ⇒ ⛔ vẽ hàng)* ⇒ danh sách cũ ⛔ được sống **sau lưng** nó:
       một lựa chọn trên hàng ⛔ còn hiện mà nút `Gán` vẫn bấm được là đúng
       cái lỗ `(i)` vừa vá. Xoá ⇒ `chon_itl` `null`, `Gán` khoá; `Thử lại`
       nạp lại. */
    _thay_uv([]);
  }

  /* Trả `true` ⇔ lượt `luot` còn là lượt mới nhất *(đã ghi trạng thái)*. */
  async function _tai_toan_so(ma, luot) {
    let d;
    try {
      d = await FLS.doc('/queue/lenh/' + encodeURIComponent(ma) + '/so'
                        + (ST.tim ? '?q=' + encodeURIComponent(ST.tim) : ''));
    } catch (e) {
      if (luot !== _luot_uv) return false;   /* ⭐ lỗi lượt cũ ⛔ hiện */
      /* ⛔⛔ `WO-023` `(h)` ⓔ *(`KQ-050 F-2`)*: bản trước chỉ `throw` ⇒ lượt
         chữ mới nhất lỗi khi lệnh mới đang tải ⇒ `ST.dang_tai_uv` vẫn `true`
         ⇒ khung `Đang hỏi sổ…` **treo mãi**, ⛔ câu lỗi; lỗi rơi ra trình nghe
         `setTimeout(async …)` ⇒ `Uncaught`. Luật có sẵn *(`ⓦ` ④ hàng lỗi)*:
         lỗi lượt mới nhất ⇒ hạ khung + câu `⛔ Cửa lỗi:` + `Thử lại`. Vẫn ném
         — `mo_lenh` *(Toàn sổ tự bật)* đọc nó cho `bo_gan`. */
      _loi_uv(e);
      throw e;
    }
    if (luot !== _luot_uv) return false;
    _thay_uv(((d && d.data) || {}).ung_vien || []);
    ST.dang_tai_uv = false; ST.loi_uv = null;
    return true;
  }

  /* Cửa ngoài *(ô tìm · bài thử)*: **một lượt mới** ⇒ mọi lượt đang bay của
     `mo_lenh` / ô tìm trước đó bị thay. */
  async function tai_toan_so(ma) {
    return _tai_toan_so(ma, ++_luot_uv);
  }

  /* ── bàn phím — `NFR-I24`, đủ 9 phím ───────────────────────────────── */

  function phim(e) {
    const a = document.activeElement;
    if (a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA')) {
      if (e.key === 'Escape' && a.blur) a.blur();
      return;
    }
    if (e.key === '/') { tim_focus(); return; }
    if (!ST.mo) {
      if (e.key === 'ArrowDown') { ST.tro = Math.min(ST.tro + 1, ST.dong.length - 1); ve(); }
      else if (e.key === 'ArrowUp') { ST.tro = Math.max(ST.tro - 1, 0); ve(); }
      else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        const d = ST.dong[ST.tro]; if (d) _nguoi_mo(mo_lenh(d.ma_lenh));
      }
      return;
    }
    /* ⛔⛔ `Esc` phai boc **tung lop mot**. Neu no dong thang ca lenh thi
       mot nguoi vua mo *"Xem du truong"* de doi chieu se **mat luon dong
       lenh dang lam** chi vi muon dong mot lop phu — va ⛔ khong cach nao
       quay lai ngoai viec tim lai dong ay trong `738` dong. */
    if (e.key === 'Escape' && ST.du_truong) {
      ST.du_truong = false; ve(); return;
    }
    if (e.key === 'ArrowLeft' || e.key === 'Escape') { ST.mo = null; ve(); return; }
    if (e.key === 'ArrowDown' || e.key === 'j') { doi_lenh(1); return; }
    if (e.key === 'ArrowUp' || e.key === 'k') { doi_lenh(-1); return; }
    if (e.key === 'Enter') {
      /* ⭐⭐⭐ `Enter` **CHỈ** gán khi ứng viên khớp **đúng số tiền**.
         ⛔ `45%` ca ⛔ không có ứng viên khớp đúng tiền — ca lệch phải xác
            nhận **bằng chuột**, hai lần. `NFR-I25` · `INV-I16`. */
      const lenh = ST.dong.find(d => d.ma_lenh === ST.mo);
      const uv = _uv_chon();
      if (lenh && uv && khop_dung_tien(lenh, uv)) gan(lenh);
    }
  }

  /* ⛔⛔⛔ **`phim()` đã viết đủ 9 phím từ `21/09` và ⛔ KHÔNG AI GỌI NÓ.**

     Ba cổng đều xanh: hai cổng quét chữ thấy đủ `9` chuỗi phím; cổng **chạy
     mã** thì **tự gọi thẳng** `F01G.phim({key:'Enter'})`. ⛔ Không cổng nào
     hỏi *"ai gọi nó khi **người thật** gõ"*.

     ⭐⭐ Đây là lần thứ **ba** cùng một hình dạng: khuôn thử **với tay VÀO**
       gọi thứ mà sản phẩm phải **với tay RA** nối.

     ⭐ Theo đúng khuôn `man_f02.js::_noi_ban_phim` — một cờ, một listener
       trên `document`, và **tự chặn** khi màn ⛔ không bật. */
  let _da_noi = false;

  function _noi_ban_phim() {
    if (_da_noi) return;
    _da_noi = true;
    document.addEventListener('keydown', function (e) {
      /* ⛔⛔ Một listener trên `document` nghe phím của **MỌI** màn. Thiếu
         phép chặn này thì gõ `j` ở `F02` sẽ **đổi lệnh chi** ở một màn
         ⛔ không ai đang nhìn — nó lặng lẽ đổi trạng thái sau lưng người
         dùng. `man_f02.js` đã phải đặt đúng phép chặn này. */
      const man = document.querySelector('#man-ghep');
      if (!man || !man.classList.contains('on')) return;
      /* ⛔⛔ `WO-023` `(a)` *(`BA-06` v4.11 `ⓕ1` — `KQ-021 F-1`)*: hộp `HT`
         đang mở ⇒ phím **⛔** thuộc về màn sau lưng. Bản trước ⛔ hỏi ⇒ `Esc`
         đóng hộp **và** đóng luôn lệnh *(`ST.mo` → `null`)*; `j` đổi lệnh
         **sau lưng** hộp trong khi `Gỡ cả 2` vẫn gỡ lệnh cũ *(Chrome `8099`
         ca **I**)*. `HT.nuot_phim(e)` cũng trả `true` cho sự kiện **vừa**
         đóng hộp *(pha capture của `hop_thoai.js` chạy trước — dấu
         `_hop_thoai`)* ⇒ ⛔ phụ thuộc thứ tự đăng ký. Bài thử nạp màn ⛔ kèm
         `hop_thoai.js` ⇒ `HT` ⛔ có ⇒ như cũ. */
      if (typeof HT !== 'undefined' && HT.nuot_phim && HT.nuot_phim(e)) return;
      /* ⭐ Chặn cuộn trang cho phím **điều hướng**. ⛔ Không chặn `Enter` /
         `Escape`: chúng ⛔ không cuộn, và chặn bừa là cướp mất hành vi mặc
         định của ô nhập. */
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', '/']
          .indexOf(e.key) >= 0 && e.preventDefault) e.preventDefault();
      phim(e);
    });
  }

  let _hen_tim = null;
  let _da_noi_tim = false;

  /* ⛔⛔ `#ghep-tim` có trong vỏ từ `21/09`, và trong cả `fls/web/` nó xuất
     hiện đúng **hai** chỗ: dòng khai ở `index.html`, và `tim_focus()` nhảy
     vào nó. ⇒ Một ô nhập **⛔ không ai nghe**, nên cửa `?q=` — đã cài đầy đủ
     ở `man_ghep.py` — **⛔ chưa bao giờ nhận một chữ nào**.

     ⭐⭐ Một ô nhập **chỉ được nhảy vào mà ⛔ không được đọc** còn **tệ hơn**
       một ô ⛔ không có: nó **MỜI** người ta gõ, rồi ⛔ không làm gì cả. */
  function _noi_o_tim() {
    if (_da_noi_tim) return;
    _da_noi_tim = true;
    /* ⭐⭐ Uỷ quyền ở tầng `document`, ⛔ **không** gắn thẳng lên thẻ — đúng
       khuôn `man_f02.js` đang dùng cho mọi sự kiện của nó. Hai cái lợi thật:
         · ô tìm nằm trong vỏ tĩnh nhưng **mọi thứ khác của màn thì ⛔ không** —
           một listener trên thẻ sẽ chết theo lần `ve()` kế tiếp;
         · ⭐ và nó **đo được**: `_ban()` của DOM giả chỉ bắn tới listener ở
           tầng `document`, nên một listener gắn trên thẻ là một listener
           **⛔ không bài chạy nào chạm tới** — tức lại đúng cái bẫy tệp này
           sinh ra để chặn. */
    document.addEventListener('input', function (e) {
      const t = e && e.target;
      if (!t || t.id !== 'ghep-tim') return;
      const chu = String(t.value || '').trim();
      if (_hen_tim) clearTimeout(_hen_tim);
      _hen_tim = setTimeout(async function () {
        ST.tim = chu;
        /* ⭐⭐ Gõ chữ = **bật Toàn sổ**. Danh sách máy đề xuất tối đa `50`
           dòng và cố định, nên lọc trong nó ⛔ không trả lời được câu
           *"tiền của tôi nằm ở đâu khác"* — đúng câu khiến người ta gõ.
           ⭐ Việc này cũng trả lại **lối bật Toàn sổ bằng tay** mà hợp đồng
             `§8` đòi và màn ⛔ chưa có: `ST.toan_so` mới chỉ **TỰ** bật khi
             `ung_vien` rỗng. */
        ST.toan_so = chu !== '';
        /* ⭐ `WO-023` `(i)`: ⛔ bỏ chọn ở đầu lượt chữ — lựa chọn đi theo
           `itl_id`, đối chiếu ở cuối lượt *(`_thay_uv`)*; `xac_nhan` vẫn về
           `false` ngay *(như nay)*. */
        ST.xac_nhan = false;
        if (!ST.mo) { ve(); return; }
        /* ⭐ `WO-045` ①: lượt chữ **đã bị thay** ⛔ vẽ — `tai_toan_so` trả
           `false` *(lượt mới nhất thắng)*. `mo_lenh` tự vẽ khi nó thắng. */
        /* ⭐ `WO-023` `(h)` ⓑ ⓔ: hàm này chạy trong `setTimeout(async …)` —
           ⛔ ai bắt lời hứa của nó ⇒ mọi lỗi ném ra đây là `Uncaught`. Lỗi
           lượt mới nhất đã lên màn *(`_luot_chu` · `_nguoi_mo`)*. */
        if (chu) await _luot_chu();
        else await _nguoi_mo(mo_lenh(ST.mo));   /* ⛔ xoá hết ⇒ có đường LÙI */
      }, TRE_TIM);
    });
  }

  function tim_focus() {
    const t = document.querySelector('#ghep-tim');
    if (t && t.focus) t.focus();
  }

  function doi_lenh(b) {
    const i = Math.min(Math.max(ST.tro + b, 0), ST.dong.length - 1);
    ST.tro = i;
    /* ⭐ `WO-023` `(h)` ⓑ: phím `j`/`k`/`↓`/`↑` ⛔ `await` — lỗi lượt mới
       nhất lên màn qua `_nguoi_mo`, ⛔ rơi ra console. */
    if (ST.dong[i]) _nguoi_mo(mo_lenh(ST.dong[i].ma_lenh));
  }

  /* ── vẽ ────────────────────────────────────────────────────────────── */

  function ve_chip(dai) {
    /* ⭐ BỐN chip. Bản dựng có **ba**, và `Chưa gán` của nó gộp cả `768` dòng
       ĐÍCH CUỐI vào việc hằng ngày ⇒ mặc định `1.553` thay vì **738**. */
    CHIP.forEach(c => {
      const b = o('button', 'chip-loc' + (ST.chip === c[0] ? ' on' : ''), c[1]);
      b.setAttribute('type', 'button');
      b.setAttribute('aria-pressed', ST.chip === c[0] ? 'true' : 'false');
      /* ⚠ Chip ⛔ chưa có cửa vẫn **bấm được** — bấm vào nó phải đọc được
         *"⛔ chưa có đường hỏi"*, ⛔ không phải **⛔ không phản ứng gì**. */
      if (!CHIP_CUA[c[0]]) b.classList.add('chua_cua');
      b.addEventListener('click', () => doi_chip(c[0]));
      dai.appendChild(b);
    });
    /* ⭐ `C6` — dải số việc. ⛔ Một con số ở đây là **số dòng màn đang cầm**,
       ⛔ không phải một con số máy tự nghĩ ra (`UI-F8`). */
    if (!ST.thieu_cua && !ST.dang_tai && !ST.loi)
      dai.appendChild(o('span', 'dem', ST.dong.length + ' dòng'
        + (ST.het ? '' : ' (⛔ đã chạm trần ' + TRAN_DONG + ')')));
  }

  /* ── ⭐⭐⭐ VIEW ① · BẢNG SỔ — khi ⛔ CHƯA mở lệnh nào ─────────────────
     Hợp đồng `§4`: *"Chưa mở lệnh nào: một bảng sổ đầy đủ chiếm toàn bộ bề
     ngang. Đã mở: bảng thu về rail, phần còn lại là bàn làm việc."*

     ⛔⛔ Màn `21/09`→`22/09` **⛔ chỉ có một view** — luôn là rail ＋ bàn làm
        việc, kể cả khi ⛔ chưa chọn gì. Tức lúc mở màn, **`80%` bề ngang** là
        một câu *"Chọn một lệnh chi bên trái"*, còn danh sách thì bị nén vào
        một cột `380px` **⛔ không đủ chỗ** cho `Ngày`·`Loại`·`CDT`·`Số CT`.
     ⭐ Bảng cho người **quét** cả trăm dòng; rail cho người **đang làm một
       dòng**. Hai việc khác nhau ⇒ hai hình. */

  /* ⭐ MƯỜI MỘT cột. ⛔ Cột `→` là một **cột thật** *(20px)*, ⛔ không phải
     trang trí: nó chia bảng thành **bên lệnh chi** ＋ **bên giao dịch**, và
     đó là toàn bộ câu hỏi của màn này.

     ⛔⛔ `23/09` owner bỏ cột `Bậc` *(`12`⇒`11`)*. ⭐ Bậc **⛔ không biến mất
        khỏi màn**: nó vẫn là `①②③④` trên **từng dòng ứng viên** — đúng chỗ
        người ta **đang chọn**. Ở bảng sổ nó chiếm một cột mà ⛔ không ai
        dùng để quét: lúc quét, câu hỏi là *"dòng nào chưa xong"*,
        ⛔ không phải *"dòng này khớp ở mức nào"*. */
  const COT_BANG = [
    ['ngay', 'Ngày'], ['ma_lenh', 'Mã PM'], ['loai_phieu', 'Loại'],
    ['noi_dung', 'Nội dung'], ['cdt', 'CDT'], ['so_tien', 'Số tiền', 'mr'],
    ['trang_thai', 'Trạng thái'], ['so_chung_tu', 'Số CT'], ['mui', ''],
    ['gd', 'Giao dịch đã gán'], ['gd_tien', 'Số tiền GD', 'mr'],
  ];

  /* ⭐⭐ Ô `Giao dịch đã gán` nói **sáu** câu khác nhau, và ⛔ KHÔNG câu nào
     được trông giống câu kia (`INV-I16`):
       · đã gán      → diễn giải thật
       · đề xuất     → `đề xuất: …` ＋ nền warn
       · ⛔ không gán được → *"sổ không có số tiền này"* (crit)
       · lỗi nguồn   → *"⛔ không đọc được nguồn"*
       · ⭐ khớp mã chỉ ở tiền tệ khác → **câu `vi_sao` của cửa** *(`WO-037`)*
       · còn lại     → `— chưa chọn` (mờ) */
  function ve_o_gd(d) {
    const g = d.gd;
    const e = TP.el('div', 'mcell');
    /* ⭐⭐ `WO-037` *(`BA-06` v4.16 §4.5 câu thứ sáu · `BA-07` v3.9 §4g ⓹)*:
       lệnh khớp số chứng từ **chỉ** với dòng tiền tiền tệ khác ⇒ máy ⛔ đề
       xuất *(cửa ghi từ chối cặp ấy — `QĐ-ITL-62`)* ⇒ ô in **chính câu cửa
       trả** *(nói mã tiền tệ của dòng khớp)*. ⛔ Trước: *"đề xuất: …"* một dòng
       USD dưới lệnh VND — **84** lệnh sổ thật 02/10.
       ⛔ Câu màn tự ghép *(cửa đổi chữ ⇒ màn đổi theo)*. ⛔ Lớp `none`: đó là
       `--faint` **2,17 : 1** — câu mang nghĩa phải đọc được *(`NFR-I29`)* ⇒
       chữ thường của bảng *(`--ink`)* ＋ `title` = đúng câu *(ô hẹp cắt).*
       `the.vi_sao` **chỉ có** ở nhánh ấy *(`HOI-038` phương án B)* ⇒ năm câu
       kia ⛔ đổi. */
    if (!g && d.vi_sao) {
      const c = o('span', null, d.vi_sao);
      c.setAttribute('title', d.vi_sao);
      e.appendChild(c);
      return e;
    }
    if (!g) {
      e.appendChild(o('span', 'none' + (d.trang_thai === 'khong_gan_duoc'
                                        ? ' crit' : ''),
        d.trang_thai === 'khong_gan_duoc'
          ? 'sổ không có số tiền này' : '— chưa chọn'));
      return e;
    }
    if (g.loi_nguon) {
      e.appendChild(o('span', 'none crit', '⛔ không đọc được nguồn'));
      return e;
    }
    const b = TP.el('div', 'gd' + (g.da_gan ? '' : ' de-xuat'));
    const chu = g.dien_giai ? gon(g.dien_giai)
      : (g.dien_giai_vi_sao === 'chua_noi_duoc'
         ? '⛔ chưa đọc được nội dung' : '(diễn giải trống)');
    b.appendChild(o('span', 'gdchu', (g.da_gan ? '' : 'đề xuất: ') + chu));
    b.appendChild(o('span', 'gdmeta',
      [g.doc_date, ve_nguon(g.nguon)].filter(Boolean).join(' · ')));
    b.setAttribute('title', chu);
    e.appendChild(b);
    return e;
  }

  function ve_bang() {
    const t = TP.el('div', 'mtable');
    const h = TP.el('div', 'mhead mcols');
    COT_BANG.forEach(c => h.appendChild(o('div', c[2] || null, c[1])));
    t.appendChild(h);

    if (!ST.dong.length) {
      /* ⭐ `UI-F2` — hàng chờ rỗng đọc như **thành tựu**, ⛔ không như lỗi. */
      const tr = TP.el('div', 'empty');
      if (ST.chip === 'chua_gan')
        tr.appendChild(o('span', 'big', 'Hàng chờ đã sạch.'));
      tr.appendChild(o('span', null, ST.chip === 'chua_gan'
        ? 'Không còn lệnh chi nào đợi gán.'
        : 'Không có dòng nào trong bộ lọc này.'));
      t.appendChild(tr);
      return TP.el('div', 'tablescroll').appendChild(t).parentNode;
    }

    ST.dong.forEach((d, i) => {
      const r = TP.el('button', 'mrow mcols ' + (d.trang_thai || ''));
      r.setAttribute('type', 'button');
      if (ST.tro === i) r.setAttribute('aria-current', 'true');
      const oc = (lop, chu, nhan) => {
        const c = TP.el('div', 'mcell' + (lop ? ' ' + lop : ''));
        if (nhan) c.appendChild(nhan);
        else if (chu == null || chu === '')
          c.appendChild(o('span', 'none', KHONG_CO));
        else c.appendChild(o('span', null, chu));
        return c;
      };
      r.appendChild(oc('', d.ngay));
      r.appendChild(oc('', null, o('span', 'pm', d.ma_lenh)));
      r.appendChild(oc('', null, o('span', 'chip pt', d.loai_phieu)));
      r.appendChild(oc('', null, o('div', 'desc', gon(d.noi_dung))));
      r.appendChild(oc('', null, o('div', 'cdt', d.cdt)));
      /* ⭐⭐ `WO-022` vong 2 *(`BA-06` v4.13 §5b ⓘ, `HOI-026`)*: hai o tien
         rong theo **ngan sach 18 ky tu** *(`hinh.css` `.mcols`)*; chuoi
         **vuot** ngan sach ⇒ CSS in `…` *(`.mtable .mcell.r`)* va `title`
         mang **dung** chuoi in ⇒ ⛔ bao gio cat **im lang**. */
      const tien_o = (chu, c) => { c.setAttribute('title', chu); return c; };
      const chu_tien = TP.tien(d.so_tien, d.curr) + ' ' + d.curr;
      r.appendChild(tien_o(chu_tien, oc('r', null,
        o('span', 'num', chu_tien))));
      r.appendChild(oc('', null,
        o('span', 'chip ' + (d.trang_thai_mau || ''), d.trang_thai_nhan)));
      r.appendChild(oc('', null, d.so_chung_tu
        ? o('span', 'pm', d.so_chung_tu) : o('span', 'none', '— chưa có')));
      r.appendChild(oc('arr', '→'));
      r.appendChild(ve_o_gd(d));
      const chu_gd = d.gd && !d.gd.loi_nguon
        ? TP.tien(d.gd.amount, d.gd.curr) + ' ' + (d.gd.curr || '') : null;
      const o_gd = oc('r', null, chu_gd !== null
        ? o('span', 'num', chu_gd) : o('span', 'none', '—'));
      r.appendChild(chu_gd !== null ? tien_o(chu_gd, o_gd) : o_gd);
      /* ⭐ `WO-023` `(h)` ⓑ — chuột: như phím. */
      r.addEventListener('click', () => { ST.tro = i; _nguoi_mo(mo_lenh(d.ma_lenh)); });
      t.appendChild(r);
    });
    const cuon = TP.el('div', 'tablescroll');
    cuon.appendChild(t);
    return cuon;
  }

  /* ── ⭐⭐ VIEW ② · RAIL — **ba dòng** mỗi mục, đúng bản dựng ────────────
     ⛔ Bản `22/09` chỉ có `3` mục trên **một** dòng *(mã · nội dung · tiền)*
        ⇒ mất `Ngày`, `Loại`, **chip trạng thái** và `CDT`. Người đang ghép
        cần chúng để **⛔ không phải mở từng dòng ra mới biết dòng nào đáng mở**. */
  function ve_rail() {
    const rail = TP.el('div', 'rail');
    const dau = TP.el('div', 'railhead');
    dau.appendChild(o('span', null, 'Lệnh chi'));
    dau.appendChild(o('span', null, ST.dong.length + ' dòng'));
    rail.appendChild(dau);

    ST.dong.forEach((d, i) => {
      const r = TP.el('button', 'rrow ' + (d.trang_thai || '')
                               + (ST.mo === d.ma_lenh ? ' mo' : ''));
      r.setAttribute('type', 'button');
      if (ST.mo === d.ma_lenh) r.setAttribute('aria-current', 'true');

      const l0 = TP.el('div', 'l0');
      const trai = TP.el('span', 'left');
      trai.appendChild(o('span', 'd', d.ngay || ''));
      trai.appendChild(o('span', 'pm', d.ma_lenh));
      trai.appendChild(o('span', 'chip pt', d.loai_phieu));
      l0.appendChild(trai);
      l0.appendChild(o('span', 'chip ' + (d.trang_thai_mau || ''),
                       d.trang_thai_nhan));
      r.appendChild(l0);

      const l1 = TP.el('div', 'l1');
      const nd = o('span', 'nd', gon(d.noi_dung));
      nd.setAttribute('title', gon(d.noi_dung));
      l1.appendChild(nd);
      l1.appendChild(o('span', 'amt', TP.tien(d.so_tien, d.curr) + ' ' + d.curr));
      r.appendChild(l1);

      r.appendChild(o('span', 'cdt', d.cdt));
      /* ⭐ `WO-023` `(h)` ⓑ — chuột: như phím. */
      r.addEventListener('click', () => { ST.tro = i; _nguoi_mo(mo_lenh(d.ma_lenh)); });
      rail.appendChild(r);
    });
    return rail;
  }

  /* ⭐ Tay kéo. `separator` ＋ `tabindex` ＋ `←→` — ⛔ không thì người dùng
     bàn phím ⛔ không biết nó tồn tại, và `NFR-I24` đòi mọi thứ bấm được
     bằng chuột phải bấm được bằng phím. */
  function ve_keo(than) {
    const k = o('div', 'keo', '');
    k.setAttribute('role', 'separator');
    k.setAttribute('aria-orientation', 'vertical');
    k.setAttribute('tabindex', '0');
    k.setAttribute('title', 'Kéo để đổi bề rộng cột lệnh chi (←→)');
    k.setAttribute('aria-label', 'Bề rộng cột lệnh chi');

    k.addEventListener('keydown', e => {
      /* ⭐ `WO-023` `(a)` `ⓕ1`: hộp mở ⇒ ⛔ kéo rail sau lưng hộp. */
      if (typeof HT !== 'undefined' && HT.nuot_phim && HT.nuot_phim(e)) return;
      const b = e.key === 'ArrowLeft' ? -24
              : e.key === 'ArrowRight' ? 24 : 0;
      if (!b) return;
      e.preventDefault();
      ST.rail_w = chan_rail((ST.rail_w || _rong_rail(than)) + b);
      than.setAttribute('style', '--rail-w:' + ST.rail_w + 'px');
    });

    /* ⭐ Kéo **⛔ không gọi `ve()`**: dựng lại vài trăm dòng ở mỗi khung hình
       sẽ giật. Chỉ đổi một biến CSS; `ve()` lần sau đọc lại `ST.rail_w`. */
    k.addEventListener('pointerdown', e => {
      const x0 = e.clientX;
      const w0 = ST.rail_w || _rong_rail(than);
      k.classList.add('dang-keo');
      document.body.classList.add('dang-keo');
      if (k.setPointerCapture && e.pointerId != null)
        k.setPointerCapture(e.pointerId);
      const keo = ev => {
        ST.rail_w = chan_rail(w0 + (ev.clientX - x0));
        than.setAttribute('style', '--rail-w:' + ST.rail_w + 'px');
      };
      const thoi = () => {
        k.classList.remove('dang-keo');
        document.body.classList.remove('dang-keo');
        document.removeEventListener('pointermove', keo);
        document.removeEventListener('pointerup', thoi);
      };
      document.addEventListener('pointermove', keo);
      document.addEventListener('pointerup', thoi);
    });
    return k;
  }

  /* ⭐ Bề rộng ĐANG hiển thị, khi ⛔ chưa ai kéo lần nào — đo phần tử thật,
     ⛔ không đoán lại công thức `clamp` bằng JS *(một bản thứ hai của cùng
     một con số là một bản sẽ lệch)*. */
  function _rong_rail(than) {
    const r = than.querySelector && than.querySelector('.rail');
    const w = r && r.getBoundingClientRect
      ? r.getBoundingClientRect().width : 0;
    return chan_rail(w || 340);
  }

  /* ⭐⭐⭐ Ba hop cuon RIENG cua man. `ve()` dựng lại **toàn bộ** cây mỗi
     lần ⇒ `scrollTop` của cả ba về `0`: kế toán cuộn xuống dòng thứ `40`,
     bấm chọn một giao dịch, và **mất chỗ mình đang đứng**.

     ⛔⛔ Lỗi này **⛔ không tồn tại trước `23/09`** — trước đó cả trang cuộn
        và trình duyệt tự giữ vị trí. Chính phép sửa *"chỉ danh sách giao
        dịch cuộn"* đã sinh ra nó. ⭐ Một phép sửa mở ra một lỗi mới thì
        phải có một bài thử **đi kèm**, ⛔ không phải một lần nhìn lại. */
  const HOP_CUON = ['.rail', '.cands', '.tablescroll'];

  function _nho_cuon(goc) {
    const m = {};
    HOP_CUON.forEach(ten => {
      const e = goc.querySelector(ten);
      if (e) m[ten] = e.scrollTop;
    });
    return m;
  }

  function _tra_cuon(goc, m) {
    Object.keys(m).forEach(ten => {
      const e = goc.querySelector(ten);
      if (e) e.scrollTop = m[ten];
    });
  }

  function ve() {
    const goc = document.querySelector('#ghep-goc');
    if (!goc) return;
    /* ⭐ Đọc **trước** khi xoá — sau đó ⛔ không còn gì để đọc. */
    const cuon = _nho_cuon(goc);
    goc.textContent = '';

    const dai = TP.el('div', 'dai-loc');
    ve_chip(dai);
    goc.appendChild(dai);

    /* ⭐⭐ BỐN trạng thái của danh sách, và ⛔ KHÔNG cái nào được trông giống
       cái kia. Trước `22/09` màn chỉ có **một** — *"Hàng chờ đã sạch."* — và
       nó hiện ra cả khi ⛔ chưa hỏi, cả khi cửa lỗi, cả khi chip ⛔ chưa có cửa. */
    if (ST.thieu_cua) {
      goc.appendChild(o('p', 'banner warn',
        '⛔ Chưa có cửa cho bộ lọc này. Cửa `/queue/lenh-cho` lọc cứng '
        + '"chưa nối", nên FLS ⛔ chưa có đường hỏi. (GAP-API-08)'));
      return;
    }
    if (ST.loi) {
      goc.appendChild(o('p', 'banner crit', '⛔ Cửa lỗi: ' + ST.loi));
      /* ⭐ `WO-045` `(e)` *(`BA-06` v4.19 `§4.5 ⓥ` ⑤ — `HOI-043` Q4)*: trước
         nút này, đường thử lại **duy nhất** là bấm lại chip đang chọn — và
         màn ⛔ nói *(chữ `Thử lại` trong tệp: **0** chỗ, đo 05/10)*. Bấm ⇒
         **cùng đường** với bấm lại chip *(`doi_chip` — một lượt mới theo
         `ⓥ`; bấm lần hai khi lượt ấy còn bay ⇒ `ⓥ` ② ⛔ mở lượt nào)*. Lớp
         `b tiny` có sẵn *(⛔ token, ⛔ lớp CSS mới)*; ⛔ đổi câu lỗi. Áp cho
         **cả** `FLS-MAT-KET-NOI` — cùng nhánh `ST.loi`. */
      goc.appendChild(nut('tiny', 'Thử lại', () => doi_chip(ST.chip)));
      return;
    }
    if (ST.dang_tai) {
      goc.appendChild(o('p', 'banner info', 'Đang hỏi sổ…'));
      return;
    }

    /* ⭐ Câu gợi ý phím **đổi theo view** — hai view, hai bộ phím. Một câu
       đứng yên ở đây sẽ nói sai đúng một nửa số lần người ta đọc nó. */
    goc.appendChild(o('p', 'goi-phim', ST.mo
      ? '↑↓ đổi lệnh · ← về bảng sổ · Enter gán · / tìm giao dịch'
      : '↑↓ chọn dòng · → (hoặc Enter) mở vùng ghép'));

    const lenh = ST.dong.find(d => d.ma_lenh === ST.mo);

    /* ⭐⭐⭐ VIEW ① — ⛔ chưa mở lệnh nào ⇒ **bảng sổ toàn bề ngang**. */
    if (!lenh) {
      goc.appendChild(ve_bang());
      soat_cat();
      _tra_cuon(goc, cuon);
      return;
    }

    /* ⭐⭐⭐ VIEW ② — đã mở ⇒ rail ＋ bàn làm việc. */
    const than = TP.el('div', 'than');
    if (ST.rail_w) than.setAttribute('style', '--rail-w:' + ST.rail_w + 'px');
    than.appendChild(ve_rail());
    than.appendChild(ve_keo(than));

    const lam = TP.el('div', 'work');
    lam.appendChild(ve_the(lenh));

    /* ⭐⭐ Đo `23/09` trên `2.219` lệnh đã gán: **`23` (`1,0%`)** gán nhiều
       hơn một dòng tiền, nhiều nhất **`7`**. ⛔⛔ Một `1,0%` là cớ để **⛔
       không bật hộp thoại xác nhận** *(`QĐ-ITL-148 ⓔ`)* — ⛔ **không** phải
       cớ để **giấu mất sáu dòng tiền**: hiện dòng đầu và im về `6` dòng còn
       lại thì màn đang **nói sai** về một phép gán thật. */
    const ds_gan = lenh.gd_ds
      || (lenh.gd && lenh.gd.da_gan ? [lenh.gd] : []);
    ds_gan.forEach(g => lam.appendChild(ve_dang_gan(lenh, g)));
    if (ds_gan.length > 1) lam.appendChild(ve_tong_chum(lenh, ds_gan));
    /* ⭐ `WO-045` ①: vùng ứng viên **đang tải** / **lỗi** *(của lượt mới
       nhất)* ⇒ ⛔ dải *Toàn sổ*, ⛔ chú giải, ⛔ câu rỗng — chưa có câu trả
       lời nào để nói. Khung chờ dùng **đúng** chữ + lớp của danh sách lệnh
       *(`Đang hỏi sổ…` `banner info`)*; lỗi đúng khuôn `②b` *(`⛔ Cửa lỗi:`
       `banner crit`)* — ⛔ chữ mới, ⛔ lớp mới. */
    const cho_uv = ST.dang_tai_uv || !!ST.loi_uv;
    if (ST.toan_so && !cho_uv)
      lam.appendChild(o('p', 'banner info',
        ST.tim ? 'Đang tra cứu TOÀN SỔ theo chữ đã gõ.'
               : 'Máy không tìm được ứng viên nào — đang tra cứu TOÀN SỔ.'));
    /* ⭐ Chú giải **một** lần, ngay trên danh sách — ở **cả** *Máy đề xuất*
       lẫn *Toàn sổ*. ⛔ Khi danh sách rỗng: ⛔ có ký hiệu nào để giải
       *(`BA-06` v4.15 §4.5 ⓒ ①)*. Đang tải ⇒ `ve()` đã thoát ở trên. */
    if (ST.ung_vien.length && !cho_uv) lam.appendChild(ve_chu_giai());
    const ds = TP.el('div', 'cands');
    ds.appendChild(ve_dau_gd());
    if (ST.dang_tai_uv)
      ds.appendChild(o('p', 'banner info', 'Đang hỏi sổ…'));
    else if (ST.loi_uv) {
      ds.appendChild(o('p', 'banner crit', '⛔ Cửa lỗi: ' + ST.loi_uv));
      /* ⭐ `WO-023` `(h)` ⓒ *(`BA-06` v4.21 `ⓦ` ④ hàng lỗi)*: nút `Thử lại`
         lớp `b tiny` **ngay dưới** câu lỗi — trước đó lối ra duy nhất là bấm
         lại hàng lệnh / `j` rồi `k`: đi được, chỉ là màn ⛔ nói. ⛔ Chữ mới,
         ⛔ lớp mới *(`b tiny` có sẵn — `②b` `ⓥ` ⑤)*. */
      ds.appendChild(nut('tiny', 'Thử lại', () => thu_lai_uv()));
    } else {
      ST.ung_vien.forEach((uv, i) => ds.appendChild(ve_ung_vien(lenh, uv, i)));
      if (!ST.ung_vien.length)
        ds.appendChild(o('p', 'banner crit', 'Sổ không có dòng tiền nào.'));
    }
    lam.appendChild(ds);
    lam.appendChild(ve_thanh(lenh));
    than.appendChild(lam);
    goc.appendChild(than);
    /* ⭐ Đo SAU khi đã gắn vào cây — trước đó ⛔ không có kích thước. */
    soat_cat();
    _tra_cuon(goc, cuon);
  }

  return { ST, ve, mo_man, mo_lenh, phim, tim_focus,
           chan_rail, RAIL_MIN, RAIL_MAX, ve_keo, ve_dau_gd, TEN_COT_GD,
           da_noi_ban_phim: () => _da_noi, TRE_TIM,
           TRUONG_THE, COT_BO_DUOC,
           BAC, CHIP, CHIP_CUA, THU_TU_BAC, khop_dung_tien, khac_tien_te,
           gan, bo_gan,
           ve_tong_chum,
           lenh_ke_tiep, tai_danh_sach, doi_chip, tai_toan_so,
           danh_dau, soat_cat, ve_bang, ve_rail, COT_BANG,
           ve_the, ve_ung_vien, ve_thanh, ve_chu_giai };
})();
