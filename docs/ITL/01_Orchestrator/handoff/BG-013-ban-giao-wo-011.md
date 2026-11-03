# BG-013 — bàn giao `WO-011` *(sổ actor một chỗ · UAT một luật · actor mới gọi tên · `B4` loại máy · `khop_owner` trên ảnh hiệu lực · phép so `09` §7 · `--ghi`)*

| | |
|---|---|
| **Thuộc** | `WO-011` *(vòng 1)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`88ab178`** *(mã + bài thử + `khop_owner` + khối `SINH-KHOP` + `03_Dev` + `HOI-012`)* → **`75d9f85`** *(`T9` — `dong_bo_so_song --ghi`)* — **đã đẩy**. Phiếu này + nhật ký + `README` ở commit kế tiếp *(⛔ chạm `fls/`)* |
| **Spec đã đọc** | `WO-011` *(bản sửa 02/10)* · `09_MILESTONES` **v1.14** §2 luật *"người thật"* ⓐ…ⓔ + §7 dòng `B` · `BA-14` **v0.8** §8.4 `G-d` · `10_HOP_DONG_AGENT` **v1.1** §6 · `00_MASTER_INDEX` **v0.30** `QĐ-ITL-150` · `KQ-010` `F-2`/`F-3` + bài `test_kq010_…` · `BG-009` |
| **Câu hỏi đã mở** | [`HOI-012`](HOI-012-ke-toan-la-may-hay-nguoi-va-cau-sql-thuan.md) `KHONG_CHAN` — làm theo phương án ⭐ của cả hai câu, chờ `TL` |

> **Một câu cho owner:** máy nay biết **9** tài khoản ⛔ phải người *(trước: 1)*, khai ở **một** tệp; một tài khoản lạ xuất hiện trên sổ thì cổng **gọi tên nó** và đỏ một lần cho tới khi có người xác nhận; dòng thử `UAT` nhận dù gõ hoa/thường/có khoảng trắng. Con số mốc `B` trên sổ thật **⛔ đổi**: **`1 · 1 · 3`**, người thật **0**, tài khoản lạ **0**.

```mermaid
flowchart LR
  E[("fls_queue_event")] --> R{"evt_type = 'reason'?"}
  R -- có --> X1["⛔ đếm"]
  R -- không --> M{"actor ∈ ACTOR_MAY?<br/>(9 — sổ danh_muc_actor)"}
  M -- có --> X2["⛔ đếm"]
  M -- không --> U{"la_uat(reason)?<br/>(MỘT luật)"}
  U -- có --> X3["⛔ đếm"]
  U -- không --> N["NGƯỜI ⇒ B2·B3·B5"]
  M -- "không, và ∉ ACTOR_DA_THAY" --> A["⚠ ACTOR MỚI: tên · n dòng<br/>cổng NO (vẫn đếm là người)"]
```

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/danh_muc_actor.py` *(mới)* | **`T1`** sổ actor: `ACTOR_MAY` **9** hằng có chủ *(`may@fls` · `nhip@fls` · `nhip@fls(tay)` · `dung-lai-so@apero.vn` · `thu@apero.vn` · `cong-ghi@apero.vn` · `cong@apero.vn` · `verify-sua-duoc-gi@fls` · `verify-sua-duoc-gi-2@fls`)* + `ACTOR_DA_THAY = {khanhcq@apero.vn}`. **`T4`** `la_uat()` + `sql_la_uat()`/`sql_khong_uat()` *(một luật)* + `sql_ngoai_may()` |
| `fls/repo/may_ghep.py` · `fls/repo/nhip_chup.py` | `MAY`, `ACTOR_NHIP`, `ACTOR_TAY` **lấy từ** sổ *(tên cũ giữ — nhiều chỗ import)* |
| `tools/dung_lai_so.py` · `don_ly_do_sai.py` · `chay_cua.py` · `verify_cua_ghi.py` · `verify_cua_that.py` | chuỗi actor ⇒ import từ sổ |
| `tools/verify_sua_duoc_gi.py` | actor `ke-toan@apero.vn`/`ke-toan-2@apero.vn` ⇒ `verify-sua-duoc-gi@fls`/`-2@fls` *(`HOI-012` câu 1 ⭐ — chỉ chạy kho TEST)* |
| `tools/demo_dong.py:697` | dòng chữ minh hoạ cú `Xong` của người: `actor='ke-toan@apero.vn'` ⇒ `actor='<email người bấm>'` *(⛔ email bịa trong `tools/`)* |
| `tools/kiem_so_song.py` | **`T2`/`T5`** `su_kien_cho_nguoi` **và** `moi_noi_da_bo` *(`B4` nay loại cả máy)* mang hai mẩu **sinh từ sổ**, chép vào chuỗi THUẦN *(`HOI-012` câu 2)*; `_kiem_hang_may(sql, tien_to)` đối chiếu **trùng byte** cả danh sách + mẩu UAT mỗi lần chạy. **`T3`** `_q_actor_moi()` + `canh_actor_moi()` + khối in trong `main()` *(NO khi có)*. **`T7`** `Muc("mốc · §7 dòng B · phía PM")`. `anh_nhip`/`anh_nhip_gio` lấy `ACTOR_NHIP` từ sổ |
| `docs/ITL/_tools/khop_owner.py` | **`T6 ⓐ`** `C8` loại máy + UAT; **`ⓑ`** `B3`/`B4` đo trên `anh_pm_hieu_luc(conn, chi_nap_that())`; **`ⓒ`** `Ket.man` *(số tuyệt đối ra màn)*, cột `kho` của `B3`·`B4`·`C5b` chỉ mang **quan hệ**; `Boi.so(sql, ts)` nhận tham số |
| `docs/ITL/_AUDIT_ALIGNMENT_ROADMAP.md` | chỉ khối máy sinh `SINH-KHOP` *(`khop_owner.py` ⛔ `--kiem`)* — ⛔ còn `196.480` |
| `tests/repo/test_danh_muc_actor.py` *(mới, 31)* · `tests/test_kiem_so_song.py` *(+48)* · `tests/repo/test_wo011_thuoc_nguoi_pg.py` *(mới, 9 — mỗi bài một giao dịch **LÙI**)* | **`T8`** |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `02_REPO_CONVENTIONS.md` *(v1.1 → **v1.2**)* | dòng `WO-011`; quy ước *"actor ⛔ phải người khai một chỗ"* |
| `00_MASTER_INDEX.md` · `06_ORCHESTRATOR_DASHBOARD.md` · `08_MIGRATION_ROADMAP.md` · `02_BA/Artifacts/Ban-ve-Kien-truc-TOBE.html` | **`T9`** `dong_bo_so_song --ghi` *(25 mục, 0 bỏ qua — commit `75d9f85`)* |

⛔ **Không** đổi schema · ⛔ **không** ghi kho thật · ⛔ **không** chạm `tests/nghiem_thu/**` *(`git diff 27c163a -- tests/nghiem_thu/` = rỗng)* · `--ghi` chạy **một** lần.

### Câu cạnh số *(`10 §6 ⓑ`)* — đã rà **16** chỗ `--ghi` đổi, **0** câu phải sửa
⚠ Commit `75d9f85` ghi *"ra 11 chỗ"* — **sai đếm**; đúng là **16** *(bảng dưới)*. ⛔ sửa lịch sử commit.

| Tệp:dòng | Số đổi | Câu cạnh số còn đúng nghĩa? |
|---|---|---|
| `master:316` §8 tiêu đề | `97 → 103` tệp · `45 → 46` hiện vật | ✅ chỉ là số |
| `master:325` dòng `04_Test/` | `1958 → 2051` test | ✅ *"lạc hậu **hơn 1.400** phép thử (đo 01/10)"* — `2051 − 548 = 1.503` ⇒ vẫn đúng *(hụt, ⛔ sai)*; ⛔ sửa |
| `master:343` §10 | `1958 → 2051` · `24.982 → 25.133` · `249.288 → 256.928` · `109 → 110` · dấu `01/10 18:20 → 02/10 10:09` | ✅ — ⚠ cùng câu ghi `lint-imports` **`8` kept** *(thật `9`)*: lệch **có từ trước**, ⛔ số `--ghi` đổi ⇒ ⛔ sửa *(chủ câu: `fls-ba`)* |
| `dash:116`–`118` *(Test · code / Cổng / Kho thật)* | test `2051 (1782 + 269)` · `25.133` dòng · `256.928` · `02/10 10:09` · `110/110` | ✅ |
| `dash:120` *(mốc `A`)* | ảnh nhịp `131·143 → 135·147` | ✅ câu đi kèm chính là *"bốn con số kiểu này TỰ LỚN LÊN mỗi cú chụp (`GAP-CONG-01`)"* |
| `dash:131` *(nhánh)* | `5fbc29c → 88ab178` | ✅ *"lần sửa `fls/` gần nhất"* — đúng |
| `dash:139` · `:145` *(bảng tiến độ `repo` · `TỔNG`)* | `6.999/528 → 7.150/568` · `24.982/1742 → 25.133/1782` | ✅ |
| `roadmap:45` | `2051` · `25.133` · `256.928` · `02/10 10:09` | ✅ — ⚠ cùng câu *"`DEV-02` quy ước v1.0"* *(thật **v1.2** sau phiếu này; v1.1 từ 17/09)*, *"chỉ `.py` của 9 module"* — ⛔ số `--ghi` đổi |
| `banve:1072`–`1073` thẻ *"Phép thử tự động"* | `2051` · `25.133` | ✅ *"phần kiểm nhiều hơn phần làm"* |
| `banve:1097` thanh `repo` · `:1202` caption khối 6 | `528 → 568` · `18 → 19` tệp · `7.150` | ✅ |
| `banve:1319` chân trang | `01/10 → 02/10/2026` · `5fbc29c → 88ab178` · `2051` · `110/110` · `68 ảnh · 256.928` | ✅ đo lại từng vế cho ngày mới: `kiem_tai_lieu` ĐẠT · `pg_verify` *"khop: 25 bang/view"* · `69.510/69.510` = bài `tests/ledger/test_parity_ca_so.py:132` xanh trong `2051` · *"Sổ bút toán … ⛔ chưa một dòng nào của kế toán"* — người thật **0** |
| `banve:1395` thẻ ảnh nhịp | `135 · 147` | ✅ |
| `banve:1400` thẻ ảnh lệnh chi | `66 → 68` | ✅ câu đã **trỏ** *("nhiều — số ở trên")* |

## Cổng *(kết quả nguyên văn — `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`, `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` *(cây `88ab178`)* | `2051 passed in 265.60s (0:04:25)` — ⛔ `xfail`, ⛔ `XPASS`, ⛔ `skipped`. Nền `KQ-010` **1.963** ⇒ **+88** = 31 + 48 + 9 bài mới |
| `pytest tests/nghiem_thu/test_kq002_… test_kq010_…` | xanh trong cả bộ; `git diff 27c163a -- tests/nghiem_thu/` **rỗng** |
| `python tools/kiem_so_song.py` — nền @ `27c163a` *(đầu lượt)* | `⛔ CONG SO SONG KHONG DAT — 22 lech/khong-do-duoc` *(17 nhóm: nhịp chụp thêm **2** ảnh PM sáng 02/10 `66 → 68` · `249.288 → 256.928` · số tệp `97 → 101` · phép thử `1958 → 1963`…)*; mốc B ×3 **OK** |
| `python tools/kiem_so_song.py` — @ `88ab178`, trước `--ghi` | `may do : 126 con so · 110 phep so tren 6 file` · `⛔ CONG SO SONG KHONG DAT — 44 lech/khong-do-duoc` *(26 nhóm; thêm so nền: phép thử `2051`, module `repo`, hash `88ab178`, `109 → 110` phép so)*; `OK mốc · §7 dòng B · phía PM` · `OK cổng mốc B · actor ngoài sổ (`ACTOR_MAY ∪ ACTOR_DA_THAY`): 0` · mốc B ×3 **OK** |
| `python tools/dong_bo_so_song.py --ghi` *(một lần)* | `25 muc soan · 0 muc BO QUA (cong ⛔ khong do duoc)` |
| `python tools/kiem_so_song.py` — sau `--ghi` | `✅ cong so song DAT — 110 phep so, moi phep khop DUNG mot lan va khop dung con so MAY do (commit `88ab178`)` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (103 file, 1233 bang, 644 o ngay, 104 ma QD), khong chi 'khong thay loi'` |
| `python docs/ITL/_tools/khop_owner.py --kiem` — nền @ `27c163a` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `⛔ ⛔ CONG NO: · ⛔ khoi trong lo trinh LECH voi ban sinh lai` *(chính `KQ-010 F-3`: ảnh PM sáng 02/10)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` — sau | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong `C1` DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)`; màn in `· anh `NAP-2026-10-02-PME7F31617`: 3820/3820 dong co cha PE hoac PI` · `· anh …: 0 ngoai le / 3.820 dong co `tho`` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — ⛔ chạm schema *(chạy thì áp lên kho thật)*. Thay bằng `python -m fls.db.pg_verify` *(chỉ đọc)*: `khop: 25 bang/view dung nhu khai bao` |

⚠ **Đỏ lại sau phiếu này?** Tệp `BG-013` được dựng *(khung)* **trước** `--ghi` ⇒ số tệp `103` đã tính nó; phiếu + nhật ký + `README` ⛔ chạm `fls/` ⇒ hash ⛔ đổi. ⇒ Mong `kiem_so_song` **vẫn 0** ở commit phiếu — **trừ** nhóm ảnh nhịp/PM nếu nhịp chụp thêm ảnh *(loại ⓐ, `GAP-CONG-01` — ⛔ hồi quy)*. Đo lại ngay sau commit phiếu: xem dòng nhật ký §5.

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Chiều ĐỎ đã chứng *(đột biến — kịch bản tạm, mỗi mẫu khớp **đúng 1** lần, trả nguyên, so `sha256`)* |
|---|---|---|
| **AC-1** | sổ **9** actor *(⛔ 8 — `HOI-012` câu 1)*; bài `test_QUET_MA__moi_hang_actor_trong_fls_tools_THUOC_so` *(quét `ast` mọi hằng chuỗi `.py` + nguyên văn `.cmd`/`.js`/`.html`… của `fls/`+`tools/`, ⛔ `tests/`)* · `test_KHONG_GO_LAI__hang_bang_dung_actor_may_chi_o_SO` · `test_SO_MAY_du_va_ghim` · `test_hang_cu_LA_hang_cua_so`. `grep -rlF '"<actor>"' fls tools --include=*.py` ⇒ mỗi actor máy **chỉ** `fls/repo/danh_muc_actor.py`; `ke-toan@apero.vn` ⇒ **0** tệp. ⚠ `grep` thô *(kể cả chú thích)* vẫn thấy chuỗi ở `tools/kiem_so_song.py` *(câu SQL thuần + chú thích)*, `soi_nhip.py`/`nhip_chup.py`/`nhip_chup.cmd`/`ghi_tay.py` *(chú thích, `rem`, chuỗi `print`)* — ⇒ `AC-1` *"chỉ còn ở một tệp"* đúng cho **hằng bằng actor**, ⛔ cho `grep` thô *(`HOI-012` câu 2)*. Trước vá: `3 failed` *(quét: `ke-toan@apero.vn` ở `demo_dong.py`+`verify_sua_duoc_gi.py`, `ke-toan-2@apero.vn`; gõ lại: 7 actor ở 7 tệp; tên cũ ⛔ trỏ sổ)* | `D1` thêm `THU_MOI = "thu-moi@fls"` vào `tools/chay_cua.py` ⇒ `1 failed` *(đúng bài quét)* · `D2` xoá `ACTOR_NHIP` khỏi `ACTOR_MAY` ⇒ `6 failed` *(quét · ghim sổ · câu SQL lệch sổ ×2 · `AC-3` máy · `AC-4[nhip@fls]`)* |
| **AC-2** | kho THẬT *(chỉ đọc)* `kiem_so_song`: `OK dashboard · cổng mốc B` · `OK mốc · cổng mốc B` · `OK bản vẽ 13 · tổng kết cổng mốc B` *(tài liệu `1 · 1 · 3`)* · `OK cổng mốc B · actor ngoài sổ …: 0`. Actor trên 3 bảng gốc 02/10: `fls_queue_event` `reason/dung-lai-so` **108.128** · `match/may@fls` **2.219** · `match`+`unmatch/khanhcq` **1+1** *(UAT)*; `fls_adjustment` `may@fls` **4.424** + `khanhcq` **4**; `fls_journal` cùng — **mọi** actor ∈ sổ | — |
| **AC-3** | `test_AC3_actor_MOI_dem_la_NGUOI__goi_ten__khai_DA_THAY_thi_im` *(kho TEST, `ghep_lenh(actor='nguoi-moi@apero.vn', reason=None)` ⇒ đếm **1** ⇒ mốc `4·1·0`; `_q_actor_moi` ⇒ `[('nguoi-moi@apero.vn', 1, 5)]` — **1** thao tác, 5 dòng ở 3 bảng; dòng báo bắt đầu `⚠ ACTOR MỚI: nguoi-moi@apero.vn · 1 dòng`; khai vào `ACTOR_DA_THAY` ⇒ báo **biến mất**, mốc **vẫn** `4·1·0`)* · `test_AC3_cong_NO_khi_co_actor_moi` *(`main()` trả **1** + in tên; danh sách rỗng ⇒ **0**)* · `test_AC3_khai_actor_moi_vao_ACTOR_MAY_thi_B5_DUNG` *(⇒ `1·1·3`)* | `D3` `canh_actor_moi` trả rỗng *(im lặng)* ⇒ `3 failed` · `D4` câu SQL chỉ đếm actor đã biết *(loại actor mới)* ⇒ bài `AC-3` ĐỎ |
| **AC-4** | `test_T2_MOI_actor_may_trong_SO_dem_0_nguoi[×9]` · `test_T5_B4_bo_ghep_cua_MAY_dem_0[×9]` *(CTE)* · `test_AC4_MAY_ghep_roi_bo_ghep_thi_moc_B_DUNG_ca_B4[nhip@fls · dung-lai-so@apero.vn · verify-sua-duoc-gi@fls]` *(cửa ghi thật, kho TEST: `fls_pm_unlink` = **1** ⇒ ⛔ tập rỗng; người **0**, bỏ ghép **0**, mốc `1·1·3`)*. Trước vá: `T2` **8/9** đỏ *(trừ `may@fls`)*, `T5` **9/9** đỏ | `D5` bỏ vạch máy ở `B4` ⇒ `15 failed` |
| **AC-5** | `test_la_uat_PYTHON_theo_bang_mau[×25]` · `test_la_uat_SQL_TRUNG_Python_tren_CUNG_bang_mau` *(**25** mẫu: `AC-5` + `\t`/`\n`/NBSP/`U+3000`/BOM đầu, `UAT_02`, dấu kết hợp, `é`/`đ`/`Ư`/`中` sau `UAT`, `UẤT`, `''`, `NULL`; hai mặt trùng, và `sql_khong_uat` = **phủ định** đúng của `sql_la_uat` kể cả `NULL`)* · `test_T4_UAT_MOT_luat__cau_cong_TRUNG_la_uat[×25]` *(chính câu cổng)* · `test_T5_B4_UAT_MOT_luat_va_NGUOI_null_van_dem` · `C8` ở `AC-6`. Trước vá: **12** biến thể UAT bị đếm là người | `D6` về `left(…, 4) <> 'UAT '` ⇒ `3 failed` · `D7` `'%uat%'` ⇒ `'ghi chú UAT 02/10'` lệch *(1 failed)* · `D8` bỏ `coalesce` ⇒ `3 failed` *(gồm bảng mẫu `NULL`)* |
| **AC-6** | `test_AC6_C8_UAT_va_MAY_KHONG_lat__NGUOI_lat` *(kho TEST, `ghi_but_toan`: 2 cú UAT `'uat 02/10 …'`/`'  UAT02/10'` + 1 cú actor máy ⇒ `fls_sua_tay` **3** dòng ⇒ `C8` vẫn `khop=True` = `mong`; thêm 1 cú của người ⇒ `khop=False` ≠ `mong` ⇒ `--kiem` **CONG NO**)*. Lý do đọc `fls_journal` nối `(itl_id, field, actor, at)` — sổ thật 02/10: **4/4** dòng `sua_tay` nối **đúng 1** nhật ký *(vì sao ⛔ `evt_id`: `ghi_but_toan` ghi `evt_id NULL`)*. Kho thật: `NGUOI chot 0` | `D9` bỏ lọc UAT ⇒ `1 failed` · `D10` bỏ lọc máy ⇒ `1 failed` |
| **AC-7** | kho THẬT *(màn)*: ảnh `NAP-2026-10-02-PME7F31617` — `3820/3820 dong co cha` · `0 ngoai le / 3.820`; `grep -c 196.480 docs/ITL/_AUDIT_ALIGNMENT_ROADMAP.md` ⇒ **0**. `test_AC7_anh_THU_HAI_cung_noi_dung__khoi_TRUNG_BYTE__ngoai_le_thi_NO` *(kho TEST trong giao dịch lùi: ảnh 1 ⇒ khối; ảnh 2 **cùng nội dung** ⇒ khối **trùng byte**; ảnh 3 có **1** dòng `tho` mang cả `ID PELine` lẫn `ID PILine` ⇒ `B4 khop=False` ≠ `mong` ⇒ CONG NO, màn `1 ngoai le`)* | `D11` `B4` đếm trên **mọi** ảnh ⇒ `1 failed` *(khối đổi ở ảnh 2)* |
| **AC-8** | `test_T7_phep_so_09_muc7_dong_B_CO_va_khop_DUNG_mot_lan`; kho thật `OK mốc · §7 dòng B · phía PM` | sửa `09` `58,1%` ⇒ `58,2%` *(tệp thật, trả nguyên `sha256`)* ⇒ `⛔ mốc · §7 dòng B · phía PM (nhom 1): tài liệu ghi `58,2` · MÁY đo `58,1` ⛔ LỆCH` |
| **AC-9** | `2051 passed` *(⛔ xfail)*; lint `9 kept, 0 broken`; **+88** = 31 + 48 + 9 *(1.963 ⇒ 2.051)*; `git diff 27c163a -- tests/nghiem_thu/` rỗng, `kq002` + `kq010` xanh | — |
| **AC-10** | `kiem_so_song` **0** lệch *(110 phép)*; `kiem_tai_lieu` ĐẠT *(103 file)*; `khop_owner --kiem` ĐẠT *(⛔ `CONG NO`)*; bảng câu cạnh số ở trên | — |

### `T6 ⓒ` — rà **mọi** phép trong khối `SINH-KHOP`: chữ có đổi khi chỉ có một ảnh mới cùng nội dung?
| Phép | Cột `kho` | Trôi theo ảnh? | Làm gì |
|---|---|---|---|
| `B3`, `B4` | đếm `fls_pm_line` **mọi** ảnh | ✅ **có** *(`KQ-010 F-3`; 02/10 sáng khối đã lệch)* | ⭐ ảnh hiệu lực + quan hệ — `mong` ⛔ đổi |
| `C5b` | `8366/8387` dòng có `Diễn giải` *(khung xem nối ảnh Bank **mới nhất**)* | ✅ **có, đã đo**: `8.366` *(01/10 khuya)* ⇒ `8.370` *(02/10, ⛔ ai làm gì)* — đổi khi ảnh Bank mới mang chữ khác ở dòng cũ | ⭐ quan hệ *("CO dong so mang `Dien giai`")*, số ra màn; `mong` ⛔ đổi *(**một** phép ngoài `B3`/`B4` — Rủi ro 3 cho phép)*; bài `test_T6c_C5b_…` + `D12` *(in số vào khối ⇒ ĐỎ)* |
| `A2` | `{n}` ảnh lằn `Cash` | ⚠ **sẽ** — hôm nay `0` *(lằn Cash chưa chụp)*; ngày lằn mở, mỗi ảnh `+1` | ⛔ đổi — `mong=False` sẽ lật đúng một lần; ghi lại đây |
| `B1` | vũ trụ cột = `count(distinct key)` trên mọi ảnh | ⛔ — ảnh cùng nội dung ⛔ thêm khoá | — |
| `A1` · `C5` · `C6` · `C8` | loại nguồn · `memo` sổ · số bút toán · máy/người | ⛔ theo ảnh — chỉ đổi khi **ghi** *(nạp sổ / bút toán)* — đó là đổi thật | — |
| `T1`–`T3` · `B2` · `B5` · `B6` · `C1`–`C4` · `C7` | mã / tài liệu | ⛔ | — |

## Kho thật
- `KHONG_CHAM` — chỉ `SELECT` *(actor theo bảng, nối `fls_adjustment` ↔ `fls_journal`, `pg_verify`)*. Mọi bài mới chạy **kho TEST**; `test_wo011_…` trong **một giao dịch LÙI** ⇒ ⛔ để lại dòng nào. Máy 8088 ⛔ chạm, ⛔ dựng máy thứ hai.

## Dev tự thấy còn yếu
1. **`HOI-012` câu 1 — tôi đã chọn thay BA.** `ACTOR_MAY` có **9** phần tử, ⛔ 8 như `AC-1`; `ke-toan@apero.vn` **⛔ ở sổ nào** và công cụ `verify_sua_duoc_gi.py` đổi tên actor. Nếu `TL` chọn phương án 2/3 thì phải đổi một hằng + bài `test_SO_MAY_du_va_ghim`. Bài quét **⛔ bắt** chuỗi `ke-toan@apero.vn` trong `tests/` *(cố ý — người mẫu)*, nên nếu một ngày công cụ ghi kho thật bằng tên ấy thì nó được đếm là người và cổng **gọi tên** nó *(`T3`)* — đó là lưới cuối.
2. **Câu SQL thuần vẫn mang BẢN CHÉP danh sách** *(`HOI-012` câu 2)* — ⛔ thoả nguyên văn *"⛔ gõ lại danh sách trong SQL"*. Bản chép bị `_kiem_hang_may` ép **trùng byte** mỗi lần chạy + 2 bài, nhưng thêm một actor máy vẫn đòi người sửa **hai** chỗ *(sổ + chuỗi)* — cổng đỏ nói đúng chỗ, ⛔ lặng lẽ.
3. **Luật "khoảng trắng" khai tay** `' \t\n\r\f\v'` + `U+00A0` · `U+3000` · `U+FEFF`. Ký tự trắng Unicode khác *(`U+2002`…`U+200A`, `U+2028`)* ⛔ trong tập ⇒ `'\u2003UAT …'` tính là **người** *(chiều cổng nhích — có người nhìn)*. Chữ cái dùng `[[:alpha:]]` của locale kho `en_US.utf8` ↔ `str.isalpha()` — trùng trên **25** mẫu, ⛔ chứng minh cho mọi ký tự Unicode; đổi locale kho có thể lệch.
4. **`C8` nối nhật ký bằng `(itl_id, field, actor, at)`** — đúng vì `_them` chèn hai dòng trong **một** giao dịch *(`now()` chung)*. Một đường ghi tương lai ghi `fls_journal` ngoài `_them`, hoặc hai bút toán cùng ô cùng actor trong một giao dịch, thì phép nối có thể khớp ≥2 dòng *(UAT nếu **bất kỳ** dòng nào UAT)*. Hôm nay sổ thật **4/4** khớp đúng 1.
5. **Số in cạnh `⚠ ACTOR MỚI` = "thao tác"** *(sự kiện + bút toán gõ thẳng)* — tôi định nghĩa để `AC-3` ra `1` thay vì `5`; `WO` chỉ viết *"`<n>` dòng"*. Có in thêm tổng dòng ở 3 bảng. Actor chỉ có ở `fls_journal` *(⛔ có đường ghi nào hôm nay)* sẽ in `· 0 dòng`.
6. **`T3` ⛔ soi `fls_chup` / `fls_khai_cot`** — kho có **5** chuỗi actor ⛔ thuộc sổ ở đó *(`tools/chup_sao_ke.py`, `máy · trích dòng 1 (QĐ-ITL-105)`, `claude@fls(…)` ×2, `khai-thu-tu@apero.vn`)* — `WO` để ngoài phạm vi; tôi ⛔ khai hai chuỗi *"có thể khai"* *(⛔ dạng `@`, bài quét ⛔ bắt)*.
7. **Câu cũ ⛔ cổng canh, thấy khi rà `--ghi`** *(⛔ sửa — ⛔ do số `--ghi` đổi; chủ `fls-ba`)*: `master:343` *"`lint-imports` **8** kept"* *(thật 9)*; `roadmap:45` *"`DEV-02` quy ước v1.0"* *(nay v1.2)* + *"9 module"*; `master` §8 dòng `03_Dev/` *"`02` v1.0"*.
8. `kiem_so_song` **0** lệch là ảnh lúc chạy *(~10:30 02/10)*: nhịp chụp ảnh mới ⇒ nhóm ảnh/PM đỏ lại *(loại ⓐ, `GAP-CONG-01`)* — ⛔ hồi quy.
