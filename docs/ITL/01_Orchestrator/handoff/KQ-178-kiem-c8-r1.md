# KQ-178 — biên bản kiểm `BG-177` *(R1 · ISP 3.1.2 · Step 22 · C8)*

| | |
|---|---|
| **Thuộc** | `BG-177` · `WO-176` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-18 · `isp/C8` @ `7d17b48` · cụm `5447` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 3 NÊN SỬA · 3 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C8.md`)*. AC đúng; chỗ hở là bài canh *(riêng tư, oracle rỗng, lỗi có tên)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `pytest test_to_chuc.py test_to_chuc_pg.py test_cua_lenh_cho_pg.py` | `28 passed` *(8 + 6 + hồi quy 14)* |
| `--duong-nen --cong 5447` *(một mình)* | `KẾT: ĐẠT` · `12 failed · 3393 passed · 2 xfailed · 14 errors` = nền **28 = 28** node id *(thêm 0 · bớt 0)*, chạy **3421** *(mong ≥ 3421)* · `tests/web` nền **3 = 3**, chạy **675** |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL **43** tuyến |
| `kiem_tai_lieu.py` | ĐẠT *(300 file · 2.548 bảng)* |

⇒ Tập đỏ **= 28** *(BG-177 lo `test_chi_mot_cho_ghi_tay` đã sửa bằng `ghi_cdt_la` ⇒ ⛔ đỏ mới)*.

## AC *(đo · nhãn · mẫu số)*
| AC | Đo | Phán |
|---|---|---|
| C8-B1 | CDT biết ⇒ CDT1 đúng + `0` sự kiện *(đơn vị + pg)*; TK→LE qua Mapping Master | ĐẠT *(xem `C8-R1-05`: TK→CDT1 ⛔ có trong ảnh)* |
| C8-B2 | `XYZ` ⇒ `cdt1=None, la=True`, đúng `1` sự kiện, thấy ở `GET /queue` *(mẫu số 1 hàng ≠ 0)*; gọi lại ⇒ vẫn `1`; dòng khác ⇒ `cdt_la = None` | ĐẠT |
| Hồi quy | `test_cua_lenh_cho_pg.py` | ĐẠT |
| Số đo *(Đ4)* | CDT Correct **13** dòng ảnh *(ISP 18 = bề vùng sheet)* · **7** CDT1 chuẩn khác nhau *(ISP 8)* · **69** hàng `R |` = **59** pháp nhân *(19 mã LE)* + **8** `CN` + **2** `Cash Treasury` — đo lại bằng script độc lập ⇒ khớp | ĐẠT |
| Chỉ-thêm `0027` · lỗi có tên | ⛔ di trú mới; `nap` chỉ-thêm *(phiên bản +1, `khong_doi`)*; `ORG_HONG`/`CDT_RONG`/`CDT_TRUNG`/`TK_RONG`/`TK_TRUNG` có tên *(⛔ `TK_TRUNG` có bài — `C8-R1-03`)* | ĐẠT một phần |

## Riêng tư — `CN`
Kho `fls_test` `IX.ORG`: **295** hàng `tk:` ⇒ **0** hàng `CN`/`Cash Treasury`/`an_danh`/số TK; ca phá ⇒ bắt **1/1**. Quét `fls/`·`tools/`·`to_chuc.py`·`BG-177` ⇒ **0** số TK. ⚠ `C8-R1-01`: C8 thêm **1** số TK `CN` vào `test_to_chuc.py`; `C8-R1-06`: ảnh DT3 có sẵn.

## Oracle `do_trang_hang_cho.py`
Cột `cdt_la` bằng truy vấn tương quan *(⛔ chép CTE `cl`)* ⇒ độc lập cấu trúc; nhưng chỉ đo trên **tập rỗng** *(kho `fls` rỗng ⇒ bài `so_that` đỏ nền)* ⇒ `C8-R1-02`.

## Đột biến *(20 khai, 19 đo, bản sao `git archive`; nền `79 passed`)*
**BỊ BẮT 11:** M1 *(lạ→SHQ2)* · M2 *(⛔ ghi sự kiện)* · M3 *(khử trùng)* · M4 *(lọc `evt_type`)* · M6 · M7 *(CN vào kho)* · M9 · M14 · M15 · M17 · M19.
**SỐNG 8:** M5 *(sự kiện cũ nhất)* · M10 *(`TK_TRUNG`)* · M11 *(`_kiem_org`)* · M12 *(`actor`)* · M13 *(CDT rỗng)* · M16 *(`strip`)* · M18 *(lock)* · M8 *(tương đương)*. M20 ⛔ đo *(mẫu khớp 2 lần)*.

## Hỏi orchestrator
`C8-R1-05`: nguồn TK→CDT1 — chuyển BA. R2: sửa `-01`…`-03` *(rẻ, ~3 bài + 1 dòng)*.
