# KQ-163 — biên bản kiểm R2 CUỐI *(ISP 3.1.2 · Step 18 · F4)*

| | |
|---|---|
| **Thuộc** | `BG-161` *(mục Vòng sửa)* · `KQ-162` · `WO-160` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-18 · `isp/F4` @ `fde46d9` · cụm `5444` |
| **Phán quyết** | **`ĐẠT` — đủ điều kiện GỘP.** `F4-R1-01` ĐÃ ĐÓNG · 0 phát hiện mới · `F4-R1-02…04` giữ MỞ *(GHI NHẬN ⇒ backlog)* |

## F4-R1-01 *(`git diff 3e93560 isp/F4`: 5 tệp — `man_f08.js` +6/−2, bài `test_isp_f08_fx.py` +55, hằng sàn ×2 tệp, `BG-161`)*
| Đo *(Chromium thật, 390 px, tab ⑥)* | Kết quả |
|---|---|
| Trang `documentElement`: `scrollWidth` vs `clientWidth` | `390 = 390` *(không tràn; mã cũ 475 > 390)* |
| Hàng `[data-thang]` *(mẫu số, Đ3)* | `37` |
| Bảng vs khung bọc | `473,6 > 388` px · khung `overflow-x:auto` ⇒ cuộn TRONG khung |
| **Tái đột biến** *(đổi `ngang` ⇒ lớp lạ, bản worktree rồi trả nguyên)* | bài `F4_R1_01` **ĐỎ** *(`sw 475`; `'visible' in ('auto','scroll')` sai)* · còn lại `4 passed`; trả nguyên ⇒ `5 passed` |
| Token | `0` dòng đổi ở `*.css`: dùng lớp `.ngang` có sẵn *(`hinh.css:504`, chỉ `overflow-x`/`max-width:100%`)* ⇒ ⛔ màu/khoảng cách gõ tay |

## Cây gộp thử `isp/F4` ⇒ `origin/moi/lam_viec` @ `b0bbe02` *(`--no-ff --no-commit`, ⛔ commit/push)*
- Xung đột: **2** — `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(đúng loại script + bài ghim ⇒ `--ours`)*; ⛔ xung đột khác.
- Sàn ở cây gộp = số THU THẬP `--collect-only`: toàn bộ **`3377 → 3385`** · `tests/web` **`667 → 675`** *(sửa cả hằng lẫn bài ghim)*.

| Cổng | Kết quả |
|---|---|
| `--duong-nen --cong 5444` *(một lần)* | dựng + 7 phép kiểm `[ĐẠT]` · toàn bộ `12 failed · 3357 passed · 2 xfailed · 14 errors` = nền **28 = 28** node id, chạy **3385** *(mong ≥ 3385)*, 0 skipped · 0 deselected |
| `tests/web` | script bị dừng ở hạn nền *(≈ 7 phút)* trước phép so web ⇒ chạy riêng `pytest tests/web`: `3 failed · 672 passed` = **675**; 3 đỏ cùng họ `wo022`/`wo042` đã nằm trong nền *(nền web 3 = 3)* |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT *(292 file · 2.529 bảng)* |
| `kiem_thuyet_minh.py` | `31/31 nút` ĐẠT |

## Kết
Đủ điều kiện **GỘP**. Khi gộp: xung đột script + bài ghim ⇒ giữ bản nhánh làm việc, nâng sàn **`3385` / `675`** *(hoặc số thu thập lúc gộp, ⛔ cộng tay)*. Sổ: `SO_PHAT_HIEN_ISP-3.1_F4.md` v0.2.
