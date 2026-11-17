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
