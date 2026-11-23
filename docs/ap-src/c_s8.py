# -*- coding: utf-8 -*-
"""§8 «Hoàn thành trông như thế nào» — FLS."""
from apgen import *

# (id, level, statement, governs[list of UF ids], status_text, red?)
HD = [
    ("HD-01", "L1", "Người mở màn vào thẳng tab ② với lằn <kbd>Theo LỆNH CHI</kbd> sáng; thanh trên nói <code>cửa: ĐỌC + GHI</code> hay <code>CHỈ ĐỌC</code> và tên actor.", ["UF-1.1", "UF-4.2"], "kho TEST: <code>test_man_f01_lenh_dom</code> 10 bài xanh [CODE 17/09]; sổ thật: chưa ai mở ngoài Dev", False),
    ("HD-02", "L1", "Bốn tab F01–F04 mở được từ một máy có kho sống; tab F06 tắt và nói vì sao (<code>GAP-SPEC-01</code>).", ["UF-1.1", "UF-2.1", "UF-3.1", "UF-3.7"], "<code>test_cua_phuc_vu_man_hinh_pg</code> 13 bài xanh; F06 <code>disabled</code> [CODE]", False),
    ("HD-03", "L1", "Máy từ chối dựng khi thiếu khoá, đường đọc còn ghi được, hay bảng tuyến / bảng tệp vi phạm — không có cửa nửa vời.", ["UF-4.2"], "<code>test_cua_pg</code> «thiếu khoá/kết nối ghi được ⇒ máy TỪ CHỐI CHẠY» xanh [CODE]", False),
    ("HD-04", "L2", "Ghép lô chỉ nhận dòng tự chứng: một dòng xấu ⇒ 422 cả lô và 0 mối nối mới; thành công ⇒ Σ mối nối = tiền bank từng dòng.", ["UF-1.3", "UF-5.3"], "<code>test_cua_ghep_lo_pg</code> 12 bài xanh; sổ thật: 0 lô người bấm (<code>B2</code> chưa) [DOC 10/09]", True),
    ("HD-05", "L2", "Ghép tay bị chặn khi Σ lệch quá <code>min(1.000, 0,5 %)</code> hay khác tiền tệ; nút <kbd>Ghép</kbd> mờ trước khi gọi cửa.", ["UF-1.4", "UF-1.5"], "<code>test_cua_ghep_pg</code> 14 bài xanh [CODE]", False),
    ("HD-06", "L2", "Bỏ ghép thêm dòng <code>fls_pm_unlink</code> và đảo đúng bút toán máy suy; không dòng nào bị xoá; ghép lại là <code>lan = 2</code>.", ["UF-1.8"], "<code>test_vong_f01_pg</code> «ghép→bỏ→ghép lại TRÒN» xanh; sổ thật <code>fls_pm_unlink = 0</code> (<code>B4</code> một nửa) [DOC 10/09]", True),
    ("HD-07", "L2", "Mọi thao tác ghi trừ <kbd>Xong</kbd> đều đòi lý do và ghi actor từ thẻ; <kbd>Mở lại</kbd> đòi lý do; hoãn không hạn bị từ chối; lần hoãn 3 đổi màu không leo cấp.", ["UF-1.9"], "<code>test_cua_ghi_pg</code> 18 bài xanh [CODE]", False),
    ("HD-08", "L2", "Gõ một ô Final ghi bút toán + nhật ký 7 trường trong <b>một</b> giao dịch; gõ lại cùng giá trị không sinh bút toán thứ hai.", ["UF-2.3", "UF-2.4"], "<code>test_vong_f02_pg</code> 14 bài xanh [CODE]", False),
    ("HD-09", "L2", "Gõ khác nguồn ⇒ 409 kèm giá trị đang có; chỉ <code>force</code> + lý do riêng mới ghi; mã ngoài 73 mã ⇒ <code>FLS-UNKNOWN-CODE</code>; kỳ sai khuôn ⇒ <code>FLS-BAD-FORMAT</code>.", ["UF-2.3", "UF-2.5"], "<code>test_lo_luu_f02</code> «khác nguồn HỎI NGƯỜI» + <code>test_cua_ghi_pg</code> xanh [CODE]", False),
    ("HD-10", "L2", "Đảo lùi đúng về bút toán trước; đảo bản đảo bị chặn; kỳ <code>locked</code> chặn kể cả <code>force</code>.", ["UF-2.6", "UF-2.7"], "<code>test_vong_f02_pg</code> xanh; kho thật <b>không có</b> đường tạo kỳ locked (<code>GAP-PLAN-04</code>)", True),
    ("HD-11", "L2", "Xem trước và Nhận trả <b>cùng</b> biên bản; CHẶN ⇒ 422 và 0 dòng; nạp lại cùng ảnh ⇒ 0 dòng trùng; <code>fls_run.chup_id</code> trỏ đúng ảnh; 0 dòng loại nào không có bản ghi.", ["UF-3.5", "UF-3.6", "UF-5.3"], "<code>test_cua_nap_lo_pg</code> 15 bài xanh; sổ thật: nạp <code>R |</code> bị NÚT chặn cho tới khi giải thích 3.413 dòng [DOC 10/09]", True),
    ("HD-12", "L2", "Nguồn chưa khai ⇒ 409 không đoán; khai lô chỉ nhận nguồn tự chứng và không nhận <code>thu_tu</code> từ màn; nguồn mâu thuẫn không được đề xuất.", ["UF-3.2", "UF-3.4"], "<code>test_cua_thu_tu_lo_pg</code> 11 bài xanh; đo 08/09: 29/29 nguồn mơ hồ là <code>mdy</code> [DOC]", False),
    ("HD-13", "L2", "Nhịp mỗi giờ 8–19h sinh ảnh với actor <code>nhip@fls</code>; giờ đã có ảnh bỏ lượt kèm lý do; dọn ảnh không đứt <code>fls_run.chup_id</code>; giờ trống đếm được từ kho.", ["UF-4.1", "UF-5.1", "UF-5.2"], "<b>ĐỎ</b>: log 16/09 mọi lượt trả mã 1 (kho không chạy); 11–15/09 không lượt nào [LOG 17/09]; <code>A1</code> đạt trên kho, chưa đạt vận hành", True),
    ("HD-14", "L3", "Dải việc chia ba rổ khép về tổng (<code>✓ a + b + c = tong</code>), mỗi rổ một câu; rổ «không» có câu vì sao; nút mỗi dòng đổi chữ theo rổ.", ["UF-1.2", "UF-1.6"], "<code>test_man_f01_lenh_g5_dom</code> 8 bài xanh; 250 + 535 + 768 = 1.553 [DOC 14/09]", False),
    ("HD-15", "L3", "Một trường một tên: <b>Số chứng từ</b> ở F01, F02 và panel; 0 lần «Mã tham chiếu» trong <code>fls/web/tep</code>.", ["UF-1.4", "UF-1.7", "UF-2.2"], "<code>tools/kiem_ten_truong.py</code> xanh (G1 xong 11/09) [CODE]", False),
    ("HD-16", "L3", "Biên bản soát nói luật nào đỏ, hạng gì, đã đo bao nhiêu, nguồn nào dính; <code>da_do = 0</code> hiện CHƯA ĐO, không xanh; xem trước ảnh hiện dấu thời điểm và nguồn 0 dòng.", ["UF-3.3", "UF-3.5", "UF-3.7"], "<code>test_man_f04_dom</code> 33 bài xanh [CODE]", False),
    ("HD-17", "L3", "Mỗi mã lỗi cửa có câu tiếng Việt và «làm gì»; không mã nào rơi ra chữ máy; cửa thêm mã mà màn thiếu câu ⇒ cổng đỏ.", ["UF-2.5", "UF-5.4"], "<code>test_goi_cua_phu_het_ma_loi</code> 6 bài xanh — 20 + 2 mã [CODE]", False),
    ("HD-18", "L3", "Panel F02 phân biệt «nguồn nói» và «người gõ»; ô phân bổ nói rõ là máy suy, <code>Method = 0</code> nói bẫy VLOOKUP, <code>#N/A</code> nói không tra được.", ["UF-2.2"], "<code>test_drawer_f02</code> 58 bài xanh [CODE]", False),
    ("HD-19", "L4", "Câu hỏi mặc định của F01 là câu của việc: hỏi 1.345 dòng lệnh chưa có tiền, không hỏi 7.682 dòng tiền; độ phủ chân màn đo phía PM (<code>QĐ-ITL-122</code>).", ["UF-1.1", "UF-1.2"], "lằn mặc định = LỆNH CHI [CODE]; 64,3 % phía PM [DOC 09/09]", False),
    ("HD-20", "L4", "Mọi số trên màn đi qua cửa; <code>fls.web</code> không import gì trong <code>fls</code>; đường đọc không bao giờ dùng kết nối ghi; chỉ hai tuyến được INSERT <code>fls_itl</code>.", ["UF-1.1", "UF-4.3"], "<code>lint-imports</code> 9/9 · <code>test_web_khong_biet_tang_duoi</code> · <code>test_them_vao_so</code> xanh [CODE]", False),
    ("HD-21", "L4", "Mốc đóng bằng con số máy đếm trên kho thật (<code>kiem_so_song</code>), không bằng bộ test xanh; 108.128 sự kiện <code>reason</code> do máy không đóng được cổng nào.", ["UF-4.3"], "109/109 [DOC 08/09]; <code>test_MAY_ghi_93k_su_kien_ma_KHONG_dong_duoc_cong_nao</code> xanh [CODE]", False),
    ("HD-22", "L5", "Một phiên sửa <b>thật</b>: ≥20 bút toán <code>fls_journal</code> của người thật trải cả 7 ô, ≥1 cặp adjust→reverse, và danh sách «đã phải mở Excel vì…» rỗng (<code>C1</code>, <code>C2</code>, <code>C5</code>).", ["UF-2.3", "UF-2.4", "UF-2.6"], "<b>ĐỎ</b>: <code>fls_journal = 0</code> [DOC 10/09] — lằn chưa ai đi qua", True),
    ("HD-23", "L5", "Một vòng hàng chờ <b>thật</b>: ≥1 <code>fls_queue_event</code> do người (<code>evt_type &lt;&gt; 'reason'</code>, <code>B5</code>), ≥1 <code>fls_pm_unlink</code> (<code>B4</code>), độ phủ đổi sau một lô thật (<code>B3</code>).", ["UF-1.3", "UF-1.8", "UF-1.9"], "<b>ĐỎ</b>: 0 · 0 · chưa [DOC 10/09]; mốc B 1 đạt · 1 nửa · 3 chưa", True),
    ("HD-24", "L5", "Kế toán ngồi máy của họ mở được màn và đăng nhập bằng tên mình; nhịp sống mà không ai ngồi cạnh (bộ hẹn giờ thức máy, Docker tự lên); một buổi UAT xảy ra.", ["UF-3.1", "UF-4.4", "UF-5.1"], "<b>ĐỔ</b>: <code>GAP-WEB-01</code>, loopback-only, <code>V1b</code> chặn ở quyền admin [DOC 10/09]; đăng nhập là PROPOSED (§10.3)", True),
]

UF_STEPS = ["UF-1.%d" % i for i in range(1, 10)] + ["UF-2.%d" % i for i in range(1, 8)] + ["UF-3.%d" % i for i in range(1, 8)] + ["UF-4.%d" % i for i in range(1, 5)] + ["UF-5.%d" % i for i in range(1, 5)]
LEVELS = ["L1", "L2", "L3", "L4", "L5"]

def sections():
    out = []
    out.append(S("s8", "§8 «Hoàn thành trông như thế nào» — phát biểu chấp nhận và lưới đối soát", st="draft", body=
        P("Userflows (§3) nói người <b>làm</b> gì; mục này nói cái gì phải <b>đúng</b> sau đó. Mỗi phát biểu quan sát được trên màn hoặc trong một dòng kho, một người kiểm trong vài phút, mang đúng một mức L1–L5, nêu bước UF nó chi phối, và có trạng thái đo kèm ngày. <b>Đỏ = CHƯA đạt, không phải chưa đo</b>; phần lớn phát biểu L1–L4 xanh trên kho TEST qua HTTP nhưng ba phát biểu L5 đỏ trên sổ thật — đúng bức tranh của <code>QĐ-ITL-128</code>.")
        + T([("Mức", 16), ("Câu hỏi", 84)], [
            ["<b>L1 · Reachable</b>", "Vai có tới được việc thật, hiện tại không? Không dead-end."],
            ["<b>L2 · Executable</b>", "Làm được thật không? Hành động hoàn tất, bền, không bị chặn bởi chi phí/chờ."],
            ["<b>L3 · Understandable</b>", "Biết đang được hỏi gì, và «xong» nghĩa là gì?"],
            ["<b>L4 · Goal-aligned</b>", "Chuỗi từ việc này tới mục tiêu (hai tác vụ) còn nguyên và <i>nhìn thấy</i>?"],
            ["<b>L5 · Sufficient</b>", "Làm việc này có thật sự dịch mục tiêu? Việc thật, không phải điểm danh."],
        ])
    ))

    rows = [[f"<b>{i}</b>", f"<code>{lv}</code>", st, " · ".join(g)] for i, lv, st, g, _, _ in HD]
    out.append(S("s8-1", "§8.1 Danh sách phát biểu HD-01…HD-24 theo mức", body=
        T([("ID", 8), ("Mức", 6), ("Phát biểu (quan sát được, một người kiểm trong vài phút)", 60), ("Governs (bước UF)", 26)], rows)
    ))

    rows2 = [[f"<b>{i}</b>", f"<code>{lv}</code>", txt] for i, lv, _, _, txt, red in HD]
    cls2 = ["holerow" if red else "" for *_, red in HD]
    out.append(S("s8-2", "§8.2 Bảng trạng thái đo được (đỏ = CHƯA đạt trên sổ thật)", body=
        P("Hai hạng chứng cứ, đừng gộp: <code>[CODE]</code> = bộ test xanh trên kho TEST (chứng minh <i>mã chạy đúng</i>); <code>[DOC dd/mm]</code>/<code>[LOG]</code> = con số trên sổ THẬT (chứng minh <i>việc đã xảy ra</i>). Luật của tệp mốc: <i>«bộ test xanh không đóng được một cổng của mốc»</i>.")
        + T([("ID", 8), ("Mức", 6), ("Trạng thái · số đo · ngày", 86)], rows2, rowcls=cls2)
        + T([("Mốc", 8), ("Cổng", 52), ("Máy đếm [DOC 10/09]", 40)], [
            ["<b>A</b>", "A1 ảnh tự động ≥2 giờ · A2 dọn 30 ngày, vết không đứt · A3 PM có đường vào (≥2 <code>run_id</code>) · A4 nạp PM không nhân đôi · A5b ảnh Bank đã nạp ≤48 h", "4 đạt · 1 một nửa (A2 xanh trên tập rỗng) · 1 chưa (A5b đo 88 h; nhịp dừng 11/09)"],
            ["<b>B</b>", "B1 mẫu số bằng sự kiện phía PM · B2 cửa ghép lô đã dùng trên sổ thật · B3 hậu quả đo được · B4 đường lùi (<code>fls_pm_unlink</code> ≥1) · B5 ≥1 sự kiện do người", "1 đạt (B1) · 1 một nửa (B4 có bài, sổ thật 0) · 3 chưa (B2·B3·B5: 0 cú bấm người)"],
            ["<b>C</b>", "C1 ≥20 bút toán người thật trải 7 ô · C2 adjust→reverse · C3 va chạm 409/force · C4 kỳ locked 409 · C5 không phải mở Excel", "0 bút toán thật; C3/C4 xanh trên TEST; C4 không có đường tạo kỳ locked"],
            ["<b>D</b>", "D1 bộ xuất 64 cột · D2 đối chiếu từng dòng sheet thật · D3 ghi an toàn · D4 chạy khô + owner duyệt · D5 vòng khép kín", "chỉ D3 (27 bài); D1/D2/D5 không tồn tại; D4 chờ đích (<a href='#s7-5'>§7.5</a>)"],
        ])
    ))

    # grid
    cover = {s: {l: [] for l in LEVELS} for s in UF_STEPS}
    for i, lv, _, g, _, _ in HD:
        for s in g:
            assert s in cover, s
            cover[s][lv].append(i)
    grows, gcls = [], []
    holes = 0
    for s in UF_STEPS:
        cells = []
        any_ = False
        for l in LEVELS:
            v = cover[s][l]
            if v:
                any_ = True
                cells.append(", ".join(v))
            else:
                cells.append('<span class="hole">▢</span>')
        grows.append([f"<b>{s}</b>"] + cells)
        gcls.append("" if any_ else "holerow")
        holes += 0 if any_ else 1
    from collections import Counter
    cnt = Counter(lv for _, lv, *_ in HD)
    out.append(S("s8-3", "§8.3 Lưới đối soát Userflow × L1–L5", body=
        P(f"Hàng = bước Userflow (31), cột = mức, ô = phát biểu HD phủ bước ở mức đó. <code>▢</code> = ô trống ở mức đó (bình thường); <b>hàng đỏ</b> = bước không có phát biểu nào — lỗ phải công bố. Phát biểu theo mức: " + " · ".join(f"<code>{l}</code> {cnt[l]}" for l in LEVELS) + f". Hàng trống: <b>{holes}</b>. Mọi phát biểu chi phối ≥1 bước và mọi bước có ≥1 phát biểu — điều kiện của §A.13 được kiểm bằng chính bộ sinh tài liệu này (assert khi dựng).")
        + T([("Bước", 15), ("L1 · Reachable", 17), ("L2 · Executable", 17), ("L3 · Understandable", 17), ("L4 · Goal-aligned", 17), ("L5 · Sufficient", 17)], grows, cls="grid-rec", rowcls=gcls)
        + P("<b>Đọc lưới một câu:</b> cột L5 chỉ có ba phát biểu và cả ba đều đỏ trên sổ thật — AP có ý kiến rõ rằng hệ chưa «đủ», và lỗ nằm ở <i>người dùng thật</i> (UAT), không ở mã. Cột L1–L2 dày vì FLS đo mọi thứ bằng test qua HTTP; muốn chuyển một ô từ TEST sang THẬT chỉ cần một buổi C1 + B5 (<a href='#s11-2'>§11.2</a>).")
    ))
    assert holes == 0, "còn bước UF không có phát biểu"
    return out
