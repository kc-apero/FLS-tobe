# WO-192 — ISP 3.1.2 · Step 23 · DT6: ảnh đáp án GL HR + CFA3 (PD 407 · 408 · 412 · 413)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~20:35 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5436** của phiên ấy · nhánh `isp/DT6` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT2…DT5 · DT8 — công cụ chung `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`) |
| **Dải phiếu** | `BG-193` · `KQ-194` (R1) · `KQ-195` (R2). Số trống kế tiếp: **196** |

## Vì sao
- ISP **Step 23 · DT6** (wave W8) — nguồn sự thật duy nhất. Phụ thuộc Step 8 · DT2 (đã gộp). Đầu ra là đáp án cho bước engine HR (Q3: HR ⛔ qua ALLOCATE) và CFA3.

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 23** (· Step 15 DT5 · Step 19 DT8 làm khuôn) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.3.1 PD 401–404 · **407 · 408 · 412 · 413** · Q3 | 3.1.2 |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` | khuôn DT2…DT8 (hợp đồng bản thô = LƯỚI SA) | nền |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA
- Sheet PD **407 · 408** (GL HR) và **412 · 413** (CFA3) theo tên AP §3.3.1. Tìm bằng `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_ds.py` + `sa_meta.py`; ưu tiên bản `[COPY]`. **Tên không khớp AP, ≥ 2 ứng viên, hoặc 403 ⇒ DỪNG, báo bằng tin nhắn cuối kèm danh sách ứng viên (id + tên + kích thước lưới) và khuyến nghị** — ⛔ đoán.
- Đọc GIÁ TRỊ bằng `UNFORMATTED_VALUE` (⛔ `FORMATTED_VALUE` — bài học DT1b).
- ⛔⛔ **PII (HR có tên người):** lập bản đồ cột bằng hàng tiêu đề TRƯỚC, đọc vùng hẹp; ⛔ đọc cột tên · email · Diễn giải · Số chứng từ · số tài khoản cá nhân. Bản thô chỉ ở `/tmp` của phiên (chmod 600) — ⛔ commit, xoá sau dùng.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT6-B1) | `tests/fixture/dap_an/gl_hr.json` + `cfa3.json`; kỳ ⊂ **2025** (AS-IS chỉ có sheet Y2025) và cổng IN rõ điều đó; số dòng theo kỳ khai MONG trước (Đ5 hai chiều; tập rỗng ⇒ ĐỎ, Đ3); mỗi số kèm nhãn nó đếm gì (Đ4) | cổng `dong_bang_sheet.py … --mong` + `tests/du_lieu/…` | ảnh chưa có |
| AC-2 (DT6-B2) | PII: ảnh **0** cột tên/email; mã nhân sự băm hoặc bỏ (khai cách nào + lý do); máy quét có ca phá; lời lỗi ⛔ in giá trị ô (luật `DT5-R1-02`) | pytest | — |
| AC-3 | H1000 Y2024 đi bằng IMPORTRANGE — đọc ⛔ được ⇒ ghi `thiếu Y2024` có tên trong ảnh + BG (⛔ suy, ⛔ hoá 0) | pytest | — |
| AC-4 | `#REF!`/`#N/A` ở nguồn ghi NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố (luật `DT5-R1-04`) | pytest | — |
| AC-5 | khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; sửa công cụ chung chỉ khi bài đòi (khai lý do; mọi ảnh DT2…DT8 đúng từng byte) | diff | — |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Ảnh BG ghi kích thước + NGUYÊN NHÂN nếu > 2 MB (luật `DT4-R1-07`).

## Câu còn treo
- không có.
