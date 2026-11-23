# -*- coding: utf-8 -*-
"""§6 Implementation — FLS."""
from apgen import *

def sections():
    out = []
    out.append(S("s6", "§6 Implementation — tầng mã, cửa, kho, công cụ, migration", st="draft", body=
        P("Repo <code>FLS</code> độc lập (ADR-FLS-01, <code>QĐ-ITL-45</code>): Python 3.12 · psycopg 3 · PostgreSQL 16 trong Docker · pytest · import-linter; <b>không</b> framework web, <b>không</b> ORM, <b>không</b> thư viện lưới. 62 tệp <code>fls/*.py</code> trong 10 gói, 51 tool, 123 tệp test. Mọi con số [CODE 17/09].")
    ))

    out.append(S("s6-1", f"§6.1 Tầng mã &amp; 9 hợp đồng import-linter {BUILT}", body=
        MER("""flowchart TB
  classDef pure fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef io fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef edge fill:#fff7ed,stroke:#ea580c,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  web["fls.web (P6)<br/>phục vụ tệp tĩnh · KHÔNG import gì trong fls"]:::edge
  api["fls.api (P4 đọc · P5 ghi)<br/>bang_tuyen · xu_ly · nap_cua · the · bao · cot_so<br/>kết nối TRUYỀN VÀO, không import fls.db"]:::edge
  repo["fls.repo (16 module)<br/>chay_nap · nap_lo · chup · nhip_chup · ghi_tay · lenh_cho · doc_bao_cao …"]:::io
  db["fls.db<br/>model · schema · render · migration_runner · pg_migrate · pg_verify · kho · triggers"]:::io
  ledger["fls.ledger (thuần)<br/>classifying · final_rule · allocate · build"]:::pure
  canon["fls.canon (thuần)<br/>spec 38 · row · validate · o_loi · le"]:::pure
  contract["fls.contract<br/>ITL-CONTRACT v1.1 · 14 trường"]:::pure
  adapters["fls.adapters<br/>sao_ke · sao_ke_canon · bank · pm_join · mapping_master"]:::pure
  oracle["fls.oracle — THƯỚC<br/>nguon · song · cong_parity · tu_soi · doc_du · ledge_spec"]:::gate
  kiem["fls.kiem<br/>nguon_song L1–L9 · soat_nap S1–S10 · thu_tu_ngay"]:::gate
  xuat["fls.xuat<br/>ghi_o D3 — số phải được truyền vào"]:::edge
  tools["tools/chay_cua.py<br/>chỗ DUY NHẤT mở kết nối"]:::io
  web -.->|"chỉ HTTP"| api
  tools --> api
  tools --> db
  api --> repo
  repo --> db
  repo --> ledger
  repo --> adapters
  repo --> kiem
  ledger --> canon
  adapters --> canon
  canon --> contract
  oracle --> ledger
  oracle -.-x repo
  xuat -.-x repo
  adapters -.-x repo
""", "<strong>Hình 6.1</strong> — Mũi tên một chiều về canon và contract; ba tầng <code>oracle</code>, <code>xuat</code>, <code>adapters</code> bị cấm biết tầng ghi (nét đứt gạch chéo); <code>fls.web</code> chỉ nói chuyện qua HTTP.")
        + T([("#", 4), ("Hợp đồng (<code>.importlinter</code>)", 40), ("Vì sao (nguyên văn ý tệp)", 56)], [
            ["1", "<code>contract · canon · ledger · oracle · adapters · api</code> cấm <code>psycopg</code>", "chỉ <code>fls/repo</code> và <code>fls/db</code> được chạm driver"],
            ["2", "<code>fls.db.model</code> là leaf SSOT, không phụ thuộc gì trong <code>fls</code>", "model import render/schema thì «khai báo một lần» mất nghĩa (vòng phụ thuộc)"],
            ["3", "<code>fls.canon</code> không phụ thuộc <code>ledger/repo/db</code>", "canon là tầng dưới cùng của nghiệp vụ: chuẩn hoá hình dạng"],
            ["4", "<code>fls.ledger</code> không biết <code>repo/db</code>", "hàm thuần canon → payload"],
            ["5", "<code>fls.oracle</code> không biết <code>repo/db</code>", "«một cái thước mà ghi được vào sổ là thước không còn dùng để đo»; dùng lại luật <code>ledger</code> để cả hệ chỉ có một bản luật Final"],
            ["6", "<code>fls.adapters</code> không biết <code>repo/db</code>", "một bộ nạp ghi thẳng vào sổ thì không còn chỗ chặn «0 dòng rơi im lặng»"],
            ["7", "<code>fls.api</code> không biết <code>fls.db</code>", "kết nối truyền vào từ <code>tools/chay_cua.py</code> ⇒ trong cả tầng cửa không có đường nào tự mở được một kết nối ghi — cửa đọc P4 không thể ghi <b>bằng cấu trúc</b>"],
            ["8", "<code>fls.web</code> chỉ được gọi <code>fls.api</code>; cấm mọi tầng dưới", "tầng màn hình dễ bị ép nhất («cho nó đọc thẳng một bảng»); bài <code>test_web_khong_biet_tang_duoi</code> ghim chặt hơn: không import <b>bất cứ gì</b> trong <code>fls</code>"],
            ["9", "<code>fls.xuat</code> không biết <code>db/repo/psycopg</code>", "bộ ghi ra ngoài mà đọc được kho sẽ «tự đi lấy số» — không còn chỗ chặn «xuất một con số không ai duyệt»"],
        ])
        + T([("Gói", 12), ("Tệp", 6), ("Hàm", 6), ("Vai một câu", 56), ("§", 20)], [
            ["<code>contract</code>", "1", "—", "14 trường ITL-CONTRACT, v1.0 đóng băng + v1.1 sống", "<a href='#s5-1'>§5.1</a>"],
            ["<code>canon</code>", "5", "16", "khuôn 38 vị trí, validate LOẠI/CHỜ, ô lỗi, LE", "<a href='#s5-1'>§5.1</a>"],
            ["<code>adapters</code>", "5", "35", "sao kê 64 sheet → canon; PM join 6 hình; Mapping Master 73 mã", "<a href='#s2-2'>§2.2</a> · <a href='#s2-3'>§2.3</a>"],
            ["<code>ledger</code>", "4", "14", "7 khối Final, <code>_thyt</code>, ALLOCATE suy, payload", "<a href='#s5-2'>§5.2</a>"],
            ["<code>repo</code>", "16", "130", "một chỗ ghi <code>fls_itl</code> (<code>itl_repo</code>), một chỗ ghi người (<code>ghi_tay</code>); nạp, chụp, nhịp, dọn, hàng chờ, mẫu số, phạm vi, kho sạch", "<a href='#s2'>§2</a>"],
            ["<code>oracle</code>", "9", "20", "thước chuẩn: nguồn, sống, parity, tự soi, đọc đủ, 64 cột Ledge", "<a href='#s5-4'>§5.4</a>"],
            ["<code>kiem</code>", "4", "32", "L1–L9, S1–S10, thứ tự ngày, bảo hộ phép đo", "<a href='#s5-4'>§5.4</a>"],
            ["<code>api</code>", "7", "111", "37 tuyến, thẻ, vỏ trả lời, bảng cột lưới", "<a href='#s6-2'>§6.2</a>"],
            ["<code>db</code>", "9", "32", "model · schema · render · migration · verify · kho · erd", "<a href='#s1'>§1</a> · <a href='#s6-5'>§6.5</a>"],
            ["<code>web</code>", "1", "5", "bảng tệp tĩnh 17 đường, 3 tệp sinh", "<a href='#s4-1'>§4.1</a>"],
            ["<code>xuat</code>", "1", "12", "ghi an toàn D3", "<a href='#s2-5'>§2.5</a>"],
        ])
    ))

    routes = [
        ["GET", "/ledger", "P4", "dòng sổ + vùng phân bổ 🔒, keyset <code>cursor/limit≤500</code>", "<code>bc.doc_so</code>"],
        ["GET", "/ledger/{itl_id}", "P4", "một dòng + 36 canon + mối nối + đã bỏ; 404 một câu", "<code>bc.doc_mot_dong</code>"],
        ["GET", "/ledger/{itl_id}/fields/{field}", "P4", "«nguồn nói gì» trước khi gõ", "<code>gt.truoc_khi_go</code>"],
        ["POST", "/ledger/{itl_id}/adjust", "<b>P5</b>", "gõ 1/7 trường <code>{field,value,reason,force?}</code>; 409 khác nguồn / kỳ chốt", "<code>gt.ghi_but_toan</code>"],
        ["POST", "/adjustments/{adj_id}/reverse", "<b>P5</b>", "đảo = thêm dòng", "<code>gt.dao_but_toan</code>"],
        ["GET", "/journal?itl_id=", "P4", "nhật ký 7 trường", "<code>bc.doc_nhat_ky</code>"],
        ["GET", "/gates", "P4", "3 cổng đo được + 5 khai chưa đo", "<code>bc.doc_cong</code>"],
        ["GET", "/queue · /queue/summary · /queue/coverage", "P4", "hàng chờ theo tiền tệ; Σ; dòng phủ N %", "<code>bc.doc_hang_cho…</code>"],
        ["GET", "/queue/{itl_id}/pm-candidates", "P4", "ứng viên 4 bậc + tuổi ảnh", "<code>bc.ung_vien_pm</code>"],
        ["POST", "/queue/{itl_id}/match · /unmatch · /reason · /defer · /done · /reopen", "<b>P5</b>", "6 sự kiện hàng chờ; <code>match</code> thân <code>pm_line_ids[]</code>; <code>unmatch</code> bỏ cả chùm", "<code>gt.*</code>"],
        ["GET", "/queue/lenh-cho · /lenh-cho/ro · /lenh-cho/summary", "P4", "lằn LỆNH CHI: dòng lệnh chờ, ba rổ, chân màn theo tiền tệ", "<code>lc.*</code>"],
        ["GET", "/queue/lenh/{pm_line_id} · /itl-candidates", "P4", "một dòng lệnh + <code>tho</code> 28 cột; ứng viên dòng tiền", "<code>lc.doc_mot_dong_lenh · ung_vien_itl</code>"],
        ["GET", "/queue/mau-so · /queue/tu-chung", "P4", "mẫu số B0/B1; danh sách tự chứng + lý do từ chối", "<code>dms.*</code>"],
        ["POST", "/queue/match-lo", "<b>P5</b>", "ghép cả lô, chỉ <code>itl_ids[]</code>, không <code>force</code>, 422 cả lô", "<code>dms.ds_tu_chung + gt.ghep_lenh</code>"],
        ["GET", "/sources · /sources/{id}/khai-cot", "P4", "68 nguồn + <code>khai_version</code>; bản khai + cả dãy version (404/409)", "<code>nap_cua</code>"],
        ["POST", "/sources/{id}/khai-cot · /sources/{id}/thu-tu", "<b>P5</b>", "bản khai version mới; khai chỉ <code>thu_tu</code>", "<code>kc.ghi_khai</code>"],
        ["GET", "/chup · /chup/{id} · /chup/{id}/thu-tu", "P4", "ảnh chụp; một ảnh + dòng; bằng chứng thứ tự ngày (<code>de_xuat</code>)", "<code>chup.* · ttn.*</code>"],
        ["POST", "/chup/{id}/thu-tu", "<b>P5</b>", "khai thứ tự cả lô, chỉ nguồn tự chứng, không mang <code>thu_tu</code>", "<code>nap_cua.khai_thu_tu_lo</code>"],
        ["POST", "/nap/xem-truoc · /nap/lo/xem-truoc", "P4 (đọc thân)", "soát không ghi, chạy trên kết nối chỉ-đọc", "<code>nap_cua._dung_lo · _soat_lo</code>"],
        ["POST", "/nap · /nap/lo", "<b>P5</b> <code>them_vao_so</code>", "<b>hai tuyến duy nhất</b> được INSERT <code>fls_itl</code>; CHẶN ⇒ 422 + biên bản", "<code>nl.nap_lo</code>"],
    ]
    out.append(S("s6-2", f"§6.2 Bề mặt cửa HTTP — 37 tuyến, một bảng khai {BUILT}", body=
        P("Máy HTTP là <code>ThreadingHTTPServer</code> thư viện chuẩn (<code>fls/api/cua.py</code>), không luật nghiệp vụ. <code>BANG_TUYEN</code> (<code>bang_tuyen.py</code>) là <b>một bản khai duy nhất</b>: mỗi tuyến khai method, đường, <code>ghi</code>, bảng chạm, <code>them_vao_so</code>; từ đó sinh bộ định tuyến và cổng tự kiểm lúc dựng máy. Tiền tố <code>/api/fls/v1</code>; mọi tuyến đòi <code>Authorization: Bearer</code>; mọi tuyến nhận <code>?run_id=</code> để thu phạm vi.")
        + T([("Method", 8), ("Đường", 30), ("P", 8), ("Việc", 36), ("Gọi xuống", 18)], routes)
        + P("<b>Đếm:</b> 37 tuyến = 21 GET + 16 POST; 15 tuyến <code>ghi=True</code>; 2 tuyến POST đọc thân không ghi; 0 PUT/DELETE/PATCH (mọi phương thức sửa ⇒ 405). BA-07 v2.8 ghi 35 tuyến — lệch 2 với mã (<a href='#s9-3'>§9.3</a>).")
        + T([("Cổng tự kiểm <code>kiem_bang_tuyen</code>", 40), ("Vi phạm bị từ chối dựng máy", 60)], [
            ["ⓐ ⓐ′ ⓐ‴", "PUT/DELETE/PATCH nhắm <code>fls_itl</code>; tuyến khai ghi <code>fls_itl</code> mà không <code>them_vao_so</code>; <code>them_vao_so</code> phải là POST và ghi cả <code>fls_run</code>"],
            ["ⓑ", "tuyến ghi phải chạm một trong <code>BANG_CO_VET = {fls_journal, fls_queue_event, fls_khai_cot}</code>"],
            ["ⓒ ⓓ ⓔ ⓕ", "tiền tố đúng; chỉ 23 bảng <code>fls_*</code>; không trùng tuyến; phương thức biết"],
            ["ngoài máy", "<code>tools/soi_bang_tuyen.py</code> đối chiếu bản khai với SQL thật (AST); <code>tests/api/test_them_vao_so.py</code> quét cả <code>fls/</code> không có UPDATE/DELETE nhắm <code>fls_itl</code>; <code>test_ba07_phu_het_tuyen</code> đối chiếu BA-07"],
        ])
        + P("<b>Vỏ trả lời</b> (<code>bao.py</code>): <code>{data, error, meta}</code>, <code>meta = {request_id, pham_vi, as_of, data_status flash|reconciled|signed, contract_version, run_id}</code>; <b>tiền ra JSON là chuỗi</b> (không mất chữ số); 20 mã lỗi (<a href='#s5-5'>§5.5</a>); khoá phụ <code>khac · gia_tri_go · bien_ban</code>. Thân ≤ 64 KB, lô ≤ 50.000 dòng, trang ≤ 500, ứng viên ≤ 200.")
    ))

    out.append(S("s6-3", f"§6.3 Kho, env, Docker, NÚT, thẻ — runbook tối thiểu {BUILT}", body=
        T([("Mục", 18), ("Sự thật", 58), ("Nguồn", 24)], [
            ["Kho", "PostgreSQL 16 Docker <code>fls-pg-1</code> (<code>docker-compose.yml</code>), <code>localhost:5433</code>, user/db <code>fls</code>; kho TEST <code>fls_test</code> — <code>dsn_test()</code> NỔ nếu trỏ vào tên kho thật; <code>dung_lai_kho_test()</code> DROP/CREATE + áp di trú (không DELETE — <code>INV-I03</code> chặn; không TRUNCATE — 0015 chặn)", "<code>fls/db/kho.py</code>; lý do: 27/08 1.204 dòng test lọt kho thật"],
            ["Biến môi trường", "<code>PG_DSN</code> (thật) · <code>PG_DSN_TEST</code> · <code>FLS_JWT_SECRET</code> ≥ 32 ký tự (bắt buộc) · <code>FLS_CHO_GHI_SHEET=1</code> (khoá thứ hai của D3) · <code>PYTHONUTF8=1</code>, <code>PYTHONIOENCODING=utf-8</code> (bắt buộc trên Windows — thiếu là công cụ chết ở dòng in)", "<code>the.py</code>, <code>NUT-*.cmd</code>, MI"],
            ["Dựng cửa", "<code>python tools/chay_cua.py [--cong 8088] [--dia-chi 127.0.0.1] [--cho-ghi] [--cho-web] [--actor …] [--the-tam N] [--in-bang-tuyen]</code>; bốn NO lúc dựng: thiếu khoá · kết nối đọc còn ghi được · đường ghi mà chỉ-đọc · bảng tuyến/bảng tệp vi phạm; <code>--cho-web</code> + địa chỉ ngoài loopback ⇒ từ chối", "<code>tools/chay_cua.py</code>, <code>cua.dung_may</code>"],
            ["NÚT owner", "<code>NUT-CHAY-FLS.cmd</code> — chỉ CHỤP (kho → token → <code>nhip_chup.py --that --bo-qua-gio</code> → <code>nut_trang_thai.py</code>); <code>NUT-MO-MAN-HINH.cmd</code> — mở màn UAT trên máy này với <code>--cho-web --cho-ghi</code>; cả hai <b>ASCII thuần</b> (UTF-8 trong .cmd làm hỏng dòng lệnh — lỗi 10/09)", "gốc repo"],
            ["Nhịp", "Task Scheduler <code>'FLS nhip chup'</code> gọi <code>tools/nhip_chup.cmd</code> mỗi giờ, cửa sổ 12 giờ từ 08:00, log <code>.nhip/nhip_chup.log</code>; ba cài đặt điện + Docker tự lên là việc owner", "<code>QĐ-ITL-125/127</code>"],
            ["Thẻ", "JWT HS256 tự viết: <code>alg</code> đúng bằng HS256, <code>exp</code> bắt buộc, <code>sub</code> = actor, <code>vai</code> list nhưng không tuyến nào đọc; ≤ 8.192 byte; mọi lỗi ⇒ 401, chi tiết chỉ vào log; <code>dong_the</code> chỉ ở tools/test (có bài cấm <code>cua.py</code> nhắc tên)", "<code>fls/api/the.py</code>, 19 bài"],
            ["Google Sheets", "chỉ-đọc, qua token <code>gcloud</code> (SA <code>claude-code-access@fpa-t-494007</code>); cửa không bao giờ đọc Sheets sống — chỉ tool nhịp/chụp; D3 ghi qua bộ vận chuyển tiêm vào với hai khoá", "<code>tools/do_hinh_dang.token</code>"],
            ["Sao lưu", "<code>sao_luu/</code>: 3 <code>pg_dump</code> (trước/sau dựng lại 10–11/09) + 8 ảnh sổ JSON có checksum nội dung (<code>tools/sao_luu_kho.py --so-sanh</code> chứng minh sổ dựng lại được)", "[CODE]"],
        ])
    ))

    out.append(S("s6-4", f"§6.4 Công cụ (51) &amp; bộ test (1.652 bài / 123 tệp) {BUILT}", body=
        T([("Nhóm", 16), ("Số", 6), ("Tool tiêu biểu", 78)], [
            ["Nạp · chụp · nhịp", "11", "<code>nhip_chup.py</code> (A1+A2+A3 một lượt) · <code>chup_sao_ke.py</code> · <code>nap_nguon_va_khai.py</code> (nguồn + bản khai v1) · <code>nap_nguon_dai.py</code> (bản khai thứ hai, S10) · <code>nap_mapping_master.py</code> · <code>dung_lai_so.py</code> (dựng lại sổ chỉ từ <code>R |</code>) · <code>nap_lai_sau_khi_don.py</code> · <code>chay_cua.py</code>"],
            ["Đo (Đ-series, B0/B1)", "15", "<code>do_mau_so.py</code> (mẫu số + TRẦN CỨNG) · <code>do_do_phu_ghep.py</code> (gọi <code>ung_vien_pm</code> 7.329 lần) · <code>do_vi_sao_khong_khop.py</code> · <code>do_hinh_dang.py</code> (+ token) · <code>do_chenh_lech.py</code> · <code>do_khoa_ghep.py</code> · <code>do_trong_tai.py</code> · <code>do_bat_bien_ngam.py</code> · <code>do_soat_nap.py</code> · <code>do_danh_muc_nguon.py</code> · <code>tien_do.py</code> · <code>nhin_so.py</code> (cửa sổ đọc chỉ-đọc) · <code>demo_dong.py</code>"],
            ["Kiểm · cổng", "14", "<code>kiem_so_song.py</code> (#13, đếm mốc A/B) · <code>kiem_nguon_song.py</code> (#17) · <code>soat_nap_sao_ke.py</code> · <code>kiem_kho.py</code> · <code>soi_bang_tuyen.py</code> · <code>soi_nhip.py</code> · <code>kiem_ten_truong.py</code> (G1) · <code>kiem_thuyet_minh.py</code> · <code>verify_cua_that.py / verify_cua_ghi.py</code> (#8) · <code>verify_ora_live.py</code> · <code>verify_allocate_that.py</code> · <code>verify_sua_duoc_gi.py</code> · <code>mui_thu_luoi.py</code>"],
            ["Dựng lại · sao lưu · dọn · tài liệu", "8", "<code>dung_lai_bank_transactions.py</code> (8.338/8.338) · <code>sao_luu_kho.py</code> · <code>don_ly_do_sai.py</code> (tự chứng minh trước khi xoá, hai khoá) · <code>dong_bo_so_song.py / va_so_song.py</code> · <code>sinh_ban_do_tang.py</code> · <code>sync_erd_doc.py</code> · <code>lam_bo_asset_thiet_ke.py</code> · <code>nut_trang_thai.py</code>"],
        ])
        + T([("Thư mục test", 16), ("Tệp · bài", 12), ("Canh cái gì (một dòng)", 72)], [
            ["gốc", "10 · 74", "bản đồ 7 tầng không giả được · luật cổng #13 + đếm mốc B (108k sự kiện máy không đóng cổng) · mọi nút có thuyết minh · định dạng VN + kết nối chỉ đọc · gọi tên nguồn 0 dòng · luật bộ hẹn giờ · đếm hết vật liệu kể cả <code>.js</code>"],
            ["<code>adapters/</code>", "6 · 85", "38 vị trí, ba đường, R-ORA-07a/c · đường nạp không còn đọc dòng 1 · Mapping Master None→<code>0</code> · T-JOIN-01…09, 6 hình, dung sai, chia tiền khít · một bản khai trong cả hệ · canh từ vựng PII"],
            ["<code>api/</code>", "17 · 249", "không tuyến nào ghi sổ, mọi ghi để vết · mọi cửa có trong BA-07 · tiền là CHUỖI · bảng cột khớp cửa hai chiều · P4/P5 qua HTTP (401/405/404, phạm vi) · ghép tay/lô · 3 cửa lệnh chi không thêm đường ghi · nạp một nguồn/cả lô, S10 · JWT (alg none, exp, nbf) · chỉ hai tuyến INSERT <code>fls_itl</code>"],
            ["<code>canon/ contract/</code>", "5 · 43", "tập đóng mã lỗi · đúng 38 · 4 cột trùng tên · LOẠI vs CHỜ · không đoán ngày · 14 trường, v1.0 không đổi một chữ"],
            ["<code>db/</code>", "14 · 100", "G-ERD-1/2/3 · INV-I03/I04a, FK run · DD-I10 · test không chạm kho thật · khoá nhiều cột · migration tới đúng schema, checksum · DB khớp khai báo · golden DDL"],
            ["<code>kiem/ ledger/ oracle/</code>", "22 · 237", "L1–L9 mỗi luật có ca ĐỎ · S10 192 phép so · 3 công thức ALLOCATE 2 bẫy · 68.915 ô 100 % · parity 584 dòng / 9.219 dòng 22 kỳ / thước thứ hai · 0 ô ⇒ KHÔNG ĐẠT · 257 ô mất ⇒ ĐỎ · 64 cột đi đâu · G-ORA-LIVE"],
            ["<code>repo/</code>", "29 · 377", "bốn đường, chạy lại không nhân đôi · CHẶN/CỜ lý do đúng dòng · A1/A2 chụp/dọn/nhịp/giờ trống · A3/A4 ảnh PM, Σ mối nối · bản khai · <code>ghi_tay</code>, ghép, bỏ mối nối, đã xong · <b>một chỗ ghi tay</b> (quét mã nguồn) · mẫu số, TRẦN CỨNG, ba rổ · phạm vi · kho sạch · chặn TRUNCATE"],
            ["<code>web/</code>", "19 · 254", "web không biết tầng dưới · bảng tệp · cửa không đổi khi tắt màn · 8 hành vi lưới · lô lưu · panel 38 cột · F01 lằn tiền/lệnh/G5/lô DOM · F04 DOM 33 bài · vòng F01/F02/F04 qua HTTP · JS chạy được (node) · không mã màu gõ tay · một bản mẫu · phủ hết mã lỗi · luật ký hiệu"],
            ["<code>xuat/</code>", "1 · 27", "D3: ô đích giải từ bản sống, chèn dòng ⇒ tự dịch, ghi hai lần 0 ô, cờ duyệt tắt 0 ô, hai khoá"],
        ])
        + P("Fixture: <code>tests/conftest.py</code> dựng lại kho TEST từ <code>DROP DATABASE</code> trước mọi test <code>pg</code> (634 bài cần PostgreSQL thật); <code>tests/fixture/</code> 6 JSON đóng băng (ITL Ledge T3/2026 584 dòng · 9.219 dòng 22 kỳ · 9.845 dòng Classifying · 3.703 PM × 9.992 bank không PII) + <code>tests/golden/ddl.sql</code>. Hai vòng lỗi kho test đã khai: 1.204 dòng test lọt kho thật (27/08) và kho test phình 56.323 dòng làm 5 bài đỏ vì timeout (<code>GAP-KHO-02</code>).")
    ))

    out.append(S("s6-5", f"§6.5 Migration ledger &amp; an toàn ghi {BUILT}", body=
        P("<code>fls/db/migrations/00NN_*.sql</code>, forward-only, tách câu bằng <code>-- &gt;&gt;&gt;</code> (không tách theo <code>;</code> vì plpgsql), mỗi migration một giao dịch, sổ <code>fls_migration</code> + sha256; sửa tệp đã áp ⇒ NỔ; sau <code>ap()</code> tự chạy <code>pg_verify</code>. Lý do tồn tại: <code>CREATE TABLE IF NOT EXISTS</code> «áp THIẾU, báo ĐỦ» (<code>GAP-DB-P0-02</code>, gặp thật 26/08).")
        + T([("#", 5), ("Ngày", 10), ("Làm gì", 60), ("Vì sao / QĐ", 25)], [
            ["0001", "26/08", "baseline: sequence, 9 bảng (<code>fls_itl</code> 49 cột kể cả 5 ALLOCATE), 2 view queue, 2 trigger", "đóng băng, commit <code>01898b9</code>"],
            ["0002–0005", "26/08", "<code>id_payee_thyt/invoice_thyt</code> · <code>itl_id_sheet</code> · <code>le_name</code> nullable · <code>svc_*</code> date → text", "QĐ-ITL-35 cả 7 khối · 357 dòng trùng khoá · GAP-LE-01 · «202412», «thang 5»"],
            ["0006–0009", "27/08", "<code>pm_line_id/pm_hinh</code> → tạo <code>fls_pm_link</code>, chuyển 2.650 mối nối, DROP cột · view <code>fls_queue_xep_tien</code> dựng rồi <b>bỏ</b> sau 1h48", "GAP-JOIN-03 · view không mang phạm vi (CR#4)"],
            ["0010–0011", "27/08", "view <code>fls_sua_tay</code> + 4 index · <code>fls_pm_line</code> ảnh chụp dòng lệnh", "P5 · GAP-API-04"],
            ["0012–0014", "28/08", "DROP 5 cột ALLOCATE · <code>link_id</code>, <code>lan</code>, <code>fls_pm_unlink</code>, <code>fls_adjustment.evt_id</code>, view <code>fls_moi_noi</code> · view <code>fls_da_xong</code>", "QĐ-ITL-64/65 · 69 · 71"],
            ["0015", "07/09", "trigger chặn TRUNCATE", "QĐ-ITL-91 — bịt lỗ INV-I03"],
            ["0016–0019", "07–08/09", "<code>fls_khai_cot</code> + <code>fls_run.khai_id</code> · <code>fls_nguon_dai</code> · <code>fls_chup*</code> + <code>fls_run.chup_id</code> · <code>thu_tu</code> + CHECK đầu tiên", "CR#11 · GAP-KHAI-01 · QĐ-ITL-110 · 113"],
            ["0020–0022", "10–11/09", "<code>fls_reject</code> khoá theo nguồn · <code>fls_pm_line.tho</code> jsonb → json giữ thứ tự", "646 dòng loại mất bản ghi · GAP-CHUP-01"],
        ])
        + T([("Cơ chế an toàn ghi", 30), ("Ở đâu", 34), ("Chứng minh", 36)], [
            ["Sổ chỉ-thêm ba lớp", "trigger UPDATE/DELETE · trigger TRUNCATE · <code>itl_repo</code> chỉ INSERT", "<code>test_invariants_pg</code>, <code>test_chan_truncate_so_pg</code>, <code>test_chi_mot_cho_ghi_tay</code>"],
            ["Kết nối đọc bị PostgreSQL chặn ghi", "<code>noi_chi_doc</code> → <code>SET default_transaction_read_only = on</code>; máy tự kiểm <code>la_chi_doc</code> trước khi mở cổng", "<code>test_noi_chi_doc_KHONG_GHI_DUOC_len_kho_that</code>"],
            ["Kho test tách cứng", "<code>dsn_test()</code> NỔ nếu trỏ kho thật; test không được ghi cứng DSN", "<code>test_khong_ai_tro_lai_kho_that</code>"],
            ["Xem trước = nạp", "cùng hàm <code>_dung_lo</code>, cùng <code>chup_id</code>; xem trước trên kết nối chỉ-đọc", "<code>test_cua_nap_pg</code>"],
            ["Ghi ra ngoài", "D3 hai khoá + biên bản chạy khô; <code>don_ly_do_sai.py</code> tự chứng minh rồi mới xoá, có hoàn tác", "27 + 8 bài"],
            ["Schema ↔ kho", "<code>pg_verify</code> so cột/null/FK/PK/UNIQUE/CHECK (không so index, trigger, default)", "<code>test_pg_verify</code>; lệch trigger 0015 không có cổng (<a href='#s9-1'>§9.1</a>)"],
        ])
    ))
    return out
