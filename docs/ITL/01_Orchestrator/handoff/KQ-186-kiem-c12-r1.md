# KQ-186 — Kiểm R1 · ISP 3.1.2 · Step 26 · C12 (IX.PL) · `BG-185`

| | |
|---|---|
| **Từ → Đến** | fls-test (R1, Sonnet 5.5) → orchestrator / owner·BA |
| **Mã kiểm** | `isp/C12` @ `c5e94e7` · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C12.md` v0.1 |
| **Kết** | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **2 NÊN SỬA** *(chênh nguồn ATL — quyết ở owner/BA, trước H13)* · 4 GHI NHẬN |

## Số theo mức
| CHẶN | NÊN SỬA | GHI NHẬN |
|---|---|---|
| 0 | 2 (`C12-R1-01` chênh công thức · `-02` dấu) | 4 (`-03…-06`) |

## Bài mục 6 Step 26
- `C12-B1/B2/B3` + kho: `34 passed` *(0,39 s)*. `--duong-nen --cong 5446` (một mình): **tập đỏ 28 = 28** node id *(thêm 0 · bớt 0 · XFAIL 2 = 2)*, chạy **3500** *(mong ≥ 3500)*, `tests/web` 3 = 3 · `lint-imports` 11 kept 0 broken · `soi_bang_tuyen` 44/44 · `kiem_tai_lieu` ĐẠT.
- Chỉ-thêm `0027`: C12 ⛔ di trú mới *(`git diff a1b2444..HEAD`: 0 tệp `fls/db/`)*; `IX.PL` dùng bảng sẵn có.
- `nap_ix_pl` kiểm **trước** khi ghi: bài kho ĐẠT; nhưng `nap()` trực tiếp ⛔ có bài *(`-03`)*, mã lạ ⛔ bắt khi `cay=None` *(`-04`)*.

## PL khớp nguồn — **3/7** *(đo trên công thức ô THẬT, ⛔ trên mô tả)*
Nguồn: sheet ATL `A7:AZ90`, `FORMULA`; công thức mỗi dòng giống nhau 46/46 cột. **PL2 · PL3 · PL4** lệch **0** *(46 cột, 28 cột ≠ 0)* **khi dùng dấu `+` của sheet**. **PL5**: sheet ⛔ tính theo tháng *(N:Y rỗng)*. **PL6** = `PL4 + …` *(bỏ COM)* lệch max 0,0914 · **PL7** thừa hưởng · **PL8** dùng `TAC` ⛔ `CIT` lệch 0,0797. Dấu: sheet `+` chi phí âm ⇒ `−` của mã lệch 88–107 nếu HD mang dấu sheet.

## Đột biến *(bản sao `git archive`, 14)*
11 giết · 3 sống: `nap` nhánh `IX.PL` bỏ · `_ma_cua` bỏ dấu đơn ngôi *(2 lỗ phủ thật)* · regex `*` *(tương đương)*. Giết cả "đổi PL6/PL8/PL3 theo sheet" ⇒ bài ghim **bản mô tả**, ⛔ ghim nguồn.

## Việc kế
Owner/BA quyết từng chênh PL5–PL8 + quy ước dấu *(`-01`, `-02`)*; DEV vá `-03…-06` khi tiện. Sổ ⛔ sửa mã *(vai KIỂM)*.
