# WO-003 — Cú Ghép đi được trên màn thật: `reason` tuỳ ý · `hd`/`cdt1` thành MÁY GỢI Ý · màn ⛔ nói "đã sạch" lúc tải · ghi `run_pm`

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(`fls-ba` nghiệm thu PO 2026-10-01 tối — [`KQ-007`](KQ-007-kiem-bg-006.md) ĐẠT; mục **Nghiệm thu PO** cuối phiếu)* · ~~`CHO_TEST` — **VÒNG 2** *(`fls-dev` 2026-10-01 tối — [`BG-006`](BG-006-ban-giao-wo-003-vong-2.md), mã @ `5fbc29c`)*~~ · ~~`DANG_LAM` — **VÒNG 2** *(`fls-ba` mở lại 2026-10-01 tối theo [`KQ-005`](KQ-005-kiem-bg-004.md) TRƯỢT `AC-7` — `10 §2` bước ④: TRƯỢT mã ⇒ Dev mở lại **cùng** WO; việc ở mục **Vòng 2** cuối phiếu)*~~ · ~~`CHO_TEST` *(`fls-dev` 2026-10-01 — [`BG-004`](BG-004-ban-giao-wo-003.md), mã @ `48fb68f`)*~~ *(vòng 1: **11/12** AC đạt)* · ~~`DANG_LAM` *(`fls-dev` nhận 2026-10-01 tại `c1fb250`)*~~ · ~~`MO` · ⭐ **SẴN SÀNG cho Dev** *(⛔ câu treo chặn)*~~ *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-01 |
| **Nhận** | `fls-dev` |
| **Vòng** | `2` · vòng 1 phát 01/10 *(BG-004 · KQ-005 TRƯỢT)* · vòng 2 mở 01/10 tối |
| **Thứ tự với phiếu khác** | ⭐ Làm **TRƯỚC** `WO-001` — `F-1` là `CHAN`; ⭐ **vòng 2 vẫn trước `WO-001`** *(phiếu nhỏ, cùng tệp `ghi_tay.py`; `WO-001 T5` chụp số sau khi `KQ` vòng 2 ĐẠT)*; và `WO-001 T5` *(`dong_bo --ghi`)* phải chụp số **sau** khi phiếu này thêm bài thử *(`WO-001` Rủi ro 3)* |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(tác vụ ① mapping)* — cổng `B5` *(người thật bấm hàng chờ)* và `B4` *(bỏ ghép trên sổ thật)* **⛔ đạt được bằng cách nào** khi nút `Gán`/`Bỏ gán` trên máy thật trả **`400`** *(`KQ-002 F-1`)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: **"SHQ1 / SHQ2 → chuẩn hoá & mapping"** — kế toán ghép lệnh chi ↔ tiền **trên màn FLS** thay vì `VLOOKUP` tay trên Google Sheets. Hôm nay mắt xích ấy **⛔ xoá được**: màn có, cửa có, nhưng hai thứ **⛔ nói chuyện được với nhau**.

## Căn cứ
- **`QĐ-ITL-149`** — owner 01/10, nguyên văn:
  - Câu hỏi *(`WO-001 Q3`)*: *"Khi bấm Ghép, máy tự điền cdt1/hd. Hai ô này nên được ghi là người chốt hay máy gợi ý?"* ⇒ **"Máy gợi ý"**.
  - Câu hỏi *(`KQ-002 F-1`: màn ghép ⛔ có ô lý do, cửa đòi `reason`)* ⇒ **"bỏ yêu cầu lý do cho cú Ghép"**.
- `KQ-002` *(`fls-test`, 01/10)* — `F-1` `CHAN` · `F-3` `NANG` · `F-4` `NANG`; mỗi cái có bài nghiệm thu đỏ sẵn ở `tests/nghiem_thu/` *(`xfail(strict=True)`)*.
- `QĐ-ITL-143` *(máy ghép xong thì GỢI Ý, ⛔ QUYẾT — `may_ghep.ghi_goi_y_may`)*: đường ghép **tay** về cùng lằn.
- `QĐ-ITL-150 ⓐ`: dòng UAT 01/10 ⛔ tính người thật — phiếu này ⛔ chạm chúng.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/07_API_CONTRACT.md` | `§3` dòng `POST /queue/{itl_id}/match` · `§4h ⓻` *(+ đính chính)* · ⭐ `§4h ⓼` | **v3.4** |
| `02_BA/05_DATA_DICTIONARY_ERD.md` | ⭐ `DD-I15 ⓓd` · `DD-I15 ⓒ` *(`run_pm`)* | **v0.32** |
| `02_BA/10_DECISION_TABLE.md` | ⭐ `DT-I14` | **v0.6** |
| `02_BA/09_STATE_MACHINE_SPEC.md` | ⭐ `SM-I06` *(chuyển cấm `F-7`, `F-9`)* | **v0.5** |
| `02_BA/11_INVARIANTS.md` | `INV-I16` *(phạm vi lý do)* · `INV-I21` *(lằn máy gồm ghép tay)* | **v0.14** |
| `02_BA/08_NFR.md` | `NFR-I04` | **v1.2** |
| `02_BA/06_SCREEN_SPEC.md` | `C10` trạng thái khung *(«Hàng chờ đã sạch.» = **rỗng**, ⛔ tải)* | v4.7 |
| `01_Orchestrator/handoff/KQ-002-doi-chieu-hien-trang-01-10.md` | `F-1`, `F-3`, `F-4` + bảng *Bài thử mới* | — |

## Phạm vi

**Thứ tự làm bên trong phiếu** *(nhỏ → lớn; mỗi phần một commit được)*: **(a)** → **(d)** → **(b)** → **(c)**.

| TRONG | NGOÀI |
|---|---|
| **(a) `F-1` — `reason` TUỲ Ý cho `match` + `unmatch`** *(`BA-07 §4h ⓼`)*. ⓐ `fls/api/xu_ly.py:310` *(`ghep`)* và `:458` *(`bo_ghep`)*: ⛔ `_chu(yc.than, "reason")` — đọc tuỳ ý. ⓑ `fls/repo/ghi_tay.py`: khai **hai hằng** `LY_DO_MAC_DINH_GHEP = "(may dien) ghep tren man - nguoi bam khong ghi ly do"` · `LY_DO_MAC_DINH_BO_GHEP = "(may dien) bo ghep tren man - nguoi bam khong ghi ly do"`; `ghep_lenh` *(`:549`)* và `bo_moi_noi` *(`:776`)* thay `raise ThieuLyDo` bằng **điền hằng** khi `reason` rỗng/toàn khoảng trắng. ⭐ Điền ở **repo**, ⛔ ở cửa | ⛔ Cửa lô `match-lo` *(`xu_ly.py:392`)* — **giữ** `reason` bắt buộc. ⛔ `/adjust`, `reverse`, `reopen`, `defer` — giữ luật cũ. ⛔ `_them()` *(`:286`)* — giữ `ThieuLyDo` |
| **(d) `F-4` — ghi `run_pm`** khi ghép tay: `ghi_tay.py:676` `INSERT INTO fls_pm_link (…)` thêm cột `run_pm` = ảnh PM vừa dùng *(biến `run_pm`, `:587`)*. Cột `run_id` giữ nghĩa hiện có | ⛔ Vá ngược `run_pm` cho **2.262** mối nối cũ *(chú thích migration `0024`: NULL = sinh trước 18/09 — đúng nghĩa)* |
| **(b) Q3 — `hd`/`cdt1` suy lúc ghép = MÁY GỢI Ý** *(`BA-05 DD-I15 ⓓd`, `BA-10 DT-I14`)*. ⓐ `ghep_lenh` *(`:686`–`697`)*: bút toán suy ghi `nguon='may_goi_y'` + `value_source='may_goi_y'`, `actor` = **người bấm**, `evt_id` = sự kiện `match` của cú ghép; `value_before` = gợi ý đang hiệu lực *(`fls_may_goi_y`)* hay `NULL`; ⭐ người đã chốt ô ⇒ ⛔ ghi, khai `nguoi_da_chot` *(khoá mới trong kết quả)*; gợi ý trùng ⇒ ⛔ thêm dòng. Gợi ý: **dùng lại** phần ghi của `may_ghep.ghi_goi_y_may` *(tách hàm nhận `evt_id` + `actor`)* — ⛔ viết bản thứ hai của luật *"người đã chốt ⇒ im"*. ⓑ `bo_moi_noi` *(`:796`–`812`)*: tập *"còn hiệu lực"* = bút toán gắn sự kiện `match` của dòng **có trong `fls_may_goi_y` HOẶC `fls_sua_tay`**; bản đảo mang `nguon` **bằng** `nguon` của dòng bị đảo. ⓒ Áp cho **mọi** đường qua `ghep_lenh` *(cửa `match` + cửa lô)* | ⛔ Đổi `fls_sua_tay`/`fls_may_goi_y` *(migration `0025` đúng)*. ⛔ Sửa/xoá **4** dòng UAT `nguon='sua_tay'` *(`INV-I08`; biên bản)*. ⛔ Màn hiện gợi ý / nút gật *(`GAP-SCR-33` — chờ owner)*. ⛔ Đổi cửa `GET /ledger/{itl_id}/fields/{field}` *(`ghi_tay.py:254` đọc `*_thyt`)* — `GAP-SCR-33` |
| **(c) `F-3` — màn ghép ⛔ nói "Hàng chờ đã sạch" lúc đang tải**: `fls/web/tep/man_f01_ghep.js` — `mo_man()` *(`:685`)* và `doi_chip()` *(`:675`)* phải đặt `ST.dang_tai = true` **trước** lượt `ve()` đầu, để nhánh `Đang hỏi sổ…` *(`:1128`)* tới được; `?gia_lap=tai` phải hiện **tải**, ⛔ **rỗng** | ⛔ Đổi thiết kế 5 trạng thái *(`BA-06` v4.7 đã đủ)*; ⛔ chip `Tất cả` *(`GAP-SCR-26`)* |
| **Bài thử của Dev** *(`tests/**` trừ `nghiem_thu/`)*: sửa các bài **đang ghim luật cũ** — `tests/repo/test_ghep_lenh_pg.py:365` *(`ThieuLyDo` khi ghép thiếu lý do)* · `tests/repo/test_bo_moi_noi_pg.py:267` *(`test_KHONG_ly_do_thi_KHONG_bo`)* và `:190`–`:233` *(đảo qua `fls_sua_tay`)* · mọi bài khác `grep` ra theo `fls_sua_tay` + `ghep_lenh`. ⭐ Bài **mới** chứng minh ĐỎ trước *(`Đ5`)* cho từng AC dưới | ⛔ Sửa / gỡ `xfail` trong `tests/nghiem_thu/**` — việc của `fls-test` *(`10 §1`)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a)* | Hai bài `F-1` của `fls-test` **qua** khi tắt dấu `xfail` | `pytest tests/nghiem_thu/test_kq002_than_man_ghep_qua_cua_that.py --runxfail` ⇒ **3 passed** *(2 bài-đỏ + 1 đối chứng)*; chạy thường ⇒ 2 bài báo **`XPASS(strict)`** = FAILED — **đúng mong**, `BG` ghi rõ để `fls-test` gỡ dấu | Trả `xu_ly.py:310` về `_chu(yc.than, "reason")` ⇒ `--runxfail` **2 failed** |
| AC-2 *(a)* | Ghép + bỏ ghép **thiếu** `reason` trên kho TEST ⇒ `fls_queue_event.reason` của hai sự kiện **bắt đầu** `"(may dien) "`; `actor` = actor của thẻ *(⛔ `may@fls`)*; **0** dòng `reason` rỗng | bài repo mới: gọi `ghep_lenh(..., reason="")` rồi `bo_moi_noi(..., reason="   ")`, `SELECT reason, actor FROM fls_queue_event` | Bỏ phép điền mặc định ⇒ bài thấy `reason` rỗng ⇒ **ĐỎ**; điền mà đặt `actor='may@fls'` ⇒ **ĐỎ** |
| AC-3 *(a)* | `match-lo` thiếu `reason` ⇒ vẫn **`400`** | bài cửa mới trên `tests/api/test_cua_ghep_lo_pg.py` | Nới luật ở `xu_ly.py:392` ⇒ **ĐỎ** |
| AC-4 *(d)* | Bài `F-4` **qua** khi tắt `xfail`; mối nối tay mới có `run_pm` = ảnh PM đã dùng | `pytest tests/nghiem_thu/test_kq002_ghep_tay_ghi_run_pm.py --runxfail` ⇒ **passed**; chạy thường ⇒ `XPASS(strict)` | Bỏ cột `run_pm` khỏi `INSERT` ⇒ `--runxfail` **failed** |
| AC-5 *(b)* | Ghép tay một dòng *(N = 1, lệnh có `hd`+`cdt1`)* trên kho TEST ⇒ `fls_may_goi_y` **+2** ô · `fls_sua_tay` **+0** · `fls_adjustment.nguon` của 2 dòng = `'may_goi_y'` · `fls_journal.value_source` = `'may_goi_y'` · `actor` = người · Final *(`COALESCE(fls_sua_tay, fls_itl.<field>)`)* **⛔ đổi** | bài repo mới *(đếm trước/sau trên **cùng** `itl_id`, mẫu số ≠ 0 — `Đ3`)* | Trả `ghi_tay.py:695` về `value_source=NGUON_TAY` *(⛔ `nguon=`)* ⇒ `fls_sua_tay` +2 ⇒ **ĐỎ** |
| AC-6 *(b)* | Người **đã** chốt `hd` *(qua `/adjust`)* rồi mới ghép ⇒ ⛔ gợi ý `hd`; kết quả có `nguoi_da_chot: ["hd"]`; `cdt1` vẫn được gợi ý | bài repo mới | Bỏ phép kiểm `_hieu_luc` trước khi ghi ⇒ có gợi ý `hd` ⇒ **ĐỎ** |
| AC-7 *(b)* | Bỏ ghép ⇒ mọi gợi ý gắn sự kiện `match` của dòng **bị đảo** *(cả gợi ý ghép tay **lẫn** gợi ý máy ghép tự động)*; `fls_may_goi_y` của dòng về **0**; giá trị người **⛔ bị đảo**, có trong `bo_qua` | hai bài repo mới: ⓐ dòng ghép tay · ⓑ dòng có mối nối `hinh='A'` + gợi ý `may@fls` | Giữ phép lọc cũ `con_hieu_luc &= dang_dung` *(chỉ `fls_sua_tay`)* ⇒ ca ⓑ còn gợi ý mồ côi ⇒ **ĐỎ** |
| AC-8 *(b)* | Cổng `khop_owner C8` ⛔ lật khi chỉ có cú ghép | bài repo mới: ghép tay trên kho TEST ⇒ `select count(*) from fls_sua_tay` **không đổi** | như AC-5 |
| AC-9 *(c)* | Hai bài `F-3` **qua** khi tắt `xfail` | `pytest tests/nghiem_thu/test_kq002_man_ghep_dang_tai_khong_noi_da_sach.py --runxfail` ⇒ **passed** cả 2; chạy thường ⇒ `XPASS(strict)` | Gỡ dòng đặt `ST.dang_tai = true` trước `ve()` ⇒ `--runxfail` **failed** |
| AC-10 *(c)* | Máy chạy CHỈ ĐỌC *(8088)*: mở tab `man-ghep` — trong lúc cửa chưa trả **⛔** chữ *"Hàng chờ đã sạch"* / *"0 dòng"*; `?gia_lap=tai` hiện `Đang hỏi sổ…` **mãi** | `fls-test` chụp chữ màn ở 300/800/1.500 ms như `KQ-002` *(Chrome headless, 1440×900)* | — *(đo ở `KQ`)* |
| AC-11 | `pytest` toàn bộ: **chỉ** đỏ đúng **5** bài `XPASS(strict)` liệt kê ở AC-1/4/9 *(chờ `fls-test` gỡ dấu)*, ⛔ bài nào khác · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp *(cửa `match`/`unmatch` ⛔ đổi bảng chạm)* · `kiem_thuyet_minh` khớp | lệnh ở `CLAUDE.md` | — |
| AC-12 | `BG` ghi `kiem_so_song`: số nhóm đỏ **mới** do phiếu này *(loại c — số phép thử)* tách khỏi đỏ nền; ⛔ chạy `dong_bo --ghi` *(việc của `WO-001 T5`)* | đọc `BG` | — |

⛔ **Đính chính `AC-11`** *(`fls-ba` 01/10 tối — `KQ-005 F-4` `NHE`; chữ gốc ở trên giữ làm biên bản)*: câu trong ngoặc *"cửa `match`/`unmatch` ⛔ đổi bảng chạm"* **sai so với chính phạm vi `(b)`** — `(b) ⓐ` đọc `fls_may_goi_y` *(lấy `value_before`, kiểm `loc_goi_y`)* và `(b) ⓑ` đọc `fls_may_goi_y ∪ fls_sua_tay` ⇒ bảng **đọc** của `match`·`match-lo`·`unmatch` **phải** thêm `fls_may_goi_y`. Mã `48fb68f` làm đúng *(`fls/api/bang_tuyen.py` — `BG-004` mục 3)*, `soi_bang_tuyen` **40/40** khớp. Câu đúng: *"`soi_bang_tuyen` khớp SQL thật ở **mọi** tuyến — bảng chạm của `match`/`match-lo`/`unmatch` được phép thêm đúng những khung xem phạm vi `(b)` đọc"*. Lỗi **giấy**, ⛔ lỗi mã; ⛔ đổi phán quyết `AC-11` *(ĐẠT)*.

## Màn hình *(chạm UI — phần (c))*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` v4.7 `C10` · bản dựng `02_BA/Artifacts/` của `SCR-F01` *(⛔ đổi)*.

| Trạng thái | Hiện gì |
|---|---|
| tải | `Đang hỏi sổ…` *(banner `info`)* — ⛔ *"0 dòng"*, ⛔ *"Hàng chờ đã sạch"* |
| rỗng | *"0 dòng · Hàng chờ đã sạch."* — **chỉ** khi cửa đã trả và trả rỗng |
| lỗi | *"⛔ Cửa lỗi: Máy gặp lỗi bên trong."* *(như hiện tại — `KQ-002` đo ✅)* |
| mất kết nối | *"⛔ Cửa lỗi: Không nối được tới máy chủ FLS."* *(như hiện tại ✅)* |
| có dữ liệu | danh sách lệnh chi *(đo 01/10: **736** dòng sau ~4 s)*; bấm `Gán` / `Bỏ gán` ⛔ còn `400` |

## Dữ liệu
- Bảng/cột chạm: `fls_pm_link(run_pm)` · `fls_queue_event(reason, actor)` · `fls_adjustment(nguon, reversal_of, state)` · `fls_journal(value_source)` · khung xem `fls_may_goi_y`, `fls_sua_tay` *(đọc)*.
- **Ghi kho THẬT: `KHONG`.** Dev thử **chỉ trên kho TEST** *(`dsn_test()` — bản TRẮNG `NAP-2000-…`)*. Máy 8088 *(kho thật)* vẫn **CHỈ ĐỌC**; ⛔ bật `--cho-ghi` trên kho thật trong phiếu này.
- Số dòng kho thật **sẽ** bị luật mới chạm khi có người bấm thật *(đã đếm 01/10, chỉ để biết, ⛔ ghi)*: `fls_may_goi_y` **4.424** · `fls_sua_tay` **0** · mối nối hiệu lực **2.262** trên **2.222** dòng tiền *(hình `A` 2.145 · `B` 65 · `C` 52 · `T` 0)* · sự kiện `match`/`unmatch` mang `reason` rỗng **0/2.221**.

## Câu còn treo
- ⛔ **Không câu nào chặn phiếu này.**
- *(ngoài phạm vi, chờ owner)* `GAP-SCR-33` — khi nào mở lằn **GIÁ TRỊ** *(màn hiện gợi ý `hd`/`cdt1` + nút gật)*. Vì sao phiếu vẫn làm được: owner đã chốt **nơi ghi** *(máy gợi ý)*; câu treo chỉ là **màn nào đọc** chỗ ấy. Hệ quả cần nói với kế toán: sau phiếu này, ghép tay **⛔ điền** `hd`/`cdt1` vào Final — họ vẫn phải gõ qua ô sửa.

## Rủi ro
1. **Đổi hành vi thấy được:** trước phiếu này *(chỉ trên giấy — 0 kế toán đã bấm)* ghép tay điền Final `hd`/`cdt1`; sau phiếu, ô ấy **vẫn trống** cho tới khi người gõ. Đúng lời owner, nhưng ai đọc lướt sẽ tưởng *"ghép xong mà ⛔ điền"* là lỗi ⇒ `BG` và báo cáo nghiệm thu phải nói thẳng.
2. Bỏ ghép nay **đảo cả gợi ý máy** của dòng máy ghép *(trước đây bỏ mồ côi)* — đúng `DT-I14`, nó gặp `tools/goi_y_lai.py` *(chạy lại gợi ý cho mối nối cũ)*: công cụ ấy **đã** đọc khung xem `fls_moi_noi` *(`goi_y_lai.py:37`, `:51`)* nên dòng đã bỏ ghép ⛔ được gợi ý lại — Dev ghim điều ấy bằng **một** bài, ⛔ chỉ tin chú thích.
3. `XPASS(strict)` làm `pytest` **đỏ có chủ ý** 5 bài cho tới khi `fls-test` gỡ dấu — `BG` phải liệt kê đúng 5 tên, ⛔ "pytest đỏ vài bài".

---

## Vòng 2 — `KQ-005` `F-1` · `F-2` · `F-3`

> ⭐ **Một câu:** bỏ ghép phải rút **mọi** gợi ý máy của dòng — kể cả lớp bị gợi ý mới hơn đè — và hộp *"Đã bỏ ghép"* chỉ được nói *"người đã gõ tay"* khi **người** thật sự gõ. Hôm nay **0** dòng thật dính *(đo `KQ-005`)*; sẽ dính lần đầu `tools/goi_y_lai.py` chồng gợi ý lên một dòng rồi có người bỏ ghép.

**Vì sao mở lại cùng phiếu, ⛔ tách phiếu mới:** cả ba phát hiện nằm trong **chính** phạm vi `(b) ⓑ` của vòng 1 *(cùng hàm `fls/repo/ghi_tay.py::bo_moi_noi`, cùng `AC-7`)*; `10 §2` bước ④ khai *"TRƯỢT mã ⇒ Dev mở lại **cùng** WO"*. Vòng 2 chỉ **thêm** AC `AC-13`…`AC-18`; `AC-1`…`AC-12` đã phán ở `KQ-005` *(11/12 ĐẠT)* — ⛔ đo lại trừ khi vòng 2 làm chúng đổi *(`AC-7` được đo lại qua `AC-13`/`AC-14`)*.

### Căn cứ vòng 2
- [`KQ-005`](KQ-005-kiem-bg-004.md) *(`fls-test` 01/10)* — `F-1` `NANG` *(DEV + BA)* · `F-2` `NANG` *(DEV)* · `F-3` `NHE` *(BA)* · `F-4` `NHE` *(BA — đã đính chính `AC-11` ở trên)*. Ba bài đỏ sẵn `xfail(strict=True)` ở `tests/nghiem_thu/test_kq005_*`.
- Spec đã sửa *(`fls-ba` 01/10 tối, trong thẩm quyền spec — ⛔ câu owner)*: `BA-10` **v0.7** `DT-I14` *(nhánh 7 rút vế "bị đè"; nhánh 6/8 xét **mọi lớp**; định nghĩa `bo_qua`; nhánh `5a` ca trộn)* · `BA-11` **v0.15** `INV-I22` · `BA-09` **v0.6** `SM-I06` *(`F-10`, `F-11`)* · `BA-05` **v0.33** `DD-I15 ⓓd`. `BA-06` v4.7 `:1174` **đúng**, ⛔ đổi.

### Spec phải đọc *(vòng 2)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/10_DECISION_TABLE.md` | ⭐ `DT-I14` — bảng **Bỏ ghép** nhánh 6–8 · *Luật một câu* · ⭐ *Định nghĩa `bo_qua`* · nhánh `5a` | **v0.7** |
| `02_BA/11_INVARIANTS.md` | ⭐ `INV-I22` | **v0.15** |
| `02_BA/09_STATE_MACHINE_SPEC.md` | `SM-I06` chuyển `da_ghep_* → chua_ghep` · chuyển cấm `F-10`, `F-11` | **v0.6** |
| `02_BA/05_DATA_DICTIONARY_ERD.md` | `DD-I15 ⓓd` dòng *"Bỏ ghép thì gợi ý đi đâu"* + dòng *"Ca TRỘN"* | **v0.33** |
| `02_BA/06_SCREEN_SPEC.md` | `:1174` *(`bo_qua` = người đã gõ tay)* | v4.7 *(⛔ đổi)* |
| `01_Orchestrator/handoff/KQ-005-kiem-bg-004.md` | `F-1`, `F-2`, `F-3` + bảng *Bài thử mới* | — |

### Phạm vi vòng 2
| TRONG | NGOÀI |
|---|---|
| **(e) `F-1` — đảo MỌI LỚP.** `bo_moi_noi`: tập cần đảo = bút toán `fls_adjustment` của dòng gắn sự kiện `evt_type='match'` **và ⛔ có dòng nào `reversal_of` trỏ về nó** — ⛔ lọc qua khung xem `fls_may_goi_y`/`fls_sua_tay` *(chúng trả **lớp trên cùng**; `DT-I14` v0.7 *Luật một câu*)*. Áp cho **cả hai** `nguon` *(nhánh 6 `may_goi_y` · nhánh 8 `sua_tay` cũ)*; bản đảo mang `nguon` **bằng** dòng bị đảo *(như vòng 1)*. ⭐ Bút toán **đã có bản đảo** ⇒ ⛔ đảo lần hai *(nhánh 7)* | ⛔ Đổi khung xem `fls_may_goi_y`/`fls_sua_tay` *(migration `0025` đúng cho câu "ô đang là gì")*. ⛔ Đổi `tools/goi_y_lai.py` *(chồng lớp lên dòng **còn** mối nối là đúng — lớp trên thắng)*. ⛔ Vá sổ thật *(đo: **0** ca mồ côi / 4.424)* |
| **(f) `F-2` — `bo_qua` chỉ giá trị NGƯỜI** *(`DT-I14` v0.7 *Định nghĩa `bo_qua`*)*: mục = dòng `fls_sua_tay` của dòng tiền, bút toán ⛔ gắn `match`, trên ô mà dòng **từng** có bút toán gắn `match`; mỗi ô ≤ 1 mục; `nguon='sua_tay'`. ⛔ Bút toán máy — đã đảo lượt trước hay vừa đảo — **⛔ bao giờ** vào `bo_qua` | ⛔ Đổi câu màn `fls/web/tep/man_f01.js::_bao_bo_ghep` *(câu "người đã gõ tay" **đúng** khi `bo_qua` đúng nghĩa)* |
| **(g) `F-3` — ghim ca TRỘN** *(`DT-I14` nhánh `5a`)*: ⛔ đổi `may_ghep.suy_hd_cdt1` *(đã đúng — `:68`–`69`)*; chỉ thêm **bài ghim** | ⛔ Đổi luật `khong_suy_duoc` cho ca lệch thật *(nhánh 4 giữ)* |
| Bài thử của Dev *(`tests/**` trừ `nghiem_thu/`)* cho `AC-14`, `AC-16`; sửa bài **đang ghim luật cũ** nếu có *(vd. bài ghim chữ `vi_sao` "bị gợi ý mới hơn đè" trong `bo_qua`)* | ⛔ Sửa / gỡ `xfail` 3 bài `tests/nghiem_thu/test_kq005_*` — việc của `fls-test` |

### Tiêu chí nghiệm thu vòng 2
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-13 *(e)* | Hai bài `F-1` của `fls-test` **qua** khi tắt dấu `xfail`; đối chứng một lớp vẫn xanh | `pytest tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py --runxfail` ⇒ **3 passed**; chạy thường ⇒ **2** bài `XPASS(strict)` = FAILED — **đúng mong**, `BG` ghi đúng 2 tên | Trả phép chọn về khung xem *(`con_hieu_luc &= {adj_id ∈ fls_may_goi_y ∪ fls_sua_tay}`)* ⇒ `--runxfail` **2 failed** *("gợi ý lớp dưới NỔI LÊN LẠI")* |
| AC-14 *(e)* | Bài repo mới trên kho TEST, **ba lớp**: ghép tay *(gợi ý `hd=HD-A`, `cdt1=C-1`)* → `ghi_goi_y_may` chồng `hd=HD-B` → chồng `hd=HD-C` → bỏ ghép ⇒ ⓐ trước bỏ: bút toán gợi ý chưa đảo của dòng = **4** *(mẫu số ≠ 0, `Đ3`)*; ⓑ sau bỏ: = **0** *(`INV-I22 ⓐ`)* và `fls_may_goi_y` của dòng **{}**; ⓒ mỗi bút toán gợi ý có **đúng 1** bản đảo. ⭐ Thêm vòng **ghép → bỏ → ghép lại → bỏ**: ⓓ ⛔ bút toán nào có **≥ 2** bản đảo | bài repo mới *(đếm `fls_adjustment` gắn `match`, `nguon='may_goi_y'`, `NOT EXISTS` bản đảo — trên **cùng** `itl_id`)* | ⓑ đỏ nếu chọn theo khung xem · ⓓ đỏ nếu bỏ điều kiện *"chưa có bản đảo"* *(đảo hai lần)* |
| AC-15 *(f)* | Bài `F-2` của `fls-test` **qua** khi tắt `xfail`; đối chứng *(người gõ thật ⇒ `bo_qua` có `hd`)* vẫn xanh | `pytest tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py --runxfail` ⇒ **2 passed**; chạy thường ⇒ **1** bài `XPASS(strict)` | Dựng lại `bo_qua` từ *mọi bút toán `match` ngoài tập đảo* *(mã `48fb68f`)* ⇒ `--runxfail` **1 failed** *("bo_qua có 2 mục")* |
| AC-16 *(g)* | Bài repo mới: ghép N = 2 dòng lệnh — dòng X `hd` **rỗng**, dòng Y `hd='HD-Y'`, cả hai `cdt1='C-1'` ⇒ gợi ý `hd=HD-Y` + `cdt1=C-1`; `khong_suy_duoc` **⛔ chứa** `hd` | bài repo mới *(gọi `ghep_lenh` thật, đọc `fls_may_goi_y`)* | Bỏ `gt.discard("")` ở `may_ghep.suy_hd_cdt1` ⇒ `hd` vào `khong_suy_duoc` ⇒ **ĐỎ** |
| AC-17 | `pytest` toàn bộ: **chỉ** đỏ đúng **3** bài `XPASS(strict)` của `AC-13`/`AC-15` *(chờ `fls-test` gỡ dấu)*; bài `xfail` của `WO-001` *(`test_kq002_moc_b_khong_dem_may_la_nguoi.py`)* **vẫn** `xfail` · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp SQL thật ở mọi tuyến *(đổi cách đọc ở `unmatch` — vd. đọc thẳng `fls_adjustment` thay khung xem — thì sửa `bang_tuyen.py` cho khớp và `BG` ghi rõ bảng chạm cũ → mới)* · `kiem_thuyet_minh` **31/31** | lệnh ở `CLAUDE.md` | — |
| AC-18 | `BG` tách `kiem_so_song`: nền **83** nhóm *(`KQ-005`, 01/10 tối)* ⟷ đỏ **mới** do vòng 2 *(loại c — số phép thử)*; ⛔ chạy `dong_bo --ghi` | đọc `BG` | — |

### Dữ liệu vòng 2
- Bảng chạm: `fls_adjustment(reversal_of, nguon, state)` · `fls_journal` · `fls_queue_event` · khung xem `fls_sua_tay` *(đọc, cho `bo_qua`)*.
- **Ghi kho THẬT: `KHONG`.** Chỉ kho TEST *(`dsn_test()`)*.
- Số dòng kho thật luật mới **sẽ** chạm khi có người bỏ ghép *(đếm 01/10 tối, chỉ để biết)*: bút toán gợi ý chưa đảo **4.424** *(mọi lớp)* · ô ≥ 2 lớp **0** · gợi ý trên dòng 0 mối nối **0** · `sua_tay` gắn `match` chưa đảo **0**.

### Câu còn treo vòng 2
- ⛔ **Không câu nào chặn.** Nhánh `5a` *(ca trộn — rỗng = ⛔ lên tiếng)* là quyết định **BA trong thẩm quyền spec**: kết quả chỉ là gợi ý *(Final ⛔ đổi — `QĐ-ITL-149`)*, hôm nay **0/25** dòng chạm, mã đã vậy. Owner muốn ngược lại thì đổi một dòng + bài `AC-16` — ⛔ chặn phiếu.

### Rủi ro vòng 2
1. **Đảo hai lần:** phép chọn mới phải loại bút toán **đã có bản đảo** — bỏ điều kiện ấy thì vòng *ghép lại → bỏ* đảo lại bút toán vòng trước *(`AC-14 ⓓ` canh)*.
2. **Bản đảo của lớp dưới** mang `value_before` = giá trị **của chính lớp ấy** *(⛔ giá trị lớp trên)* — nhật ký phải đọc được *"rút HD-A"*, *"rút HD-B"*, *"rút HD-C"* riêng.
3. `XPASS(strict)` làm `pytest` đỏ **có chủ ý** 3 bài cho tới khi `fls-test` gỡ dấu — `BG` liệt kê đúng 3 tên.

## Nghiệm thu PO *(`fls-ba` · 2026-10-01 tối)*

✅ **ĐÓNG.** `KQ-007` ĐẠT trọn *(`AC-13`…`AC-18` 6/6; `AC-1`…`AC-12` ⛔ hồi quy — `pytest` **`1948 passed, 1 xfailed`**; sổ thật 8/8 bảng **⛔ đổi**)*. Đối chiếu lại từng AC với **ý owner**, ⛔ chỉ với chữ AC:

| Ý owner *(nguyên văn)* | AC chứng nó | Kết luận PO |
|---|---|---|
| `QĐ-ITL-149 ⓐ` — hai ô `hd`/`cdt1` khi ghép là **"Máy gợi ý"** | `AC-5` *(gợi ý vào `fls_may_goi_y`, Final ⛔ đổi)* · `AC-6` *(người đã chốt ⇒ máy im)* · `AC-8` *(`C8` ⛔ lật)* — `KQ-005` · ⭐ `AC-14` *(bỏ ghép rút **mọi lớp** gợi ý — gợi ý ⛔ sống lâu hơn căn cứ của nó)* · `AC-16` *(ca trộn — chỉ là gợi ý)* | ✅ đúng ý: ghép ⛔ còn **nhân danh người** chốt ô nào |
| `QĐ-ITL-149 ⓑ` — **"bỏ yêu cầu lý do cho cú Ghép"** | `AC-1` · `AC-2` *(máy điền `(may dien) …`, `actor` = người bấm)* · `AC-3` *(cửa lô vẫn đòi — ngoài lời owner, giữ luật cũ)* | ✅ đúng ý; vết vẫn đủ *(⛔ dòng `reason` rỗng)* |
| `QĐ-ITL-150 ⓐ` — cú UAT **⛔ tính người thật** | phiếu ⛔ chạm 4 dòng UAT *(`INV-I08`)*; `KQ-007` đo sổ thật 8/8 bảng khớp | ✅ — bộ đếm mốc `B` là việc của `WO-001 T1b` |
| `QĐ-ITL-27` — kiểm soát nằm trong máy, ⛔ bịa về việc người làm | `AC-15` *(`bo_qua` chỉ giá trị **người** ⇒ hộp "người đã gõ tay" ⛔ nói sai)* | ✅ |
| `KQ-002` `F-3`/`F-4` *(màn nói "đã sạch" lúc tải · thiếu `run_pm`)* | `AC-9` · `AC-10` *(5 trạng thái 8088)* · `AC-4` | ✅ |

**Còn lại, ⛔ chặn đóng:** `KQ-007 F-4` *(giấy)* — đã sửa: `BA-10` **v0.8** *(`AC-15` ⇒ `AC-16`)* · `BA-09` **v0.7** *(`F-10`/`F-11` ✅ đã chặn)*. `F-1`/`F-2`/`F-3` *(chữ trên màn sau bỏ ghép)* — spec `BA-06` **v4.8** + `BA-10` v0.8, mã ⇒ [`WO-008`](WO-008-chu-man-sau-bo-ghep.md) *(ưu tiên thấp, sau `WO-001`)*.

**Nói thẳng với kế toán *(Rủi ro 1)*:** ghép xong, hai ô `hd`/`cdt1` **⛔ tự điền** vào Final — máy chỉ ghi **gợi ý**; người vẫn gõ qua ô sửa. Đây là đúng lời owner, ⛔ lỗi. Sổ thật hôm nay **0** cú ghép của người ⇒ luật mới chạm người thật lần đầu ở cú bấm thật đầu tiên.

## Changelog
- 2026-10-01 tối · `fls-ba` · ✅ **nghiệm thu PO — `DONG`** theo `KQ-007` ĐẠT *(mục **Nghiệm thu PO**)*; `KQ-007 F-4` sửa giấy *(`BA-10` v0.8, `BA-09` v0.7)*; `F-1`…`F-3` ⇒ `BA-06` v4.8 + `WO-008`.
- 2026-10-01 tối · `fls-dev` · vòng 2 xong → `CHO_TEST`; bàn giao `BG-006` *(mã `5fbc29c`: `bo_moi_noi` đảo mọi lớp theo bảng gốc + `reversal_of`; `bo_qua` chỉ giá trị người; ghim ca trộn)*.
- 2026-10-01 tối · `fls-ba` · ⭐ **mở lại — VÒNG 2** theo `KQ-005` *(TRƯỢT `AC-7`)*: thêm mục **Vòng 2** *(`AC-13`…`AC-18` cho `F-1`/`F-2`/`F-3`)*; spec `BA-10` v0.7 · `BA-11` v0.15 · `BA-09` v0.6 · `BA-05` v0.33; đính chính câu ngoặc `AC-11` *(`F-4`)*. Trạng thái `CHO_TEST` → `DANG_LAM`.
- 2026-10-01 · `fls-dev` · nhận → `DANG_LAM` → `CHO_TEST`; bàn giao `BG-004` *(mã `48fb68f`)*.
- 2026-10-01 · `fls-ba` · phát `WO-003` *(từ `KQ-002` `F-1`/`F-3`/`F-4` + `QĐ-ITL-149`)*.
