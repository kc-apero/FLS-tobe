# KQ-214 — biên bản kiểm `BG-213` *(R1 · ISP 3.1.2 · Step 33 · C7)*

| | |
|---|---|
| **Thuộc** | `BG-213` · `WO-212` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-19 · `isp/C7` @ `dcef226` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 2 NÊN SỬA · 5 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C7.md`)*. Hành vi đúng ở mọi biên đo; 2 hàng NÊN SỬA là **bài thiếu** *(ca đổi số sau ký · ký song song)*, ⛔ lỗi hành vi |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --cong 5434` | `KẾT: ĐẠT` · kho rỗng |
| `test_ky_fx_pg.py` | **9/9** xanh |
| `--duong-nen --cong 5434` *(một mình, 1 lần)* | `ĐẠT` · tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)* · chạy **3659** ≥ 3659 · skipped 0 · deselected 0 *(12 failed + 14 errors + 2 xfailed = 28 node id nền)* |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL **46** tuyến |
| `kiem_tai_lieu.py` | ĐẠT |

## Trọng tâm
| # | Kết luận | Đo |
|---|---|---|
| 1 | **`the.kiem` AN TOÀN** — sửa ⛔ nới cửa | 2 bản *(`4a13162` ↔ `dcef226`)* × **3.523** thẻ *(23 tay: hết hạn · sai chữ ký · `alg:none` · thiếu `sub`/`exp` · … + 3.000 ngẫu nhiên + 500 đột biến)*: **0** thẻ mới được nhận; **318** `UnicodeDecodeError` ⇒ 401, chỉ loại ấy. Hồi quy `rac.rac.rac` = bài `B5`; hoàn nguyên ⇒ ĐỎ *(M18)*; bỏ so chữ ký/`alg`/`sub`/`exp` ⇒ ĐỎ cả 4 |
| 2 | **Lệch AC-4: giữ cửa** — `07_API_CONTRACT §1:56` đã ghi **400, ⛔ âm thầm bỏ qua**; AC sai chữ | `C7-R1-04` ⇒ **câu BA** sửa chữ AC-4; ⛔ sửa mã |
| 3 | `actor` CHỈ từ token; ký lại 409 ⛔ thêm dòng; **ký song song ⇒ đúng 1 thành công** | đột biến lấy từ thân ⇒ ĐỎ; **5 tháng × 8 luồng**: mỗi tháng 1×`201` + 7×`409`; bỏ khoá advisory ⇒ ĐỎ *(chỉ script R1)* ⇒ `C7-R1-02` |
| 4 | `fx_cua` CHẶN có tên: chưa ký · thiếu · đổi số sau ký *(bài phụ bản sao: đổi `HKD` ⇒ `FxChan "ĐỔI"`, GET `chua_ky`, ký lại 201)* — ⛔ rơi gần nhất. Dấu vân = sha256 của `[yyyymm, [[tiền tệ, str(Decimal)]…]]` theo `TIEN_TE` cố định *(thứ tự ổn định)*, **nhưng ⛔ chuẩn hoá số** | `C7-R1-01` *(chỉ ghim bằng dấu vân giả; M7·M16 sống)* · `C7-R1-03` |
| 5 | `bang_ghi = (fls_cau_hinh_ban, fls_cau_hinh_dong)`, thêm `fls_itl` ⇒ ĐỎ *(M9)*; `07 §4i` dòng POST còn ⬜ | đạt |
| 6 | Câu `FLS-CAUHINH-DA-KY` có ở `goi_cua.js` *(bỏ ⇒ ĐỎ, M15)*; `FX_CHAN` chưa có mã/câu — hôm nay đúng *(chưa ai gọi)* | `C7-R1-05` |

## Đột biến *(bản sao `git archive`)*
**19 chỗ: 15 giết · 4 SỐNG** — `M2` · `M19` *(`C7-R1-07`)* · `M7` · `M16` *(`C7-R1-01`)*. `M6` chỉ bị script R1 cắn.

## Câu BA
AC-4 sửa chữ *(`C7-R1-04`)*; ai là "người ký sau cùng" khi ký lại sau đổi số *(`C7-R1-06`)*; dấu vân chuẩn hoá số hay không *(`C7-R1-03`)*.

## Gợi ý R2
Chỉ cần thêm hai bài pg *(`-01` đổi 1 tiền tệ sau ký · `-02` 8 luồng cùng tháng)* + sửa chú thích `fx.py:312`. ⛔ đụng logic.
