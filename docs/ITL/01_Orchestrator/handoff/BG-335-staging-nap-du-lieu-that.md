# BG-335 — bàn giao `WO-334` *(STAGING bước 05: nạp DỮ LIỆU THẬT — sổ · PM · 68 dòng chảy · Mapping Master · ảnh chụp 60 sao kê)*

| | |
|---|---|
| **Thuộc** | `WO-334` |
| **Phát bởi** | `fls-dev` làn **DATA** · phiên cloud Sonnet 5.5 · cụm PG **5436** · 2026-11-23 |
| **Nhận** | `fls-test` *(R1 → `KQ-336`, R2 cuối → `KQ-337`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/STG-NAP` @ `608e35f` *(mã + bài + README + UAT + sàn + BG; đã đẩy; `441f765` là mốc mã đầu)* — nền = ngọn `isp/STG` `1a94247` |
| **Kho thật** | `KHONG_CHAM` — ⛔ vào GCP/Cloud SQL · ⛔ ghi `fls-pg-1` *(cổng 5433; công cụ TỪ CHỐI `PG_DSN` cổng 5433 — bài ghim)* · ⛔ ghi sheet. Mọi phép ghi ở kho scratch `fls_stg_*` của cụm 5436 phiên |

## Kết luận một dòng
**Mã xong, chứng minh ĐỎ-khi-hỏng; chạy live bằng SA chỉ-đọc cho ra 3 phát hiện NGUỒN mà chủ phải quyết** — ⛔ phải lỗi script: *(1)* SA của phiên **403** trên cả hai workbook sao kê *(Bank · Quỹ)* ⇒ bước ① `68 dòng chảy` và ④ `chụp 60 sheet` **DỪNG có tên**; *(2)* cổng đọc-đủ ĐỎ ở cột `T · CDT1` *(3.056 < sàn 3.300; đọc theo HÀNG = theo CỘT)* ⇒ sổ **⛔ được ghi**; *(3)* so với ảnh đóng băng: PM mất **0** dòng nhưng `hd`/`cdt1`/`status`/`ref` bị sửa ở **117/534/29/30** dòng; bank bị **sắp lại/chèn dòng** *(7.545 dòng lệch vị trí)* và **37/9.992** bộ ba `(ref,cur,tiền)` không còn theo nội dung.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/staging/cred_sheets.py` *(mới)* | AC-2: **một chỗ** lấy token Sheets — `FLS_SHEETS_TOKEN` · khoá SA (`FLS_SHEETS_SA_JSON_TEP` đường dẫn · `FLS_GSHEETS_SA_JSON(_B64)`) · ADC · ⛔ không khai ⇒ đường cũ `gcloud --account <SA máy chủ>` *(tương thích)*. Phạm vi `spreadsheets.readonly` + `drive.metadata.readonly`. Gốc API đổi được (`FLS_SHEETS_API_GOC`) cho bài thử |
| `tools/do_hinh_dang.py` · `nap_that.py` · `nap_mapping_master.py` *(sửa nhỏ)* | `token()`/`_token()` + gốc API đi qua `cred_sheets` *(⛔ sửa hành vi khác)*. `nap_that.main` **tách** thành `chay_that(tok, ghi=…)` *(trả số đếm; cổng đọc-đủ ĐỎ vẫn ĐO, ⛔ ghi)* + `CongDocDuDo` mang bằng chứng; `main()` giữ hành vi cũ |
| `tools/staging/nap_nguon_that.py` *(mới)* | AC-2/3: điều phối mỏng 4 bước theo thứ tự phụ thuộc, BÁO CÁO có `mong` · mẫu số · nhãn đếm-gì · quyền đọc từng workbook · CŨ ↔ HIỆN TẠI |
| `tools/staging/05_nap_nguon_that.sh` *(mới)* | AC-2: Cloud Shell + Auth Proxy bằng `fls_ghi`; `--sa-json-tep` · `--adc` · `--token-gcloud`; `--kiem`; đòi `FLS_CHO_GHI_THAT=1` |
| `tests/staging/sheets_gia.py` · `test_05_nap_nguon_that.py` *(mới)* | máy chủ Sheets GIẢ HTTP thật + **18 bài** *(PG thật, kho scratch)* |
| `tools/staging/README.md` · `docs/ITL/04_Test/UAT_STAGING_E2E.md` v0.2 | AC-6: bước 05, quyền đọc sheet, đọc BÁO CÁO; UAT §1b số mong khi có dữ liệu thật |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | AC-6: `MONG_PYTEST_TOAN_BO` **4868 → 4886** + bài ghim cùng commit *(đo `pytest --collect-only -o addopts=` = 4886; web giữ 690)* |

⛔ **Không sửa**: `fls/**` *(0 tệp — `git diff 1a94247 -- fls \| wc -l` = 0)* · tuyến/bảng tuyến · luật cửa · tệp của `WO-325` *(chỉ **đọc** `04_nap_du_lieu.sh`, `nap_cau_hinh_ix.py`)*. `pip install google-auth requests` chỉ vào `.venv` phiên và venv của script 05 — `requirements.txt` ⛔ đổi.

## 1 · AC-1 — công cụ nạp nguồn đang dùng ở máy chủ *(đo trước — Đ1: grep `docs/` LẪN `fls/` + `tools/`)*
| Thứ tự | Công cụ | Đọc từ | Ghi vào | Số mong đã đo *(nhãn đếm gì)* |
|---|---|---|---|---|
| ① | `tools/nap_nguon_va_khai.py --that` | 2 workbook sao kê: sổ Bank `1zJA0M…` · sổ Quỹ `1RmmkO…` — tên sheet `R \|` + **dòng 1** | `fls_source` · `fls_khai_cot` | **68** dòng chảy *(60 ngân hàng + 8 quỹ)* · **408** dòng khai = 68 × 6 *(`03_IMPLEMENTATION_PLAN` task 7, 08/09)* |
| ② | `tools/nap_mapping_master.py --ghi` | RAW `1md85t…` tab `Mapping Master` | `fls_mapping_master` *(thay trọn; ⛔ nạp rỗng)* | **73** mã `hd` *(tài liệu; live 23/11 = 73 ✓)* |
| ③ | `tools/nap_that.py --that` | RAW tab `Transaction Mapping L1` (A…AL, từ dòng 5) + `[Importrange]PM_Unpivot` | `fls_itl` · `fls_reject` · `fls_pm_line` | sổ **9.967** dòng · **23** kỳ · parity **69.510/69.510** ô *(`voi_so_luong.tong`)*; lần nạp 26/08 *vào 10.100 = sổ 9.973 + loại 19 + rỗng 108*; ảnh canon **9.992** dòng; PM **3.703** dòng · **3.173** có mã |
| ④ | `tools/chup_sao_ke.py --that` | workbook Bank, vùng CHUẨN của 60 sheet `R \|` | `fls_chup` · `fls_chup_nguon` · `fls_chup_dong` | **60** nguồn · **8.368** dòng · **10** nguồn ra 0 dòng *(`03_IMPLEMENTATION_PLAN` task 9, 08/09)*; chặng 1 `8.338/8.338` |
| *(04)* | `tools/staging/nap_cau_hinh_ix.py` *(WO-325)* | ảnh `tests/fixture/cau_hinh/` | `fls_cau_hinh_*` | 9 bảng `IX.*` *(BG-326)* |
| **⛔ không có** | **H1000 · nền tảng (CCR/Platform) · FPS** | — | — | `grep -rli h1000 fls tools --include=*.py` = **17** tệp, trong đó **3** có `psycopg`/`INSERT INTO` *(`fls/bao_cao/gl.py` · `tools/do_hd2_c5a.py` · `tools/do_hd2_c3c.py` — gói ĐO HD2/báo cáo, ⛔ bộ nạp)* ⇒ **0 công cụ nạp**; `fps_` ở `fls/`+`tools/` = **5** chỗ, đều **chú thích** "FLS chỉ ĐỌC (`QĐ-ITL-45`)". ⇒ **ngoài phạm vi 05**, cần WO riêng nếu chủ muốn *(chúng chỉ vào HD2 qua ảnh đóng băng `tests/fixture/dau_vao`)* |

## 2 · Bằng chứng từng AC
| AC | Mong | Bằng chứng của Dev *(số đo thật, nhãn đếm gì — Đ4)* |
|---|---|---|
| **AC-1** | liệt kê đủ công cụ + thứ tự + bảng đích + số mong | **XONG** — bảng §1 *(4 công cụ nạp nguồn + 04; H1000/nền tảng/FPS: 0 công cụ — đo, ⛔ giả định)* |
| **AC-2** | `05_nap_nguon_that.sh`: Cloud Shell + Auth Proxy + `fls_ghi`; Sheets chỉ-đọc, xác thực ⛔ gắn cứng; đòi `FLS_CHO_GHI_THAT=1`; ⛔ ghi sheet; chạy lại ⛔ nhân đôi | **XONG, chưa chạy ở GCP** *(⛔ vào GCP)*. Bài `test_05_sh_*` ×3: từ chối đúng luật **TRƯỚC mọi lệnh gcloud** *(6 ca: thiếu cổng ghi · thiếu/xấu `--nguoi-nap` · chưa khai cách cấp quyền · hai cách cùng lúc · tệp khoá ⛔ tồn tại — exit 2, `gcloud.log` rỗng)*; `--kiem` chỉ đọc bí mật `fls_ghi`; nạp thật qua proxy GIẢ + `fls_ghi` THẬT; chạy lại ⇒ `fls_source` 4 · `fls_khai_cot` 24 · `fls_mapping_master` 6 **không đổi**. `fls_itl` chạy lại: bài `test_CHAY_LAI…` **9.985 → 9.985** *(lần 2 ⛔ nhân đôi)*. Máy chủ Sheets giả đếm **0** yêu cầu ≠ GET + bài quét mã *(7 tệp: ⛔ `POST/PUT/PATCH/DELETE` · `:append` · `values:update` · `:batchUpdate`)* + phạm vi chỉ-đọc ghim |
| **AC-3** | BÁO CÁO khớp 100 % `mong`; lệch 1 dòng ⇒ ĐỎ có tên; ⛔ đo ⇒ ĐỎ; mẫu số ≠ 0; ĐỎ hai chiều | **XONG** — mỗi hàng có `mong`; mẫu số ≠ 0 đứng cạnh *(`True`)*; ĐỎ **chứng minh** ở bài: sửa **1** ô tiền bank ⇒ `LỆCH tien = 1` + `bộ ba mất = 1`, **chỉ** trường ấy đỏ · xoá 1 dòng PM + sửa 1 `hd` ⇒ `pm_mat 1` · `pm_lech_hd 1` · `pm_lech_tien 0` · thêm 1 dòng ⇒ `MỚI = 1` (⛔ đỏ) · hạ sàn đọc-đủ về thật ⇒ ĐỎ + `fls_itl = 0` · **403** ⇒ ĐỎ `HTTP … 403` + bước DỪNG, sổ vẫn nạp **9.985** |
| **AC-4** | `Email Address` ⛔ vào kho; `Tên tài khoản` GIỮ; BÁO CÁO chỉ số đếm | **XONG** — nguồn giả có cột `Email Address` ⇒ kho **0** khoá `Email Address` trên **3.703** dòng PM *(mẫu số — Đ3)*, `Tên tài khoản` GIỮ **3.703/3.703**; BÁO CÁO ⛔ chứa email/tên/tiền/mã/token/mật khẩu giả *(bài `test_BAO_CAO_chi_so_dem…`)*. **Chứng ĐỎ:** gỡ `Email Address` khỏi `pm_join.PM_COT_RIENG_TU` ⇒ bài ĐỎ *(đã làm, trả nguyên)*; thêm cột `Email Address` vào kho ⇒ ĐỎ `cột tên có 'email' = 1`. `quet_pii_repo`: **[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp** |
| **AC-5** | chuỗi HD2 + `do_voi_so_luong.py` đọc kho staging ⇒ số khớp `voi_so_luong.json`/`hd2_cong.json` | **XONG, với 2 chỉnh phiếu** *(Đ1)*: **(a)** `tools/do_voi_so_luong.py` ⛔ đọc kho — `grep -c "psycopg\|PG_DSN"` = **0** / 809 dòng; nó chạy lên **ảnh đóng băng** ⇒ chạy nguyên: `Σ 9967 · 9845 · 3341 · 2700 · 30756 · 22290 · 112 · 13 · 69510/69510 · PM 3703/2426/3173 · bank 9992/105/6532` = đúng `voi_so_luong.json`. **(b)** chuỗi HD2 *(10 gói `do_hd2.py --goi`)* trên kho scratch + config 04 *(9 bảng `IX.*` ĐẠT)* = **10/10 `KẾT: DAT`**; chạy `--ghi` rồi so `hd2_cong.json`: **2 dòng khác — cả hai là nhãn nguồn dạng chữ** `nguon_ngay_dau` *("bai-test-h6…" → "staging-04 · IX.PER kho…")*, **0 con số khác** *(đã `git checkout` trả nguyên)* ⇒ HD2 chỉ cần config, ⛔ cần sổ |
| **AC-6** | README + UAT + `--duong-nen` ĐẠT + nâng sàn cùng commit | README bước 05 + UAT v0.2 §1b ✓ · sàn **4868 → 4886** + bài ghim cùng commit `441f765` ✓ · `--duong-nen`: **`KẾT: ĐẠT`** @ `608e35f` *(lần 3)*: toàn bộ **12 failed + 14 errors + 2 xfailed = 28 node id = `duong_nen_bai_do.txt` (thêm 0 · bớt 0)**, chạy **4.886** bài *(≥ sàn 4.886)*, skipped 0; `tests/web` 3 = 3, chạy 690. ⚠ Hai lần đầu ĐỎ do **bài của tôi**: lần 1 *(`4886` bài, thêm 2 node id)* — bài `test_05` viết DSN kho thật + `API` bị chốt lúc nhập khi chạy trọn bộ; lần 2 *(skipped 1)* — bài 5433 để `PG_DSN` sai lúc dọn. Cả hai đã sửa + chạy lại |
| **AC-7** · dữ liệu CŨ | phát lại ảnh vào kho test ⇒ khớp 100 % số đã đo, lệch 0 | **XONG** *(`test_CU_phat_lai_anh…`, nguồn GIẢ dựng từ `pm_join.json`)*: sổ đọc **9.992** · PM **3.703** · có mã **3.173** · bậc thang ghép `A 2.272 · B 29 · C 400 · D 27 · E 199 · F 428` + `không mã 105` + `không thấy mã PM 6.532` = `voi_so_luong.bank_tong` **từng số**; CŨ↔HIỆN TẠI: mất 0 · lệch 0 · mới 0 *(14 phép)*; kho: `fls_itl` **9.985** + `fls_reject` **7** = **9.992** *(7 = đúng số dòng ảnh có tiền 0, tầng sổ loại "PS Nợ và PS Có")*; `fls_pm_line` **3.703**. ⚠ **Giới hạn đã đo:** ảnh commit ⛔ có lưới thô 38 cột *(chỉ `dong · ref_tho · cur · tien` + 8 trường PM)* ⇒ ngày · tài khoản là **TỔNG HỢP**; ⛔ khẳng định gì về số theo kỳ ở đây. **60 sheet `R \|` ⛔ có ảnh** ⇒ bước ①④ thử trên 4 sheet tổng hợp *(cơ chế, ⛔ số liệu)* |
| **AC-8** · dữ liệu THẬT hiện tại | đọc live bằng SA chỉ-đọc vào PG cục bộ ⇒ Σ nguồn = Σ kho; kỳ chốt = cũ; kỳ mới đếm riêng | **ĐÃ CHẠY (23/11), kết quả ĐỎ CÓ TÊN — đúng thứ phiếu dặn phải báo**: §3 *(BÁO CÁO dán nguyên)* và §4 *(bảng cũ ↔ hiện tại)*. Ghi được vào kho phiên: **Mapping Master 73/73** *(Σ nguồn = Σ kho ✓)*. **Không** ghi được: sổ/PM *(cổng đọc-đủ ĐỎ)*, ① và ④ *(403)* ⇒ "Σ nguồn = Σ kho" **chưa đo được** ở đó |

## 3 · BÁO CÁO live — 23/11, SA chỉ-đọc, kho scratch `fls_stg_that_wo334` *(chỉ SỐ ĐẾM; ⛔ tên người/số TK/tiền dòng)*
Đường xác thực: `sa-env-b64` *(giá trị ⛔ in)* · checksum `sha256[:16]` của JSON số đếm = `90598dd8bf6f966d` · của văn bản dưới = `39dc222e4d0bb928` *(**15** mục ĐỎ · **16** ĐẠT)*.
```
── 0 · THÔNG TIN
   đường thông tin xác thực Sheets (⛔ giá trị)                                     sa-env-b64
   chế độ                                                                          NẠP

── 0b · QUYỀN ĐỌC từng workbook nguồn (HTTP; ⛔ nội dung)
   [ĐẠT] HTTP đọc workbook RAW (sổ ITL · PM · Mapping Master)                        200  (mong 200)
   [ĐỎ] HTTP đọc workbook BANK (60 sheet `R |` ngân hàng)                           403  (mong 200)
   [ĐỎ] HTTP đọc workbook QUỸ (8 sheet `R |` quỹ)                                   403  (mong 200)

── bước khai
   [ĐỎ] bước khai chạy được — DỪNG vì ⛔ quyền đọc workbook BANK+QUỸ                 None  (mong 'đo được')

── ② Mapping Master (nap_mapping_master)
   NGUỒN: mã `hd` đọc được (đếm)                                                   73
   NGUỒN: dòng bị loại (đếm, mỗi cái có lý do)                                     0
   NGUỒN: cần phân bổ / có phương pháp (đếm)                                       23 / 21
   [ĐẠT] mẫu số: mã đọc được ≠ 0                                                     True  (mong True)
   [ĐẠT] KHO: `fls_mapping_master` (đếm) = Σ nguồn đọc được                          73  (mong 73)

── ③ sổ ITL + PM (nap_that.chay_that)
   NGUỒN `Transaction Mapping L1`: dòng đọc (đếm)                                  14265
      = canon (đếm)                                                                12601
      + loại có lý do (đếm)                                                        121
      + rỗng (đếm)                                                                 1543
   [ĐẠT] mẫu số: dòng đọc ≠ 0                                                        True  (mong True)
   [ĐẠT] ba đường adapter cân (vào = canon + loại + rỗng)                            True  (mong True)
   NGUỒN `[Importrange]PM_Unpivot`: dòng đọc (đếm)                                 3909
      trong đó có mã tham chiếu (đếm)                                              3369
   [ĐẠT] mẫu số PM ≠ 0                                                               True  (mong True)
   [ĐẠT] bốn đường ghép PM cân                                                       True  (mong True)
   cổng đọc-đủ · S · Budget Code (hd): theo HÀNG / theo CỘT / sàn                  3422 / 3422 / 3300
   cổng đọc-đủ · H · Payment Type: theo HÀNG / theo CỘT / sàn                      3549 / 3549 / 3300
   cổng đọc-đủ · T · CDT1: theo HÀNG / theo CỘT / sàn                              3056 / 3056 / 3300
   cổng đọc-đủ · AB · svc_start: theo HÀNG / theo CỘT / sàn                        2525 / 2525 / 2300
   cổng đọc-đủ · AC · svc_end: theo HÀNG / theo CỘT / sàn                          2518 / 2518 / 2300
   cổng đọc-đủ · Y · ID Payee: theo HÀNG / theo CỘT / sàn                          463 / 463 / 400
   [ĐỎ] cổng đọc-đủ (nguồn có đủ ô so với sàn đã đo 27/08)                          False  (mong True)
      ⛔ lý do cổng: cot T · CDT1: 3056 o co gia tri, duoi nguong san 3300 — nguon thieu hoac lan doc thieu  ĐỎ
   [ĐỎ] KHO: sổ ĐÃ ghi (cổng đọc-đủ/ba đường chặn ⇒ ⛔)                              False  (mong True)

── ⓑ CŨ (ảnh đóng băng) ↔ HIỆN TẠI (nguồn sống)
   [ĐẠT] mẫu số: dòng bank trong ảnh (đếm)                                           9992  (mong 9992)
   [ĐỎ] dòng bank ảnh ⛔ còn ở đúng số dòng nguồn (MẤT, đếm)                         12  (mong 0)
   [ĐỎ] dòng bank ảnh LỆCH `ref` ở nguồn sống (đếm)                                 7550  (mong 0)
   [ĐỎ] dòng bank ảnh LỆCH `cur` ở nguồn sống (đếm)                                 2975  (mong 0)
   [ĐỎ] dòng bank ảnh LỆCH `tien` ở nguồn sống (đếm)                                7545  (mong 0)
   [ĐỎ] bộ ba (ref,cur,tien) của ảnh ⛔ còn ở nguồn sống — SO THEO NỘI DUNG, bỏ vị trí (đếm)  37  (mong 0)
   MỚI — dòng canon nguồn sống ⛔ có trong ảnh (đếm, nhãn riêng)                    2621
   [ĐẠT] mẫu số: dòng PM trong ảnh (đếm)                                             3703  (mong 3703)
   [ĐẠT] dòng PM ảnh ⛔ còn ở đúng số dòng nguồn (MẤT, đếm)                           0  (mong 0)
   [ĐỎ] dòng PM ảnh LỆCH `ref` ở nguồn sống (đếm)                                   30  (mong 0)
   [ĐẠT] dòng PM ảnh LỆCH `slip` ở nguồn sống (đếm)                                  0  (mong 0)
   [ĐẠT] dòng PM ảnh LỆCH `line` ở nguồn sống (đếm)                                  0  (mong 0)
   [ĐẠT] dòng PM ảnh LỆCH `cur` ở nguồn sống (đếm)                                   0  (mong 0)
   [ĐỎ] dòng PM ảnh LỆCH `status` ở nguồn sống (đếm)                                29  (mong 0)
   [ĐỎ] dòng PM ảnh LỆCH `hd` ở nguồn sống (đếm)                                    117  (mong 0)
   [ĐỎ] dòng PM ảnh LỆCH `cdt1` ở nguồn sống (đếm)                                  534  (mong 0)
   [ĐẠT] dòng PM ảnh LỆCH `tien` ở nguồn sống (đếm)                                  0  (mong 0)
   MỚI — dòng PM nguồn sống ⛔ có trong ảnh (đếm, nhãn riêng)                       206
   CŨ `voi_so_luong.pm_tong.so_dong_pm` ↔ HIỆN TẠI PM đọc                          3703 ↔ 3909
   CŨ `bank_tong.dong_bank` ↔ HIỆN TẠI canon                                       9992 ↔ 12601
   HIỆN TẠI canon thuộc kỳ ĐÃ CHỐT trong ảnh (23 kỳ; đếm)                          10187
   HIỆN TẠI canon thuộc kỳ MỚI sau ảnh (đếm, nhãn riêng)                           2414
   HIỆN TẠI canon ⛔ đọc được ngày (đếm)                                            0

── bước chup
   [ĐỎ] bước chup chạy được — DỪNG vì ⛔ quyền đọc workbook BANK+QUỸ                 None  (mong 'đo được')

── ⑤ RIÊNG TƯ (đếm; ⛔ in nội dung)
   MẪU SỐ — cột của kho (đếm)                                                      208
   [ĐẠT] cột tên có 'email' (đếm, ⛔ vào kho)                                         0  (mong 0)
   [ĐẠT] dòng PM mang khoá `Email Address` (đếm)                                     0  (mong 0)
   mẫu số PM trong kho (đếm; 0 ⇒ phép trên ⛔ chứng minh gì — Đ3)                   0

── Z · THỜI GIAN
   giây (đo)                                                                       13.8

══ KẾT: ĐỎ — 15 mục khác mong
```

## 4 · Dữ liệu CŨ ↔ dữ liệu THẬT hiện tại — theo nguồn/kỳ *(chỉ số đếm; nhãn đếm gì)*
| Nguồn · đại lượng | CŨ *(ảnh 26–27/08)* | HIỆN TẠI *(live 23/11)* | Kết luận |
|---|---|---|---|
| `Transaction Mapping L1` · dòng sheet đọc | 10.100 *(nạp 26/08)* | **14.265** | +4.165 dòng |
| · canon *(sau adapter)* | 9.992 *(ảnh)* | **12.601** *(loại 121 · rỗng 1.543)* | +2.609 |
| · **kỳ ĐÃ CHỐT** *(23 kỳ 2024-10…2026-08)*, dòng canon | — *(ảnh ⛔ có ngày)* | **10.187** | ảnh ⛔ có ngày ⇒ ⛔ có số CŨ cùng nhãn để so |
| · **kỳ MỚI** *(sau 2026-08)*, dòng canon | 0 | **2.414** = `2026-09` **702** · `2026-10` **991** · `2026-11` **721** | MỚI — đếm riêng |
| bank — dòng ảnh còn ở **đúng số dòng** *(khoá = số dòng sheet)* | 9.992/9.992 | mất **12** · lệch `ref` **7.550** · `cur` **2.975** · tiền **7.545** | ĐỎ: sheet bị **sắp lại/chèn** dòng |
| bank — bộ ba `(ref,cur,tiền)` của ảnh còn ở nguồn *(so theo **nội dung**, bỏ vị trí)* | 9.992/9.992 | còn **9.955**, mất **37** | ĐỎ có tên: **37** dòng ảnh đã bị sửa hoặc xoá sau chốt |
| bank — dòng canon ⛔ có trong ảnh | 0 | **2.621** | MỚI |
| PM — dòng sheet | 3.703 | **3.909** *(mới **206**)* | +206 |
| PM — dòng ảnh mất · lệch `slip`/`line`/`cur`/`tiền` | — | **0** · **0** | ĐẠT |
| PM — lệch `ref` · `status` · `hd` · `cdt1` | — | **30 · 29 · 117 · 534** dòng | ĐỎ: nguồn PM đã bị **sửa sau chốt** |
| PM — dòng có mã tham chiếu | 3.173 | **3.369** | — |
| bậc thang ghép PM `A·B·C·D·E·F` *(dòng)* | 2.272·29·400·27·199·428 | 2.438·30·404·27·201·438 | — |
| · không có mã · không thấy mã PM *(dòng)* | 105 · 6.532 | 100 · 8.963 | — |
| `Mapping Master` mã `hd` | 73 *(tài liệu)* | **73** · loại 0 · cần phân bổ 23 · có phương pháp 21 | ĐẠT *(Σ nguồn = Σ kho 73/73)* |
| 60 sheet `R \|` · dòng chụp · nguồn 0 dòng | 60 · 8.368 · 10 *(08/09)* | ⛔ **403** | ⛔ đo được |
| cổng đọc-đủ `T · CDT1` *(ô có giá trị)* | 3.339 *(27/08)* · sàn 3.300 | **3.056** *(theo HÀNG = theo CỘT)* | ĐỎ: ⛔ phải đọc thiếu — nguồn **mất ≥ 283 ô** `CDT1` dù lớn thêm |

## 5 · Phát hiện *(đo, ⛔ giả định — Đ1: đo ở CẢ HAI nơi)*
| # | Phát hiện | Đo | Hệ quả / việc của ai |
|---|---|---|---|
| 1 | **SA của phiên ⛔ đọc được hai workbook sao kê** | `GET …/spreadsheets/<id>?fields=spreadsheetId`: RAW `1md85t…` **200** · ADJUSTED `1r4Wem…` **200** · Bank `1zJA0M…` **403** · Quỹ `1RmmkO…` **403** | ①④ DỪNG có tên (BÁO CÁO mục `HTTP đọc workbook`). **Chủ:** chia sẻ "Người xem" workbook Bank + Quỹ cho SA đọc-sheet *(cả SA của phiên lẫn danh tính đọc-sheet dùng ở staging)* |
| 2 | **Cổng đọc-đủ ĐỎ trên nguồn sống** | `T · CDT1` **3.056** ô < sàn **3.300** *(đo 27/08: 3.339)*; theo HÀNG **=** theo CỘT *(⇒ ⛔ phải đọc thiếu)*; 5 cột kia ĐẠT *(S 3.422 · H 3.549 · AB 2.525 · AC 2.518 · Y 463)* | sổ ⛔ ghi. ⛔ **Tôi ⛔ hạ sàn** ("ai hạ con số này để cho qua là đang tắt cổng" — `doc_du.py:97`). **BA/chủ quyết:** nguồn mất giá trị `CDT1` có chủ ý, hay sàn cần đo lại có bản khai |
| 3 | **Nguồn đã bị sửa/sắp lại sau ảnh** | §4 | "kỳ đã chốt = dữ liệu cũ" **⛔ đúng** ở PM `hd`/`cdt1`/`status`/`ref` và 37 bộ ba bank; **chủ quyết** nguồn nào là chuẩn trước khi UAT đọc số |
| 4 | **`do_voi_so_luong.py` ⛔ đọc kho** *(phiếu giả định có)* | 0 lời gọi `psycopg`/`PG_DSN` | AC-5 chỉnh như §2; ⛔ việc cho bước 05 |
| 5 | **Công cụ cũ vẫn ĐÚNG ở máy chủ, nhưng ⛔ ở Cloud Shell nếu không có `cred_sheets`** *(BG-326 #6)* | nay đi qua `cred_sheets` — bài `test_cac_cong_cu_nap_di_qua_MOT_cho_lay_token` | — |
| 6 | **`kiem_so_song.py` · `dong_bo_so_song.py`** gọi `.venv/Scripts/lint-imports.exe` *(đường Windows)* ⇒ `FileNotFoundError` trên Linux | chạy `kiem_so_song`: `No such file …/.venv/Scripts/lint-imports.exe` | đã có từ BG-326 #7; ⛔ sửa ở đây *(ngoài phiếu)*; còn đòi kho có sổ thật |
| 7 | **`khop_owner.py --kiem` ĐỎ ở nền** *(`A1`/`B1`/`C6` "đổi trạng thái" + khối lộ trình lệch bản sinh lại)* | chạy **trước và sau** thay đổi của tôi trên cùng `PG_DSN`: **cùng** đầu ra, exit 1 | **có sẵn ở nền** `1a94247`, ⛔ do WO-334 |
| 8 | Nguồn sống tải **chậm khi nguội**: đọc tiêu đề `A3:AL3` lần đầu **30,4 giây** *(2 lần timeout 45 s rồi OK)*; cả lượt ③ ~2 phút lần đầu, ~14 giây khi ấm | `nap_that._lat` retry 3 lần | chủ chạy lúc workbook nguội ⇒ có thể thấy `lan 1/3 LOI TimeoutError` — **bình thường** |

## 6 · Cổng `CLAUDE.md` *(dán thật)*
```
=== docs/ITL/_tools/kiem_tai_lieu.py
OK K5 khong ngay CHUA XAY RA       (da do: 968 o ngay)
OK K6 ma QD khong bi cap hai lan   (da do: 104 ma)

✅ cong tai lieu DAT — va no da do duoc that (486 file, 2965 bang, 968 o ngay, 104 ma QD), khong chi 'khong thay loi'
rc=0
=== docs/ITL/_tools/khop_owner.py --kiem
   · A1 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH — mot cho DANG KHOP vua vo
   · B1 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH — mot cho DANG KHOP vua vo
   · C6 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH — mot cho DANG KHOP vua vo
   · ⛔ khoi trong lo trinh LECH voi ban sinh lai ⇒ chay lai ⛔ khong co `--kiem`
rc=1
=== tools/soi_bang_tuyen.py
OK /api/fls/v1/config/alr
OK /api/fls/v1/config/drv

✅ ban khai KHOP SQL that o ca 49 tuyen
rc=0
=== tools/kiem_thuyet_minh.py
  · Ban-ve-TOBE-Man-Ghep-PM.html

✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban
⚠ Cong nay chi biet nut CO duoc nhac den, ⛔ KHONG biet dong ay co DUNG hay khong.
rc=0
=== tools/quet_pii_repo.py
  [không đọc · khai theo đuôi] docs/ITL/01_Orchestrator/handoff/anh_BG-254/f5_sau_ky_cuon.png
  [không đọc · khai theo đuôi] docs/ITL/01_Orchestrator/handoff/anh_BG-254/f5_truoc_ky.png
  giữ (⛔ chắc cá nhân; chỉ đếm): cho=46 ref=26 tk=1 · số_vừa_CN_vừa_pháp_nhân=0
[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp
rc=0
=== tools/kiem_so_song.py
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/subprocess.py", line 1992, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.venv/Scripts/lint-imports.exe'
rc=1
```
- `python -m pytest tests/staging/test_05_nap_nguon_that.py` → **18 passed** *(+ `test_khong_ai_tro_lai_kho_that` · `test_uat_doc` xanh)*. `lint-imports`: **11 kept, 0 broken**. `pg_migrate`: "khong co gi de ap · pg_verify: khop".
- `python -m pytest` toàn bộ + `--duong-nen`: **`KẾT: ĐẠT`** @ `608e35f` *(lần 3)*: toàn bộ **12 failed + 14 errors + 2 xfailed = 28 node id = `duong_nen_bai_do.txt` (thêm 0 · bớt 0)**, chạy **4.886** bài *(≥ sàn 4.886)*, skipped 0; `tests/web` 3 = 3, chạy 690. ⚠ Hai lần đầu ĐỎ do **bài của tôi**: lần 1 *(`4886` bài, thêm 2 node id)* — bài `test_05` viết DSN kho thật + `API` bị chốt lúc nhập khi chạy trọn bộ; lần 2 *(skipped 1)* — bài 5433 để `PG_DSN` sai lúc dọn. Cả hai đã sửa + chạy lại
- ⛔ **không chạy được ở phiên này:** `kiem_so_song.py` · `dong_bo_so_song.py` *(Windows path + kho thật — #6)*.

## 7 · Kho thật
`KHONG_CHAM`. Cụm phiên `localhost:5436`; kho scratch `fls_stg_that_wo334` *(giữ cho `fls-test` soi: `fls_mapping_master` 73 · config `IX.*` 10 phiên bản · `fls_itl` 0)* và `fls_stg_n5_<pid>`/`fls_stg_<pid>` của bài thử *(tự dọn)*. Bản thô `/tmp`: **không có** *(công cụ ⛔ ghi thô ra đĩa; BÁO CÁO/JSON chỉ số đếm ở scratchpad phiên, chmod 700)*.

## 8 · Cách chạy để xem
- Bài thử: `PG_DSN=… pytest tests/staging/test_05_nap_nguon_that.py` *(~65 giây)*.
- Chạy live chỉ-đọc: `PG_DSN=… FLS_GSHEETS_SA_JSON_B64=… python tools/staging/nap_nguon_that.py --kiem` *(⛔ in khoá)*.
- Chủ ở Cloud Shell: `bash tools/staging/05_nap_nguon_that.sh --project fp-a-project --kiem --token-gcloud` rồi bỏ `--kiem` + `FLS_CHO_GHI_THAT=1 … --nguoi-nap <tên.người>`.

## 9 · Dev tự thấy còn yếu *(Test soi chỗ này trước)*
1. ⛔ **Chưa chạy ở GCP** — các giả định của BG-326 §"Giả định chưa kiểm" vẫn nguyên; thêm: `fls_ghi` ghi được `fls_chup*`/`fls_mapping_master`/`fls_source` trên **Cloud SQL thật** *(đã chứng ở PG cục bộ qua 02b)*; `google-auth` cài được ở Cloud Shell *(script tự `pip install`)*.
2. **CŨ ↔ HIỆN TẠI bank so theo SỐ DÒNG** vì ảnh khoá theo số dòng; khi sheet bị chèn/sắp lại thì phép vị trí đỏ hàng nghìn dòng *(đúng, nhưng ồn)* — phép **theo nội dung** *(37)* mới là tín hiệu "sửa/mất". Chưa có phép gán dòng ảnh ↔ dòng sống theo khoá nghiệp vụ *(⛔ có khoá ổn định trong ảnh)*.
3. **Phát lại ảnh = nguồn TỔNG HỢP** về ngày/tài khoản; ⛔ chứng minh số theo kỳ, ⛔ chứng minh cổng đọc-đủ trên dữ liệu thật *(ở bài, sàn bị hạ về 0 bằng `monkeypatch` — chỉ để thử đường ống)*.
4. **Σ kho** của sổ dùng `fls_itl + fls_reject` *sau* nạp = canon + loại ⇒ **đúng khi kho CHỈ chứa nguồn này** (staging: kho trắng + 04 ⛔ ghi sổ). Chạy lại sau khi nguồn sửa dòng ⇒ ĐỎ *(đúng — chỉ-THÊM)*; ⛔ có đường "nạp bù".
5. `05` ⛔ nạp **config 04** — chủ phải chạy 04 trước *(thứ tự README)*; ⛔ kiểm trong script.
6. **Bước ① cần `fls_source` có `Platform`/`CCR`?** — ⛔: `nap_nguon_va_khai` chỉ `Bank|Cash`; H1000/nền tảng ngoài phạm vi *(§1)*.
7. Khoá SA tôi dùng là khoá của container *(⛔ in/commit/ghi tệp)*; ⛔ thay thế cho khoá staging của chủ.
