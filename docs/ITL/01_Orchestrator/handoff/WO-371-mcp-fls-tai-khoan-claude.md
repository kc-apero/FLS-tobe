# WO-371 — cổng **MCP FLS**: tài khoản Claude của chủ kết nối vào FLS và **ĐỌC** toàn bộ dữ liệu

| | |
|---|---|
| **Trạng thái** | `MO` — 27/11 ~03:56 UTC |
| **Phát bởi** | orchestrator · 2026-11-27 |
| **Nhận** | `fls-dev` — phiên cloud Opus 5.5 `session_01Ci2qSM4SkDRsCHvvfGwxrq` · nhánh `claude/bold-galileo-zukpaf-isp/MCP` (nền = nhánh làm việc `6f996cf`) |
| **Dải phiếu** | `BG-372` · `KQ-373` (R1) · `KQ-374` (R2 cuối). Số trống kế tiếp sau dải: **375** |

## Vì sao — lời chủ 27/11
> *"Chuyển việc dùng Vertex sang dùng OpenRouter. Nếu không thể fleet eval tự động thì tạo thêm cổng MCP với tài khoản Claude này…"* ⇒ *"vẫn dựng MCP"* ⇒ *"chưa cần thiết đặt API key vào đây, dựng MCP trước, cho phép kết nối tài khoản claude vào FLS để access toàn bộ data."*

- Cổng MCP TÁCH khỏi `WO-367` (OpenRouter + fleet eval — AC-7 cũ BỎ ở đó). Công cụ OpenRouter thêm vào cổng này ở phiếu sau, khi chủ có khoá.
- Chủ cho agent đọc TOÀN BỘ nội dung + số TK (23/11); staging mang dữ liệu THẬT. Quyết 20/11 *"Claude ⛔ vào GCP"* GIỮ: Claude đọc QUA MCP, ⛔ có quyền GCP.
- Quyền **CHỈ ĐỌC** — chủ chưa nói cho ghi; `fls_itl` chỉ-THÊM (`INV-I08`). Ghi = phiếu sau.

## Tiêu chí nghiệm thu
| AC | Mong |
|---|---|
| AC-1 · máy chủ MCP | TRA tài liệu MCP hiện hành (spec — Streamable HTTP, authorization; SDK Python) + tài liệu Anthropic về custom connector / remote MCP của claude.ai (ghi nguồn + ngày, ⛔ đoán). Một mã chạy cả stdio (Claude Code, `.mcp.json` dự án) lẫn HTTP từ xa (connector claude.ai); hợp đồng tầng giữ 11 kept (+ hợp đồng mới nếu cần) |
| AC-2 · công cụ CHỈ ĐỌC | `liet_ke_bang` · `mo_ta_bang` · `truy_van_doc(sql, gioi_han)` (một câu SELECT/WITH…SELECT, giao dịch READ ONLY bằng vai `fls_doc`, `statement_timeout`, trần dòng; chặn DML/DDL/`COPY`/nhiều câu/`SET`/hàm tác dụng phụ ở CẢ ứng dụng LẪN vai PG) · `goi_tuyen` (dùng lại tuyến ĐỌC của `fls/api`, ⛔ viết lại logic) · cổng HD2/báo cáo nếu có tuyến. `Email Address` vẫn ⛔ trong kho (đo lại) |
| AC-3 · xác thực | endpoint công khai ⇒ ⛔ authless; chỉ tài khoản Google trong danh sách cho phép (mặc định chỉ chủ — đọc từ bí mật/biến, ⛔ ghim email trong repo); token sai `aud`/hết hạn/người ngoài ⇒ 401/403; theo cơ chế OAuth connector claude.ai hỗ trợ; IAP ⛔ đứng trước MCP (claude.ai ⛔ qua IAP) — ghi rõ thiết kế |
| AC-4 · hạ tầng cho CHỦ | `tools/staging/10_mcp.sh --project fp-a-project [--kiem]`: Cloud Run `fls-staging-mcp` · SA riêng `fls-staging-mcp` CHỈ `secretAccessor` trên bí mật `fls_doc` + `cloudsql.client` CÓ ĐIỀU KIỆN chỉ instance `fls-staging` · binding mức dự án khác `--condition=None` · ⛔ đụng tài nguyên ngoài tên FLS · in URL + bước thêm connector · BÁO CÁO `mong` ĐỎ hai chiều |
| AC-5 · nhật ký + giới hạn | Cloud Logging: ai · công cụ · băm SQL · số dòng · thời gian (⛔ nội dung) · trần tốc độ/người |
| AC-6 · bài | client MCP thật gọi từng công cụ vào máy chủ cục bộ + kho TEST đã nạp; đột biến SQL ghi (INSERT · UPDATE · DELETE · DROP · `COPY` · hai câu · CTE chứa DML · `set_config` · `pg_sleep`) ⇒ 100 % chặn ở cả hai lớp; xác thực sai ⇒ từ chối; gcloud GIẢ (chính sách CÓ điều kiện) cho 10; mỗi bài canh chứng minh ĐỎ |
| AC-7 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit; ⛔ cổng 5433) · `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` 0 · `requirements.txt` đủ |

## Câu cho chủ (Dev ghi ở BG)
- **C1** danh sách email được kết nối (mặc định chỉ chủ).
- **C2** xác nhận: dữ liệu thật đọc qua MCP vào ngữ cảnh hội thoại Claude của tài khoản đó.

## Luật
⛔ GCP thật · ⛔ khoá/mật khẩu/email thật vào repo · ⛔ `docker compose down` · ⛔ sửa `tests/nghiem_thu/` · sổ phát hiện 10 cột · Đ1–Đ5.
