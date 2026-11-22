# BG-278 — bàn giao `WO-277` *(ISP 3.1.2 · Step 39 · H8 — SO.PLA1 dồn ngày 1 tháng PL start (D4) + SO.PLA3 cộng theo khoá, cổng WP-C3d)*

| | |
|---|---|
| **Thuộc** | `WO-277` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5435** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-279`, R2 cuối → `KQ-280`)* |
| **Commit** | `isp/H8` ⇒ `claude/bold-galileo-zukpaf-isp/H8` · ① mã+bài+tệp sinh `2ce7de4` · ② BG này |
| **Nền** | `21d88ac` + gộp `isp/DT7B` @ `d2afe2a` *(BG-282)* + ngọn `claude/bold-galileo-zukpaf` @ `dbac86e` |

## Kết luận một dòng
WP-C3d **ĐẠT**: **258.880/258.888** ô khớp đáp án thật *(khớp THẬT **11.881/11.889** ô có số · **246.999** ô `0 = 0`)* + **8** lệch có chủ đích *(= mong)* · **0** lệch ngoài tên · `atol 1e-12`, `rtol 0`. `/gates` có thêm `HD2_WP_C3D` = `true`; cha `HD2_WP_C3` = `4/4 gói con`, **138** lệch có chủ đích.

## Lịch sử phiên *(Đ1 — ghi cả lượt dừng)*
1. Lượt đầu **DỪNG đúng luật AC-2**: ảnh GL đầu vào thiếu `V·P·DE`, ảnh HR thiếu `BM`. Dựng lại `DE` từ ITL Ledge chỉ khớp **78/1.227** ô ⇒ ⛔ dùng. ⇒ orchestrator phát DT7b *(`WO-281` → `BG-282`)*.
2. Gộp DT7b. Đo FORMULA *(SA chỉ-đọc, 22/11)* thấy **khối CDT của PLA1 cũng thiếu khoá** *(`414!G449` cộng `GL!$AD`; `AD` ⛔ có trong `gl_pl_dau_vao`)*; khối LE/CDT của 416 *(cột `G`)* cộng `HR!$BR/$BS`. Đã nhắn orchestrator; **đính chính của orchestrator 06:26** *(phiên sửa DT7b đo)*: `HR!BR:BS` là bảng ánh xạ CHỮ ⇒ 72 cột đầu *(< `CA`, 2024)* của khối HR LE/CDT = 0; từ `CA` mọi khối dùng `BA − BB`, khối CDT khoá `BP` *(CDT Correct)*. Trong lúc chờ: làm khối có khoá, khai phần còn lại `chua_co_dau_vao` CÓ TÊN.

## Nguồn đầu vào *(⛔ vòng tròn)*
- **PLA1** = `tests/fixture/dau_vao/gl_pl_dau_vao.json` *(DT7b)*: `A·D·E·F` → `tinh_gl` *(H4 — BR/BS tính LẠI; `BR/BS` của ảnh chỉ đối chiếu: `br_lech` **0**)* · `P` = khối LE · `V` = nhãn HD *(so NGUYÊN nhãn như SUMIFS — ⛔ bảng alias)* · **`AH` → `ky.ngay_ghi_nhan` của C6** *(D4 A)*. Cột `DE` của sổ chỉ đối chiếu: `de_lech` **0/7.560**.
- **PLA3 HR** = `tests/fixture/dau_vao/hr_pl_dau_vao.json`: `V` · `BA/BB` *(mUSD của tab — tab ⛔ mang E/F)* · `BK/BL` → luật năm AS-IS của `BM` *(2024 chỉ khi `BL=2024` và tháng 11·12, còn lại 2025)* → C6. `BM` chỉ đối chiếu: `bm_lech` **0/13.356**.
- Config: IX.FX `ix_fx.json` · IX.HD `atl_cay.json` · **IX.PER đọc TỪ KHO** *(C6; kho test nạp `2024-10-21`, luật A)*.
- Đáp án 414–419 chỉ được ĐỌC ở bước so *(bài `test_H8_AC2_xoa_gia_tri_dap_an…`: xoá mọi giá trị đáp án ⇒ 6 lưới engine y nguyên)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/pla.py` *(mới)* | `ngay_pl` *(chỉ qua C6)* · `ngay_pl_tu_yyyymm` *(`AH` rỗng ⇒ `AH_RONG`, lạ ⇒ `AH_LA` — ⛔ tràn tháng như `DATE`)* · `ngay_pl_hr` · `CONG_THUC_PM`/`CONG_THUC_HR` *(17 KPI đo từ FORMULA cột G)* · `pla_daily` = `cfa1_daily` H5 + `danh_gia` · `cong_theo_khoa` · `pla_pm_hr_daily` · `pla_yhqm` = `cuon_ky` H6 + `danh_gia` |
| `tools/do_hd2_c3d.py` · `tools/do_hd2_c3d_mong.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C3d [--dsn]`; `MONG` khai TRƯỚC *(lớp đếm + 8 ô lệch theo giá trị)* |
| `docs/ITL/_tools/hd2_cong.json` | khối `WP-C3d`, sinh bằng `do_hd2.py --goi WP-C3d --dsn $PG_DSN_TEST --ghi` *(khối cũ giữ nguyên)* |
| `tests/bao_cao/test_pla.py` *(19)* · `tests/oracle/test_do_hd2_c3d.py` *(21)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | ghim 10 → **11** cổng; C3 `4/4 gói con` · `476398/476536 ô` · **138** lệch có chủ đích |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` **4375 → 4415** *(= thu thập thật; +40)*, cùng commit |

## Công thức AS-IS engine tái lập *(FORMULA cột G khối GROUP, đọc 22/11)*
- Lá 414: `SUMIFS(GL!BR, GL!DE, G$5, GL!V, $F8) − SUMIFS(GL!BS, …)`; khối LE + `GL!$P, $A$115`; khối CDT + `GL!$AD, A448`; `SHQ2` = `G8 − SUMIFS(G448:G945, …)` *(dư)*. `DE10 = ArrayFormula(DATE(left(AH,4), RIGHT(AH,2), 1))`.
- Lá 416 GROUP: `SUMIFS(HR!BA, HR!BM, …) − SUMIFS(HR!BB, …)`; khối LE/CDT: `HR!$BR/$BS` với `HR!$P`/`HR!$J`.
- `tong` = `=sum(con)` *(10 mã, khớp cây ATL)*. ⚠ **416 `GAC` = `sum(G24,…,G31,G33)` THIẾU `G32` (`CXA`)** — 414/417/418 có đủ.
- KPI *(dấu PM/HR)*: `EBITDA = GI ± OPC ± GAC` · `EBIT = EBITDA ± CDC` · `EBT = EBIT ± ITE` · `NP = EBT ± CIT` · `NPC = sum(G67:67)` ⇒ **Σ hậu tố của NP** · `NCF = NCFO + NCFI + NCFF` · `CRO = GI` · `COO = OPC+GAC+ITE+NIS+INT+PIT+COM+DEP+NB+TAC+CIT` · `COI = CDC` · `CRF = CFI + LMN` · `COF = OMN` · `PL2 = GI ± OMC` · `PL3 = PL2 ± API ± SC ± LC` · `PL4 = PL3 ± PS` · `PL6 = PL4 ± MC ± OTMC ± DC ± CSO` · `PL7 = PL6 ± GAC ± CDC ± ITE` · **`PL8 = PL7 ± TAC`** *(hàng 57 = TAC — nhãn ghi "Tax (CIT)")*. Tab HR: 11 KPI lợi nhuận *(EBITDA…NPC, PL2…PL8)* **chỉ có công thức ở cột `G`** *(cột khác rỗng)*.
- Y/H/Q/M: lá = `sumifs(Daily!$G8:8, Daily!$G$1:$1, G$6)`; `tong`/KPI tính lại trong tab *(NPC hậu tố dọc cột kỳ)*. 419 = Σ-kỳ của **418** *(⛔ 415 + 417)*.

## Số đo WP-C3d *(Đ4 — mỗi số nói nó đếm gì · mong khai TRƯỚC trong `tools/do_hd2_c3d_mong.py`)*
Trục Daily = IX.PER kho `2024-10-21 … 2026-02-27` = **495** ngày *(`den` = cột cuối lưới AS-IS — NPC hậu tố cần cùng mốc cuối)*; Y/H/Q/M = **57** kỳ *(2024·2025·2026 × 19)*.

| Tab | Khối đo được | Ô so thường *(la+tong)* · khớp | Ô so KPI · khớp | `chua_co_dau_vao` *(ô đáp án ≠ 0)* | `cot_ngoai_truc` *(2024-10-20, ô ≠ 0)* |
|---|---|---|---|---|---|
| 414 `pla1_daily` | GROUP + SGO2 SGO1 HGO6 BGO2 | 123.750 · 123.750 | 42.075 · 42.075 | 5.417 *(7 khối CDT)* | 5 *(NPC)* |
| 416 `pla3_hr_daily` | GROUP | 24.750 · **24.746** | 8.415 · **8.411** | 4.457 *(4 LE + 7 CDT)* | 0 |
| 418 `pla3_pm_hr_daily` | GROUP | 24.750 · 24.750 | 8.415 · 8.415 | 9.056 | 1 |
| 415 `pla1_yhqm` | GROUP + 4 LE | 14.250 · 14.250 | 4.845 · 4.845 | 4.862 | — |
| 417 `pla3_hr_yhqm` | GROUP *(ảnh chỉ có GROUP)* | 2.850 · 2.850 | 969 · 969 | 0 | — |
| 419 `pla3_pm_hr_yhqm` | GROUP | 2.850 · 2.850 | 969 · 969 | 8.146 | — |
| **Σ** | | **192.400** · 192.396 | **66.488** · 66.484 | 31.938 | 6 |

- **`tong_o` 258.888** = `o_co_so` 11.889 + `o_0_0` 246.999 · **`khop` 258.880** = `khop_co_so` 11.881 + `o_0_0` · **`lech_co_chu_dich` 8** · `lech_ngoai_ten` **0**.
- **Daily**: ô so 165.825 + 33.165 + 33.165 · lệch FLS **0** · lệch AS-IS **8** *(416)*. **Y/H/Q/M**: ô so 19.095 + 3.819 + 3.819 · lệch FLS **0** · lệch AS-IS **0**.
- **`khong_so_duoc`** = **46.398** = 11 khối × 74 mã × 57 kỳ *(417 chỉ GROUP — ⛔ coi là khớp)*.
- Dung sai: max|lệch| trên ô khớp **3,2e-14** *(415 KPI)* ⇒ `atol 1e-12` *(≥ ×30)*. Chứng ĐỎ: +1e-11 vào một ô đáp án 415 ⇒ ĐỎ đúng ô ấy.

**Lớp lệch / loại CÓ TÊN** *(Đ5: khác mong ⇒ ĐỎ cả hai chiều)*:
- `lech_co_chu_dich` = **8 ô** `pla3_hr_daily` GROUP `GAC · NCFO · COO · NCF` × `2024-11-01 · 2024-12-01` *(khai TỪNG ô theo giá trị, `atol_lech 1e-9`)*. Nguyên nhân: 416 `GAC` thiếu `CXA` *(trên)*; engine theo cây IX.HD. Chênh `GAC` = −0,016428 / −0,032641 — **trùng đúng** 4 ô lệch AS-IS `BG-262` §4 *(`GAC`/`NCFO` × 45597/45627)*; `COO`/`NCF` là hệ quả KPI. ⇒ đây là "Daily 4 ô AS-IS" của WO, nay đã có nguyên nhân.
- `tu_kiem_dap_an` *(GROUP, `418 ≠ 414 + 416` theo khoá, đo trên ĐÁP ÁN)*: Daily thường **4** · KPI **510** · Y/H/Q/M thường **0** · KPI **206**. `tu_kiem_engine` *(cùng phép trên lưới engine)*: thường **0/0** · KPI **505/206**. ⇒ KPI 510/206 là **cấu trúc** *(dấu HR ngược · NPC · HR KPI chỉ cột đầu)*, engine tái lập từng tab nên ⛔ là lệch FLS; 510 − 505 = **5** ô, đo đủ tên *(tập đáp án ⊃ tập engine, hiệu ngược = ∅)*: `COO`/`NCF` × 45597/45627 *(hệ quả 416 `GAC` thiếu `CXA`)* + `NPC` × 45585 *(cột 2024-10-20 ngoài trục engine)*. Hai con số khai ở `lech_co_ten` + `MONG.lop`, ⛔ cộng vào `lech_co_chu_dich` *(hợp đồng CG2: `lech_co_chu_dich` = ô engine ≠ đáp án)*.
- GL: `thieu_D` **6** · `AH_RONG` **309** *(AS-IS `DE = #NUM!`)* · `AH_LA` **8** hàng sheet `669 5487 5556 5557 5634 5712 6230 7098` *(`DT7B-R1-01`: tháng 27/14 · serial 45962 ×2 · `yymmdd` ×4 — năm ∉ 2000…2099 ⇒ lạ; AS-IS `DE` tràn ra ngoài lưới ⇒ bỏ như nhau)* · `dong_ngoai_cay` **51** *(V rỗng / nhãn ⛔ là nút, gồm 2 biến thể ITE — `DT7B-R1-04`)* · `dong_ngoai_truc` **922** *(ngày ghi nhận trước 21/10/2024 hoặc sau 27/02/2026)* · vào engine **7.560**.
- HR: `ba_bb_rong` **2.571** *(góp 0)* · vào engine **13.356** · ngoài cây/trục **0**.

## Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 · H8-B1 | ⚠ bài đơn vị viết CÙNG lượt với engine *(⛔ chạy trước khi có `pla.py`)*; ĐỎ chứng bằng đột biến: **M5** bỏ C6 *(`ngay_pl` trả `pl_start`)* ⇒ `test_H8_B1…` ĐỎ *(2 failed)* | `PL start 2025-03-15 → end 2025-08` ⇒ chỉ ô `2025-03-01` = 6 *(⛔ 1/6 mỗi tháng)*; luật B ⇒ `LUAT_CHUA_KY` |
| AC-2 | lượt đầu DỪNG *(thiếu ảnh)* | `de_lech`/`bm_lech`/`br_lech` = 0; đổi `DE`/`BM`/`BR` ⇒ lưới y nguyên, chỉ bộ đếm đối chiếu ĐỎ |
| AC-3 | `mong` rỗng ⇒ `KHONG DAT` *(`lop … ≠ mong None` · `tong_o 258888 ≠ mong 0`)* | `KẾT: DAT`; Đ3 đáp án rỗng ⇒ ĐỎ; 6 đột biến `mong` + 3 đột biến `o_lech` *(thiếu · thừa · sai giá trị)* ⇒ ĐỎ |
| AC-4 | `test_H8_AC4…` ⇒ `KeyError: 'WP-C3d'` *(trước `--ghi`)*; `test_isp_gates_hd2.py` ⇒ **12 failed** | 79 passed; bài quét tệp thật CG2 xanh |
| AC-5 | — | +E×2 một dòng GL *(GI · SGO1 · AH 202503)* ⇒ ĐỎ đúng `GI` ở 414 GROUP+SGO1 · 418 · 415 · 419 *(HR ⛔ đổi, khối khác ⛔ đổi)*; +1 BA một dòng HR *(NIS · BK 5)* ⇒ ĐỎ 416 · 418 · 417 · 419 *(PLA1 ⛔ đổi)*; đổi `AH` 202503→202504 ⇒ số dời đúng 45717→45748; thay `cong_theo_khoa` bằng zip VỊ TRÍ ⇒ ĐỎ ở 418/419 |

**Đột biến engine** *(bản sao `pla.py`, trả nguyên — cổng · bài đơn vị)*: M1 dấu HR = PM ⇒ ĐỎ · ĐỎ · M2 bỏ "chỉ cột đầu" HR ⇒ ĐỎ · ĐỎ · M3 NPC tiền tố ⇒ ĐỎ · ĐỎ · M6 `PL8` dùng `CIT` ⇒ ĐỎ · ĐỎ · **M5** bỏ C6 ⇒ cổng **XANH** *(mọi `AH` là tháng ⇒ ngày 1 sẵn — tương đương trên dữ liệu thật)*, bài B1 ĐỎ · **M4** `AH` → ngày 15 ⇒ XANH cả hai *(C6 vẫn dồn về ngày 1 — đột biến tương đương, đúng thiết kế)*.

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(một mình, trên `2ce7de4`)* | **`KẾT: ĐẠT`** — toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4415** *(mong ≥ 4415)* · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy 681. Chạy MỘT lần. |
| `pytest tests/oracle tests/bao_cao tests/api/test_isp_gates_hd2.py tests/du_lieu/test_dap_an_pla.py tests/du_lieu/test_dap_an_pl_dau_vao.py` | **700 passed** |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT` *(430 tệp · 2.834 bảng · 924 ô ngày · 104 mã QĐ — đo SAU khi thêm BG này)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 48 tuyen` |
| `tools/sinh_ban_do_tang.py` | ⛔ đổi |

## Errata AP/ISP v3.1.3 *(đo, ⛔ sửa ở bước này)*
1. ISP H8 "PLA3 PM+HR = PLA1 + PLA3 HR cộng theo (HD, ngày)" chỉ đúng cho **lá**; `tong`/KPI tính lại bằng công thức tab 418 *(KPI ⛔ cộng)*.
2. AP "Daily từ 21/10/2024": sheet bắt đầu **20/10** *(`DT7-R1-07`)*; IX.PER kho = 21/10 ⇒ cột 20/10 = `cot_ngoai_truc` *(6 ô NPC ≠ 0, khai)*.
3. 416 `GAC` thiếu `CXA` — lỗi công thức AS-IS *(8 ô)*; báo chủ sổ, ⛔ chép vào engine.
4. `PL8 = PL7 + TAC` *(⛔ CIT như nhãn "Tax (CIT)")* — engine theo công thức.

## Câu hỏi cho orchestrator / BA
1. **Mở khối CDT** *(PLA1 7 khối · HR 11 khối · PM+HR 11 khối = 31.938 ô `chua_co_dau_vao`)*: DT7b đang sửa: GL thêm **`AD`**, HR thêm **`J` + `BP`** *(⛔ BR/BS — đính chính 06:26)*. Khi có ⇒ thêm khối vào `KHOI_DO` + mong; khối CDT cần khoá thứ hai *(`AD`/`BP`)* và `SHQ2` = dư; vùng cột HR < `CA` = 0 của AS-IS ⇒ khai lớp CÓ TÊN.
2. IX.PER ngày đầu 20 hay 21/10 *(errata ㉑)*: nếu 20/10 ⇒ `cot_ngoai_truc` về 0, `o_so` +1 cột.
3. 8 hàng `AH` lạ + 416 `GAC` thiếu `CXA`: báo chủ sổ sửa nguồn?

## Kho thật
`KHONG_CHAM`. IX.PER nạp vào **`fls_test`** *(actor `bai-h8`)* để `--ghi` chạy được. SA đọc FORMULA *(chỉ-đọc)* 22/11: 10 vùng công thức + 4 ô tiêu đề — ⛔ đọc giá trị dữ liệu, ⛔ ghi tệp repo.

## Dev tự thấy còn yếu
- Khối CDT chưa đo *(trên)* — 12 % số ô ≠ 0 của đáp án Daily nằm ngoài phép so.
- `den` *(ngày cuối trục)* lấy từ `MONG` *(cột cuối lưới AS-IS)*, ⛔ từ config: NPC hậu tố phụ thuộc mốc cuối; TO-BE cần quyết NPC tính đến đâu.
- Năm hợp lệ của `AH` *(2000…2099)* là ngưỡng đo, ⛔ luật nghiệp vụ.
