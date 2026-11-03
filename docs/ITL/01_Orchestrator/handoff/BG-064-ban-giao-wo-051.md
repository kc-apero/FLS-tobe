# BG-064 — bàn giao `WO-051` *(vòng 1)* — trang hàng chờ `VND` ~100 s ⇒ ~0,1 s · `F01` `Xem thêm` khung chờ + lỗi ⛔ xoá lưới · bài chập chờn `KQ-061`

| | |
|---|---|
| **Thuộc** | `WO-051` |
| **Phát bởi** | `fls-dev` · 2026-10-06 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `c0c9963` *(đã đẩy; tờ này điền số `pytest` cuối ở commit kế tiếp — chỉ giấy)* — mã: `9467744` *(b)* · `57563d7` *(c)* · `75a8c57` *(AC-10 + `HOI-063`)* |
| **Spec đã đọc** | `BA-08` **v1.4** `NFR-I30` · `BA-06` **v4.24** `§4.5 ⓦ` ⑦ *(phiếu ghi v4.22; ⑦ ⛔ đổi từ v4.22 — đọc lại `06_SCREEN_SPEC.md:814-825`)* · `BA-07` `GET /queue` *(⛔ đổi)* · `KQ-050 F-1` · `KQ-061` ghi chú phương pháp |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/doc_bao_cao.py` | `_SQL_HANG_CHO`: `st AS MATERIALIZED` *(view `fls_queue_state` gom **đúng một lần** mỗi câu)* + `trang AS MATERIALIZED` *(lọc + xếp + `LIMIT` trên `x` trước)* rồi `trang ⟕ st`. `_CTE_HANG_CHO` ⛔ đổi *(`do_phu_hang_cho` cùng số)*; khuôn con trỏ / hợp đồng cửa ⛔ đổi. Chú thích tại chỗ: số đo trước/sau, vì sao ⛔ `LATERAL`, bẫy `OFFSET 0`, bẫy đo `prepare` |
| `fls/web/tep/man_f01.js` | `_xem_them`: nút khoá + chữ `Đang tải thêm…`; lỗi ⇒ `_loi_xem_them` — hàng **giữ**, nút nhường chỗ cho `⛔ Cửa lỗi: <e.cau>` *(`banner crit`, `textContent`)* + **một** nút `Thử lại` *(`b tiny`)* gọi lại `_xem_them` với **cùng** `ST.con_tro`. ⛔ token / lớp CSS mới; ⛔ đổi `ve_luoi` / luật lượt `WO-045` |
| `tools/do_trang_hang_cho.py` *(mới)* | đo đồng hồ **mọi** trang `/queue` *(mỗi tiền tệ + `curr=None`)* và `/lenh-cho`, **kết nối mới mỗi trang** *(như cửa)*; mẫu số `dem_hang_cho`; `itl_id` ⛔ trùng; `(curr, hang)` tăng nghiêm; **oracle** = câu `_SQL_HANG_CHO` của mã khi nhận **chép nguyên văn**, ⛔ con trỏ; `--explain CURR:HANG` ⇒ `EXPLAIN (ANALYZE, BUFFERS)` **đúng câu** hàm thật gửi *(`bat_cau`)*. Chỉ đọc *(`noi_chi_doc`)*; mã thoát `1` khi ⛔ đo được |
| `tests/repo/test_wo051_trang_hang_cho_so_that_pg.py` *(mới, 3 bài)* | `AC-5` sổ thật chỉ đọc, `statement_timeout = 2s`, kết nối mới: trang 2 tiền tệ **nhiều dòng nhất** *(tra lúc chạy)* · trang 2 **mọi** tiền tệ có trang 2 · ⭐ cổng **hình dạng**: mọi `GroupAggregate` `loops=1` *(bắt vùng mù của đồng hồ — bản `LATERAL` bị kéo phẳng chạy 1,05–1,31 s vẫn **dưới** 2 s)* |
| `tests/repo/test_wo051_phan_trang_khong_doi_pg.py` *(mới, 13 bài)* | `AC-4` kho TEST: 3 tiền tệ *(37 · 12 · 1 dòng)*, 9 dòng cùng tiền, lý do ×2, hoãn ×2, một dòng đã xong; lật hết với `limit` **1 · 7 · 50** × 4 phạm vi tiền tệ, so **từng hàng mọi cột** + `next_cursor` với oracle; trần số trang *(con trỏ ⛔ tiến ⇒ ĐỎ, ⛔ treo)* |
| `tests/web/test_wo051_xem_them_khung_cho.py` *(mới, 5 bài)* | `AC-6` · `AC-7` DOM giả, thân **cửa HTTP thật** kho TEST *(lần nạp riêng **120** dòng `VND` = ba trang ⇒ thấy nút **về** `Xem thêm`)*, cửa giả **giữ** / **ném** lượt `cursor=` |
| `tests/web/ca_wo032.py` | `goi_ca(may, ca, duong)` — `goi_ok` kèm `?run_id=<ca.run>` *(`AC-10` gốc `M2`)* |
| `tests/api/test_wo032_v2_bac_da_gan_pg.py` · `test_wo037_ro_may_theo_cua_ghi_pg.py` · `test_wo037_v2_ro_nguoi_hai_cau_pg.py` | `AC-10` `M2`: mọi cửa kho TEST hỏi với phạm vi **của ca** *(`goi_ca`)*; `AC14` phía mong đếm **cùng** phạm vi *(`run_id = ca.run`)*. **Lo gốc giữ** từng bài *(bậc `ma`, rổ theo cửa ghi, câu `vi_sao`, dòng `' vnd '` vào bậc `tien`)* — chỉ bỏ tiền đề ngầm *"ảnh mới nhất của cả kho TEST là ảnh của ca"* |
| `tests/repo/test_anh_pm_pg.py` | `AC-10` `M1`: mã dòng lệnh **ngẫu nhiên** *(`_ma`)* thay `PMA-1`/`PMB-1`/`PMC-CU`/`PMC-KHAC`/`PMD-NGOAI`; tiền đề `_anh_cua_ca_hieu_luc` *(ảnh lạ mới hơn ⇒ ĐỎ **có câu nói gốc**, ⛔ đỏ mù)*. Lo gốc từng bài ⛔ đổi |
| `docs/ITL/01_Orchestrator/handoff/HOI-063-…` *(mới)* | `LECH_DU_LIEU` · `KHONG_CHAN` — `reason` của view `fls_queue_state` ⛔ xác định *(8.256 / 8.387 dòng)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `04_DB_IMPLEMENTATION.md` **v1.18** | dòng changelog · §8 thêm `HOI-063` |
| `WO-051` · `handoff/README.md` · dashboard §5 | trạng thái `CHO_TEST` + nhật ký |

## Cổng *(kết quả nguyên văn — `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` **cổng vào** ×2 *(một mình, `9af99c4`)* | lượt 1 `2407 passed, 2 xfailed in 458.17s (0:07:38)` · lượt 2 `2407 passed, 2 xfailed in 454.57s (0:07:34)` *(⚠ lượt 2 chạy song song với phép đo **sổ thật** chỉ đọc của tôi — `fls`, ⛔ `fls_test`)* |
| `python -m pytest` **cuối phiếu** ×2 *(một mình)* | lượt 1 `2428 passed, 2 xfailed in 463.29s (0:07:43)` · lượt 2 `2428 passed, 2 xfailed in 460.19s (0:07:40)` *(@ `c0c9963`, kho TEST dựng lại đầu mỗi lượt; **0** failed; `2428 = 2407 + 21` bài mới — 3 `AC-5` + 13 `AC-4` + 5 web; `2` xfailed = như nền)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 79 lech/khong-do-duoc`. **Nền đầu phiếu đo cùng giờ** *(worktree `9af99c4`, cùng sổ thật)*: `⛔ … — 79 lech/khong-do-duoc` ⇒ **tập dòng lệch y hệt** *(`diff` theo khoá: **0** dòng thêm/bớt)*; chỉ **giá trị máy** của các dòng vốn đã lệch đổi theo phiếu *(số bài `2409→2430` · dòng `tests` `27.056→27.187` · `fls/web` `9.990→10.045` · `repo` `7.476→7.552` · commit · ngày · số tệp master `152→153`)* ⇒ **0** đỏ loại (c) mới. *(KQ-050 ghi nền **55**; +24 từ đó tới nay là số trôi theo sổ thật — ảnh chụp PM `NAP-2026-10-06-PMDC0F84D8` 10:24 — và theo phiếu của người khác, ⛔ của phiếu này.)* ⛔ `dong_bo --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (154 file, 1616 bang, 710 o ngay, 104 ma QD), khong chi 'khong thay loi'` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech   (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến mới; tập bảng `/queue` ⛔ đổi)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — phiếu ⛔ chạm schema *(`git diff 9af99c4 -- fls/db` rỗng)*; chạy là áp di trú lên kho THẬT |

## AC-1 — `EXPLAIN (ANALYZE, BUFFERS)` trang 2 `VND` *(sổ thật chỉ đọc — `noi_chi_doc`, `transaction_read_only = on`, `statement_timeout` của phiên 240 s; câu bắt từ **hàm thật**)*

**Mã khi nhận `9af99c4`** *(hàm thật `doc_hang_cho(curr='VND', con_tro='VND:50')` **89,15 s** · lượt sau **97,98 s**; `EXPLAIN ANALYZE` **111,9 s**)* — rút các nút *(bản trọn trong scratchpad phiên)*:
```
Limit  (cost=19758.90..19758.90 rows=2 width=207) (actual time=111911.443..111911.484 rows=51 loops=1)
  Buffers: shared hit=182573086
  ->  Sort ... Sort Key: x.hang
        ->  Nested Loop Left Join  (cost=950.99..19758.89 rows=2 width=207) (actual time=28.288..111905.061 rows=4192 loops=1)
              Join Filter: (fls_queue_event.itl_id = x.itl_id)
              Rows Removed by Join Filter: 10087864
              ->  Subquery Scan on x  (cost=948.87..1266.95 rows=1 width=167) (actual time=17.859..39.511 rows=4192 loops=1)
                    Filter: (ROW(x.curr, x.hang) > ROW('VND'::text, '50'::smallint))
                    Rows Removed by Filter: 50
              ->  GroupAggregate  (cost=2.12..18310.07 rows=8083 width=48) (actual time=0.031..26.549 rows=2407 loops=4192)
                    Group Key: fls_queue_event.itl_id
                    Buffers: shared hit=182572610
                    ->  Incremental Sort ... (actual time=0.026..18.960 rows=43471 loops=4192)
                          ->  Index Scan using fls_queue_event_itl_idx on fls_queue_event ... (actual time=0.004..10.125 rows=43499 loops=4192)
Execution Time: 111911.657 ms
```
⇒ **CHỨNG** giả thuyết `fls-ba` bằng chính `loops`: ước **`rows=1`**, thật **4.192**; nút ăn giờ = `GroupAggregate` *(view `fls_queue_state`)* **`loops=4192`** × **26,5 ms** ≈ 111 s. Đối chứng `USD:50`: ước `rows=2013` ⇒ `Hash Right Join`, `GroupAggregate` **`loops=1`** *(73 ms)*, cả câu **0,105 s**. ⭐ Thêm một điều giả thuyết chưa nói: `curr=None` gãy ở trang **84** *(con trỏ `VND:5` — mép `USD`→`VND`)*.

**Sau sửa** *(hàm thật **0,079 s**; `EXPLAIN ANALYZE` 85,65 ms)*:
```
Sort  (cost=19770.50..19770.60 rows=40 width=252) (actual time=85.474..85.482 rows=51 loops=1)
  CTE st
    ->  GroupAggregate  (cost=2.12..18310.07 rows=8083 width=48) (actual time=0.068..61.632 rows=8387 loops=1)
          ->  Incremental Sort ... -> Index Scan using fls_queue_event_itl_idx ... (rows=110349 loops=1)
  CTE trang
    ->  Limit  (cost=1266.96..1266.96 rows=1 width=167) (actual time=21.277..21.285 rows=51 loops=1)
          ->  Sort ... ->  Subquery Scan on x  (cost=948.87..1266.95 rows=1 width=167) (actual time=18.455..20.683 rows=4192 loops=1)
                      Filter: (ROW(x.curr, x.hang) > ROW('VND'::text, '50'::smallint))
  ->  Hash Right Join  (cost=0.03..192.40 rows=40 width=252) (actual time=31.707..85.444 rows=51 loops=1)
        Hash Cond: (s.itl_id = t.itl_id)
        ->  CTE Scan on st s  (... rows=8387 loops=1)
        ->  Hash -> CTE Scan on trang t  (... rows=51 loops=1)
Execution Time: 85.650 ms
```
⇒ bộ lập kế hoạch **vẫn** ước `rows=1` *(chỗ ấy ⛔ sửa được — ⛔ `ANALYZE`, ⛔ chỉ mục)*, nhưng nay ước sai ⛔ còn giá: view nằm trong CTE vật chất hoá ⇒ **`loops=1`** là lời hứa của ngữ nghĩa, ⛔ của bộ ước lượng *(`WO-051` Rủi ro 3)*.

## Bằng chứng từng AC
| AC | Bằng chứng | Chiều ĐỎ *(đã chạy)* |
|---|---|---|
| **AC-1** | mục trên | — |
| **AC-2** | `tools/do_trang_hang_cho.py --het-gio 10s` *(sổ thật chỉ đọc, kết nối mới mỗi trang, hàm thật `limit=50`)*. **Sau** *(@ `9467744`)*: <br>`c · trang · hàng · dem · max s · trang chậm · oracle`<br>`HKD 1 · 20 · 20 · 0.064 · 1 · 0/20`<br>`SGD 3 · 145 · 145 · 0.069 · 2 · 0/145`<br>`USD 80 · 3980 · 3980 · 0.088 · 51 · 0/3980`<br>`VND 85 · 4242 · 4242 · 0.101 · 64 · 0/4242`<br>`None 168 · 8387 · 8387 · 0.109 · 165 · 0/8387`<br>`Σ bốn tiền tệ lật được: 8387 / dem 8387` · `itl_id` ⛔ trùng · `(curr, hang)` tăng nghiêm · `✅ XANH` *(mã thoát 0)*. Mẫu số cùng lượt `dem_hang_cho`: `VND 4242 · USD 3980 · SGD 145 · HKD 20` *(≠ 0 — `Đ3`)* | **Mã khi nhận**, cùng công cụ: `HKD 0.083` · `SGD 0.075` · `USD 0.161` *(80 trang)* · **`VND` 2 trang, 50 hàng — `⛔ HUY trang 2 (VND:50): QueryCanceled` · `⛔ trang 2 10.00 s > 2.0`** · **`None` 84 trang, 4150 hàng — `⛔ HUY trang 84 (VND:5)`** ⇒ `⛔ ĐỎ — 8 điều`, mã thoát 1 |
| **AC-3** | `/lenh-cho` cùng công cụ *(⛔ lọc + từng tiền tệ, lật hết)* — **⛔ sửa**: sau `20 1 trang 0.564` · `EUR 0.546` · `HKD 0.546` · `SGD 2 trang 0.556` · `USD 17 trang / 818 hàng 0.591` · `VND 15 / 744 0.608` · `None 33 / 1626 0.620` *(trước, cùng ngày: max **0,78–0,84 s**)* ⇒ mọi trang ≤ 2 s, xanh ⛔ sửa | — *(đo)* |
| **AC-4** | ⓐ sổ thật: oracle lệch **0 / 8.387** *(bảng AC-2, cột oracle — so **mọi cột** của hàng, kể cả `reason` · `defer_until` · `defer_count` · `luy_ke_pct` · `hang`)*; `do_phu_hang_cho(90)` trước = sau `{'VND': (4242, 495, 90.01), 'USD': (3980, 406, 90.04), 'SGD': (145, 13, 91.03), 'HKD': (20, 2, 99.91)}` **4/4**. ⓑ kho TEST `tests/repo/test_wo051_phan_trang_khong_doi_pg.py` **13 passed**. ⓒ bài cửa `GET /queue` hiện có xanh ⛔ sửa `assert` *(`tests/web/test_wo045_…` 24 + `tests/repo/test_doc_bao_cao_pg.py` trong `pytest`)* | phá mã mới, chạy lại bài *(trả nguyên mỗi lần — so byte)*: `ORDER BY … DESC` trong `trang` ⇒ `6 failed, 7 passed` · con trỏ `>=` ⇒ `6 failed` *(trần trang bắt, ⛔ treo)* · `JOIN` thường thay `LEFT` ⇒ `12 failed, 1 passed`. ⚠ bỏ hẳn `ORDER BY` trong `trang` ⇒ **xanh** *(13 passed — xem "còn yếu" 3)* |
| **AC-5** | `tests/repo/test_wo051_trang_hang_cho_so_that_pg.py` **3 passed** *(`-s`: `VND (4242 dòng) trang 2 cursor=VND:50: 0.072 s, 50 hàng` · `USD 0.074 s` · `SGD 0.065 s` · `GroupAggregate … loops=1`)* | **mã khi nhận**: `3 failed in 6.62s` — hai bài `psycopg.errors.QueryCanceled: canceling statement due to statement timeout`, bài hình dạng cũng đỏ. Bản `LATERAL` ⛔ `OFFSET 0`: `1 failed, 2 passed` *(chỉ cổng hình dạng bắt — đồng hồ xanh ở 1,05 s)* · bỏ `MATERIALIZED` của `st`: `1 failed, 2 passed` |
| **AC-6** | `test_AC6_XEM_THEM_dang_tai_nut_KHOA_chu_DANG_TAI_THEM_hang_GIU` xanh: bấm ⇒ `('Đang tải thêm…', True)`, lưới **50**, bấm thêm ×2 ⇒ `cursor` **1** `GET`; thả ⇒ **100** hàng, nút `[['Xem thêm', False]]`, `ST.con_tro` = `next_cursor` trang 2 | **mã khi nhận**: `AssertionError: ('Xem thêm', True)` *(chữ ⛔ đổi)*. Phá: bỏ `b.disabled = true` ⇒ `('Đang tải thêm…', False)` đỏ |
| **AC-7** | hai ca `FLS-INTERNAL` / `FLS-MAT-KET-NOI` xanh: lưới **50**, `[['banner crit', '⛔ Cửa lỗi: Máy gặp lỗi bên trong.']]` / `…Không nối được tới máy chủ FLS.`, nút `['b tiny']` **một**; bấm `Thử lại` ×2 ⇒ **một** `GET` `/queue?curr=VND&cursor=VND%3A50&limit=50` *(đúng con trỏ vừa lỗi)*; khi chờ lưới 50, ⛔ câu lỗi, nút `Đang tải thêm…` khoá; xanh ⇒ 100 hàng, câu lỗi mất, nút `Xem thêm`. Thêm: `Thử lại` lại lỗi ⇒ **một** dòng lỗi + **một** nút *(⛔ chồng)*, lật tiếp tới **120** + chip `hết danh sách`; lượt `Xem thêm` **cũ** lỗi sau `ve()` ⛔ hiện *(luật lượt `WO-045` giữ)*. **Chrome 8097 sổ thật chỉ đọc**, CDP `Fetch` giữ rồi `failRequest(ConnectionFailed)` lượt `cursor=`: khi giữ `{n: 50, nut: [["Đang tải thêm…", true, "b tiny"]]}`, bấm thêm ⇒ vẫn **1** lượt bị giữ; lỗi ⇒ `{n: 50, loi: [["banner crit","⛔ Cửa lỗi: Không nối được tới máy chủ FLS."]], nut: [["Thử lại", false, "b tiny"]]}`; `Thử lại` ×2 ⇒ **1** lượt, URL **=** URL lượt lỗi; thả ⇒ `n: 100`, ⛔ lỗi, nút `Xem thêm` | **mã khi nhận**: 3 bài `AssertionError: ⛔ lỗi xoá lưới: còn 0 hàng` *(`TT.loi` thay cả khung)*. Phá: `Thử lại` ⇒ `ve_luoi(o)` *(lật từ đầu)* ⇒ `⛔ Thử lại ⛔ mở lượt cursor= (lật từ đầu?)`; `_loi_xem_them` ⇒ `TT.loi` ⇒ `còn 0 hàng` |
| **AC-8** | **Chrome 154 headless 1440×900, chuột thật** *(`Input.dispatchMouseEvent` vào tâm `getBoundingClientRect` sau `scrollIntoView`)*, **8097 sổ thật CHỈ ĐỌC** *(⛔ `--cho-ghi`; 8088 ⛔ đụng)*: tab `Hàng chờ · F01` ▸ `Theo dòng tiền` ▸ nút thẻ `VND` *(thẻ in `VND4.242dòng chờ`)* ▸ `Xem thêm` **84** lần tới hết. Mỗi cú: chữ ngay sau cú bấm `["Đang tải thêm…", true]` *(84/84)*; đồng hồ trong trang `mousedown` → `MutationObserver` thấy số hàng tăng: **min 90 ms · max 265 ms** *(trang 82 — lưới vẽ lại 4.100 hàng)*. Cuối: DOM **4.242** hàng, `itl_id` khác nhau **4.242**, chip `hết danh sách`, `Đang xem 4242 dòng VND` = thẻ = `dem_hang_cho` cùng lượt *(`VND 4242`)*; `GET /queue?` **85**; **0** `POST`; console: **1** dòng `404 favicon.ico` *(trình duyệt tự xin)*, **0** lỗi khác | — |
| **AC-9** | bảng Cổng | — |
| **AC-10** | ⓐ cổng vào ×2 + cuối ×2 *(bảng Cổng)*. ⓑ **Hai gốc, cả hai chứng có kiểm soát** — xem mục dưới | xem dưới |

## AC-10 — bài chập chờn `KQ-061` *(9 đỏ / 4 tệp ở lượt 4; xanh khi chạy riêng)*
Cơ chế chung: **ảnh PM hiệu lực** = ảnh `max(read_at)` của **phạm vi** *(`fls/repo/anh_pm.py:65-72`)*; mọi bài dưới gọi với phạm vi `chi_nap_that` = **mọi** lần nạp của kho TEST.

| Gốc | Bài dính | Tái hiện có kiểm soát *(06/10)* | Sửa | Cùng trạng thái kho, bản mới |
|---|---|---|---|---|
| **`M2`** — bài **cửa** dựng ca trong fixture `module`, rồi hỏi cửa ⛔ `run_id` ⇒ ảnh của ca chỉ "hiệu lực" khi **⛔ ai** nạp ảnh mới hơn sau đó. Một tiến trình khác ghi `fls_test` giữa lượt *(máy 8099 / kịch bản Chrome dựng ca — đúng điều `KQ-061` nghi)* là đủ | `test_wo032_v2` ×2 · `test_wo037_ro_may` ×4 *(+2 ở tái hiện)* · `test_wo037_v2` ×1 *(+1)* | kho TEST dựng mới *(`pytest` một bài ⛔ `FLS_GIU_KHO`)* → chèn **một** ảnh PM `NAP-2000-01-01-LA4C5A52` `read_at = now()+1h` *(scratchpad `anh_la.py`, kho TEST)* → chạy 4 tệp mã cũ `FLS_GIU_KHO=1`: **`13 failed, 23 passed`** — lý do nguyên văn: `⛔ không đo được: cửa ⛔ trả lệnh PB81CBA1-1 (0 hàng)` · `'pm_line_id=…' ⛔ khong co trong anh chup hieu luc` · `DongLenhLa: … ⛔ khong co trong anh chup cua lan nap 'NAP-2000-01-01-LA…'` *(chứa cả **7** bài cửa của `KQ-061`)*. Thử thêm ảnh lạ **tự nhiên** *(`read_at = now()`, chèn **6 s** sau khi 4 tệp bắt đầu)*: `2 failed, 34 passed` — hai bài `test_anh_pm_pg` *(gốc `M1` — kho đang giữ)*, **0** bài cửa *(chúng đã chạy xong trước mốc 6 s)* ⇒ ⛔ chứng được hình "theo giờ" bằng ảnh tự nhiên | `tests/web/ca_wo032.goi_ca` — hỏi cửa thật với `?run_id=<ca.run>` *(khuôn `WO-023 (j)`)*; `AC14` phía mong đếm cùng phạm vi | **cùng** kho có ảnh `+1h`: 3 tệp cửa **xanh hết** *(`3 failed, 33 passed` — 3 đỏ còn lại là `test_anh_pm_pg`, dưới)* |
| **`M1`** — `test_anh_pm_pg` dùng mã lệnh **cố định** *(`PMB-1`, `PMC-CU`, …)*; kho TEST **giữ** giữa hai lượt *(`FLS_GIU_KHO=1` — `KQ-061` ghi Test đặt nó cho mọi lượt riêng)* ⇒ lượt sau gặp mối nối/dòng lệnh **cùng mã** của lượt trước | `test_anh_pm_pg` ×2 *(`test_BA_NOI…` · `test_anh_CU…` — **đúng** hai bài của `KQ-061`)* | ⓐ `pytest` **toàn bộ** hai lượt liền: lượt A kho mới `2428 passed, 2 xfailed in 462.78s` → lượt B `FLS_GIU_KHO=1` **`2 failed, 2426 passed, 2 xfailed in 469.47s`** = **đúng** `test_BA_NOI_deu_nhin_CUNG_mot_anh` + `test_anh_CU_KHONG_con_lam_ung_vien` *(`assert {} == {64: ['PMB-1']}` · `assert 3 == 1`)*. ⓑ thu nhỏ: mã cũ kho mới `6 passed` → giữ kho `2 failed, 4 passed` | mã ngẫu nhiên `_ma()`; tiền đề `_anh_cua_ca_hieu_luc` | **cùng** kho giữ: `6 passed`; giữ thêm lần nữa: `6 passed` |

⚠ `test_anh_pm_pg` *(3 bài)* hỏi **đúng** câu *"ảnh hiệu lực của cả phạm vi"* *(dòng tiền lần nạp cũ thấy lệnh lần nạp mới — **hai** lần nạp, `PhamVi` ⛔ có kiểu "tập lần nạp")* ⇒ ⛔ thu phạm vi về một ca được. Dưới ảnh lạ `+1h` chúng **vẫn đỏ** — nhưng nay đỏ **có câu nói gốc**: `⛔ không đo được: ảnh PM hiệu lực của kho TEST là 'NAP-2000-01-01-LA4C5A52', ⛔ phải ảnh của ca 'NAP-2000-06-01-APA18DC1' — có tiến trình khác vừa nạp ảnh PM mới hơn vào fls_test (chạy pytest một mình)` *(`Đ5`)*. Xem "còn yếu" 4.

## Kho thật
- **`KHONG_CHAM`**. Sổ thật chỉ **đọc**: `noi_chi_doc` *(công cụ + bài `AC-5`, `transaction_read_only = on`)*, `psql` `SET default_transaction_read_only = on` *(đếm `HOI-063`)*, máy **8097 ⛔ `--cho-ghi`** *(Chrome: **0** `POST` cả hai lượt)*. ⛔ `ANALYZE` / `VACUUM` / chỉ mục / `SET` lưu. `fls_queue_event` sổ thật đầu = cuối phiếu **110.349**. ⚠ Một lần đầu tôi gõ `psql` ⛔ chỉ đọc để xem `\d fls_queue_event` + `count(*)` — chỉ `SELECT`/`\d`, ⛔ ghi.
- Kho TEST *(`fls_test`)*: các ca bài thử + **hai** ảnh PM lạ `NAP-2000-01-01-LA…` của phép tái hiện `AC-10` *(sẽ mất ở lượt `pytest` kế ⛔ `FLS_GIU_KHO` — kho dựng lại đầu phiên)*.

## Cách chạy để xem *(chạm UI)*
- Sổ thật **chỉ đọc**: `PG_DSN=postgresql://fls:fls@localhost:5433/fls FLS_JWT_SECRET=<≥32 ký tự> python tools/chay_cua.py --cho-web --cong 8097` ⇒ `Hàng chờ · F01` ▸ `Theo dòng tiền` ▸ thẻ `VND` ▸ `Xem thêm` *(chữ `Đang tải thêm…` chớp ~0,1 s; muốn thấy lâu / lỗi: DevTools chặn hay làm chậm `*cursor=*`)*.
- Đo cửa: `python tools/do_trang_hang_cho.py` *(mọi trang)* · `--explain VND:50`.
- Chrome: `node cdp51.mjs 8097 <cổng CDP>` *(lật hết)* · `cdp51b.mjs` *(giữ / làm hỏng lượt `cursor=`)* — kịch bản một lần ở scratchpad phiên *(⛔ vào `tools/`)*.

## Dev tự thấy còn yếu
1. **Giá của cách sửa tăng tuyến tính theo `fls_queue_event`.** View gom **cả bảng** một lần mỗi trang: **~60 ms** trên 110.349 sự kiện ⇒ chạm `2 s` ở cỡ ~3,6 triệu sự kiện *(ngoại suy tuyến tính, ⛔ đo)*. Cách O(một trang) *(`LATERAL … OFFSET 0`, **0,021 s**)* có sẵn nhưng đổi `reason` **398 / 8.387** hàng ⇒ chờ `HOI-063` *(khoá phụ `evt_id` cho view)*.
2. **"Không đổi một byte" là so với một kết quả vốn ⛔ xác định.** `reason` trên **8.256 / 8.387** dòng là phần tử nào kế hoạch gom đưa ra trước *(`HOI-063`)*; oracle và mã mới khớp vì **cùng** kế hoạch gom cả bảng *(`GroupAggregate` + `Incremental Sort` trên `fls_queue_event_itl_idx`)*. Nếu PostgreSQL đổi kế hoạch của **chính** view *(thống kê trôi, `HashAggregate`)* thì **cả hai** cùng đổi — oracle vẫn 0 lệch, nhưng chữ chip `lý do` trên màn có thể đổi mà ⛔ ai bấm gì.
3. **Bài `AC-4` kho TEST ⛔ bắt "bỏ hẳn `ORDER BY` trong `trang`"** *(13 passed)*: `WindowAgg` trả hàng đã theo `(curr, hang)` nên `LIMIT` ⛔ xếp vẫn ra đúng — hôm nay, trên kế hoạch này. Mã giữ `ORDER BY` *(⛔ dựa vào thứ tự ngầm)*; bài bắt được `ORDER BY` sai chiều, con trỏ `>=`, `JOIN` thường.
4. **`test_anh_pm_pg` vẫn phụ thuộc trạng thái kho** *(3 bài — gốc `M2`)*: một ảnh PM lạ mới hơn ⇒ đỏ *"⛔ không đo được"* có câu, ⛔ còn đỏ mù. ⛔ Thu về một ca được vì bài hỏi đúng câu "hai lần nạp". Nếu Test lại chạy máy 8099 / dựng ca trên `fls_test` **trong lúc** `pytest` toàn bộ chạy, ba bài này sẽ đỏ — lần này câu đỏ nói vì sao.
5. **`M2` chứng bằng ảnh lạ `+1h` (cực trị)**. Ảnh lạ `now()` chèn giữa lượt *(hình thật của một tiến trình khác)* tôi thử **một** lần ở mốc 6 s — bài cửa đã chạy xong trước mốc ⇒ **0** đỏ cửa; ⛔ thử mốc khác. Lý thuyết: bài dựng ca **trước** mốc mà hỏi cửa **sau** mốc sẽ đỏ — ⛔ chứng bằng ảnh tự nhiên, và tôi ⛔ tái hiện **đúng** 9 bài của lượt 4 *(⛔ biết giờ Test dựng ca)*. Hai gốc giải thích **cả 9** *(2 + 7)*, nhưng gán từng bài của lượt 4 vào gốc nào là suy luận.
6. **`AC-8` đo trên Chrome headless**; `265 ms` là thời gian từ `mousedown` tới khi `MutationObserver` thấy số hàng tăng — gồm cửa *(~0,1 s)* + vẽ lại **cả** lưới *(`_ve_luoi` dựng lại 4.000+ hàng mỗi lượt)*; trang cuối chậm dần theo số hàng *(90 → 265 ms)*. ⛔ Đổi `ve_luoi` *(ngoài phạm vi `(c)`)*.
7. **`Thử lại` cũng đổi chữ thành `Đang tải thêm…` khi đang chờ** — tôi đọc `ⓦ` ⑦ hàng "tải" là trạng thái của **lượt** `Xem thêm` *(cả lượt lật lại)*; spec ⛔ nói riêng chữ của nút `Thử lại` lúc chờ. `fls-ba` soi.
8. Bẫy đo đã cắn **trong** phiếu: bản đầu công cụ dùng **một** kết nối ⇒ mã cũ báo trang 2 `VND` **0,088 s** *(xanh giả — `psycopg` `prepare` sau 5 lần ⇒ kế hoạch chung)*. Đã sửa *(kết nối mới mỗi trang)* và ghi chú tại `ket_noi_moi` + `_SQL_HANG_CHO`; nhưng mọi phép đo hiệu năng khác trong repo đo trên một kết nối dùng lại đều có thể mang bẫy này *(⛔ rà)*.
