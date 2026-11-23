# -*- coding: utf-8 -*-
"""§4 UIWireFrame — FLS."""
from apgen import *

def sections():
    out = []
    out.append(S("s4", "§4 UIWireFrame — bốn màn F01–F04, mười tám hộp thoại", st="draft", part="PART B · THIẾT KẾ CHI TIẾT — UI · LOGIC · IMPLEMENTATION", body=
        P("Màn hình là <b>tệp tĩnh</b> (HTML + CSS + JS thuần, không framework, không thư viện lưới — <code>QĐ-ITL-66</code>) do chính máy cửa phục vụ trên loopback; mọi con số đi qua cửa HTTP như bất cứ người gọi nào khác. Mục này không vẽ lại mockup: nhãn nút và bố cục chép từ mã đang chạy; hình dạng thật xem <code>docs/ITL/02_BA/Artifacts/Ban-ve-TOBE-Man-Ghep-PM.html</code>.")
    ))

    out.append(S("s4-1", f"§4.1 App shell + bản đồ tệp → tab → cửa {BUILT}", body=
        T([("Tệp (đường)", 20), ("Cỡ", 8), ("Vai", 40), ("Cửa gọi", 32)], [
            ["<code>/</code> → <code>index.html</code>", "11,7 KB", "vỏ: thanh trên <code>FLS · Sổ ITL</code> · <code>#p-nap</code> phạm vi · <code>#p-cua</code> (<code>cửa: ĐỌC + GHI</code> / <code>CHỈ ĐỌC</code>) · <code>#p-nguoi</code>; 5 tab", "—"],
            ["<code>tokens.css</code> · <code>hinh.css</code>", "6,8 + 32,3 KB", "token màu từ A-CCR — <b>chỗ duy nhất có mã màu</b> (<code>QĐ-ITL-77</code>, cổng <code>test_khong_ma_mau_go_tay</code>); hình dạng shell · thẻ · chip · nút · lưới · 4 trạng thái", "—"],
            ["<code>goi_cua.js</code>", "12,0 KB", "<b>chỗ duy nhất gọi cửa</b>; dịch đủ 20 mã lỗi + 2 mã màn (<code>FLS-MAT-KET-NOI</code>, <code>FLS-TRA-LOI-LA</code>) thành <code>cau + lam_gi</code>", "mọi tuyến"],
            ["<code>thanh_phan.js</code> · <code>trang_thai.js</code> · <code>hop_thoai.js</code>", "6,3 + 4,3 + 4,4 KB", "chip niềm tin/trạng thái, số kế toán, <code>TP.bang</code>; khuôn 4 trạng thái (đang tải · rỗng · lỗi · mặc định); <code>HT.mo(tieu_de, than, nut)</code> — hàm trả <code>false</code> ⇒ hộp ở nguyên, Esc/bấm ngoài = đóng không làm gì", "—"],
            ["<code>man_f03.js</code>", "12,2 KB", "① Cổng hôm nay", "<code>GET /gates</code> · <code>/queue/coverage</code> · <code>/queue/mau-so</code>"],
            ["<code>man_f01.js</code> · <code>man_f01_lenh.js</code>", "38,7 + 41,6 KB", "② Hàng chờ — lằn TIỀN 5 hành động/dòng; lằn LỆNH CHI G1–G5", "<code>/queue*</code> 15 tuyến"],
            ["<code>man_f02.js</code>", "106,8 KB", "③ Sổ ITL — lưới 8 hành vi + panel", "<code>/ledger*</code> · <code>/adjustments/*/reverse</code> · <code>/journal</code>"],
            ["<code>man_f04.js</code>", "44,7 KB", "④ Nạp sao kê — 5 trạng thái, biên bản 9 luật", "<code>/sources*</code> · <code>/chup*</code> · <code>/nap/lo*</code>"],
            ["<code>ung_dung.js</code>", "5,3 KB", "khởi động vỏ, chọn màn; chế độ giả lập <code>?gia_lap=rong|loi|mat_ket_noi|tai</code> hiện thanh đỏ, <b>không bao giờ sinh số</b>", "—"],
            ["<code>danh_muc.js</code> · <code>phien.js</code> · <code>cot.js</code>", "sinh", "73 mã <code>hd</code> từ <code>fls_mapping_master</code>; <code>window.FLS_PHIEN = {the, actor, cho_ghi, pham_vi}</code> — <b>chở thẻ</b> (lỗ đăng nhập, §4.5); 52 cột lưới + 38 vị trí canon từ <code>ledge_spec</code>/<code>canon.spec</code>", "—"],
        ])
        + P("Bảng tệp <code>BANG_TEP</code> 17 đường là <b>khoá tra</b>, không ghép đường; đuôi cho phép <code>.html .css .js</code>; tệp trên đĩa không khai ⇒ máy từ chối chạy; đường <code>/api/…</code> không bao giờ ra tệp. CSP <code>default-src 'none'; script-src 'self'</code>. Tab <kbd>⑤ Danh mục · F06 (B6)</kbd> <code>disabled</code> vì <code>GET /catalog</code> chưa đặc tả (<code>GAP-SPEC-01</code>).")
    ))

    out.append(S("s4-2", f"§4.2 SCR-F01 Hàng chờ — hai lằn trên một kho mối nối {BUILT}", body=
        P("Thanh <code>tabs sub</code>: <kbd>Theo LỆNH CHI</kbd> (mặc định, <code>QĐ-ITL-124</code>) · <kbd>Theo dòng tiền</kbd>. Hai lằn hỏi hai câu khác nhau trên cùng <code>fls_moi_noi</code>; cú ghép vẫn đi qua <b>một</b> cửa <code>POST /queue/{itl_id}/match</code>.")
        + '<pre class="ascii">'
        + """┌ FLS · Sổ ITL      phạm vi: lần nạp thật      cửa: ĐỌC + GHI      kế toán · &lt;actor&gt; ┐
│ ① Cổng hôm nay · F03 │ ② Hàng chờ · F01 │ ③ Sổ ITL · F02 │ ④ Nạp sao kê · F04 │ ⑤ Danh mục (tắt) │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [Theo LỆNH CHI] [Theo dòng tiền]                                                 │
│ ┌ VIỆC CỦA BẠN HÔM NAY ─────────────────────────────────────────────────────────┐ │
│ │ ● 250 dòng  máy ghép được — bạn chỉ DUYỆT                 [Duyệt cả 47 dòng] │ │
│ │ ● 535 dòng  CẦN BẠN tra bằng tiền + ngày                      [Bắt đầu tra] │ │
│ │ ● 768 dòng  ⛔ KHÔNG làm được — đừng động vào                   [Xem vì sao] │ │
│ │ ⚠ Còn 203 dòng khớp số chứng từ nhưng lệch tiền …           [Xem 203 dòng] │ │
│ └───────────────────────────────────────────────────────────────────────────────┘ │
│ ▸ Số liệu kiểm chứng (ba rổ có khép không · từng tiền tệ · phủ 90%)               │
│ Hay xem theo tiền tệ [— chọn —▾]   Trạng thái lệnh [tất cả▾]   [Hiện ĐỦ các cột của GGSheet] │
│ ┌#·phủ┬Số chứng từ┬Phiếu┬Tiền lệnh┬Trạng thái┬HĐ┬CĐT┬…┬Ai trả lời được┬Việc─────┐ │
│ │ 1   │ FT25…     │3/5  │ 12.000.000│Approve  │NB│SHQ2│ │ tự chứng     │[Duyệt]  │ │
│ │ 2   │ …         │1    │ …         │⛔ RỖNG  │  │    │ │ cần người    │[Tra tiền]│ │
│ └─────┴───────────┴─────┴───────────┴─────────┴──┴────┴─┴──────────────┴─────────┘ │
│                                                                    [Xem thêm]    │
└──────────────────────────────────────────────────────────────────────────────────┘"""
        + '</pre><p class="fig-cap"><strong>Hình 4.2</strong> — F01 lằn LỆNH CHI (bố cục G5, 11/09): dải việc đứng đầu, số liệu kiểm chứng gập, lưới ghim hai cột đầu và cột Việc. Con số minh hoạ [DOC 14/09].</p>'
        + T([("Khối", 18), ("Lằn LỆNH CHI (<code>man_f01_lenh.js</code>)", 42), ("Lằn TIỀN (<code>man_f01.js</code>)", 40)], [
            ["Câu hỏi", "«lệnh chi nào chưa tìm được tiền» — 1.345 dòng / 698 phiếu; 69 dòng phủ 90 % tiền", "«dòng tiền nào chưa có lệnh» — 7.682 dòng; 799 dòng phủ 90 % (11,6× nhiều hơn)"],
            ["Đầu màn", "dải <b>VIỆC CỦA BẠN HÔM NAY</b> 3 rổ (<code>GET /queue/lenh-cho/ro</code>); ghi chú lệch tiền; khi lọc rổ có <kbd>← Quay lại toàn bộ</kbd>", "mỗi tiền tệ một card <code>dòng chờ · Σ tiền</code> + <kbd>Xem</kbd>; ghi chú <code>⛔ Không có ô “tổng”</code>; khối <b>Ghép cả lô · chỉ dòng TỰ CHỨNG</b> với <kbd>Ghép N dòng tự chứng</kbd> và bảng «vì sao — và sửa ở đâu»"],
            ["Lọc", "<kbd>Hay xem theo tiền tệ</kbd> · <kbd>Trạng thái lệnh</kbd> (tất cả / chỉ đã duyệt / ⛔ chỉ chưa duyệt) · <kbd>Hiện ĐỦ các cột của GGSheet</kbd>", "segment <b>Chỉ xem tới mức phủ</b> tất cả / 50 % / 80 % / 90 %; chip <code>⛔ cửa đang CHỈ ĐỌC — mọi nút ghi đều mờ</code>"],
            ["Lưới", "<code># · phủ</code> (ghim) · <code>Số chứng từ</code> (ghim, tên duy nhất — G1) · <code>Phiếu</code> (chip <code>chờ/tổng</code> chỉ khi phiếu >1 dòng) · <code>Tiền lệnh</code> · <code>Trạng thái</code> (<code>Approve</code> / <code>⛔ RỖNG = không biết</code>) · <code>HĐ</code>, <code>CĐT</code> chỉ MÃ, tên ở <code>title</code> · 2 hay 28 cột thô · <code>Ai trả lời được</code> · <code>Việc</code> (ghim phải)", "<code>Hạng · Mã dòng · Số chứng từ · Diễn giải · Tiền · % luỹ kế · Pháp nhân · Việc</code>; chip trên Diễn giải: <code>đã ghép N dòng lệnh</code> · <code>đã xong</code> · <code>lý do: …</code> · <code>hoãn đến … · lần N</code> (đỏ từ lần 3)"],
            ["Nút mỗi dòng", "theo rổ: <kbd>Xem vì sao</kbd> · <kbd>Tra tiền</kbd> · <kbd>Duyệt</kbd> · <kbd>Mở để chia</kbd> — cùng một drawer, không đường ghi thứ hai. <b>Chưa có</b>: Lý do · Hoãn · Bỏ ghép · Xong (ranh giới kho: <code>fls_queue_event</code> chỉ treo vào <code>itl_id</code>)", "<kbd>Lý do</kbd> · <kbd>Hoãn</kbd> · <kbd>Ghép</kbd> · <kbd>Bỏ ghép</kbd> (chỉ khi đã ghép) · <kbd>Xong</kbd>; dòng xong ⇒ chỉ <kbd>Mở lại</kbd>"],
            ["Duyệt lô", "<kbd>Duyệt cả N dòng</kbd> → thanh <kbd>← Quay lại</kbd> + <code>Duyệt theo lô — cùng một cửa ghi với lằn dòng tiền</code>; <b>dùng lại</b> <code>F01.ve_lo</code>", "chủ khối lô; N = <code>ds_tu_chung</code> của cửa ghi, không phải màn đo"],
            ["Chân", "<kbd>Xem thêm</kbd> khi còn <code>next_cursor</code> (<code>&lt;curr&gt;:&lt;hang&gt;</code>)", "<code>Đang xem N dòng &lt;curr&gt; · tới mức phủ X%</code> + <kbd>Xem thêm</kbd> / <code>hết danh sách</code>; note <code>⚠ ⛔ Chưa có cột “tuổi việc”</code>"],
        ])
    ))

    out.append(S("s4-3", f"§4.3 SCR-F02 Sổ ITL — lưới 52 cột, hai chế độ, panel 7 ô {BUILT}", body=
        '<pre class="ascii">'
        + """┌ ③ Sổ ITL · F02 ────────────────────────────────────────────────────────────────┐
│ [lọc cách nhìn (gõ để ẩn dòng không khớp)…] [chỉ UNMAPPED] [▤ Quét · lưới chỉ-đọc]│
│ ┌itl_id┬memo┬doc_date┬curr┬ps_no┬ps_co┬hd┬pay_type┬cdt1┬work_status┐ ┃ PANEL DÒNG 4711  [Đóng] │
│ │ 4711 │ CK │ 05/03  │VND │     │ 12tr│OGA│Thanh… │SHQ2│ UNMAPPED   │ ┃ ▌dải phán quyết          │
│ │ 4712 │ …  │        │    │     │     │   │        │    │ ok         │ ┃ Budget Code  nguồn: OGA │
│ │      │    │        │    │     │     │   │        │    │            │ ┃              gõ: [____] │
│ │      │    │        │    │     │     │   │        │    │            │ ┃ Loại giao dịch  [chọn▾] │
│ │      │    │        │    │     │     │   │        │    │            │ ┃ Chủ dự toán  · Bắt đầu DV│
│ │      │    │        │    │     │     │   │        │    │            │ ┃ Kết thúc DV · Mã đối tác │
│ │      │    │        │    │     │     │   │        │    │            │ ┃ Hoá đơn                  │
│ │      │    │        │    │     │     │   │        │    │            │ ┃ PHÂN BỔ (máy suy) 🔒     │
│ │      │    │        │    │     │     │   │        │    │            │ ┃ Mối nối · Bút toán [Đảo] │
│ └──────┴────┴────────┴────┴─────┴─────┴───┴────────┴────┴────────────┘ ┃ 38 cột canon A…AL        │
│                                            [Xem thêm 200 dòng]                                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘"""
        + '</pre><p class="fig-cap"><strong>Hình 4.3</strong> — F02 chế độ Quét: lưới 9 cột chỉ-đọc bên trái, panel là cột bên phải không che lưới. Chế độ Gõ mở đủ 52 cột và cho gõ thẳng 5 ô hợp đồng.</p>'
        + T([("Thành phần", 20), ("Hành vi", 54), ("Cổng canh", 26)], [
            ["Hai chế độ", "<kbd>▤ Quét · lưới chỉ-đọc</kbd> (mặc định, 9 cột, sửa ở panel) ↔ <kbd>✎ Gõ · lưới sửa được</kbd> (52 cột = 25 nền + 27 <code>canon_*</code>, 5 ô gõ được trên lưới <code>hd pay_type cdt1 svc_start svc_end</code>, 2 ô 🔒 <code>alloc_cfa2 alloc_method</code>)", "<code>test_luoi_f02_hanh_vi</code> 23 bài; <code>cot_so.kiem_bang_cot</code> hai chiều với cửa thật"],
            ["8 hành vi Sheets", "phím · dán vùng · kéo xuống (Ctrl+D chép dòng đang thấy) · hoàn tác có lịch sử (Ctrl+Z trên ô đã lưu ⇒ hộp <i>Ô này đã vào sổ rồi</i>) · filter ẩn không xoá · đóng cứng tiêu đề + 2 cột khoá (<code>itl_id</code>, <code>memo</code>) · số kế toán/âm đỏ · lưu không nút", "<code>test_mui_thu_luoi</code> 11 bài; <code>hien_vat/mui_thu_luoi_F02.html</code>"],
            ["Lô lưu", "tự bay sau <code>CHO_MS = 2500</code>; hỏi lại cửa trước <b>mỗi</b> bút toán; không lý do ⇒ không bay; cửa chỉ đọc ⇒ không bay; ô chưa vào sổ viền vàng", "<code>test_lo_luu_f02</code> 12 bài"],
            ["Panel phải", "7 nhóm; dải phán quyết h1; băng báo tối đa một; digest 9 ô; «nguồn nói» vs «người gõ»; <code>hd</code> gợi ý từ danh mục là <b>ảnh chụp</b> (<code>danh_muc.js</code>); kỳ là ô chọn tháng; loại giao dịch là ô đóng; khối phân bổ 3 trạng thái (<code>Method = 0</code> nói bẫy VLOOKUP, <code>#N/A</code> nói không tra được); 2 ô <code>id_payee</code>, <code>invoice</code> chỉ gõ ở panel", "<code>test_drawer_f02</code> 58 bài"],
            ["Xung đột", "409 <code>FLS-CONFLICT-SOURCE</code> ⇒ hộp <i>Giá trị bạn gõ KHÁC cái đang có</i>; người khác gõ ⇒ hộp <i>Ô này đã có NGƯỜI KHÁC gõ</i> — máy chưa ghi gì; lô dừng ⇒ hộp <i>Lô lưu DỪNG giữa chừng</i>", "<code>test_vong_f02_pg</code> 14 bài"],
            ["Kỳ chốt", "mọi ô chỉ đọc và nói ra; cửa 409 kể cả <code>force</code>", "hôm nay không có dòng locked trên kho thật"],
        ])
    ))

    out.append(S("s4-4", f"§4.4 SCR-F03 Cổng hôm nay · SCR-F04 Nạp sao kê {BUILT}", body=
        T([("Màn", 12), ("Bố cục", 46), ("Cửa", 22), ("Điều cố ý không có", 20)], [
            ["<b>F03</b> Cổng hôm nay", "3 khối gọi độc lập: <b>cổng</b> (<code>KHO_SACH</code> · <code>SIGMA_MOI_NOI</code> · <code>RUN_DEM_KHOP</code> + 5 cổng khai <b>chưa đo được</b> <code>DIF_BANK · VI · DONG_BO · FINAL · BON_DUONG</code>, ba nhãn <code>✓ ĐẠT</code> / <code>✗ KHÔNG ĐẠT</code> / <code>— ⛔ KHÔNG ĐO ĐƯỢC</code>) · <b>độ phủ theo tiền tệ</b> · <b>mẫu số</b> <code>Vế của sổ · Dòng · Đã nối lệnh chi · ⛔ Chưa nối · Độ phủ</code>", "<code>GET /gates</code> · <code>/queue/coverage</code> · <code>/queue/mau-so</code>", "không nút; <kbd>Xuất báo cáo tuần</kbd> mờ (cửa <code>/weekly</code> chưa có); không dòng «tổng»; <code>dat = null</code> không vẽ như ĐẠT"],
            ["<b>F04</b> Nạp sao kê", "5 trạng thái ① chọn phạm vi (segment <kbd>Tất cả</kbd>/<kbd>Ngân hàng</kbd>/<kbd>Quỹ</kbd> + checkbox <code>chọn &lt;source_key&gt;</code>) → ② ảnh chụp mới nhất <kbd>Xem trước</kbd> + nút <kbd>Bản khai</kbd> mỗi nguồn → ②b thứ tự ngày (<kbd>ngày/tháng</kbd> / <kbd>tháng/ngày</kbd> từng nguồn, <kbd>Khai theo bằng chứng · N nguồn</kbd>) → ③ <kbd>Soát</kbd> → biên bản GỘP 9 dòng <code>Hạng · Luật · Kết quả · Đã đo · Nguồn dính · Thông điệp</code> → ④ <kbd>Nhận</kbd> (tắt khi CHẶN) → ⑤ <code>run_id</code> + <kbd>Mở hàng chờ để xử N dòng</kbd>", "<code>GET /sources</code> → <code>/chup?lan=Bank&amp;limit=10</code> → <code>/chup/{id}</code> → <code>/chup/{id}/thu-tu</code> → <code>POST /sources/{id}/thu-tu</code> / <code>/chup/{id}/thu-tu</code> → <code>POST /nap/lo/xem-truoc</code> → <code>POST /nap/lo</code>", "không ô nhập giao dịch, không nút <kbd>Đọc lại</kbd> (<code>QĐ-ITL-114</code>: nhịp thay người), không nút đẩy A-CCR; văn bản không dùng ký hiệu ⛔⚠⭐🔒 (<code>test_luat_ky_hieu_man_hinh</code>)"],
        ])
    ))

    out.append(S("s4-5", f"§4.5 Hộp thoại, mã lỗi, điều kiện hiển thị và thẻ {PARTIAL}", body=
        P("<b>18 hộp thoại</b> (<code>HT.mo</code>; đếm từ mã: F01 tiền 11 · F01 lệnh chi 1 · F02 6; khớp BA-13 §7). Luật chung: ô bắt buộc trống ⇒ hộp ở nguyên; Esc/bấm ngoài = đóng không làm gì; focus vào ô nhập đầu.")
        + T([("#", 3), ("Màn", 8), ("Tiêu đề (nguyên văn)", 30), ("Nút (trái → phải)", 27), ("Cửa khi bấm nút chính", 32)], [
            ["1", "F01 tiền", "<i>Lý do · dòng &lt;itl_id&gt;</i>", "<kbd>Thôi</kbd> · <kbd>Ghi lý do</kbd>", "<code>POST /queue/{id}/reason</code>"],
            ["2", "F01 tiền", "<i>Hoãn · dòng &lt;itl_id&gt;</i>", "<kbd>Thôi</kbd> · <kbd>Hoãn</kbd>", "<code>POST /queue/{id}/defer {until, reason}</code>"],
            ["3", "F01 tiền", "<i>Ghép lệnh · dòng &lt;itl_id&gt;</i> (lỗi: chỉ <kbd>Đóng</kbd>)", "<kbd>Thôi</kbd> · <kbd>Ghép</kbd> (disabled khi Σ lệch)", "<code>GET …/pm-candidates</code> → <code>POST /queue/{id}/match</code>"],
            ["4", "F01 tiền", "<i>Đã ghép · nhưng máy ⛔ KHÔNG tự điền được</i>", "<kbd>Đã hiểu</kbd>", "—"],
            ["5", "F01 tiền", "<i>Bỏ ghép · dòng &lt;itl_id&gt;</i>", "<kbd>Thôi</kbd> · <kbd>Bỏ cả chùm</kbd>", "<code>POST /queue/{id}/unmatch</code>"],
            ["6", "F01 tiền", "<i>Đã bỏ ghép</i>", "<kbd>Đã hiểu</kbd>", "—"],
            ["7", "F01 tiền", "<i>Xong · dòng &lt;itl_id&gt;</i>", "<kbd>Thôi</kbd> · <kbd>Xong</kbd>", "<code>POST /queue/{id}/done</code>"],
            ["8", "F01 tiền", "<i>Đã ghi</i>", "<kbd>Đã hiểu</kbd>", "—"],
            ["9", "F01 tiền", "<i>Mở lại · dòng &lt;itl_id&gt;</i>", "<kbd>Thôi</kbd> · <kbd>Mở lại</kbd>", "<code>POST /queue/{id}/reopen</code>"],
            ["10", "F01 tiền", "<i>Ghép cả lô · N dòng</i>", "<kbd>Thôi</kbd> · <kbd>Ghép cả lô</kbd>", "<code>POST /queue/match-lo {itl_ids, reason}</code>"],
            ["11", "F01 tiền", "<i>Đã ghép cả lô</i>", "<kbd>Đã hiểu</kbd>", "—"],
            ["12", "F01 lệnh", "<i>Tìm tiền cho lệnh &lt;pm_line_id&gt;</i> (chứa panel Bảng PM <code>n/28 cột</code>)", "<kbd>Thôi</kbd> · <kbd>Ghép</kbd>", "<code>GET /queue/lenh/{id}/itl-candidates</code> + <code>/queue/lenh/{id}</code> → <code>POST /queue/{itl_id}/match</code>"],
            ["13", "F02", "<i>không lấy thêm được</i>", "<kbd>Đóng</kbd>", "—"],
            ["14", "F02", "<i>Ô này đã vào sổ rồi</i>", "<kbd>Mở ngăn kéo dòng này</kbd> · <kbd>Đóng</kbd>", "—"],
            ["15", "F02", "<i>Giá trị bạn gõ KHÁC cái đang có</i>", "<kbd>Ghi đè</kbd> · <kbd>Để nguyên, không ghi</kbd>", "<code>POST /ledger/{id}/adjust {force:true, reason}</code>"],
            ["16", "F02", "<i>Ô này đã có NGƯỒI KHÁC gõ</i>", "<kbd>Lấy giá trị của họ</kbd> · <kbd>Giữ số của tôi, để tôi hỏi lại họ</kbd>", "— (chưa ghi gì)"],
            ["17", "F02", "<i>Lô lưu DỪNG giữa chừng</i>", "<kbd>Thử lại ngay</kbd> · <kbd>Đóng</kbd>", "gửi lại lô <code>/adjust</code>"],
            ["18", "F02", "<i>Đảo bút toán #&lt;adj_id&gt;</i>", "<kbd>Đảo</kbd> · <kbd>Thôi</kbd>", "<code>POST /adjustments/{adj_id}/reverse</code>"],
        ])
        + T([("Điều kiện", 22), ("Hiển thị", 42), ("Cưỡng chế ở đâu", 36)], [
            ["Cửa chỉ đọc (không <code>--cho-ghi</code>)", "<code>#p-cua</code> = <code>cửa: CHỈ ĐỌC</code>; mọi nút ghi <code>disabled</code> với <code>title</code> «⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC…»; F02 không ô nào gõ được và nói ra", "bảng tuyến: <code>tuyen.ghi</code> mà <code>mo_ghi is None</code> ⇒ 405 <code>FLS-METHOD</code>; PostgreSQL <code>default_transaction_read_only</code> trên đường đọc"],
            ["Không thẻ / thẻ hỏng", "trình duyệt nhận <code>phien.js</code> chở thẻ 8 giờ cho <code>--actor</code>; hết hạn ⇒ 401 mọi đường, kể cả 404/405 không lộ", "<code>the.py</code>: <code>alg</code> đúng bằng HS256, <code>exp</code> bắt buộc, <code>hmac.compare_digest</code>; thiếu <code>FLS_JWT_SECRET</code> ⇒ máy không dựng"],
            ["Phạm vi", "<code>#p-nap</code> hiện <code>lần nạp thật</code> hoặc <code>run_id</code>; dòng ngoài phạm vi ⇒ 404 <b>một câu</b> (không 403)", "<code>PhamVi</code> bắt buộc trên mọi hàm đọc; không có <code>ca_kho</code> trong <code>fls/api</code>"],
            ["Ai đang làm", "<code>#p-nguoi</code> = <code>kế toán · &lt;actor&gt;</code>", "actor <b>từ thẻ</b>; gửi trong thân ⇒ 400. <b>Hôm nay actor = cờ <code>--actor</code></b> lúc dựng máy ⇒ «ai sửa ô này» là «ai khởi động máy chủ» (<code>GAP-WEB-01</code>, <a href='#s10-3'>§10.3</a>)"],
            ["Máy nghe ngoài loopback", "từ chối chạy khi vừa <code>--cho-web</code> vừa địa chỉ ngoài <code>{127.0.0.1, ::1, localhost}</code> (<code>QĐ-ITL-76</code>)", "<code>cua.dung_may</code>; ⇒ hôm nay <b>0 máy khác</b> mở được màn — điều kiện UAT chưa có"],
        ])
    ))
    return out
