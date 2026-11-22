# KQ-305 — R1 kiểm `I1` · ISP Step 45 *(HD1 xuyên suốt)* · `WO-303` · `BG-304`

**Kết luận: CẦN VÒNG SỬA — 0 CHẶN · 3 NÊN SỬA · 4 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_I1.md` v0.1. Đo trên `isp/I1` @ `a4dff50`. Vai KIỂM: ⛔ sửa mã.

| # | Việc | Kết |
|---|---|---|
| 1 | Bài tích hợp | 11/11 xanh; **3 tầng thật** (công cụ sống → JSON → HTTP → vm + Chromium); đột biến **8/8 đỏ**; bật 1 kỳ ở công cụ ⇒ 3 tầng đổi |
| 2 | 5/23 đo lại | đạt 5 · đỏ 18 · Σ 122 = DT1a 122, khớp từng kỳ |
| 3 | `I1-P1` | **NÊN SỬA** `I1-R1-01`: cổng 23 kỳ; `fls/` đọc `tu_sinh` 0 chỗ; `tu_sinh` ⛔ có vế dòng 1-1 ⇒ 3 kỳ mới phải `null` |
| 4 | `I1-P2` | **NÊN SỬA** `I1-R1-02`: có nhãn (tệp tmp) mà `ly_do` vẫn ⛔ mang tên nhãn |
| 5 | B2 / F2 | tệp vắng ⇒ `dat=null` + thẻ KHÔNG ĐO ĐƯỢC: ĐẠT |
| 6 | Chữ ký giả | chỉ tệp tạm; `so_ly_do_hd1.json` `chu_ky == []` |
| 7 | Bảng AC10/AC11 | **NÊN SỬA** `I1-R1-03`: gán cột đảo so AP §5.3.2 |
| 8 | `I1-P3` | GHI NHẬN môi trường (có sẵn ở nền) |
| 9 | Sàn / cổng | 4.561 = collect thật · `--duong-nen` ĐẠT 28 = 28 · `lint-imports` 11 kept · `kiem_tai_lieu` · `kiem_thuyet_minh` ĐẠT |

**Gửi orchestrator:** mở vòng sửa cho `I1-R1-01…03` *(01·02 ở lane CG1/H2, 03 ở BG)*.
