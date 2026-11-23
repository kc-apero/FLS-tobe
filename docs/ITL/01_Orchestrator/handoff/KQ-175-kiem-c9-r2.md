# KQ-175 — biên bản kiểm R2 CUỐI *(ISP 3.1.2 · Step 21 · C9 IX.VEN)*

| | |
|---|---|
| **Thuộc** | `BG-173` · `WO-172` · tiếp `KQ-174` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-18 · `isp/C9` @ `9a01352` · cụm `5444` |
| **Phán quyết** | **`ĐẠT` — đủ điều kiện GỘP** · `0 CHẶN · 0 NÊN SỬA mở · 1 GHI NHẬN mới` *(sổ `SO_PHAT_HIEN_ISP-3.1_C9.md` v0.2)* |

## Việc 1 · `C9-R1-01` ĐÓNG
`git diff 7496bd5 isp/C9` = 2 tệp *(`BG-173` +8 dòng · `test_kho_cau_hinh_pg.py` +8/−3, chỉ đổi `IX.DRV`→`IX.ALR` + chú thích)*; ⛔ đổi mã `fls/`.
Đột biến trên bản sao `git archive 9a01352` *(chạy `-k "C5R1_05 or AC5 or C5R1_03"`)*: gốc `4 passed` · `ORDER BY … ASC` *(`khong_doi` so bản ĐẦU)* ⇒ `1 failed` · `khong_doi=True` ⇒ `1 failed` · đảo thứ tự `C5R1_05` → `AC5` ⇒ `2 passed` *(hết ghép nối ẩn)*. `khong_doi=False` cố định ⇒ sống *(ngoài phạm vi bài này; `test_vendor_pg` đo `khong_doi=True` nạp lại)*.
## `C9-R2-01` GHI NHẬN — phụ thuộc ngầm vào `IX.ALR`
Mô phỏng C11 thêm kiểm riêng `IX.ALR` ở `_kiem_noi_dung` ⇒ `test_C5R1_05` ĐỎ `1 failed`. Đề xuất bảng mẫu bền: `monkeypatch` thêm `bang` giả duy nhất mỗi lần chạy *(`IX.ZZ_<uuid>`)* vào `BANG_HOP_LE`, chỉ kiểm HÌNH chung. Làm khi C11 gộp ⇒ backlog.

## Việc 2 · cây gộp thử *(`/tmp/r2_c9/gop` @ `4ce762e` + `merge --no-ff --no-commit isp/C9`; ⛔ commit/push)*
Xung đột **0** *(script + bài ghim hợp tự động; sàn script gộp = 3447)*. Thu thập cây gộp = **3447** *(= sàn)*.
| Cổng | Kết |
|---|---|
| `--duong-nen --cong 5444` *(một lần)* | **KẾT ĐẠT** · toàn bộ `28 = 28` node *(XFAIL 2 · thêm 0 · bớt 0)* · chạy 3447 · web `3 = 3` *(675 bài)* · HD1 9845/9967 |
| `lint-imports` | 11 kept / 0 broken |
| `soi_bang_tuyen` | KHỚP SQL **44** tuyến |
| `kiem_tai_lieu` | ĐẠT *(302 file · 2553 bảng)* |

## Còn mở *(backlog, ⛔ chặn gộp)*
`C9-R1-02…04` · `C9-R2-01` — GHI NHẬN.
