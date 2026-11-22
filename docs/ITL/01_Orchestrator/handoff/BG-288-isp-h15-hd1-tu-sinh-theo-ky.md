# BG-288 — Bàn giao WO-287 · ISP Step 43 · H15 · HD1 tự sinh theo từng kỳ (AC10 · AC11)

| | |
|---|---|
| Phát bởi | fls-dev (phiên cloud, làn FE ↩ BE-HC) · 2026-11-22 · nhánh `isp/H15` (nền `291993f`) |
| Gửi | fls-test (R1 → `KQ-289` · R2 cuối → `KQ-290`) |
| Ghi kho THẬT | `KHONG` · ⛔ sửa ảnh DT12 / ảnh 2026-03 · ⛔ đọc sheet · ⛔ sửa lệch MID tự sinh · `fls/oracle/tu_soi.py` chỉ đọc |

## Kết luận
**26/26 kỳ có ảnh đo được tự sinh · 0 kỳ `chua_do`.** Khối HD (mã HD): **12.633/12.633** — mọi kỳ 100 %. Ô Final (7 khối) **88.339/88.431**: **92 ô lệch, cả 92 ở 8 kỳ** (2025-02·03·05·10·11·12, 2026-01·07; lớp `svc_start`/`svc_end`/`cdt1`/`id_payee`/`invoice`). Kỳ 2026-03 hồi quy: HD **584/584** · ô 4.088/4.088 · MID 4.020/4.088 *(đúng số trước bước)*.

## Đã làm
- `tools/do_voi_so_luong.py`: `do_tu_sinh_ky(d, ky)` (một ảnh) · `do_tu_sinh_theo_ky()` (lặp 26 kỳ theo manifest DT12 `dong_theo_ky_o_cot_A`) · `do_tu_sinh()` giữ nguyên nghĩa (lát cắt 2026-03). `voi_so_luong.json` → `tu_sinh` thêm `theo_ky` · `chua_do` · `tong` · `moc_so` (giữ khoá cũ `ky`·`o`·`hd`·`mid`).
- Kỳ ⛔ có ảnh / ảnh hỏng / ảnh khai sai kỳ ⇒ `chua_do` kèm lý do; manifest 0 kỳ hoặc hỏng ⇒ ĐỎ (Đ3).
- Mọi phép so ô qua `_chuan`. `MONG` khai SAU lần đo đầu: `tu_sinh_so_ky` · `tu_sinh_chua_do` · `tu_sinh_theo_ky[kỳ]` (ô · HD · MID · lệch Final theo khối · lệch MID theo khối · ô lỗi); kỳ đo được mà ⛔ khai ⇒ ĐỎ; sai một kỳ (tốt hơn hay xấu hơn) ⇒ ĐỎ đúng kỳ ấy.
- Bài: `tests/oracle/test_tu_sinh_theo_ky.py` **16 bài** (B1 26 kỳ · B2 hồi quy 2026-03 · B3 manifest/ảnh vắng/hỏng/sai kỳ · B4 `_chuan` · B5 Đ5 hai chiều · B6 tệp sinh khớp).

## Số đo theo kỳ *(mỗi cột nói nó đếm gì — Đ4)*
HD = ô khối `hd` · ô = ô Final 7 khối ⛔ có mã lỗi Sheets (`o_loi` = 0 ở cả 26 kỳ) · lệch Final = ô `Final_fls ≠ Final_sổ` · lệch MID = ô `MID_fls ≠ MID_sổ` *(lớp riêng, ⛔ sửa — ISP loại trừ; Final vẫn khớp đủ ở ô mà Classifying có trả lời)*.

| Kỳ | Dòng | HD khớp | Ô Final khớp | Lệch Final *(ô, theo khối)* | Lệch MID *(ô)* |
|---|---|---|---|---|---|
| 2024-10 | 6 | 6/6 | 42/42 | 0 (—) | 0 |
| 2024-11 | 3 | 3/3 | 21/21 | 0 (—) | 0 |
| 2024-12 | 6 | 6/6 | 42/42 | 0 (—) | 0 |
| 2025-01 | 748 | 748/748 | 5236/5236 | 0 (—) | 478 |
| 2025-02 | 283 | 283/283 | 1979/1981 | 2 (svc_end 1, svc_start 1) | 517 |
| 2025-03 | 297 | 297/297 | 2077/2079 | 2 (svc_end 1, svc_start 1) | 805 |
| 2025-04 | 332 | 332/332 | 2324/2324 | 0 (—) | 817 |
| 2025-05 | 408 | 408/408 | 2852/2856 | 4 (svc_end 2, svc_start 2) | 1245 |
| 2025-06 | 348 | 348/348 | 2436/2436 | 0 (—) | 480 |
| 2025-07 | 546 | 546/546 | 3822/3822 | 0 (—) | 281 |
| 2025-08 | 537 | 537/537 | 3759/3759 | 0 (—) | 271 |
| 2025-09 | 501 | 501/501 | 3507/3507 | 0 (—) | 151 |
| 2025-10 | 487 | 487/487 | 3401/3409 | 8 (svc_end 8) | 145 |
| 2025-11 | 477 | 477/477 | 3321/3339 | 18 (svc_end 18) | 131 |
| 2025-12 | 566 | 566/566 | 3943/3962 | 19 (svc_end 19) | 198 |
| 2026-01 | 471 | 471/471 | 3290/3297 | 7 (svc_end 7) | 113 |
| 2026-02 | 439 | 439/439 | 3073/3073 | 0 (—) | 53 |
| 2026-03 *(sổ CŨ)* | 584 | 584/584 | 4088/4088 | 0 (—) | 68 |
| 2026-04 | 600 | 600/600 | 4200/4200 | 0 (—) | 74 |
| 2026-05 | 537 | 537/537 | 3759/3759 | 0 (—) | 77 |
| 2026-06 | 613 | 613/613 | 4291/4291 | 0 (—) | 40 |
| 2026-07 | 686 | 686/686 | 4770/4802 | 32 (cdt1 7, id_payee 6, invoice 9, svc_end 5, svc_start 5) | 40 |
| 2026-08 | 724 | 724/724 | 5068/5068 | 0 (—) | 25 |
| 2026-09 | 737 | 737/737 | 5159/5159 | 0 (—) | 40 |
| 2026-10 | 1038 | 1038/1038 | 7266/7266 | 0 (—) | 17 |
| 2026-11 | 659 | 659/659 | 4613/4613 | 0 (—) | 3 |
| **Σ 26 kỳ** | 12.633 | 12633/12633 | 88339/88431 | 92 | 6069 |

- **Kỳ tệ nhất theo ô Final: 2026-07** — 32 ô lệch (`cdt1` 7 · `id_payee` 6 · `invoice` 9 · `svc_start` 5 · `svc_end` 5).
- Mốc sổ: **25 kỳ đọc 20/11** (sổ hiện tại) · **2026-03 mốc CŨ** (ảnh chụp sổ cũ — chủ chưa quyết đóng băng lại, `DT12-R1-05`). ⛔ Cột tổng Σ trộn hai mốc: chỉ để đối chiếu, mỗi kỳ ở trên mang mốc riêng; `voi_so_luong.json` ghi `moc_so` theo kỳ.
- `#N/A ()` 119 ô nằm ở cột `itl_id` (⛔ thuộc 7 khối) ⇒ ⛔ vào phép so ô; `o_loi` (ô khối bị bỏ vì mã lỗi) = 0.

## Chứng minh cổng cắn *(Đ5)*
- Đột biến số↔chuỗi: đổi `_chuan` thành bản so kiểu ⇒ 3 bài B4 ĐỎ; trả nguyên ⇒ xanh. Ô `svc_*_final` 2025-06 đổi int→chuỗi cùng giá trị ⇒ `do()` xanh; đổi giá trị (+7) ⇒ chỉ `tự sinh 2025-06` ĐỎ.
- Bài B5: sửa MONG 2025-02 về 0 lệch ⇒ ĐỎ; 2026-10 xấu đi ⇒ ĐỎ; thiếu kỳ / mất khoá / khai `chua_do` thừa ⇒ ĐỎ một dòng (⛔ traceback).

## Q8 · sàn
`MONG_PYTEST_TOAN_BO` **4481 → 4497** (+16 bài thu thập thật `4497`) cùng bài ghim `test_dung_moi_truong_isp.py` · `MONG_PYTEST_WEB` giữ 681.

## Cổng
`pytest` (bộ liên quan 1.486 xanh) · `kiem_tai_lieu` ĐẠT · `quet_pii_repo` 0 · `lint-imports` 11 kept 0 broken · `--duong-nen --cong 5435`: **ĐẠT** — toàn bộ: 12 đỏ + 14 lỗi + 2 xfail = 28 = đường nền *(thêm 0 · bớt 0)* · chạy 4.497 bài ≥ sàn 4.497 · skipped 0; `tests/web` ĐẠT *(681)*

## Cho R1 *(KQ-289)*
Soi: (1) B4 có thật bắt kiểu (tự đột biến `_chuan`); (2) 92 ô lệch Final là lớp có tên, ⛔ bị MONG che; (3) manifest là nguồn 26 kỳ — ⛔ liệt kê tay; (4) `tu_soi.py` ⛔ đổi (`git diff` rỗng).
