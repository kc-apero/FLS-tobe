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
     ⚠ Ham nay ⛔ khong duoc dung de TINH. Moi phep cong tien phai o may chu.
     ⭐ *(`WO-022`, `BA-06` §5b ⓕ)*: phep cong / tru tien **TREN MAN** *(Σ hop
       ghep, lech, tong chum)* thi duoc — nhung **chi** tren so nguyen XU qua
       `xu()` ben duoi, ⛔ bao gio tren chuoi `tien()` da in, ⛔ bao gio tren
       `Number(v)` cong thang. Con so GUI LEN CUA van la chuoi cua tra (ⓖ). */

  /* ── ⭐⭐ SO LE THEO TIEN TE — `BA-06` v4.12 `UI-F10` §5b ⓐ *(`WO-022`)* ──
     ⛔⛔ **Loi that, do 02/10 *(`KQ-021 F-3`, may `8099` ca U)*:** ham in cu
       goi `toLocaleString('vi-VN', {maximumFractionDigits: 0})` cho **MOI**
       tien te ⇒ chum USD `1234.56` + `765.44` in **`1.235 USD`** · **`765
       USD`**. So that *(chi `SELECT`)*: **2.413 / 3.980** dong USD mang phan
       le — **da so** dong ngoai te in sai, trai thang `QĐ-ITL-62` *(ngoai te
       ⛔ dung sai, du vai xu)*: man **giau dung vai xu ay**. Khu hoi tren ca
       so that *(bai `AC-5`)*: ham cu lech **2.518 / 8.387** gia tri.
     ⭐ So le **ISO 4217**, **CO DINH** *(luon du — cot so thang hang, `UI-F3`
       `tabular-nums`)*. Khai **MOT cho** — dung **5** ma cua dang biet
       *(`man_f01_lenh.js` o chon tien te liet ke cung 5 ma)*.
     ⚠⚠ **Hai noi giu bang so le** *(Rui ro ③ cua `WO-022`)*: khi
       `fls_tien_te(ma, so_le)` ra doi *(`BA-05` `DD-I11` ❶)*, bang nay phai
       **DOC tu cua** — ⛔ de hai bang gia lech nhau trong im lang.
     ⛔ `Object.freeze`: sua bang luc chay o mot man la hai man in hai kieu. */
  const SO_LE = Object.freeze({ VND: 0, USD: 2, SGD: 2, HKD: 2, EUR: 2 });

  /* Thang cua kho: `numeric(20,2)` *(`ps_no`/`ps_co`/`amount`)* ⇒ toi da 2
     chu so le *co that*. ⛔ Trung voi so le USD chi la tinh co. */
  const LE_KHO = 2;

  /* ── tach CHUOI tien thanh ba manh — ⛔ qua `Number` ────────────────────
     ⛔⛔ `Number('1.005') * 100 = 100,49999…` · `4.35 * 100 = 434,99999…`
       *(Rui ro ② cua `WO-022`)*. Tach chuoi thi ⛔ co so thuc nao chen giua.
     Tra `{am, nguyen, le}` *(da LAM TRON MOT LAN ve `LE_KHO` chu so, nua ra xa
     0)* hoac `null` neu ⛔ phai mot so. `san = true` ⇒ **cat** thay vi lam
     tron *(cho DUNG SAI — xem `xu`)*.
     ⚠ Cua co the tra **so** *(`F04` xem truoc: o sao ke tho `66923.25`)* —
       `String(66923.25)` ra dung `66923.25` *(chuoi ngan nhat khu hoi)*; dang
       mu *(`5.55e-17`)* thi qua `toFixed`. */
  function _tach(v, san) {
    let s;
    if (typeof v === 'number') {
      if (!isFinite(v)) return null;
      s = String(v);
      if (/e/i.test(s)) s = v.toFixed(LE_KHO);
    } else {
      s = String(v).trim();
    }
    const m = /^([+-]?)(\d*)(?:\.(\d*))?$/.exec(s);
    if (!m || (m[2] === '' && !m[3])) return null;
    let nguyen = m[2].replace(/^0+(?=\d)/, '') || '0';
    const tho = m[3] || '';
    let le = (tho + '00').slice(0, LE_KHO);
    // ⭐ Lam tron MOT lan, nua ra xa 0 — chi khi chuoi dai hon thang kho
    if (!san && tho.length > LE_KHO && tho.charAt(LE_KHO) >= '5') {
      const tang = _cong_mot(nguyen + le);
      nguyen = tang.slice(0, tang.length - LE_KHO) || '0';
      le = tang.slice(-LE_KHO);
    }
    return { am: m[1] === '-' && !/^0+$/.test(nguyen + le),
             nguyen: nguyen, le: le };
  }

  /* `'0999'` + 1 = `'1000'` — cong tren CHUOI chu so, ⛔ tran `Number`. */
  function _cong_mot(s) {
    const a = s.split('');
    let i = a.length - 1;
    while (i >= 0) {
      if (a[i] === '9') { a[i] = '0'; i--; continue; }
      a[i] = String(Number(a[i]) + 1);
      return a.join('');
    }
    return '1' + a.join('');
  }

  /* `'1234567'` → `'1.234.567'` — `.` hang nghin *(§5b ⓓ, quy uoc `vi-VN`)*. */
  function _nhom(nguyen) {
    return nguyen.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  /* ── ⭐⭐ IN TIEN — `tien(gia_tri, ma_tien_te)` *(§5b ⓐ…ⓓ)* ─────────────
     ⓐ ma CO trong `SO_LE` ⇒ in **dung** so le cua no, co dinh:
        `('1234', 'USD')` → `1.234,00` · `('39457436', 'VND')` → `39.457.436`.
     ⓑ ⛔ **BAO GIO lam tron gia tri so khi in**: gia tri co **nhieu** chu so
        le khac 0 hon bang ⓐ *(hom nay: **11** dong VND — vd. `1306103.80`)*
        ⇒ in **du** theo thang kho *(`LE_KHO` = 2)* ⇒ `1.306.103,80`. Day la
        **mac dinh**; cau treo `Q-TIEN-1` *(owner)*. Doi theo owner = sua
        **mot** nhanh duoi day.
     ⓒ ma **LA hoac THIEU** *(`'20'` — **69** dong trong anh `fls_pm_line`;
        `null`)* ⇒ coi so le bang = **0**, ⛔ doan tien te: so nguyen in
        nguyen, co phan le in **du thang kho 2** — **dung nhu nhanh ⓑ**:
        `('100', '20')` → `100` · `('100.50', '20')` → `100,50`.
        ⭐⭐ *(v4.13, `WO-022` vong 2 — `TL-026`, yeu #1 cua `BG-027`)*: ⛔
        Vong 1 *(`BA-06` v4.11–v4.12)* cho nhanh nay **cat so 0 duoi**
        *(`100,5`)* trong khi ma trong bang lai in thang kho *(`,80`)* — **hai
        nhanh bat doi xung** cho cung mot tinh huong *"gia tri co phan le ma
        bang ⛔ cho"*. Mot cot cung ma co `100,5` canh `12,25` thi dau phay ⛔
        thang hang *(`UI-F3`)*. **Luat chung ⓐ+ⓑ+ⓒ:** so le in = bang cua ma
        neu gia tri vua bang, nguoc lai = `LE_KHO` *(kho `numeric(20,2)` ⇒
        chu so that cua gia tri so **la** 2)*. Tam so hom nay **0** dong doi
        chu *(ma la co le: `fls_pm_line` `'20'` 0 dong, `fls_itl` 0)*.
     ⓓ `.` nghin, `,` thap phan. Dau am **⛔ doi** *(`-0,40`)*; so **0** ⛔
        mang dau *(`'-0.00'` → `0,00`)*.
     ⚠ Ma tien te so khop sau khi `trim` + viet HOA: sao ke `F04` cho chuoi
       `Currency` **nguyen van nguon** *(`' usd'`)* — coi la ma la thi mot
       USD lai in `1.234,5`.
     ⛔ Chuoi ⛔ phai so *(o sao ke tho `'1,234.56'`)* ⇒ in **nguyen van da
       thoat** — hanh vi cu, ⛔ doan. */
  function tien(v, curr) {
    if (v === null || v === undefined || v === '') return '—';
    const t = _tach(v, false);
    if (!t) return chu(v);
    /* `WO-042 (c)`: **cùng** `ma_te` *(tập 30 ký tự)* — trước: `trim()` (25) */
    const ma = ma_te(curr);
    // ⓒ ma la / thieu ⇒ bang coi la 0 — ⛔ mot nhanh rieng *(v4.13)*
    const bang = Object.prototype.hasOwnProperty.call(SO_LE, ma)
      ? SO_LE[ma] : 0;
    // so chu so le CO THAT *(bo so 0 duoi)* — de biet co vua bang khong
    const that = t.le.replace(/0+$/, '').length;
    const n = that <= bang ? bang                      // ⓐ co dinh
                           : LE_KHO;                   // ⓑⓒ ⛔ lam tron so
    return (t.am ? '-' : '') + _nhom(t.nguyen)
         + (n > 0 ? ',' + t.le.slice(0, n) : '');
  }

  /* ── ⭐⭐ SO NGUYEN XU — `xu(gia_tri)` *(§5b ⓕ)* ─────────────────────────
     Doi chuoi cua tra sang **so nguyen don vi nho nhat** *(nhan `10^2` — thang
     kho, ⛔ so le cua tien te: VND co **11** dong co xu)* bang **TACH CHUOI**,
     lam tron MOT lan. Moi phep cong / tru / so tien tren man di qua day:
     **khop ⇔ lech nguyen = 0** *(ngoai te: `QĐ-ITL-62`)*.
     ⛔⛔ Truoc `WO-022`: Σ `0.10 + 0.20` tru tien bank `0.30` ra `5,55·10⁻¹⁷`
       ⇒ `Math.abs(lech) <= 0` *(dung sai ngoai te **0**)* ra `false` ⇒ hop
       ghep nhieu dong `F01` **khoa nut Ghep** tren mot chum **khop dung tung
       xu** ma cua ghi se nhan.
     `che_do = 'san'` ⇒ **CAT** phan sau xu thay vi lam tron — dung cho **DUNG
       SAI**: `|lech| <= ds` ⇔ `|lech_xu| <= san(ds × 100)` vi `lech_xu` la so
       nguyen. ⛔ Lam tron len *(`617.285` → `61729`)* thi man **cho** ghep mot
       lech `617,29` ma cua ghi *(`QĐ-ITL-63`: `min(1.000 đ, 0,5%)`)* **tu
       choi**.
     Tra `null` neu ⛔ phai so, hoac vuot so nguyen an toan cua `Number`
     *(`9·10^15` xu = 90 nghin ty — tien lon nhat so hom nay `11.742.361.787
     VND`)*: ⛔ tinh duoc thi noi ra, ⛔ mot so sai lang le. */
  function xu(v, che_do) {
    if (v === null || v === undefined || v === '') return null;
    const t = _tach(v, che_do === 'san');
    if (!t) return null;
    const n = Number(t.nguyen + t.le);
    if (!Number.isSafeInteger(n)) return null;
    return t.am ? -n : n;
  }

  /* So nguyen xu → chuoi kieu CUA *(`-40` → `'-0.40'`)* — de dua lai vao
     `tien()`. ⛔ Gui chuoi nay len cua thay chuoi cua tra (ⓖ). */
  function chuoi_xu(n) {
    const a = String(Math.abs(n)).padStart(LE_KHO + 1, '0');
    return (n < 0 ? '-' : '') + a.slice(0, a.length - LE_KHO) + '.'
         + a.slice(-LE_KHO);
  }

  /* ⭐⭐ `WO-032` *(`BA-06` v4.14 §5b ⓕ)* — mã tiền tệ để **SO**: `trim` +
     chữ hoa; ⛔ có ⇒ `''`. **Lệch CHỈ có khi CÙNG tiền tệ**: màn so mã
     **TRƯỚC** khi đổi sang xu *(`QĐ-ITL-62` — ngoại tệ ⛔ có dung sai; cửa ghi
     `ghep_lenh` ném `KhacTienTe`)*. ⛔ Trước: hộp *Tìm tiền* trừ `100.000 VND`
     cho `100.000,00 USD` ⇒ *"lệch 0 ⇒ trong dung sai"* — **4** lệnh sổ thật
     *(`KQ-031 F-1`)*. Cùng luật với `fls/repo/man_ghep.py::ma_tien_te` phía
     cửa — hai phía, **một** phép so. */
  /* ⛔⛔ `KQ-041 F-2` *(`WO-042 (c)`, `BA-07` v3.11)*: `String.trim()` gỡ
     **25** ký tự *(đo bằng `node`)* — **có** `U+FEFF` mà Python ⛔ gỡ, **thiếu**
     `U+001C`…`U+001F` ＋ `U+0085` mà Python gỡ. Một chuỗi `'USD' + U+0085`
     là `USD` ở cửa mà là một mã **lạ** ở màn *(in `1.234,5` thay `1.234,50`)*.
     ⇒ **Một** tập `TAP_TRANG_TIEN_TE` *(30 = Python `isspace` 29 ＋ `U+FEFF`)*,
       **bản chép** của `fls/canon/tien_te.py` — trình duyệt ⛔ nhập được
       Python; bài `tests/web/test_wo042_mot_tap_ky_tu_trang.py` so hai tập
       **từng ký tự**. Viết bằng **số điểm mã**: 22 / 30 ký tự **vô hình**
       trong trình soạn thảo. ⛔ `U+200B` *(cả ba ngôn ngữ đều ⛔ gỡ — giữ thế)*. */
  const TAP_TRANG_TIEN_TE = String.fromCharCode(
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D,
    0x001C, 0x001D, 0x001E, 0x001F,
    0x0020, 0x0085, 0x00A0, 0x1680,
    0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005,
    0x2006, 0x2007, 0x2008, 0x2009, 0x200A,
    0x2028, 0x2029, 0x202F, 0x205F, 0x3000, 0xFEFF);

  /* ⭐ **Một** hàm mã tiền tệ của màn: gỡ `TAP_TRANG_TIEN_TE` ở hai mép +
     chữ hoa *(⛔ `String.trim()`)*. `TP.tien` gọi nó cho mã in số lẻ. */
  function ma_te(c) {
    const s = String(c === null || c === undefined ? '' : c);
    let a = 0, b = s.length;
    while (a < b && TAP_TRANG_TIEN_TE.indexOf(s[a]) >= 0) a++;
    while (b > a && TAP_TRANG_TIEN_TE.indexOf(s[b - 1]) >= 0) b--;
    return s.slice(a, b).toUpperCase();
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

  /* ── ⭐⭐ Bang: dung bang `createElement`, ⛔ KHONG bang `innerHTML` ─────
     `tieu_de` = [{chu, rong}] ⇒ tra `{bang, than}`.

     ⛔⛔ **Vi sao mot ham thay vi mot chuoi HTML — va ly do ⛔ khong phai gon.**
     Dung `<thead>…<tbody>` bang `innerHTML` thi **chay dung tren trinh
     duyet** nhung `tBodies` **rong** tren DOM toi thieu cua bo test — vi
     `dom_gia.js` **CO Y ⛔ khong phan tich HTML** *(*"bai kiem nao can cau
     truc that thi phai dung `createElement`"*)*.

     ⇒ Mot cai luoi chi ton tai duoi dang **chuoi** la mot cai luoi **⛔ khong
       may nao soi duoc**: ⛔ khong bai nao dem duoc so cot, ⛔ khong bai nao
       doc duoc lop cua mot o. Da vap dung cho nay khi viet `F04` *(16 bai do
       cung mot luc voi `tBodies[0] is undefined`)*.

     ⚠ Nen han che nay cua DOM gia la mot **rang buoc tot**, ⛔ khong phai mot
       cho bat tien de ne: no ep cau truc phai la **cay the that**.          */
  function bang(tieu_de) {
    const t = el('table', 'g');
    const dau = el('thead');
    const tr = el('tr');
    (tieu_de || []).forEach(function (h) {
      const th = el('th');
      /* ⭐ `lop` — them 11/09 cho `G5`. Can de ghim cot (`f1`/`f2`): lop
         sticky phai nam tren **ca `th` lan `td`**, ⛔ khong chi `td` — neu
         thieu o `th` thi dong tieu de troi ngang trong khi than bang dung
         yen, va bang **lech dau** ngay lan cuon dau tien.
         ⛔ Them, ⛔ khong doi: moi luoi cu ⛔ khong truyen `lop` van chay y
         nguyen — day la mot khoa **tuy chon**. */
      if (h.lop) th.className = h.lop;
      if (h.rong) th.style.width = h.rong;
      if (h.html !== undefined) th.innerHTML = h.html;
      else th.textContent = h.chu || '';
      tr.appendChild(th);
    });
    dau.appendChild(tr);
    const than = el('tbody');
    t.appendChild(dau);
    t.appendChild(than);
    return { bang: t, than: than };
  }

  return { chu, tien, xu, chuoi_xu, ma_te, TAP_TRANG_TIEN_TE, SO_LE, so, NIEM_TIN, chip_niem_tin,
           chip, el, $, bang };
})();
