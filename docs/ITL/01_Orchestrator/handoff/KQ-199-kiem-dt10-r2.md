# KQ-199 — Kiểm R2 CUỐI · ISP Step 27 · DT10 ảnh IX.DRV + đáp án ATL

| | |
|---|---|
| Phát bởi | fls-test (R2) · 2026-11-18 · `isp/DT10` @ `7c6c0f3` |
| Gửi | orchestrator |
| Kết | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · **2 GHI NHẬN** mới (`DT10-R2-01…02`) |

- **Gộp thử** `isp/DT10` vào nhánh làm việc `6afb0ce` *(C11 · H6 · DT8b)*: xung đột **2 tệp** — `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(chỉ hằng sàn + câu khai)*; giữ bản nhánh làm việc, đặt sàn = số THU THẬP đo cây gộp = **3616** *(web **675**)* = 3585 + 29 bài DT10 + 2 lệch nền có từ trước. Hằng `3588` của nhánh DT10 sẽ SAI trên cây gộp ⇒ `-R2-02`.
- `--duong-nen --cong 5437` MỘT lần, một mình: **ĐẠT** — `12 failed · 3588 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **3616** *(mong ≥ 3616)*; `tests/web` **3 = 3** · 675 bài. (3588 passed ở đây = số *đạt*, ⛔ số thu thập.)
- **Khớp IX.ALR (C11)**: 17 HD có luật = 8 By GI · 5 By NOEM *(OFR·HCC·REC·BON·OGA)* · 4 H1000 — đo từ `mapping_master_cfg.json`. `NOEM` ↔ ảnh `NOEM` **trùng tên**; ngoại lệ `OFR⇒CAH` ∈ 7 CDT1 của ảnh *(ASA·CAH·COR·CSM·CVL·SHQ1·SHQ2)*. **Lệch**: ALR `PE` ↔ ảnh `GI_PE`; ảnh có `GI_PM` mà ALR ⛔ tham chiếu; `IX.ALR` không có cột CDT1 ⇒ khoá nối H12 = `(driver, cdt1)` ⇒ GHI NHẬN cho H12 *(`-R2-01`, gắn `-R1-02` CMN)*.
- **Ghim checksum cắn**: đổi 1 chữ số cuối ô `GI_PE|CVL` tháng 2 của `ix_drv.json` ⇒ `test_anh_cong_dat_va_checksum[ix_drv]` **ĐỎ** *(1 failed · 28 passed)*; trả nguyên, `git status` sạch.
- Cây gộp thử: `lint-imports` **11 kept / 0 broken** · `kiem_tai_lieu` ĐẠT *(329 tệp · 104 mã QĐ)* · `soi_bang_tuyen` **khớp 45 tuyến**.
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT10.md` v0.2 *(THÊM 2 hàng)*. Cây gộp thử **không** commit/đẩy.
