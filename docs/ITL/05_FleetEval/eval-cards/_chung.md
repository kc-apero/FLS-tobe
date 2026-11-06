# Phần chung của bốn thẻ eval — FLS phase 1 · vùng NẠP

Áp cho `a3-1-ref` · `a3-2-luong` · `a3-3-nen-tang` · `a4-soat`. Mỗi thẻ chỉ ghi phần riêng.
Trạng thái: **đã chốt ở Gate 3 (KhanhCQ 06/11)** — bar, cỡ mẫu, ngưỡng theo đề xuất. Bản ký: `../AP_FLS_FleetEval_v1.0.0_2026-11-06.html` (chờ ThuongCT đặt *agreed*).

| Mục | Nội dung |
|---|---|
| Mô hình agent | Agent **làm** (A1 · A2 · A3.1–A3.3): `Qwen 3.8-27B`. Agent **kiểm** trong luồng (A4 SOÁT): **`gpt-oss-20b`** — khác họ với thứ nó kiểm (KhanhCQ 06/11: "dùng 1 model khác để kiểm"). Cả hai chạy local. Phiên bản LLM đầu tiên = `v1`. **Phiên bản gốc `v0` = mã tất định hôm nay** (`fls/` @ commit đóng băng) — cột "không tệ hơn bản trước" của vòng đầu so với `v0`. |
| Mô hình chấm | Khác mô hình của **chính** agent bị đo: A3.1 · A3.2 · A3.3 chấm bằng `gpt-oss-20b`; **A4 chấm bằng `Qwen 3.8-27B`** (A4 đã là gpt-oss). ⛔ agent nào được chấm bằng mô hình của chính nó. |
| Mô hình persona | Cùng mô hình với bộ chấm của agent ấy (A3.x: `gpt-oss-20b` · A4: `Qwen 3.8-27B`), prompt riêng (⛔ chung prompt với bộ chấm, ⛔ trùng mô hình agent bị đo). |
| Chấm mù | Bộ chấm chỉ thấy mã ngẫu nhiên, ⛔ tên agent, ⛔ phiên bản. Đáp án chỉ bộ chấm đọc; mọi lượt đọc được ghi log. |
| Chấm lại bằng người | Lanptn chấm lại **10%** số mục mỗi vòng *(đề xuất)*; đồng thuận < **0,8** ⇒ vòng **vô hiệu** *(đề xuất)*. |
| Nguồn đáp án | **ITL Ledge Final của AS-IS** (sổ kế toán đã chỉnh) + kết quả so khớp oracle (`fls/oracle`). Chỗ AS-IS biết là sai (lỗi đã ghi) ⇒ đáp án do người xác nhận lại, `label_source = human-verified`. |
| Ca cài sẵn | Lấy từ **lỗi thật đã ghi** (mỗi thẻ liệt kê) + ca dựng có đáp án biết trước. Mỗi vòng có ≥ 1 **ca chuyển** (tháng / nguồn chưa dùng khi tinh chỉnh). |
| Giữ riêng | Ca + đáp án để ngoài repo (giống `sao_luu/`, `hien_vat/` — có tên người, tiền thật); chỉ bộ chấm và operator đọc. Ca đã dùng để sửa agent ⇒ chuyển sang bộ hồi quy, rút ca mới. |
| Persona | Chung cho ba agent mapping (thẻ A4 dùng lại P1–P3): **P1 kế toán mới** (nghiệp vụ 1/5, phần mềm 2/5; biết "sao kê", "PM"; ⛔ biết "Reference No", "L1/L2/L3", "CDT1"; đọc hết, tin câu chắc chắn) · **P2 kế toán ngân hàng lâu năm** (nghiệp vụ 4/5; biết mọi thuật ngữ; đọc lướt, chỉ soát tiền và mã) · **P3 người duyệt cuối kỳ** (vai owner: nghiệp vụ 4/5; ít thời gian, duyệt mọi dòng "đã khớp"). A3.2 thêm **P4 C&B HR**. |
| Hiệu chuẩn persona | Think-aloud với **ThuongCT · AnhMC · NgaNLT** trên một mục, người quan sát ghi chỗ vướng. Bar ghi **trước khi xem**: recall ≥ **0,6**, precision ≥ **0,5** *(đề xuất, theo khoảng khởi điểm của how-to)*, phải giữ trên **mục thứ hai**. Tới khi đạt: mọi phát hiện của persona là **gợi ý**, ⛔ phát hiện. Hôm nay **cả 4 persona = gợi ý**. |
| Chi phí | **Không đặt trần** (owner 06/11). Mỗi vòng vẫn **ghi giờ GPU thực tiêu** của agent, persona, bộ chấm vào báo cáo vòng. |
| Lưu | Một bản ghi mỗi mục, cùng khuôn với tín hiệu người kiểm thật (`fls_pm_link` · `fls_adjustment` · `fls_journal` đã có actor); lớp lưu giữ: `tho` (ngắn) · `scrubbed` (suốt đời agent) · `heldout` (hạn chế). |
| Vai | Owner **ThuongCT** · Operator **KhanhCQ** · Duyệt độc lập **Lanptn**. ⚠ KhanhCQ dựng mọi agent và prompt (trái quy tắc how-to) — cách bù ở AP Q1 · A6. |
| Quy tắc dừng | **Ship:** đạt bar chính + không tệ hơn `v0` / bản trước + vòng không vô hiệu. **Chặn:** bất kỳ ca cài sẵn nào của bar chính trượt. **Chạy lại:** vòng vô hiệu, hoặc có ô heatmap "không có ca". |
