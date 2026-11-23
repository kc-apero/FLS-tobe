# KQ-283 — R1 kiểm `WO-281` · `BG-282` · DT7b *(ảnh đầu vào PLA cho H8)*

**Kết luận: ĐẠT CÓ ĐIỀU KIỆN — 0 CHẶN · 2 NÊN SỬA · 2 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT7B.md` (v0.1). Đo trên cây gộp thử `thu/DT7B` *(`fd064b1` + `isp/DT7B` @ `915e0ae`, 0 xung đột)*, cụm `5447`.

| Việc | Kết |
|---|---|
| Công thức đọc lại SA | `DE10`, `BM10` + 23 ô khác: **khớp BG nguyên văn** *(gồm `AH5487`·`AH7098`)* |
| Ảnh ↔ thô, từng ô | GL **86.713/86.713** · HR **106.848/106.848**, lệch 0; hàng **7.883 / 13.356** đúng |
| Tái dựng `DE` · `BM` | `DE` 7.574 số + 309 `#NUM!` = **7.883**, lệch 0 *(7.574 gồm **8** `AH` bất thường, ⛔ 6 — `-01`)*; `BM` **13.356/13.356** |
| AC-4 tự tính | GL↔414 **371/371** *(chỉ khi khớp NHÃN `V`; theo mã ITE ⇒ 359/374)* · HR↔416 **119/119**; đo thêm 4 khối LE **243/243** *(`-03`)* |
| Đủ cho H8? | GL **đủ** *(`V·P·BR·BS·DE`, `R`)*. HR **thiếu khoá CDT**: 416 có **4.381** ô ≠ 0 ở 7 khối CDT, ảnh chỉ dựng được `GROUP` *(`-02`)* |
| PII | 0 `@` · 0 cột cấm; `quet_pii_repo` = 0 trên cây gộp + 2 commit |
| Đột biến | **10/10 ĐỎ** |
| Cổng | `--duong-nen`: tập đỏ **28 = 28**, chạy **4375** ≥ 4375; web **3 = 3**/681; lint 11/0; `kiem_tai_lieu` ĐẠT |

## NÊN SỬA
- `-01` `AH` bất thường là **8** hàng: thêm sheet **669** *(tháng 27)* + **6230** *(tháng 14)*, `BS` ≠ 0, `DE` 2027 ngoài lưới; cổng "lạ" dùng `202000<AH<203000` nên ⛔ bắt. Mong 8 + khai tên.
- `-02` Ảnh HR cần cột quyết khối CDT *(`BP`/`AA`/…)* — ánh xạ chưa xác định *(`BP` thử 312/4.381)*; hoặc BA chốt H8 chỉ cần `GROUP`.

⇒ H8 chạy được phần GL + HR `GROUP`; khối CDT của HR chờ `-02`. Sàn cây gộp = thu thập thật **4.375**.
