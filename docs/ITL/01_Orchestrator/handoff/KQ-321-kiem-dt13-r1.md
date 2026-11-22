# KQ-321 — R1 kiểm `DT13` · `WO-319` · `BG-320` *(đầu vào còn thiếu cho WP-C5a·b·c)*

**Kết luận: CÓ SỬA — 0 CHẶN · 2 NÊN SỬA · 5 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT13.md` v0.1. Đo trên `isp/DT13` @ `62787b8` + cây gộp thử `thu/DT13` *(⛔ commit; gộp sạch, 0 xung đột sàn)*. Vai KIỂM: ⛔ sửa mã.

| # | Việc | Kết |
|---|---|---|
| 1 | **Vòng tròn** `sign_off_dau_vao` | trùng đáp án 605 **14.036/14.036** ô *(13.541 ô số)*, cùng checksum; ô sổ thật sự đọc Sign off = **1.363** ô `[FS1]` *(608)*, 4 tab khác 0 ⇒ hợp lệ **chỉ cho 608**; dựng 605 = vòng tròn; **0 rào** *(bài `test_AC4_engine_khong_doc_dap_an` không tồn tại)* ⇒ `DT13-R1-01` NÊN SỬA |
| 2 | `ccr_daily_report_2` | ≠ đáp án 610 đổi tên: trùng **25.185/26.272 = 95,9 %** ⇒ ⛔ dùng cho 610; hợp lệ cho **615**, nhưng **23.746/48.021 (49,4 %)** ô 615 là chép nguyên ⇒ `DT13-R1-02` NÊN SỬA |
| 3 | FORMULA đọc lại | ≥ 2 ô mỗi nguồn *(8 dòng AC-1)* khớp BG; MID3 TOTAL 0 công thức; NOEM `F18:Q26` 0/108; 605 "0 ứng viên" đúng *(25 tab, 0 tab PLA5)* |
| 4 | Ảnh ↔ thô | mẫu 400/ảnh: **400/400** ×4 ảnh lớn · mid3 546/546 · noem 108/108; chiều ngược 0 thiếu |
| 5 | AC-3 độc lập | 615 CB **1.530/1.530** *(BG 1.380 — 54 hàng AS-IS, map 46)* · mUSD+GROUP **14.421/14.421** · CM 4 LE tham chiếu **6.178/6.178** · ATL MID3 **228/228** *(BG 231/234)* · PL5 **84/84** · 608 **1.363/1.363** — nhãn mẫu số lệch ⇒ `-03/-05/-06`; cột `g` 846 ô ngoài `mong` ⇒ `-04` |
| 6 | PII | 6 ảnh mới 0 nhãn ≥ 8 chữ số, 1 `TK_CA_NHAN`; `quet_pii_repo` 0 ở cây gộp + 2/2 commit; `DT11-R2-02` còn mở ở ảnh 615 cũ ⇒ `-07` |
| 7 | Ảnh cũ · sàn | 22 `dap_an` + 6 `dau_vao` + `dong_bang_sheet.py` đúng từng byte; sàn 4678 → 4724 |
| 8 | Đột biến | **10/10 cắn** *(nền 40 xanh; 6 ảnh · ảnh cũ +1 byte · ảnh lạ · `dong_bang_sheet.py` · sàn 4700 · `CB_MAP` mũ)* |
| 9 | Cổng | `--duong-nen --cong 5447` ĐẠT 28 = 28 · chạy **4.724** · web 3 = 3 · 690 · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT |

**Tập đỏ:** 28 = 28 *(0 thêm)*.
**Gửi orchestrator:** vòng sửa nhẹ cho `-01`, `-02` *(bài ghim "ảnh chỉ cho 608/615, cấm 605/610" + khai `DAU_VAO_CHO`)* trước khi H14 nạp ảnh; còn lại backlog. Chưa làm: HR DR2 · By NOEM · 605 tái lập.
