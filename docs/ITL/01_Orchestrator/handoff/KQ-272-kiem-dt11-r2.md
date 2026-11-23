# KQ-272 — R2 cuối `WO-269` / `BG-270` vòng sửa `KQ-271` *(ISP 3.1.2 · Step 41 · DT11: ảnh đáp án Daily Report 2 · 3 + 4 ảnh H14 PD 607·608·609·615)*

| | |
|---|---|
| **Kết quả** | **TRƯỢT** — **0 CHẶN · 2 NÊN SỬA · 1 GHI NHẬN** |
| **Phát bởi** | `fls-test` *(R2 cuối, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/DT11` `34a119c` + cây gộp thử `thu/DT11` *(nhánh làm việc + DT7 · DT12)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT11.md` *(v0.3)* |

## Đã đóng *(R1 → R2)*
- `-01` CHẶN **đóng**: checksum tính lại; 2 đột biến R1 **chết**; thêm 8 đột biến mới *(607 · 608 · 609 · 615, xoá ô, sửa tiêu đề, đổi/thay ô lỗi)* — **10/10 chết**, kiểm chứng "ghi lại không đổi" 0 đỏ.
- `-03` **đóng**: DR3 `có số 0 · 0=0 14` · DR2 `0 · 262`; nhãn in ra tách. `-04` **đóng**: `AK` = ngày thật **chỉ ở 609**; 607 · 608 · 615 `AK` rỗng ở hàng ngày (đo SA). `-02` **đóng** bằng 4 ảnh.
- **4 ảnh đọc lại SA** *(từng ô, mẫu số ≠ 0 khai trước)*: 27.605 · 18.199 · 35.860 · 48.759 ô số/lỗi `F…AL` ⇒ **lệch 0**; checksum tái đóng băng **= ghim** cả 4. 615: 127 ô lỗi ở bảng chính khớp từng cột; vùng dưới hàng 2502 = 0 giá trị; 2,14 MB đã khai.
- PII: `quet_pii_repo` **0** ở cây gộp thử và ở **9/9** commit dải `origin/…..isp/DT11`. Ảnh cũ nguyên byte.

## Phát hiện cần sửa
1. **`DT11-R2-01` NÊN SỬA** — bài `test_AC6_anh_cu_va_cong_cu_chung_dung_tung_byte` đòi tập ảnh `dap_an/` = 22 cũ + đúng 6 DT11 ⇒ **ĐỎ ở cây gộp** *(DT7 +6 · DT12 +25 ảnh)*. `--duong-nen`: 28 nền + **THÊM 1**. Sửa `==` → `⊇` rồi gộp.
2. **`DT11-R2-02` NÊN SỬA (B2 — chủ quyết)** — ảnh 615 còn **7** số dài ở nhãn với hậu tố **tên-viết-tắt người** *(⛔ `_CN`; máy quét 0 vì chỉ bắt `CN`)*; 3 trong 7 đã có ở `docs/ITL/02_BA/Artifacts/Ket-qua-Phan-loai-4-loai-o.md`. Nếu là TK cá nhân ⇒ mở rộng quét + che ảnh 615 + tài liệu. ⛔ in số.
- GHI NHẬN `-03`: phần gốc `BG-270` còn "đạt ②" trơn *(biên bản)*.

## Cổng
- **Xung đột gộp thử**: chỉ `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(sàn)* ⇒ gộp tay; sàn = thu thập thật **4448** *(= 4351 + 97 bài DT11; web 681)*; chú thích chuỗi gộp thêm đoạn DT11.
- `--duong-nen --cong 5446` *(một mình)*: **ĐỎ** — `13 failed · 4419 passed · 2 xfailed · 14 errors`, tập đỏ 29 = 28 + THÊM 1 *(`R2-01`)*, bớt 0, chạy 4448; web 3 = 3, 681. `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT.
- Bản thô SA ở thư mục tạm *(chmod 600)* **đã xoá**, ⛔ commit.

Việc kế: Dev sửa `R2-01` *(+ `R2-02` theo quyết định chủ)*, R2b nhẹ trên cây gộp, rồi mới `isp-gop-buoc`.
