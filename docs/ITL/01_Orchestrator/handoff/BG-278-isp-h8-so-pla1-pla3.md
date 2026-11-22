# BG-278 — bàn giao `WO-277` *(ISP 3.1.2 · Step 39 · H8 — SO.PLA1 dồn ngày 1 tháng PL start (D4) + SO.PLA3 cộng theo khoá, cổng WP-C3d)*

| | |
|---|---|
| **Thuộc** | `WO-277` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5435** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-279`, R2 cuối → `KQ-280`)* |
| **Commit** | `isp/H8` ⇒ `claude/bold-galileo-zukpaf-isp/H8` · ① `2ce7de4` *(5 khối)* · BG lần đầu `65b4e0c` · **gộp DT7b vòng sửa + mở 12 khối `34b6663`** · BG này *(thay bản `65b4e0c`)* |
| **Nền** | `21d88ac` + gộp `isp/DT7B` @ `d2afe2a` rồi @ `8553ca6` *(BG-282 + vòng sửa R1)* + ngọn `claude/bold-galileo-zukpaf` @ `dbac86e` |

## Kết luận một dòng
WP-C3d **ĐẠT** trên **6 tab × 12 khối** *(417: chỉ GROUP)*: **1.287.624/1.289.415** ô khớp đáp án thật *(khớp THẬT **42.710/44.501** ô có số · **1.244.914** ô `0 = 0`)* + **1.791** lệch có chủ đích — **toàn bộ là lệch của AS-IS** *(= mong)* · **0** lệch FLS *(ngoài tên)* · `atol 1e-12`, `rtol 0`. `/gates`: `HD2_WP_C3D` = `true`; cha `HD2_WP_C3` = `4/4 gói con`, **1.921** lệch có chủ đích.

## Lịch sử phiên *(Đ1 — ghi cả lượt dừng)*
1. Lượt đầu **DỪNG đúng luật AC-2**: ảnh GL đầu vào thiếu `V·P·DE`, ảnh HR thiếu `BM` *(dựng `DE` từ ITL Ledge chỉ khớp 78/1.227 ⇒ ⛔ dùng)* ⇒ orchestrator phát DT7b *(`WO-281` → `BG-282`)*.
2. Gộp DT7b `d2afe2a`; đo FORMULA *(SA chỉ-đọc)*: khối CDT của PLA1 cộng `GL!$AD`, của 416 cần khoá CDT ⇒ báo orchestrator; làm 5 khối *(`2ce7de4`, BG `65b4e0c` — 258.880/258.888)*.
3. Orchestrator đính chính *(06:26)* + chốt *(06:57)*: DT7b vòng sửa thêm GL `AD`, HR `J`+`BP`; engine tính luật ĐÚNG mọi cột; 72 cột 2024 của 416 *(bản dán cũ)* ⇒ lệch AS-IS có tên. ⇒ gộp `8553ca6`, mở 12 khối *(`34b6663`)*.

## Nguồn đầu vào *(⛔ vòng tròn)*
- **PLA1** = `tests/fixture/dau_vao/gl_pl_dau_vao.json`: `A·D·E·F` → `tinh_gl` *(H4 — BR/BS tính LẠI; `BR/BS` ảnh chỉ đối chiếu: `br_lech` **0**)* · `P` = khối LE · **`AD` = khối CDT** · `V` = nhãn HD *(so NGUYÊN nhãn như SUMIFS — ⛔ bảng alias)* · **`AH` → `ky.ngay_ghi_nhan` của C6** *(D4 A)*; `DE` chỉ đối chiếu: `de_lech` **0/7.560**.
- **PLA3 HR** = `tests/fixture/dau_vao/hr_pl_dau_vao.json`: `V` · `BA/BB` *(mUSD của tab — ⛔ mang E/F)* · `P` = khối LE · **`BP` = khối CDT** *("CDT Correct" — cột của tab, công thức `VLOOKUP(J, BR11:BS28)`; engine dùng `BP` như SUMIFS của sổ, `J` chưa dùng)* · `BK/BL` → luật năm AS-IS của `BM` → C6; `BM` chỉ đối chiếu: `bm_lech` **0/13.356**. **⛔ `HR!BR/BS`** *(bảng ánh xạ chữ — đính chính 06:26)*.
- Config: IX.FX `ix_fx.json` · IX.HD `atl_cay.json` · **IX.PER đọc TỪ KHO** *(C6; kho test nạp `2024-10-21`, luật A)*. Nhãn 6 khối CDT *(`CVL | VisionLab` … `ASA | Super App`)* = hằng `KHOI_CDT` *(ô `A{mở khối}` 414/416)*; khối dư `SHQ2` = GROUP − Σ 6 khối CDT.
- Đáp án 414–419 chỉ ĐỌC ở bước so *(bài `test_H8_AC2_xoa_gia_tri_dap_an…`: xoá mọi giá trị ⇒ 6 lưới engine y nguyên)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/pla.py` *(mới)* | `ngay_pl` *(chỉ qua C6)* · `ngay_pl_tu_yyyymm` *(`AH` rỗng ⇒ `AH_RONG`, lạ ⇒ `AH_LA`)* · `ngay_pl_hr` · `CONG_THUC_PM`/`CONG_THUC_HR` *(17 KPI; HR chỉ áp khối GROUP — `chi_khoi`/`khoi_khac`)* · `pla_daily(…, cdt=)` = `cfa1_daily` H5 ×2 *(khoá LE · khoá CDT)* + khối dư + `danh_gia` · `cong_theo_khoa` · `pla_pm_hr_daily` · `pla_yhqm` = `cuon_ky` H6 + `danh_gia` |
| `tools/do_hd2_c3d.py` · `tools/do_hd2_c3d_mong.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C3d [--dsn]`; `MONG` khai TRƯỚC *(lớp đếm + 8 ô lệch theo giá trị + lớp `as_is_truoc_CA` theo `tab\|khối` + sha256)* |
| `docs/ITL/_tools/hd2_cong.json` | khối `WP-C3d`, sinh bằng `do_hd2.py --goi WP-C3d --dsn $PG_DSN_TEST --ghi` *(khối cũ giữ nguyên)* |
| `tests/bao_cao/test_pla.py` *(21)* · `tests/oracle/test_do_hd2_c3d.py` *(23)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | 10 → **11** cổng; C3 `4/4 gói con` · `1505142/1507063 ô` · **1.921** lệch có chủ đích |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 4375 → 4415 → **4426** *(= thu thập thật cây gộp; xung đột sàn với DT7b 4382 ⇒ đặt = thu thập)*, cùng commit |

## Công thức AS-IS engine tái lập *(FORMULA, SA chỉ-đọc, 22/11)*
- Lá 414: `SUMIFS(GL!BR, GL!DE, G$5, GL!V, $F8) − SUMIFS(GL!BS, …)`; khối LE + `GL!$P, $A$115`; khối CDT + `GL!$AD, A448`; `SHQ2` = `G8 − SUMIFS(G448:G945, …)` *(dư)*. `DE10 = ArrayFormula(DATE(left(AH,4), RIGHT(AH,2), 1))`.
- Lá 416 *(từ cột `CA` = 2025-01-01)*: `SUMIFS(HR!BA, HR!BM, …, HR!V, …[, HR!P | HR!BP, khối]) − SUMIFS(HR!BB, …)`. **72 cột `G…BX` *(2024)***: GROUP như trên; khối LE/CDT dán CŨ `HR!BR/BS` *(chữ ⇒ 0)* — engine ⛔ chép.
- `tong` = `=sum(con)` theo cây ATL. ⚠ **416 GROUP `GAC` cột `G` = `sum(G24,…,G31,G33)` THIẾU `G32` (`CXA`)**.
- KPI *(dấu ± = PM + / HR −)*: `EBITDA = GI ± OPC ± GAC` · `EBIT = EBITDA ± CDC` · `EBT = EBIT ± ITE` · `NP = EBT ± CIT` · `NPC = sum(G67:67)` ⇒ **Σ hậu tố của NP** · `NCF = NCFO + NCFI + NCFF` · `CRO = GI` · `COO = OPC+GAC+ITE+NIS+INT+PIT+COM+DEP+NB+TAC+CIT` · `COI = CDC` · `CRF = CFI + LMN` · `COF = OMN` · `PL2 = GI ± OMC` · `PL3 = PL2 ± API ± SC ± LC` · `PL4 = PL3 ± PS` · `PL6 = PL4 ± MC ± OTMC ± DC ± CSO` · `PL7 = PL6 ± GAC ± CDC ± ITE` · **`PL8 = PL7 ± TAC`** *(hàng 57 — nhãn "Tax (CIT)")*.
  ⚠ **Dấu HR NGƯỢC + "chỉ cột `G`" + TAC/CIT ⛔ công thức chỉ ở khối GROUP của 416/417**; khối LE/CDT/dư của 416 dùng khuôn KPI 414 *(dấu +, mọi cột)*.
- Y/H/Q/M: lá = `sumifs(Daily!$G8:8, Daily!$G$1:$1, G$6)`; `tong`/KPI tính lại trong tab. 419 = Σ-kỳ của **418**.

## Số đo WP-C3d *(Đ4 — mỗi số nói nó đếm gì · mong khai TRƯỚC trong `tools/do_hd2_c3d_mong.py`)*
Trục Daily = IX.PER kho `2024-10-21 … 2026-02-27` = **495** ngày *(`den` = cột cuối lưới AS-IS — NPC hậu tố cần cùng mốc cuối)*; Y/H/Q/M = **57** kỳ. Khối: 12 *(417: 1)*. Mỗi tab tách **thường** *(la + tong, 50 mã)* · **KPI** *(17 mã)*; `trong` *(7 mã)* ⛔ so *(`trong_khac_0` = 0)*.

| Tab | Ô so thường · khớp · lệch | Ô so KPI · khớp · lệch | `cot_ngoai_truc` *(20/10, ô ≠ 0)* |
|---|---|---|---|
| 414 `pla1_daily` | 297.000 · 297.000 · 0 | 100.980 · 100.980 · 0 | 12 *(NPC)* |
| 416 `pla3_hr_daily` | 297.000 · 296.884 · **116** | 100.980 · 100.562 · **418** | 7 |
| 418 `pla3_pm_hr_daily` | 297.000 · 296.888 · **112** | 100.980 · 100.566 · **414** | 12 |
| 415 `pla1_yhqm` | 34.200 · 34.200 · 0 | 11.628 · 11.628 · 0 | — |
| 417 `pla3_hr_yhqm` *(GROUP)* | 2.850 · 2.850 · 0 | 969 · 969 · 0 | — |
| 419 `pla3_pm_hr_yhqm` | 34.200 · 33.908 · **292** | 11.628 · 11.189 · **439** | — |

- **Daily**: ô so **1.193.940** · khớp **1.192.880** · lệch FLS **0** · lệch AS-IS **1.060** *(thường 228 · KPI 832)*.
- **Y/H/Q/M**: ô so **95.475** · khớp **94.744** · lệch FLS **0** · lệch AS-IS **731** *(thường 292 · KPI 439)*.
- `khong_so_duoc` **46.398** = 11 khối × 74 × 57 *(417 chỉ GROUP — ⛔ coi là khớp)* · `chua_co_dau_vao` **0** *(mọi khối có khoá)*.
- **`tong_o` 1.289.415** = `o_co_so` 44.501 + `o_0_0` 1.244.914 · **`khop` 1.287.624** = `khop_co_so` 42.710 + `o_0_0` · `lech_co_chu_dich` **1.791** = mong · `lech_ngoai_ten` **0**.
- Dung sai: max|lệch| ô khớp **5,3e-14** *(419 KPI)* ⇒ `atol 1e-12` *(≥ ×18)*. Chứng ĐỎ: +1e-11 một ô 415 ⇒ ĐỎ đúng ô.

**Lệch của AS-IS** *(`lech_co_chu_dich` — Đ5 hai chiều)*:
1. **`as_is_416_GAC_thieu_CXA` — 8 ô** khai TỪNG ô theo giá trị *(`atol_lech 1e-9`)*: 416 GROUP `GAC·NCFO·COO·NCF` × 2024-11-01 · 2024-12-01. Chênh `GAC` −0,016428 / −0,032641 = đúng 4 ô AS-IS của `BG-262` §4 *(nay có nguyên nhân)*.
2. **`as_is_truoc_CA` — 1.783 ô**: khối CDT + `SHQ2` ở 72 cột 2024 của 416 *(bản dán cũ ⇒ CDT = 0, SHQ2 = GROUP)*; lan 418 *(= 414 + 416 từng ô)* và kỳ 2024 của 419. Khai đếm theo `tab|khối` *(416: 526 · 418: 526 · 419: 731 — 7 khối mỗi tab)* + **sha256 của (ô, engine, đáp án)** ⇒ đổi GIÁ TRỊ một ô cũng ĐỎ. Quy tắc lớp *(`la_truoc_ca`)*: tab ∈ {416, 418, 419} · khối ∈ CDT ∪ {SHQ2} · ngày < `CA` *(45658)* hoặc kỳ 2024 — ô lệch ngoài quy tắc ⇒ ngoài tên ⇒ ĐỎ. Bằng chứng dương *(Đ3)*: ô LÁ khối CDT 416 trước `CA` ≠ 0 — đáp án **0** · engine **38** *(= số phiên DT7b đếm)*.
- `tu_kiem_*` *(GROUP, `418 ≠ 414 + 416` theo khoá — đếm riêng, ⛔ cộng vào lệch)*: đáp án Daily thường **4** · KPI **510** · Y/H/Q/M **0 · 206**; engine **0 · 505 · 0 · 206**. 510 − 505 = 5 ô: `COO`/`NCF` × 2 ngày *(hệ quả `GAC`)* + `NPC` 20/10 *(ngoài trục)*. KPI 505/206 là **cấu trúc** *(dấu HR · NPC · cột đầu)* ⇒ ⛔ lệch.

**Dòng bỏ / loại CÓ TÊN** *(mong)*: GL `thieu_D` **6** · `AH_RONG` **309** · `AH_LA` **8** *(sheet `669 5487 5556 5557 5634 5712 6230 7098` — `DT7B-R1-01`)* · `dong_ngoai_cay` **51** · `dong_ngoai_truc` **922** · `cdt_khong_khop` **4.798** *(dòng vào engine có nhãn `AD` ⛔ thuộc 6 khối CDT ⇒ chỉ GROUP ⇒ rơi vào dư `SHQ2` — đúng công thức sổ; phần lớn là `SHQ2 | Headquarters2`, còn lại các nhãn lệch chuẩn như `SHQ1| Headquarters1` *(thiếu dấu cách)* · `SHQ2 | Headquarters1` · `TOR | Project A` — đếm ở ảnh: 92 · 31 · 12)* · vào engine **7.560**. HR `ba_bb_rong` **2.571** · `cdt_khong_khop` **1.982** *(= `SHQ2 | Headquarters2` ⇒ dư)* · vào engine **13.356**.

## Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 · H8-B1 | ⚠ bài đơn vị viết CÙNG lượt với engine; ĐỎ chứng bằng đột biến **M5** bỏ C6 ⇒ B1 ĐỎ | PL start `2025-03-15 → 2025-08` ⇒ chỉ ô `2025-03-01` = 6; luật B ⇒ `LUAT_CHUA_KY` |
| AC-2 | lượt đầu DỪNG *(thiếu ảnh)* | `de/bm/br_lech` = 0; đổi `DE`/`BM`/`BR` ⇒ lưới y nguyên, chỉ bộ đếm đối chiếu ĐỎ |
| AC-3 | `mong` rỗng ⇒ `KHONG DAT`; sau gộp DT7b vòng sửa: 4.829 ô ngoài tên ⇒ đo ra công thức KPI khối LE/CDT 416 = khuôn 414 ⇒ còn 1.791, toàn trước `CA` + 8 `GAC` | `KẾT: DAT`; Đ3 đáp án rỗng ⇒ ĐỎ; 7 đột biến `mong` + 3 `o_lech` + 1 giá trị ô trong vùng trước `CA` *(sha)* ⇒ ĐỎ |
| AC-4 | `test_H8_AC4…` ⇒ `KeyError: 'WP-C3d'`; gates ⇒ 12 failed | gates 79 passed; bài quét tệp thật CG2 xanh |
| AC-5 | — | +E×2 một dòng GL *(GI · SGO1 · AD SHQ2 · AH 202503)* ⇒ ĐỎ đúng `GI` ở 414/418/415/419 *(HR ⛔ đổi)*; +1 BA một dòng HR ⇒ ĐỎ 416/418/417/419 *(PLA1 ⛔ đổi)*; đổi `AH` ⇒ số dời tháng; `cong_theo_khoa` → zip VỊ TRÍ ⇒ ĐỎ 418/419 |

**Đột biến engine** *(bản sao `pla.py`, trả nguyên — cổng · bài đơn vị)*: M1 dấu HR = PM ⇒ ĐỎ · ĐỎ · **M7** dấu HR mọi khối ⇒ ĐỎ · ĐỎ · M3 NPC tiền tố ⇒ ĐỎ · ĐỎ · **M8** `SHQ2` = 0 ⇒ ĐỎ · ĐỎ · M6 `PL8` dùng `CIT` ⇒ ĐỎ · ĐỎ *(đo ở bản 5 khối)* · **M5** bỏ C6 ⇒ cổng **XANH** *(mọi `AH` là tháng ⇒ ngày 1 sẵn — tương đương trên dữ liệu thật)*, B1 ĐỎ · M4 `AH` → ngày 15 ⇒ XANH cả hai *(C6 vẫn dồn — tương đương, đúng thiết kế)*.

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(một mình, trên `34b6663`)* | **`KẾT: ĐẠT`** — toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4426** *(mong ≥ 4426)* · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy 681. *(Lần chạy trước trên `2ce7de4` — 5 khối — cũng ĐẠT 4415; chạy lại MỘT lần vì phạm vi đổi theo chốt 06:57.)* |
| `pytest tests/oracle tests/bao_cao tests/api/test_isp_gates_hd2.py tests/du_lieu/test_dap_an_pla.py tests/du_lieu/test_dap_an_pl_dau_vao.py tests/test_dung_moi_truong_isp.py` | **770 passed** + 1 đỏ sàn *(trước khi nâng sàn 4426 — nay xanh)* |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (430 file, 2835 bang, 924 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo SAU khi thêm BG này)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 48 tuyen` |

## Errata AP/ISP v3.1.3 *(đo, ⛔ sửa ở bước này)*
1. ISP H8 "PM+HR = PLA1 + HR cộng theo (HD, ngày)" chỉ đúng cho **lá**; `tong`/KPI tính lại bằng công thức tab 418 *(KPI ⛔ cộng)*.
2. AP "Daily từ 21/10/2024": sheet bắt đầu **20/10** *(`DT7-R1-07`)*; IX.PER kho = 21/10 ⇒ cột 20/10 = `cot_ngoai_truc` *(31 ô NPC ≠ 0)*.
3. `PL8 = PL7 + TAC` *(⛔ CIT như nhãn)*; dấu HR ngược chỉ ở khối GROUP 416/417.

## Câu hỏi cho BA / chủ sổ
1. **Sửa sổ 416?** *(a)* 72 cột 2024 `G…BX` dán cũ `HR!BR/BS` ⇒ khối CDT = 0, SHQ2 = GROUP — **1.783 ô** *(416 · 418 · 419)*; *(b)* GROUP `GAC` cột `G` thiếu `CXA` — **8 ô**. FLS đang tính luật đúng; nếu sửa sổ ⇒ hai lớp về 0 và cổng ĐỎ đúng chỗ ⇒ cập nhật mong.
2. 8 hàng `AH` lạ *(trên)* — chủ sổ sửa nguồn?
3. IX.PER ngày đầu 20 hay 21/10 *(errata ㉑)* — nếu 20/10 ⇒ `cot_ngoai_truc` về 0.
4. Khoá CDT của HR: engine dùng `BP` *(cột tính của tab)*; TO-BE có tính `BP` từ `J` qua IX.ORG/CDT Correct *(`cdt_cua`)* không?

## Kho thật
`KHONG_CHAM`. IX.PER nạp vào **`fls_test`** *(actor `bai-h8`)*. SA đọc FORMULA *(chỉ-đọc)* 22/11 — ⛔ giá trị dữ liệu, ⛔ ghi tệp repo.

## Dev tự thấy còn yếu
- `den` *(ngày cuối trục)* lấy từ `MONG`, ⛔ config — NPC hậu tố phụ thuộc mốc cuối.
- Ngưỡng năm `AH` *(2000…2099)* là ngưỡng đo, ⛔ luật nghiệp vụ.
- Lớp `as_is_truoc_CA` khai bằng đếm + sha *(⛔ từng ô như 8 ô GAC)*: đổi chỗ ô sẽ đổi sha ⇒ ĐỎ, nhưng lời ĐỎ chỉ nói "sha khác" — tái tạo chi tiết bằng `so_sanh_c3d(...).lech`.
