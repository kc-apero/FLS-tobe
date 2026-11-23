# BG-346 — bàn giao `WO-345` *(đóng băng LẠI ảnh HD1/HD2 từ NGUỒN SỐNG — chủ 23/11: nguồn sống là chuẩn)*

| | |
|---|---|
| **Thuộc** | `WO-345` |
| **Phát bởi** | `fls-dev` làn DATA · 2026-11-23 *(phiên cloud con; 4 nhánh con song song cho 52 khuôn HD2)* |
| **Nhận** | `fls-test` *(R1 `KQ-347` · R2 cuối `KQ-348`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/SONG` @ `26edcf1` *(mã + ảnh + bài; BG này ở commit kế)* *(đã đẩy)* — ⛔ gộp *(chủ: chờ PR #1; PR #1 đã merge `c5ea872`, orchestrator gộp sau R2)* |
| **Ghi kho thật** | `KHONG` *(kho nháp `fls_wo345_cu` · `fls_wo345_moi` trên cụm PG 5435, dựng lại từ 0)* |

## Kết luận một dòng
Đóng băng lại **78** ảnh đọc được bằng khuôn/công cụ sẵn có *(52 ảnh HD2 + 26 kỳ sổ DT12)*: **70 ≡** checksum ảnh cũ *(⛔ tệp mới)*, **5 khác nội dung** *(DT12 2025-10 · 2026-03 · 2026-11 · `ccr_so_du_ccr` · `ccr_so_du_cash`)*, **5 khác chỉ ở ô phụ thuộc NGÀY ĐỌC** *(`cfa1_daily` · 4 `daily_report_*` — coi ≡, Giả định G2)*, **3 ĐỎ có tên** *(`ccr_daily_report` khuôn TỪ CHỐI · `ccr_daily_report_2` cổng ĐỎ · `mapping_master_cfg` PII)*. HD2 **11/11 gói số MỚI = số CŨ** trên ảnh cổng đọc; HD1 tự sinh đổi **3 kỳ**; HD1 ghép 1-1 *(5/23 kỳ đạt)* ⛔ đóng băng lại được — **bộ ba ảnh tháng 8 ⛔ có khuôn** ⇒ ĐỎ có tên + câu chủ.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/doc_itl_ledge_ky.py` | `--hau-to _20261123` *(⛔ đè ảnh cũ)* · `--ca-2026-03` *(chủ đã quyết nguồn sống ⇒ `DT12-R1-05` hết chờ)* · `--hang-cuoi` *(lưới **12.824** hàng đo 23/11; hằng cũ 12.684 ⇒ ô A cuối ở hàng **12.731** sẽ bị bỏ **47** hàng)* |
| `tools/do_voi_so_luong.py` | `MANIFEST_KY` = `itl_ledge_cac_ky_20261123.json`; `_duong_anh_ky` = ảnh `_20261123` nếu có, ⛔ thì ảnh 20/11 *(≡)*; nhãn mốc `_moc_so` 3 lớp; `MONG` tự sinh 2026-03 · 2026-11 · `tu_sinh_mid` mới *(số cũ trong chú thích)* |
| `tools/do_tren_anh_song.py` *(mới)* | đo 11 gói HD2 bằng CHÍNH `do_hd2.chay_goi(…, fx="kho")` trên ảnh CŨ hoặc MỚI: kho nháp + `_nap_config` như I2 + ký 37 tháng FX *(actor TEST)*; chuyển hướng ở tầng `open` *(gói ghép đường từ thư mục — vá hằng thì sót)*, GHI LẠI tệp bị chuyển |
| `tests/fixture/dap_an/itl_ledge_{2025-10,2026-03,2026-11}_20261123.json` · `itl_ledge_cac_ky_20261123.json` | ảnh sổ sống 23/11 *(3 kỳ khác)* + manifest 26 kỳ *(23 kỳ ≡ ghi checksum)* |
| `tests/fixture/dau_vao/ccr_so_du_{ccr,cash}_20261123.json` | ảnh số dư A-CCR sống *(cổng khuôn ĐẠT)* — **biên bản**, cổng ⛔ đọc *(G3)* |
| `tests/fixture/dau_vao/ccr_daily_report_2_20261123.DO.json` | cổng ĐỎ `thiếu 2` ⇒ giữ đúng nguồn làm biên bản, đuôi `.DO` *(quy ước `dong_bang_sheet`)* — ⛔ cổng nào đọc |
| `docs/ITL/_tools/voi_so_luong.json` | sinh lại `--ghi` *(khối `tu_sinh` đổi; `tong` · `pm_tong` · `bank_tong` · `dat_hd1` ⛔ đổi — đo)* |
| `tests/oracle/test_tu_sinh_theo_ky.py` · `tests/tich_hop/test_hd1_xuyen_suot.py` | mong theo số MỚI, số cũ ở chú thích; bài B4 đi qua `_duong_anh_ky` THẬT *(⛔ chép luật chọn ảnh)* — giữ lo gốc |
| `tests/test_do_tren_anh_song.py` *(mới, 3 bài)* · `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` | bộ chuyển hướng; sàn **4887 → 4890** = thu thập thật *(Q8)* |
| `hd2_cong.json` | **⛔ đổi** — số MỚI = số CŨ 11/11 gói trên ảnh cổng đọc *(xem §3)* |

## 1 · AC-1 — danh mục ảnh cổng HD1/HD2 đọc *(Đ1: tìm ở `tools/` + `fls/` + `tests/` + `docs/`)*
Cách đo người đọc: **audit-hook `open`** khi chạy 11 gói *(`tools/do_tren_anh_song.py` in tệp bị chuyển)* + grep hằng đường `tools/do_hd2*.py` · `tools/do_voi_so_luong.py`.

**Quyền đọc SA `fls-sheets-reader` *(đo 08:2x–08:53Z 23/11)*:**
| Workbook | id | HTTP |
|---|---|---|
| ITL RAW *(Copy of ITL 1/2)* — L1 · PM · Mapping Master | `1md85t…` | 200 |
| ITL ADJUSTED — `ITL Ledge` | `1r4Wem…` | 200 |
| `[COPY] Report I General Ledger \| P&L Report` | `19NNTb…` | 200 |
| `[COPY] Report I General Ledger \| CF report` | `12S00T…` | 200 |
| `A-CCR_V2_Working` | `1ycMOK…` | 200 |
| `H1000 Ledger (APERO-HR Allocate HD_FS1)` | `1YEyGx…` | 200 |
| `[COPY] APERO \| FS2 (nguồn tỷ giá)` | `1rEky3…` | 200 |
| GI · OMC · SC · PS Data Ledger `[COPY]` | `1rciS4…` · `1-blt0…` · `1X54eY…` · `1QRfU5…` | 200 ×4 |
| `P100 \| Bank Transactions` | `1zJA0M…` | **200** *(08:2x 403 → sau chủ cấp 200)* — 71 tab, **64** tab `R \|` *(08/09: 60)*, 17.656 hàng có ≥1 ô |
| `Copy of P100 \| Cash Ledger` *(bản COPY)* | `1RmmkO…` | **403** *(08:53Z)* — **ĐỎ có tên** |
| ⭐ `P100 \| Cash Ledger` *(bản GỐC — chủ gửi id 23/11)* | `1QSYSzCC0_ZjDmLgEOb2Nre8lp0CXfsAYqmw_Mgs8e9Y` | **200** — 31 tab, 8 tab `R \|`, Σ lưới 46.405 hàng *(= hàng có ≥1 ô A:Z ⇒ ô công thức kín lưới, ⛔ là "dòng giao dịch")* |

⚠ Sao kê Bank/Quỹ ⛔ có ảnh nào trong `tests/fixture/**` *(grep `1zJA0M`/`1RmmkO`/`R |` trong ảnh: 0)* — ảnh 8.368 dòng là ảnh KHO `chup_id 23719` *(cần bản khai cột kho thật)*, mang PII ⇒ ⛔ đóng băng vào repo. Số "dòng chụp" cùng nhãn ⇒ **⛔ đo được ở container này (ĐỎ có tên)**; GỐC ↔ COPY Quỹ ⇒ **⛔ đo được (COPY 403)**.

**Ảnh × khuôn × kết quả** *(nhóm A · B · C · D = 4 nhánh con; chi tiết từng khuôn ở JSON nhánh — số đếm ở đây)*:
| Nhóm · khuôn | Nguồn | Dòng cũ → mới | Kết |
|---|---|---|---|
| A · `gl_406` · `gl_406_dau_vao` · `gl_pl_dau_vao` · `hr_pl_dau_vao` · `gl_hr_413` | P&L `19NNTb…` | 7.883 · 7.883 · 7.883 · 13.356 · 13.087 | ≡ ×5 |
| A · `gl_cf_dau_vao` · `gl_hr_407` · `gl_hr_408` | CF `12S00T…` | 12.385 · 9.421 · 11.712 | ≡ ×3 |
| A · `hr_ledger_2024` · `hr_ledger_2025` | H1000 `1YEyGx…` | 1.381 · 10.105 | ≡ ×2 |
| B · `cfa1_yhqm` · `cfa3` · `pla1_daily` · `pla1_yhqm` · `pla3_hr_daily` · `pla3_hr_yhqm` · `pla3_pm_hr_daily` · `pla3_pm_hr_yhqm` · `atl` | CF · P&L | 5.655 · 650 · 9.694 · 8.844 · 4.730 · 486 · 10.343 · 9.714 · 829 | ≡ ×9 |
| B · `cfa1_daily` | CF | 33.355 → 33.355 | **khác chỉ do ngày đọc**: phụ `ngay_truc` 760 → 765 *(19–23/11 thôi bị cắt "tương lai")*; dòng chính khoá `o_id` 0/0/0; bản thô sống với `doc_luc` 18/11 ⇒ checksum **`6e01ee2b0f2207a3` = ảnh cũ** ⇒ G2 |
| C · `gi_cfa1` · `gi_mid1..3` · `omc_mid1..3` · `sc_mid1..3` · `ps_mid1..3` · `ix_ven` · `mid3_total` | GI/OMC/SC/PS · P&L | 408 · 2.856 · 1.463 · 253 · 6.230 · 1.470 · 900 · 5.187 · 581 · 750 · 8.505 · 3.339 · 594 · 359 · 39 | ≡ ×15 |
| D · `daily_report_3` · `sign_off_dau_vao` · `noem_com_cdt` · `noem_com_gag` · `ix_fx` · `ix_drv` · `atl_cay` · `cdt_correct` | P&L · FS2 · CF | 94 · 94 · 9 · 12 · 37 · 21 · 74 · 13 | ≡ ×8 |
| D · `daily_report_2` · `daily_report_3_fs1` · `_fs2` · `_gop` | CF · P&L | 846 · 921 · 1.236 · 1.742 *(bảng chính 0 ô khác)* | **khác chỉ ô tiêu đề hàng 1** *(2/356 · 1/1.930 · 1/1.998 · 1/594 ô — công thức theo ngày `=G5=$C$1`)* ⇒ G2 |
| D · `ccr_so_du_ccr` · `ccr_so_du_cash` | A-CCR | 191 → 191 *(32 dòng · 342 ô khác)* · 62 → 62 *(14 dòng · 154 ô)* | **khác — cổng ĐẠT** ⇒ ảnh `_20261123` |
| D · `ccr_daily_report_2` | A-CCR | 846 → 846 *(190 dòng · 780 ô khác)* | **ĐỎ** `[ĐỎ] cổng --mong 846: thiếu 2` *(`MONG_CHECK` khuôn: ngày 2026-11-22 mới ở `ngay:GROUP`/`ngay:SGO2`)* ⇒ `.DO.json` |
| D · `ccr_daily_report` *(đáp án 615)* | A-CCR | 2.057 → — | **ĐỎ — khuôn TỪ CHỐI** `values phải 2502 hàng` — nguồn sống **2.566** hàng *(+64)*; ⛔ sửa khuôn |
| D · `mapping_master_cfg` | RAW | 73 → 73 *(bảng chính 0 ô khác)* | **ĐỎ — PII**: bảng phụ `tho` khác 5/84 hàng (25–29, cột A) và mang **8** số TK cá nhân *(`quet_pii_repo`: `khoa_R_CN=4 · so_da_biet_CN=4`)* — luật giả danh của khuôn ⛔ phủ *(cột B thuộc `LE_PHAP_NHAN`)* ⇒ ảnh mới ĐÃ XOÁ, ⛔ commit |
| DT12 `itl_ledge_ky` × 26 kỳ | ADJ `ITL Ledge` | Σ cột A **12.633 → 12.722** | ≡ **23** kỳ; khác **2025-10** *(487 dòng; 1 dòng · 3 ô `svc_start_*`)* · **2026-11** *(659 → 748; +89 dòng, 5 dòng · 33 ô khác)* · **2026-03** *(ảnh cũ là sổ xlsx — hai hình; so bằng tự sinh §2)*; lần 1 kỳ 2026-04 `blocked HTTP 429` *(hạn mức — 4 nhánh song song)* ⇒ lần 2 ĐẠT 26/26 |
| `ix_alr_2025_bat.json` | — | — | ⛔ đóng băng từ sheet *(phiên bản KÝ theo quyết chủ 22/11)* — ngoài phạm vi |
| **HD1 bộ ba** `itl_ledge_adjustment.json` *(xlsx 26/08)* · `classifying_vs_canon.json` *(L1 live 26/08)* · `pm_join.json` *(27/08)* | xlsx · RAW | 9.967 · 9.845 · 3.703/9.992 | **ĐỎ — ⛔ khuôn/công cụ dựng trong repo**: `git log --diff-filter=A` = commit nhập `66cef65` *(lịch sử ép)*; grep `canon_pos_`/`classifying_vs_canon` trong `tools/`+`fls/` ngoài NGƯỜI ĐỌC = **0** ⇒ WO cấm viết khuôn mới ⇒ câu chủ C1 |

⚠ Bẫy đo *(nhánh C + A phát hiện, `fls/oracle/anh_chup.py:38`)*: `checksum_noi_dung` băm cả chuỗi `nguon` ⇒ bản thô phải giữ NGUYÊN VĂN `nguon` của ảnh cũ thì phép ≡ mới có nghĩa *(gl_406 với `nguon` khác chữ: 0 dòng khác mà checksum `53a243…` → `f65e69…`)*.

## 2 · AC-3 — bảng CŨ ↔ MỚI từng số có nhãn

**HD1 — `voi_so_luong.json`** *(CŨ = tệp commit trước WO; MỚI = `--ghi` 23/11)*
| Số *(nhãn — Đ4)* | CŨ | MỚI | Ghi |
|---|---|---|---|
| dòng sổ `co` *(ảnh xlsx 26/08)* · dòng ghép 1-1 `chay` | 9.967 · 9.845 | 9.967 · 9.845 | ⛔ đóng băng lại được *(bộ ba — ĐỎ có tên)* |
| ô parity Final 7 khối | 69.510/69.510 | 69.510/69.510 | như trên |
| kỳ đạt HD1 `dat_hd1` | **5/23** *(2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04)* | **5/23** | như trên |
| tự sinh — ô Final khớp/tổng, 26 kỳ | 88.339/88.431 | **88.962/89.054** | 2026-11 +623 ô |
| tự sinh — khối HD khớp/tổng | 12.633/12.633 | **12.722/12.722** | = Σ cột A manifest |
| tự sinh — MID tự tính = MID sổ | 82.362/88.431 | **82.987/89.054** | |
| 2026-03 MID | 4.020/4.088 *(ảnh xlsx)* | **4.022**/4.088 *(ảnh sống)* | lệch `id_payee` 2 → 0 |
| 2026-11 ô · HD · MID | 4.613 · 659 · 4.610 | **5.236 · 748 · 5.233** | +89 dòng sổ |
| 2025-10 | 3.401/3.409 · lệch Final `svc_end` 8 | = | nội dung đổi 3 ô, số tự sinh ⛔ đổi |
| **HD1 nguồn SỐNG** *(đo lại bằng hàm chỉ-đọc `tools/nap_that.py`, ⛔ `--that`)* | | | *(⛔ vào cổng — ảnh ⛔ khuôn)* |
| L1 dòng đọc = canon + loại + rỗng | 10.100 *(26/08)* · canon 9.992 | **14.265** = 12.601 + 121 + 1.543 *(cân)* | |
| PM dòng · có mã | 3.703 · 3.173 | **3.909** · 3.369 | |
| PM ảnh lệch ở nguồn sống *(theo `dong`)* | — | `cdt1` **534** · `hd` **117** · `ref` **30** · `status` **29** · mất 0 · mới 206 | = BG-335 |
| bậc thang ghép A·B·C·D·E·F *(dòng bank)* | 2.272·29·400·27·199·428 | **2.438·30·404·27·201·438** | |
| bank ⛔ có mã · ⛔ thấy mã PM | 105 · 6.532 | **100 · 8.963** | |
| bộ ba bank `(ref chuẩn hoá, cur, tiền)` của ảnh ⛔ còn ở nguồn sống | — | **18** *(⚠ BG-335 đo **37** theo `ref` THÔ — hai phép, hai nhãn)* | |
| cổng đọc-đủ `T · CDT1` | 3.339 *(27/08)* | **3.056** < sàn 3.300 ⇒ ĐỎ | = BG-335 |

**HD2 — 11 gói** *(CŨ = bộ đo chạy trên ảnh cũ = `hd2_cong.json` commit: **0** khoá lệch ở 11/11 gói — bộ đo đáng tin; MỚI = ảnh `_20261123` chuyển hướng: chỉ **2** tệp đổi — `ccr_so_du_ccr` · `ccr_so_du_cash`)*
| Gói | ô so `tong_o` | khớp | lệch có tên | lệch FLS | CŨ → MỚI |
|---|---|---|---|---|---|
| WP-C2 | 63.016 | 63.016 | — | 0 | = |
| WP-C3a | 205.175 | 205.140 | 35 | 0 | = |
| WP-C3b | 11.585 | 11.543 | 42 | 0 | = |
| WP-C3c | 888 | 835 | 53 | 0 | = |
| WP-C3d | 1.289.415 | 1.287.624 | 1.791 | 0 | = |
| WP-C4a | 420 | 420 | 0 | — | = |
| WP-C4b | 1.981 | 1.981 | 0 | — | = |
| WP-C4c | 19.894 | 19.591 | 303 | — | = |
| WP-C5a | 45.674 | 40.556 | 5.118 | 0 | = |
| WP-C5b | 4.102 | 3.179 | 923 | 0 | = |
| WP-C5c *(ảnh cổng đọc)* | 86.150 | 77.672 | 8.478 | 0 | = |
| WP-C5c *(nếu đọc ảnh số dư MỚI)* | 86.150 | **77.593** | 8.478 | **79** | **ĐỎ** — xem dưới |

**WP-C5c × ảnh số dư mới — ĐỎ có tên, phân lớp:** 79 ô lệch FLS **toàn bộ** ở phần `cb` *(Cash Balance by LE)* của đáp án 615, ngày **2026-11-19…30**, 6 LE *(LE01 bVND/mUSD · LE02 · LE03 · LE06 · LE15 bVND · LE16 mUSD)*; `615.dem.khop_co_so` 2.875 → 2.796. **Lớp = LỆCH THỜI ĐIỂM ẢNH** *(đầu vào số dư 23/11 ↔ đáp án 615 chụp 22/11 — đáp án 615 ⛔ đóng băng lại được vì khuôn TỪ CHỐI 2.566 ≠ 2.502 hàng)*, ⛔ lệch engine. ⇒ cổng giữ ảnh số dư 22/11 *(cùng thời điểm với đáp án — G3)*; ⛔ nới `mong`.

## 3 · Bằng chứng từng AC
| AC | Bằng chứng | Trạng thái |
|---|---|---|
| AC-1 danh mục | §1 *(78 ảnh khuôn + bộ ba + `ix_alr` + 13 workbook đo quyền)* | ĐẠT |
| AC-2 đóng băng lại | 78 ảnh chạy lại KHUÔN có sẵn qua `tools/dong_bang_sheet.py … --mong` *(mong cũ; đếm độc lập)*; ảnh mới `_20261123`, ảnh cũ GIỮ; ≡ ⇒ ⛔ tệp; `quet_pii_repo` 0 | **ĐẠT một phần** — ĐỎ có tên: bộ ba HD1 *(⛔ khuôn)* · `ccr_daily_report` *(khuôn từ chối)* · `ccr_daily_report_2` *(cổng ĐỎ)* · `mapping_master_cfg` *(PII)* · Quỹ COPY 403 · sao kê/quỹ ⛔ có ảnh repo |
| AC-3 đo lại | §2; `voi_so_luong.json` sinh lại; `hd2_cong.json` ⛔ đổi *(MỚI = CŨ trên ảnh cổng đọc)* | ĐẠT |
| AC-4 khớp 100 % | DT12: Σ dòng mỗi kỳ = đếm độc lập cột A *(26/26 · 12.722)*; 52 khuôn HD2: cổng `--mong` ĐẠT trừ 3 ĐỎ có tên; lệch FLS 11/11 gói = **0** trên ảnh cổng đọc; WP-C5c × số dư mới = **79 ĐỎ có tên, phân lớp** | ĐẠT một phần |
| AC-5 cổng | mong đổi cùng commit, số cũ ở chú thích; chứng ĐỎ: trả `MONG["tu_sinh_theo_ky"]["2026-11"]` về 4.613/659 ⇒ `do_voi_so_luong` **exit 1** *(trả nguyên)*; 2 đột biến bộ chuyển hướng *(bỏ `moi.exists()` · bỏ chặn ngoài `tests/fixture`)* ⇒ **1 failed** mỗi cái; `--duong-nen` §5 | xem §5 |
| AC-6 câu chủ | §4 | ĐẠT |

## 4 · AC-6 — số MỚI khác số đã ký O6 *(chủ / ThuongCT ký lại — ⛔ tự coi là đã ký)*
| # | Số đã ký *(O6, 23/11, đo trên ảnh 20/11)* | Số MỚI *(ảnh sống 23/11)* |
|---|---|---|
| 1 | HD1 tự sinh 26 kỳ — ô Final 88.339/88.431 | **88.962/89.054** |
| 2 | HD1 tự sinh — HD 12.633/12.633 · MID 82.362/88.431 | **12.722/12.722 · 82.987/89.054** |
| 3 | 2026-03 MID 4.020/4.088 *(ảnh sổ xlsx — "mốc CŨ")* | **4.022/4.088** *(ảnh sống)* |
| 4 | 2026-11: 659 dòng · ô 4.613 | **748 dòng · ô 5.236** |
| 5 | HD1 5/23 kỳ đạt · 9.845/9.967 dòng ghép | **chưa đo lại được** *(bộ ba ⛔ khuôn — câu C1)*; nguồn sống đã khác §2 *(PM `cdt1` 534 …)* |
| 6 | HD2 11 gói | **⛔ đổi** *(ảnh cổng đọc)*; WP-C5c đọc số dư mới ⇒ 79 lệch FLS *(câu C3)* |

**Câu chủ / BA *(khuyến nghị kèm)*:**
- **C1 — bộ ba HD1 tháng 8:** ⛔ khuôn ⇒ ⛔ đóng băng lại được theo luật WO. *Khuyến nghị:* WO mới viết khuôn `pm_join` + `l1_canon` trên `fls.adapters.pm_join`/`bank` *(hàm đã có, `nap_that.doc_pm`/`doc_nguon`)* + quyết sổ HD1 lấy từ **ITL Ledge sống** *(DT12)* thay ảnh xlsx — cái giá: đổi mẫu số 23 kỳ ⇒ 26 kỳ, mọi số HD1 ký lại.
- **C2 — cổng đọc-đủ CDT1 3.056 < sàn 3.300** *(BG-335 #2)*: vẫn ĐỎ — nguồn mất ≥ 283 ô `CDT1`; ⛔ hạ sàn.
- **C3 — đáp án 615 `ccr_daily_report`:** nguồn 2.566 hàng ≠ khuôn 2.502 ⇒ khuôn TỪ CHỐI; `ccr_daily_report_2` cổng `MONG_CHECK` ĐỎ *(ngày 22/11 mới)*. *Khuyến nghị:* WO khuôn DT13 khai lại `N_HANG`/`MONG_CHECK` theo nguồn sống ⇒ đóng băng lại 615 + DR2 + số dư CÙNG lượt ⇒ đo lại WP-C5c.
- **C4 — `mapping_master_cfg`:** bảng phụ `tho` nguồn sống mang 8 số TK cá nhân mà luật giả danh ⛔ phủ ⇒ sửa luật giả danh *(WO riêng)* trước khi đóng băng lại.
- **C5 — Quỹ:** COPY `1RmmkO…` 403; GỐC `1QSYSz…` 200 ⇒ đổi danh mục nguồn Quỹ sang GỐC *(⛔ sửa `tools/do_hinh_dang.py` ở WO này)*.

## 5 · Cổng `CLAUDE.md` *(dán thật — `PG_DSN=…localhost:5435`)*
| Lệnh | Kết quả *(nguyên văn)* |
|---|---|
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(lần 2, một mình)* | `12 failed, 4862 passed, 2 xfailed, 14 errors in 1389.46s` · `[ĐẠT] đường nền toàn bộ tập đỏ + XFAIL = đường nền: 28 = 28 node id (trong đó XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 4890 bài (mong ≥ 4890)` · web `3 failed, 687 passed` · `[ĐẠT] … 3 = 3 … chạy 690 bài` · **`══ KẾT: ĐẠT — mọi phép kiểm khớp mong`** |
| ↳ lần 1 *(trước sửa bài DT13)* | `13 failed, 4861 passed …` · `[ĐỎ] … đo: 29 · thêm 1` — `+ THÊM tests/du_lieu/test_dau_vao_dt13.py::test_AC2_anh_cu_va_cong_cu_chung_dung_tung_byte` *(bài canh "⛔ ảnh lạ" trong `dau_vao/` thấy 3 ảnh `_20261123`)* ⇒ khai đích danh 3 tệp + sha256, chứng ĐỎ: thêm `la.json` ⇒ `1 failed` |
| `python -m pytest` *(trong `--duong-nen`)* | như trên — tập đỏ nền **28**, ⛔ thêm |
| `python tools/kiem_so_song.py` | `FileNotFoundError: … '.venv/Scripts/lint-imports.exe'` exit 1 — ⛔ CHƯA CHẠY được trên Linux *(đường Windows; có sẵn — BG-326 #7 · BG-335 #6)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (499 file, 3001 bang, 982 o ngay, 104 ma QD)` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 — `A1`/`B1`/`C6 ⛔ DOI TRANG THAI` + `khoi trong lo trinh LECH` — **có sẵn ở nền**: chạy ở `c173338` *(đầu phiếu)* cùng `PG_DSN` ⇒ exit 1, đầu ra **trùng** *(khác duy nhất: `SyntaxWarning` biên dịch lần đầu của worktree)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `python tools/quet_pii_repo.py` | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` *(⛔ chạm schema)* | `khong co gi de ap` · `pg_verify: khop` |
| `python tools/do_voi_so_luong.py` | exit 0 *(HD1 kỳ đạt 5/23; tự sinh 26 kỳ khớp MONG mới)* |
| `python tools/do_tren_anh_song.py --anh cu` · `--anh moi` | exit 0 · CŨ = `hd2_cong.json` 0 khoá lệch 11/11; MỚI: 2 tệp chuyển hướng, WP-C5c `dat=False` lệch FLS 79 *(§2)* |

## Giả định *(phương án hẹp nhất — R1 soi)*
- **G1** ảnh đóng băng lại ra checksum ≡ ⇒ ⛔ ghi tệp `_20261123` *(⛔ nhân đôi repo — 22+1 kỳ DT12 · 61 ảnh HD2)*; manifest DT12 mới ghi checksum mọi kỳ.
- **G2** ảnh chỉ khác ở ô PHỤ THUỘC NGÀY ĐỌC *(trục ngày bị cắt "tương lai" · công thức tiêu đề `=G5=$C$1`)* mà bảng chính 0 ô khác ⇒ coi ≡, xoá ảnh mới *(nhận ảnh mới thì phải đổi `PHU_MONG` khuôn — ngoài phiếu)*.
- **G3** cổng HD2 GIỮ ảnh số dư 22/11 *(cùng thời điểm đáp án 615 22/11)*; ảnh số dư 23/11 là biên bản nguồn sống.

## Kho thật
- `KHONG_CHAM`. Kho nháp `fls_wo345_cu` · `fls_wo345_moi` *(dựng lại từ 0 bằng `dung_lai_kho_test`)*.

## Dev tự thấy còn yếu
- **HD1 lõi chưa đo lại** — đúng chỗ chủ lo nhất *(số O6 ký trên ảnh 26–27/08)*; chỉ có số nguồn sống ngoài cổng §2.
- G2 là phán đoán của Dev: `cfa1_daily` chứng bằng bản thô sống `doc_luc` 18/11 ⇒ checksum cũ; 4 `daily_report_*` chỉ có số đếm ô khác *(⛔ chạy lại với ngày cũ)*.
- 52 ảnh HD2 do 4 nhánh con dựng bản thô theo BG từng bước DT — script ở scratchpad *(⛔ trong repo)* ⇒ R1 ⛔ chạy lại đúng từng byte được; bằng chứng ≡ là checksum *(độc lập cách dựng)*.
- Bộ ba bank 18 ≠ 37 *(BG-335)*: tôi so `ref` chuẩn hoá, BG-335 so `ref` thô — hai phép, chưa đối chiếu tập.
- `tools/do_tren_anh_song.py` ký 37 tháng FX trong kho nháp bằng gọi repo thẳng *(⛔ qua tuyến C7 như I2)* — chỉ để đo.

---

## Vòng sửa sau R1 (`KQ-347`) *(fls-dev làn DATA · 23/11 · cụm PG 5435 · chỉ THÊM)*

Quyết orchestrator *(theo quyết chủ "nguồn sống là chuẩn")*: **⛔ chấp nhận tập đỏ nền 34** — 6 node thêm về 0 bằng sửa gốc.

| Mã | Sửa | ĐỎ trước *(đúng đột biến reviewer)* | Sau |
|---|---|---|---|
| `SONG-R1-01` CHẶN | `tests/du_lieu/test_dau_vao_dt13.py`: bỏ ghim sha256 ảnh `ccr_daily_report_2_20261123.DO.json` *(`.gitignore:26` cấm commit `*.DO.json` — DT2 Q6 = ⓐ)*; tập "⛔ ảnh lạ" lọc `*.DO.json`; **bài mới** `test_AC2_anh_DO_bi_gitignore_nen_bai_khong_duoc_doi_no` ghim luật ignore khớp **đúng 1** dòng + ⛔ khoá `.DO.json` trong `SHA_WO345`. Ảnh `.DO` = biên bản §1 *(số đếm)*, ⛔ vào repo | container sạch *(⛔ tệp `.DO` ở máy)*: **1 failed, 39 passed** `FileNotFoundError` | **41 passed**; đột biến: thêm `la.json` ⇒ 1 failed · gỡ dòng `.gitignore` ⇒ 1 failed · đặt `.DO.json` ở máy ⇒ 41 passed *(bài ⛔ phụ thuộc máy)* |
| `SONG-R1-02` CHẶN | gộp `origin/claude/bold-galileo-zukpaf` @ `f8c6d55` *(có AG)* vào SONG *(xung đột: changelog giữ cả hai · sàn ⇒ bản nhánh làm việc rồi đặt = thu thập)*; **sinh lại bằng công cụ** *(⛔ sửa tay số)*: `tools/chay_agent_voi.py --gia --ghi-phat-lai` ⇒ `phat_lai/A3_SI_ITL.json` · `--ghi-report` ⇒ `report.html` · `tools/sinh_the_agent.py --zip` ⇒ `goi/A3_SI_ITL.zip` · `goi/A4_AUDITOR.zip` *(A1/A2 zip chỉ khác dấu giờ trong zip, nội dung giải nén 0 khác ⇒ giữ; 4 thẻ `A*.md` 0 khác — prompt ⛔ đổi)*; `report.png` chụp lại từ `report.html` mới *(Playwright 1240×1000 — ảnh cũ còn ở bản 627/627)* | `chay_agent_voi.py` phát lại: **`KẾT: ĐỎ`** `KhongCoBanGhi … 19d358a5b379ca84` · 475/557 · 28/74 · chưa chạy 128 · A4 2/4; `tests/agent/test_chuoi.py` **5 failed, 8 passed** | `KẾT: ĐẠT` — ô ĐỘC LẬP **557/557** · ô VÒNG TRÒN **74/74** · lệch 0 · chưa chạy 0 · A4 **4/4**; `tests/agent` **71 passed** |
| `SONG-R1-03` NÊN SỬA | ⚠ Đ1: `hd2_cong.json` **ĐÃ có 11 khối** — `do_hd2._ghi_cong` giữ `WP-C2` ở GỐC *(trường `goi` gốc = `WP-C2` — chỗ R1 đọc)*, 10 gói kia ở khoá `<gói>`. Vẫn **sinh lại cả 11** bằng `do_hd2.py --goi <g> --dsn <kho TEST fls_song_r1_03> --ghi` trên kho ĐÃ nạp nền *(`_nap_config` của `do_tren_anh_song` = I2; 37 tháng FX ký actor TEST; bẫy `H14-R2-04`: gói exit ≠ 0 ⇒ DỪNG + trả tệp)* ⇒ **11/11 `KẾT: ĐẠT`**, số lệch **0**; diff duy nhất 2 chuỗi `truc.nguon_ngay_dau` *(actor nạp IX.PER của kho TEST)* ⇒ **giữ tệp cũ** *(⛔ đổi nguồn gốc ghi bằng actor TEST)*. **Bài mới** `test_SONG_R1_03_hd2_cong_du_11_khoi_dat_va_so_ghim` *(`tests/test_do_tren_anh_song.py`)* ghim 11 khối · `dat` · `tong_o`/`khop` từng gói | — *(bài mới)* | đột biến: xoá khối `WP-C4b` ⇒ 1 failed · `WP-C5c.khop` 77.672 → 77.593 ⇒ 1 failed |
| `SONG-R1-04` GHI NHẬN | — *(SHA/cổng đã điền ở `85138dd`)* | | |
| `SONG-R1-05` GHI NHẬN | backlog — 52 ảnh HD2: script dựng bản thô ở scratchpad 4 nhánh con, ⛔ chạy lại từng byte ở vòng này *(bằng chứng ≡ vẫn là checksum)*; đột biến ≥ 6 *(phiếu R1 ⛔ đòi)* — giao R2 nếu cần | | |
| `SONG-R1-06` GHI NHẬN | → câu chủ **C3** dưới | | |

**Số đổi ở bản ghi agent *(`phat_lai/A3_SI_ITL.json` — 3/395 ô của A3, đo bằng so hai bản JSON)*:**
| Ô *(nhãn — Đ4)* | CŨ *(ảnh 20/11)* | MỚI *(ảnh sống 23/11)* |
|---|---|---|
| `voi:tu_sinh.mid` *(2026-03 · MID tự tính = MID sổ / ô)* | 4.020/4.088 | **4.022/4.088** |
| `voi:tu_sinh.theo_ky.2026-11.hd` *(dòng HD)* | 659/659 | **748/748** |
| `voi:tu_sinh.theo_ky.2026-11.o` *(ô Final)* | 4.613/4.613 | **5.236/5.236** |
| độ phủ `voi` *(lá tệp đo · lá số — ⛔ vào mẫu số)* | 1.045 · 660 | **1.043 · 658** *(2 lá `lech_mid.id_payee` biến mất: 2026-03 lệch 2 → 0; `la_vao` 557 · `so_vao` 318 ⛔ đổi)* — `mong` bài `test_AG_R1_05_…` đổi cùng commit, số cũ ở chú thích |
| `van_tay_yeu_cau` lượt `03_tu_sinh` | `9a6f87ea98497fd7` | `19d358a5b379ca84` |

**Sàn pytest** *(Q8 — thu thập thật cây SONG sau gộp)*: 4958 *(AG)* + 3 *(`WO-345`)* + 1 *(R1-01)* + 1 *(R1-03)* = **4963**; web **690** ⛔ đổi.

### Số cần chủ / ThuongCT ký lại *(cập nhật sau vòng sửa — ⛔ tự coi đã ký)*
| # | Số đã ký *(O6, ảnh 20/11)* | Số MỚI *(ảnh sống 23/11)* | Đổi ở vòng sửa |
|---|---|---|---|
| 1 | HD1 tự sinh 26 kỳ — ô Final 88.339/88.431 | **88.962/89.054** | — |
| 2 | HD1 tự sinh — HD 12.633/12.633 · MID 82.362/88.431 | **12.722/12.722 · 82.987/89.054** | — |
| 3 | 2026-03 MID 4.020/4.088 | **4.022/4.088** | — |
| 4 | 2026-11: 659 dòng · ô 4.613 | **748 dòng · ô 5.236** | — |
| 5 | HD1 5/23 kỳ đạt · 9.845/9.967 dòng ghép | **chưa đo lại được** *(câu C1)* | — |
| 6 | HD2 11 gói *(ảnh cổng đọc)* | **⛔ đổi** — sinh lại 11/11 ĐẠT, lệch số 0 | ⭐ nay có bài ghim 11 khối |
| 7 | WP-C5c đọc số dư MỚI | `khop` 77.672 → **77.593** · lệch FLS **79** | câu C3 |
| 8 | Report agent `WO-329` *(ô A3 + độ phủ)* | 3 ô A3 = #3 · #4; độ phủ `voi` 1.043/658 · KẾT vẫn **ĐẠT 557/557 · 74/74** | ⭐ sinh lại vòng này |

### Câu chủ *(2 phương án + khuyến nghị)*
- **C1 — bộ ba ảnh HD1 tháng 8 *(`itl_ledge_adjustment` · `classifying_vs_canon` · `pm_join`)* ⛔ có khuôn.**
  - ⓐ WO mới viết khuôn `pm_join` + `l1_canon` trên `fls.adapters.pm_join`/`bank` + `nap_that.doc_pm`/`doc_nguon` *(hàm có sẵn)* ⇒ đóng băng lại bộ ba từ nguồn sống, đo lại "5/23 kỳ · 9.845/9.967". Cái giá: ~1 WO DATA + R1/R2; số ghép 1-1 sẽ đổi *(nguồn sống: L1 14.265 dòng · PM 3.909 · `cdt1` lệch 534)* ⇒ ký lại toàn bộ HD1 ghép.
  - ⓑ Bỏ bộ ba làm mẫu số HD1; lấy sổ HD1 từ **ITL Ledge sống** *(DT12, đã đóng băng 26 kỳ 23/11)* — mẫu số 23 → 26 kỳ. Cái giá: đổi định nghĩa "kỳ đạt HD1" *(quyết BA/chủ)*; bộ ba giữ làm biên bản tháng 8.
  - **Khuyến nghị ⓐ trước, ⓑ sau**: ⓐ giữ nguyên định nghĩa đã ký, chỉ thay dữ liệu — đúng tinh thần "nguồn sống là chuẩn" mà ⛔ đổi luật đo cùng lúc.
- **C3 — `WP-C5c` × ảnh số dư 23/11: 79 lệch FLS** *(toàn bộ phần `cb` Cash Balance by LE của đáp án 615, ngày 19–30/11, 6 LE — lớp **lệch thời điểm ảnh**: số dư 23/11 ↔ đáp án 615 chụp 22/11)*.
  - ⓐ Giữ cổng trên ảnh số dư 22/11 *(cùng thời điểm đáp án — G3, hiện trạng)*; mở WO khuôn DT13 khai lại `N_HANG` *(2.502 → 2.566)* + `MONG_CHECK` theo nguồn sống ⇒ đóng băng lại 615 + DR2 + số dư **CÙNG một lượt** ⇒ đo lại WP-C5c *(mong lệch FLS 0)*. Cái giá: 1 WO DATA nhỏ.
  - ⓑ Chuyển cổng sang ảnh số dư 23/11 ngay và khai 79 ô thành lớp lệch có tên `lech_thoi_diem_anh`. Cái giá: cổng mang một lớp lệch **⛔ có trong engine** — gần với "nới `mong`", và che lỗi thật nếu sau này lệch cùng ngày.
  - **Khuyến nghị ⓐ** — ⛔ nới; 79 ô là hệ quả hai ảnh khác thời điểm, chụp cùng lượt thì tự hết hoặc lộ lỗi thật.

### Cổng sau vòng sửa *(dán thật — `PG_DSN=…localhost:5435`)*
| Lệnh | Kết quả *(nguyên văn)* |
|---|---|
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(MỘT lần, một mình, cây `855144c` = SONG đã gộp nhánh làm việc)* | `12 failed, 4935 passed, 2 xfailed, 14 errors in 1245.46s` · `[ĐẠT] đường nền toàn bộ tập đỏ + XFAIL = đường nền: 28 = 28 node id (trong đó XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 4963 bài (mong ≥ 4963)` · web `3 failed, 687 passed` · `[ĐẠT] … 3 = 3 … chạy 690 bài (mong ≥ 690)` · **`══ KẾT: ĐẠT — mọi phép kiểm khớp mong`** *(tập đỏ 34 của R1 ⇒ 28: 6 node thêm về 0)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (511 file, 3042 bang, 984 o ngay, 104 ma QD)` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python tools/quet_pii_repo.py` | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `python tools/chay_agent_voi.py` *(phát lại)* | `KẾT: ĐẠT — ô ĐỘC LẬP … 557/557 khớp · ô VÒNG TRÒN … 74/74 khớp · lệch 0 · … A4 ĐẠT 4/4 agent` |

**Dev tự thấy còn yếu *(vòng sửa)*:** `report.png` chụp bằng Playwright ở khung 1240×1000 đoán theo kích thước ảnh cũ *(⛔ có công cụ sinh trong repo)*; dòng "Tham chiếu: `voi_so_luong.json` 2026-08-26" trong report đọc trường ngày của tệp đo *(ngày ảnh sổ xlsx)* — ⛔ đổi ở vòng này; C1/C3 vẫn chờ chủ.

---

## WO-353 — khuôn bộ ba HD1 *(C1 = ⓐ)* · chụp lại 615 + DR2 + số dư CÙNG một lượt *(C3 = ⓐ)* *(fls-dev làn DATA · 23/11 · cụm PG 5435)*

**Kết luận một dòng.** 7 khuôn ĐẠT trên MỘT lượt đọc sống bằng công cụ commit `tools/doc_bo_ba_hd1.py` *(⛔ script scratchpad — `SONG-R1-05`)*. **C1:** HD1 trên bộ ba sống, ĐỊNH NGHĨA + mẫu số 23 kỳ GIỮ NGUYÊN ⇒ **16/23 kỳ đạt** *(cũ 5/23)* · ghép 1-1 **10.187/10.199** *(cũ 9.845/9.967)* — nhưng **cổng mặc định GIỮ bộ ba CŨ** *(số đã ký; chuyển = câu chủ C6 — đo: 81 bài ràng vào bộ ba cũ)*. **C3:** WP-C5c trên 615 + số dư cùng lượt ⇒ phần `cb` **1.380/1.380 · lệch FLS 0** *(79 ô của WO-345 = lệch THỜI ĐIỂM ẢNH, đã hết)*; cổng `do_hd2.py --goi WP-C5c` **ĐẠT**, `khop` 77.672 → **77.663** *(+9 ô lớp có tên `lech_ban_ccr_vs_cf`)* ⇒ sinh lại bản ghi phát lại + report agent, **KẾT ĐẠT 557/557 · 74/74**.

### Lượt đọc *(SA `fls-sheets-reader` chỉ-đọc · `UNFORMATTED_VALUE` · bản thô `/tmp/wo353` thư mục 700 / tệp 600, ĐÃ XOÁ sau dùng)*
| Lượt | Giờ đọc *(UTC, `luot_*.json`)* | Vùng | Hàng đọc về |
|---|---|---|---|
| C3 · A-CCR `1ycMOK…` | **12:11:45 → 12:11:50** *(4 tab liền nhau)* | `5. Daily Report` A1:AR12521 · `5. Daily Report 2` A1:AR1114 · `2. CCR` A1:ABM240 · `2. CCR Cash` A1:ABM240 | 2.566 · 958 · 236 · 175 |
| C1 · sổ ADJUSTED `1r4Wem…` `ITL Ledge` | 12:11:50 → 12:17:13 *(1 lát `HTTP 503` lần 1 ⇒ lần 2 ĐẠT)* | A7:AT8 tiêu đề · `A:B` · `D:G` · `R:AT` hàng 10…12.731 *(⛔ cột C Diễn giải)* | 12.722 hàng có ô A |
| C1 · RAW `1md85t…` `Transaction Mapping L1` | → 12:17:21 | A3:AL3 + A5:AL… | 14.265 |
| C1 · RAW `[Importrange]PM_Unpivot` | → 12:17:22 | A2:AC2 + A3:AC… — **CHIẾU 14 vị trí `PM_TIEU_DE_MONG_DOI` trước khi chạm đĩa** *(⛔ Email · tên/số TK · ghi chú)* | 3.909 |

⚠ Một lượt đọc thử trước đó *(script scratchpad 12:04–12:11Z)* chỉ để dựng khuôn; MỌI ảnh commit sinh từ lượt công cụ commit ở trên. Nguồn Bank `1zJA0M…` · Quỹ GỐC `1QSYSz…` ⛔ cần cho WO này *(bộ ba đọc L1/PM ở RAW; C3 đọc A-CCR)* — ⛔ đọc.

### Đã đổi *(WO-353)*
| Tệp | Vì sao |
|---|---|
| `tools/khuon_dong_bang/_bo_ba_hd1.py` *(mới)* | thân chung: `khoa_ghep` = sha256[:16] của (Số CT `canon_ref` · PS Nợ · PS Có `parse_so` · TK · tiền tệ) — MỘT hàm cho sổ VÀ L1; ⛔ lưu Số CT sổ |
| `tools/khuon_dong_bang/itl_ledge_adjustment.py` *(mới)* | khuôn SỔ: `dong_sheet · ky · khoa_ghep` + 7 khối × Cls/MID/Final *(= cột ảnh tháng 8)*; tên 30 cột R:AT so `itl_ledge_ky.TIEU_DE`; `MONG_KY` 26 kỳ Σ 12.722 |
| `tools/khuon_dong_bang/l1_canon.py` *(mới)* | khuôn L1 qua CHÍNH `bank.nap` + `chay_nap._bank_tu_canon`; `ref_tho · cur · tien · khoa_ghep` + 7 `canon_pos_p` *(vị trí `VI_TRI_CLASSIFYING`; ảnh tháng 8 giữ 13 — 6 vị trí thừa ~5,3 MB ô `#N/A` ⛔ mang)*; `MONG_BA_DUONG` |
| `tools/khuon_dong_bang/pm_join.py` *(mới)* | khuôn PM qua `nap_that.dung_pm`; TỪ CHỐI tên cột riêng tư / ô ngoài 14 vị trí; `MONG_DEM` |
| `tools/nap_that.py` | tách `dung_pm(tieu_de, hang)` THUẦN ra khỏi `doc_pm` *(⛔ đổi luật đọc — `doc_pm` gọi lại nó)* |
| `tools/khuon_dong_bang/ccr_daily_report_song.py` · `ccr_daily_report_2_song.py` *(mới)* | khuôn ANH EM *(⛔ sửa khuôn cũ — khuôn cũ là cổng của ảnh 22/11 biên bản)*: 615 `N_HANG` 2.502 → **2.566**, `LOI_MONG` 127 → 120 ô, `PHU_MONG.tieu_de` 1.792 → 2.377, bỏ `Daily Transactions:No`; DR2 CHỈ `MONG_CHECK` `nb_khac_0` thêm `2026-11-22` ở GROUP · SGO2 |
| `tools/khuon_dong_bang/_rao_dau_vao.py` | `ANH_CO_RAO` + `ccr_daily_report_2_song` *(ảnh mang tên khuôn ấy — ⛔ thì rào cho qua IM LẶNG)*; `quet_tham_chieu` so theo TOKEN *(`ccr_daily_report_2` là chuỗi con của `ccr_daily_report_20261123` — quét chuỗi con bắt nhầm)* |
| `tools/doc_bo_ba_hd1.py` *(mới)* | MỘT lượt đọc 7 nguồn ⇒ bản thô `/tmp` ⇒ 7 khuôn qua `dong_bang_sheet.py --mong` *(`MONG_DONG_ANH`)*; kiểm rào DR2 → 615 ĐẠT / → 610 ĐỎ ngay sau đóng băng |
| `tests/fixture/{itl_ledge_adjustment,l1_canon,pm_join}_song_20261123.json` | ảnh bộ ba sống *(17,2 · 11,1 · 1,5 MB)*; hậu tố `_song_` để `do_tren_anh_song --hau-to _20261123` ⛔ chuyển hướng nhầm ảnh sổ cũ *(đo: lần đầu WP-C2 `KeyError: 'phan_bo_ky'`)*. Bộ ba tháng 8 GIỮ — biên bản |
| `tests/fixture/dap_an/ccr_daily_report_20261123.json` · `dau_vao/ccr_daily_report_2_20261123.json` | 615 · DR2 cùng lượt. Số dư lượt này ra **ĐÚNG TỪNG BYTE** ảnh `ccr_so_du_{ccr,cash}_20261123.json` sáng 23/11 *(ghi đè ⇒ `git status` 0 đổi)* ⇒ G1, ⛔ tệp mới |
| `tools/do_voi_so_luong.py` | `do(bo_ba=…)`: `cu` *(mặc định — `voi_so_luong.json` **0 byte đổi**)* · `song` *(`MONG_SONG`, ghép `ghep_theo_khoa`, mẫu số `KY_HD1` = 23 kỳ ảnh tháng 8; kỳ 2026-09…11 ⇒ `ngoai_mau_so`)*; `--bo-ba song --ghi` ⇒ `docs/ITL/_tools/voi_so_luong_song.json` |
| `tools/do_hd2_c5c.py` · `do_hd2_c5c_mong.py` | 615 + số dư đọc bộ ảnh cùng lượt `_20261123` *(`TEP_LUOT_C5C`)*; khối `615` của `mong` SINH LẠI từ MỘT lần `chay_wp_c5c` *(`pprint width=120` — tái tạo đúng từng byte tệp cũ trước khi đổi; 4 đáp án kia máy so bằng)* |
| `docs/ITL/_tools/hd2_cong.json` | `do_hd2.py --goi WP-C5c --dsn …/fls_wo353_mong --ghi` — CHỈ khối WP-C5c đổi *(diff dưới)* |
| `docs/ITL/06_Agent/phat_lai/A3_SI_ITL.json` · `report.html` · `report.png` · `goi/A3_SI_ITL.zip` · `goi/A4_AUDITOR.zip` | sinh lại bằng công cụ; A1/A2 zip chỉ khác dấu giờ *(giải nén 0 tệp khác)* ⇒ giữ |
| `tests/du_lieu/test_bo_ba_hd1_song.py` *(mới)* · bài ghim cũ *(`test_do_hd2_c5c` · `test_isp_gates_hd2` · `test_do_tren_anh_song` · `test_dau_vao_dt13` · `test_rao_dau_vao_dt13_r1`)* | mong mới = số đo mới, số cũ ở chú thích |

### AC-2 · HD1 — bảng CŨ ↔ MỚI *(định nghĩa `phan_hd1` y nguyên; CŨ = bộ ba tháng 8 = cổng; MỚI = `do(bo_ba="song")`)*
| Số *(nhãn — Đ4)* | CŨ *(xlsx 26/08 · L1 26/08 · PM 27/08)* | MỚI *(sống 23/11)* |
|---|---|---|
| mẫu số kỳ | 23 *(2024-10…2026-08)* | **23** *(GIỮ — `KY_HD1`)*; ngoài mẫu số: 2026-09 737 · 10 1.038 · 11 748 dòng sổ |
| **kỳ đạt HD1** `dat_hd1` | **5/23** *(2024-10 · 11 · 12 · 2025-03 · 04)* | **16/23** *(2024-10…2025-10 · 2025-12 · 2026-01 · 2026-08)* |
| kỳ đỏ *(dòng thiếu · [loại] · ô)* | 18 | **7**: 2025-11 2 · 2026-02 1 · 03 2 · 04 1 · 05 1 · 06 2 · 07 3 + loại 13 · ô 4.770/4.802 |
| dòng sổ `co` · **dòng ghép 1-1** `chay` | 9.967 · 9.845 | **10.199 · 10.187** |
| dòng thiếu *(sổ ⛔ ghép)* | 122 | **12** — cả 12 *(và 121/121 trên 26 kỳ)* = hàng L1 bị `bank.nap` LOẠI `cot goc AG ('LE') la o loi` *(khoá ghép trùng khoá hàng loại — đo trên bản thô)* |
| chiều ngược *(dòng FLS ⛔ dòng sổ)* | 147 | **0** *(12.601/12.601 canon ghép)* |
| **ô parity** Final 7 khối *(dòng tự nhất quán)* | 69.510/69.510 | **71.302/71.302** |
| ô Final trên MỌI dòng `o_moi_dong` | 69.706/69.769 *(63 lệch)* | **71.361/71.393** *(32 lệch, cả 32 ở 2026-07)* |
| dòng tự-soi loại | 37 | **13** *(2026-07)* |
| khối HD parity | 9.930/9.930 | **10.186/10.186** |
| Classifying sổ = `iferror(canon)` *(phép của ảnh `classifying_vs_canon`)* | 68.915/68.915 | **88.207/88.207** *(23 kỳ: 71.309/71.309)* |
| bank · PM · có mã PM | 9.992 · 3.703 · 3.173 | **12.601 · 3.909 · 3.369** |
| bậc thang ghép A·B·C·D·E·F | 2.272·29·400·27·199·428 | **2.438·30·404·27·201·438** *(= BG-346 §2 đo chỉ-đọc — Đ2)* |
| bank ⛔ mã · ⛔ thấy mã PM | 105 · 6.532 | **100 · 8.963** |
| checksum ảnh | `575c5337…` · `7226ef11…` · `6ec10945…` | `469daa90…` · `bb2386bf…` · `51c6454d…` |

### AC-3 · WP-C5c — CŨ ↔ MỚI *(`do_hd2.py --goi WP-C5c` — cổng)*
| Số | CŨ *(615 + số dư 22/11)* | WO-345 *(615 22/11 + số dư 23/11)* | **MỚI** *(615 + số dư CÙNG lượt 23/11)* |
|---|---|---|---|
| ô so `tong_o` | 86.150 | 86.150 | **86.150** |
| khớp `khop` | 77.672 | 77.593 | **77.663** |
| lệch có tên `lech_co_chu_dich` | 8.478 | 8.478 | **8.487** |
| **lệch FLS** *(5 đáp án)* | 0 | **79** *(`cb` 19–30/11)* | **0** |
| 615 `cb` khớp/ô | 1.380/1.380 | 1.301/1.380 | **1.380/1.380** |
| 615 `luy_ke` khớp · lệch | 7.041 · 479 | — | **7.032 · 488** |
| 615 lớp `lech_ban_ccr_vs_cf` *(engine = 610, A-CCR ≠ CF report)* | 671 | — | **680** *(+9 — bản A-CCR đổi từ 22/11; ⛔ engine)* |
| 615 `ngoai_khuon.daily_transactions` | 0 | — | **⛔ còn đoạn** *(hàng mang chữ ⇒ tiêu đề; bảng chính 2.057 → 2.056)* |
| cổng | ĐẠT | ĐỎ | **ĐẠT** · `KẾT: ĐẠT · so mong: DAT` |

### Số cần chủ / ThuongCT ký lại *(cập nhật WO-353 — ⛔ tự coi đã ký)*
| # | Số đã ký *(O6)* | Số MỚI | WO-353 |
|---|---|---|---|
| 1–4 | *(tự sinh — như trên)* | *(như trên)* | — |
| 5 | HD1 **5/23** kỳ đạt · **9.845/9.967** dòng ghép · ô 69.510/69.510 | **16/23 · 10.187/10.199 · 71.302/71.302** *(bộ ba sống, đo được — `voi_so_luong_song.json`)* | ⭐ đo được; **cổng vẫn đọc bộ ba cũ** ⇒ câu C6 |
| 6 | HD2 11 gói | 10 gói ⛔ đổi; **WP-C5c khop 77.663 · lệch có tên 8.487 · lệch FLS 0** | ⭐ cổng đổi |
| 7 | *(WO-345)* WP-C5c × số dư mới 79 lệch FLS | **hết** — lệch thời điểm ảnh | ⭐ đóng C3 |
| 8 | Report agent | ô `hd2:WP-C5c.*` đổi ở lượt 7 A3 *(`van_tay_yeu_cau` `ab7bc4c0…` → `74776d1c…`)*; KẾT **ĐẠT 557/557 · 74/74** | ⭐ sinh lại |

### Câu chủ *(mới)*
- **C6 — chuyển cổng HD1 sang bộ ba sống?** Đo: đặt `BO_BA_MAC_DINH = "song"` ⇒ **81 failed · 237 passed** ở 10 tệp bài HD1/CG1/F03/agent — vì tập 122 dòng thiếu của DT1a/DT1b *(nhãn lý do + vân tay)*, chữ ký O8 `so_ly_do_hd1.json`, các số 69.510 · 5/23 đều buộc vào bộ ba tháng 8.
  - ⓐ Chuyển: WO DATA mới — sinh lại DT1a `phan_loai_dong_thieu` + DT1b `phan_loai_ly_do` trên tập 12 dòng thiếu sống *(đều cùng MỘT lý do có tên `AG (LE) ô lỗi`)* + 13 dòng loại 2026-07, ký lại O6/O8, sửa ~81 bài. Cái giá: 1 WO + R1/R2.
  - ⓑ Giữ cổng cũ đến khi chủ ký số #5; bộ ba sống là cổng PHỤ có ghim *(hiện trạng)*.
  - **Khuyến nghị ⓐ sau khi chủ ký #5** — nguồn sống là chuẩn, nhưng đổi số đã ký trước chữ ký là "tự coi đã ký".

### Giả định *(R1 soi)*
- **G4** mẫu số HD1 trên bộ ba sống = 23 kỳ của ảnh tháng 8 *(C1 = ⓐ "⛔ đổi mẫu số")*; dòng 2026-09…11 đo nhưng ⛔ phán.
- **G5** ghép sổ ↔ canon = luật `ghep_bang` của ảnh tháng 8 *(5 trường + seq trùng theo hàng sheet)*, chạy lại bằng mã thay cho ảnh kết quả ⛔ có mã sinh.
- **G6** khuôn ANH EM `_song` thay vì sửa khuôn DT13 tại chỗ — khuôn cũ còn là cổng của ảnh 22/11 biên bản.
