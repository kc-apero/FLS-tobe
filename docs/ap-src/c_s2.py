# -*- coding: utf-8 -*-
"""§2 ProcessDescription — FLS."""
from apgen import *

def sections():
    out = []
    out.append(S("s2", "§2 ProcessDescription — từ tờ sao kê tới sổ, và đường ra", st="draft", body=
        P("FLS có <b>một</b> đường số đi một chiều và <b>hai</b> bề mặt người chạm vào nó. Đường số: tờ Google Sheets kế toán → <b>ảnh chụp</b> (①) → <b>nạp lô</b> (②) → <b>sổ</b> <code>fls_itl</code> (③) → <b>ghép lệnh chi</b> (④) → hàng chờ việc (⑤) và bút toán sửa (⑥). Hai bề mặt người: màn <code>F01</code> (ghép) và <code>F02</code> (sửa 7 ô). Đường ra duy nhất đã có là cơ chế ghi an toàn <code>D3</code>; bộ xuất 64 cột <code>D1</code> chưa tồn tại (<a href='#s10-1'>§10.1</a>).")
        + P("Mọi bước đều tuân một nguyên tắc lặp lại ở mọi tầng mã: <i>«0 dòng rơi im lặng»</i> (cổng chung #3, <code>fls/repo/chay_nap.py</code>), <i>«đo được 0 thứ ⇒ KHÔNG ĐẠT»</i> (<code>fls/kiem/nguon_song.py</code>), <i>«không mặc định im lặng»</i> (<code>INV-I16</code>). Sơ đồ tổng ở <a href='#s0-4'>Hình 0.4</a>.")
    ))

    # 2.1
    out.append(S("s2-1", f"§2.1 Nhịp chụp và ảnh chụp — cổng <code>A1</code> · <code>A2</code> · <code>A3</code> {PARTIAL}", body=
        P("<b>Ảnh chụp</b> (<code>QĐ-ITL-110</code>) là «tờ giấy lúc ấy ghi gì»: FLS không đọc Google Sheets lúc nạp mà đọc một bản sao đóng băng trong kho. Ba lằn <code>Bank</code> · <code>Cash</code> · <code>PM</code>; <code>Cash</code> chưa mở (0 ảnh).")
        + MER("""flowchart LR
  classDef src fill:#f4f4f5,stroke:#71717a,color:#1f2937;
  classDef act fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef store fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  sched["Task Scheduler Windows<br/>'FLS nhip chup' mỗi giờ"]:::src
  nut["NÚT NUT-CHAY-FLS.cmd<br/>owner bấm tay"]:::src
  nhip["tools/nhip_chup.py --that<br/>can_chup(lan) → lý do"]:::act
  sheets["Workbook P100 · 64 sheet R |<br/>[Importrange]PM_Unpivot"]:::src
  chup[("fls_chup · fls_chup_nguon · fls_chup_dong<br/>chỉ-THÊM · actor nhip@fls")]:::store
  pm[("fls_pm_line<br/>run_id = ảnh PM")]:::store
  don["don_chup: xoá ảnh >30 ngày<br/>KHÔNG fls_run trỏ tới"]:::gate
  soi["soi_nhip.py · do_gio_trong<br/>đếm giờ trống 8h–19h"]:::gate
  sched --> nhip
  nut --> nhip
  sheets --> nhip
  nhip -->|"lằn Bank"| chup
  nhip -->|"lằn PM (A3)"| pm
  nhip --> don
  chup -.-> soi
""", "<strong>Hình 2.1</strong> — Nhịp chụp: hai lối kích (bộ hẹn giờ · NÚT), một hàm quyết định có chụp hay không kèm lý do, ba bảng chỉ-thêm, và hai phép soi độc lập.")
        + T([("Bước", 16), ("Cơ chế", 40), ("Định danh · vết", 20), ("Cổng", 24)], [
            ["Quyết định chụp", "<code>nhip_chup.can_chup(conn, lan)</code>: trong khung <b>8h–19h giờ VN</b> (<code>QĐ-ITL-114</code>) và giờ đồng hồ này chưa có ảnh; trả <code>(bool, lý do)</code>, không tự chụp", "<code>actor</code> = <code>nhip@fls</code> (hẹn giờ) hoặc <code>nhip@fls(tay)</code> (gõ tay) — hai actor tách để cổng không tự bấm cho mình xanh", "<code>A1</code>: ≥2 ảnh do nhịp, ≥2 giờ khác nhau"],
            ["Ghi ảnh lằn Bank", "<code>chup.ghi_chup</code> một giao dịch: 1 dòng <code>fls_chup</code> (spreadsheet, lằn, giây), N dòng <code>fls_chup_nguon</code> (nguồn × <code>khai_version</code> đã dùng), M dòng <code>fls_chup_dong</code> (ô thô jsonb). <code>_soi_o</code> cấm trường PII (<code>Description</code>, khối nhân sự 9–14)", "<code>chup_id</code>; ảnh cũ không bao giờ đổi một ô (đã chứng minh)", "3,2–5,1 giây / 60–64 nguồn; nguồn ra 0 dòng được <b>gọi tên</b> (<code>khai_rong()</code>)"],
            ["Ghi ảnh lằn PM", "<code>ghi_chup_pm</code> chỉ ghi dấu xuất xứ; dòng lệnh chi vào <code>fls_pm_line</code> với <code>run_id</code> = ảnh. Ảnh PM <b>không lưu dòng thô</b> (<code>GAP-CHUP-01</code>) ⇒ thêm cột phải đợi cú chụp sau", "<code>fls_pm_line(run_id, pm_line_id)</code>; <code>anh_pm_hieu_luc</code> = ảnh có <code>max(read_at)</code>", "<code>A3</code>: ≥2 <code>run_id</code> khác nhau · <code>A4</code>: nạp lại cùng tệp ⇒ 0 dòng trùng"],
            ["Dọn ảnh", "<code>don_chup.don_anh_chup</code>: giữ vĩnh viễn ảnh có <code>fls_run.chup_id</code> trỏ tới; xoá ảnh >30 ngày không ai dùng (<code>QĐ-ITL-115</code>). Mọi câu <code>DELETE</code> phải mang hàng rào <code>NOT EXISTS fls_run</code> — có cổng nguồn canh", "biên bản «giữ vì ĐÃ NẠP · giữ vì CÒN MỚI · xoá N»", "<code>A2</code>: vết không đứt; vế «xoá >30 ngày» đang xanh trên tập rỗng ⇒ <b>chưa đo</b>"],
            ["Soi nhịp", "<code>tools/soi_nhip.py</code> đọc bản ghi của <b>chính bộ hẹn giờ</b> Windows (mã 4 = lượt hụt / máy ngủ / pin); <code>nhip_chup.do_gio_trong</code> đếm giờ khung không có ảnh <b>từ kho</b>, chạy trên mọi máy", "cửa sổ đếm theo giờ khung để cổng hồi phục được", "đo 10/09: Bank thiếu 3 giờ · PM thiếu 5 giờ"],
        ])
        + NOTE("<b>Trạng thái thật lúc viết (log <code>.nhip/nhip_chup.log</code>, 43 lượt, đọc 2026-09-17):</b> nhịp đăng ký 09/09 17:40 và chạy được tới 10/09; <b>không một lượt nào</b> từ 11/09 tới 15/09 10:10 (máy ngủ, <code>WakeToRun=False</code> — <code>QĐ-ITL-127</code>); 15/09 chạy lại xen kẽ; <b>16/09 cả bốn lượt có mã đều trả 1</b> vì kho PostgreSQL không chạy (<code>ConnectionTimeout</code> port 5433). Đúng hình «nhịp đổ trong im lặng khi Docker tắt» mà tệp mốc đã dự báo; ba cài đặt điện + Docker tự khởi động là việc của owner (<a href='#s11-2'>§11.2</a>).", warn=True)
    ))

    # 2.2
    out.append(S("s2-2", f"§2.2 Nạp một lô — adapters → canon → soát → lớp sổ → kho {BUILT}", body=
        P("Một lần nạp là <b>một giao dịch</b> đi qua năm tầng mã, mỗi tầng chỉ biết tầng dưới (<a href='#s6-1'>§6.1</a>). Đầu vào là một ảnh chụp (hoặc tờ RAW cho lằn cũ), đầu ra là các dòng <code>fls_itl</code> mang đủ lineage, hoặc dòng <code>fls_reject</code> mang lý do có tên.")
        + MER("""flowchart TB
  classDef src fill:#f4f4f5,stroke:#71717a,color:#1f2937;
  classDef act fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef store fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  anh[("fls_chup_dong<br/>ô thô theo nguồn")]:::store
  khai[("fls_khai_cot<br/>bản khai 6 trường + thu_tu")]:::store
  ad["adapters.sao_ke.chuyen<br/>→ khuôn Bank Transactions 10 cột<br/>→ sao_ke_canon.nap → canon 38"]:::act
  soat["kiem.soat_nap S1–S10<br/>CHẶN · CỜ · CANH"]:::gate
  led["ledger: validate → khoi_tu_canon<br/>→ dung_khoi (7 khối) → dung_dong"]:::act
  chay["repo.chay_nap.chay<br/>bốn đường cân · Σ mối nối · MỘT giao dịch"]:::act
  itl[("fls_itl · fls_le · fls_reject<br/>fls_run(run_id, chup_id)")]:::store
  pm[("fls_pm_link · fls_pm_line")]:::store
  q[("fls_queue_event<br/>lý do đúng dòng (CỜ)")]:::store
  anh --> ad
  khai --> ad
  ad --> soat
  soat -->|"CHẶN ⇒ 422 FLS-SOAT-CHAN, 0 dòng ghi"| stop["dừng"]:::gate
  soat -->|"CỜ / CANH"| led
  led --> chay
  chay --> itl
  chay --> pm
  chay --> q
""", "<strong>Hình 2.2</strong> — Nạp lô: hạng CHẶN dừng cả lô trước khi ghi; hạng CỜ vẫn ghi nhưng chỉ đích danh dòng vào hàng chờ kèm lý do của đúng dòng ấy.")
        + T([("Tầng", 14), ("Hàm chính", 26), ("Vào → Ra", 30), ("Luật / cổng", 30)], [
            ["Bản khai cột", "<code>khai_cot.ghi_khai</code> · <code>doc_khai</code>", "6 trường (<code>Date</code>…<code>Reference number</code>) + <code>thu_tu</code> chỉ trên dòng <code>Date</code> → <code>(source_id, version)</code>, chỉ-THÊM", "đủ 6 hoặc không ghi; <code>hieu_luc_tu</code> do kho đặt; 404 <code>FLS-NGUON-LA</code> ≠ 409 <code>FLS-KHAI-KHONG-CO</code>; bản khai khoá theo <b>tên sheet</b> ⇒ đổi tên là lằn đổ"],
            ["Adapter", "<code>sao_ke.chuyen</code> · <code>sao_ke_canon.nap</code> · <code>bank.nap</code> (lằn cũ) · <code>pm_join.loc_tho</code>", "ô thô → khuôn <code>Bank Transactions</code> 10 cột → canon 38 vị trí (32 vị trí trống có chủ ý) ; <code>Num</code> = thứ tự xuất hiện của mã", "ba đường <code>ra + rỗng + lỗi = vào</code>; không đoán vị trí (<code>QĐ-ITL-105</code>); không đọc <code>Description</code> (<code>QĐ-ITL-92</code>)"],
            ["Soát lô", "<code>nap_cua._soat</code> → <code>soat_nap.S1…S10</code>", "một lô → danh sách luật đỏ có hạng; xem trước là tuyến riêng <code>POST /nap/lo/xem-truoc</code>", "<code>S1</code> ba đường cân (CHẶN) · <code>S10</code> hai bản khai cùng cột (CHẶN) · <code>S2–S4, S7, S8</code> (CỜ) · <code>S5, S6</code> (CANH); <code>R-A5</code> không nới cổng"],
            ["Lớp sổ (thuần)", "<code>validate</code> · <code>classifying.khoi_tu_canon</code> · <code>final_rule.dung_khoi</code> · <code>build.dung_dong</code>", "canon → payload 34 cột: 14 trường hợp đồng, lineage, <code>content_key</code>, <code>canon</code> jsonb, 7 cặp <code>(khối, khối_thyt)</code>, <code>work_status</code>", "THIẾU ≠ SAI KIỂU: sai kiểu → <code>loai</code> (reject, <code>ACC-4</code>), thiếu tài khoản/tiền tệ → <code>cho</code> (<code>UNMAPPED</code>); ngày <code>d/m/y</code> mơ hồ NỔ nếu nguồn chưa khai <code>thu_tu</code> (<code>QĐ-ITL-113</code>)"],
            ["Ghi kho", "<code>chay_nap.chay</code>: <code>mo_run → them_le → _chen_reject → chen_bo_qua_trung → chen_moi_noi → chen_dong_pm → dong_run</code>", "một <code>run_id</code> <code>NAP-yyyy-mm-dd-NGUON</code> cho cả lô (59 nguồn, <code>QĐ-ITL-111/112</code>); <code>itl_id</code> do SEQUENCE cấp lúc <code>staged</code> (<code>INV-I04a</code>)", "bốn đường <code>vào = sổ + loại + rỗng + trùng</code> kiểm <b>trước và sau</b> ghi; <code>ON CONFLICT (content_key) DO NOTHING</code>; <code>row_count</code> đếm từ bảng, không cộng tay (<code>RUN_DEM_KHOP</code>); <code>_chen_reject</code> sửa 10/09 sau khi 646 dòng loại của 23 nguồn bị nuốt im lặng"],
        ])
        + P("<b>Hai lằn nạp cùng tồn tại.</b> Lằn cũ <code>NAP-2026-08-27-RAW</code> đọc <code>Transaction Mapping L1</code> (36 cột, đã phân loại) — 10.030 dòng, <code>chup_id = NULL</code> hợp lệ vì lô có trước bảng ảnh (<code>R-A1</code>: không bịa). Lằn mới <code>F04</code> đọc thẳng 64 sheet <code>R |</code> qua ảnh chụp — 8.387 dòng tiền sau khi dựng lại sổ 10/09. NÚT của owner <b>chỉ chụp, không nạp</b>: nạp tầng <code>R |</code> lên sổ hiện tại sinh +6.617 dòng và 3.694 dòng trùng; khoảng lệch 3.413 dòng phải giải thích từng dòng trước khi mở (<code>NUT-CHAY-FLS.cmd</code>).")
    ))

    # 2.3
    out.append(S("s2-3", f"§2.3 Ghép lệnh chi ↔ dòng tiền — sáu hình dạng, hai lằn hàng chờ {BUILT}", body=
        P("Ghép là ghép <b>dòng tiền bank ↔ DÒNG lệnh chi</b> (không phải phiếu: 526 phiếu mang 2–36 reference khác nhau, <code>CR#4</code>). Máy ghép lúc nạp những gì <b>tự chứng</b>; phần còn lại thành <b>việc của người</b> trên màn <code>F01</code>. Chiều đo đúng là <b>phía lệnh chi</b> (<code>QĐ-ITL-122</code>): câu hỏi của việc là «lệnh chi nào chưa tìm được tiền», không phải «dòng tiền nào chưa có lệnh».")
        + T([("Hình", 8), ("Định nghĩa", 26), ("Đo trên dữ liệu thật", 22), ("Máy làm gì", 44)], [
            ["<b>A</b>", "1 bank × 1 PM · Σ khớp", "2.256 mã · 2.256 dòng", "GHÉP lúc nạp; <code>fls_pm_link.hinh='A'</code>"],
            ["<b>B</b>", "1 bank × N PM · Σ khớp", "27 mã · 27 dòng", "GHÉP + <code>chia_tien</code> theo tỷ lệ, dồn dư vào phần lớn nhất — đúng tới đồng"],
            ["<b>C</b>", "N bank × 1 PM · Σ khớp (trả nhiều lần)", "80 mã · 394 dòng", "GHÉP, mỗi dòng bank giữ tiền của chính nó"],
            ["D", "N × M · Σ khớp", "5 mã · 27 dòng", "⛔ KHÔNG ĐOÁN (<code>INV-I16</code>) → người"],
            ["E", "khác tiền tệ", "119 mã · 199 dòng", "→ người (cần tỷ giá)"],
            ["F", "Σ lệch quá dung sai", "325 mã · 452 dòng", "→ người; dung sai VND 1.000 · ngoại tệ 0 · ghép tay <code>min(1.000, 0,5%)</code> (<code>QĐ-ITL-57/62/63</code>)"],
            ["<b>T</b>", "người ghép tay trên màn", "—", "<code>ghi_tay.ghep_lenh</code> 7 phép kiểm ⓐ–ⓖ; <code>lan</code> = lần ghép thứ n của cặp; bỏ ghép = thêm dòng <code>fls_pm_unlink</code> (<code>QĐ-ITL-69</code>), không xoá"],
        ])
        + MER("""flowchart LR
  classDef act fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef store fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef out fill:#fff7ed,stroke:#ea580c,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  itl[("fls_itl · vế PS Có 8.246")]:::store
  pml[("fls_pm_line · ảnh hiệu lực 3.772")]:::store
  auto["pm_join.xep_ca_lat<br/>canon_ref → hình A/B/C"]:::act
  link[("fls_pm_link 2.262–2.745<br/>view fls_moi_noi")]:::store
  lt["Lằn TIỀN (F01 cũ)<br/>doc_hang_cho · ung_vien_pm 4 bậc<br/>match · unmatch · done · reason · defer"]:::out
  ll["Lằn LỆNH CHI (F01 mặc định)<br/>lenh_cho.xep_ro → 3 rổ<br/>máy 60+61 · người · không bao giờ 514"]:::out
  lo["POST /queue/match-lo<br/>chỉ itl_ids[] · tự chứng · 422 cả lô"]:::gate
  tran["do_mau_so: TRẦN CỨNG 47,4%<br/>phủ trên trần 65,6%"]:::gate
  itl --> auto
  pml --> auto
  auto --> link
  itl --> lt
  pml --> ll
  link -.-> ll
  lt --> lo
  ll --> lo
  lo --> link
  link -.-> tran
""", "<strong>Hình 2.3</strong> — Hai lằn hàng chờ trên cùng một kho mối nối. Lằn LỆNH CHI hỏi đúng câu của việc và chia ba rổ; cú ghép vẫn đi qua một cửa ghi duy nhất.")
        + T([("Khái niệm", 20), ("Nghĩa", 50), ("Con số neo", 30)], [
            ["Ứng viên 4 bậc", "<code>ung_vien_pm</code>: <code>ma</code> (khớp <code>canon_ref</code>) › <code>tien</code> › <code>gan_tien</code> › <code>cung_tien_te</code>; bậc <code>ma</code> tính bằng Python, không SQL (một bản luật)", "trong 7.329 dòng chưa ghép: 0 dòng «không có ứng viên»"],
            ["Tự chứng", "đúng theo luật của <b>cửa GHI</b> (<code>ghep_lenh</code> 4 cổng: cùng tiền tệ · Σ trong dung sai · cả chùm cùng mã · <code>status = Approve</code>), <b>không</b> theo luật danh sách ứng viên", "68 dòng (0,9 %), không phải 584 — <code>QĐ-ITL-118</code>"],
            ["Ba rổ (G2)", "<code>lenh_cho.xep_ro</code>: <code>may</code> (máy trả lời được) · <code>nguoi</code> (cần tra) · <code>khong</code> (không bao giờ — số chứng từ không có tiền trong sổ, kèm lý do)", "121 máy (60 tự chứng + 61 lệch tiền) · 514 không bao giờ · 535 trống · 354 «số chứng từ là số tiền»"],
            ["Ảnh PM hiệu lực", "<code>anh_pm.anh_pm_hieu_luc</code> = ảnh có <code>max(read_at)</code>; ba nơi (ứng viên · ghép · đo) nhìn cùng một ảnh (<code>QĐ-ITL-119</code>) — thay luật cũ lọc theo <code>run_id</code> của dòng tiền khiến PM mới không bao giờ giúp được dòng tiền cũ", "nạp PM mới chỉ dịch 50/6.577 dòng ⇒ nút thắt là <b>số lệnh chi tồn tại</b>"],
            ["Trần cứng", "<code>toi_da_noi_duoc = da_noi + ranh</code>; <code>tran = toi_da / PS Có</code>; <code>phu_tren_tran = da_noi / toi_da</code>", "47,4 % · 65,6 % (thay 31,1 % đọc như thất bại) — chi tiết <a href='#s5-3'>§5.3</a>"],
        ])
    ))

    # 2.4
    out.append(S("s2-4", f"§2.4 Máy trạng thái <code>SM-I01…I05</code> và sổ chạy {PARTIAL}", body=
        P("Tài liệu BA-09 khai <b>năm</b> máy trạng thái; mã hôm nay cưỡng chế được <b>ba</b> hoàn toàn bằng cấu trúc, hai còn lại chỉ có cột trạng thái chờ đường đi. Tên trạng thái là hợp đồng (<code>R-A2</code>).")
        + MER("""stateDiagram-v2
  [*] --> staged : dung_dong + SEQUENCE cấp itl_id (INV-I04a)
  staged --> rejected : validate.loai → fls_reject (ACC-4)
  staged --> mapped : ghép PM tự chứng lúc nạp
  staged --> unmapped : máy tự bịa / thiếu 1 khối P&L → work_status UNMAPPED (INV-I16)
  mapped --> raw_frozen : raw_frozen = true → trigger cấm UPDATE/DELETE (INV-I03)
  unmapped --> raw_frozen
  raw_frozen --> adjusted : fls_adjustment + fls_journal (INV-I08, AUD-1)
  adjusted --> adjusted : reversal_of = bút toán mới, không có deleted (SM-I03)
  raw_frozen --> locked : period_state = locked (INV-I13) — CHƯA có đường đi
  note right of staged
    danh tính sinh TRƯỚC ghép (cú lật so với AS-IS)
    unmapped vẫn giữ itl_id
  end note
""", "<strong>Hình 2.4</strong> — SM-I01 dòng ITL như mã đang chạy: <code>raw_frozen</code> là điểm không quay lui; sửa sau đó chỉ bằng bút toán mới.")
        + T([("Máy", 12), ("Trạng thái trong mã", 34), ("Cưỡng chế ở đâu", 30), ("Build", 24)], [
            ["<code>SM-I01</code> dòng ITL", "<code>staged → mapped/unmapped → raw_frozen → adjusted</code>; <code>work_status</code> <code>ok | UNMAPPED | rejected</code>", "trigger <code>trg_fls_itl_inv_i03</code> (UPDATE/DELETE/TRUNCATE) · <code>itl_repo</code> chỉ INSERT · <code>test_chi_mot_cho_ghi_tay</code> quét mã nguồn", f"{BUILT} trừ <code>locked</code>"],
            ["<code>SM-I02</code> trường cần bổ sung", "<code>Classifying</code> có giá trị → <code>inherited</code>; <code>Need to manual input</code> → <code>needs_input</code>; <code>proposed_by_rule</code> (máy suy) · <code>proposed_by_human</code> → <code>final</code>; <b>bỏ</b> <code>approved</code> (<code>QĐ-ITL-16</code>)", "<code>final_rule.dung_khoi</code> + cột <code>*_thyt</code> = NULL chỗ máy bịa; mọi chuyển đổi sinh 1 dòng <code>fls_journal</code> 7 trường (<code>AUD-1</code>)", BUILT],
            ["<code>SM-I03</code> bút toán", "<code>posted | reversed</code>; đảo = dòng mới <code>reversal_of</code>; không <code>deleted</code>, không <code>draft/submitted/approved</code>", "<code>fls_adjustment.state</code> CHECK · <code>ghi_tay.dao_but_toan</code>", BUILT],
            ["<code>SM-I04</code> lần chạy", "<code>fls_run.state</code> mặc định <code>queued</code>; <code>chay_nap</code> dùng <code>staged → mapped</code>; các trạng thái <code>dq_passed/reconciling/published</code> của BA-09 không có trong mã", "<code>mo_run</code>/<code>dong_run</code>", f"{PARTIAL} — 2/8 trạng thái"],
            ["<code>SM-I05</code> kỳ", "<code>fls_itl.period_state</code> <code>open | locked</code>; <code>INV-I13</code> chặn ghi vào <code>locked</code> kể cả <code>force</code>", "<code>ghi_tay.truoc_khi_go</code>", f"{PARTIAL} — không có nút/cửa nào đưa kỳ sang <code>locked</code>; vai ký chốt chưa có người (<code>GAP-PLAN-04</code>)"],
        ])
        + P("<b>Sổ chạy, không sổ chung.</b> Mỗi loại việc có bảng vết riêng: <code>fls_run</code> (lô nạp, ghim 3 version hợp đồng — <code>INV-I12</code>), <code>fls_chup</code> (ảnh), <code>fls_queue_event</code> (việc người: <code>reason · defer · done · reopen</code>; máy cũng ghi <code>reason</code> lúc nạp CỜ), <code>fls_journal</code> (sửa 7 ô), <code>fls_pm_unlink</code> (bỏ ghép), <code>fls_migration</code> (di trú). Phép đếm mốc do đó hỏi <code>evt_type</code>, không hỏi <code>count(*)</code>: 108.128 sự kiện <code>reason</code> do máy không đóng được cổng nào (<code>test_MAY_ghi_93k_su_kien_ma_KHONG_dong_duoc_cong_nao</code>).")
    ))

    # 2.5
    out.append(S("s2-5", f"§2.5 Thước chuẩn, cổng số sống và đường ra <code>D3</code> {PARTIAL}", body=
        P("FLS không tin chính mình: mỗi con số nó sinh ra phải khớp một <b>thước</b> nằm ngoài đường ghi. Có ba lớp thước.")
        + T([("Lớp", 14), ("Cơ chế", 44), ("Đo được gì", 22), ("Nguồn", 20)], [
            ["Parity với sổ gốc", "<code>fls/oracle</code> đọc <code>ITL Ledge</code> (ADJUSTED) và bản sao RAW; <code>tu_soi</code> loại dòng bị gõ giữa hai lần đọc; <code>cong_parity.danh_gia</code> mặc định KHÔNG ĐẠT, đạt khi ≥1.000 ô · 0 lát trượt · 0 ô lệch; hiện vật đóng băng trong <code>tests/fixture/</code>", "4.088/4.088 ô (584 dòng T3/2026) · 68.915 ô 7 khối 100 % · 69.510/69.510 ô 23 kỳ", "<code>test_parity_*</code>, <code>ledge_spec</code> 64 cột"],
            ["Nguồn còn sống", "<code>G-ORA-LIVE-1/2/3</code>: kỳ mới nhất >45 ngày ⇒ nghi IMPORTRANGE chết · tab 0 dòng · tỷ lệ ghép ngoài [25 %, 45 %]; <code>doc_du</code> đọc lại cột then chốt sau khi 257 ô <code>svc_start</code> biến mất im lặng", "L1–L9 trên 64 sheet <code>R |</code> (cổng chung #17)", "<code>song.py</code>, <code>doc_du.py</code>, <code>kiem/nguon_song.py</code>"],
            ["Số sống trong tài liệu", "<code>tools/kiem_so_song.py</code> (cổng chung #13): mỗi con số máy đo (kho · git · pytest · lint-imports · <code>tien_do</code> · <code>do_mau_so</code>) phải xuất hiện <b>đúng một lần</b> trong <code>docs/ITL</code>; 0 hay ≥2 đều đỏ; không đo được ⇒ đỏ. Cũng là nơi <b>máy đếm mốc A/B</b>", "109/109 XANH (master index 2026-09-08); từng 66/66, 104", "<code>kiem_so_song.py::_cong_moc_a/_b</code>"],
        ])
        + P(f"<b>Đường ra hôm nay chỉ có <code>D3</code>.</b> <code>fls/xuat/ghi_o.py</code> là hàm thuần: ô đích là <code>Neo(tab, cột khoá, khoá, cột)</code> giải ra <code>A1</code> <b>trên bản sống</b> lúc lập biên bản (chèn dòng làm địa chỉ dịch — đã cắn thật khi owner co-edit); ghi hai lần không nhân đôi (so với giá trị đang có); biên bản chạy khô với 6 lý do từ chối có tên; <code>ap_dung(duyet=True)</code> + <code>FLS_CHO_GHI_SHEET=1</code> là hai khoá, một dòng bị từ chối ⇒ cả lô không ghi. Bộ vận chuyển được <b>tiêm vào</b>, module không gọi mạng và không tự lấy số từ kho (hợp đồng import-linter 9). Bộ xuất 64 cột <code>D1</code>, đối chiếu từng dòng <code>D2</code>, vòng khép kín <code>D5</code>: {PROPOSED} — <a href='#s10-1'>§10.1</a>. Owner đã đổi đích lưu trữ dài hạn sang BigQuery (<code>QĐ-ITL-120</code>) và hoãn (<code>QĐ-ITL-123</code>); FLS có 0 dòng mã BigQuery.")
    ))
    return out
