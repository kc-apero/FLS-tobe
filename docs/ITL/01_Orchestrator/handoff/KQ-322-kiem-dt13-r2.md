# KQ-322 — R2 CUỐI kiểm `DT13` · `WO-319` · `BG-320` *(vòng sửa sau R1 `KQ-321`)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT13.md` v0.2. Đo trên `isp/DT13` @ `ab831d7` + cây gộp thử `thu/DT13` *(`origin/claude/bold-galileo-zukpaf` `3ea8052` + `isp/DT13`, gộp sạch, 0 xung đột; ⛔ commit)*. Vai KIỂM: ⛔ sửa mã.

| # | Việc | Kết |
|---|---|---|
| 1 | `-01` rào 605 | khuôn `sign_off_dau_vao`: `DAU_VAO_CHO={608}` · `CAM_CHO={605}`; hàm có tên `_rao_dau_vao.kiem_dau_vao_hop_le` ném `DauVaoSaiChoError` *(whitelist: PD 609 cũng ĐỎ)*. Số đo ghim **13.541/13.541** ô SỐ `cot[7:]` *(đo lại bằng bài; KQ-321 ghi 14.036 = đếm cả chữ — Đ4)*. Docstring hết `test_AC4_engine_khong_doc_dap_an`; 2 bài viện dẫn **tồn tại**. Đột biến engine giả ở `fls/` đọc ảnh mà ⛔ gọi hàm ⇒ `test_quet_ma_thuc_…` ĐỎ |
| 2 | `-02` rào 610 | `ccr_daily_report_2`: `{615}`/`{610}`; `kiem_dau_vao_hop_le(…,"610")` ném lỗi; **25.185/26.272 = 95,9 %**. BG tách đếm **chép 23.746 · tính 24.275** *(= 48.021 − 23.746; 49,4 % chép)*, dặn "⛔ cộng chung thành khớp". Đột biến engine giả ở `tools/` ⇒ ĐỎ |
| 3 | Ảnh | `git diff 90e797c ab831d7 -- tests/fixture` = **0**; `76e752a` *(R1)* ↔ `ab831d7` **0**; 7 tệp đổi = BG · 2 khuôn · module rào · bài · sàn *(chỉ thêm khai + bài)* |
| 4 | PII | `quet_pii_repo` cây gộp **0 chỗ · 0 tệp** *(quét thật: cho=46 ref=26 tk=1 — mẫu không rỗng, Đ3)*; **6/6 commit** nhánh *(`76e752a`…`ab831d7`, `git worktree` từng sha)* đều **0** |
| 5 | Đột biến mới | **9**: **6 cắn** *(M1 engine 605 · M2 engine 610 · M6 thêm 605 vào CHO · M7 thêm 610 vào CHO · M8 đổi 23746 · M9 bỏ whitelist)*; **3 sống** *(M3 gọi hàm với `608` trong engine 605 · M4 chỉ nhắc tên hàm trong chú thích · M5 `glob dau_vao/`)* ⇒ `DT13-R2-01` GHI NHẬN — hôm nay **0** engine đọc hai ảnh nên chưa lọt. Nền 16/16 xanh; **lưu ý phương pháp:** `sed` + `git checkout` cùng giây giữ nguyên cỡ tệp ⇒ `.pyc` cũ làm nền đỏ giả — đã xoá `__pycache__`, chạy lại 16/16 |
| 6 | Cổng | `--duong-nen --cong 5447` *(một mình, MỘT lần)* **ĐẠT**: `12 failed · 4744 passed · 2 xfailed · 14 errors` = tập đỏ nền **28 = 28** node id *(thêm 0 · bớt 0)*, chạy **4.772** *(mong ≥ 4772 — sàn = thu thập thật cây gộp, 0 xung đột sàn)*; `tests/web` **3 = 3**, chạy **690** · `lint-imports` **11 kept 0 broken** · `kiem_tai_lieu` **ĐẠT** *(480 file · 104 mã QĐ)* |

**Tập đỏ:** 28 = 28 *(0 thêm)*. **Sàn cây gộp:** 4772 = chạy 4772.
**GHI NHẬN ⇒ backlog:** `R2-01` quét mã từ vựng *(3 đường lách; AST + đối số PD khi H14 nối)* · `R2-02` hằng 23.746/48.021 khai tay, ⛔ tái lập offline · `R2-03` hàm rào ở `tools/`, 0 tệp `fls/` nhập `tools` — chốt nơi đặt khi mở H14. `DT13-R1-03…07` còn backlog như `KQ-321`.
**Gửi orchestrator:** `isp-gop-buoc` được — 0 CHẶN · 0 NÊN SỬA. Khi gộp, sàn `MONG_PYTEST_TOAN_BO` = thu thập thật cây gộp lúc đó *(4772 là của `isp/DT13` + `3ea8052`)*.
