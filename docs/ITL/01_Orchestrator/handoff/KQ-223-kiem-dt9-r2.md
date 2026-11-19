# KQ-223 — biên bản kiểm R2 `BG-221` *(Step 34 · DT9 · soát vòng sửa sau `KQ-222`)*

| | |
|---|---|
| **Thuộc** | `BG-221` mục "Vòng sửa sau R1" · nhánh `isp/DT9` @ `8b43b47` |
| **Kiểm bởi** | `fls-test` · 2026-11-19 *(⛔ sửa mã)* |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA** *(`-01` · `-02` đóng; `-03…-06` GHI NHẬN ⇒ backlog)* · sổ `SO_PHAT_HIEN_ISP-3.1_DT9.md` v0.2 |

## Soát vòng sửa
1. **`DT9-R1-01` đóng:** `TAP_THANG_SO` khai tập tháng mỗi sổ theo dữ liệu *(OMC 10 tháng · SC 9 · PS 9; mẫu số > 0, Đ3)* + bài "202603–202609 = 0 dòng ở CẢ ba sổ". Errata AP/ISP ghi trong `BG-221`. Thêm 1 dòng 2026 vào ảnh ⇒ ĐỎ *(đo: `ps_mid2` ⇒ 6 bài đỏ, gồm hai bài tập tháng)*.
2. **`DT9-R1-02` đóng:** `lac` 72 hàng SC ghim theo tên *(70 "chưa chia" + 2 "chia lệch thật" `478` · `505`)*, phân loại tính lại từ ảnh. Đổi tên một hàng trong `lac` ⇒ ĐỎ; đổi một tên trong bản ghim ⇒ ĐỎ.
3. **Ảnh `tests/fixture/dap_an/*`:** 9/9 băm khớp `4e49253` *(0 byte đổi)*. Vòng sửa chỉ chạm 1 bài + 2 tệp sàn + tài liệu; mã hệ thống 0 dòng.
4. **Đột biến *(cây tạm, đã trả nguyên)* — 4/4 CHẾT** *(`-x` dừng ở bài đỏ đầu)*: thêm dòng 2026 vào `omc_mid1` · đổi tên một `lac` ở `sc_mid3` · đổi một tên trong `LAC_SC_CHUA_CHIA` · đổi `TAP_THANG_SO` OMC 10→9 tháng; thêm dòng 2026 vào `ps_mid2` chạy đủ ⇒ 6 đỏ. Gốc: **141 passed**.

## Cây gộp thử *(`thu/DT9` = `origin/claude/bold-galileo-zukpaf` @ `cd7a836` + `isp/DT9`; ⛔ đẩy)*
- **Xung đột 2:** `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(chỉ hằng sàn `MONG_PYTEST_TOAN_BO`: 3864 ↔ 3904)* ⇒ gộp tay theo thu thập thật: **4014** *(`pytest --collect-only`; web giữ 675)*. Báo orchestrator nâng sàn khi gộp thật.
- `--duong-nen --cong 5445` *(1 lần, một mình)*: **ĐẠT** — toàn bộ: tập đỏ 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **4014** *(sàn ≥ 4014)*, skipped 0 · deselected 0; web 3 = 3, chạy **675**.
- `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu.py` ĐẠT *(365 tệp · 2692 bảng)* · `soi_bang_tuyen.py` KHỚP 46 tuyến.

## Việc kế
Orchestrator: gộp `isp/DT9` vào nhánh làm việc, nâng sàn theo thu thập cây gộp; sửa AP §3.4.1 + ISP Step 34 `DT9-B1` ở 3.1.3. `-03…-06` ⇒ backlog.
