# WO-172 — ISP 3.1.2 · Step 21 · C9: IX.VEN: vendor · network · CDT1 + cột 'cách tính'

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-CF** — phiên cloud **Sonnet 5.5** medium · cụm PG **5434** · nhánh `isp/C9` |
| **Nền** | ngọn nhánh làm việc — phụ thuộc đã gộp: C5 (kho config) · DT8 (ảnh `ix_ven.json` Block 1 = 42 dòng — errata ㉒) |
| **Dải phiếu** | `BG-173` · `KQ-174` (R1) · `KQ-175` (R2 cuối). Số trống kế tiếp: **176** |

## Spec — nguồn sự thật
ISP `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 21** (mục 2 Goal · 3 Scope · 6 Test cases · 8 Exit) + AP v3.1.2 các mục Traceability của Step. Khuôn đã gộp: C1/C4/C5/C6 (`fls/cau_hinh/*.py` · `fls/repo/cau_hinh_repo.py` · tuyến tĩnh→kho · `?run_id=` ⇒ 400 · lỗi có TÊN · chỉ-thêm `0027`, ⛔ di trú mới trừ khi Step ghi rõ).

## Tiêu chí nghiệm thu
- **AC-1…AC-n = đúng từng test case mục 6 của Step 21** (mỗi ID một bài, ĐỎ trước — ghi lệnh + kết quả đỏ vào BG). Số đo ở dữ liệu thật (ảnh repo) khác số ISP ghi ⇒ ⛔ sửa cho khớp — báo bằng số đếm (Đ4: số nào đếm gì).
- Tuyến mới (nếu Step có): `tools/soi_bang_tuyen.py` ĐẠT; dòng `07_API_CONTRACT.md` §4i do orchestrator đổi lúc gộp (⛔ sửa).
- Q8: nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` MỘT lần cuối.

## Dữ liệu
Ghi kho THẬT: `KHONG`. ⛔ Drive (ảnh đã đóng băng trong repo).
