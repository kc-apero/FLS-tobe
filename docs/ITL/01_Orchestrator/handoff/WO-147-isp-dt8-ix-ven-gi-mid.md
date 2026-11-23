# WO-147 — ISP 3.1.2 · Step 19 · DT8: ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~06:15 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Opus 4.8 · medium) · cụm PG **5437** của phiên ấy · nhánh `isp/DT8` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT2 · DT3 · DT4 — công cụ chung `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`) |
| **Dải phiếu** | `BG-148` · `KQ-149` (R1) · `KQ-150` (R2) · `KQ-151` (R3). Số trống kế tiếp: **152** |

## Vì sao
- ISP **Step 19 · DT8** (wave W7) — nguồn sự thật duy nhất. Phụ thuộc duy nhất DT2 (đã gộp). Đầu ra là đáp án cho H9 (AL.PLT · GI vendor thường) và H10 (5 vendor đặc biệt).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 19** (· Step 12 DT4 / Step 15 DT5 làm khuôn) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.2 IX.VEN (Block 1 = 36 dòng `M:S` hàng 4–39 × 7 CDT1; 5 vendor tính riêng VD341 · VD444 · VD428 · 'Max' · VD62) · §3.4.1 PD 503–507 · §3.5.4 WP-C4 | 3.1.2 |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` | khuôn DT2…DT5 (hợp đồng bản thô = LƯỚI SA) | nền |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA
- Sheet PD **503 `Vendor & Network Mapping`** (sổ GI · OMC) và PD **504–507** (`CFA1 | GI Platform Data Ledger` … MID1–MID3 của GI) — AP §3.4.1 nêu tên. Tìm tệp bằng danh sách tệp SA thấy (`docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_ds.py` + `sa_meta.py`); ưu tiên bản `[COPY]`. **Tên sheet/tệp không khớp AP, hoặc có ≥ 2 ứng viên, hoặc 403 ⇒ DỪNG, báo bằng tin nhắn cuối kèm danh sách ứng viên (id + tên + kích thước lưới) và khuyến nghị** — ⛔ đoán.
- ⛔⛔ **PII:** ⛔ đọc cột Diễn giải · Số chứng từ · Email · tên người · số tài khoản cá nhân. Lập bản đồ cột bằng hàng tiêu đề TRƯỚC, đọc vùng hẹp. Bản thô chỉ ở `/tmp` của phiên — ⛔ commit.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT8-B1) | `tests/fixture/cau_hinh/ix_ven.json`: **36** dòng Block 1 × 7 CDT1; cột "cách tính" khai đúng **5** vendor ≠ thường (VD341 · VD444 · VD428 · 'Max' · VD62) — số đo khác ⇒ dừng, báo (Đ4: nói rõ số đếm gì) | `tests/du_lieu/test_dap_an_gi.py` + cổng `dong_bang_sheet.py … --mong` | ảnh chưa có |
| AC-2 (DT8-B2) | `tests/fixture/dap_an/gi_mid1.json` · `gi_mid2.json` · `gi_mid3.json`; cổng tự kiểm **Σ chia MID3 = O / P** trên chính đáp án — số Vendor-tháng lệch khai MONG trước (Đ5 hai chiều; tập rỗng ⇒ ĐỎ, Đ3) | cổng + pytest | — |
| AC-3 | `#REF!`/`#N/A` ở nguồn (U3) ghi NGUYÊN chuỗi, ĐẾM theo cột và ghim phân bố giá trị (luật `DT5-R1-04`), ⛔ hoá 0 | pytest | — |
| AC-4 | PII: ảnh 0 cột cấm; máy quét có ca phá; lời lỗi ⛔ in giá trị ô (luật `DT5-R1-02`); cổng "mã ∈ tập tham chiếu" đo trên tập ĐẦY ĐỦ, ⛔ tập con thưa (luật `DT5-R1-01`) | pytest | — |
| AC-5 | khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; sửa công cụ chung chỉ khi bài đòi (khai lý do; mọi ảnh DT2…DT5 đúng từng byte) | diff | — |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Ảnh BG ghi kích thước + NGUYÊN NHÂN nếu > 2 MB (luật `DT4-R1-07`).

## Câu còn treo
- không có.
