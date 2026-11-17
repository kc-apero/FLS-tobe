# KQ-118 — biên bản kiểm `BG-117` *(ISP 3.1.2 · Step 9 · FG · R1)*

| | |
|---|---|
| **Thuộc** | `BG-117` · `WO-116` *(dải: WO-116 · BG-117 · KQ-118 R1 · KQ-119 R2 · KQ-120 R3)* |
| **Kiểm bởi** | `fls-test` — **R1** *(phiên cloud CON độc lập)* · 2026-11-17 |
| **Đối tượng** | nhánh `isp/FG` @ `243a1ba` *(mã `4933038` + `BG-117`)* · nền `4dfb7bd` *(CG1 sau `KQ-103`)* · cụm PG riêng **5446** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN** *(1 NÊN SỬA → Dev · 3 GHI NHẬN; chi tiết + luật phòng: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_FG.md`)* |

> **Điều kiện PUSH** *(ISP mục 8)*: đủ R1 · R2 · R3, chặn = 0. R1 `ĐẠT · 0 chặn`; còn R2 *(KQ-119)* · R3 *(KQ-120)* ⇒ **chưa đủ PUSH**.
> Mọi số R1 tự chạy lại, `PG_DSN=…:5446/fls PG_DSN_TEST=…:5446/fls_test PYTHONUTF8=1`. Đột biến trên **bản sao** `git archive isp/FG` ở `/tmp/r1_fg/` *(⛔ chạm worktree)*.

## Cổng chạy lại
| Lệnh | `BG-117` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/web/test_isp_f03_hd.py` | `3 passed` | `3 passed` · `-rs` 0 skip | ✅ |
| `--duong-nen --cong 5446` *(script NHÁNH, GOC = `isp-fg`)* | `KẾT: ĐẠT` · toàn bộ `26 = 26 · 2603 (≥ 2496)` · web `3 = 3 · 667 (≥ 667)` · skipped 0 | `KẾT: ĐẠT` · `12 failed, 2575 passed, 2 xfailed, 14 errors` · `26 = 26 (thêm 0 · bớt 0) · chạy 2603 · skipped 0 · deselected 0`; `tests/web` `3 failed, 664 passed` · `3 = 3 · chạy 667 · skipped 0` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | *(BG ⛔ ghi)* | K1–K6 `OK` *(187 file · 1.940 bảng · 734 ô ngày · 104 mã QĐ)* | ✅ |
| `git diff 4dfb7bd HEAD -- fls` | rỗng *(`man_f03.js` ⛔ đổi)* | **0 dòng** | ✅ |
| Dựng môi trường *(script S0)* | — | `KẾT: ĐẠT` · di trú 26/26 · pg_verify 25 bảng 0 lệch · `lint-imports 11 kept` · kho `fls_itl = 0` | ✅ |
| `kiem_so_song.py` · `soi_bang_tuyen.py` · `pg_migrate` | *(BG ⛔ chạy mục ISP 6)* | **⛔ chạy** — bước ⛔ chạm `fls/` *(diff 0)*, ⛔ tuyến, ⛔ schema; `pg_migrate` đã chạy trong dựng môi trường | — |

## Bảng AC *(mỗi dòng mục 8 + test ID mục 6)*
| AC *(test)* | Mong | R1 đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** `FG-F1` | `FINAL` ĐẠT; `HD1_THANG` KHÔNG ĐẠT '5/23'; số 'chưa đo được' khớp tuyến | Bài chạy **máy thật** + `tep_do` thật ⇒ `GET /gates` ⇒ nuôi envelope ấy vào `man_f03.js`. **(a)** số 'chưa đo được' so `"%d ⛔ chưa đo được" % d["chua_do_duoc"]` — `d` là chuỗi tuyến trả, **⛔ hằng gõ cứng**; mẫu số khác rỗng *(`chua_do_duoc > 0`, `dat ≥ 1`, `khong_dat ≥ 1` — Đ3)*; `_the()` buộc **đúng 1** thẻ khớp *(Đ5)*. Đột biến M1·M5·M6·M7·M8 đều giết F1 | **ĐẠT** |
| **AC-2** `FG-F2` | tệp đo vắng ⇒ hai thẻ `.gate.unk` 'KHÔNG ĐO ĐƯỢC', ⛔ xanh | **(b)** tệp trỏ đường ⛔ tồn tại *(assert `not exists`)* ⇒ tuyến `dat=None` cả hai; màn: `unk` **trong** lớp, `pass` **⛔ trong** lớp, `KHÔNG ĐO ĐƯỢC` trong chữ — **cả hai** thẻ. M2 *(thẻ `pass unk`)* + M7 giết F2 | **ĐẠT** |
| **AC-3** `FG-F3` | lý do 23 kỳ ở 390 px ⛔ tràn ngang | Chromium **thật** 390 px: thẻ HD1 mang `5/23` *(⛔ rỗng, Đ3)*, `scrollWidth 318 = clientWidth 318`; 9/9 thẻ nằm `[35, 355]` trong 390. M3 *(nowrap)* + M9 *(NBSP, `sw 566 > cw 318`)* giết F3. **Sót một hướng:** M4 `min-width:520px` ⇒ thẻ rộng hơn màn mà `3 passed` ⇒ **`FG-R1-01`**. **(d)** cả trang tràn `692 > 390` do `TABLE` `right = 429` *(bảng mẫu số)*, ⛔ do thẻ ⇒ **ngoài** AC-3 *(AC nói về lý do)* ⇒ `FG-R1-02` | **ĐẠT** *(kèm `FG-R1-01`)* |
| **AC-4** `FG-F4` | `tests/web` sẵn có xanh | `--duong-nen` web: `3 = 3 node id (thêm 0 · bớt 0)` · 667 bài · skipped 0 *(ba đỏ = đường nền)* | **ĐẠT** |
| **AC-5** Q8 | nâng sàn cùng commit theo `--collect-only` | `2493 → 2496` · `664 → 667` ở `4933038`; bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho` đổi cùng chỗ; `chạy 2603 ≥ 2496` | **ĐẠT** *(→ `FG-R1-04` về mức cộng khi gộp)* |
| mục 8 · "`man_f03.js` sửa tối thiểu **nếu** vỡ" | — | đo: thẻ ⛔ tràn ⇒ **⛔ sửa** là đúng ISP §3 *(`fls/` diff 0)* | **ĐẠT** |
| mục 8 · "3 vòng review · PUSH" | — | **chưa** — chờ R2 · R3 | *(ngoài R1)* |

## Q-FG-1 = A *(orchestrator đã quyết — R1 chỉ kiểm hai điều được dặn)*
1. **Thiếu Chromium ⇒ gì:** bản sao đổi glob Chromium ⇒ `2 passed, 1 skipped`; dòng tổng kết mẫu `… 664 passed, 1 skipped` qua đúng `awk` của script ⇒ `chạy 667 · skip 1` ⇒ `n_skip ≠ 0` ⇒ `do_` **ĐỎ** *(Đ5 giữ — đo từng mắt xích, ⛔ chạy trọn vòng trên môi trường thiếu Chromium)*.
2. **F3 có ĐỎ khi thẻ tràn:** có *(M3, M9)*; hướng thẻ rộng hơn màn sót *(`FG-R1-01`)*.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | **ĐẠT** | Ba mức `pass/fail/unk` chỉ sống ở `_muc`; M1/M2/M8 bẻ từng nhánh ⇒ bài đỏ đúng nhánh. `ĐÚNG MỘT thẻ` + mẫu số khác rỗng ⇒ Đ3/Đ5 giữ |
| **Dữ liệu** | **ĐẠT** | Bài chỉ đọc kho `fls_test` rỗng *(`noi_chi_doc`)*; số HD1 là của **tệp đo tĩnh** *(ảnh 2026-08-26)*, ⛔ kho sống; `FLS_CHO_GHI_THAT` ⛔ đặt; `fls_itl = 0` |
| **Màn hình** | **ĐẠT có giới hạn** | Thẻ HD1 ⛔ tràn ở 390 px *(318/318)*; trang tràn `692` do bảng — ghi nhận `FG-R1-02`. Phím · token màu: hồi quy web `3 = 3` |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `FG-R1-01` | **NÊN SỬA** | `tests/web/test_isp_f03_hd.py:252,280` | M4 `.gate{min-width:520px}` ⇒ `3 passed`; thẻ HD1 `cw=518` > 390. Thêm `getBoundingClientRect().right ≤ innerWidth` | **DEV** |
| `FG-R1-02` | GHI NHẬN | F03 vỏ/bảng ở 390 px | `documentElement.scrollWidth 692 > 390`; `TABLE right=429`; thẻ `[35,355]` | orchestrator/BA |
| `FG-R1-03` | GHI NHẬN | `test_isp_f03_hd.py:210-233` | Đường Chromium gõ cứng Linux, ⛔ biến ghi đè; thiếu ⇒ skip ⇒ `--duong-nen` ĐỎ *(đúng)* | DEV *(tuỳ)* |
| `FG-R1-04` | GHI NHẬN | `tools/dung_moi_truong_isp.sh:396-402` · `CG1-R1-01` | Script nhánh vẫn yếu hơn S0; lúc gộp cộng **+33 +3** lên S0 `2490` ⇒ `2526` | orchestrator |

## Bài thử mới `tests/nghiem_thu/`
*(không)* — phủ của `test_isp_f03_hd.py` đủ cho AC; 8/9 đột biến giết; lỗ M4 giao Dev vá ở chính bài FG-F3 *(R1 ⛔ sửa bài của Dev)*.

## Môi trường R1
`tools/dung_moi_truong_isp.sh --cong 5446` *(script S0 `c1cf29b`)* ⇒ `KẾT: ĐẠT`. Sha: `isp/S0` = `c1cf29b` · `isp/FG` = `243a1ba` *(khớp brief)*.
