# KQ-174 — biên bản kiểm `BG-173` *(R1 · ISP 3.1.2 · Step 21 · C9 IX.VEN)*

| | |
|---|---|
| **Thuộc** | `BG-173` · `WO-172` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-18 · `isp/C9` @ `2555054` · cụm `5444` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C9.md`)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5444` *(một lần, một mình)* | `KẾT: ĐẠT` · `12 failed · 3419 passed · 2 xfailed · 14 errors` = nền **28 = 28** node id *(thêm 0 · bớt 0)* · chạy **3447** *(mong ≥ 3447)* · skipped 0 · deselected 0 ⇒ **đã đổi `C5R1_05` ⇒ 29 → 28 xác nhận** |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT *(300 file · 2.549 bảng)* |
| `soi_bang_tuyen.py` | KHỚP SQL **44** tuyến-đo · `/config/ven` OK |

## AC
| AC | Đo | Phán |
|---|---|---|
| C9-B1 | PG thật: **42** dòng *(36 bộ khác nhau)* · 5 nhãn `{Max 12 · VD341 12 · VD444 8 · VD428 3 · VD62 1}` + `thường 6` · `pct` null **14/42** · **7** CDT1 khác nhau · nạp lại cùng ảnh ⇒ `khong_doi` · kiểm trước ghi ⇒ `0` phiên bản thêm · bản SQL tay hỏng ⇒ `BanHong`, bản tốt kế thắng · tuyến HTTP thật: 200 · `?run_id=` ⇒ **400** `FLS-BAD-REQUEST` · 401 · POST 405 · `ChuaKhai`/`BangLa`/`BanHong` ⇒ 409/404/500 | ĐẠT |
| C9-B2 | `(vendor, No)` trùng ⇒ `LoiVen` có tên, một dòng · `dong_sheet` trùng · thiếu từng nhãn riêng ×5 · nhãn lạ · CDT1 ≠ 7 ×4 · tập rỗng *(mẫu số `0` ⇒ nổ — `Đ3`)* · ô hỏng ×11 · cột lạ | ĐẠT |
| Chỉ-thêm · 0027 | 0 di trú mới *(`pg_verify` 27/27)* · `fls_cau_hinh_*` chỉ INSERT *(bài bản hỏng ghi SQL tay)* | ĐẠT |

## Đột biến *(16, bản sao `git archive 2555054`)*
BỊ BẮT **16/16**: bỏ `(vendor,No)` · bỏ thiếu-nhãn · CDT1 trùng lọt · `pct <=0→<0` · tuyến nhận `run_id` · `nap` ⛔ kiểm trước ghi · nạp 5/7 CDT1 · bảng tuyến thiếu 1 bảng · `cashin_day` hi 31→40 · bỏ cột lạ · tập rỗng xanh · khoá kho = `No` · nuốt `LoiVen` ở `doc_ven` · `pct` nhận float · bỏ nhãn VD62 · `@cdt1` +1 phần tử. **Việc đổi `C5R1_05`:** đột biến gốc `khong_doi` so bản ĐẦU ⇒ bài ĐỎ ⇒ bài **⛔ yếu đi**; nhưng sinh ghép nối ẩn ⇒ **`C9-R1-01`**.

## Phát hiện
- **`C9-R1-01` NÊN SỬA** — `C5R1_05` nạp 3 bản vào `IX.DRV` mà `test_AC5_…` đòi `IX.DRV` rỗng: đảo thứ tự ⇒ AC5 ĐỎ *(`_max_phien = 3`)*; thứ tự tệp + `fls_test` dựng lại ⇒ xanh. Đổi sang `IX.ALR`/`IX.TMP` *(⛔ ai đo)*.
- `C9-R1-02..04` GHI NHẬN *(`TypeError` thô ở CDT1 ⛔ băm được · 4 chốt dữ liệu lối vào lọt · `BA-07:854` còn "36 dòng ⬜" + `CLAUDE.md:71` "37 tuyến")*.
Tác giả chốt (1) danh mục 7 CDT1, (2) 42 dòng — R1 **chấp nhận**, ⛔ tính là lệch.
