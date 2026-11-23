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

---

## Vòng sửa sau R1 *(`KQ-313` — TRƯỢT 1 CHẶN · 4 NÊN SỬA · 6 GHI NHẬN)* · 2026-11-22

| | |
|---|---|
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5434** |
| **Nền** | `isp/H14` `d07f8c3` + gộp ngọn nhánh làm việc *(có I1 · C13b · `WO-315` · `WO-319`)*; xung đột sàn script + bài ghim ⇒ bản nhánh làm việc rồi đặt = thu thập thật. ⛔ gộp DT13 *(R1 DT13 đang chạy)* |
| **Commit** | gộp + ① mã · bài · `hd2_cong.json` · `mong` sinh lại + ② mục này *(chỉ THÊM)* |
| **Kho thật** | `KHONG_CHAM`. `--ghi` khối `WP-C5c`: kho `fls_test`, schema tạm `h14_ghi` *(`nap_nen_kho` rồi ROLLBACK)* |

### Kết luận một dòng
**`HD2_WP_C5C` = `None` CÓ TÊN** *(⛔ `true`)*: **605** ô so **0/13.706** ô số, chưa chữ ký chủ "DỪNG có tên"; cha `HD2_WP_C5` = `None`. **615** hết DỪNG: khuôn CF ⇒ ô so **12.380** · khớp **11.674** *(thật **2.023/2.729** ô có số · 9.651 ô `0 = 0`)* · lệch **706** = `lech_ban_ccr_vs_cf` **671** + `ite_alias` **35** · lệch FLS **0**. Σ 5 đáp án: ô so **84.770** · khớp **76.292** *(thật 13.563/22.041)* · lệch có chủ đích **8.478**.

### Từng phát hiện *(ĐỎ trước — mã cũ `HEAD` + bài mới: **21** failed / 51 ở `tests/oracle/test_do_hd2_c5c.py` + `tests/bao_cao/test_bao_cao_daily_report.py`; **5** failed / 8 bài `/gates` chọn lọc trên `doc_bao_cao.py` cũ)*

| Mã | Sửa | Bằng chứng ĐỎ → xanh |
|---|---|---|
| **`H14-R1-01`** CHẶN | `tools/do_hd2_c5c.py`: `do_phu` *(ô so / ô SỐ của ảnh, từng đáp án)* · `khong_do_duoc` *(đáp án ô so = 0 ⛔ có trong `DUNG_KY`)* · `dat` cổng = `None` khi danh sách ⛔ rỗng *(`dat_mong` giữ phép so `mong`)* · `phu_mot_phan` *(615)*. `DUNG_KY = {}` — chữ ký chủ là ngoại lệ DUY NHẤT. `fls/repo/doc_bao_cao.py` `_goi_la`: `dat=null` + `khong_do_duoc` ⛔ rỗng ⇒ cổng `None` nói tên; `dat=true` mà danh sách ⛔ rỗng ⇒ `None` "tự mâu thuẫn"; sai kiểu ⇒ `None` "hỏng". `do_hd2.py --goi WP-C5c` ⇒ mã thoát 1 khi `None` | Bài mới `test_R1_01_*` ×4 + `test_H14_R1_01_*` ×6 *(gates)*; **đột biến** `dat_cong = px.dat` *(bỏ nhánh `khong_do_duoc`)* ⇒ **3 failed** *(`test_R1_01_cong_null…` · `test_AC5_kho_rong…` · `test_AC5_hd2_cong_json…`)*, trả nguyên `cmp` rỗng. **Xoá khuôn 615** *(`phan_khuon`)* ⇒ 615 ô so 0 ⇒ cổng **ĐỎ** `615: 0 ô được so` *(bài `test_R1_01_bo_khuon_615_thi_DO`)*. `/gates` thật: `HD2_WP_C5C` `None` — `da_do` "76292/84770 ô đáp án khớp [khớp thật 13563/22041 ô có số · 62729 ô 0 = 0] + 8478 lệch có chủ đích"; `ly_do` "1 đáp án ô so = 0 ⇒ ⛔ đo được: 605: ô so 0/13706 ô số — DỪNG `chua_co_dau_vao` CHƯA có chữ ký chủ … · độ phủ 615: ô so 12380/48021 ô số · 35641 ô số chưa so (…)" |
| **`H14-R1-02`** | `DAP_AN["615"]` = khuôn CF *(nhãn đoạn `Unit: mUSD` ↔ `ngay` · `CM Cumulative` ↔ `luy_ke`, kỳ 11/2026)*; đoạn khác ⇒ `NGOAI_KHUON_615` CÓ TÊN; `doi_chieu` = đáp án 610 ⇒ lớp **`lech_ban_ccr_vs_cf`** *(ô lệch mà engine = 610 ⇒ bản chính thức A-CCR ≠ bản CF report — DT13 `BG-320` §1: 615 `Unit: mUSD`/`CM` = `='5. Daily Report 2'!…` của A-CCR, tab ấy DÁN GIÁ TRỊ)* | `test_R1_02_*` ×2: lớp **671 + 35**; mỗi ô `lech_ban_ccr_vs_cf` đo lại từ HAI ảnh *(engine = 610 ≤ 1e-12 < \|615 − 610\|)*; bỏ đối chiếu ⇒ 671 rơi về `lech_dap_an_nguon` |
| **`-02`** · kế toán ô số 615 | mọi ô SỐ ở ĐÚNG MỘT rổ có tên, Σ = **48.021** | ô so **12.380** + `engine_vang` **10.040** *(KPI CFA1 6.200 · ngày sau 18/11 3.240 · mã ngoài IX.HD 600)* + ngoài trục **800** *(`AK` 390 · hàng ⛔ nhãn 410)* + `chua_co_dau_vao` **6.753** *(`cash_balance_by_le` **1.495** chờ ảnh DT13 · `hr` 3.147 · `raw_data_management` 1.040 · `tien_dau_bao_cao` 1.071)* + `ngoai_khuon` **18.048** *(`ban_sao_DR3_A_CCR` 18.046 — đã so ở 609 · hàng ⛔ khối 2)* — bài `test_R1_02_615_khuon_CF_ke_toan_du_48021_o_so` |
| **`H14-R1-03`** | `test_AC4_engine_khong_doc_dap_an` viết lại: ĐẦU ĐỘC *(mọi ô số ⛔ khoá ⇒ "7")* mọi ảnh `tests/fixture/dap_an/*` ⛔ tên `dau_vao` mà `nguon_engine` nạp *(qua `nap_anh` của `do_hd2` · `do_hd2_c3d` · `do_hd2_c5c`)*, dựng lại ⇒ lưới + báo cáo y nguyên. Đ3: bài khẳng định đầu độc CÓ TÁC DỤNG *(ảnh `cfa1_daily` · `cfa1_yhqm` · `pla3_pm_hr_daily` · `atl` bị nạp-độc; `dap_an` thượng nguồn đổi; cổng thượng nguồn đỏ)* | **Đột biến** engine đọc 1 ô đáp án ATL *(`luoi_atl[k] = gia_tri_atl(atl)[k]`)* ⇒ bài **ĐỎ** *(`ne0.luoi ≠ ne.luoi`)*; trả nguyên `cmp` rỗng |
| **`H14-R1-04`** | chỉnh tay = **chuỗi lan** từ gốc `GOC_CHINH_TAY = (GROUP, OMC, 2025M02)`: mã khối GROUP mang `±0,5` ở M02 **VÀ** Q1 · H1 · Y. Ô `loi_as_is` \|e − a\| = 0,5 NGOÀI chuỗi ⇒ `chinh_tay_trung_0_5` *(⛔ gọi chỉnh tay)* | **68** *(17 mã × 4 kỳ)* + **3** trùng *(`GROUP·NPC·2025M01` · `GROUP·NPC·2025M02` · `GROUP·PL5·2025M02`)* ở 607 và 609; `SHQ` trong chuỗi **0**. Gốc đối chiếu HAI nguồn: ảnh 605 `phu.o_chinh_tay` *(hàng ATL 12 · `y2025_m02` · trừ 0.5)* ↔ ảnh ATL hàng 12 = `OMC` *(bài `test_R1_04_goc…`)*; bài đơn vị `chuoi_chinh_tay` *(thiếu một kỳ ⇒ trùng; ⛔ ô gốc ⇒ chuỗi rỗng)*. **Sửa số §4**: "71 + 71" ⇒ **68 + 68** chỉnh tay + **3 + 3** trùng; giả định 3 *("1 ô M01 lọt")* ⇒ thật **3** ô |
| **`H14-R1-08`** | `KHUON_FS`: `FS1_FS2_gop` = *(luỹ kế FS1, luỹ kế FS2)* — tên đúng nghĩa hiện dựng *(609)*; `FS3` = phần `luy_ke:FS3` nguồn `fs3_tin_cay` ⛔ tồn tại ⇒ luôn DỪNG `chua_co_dau_vao` có câu "cần gì" *(⛔ nhãn FS3 trên dữ liệu FS1/FS2)*. `DAP_AN["609"].fs` = `FS1_FS2_gop` | `test_R1_08_FS3_la_cap_tin_cay…` *(đủ nguồn FS1 + FS2 mà FS3 vẫn DỪNG, 0 ô luỹ kế)* · `test_R1_08_anh_609_615…` *(câu "FS3 là mức độ tin cậy giao dịch đủ" có ở ĐÚNG 1 chỗ mỗi ảnh 609 · 615)*. **Sửa Giả định 1**: *"sổ ⛔ ghi nhãn FS3"* **SAI** — ảnh 609 + 615 định nghĩa FS3 = cấp tin cậy cao nhất |
| `H14-R1-09` *(GHI NHẬN, làm kèm)* | bài M10: đáp án DỪNG rỗng ⇒ ĐỎ | `test_R1_09_dap_an_DUNG_rong_DO` |

### ⛔ VÒNG TRÒN — ảnh DT13 `sign_off_dau_vao`
DT13 (`BG-320` §2) đóng băng `sign_off_dau_vao` với **nội dung Y HỆT đáp án 605** *(`BG-320` §2: "= ảnh đáp án 605, cùng nội dung")*. **⛔ được dùng nó để dựng 605**: đổi tên đáp án thành "đầu vào" rồi so lại với chính nó = phép so xanh trên chính mình *(Đ3)*. **Được dùng cho 608** *(luỹ kế FS1: AS-IS 608 đọc tab Sign off thật — `='[MID]…(Sign off)'!W5/…`, DT13 đo 1.363/1.363)* — khi orchestrator nhắn gộp DT13. Ghi ở chú thích `DUNG` + câu "cần" của 605 trong mã.

### Còn lại *(có tên)*
- **605**: `None` tới khi chủ ký "DỪNG có tên" *(điền `DUNG_KY["605"]` = văn bản + ngày + người ký ⇒ cổng `true`; bài `test_R1_01_chu_ky…`)*. DT13: tab gốc `[FS1][PLA5]` ⛔ còn trong sổ — 0 ứng viên.
- **615 `Cash Balance by LE` 1.495 ô**: `chua_co_dau_vao` tới khi gộp DT13 *(`ccr_so_du_ccr` · `ccr_so_du_cash`)*.
- Backlog GHI NHẬN: `-05` *(`chua_co_dau_vao` hai nghĩa — 615 nay tách thêm `ngoai_khuon`, chưa đổi tên nghĩa (a))* · `-06` *(biên độ lệch)* · `-07` *(`NPC` 3 khối × 7 kỳ)* · `-10` *(`dua_ban_ky` khoá theo kỳ — I2)* · `-11` *(WO-319 nay CÓ trên nhánh sau gộp)*.

### Câu hỏi
1. **Chủ**: ký *"605 DỪNG có tên"* không? *(chưa ký ⇒ `HD2_WP_C5C` + cha `HD2_WP_C5` = `None`)*.
2. **BA** *(`H14-R1-08`)*: định nghĩa FS3 *("data đủ PI&PM VÀ consistent với Non-Finance")* — đầu vào nào, mốc nào; ghi `QĐ`. Tới khi có: `FS3` DỪNG, bản 609 mang tên `FS1_FS2_gop`.

### Cổng
| Lệnh | Kết quả |
|---|---|
| `pytest tests/oracle/test_do_hd2_c5c.py tests/bao_cao/test_bao_cao_daily_report.py tests/api/test_isp_gates_hd2.py tests/test_dung_moi_truong_isp.py` | 51 + 85 + 60 passed |
| `pytest --collect-only` | **4.764** *(= 4.678 nhánh làm việc + H13 29 + H14 40 + vòng sửa 17)*; `tests/web` 690 ⇒ `MONG_PYTEST_TOAN_BO` **4.764**, cùng commit |
| `--duong-nen --cong 5434` *(một mình)* | **`KẾT: ĐẠT`** — toàn bộ `12 failed · 4736 passed · 2 xfailed · 14 errors` *(16:13)*: tập đỏ + XFAIL **28 = 28** node id *(thêm 0 · bớt 0)* · chạy **4.764** *(mong ≥ 4.764)* · skipped 0 · deselected 0; `tests/web` `3 failed · 687 passed` = **3 = 3** · chạy 690 |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `kiem_tai_lieu.py` | `✅ cong tai lieu DAT … (479 file, 2938 bang, 966 o ngay, 104 ma QD)` |
| `soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |

## Vòng sửa tích hợp sau R2 (KQ-314)
*(chỉ THÊM · `isp/H14` gộp nhánh làm việc `3ea8052` + `isp/DT13` `ab831d7`; xung đột sàn script + bài ghim ×2 ⇒ bản `isp/H14` rồi đặt = thu thập thật · cụm 5434 · `KHONG_CHAM` kho thật)*

| Mã | Sửa | ĐỎ trước *(Đ5)* |
|---|---|---|
| **`H14-R2-01`** CHẶN | khối `check` của `tools/do_hd2_c5c_mong.py` **sinh lại bằng lần đo** *(cùng đường fixture bài; định dạng `pprint` tái lập từng byte — ⛔ sửa tay)* + `hd2_cong.json` `WP-C5c` bằng `do_hd2.py --goi WP-C5c --dsn <kho test, schema tạm h14_ghi nạp nen_kho> --ghi`. Chỉ `check` đổi *(dap_an · dung giữ)*: `NB = 0` 607/608/609 `dat_0_0` → `dat_co_so` *(147 · 116 · 151)*, 610/615 tách 26/56 · 35/24 — đúng phân loại H13-R1. Bài ghim `test_R2_01_check_NB_0_theo_phan_loai_CHECK_cua_H13` | trên cây gộp: **5 bài đỏ** đúng danh sách KQ-314 ⇒ xanh |
| *(tích hợp, phát hiện thêm)* rào DT13 | `tests/du_lieu/test_rao_dau_vao_dt13_r1.py::test_quet_ma_thuc_…` ĐỎ trên cây gộp: `tools/do_hd2_c5c.py` nhắc `sign_off_dau_vao` mà ⛔ gọi `kiem_dau_vao_hop_le`. Sửa: engine GỌI rào khi nạp ảnh số dư (`nap_so_du`) + `so_sanh_c5c` tự kiểm rào còn chặn `sign_off_dau_vao`→605 và `ccr_daily_report_2`→610 *(mở rào ⇒ ĐỎ có tên)* | 1 bài đỏ ⇒ xanh; bài `test_R2i_rao_DT13_…` *(monkeypatch mở rào ⇒ `dat = False`)* |
| **615 `Cash Balance`** | `fls/bao_cao/so_du_le.py` *(mới, thuần)*: khuôn tường minh 46 cặp (LE × đơn vị) → hàng `2. CCR`/`2. CCR Cash` *(công thức AS-IS DT13; ⛔ suy được bằng nhãn — VVON↔VOON · VVOL↔VOOL · VVOT↔VVOO · UGO2 gồm `Non USD` · 7 LE cá nhân theo thứ tự, khoá `LE<nn>` ⛔ mang tên)*. `do_hd2_c5c`: phần `cb` của báo cáo 615 *(`chep = False`)*; hàng 71 *(công thức đổi theo cột)* = `ngoai_khuon:cb_cong_thuc_doi_theo_cot` | 15 bài đỏ *(mong mới khai trước)* ⇒ xanh; đột biến khuôn hàng 100 ⇒ **7 bài đỏ**, trả nguyên xanh *(đột biến hàng 101 — toàn 0 — chỉ bài hai nguồn cắn: Đ3)* |
| `khop_tinh` / `khop_chep` *(Đ4)* | `dem` mọi đáp án + tổng `hd2_cong`: `khop_co_so = khop_tinh + khop_chep`; phần đánh dấu `chep` ⇒ đếm riêng | PHA đánh dấu `cb` chép ⇒ 852 chuyển sang `khop_chep` |

**Số đo *(Đ4)*:**
| Số | Đếm gì |
|---|---|
| **12.380 → 13.760** / 48.021 | ô so 615 / ô SỐ ảnh 615; chưa so 35.641 → **34.261** |
| **1.380 = 852 + 528**, lệch **0** | ô so khối CB = khớp có số + 0=0 *(46 cặp × 30 ngày 01–30/11)*; ≤ 1e-12, max 1,01e-15 |
| 1.495 = 1.380 + 32 + 37 + 46 | rổ CB cũ = ô so + hàng 71 `ngoai_khuon` + cột `F` 31/10 `cb:f` + cột `AK` `cb:ak` *(ngoài trục)* |
| `khop_tinh` 615 **2.875** · `khop_chep` **0** | ô khớp có số engine TÍNH · ô khớp do CHÉP ảnh dán *(engine 615 ⛔ đọc DR2 ⇒ 0 là KẾT QUẢ, mẫu số phần chép = 0)*; 23.746 ô AS-IS tham chiếu DR2 *(KQ-321)* ⛔ tách từng ô offline |
| Σ ô so **86.150** · khớp **77.672** | WP-C5c 5 đáp án *(trước 84.770 · 76.292)*; lệch có chủ đích 8.478 giữ, lệch FLS 0 |

**⚠ GHI NHẬN mới** — bài hai nguồn *(khuôn engine ⇔ `CB_MAP` DT13)* bắt: công thức AS-IS `LE17 mUSD` *(hàng 132)* và `LE19 mUSD` *(hàng 138)* chia **10^9** dù nhãn `mUSD`. Khuôn GIỮ công thức AS-IS *(`MU_LECH_DON_VI`)*; hàng nguồn 79 · 82 = 0 cả 31 ngày ⇒ phép so ⛔ phân biệt hai mũ *(Đ3)* — câu "AS-IS sai mũ?" chờ chủ/BA.

**Cổng `HD2_WP_C5C`**: vẫn `None` có tên *(605 ô so 0/13.706 chưa chữ ký; `DUNG_KY = {}` — ⛔ tự thêm)*; chuỗi `/gates` nay *"615: ô so 13760/48021 ô số · 34261 ô số chưa so"*, `da_do` *"77672/86150 ô"*.

**GHI NHẬN ⇒ backlog** *(⛔ sửa vòng này)*: `H14-R2-02` *(`DUNG_KY` nhận mọi chuỗi — cần `{nguoi, ngay, qd}`)* · `H14-R2-03` *(câu "35.542" ở chú thích `ban_sao_DR3_A_CCR` — đo ở repo được 18.046/18.046)*.

| Lệnh | Kết quả |
|---|---|
| `pytest --collect-only` | **4.843** = 4.829 cây gộp *(4.767 + DT13 62)* + 14 bài mới *(`test_so_du_le.py` 7 · `test_do_hd2_c5c.py` 7)*; `MONG_PYTEST_TOAN_BO` 4.764 → **4.843** cùng commit; web 690 |
| `--duong-nen --cong 5434` *(một mình, MỘT lần)* | **KẾT: ĐẠT** — `12 failed · 4815 passed · 2 xfailed · 14 errors`: tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)* · chạy 4.843; web 3 = 3 · 690 |
| `lint-imports` | 11 kept, 0 broken |
| `kiem_tai_lieu.py` | ĐẠT *(484 file · 2.954 bảng)* |
| `soi_bang_tuyen.py` · `kiem_thuyet_minh.py` · `sinh_ban_do_tang.py --kiem` | KHỚP 49 tuyến · 35/35 nút · bản đồ khớp |

## Chữ ký chủ 605 (23/11)
Chủ đã ký *"605 DỪNG có tên"* ngày 23/11 *(`TIEN_DO.md` hàng 2026-11-23)*; sửa nhỏ này đóng `H14-R2-02`.

| Việc | Kết quả đo được |
|---|---|
| `DUNG_KY["605"]` | bản ghi **4 khoá**: `nguoi_ky` = `KhanhCQ` *(⛔ email)* · `ngay` = `2026-11-23` · `ly_do` *(tab `[FS1][PLA5]` đã xoá — 0 ứng viên, DT13 `BG-320`; tái lập bằng `sign_off_dau_vao` = vòng tròn, rào DT13)* · `nguon_quyet` = `TIEN_DO 2026-11-23` |
| `kiem_dung_ky()` | thiếu/thừa trường · người ký rỗng hoặc là email · `ly_do` rỗng · ngày sai khuôn hoặc không có thật · mã ⛔ đáp án DỪNG · chuỗi tự do `"x"` ⇒ lỗi CÓ TÊN `DUNG_KY 605: …` ⇒ cổng **ĐỎ** *(⛔ coi như không ký, ⛔ mở cổng)* |
| Cổng `HD2_WP_C5C` | 605 hết chặn: `khong_do_duoc = []` ⇒ `dat = true`; khối mới `dung_co_ky` = `["605: DỪNG có chữ ký KhanhCQ 2026-11-23"]` in ở `da_do` của `/gates` cùng câu *"độ phủ 615: ô so 13760/48021 ô số · 34261 ô số chưa so"* *(giữ nguyên chữ)* |
| Cha `HD2_WP_C5` | theo luật cũ *(mọi con true ⇒ true)*; còn `None` vì lý do khác? **không** — 615 ô so 13760 > 0 *(độ phủ chỉ IN, ⛔ chặn)* |
| `hd2_cong.json` | sinh lại bằng chính `so_sanh_c5c` trên kho `fls_test` đã nạp nền *(schema tạm, ROLLBACK)*: 11+/5−, ⛔ sửa tay *(⛔ `do_hd2.py --ghi` trên kho chưa nạp nền — đúng bẫy `H14-R2-04`, đã trả tệp bằng `git checkout`)* |
| Bài *(Đ5 hai chiều)* | `test_do_hd2_c5c.py` +12 *(`KY605`: cấu trúc · 8 ca hỏng ĐỎ có tên · chuỗi tự do/mã lạ ĐỎ · hợp lệ ⇒ 605 rời danh sách chặn · gỡ chữ ký ⇒ `None`)* · `test_isp_gates_hd2.py` +2 *(tệp thật có chữ ký ⇒ true, gỡ ⇒ `None`; `dung_co_ky` sai kiểu ⇒ `None` tệp hỏng)* · 12 bài cũ đổi kỳ vọng `None → true` |
| Sàn *(Q8)* | `MONG_PYTEST_TOAN_BO` 4843 → **4857** = thu thập thật; web giữ 690 |
