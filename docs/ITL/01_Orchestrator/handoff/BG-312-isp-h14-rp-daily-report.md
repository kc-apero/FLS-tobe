# BG-312 — bàn giao `WO-311` *(ISP 3.1.2 · Step 46 · H14 — RP.CF · RP.PL · Daily Report 2 · 3 theo khuôn, cổng WP-C5c)*

| | |
|---|---|
| **Thuộc** | `WO-311` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5434** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-313`, R2 cuối → `KQ-314`)* |
| **Commit** | `isp/H14` ⇒ `claude/bold-galileo-zukpaf-isp/H14` · ① mã + bài + tệp sinh lại · ② BG này |
| **Nền** | ngọn nhánh làm việc `4ae4824` *(có `WO-311`)* + gộp `…-isp/H13` `1db1b55` *(tăng tốc ③, H13 CHƯA gộp)* — gộp `a4c97ea` |
| **Kho thật** | `KHONG_CHAM`. Bài: kho `fls_test` *(schema tạm, giao dịch ROLLBACK)*; `--ghi`: kho `fls_test` nạp nền bằng `do_hd2_c5c.nap_nen_kho` *(IX.PER · IX.ALR 17 luật MM + ký BẬT 2025 `ix_alr_2025_bat.json` · IX.PL)* |

## Kết luận một dòng
**WP-C5c ĐẠT**: **64.618/72.390** ô đáp án khớp *(khớp THẬT **11.540/19.312** ô có số · **53.078** ô `0 = 0`)* + **7.772** lệch có chủ đích — **MỌI ô thừa kế lớp bằng truy ngược ô nguồn** · lệch FLS **0**. 605 · 615 **DỪNG** `chua_co_dau_vao` *(cần ảnh — §4)*. `/gates`: `HD2_WP_C5C` = `true`, cha `HD2_WP_C5` = `3/3 gói con đạt (WP-C5a · WP-C5b · WP-C5c)`.

## 1 · Khuôn — đo TRƯỚC khi viết engine *(Đ1: đo ở ảnh, ⛔ suy từ tên)*
Đo 22/11 trên ảnh đáp án *(CHỈ để hiểu khuôn — ⛔ đầu vào engine)*: mỗi ô báo cáo là **phép chiếu** của MỘT ô lưới thượng nguồn.

| Báo cáo · phần | Nguồn đo được | Bằng chứng *(ô ≠ 0 khớp ≤ 1e-9 / ô ≠ 0)* |
|---|---|---|
| 607 · 608 · 609 phần **ngày** | `PLA3 Daily PM + HR` *(H8 · 418)* | **304/304 · 269/269 · 306/306** |
| 607 · 609 **`CM Cumulative`** *(FS2)* | **ATL** *(606, H12 + H13)*; `SHQ` = `SHQ1 + SHQ2` | `SHQ·GI·2025` 0,7777 = 0,2393 + 0,5385 |
| 608 · nửa `[FS1][PLA3]` của 609 *(FS1)* | **⛔ nguồn nào của FLS** | `GROUP·GI·2025` FS1 **57,6738** ≠ ATL/PLA3 **57,2144** |
| 610 phần **ngày** · **luỹ kế** | `CFA1 Daily` *(409)* · `CFA1 Y/H/Q/M` *(410)* | **788/788 · 4.687/4.687** |
| 610 phần **`hr`** | `Report HR` *(số người)* — FLS ⛔ có engine | — |
| 605 Sign off *(VND, 8 thực thể × 24 tháng)* | ATL FLS × tỷ giá ⛔ tái lập | ~1,4 nghìn/8,1 nghìn ô ≠ 0 *(2024 trước ITL ⛔ có nguồn)* |
| 615 A-CCR `5. Daily Report` | `Cash Balance by LE` — ⛔ engine | — |
- Nhãn khối sổ **`HGO2`** = khối engine **`HGO6`** *(đo: 100 % ô ≠ 0 khớp)*.

## 2 · Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/bao_cao.py` *(mới)* | `daily_report(ky, fs, nguon, loai)` · `rp_pl` · `rp_cf` — khuôn `KHUON` + `KHUON_FS` *(FS là tham số DUY NHẤT đổi phần luỹ kế — D5 A)*; JSON ô THUẦN *(chuỗi `str(Decimal)`, khoá `phần\|khối\|mã\|cột`)*; nguồn vắng ⇒ `chua_co_dau_vao` + câu cần gì; `check_bao_cao` *(dùng lại `pla.check_atl`)* — chỉ ĐẾM + LIỆT KÊ |
| `tools/do_hd2_c5c.py` · `tools/do_hd2_c5c_mong.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C5c [--dsn] [--ghi]`; `mong` khai TRƯỚC theo TỪNG đáp án *(mẫu số + lớp + sha256 + CHECK + đáp án DỪNG)*; `nap_nen_kho` |
| `docs/ITL/_tools/hd2_cong.json` | khối `WP-C5c` sinh bằng `do_hd2.py --goi WP-C5c --dsn $PG_DSN_TEST --ghi` *(706 dòng THÊM, 0 xoá)* |
| `tests/bao_cao/test_bao_cao_daily_report.py` *(20)* · `tests/oracle/test_do_hd2_c5c.py` *(20)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | 13 → **14** cổng; `HD2_WP_C5C` `64618/72390 ô` + 7772; cha C5 `3/3`, `lech_co_chu_dich` 6.041 → **13.813** |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | gộp H13: xung đột sàn ⇒ bản nhánh làm việc rồi đặt = thu thập *(4.653 + 29 = 4.682)*; Q8 H14: **4.682 → 4.722** *(+40 = thu thập thật)*, cùng commit |

⛔ sửa engine H5–H13 / C13 *(chỉ GỌI)* · ⛔ ghi CCR/PDF · ⛔ chép ô chỉnh tay vào config.

## 3 · Đầu vào *(⛔ vòng tròn — AC-4)*
Lưới = đầu ra engine: `so_sanh_c3a(...).luoi` *(CFA1 Daily)* · `so_sanh_c3b(...).luoi` *(Y/H/Q/M)* · `so_sanh_c3d(...).luoi['pla3_pm_hr_daily']` · `so_sanh_c5a(...).o` đè dòng `PL*` bằng `so_sanh_c5b(...).pl` *(IX.ALR + IX.PL từ KHO)*. Hai lớp BỎ khỏi lưới *(⛔ để báo cáo in 0 ngầm)*: ô **KPI CFA1** *(`MA_KPI` — H5/H6 ⛔ tính, C3a/C3b loại `o_kpi`; đo: chính 2.948 ô luỹ kế 610 từng hiện "lệch FLS" trước khi bỏ)* · **672** ô `PL5` IX.PL ⛔ tính được. Bài `test_AC4_engine_khong_doc_dap_an`: xoá MỌI giá trị đáp án ⇒ 4 báo cáo y nguyên.

## 4 · Số đo WP-C5c *(Đ4 — mỗi số nói nó đếm gì)*
**Ô so** = ô đáp án là số × cột thuộc trục *(ngày của tháng kỳ · kỳ luỹ kế)* × phần có đầu vào × báo cáo engine có ô. `khop` = khớp THẬT *(atol 1e-12, rtol 0; lớn nhất 1,13e-14)* + `0 = 0`.

| Đáp án · FS | Ô so | Khớp *(thật / có số)* | Lệch theo lớp *(thừa kế)* | Lệch FLS | `chua_co_dau_vao` *(ngoài mẫu số)* | Engine vắng · ngoài trục | Chỉnh tay |
|---|---|---|---|---|---|---|---|
| **607** `[FS2]` 11/2025 | **25.649** | 21.770 *(4.365/8.244)* | **3.879** | 0 | 0 | 886 · 407 | **71** |
| **608** `[FS1]` 11/2025 | **8.510** | 8.510 *(270/270)* | 0 | 0 | `luy_ke:FS1` **8.421** | 460 · 402 | 0 |
| **609** FS3 12/2025 | **25.851** | 21.993 *(4.387/8.245)* | **3.858** | 0 | `luy_ke:FS1` **8.402** | 850 · 37 | **71** |
| **610** CF 11/2026 | **12.380** | 12.345 *(2.518/2.553)* | **35** `ite_alias` | 0 | `hr` **1.537** | 10.040 · 400 | 0 |
| **605** Sign off | — **DỪNG** | — | — | — | **13.706** ô số | — | — |
| **615** A-CCR | — **DỪNG** | — | — | — | **48.021** ô số | — | — |

- **Lớp thừa kế 607** *(609 cùng bộ, khác ở đuôi)*: `lech_D3` 2.133 · `chua_co_dau_vao` 862 · `chua_co_dau_vao+lech_D3` 590 · `loi_as_is` 173 *(609: 180)* · `lech_D3+lech_dap_an_nguon` 42 · `lech_dap_an_nguon` 21 *(609: 0)* · `chua_co_dau_vao+lech_D3+loi_as_is` 20 · `chua_co_dau_vao+loi_as_is` 16 · `lech_dap_an_nguon+loi_as_is` 14 *(609: 7)* · `lech_D3+loi_as_is` 8.
- **Truy ngược thật** *(⛔ quy tắc khối × năm — `H12-R1-01`)*: so 3 số cùng khoá — `e` engine · `a` đáp án báo cáo · `s` đáp án NGUỒN *(409/410/418/606)*. `e ≠ s` ⇒ lớp của CHÍNH ô nguồn ở cổng thượng nguồn *(C5a `lop_o` · C5b `lop` · C3a/C3b `lech_ite` · C3d)*; `e ≈ s`, `a ≠ s` ⇒ `lech_dap_an_nguon` *(hai ảnh AS-IS của cùng ô khác nhau — đóng băng khác ngày)*. Ô nguồn lệch mà thượng nguồn ⛔ gán lớp ⇒ `lech_FLS` *(bài `test_AC4_bo_lop_thuong_nguon_thi_DO`)*.
- **Engine vắng** *(có tên, ngoài mẫu số)*: mã sổ ngoài cây IX.HD `HDAP·HDC·HDCI·HDH·HDT` · `PL5_ix_pl_khong_tinh_duoc` *(149 · 121)* · `kpi_cfa1_engine_chua_tinh` 6.200 · `ngay_sau_ngay_doc_dau_vao` 3.240 *(610: 19→30/11/2026 sau ngày đọc GL CF 18/11)*.
- **Ô chỉnh tay ⛔ actor** *(71 ở 607, 71 ở 609 — luỹ kế `GROUP`, kỳ `2025M02` 19 · `2025`/`2025H1`/`2025Q1` 17 mỗi kỳ · `2025M01` 1)*: ô lệch có lớp chứa `loi_as_is` và `|e − a| = 0,5 ± 1e-9`; gốc ATL `AH12` `='…'!AH12-0.5`. Danh sách ở `hd2_cong.json` › `WP-C5c.lech_co_ten.chinh_tay_actor`. ⛔ config: bài đếm 0 chỗ `AH12` ở `fls/cau_hinh` + `tests/fixture/cau_hinh` *(mẫu số > 10 tệp)*.
- **CHECK của báo cáo** *(chỉ ĐẾM + LIỆT KÊ — câu "chặn đóng sổ" chờ chủ)*: đỏ **607 230 · 608 4 · 609 231 · 610 198**; `dat_co_so` = **0** mọi phần *(mọi "đạt" là 0 = 0 — trùng DT11/H13)*. Danh sách đỏ băm ở `mong` + in bởi `do_hd2.py --goi WP-C5c`.

## 5 · FS là tham số *(AC-2 · `H14-B2`)*
`KHUON_FS = {FS1: (luy_ke:FS1,), FS2: (luy_ke:FS2,), FS3: (luy_ke:FS1, luy_ke:FS2)}`; phần `ngay` + phép chiếu + JSON dùng chung. Bài: đổi FS ⇒ phần ngày y nguyên từng ô, FS3 = HỢP FS1 ∪ FS2 *(⛔ ô lạ)*; FS1 có nguồn `atl_fs1` ⇒ hết dừng, cùng engine.

## 6 · Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 · AC-2 · AC-3 *(đơn vị)* | gỡ `bao_cao.py` ⇒ `tests/bao_cao/test_bao_cao_daily_report.py` **lỗi thu thập** `ImportError` | 20 passed |
| AC-1 *(cổng)* | `mong = None` ⇒ ĐỎ "`mong` chưa khai"; 5 đột biến `mong` *(tong_o +1 · bỏ lớp · thêm lớp · đáp án dừng +1 · CHECK +1)* ⇒ ĐỎ; đáp án 610 rỗng ⇒ ĐỎ Đ3 | 20 passed |
| AC-3 | — | `dua_ban_ky` ×2 cùng đầu vào ⇒ `(1, False)` rồi `(1, True)` cùng checksum; FS khác cùng kỳ ⇒ phiên bản 2; nội dung đọc lại = bản đưa |
| AC-4 | — | đột biến 1 ô lưới: `pla3_daily SGO1·GI·03/11` ⇒ ĐỎ **đúng** `ngay\|SGO1\|GI\|2025-11-03` ở 607 + 608 *(609/610 ⛔)*; `atl BGO2·GI·2025M07` ⇒ đúng ô 607/609 *(608 FS1 ⛔)*; `cfa1_yhqm GROUP·GI·2026Q1` ⇒ đúng ô 610 |
| AC-5 | `KeyError: 'WP-C5c'` *(trước `--ghi`)*; bài gates **8 failed** *(14 ≠ 13 …)*; kho rỗng ⇒ ĐỎ có tên IX.PER | khối = lần đo; `/gates` 14 cổng, 0 null |
| AC-6 *(Q8)* | sàn 4.682 ≠ thu thập 4.722 | `MONG_PYTEST_TOAN_BO` = **4.722** |

## 7 · Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` *(một mình, MỘT lần, trên `5c17f13`)* | **`KẾT: ĐẠT`** — toàn bộ `12 failed · 4694 passed · 2 xfailed · 14 errors`: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4722** *(mong ≥ 4722)* · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy 690; di trú 27/27 · `pg_verify` 0 lệch · kho `fls` rỗng |
| `pytest tests/oracle tests/bao_cao tests/api tests/cau_hinh tests/du_lieu tests/canon tests/test_dung_moi_truong_isp.py` | 2.712 passed · 3 failed + 11 errors = tập đỏ sẵn *(`*_SO_THAT_*` ×3 · `test_mui_thu_luoi.py` ×11)* |
| Đột biến NGUỒN `bao_cao.py` *(sửa → chạy → trả nguyên, `git diff` rỗng)* | **3/3** bị cắn: `SHQ` chỉ `SHQ1` ⇒ 4 failed · `HGO2` ⛔ ánh xạ `HGO6` ⇒ 5 · trục ngày cứng 30 ngày ⇒ 3 |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (467 file, 2912 bang, 956 o ngay, 104 ma QD)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |

## Giả định *(chọn phương án hẹp nhất — R1 soát)*
1. **"FS3" = bản `5. Daily Report 3` (609)** — sổ ⛔ ghi nhãn "FS3"; đo: 609 = hợp nửa `[FS1][PLA3]` + `[FS2][PLA3]`. Chủ xác nhận nếu FS3 nghĩa khác.
2. **FS1 luỹ kế · 605 · 615 · `hr` DỪNG** *(tiền lệ DT7b)* — cần ảnh: `[FS1][PLA3]`/`[PLA5]` Y/H/Q/M nguồn *(sổ P&L Report)* + đường VND cho 605; số dư tiền theo LE × ngày cho 615; `Report HR` cho `hr`.
3. **Ô chỉnh tay** nhận diện bằng PHÉP ĐO `|e − a| = 0,5` trên ô `loi_as_is` — ⚠ có thể trùng ngẫu nhiên; 1 ô `2025M01` lọt *(đo: KPI hậu tố dọc cột)* — R1 soát.
4. **Ngày 19→30/11/2026** ở 610 = `engine_vang` *(sau ngày đọc đầu vào 18/11)* — ⛔ coi 0.
5. Bản đưa `dua_ban_ky` ở bài = MỘT báo cáo/kỳ; hai báo cáo cùng kỳ *(607 FS2 · 608 FS1, cùng 11/2025)* sinh hai phiên bản nối tiếp — hợp đồng bó nhiều báo cáo/kỳ là việc I2.

## Câu hỏi cho orchestrator / chủ sổ
1. **CHECK đỏ** *(607 230 · 609 231 · 610 198)* có chặn đóng sổ không — vẫn đang chờ *(kế thừa câu H13)*.
2. Mở bước DATA đóng băng nguồn **FS1** *(cho 608 luỹ kế + 605)* hay để ngoài phạm vi?
