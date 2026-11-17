# WO-111 — ISP 3.1.2 · Step 12 · DT4: ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT)

| | |
|---|---|
| **Trạng thái** | `MO` — giao khi DT3 dựng lại xong (nền) |
| **Phát bởi** | orchestrator (phiên điều phối ISP, account mới) · 2026-11-17 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (người dùng 17/11: việc mới chạy ở phiên cloud, model Opus 4.8 · medium) · cụm PG **5437** của phiên ấy · nhánh `isp/DT4` |
| **Nền** | ngọn `claude/bold-galileo-zukpaf-isp/DT3` sau vòng dựng lại + sửa R1 DT3 (= `isp/DT2` đã sửa R2 `d46e817` + DT3) — `DT3-R1-07`: công cụ chung `tools/dong_bang_sheet.py` một dòng lịch sử |
| **Dải phiếu** | `BG-112` (bàn giao) · `KQ-113` (R1) · `KQ-114` (R2) · `KQ-115` (R3). Số trống kế tiếp: **116** |

## Vì sao
- ISP **Step 12 · DT4** — nguồn sự thật duy nhất. Phụ thuộc DT2: bàn giao `BG-086`, R1 `KQ-087` · R2 `KQ-088` đều **0 CHẶN** (chế độ tăng tốc). `B-DATA-3` gỡ 17/11 (khoá SA chỉ-đọc).
- Đầu ra là đáp án cho **H4** (parity CA.GL ↔ 406, theo dòng × kỳ, 8 cột BM…BT).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 12** (· Step 1 H1 để biết BM…BT) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.3.1 PD 406 · §3.5.4 WP-C2 | 3.1.2 |
| `01_Orchestrator/isp-3.1/CALC_ZONE_406.md` | bản đồ cột + công thức BM…BT, hai ngữ nghĩa tra tỷ giá | 16/11 |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` | khuôn mẫu DT2 · DT3 (hợp đồng bản thô = LƯỚI SA) | nền |
| `tests/fixture/itl_ledge_adjustment.json` | `phan_bo_ky` (mẫu so DT4-B1) | — |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — orchestrator đọc trước 17/11 (O7), phiên cloud TỰ đọc lại bằng khoá SA
Bản sao `[COPY] Report I General Ledger | P&L Report` · id `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` · sheet **`Report I General Ledger`** (lưới 21.238 hàng × 119 cột).

| Đo 17/11 (Sheets API · `UNFORMATTED_VALUE` · `SERIAL_NUMBER`) | Giá trị |
|---|---|
| Hàng tiêu đề | 7–9 (bản đồ cột ở `CALC_ZONE_406.md`); dữ liệu từ hàng **10** |
| Dòng dữ liệu (cột A có ngày, số serial `int`) | **7.883** = hàng 10 … 7.892; cột A **tăng dần** (⛔ giảm) |
| `BM10:BT7892` | **0** ô lỗi · **6** ô rỗng (đều ở BO · BP — `iferror` của `INDEX/MATCH`) |
| Hàng 7.893 … 17.735 | **9.843** hàng chỉ có công thức, mọi ô BM…BU = `#DIV/0!`, cột A rỗng ⇒ ⛔ thuộc ảnh (phải ĐẾM + khai, ⛔ lặng lẽ bỏ) |
| Phân bố kỳ (tháng của cột A) | khớp ĐÚNG `phan_bo_ky` của `itl_ledge_adjustment.json` ở **21 kỳ** 2024-10 … 2026-04; **2026-05: 239 ≠ 537**; **2026-06 · 2026-07 · 2026-08: vắng** (bản sao 406 dừng giữa 2026-05) |
| Thời gian đọc | ~9 s mỗi vùng ~10⁴ hàng (⛔ hết giờ) |

- ⛔⛔ **PII:** cột **B (Số chứng từ)** và **C (Diễn giải)** — ⛔ ĐỌC (vùng đọc không được phủ B:C). Các cột khác của A…AW ngoài danh sách dưới ⛔ đọc.
- Bản thô chỉ ở `/tmp` của phiên cloud (người dùng 17/11, O7 cho phiên cloud) — ⛔ commit.

## Quyết định orchestrator *(ghi errata cho bản vá ISP)*
- **② (errata đã có):** ISP §3 ghi BM–BT là "tiền theo 5 tiền tệ, bVND, mUSD" ⇒ SAI. 5 tiền tệ là `AX:BL`. **BM…BT là 8 cột:** `BM` tồn ALL quy VND · `BN` tồn ALL mUSD · `BO`/`BP` PS Nợ/Có bVND · `BQ` tồn bVND · `BR`/`BS` PS Nợ/Có mUSD · `BT` tồn mUSD (`CALC_ZONE_406.md`). Mỗi cột trong ảnh mang ĐƠN VỊ (Đ4).
- **⑯ Khoá + cột mang theo:** khoá `dong_sheet` (số nguyên, hàng sheet) — đúng ISP; thêm `ky` (`yyyymm` kiểu `int`, errata ⑦, suy từ cột A) và **`itl_id` (cột R "ITL ID")** để H4 nối dòng 406 ↔ dòng sổ mà ⛔ dựa vào thứ tự (cột R ⛔ PII). Cột D (tiền tệ) mang theo nếu rẻ (chẩn đoán lệch H4). ⛔ mang cột nào khác.
- **Giữ NGUYÊN thứ tự dòng** (ISP §3 giới hạn: tồn lũy kế AS-IS phụ thuộc thứ tự).
- **Số giữ y giá trị API trả** (số JSON; ⛔ làm tròn, ⛔ định dạng) — dung sai là việc của H4 (`CALC_ZONE_406.md` §H4).
- **Đọc theo lát kỳ** (ISP Scope): đọc cột A trước để lập dải hàng mỗi kỳ, rồi đọc `BM:BT` (+ R, D) theo từng dải; mỗi lát kiểm: số hàng về = số hàng của dải; lát rỗng hoặc hỏng ⇒ **ĐỎ** (⛔ "không thấy lệch").
- Ô rỗng BO/BP: cho phép, ĐẾM theo cột và kỳ, khai trong ảnh (`mong` = 6 đo 17/11); khác ⇒ ĐỎ.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT4-B1) | `tests/fixture/dap_an/gl_406.json`: **7.883** dòng; Σ dòng theo kỳ = `phan_bo_ky` của `itl_ledge_adjustment.json` ở 21 kỳ, và **lệch CÓ TÊN** đúng 4 kỳ: `2026-05` 239/537 · `2026-06` 0/613 · `2026-07` 0/686 · `2026-08` 0/487 (nguyên nhân: bản sao 406 dừng giữa 2026-05). Lệch nào khác ⇒ ĐỎ | `tests/du_lieu/test_dap_an_406.py` + cổng `tools/dong_bang_sheet.py gl_406 … --mong 7883` | ảnh chưa có |
| AC-2 (DT4-B2) | một lát kỳ trả RỖNG ⇒ ĐỎ (Đ3: mẫu số 0 là kết quả) — ca phá trên BẢN SAO; trả nguyên ⇒ xanh, ảnh đúng từng byte | ghi lệnh + exit | — |
| AC-3 (DT4-B3) | ⛔ PII: ảnh có **0** cột Diễn giải / Số chứng từ / Email; máy quét có ca phá; vùng đọc ⛔ phủ B:C | pytest | — |
| AC-4 | khuôn mới = tệp riêng `tools/khuon_dong_bang/gl_406.py`; sửa công cụ chung chỉ khi bài đòi (khai lý do, giữ mọi bài DT2 · DT3 xanh + `ix_fx.json` đúng từng byte) | diff | — |
| AC-5 | 9.843 hàng công thức thừa dưới dữ liệu: ĐẾM + khai, ⛔ vào bảng chính; hàng có ngày mà BM…BT lỗi ⇒ ĐỎ | pytest | — |
| AC-6 (Q8) | nhánh ⛔ có `MONG_PYTEST_TOAN_BO` ⇒ ghi số `--collect-only` trước → sau vào BG (orchestrator đặt sàn lúc gộp) | — | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Đầu ra là ảnh JSON đã commit (dự kiến ~1–2 MB; khuôn dạng `{cot, dong}` gọn như DT2).

## Câu còn treo
- không có.
