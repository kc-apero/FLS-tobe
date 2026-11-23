# KQ-333 — R2b nhẹ `I2` · `WO-315` · `BG-316` *(sửa tích hợp I2 × H14, chữ ký 605 23/11)*

| | |
|---|---|
| **Kết quả** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA** · 2 GHI NHẬN |
| **Phát phiếu** | `fls-test` *(vai KIỂM — ⛔ sửa mã)* · 2026-11-23 · `isp/I2` `0c846c4` *(`15288f1` gộp H14 `b1038a7` + `0c846c4`)* · cây gộp thử *(⛔ commit)* = `origin/claude/bold-galileo-zukpaf` `6e68811` + `0c846c4`, gộp **sạch**, 0 xung đột · cụm PG 5446 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_I2.md` *(v0.6)* |

| # | Kiểm | Đo được |
|---|---|---|
| 1 | 5 bài đỏ cũ *(`B1[WP-C5c]` · `F1_cong_bon_cha` · `C5c_H14_R2_01` · `F1_vm_bon_the` · `F1_F2_chromium_that`)* | cả 5 **xanh** *(30 passed)*, kỳ vọng mới = trạng thái ký thật: C5c `dat True`, cha C5 `True`, chuỗi `605: DỪNG có chữ ký KhanhCQ 2026-11-23` + `độ phủ 615: ô so …` ở cổng C5c; `khong_do_duoc == []`; độ phủ 615 mẫu số ≠ 0 *(`0 < o_so ≤ o_dap_an_so`)*. `hd2_cong.json` thật: `13760/48021 ô số · 34261 chưa so`. Diff so `cd04d58`: **0 bài bị xoá**; assert đổi chỉ ở chỗ trạng thái 605 *(`None`→`True`, `KHÔNG ĐO ĐƯỢC`→`ĐẠT`, không `KHÔNG ĐẠT`)*; thêm chữ ký + độ phủ ở cổng C5c. ⛔ nới |
| 2 | Ca gỡ ký hai chiều | 2 bài mới: `test_C5c_go_ky_605_…` *(gỡ `DUNG_KY` ⇒ C5c `None`, `khong_do_duoc` = `605`, `dung_co_ky` rỗng; đủ ký ⇒ `True`)* · `test_F1_go_ky_605_…` *(cha C5 `None`, chuỗi có `605`, thẻ F03 C5 `KHÔNG ĐO ĐƯỢC` + `605`)*. **Chứng minh ĐỎ** *(bản sao `git archive`, trả nguyên)*: ① patch gỡ ký thành no-op ⇒ **2 đỏ** đúng 2 bài đó · ② `DUNG_KY = {}` ở `tools/do_hd2_c5c.py` ⇒ **6 đỏ** *(5 bài cũ + ca gỡ ký)* |
| 3 | D1 + B3 | giữ xanh *(nằm trong 30 passed, cả nhánh I2 lẫn cây gộp)*; ⛔ nới |
| 4 | Cây gộp thử | `grep` dấu xung đột + `git ls-files -u` = **0** · thu thập thật **4887** = `MONG_PYTEST_TOAN_BO`, web **690** · `test_hd2_xuyen_suot.py` **30 passed** *(166 s)* · `tests/api/test_isp_gates_hd2.py` + `tests/oracle/test_do_hd2_c5c.py` + `tests/test_dung_moi_truong_isp.py` **196 passed** · `--duong-nen --cong 5446` MỘT lần, một mình: **`KẾT: ĐẠT`** — toàn bộ `12 failed · 4859 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy **4887** ≥ 4887, skipped 0; web `3 failed · 687 passed`, **3 = 3**, chạy 690 · `kiem_tai_lieu` ĐẠT *(494 tệp · 2983 bảng · 980 ô ngày · 104 mã QĐ)* · `lint-imports` 11 kept · `quet_pii_repo` **0 chỗ · 0 tệp** |
| 5 | `fls/` | 2 commit sửa `15288f1`+`0c846c4` so cha H14 `b1038a7`: **0** tệp · so cha I2 `cd04d58`: **1** tệp `fls/repo/doc_bao_cao.py` do H14 `a59f4b9` *(`KQ-324` ĐẠT)* ⇒ `I2-R2b-02` |

**GHI NHẬN** *(⛔ chặn)*: `I2-R2b-01` lời *"mong 28 passed"* ở `BG-316`/`HANDOFF` cũ — thật là **30** *(29 + 1 skipped khi thiếu Chromium)* · `I2-R2b-02` cách đọc *"0 tệp `fls/`"* theo cha nào.

**Lưu ý phương pháp:** lượt đo đầu của phiên này lỡ chạy trên nhánh cục bộ cũ `cd04d58`; đã loại, mọi số trên đo lại ở `0c846c4`.

## Điều kiện MERGE còn lại
Như `KQ-318` mục 1–3, trừ `O6` đã ký 23/11 và 605 đã ký. Chủ chạy lại trên máy chủ: mong **30 passed** *(không phải 28)*.
