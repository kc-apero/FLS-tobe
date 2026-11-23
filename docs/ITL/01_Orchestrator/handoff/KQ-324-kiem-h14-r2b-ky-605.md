# KQ-324 — R2b nhẹ `WO-311` / `BG-312` *(ISP 3.1.2 · Step 46 · H14 — chữ ký chủ 605, 23/11)*

| | |
|---|---|
| **Kết quả** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA** · 3 GHI NHẬN |
| **Phát phiếu** | `fls-test` *(vai KIỂM — ⛔ sửa mã)* · 2026-11-23 · `isp/H14` `25adbef` *(diff `854550b..25adbef` = `a59f4b9` + `25adbef`)* + cây gộp thử `thu/H14` *(`origin/claude/bold-galileo-zukpaf` `8a04fd4` + `25adbef`, gộp **sạch**, 0 xung đột)* · cụm 5436 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H14.md` *(v0.4)* |

## Kết luận
Chữ ký 605 **đúng** và cổng cắn đủ ca hỏng. Phần ĐẠT ở `KQ-314` / `KQ-323` ⛔ soát lại.

| # | Kiểm | Đo được |
|---|---|---|
| 1 | `DUNG_KY["605"]` | đúng **4 trường**: `nguoi_ky` `KhanhCQ` · `ngay` `2026-11-23` · `ly_do` *(`[FS1][PLA5]` đã xoá, 0 ứng viên DT13, `sign_off_dau_vao` = vòng tròn)* · `nguon_quyet` `TIEN_DO 2026-11-23` — khớp dòng `TIEN_DO.md` 2026-11-23; `kiem_dung_ky(DUNG_KY) = []` |
| 1b | `kiem_dung_ky()` cắn | **11/11** ca hỏng, mỗi ca đúng **1** lỗi có tên *(thiếu trường · thừa trường · người ký rỗng · email · người ký không phải chuỗi · ngày `23/11/2026` · ngày `2026-02-30` · ngày có dấu cách · ngày kiểu số · lý do rỗng · nguồn rỗng)* + mã lạ `999` · chuỗi tự do `"x"` · kiểu list · `None` ⇒ **4/4** có tên |
| 1c | Chứng minh ĐỎ *(Đ5, bản sao `git archive`, trả nguyên `diff` = 0)* | ① `DUNG_KY = {}` ⇒ **12 đỏ** *(`test_do_hd2_c5c` + `test_isp_gates_hd2`; baseline 136 xanh)* · ② bỏ kiểm email ⇒ **1 đỏ** đúng ca `email` *(11 xanh)* · ③ `kiem_dung_ky` luôn `[]` ⇒ **9 đỏ** |
| 2 | `/gates` *(`doc_cong_hd2`, mẫu số 14 cổng, so `854550b` ↔ `25adbef`)* | chỉ **2/14** đổi `dat`: `HD2_WP_C5C` `None→true`, cha `HD2_WP_C5` `None→true`; **12/12** cổng còn lại giữ nguyên *(`true`)*; `da_do` có `605: DỪNG có chữ ký KhanhCQ 2026-11-23` **và** `độ phủ 615: ô so 13760/48021 ô số · 34261 ô số chưa so` |
| 3 | `hd2_cong.json` | diff **11+/5−**, chỉ khối `WP-C5c` *(`dung_ky`, `khong_do_duoc`, `dung_co_ky`, `dat`)*. Nạp nền `fls_test` *(IX.PER · IX.ALR 17 luật + ký · IX.PL)* rồi `do_hd2.py --goi WP-C5c --ghi` ⇒ `KẾT: ĐẠT`, `git status` **0 tệp** = **0 byte đổi** |
| 4 | Bài | `pytest --collect-only` = **4857** = `MONG_PYTEST_TOAN_BO` *(4843 + 14)*; web 690 giữ. 12 bài đổi `None→true` chỉ là hệ quả của chữ ký; các ca `None` được thêm lại bằng bài gỡ chữ ký *(2 chiều)* — ⛔ nới |
| 5 | PII | quét `quet_pii_repo.py` = **0 chỗ** · 0 tệp; email/tên người khác ngoài `KhanhCQ` trong dữ liệu: **0**; trong bài có địa chỉ chủ ở ca đột biến ⇒ `R2b2-01` |
| 6 | Cây gộp thử | `--duong-nen --cong 5436` một mình: `KẾT: ĐẠT` — toàn bộ `12 failed · 4829 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy **4857** *(mong ≥ 4857)*; web `3 failed · 687 passed`, **3 = 3**, chạy 690. `kiem_tai_lieu` ĐẠT *(487 file · 2.965 bảng)* · `lint-imports` 11 kept · `soi_bang_tuyen` KHỚP 49 tuyến |

`H14-R2-02` **đóng** *(đột biến chuỗi tự do `"x"` giờ ĐỎ có tên)*.

## GHI NHẬN ⇒ backlog
`H14-R2b2-01` *(email thật của chủ ở bài đột biến)* · `H14-R2b2-02` *(`/gates` không đối chiếu `dung_co_ky` ↔ `DUNG_KY`)* · `H14-R2b2-03` *(console còn in "605: DỪNG … cần nguồn" sau khi đã ký)*. Còn mở từ trước: `R2-03` · `R2-04` · `R2b-01` · `R2b-02`.

## Điều kiện gộp
H14 gộp được. Cổng C5 **xanh** *(`HD2_WP_C5C` = `HD2_WP_C5` = true)*. Ngoài phạm vi vòng này: ⛔ `kiem_thuyet_minh` · ⛔ `tests/web` ngoài đường nền.
