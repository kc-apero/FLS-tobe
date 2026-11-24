# WO-355 — 4 agent Voi: MỘT nhà cung cấp Anthropic (Opus 5.5 · Sonnet 5.5), gọi API THẬT, bắt đầu test

| | |
|---|---|
| **Trạng thái** | `MO` — 23/11 ~12:50 UTC |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` — phiên cloud Opus 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/AG2` (nền = ngọn nhánh làm việc: AG + HELD đã gộp) |
| **Dải phiếu** | `BG-356` · `KQ-357` (R1) · `KQ-358` (R2 cuối). Số trống kế tiếp sau dải: **359** |

## Vì sao — lời chủ 23/11 ~12:45
> *"Lấy 4 agents mới nhất, nạp vào model và bắt đầu test. Tránh phức tạp, giai đoạn này tạm thời dùng duy nhất 1 bên cung cấp là Anthropic, dùng opus 5.5 và sonnet 5.5. Giai đoạn sau sẽ dùng các model khác của OpenAI, không dùng gemini nữa."*
- ⇒ **THAY** quyết C1/C2 (BG-330): một nhà cung cấp **Anthropic**; agent LÀM (A1 · A2 · A3) = **`claude-opus-5-5`**; agent KIỂM / A4 phần dùng mô hình = **`claude-sonnet-5-5`** (A4 phán cuối vẫn là MÃ `doi_chieu`); **bỏ Gemini** (`GEMINI_FLASH`, nhà cung cấp `google`); chừa chỗ nhà cung cấp **OpenAI** cho giai đoạn sau (giao diện, ⛔ dựng adapter bây giờ).
- Quyết chủ còn hiệu lực: agent đọc TOÀN BỘ nội dung + số TK (bộ che mặc định `mo`); G0 BÓNG — ⛔ ghi kho/sổ; A2.04 siết.
- Khoá: `fls/agent/mo_hinh.py:60` đọc **`ANTHROPIC_API_KEY`** — chủ thêm vào biến môi trường của environment (⛔ repo/chat). Phiên tạo SAU khi chủ thêm mới thấy khoá.

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 · nhà cung cấp | `mo_hinh.py`: chỉ họ `anthropic` (Opus 5.5 · Sonnet 5.5 ghim, ⛔ bí danh); xoá Gemini + mọi nhánh `google`; giao diện nhà cung cấp còn mở cho `openai` (⛔ adapter); thẻ agent + zip sinh lại ghi đúng mô hình từng skill | pytest + `sinh_the_agent.py --zip` |
| AC-2 · gọi thật đúng chuẩn | adapter Anthropic dùng SDK `anthropic` chính thức (tra skill `claude-api` — ⛔ đoán tham số); 3 chốt giữ nguyên (`--that` · `FLS_CHO_GOI_API=1` · khoá); ghi mỗi lời gọi: mô hình · token vào/ra · thời gian · chi phí ước (bảng giá ghi ngày tra) vào nhật ký vòng; lỗi API ⇒ ĐỎ có tên (⛔ rơi về GIẢ im lặng) | pytest (SDK giả) |
| AC-3 · test THẬT vòng 1 | KHI có khoá: chạy (a) **chuỗi 4 agent** trên tập nhỏ có đáp án (ca dựng 12 + mẫu ≤ 20 ca từ bể giữ riêng — dựng lại bể từ nguồn sống bằng `tools/dung_be_giu_rieng.py`, ngoài repo) và (b) **fleet eval A2.04** trên bể A/B với Opus thật ⇒ report MỘT trang: cột GIẢ ↔ THẬT, recall · nối sai · ca phải-để-người bị nối · ô độc lập khớp/lệch, token + chi phí. Chưa có khoá ⇒ AC-3 = ĐỎ có tên "thiếu ANTHROPIC_API_KEY", ⛔ bịa số | report + BG |
| AC-4 · an toàn | ⛔ ghi kho/sổ (G0 bóng); nội dung gửi API theo quyết chủ (đọc toàn bộ) — nhưng ⛔ ghi nội dung/phản hồi thô vào repo (chỉ số đếm + vân tay); khoá ⛔ in/log | pytest + `quet_pii_repo` 0 |
| AC-5 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` 11 kept | `--duong-nen` |
