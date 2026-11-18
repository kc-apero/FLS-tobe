# BG-161 — bàn giao `WO-160`

| | |
|---|---|
| **Thuộc** | `WO-160` (ISP 3.1.2 · Step 18 · F4) |
| **Phát bởi** | `fls-dev` làn FE · 2026-11-18 |
| **Nhận** | `fls-test` (R1) |
| **Commit** | `claude/bold-galileo-zukpaf-isp/F4` @ `11b4c93` *(đã đẩy)* |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f08.js` *(mới)* | màn SCR-F08: bảng IX.FX chỉ đọc; nhãn CHẶN/TRÙNG/LẠC lấy từ `thieu[]`/`trung[]`/`lac[]`; tháng thiếu có HÀNG riêng; 0 nút; bốn trạng thái qua `TT.chay` |
| `fls/web/phuc_vu.py` · `index.html` · `ung_dung.js` | khai BẢNG TỆP + tab ⑥ + `VE_KHI_MO['man-f08']` |
| `tests/web/test_isp_f08_fx.py` *(mới, 4 bài)* | AC-1…AC-3 qua máy chủ thử thật + node headless |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3296→**3303**, `MONG_PYTEST_WEB` 667→**674** (cùng commit) |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5436` (một lần, một mình) | `KẾT: ĐẠT` · toàn bộ `12 failed, 3275 passed, 2 xfailed, 14 errors` = đường nền 28=28 node id, chạy 3303 (mong ≥3303) · web `3 failed, 671 passed` = nền 3=3, chạy 674 (mong ≥674) |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT (279 file, 2484 bảng) |
| `kiem_thuyet_minh.py` | `31/31 nút` ĐẠT |
| `pytest tests/web/test_khong_ma_mau_go_tay.py tests/web/test_phuc_vu.py` | xanh (117 passed cùng bài ghim + F08) |
| `kiem_so_song` · `khop_owner` · `soi_bang_tuyen` | ⛔ CHƯA CHẠY — phiếu không yêu cầu; không chạm tuyến/schema |

## Bằng chứng từng AC
| AC | Đỏ trước | Bằng chứng |
|---|---|---|
| AC-1 | `pytest tests/web/test_isp_f08_fx.py` (chưa có `man_f08.js`) ⇒ `4 failed` (`ENOENT man_f08.js`) | `test_AC1_F4_F1_…`: tuyến thật 37 `ky`, `lac=[202306]` (nền ≠ rỗng, Đ3) ⇒ màn 37 hàng, đúng 1 nhãn LẠC ở `202306`, 0 nút. Chromium thật: 37 hàng, LẠC=`['202306']`, 0 nút |
| AC-2 | cùng lượt đỏ | `…thieu_202408_nhan_CHAN`: nạp ảnh bỏ `202408` ⇒ tuyến `thieu=[202408]` ⇒ đúng 1 CHẶN, màn vẫn 37 hàng. `…trung…`: envelope bài khai (kho khoá theo yyyymm ⛔ nạp trùng được) ⇒ 2 hàng cùng tháng, đều TRÙNG, ⛔ gộp |
| AC-3 | cùng lượt đỏ | `test_AC3_…`: tải (`.tt-tai`) · rỗng (`.tt-rong`, 0 hàng) · lỗi `FLS-CAUHINH-CHUA-KHAI` (0 bảng) · có số (1 hàng). Lỗi 409 là cửa giả (`_TRA.no`) vì kho chỉ-THÊM ⛔ làm rỗng được |
| AC-4 | — | `--duong-nen` ĐẠT; `test_khong_ma_mau_go_tay` + `test_phuc_vu` (cổng `kiem_bang_tep`) xanh |
| AC-5 | — | `--duong-nen`: "chạy 3303 (mong ≥3303)" · "674 (mong ≥674)"; bài ghim đòi đúng 3303/674 |

Chứng minh ĐỎ: phá `CHAN`+`LAC` trong `man_f08.js` ⇒ AC1, AC2-thieu ĐỎ (`2 failed, 2 passed`); trả nguyên.

## Kho thật
- `KHONG_CHAM`. Kho TEST (5436) nạp lại ảnh `ix_fx.json` đầy đủ sau mỗi bài (fixture trả nguyên).

## Cách chạy để xem
- `python -m pytest tests/web/test_isp_f08_fx.py` · máy chủ thử `chỉ đọc`, tab ⑥ *Cấu hình · F08*.

## Dev tự thấy còn yếu
- Nhãn `TRÙNG` chưa có đột biến riêng (chỉ AC-2-trung đo); lỗi 409 thật chưa đo qua HTTP.
- Sàn Q8 nền cũ đã hở 3 (3299 thu thập vs ghim 3296 trước F4) — đã nâng theo số thu thập.
- Chưa đo pixel 390 px cho bảng 7 cột (chưa có AC).

## Vòng sửa sau R1 (KQ-162)
`KQ-162` = `ĐẠT` · 0 CHẶN · 1 NÊN SỬA *(`F4-R1-01`, tràn ngang 390 px)* · 3 GHI NHẬN *(`F4-R1-02…04` ⇒ backlog, ⛔ làm ở vòng này)*. Chỉ sửa `F4-R1-01`.

| | |
|---|---|
| **Sửa** | `fls/web/tep/man_f08.js`: bọc `<table>` trong `div.ngang` *(`hinh.css:504` `overflow-x:auto;max-width:100%`, có sẵn — ⛔ token mới)* ⇒ bảng cuộn TRONG khung |
| **Bài** | `tests/web/test_isp_f08_fx.py::test_F4_R1_01_bang_IXFX_khong_tran_ngang_o_390px` — Chromium thật, 390 px, bấm tab ⑥ |
| **Đo 390 px** *(nhãn: `documentElement` · hàng `[data-thang]`)* | trước: `scrollWidth 475 > clientWidth 390` · sau: `390 = 390`; `37` hàng *(mẫu số ≠ 0)*; bảng `473,6` px > khung `388` px ⇒ khung cuộn thật, `overflow-x:auto` |
| **ĐỎ trước** | bài chạy trên mã cũ ⇒ `1 failed` *(`sw=475`, khung `overflow-x: visible`)*; sau sửa ⇒ `5 passed` cả tệp F08 |
| **Sàn Q8** | toàn bộ `3303 → 3304` · `tests/web` `674 → 675` *(= số THU THẬP `--collect-only`: `3304` · `675`)*; `tools/dung_moi_truong_isp.sh` + bài ghim `test_dung_moi_truong_isp.py` cùng commit |
| **Cổng** | xem dòng cổng ở tin nhắn cuối của phiên: `--duong-nen --cong 5436` một lần · `lint-imports` |
