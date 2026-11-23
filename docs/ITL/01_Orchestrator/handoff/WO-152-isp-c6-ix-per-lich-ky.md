# WO-152 — ISP 3.1.2 · Step 17 · C6: IX.PER — lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (quy trình A–E: Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-CF** — phiên cloud **Sonnet 5.5** medium · cụm PG **5434** · nhánh `isp/C6` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp C5 — kho config chỉ-thêm `0027` + `fls/repo/cau_hinh_repo.py`) |
| **Dải phiếu** | `BG-153` · `KQ-154` (R1) · `KQ-155` (R2 cuối). Số trống kế tiếp: **156** |

## Spec
ISP `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 17** (nguồn sự thật) · AP v3.1.2 §3.2.1 IX.PER · §3.2.4 ("ngày đầu cột… năm ép 2025") · D4 · khuôn C1/C4/C5 (`fls/cau_hinh/fx.py` · `hd.py` · `cau_hinh_repo.py`, tuyến tĩnh→kho, `?run_id=` ⇒ 400).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 (C6-B1) | `ky_cua(2026-11-05)` ⇒ Y2026 · H2 · Q4 · M11 (⛔ ép 2025) | đơn vị, ĐỎ trước |
| AC-2 (C6-B2) | `ky_cua(2024-12-31)` ⇒ Y2024 (năm của chính dữ liệu) | đơn vị |
| AC-3 (C6-B3) | luật B (chia đều PL start→end) ⇒ lỗi có tên `LUAT_CHUA_KY`; chỉ luật A ("dồn ngày 1 tháng PL start") chạy | đơn vị |
| AC-4 (C6-B4) | `GET /api/fls/v1/config/per` ⇒ 200 · ngày đầu + luật A đọc từ KHO (dòng config IX.PER qua `0027`, ⛔ di trú mới, ⛔ gõ cứng ngày); kho chưa nạp ⇒ lỗi "chưa khai" có tên | API + `soi_bang_tuyen.py` |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` (MỘT lần cuối) |

## Lưu ý orchestrator
- **Ngày đầu:** ISP ghi 21/10/2024 (sổ ITL). Errata ㉑ (TIEN_DO 18/11): trục CFA1 (đáp án 409) bắt đầu **2024-10-20**. ⇒ C6 lưu ngày đầu là GIÁ TRỊ CẤU HÌNH (nạp vào kho, có nguồn), bài mong 2024-10-21 theo ISP; ⛔ gõ cứng ở mã. Khác biệt 20/21 để H5 đối chiếu (khai trong BG một câu).
- `07_API_CONTRACT.md`: ⛔ sửa (orchestrator đổi dòng `/config/per` lúc gộp).

## Dữ liệu
Ghi kho THẬT: `KHONG`.
