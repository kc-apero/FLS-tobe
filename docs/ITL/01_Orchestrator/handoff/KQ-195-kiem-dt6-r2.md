# KQ-195 — Kiểm R2 CUỐI · ISP Step 23 · DT6 (ảnh đáp án GL HR 407·408·413 + CFA3)

| | |
|---|---|
| Phát bởi | fls-test (R2) · 2026-11-18 · `isp/DT6` @ `b9847c9` |
| Gửi | orchestrator (gộp thật) |
| Kết | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới |

- **Vòng sửa R1 đóng**: `DT6-R1-01` *(`ITL_ID_RE` `\d+`→`\d{1,6}` + 2 ca phá riêng, lỗi ⛔ in giá trị)* · `-02` *(2 bài cho nhánh `NGU_CANH@thiếu` · lưới không ngày)* · `-03` *(nhánh `\d{6,}` chết đã gỡ)* · `-06` *(docstring đổi `<số>_<NH>_<ĐƠN VỊ>`)*. `-04`/`-05` vẫn GHI NHẬN mở *(câu BA · định dạng ảnh)*.
- **Đột biến 4/4 cắn** trên mã sửa: regex về `\d+` ⇒ 2 ĐỎ · `.*` ⇒ 2 ĐỎ · bỏ `NGU_CANH` ⇒ 1 ĐỎ · bỏ `if not dong` ⇒ 1 ĐỎ. Trên `5d17b83` (mã+bài cũ) 27 xanh; ngọn 30 xanh.
- **PII**: `git grep` toàn nhánh DT6 — 0 chỗ đầu số TK thật trong `tools/` · `tests/` của DT6; còn 4 chỗ **có sẵn ở nhánh làm việc, ngoài DT6** *(3 HTML BA `Artifacts/` + `mapping_master_cfg.json`)* ⇒ báo orchestrator. Dòng sổ R1 tự trích 3 số đầu ⇒ đã che ở v0.2. Ảnh: 0 `@` · 0 tên ngân hàng.
- **Ảnh** `tests/fixture/dap_an/{gl_hr_407,408,413,cfa3}.json` = `5d17b83` từng byte *(`git diff` 0)*.
- **Gộp thử** `thu/DT6` = nhánh làm việc `aa97343` + `isp/DT6`: xung đột **2 tệp** `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(sàn 3616 vs 3591)* ⇒ giữ nhánh làm việc, sàn = thu thập thật **3650** *(web 675)*.
- `--duong-nen --cong 5436` MỘT lần: **ĐẠT** — tập đỏ + XFAIL **28 = 28** *(12 đỏ + 14 lỗi + 2 XFAIL; thêm 0 · bớt 0)*, chạy **3650**; web 3 = 3, chạy 675. `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` 45/45.
- **Kích thước** *(GHI NHẬN `DT6-R2-02`)*: `.git` 13.192.499 → 13.236.283 B *(+43.784 B)*; pack 10,74 MiB.
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT6.md` v0.2.
