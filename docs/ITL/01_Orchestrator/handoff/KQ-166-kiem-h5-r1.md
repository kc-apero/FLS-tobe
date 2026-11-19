# KQ-166 — R1 kiểm `H5` *(ISP 3.1.2 · Step 16 · WO-164 · BG-165)*

| | |
|---|---|
| **Phát bởi** | `fls-test` R1 · 2026-11-18 · `isp/H5` @ `884953e` · cụm 5435 |
| **Kết luận** | **ĐẠT có điều kiện** — 0 CHẶN · 1 NÊN SỬA · 5 GHI NHẬN *(sổ `SO_PHAT_HIEN_ISP-3.1_H5.md`)* |

## Số đo *(mỗi số một vật)*
- WP-C3a: **205.175/205.175** ô so khớp *(trong đó 10.540 ô đáp án ≠ 0)* · lệch ngoài tên 0 · KPI loại 76.000 *(engine khớp 53.189 — nền cho bước sau)*.
- Đường nền `--duong-nen` *(một lần)*: tập đỏ **28 = 28** · 3.423 bài · web 3 = 3. `lint-imports` 11 kept · `kiem_tai_lieu` DAT.
- Đột biến: **17** trên bản sao `git archive` — 15 ĐỎ ở cổng/bài đúng chỗ; **3** chỉ bài ĐỎ, cổng DAT *(M2 nhãn cha — dữ liệu không có; M5 atol rộng; M17 KPI co mẫu số)*; **2 lọt hết** *(M12/M16: cột C/G thêm vào dòng ảnh, checksum tái tính ⇒ `H5-R1-01`)*.

## Phát hiện cần sửa
- `H5-R1-01` **NÊN SỬA** — bài PII quét khoá dòng ảnh.
- Backlog: `-02` khoá số ô ≠ 0 · `-03` mong literal · `-04` ô KPI cần WP riêng · `-05` 153 dòng ITE ≈ 0,012 mUSD *(BA)* · `-06` cột `itl_id` thừa.

## Câu hỏi
BA: 153 dòng `ITE | ITE Interest` — sửa nguồn hay alias? *Khuyến nghị:* sửa nhãn nguồn, giữ parity AS-IS tới lúc đó.
