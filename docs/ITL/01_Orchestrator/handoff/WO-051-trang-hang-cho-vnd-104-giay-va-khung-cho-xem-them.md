# WO-051 — Trang hàng chờ `VND` từ trang 2 trở đi mất **~100 s** ⇒ ≤ `2 s` *(`NFR-I30`)* · `F01` `Xem thêm` có khung chờ và lỗi ⛔ xoá lưới

| | |
|---|---|
| **Trạng thái** | ⭐ `CHO_TEST` *(`fls-dev` 06/10 — [`BG-064`](BG-064-ban-giao-wo-051.md); `HOI-063` `KHONG_CHAN` mở cho `fls-ba`)* · ~~`DANG_LAM` *(`fls-dev` nhận 06/10 — cổng vào: `git` `9af99c4` = `origin` ✔ · `BA-08` **v1.4** ✔ · `BA-06` **v4.24** *(phiếu ghi v4.22; `ⓦ` ⑦ ⛔ đổi từ v4.22 — đọc lại `:814-825`)* ✔ · `pytest` một mình **2** lượt: `2407 passed, 2 xfailed` ×2)*~~ · ~~`MO` · ⭐ **SẴN SÀNG — LÀM NGAY** *(06/10 — `WO-023` ✅ `DONG`, `KQ-061` ĐẠT 17/17; thứ tự `fls-ba` 06/10: **phiếu này** → `WO-062` → `WO-060` → `WO-047` → `WO-015`; ⭐ thêm `AC-10` bài chập chờn — vẫn **vòng 1**)*~~ · ~~⏳ chờ `WO-023` *(thứ tự điều phối 05/10: `WO-023` → phiếu này → `WO-047` → `WO-015`)*~~ · ưu tiên **CAO** *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-05 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(cú `Gán` sai dòng — `(i)` `NANG` chạm cú **ghi**; phiếu này chạm cú **đọc**)*. **Trước** [`WO-047`](WO-047-mot-tap-ky-tu-cho-phep-so-tien-te-con-lai.md) *(sổ thật **0** ca)* · [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) *(⛔ con số nào đổi)*. Khác tệp với `WO-023` ở tầng repo *(`doc_bao_cao.py`)*; giao nhau **một** tệp màn `man_f01.js` *(`WO-023` ⛔ chạm `_xem_them`)* ⇒ ⛔ giẫm nhau, nhưng giữ thứ tự để hai `BG` ⛔ chồng trên cùng nền đang kiểm |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết một vòng ghép thật)* — màn `F01` hàng chờ là nơi kế toán **tìm** dòng tiền cần ghép, xếp theo tiền *(`QĐ-ITL-58`)*. `VND` là tiền tệ **lớn nhất** của hàng chờ *(sổ thật `dem_hang_cho` 05/10: `VND` **4.242** · `USD` **3.980** · `SGD` **145** · `HKD` **20** dòng)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; giữ mắt xích *"ghép PM ↔ tiền"* đã lên FLS **⛔ thua Sheets** — trên Sheets cuộn xuống dòng 51 là tức thì; trên FLS hôm nay là **104 s** một nút xám ⛔ một chữ. Một kế toán *(`QĐ-ITL-27`: 2–3 người)* bấm `Xem thêm` hai lần mà ⛔ thấy gì sẽ kết luận **màn hỏng** và quay về Sheets.

### Vì sao ưu tiên **CAO**, và vì sao **sau** `WO-023`
| Phiếu | Hại hôm nay | Chạm GHI? |
|---|---|:-:|
| `WO-023` `(i)` | `Gán` / `Enter` gửi dòng tiền người **⛔ chọn**, cửa ghi **nhận** *(① `KQ-050`: cặp trong dung sai ⇒ `200`)* | ✅ ghi sai vào sổ chỉ-thêm |
| **phiếu này** | trang 2…85 `VND` **⛔ tới được** trong thực tế *(104 s/trang ⇒ lật hết ≈ **2,4 giờ**)*; dòng `VND` hạng **> 50** ⛔ ai thấy trên `F01` | ⛔ — nhưng **giấu** 4.192 / 4.242 dòng `VND` = **98,8%** |
| `WO-047` · `WO-015` | sổ thật **0** ca / ⛔ con số nào đổi | ⛔ |

## Căn cứ
- [`KQ-050`](KQ-050-kiem-bg-048.md) **`F-1`** *(`fls-test` 05/10, `NANG` ngoài phạm vi `WO-045`)*: `curl` 8088 sổ thật — `/queue?curr=VND&limit=50` **0,11 s** · `…&cursor=VND%3A50` **95,1 s** rồi **81,1 s** · `curr=USD&cursor=USD%3A50` **0,11 s**; `F01` `VND` bấm `Xem thêm` ⇒ nút khoá **~1,5 phút**, ⛔ khung chờ. Nghi `doc_bao_cao.doc_hang_cho` `AND (x.curr, x.hang) > (%s, %s)` trên CTE cửa sổ; chưa đo `EXPLAIN`.
- ⭐ **`fls-ba` đo lại 05/10** *(hàm thật `fls.repo.doc_bao_cao.doc_hang_cho`, `noi_chi_doc` — `transaction_read_only = on`, `chi_nap_that()`, `limit=50`)*:

| Cửa | Trang 1 | Trang 2 |
|---|---|---|
| `/queue` `HKD` *(20 dòng)* | **0,12 s** | — *(một trang)* |
| `/queue` `SGD` | **0,07 s** | **0,07 s** |
| `/queue` `USD` | **0,09 s** | **0,08 s** |
| `/queue` `VND` | **0,09 s** | ⛔ **104,33 s** |
| `/lenh-cho` `VND` · `USD` · ⛔ lọc *(trang 1–4 mỗi loại, `doc_lenh_cho`)* | **0,64–0,74 s** | *(cùng khoảng)* |

- ⭐ **Giả thuyết `fls-ba`** *(đọc `EXPLAIN` **⛔ `ANALYZE`** trên sổ thật — **chưa chứng minh**, đó là `AC-1` của Dev)*: với con trỏ `('VND', 50)` bộ lập kế hoạch ước lọc `ROW(x.curr, x.hang) > ROW('VND', 50)` còn **`rows=1`** *(`VND` là tiền tệ **cuối** theo thứ tự chữ ⇒ ước như cận trên)* nên chọn **`Nested Loop Left Join`** với `fls_queue_state` — một **view** gom *(`GroupAggregate` + `Incremental Sort`)* trên **`fls_queue_event` 110.349 dòng** *(`SELECT count(*)` 05/10; **108.128** là `reason` của lần dựng lại 10/09, actor `dung-lai-so@apero.vn`)* ⇒ view bị tính lại cho **mỗi** dòng ngoài *(thật ~4.192)*. Con trỏ `('USD', 50)` ước `rows=2013` ⇒ `Hash Right Join`, view tính **một** lần ⇒ 0,08 s. Nếu đúng: ⓐ lỗi **⛔ phải** của chỉ `VND` — mọi con trỏ mà ước ra nhỏ đều dính; ⓑ sẽ **chậm thêm** theo mỗi `fls_queue_event` mới *(mỗi cú ghép / lý do / hoãn của kế toán)*.
- Cùng khuôn con trỏ ở `fls/repo/lenh_cho.py:320` *(`doc_lenh_cho`)* — đo **lành** *(bảng trên)*, ⛔ trong phạm vi sửa nhưng **trong** phạm vi đo *(`AC-3`)*.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(ngưỡng `NFR-I30` — số `fls-ba` chọn sau khi đo, owner đổi được một số; hành vi trạng thái màn `ⓦ` ⑦)*. ⛔ câu nghiệp vụ: phiếu ⛔ đổi **thứ tự** hàng chờ, ⛔ đổi **dòng nào** vào hàng chờ, ⛔ đổi con số nào.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/08_NFR.md` | ⭐ `§2` **`NFR-I30`** *(một trang danh sách việc ≤ `2 s`, mọi trang, sổ thật, đồng hồ quanh hàm thật)* · `NFR-I07` · `NFR-I09` *(⛔ nới `timeout` để giấu)* | ⭐ **v1.4** |
| `02_BA/06_SCREEN_SPEC.md` | ⭐ `§4.5 ⓦ` ⑦ *(`F01` `Xem thêm` — bảng bốn trạng thái)* · `ⓦ` ① *(lượt mới nhất — `WO-045` đã làm, ⛔ đổi)* · `ⓦ` ④ *(khuôn chữ `⛔ Cửa lỗi:`)* | ⭐ **v4.22** |
| `02_BA/07_API_CONTRACT.md` | `GET /queue` *(`next_cursor` · `cursor` `"<tiền tệ>:<hạng>"`)* — ⛔ đổi | hiện hành |
| `fls/repo/doc_bao_cao.py` | `_CTE_HANG_CHO` · `_SQL_HANG_CHO` · `doc_hang_cho` — chú thích đầu khối *(phạm vi **trong** câu con `q`, `fls_da_xong` cùng điều kiện `dem_hang_cho`, ⛔ chép CTE)* | `HEAD` |
| `01_Orchestrator/handoff/KQ-050-kiem-bg-048.md` | `F-1` + lăng kính **Màn hình** *(⛔ lật hết `F01` `VND`)* | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a) Đo trước khi sửa** — `EXPLAIN (ANALYZE, BUFFERS)` câu `_SQL_HANG_CHO` của trang 2 `VND` trên **sổ thật chỉ đọc** *(`noi_chi_doc`; `statement_timeout` đủ cho một lượt ~100 s)*; dán kế hoạch vào `BG`, gọi tên **nút** ăn thời gian; **chứng** hay **bác** giả thuyết *Căn cứ*. Bác ⇒ ghi `BG` gốc thật, sửa theo gốc thật *(⛔ `HOI` nếu vẫn trong (b))* | ⛔ `ANALYZE` / `VACUUM` / `SET` lưu lại trên sổ thật *(đều là **ghi** — `10` §4.4)*; ⛔ đổi tham số máy chủ PG |
| **(b) Sửa `doc_hang_cho`** *(`fls/repo/doc_bao_cao.py`)* sao cho **mọi** trang **mọi** tiền tệ ≤ `2 s` trên sổ thật — Dev chọn cách *(gợi ý, ⛔ bắt buộc: nối `fls_queue_state` **sau** `LIMIT`; lọc hạng ở một câu con đã chốt tập trước khi nối; `MATERIALIZED`)*; **kết quả trả ra ⛔ đổi một byte** *(hàng · thứ tự · `hang` · `luy_ke_pct` · `next_cursor`)*. Chú thích tại chỗ ghi số đo trước/sau *(bia của lỗi)* | ⛔ đổi khuôn con trỏ / hợp đồng cửa · ⛔ đổi `_CTE_HANG_CHO` cho `_SQL_DO_PHU` nếu ⛔ cần *(nó ⛔ có con trỏ)* — nếu đổi CTE chung thì `do_phu_hang_cho` phải ra **cùng** số *(`AC-4`)* · ⛔ **migration / chỉ mục** *(chạm sổ thật = ghi lược đồ)* ⇒ nếu (b) ⛔ đủ mà ⛔ có chỉ mục ⇒ **`HOI`**, ⛔ tự thêm |
| **(c) `F01` `Xem thêm`** *(`fls/web/tep/man_f01.js` `_xem_them` · khối chân lưới `:176-187` @ `c903eb3`)* theo `BA-06` v4.22 `ⓦ` ⑦: tải ⇒ nút khoá + chữ `Đang tải thêm…`; lỗi / mất kết nối ⇒ hàng đã có **giữ**, dòng `⛔ Cửa lỗi: <e.cau>` + nút `Thử lại` *(`b tiny`)* lật lại **đúng** con trỏ, **một** lượt | ⛔ token / lớp CSS mới · ⛔ đếm giây · ⛔ đổi `ve_luoi` / luật lượt `WO-045` · ⛔ `F01L` / `F02` `Xem thêm` *(đo nhanh — `ⓦ` ⑦)* |
| **(d) Bài thử** — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; bài **hồi quy hiệu năng** đọc **sổ thật chỉ đọc** *(`noi_chi_doc`; khuôn các bài đang soi kho thật)* với `statement_timeout` ngắn ⇒ mã khi nhận **ĐỎ trong vài giây**, ⛔ chờ 100 s | ⛔ sửa `tests/nghiem_thu/**` · ⛔ bài ghi vào sổ thật · ⛔ nới `timeout` bài nào để xanh *(`NFR-I09`)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a)* | `BG` dán kế hoạch `EXPLAIN (ANALYZE, BUFFERS)` trang 2 `VND` **trên mã khi nhận** + **sau sửa**, có: nút ăn thời gian *(tên + `actual time` + `loops`)*, kết luận **chứng / bác** giả thuyết *Căn cứ* bằng chính số `loops` | lệnh trên sổ thật chỉ đọc *(`noi_chi_doc`)* | — *(bằng chứng chẩn đoán)* |
| AC-2 *(b — ngân sách)* | Sổ thật chỉ đọc, hàm thật `doc_hang_cho(chi_nap_that(), curr=c, limit=50)` lật **hết** mọi trang cho **mỗi** `c` ∈ {`HKD`, `SGD`, `USD`, `VND`} **và** `curr=None`: **mọi** trang ≤ `2,0 s` đồng hồ *(`BG` in bảng `c · số trang · max s · trang chậm nhất`)*; số hàng mỗi `c` = `dem_hang_cho` **cùng lượt** *(05/10: 4.242 · 3.980 · 145 · 20 — mẫu số ≠ 0, `Đ3`)*; `itl_id` ⛔ trùng; `(curr, hang)` tăng nghiêm | kịch bản đo + bảng trong `BG` | mã khi nhận ⇒ trang 2 `VND` > `2 s` ⇒ **ĐỎ** |
| AC-3 *(b — `/lenh-cho` cùng khuôn)* | Cùng phép `AC-2` cho `doc_lenh_cho` *(⛔ lọc + từng tiền tệ, lật hết)*: mọi trang ≤ `2,0 s`. Hôm nay đo **0,64–0,74 s** ⇒ mong **xanh ⛔ sửa**; đỏ ⇒ cùng gốc ⇒ sửa trong phiếu này | như trên | — *(đo; đỏ ⇒ mở rộng (b))* |
| AC-4 *(b — kết quả ⛔ đổi)* | **Oracle độc lập con trỏ**: mã **khi nhận**, câu `_SQL_HANG_CHO` **⛔ con trỏ** với `limit` ≥ số dòng *(trang đầu nhanh — `0,09 s`)* ⇒ danh sách đầy đủ mỗi tiền tệ; nối mọi trang của mã **mới** ⇒ **bằng hệt** theo `(itl_id, hang, luy_ke_pct, reason, defer_until, defer_count)` — lệch **0 / 8.387** hàng *(Σ bốn tiền tệ 4.242 + 3.980 + 145 + 20, đo 05/10)*. `do_phu_hang_cho(90)` cũ = mới **4/4** tiền tệ. Kho TEST: bài cửa `GET /queue` hiện có xanh ⛔ sửa `assert` | bài `tests/repo/` *(kho TEST, phân trang nhiều tiền tệ, so với danh sách ⛔ con trỏ)* + phép sổ thật trong `BG` | lệch thứ tự / mất hàng ở mép trang ⇒ **ĐỎ** |
| AC-5 *(d — hồi quy hiệu năng)* | Bài đọc **sổ thật chỉ đọc** gọi `doc_hang_cho` trang 2 của tiền tệ **nhiều dòng nhất** *(tra `dem_hang_cho` lúc chạy — ⛔ ghi cứng `VND`)* với `statement_timeout = 2s` ⇒ xanh. Sổ thật tắt / tiền tệ ⛔ có trang 2 ⇒ **ĐỎ** "⛔ không đo được" *(`Đ5`, ⛔ `skip`)* | `pytest` bài mới | mã khi nhận ⇒ `QueryCanceled` ⇒ **ĐỎ** *(BG dán)* |
| AC-6 *(c — tải)* | Bài DOM `man_f01.js` thật, cửa giả `/queue` **treo** khi có `cursor`: bấm `Xem thêm` ⇒ nút `disabled` **và** `textContent` = `Đang tải thêm…`; số hàng lưới **giữ** 50; bấm thêm ⇒ **0** `GET` thêm. Thả ⇒ 100 hàng, nút về `Xem thêm` | bài DOM `tests/web/` | mã khi nhận *(chữ ⛔ đổi)* ⇒ **ĐỎ** |
| AC-7 *(c — lỗi)* | Cửa giả trả lỗi `FLS-INTERNAL` / `FLS-MAT-KET-NOI` cho lượt `cursor`: lưới **còn 50** hàng; dưới lưới `⛔ Cửa lỗi: <e.cau>` + **một** nút `Thử lại` lớp `b tiny`; bấm ⇒ **một** `GET` mang **đúng** `cursor` vừa lỗi; xanh ⇒ 100 hàng, câu lỗi mất | bài DOM — hai ca | mã khi nhận *(`TT.loi` thay cả khung ⇒ 0 hàng)* ⇒ **ĐỎ**; `Thử lại` lật từ đầu / mở hai lượt ⇒ **ĐỎ** |
| AC-8 ⭐ *(Chrome — sổ thật)* | **8088 sổ thật CHỈ ĐỌC**, Chrome 1440×900, chuột thật: `F01` `VND` ▸ `Xem thêm` ⇒ chữ `Đang tải thêm…` hiện; 100 hàng hiện trong ≤ **`2 s`** *(đồng hồ từ cú bấm tới DOM)*; lật **hết** `VND` ⇒ DOM **= thẻ `VND <n> dòng chờ` = `dem_hang_cho`** cùng lượt *(05/10: 4.242)*, `itl_id` ⛔ trùng; **0** `POST`; console **0** lỗi *(ngoài `favicon.ico` của trình duyệt)* | Chrome CDP | — |
| ⭐ AC-10 *(đo — bài chập chờn, `KQ-061` ghi chú phương pháp)* | `KQ-061` lượt `pytest` 4: **9** đỏ ở **4** tệp ngoài `WO-023` — `tests/**/test_wo032_v2_bac_da_gan_pg.py` ×2 · `test_wo037_ro_may_theo_cua_ghi_pg.py` ×4 · `test_wo037_v2_ro_nguoi_hai_cau_pg.py` ×1 · `test_anh_pm_pg.py` ×2 *(lý do `⛔ không có trong ảnh chụp hiệu lực` / `0 hàng`)*; lượt 5 cùng mã + chạy riêng **xanh**; Test nghi chọn *"ảnh PM hiệu lực"* theo `max(read_at)` *(`anh_pm.py:65`)* gặp ảnh của ca khác. ⓐ `BG` dán `pytest` toàn bộ **một mình** *(⛔ tiến trình nào khác chạm `fls_test`)* **≥ 2** lượt ở cổng vào **và** ≥ 2 lượt cuối phiếu, nguyên văn dòng tổng; ⓑ **tái hiện có kiểm soát**: chạy 4 tệp **sau** một bài dựng ảnh PM có `read_at` mới hơn *(hay đảo thứ tự tệp)* — đỏ ⇒ gốc **chứng**, bài sửa cho **tự đủ** *(đọc ảnh của **chính** ca — khuôn `WO-023 (j)`)*, chứng đỏ bản cũ / xanh bản mới **cùng** trạng thái kho; ⛔ đỏ sau ≥ 3 cách ⇒ `BG` ghi *"⛔ tái hiện — <các cách đã thử>"*, **⛔ sửa** | `pytest` + `BG` | *(nếu chứng)* bài sửa vẫn đọc `max(read_at)` toàn kho ⇒ lượt có ảnh lạ **ĐỎ** |
| AC-9 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai · `lint-imports` **9 / 0** · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI — chân lưới `F01`)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.22** `§4.5 ⓦ` ⑦. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(⛔ token, ⛔ lớp CSS mới — `b tiny`, `banner crit` / khuôn `⛔ Cửa lỗi:` đang có)*.

| Trạng thái | Lưới `F01` *(trang đầu — ⛔ đổi)* | Lượt `Xem thêm` *(mới)* |
|---|---|---|
| tải | `TT.chay` như nay | nút khoá + `Đang tải thêm…`; hàng đã có giữ |
| rỗng | `Không còn dòng nào ở mức lọc này` như nay | ⛔ áp *(⛔ `next_cursor` ⇒ ⛔ nút)* |
| lỗi | `TT.loi` + `Thử lại` như nay | hàng đã có giữ + `⛔ Cửa lỗi: <e.cau>` + `Thử lại` *(đúng con trỏ)* |
| mất kết nối | như lỗi | như lỗi *(`FLS-MAT-KET-NOI`)* |
| có dữ liệu | như nay | nối hàng, nút `Xem thêm` / chip `hết danh sách` |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ đổi **câu đọc** `_SQL_HANG_CHO` *(⛔ đổi tập bảng mà bảng tuyến khai cho `/queue` — `soi_bang_tuyen` giữ khớp)*.
- Ghi kho THẬT: **`KHONG`**. Sổ thật chỉ **đọc** qua `noi_chi_doc` *(AC-1…AC-5)* và 8088 chỉ đọc *(AC-8)*. ⛔ `ANALYZE` / `VACUUM` / chỉ mục trên sổ thật.
- Số dòng sổ thật đổi *(đã đếm — `fls-ba` 05/10)*: **0** — phiếu đổi **tốc độ** một câu đọc, ⛔ đổi kết quả *(`AC-4` lệch 0)*. Báo động hiếm ⛔ áp.

## Nền khi nhận *(`fls-ba` chép 05/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — sau `BG` + `KQ` của `WO-023`; mã `fls/**` cuối hôm nay = `2b804e3` *(`WO-045` ✅ `DONG`)* | `git log` |
| `pytest` | hôm nay **`2330 passed, 6 xfailed`** *(`KQ-050` đo cuối lượt @ giấy `168e126`)* — sẽ đổi sau `WO-023` | `KQ-050` |
| `kiem_so_song` | **55** hôm nay *(⛔ `dong_bo --ghi`)* | `KQ-050` · lệnh |
| sổ thật | `dem_hang_cho` `VND` **4.242** · `USD` **3.980** · `SGD` **145** · `HKD` **20**; trang 2 `VND` **104,33 s**; `fls_queue_event` **110.349** dòng | `fls-ba` 05/10 |

## Câu còn treo
- ⛔ câu cho owner. Ngưỡng `2 s` *(`NFR-I30`)* là số `fls-ba` chọn sau khi đo — owner muốn khác thì đổi **một** số + một dòng spec; ⛔ chặn.
- `Q-FX-1` · `Q-TIEN-1` · `GAP-SCR-33` · `GAP-SCR-26` vẫn treo — ⛔ chạm: phiếu ⛔ đổi thứ tự, tập hay nguồn con số.

## Rủi ro
1. **Sửa nhanh mà đổi kết quả** — viết lại câu có cửa sổ + `LEFT JOIN` dễ lệch **một** hàng ở mép trang *(cùng lớp `do_phu` ⓐ/ⓑ "lệch đúng một dòng")* ⇒ `AC-4` so **toàn bộ** danh sách, ⛔ mẫu.
2. **Bài hồi quy đọc sổ thật** — sổ thật tắt / đổi phân bố ⇒ bài đỏ "⛔ không đo được" *(đúng `Đ5`)*; ⛔ biến nó thành `skip`.
3. **Kế hoạch truy vấn trôi theo dữ liệu** — `fls_queue_event` lớn dần theo mỗi thao tác người ⇒ một cách sửa "nhờ may" ước lượng hôm nay có thể hỏng lại; cách sửa nên **⛔ phụ thuộc** ước lượng hàng *(chốt tập trước khi nối)* — `BG` nói vì sao.

## Changelog
- 2026-10-06 · `fls-dev` · `DANG_LAM` → **`CHO_TEST`** — [`BG-064`](BG-064-ban-giao-wo-051.md): gốc **chứng** *(`EXPLAIN ANALYZE`: `GroupAggregate` view `loops=4192`, 111,9 s)*; `doc_hang_cho` gom view một lần *(`MATERIALIZED`)* ⇒ mọi trang mọi tiền tệ ≤ **0,11 s**, oracle lệch **0 / 8.387**; `F01` `Xem thêm` khung chờ + lỗi giữ hàng; Chrome 8097 lật hết `VND` 4.242; `AC-10` hai gốc chứng *(`M1` mã lệnh cố định + kho giữ · `M2` ảnh PM của cả kho TEST)*; mở [`HOI-063`](HOI-063-ly-do-moi-nhat-cua-fls-queue-state-khong-xac-dinh.md) *(`reason` của view ⛔ xác định — `KHONG_CHAN`)*.
- 2026-10-06 · `fls-ba` · `WO-023` ✅ `DONG` ⇒ phiếu này **SẴN SÀNG**; ⭐ thêm **`AC-10`** *(đo)* — bài chập chờn `KQ-061` *(9 đỏ / 4 tệp ở một lượt, xanh khi chạy riêng)*: tái hiện có kiểm soát trước khi sửa. Vì sao vào đây: phiếu Dev nhận **kế tiếp**, và `AC-4` của nó so **toàn bộ** danh sách qua `pytest` — cổng chập chờn làm `BG` ⛔ đọc được. Thứ tự 06/10: **`WO-051`** → `WO-062` → `WO-060` → `WO-047` → `WO-015`.
- 2026-10-05 · `fls-ba` · phát **`WO-051`** `MO` từ `KQ-050 F-1` *(`NANG` ngoài phạm vi `WO-045`)*; đo lại hàm thật trên sổ thật chỉ đọc *(trang 2 `VND` **104,33 s**; 18 trang lành **0,07–0,74 s**)* + `EXPLAIN` ⛔ `ANALYZE` ⇒ giả thuyết `Nested Loop` × view `fls_queue_state`; spec `BA-08` **v1.4** `NFR-I30` *(khai mới — `§2` trước đó ⛔ có ngưỡng cho trang hàng chờ)* · `BA-06` **v4.22** `ⓦ` ⑦. Ưu tiên **CAO**; thứ tự điều phối 05/10 `WO-023` → **`WO-051`** → `WO-047` → `WO-015`.
