# WO-184 — ISP 3.1.2 · Step 26 · C12: IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-CF** — phiên cloud **Sonnet 5.5** medium · cụm PG **5446** · nhánh `isp/C12` |
| **Nền** | ngọn nhánh làm việc — phụ thuộc đã gộp: C4 (cây IX.HD) · C5 (kho config) |
| **Dải phiếu** | `BG-185` · `KQ-186` (R1) · `KQ-187` (R2 cuối). Số trống kế tiếp: **188** |

## Spec — nguồn sự thật
ISP `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 26** (mục 2 Goal · 3 Scope · 6 Test cases · 8 Exit) + AP v3.1.2 các mục Traceability của Step. Khuôn đã gộp: C1/C4/C5/C6/C8/C9 (`fls/cau_hinh/*.py` · `fls/repo/cau_hinh_repo.py` · tuyến tĩnh→kho · `?run_id=` ⇒ 400 · lỗi có TÊN · chỉ-thêm `0027`, ⛔ di trú mới trừ khi Step ghi rõ · `nap()` kiểm nội dung TRƯỚC khi ghi — luật `C5-R1-04`).

## Lưu ý orchestrator
- Bộ phân tích biểu thức cộng/trừ trên mã HD: lỗi cú pháp/mã lạ ⇒ lỗi có TÊN; ⛔ `eval`.
- Bài học đã gặp: ⛔ chép số TK cá nhân / giá trị thật vào bài (`C8-R1-01`); oracle phải đo trên tập KHÔNG rỗng (`C8-R1-02`); lỗi có tên phải có bài (`C8-R1-03`); INSERT kho chỉ qua `ghi_tay.py` (`test_chi_mot_cho_ghi_tay`).

## Tiêu chí nghiệm thu
- **AC = đúng từng test case mục 6 của Step 26** (mỗi ID một bài, ĐỎ trước — ghi lệnh + kết quả đỏ vào BG). Số đo ở dữ liệu thật (ảnh repo) khác số ISP ⇒ ⛔ sửa cho khớp — báo bằng số đếm (Đ4).
- Tuyến mới (nếu có): `tools/soi_bang_tuyen.py` ĐẠT; dòng `07_API_CONTRACT.md` §4i do orchestrator đổi lúc gộp.
- Q8: nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` MỘT lần cuối — ĐỎ thì sửa rồi chạy lại MỘT lần nữa (⛔ bàn giao khi tập đỏ ≠ 28).

## Dữ liệu
Ghi kho THẬT: `KHONG`. ⛔ Drive.
