# WO-359 — 4 agent Voi gọi Claude qua **Vertex AI trên GCP** (`fp-a-project`) + chạy test e2e trên staging

| | |
|---|---|
| **Trạng thái** | `MO` — 24/11 ~03:20 UTC |
| **Phát bởi** | orchestrator · 2026-11-24 |
| **Nhận** | `fls-dev` — phiên cloud Opus 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/AG3` (nền = ngọn `isp/AG2` `5b6c525`: một nhà cung cấp Anthropic, đường gọi thật bằng `ANTHROPIC_API_KEY`) |
| **Dải phiếu** | `BG-360` · `KQ-361` (R1) · `KQ-362` (R2 cuối). Số trống kế tiếp sau dải: **363** |

## Vì sao — lời chủ 24/11 ~03:15
> *"hôm trước tôi đã xác nhận rằng sẽ dùng claude trực tiếp trong GCP, thông qua vertex AI và nạp vào 4 agents để bắt đầu test e2e"*
- Đo (Đ1): `git grep -i vertex` trên `docs/ fls/ tools/` của nhánh làm việc + 6 nhánh bước = **0** — quyết này CHƯA có bản ghi; ghi từ hôm nay (TIEN_DO 24/11).
- ⇒ THAY đường khoá `ANTHROPIC_API_KEY` (WO-355 AC-3) bằng **Claude trên Vertex AI** của project `fp-a-project`: tính tiền qua GCP, xác thực bằng **service account** (⛔ khoá `sk-ant`). Mô hình giữ quyết 23/11: Opus 5.5 làm (A1–A3) · Sonnet 5.5 kiểm (A4 phần mô hình; phán cuối vẫn mã) · ⛔ Gemini · OpenAI giai đoạn sau.
- Claude ⛔ vào GCP (quyết 20/11) ⇒ phiên cloud CHỈ viết mã + script; CHỦ chạy trên GCP (Cloud Shell hoặc VM staging `fls-staging-app` — SA `fls-staging-app`).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 · nhà cung cấp Vertex | `mo_hinh.py`: thêm đường `anthropic-vertex` (client `AnthropicVertex` của SDK `anthropic` — TRA skill `claude-api`: tên lớp, tham số `project_id` · `region`, model id dạng Vertex của Opus 5.5 / Sonnet 5.5, region hỗ trợ); chọn đường bằng cấu hình (`FLS_NHA_CUNG_CAP=vertex` · `FLS_GCP_PROJECT` · `FLS_VERTEX_REGION`); xác thực ADC/SA (⛔ khoá trong repo); giữ đường API-key làm dự phòng | pytest (client giả) |
| AC-2 · chốt + chi phí | 3 chốt + trần USD giữ nguyên (`--that` · `FLS_CHO_GOI_API=1` · trần); bỏ đòi khoá `ANTHROPIC_API_KEY` khi đường = vertex; thay `FLS_ZDR_DA_BAT` bằng xác nhận phù hợp Vertex (ghi rõ chính sách dữ liệu của Claude trên Vertex — tra, ⛔ đoán; câu chủ nếu cần); nhật ký token + chi phí (giá Vertex, ghi ngày tra) | pytest |
| AC-3 · script GCP cho CHỦ | `tools/staging/06_vertex_agent.sh --project fp-a-project [--kiem]`: bật API `aiplatform.googleapis.com` · kiểm/hướng dẫn bật Claude Opus 5.5 + Sonnet 5.5 trong **Model Garden** (bước bấm tay nếu API không làm được — ghi rõ) · cấp `roles/aiplatform.user` cho SA `fls-staging-app` · gọi THỬ 1 lời nhỏ mỗi mô hình ⇒ BÁO CÁO có `mong`, ĐỎ hai chiều, ⛔ in khoá/token | bài với gcloud GIẢ + BG |
| AC-4 · test e2e trên staging | lệnh CHỦ chạy (Cloud Shell hoặc trong VM) để: dựng bể giữ riêng từ nguồn sống (ngoài repo) ⇒ chạy chuỗi 4 agent THẬT (tập nhỏ trước, xem chi phí, rồi bể A/B) ⇒ report MỘT trang GIẢ ↔ THẬT (recall · nối sai · ca phải-để-người bị nối · ô độc lập · token · USD); G0 BÓNG ⛔ ghi kho staging | BG (khối lệnh + mong) |
| AC-5 · an toàn | ⛔ nội dung/phản hồi thô vào repo; ⛔ khoá; `quet_pii_repo` 0; agent đọc toàn bộ nội dung + số TK (quyết chủ 23/11) chỉ trong GCP của công ty | pytest |
| AC-6 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` | `--duong-nen` |
