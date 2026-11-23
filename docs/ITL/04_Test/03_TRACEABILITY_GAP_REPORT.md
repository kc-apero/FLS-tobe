# 03 — TRACEABILITY & GAP REPORT

> ⏸ **BẢN COPY CHƯƠNG TRÌNH — CHƯA DẪN XUẤT CHO ITL.** Nội dung dưới đây là scope chương trình FIN ERP, **chưa phải spec dự án ITL**. Sẽ viết lại theo `_DOC_REWRITE_ROADMAP.md`. Đừng dùng làm căn cứ build ITL.

**Version:** v0.18 (sống) | **Chủ sở hữu:** QA

---

## 1. Ma trận truy vết (cập nhật mỗi khi thêm test)

| Spec | Tổng mục | Bài **gọi tên** mục | Gap |
|---|--:|--:|---|
| `BA-11` INV | **22** *(`I01`…`I22`)* | **10** *(`I03`·`I04`·`I05`·`I08`·`I13`·`I14`·`I16`·`I20`·`I21`·⭐`I22`)* — đo `KQ-007` 01/10 tối: `grep -rhoE "INV-I[0-9]{2}" tests/` trên tệp chữ | ⛔ **12 bất biến ⛔ không bài nào gọi tên** *(`I22` mới sinh **đã kèm** bài gọi tên nó — lần thứ hai sau `I21`)* |
| `BA-09` SM | 16 T + 8 F | ⛔ **chưa đếm được** | máy trạng thái ⛔ chưa có mã định danh trong tên bài |
| `BA-10` DT | ~20 nhánh | ⛔ **chưa đếm được** | như trên |
| `BA-03` US | **56** *(`001`…`056`)* | ⛔ **chưa đếm được** | như trên |
| `BA-04` RP/SoD | ma trận + 4 SoD | ⛔ **chưa đếm được** | như trên |
| `BA-07` ERR | 10 mã | ⛔ **chưa đếm được** | như trên |

⭐ **Đo `2026-09-18` tối muộn:** **1.712** bài xanh · **145** tệp test · **44** tệp có nhắc một mã `INV`.

> ⭐⭐ **`INV-I21` là bất biến ĐẦU TIÊN ra đời ĐÃ CÓ SẴN bài gọi tên nó** *(`QĐ-ITL-143`)*. Bảy cái trước được gọi tên **về sau**, khi ai đó tình cờ viết mã vào chú thích. ⇒ Nếu giữ nếp này thì cột *«bài gọi tên»* tự lớn theo, ⛔ không cần một đợt truy ngược.

⛔⛔ **Cột *"Bài gọi tên mục"* ⛔ KHÔNG phải cột *"đã phủ"*.** Nó chỉ đếm những bài **viết mã spec vào tên hoặc chú thích** — một phép đo **máy làm được**, và cố ý **hẹp hơn** sự thật. ⭐ Chỗ ghi `⛔ chưa đếm được` là **thật**: `BA-09`/`BA-10`/`BA-03` ⛔ **không có** mã định danh nào xuất hiện trong mã test, nên ⛔ **không có gì để đếm** — và tôi ⛔ **không** dựng bảng bằng cách suy từ tên hàm *(`R-A1`)*.

⇒ ⭐⭐ **Việc đáng làm trước tiên ⛔ không phải viết thêm test — là ĐẶT MÃ SPEC vào tên bài**, để cột này **đo được** thay vì đoán. `INV` làm được điều ấy vì nó **đã có** thói quen ghi mã; năm spec còn lại thì chưa.

> ⛔⛔ **Câu *"dự án chưa code"* ngay trên đây HẾT ĐÚNG từ 26/08 — sửa 2026-09-07.** Thực đo hôm nay: **1.104 phép thử xanh · 49 tệp · 8.786 dòng `fls/`**, năm pha `P0`…`P5` xong, ba màn chạy thật, **17 cổng chung**. ⇒ **Cột *Có code test* của bảng trên ⛔ KHÔNG còn là `0`** — nó chỉ **chưa ai truy ngược** về từng mục `BA-09`/`BA-10`/`BA-11`.
>
> ⚠ **Và đó mới là điều đáng ghi:** banner `⏸` đầu tệp nói *"chưa dẫn xuất cho ITL"* — đúng — nhưng nó **⛔ không** làm câu *"dự án chưa code"* trở thành vô hại. **Một tệp treo `⏸` vẫn nói dối được**, và tệp này đã nói dối **12 ngày**. ⛔ Tôi ⛔ **không** dựng bảng truy vết bằng cách suy từ tên test *(`R-A1`)*; việc dẫn xuất thật vẫn là việc của QA.

### 1.1 ⭐ `QĐ-ITL-149` · `SM-I06` · `DT-I14` → bài *(`KQ-005`, 2026-10-01 — `fls-test` đọc spec rồi tìm bài, ⛔ suy từ tên hàm)*

> Ba spec **mới v0.5/v0.6** ra đời 01/10 **đã mang mã** *(`F-1`…`F-9`, nhánh `1`…`8`)* ⇒ lần đầu `BA-09`/`BA-10` có thứ để đếm. Cột *Bài* ghi bài **chạy thật** hành vi ấy; *"gọi tên"* = bài viết mã spec trong docstring.

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `SM-I06 F-1` ghép dòng đã ghép | `409 DaGhep` | `tests/repo/test_ghep_lenh_pg.py::test_TU_CHOI_khi_dong_DA_ghep__kem_moi_noi_dang_co` · `tests/api/test_cua_ghep_pg.py::test_ghep_LAN_HAI_thi_409_kem_moi_noi_dang_co` | ⛔ | ✅ xanh |
| `SM-I06 F-2` bỏ lẻ | cửa `unmatch` + `pm_line_ids` ⇒ `400` | `tests/repo/test_bo_moi_noi_pg.py::test_bo_CA_CHUM_ba_moi_noi__Σ_khong_bao_gio_lech` *(tầng repo)*; tầng **cửa**: ⚠ chỉ đo tay ở `KQ-005` *(gọi `xu_ly.bo_ghep`, `conn=None` ⇒ `LoiCua`)* | ⛔ | ⚠ thiếu bài cửa |
| `SM-I06 F-3` kỳ `locked` | `KyDaChot`, kể cả `force` | `test_ghep_lenh_pg.py::test_TU_CHOI_ky_DA_CHOT__ke_ca_force` · `test_bo_moi_noi_pg.py::test_ky_DA_CHOT_thi_KHONG_bo` | ⛔ | ✅ |
| `SM-I06 F-4` bỏ dòng chưa ghép | `KhongCoMoiNoi` | `test_bo_moi_noi_pg.py` *(`:261`, `:269`)* | ⛔ | ✅ |
| `SM-I06 F-5` Σ lệch / khác tiền tệ | `422`, ⛔ ghi | `test_ghep_lenh_pg.py::test_TU_CHOI_khi_Σ_lech__va_KHONG_ghi_gi` · `::test_TU_CHOI_khi_tien_te_khac_nhau__kiem_TRUOC_Σ` · `test_cua_ghep_pg.py::test_Σ_lech_thi_422_va_KHONG_ghi_gi` | ⛔ | ✅ |
| `SM-I06 F-6` `UPDATE`/`DELETE` | ⛔ đường mã nào | ⛔ **không bài** — chỉ giữ bằng mã *(`GAP-DB-06`, `NFR-I01`)* | — | ⛔ gap *(spec tự khai)* |
| `SM-I06 F-7` ghép đổi Final | gợi ý → `fls_may_goi_y`, `fls_sua_tay` +0 | `tests/repo/test_wo003_ghep_tay_la_goi_y_pg.py::test_ghep_TAY_hd_cdt1_vao_fls_may_goi_y__Final_KHONG_doi` · `::test_cong_C8_KHONG_lat_khi_chi_co_cu_ghep` | ✅ | ✅ |
| `SM-I06 F-8` bỏ ghép đảo giá trị người | ⛔ đảo, khai `bo_qua` | `test_wo003…::test_bo_ghep_KHONG_dao_gia_tri_NGUOI__va_KHAI_trong_bo_qua` · ⭐ `tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py` *(`bo_qua` ⛔ được chứa thứ người ⛔ gõ — `xfail strict`, `KQ-005 F-2`)* | ✅ | ⏳ đỏ `F-2` |
| `SM-I06 F-9` thiếu `reason` | nhận, điền `(may dien)` | `test_wo003…::test_ghep_va_bo_ghep_THIEU_ly_do__…` · `tests/nghiem_thu/test_kq002_than_man_ghep_qua_cua_that.py` ×2 *(gỡ `xfail` ở `KQ-005`)* | ✅ | ✅ |
| `SM-I06` chuyển `da_ghep_* → chua_ghep` | đảo **mọi** gợi ý gắn `match` | `test_wo003…::test_bo_ghep_dong_ghep_TAY__…` · `::test_bo_ghep_dong_MAY_ghep__…` · ⭐ `tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py` ×2 *(gợi ý **chồng** — `xfail strict`, `KQ-005 F-1`)* | ✅ | ⏳ đỏ `F-1` |
| `DT-I14` nhánh 1 *(người đã chốt)* | ⛔ ghi, `nguoi_da_chot` | `test_wo003…::test_NGUOI_da_chot_hd_roi_moi_ghep__…` | ✅ | ✅ |
| `DT-I14` nhánh 2 *(gợi ý trùng)* | ⛔ thêm dòng | `test_wo003…::test_goi_y_TRUNG_gia_tri_dang_co__KHONG_them_dong` | ✅ | ✅ |
| `DT-I14` nhánh 3 *(ghi gợi ý)* | `nguon='may_goi_y'`, actor người | `test_wo003…::test_ghep_TAY_hd_cdt1_vao_fls_may_goi_y__…` | ✅ | ✅ |
| `DT-I14` nhánh 4 *(N dòng lệch)* | `khong_suy_duoc` | `test_wo003…::test_N_dong_lenh_noi_KHAC_nhau__khong_suy_va_KHONG_goi_y` | ✅ | ✅ *(ca trộn rỗng/có ⛔ khai — `KQ-005 F-3`)* |
| `DT-I14` nhánh 5 *(mọi dòng rỗng)* | ⛔ ghi | ⛔ **không bài gọi tên** | — | ⛔ gap |
| `DT-I14` nhánh 6 *(đảo gợi ý còn hiệu lực)* | ĐẢO, `nguon` giữ | `test_wo003…::test_bo_ghep_dong_ghep_TAY__dao_goi_y__fls_may_goi_y_ve_0` | ✅ | ✅ |
| `DT-I14` nhánh 7 *(bị đè ⇒ ⛔ làm gì)* | — | ⭐ `test_kq005_bo_ghep_dao_ca_goi_y_chong.py` — **chính nhánh này đẻ ra gợi ý mồ côi** | ✅ | ⏳ đỏ `F-1` *(gửi `BA`)* |
| `DT-I14` nhánh 8 *(`sua_tay` cũ)* | ĐẢO | `tests/repo/test_bo_moi_noi_pg.py` *(bài đảo cũ, viết lại ở `WO-003`)* | ⛔ | ✅ |
| `QĐ-ITL-149` *(`BA-07 §4h ⓼`)* `match-lo` giữ bắt buộc | `400` | `tests/api/test_cua_ghep_lo_pg.py::test_cua_LO_thieu_ly_do_VAN_400…` ×3 | ⛔ | ✅ |
| `DD-I15 ⓒ` `run_pm` | ghi ảnh PM | `tests/nghiem_thu/test_kq002_ghep_tay_ghi_run_pm.py` *(gỡ `xfail`)* · `test_wo003…::test_ghep_TAY_ghi_run_pm_bang_anh_PM_da_dung` | ✅ | ✅ |
| `BA-06 C10` tải ≠ rỗng | `Đang hỏi sổ…` | `tests/nghiem_thu/test_kq002_man_ghep_dang_tai_khong_noi_da_sach.py` ×2 *(gỡ `xfail`)* + đo máy 8088 *(`KQ-005` AC-10)* | ✅ | ✅ |

⇒ **`SM-I06`: 9 chuyển cấm — 8 có bài chạy hành vi, 1 (`F-6`) gap đã khai; 4/9 bài gọi tên mã.** **`DT-I14`: 8 nhánh — 7 có bài, nhánh 5 ⛔ bài; 2 nhánh (`7`, và chuyển bỏ ghép) đang đỏ ở `KQ-005`.**

> ⚠ Bảng §1.1 là **biên bản `KQ-005`** *(v0.5)* — giữ nguyên. Trạng thái **sau** `WO-003` vòng 2 ở §1.2: các dòng `⏳ đỏ` trên đã **xanh**.

### 1.2 ⭐ `WO-003` vòng 2 — `INV-I22` · `SM-I06 F-10`/`F-11` · `DT-I14` `5a`/`6`–`8` → bài *(`KQ-007`, 2026-10-01 tối — đọc `BA-10` v0.7 · `BA-11` v0.15 · `BA-09` v0.6 rồi tìm bài)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `INV-I22 ⓐ` *(một dòng sau bỏ ghép: 0 gợi ý chưa đảo, mọi lớp)* | đếm `fls_adjustment` gắn `match`, `NOT EXISTS` bản đảo = 0 | `tests/repo/test_wo003_vong2_bo_ghep_moi_lop_pg.py::test_BA_lop_goi_y_chong__…` · `tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py` ×2 *(gỡ `xfail`)* · ⭐ `tests/nghiem_thu/test_kq007_bo_ghep_moi_lop_pha_them.py` ×3 *(5 lớp + người · máy `hinh='A'` · 3 vòng)* | ✅ | ✅ xanh |
| `INV-I22 ⓑ` *(toàn sổ: 0 gợi ý chưa đảo trên dòng 0 mối nối)* | — | ⛔ **không cổng sổ** *(spec tự khai "chỉ bài thử")*; đo tay `KQ-007` trên sổ thật: **0** / **4.424** | — | ⚠ chỉ bài + đo tay |
| `SM-I06 F-10` *(gợi ý mồ côi sau bỏ ghép)* | `fls_may_goi_y` của dòng = 0 | như `INV-I22 ⓐ` | ✅ | ✅ xanh |
| `SM-I06 F-11` *(`bo_qua` mang bút toán máy)* | `bo_qua` chỉ giá trị người, ≤ 1 mục/ô | `tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py` ×2 *(gỡ `xfail` 1)* · `test_wo003_vong2…::test_bo_qua_moi_O_nhieu_nhat_MOT_muc_va_CHI_gia_tri_nguoi` · `::test_bo_qua_KHONG_khai_o_ma_dong_CHUA_tung_co_goi_y` · ⭐ `test_kq007…::test_but_toan_ghep_CU_sua_tay_o_TREN_gia_tri_nguoi__bo_qua_HIEN_nguoi` | ✅ | ✅ xanh |
| `DT-I14` nhánh `5a` *(ca TRỘN rỗng + `v`)* | xử như "đồng ý `v`" | `test_wo003_vong2…::test_ca_TRON_dong_rong_hd_va_dong_co_hd__goi_y_gia_tri_co` *(ghim; đỏ khi bỏ `discard("")` — đột biến `M4`)* | ✅ | ✅ xanh |
| `DT-I14` nhánh `6` *(đảo gợi ý chưa có bản đảo — bất kể lớp)* | ĐẢO, `nguon` + `value_before` của chính lớp | `test_wo003_vong2…::test_BA_lop_goi_y_chong__…` *(đọc nhật ký `[C-1, HD-A, HD-B, HD-C]`)* · `test_kq005…` ×2 · `test_kq007…` ×3 | ✅ | ✅ xanh |
| `DT-I14` nhánh `7` *(đã có bản đảo ⇒ ⛔ làm gì)* | ⛔ đảo hai lần | `test_wo003_vong2…::test_ghep_BO_ghep_lai_BO__KHONG_bao_gio_dao_HAI_lan` · ⭐ `test_kq007…::test_BA_vong_ghep_bo_co_lop_chong__…` *(cả hai đỏ khi bỏ `NOT EXISTS` — `M2`)* | ✅ | ✅ xanh |
| `DT-I14` nhánh `8` *(`sua_tay` cũ — bất kể lớp)* | ĐẢO, `nguon='sua_tay'`, người nguyên | `test_wo003_vong2…::test_but_toan_ghep_CU_sua_tay_o_LOP_DUOI_gia_tri_nguoi__…` *(lớp dưới)* · ⭐ `test_kq007…::test_but_toan_ghep_CU_sua_tay_o_TREN_…` *(lớp trên)* | ✅ | ✅ xanh — ⚠ nhật ký lớp dưới đọc như "ô bị xoá" *(`KQ-007 F-1`, gửi `BA`)* |
| `DT-I14` *Định nghĩa `bo_qua`* | mục = dòng `fls_sua_tay` ⛔ gắn `match` trên ô từng có `match` | như `SM-I06 F-11` · đột biến `M3`/`M5`/`M6` đều bị bắt | ✅ | ✅ xanh |

⇒ ⭐ **Vòng 2: 9 mục — 8 có bài chạy hành vi, cả 8 gọi tên mã; 1 (`INV-I22 ⓑ`) chỉ có đo tay, spec tự khai.** Mỗi bài `kq007` **đỏ trên `38a6b08`** *(mã vòng 1)* trước khi được tin; sáu đột biến của `KQ-007` *(`M1`…`M6`)* đều làm ≥ 1 bài đỏ.

### 1.3 ⭐ `WO-001` — `QĐ-ITL-150 ⓐ` · `10 §6` · `09` §2 mốc `B` → bài *(`KQ-010`, 2026-10-01 tối)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `WO-001 T1a` *(sự kiện MÁY ⛔ là người)* | `actor = MAY` ⇒ đếm 0 | `tests/test_kiem_so_song.py::test_T1a_*` ×3 · `tests/nghiem_thu/test_kq002_moc_b…::test_su_kien_cua_MAY_…` *(gỡ `xfail`)* · ⭐ `tests/nghiem_thu/test_kq010…::test_MAY_ghep_thi_moc_B_DUNG_YEN` *(cửa ghi thật `ghi_goi_y_may`)* | ✅ | ✅ xanh |
| `QĐ-ITL-150 ⓐ` *(UAT ⛔ là người — `B2/3/5`)* | lý do bắt đầu `UAT ` ⇒ 0 | `test_kiem_so_song.py::test_T1b_dong_UAT_dem_0_nguoi` · `::test_T1b_UAT_phai_o_DAU_ly_do` · ⭐ `test_kq010…::test_UAT_ghep_roi_bo_ghep_…` | ✅ | ✅ xanh |
| `QĐ-ITL-150 ⓐ` *(UAT ⛔ là người — `B4`)* | bỏ ghép UAT ⛔ đếm; bỏ ghép thật của chính owner **đếm** | `test_kiem_so_song.py::test_T1b_bo_ghep_UAT_KHONG_dong_not_B4` · ⭐ `test_kq010…::test_OWNER_bo_ghep_THAT_thi_B4_DEM__…` *(bắt đột biến lọc theo actor — bài Dev ⛔ bắt)* | ✅ | ✅ xanh |
| `WO-001 AC-2b` *(lý do `(may dien)` là người)* | đếm 1 | `test_kiem_so_song.py::test_T1b_ly_do_MAC_DINH_…` *(khuôn CTE)* · ⭐ `test_kq010…::test_NGUOI_ghep_KHONG_ly_do_…` *(`ghep_lenh(reason=None)` thật ⇒ `1·1·3 → 4·1·0 → 5·0·0`)* | ✅ | ✅ xanh |
| `done` của người, `reason NULL` | đếm 1 | ⭐ `test_kq010…::test_NGUOI_bam_XONG_khong_ly_do_…` *(bắt đột biến bỏ `coalesce`)* | — | ✅ xanh |
| `WO-001 T2` *(dấu sổ = lượt nạp SỔ)* | `_Q_GIO` | `test_kiem_so_song.py::test_T2_dau_SO_…` | ✅ | ✅ xanh |
| `WO-001 T4` *(`B5` neo `BA-06`, `C5`/`C5b`)* | `khop_owner --kiem` | ⛔ **không bài pytest** — cổng giấy tự khai `mong`; chiều ĐỎ đo tay `KQ-010` *(`K1`/`K2`/`K3`)* | — | ⚠ chỉ cổng + đo tay |
| `QĐ-ITL-150 ⓐ` *("bất kỳ cổng người đã làm": `C8`, `G-d`)* | — | ⛔ **chưa có** — `KQ-010 F-2 ⓓ` gửi `BA` | — | ⏳ |

⇒ **8 mục — 6 có bài chạy hành vi; `T4` chỉ cổng giấy; vế `C8`/`G-d` chưa khai.** Bài `kq010` đỏ trên mã `ee390cb` *(2 bài)* và dưới 6 đột biến *(`M1`·`M2`·`M3`·`M4`·`M5`·`M7`)*.

### 1.15 ⭐ `WO-023` — `BA-06` **v4.22–v4.23** §4.5 `ⓕ1`…`ⓕ4` *(v4.23: `ⓕ3` vế `Gán` + khuôn chung)* · `ⓦ` ④ ⑤ ⑥ · dòng *"F02 · nhật ký"* ⓐ…ⓔ · *"F02 · hoàn tác"* ⓐ…ⓒ *(v4.12, `TL-058` giữ)* · `BA-07` **v3.13** *(§5 ba mã `409`; §3 `la_ban_dao` · `but_toan[].nguon`; `GAP-API-12` nợ)* → bài *(`KQ-061`, 2026-10-06)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `ⓦ` ⑥ lựa chọn ứng viên theo `itl_id` | ⛔ còn ⇒ `null`, 0 `POST`; còn ⇒ tô vị trí mới; `xac_nhan` về `false` | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py` ×5 · `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F3_*` · Chrome 8099 *(`KQ-061`: mã cũ `POST /queue/4267/match` **200**, mã mới **0**)* | ✅ | ✅ xanh `d1cea7c` · đỏ `7e67a09` · ⭐ `kq050 F3` **gỡ dấu** |
| `ⓦ` ⑤ ⓐ `Gán` lỗi ⇒ dòng lỗi + khoá nút | `422` ⇒ *"Gán chưa xảy ra — Cửa lỗi:"*; treo ⇒ 1 `POST` | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC10_*` ×2 · Chrome 8099 *(4 cú bấm khi treo ⇒ 1 `POST`)* | ✅ | ✅ |
| `ⓦ` ⑤ ⓑ · ④ `Thử lại` · ④ hàng lỗi ô tìm | 0 `Uncaught`; một lượt | `test_wo023_h_*::test_AC11_*` ×2 · `::test_AC12_*` ×2 · `::test_AC14_*` · `kq050::test_F2_*` | ✅ | ✅ · `kq050 F2` **gỡ dấu** |
| `ⓕ1` hộp modal với bàn phím | `Esc` một lớp; phím màn nằm im; hai thứ tự | `tests/web/test_wo023_ab_hop_modal_va_hop_cho_cua.py` *(27)* · `kq021::test_F1_*` ×2 *(bỏ bản chép trình nghe)* · Chrome 8088 hộp thật ① | ✅ | ✅ · **gỡ dấu** ×2 |
| `ⓕ2` hộp chờ cửa ⛔ đóng | `Esc`/nền nuốt; dòng *"Đang ghi vào sổ…"*; lỗi trong hộp | `test_wo023_ab_*::test_AC2_*` · `kq021::test_F2_*` · Chrome 8099 chùm thật | ✅ | ✅ · **gỡ dấu** |
| `ⓕ3` hạn chờ ghi `30 s` — `Bỏ gán` · `Gán` *(v4.23)* | *"Chưa rõ … đã xảy ra chưa"* | `tests/web/test_wo023_cd_het_gio_va_cau_409.py::test_AC3_*` ×6 · Chrome 8099 hạn **thật** *(30,10 s / 30,09 s)* | ✅ | ✅ |
| `ⓕ3` — lô lưu `F02` *(spec ⛔ kể)* | ⛔ khẳng định *"CHƯA vào sổ"* khi hết giờ | ⭐ `tests/nghiem_thu/test_kq061_f02_het_gio_lo_luu.py::test_F1_*` | ✅ | ⛔ **`xfail(strict)`** — `KQ-061 F-1` |
| `ⓕ4` ba mã `409` | 4 ca 4 mã qua cửa thật | `tests/api/test_wo023_d_ma_409_pg.py` ×3 · `test_wo023_cd_*::test_AC4_*` · cửa HTTP 8099 *(Test tự gọi)* | ✅ | ✅ |
| *"F02 · nhật ký"* `la_ban_dao` | đảo người ≠ xoá ô | `tests/repo/test_wo023_f_la_ban_dao_pg.py` ×3 · `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py` · ⭐ `kq019::test_nhat_ky_SO_THAT_*` *(viết lại `TL-058`, sổ thật 4.428 dòng)* · Chrome 8088 `27728` | ✅ | ✅ · vế `xoá ô` sổ thật **0** mẫu *(chỉ kho TEST)* |
| *"F02 · hoàn tác"* hộp `Đảo` theo lớp | máy ⇒ *"không đổi Final"* | `test_wo023_fg_*::test_AC9_*` ×2 · Chrome 8088 `#163563` / `#152383` | ✅ | ✅ |
| `WO-023 (e)` khối `SINH-KHOP` chỉ quan hệ | thêm cụm ⇒ vẫn ĐẠT; xoá ⇒ lật | `tests/test_wo023_e_khoi_sinh_khop_chi_quan_he.py` ×14 · đột biến Test trên worktree *(mới rc 0 / cũ rc 1)* | ✅ | ✅ |
| `WO-023 (j)` bài `AC7_doi_MUC_PHU` tự đủ | xanh khi kho có thêm ca | `test_wo045_…::test_AC7_doi_MUC_PHU_*` *(kho TEST 719 dòng VND: mới xanh · bản `7ec2dc0` đỏ)* | ✅ | ✅ |
| *(spec ⛔ khai)* `GET /ledger` lưới: thô hay Final | ô vừa ghi hiện lại sau tải | ⛔ chưa có bài | — | ⏳ `KQ-061 F-2` → `BA` |

⇒ **13 mục — 11 xanh**; **5** `xfail(strict)` cũ **gỡ** *(`kq021` ×3 · `kq050` ×2)*; **1** `xfail(strict)` mới *(`KQ-061 F-1`)*; **1** mục spec thiếu *(`F-2`)*. Dòng `ⓦ` ⑤ + `ⓦ` ④ `Thử lại` của **§1.14** nay ✅.

### 1.14 ⭐ `WO-045` — `BA-06` **v4.19–v4.21** §4.5 `ⓥ` ⑤ *(nút `Thử lại` `②b`; v4.21 đính chính lớp `b tiny`)* · `ⓦ` ① *(lượt mới nhất thắng ở mọi màn)* · ② *(chỉ đọc khoá **chỉ** GHI)* · ③ *(v4.20 `title` ⛔ số đo; v4.21 đếm sau khi bỏ `QĐ-ITL-\d+`)* · ④ *(v4.21 năm trạng thái vùng ứng viên)* · ⑤ *(v4.21 lỗi cú bấm ⛔ ra console)* → bài *(`KQ-050`, 2026-10-05)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `ⓦ` ① ưu tiên ① `F01G` `mo_lenh` *(#2)* — đổi lệnh khi đang tải | lượt lệnh trước về sau / trước / lỗi ⇒ ứng viên **chỉ** của `ST.mo` | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC1_*` ×4 · Chrome 8099 *(`KQ-050` bảng ①)* | ✅ | ✅ xanh `2b804e3` · ĐỎ `14a4b72` *(Test chạy lại 25/26)* |
| `ⓦ` ① ① — cú `Gán` ⛔ mang `itl_id` lệnh khác | ⭐ cặp sai **cùng tệ trong dung sai** | `test_wo045_…::test_AC2_*` ×2 · ⭐ `tests/nghiem_thu/test_kq050_cap_sai_cung_tien_te.py::test_kq050_GAN_sau_khi_luot_lenh_TRUOC_ve_muon_*` *(DOM, ca VND–VND)* · Chrome 8099 | ✅ | ✅ · ĐỎ `14a4b72` `[1, 2] ≠ [2, 1]`; Chrome mã cũ `POST /queue/4161/match` ⇒ **`200`** *(lọt)*, mã mới ⛔ |
| ⭐ *Sự thật* cửa ghi *(`WO-045` "Câu còn treo")* | cặp sai trong dung sai ⇒ **nhận** *(`mong 200`)*; cặp đúng mã lệch 1.500 ⇒ `422` | ⭐ `test_kq050_cap_sai_cung_tien_te.py::test_kq050_SU_THAT_cua_ghi_NHAN_*` | ✅ | ✅ *(canh cửa — đổi luật ⇒ ĐỎ, khai lại)* |
| `ⓦ` ① ① `tai_toan_so` *(#3)* — hai chữ cùng bay | chữ mới thắng | `test_wo045_…::test_AC3_*` | ✅ | ✅ |
| `ⓦ` ① + `WO-045` bảng *Màn hình* hàng **lỗi** — lượt **chữ** mới nhất lỗi khi lệnh mới đang tải | ⛔ khung tải treo; `⛔ Cửa lỗi:` | ⭐ `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_*` | ✅ | ✅ **gỡ dấu** `KQ-061` *(vá `WO-023 (h)` ⓔ)* · ~~`xfail(strict)`~~ |
| *(spec ⛔ nói)* lượt mới nhất thay danh sách ⇒ lựa chọn cũ? | `Gán` ⛔ gửi hàng người ⛔ chọn | ⭐ `test_kq050_vung_ung_vien_luot_tim.py::test_F3_*` | ✅ | ✅ **gỡ dấu** `KQ-061` *(vá `WO-023 (i)`)* · ~~`xfail(strict)`~~ |
| `ⓦ` ① ② `F01L` `_loc` → `ve_luoi` *(#6)* · `Xem thêm` *(#7)* | lưới **một** rổ; `Xem thêm` hai lần ⇒ 1 `GET` | `test_wo045_…::test_AC4_*` ×3 · `::test_AC5_*` · Chrome 8088 *(ba rổ; giữ `cursor=` + bấm hai lần ⇒ **1** `GET`)* | ✅ | ✅ |
| `ⓦ` ① ③ `F01` `ve_luoi` *(#10)* · `_xem_them` *(#11)* | lọc cuối thắng; ⛔ trùng | `test_wo045_…::test_AC7_*` ×4 · Chrome 8088 *(giữ VND, bấm USD ⇒ 50 hàng USD; USD lật hết **3.980** = `dem_hang_cho`)* | ✅ | ✅ · ⚠ `AC7_doi_MUC_PHU` phụ thuộc toàn kho TEST — `KQ-050 F-4` |
| `ⓦ` ① ④ `F04` `_mo_chup` *(#17)* · `_ve_thu_tu` *(#18)* | màn + `S.chup` + `S.thu_tu` = ảnh bấm cuối | `test_wo045_…::test_AC8_*` ×2 · Chrome 8088 *(`163589` thắng `163591`; ô `8.978`)* | ✅ | ✅ |
| `ⓦ` ② chỉ đọc: `Xem thêm` · `Tìm tiền` **chạy**; `Ghép`/nút ghi **khoá** + `405` | hai chế độ | `test_wo045_…::test_AC6_*` ×5 · Chrome 8088 *(`may` 120/120 · `nguoi` 616/616 · `khong` 801/801; hộp mở, `Ghép` khoá + `405`, bấm ⇒ 0 `POST`)* | ✅ | ✅ |
| `ⓦ` ③ `title` thanh lằn = chuỗi ⓐ; chữ số ngoài `QĐ-ITL-\d+` = 0 | oracle đọc `06_SCREEN_SPEC.md` | `tests/web/test_wo045_thanh_lan_khong_so_cung.py` ×2 · Chrome 8088 | ✅ | ✅ |
| `ⓦ` ④ vùng ứng viên **tải** · **lỗi** · **mất kết nối** · **có dữ liệu** | chữ + lớp của `②b` | `test_wo045_…::test_AC1_loi_*` · Chrome 8088 *(`Đang hỏi sổ…` info · `⛔ Cửa lỗi:` crit ×2 · 50 = 50)* | ✅ | ✅ · **rỗng** ⛔ đo *(sổ thật ⛔ có ca)* · nút `Thử lại` ⏳ `WO-023 (h)` |
| `ⓦ` ⑤ ⓐⓑ lỗi cú bấm ⛔ `Uncaught` · ⓒ `F04` `S.chup` khi ảnh mới tải | — | ⛔ **chưa có bài** *(Chrome đo: `Uncaught` 8099 **1** · 8088 **2**)* | — | ⏳ `WO-023 (h)` · `GAP-SCR-35` |
| `ⓥ` ⑤ nút `Thử lại` `②b` lớp `b tiny` *(v4.21)* | lỗi + mất kết nối; bấm ⇒ **một** lượt | `test_wo045_…::test_AC9_*` ×2 · Chrome 8088 *(`b tiny`; 3 `GET` = một lượt; 736 dòng)* | ✅ | ✅ |

⇒ **14 mục — 10 xanh**; **2** `xfail(strict)` mới *(`KQ-050 F-2` · `F-3`)*; **1** mục chờ `WO-023 (h)` / `GAP-SCR-35` *(`ⓦ` ⑤)*; `ⓦ` ④ vế **rỗng** ⛔ đo. Hai dòng ⏳ `WO-045` của **§1.13** nay ✅.

### 1.13 ⭐ `WO-042` — `BA-06` **v4.18** §4.5 `ⓤ` đoạn v4.18 *(bốn chuỗi `F01L` + `LY_DO_LO`)* · `ⓥ` ①…④ ＋ đoạn **v4.19** *(① dừng ngay · ⑤ `Thử lại`)* · `ⓦ` *(v4.19)* · `BA-07` **v3.11** §4g `TAP_TRANG_TIEN_TE` · `BA-13` **v1.9** → bài *(`KQ-046`, 2026-10-05)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `ⓥ` ① đổi sang chip khác khi đang tải ⇒ lượt cũ bị bỏ *(⛔ `ST.dong` · cờ tải · lỗi · con trỏ)* | hai thứ tự về *(cũ về sau / trước)* ⇒ chỉ hàng chip mới | `tests/web/test_wo042_doi_chip_khi_dang_tai.py::test_AC1_*` ×3 · ⭐ `tests/nghiem_thu/test_kq041_…::test_F3_doi_chip_KHI_DANG_TAI_*[cu_ve_SAU]` · `[cu_ve_TRUOC]` *(cửa giả **giữ**, viết lại `KQ-046`)* · Chrome 8088 ⓐ | ✅ | ✅ xanh `db0adae` · ĐỎ đúng lý do `77737f7` · 8088 `2219` *(đối chứng `2955`)* |
| `ⓥ` ① đoạn v4.19 — lượt bị thay **được dừng ngay** | ⛔ đòi lượt cũ xin tiếp; gác đếm **theo đường** | `kq041::test_F3_doi_chip_*` *(gác `goi_cho ≥ 1 ∧ goi_da ≥ 1`)* · Chrome 8088 ⓐ *(6 `GET`: lượt cũ dừng sau 1 trang)* | ✅ | ✅ |
| `ⓥ` ② bấm lại chip **đang chọn** khi đang tải ⇒ **0** `GET` thêm *(cả `doi_chip` lẫn `mo_man`)* | số `GET` = một lượt *(mỏ neo)*; mỗi lệnh một lần | `test_wo042_…::test_AC2_*` ×2 · ⭐ `kq041::test_F3_bam_lai_chip_DANG_CHON_*` *(số `GET` từ mỏ neo, ⛔ gõ 2)* · Chrome 8088 ⓑ | ✅ | ✅ `goi 2 = 2` · 8088 `736` / **3** `GET` *(đối chứng `1472` / 6)* |
| `ⓥ` ③ năm trạng thái **chỉ** của lượt mới nhất; lỗi lượt cũ ⛔ hiện | tải giữ tới khi lượt mới xong | `test_wo042_…::test_AC3_*` ×5 · `kq041 …[cu_ve_TRUOC]` *(ảnh giữa: `dang_tai true · n 0`)* · Chrome 8088 `?gia_lap=` ×4 | ✅ | ✅ *(lỗi / mất kết nối "như cũ" — `TL-043`)* |
| `ⓥ` ④ đổi chip nhiều lần ⇒ màn = chip cuối | `Chưa → Đã → Chưa` · `Đã → Chưa → Đã` | `test_wo042_…::test_AC4_*` ×2 · Chrome 8088 + 8099 ⓒ | ✅ | ✅ 8088 `2219` *(đối chứng `4356 (⛔ chạm trần)`)* |
| `ⓥ` ⑤ *(v4.19)* nút `Thử lại` `②b` | — | `test_wo045_…::test_AC9_*` ×2 *(§1.14)* | ✅ | ✅ `WO-045` — `KQ-050` · ~~⏳ `WO-045`~~ |
| `ⓦ` *(v4.19)* lượt mới nhất thắng ở mọi màn *(16 hàm)* · chỉ đọc khoá **chỉ** GHI | — | §1.14 *(`test_wo045_*` 26 bài + `kq050` 4)* | ✅ | ✅ `WO-045` — `KQ-050` *(8088 lưới **120 / 120**)* · ~~⏳ `WO-045`~~ |
| `ⓤ` v4.18 ⓐ ghi chú băng · ⓑ `note ok` · ⓒ nhãn lọc · ⓓ `RO.may` · `LY_DO_LO` **một** hằng | so `textContent`; `<t>`/`<c>` từ cửa | `tests/web/test_wo042_bon_chuoi_f01l_cua_that.py` ×3 · `test_wo037_v2_bang_f01l_cua_that.py` · ⭐ Chrome 8088 + 8099 so với chữ **trích thẳng từ `BA-06`** *(regex, ⛔ chép tay)* | ✅ | ✅ 4/4 hai máy *(8088 `t 64 · c 120`; 8099 `t 1 · c 1`)* |
| `BA-07` v3.11 tập **30** = `isspace` ∪ `U+FEFF`; ⛔ `U+200B` | so tập; Python/PG/JS 30/30 | `tests/web/test_wo042_mot_tap_ky_tu_trang.py::test_AC8_*` ×6 · đo độc lập `KQ-046` *(kịch bản riêng)* | ✅ | ✅ 30/30 ×3 · `U+200B` giữ ×3 · điểm mã JS = Python |
| `BA-07` v3.11 SQL vế sổ `btrim(i.curr, %(tap)s)` — **cùng** luật `ma_tien_te` | dòng tiền biên ⇒ bậc `tien` ⟺ `ma_tien_te` khớp; `tong_cung_tien_te` = oracle Python | ⭐ `kq041::test_F2_ca_bien_HAM_THAT_ung_vien_itl_BANG_ma_tien_te` *(hàm thật, viết lại `KQ-046`)* · `kq041::test_CANH_ca_thuong_*_qua_ham_that` · `tests/api/test_wo042_mot_tap_cua_that_pg.py::test_AC10_1_*` | ✅ | ✅ 8/8 ca · ĐỎ **6/6** trên `77737f7` |
| `BA-07` v3.11 Python — **mọi** phép so tiền tệ gọi `ma_tien_te` *(kể cả cửa ghi)* | quét AST + JS + SQL; cửa ghi nhận BOM+VND | `test_wo042_mot_tap_ky_tu_trang.py::test_AC9_*` · `test_wo042_mot_tap_cua_that_pg.py::test_AC10_2_*` · `::test_AC10_3_*` | ✅ | ✅ theo chữ `AC-9` |
| `BA-07` v3.11 *"mọi phép so"* — **chiều ngược** `ung_vien_pm` *(vế lệnh `upper(l.curr)` trần)* | lệnh `' vnd '` / NBSP / BOM / NEL / U+3000 ⇒ bậc `tien` của dòng `VND` | ⭐ `tests/nghiem_thu/test_kq046_chieu_nguoc_ung_vien_pm_mot_tap.py::test_F1_*` *(`xfail(strict)`)* + mỏ neo | ✅ | ⛔ **`xfail(strict)`** — `KQ-046 F-1` *(5/5 lệch; sổ thật **0 / 276.028**)* |
| Sổ thật ⛔ đổi *(`AC-11`)* | `dem_theo_ro` cũ = mới; mép tập 0 / mẫu số | `test_wo042_mot_tap_ky_tu_trang.py::test_AC11_SO_THAT_*` · `kq041::test_CANH_ORACLE_*` · đo `KQ-046` hai commit | ✅ | ✅ **6/6** khoá · `0 / 8.387` · `0 / 276.028` |

⇒ **13 mục — 10 xanh** *(cửa thật + sổ thật chỉ đọc + Chrome có cửa sổ, đối chứng cùng máy)*; **2** mục chờ `WO-045` *(`ⓥ` ⑤ · `ⓦ`)*; **1** mục ghim `xfail(strict)` mới *(`KQ-046 F-1`)*. Ba dòng `xfail` `kq041` của **§1.12** nay ✅ *(viết lại theo `TL-043`, ⛔ gỡ dấu)*.

### 1.12 ⭐ `WO-037` *(vòng 1 + 2)* — `BA-07` **v3.10** §4g ⓹ *(rổ `may` theo cửa ghi · bảng chữ in `VI_SAO` · `btrim` · `nguoi_khac_tien_te`)* · §4h ⓵ dòng `bac` · ⓵' `the.vi_sao` · `BA-06` **v4.17** §4.5 câu thứ sáu + `ⓤ` · `BA-08` **v1.3** `NFR-I29` · `BA-13` **v1.8** → bài *(`KQ-041`, 2026-10-05)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| §4g ⓹ ⓐ rổ `may` ⇔ ∃ dòng khớp mã **cùng** tiền tệ; khớp mã **chỉ** khác tệ ⇒ `nguoi` + `ma_khop_khac_tien_te` | lệnh `K` ⇒ `nguoi`; thêm dòng VND ⇒ `may`; `' vnd '` = VND | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC1_*` ×4 · ⭐ `tests/nghiem_thu/test_kq041_…::test_CANH_ORACLE_ro_WO037_so_that_khop_tung_pm_line_id` *(oracle SQL tự viết, sổ thật chỉ đọc)* | ✅ | ✅ xanh · sổ thật lệch **0 / 1.601** `pm_line_id` · đột biến `xep_ro` cũ ⇒ ĐỎ |
| §4g ⓹ ⓑ `ung_vien_itl` / `the.gd` chưa gán ⛔ khác tệ | `gd` khác tệ rổ `may` **0** | `test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC2_SO_THAT_*` · `kq041::test_CANH_ORACLE_*` | ✅ | ✅ xanh · **0 / 184** *(nền 84 / 268)* |
| §4g ⓹ ⓓ `Chưa gán` ⛔ đổi | `may` ＋ `nguoi` | `kq041::test_CANH_ORACLE_*` *(từng rổ = oracle)* | ✅ | ✅ `800 = 800` |
| §4g *(v3.10)* `nguoi_khac_tien_te` luôn có = số `the.vi_sao` | khoá `int`, `0` khi rỗng | `tests/api/test_wo037_v2_ro_nguoi_hai_cau_pg.py::test_AC11_*` ×3 · `kq041::test_CANH_ORACLE_*` | ✅ | ✅ sổ thật **84 = 84 = 84** *(cửa · thẻ · oracle)* |
| §4g *(v3.10)* bảng chữ in `VI_SAO` ⛔ ký hiệu cấm | so chuỗi + `CAM` | `test_wo037_v2_ro_nguoi_hai_cau_pg.py::test_AC13_*` ×3 | ✅ | ✅ xanh · Chrome ký hiệu cấm **0** |
| §4g *(v3.10)* SQL vế sổ `btrim` — **cùng** luật `ma_tien_te` | dòng `' vnd '` ⇒ bậc `tien` | `test_wo037_v2_…::test_AC14_*` · `::test_AC15_*` ×5 · ⭐ `kq041::test_CANH_ca_thuong_*_qua_ham_that` *(viết lại `KQ-046`: hàm thật thay câu SQL của bài)* · `kq041::test_F2_ca_bien_HAM_THAT_*` | ✅ | ✅ ca thường **8/8** · ✅ biên *(`WO-042` — viết lại `KQ-046`; ~~⛔ `xfail(strict)` — `KQ-041 F-2`~~)* |
| §4g ⓹ thứ tự bậc `ma`: cùng tệ › khác tệ › bậc tiền | `[ma VND, ma USD, tien VND]` | `test_wo037_ro_may_…::test_AC3_*` · Chrome 8099 ca `Y` | ✅ | ✅ xanh · sổ thật tập **rỗng** *(`Đ3`)* |
| §4h ⓵ dòng `bac` — `gd`/`gd_ds` khác tệ ⇒ `khac_tien_te`; một phép so tiền tệ; bậc lạ in nguyên tên | `_bac` · `ve_dang_gan` | `test_wo037_…::test_AC4_*` · `::test_AC5_*` · `tests/web/test_wo037_man_cua_that.py::test_AC6_*` · `test_kq036_…::test_F1_*` · `::test_F2_*` · `::test_F3_*` *(gỡ dấu)* | ✅ | ✅ xanh |
| §4h ⓵' `the.vi_sao` **chỉ** khi `gd null ∧` khớp mã chỉ khác tệ | 84 thẻ, ⛔ 616 | `test_wo032_quet_khoa_cua_that.py::test_WO037_*` · `kq041::test_CANH_ORACLE_*` | ✅ | ✅ sổ thật `the.vi_sao` ở `may` **0** · `nguoi` **84** |
| `BA-06` §4.5 câu thứ sáu — ô *Giao dịch* = câu cửa | so chuỗi, ⛔ `đề xuất:` | `test_wo037_man_cua_that.py::test_AC8_*` ×2 · Chrome 8088 + 8099 | ✅ | ✅ 8088 **736** ô = **84** câu ＋ **120** `đề xuất:` ＋ **532** `— chưa chọn` |
| `BA-06` §4.5 `ⓤ` — băng `F01L` hai câu + ghi chú + hàng `nguoi` | chữ nguyên văn, `a`/`b`/`c` từ cửa | `tests/web/test_wo037_v2_bang_f01l_cua_that.py` ×4 · Chrome 8088 *(532 · 84 · 120)* · 8099 *(`a = 0 ∧ b > 0` trên cửa thật)* | ✅ | ✅ xanh · ⚠ `note ok` + nhãn lọc + `RO.may` còn *"lệch tiền"* — `KQ-041 F-1` *(spec ⛔ phủ)* |
| `NFR-I29` — chú giải ≥ 4,5 · `.tg` ⛔ tông ≥ 3 | `getComputedStyle` | `test_wo037_man_cua_that.py::test_AC7_*` ×3 · Chrome 8088 + 8099 | ✅ | ✅ **4,92** · **5,59** *(8088 `≠` 50/50)* |
| `BA-06` §5b — danh sách `②b` theo **chip** *(⛔ phạm vi `WO-037`)* | đổi chip khi đang tải ⛔ trộn rổ | `kq041::test_CANH_doi_chip_SAU_*` · `::test_F3_*` ×3 | ✅ | ✅ *(`WO-042` — viết lại `KQ-046` §1.13; ~~⛔ `xfail(strict)` — `KQ-041 F-3` `NANG`~~)* |

⇒ **13 mục — 11 xanh** trên cửa thật + sổ thật chỉ đọc; **1** mục biên ghim `xfail(strict)` *(`F-2`, mẫu số sổ thật **0**)*; **1** mục **ngoài phạm vi** ghim `xfail(strict)` *(`F-3`)*. Ba dòng `xfail` của **§1.11** *(`KQ-036 F-1`…`F-3`)* nay ✅.

### 1.11 ⭐ `WO-032` *(vòng 1 + 2)* — `BA-07` **v3.8** §4h ⓵ · ⓵' · ⓹ *(+ `GAP-API-11` NGOÀI)* · `BA-06` **v4.15** §5b ⓕ ⓘ ⓙ + §4.5 ⓒ ① · `QĐ-ITL-149 ⓑ` → bài *(`KQ-036`, 2026-10-02)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| ⓵ `lech` = `\|Δ\|` mọi bậc, `null` ⇔ khác tiền tệ / thiếu số — **bốn** cửa | oracle `Decimal` độc lập trên HTTP | `tests/api/test_wo032_khuon_cua_pg.py::test_AC2_*` · `tests/nghiem_thu/test_kq031_…::test_F2_*` *(gỡ dấu)* · `test_kq036_…::test_CANH_lech_ung_vien_*` | ✅ | ✅ xanh · sổ thật 8088 **0** sai / **10.909** phần tử *(`KQ-036` Dữ liệu)* |
| ⓵ `khoa_to` luôn có — kể cả `gd`/`gd_ds` *(⓵')* | `<mark>` khối *"Đang gán"* trên thân cửa thật | `test_wo032_khuon_cua_pg.py::test_AC4_*` · `test_wo032_man_cua_that.py::test_AC3_AC4_*` · `kq031::test_F3_*` *(gỡ dấu)* · ⭐ `test_kq036_…::test_CANH_bai_b3_KHONG_tu_nhet_khoa_to` | ✅ | ✅ xanh · sổ thật vắng **0** · chiều ĐỎ *"b3 nhét lại"* nay có cổng *(`KQ-036 F-5` ⓑ)* |
| ⓵ `bac` — bậc **lạ** ⇒ in nguyên tên | `ve_ung_vien` in `xyz` · khối *"Đang gán"* in `xyz` | `test_wo032_man_cua_that.py::test_AC5_*` · `test_kq036_…::test_F3_khoi_DANG_GAN_bac_LA_*` | ✅ | ✅ `ve_ung_vien` · ✅ khối *"Đang gán"* *(gỡ dấu `KQ-041`; ~~⛔ `xfail(strict)` — `KQ-036 F-3`~~)* |
| ⓵' bậc `gd`/`gd_ds` theo mã **chính** dòng lệnh, **cả hai** cửa; **một** chỗ gắn `ma_canon` | `lenh-da-gan` khớp số CT ⇒ `ma` | `tests/api/test_wo032_v2_bac_da_gan_pg.py` ×4 *(kho TEST + sổ thật chỉ đọc + quét AST một chỗ)* · `test_kq036_…::test_CANH_khoi_DANG_GAN_bac_MA_*` | ✅ | ✅ xanh · sổ thật `gd_ds` **2.262/2.262** · `gd` **2.219/2.219** · `lenh-cho` 268 ⛔ hồi quy |
| ⓵' bậc `gd`/`gd_ds` — phép so tiền tệ **giống hệt** khuôn ⓵ | `_bac` cùng luật `ma_tien_te` | `test_kq036_…::test_F1_bac_gd_so_tien_te_*` | ✅ | ✅ *(gỡ dấu `KQ-041`; ~~⛔ `xfail(strict)` — `KQ-036 F-1`~~)* |
| ⓵' `gd`/`gd_ds` **khác tiền tệ**, ⛔ khớp mã | ⛔ mang nhãn *"cùng đơn vị tiền"* | `test_kq036_…::test_F2_gd_ds_KHAC_tien_te_*` | ✅ | ✅ *(gỡ dấu `KQ-041` — `BA-07` v3.9 khai `khac_tien_te` ở `gd`/`gd_ds`; ~~⛔ `xfail(strict)` — `KQ-036 F-2`~~)* · sổ thật **0 / 2.262** |
| ⓹ `/so` khác tiền tệ ⇒ `khac_tien_te` | ⛔ dòng khác tiền tệ nào `cung_tien_te` | `test_wo032_khuon_cua_pg.py::test_AC5_*` ×2 | ✅ | ✅ xanh · sổ thật **0 / 552** dòng khác tiền tệ mang nhãn sai |
| `GAP-API-11` *(`/so` `500` khi dòng tiền `0`)* | — | ⛔ **chưa có** — NGOÀI `WO-032` | — | ⏳ sổ thật **0 / 8.387** dòng |
| `BA-06` §5b ⓕ — so mã **trước** xu, câu `crit` *"khác tiền tệ … TỪ CHỐI"* | hộp *Tìm tiền* | `test_wo032_man_cua_that.py::test_AC1_*` · `kq031::test_F1_*` *(gỡ dấu)* · Chrome 8099 + 8088 chuột thật `KQ-036` | ✅ | ✅ xanh |
| §5b ⓙ — ô tiền kèm mã ở bảng trộn tiền tệ | `100.000,00 USD` | `test_wo032_man_cua_that.py::test_AC1_*` · Chrome 8088 `PM00329-1` | ✅ | ✅ xanh |
| §5b ⓘ — `.cand-cols` `160px` ×3 + `title` | `title` = chữ in | `test_wo032_man_cua_that.py::test_AC7_*` ×2 | ✅ | ✅ xanh · 8088 **70/70** · ⚠ câu `.cand .amt .lech` của ⓘ tả phần tử ⛔ tồn tại *(`F-5` ⓒ)* |
| §5b *Năm trạng thái* — rỗng của màn vẽ được *(`F01L` · `F04` ×3)* | 0 `TypeError` | `test_wo032_man_cua_that.py::test_AC6_*` ×3 · `test_wo032_v2_chu_giai_bac_va_f04.py::test_AC14_*` · Chrome 8088 `?gia_lap=` ×4 | ✅ | ✅ xanh |
| §4.5 ⓒ ① — chú giải bậc **sinh từ `BAC`**, một dòng, cả hai chế độ, ⛔ khi rỗng/tải | `textContent` 5/5 | `test_wo032_v2_chu_giai_bac_va_f04.py::test_AC13_*` ×5 · Chrome 8088 + 8099 | ✅ | ✅ xanh · ⚠ tương phản chữ nghĩa **2,17 : 1** *(`KQ-036 F-4` — ⛔ ngưỡng, `GAP-NFR-01`)* |
| `QĐ-ITL-149 ⓑ` — ba hộp ô lý do tuỳ ý; `Hoãn`/`Mở lại` giữ | 1 `POST` · `(may dien)` · 0 `POST` | `test_wo032_man_cua_that.py::test_AC8_*` ×2 · Chrome 8099 **POST thật** `KQ-036` *(evt 31 · 37 · 43)* | ✅ | ✅ xanh |
| Cổng quét khoá màn ⊆ khoá cửa thật *(43 cặp)* | — | `tests/web/test_wo032_quet_khoa_cua_that.py` | ✅ | ✅ xanh · 12 đột biến Test: 11 bắt, `T12` lấp |

⇒ **15 mục — 11 xanh** trên cửa thật; **3** mục ghim `xfail(strict)` *(`KQ-036 F-1`…`F-3`, cả ba ca biên mẫu số **0** trên sổ thật)*; **1** `GAP` ngoài phạm vi. Dòng `xfail` của **§1.10** *(`KQ-031 F-1`…`F-3`)* nay ✅.

### 1.10 ⭐ `WO-022` **vòng 3** — `BA-07` **v3.6** §4h ⓵ *(khuôn ứng viên)* · `BA-06` **v4.13** §5b ⓕ *(hộp Tìm tiền)* → bài *(`KQ-031`, 2026-10-02)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| ⓵ hộp *Tìm tiền* đọc `amount` · `lech` · `dien_giai` *(`AC-16`)* | cột Tiền/Lệch/Diễn giải in đúng; khớp đúng xu ⇒ *"trong dung sai"* | `tests/nghiem_thu/test_kq029_tim_tien_khuon_cua_that.py::test_F1_*` ×2 *(gỡ `xfail` — tiền `<N>` ngẫu nhiên)* · `tests/web/test_wo022_v3_tim_tien_cua_that.py::test_AC16_tim_tien_*` · Chrome 8099 + 8088 chuột thật `KQ-031` | ✅ | ✅ xanh *(JS `a69ee92` ⇒ đỏ đúng lý do)* |
| ⓕ lệch `0,40` in `0,40` + `VƯỢT` — thân **cửa thật** *(`AC-17`)* | 4 đường màn từ cửa HTTP kho TEST | `tests/web/test_wo022_tien_theo_tien_te.py::test_AC6_man_f01_lenh_CHAN_MAN_va_hop_TIM_TIEN_lech_0_40` | ✅ | ✅ xanh *(6 đột biến Test: 5 bị bắt; ⛔ `lech null ⇒ 0` sống — `KQ-031 F-2`)* |
| Cổng **quét khoá** màn ⊆ khoá cửa thật | `F01L` 2 hàm · 26 khoá | `tests/web/test_wo022_v3_tim_tien_cua_that.py::test_AC16_MOI_khoa_*` · `::test_AC16_moi_ham_*` · `::test_AC16_KHUON_THU_*` | ✅ | ✅ xanh · ⭐ Test đo **28** cặp *(hàm, biến)* `F01L`+`F01G` trên **89** thân cửa 8088: `F01L` **0** thiếu, `F01G` thiếu `khoa_to` *(`F-3`)* |
| ⓵ `lech` — *"`null` khi khớp tuyệt đối"* | bậc `ma` tiền lệch ⇒ `lech` ≠ `null` | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F2_*` | ✅ | ⛔ **`xfail(strict)`** — `KQ-031 F-2` *(sổ thật **338/448** bậc `ma` lệch mà `null`)* |
| ⓵' `the.gd` mang khoá khối *"đang gán"* đọc | `ve_dang_gan`/`ve_o_gd` ⊆ `gd` | `…kq031…::test_khoi_DANG_GAN_*` *(canh)* · `::test_F3_*` *(`khoa_to`)* | ✅ | ✅ canh xanh · ⛔ `xfail(strict)` `KQ-031 F-3` *(`khoa_to` **0/768**; `BA-07` ⛔ khai)* |
| ⓕ phép lệch khi ứng viên **khác tiền tệ** | ⛔ nói *"trong dung sai"* cho cặp cửa ghi ⓔ từ chối | `…kq031…::test_F1_CANH_cua_ghi_*` *(mỏ neo `KhacTienTe`)* · `::test_F1_tim_tien_KHAC_TIEN_TE_*` | ✅ | ⛔ **`xfail(strict)`** — `KQ-031 F-1` *(sổ thật **4** lệnh; **165/5.360** ứng viên khác tiền tệ)* · ⏳ spec ⓕ ⛔ nói ca này |
| Năm trạng thái hộp *Tìm tiền* | rỗng ⇒ ⛔ nổ | Chrome 8088 `?gia_lap=` `KQ-031` | — | ⛔ rỗng nổ `TypeError` *(`KQ-031 F-4`, có từ trước)* · tải/lỗi/mất kết nối ✅ |

⇒ **7 mục — 4 xanh** *(hành vi trên cửa thật)*; **3** mục ghim `xfail(strict)` *(`F-1`…`F-3`, cả ba có từ **trước** vòng 3)*; **1** trạng thái nổ *(`F-4`)*. Dòng `xfail` hộp *Tìm tiền* của **§1.9** nay ✅.

### 1.9 ⭐ `WO-022` *(vòng 1 + 2)* — `BA-06` **v4.13** `UI-F10` §5b ⓐ…ⓘ *(in tiền theo tiền tệ)* → bài *(`KQ-029`, 2026-10-02)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| ⓐ số lẻ ISO 4217 cố định, bảng **một chỗ** | `1234` USD ⇒ `1.234,00`; VND ⇒ `0` lẻ | `tests/web/test_wo022_tien_theo_tien_te.py::test_AC1_*` *(12 ca từng byte + `SO_LE` đóng băng)* | ✅ | ✅ xanh *(Test đo lại `node` 16/16)* |
| ⓑ ⛔ làm tròn giá trị sổ — in đủ tới thang kho 2 *(`Q-TIEN-1` mặc định)* | `1306103.80` VND ⇒ `1.306.103,80` | `test_wo022_tien…::test_AC1_*` · `tests/web/test_wo022_tien_theo_tien_te_pg.py::test_AC5_*` *(khứ hồi sổ thật **8.387**)* | ✅ | ✅ xanh *(Test đo **8.387** sổ + **272.208** lệnh: **0** lệch)* |
| ⓒ *(v4.13)* mã lạ / thiếu = bảng 0, có lẻ in đủ 2 | `100.50` `'20'` ⇒ `100,50` | `tests/web/test_wo022_v2_o_tien_va_mot_luat_so_le.py::test_AC13_*` ×2 *(6 ca + quan hệ 16 giá trị)* | ✅ | ✅ xanh |
| ⓓ `.` nghìn `,` thập phân; số 0 ⛔ dấu | `-0.00` ⇒ `0,00` | `test_wo022_tien…::test_AC1_*` · `::test_AC13_*` | ✅ | ✅ xanh *(Test phá 39 ca — `KQ-029` Logic)* |
| ⓔ mọi chỗ gọi truyền mã tiền tệ | **42** lời gọi, 2 đối số | `test_wo022_tien…::test_AC2_*` *(đếm theo ngoặc + bài chứng minh máy đếm cắn)* | ✅ | ✅ xanh *(Test đếm độc lập 43 − 1 chú thích = 42)* |
| ⓕ Σ / lệch trên **xu**, khớp ⇔ lệch = 0 — hộp `Ghép lệnh` `F01` | `0.10+0.20` vs `0.30` ⇒ khớp, nút mở | `test_wo022_tien…::test_AC4_*` *(DOM)* · Chrome 8099 **tích chuột thật** `KQ-029` | ✅ | ✅ xanh |
| ⓕ — `ve_tong_chum` · `khop_dung_tien` | `4.35+0.65` vs `5.00` khớp; hai số thiếu ⛔ khớp | `test_wo022_tien…::test_AC4_*` *(DOM — cửa ghép tay ⛔ dựng được ca này)* | ✅ | ✅ xanh |
| ⓕ — hộp **Tìm tiền** `F01L` *(tiền lệnh ↔ tiền bank · lệch — `WO-022` (c))* | chọn ứng viên ⇒ in tiền bank + lệch trên xu | ⛔ bài Dev `test_wo022_tien…::test_AC6_man_f01_lenh_*` nuôi **khuôn tự nhét** `{tien, lech_tuyet_doi}` · ⭐ `tests/nghiem_thu/test_kq029_tim_tien_khuon_cua_that.py::test_F1_*` ×2 *(thân **cửa thật**)* + `::test_khuon_CUA_THAT_*` *(canh khuôn `⓵`)* | ✅ | ✅ xanh *(`KQ-031` — `BG-030` vá; gỡ dấu 2 bài; bài Dev viết lại lấy thân cửa thật)* · ~~⛔ `xfail(strict)` — `KQ-029 F-1` `NANG`~~ |
| ⓕ *(v4.13)* dung sai in = dung sai đem so *(sàn)* | `617.285` ⇒ `617,28`; lệch `617,29` ⛔ khớp | `test_wo022_v2…::test_AC14_*` ×4 · Chrome 8099 chuột thật `F01` + cửa thật `F01L` `KQ-029` | ✅ | ✅ xanh |
| ⓖ hàm in ⛔ dùng để tính; gửi cửa chuỗi cửa trả | `data-a` mang chuỗi cửa | đọc mã `man_f01.js:304` *(⛔ bài riêng)* | — | ✅ đọc mã |
| ⓘ *(v4.13)* ô tiền theo ngân sách 18 ký tự × phông rộng nhất — `.mcols` | `136px`; > 18 ⇒ `…` + `title` | `test_wo022_v2…::test_AC10_*` ×3 · `::test_AC12_*` ×2 · `tests/web/test_wo022_v2_o_tien_pg.py::test_AC11_*` *(sổ thật)* · Chrome 8088 + 8099 `KQ-029` *(18 ký tự 136/136; phông 0,6em 135 ≤ 136; 19/24 ký tự `…` + `title`)* | ✅ | ✅ xanh |
| ⓘ — ô tiền cố định **khác** `.mcols`: ứng viên `.cand-cols` `160px` | vừa 18 ký tự *(137px ô chữ)*; ⛔ `title` | ⛔ **chưa có** — spec ⛔ khai ô này | — | ⏳ `KQ-029 F-3` → `BA` |
| Năm trạng thái *(tải · rỗng · lỗi · mất kết nối · có dữ liệu)* | ⛔ thêm trạng thái; rỗng ⇒ `—` | Chrome 8088 `?gia_lap=` × 5 màn `KQ-029` | — | ✅ ⛔ hồi quy *(`F04` rỗng nổ `TypeError` có từ 08/09 ⇒ `KQ-029 F-2`)* |

⇒ **13 mục — 10 có bài chạy hành vi xanh**, 1 đọc mã *(ⓖ)*; **1** mục ghim `xfail(strict)` *(`F-1` — hộp *Tìm tiền* trên cửa thật; bản vá mô phỏng lật cả 2 bài)*; **1** mục chờ spec *(`F-3`)*. Dòng ⏳ `KQ-021 F-3` của **§1.7** nay ✅ *(`WO-022`)* — giữ §1.7 làm biên bản.

### 1.8 ⭐ `WO-018` — `BA-05` **v0.34** `DD-I15 ⓓe` *(`value_source` = lớp của chính dòng)* · `BA-06` v4.9 dòng *"F02 · nhật ký"* → bài *(`KQ-025`, 2026-10-02 khuya)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `ⓓe` bất biến `fls_journal.value_source = fls_adjustment.nguon` cùng giao dịch — **mọi** cặp | đa tập hai bảng bằng nhau trên đủ đường ghi | `tests/repo/test_wo018_bat_bien_cap_nhat_ky_pg.py::test_AC3_da_tap_*` *(hàm repo, mẫu số **14**)* · ⭐ `tests/nghiem_thu/test_kq025_nhat_ky_lop_cua_dong.py::test_e_*` *(toàn bộ qua **HTTP**, mẫu số **10**)* | ✅ | ✅ xanh *(sổ thật **4.428 / 4.428**)* |
| `ⓓe` cửa ghi duy nhất cưỡng chế | `_them` NO khi `value_source ≠ nguon`, **0** dòng | `test_wo018_bat_bien…::test_them_NO_*` · bài quét `tests/repo/test_chi_mot_cho_ghi_tay.py` | ✅ | ✅ xanh |
| `ⓓe` người gõ ⇒ `sua_tay` *(ô rỗng · nguồn sổ · `*_thyt` · đã có người · xoá `null`)* | nhật ký `sua_tay`; thân trả `/adjust` giữ nguồn **trước** khi gõ | `tests/web/test_wo018_nhat_ky_nguoi_sua_pg.py::test_AC1_*` ×2 · `test_wo008_than_that_bo_ghep_pg.py::test_AC2_*` · `test_vong_f02_pg.py::test_force_KEM_*` · `tests/repo/test_ghi_tay_pg.py::test_nhat_ky_du_BAY_truong` · `tests/api/test_cua_ghi_pg.py` `:241` *(thân trả)* · `kq025::test_e_*` | ✅ | ✅ xanh *(8099 **B** chuột thật)* |
| `ⓓe` *"Bản đảo ⇒ lớp của **dòng bị đảo**"* — đảo **máy** qua cửa `/reverse` | bản đảo + nhật ký `may_goi_y`; Final ⛔ đổi | `test_wo018_bat_bien…::test_AC3_ban_dao_*` *(hàm repo)* · ⭐ `kq025::test_a_*` *(HTTP)* · ⭐ `kq025::test_c_*` *(dòng máy **dưới** giá trị người — duy nhất bắt đột biến "lớp theo ô")* | ✅ | ✅ xanh *(8099 **A** chuột thật)* |
| `ⓓe` đảo **người** qua `/reverse` | bản đảo `sua_tay`; Final lùi về lớp dưới / sổ gốc | `test_wo018_bat_bien…::test_AC3_ban_dao_*` · ⭐ `kq025::test_d_*` | ✅ | ✅ xanh |
| `ⓓe` bản đảo của **bỏ ghép** | lớp dòng bị đảo *(mọi lớp)* | `test_wo018_bat_bien…::test_AC3_ban_dao_*` · `test_wo008_than_that…::test_AC2_*` · `kq025::test_e_*` | ✅ | ✅ xanh |
| `BA-06` v4.9 ⓑ — bản đảo máy ⇒ *"rút gợi ý"*, ⛔ ô trống | qua **cửa đảo** *(⛔ chỉ bỏ ghép)* | ⭐ `kq025::test_b_*` *(thân `GET /journal` thật ⇒ màn, node)* | ✅ | ✅ xanh |
| `BA-06` v4.9 ⓒ — bản đảo **người** *(`sua_tay`, `value_after NULL`)* | ⛔ spec khai chữ — in ô trống + *"người sửa"*, giống hệt người **xoá ô** | ⛔ **chưa có** — chờ spec | — | ⏳ `KQ-025 F-3` → `BA` |

⇒ **8 mục — 7 có bài chạy hành vi xanh**; **6** đột biến của `fls-test` *(`T0`…`T5`)* đều bị bắt, `T3` chỉ `kq025::test_c_*` bắt; **1** mục chờ spec *(`F-3`)*. Dòng ⏳ `ⓓe` của **§1.6** nay ✅ — giữ §1.6 làm biên bản.

### 1.7 ⭐ `WO-008` **vòng 2** — `BA-06` **v4.10** mục ⓔ *(năm ca nút `Bỏ gán` + 5 trạng thái)* → bài *(`KQ-021`, 2026-10-02 tối)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| ⓔ ① lệnh ≥ 2 dòng tiền | hộp **báo** `HT.mo`, `Lệnh này đang gắn N giao dịch`, `["Đã hiểu"]`, 0 `/chum`, 0 `/unmatch` | `tests/web/test_wo008_v2_nam_ca_bo_gan.py::test_AC8_*` ×2 · `tests/nghiem_thu/test_kq019…::test_F1_…[da_giao_dich]` · ⭐ `tests/nghiem_thu/test_kq021_bo_gan_vong2.py::test_SO_THAT_*` *(sổ thật, hàm thật — ca ① **23**)* | ✅ | ✅ xanh *(Chrome 8088 **23/23**)* |
| ⓔ ② chùm *(`can_hoi`)* | hộp **hỏi** `Thôi` · `Gỡ cả N`, ghi trong nút, lỗi trong hộp | `test_wo008_v2…::test_AC7_*` ×6 · `test_kq019…::test_F1_…[chum]` · ⭐ `test_kq021…::test_SO_THAT_*` *(ca ② **65**)* · `::test_T1_*` *(sau `Thôi` nút mở lại)* · `::test_T6_*` *(lệnh còn dòng tiền khác giữ `Đã gán`)* | ✅ | ✅ xanh *(Chrome 8088 **65/65**; 8099 **D2** chùm + `bo_qua`)* |
| ⓔ ② `Thôi` / `Esc` / bấm ngoài ⇒ 0 ghi + `§4.5` *"`Esc` bóc từng lớp một"* (`06:745`) | `Esc` chỉ đóng hộp; `j`/`k` ⛔ đổi lệnh sau hộp | ⭐ `test_kq021…::test_F1_ESC_*` · `::test_F1_phim_J_*` | ✅ | ⛔ **`xfail(strict)`** — `KQ-021 F-1` *(vế 0 ghi ✅)* |
| ⓔ ② cửa lỗi ⇒ *"hộp ở nguyên, lỗi trong hộp"* — khi người `Esc` **giữa lúc chờ** | lỗi vẫn hiện | ⭐ `test_kq021…::test_F2_ESC_khi_GO_CA_N_*` | ✅ | ⛔ **`xfail(strict)`** — `KQ-021 F-2` *(⏳ `BA` chọn hướng)* |
| ⓔ ③ bỏ gán xong — thẻ tại chỗ, bộ ba = `khuon_the_lenh`, dòng tín hiệu, ở yên | khối *"Đang gán"* mất, `Gán` trở lại | `test_wo008_v2…::test_AC9_*` ×4 · `test_kq019…::test_F2_*` · ⭐ `test_kq021…::test_T4_*` *(view ① ⛔ in giao dịch vừa gỡ)* · `::test_T6_*` | ✅ | ✅ xanh |
| ⓔ ④ đọc lại ứng viên lỗi | ③ trước, dòng *"Chưa tải lại được…"*, hộp `bo_qua` vẫn mở | `test_wo008_v2…::test_AC12_*` · `test_kq019…::test_F4_*` | ✅ | ✅ xanh *(đột biến `T13` bị bắt)* |
| ⓔ ⑤ cửa lỗi ngoài hộp | *"Bỏ gán chưa xảy ra — Cửa lỗi: …"* + `lam_gi` + `chi_tiet`, 0 `Uncaught`, thử lại được | `test_wo008_v2…::test_AC11_*` ×4 · `test_kq019…::test_F3_*` · ⭐ `test_kq021…::test_T2_*` · `::test_T18_*` | ✅ | ✅ xanh |
| 5 trạng thái vùng `Bỏ gán` — **tải** | nút khoá trong lúc chờ, mở lại sau | `test_wo008_v2…::test_AC10_*` · ⭐ `test_kq021…::test_T1_*` · `::test_T2_*` | ✅ | ✅ xanh *(8099 **C2** chuột thật: 1 `POST`)* |
| *(⛔ spec khai)* số chữ số thập phân khi in tiền **ngoại tệ** *(hộp ② liệt kê số tiền + tiền tệ)* | `1234.56 USD` ⛔ in `1.235 USD` | ⛔ **chưa có** — chờ spec | — | ⏳ `KQ-021 F-3` → `BA` |

⇒ **9 mục — 7 có bài chạy hành vi xanh** *(đột biến `fls-test` `T1` `T2` `T4` `T6` `T18` + tiêu đề ca ① + mã `124a067` đều bị bắt bởi `kq021`)*; **2** mục ghim `xfail(strict)` *(`F-1` · `F-2`; bản sửa mô phỏng `X1` / `X1`+`X2` lật cả 3 bài)*; **1** mục chờ spec *(`F-3`)*. ⭐ Bốn dòng `xfail(strict)` của **§1.6** *(`KQ-019 F-1`…`F-4`)* nay **xanh không dấu** — gỡ ở `KQ-021`; giữ §1.6 làm biên bản.

### 1.6 ⭐ `WO-008` — `BA-06` v4.9 *(ba chỗ chữ sau bỏ ghép)* · `BA-05` v0.34 `DD-I15 ⓓe` → bài *(`KQ-019`, 2026-10-02 chiều)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `BA-06` v4.9 *"F02 · nhật ký"* ⓐⓑⓒ *(`gợi ý: X` · `rút gợi ý` · giá trị người)* + nhãn nguồn chữ trơn | ô thành/nguồn đọc theo `value_source` | `tests/web/test_wo008_chu_man_sau_bo_ghep.py::test_AC1_*` ×3 · `tests/web/test_wo008_than_that_bo_ghep_pg.py::test_AC2_*` *(cửa thật, kho TEST)* · ⭐ `tests/nghiem_thu/test_kq019…::test_nhat_ky_SO_THAT_qua_man_THAT__…` *(toàn nhật ký sổ thật, `doc_nhat_ky` thật, quan hệ — mẫu số **4.424**)* | ✅ | ✅ xanh *(`M1`, `M2` ⇒ đỏ)* |
| `BA-06` v4.9/v4.8 hộp *"Đã bỏ ghép"* nói theo **ô** + `bo_qua` in `ô = giá trị` | `2 ô` · `M bút toán` khi `M > N`; mỗi tên ô 1 lần | `test_wo008_chu…::test_AC3_*` ×2 · `test_wo008_than_that…::test_AC3_*` · ⭐ `test_kq019…::test_bo_gan_bo_qua_CO__HOP_THAT_…` *(`hop_thoai.js` **thật** — bài Dev thay `HT.mo` bằng bẫy)* | ✅ | ✅ xanh *(`M4`, `M6` ⇒ đỏ)* |
| `BA-06` mục ⓔ v4.8 màn ghép **báo sau** khi `bo_qua` ⛔ rỗng, ⛔ hộp khi rỗng | 1 hộp `Đã hiểu` / 0 hộp | `test_wo008_chu…::test_AC4_*` ×3 · `test_wo008_than_that…::test_AC4_*` · ⭐ `test_kq019…::test_bo_gan_bo_qua_CO__…` · `::test_bo_gan_bo_qua_RONG__HOP_THAT_khong_mo` | ✅ | ✅ xanh *(`M3`, `M5` ⇒ đỏ)* — ⚠ chỉ ca **1 lệnh – 1 dòng tiền** |
| `BA-06` mục ⓔ — chùm: **hỏi trước** rồi báo; lệnh ≥ 2 giao dịch ⇒ chỉ sang `Sổ ITL` | hộp hỏi mở | ⭐ `test_kq019…::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[×2]` | ✅ | ⛔ **`xfail(strict)`** — `KQ-019 F-1` *(`HT.hoi` ⛔ tồn tại)* |
| *(⛔ spec khai)* màn ghép sau bỏ gán **⛔ còn nói "Đang gán"** | thẻ/khối lệnh làm mới | ⭐ `test_kq019…::test_F2_sau_bo_gan_THANH_CONG__…` | ✅ | ⛔ **`xfail(strict)`** — `KQ-019 F-2` *(⏳ `BA` khai)* |
| `WO-008` Màn hình *lỗi* / *mất kết nối* của `Bỏ gán` | người thấy lỗi, ⛔ hộp "Đã bỏ ghép" | `test_wo008_chu…::test_AC4_cua_unmatch_LOI__…` *(chỉ vế ⛔ hộp)* · ⭐ `test_kq019…::test_F3_bo_gan_cua_LOI__nguoi_THAY_loi` | ✅ | ◐ vế ⛔ hộp ✅; vế *thấy lỗi* ⛔ **`xfail(strict)`** — `KQ-019 F-3` |
| `BA-06` *"`bo_qua` phải hiện"* khi vẽ lại lệnh lỗi | hộp vẫn mở | ⭐ `test_kq019…::test_F4_ve_lai_lenh_LOI_sau_bo_gan__…` | ✅ | ⛔ **`xfail(strict)`** — `KQ-019 F-4` |
| `BA-05` v0.34 `DD-I15 ⓓe` *(`value_source` = lớp của chính dòng; bất biến `= fls_adjustment.nguon`)* | cửa ghi `/adjust` ghi `sua_tay` | ⛔ **chưa có** — mã ⇒ `WO-018`; bài `test_wo008_than_that…::test_AC2_*` **ghim** nghĩa cũ `("HD-K7B", "UNMAPPED")` *(`WO-018` lật đúng một `assert`)*; sổ thật: bất biến **4.428 / 4.428** *(đo `TL-016`)*, dòng `/adjust` **0**, `*_thyt` ≠ NULL **0 / 8.387** *(`KQ-019`)* | — | ⏳ chờ `WO-018` |

⇒ **8 mục — 3 có bài chạy hành vi xanh, 6 đột biến `M1`…`M6` đều bị bắt; 4 mục là phát hiện mới của `KQ-019` ghim bằng `xfail(strict)` *(bản sửa mô phỏng `X1`…`X4` lật cả 4)*; `ⓓe` chờ `WO-018`.** Ba dòng ⏳ của §1.4 *(v0.7)* nay ✅ — giữ làm biên bản.

### 1.5 ⭐ `WO-011` — `09` v1.14 luật *"người thật"* ⓐ…ⓔ · `QĐ-ITL-150 ⓐ` · `TL-012` → bài *(`KQ-014`, 2026-10-02 trưa)*

| Mục spec | Hành vi | Bài *(tệp::bài)* | Gọi tên? | Trạng thái |
|---|---|---|:-:|---|
| `WO-011 T1` / `AC-1` *(sổ actor **9** máy, một chỗ)* | hằng cũ lấy từ sổ; hằng `@fls`/`@apero.vn` mới ⇒ ĐỎ | `tests/repo/test_danh_muc_actor.py::test_QUET_MA__…` · `::test_KHONG_GO_LAI__…` · `::test_SO_MAY_du_va_ghim` · `::test_hang_cu_LA_hang_cua_so` | ✅ | ✅ xanh *(đột biến `K10` ⇒ đỏ)* |
| `WO-011 T2` *(người = ⛔ `ACTOR_MAY` ∧ ⛔ UAT — `B2/3/5`)* | 9/9 máy ⇒ 0 | `tests/test_kiem_so_song.py::test_T2_MOI_actor_may_trong_SO_dem_0_nguoi` · `::test_T2_cau_SQL_mang_DUNG_ban_sinh_tu_SO` *(bản chép ép trùng byte — `TL-012`)* · `tests/repo/test_wo011_…::test_AC4_*` | ✅ | ✅ xanh *(`K3`, `K4` ⇒ cổng nổ `⛔ khong do duoc`)* |
| `WO-011 T3` / `AC-3` *(actor mới ⇒ đếm + gọi tên + NO)* | một dòng `⚠ ACTOR MỚI: <tên> · <n>`; `main()` = 1 | `test_kiem_so_song.py::test_T3_*` ×2 · `test_wo011_…::test_AC3_*` ×3 · ⭐ `tests/nghiem_thu/test_kq014…::test_MAY_MOI_chua_khai__…` *(máy mới quên khai, 3 thao tác qua cửa ghi thật)* | ✅ | ✅ xanh *(`K5` ⇒ đỏ)* |
| `WO-011 T4` / `AC-5` *(UAT một luật, hai mặt)* | 10 biến thể UAT ⇒ 0; 6 lý do người ⇒ đếm | `tests/repo/test_danh_muc_actor.py::test_la_uat_*` *(25 mẫu)* · `test_kiem_so_song.py::test_T4_*` · ⭐ `test_kq014…::test_UAT_ghep_roi_bo_ghep_qua_cua_that__…[×10]` · `::test_NGUOI_ghep_roi_bo_ghep_qua_cua_that__…[×6]` · ⭐ `::test_luat_UAT_moi_diem_ma__…[×5]` *(BMP — ghim chiều; lệch toàn Unicode `KQ-014 F-1`)* | ✅ | ✅ xanh *(`K1`, `K6` ⇒ đỏ)* |
| `WO-011 T5` / `AC-4` *(`B4` loại máy)* | bỏ ghép máy ⇒ 0 | `test_kiem_so_song.py::test_T5_*` ×2 · ⭐ `test_kq014…::test_MAY_bo_ghep_qua_cua_that__B4_DUNG[×9]` | ✅ | ✅ xanh *(`K2` ⇒ 9 đỏ)* |
| `WO-011 T6 ⓐ` / `AC-6` *(`C8` loại máy + UAT — "bất kỳ cổng người đã làm")* | UAT/máy ⛔ lật; người lật | `test_wo011_…::test_AC6_*` · ⭐ `test_kq014…::test_C8_*` | ✅ | ✅ xanh *(`K7`, `K8` ⇒ đỏ)*; ⚠ phép nối nhật ký ⛔ khoá — `KQ-014 F-2` |
| `WO-011 T6 ⓑⓒ` / `AC-7` *(`B3`/`B4` trên ảnh hiệu lực; khối chỉ quan hệ)* | ảnh mới cùng nội dung ⇒ khối trùng byte; ảnh cũ bẩn ⇒ ⛔ ảnh hưởng | `test_wo011_…::test_AC7_*` · `::test_T6c_C5b_*` · ⭐ `test_kq014…::test_B3_B4_anh_CU_ban_anh_HIEU_LUC_sach__…` | ✅ | ✅ xanh *(`K11`, `K12` ⇒ đỏ)* |
| `WO-011 T7` / `AC-8` *(phép so `09` §7 dòng `B`)* | `58,1%` · `1.601` · `826` | `test_kiem_so_song.py::test_T7_*` | ✅ | ✅ xanh *(`K9` ⇒ cổng đỏ)* |
| `BA-14` v0.8 `G-d` *(loại máy + UAT)* | — | ⛔ **chưa có** — `WO-011` NGOÀI phạm vi *("phiếu sau")* | — | ⏳ |
| `fls_chup` · `fls_khai_cot` actor ngoài sổ | — | ⛔ **ngoài phạm vi** `T3` — `KQ-014 F-4` gửi `BA` | — | ⏳ |

⇒ **10 mục — 8 có bài chạy hành vi, mỗi mục có đột biến bị bắt; `G-d` và hai bảng ảnh/khai chưa khai.** Vế `C8` của §1.3 *(⏳ v0.7)* nay ✅.

### 1.4 Rà spec mới của `fls-ba` *(`ee390cb`: `BA-06` v4.8 · `BA-09` v0.7 · `BA-10` v0.8)*

| Mục spec | Bài | Trạng thái |
|---|---|---|
| `BA-09` v0.7 `F-10`/`F-11` *"✅ đã chặn"* | như §1.2 *(`test_kq005_*` gỡ `xfail`, `test_kq007_*`)* | ✅ khớp — chữ *"mã đang vi phạm"* giữ làm biên bản *(`Đ2`)* |
| `BA-10` v0.8 nhánh `5a` ⇒ `AC-16` | `test_wo003_vong2…::test_ca_TRON_…` | ✅ khớp — `KQ-007 F-4` đóng |
| `BA-10` v0.8 *Nhật ký của bản đảo — đọc thế nào* | — *(luật **ghi** ⛔ đổi — bài §1.2 nhánh 6/8 vẫn phủ)* | ✅ ⛔ cần bài mới |
| `BA-06` v4.8 `F02` nhật ký đọc theo `value_source` *("rút gợi ý")* | ⛔ **chưa có** — mã ⇒ `WO-008` | ⏳ chờ `WO-008` |
| `BA-06` v4.8 hộp *"Đã bỏ ghép"* nói theo **ô** | ⛔ **chưa có** — `WO-008` | ⏳ |
| `BA-06` v4.8 màn ghép **báo sau** khi `bo_qua` ⛔ rỗng | ⛔ **chưa có** — `WO-008` *(sổ thật hôm nay bật **0** lần — `fls_sua_tay` 0)* | ⏳ |

⚠ Ba số `BA-06` v4.8 ghi *(`fls_journal` `may_goi_y` 4.424 · `sua_tay` 2 + 2 rỗng; `sua_tay` gắn `match` chưa đảo 0)* — đo lại sổ thật 01/10 tối: **khớp**.

## 2. GAP_REPORT (spec thiếu/mâu thuẫn — AI không tự đóng, R5)

| ID | Mô tả | Phát hiện bởi | Quyết định con người |
|---|---|---|---|
| ⭐ `GAP-ERD-P0-02` | `fls_pm_link.pm_line_id` ⛔ **không có khoá ngoại** và ⛔ không thể có: `fls_pm_line` khoá chính **ghép đôi** `(run_id, pm_line_id)`, còn `run_id` trên mối nối mang **hai nghĩa** *(`chay_nap` ghi run **nạp**, `ghi_tay` ghi run **ảnh PM**)*. Đo: nối bằng khoá đơn phồng **×22** *(2.262 → 49.764)* | `CR#12` · `DD-I13` | ⏳ **mở** — hướng: thêm cột `run_pm` |
| ⭐ `GAP-PEPI-01` | FLS ⛔ **không có bảng `PE`/`PI` nào**. `fls_pm_line.pe_line` *(13%)* và `pi_line` *(87%)* chỉ giữ **mã**, trỏ vào ⛔ không có gì — **lần thứ ba** của lớp lỗi `pm_line_id` | `CR#13` · `DD-I15` | ⏸ **HOÃN** *(owner `18/09`: "defer FPS related work")* |
| `GAP-DITRU-01` | ⛔ **Không có cầu khoá** AS-IS ↔ FLS *(`ITL#n` vs `itl_id` bigint)* ⇒ đối soát di trú phải đi **theo nội dung**, ⛔ không theo khoá | `QĐ-ITL-139` | ⏳ mở |
| `GAP-ALLOC-01` | *"Bao nhiêu dòng ra `0`"* khi `VLOOKUP` trúng ô rỗng — phép đo **⛔ chưa chạy** *(`fls/ledger/allocate.py`)* | `allocate.py` `28/08` | ⏳ mở |
| ⚠ `GAP-CONG-01` | Cổng số sống so **giá trị ghim** với những con số **tự lớn lên mỗi cú chụp** *(tới 12 lần/ngày)* ⇒ **tự chuyển ĐỎ**; riêng `18/09` phải vá **3 lượt**. Một cổng đỏ ⛔ không vì lỗi thì người ta học cách bỏ qua | `18/09` khi chạy cổng | ⏳ mở — hướng: so **quan hệ** thay vì giá trị |
| ✅ ~~`GAP-ERD-P0-03`~~ | ~~sổ ⛔ không giữ kết quả ghép~~ | — | ✅ **ĐÓNG `18/09`** *(`QĐ-ITL-141`)* — ⛔ **không phải khuyết tật**: `NGUON_MAY` chỉ được gợi ý `*_thyt` *(`QĐ-ITL-35`)*, sổ hiện chủ dự toán **chỉ khi người duyệt** — cố ý |

## 3. ERROR_REPORT (bug tìm thấy khi test)

| ID | Mô tả | TC tái hiện | Trạng thái |
|---|---|---|---|
| `KQ-005 F-1` | Bỏ ghép chỉ đảo **lớp trên cùng** của gợi ý ⇒ gợi ý chồng lớp *(`goi_y_lai` sau khi ảnh PM đổi `hd`)* nổi lên lại thành **mồ côi** | `tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py` | ✅ **vá** `5fbc29c` *(`WO-003` vòng 2)* — `KQ-007` gỡ `xfail` *(⛔ đóng mục ở đây: ⏳ v0.5 là biên bản)* |
| `KQ-005 F-2` | `bo_qua` chứa bút toán **đã đảo** lượt trước ⇒ màn `F01` nói *"người đã gõ tay"* khi ⛔ ai gõ *(ghép → bỏ → ghép lại → bỏ)* | `tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py` | ✅ **vá** `5fbc29c` — `KQ-007` gỡ `xfail` |
| `KQ-007 F-1` `NHE` | Nhật ký ô: bản đảo một lớp **⛔ hiệu lực** *(dưới giá trị người)* in *"X → trống"* — người đọc tưởng ô bị xoá *(`F02` ⑦)* | đo tay `KQ-007` `P1`, `P5` · `test_wo008_*::test_AC1_*`/`AC2_*` · `test_kq019…::test_nhat_ky_SO_THAT_…` | ✅ **vá** `69f03f6` *(`WO-008`)* — `KQ-019` đo 8088 + 8099 *(◐ v0.6–v0.8 là biên bản)* |
| `KQ-007 F-2` `NHE` | Hộp *"Đã bỏ ghép"* in tên ô **lặp** khi nhiều lớp *("cdt1, hd, hd, cdt1")* | đo 8099 `KQ-007` · `test_wo008_*::test_AC3_*` · `test_kq019…::test_bo_gan_bo_qua_CO__…` | ✅ **vá** `69f03f6` — 8099: *"2 ô (cdt1, hd) · 5 bút toán"* |
| `KQ-007 F-3` `NHE` | Màn ghép `Bỏ gán` **nuốt** `bo_qua` *(⛔ báo giá trị người còn lại)* | đo 8099 `KQ-007` · `test_wo008_*::test_AC4_*` · `test_kq019…` | ✅ **vá** `69f03f6` cho lệnh **một** dòng tiền *(8099 B2: 1 hộp)*; nhánh chùm ⛔ tới được bỏ gán ⇒ `KQ-019 F-1` |
| `KQ-007 F-4` `NHE` | `BA-10:82` ghi `AC-15` *(đúng `AC-16`)*; `BA-09:158`–`159` `F-10`/`F-11` còn "mã đang vi phạm" | grep | ✅ `BA` đã sửa *(`BA-10` v0.8 `:82` · `BA-09` v0.7)* — grep `KQ-010` xác nhận |
| `KQ-010 F-1` `NHE` | Bài `T1b` của Dev ⛔ bắt đột biến `B4` lọc theo **actor** và đột biến bỏ `coalesce` *(cú `Xong` của người `reason NULL` rơi im lặng)* — mã đúng | `tests/nghiem_thu/test_kq010_moc_b_dem_tren_duong_ghi_that.py` | ✅ đã lấp bằng bài nghiệm thu — `DEV` ghi nhận |
| `KQ-010 F-2` `NHE` | Actor máy là danh sách đen **một** phần tử *(mã còn `dung-lai-so@`, `nhip@fls`, `nhip@fls(tay)`)*; `B4` ⛔ loại `MAY`; UAT nhận bằng chữ *(`'uat '`, `' UAT'`, `'UAT02'` ⇒ người)*; `C8`/`G-d` ⛔ loại UAT | đo tay `KQ-010` | ✅ **vá** `88ab178` *(`WO-011`)* — `KQ-014` ĐẠT; `G-d` còn ngoài phạm vi *(⏳ v0.7 là biên bản)* |
| `KQ-010 F-3` `NHE` | `khop_owner` `B3`/`B4` đếm **mọi ảnh** `fls_pm_line` ⇒ khối `SINH-KHOP` đỏ ở ảnh PM kế tiếp *(lớp `GAP-CONG-01`)* | đo tay `KQ-010` | ✅ **vá** `88ab178` — `KQ-014` đo: mọi ảnh **204.120** dòng `tho` *(số cũ `196.480` đã trôi)*, khối ⛔ còn số |
| `KQ-014 F-1` `NHE` | Luật UAT hai mặt lệch **7.405 / 1.112.063** điểm mã ở *«ký tự sau `UAT`»* *(`[[:alpha:]]` nhận dấu kết hợp Alphabetic, `isalpha()` ⛔)* — một chiều, ỒN; `la_uat` ⛔ dùng ở đường chạy | `tests/nghiem_thu/test_kq014…::test_luat_UAT_moi_diem_ma__…` *(ghim chiều, BMP)* | ⏳ `DEV` ghi nhận |
| `KQ-014 F-2` `NHE` | `C8` nối nhật ký `(itl_id, field, actor, at)` ⛔ khoá ⇒ UAT rồi sửa thật cùng ô, cùng giao dịch ⇒ người **⛔ đếm** *(chiều IM)*; 0 đường hôm nay | tái hiện tay `KQ-014` *(kho TEST, giao dịch lùi)* | ⏳ `DEV` ghi nhận |
| `KQ-014 F-3` `NHE` | Câu cũ ⛔ do `--ghi`: `master:343` `lint` **8** kept · *«9 module»*; `roadmap:45` / `master:324` `DEV-02` **v1.0** *(thật v1.2)* | grep `KQ-014` | ⏳ `BA` |
| `KQ-014 F-4` `NHE` | **5** chuỗi actor ngoài sổ ở `fls_chup`/`fls_khai_cot` *(ngoài `T3`)*; 2 chuỗi máy trong mã ⛔ dạng `@` ⇒ lọt bài quét | `SELECT` `KQ-014` | ⏳ `BA` |
| ⭐ `KQ-019 F-1` `NANG` | Màn ghép gọi `HT.hoi` — `hop_thoai.js` ⛔ có ⇒ `Bỏ gán` trên lệnh **chùm** / gắn ≥ 2 giao dịch chết im *(`TypeError`, 0 hộp, 0 `/unmatch`)*; sổ thật **88 / 2.219** lệnh đã gán *(4,0%)*. Có từ `45a79e0`/`a09e5a1` | `tests/nghiem_thu/test_kq019…::test_F1_*` *(`xfail(strict)`)* · Chrome 8099 dòng D | ✅ **vá** `9dae3ac` *(`WO-008` vòng 2)* — `KQ-021`: Chrome 8088 sổ thật **88/88** đúng hộp; `xfail` gỡ *(trước: ⏳ `DEV` · `BA`)* |
| ⭐ `KQ-019 F-2` `NANG` | Sau `Bỏ gán` **200** màn ghép vẫn vẽ `Đã gán` + *"✓ Đang gán với giao dịch … bỏ gán"* *(`ST.dong` ⛔ làm mới)*; bấm lại ⇒ `409` im; `bo_qua` rỗng *(100% hôm nay)* ⇒ **⛔ tín hiệu nào** | `test_kq019…::test_F2_*` *(`xfail(strict)`)* · 8099 dòng C/B2/E | ✅ **vá** `9dae3ac` — `KQ-021`: 8099 L/C2/D2; `xfail` gỡ *(trước: ⏳ `DEV` · `BA`)* |
| `KQ-019 F-3` `NHE` | `Bỏ gán` lỗi / mất kết nối ⇒ `Uncaught LoiCua`, màn ⛔ hiện chữ nào; `WO-008` ghi *"như nay (⛔ Cửa lỗi…)"* — câu ấy ⛔ có trên màn ghép | `test_kq019…::test_F3_*` *(`xfail(strict)`)* · 8099 dòng E cắt mạng | ✅ **vá** `9dae3ac` — `KQ-021`: 8099 MKN/K; `xfail` gỡ *(trước: ⏳ `DEV` · `BA`)* |
| `KQ-019 F-4` `NHE` | `mo_lenh` ném sau bỏ gán **200** ⇒ hộp `bo_qua` ⛔ mở *(`BG-017` yếu #5)* | `test_kq019…::test_F4_*` *(`xfail(strict)`)* | ✅ **vá** `9dae3ac` — `KQ-021`; `xfail` gỡ *(trước: ⏳ `DEV`)* |
| `KQ-019 F-5` `NHE` | `BG-017` bảng tách `kiem_so_song` cộng **18**, tổng ghi **20** *(×5→×6, ×4→×5)* | đếm tay `KQ-019` | ✅ `BG-020` bảng tách cộng **đúng** 34 *(`KQ-021`)* *(trước: ⏳ `DEV` ghi nhận)* |
| `KQ-021 F-1` `NHE` | Màn ghép: `phim()` ⛔ nhường hộp đang mở ⇒ `Esc` trên hộp ①/② đóng hộp **và** đóng lệnh *(`BA-06:745` "bóc từng lớp một")*; `j`/`k` đổi lệnh **sau lưng** hộp. Tầm **88** lệnh | `tests/nghiem_thu/test_kq021…::test_F1_*` ×2 *(`xfail(strict)`)* · Chrome 8099 I/F2 phím thật | ✅ **vá** `f52dafe` *(`WO-023 (a)`)* — `KQ-061` gỡ dấu ×2 · ~~⏳ `DEV`~~ |
| `KQ-021 F-2` `NHE` | `Esc`/bấm ngoài khi `Gỡ cả N` đang chờ cửa ⇒ hộp đóng ⇒ cửa lỗi ghi vào hộp **đã đóng**, màn im *(`hop_thoai.js` luật ⓒ chỉ tính lúc chưa bấm)*; `F01` ⑥ cùng khuôn — ⛔ đo | `test_kq021…::test_F2_*` *(`xfail(strict)`)* · Chrome 8099 G | ✅ **vá** `f52dafe` *(`WO-023 (b)`)* — `KQ-061` gỡ dấu · ~~⏳ `BA` → `DEV`~~ |
| `KQ-021 F-3` `NHE` | `TP.tien` `maximumFractionDigits: 0` cho **mọi** tiền tệ ⇒ `1234.56 USD` in `1.235 USD` *(hộp ②, rail, ứng viên)*; sổ thật dòng USD có lẻ **2.325/3.980**, mối nối USD có lẻ **72/218** | đo 8099 U · `SELECT` sổ thật | ✅ **vá** `7746e48` + `3173d7f` *(`WO-022`)* — `KQ-029`: khứ hồi sổ thật **0** lệch; hộp *Tìm tiền* còn `KQ-029 F-1` *(trước: ⏳ `BA` → `DEV`)* |
| `KQ-021 F-4` `NHE` | Khối `SINH-KHOP` ô `B5` `49 → 50` sau `BA-06` v4.10 ⇒ `khop_owner --kiem` `CONG NO` *(nền, ⛔ do `BG-020`)* | `khop_owner --kiem` + `difflib` khối | ✅ **vá** `aa292e5` *(`WO-023 (e)`)* — `KQ-061` đột biến *(mới rc 0 / cũ rc 1)* |
| `KQ-025 F-1` `NHE` | `khop_owner --kiem` `CONG NO` trên `803889e`: ô `C3` in **số lần xuất hiện** một cụm chữ *(`59 → 60`)* — dòng thêm là **chính tờ `BG-024`**; `C2` cùng khuôn. Cùng lớp `KQ-021 F-4`, `WO-023 (e)` chỉ chữa `B5` | `khop_owner --kiem` + `difflib` khối · `git grep -c` `25f4b91` ⟷ `803889e` | ✅ **vá** `aa292e5` *(`WO-023 (e)` mở rộng)* — `KQ-061` |
| `KQ-025 F-2` `NHE` | `WO-018` cột *"Chiều ĐỎ"* sai: giữ `NGUON_TAY` ở `dao_but_toan` ⛔ làm đỏ phép so đa tập `AC-3`; `:292` của `AC-4` là `before-edit`, ⛔ đi qua `KetQuaGhi` — mã + bài đúng | đột biến `T1` · thân trả `NGUON_TAY` *(worktree)* | ⏳ `BA` *(đính chính `WO-018`)* |
| `KQ-025 F-3` `NHE` | ⑦ in bản đảo **người** *(`/reverse`)* và người **xoá ô** *(`/adjust null`)* **giống hệt** — `X → (trống) · người sửa` — trong khi sau đảo Final lùi về lớp dưới; tập **mở** *(nút `Đảo` trên mọi giá trị người)*. Có từ trước `WO-018`; sổ thật **0** | 8099 **C** · `kq025::test_e_*` | ✅ **vá** `41b9a20` *(`WO-023 (f)`)* — `KQ-061` 8088 `27728` |
| `KQ-025 F-4` `NHE` | Hộp `Đảo` *(`man_f02.js` `_dao`)* nói *"giá trị lùi về bút toán trước đó…"* cả khi đảo **gợi ý máy** — Final ⛔ đổi; **4.424** nút tới được trên sổ thật | 8099 **A** *(`fls_sua_tay` 0 → 0)* | ✅ **vá** `41b9a20` *(`WO-023 (g)`)* — `KQ-061` 8088 |
| ⭐ `KQ-029 F-1` `NANG` | Hộp **Tìm tiền** `F01L` *(`man_f01_lenh.js` `_drawer_tim_tien`)* đọc khoá hàng thô `u.tien` · `u.lech_tuyet_doi` · `u.memo`; cửa `/queue/lenh/{id}/itl-candidates` trả khuôn `⓵` *(`amount` · `lech` · `dien_giai` — `GAP-API-10`, từ `23/09`)* ⇒ cột Tiền/Lệch `—`, câu *"⛔ VƯỢT dung sai — cửa ghi sẽ TỪ CHỐI"* cho **mọi** ứng viên kể cả khớp đúng. Bài Dev `AC-6` nuôi khuôn tự nhét | `tests/nghiem_thu/test_kq029_tim_tien_khuon_cua_that.py::test_F1_*` *(gỡ `xfail` ở `KQ-031`)* · Chrome 8099 lệnh D | ✅ **vá** `e0d2a96` *(`BG-030`)* — `KQ-031` ĐẠT: 8099 + 8088 chuột thật đúng; JS cũ đỏ đúng lý do · ~~⏳ `DEV` *(`WO-022` vòng 3)*~~ |
| `KQ-029 F-2` `NHE` | `F04` trạng thái **rỗng** *(`?gia_lap=rong`)* nổ `TypeError … reading 'nguon'` ở `man_f04.js:894` *(`la_rong` ⛔ chịu `null`)*; khối chọn nguồn trống. Có từ `5f668000` *(08/09)* | Chrome 8088 `kq029/soi_f04_rong.mjs` | ⏳ `DEV` *(phiếu riêng)* |
| `KQ-029 F-3` `NHE` | `BA-06` §5b ⓘ chỉ kể `.mcols`; ô tiền ứng viên `.cand-cols` `160px` cũng cố định *(ô chữ 137px, `ellipsis` ⛔ `title`)* — hôm nay vừa 18 ký tự | Chrome 8088 `PM01812-3` | ⏳ `BA` |
| ⭐ `KQ-031 F-1` `NHE` | Hộp **Tìm tiền** `F01L` `_tinh` trừ tiền **hai đơn vị** *(⛔ so `u.curr`/`r.curr`)*; cột Tiền ⛔ mã tiền tệ ⇒ ứng viên bậc `ma` **khác tiền tệ cùng số** in *"lệch 0 ⇒ trong dung sai"* *(`note ok`)* cho cặp cửa ghi ⓔ `KhacTienTe` từ chối. Sổ thật: **4** lệnh *(`PM00329-1` 100.000 VND ↔ USD …)*; **165/5.360** ứng viên khác tiền tệ in lệch vô nghĩa. Vòng 3 làm lộ ra | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F1_*` *(`xfail(strict)` + mỏ neo xanh)* · Chrome 8088 + 8099 | ⏳ `DEV` *(+ `BA` §5b ⓕ)* |
| `KQ-031 F-2` `NHE` | `lech` bậc `ma` luôn `null` *(`lenh_cho.py:420`)* ⟷ `BA-07 ⓵` *"`null` khi khớp tuyệt đối"*; mã trả trị tuyệt đối. Sổ thật **338/448** ⇒ cột Lệch `—`, nhãn xác nhận `F01G` mất *"(lệch …)"* | `…kq031…::test_F2_*` *(`xfail(strict)`)* | ⏳ `BA` → `DEV` |
| `KQ-031 F-3` `NHE` | `the.gd`/`gd_ds` ⛔ qua `_gan_khoa_to` ⇒ khối *"đang gán"* `F01G` ⛔ tô `<mark>` *(sổ thật **0/768**)*; bài Dev tự nhét `khoa_to` — lần thứ ba lớp *"khuôn thử tự nhét"*; `BA-07` ⛔ khai `khoa_to` | `…kq031…::test_F3_*` *(`xfail(strict)`)* + canh khối | ⏳ `DEV` + `BA` |
| ⭐ `KQ-036 F-1` `NHE` | `xu_ly._bac` so tiền tệ bằng `str().upper()` ⛔ `strip` — bản thứ hai của `mg.ma_tien_te` *(`WO-032` Rủi ro 2)* ⇒ cặp `lech = 0` mà bậc ⛔ ra `tien`; sổ thật **0** giá trị `curr` mang khoảng trắng | `test_kq036…::test_F1_*` *(gỡ dấu `KQ-041`)* | ✅ **vá** `4c3b2ae` *(`WO-037 (d)`)* · ~~⏳ `DEV`~~ |
| `KQ-036 F-2` `NHE` | `_bac` nhánh cuối dán `cung_tien_te` lên `gd`/`gd_ds` **khác tiền tệ** ⛔ khớp mã *(chip "④ cùng đơn vị tiền" cạnh `lech null`)*; `BA-07 ⓵` chỉ cho `khac_tien_te` ở `/so`. Sổ thật **0 / 2.262** | `test_kq036…::test_F2_*` *(gỡ dấu `KQ-041`)* | ✅ **vá** `4c3b2ae` *(`BA-07` v3.9 · `WO-037 (c)`)* · ~~⏳ `BA` → `DEV`~~ |
| `KQ-036 F-3` `NHE` | `F01G.ve_dang_gan` gặp bậc lạ ⇒ **bỏ** chip *(`if (b)`)* ⟷ `BA-07 ⓵` *"in nguyên tên"* | `test_kq036…::test_F3_*` *(gỡ dấu `KQ-041`)* | ✅ **vá** `4c3b2ae` *(`WO-037 (e)`)* · ~~⏳ `DEV`~~ |
| `KQ-036 F-4` `NHE` | Chú giải bậc: chữ nghĩa `--faint` **2,17 : 1** trên nền trang *(đo `getComputedStyle`, 10/10 mục, `10.5px`)*; ký hiệu `--muted` 4,92 : 1 — chú giải là lối đọc nghĩa ⛔ cần chuột duy nhất | Chrome 8088 + 8099 | ✅ **vá** `4c3b2ae` *(`NFR-I29` · `WO-037 (f)`: 8088 chú giải **4,92** · `≠` **5,59**)* · ~~⏳ `BA` *(`GAP-NFR-01`)*~~ |
| `KQ-036 F-5` `NHE` | ⓐ khoá `ma_canon` ở hàng `lenh-da-gan`/`lenh-cho` ⛔ khai `BA-07` · ⓑ chiều ĐỎ `AC-4` *"b3 nhét lại `khoa_to`"* ⛔ đạt được bằng ⊆ *(đột biến `T12` sống)* · ⓒ `BA-06` ⓘ tả `.cand .amt .lech` ⛔ tồn tại | ⓑ `test_kq036…::test_CANH_bai_b3_*` | ⏳ `BA` *(ⓑ ✅ đã lấp)* |
| `KQ-036 F-6` `NHE` | **Ngoài `WO-032`**: **84 / 268** lệnh rổ `may` có đề xuất đầu `gd` **khác tiền tệ** lệnh *(cửa ghi từ chối)*; cả 84 có ứng viên cùng tiền tệ ở dưới, **45** lệch 0 | `kq036/do_84.py` 8088 | ✅ **vá** `4c3b2ae` *(`WO-037 (a)`: sổ thật `gd` khác tệ rổ `may` **0 / 184**, oracle `KQ-041`)* · ~~⏳ `BA` *(ứng viên `GAP`)*~~ |
| ⭐ `KQ-041 F-1` `NHE` | `F01L` còn ba chỗ nói *"lệch tiền"* / *"khớp đúng một dòng — chỉ DUYỆT"* cho cả nhóm `may − tu_chung`: `note ok` dưới bảng rổ *(`man_f01_lenh.js:308`)* · nhãn lọc `chỉ LỆCH TIỀN` *(`:799`, ngay sau ghi chú đã sửa)* · `RO.may`. Sổ thật: *"lệch tiền"* đúng **78 / 120**; 39 lệnh một dòng khớp đúng tiền bị giữ bởi `chum_lech_tien` **25** + `co_dong_chua_duyet` **14** | Chrome 8088 chuột thật · `kq041/oracle.py` | ✅ **vá** `db0adae` *(`BA-06` v4.18 `ⓤ` · `WO-042 (b)`; `KQ-046` 8088 + 8099 4/4 = spec)* · ~~⏳ `BA`~~ |
| `KQ-041 F-2` `NHE` | SQL `btrim(i.curr, E' \t\r\n')` hẹp hơn `str.strip()` *(`ma_tien_te` — rổ, bậc `ma`, cửa ghi)*: `NBSP` · `\v` · `\f` · `U+3000` · `U+2003` · `U+0085` ⇒ hai luật ở biên; sổ thật **0 / 8.387** | `tests/nghiem_thu/test_kq041_…::test_F2_*` *(viết lại `KQ-046` — hàm thật)* | ✅ **vá** `db0adae` *(`BA-07` v3.11 · `WO-042 (c)`)* · ~~⏳ `BA`~~ |
| ⭐ `KQ-041 F-3` **`NANG`** | **Ngoài `WO-037`** *(có từ `9ed4d4a` 22/09)*: `F01G.tai_danh_sach` ⛔ chống tải chồng ⇒ đổi chip khi đang tải trộn rổ *(8088: `Đã gán` **2955 dòng** = 2.219 ＋ **736** chưa gán)*; bấm lại chip đang chọn ⇒ mỗi lệnh hai lần *(**1.472** = 736 × 2)*. **0** ghi sai *(cửa ghi chặn)* | `test_kq041_…::test_F3_*` ×3 *(viết lại `KQ-046`)* + mỏ neo · Chrome 8088 | ✅ **vá** `db0adae` *(`BA-06` v4.18 `ⓥ` · `WO-042 (a)`; 8088 `2219` / `736`, đối chứng `2955` / `1472`)* · ~~⏳ `BA` → `DEV`~~ |
| ⭐ `KQ-046 F-1` `NHE` | Phép so tiền tệ **thứ chín** ngoài kiểm kê `WO-042`: `doc_bao_cao._SQL_UNG_VIEN` *(`ung_vien_pm`, `:309` `:310` `:317`)* so `upper(l.curr) = s.cur` — vế lệnh ⛔ `btrim` ⇒ lệnh `' vnd '` / NBSP / BOM / NEL / U+3000 cùng số tiền ⛔ hiện ở chiều ngược trong khi cửa ghi nhận cặp ấy. Cùng lớp: `do_mau_so.py:297` `GROUP BY upper(…l.curr…)`. Có từ `0f6f054`; sổ thật **0 / 276.028** | `tests/nghiem_thu/test_kq046_chieu_nguoc_ung_vien_pm_mot_tap.py::test_F1_*` *(`xfail(strict)`)* + mỏ neo | ⏳ `BA` → `DEV` |
| `KQ-046 F-2` `NHE` | `WO-042:65` *(`AC-10`)* mang **U+00A0** + **U+FEFF** thật trong chữ phiếu — đọc thành *"`' VND'`"* / *"`'VND'`"* | quét byte `KQ-046` | ⏳ `BA` |
| `KQ-046 F-3` `NHE` | `man_f01.js:766` tooltip lằn `Theo LỆNH CHI` in số cứng **1.345** *(đo 09/09)*; sổ thật `/ro` `tong` **1.601** — ngoài phạm vi `WO-042` | `grep` · Chrome 8088 · `test_wo045_thanh_lan_khong_so_cung.py` | ✅ **vá** `2b804e3` *(`WO-045` ⑤; `KQ-050` Chrome: `title` = chuỗi spec)* · ~~⏳ `BA`~~ |
| ⭐ `KQ-050 F-1` **`NANG`** *(ngoài `WO-045`)* | Cửa `/queue?curr=VND&cursor=…` *(`doc_bao_cao.doc_hang_cho` — `(x.curr, x.hang) > (…)` trên CTE cửa sổ)* mất **81–95 s** ở sổ thật; trang đầu VND và trang 2 USD **0,11 s** ⇒ `F01` VND `Xem thêm` khoá ~1,5 phút, ⛔ khung chờ | `curl` 8088 *(KQ-050)* | ⏳ `BA` → `DEV` |
| `KQ-050 F-2` `NHE` | `F01G` lượt **ô tìm** mới nhất lỗi khi lệnh mới đang tải ⇒ `Đang hỏi sổ…` **treo**, ⛔ câu lỗi *(`_tai_toan_so` ⛔ `_loi_uv`)* | `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_*` *(`xfail(strict)`)* | ✅ **vá** `5f7dd5f` *(`WO-023 (h)` ⓔ)* — `KQ-061` gỡ dấu |
| `KQ-050 F-3` `NHE` | `ST.ung_vien_chon` là **chỉ số** — lượt chữ mới thay danh sách mà ⛔ bỏ lựa chọn ⇒ `Gán` gửi dòng tiền người ⛔ chọn *(cùng lệnh; có từ trước)* | `…::test_F3_*` *(`xfail(strict)`)* | ✅ **vá** `bc5e0bc` *(`WO-023 (i)`)* — `KQ-061` gỡ dấu · ~~⏳ `BA` |
| `KQ-050 F-4` `NHE` | Bài Dev `test_wo045_…::test_AC7_doi_MUC_PHU_*` tự chứng trên phân bố tiền VND của **cả** kho TEST *(phạm vi `chi_nap_that` = mọi lần nạp)* ⇒ thêm một ca 58 dòng VND trước nó ⇒ `pytest` trọn **1 failed** "⛔ không đo được"; chạy riêng xanh | `pytest` trọn `KQ-050` lượt 2 | ✅ **vá** `7b2b901` *(`WO-023 (j)`)* — `KQ-061` |
| `KQ-031 F-4` `NHE` | `?gia_lap=rong` + mở hộp *Tìm tiền* ⇒ `TypeError … reading 'ung_vien'` `man_f01_lenh.js:578` — cùng lớp `KQ-029 F-2` | Chrome 8088 | ⏳ `DEV` |
| `KQ-029 F-4` `NHE` | Tầm `Q-TIEN-1` chỉ đếm **11** dòng sổ VND; lệnh VND có xu **2** dòng/ảnh *(`560001.60`, `1119018.74`)* ⇒ tổng VND in lẻ ở `F03` *(`…941,22`)* + chân màn `F01L` *(`…986,74`)* | `SELECT` sổ thật · Chrome 8088 | ⏳ `BA` *(bổ sung câu owner)* |
| `KQ-010 F-4` `NHE` | Câu văn ⛔ cổng canh sai cạnh số đúng *(chân trang bản vẽ dấu 01/10 mà nói 10.030 dòng sổ · 0 bút toán; `64,3%` cạnh `58,1%`…)* | grep `KQ-010` | ✅ `BA` đã sửa *(`KQ-014` đọc lại `banve:1319`: "⛔ chưa một dòng nào của kế toán" — đúng)* |
| ⭐ `KQ-061 F-1` `NHE` | Lô lưu `F02` *(`man_f02.js::_bay` → `_bao_hong` `:1051` + trạng thái `:929`)* gặp `FLS-HET-GIO` vẫn khẳng định *"1 ô dưới đây CHƯA vào sổ"* — trái `ⓕ3` *(khuôn chung chỉ đếm tiền tố "… chưa xảy ra — ")*; 8099 hạn thật: ô **đã** vào sổ *(`adj_id 4312`)* | `tests/nghiem_thu/test_kq061_f02_het_gio_lo_luu.py::test_F1_*` *(`xfail(strict)`)* · Chrome 8099 | ⏳ `BA` → `DEV` |
| `KQ-061 F-2` `NHE` *(ngoài `WO-023`)* | Lưới `F02` *(`doc_so` đọc `i.hd` thô)* ⛔ in Final ⇒ ô vừa ghi hiện `chưa gán` sau tải lại ⇒ gõ lại gặp hộp *"NGƯỜI KHÁC gõ"* cho chính mình; `BA-07:31` ⛔ nói thô hay Final; sổ thật `fls_sua_tay` **0** | Chrome 8099 *(`/fields/hd` = `sua_tay` ↔ lưới `unmapped`)* | ⏳ `BA` |

## 4. Checklist trước đóng băng mỗi GĐ

- [ ] 100% T/F của SM liên quan GĐ có test pass/chặn
- [ ] 100% ERR liên quan có negative test
- [ ] INV liên quan có property test + job kiểm chạy trong CI
- [ ] Mutation smoke module chạm tiền ≥70% killed
- [ ] Critic session đã chạy, GAP mở có quyết định con người
- [ ] Người vận hành chạy thử kịch bản nghiệm thu (ORC-03) trên staging

## Changelog
- **v0.18** *(2026-10-06, `fls-test`, `KQ-061` kiểm `WO-023` — `BG-052`…`BG-059`)*: thêm **§1.15** — truy vết `BA-06` v4.22–v4.23 *(`ⓕ1`…`ⓕ4` · `ⓦ` ④⑤⑥ · nhật ký/hoàn tác v4.12)* · `BA-07` v3.13: 11/13 mục xanh; **5** `xfail(strict)` gỡ *(`kq021` ×3 · `kq050` ×2)*; bài `kq019` sổ thật viết lại theo `TL-058`; **1** `xfail(strict)` mới *(`KQ-061 F-1`)*. §1.14: hai dòng `xfail` ⇒ ✅. `ERROR_REPORT`: `KQ-021 F-1`/`F-2`/`F-4` · `KQ-025 F-1`/`F-3`/`F-4` · `KQ-050 F-2`/`F-3`/`F-4` ✅ vá; +2 dòng `KQ-061` *(cả hai `NHE`)*.
- **v0.17** *(2026-10-05, `fls-test`, `KQ-050` kiểm `BG-048`)*: thêm **§1.14** — truy vết `WO-045` *(`BA-06` v4.19–v4.21 `ⓥ` ⑤ · `ⓦ` ①…⑤)*: 10/14 mục xanh *(26 bài Dev ĐỎ 25/26 trên `14a4b72`, Test chạy lại; Chrome 8088 sổ thật + 8099 kho TEST)*; ⭐ mục *sự thật cửa ghi* — cặp sai **cùng tệ trong dung sai** được **nhận** *(`200`)*; **2** `xfail(strict)` mới *(`KQ-050 F-2` · `F-3`)*. §1.13: dòng `ⓥ` ⑤ + `ⓦ` ⇒ ✅. `ERROR_REPORT`: `KQ-046 F-3` ✅ vá `2b804e3`; +4 dòng `KQ-050` *(1 `NANG` ngoài phạm vi · 3 `NHE`)*.
- **v0.16** *(2026-10-05, `fls-test`, `KQ-046` kiểm `BG-044`)*: thêm **§1.13** — truy vết `WO-042` *(`BA-06` v4.18 `ⓤ` + `ⓥ` ①…④ · v4.19 đoạn `ⓥ` + `ⓦ` · `BA-07` v3.11 · `BA-13` v1.9)*: 10/13 mục xanh *(Chrome có cửa sổ, đối chứng cùng máy 8088: `2955`/`1472` ⇒ `2219`/`736`)*; **2** mục chờ `WO-045`; **1** `xfail(strict)` mới *(`KQ-046 F-1` chiều ngược `ung_vien_pm`)*. §1.12: dòng `F-2` + `F-3` ⇒ ✅ *(ba bài `kq041` **viết lại** theo `TL-043`, ⛔ gỡ dấu)*. `ERROR_REPORT`: `KQ-041 F-1`/`F-2`/`F-3` ✅ vá `db0adae`; +3 dòng `KQ-046` *(cả ba `NHE`)*.
- **v0.15** *(2026-10-05, `fls-test`, `KQ-041` kiểm gộp `BG-039` + `BG-040`)*: thêm **§1.12** — truy vết `WO-037` vòng 1 + 2 *(`BA-07` v3.10 §4g ⓹ + §4h ⓵/⓵' · `BA-06` v4.17 §4.5 + `ⓤ` · `BA-08` v1.3 `NFR-I29` · `BA-13` v1.8)*: 11/13 mục xanh trên cửa thật + sổ thật chỉ đọc *(oracle độc lập lệch **0 / 1.601**)*; **2** `xfail(strict)` mới *(`KQ-041 F-2` biên khoảng trắng · `F-3` `NANG` ngoài phạm vi)*. §1.11: 3 dòng `xfail` `kq036` ⇒ ✅ *(gỡ dấu)*. `ERROR_REPORT`: `KQ-036 F-1`/`F-2`/`F-3`/`F-4`/`F-6` ✅ vá `4c3b2ae`; +3 dòng `KQ-041` *(2 `NHE` · 1 `NANG`)*.
- **v0.14** *(2026-10-02, `fls-test`, `KQ-036` kiểm gộp `BG-034` + `BG-035`)*: thêm **§1.11** — truy vết `WO-032` vòng 1 + 2 *(`BA-07` v3.8 §4h ⓵ · ⓵' · ⓹ + `GAP-API-11` ngoài · `BA-06` v4.15 §5b ⓕ ⓘ ⓙ + §4.5 ⓒ ① · `QĐ-ITL-149 ⓑ`)*: 11/15 mục xanh trên cửa thật; **3** `xfail(strict)` mới *(`KQ-036 F-1`…`F-3`)*; 3 `xfail` `kq031` của §1.10 gỡ ⇒ ✅; 6 hàng `F` mới.
- **v0.13** *(2026-10-02, `fls-test`, `KQ-031` kiểm `BG-030`)*: thêm **§1.10** — truy vết `WO-022` vòng 3 *(`BA-07` v3.6 §4h ⓵ · `BA-06` v4.13 §5b ⓕ)*: 4/7 mục xanh trên cửa thật; **3** `xfail(strict)` mới *(`KQ-031 F-1` khác tiền tệ · `F-2` `lech` bậc `ma` · `F-3` `gd.khoa_to`)*; dòng hộp *Tìm tiền* §1.9 ⛔ `xfail` ⇒ ✅ *(gỡ dấu 2 bài `kq029`)*. `ERROR_REPORT`: `KQ-029 F-1` ✅ vá `e0d2a96`; thêm `KQ-031 F-1`…`F-4` *(cả bốn `NHE`)*.
- **v0.12** *(2026-10-02, `fls-test`, `KQ-029` kiểm gộp `BG-027` + `BG-028`)*: thêm **§1.9** — truy vết `WO-022` *(`BA-06` v4.13 `UI-F10` §5b ⓐ…ⓘ + năm trạng thái)*: 10/13 mục có bài chạy hành vi xanh, 1 đọc mã; **1** mục `xfail(strict)` mới *(`F-1` `NANG` — hộp *Tìm tiền* `F01L` đọc khoá hàng thô, cửa trả khuôn `⓵`; bài Dev nuôi khuôn tự nhét)*; **1** mục chờ spec *(`F-3` ô `.cand-cols`)*. `ERROR_REPORT`: `KQ-021 F-3` ✅ vá; +4 dòng `KQ-029` *(1 `NANG` · 3 `NHE`)*.
- **v0.11** *(2026-10-02 khuya, `fls-test`, `KQ-025` kiểm `BG-024`)*: thêm **§1.8** — truy vết `WO-018` *(`BA-05` v0.34 `DD-I15 ⓓe` · `BA-06` v4.9 dòng nhật ký)*: 7/8 mục có bài chạy hành vi xanh *(`kq025` lấp lỗ cửa `/reverse` qua HTTP + màn, và đột biến `T3` "lớp theo ô" mà bộ bài Dev ⛔ bắt)*; 1 mục chờ spec *(`F-3` chữ cho bản đảo người)*. Dòng ⏳ `ⓓe` của §1.6 nay ✅. `ERROR_REPORT`: +4 dòng `KQ-025` *(cả 4 `NHE`)*.
- **v0.10** *(2026-10-02 tối, `fls-test`, `KQ-021` kiểm `BG-020`)*: thêm **§1.7** — truy vết `WO-008` vòng 2 *(`BA-06` v4.10 ⓔ ①…⑤ + trạng thái tải)*: 7/9 mục có bài chạy hành vi xanh *(`kq021` lấp 5 lỗ phủ: `T1` `T2` `T4` `T6` `T18`; bài sổ thật **88** lệnh qua hàm thật)*; 2 mục `xfail(strict)` mới *(`F-1` `Esc`/`j` sau lưng hộp · `F-2` lỗi vào hộp đã đóng)*; 1 mục chờ spec *(`F-3` tiền ngoại tệ)*. §1.6: 4 dòng `xfail` nay xanh *(gỡ dấu)*. `ERROR_REPORT`: `KQ-019 F-1`…`F-5` ✅; +4 dòng `KQ-021` *(cả 4 `NHE`)*.
- **v0.9** *(2026-10-02 chiều, `fls-test`, `KQ-019` kiểm `BG-017`)*: thêm **§1.6** — truy vết `WO-008` *(`BA-06` v4.9 ba chỗ chữ · mục ⓔ chùm · lỗi/mất kết nối · `BA-05` v0.34 `DD-I15 ⓓe`)*: 3 mục xanh *(6 đột biến bị bắt)*, 4 mục `xfail(strict)` là phát hiện mới, `ⓓe` chờ `WO-018`; ba dòng ⏳ của §1.4 nay ✅. `ERROR_REPORT`: `KQ-007 F-1`/`F-2`/`F-3` ✅ vá `69f03f6` *(`F-3` phần chùm ⇒ `KQ-019 F-1`)*; +5 dòng `KQ-019` *(2 `NANG` · 3 `NHE`)*.
- **v0.8** *(2026-10-02 trưa, `fls-test`, `KQ-014` kiểm `BG-013`)*: thêm **§1.5** — truy vết `WO-011` *(`T1`…`T7`, `G-d`, hai bảng ảnh/khai)*: 8/10 mục có bài chạy hành vi, 12 đột biến bị bắt; vế `C8` của §1.3 nay ✅. `ERROR_REPORT`: `KQ-010 F-2`, `F-3` ✅ vá `88ab178`; `F-4` ✅ `BA`; +4 dòng `KQ-014` `NHE`.
- **v0.7** *(2026-10-01 tối, `fls-test`, `KQ-010` kiểm `BG-009`)*: thêm **§1.3** — truy vết `WO-001` *(`T1a` · `QĐ-ITL-150 ⓐ` cho `B2/3/5` và `B4` · `AC-2b` · `done` `reason NULL` · `T2` · `T4` · vế `C8`/`G-d`)*: 6/8 mục có bài chạy hành vi; `T4` chỉ cổng giấy; `C8`/`G-d` chưa khai. **§1.4** rà `BA-06` v4.8 · `BA-09` v0.7 · `BA-10` v0.8 *(BA yêu cầu ở `KQ-007`)*: ba mục màn v4.8 **chưa có bài** — chờ `WO-008`. `ERROR_REPORT`: `KQ-007 F-4` ✅, `F-1`…`F-3` ◐ spec đã trả; +4 dòng `KQ-010` `NHE`.
- **v0.6** *(2026-10-01 tối, `fls-test`, `KQ-007` kiểm `BG-006`)*: ⭐ thêm **§1.2** — truy vết `WO-003` vòng 2 *(`INV-I22` ⓐⓑ · `SM-I06 F-10`/`F-11` · `DT-I14` `5a`/`6`/`7`/`8` · định nghĩa `bo_qua`)* → bài: **8/9** mục có bài chạy hành vi, cả 8 gọi tên mã; `INV-I22 ⓑ` chỉ đo tay *(0 / 4.424)*. Ma trận §1: `BA-11` **21 → 22**, bài gọi tên **8 → 10** *(thêm `I20` — đã có từ trước mà v0.5 ⛔ đếm — và `I22`)*. `ERROR_REPORT`: `KQ-005 F-1`/`F-2` → ✅ vá; +4 dòng `KQ-007` `NHE` gửi `BA`. §1.1 giữ nguyên làm biên bản.
- **v0.5** *(2026-10-01, `fls-test`, `KQ-005` kiểm `BG-004`)*: ⭐ thêm **§1.1** — truy vết `QĐ-ITL-149` · `SM-I06` *(9 chuyển cấm)* · `DT-I14` *(8 nhánh)* → bài, **đọc spec rồi tìm bài** *(⛔ suy từ tên hàm)*: `SM-I06` 8/9 có bài *(`F-6` gap tự khai)*, `DT-I14` 7/8 *(nhánh 5 ⛔ bài)*. ⭐ `ERROR_REPORT` từ trống → **2** lỗi mở *(`KQ-005 F-1`, `F-2`)*, mỗi lỗi một bài `xfail strict`. ⚠ Banner `⏸` đầu tệp vẫn đúng cho §1 bảng tổng; §1.1 là phần **đã dẫn xuất cho ITL**.
- **v0.4** *(2026-09-18 tối muộn, `QĐ-ITL-143` — quy trình `CR` bắt rà tệp này khi chạm `BA-11`)*: ⭐ `BA-11` **20 → 21** bất biến; bài **gọi tên** **7 → 8**. ⭐⭐ **Và `INV-I21` là cái ĐẦU TIÊN ra đời ĐÃ KÈM bài gọi tên nó** — bảy cái trước đều được gọi tên **về sau**, tình cờ. ⇒ Số *«⛔ không ai gọi tên»* **đứng nguyên 13**, tức lần này ⛔ **không** thêm nợ. ⛔ Đây đúng là việc mà `v0.3` nói là *«đáng làm trước»*: ⛔ không phải viết thêm test, mà **đặt mã spec vào tên bài** — lần này làm được vì bất biến và bài thử **sinh ra cùng một lượt**. ⭐ Bài xanh **1.698 → 1.712** *(＋9 bài `test_may_goi_y_pg.py`, đỏ trước)*; tệp test **128 → 145**.
- **v0.3** *(2026-09-18, `CR#12`·`CR#13` — bước 2 quy trình CR bắt rà tệp này khi chạm `BA-05`/`BA-11`)*: ⭐⭐ **Ma trận truy vết thay `0` bằng một PHÉP ĐẾM THẬT, và phép đếm ấy lộ ra chỗ đáng làm trước.** Đo `18/09`: **1.698** bài xanh · **128** tệp · `BA-11` có **20** bất biến mà chỉ **7** được bài nào **gọi tên** ⇒ ⛔ **13 bất biến ⛔ không bài nào gọi tên**. ⛔⛔ **Năm spec còn lại ghi `⛔ chưa đếm được` — và đó là SỰ THẬT, ⛔ không phải lười**: `BA-09`/`BA-10`/`BA-03`/`BA-04`/`BA-07` ⛔ **không có mã định danh nào xuất hiện trong mã test**, nên ⛔ **không có gì để đếm**; tôi ⛔ **không** dựng bảng bằng cách suy từ tên hàm *(`R-A1`)* — đúng lập trường `v0.2`. ⇒ ⭐⭐ **Việc đáng làm trước ⛔ không phải viết thêm test, mà là ĐẶT MÃ SPEC vào tên bài** để cột này **đo được**. ⭐ `GAP_REPORT` từ **rỗng** → **5 GAP đang mở + 1 đã đóng**, mỗi cái có người phát hiện và trạng thái quyết định.
- **v0.2** (2026-09-07, `QĐ-ITL-103`): ⛔ **Đính chính một câu SAI đã đứng 12 ngày** — *"dự án chưa code"*, trong khi thực đo là **1.073 phép thử xanh / 8.771 dòng / 5 pha xong**. ⛔ **Chỉ đính chính, ⛔ không lấp bảng truy vết**: dẫn xuất `BA-09`/`BA-10`/`BA-11` → test là việc **QA làm bằng đọc spec**, ⛔ không phải việc tôi suy từ tên hàm test *(`R-A1`)*. ⚠ Ghi kèm bài học: **banner `⏸` ⛔ không miễn trừ một câu sai** nằm dưới nó.
- v0.1 (2026-07-17): Khởi tạo khuôn forward-fill.
