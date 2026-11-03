# 03 — IMPLEMENTATION PLAN: roadmap triển khai FLS

**Version:** v2.9 · **Ngày:** 2026-08-27 · **Chủ sở hữu:** Tech Lead
**Thay thế:** v0.1 *(bản copy chương trình FIN-ERP, tự ghi "chưa dẫn xuất cho ITL")* — đã khai tử.

**Căn cứ:** `01_TECH_DESIGN` v1.0 §2·§4 *(sơ đồ khối + ranh giới module)* · `02_REPO_CONVENTIONS` v1.0 *(repo `FLS` độc lập)* · `04_DB_IMPLEMENTATION` v1.0 *(schema)* · `06_SCREEN_SPEC` v1.7 *(4 màn)* · `07_API_CONTRACT` v1.1 · `10_PM_JOIN_ADAPTER_SPEC` **v0.2**

> ⭐ **Luật xuyên suốt roadmap này: mỗi pha kết thúc bằng CỔNG ERD chạy được, không phải một buổi rà tài liệu.** Lý do ở §1 — drift ERD↔thiết kế đã xảy ra rồi, và một cổng bằng mắt người sẽ trượt lần nữa.

---

## §1 · Vì sao cổng ERD phải là TEST, không phải review

Anh chủ dự án nêu: *"trong quá khứ hay gặp vấn đề drift thiết kế và ERD"*. Rà lại ngày 26/08 thì **drift đang tồn tại ngay tại vạch xuất phát**, chưa viết dòng code nào.

### 1.1 · Drift #1 — ERD của BA và DDL của Dev đang tả hai mô hình khác nhau

`02_BA/05_DATA_DICTIONARY_ERD.md` §ERD có **10 entity**; `04_DB_IMPLEMENTATION` có **10 bảng + 2 view**. Chỉ **3 chỗ khớp**.

| ERD *(BA)* | Thực tế DDL *(Dev)* |
|---|---|
| `SOURCE_FILE` | ≈ `fls_source` — **khác tên** |
| `STAGED_ROW` | ✗ **không phải bảng** — là trạng thái `staged` của `fls_itl` |
| `MAPPING_MASTER` | ✅ `fls_mapping_master` |
| `ITL_RAW` | ✗ **gộp** vào `fls_itl` *(`raw_frozen=true`)* |
| `ADJUSTMENT_ENTRY` | ✅ `fls_adjustment` |
| `ITL_LEDGE` | ✗ **gộp** vào `fls_itl` |
| `ALLOCATION` | ✗ **không phải bảng** — 3 cột trong `fls_itl` |
| `AUDIT_RESULT` | ✗ **không phải bảng** — cột `audit_status` |
| `RUN` | ✅ `fls_run` |
| `PERIOD` | ✗ **không phải bảng** — cột `period_state` |

**Bảng có trong code mà ERD KHÔNG hề nhắc:** `fls_journal` · `fls_queue_event` · `fls_le` · `fls_reject` · `fls_id_counter` · view `fls_queue_state` · view `fls_queue_reason_weekly`.

⛔ **Nặng nhất: `fls_journal` vắng mặt khỏi ERD** — mà `QĐ-ITL-27` gọi nhật ký là **chỗ kiểm soát duy nhất còn lại** sau khi khai tử người hậu kiểm. Cấu phần quan trọng nhất của hệ không có trên bản đồ dữ liệu.

⛔ **Và hai doc nói trái nhau về mô hình vật lý:**

| Doc | Câu |
|---|---|
| `05_DATA_DICTIONARY_ERD:427` | *"`ITL_LEDGE` là **view kết hợp** RAW + bút toán đã duyệt, **không phải bảng**"* |
| `04_DB_IMPLEMENTATION:40` | *"Ba lớp **một bảng, không tách**"* |

Một bên bảo view, một bên bảo bảng. Người viết adapter đọc doc nào thì code ra hệ đó.

### 1.2 · Drift #2 — `fls_id_counter` sao chép đúng cái pattern FPS đã khai tử

`04_DB_IMPLEMENTATION:166` viết: *"sinh atomic bằng bảng `fls_id_counter` (pattern `fps_id_counter` — **đã fix bug dup thật ở FPS**)"*.

Nhưng đọc code FPS thật *(`P100-R/fps-backend/fps/db/pg_schema.py:9`)*, cách FPS **fix** bug đó là **bỏ bảng counter đi**:

> *"`fps_id_counter` (UPDATE+SELECT 2 round-trip, 36% độ trễ, streaming-buffer trùng ID) → **THAY bằng SEQUENCE + DEFAULT** sinh business-id tại DB."*

⇒ Bài học bị đọc ngược: cái được "fix" là **thôi dùng counter**, không phải "counter đã lành, cứ copy". Và `itl_id` là **danh tính đóng băng** (`INV-I04a`) — trùng id ở đây là hỏng khoá của cả sổ.
**Sửa trong P0:** `CREATE SEQUENCE seq_itl_id` + `DEFAULT nextval(...)`, bỏ `fls_id_counter`.

### 1.3 · Ba cổng chạy được — thay cho rà bằng mắt

ERD trở thành **hiện vật sinh ra từ code**, không phải hình vẽ tay:

| Cổng | Test | Bắt được gì |
|---|---|---|
| **G-ERD-1** *(đồng bộ)* | `test_erd_generated_matches_committed` | sinh ERD từ `pg_schema.py`, diff với file đã commit ⇒ đổi schema mà quên cập nhật ERD = **build đỏ** |
| **G-ERD-2** *(đầy đủ entity, hai chiều)* | `test_erd_doc_covers_all_tables` | mọi bảng/view trong code **phải** có trong ERD của BA; mọi entity trong ERD **phải** tồn tại trong code ⇒ **cổng này bắt đúng drift §1.1** |
| **G-ERD-3** *(bảng có kết nối)* | `test_fk_graph_connected` | mọi bảng phải với tới được `fls_itl` qua FK, nếu không thì **phải** khai trong `ERD_ISLANDS` kèm lý do bằng chữ ⇒ không có bảng mồ côi lặng lẽ |

Kèm cổng đã được `01_TECH_DESIGN` §6 yêu cầu sẵn: `test_itl_contract_v1_lock` *(khoá 14 trường, `INV-I07`)*.

★ **Cả 4 cổng chạy ở CUỐI MỖI PHA, và trong CI mọi PR.** Không pha nào được "xong" khi cổng đỏ.

---

## §2 · Bảy pha

Mỗi pha ra được **software chạy và test được**, không pha nào là "chuẩn bị cho pha sau".

| Pha | Ra cái gì | Điều kiện vào | Cổng ra |
|:--:|---|---|---|
| **P0** ✅ **XONG 26/08** | Nền + **4 cổng**. `pg_migrate --dry-run` in trọn DDL. **0 dòng luật nghiệp vụ** | ~~repo `FLS` được tạo~~ ✅ | ✅ `pytest` **34 passed** *(29 offline + 5 PG thật)* · `lint-imports` **2 kept 0 broken** · ERD đồng bộ DDL · trigger `INV-I03/I04a` có test. Repo `C:\Users\0_Apero Project\FLS`, nhánh `feat/p0-foundation`, 9 commit |
| **P1** ✅ **XONG 26/08** | `ITL-CANON` **38 vị trí / 36 trường** + **lớp sổ**: 6 chép · 1 join · 5 `if`. *(1 phép đánh số cố ý **không** ở lớp sổ — `SEQUENCE` của DB cấp, `INV-I04a`)* | ~~P0~~ ✅ | ✅ **107 test** *(86 offline + 21 PG thật)* · ⭐ **chèn lùi ngày không đổi id** — và **DB từ chối** thao tác AS-IS *(`INV-I04a: itl_id dong bang, khong duoc doi`)* · `content_key` `UNIQUE` + test khoá **không chứa `source_row`** · `lint-imports` **4 kept** · 5 cổng xanh |
| **P2** ✅ **XONG 26/08** | **Adapter B** *(Cash/Bank)* + **`fls/oracle/`** *(ảnh chụp đóng băng, tự soi, đọc tăng dần)*. `ACC-1…4` | P1 | ⭐ **parity cả sổ 64.393/64.393 ô = 100,0000%** · **22 kỳ** · 0 ô lệch · 0 ô phải chuẩn hoá số. `fls/oracle/` **62 test** *(3 cổng SONG đã thấy đỏ thật)* + `adapters/bank.py` **19 test**; **205 test xanh** · `lint-imports` **6 kept**. ⭐ **Cập nhật cuối 26/08:** parity cả sổ **69.510/69.510 ô · 23 kỳ** *(bản `[Master]` mới owner dán — hết hụt kỳ)*; `fls/oracle/` **82 test**; `adapters/bank.py` **20 test**; **273 test xanh**. ⭐⭐ Và **LẦN NẠP THẬT ĐẦU TIÊN đã chạy**: `vào 10.100 = sổ 9.973 + loại 19 + rỗng 108`, chạy lại không nhân đôi — cú chạy đó **làm đỏ 6 lỗ** mà không test tự bịa nào bắt được *(xem cổng chung #8)* |
| **P3** ◐ **LÕI XONG 27/08** | **Adapter A + ghép PM** theo `10_PM_JOIN_ADAPTER_SPEC` **v0.2**. Đọc `fps_*` chỉ-đọc | P2 · `QĐ-ITL-20` | ⭐ **2.650 mối nối đã vào kho** *(`fls_itl.pm_line_id`, migration `0006`)* · **26 phép thử** · ghép theo **DÒNG** *(⛔ không theo phiếu — tiền đề v0.1 bị đo lật)* · **sáu hình dạng `A…F`**, mỗi hình một con số. ⚠ **Còn nợ, khai rõ:** `T-JOIN-06`/`07` **chưa có test** vì ba tầng `T0`/`T3`/`T4` bị chặn *(`GAP-ITL-56`/`57` chờ kế toán · `T4` chờ P4·P6)* — ⛔ đừng đọc *"26 test"* thành *"xong hết"* |
| **P4** ◐ **PHẠM VI PLAN XONG 27/08** | **API đọc** `/ledger` `/queue` `/journal` `/gates` + `fls_queue_event` + 2 view | P3 | ⭐ **Chạy thật qua HTTP: 10.030 dòng lật hết** · `DELETE /ledger` = **405** · `/gates` 3 ĐẠT · 0 không đạt · **5 CHƯA ĐO ĐƯỢC** · `tools/verify_cua_that.py` · **492 phép thử**. ⭐⭐ **Phạm vi theo lần nạp là BẮT BUỘC ở chữ ký hàm** *(`PhamVi` ⛔ không có mặc định)*, và **kết nối bị PostgreSQL chặn ghi** — máy **từ chối chạy** nếu không. ⚠ **Còn nợ, khai rõ chứ ⛔ không làm tròn:** `BA-07` §2 có **6 đường đọc nữa** *(`/queue/coverage` `/weekly` `/sources` `/mapping-master` `/le` `/queue/state`)* phần lớn **chờ bảng nguồn có dữ liệu**, cộng nhóm `/runs*` §4 ⇒ ⛔ đừng đọc *"P4 xong"* thành *"cửa đọc xong"* |
| **P5** ◐ **XONG 27/08 — kể cả `/match`** | **API ghi**: `/adjust` *(10 trường, `409` khi khác nguồn)* · `/reason` · `/defer` · `/match`. Append-only cưỡng chế | P4 | ⭐⭐ **Sửa là THÊM bút toán** — sau mọi phép ghi, ⛔ **không một ô nào của `fls_itl` đổi** *(`CR#5`: đặc tả `BA-07` §3 nói sai, đã sửa đặc tả)*. ⭐ `actor` **đến TỪ THẺ** *(gửi trong thân ⇒ 400)* · bút toán + nhật ký trong **MỘT giao dịch** *(chứng minh bằng trigger tạm làm nhật ký NỔ)* · **một CHỖ DUY NHẤT được ghi**, cưỡng chế bằng cổng quét mã nguồn · `409` khi khác nguồn kèm *"nguồn đang là gì"* · kỳ chốt **409 kể cả `force`** · đảo bút toán = **thêm** dòng. ⭐⭐ **`P5` ⛔ không làm yếu `P4`**: **bảng tuyến** chọn kết nối, nên đường `GET` **luôn** chạy trên kết nối bị PostgreSQL chặn ghi — đo bằng cách đếm số lần mở kết nối ghi = **0**. `tools/verify_cua_ghi.py` chạy cả vòng ghi qua HTTP. **548 phép thử**. ⚠ **Còn nợ, khai rõ:** `/match` + `/pm-candidates` **BỊ CHẶN** — chúng cần `fps_pm_slip`/`fps_pm_line` mà FLS ⛔ không có bảng đó trong kho *(`QĐ-ITL-45`)* ⇒ **`GAP-API-04`** chờ owner chọn; và **chốt kỳ/ký** vẫn chưa có đặc tả *(`GAP-PLAN-04`)* |
| **P5b** ✅ **GHÉP LỆNH XONG 27/08** | `GET .../pm-candidates` + `POST .../match` — hai đường **từng BỊ CHẶN** *(`GAP-API-04`)* | P5 · `QĐ-ITL-61` | ⭐⭐ **Owner chốt đường (a): lưu ẢNH CHỤP dòng lệnh vào kho** *(`fls_pm_line`, migration `0011`)*. Loại đường (b) *(đọc Sheets sống trong một đường HTTP)*: nguồn đo được là **chập chờn** *(timeout 3/3 lần)*, và một cửa treo vì mạng là cửa kế toán sẽ bỏ. ⭐ Ứng viên xếp **4 BẬC CÓ TÊN** *(`ma` › `tien` › `gan_tien` › `cung_tien_te`)* ⛔ không phải điểm số mờ — màn hình phải nói được **vì sao** phiếu này đứng đầu. ⭐ Trả kèm **TUỔI của ảnh chụp**: câu trả lời cho *"bản lưu già đi thì sao"* là **nói ra nó già bao nhiêu**. ⭐ `/match` ghi **THÊM** trong MỘT giao dịch *(`fls_pm_link` `hinh='T'` + sự kiện + bút toán `hd`/`cdt1`)*, sổ ⛔ không đổi một ô *(bài so 17 cột)*. `hd`/`cdt1` chỉ suy khi **cả N dòng lệnh ĐỒNG Ý**, N dòng nói N thứ ⇒ **khai là không suy được** *(`INV-I16`)*. ⛔⛔ **`CR#6` sửa đặc tả**: thân là `{pm_line_ids}` ⛔ không phải `{pm_id}` — 526 phiếu mang 2–36 reference khác nhau. **Chạy thật trên sổ thật**: nạp lại ⇒ `sổ 0 + trùng 10.030` *(⛔ không thêm dòng nào)* + ảnh chụp **3.703 dòng · 1.468 phiếu**; `/pm-candidates` đo trên **25 dòng hàng chờ thật**, `itl_id=1022` → `PM00688-2` bậc `ma`. Cổng đã diễn tập ĐỎ. **589 phép thử** · `pg_verify` **15 bảng/view** ⛔ **CÒN**: `GAP-JOIN-05` *(chưa có đường BỎ mối nối — ghép sai thì chưa sửa được)* · `GAP-JOIN-04` *(⛔ không xếp được theo ngày/payee)* · `GAP-CR1-04` *(dung sai tuyệt đối quá rộng cho cửa tay)* |
| **P6** | **FE 4 màn** `F01·F02·F03·F06` — ⭐ **kế hoạch chi tiết ở `DEV-12` v0.1** *(7 bước: thiết kế → bộ xương → `F03` → `F01` → `F02` → `F06`+2 cửa đọc → UAT)*. Bước 1 là **một lượt THIẾT KẾ ⛔ chưa code**; lưới dựng bằng **bảng HTML trần** *(`QĐ-ITL-66`)*; hệ thị giác **lấy nguyên từ `A-CCR`** *(`BA-06` §7)* | P5 ✅ *(gồm **bỏ mối nối** `QĐ-ITL-69` + **xong/mở lại** `QĐ-ITL-71`)* · ⛔ **không còn gì chặn** | **8 cổng DoD** `DEV-12` §5 — gồm 8 hành vi Sheets · 4 trạng thái mỗi màn · `web` ⛔ không gọi `repo`/`db` · ⛔ `dat=null` không trông như ĐẠT · ⭐ **UAT tuần đầu** *(cổng MÁY ⛔ không đóng được)* |

### Chưa xếp vào pha nào — và vì sao

| Việc | Chặn bởi |
|---|---|
| Adapter C *(A-CCR)* · D *(HR)* · E *(Platform)* | không chặn P0–P6; xếp sau khi P3 chứng minh khuôn adapter đúng |
| Adapter F *(AP/AR)* | `QĐ-ITL-03` — gói riêng |
| 4 ledger nền tảng *(15.517 ô, 69% phạm vi)* | ⛔ **`GAP-ITL-18`** — ranh giới L4 với engine ACA v2 **chưa ai quyết** |
| Công bố ra BQ | ⏸ `QĐ-ITL-46` hoãn |
| Đảo bút toán · chốt kỳ + ký | ⛔ **chưa có endpoint, chưa có màn** — lỗ đã nêu ở rà scope 26/08; phải bổ spec trước khi vào pha |

---

## §3 · Khuôn một pha — 5 bước, bước 4 là cổng

```
① Spec pha      → task + interface, không placeholder
② TDD từng task → test đỏ → code tối thiểu → test xanh → commit
③ Tích hợp      → chạy trọn pha trên PG container thật (⛔ không sqlite giả)
④ CỔNG ERD      → 4 cổng; đỏ ⇒ pha CHƯA xong, không thương lượng
⑤ Đồng bộ doc   → ERD sinh ra ghi vào 05_DATA_DICTIONARY_ERD + bump version + changelog
```

⭐ **Bước ⑤ là chỗ chống drift thật.** Cổng G-ERD-2 sẽ **đỏ** cho tới khi ERD của BA được cập nhật — nên doc không thể già đi trong im lặng nữa. Đây là điểm khác căn bản với cách làm cũ.

---

## §4 · Việc mở

| ID | Việc | Ai |
|---|---|---|
| ~~`GAP-PLAN-01`~~ | ~~Repo `FLS` chưa tạo~~ ✅ **ĐÓNG 26/08** — đã tạo tại `C:\Users\0_Apero Project\FLS`, `git init` + nhánh `feat/p0-foundation`, venv riêng, PG 16 container cổng **5433** | — |
| ~~`GAP-PLAN-02`~~ | ~~Bỏ `fls_id_counter`~~ ✅ **ĐÓNG 26/08** — `04_DB_IMPLEMENTATION` **v1.5** §5/§6 đã gạch, ghi rõ FPS *fix* bằng cách **bỏ** bảng counter; `11_INVARIANTS` **v0.6** sửa `INV-I04a` sang `SEQUENCE` | — |
| ~~`GAP-PLAN-03`~~ | ~~Viết lại §ERD + chốt \"view hay bảng\"~~ ✅ **ĐÓNG 26/08** — `05_DATA_DICTIONARY_ERD` **v0.7**: khối `erDiagram` giờ **sinh từ code** *(`tools/sync_erd_doc.py`)*, chốt `fls_itl` là **bảng ba lớp** không phải view, 6 entity ảo thành cột, 4 island có lý do | — |
| `GAP-ERD-P0-01` ⚠ | `fls_itl.run_id` là `NOT NULL` và trỏ tới `fls_run.run_id` nhưng **không có FK** ⇒ gõ sai `run_id` thì dòng sổ **mất lineage trong im lặng**, trái tinh thần `INV-I05`. Thêm FK sẽ bỏ được 2 trong 4 island. Phát hiện khi cổng `G-ERD-3` chạy thật | Tech Lead |
| `GAP-PLAN-04` | Đảo bút toán + chốt kỳ chưa có API/màn ⇒ bổ `07_API_CONTRACT` + `06_SCREEN_SPEC` trước khi tới pha tương ứng | BA |

---

## §5 · Definition of Done — chín module chính

> **Vì sao mục này tồn tại.** "Xong" ở dự án này đã từng nghĩa là *"code chạy không lỗi"* — và đó là cách một module hụt 22 dòng mà `row_counts` vẫn tự khớp, một khối tầng-2 chia sai suốt 3 ngày trong im lặng, một hợp đồng trôi từ 14 trường về 13. Nên mỗi module dưới đây có **ba phần**: điều kiện *xong*, **lệnh chạy được** để chứng minh, và ⛔ **điều kiện CHƯA xong** — viết từ chính những cái bẫy đã sập.
>
> Luật chung cho cả chín: **4 cổng ERD + cổng verify DB xanh** *(§1.3)*, `import-linter` xanh, file ≤ 300 dòng · hàm ≤ 40 dòng, và **0 dòng rơi im lặng**.

### 5.1 · `fls/db/` — schema SSOT · ✅ XONG (P0)

| | |
|---|---|
| **Xong khi** | ① schema khai **một lần** dạng dữ liệu Python, **sinh ra cả DDL lẫn ERD** — không có bản viết tay thứ hai. ② `pg_migrate --dry-run` in trọn DDL **offline**, không cần DB. ③ `pg_verify` so DB **thật** với schema khai báo *(cột · `NOT NULL` · FK)*. ④ Bất biến ở tầng DB có **trigger + test trên PG thật**: `INV-I03` · `INV-I04a` · `content_key UNIQUE` · FK `run_id`. ⑤ ERD của BA được **bơm bằng công cụ**, không sửa tay |
| **Cổng** | `pytest -q` · `lint-imports` · `python -m fls.db.pg_migrate --dry-run` · `PG_DSN=… python -m fls.db.pg_verify` · `erd_export --write && git diff --exit-code` |
| ⛔ **CHƯA xong nếu** | cổng **chưa từng thấy đỏ** *(phải cố tình làm nó đỏ một lần)* · còn bảng `fls_id_counter` · ERD sửa được bằng tay mà build vẫn xanh · migration báo *"đã áp N câu"* mà `pg_verify` lệch · **đổi `schema.py` mà không có migration** và build vẫn xanh · bảng có trong `TABLES` mà **không ai tạo** *(thiếu ở `CREATE_ORDER`, không khai `BOOTSTRAP`)* |
| **Di trú** ✅ | ⑥ **forward-only có số thứ tự + sổ ghi** `fls_migration`: `checksum` chống sửa migration đã áp · số thứ tự tăng đơn không hở · runner **tự chạy `pg_verify`** sau khi áp. ⑦ ⭐ **cổng nối hai nguồn**: schema PG **trống** → áp hết migration → `pg_verify` **phải xanh** *(`schema.py` = trạng thái mong đợi; `migrations/` = đường đi)*. ⑧ 5 cột `*_thyt` + `canon` **có trong migration đầu tiên** *(`QĐ-ITL-35`, có test khoá)* |

### 5.2 · `fls/contract/` — `ITL-CONTRACT` 14 trường · ✅ XONG (P0)

| | |
|---|---|
| **Xong khi** | ① hợp đồng là **DATA** *(bảng dữ liệu)*, không phải hằng rải trong code. ② **đúng 14 trường**, đọc **theo TÊN** *(`QĐ-ITL-42`)*. ③ `le` = cột **`P`**, và **`BL` không xuất hiện ở đâu** *(`QĐ-owner-0820`)*. ④ mọi trường hợp đồng **tồn tại thật** trong `fls_itl` với kiểu khớp |
| **Cổng** | `tests/contract/test_itl_contract_v1_lock.py` — chạy ở **mọi** milestone, không chỉ P0 *(`INV-I07`, rủi ro #1)* |
| ⛔ **CHƯA xong nếu** | số trường lấy từ **tài liệu** thay vì từ **code** — đúng cái đã làm hợp đồng trôi 14→13 ngày 24/08 · đổi file này mà không kèm test tương thích *(CR loại 3, `DEV-02` §4.5)* |

### 5.3 · `fls/canon/` — `ITL-CANON` 36 cột · ✅ XONG (P1)

| | |
|---|---|
| **Xong khi** | ① 36 cột lưu **theo VỊ TRÍ**, ⛔ **không theo tên** — có **4 cột `AH`–`AK` trùng tên hệt nhau**, lưu theo key là **mất cột**. ② tên trường **nguyên văn** nguồn, kể cả sai chính tả *(`R-A2`)*. ③ `validate()` phân biệt được **thiếu dữ liệu** *(→ `UNMAPPED`)* với **sai kiểu** *(→ `fls_reject`, lý do CÓ TÊN)*. ④ ngày là **`date`**, không phải chuỗi *(`INV-I11`)* — nguồn có **~5.369 dòng ngày dạng chuỗi**. ⑤ **không import `adapters`** |
| **Cổng** | fixture canon → 36 cột đúng vị trí · test 4 cột trùng tên vẫn phân biệt được · test ngày dạng chuỗi **không** lọt xuống sổ |
| ⛔ **CHƯA xong nếu** | có **bất kỳ** giá trị mặc định im lặng *(`INV-I16`)* — nguồn AS-IS sinh `GAC-Other`/`Headquarters2`/`VD0` bằng cách này, và đó là gốc của thùng rác `GAC-OTH` · một dòng bị loại mà **không có lý do bằng chữ** *(`ACC-4`)* |

### 5.4 · `fls/ledger/` — lớp sổ mỏng · ✅ XONG (P1)

| | |
|---|---|
| **Xong khi** | ① `itl_id` cấp lúc `staged` — **TRƯỚC** mapping — rồi **đóng băng** *(`INV-I04a`)*. ② **chèn lùi ngày không làm đổi id của bất kỳ dòng nào** — đây là cổng quan trọng nhất của cả module. ③ `content_key` `UNIQUE`, chỉ dùng để **đối sánh**, ⛔ không làm danh tính *(`INV-I04b`)*. ④ lineage `source_system`/`source_sheet`/`source_row` + 3 version **không NULL** *(`INV-I05`/`I12`)*. ⑤ đúng **6 phép chép · 1 đánh số · 5 câu `if` · 1 phép ghép** — nhiều hơn nghĩa là luật nghiệp vụ đã lẫn vào lớp sổ |
| **Cổng** | test chèn một dòng lùi ngày vào giữa sổ → **id mọi dòng khác không đổi** · `content_key` trùng bị chặn ở DB · chạy 2 lần cùng kết quả · ⭐ **parity trên dữ liệu THẬT**: `tests/ledger/test_parity_2026_03.py` — **4.088/4.088 ô** trên 584 dòng tháng 3/2026 |
| ⚠ **Đã sập một lần** | luật `Final` từng viết là `f(Classifying, **Manual input**)` — **sai**. Thật là **hai bước**: `MID = f(Classifying, Manual, mặc định RIÊNG của khối)` rồi `Final = f(Classifying, **MID**)`. Cổng parity trên dữ liệu thật bắt được: 6/7 khối khớp nhưng **khối 7 lệch 521/584**. Và **mặc định là một hằng riêng cho từng khối**, không dùng chung *(khối 4–5 **không có hằng** ⇒ `GAP-ORA-06`)*. ⇒ Bài học: **cổng chỉ đáng tin khi chạy trên dữ liệu thật**, test tự bịa đầu vào sẽ xanh với luật sai |
| ⛔ **CHƯA xong nếu** | id bám **vị trí dòng** — AS-IS làm thế *(`="ITL#"&ROW()` trên bảng đã SORT theo ngày)* và đó là gốc của **1.356 dòng `FALSE`** ở vùng AUDIT · lớp sổ chứa luật phân loại |

### 5.5 · `fls/repo/` — tầng truy cập DB · ◐ **85%** — đã CHẠY THẬT (P1 · P2 · P3)

| | |
|---|---|
| **Xong khi** | ① **chỉ `fls/repo/` và `fls/db/`** được import driver DB — cưỡng chế bằng `import-linter`, ⛔ không bằng nhắc nhở. ② SQL viết **nguyên văn**, không ORM sinh ngầm. ③ ghi vào `fls_*` là **APPEND** — không hàm nào phát `UPDATE`/`DELETE` lên `fls_itl` *(`INV-I08`)*. ④ **không có đường ghi nào** tới `fps_*` / P100 *(`QĐ-ITL-45`)*. ⑤ ⛔ **không đọc cột PII** *(Họ tên · CMND/CCCD/Passport)* |
| **Cổng** | `lint-imports` · test **quét** repo layer: không tồn tại câu `UPDATE`/`DELETE` nào nhắm `fls_itl` · test kết nối `fps_*` là read-only |
| ⛔ **CHƯA xong nếu** | một module khác import `psycopg` "cho nhanh" · có hàm nào ghi vào file Google của kế toán *(`QĐ-ITL-34`, sự cố 13/08)* |

### 5.6 · `fls/oracle/` — thước chuẩn · ◐ **95%** (P2)

| | |
|---|---|
| **Xong khi** | ① ảnh chụp **đóng băng** từ **FILE GỐC** `ITL Ledge`, chụp **cả đầu vào lẫn đầu ra trong cùng một lần đọc**, có `run_id` + ngày. ② **tự soi**: kiểm `Final == f(Classifying, U)` từng dòng; dòng không tự nhất quán ⇒ **loại khỏi oracle** *(bị gõ giữa hai lần đọc)*. ③ ⛔ **SỬA 26/08:** *"đọc có retry + cắt lát nhỏ hơn"* là **chữa sai bệnh**. Đo thật: workbook `ADJUSTED` **không trả được giá trị đã tính** — **một ô** cũng timeout, ở **mọi** sheet, mọi endpoint *(`GAP-ORA-08`)*. Hiện tượng *"4/7 khối mỗi buổi, khối trượt 3/3 lần"* **không phải kích thước lát** mà là **may mắn gặp lúc workbook còn ấm**. ⇒ Thước chuẩn chạy trên **hiện vật đóng băng**; cách gỡ dứt điểm là bản **"dán giá trị"** từ file gốc. ⚠ `timeout` ≤ **45s**, ⛔ không 300s *(một lần chờ vô vọng × nhiều lát = treo cả giờ, 0 dòng, 0 thông tin)*. ④ là **code có test**, ⛔ không phải script tạm |
| **Cổng** | chụp 2 lần cách nhau → checksum khớp · dòng cố tình làm không nhất quán bị loại · một khối lỗi **không** phá cả lần đọc |
| ⛔ **CHƯA xong nếu** | dùng `ITL_altered` *(sai **680 `HD`** + **1.048 `CDT`**)* · dùng **bản copy của `ADJUSTED`** *(nó **tự sản xuất giá trị mặc định** với **0 ô lỗi** — nguy hơn `#REF!`)* · ⚠ **ngoại lệ có căn cứ:** bản sao **RAW** `1md85t…` **được dùng** *(`QĐ-ITL-50`)* vì `Transaction Mapping L1` **giữ nguyên 6.648 ô `#N/A`** thay vì bịa — nhưng **chưa xong nếu thiếu 3 cổng tự kiểm** `G-ORA-LIVE-1/2/3` *(kỳ mới nhất cũ >45 ngày · tab nguồn 0 dòng · tỷ lệ ghép rơi khỏi 25–45%)* · dùng bản `.xlsx` xuất ra *(**~84 dòng mất mã** làm **bốc hơi 19,9 tỷ** mà tổng vẫn tự khớp; chỉ **2,7%** ô ngày còn nguyên kiểu)* |

### 5.7 · `fls/adapters/` — sáu nguồn A–F · ◐ **45%** *(B xong; **A xong hết phần máy làm được** — cả 3 hình ghép được đều đậu; còn C·D·E·F + 3 tầng chờ người)* (P2 · P3)

| | |
|---|---|
| **Xong khi** *(từng adapter)* | ① xuất đúng **36 cột** + `source_id` + provenance. ② **parity vs oracle 100% từng ô**, ⛔ **cấm dung sai**. ③ **row-count khớp sheet nguồn**; lệch phải **phân loại được**: lệch thật vs cash-vs-accrual hợp lệ. ④ **fail-loud khi schema nguồn đổi** — nổ to, không đoán. ⑤ **idempotent** — chạy lại không nhân đôi. ⑥ nguồn thiếu trường ⇒ để trống **có kiểm soát**, ⛔ không bịa *(`P-ITL-05`)* |
| **Riêng adapter A — ghép PM** | ⑦ **công bố tỷ lệ ghép TỪNG TẦNG** `T0…T5`, ⛔ không gộp thành một con số. ⑧ cổng `Σ`: tổng tiền các dòng lệnh **=** tiền dòng bank; lệch thì **chặn**, ⛔ không chia bừa *(`INV-I16`)*. ⑨ ghép theo **DÒNG lệnh + chia tiền + `line_id`**, ⛔ không `VLOOKUP` lấy dòng đầu. ⛔⛔ **Sửa 27/08 — câu cũ ở đây SAI:** ~~*"mã tham chiếu nằm ở **phiếu**, không ở **dòng**"*~~ và ~~*"cách cũ rơi im lặng **289 dòng**"*~~. Đo thật: mã **nằm ở DÒNG** — **526/1.468 phiếu mang 2–36 mã KHÁC NHAU**, tiền cũng khác nhau từng dòng; và con số **289 không tái lập được** ⇒ **rút** *(`CR#1-a`, spec `10` **v0.2 §1a**)*. ⑩ ⛔ **KHÔNG tách một dòng bank thành N dòng sổ** *(`T-JOIN-03` của v0.1)*: tách như thế **vỡ thế 1–1 giữa sổ và nguồn** mà cả bốn đường đối soát dựa vào, đổi lại chỉ **27 dòng** ⇒ hình `B` chờ bảng nối `fls_pm_link` *(`GAP-JOIN-03`)*, và trong khi chờ thì **vào hàng chờ kèm lý do có tên** |
| **Cổng** | 9 test `T-JOIN-*` · parity từng ô · test đổi tên một cột nguồn → adapter **nổ**, không âm thầm bỏ cột |
| ⛔ **CHƯA xong nếu** | tỷ lệ ghép công bố **cao hơn thực đo** · bảng đo lấy tử số và mẫu số **từ hai tổng thể khác nhau** *(đúng cơ chế đã tạo ra con số "100%" giả)* · ⭐⭐ **công bố MỘT con số ghép mà không nói kèm con số kia**: AS-IS `VLOOKUP` báo ghép **3.312 = 33,2%** nhưng **968 dòng trong đó (29%) KHÔNG KHỚP TIỀN**; ghép **đúng** *(qua cổng Σ)* chỉ **2.677 = 26,79%**. ⇒ **Luật công bố:** đưa **cả hai** cách đếm, vì con số đúng **nhỏ hơn** con số đang dùng và sẽ **trông như một bước lùi** — che nó đi là làm đúng cái bệnh này · **4.940 dòng tiền ra không có lệnh** *(`GAP-ITL-29`)* vẫn còn nguyên |

### 5.8 · `fls/api/` — cửa vào ra (P4 đọc ✅ · P5 ghi ✅ · ghép lệnh ✅ — tổng **85%**) 

| | |
|---|---|
| **Xong khi** | ① router **mỏng**, ⛔ **không chứa luật** — luật ở `ledger`/`canon`. ② **không endpoint `PUT`/`DELETE` nào** tới `fls_itl`; sửa **chỉ** bằng bút toán mới *(`INV-I08`)*. ③ mỗi lần ghi sinh **nhật ký `AUD-1` đủ 7 trường** — đây là **chỗ kiểm soát duy nhất còn lại** sau khi `QĐ-ITL-27` khai tử người hậu kiểm. ④ `409` khi giá trị đến từ nguồn khác. ⑤ AuthN/Z **fail-closed** |
| **Cổng** | test **quét route table**: không tồn tại `PUT`/`DELETE` nhắm `fls_itl` · mọi endpoint ghi có test kiểm nhật ký đủ 7 trường · test token hỏng → **từ chối** |
| ⛔ **CHƯA xong nếu** | có bước **duyệt của người thứ hai** — `QĐ-ITL-16` bỏ bước duyệt, `QĐ-ITL-27` khai tử vai đó; dựng ra một nút không ai bấm là **tệ hơn không có** · thiếu cửa cho **đảo bút toán** và **chốt kỳ/ký** *(`GAP-PLAN-04`: có máy trạng thái mà không có cửa, không có màn)* |

### 5.9 · `fls/web/` — bốn màn hình (P6)

| | |
|---|---|
| **Xong khi** | ① 4 màn `F01` *(hàng chờ + Ghép lệnh)* · `F02` *(sổ ITL)* · `F03` *(cổng hôm nay)* · `F06` *(danh mục · nguồn)*, cộng khay **Nhật ký** xuyên suốt. ② **8 hành vi Sheets bắt buộc** *(`BA-06` §1)* đều có — thiếu một cái là kế toán về Sheets. ③ **spike lưới đạt TRƯỚC khi code màn** *(`GAP-SCR-03`)*. ④ lệch `Σ` thì nút xác nhận **bị chặn** |
| **Cổng** | test DOM cho từng hành vi bắt buộc · test nút xác nhận bị chặn khi `Σ` lệch |
| ⛔ **CHƯA xong nếu** | **2–3 kế toán không dùng** — đây là **rủi ro số một của cả dự án**, và là **hành vi**, không phải kỹ thuật. Màn đẹp mà họ về Sheets thì module này **chưa xong**, dù test xanh hết |

### 5.10 · Cổng chung — module nào cũng phải qua

| # | Điều kiện | Đo bằng |
|--:|---|---|
| 1 | 4 cổng ERD + cổng `pg_verify` **xanh** | `pytest` · `pg_verify` |
| 2 | `import-linter` **0 vi phạm** | `lint-imports` |
| 3 | **0 dòng rơi im lặng** — mọi dòng vào sổ, hoặc vào `fls_reject` có lý do, hoặc vào hàng chờ `UNMAPPED` | test đối chiếu số dòng cả ba đường |
| 4 | Chạy 2 lần **cùng kết quả** | test idempotent |
| 5 | Tài liệu BA đã đồng bộ *(bước ⑤ của khuôn một pha)* | `G-ERD-2` **đỏ** cho tới khi làm xong |
| 6 | **Cổng của module đã từng thấy đỏ một lần** | có commit chứng minh |
| **7** ⭐ | **Cổng phải chứng minh nó ĐÃ ĐO ĐƯỢC GÌ**, ⛔ không chỉ chứng minh *"không thấy lỗi"* | `fls/oracle/cong_parity.py` — mặc định **KHÔNG ĐẠT**; ngưỡng số ô + đối chiếu số dòng + đếm lát bị bỏ |
| **8** ⭐ | **Đã CHẠY THẬT một lần trên NGUỒN ĐẦY ĐỦ** — ⛔ không chỉ chạy test | có lệnh chạy được *(`tools/nap_that.py --that`)* + in ra con số **bốn đường** |
| **9** ⭐ | **Đếm GIÁ TRỊ, ⛔ không chỉ đếm DÒNG** — một lát đọc **hợp lệ** vẫn có thể **thiếu giá trị** | `fls/oracle/doc_du.py` — đọc lại **6 cột then chốt** bằng câu **RIÊNG theo CỘT** rồi so số ô có giá trị, **+ ngưỡng SÀN** từng cột; mặc định **KHÔNG ĐẠT** |
| **10** ⭐⭐ | **Kho THẬT và kho TEST phải là HAI KHO** — ⛔ bộ test không được ghi vào sổ | `fls/db/kho.py` *(`dsn_test()` **NỔ** nếu trỏ vào kho thật)* · `fls/repo/kho_sach.py` + `tools/kiem_kho.py` *(kho thật chỉ được chứa `run_id` khớp `NAP-yyyy-mm-dd-NGUỒN` **và NGÀY nằm trong khoảng sống của sổ**)* · test **quét mã nguồn** chặn người sau gõ lại địa chỉ cũ |
| **11** ⭐⭐ | **Cổng phải so HAI phép đo ĐỘC LẬP** — ⛔ so một con số với **chính nguồn sinh ra nó** là cổng **vòng tròn**: nó không bao giờ đỏ, nên nó không bao giờ nói gì | Đối chiếu chéo hai đường sinh khác nhau *(vd `la_run_that()` Python **vs** toán tử `~` của PostgreSQL trên **cùng một chuỗi mẫu**)*; ⛔ cấm so `X` với `count(X)` |
| **12** ⭐⭐ | **Một cổng chỉ được XOÁ khi bất biến nó canh đã hết hiệu lực.** ⛔ Xoá một cổng **để tính năng mới đi qua** ⇒ cổng đó chưa từng canh gì: nó khoá một **trạng thái tạm thời**, không phải một **bất biến** | Mỗi lần xoá/sửa một cổng: viết ra **bất biến nào** vừa hết hiệu lực, và **cổng nào thay nó**. Nếu không có cổng thay ⇒ đang mất một lớp bảo vệ |
| **13** ⭐⭐ | **Một con số đo được, chép ở ≥2 file, phải có MỘT phép so nối chúng.** ⛔ Cổng nằm **trong** từng file *(version vs changelog, bảng vs bảng)* ⛔ không bắt được bản chép **thứ hai già đi**: đợt sync đi theo **danh sách file**, file ngoài danh sách im lặng lạc hậu | ✅ **CÓ MÁY 28/08** — `tools/kiem_so_song.py` *(repo `FLS`)*: **43 phép so** trên 4 file, **12 phép thử**, `GAP-DOC-04` đóng. ⛔ **Còn hở** `GAP-DOC-05`: cổng chỉ canh **chỗ đã khai** |

> ⛔ **Cổng thứ 7 sinh ra từ một lần cổng NÓI DỐI, 26/08.** `tools/verify_parity_all.py` chạy lần đầu: cả 3 lát đọc bị `503/500`, đọc **0 dòng**, so **0 ô** — rồi in *"0 Ô LỆCH trên cả sổ — luật `Final` tái hiện ĐÚNG 100% từng ô"* và trả **PASS**.
>
> **Sáu cổng trên không cái nào bắt được** chuyện này: cả sáu đều hỏi *"có thấy lỗi không?"* — mà không đo gì thì tất nhiên không thấy lỗi. Cổng chạy trên **hạ tầng có thể fail** *(mạng · quota · API 503)* phải trả lời thêm một câu: **"mày đã đo được bao nhiêu?"**
>
> Áp cho mọi cổng sau này đọc nguồn ngoài: ⓐ **ngưỡng tối thiểu** *(dưới ngưỡng ⇒ đỏ)* · ⓑ **đối chiếu số dòng** với con số đã đo độc lập *(hụt quá sai số ⇒ đỏ)* · ⓒ **đếm phần bị bỏ** *(có lỗ trống ⇒ ⛔ không được nói "cả sổ")*.

> ⛔⛔ **Cổng thứ 13 sinh ra từ chính đợt đồng bộ tiến độ, 27/08 — và lần này cái già đi là BỘ TÀI LIỆU, không phải code.** `08_MIGRATION_ROADMAP` bước 4 lạc hậu **9 con số cùng lúc** *(`360 test · 3.778 dòng · 10 cổng · lint 6 kept · kho 9.973 · 2.650 mối nối · 49% · `DEV-04` v1.5 · `DEV-03` v1.8`)*, trong khi số thật là **548 · 5.780 · 12 · 7 kept · 10.030 · 2.745 · 63% · v1.6 · v2.3**. Bản vẽ kiến trúc lạc hậu **4 con số**.
>
> ★ **Lý do không phải "quên"** — và đây mới là chỗ đáng học: hai đợt `P4`/`P5` **đều** chép số mới, nhưng chỉ chép vào **danh sách file mà đợt đó đi qua** *(`06_DASHBOARD` · `DEV-03` · bản vẽ)*. File nào không có trong danh sách thì **không ai chạm**, và ⛔ **không cổng nào so số giữa hai file** — cả `K1..K5` đều là phép kiểm **bên trong một file** hoặc đếm hai danh sách.
>
> ⇒ Luật: con số đo được **chỉ nên có MỘT chỗ ghi**, chỗ khác thì **trỏ tới**. Chỗ nào buộc phải chép thì phải có phép so nối. ⛔ Cơ chế **chưa dựng** *(`GAP-DOC-04`)* — ghi ra ở đây để lần sau ⛔ không ai tưởng luật này đã có cổng canh.
>
> ⛔⛔ **Cổng thứ 12 sinh ra từ chính bộ test của `P4`, 27/08.** `P4` có bài `test_P4_CHI_DOC_khong_mot_duong_ghi_nao` — *"không tuyến nào là `POST`"*. Bài đó **đúng lúc đó nhưng sai luật**: nó khoá một **trạng thái tạm thời** *(chưa có đường ghi)* thay vì một **bất biến** *(⛔ không đường nào được sửa sổ)*.
>
> Đến `P5` nó **bắt buộc phải xoá** — và một bài bị xoá để tính năng mới đi qua là **một bài chưa từng bảo vệ gì**.
>
> ★ Thay bằng bài khoá điều **không bao giờ đổi**: `fls_itl` là append-only, nên ⛔ không tuyến nào — **dù phương thức gì** — được GHI vào nó. Và đó cũng là chỗ bịt **một lỗ THẬT của `P4`**: cổng cũ kiểm theo **phương thức** *(`PUT`/`DELETE`/`PATCH`)*, nên một `POST .../adjust` ghi thẳng vào `fls_itl` sẽ **đi qua trong im lặng** — mà `BA-07` §3 còn viết *"trường hợp-đồng cập nhật `*_thyt`"*, tức là đường đó **đã được đặc tả mở sẵn**.
>
> ⇒ Khai tường minh `bang_ghi` cho từng tuyến, và cổng chặn `fls_itl` ở **mọi** phương thức.

> ⛔⛔ **Cổng thứ 11 sinh ra từ một cổng NÓI DỐI theo kiểu mới, 27/08 — và lần này nó nói dối bằng cách ĐỎ.** Cửa đọc `P4` có một cổng tên `BON_DUONG` so `fls_run.row_count` với `count(fls_itl) + count(fls_reject)`. Lần chạy thật đầu tiên nó **ĐỎ**: `10.030 ≠ 10.030 + 19`.
>
> Nhưng **đỏ GIẢ**. Đọc `chay_nap.dong_run()` mới thấy: `row_count` **được ĐẾM TỪ CHÍNH BẢNG `fls_itl`** — nên phép so đó là **vòng tròn**, và công thức `+ loai` là thứ tôi **tự suy ra từ chữ *"bốn đường"* trong tài liệu** mà ⛔ không đọc xem cột đó **thực sự chứa gì**.
>
> ★ Hai bài học khác nhau, cả hai đều mới: ⓐ một cổng so `X` với nguồn sinh ra `X` thì **không bao giờ đỏ** — cổng #7 bắt *"có đo gì không"*, cổng #11 bắt *"hai số có ĐỘC LẬP không"* · ⓑ **bốn đường thật sự KHÔNG đo được từ kho**: `rỗng` và `trùng` ⛔ không được lưu ở bảng nào, chúng chỉ in ra lúc chạy `nap_that.py` rồi mất *(`GAP-API-03`)*. ⇒ Nay tách làm hai: `RUN_DEM_KHOP` *(đo được — nó bắt **kho bị đổi sau lần nạp**)* và `BON_DUONG` = **CHƯA ĐO ĐƯỢC**, kèm lý do.
>
> ⚠ Và cổng `tools/verify_cua_that.py` in *"KHÔNG ĐẠT `BON_DUONG`"* rồi vẫn tự kết luận **✅ ĐẠT** — vì nó chỉ kiểm số cổng *"chưa đo được"*. **Một cổng báo một cổng khác đỏ rồi tự nói mình đạt là cổng vô nghĩa.** Đã sửa.

> ⛔⛔ **Cổng thứ 8 sinh ra từ LẦN NẠP THẬT ĐẦU TIÊN, 26/08.** Lúc đó module `adapters` có **20 phép thử xanh**, `ledger` có **64**, `repo` có **17**, và cả bảy cổng trên đều xanh. Rồi chạy `tools/nap_that.py --that` một lần trên nguồn đầy đủ, và nó **làm đỏ SÁU LỖ**:
>
> ⓵ luật *"ô lỗi là chuỗi bắt đầu bằng `#`"* ném **7 giao dịch THẬT** vào `fls_reject` vì kế toán gõ `##LAI NHAP VON#` · ⓶ `fls_le` **rỗng** mà `fls_itl.le` FK tới nó · ⓷ nguồn mang **hai hình** cho cùng một pháp nhân *(`'VGOH'` vs `'VGOH - APERO HQ'`)*, cả hai đều FK ⇒ một pháp nhân thành **hai dòng danh mục** · ⓸ `svc_*` khai `date` mà sổ là **KỲ dạng text** · ⓹ ⭐ **hàng chờ rỗng**: 6.634 dòng không có `hd` mà `work_status` đếm được **0** · ⓺ `autocommit` để lại **394 dòng đã commit** sau một lần nổ giữa đường, `fls_reject` **nhân bản** mỗi lần chạy lại, `row_count` bị lần chạy lại ghi về **0**.
>
> ★ **Vì sao 101 phép thử không bắt được cái nào:** cả 101 đều **tự bịa đầu vào**. Đầu vào tự bịa thì sạch — không có ai gõ `#` vào ô diễn giải, không có bảng danh mục rỗng, không có hai hình cho một mã, không có `'tháng 5'` trong ô kỳ. **Nguồn thật là thứ duy nhất biết những chuyện đó.** ⇒ Một module chưa chạy thật lần nào là một module **chưa biết nó có sống**, y như một cổng chưa từng thấy đỏ.

> ⛔⛔⛔ **Cổng thứ 9 sinh ra từ một lỗ IM LẶNG, 27/08 — và đây là cái cổng thứ 7 KHÔNG bắt được.** Lần nạp thật ghi **257 giá trị `svc_start` ÍT HƠN** chính dữ liệu đó khi tính lại offline.
>
> **Sổ không đổi:** đọc lại cả sheet 2 lần cách nhau vài giờ ⇒ **0 ô khác nhau**. Lát đọc **hợp lệ**: đúng số cột, đúng số dòng, **0 lỗi HTTP**. 257 ô về rỗng và **không cái gì báo gì**.
>
> ★ **Bốn cổng đã có đều im, mỗi cái vì một lý do riêng:** cổng hình dạng *(chỉ so tiêu đề, nó không đọc dữ liệu)* · cổng bốn đường *(đếm **DÒNG**, và số dòng vẫn cân)* · cổng Σ *(`svc_*` không phải tiền)* · `pg_verify` *(so schema, không so dữ liệu)*. Cổng **#7** cũng không đủ: nó bắt *"đo được bao nhiêu **dòng**"*, còn đây là *"đo được bao nhiêu **giá trị trong một cột**"* — **hai trục khác nhau**.
>
> ⚠ **Cơ chế là GIẢ THUYẾT, ⛔ chưa chứng minh:** `IMPORTRANGE` của tab nguồn còn đang nạp. Bằng chứng phụ: ở đuôi sổ, cột từ `PM_Unpivot` về **551** giá trị bình thường còn cột từ `PI_Unpivot` chỉ **21/278** — **một tab ấm một tab lạnh**, ⛔ không phải cả lát bị cắt.
>
> ★ **Nửa đáng tin của cổng là NGƯỠNG SÀN** *(2.111 < sàn 2.300 ⇒ chặn chắc, không cần biết cơ chế)*; **đọc-hai-lần là dây an toàn**, nó chỉ bắt được khi hai lần đọc lệch nhau. ⇒ Áp cho mọi cổng đọc nguồn ngoài: khai **sàn cho từng cột then chốt**, ⛔ đừng tin *"số dòng khớp"* là *"dữ liệu đủ"*.

> ⛔⛔⛔ **Cổng thứ 10 sinh ra vì BỘ TEST ĐANG GHI VÀO SỔ THẬT, 27/08.** Đếm `fls_itl` ra **11.177 dòng** trong khi mọi tài liệu ghi **9.973**. Truy ra: **năm file test PG lấy MẶC ĐỊNH đúng địa chỉ kho thật** — biến môi trường trỏ được đi nơi khác, nhưng **không gì bắt buộc**, nên một lệnh `pytest` trơn ghi thẳng vào sổ.
>
> ```
> fls_itl   : 9.973 THẬT + 1.204 dấu test   (1.285.475.949 tiền BỊA cạnh 1.214 tỷ tiền thật)
> fls_reject:    19 THẬT +   106 dấu test
> fls_run   :     1 THẬT +   227 lần chạy test
> hàng chờ  : 7.625 THẬT +   194 dấu test
> ```
>
> ★ **Con số trong mọi tài liệu VẪN ĐÚNG** — chúng được tính **có lọc** theo lần nạp. Chỗ hỏng là **không gì bắt buộc phải lọc**. Và `P4` *(cửa đọc)* + `P6` *(màn `F01`)* đọc **đúng bảng này** ⇒ **màn hình đầu tiên kế toán nhìn thấy sẽ có 194 dòng bịa trong danh sách việc phải làm**, không cổng nào báo gì. ⇒ **Phải chặn TRƯỚC `P4`**, vì sau khi có cửa thì mọi thứ đọc qua cửa, và lúc ấy sửa là sửa cả tầng trên.
>
> **Ba tầng chặn, cố ý xếp từ cứng xuống mềm:**
>
> ⓵ `dsn_test()` **NỔ** nếu kết quả trỏ vào tên kho thật — kể cả khi ai đó đặt `PG_DSN_TEST = PG_DSN`. Chặn cứng, ⛔ không phải lời khuyên.
> ⓶ Test **cố ý** phải soi kho thật *(`test_pg_verify`: kho phải khớp bản khai)* thì mở bằng **kết nối CHỈ ĐỌC** — **PostgreSQL tự từ chối** mọi phép ghi. ⭐ Chốt này **bắt được ngay** một bài đang `CREATE TABLE` thẳng vào kho thật mà không ai thấy *(`test_verify_bat_duoc_cot_bi_thieu`)* — tức nó **thấy đỏ THẬT trong lần đầu tiên bật lên**.
> ⓷ Test **quét mã nguồn** chặn người sau gõ lại dòng cũ. ★ Sửa 5 file là sửa **lần này**; cùng họ với lỗ *"luật ô-lỗi từng có BỐN bản sao"* — không sửa bản sao, mà làm cho bản sao mới **không thể tồn tại**.
>
> ⭐ **Luật của cổng là BẢN TRẮNG, ⛔ không phải bản đen:** một lần nạp là thật khi `run_id` khớp `NAP-yyyy-mm-dd-NGUỒN`; mọi thứ khác trong kho thật là **vi phạm**. Bản đen *(loại `T-%` và `r1` ra)* sẽ hỏng ngay lần sau có một tiền tố test mới — và hỏng trong im lặng.
>
> ⚠ **Dọn 1.204 dòng đã có thì ⛔ KHÔNG dùng `DELETE`** — `INV-I08` append-only. Câu `DELETE FROM fls_itl WHERE run_id LIKE 'T-%'` dọn được đúng chỗ nhưng **để lại một đường xoá sổ trong mã nguồn**, và lần sau khi cần dọn thứ khác thì đường đó đã có sẵn. Đường đúng là **DDL** *(bỏ cả kho rồi dựng lại rỗng + nạp lại từ NGUỒN)*, và nó **không lùi được** ⇒ `GAP-KHO-01` **chờ owner**. ★ Kèm một cái đáng giá: `tools/sao_luu_kho.py --so-sanh` kiểm **một tính chất chưa ai kiểm** — sổ này có **dựng lại được từ nguồn** hay không *(checksum NỘI DUNG, ⛔ bỏ `itl_id` vì số ấy cấp lại mỗi lần nạp)*.

## Changelog
- **v2.9** (2026-08-28): hàng `P6` trỏ sang **`DEV-12` — kế hoạch chi tiết bốn màn** *(v0.1, viết **trước khi** gõ một dòng code màn hình theo yêu cầu owner)*. ⭐ Thứ tự 7 bước có **lý do đo được**: `F03` đi trước vì nó **nhỏ nhất nhưng đi trọn vòng** *(sai kiến trúc thì sai ở màn 200 dòng, ⛔ không phải màn lưới 2.000 dòng)*; `F01` trước `F02` vì nó là **việc hằng ngày**; `F02` gần cuối vì **đắt nhất và hưởng lợi từ ba bước trước**. ⭐⭐ **Bước 1 là một lượt THIẾT KẾ ⛔ chưa code** — lớp lỗi owner bắt trong **30 giây** *(5/10 trường ⛔ không gõ được, tiêu đề in bằng chữ cái)* là lớp lỗi của **thiếu thiết kế**, ⛔ không phải thiếu phép thử. ⛔ Và `DEV-12` §5 khai thẳng: **cổng số 8 (UAT) MÁY ⛔ KHÔNG ĐÓNG ĐƯỢC** — để ⛔ không ai đọc *"680 phép thử xanh"* thành *"màn hình đã tốt"*.
- **v2.8** (2026-08-28, `QĐ-ITL-69`/`QĐ-ITL-70`): ⭐⭐⭐ **`P6` ⛔ KHÔNG còn gì chặn.** Điều kiện vào `P6` của v2.7 là `GAP-JOIN-05` *(đường **bỏ mối nối**)* — nay **đóng** *(`POST /queue/{itl_id}/unmatch`, migration `0013`, `CR#9`)*. Cùng đó `GAP-SCR-03` **hạ hẳn** *(kế toán 2/2 xác nhận đủ trường — `QĐ-ITL-68`)* và dung sai cửa tay đã chốt *(`QĐ-ITL-63`)*. ⇒ `P5` ✅ **xong hẳn**, `repo` **100%**. ⭐ Việc **đầu tiên** của `P6` là **một lượt thiết kế** *(theo `FLS-Wireframe` + `Demo-MVP`, dùng lại token/handoff UIUX của `A-CCR`)*, ⛔ không phải gõ code lưới ngay. ⚠ **Nên giải trong `P6`, ⛔ không chặn:** `GAP-JOIN-06` — hàng chờ ⛔ không tự nhả một dòng đã chữa xong; nó cần **câu trả lời nghiệp vụ** *(máy thấy đủ 5 trường, hay người bấm "xong"?)*, ⛔ không phải một dòng code.

- **v2.7** (2026-08-28, `QĐ-ITL-66`/`68`): **`P6` viết lại điều kiện vào** — ⛔ không còn *"spike lưới trước"* *(spike xong: lưới dùng **bảng HTML trần**, `QĐ-ITL-66`)*. `P6` = **FE 4 màn theo `FLS-Wireframe` + `Demo-MVP`, có một lượt thiết kế** *(dùng lại token/handoff UIUX của `A-CCR`, ⛔ không thiết kế lại)*. ⛔ Điều kiện vào nay chỉ còn **một**: `GAP-JOIN-05` *(đường bỏ mối nối)* — mở màn hàng chờ mà thiếu nó là giao cho kế toán một cái nút ⛔ không có đường lùi. ★ Và **`GAP-SCR-03` hạ hẳn**: kế toán (2/2) đã xác nhận **đủ trường**; ba thứ còn lại *(cảm giác · thời gian vẽ · 346px)* chuyển vào **UAT tuần đầu** — đo trên một **tệp thô** thì chỉ ra cảm giác của **tệp thô**.
- **v2.6** (2026-08-28): ⭐⭐⭐ **Cổng chung #13 từ *luật viết ra* thành MÁY** — `tools/kiem_so_song.py`, **43 phép so** trên 4 file, **12 phép thử**, đóng `GAP-DOC-04`. Sinh ra vì đo lại bộ tài liệu **19 giờ** sau đợt sync trước và thấy **20 con số đã lệch**, gồm cả hai chỗ vừa sửa hôm qua. ★ Bài học chép vào đây vì nó là luật cho mọi cổng sau: **một cổng chỉ tồn tại bằng lời văn là một cổng chưa tồn tại** — cổng #13 có lời văn từ 27/08 và bộ tài liệu vẫn lệch 20 con số ngay hôm sau. ⛔ Kèm một hướng **bị loại**: phép kiểm thuần giấy *(bảng có dòng `TỔNG` phải cộng đúng)* — **4/5 lần đỏ giả**, vì trên giấy ⛔ không phân biệt được *KHAI một con số* với *GHI LẠI con số của người khác*. ⚠ Mở `GAP-DOC-05`.
- **v2.5** (2026-08-27): ⭐⭐ **GHÉP LỆNH mở được — hai đường từng BỊ CHẶN nay đã chạy thật** *(`QĐ-ITL-61`, đóng `GAP-API-04`)*. Owner chốt **đường (a)**: lưu **ảnh chụp** dòng lệnh vào kho *(`fls_pm_line`, migration `0011`)*, ⛔ không đọc Sheets sống trong đường HTTP. §5.8 **75% → 85%**. ⛔⛔ Kèm **`CR#6`**: thân `/match` là `{pm_line_ids}` ⛔ không phải `{pm_id}` — cùng loại sửa đặc tả với `CR#5`. ⛔⛔ **Hai lỗ chính bộ test bắt được:** ⓐ `ghep_lenh` **⛔ không kiểm lý do** *(`_them` có kiểm nhưng nó chỉ chạy khi có `hd`/`cdt1` để ghi, còn `_them_su_kien` thì không)* ⇒ một phép ghép **không lý do** đi qua được, vết mang `reason` rỗng; ⓑ ⚠ **dung sai 1.000 VND tuyệt đối làm HAI bài test của tôi xanh SAI trong một buổi** — con số đó được đo và duyệt trên phép ghép **TỰ ĐỘNG** *(khoảng lệch lớn nhất thật: **2,00 đồng**)*, còn trên cửa **tay** thì nó cho ghép `100 VND` với `1.099 VND` = lệch **999%** ⇒ **`GAP-CR1-04`**, câu hỏi cho kế toán trưởng, ⛔ tôi không tự đặt ngưỡng tỷ lệ. ⭐ Cổng quét mã nguồn mở rộng: `fls_pm_link` chỉ được ghi ở **HAI chỗ đã khai** *(bộ nạp = máy · cửa ghi = người)*, kèm bài chứng minh **cả hai** thật sự có ghi. Mở `GAP-JOIN-04`/`GAP-JOIN-05`. **589 phép thử** · `pg_verify` **15 bảng/view**.
- **v2.4** (2026-08-27, đợt đồng bộ tiến độ): ⭐ **Thêm cổng chung #13** — *một con số đo được, chép ở ≥2 file, phải có MỘT phép so nối chúng*. Sinh ra vì `08_MIGRATION_ROADMAP` bước 4 lạc hậu **9 con số cùng lúc** và bản vẽ kiến trúc lạc hậu **4 con số**, dù hai đợt `P4`/`P5` đều đã chép số mới — chúng chỉ chép vào **danh sách file mà đợt đó đi qua**. ⛔ **Cơ chế cho #13 CHƯA dựng** *(`GAP-DOC-04`)*, chỉ là luật viết ra. ⭐⭐ Cùng đợt: **cổng tài liệu lên 5 phép kiểm** — `K5` chặn **ngày chưa xảy ra**, sinh ra từ **54 chỗ / 16 file** ghi `28/08` cho việc làm **27/08 13:56–17:49** *(bốn phép kiểm cũ xanh suốt vì không phép nào kiểm ngày)*. `K5` **đỏ giả 30 lỗi rồi xanh giả một lần** trước khi sống — nó bỏ sót **đúng ô đã lệch thật** vì mẫu đòi `**Cập nhật:**` mà file ghi `**Cập nhật lần cuối:**`. Mở **`GAP-DOC-03`** *(`DEV-05` API vẫn là bản copy chương trình trong khi cửa API đã chạy thật)* + **`GAP-DOC-04`**.
- **v2.3** (2026-08-27): ⭐⭐ **`P5` cửa GHI — sửa là THÊM bút toán, ⛔ không sửa ô nào của sổ.** Kèm **`CR#5`**: `BA-07` §3 *("trường hợp-đồng cập nhật `*_thyt`")* sai `INV-I08` **và** `QĐ-ITL-35` ⇒ **sửa đặc tả**, giá trị người gõ vào `fls_adjustment` + khung xem `fls_sua_tay` *(migration `0010`)*. `actor` **từ THẺ**; bút toán + nhật ký **một giao dịch**; **một chỗ duy nhất được ghi** *(cổng quét AST)*; `409` khác nguồn; kỳ chốt `409` kể cả `force`; đảo bút toán = thêm dòng. §5.8 **40→75%** · §5.5 `repo` **90→95%**. ⭐ **Thêm cổng chung #12** *(một cổng chỉ được xoá khi bất biến nó canh đã hết hiệu lực)* — sinh ra từ chính bài `test_P4_CHI_DOC_khong_mot_duong_ghi_nao`, và nó bịt **một lỗ THẬT của `P4`**: cổng cũ kiểm theo **phương thức** nên `POST .../adjust` ghi vào `fls_itl` sẽ đi qua **im lặng**. Mở **`GAP-API-04`** *(`/match` chặn: `fps_pm_line` không nằm trong kho `fls_*`)*. **548 phép thử** · `pg_verify` **14 bảng/view**.

- **v2.2** (2026-08-27): ⭐⭐ **`P4` cửa ĐỌC — phạm vi theo lần nạp CƯỠNG CHẾ Ở CHỮ KÝ HÀM.** 6 đường `GET`, thẻ fail-closed *(HS256 tự viết, bản **trắng** một thuật toán, bắt buộc `exp`)*, bảng tuyến **khai một lần → sinh cả máy định tuyến cả cổng quét**, và máy **từ chối chạy** nếu ⓐ thiếu khoá ⓑ **kết nối còn ghi được** ⓒ bảng tuyến vi phạm. §5.8 **0→40%** *(⛔ không phải 100: `BA-07` §2 còn 6 đường đọc + nhóm `/runs*`)* · §5.5 `repo` **85→90%**. ⭐ **Thêm cổng chung #11** *(so hai phép đo ĐỘC LẬP)* — sinh ra từ một cổng **đỏ GIẢ**: nó so `row_count` với `count()` trong khi `row_count` **được đếm từ chính bảng đó**. ⛔ **`CR#4`: bỏ khung xem `fls_queue_xep_tien`** *(migration `0009`)* — khung xem SQL không nhận tham số nên ⛔ không mang được phạm vi. Mở **`GAP-API-03`** *(bốn đường ⛔ không đo được từ kho: `rỗng`/`trùng` không lưu ở đâu)*. **492 phép thử** · `lint-imports` **7 kept** *(thêm ràng buộc `fls.api` ⛔ không được biết `fls.db`)*.

- **v2.1** (2026-08-27): Đồng bộ tiến độ đo được: **360 phép thử** · **3.778 dòng** `fls/` · **10 cổng chung** · **49%**. Hai con số **do người phán đoán** được đổi, **kèm lý do ghi ngay tại chỗ khai** *(nhật ký trong `tools/tien_do.py`)*: `§5.5 repo` **78→85%** *(+cổng kho-sạch, +chèn mối nối, +cổng Σ; còn lại là đường ghi cho `P5`)* · `§5.7 adapters` **40→45%** *(hình `B` đậu được; còn 4 bộ nạp + 3 tầng **chặn ngoài**)*. ⛔ `db` **giữ 100%** dù vừa thêm khoá nhiều cột — DoD đã đạt từ trước, không có chỗ để tăng. ⚠ Chặng **giữ 3,5/7**, ⛔ **không làm tròn lên 4/7**: DoD của `P3` đòi test cho `T0`/`T3`/`T4` mà hai tầng chờ kế toán — **dời việc bị chặn sang pha khác là cách dễ nhất để bảng tiến độ nói dối**.

- **v2.0** (2026-08-27): ⭐⭐ **`GAP-JOIN-03` + `GAP-DB-P0-03` ĐÓNG.** Bảng nối **`fls_pm_link`** *(migration `0007`, khoá **hai cột** `(itl_id, pm_line_id)`)* ⇒ hình `B` **đậu được**; cột `fls_itl.pm_line_id` **BỎ** — mối nối chỉ còn **MỘT chỗ**, vì giữ cả cột lẫn bảng là **hai bản sự thật**. Di trú chuyển **2.650 mối nối cũ** trên kho thật, **Σ lệch 0**. ⛔ **Cổng Σ CHẶN trước khi ghi**: Σ tiền mối nối = tiền dòng bank, lệch thì NỔ và ⛔ không ghi dòng nào. Khuôn `fls/db/model.py` thêm `pk_cols`/`unique_keys` + luật **cấm khai khoá hai chỗ**; `pg_verify` nay **so cả khoá chính lẫn UNIQUE** *(trước đây ⛔ không so, nên khoá **khai mà không áp** đi qua im lặng — cùng bệnh với lỗ đã sinh ra chính cổng đó)*. ⭐⭐ **Phân biệt hai con số**: **DÒNG SỔ ghép được 2.677** *(tỷ lệ ghép 26,79% tính theo đây)* vs **MỐI NỐI 2.719** *(hình `B` 27 dòng mang **69** mối nối, một dòng chia cho **10** dòng lệnh)* — chính tôi đã gọi lẫn một lần, test bắt được, nay cả hai bị khoá. **360 phép thử** *(+23)*. ⚠ 27 dòng `B` trong kho **hiện tại** vẫn ở hàng chờ *(sổ append-only, không sửa trạng thái được)* — chúng đậu ở **lần nạp sạch kế tiếp**, tức **lý do thứ hai cụ thể** để làm `GAP-KHO-01`.

- **v1.9** (2026-08-27): ⛔⛔⛔ **Bộ test đang GHI VÀO SỔ THẬT** — `fls_itl` **11.177** dòng trong khi tài liệu ghi **9.973**: 5 file test PG lấy **mặc định** đúng địa chỉ kho thật ⇒ **1.204 dòng dấu test** *(kèm 1.285.475.949 tiền bịa)*, **106** dòng `fls_reject`, **227** lần chạy test, và **194 dòng bịa trong hàng chờ việc của kế toán**. ⭐⭐ **Thêm cổng chung #10 "kho THẬT và kho TEST là HAI KHO"** với **ba tầng chặn** *(`dsn_test()` nổ · kết nối **chỉ-đọc** ở tầng PostgreSQL · test **quét mã nguồn**)*; ★ tầng ⓶ **thấy đỏ THẬT ngay lần đầu bật**, bắt một bài đang `CREATE TABLE` vào kho thật. Luật là **bản TRẮNG** `NAP-yyyy-mm-dd-NGUỒN`, ⛔ không phải bản đen. Kho thật **không tăng một dòng** qua 3 lần chạy `pytest`. ⚠ Dọn 1.204 dòng cũ ⛔ **không bằng `DELETE`** *(`INV-I08`)* ⇒ **`GAP-KHO-01` chờ owner**; kèm `tools/sao_luu_kho.py --so-sanh` kiểm tính chất **chưa ai kiểm**: sổ có dựng lại được từ nguồn hay không.
  > ⛔ **Mục changelog này từng BỊ MẤT TRONG IM LẶNG.** Script vá tài liệu dùng `str.replace` với mẫu **không tồn tại** — Python bỏ qua **không báo gì** — nên header lên `v1.9` mà mục changelog `v1.9` **không bao giờ được thêm**. Cổng `K1` lúc đó soi **một chiều** *(chỉ bắt header < changelog)* nên cũng im. ⇒ Đã thêm **chiều ngược lại** vào `K1`, và nó bắt được đúng lỗ này.

- **v1.8** (2026-08-27): ⛔ **Sửa một lệch của chính file này:** v1.7 đã **thêm cổng chung #8 vào §5.10** nhưng **không bump version, không ghi changelog** — tức bản này từng vi phạm đúng luật spec-first của `07_CHANGE_CONTROL` §2 bước 4. ⭐⭐ **Thêm cổng chung #9: "đếm GIÁ TRỊ, không chỉ đếm DÒNG"** — sinh ra từ một lát đọc **hợp lệ** vẫn **thiếu 257 giá trị** mà **bốn cổng đều im** *(và cổng #7 cũng không đủ: nó đo trục **dòng**, đây là trục **giá trị/cột**)*. ⭐ **P3 phần lõi xong** — adapter A, **2.650 mối nối** vào kho, **26 phép thử**, sáu hình dạng `A…F`; `§5.7` **22% → 40%**, `§5.5` **70% → 78%**. ⛔⛔ **Rút hai câu SAI trong §5.7** *(dựng trên tiền đề `CR#1` đã bị đo lật)*: *"mã tham chiếu nằm ở phiếu, không ở dòng"* và *"cách cũ rơi im lặng 289 dòng"* — mã nằm ở **DÒNG** *(526/1.468 phiếu mang 2–36 mã khác nhau)*, con số 289 **không tái lập được**. Thêm **luật công bố tỷ lệ ghép phải đưa CẢ HAI cách đếm** *(33,2% đang dùng vs **26,79%** đúng — con số đúng **nhỏ hơn**)*. **308 phép thử** · **3.301 dòng** `fls/`.

- **v1.7** (2026-08-26): ⭐ **Parity cả sổ ĐẠT: 64.393/64.393 ô = 100,0000%, 22 kỳ.** Và ⛔ **sửa `DoD 5.6 ③`** — luật *"đọc có retry + cắt lát nhỏ hơn"* **chữa sai bệnh**: workbook `ADJUSTED` **không trả được giá trị đã tính**, một ô cũng timeout *(`GAP-ORA-08`)*; *"4/7 khối mỗi buổi"* là **may mắn**, không phải kích thước lát. Thêm giới hạn `timeout` ≤ 45s. §5.6 ◐85%.

- **v1.6** (2026-08-26): **P2 nửa đầu xong** — `fls/oracle/` ◐75% *(6 tệp · 55 test · 3 cổng SONG đã thấy đỏ thật)* + `fls/adapters/bank.py` ◐15% *(19 test)*; **198 test xanh** · `lint-imports` **6 kept**. ⭐ **Thêm cổng chung thứ 7: "cổng phải chứng minh nó ĐÃ ĐO ĐƯỢC GÌ"** — sinh ra từ một lần cổng parity **nói dối** *(đọc 0 dòng, so 0 ô, in "khớp 100%", trả PASS)*; sáu cổng cũ không cái nào bắt được vì cả sáu chỉ hỏi *"có thấy lỗi không"*. Tiến độ theo khối lượng việc **37%** — bảng sống ở `tools/tien_do.py` và `Ban-ve-Kien-truc-TOBE.html` **BẢN VẼ 12**.

- **v1.4** (2026-08-26): **P1 xong** — `canon` · `ledger` · khung `repo`. §2 P1 → ✅; §5.3/§5.4 → ✅, §5.5 → ◐. Ghi rõ **1 phép đánh số cố ý KHÔNG ở lớp sổ** *(`SEQUENCE` của DB, `INV-I04a`)*. ⭐ Cổng chèn lùi ngày đã thấy đỏ theo cách mạnh nhất: **DB từ chối** thao tác AS-IS. `import-linter` **2 → 4 contract** ⇒ mũi tên một chiều về `canon`/`contract` của `01_TECH_DESIGN` §4 nay là **test**.

- **v1.3** (2026-08-26): **Đóng `GAP-DB-P0-02`** — di trú forward-only có số thứ tự + sổ ghi. §5.1 đổi dòng *Nợ lại* thành dòng **Di trú ✅**, và siết dòng *CHƯA xong* thêm hai điều kiện: **đổi `schema.py` mà không có migration** · **bảng trong `TABLES` mà không ai tạo**. Cả hai lỗ này trước đây build vẫn xanh. Chi tiết cưỡng chế: `DEV-04` **v1.6 §7**.

- **v1.2** (2026-08-26): **Thêm §5 — Definition of Done cho 9 module chính** *(`db` · `contract` · `canon` · `ledger` · `repo` · `oracle` · `adapters` · `api` · `web`)*. Mọi module có **ba phần**: điều kiện xong · **lệnh chạy được** để chứng minh · ⛔ **điều kiện CHƯA xong** viết từ chính những cái bẫy đã sập. Cộng §5.10 sáu cổng chung, trong đó có điều kiện **"cổng đã từng thấy đỏ một lần"**.
  ⭐ **Đóng `GAP-ERD-P0-01`** *(owner chốt)*: thêm FK `fls_itl.run_id → fls_run.run_id`; `ERD_ISLANDS` **4 → 2**. Khi áp FK phát hiện `pg_migrate` **báo thành công trong khi áp THIẾU** *(`CREATE TABLE IF NOT EXISTS` bỏ qua bảng đã có, trong im lặng)* ⇒ thêm **cổng thứ 5** `fls/db/pg_verify.py` so DB thật vỗi schema khai báo. Mở `GAP-DB-P0-02` *(chưa có đường `ALTER`)*.

- **v1.1** (2026-08-26): **P0 đã chạy xong** — 8 task, 9 commit, 34 test xanh, 4 cổng sống. Đóng `GAP-PLAN-01/02/03`. Mở `GAP-ERD-P0-01`. ⭐ **Cổng `G-ERD-3` bắt được lỗ của chính plan đề ra nó**: plan khai 2 island, chạy thật ra 4 *(thiếu `fls_run`, `fls_reject`)* — bằng chứng cụ thể rằng cổng-bằng-test khác cổng-bằng-mắt.

- **v1.0** (2026-08-26): Viết mới cho FLS, khai tử bản copy chương trình. **7 pha P0–P6**, mỗi pha một deliverable chạy được. Trục của bản này là **4 cổng chạy được thay cho rà tài liệu** — dựng sau khi phát hiện **drift đang tồn tại**: ERD của BA và DDL của Dev tả hai mô hình khác nhau *(chỉ 3/10 entity khớp, `fls_journal` vắng mặt, "view hay bảng" nói trái nhau)*, và `fls_id_counter` sao chép đúng pattern FPS đã khai tử *(đọc ngược bài học)*. Mở `GAP-PLAN-01…04`.
