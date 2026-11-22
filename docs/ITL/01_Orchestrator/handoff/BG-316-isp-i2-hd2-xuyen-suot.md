# BG-316 — Bàn giao WO-315 · ISP Step 47 · I2 · Tích hợp HD2 xuyên suốt

| | |
|---|---|
| **Nhánh / commit** | `isp/I2` · bài ① `53bdf36` · nền = ngọn nhánh làm việc `3ea8052` *(có `WO-315` + H13 gộp `8c7f3df`)* + `isp/H14` `a6a2df2` + `isp/DT13` `ab831d7` *(tăng tốc ③)* |
| **Dải phiếu** | R1 `KQ-317` · R2 cuối `KQ-318` · số trống kế tiếp **319** |
| **Chạm** | `tests/tich_hop/test_hd2_xuyen_suot.py` (mới, **25 bài**) · sàn `tools/dung_moi_truong_isp.sh` + bài ghim `tests/test_dung_moi_truong_isp.py`. ⛔ sửa engine/tuyến · ⛔ mã nối trong `fls/`/`tools/` *(nối tỷ giá kho nằm TRONG bài — xem `I2-P2`)* · ⛔ chữ ký thật · ⛔ kho sống |

## Kết luận
Bài tích hợp xanh **25/25** *(~60 s)*. Chuỗi CA → SO → AL → RP với `fx_cua()` THẬT cho **ĐÚNG** số của 11 khối `hd2_cong.json` đã commit ở bước của gói *(10/11 khớp trọn; `WP-C5c` khớp mọi số ô, chỉ khác `dat` vì `H14-R2-01` chưa sửa ở ngọn H14 — ⛔ do I2, đo đối chứng)*. Bốn phát hiện ghi ở **Phát hiện**, ⛔ sửa. `--duong-nen` **ĐỎ** chỉ vì 6 bài của H14/DT13 *(5 = `H14-R2-01` · 1 = rào DT13 × H14)* — ⛔ bài nào do I2.

## Cách dựng (tầng — mỗi tầng là CHÍNH mã thật)
| | Tầng | Mã thật |
|---|---|---|
| ⓪ | kho TEST **riêng** `fls_test_i2` dựng lại từ 0 mỗi lượt *(ký tháng là MỘT CHIỀU — ⛔ huỷ ký, C7 `WO-212` ⇒ "bỏ ký 202510" = kho CHƯA có chữ ký 202510; `fls_test` chung có bài khác ký tháng ⇒ ⛔ dùng chung)*. Nạp IX.FX · IX.PER (21/10, A) · IX.ALR 17 luật MM **+ KÝ BẬT 2025** (`ix_alr_2025_bat.json`, `KhanhCQ`, quyết chủ 22/11) · IX.PL · IX.ORG · IX.VEN | `chc.nap_ix_fx` · `do_hd2_c5c.nap_nen_kho` · `chc.nap_ix_org` · `chc.nap_ix_ven` |
| ① | ký **37/37** tháng IX.FX *(202306 + 202401…202612)* qua `POST /config/fx/{t}/sign`, máy chủ thử, actor = thẻ test `i2.tich.hop@vi-du.invalid` ⇒ 37 × `201` | tuyến C7 `ky_thang_fx` |
| ② | 11 gói `tools/do_hd2*.py` `chay_wp_*` (dsn = kho riêng). Tỷ giá: `FxKho` = Mapping mà MỖI tháng đọc qua `chc.fx_cua(conn, tháng)`; thay `nap_fx` ở **4** chỗ gọi tên ấy (`do_hd2` · `c3c` · `c3d` · `c5b`); `IX_FX` trỏ tệp vắng ⇒ bài canh ảnh `ix_fx.json` **0** lần mở. Chuỗi đủ: **26** tháng đọc qua `fx_cua` (202410…202611) | `fls.repo.cau_hinh_repo.fx_cua` |
| ③ | `GET /gates` máy chủ thử, `tep_hd2` = tệp tạm ghi đúng hợp đồng `_ghi_cong` | `doc_bao_cao.doc_cong_hd2` |
| ④ | F03 node-vm (`man_f03.js` thật) + Chromium headless THẬT 390 px | `man_f03.js` |
| ⑤ | `bao["609"]` *(Daily Report 3 PL · `FS1_FS2_gop` · kỳ 202512 — đầu ra H14)* → `dua_ban_ky` → `ky_ban` | `chc.dua_ban_ky` · `chc.ky_ban` |

## I2-B1 · báo cáo HD2 theo gói *(chuỗi đủ — tỷ giá TỪ KHO đã ký)*
Nhãn (Đ4): **ô so** = `tong_o` (mẫu số của gói) · **khớp** = `khop` · **lệch có chủ đích** = `lech_co_chu_dich` (Σ lớp có tên) · **lệch FLS** = `lech_ngoai_ten` (ngoài tên — phải 0). Cột "= mong" = mọi khoá số có trong khối commit của bước gói *(`tong_o` · `khop` · `khop_co_so` · `o_co_so` · `o_0_0` · `so_o_dap_an_so_duoc` · `lech_*` · `o_so` · `dong_so` · `mau_so_thang` · `dat` + `lech_co_ten` · `mong_*`)* bằng nhau — bài `test_B1_goi_so_o_va_lech_bang_mong_da_khai[gói]`.

| Gói (bước) | ô so | khớp | lệch có chủ đích | lệch FLS | lệch theo lớp *(số ô / số hàng)* | dat | = mong |
|---|---|---|---|---|---|---|---|
| WP-C2 (H4) | 63.016 | 63.016 | — | 0 | `thieu_tien_te_D` 6 hàng · `itl_id_na` 4 · `ky_vang_406` 4 kỳ · `thang_thieu_ty_gia` 0 | true | ✓ *(ô so = `so_o_dap_an_so_duoc` 63.016)* |
| WP-C3a (H5) | 205.175 | 205.140 | 35 | 0 | `thieu_tien_te_D` 12 · `hd_ngoai_cay` 3 · `hd_alias` 2 · `hd_khac_hoa_thuong` 5 | true | ✓ |
| WP-C3b (H6) | 11.585 | 11.543 | 42 | 0 | như C3a + `o_khac_0_ky_khong_ngay` 0 | true | ✓ |
| WP-C3c (H7) | 888 | 835 | 53 | 0 | `thieu_tien_te_D` 462 · `hd_mac_dinh_oga` 20 · `cdt_la` 5 · `ky_suy` 3 · `chua_co_dau_vao` 3 | true | ✓ |
| WP-C3d (H8) | 1.289.415 | 1.287.624 | 1.791 | **0** | `as_is_416_GAC_thieu_CXA` 8 · `as_is_truoc_CA` 2 · `chua_co_dau_vao` 6 · `cot_ngoai_truc` 6 · `gl` 12 · `hr` 11 · `tu_kiem_*` 2+2 · `khong_so_duoc` 46.398 | true | ✓ *(WO: lệch FLS 0, AS-IS 1.791)* |
| WP-C4a (H9) | 420 | 420 | — | — | — | true | ✓ |
| WP-C4b (H10) | 1.981 | 1.981 | — | — | — | true | ✓ |
| WP-C4c (H11) | 19.894 | 19.591 | 303 | — | 303 có tên | true | ✓ |
| WP-C5a (H12, cờ 2025 BẬT) | 45.674 *(ô có số 11.764)* | 40.556 *(có số 6.646)* | 5.118 | 0 | `loi_as_is` 928 · `lech_D3` 3.099 · `chua_co_dau_vao` 1.091 · `as_is_truoc_CA` 675 · `as_is_tay_lan_du` 29 · `o_lech` 224 · `khong_so_duoc` 154 · `o_trong` 741 | true | ✓ *(đúng "Đã đo" WO-315)* |
| WP-C5b (H13) | 4.102 | 3.179 | 923 | 0 | `pl5_khong_tinh_duoc` 252 · `o_trong_dap_an` 192 · `khong_so_duoc` 14 · `lop_thua_ke` 5 | true | ✓ |
| WP-C5c (H14) | 84.770 *(có số 22.041)* | 76.292 *(có số 13.563)* | 8.478 | 0 | `lop_thua_ke` 12 · `chinh_tay_actor` 2 · `chinh_tay_trung_0_5` 2 · 605 DỪNG 0/13.706 *(`khong_do_duoc`)* | **false** | số ô ✓ · `dat` ✗ ⇒ `H14-R2-01` |

**WP-C5c:** mọi số ô = khối commit; `dat` = **false** *(commit: null)* vì 18 dòng `check.<607·608·609·610·615>.….NB = 0.dat_0_0 ↔ dat_co_so` — đúng `H14-R2-01` của `KQ-314` *(mong CHECK `NB = 0` chưa sinh lại sau H13-R1 `pla.check_atl`)*. **Đối chứng:** `python tools/do_hd2.py --goi WP-C5c --dsn …/fls_test_i2` *(tỷ giá ẢNH, ⛔ kho)* ra **y hệt** 18 dòng ⇒ ⛔ do tỷ giá kho. Bài ghim `MONG_H14_R2_01_CHUA_SUA = True` *(`test_C5c_H14_R2_01_…`)*: khi gộp ngọn H14 đã sửa ⇒ bài ĐỎ ⇒ đặt `False` ⇒ C5c/C5 mong `None`.

## I2-B2 · bỏ ký 202510
Kho ký 36/37 tháng *(thiếu 202510)* ⇒ chạy chuỗi:
- **8/11** gói nổ `FxChan` *(`WP-C2 · C3a · C3b · C3c · C3d · C5a · C5b · C5c`)*, lý do mỗi gói = `FX_CHAN 202510: tháng CHƯA ký (D1: owner ký mỗi tháng)`; tháng 202510 **⛔** có trong tập tháng đã đọc qua `fx_cua` ⇒ ⛔ số tỷ giá nào ra cho tháng ấy; các gói ấy ⛔ ra số nào *(cả lượt dừng)*.
- `GET /gates`: `HD2_WP_C2` **`dat = false`**, `ly_do` mang `FX_CHAN 202510`; cha `HD2_WP_C3` · `HD2_WP_C5` cũng false.
- 3 gói **⛔ đọc tỷ giá** *(C4a/b/c)* vẫn chạy ra số — `I2-P1`.

## I2-B3 · ký bản 2025-12
`dua_ban_ky(202512, bao["609"], actor="engine-h14-i2")` ⇒ phiên bản **1** `chua_ky` · `ky_ban(202512, actor=thẻ test)` ⇒ phiên bản **1** `da_ky`. `checksum` bản đưa = bản ký = `ban_ky.checksum(JSON ô)` = checksum nội dung đọc lại từ kho; nội dung kho = `chuan_hoa(JSON ô)` *(bài `test_B3_…`)*.

## I2-F1 · I2-F2 *(F03 · vm + Chromium 390 px)*
- **F1** *(chuỗi đủ)*: 4 thẻ cha `HD2 WP-C2/C3/C4` **✓ ĐẠT** có số *(`da_do`)*; thẻ **WP-C5**: chữ ISP I2-F1 đòi "có số, ⛔ KHÔNG ĐO ĐƯỢC" — **lệch có tên**: trạng thái ĐÚNG của C5 là **"⛔ KHÔNG ĐO ĐƯỢC" có lý do 605 chờ chủ ký "DỪNG có tên"** *(H14-R1-01 — ⛔ ép xanh)*. Ở cây này C5 còn **✗ KHÔNG ĐẠT** vì `H14-R2-01` *(lý do `NB = 0` trên thẻ)*; gộp ngọn H14 đã sửa ⇒ về "KHÔNG ĐO ĐƯỢC · 605" *(bài ghim tự ĐỎ để khai lại)*.
- **F2** *(bỏ ký 202510)*: thẻ `HD2 WP-C2` **✗ KHÔNG ĐẠT** + chữ `FX_CHAN 202510` *(vm + Chromium)*.

## Chứng minh ĐỎ (Đ5)
| Phá | Kết | Trả |
|---|---|---|
| `chc.fx_cua` bỏ kiểm chữ ký *(coi mọi tháng đã ký)* | **4 bài ĐỎ** (B2 ×2 · F2 vm · Chromium) | `cp` bản lưu — `git status` sạch |
| `man_f03.js` đổi chữ `KHÔNG ĐẠT` | **3 bài ĐỎ** (F1 vm · F2 vm · Chromium) | `git checkout` |
| Lượt đầu bài (ĐỎ trước) | 7 đỏ: mẫu số tháng 37 ≠ 36 *(202306)*, nhãn khớp C5a *(6.646 là ô CÓ SỐ)*, cấu trúc IX.ALR, C5c `H14-R2-01` | khai lại có nhãn |

## Phát hiện (⛔ sửa engine/tuyến — báo)
- **`I2-P1` (lệch giữa tầng · AL).** `WP-C4a/b/c` ⛔ đọc tỷ giá: đầu vào là ẢNH `gi_cfa1.json` *(36 dòng tháng 202510)* · `gi_mid3.json` *(19 dòng)* — số AS-IS **đã nhân tỷ giá sẵn** ⇒ tháng 202510 chưa ký vẫn ra số ở tầng AL. Chữ AC-2 "⛔ số nào ra cho tháng ấy ở MỌI tầng" ⛔ thoả ở AL cho tới khi AL đọc CFA1 do engine FLS sinh *(qua `fx_cua`)* thay ảnh. Bài ghim `MONG_GOI_KHONG_DOC_FX`.
- **`I2-P2` (nối tỷ giá kho ⛔ có ở mã).** `tools/do_hd2*.py` đọc tỷ giá từ ẢNH `ix_fx.json` (`nap_fx`, chú thích "⛔ đọc kho, I2"); ⛔ đường `--dsn` nào cho IX.FX; và ⛔ bắt `FxChan` *(CLI nổ thay vì ghi khối `dat=false` có lý do)*. I2 nối TRONG bài *(Mapping `FxKho` + thay `nap_fx` + bọc `FxChan` thành khối đỏ)* để ⛔ sửa engine. Câu cho orchestrator: có mở bước nối `fx_cua` vào `do_hd2` (và `hd2_cong.json` máy chủ) không?
- **`I2-P3` (tích hợp H14).** `H14-R2-01` *(KQ-314)* còn mở ở ngọn `a6a2df2` ⇒ C5c `dat=false` thay `null`. Ghim hiện trạng; gộp lại ngọn H14 khi orchestrator nhắn.

- **`I2-P4` (tích hợp H14 × DT13).** Rào DT13 `quet_tham_chieu("sign_off_dau_vao")` bắt `tools/do_hd2_c5c.py` — tệp H14 chỉ nhắc tên ấy trong câu CẤM dùng *(vòng tròn 605)*. Một trong hai phải đổi *(rào bỏ qua chú thích / H14 đổi chữ)* — việc của vòng sửa H14 hoặc DT13, ⛔ I2.

## Câu chủ đang mở (⛔ tự quyết)
- **D3** (`lech_D3` 3.099 ô WP-C5a) — chờ chủ.
- **CHECK IX.PL đỏ có chặn đóng sổ không** — chờ chủ *(I2 chỉ đếm, ⛔ chặn)*.
- **605 "DỪNG có tên"** (`DUNG_KY` rỗng) — chờ chủ; C5 giữ "KHÔNG ĐO ĐƯỢC".

## Cổng `CLAUDE.md` — kết quả thật (cụm 5435)
| Cổng | Kết quả |
|---|---|
| `pytest` toàn bộ (qua `--duong-nen`, MỘT lần, một mình) | 18 failed · 4.820 passed · 2 xfailed · 14 errors; chạy **4.854** = mong · skipped 0 · deselected 0. Tập đỏ **34** = 28 đường nền **+ 6** · bớt 0 — **cả 6 ⛔ do I2** *(xem dưới)* |
| ↳ +5 `tests/oracle/test_do_hd2_c5c.py` | `test_AC1_dat_va_mau_so_khai_truoc` · `test_AC5_hd2_cong_json_khoi_WP_C5c_khop_lan_do` · `test_AC5_kho_rong_DO_roi_nap_nen_DAT` · `test_R1_01_chu_ky_DUNG_co_ten_la_ngoai_le_duy_nhat` · `test_R1_01_cong_null_co_ten_khi_605_o_so_0_chua_ky` = đúng **5 bài `H14-R2-01`** mà `KQ-314` đo trên cây gộp *(`I2-P3`)* |
| ↳ +1 `tests/du_lieu/test_rao_dau_vao_dt13_r1.py::test_quet_ma_thuc_khong_co_tham_chieu_ngoai_khuon_va_rao` | rào DT13 bắt `tools/do_hd2_c5c.py` (H14) nhắc `sign_off_dau_vao` — chính là chú thích **cấm** dùng nó *(dòng 93 · 100)* — tích hợp H14 × DT13 *(`I2-P4`)* |
| `pytest tests/web` | 3 failed · 687 passed = **3 = 3** đường nền; chạy 690 ≥ 690 — ĐẠT |
| `--duong-nen` | **KẾT: ĐỎ** — chỉ vì 6 bài trên *(⛔ chạy lại: cả 6 nằm ở mã H14/DT13 mà I2 ⛔ được sửa ⇒ lần hai ra y hệt)*. Khi gộp ngọn H14 đã sửa `R2-01` + DT13×H14 ⇒ kỳ vọng về 28 = 28 |
| `lint-imports` | 11 kept · 0 broken |
| `kiem_tai_lieu.py` | ĐẠT *(sau BG này)* |
| `soi_bang_tuyen.py` | khớp SQL ở **49/49** tuyến |
| `kiem_thuyet_minh.py` | **35/35** nút — ĐẠT |
| `pg_migrate` | `pg_verify: khop` |
| `khop_owner.py --kiem` | ĐỎ — có sẵn ở nền *(như `I1-P3`: `fls_itl` rỗng ở cụm cloud)* |
| `kiem_so_song.py` | lỗi `FileNotFoundError .venv/Scripts/lint-imports.exe` (đường Windows — có sẵn, `I1-P3`); `dong_bo_so_song.py` ⛔ chạy |

## Sàn (Q8)
`MONG_PYTEST_TOAN_BO` **4764 → 4854** = thu thập thật cây gộp *(H14 + DT13 = 4.829)* + **25** bài I2; cùng bài ghim, cùng commit `53bdf36`. `MONG_PYTEST_WEB` **giữ 690** *(bài mới ở `tests/tich_hop`)*.

## Lệnh chạy lại trên máy chủ (owner · `fls-pg-1` · O4)
Bài ⛔ đọc/ghi kho THẬT `fls`: mọi ghi vào kho TEST **riêng** `fls_test_i2` *(tạo + DROP/CREATE bởi bài, cần role có `CREATEDB` — `fls` có)*. ⛔ đặt `PG_DSN_TEST` vào kho thật *(`dsn_test` từ chối)*.
```powershell
$env:PG_DSN='postgresql://fls:fls@localhost:5433/fls'
$env:PG_DSN_TEST='postgresql://fls:fls@localhost:5433/fls_test'
$env:PYTHONUTF8='1'
python -m pytest tests/tich_hop/test_hd2_xuyen_suot.py -p no:cacheprovider
```
- **Mong:** `25 passed` *(~1 phút; Chromium thiếu ⇒ 1 skipped `test_F1_F2_chromium_that`, còn 24 passed)*. ⚠ conftest phiên DROP/CREATE `fls_test` *(như mọi lượt pytest — ⛔ chạm `fls`)*.
- **Đọc kết quả:** `test_B1_goi_…[WP-Cx]` đỏ ⇒ gói x ra số khác khối `hd2_cong.json` commit *(lệch giữa tầng — dán diff)*; `test_B2_*` đỏ ⇒ chữ ký tháng ⛔ chặn; `test_C5c_H14_R2_01_*` đỏ sau khi gộp H14 đã sửa = **mong đợi** ⇒ khai lại `MONG_H14_R2_01_CHUA_SUA = False`.
- Dọn tuỳ chọn: `psql … -c 'DROP DATABASE fls_test_i2'` *(bài tự dựng lại lần sau)*.

---

## Vòng gộp lại H14 sau `KQ-314` (orchestrator nhắn 22/11 19:31)
Gộp `origin/…-isp/H14` **`4b49d00`** (`H14-R2-01` đã sửa: `mong` CHECK `NB = 0` của WP-C5c sinh lại; 615 ô so 12.380 → 13.760) + ngọn nhánh làm việc **`31ae77a`**. Xung đột chỉ ở sàn script + bài ghim ⇒ bản `isp/I2` rồi đặt = thu thập thật; `hd2_cong.json`/`do_hd2*.py` tự gộp *(mong C5c = bản H14 mới)*.
- **Bài ghim cắn đúng:** với `MONG_H14_R2_01_CHUA_SUA = True` ⇒ **5 bài ĐỎ** (B1[WP-C5c] · F1 cổng · `test_C5c_H14_R2_01_…` · F1 vm · Chromium) — C5 giờ `None`. Khai lại `= False` ⇒ **25/25** xanh.
- **Số đổi (chỉ WP-C5c):** ô so **84.770 → 86.150** *(+1.380 = 615: 12.380 → 13.760)* · khớp **76.292 → 77.672** · ô có số 22.041 → **22.893** · khớp có số 13.563 → **14.415** · lệch có chủ đích **8.478** (giữ) · lệch FLS **0** · `dat` **null** = khối commit H14 *(605 DỪNG 0/13.706 chờ chủ ký "DỪNG có tên")*. 10 gói khác **⛔ đổi số**.
- **I2-F1 nay đúng trạng thái:** thẻ C2/C3/C4 ✓ ĐẠT có số · thẻ **C5 "⛔ KHÔNG ĐO ĐƯỢC" có lý do 605** *(lệch có tên so với chữ ISP — ⛔ ép xanh)*. `I2-P3` **đóng**.
- **Sàn:** `MONG_PYTEST_TOAN_BO` **4854 → 4868** = thu thập thật cây gộp; web giữ **690**.
- **Cổng (cây gộp `387ab0c`, cụm 5435):** `--duong-nen` MỘT lần, một mình ⇒ **KẾT: ĐẠT** — toàn bộ 12 failed · 4.840 passed · 2 xfailed · 14 errors = tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy **4.868** = mong · skipped 0; web **3 = 3**, chạy 690. 6 bài đỏ thêm của lượt đầu *(5 `H14-R2-01` + 1 rào DT13 × H14 — `I2-P4`)* **hết** sau gộp ngọn H14 ⇒ `I2-P4` **đóng**. `lint-imports` 11 kept · 0 broken · `soi_bang_tuyen` 49/49 · `kiem_thuyet_minh` 35/35 · `kiem_tai_lieu` ĐẠT. `khop_owner --kiem` · `kiem_so_song` như trên *(có sẵn, `I1-P3`)*.
- **Phát hiện còn mở:** `I2-P1` (C4 ⛔ đọc tỷ giá) · `I2-P2` (`do_hd2` ⛔ nối `fx_cua`/⛔ bắt `FxChan`).
