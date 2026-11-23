# WO-015 — Sổ actor phủ **mọi** bảng có cột `actor` · bài quét bắt actor theo **chỗ dùng** · UAT "chữ cái" = ASCII · `C8` nối **đúng một** dòng nhật ký · phép so cho ô version của master/roadmap

| | |
|---|---|
| **Trạng thái** | `MO` · ⏳ ưu tiên **THẤP** — ⭐ *(02/10, `fls-ba`)* làm **SAU** [`WO-032`](WO-032-so-tien-khac-tien-te-va-khuon-cua-du-truong.md) *(phiếu ấy chạm hai màn kế toán dùng cho vòng ghép thật đầu tiên — `B5`)*, **TRƯỚC** `WO-023` · ~~làm **SAU** [`WO-008`](WO-008-chu-man-sau-bo-ghep.md)~~ *(⛔ câu treo; ⛔ chặn gì; sổ thật hôm nay ⛔ con số nào đổi)* *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Vòng** | `1` |
| **Phát bởi** | `fls-ba` · 2026-10-02 chiều |
| **Nhận** | `fls-dev` |
| **Thứ tự với phiếu khác** | ⭐ *(thêm 02/10, `TL-016`)* **SAU [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md)** — lỗ của `WO-018` là **dòng nhật ký** ghi sai vĩnh viễn, lỗ của phiếu này là **cổng đếm** tính lại được; `T7` dọn luôn đỏ loại c của `WO-018` **chỉ khi** nó đã ĐẠT. · ⭐ **SAU `WO-008`** *(kể cả khi `WO-008` đã `KQ` ĐẠT)*. Lý do: cả hai phiếu thêm bài thử ⇒ số phép thử ghim trôi *(loại c)*; làm nối đuôi thì `BG` mỗi phiếu tách được đỏ của **chính** nó. `T7` *(`--ghi`)* của phiếu này dọn luôn đỏ loại c của `WO-008` **chỉ khi** `WO-008` đã ĐẠT *(`10 §6 ⓒ`)* |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(tác vụ ① — thước `B2`…`B5`)* + cổng *"người đã làm"* của tác vụ ② *(`khop_owner C8`)* + một cổng *"người đã làm"* **tương lai**: bản khai cột *"đã xác nhận"* trên `fls_khai_cot`.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ **phiếu này ⛔ xoá trực tiếp mắt xích nào** — nói thẳng. Nó vá **bốn lỗ nhỏ** của thước *"người thật"* mà `WO-011` vừa dựng, trước khi kế toán thật bấm cú đầu tiên — lúc ấy mỗi lỗ là một con số sai trên màn owner.
- Bốn lỗ, mỗi lỗ một chiều:

| Lỗ | Chiều | Đo được *(02/10, kho thật chỉ `SELECT` / `KQ-014`)* |
|---|---|---|
| ⓐ Hai actor máy đang chạy ⛔ mang dấu `@` ⇒ lọt bài quét mã | **im** *(máy mới quên khai ⇒ đếm là người)* | `tools/chup_sao_ke.py:85` `actor="tools/chup_sao_ke.py"` · `tools/nap_nguon_va_khai.py:67` `MAY = "máy · trích dòng 1 (QĐ-ITL-105)"` |
| ⓑ Cổng *actor lạ* chỉ soi **5** bảng/khung xem; kho có **7** có cột `actor` | **im** | `fls_chup` **147** dòng *(`tools/chup_sao_ke.py` **2**)* · `fls_khai_cot` **704** dòng — **4** chuỗi ngoài sổ: `máy · trích dòng 1 (QĐ-ITL-105)` **464** · `khai-thu-tu@apero.vn` **144** · `claude@fls(bo-thu_tu-tu-them)` **12** · `claude@fls(sua-khai-ACB-USD)` **12** |
| ⓒ Luật UAT: SQL `[[:alpha:]]` ↔ Python `isalpha()` lệch | **ồn** | **7.405 / 1.112.063** điểm mã ở vị trí *"ký tự sau `UAT`"* *(`KQ-014 F-1`)*; `la_uat` Python ⛔ được gọi ở đường chạy nào |
| ⓓ `C8` nối nhật ký theo `(itl_id, field, actor, at)` ⇒ hai bút toán cùng giao dịch khớp **2** dòng | **im** *(một cú sửa thật bị nuốt)* | tái hiện `KQ-014 F-2` trên kho TEST; hôm nay **0** đường *(`fls/api/xu_ly.py::sua` một bút toán / yêu cầu)* |
| ⓔ Ô **version** ở master §8 / roadmap bước 4 và ô `lint` ⛔ phép so ⇒ già im lặng | **im** *(câu văn)* | `KQ-014 F-3`: `DEV-02 v1.0` *(thật **v1.2**)* · `lint 8 kept` *(thật **9**)*; `fls-ba` sửa thêm 02/10: `DEV-12 v0.6` · `BA-14 v0.1` · `BA-13 v1.0` · `BA-12 v0.2` · `BA-09 v0.4` |

## Căn cứ
- [`KQ-014`](KQ-014-kiem-bg-013.md) *(`fls-test` 02/10 trưa — `WO-011` ĐẠT)*: `F-1`, `F-2` *(gửi `DEV` ghi nhận)* · `F-3`, `F-4` *(gửi `BA`)*. `fls-ba` quyết **sửa cả bốn** — bảng *Nghiệm thu PO* của [`WO-011`](WO-011-thuoc-nguoi-ban-trang-va-anh-hieu-luc.md).
- **`QĐ-ITL-150 ⓐ`** *(owner 01/10: "còn lại như đề xuất")*: UAT ⛔ tính người cho mốc `B` *"hay **bất kỳ** cổng *người đã làm* nào"* ⇒ `fls_khai_cot` thuộc luật này vì chính mã khai nghĩa ấy: `tools/nap_nguon_va_khai.py:62`–`66` *"Kế toán xác nhận lúc tải tệp lần đầu sẽ sinh **`version` mang tên họ**; *"đã xác nhận"* = *"có một bản khai mang tên người thật"*"*.
- Owner 02/10 *(lần 3)*: *"defer phần tài khoản, làm xong công cụ đã"* ⇒ phiếu này **⛔ dựng danh mục người**; chỉ khai thêm vào `ACTOR_MAY` những actor **⛔ phải người** có bằng chứng.
- Luật `Đ5` *(`CLAUDE.md`)*: cổng NO khi khác — **cả hai chiều**; ⓐ ⓑ ⓓ ⓔ đều là chiều **im**.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md` | §2 bảng luật *"người thật"* — các đoạn ⭐ **v1.15** ở ⓐ · ⓒ · ⓓ · ⓔ | ⭐ **v1.15** |
| `01_Orchestrator/10_HOP_DONG_AGENT.md` | §6 `dong_bo_so_song --ghi` *(ⓐ ⓑ ⓒ)* | v1.1 |
| `00_MASTER_INDEX.md` | §8 bảng kit *(ô version)* · §10 *(ô `lint-imports`)* | ⭐ **v0.31** |
| `01_Orchestrator/08_MIGRATION_ROADMAP.md` | bước 4 *(ô `DEV-02`, `DEV-12`)* | ⭐ **v1.1** |
| `handoff/KQ-014-kiem-bg-013.md` | `F-1`…`F-4` · bài `tests/nghiem_thu/test_kq014_thuoc_nguoi_tren_duong_ghi_that.py` *(33 bài — ⛔ sửa; nó là thước nghiệm thu của `T4`/`T5`)* | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **`T1` — khai 5 actor vào `ACTOR_MAY`** *(`fls/repo/danh_muc_actor.py`, mỗi hằng một dòng chú thích: ai dùng · ngày · số dòng trên kho thật)*: ⓐ `tools/chup_sao_ke.py` *(đang chạy — `tools/chup_sao_ke.py:85` **lấy từ** sổ)* · ⓑ `máy · trích dòng 1 (QĐ-ITL-105)` *(đang chạy — `tools/nap_nguon_va_khai.py::MAY` **lấy từ** sổ)* · ⓒ **lịch sử** *(⛔ còn mã nào ghi — `git log -S` ra **0** commit mã, chỉ commit phiếu)*: `khai-thu-tu@apero.vn` *(**144** dòng, **một** thời điểm `10/09 11:53:32` UTC ⇒ một lô ghi, ⛔ cú bấm người)* · `claude@fls(bo-thu_tu-tu-them)` *(**12**, `10/09 04:24:55`)* · `claude@fls(sua-khai-ACB-USD)` *(**12**, `10/09 04:24:24`)*. Sổ **9 → 14**. Chuỗi SQL cổng ở `tools/kiem_so_song.py` *(bản chép bị `_kiem_hang_may` ép trùng byte)* theo đó | ⛔ Danh mục người / `DANH_MUC_NGUOI` *(owner hoãn)*. ⛔ Đổi `actor` của dòng **đã ghi** *(`INV-I08`)* |
| **`T2` — bài quét mã theo CHỖ DÙNG**: ngoài mẫu `…@fls…`/`…@apero.vn` hiện có, mọi **chuỗi hằng** đi vào chỗ ghi actor trong `fls/` + `tools/` *(⛔ `tests/`)* — tham số từ khoá `actor=` · giá trị mặc định của tham số tên `actor` · hằng module được truyền vào hai chỗ ấy — phải ⊆ `ACTOR_MAY ∪ ACTOR_DA_THAY`. Dev chọn cách đọc *(`ast` khuyến nghị)*, `BG` ghi cách và **số chỗ** bài quét thấy | ⛔ Quét `tests/` *(người mẫu của bài thử, vd. `ke-toan@apero.vn`, là chủ ý)* |
| **`T3` — soi actor lạ trên MỌI bảng có cột `actor`**: `_q_actor_moi` *(`tools/kiem_so_song.py` ~`:373`)* lấy danh sách bảng/khung xem từ `information_schema.columns where column_name = 'actor'` **lúc chạy** — ⛔ gõ tay danh sách. Đo 02/10: **7** *(`fls_queue_event` · `fls_adjustment` · `fls_journal` · `fls_da_xong` · `fls_sua_tay` · `fls_chup` · `fls_khai_cot`)*; dòng báo `⚠ ACTOR MỚI` ghi thêm **tên bảng** đầu tiên thấy actor ấy. Danh sách đọc ra **rỗng** ⇒ `⛔ khong do duoc` *(`Đ3`)* | ⛔ Đổi phép đếm **người** của mốc `B` *(`B2`…`B5` vẫn chỉ đọc `fls_queue_event`/`fls_pm_unlink`)* |
| **`T4` — UAT "chữ cái" = ASCII** *(`09` v1.15 ⓓ)*: `la_uat` ⇒ ký tự kế `UAT` ∈ `A`–`Z`/`a`–`z` *(khai tường minh, ⛔ `isalpha()`)*; mẩu SQL ⇒ lớp **tường minh** `[A-Za-z]`, **⛔ dựa cờ không-phân-biệt-hoa-thường cho lớp này** *(cờ `~*` gập `K` Kelvin `U+212A` về `k` ⇒ lệch lại)*; tiền tố `uat` vẫn không phân biệt hoa thường. Tập khoảng trắng đầu **giữ** 9 ký tự khai tay. Bảng mẫu của Dev *(`tests/repo/test_danh_muc_actor.py:149`–`152` — `'UATé'`, `'UATđ'`, `'UATƯ'`, `'UAT中'` mong `False`)* đổi mong theo luật mới | ⛔ Mở rộng tập khoảng trắng *(ký tự ngoài tập ⇒ người ở **cả hai** mặt — chiều ồn, chấp nhận ở `09` v1.15)* |
| **`T5` — `C8` nối đúng một dòng nhật ký** *(`docs/ITL/_tools/khop_owner.py::_c8` ~`:515`)*: mỗi dòng `fls_sua_tay` lấy lý do từ **chính** dòng nhật ký của bút toán đang hiệu lực *(Dev chọn: dòng `jrn_id` lớn nhất trong khoá, hay khoá + `value_after` — `BG` ghi vì sao và ca nào cách ấy vẫn mơ hồ)*; phép nối ra **≠ 1** dòng ⇒ `C8` **⛔ không đo được** *(NO)*. ⚠ ⛔ dùng `fls_adjustment.evt_id`: đường `ghi_tay.ghi_but_toan` ghi `evt_id` **NULL** *(đo 02/10 — chính docstring `_c8` đã ghi)* | ⛔ Migration thêm `fls_journal.adj_id` *(nếu Dev thấy cần ⇒ `HOI`, ⛔ tự làm)* |
| **`T6` — phép so cho ô version / `lint`** *(`tools/kiem_so_song.py`, cổng chung #13)*: thêm `Muc` cho master §8 `03_Dev/` `02` · `02_BA/` `09` `12` `13` `14` · `01_Orchestrator/` `09` `10` `11` *(đọc `Version` từ đầu tệp như `v(…)` đang làm)*; roadmap bước 4 `DEV-02` · `DEV-12`; master §10 `` `lint-imports` **N kept 0 broken** ``. Neo vào **ô đầu hàng** của kit *(bài học `ORCH-08` — `kiem_so_song.py:1180`–`1185`)* | ⛔ Phép so cho **câu** *(máy ⛔ canh nghĩa — lớp `doc-set-silent-drift`)*; ⛔ ô *"◐ 8 file thật"* của `03_Dev/` *(chưa ai đo lại — `fls-ba`)* |
| **`T7` — sau cùng**: `tools/dong_bo_so_song.py --ghi` **một lần** *(`10 §6`)* — dọn đỏ loại *b/c* của chính phiếu *(số phép thử · số phép so `110 → 110 + n`)* và của `WO-008` **nếu** `WO-008` đã ĐẠT; sửa câu cạnh số mà số mới làm sai nghĩa, `BG` liệt kê `tệp:dòng · cũ → mới` | ⛔ Chạy `--ghi` **trước** `T1`…`T6` xanh |
| **`T8` — bài thử, chứng minh ĐỎ trước** *(`Đ5`)* — `tests/repo/`, `tests/test_kiem_so_song.py`, bài cho `khop_owner` | ⛔ Sửa / xoá bài trong `tests/nghiem_thu/**` |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 | `ACTOR_MAY` = **14** tên *(9 cũ + 5 của `T1`)*, mỗi tên một hằng có chú thích; `grep -rnF 'tools/chup_sao_ke.py"'` và `grep -rnF 'máy · trích dòng 1 (QĐ-ITL-105)'` trong `fls/`+`tools/` *(⛔ `__pycache__`)* ⇒ chỉ ở **sổ** + **chuỗi SQL** `tools/kiem_so_song.py` | bài `test_SO_MAY_du_va_ghim` *(cập nhật)* + `grep` dán vào `BG` | xoá một tên khỏi sổ ⇒ bài **ĐỎ**; gõ lại chuỗi `tools/chup_sao_ke.py` trong `tools/chup_sao_ke.py` ⇒ bài **ĐỎ** |
| AC-2 | Bài quét mã `T2` thấy **cả hai** chỗ dùng ⛔ `@` *(`chup_sao_ke.py:85`, `nap_nguon_va_khai.py:67`)* và xanh khi chúng lấy từ sổ; `BG` in số chỗ quét được *(mẫu số ≠ 0 — `Đ3`)* | `pytest tests/repo/test_danh_muc_actor.py` | ⓐ thêm `actor="tools/thu_moi.py"` vào một lệnh gọi trong `tools/` ⇒ **ĐỎ**; ⓑ thêm hằng module `MAY_MOI = "may moi"` rồi truyền `actor=MAY_MOI` ⇒ **ĐỎ**; ⓒ `def f(conn, actor="mac-dinh-moi")` ⇒ **ĐỎ** |
| AC-3 | Kho THẬT *(chỉ đọc)*: `kiem_so_song` dòng *actor ngoài sổ* đọc **7** bảng/khung xem và in **0**; mốc `B` vẫn **`1 · 1 · 3`**, người thật **0** | `python tools/kiem_so_song.py` nguyên văn | kho TEST: chèn **một** dòng `fls_chup` actor `chup-moi-chua-khai@fls` ⇒ **một** dòng `⚠ ACTOR MỚI: chup-moi-chua-khai@fls · 1 · fls_chup` + **NO**; gõ tay danh sách 5 bảng như cũ ⇒ bài **ĐỎ**; `information_schema` trả rỗng *(giả)* ⇒ `⛔ khong do duoc` |
| AC-4 | Luật UAT: trên **mọi** điểm mã `1`…`0x10FFFF` *(⛔ `0xD800`–`0xDFFF`)* ở **5** vị trí của bài `KQ-014` *(`sau` · `dau` · `u` · `a` · `t`)*, tập SQL **=** tập Python — **0** lệch; `'UAT02/10'` · `'UAT-02'` · `'UATé'` ⇒ UAT; `'UATX'` · `'UATs'` · `'uất ức'` · `NULL` ⇒ người | bài Dev mới *(phủ cả ngoài BMP)* + bài `KQ-014` `test_luat_UAT_moi_diem_ma__…` **⛔ đổi một dòng**, vẫn xanh | trả `la_uat` về `isalpha()` ⇒ lệch **> 0** ⇒ **ĐỎ**; mẩu SQL dùng `~*` với `[a-z]` ⇒ lệch ở `U+212A` ⇒ **ĐỎ** |
| AC-5 | `C8` kho TEST, **một** giao dịch: cùng actor `ghi_but_toan(cdt1, reason='UAT 02/10 thu')` rồi `ghi_but_toan(cdt1, 'C-THAT', reason='chot that', force=True)` ⇒ `C8` đếm **người 1** ⇒ `khop_owner --kiem` **CONG NO** *(đúng hành vi)*; kho THẬT ⇒ `C8` vẫn `NGUOI chot 0` *(`fls_sua_tay` **0** dòng hiệu lực)*; ba bài `C8` của `KQ-014` vẫn xanh | bài cho `_c8` *(tái hiện nguyên kịch bản `KQ-014 F-2`)* + `khop_owner --kiem` nguyên văn | trả về nối theo khoá 4 cột với `not exists … UAT` như hôm nay ⇒ bài **ĐỎ**; dựng ca nối ra **2** dòng mơ hồ *(Dev chỉ ra trong `BG`)* ⇒ `⛔ khong do duoc`, ⛔ im |
| AC-6 | `T6`: `kiem_so_song` có phép so mới cho **11** ô *(master §8 ×8 · roadmap ×2 · master §10 `lint` ×1)*; hôm nay **OK** cả 11 | lệnh cổng | *(worktree)* sửa `02` **v1.2** → `v1.1` ở master §8 ⇒ **ĐỎ**; sửa `9 kept` → `8 kept` ở master §10 ⇒ **ĐỎ**; sửa `DEV-12` **v0.9** → `v0.6` ở roadmap ⇒ **ĐỎ** |
| AC-7 | `pytest` toàn bộ xanh *(⛔ `xfail`)* · `lint-imports` **9 kept 0 broken** · số bài tăng đúng số bài mới so với nền lúc nhận *(đo lại — sau `WO-008`)* · `git diff <nền> -- tests/nghiem_thu/` **rỗng** | lệnh ở `CLAUDE.md` | — |
| AC-8 | `T7`: sau `--ghi`, `kiem_so_song` **0 lệch**; `kiem_tai_lieu` ĐẠT; `khop_owner --kiem` **17/20** như nền *(⛔ phép mới lật)*; `BG` có bảng câu cạnh số đã sửa | lệnh cổng nguyên văn | — |

## Dữ liệu
- Bảng/cột chạm *(chỉ ĐỌC)*: `information_schema.columns` · cột `actor` của **7** bảng/khung xem ở `T3` · `fls_sua_tay` · `fls_journal(jrn_id, itl_id, field, actor, at, value_after, reason)` · `fls_adjustment`.
- Ghi kho THẬT: **`KHONG`**. Mọi bài chạy kho TEST, mỗi bài một giao dịch lùi.
- Số dòng dự kiến chạm *(đếm 02/10 chiều, chỉ `SELECT`)*: actor theo bảng — `fls_chup` **147** *(`nhip@fls` 135 · `nhip@fls(tay)` 10 · `tools/chup_sao_ke.py` 2)* · `fls_khai_cot` **704** *(`máy · trích dòng 1 (QĐ-ITL-105)` 464 · `khai-thu-tu@apero.vn` 144 · `thu@apero.vn` 72 · `claude@fls(…)` 12 + 12)* · `fls_adjustment` **4.428** *(`may_goi_y` 4.424 đều có `evt_id` · `sua_tay` 4 đều có `evt_id` — 4 dòng UAT 01/10 đi qua đường ghép/bỏ ghép, ⛔ qua `ghi_but_toan`)* · `fls_sua_tay` **0** dòng hiệu lực. Sau `T1`: actor ngoài sổ trên 7 bảng **0** ⇒ cổng ⛔ đổi trạng thái hôm nay.

## Câu còn treo
- ⛔ **Không câu nào chặn.** Năm quyết định là **thước đo** *(ai ⛔ phải người · nhận UAT thế nào · nối nhật ký ra sao)* — `fls-ba` quyết trong thẩm quyền spec *(`09` v1.15)*, ⛔ đổi *"con số trên màn đến từ đâu"*.
- *(⛔ chặn)* Nếu owner nói `khai-thu-tu@apero.vn` **là một người** ⇒ chuyển tên ấy từ `ACTOR_MAY` sang `ACTOR_DA_THAY` — **một dòng**, ⛔ đổi thiết kế. Bằng chứng xếp vào máy: **144** dòng mang **cùng một** thời điểm *(một lệnh ghi)*, ⛔ commit mã nào từng mang chuỗi.
- *(ngoài phạm vi, ⏸ owner hoãn)* Danh mục người + email đăng nhập *(`WO-011 Q1`)*.

## Rủi ro
1. **`T2` quét theo chỗ dùng có thể thấy actor ở chỗ ⛔ ngờ** *(vd. chuỗi mặc định của một công cụ cũ)* — đó là **mục đích**; mỗi tên mới phải vào sổ kèm chú thích, ⛔ thêm ngoại lệ vào bài quét. Quá **3** tên ngoài 5 tên của `T1` ⇒ `HOI` *(có thể là một lớp actor `fls-ba` chưa biết)*.
2. **`T4` đổi mong của 4 mẫu Dev** *(`'UATé'`…)* — đổi có chủ ý *(`09` v1.15 ⓓ ghi cái giá)*; bài `KQ-014` ⛔ được đổi, và nó vẫn phải xanh *(hai tập bằng nhau thì thoả cả hai assert của nó)*. Bài `kq014` nào đỏ ⇒ `HOI`, ⛔ sửa bài.
3. **`T5` chọn sai dòng nhật ký** cho ca nhiều bút toán cùng khoá *(cùng giá trị qua lại trong một giao dịch)* — chặn bằng luật *≠ 1 ⇒ ⛔ không đo được*; `BG` liệt kê ca nào còn mơ hồ.

## Changelog
- 2026-10-02 chiều · `fls-ba` · phát `WO-015` từ `KQ-014` `F-1`…`F-4` *(ưu tiên **THẤP**, sau `WO-008`)*; spec `09` **v1.15** · master **v0.31** · roadmap **v1.1**. ⚠ Đo trước khi viết `T5` *(`Đ1`)*: lời khuyên *"nối theo `adj_id`/`evt_id`"* của `KQ-014 F-2` ⛔ dùng được — `ghi_but_toan` để `evt_id` **NULL** *(`fls/repo/ghi_tay.py:403`–`447`, gọi `_them` ⛔ truyền `evt_id`)*.
