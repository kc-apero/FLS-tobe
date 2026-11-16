# IncrementalStepPlan-FLS-Voi v3.1.1

> **ISP v3.1.1** — cùng số với AP nó thực thi (apr-build-ap §A.30). Sinh bởi `docs/ITL/_tools/sinh_isp_voi.py` (2026-11-16); bộ sinh ĐỎ khi bước thiếu trường, phụ thuộc trỏ vào bước không có, DAG có chu trình, ước lượng > 4h, hoặc AP ghim sai sha256.
> ⛔ **Chưa triển khai.** Đây là bản chia bước để bạn duyệt. Không bước nào được chạy trước khi bạn xác nhận breakdown này.

## 1. Phần đầu kế hoạch

| Mục | Giá trị |
|---|---|
| Project | FLS — sổ cái ITL code hoá · lõi config chung (báo cáo + phân bổ) và HD1 'mapping 100% giống quá khứ' |
| Ngày lập | 2026-11-16 |
| AP baseline | `docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.1_Duyet_2026-11-16.html` · v3.1.1 · sha256 `d34f85842f6931d5e0d980806f5724056f66de3280bfe1ee6d41c2f2fcb3bb44` · 64/64 đơn vị `approved · 2026-11-16` · 0 lỗi ở 4 bộ kiểm |
| Phiên bản ISP | 3.1.1 (= AP) |
| Duyệt AP | người dùng phiên 16/11: *"Duyệt AP, đồng ý với các recommendation"* → 15 nhãn RECOMMENDED thành DECIDED (§2.1.1 · §2.1.2 · D1–D5 · Q1–Q6) ở v3.1.1; ThuongCT ký trước merge (O6) |
| Project instructions | `CLAUDE.md` (Đ1–Đ5, cổng, bẫy, riêng tư) · `docs/ITL/01_Orchestrator/10_HOP_DONG_AGENT.md` (vai, phiếu WO/HOI·TL/BG/KQ) |
| Repo / nhánh | `kc-apero/FLS-tobe` · nhánh làm việc `claude/laughing-bohr-331pt0` (hiện đi trước remote 2 commit + bản này — push 403, O1) · main ⛔ commit thẳng |
| Trạng thái hệ thống | **đang có, có lỗi đã đo**: 40 dòng `Tuyen(` ở `fls/api/bang_tuyen.py` · di trú 0001–0026 · 17 bảng · màn F01 (3 tệp) · F02 · F03 · F04 · 6 ảnh đóng băng ở `tests/fixture/` · ~1.677 bài test (số của CLAUDE.md, **chưa đo ở container**) |
| HD1 hôm nay (đo) | dòng ghép 1-1 **9.845/9.967** (5/23 kỳ đủ) · ô Final 7 khối 69.510/69.510 (23/23) · khối HD 9.930/9.930 · tự sinh 2026-03: HD 584/584, MID 4.020/4.088 — `voi_so_luong.json` |
| 122 dòng thiếu (đo 16/11, chỉ đọc ảnh) | rải 18/23 kỳ (2026-07: 23 · 2025-11: 14 · 2026-08: 13 …) · 121/122 có `hd_classifying = Need to manual input` · hd Final: OGA 74 · GI 25 · DEP 8 · ITE 7 · khác 8 · chiều ngược: 9.992 − 9.845 = **147** dòng FLS ⛔ có dòng sổ |
| HD2 hôm nay | 0 ô — engine báo cáo/phân bổ chưa có (AC9: 0/10 bảng config có mã engine) |
| Môi trường container (đo 16/11) | PostgreSQL 16 có binary · node 22 · PyPI vào được · ⛔ Docker daemon · ⛔ pytest ở python hệ thống · ⛔ `.venv` |
| Nguồn đã đọc | AP v3.1.1 §1.3 · §2.1–§2.5 · §3.1–§3.5 · §4.3–§4.5 · §5.1–§5.5 · `CLAUDE.md` · `10_HOP_DONG_AGENT.md` §1–§4 · `.importlinter` (9 hợp đồng) · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `fls/ledger/allocate.py` · `fls/oracle/cong_parity.py` · `tests/conftest.py` · danh sách `tests/**` · 3 ảnh fixture HD1 · `06_SCREEN_SPEC.md` (mã màn) |
| Nguồn nhắc tới, chưa đọc lại ở lượt này | sheet Drive AS-IS (đã đọc ở phiên dựng AP v3.0.0 — giá trị sẽ đóng băng ở DT2…DT12) · `docs/ITL/03_Dev/01_TECH_DESIGN.md` |
| agent_count | **4** — BE-HC (hard code) · BE-CF (config) · FE · DATA; mỗi agent một bước đang chạy |
| review_rounds | **3** — R1 quét toàn diff + process-issues (O3) · R2 chỉ phần đổi sau R1 · R3 chỉ phần đổi sau R2 · rồi push tự động (khi O1 xong) |
| Đơn vị ước lượng | giờ làm việc của agent; **nửa ngày = 4 giờ** (giả định lập kế hoạch — dự án chưa khai quy ước); một ô wave = nửa ngày |
| Tổng | 51 bước · 141–203 giờ-agent · 18 wave (máy xếp) · theo làn: BE-CF 15 · BE-HC 16 · FE 7 · DATA 13 |

### 1.1 Phạm vi

|  | Gồm | Ngoài (lý do) |
|---|---|---|
| HD1 | 122 dòng chưa 1-1: phân loại → sửa lớp lỗi mã → miễn trừ có chữ ký; tự sinh theo kỳ (AC10 · AC11) | đọc kho sống theo tháng (HD5 — sau khi O4 có kho thật) |
| Lõi config (WP-C1) | IX.FX · IX.HD · IX.ORG · IX.PER · IX.VEN · IX.DRV · IX.ALR · IX.PL · IX.TMP — nạp, kiểm, kho chỉ-thêm, ký | bật cờ luật (D2: parity trước) · chia đều kỳ PL (D4 B) |
| Engine (WP-C2…C5) | CA.GL · SO.CFA1/3 · SO.PLA1/3 · AL.PLT · AL.KEY · SO.PLA3-ATL · RP.CF/PL — mỗi cái có cổng parity với đáp án NOW | ghi CCR / PDF (HD4 — cắt Gsheet) · BigQuery (Q4 DECIDED: PostgreSQL trước) |
| Màn | SCR-F09 Đối chiếu (Figure 2.2 làm wireframe) · SCR-F08 Cấu hình (IX.FX + ký) | màn cây HD, màn cờ luật (⛔ có trong AP v3.1.1) |
| Ngoài hẳn | — | agent RI/PR/SI (AP §5.3.1: agent chỉ vào sau HD1 + HD2) · họ HR/PLT ở Agent 1·2 (§4.5 PROPOSED) · AP/AR (Q5 DECIDED: GĐ2) |

### 1.2 Quyết định còn mở — mỗi câu đã có khuyến nghị

| Mã | Câu | A | B | Khuyến nghị | Chặn gì |
|---|---|---|---|---|---|
| O1 | Push bị chặn 403 (`push_denied`) — 2 commit AP đang chờ, mọi bước sẽ chờ theo | A · nối lại GitHub bằng tài khoản có quyền ghi trước Wave 1 (claude.ai/connect-github) — được: push tự động sau R3 chạy đúng luật · mất: cần owner thao tác một lần | B · chạy hết, orchestrator gửi patch theo wave — được: ⛔ chờ · mất: 'tự push sau 3 vòng' ⛔ thực hiện được; rủi ro lệch nhánh | A | Chặn mọi bước ở trạng thái `review → done-pushed`; bước vẫn code + review được |
| O2 | Nhánh làm việc | A · mỗi agent một worktree cục bộ, nhánh cục bộ `isp/<bước>` (⛔ push); sau R3 orchestrator gộp vào `claude/laughing-bohr-331pt0` rồi push; PR vào main chỉ khi bạn duyệt | B · push từng nhánh `claude/laughing-bohr-331pt0-<bước>` lên remote — được: thấy trên GitHub · mất: cần bạn cho phép push nhánh khác | A | B cần quyền rõ ràng (luật phiên: chỉ push nhánh đã giao) |
| O3 | `/process-issues` cần bảng ReportIssue + gấp vào AP; dự án ⛔ có bảng ấy | A · R1 chạy triage A1/A2/B1/B2 của process-issues trên phát hiện review, ghi `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.1.md` + một dòng 'luật phòng tái phạm' cho bước sau đọc; chỉ phát hiện làm đổi AP mới gấp vào bản AP vá (gom theo wave, ISP cùng số §A.30) | B · mỗi phát hiện một bản AP mới — được: đúng nguyên skill · mất: ~50 bản AP, nhiễu | A | Sổ phát hiện là bằng chứng 'đã chạy process-issues' của R1 |
| O4 | Nơi chạy test | A · container cloud này: PG16 cục bộ :5433 (đo: có binary, PyPI vào được) — được: cô lập, lặp lại được · mất: ⛔ phải `fls-pg-1` thật | B · máy Windows của owner với `fls-pg-1` — được: kho thật · mất: agent cloud ⛔ chạm được | A cho mọi bước + chạy lại I2 trên máy owner trước merge | Ảnh hưởng S0 và điều kiện merge |
| O5 | Lưu config: một cặp bảng chỉ-thêm có phiên bản dùng chung, hay một bảng gõ kiểu cho mỗi IX.* | A · dùng chung (`fls_cau_hinh_ban` + `fls_cau_hinh_dong` jsonb) — được: một khái niệm, một di trú, ít sửa ERD · mất: kiểu dữ liệu kiểm ở tầng `fls/cau_hinh` thay vì DDL | B · 10 bảng gõ kiểu — được: DDL chặt · mất: 10 di trú + 10 lần sinh lại ERD/golden | A | Đổi C5…C13; B thêm ~1 bước mỗi bảng |
| O6 | AP v3.1.1 ghi duyệt theo lời bạn trong phiên; AP ghi Owner là ThuongCT | A · chạy Wave 0–n trên nhánh (đảo ngược được), ThuongCT ký trước MERGE vào main | B · chờ ThuongCT ký trước Wave 0 | A | Chỉ chặn merge |
| O7 | Agent con có thể ⛔ có công cụ Google Drive/Sheets | A · orchestrator (phiên này) đọc giá trị sheet chỉ-đọc vào scratchpad; DATA đóng băng từ bản ấy; bản thô ⛔ commit; cổng PII chặn cột cấm | B · cấp công cụ Drive cho agent DATA — được: tự chủ · mất: chưa chắc khả dụng; rộng quyền | A | Chặn DT2…DT12 |
| O8 | Ai ký 'lệch có tên lý do' của HD1 | A · ThuongCT ký sổ `so_ly_do_hd1.json`; chưa ký = đỏ | B · operator ký thay | A | Quyết định số kỳ đạt HD1 thật |
| O9 | AP v3.1.1 ⛔ có wireframe cho màn mới; F05–F07 đã dùng/khai tử ở `06_SCREEN_SPEC` | A · SCR-F09 lấy Figure 2.2 · 5.3.3 làm wireframe, SCR-F08 theo khuôn F04; fls-ba đăng ký mã F08/F09 trước F1 | B · BA vẽ wireframe đầy đủ trước — được: chặt · mất: FE chờ ≥ 1 wave | A | Chặn F1 tới khi mã màn được đăng ký |

Quyết định đã chốt (AP v3.1.1, DECIDED 16/11) được dùng thẳng: §2.1 định nghĩa A · Q1 giữ ngữ pháp · Q2 SI.MAP → Agent 2 · Q3 HR ⛔ qua ALLOCATE · Q4 PostgreSQL trước · Q5 AP/AR ở GĐ2 · Q6 A · D1 IX.FX ký tháng, thiếu = CHẶN · D2 parity trước, cờ tắt · D3 driver by GI = PE · D4 dồn ngày 1 PL start · D5 bản A-CCR chính thức, FS là tham số.

## 2. Dependency và lịch thực hiện

### 2.1 Làn và tệp sở hữu (⛔ giao trùng)

| Làn | Agent | Số bước | Tệp/thư mục chỉ làn này ghi |
|---|---|---|---|
| BE-CF | Backend · config · `fls-dev #CF` | 15 | `fls/cau_hinh/**` · `fls/repo/cau_hinh_repo.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `fls/api/doi_chieu.py` · `fls/db/migrations/0027_*.sql` · `fls/db/schema.py (chỉ phần 0027)` · `tests/cau_hinh/**` · `tests/api/test_isp_*.py` · `tools/soi_bang_tuyen.py` |
| BE-HC | Backend · hard code (engine) · `fls-dev #HC` | 16 | `fls/bao_cao/**` · `fls/ledger/**` · `fls/oracle/**` · `fls/adapters/**` · `tools/do_voi_so_luong.py` · `tools/do_hd2.py` · `docs/ITL/_tools/voi_so_luong.json` · `docs/ITL/_tools/hd2_cong.json` · `tests/bao_cao/**` · `tests/ledger/**` · `tests/oracle/**` |
| FE | Frontend · `fls-dev #FE` | 7 | `fls/web/tep/**` · `tests/web/test_isp_*.py` |
| DATA | Data · `fls-dev #DATA` | 13 | `tests/fixture/cau_hinh/**` · `tests/fixture/dap_an/**` · `tests/du_lieu/**` · `tools/dong_bang_sheet.py` · `tools/phan_loai_dong_thieu.py` · `docs/ITL/_tools/phan_loai_dong_thieu.json` · `tests/tich_hop/test_hd1_*.py` |

Mã bước: `S0` · `C*` BE-CF · `H*` BE-HC · `F*` FE · `DT*` DATA · `I*` tích hợp cuối. ⚠ `D1`–`D5` trong tài liệu này luôn là **quyết định** của AP §3.5.3, ⛔ bước — bước DATA mang tiền tố `DT` chính vì vậy.

Tệp dùng chung, tuần tự hoá: `.importlinter` → S0 · `pyproject.toml` → S0 · `requirements.txt` → S0 · `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md §5` → mọi bước — chỉ THÊM một dòng (hợp đồng agent §1). Mọi tuyến API mới đi qua làn BE-CF (chỉ một làn chạm `bang_tuyen.py`/`xu_ly.py`); engine của BE-HC lộ ra bằng lệnh cổng + JSON, BE-CF mở tuyến đọc JSON ấy (C2 · C3 · C14).

### 2.2 Wave (máy xếp — mỗi làn một bước một lúc; một wave ≈ nửa ngày)

| Wave | BE-HC | BE-CF | FE | DATA |
|---|---|---|---|---|
| W0 |  | Step 0 · S0 · Môi trường test + đường nền cổng + khung hai gói mới |  |  |
| W1 | Step 2 · H1 · CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD) | Step 1 · C1 · IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx | Step 3 · F1 · SCR-F09 Đối chiếu · bảng tháng × loại dữ liệu (dữ liệu giả theo hợp đồng C2) | Step 4 · DT1 · HD1 · phân loại 122 dòng sổ chưa có bản dựng 1-1 |
| W2 | Step 6 · H2 · HD1 · cổng nhận 'lệch có tên lý do và owner ký' | Step 5 · C2 · GET /parity/months — bảng tháng × loại dữ liệu từ tệp đo |  | Step 7 · DT2 · Đường ống đóng băng sheet + ảnh IX.FX (9.2 Exchange Rate) |
| W3 | Step 9 · H3 · HD1 · sửa lớp lỗi mã lớn nhất mà DT1 chỉ ra | Step 8 · C3 · GET /parity/months/{ky}/rows — danh sách dòng chưa 1-1 của một kỳ | Step 10 · F2 · SCR-F09 nối tuyến thật GET /parity/months | Step 11 · DT3 · Ảnh nguồn IX.HD · IX.ORG: cây ATL 74 dòng + Mapping Master + CDT Correct |
| W4 |  | Step 12 · C4 · IX.HD cây: nạp + kiểm cha–con + GET /config/hd (tĩnh từ ảnh) | Step 13 · F3 · SCR-F09 khoan xuống: ô kỳ → danh sách dòng chưa 1-1 (AC7) | Step 14 · DT4 · Ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT) |
| W5 | Step 16 · H4 · KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên) | Step 15 · C5 · Kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho |  | Step 17 · DT5 · Ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M |
| W6 | Step 19 · H5 · SO.CFA1 Daily: Σ theo (HD, ngày) trên cây IX.HD | Step 18 · C6 · IX.PER: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4) | Step 20 · F4 · SCR-F08 Cấu hình · bảng IX.FX chỉ đọc trên tuyến thật | Step 21 · DT8 · Ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI |
| W7 | Step 23 · H6 · SO Y/H/Q/M theo IX.PER | Step 22 · C9 · IX.VEN: vendor · network · CDT1 + cột 'cách tính' |  | Step 24 · DT6 · Ảnh đáp án GL HR + CFA3 (407 · 408 · 412 · 413) |
| W8 | Step 26 · H9 · AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P) | Step 25 · C8 · IX.ORG: LE · TK → CDT1 + CDT lạ vào hàng chờ (⛔ rơi về SHQ2) |  | Step 27 · DT10 · Ảnh IX.DRV (Allocation Table) + đáp án ATL (604 · 606) |
| W9 | Step 29 · H10 · AL.PLT · 5 vendor đặc biệt theo cột 'cách tính' | Step 28 · C10 · IX.DRV: driver theo (driver, CDT1, tháng) |  | Step 30 · DT7 · Ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (414–419) |
| W10 | Step 32 · H7 · CA.GL dòng HR + SO.CFA3 | Step 31 · C11 · IX.ALR: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT (D2) |  | Step 33 · DT9 · Ảnh đáp án MID1–MID3 của OMC · SC · PS |
| W11 | Step 35 · H11 · AL.PLT · OMC · SC · PS | Step 34 · C12 · IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK |  | Step 36 · DT12 · Ảnh Manual input của 22 kỳ còn lại (chế độ tự sinh AC10) |
| W12 | Step 38 · H8 · SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá | Step 37 · C14 · GET /parity/hd2 — trạng thái cổng HD2 theo gói WP-C2…C5 |  | Step 39 · DT11 · Ảnh đáp án Daily Report 2 · 3 (607–616) |
| W13 | Step 41 · H12 · AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2) | Step 40 · C7 · IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1) | Step 42 · F6 · SCR-F09 khối HD2 theo gói WP-C2…C5 |  |
| W14 | Step 44 · H13 · SO.PLA3-ATL + IX.PL CHECK | Step 43 · C13 · IX.TMP: bản báo cáo ký có phiên bản (snapshot sign-off) | Step 45 · F5 · SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận |  |
| W15 | Step 46 · H15 · HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho 22 kỳ còn lại) |  | Step 47 · F7 · SCR-F09 ký bản Daily Report 3 (IX.TMP snapshot) |  |
| W16 | Step 48 · H14 · RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5) |  |  | Step 49 · I1 · Tích hợp HD1 xuyên suốt: ảnh → ghép → cổng theo kỳ → API → SCR-F09 |
| W17 | Step 50 · I2 · Tích hợp HD2 xuyên suốt: config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản |  |  |  |

Đường găng (13 bước): S0 → DT2 → DT3 → C4 → C5 → C6 → H6 → H7 → H8 → H12 → H13 → H14 → I2. Ô trống = làn chờ phụ thuộc — dùng để sửa phát hiện review của bước trước (review 3 vòng tốn thời gian thật).

### 2.3 Bảng phân công

| Bước | Phụ thuộc | Wave | Owner | Tệp chạm | Ước lượng | Trạng thái | Review |
|---|---|---|---|---|---|---|---|
| Step 0 · S0 | — | W0 | BE-CF · `fls-dev #CF` | `tools/dung_moi_truong_isp.sh` · `.importlinter` · `fls/cau_hinh/__init__.py` · `fls/bao_cao/__init__.py` · `docs/ITL/03_Dev/isp-3.1.1/DUONG_NEN.md` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 1 · C1 | S0 | W1 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/fx.py` · `fls/cau_hinh/tinh/ix_fx_mau.json` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_fx.py` · `tests/api/test_isp_config_fx.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 2 · H1 | S0 | W1 | BE-HC · `fls-dev #HC` | `fls/bao_cao/gl.py` · `tests/bao_cao/test_gl.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 3 · F1 | S0 | W1 | FE · `fls-dev #FE` | `fls/web/tep/man_f09.js` · `fls/web/tep/ung_dung.js` · `fls/web/tep/index.html` · `tests/web/test_isp_f09_bang.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 4 · DT1 | S0 | W1 | DATA · `fls-dev #DATA` | `tools/phan_loai_dong_thieu.py` · `tests/du_lieu/test_phan_loai_dong_thieu.py` · `docs/ITL/_tools/phan_loai_dong_thieu.json` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 5 · C2 | S0 | W2 | BE-CF · `fls-dev #CF` | `fls/api/doi_chieu.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/api/test_isp_parity_months.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 6 · H2 | DT1 | W2 | BE-HC · `fls-dev #HC` | `tools/do_voi_so_luong.py` · `docs/ITL/_tools/voi_so_luong.json` · `tests/oracle/test_do_voi_hd1.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 7 · DT2 | S0 | W2 | DATA · `fls-dev #DATA` | `tools/dong_bang_sheet.py` · `tests/du_lieu/test_dong_bang_sheet.py` · `tests/fixture/cau_hinh/ix_fx.json` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 8 · C3 | C2, DT1 | W3 | BE-CF · `fls-dev #CF` | `fls/api/doi_chieu.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/api/test_isp_parity_rows.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 9 · H3 | H2, DT1 | W3 | BE-HC · `fls-dev #HC` | `fls/ledger/classifying.py \| fls/adapters/sao_ke_canon.py` · `tools/do_voi_so_luong.py` · `tests/ledger/test_hd1_lop1.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 10 · F2 | F1, C2 | W3 | FE · `fls-dev #FE` | `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_that.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 11 · DT3 | DT2 | W3 | DATA · `fls-dev #DATA` | `tests/fixture/cau_hinh/*.json` · `tests/du_lieu/test_anh_cau_hinh.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 12 · C4 | DT3 | W4 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/hd.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_hd.py` · `tests/api/test_isp_config_hd.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 13 · F3 | F2, C3 | W4 | FE · `fls-dev #FE` | `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_khoan.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 14 · DT4 | DT2 | W4 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/gl_406.json` · `tests/du_lieu/test_dap_an_406.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 15 · C5 | C4, DT2 | W5 | BE-CF · `fls-dev #CF` | `fls/db/migrations/0027_cau_hinh_chi_them.sql` · `fls/db/schema.py` · `fls/repo/cau_hinh_repo.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_kho_cau_hinh_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 16 · H4 | H1, DT4, DT2, C1 | W5 | BE-HC · `fls-dev #HC` | `tools/do_hd2.py` · `docs/ITL/_tools/hd2_cong.json` · `tests/oracle/test_do_hd2_ca.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 17 · DT5 | DT3 | W5 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/cfa1_*.json` · `tests/du_lieu/test_dap_an_cfa1.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 18 · C6 | C5 | W6 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/ky.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_ky.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 19 · H5 | H4, C4, DT5 | W6 | BE-HC · `fls-dev #HC` | `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cfa1.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 20 · F4 | F1, C5 | W6 | FE · `fls-dev #FE` | `fls/web/tep/man_f08.js` · `fls/web/tep/ung_dung.js` · `tests/web/test_isp_f08_fx_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 21 · DT8 | DT2 | W6 | DATA · `fls-dev #DATA` | `tests/fixture/cau_hinh/ix_ven.json` · `tests/fixture/dap_an/gi_mid*.json` · `tests/du_lieu/test_dap_an_gi.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 22 · C9 | C5, DT8 | W7 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/vendor.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_vendor_pg.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 23 · H6 | H5, C6 | W7 | BE-HC · `fls-dev #HC` | `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cuon_ky.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 24 · DT6 | DT2 | W7 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/gl_hr.json` · `tests/fixture/dap_an/cfa3.json` · `tests/du_lieu/test_dap_an_hr.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 25 · C8 | C5, DT3 | W8 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/to_chuc.py` · `fls/repo/cau_hinh_repo.py` · `tests/cau_hinh/test_to_chuc_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 26 · H9 | H4, C9, DT8 | W8 | BE-HC · `fls-dev #HC` | `fls/bao_cao/phan_bo.py` · `tools/do_hd2.py` · `tests/bao_cao/test_phan_bo.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 27 · DT10 | DT2 | W8 | DATA · `fls-dev #DATA` | `tests/fixture/cau_hinh/ix_drv.json` · `tests/fixture/dap_an/atl.json` · `tests/du_lieu/test_dap_an_atl.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 28 · C10 | C5, DT10 | W9 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/driver.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_driver_pg.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 29 · H10 | H9 | W9 | BE-HC · `fls-dev #HC` | `fls/bao_cao/phan_bo.py` · `tests/bao_cao/test_vendor_dac_biet.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 30 · DT7 | DT2 | W9 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/pla*.json` · `tests/du_lieu/test_dap_an_pla.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 31 · C11 | C5, DT3 | W10 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/luat_pb.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_luat_pb_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 32 · H7 | H6, DT6, C8 | W10 | BE-HC · `fls-dev #HC` | `fls/bao_cao/gl.py` · `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cfa3.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 33 · DT9 | DT8 | W10 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/{omc,sc,ps}_mid*.json` · `tests/du_lieu/test_dap_an_nen_tang.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 34 · C12 | C4, C5 | W11 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/dong_pl.py` · `tests/cau_hinh/test_dong_pl.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 35 · H11 | H10, DT9 | W11 | BE-HC · `fls-dev #HC` | `fls/bao_cao/phan_bo.py` · `tools/do_hd2.py` · `tests/bao_cao/test_nen_tang_ba_so.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 36 · DT12 | DT2 | W11 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/itl_ledge_*.json` · `tests/du_lieu/test_anh_manual_input.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 37 · C14 | C2, H4 | W12 | BE-CF · `fls-dev #CF` | `fls/api/doi_chieu.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/api/test_isp_parity_hd2.py` | 2–3h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 38 · H8 | H7, DT7, C6 | W12 | BE-HC · `fls-dev #HC` | `fls/bao_cao/pla.py` · `tools/do_hd2.py` · `tests/bao_cao/test_pla.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 39 · DT11 | DT2 | W12 | DATA · `fls-dev #DATA` | `tests/fixture/dap_an/daily_report_*.json` · `tests/du_lieu/test_dap_an_report.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 40 · C7 | C5 | W13 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/fx.py` · `fls/repo/cau_hinh_repo.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_ky_fx_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 41 · H12 | H8, H11, C10, C11, DT10 | W13 | BE-HC · `fls-dev #HC` | `fls/bao_cao/phan_bo_khoa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_phan_bo_khoa.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 42 · F6 | F2, C14 | W13 | FE · `fls-dev #FE` | `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_hd2.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 43 · C13 | C7 | W14 | BE-CF · `fls-dev #CF` | `fls/cau_hinh/ban_ky.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_ban_ky_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 44 · H13 | H12, C12 | W14 | BE-HC · `fls-dev #HC` | `fls/bao_cao/pla.py` · `tools/do_hd2.py` · `tests/bao_cao/test_pla_atl.py` | 2–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 45 · F5 | F4, C7 | W14 | FE · `fls-dev #FE` | `fls/web/tep/man_f08.js` · `tests/web/test_isp_f08_ky_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 46 · H15 | H3, DT12 | W15 | BE-HC · `fls-dev #HC` | `tools/do_voi_so_luong.py` · `docs/ITL/_tools/voi_so_luong.json` · `tests/oracle/test_tu_sinh_theo_ky.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 47 · F7 | F6, C13 | W15 | FE · `fls-dev #FE` | `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_ky_ban_pg.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 48 · H14 | H13, DT11, C13 | W16 | BE-HC · `fls-dev #HC` | `fls/bao_cao/bao_cao.py` · `tools/do_hd2.py` · `tests/bao_cao/test_daily_report.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 49 · I1 | H15, C3, F3, H2 | W16 | DATA · `fls-dev #DATA` | `tests/tich_hop/test_hd1_xuyen_suot.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |
| Step 50 · I2 | H14, C13, C14, F7, I1 | W17 | BE-HC · `fls-dev #HC` | `tests/tich_hop/test_hd2_xuyen_suot.py` | 3–4h | planned | R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới) |

<details><summary>Sơ đồ phụ thuộc (mermaid)</summary>

```mermaid
flowchart LR
  subgraph BE_CF["BE-CF"]
    S0["S0"]
    C1["C1"]
    C2["C2"]
    C3["C3"]
    C4["C4"]
    C5["C5"]
    C6["C6"]
    C9["C9"]
    C8["C8"]
    C10["C10"]
    C11["C11"]
    C12["C12"]
    C14["C14"]
    C7["C7"]
    C13["C13"]
  end
  subgraph BE_HC["BE-HC"]
    H1["H1"]
    H2["H2"]
    H3["H3"]
    H4["H4"]
    H5["H5"]
    H6["H6"]
    H9["H9"]
    H10["H10"]
    H7["H7"]
    H11["H11"]
    H8["H8"]
    H12["H12"]
    H13["H13"]
    H15["H15"]
    H14["H14"]
    I2["I2"]
  end
  subgraph FE["FE"]
    F1["F1"]
    F2["F2"]
    F3["F3"]
    F4["F4"]
    F6["F6"]
    F5["F5"]
    F7["F7"]
  end
  subgraph DATA["DATA"]
    DT1["DT1"]
    DT2["DT2"]
    DT3["DT3"]
    DT4["DT4"]
    DT5["DT5"]
    DT8["DT8"]
    DT6["DT6"]
    DT10["DT10"]
    DT7["DT7"]
    DT9["DT9"]
    DT12["DT12"]
    DT11["DT11"]
    I1["I1"]
  end
  S0 --> C1
  S0 --> H1
  S0 --> F1
  S0 --> DT1
  S0 --> C2
  DT1 --> H2
  S0 --> DT2
  C2 --> C3
  DT1 --> C3
  H2 --> H3
  DT1 --> H3
  F1 --> F2
  C2 --> F2
  DT2 --> DT3
  DT3 --> C4
  F2 --> F3
  C3 --> F3
  DT2 --> DT4
  C4 --> C5
  DT2 --> C5
  H1 --> H4
  DT4 --> H4
  DT2 --> H4
  C1 --> H4
  DT3 --> DT5
  C5 --> C6
  H4 --> H5
  C4 --> H5
  DT5 --> H5
  F1 --> F4
  C5 --> F4
  DT2 --> DT8
  C5 --> C9
  DT8 --> C9
  H5 --> H6
  C6 --> H6
  DT2 --> DT6
  C5 --> C8
  DT3 --> C8
  H4 --> H9
  C9 --> H9
  DT8 --> H9
  DT2 --> DT10
  C5 --> C10
  DT10 --> C10
  H9 --> H10
  DT2 --> DT7
  C5 --> C11
  DT3 --> C11
  H6 --> H7
  DT6 --> H7
  C8 --> H7
  DT8 --> DT9
  C4 --> C12
  C5 --> C12
  H10 --> H11
  DT9 --> H11
  DT2 --> DT12
  C2 --> C14
  H4 --> C14
  H7 --> H8
  DT7 --> H8
  C6 --> H8
  DT2 --> DT11
  C5 --> C7
  H8 --> H12
  H11 --> H12
  C10 --> H12
  C11 --> H12
  DT10 --> H12
  F2 --> F6
  C14 --> F6
  C7 --> C13
  H12 --> H13
  C12 --> H13
  F4 --> F5
  C7 --> F5
  H3 --> H15
  DT12 --> H15
  F6 --> F7
  C13 --> F7
  H13 --> H14
  DT11 --> H14
  C13 --> H14
  H15 --> I1
  C3 --> I1
  F3 --> I1
  H2 --> I1
  H14 --> I2
  C13 --> I2
  C14 --> I2
  F7 --> I2
  I1 --> I2
```

</details>

### 2.4 Vòng một bước — orchestrator, phiếu, review, push

| # | Ai | Làm gì | Ra |
|---|---|---|---|
| 1 | orchestrator (phiên này) | kiểm phụ thuộc done · ước lượng còn lại · rủi ro · tệp ⛔ chồng → đổi `planned → ready`; cấp `WO-063+` tối thiểu trỏ về bước ISP (ISP là spec — hợp đồng agent §2 luật thứ tự) | WO |
| 2 | agent của làn (worktree riêng, nhánh cục bộ `isp/<bước>`) | Substep 1 → báo; Substep 2 TDD: test đỏ → lưu log đỏ → mã tối thiểu → xanh → chạy lại bộ liên quan | BG kèm log đỏ/xanh thật |
| 3 | R1 · fls-test phiên mới | quét TOÀN diff của bước: lỗi, lệch spec, lệch AP, Đ1–Đ5; chạy triage process-issues (A1/A2/B1/B2) vào sổ phát hiện + luật phòng tái phạm (O3) | KQ-R1 + sổ phát hiện |
| 4 | agent | sửa theo khuyến nghị R1; chạy lại test bị ảnh hưởng | commit sửa |
| 5 | R2 · fls-test phiên mới | chỉ quét phần đổi SAU R1 | KQ-R2 |
| 6 | R3 · fls-test phiên mới | chỉ quét phần đổi SAU R2; còn phát hiện chặn ⇒ sửa rồi R3 lại (⛔ push khi còn chặn) | KQ-R3 |
| 7 | orchestrator | gộp `isp/<bước>` vào `claude/laughing-bohr-331pt0`, chạy lại cổng CLAUDE.md, push (sau O1); ghi §5 dashboard; `review → done` | commit trên nhánh làm việc |
| 8 | người dùng | merge vào main chỉ qua PR bạn duyệt + ThuongCT ký (O6) | PR |

Theo dõi: `docs/ITL/01_Orchestrator/isp-3.1.1/TIEN_DO.md` — trạng thái `planned → ready → in_progress → review(R1/R2/R3) → done` hoặc `blocked` kèm nguyên nhân; tiến độ theo bằng chứng (exit criteria), ⛔ gán phần trăm.

## 3. Các bước

## Step 0 · S0 — Môi trường test + đường nền cổng + khung hai gói mới

**Traceability:** AP v3.1.1 §1.3.3 (luật agent lấy từ CLAUDE.md) · §5.3.1 HD5 (lặp lại được) · CLAUDE.md §Cổng.  
**Estimate:** 3–4 giờ · độ tin: trung bình — đo 16/11: container có PostgreSQL 16 (`/usr/lib/postgresql/16/bin`), node 22, PyPI vào được; ⛔ Docker, ⛔ pytest; **Dependency:** không có.  
**Ownership:** task `S0` · owner `fls-dev #CF` (BE-CF) · wave W0 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Môi trường test + đường nền cổng + khung hai gói mới

### 2. Goal

Một lệnh dựng được môi trường và in đường nền: số bài pytest đỏ/xanh, 26 di trú áp đủ, lint-imports 11 hợp đồng giữ, cổng HD1 in 9.845/9.967.

### 3. Scope

- **Gồm:** venv `.venv` + `requirements.txt` (psycopg · pytest · import-linter); cụm PostgreSQL 16 cục bộ cổng 5433, user/kho `fls` (⛔ `docker compose down` — ở container ⛔ có Docker; trên máy owner vẫn `docker start fls-pg-1`); chạy đường nền mọi cổng ở CLAUDE.md, GHI kết quả THẬT (kể cả bài đỏ có sẵn) vào `docs/ITL/03_Dev/isp-3.1.1/DUONG_NEN.md`; tạo hai gói rỗng có hợp đồng tầng: `fls/cau_hinh` (config thuần, ⛔ DB) · `fls/bao_cao` (engine báo cáo/phân bổ thuần, ⛔ DB) — để hai làn BE ⛔ cùng sửa `.importlinter` về sau
- **Loại trừ:** sửa bất kỳ bài đỏ có sẵn nào (ghi vào DUONG_NEN, chuyển orchestrator); dữ liệu thật vào kho (`FLS_CHO_GHI_THAT` ⛔ đặt)
- **Khái niệm mới duy nhất:** môi trường test của ISP (hạ tầng chạy)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** kho test là cụm cục bộ, ⛔ phải `fls-pg-1` của owner — bước tích hợp cuối chạy lại trên máy owner (O4)

### 4. Components touched

- **Frontend:** N/A — chưa có màn mới; chỉ chạy bộ test web sẵn có để lấy đường nền.
- **Backend:** `fls/cau_hinh/__init__.py`, `fls/bao_cao/__init__.py` (rỗng, có docstring vai)
- **DB:** cụm PG16 cục bộ :5433 · `python -m fls.db.pg_migrate` → 0001…0026
- **Integrations:** `.importlinter` +2 hợp đồng (cau_hinh, bao_cao ⛔ psycopg/fls.repo/fls.db)

### 5. Preconditions

- người dùng duyệt ISP 3.1.1
- O4 chốt nơi chạy (khuyến nghị: container này)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| S0-B1 | chạy `python -m pytest` lần đầu | có dòng tổng kết `N passed`; mọi bài đỏ được liệt kê tên trong DUONG_NEN (⛔ con số trần) | toàn bộ | chưa có pytest ⇒ hôm nay ⛔ chạy được |
| S0-B2 | `python -m fls.db.pg_migrate` | 26/26 di trú áp; `pg_verify` exit 0 | tích hợp DB | chưa có cụm PG |
| S0-B3 | `lint-imports` | 11 hợp đồng giữ (9 cũ + 2 mới); phá thử: `import psycopg` trong `fls/bao_cao` ⇒ ĐỎ, gỡ ⇒ xanh (Đ5) | kiến trúc | hai hợp đồng mới chưa có |
| S0-B4 | `python tools/do_voi_so_luong.py` | exit 0; in `chay 9845 / co 9967` (đúng `MONG`) | cổng dữ liệu | chưa chạy ở môi trường mới |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| S0-F1 | chạy `python -m pytest tests/web` (node headless qua `khung_node.py`) | dòng tổng kết có; bài đỏ ghi tên | web headless | node chưa được bộ test gọi ở container |

### 7. Expected artifacts

- `docs/ITL/03_Dev/isp-3.1.1/DUONG_NEN.md` (số đo + lệnh + exit code)
- 2 gói rỗng + 2 hợp đồng tầng
- script dựng `tools/dung_moi_truong_isp.sh`

### 8. Exit criteria

- [ ] S0-B1…B4, S0-F1 chạy được và kết quả THẬT được ghi (bài đỏ có sẵn ≠ lỗi bước này)
- [ ] phép phá thử S0-B3 đã thấy ĐỎ rồi trả nguyên
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** S0-B1, S0-B2, S0-B3, S0-B4, S0-F1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** script dựng môi trường + 2 `__init__.py` + 2 khối hợp đồng `.importlinter`; ⛔ đụng mã nghiệp vụ. Tệp: `tools/dung_moi_truong_isp.sh` · `.importlinter` · `fls/cau_hinh/__init__.py` · `fls/bao_cao/__init__.py` · `docs/ITL/03_Dev/isp-3.1.1/DUONG_NEN.md`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `bash tools/dung_moi_truong_isp.sh`
   - `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`
   - `.venv/bin/python -m pytest `
   - `.venv/bin/lint-imports`
   - `python -m fls.db.pg_migrate`
   - `python tools/do_voi_so_luong.py`
4. **Known limitations:** kho test là cụm cục bộ, ⛔ phải `fls-pg-1` của owner — bước tích hợp cuối chạy lại trên máy owner (O4).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `S0` sang `ready` (phụ thuộc done: —); cần chốt trước: O4. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 0 · S0** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: S0-B1, S0-B2, S0-B3, S0-B4, S0-F1; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 1 · C1 — IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx

**Traceability:** AP v3.1.1 §3.2.1 IX.FX · §3.2.4 dòng 'bảng tỷ giá' · §3.5.3 D1 · AC9.  
**Estimate:** 3–4 giờ · độ tin: trung bình — tuyến GET theo khuôn `bang_tuyen.py` (40 dòng `Tuyen(`); **Dependency:** Step 0 · S0.  
**Ownership:** task `C1` · owner `fls-dev #CF` (BE-CF) · wave W1 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx

### 2. Goal

Gọi `GET /api/fls/v1/config/fx` → `{bang:'IX.FX', nguon, ky:[{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}], thieu:[yyyymm], trung:[yyyymm], lac:[yyyymm]}` trả bảng tỷ giá từ nguồn tĩnh, và tháng thiếu/trùng/lạc hiện ra trong trường riêng thay vì im lặng thành 0.

### 3. Scope

- **Gồm:** `fls/cau_hinh/fx.py`: nạp + kiểm (một dòng/tháng, VND = 1, 5 tiền tệ, thiếu/trùng/lạc); tuyến GET đọc nguồn tĩnh `fls/cau_hinh/tinh/ix_fx_mau.json` (4 tháng TỔNG HỢP, ⛔ số thật); khai tuyến + bảng ở `soi_bang_tuyen`
- **Loại trừ:** kho (C5); ký tháng (C7); ảnh thật (DT2 — C5 nối)
- **Khái niệm mới duy nhất:** miền config `fls/cau_hinh` (nạp + kiểm thuần)
- **Mock/static:** nguồn tĩnh 4 tháng tổng hợp
- **Giới hạn còn lại sau bước:** số trả về là tổng hợp cho tới C5 — FE vẫn dựng được trên hợp đồng

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F4)
- **Backend:** `fls/cau_hinh/fx.py` · `fls/api/xu_ly.py` (+1 hàm) · `fls/api/bang_tuyen.py` (+1 `Tuyen`)
- **DB:** không (tĩnh)
- **Integrations:** không

### 5. Preconditions

- S0 (gói `fls/cau_hinh` + hợp đồng tầng)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C1-B1 | nạp 4 tháng hợp lệ | 4 dòng, VND = 1, `thieu = trung = lac = []` | đơn vị | module chưa có |
| C1-B2 | tháng 202407 có hai dòng | `trung = ['202407']`; ⛔ cộng đôi | đơn vị | — |
| C1-B3 | thiếu 202408 giữa dải | `thieu = ['202408']` | đơn vị | — |
| C1-B4 | GET qua máy chủ thử | 200, đúng hợp đồng; `soi_bang_tuyen` xanh với tuyến mới | API | tuyến chưa có |
| C1-B5 | lint-imports | `fls/cau_hinh` ⛔ import psycopg/repo/db | kiến trúc | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F4)

### 7. Expected artifacts

- `GET /api/fls/v1/config/fx` → `{bang:'IX.FX', nguon, ky:[{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}], thieu:[yyyymm], trung:[yyyymm], lac:[yyyymm]}`
- `fls/cau_hinh/fx.py`
- nguồn tĩnh 4 tháng

### 8. Exit criteria

- [ ] C1-B1…B5 xanh, đỏ trước khi có mã
- [ ] regression `tests/api` xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C1-B1, C1-B2, C1-B3, C1-B4, C1-B5 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** hàm thuần nạp/kiểm + 1 handler + 1 dòng `Tuyen`. Tệp: `fls/cau_hinh/fx.py` · `fls/cau_hinh/tinh/ix_fx_mau.json` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_fx.py` · `tests/api/test_isp_config_fx.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_fx.py tests/api/test_isp_config_fx.py`
   - `python tools/soi_bang_tuyen.py`
   - `.venv/bin/lint-imports`
4. **Known limitations:** số trả về là tổng hợp cho tới C5 — FE vẫn dựng được trên hợp đồng.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C1` sang `ready` (phụ thuộc done: S0). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 1 · C1** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C1-B1, C1-B2, C1-B3, C1-B4, C1-B5; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 2 · H1 — CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD)

**Traceability:** AP v3.1.1 §3.3.1 PD 406 · 412 · §3.5.4 WP-C2 · AC9 (engine đọc config, ⛔ gõ lại).  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 0 · S0.  
**Ownership:** task `H1` · owner `fls-dev #HC` (BE-HC) · wave W1 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD)

### 2. Goal

`tinh_gl(dong, fx)` trả, cho mỗi dòng, Nợ/Có tách theo 5 tiền tệ, bVND = tỷ giá × tiền / 10⁹ và mUSD = bVND ÷ USD × 10³ — đúng tay tính trên 6 dòng tổng hợp.

### 3. Scope

- **Gồm:** `fls/bao_cao/gl.py` thuần; tỷ giá vào bằng THAM SỐ (dict tháng → tiền tệ) — ⛔ đọc kho; tồn luỹ kế theo thứ tự dòng đưa vào (giữ hành vi AS-IS, ghi rõ)
- **Loại trừ:** dữ liệu thật (H4); dòng HR (H7)
- **Khái niệm mới duy nhất:** engine quy đổi GL
- **Mock/static:** 6 dòng tổng hợp + tỷ giá tổng hợp
- **Giới hạn còn lại sau bước:** chưa so với đáp án 406 — H4

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/gl.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- S0 (gói `fls/bao_cao`)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H1-B1 | dòng VND Nợ 2.500.000.000, tỷ giá USD 25.500 | bVND 2,5 · mUSD 98,039… | đơn vị | module chưa có |
| H1-B2 | dòng USD Có | tách đúng cột Có; tồn = tồn trước − Có | đơn vị | — |
| H1-B3 | tháng ⛔ có tỷ giá | ném lỗi có tên (⛔ trả 0 — chính lỗi SUMIFS = 0 của AS-IS) | đơn vị | — |
| H1-B4 | lint-imports | `fls/bao_cao` ⛔ chạm DB | kiến trúc | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/gl.py`

### 8. Exit criteria

- [ ] H1-B1…B4 xanh, đỏ trước khi có mã
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H1-B1, H1-B2, H1-B3, H1-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một hàm thuần + dataclass dòng GL. Tệp: `fls/bao_cao/gl.py` · `tests/bao_cao/test_gl.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_gl.py`
   - `.venv/bin/lint-imports`
4. **Known limitations:** chưa so với đáp án 406 — H4.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H1` sang `ready` (phụ thuộc done: S0). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 2 · H1** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H1-B1, H1-B2, H1-B3, H1-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 3 · F1 — SCR-F09 Đối chiếu · bảng tháng × loại dữ liệu (dữ liệu giả theo hợp đồng C2)

**Traceability:** AP v3.1.1 Figure 2.2 (khuôn lưới = wireframe) · Figure 5.3.3 · §5.2 UF-2 · AC10.  
**Estimate:** 3–4 giờ · độ tin: trung bình — khuôn màn theo `man_f04.js` + `thanh_phan.js` + `tokens.css`; **Dependency:** Step 0 · S0.  
**Ownership:** task `F1` · owner `fls-dev #FE` (FE) · wave W1 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F09 Đối chiếu · bảng tháng × loại dữ liệu (dữ liệu giả theo hợp đồng C2)

### 2. Goal

Mở màn Đối chiếu thấy lưới 23 kỳ × hàng (CÓ · CHẠY · MAP · SỬA) giống Figure 2.2, kỳ đạt HD1 tô xanh, kỳ chưa đạt tô đỏ, từ payload giả đúng hợp đồng C2.

### 3. Scope

- **Gồm:** `fls/web/tep/man_f09.js` + mục điều hướng trong `ung_dung.js`; trạng thái: đang tải · rỗng · lỗi · có dữ liệu; màu chỉ từ token có sẵn (bài `test_khong_ma_mau_go_tay.py`)
- **Loại trừ:** khoan xuống (F3); tuyến thật (F2); HD2 (F6)
- **Khái niệm mới duy nhất:** màn mới SCR-F09
- **Mock/static:** `goi_cua` trả payload giả 3 kỳ trong test
- **Giới hạn còn lại sau bước:** mã màn F09 cần BA đăng ký ở `06_SCREEN_SPEC` (F05–F07 đã dùng/khai tử) — O9

### 4. Components touched

- **Frontend:** `fls/web/tep/man_f09.js` · `ung_dung.js` · `index.html` (+1 mục)
- **Backend:** N/A ở bước này — dữ liệu giả ở biên `goi_cua`; tuyến thật ở F2.
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- S0 (bộ test web chạy được)
- hợp đồng C2 (ghi trong ISP này)
- O9 (fls-ba đăng ký mã SCR-F09)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F1-B1 | N/A — xem lý do ở Components | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F1-F1 | nạp màn với payload 3 kỳ (1 đạt, 2 chưa) | 3 cột kỳ; 1 xanh 2 đỏ; nhãn đơn vị ở đầu hàng (AC3) | DOM headless | màn chưa có |
| F1-F2 | payload rỗng | trạng thái rỗng có chữ, ⛔ lưới trống im | DOM | — |
| F1-F3 | `goi_cua` lỗi 503 | khối lỗi + mã lỗi | DOM | — |
| F1-F4 | bài sẵn có: token màu, một bản mẫu, phím | xanh | hồi quy web | — |

### 7. Expected artifacts

- SCR-F09 (màn)
- `man_f09.js`

### 8. Exit criteria

- [ ] F1-F1…F4 xanh, đỏ trước khi có mã
- [ ] bộ `tests/web` xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F1-F1, F1-F2, F1-F3, F1-F4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một màn + một mục điều hướng. Tệp: `fls/web/tep/man_f09.js` · `fls/web/tep/ung_dung.js` · `fls/web/tep/index.html` · `tests/web/test_isp_f09_bang.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f09_bang.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
   - `.venv/bin/python -m pytest tests/web`
4. **Known limitations:** mã màn F09 cần BA đăng ký ở `06_SCREEN_SPEC` (F05–F07 đã dùng/khai tử) — O9.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F1` sang `ready` (phụ thuộc done: S0); cần chốt trước: O9. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 3 · F1** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F1-F1, F1-F2, F1-F3, F1-F4; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 4 · DT1 — HD1 · phân loại 122 dòng sổ chưa có bản dựng 1-1

**Traceability:** AP v3.1.1 §5.3.1 HD1 ★ · §5.3.2 AC10 · §2.5.3 · Figure 2.2 hàng BANK.  
**Estimate:** 3–4 giờ · độ tin: trung bình — đã đo 16/11 trên ảnh đóng băng: 122 dòng ở 18/23 kỳ; 121/122 có `hd_classifying = Need to manual input`; hd Final: OGA 74 · GI 25 · DEP 8 · ITE 7 · khác 8; **Dependency:** Step 0 · S0.  
**Ownership:** task `DT1` · owner `fls-dev #DATA` (DATA) · wave W1 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

HD1 · phân loại 122 dòng sổ chưa có bản dựng 1-1

### 2. Goal

Mỗi dòng trong 122 dòng sổ AS-IS chưa ghép 1-1 mang đúng một nhãn lý do, và cổng đỏ khi tổng khác 122 hoặc một dòng có 0/≥2 nhãn.

### 3. Scope

- **Gồm:** tool `tools/phan_loai_dong_thieu.py` đọc `itl_ledge_adjustment.json` × `classifying_vs_canon.json` (+ `pm_join.json` cho chiều bank); nhãn lý do theo bảng đóng: `KHONG_CO_SAO_KE` (dòng sổ ⛔ có dòng sao kê) · `KHOA_LECH` (có sao kê nhưng khoá Số CT/tiền/TK/tiền tệ lệch) · `TRUNG_SEQ` · `KHAC` (phải kèm ghi chú); đo luôn chiều ngược: 9.992 − 9.845 = 147 dòng FLS ⛔ có dòng sổ (chỉ ĐẾM + nhãn, ⛔ sửa); ghi `docs/ITL/_tools/phan_loai_dong_thieu.json` (theo `dong_sheet`, ⛔ Diễn giải, ⛔ Số CT)
- **Loại trừ:** sửa mã ghép (BE-HC · H3); ký lý do (owner — O8)
- **Khái niệm mới duy nhất:** phân loại lý do lệch (bảng nhãn đóng)
- **Mock/static:** không — ảnh đóng băng thật đã có trong repo
- **Giới hạn còn lại sau bước:** nhãn `KHOA_LECH` cần trường khoá mà ảnh `itl_ledge_adjustment` ⛔ mang; nếu ảnh thiếu, dòng mang `KHAC · thiếu trường` và bước báo về orchestrator (⛔ đoán)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** `tools/phan_loai_dong_thieu.py` (đọc fixture, ⛔ ghi kho)
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- S0 xong (pytest chạy được)
- ba checksum fixture khớp `MONG` của `do_voi_so_luong.py`

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT1-B1 | chạy tool trên 3 fixture | Σ nhãn = 122; mỗi `dong_sheet` đúng 1 nhãn; chiều ngược = 147 | đơn vị + cổng | tool chưa có |
| DT1-B2 | phá nguồn: bỏ 1 dòng khỏi tập ghép (bản sao tạm) | cổng ĐỎ (123 ≠ 122) rồi trả nguyên (Đ5) | chứng minh đỏ | — |
| DT1-B3 | mẫu số (Đ3) | in mẫu số 9.967 dòng sổ và 9.845 dòng ghép trước khi in tỷ lệ | đơn vị | — |
| DT1-B4 | quét PII trên JSON ra | 0 khoá `dien_giai`/`so_chung_tu`/`email` | riêng tư | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- `phan_loai_dong_thieu.json` (122 + 147 dòng, nhãn, kỳ)
- bảng đếm theo nhãn × kỳ dán vào BG

### 8. Exit criteria

- [ ] DT1-B1…B4 xanh; DT1-B2 đã thấy đỏ
- [ ] bảng đếm theo nhãn có MONG khai trong tool (Đ5)
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT1-B1, DT1-B2, DT1-B3, DT1-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một module tool + bài test `tests/du_lieu/test_phan_loai_dong_thieu.py`. Tệp: `tools/phan_loai_dong_thieu.py` · `tests/du_lieu/test_phan_loai_dong_thieu.py` · `docs/ITL/_tools/phan_loai_dong_thieu.json`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_phan_loai_dong_thieu.py`
   - `python tools/phan_loai_dong_thieu.py --ghi`
4. **Known limitations:** nhãn `KHOA_LECH` cần trường khoá mà ảnh `itl_ledge_adjustment` ⛔ mang; nếu ảnh thiếu, dòng mang `KHAC · thiếu trường` và bước báo về orchestrator (⛔ đoán).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT1` sang `ready` (phụ thuộc done: S0). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 4 · DT1** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT1-B1, DT1-B2, DT1-B3, DT1-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 5 · C2 — GET /parity/months — bảng tháng × loại dữ liệu từ tệp đo

**Traceability:** AP v3.1.1 Figure 2.2 · §5.2 UF-2 · §5.3.2 AC10.  
**Estimate:** 2–4 giờ · độ tin: cao — đọc JSON có sẵn; **Dependency:** Step 0 · S0.  
**Ownership:** task `C2` · owner `fls-dev #CF` (BE-CF) · wave W2 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

GET /parity/months — bảng tháng × loại dữ liệu từ tệp đo

### 2. Goal

Gọi `GET /api/fls/v1/parity/months` → `{nguon, ky:[{ky, co, chay, map_now, map_fls, o_go_that, o_mac_dinh, o_parity, o_parity_khop, hd_parity, hd_parity_khop, dat_hd1}]}` trả đúng 23 kỳ của `voi_so_luong.json`, và `dat_hd1` chỉ đúng khi dòng 100% và ô 100% của kỳ ấy.

### 3. Scope

- **Gồm:** handler đọc tệp đo qua đường dẫn TRUYỀN VÀO (⛔ gõ cứng; như kết nối kho — hợp đồng tầng 7); tính `dat_hd1` = (chay = co) ∧ (o_parity_khop = o_parity)
- **Loại trừ:** đo sống từ kho (O4/HD5 sau); tự sinh theo kỳ (H15)
- **Khái niệm mới duy nhất:** tuyến đọc tệp đo (nguồn đối chiếu)
- **Mock/static:** tệp đo tĩnh `voi_so_luong.json`
- **Giới hạn còn lại sau bước:** số là của ảnh đóng băng 26/08, ⛔ của kho hôm nay

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F2)
- **Backend:** `fls/api/doi_chieu.py` · `xu_ly.py` · `bang_tuyen.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- S0
- `voi_so_luong.json` có trong repo

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C2-B1 | GET | 23 kỳ; Σ co = 9.967; Σ chay = 9.845 | API | tuyến chưa có |
| C2-B2 | kỳ 2024-10 | `dat_hd1 = true` (1 trong 5 kỳ đủ dòng) | API | — |
| C2-B3 | đếm `dat_hd1` | = 5 (đúng AP v3.1.1: 5/23) | API | — |
| C2-B4 | tệp đo vắng | 503 có mã lỗi, ⛔ 200 rỗng (Đ5) | API lỗi | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F2)

### 7. Expected artifacts

- `GET /api/fls/v1/parity/months` → `{nguon, ky:[{ky, co, chay, map_now, map_fls, o_go_that, o_mac_dinh, o_parity, o_parity_khop, hd_parity, hd_parity_khop, dat_hd1}]}`

### 8. Exit criteria

- [ ] C2-B1…B4 xanh
- [ ] `soi_bang_tuyen` xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C2-B1, C2-B2, C2-B3, C2-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 1 module handler + 1 `Tuyen`. Tệp: `fls/api/doi_chieu.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/api/test_isp_parity_months.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/api/test_isp_parity_months.py`
   - `python tools/soi_bang_tuyen.py`
4. **Known limitations:** số là của ảnh đóng băng 26/08, ⛔ của kho hôm nay.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C2` sang `ready` (phụ thuộc done: S0). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 5 · C2** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C2-B1, C2-B2, C2-B3, C2-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 6 · H2 — HD1 · cổng nhận 'lệch có tên lý do và owner ký'

**Traceability:** AP v3.1.1 §5.3.1 HD1 ('Lệch = 0, hoặc mỗi lệch có tên lý do và owner ký') · AC10.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 4 · DT1.  
**Ownership:** task `H2` · owner `fls-dev #HC` (BE-HC) · wave W2 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

HD1 · cổng nhận 'lệch có tên lý do và owner ký'

### 2. Goal

`do_voi_so_luong.py` tính kỳ 'đạt HD1' khi mọi dòng chưa 1-1 của kỳ đều có nhãn DT1 ĐÃ KÝ trong sổ lý do, và nhãn chưa ký vẫn tính là đỏ.

### 3. Scope

- **Gồm:** sổ lý do `docs/ITL/_tools/so_ly_do_hd1.json` (nhãn · số dòng · người ký · ngày) — khởi tạo RỖNG (0 chữ ký); MONG mới: `dat_hd1_theo_ky` khai trước (Đ5)
- **Loại trừ:** ký thật (owner — O8); sửa mã ghép (H3)
- **Khái niệm mới duy nhất:** miễn trừ có chữ ký trong cổng
- **Mock/static:** chữ ký tổng hợp chỉ trong test
- **Giới hạn còn lại sau bước:** khi chưa có chữ ký thật, số kỳ đạt giữ 5/23

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `tools/do_voi_so_luong.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- DT1

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H2-B1 | sổ rỗng | kỳ đạt = 5 (= AP v3.1.1) | cổng | trường mới chưa có |
| H2-B2 | test ký giả nhãn của mọi dòng 2026-07 | 2026-07 thành đạt; tổng 6 | đơn vị | — |
| H2-B3 | nhãn có nhưng chưa ký | vẫn đỏ | đơn vị | — |
| H2-B4 | phá MONG | cổng ĐỎ rồi trả nguyên | chứng minh đỏ | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `so_ly_do_hd1.json` (rỗng)
- trường `dat_hd1` trong `voi_so_luong.json`

### 8. Exit criteria

- [ ] H2-B1…B4 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H2-B1, H2-B2, H2-B3, H2-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** đọc sổ lý do + phán theo kỳ. Tệp: `tools/do_voi_so_luong.py` · `docs/ITL/_tools/voi_so_luong.json` · `tests/oracle/test_do_voi_hd1.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/oracle/test_do_voi_hd1.py`
   - `python tools/do_voi_so_luong.py --ghi`
4. **Known limitations:** khi chưa có chữ ký thật, số kỳ đạt giữ 5/23.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H2` sang `ready` (phụ thuộc done: DT1). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 6 · H2** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H2-B1, H2-B2, H2-B3, H2-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 7 · DT2 — Đường ống đóng băng sheet + ảnh IX.FX (9.2 Exchange Rate)

**Traceability:** AP v3.1.1 §3.2.1 IX.FX · §3.2.4 (bảng tỷ giá gõ cứng) · §3.5.3 D1.  
**Estimate:** 3–4 giờ · độ tin: trung bình — khuôn theo `pm_join.json` (`khong_mang_PII`, `checksum_noi_dung`); **Dependency:** Step 0 · S0.  
**Ownership:** task `DT2` · owner `fls-dev #DATA` (DATA) · wave W2 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Đường ống đóng băng sheet + ảnh IX.FX (9.2 Exchange Rate)

### 2. Goal

Một lệnh biến bản đọc giá trị sheet thành ảnh đóng băng có checksum và cổng; ảnh IX.FX ra đúng 37 dòng 202401→202612 kể cả dòng lạc 202306.

### 3. Scope

- **Gồm:** `tools/dong_bang_sheet.py`: vào = JSON giá trị đọc từ Drive (orchestrator lấy, O7), ra = `tests/fixture/cau_hinh/ix_fx.json` có `nguon`, `ngay_dong_bang`, `khong_mang_PII`, `checksum_noi_dung`; cổng: 37 dòng · khoá `yyyymm` · 5 tiền tệ (USD · SGD · COP · VND = 1 · HKD) · liệt kê tháng trùng/thiếu/lạc (⛔ sửa — ghi đúng như nguồn)
- **Loại trừ:** kiểm nghiệp vụ tỷ giá (BE-CF · C1); đọc Drive trực tiếp từ agent (O7)
- **Khái niệm mới duy nhất:** đường ống đóng băng sheet → fixture có checksum
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ảnh là của MỘT ngày đọc; tháng mới cần lượt đóng băng mới (HD5 ngoài bước này)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** `tools/dong_bang_sheet.py`
- **DB:** không
- **Integrations:** Google Sheets (đọc, qua orchestrator — O7)

### 5. Preconditions

- S0
- O7 chốt cách lấy dữ liệu Drive
- bản đọc thô nằm ở scratchpad orchestrator, ⛔ commit

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT2-B1 | đóng băng từ bản đọc thô | 37 dòng; checksum ổn định qua 2 lần chạy (tất định) | đơn vị | tool chưa có |
| DT2-B2 | bản thô có cột `Email Address` giả lập | tool ĐỎ, ⛔ ghi tệp (PM_COT_RIENG_TU) | riêng tư | — |
| DT2-B3 | bản thô thiếu 1 tháng | ảnh vẫn ghi đúng nguồn + cổng in `thiếu: [yyyymm]` và exit ≠ 0 khi `--mong 37` lệch | cổng | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- `tests/fixture/cau_hinh/ix_fx.json`
- `tools/dong_bang_sheet.py`

### 8. Exit criteria

- [ ] DT2-B1…B3 xanh; cổng đã thấy đỏ
- [ ] ảnh ⛔ mang khoá PII (quét = 0)
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT2-B1, DT2-B2, DT2-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** tool đóng băng tổng quát (cột chọn + khoá + checksum) dùng lại ở DT3…DT11. Tệp: `tools/dong_bang_sheet.py` · `tests/du_lieu/test_dong_bang_sheet.py` · `tests/fixture/cau_hinh/ix_fx.json`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dong_bang_sheet.py`
   - `python tools/dong_bang_sheet.py ix_fx <bản_thô.json> --mong 37`
4. **Known limitations:** ảnh là của MỘT ngày đọc; tháng mới cần lượt đóng băng mới (HD5 ngoài bước này).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT2` sang `ready` (phụ thuộc done: S0); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 7 · DT2** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT2-B1, DT2-B2, DT2-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 8 · C3 — GET /parity/months/{ky}/rows — danh sách dòng chưa 1-1 của một kỳ

**Traceability:** AP v3.1.1 §5.3.2 AC7 (từ ô đỏ tới gói việc một cú bấm) · HD1.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 5 · C2, Step 4 · DT1.  
**Ownership:** task `C3` · owner `fls-dev #CF` (BE-CF) · wave W3 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

GET /parity/months/{ky}/rows — danh sách dòng chưa 1-1 của một kỳ

### 2. Goal

Gọi `GET /api/fls/v1/parity/months/{ky}/rows` → `{ky, dong:[{dong_sheet, nhan, hd_final, chieu:'so→fls'|'fls→so'}], dem_theo_nhan:{…}}` cho kỳ 2026-07 trả đúng 23 dòng sổ chưa 1-1 kèm nhãn lý do của DT1.

### 3. Scope

- **Gồm:** handler đọc `phan_loai_dong_thieu.json`; kỳ sai dạng ⇒ 400; kỳ ⛔ có ⇒ 404
- **Loại trừ:** sửa dòng
- **Khái niệm mới duy nhất:** không (dùng lại khuôn C2)
- **Mock/static:** tệp phân loại tĩnh
- **Giới hạn còn lại sau bước:** chỉ có `dong_sheet`, ⛔ Diễn giải (riêng tư)

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F3)
- **Backend:** `fls/api/doi_chieu.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- C2
- DT1

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C3-B1 | GET 2026-07 | 23 dòng chiều so→fls (đo 16/11) | API | tuyến chưa có |
| C3-B2 | GET 2024-10 | 0 dòng — và trả `mau_so = 6` để phân biệt 'đạt' với 'rỗng' (Đ3) | API | — |
| C3-B3 | GET 2026-13 | 400 | API lỗi | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F3)

### 7. Expected artifacts

- `GET /api/fls/v1/parity/months/{ky}/rows` → `{ky, dong:[{dong_sheet, nhan, hd_final, chieu:'so→fls'|'fls→so'}], dem_theo_nhan:{…}}`

### 8. Exit criteria

- [ ] C3-B1…B3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C3-B1, C3-B2, C3-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** +1 handler +1 `Tuyen`. Tệp: `fls/api/doi_chieu.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/api/test_isp_parity_rows.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/api/test_isp_parity_rows.py`
4. **Known limitations:** chỉ có `dong_sheet`, ⛔ Diễn giải (riêng tư).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C3` sang `ready` (phụ thuộc done: C2, DT1). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 8 · C3** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C3-B1, C3-B2, C3-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 9 · H3 — HD1 · sửa lớp lỗi mã lớn nhất mà DT1 chỉ ra

**Traceability:** AP v3.1.1 §5.3.1 HD1 · AC10 · §4.3.1 SI.MAP.  
**Estimate:** 3–4 giờ · độ tin: thấp — lớp chỉ biết sau DT1; **Dependency:** Step 6 · H2, Step 4 · DT1.  
**Ownership:** task `H3` · owner `fls-dev #HC` (BE-HC) · wave W3 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

HD1 · sửa lớp lỗi mã lớn nhất mà DT1 chỉ ra

### 2. Goal

Số dòng ghép 1-1 tăng đúng bằng số dòng của lớp được sửa (mong khai trước từ DT1), ⛔ dòng đang ghép nào bị mất.

### 3. Scope

- **Gồm:** lớp nhãn `KHOA_LECH` hoặc `TRUNG_SEQ` lớn nhất (theo DT1) — sửa ở chỗ DT1 trỏ (chuẩn hoá khoá / seq); bài hồi quy dùng đúng các `dong_sheet` của lớp
- **Loại trừ:** lớp `KHONG_CO_SAO_KE` (đi đường ký lý do — H2/O8); lớp thứ hai (ISP sửa đổi nếu cần)
- **Khái niệm mới duy nhất:** không (sửa lỗi)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ⚠ DT1 cho 0 dòng 'lỗi mã' ⇒ bước này bị HUỶ bằng bản ISP sửa có lý do (⛔ chạy rỗng)

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/ledger/classifying.py` hoặc `fls/adapters/sao_ke_canon.py` (DT1 trỏ chỗ nào sửa chỗ ấy)
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- DT1 có lớp lỗi mã ≥ 1 dòng
- H2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H3-B1 | bài hồi quy theo `dong_sheet` của lớp | đỏ trước sửa; xanh sau | hồi quy | lỗi đang có |
| H3-B2 | toàn bộ ghép | chay = 9.845 + n (n khai từ DT1); 0 dòng cũ mất | cổng | — |
| H3-B3 | bộ parity cũ | `tests/ledger/test_parity_*` xanh | hồi quy | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- sửa tối thiểu
- MONG `so_dong_ghep_canon` mới

### 8. Exit criteria

- [ ] H3-B1…B3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H3-B1, H3-B2, H3-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** sửa nhỏ nhất tại điểm DT1 chỉ. Tệp: `fls/ledger/classifying.py | fls/adapters/sao_ke_canon.py` · `tools/do_voi_so_luong.py` · `tests/ledger/test_hd1_lop1.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/ledger`
   - `python tools/do_voi_so_luong.py`
4. **Known limitations:** ⚠ DT1 cho 0 dòng 'lỗi mã' ⇒ bước này bị HUỶ bằng bản ISP sửa có lý do (⛔ chạy rỗng).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H3` sang `ready` (phụ thuộc done: H2, DT1). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 9 · H3** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H3-B1, H3-B2, H3-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 10 · F2 — SCR-F09 nối tuyến thật GET /parity/months

**Traceability:** AP v3.1.1 §5.2 UF-2 · AC10.  
**Estimate:** 2–4 giờ · độ tin: cao — khuôn `test_cua_phuc_vu_man_hinh_pg.py`; **Dependency:** Step 3 · F1, Step 5 · C2.  
**Ownership:** task `F2` · owner `fls-dev #FE` (FE) · wave W3 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F09 nối tuyến thật GET /parity/months

### 2. Goal

Chạy máy chủ thử và mở SCR-F09 thấy đúng 23 kỳ, đúng 5 kỳ xanh như `GET /parity/months` trả, ⛔ còn dữ liệu giả.

### 3. Scope

- **Gồm:** `goi_cua` gọi tuyến thật; bài tích hợp qua `fls/web/phuc_vu.py`
- **Loại trừ:** khoan xuống
- **Khái niệm mới duy nhất:** tích hợp API thật cho màn mới
- **Mock/static:** không (tuyến đọc tệp đo tĩnh)
- **Giới hạn còn lại sau bước:** số là của ảnh đóng băng (C2)

### 4. Components touched

- **Frontend:** `man_f09.js`
- **Backend:** tuyến C2 (dùng, ⛔ sửa)
- **DB:** không
- **Integrations:** máy chủ thử `phuc_vu`

### 5. Preconditions

- F1
- C2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F2-B1 | máy chủ thử phục vụ tĩnh + API | 200 cho cả hai | tích hợp | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F2-F1 | mở màn qua máy chủ thử | 23 kỳ; 5 xanh; Σ CÓ = 9.967 ở chân bảng | tích hợp headless | màn còn đọc giả |
| F2-F2 | API trả 503 | khối lỗi; ⛔ hiện số cũ | tích hợp | — |

### 7. Expected artifacts

- SCR-F09 dùng tuyến thật

### 8. Exit criteria

- [ ] F2-F1, F2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F2-B1, F2-F1, F2-F2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** đổi nguồn + bài tích hợp. Tệp: `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_that.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f09_that.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** số là của ảnh đóng băng (C2).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F2` sang `ready` (phụ thuộc done: F1, C2). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 10 · F2** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F2-B1, F2-F1, F2-F2; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 11 · DT3 — Ảnh nguồn IX.HD · IX.ORG: cây ATL 74 dòng + Mapping Master + CDT Correct

**Traceability:** AP v3.1.1 §3.2.1 IX.HD · IX.ORG · §3.2.5 cây HD · §3.5.4 WP-C1.  
**Estimate:** 3–4 giờ · độ tin: trung bình — tool DT2 dùng lại; ba nguồn nhỏ; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT3` · owner `fls-dev #DATA` (DATA) · wave W3 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh nguồn IX.HD · IX.ORG: cây ATL 74 dòng + Mapping Master + CDT Correct

### 2. Goal

Ba ảnh đóng băng mới nạp được và cổng khẳng định: cây ATL 74 dòng · 6 nhóm, Mapping Master 73 mã hd, CDT Correct 18 dòng.

### 3. Scope

- **Gồm:** `tests/fixture/cau_hinh/atl_cay.json` (mã · tên · cha · cấp · nhóm); `mapping_master_cfg.json` (A:B · AA:AD · D:L); `cdt_correct.json` (BR11:BS28)
- **Loại trừ:** kiểm cha–con, chu trình (BE-CF · C4)
- **Khái niệm mới duy nhất:** không (dùng lại đường ống DT2)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** hai định nghĩa dòng PL (ATL ↔ Mapping Master) được đóng băng NGUYÊN, ⛔ hoà giải — C12 xử

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** `tools/dong_bang_sheet.py` (khuôn mới)
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2 xong

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT3-B1 | đóng băng 3 nguồn | 74 · 73 · 18 dòng đúng MONG; 6 nhóm | cổng | ảnh chưa có |
| DT3-B2 | phá: xoá 1 dòng cây ở bản sao | ĐỎ 73 ≠ 74, trả nguyên | chứng minh đỏ | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 3 ảnh trong `tests/fixture/cau_hinh/`

### 8. Exit criteria

- [ ] DT3-B1, DT3-B2 xanh/đỏ đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT3-B1, DT3-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 3 khuôn cột cho tool + 1 bài test. Tệp: `tests/fixture/cau_hinh/*.json` · `tests/du_lieu/test_anh_cau_hinh.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_anh_cau_hinh.py`
4. **Known limitations:** hai định nghĩa dòng PL (ATL ↔ Mapping Master) được đóng băng NGUYÊN, ⛔ hoà giải — C12 xử.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT3` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 11 · DT3** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT3-B1, DT3-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 12 · C4 — IX.HD cây: nạp + kiểm cha–con + GET /config/hd (tĩnh từ ảnh)

**Traceability:** AP v3.1.1 §3.2.1 IX.HD · §3.2.5 · §3.2.4 dòng 'cây HD theo vị trí dòng' · WP-C1.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 11 · DT3.  
**Ownership:** task `C4` · owner `fls-dev #CF` (BE-CF) · wave W4 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.HD cây: nạp + kiểm cha–con + GET /config/hd (tĩnh từ ảnh)

### 2. Goal

Gọi `GET /api/fls/v1/config/hd` trả cây 74 dòng · 6 nhóm từ ảnh ATL, và cây hỏng (cha vắng, chu trình, cấp nhảy) bị từ chối có tên lỗi.

### 3. Scope

- **Gồm:** `fls/cau_hinh/hd.py`: cây + `con_cua()` + `la()`; cha = Σ con là việc của engine (H5), ⛔ ở đây; GET đọc ảnh `atl_cay.json` qua đường dẫn truyền vào
- **Loại trừ:** kho (C5); đối chiếu 73 mã Mapping Master (ghi chênh, ⛔ hoà giải)
- **Khái niệm mới duy nhất:** cây phân cấp có kiểm
- **Mock/static:** ảnh đóng băng thật (tĩnh)
- **Giới hạn còn lại sau bước:** 74 (ATL) ≠ 73 (Mapping Master): trả cả hai số + danh sách chênh

### 4. Components touched

- **Frontend:** N/A — ⛔ có màn cây trong AP v3.1.1; cây được dùng bởi engine H5.
- **Backend:** `fls/cau_hinh/hd.py` · tuyến
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- DT3

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C4-B1 | nạp ảnh ATL | 74 nút, 6 nhóm, gốc đúng, ⛔ chu trình | đơn vị | module chưa có |
| C4-B2 | cây có chu trình A→B→A (tổng hợp) | lỗi `HD_CHU_TRINH` | đơn vị | — |
| C4-B3 | cha vắng | lỗi `HD_CHA_VANG` | đơn vị | — |
| C4-B4 | GET | 200 · 74 · `chenh_mapping_master` liệt kê | API | tuyến chưa có |

**Frontend/UI**

N/A — ⛔ có màn cây trong AP v3.1.1; cây được dùng bởi engine H5.

### 7. Expected artifacts

- `GET /api/fls/v1/config/hd`
- `fls/cau_hinh/hd.py`

### 8. Exit criteria

- [ ] C4-B1…B4 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C4-B1, C4-B2, C4-B3, C4-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module cây + 1 tuyến. Tệp: `fls/cau_hinh/hd.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_hd.py` · `tests/api/test_isp_config_hd.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py`
4. **Known limitations:** 74 (ATL) ≠ 73 (Mapping Master): trả cả hai số + danh sách chênh.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C4` sang `ready` (phụ thuộc done: DT3). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 12 · C4** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C4-B1, C4-B2, C4-B3, C4-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 13 · F3 — SCR-F09 khoan xuống: ô kỳ → danh sách dòng chưa 1-1 (AC7)

**Traceability:** AP v3.1.1 §5.3.2 AC7 · HD1.  
**Estimate:** 3–4 giờ · độ tin: trung bình — ngăn kéo theo `test_drawer_f02.py`; **Dependency:** Step 10 · F2, Step 8 · C3.  
**Ownership:** task `F3` · owner `fls-dev #FE` (FE) · wave W4 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F09 khoan xuống: ô kỳ → danh sách dòng chưa 1-1 (AC7)

### 2. Goal

Bấm ô kỳ đỏ 2026-07 mở ngăn kéo liệt kê 23 dòng chưa 1-1 kèm nhãn lý do và đường dẫn tới hộp/gói việc của AP, trong một cú bấm.

### 3. Scope

- **Gồm:** ngăn kéo + phím Esc đóng + Enter mở (bài phím sẵn có); nhãn lý do tiếng Việt, ⛔ Diễn giải
- **Loại trừ:** sửa dòng
- **Khái niệm mới duy nhất:** điều hướng khoan xuống
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** kỳ đạt hiển thị 'đạt · mẫu số N' (Đ3)

### 4. Components touched

- **Frontend:** `man_f09.js`
- **Backend:** tuyến C3 (dùng)
- **DB:** không
- **Integrations:** máy chủ thử

### 5. Preconditions

- F2
- C3

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F3-B1 | N/A — tuyến C3 đã có bài API | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F3-F1 | bấm 2026-07 | 23 dòng; đếm theo nhãn khớp `dem_theo_nhan` | tích hợp headless | chưa có |
| F3-F2 | bấm 2024-10 | 'đạt · mẫu số 6' | DOM | — |
| F3-F3 | phím Esc | ngăn kéo đóng, focus về ô | phím | — |

### 7. Expected artifacts

- ngăn kéo SCR-F09

### 8. Exit criteria

- [ ] F3-F1…F3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F3-F1, F3-F2, F3-F3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** ngăn kéo + gọi tuyến. Tệp: `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_khoan.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f09_khoan.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** kỳ đạt hiển thị 'đạt · mẫu số N' (Đ3).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F3` sang `ready` (phụ thuộc done: F2, C3). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 13 · F3** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F3-F1, F3-F2, F3-F3; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 14 · DT4 — Ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT)

**Traceability:** AP v3.1.1 §3.3.1 PD 406 · §3.5.4 WP-C2 · HD2.  
**Estimate:** 3–4 giờ · độ tin: thấp–trung bình — bảng lớn (cỡ 10⁴ dòng); rủi ro hết giờ đọc (GAP-ORA-08) ⇒ đọc theo lát kỳ; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT4` · owner `fls-dev #DATA` (DATA) · wave W4 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT)

### 2. Goal

Đáp án 406 đóng băng theo dòng × kỳ cho cột BM–BT, bỏ Diễn giải/Số CT, cổng khẳng định số dòng mỗi kỳ bằng số dòng sổ cùng kỳ.

### 3. Scope

- **Gồm:** `tests/fixture/dap_an/gl_406.json`: khoá dòng (`dong_sheet`), kỳ, BM–BT (tiền theo 5 tiền tệ, bVND, mUSD); đọc theo lát kỳ; lát hỏng = ĐỎ (⛔ 'không thấy lệch')
- **Loại trừ:** tính lại GL (BE-HC · H1/H4)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** tồn luỹ kế AS-IS phụ thuộc thứ tự dòng (AP §3.3.1) — ảnh giữ NGUYÊN thứ tự dòng để H4 tái hiện

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2
- O7

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT4-B1 | đóng băng mọi lát kỳ | Σ dòng theo kỳ = phân bố kỳ của `itl_ledge_adjustment.json` (hoặc lệch có tên) | cổng | ảnh chưa có |
| DT4-B2 | một lát trả rỗng | ĐỎ (Đ3: mẫu số 0 là kết quả) | chứng minh đỏ | — |
| DT4-B3 | quét PII | 0 cột Diễn giải/Số CT | riêng tư | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- `gl_406.json`

### 8. Exit criteria

- [ ] DT4-B1…B3 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT4-B1, DT4-B2, DT4-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** khuôn cột 406 + đọc theo lát. Tệp: `tests/fixture/dap_an/gl_406.json` · `tests/du_lieu/test_dap_an_406.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_406.py`
4. **Known limitations:** tồn luỹ kế AS-IS phụ thuộc thứ tự dòng (AP §3.3.1) — ảnh giữ NGUYÊN thứ tự dòng để H4 tái hiện.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT4` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 14 · DT4** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT4-B1, DT4-B2, DT4-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 15 · C5 — Kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho

**Traceability:** AP v3.1.1 §3.2.3 IX.TMP ('snapshot có version') · §3.5.3 D1 · AP Q4 (PostgreSQL trước) · INV-I08 (chỉ-thêm).  
**Estimate:** 3–4 giờ · độ tin: trung bình — di trú + trigger theo khuôn 0015/INV-I03; **Dependency:** Step 12 · C4, Step 7 · DT2.  
**Ownership:** task `C5` · owner `fls-dev #CF` (BE-CF) · wave W5 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho

### 2. Goal

Hai tuyến /config/fx và /config/hd trả số từ kho; mọi UPDATE/DELETE trên bảng config bị trigger chặn, và một lần nạp lại tạo phiên bản mới thay vì ghi đè.

### 3. Scope

- **Gồm:** 0027: `fls_cau_hinh_ban` (bang · phien_ban · nguon · checksum · actor · luc) + `fls_cau_hinh_dong` (ban_id · khoa · gia_tri jsonb) — chỉ-thêm (O5); `fls/repo/cau_hinh_repo.py`: nạp ảnh → phiên bản mới; đọc phiên bản mới nhất; C1/C4 đổi nguồn từ tĩnh sang kho; GỠ `fls/cau_hinh/tinh/ix_fx_mau.json`; sinh lại hiện vật ERD/golden (CLAUDE.md §Cổng)
- **Loại trừ:** ký (C7); bảng config khác (C6, C8…)
- **Khái niệm mới duy nhất:** lưu kho (persistence) config
- **Mock/static:** không — kho test PG
- **Giới hạn còn lại sau bước:** kho test cục bộ (O4)

### 4. Components touched

- **Frontend:** N/A — hợp đồng tuyến ⛔ đổi; F4 dùng lại nguyên.
- **Backend:** `fls/repo/cau_hinh_repo.py` · handler C1/C4
- **DB:** `0027_cau_hinh_chi_them.sql` · trigger chặn UPDATE/DELETE
- **Integrations:** không

### 5. Preconditions

- C4
- DT2 (ảnh FX thật)
- S0 (kho test)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C5-B1 | nạp `ix_fx.json` thật | phiên bản 1; GET trả 37 dòng; `lac = ['202306']` | tích hợp DB (pg) | bảng chưa có |
| C5-B2 | nạp lại cùng ảnh | phiên bản 2, checksum trùng ⇒ ghi `khong_doi = true`, ⛔ ghi đè | pg | — |
| C5-B3 | UPDATE một dòng | trigger ĐỎ có tên | pg | — |
| C5-B4 | golden DDL + `pg_verify` | xanh sau `--update-golden` có chủ đích | pg | — |

**Frontend/UI**

N/A — hợp đồng tuyến ⛔ đổi; F4 dùng lại nguyên.

### 7. Expected artifacts

- di trú 0027
- `cau_hinh_repo.py`
- ERD/golden sinh lại

### 8. Exit criteria

- [ ] C5-B1…B4 xanh
- [ ] bộ `tests/db` xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C5-B1, C5-B2, C5-B3, C5-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 1 di trú + 1 repo + đổi nguồn 2 handler. Tệp: `fls/db/migrations/0027_cau_hinh_chi_them.sql` · `fls/db/schema.py` · `fls/repo/cau_hinh_repo.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_kho_cau_hinh_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`
   - `python -m fls.db.pg_migrate`
   - `.venv/bin/python -m pytest tests/cau_hinh/test_kho_cau_hinh_pg.py tests/db`
   - `python -m fls.db.erd_export --write`
4. **Known limitations:** kho test cục bộ (O4).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C5` sang `ready` (phụ thuộc done: C4, DT2). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 15 · C5** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C5-B1, C5-B2, C5-B3, C5-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 16 · H4 — KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên)

**Traceability:** AP v3.1.1 §3.5.4 WP-C2 (cổng 'từng ô BM–BT khớp, mọi tháng') · §5.3.1 HD2.  
**Estimate:** 3–4 giờ · độ tin: trung bình — dùng lại `fls/oracle/cong_parity.py`; **Dependency:** Step 2 · H1, Step 14 · DT4, Step 7 · DT2, Step 1 · C1.  
**Ownership:** task `H4` · owner `fls-dev #HC` (BE-HC) · wave W5 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên)

### 2. Goal

`tools/do_hd2.py --goi WP-C2` so từng ô BM–BT của CA.GL với đáp án 406 ở mọi kỳ có dữ liệu, ghi `hd2_cong.json`, và ĐỎ khi 0 ô hoặc có lát bị bỏ.

### 3. Scope

- **Gồm:** tool chạy H1 trên dòng sổ + `ix_fx.json` (qua `fls/cau_hinh/fx.py`); phân xử bằng `cong_parity.PhanXu` (≥ 1 ô, ⛔ lát bỏ, 0 lệch); khai hợp đồng `hd2_cong.json` cho C14
- **Loại trừ:** đọc tỷ giá từ kho (I2)
- **Khái niệm mới duy nhất:** đối chiếu với đáp án thật (oracle) cho engine
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** tỷ giá đọc từ ảnh, ⛔ từ kho ký — I2 nối

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `tools/do_hd2.py` · `fls/bao_cao/gl.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H1
- DT4
- DT2
- C1 (`fls/cau_hinh/fx.py`)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H4-B1 | chạy WP-C2 | số ô so > 0 và = số ô của đáp án; lệch được liệt kê theo (kỳ, dòng, cột) | cổng | tool chưa có |
| H4-B2 | đáp án rỗng | ĐỎ `0 ô` (Đ3) | chứng minh đỏ | — |
| H4-B3 | MONG lệch khai trước | khác ⇒ ĐỎ cả hai chiều (Đ5) | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `tools/do_hd2.py`
- `docs/ITL/_tools/hd2_cong.json` (WP-C2)

### 8. Exit criteria

- [ ] H4-B1…B3 đúng
- [ ] lệch còn lại (nếu có) mỗi cái có tên lý do trong JSON
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H4-B1, H4-B2, H4-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** tool cổng + nối engine. Tệp: `tools/do_hd2.py` · `docs/ITL/_tools/hd2_cong.json` · `tests/oracle/test_do_hd2_ca.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/oracle/test_do_hd2_ca.py`
   - `python tools/do_hd2.py --goi WP-C2 --ghi`
4. **Known limitations:** tỷ giá đọc từ ảnh, ⛔ từ kho ký — I2 nối.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H4` sang `ready` (phụ thuộc done: H1, DT4, DT2, C1). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 16 · H4** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H4-B1, H4-B2, H4-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 17 · DT5 — Ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M

**Traceability:** AP v3.1.1 §3.3.1 PD 409–411 · §3.5.4 WP-C3.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 11 · DT3.  
**Ownership:** task `DT5` · owner `fls-dev #DATA` (DATA) · wave W5 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M

### 2. Goal

Đáp án CFA1 theo (HD, ngày) và theo Y/H/Q/M đóng băng; cổng khẳng định mọi hàng có mã HD nằm trong cây ATL 74 dòng.

### 3. Scope

- **Gồm:** `dap_an/cfa1_daily.json` (HD × ngày); `dap_an/cfa1_yhqm.json` (HD × kỳ Y/H/Q/M)
- **Loại trừ:** CFA3/PLA (D6a, D6b)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ô công thức lỗi ở nguồn (#REF!, #N/A) được ghi nguyên dạng chuỗi, ⛔ đổi thành 0

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT3 (cây để kiểm mã HD)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT5-B1 | đóng băng | mọi mã HD ∈ cây ATL; số cột ngày = số ngày từ 21/10/2024 tới ngày đọc | cổng | ảnh chưa có |
| DT5-B2 | phá: đổi 1 mã HD lạ | ĐỎ, trả nguyên | chứng minh đỏ | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 2 ảnh đáp án

### 8. Exit criteria

- [ ] DT5-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT5-B1, DT5-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 2 khuôn cột + test. Tệp: `tests/fixture/dap_an/cfa1_*.json` · `tests/du_lieu/test_dap_an_cfa1.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_cfa1.py`
4. **Known limitations:** ô công thức lỗi ở nguồn (#REF!, #N/A) được ghi nguyên dạng chuỗi, ⛔ đổi thành 0.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT5` sang `ready` (phụ thuộc done: DT3); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 17 · DT5** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT5-B1, DT5-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 18 · C6 — IX.PER: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4)

**Traceability:** AP v3.1.1 §3.2.1 IX.PER · §3.2.4 dòng 'ngày đầu cột… năm ép 2025' · D4.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 15 · C5.  
**Ownership:** task `C6` · owner `fls-dev #CF` (BE-CF) · wave W6 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.PER: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4)

### 2. Goal

`kỳ_của(ngày)` trả Y/H/Q/M đúng năm của chính dữ liệu (⛔ ép 2025), ngày đầu cột đọc từ config (21/10/2024), luật ghi nhận = 'dồn ngày 1 tháng PL start' (D4 A).

### 3. Scope

- **Gồm:** `fls/cau_hinh/ky.py` + dòng config IX.PER trong kho (phiên bản); GET /config/per
- **Loại trừ:** chia đều PL start→end (D4 B — sau khi owner ký)
- **Khái niệm mới duy nhất:** lịch kỳ có cấu hình
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** chỉ luật A hoạt động; luật B bị từ chối có tên `LUAT_CHUA_KY`

### 4. Components touched

- **Frontend:** N/A — ⛔ có màn kỳ trong AP; engine H6 tiêu thụ.
- **Backend:** `fls/cau_hinh/ky.py` · tuyến
- **DB:** dòng config qua 0027 (⛔ di trú mới)
- **Integrations:** không

### 5. Preconditions

- C5

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C6-B1 | ngày 2026-11-05 | Y2026 · H2 · Q4 · M11 (⛔ 2025) | đơn vị | module chưa có |
| C6-B2 | ngày 2024-12-31 | Y2024 (bản AS-IS ép T11/T12 → 2024 — giữ đúng dữ liệu) | đơn vị | — |
| C6-B3 | chọn luật B | lỗi `LUAT_CHUA_KY` | đơn vị | — |
| C6-B4 | GET /config/per | 200 · ngày đầu 2024-10-21 · luật A | API | — |

**Frontend/UI**

N/A — ⛔ có màn kỳ trong AP; engine H6 tiêu thụ.

### 7. Expected artifacts

- `fls/cau_hinh/ky.py`
- `GET /api/fls/v1/config/per`

### 8. Exit criteria

- [ ] C6-B1…B4 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C6-B1, C6-B2, C6-B3, C6-B4 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module lịch + nạp dòng config + 1 tuyến. Tệp: `fls/cau_hinh/ky.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_ky.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_ky.py`
4. **Known limitations:** chỉ luật A hoạt động; luật B bị từ chối có tên `LUAT_CHUA_KY`.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C6` sang `ready` (phụ thuộc done: C5). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 18 · C6** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C6-B1, C6-B2, C6-B3, C6-B4; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 19 · H5 — SO.CFA1 Daily: Σ theo (HD, ngày) trên cây IX.HD

**Traceability:** AP v3.1.1 §3.3.1 PD 409 · §3.2.4 dòng 'cây HD theo vị trí dòng, cha = SUM con' · WP-C3.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 16 · H4, Step 12 · C4, Step 17 · DT5.  
**Ownership:** task `H5` · owner `fls-dev #HC` (BE-HC) · wave W6 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SO.CFA1 Daily: Σ theo (HD, ngày) trên cây IX.HD

### 2. Goal

`cfa1_daily(gl, cay)` trả ô lá = Σ mUSD Nợ − Σ mUSD Có theo (HD Final, ngày) và ô cha = Σ con theo cây; cổng WP-C3a khớp đáp án 409 từng ô.

### 3. Scope

- **Gồm:** `fls/bao_cao/cfa.py`; `do_hd2.py --goi WP-C3a`
- **Loại trừ:** Y/H/Q/M (H6); HR (H7)
- **Khái niệm mới duy nhất:** tổng hợp theo cây (cha = Σ con do engine)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** cột ngày bắt đầu 21/10/2024 lấy tạm từ tham số tới khi H6 đọc IX.PER

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/cfa.py` · `tools/do_hd2.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H4
- C4 (`fls/cau_hinh/hd.py`)
- DT5

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H5-B1 | cây 3 nút tổng hợp | cha = Σ hai con | đơn vị | chưa có |
| H5-B2 | WP-C3a trên đáp án 409 | ô so > 0; lệch có MONG | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/cfa.py`
- `hd2_cong.json` + WP-C3a

### 8. Exit criteria

- [ ] H5-B1, B2 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H5-B1, H5-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** hàm tổng hợp + nối cổng. Tệp: `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cfa1.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_cfa1.py`
   - `python tools/do_hd2.py --goi WP-C3a`
4. **Known limitations:** cột ngày bắt đầu 21/10/2024 lấy tạm từ tham số tới khi H6 đọc IX.PER.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H5` sang `ready` (phụ thuộc done: H4, C4, DT5). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 19 · H5** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H5-B1, H5-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 20 · F4 — SCR-F08 Cấu hình · bảng IX.FX chỉ đọc trên tuyến thật

**Traceability:** AP v3.1.1 §3.2.1 IX.FX · §3.2.4 · §3.5.3 D1.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 3 · F1, Step 15 · C5.  
**Ownership:** task `F4` · owner `fls-dev #FE` (FE) · wave W6 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F08 Cấu hình · bảng IX.FX chỉ đọc trên tuyến thật

### 2. Goal

Mở màn Cấu hình thấy bảng tỷ giá theo tháng từ `GET /config/fx`, tháng thiếu/trùng/lạc mang nhãn riêng (CHẶN · TRÙNG · LẠC).

### 3. Scope

- **Gồm:** `man_f08.js` + mục điều hướng; đọc tuyến thật (kho — C5)
- **Loại trừ:** ký (F5)
- **Khái niệm mới duy nhất:** màn mới SCR-F08
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** mã F08 cần BA đăng ký (O9)

### 4. Components touched

- **Frontend:** `fls/web/tep/man_f08.js` · `ung_dung.js`
- **Backend:** tuyến C1/C5 (dùng)
- **DB:** kho test (C5)
- **Integrations:** máy chủ thử

### 5. Preconditions

- C5
- F1 (khuôn màn)
- O9 (fls-ba đăng ký mã SCR-F08)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F4-B1 | N/A — tuyến có bài ở C1/C5 | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F4-F1 | mở màn trên kho có ảnh FX | 37 dòng; 202306 nhãn LẠC | tích hợp headless (pg) | chưa có |
| F4-F2 | kho thiếu 202408 (dữ liệu test) | nhãn CHẶN ở 202408 | tích hợp | — |
| F4-F3 | token màu + bản mẫu | xanh | hồi quy | — |

### 7. Expected artifacts

- SCR-F08

### 8. Exit criteria

- [ ] F4-F1…F3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F4-F1, F4-F2, F4-F3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một màn. Tệp: `fls/web/tep/man_f08.js` · `fls/web/tep/ung_dung.js` · `tests/web/test_isp_f08_fx_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f08_fx_pg.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** mã F08 cần BA đăng ký (O9).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F4` sang `ready` (phụ thuộc done: F1, C5); cần chốt trước: O9. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 20 · F4** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F4-F1, F4-F2, F4-F3; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 21 · DT8 — Ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI

**Traceability:** AP v3.1.1 §3.2.2 IX.VEN · §3.4.1 PD 503–507 · §3.5.4 WP-C4.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT8` · owner `fls-dev #DATA` (DATA) · wave W6 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI

### 2. Goal

Ảnh Vendor & Network Block 1 (36 dòng × 7 CDT1) và MID1–MID3 của GI đóng băng; cổng khẳng định Σ chia của MID3 = O / P trên chính đáp án.

### 3. Scope

- **Gồm:** `cau_hinh/ix_ven.json` (36 dòng, cột 'cách tính' cho VD341 · VD444 · VD428 · 'Max' · VD62); `dap_an/gi_mid1.json` · `gi_mid2.json` · `gi_mid3.json`
- **Loại trừ:** OMC · SC · PS (DT9)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** U3 #REF! ở nguồn được ghi nguyên

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT8-B1 | đóng băng | 36 dòng Block 1; 5 vendor có 'cách tính' ≠ thường | cổng | ảnh chưa có |
| DT8-B2 | tự kiểm Σ chia MID3 = O/P | số Vendor-tháng lệch có MONG | cổng | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 4 ảnh

### 8. Exit criteria

- [ ] DT8-B1, B2 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT8-B1, DT8-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 4 khuôn cột + test. Tệp: `tests/fixture/cau_hinh/ix_ven.json` · `tests/fixture/dap_an/gi_mid*.json` · `tests/du_lieu/test_dap_an_gi.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_gi.py`
4. **Known limitations:** U3 #REF! ở nguồn được ghi nguyên.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT8` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 21 · DT8** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT8-B1, DT8-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 22 · C9 — IX.VEN: vendor · network · CDT1 + cột 'cách tính'

**Traceability:** AP v3.1.1 §3.2.2 IX.VEN · §3.2.4 dòng 'VD341 · VD444…'.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 15 · C5, Step 21 · DT8.  
**Ownership:** task `C9` · owner `fls-dev #CF` (BE-CF) · wave W7 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.VEN: vendor · network · CDT1 + cột 'cách tính'

### 2. Goal

`GET /api/fls/v1/config/ven` trả 36 dòng Block 1 từ kho, và 5 vendor VD341 · VD444 · VD428 · 'Max' · VD62 mang mã 'cách tính' riêng thay vì nằm trong công thức.

### 3. Scope

- **Gồm:** `fls/cau_hinh/vendor.py` + nạp ảnh `ix_ven.json`; tuyến GET
- **Loại trừ:** phép tính riêng (H10)
- **Khái niệm mới duy nhất:** không (bảng config theo khuôn C5)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** mã 'cách tính' chỉ là NHÃN; phép tính ở H10

### 4. Components touched

- **Frontend:** N/A — ⛔ màn trong AP; engine H9/H10 tiêu thụ.
- **Backend:** `fls/cau_hinh/vendor.py` · tuyến
- **DB:** dòng config 0027
- **Integrations:** không

### 5. Preconditions

- C5
- DT8

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C9-B1 | nạp | 36 dòng; 5 mã đặc biệt; product_id → CDT1 đủ 7 CDT1 | pg | chưa có |
| C9-B2 | vendor trùng khoá | lỗi có tên | đơn vị | — |

**Frontend/UI**

N/A — ⛔ màn trong AP; engine H9/H10 tiêu thụ.

### 7. Expected artifacts

- `GET /api/fls/v1/config/ven`

### 8. Exit criteria

- [ ] C9-B1, B2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C9-B1, C9-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module + tuyến. Tệp: `fls/cau_hinh/vendor.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_vendor_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_vendor_pg.py`
4. **Known limitations:** mã 'cách tính' chỉ là NHÃN; phép tính ở H10.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C9` sang `ready` (phụ thuộc done: C5, DT8). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 22 · C9** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C9-B1, C9-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 23 · H6 — SO Y/H/Q/M theo IX.PER

**Traceability:** AP v3.1.1 §3.3.1 PD 410 · 411 · IX.PER.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 19 · H5, Step 18 · C6.  
**Ownership:** task `H6` · owner `fls-dev #HC` (BE-HC) · wave W7 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SO Y/H/Q/M theo IX.PER

### 2. Goal

`cuon_ky(daily, per)` cuộn Daily thành Y/H/Q/M dùng lịch IX.PER (năm từ dữ liệu); cổng WP-C3b khớp đáp án 410 · 411.

### 3. Scope

- **Gồm:** `fls/bao_cao/cfa.py` (+cuộn); bỏ tham số ngày đầu tạm của H5 — đọc IX.PER
- **Loại trừ:** PLA
- **Khái niệm mới duy nhất:** cuộn kỳ
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** —

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/cfa.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H5
- C6

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H6-B1 | Daily 2 ngày T11/2024 tổng hợp | Y2024 (⛔ 2025) | đơn vị | chưa có |
| H6-B2 | WP-C3b | lệch có MONG | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- WP-C3b trong `hd2_cong.json`

### 8. Exit criteria

- [ ] H6-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H6-B1, H6-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** +1 hàm cuộn. Tệp: `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cuon_ky.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_cuon_ky.py`
4. **Known limitations:** —.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H6` sang `ready` (phụ thuộc done: H5, C6). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 23 · H6** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H6-B1, H6-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 24 · DT6 — Ảnh đáp án GL HR + CFA3 (407 · 408 · 412 · 413)

**Traceability:** AP v3.1.1 §3.3.1 PD 401–404 · 407 · 408 · 412 · 413 · Q3 (HR ⛔ qua ALLOCATE).  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT6` · owner `fls-dev #DATA` (DATA) · wave W7 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án GL HR + CFA3 (407 · 408 · 412 · 413)

### 2. Goal

Đáp án GL HR và CFA3 đóng băng; cổng khẳng định chỉ có kỳ của Y2025 (AS-IS chỉ có sheet Y2025) và in rõ điều đó.

### 3. Scope

- **Gồm:** `dap_an/gl_hr.json`; `dap_an/cfa3.json`
- **Loại trừ:** PLA1/PLA3 (DT7)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** H1000 Y2024 đi bằng IMPORTRANGE — nếu đọc ⛔ được, ghi `thiếu Y2024` (⛔ suy)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT6-B1 | đóng băng | kỳ ⊂ 2025; số dòng theo kỳ có MONG | cổng | ảnh chưa có |
| DT6-B2 | quét PII (HR có tên người) | 0 cột tên/email; chỉ mã nhân sự băm hoặc bỏ | riêng tư | — |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 2 ảnh

### 8. Exit criteria

- [ ] DT6-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT6-B1, DT6-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 2 khuôn cột + test. Tệp: `tests/fixture/dap_an/gl_hr.json` · `tests/fixture/dap_an/cfa3.json` · `tests/du_lieu/test_dap_an_hr.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_hr.py`
4. **Known limitations:** H1000 Y2024 đi bằng IMPORTRANGE — nếu đọc ⛔ được, ghi `thiếu Y2024` (⛔ suy).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT6` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 24 · DT6** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT6-B1, DT6-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 25 · C8 — IX.ORG: LE · TK → CDT1 + CDT lạ vào hàng chờ (⛔ rơi về SHQ2)

**Traceability:** AP v3.1.1 §3.2.1 IX.ORG · §3.2.4 dòng 'CDT Correct… mặc định SHQ2'.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 15 · C5, Step 11 · DT3.  
**Ownership:** task `C8` · owner `fls-dev #CF` (BE-CF) · wave W8 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.ORG: LE · TK → CDT1 + CDT lạ vào hàng chờ (⛔ rơi về SHQ2)

### 2. Goal

`cdt_cua(tk)` trả CDT1 từ IX.ORG; CDT ⛔ có trong CDT Correct sinh một sự kiện hàng chờ thấy được qua `GET /api/fls/v1/queue` hiện có, thay vì mặc định SHQ2 im lặng.

### 3. Scope

- **Gồm:** `fls/cau_hinh/to_chuc.py` + nạp ảnh `mapping_master_cfg.json`, `cdt_correct.json` vào kho (0027); CDT lạ → `fls_queue_event` (bảng có sẵn) loại `CDT_LA`
- **Loại trừ:** màn mới (hàng chờ hiện có hiển thị)
- **Khái niệm mới duy nhất:** hàng chờ cho giá trị config lạ
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** 8 CDT1 · 18 dòng CDT Correct là của ảnh đóng băng

### 4. Components touched

- **Frontend:** N/A — màn hàng chờ hiện có đọc `GET /queue`; ⛔ màn mới.
- **Backend:** `fls/cau_hinh/to_chuc.py` · repo
- **DB:** `fls_queue_event` (có sẵn) + dòng config 0027
- **Integrations:** không

### 5. Preconditions

- C5
- DT3

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C8-B1 | TK có trong Mapping Master | CDT1 đúng; 0 sự kiện | đơn vị | module chưa có |
| C8-B2 | CDT 'XYZ' lạ | 1 sự kiện `CDT_LA` thấy ở `GET /queue`; ⛔ trả SHQ2 | pg | — |

**Frontend/UI**

N/A — màn hàng chờ hiện có đọc `GET /queue`; ⛔ màn mới.

### 7. Expected artifacts

- `fls/cau_hinh/to_chuc.py`

### 8. Exit criteria

- [ ] C8-B1, B2 xanh
- [ ] regression `tests/api/test_cua_lenh_cho_pg.py` xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C8-B1, C8-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module tổ chức + ghi hàng chờ. Tệp: `fls/cau_hinh/to_chuc.py` · `fls/repo/cau_hinh_repo.py` · `tests/cau_hinh/test_to_chuc_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_to_chuc_pg.py tests/api/test_cua_lenh_cho_pg.py`
4. **Known limitations:** 8 CDT1 · 18 dòng CDT Correct là của ảnh đóng băng.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C8` sang `ready` (phụ thuộc done: C5, DT3). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 25 · C8** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C8-B1, C8-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 26 · H9 — AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P)

**Traceability:** AP v3.1.1 §3.4.1 PD 501–507 · §3.5.4 WP-C4.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 16 · H4, Step 22 · C9, Step 21 · DT8.  
**Ownership:** task `H9` · owner `fls-dev #HC` (BE-HC) · wave W8 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P)

### 2. Goal

`chia_nen_tang(pe, o, p, ven)` chia theo RATE = PE của CDT1 ÷ Σ PE 6 CDT1 theo Vendor-tháng (O = 0 ∧ P > 0 ⇒ theo tổng tháng), Σ chia = O/P từng Vendor-tháng; cổng WP-C4a khớp MID3 GI cho vendor thường.

### 3. Scope

- **Gồm:** `fls/bao_cao/phan_bo.py`; KS.AL: Σ chia ≠ tiền ⇒ lỗi có tên
- **Loại trừ:** 5 vendor đặc biệt (H10)
- **Khái niệm mới duy nhất:** phân bổ nền tảng theo tỷ lệ
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** vendor đặc biệt bị bỏ qua có ĐẾM (⛔ im)

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/phan_bo.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H4
- C9
- DT8

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H9-B1 | Vendor-tháng 6 CDT1 tổng hợp | Σ chia = O; RATE đúng | đơn vị | chưa có |
| H9-B2 | O = 0, P > 0 | chia theo tổng tháng | đơn vị | — |
| H9-B3 | WP-C4a | lệch có MONG; số vendor bỏ qua = 5 mã | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/phan_bo.py`
- WP-C4a

### 8. Exit criteria

- [ ] H9-B1…B3 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H9-B1, H9-B2, H9-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module phân bổ. Tệp: `fls/bao_cao/phan_bo.py` · `tools/do_hd2.py` · `tests/bao_cao/test_phan_bo.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_phan_bo.py`
4. **Known limitations:** vendor đặc biệt bị bỏ qua có ĐẾM (⛔ im).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H9` sang `ready` (phụ thuộc done: H4, C9, DT8). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 26 · H9** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H9-B1, H9-B2, H9-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 27 · DT10 — Ảnh IX.DRV (Allocation Table) + đáp án ATL (604 · 606)

**Traceability:** AP v3.1.1 §3.2.2 IX.DRV · §3.4.2 PD 500 · 511–513 · 604.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT10` · owner `fls-dev #DATA` (DATA) · wave W8 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh IX.DRV (Allocation Table) + đáp án ATL (604 · 606)

### 2. Goal

Driver theo (driver, CDT1, tháng) và ATL đóng băng; cổng khẳng định driver chỉ có 2025 (AP đo) và NOEM trỏ ô cứng của H1000 được ghi nguồn.

### 3. Scope

- **Gồm:** `cau_hinh/ix_drv.json` (NOEM · GI theo PE · GI theo PM · NB theo LE); `dap_an/atl.json` (604 · 606)
- **Loại trừ:** engine AL.KEY (H12)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** driver 2026 ⛔ có ở nguồn ⇒ ATL 2026 chỉ đối chiếu được khi cờ tắt (D2)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT10-B1 | đóng băng | driver: 4 loại × 8 CDT1 × 12 tháng 2025 (hoặc lệch có tên) | cổng | ảnh chưa có |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 2 ảnh

### 8. Exit criteria

- [ ] DT10-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT10-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 2 khuôn cột + test. Tệp: `tests/fixture/cau_hinh/ix_drv.json` · `tests/fixture/dap_an/atl.json` · `tests/du_lieu/test_dap_an_atl.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_atl.py`
4. **Known limitations:** driver 2026 ⛔ có ở nguồn ⇒ ATL 2026 chỉ đối chiếu được khi cờ tắt (D2).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT10` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 27 · DT10** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT10-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 28 · C10 — IX.DRV: driver theo (driver, CDT1, tháng)

**Traceability:** AP v3.1.1 §3.2.2 IX.DRV · §3.2.4 dòng 'headcount NOEM lấy ô cứng'.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 15 · C5, Step 27 · DT10.  
**Ownership:** task `C10` · owner `fls-dev #CF` (BE-CF) · wave W9 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.DRV: driver theo (driver, CDT1, tháng)

### 2. Goal

`driver_cua(loai, cdt1, thang)` trả giá trị từ kho; tháng ⛔ có driver ném `DRV_THIEU` có tên (⛔ trỏ ô cứng của H1000).

### 3. Scope

- **Gồm:** `fls/cau_hinh/driver.py` + nạp `ix_drv.json` + GET /config/drv
- **Loại trừ:** driver 2026 (nguồn ⛔ có)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** chỉ 2025 (AP đo)

### 4. Components touched

- **Frontend:** N/A — engine H12 tiêu thụ.
- **Backend:** `fls/cau_hinh/driver.py`
- **DB:** dòng config 0027
- **Integrations:** không

### 5. Preconditions

- C5
- DT10

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C10-B1 | NOEM · SHQ1 · 202503 | giá trị = ảnh | pg | chưa có |
| C10-B2 | 202603 | `DRV_THIEU` | đơn vị | — |

**Frontend/UI**

N/A — engine H12 tiêu thụ.

### 7. Expected artifacts

- `fls/cau_hinh/driver.py`
- `GET /api/fls/v1/config/drv`

### 8. Exit criteria

- [ ] C10-B1, B2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C10-B1, C10-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module + tuyến. Tệp: `fls/cau_hinh/driver.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_driver_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_driver_pg.py`
4. **Known limitations:** chỉ 2025 (AP đo).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C10` sang `ready` (phụ thuộc done: C5, DT10). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 28 · C10** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C10-B1, C10-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 29 · H10 — AL.PLT · 5 vendor đặc biệt theo cột 'cách tính'

**Traceability:** AP v3.1.1 §3.2.2 IX.VEN · §3.2.4 dòng 'VD341 · VD444 · VD428 · Max · VD62 tính riêng'.  
**Estimate:** 3–4 giờ · độ tin: thấp — công thức riêng cần đọc nguyên văn; **Dependency:** Step 26 · H9.  
**Ownership:** task `H10` · owner `fls-dev #HC` (BE-HC) · wave W9 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

AL.PLT · 5 vendor đặc biệt theo cột 'cách tính'

### 2. Goal

VD341 · VD444 · VD428 · 'Max' · VD62 được tính bằng hàm chọn theo mã 'cách tính' của IX.VEN (⛔ if theo tên vendor); cổng WP-C4b khớp MID3 GI đủ mọi vendor.

### 3. Scope

- **Gồm:** bảng hàm theo mã 'cách tính' (5 mã); mã lạ ⇒ lỗi có tên
- **Loại trừ:** vendor mới
- **Khái niệm mới duy nhất:** tính theo mã cấu hình
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** công thức riêng chép từ công thức AS-IS nguyên văn vào chú thích (giọng repo)

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/phan_bo.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H9

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H10-B1 | mỗi mã một ca tổng hợp | đúng tay tính | đơn vị | chưa có |
| H10-B2 | grep tên vendor trong `fls/bao_cao` | 0 lần (Đ1: đếm cả `fls/` lẫn `tools/`) | kiến trúc | — |
| H10-B3 | WP-C4b | lệch có MONG; vendor bỏ qua = 0 | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- WP-C4b

### 8. Exit criteria

- [ ] H10-B1…B3 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H10-B1, H10-B2, H10-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** bảng hàm theo mã. Tệp: `fls/bao_cao/phan_bo.py` · `tests/bao_cao/test_vendor_dac_biet.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_vendor_dac_biet.py`
4. **Known limitations:** công thức riêng chép từ công thức AS-IS nguyên văn vào chú thích (giọng repo).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H10` sang `ready` (phụ thuộc done: H9). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 29 · H10** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H10-B1, H10-B2, H10-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 30 · DT7 — Ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (414–419)

**Traceability:** AP v3.1.1 §3.3.1 PD 414–419 · §3.5.3 D4.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT7` · owner `fls-dev #DATA` (DATA) · wave W9 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (414–419)

### 2. Goal

Đáp án PLA đóng băng; cổng khẳng định PLA3 PM+HR = PLA1 + PLA3 HR từng ô ngay trên đáp án (nếu AS-IS lệch chính nó, liệt kê ô lệch).

### 3. Scope

- **Gồm:** `dap_an/pla1.json`; `dap_an/pla3_hr.json`; `dap_an/pla3_pm_hr.json`
- **Loại trừ:** engine PLA (H8)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** phép tự kiểm cộng theo VỊ TRÍ ô (đúng như AS-IS) — lệch nào là của AS-IS, ⛔ của FLS

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT7-B1 | đóng băng + tự kiểm cộng | số ô lệch của chính AS-IS có MONG (đo lần đầu rồi khai) | cổng | ảnh chưa có |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 3 ảnh

### 8. Exit criteria

- [ ] DT7-B1 đúng + đã chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT7-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 3 khuôn cột + test. Tệp: `tests/fixture/dap_an/pla*.json` · `tests/du_lieu/test_dap_an_pla.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_pla.py`
4. **Known limitations:** phép tự kiểm cộng theo VỊ TRÍ ô (đúng như AS-IS) — lệch nào là của AS-IS, ⛔ của FLS.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT7` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 30 · DT7** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT7-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 31 · C11 — IX.ALR: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT (D2)

**Traceability:** AP v3.1.1 §3.2.2 IX.ALR · §3.2.5 · §3.5.3 D2 · D3 (driver by GI = PE).  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 15 · C5, Step 11 · DT3.  
**Ownership:** task `C11` · owner `fls-dev #CF` (BE-CF) · wave W10 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.ALR: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT (D2)

### 2. Goal

`luat_cua(hd, ky)` trả phương pháp và cờ; mọi luật nạp vào đều `bat = false` (D2 A), theo PM 4 · by GI 8 · by NOEM 5 · by LE 0 HD như AP đo.

### 3. Scope

- **Gồm:** `fls/cau_hinh/luat_pb.py` + nạp từ ảnh Mapping Master K·L + ghi chú ATL B2:C4; GET /config/alr
- **Loại trừ:** bật cờ (owner ký — ngoài ISP)
- **Khái niệm mới duy nhất:** luật có hiệu lực theo kỳ + cờ
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** bật cờ ⛔ có tuyến trong ISP này (D2: parity trước)

### 4. Components touched

- **Frontend:** N/A — ⛔ màn cờ trong AP v3.1.1; engine H12 tiêu thụ.
- **Backend:** `fls/cau_hinh/luat_pb.py`
- **DB:** dòng config 0027
- **Integrations:** không

### 5. Preconditions

- C5
- DT3

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C11-B1 | nạp | 17 HD có luật (4 + 8 + 5); 100% `bat = false` | pg | chưa có |
| C11-B2 | HD OFR của CAH | ⛔ by NOEM (ngoại lệ AP §3.2.5) | đơn vị | — |
| C11-B3 | by GI | driver = PE (D3) | đơn vị | — |

**Frontend/UI**

N/A — ⛔ màn cờ trong AP v3.1.1; engine H12 tiêu thụ.

### 7. Expected artifacts

- `fls/cau_hinh/luat_pb.py`
- `GET /api/fls/v1/config/alr`

### 8. Exit criteria

- [ ] C11-B1…B3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C11-B1, C11-B2, C11-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module + tuyến. Tệp: `fls/cau_hinh/luat_pb.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_luat_pb_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_luat_pb_pg.py`
4. **Known limitations:** bật cờ ⛔ có tuyến trong ISP này (D2: parity trước).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C11` sang `ready` (phụ thuộc done: C5, DT3). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 31 · C11** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C11-B1, C11-B2, C11-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 32 · H7 — CA.GL dòng HR + SO.CFA3

**Traceability:** AP v3.1.1 §3.3.1 PD 401–404 · 407 · 408 · 412 · 413 · Q3.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 23 · H6, Step 24 · DT6, Step 25 · C8.  
**Ownership:** task `H7` · owner `fls-dev #HC` (BE-HC) · wave W10 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

CA.GL dòng HR + SO.CFA3

### 2. Goal

CA.GL chạy trên dòng họ HR và CFA3 dựng theo khuôn CFA1; cổng WP-C3c khớp đáp án GL HR · CFA3 (chỉ Y2025 như AS-IS).

### 3. Scope

- **Gồm:** CDT chuẩn hoá qua IX.ORG (`cdt_cua`) — ⛔ CDT Correct mặc định
- **Loại trừ:** HR qua ALLOCATE (Q3 DECIDED: ⛔)
- **Khái niệm mới duy nhất:** không (dùng lại H1/H5 cho họ HR)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** chỉ 2025

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/gl.py` · `cfa.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H6
- DT6
- C8 (`cdt_cua`)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H7-B1 | WP-C3c | ô so > 0; lệch có MONG | cổng | chưa có |
| H7-B2 | CDT lạ trong dòng HR | ném lỗi có tên (⛔ SHQ2) | đơn vị | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- WP-C3c

### 8. Exit criteria

- [ ] H7-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H7-B1, H7-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** nối họ HR. Tệp: `fls/bao_cao/gl.py` · `fls/bao_cao/cfa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_cfa3.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_cfa3.py`
4. **Known limitations:** chỉ 2025.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H7` sang `ready` (phụ thuộc done: H6, DT6, C8). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 32 · H7** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H7-B1, H7-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 33 · DT9 — Ảnh đáp án MID1–MID3 của OMC · SC · PS

**Traceability:** AP v3.1.1 §3.4.1 PD 508–510 · 600–603.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 21 · DT8.  
**Ownership:** task `DT9` · owner `fls-dev #DATA` (DATA) · wave W10 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án MID1–MID3 của OMC · SC · PS

### 2. Goal

Ba bộ MID của OMC · SC · PS đóng băng; cổng in rõ PS thiếu 03–09/2026 như AP đã đo (⛔ lấp).

### 3. Scope

- **Gồm:** `dap_an/{omc,sc,ps}_mid{1,2,3}.json`
- **Loại trừ:** engine (H11)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** lỗi row[45] của script OMC (AP §3.4.1) làm đáp án có thể sai — ghi cờ `nguon_nghi_loi`

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT8

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT9-B1 | đóng băng | PS thiếu đúng 7 tháng 03–09/2026; còn lại có MONG số dòng | cổng | ảnh chưa có |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 9 ảnh

### 8. Exit criteria

- [ ] DT9-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT9-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** khuôn cột dùng chung 3 sổ + test. Tệp: `tests/fixture/dap_an/{omc,sc,ps}_mid*.json` · `tests/du_lieu/test_dap_an_nen_tang.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_nen_tang.py`
4. **Known limitations:** lỗi row[45] của script OMC (AP §3.4.1) làm đáp án có thể sai — ghi cờ `nguon_nghi_loi`.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT9` sang `ready` (phụ thuộc done: DT8); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 33 · DT9** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT9-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 34 · C12 — IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK

**Traceability:** AP v3.1.1 §3.2.3 IX.PL · §3.2.4 dòng 'dòng PL viết trong ô ATL… hai định nghĩa'.  
**Estimate:** 3–4 giờ · độ tin: trung bình — bộ phân tích biểu thức cộng/trừ trên mã HD; **Dependency:** Step 12 · C4, Step 15 · C5.  
**Ownership:** task `C12` · owner `fls-dev #CF` (BE-CF) · wave W11 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK

### 2. Goal

`tinh_pl(gia_tri_hd)` trả PL2…PL8 từ MỘT định nghĩa biểu thức (⛔ eval), và `check_pl()` trả kết quả hai phép NB = 0 · NIS+INT+PIT+COM = CXA+GAH+DC+MC.

### 3. Scope

- **Gồm:** ngữ pháp tối thiểu: mã HD, `+`, `−`, ngoặc — ⛔ `eval`; nguồn định nghĩa = ATL (bản DECIDED theo đề xuất A của §3.2.3); chênh với Mapping Master ghi thành danh sách
- **Loại trừ:** hàm khác ngoài + −
- **Khái niệm mới duy nhất:** biểu thức cấu hình (bộ phân tích an toàn)
- **Mock/static:** giá trị HD tổng hợp ở test
- **Giới hạn còn lại sau bước:** chênh định nghĩa (vd LC ở PL3) được LIỆT KÊ cho owner, ⛔ tự hoà giải

### 4. Components touched

- **Frontend:** N/A — engine H13 tiêu thụ.
- **Backend:** `fls/cau_hinh/dong_pl.py`
- **DB:** dòng config 0027
- **Integrations:** không

### 5. Preconditions

- C4 (cây)
- C5

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C12-B1 | PL2 với giá trị HD tổng hợp | đúng tay tính | đơn vị | chưa có |
| C12-B2 | biểu thức `__import__` | từ chối | an toàn | — |
| C12-B3 | CHECK trên số cân | cả hai đúng; lệch 1 ⇒ báo dòng nào | đơn vị | — |

**Frontend/UI**

N/A — engine H13 tiêu thụ.

### 7. Expected artifacts

- `fls/cau_hinh/dong_pl.py`

### 8. Exit criteria

- [ ] C12-B1…B3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C12-B1, C12-B2, C12-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** bộ phân tích nhỏ + nạp định nghĩa. Tệp: `fls/cau_hinh/dong_pl.py` · `tests/cau_hinh/test_dong_pl.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_dong_pl.py`
4. **Known limitations:** chênh định nghĩa (vd LC ở PL3) được LIỆT KÊ cho owner, ⛔ tự hoà giải.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C12` sang `ready` (phụ thuộc done: C4, C5). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 34 · C12** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C12-B1, C12-B2, C12-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 35 · H11 — AL.PLT · OMC · SC · PS

**Traceability:** AP v3.1.1 §3.4.1 PD 508–510 · 600–603.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 29 · H10, Step 33 · DT9.  
**Ownership:** task `H11` · owner `fls-dev #HC` (BE-HC) · wave W11 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

AL.PLT · OMC · SC · PS

### 2. Goal

Cùng engine H9/H10 chạy cho OMC · SC · PS; cổng WP-C4c khớp MID3 ba sổ, kỳ PS thiếu 03–09/2026 hiện là `chua_co_dap_an` thay vì đạt.

### 3. Scope

- **Gồm:** tham số hoá theo sổ (⛔ chép code)
- **Loại trừ:** sửa lỗi row[45] của AS-IS
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** đáp án nghi lỗi (cờ DT9) tách khỏi lệch FLS

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/phan_bo.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H10
- DT9

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H11-B1 | WP-C4c | 3 sổ; lệch có MONG; PS 7 kỳ `chua_co_dap_an` | cổng | chưa có |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- WP-C4c

### 8. Exit criteria

- [ ] H11-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H11-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** tham số hoá sổ. Tệp: `fls/bao_cao/phan_bo.py` · `tools/do_hd2.py` · `tests/bao_cao/test_nen_tang_ba_so.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_nen_tang_ba_so.py`
4. **Known limitations:** đáp án nghi lỗi (cờ DT9) tách khỏi lệch FLS.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H11` sang `ready` (phụ thuộc done: H10, DT9). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 35 · H11** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H11-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 36 · DT12 — Ảnh Manual input của 22 kỳ còn lại (chế độ tự sinh AC10)

**Traceability:** AP v3.1.1 §5.3.2 AC10 · AC11 (tự sinh) · §5.3.1 HD1.  
**Estimate:** 3–4 giờ · độ tin: thấp — rủi ro hết giờ đọc sổ ADJUSTED (GAP-ORA-08); **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT12` · owner `fls-dev #DATA` (DATA) · wave W11 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh Manual input của 22 kỳ còn lại (chế độ tự sinh AC10)

### 2. Goal

Ảnh ô Manual input của ITL Ledge cho 22 kỳ ngoài 2026-03 đóng băng theo khuôn `itl_ledge_2026_03.json`; cổng liệt kê kỳ đọc được / hỏng.

### 3. Scope

- **Gồm:** 22 tệp `dap_an/itl_ledge_<ky>.json` (28 cột của 7 khối + ngày + itl_id; ⛔ Diễn giải, ⛔ Số CT — như ảnh 2026-03)
- **Loại trừ:** chạy tự sinh (H15)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** kỳ đọc hỏng sau 3 lần thử = `blocked` có tên, báo orchestrator (⛔ bỏ im)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2
- O7

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT12-B1 | đóng băng 22 kỳ | số kỳ đọc được + số kỳ hỏng = 22; mỗi kỳ số dòng = phân bố kỳ của sổ | cổng | ảnh chưa có |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- ≤ 22 ảnh

### 8. Exit criteria

- [ ] DT12-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT12-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** khuôn dùng lại + vòng đọc theo kỳ. Tệp: `tests/fixture/dap_an/itl_ledge_*.json` · `tests/du_lieu/test_anh_manual_input.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_anh_manual_input.py`
4. **Known limitations:** kỳ đọc hỏng sau 3 lần thử = `blocked` có tên, báo orchestrator (⛔ bỏ im).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT12` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 36 · DT12** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT12-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 37 · C14 — GET /parity/hd2 — trạng thái cổng HD2 theo gói WP-C2…C5

**Traceability:** AP v3.1.1 §5.3.1 HD2 · §3.5.4.  
**Estimate:** 2–3 giờ · độ tin: cao; **Dependency:** Step 5 · C2, Step 16 · H4.  
**Ownership:** task `C14` · owner `fls-dev #CF` (BE-CF) · wave W12 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

GET /parity/hd2 — trạng thái cổng HD2 theo gói WP-C2…C5

### 2. Goal

`GET /api/fls/v1/parity/hd2` trả, theo từng gói, số ô so · khớp · lệch · lát bị bỏ đọc từ `hd2_cong.json`, và gói chưa có cổng hiện `chua_do` thay vì 0 lệch.

### 3. Scope

- **Gồm:** handler đọc `hd2_cong.json` (hợp đồng do H4 khai)
- **Loại trừ:** đo sống
- **Khái niệm mới duy nhất:** không
- **Mock/static:** tệp cổng tĩnh
- **Giới hạn còn lại sau bước:** chỉ phản ánh gói đã có cổng tại lúc chạy

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F6)
- **Backend:** `fls/api/doi_chieu.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H4 (khai hợp đồng `hd2_cong.json`)
- C2 (module `doi_chieu.py`)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C14-B1 | tệp có WP-C2 | WP-C2: so = khớp; WP-C3…C5 `chua_do` | API | tuyến chưa có |
| C14-B2 | gói có `lat_bo > 0` | `dat = false` (cong_parity: thiếu lát ⛔ được nói 100%) | API | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F6)

### 7. Expected artifacts

- `GET /api/fls/v1/parity/hd2`

### 8. Exit criteria

- [ ] C14-B1, B2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C14-B1, C14-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** +1 handler +1 `Tuyen`. Tệp: `fls/api/doi_chieu.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/api/test_isp_parity_hd2.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/api/test_isp_parity_hd2.py`
4. **Known limitations:** chỉ phản ánh gói đã có cổng tại lúc chạy.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C14` sang `ready` (phụ thuộc done: C2, H4). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 37 · C14** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C14-B1, C14-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 38 · H8 — SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá

**Traceability:** AP v3.1.1 §3.3.1 PD 414–419 · §3.5.3 D4 · §3.2.4 dòng 'PLA3 PM + HR = cộng theo VỊ TRÍ'.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 32 · H7, Step 30 · DT7, Step 18 · C6.  
**Ownership:** task `H8` · owner `fls-dev #HC` (BE-HC) · wave W12 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá

### 2. Goal

PLA1 ghi mọi số vào ngày 1 tháng PL start (D4 A) và PLA3 PM+HR = PLA1 + PLA3 HR cộng theo (HD, ngày) — ⛔ theo vị trí ô; cổng WP-C3d khớp đáp án 414–419.

### 3. Scope

- **Gồm:** `fls/bao_cao/pla.py`
- **Loại trừ:** chia đều (D4 B)
- **Khái niệm mới duy nhất:** ghi nhận kỳ P&L
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ô AS-IS tự lệch (DT7) được tách khỏi lệch FLS

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/pla.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H7
- DT7
- C6 (luật A)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H8-B1 | dịch vụ PL start 2025-03-15 → end 2025-08 | toàn bộ vào 2025-03-01 | đơn vị | chưa có |
| H8-B2 | WP-C3d | lệch FLS có MONG; lệch của AS-IS tách riêng | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/pla.py`
- WP-C3d

### 8. Exit criteria

- [ ] H8-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H8-B1, H8-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module PLA. Tệp: `fls/bao_cao/pla.py` · `tools/do_hd2.py` · `tests/bao_cao/test_pla.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_pla.py`
4. **Known limitations:** ô AS-IS tự lệch (DT7) được tách khỏi lệch FLS.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H8` sang `ready` (phụ thuộc done: H7, DT7, C6). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 38 · H8** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H8-B1, H8-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 39 · DT11 — Ảnh đáp án Daily Report 2 · 3 (607–616)

**Traceability:** AP v3.1.1 §3.3.2 PD 605–617 · §3.5.3 D5 · IX.PL CHECK.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 7 · DT2.  
**Ownership:** task `DT11` · owner `fls-dev #DATA` (DATA) · wave W12 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Ảnh đáp án Daily Report 2 · 3 (607–616)

### 2. Goal

Daily Report 2 · 3 của bản A-CCR (D5) đóng băng theo (dòng PL, ngày/kỳ); cổng khẳng định hai phép CHECK của IX.PL trên chính đáp án.

### 3. Scope

- **Gồm:** `dap_an/daily_report_2.json`; `dap_an/daily_report_3.json` (bản [MID][FS1][PLA5] Sign off)
- **Loại trừ:** engine RP (H14); PDF
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ATL AH12 '− 0.5' chỉnh tay được ghi là ô chỉnh tay (⛔ config)

### 4. Components touched

- **Frontend:** N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.
- **Backend:** tool DT2
- **DB:** không
- **Integrations:** Google Sheets qua orchestrator

### 5. Preconditions

- DT2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| DT11-B1 | đóng băng + CHECK | NB = 0 và NIS+INT+PIT+COM = CXA+GAH+DC+MC: số kỳ đạt có MONG | cổng | ảnh chưa có |

**Frontend/UI**

N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ.

### 7. Expected artifacts

- 2 ảnh

### 8. Exit criteria

- [ ] DT11-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** DT11-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** 2 khuôn cột + test. Tệp: `tests/fixture/dap_an/daily_report_*.json` · `tests/du_lieu/test_dap_an_report.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/du_lieu/test_dap_an_report.py`
4. **Known limitations:** ATL AH12 '− 0.5' chỉnh tay được ghi là ô chỉnh tay (⛔ config).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `DT11` sang `ready` (phụ thuộc done: DT2); cần chốt trước: O7. Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 39 · DT11** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: DT11-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 40 · C7 — IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1)

**Traceability:** AP v3.1.1 §3.5.3 D1 (DECIDED · A: owner ký mỗi tháng; thiếu tháng = CHẶN) · §3.2.4.  
**Estimate:** 3–4 giờ · độ tin: trung bình — khuôn actor theo `danh_muc_actor.py`; **Dependency:** Step 15 · C5.  
**Ownership:** task `C7` · owner `fls-dev #CF` (BE-CF) · wave W13 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1)

### 2. Goal

`POST /api/fls/v1/config/fx/{yyyymm}/sign` (có actor) niêm phong tháng; `fx_cua(yyyymm)` cho engine trả tỷ giá chỉ khi tháng đã ký, còn lại ném `FX_CHAN` có tên tháng.

### 3. Scope

- **Gồm:** bản ký = phiên bản mới có `actor`, `ky_luc`; ký lại cùng tháng ⇒ 409; `fx_cua()` thuần cho engine H4 (CHẶN); actor ⛔ có trong danh mục ⇒ 403
- **Loại trừ:** UI ký (F5); huỷ ký
- **Khái niệm mới duy nhất:** ký niêm phong (sign-off) có actor
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ⛔ có đăng nhập (dùng danh mục actor hiện có)

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F5)
- **Backend:** `fls/cau_hinh/fx.py` (+`fx_cua`) · `cau_hinh_repo.py` (+ký) · tuyến POST `bang_ghi=('fls_cau_hinh_ban','fls_cau_hinh_dong')`
- **DB:** dòng mới qua 0027
- **Integrations:** không

### 5. Preconditions

- C5

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C7-B1 | ký 202510 với actor hợp lệ | 201; GET thấy `trang_thai = 'da_ky'` | pg | tuyến chưa có |
| C7-B2 | ký lại 202510 | 409 | pg | — |
| C7-B3 | `fx_cua('202511')` chưa ký | `FX_CHAN 202511` | đơn vị | — |
| C7-B4 | actor lạ | 403 | pg | — |
| C7-B5 | `soi_bang_tuyen`: POST khai `bang_ghi`, ⛔ chạm `fls_itl` | xanh | kiến trúc | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F5)

### 7. Expected artifacts

- `POST …/config/fx/{yyyymm}/sign`
- `fx_cua()`

### 8. Exit criteria

- [ ] C7-B1…B5 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C7-B1, C7-B2, C7-B3, C7-B4, C7-B5 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** +1 tuyến ghi +1 hàm CHẶN. Tệp: `fls/cau_hinh/fx.py` · `fls/repo/cau_hinh_repo.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_ky_fx_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_ky_fx_pg.py`
   - `python tools/soi_bang_tuyen.py`
4. **Known limitations:** ⛔ có đăng nhập (dùng danh mục actor hiện có).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C7` sang `ready` (phụ thuộc done: C5). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 40 · C7** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C7-B1, C7-B2, C7-B3, C7-B4, C7-B5; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 41 · H12 — AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2)

**Traceability:** AP v3.1.1 §3.4.2 PD 500 · 511–513 · 604 · §3.5.3 D2 · D3.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 38 · H8, Step 35 · H11, Step 28 · C10, Step 31 · C11, Step 27 · DT10.  
**Ownership:** task `H12` · owner `fls-dev #HC` (BE-HC) · wave W13 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2)

### 2. Goal

Khi mọi cờ IX.ALR tắt, `phan_bo_khoa()` trả đúng PLA3 PM + HR (đồng nhất) và cổng WP-C5a khớp ATL 604 · 606; khi bật cờ trên dữ liệu tổng hợp, Σ chia theo driver = tiền.

### 3. Scope

- **Gồm:** `fls/bao_cao/phan_bo_khoa.py`; nhánh bật cờ chỉ chạy trong test tổng hợp
- **Loại trừ:** bật cờ trên dữ liệu thật (owner ký)
- **Khái niệm mới duy nhất:** phân bổ theo khoá driver có cờ
- **Mock/static:** dữ liệu tổng hợp cho nhánh bật cờ
- **Giới hạn còn lại sau bước:** kỳ 2026 ⛔ có driver ⇒ chỉ đối chiếu ở cờ tắt

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/phan_bo_khoa.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H8
- H11
- C10
- C11
- DT10

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H12-B1 | cờ tắt | đầu ra = đầu vào từng ô | đơn vị | chưa có |
| H12-B2 | bật by NOEM tổng hợp | Σ chia = tiền; theo driver | đơn vị | — |
| H12-B3 | WP-C5a | ATL khớp; lệch có MONG | cổng | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/phan_bo_khoa.py`
- WP-C5a

### 8. Exit criteria

- [ ] H12-B1…B3 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H12-B1, H12-B2, H12-B3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module khoá. Tệp: `fls/bao_cao/phan_bo_khoa.py` · `tools/do_hd2.py` · `tests/bao_cao/test_phan_bo_khoa.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_phan_bo_khoa.py`
4. **Known limitations:** kỳ 2026 ⛔ có driver ⇒ chỉ đối chiếu ở cờ tắt.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H12` sang `ready` (phụ thuộc done: H8, H11, C10, C11, DT10). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 41 · H12** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H12-B1, H12-B2, H12-B3; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 42 · F6 — SCR-F09 khối HD2 theo gói WP-C2…C5

**Traceability:** AP v3.1.1 §5.3.1 HD2 · §3.5.4.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 10 · F2, Step 37 · C14.  
**Ownership:** task `F6` · owner `fls-dev #FE` (FE) · wave W13 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F09 khối HD2 theo gói WP-C2…C5

### 2. Goal

Màn Đối chiếu có khối HD2 liệt kê từng gói với ô so · khớp · lệch · lát bỏ từ `GET /parity/hd2`; gói chưa có cổng hiện 'chưa đo', ⛔ '0 lệch'.

### 3. Scope

- **Gồm:** khối HD2 dưới lưới HD1
- **Loại trừ:** khoan xuống ô HD2
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** chỉ gói đã có cổng

### 4. Components touched

- **Frontend:** `man_f09.js`
- **Backend:** tuyến C14 (dùng)
- **DB:** không
- **Integrations:** máy chủ thử

### 5. Preconditions

- C14
- F2 (màn trên tuyến thật)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F6-B1 | N/A — tuyến có bài ở C14 | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F6-F1 | tệp cổng chỉ có WP-C2 | WP-C2 có số; C3…C5 'chưa đo' | tích hợp headless | chưa có |
| F6-F2 | gói có lát bỏ | đỏ + chữ 'thiếu lát' | DOM | — |

### 7. Expected artifacts

- khối HD2

### 8. Exit criteria

- [ ] F6-F1, F2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F6-F1, F6-F2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một khối. Tệp: `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_hd2.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f09_hd2.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** chỉ gói đã có cổng.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F6` sang `ready` (phụ thuộc done: F2, C14). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 42 · F6** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F6-F1, F6-F2; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 43 · C13 — IX.TMP: bản báo cáo ký có phiên bản (snapshot sign-off)

**Traceability:** AP v3.1.1 §3.2.3 IX.TMP · §3.2.4 dòng 'sign-off dán value ở sheet [PLA5]'.  
**Estimate:** 3–4 giờ · độ tin: trung bình — khuôn ký của C7; **Dependency:** Step 40 · C7.  
**Ownership:** task `C13` · owner `fls-dev #CF` (BE-CF) · wave W14 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

IX.TMP: bản báo cáo ký có phiên bản (snapshot sign-off)

### 2. Goal

`POST /api/fls/v1/report/snapshot/{ky}/sign` lưu bản Daily Report 3 kèm checksum và actor; bản đã ký ⛔ đổi khi số nguồn đổi — số mới thành phiên bản mới chưa ký.

### 3. Scope

- **Gồm:** lưu bản (JSON ô) do engine H14 đưa vào; GET danh sách phiên bản + trạng thái
- **Loại trừ:** khuôn Templ 1–5 dạng trình bày; PDF
- **Khái niệm mới duy nhất:** không (dùng lại ký C7 + kho C5)
- **Mock/static:** bản báo cáo tổng hợp cho tới khi H14 xong
- **Giới hạn còn lại sau bước:** nội dung bản lấy từ tham số; nối engine thật ở I2

### 4. Components touched

- **Frontend:** N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F7)
- **Backend:** `fls/cau_hinh/ban_ky.py` · tuyến GET + POST
- **DB:** dòng 0027
- **Integrations:** không

### 5. Preconditions

- C7 (khuôn ký)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| C13-B1 | ký bản kỳ 2025-12 | 201; GET thấy phiên bản 1 đã ký + checksum | pg | chưa có |
| C13-B2 | đưa bản mới khác 1 ô | phiên bản 2 `chua_ky`; phiên bản 1 giữ nguyên | pg | — |

**Frontend/UI**

N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp). (F7)

### 7. Expected artifacts

- `GET/POST /api/fls/v1/report/snapshot/{ky}…`

### 8. Exit criteria

- [ ] C13-B1, B2 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** C13-B1, C13-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module + 2 tuyến. Tệp: `fls/cau_hinh/ban_ky.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tests/cau_hinh/test_ban_ky_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/cau_hinh/test_ban_ky_pg.py`
   - `python tools/soi_bang_tuyen.py`
4. **Known limitations:** nội dung bản lấy từ tham số; nối engine thật ở I2.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `C13` sang `ready` (phụ thuộc done: C7). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 43 · C13** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: C13-B1, C13-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 44 · H13 — SO.PLA3-ATL + IX.PL CHECK

**Traceability:** AP v3.1.1 §3.2.3 IX.PL · §3.4.2 PD 606.  
**Estimate:** 2–4 giờ · độ tin: cao; **Dependency:** Step 41 · H12, Step 34 · C12.  
**Ownership:** task `H13` · owner `fls-dev #HC` (BE-HC) · wave W14 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SO.PLA3-ATL + IX.PL CHECK

### 2. Goal

Dòng PL2…PL8 tính từ IX.PL trên ATL của FLS và hai phép CHECK chạy mỗi kỳ; cổng WP-C5b khớp dòng PL của đáp án và in kỳ nào CHECK đỏ.

### 3. Scope

- **Gồm:** dùng `fls/cau_hinh/dong_pl.py` (C12)
- **Loại trừ:** báo cáo trình bày (H14)
- **Khái niệm mới duy nhất:** không
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** chênh định nghĩa PL ATL ↔ Mapping Master hiện ở báo cáo cổng

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/pla.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H12
- C12

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H13-B1 | WP-C5b | dòng PL khớp; CHECK đỏ kỳ nào có tên | cổng | chưa có |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- WP-C5b

### 8. Exit criteria

- [ ] H13-B1 đúng + chứng minh đỏ
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H13-B1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** nối IX.PL. Tệp: `fls/bao_cao/pla.py` · `tools/do_hd2.py` · `tests/bao_cao/test_pla_atl.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_pla_atl.py`
4. **Known limitations:** chênh định nghĩa PL ATL ↔ Mapping Master hiện ở báo cáo cổng.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H13` sang `ready` (phụ thuộc done: H12, C12). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 44 · H13** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H13-B1; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 45 · F5 — SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận

**Traceability:** AP v3.1.1 §3.5.3 D1 · §3.2.4.  
**Estimate:** 3–4 giờ · độ tin: trung bình — hộp thoại theo `hop_thoai.js`; **Dependency:** Step 20 · F4, Step 40 · C7.  
**Ownership:** task `F5` · owner `fls-dev #FE` (FE) · wave W14 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận

### 2. Goal

Bấm 'Ký tháng' ở một tháng chưa ký, xác nhận trong hộp thoại, thấy tháng chuyển 'đã ký · actor · ngày' và nút khoá; ký lại báo 409 bằng chữ.

### 3. Scope

- **Gồm:** nút + hộp xác nhận + khoá sau ký; mã lỗi 403/409 có chữ (bài `test_goi_cua_phu_het_ma_loi.py`)
- **Loại trừ:** huỷ ký
- **Khái niệm mới duy nhất:** hành động ghi từ màn cấu hình
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** actor lấy từ danh mục hiện có (⛔ đăng nhập)

### 4. Components touched

- **Frontend:** `man_f08.js`
- **Backend:** tuyến C7 (dùng)
- **DB:** kho test
- **Integrations:** máy chủ thử

### 5. Preconditions

- F4
- C7

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F5-B1 | N/A — tuyến có bài ở C7 | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F5-F1 | ký 202510 | hộp xác nhận → 'đã ký'; nút khoá | tích hợp headless (pg) | chưa có |
| F5-F2 | ký lại | chữ lỗi 409 | tích hợp | — |
| F5-F3 | huỷ ở hộp xác nhận | ⛔ gọi POST | DOM | — |

### 7. Expected artifacts

- nút ký SCR-F08

### 8. Exit criteria

- [ ] F5-F1…F3 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F5-F1, F5-F2, F5-F3 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** nút + hộp + gọi POST. Tệp: `fls/web/tep/man_f08.js` · `tests/web/test_isp_f08_ky_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f08_ky_pg.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** actor lấy từ danh mục hiện có (⛔ đăng nhập).
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F5` sang `ready` (phụ thuộc done: F4, C7). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 45 · F5** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F5-F1, F5-F2, F5-F3; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 46 · H15 — HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho 22 kỳ còn lại)

**Traceability:** AP v3.1.1 §5.3.2 AC10 · AC11 · §5.3.1 HD1.  
**Estimate:** 3–4 giờ · độ tin: trung bình — đường tự sinh đã chạy trên 2026-03 (584/584 HD); **Dependency:** Step 9 · H3, Step 36 · DT12.  
**Ownership:** task `H15` · owner `fls-dev #HC` (BE-HC) · wave W15 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho 22 kỳ còn lại)

### 2. Goal

`do_voi_so_luong.py` chạy chế độ tự sinh (FLS tự tính MID) trên mọi kỳ có ảnh Manual input và ghi `tu_sinh` theo kỳ; kỳ ⛔ có ảnh hiện `chua_do` thay vì đạt.

### 3. Scope

- **Gồm:** lặp `do_tu_sinh()` theo kỳ; MONG theo kỳ khai sau lần đo đầu
- **Loại trừ:** sửa lệch MID tự sinh (4.020/4.088 ở 2026-03) — mỗi lớp là một bước riêng nếu cần
- **Khái niệm mới duy nhất:** không (mở rộng đường tự sinh có sẵn)
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** kỳ DT12 đọc hỏng = `chua_do`

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `tools/do_voi_so_luong.py` · `fls/oracle/tu_soi.py` (đọc)
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H3
- DT12

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H15-B1 | chạy mọi kỳ | `tu_sinh` có ở ≥ 1 kỳ ngoài 2026-03 hoặc DT12 cho 0 kỳ ⇒ ĐỎ có tên | cổng | chưa có |
| H15-B2 | kỳ 2026-03 | HD 584/584 giữ nguyên (hồi quy) | hồi quy | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `voi_so_luong.json` + `tu_sinh` theo kỳ

### 8. Exit criteria

- [ ] H15-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H15-B1, H15-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** vòng theo kỳ. Tệp: `tools/do_voi_so_luong.py` · `docs/ITL/_tools/voi_so_luong.json` · `tests/oracle/test_tu_sinh_theo_ky.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/oracle/test_tu_sinh_theo_ky.py`
   - `python tools/do_voi_so_luong.py --ghi`
4. **Known limitations:** kỳ DT12 đọc hỏng = `chua_do`.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H15` sang `ready` (phụ thuộc done: H3, DT12). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 46 · H15** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H15-B1, H15-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 47 · F7 — SCR-F09 ký bản Daily Report 3 (IX.TMP snapshot)

**Traceability:** AP v3.1.1 §3.2.3 IX.TMP · §3.2.4 dòng 'sign-off dán value'.  
**Estimate:** 3–4 giờ · độ tin: trung bình — dùng lại hộp ký F5; **Dependency:** Step 42 · F6, Step 43 · C13.  
**Ownership:** task `F7` · owner `fls-dev #FE` (FE) · wave W15 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

SCR-F09 ký bản Daily Report 3 (IX.TMP snapshot)

### 2. Goal

Ở khối HD2, kỳ có bản báo cáo hiện danh sách phiên bản (checksum · trạng thái); bấm 'Ký bản' ký phiên bản mới nhất, phiên bản cũ đã ký giữ nguyên.

### 3. Scope

- **Gồm:** danh sách phiên bản + nút ký
- **Loại trừ:** xem nội dung báo cáo từng ô; PDF
- **Khái niệm mới duy nhất:** hiển thị phiên bản có ký
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** nội dung bản là của engine H14 khi I2 chạy; trước đó là bản tổng hợp của C13

### 4. Components touched

- **Frontend:** `man_f09.js`
- **Backend:** tuyến C13 (dùng)
- **DB:** kho test
- **Integrations:** máy chủ thử

### 5. Preconditions

- C13
- F6

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F7-B1 | N/A — tuyến có bài ở C13 | — | — | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| F7-F1 | kỳ có 2 phiên bản (1 đã ký) | ký bản 2 → cả hai 'đã ký', checksum khác nhau | tích hợp headless (pg) | chưa có |

### 7. Expected artifacts

- danh sách phiên bản + ký

### 8. Exit criteria

- [ ] F7-F1 xanh
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** F7-F1 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** danh sách + nút. Tệp: `fls/web/tep/man_f09.js` · `tests/web/test_isp_f09_ky_ban_pg.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/web/test_isp_f09_ky_ban_pg.py` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)
4. **Known limitations:** nội dung bản là của engine H14 khi I2 chạy; trước đó là bản tổng hợp của C13.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `F7` sang `ready` (phụ thuộc done: F6, C13). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 47 · F7** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: F7-F1; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 48 · H14 — RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5)

**Traceability:** AP v3.1.1 §3.3.2 PD 605–617 · §3.5.3 D5 · §5.3.1 HD2.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 44 · H13, Step 39 · DT11, Step 43 · C13.  
**Ownership:** task `H14` · owner `fls-dev #HC` (BE-HC) · wave W16 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5)

### 2. Goal

`daily_report(ky, fs)` dựng Daily Report 2 · 3 với FS là tham số (D5 A) và cổng WP-C5c khớp đáp án 607–616 từng ô; đầu ra là JSON ô đưa được vào C13.

### 3. Scope

- **Gồm:** `fls/bao_cao/bao_cao.py`; JSON ô theo hợp đồng của C13
- **Loại trừ:** ghi CCR / PDF (HD4 — ngoài ISP)
- **Khái niệm mới duy nhất:** dựng báo cáo theo khuôn
- **Mock/static:** không
- **Giới hạn còn lại sau bước:** ô chỉnh tay AS-IS (ATL AH12 '− 0.5') tính là lệch có tên 'chỉnh tay ⛔ actor', ⛔ chép vào config

### 4. Components touched

- **Frontend:** N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).
- **Backend:** `fls/bao_cao/bao_cao.py`
- **DB:** không
- **Integrations:** không

### 5. Preconditions

- H13
- DT11
- C13 (hợp đồng JSON ô của bản ký)

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| H14-B1 | WP-C5c | ô so > 0; lệch có MONG; ô chỉnh tay liệt kê | cổng | chưa có |
| H14-B2 | FS = FS1/FS2/FS3 | cùng engine, khác tham số | đơn vị | — |

**Frontend/UI**

N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2).

### 7. Expected artifacts

- `fls/bao_cao/bao_cao.py`
- WP-C5c

### 8. Exit criteria

- [ ] H14-B1, B2 đúng
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** H14-B1, H14-B2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** module báo cáo. Tệp: `fls/bao_cao/bao_cao.py` · `tools/do_hd2.py` · `tests/bao_cao/test_daily_report.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/bao_cao/test_daily_report.py`
4. **Known limitations:** ô chỉnh tay AS-IS (ATL AH12 '− 0.5') tính là lệch có tên 'chỉnh tay ⛔ actor', ⛔ chép vào config.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `H14` sang `ready` (phụ thuộc done: H13, DT11, C13). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 48 · H14** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: H14-B1, H14-B2; tách BE/API ↔ FE/UI (FE: N/A có lý do); chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 49 · I1 — Tích hợp HD1 xuyên suốt: ảnh → ghép → cổng theo kỳ → API → SCR-F09

**Traceability:** AP v3.1.1 §5.3.1 HD1 · §5.3.2 AC7 · AC10 · AC11 · HD5.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 46 · H15, Step 8 · C3, Step 13 · F3, Step 6 · H2.  
**Ownership:** task `I1` · owner `fls-dev #DATA` (DATA) · wave W16 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Tích hợp HD1 xuyên suốt: ảnh → ghép → cổng theo kỳ → API → SCR-F09

### 2. Goal

Một bài tích hợp chạy từ ba ảnh đóng băng qua ghép FLS, cổng HD1 theo kỳ (kể cả tự sinh), tuyến /parity/months và SCR-F09, và kết luận AC10 · AC11 theo từng kỳ khớp nhau ở mọi tầng.

### 3. Scope

- **Gồm:** bài `tests/tich_hop/test_hd1_xuyen_suot.py`: tầng cổng ↔ JSON ↔ API ↔ DOM cùng một số mỗi kỳ; đường lỗi: tệp đo vắng ⇒ API 503 ⇒ màn khối lỗi; sổ lý do có chữ ký giả ⇒ kỳ đổi xanh ở cả 3 tầng
- **Loại trừ:** chữ ký thật (O8)
- **Khái niệm mới duy nhất:** không (tích hợp)
- **Mock/static:** chữ ký lý do giả trong bài (biên ghi rõ)
- **Giới hạn còn lại sau bước:** số là của ảnh 26/08; đọc kho sống (HD5) ngoài ISP

### 4. Components touched

- **Frontend:** SCR-F09 qua máy chủ thử
- **Backend:** cổng + tuyến C2/C3
- **DB:** không
- **Integrations:** máy chủ thử

### 5. Preconditions

- H15
- C3
- F3
- H2

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| I1-B1 | cổng → JSON → API | mỗi kỳ: `dat_hd1` giống nhau ở 3 tầng | tích hợp | chưa có |
| I1-B2 | tệp đo vắng | 503 có mã | tích hợp lỗi | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| I1-F1 | SCR-F09 | số kỳ xanh = số kỳ `dat_hd1` của cổng | tích hợp headless | — |
| I1-F2 | đường lỗi | khối lỗi | tích hợp | — |

### 7. Expected artifacts

- `tests/tich_hop/test_hd1_xuyen_suot.py`
- bảng AC10/AC11 theo kỳ dán vào BG

### 8. Exit criteria

- [ ] I1-B1, B2, F1, F2 xanh
- [ ] toàn bộ cổng CLAUDE.md chạy, kết quả thật dán vào BG
- [ ] 3 vòng review xong
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** I1-B1, I1-B2, I1-F1, I1-F2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một bài tích hợp. Tệp: `tests/tich_hop/test_hd1_xuyen_suot.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `.venv/bin/python -m pytest tests/tich_hop/test_hd1_xuyen_suot.py`
4. **Known limitations:** số là của ảnh 26/08; đọc kho sống (HD5) ngoài ISP.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `I1` sang `ready` (phụ thuộc done: H15, C3, F3, H2). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 49 · I1** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: I1-B1, I1-B2, I1-F1, I1-F2; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## Step 50 · I2 — Tích hợp HD2 xuyên suốt: config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản

**Traceability:** AP v3.1.1 §5.3.1 HD2 · §5.3.2 AC9 · §3.5.4 WP-C1…C5 · D1 · D2 · D5.  
**Estimate:** 3–4 giờ · độ tin: trung bình; **Dependency:** Step 48 · H14, Step 43 · C13, Step 37 · C14, Step 47 · F7, Step 49 · I1.  
**Ownership:** task `I2` · owner `fls-dev #HC` (BE-HC) · wave W17 · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).

### 1. Step name

Tích hợp HD2 xuyên suốt: config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản

### 2. Goal

Một bài tích hợp nạp config vào kho, ký tỷ giá các tháng, chạy chuỗi engine CA→SO→AL→RP với `fx_cua()` thật, so mọi gói WP-C2…C5 với đáp án và ký bản Daily Report 3 — và tháng chưa ký tỷ giá CHẶN cả chuỗi có tên.

### 3. Scope

- **Gồm:** `tests/tich_hop/test_hd2_xuyen_suot.py` (pg); đường lỗi: bỏ ký 1 tháng ⇒ `FX_CHAN` ở GL ⇒ gói WP-C2 `dat = false` ⇒ F09 đỏ; chạy lại trên máy owner (`fls-pg-1`, chỉ đọc) trước merge — O4
- **Loại trừ:** bật cờ luật; ghi CCR/PDF; agent
- **Khái niệm mới duy nhất:** không (tích hợp)
- **Mock/static:** actor ký là actor test
- **Giới hạn còn lại sau bước:** kho test; bản owner chạy lại là điều kiện MERGE, ⛔ điều kiện xong bước

### 4. Components touched

- **Frontend:** SCR-F09 khối HD2 + ký bản
- **Backend:** toàn chuỗi engine + tuyến
- **DB:** kho test (0027)
- **Integrations:** máy chủ thử

### 5. Preconditions

- H14
- C13
- C14
- F7
- I1

### 6. Test cases

**Backend/API**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| I2-B1 | chuỗi đủ | mỗi gói: số ô so = số ô đáp án; lệch = MONG đã khai ở từng bước | tích hợp (pg) | chưa có |
| I2-B2 | bỏ ký 202510 | `FX_CHAN 202510` xuyên chuỗi; ⛔ số nào ra cho tháng ấy | tích hợp lỗi | — |
| I2-B3 | ký bản 2025-12 từ đầu ra H14 | phiên bản có checksum = checksum JSON ô | tích hợp | — |

**Frontend/UI**

| ID | Setup · input · action | Mong (assertion) | Loại | Vì sao đỏ trước thay đổi |
|---|---|---|---|---|
| I2-F1 | SCR-F09 khối HD2 sau chuỗi đủ | mọi gói có số; ⛔ 'chưa đo' | tích hợp headless | — |
| I2-F2 | sau bỏ ký | WP-C2 đỏ có chữ | tích hợp | — |

### 7. Expected artifacts

- `tests/tich_hop/test_hd2_xuyen_suot.py`
- báo cáo HD2 theo gói dán vào BG

### 8. Exit criteria

- [ ] I2-B1…B3, F1, F2 xanh
- [ ] toàn bộ cổng CLAUDE.md xanh hoặc đỏ-có-sẵn đã ghi ở S0
- [ ] 3 vòng review xong
- [ ] điều kiện MERGE (khác điều kiện xong): chạy lại trên máy owner + ThuongCT ký (O6)
- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0, O1 đã gỡ

### Substep 1 — Test cases và handoff cho một thay đổi nhỏ

1. **Test cases:** I2-B1, I2-B2, I2-B3, I2-F1, I2-F2 — phủ mọi dòng ở mục 8.
2. **Implementation (kế hoạch, chưa viết mã):** một bài tích hợp. Tệp: `tests/tich_hop/test_hd2_xuyen_suot.py`.
3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`):
   - `export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1`
   - `.venv/bin/python -m pytest tests/tich_hop/test_hd2_xuyen_suot.py`
   - `.venv/bin/python -m pytest `
4. **Known limitations:** kho test; bản owner chạy lại là điều kiện MERGE, ⛔ điều kiện xong bước.
5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.1 và orchestrator đổi `I2` sang `ready` (phụ thuộc done: H14, C13, C14, F7, I1). Hết bước: báo và hỏi có sang bước kế không.

### Substep 2 — Hợp đồng strict TDD của bước này

Nguồn sự thật duy nhất: **Step 50 · I2** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.

1. **Test design** — dẫn từ mục 6 + 8: I2-B1, I2-B2, I2-B3, I2-F1, I2-F2; tách BE/API ↔ FE/UI; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.
2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.
3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.
4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.
5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.
6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + `.venv/bin/lint-imports`, `python -m fls.db.pg_migrate`, `python tools/kiem_so_song.py`; ghi bộ nào ⛔ chạy và vì sao.
7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.

## 4. Phần cuối kế hoạch

### 4.1 Tích hợp cuối và acceptance được phủ

| Acceptance / quyết định | Bước phủ | Tích hợp cuối |
|---|---|---|
| AC10 | DT1, DT12, C2, H2, H3, H15, F1, F2, I1 | I1 |
| AC11 | DT12, H15, I1 | I1 |
| AC7 | C3, F3, I1 | I1 |
| AC9 | C1, H1, I2 | I2 |
| D1 | DT2, C1, C5, C7, F4, F5, I2 | I2 |
| D2 | C11, H12, I2 | I2 |
| D3 | C11, H12 | I2 |
| D4 | DT7, C6, H8 | I2 |
| D5 | DT11, H14, I2 | I2 |
| HD1 | S0, DT1, DT12, C3, H2, H3, H15, F1, F3, I1 | I1 |
| HD2 | DT4, C14, H4, H14, F6, F7, I2 | I2 |
| HD5 | S0, I1 | I1 |
| WP-C1 | DT3, C4, I2 | I2 |
| WP-C2 | DT4, H1, H4, I2 | I2 |
| WP-C3 | DT5, H5, H6, H7, H8 | I2 |
| WP-C4 | DT8, H9, H10, H11 | I2 |
| WP-C5 | H12, H13, H14 | I2 |

- **I1** (HD1) và **I2** (HD2) chạy trên thành phần đã tích hợp thật (ảnh đóng băng, kho test PG, máy chủ thử, màn headless).
- **Biên còn mô phỏng:** chữ ký lý do HD1 trong I1 là chữ ký test (O8 cho chữ ký thật) · actor ký là actor test · kho test cục bộ (O4: chạy lại I2 trên `fls-pg-1` trước merge) · số NOW là ảnh đóng băng một ngày (đọc kho sống = HD5, ngoài ISP).
- **Chưa phủ (có tên):** HD3 (đủ bốn họ dữ liệu — cần RI/PR) · HD4 (kế toán làm trên FLS, cắt Gsheet) · AC1–AC6, AC8 (đã đạt ở AP — đo bằng máy lúc sinh AP).

### 4.2 Việc cần bạn chốt trước Wave 0

1. **Xác nhận breakdown này** (51 bước, 4 làn, 3 vòng review).
2. **O1** — nối lại GitHub có quyền ghi (khuyến nghị A), nếu không thì mọi bước dừng ở `review` chờ push.
3. **O2 · O3 · O4 · O5 · O7 · O9** — khuyến nghị A cho cả sáu; **O6 · O8** — xác nhận ThuongCT là người ký (merge và sổ lý do HD1).

<sub>Kiểm bởi bộ sinh: 51 bước · đủ 8 trường + 2 substep · DAG ⛔ chu trình · ước lượng ≤ 4h · AP sha256 khớp.</sub>
