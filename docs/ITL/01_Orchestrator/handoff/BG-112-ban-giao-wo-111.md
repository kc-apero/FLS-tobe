# BG-112 — bàn giao `WO-111` *(ISP 3.1.2 · Step 12 · DT4: ảnh đáp án 406 · CALC ZONE BM–BT)*

| | |
|---|---|
| **Thuộc** | `WO-111` |
| **Phát bởi** | `fls-dev` làn **DATA** *(phiên cloud · Opus 4.8)* · 2026-11-17 |
| **Nhận** | `fls-test` *(R1 `KQ-113` · R2 `KQ-114` · R3 `KQ-115`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/DT4` @ `afe1c0a` *(đã đẩy — mã + bài + ảnh)* · nền `cf5156e` *(DT3)* |

## Tóm tắt

Đóng băng **đáp án 406** cho bước H4 *(parity CA.GL ↔ 406, dòng × kỳ, 8 cột `BM…BT`)*: đọc bản sao
`Report I General Ledger` theo **lát kỳ** bằng khoá SA chỉ-đọc *(A·D·R·BM:BT — ⛔ phủ `B:C`)*,
dựng khuôn **tệp riêng** `gl_406`, và một ảnh `tests/fixture/dap_an/gl_406.json` *(7883 dòng,
checksum `e98f3a699e2de469`)* qua cổng `[ĐẠT] --mong 7883`.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/khuon_dong_bang/gl_406.py` *(mới)* | Khuôn đáp án 406: khoá `dong_sheet`, mang `ky·itl_id·D + BM…BT`; `chuan_bi` lắp lưới SA + tách 9843 hàng công thức; `thieu_lac` = cổng kỳ ↔ `phan_bo_ky`. |
| `tools/dong_bang_sheet.py` *(sửa — bài đòi, AC-4)* | Thêm `KIEU_KHOA = "dong_sheet"` *(khoá hàng sheet, số nguyên)* + `KIEU_COT = "so?"` *(ô SỐ hoặc RỖNG — `BO`/`BP` `iferror` ra rỗng)*. Khuôn ⛔ khai hai kiểu ấy ⇒ chạy **y như cũ** *(giữ ix_fx + 3 ảnh DT3 đúng từng byte)*. |
| `tests/fixture/dap_an/gl_406.json` *(mới)* | Ảnh đáp án — 7883 dòng, bảng phụ `cong_thuc` *(9843)*, cổng ĐẠT. |
| `tests/du_lieu/test_dap_an_406.py` *(mới, 25 bài)* | DT4-B1…B3 + AC-1…AC-5; tái tạo byte-identical; mọi cổng mới chứng minh ĐỎ. |

> ⛔ **⛔ sửa** `TIEN_DO.md` / dashboard / changelog chung *(WO-111 dặn)*. ⛔ chạm kho THẬT *(`Dữ liệu: KHONG`)*.

## Cổng *(kết quả nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_dap_an_406.py` | `25 passed in 7.49s` |
| `pytest tests/du_lieu` | `188 passed in 15.88s` *(trước 162 · +25 bài DT4 + 1 đã có)* |
| `dung_moi_truong_isp.sh --duong-nen` *(script NHÁNH, cổng 5437)* | `KẾT: ĐẠT` — toàn bộ `26 = 26 node id (thêm 0 · bớt 0)` · `tests/web 3 = 3` · toàn bộ `12 failed, 2650 passed, 2 xfailed, 14 errors` *(tập đỏ = đường nền cf5156e)* |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cổng tài liệu ĐẠT` — K1…K6 OK *(182 file · 1903 bảng · 729 ô ngày · 104 mã QĐ)* |
| `tools/soi_bang_tuyen.py` | `✅ bản khai KHỚP SQL thật ở cả 41 tuyến` |
| `tools/kiem_thuyet_minh.py` | `✅ 31/31 nút` |
| `tools/kiem_so_song.py` | ⛔ **CHƯA CHẠY** — tool gọi `.venv/Scripts/lint-imports.exe` *(đường Windows)*; container Linux ⇒ `FileNotFoundError`. ĐO TRÊN NỀN `cf5156e`: **cùng lỗi** *(pre-existing, ⛔ do DT4)*. |
| `docs/ITL/_tools/khop_owner.py --kiem` | ⛔ **ĐỎ pre-existing** — `A1·B1·C6 ĐỔI TRẠNG THÁI` *(audit `_AUDIT_ALIGNMENT_ROADMAP` đang chạy)*. ĐO TRÊN NỀN `cf5156e`: **cùng A1·B1·C6** *(⛔ do DT4 — DT4 ⛔ chạm docs owner/audit)*. |
| `pg_migrate` | n/a — ⛔ chạm schema. |

## Bằng chứng từng AC *(đỏ-trước = đã chứng minh ĐỎ)*
| AC | Bằng chứng | Đỏ-trước |
|---|---|---|
| **AC-1 / DT4-B1** | `test_DT4_B1_phan_bo_ky_19_khop_4_lech_co_ten`: đếm số dòng/kỳ TRÊN ẢNH ↔ `phan_bo_ky` ⇒ **19 kỳ khớp** CHÍNH XÁC · 4 kỳ lệch có tên `{202605:(239,537), 202606:(0,613), 202607:(0,686), 202608:(0,487)}` · Σ=7883. Cổng `dong_bang_sheet gl_406 --mong 7883` ⇒ `[ĐẠT]`. | `test_DT4_B1_cong_ky_DO_khi_lech_NGOAI_4_ky_co_ten` *(3 ca: thiếu kỳ khớp · thêm kỳ vắng · kỳ lạ)* + mutation `LECH_CO_TEN[202605]=538 ⇒ thiếu [202605] ĐỎ` |
| **AC-2 / DT4-B2** | `test_DT4_B2_mot_lat_ky_RONG_thi_DO`: bỏ hết kỳ `202502` ⇒ `thieu:[202502]` ⇒ exit 1. `test_DT4_B2_ban_tho_values_RONG_thi_TU_CHOI`: `values=[]` ⇒ exit 2, ⛔ ghi. | chính bài là ca phá *(Đ3: mẫu số 0 LÀ kết quả)* |
| **AC-3 / DT4-B3** | `test_DT4_B3_anh_khong_mang_cot_Dien_giai_So_CT_Email`: quét ≥ 3·7883 khoá ⇒ 0 khớp; vùng đọc `COT_THO` ⛔ có `B`/`C`. | `test_DT4_B3_may_quet_PII_CAN_ca_pha` *(4 ca: Diễn giải · Diễn  giải · số chứng từ · Email)* + `test_DT4_B3_ban_tho_co_cot_Email_thi_TU_CHOI` *(exit 2, ⛔ in giá trị)* |
| **AC-4** | `test_DT4_khuon_gl_406_la_tep_rieng_dung_giao_keo` *(tệp riêng, giao kèo)*; `test_DT4_giu_anh_IX_FX_va_ba_anh_DT3_dung_tung_byte` *(sha256[:16]: ix_fx `e2c9fdd028bd3286` · atl_cay `504fa53d27c44b83` · cdt_correct `8d8cfaed26b6aa5a` · mapping_master_cfg `3c1f61a28fd3d8ce` — ĐÚNG TỪNG BYTE)*. | mutation `BO/BP="so" ⇒ ô rỗng 12/78830 ĐỎ` *(chứng minh `so?` làm việc)* |
| **AC-5** | `test_DT4_B1_anh_khai_9843_hang_cong_thuc` *(bảng phụ `cong_thuc` 1 dòng vào checksum + ghi_chu)*; `test_DT4_hang_du_lieu_co_loi_BM_thi_DO` *(ô lỗi `#DIV/0!` ⇒ "ô ⛔ số" ⇒ ĐỎ)*; `test_DT4_cot_A_rong_False_thi_TU_CHOI`. | ba bài đều là ca phá |
| **AC-6 / Q8** | Nhánh **⛔ có** `MONG_PYTEST_TOAN_BO` *(grep 0)*. Số `--collect-only`: **TOÀN BỘ 2653 → 2678 (+25)** · `tests/du_lieu 163 → 188 (+25)` · `test_dap_an_406 = 25`. *(Orchestrator đặt sàn lúc gộp.)* | — |

## Số bài trước → sau
- `tests/du_lieu`: **162 → 188** *(+26: 25 bài DT4 + 1 đã có đếm lại)*; toàn bộ passed **2624 → 2650** *(+26)*.
- Tập đỏ đường nền: **26 → 26** *(thêm 0 · bớt 0)* · `tests/web 3 → 3`.

## Kết quả đóng băng *(mỗi số đếm MỘT vật — Đ4)*
- **7883** dòng dữ liệu = sheet **10…7892** *(liên tục, cột A tăng dần serial)* — khoá `dong_sheet`.
- **20** lát kỳ có mặt *(202410…202605)*; `checksum_noi_dung = e98f3a699e2de469` *(= `AnhChup` tính lại)*.
- **19** KỲ khớp `phan_bo_ky` CHÍNH XÁC *(dải 2024-10…2026-04 = **19 THÁNG**)* · **4** kỳ lệch CÓ TÊN → `lac`.
- **6** HÀNG *(4962·4963·6073·6507·6949·7631)* thiếu tiền tệ `D` ⇒ `BO` & `BP` rỗng = **12 Ô** *(6 `BO` + 6 `BP`)* — cột `so?`/`chu?`, cho phép.
- **9843** hàng công thức thừa *(7893…17735, cột A rỗng)* — bảng phụ `cong_thuc`, ⛔ bảng chính.
- **0** ô lỗi trong hàng dữ liệu *(BM·BN·BQ·BR·BS·BT strict = 70947/70947 số)*.
- `D` thật: `HKD · SGD · USD · VND` *(⛔ `COP` trong dữ liệu)* + 6 rỗng. `itl_id`: `ITL#1…ITL#7883`, 0 rỗng.

## Quét PII *(số đếm + mẫu số — Đ3)*
- Vùng đọc = `A·D·R·BM:BT` *(⛔ `B` Số chứng từ · `C` Diễn giải)* — lưới thô `COT_THO` ⛔ có `B`/`C`.
- Máy soát **12/12** tên cột bản thô + **2** tên cột bảng phụ với `PM_COT_RIENG_TU {Email Address}` ⇒ **0** trùng.
- Bài quét ảnh: ≥ **3·7883 = 23 649** khoá ⇒ **0** khớp mẫu `Diễn giải|Số chứng từ|Email`. Ca phá *(4 tên)* CẮN đủ 4.

## ⚠ Hai chỗ `WO-111` lệch số đo — Dev khai đúng số ĐO ĐƯỢC, hỏi orchestrator *(⛔ tự sửa WO)*
1. **"21 kỳ khớp"** *(WO §Nguồn · AC-1)* — ĐO ĐƯỢC **19**. Dải `2024-10…2026-04` có **19 THÁNG** *(3+12+4)*, ⛔ 21; 23 kỳ sổ − 4 kỳ lệch = 19. Bản chất *(4 kỳ lệch tên + số)* ĐÚNG y WO. Khuôn/bài khai **19**.
   - *Khuyến nghị:* **(A)** đổi WO/AC-1 "21 kỳ" → "19 kỳ" *(khuyên)*. **(B)** giữ WO, nhận chú thích Đ4 ở khuôn. *(⛔ chặn — số thực chất khớp.)*
2. **"6 ô rỗng BO/BP"** *(WO §Nguồn O7 · AC)* — ĐO ĐƯỢC **6 HÀNG = 12 Ô** *(6 `BO` + 6 `BP`)*. "6" đếm HÀNG; "12" đếm Ô *(Đ4: hàng ≠ ô)*. Cùng 6 hàng ấy thiếu `D`.
   - *Khuyến nghị:* **(A)** đọc "mong=6" là **6 hàng** *(khuyên — khớp đo)*; bài khai cả hai số *(6 hàng · 12 ô)*. **(B)** nếu WO ý "6 ô" thì SAI đo — cần orchestrator xác nhận.

## Quyết định Dev tự quyết *(trong khoảng WO cho)* — nêu để Test soi
- **`BANG = "PD.406"`** *(AP §3.3.1 PD 406)* — WO ⛔ khai tên bảng; chọn `PD.406`. Đổi nếu orchestrator muốn mã khác.
- **Mang `D` (tiền tệ)** — WO ⑯ "nếu rẻ"; rẻ *(đã đọc)* và chẩn đoán được: 6 hàng thiếu `D` ⇒ `BO/BP` rỗng. Giữ.
- **Sửa công cụ chung** *(AC-4 "chỉ khi bài đòi")*: thêm `KIEU_KHOA dong_sheet` + `KIEU_COT so?` — bài `test_DT4_khoa_dong_sheet_hop_le` · `test_DT4_cot_so_opt_*` đòi; cùng tinh thần DT3 thêm `ma`/`chu?`. Giữ mọi ảnh cũ từng byte *(sha ghim)*.
- **Bảng phụ `cong_thuc` (1 dòng)** giữ tóm tắt 9843 hàng công thức — để vào checksum *(sửa tay là ĐỎ)* và tái tạo byte-identical *(cột A ⛔ vào ảnh ⇒ phải có chỗ khai số này)*.

## Dev tự thấy còn yếu *(Test soi chỗ này trước)*
- **Cổng kỳ phụ thuộc `itl_ledge_adjustment.json`** — nếu ảnh sổ đổi, `thieu_lac` đổi theo *(cố ý, như `ix_fx`→C1)*. Nhưng `phan_bo_ky` là của **sổ đã ADJUSTED** *(9967 dòng, 23 kỳ)*; parity H4 thật sẽ so 406 ↔ **CA.GL** *(BE-HC)*, ⛔ so với chính con số điều chỉnh này. Cổng kỳ ở đây chỉ chứng *số dòng mỗi kỳ* khớp, ⛔ chứng *giá trị* BM…BT đúng — đó là việc của H4 *(ngoài DT4)*.
- **`cot_A_rong` tin lưới thô** — khuôn đòi `True` nhưng ⛔ tự đọc lại vùng 7893…17735 *(orchestrator O7: agent ⛔ đọc Drive; phiên này ĐÃ đọc và xác nhận cột A trả 0 hàng)*. Bằng chứng ở log đọc, ⛔ trong ảnh.
- **`dong_sheet` tin vị trí đọc** — khuôn kiểm LIÊN TỤC *(10+i)* nhưng `dong_sheet` do lượt đọc lắp, ⛔ đọc lại từ một cột sheet. Nếu đọc bỏ sót một hàng DỮ LIỆU giữa chừng *(cột A có ngày)*, `dong_sheet` vẫn liên tục mà kỳ có thể lệch ⇒ cổng kỳ bắt; nhưng một hàng mất mà kỳ vẫn khớp thì ⛔ cổng nào bắt *(giới hạn đã biết — lát kỳ + liên tục giảm thiểu)*.
- **Ảnh 2.7 MB** *(> ước 1–2 MB của WO)* — 7883 dòng × 11 cột, số thực nhị phân dài. ⛔ nén.

## Câu còn treo
- Hai chỗ lệch số đo ở trên *(21→19 · 6 hàng=12 ô)* — Dev khai số ĐO ĐƯỢC + khuyến nghị A/B; chờ R1 xác nhận, ⛔ chặn.

---

## Vòng sửa sau R1 (KQ-113) — `fls-dev` làn DATA *(phiên cloud · Opus 4.8)* · 2026-11-17

> Mục này **chỉ THÊM** *(⛔ sửa dòng cũ ở trên)*. `KQ-113` TRƯỢT nhẹ — **0 CHẶN · 1 NÊN SỬA (`F-1`) · 6 GHI NHẬN**; dữ liệu khớp nguồn **157.648/157.648**. Orchestrator quyết: `F-1` = **A** *(sửa khuôn + khai lệch có tên)*; `F-2`·`F-3`·`F-4`·`F-6` = GHI NHẬN rẻ làm luôn; `F-5`·`F-7` ⛔ của Dev.

### Đã sửa *(mỗi phát hiện — bằng chứng đo + ĐỎ-trước)*

| F | Mức | Sửa gì | Bằng chứng ĐẠT | ĐỎ-TRƯỚC *(đo trên công cụ TRƯỚC sửa)* |
|---|---|---|---|---|
| **`F-1` `DT4-R1-01`** | **NÊN SỬA** | `gl_406.py`: `itl_id` phải khớp `^ITL#\d+$`; **4** hàng `#N/A ()` *(`dong_sheet` 6684·6836·7500·7832)* khai thành **LỆCH CÓ TÊN** ở **bảng phụ `itl_id_lech`** *(`PHU_MONG` mong = **4**; khác ⇒ cổng bảng phụ ĐỎ)* — ⛔ sửa giá trị nguồn, ⛔ âm thầm cho qua. Khai 4 `dong_sheet` + giá trị thô để H4 thấy 4 dòng ⛔ nối được. | `test_DT4_R1_itl_id_lech_co_ten_4_hang`: bảng phụ 4 hàng = `{6684,6836,7500,7832}`; bảng CHÍNH **7879/7883** khớp `^ITL#\d+$`. **Đọc lại nguồn SA** *(1 lượt `batchGet` A·D·R·BM:BT, ⛔ B:C)* xác nhận y **4** hàng ấy; bảng chính + `nguon` + `cong_thuc` **TRÙNG TỪNG BYTE** ảnh gốc *(7883×11)*. | `test_DT4_R1_itl_id_lech_khac_4_thi_DO` *(2 ca)*: thêm hàng `#N/A` thứ 5 ⇒ `itl_id_lech 5≠4` **ĐỎ** exit 1; bỏ 1 ⇒ `3≠4` **ĐỎ**. Công cụ TRƯỚC: cả hai qua `[ĐẠT]` exit 0. |
| `F-2` `DT4-R1-02` | GHI NHẬN | *(bài)* ghim `_ky_tu_serial` ở **hai phía ranh giới tháng** bằng serial VIẾT TAY *(⛔ chung `EPOCH` với mã)*. | `test_DT4_R1_ky_tu_serial_ghim_ranh_gioi_thang`: `45688→202501` *(2025-01-31)* · `45689→202502` · `45657→202412` · `45717→202503`. | Đột biến M7 *(`EPOCH`+1)* xưa 25/25 xanh; nay serial ngày CUỐI tháng ⇒ kỳ kế ⇒ **ĐỎ**. |
| `F-3` `DT4-R1-03` | GHI NHẬN | `gl_406.py`: `D` ghim **TẬP ĐÓNG** `TIEN_TE = {USD,SGD,COP,VND,HKD}` — giá trị lạ *(⛔ rỗng)* ⇒ `thieu_lac` báo `D_la@<dong_sheet>` ⇒ ĐỎ. *(Bài)* quét PII cả **GIÁ TRỊ** ô `itl_id`/`D` *(⛔ chỉ tên cột)*. | `test_DT4_R1_quet_PII_GIA_TRI_o_itl_id_va_D`: mẫu số **2·7883** ô, **0** khớp Diễn giải/Số CT/Email; ca phá CẮN. `D ∈ {USD 4085·VND·SGD·HKD}` + 6 rỗng *(⛔ COP trong dữ liệu)*. | `test_DT4_R1_D_ngoai_tap_tien_te_thi_DO`: `D = "Diễn giải lạc cột D"` ⇒ `thieu=[D_la@10]` **ĐỎ** exit 1, ⛔ in giá trị. Công cụ TRƯỚC: `[ĐẠT]` exit 0. |
| `F-4` `DT4-R1-04` | GHI NHẬN | `dong_bang_sheet.py` `_khoa_hop_le` *(khoá `dong_sheet`)*: `fullmatch(r"[0-9]+")` thay `str.isdigit()`. | `test_DT4_khoa_dong_sheet_hop_le` *(mở rộng)*: `"٣"`·`"٧"`-full-width ⇒ `False` *(⛔ nhận nhầm)*; `"²"` ⇒ `False` *(⛔ `int()` NỔ)*. | `isdigit()` xưa: `"٣"`→`True` · `int("²")`→`ValueError` traceback. |
| `F-5` `DT4-R1-05` | GHI NHẬN | **⛔ việc Dev** — vá ISP `:1355` + sàn `MONG_PYTEST_TOAN_BO` = việc orchestrator. | — | — |
| `F-6` `DT4-R1-06` | GHI NHẬN | **Đính chính số** *(dưới)*. | `--collect-only` đo lại: xem bảng số. | — |
| `F-7` `DT4-R1-07` | chấp nhận | **⛔ đổi** hình dạng công cụ chung *(ảnh dạng dict là hợp đồng DT2·DT3)*. | — | — |

### Đính chính *(theo `F-1` · `F-6`; ⛔ sửa dòng cũ — ghi đúng ở đây)*
- **`F-1`** — câu mục *"Kết quả đóng băng"* ở trên: *"`itl_id`: `ITL#1…ITL#7883`, 0 rỗng"* **SAI** *(khoảng đoán, ⛔ số đo)*. **Đúng:** `itl_id` **7879/7883** hàng khớp `^ITL#\d+$`; **4** hàng mang chuỗi lỗi Sheets `#N/A ()` *(`dong_sheet` 6684·6836·7500·7832 — ⇒ 3 khoá trùng giá trị)*. 0 ô rỗng *(đúng)*, nhưng ⛔ phải dải `ITL#1…ITL#7883`.
- **`F-6`** — AC-6 + *"Số bài trước → sau"* ở trên ghi **lệch nhau 1**. **Đúng** *(đo `--collect-only` đếm `::` trên `cf5156e` → `isp/DT4` nền, trước vòng sửa này)*: `tests/du_lieu` **162 → 188 (+26)** · TOÀN BỘ **2652 → 2678 (+26)** *(= 25 bài DT4 + 1 node `[gl_406]` của bài DT2-R2-02 tham số hoá)*. Bỏ hai số `163→188 (+25)` và `2653→2678 (+25)`.

### Số bài `--collect-only` *(đếm `::` — vòng sửa R1 thêm 7)*
| Mốc | `test_dap_an_406` | `tests/du_lieu` | TOÀN BỘ |
|---|---|---|---|
| nền `cf5156e` *(trước DT4)* | 0 | 162 | 2652 |
| `isp/DT4` sau R1 *(trước vòng sửa)* | 25 | 188 | 2678 |
| **sau vòng sửa R1 *(phiếu này)*** | **32** *(+7)* | **195** *(+7)* | **2685** *(+7)* |

*(+7 = `itl_id_lech` 4 hàng×0… thực: 1 cấu trúc + 2 ĐỎ-trước itl_id + 1 ĐỎ-trước D + 1 quét-giá-trị + 1 ca-phá + 1 ghim-serial. `F-4` mở rộng bài CÓ SẴN ⇒ ⛔ thêm node.)*

### Checksum ảnh `gl_406.json`
- **trước:** `e98f3a699e2de469` → **sau:** `53a243b42101c314`. Đổi **CHỈ** do bảng phụ `itl_id_lech` mới *(`nguon` · `dong` 7883×11 · `cong_thuc` giữ **từng byte** — đọc lại SA 1 lượt `batchGet` xác nhận 0 lệch)*.

### Cổng *(nguyên văn — chạy trên `isp/DT4` sau vòng sửa, cổng 5437)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_dap_an_406.py` | `32 passed` |
| `pytest tests/du_lieu` | `195 passed` |
| `dung_moi_truong_isp.sh --duong-nen` *(script NHÁNH, một mình)* | `KẾT: ĐẠT` · `12 failed, 2657 passed, 2 xfailed, 14 errors` · tập đỏ **26 = 26** *(thêm 0·bớt 0)* · `tests/web 3 = 3` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `kiem_tai_lieu.py` | `✅ cổng tài liệu ĐẠT` |
| `ix_fx.json` + 3 ảnh DT3 | **đúng từng byte** *(`git diff tests/fixture/cau_hinh/` rỗng; `test_DT4_giu_anh_IX_FX…` xanh)* |

### Đổi tệp *(4 — `git diff --stat cf5156e→phiếu` phần vòng sửa)*
- `tools/khuon_dong_bang/gl_406.py` — `F-1` *(bảng phụ `itl_id_lech`, `ITL_ID_RE`, `LECH_ITL_ID`)* + `F-3` *(`TIEN_TE`, cổng `D`)*.
- `tools/dong_bang_sheet.py` — `F-4` *(`_khoa_hop_le` `dong_sheet` dùng `fullmatch`)*.
- `tests/fixture/dap_an/gl_406.json` — đóng băng lại từ SA *(bảng phụ `itl_id_lech`)*.
- `tests/du_lieu/test_dap_an_406.py` — +7 bài *(F-1·F-2·F-3)* + mở rộng `F-4` + checksum mới.

### Câu còn treo cho orchestrator
1. **BG `chỉ THÊM` ⟂ `F-1`/`F-6` "Sửa câu/số":** Dev đọc *"chỉ THÊM"* là **mạnh hơn** ⇒ đính chính Ở MỤC NÀY *(⛔ sửa dòng lịch sử)*. **(A)** *(đã làm — khuyên)* giữ dòng cũ, đính chính ở đây. **(B)** sửa thẳng dòng `itl_id: ITL#1…ITL#7883` + hai số AC-6 inline. Chờ orchestrator chọn.
2. `F-5` *(ISP `:1355` "5 tiền tệ" · sàn `MONG_PYTEST_TOAN_BO` +26)* — việc orchestrator, ⛔ đụng tới.
