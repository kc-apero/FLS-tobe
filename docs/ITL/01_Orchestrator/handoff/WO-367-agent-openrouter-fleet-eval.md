# WO-367 — 4 agent Voi gọi mô hình qua **OpenRouter** (thay Vertex) + **fleet eval đa mô hình** tự động

| | |
|---|---|
| **Trạng thái** | `MO` — 27/11 |
| **Phát bởi** | orchestrator · 2026-11-27 |
| **Nhận** | `fls-dev` — phiên cloud Opus 5.5 · nhánh `claude/bold-galileo-zukpaf-isp/OR` (nền = nhánh làm việc `aeef154`: đã gộp AG3 — 3 đường `anthropic` · `google-cloud` · `vertex`) |
| **Dải phiếu** | `BG-368` · `KQ-369` (R1) · `KQ-370` (R2 cuối). Số trống kế tiếp sau dải: **371** |

## Vì sao — lời chủ 27/11
> *"Chuyển việc dùng Vertex sang dùng OpenRouter. Nếu không thể fleet eval tự động thì tạo thêm cổng MCP với tài khoản Claude này, Claude này sẽ fleet eval với các model trên Open Router"*

Đo trước khi giao (Đ1/Đ3, 25/11 — `TIEN_DO`):
- Vertex: 2 mô hình *Enable* xong, nhưng hạn mức `global_online_prediction_requests_per_base_model` của `anthropic-claude-opus` · `anthropic-claude-sonnet` = **0**; 6 yêu cầu tăng ⇒ **Denied tự động** *("wait 48h … or until your Billing account has additional history")*. `claude.googleapis.com` chặn ở Subscribe Marketplace (chủ ⛔ quản trị billing). ⇒ **0** đường GCP gọi được.
- `git grep -il openrouter -- fls tools docs` trên nhánh làm việc `aeef154` = **0** tệp — chưa có gì.
- Fleet eval: `tools/fleet_eval_voi.py` ĐÃ CÓ (`WO-338` — bể giữ riêng A/B, chế độ `mo` qua `chay_skill`) ⇒ fleet eval TỰ ĐỘNG khả thi; việc là thêm đường OpenRouter + ma trận mô hình. **Cổng MCP chỉ là dự phòng** (AC-7) — làm khi AC-1…AC-5 chứng minh ⛔ được.

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 · đường `openrouter` | `fls/agent/mo_hinh.py`: thêm `DUONG_OPENROUTER = "openrouter"` vào `DUONG_HOP_LE`; adapter gọi API OpenRouter (giao diện kiểu OpenAI *chat completions* — **TRA tài liệu OpenRouter hiện hành** `openrouter.ai/docs`: URL, header, tên trường usage/giá; ⛔ đoán) bằng `requests` (đã có trong `requirements.txt`) hoặc gói chính thức nếu tài liệu khuyên — DỊCH đúng hợp đồng nội bộ (`LuotGoi`, token vào/ra, lỗi có tên). `HO_DE_DANH` `openai` nay có adapter qua OpenRouter. Khoá: biến `OPENROUTER_API_KEY` (⛔ repo/log/argv/BÁO CÁO — bài grep `sk-or-` ngoài `tests/` = 0). Biến vắng `FLS_NHA_CUNG_CAP` ⇒ GIỮ mặc định `anthropic` (19/27 bài `KQ-357` khoá hành vi ấy) | pytest SDK/HTTP giả + máy chủ cục bộ `127.0.0.1` (⛔ mạng ngoài) |
| AC-2 · chốt dữ liệu + chi phí | 3 chốt giữ (`--that` · `FLS_CHO_GOI_API=1` · trần USD). Chốt MỚI `FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1` (OpenRouter là BÊN THỨ BA chuyển tiếp tới nhà cung cấp gốc — dữ liệu sổ thật, số TK, tên người). Mỗi lời gọi gửi tuỳ chọn định tuyến **⛔ thu thập dữ liệu / chỉ nhà cung cấp ZDR** nếu tài liệu OpenRouter có (TRA: tên trường `provider`…; ghi nguồn + ngày) — thiếu chốt ⇒ ĐỎ trước khi gửi byte nào. Giá: lấy từ `usage`/trường chi phí OpenRouter trả về nếu có (ưu tiên), không thì bảng giá `GET /api/v1/models` (ghi ngày tra) — USD in ra mang nhãn đúng nguồn (THẬT do OpenRouter trả · ƯỚC) | pytest: 0 lời gọi khi thiếu từng chốt (đếm) |
| AC-3 · ma trận mô hình | Cấu hình MỘT chỗ (tệp/biến) danh sách mô hình OpenRouter cho từng vai (3 agent làm · 1 Auditor) + danh sách **ứng viên fleet eval**. Mặc định: `anthropic/` Opus 5.5 (làm) + Sonnet 5.5 (Auditor) — slug THẬT lấy từ `GET /api/v1/models` (⛔ đoán slug). ⛔ Gemini / `google/*` (quyết chủ 23/11) — bài canh. Ứng viên khác (vd. `openai/*` — chủ 23/11: *"giai đoạn sau dùng OpenAI"*) để chủ chọn ở câu C1 | pytest |
| AC-4 · fleet eval tự động đa mô hình | `tools/fleet_eval_voi.py` (+ `vong_that_voi.py` nếu cần) chạy ma trận *ứng viên × bể A/B*: mỗi ô = cùng bộ ca, cùng skill, chỉ đổi mô hình; grader/ A4 so từng ô với số máy đã đo (⛔ mô hình tự chấm mình); report MỘT trang: ma trận mô hình × chỉ số (đúng/sai/phải-để-người/lỗi · token · USD + nhãn nguồn · thời gian) + so ngược bản trước. Trần USD theo TỔNG lượt + theo mô hình; chạm trần ⇒ dừng lời KẾ, nhật ký ghi mọi lối thoát (`AG3-R1-01`) | pytest giả + 1 lượt chạy GIẢ trọn ma trận |
| AC-5 · script cho CHỦ | `tools/staging/09_openrouter_agent.sh --project fp-a-project [--kiem]` (hoặc mở rộng 06 `--duong openrouter` — Dev chọn, ghi lý do): đọc khoá bằng `read -s` ⇒ Secret Manager `fls-staging-openrouter-key` (⛔ argv/echo) · cấp SA `fls-staging-app` `secretAccessor` CHỈ trên bí mật ấy (`--condition=None` không cần cho binding mức bí mật — nếu có binding mức dự án thì PHẢI `--condition=None`) · `--kiem`: khoá đọc được · `GET /models` 200 · 1 lời gọi 1-token mỗi mô hình mặc định = 200 · mô hình trả về = slug ghim · trần · BÁO CÁO có `mong`, ĐỎ hai chiều, 429/402 in TÊN nguyên nhân (hết credit / giới hạn) ⛔ câu chung (bài học `AG3-GOP-01`). Khối lệnh e2e Cloud Shell trong BG: tập nhỏ trần 2 USD ⇒ bể A/B ⇒ fleet eval | pytest gcloud/curl GIẢ |
| AC-6 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit; ⛔ cổng 5433 — dùng 5434–5437); `kiem_tai_lieu` · `lint-imports` 11 kept · `quet_pii_repo` 0; `requirements.txt` đủ mọi import mới (bài canh `AG2-R1-01`) | `--duong-nen` |
| AC-7 · **dự phòng** cổng MCP | CHỈ làm nếu AC-4 chứng minh ⛔ tự động được (ghi bằng chứng): máy chủ MCP nhỏ (`tools/mcp_openrouter/`) mở công cụ `goi_mo_hinh(slug, thong_diep)` + `chay_ca(ca_id, slug)` + `cham_o(...)` để một phiên Claude điều phối fleet eval; cùng chốt AC-2, cùng trần, cùng nhật ký | — |

## Câu cho chủ (Dev ghi ở BG, ⛔ tự quyết)
- **C1 · ứng viên fleet eval**: danh sách mô hình OpenRouter muốn so (Dev in danh sách slug THẬT còn hiệu lực của Anthropic + OpenAI kèm giá/ngữ cảnh để chủ chọn).
- **C2 · dữ liệu qua bên thứ ba**: OpenRouter nhận nội dung sổ thật (số TK, tên người, tiền) rồi chuyển tiếp — chủ xác nhận + bật cài đặt riêng tư ở tài khoản OpenRouter (tắt lưu prompt/huấn luyện) TRƯỚC khi đặt `FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1`.

## Luật
⛔ GCP thật · ⛔ gọi API thật (phiên cloud — CHỦ chạy) · ⛔ khoá/nội dung trả lời vào repo · ⛔ `docker compose down` · ⛔ sửa bài nghiệm thu `tests/nghiem_thu/` · sổ phát hiện 10 cột · Đ1–Đ5.
