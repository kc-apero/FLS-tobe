# KQ-167 — R2 CUỐI kiểm `H5` *(ISP 3.1.2 · Step 16 · WO-164 · BG-165 · KQ-166)*

| | |
|---|---|
| **Phát bởi** | `fls-test` R2 · 2026-11-18 · `isp/H5` @ `8abde6f` · cụm 5435 |
| **Kết luận** | **ĐẠT — đủ điều kiện GỘP.** 0 CHẶN · 0 NÊN SỬA · 0 phát hiện mới *(sổ `SO_PHAT_HIEN_ISP-3.1_H5.md` v0.2)* |

## Số đo *(mỗi số một vật)*
- `git diff 6cf13d3 isp/H5`: 5 tệp *(2 bài · 1 BG · script + bài ghim sàn)*, ⛔ đổi mã công cụ.
- WP-C3a `do_hd2 --goi WP-C3a`: **205.175/205.175** ô so · lệch ngoài tên 0 · KPI loại 76.000 · `KẾT: DAT`. *(Nhãn "10.540 ô ≠ 0" của `-02`: đã vào `BG-165`; R2 **đọc**, ⛔ tự đo lại.)*
- `H5-R1-01` **ĐÓNG**: bài quét khoá cấm trên khoá **từng dòng** + đòi mỗi dòng đúng tập khoá khai. Đột biến **thật** *(thêm `C` vào `gl_cf_dau_vao.json`, dòng 100; bài mới 2 tham số `C`·`G`)*: `3 failed, 5 passed` *(`B2_cot_dung_khong_PII` ĐỎ — R1 là 23/23 xanh)*; trả nguyên, `git status` sạch. Mẫu số: 8 bài, 12.385 dòng.
- `H5-R1-03` **ĐÓNG**: thêm `"GI"` vào `MA_KPI` ⇒ `test_H5_R1_03_MA_KPI_ghim_20_ma` ĐỎ `1 failed`; trả nguyên. `H5-R1-02` giữ MỞ *(ghi nhận, chưa khoá bằng `mong`)*.
- Bài H5 sau sửa: `20 passed` *(2 tệp)*.

## Cây gộp thử `origin/moi/lam_viec` @ `d95fc78` + `isp/H5` *(⛔ commit/push)*
- **Xung đột: 2** — `tools/dung_moi_truong_isp.sh`, `tests/test_dung_moi_truong_isp.py` *(đúng loại script + bài ghim sàn)* ⇒ `checkout --ours`; ⛔ xung đột khác *(`hd2_cong.json` sạch)*.
- **Sàn = thu thập cây gộp:** `3434` bài *(lam_viec 3407 + 27 của H5)* · web `675` ⇒ nâng `MONG_PYTEST_TOAN_BO` 3407 → **3434** *(script + bài ghim — orchestrator làm khi gộp)*.
- `--duong-nen --cong 5435` một lần: toàn bộ `12 failed, 3406 passed, 2 xfailed, 14 errors` ⇒ tập đỏ **28 = 28** *(thêm 0 · bớt 0)* · web `3 failed, 672 passed` ⇒ **3 = 3**. `lint-imports` 11 kept · `kiem_tai_lieu` DAT *(302 tệp)*. **KẾT: ĐẠT.**

## Còn mở *(backlog, ⛔ chặn gộp)*
`-02` khoá `mong` ô ≠ 0 · `-04` WP KPI · `-05` BA: 153 dòng ITE · `-06` cột `itl_id` thừa.
