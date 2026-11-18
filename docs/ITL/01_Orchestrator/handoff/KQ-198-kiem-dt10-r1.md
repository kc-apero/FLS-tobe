# KQ-198 — Kiểm R1 · ISP Step 27 · DT10 ảnh IX.DRV + đáp án ATL

| | |
|---|---|
| Phát bởi | fls-test (R1) · 2026-11-18 · `isp/DT10` @ `e3fe912` |
| Gửi | orchestrator (⇒ R2 `KQ-199`) |
| Kết | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · **5 GHI NHẬN** |

- **Tái đo độc lập** (khoá SA, script riêng, ⛔ khuôn): ATL **51.398/51.398** ô · driver **252/252** · NB **3.648/3.648** · công thức NOEM **96/96** · tử HR **84/84** — lệch 0. Tái chạy khuôn trên lần đọc của tôi ⇒ `dong`+`phu` **giống từng byte**.
- **146 ô thiếu: XÁC NHẬN thiếu ở nguồn** — 0 hàng nhãn CMN ở lưới; MID3 chỉ 11 dòng `TOTAL` (⛔ 202501); NB khoá From×To (16 From × 19 hàng; 49 To). Lưới "4×8" = **3 loại × 7 CDT1** có số (238/384) — nhãn Đ4 đúng; CMN→SHQ1 có bằng chứng `cdt_correct.json:59`.
- **Cổng Đ5**: khai `mong` + ĐỎ hai chiều. **20 đột biến, 20 cắn** (thêm năm 2026 ⇒ ĐỎ/TỪ CHỐI; bớt hàng; phá 1 ô; lấp ô thiếu; `Email Address`).
- PII: 0 cột cấm, 0 `@`; máy quét có ca phá (cắn).
- Công cụ chung: sha `ae917adbf80b1c14`, diff vs `fba4849` = 0. `KeyError` dòng 866 đo thật: exit 1 *sau* ghi ảnh, hướng an toàn (đỏ giả) ⇒ GHI NHẬN `-04`.
- `--duong-nen` MỘT lần: ĐẠT, tập đỏ + XFAIL = **28** (thêm 0 · bớt 0), chạy **3588**. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT.
- GHI NHẬN: `-01` nhãn "16 From × 19 To" (To khác nhau = 49) · `-02` CMN: GL→SHQ1 nhưng driver NOEM→phần dư SHQ2 (orchestrator chốt cho H12) · `-03` bài ghim lỗi không đếm lại từ hàng · `-04` KeyError · `-05` 829 = 824 có giá trị + 5 hàng chỉ gạch.
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT10.md` v0.1.
