# KQ-275 — R1 kiểm `WO-273` · `BG-274` · ISP Step 40 · F7 *(SCR-F08 ký bản Daily Report 3)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN** *(sổ `04_Test/review/SO_PHAT_HIEN_ISP-3.1_F7.md` v0.1)*. Đo trên `isp/F7` @ `0202147`, cụm `5444`, Chromium + máy chủ thử + kho TEST.

| Trọng tâm | Kết quả |
|---|---|
| AC-1 F7-F1 | Kịch bản độc lập đọc lại từ `GET …/snapshot/{ky}`: cả 2/2 `da_ky`, checksum khác, bản 1 giữ nguyên 7/7 trường, bản 2 người ký = thẻ |
| AC-2 | Bài tác giả xanh; đột biến *rỗng không tên* đỏ; đột biến *không khoá nút* đỏ |
| AC-3 | Huỷ nút/`Esc`/nền ⇒ **0** POST; `Enter`×3 ⇒ **1** POST |
| AC-5 | thân `{}`; đột biến *gửi actor* đỏ 4 bài |
| `C13-R1-04` | chữ 409 *bản báo cáo* ở F7 (đột biến bỏ ⇒ đỏ); F5 giữ câu *"đã được ký rồi"* — `test_isp_f08_ky_pg` + `test_goi_cua_phu_het_ma_loi` xanh *(29 bài cụm F7/F5/thuyết minh)* |
| Phím/thuyết minh | `Enter` lúc hộp vừa mở ⛔ ký; tiêu điểm về nút (đột biến bỏ trả ⇒ đỏ); `kiem_thuyet_minh` 35/35 |
| Bài F4 | đếm `button.nut-ky` không yếu đi với đường cũ (`M10` đỏ) — `F7-R1-03` |
| Đột biến | **11/11** cắn |
| Ảnh *(1100×900, scale 1, ⛔ commit)* | Trước: bảng tỷ giá + thẻ F7 dưới đáy (cần cuộn — `F7-R1-01`). Sau: 2 hàng `đã ký`, người ký bản 1 cũ / bản 2 từ thẻ, `Ký bản` mờ + *"Phiên bản 2 (mới nhất) đã ký"* |

## Cổng
- `--duong-nen --cong 5444` *(một lần, một mình, 596 s + 199 s)*: **ĐẠT** — toàn bộ tập đỏ+XFAIL **28 = 28** *(thêm 0 · bớt 0; `a41490d` đã sửa bài thuyết minh)*, chạy **4285** ≥ 4285; `tests/web` **3 = 3**, chạy **688** ≥ 688; skipped 0.
- `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT *(417 tệp · 2806 bảng)* · `soi_bang_tuyen` khớp 48 tuyến.
