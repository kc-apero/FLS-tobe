# BG-304 — Bàn giao WO-303 · ISP Step 45 · I1 · Tích hợp HD1 xuyên suốt

| | |
|---|---|
| **Nhánh / commit** | `isp/I1` · bài ① `313bcec` (nền `800c050`, đã có H15 `a7e3741` + `WO-303`) |
| **Dải phiếu** | R1 `KQ-305` · R2 cuối `KQ-306` · số trống kế tiếp **307** |
| **Chạm** | `tests/tich_hop/test_hd1_xuyen_suot.py` (mới, 11 bài) · sàn `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py`. ⛔ sửa engine H15/CG1/FG · ⛔ chữ ký thật (O8) · ⛔ kho sống |

## Kết luận
Bài tích hợp xanh `11/11`; `--duong-nen --cong 5437` **ĐẠT** (một lần). **Nhưng "x/26" của WO ⛔ đúng ở tầng cổng** — xem phát hiện `I1-P1`.

## Ba tầng — đo thật (mốc sổ: 25 kỳ đọc 20/11 · 2026-03 mốc cũ)
Tầng ① `do_voi_so_luong.do()` chạy sống → tệp tạm · ② `GET /gates` (máy chủ thử, tệp tạm ấy) · ③ F03 (node-vm `man_f03.js` thật **và** Chromium headless thật, 390 px).

| | số kỳ đạt (nhãn: kỳ HD1 của `dat_hd1`) | kỳ đỏ |
|---|---|---|
| ① `dat_hd1` | **5/23** | 18 kỳ, Σ 122 dòng thiếu |
| ② `/gates` `HD1_THANG` | **5/23** (`dat=false`) | cùng 18 kỳ (bóc từ `ly_do`) |
| ③ F03 thẻ HD1 | **5/23** `KHÔNG ĐẠT`, `ly_do` đầy đủ | cùng 18 kỳ |
| Nguồn thứ hai (Đ2) | tệp `voi_so_luong.json` đã commit = lần đo sống | |

| AC | Kết quả |
|---|---|
| AC-1 · I1-B1 | ba tầng cùng 5/23 + cùng danh sách đỏ; `ly_do` mang ngày ảnh `2026-08-26` + "kỳ đỏ 18/23". `tu_sinh` ⛔ tới cổng (khai ở `I1-P1`) |
| AC-2 · I1-B2 | tệp vắng ⇒ `FINAL` · `HD1_THANG` `dat=null` (⛔ false/true), HTTP 200 đúng hợp đồng CG1 (`07_API_CONTRACT` dòng 860: ba trạng thái `true/false/null`, ⛔ 503); `chua_do_duoc` vắng − thật = **+2** (đếm cổng `dat=null`, gồm HD2 — ⛔ gõ tay "6") |
| AC-3 · I1-F1 | thẻ F03 ghi **x/23** đúng như cổng (vm + Chromium), ⛔ x/26 |
| AC-4 · I1-F2 | tệp vắng ⇒ hai thẻ `.unk` "KHÔNG ĐO ĐƯỢC" (vm + Chromium; ⛔ `pass`, ⛔ trống) |
| AC-5 | chữ ký GIẢ `TONG_HOP_TEST` (nhãn `TONG_HOP_A`+`TONG_HOP_L`, tệp tạm, ⛔ thật) ⇒ `2026-07` xanh ở ① ② ③ (**6/23**, 17 kỳ đỏ); gỡ ⇒ **5/23**, `2026-07` đỏ lại. Sổ lý do thật còn `chu_ky == []` |
| Chứng minh ĐỎ | phá `da_do` của `_cong_hd1` (+3 kỳ) ⇒ 4 bài ĐỎ; đổi chữ "KHÔNG ĐO ĐƯỢC" ở `man_f03.js` ⇒ 2 bài F2 ĐỎ; cả hai đã TRẢ NGUYÊN (`git status` sạch) |

## Phát hiện (⛔ sửa ngầm — báo)
- **`I1-P1` (lệch giữa hai khối).** Cổng `HD1_THANG` đọc `dat_hd1` ⇒ mẫu số **23 kỳ** (ảnh sổ 26/08). H15 `tu_sinh` = **26 kỳ** (manifest DT12) là khối khác mà CG1 ⛔ đọc; ba kỳ `2026-09 · 2026-10 · 2026-11` chỉ có ở `tu_sinh`. Bài ghim hiện trạng (`test_P1_…`): khi CG1 đọc `tu_sinh`, bài ĐỎ ⇒ khai lại `MONG_SO_KY_CONG`. **Câu cho orchestrator/BA:** cổng HD1 có phải phán 26 kỳ (cần CG1 mới) hay chỉ 23?
- **`I1-P2`.** `ly_do` chỉ mang *kỳ: số dòng thiếu*, ⛔ mang TÊN nhãn DT1b (tệp nhãn `phan_loai_ly_do.json` vắng — `tep_nhan.co=false`). AC-1 "nhãn DT1b trong `ly_do`" ⇒ chưa thoả; bài `test_P2_…` ghim ⛔ có.
- **`I1-P3` (môi trường).** `khop_owner.py --kiem` ĐỎ — **đỏ cả trên nền `800c050` không có commit này** (`fls_itl` rỗng ở cụm cloud ⇒ C5/C5b "KHÔNG ĐO ĐƯỢC"); `tools/kiem_so_song.py` lỗi `FileNotFoundError .venv/Scripts/lint-imports.exe` (đường Windows). Cả hai ⛔ do I1; ⛔ sửa.

## Bảng AC10/AC11 theo kỳ (26 hàng)
Nguồn: `voi_so_luong.json › tu_sinh` (H15). Nhãn cột: **AC10** = ô khối HD khớp/tổng; **AC11** = ô Final 7 khối khớp/tổng *(cách gán nhãn AC10/AC11 vào hai cột là của tôi — WO ⛔ định nghĩa; mời R1 đối chiếu)*. Cột cuối = phán kỳ của cổng (`dat_hd1`); 3 kỳ ngoài cổng.

| kỳ | mốc sổ | AC10 · HD khớp/tổng ô (khối HD) | AC11 · ô Final khớp/tổng (7 khối) | lệch Final (khối) | HD1_THANG kỳ (cổng, dòng thiếu) |
|---|---|---|---|---|---|
| 2024-10 | 20/11 | 6/6 | 42/42 | — | ĐẠT |
| 2024-11 | 20/11 | 3/3 | 21/21 | — | ĐẠT |
| 2024-12 | 20/11 | 6/6 | 42/42 | — | ĐẠT |
| 2025-01 | 20/11 | 748/748 | 5236/5236 | — | ĐỎ (1 thiếu) |
| 2025-02 | 20/11 | 283/283 | 1979/1981 | {'svc_start': 1, 'svc_end': 1} | ĐỎ (2 thiếu) |
| 2025-03 | 20/11 | 297/297 | 2077/2079 | {'svc_start': 1, 'svc_end': 1} | ĐẠT |
| 2025-04 | 20/11 | 332/332 | 2324/2324 | — | ĐẠT |
| 2025-05 | 20/11 | 408/408 | 2852/2856 | {'svc_start': 2, 'svc_end': 2} | ĐỎ (1 thiếu) |
| 2025-06 | 20/11 | 348/348 | 2436/2436 | — | ĐỎ (3 thiếu) |
| 2025-07 | 20/11 | 546/546 | 3822/3822 | — | ĐỎ (4 thiếu) |
| 2025-08 | 20/11 | 537/537 | 3759/3759 | — | ĐỎ (4 thiếu) |
| 2025-09 | 20/11 | 501/501 | 3507/3507 | — | ĐỎ (4 thiếu) |
| 2025-10 | 20/11 | 487/487 | 3401/3409 | {'svc_end': 8} | ĐỎ (9 thiếu) |
| 2025-11 | 20/11 | 477/477 | 3321/3339 | {'svc_end': 18} | ĐỎ (14 thiếu) |
| 2025-12 | 20/11 | 566/566 | 3943/3962 | {'svc_end': 19} | ĐỎ (5 thiếu) |
| 2026-01 | 20/11 | 471/471 | 3290/3297 | {'svc_end': 7} | ĐỎ (4 thiếu) |
| 2026-02 | 20/11 | 439/439 | 3073/3073 | — | ĐỎ (5 thiếu) |
| 2026-03 | mốc CŨ | 584/584 | 4088/4088 | — | ĐỎ (5 thiếu) |
| 2026-04 | 20/11 | 600/600 | 4200/4200 | — | ĐỎ (8 thiếu) |
| 2026-05 | 20/11 | 537/537 | 3759/3759 | — | ĐỎ (5 thiếu) |
| 2026-06 | 20/11 | 613/613 | 4291/4291 | — | ĐỎ (12 thiếu) |
| 2026-07 | 20/11 | 686/686 | 4770/4802 | {'cdt1': 7, 'svc_start': 5, 'svc_end': 5, 'id_payee': 6, 'invoice': 9} | ĐỎ (23 thiếu) |
| 2026-08 | 20/11 | 724/724 | 5068/5068 | — | ĐỎ (13 thiếu) |
| 2026-09 | 20/11 | 737/737 | 5159/5159 | — | ngoài cổng (không có trong `dat_hd1`) |
| 2026-10 | 20/11 | 1038/1038 | 7266/7266 | — | ngoài cổng (không có trong `dat_hd1`) |
| 2026-11 | 20/11 | 659/659 | 4613/4613 | — | ngoài cổng (không có trong `dat_hd1`) |
| **Σ 26** | | 12633/12633 | 88339/88431 | | 5/23 kỳ đạt |

Lệch Final ở 8 kỳ, Σ **92** ô = 88.431 − 88.339 (khớp WO).

## Cổng `CLAUDE.md` — kết quả thật (cụm 5437)
| Cổng | Kết quả |
|---|---|
| `pytest` toàn bộ (qua `--duong-nen`) | 12 failed · 4.533 passed · 2 xfailed · 14 errors = tập đỏ **28 = 28** đường nền (thêm 0 · bớt 0); chạy 4.561 ≥ mong |
| `pytest tests/web` | 3 failed · 687 passed = **3 = 3** đường nền; chạy 690 ≥ 690 |
| `--duong-nen` | **KẾT: ĐẠT** (chạy lần 1 bị dừng vì hết giờ nền do tôi đặt 10 phút — ⛔ ĐỎ; chạy lại MỘT lần với 1 giờ ⇒ ĐẠT) |
| `lint-imports` | 11 kept · 0 broken |
| `kiem_tai_lieu.py` | ĐẠT (453 tệp · 2.880 bảng · 945 ô ngày · 104 mã QĐ) |
| `soi_bang_tuyen.py` | khớp SQL ở **48/48** tuyến |
| `kiem_thuyet_minh.py` | 35/35 nút |
| `pg_migrate` | ⛔ gì để áp · `pg_verify` khớp |
| `khop_owner.py --kiem` | ĐỎ — có sẵn ở nền (`I1-P3`) |
| `kiem_so_song.py` | lỗi đường Windows (`I1-P3`); `dong_bo_so_song.py` ⛔ chạy |

## Sàn (Q8)
`MONG_PYTEST_TOAN_BO` **4550 → 4561** (= 11 bài thu thập thật) cùng bài ghim, cùng commit `313bcec`. `MONG_PYTEST_WEB` **giữ 690** (bài mới ở `tests/tich_hop`, ⛔ `tests/web`).
