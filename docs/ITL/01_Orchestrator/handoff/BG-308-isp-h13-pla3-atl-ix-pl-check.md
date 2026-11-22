# BG-308 — bàn giao `WO-307` *(ISP 3.1.2 · Step 44 · H13 — SO.PLA3-ATL + IX.PL CHECK, cổng WP-C5b)*

| | |
|---|---|
| **Thuộc** | `WO-307` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5435** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-309`, R2 cuối → `KQ-310`)* |
| **Commit** | `isp/H13` ⇒ `claude/bold-galileo-zukpaf-isp/H13` · ① mã + bài + tệp sinh lại `35ad850` · ② BG này |
| **Nền** | `ad9b70f` *(có gộp H12 `3e23e61` + `WO-307` `15eccc8`)* |
| **Kho thật** | `KHONG_CHAM`. Bài: kho `fls_test` *(schema tạm, giao dịch rollback)*; `--ghi`: kho riêng `fls_h13_cong` *(IX.PER · IX.ALR v1 MM + ký `KhanhCQ` · IX.PL)* |

## Kết luận một dòng
**WP-C5b ĐẠT**: **3.179/4.102** ô dòng PL khớp *(khớp THẬT **884/1.807** ô có số · **2.295** ô `0 = 0`)* + **923** lệch có chủ đích — **MỌI ô thừa kế lớp từ lá** · lệch FLS **0**. CHECK mỗi kỳ-khối: ① `NB = 0` đỏ **147** · ② đỏ **214** · `dat_co_so` **0** ở cả hai *(mọi "đạt" là 0 = 0 — trùng DT11)* ⚠ **đính chính `H13-R1-01`**: câu này đúng cho ②, **sai cho ①** — sau vòng sửa ① `dat_co_so` **178** · `dat_0_0` **359**, xem *Vòng sửa sau R1*. `/gates`: `HD2_WP_C5B` = `true`, cha `HD2_WP_C5` = `2/2 gói con đạt (WP-C5a · WP-C5b)`.

## Đầu vào *(⛔ vòng tròn)*
- **ATL của FLS** = đầu ra AL.KEY H12 ở cờ 2025 BẬT ký *(`do_hd2_c5a.so_sanh_c5a` — WP-C5a phải ĐẠT, khác ⇒ C5b ĐỎ có tên)*. `ThanhQuaC5a` nay trả thêm `o` *(lưới)* + `lop_o` *(lớp từng ô lệch)* — chỉ THÊM.
- **IX.PL ĐỌC TỪ KHO** *(`cau_hinh_repo.doc_pl`)*; engine nhận định nghĩa làm THAM SỐ, tính qua CHÍNH `dong_pl.tinh_pl`/`check_pl` *(⛔ chép biểu thức — bài grep `test_engine_khong_go_cung_ma_HD`)*.
- **`COM_GAG`** *(đầu vào ngoài cây của PL5)* = ảnh `noem_com_gag.json` ÷ USD `ix_fx.json` ÷ 10⁶ — đúng phép ô `AG84:AR84` *(bài C12)*. Ảnh chỉ có **GROUP × 12 tháng 2025** ⇒ ô PL5 khác là `PL_THIEU_GIA_TRI` CÓ TÊN, ngoài mẫu số.
- Đáp án `atl.json` chỉ ĐỌC ở bước so + phép đo hồi phục *(bài `test_AC1_dap_an_khong_vao_engine`: xoá mọi ô dòng PL của ATL ⇒ dòng PL engine y nguyên)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/pla.py` | `dong_pl_atl` — mỗi dòng tính với BAO ĐÓNG riêng *(`tinh_pl` tính mọi dòng đưa vào ⇒ PL5 thiếu `COM_GAG` sẽ làm hỏng cả 7)*; `check_atl` — 4 trạng thái, `atol` 1e-9 ở tầng phân loại *(C12 so `==` tuyệt đối)*; `la_cua_dong` |
| `tools/do_hd2_c5b.py` · `tools/do_hd2_c5b_mong.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C5b [--dsn] [--ghi]`; `mong` khai TRƯỚC *(mẫu số + lớp thừa kế đếm theo khối + sha256 + CHECK)* |
| `tools/do_hd2_c5a.py` | `ThanhQuaC5a.o` + `.lop_o` *(9 dòng THÊM, phép đo C5a ⛔ đổi — `hd2_cong.json` khối C5a y nguyên)* |
| `docs/ITL/_tools/hd2_cong.json` | khối `WP-C5b` sinh bằng `do_hd2.py --goi WP-C5b --dsn …/fls_h13_cong --ghi` *(636 dòng THÊM, 0 xoá)* |
| `tests/bao_cao/test_pla_atl.py` *(10)* · `tests/oracle/test_do_hd2_c5b.py` *(19)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | 12 → **13** cổng; `HD2_WP_C5B` `3179/4102 ô` + 923; cha C5 `2/2`, `lech_co_chu_dich` 5.118 → **6.041** |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 4621 → **4650** *(+29 = thu thập)*, cùng commit |

## Số đo WP-C5b *(Đ4 — mỗi số nói nó đếm gì)*
- **Hàng**: 80 hàng dòng PL có nhãn của ATL = 12 khối × 6 *(PL2·3·4·6·7·8)* + **8** hàng PL5.
- **`tong_o` 4.102** = ô dòng PL so *(80 × 57 kỳ, ô là số, IX.PL tính được)* = `o_co_so` **1.807** + `o_0_0` **2.295**. Ngoài mẫu số, có tên: `pl5_khong_tinh_duoc` **252** · ô ATL rỗng **192** *(PL5 tháng 2024/2026)* · `khong_so_duoc` **14**.
- **`khop` 3.179** = THẬT **884** + `0 = 0` **2.295** · `atol 1e-12`, `rtol 0`. ⚠ Đ4: khớp THẬT chỉ **48,9 %** ô có số — phần còn lại là lệch thừa kế, ⛔ "gần khớp".
- **Hai định nghĩa** *(Đ2 — so HAI nguồn)*: IX.PL ↔ KPI `PL*` của `pla.CONG_THUC_PM` *(H8)* trên cùng lưới FLS: **4.104** ô *(6 dòng × 12 × 57)*, chênh **0**.

**Lệch THỪA KẾ từ lá** *(923 ô — lan nhãn bằng PHÉP ĐO, ⛔ quy tắc khối × năm)*: lá của dòng = `la_cua_dong` *(trải chuỗi PL)*; lá lệch mang lớp C5a. Nhãn = TẬP lớp NHỎ NHẤT mà thay lá lệch thuộc tập ấy bằng giá trị ATL ⇒ ô hồi phục *(≤ 1e-9)*; ⛔ hồi phục / ⛔ lá lệch ⇒ `lech_FLS`.

| Nhãn *(lớp cần để hồi phục)* | Ô | Khối |
|---|---|---|
| `chua_co_dau_vao+lech_D3` | **600** | 6 CDT + SHQ2 |
| `chua_co_dau_vao` | **167** | 6 CDT + SHQ2 |
| `loi_as_is` | **132** | 9 khối *(GROUP 25 · SGO1 21 …)* |
| `chua_co_dau_vao+lech_D3+loi_as_is` | **15** | SHQ2 |
| `chua_co_dau_vao+loi_as_is` | **9** | SHQ2 |
| lệch FLS | **0** | — |

Bằng chứng ĐỘC LẬP: C5a gán lớp cho CHÍNH ô KPI `PL*` bằng phản thực cả lưới ⇒ nhãn thừa kế **chứa** lớp C5a ở **922/922** ô C5a có so · **0** khác · 1 ô C5a ⛔ so *(GROUP PL5 2025M02 — PL5 là ô `trong` của `pla`; thừa kế `loi_as_is` từ `OMC` −0,5 gõ tay)*.

## CHECK mỗi kỳ-khối *(AC-2 — 684 = 12 khối × 57 kỳ mỗi phép)*
| Phép | `dat_co_so` | `dat_0_0` | `do` | `khong_do_duoc` |
|---|---|---|---|---|
| ① `NB = 0` — FLS | **0** | 537 | **147** | 0 |
| ② `NIS+INT+PIT+COM = CXA+GAH+DC+MC` — FLS | **0** | 470 | **214** | 0 |
| ① — ATL *(tham chiếu)* | 0 | 537 | 147 | 0 |
| ② — ATL *(tham chiếu)* | 0 | 473 | 211 | 0 |

- ⚠ **Đính chính `H13-R1-01`** *(bảng trên và câu dưới là số bản đầu — ① `dat_0_0` 537 trộn kỳ-khối có lá ≠ 0 mà `NB` cân; số mới ở *Vòng sửa sau R1*)*.
- ⭐ Bằng chứng dương của CHECK = **0** kỳ-khối ở cả hai phép *(Đ3)* — giống DT11 trên Daily Report; `mong` khai `dat_co_so = 0` RÕ ⇒ ngày có kỳ cân với số ≠ 0, cổng ĐỎ buộc ghi lại.
- **29** kỳ có ≥ 1 khối đỏ; danh sách CÓ TÊN *(kỳ → `phép @khối: chênh`)* ở `hd2_cong.json` › `WP-C5b.check.do_theo_ky` + in bởi `do_hd2.py --goi WP-C5b` *(vd `2025M01`: `NB = 0 @GROUP: -3.221976665` · `@SHQ2` · `@SGO2` …)*; sha256 danh sách khai ở `mong`.
- Đối chiếu CHECK FLS ↔ ATL: **1.326** khớp *(cùng trạng thái + chênh ≤ 1e-9)* + **42** lệch thừa kế `loi_as_is` · lệch FLS **0**.

## AC-5 — chênh định nghĩa PL ATL ↔ Mapping Master
`hd2_cong.json` › `WP-C5b.chenh_dinh_nghia_mm` + báo cáo in: **PL3 `LC`** — ATL trừ License Cost ở PL3; MM mô tả PL3 = PL2 − Tech Service Cost *(⛔ nêu License)*. Nguồn: `dong_pl.CHENH_VOI_MM` *(⛔ tự hoà giải)*.

## Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 | `pytest tests/bao_cao/test_pla_atl.py` ⇒ **10 failed** *(`AttributeError: pla.la_cua_dong`…)*; `tests/oracle/test_do_hd2_c5b.py` ⇒ lỗi thu thập `ImportError: do_hd2_c5b` | mẫu số khai TRƯỚC *(4102 · 3179 · 884 · 923 · 252)*; đột biến `mong` *(tong_o +1 · đếm lớp +1 · bỏ lớp · sha)* + `mong` chưa khai ⇒ ĐỎ; ATL rỗng ⇒ ĐỎ Đ3; nền C5a ĐỎ ⇒ ĐỎ |
| AC-2 | — *(cùng lượt)* | 4 trạng thái *(bài tổng hợp: 0=0 · có số · đỏ · thiếu `MC` ⇒ `khong_do_duoc` có tên `PL_THIEU_GIA_TRI`)*; nhiễu 1e-15 đạt, 1e-6 đỏ |
| AC-3 | — | `GROUP#GI#2025M05` +1e-3 ⇒ ĐỎ **đúng 7** ô `GROUP#PL*#2025M05`, CHECK y nguyên; `SGO2#NB#2025M07` +1 ⇒ ĐỎ **đúng** `NB = 0@SGO2#2025M07`, 0 ô dòng PL; IX.PL `PL2 = GI − OMC` *(hằng và qua KHO)* ⇒ ĐỎ |
| AC-4 | `KeyError: 'WP-C5b'` *(trước `--ghi`)*; bài gates **8 failed** *(13 ≠ 12 …)* | khối `WP-C5b` = lần đo; `/gates` 13 cổng, 0 null |
| AC-5 | — | `chenh_dinh_nghia_mm` = `CHENH_VOI_MM` |
| AC-6 | sàn 4621 ≠ thu thập 4650 | `MONG_PYTEST_TOAN_BO` = **4650** |

**Đột biến NGUỒN** *(sửa → chạy → trả nguyên, `cmp` xác nhận)* — **5/5** bị cắn: M1 thừa kế no-op ⇒ 7 failed · M2 bỏ bao đóng từng dòng ⇒ 12 · M3 `0 = 0` gọi là `dat_co_so` ⇒ 5 · M4 `ATOL_CHECK = 0` ⇒ 1 · M5 bỏ `COM_GAG` ⇒ 4.

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(một mình, MỘT lần, trên `35ad850`)* | **`KẾT: ĐẠT`** *(lần 1 bị dừng ở giới hạn 30 phút của tác vụ nền — hết giờ, ⛔ ĐỎ; chạy lại một lần)* — toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4650** *(mong ≥ 4650)* · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy 690; di trú 27/27 · `pg_verify` 0 lệch · kho `fls` rỗng |
| `pytest tests/oracle tests/bao_cao tests/api tests/cau_hinh tests/du_lieu tests/test_dung_moi_truong_isp.py` | 2.606 passed · 3 failed + 11 errors = tập đỏ sẵn của đường nền *(`*_SO_THAT_*` kho rỗng ×3 · `test_mui_thu_luoi.py` ×11)* |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (459 file, 2897 bang, 949 o ngay, 104 ma QD)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 48 tuyen` |

## Errata v3.1.3 *(đo)*
- ISP Step 44 ghi "dòng PL2…PL8" như MỘT khối đồng đều: **PL5 chỉ đo được ở GROUP × 12 tháng 2025** *(đầu vào `COM_GAG`)*. 7 khối CDT/SHQ2 có hàng PL5 *(33 ô số/khối)* mà ATL tính bằng COM theo CDT1 *(⛔ có ảnh)* — Y/H/Q của PL5 GROUP 2024/2026 *(vd `2024_y` −1,216)* cũng ⛔ có tháng nguồn. ⇒ 252 ô `PL_THIEU_GIA_TRI` có tên; cần ảnh COM theo CDT1 *(`[2025][RPT] NOEM PL & COM` hàng khác `GAG`)* nếu muốn đo.

## Câu hỏi cho orchestrator / chủ sổ
1. **CHECK đỏ là sự thật AS-IS** *(ATL đỏ đúng các kỳ-khối ấy: ① 147/147; ② 204 chung)* — cổng ⛔ đòi CHECK xanh, chỉ đòi đếm = `mong` và kỳ đỏ có tên. Nếu chủ muốn CHECK là cổng CHẶN *(đỏ ⇒ ⛔ đóng sổ)* thì đó là quyết định của H14/I2, ⛔ ở đây.
2. Ảnh COM theo CDT1 cho PL5 khối CDT — mở bước DATA hay để ngoài phạm vi?

## Dev tự thấy còn yếu
- Nhãn thừa kế ghép *(`a+b`)* là tập con của 3 lớp C5a ⇒ khoá `lech_co_ten.lop_thua_ke` có 5 tên, ⛔ 3 — chủ ý *(⛔ ép một nhãn khi cần ≥ 2 lớp mới hồi phục)*.
- `pla._bao_dong` gọi từ công cụ *(tên riêng)* — để công khai nếu bước sau dùng.
- CHECK dùng `atol` 1e-9 ở tầng phân loại; đỏ nhỏ nhất trong 361 ô đỏ = **2,6e-5** *(≥ ×26.000 ngưỡng — đo trên `do_theo_ky`)*, nhưng ngưỡng là quyết định của tầng này, ⛔ của C12.

## Vòng sửa sau R1 (KQ-309)
*(`fls-dev` · cụm 5435 · 2026-11-22 · commit ① `31a6bb3` gộp nhánh làm việc + mã/bài/tệp sinh · ② mục này)*

**`H13-R1-01` — NÊN SỬA ⇒ đã sửa.** `dat_0_0` nay = **TẬP BẰNG CHỨNG của phép toàn 0/trống** *(định nghĩa có tên ở `pla.check_atl`)*:
- phép **MỘT vế** *(so với hằng 0 — ① `NB = 0`)* ⇒ mọi mã **LÁ** của kỳ-khối = **kỳ-khối rỗng thật**;
- phép **HAI vế** *(②)* ⇒ 8 mã của phép *(8 mã = 0 là 0 = 0, ⛔ chứng minh đẳng thức dù kỳ-khối có số)*.
- ⚠ Rỗng đo trên **mã LÁ** *(`ma_la` = `loai_ma` = `la`, 40 mã)*, ⛔ toàn lưới: `NPC` *(Σ hậu tố `NP` QUA kỳ)* ≠ 0 ở **256** kỳ-khối ⛔ có lá nào ≠ 0 ⇒ toàn lưới cho rỗng **129**, lá cho **359**. ⚠ Đo cũng bác định nghĩa "rỗng ⇔ toàn kỳ-khối = 0" cho ② *(②: 111 kỳ-khối có lá ≠ 0 nhưng 8 mã đều 0 sẽ thành `dat_co_so` — bằng chứng giả, Đ3)*.
- ⚠ Dự kiến của R1 *(① `dat_co_so` 56 · `dat_0_0` 481)* dùng `GI = 0` làm thế cho "rỗng"; đo lá: **122** kỳ-khối `GI = 0` vẫn có lá ≠ 0 *(chi phí…)* ⇒ ① `dat_co_so` = 56 *(`GI ≠ 0`)* + 122 = **178**.

| Phép *(684 kỳ-khối)* | `dat_co_so` | `dat_0_0` | `do` | `khong_do_duoc` |
|---|---|---|---|---|
| ① `NB = 0` — FLS | **178** *(trước 0)* | **359** *(trước 537)* | 147 | 0 |
| ② — FLS | 0 | 470 | 214 | 0 |
| ① — ATL *(tham chiếu)* | 172 | 365 | 147 | 0 |
| ② — ATL *(tham chiếu)* | 0 | 473 | 211 | 0 |

- Câu "mọi 'đạt' là 0 = 0" **đúng cho ②, sai cho ①** — đã đính chính tại chỗ *(Kết luận + mục CHECK)*.
- Đối chiếu CHECK FLS ↔ ATL: **1.320** khớp + **48** thừa kế `loi_as_is` *(+6: ① FLS `dat_co_so` ↔ ATL `dat_0_0` ở ASA `2024`·`2024H2`·`2024Q4`·`2024M11`·`2024M12` + SHQ1 `2024M11` — lá `CXA` lệch `loi_as_is`, ≠ 0 ở FLS, 0 ở ATL)* · lệch FLS **0**. Phép đo hồi phục CHECK nay so **CẢ chênh LẪN trạng thái** *(qua chính `check_atl`)*: chỉ so chênh thì 6 ô ấy hồi phục **xanh trên tập rỗng** *(chênh đã bằng 0 = 0)*.
- **Kỳ tổng hợp** `NIS 3 INT 2 PIT 1 COM 1 = CXA 4 GAH 2 DC 1 MC 0`, `NB 0` ⇒ ① **và** ② `dat_co_so` *(bài `test_H13_R1_01_ky_tong_hop_…`)*.
- **WP-C5b không đổi số ô**: `tong_o` 4.102 · `khop` 3.179 *(thật 884 + 0 = 0 2.295)* · 923 lệch thừa kế · `do_sha256` y nguyên. `hd2_cong.json` khối `WP-C5b`: 6 dòng đổi *(chỉ `check`)*.

**`H13-R1-02` — GHI NHẬN ⇒ backlog** *(7 ô GROUP Y/H/Q 2025 vào mẫu số bằng cộng tháng · lớp `dinh_nghia_khac_AS_IS` · ảnh COM CDT1 chỉ cho 75 ô — đổi mẫu số + errata, ⛔ rẻ)*.
**`H13-R1-03` — GHI NHẬN ⇒ làm luôn (rẻ)**: bài `test_H13_R1_03_thua_ke_lay_tap_lop_NHO_NHAT_khong_lay_hop` *(2 lá lệch 2 lớp, dòng chỉ phụ thuộc lá thứ nhất ⇒ nhãn `loi_as_is` ⊊ hợp)*.

**ĐỎ trước:** bài mới ĐỎ trước sửa *(`test_pla_atl.py`: 3 failed)*. **Đột biến nguồn** *(sửa → chạy → trả nguyên)*: M6 trả luật cũ "mọi mã của phép = 0" ⇒ **8** failed · M7 bỏ `ma_la` ở `do_hd2_c5b` ⇒ **7** failed · M8 `_thua_ke` lấy hợp thay vì tập nhỏ nhất ⇒ bài `-03` **1** failed *(trước: SỐNG)*.

**Q8 / sàn:** gộp nhánh làm việc *(có C10)* — xung đột sàn ⇒ bản nhánh làm việc rồi đặt = thu thập thật; `MONG_PYTEST_TOAN_BO` **4685** *(= `--collect-only`; +3 bài vòng sửa)* · web **690**, cùng commit ①.

| Cổng | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --duong-nen --cong 5435` | **ĐẠT** — toàn bộ tập đỏ + XFAIL = đường nền **28 = 28** node id *(thêm 0 · bớt 0)* · chạy 4685 · `tests/web` 3 = 3 · chạy 690 |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `kiem_tai_lieu.py` | `✅ cong tai lieu DAT` *(466 file, 2907 bang)* |
| `soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
