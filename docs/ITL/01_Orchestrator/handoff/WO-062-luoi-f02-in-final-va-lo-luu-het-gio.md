# WO-062 — Lưới `F02` in **Final** ⛔ cột nguồn thô · phép hỏi lại ⛔ gọi chính người gõ là *"người khác"* · lô lưu hết giờ ⛔ khẳng định *"CHƯA vào sổ"*

| | |
|---|---|
| **Trạng thái** | `MO` · ⏳ sau [`WO-051`](WO-051-trang-hang-cho-vnd-104-giay-va-khung-cho-xem-them.md) · ưu tiên **CAO** *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-06 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** `WO-051` *(đã xếp từ 05/10, Dev nhận được ngay; giấu **98,8%** dòng `VND` khỏi `F01` ở **mỗi** lần mở màn — phiếu này chỉ tới được **sau** cú sửa thật đầu tiên, sổ thật hôm nay `fls_sua_tay` **0**; hai phiếu chung `doc_bao_cao.py` nhưng khác hàm — `_SQL_HANG_CHO` ⟷ `doc_so` — làm nối tiếp để hai `BG` ⛔ chồng nền)*. **Trước** [`WO-060`](WO-060-chi-doc-khoa-nut-ghi-dao-da-dao-va-cau-dq-failed.md) *(cùng `man_f02.js` — `Đảo` khoá + `.onkeydown`; phiếu này chạm lưới + lô lưu)* → `WO-047` → `WO-015` |
| **Vì sao một phiếu** | `F-1` và `F-2` của `KQ-061` là **một** đường người đi trên `F02`: lô lưu hết giờ ⇒ bấm `Thử lại` *(hay tải lại rồi gõ lại)* ⇒ phép hỏi lại `ⓒ` so với **ảnh lưới thô** ⇒ hộp *"NGƯỜI KHÁC gõ"* cho chính giá trị mình. Cùng tệp `man_f02.js` *(`_bay` · `_ghi_mot_o` · `_bao_hong` + vẽ ô lưới)*; sửa một nửa là để nửa kia nói sai |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **tác vụ ② — mốc `C`**: cổng **`C1`** *(một phiên sửa thật ≥20 bút toán trải 7 ô)* — hôm nay **mọi** ô người vừa gõ sẽ in `chưa gán` sau một lần tải lại *(sổ thật cột nguồn năm trường rỗng **8.387 / 8.387** ⇒ Final = chỉ lớp người ⇒ **100%**)*; **`C3`** *(va chạm hai người)* — phép kiểm va chạm báo va chạm **giả** cho chính người gõ, làm hỏng đúng tín hiệu `C3` đo; **`C2`** *(hoàn tác — sau `Đảo` lưới phải in Final lùi đúng)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; giữ cho mắt xích *"kế toán sửa 7 cột `· Final` trên sheet ITL Ledge"* — đã lên `F02` — **⛔ đẻ ra câu hỏi** *("số tôi vừa gõ đâu rồi?" · "ai gõ đè ô của tôi?")* mà với `2–3` kế toán *(`QĐ-ITL-27`)* chỉ có thể đem đi hỏi một đồng nghiệp **⛔ hề gõ**.

## Căn cứ
- [`KQ-061`](KQ-061-kiem-wo-023-bg-052-den-bg-059.md) *(`fls-test` 06/10)*:
  - `F-1` `NHE` → `BA` → `DEV`: *"Lô lưu `F02` nói cùng khẳng định bằng chữ khác … sau **32,5 s** hộp *"Lô lưu DỪNG giữa chừng"* in `Máy chưa trả lời sau 30 giây — chưa biết lượt ghi đã vào sổ hay chưa.` **rồi ngay dưới** `1 ô dưới đây CHƯA vào sổ …`; thả lượt ⇒ cửa **`200`**, kho TEST `adj_id 4312` — ô **đã** vào sổ."* Bài `tests/nghiem_thu/test_kq061_f02_het_gio_lo_luu.py::test_F1_HET_GIO_lo_luu_F02_KHONG_noi_o_CHUA_vao_so` `xfail(strict)`.
  - `F-2` `NHE` ngoài phạm vi → `BA`: *"tải lại trang: ô `hd` dòng `1` in `chưa gán` … dù `GET /ledger/1/fields/hd` trả `gia_tri: HD-KQ061-T · value_source: sua_tay` … gõ lại ⇒ hộp *"NGƯỜI KHÁC gõ"* cho **chính** người ấy"*; *"`BA-07:31` `GET /ledger` chỉ khai *"dòng `fls_itl`"* ⛔ nói Final hay thô ⇒ spec **thiếu**"*.
- Quyết định: **`fls-ba` trong thẩm quyền spec** — áp **luật đã có** *(`BA-05` v0.32: *"Final = `fls_sua_tay` ∪ cột nguồn"*; `BA-06` `§3-cũ`: năm cột lưới là *"5 trường Final … vùng người gõ"*; `QĐ-ITL-149`: gợi ý máy ⛔ Final; `QĐ-ITL-73 ⓔ`: *"nguồn nói X, người gõ Y"*)* vào một hợp đồng cửa còn thiếu chữ. ⛔ Đổi luật Final, ⛔ đổi sổ, ⛔ đổi *"con số đến từ đâu"*. PO nâng mức `F-2` **`NHE` → CAO** cho lượt chọn việc: chặn `C1` ngay lượt sửa đầu *(Test ghi đúng: `NHE` **hôm nay** vì sổ thật 0 ô)*.
- ⭐ **`fls-ba` đo lại 06/10** *(`Đ1` đọc mã @ `7b4237f`; sổ thật chỉ `SELECT` qua `docker exec fls-pg-1 psql`)*:

| Phép đo | Kết quả |
|---|---|
| `grep -n fls_sua_tay fls/repo/doc_bao_cao.py` | **2** chỗ: `:461` `doc_mot_dong` *(drawer)* · `:662` `dem_xong_du_thieu` — **⛔** ở `doc_so` *(`_COT_SO` `:73-80` đọc `i.hd`… thô)* |
| người đọc `GET /ledger` *(danh sách)* | **1**: `man_f02.js` `:104` · `:372`; `doc_so` chỉ được gọi ở `fls/api/xu_ly.py:132` |
| sổ thật, cột nguồn có giá trị | `hd` **0** · `pay_type` **0** · `cdt1` **0** · `svc_start` **0** · `svc_end` **0** — trên **8.387** dòng; `*_thyt` có giá trị **0 / 8.387** |
| sổ thật, các lớp | `fls_sua_tay` hiệu lực **0** · giá trị rỗng **0** · `fls_adjustment` **4.428** *(`nguon='sua_tay'` **4** = 2 UAT + 2 bản đảo)* · `fls_may_goi_y` **4.424** |
| giá câu đọc mới *(sổ thật, `EXPLAIN ANALYZE` chỉ đọc)* | trang **501** dòng + năm `LEFT JOIN fls_sua_tay` = **3,28 ms** *(với **0** dòng `fls_sua_tay` — tập rỗng, `Đ3` ⇒ `AC-10` đo trên kho TEST có bút toán)* |
| cửa ghi lặp cùng giá trị | `ghi_tay.ghi_but_toan` `:462`: *"lặp lại cùng giá trị thì ⛔ chèn dòng thứ hai"* *(`da_co=True`)* ⇒ `Thử lại` sau hết giờ ⛔ ghi đôi được ở **cửa** |
| `FLS.ghi(` ở `fls/web/tep` | **19** dòng = **18** chỗ gọi + **1** chú thích *(`man_f01_ghep.js:739`)* — `man_f01.js` 7 · `man_f01_ghep.js` 3 · `man_f01_lenh.js` 1 · `man_f02.js` 3 · `man_f04.js` 4 |

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | ⭐ **§3c ⑪** *(lưới in Final — bảng ⓐ…ⓔ + câu treo)* · §3c ① *(hai cột Quét)* · §3c ④ *(lô lưu)* | **v4.24** |
| `02_BA/06_SCREEN_SPEC.md` | ⭐ **§4.5 ⓔ `ⓕ3`** — đoạn **v4.24** *(đính chính phép đếm "2 nơi"; chữ nguyên văn hộp lô lưu + dòng trạng thái; kiểm kê 18 chỗ)* | **v4.24** |
| `02_BA/07_API_CONTRACT.md` | §2 dòng `GET /api/fls/v1/ledger` — đoạn **v3.14** | **v3.14** |
| `02_BA/05_DATA_DICTIONARY_ERD.md` | ⭐ `DD-I15 ⓓf` *(Final một ô — một luật, mọi nơi đọc)* | **v0.35** |
| `01_Orchestrator/handoff/KQ-061-kiem-wo-023-bg-052-den-bg-059.md` | `F-1` · `F-2` · bài `test_kq061_f02_het_gio_lo_luu.py` *(1 `xfail(strict)` + 1 mẫu số)* | — |
| `fls/repo/ghi_tay.py` | `truoc_khi_go` `:293-315` · `ghi_but_toan` `:458-480` | `HEAD` |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a) Cửa — `<f>_final` + `<f>_nguon`** *(`BA-07` v3.14 · `BA-05` v0.35 `ⓓf`)*: `doc_bao_cao.py::doc_so` trả, cho **mỗi** trường `hd` · `pay_type` · `cdt1` · `svc_start` · `svc_end`: `<f>_final` *(người `IS NOT NULL` ?? nguồn `IS NOT NULL` ?? `null`)* + `<f>_nguon` ∈ {`sua_tay`, `nguon`, `UNMAPPED`} *(hằng `ghi_tay.NGUON_*`)*. Năm trường thô **giữ nguyên từng byte**. ⭐ Phép xếp lớp người-trên-nguồn sống **một chỗ** ở tầng kho, dùng chung với `truoc_khi_go` *(và `dem_xong_du_thieu` nếu Dev thấy rẻ)* — Dev chọn hình *(hàm SQL / Python)*, ghi `BG`. Mười tên khai **một hằng** như `TRUONG_ALLOC` *(cổng `kiem_bang_cot` hai chiều)*; `fls/api/bang_tuyen.py` tuyến `GET /ledger` khai đọc thêm `fls_sua_tay` *(cổng `soi_bang_tuyen`)* | ⛔ Đổi luật Final *(kể cả ca người xoá ô — câu treo)*. ⛔ In gợi ý máy vào ô. ⛔ Đổi nghĩa năm trường thô. ⛔ Đổi `GET /ledger/{itl_id}` / drawer `_dem_viec`. ⛔ Migration, ⛔ view mới trong kho *(nếu Dev thấy cần view ⇒ `HOI` trước)* |
| **(b) Lưới — in Final** *(`BA-06` v4.24 §3c ⑪ ⓐ ⓑ ⓒ ⓔ)*: `man_f02.js` — năm ô gõ được *(chế độ `Gõ`)* + hai cột `HDCode` · `CDT1` *(chế độ `Quét`)* in `<f>_final`; `null` ⇒ `chưa gán` lớp `unmapped` như nay; ô `<f>_nguon = sua_tay` mang `title` *"người sửa — sổ gốc nói: <thô hay chữ `trống`>"*; ảnh `ST.theo_id` mà phép hỏi lại `ⓒ` so = `<f>_final`. Mọi chỗ khác của màn đang đọc `r.<f>` cho **năm** trường ấy *(bộ lọc ô tìm, `Ctrl+Z` `ST.lich`, `_dat`…)* — Dev `grep` lại, ghi `BG` từng chỗ *đổi / giữ — vì sao* | ⛔ Token / lớp CSS mới *(luật `test_moi_token_deu_duoc_khai.py`)*. ⛔ Ký hiệu cấm trong chữ màn *(`test_luat_ky_hieu_man_hinh.py`)*. ⛔ Đổi nút *"chi UNMAPPED"* *(lọc `work_status` — trạng thái đóng băng lúc nạp, khác câu)* |
| **(c) Phép hỏi lại `ⓒ` — ⛔ va chạm với chính mình** *(§3c ⑪ ⓓ)*: `_ghi_mot_o` — `tay` bằng `o.gia_tri` *(sau `String()`)* ⇒ ⛔ hộp *"NGƯỜI KHÁC gõ"*; ô `da-luu`; **0** dòng `fls_adjustment` mới *(bỏ `POST`, hay gửi và nhận `da_co: true` — Dev chọn, ghi `BG`)*. Vế *"người khác thật"* **giữ** | ⛔ Đổi hộp `_bao_nguoi_khac` / `_hoi_ghi_de`. ⛔ Đóng `GAP-SCR-09` *(cửa ghi ⛔ thấy hai người sửa một ô — khe giữa hỏi và ghi vẫn còn, hộp vẫn nói thẳng)* |
| **(d) Lô lưu hết giờ** *(`KQ-061 F-1` — `BA-06` v4.24 `ⓕ3`)*: `_bay` + `_bao_hong` — mã `FLS-HET-GIO`: ô **đang bay** in riêng *"1 ô dưới đây CHƯA RÕ đã vào sổ chưa — máy đã gửi nhưng không nhận được trả lời:"* + dòng ô; ô **sau** giữ *"M ô dưới đây CHƯA vào sổ"* *(⛔ in khi `M = 0`)*; câu cuối *"Bấm Thử lại: máy hỏi sổ trước khi ghi từng ô, nên ô đã vào sổ sẽ không bị ghi lần hai."*; dòng trạng thái *"1 ô chưa rõ đã vào sổ chưa"* + *" · M ô CHƯA vào sổ"* khi `M > 0`; ô đang bay `chua-luu` + `title` *"chưa rõ đã vào sổ chưa"*. **Nguyên văn** từng byte. Mã khác ⇒ ⛔ đổi | ⛔ Tự thử lại lượt ghi *(`WO-023 (c)`)*. ⛔ Đổi `e.cau` / `e.lam_gi` của `FLS-HET-GIO`. ⛔ Đổi hạn `30 s` |
| **(e) Kiểm kê 18 chỗ `FLS.ghi(` theo NGHĨA** *(bài học của `F-1`: phép đếm **chuỗi** "2 nơi" sót lô lưu)*: `BG` bảng **18** dòng *(`tệp:dòng` · việc · màn in gì khi lượt ấy gặp `FLS-HET-GIO` · có khẳng định *"chưa xảy ra / chưa vào sổ / chưa ghi"* về lượt **đã gửi** không)*. Chỗ nào **có** ⇒ sửa theo khuôn `ⓕ3` trong phiếu này **nếu ≤ 2 chỗ ngoài lô lưu**; nhiều hơn ⇒ `HOI` *(⛔ tự nới phạm vi)* | ⛔ Đổi chữ của chỗ nào **⛔** khẳng định sai *(vd `HT.loi_trong_hop` in `e.cau` trần — đúng sẵn)* |
| **Bài thử của Dev** *(`tests/web/**`, `tests/api/**`, `tests/repo/**`)*: một bài mỗi AC, **chứng minh ĐỎ trước** trên mã @ nhận phiếu; thân màn dựng từ **cửa thật** kho TEST *(khuôn `test_wo018_nhat_ky_nguoi_sua_pg.py` — ⛔ khuôn tự nhét `ST`, `11` §6)* | ⛔ Sửa / gỡ dấu bài `tests/nghiem_thu/test_kq061_*` — việc của `fls-test` |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a — sáu ca)* | Kho TEST qua **cửa thật** `GET /ledger`, mỗi ca **≥ 1** dòng *(mẫu số — `Đ3`)*: ⓐ nguồn `NULL` + người gõ `X` ⇒ `hd_final = X` · `hd_nguon = sua_tay` · `hd` **`NULL`** *(thô giữ)*; ⓑ nguồn `N` + ⛔ người ⇒ `N` · `nguon`; ⓒ **chỉ** gợi ý máy *(cú ghép ⇒ `fls_may_goi_y`)* ⇒ `null` · `UNMAPPED`; ⓓ người gõ `X` rồi `Đảo` ⇒ về nguồn *(hay `null`)*; ⓔ người gõ `A` rồi `B` ⇒ `B`; ⓕ nguồn `N` + người gõ ô rỗng *(`value=null`)* ⇒ `N` · `nguon` *(luật cửa ghi — câu treo)* | bài `tests/api/*_pg.py` | đọc thô ⇒ ⓐ **ĐỎ**; tính cả gợi ý máy ⇒ ⓒ **ĐỎ**; lấy bút toán đã bị đảo ⇒ ⓓ **ĐỎ**; lấy bút toán người **đầu** thay **cuối** ⇒ ⓔ **ĐỎ** |
| AC-2 *(a — một luật)* | Kho TEST sau `AC-1`: **mọi** ô năm trường của **mọi** trang `doc_so` = `truoc_khi_go(…)` **gọi hàm thật** *(`gia_tri` khi `value_source` ∈ {`sua_tay`, `nguon`}, khác ⇒ `null`; `<f>_nguon` = `value_source`, riêng `may_goi_y` ⇒ `UNMAPPED`)*; bài in số ô đã so *(mẫu số **> 0** và có **≥ 3** lớp khác nhau)* | bài `tests/repo/*_pg.py` | sửa một bản luật mà ⛔ sửa bản kia ⇒ **ĐỎ** |
| AC-3 *(a — sổ thật ⛔ đổi)* | Sổ thật **chỉ đọc** *(`noi_chi_doc`)*, hàm thật `doc_so` lật **hết** trang: các trường **cũ** trước = sau **từng byte** trên **mọi** dòng *(đo 06/10: **8.387**)*; `<f>_final` / `<f>_nguon` khớp `truoc_khi_go` như `AC-2` *(đo 06/10 dự đoán: **41.935 / 41.935** ô `null` · `UNMAPPED` — nếu sổ đã có người sửa thì **số lúc chạy**, ⛔ số này)* | bài đọc sổ thật + `BG` dán số | thêm/bớt/đổi một trường cũ ⇒ **ĐỎ** |
| AC-4 *(a — hai cổng)* | `kiem_bang_cot` hai chiều xanh với mười tên mới; `soi_bang_tuyen` khớp *(tuyến `/ledger` mang `fls_sua_tay`)* | `pytest tests/api/test_cot_so.py` + `python tools/soi_bang_tuyen.py` | bỏ khai hằng ⇒ cổng cột **ĐỎ**; bỏ `fls_sua_tay` khỏi bảng tuyến ⇒ `soi_bang_tuyen` **ĐỎ** |
| AC-5 *(b — lưới)* | Bài DOM `man_f02.js` thật, thân từ cửa thật kho TEST *(ca `AC-1`)*: chế độ `Gõ` ô `hd` ca ⓐ `textContent` = `X`, ⛔ lớp `unmapped`; ca ⓑ = `N`; ca ⓒ = `chưa gán` lớp `unmapped`; chế độ `Quét` cột `HDCode` · `CDT1` cùng giá trị | bài `tests/web/` | màn đọc `r.hd` thô ⇒ ca ⓐ **ĐỎ**; Quét quên đổi ⇒ ca Quét **ĐỎ** |
| AC-6 *(b — `title`)* | ô ca ⓐ `title` = `người sửa — sổ gốc nói: trống`; ô `sua_tay` trên nguồn `N` ⇒ `… sổ gốc nói: N`; ô `nguon` ⇒ ⛔ `title` ấy | bài DOM | thiếu `title` ⇒ **ĐỎ** |
| ⭐ AC-7 *(c — `F-2` đầu cuối)* | Kho TEST cửa thật, bài DOM: gõ `X` ⇒ lưu ⇒ **tải lại** ⇒ ô in `X`; gõ lại `X` ⇒ **0** hộp *"NGƯỜI KHÁC gõ"*, `fls_adjustment` **+0** dòng. **Mẫu số**: actor **khác** gõ `Y` sau lúc tải ⇒ gõ `Z` ⇒ hộp *"NGƯỜI KHÁC gõ"* **vẫn** hiện *(phép kiểm còn sống)*. **Chrome 8099** kho TEST chuột/phím thật, đúng kịch bản `KQ-061 F-2`: mã khi nhận tái hiện hộp *"người khác"*, mã mới ⛔ | bài `tests/web/` + Chrome CDP + `BG` | bỏ vế `tay = gia_tri` ⇒ **ĐỎ**; nuốt cả va chạm thật ⇒ mẫu số **ĐỎ** |
| ⭐ AC-8 *(d — `F-1`)* | Bài DOM cửa giả treo, hằng hạn chờ nhỏ, lô **3** ô dừng ở ô đầu: hộp chứa đúng *"1 ô dưới đây CHƯA RÕ đã vào sổ chưa — máy đã gửi nhưng không nhận được trả lời:"* + ô đầu, *"2 ô dưới đây CHƯA vào sổ"* + hai ô sau, ô đầu **⛔** nằm dưới câu *"CHƯA vào sổ"*; dòng trạng thái = `1 ô chưa rõ đã vào sổ chưa · 2 ô CHƯA vào sổ`; lô **1** ô ⇒ ⛔ câu *"0 ô"*. `pytest --runxfail "tests/nghiem_thu/test_kq061_f02_het_gio_lo_luu.py::test_F1_HET_GIO_lo_luu_F02_KHONG_noi_o_CHUA_vao_so"` xanh *(⛔ `--runxfail` ⇒ `XPASS(strict)` — đúng mong, `fls-test` gỡ dấu)* · `::test_MAU_SO_mat_ket_noi_*` **vẫn xanh** *(mã khác ⇒ chữ cũ)*. **Chrome 8099** hạn **thật** `30 s`: giữ `POST /adjust`, hết giờ, thả ⇒ `200`, bấm `Thử lại ngay` ⇒ **0** hộp *"người khác"*, `fls_adjustment` **+0** | bài `tests/web/` + Chrome CDP + `BG` | gộp ô đang bay vào *"CHƯA vào sổ"* ⇒ **ĐỎ**; đổi chữ cả mã khác ⇒ mẫu số **ĐỎ** |
| AC-9 *(e — kiểm kê)* | `BG` bảng **18 / 18** chỗ `FLS.ghi(` *(cột như Phạm vi `(e)`)*; số dòng bảng = số chỗ gọi `grep` lúc giao *(⛔ khác ⇒ ghi vì sao)*; chỗ khẳng định sai ⇒ đã sửa + một bài mỗi chỗ, hay `HOI` | đọc `BG` *(Test đọc lại **từng** chỗ)* | — |
| AC-10 *(NFR)* | Kho TEST dựng **≥ 5.000** bút toán `sua_tay` hiệu lực trên **≥ 1.000** dòng *(trong ca, ⛔ để lại rác — `11` §2 kho TEST phình)*: `doc_so` trang **500** ≤ **`2,0 s`** *(đồng hồ quanh hàm thật; ngưỡng mượn `NFR-I30` — ⛔ khai NFR mới)*; sổ thật chỉ đọc lật hết trang 500: **mọi** trang ≤ `2,0 s` | bài + `BG` dán số | câu đọc mỗi dòng một lượt kho ⇒ **ĐỎ** |
| AC-11 | `pytest` toàn bộ: **0** đỏ **ngoài** đúng **1** `XPASS(strict)` *(`kq061::test_F1_*`)* *(`BG` liệt kê tên)* · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp · `kiem_thuyet_minh` khớp · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh · `kiem_tai_lieu` ĐẠT. ⚠ Nếu lượt toàn bộ đỏ ở bài **ngoài** phiếu mà chạy riêng xanh *(đã gặp `KQ-061` lượt 4 — **9** bài ở `test_wo032_v2_bac_da_gan_pg` · `test_wo037_ro_may_theo_cua_ghi_pg` · `test_wo037_v2_ro_nguoi_hai_cau_pg` · `test_anh_pm_pg`)* ⇒ `BG` dán **nguyên văn** + chạy lại **một mình**, ⛔ coi là xanh | lệnh ở `CLAUDE.md` | — |
| AC-12 | `BG` ghi `kiem_so_song`: nền đầu phiếu ⟷ cuối phiếu, ⛔ đỏ mới loại (c); ⛔ `dong_bo --ghi`. `khop_owner --kiem` chạy **sau** commit giấy cuối *(hay ghi "đo trên `<hash>`, trước tờ")* | đọc `BG` | — |

## Màn hình *(chạm UI — lưới `F02` + hộp lô lưu)*
- Thiết kế: `BA-06` **v4.24** §3c ⑪ + `§4.5 ⓔ` `ⓕ3` *(đoạn v4.24)*. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(⛔ token, ⛔ lớp CSS mới — `unmapped` · `chua-luu` · `da-luu` · `note crit` đang có)*.

| Trạng thái | Lưới `F02` | Hộp lô lưu |
|---|---|---|
| tải | `TT.chay` như nay | lô đang bay: viền vàng như nay |
| rỗng | `Sổ ITL trống trong phạm vi này` như nay | ⛔ áp |
| lỗi | `FLS-INTERNAL · HTTP 500` + `Thử lại` như nay | mã khác `FLS-HET-GIO` ⇒ chữ **như nay** *("N ô dưới đây CHƯA vào sổ")* |
| mất kết nối | `FLS-MAT-KET-NOI` + `Thử lại` như nay | như lỗi *(bài mẫu số `kq061::test_MAU_SO_mat_ket_noi_*`)* · ⭐ quá `30 s` ⇒ ô đang bay *"CHƯA RÕ đã vào sổ chưa"*, ô sau *"CHƯA vào sổ"* |
| có dữ liệu | ⭐ năm ô gõ được + hai cột Quét in **Final**; ô người sửa có `title` *"người sửa — sổ gốc nói: …"*; ô ⛔ Final ⇒ `chưa gán` | ⭐ `Thử lại` sau hết giờ ⇒ ô đã vào sổ ⛔ gọi *"người khác"*, ⛔ ghi đôi |

## Dữ liệu
- Bảng/cột chạm: **đọc** thêm `fls_sua_tay` *(khung xem trên `fls_adjustment`)* ở cửa `GET /ledger`; ⛔ ghi, ⛔ cột mới, ⛔ migration.
- Ghi kho THẬT: **`KHONG`**. Sổ thật chỉ **đọc** qua `noi_chi_doc` *(`AC-3`, `AC-10`)* và 8088 chỉ đọc.
- Số dòng sổ thật đổi *(đã đếm — `fls-ba` 06/10)*: **0**. Số ô lưới **in khác** hôm nay trên sổ thật: **0 / 41.935** *(`fls_sua_tay` **0**)* — phiếu sửa cho phiên sửa thật **kế tiếp**, ⛔ cho dữ liệu hôm nay ⇒ báo động hiếm ⛔ áp.

## Câu còn treo
- ⚠ **Người xoá ô thì Final là trống hay nguồn?** Hôm nay cửa ghi *(`truoc_khi_go`)* + `dem_xong_du_thieu` rơi về **nguồn** ⇒ phiếu **theo đúng** luật ấy *(`AC-1` ⓕ)*. Câu của **owner** *("con số trên màn đến từ đâu")* — ⛔ chặn: sổ thật cột nguồn rỗng **8.387 / 8.387** ở cả năm trường ⇒ ⛔ ô nào gặp tới khi nạp có cột Final nguồn. Đổi là phiếu riêng *(luật cửa ghi)*.
- `GAP-SCR-09` *(hai người sửa một ô — khe giữa hỏi và ghi)* vẫn mở, ⛔ chạm.

## Rủi ro
1. **Hai bản luật Final lệch** — xếp lớp ở `doc_so` một kiểu, ở `truoc_khi_go` một kiểu *(vd `IS NOT NULL` ⟷ `<> ''`)* ⇒ lưới và hộp `US-025` nói hai giá trị cho một ô. `AC-2` gọi **hàm thật** so **mọi** ô; ⛔ dựng lại SQL tay *(`11` §6: 2/35 ⟷ 18/35)*.
2. **Ảnh lưới đổi nghĩa làm hỏng chỗ khác** — `Ctrl+Z` *(`ST.lich`)*, ô tìm, `_dat` đang đọc `r.<f>`/`o.cu` theo nghĩa thô; đổi một nửa là để `Ctrl+Z` khôi phục giá trị **thô** lên ô đang in Final. Phạm vi `(b)` đòi `grep` + bảng `đổi / giữ`.
3. **`WO-060` cùng tệp** — giữ thứ tự *(phiếu này trước)*; `WO-060` dựng trên mã của phiếu này.

## Changelog
- 2026-10-06 · `fls-ba` · phát **`WO-062`** `MO` từ `KQ-061` `F-2` *(ngoài phạm vi `WO-023` — lưới thô)* + `F-1` *(lô lưu hết giờ — cùng đường người đi, cùng `man_f02.js`)*; đo lại `Đ1` mã @ `7b4237f` + sổ thật chỉ `SELECT` *(cột nguồn rỗng **8.387 / 8.387** ⇒ phiên sửa thật đầu tiên gặp **100%**; câu đọc mới **3,28 ms**/501 dòng)*; spec `BA-06` **v4.24** §3c ⑪ + `ⓕ3` · `BA-07` **v3.14** · `BA-05` **v0.35** `ⓓf`. PO nâng ưu tiên **CAO** *(chặn `C1` ngay lượt sửa đầu)*; thứ tự `WO-051` → **`WO-062`** → `WO-060` → `WO-047` → `WO-015`.
