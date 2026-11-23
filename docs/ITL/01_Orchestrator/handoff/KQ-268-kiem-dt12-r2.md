# KQ-268 — R2 CUỐI kiểm `DT12` · ISP Step 38 *(ảnh Manual input `ITL Ledge`, kỳ ≠ 2026-03)* · vòng sửa sau `KQ-267`

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN** *(⇒ backlog)*. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT12.md` v0.2 *(`DT12-R1-01` **Đóng**; THÊM `DT12-R2-01` · `-02`)*. Đo trên `isp/DT12` @ `53e2571`, cây gộp thử `thu/DT12` *(nhánh làm việc @ `96d6ebf` + gộp `--no-ff`, **0 xung đột**)*, cụm `5445`. Vai KIỂM: ⛔ sửa mã; cây gộp thử ⛔ commit.

## Soát
| # | Việc | Mẫu số | Kết |
|---|---|---|---|
| 1 | `-01` đóng: hình = ảnh 2026-03, đo ĐỘC LẬP *(mã riêng, `_nap` + `_chuan`)* | **25** ảnh · 12.049 dòng | **25/25** đúng: khoá cấp trên *(tập + thứ tự)* · `ky` = tên tệp · `dong_du_lieu_bat_dau` = 10 · `so_dong` = số dòng · khoá dòng · `dong_sheet` int · 0 ô dict/bool · `_chuan(hd_manual)` ⛔ chuỗi dict. Gồm ≥ 3 ảnh dev **chưa** thử *(2025-01 · 2025-09 · 2026-06 · 2026-08 …)*; ảnh 2026-03 **0** byte đổi *(`test_AC3_anh_2026_03_dung_tung_byte` xanh)* |
| 2 | Khứ hồi *(từ `7504ec2` — ảnh `{"chu"}` cũ)* | **361.470** ô *(12.049 × 30)* | `_chuan` trước = sau, lệch **0**; `dong_sheet` khớp 12.049/12.049; **74.419** ô `svc_*` chữ-số → số *(khớp dev)* |
| 2b | **Kiểu ô `svc_*` so ảnh 2026-03** | 2026-03: **4.672** ô *(584 × 8)* · ảnh mới: **96.392** | **LỆCH KIỂU** → `DT12-R2-02` *(GHI NHẬN)*. 2026-03: **2.512 chữ-số-CHUỖI** · 1.186 số · 8 rỗng *(cả 8 cột có đủ hai kiểu)*; ảnh mới: **0 chuỗi** · 74.417 int + 2 float · 18.200 chữ khác. Tác động qua `_chuan` = **0**; chỉ cắn nếu H15 so theo KIỂU |
| 3 | Bài AC-5 mới đo GIÁ TRỊ thật | đột biến **7/7 dev** tái lập *(4 trong bộ nhớ + 3 trên ảnh thật, bản sao)* + **9** mới | 7/7 ĐỎ · mới **8/9 bắt**, **1 sống**: đổi 1 ô *(checksum)* · đổi thứ tự cột *(AC-3)* · xoá `dong_du_lieu_bat_dau` *(AC-5 hình)* · số→chuỗi svc *(chỉ nhờ `tong_bytes`)* · `dong_sheet`+1 *(AC-1)* · đổi thứ tự hàng *(checksum khứ hồi)* · `so_dong`+1 · ô svc thập phân — bắt; **đổi `ky` ảnh 2025-12 → `2000-01` ⇒ 18/18 XANH** ⇒ `DT12-R2-01` *(`ky` chỉ đo giá trị ở 4/25 ảnh; dữ liệu hiện đúng 25/25)*. Bản sao trả nguyên: `diff` = 0 |
| 4 | `--chuan-hoa-anh-cu` chạy lại | 25 ảnh + manifest từ `7504ec2` | `[khứ hồi] 25 kỳ · 361470 = 361470 ô`, exit 0; **26 tệp `diff -rq` = 0 byte**; chạy lần 2 ⇒ "đã đúng hình — bỏ qua", 0 byte đổi *(idempotent; in `0 = 0 ô` là no-op, đúng thiết kế)* |
| 5 | Cổng trên cây gộp thử | — | xem dưới |

## Cổng *(cây gộp thử, `--duong-nen --cong 5445` MỘT lần, một mình)*
Toàn bộ: `12 failed · 4269 passed · 2 xfailed · 14 errors`; tập đỏ **28 = 28** *(thêm 0 · bớt 0 · XFAIL 2 = 2)*; chạy **4297 ≥ 4297** *(sàn Q8 = chạy thật)*. `tests/web`: **3 = 3**, chạy **681 ≥ 681**. `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu` ĐẠT *(418 tệp)* · `quet_pii_repo` **0 chỗ · 0 tệp** · 18/18 bài DT12 xanh. *(Lượt đầu bị dừng ở giới hạn thời gian nền, chạy lại từ đầu — số trên là lượt hoàn chỉnh.)*

## Gửi orchestrator
`DT12-R1-01` ĐÓNG. **Gộp bước được** *(0 CHẶN · 0 NÊN SỬA)*. Ghi vào WO H15 *(Step 43)*: so ô **qua `_chuan`**, ⛔ so kiểu *(`-R2-02`)*; thêm assert `d["ky"] == kỳ` cho 25 ảnh *(`-R2-01`)*. `-R1-02…06` vẫn ở backlog; **`-R1-05`** *(đóng băng lại 2026-03 — ảnh lệch sổ nay)* là quyết của chủ, nên **trước H15**.
