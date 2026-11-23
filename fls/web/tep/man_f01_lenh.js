/* ═══════════════════════════════════════════════════════════════════════
   man_f01_lenh.js — **LẰN LỆNH CHI** của màn hàng chờ (`GAP-SCR-14`).

   ⛔⛔⛔ **Vì sao lằn này ra đời, và vì sao nó là lằn MẶC ĐỊNH.**

   Chủ sổ chốt chiều đo ngày 09/09 (`QĐ-ITL-122`):

     > *"Trans map vào PM. Số lượng Trans vốn nhiều hơn PM; không cần
     >  question các Trans không được map."*

   Đo trên bảng tuyến cùng ngày: **10** cửa khoá theo dòng tiền, ⛔ **0** cửa
   khoá theo dòng lệnh. Nghĩa là cả hệ ⛔ **không có một đường nào** hỏi được
   câu *"lệnh chi nào chưa tìm được tiền"* — tức **đúng câu hỏi của việc**. Và
   lằn cũ đang hiển thị **7.682** dòng tiền, tức đang hỏi **đúng cái câu chủ
   sổ vừa nói là ⛔ không cần hỏi**.

   ★ Hai con số của cùng một kho, đọc cạnh nhau:

     · hỏi phía TIỀN : **5.684** dòng chưa nối · **799** dòng để phủ 90% tiền
     · hỏi phía LỆNH : **1.345** dòng chưa có tiền · ⭐ **69** dòng để phủ 90%

   ⇒ **69** thay vì **799**: chênh **11,6 lần**, và **cùng một dữ liệu**.

   ⛔⛔ **Và lằn này ⛔ KHÔNG mở một đường GHI thứ hai.** Cú ghép vẫn gọi
   `POST /queue/{itl_id}/match` — đúng cửa ghi cũ. Lằn này chỉ **đổi thứ tự
   hỏi**: chọn dòng lệnh trước, rồi chọn dòng tiền.

   ⭐ Luật **⛔ không gộp tiền tệ** giữ nguyên từng chữ (`QĐ-ITL-58`). Ở đây nó
   còn gắt hơn: dòng lệnh **USD** nhiều hơn **VND** (700 vs 590), nên gộp lại
   thì cả vế USD bị dìm xuống dưới.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

const F01L = (function () {

  const ST = { curr: null, duyet: '', con_tro: null, dong: [], het: false,
               ro: null, tu_chung: null, du_cot: false, vua_ghep: new Map() };

  /* ⛔⛔ **Ô thân phải NHỚ.** Lằn này được vẽ vào một ô do `F01` cấp — nó
     ⛔ **không có `id` riêng**. Nếu ⛔ không nhớ, thì mọi lần `ve()` gọi lại
     sau một cú ghép sẽ ⛔ không tìm thấy ô nào ⇒ lưới **⛔ không tươi lại** mà
     cũng ⛔ **không báo lỗi** — đúng loại lỗi im lặng khó thấy nhất. */
  let _than = null;

  const CO_GHI = () => !!(window.FLS_PHIEN || {}).cho_ghi;

  /* Bậc dùng **cùng một bộ tên** với lằn dòng tiền — cố ý: hai lằn nói cùng
     một từ cho cùng một ý. Đổi tên ở một phía sẽ làm người đọc tưởng đây là
     hai thang đo khác nhau. */
  const BAC = {
    ma:           ['ok',   'mã khớp'],
    tien:         ['info', 'tiền khớp'],
    gan_tien:     ['warn', 'gần tiền'],
    cung_tien_te: ['lock', 'cùng tiền tệ'],
    /* ⭐ `WO-032` *(`BA-07` v3.7 §4h ⓹)*: bậc **chỉ** cửa `/so` sinh — dòng
       toàn sổ ⛔ khớp mã, **khác tiền tệ** lệnh. Tông `crit` đã có của `TP.chip`
       *(⛔ token mới)*: cửa ghi sẽ **từ chối** cặp này. */
    khac_tien_te: ['crit', 'khác tiền tệ']
  };

  function _chan_ghi(nut) {
    if (CO_GHI()) return false;
    nut.disabled = true;
    nut.title = '⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC. Mọi thao tác ghi bị trả '
              + '405. Khởi động lại máy chủ với --cho-ghi (nó sửa SỔ THẬT).';
    return true;
  }

  function _nut(nhan, lop, ham) {
    const b = TP.el('button', 'b tiny' + (lop ? ' ' + lop : ''), nhan);
    if (!_chan_ghi(b)) b.onclick = ham;
    return b;
  }

  /* ⭐⭐ `WO-045` ② ⓒ *(`BA-06` v4.19 `§4.5 ⓦ` ② — `BG-044` phát hiện ngoài
     phạm vi)*: nút **ĐỌC** ⛔ đi qua `_chan_ghi`. Bản trước dựng **mọi** nút
     bằng `_nut` ⇒ ở chế độ chỉ đọc *(mặc định — `NFR-I03`, luật về đường
     **ghi**)* cả `Xem thêm` lẫn nút mở hộp `Tìm tiền` mỗi hàng bị khoá kèm câu
     *"Mọi thao tác ghi bị trả 405"* cho một thao tác **⛔ ghi** ⇒ mỗi rổ chỉ
     thấy **50** dòng đầu *(sổ thật 05/10: `may` chưa nhận theo lô 50 / 120 ·
     `nguoi` 50 / 616 · `khong` 50 / 801)*. Màn `F01` *(`Xem thêm` gắn
     `onclick` thẳng)* ⛔ có lỗi này — lệch **giữa hai màn**, ⛔ chủ ý.
     ⇒ Đọc chạy ở **mọi** chế độ; nút **`Ghép`** trong hộp vẫn khoá + câu
     `405` *(`_drawer_tim_tien`)*. ⛔ Đổi câu `405`. */
  function _nut_doc(nhan, lop, ham) {
    const b = TP.el('button', 'b tiny' + (lop ? ' ' + lop : ''), nhan);
    b.onclick = ham;
    return b;
  }

  /* ⭐⭐ `WO-045` ② ⓐⓑ *(`BG-044` `(d)` #6 · #7)*: **lượt mới nhất** của lưới.
     Bản trước: `_loc` đặt `ST.dong = []`, lượt rổ trước về sau **nối** vào
     *(`_ve_luoi` `concat`)* ⇒ lưới trộn hai rổ — cùng hình `F-3` của `②b`
     *(bài `test_AC4_doi_ro_…` đỏ trên `db0adae`: `['may', 'may', 'nguoi']`)*;
     `Xem thêm` bấm hai lần ⇒ hai `GET` cùng con trỏ ⇒ hàng lặp. Mỗi lần
     `ve()` dựng lại lưới *(lưới cũ rời cây)* là một lượt mới; mỗi lượt tải /
     lật trang mang số lượt và **⛔ chạm** `ST` khi đã bị thay. */
  let _luot_luoi = 0;

  /* ══ ① CHÂN MÀN — theo TỪNG tiền tệ, ⛔ không có dòng "tổng" ══════════ */
  /* ⚠ Khuôn `TT.chay` gọi `ve(data, meta, o)` — **ba** tham số, đúng thứ tự
     ấy. Tự viết `try/catch` ở đây là **bỏ mất hai trạng thái** *(đang tải ·
     rỗng)* mà `BA-06` đòi mọi lưới phải có. */
  function _ve_tom(data, meta, o) {
    o.innerHTML = '';
    const hang = (data && data.theo_tien_te) || [];
    const b = TP.bang([{chu: 'Tiền tệ'}, {chu: 'Dòng chờ'},
                       {chu: 'Phiếu'}, {chu: 'Tiền'}, {chu: 'Đã duyệt'},
                       {chu: '⛔ Chưa duyệt'},
                       {chu: 'Xem mấy dòng là phủ 90% tiền'}]);
    b.than.innerHTML =
      hang.map(r =>
        '<tr><td><b>' + TP.chu(r.curr || '?') + '</b></td>'
        + '<td class="r num">' + TP.so(r.so_dong) + '</td>'
        + '<td class="r num">' + TP.so(r.so_phieu) + '</td>'
        + '<td class="r num">' + TP.tien(r.tien, r.curr) + '</td>'
        + '<td class="r num">' + TP.so(r.so_dong_duyet) + '</td>'
        + '<td class="r num">' + (Number(r.so_dong_chua_duyet)
            ? TP.chip('warn', TP.so(r.so_dong_chua_duyet)) : '0') + '</td>'
        /* ⭐ `null` = ⛔ KHÔNG ĐO ĐƯỢC (Σ tiền = 0), ⛔ không phải 0 dòng.
           Vẽ `0` ở đây nói *"xem 0 dòng là đủ"* — một câu sai. */
        + '<td class="r num">' + (r.so_dong_phu == null
            ? '⛔ không đo được'
            : '<b>' + TP.so(r.so_dong_phu) + '</b> ⇒ ' + TP.chu(r.pct_that)
              + '%') + '</td></tr>').join('');
    o.appendChild(b.bang);
    o.appendChild(TP.el('div', 'hint',
      '⛔ <b>⛔ Không có dòng “tổng”</b> — cộng hai đơn vị tiền ra một con số '
      + 'là vô nghĩa, và ở đây nó còn dìm cả vế USD xuống dưới.'));
    /* ⭐⭐ Hai loại việc, nói tách ra. Gộp lại thì kế toán tưởng họ còn
       1.345 việc trong khi phần họ làm được chỉ là 1.070. */
    const cd = hang.reduce((s, r) => s + Number(r.so_dong_chua_duyet || 0), 0);
    if (cd) {
      o.appendChild(TP.el('div', 'note warn',
        '⚠ <b>' + TP.so(cd) + ' dòng lệnh ⛔ chưa được duyệt</b> — cửa ghép '
        + 'đòi <code>force</code> kèm lý do, nên chúng ⛔ <b>không phải việc '
        + 'của kế toán ITL</b>. Bộ lọc bên dưới tách được chúng ra.'));
    }
  }

  function ve_tom(o) {
    return TT.chay(o, () => FLS.doc('/queue/lenh-cho/summary'), _ve_tom, {
      so_dong: 4,
      la_rong: x => !((x && x.theo_tien_te) || []).length,
      /* ⭐ RỖNG ở đây là một tin TỐT, và màn phải nói ra là tin gì — ⛔ không
         để một ô trắng cho người đọc tự đoán là *"cửa hỏng"*. */
      rong: '⭐ ⛔ Không còn dòng lệnh nào chờ tiền. Nếu điều này lạ thì hãy '
            + 'xem ảnh chụp lệnh chi ở màn Cổng hôm nay — một ảnh RỖNG cũng '
            + 'cho ra đúng màn hình này.'
    });
  }

  /* ══ ② THANH LỌC ═════════════════════════════════════════════════════ */
  function _thanh_loc(o) {
    const th = TP.el('div', 'bar');
    th.appendChild(TP.el('span', 'lbl', 'Trạng thái lệnh'));
    const s = TP.el('select', 'inp');
    s.innerHTML = '<option value="">tất cả</option>'
                + '<option value="1">chỉ đã duyệt</option>'
                + '<option value="0">⛔ chỉ chưa duyệt</option>';
    s.value = ST.duyet;
    s.onchange = function () {
      ST.duyet = s.value; ST.con_tro = null; ST.dong = []; ve();
    };
    th.appendChild(s);
    o.appendChild(th);
  }

  /* ══ ⓪ VIỆC CỦA BẠN HÔM NAY ═════════════════════════════════════════ */
  /* ⛔⛔⛔ **Vì sao khối này ra đời, và nó sửa lỗi của CHÍNH TÔI.**

     Owner mở màn `G2` và nói: *"tôi ⛔ không hiểu ý nghĩa của những bảng
     thông tin này, có gì cần nhìn không"*. Đó ⛔ **không phải** lời chê
     *"chưa đẹp"* — nó là **⛔ không hiểu**, và nó đúng: ba bảng đầu màn là
     thứ **tôi** dựng để **tự chứng minh phép chia đúng** *(ba rổ có khép về
     `1.553` không)*. Đó là việc của **tôi**, ⛔ không phải của kế toán — mà
     tôi để nó chiếm hai phần ba màn hình, **đứng TRÊN** chỗ có việc.

     ⇒ Khối này trả lời đúng một câu — ***"hôm nay tôi phải làm gì"*** — bằng
       **ba dòng**, và mỗi dòng có **một** nút dẫn thẳng tới đúng tập ấy.
       Ba bảng kia lui xuống sau một nút *"Số liệu kiểm chứng"*: chúng ⛔ vẫn
       phải còn *(cổng của dự án là ⛔ không giấu con số)*, nhưng chúng ⛔
       không được đứng trước việc. */
  /* ⭐⭐ `WO-037` vòng 2 `(i)` *(`BA-06` v4.17 `§4.5 ⓤ` — chữ NGUYÊN VĂN)*.
     ⛔⛔ **Bia `BG-039` yếu #1.** Vòng 1 đưa lệnh khớp mã **chỉ** ở tiền tệ
     khác từ rổ `may` sang `nguoi` ⇒ rổ `nguoi` có **hai** loại lệnh, mà dòng 2
     vẫn nói *"⛔ Chưa có số chứng từ"* cho cả rổ — sổ thật 02/10 sai **84 /
     616**. Dòng ghi chú `may − tu_chung` nói *"lệch tiền — trả nhiều đợt"* cho
     cả nhóm — đúng **78 / 120** *(39 lệnh có **một** dòng cùng tệ khớp **đúng**
     tiền mà cửa ghi vẫn ⛔ nhận theo lô; cổng nào giữ chúng: chưa đo ⇒ câu ⛔
     khẳng định)*.
     ⇒ Hai câu theo `a = nguoi − nguoi_khac_tien_te`, `b = nguoi_khac_tien_te`
       **của CỬA** *(`/lenh-cho/ro`)*. ⛔ Màn tự đếm `b` từ trang đang xem: nó
       chỉ thấy một trang *(lớp lỗi `do_phu` dừng ở 500)*. `b = 0` ⇒ chỉ câu ①;
       `a = 0` ⇒ câu ① vẫn in `0 dòng…` *(một con số `0` là một câu trả lời)*.
     ⚠ Dòng 2 + ghi chú dựng bằng **phần tử**, ⛔ chuỗi HTML: hai câu là hai
       con số của cửa, và bài DOM *(`test_wo037_v2_bang_f01l_cua_that.py`)* so
       từng chuỗi. Chữ ⛔ ký hiệu `⛔ ⚠ ⭐ 🔒` *(luật ký hiệu màn hình)*. */
  const CAU_NGUOI_1 = ' dòng chưa có số chứng từ: tra bằng tiền + ngày.';
  const CAU_NGUOI_2 = ' dòng có số chứng từ nhưng dòng tiền khớp mang tiền tệ '
                    + 'khác: cửa ghi chưa ghép được hai tiền tệ.';

  /* ⛔⛔ **Bia `KQ-041 F-1`** *(`fls-test` 05/10, sổ thật chỉ đọc, hàm thật
     `ds_tu_chung`, ảnh `NAP-2026-10-02-PMA07ED283`)*: ba chỗ khác của `F01L`
     vẫn hứa *"lệch tiền"* / *"khớp đúng một dòng — người chỉ DUYỆT"* cho cả
     rổ `may`. Rổ `may` **184** = tự chứng **64** ＋ cửa ghi ⛔ nhận theo lô
     **120**; trong **120**: lệch tiền **78** · nhiều dòng tiền cùng mã có dòng
     khớp **3** · **một** dòng khớp **đúng tiền 39** — giữ vì `chum_lech_tien`
     **25** *(một dòng tiền mang mã của nhiều dòng LỆNH, Σ chùm ≠ tiền bank)* ＋
     `co_dong_chua_duyet` **14** ⇒ *"lệch tiền"* đúng **78 / 120**, *"chỉ
     DUYỆT"* sai **120 / 184**; câu v4.17 *"nhiều dòng tiền cùng mã"* gọi
     `chum_lech_tien` sai tên *(đó là nhiều dòng **lệnh**)*.
     ⇒ `BA-06` v4.18 `§4.5 ⓤ`: **một** câu nêu đủ lý do cửa ghi giữ, dùng ở
       **hai** chỗ *(ghi chú băng ⓐ + `note ok` dưới bảng rổ ⓑ)* — **một** hằng,
       ⛔ hai bản gõ *(hai bản sẽ lệch nhau đúng một ký tự, rồi một bài so chuỗi
       xanh ở chỗ này đỏ ở chỗ kia)*. Mở đầu **một** dấu cách. Vế *"cổng khác"*
       giữ dù hôm nay **0** lệnh *(`ung_vien_da_bi_ghep`)* — câu ⛔ khẳng định
       thiếu khi sổ đổi. Lý do **từng hàng** ⇒ `GAP-SCR-34` *(khoá cửa mới,
       phiếu sau)*. */
  const LY_DO_LO = ' khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận '
    + 'theo lô — lệch tiền, nhiều dòng tiền cùng mã, một dòng tiền mang mã của '
    + 'nhiều dòng lệnh mà tổng các dòng lệnh khác tiền bank, có dòng lệnh cùng '
    + 'chùm chưa được duyệt, hoặc vướng một cổng khác của cửa ghi.';
  const MO_TUNG_DONG = ' Phải mở từng dòng.';

  function cau_ro_nguoi(data) {
    const b = data.nguoi_khac_tien_te || 0;
    const a = (data.nguoi || 0) - b;
    return TP.so(a) + CAU_NGUOI_1 + (b > 0 ? ' ' + TP.so(b) + CAU_NGUOI_2 : '');
  }

  function _ve_viec(data, meta, o) {
    o.innerHTML = '';
    const tc = data.tu_chung || 0;
    const can_hoi = (data.may || 0) - tc;
    const viec = [
      /* ⭐⭐ `tu_chung` ở đây là **cửa GHI nói thế** (`ds_tu_chung`), ⛔ không
         phải phép đo của màn hình. Bản trước tôi tự tính và ra **90**, trong
         khi cửa ghi chỉ nhận **47** ⇒ một nút *"Duyệt cả 90"* sẽ bị **từ chối
         CẢ LÔ**. Một con số hứa nhiều hơn cái bấm được là một con số nói dối. */
      ['ok', tc, 'máy ghép được — bạn chỉ DUYỆT',
       'Cửa ghi ĐÃ soi cả bốn cổng và nhận. ⛔ Không cần suy nghĩ.',
       'Duyệt cả ' + tc + ' dòng', function () { _mo_lo(); }],
      ['warn', data.nguoi || 0, 'CẦN BẠN tra — máy chưa đề xuất được dòng tiền',
       cau_ro_nguoi(data),
       'Bắt đầu tra', function () { _loc('nguoi', null); }],
      ['lock', data.khong || 0, '⛔ KHÔNG làm được — đừng động vào',
       'Có số chứng từ nhưng ⛔ không dòng tiền nào trong sổ mang số ấy. '
       + 'Ngồi tìm là phí công.',
       'Xem vì sao', function () { _loc('khong', null); }]
    ];
    viec.forEach(function (v) {
      const d = TP.el('div', 'viec');
      d.appendChild(TP.el('span', 'chip ' + v[0], TP.so(v[1]) + ' dòng'));
      const ten = TP.el('span', 'viec-ten');
      ten.appendChild(TP.el('b', '', v[2]));
      ten.appendChild(TP.el('div', 'hint', v[3]));
      d.appendChild(ten);
      const b = TP.el('button', 'b tiny pri', v[4]);
      b.onclick = v[5];
      d.appendChild(b);
      o.appendChild(d);
    });
    /* ⚠ `160` dòng khớp mã nhưng LỆCH tiền ⛔ không nằm trong ba dòng trên —
       chúng ⛔ không phải *"bấm duyệt"* mà cũng ⛔ không phải *"⛔ không làm
       được"*. Nói ra, ⛔ không để chúng biến mất giữa hai nhóm. */
    if (can_hoi > 0) {
      /* `WO-037` vòng 2 *(`§4.5 ⓤ`)*: ⛔ còn hứa *"lệch tiền"* cho cả nhóm.
         `WO-042 (b)` ⓐ *(v4.18)*: câu chung `LY_DO_LO` — v4.17 gọi
         `chum_lech_tien` là *"nhiều dòng tiền cùng mã"* và ⛔ nói cổng
         `co_dong_chua_duyet`. Dấu cách cuối ngăn câu với liên kết. */
      const n = TP.el('div', 'note warn');
      n.appendChild(TP.el('span', '',
        'Còn ' + TP.so(can_hoi) + ' dòng' + LY_DO_LO + MO_TUNG_DONG + ' '));
      const a = TP.el('a', '', 'Xem ' + TP.so(can_hoi) + ' dòng');
      a.href = '#'; a.id = 'f01l-lech';
      a.onclick = function (e) { e.preventDefault(); _loc('may', false); };
      n.appendChild(a);
      o.appendChild(n);
    }
  }

  /* ⛔⛔⛔ **DÙNG LẠI khối lô của lằn TIỀN, ⛔ KHÔNG dựng cái thứ hai.**
     `F01.ve_lo` đã gọi `GET /queue/tu-chung` rồi `POST /queue/match-lo` —
     đúng **một** đường ghi. Dựng một khối lô riêng cho lằn này là mở **đường
     ghi thứ hai** vào `fls_pm_link`, và hai đường sẽ lệch nhau ở bốn cổng
     của `ghep_lenh` — đúng thứ `test_KHONG_them_mot_duong_GHI_nao` canh. */
  function _mo_lo() {
    const than = _than;
    if (!than) return;
    than.innerHTML = '';
    const b = TP.el('div', 'bar');
    const q = TP.el('button', 'b tiny', '← Quay lại');
    q.onclick = function () { ve(); };
    b.appendChild(q);
    b.appendChild(TP.el('span', 'lbl',
      'Duyệt theo lô — cùng một cửa ghi với lằn dòng tiền'));
    than.appendChild(b);
    const c = TP.el('div', 'card');
    than.appendChild(c);
    F01.ve_lo(c);
  }

  function _loc(ro, tu_chung) {
    ST.ro = ro; ST.tu_chung = tu_chung;
    ST.con_tro = null; ST.dong = []; ST.het = false;
    ve();
  }

  function ve_viec(o) {
    return TT.chay(o, () => FLS.doc('/queue/lenh-cho/ro'), _ve_viec, {
      so_dong: 3,
      la_rong: x => !x || !x.tong,
      rong: '⭐ ⛔ Không còn dòng lệnh nào chờ tiền — ⛔ không có việc gì hôm nay.'
    });
  }

  /* ══ ②b BA RỔ — *"AI trả lời được câu này"* (`BA-12 §2`, `G2`) ════════ */
  /* ⛔⛔⛔ Đo 11/09 trên 1.553 dòng lệnh chưa nối: **250** máy trả lời được
     và **768** ⛔ không ai trả lời được ở FLS ⇒ **1.018 = 65,6%** danh sách
     ⛔ **không phải việc ghép** của kế toán. Trước `G2` cả ba loại nằm lẫn
     trong một bảng, ⛔ không một chữ phân biệt. */
  const RO = {
    /* `WO-042 (b)` ⓓ *(`BA-06` v4.18)*: câu cũ *"khớp đúng một dòng tiền
       trong sổ — người chỉ DUYỆT"* sai **120 / 184** *(chỉ **64** tự chứng
       duyệt theo lô được)*. */
    may:   ['ok',   'máy trả lời được',
            'Số chứng từ khớp ít nhất một dòng tiền cùng tiền tệ — máy đề xuất '
            + 'được dòng tiền. Dòng tự chứng được duyệt theo lô; các dòng còn '
            + 'lại phải mở từng dòng.'],
    /* `WO-037` vòng 2 *(`§4.5 ⓤ`)*: rổ có **hai** loại lệnh — câu cũ *"⛔
       Chưa có số chứng từ"* sai cho 84 / 616 *(sổ thật 02/10)*. */
    nguoi: ['warn', 'cần người tra',
            'Máy chưa đề xuất được dòng tiền — chưa có số chứng từ, hoặc số '
            + 'chứng từ khớp một dòng tiền bằng tiền tệ khác. Mỗi dòng nói vì sao.'],
    khong: ['lock', '⛔ không ai trả lời được',
            'Có số chứng từ nhưng ⛔ KHÔNG dòng tiền nào trong sổ mang số ấy. '
            + 'Ngồi tìm là phí công — xem cột “vì sao”.']
  };

  function _ve_ro(data, meta, o) {
    o.innerHTML = '';
    const b = TP.bang([{chu: 'Rổ'}, {chu: 'Dòng'}, {chu: 'Nghĩa là gì'}]);
    ['may', 'nguoi', 'khong'].forEach(function (k) {
      const r = RO[k];
      const tr = TP.el('tr');
      tr.appendChild(TP.el('td', '', TP.chip(r[0], r[1])));
      tr.appendChild(TP.el('td', 'num r', '<b>' + TP.so(data[k] || 0) + '</b>'));
      tr.appendChild(TP.el('td', '', r[2]));
      b.than.appendChild(tr);
    });
    o.appendChild(b.bang);
    /* ⭐ Ba rổ phải KHÉP về tổng. Một bảng phân loại ⛔ không cộng về tổng là
       một bảng ⛔ không kiểm được — nên màn hình **tự kiểm** và nói ra. */
    const cong = (data.may || 0) + (data.nguoi || 0) + (data.khong || 0);
    o.appendChild(TP.el('div', cong === data.tong ? 'hint' : 'note warn',
      cong === data.tong
        ? '✓ ' + TP.so(data.may) + ' + ' + TP.so(data.nguoi) + ' + '
          + TP.so(data.khong) + ' = ' + TP.so(data.tong) + ' dòng — ba rổ khép.'
        : '⛔ ' + TP.so(cong) + ' ≠ ' + TP.so(data.tong)
          + ' — ba rổ ⛔ KHÔNG khép, có dòng rơi khỏi phép chia.'));
    /* `WO-042 (b)` ⓑ *(`BA-06` v4.18)*: câu cũ nói *"<c> dòng còn lại khớp
       số chứng từ nhưng lệch tiền"* — đúng **78 / 120** — và mang `⭐` `⛔`
       *(luật ký hiệu)*. Dựng bằng **chữ trơn** *(`TP.el` gán `innerHTML` —
       ⛔ để một câu có `<`/`&` trong tương lai thành thẻ)*; bài DOM so
       `textContent`. */
    if (data.tu_chung) {
      const c = (data.may || 0) - data.tu_chung;
      const n = TP.el('div', 'note ok');
      n.textContent = 'Trong rổ “máy trả lời được” có ' + TP.so(data.tu_chung)
        + ' dòng tự chứng — khớp cả số chứng từ, số tiền và tiền tệ; cửa ghi '
        + 'nhận chúng theo lô. Còn ' + TP.so(c) + ' dòng' + LY_DO_LO
        + MO_TUNG_DONG;
      o.appendChild(n);
    }
  }

  function ve_ro(o) {
    return TT.chay(o, () => FLS.doc('/queue/lenh-cho/ro'), _ve_ro, {
      so_dong: 3,
      la_rong: x => !x || !x.tong,
      rong: '⭐ ⛔ Không còn dòng lệnh nào chờ tiền.'
    });
  }

  /* ══ ②c CỘT CỦA LƯỚI — `BA-12`, owner 11/09 lần hai ═══════════════════
     ⛔⛔⛔ **Bản trước tôi để 28 cột trong NGĂN KÉO** *(phải bấm "Tìm tiền"
     từng dòng mới thấy)*, trong khi câu hỏi của owner là về **BẢNG**:
     *"bảng PM cần có đủ trường thông tin như trong GGSheet"*. Đọc sai yêu
     cầu — cùng dữ liệu, sai chỗ đặt.

     ★ Nhưng **⛔ không** đổ thẳng 28 cột ra lưới làm mặc định: một lưới 28
       cột thì ⛔ không đọc được, và **2 cột** dưới đây là hai thứ thật sự
       giúp nhận ra khoản tiền *(đo 11/09: cả hai điền **100%**)*. Còn lại
       nằm sau một nút bật — **người** chọn, ⛔ không phải tôi chọn hộ. */
  const COT_NHAN_DIEN = [
    ['Nội dung giao dịch nhập khi lập lệnh ở bank', 'Nội dung (ghi ở bank)'],
    ['Tên tài khoản', 'Người nhận']
  ];

  function _cot_them() {
    if (!ST.du_cot) return COT_NHAN_DIEN;
    /* ⭐ Tập cột lấy từ **chính dữ liệu** đang có, ⛔ không gõ tay một danh
       sách 28 tên: gõ tay thì một cột mới ở GGSheet sẽ ⛔ không bao giờ hiện
       ra, im lặng. */
    /* ⭐⭐ **THỨ TỰ TỜ GIẤY**, ⛔ không `sort()` (owner 11/09). `Set` của JS
       giữ **thứ tự chèn**, và `tho` từ cửa đã đúng thứ tự cột của GGSheet
       *(migration `0022`: cột kiểu `json` — `jsonb` **sắp lại khoá**)*.
       ⛔ Một `.sort()` ở đây sẽ vứt đi đúng thứ vừa phải đổi kiểu cột để giữ. */
    const co = new Set();
    ST.dong.forEach(r => Object.keys(r.tho || {}).forEach(k => co.add(k)));
    const uu = COT_NHAN_DIEN.map(x => x[0]);
    const con = [...co].filter(k => uu.indexOf(k) < 0);
    return COT_NHAN_DIEN.concat(con.map(k => [k, k]));
  }

  function _nut_du_cot(o) {
    const b = TP.el('div', 'bar');
    const n = TP.el('button', 'b tiny' + (ST.du_cot ? ' pri' : ''),
      ST.du_cot ? '← Chỉ 2 cột nhận diện' : 'Hiện ĐỦ các cột của GGSheet');
    n.onclick = function () { ST.du_cot = !ST.du_cot; ve(); };
    b.appendChild(n);
    const co = new Set();
    ST.dong.forEach(r => Object.keys(r.tho || {}).forEach(k => co.add(k)));
    b.appendChild(TP.el('span', 'lbl',
      co.size ? co.size + ' cột có dữ liệu trong trang này (GGSheet có 28)'
              : '⛔ trang này thuộc ảnh chụp CŨ — ⛔ không giữ hàng thô'));
    o.appendChild(b);
  }

  /* ══ ③ LƯỚI DÒNG LỆNH ════════════════════════════════════════════════ */

  /* ⭐ `G5` ① — **`CODE | Tên người đọc` ⇒ chỉ giữ CODE trên lưới.**

     ⛔⛔ Đo 11/09 trước khi cắt, vì **cắt mà mất chữ là một mặc định im
        lặng** (`INV-I16`): `hd` có **31** mã ↔ **31** giá trị đầy đủ, `cdt1`
        có **9** ↔ **9** ⇒ **song ánh**, mã xác định tên **duy nhất**. Nên bỏ
        phần tên khỏi lưới ⛔ **không mất một thông tin nào** — nó chỉ dời chỗ
        sang `title`. Nếu một ngày hai tên đeo chung một mã thì phép này sai,
        và cổng `tools/kiem_rut_gon_ma.py` là chỗ điều đó **nổ ra**.

     ⚠ **5** dòng `hd` và **9** dòng `cdt1` ⛔ không mang dấu `|`. Chúng giữ
       **nguyên văn** — ⛔ không cắt bừa theo vị trí ký tự. */
  function _ma_ngan(v) {
    const s = String(v == null ? '' : v).trim();
    if (!s) return '<span class="faint">—</span>';
    const i = s.indexOf('|');
    if (i < 0) return '<span class="mono" title="' + TP.chu(s) + '">'
                    + TP.chu(s) + '</span>';
    const ma = s.slice(0, i).trim(), ten = s.slice(i + 1).trim();
    return '<span class="ma-goi" title="' + TP.chu(ma + ' — ' + ten) + '">'
         + TP.chu(ma) + '</span>';
  }

  /* ⭐ `G5` ② — **động từ theo RỔ**, ⛔ không một chữ *"Tìm tiền"* lặp 1.553
     lần. Cùng một ngăn kéo mở ra; đổi là **chữ trên nút**, và chữ ấy nói
     đúng việc sắp làm. Một nút lặp y hệt trên mọi dòng thì ⛔ không mang
     thông tin nào — nó chỉ là tiếng ồn chiếm một cột. */
  function _viec_cua_dong(r) {
    if (r.ro === 'khong') return ['Xem vì sao', ''];
    if (r.ro === 'nguoi') return ['Tra tiền', 'pri'];
    return r.tu_chung ? ['Duyệt', 'pri'] : ['Mở để chia', 'pri'];
  }

  function _the_dong(r) {
    const tr = TP.el('tr');
    const o = (h, lop) => { const td = TP.el('td', lop, h); tr.appendChild(td); };
    /* ⭐ `G5` ④ — **`Luỹ kế %` ⛔ KHÔNG phải một cột tiền.** Nó nằm giữa
       `Tiền lệnh` và `Trạng thái`, cạnh những con số **của dòng này** — nên
       đọc như một thuộc tính của dòng. Nó ⛔ không phải: nó là *"đọc tới đây
       là phủ bao nhiêu % tiền"*, tức **vị trí trong danh sách**, cùng loại
       với `#`. ⇒ Gộp vào `#`, và mất hẳn một cột. */
    /* ⚠ MỘT dòng, ⛔ không hai: `th,td` khoá `height:var(--row)` = **30px**
       cho **mọi** lưới của hệ. Một ô hai dòng ở đây sẽ **tràn ra ngoài** ô —
       và ⛔ không báo gì, vì `overflow` mặc định là `visible`. */
    o('<b>' + String(r.hang) + '</b> <span class="faint" title="đọc tới dòng '
      + 'này là đã phủ ' + TP.chu(r.luy_ke_pct) + '% tổng tiền của ' + TP.chu(r.curr)
      + '">' + TP.chu(r.luy_ke_pct) + '%</span>', 'num r f1');
    o('<span class="mono">' + TP.chu(r.ref_tho || '—') + '</span>', 'f2');
    /* ⭐ `G5` ③ — **CẢ PHIẾU có mấy dòng.** Đo: `1.088/1.553` (**70,1%**)
       dòng chờ nằm trong phiếu nhiều dòng, phiếu to nhất **44** dòng. */
    o('<span class="mono">' + TP.chu(r.pm_slip_id || '—') + '</span>'
      + (Number(r.phieu_tong) > 1
         ? ' <span class="chip lock" title="Phiếu này có ' + r.phieu_tong
           + ' dòng lệnh, ' + r.phieu_cho + ' còn chờ tiền. Mở một dòng để '
           + 'xem CẢ phiếu — nhìn một dòng lẻ mà quyết là nhìn một mảnh của '
           + 'tờ giấy.">' + r.phieu_cho + '/' + r.phieu_tong + '</span>'
         : ''));
    o(TP.tien(r.amount, r.curr), 'num r');
    o(r.duyet ? TP.chip('ok', 'Approve')
              : TP.chip('warn', TP.chu(r.status || '⛔ RỖNG = không biết')));
    o(_ma_ngan(r.hd));
    o(_ma_ngan(r.cdt1));
    /* ⭐ Cột lấy thẳng từ `tho`. ⛔ `—` khi ảnh chụp cũ ⛔ không giữ hàng
       thô — ⛔ không để ô trắng cho người đọc tự đoán là "⛔ không có". */
    const tho = r.tho || {};
    _cot_them().forEach(function (c) {
      const v = String(tho[c[0]] != null ? tho[c[0]] : '—');
      /* ⛔ Cắt bề NGANG chỉ là chuyện hiển thị — `title` giữ **nguyên văn**,
         nên ⛔ không một ký tự nào biến mất khỏi tầm với của người đọc. */
      o('<span class="o-tho" title="' + TP.chu(v) + '">' + TP.chu(v)
        + '</span>');
    });
    /* ⭐ `G2` — RỔ + câu VÌ SAO ngay trên dòng. ⛔ Một rổ *"⛔ không bao giờ"*
       mà ⛔ không nói vì sao thì kế toán sẽ tìm **mãi mãi** — đúng điều màn
       hình trước `G2` đang bắt họ làm. */
    const ro = RO[r.ro] || ['lock', r.ro || '?', ''];
    o(TP.chip(ro[0], r.tu_chung ? 'tự chứng' : ro[1])
      + (r.vi_sao ? '<div class="hint">' + TP.chu(r.vi_sao) + '</div>' : ''));
    const da = ST.vua_ghep.get(r.pm_line_id);
    const td = TP.el('td', 'lam');
    if (da) {
      td.appendChild(TP.el('span', 'chip ok', '✓ vừa ghép vào dòng ' + da));
    } else {
      const v = _viec_cua_dong(r);
      /* ⭐ `WO-045` ⓒ: mở hộp = **đọc** ⇒ ⛔ khoá ở chỉ đọc. */
      td.appendChild(_nut_doc(v[0], v[1], () => _drawer_tim_tien(r)));
    }
    tr.appendChild(td);
    return tr;
  }

  function _ve_luoi(data, meta, o) {
    o.innerHTML = '';
    ST.dong = ST.dong.concat(data.rows || []);
    ST.con_tro = data.next_cursor || null;
    ST.het = !ST.con_tro;
    _nut_du_cot(o);
    /* ⛔⛔ `TP.bang` dựng **cây thẻ thật**, ⛔ không phải một chuỗi
       `innerHTML`. Bản đầu tôi viết `t.innerHTML = '…<tbody></tbody>'` rồi
       `t.querySelector('tbody')` — và nó **NỔ**: `Cannot read properties of
       null`. Lý do ⛔ không phải khung thử: `dom_gia.js` cố ý ⛔ không phân
       tích HTML, và **đó là một ràng buộc TỐT** — nó ép cấu trúc phải là cây
       thẻ thật, đúng thứ mọi lưới khác của hệ đang dùng. */
    /* ⭐ `G1` — MỘT TÊN cho một trường (`BA-12 §1`, 11/09).
       ⛔⛔ Ô này từng mang **một tên khác**, trong khi cùng tệp này — bảng ứng
       viên phía dưới — đã gọi đúng tên. Hai tên cho một trường, cách nhau 74
       dòng, trên cùng một màn hình. Nguồn gọi `Reference number` ở **cả**
       `PM_Unpivot` cột 25 **lẫn** sao kê ngân hàng ⇒ ⛔ không có cái tên thứ
       ba nào để bịa ra.
       ⚠ Cổng `tools/kiem_ten_truong.py` canh chỗ này — và ghi chú này CỐ Ý
       ⛔ không viết lại tên cũ ra, vì cổng quét **cả** ghi chú. Dạy cổng bỏ
       qua ghi chú là làm nó yếu đi ở đúng chỗ nó cần chặt. */
    /* ⭐⭐ `G5` — **hai cột đầu GHIM TẠI CHỖ** (`f1`/`f2`, đã có sẵn trong
       `table.g` của hệ). Với 28 cột thì cuộn ngang làm **mất danh tính của
       dòng**: người đọc trôi tới cột 20 và ⛔ không còn biết mình đang đứng ở
       lệnh nào. Ghim `#` và `Số chứng từ` là giữ đúng hai thứ trả lời câu
       *"dòng nào"* — ⛔ không ghim thêm, vì mỗi cột ghim ăn mất bề ngang. */
    const b = TP.bang([{chu: '# · phủ', lop: 'f1'},
                       {chu: 'Số chứng từ', lop: 'f2'},
                       {chu: 'Phiếu'}, {chu: 'Tiền lệnh'},
                       {chu: 'Trạng thái'}, {chu: 'HĐ'}, {chu: 'CĐT'}]
                      .concat(_cot_them().map(c => ({chu: c[1]})))
                      .concat([{chu: 'Ai trả lời được'}, {chu: 'Việc'}]));
    ST.dong.forEach(r => b.than.appendChild(_the_dong(r)));
    /* ⛔⛔ Bọc **cuộn NGANG**. `TP.bang` trả một `<table>` trần, và với 28 cột
       thì nó **đẩy cả trang** trôi ngang — thanh cuộn của trình duyệt chứ
       ⛔ không phải của bảng, tức mọi thứ khác trên màn cũng trôi theo.
       ⛔ Sửa ở ĐÂY chứ ⛔ không sửa `TP.bang`: mọi lưới khác của hệ đang
       dùng nó và ⛔ không màn nào trong số đó có 28 cột. */
    const cuon = TP.el('div', 'ngang');
    /* ⭐ `G5` — lớp `lenh` **chỉ** để thu hẹp hai cột ghim cho màn này.
       ⛔ Sửa `--khoa-1`/`--khoa-2` ở `tokens.css` sẽ đổi luôn lưới `F02`,
       nơi `346px` là con số **đã đo ở mũi thử** — biến CSS kế thừa theo cây
       thẻ, nên đặt lại trên **chính bảng này** là đủ và ⛔ không chạm ai. */
    b.bang.classList.add('lenh');
    cuon.appendChild(b.bang);
    o.appendChild(cuon);
    if (!ST.het) {
      const luot = _luot_luoi;
      const b = _nut_doc('Xem thêm', '', async function () {
        /* ⭐ `ⓦ` ② *(như `F02` `:369`)*: nút khoá trong lúc chờ ⇒ ⛔ lượt
           thứ hai cùng con trỏ. */
        if (b.disabled) return;
        b.disabled = true;
        try {
          const kq = await FLS.doc('/queue/lenh-cho?' + _qs());
          if (luot !== _luot_luoi) return;   /* ⭐ lưới đã đổi rổ / lọc */
          _ve_luoi(kq.data, kq.meta, o);
        } catch (err) {
          if (luot !== _luot_luoi) return;
          TT.loi(o, err, () => ve_luoi(o));
        }
      });
      o.appendChild(b);
    }
  }

  function _qs() {
    const p = ['limit=50'];
    /* ⚠ Cửa ⛔ KHÔNG nhận `ro` cùng `curr`/`duyet`: lọc theo rổ là một câu
       hỏi khác *(ai trả lời được)*, và trộn hai trục vào một truy vấn sẽ ra
       một tập ⛔ không ai đọc được ý nghĩa. Màn hình vì thế cũng gửi MỘT
       trong hai, ⛔ không gửi cả hai. */
    if (ST.ro) {
      p.push('ro=' + encodeURIComponent(ST.ro));
      if (ST.tu_chung !== null) p.push('tu_chung=' + (ST.tu_chung ? '1' : '0'));
    } else {
      if (ST.curr) p.push('curr=' + encodeURIComponent(ST.curr));
      if (ST.duyet) p.push('duyet=' + ST.duyet);
    }
    if (ST.con_tro) p.push('cursor=' + encodeURIComponent(ST.con_tro));
    return p.join('&');
  }

  function ve_luoi(o) {
    const luot = ++_luot_luoi;
    ST.dong = []; ST.con_tro = null;
    return TT.chay(o, () => FLS.doc('/queue/lenh-cho?' + _qs()), _ve_luoi, {
      so_dong: 8,
      con_hieu_luc: () => luot === _luot_luoi,
      la_rong: x => !((x && x.rows) || []).length,
      rong: '⭐ ⛔ Không còn dòng lệnh nào chờ tiền ở tiền tệ này.'
    });
  }

  /* ══ ④ DRAWER — chọn DÒNG TIỀN cho một dòng lệnh ══════════════════════
     ⛔⛔ Cú ghi gọi **đúng cửa cũ** `POST /queue/{itl_id}/match`, thân
     `{pm_line_ids:[…], reason}`. ⛔ Lằn này ⛔ không có cửa ghi riêng. */
  /* ══ ⑤ PANEL "NHÌN ĐỦ BẢNG PM" ══════════════════════════════════════
     ⛔⛔⛔ Owner 11/09: *"bảng PM vẫn chưa đủ các trường như trong GGSheet"*.
     Đo thật: `PM_Unpivot` có **28 cột**, FLS đọc **8**, và 20 cột bỏ qua kia
     điền **100%** — trong đó có đúng hai thứ một người dùng để nhận ra khoản
     tiền: *"Nội dung giao dịch nhập khi lập lệnh ở bank"* và *"Tên tài
     khoản"* (trả cho AI). ⇒ `535` dòng ⛔ không có số chứng từ **chỉ tra
     được bằng hai cột ấy**, mà màn hình ⛔ không hề hiện chúng. */
  const COT_QUAN_TRONG = [
    'Nội dung giao dịch nhập khi lập lệnh ở bank', 'Tên tài khoản',
    'Số tài khoản', 'Ngân hàng', 'Pháp nhân thanh toán',
    'Loại giao dịch (Payment Type)'];

  function _panel_pm(d) {
    const tho = d.tho;
    /* ⚠ `tho = null` có nghĩa **THẬT**: dòng này thuộc ảnh chụp TRƯỚC 11/09
       — ⛔ không phải *"đọc được 0 cột"*. Nói đúng câu ấy. */
    if (!tho) {
      return '<div class="note warn">⚠ Dòng này thuộc một <b>ảnh chụp cũ</b> '
           + '(trước 11/09) nên ⛔ <b>không giữ hàng thô</b>. Ảnh chụp kế tiếp '
           + 'sẽ có đủ 28 cột. ⛔ Đây ⛔ không phải "đọc được 0 cột".</div>';
    }
    const khoa = Object.keys(tho);
    const uu = COT_QUAN_TRONG.filter(k => tho[k] != null);
    /* ⛔ ⛔ Không `sort()` — giữ THỨ TỰ CỘT của tờ giấy. */
    const con = khoa.filter(k => COT_QUAN_TRONG.indexOf(k) < 0);
    const o = k => '<tr><th>' + TP.chu(k) + '</th><td>'
                 + TP.chu(String(tho[k])) + '</td></tr>';
    return '<div class="hint" style="margin:8px 0 4px">Bảng PM — <b>'
         + khoa.length + '/28 cột</b> có dữ liệu '
         + '<span class="hint">(⛔ cột <code>Email Address</code> ⛔ không bao '
         + 'giờ vào kho)</span></div>'
         + '<table class="pm-du"><tbody>'
         + uu.map(o).join('')
         + (uu.length && con.length
            ? '<tr class="pm-ngan"><th colspan="2">— các cột còn lại —</th></tr>'
            : '')
         + con.map(o).join('') + '</tbody></table>'
         + (d.ca_phieu && d.ca_phieu.length > 1
            ? '<div class="hint" style="margin-top:8px">Phiếu <b>'
              + TP.chu(d.pm_slip_id) + '</b> có <b>' + d.ca_phieu.length
              + ' dòng</b>: '
              + d.ca_phieu.map(x =>
                  '<span class="chip ' + (x.dang_xem ? 'info'
                    : x.da_noi ? 'ok' : 'lock') + '">'
                  + TP.chu(x.pm_line_id) + ' · ' + TP.tien(x.amount, x.curr)
                  + (x.da_noi ? ' ✓' : '') + '</span>').join(' ')
              + '<br>⚠ 526 phiếu mang 2–36 số chứng từ khác nhau — nhìn một '
              + 'dòng lẻ mà quyết là nhìn một mảnh của tờ giấy.</div>'
            : '');
  }

  /* ⭐ `WO-032`: hai mã **cùng có** mà **khác nhau** sau `trim` + chữ hoa
     *(`TP.ma_te`)*. Một bên thiếu ⇒ `false` — đó là **thiếu số** *(`—`)*,
     ⛔ phải *"khác tiền tệ"*. */
  function _khac_te(a, b) {
    const x = TP.ma_te(a), y = TP.ma_te(b);
    return !!x && !!y && x !== y;
  }

  async function _drawer_tim_tien(r) {
    let d, du = null;
    try {
      d = (await FLS.doc('/queue/lenh/'
             + encodeURIComponent(r.pm_line_id) + '/itl-candidates')).data;
      /* ⛔ Cửa "nhìn đủ" gọi RIÊNG và lỗi của nó ⛔ KHÔNG được làm hỏng cả
         ngăn kéo: thiếu vài cột hiển thị thì vẫn ghép được, còn ⛔ không mở
         được ngăn kéo thì ⛔ không làm gì được. */
      try {
        du = (await FLS.doc('/queue/lenh/'
               + encodeURIComponent(r.pm_line_id))).data;
      } catch (e2) { du = null; }
    } catch (e) {
      return HT.mo('Tìm tiền · lệnh ' + r.pm_line_id,
        '<div class="note crit"><b>' + TP.chu(e.cau) + '</b><br>'
        + TP.chu(e.lam_gi) + '</div>', [['Đóng', null]]);
    }
    /* ⭐⭐ `WO-032` (e) *(`BA-06` v4.14 §5b *Năm trạng thái*, `KQ-031 F-4`)*:
       cửa trả `data: null` *(chế độ `?gia_lap=rong`)* ⇒ hộp vẫn **mở** với câu
       rỗng của nhánh `uv.length = 0`. ⛔ Trước: `d.ung_vien` khi `d = null` ⇒
       `TypeError` ⇒ ⛔ hộp — trạng thái rỗng của màn ⛔ vẽ được. */
    if (!d) d = {};
    const uv = d.ung_vien || [];
    /* ⭐⭐⭐ `WO-022` vong 3 *(`KQ-029` `F-1`)*: thân ứng viên là **khuôn `⓵`**
       `BA-07 §4h` *(nắn ở `fls/repo/man_ghep.py::khuon_ung_vien` từ `23/09`,
       `GAP-API-10`)* — `amount` · `lech` · `dien_giai`. ⛔ Trước: hàm này đọc
       **khoá hàng thô** `u.tien` · `u.lech_tuyet_doi` · `u.memo` mà cửa
       ⛔ còn trả ⇒ Chrome thật *(8088 sổ thật + 8099 kho TEST)*: cột `Tiền`
       `—`, `Lệch` `—`, `Diễn giải` trống, và *"⛔ VƯỢT dung sai — cửa ghi sẽ
       TỪ CHỐI"* cho **MỌI** ứng viên, kể cả ứng viên khớp đúng từng xu.
       ⛔⛔ Bộ bài xanh suốt vì bài **tự nhét** khuôn người viết *tưởng*. Giờ
       cổng `tests/web/test_wo022_v3_tim_tien_cua_that.py` quét **mọi** khoá
       `u.`/`d.`/`r.` của hàm này ⊆ khoá **cửa thật** trả *(HTTP, kho TEST)*
       — đọc một khoá mới mà cửa ⛔ trả ⇒ ĐỎ. */
    const hang = uv.map((u, i) =>
      '<tr><td><input type="radio" name="uv" data-i="' + i + '"></td>'
      + '<td class="mono">' + TP.chu(u.itl_id) + '</td>'
      + '<td>' + TP.chip(BAC[u.bac] ? BAC[u.bac][0] : 'lock',
                         BAC[u.bac] ? BAC[u.bac][1] : u.bac) + '</td>'
      + '<td>' + TP.chu(String(u.doc_date || '').slice(0, 10)) + '</td>'
      + '<td class="mono">' + TP.chu(u.doc_no || '—') + '</td>'
      /* ⭐ `WO-032` *(§5b ⓙ)*: bảng này **trộn** tiền tệ *(bậc `ma` khớp
         **mã**, ⛔ lọc tiền tệ — sổ thật **165 / 5.360** ứng viên khác tiền tệ
         lệnh)* ⇒ ô tiền in **kèm mã**. ⛔ Trước: `100.000,00` trần cạnh dòng
         ghim `100.000 VND` — mắt đọc hai số **bằng nhau**. */
      + '<td class="r num">' + TP.tien(u.amount, u.curr) + ' '
      + TP.chu(u.curr || '') + '</td>'
      /* ⭐⭐ `WO-032` *(`BA-07` v3.7 §4h ⓵ · §5b ⓕ)*: cửa trả `lech` có số ở
         **mọi** bậc khi cùng tiền tệ; `null` ⇔ ⛔ so được — và màn phải nói
         **vì sao**: khác tiền tệ ⇒ chữ **`khác tiền tệ`**; `—` để dành cho
         **thiếu số** *(hai nghĩa ⛔ chung một ký hiệu — `INV-I16`)*. ⛔ Trước:
         bậc `ma` luôn `null` ⇒ `—` cho lệch thật `21.586,78` *(8088
         `PM02117-1`)*. */
      + '<td class="r num">' + (u.lech != null ? TP.tien(u.lech, u.curr)
          : _khac_te(u.curr, r.curr) ? 'khác tiền tệ' : '—') + '</td>'
      + '<td>' + TP.chu((u.dien_giai || '').slice(0, 48)) + '</td></tr>'
    ).join('');

    HT.mo('Tìm tiền cho lệnh ' + r.pm_line_id,
      '<div class="note" style="margin-top:0"><b>Dòng lệnh (ghim):</b> '
      + '<span class="num">' + TP.tien(r.amount, r.curr) + '</span> '
      + TP.chu(r.curr) + ' — mã <span class="mono">'
      + TP.chu(r.ref_tho || '—') + '</span> · phiếu <span class="mono">'
      + TP.chu(r.pm_slip_id || '—') + '</span></div>'
      + (du ? _panel_pm(du) : '')
      /* ⛔ `status` RỖNG là KHÔNG BIẾT, ⛔ không phải "đã duyệt" */
      + (d.canh_bao
         ? '<div class="note warn">⚠ <b>' + TP.chu(d.canh_bao) + '</b><br>'
           + 'Cửa ghép sẽ đòi <code>force</code> kèm lý do, và một cú bấm lô '
           + '⛔ không bao giờ được mang <code>force</code>.</div>' : '')
      + '<div class="hint">dung sai Σ cho tiền tệ này: <b>'
      /* ⭐⭐ `WO-022` vong 2 *(§5b ⓕ v4.13)*: in **dung** dung sai dem so
         — san xu, nhu `_tinh` ben duoi *(`"617.285"` → `617,28`, ⛔
         `617,29`)*. ⛔ Doi duoc sang xu ⇒ chuoi cua tra nguyen van. */
      + (TP.xu(d.dung_sai, 'san') === null ? TP.tien(d.dung_sai, r.curr)
         : TP.tien(TP.chuoi_xu(TP.xu(d.dung_sai, 'san')), r.curr))
      + '</b> — cùng phép dung sai mà cửa GHI dùng</div>'
      + (uv.length
         ? '<table><thead><tr><th></th><th>Dòng tiền</th><th>Độ khớp</th>'
           + '<th>Ngày</th><th>Số chứng từ</th><th class="r">Tiền</th>'
           + '<th class="r">Lệch</th><th>Diễn giải</th></tr></thead><tbody>'
           + hang + '</tbody></table>'
         : '<div class="note crit">⛔ <b>⛔ Không có dòng tiền nào ứng.</b> '
           + '⛔ Không dòng tiền nào chưa nối mang mã này, và ⛔ không dòng nào '
           + 'cùng tiền tệ còn trống.</div>')
      /* ⭐⭐ KHAI RA đã cắt — cắt mà im là một mặc định im lặng (`INV-I16`):
         người gõ sẽ tưởng danh sách là đầy đủ và kết luận *"không có dòng
         tiền nào khớp"*. */
      + (d.bi_cat
         ? '<div class="note warn">⚠ <b>Danh sách bị CẮT.</b> Còn '
           + TP.so(d.tong_cung_tien_te) + ' dòng tiền cùng tiền tệ chưa nối — '
           + 'màn chỉ hiện những dòng gần tiền nhất. ⛔ Đừng đọc danh sách này '
           + 'thành <i>“chỉ có mấy dòng ấy”</i>.</div>' : '')
      /* ⭐⭐ `WO-032` (g) *(`QĐ-ITL-149 ⓑ` — owner 01/10: *"bỏ yêu cầu lý do
         cho cú Ghép"*; `BA-07 §4h ⓼`)*: ô **tuỳ ý**. Trống ⇒ thân ⛔ mang
         `reason`, cửa *(tầng repo `ghep_lenh`)* ghi `LY_DO_MAC_DINH_GHEP` có
         nhãn `(may dien)` ⇒ vết ⛔ bao giờ rỗng. ⛔ Trước: placeholder
         *"BẮT BUỘC"* + nút chặn khi ô trống — trái lời owner. */
      + '<input class="inp" id="o-vi-sao-l" style="max-width:none;'
      + 'margin-top:9px" placeholder="vì sao ghép cặp này — tuỳ ý — bỏ '
      + 'trống thì máy ghi lý do mặc định…">'
      + '<div class="note" id="sig-l" style="margin-bottom:0"></div>',
      [['Thôi', null],
       ['Ghép', async function () {
         /* ⚠ `WO-032` `AC-8`: lọc `name`/`checked` *(⛔ bộ chọn `:checked`)* —
            cùng ô trên trình duyệt, DOM giả đọc được *(như `_tinh`)*. */
         const ck = [...document.querySelectorAll('#dlg-b input')]
           .filter(c => c.name === 'uv' && c.checked)[0];
         if (!ck) return false;
         const u = uv[Number(ck.dataset.i)];
         const v = (TP.$('#o-vi-sao-l').value || '').trim();
         const than = { pm_line_ids: [r.pm_line_id] };
         if (v) than.reason = v;
         try {
           /* ⛔⛔ ĐÚNG cửa ghi cũ — ⛔ không có đường ghi thứ hai. */
           await FLS.ghi('/queue/' + u.itl_id + '/match', than);
           ST.vua_ghep.set(r.pm_line_id, u.itl_id);
         } catch (e) { HT.loi_trong_hop(e); return false; }
         ve();
       }, { pri: true }]]);
    /* ⭐ `WO-045` ⓒ *(`ⓦ` ② bảng)*: hộp mở được ở chỉ đọc *(xem ứng viên)*,
       nhưng **`Ghép`** là đường **ghi** ⇒ khoá + câu `405` như nay. `HT.mo`
       ⛔ có tuỳ chọn khoá ⇒ khoá **sau** khi hộp dựng, và gỡ `onclick` để
       vòng `finally` của `HT.mo` *(mở lại cả hàng nút)* ⛔ có gì để chạy. */
    const g = [...document.querySelectorAll('#dlg-f button')]
      .filter(x => x.textContent === 'Ghép')[0];
    if (g && _chan_ghi(g)) g.onclick = null;

    /* ── Σ hai con số, tính lại mỗi lần chọn ─────────────────────────── */
    function _tinh() {
      /* ⚠ `#dlg-b input` + loc `name`/`checked` *(⛔ bo chon `:checked`)* —
         cung mot o tren trinh duyet, va DOM gia cua bo thu doc duoc. */
      const ck = [...document.querySelectorAll('#dlg-b input')]
        .filter(c => c.name === 'uv' && c.checked)[0];
      const s = TP.$('#sig-l');
      if (!s) return;
      if (!ck) { s.className = 'note'; s.innerHTML = 'chưa chọn dòng tiền nào';
                 return; }
      const u = uv[Number(ck.dataset.i)];
      /* ⭐⭐⭐ `WO-032` (a) *(`BA-06` v4.14 §5b ⓕ, `KQ-031 F-1`)*: **lệch CHỈ có
         khi CÙNG tiền tệ** — so mã **TRƯỚC** khi đổi xu. ⛔ Trước: hàm này
         trừ hai đơn vị ⇒ 8088 `PM00329-1` *(`100.000 VND`)* ↔ ứng viên
         `32700` *(`100.000,00 USD`, bậc `ma`)* ⇒ `note ok` *"lệch 0 ⇒ trong
         dung sai"* cho một cặp cửa ghi ném `KhacTienTe` — câu máy nói
         **ngược** cửa ghi; **4** lệnh sổ thật. ⛔ Màn ⛔ thêm nút chặn: cửa ghi
         đã chặn, màn chỉ phải **nói đúng**. */
      if (_khac_te(u.curr, r.curr)) {
        s.className = 'note crit';
        s.innerHTML = 'tiền lệnh <b>' + TP.tien(r.amount, r.curr) + ' '
          + TP.chu(r.curr) + '</b> ↔ tiền bank <b>' + TP.tien(u.amount, u.curr)
          + ' ' + TP.chu(u.curr) + '</b> · <b>khác tiền tệ</b> ⇒ ⛔ cửa ghi '
          + 'sẽ TỪ CHỐI';
        return;
      }
      /* ⭐⭐ `WO-022` §5b ⓕ: lech tren SO NGUYEN XU; dung sai doi xu bang
         SAN *(`|lech| <= ds` ⇔ `|lech_xu| <= san(ds × 100)`)*. ⛔ Truoc:
         `Math.abs(Number - Number)` roi in bang ham cu ⇒ lech `0,40 USD`
         in **`0`** canh chu *"VƯỢT dung sai"*. */
      const a = TP.xu(u.amount), b = TP.xu(r.amount);
      const ds = TP.xu(d.dung_sai, 'san');
      const hong = a === null || b === null || ds === null;
      const lech = hong ? null : Math.abs(a - b);
      const ok = !hong && lech <= ds;
      s.className = 'note ' + (ok ? 'ok' : 'crit');
      s.innerHTML = 'tiền lệnh <b>' + TP.tien(r.amount, r.curr)
        + '</b> ↔ tiền bank <b>' + TP.tien(u.amount, u.curr) + '</b> · lệch <b>'
        + (hong ? '⛔ không tính được' : TP.tien(TP.chuoi_xu(lech), r.curr))
        + '</b> '
        + (ok ? '⇒ trong dung sai'
              : '⇒ ⛔ <b>VƯỢT dung sai</b> — cửa ghi sẽ TỪ CHỐI');
    }
    const b = document.querySelector('#dlg-b');
    if (b) b.addEventListener('change', _tinh);
    _tinh();
  }

  /* ══ ⑤ VẼ ════════════════════════════════════════════════════════════ */
  function ve(o) {
    const than = o || _than;
    if (!than) return;
    _than = than;
    _luot_luoi++;   /* ⭐ `WO-045`: lưới cũ rời cây ⇒ lượt của nó bị thay */
    than.innerHTML = '';

    /* ⓪ VIỆC HÔM NAY — **luôn đứng đầu**, kể cả khi đang lọc theo rổ. */
    const cv = TP.el('div', 'card');
    than.appendChild(cv);
    ve_viec(cv);

    /* ⭐ Đang xem MỘT RỔ ⇒ vào thẳng lưới. ⛔ Không đòi chọn tiền tệ: câu hỏi
       ở đây là *"việc của tôi"*, ⛔ không phải *"đồng tiền nào nặng nhất"*.
       ⚠ Thứ tự BÊN TRONG vẫn theo từng tiền tệ (`QĐ-ITL-58`) — cột `Tiền tệ`
         vẫn hiện để người đọc ⛔ không tưởng đây là một bảng đã gộp. */
    if (ST.ro) {
      const b = TP.el('div', 'bar');
      const q = TP.el('button', 'b tiny', '← Quay lại toàn bộ');
      q.onclick = function () { _loc(null, null); };
      b.appendChild(q);
      b.appendChild(TP.el('span', 'lbl',
        'đang xem rổ: ' + ((RO[ST.ro] || [])[1] || ST.ro)
        + (ST.tu_chung === true ? ' · chỉ TỰ CHỨNG'
           /* `WO-042 (b)` ⓒ: tên **tập**, ⛔ tên **một** lý do *(nhãn
              cũ đặt trên 42 / 120 dòng ⛔ lệch tiền)* */
           : ST.tu_chung === false ? ' · chỉ CHƯA NHẬN THEO LÔ' : '')));
      than.appendChild(b);
      const l1 = TP.el('div', 'card');
      than.appendChild(l1);
      ve_luoi(l1);
      return;
    }

    /* ⭐⭐ Ba khối SỐ LIỆU lui vào đây. ⛔ Chúng ⛔ KHÔNG bị xoá — cổng của dự
       án là ⛔ không giấu con số — nhưng chúng ⛔ không được đứng trước việc.
       `<details>` đóng sẵn: người cần kiểm thì mở, người đi làm thì ⛔ không
       phải cuộn qua. */
    const d = TP.el('details', 'gop');
    const s = TP.el('summary', '', 'Số liệu kiểm chứng '
      + '<span class="hint">(ba rổ có khép không · từng tiền tệ · phủ 90%)</span>');
    d.appendChild(s);
    const cro = TP.el('div', 'card');
    d.appendChild(cro);
    ve_ro(cro);
    const tom = TP.el('div', 'card');
    d.appendChild(tom);
    ve_tom(tom);
    than.appendChild(d);

    const bar = TP.el('div', 'bar');
    bar.appendChild(TP.el('span', 'lbl', 'Hay xem theo tiền tệ'));
    const sel = TP.el('select', 'inp');
    sel.innerHTML = '<option value="">— chọn —</option>'
      + ['VND', 'USD', 'SGD', 'HKD', 'EUR'].map(
          c => '<option value="' + c + '">' + c + '</option>').join('');
    sel.value = ST.curr || '';
    sel.onchange = function () {
      ST.curr = sel.value || null; ST.con_tro = null; ST.dong = []; ve(than);
    };
    bar.appendChild(sel);
    than.appendChild(bar);

    if (!ST.curr) return;
    _thanh_loc(than);
    const luoi = TP.el('div', 'card');
    than.appendChild(luoi);
    ve_luoi(luoi);
  }

  return { ve, ST, ve_tom, ve_luoi, ve_ro, ve_viec, BAC, RO, LY_DO_LO,
           /* ⭐ `G5` — mở ra cho bài thử soi thẳng phép chọn động từ, ⛔ không
              phải đi vòng qua cả một lần vẽ lưới. */
           viec_cua_dong: _viec_cua_dong, ma_ngan: _ma_ngan,
           /* ⭐ `WO-022` `AC-6` — hộp *"Tìm tiền"* *(tiền lệnh ↔ tiền bank ·
              lệch)*: DOM giả ⛔ dựng được lưới để bấm tới nó. */
           _drawer_tim_tien };
})();
