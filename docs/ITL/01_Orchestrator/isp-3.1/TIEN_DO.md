# Tiến độ ISP 3.1 — orchestrator

> Sổ trạng thái của `IncrementalStepPlan-FLS-Voi_v3.1.2.md` (AP v3.1.2 sha256 `5cf6e576…`). **Chỉ orchestrator ghi.**
> Trạng thái: `planned → ready → in_progress → review(R1/R2/R3) → done` hoặc `blocked` kèm nguyên nhân. Tiến độ theo BẰNG CHỨNG (exit criteria), ⛔ gán phần trăm.
> Người dùng 16/11: *"Xác nhận các recommend. Xác nhận ISP. Bắt đầu triển khai"* ⇒ O2–O11 = A; O6/O8: ThuongCT ký trước merge và ký sổ lý do HD1.

## Quy ước chạy song song (orchestrator chốt 16/11)

| Thứ | Quy ước | Vì sao |
|---|---|---|
| Kho test | ⛔ **Đổi 16/11 (S0-Q1 = A):** mỗi agent một **CỤM PostgreSQL riêng theo cổng**, tên kho giữ `fls` / `fls_test` — agent BE-CF `5434` · BE-HC `5435` · FE `5436` · DATA `5437`; reviewer theo làn của bước đang kiểm `5444` · `5445` · `5446` · `5447`; cụm `5433` = cụm gốc của S0. Đặt cả `PG_DSN` lẫn `PG_DSN_TEST` vào cổng của mình. ~~`fls_test_<làn>` trên một cụm~~ — bỏ: 24 dòng trong 19 tệp bài ghim `== "fls_test"` ⇒ +131 bài đỏ giả (đo ở S0) | `tests/conftest.py` **DROP rồi CREATE** kho test đầu mỗi lượt — hai lượt chung một kho là giẫm nhau (S0 AC-6: đối chứng chung kho ⇒ `3 failed`) |
| venv | `/home/user/FLS-tobe/.venv` dùng chung (đã `gitignore`), mỗi worktree gọi bằng đường dẫn tuyệt đối | gói `fls` lấy từ thư mục làm việc của worktree, ⛔ cài vào venv |
| Nhánh | worktree riêng mỗi bước, nhánh cục bộ `isp/<bước>` (⛔ push); orchestrator gộp vào `claude/laughing-bohr-331pt0` sau R3 rồi push | O2 = A |
| Phiếu | orchestrator cấp trước dải số cho mỗi bước (WO · BG · KQ-R1 · KQ-R2 · KQ-R3) | dãy số chung — agent song song tự lấy số sẽ trùng |
| Dashboard §5 | orchestrator ghi một dòng khi phát / đóng bước (agent ⛔ sửa) | bốn worktree cùng chèn đầu một bảng ⇒ xung đột gộp mỗi lần |

## Bảng bước

| Step | ID | Tên | Agent làm | Wave | Phụ thuộc | Ước lượng | Trạng thái | Phiếu |
|---|---|---|---|---|---|---|---|---|
| 0 | `S0` | Môi trường test + đường nền cổng + khung hai gói mới | fls-dev #CF | W0 | — | 2–3h | `in_progress` (sửa sau R1) | WO-065 · BG-066 · KQ-067 ✅ |
| 1 | `H1` | CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD) | fls-dev #HC | W1 | S0 | 3–4h | `planned` | — |
| 2 | `C1` | IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx | fls-dev #CF | W1 | S0 | 3–4h | `planned` | — |
| 3 | `DT1a` | HD1 · kiểm kê 122 dòng sổ chưa 1-1 (offline, trên ảnh đóng băng) | fls-dev #DATA | W1 | S0 | 2–3h | `planned` | — |
| 4 | `H2` | HD1 · cổng nhận 'lệch có tên lý do và owner ký' | fls-dev #HC | W2 | DT1a | 2–4h | `planned` | — |
| 5 | `DT1b` | HD1 · gán lý do cho 122 dòng bằng khoá đọc ở nguồn (khoá băm, ⛔ commit giá trị) | fls-dev #DATA | W2 | DT1a | 3–4h | `planned` | — |
| 6 | `H3` | HD1 · sửa lớp lỗi mã lớn nhất mà DT1b chỉ ra | fls-dev #HC | W3 | H2, DT1b | 3–4h | `planned` | — |
| 7 | `CG1` | Cổng HD1 vào `GET /gates`: ô chờ `FINAL` thành số đo + cổng `HD1_THANG` | fls-dev #CF | W3 | H2, DT1a | 2–3h | `planned` | — |
| 8 | `DT2` | Đường ống đóng băng sheet + ảnh IX.FX (9.2 Exchange Rate) | fls-dev #DATA | W3 | S0 | 2–3h | `planned` | — |
| 9 | `FG` | F03 'Cổng hôm nay' hiện cổng HD1 (đọc tuyến thật) | fls-dev #FE | W4 | CG1 | 2–3h | `planned` | — |
| 10 | `DT3` | Ảnh nguồn IX.HD · IX.ORG: cây ATL 74 dòng + Mapping Master + CDT Correct | fls-dev #DATA | W4 | DT2 | 2–3h | `planned` | — |
| 11 | `C4` | IX.HD cây: nạp + kiểm cha–con + GET /config/hd (tĩnh từ ảnh) | fls-dev #CF | W5 | DT3 | 3–4h | `planned` | — |
| 12 | `DT4` | Ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT) | fls-dev #DATA | W5 | DT2 | 3–4h | `planned` | — |
| 13 | `H4` | KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên) | fls-dev #HC | W6 | H1, DT4, DT2, C1 | 3–4h | `planned` | — |
| 14 | `C5` | Kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho | fls-dev #CF | W6 | C4, DT2 | 2–3h | `planned` | — |
| 15 | `DT5` | Ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M | fls-dev #DATA | W6 | DT3 | 3–4h | `planned` | — |
| 16 | `H5` | SO.CFA1 Daily: Σ theo (HD, ngày) trên cây IX.HD | fls-dev #HC | W7 | H4, C4, DT5 | 3–4h | `planned` | — |
| 17 | `C6` | IX.PER: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4) | fls-dev #CF | W7 | C5 | 2–4h | `planned` | — |
| 18 | `F4` | SCR-F08 Cấu hình · bảng IX.FX chỉ đọc trên tuyến thật | fls-dev #FE | W7 | C5 | 3–4h | `planned` | — |
| 19 | `DT8` | Ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI | fls-dev #DATA | W7 | DT2 | 3–4h | `planned` | — |
| 20 | `H6` | SO Y/H/Q/M theo IX.PER | fls-dev #HC | W8 | H5, C6 | 2–4h | `planned` | — |
| 21 | `C9` | IX.VEN: vendor · network · CDT1 + cột 'cách tính' | fls-dev #CF | W8 | C5, DT8 | 2–4h | `planned` | — |
| 22 | `C8` | IX.ORG: LE · TK → CDT1 + CDT lạ vào hàng chờ (⛔ rơi về SHQ2) | fls-dev #FE ↩ làn BE-CF | W8 | C5, DT3 | 2–3h | `planned` | — |
| 23 | `DT6` | Ảnh đáp án GL HR + CFA3 (407 · 408 · 412 · 413) | fls-dev #DATA | W8 | DT2 | 3–4h | `planned` | — |
| 24 | `H9` | AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P) | fls-dev #HC | W9 | H4, C9, DT8 | 3–4h | `planned` | — |
| 25 | `C11` | IX.ALR: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT (D2) | fls-dev #CF | W9 | C5, DT3 | 2–3h | `planned` | — |
| 26 | `C12` | IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK | fls-dev #FE ↩ làn BE-CF | W9 | C4, C5 | 3–4h | `planned` | — |
| 27 | `DT10` | Ảnh IX.DRV (Allocation Table) + đáp án ATL (604 · 606) | fls-dev #DATA | W9 | DT2 | 3–4h | `planned` | — |
| 28 | `H10` | AL.PLT · 5 vendor đặc biệt theo cột 'cách tính' | fls-dev #HC | W10 | H9 | 3–4h | `planned` | — |
| 29 | `C10` | IX.DRV: driver theo (driver, CDT1, tháng) | fls-dev #CF | W10 | C5, DT10 | 2–4h | `planned` | — |
| 30 | `CG2` | Cổng HD2 theo gói WP-C2…C5 vào `GET /gates` | fls-dev #FE ↩ làn BE-CF | W10 | CG1, H4 | 2–3h | `planned` | — |
| 31 | `DT7` | Ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (414–419) | fls-dev #DATA | W10 | DT2 | 3–4h | `planned` | — |
| 32 | `H7` | CA.GL dòng HR + SO.CFA3 | fls-dev #HC | W11 | H6, DT6, C8 | 3–4h | `planned` | — |
| 33 | `C7` | IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1) | fls-dev #CF | W11 | C5 | 2–3h | `planned` | — |
| 34 | `DT9` | Ảnh đáp án MID1–MID3 của OMC · SC · PS | fls-dev #DATA | W11 | DT8 | 3–4h | `planned` | — |
| 35 | `H11` | AL.PLT · OMC · SC · PS | fls-dev #HC | W12 | H10, DT9 | 2–4h | `planned` | — |
| 36 | `C13` | IX.TMP: bản báo cáo ký có phiên bản (snapshot sign-off) | fls-dev #CF | W12 | C7 | 2–3h | `planned` | — |
| 37 | `F5` | SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận | fls-dev #FE | W12 | F4, C7 | 3–4h | `planned` | — |
| 38 | `DT12` | Ảnh Manual input của 22 kỳ còn lại (chế độ tự sinh AC10) | fls-dev #DATA | W12 | DT2 | 3–4h | `planned` | — |
| 39 | `H8` | SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá | fls-dev #HC | W13 | H7, DT7, C6 | 3–4h | `planned` | — |
| 40 | `F7` | SCR-F08 ký bản Daily Report 3 (IX.TMP snapshot) | fls-dev #FE | W13 | F5, C13 | 2–3h | `planned` | — |
| 41 | `DT11` | Ảnh đáp án Daily Report 2 · 3 (607–616) | fls-dev #DATA | W13 | DT2 | 3–4h | `planned` | — |
| 42 | `H12` | AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2) | fls-dev #HC | W14 | H8, H11, C10, C11, DT10 | 3–4h | `planned` | — |
| 43 | `H15` | HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho 22 kỳ còn lại) | fls-dev #FE ↩ làn BE-HC | W14 | H3, DT12 | 3–4h | `planned` | — |
| 44 | `H13` | SO.PLA3-ATL + IX.PL CHECK | fls-dev #HC | W15 | H12, C12 | 2–4h | `planned` | — |
| 45 | `I1` | Tích hợp HD1 xuyên suốt: ảnh → ghép → cổng theo kỳ → `GET /gates` → F03 | fls-dev #DATA | W15 | H15, H3, CG1, FG | 3–4h | `planned` | — |
| 46 | `H14` | RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5) | fls-dev #HC | W16 | H13, DT11, C13 | 3–4h | `planned` | — |
| 47 | `I2` | Tích hợp HD2 xuyên suốt: config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản | fls-dev #HC | W17 | H14, C13, CG2, F7, I1 | 3–4h | `planned` | — |

## Nhật ký orchestrator

| Ngày | Sự kiện |
|---|---|
| 2026-11-16 | người dùng xác nhận ISP 3.1.2 + mọi khuyến nghị; phát `WO-065` (Step 0) cho agent BE-CF; dải phiếu S0: WO-065 · BG-066 · KQ-067/068/069 |
| 2026-11-16 | **O7 thăm dò (chỉ đọc, connector của phiên):** thư mục Drive AS-IS có **25 mục** (đếm 2 trang tìm): 22 sheet `[COPY]` + 1 sheet `[FS2] PD Now – Logic & Rules script` (phiên 13/11 tạo) + 1 tài liệu nháp + 1 thư mục `[COPY] Payroll`; mọi mục tạo 13/11. `[COPY] APERO \| FS2 (nguồn tỷ giá)` → sheet `9.2.Exchange Rate` **đọc được giá trị**: 37 dòng dữ liệu (202401…202512 = 24 · 202306 lạc · 202601…202612 = 12) — khớp AP §3.2.1. ⛔⛔ **Bẫy cho DT2:** `get_values` trả số **ĐÃ ĐỊNH DẠNG** — SGD 202507 hiện `20,692` mà `effectiveValue` = **20691.51** ⇒ đóng băng phải đọc `effectiveValue` (`get_spreadsheet` + `includeGridData`), ⛔ đọc chuỗi hiển thị. |
| 2026-11-16 | **O10 thăm dò:** sheet RAW GỐC `1md85t…` ⇒ **Permission denied** với tài khoản connector. Bản sao `[COPY] ITL I Input Transaction Ledger File 1/2 (RAW)` đọc được metadata: có `Transaction Mapping L1` (lưới 12.888 hàng) · `Mapping Master` (4.464 × 40). Cột khoá phía sổ (`ITL Ledge`) nằm ở bản ADJUSTED — `GAP-ORA-08` (ADJUSTED ⛔ trả giá trị qua API) chưa thử trên bản sao. ⇒ DT1b: thử bản sao ADJUSTED trước; bản sao là của 13/11 còn ảnh là 26/08 ⇒ ghép theo KHOÁ, ⛔ theo vị trí dòng; hỏng thì về máy owner (O10 = A). |
| 2026-11-16 | **S0 bàn giao** (`BG-066`, nhánh `isp/S0` @ `d6cc31d`): AC-1…AC-6 đạt theo agent. Đường nền: pytest `12 failed · 2402 passed · 2 xfailed · 14 errors` trên **2.430 bài thu thập** — 26 bài đỏ đều là bài đọc SỔ THẬT đỏ vì kho `fls` cục bộ rỗng; tập đỏ trùng khít bản gốc `39524c5` (26 = 26 theo node id) · `tests/web` `3 failed · 661 passed` · `lint-imports` 11 kept · 26/26 di trú · `kiem_so_song` ⛔ ĐO ĐƯỢC ở container (gọi cứng `.venv/Scripts/lint-imports.exe`, đọc kho thật) · `khop_owner --kiem` 11/16 (5 phép đếm từ kho rỗng). Phát `R1` (`KQ-067`). |
| 2026-11-16 | **Quyết định orchestrator trên 4 câu của S0:** Q1 = **A** (cụm theo cổng — sửa trong vòng sau R1, nằm trong phạm vi S0 'môi trường test'); B (đổi 24 dòng bài sang `ten_kho(dsn_test())`) để sau, cần WO riêng có `fls-test` vì chạm `nghiem_thu`. Q2: số ghim `9 kept` ở dashboard:137 · `08_MIGRATION_ROADMAP.md:45` · `CLAUDE.md` sẽ lệch 11 sau gộp — chờ máy owner chạy `dong_bo_so_song --ghi`; `CLAUDE.md` để người dùng quyết. Q3: chấp nhận đo AC-4 trên hàng `Σ`. Q4 (`fls.kiem` ⛔ có hợp đồng tầng) ngoài ISP — đề xuất việc riêng. |
| 2026-11-16 | **R1 S0 xong** (`KQ-067` @ `afb9e3a`): **ĐẠT vòng R1** — 0 CHẶN · 2 NÊN SỬA (`S0-R1-01` chốt `PG_DSN` lọt 3 đường · `S0-R1-02` đường nền ⛔ máy so tập bài đỏ) · 8 GHI NHẬN; sổ phát hiện `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` mở. Theo luật (khuyến nghị R1 được làm theo): phát vòng sửa cho agent BE-CF — 2 NÊN SỬA + `S0-R1-03/04/05/06/07/10` + Q1 (cụm theo cổng). `S0-R1-08` (changelog): **từ W1, `08_CHANGELOG_RELEASE.md` do orchestrator ghi lúc gộp** (bốn làn cùng chèn đầu một bảng ⇒ xung đột). Container khởi động lại một lần trong lúc chờ — R1 đã commit trước đó, ⛔ mất gì. |
| 2026-11-16 | **Người dùng chốt:** (1) **tự chạy theo wave** — mỗi bước vẫn đủ 3 vòng review rồi mới push; chỉ dừng khi có quyết định hoặc bị chặn; báo sau mỗi wave. (2) **sửa số `9` → `11` hợp đồng tầng lúc gộp S0** ở `CLAUDE.md` + dashboard + `08_MIGRATION_ROADMAP.md` (orchestrator gộp thêm `NFR-I16` của `08_NFR.md` — cùng một sự thật, `S0-R1-07`). |
