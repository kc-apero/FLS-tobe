# Mẫu `send_message` — nhắn tiếp phiên tác giả (rẻ hơn mở phiên mới, giữ ngữ cảnh)

> Dùng khi: phiên DỪNG vì thiếu đầu vào và bước dữ liệu đã xong · hạn mức đặt lại · trả lời câu hỏi phiên nêu. Nguyên văn đã gửi 19/11.

## A. Đầu vào đã có — làm tiếp (H7 ← DT6c)

````text
Orchestrator → H7 (WO-245): DT6c xong — nhánh `claude/bold-galileo-zukpaf-isp/DT6C` @ `2ee5ee5` (BG-250). Ảnh `tests/fixture/dau_vao/hr_ledger_2025.json` 10.105 hàng (NIS 7.585 + PIT 2.520), khuôn dùng chung hàm của `hr_ledger_2024`. Đối chiếu `gl_hr_408`: khớp số hàng + Σ PS Có 6/12 kỳ; 2025-10 nguồn hơn 1.227 (408 thiếu PIT kỳ 10: 1.223 hàng, ΣF 3,37 tỷ); 2025-12 408 hơn 269 (ΣF −413,5 tr); 02 +3 · 06/08/09 +1; **2026-01 (408 có 269 hàng) ⛔ có đầu vào ở nguồn**. 2.302 hàng `ky_suy`: nguồn ⛔ chứng thực kỳ "hàng trên" (1.201 trùng nội dung, chỉ 76 cùng kỳ; 1.125 nguồn ghi 2025-10; 1.101 ⛔ trùng). Công thức CFA3 `G13` = `SUMIFS(…!$BA, $A=ngày, $V=nhóm HD) − SUMIFS(…!$BB, …)` trên sheet `… Y2025`; `For PL Report`: `A10`·`E10`·`V10` là HẰNG, `BA10` = `AX10`/tỷ giá tháng ×10³ (BG-250 §3).

Orchestrator CHỐT: (a) các lệch kỳ trên ⇒ khai `mong` CÓ TÊN theo kỳ (lớp "đáp án ≠ nguồn"), ⛔ lấp; (b) 2026-01 ⇒ `chua_co_dau_vao` có tên (⛔ so); (c) 2.302 hàng `ky_suy`: giữ quyết chủ (kỳ hàng trên) cho đáp án, nhưng khai lớp lệch riêng `ky_suy` (đếm + Σ) — ⛔ tính là FLS sai; ghi câu hỏi cho chủ trong BG ("nguồn ghi 2025-10 cho 1.125 hàng — đổi quyết gán kỳ?").

Làm tiếp: `git fetch origin claude/bold-galileo-zukpaf-isp/DT6C` rồi gộp `FETCH_HEAD` vào `isp/H7` (merge; xung đột sàn ⇒ đặt = thu thập thật), gộp luôn ngọn `origin/claude/bold-galileo-zukpaf`, rồi hoàn tất WO-245 theo prompt đầu (TDD; dùng lại H4/H5/H6; CDT qua `cdt_cua`; WP-C3c khối `hd2_cong.json` hợp đồng CG2 `khop` = ô khớp thật + `lech_co_chu_dich` nếu dùng; `--duong-nen --cong 5435` MỘT lần; BG-246). Push `isp/H7`. Tin nhắn cuối ≤ 15 dòng: WP-C3c (GL HR · CFA3: ô so · ô ≠ 0 · lệch theo lớp) · /gates C3C · tập đỏ · sàn · sha.
````

## B. Hạn mức đặt lại

````text
Hạn mức đã đặt lại — tiếp tục đúng nhiệm vụ trong lời giao đầu (R2 DT5 · KQ-140, nhánh `isp/DT5` @ 5b8f7b5).
````
