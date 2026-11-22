# KQ-323 — R2b nhẹ `WO-311` / `BG-312` *(ISP 3.1.2 · Step 46 · H14 — WP-C5c · vòng sửa tích hợp sau R2 `KQ-314`)*

| | |
|---|---|
| **Kết quả** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA** · 2 GHI NHẬN |
| **Phát phiếu** | `fls-test` *(vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/H14` `4b49d00` + cây gộp thử `thu/H14` *(`origin/claude/bold-galileo-zukpaf` `31ae77a` + `isp/H14`, gộp **sạch**, 0 xung đột)* · cụm 5445 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H14.md` *(v0.3)* |

## Kết luận
Vòng sửa tích hợp **đúng**. Phần ĐẠT ở R1/R2 ⛔ soát lại.

1. **`R2-01`** — cây gộp: 5 bài C5c **xanh**; tập bài C5c + `so_du_le` + `gates_hd2` + rào DT13 + `dau_vao_dt13` = **185/185**. `do_hd2.py --goi WP-C5c` rồi `--ghi` *(kho test đã nạp nền IX.PER · IX.ALR · IX.PL)* ⇒ **0 byte đổi** *(`git status` sạch)*; `NB = 0` 607 `dat_co_so` 147/116 · 609 151/116 · 610 26·56·8·60 / 35·24·131 khớp BG-312. Đường nền: `12 failed · 4815 passed · 2 xfailed · 14 errors` — tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4.843** *(mong ≥ 4.843)*; sàn = thu thập thật.
2. **615 `Cash Balance` 12.380 → 13.760 *(+1.380)*** — ô so 13.760 · có số 3.581 · khớp **13.054** *(thật 2.875)* ✓. **Tính ĐỘC LẬP** *(⛔ dùng bảng khuôn; tìm tập hàng `2. CCR`/`2. CCR Cash` ≤ 3 hạng tử, ÷10⁶ hoặc ÷10⁹, khớp ô đáp án ≤ 1e-7 trên 30 ngày 01–30/11)*: **30/30** hàng 615 CÓ SỐ khớp = **900 ô số** ≫ 30 ô; khớp thật, ⛔ chép *(đầu vào là `2. CCR`, không phải ảnh 615; `khop_chep` = 0 vì engine 615 ⛔ đọc DR2)*. 46 hàng = 30 có số + 16 toàn 0; ô `0=0` 528 = 480 *(16 × 30)* + 48 *(`LE15 mUSD` 20 · `LE27 mUSD` 28)* ⇒ 852 + 528 = 1.380 ✓ *(Đ3: mẫu số khai)*. Tập hàng độc lập ≠ khuôn ở 6 hàng nhưng **cùng số** ⇒ `R2b-02`.
3. **Rào DT13** *(605 · 610)* không bị vượt: 16 bài `test_rao_dau_vao_dt13_r1` xanh; `so_sanh_c5c` tự kiểm rào; `ccr_daily_report_2` 0 tệp mã đọc cho 610.
4. **Rổ 115 ô** *(1.495 − 1.380)* có tên: `ngoai_khuon:cb_cong_thuc_doi_theo_cot` **32** *(hàng 71)* + `ngoai_truc` `cb:f` **37** + `cb:ak` **46** = **115** ✓ *(đo từ `hd2_cong.json`/báo cáo)*.
5. **Cổng `None`**: `HD2_WP_C5C` vẫn `null` có tên — *"605: ô so 0/13706 ô số — DỪNG `chua_co_dau_vao` CHƯA có chữ ký chủ"*; `DUNG_KY = {}`; chuỗi `/gates`: *"độ phủ 615: ô so 13760/48021 ô số · 34261 ô số chưa so"*, `da_do` 77.672/86.150 ✓.
6. **Đột biến 4/4 cắn** *(baseline 185 xanh; mỗi lần `git checkout` trả nguyên)*: ① đổi 1 ô `ccr_so_du_ccr` hàng 10 ngày 10/11 (+10⁶) ⇒ 16 bài đỏ gồm `test_R2i_PHA_doi_mot_o_so_du…` + checksum + `AC3_PHA` · ② bỏ hàng 105 khỏi `LE05 mUSD` ⇒ 13 đỏ gồm `test_khuon_engine_khop_ban_do_…_hai_nguon` · ③ `CAM_CHO` rỗng ⇒ 1 đỏ *(`R2b-01`)* · ④ `chep=True` cho phần `cb` ⇒ 6 đỏ gồm `test_R2i_khop_tach_TINH_va_CHEP`. *(Lần đầu chạy lẫn ô nhiễm kho test do tôi nạp nền trước — làm lại sạch.)*
7. **Cổng**: `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT *(484 file · 2.957 bảng)* · `soi_bang_tuyen` KHỚP 49 tuyến. ⛔ `tests/web` · `kiem_thuyet_minh` không đo ở vòng này.

## GHI NHẬN ⇒ backlog
`H14-R2b-01` *(`CAM_CHO` dư vì whitelist `DAU_VAO_CHO` — đột biến chỉ cắn bài khai)* · `H14-R2b-02` *(phép so ⛔ phân biệt tập hàng cùng số: 4 hàng dư toàn 0, 2 hàng tổng trùng giá trị)*. Còn mở từ trước: `R2-02` · `R2-03` · `R2-04` · câu `LE17/LE19` chia 10⁹ chờ chủ/BA.

## Điều kiện gộp
H14 gộp được. Cổng C5 vẫn **không** xanh *(`HD2_WP_C5C = None` — 605 chờ chủ ký)*.
