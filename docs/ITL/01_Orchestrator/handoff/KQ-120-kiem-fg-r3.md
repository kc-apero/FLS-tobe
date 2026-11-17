# KQ-120 — biên bản kiểm `BG-117` · R3 *(xác nhận cuối trước gộp)* của `FG`

| | |
|---|---|
| **Thuộc** | `BG-117` *(mục "Vòng sửa sau R2")* · `WO-116` · ISP Step 9 · FG |
| **Kiểm bởi** | `fls-test` · 2026-11-17 · R3 · phiên cloud riêng · cụm PG riêng **5436** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA mở** · 2 GHI NHẬN mới *(`FG-R3-01`, `FG-R3-02`)* |
| **Đối tượng** | `isp/FG` @ `a5e876e` · phạm vi R3 = `git diff c037297 isp/FG` *(2 tệp: `tests/web/test_isp_f03_hd.py` +30 −2 · `BG-117` +46)* |

## Cổng chạy lại *(Test tự chạy)*
| Lệnh | Mong | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/web/test_isp_f03_hd.py` | `3 passed` | `3 passed in 3.43s` | ✅ |
| `pytest tests/web` | 3 bài đỏ CÓ SẴN | `3 failed, 664 passed` *(3 đỏ = `test_wo022_…AC5` · `test_wo022_v2…AC11` · `test_wo042…AC11`: sổ thật 0 giá trị tiền — kho rỗng)* | ✅ |
| `--duong-nen --cong 5436` *(script nhánh · GOC `isp-fg`)* | `KẾT: ĐẠT` | `KẾT: ĐẠT` · toàn bộ `26 = 26 (thêm 0 · bớt 0)`, chạy 2603 · web `3 = 3`, chạy 667, skipped 0 | ✅ |
| `lint-imports` | 11 kept | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | K1–K6 OK | K1–K6 `OK` *(190 file · 1963 bảng · 737 ô ngày · 104 mã QĐ)* | ✅ |
| `git diff c037297 isp/FG -- fls` | 0 dòng | **0 dòng** | ✅ |
| Dựng môi trường (S0) | `KẾT: ĐẠT` | `KẾT: ĐẠT` · sha `isp/FG` = `a5e876e` | ✅ |

## Bảng AC *(ISP Step 9 mục 8)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| FG-F1 | `FINAL` ĐẠT · `HD1_THANG` KHÔNG ĐẠT · `5/23` · số 'chưa đo được' khớp tuyến | `test_FG_F1` xanh qua máy thật + `tep_do` thật; **mới:** `ly_do` *(≥ 50 ký tự — mẫu số ⛔ rỗng, Đ3)* ⊂ thẻ HD1 · `"%d đạt"`, `"%d không đạt"`, `"%d ⛔ chưa đo được"` lấy từ `GET /gates` *(⛔ hằng gõ tay)* ⊂ dòng tóm | ĐẠT |
| FG-F2 | `tep_do` vắng ⇒ hai thẻ `.gate.unk` | xanh; N14 *(`null` ⇒ `✓ ĐẠT`)* ⇒ F2 ĐỎ | ĐẠT |
| FG-F3 | lý do 23 kỳ ở 390 px ⛔ tràn | Chromium thật, 0 skip; **mới:** `ly_do` ⊂ thẻ HD1 trước phép đo tràn; N9/N11/N19 ⇒ F3 ĐỎ | ĐẠT |
| FG-F4 | `tests/web` xanh | 664 xanh + 3 đỏ CÓ SẴN = đường nền `3 = 3` | ĐẠT |
| Điều kiện PUSH | R1·R2·R3, chặn = 0 | R1 `KQ-118` · R2 `KQ-119` · R3 này — 0 CHẶN, 0 NÊN SỬA mở | ĐẠT |

## Vòng sửa `FG-R2-01` / `FG-R2-02`
| Phát hiện | Việc đòi | R3 đo | Kết |
|---|---|---|---|
| `FG-R2-01` *(NÊN SỬA)* | `ly_do` tuyến trả ⊂ thẻ HD1, so CHÍNH chuỗi tuyến | N9 *(bỏ khối `ly_do`)* ⇒ F1 + F3 **ĐỎ** · N11 *(`slice(0,40)`)* ⇒ F1 + F3 **ĐỎ** · N19 *(đảo thứ tự kỳ)* ⇒ **ĐỎ**; trả nguyên ⇒ `3 passed`. Khẳng định lấy `ly_do` từ `_gates(...)`, ⛔ hằng | **ĐÃ SỬA** |
| `FG-R2-02` | canh cả ba số dòng tóm | N10 *(`đạt` in `khong_dat`)* ⇒ F1 **ĐỎ** · N17 *(`không đạt` in `dat`)* ⇒ **ĐỎ** · N16 *(`chua+1`)* ⇒ **ĐỎ**; trả nguyên ⇒ `3 passed` | **ĐÃ SỬA** *(ranh giới: `FG-R3-01`)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | Khớp spec Step 9: bài chỉ THÊM khẳng định so tuyến thật; `fls/` ⛔ đổi | `git diff c037297 isp/FG -- fls` = **0 dòng**; mẫu số Đ3 canh `len(ly_do) ≥ 50` và `chua_do_duoc > 0` *(⛔ `"" in txt`)*; Đ5: đột biến phá → cắn → trả |
| **Dữ liệu** | Tập đo ⛔ rỗng: tuyến trả `dat=1 · khong_dat=2 · chua_do_duoc=4` · `HD1_THANG` `5/23` · `ly_do` 431 ký tự. Kho `fls` rỗng *(`fls_itl` 0 dòng — môi trường dựng)* ⇒ ⛔ liên quan bài này, bài dựng từ `tep_do` tĩnh | `KẾT: ĐẠT` dựng; `HD1 do_voi_so_luong chạy 9845 / có 9967` |
| **Màn hình** | Thẻ `FINAL` ĐẠT · `HD1` KHÔNG ĐẠT mang `ly_do` đầy đủ · `tep_do` vắng ⇒ `.unk` ⛔ xanh · F3 ⛔ tràn ở 390 px *(thẻ — không phải cả trang: `FG-R1-02` CHẤP NHẬN, backlog UIUX)* | F1 + F2 + F3 xanh; Chromium thật, 0 skip |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `FG-R3-01` | `NHE` *(GHI NHẬN)* | `tests/web/test_isp_f03_hd.py:195-196` | Phép `in` là chuỗi con: `"1 đạt" ⊂ "11 đạt"`, `"2 không đạt" ⊂ "12 không đạt"`. N20/N21 *(`dat+10`, `khong_dat+10`)* ⇒ `3 passed` | `DEV` *(backlog; neo ranh giới chữ số)* |
| `FG-R3-02` | `NHE` *(GHI NHẬN)* | `fls/web/tep/man_f03.js:42` · bài FG | N15 *(`slice(0,-1)` — rớt thẻ cổng cuối)* ⇒ `3 passed` + 50 bài `tests/web` liên quan F03 xanh; cổng cuối ⛔ phải `FINAL`/`HD1_THANG` ⇒ ngoài phạm vi FG | `DEV` *(backlog; khẳng định số thẻ = số cổng)* |
| `FG-R1-02` | `NHE` | cả trang F03 tràn 390 px | CHẤP NHẬN *(quyết sẵn — backlog UIUX)* | — |
| `FG-R1-04` | `NHE` | sàn lúc gộp | CHẤP NHẬN *(quyết sẵn — sàn gộp 2526 · web 667)* | orchestrator |

Thang gộp: **0 CHẶN · 0 NÊN SỬA mở** ⇒ đủ điều kiện PUSH.

## Đột biến *(bản sao `git archive`, `/tmp/r3_fg/`; chi tiết `SO_PHAT_HIEN_ISP-3.1_FG.md` v0.3)*
**N9 · N10 · N11 *(ba cái R2 thấy sống)* — cả ba GIẾT.** Tự dựng thêm 8: N12 N13 N14 N16 N17 N18 N19 *(giết)* · N15 *(sống → `FG-R3-02`)* · N20 N21 *(sống → `FG-R3-01`)* · N22 *(thêm đuôi vào `ly_do` — sống đúng thiết kế, phép chứa)*. Mẫu ⛔ khớp đúng 1 lần mới chạy *(Đ5: khớp 0/≥2 ⇒ ĐỎ phép đo)*. Trả nguyên ⇒ `3 passed`.

## Bài thử mới
Không thêm `tests/nghiem_thu/` — R3 chỉ chạy lại và phá bài Dev; ⛔ sửa mã/bài hệ thống.

## Đ1–Đ5
- **Đ1** *(phủ định)*: câu *"N15 ⛔ bài nào bắt"* — đo: chạy `tests/web -k "f03 or gate or cong"` trên bản sao N15 = 50 bài xanh; grep `len(cards)` ⛔ tìm trong `tests/web/test_isp_f03_hd.py` ⇒ 0 hit *(`fls/` + `tools/` ⛔ liên quan — mã ⛔ đổi)*.
- **Đ3**: mọi khẳng định mới canh mẫu số trước *(`len(ly_do) ≥ 50`; `chua_do_duoc > 0`)*.
- **Đ4**: số `đạt`/`không đạt`/`chưa đo được` mỗi số một nhãn; `1`/`2`/`4` đếm **cổng**, ⛔ kỳ; `5/23` đếm **kỳ** của `HD1_THANG`.
- **Đ5**: đột biến phá → cắn → trả cho từng cái.
