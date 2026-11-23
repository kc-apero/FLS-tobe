# -*- coding: utf-8 -*-
"""§7 Quyết định — FLS."""
from apgen import *

REJ = '<span class="badge tbd">REJECTED</span>'
DEC = lambda d: f'<span class="badge new">DECIDED · {d}</span>'
KEEP = '<span class="badge keep">HIỆN TRẠNG</span>'
OPEN = '<span class="badge tbd">CHỜ OWNER</span>'

def sections():
    out = []
    out.append(S("s7", "§7 Quyết định — sổ đã chốt và các lựa chọn còn mở", st="draft", part="PART C · QUẢN TRỊ — QUYẾT ĐỊNH · CHẤP NHẬN · KHOẢNG TRỐNG · ĐỀ XUẤT", body=
        P("Sổ quyết định gốc là <code>docs/ITL/00_MASTER_INDEX.md</code> §3: <b>131</b> <code>QĐ-ITL</code> + 2 <code>QĐ-owner</code> + <code>AUD-12</code> + 11 CR, mỗi dòng có ngày, một dòng và phương án bị loại. Mục này (§7.1) trích 16 quyết định kiến trúc nhất, rồi (§7.2–§7.5) viết lại <b>bốn</b> quyết định lớn theo khuôn §A.15: ≥2 phương án thật, cons trên cả phương án thắng, một câu «điều gì sẽ đảo».")
    ))

    out.append(S("s7-1", "§7.1 Sổ quyết định đã chốt — 16 dòng kiến trúc", body=
        T([("QĐ", 9), ("Ngày", 8), ("Một dòng", 50), ("Loại bỏ / hệ quả", 33)], [
            ["<b>13</b>", "19/08", "Đảo VALUE-FIRST — code hoá tới ITL Ledge", "loại «hoãn code L0–L2» (07/08)"],
            ["<b>15</b>", "19/08", "Google Sheets thay bằng màn hình mới, chuyển dần", "đóng GAP-ITL-02"],
            ["<b>16</b>", "19/08", "Bút toán điều chỉnh <b>không thêm bước duyệt</b>, bắt buộc nhật ký", "SoD-1 không áp dụng; <code>approved</code> bỏ khỏi SM-I02/I03"],
            ["<b>27</b>", "22/08", "Kiểm soát đến từ máy: 3 vai người + 1 máy, một hàng chờ, không leo thang", "khai tử AC-06/AC-08/RP-I11 (<a href='#s7-4'>§7.4</a>)"],
            ["<b>30</b>", "22/08", "<code>itl_id</code> cấp khi vào sổ rồi đóng băng, không cắt theo năm", "đóng GAP-ITL-27 (<a href='#s7-3'>§7.3</a>)"],
            ["<b>34</b>", "24/08", "Không đụng sheet hiện có, không động file kế toán", "hệ quả: sổ cũ không nhanh hơn"],
            ["<b>35</b>", "24/08", "Hai đầu ra song song: Final parity 100 % + cột <code>*_thyt</code> không vào parity", "—"],
            ["<b>38</b>", "24/08", "Đầu ra: PostgreSQL chính · BQ bản sao · APP thay Sheets", "về QĐ-VOI-04 («BQ không chịu OLTP 64–77 s»); sau đó QĐ-120/123 (<a href='#s7-5'>§7.5</a>)"],
            ["<b>42</b>", "24/08", "Đóng băng ITL-CONTRACT = 14 trường theo TÊN; khối 6–7 ngoài hợp đồng", "«13 trường theo vị trí» SUPERSEDED"],
            ["<b>45</b>", "24/08", "FLS code + DB độc lập với FPA/P100; chỉ đọc <code>fps_*</code>", "loại port vào FPA-T4 như A-CCR"],
            ["<b>48</b>", "25/08", "MAPPING là việc của FLS, không đẩy lên FPS", "lật FLS-Process chặng 2"],
            ["<b>54</b>", "27/08", "Ghép bank ↔ DÒNG lệnh, không tách dòng bank; hình A…F", "lật 3 tiền đề DEV-10 v0.1 (T-JOIN-03 là cách không làm)"],
            ["<b>58</b>", "27/08", "Bỏ hẳn trạng thái «không cần lệnh chi»; chỉ <code>ok / UNMAPPED</code>", "QĐ-28 SUPERSEDED; máy dán nhãn ấy là máy tự đặt quy định"],
            ["<b>60</b>", "27/08", "P5 cửa GHI: sửa là THÊM bút toán (<code>/adjust · /reverse · /reason · /defer</code>)", "CR#5"],
            ["<b>90</b>", "07/09", "Mở phạm vi: FLS cầm hai màn nhập Bank Transaction + Cash Ledger (CR#10)", "lật QĐ-23 «vĩnh viễn» sau 16 ngày"],
            ["<b>105 · 109 · 110</b>", "07–08/09", "Khuôn nhận là sao kê thô 6 trường; F04 đọc vùng CHUẨN, không thay phép chuẩn hoá; đọc qua ảnh chụp trong kho", "loại «màn dán»; Ctrl+V ở lại Sheets"],
            ["<b>122 · 124</b>", "09/09", "Chiều đo: Trans map vào PM; màn ghép hỏi từ phía lệnh chi (lằn mặc định)", "mọi độ phủ 27/08–09/09 «đo sai phía» (<a href='#s7-2'>§7.2</a>)"],
        ])
        + P("Đọc sổ đầy đủ: MI §3 (mỗi dòng có cột «Loại bỏ»). Quy ước giữ bia: câu cũ gạch ngang nhưng không xoá, nên một con số có nhiều giá trị theo ngày — AP này ghi giá trị mới nhất kèm ngày.")
    ))

    out.append(S("s7-2", "§7.2 QĐ-A · Chiều đo độ phủ ghép — phía tiền, phía lệnh chi, hay cả hai", body=
        P("Chốt <b>2026-09-09</b> (<code>QĐ-ITL-122</code>, owner nguyên văn: «Trans map vào PM; không cần question các Trans không được map»). Ba cách đo, ba câu hỏi khác nhau.")
        + T([("Phương án", 18), ("Được", 30), ("Mất", 30), ("Kết luận", 22)], [
            ["<b>A · Đo phía TIỀN</b> — mẫu số 8.246 dòng <code>PS Có</code>", "hỏi được «tiền này đi đâu» cho từng đồng; đúng cho kiểm toán số dư", "10.030 dòng tiền so với 3.772 dòng lệnh là <i>đúng như thiết kế</i> ⇒ độ phủ 31,1 % «mãi mãi trông như thất bại»; 7.682 dòng hàng chờ, 7.329 cú bấm; hỏi câu owner nói không cần hỏi", REJ + " làm chiều mặc định; giữ lằn TIỀN vì là đường duy nhất để ghi lý do/hoãn/bỏ ghép"],
            ["<b>B · Đo phía LỆNH CHI</b> — mẫu số 3.772 dòng lệnh ảnh hiệu lực", "câu của việc: «lệnh chi nào chưa tìm được tiền» — 1.345 dòng / 698 phiếu; 69 dòng phủ 90 % tiền (vs 799); ba rổ tách được việc thật khỏi việc máy và việc không bao giờ", "<b>Mất:</b> không thấy dòng tiền RA không có lệnh (UC-KT-12 phải khai tử — <code>QĐ-ITL-131</code>); mẫu số đổi theo mỗi ảnh PM; <code>fls_queue_event</code> chỉ treo vào <code>itl_id</code> ⇒ lằn này chưa có lý do/hoãn/xong; tất cả độ phủ cũ phải đo lại", DEC("2026-09-09")],
            ["<b>C · Trần cứng</b> — <code>toi_da = da_noi + ranh</code>, phủ trên trần", "nói đúng phần việc đã làm (65,6 %) thay 31,1 %; không hứa 100 % trên <code>PS Có</code>", "chỉ là tỷ lệ kích thước hai tập (tan khi đo phía PM); vẫn cần A làm mẫu số", KEEP + " làm con số phụ, không ra quyết định"],
        ], rowcls=["", "recommended", ""])
        + P("<b>Điều gì sẽ đảo quyết định này:</b> nếu owner cần giải trình <i>từng dòng tiền RA không có lệnh</i> (UC-KT-12 sống lại) thì chiều A trở thành câu chính và cần một bảng nhãn «vốn không cần lệnh» — thứ <code>QĐ-ITL-56/58</code> đã cấm máy tự dán.")
    ))

    out.append(S("s7-3", "§7.3 QĐ-B · Danh tính dòng sổ — cấp trước ghép, sau ghép, hay dùng khoá nội dung", body=
        P("Chốt <b>2026-08-22/24</b> (<code>QĐ-ITL-30</code>, <code>QĐ-ITL-43</code>, <code>INV-I04a/b</code>). Cú lật lõi so với AS-IS.")
        + T([("Phương án", 18), ("Được", 30), ("Mất", 30), ("Kết luận", 22)], [
            ["<b>A · AS-IS</b> — <code>itl_id = 'ITL#' &amp; No</code>, <code>No = ROW()</code> trên bảng đã SORT, cấp SAU mapping", "không cần sequence; khớp thói quen sheet", "nhập lùi ngày ⇒ đánh số lại toàn bộ (gốc 1.356 <code>FALSE</code> ở AUDIT); <code>No</code> rỗng khi thiếu tài khoản ⇒ <code>ITL#</code> mất khoá; dòng UNMAPPED không có danh tính", REJ + " — giữ <code>itl_id_sheet</code> chỉ để đối soát"],
            ["<b>B · SEQUENCE lúc <code>staged</code></b>, đóng băng, trước mapping", "danh tính bất động với mọi sửa/sắp lại; <code>unmapped</code> vẫn có khoá; trigger chặn đổi; một sequence cho mọi PK", "<b>Mất:</b> không mang nghĩa nghiệp vụ (không đọc ra ngày/kỳ từ id); cần khoá <i>thứ hai</i> để chống trùng nội dung; số cũ trên sheet không suy được từ id mới (phải lưu <code>itl_id_sheet</code>)", DEC("2026-08-22")],
            ["<b>C · <code>content_key</code> làm danh tính</b> — sha256 của 7 thành phần", "chống nạp trùng bằng cấu trúc (<code>ON CONFLICT DO NOTHING</code>); tái lập được từ nguồn", "357 dòng (3,7 %) trùng khoá nội dung + 105 dòng không số chứng từ ⇒ cần <code>seq_trung</code>; đổi thuật toán hash là đổi danh tính", REJ + " làm danh tính; " + KEEP + " làm khoá <b>đối sánh</b> UNIQUE (<code>INV-I04b</code>)"],
        ], rowcls=["", "recommended", ""])
        + P("<b>Điều gì sẽ đảo quyết định này:</b> nếu FLS phải cấp lại toàn bộ sổ từ một kho khác (BigQuery, <a href='#s7-5'>§7.5</a>) mà không mang sequence theo, danh tính B mất tính bất động và C trở thành danh tính duy nhất tái lập được — khi đó phải giải quyết 357 dòng trùng bằng luật, không bằng <code>seq_trung</code>.")
    ))

    out.append(S("s7-4", "§7.4 QĐ-C · Kiểm soát: bước duyệt của người, máy + nhật ký, hay hậu kiểm định kỳ", body=
        P("Chốt <b>2026-08-19 → 22</b> (<code>QĐ-ITL-16</code>, <code>QĐ-ITL-27</code>). Lý do là <b>vận hành</b>, không phải thiết kế: luồng PM → ITL chỉ có 2–3 kế toán; kế toán trưởng và CFO-COO hầu như không tham gia.")
        + T([("Phương án", 18), ("Được", 30), ("Mất", 30), ("Kết luận", 22)], [
            ["<b>A · Maker–checker</b> (10 vai, SoD-1, <code>approved</code> trong SM-I02/I03)", "tiền kiểm; chuẩn kiểm toán", "bước duyệt «leo vào chỗ trống» — trông như kiểm soát mà không ai đứng đó; chậm hơn Gsheet đang dùng", REJ + " — §1–§2 BA-04 giữ làm biên bản"],
            ["<b>B · MÁY là chỗ kiểm soát duy nhất</b> + nhật ký 7 trường bắt buộc", "7 phép chặn có bằng chứng (trigger, <code>FLS-UNMAPPED-HIDDEN</code>, 73 mã, <code>YYYYMM</code>, kỳ chốt, 409 khác nguồn, <code>--cho-ghi</code> tắt); người gõ là người chốt y như Gsheet; nhật ký để việc sống sót khi một người rời đi (rủi ro số 1)", "<b>Mất:</b> không có người soi nhật ký theo nhịp (<code>RP-I11</code> khai tử) ⇒ <code>AUD-1</code> là hậu kiểm không ai đọc; máy <b>không chặn được</b> ba thứ: hai người sửa một ô (<code>GAP-SCR-09</code>), ba danh sách suy không ép (<code>INV-I18</code>), danh mục rỗng thì máy không biết (<code>INV-I17</code>); thước «có ai đọc bảng việc không» (<code>US-KT-045</code>) chưa dựng", DEC("2026-08-22")],
            ["<b>C · Hậu kiểm định kỳ</b> — một người soi <code>fls_journal</code> hàng tuần", "rẻ; giữ được tiền lệ Gsheet version history", "cần một người nhận (<code>GAP-ITL-24</code> chưa ai); kém an toàn hơn Gsheet nếu không ai soi", REJ + " — không có người; giữ <code>fls_queue_reason_weekly</code> làm thước nếu sau này có"],
        ], rowcls=["", "recommended", ""])
        + P("<b>Điều gì sẽ đảo quyết định này:</b> nếu số kế toán vận hành lên ≥5 hoặc kiểm toán ngoài đòi SoD, bước duyệt có người đứng và A quay lại; hoặc nếu phép đếm <code>US-KT-045</code> (4 tuần không ai gõ = cổng chết) được dựng và lần đầu đỏ, cần một vai soi thật.")
    ))

    out.append(S("s7-5", "§7.5 QĐ-D · Đích lưu trữ dài hạn và đích output — Sheets, PostgreSQL, hay BigQuery", st="review", body=
        P("<b>Chưa chốt hết — đang REVIEW.</b> Owner đã trả lời một nửa (<code>QĐ-ITL-120</code>, 09/09: «BQ sẽ là nơi lưu trữ toàn bộ dữ liệu sau này», không động vào trang tính kế toán) rồi <b>hoãn</b> (<code>QĐ-ITL-123</code>). Ba điều chưa có câu trả lời: «sau này» là khi nào; hai bất biến PostgreSQL cưỡng chế (<code>INV-I08</code>, bút toán + vết một nhịp) có mở lại không; FLS hôm nay 0 dòng mã BigQuery.")
        + T([("Phương án", 18), ("Được", 30), ("Mất", 30), ("Kết luận", 22)], [
            ["<b>A · Ghi ngược ITL adjust lên Google Sheets</b> (đích cũ của <code>QĐ-ITL-116</code>, kể cả A-CCR)", "kế toán thấy output ở chỗ quen; D3 đã có cơ chế an toàn", "địa chỉ dịch khi owner co-edit (đã cắn thật); không giao dịch, không khoá; «không động vào trang tính kế toán» (owner 09/09)", REJ + " làm đích lâu dài; D3 giữ làm lằn chở"],
            ["<b>B · PostgreSQL là kho vận hành</b> + bộ xuất 64 cột đọc từ nó", "giữ nguyên hai bất biến đã đóng; mọi cổng hôm nay đo trên nó; xuất là việc <i>thuần đọc</i>", "<b>Mất:</b> không phải đích lưu trữ owner chốt; FPA-T4 (consumer) đọc BQ nên vẫn cần một cú sao chép; kho nằm trên máy làm việc (Docker tắt là kho tắt)", KEEP + " — mọi việc D1/D2/D5 làm trên B trước"],
            ["<b>C · BigQuery làm kho vận hành + lưu trữ</b>", "một kho cho cả FLS và FPA-T4; đúng câu owner", "BQ không có <code>INV-I08</code> cùng ngữ nghĩa, có đệm chèn-luồng ⇒ mở lại hai bất biến; QĐ-VOI-04 đã đo «BQ không chịu OLTP 64–77 s»; 0 dòng mã", OPEN + " — hoãn (<code>QĐ-ITL-123</code>)"],
            ["<b>D · Lai</b> — PostgreSQL vận hành, BigQuery bản sao chỉ-đọc theo nhịp (đúng <code>QĐ-ITL-38</code>)", "giữ bất biến ở PG; FPA-T4 đọc BQ; bộ xuất 64 cột và bản sao BQ dùng chung một phép đọc", "<b>Mất:</b> hai kho phải khớp (cần một cổng đối soát PG↔BQ); trễ theo nhịp; thêm một đường ra phải kiểm «không tự đi lấy số» (hợp đồng 9)", '<span class="badge new">RECOMMENDED — chờ owner</span>'],
        ], rowcls=["", "", "", "recommended"])
        + P("<b>Điều gì sẽ đảo quyết định này:</b> nếu owner chốt «sau này» là <i>ngay</i> (chuyển kho vận hành), D bị loại và phải thiết kế lại <code>INV-I08</code> trên BQ trước khi viết một dòng xuất; ngược lại nếu FPA-T4 chấp nhận đọc PostgreSQL qua cửa, C và D đều thừa.")
        + P("Câu hỏi owner đi kèm ở <a href='#s9-4'>§9.4</a>.")
    ))
    return out
