# KQ-294 — R2 cuối `WO-291` / `BG-292` *(ISP 3.1.2 · Step 42 · H12 — AL.KEY + WP-C5a, cờ 2025 BẬT)*

| | |
|---|---|
| **Kết quả** | **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(`H12-R1-01` đóng)* |
| **Phát bởi** | `fls-test` *(R2 cuối, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/H12` `abea054` + cây gộp thử *(⛔ commit)* · cụm 5447 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H12.md` *(v0.2 — mục "Đo R2 cuối" có đủ số)* |

## Kết luận từng trọng tâm
1. **Cờ bật qua kho có ký** — IX.ALR **v2** *(38 dòng)* mới, v1 *(17)* nguyên; `actor` `KhanhCQ` *(tên, ⛔ email, ⛔ hằng)*. SA `FORMULA` ATL: By GI **48/48 ô/tháng 2025** *(AS-IS bật từ 202501; FLS 202502 vì thiếu driver — đã khai, `R2-01`)* · By NOEM **29/30** · 2024/2026 **0**.
2. **Lớp bằng phép đo**: mẫu 10 ô/lớp **10/10** đúng lớp *(toàn lớp: `chua_co_dau_vao` 709/709 dò về MID3·FS1 DR3; D3 lá 348/348 `ATL/GROUP = GI_khối/GI_GROUP`)*. `mong` Đ5 hai chiều **16/16** ĐỎ. Lệch FLS **0**; 224+675+29+1.091+3.099 = 5.118 = tổng lệch.
3. **OFR/H11**: 72/72; `phan_bo_khoa` chỉ cổng C5a dùng ⇒ ⛔ chạm AL.PLT; 996 bài `bao_cao·oracle·cau_hinh` xanh; C3d/C4c số y nguyên.
4. **H12-B1** cờ tắt **50.616/50.616** *(≠0: 9.995)*; `-05` `-06` đúng.
5. **Cây gộp thử** `WP-C3d/C4c/C5a` ĐẠT, `--ghi` ⇒ 0 byte; `/gates` C5A + C5 xanh. Xung đột: CHỈ sàn script + bài ghim ⇒ sàn = thu thập thật **4.621**.
6. **Đột biến** mới **8/8** cắn. 7. `--duong-nen` ĐẠT *(28=28 · 4.621 · web 3=3)* · lint 11/0 · tài liệu ĐẠT · 48 tuyến KHỚP.

## GHI NHẬN ⇒ backlog
`R2-01` tên `lech_D3` gộp cả By GI T01/2025 · `R2-02` `chua_co_dau_vao`: 59/247 lá engine≠0 *(46 lớn hơn ATL)* ⇒ phải đo lại khi có ảnh MID3 · `R2-03` chia `1−Σ` ngoại lệ ⛔ canh mẫu số.

Việc kế: orchestrator gộp `isp/H12` *(`isp-gop-buoc`)*.
