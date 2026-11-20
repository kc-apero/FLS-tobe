---
name: isp-orchestrator
description: Vận hành vai orchestrator ISP 3.1.2 của FLS — giao phiên con cloud (dev · sửa · R1 · R2 cuối · bước dữ liệu), lượt kiểm định kỳ, quyết việc kế theo bảng, cấp số phiếu WO/BG/KQ, ghi TIEN_DO, hỏi chủ kèm khuyến nghị. Dùng khi chủ nói "lượt kiểm", "giao phiên", "mở bước", "chạy tiếp ISP", "việc kế", "orchestrator", "R1", "R2 cuối", "vòng sửa", "nhắn tiếp phiên", hoặc khi một lượt hẹn `send_later` của orchestrator đến.
---

# isp-orchestrator — vòng lượt ISP 3.1.2

Nguồn: `docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-19.md` §3 · §5 · §6 · "Trạng thái cuối". Nhật ký + quyết của chủ: `docs/ITL/01_Orchestrator/isp-3.1/TIEN_DO.md`. Spec: `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` (bảng phụ thuộc §2.3, làn §2.1).
Orchestrator ⛔ viết mã bước. Trả lời chủ bằng tiếng Việt; mọi câu hỏi kèm khuyến nghị.

## Luật của chủ — ⛔ hỏi lại
| Luật | Nội dung |
|---|---|
| **A** | dev / sửa / review = **Sonnet 5.5 medium**; bước engine khó (H5 · H6 · H7 · H9–H14) = **Opus 5.5 medium** |
| **B** | **2 vòng review**: R1 đầy đủ + R2 cuối trên **cây gộp thử** (chữ "R1·R2·R3" trong ISP §2.4 là bản cũ). GHI NHẬN ⇒ backlog sổ phát hiện. NÊN SỬA sau R2 ⇒ 1 vòng sửa + **R2b nhẹ** |
| **C** | `--duong-nen` MỘT lần cuối mỗi phiên con |
| **D** | ≤ **3** phiên con song song |
| **E** | tin nhắn cuối của phiên con ≤ **15 dòng** |
| Agent | chia theo **VAI** (chủ 19/11): orchestrator · `fls-dev` (làn CF/HC/FE/DATA đọc từ WO) · `fls-test` · `fls-ba` |
| Project | phiên con gắn tag `remote-agents-project:fp-a-project` (chủ 20/11) + `isp-3.1.2` + vai (`dev` · `sua` · `r1` · `r2` · `du-lieu`) |

## Nhịp một lượt
1. **Giao** ≤ 3 phiên: `create_session` — `source_url` repo · `source_revision` = nhánh làm việc · `model` theo luật A · `effort` medium · `tags` như trên · `prompt` từ mẫu (§Mẫu). Mỗi phiên song song **một cổng PG khác** (5434–5437, 5444–5447).
2. **Hẹn** lượt kiểm sau **40 phút** bằng `send_later` (nội dung = id phiên + việc lượt kế). ⛔ poll ngắn.
3. **Kiểm**: `list_sessions` (`children: true`) → phiên xong: `list_events` (`kinds ["result"]`, `limit 100`) đọc tin cuối → cần thì `git fetch origin refs/heads/<nhánh làm việc>-isp/<ID>` + `git show` phiếu `BG`/`KQ` → quyết theo bảng dưới.
4. **Ghi** một hàng `TIEN_DO.md` (`\|` trong ô) → `python docs/ITL/_tools/kiem_tai_lieu.py` → commit (trailer phiên) → push → hẹn lượt kế.
5. Phiên con **DỪNG vì thiếu đầu vào** ⇒ orchestrator đo nguồn bằng SA chỉ-đọc (skill `fls-moi-truong` §5), hỏi chủ khi là quyết nghiệp vụ, mở **bước dữ liệu nhỏ** (tiền lệ DT8b · DT9b · DT6b · DT6c — mẫu `du_lieu.md`), rồi `send_message` cho phiên tác giả (mẫu `nhan_tiep.md`).
6. Phiên đang chạy: ⛔ ngắt; chờ thêm 15–20 phút.

## Vòng đời một bước · bảng quyết
`WO-n` (orchestrator viết `docs/ITL/01_Orchestrator/handoff/WO-<n>-…md`, commit nhánh làm việc) → dev `BG-(n+1)` → R1 `KQ-(n+2)` → R2 cuối `KQ-(n+3)` → gộp (skill `isp-gop-buoc`). Dải 4 số mỗi bước; số trống kế tiếp ghi ở hàng `TIEN_DO` mới nhất.

| Kết quả về | Việc kế |
|---|---|
| dev xong, `--duong-nen` ĐẠT | R1 — phiên mới, mẫu `r1.md` |
| R1 ĐẠT 0 CHẶN · 0 NÊN SỬA | R2 cuối — mẫu `r2_cay_gop_thu.md` |
| R1 có CHẶN / NÊN SỬA | phiên sửa — mẫu `sua.md` (thêm mục "Vòng sửa sau R1" vào BG) → R2 cuối |
| R2 ĐẠT 0 · 0 | gộp — skill `isp-gop-buoc` |
| R2 có NÊN SỬA | 1 vòng sửa + R2b nhẹ (chỉ phần sửa + cây gộp thử) |
| GHI NHẬN | backlog sổ phát hiện, ⛔ chặn |
| gộp đỏ ở `--duong-nen` | ⛔ push; `git reset --hard origin/<nhánh>` (chỉ commit chưa push); phiên sửa tích hợp trên nhánh bước |
| phiên dừng vì thiếu dữ liệu | nhịp bước 5 |

## Chọn bước kế
Bước **sẵn sàng** = mọi phụ thuộc ở ISP §2.3 đã GỘP. Ưu tiên **đường găng** H7 → H8 → H12 → H13 → H14 → I2, rồi bước mở khoá nhiều bước khác. ⛔ hai bước cùng làn chạm cùng tệp chạy song song (ISP §2.1). Bước cần sheet ⇒ kiểm khoá SA trước.

## Mẫu prompt phiên con
`docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/mau_phien_cloud/`: `dev.md` · `dev_engine.md` · `du_lieu.md` · `r1.md` · `sua.md` · `r2_cay_gop_thu.md` · `nhan_tiep.md`. Đầu mỗi tệp ghi phần cần thay (mã bước · số phiếu · `## Step NN` · sha mong · cổng PG). Giữ nguyên các khối luật (⛔ `cd` · worktree `.claude/worktrees/isp-<id>` · push đúng `isp/<ID>:refs/heads/<nhánh làm việc>-isp/<ID>` · ⛔ force/PR · trailer của chính phiên).

## Chi phí
Đo bằng `get_session(<id>).external_metadata.usage.cost_usd`. Mốc: Sonnet review ≈ 0,5–1,7 · dev/sửa ≈ 0,5–3 · DATA ≈ 1,5–3 · Opus engine ≈ 2–8 USD. Theo dõi `rate_limit_info`.

## Bẫy (HANDOFF §6)
Hợp đồng khối HD2 (`tong_o`/`khop` = ô khớp THẬT, lệch có chủ đích ở `lech_co_chu_dich` + `mong_lech_co_chu_dich`, sinh bằng `do_hd2.py --ghi`) · engine thiếu ảnh đầu vào ⇒ DỪNG, ⛔ lấy đáp án làm đầu vào · tập toàn 0 là KẾT QUẢ (Đ3) · đếm "x/48" chỉ Step ISP · ⛔ in giá trị nhạy cảm khi dò sheet · AP/ISP sai dữ liệu ⇒ đo trước, gom errata v3.1.3 (HANDOFF §7).
