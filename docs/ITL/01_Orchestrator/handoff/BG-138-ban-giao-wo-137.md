# BG-138 — bàn giao WO-137 · ISP 3.1.2 · Step 15 · DT5: ảnh đáp án 409·410 · CFA1 Daily + Y/H/Q/M

| | |
|---|---|
| **Phiếu** | trả `WO-137` *(DT5, làn DATA)* |
| **Bởi** | phiên cloud `fls-dev #DATA` *(Opus 4.8)* · cụm PG **5436** · nhánh `isp/DT5` · 2026-11-18 |
| **Nền** | sha `a8367ed6ec0bc5a31c92bb34bdf70d736cbc9a65` *(HEAD khi dựng — ghi theo Bước 0)* |
| **Dải phiếu** | `KQ-139` (R1) · `KQ-140` (R2) · `KQ-141` (R3). Số trống kế tiếp: **142** |

---

## 0. Một dòng kết luận

Đóng băng **hai ảnh đáp án CFA1** — `cfa1_daily.json` *(409, HD × ngày)* + `cfa1_yhqm.json`
*(410, HD × kỳ Y/H/Q/M)* — từ bản sao **CF report** *(không phải P&L)*, với hai khuôn mới
`cfa1_daily`·`cfa1_yhqm` dùng chung `_cfa1`; **⛔ sửa `dong_bang_sheet.py`** *(bài ⛔ đòi)*; mọi
cổng DT5-B1/B2 + AC-3/AC-4 ĐẠT và được chứng minh ĐỎ; hồi quy `--duong-nen` KẾT: ĐẠT *(tập đỏ
+0/−0)*.

## 1. Nguồn đã chọn + lý do *(mơ hồ ⇒ đã hỏi orchestrator — WO yêu cầu)*

- Bản sao WO cấp *(`19NN…`, `[COPY] … | P&L Report`)* **KHÔNG có sheet CFA1** — chỉ PLA1/PLA3
  *(PD 414–419, ISP §3 LOẠI TRỪ)*. Đã hỏi; orchestrator trả **A**: CFA1 ở bản sao
  **`[COPY] Report I General Ledger | CF report`**, id `12S00TnFMd9Uz0g-NLvOA7kdmPPhY1V_SVOQJkDi1ZiU`.
- Khoá SA chỉ-đọc ĐỌC ĐƯỢC tệp ấy; `sa_meta.py` liệt kê đúng tên AP:
  - **409** = `Report I CFA1 Daily` *(458 × 818)*
  - **410** = `Report I CFA1 Y H Q M` *(458 × 502)*
  - 411 = `MID I Report I CFA3 Daily` — **CFA3, ISP §3 LOẠI TRỪ** ⇒ ⛔ đóng băng *(đúng 2 ảnh)*.
- Bản thô CHỈ ở `/tmp/dt5/` *(⛔ commit)*. ⛔ đọc cột tên người/email/Diễn giải/Số CT *(CFA1 là
  tổng hợp theo HD × ngày — ⛔ có cột ấy)*.

## 2. Hiện vật *(mỗi số có nhãn Đ4 — đếm GÌ)*

| Tệp | Nội dung | checksum / sha256[:16] |
|---|---|---|
| `tools/khuon_dong_bang/_cfa1.py` | bộ máy chung *(phân loại hàng · dựng cây 5 LE × 74 · bóc ô thưa · cổng cây ATL · soát PII lưới)* | — |
| `tools/khuon_dong_bang/cfa1_daily.py` | khuôn 409 *(trục NGÀY)* | — |
| `tools/khuon_dong_bang/cfa1_yhqm.py` | khuôn 410 *(trục KỲ Y/H/Q/M)* | — |
| `tests/fixture/dap_an/cfa1_daily.json` | ảnh 409 · **6.830.862 byte** | `checksum_noi_dung` = `6e01ee2b0f2207a3` |
| `tests/fixture/dap_an/cfa1_yhqm.json` | ảnh 410 · **1.342.006 byte** | `checksum_noi_dung` = `ff9e76976cda1401` |
| `tests/du_lieu/test_dap_an_cfa1.py` | 21 bài *(DT5-B1/B2 · AC-3 · AC-4 · PII)* | — |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: sàn 3100 → **3123** + bài ghim | — |

**Số đo 18/11 — mỗi số đếm MỘT vật (Đ4):**

| Số | Đếm gì |
|---|---|
| **5** khối LE | GROUP · SGO2 · SGO1 · HGO6 · BGO2 *(CFA1 = CF THEO LE — AP §3.5.1)* |
| **74** mã HD/khối | = cây ATL *(`atl_cay.json`)* — 0 mã lạ, 0 mã thiếu, cả 5 khối |
| **370** hàng cây `phu.hd` | = 5 × 74 *(mọi mã ∈ cây ATL — cổng DT5-B1)* |
| Daily **760** cột ngày `phu.ngay_truc` | ngày từ 2024-10-20 tới 2026-11-18, LIÊN TỤC *(cắt 52 cột tương lai toàn 0)* |
| Daily **33.355** dòng chính | ô mUSD **≠ 0** *(ô 0/vắng ⇒ 0 — H5 so "ô so > 0")* |
| Daily **25** `phu.o_loi` | ô `"-"` *(⛔ số)* — giữ chuỗi, ĐẾM, ⛔ hoá 0 *(AC-3)*; ⛔ có `#REF!`/`#N/A` |
| Y/H/Q/M **57** cột kỳ `phu.ky_truc` | 3 năm *(2024·2025·2026)* × 19 Y/H/Q/M *(cắt 7 năm tương lai toàn 0)* |
| Y/H/Q/M **5.655** dòng chính · **25** o_loi | ô ≠ 0 · ô `"-"` |

## 3. Quyết định kiến trúc *(⛔ sửa công cụ chung — bài ⛔ đòi)*

- Ảnh là LƯỚI HD × trục rất rộng *(370 × 760)*, ⛔ hợp mô hình "một hàng một thực thể" của
  `dong_bang_sheet.py`. Giải bằng **bảng phụ + dòng thưa**, ⛔ đụng công cụ:
  dòng chính = ô ≠ 0 *(khoá ghép `o_id = le#ma#nhãn`, kiểu `ma`)*; ô `"-"` ⇒ `phu.o_loi`; cây đầy
  đủ ⇒ `phu.hd`; trục ⇒ `phu.ngay_truc`/`ky_truc` *(`PHU_MONG` khai số — Đ5)*.
- ⇒ `tools/dong_bang_sheet.py` **0 dòng đổi** *(git diff = rỗng)* ⇒ `ix_fx` + 3 ảnh DT3 +
  `gl_406` giữ **đúng từng byte** *(sha256[:16] ghim ở bài `test_giu_anh_DT2_DT3_DT4_dung_tung_byte`)*.
- Soát PII riêng: LƯỚI SA ⛔ có trường `cot` ⇒ `_soat_rieng_tu` của công cụ ⛔ thấy tiêu đề nguồn
  ⇒ khuôn thêm `soat_pii_luoi` *(quét 7 hàng tiêu đề + cột A…F)* ⇒ TỪ CHỐI khi có `PM_COT_RIENG_TU`.

## 4. Cổng ↔ bằng chứng *(mỗi cổng mới chứng minh ĐỎ — phá, chạy, xem cắn, trả nguyên)*

| AC / bài | Mong | Bằng chứng | Đỏ-trước |
|---|---|---|---|
| **DT5-B1** mọi mã HD ∈ cây ATL | ✅ | `test_DT5_B1_daily_moi_ma_HD_trong_cay_ATL` · `…yhqm…` *(dòng ∈ cây 74; `phu.hd` = 370)* | ⇐ DT5-B2 |
| **DT5-B1** số cột ngày = số ngày 21/10/2024→ngày đọc | ✅ *(⚠ xem §5)* | `test_DT5_B1_daily_so_cot_ngay_tu_moc_toi_ngay_doc` *(760 = 2024-10-20…2026-11-18, LIÊN TỤC)* | mốc sai/hụt lát ⇒ TỪ CHỐI |
| **DT5-B2** đổi 1 mã HD lạ ⇒ ĐỎ; trả nguyên ⇒ đúng từng byte | ✅ | `test_DT5_B2_doi_ma_HD_la_thi_DO_tra_nguyen_dung_tung_byte` *(GI→ZZZ ⇒ exit 1, thieu=['ZZZ']; trả nguyên ⇒ byte khớp baseline)* | **ĐỎ chứng minh** |
| **DT5-B2** *(chiều LE)* | ✅ | `test_DT5_B2_doi_LE_la_thi_TU_CHOI` *(LE khối 1 → XXX ⇒ TỪ CHỐI)* | TỪ CHỐI |
| **AC-3** ô lỗi ⇒ chuỗi + đếm, ⛔ hoá 0 | ✅ | `test_AC3_o_loi_giu_chuoi_dem_khong_hoa_0` *(25 ô `"-"`, giữ `{"chu":"-"}`, ⛔ vào dòng chính)* | — |
| **AC-4** trục ⛔ liên tục / mốc sai / cột tương lai ≠ 0 / thiếu khối LE / lưới rỗng | ✅ | 5 bài `test_AC4_*` ⇒ TỪ CHỐI, ⛔ ghi tệp | mỗi bài TỪ CHỐI |
| **AC-4** PII | ✅ | `test_PII_*` *(quét có ca phá CẮN Diễn giải/Số CT/Email; lưới có `Email Address` ⇒ TỪ CHỐI, ⛔ in giá trị)* | ca phá |
| **AC-5 (Q8)** sàn + bài ghim cùng commit | ✅ | `MONG_PYTEST_TOAN_BO` 3100 → **3123** *(= thu thập)*; `test_S0_R3_02_…` + `test_S0_R2_03_…` ĐẠT | — |

## 5. ⚠ Câu hỏi kèm khuyến nghị *(cho orchestrator — Đ1/Đ4, ⛔ tự quyết)*

**Cột ngày đầu của sheet = 2024-10-20 (Chủ nhật, serial 45585), sớm MỘT ngày so với mốc
`21/10/2024` (Thứ 2) mà ISP/AP khai** *(H5 §3: "cột ngày bắt đầu 21/10/2024")*. Cột 2024-10-20 có
dữ liệu thật *(5 ô ≠ 0 + các ô `"-"`)* nên **đã GIỮ** *(cắt là mất số)*; trục neo mốc THẬT của
sheet và ảnh khai rõ *(`ghi_chu_khuon` + bài ghi cả hai mốc)*.
- **Khuyến nghị A *(giữ như hiện tại)*:** trục = cột THẬT của sheet *(2024-10-20 → ngày đọc)*,
  H5/H6 đọc mốc từ ảnh. Đã làm vậy. *(Trục chứa 2024-10-21; chỉ dư 1 ngày mở đầu.)*
- **Khuyến nghị B:** nếu BA chốt mốc cứng 2024-10-21, cắt cột 2024-10-20 *(khai số 5 ô bị bỏ)* ⇒
  đóng băng lại, số cột ngày 760 → 759.
→ Cần orchestrator/BA chốt A hay B trước khi H5 dùng mốc.

## 6. Hồi quy *(chạy từ worktree, cổng 5436)*

| Cổng | Kết quả |
|---|---|
| `tests/du_lieu/test_dap_an_cfa1.py` | **21 passed** |
| `tests/du_lieu/` *(DT2·DT3·DT4 + khuôn-param + DT5)* | **358 passed** |
| `--duong-nen` *(một mình)* | **KẾT: ĐẠT** — toàn bộ `12 failed · 3095 passed · 2 xfailed · 14 errors` *(tập đỏ+XFAIL = 28 = đường nền, thêm 0 · bớt 0)*; `tests/web` `3 failed · 664 passed` *(3 = đường nền)*; chạy **3123** *(mong ≥ 3123)* · skipped 0 · deselected 0 |
| `lint-imports` | **11 kept, 0 broken** |
| `pg_migrate` → `pg_verify` | **khớp** *(26/26 di trú · 25 bảng/view · 0 lệch)* |
| `kiem_tai_lieu.py` | **K1–K6 OK** *(248 file · 2309 bảng)* |

- Số bài THU THẬP: **3102 → 3123** *(+21 bài `test_dap_an_cfa1.py`; +2 bài khuôn-tham-số của
  `test_anh_cau_hinh.py` nhận 2 khuôn CFA1 mới)*. `tests/web` 667 *(⛔ đổi)*.
- Quét PII: ảnh 409 + 410 — **0** tên khoá / giá trị chữ khớp mẫu Diễn giải/Số CT/Email *(mẫu số
  > so_dong × 3)*; ca phá CẮN; lưới có `Email Address` ⇒ TỪ CHỐI *(⛔ in giá trị)*.

## 7. Giới hạn còn lại *(bàn giao cho R1/R2/R3 + H5/H6)*

- Ô lỗi nguồn hiện CHỈ thấy `"-"` *(25 ô, đều ở cột 2024-10-20)* — ⛔ `#REF!`/`#N/A`. Khuôn vẫn
  xử mọi ô ⛔ số như `o_loi` *(AC-3)*; nếu re-read về sau có `#REF!` thì PHU_MONG `o_loi` đổi ⇒ cổng ĐỎ ⇒ đóng băng lại.
- `PHU_MONG`/`--mong` là số ĐO 18/11 *(như `gl_406.MONG`)*; re-read ngày khác ⇒ cập nhật hằng +
  đóng băng lại *(báo cáo daily mọc thêm cột ngày)*.
- Câu hỏi mốc 2024-10-20 vs 21 *(§5)* — chờ chốt.
