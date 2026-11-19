# KQ-194 — Kiểm R1 · ISP Step 23 · DT6 (ảnh đáp án GL HR 407·408·413 + CFA3)

| | |
|---|---|
| Phát bởi | fls-test (R1) · 2026-11-18 · `isp/DT6` @ `f2a959f` |
| Gửi | orchestrator (⇒ R2 `KQ-195`) |
| Kết | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **1 NÊN SỬA** · 5 GHI NHẬN |

- **PII — sạch, không đảo được.** Quét 4 ảnh + bảng phụ: 0 `@`, 0 tên, 0 chuỗi ≥ 6 chữ số ở MỌI cột chữ *(không chỉ `H`·`Z`)*, mọi cột chữ ⊂ tập đóng. "Che" = thay bằng `R` *(không băm ⇒ không đảo được)*; `AP` bỏ. Lời lỗi ⛔ in giá trị *(đột biến cắn)*.
- **Tái đo độc lập (khoá SA, ⛔ đọc cột PII): 0 lệch trên 552.686 ô** — 407 150.736 · 408 150.560 · 413 172.560 · 412↔`gl_406` 78.830 *(7.883/7.883 hàng)* — và CFA3 650/650 ô ≠ 0 *(74 HD · 496 ngày · 5 `"-"`)*. Số dòng theo kỳ khớp cả 3 ảnh; 413 − 408 = **1.375** ✔. Y2024 = chỉ `#REF!`, 0 hàng giá trị ✔. Không đo lại được `H`·`Z` *(PII)*.
- **2.302 hàng thiếu ngày**: KHÔNG im — đếm + tên + cổng ghim + câu cho BA. Thiếu số TIỀN: ΣF = 6.763.528.503 *(≈ 7,45 % ΣF hàng có ngày)*, 0 ITL ID, 0 ô bVND ⇒ `DT6-R1-04` GHI NHẬN.
- **Kích thước**: 6,02 · 6,02 · 6,89 MB *(DT6 = 19,15 MB = 50,8 % thư mục `dap_an`)*. Nguyên nhân thật: thụt lề ≈ 31 % *(compact 4,13 · 4,13 · 4,73 MB)*, gzip ≈ 0,34–0,40 MB mỗi ảnh ⇒ `.git` phình ≈ 1,1 MB; cột trùng `Z=H` 97 % không bỏ được. Mức thấp ⇒ `DT6-R1-05` GHI NHẬN, không sửa ở DT6.
- **Đột biến 16, cắn 12, sống 4**: `M14` *(nới `ITL_ID_RE` ⇒ 27/27 xanh; cột `R` không bài ghim)* ⇒ **NÊN SỬA `DT6-R1-01`**; `M9`/`M10` nhánh ĐỎ không bài ⇒ `-02`; `M13` mã chết `\d{6,}` ⇒ `-03`. Thêm `-06`: docstring `_gl_hr.py:111` chép 3 chữ số đầu số TK thật.
- **Cổng**: khai `mong` + ĐỎ hai chiều; `kỳ ⊂ 2025: KHÔNG` IN rõ *(`M7`/`M8` cắn)*; Y2024 thiếu CÓ TÊN.
- `--duong-nen --cong 5436` MỘT lần: **KẾT ĐẠT**, tập đỏ + XFAIL 28 = 28 *(thêm 0 · bớt 0)*, chạy 3588; web 3 = 3, chạy 675. `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT.
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT6.md` v0.1.
