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

---

## Vòng sửa sau R1 (KQ-305)
R1 = 0 CHẶN · 3 NÊN SỬA (`I1-R1-01/02/03`) · người dùng đã duyệt. Nhánh làm việc đã gộp vào `isp/I1` (xung đột `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` ⇒ bản nhánh làm việc rồi đặt sàn = thu thập thật).

### Việc 1 · `I1-R1-01` — cổng `HD1_THANG` phán MỌI kỳ có ảnh (26)
- **ĐỎ trước:** `tests/api/test_isp_gates_hd1_i1r1.py` (11 bài; trên mã cũ **9 ĐỎ**, 2 xanh có chủ ý: tập `26 − 23 = 3` kỳ không rỗng · khoá CG1 "tệp không có `tu_sinh` ⇒ mẫu số cũ"). Phá chiều ngược: tệp mà `tu_sinh` chỉ phủ đúng 23 kỳ + mọi kỳ đạt ⇒ `dat=True`.
- **Sửa** `fls/repo/doc_bao_cao.py` `_cong_hd1` (+`_ky_tu_sinh`, `_cap_o`): đọc `tu_sinh.theo_ky` (26 kỳ). Kỳ của `dat_hd1` ⇒ phán như cũ (**đo được**, 23 kỳ). Kỳ chỉ có ở `tu_sinh` (`2026-09·10·11`) ⇒ **`khong_do_duoc` có tên vế "dòng ghép 1-1"** (`tu_sinh` chỉ có `o·hd·mid·lech_*`), ⛔ tính đạt, ⛔ bỏ khỏi mẫu số. Ô lệch ở kỳ ấy ⇒ ĐỎ nói tên. `dat` = `False` nếu có kỳ đỏ · `None` nếu không đỏ mà còn kỳ ⛔ đo được · `True` chỉ khi mọi kỳ có ảnh đo được và đạt. `tu_sinh` có mà hỏng / tự mâu thuẫn ⇒ `dat=None` kèm lý do (Đ5). Tệp ⛔ có `tu_sinh` ⇒ giữ nguyên hành vi cũ (khoá CG1).
- **Mẫu số in rõ (Đ4):** `da_do` = `5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh`. Ba tầng cùng chuỗi (ghim bởi `test_B1_…` ①②, `test_F1_vm_…` + `test_F1_chromium_…` ③ — node-vm và Chromium 390 px; `test_FG_F1`/`FG_F3` ở `tests/web`).
- **Hợp đồng `/gates`:** ⛔ thêm/đổi khoá (chỉ đổi chuỗi `da_do`/`ly_do`); `07_API_CONTRACT` dòng 860 thêm một câu (⬜ ⛔ đổi tuyến). Bài CG1 (`test_isp_gates_hd1.py`) xanh sau khi khai lại ghim mẫu số `MONG_HD1_DA_DO` và ca chiều ngược `B4` (khai `tu_sinh` chỉ 23 kỳ).

### Việc 2 · `I1-R1-02` — `ly_do` mang TÊN nhãn DT1b
- **ĐỎ trước** (cùng tệp bài): `test_I1_R1_02_ly_do_mang_TEN_nhan_va_so_dong_khi_co_nhan` dựng `dat_hd1.theo_nhan` có nhãn thật trong đầu vào (Đ3) · `…thieu_tep_nhan_ghi_chua_co_nhan_co_ten`.
- **Sửa** `_nhan_dt1b`: có nhãn ⇒ `nhãn DT1b: TONG_HOP_A 23 dòng (đã ký) · KHOA_LECH_B 99 dòng (chưa ký)`; mỗi kỳ đỏ kèm `(N có nhãn)` khi `co_nhan>0`. ⛔ nhãn ⇒ `chưa có nhãn DT1b (tệp nhãn docs/ITL/_tools/phan_loai_ly_do.json VẮNG)` — có tên tệp. Mẫu `kỳ: số` vẫn bóc đúng 18 kỳ đỏ (bài kiểm).
- Bài tích hợp `test_AC5_…` dùng tệp nhãn tmp (3 nhãn `TONG_HOP_A/B/L`, chữ ký GIẢ) ⇒ tên nhãn có ở ② và ③ (vm + Chromium).

### Việc 3 · `I1-R1-03` — bảng AC10/AC11 theo AP §5.3.2
**AC10** = *dòng ghép 1-1* **và** *ô mapping Final 7 khối*, đạt khi **CẢ HAI 100 %** (cả chế độ tự sinh) · **AC11** = riêng *ô khối HD* (đọc MID sổ 9.930/9.930 · tự sinh). Mốc sổ ghi từng hàng (`tu_sinh.moc_so`). Ô Final/HD ở bảng = `tu_sinh` (chế độ **tự sinh**, ⛔ cùng mẫu số với `dat_hd1.o_100` của sổ ⇒ `2025-03` ô tự sinh `2077/2079` ⇒ AC10 ĐỎ dù cổng kỳ ĐẠT — hai mốc/chế độ, Đ4). Dòng 1-1 chỉ đo được ở 23 kỳ `dat_hd1` (ảnh sổ 26/08); 3 kỳ mới ghi "⛔ đo được vế dòng". Mốc cột dòng: ảnh **26/08**; mốc cột ô/HD: cột "mốc sổ".

| kỳ | mốc sổ | AC10a · dòng ghép 1-1 (`dat_hd1`, dòng thiếu) | AC10b · ô mapping Final 7 khối khớp/tổng | AC10 (cả hai 100 %) | AC11 · ô khối HD khớp/tổng |
|---|---|---|---|---|---|
| 2024-10 | 20/11 | 100 % (0 thiếu) | 42/42 | ĐẠT | 6/6 |
| 2024-11 | 20/11 | 100 % (0 thiếu) | 21/21 | ĐẠT | 3/3 |
| 2024-12 | 20/11 | 100 % (0 thiếu) | 42/42 | ĐẠT | 6/6 |
| 2025-01 | 20/11 | ĐỎ (1 thiếu) | 5236/5236 | ĐỎ | 748/748 |
| 2025-02 | 20/11 | ĐỎ (2 thiếu) | 1979/1981 | ĐỎ | 283/283 |
| 2025-03 | 20/11 | 100 % (0 thiếu) | 2077/2079 | ĐỎ | 297/297 |
| 2025-04 | 20/11 | 100 % (0 thiếu) | 2324/2324 | ĐẠT | 332/332 |
| 2025-05 | 20/11 | ĐỎ (1 thiếu) | 2852/2856 | ĐỎ | 408/408 |
| 2025-06 | 20/11 | ĐỎ (3 thiếu) | 2436/2436 | ĐỎ | 348/348 |
| 2025-07 | 20/11 | ĐỎ (4 thiếu) | 3822/3822 | ĐỎ | 546/546 |
| 2025-08 | 20/11 | ĐỎ (4 thiếu) | 3759/3759 | ĐỎ | 537/537 |
| 2025-09 | 20/11 | ĐỎ (4 thiếu) | 3507/3507 | ĐỎ | 501/501 |
| 2025-10 | 20/11 | ĐỎ (9 thiếu) | 3401/3409 | ĐỎ | 487/487 |
| 2025-11 | 20/11 | ĐỎ (14 thiếu) | 3321/3339 | ĐỎ | 477/477 |
| 2025-12 | 20/11 | ĐỎ (5 thiếu) | 3943/3962 | ĐỎ | 566/566 |
| 2026-01 | 20/11 | ĐỎ (4 thiếu) | 3290/3297 | ĐỎ | 471/471 |
| 2026-02 | 20/11 | ĐỎ (5 thiếu) | 3073/3073 | ĐỎ | 439/439 |
| 2026-03 | mốc CŨ | ĐỎ (5 thiếu) | 4088/4088 | ĐỎ | 584/584 |
| 2026-04 | 20/11 | ĐỎ (8 thiếu) | 4200/4200 | ĐỎ | 600/600 |
| 2026-05 | 20/11 | ĐỎ (5 thiếu) | 3759/3759 | ĐỎ | 537/537 |
| 2026-06 | 20/11 | ĐỎ (12 thiếu) | 4291/4291 | ĐỎ | 613/613 |
| 2026-07 | 20/11 | ĐỎ (23 thiếu) | 4770/4802 | ĐỎ | 686/686 |
| 2026-08 | 20/11 | ĐỎ (13 thiếu) | 5068/5068 | ĐỎ | 724/724 |
| 2026-09 | 20/11 | ⛔ đo được vế dòng (`tu_sinh` ⛔ có dòng ghép 1-1) | 5159/5159 | ⛔ đo được (ô 100 %) | 737/737 |
| 2026-10 | 20/11 | ⛔ đo được vế dòng (`tu_sinh` ⛔ có dòng ghép 1-1) | 7266/7266 | ⛔ đo được (ô 100 %) | 1038/1038 |
| 2026-11 | 20/11 | ⛔ đo được vế dòng (`tu_sinh` ⛔ có dòng ghép 1-1) | 4613/4613 | ⛔ đo được (ô 100 %) | 659/659 |
| **Σ 26** | | dòng 100 %: **5/23** kỳ đo được | 88339/88431 | **4/23** kỳ đo được · 3 ⛔ đo được vế dòng | 12633/12633 · **26/26** kỳ |

### Cổng sau vòng sửa
| Cổng | Kết quả |
|---|---|
| `--duong-nen --cong 5437` (một mình, chạy 1 lần) | **ĐẠT**: toàn bộ 12 failed · 4.615 passed · 2 xfailed · 14 errors = tập đỏ 28 = 28 (thêm 0 · bớt 0), chạy **4.643** ≥ mong 4.643 · `tests/web` 3 failed · 687 passed = 3 = 3, chạy 690 ≥ 690 |
| bài mới `test_isp_gates_hd1_i1r1.py` | 11/11 xanh (9 ĐỎ trên mã cũ) |
| GHI NHẬN (backlog) | `I1-R1-04..07` giữ nguyên sổ; ⛔ phát hiện mới |
