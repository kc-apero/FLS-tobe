# -*- coding: utf-8 -*-
"""§0 Tổng quan — FLS."""
from apgen import *

HEADER_ROWS = [
    ("Component", "FLS — Financial Ledger System, sub-project <b>ITL</b> (Input Transaction Ledger) của chương trình FIN ERP; repo <code>fcootest/FLS</code> nhánh <code>feat/p2-oracle-parity</code> @ <code>bfeb1a7</code> (2026-09-15)"),
    ("Version", "<b>v1.0.0</b> — bản current-state đầu tiên; ghi cái <b>đang có trong mã</b> tại mốc đo <code>bfeb1a7</code> (đọc sáng 2026-09-17), đề xuất cách ly ở §10"),
    ("Mốc đo &amp; phần chưa fold", "Mã và tài liệu đọc tại <code>bfeb1a7</code>. Trong lúc viết, repo nhận thêm <b>7 commit</b> (<code>5a988c9</code> → <code>b0b40c0</code>, 12:05–15:57 cùng ngày: DD-I11 rà soát ERD, trục thứ hai «khẩu» Ⓐ nạp ⇒ Ⓑ ghép ⇒ Ⓒ sửa trong <code>sinh_ban_do_tang.py</code>, lộ trình audit <code>_AUDIT_ALIGNMENT_ROADMAP.md</code> + <code>_tools/khop_owner.py</code>) và working tree có migration <b>0023</b> chưa commit (5 cột <code>pe_slip · pe_line · pe_loai · pi_slip · pi_line</code> trên <code>fls_pm_line</code>, owner chốt 17/09). <b>Không fold</b> vào bản này — ghi ở Phụ lục A và §9.3; bản v1.1.0 sẽ fold khi chúng được commit."),
    ("Ngày", "2026-09-17"),
    ("Trạng thái", "🟡 <b>DRAFT</b> — chưa mục nào <code>approved</code>; 2 mục <code>review</code> (§7.5, §9.4). Trục build ghi ở §0.3."),
    ("SSOT thắng khi lệch", "<code>fls/db/schema.py</code> (kho) · <code>fls/api/bang_tuyen.py</code> (cửa) · <code>fls/web/tep/*.js</code> (nhãn nút) · <code>docs/ITL/00_MASTER_INDEX.md</code> §3 (quyết định) · <code>01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md</code> (mốc) · <code>02_BA/11_INVARIANTS.md</code> (bất biến)"),
    ("Tiền thân", "<code>docs/ITL/02_BA/Artifacts/ArchitecturePack-Ledger.md</code> v0.3 (AP mặt phẳng Ledger, 25 entity, phần lớn PROPOSED) → cite-only; <code>Ban-do-Kien-truc-7-Tang.html</code> (SVG sinh từ schema) → tái dùng ở §1.1"),
    ("Khuôn", "build-ap §A.1–§A.18 (FIN-ERP authoring-kit) · hình dạng mục theo AP FPA-T4 v2.0.0 (ERD → Process → UserFlows → UI → Logic → Implementation → Quyết định → How-done → Gap → Đề xuất → hậu mục) · Vietnamese, keyword kỹ thuật giữ Anh"),
    ("Changes in v1.0.0", "Bản đầu. Xem §0.2."),
    ("Lịch sử sửa đổi", '<details><summary style="cursor:pointer;color:var(--muted)"><b>0 sửa đổi trước đó</b></summary><p>Chưa có.</p></details>'),
]

def sections():
    out = []
    out.append(S("s0", "§0 Tổng quan &amp; lịch sử phiên bản", st="draft", part="PART 0 · TỔNG QUAN", body=
        P("Mục này để đọc trong 10 phút: hệ là gì, đã xây tới đâu, bản này ghi gì, và đọc tiếp ở đâu.")
        + P("<b>Chú giải: hai trục trạng thái, nhãn bằng chứng</b>")
        + T([("Trục", 22), ("Trả lời", 34), ("Ở đâu trên trang", 44)], [
            ["<b>Thoả thuận</b> (agreement)", "Chữ này đã được ai ký chưa?", "Thanh màu bên trái mỗi heading + chấm trong mục lục (<code>data-st</code>)"],
            ["<b>Build</b>", "Cái này có trong mã hôm nay chưa?", f"Huy hiệu {BUILT} {PARTIAL} {PROPOSED} {SUPERSEDED} cạnh heading và trong §0.3"],
        ])
        + '<div class="stlegend"><span><i style="background:#71717a"></i><code>draft</code> viết xong, chưa có chữ ký</span><span><i style="background:#c026d3"></i><code>review</code> đang đặt câu hỏi, chờ chủ sở hữu</span><span><i style="background:#16a34a"></i><code>approved</code> chủ sở hữu ký (chỉ người đọc mới đặt được)</span><span><i style="background:#1d4ed8;border:2px double #fff;outline:2px solid #1d4ed8"></i><code>locked</code> đã ký và đã soi trên build chạy thật (ghi vòng)</span><span><i style="border:1px dashed #a8a29e;background:none"></i><code>superseded</code> giữ làm lịch sử</span></div>'
        + P("Thanh <b>dày có nền</b> = trạng thái đặt riêng cho mục đó; thanh <b>mảnh không nền</b> = kế thừa từ mục cha. Mọi heading mang <code>data-st-hash</code> (băm nội dung lúc đặt trạng thái) và <code>data-st-on</code> (ngày). Checker: <code>python docs/ap-status-check.py docs/architecturepack_FLS_v1.0.0_current-state_2026-09-17.html</code>.")
        + P("<b>Mốc đo.</b> Mọi câu «hôm nay» trong AP này nghĩa là <b>tại commit <code>bfeb1a7</code></b>, đọc sáng 2026-09-17. Repo đã nhận 7 commit và một migration chưa commit trong cùng ngày (bảng header) — chúng nằm ngoài bản này, không phải bị bỏ quên.")
        + P("<b>Nhãn bằng chứng</b> (theo luật <code>R-A1</code>/<code>R-A2</code> của bộ ITL): <code>[CODE]</code> đọc trong repo · <code>[DOC dd/mm]</code> trích tài liệu ITL kèm ngày đo · <code>[LOG]</code> đọc log chạy thật · <code>[LIVE]</code> truy vấn kho. <b>Kho PostgreSQL không chạy lúc viết</b> (Docker tắt, xem §2.1) nên bản này <b>không có con số [LIVE]</b>; mọi số về dữ liệu là [DOC] với ngày, đúng như tài liệu ITL tự khai.")
    ))

    out.append(S("s0-1", "§0.1 Executive Summary", body=
        P("<b>FLS</b> số hoá luồng kế toán <b>PM → ITL</b>: từ tờ sao kê ngân hàng và lệnh chi trên Google Sheets (<code>P100</code>, <code>PM_Unpivot</code>) tới một <b>sổ chỉ-thêm</b> trong PostgreSQL (<code>fls_itl</code>), rồi hai bề mặt cho 2–3 kế toán: <b>ghép lệnh chi ↔ dòng tiền</b> (tác vụ ①) và <b>sửa 7 ô Final</b> (tác vụ ②). Đích cuối owner gọi tên: «ITL adjust như trong Excel» — 64 cột. Kiểm soát <b>đến từ máy</b>, không từ bước duyệt (<code>QĐ-ITL-27</code>): 3 vai người + 1 vai máy, không leo cấp.")
        + T([("Lằn", 12), ("Đường đi", 48), ("Số nằm ở", 20), ("Tài liệu gốc", 20)], [
            ["<b>Bank</b> (sao kê)", "64 sheet <code>R |</code> của workbook P100 → <b>nhịp chụp</b> mỗi giờ 8–19h → <code>fls_chup*</code> → bản khai cột <code>fls_khai_cot</code> → <code>sao_ke.chuyen</code> → canon 38 vị trí → soát S1–S10 → lớp sổ 7 khối → <code>fls_itl</code>", "<code>fls_chup_dong</code> 7,45 triệu ô thô · <code>fls_itl</code> 8.387 dòng tiền [DOC 11/09]", "BA-05 DD-I10 · BA-06 F04 · QĐ-ITL-105/109/110"],
            ["<b>PM</b> (lệnh chi)", "<code>[Importrange]PM_Unpivot</code> 8 cột → ảnh <code>fls_pm_line</code> (không dòng thô) → <code>pm_join</code> ghép hình A/B/C lúc nạp → <code>fls_pm_link</code>; phần còn lại là việc của người trên <code>F01</code>", "3.772 dòng lệnh / ảnh hiệu lực · 2.262 mối nối [DOC 15/09]", "DEV-09/10 · CR#1 · QĐ-ITL-54/122"],
            ["<b>Cash</b> (quỹ)", "8 nguồn có trong <code>fls_source</code>, 0 ảnh chụp — chưa mở (khuôn 11 cột, <code>GAP-CANON-02</code>)", "—", f"{PROPOSED} §10.2"],
            ["<b>Điểm gặp</b>", "Màn <code>F01</code> hai lằn (LỆNH CHI mặc định · TIỀN) · <code>F02</code> Sổ ITL 52 cột + panel 7 ô · <code>F03</code> Cổng hôm nay · <code>F04</code> Nạp sao kê; đường ra <code>D3</code> ghi an toàn (chạy khô)", "<code>fls_journal</code> 0 · <code>fls_queue_event</code> người 0 [DOC 10/09]", "BA-12/13 · ORC-09"],
        ])
        + P("<b>Bốn trụ kiến trúc (chi tiết <a href='#s1'>§1</a>, <a href='#s6-1'>§6.1</a>)</b>")
        + OL([
            "<b>Sổ chỉ-THÊM, danh tính trước ghép</b> — <code>itl_id</code> cấp bằng SEQUENCE lúc <code>staged</code> rồi đóng băng (<code>INV-I04a</code>); trigger cấm UPDATE/DELETE/TRUNCATE (<code>INV-I03</code>); sửa = bút toán mới, đảo = dòng <code>reversal_of</code>, bỏ ghép = dòng <code>fls_pm_unlink</code> (<code>INV-I08</code>).",
            "<b>Ảnh chụp là chỗ ở của dữ liệu</b> — cửa không đọc Google Sheets sống; mọi phép nạp đi qua <code>fls_chup*</code> + bản khai cột có version (<code>QĐ-ITL-110/105</code>); xem trước và nạp là <b>cùng một hàm</b> trên cùng <code>chup_id</code>.",
            "<b>Máy không bịa</b> — <code>INV-I16</code>: không suy được ⇒ <code>UNMAPPED</code> và có mặt trong hàng chờ; cột <code>*_thyt</code> NULL đúng chỗ máy tự bịa; mọi cú ghi phải có lý do và để vết 7 trường (<code>AUD-1</code>).",
            "<b>Cấu trúc thay kỷ luật</b> — 9 hợp đồng import-linter: <code>fls.api</code> không mở được kết nối (kết nối <b>truyền vào</b>, đường đọc bị PostgreSQL chặn ghi); <code>fls.web</code> không import gì trong <code>fls</code>; <code>oracle</code>/<code>xuat</code> không biết tầng ghi.",
        ])
        + P("<b>Con số neo</b> (ngày đo trong ngoặc — kho không chạy lúc viết nên không có [LIVE])")
        + T([("Đại lượng", 26), ("Số", 44), ("Nguồn đo", 30)], [
            ["Kho", "<b>18</b> bảng + <b>5</b> view = 23 thực thể · 7 tầng · 23 FK · 22 migration · 3 trigger · 1 sequence", "<code>fls/db/schema.py</code> [CODE 17/09]"],
            ["Cửa HTTP", "<b>37</b> tuyến (21 GET · 16 POST · 0 PUT/DELETE) · 15 tuyến ghi · 2 tuyến duy nhất được INSERT <code>fls_itl</code> · 20 mã lỗi", "<code>fls/api/bang_tuyen.py</code> [CODE 17/09]"],
            ["Màn hình", "4 màn sống (F01·F02·F03·F04) + F06 <code>disabled</code> · 13 tệp tĩnh + 3 tệp sinh · <b>18</b> hộp thoại · lưới F02 52 cột · Bảng PM 28 cột", "<code>fls/web/tep/</code> [CODE 17/09]"],
            ["Bộ test", "<b>1.652</b> bài / 123 tệp thu thập được; 634 bài <code>pg</code> cần PostgreSQL thật", "<code>pytest --collect-only</code> [CODE 17/09]"],
            ["Mã", "62 tệp <code>fls/*.py</code> · 51 tool · 9 hợp đồng import-linter xanh", "[CODE 17/09]"],
            ["Sổ thật", "8.387 dòng tiền (8.246 vế <code>PS Có</code>) · 3.772 dòng lệnh · 2.262 mối nối · <code>fls_journal</code> <b>0</b> · <code>fls_queue_event</code> do người <b>0</b>", "ORC-09 §2/§3, MI §10 [DOC 10–15/09]"],
            ["Độ phủ ghép", "phía PM <b>64,3 %</b> (2.427/3.772) · việc thật 1.345 dòng / 698 phiếu · trần cứng phía tiền 47,4 %, phủ trên trần 65,6 %", "<code>do_mau_so</code> [DOC 09/09]"],
            ["Parity với sổ gốc", "69.510/69.510 ô · 23 kỳ · 0 dung sai · 68.915 ô Classifying 100 %", "MI §10, <code>test_parity_*</code> [DOC 08/09]"],
            ["Mốc", "A: 4 đạt · 1 nửa · 1 chưa · B: 1 · 1 · 3 · C: 0 bút toán thật · D: chỉ <code>D3</code>", "<code>kiem_so_song::_cong_moc_a/_b</code> [DOC 10/09]"],
            ["Nhịp chụp", "43 lượt trong log; 16/09 mọi lượt trả mã 1 vì kho không chạy", "<code>.nhip/nhip_chup.log</code> [LOG 17/09]"],
        ])
        + NOTE("<b>Ba điều đảo ấn tượng phải đọc trước.</b> (1) <b>Mọi bảng máy điền thì đầy, mọi bảng người điền thì rỗng</b> (<code>QĐ-ITL-128</code>): 8/23 bảng rỗng đều là bảng người ghi — hai giao diện có mặt nhưng chưa một cú bấm nào của người trên sổ thật. (2) <b>UAT chưa làm được</b> và cái chặn không phải mã: không chỗ chạy ngoài loopback, không đăng nhập (<code>GAP-WEB-01</code>), Docker phải bật tay (<a href='#s9-2'>§9.2</a>). (3) <b>Output cuối chưa tồn tại</b>: bộ xuất 64 cột là 0 dòng mã; 7/7 cột Final đã lưu đủ nên khoảng cách là một bộ xuất chưa viết, không phải dữ liệu (<a href='#s10-1'>§10.1</a>).", warn=True)
    ))

    out.append(S("s0-2", "§0.2 Change log (bản mới nhất) + lịch sử gập", body=
        T([("Version", 16), ("Ngày", 12), ("Highlights", 72)], [
            ["<b>v1.0.0</b> 🟡 DRAFT", "2026-09-17", "Bản đầu của AP FLS theo khuôn build-ap. Fold: <code>schema.py</code> + <code>ERD-TANG.mmd</code> + SVG 7 tầng vào §1; mã 10 gói <code>fls/</code> vào §2/§5/§6; <code>bang_tuyen.py</code> 37 tuyến vào §6.2; nhãn nút <code>man_f0*.js</code> + BA-13 18 hộp thoại vào §3/§4; ORC-09 bốn mốc + DEV-13 bốn chặng vào §8/§11; MI §3 sổ 131 QĐ vào §7; ORC-06 §4 GAP vào §9; DEV-14/15 + ORC-09 §5 «lan man» vào §10. <b>Mới so với bộ tài liệu ITL:</b> §3 Userflows theo cú bấm cho 5 vai (§A.12) · §7 bốn quyết định dạng options + cons + falsifier (§A.15) · §8 «Hoàn thành trông như thế nào» HD-01…HD-24 + lưới đối soát UF × L1–L5 (§A.13) · §10 đề xuất cách ly (§A.11) · thanh trạng thái <code>data-st</code> trên mọi heading + checker (§A.14)."],
        ])
        + '<details><summary style="cursor:pointer;color:var(--muted)"><b>0 sửa đổi trước đó</b></summary><p>Chưa có bản trước. Tiền thân cite-only: <code>ArchitecturePack-Ledger.md</code> v0.3 (2026-09-07) — Phụ lục A.</p></details>'
        + P("Quy ước version: MAJOR khi đảo một quyết định owner / đổi phát biểu bất biến / đổi cây mục; MINOR khi thêm mục; PATCH khi sửa chữ. Mỗi lần sửa là một <b>tệp mới</b>, tệp cũ đóng băng (§A.16); hash từng mục cho phép diff «đã đổi gì» bằng một lệnh.")
    ))

    fi = [
        # (tính năng, lằn, module, build, §, nguồn)
        ["Nhịp chụp mỗi giờ 8–19h (A1) · dọn ảnh 30 ngày (A2) · đường nạp PM (A3/A4)", "Bank·PM", "repo/chup", PARTIAL, "s2-1", "A1 đạt trên kho, chưa đạt vận hành; A2 nửa"],
        ["Ảnh chụp 3 bảng <code>fls_chup*</code>, chỉ-thêm, không PII", "Bank", "repo/chup", BUILT, "s1-2", "QĐ-ITL-110"],
        ["Bản khai cột có version + <code>thu_tu</code>; khai lô tự chứng", "Bank", "repo/khai_cot", BUILT, "s2-2", "DD-I10, QĐ-ITL-113/117"],
        ["Adapter sao kê 64 sheet <code>R |</code> → canon 38, ba đường cân", "Bank", "adapters", BUILT, "s2-2", "8.338/8.338"],
        ["Soát lô S1–S10, ba hạng CHẶN/CỜ/CANH; xem trước = nạp cùng hàm", "Bank", "kiem/api", BUILT, "s5-4", "F04 chặng 2"],
        ["Lớp sổ thuần: Final 7 khối, <code>*_thyt</code>, <code>work_status</code>", "cả hai", "ledger", BUILT, "s5-2", "parity 4.088/4.088"],
        ["Nạp lô một giao dịch, bốn đường cân, một <code>run_id</code>/lô", "Bank", "repo/chay_nap", BUILT, "s2-2", "QĐ-ITL-111"],
        ["Ghép PM lúc nạp: hình A/B/C, dung sai, chia tiền", "PM", "adapters/pm_join", BUILT, "s2-3", "26,79 % không đoán"],
        ["Hàng chờ lằn TIỀN: ứng viên 4 bậc · ghép tay · bỏ ghép · lý do · hoãn · xong · mở lại", "PM", "repo/ghi_tay", BUILT, "s4-2", "0 sự kiện người [DOC]"],
        ["Hàng chờ lằn LỆNH CHI (mặc định): ba rổ, tự chứng, Bảng PM 28 cột", "PM", "repo/lenh_cho", BUILT, "s4-2", "QĐ-ITL-122/124, G1–G5"],
        ["Cửa ghép LÔ chỉ dòng tự chứng, 422 cả lô", "PM", "api/xu_ly", BUILT, "s5-3", "68 dòng (0,9 %)"],
        ["Sổ ITL F02: lưới 52 cột, Quét/Gõ, panel 7 ô, lô lưu 2,5 s, 409 hai người", "cả hai", "web/man_f02", BUILT, "s4-3", "<code>fls_journal</code> = 0"],
        ["Bút toán + nhật ký 7 trường một giao dịch; đảo = thêm dòng", "cả hai", "repo/ghi_tay", BUILT, "s2-4", "INV-I08, AUD-1"],
        ["Cổng hôm nay F03: 3 cổng đo được + 5 khai chưa đo · độ phủ · mẫu số", "—", "web/man_f03", BUILT, "s4-4", "<code>GET /gates</code>"],
        ["Mẫu số B0/B1: bốn ô có tên, tự chứng, TRẦN CỨNG", "PM", "repo/do_mau_so", BUILT, "s5-3", "QĐ-ITL-118/121"],
        ["Thẻ JWT HS256 fail-closed; actor từ thẻ", "—", "api/the", BUILT, "s4-5", "vai chưa dùng phân quyền"],
        ["Kết nối truyền vào; đường đọc chặn ghi ở PostgreSQL; <code>--cho-ghi</code> mặc định tắt", "—", "tools/chay_cua", BUILT, "s6-3", "cổng chung #8"],
        ["Cơ chế ghi an toàn Google Sheets D3 (neo theo khoá, chạy khô, hai khoá)", "ra", "xuat/ghi_o", BUILT, "s2-5", "27 bài; chưa bật"],
        ["Thước chuẩn oracle + parity + cổng số sống 109/109", "—", "oracle/tools", BUILT, "s5-4", "MI §10"],
        ["Bản đồ 7 tầng sinh từ schema, cổng G-ERD-1/2/3", "—", "db", BUILT, "s1-1", "16 bài"],
        ["Đăng nhập Google OIDC + chỗ chạy Tailscale (W1–W6)", "—", "api", PROPOSED, "s10-3", "DEV-14 v0.1"],
        ["Bộ xuất 64 cột D1 · đối chiếu D2 · vòng khép kín D5", "ra", "xuat", PROPOSED, "s10-1", "0 dòng mã"],
        ["F06 Danh mục · Nguồn (<code>GET /catalog</code>)", "—", "web", PROPOSED, "s10-2", "GAP-SPEC-01"],
        ["Lằn quỹ Cash (F05, khuôn 11 cột) · adapters C·D·E·F", "Cash", "adapters", PROPOSED, "s10-2", "ORC-09 §5 «gác»"],
        ["BigQuery làm đích lưu trữ dài hạn", "ra", "—", PROPOSED, "s10-3", "QĐ-ITL-120 chốt, 123 hoãn"],
        ["Chốt kỳ / period signer (<code>period_state = locked</code>)", "—", "—", PROPOSED, "s10-4", "GAP-PLAN-04"],
        ["Ba trạng thái «không cần lệnh chi» · sheet gương 3 tab · 5 cột ALLOCATE · <code>fls_id_counter</code> · view <code>fls_queue_xep_tien</code>", "—", "—", SUPERSEDED, "s7-1", "QĐ-ITL-58/33/65, CR#4"],
    ]
    rows = [[a, b, c, d, f"<a href='#{e}'>§{e[1:].replace('-', '.')}</a>", f] for a, b, c, d, e, f in fi]
    out.append(S("s0-3", "§0.3 FEATURE INDEX — tính năng → lằn → module → build → §", body=
        P(f"Một dòng = một tính năng có thể trỏ tới. Cột <b>Build</b> là trục «tồn tại trong mã hôm nay» (§A.11), độc lập với trục «văn bản đã được ký» (thanh màu trái heading). {BUILT} có trong code và chạy được · {PARTIAL} chạy một phần / thiếu một mặt · {PROPOSED} chỉ có trong §10 · {SUPERSEDED} đã thay, giữ làm lịch sử.")
        + T([("Tính năng", 40), ("Lằn", 8), ("Module", 12), ("Build", 10), ("§", 7), ("Ghi chú", 23)], rows)
    ))

    out.append(S("s0-4", "§0.4 Megamap hệ thống + VOI theo tầng", body=
        P("Một mặt phẳng, một đường số, hai bề mặt người. Mũi tên <b>đậm</b> = luồng số; <b>đứt</b> = vết / cổng / phạm vi. Trục tầng ①–⑦ là trục của kho (<a href='#s1-1'>§1.1</a>); tầng mã (contract → canon → ledger → repo → api → web) là trục khác, ở <a href='#s6-1'>§6.1</a>.")
        + MER("""flowchart TB
  classDef src fill:#f4f4f5,stroke:#71717a,color:#1f2937;
  classDef act fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef store fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef out fill:#fff7ed,stroke:#ea580c,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  classDef prop fill:#fef3c7,stroke:#92400e,color:#1f2937,stroke-dasharray:4 3;

  subgraph N["NGUỒN — Google Sheets kế toán (chỉ ĐỌC)"]
    direction LR
    p100["Workbook P100<br/>64 sheet R | · BankAccountList"]:::src
    pmu["[Importrange]PM_Unpivot<br/>28 cột · 3.772 dòng lệnh"]:::src
    mm["Mapping Master<br/>73 mã hd"]:::src
  end
  subgraph T1["① ẢNH CHỤP — tờ giấy lúc ấy ghi gì"]
    direction LR
    nhip["nhip_chup mỗi giờ 8–19h<br/>hoặc NÚT"]:::act
    chup[("fls_chup · fls_chup_nguon · fls_chup_dong<br/>fls_source · fls_khai_cot · fls_nguon_dai")]:::store
  end
  subgraph T2["② NẠP — dòng nào vào, dòng nào bị loại"]
    direction LR
    f04["F04 Nạp sao kê<br/>khai cột → xem trước → Nhận"]:::out
    nap["adapters → canon → soát S1–S10<br/>→ ledger 7 khối → chay_nap"]:::act
    run[("fls_run · fls_reject")]:::store
  end
  subgraph T3["③ SỔ — append-only"]
    direction LR
    itl[("fls_itl 8.387 dòng · fls_le · fls_mapping_master")]:::store
  end
  subgraph T4["④ GHÉP LỆNH CHI"]
    direction LR
    pmj["pm_join hình A/B/C lúc nạp"]:::act
    link[("fls_pm_line · fls_pm_link · fls_pm_unlink<br/>view fls_moi_noi")]:::store
    f01["F01 Hàng chờ · hai lằn<br/>LỆNH CHI (3 rổ) · TIỀN"]:::out
  end
  subgraph T56["⑤ VIỆC CỦA NGƯỜI · ⑥ SỬA & VẾT"]
    direction LR
    q[("fls_queue_event · views state/weekly/da_xong")]:::store
    f02["F02 Sổ ITL 52 cột<br/>panel 7 ô Final"]:::out
    adj[("fls_adjustment · fls_journal<br/>view fls_sua_tay")]:::store
  end
  subgraph RA["ĐƯỜNG RA"]
    direction LR
    d3["D3 ghi_o an toàn<br/>chạy khô · hai khoá"]:::act
    d1["D1 bộ xuất 64 cột · BigQuery<br/>CHƯA CÓ"]:::prop
  end
  subgraph TX["CẮT NGANG — thẻ · phạm vi · cổng · thước"]
    direction LR
    the["thẻ JWT · actor từ thẻ<br/>--cho-ghi mặc định TẮT"]:::gate
    ora["oracle parity 69.510 ô<br/>kiem_so_song 109/109 · G-ERD · F03"]:::gate
  end

  p100 ==> nhip
  pmu ==> nhip
  mm -.-> itl
  nhip ==> chup
  chup ==> f04
  f04 ==> nap
  nap ==> run
  nap ==> itl
  nap ==> pmj
  pmu -.-> pmj
  pmj ==> link
  itl ==> f01
  link ==> f01
  f01 ==> q
  f01 ==> link
  itl ==> f02
  f02 ==> adj
  adj -.-> ora
  itl -.-> d3
  d3 -.-> d1
  the -.-> f01
  the -.-> f02
  the -.-> f04
  ora -.-> itl
""", "<strong>Hình 0.4</strong> — Megamap theo TẦNG của kho: dữ liệu đi một chiều từ ảnh chụp tới sổ; hai bề mặt F01/F02 chỉ được <i>thêm</i> vào tầng ④⑤⑥; đường ra D1 vẽ nét đứt vì chưa có.")
        + P("<b>VOI theo tầng — đi sâu chỗ nào</b>")
        + T([("Tầng / bề mặt", 30), ("Trả lời câu gì", 40), ("§ đọc", 30)], [
            ["① ẢNH CHỤP · bản khai", "Tờ giấy lúc ấy ghi gì; ai khai cột nào; nhịp có sống không", "<a href='#s1-2'>§1.2</a> · <a href='#s2-1'>§2.1</a> · <a href='#s3-5'>§3.5</a>"],
            ["② NẠP", "Dòng nào vào sổ, dòng nào bị loại và vì sao; lô có bị chặn không", "<a href='#s2-2'>§2.2</a> · <a href='#s4-4'>§4.4</a> · <a href='#s5-4'>§5.4</a>"],
            ["③ SỔ", "Một dòng sổ có gì, danh tính từ đâu, sửa thế nào", "<a href='#s1-3'>§1.3</a> · <a href='#s5-1'>§5.1</a> · <a href='#s5-2'>§5.2</a>"],
            ["④ GHÉP", "Dòng tiền này chi theo lệnh nào; máy ghép được bao nhiêu; trần ở đâu", "<a href='#s2-3'>§2.3</a> · <a href='#s5-3'>§5.3</a> · <a href='#s7-2'>§7.2</a>"],
            ["⑤ VIỆC · ⑥ SỬA", "Người còn phải làm gì; ai đã gõ gì lúc nào vì sao", "<a href='#s3-2'>§3.2</a> · <a href='#s3-3'>§3.3</a> · <a href='#s4-2'>§4.2</a> · <a href='#s4-3'>§4.3</a>"],
            ["CẮT NGANG", "Ai vào được cửa nào; số có khớp sổ gốc không; cổng nào đang đỏ", "<a href='#s4-5'>§4.5</a> · <a href='#s5-5'>§5.5</a> · <a href='#s8-2'>§8.2</a>"],
            ["ĐƯỜNG RA", "Số ra ngoài bằng cách nào; output 64 cột ở đâu", "<a href='#s2-5'>§2.5</a> · <a href='#s10-1'>§10.1</a>"],
        ])
    ))

    out.append(S("s0-B", "§0.B Mục còn nợ quyết định (sinh tự động từ marker)"))
    return out
