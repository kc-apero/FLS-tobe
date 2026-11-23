# WO-338 — Voi fleet eval: dựng BỂ GIỮ RIÊNG (~60 ca) cho A2.04 ghép theo nội dung — đáp án = ITL Ledge Final AS-IS

| | |
|---|---|
| **Trạng thái** | `MO` — viết 23/11 ~05:05 UTC; giao NGAY 23/11 ~05:25 (lời chủ) |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/HELD` (nền = ngọn `isp/AG` — tăng tốc ③) |
| **Dải phiếu** | `BG-339` · `KQ-340` (R1) · `KQ-341` (R2 cuối). Số trống kế tiếp sau dải: **342** |

## Vì sao — quyết chủ 23/11 (BG-330, theo khuyến nghị)
- **C5 = 1:** một WO làn DATA dựng ~60 ca theo thẻ `docs/ITL/05_FleetEval/eval-cards/a3-1-ref.md` (D · E · F · L3 + ca chuyển), đọc live qua SA chỉ-đọc, nội dung ⛔ vào repo (`FLS_HELDOUT_NOI_DUNG` ngoài repo) — repo chỉ ĐẾM.
- **C4 = bật nội dung ĐÃ CHE, SAU KHI ĐO trên bể giữ riêng** ⇒ bể này là điều kiện để bật; trước đó mặc định TẮT.
- C1 = A (Opus 5.5 làm, G0 bóng) · C2 = A4 mã thuần tới G1 · C3 = ngưỡng đề xuất, A2.04 siết (G1 chỉ khi 2 vòng liên tiếp 0 ca phải-để-người bị nối).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | công cụ dựng bể: đọc ITL Ledge Final + nguồn giao dịch (SA chỉ-đọc), chọn ~60 ca theo phân tầng thẻ `a3-1-ref` (khai `mong` số ca từng tầng, Đ4), ghi bể ra thư mục NGOÀI repo (`FLS_HELDOUT_NOI_DUNG`, chmod 600); repo chỉ giữ tệp ĐẾM (số ca/tầng + vân tay) | pytest (nguồn GIẢ) + chạy thật chỉ-đọc |
| AC-2 | bể **độc lập** với bể dựng 12 ca của WO-329 (0 ca trùng — vân tay) và với dữ liệu prompt/ví dụ của agent (0 trùng) | pytest |
| AC-3 | `tools/fleet_eval_voi.py --be-giu-rieng` chạy ở chế độ PHÁT LẠI/GIẢ trên bể (⛔ gọi API thật) ⇒ báo cáo vòng: recall · nối sai · ca phải-để-người bị nối, nội dung TẮT vs BẬT-đã-che; chỉ số, ⛔ nội dung | BG |
| AC-4 | riêng tư: bộ che NFR-I13 trên bể thật — đếm 0 tên người/số TK/email/Số chứng từ lọt sau che (bài trên mẫu thật, ⛔ in mẫu); `quet_pii_repo` 0; ⛔ commit bể | pytest |
| AC-5 | `--duong-nen` ĐẠT; nâng sàn + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ gọi API mô hình thật · ⛔ bật agent · ⛔ ghi kho THẬT · ⛔ commit nội dung giao dịch thật. Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét sheet của chủ). Bản thô `/tmp` chmod 600, xoá sau.

## Bổ sung 23/11 ~05:25 — lời chủ: *"Làm cả 2, test trên dữ liệu cũ và dữ liệu thật hiện tại."*
- Giao NGAY (⛔ chờ R1 AG `KQ-331`) — chủ chỉ định; nền vẫn là ngọn `isp/AG`.
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-6 · dữ liệu CŨ | bể A: ca lấy từ **kỳ đã chốt** (đáp án = ITL Ledge Final đã chốt) — chạy chuỗi 4 agent ở chế độ phát lại + fleet eval ⇒ report một trang trên bể A: mẫu số · khớp · lệch (agent ↔ máy) + recall/nối sai (A2.04) | pytest + BG |
| AC-7 · dữ liệu THẬT hiện tại | bể B: ca từ **dữ liệu live hiện tại** (đọc SA chỉ-đọc ngay hôm chạy) — kỳ đã chốt ⇒ đáp án Final; kỳ đang mở ⇒ đáp án CHƯA chốt, nhãn `chua_chot` riêng, ⛔ tính vào recall chính. Report một trang hiện **hai cột bể A ↔ bể B**; số kỳ đã chốt ở bể B phải = bể A (lệch ⇒ ĐỎ có tên — nguồn đã sửa sau chốt) | chạy thật chỉ-đọc + BG |
- Cả hai bể: ⛔ gọi API mô hình thật (agent ở chế độ phát lại/GIẢ — ghi rõ report đo ĐƯỜNG ỐNG + cổng, ⛔ chất lượng mô hình); nội dung ngoài repo; repo chỉ đếm.
