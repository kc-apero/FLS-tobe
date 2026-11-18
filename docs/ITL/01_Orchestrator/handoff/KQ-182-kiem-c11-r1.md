# KQ-182 — Kiểm R1 · ISP Step 25 · C11 IX.ALR

| | |
|---|---|
| Phát bởi | fls-test (R1) · 2026-11-18 · `isp/C11` @ `c76293a` |
| Gửi | orchestrator (⇒ R2 `KQ-183`) |
| Kết | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **1 NÊN SỬA** · 2 GHI NHẬN |

- C11-B1/B2/B3 xanh; **72** bài liên quan xanh (cụm 5444). `--duong-nen` MỘT lần: ĐẠT, tập đỏ + XFAIL = **28** (thêm 0 · bớt 0), chạy **3520**.
- **17 = 4 H1000 + 8 By GI + 5 By NOEM: ĐÚNG** — đếm độc lập trên ảnh DT3: 21 mã có method − 4 sổ nền tảng = 17 mã khác nhau; 2 mã `need` rỗng method ⇒ ⛔ luật.
- Đột biến **17/17** bị cắn (gồm biên kỳ `<=`, `bat`, `?run_id=`, nạp kiểm trước ghi, `khong_doi` bản ĐẦU của `test_C5R1_05` đổi sang `IX.TMP` ⇒ **vẫn cắn đủ**). Cờ TẮT 100 %; bẫy VLOOKUP `0` ghim; chỉ-thêm chặn UPDATE/DELETE.
- `lint-imports` 11/0 · `soi_bang_tuyen` 45 KHỚP · `kiem_tai_lieu` ĐẠT.
- **NÊN SỬA `C11-R1-01`**: nạp lần hai với `tu_ky` khác thay cả bản ⇒ `luat_cua(LC, 202503)` = None sau nạp 202507; hiệu lực theo kỳ ⛔ tích luỹ qua `nap`. Orchestrator quyết: gộp bản trước, hoặc chốt "mỗi nạp là bản đầy đủ".
- GHI NHẬN: `C11-R1-02` (Scope "ghi chú ATL B2:C4" chưa làm, 0 hit) · `C11-R1-03` (`cdt1=""` không ra `CAN_CDT1`).
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C11.md` v0.1.
