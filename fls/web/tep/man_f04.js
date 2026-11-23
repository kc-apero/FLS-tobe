/* ═══════════════════════════════════════════════════════════════════════
   man_f04.js — man **NAP SAO KE** (`SCR-F04`, `BA-06` §7 v2.7).

   ⛔⛔ **DOC DONG NAY TRUOC KHI SUA MOT CHU:** man nay ⛔ **KHONG PHAI MAN
   DAN**. `QĐ-ITL-109` chot FLS **doc vung CHUAN** cua sheet `R |`; cu chi
   `Ctrl+V` **o lai Google Sheets**, va man nay ⛔ **khong co MOT O NHAP NAO**
   cho du lieu giao dich.

   ⭐ Ly do duoc **ky thanh quyet dinh** chu ⛔ khong de tuy nghi: do song 60
     nguon bank thi **36** nguon boc ngay bang cong thuc rieng va **23** nguon
     **DOI DAU** (`Credit = <cot tho> × (−1)`, kem hoan ve No ↔ Co). Cho 60
     phep bien doi ay sang FLS la mo mot cho de **SAI DAU TIEN**.

   ── Nam trang thai (`BA-06` §7 ⓶) ─────────────────────────────────────
      ① chon pham vi  — `GET /sources`
      ② FLS doc       — `GET /chup` + `GET /chup/{id}`   *(ANH CHUP, ⛔ khong
                        goi Sheets tu man — `QĐ-ITL-110`)*
      ③ ban khai      — `GET /sources/{id}/khai-cot`     *(de XEM)*
      ④ bien ban      — `POST /nap/xem-truoc`            *(9 luat)*
      ⑤ da nhan       — `POST /nap`

   ⛔⛔ **O quan trong nhat cua ca man la `da_do`.** Mot luat noi *"dat"* ma
   ⛔ khong noi **da do bao nhieu** la mot luat **chua do**. Luat nen ay da cuu
   that mot lan: `L6` cua cong #17 bao do `0` ⇒ DO, ⛔ khong co no thi cong
   **xanh gia**. ⇒ Cot `Da do` la cot ⛔ **khong duoc bo**.

   ── ⛔ Man nay CO Y ⛔ khong co (`BA-06` §7 ⓺) ─────────────────────────
      · nut day sang `A-CCR`  — chang 3, **chan o owner** (`GAP-PLAN-05`).
        Dung san mot nut chua duoc phep bam la **moi nguoi bam nham**.
      · sua gia tri o ngay tren man nap — sua la **them but toan** (`INV-I08`),
        va cho sua la `SCR-F02`.
      · buoc duyet cua nguoi thu hai — `QĐ-ITL-27`: van hanh that **2–3 ke
        toan**, ⛔ khong co nguoi thu hai. Kiem soat nam o **MAY** (bien ban ④).

   ── Hanh vi Sheets: man nay can **4/8** (`BA-06` §7 ⓹) ────────────────
      CAN     : 7 so kieu ke toan · 6 dong cung tieu de · 5 filter view ·
                1 dieu huong ban phim *(tren luoi xem truoc)*
      ⛔ KHONG: 2 dan vung · 3 keo xuong · 4 hoan tac · 8 tu luu
      ⇒ Man nay la cho **NAP va SOAT**, ⛔ khong phai cho **GO**.

   ⚠ Tep nay theo **LUAT KY HIEU** (`tests/web/test_luat_ky_hieu_man_hinh.py`):
     `⛔ ⚠ ⭐ 🔒` **cat han** khoi van ban hien ra man; chu thich thi duoc.
     Ly do: ke toan noi nguyen van *"qua nhieu note, ky hieu → kho nhin"*.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F04 = (function () {

  /* ── trang thai cua man, ⛔ khong phai cua du lieu ─────────────────── */
  const S = {
    nguon: [],          // GET /sources
    chon: new Set(),    // source_id da tick
    loc: 'tat_ca',      // tat_ca | Bank | Cash
    chup: null,         // anh chup dang xem
    bien_ban: null,     // ket qua xem-truoc
    nguon_soat: null,   // soat cho nguon nao
    thu_tu: null,       // GET /chup/{id}/thu-tu — BANG CHUNG, ⛔ khong ket luan
    da_nhan: null,      // ket qua nap
    gap_trang_thai: ''  // ma GAP do CUA khai, ⛔ khong go tay o tang man
  };

  /* ⭐ Ba hang cua bien ban, va **BA**, ⛔ khong phai hai. Hang tra loi cau
     *"khuyet tat nay la cua AI"*, ⛔ khong phai *"no nang bao nhieu"*.       */
  const HANG = {
    CHAN: { lop: 'crit', chu: 'chặn',
            ghi: 'Lỗi của hệ. Nạp sai, mất dòng. Không một dòng nào vào sổ.' },
    CO:   { lop: 'warn', chu: 'cờ',
            ghi: 'Khuyết tật có sẵn trong dữ liệu kế toán. Vẫn đỏ, vẫn báo, '
               + 'nhưng nút Nhận vẫn bật: những dòng ấy là tiền thật.' },
    CANH: { lop: 'lock', chu: 'canh', ghi: 'Theo dõi, không chặn.' }
  };

  /* ⭐ Mot o cua bang. ⛔ DOM toi thieu cua bo test ⛔ khong co `insertCell`
     *(no co Y chi lam nhung gi man that cham toi)*, va no cung ⛔ khong phan
     tich `innerHTML` ⇒ moi cau truc phai la **cay the that**. */
  function _td(tr, lop) {
    const c = TP.el('td', lop);
    tr.appendChild(c);
    return c;
  }

  /* ═══════════════════════════════════════════════ ① chon pham vi ═══ */
  function _loc_nguon() {
    if (S.loc === 'tat_ca') return S.nguon;
    return S.nguon.filter(n => n.src_type === S.loc);
  }

  function _dem(t) {
    return S.nguon.filter(n => t === 'tat_ca' || n.src_type === t).length;
  }

  function _ve_chon(o) {
    o.textContent = '';

    /* Bo loc — mot `seg`, cung khuon cong tac Quet/Go cua `F02`. */
    const seg = TP.el('div', 'seg');
    [['tat_ca', 'Tất cả'], ['Bank', 'Ngân hàng'], ['Cash', 'Quỹ']]
      .forEach(function (x) {
        const b = TP.el('button', null,
          TP.chu(x[1]) + ' <span class="num">' + _dem(x[0]) + '</span>');
        b.setAttribute('aria-pressed', String(S.loc === x[0]));
        b.dataset.loc = x[0];
        b.onclick = function () { S.loc = x[0]; _ve_chon(o); };
        seg.appendChild(b);
      });

    const thanh = TP.el('div', 'dstrip');
    thanh.appendChild(seg);
    thanh.appendChild(TP.el('span', 'spacer'));
    thanh.appendChild(TP.el('span', 'muted',
      'Mặc định tick tất cả, vì nút Run hôm nay cũng gom cả '
      + S.nguon.length + ' nguồn một lượt.'));
    o.appendChild(thanh);

    /* ⛔⛔ `GAP-CHUP-02` — man PHAI noi ra cho thieu, ⛔ khong im lang.
       `fls_source` ⛔ khong co cot trang thai; `Account Status`
       (`Closed` 10 · `InActive` 5) chi song o sheet AS-IS. Im lang thi ke
       toan doc danh sach nay thanh *"ca 68 nguon deu dang chay"*.          */
    if (S.nguon.some(n => n.trang_thai_nguon === null)) {
      o.appendChild(TP.el('div', 'note warn',
        '<b>Danh sách này chưa phân biệt được nguồn đã đóng.</b> Kho của FLS '
        + 'chưa chở trạng thái tài khoản (Active / InActive / Closed) — nó '
        + 'chỉ có trên sheet danh mục. Nên một nguồn đọc ra 0 dòng ở đây có '
        + 'thể là thiếu sheet, mà cũng có thể là tài khoản đã đóng hợp lệ. '
        /* ⭐ Ma GAP lay TU CUA (`gap_trang_thai`), ⛔ khong go tay o day: mot
           ma go tay o tang man la **cho khai thu hai**, va no se troi khi
           GAP kia doi so. */
        + 'Đang chờ quyết định: ' + TP.chu(S.gap_trang_thai || '')));
    }

    /* Luoi nguon. ⛔ Chi-doc ve du lieu; o tick la **pham vi**, ⛔ khong
       phai mot o nhap du lieu giao dich.                                  */
    const ds = _loc_nguon();
    const b = TP.bang([{ chu: '', rong: '30px' }, { chu: 'Nguồn' },
                       { chu: 'Bản khai', rong: '96px' },
                       { chu: 'Đọc lần cuối', rong: '132px' },
                       { chu: 'Số dòng', rong: '96px' },
                       { chu: '', rong: '78px' }]);
    const bang = b.bang, than = b.than;

    ds.forEach(function (n) {
      const tr = TP.el('tr');
      than.appendChild(tr);
      tr.dataset.sid = String(n.source_id);

      const c0 = _td(tr);
      const tick = document.createElement('input');
      tick.type = 'checkbox';
      tick.checked = S.chon.has(n.source_id);
      tick.setAttribute('aria-label', 'chọn ' + n.source_key);
      tick.onchange = function () {
        if (tick.checked) S.chon.add(n.source_id);
        else S.chon.delete(n.source_id);
        _cap_nhat_nut();
      };
      c0.appendChild(tick);

      _td(tr).innerHTML =
        '<span class="mono">' + TP.chu(n.source_key) + '</span>';

      /* ⭐ `khai_version === null` la mot CAU TRA LOI: *"chua ai khai cach
         doc nguon nay"* ⇒ hien mot dau gach, va nut Soat cua no **tat**.  */
      _td(tr).innerHTML = n.khai_version === null
        ? TP.chip('lock', 'chưa khai', 'Chưa ai khai cột nào là gì cho nguồn '
            + 'này. Máy không đoán vị trí cột: đoán sai một cột là sai tiền.')
        : '<span class="mono">v' + TP.chu(n.khai_version) + '</span>';

      _td(tr).innerHTML = n.chup_cuoi
        ? '<span class="mono tiny">' + TP.chu(_gio(n.chup_cuoi)) + '</span>'
        : TP.chip('lock', 'chưa đọc');

      _td(tr).innerHTML =
        '<span class="num">' + TP.so(n.txn_count) + '</span>';

      const c5 = _td(tr);
      const b = TP.el('button', 'b');
      b.textContent = 'Bản khai';
      b.disabled = n.khai_version === null;
      b.onclick = function () { _xem_khai(n); };
      c5.appendChild(b);
    });

    const boc = TP.el('div', 'gwrap');
    boc.appendChild(bang);
    o.appendChild(boc);

    o.appendChild(TP.el('div', 'note',
      '<b>Bản khai ở đây là để xem, không để sửa.</b> Nó là cấu hình của '
      + 'nguồn, đặt một lần rồi thôi. Sửa khai sinh ra một bản mới, và mọi '
      + 'lần nạp sau sẽ đọc theo bản mới.'));
  }

  function _gio(s) {
    /* ⛔ Hien **DAU THOI DIEM**, ⛔ khong hien "tuoi". Tuoi la mot phep tru
       *(no doi moi giay)*; dau thoi diem la mot su that. `BA-06` §7 ⓶ doi
       dung con so nay.                                                    */
    const d = new Date(s);
    if (isNaN(d)) return String(s);
    const h = x => String(x).padStart(2, '0');
    return h(d.getDate()) + '/' + h(d.getMonth() + 1) + ' '
         + h(d.getHours()) + ':' + h(d.getMinutes()) + ':' + h(d.getSeconds());
  }

  /* ═══════════════════════════════════ ③ ban khai — de XEM ═══════════ */
  async function _xem_khai(n) {
    const noi = TP.$('#nap-khai');
    noi.hidden = false;
    await TT.chay(noi,
      () => FLS.doc('/sources/' + n.source_id + '/khai-cot'),
      function (d, _m, o) {
        o.appendChild(TP.el('div', 'dstrip',
          '<b>' + TP.chu(d.source_key) + '</b>'
          + TP.chip('info', 'đang hiệu lực: v' + d.hieu_luc.version)
          + TP.chip('lock', d.dai_version.length + ' bản đã khai')));

        d.dai_version.forEach(function (b) {
          const kh = TP.el('div', 'grp');
          const cot = Object.keys(b.cot).sort()
            .map(k => '<span class="chip lock">' + TP.chu(k) + ' → cột '
                    + TP.chu(b.cot[k]) + '</span>').join(' ');
          kh.innerHTML =
            '<div class="t">v' + TP.chu(b.version)
            + (b.version === d.hieu_luc.version
                ? ' · đang hiệu lực' : ' · bản cũ')
            + '</div>'
            + '<div class="pad">' + cot
            + '<div class="muted tiny" style="margin-top:6px">'
            + TP.chu(b.actor) + ' khai lúc ' + TP.chu(_gio(b.hieu_luc_tu))
            + '</div></div>';
          o.appendChild(kh);
        });

        o.appendChild(TP.el('div', 'note',
          'Bản cũ vẫn giữ nguyên, vì một dòng nạp tháng trước phải giải '
          + 'thích được bằng bản khai đang hiệu lực lúc ấy.'));
      },
      { so_dong: 3 });
  }

  /* ═══════════════════════════════════ ② FLS doc — ANH CHUP ═════════ */
  async function _ve_doc(o) {
    await TT.chay(o,
      () => FLS.doc('/chup?lan=Bank&limit=10'),
      function (d, _m, oo) {
        const ds = d.chup || [];
        oo.appendChild(TP.el('div', 'muted',
          'FLS đọc vùng CHUẨN của sheet, không đọc vùng thô, và không ghi '
          + 'một ô nào về Google Sheets.'));

        const bb = TP.bang([{ chu: 'Đọc lúc' }, { chu: 'Nguồn', rong: '86px' },
                            { chu: 'Dòng', rong: '96px' },
                            { chu: 'Giây', rong: '78px' },
                            { chu: '', rong: '96px' }]);
        const bang = bb.bang;
        ds.forEach(function (a) {
          const tr = TP.el('tr');
          bb.than.appendChild(tr);
          /* ⭐ Neo `data-chup`: bo chon cua DOM toi thieu **chi mot cap**, nen
             mot bai kiem ⛔ khong voi duoc `#nap-doc tbody tr`. Neo nay la
             duong de MAY soi duoc dong nao la anh nao. */
          tr.dataset.chup = String(a.chup_id);
          _td(tr).innerHTML =
            '<span class="mono">' + TP.chu(_gio(a.doc_luc)) + '</span>';
          _td(tr).innerHTML =
            '<span class="num">' + TP.so(a.so_nguon) + '</span>';
          _td(tr).innerHTML =
            '<span class="num">' + TP.so(a.so_dong) + '</span>';
          _td(tr).innerHTML =
            '<span class="num">' + TP.chu(a.giay === null ? '—' : a.giay)
            + '</span>';
          const b = TP.el('button', 'b');
          b.textContent = 'Xem trước';
          b.onclick = function () { _mo_chup(a.chup_id); };
          _td(tr).appendChild(b);
        });
        const boc = TP.el('div', 'gwrap');
        boc.appendChild(bang);
        oo.appendChild(boc);

        /* ⛔⛔ `GAP-CHUP-01` — man PHAI noi ra rang no ⛔ KHONG tu doc duoc.
           Dung san mot nut "Doc lai" chua co duong chay la **moi nguoi bam
           roi cho mai**.                                                  */
        oo.appendChild(TP.el('div', 'note warn',
          '<b>Màn này chưa tự đọc lại được.</b> Phép đọc 60 sheet chạy ngoài '
          + 'màn hình, và ai bấm đọc lại theo nhịp nào thì còn chờ quyết '
          + 'định: GAP-CHUP-01. Hôm nay nó chạy bằng một lệnh.'));
      },
      /* ⭐ `WO-032` (e): `data: null` *(`?gia_lap=rong`)* ⇒ câu rỗng, ⛔
         `TypeError`. ⚠ Chỗ này **lộ ra** khi vá `ve()` bên dưới: trước đó
         `TypeError` ở `#nap-chon` làm `ve()` dừng **trước** `_ve_doc` ⇒ lỗi
         thứ hai ⛔ ai thấy. */
      { la_rong: d => !d || !d.chup || d.chup.length === 0,
        rong: { icon: '—', tieu_de: 'Chưa có lần đọc nào',
                cau: 'Kho đã trả lời, và câu trả lời là chưa có ảnh chụp '
                   + 'nào. Cần chạy phép đọc một lần trước khi soát.' },
        so_dong: 3 });
  }

  /* ⭐⭐ `WO-045` ④ *(`BA-06` v4.19 `§4.5 ⓦ` ① — `BG-044` `(d)` #17 · #18)*:
     lượt **mới nhất** thắng. Bản trước: bấm `Xem trước` hai ảnh nhanh ⇒ ảnh
     **trước** về sau, `TT.chay` xoá ô rồi vẽ nó ⇒ màn + `S.chup` +
     `S.thu_tu` là ảnh **trước** — nhất quán với nhau *(`Nhận` gửi đúng ảnh
     đang hiện)* nhưng sai so với **cú bấm cuối** *(bài `test_AC8_…` đỏ trên
     `db0adae`)*. Hai bộ đếm vì hai ô: `#nap-xem` *(ảnh)* · `#nap-thu-tu`
     *(thứ tự ngày — còn được gọi lại sau một cú khai)*; mở ảnh mới cũng thay
     lượt thứ tự ngày đang bay của ảnh cũ. */
  let _luot_chup = 0;
  let _luot_thu_tu = 0;

  async function _mo_chup(cid) {
    const luot = ++_luot_chup;
    _luot_thu_tu++;
    const noi = TP.$('#nap-xem');
    noi.hidden = false;
    await TT.chay(noi,
      () => FLS.doc('/chup/' + cid + '?limit=50'),
      function (d, _m, o) {
        S.chup = d;

        /* Bon o dau — trong do **dau thoi diem** la o `BA-06` §7 ⓶ doi. */
        const the = TP.el('div', 'grid4');
        [['Nguồn đọc được', TP.so(d.so_nguon), 'trong lần đọc này'],
         ['Dòng đọc được', TP.so(d.so_dong), 'từ vùng CHUẨN'],
         ['Đọc lúc', _gio(d.doc_luc), 'dấu thời điểm, không phải tuổi'],
         ['Mất', (d.giay === null ? '—' : d.giay + 's'), 'cho cả lượt đọc']]
          .forEach(function (x) {
            o.appendChild(TP.el('div', 'card',
              '<div class="pad"><div class="k">' + TP.chu(x[0]) + '</div>'
              + '<div class="v num">' + TP.chu(x[1]) + '</div>'
              + '<div class="muted tiny">' + TP.chu(x[2]) + '</div></div>'));
          });
        o.appendChild(the);

        /* ⭐ Nguon ra **0 dong** hien RIENG — chung la thu de mat nhat, va la
           toan bo ly do bang `fls_chup_nguon` ton tai (diem mu `S8`).     */
        const khong = (d.nguon || []).filter(n => n.so_dong === 0);
        if (khong.length) {
          o.appendChild(TP.el('div', 'note',
            '<b>' + khong.length + ' nguồn đọc ra 0 dòng.</b> Chúng vẫn có '
            + 'mặt trong lần đọc này, để phân biệt được với nguồn chưa đọc: '
            + TP.chu(khong.map(n => n.source_key).join(' · '))));
        }

        o.appendChild(_luoi_xem_truoc(d));

        o.appendChild(TP.el('div', 'note',
          '<b>Lưới này chỉ đọc.</b> Sửa số nằm ở màn Sổ ITL, và sửa ở đó là '
          + 'thêm một bút toán chứ không ghi đè. Cho sửa ngay lúc đọc là sửa '
          + 'nguồn trong im lặng, mất đối chiếu với sheet gốc.'));

        _cap_nhat_nut();
        _ve_thu_tu(cid);
      },
      { so_dong: 4, con_hieu_luc: () => luot === _luot_chup });
  }


  /* ══════════════════════════ ②b THU TU NGAY — `QĐ-ITL-113` ═════════
     ⭐⭐⭐ Khoi nay ⛔ KHONG chon ho ke toan. May **de xuat kem bang chung**,
        nguoi **bam khai** — va bang chung phai co **CON SO**, ⛔ khong chi mot
        loi khuyen: mot cai nut kem loi khuyen ma ⛔ khong kem phep do la mot
        cai nut se duoc bam ma ⛔ khong ai doc.

     ⛔⛔ Do tren anh chup THAT: **1.894/8.368 dong (22,6%)** co ngay mo ho,
        trai **29/60 nguon**, va **29/29** nguon ay la `mdy` — ⛔ **0** nguon
        `dmy`. Nen man **⛔ KHONG duoc** dat `dmy` lam mac dinh "vi day la
        Viet Nam": lam the la hoan ngay<->thang tren 1.894 dong.            */
  async function _ve_thu_tu(cid) {
    const luot = ++_luot_thu_tu;
    const noi = TP.$('#nap-thu-tu');
    if (!noi) return;
    /* ⛔ `TT.chay` **xoa sach** phan tu no nhan, nen ta dua no `div.pad` chu
       ⛔ khong dua ca `<section>` — dua section thi `<header>` bi xoa sau lan
       tai dau tien. *(`#nap-xem` dang mac dung cho ay: `GAP-SCR-16`.)*     */
    const khung = TP.$('#nap-thu-tu-khung');
    if (khung) khung.hidden = false;
    await TT.chay(noi,
      () => FLS.doc('/chup/' + cid + '/thu-tu'),
      function (d, _m, o) {
        S.thu_tu = d;
        const can = (d.nguon || []).filter(n => n.can_khai);
        const thieu = can.filter(n => n.da_khai === null);

        /* ⭐ He qua bang CON SO, ⛔ khong canh bao chung chung. Cau *"co the
           mot so dong se bi loai"* ⛔ khong giup ai quyet dinh gi.          */
        const so_dong_thieu = thieu.reduce(
          (t, n) => t + n.bang_chung.mo_ho, 0);
        o.appendChild(TP.el('div', 'note ' + (thieu.length ? 'warn' : 'ok'),
          thieu.length
            ? '<b>' + thieu.length + ' nguồn chưa khai cách đọc ngày.</b> '
              + 'Trong lần đọc này có <b>' + TP.so(so_dong_thieu) + ' dòng</b> '
              + 'mà ngày đọc được hai cách. Nạp bây giờ thì đúng số dòng ấy '
              + 'vào hàng loại kèm lý do, các dòng còn lại vẫn vào sổ.'
            : '<b>Đã khai đủ.</b> ' + can.length + ' nguồn có ngày đọc được '
              + 'hai cách, và cả ' + can.length + ' đều đã có người ấn định '
              + 'thứ tự.'));

        /* ⭐⭐ Nguon ⛔ KHONG can khai hien o mot ghi chu RIENG — cung khuon
           voi *"nguon doc ra 0 dong"* o tren, va cung ly do: loc chung khoi
           man thi ke toan ⛔ khong co cach nao biet may **da soi** chung, con
           de chung thanh 21 dong noi *"khong can"* thi bang thanh nhieu.    */
        const khong = (d.nguon || []).filter(n => !n.can_khai);
        if (khong.length) {
          o.appendChild(TP.el('div', 'note',
            '<b>' + khong.length + ' nguồn không cần khai.</b> Ô ngày của '
            + 'chúng là số, nên chỉ có một cách đọc: '
            + TP.chu(khong.map(n => n.source_key).join(' · '))));
        }

        if (!can.length) return;

        /* ══ ⭐⭐⭐ mot cu bam cho ca lo — **CHI** nguon TU CHUNG (`QĐ-ITL-117`)
           ⛔⛔ Nut nay ⛔ KHONG gui `thu_tu`: cua `POST /chup/{id}/thu-tu` **do
              lai** bang chung phia may chu roi ghi dung cai no do ra. ⇒ Man
              hinh ⛔ **khong co duong nao** khai `dmy` cho 27 nguon.
           ⛔ Va no ⛔ khong nhan nguon ⛔ khong tu chung: chung o lai bang duoi,
             tung nguon mot, noi co dung **mot nguoi** chiu trach nhiem.     */
        const tu_chung = thieu.filter(n => n.de_xuat && !n.mau_thuan);
        const chua_chung = thieu.filter(n => !n.de_xuat || n.mau_thuan);
        if (tu_chung.length) {
          const kieu = Array.from(new Set(tu_chung.map(n => n.de_xuat)));
          const chung = tu_chung.reduce(
            (t, n) => t + n.bang_chung.chac_dmy + n.bang_chung.chac_mdy, 0);
          const cuu = tu_chung.reduce((t, n) => t + n.bang_chung.mo_ho, 0);
          const hop = TP.el('div', 'note');
          /* ⭐ Cau nay phai noi ca BA con so: bao nhieu nguon · bao nhieu dong
             **tu noi ra** thu tu · bao nhieu dong **nho** ban khai ay ma vao
             so. Thieu con so thu ba thi cu bam ⛔ khong co hau qua doc duoc. */
          hop.innerHTML = '<b>' + tu_chung.length + ' nguồn tự chứng '
            + (kieu.length === 1
                ? (kieu[0] === 'mdy' ? 'tháng/ngày' : 'ngày/tháng')
                : 'thứ tự của chúng')
            + '.</b> Chính dữ liệu của từng nguồn nói ra điều đó — tổng <b>'
            + TP.so(chung) + ' dòng</b> có phần không thể là tháng. Khai theo '
            + 'bằng chứng sẽ cho <b>' + TP.so(cuu) + ' dòng</b> mơ hồ vào sổ.';
          const b = TP.el('button', 'b');
          b.id = 'nap-nut-thu-tu-lo';
          b.textContent = 'Khai theo bằng chứng · ' + tu_chung.length
            + ' nguồn';
          b.onclick = function () {
            _khai_thu_tu_lo(cid, tu_chung.map(n => n.source_id));
          };
          hop.appendChild(TP.el('div', 'tiny'));
          hop.appendChild(b);
          o.appendChild(hop);
        }
        if (chua_chung.length) {
          /* ⛔ Noi ro **vi sao** chung o ngoai cu bam gop, ⛔ khong de chung
             lang le vang mat khoi con so tren nut.                         */
          o.appendChild(TP.el('div', 'note warn',
            '<b>' + chua_chung.length + ' nguồn không tự chứng.</b> Dữ liệu '
            + 'của chúng không có dòng nào loại trừ được một trong hai cách '
            + 'đọc, nên cú bấm gộp không nhận chúng — phải ấn định từng nguồn '
            + 'ở bảng dưới: '
            + TP.chu(chua_chung.map(n => n.source_key).join(' · '))));
        }

        const bb = TP.bang(['Nguồn', 'Đã khai', 'Máy đo được', 'Ấn định']);
        can.forEach(function (n) {
          const tr = TP.el('tr');
          bb.than.appendChild(tr);
          /* Neo `data-tt` — bo chon cua DOM toi thieu **chi mot cap**. */
          tr.dataset.tt = String(n.source_id);
          _td(tr).innerHTML = '<span class="mono">'
            + TP.chu(n.source_key) + '</span>';

          /* ⛔⛔ `da_khai === null` hien **"chưa khai"**, ⛔ KHONG hien o
             trong: mot o trong doc y het mot o *"khong ap dung"*.         */
          _td(tr).innerHTML = n.da_khai
            ? TP.chip('ok', n.da_khai)
            : TP.chip('crit', 'chưa khai');

          /* Cau bang chung — CO SO, den tu CUA, ⛔ khong dung o tang man. */
          _td(tr).innerHTML = TP.chu(n.cau);

          /* ⭐ HAI nut, va nut may de xuat duoc **danh dau** chu ⛔ khong
             phai nut duy nhat: mot nut duy nhat la may quyet, con hai nut
             thi nguoi chon — va ho van thay may nghieng ve dau.           */
          const o_nut = _td(tr, 'nowrap');
          if (n.mau_thuan) {
            /* ⛔ May ⛔ KHONG de xuat gi khi mau thuan — va phai NOI RA. */
            o_nut.appendChild(TP.el('span', 'muted tiny',
              'máy không đề xuất được'));
          }
          ['dmy', 'mdy'].forEach(function (tt) {
            const b = TP.el('button', tt === n.de_xuat ? 'b' : null);
            b.textContent = (tt === 'dmy' ? 'ngày/tháng' : 'tháng/ngày');
            /* ⛔ `data-chon`, ⛔ KHONG `data-tt`: dong da mang
               `data-tt` ⇒ mot bo chon `[data-tt]` se vot ca DONG lan
               NUT, va hai thu khac nhau chung mot neo la mot neo ⛔
               khong con tro duoc vao dau. *(Da can that: 3 bai DO.)* */
            b.dataset.chon = tt;
            b.disabled = (n.da_khai === tt);
            b.onclick = function () { _khai_thu_tu(n.source_id, tt, cid); };
            o_nut.appendChild(b);
          });
        });
        const boc = TP.el('div', 'gwrap');
        boc.appendChild(bb.bang);
        o.appendChild(boc);

        /* ⛔⛔ **Doan nay TUNG viet nguoc lai, va cho ay dang duoc doc.**
           Ban dau: *"Khong co nut khai tat ca: bang chung cua moi nguon khac
           nhau, va mot nut gop la mot nut duoc bam ma khong ai doc."* Do do
           thi **34/34** nguon chuoi **tu chung** thu tu bang du lieu cua chinh
           no *(0 nguon `dmy`, 0 mau thuan)* ⇒ **34 lan mot dap an**. Bat nguoi
           bam 27 cu de tra loi mot cau du lieu da tu tra loi la bat ho doc 27
           lan roi **bam theo phan xa** — dung cai lo cu, chi doi hinh.
           ⇒ Nut gop chi nhan nguon **TU CHUNG**, va nut ⛔ khong gui `thu_tu`. */
        o.appendChild(TP.el('div', 'note',
          '<b>Khai một lần cho mỗi nguồn.</b> Bản khai có phiên bản và mang '
          + 'tên người khai, nên đổi về sau là thêm một bản mới chứ không ghi '
          + 'đè. Cú bấm gộp ở trên không chọn thứ tự cho ai: cửa đo lại bằng '
          + 'chứng của từng nguồn rồi ghi đúng cái nó đo được, và nguồn nào '
          + 'không tự chứng thì nó từ chối cả lô.'));
      },
      /* ⛔⛔ `WO-032` vòng 2 `(k)` *(`BG-034` yếu #8, `TL-033 ⓒ`)*: `!d.nguon`
         ném `TypeError` khi cửa trả `data: null` — đúng lỗi `(e)` đã sửa ở
         `#nap-chon` *(`KQ-029 F-2`)*, sống sót ở chỗ thứ ba này. Thân rỗng
         là **một câu trả lời** *(câu rỗng dưới)*, ⛔ một ngoại lệ. */
      { la_rong: d => !d || !d.nguon || d.nguon.length === 0,
        rong: { icon: '—', tieu_de: 'Chưa đo được nguồn nào',
                cau: 'Lần đọc này không có nguồn nào để soi cách đọc ngày.' },
        so_dong: 3, con_hieu_luc: () => luot === _luot_thu_tu });
  }

  async function _khai_thu_tu(sid, tt, cid) {
    /* ⛔ Mot cua RIENG (`POST …/thu-tu`), ⛔ khong phai `khai-cot`: no doc
       `cot` hien hanh va ghi `version` moi **trong cung mot giao dich**, nen
       ⛔ khong co khe doc-sua-ghi de mot ban khai khac bi de lai bang ban cu. */
    await FLS.ghi('/sources/' + sid + '/thu-tu', { thu_tu: tt });
    await _ve_thu_tu(cid);
  }

  async function _khai_thu_tu_lo(cid, ids) {
    /* ⛔⛔ Than **chi** mang `source_ids` — ⛔ KHONG `thu_tu`. Cua se NO (400)
       neu man gui `thu_tu`, va cai NO ay la thiet ke: neu duong nay nhan duoc
       mot thu tu do man chon, no thanh co may khai `dmy` cho 27 nguon bang
       mot cu bam — dung cai `QĐ-ITL-113` dung ra de chan, chi nhanh hon.   */
    await FLS.ghi('/chup/' + cid + '/thu-tu', { source_ids: ids });
    await _ve_thu_tu(cid);
  }

  /* ── luoi xem truoc: **6 cot**, va cot thu 6 noi ro no ⛔ khong duoc doc */
  function _luoi_xem_truoc(d) {
    /* ⛔⛔ Ten truong den tu `window.FLS_TRUONG_CHUAN` — SINH ra tu
       `fls/adapters/sao_ke.SAU_TRUONG`. ⛔ Go tay o day la tao **ban khai
       thu hai**, dung thu cong #15 bat DO (*"ten cot phai truy duoc ve
       nguon"*).                                                          */
    const truong = window.FLS_TRUONG_CHUAN || [];
    const b = TP.bang([{ chu: 'Nguồn' }].concat(truong.map(function (t) {
      return { html: TP.chu(t.truong) + (t.doc_duoc ? ''
        : ' <span class="chip lock" title="Trường này có thể mang thông '
          + 'tin cá nhân, nên máy không đọc nó. Căn cứ: QĐ-ITL-92.">'
          + 'không đọc</span>') };
    })));
    const bang = b.bang, than = b.than;
    const khoa = {};
    (d.nguon || []).forEach(n => { khoa[n.source_id] = n.source_key; });

    (d.dong || []).forEach(function (r) {
      const tr = TP.el('tr');
      than.appendChild(tr);
      _td(tr).innerHTML =
        '<span class="mono tiny">' + TP.chu(khoa[r.source_id] || r.source_id)
        + '</span>';
      truong.forEach(function (t) {
        const c = _td(tr);
        if (!t.doc_duoc) {
          /* ⛔ O nay LUON rong, va no phai **trong nhu mot o bi chan**, ⛔
             khong trong nhu mot o tinh co thieu du lieu.                 */
          c.className = 'faint';
          c.textContent = '—';
          return;
        }
        const v = r.o[t.truong];
        /* ⭐ Hanh vi Sheets **#7 — so kieu ke toan**: tien can PHAI, chu can
           TRAI. Ke toan quet cot tien bang cach nhin **duoi cung mot mep**. */
        const la_tien = (t.truong === 'Debit' || t.truong === 'Credit');
        c.className = la_tien ? 'num' : 'mono';
        /* ⭐ `WO-022` §5b ⓔ: o tien in theo o `Currency` CUA CHINH DONG sao
           ke ay *(nguyen van nguon — `TP.tien` tu `trim` + viet HOA)*. Dong
           ⛔ co o ay *(cot chua khai)* ⇒ `undefined` ⇒ nhanh ma LA §5b ⓒ:
           in du chu so that, ⛔ doan tien te. */
        c.textContent = (v === '' || v === null || v === undefined)
          ? '—' : (la_tien ? TP.tien(v, r.o['Currency']) : String(v));
      });
    });

    if (d.so_dong > (d.dong || []).length) {
      const tr = TP.el('tr');
      than.appendChild(tr);
      const c = _td(tr);
      c.colSpan = truong.length + 1;
      c.className = 'muted tiny';
      c.textContent = 'còn ' + TP.so(d.so_dong - d.dong.length)
                    + ' dòng nữa, không hiện ở đây';
    }

    const boc = TP.el('div', 'gwrap');
    boc.appendChild(bang);
    return boc;
  }

  /* ═══════════════════════════════════ ④ BIEN BAN 9 luat ════════════ */
  /* ⭐⭐⭐ Man **LUON** goi cua LO, ke ca khi chi tick MOT nguon.
     ⛔⛔ Hai duong (mot-nguon / ca-lo) la **hai cho de chung lech nhau**, va
        cai lech ay se hien ra duoi dang *"soat thi thay 9 luat xanh, nap thi
        ra so khac"*. ⇒ Man co **MOT** duong; cua mot-nguon van con, nhung no
        la duong cua **test va phep do doi chung**, ⛔ khong phai duong nguoi
        dung di.                                                           */
  async function _soat() {
    if (!S.chup) return;
    const ds = _nguon_da_chon();
    if (!ds.length) return;
    S.nguon_soat = ds;
    const noi = TP.$('#nap-bb');
    noi.hidden = false;
    S.bien_ban = null;
    await TT.chay(noi,
      () => FLS.ghi('/nap/lo/xem-truoc',
                    { chup_id: S.chup.chup_id, source_ids: ds }),
      function (bb, _m, o) { S.bien_ban = bb; _ve_bien_ban(bb, o); },
      { la_rong: bb => !bb || !bb.luat, so_dong: 5 });
    _cap_nhat_nut();
  }

  function _ve_bien_ban(bb, o) {
    const chan = (bb.chan || []).length;
    const co = (bb.co || []).length;

    /* ⛔⛔ Dai NGUON dung TRUOC moi con so DONG (`QĐ-ITL-112`). Cau ke
       toan hoi la *"lo nay vao duoc khong, cai gi can"* — mot bien ban mo dau
       bang "8.365 dong" ma de "2 nguon bi chua" o cuoi la mot bien ban **tra
       loi dung cau ⛔ khong ai hoi**.                                      */
    const chua = (bb.nguon || []).filter(n => n.bi_chua);
    o.appendChild(TP.el('div', 'note ' + (chua.length ? 'warn' : 'ok'),
      chua.length
        ? '<b>' + TP.so(bb.so_nguon_vao) + ' nguồn vào sổ · '
          + chua.length + ' nguồn bị chừa.</b> Nguồn bị chừa có luật hạng '
          + 'chặn, nên nó không vào sổ — nhưng các nguồn còn lại vẫn vào. '
          + 'Bảng dưới nói rõ luật nào chừa nguồn nào.'
        : '<b>Cả ' + TP.so(bb.so_nguon) + ' nguồn đều vào sổ được.</b> '
          + 'Không nguồn nào có luật hạng chặn.'));

    const the = TP.el('div', 'grid4');
    [['Nguồn vào sổ', TP.so(bb.so_nguon_vao) + '/' + TP.so(bb.so_nguon),
      'nguồn bị chừa không tính'],
     ['Dòng vào', TP.so(bb.so_dong_vao), 'của các nguồn sẽ vào'],
     ['Dòng ra', TP.so(bb.so_dong_ra), 'sẽ vào sổ'],
     ['Dòng rỗng / lỗi', TP.so(bb.rong) + ' / ' + TP.so(bb.loi),
      'bỏ, có ghi nhận']]
      .forEach(function (x) {
        the.appendChild(TP.el('div', 'card',
          '<div class="pad"><div class="k">' + TP.chu(x[0]) + '</div>'
          + '<div class="v num">' + TP.chu(x[1]) + '</div>'
          + '<div class="muted tiny">' + TP.chu(x[2]) + '</div></div>'));
      });
    o.appendChild(the);

    const b = TP.bang([{ chu: 'Hạng', rong: '64px' }, { chu: 'Luật' },
                       { chu: 'Kết quả', rong: '104px' },
                       { chu: 'Đã đo', rong: '96px' },
                       { chu: 'Nguồn dính', rong: '120px' },
                       { chu: 'Thông điệp' }]);
    const bang = b.bang, than = b.than;

    bb.luat.forEach(function (k) {
      const h = HANG[k.hang] || HANG.CANH;
      const tr = TP.el('tr');
      than.appendChild(tr);
      tr.dataset.hang = k.hang;
      tr.dataset.dat = String(k.dat);
      _td(tr).innerHTML = TP.chip(h.lop, h.chu, h.ghi);
      _td(tr).innerHTML =
        '<span class="mono">' + TP.chu(k.ten) + '</span>';
      _td(tr).innerHTML = k.dat
        ? TP.chip('ok', 'đạt')
        : TP.chip(h.lop === 'lock' ? 'warn' : h.lop, 'không đạt');

      /* ⛔⛔ CO NAY LA CO CUA CA MAN. `da_do = 0` ⛔ **KHONG duoc trong giong
         mot con so binh thuong**: mot luat do duoc 0 thu la mot luat **chua
         do**, va no da cuu that mot lan (`L6` cong #17).                  */
      const c = _td(tr);
      if (Number(k.da_do) === 0) {
        c.innerHTML = TP.chip('crit', 'chưa đo',
          'Luật này đo được 0 thứ. Đo được 0 thứ thì chưa đo, và chưa đo '
          + 'thì không phải là đạt.');
      } else {
        c.innerHTML = '<span class="num">' + TP.so(k.da_do) + '</span>';
      }

      /* ⭐⭐ `QĐ-ITL-112` — **bung ra NGUON DINH**, ⛔ khong chi mot con so.
         Mot dong noi *"3 nguon khong dat"* ma ⛔ khong noi **nguon nao** thi
         ke toan ⛔ khong co buoc ke tiep nao de lam.                      */
      const cn = _td(tr, 'nowrap');
      const kd = k.nguon_khong_dat || [];
      const cd = k.nguon_chua_do || [];
      if (kd.length) {
        const bm = TP.el('button', null);
        bm.textContent = kd.length + ' nguồn';
        bm.dataset.bung = k.ten;
        bm.onclick = function () { _bung_nguon(tr, kd, cd); };
        cn.appendChild(bm);
      } else if (cd.length) {
        cn.innerHTML = TP.chip('lock', cd.length + ' chưa đo',
          'Những nguồn này đọc ra 0 dòng, nên luật không có gì để đo. '
          + 'Đó không phải khuyết tật.');
      } else {
        cn.innerHTML = '<span class="muted tiny">—</span>';
      }

      _td(tr).innerHTML =
        '<span class="muted tiny">' + TP.chu(k.thong_diep) + '</span>';
    });

    const boc = TP.el('div', 'gwrap');
    boc.appendChild(bang);
    o.appendChild(boc);

    o.appendChild(_bang_tung_nguon(bb));

    /* Dong ket luan — noi **ca ba** con so, ⛔ khong chi noi "xanh". */
    if (chan) {
      o.appendChild(TP.el('div', 'note crit',
        '<b>' + chan + ' luật hạng chặn không đạt. Không một dòng nào sẽ vào '
        + 'sổ.</b> Hạng chặn nghĩa là lỗi của hệ, không phải lỗi tệp của '
        + 'anh/chị. Báo cho người dựng hệ, kèm mã lần đọc '
        + TP.chu(S.chup.chup_id) + '.'));
    } else if (co) {
      o.appendChild(TP.el('div', 'note warn',
        '<b>' + co + ' luật hạng cờ đỏ, nhưng nút Nhận vẫn bật.</b> Đó là '
        + 'khuyết tật có sẵn trong dữ liệu kế toán, không phải lỗi của hệ. '
        + 'Những dòng ấy là tiền thật, nên chúng vào hàng chờ kèm lý do, '
        + 'chứ không bị bỏ.'));
    } else {
      o.appendChild(TP.el('div', 'note ok',
        '<b>Chín luật đều đạt.</b> Mỗi luật nói rõ nó đã đo bao nhiêu dòng '
        + 'ở cột Đã đo.'));
    }
  }

  /* ═══════════════════════════════════ ⑤ da nhan ════════════════════ */
  async function _nhan() {
    if (!S.bien_ban || (S.bien_ban.chan || []).length) return;
    const ds = S.nguon_soat || [];
    const rid = 'NAP-' + _hom_nay() + '-F04';
    const noi = TP.$('#nap-nhan');
    noi.hidden = false;
    await TT.chay(noi,
      () => FLS.ghi('/nap/lo', { chup_id: S.chup.chup_id, source_ids: ds,
                                 run_id: rid }),
      function (d, _m, o) {
        S.da_nhan = d;
        const the = TP.el('div', 'grid4');
        [['Mã lần nạp', d.run_id, 'ghim vào từng dòng sổ'],
         ['Vào sổ', TP.so(d.vao_so),
          TP.so(d.so_nguon_vao) + ' nguồn · ' + TP.so(d.so_nguon_chua)
          + ' bị chừa'],
         ['Bỏ qua vì trùng', TP.so(d.trung), 'đã có trong sổ'],
         ['Vào hàng chờ', TP.so(d.vao_hang_cho), 'kèm lý do']]
          .forEach(function (x) {
            the.appendChild(TP.el('div', 'card',
              '<div class="pad"><div class="k">' + TP.chu(x[0]) + '</div>'
              + '<div class="v num">' + TP.chu(x[1]) + '</div>'
              + '<div class="muted tiny">' + TP.chu(x[2]) + '</div></div>'));
          });
        o.appendChild(the);

        const di = TP.el('button', 'b pri');
        di.textContent = 'Mở hàng chờ để xử ' + TP.so(d.vao_hang_cho) + ' dòng';
        di.onclick = function () { UD.mo('man-f01'); };
        o.appendChild(TP.el('div', 'dstrip')).appendChild(di);

        /* ⛔⛔ CHANG 3 — man PHAI noi ra rang no DUNG O DAY. Im lang thi ke
           toan tuong da xong viec, roi van phai chep tay sang `A-CCR` ma
           ⛔ khong ai noi truoc.                                          */
        o.appendChild(TP.el('div', 'note warn',
          '<b>Dòng đã vào sổ của FLS, nhưng chưa sang A-CCR.</b> Cú đẩy sang '
          + 'A-CCR là một phép ghi vào sổ kế toán đang sống, và nó còn chờ '
          + 'chủ sổ cho phép: GAP-PLAN-05. Hôm nay khâu đó vẫn làm bằng tay.'));
      },
      { la_rong: d => !d || !d.run_id, so_dong: 4 });
  }

  function _hom_nay() {
    const d = new Date();
    const h = x => String(x).padStart(2, '0');
    return d.getFullYear() + '-' + h(d.getMonth() + 1) + '-' + h(d.getDate());
  }

  /* ── CA LO ──────────────────────────────────────────────────────────
     ✅ `GAP-SCR-15` DONG 08/09 (`QĐ-ITL-111`/`112`). Ban truoc: cua soat
     nhan **MOT** `source_id`, nen chon hon mot nguon thi nut `Soat` **TAT**
     va man **noi thang vi sao** — chon the chu ⛔ khong lang le soat nguon
     dau tien, vi lang le la **bao cao mot phep do ⛔ chua chay**.
     ⇒ Nay co cua lo, va man **luon** di duong ay.                         */
  function _nguon_da_chon() {
    /* ⛔ Loc theo bo loc dang bat: tick con nam trong `S.chon` khi doi bo
       loc, nhung nguoi dung ⛔ khong con **thay** chung ⇒ soat mot nguon ho
       ⛔ khong nhin thay la soat mot thu ho ⛔ khong chon.                 */
    const hien = new Set(_loc_nguon().map(n => n.source_id));
    return [...S.chon].filter(x => hien.has(x));
  }

  /* ⭐ Bung danh sach nguon dinh cua MOT luat — chen mot dong ngay duoi. */
  function _bung_nguon(tr, khong_dat, chua_do) {
    const co = tr.nextSibling;
    if (co && co.dataset && co.dataset.bung_cua === tr.dataset.hang + '') {
      co.remove();
      return;
    }
    const d = TP.el('tr');
    d.dataset.bung_cua = tr.dataset.hang + '';
    const c = _td(d);
    c.colSpan = 6;
    c.innerHTML =
      '<div class="note"><b>Nguồn không đạt:</b> '
      + TP.chu(khong_dat.join(' · '))
      + (chua_do.length
          ? '<br><span class="muted tiny">Và ' + chua_do.length
            + ' nguồn không có gì để đo (đọc ra 0 dòng): '
            + TP.chu(chua_do.join(' · ')) + '</span>'
          : '')
      + '</div>';
    if (tr.parentNode) tr.parentNode.insertBefore(d, tr.nextSibling);
  }

  /* ⭐⭐ Bang TUNG NGUON — **ke ca nguon bi chua, va NEU RO luat nao**.
     ⛔ Chua ma ⛔ khong noi vi sao thi ke toan ⛔ khong co duong nao sua, va
     cu bo tick lai quay ve **⛔ khong de lai vet** (`QĐ-ITL-111`).         */
  function _bang_tung_nguon(bb) {
    const b = TP.bang([{ chu: 'Nguồn' }, { chu: 'Vào sổ', rong: '96px' },
                       { chu: 'Dòng', rong: '88px' },
                       { chu: 'Đọc ngày', rong: '96px' },
                       { chu: 'Chừa vì luật' }]);
    (bb.nguon || []).forEach(function (n) {
      const tr = TP.el('tr');
      b.than.appendChild(tr);
      /* ⛔ `ngbb`, ⛔ KHONG `sid_bb`: bo chon cua DOM gia chi nhan
         `[a-z-]` ⇒ mot khoa `data-` co **gach duoi** thi
         `[data-sid_bb]` **⛔ khong khop gi ma cung ⛔ khong bao loi**
         — mot bai kiem se doc `[]` thanh *"man ⛔ khong ve bang"*.
         *(Da can that: mot bai DO 08/09.)* */
      tr.dataset.ngbb = String(n.source_id);
      _td(tr).innerHTML = '<span class="mono">'
        + TP.chu(n.source_key) + '</span>';
      _td(tr).innerHTML = n.bi_chua
        ? TP.chip('crit', 'bị chừa')
        : TP.chip('ok', 'vào sổ');
      _td(tr).innerHTML = '<span class="num">' + TP.so(n.so_dong_ra)
        + '</span>';
      /* ⛔ `thu_tu` rong hien **thanh chu**, ⛔ khong hien o trong. */
      _td(tr).innerHTML = n.thu_tu
        ? '<span class="mono">' + TP.chu(n.thu_tu) + '</span>'
        : TP.chip('lock', 'chưa khai',
                  'Nguồn này chưa ai ấn định cách đọc ngày. Dòng có ngày '
                  + 'đọc được hai cách sẽ vào hàng loại kèm lý do.');
      _td(tr).innerHTML = (n.chua_vi || []).length
        ? '<span class="muted tiny">' + TP.chu(n.chua_vi.join(' · '))
          + '</span>'
        : '<span class="muted tiny">—</span>';
    });
    const boc = TP.el('div', 'gwrap');
    boc.appendChild(b.bang);
    return boc;
  }

  function _cap_nhat_nut() {
    const bs = TP.$('#nap-nut-soat');
    const bn = TP.$('#nap-nut-nhan');
    /* ⛔ HAI o "vi sao": `Soat` o tren bien ban, `Nhan` o duoi. Mot cau
       chi hien o MOT cho la mot cau nguoi dung ⛔ khong thay khi ho dang
       dung o cho kia — va cho kia la cho co cu bam ghi vao so.          */
    const gcs = [TP.$('#nap-vi-sao'), TP.$('#nap-vi-sao-2')].filter(Boolean);
    if (!bs || !bn) return;

    const ds = _nguon_da_chon();
    bs.disabled = !(S.chup && ds.length > 0);

    /* ⛔⛔ LUAT NEN CUA MAN: co luat hang `CHAN` do ⇒ nut `Nhan` **TAT**. */
    const chan = S.bien_ban ? (S.bien_ban.chan || []).length : 0;
    bn.disabled = !S.bien_ban || chan > 0;

    {
      const chua = S.bien_ban ? (S.bien_ban.so_nguon_chua || 0) : 0;
      const cau =
        !S.chup ? 'Chọn một lần đọc ở bước 2 trước.'
        : !ds.length ? 'Chưa tick nguồn nào. Tick ít nhất một nguồn.'
        : !S.bien_ban
          ? 'Bấm Soát để lấy biên bản 9 luật cho ' + ds.length + ' nguồn.'
        : chan ? chan + ' luật hạng chặn đỏ trên mọi nguồn, nên nút Nhận tắt.'
        : chua
          ? 'Nhận được ' + (S.bien_ban.so_nguon_vao || 0) + ' nguồn. '
            + chua + ' nguồn bị chừa, xem bảng cuối biên bản.'
        : 'Biên bản không có luật hạng chặn. Nhận được.';
      gcs.forEach(g => { g.textContent = cau; });
    }
  }

  /* ═══════════════════════════════════════════════════════ ve ca man ═ */
  async function ve() {
    const oc = TP.$('#nap-chon');
    await TT.chay(oc,
      () => FLS.doc('/sources'),
      function (d, _m, o) {
        S.nguon = d.nguon || [];
        S.gap_trang_thai = d.gap_trang_thai || '';
        /* ⭐ Mac dinh **tick tat ca** — vi nut `Run` hom nay cung gom ca lo
           mot luot. Doi mac dinh la bat ke toan lam them mot viec ho ⛔ chua
           tung phai lam (`BA-06` §7 ⓶ ①).                                */
        if (!S.chon.size) S.nguon.forEach(n => S.chon.add(n.source_id));
        _ve_chon(o);
        _cap_nhat_nut();
      },
      /* ⭐ `WO-032` (e) *(`BA-06` v4.14 §5b *Năm trạng thái*, `KQ-029 F-2`)*:
         cửa trả `data: null` *(`?gia_lap=rong`)* ⇒ câu rỗng của khối, ⛔
         `TypeError` đọc `d.nguon` khi `d = null`. */
      { la_rong: d => !d || !d.nguon || d.nguon.length === 0,
        rong: { icon: '—', tieu_de: 'Kho chưa có nguồn nào',
                cau: 'Kho đã trả lời, và câu trả lời là chưa có dòng chảy '
                   + 'nào được nạp vào danh mục nguồn.' },
        so_dong: 5 });

    await _ve_doc(TP.$('#nap-doc'));
  }

  /* ⭐ `_ve_thu_tu` xuất ra *(`WO-032` vòng 2 `(k)`)* để bài DOM gọi **đúng
     hàm thật** — nó tự đi `TT.chay` + `FLS.doc`, nên bài ⛔ dựng thân nào. */
  return { ve: ve, _S: S, _soat: _soat, _nhan: _nhan,
           _cap_nhat_nut: _cap_nhat_nut, _ve_bien_ban: _ve_bien_ban,
           _ve_thu_tu: _ve_thu_tu };
})();
