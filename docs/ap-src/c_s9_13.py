# -*- coding: utf-8 -*-
"""§9 Gap · §10 Đề xuất · §11 Runbook · §12 Tham chiếu · §13 Phụ lục — FLS."""
from apgen import *

def sections():
    out = []
    # ---------------- §9 ----------------
    out.append(S("s9", "§9 Khoảng trống &amp; mục mở", st="draft", body=
        P("Sổ GAP gốc ở <code>01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md</code> §4 (~173 mã, 20 họ), trạng thái <b>không có SSOT</b> — chính tài liệu khai (<code>GAP-DOC-08</code>). Mục này chỉ giữ những gap <b>còn mở và có hệ quả kiến trúc</b>, cộng những lệch AP này tự đo được giữa mã và tài liệu.")
    ))
    out.append(S("s9-1", "§9.1 Gap kỹ thuật đang mở", body=
        T([("Mã", 14), ("Gap", 44), ("Hệ quả", 26), ("Đóng bằng", 16)], [
            ["<code>GAP-WEB-01</code>", "không đăng nhập; actor = cờ <code>--actor</code>; thẻ chở trong <code>phien.js</code>; máy từ chối nghe ngoài loopback", "«ai sửa ô này» = «ai khởi động máy chủ»; 0 máy khác mở được; UAT không làm được", "DEV-14 W1–W6 (<a href='#s10-3'>§10.3</a>)"],
            ["<code>GAP-CHUP-01</code>", "lằn PM không lưu dòng thô (0 vs 7,45 triệu ô lằn Bank)", "thêm cột PM phải đợi cú chụp sau; không bù ngược 3.772 dòng", "quyết định owner (kho to lên)"],
            ["<code>GAP-CHUP-02</code>", "kho không có trạng thái nguồn (<code>trang_thai_nguon: null</code>)", "F04 nói ra nhưng không tự đọc lại", "—"],
            ["<code>GAP-CHUP-04</code>", "<code>fls_run.khai_id</code> không định danh một bản khai (một dòng/trường)", "lineage đi đường <code>chup_nguon.khai_version</code>; cột <code>khai_id</code> thừa", "bỏ cột hoặc đổi mô hình"],
            ["<code>GAP-NAP-03</code>", "<code>fls_pm_line</code> khoá <code>(run_id, source_row)</code> cùng hình với lỗi <code>fls_reject</code> cũ; 9 bản sao mỗi giờ, <code>pm_line_id</code> không duy nhất toàn bảng", "SQL tay đếm sai 15× (23.295 vs 1.553); an toàn hôm nay vì 1 nguồn PM", "thêm <code>source_sheet</code> hoặc cổng"],
            ["<code>GAP-API-03</code>", "<code>rong</code>/<code>trung</code> không lưu ⇒ bốn đường không tái lập từ kho", "cổng <code>BON_DUONG</code> khai «chưa đo được» ở F03", "lưu hai con số vào <code>fls_run</code>"],
            ["<code>GAP-KHAI-02</code> · sheet đổi tên", "bản khai khoá theo <b>tên sheet</b>; đổi tên (mất một dấu cách) ⇒ lằn Bank đổ (10/09)", "nguồn cũ mồ côi, nguồn mới cần bản khai v1; sẽ tái diễn", "khoá theo gid hoặc cổng phát hiện"],
            ["Trigger 0015", "<code>triggers.py</code> liệt kê 2/3 trigger; <code>pg_verify</code> không so trigger/index/default", "lệch không có cổng", "mở rộng <code>pg_verify</code>"],
            ["<code>fls_run.state</code>", "SM-I04 8 trạng thái trong BA-09; mã dùng 2 (<code>staged → mapped</code>), mặc định <code>queued</code>", "sổ chạy không phân biệt run chết dở", "cắt BA-09 về mã hoặc dựng thêm"],
            ["<code>fls_queue_reason_weekly</code>", "view có, không tuyến nào đọc; thước <code>US-KT-045</code> «4 tuần không ai gõ = cổng chết» chưa lên màn", "không biết hệ kiểm soát còn sống", "<code>GET /queue/reason-weekly</code> + chân băng F01"],
            ["<code>GAP-CANON-02</code> · <code>GAP-PII-02</code> · <code>GAP-SCR-13</code>", "lằn quỹ: khuôn 11 cột; sheet <code>2. CCR Cash</code> có cột <code>ID/Pass</code>; F05 màn riêng hay bộ lọc", "chặn lằn Cash", "ngoài phạm vi đợt (ORC-09 §5)"],
            ["<code>GAP-LE-01</code> · <code>GAP-ALLOC-01</code>", "24/29 mã LE không tên; 52/73 <code>method_cfa2</code> rỗng ⇒ <code>Method = 0</code>", "panel F02 nói bẫy thay vì giá trị", "nguồn danh mục (AC-C)"],
        ])
    ))
    out.append(S("s9-2", "§9.2 Điều máy không chặn được và rủi ro vận hành", body=
        T([("Điều", 30), ("Sự thật", 44), ("Cách nói ra hôm nay", 26)], [
            ["Hai người sửa một ô (<code>GAP-SCR-09</code>)", "màn dừng và hỏi (hộp <i>Ô này đã có NGƯỜI KHÁC gõ</i>); cửa không có khoá lạc quan ở tầng kho", "nhật ký ghi cả hai; không có <code>If-Match</code>"],
            ["Ba danh sách suy không ép (<code>INV-I18</code>)", "không dùng dữ liệu để cưỡng chế giá trị (vòng tròn); máy chỉ đo", "cổng đo, không NO"],
            ["Danh mục rỗng (<code>INV-I17</code>)", "danh mục rỗng thì máy không biết, không phải «mọi mã đều sai»", "F02 nói «không tra được»"],
            ["Nhịp sống nhờ người ngồi cạnh", "bộ hẹn giờ ở mặc định PowerShell: <code>WakeToRun=False</code>, <code>DisallowStartIfOnBatteries=True</code>; Docker không tự lên; log 16/09 toàn mã 1", "<code>soi_nhip.py</code> mã 4 + bốn lý do; <code>do_gio_trong</code>"],
            ["Chỗ chạy", "FLS chạy trên <code>127.0.0.1</code> của máy Dev; <code>dung_may</code> từ chối ngoài loopback", "ORC-09 §7.1 ⓐ"],
            ["Nạp <code>R |</code> lên sổ hiện tại", "+6.617 dòng và 3.694 dòng trùng giữa hai <code>source_system</code>; khoảng lệch 3.413 dòng chưa giải thích", "NÚT cố ý chỉ chụp"],
            ["Một người rời đi", "2 người giữ 6.843 quyết định trong đầu (rủi ro số 1, <code>GAP-ITL-38</code>)", "<code>fls_journal</code> bắt buộc — nhưng đang 0"],
        ])
    ))
    out.append(S("s9-3", "§9.3 Tài liệu tự lệch với mã — đo khi viết AP này", body=
        T([("Chỗ lệch", 30), ("Tài liệu nói", 28), ("Mã / log nói", 28), ("Xử", 14)], [
            ["Số tuyến", "BA-07 v2.8: 35 tuyến", "<code>BANG_TUYEN</code>: 37 tuyến (thêm 3 cửa lệnh chi 09/09, 1 lô)", "BA-07 già 2 tuyến"],
            ["Số mối nối", "2.650 (27/08) · 2.745 (10/09) · 2.262 (15/09)", "không kho để đo; chênh không được giải thích trong tài liệu", "ghi cả ba kèm ngày"],
            ["Migration", "DEV-04 v1.12: 0001–0019", "22 tệp (0020–0022 ngày 10–11/09)", "DEV-04 già 3"],
            ["Trigger", "BA-11/DEV-04: INV-I03 vá TRUNCATE", "<code>triggers.py</code> 2 trigger; thứ 3 chỉ trong 0015", "khai §9.1"],
            ["Nhịp «đã đăng ký»", "ORC-09 v1.7 «đã đăng ký» (sai từ lúc viết, <code>QĐ-ITL-130</code> hoá thạch)", "log: đăng ký 09/09, đứt 11→15/09, đổ 16/09", "AP ghi theo log"],
            ["8.387 dòng", "MI §10 «kho 8.387 dòng sổ»", "con số không xuất hiện trong mã/comment; chỉ trong tài liệu", "nhãn [DOC]"],
            ["18 hộp thoại", "BA-13 §7: 18", "đếm <code>HT.mo</code>: 18 hộp / 20 lời gọi — khớp", "—"],
            ["«Cổng song song 103 lệch → 0» (commit 78beda9)", "không có cụm này trong 88 tệp docs; 103 là <code>QĐ-ITL-103</code>", "commit message nói về cổng số sống 109/109", "không dùng cụm ấy"],
            ["«Bản vẽ HAI CỘT» (commit 10ab2b6)", "không tệp nào tên vậy; bản vẽ TO-BE là bố cục «vẽ trái, thuyết minh phải»", "<code>Ban-ve-TOBE-Man-Ghep-PM.html</code> v0.3", "cite đúng tên tệp"],
            ["MI §8 kiểm kê", "«73 .md + 32 hiện vật»", "88 tệp đo ngày 17/09", "câu già"],
            ["Repo di chuyển trong lúc viết", "AP đo tại <code>bfeb1a7</code>", "7 commit mới cùng ngày (DD-I11 · trục «khẩu» Ⓐ/Ⓑ/Ⓒ · audit roadmap) + working tree: <code>schema.py</code> thêm 5 cột PE/PI cho <code>fls_pm_line</code>, migration <code>0023_pm_line_pe_pi.sql</code>, <code>pm_join.py</code>, <code>chay_nap.py</code> đổi — chưa commit", "không fold; v1.1.0"],
        ])
        + P("Hình dạng chung (<code>QĐ-ITL-103/130</code>): cổng số sống canh <b>con số</b>, không canh <b>câu</b>; một con số đúng có thể nằm trong một câu đã sai nhiều ngày. AP này cố ý ghi ngày đo bên mọi con số kho để không tạo thêm hoá thạch.")
    ))
    out.append(S("s9-4", "§9.4 Câu hỏi chủ sở hữu phải chốt", st="review", body=
        P("Bảy câu, mỗi câu đứng trước một nhóm việc. Trạng thái <code>review</code> của mục này chính là «đang nợ câu trả lời».")
        + OL([
            "<b>Ba cài đặt điện của bộ hẹn giờ + Docker tự lên</b> (<code>V1b</code>): đổi trên máy này, hay đây là câu trả lời «cần một chỗ chạy riêng»? Không đổi thì «nhịp mỗi giờ» mãi là «mỗi giờ nếu máy thức và cắm điện».",
            "<b>Một buổi C1 + B5</b>: kế toán (hoặc owner) ngồi sửa thật ≥20 bút toán và bấm ≥1 sự kiện hàng chờ trên sổ thật — Dev không bấm hộ được (actor sẽ là Dev, cổng xanh mà chưa đo gì).",
            "<b>«Sau này» của BigQuery là khi nào</b> (<code>QĐ-ITL-120/123</code>): quyết chặng ④ là <i>nhỏ</i> (chỉ xuất 64 cột) hay <i>lớn</i> (chuyển kho vận hành, mở lại <code>INV-I08</code>) — <a href='#s7-5'>§7.5</a>.",
            "<b>Nạp tầng <code>R |</code> lên sổ hiện tại</b>: chấp nhận giải thích 3.413 dòng lệch từng dòng trước, hay dựng lại sổ chỉ từ <code>R |</code> (bỏ lô <code>NAP-2026-08-27-RAW</code>)?",
            "<b>Lằn PM lưu dòng thô như lằn Bank không</b> (<code>GAP-CHUP-01</code>, G4)? Có thì kho to lên; không thì mọi cột mới không bù ngược được.",
            "<b><code>A2</code> chờ tới ~10/10/2026</b> (0 việc) hay nhận bằng chứng kho TEST là đủ?",
            "<b>Có cho <i>người</i> gán nhãn «vốn không cần lệnh chi» không</b> (<code>GAP-KT-05</code>)? Máy đã bị cấm (<code>QĐ-ITL-56/58</code>); câu này quyết có tồn tại một rổ thứ tư trên F01 hay không.",
        ])
    ))

    # ---------------- §10 ----------------
    out.append(S("s10", f"§10 Đề xuất — chưa xây (cách ly theo §A.11) {PROPOSED}", st="draft", body=
        P("Mọi thứ trong mục này <b>không có trong mã</b> ngày 2026-09-17. Nguồn: ORC-09 §4/§5, DEV-13 chặng ④, DEV-14/15, BA-07 các tuyến ⬜, MI §3 các QĐ ⏸. Thứ tự dưới là thứ tự tệp mốc khuyến nghị: D3 làm song song được, còn lại đi sau C1.")
    ))
    out.append(S("s10-1", f"§10.1 Chặng ④ — bộ xuất 64 cột D1 · đối chiếu D2 · vòng khép kín D5 {PROPOSED}", body=
        T([("Việc", 10), ("Cổng ra đo được (ORC-09 §4)", 50), ("Cái đã có để đứng lên", 40)], [
            ["<b>D1</b>", "xuất đúng khuôn 64 cột: 18 cột có giá trị · <b>22 cột giàn giáo</b> (Classifying 8 · Manual input 7 · MID 7) <b>rỗng có chủ ý</b> + một bài ghim điều đó · 24 cột còn lại <i>hoặc</i> lấy từ <code>canon</code> <i>hoặc</i> khai rõ không xuất", "<code>oracle/ledge_spec.py</code> đã khai 64 cột đi đâu (<code>SO_CHUA_QUYET = 0</code>); 7/7 cột Final đã lưu; <code>fls_sua_tay</code> cho giá trị hiệu lực"],
            ["<b>D2</b>", "đối chiếu với sheet <code>ITL Ledge</code> THẬT: chênh <b>liệt kê từng dòng</b>, không phần trăm; ĐẠT khi mọi chênh có tên lý do", "<code>oracle</code> đọc ADJUSTED có tự soi + đọc đủ; fixture 9.219 dòng 22 kỳ"],
            ["<b>D4</b>", "chạy khô rồi <b>owner duyệt</b>; cú ghi không chạy khi cờ duyệt tắt", "<code>ghi_o.ap_dung(duyet=True)</code> + <code>FLS_CHO_GHI_SHEET=1</code> đã có; chỉ <b>đích</b> chờ <a href='#s7-5'>§7.5</a>"],
            ["<b>D5</b>", "sửa một ô ở F02 → xuất → ô ấy đổi đúng trong bản xuất; <code>fls_journal</code> truy được ai sửa lúc nào", "cần D1 + C1"],
        ])
        + P("Vì sao chưa làm: D là <i>nội dung của bảy ô Final</i>; xuất trước khi có bút toán sửa thật thì D2 đối chiếu một bản xuất chưa ai chạm — «xanh mà chưa đo gì». Ngoại lệ duy nhất là D3 (đã xong).")
    ))
    out.append(S("s10-2", f"§10.2 Bề mặt và lằn gác lại — F06, F05/Cash, adapters C·D·E·F, 4 ledger nền tảng {PROPOSED}", body=
        T([("Hạng mục", 24), ("Trạng thái", 30), ("Vì sao gác (ORC-09 §5)", 46)], [
            ["<b>F06 Danh mục · Nguồn</b> (chỉ-đọc, <code>QĐ-ITL-47</code>) + <code>GET /catalog</code>, <code>/mapping-master</code>, <code>/le</code>", "tab <code>disabled</code>; <code>GAP-SPEC-01</code> chưa đặc tả", "không phục vụ hai tác vụ; chặn B7 UAT nhưng UAT là của hai màn kia; <code>/mapping-master</code> chỉ làm nếu C5 đo ra kế toán phải mở Excel"],
            ["<b>Lằn quỹ Cash / F05</b> (8 nguồn, khuôn 11 cột)", "0 ảnh chụp; <code>GAP-SCR-13</code>, <code>GAP-CANON-02</code>, <code>GAP-PII-02</code> chặn ở owner", "ngoài phạm vi đợt"],
            ["<b>Adapters C (A-CCR) · D (HR/H1000) · E (Platform) · F (AP/AR)</b>", "adapters 55 %; QĐ-ITL-03 gói riêng", "nuôi lằn pipeline, không nuôi mapping/adjust; nợ lớn nhất theo khối lượng — gác thì bảng tiến độ đứng yên, «và đó là sự thật»"],
            ["<b>4 ledger nền tảng</b> GI/OMC/SC/PS (15.517 ô, <code>QĐ-ITL-05</code>)", "chặn <code>GAP-ITL-18</code> (ranh giới ACA v2)", "đợt 4 lộ trình Gsheet→UI"],
            ["<b>Engine báo cáo · một trang/tuần CFO · máy quét xu hướng · <code>GET /weekly</code></b>", "nút mờ trên F03", "không phục vụ hai tác vụ"],
            ["Vùng PHÂN BỔ (CFA1/CFA2/Method) sửa được", "hiện là phép tính chỉ-đọc (<code>QĐ-ITL-64/65</code>)", "chờ cùng <code>/mapping-master</code>"],
        ])
    ))
    out.append(S("s10-3", f"§10.3 Chỗ chạy + đăng nhập (DEV-14 W1–W6) và BigQuery {PROPOSED}", body=
        P("<b>Đăng nhập thật</b> (đóng <code>GAP-WEB-01</code>): Google Sign-In (OIDC) khoá miền <code>apero.vn</code>, không kho mật khẩu; chỗ chạy giai đoạn I = máy này + <code>tailscale serve</code> (HTTPS <code>*.ts.net</code>, vì Google từ chối <code>redirect_uri</code> http ngoài localhost), giai đoạn II = GCP <code>asia-southeast1</code> + Cloud SQL.")
        + OL([
            "vỏ ra không thẻ → <code>GET /gates</code> 401 → nút <kbd>Đăng nhập bằng Google</kbd>",
            "<code>GET /dang-nhap</code> → Google → <code>GET /dang-nhap/ve</code>",
            "kiểm RS256 bằng thư viện (<code>PyJWT[crypto]</code>), đúc thẻ HS256 ngắn hạn — <code>the.py</code> <b>không đổi</b>",
            "cookie <code>fls_the</code> HttpOnly · Secure · SameSite=Lax; bỏ thẻ khỏi <code>phien.js</code>; <code>danh_muc.js</code> 73 mã phải nằm sau thẻ",
            "⚠ <code>tailscale serve</code> <b>đi vòng</b> qua <code>kiem_phuc_vu_tep</code> (proxy nối vào 127.0.0.1) ⇒ <b>cấm</b> chạy trước việc 1+1b",
            "6 cổng W1–W6; 7 việc; biến <code>FLS_GOOGLE_CLIENT_ID/SECRET</code> chỉ tên, không giá trị",
        ])
        + P("Trạng thái: kế hoạch v0.1 (11/09), <b>chưa thi công</b> — mã không có <code>fls/api/dang_nhap.py</code>, <code>BANG_TUYEN</code> không có <code>/dang-nhap</code>. Phân quyền theo vai vẫn là bước sau (DEV-14 §6: «mọi người đăng nhập được đều làm được mọi thứ»).")
        + P("<b>BigQuery</b>: <code>QĐ-ITL-120</code> chốt đích lưu trữ dài hạn, <code>QĐ-ITL-123</code> hoãn; <code>QĐ-ITL-46</code> FPA-T4 đọc một bảng ITL trên BQ ⏸. 0 dòng mã. Lựa chọn ở <a href='#s7-5'>§7.5</a>.")
    ))
    out.append(S("s10-4", f"§10.4 Chốt kỳ, thước sống của hàng chờ, và các trạng thái BA-09 chưa dựng {PROPOSED}", body=
        T([("Hạng mục", 28), ("Đặc tả có", 36), ("Mã có", 36)], [
            ["Chốt kỳ và ký (UC-KT-22, SM-I05)", "<code>open → cutoff → flash → reconciled → signed → locked</code>; chỉ COO-CFO mở lại kèm lý do (SoD-3)", "cột <code>period_state</code> open|locked + <code>INV-I13</code> chặn ghi; <b>không</b> cửa/nút nào đưa kỳ sang locked; vai ký chưa có người (<code>GAP-PLAN-04</code>)"],
            ["Thước «có ai đọc bảng việc không» (<code>US-KT-045</code>)", "cột lý do đã được gõ N lần trong 4 tuần; 4 tuần = 0 ⇒ cổng chết", "view <code>fls_queue_reason_weekly</code> có; không tuyến, không chân băng"],
            ["Lý do · Hoãn · Bỏ ghép · Xong trên lằn LỆNH CHI", "BA-13 §… ghi «chưa có»", "ranh giới kho: <code>fls_queue_event</code> chỉ treo vào <code>itl_id</code>; cần quyết có treo vào dòng lệnh không"],
            ["SM-I04 đầy đủ (<code>dq_passed · reconciling · published · superseded</code>)", "BA-09", "2 trạng thái"],
            ["<code>proposed_by_rule</code> trong SM-I02", "«phần code hoá cứu được»", "<code>_thyt</code> đã là dạng gián tiếp; chưa có trạng thái riêng"],
            ["Khoá lạc quan ô (<code>If-Match</code>)", "—", "màn hỏi người; kho không có"],
        ])
    ))

    # ---------------- §11 ----------------
    out.append(S("s11", "§11 Runbook · việc kế tiếp", st="draft", part="PART D · HẬU MỤC", body=P("Runbook thật nằm rải ở NÚT, <code>tools/</code> và MI §10 (DEV-07 là bản copy chương trình chưa dẫn xuất — <code>GAP-DOC-03</code>). Dưới đây là phần tối thiểu để một người mới bật được hệ và đo được nó.")))
    out.append(S("s11-1", "§11.1 Runbook tối thiểu", body=
        UL([
            "<b>Kho:</b> <code>docker compose up -d pg</code> · <code>docker exec fls-pg-1 pg_isready -U fls -d fls</code> · di trú <code>PG_DSN=… python -m fls.db.pg_migrate</code> (<code>--status</code> · <code>--dry-run</code> · <code>--adopt-baseline</code>) · <code>python -m fls.db.pg_verify</code> phải 0 lệch.",
            "<b>Chụp:</b> owner bấm <code>NUT-CHAY-FLS.cmd</code> (chỉ chụp) hoặc để nhịp <code>'FLS nhip chup'</code> chạy; soi <code>python tools/soi_nhip.py</code> (mã 0) và <code>python tools/nut_trang_thai.py</code>.",
            "<b>Cửa + màn (UAT trên máy này):</b> <code>NUT-MO-MAN-HINH.cmd</code> → <code>http://127.0.0.1:8088/</code>; hay tay: <code>PG_DSN=… FLS_JWT_SECRET=… python tools/chay_cua.py --cho-web [--cho-ghi] --actor &lt;email&gt;</code>; <code>--in-bang-tuyen</code> in 37 tuyến.",
            "<b>Cổng:</b> <code>lint-imports</code> · <code>PYTHONUTF8=1 pytest</code> (1.652 bài; <code>-m \"not pg\"</code> chạy offline) · <code>python tools/kiem_so_song.py</code> (109/109 + mốc A/B) · <code>python tools/kiem_nguon_song.py</code> (cần token) · <code>cd docs/ITL && PYTHONUTF8=1 python _tools/kiem_tai_lieu.py</code> (K1–K5) · <code>python tools/sinh_ban_do_tang.py --kiem</code>.",
            "<b>Đo:</b> <code>python tools/do_mau_so.py</code> (mẫu số, trần cứng, ba rổ) · <code>python tools/tien_do.py --json</code> · <code>python tools/nhin_so.py</code> (đọc sổ chỉ-đọc).",
            "<b>Sao lưu / dựng lại:</b> <code>python tools/sao_luu_kho.py</code> rồi <code>--so-sanh</code>; dựng lại sổ chỉ từ <code>R |</code>: <code>python tools/dung_lai_so.py</code> (đường F04, có cổng bốn đường).",
            "<b>Kiểm AP này:</b> <code>python docs/ap-status-check.py docs/architecturepack_FLS_v1.0.0_current-state_2026-09-17.html</code> → phải <code>0 failure(s)</code>.",
            "<b>Bắt buộc trên Windows:</b> <code>PYTHONUTF8=1</code> + <code>PYTHONIOENCODING=utf-8</code>; tệp <code>.cmd</code> phải ASCII thuần.",
        ])
    ))
    out.append(S("s11-2", "§11.2 Việc kế tiếp — theo thứ tự tệp mốc và lộ trình", body=
        T([("#", 5), ("Việc", 40), ("Của ai", 12), ("Đóng gì", 20), ("Đo xong bằng", 23)], [
            ["1", "<code>V1b</code> ba cài đặt điện Task Scheduler + Docker tự lên (lệnh PowerShell admin ở ORC-09 §8.3)", "owner", "<code>A1</code> vế vận hành; HD-13", "<code>soi_nhip.py</code> mã 0; log nhịp không còn mã 1"],
            ["2", "Bật lại kho và để nhịp chạy một ngày không ai ngồi cạnh", "owner + Dev", "HD-13", "<code>do_gio_trong</code> = 0 cho cả hai lằn"],
            ["3", "<b>Một buổi C1 + B5</b> trên máy này: ≥20 bút toán trải 7 ô, ≥1 sự kiện hàng chờ, ≥1 bỏ ghép", "kế toán / owner", "<code>C1 C2 B4 B5</code>; HD-22, HD-23", "<code>_cong_moc_b</code> đổi; <code>fls_journal ≥ 20</code>"],
            ["4", "<code>V4</code> nối <code>do_gio_trong</code> vào <code>_cong_moc_a</code> (mốc A tụt 4→2 đạt — con số tốt hơn, owner chốt)", "owner", "<code>A1</code>", "<code>kiem_so_song</code>"],
            ["5", "<code>V2</code> chờ tới ~10/10 hoặc nhận bằng chứng TEST", "owner", "<code>A2</code>", "<code>moc_a_nua = 0</code>"],
            ["6", "Đối chiếu hai bản khai 13 nguồn ra 0 dòng (<code>nap_nguon_dai.py --that</code>); câu hỏi kế toán về 2 sheet ACB USD (dòng 1 vs danh mục)", "Dev + kế toán", "V3 phần còn lại", "<code>khai_rong()</code> gọi tên → rỗng"],
            ["7", "Quyết định <a href='#s9-4'>§9.4</a> ④ (nạp <code>R |</code> lên sổ) rồi mở nạp thật qua F04", "owner → AC-A", "HD-11 trên sổ thật", "<code>fls_run</code> có <code>run_id</code> F04 với <code>chup_id</code>"],
            ["8", "Đăng nhập + chỗ chạy (DEV-14 việc 1+1b trước, rồi W1–W6)", "Dev", "<code>GAP-WEB-01</code>; HD-24", "một kế toán mở màn từ máy họ"],
            ["9", "Chặng ④: D1 trên PostgreSQL (§7.5 B), D2 đối chiếu từng dòng, D4 sau khi owner chốt đích", "Dev", "mốc D", "chênh liệt kê từng dòng, mọi chênh có tên"],
            ["10", "Đồng bộ tài liệu già (BA-07 37 tuyến, DEV-04 22 migration, <code>triggers.py</code>) và mở rộng <code>pg_verify</code> so trigger", "Dev", "<a href='#s9-3'>§9.3</a>", "<code>kiem_tai_lieu</code> 5/5; số sống N/N"],
        ])
    ))

    # ---------------- §12 ----------------
    out.append(S("s12", "§12 Tham chiếu", st="draft", body=
        T([("Nhóm", 18), ("Tài liệu", 82)], [
            ["Mã (SSOT)", "<code>fls/db/schema.py</code> · <code>fls/db/model.py</code> · <code>fls/db/migrations/0001–0022</code> · <code>fls/api/bang_tuyen.py</code> · <code>fls/api/the.py</code> · <code>fls/web/tep/*.js</code> · <code>.importlinter</code> · <code>tools/kiem_so_song.py</code> · <code>tools/chay_cua.py</code> · <code>NUT-CHAY-FLS.cmd</code> · <code>NUT-MO-MAN-HINH.cmd</code>"],
            ["Bộ tài liệu ITL", "<code>docs/ITL/00_MASTER_INDEX.md</code> v0.28 (§3 sổ QĐ · §10 trạng thái) · <code>01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md</code> đợt 43 · <code>09_MILESTONES_HAI_TAC_VU.md</code> v1.12 · <code>07_CHANGE_CONTROL.md</code> v1.5 (CR#1–11)"],
            ["BA", "<code>02_BA/04_ROLE_PERMISSION_MATRIX</code> v0.3 · <code>05_DATA_DICTIONARY_ERD</code> v0.24 · <code>06_SCREEN_SPEC</code> v3.0 · <code>07_API_CONTRACT</code> v2.8 · <code>09_STATE_MACHINE_SPEC</code> v0.4 · <code>11_INVARIANTS</code> v0.9 · <code>12_BA_MAN_GHEP_PM</code> v0.2 · <code>13_THUYET_MINH_MAN_HINH</code> v1.0 · <code>Artifacts/Ban-ve-TOBE-Man-Ghep-PM.html</code> v0.3 · <code>Artifacts/Ban-do-Kien-truc-7-Tang.html</code> · <code>Artifacts/UC-US-Ke-toan-PM-den-ITL.md</code> v0.4"],
            ["Dev · Test", "<code>03_Dev/01_TECH_DESIGN</code> v1.0 · <code>03_IMPLEMENTATION_PLAN</code> v4.7 · <code>04_DB_IMPLEMENTATION</code> v1.12 · <code>09_CR1_PM_JOIN_MODEL</code> · <code>10_PM_JOIN_ADAPTER_SPEC</code> v0.8 · <code>11_ORACLE_READ_SPEC</code> v1.3 · <code>12_P6_WEB_PLAN</code> v0.8 · <code>13_LO_TRINH_HAI_TAC_VU</code> v3.2 · <code>14_CHO_CHAY_VA_DANG_NHAP</code> v0.1 · <code>15_HUONG_DAN_OWNER_CHO_CHAY</code> v0.1 · <code>04_Test/01_TESTING_FRAMEWORK</code> v1.0"],
            ["Sheet nguồn (chỉ đọc)", "workbook P100 (64 sheet <code>R |</code>, <code>BankAccountList</code>) · bản sao RAW <code>1md85t…</code> › <code>Transaction Mapping L1</code> · sổ gốc ADJUSTED <code>1r4Wem…</code> › <code>ITL Ledge</code> · <code>[Importrange]PM_Unpivot</code> · tab <code>Mapping Master</code>"],
            ["Khuôn AP", "<code>FIN-ERP/authoring-kit-redacted/skills/build-ap/SKILL.md</code> §A.1–§A.18 · <code>FPA-T4/docs/architecturepack_FPA-T4_v2.0.0_unified_2026-09-16.html</code> (shell CSS/JS tái dùng nguyên văn) · <code>docs/ap-status-check.py</code>"],
        ])
    ))

    # ---------------- §13 ----------------
    out.append(S("s13", "§13 Phụ lục", st="draft", body=P("Bốn phụ lục: sổ nguồn đã fold (A), từ điển (B), danh mục probe (C), cách kiểm AP (D).")))
    out.append(S("s13-1", "Phụ lục A — Sổ nguồn — verdict từng nguồn đã fold", body=
        P(f"Phân loại nguồn trước khi fold (§A.11). {BUILT}/{PARTIAL} được vào thân; {PROPOSED} chỉ vào §10; {SUPERSEDED}/HISTORICAL chỉ được trích dẫn.")
        + T([("Nguồn", 30), ("Kích cỡ · ngày", 16), ("Verdict", 18), ("Fold vào", 36)], [
            ["<code>fls/</code> 62 tệp · <code>tools/</code> 51 · <code>tests/</code> 123 tệp", "@ <code>bfeb1a7</code> 15/09", BUILT + " [CODE]", "§1, §2, §4, §5, §6 — thắng về mọi con số mã"],
            ["<code>.nhip/nhip_chup.log</code> 43 lượt", "09/09 → 16/09", "[LOG]", "§2.1, §8.2 HD-13"],
            ["<code>00_MASTER_INDEX.md</code> §3/§10", "277 KB · v0.28 08/09", BUILT + " canonical (sổ QĐ)", "§7.1, §0.1 con số neo"],
            ["<code>09_MILESTONES_HAI_TAC_VU.md</code> · <code>13_LO_TRINH_HAI_TAC_VU.md</code>", "v1.12 10/09 · v3.2 10/09", PARTIAL + " (mốc đo, cổng chưa đạt)", "§8, §10, §11"],
            ["<code>06_ORCHESTRATOR_DASHBOARD.md</code> §4 GAP", "441 KB · đợt 43 09/09", PARTIAL + " (trạng thái GAP không SSOT)", "§9"],
            ["BA-04 · BA-09 · BA-11 · BA-12 · BA-13", "08–09/09", BUILT + " với lệch khai ở §9.3", "§3.1, §2.4, §5.5, §4"],
            ["BA-07 v2.8 (35 tuyến)", "09/09", PARTIAL + " (già 2 tuyến)", "§6.2 đối chiếu; mã thắng"],
            ["BA-05 v0.24 · <code>Ban-do-Kien-truc-7-Tang.html</code> · <code>ERD-TANG.mmd</code>", "15/09", BUILT + " (sinh từ schema)", "§1.1 tái dùng SVG"],
            ["<code>Ban-ve-TOBE-Man-Ghep-PM.html</code> v0.3", "14/09", BUILT + " (nhãn trích từ mã) + " + PROPOSED + " (§2, §7 bản vẽ)", "§4.2; con số 250/535/768"],
            ["DEV-14 · DEV-15", "v0.1 11/09", PROPOSED, "§10.3"],
            ["<code>ArchitecturePack-Ledger.md</code> v0.3", "07/09", PROPOSED + " (trừ STM/BNK/CSH)", "cite-only"],
            ["DEV-00/05/06/07/08 · TST-00/02/03 · <code>_DOC_REWRITE_ROADMAP</code> · <code>Ket-qua-*.md</code> · ERD chương trình cũ", "⏸ / 08/2026", "HISTORICAL", "không fold"],
            ["AP FPA-T4 v2.0.0", "16/09, hệ khác", "khuôn hình thức", "shell CSS/JS; không fold số liệu"],
            ["7 commit <code>5a988c9…b0b40c0</code> + working tree 0023 (PE/PI có kiểu)", "17/09 12:05–16:03", "<b>SAU MỐC ĐO</b> — chưa xác minh", "không fold; khai ở §0 và §9.3; ứng viên đầu cho v1.1.0"],
        ])
    ))
    out.append(S("s13-2", "Phụ lục B — Từ điển thuật ngữ rút gọn", body=
        P("Bảng đầy đủ 40 mục ở Dossier D §11 / MI §4; đây là những từ AP dùng lại nhiều mà người ngoài dự án hay đọc sai. Bẫy đồng âm xem <a href='#s1-5'>§1.5</a>.")
        + T([("Từ", 16), ("Nghĩa", 84)], [
            ["sao kê · <code>R |</code>", "sheet thô kế toán dán từ bank; ba vùng thô → công thức → CHUẨN (6 cột FLS đọc)"],
            ["lệnh chi · PM", "phiếu chuyển tiền FPS; đơn vị ghép là <b>dòng lệnh</b> (<code>fls_pm_line</code>)"],
            ["mối nối · bỏ mối nối", "<code>fls_pm_link</code> / thêm dòng <code>fls_pm_unlink</code>; hiệu lực = view <code>fls_moi_noi</code>"],
            ["ảnh chụp · nhịp chụp", "bản sao đóng băng sheet vào kho (<code>fls_chup*</code>); cron mỗi giờ 8h–19h"],
            ["bản khai cột · khai cột", "<code>fls_khai_cot</code>: nguồn X version V trường T đọc cột N (+ <code>thu_tu</code>) — lưu cách đọc, không lưu dữ liệu"],
            ["cửa · bảng tuyến · thẻ", "tuyến API / <code>BANG_TUYEN</code> khai cửa nào chạm bảng nào / JWT bắt buộc"],
            ["kho THẬT · kho TEST", "<code>fls</code> / <code>fls_test</code>; tách cứng bằng <code>dsn_test()</code>"],
            ["số sống · cổng · hoá thạch", "con số có máy so (<code>kiem_so_song</code>) / phép kiểm tự động phải «đã thấy đỏ» / số đúng trong câu sai"],
            ["thước chuẩn · oracle", "ảnh chụp đóng băng ITL Ledge dùng làm parity; không biết tầng ghi"],
            ["Final 7 khối · <code>_thyt</code>", "7 khối ADJUSTMENT × 4 cột trên ITL Ledge / cột «thật» NULL chỗ máy bịa"],
            ["UNMAPPED · tự chứng · rổ", "trạng thái tường minh thay mặc định im lặng / cửa GHI chắc chắn nhận / máy · người · không"],
            ["mốc A/B/C/D · chặng ①–④ · V1a–V4", "trục hiện hành; plan mốc A; P0–P8, B1–B7, G1–G5, Đ1–Đ6 là các dải ký hiệu khác, cố ý tách"],
            ["bia · biên bản", "câu cũ gạch ngang nhưng không xoá — nhật ký kiểu bia"],
            ["<code>[O] [E] [C] [L]</code>", "nhãn nguồn: owner xác nhận · spec · đã verify code · đọc live"],
        ])
    ))
    probes = [
        ["FLS-P01", "Mở màn & cửa", "vào tab ② lằn LỆNH CHI; <code>#p-cua</code> nói đúng chế độ; cổng 8088 trùng ⇒ NÚT từ chối", "lằn TIỀN mặc định; hai máy một cổng"],
        ["FLS-P02", "Fail-closed thẻ", "không thẻ/hết hạn/alg none ⇒ 401 mọi đường, không lộ 404/405", "404 lộ đường tồn tại; thẻ <code>alg:none</code> qua"],
        ["FLS-P03", "Ba rổ khép", "<code>a+b+c = tong</code>; rổ «không» có <code>vi_sao</code>; nút đổi chữ theo rổ", "rổ không khép; nút giống hệt mọi dòng"],
        ["FLS-P04", "Ghép lô tự chứng", "thân chỉ <code>itl_ids[]</code>; một dòng xấu ⇒ 422 cả lô, 0 mối nối", "nhận <code>pm_line_ids</code>/<code>force</code>; ghi một nửa lô"],
        ["FLS-P05", "Σ mối nối", "Σ <code>fls_moi_noi.amount</code> theo <code>itl_id</code> = tiền bank từng dòng (cổng <code>SIGMA_MOI_NOI</code>)", "lệch một đồng"],
        ["FLS-P06", "Dung sai", "lệch > <code>min(1.000, 0,5 %)</code> hay khác tiền tệ ⇒ nút mờ + 422", "ghép được"],
        ["FLS-P07", "Actor từ thẻ", "sự kiện/bút toán mang <code>sub</code> của thẻ; <code>actor</code> trong thân ⇒ 400", "actor từ thân"],
        ["FLS-P08", "Ghim cột", "lớp ghim trên cả <code>th</code> và <code>td</code>; 28 cột thô khi <code>tho</code> có", "tiêu đề trôi ngang"],
        ["FLS-P09", "Bỏ ghép = thêm", "<code>fls_pm_unlink</code> +N; <code>fls_pm_link</code> không mất dòng; ghép lại <code>lan = 2</code>", "dòng biến mất"],
        ["FLS-P10", "Lý do bắt buộc", "mọi ghi trừ Xong đòi lý do; hoãn không hạn 400; Mở lại chưa xong 409", "Xong đòi lý do; hoãn không hạn nhận"],
        ["FLS-P11", "Kho sạch", "sổ ra chỉ có <code>run_id</code> khớp <code>NAP-…</code>; <1.000 dòng ⇒ KHÔNG ĐẠT", "dòng test lọt"],
        ["FLS-P12", "Panel không che", "panel là cột phải; 7 nhóm; 38 cột canon; ô ALLOCATE chỉ đọc", "panel che lưới; gõ được ALLOCATE"],
        ["FLS-P13", "409 khác nguồn", "hộp với ba giá trị; <code>force</code> + lý do riêng mới ghi", "ghi đè không hộp"],
        ["FLS-P14", "7 phép chặn", "<code>UNKNOWN-CODE · BAD-FORMAT · LOCKED-PERIOD (kể cả force) · UNMAPPED-HIDDEN · CONFLICT-SOURCE · SOAT-CHAN</code> + trigger", "một phép chặn không nổ"],
        ["FLS-P15", "Lô lưu", "2,5 s tự bay; không lý do không bay; mạng đứt liệt kê ô chưa vào sổ", "mất ô; bay dù thiếu lý do"],
        ["FLS-P16", "Hai người", "hộp <i>Ô này đã có NGƯỜI KHÁC gõ</i>, máy chưa ghi gì", "đè im lặng"],
        ["FLS-P17", "Đảo", "+1 dòng <code>reversal_of</code>; giá trị hiệu lực lùi; đảo bản đảo chặn", "bút toán biến mất"],
        ["FLS-P18", "Không đoán bản khai", "nguồn chưa khai 409; nút <kbd>Bản khai</kbd> tắt", "máy đoán vị trí cột"],
        ["FLS-P19", "Ảnh chụp trung thực", "nguồn 0 dòng liệt kê; dấu thời điểm; không cột PII", "ẩn nguồn rỗng; hiện <code>Description</code>"],
        ["FLS-P20", "Thứ tự ngày", "máy đề xuất kèm bằng chứng số; lô không nhận <code>thu_tu</code>; mâu thuẫn không đề xuất", "màn chọn cho cả lô"],
        ["FLS-P21", "Biên bản 9 luật", "hạng · đã đo · nguồn dính; <code>da_do = 0</code> = CHƯA ĐO; CHẶN ⇒ Nhận tắt", "xanh trên tập rỗng; Nhận sáng khi CHẶN"],
        ["FLS-P22", "Xem trước = Nhận", "cùng biên bản; nạp lại cùng ảnh 0 trùng; <code>chup_id</code> đúng", "biên bản khác; nhân đôi"],
        ["FLS-P23", "F03 trung thực", "<code>dat = null</code> ≠ ĐẠT; không dòng tổng gộp tiền tệ", "null vẽ xanh"],
        ["FLS-P24", "Nhịp sống", "log mã 0 mỗi giờ 8–19h; <code>do_gio_trong</code> = 0; dọn không đứt vết", "mã 1 liên tiếp; xoá ảnh đã nạp"],
        ["FLS-P25", "Mốc do máy đếm", "<code>kiem_so_song</code> đếm A/B; 108k sự kiện máy đóng 0 cổng; <code>soi_nhip</code> đọc số rồi mới kết luận", "cổng xanh vì bộ test xanh"],
    ]
    out.append(S("s13-3", "Phụ lục C — Danh mục probe FLS-P01…P25", body=
        P("Probe là điều một người (hoặc UserAgent) kiểm được trong vài phút trên màn hoặc kho; mỗi bước UF ở §3 trỏ tới ≥1 probe. Phần lớn probe đã có bài test tương ứng (§6.4) — probe là bản «đọc bằng mắt» của bài ấy trên sổ THẬT.")
        + T([("Probe", 9), ("Tên", 16), ("PASS khi", 45), ("FAIL trông như", 30)], [[f"<b>{a}</b>", b, c, d] for a, b, c, d in probes])
    ))
    out.append(S("s13-4", "Phụ lục D — Cách kiểm AP này", body=
        P("File đi kèm <code>docs/ap-status-check.py</code> (chép nguyên từ FPA-T4). Ba việc nó làm và một việc nó cố ý không làm:")
        + UL([
            "<code>python docs/ap-status-check.py docs/architecturepack_FLS_v1.0.0_current-state_2026-09-17.html</code> — đỏ khi: heading h2–h4 không có <code>data-st</code> (và không kế thừa); mục <code>approved</code>/<code>locked</code> có hash nội dung ≠ hash lúc ký (<i>stale-approval</i>); <code>locked</code> không ghi vòng; §0.B lệch marker; tag lệch; fan-out > 5; tham chiếu § treo; href treo.",
            "<code>--stamp s7-5=approved</code> — chỉ <b>người đọc</b> chạy; ghi trạng thái + hash + ngày lên đúng heading. Tác giả không tự stamp approved.",
            "<code>--rebuild-index</code> — sinh lại §0.B từ marker (đếm trước, rồi rows).",
            "Nó <b>không</b> sửa chữ dưới thanh xanh cho bạn: sửa xong phải hạ về <code>review</code> bằng <code>--stamp id=review</code>.",
        ])
        + P("Tài liệu này được <b>sinh</b> bằng <code>apgen.py</code> + các mô-đun nội dung (giữ trong scratchpad phiên viết): shell CSS/JS lấy nguyên văn từ AP FPA-T4; mọi bảng bắt buộc <code>colgroup</code> cộng đúng 100 %; lưới §8.3 assert không còn bước UF trống trước khi ghi tệp. Chứng minh checker biết đỏ: sao chép file, đổi một câu trong mục đã <code>approved</code>, chạy lại — phải thấy <code>stale-approval</code>. Bản v1.0.0 chưa có mục approved nên phép thử này chờ chữ ký đầu tiên.")
    ))
    return out
