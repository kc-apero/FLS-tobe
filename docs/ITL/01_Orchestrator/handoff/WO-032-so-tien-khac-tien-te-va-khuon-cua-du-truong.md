# WO-032 — Hộp ghép ⛔ còn so hai tiền tệ khác nhau · khuôn ứng viên đủ trường ở mọi cửa · trạng thái rỗng vẽ được · ô lý do ghép tuỳ ý

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(02/10 — `fls-ba` nghiệm thu PO: [`KQ-036`](KQ-036-kiem-bg-034-bg-035.md) ✅ ĐẠT **15/15** `AC-1`…`AC-15`, sổ thật **0** sai trên **10.909** phần tử khuôn `⓵`; bảng đối chiếu ý owner ở mục **Nghiệm thu PO** cuối phiếu; 6 `F` `NHE` ⇒ `F-5` sửa giấy ngay · `F-1`/`F-2`/`F-3`/`F-4`/`F-6` ⇒ [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md))* · ~~⭐ **`CHO_TEST` — vòng 2** *(02/10 — [`BG-035`](BG-035-ban-giao-wo-032-vong-2.md) @ `932d8a4`; `fls-test` kiểm **gộp** `BG-034` + `BG-035`)*~~ · ~~`DANG_LAM` — vòng 2 *(02/10, `fls-dev` nhận: git `363a441` = `origin` · `BA-06` v4.15 · `BA-07` v3.8 · `BA-13` v1.7 ✔)*~~ · ~~`MO` — vòng 2~~ *(02/10, `fls-ba` — [`TL-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md): thêm `(i)` `(j)` `(k)` + `AC-12`…`AC-15`, xem mục **Vòng 2** cuối phiếu; `BG-034` ⛔ kiểm riêng — `fls-test` kiểm **gộp** `BG-034` + `BG` vòng 2)* · ~~`CHO_TEST` *(02/10 — [`BG-034`](BG-034-ban-giao-wo-032.md) @ `9c100ac`)*~~ · ~~`DANG_LAM`~~ · ~~`MO` · ⭐ **SẴN SÀNG**~~ · ưu tiên **TRUNG BÌNH** — làm **TRƯỚC** [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) và [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-02 |
| **Nhận** | `fls-dev` |
| **Vòng** | `2` *(02/10 — từ [`HOI-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md) + `BG-034` yếu #7/#8)* · ~~`1`~~ |
| **Thứ tự với phiếu khác** | **Sau** [`WO-022`](WO-022-in-tien-theo-tien-te.md) *(✅ `DONG` 02/10 — phiếu này đứng trên mã in tiền của nó: `TP.tien`/`TP.xu`/`TP.chuoi_xu`)*. ⭐ **TRƯỚC `WO-015`**: phiếu này chạm **đúng hai màn kế toán sẽ dùng** cho vòng ghép thật đầu tiên *(mốc `B5`)* — hôm nay hộp *Tìm tiền* nói *"trong dung sai"* cho **4** lệnh sổ thật mà cửa ghi **từ chối**, và in `—` cho **338 / 448** ứng viên bậc `ma` có lệch thật; `WO-015` là vệ sinh **thước đếm** *(sổ thật hôm nay ⛔ con số nào đổi)*. ⭐ **TRƯỚC `WO-023`**: hai phiếu cùng chạm `man_f01_lenh.js` / `man_f01.js` / `man_f01_ghep.js`; `WO-023` đổi **cách hộp đóng/mở** *(phím, hạn chờ, mã `409`)*, phiếu này đổi **chữ trong hộp** — làm chữ trước để bài thử của `WO-023` dựng trên chữ đúng. ⛔ **Không** xếp trên mức **TRUNG BÌNH**: cửa ghi đã chặn mọi cặp khác tiền tệ ⇒ **0** ghi sai *(`KQ-031` `F-1`, bài `kq031::test_F1_CANH_*`)*; hại là **đọc sai**, ⛔ ghi sai |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết **một vòng ghép thật** — hôm nay đo được **0**)*: người ấy quyết *"gán hay không"* bằng đúng ba thứ phiếu này sửa — câu *"trong dung sai / VƯỢT"*, ô `Lệch`, và chữ tô bằng chứng trong khối *"Đang gán"*. Và **mốc `C` cổng `C5`** *(⛔ phải mở Excel tra một ô)*: ô `Tiền` in `100.000,00` trần cạnh lệnh `100.000 VND` thì người phải mở sao kê để biết đó là **USD**.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm mắt xích; phiếu này giữ cho mắt xích **"ghép PM ↔ tiền"** đã chuyển lên màn FLS **⛔ thua Sheets** — trên Sheets người nhìn cột tiền tệ ngay cạnh số; ở FLS hộp **nói thay** người *(*"trong dung sai"*)* thì câu ấy phải đúng hơn mắt người, ⛔ sai hơn. `QĐ-ITL-27` *(2–3 kế toán)*: kiểm soát nằm **trong máy** — một câu máy nói ngược cửa ghi là dạy người **bỏ qua** câu máy nói.

## Căn cứ
- [`KQ-031`](KQ-031-kiem-bg-030.md) *(`fls-test` 02/10, cả bốn `NHE`, có từ **trước** `WO-022` vòng 3)*: `F-1` `_drawer_tim_tien::_tinh` *(`man_f01_lenh.js:661`–`:690` @ `e0d2a96`)* trừ hai tiền tệ khác nhau — 8088 `PM00329-1` *(`100.000 VND`)* ↔ ứng viên `32700` *(bậc `ma`, `100.000,00 USD`)* ⇒ `note ok` *"lệch 0 ⇒ trong dung sai"*, cửa ghi ném `KhacTienTe`; **165 / 5.360** ứng viên khác tiền tệ *(rổ `may`, 268 lệnh)* · `F-2` `lenh_cho.py:420` cho `lech = null` ở **mọi** bậc `ma` — **338 / 448** có tiền ≠ tiền lệnh · `F-3` `the.gd` **0 / 768** mang `khoa_to`, bài `tests/web/test_b3_cuon_va_khoi_dang_gan.py:34` **tự nhét** — lần **thứ ba** của lớp *"khuôn thử tự nhét"* · `F-4` `?gia_lap=rong` mở hộp *Tìm tiền* ⇒ `TypeError` `man_f01_lenh.js:578`.
- [`KQ-029`](KQ-029-kiem-bg-027-bg-028.md) `F-2` *(`F04` rỗng ⇒ `TypeError` `man_f04.js:894`)* · `F-3` *(`.cand-cols` cột tiền `160px` ngoài `BA-06 §5b ⓘ`, ô có `ellipsis` mà ⛔ `title`)*.
- **`QĐ-ITL-62`** *(28/08)*: *"NGOẠI TỆ KHÔNG CÓ DUNG SAI"* · `BA-06 §4.3` BIA *(⛔ cộng / so khác tiền tệ)* · `BA-07 §3` dòng `match`: *"tiền tệ khác `422` (kiểm TRƯỚC Σ)"*.
- **`QĐ-ITL-149 ⓑ`** *(owner 01/10: **"bỏ yêu cầu lý do cho cú Ghép"**)* + `BA-07 §4h ⓼` *(`reason` tuỳ ý cho `match` + `unmatch`)* — ⭐ `fls-ba` đo khi nghiệm thu `WO-022` *(02/10, `grep`)*: **ba** hộp vẫn chặn nút khi ô lý do trống — `man_f01.js:345` *(Ghép)* · `man_f01.js:445` *(Bỏ cả chùm)* · `man_f01_lenh.js:650` *(Ghép ở hộp Tìm tiền)*, placeholder *"— BẮT BUỘC"*, chú thích `man_f01.js:342` *"Cửa ĐÒI `reason`"* già hơn `WO-003`. Hai hộp `Hoãn` *(`:261`)* / `Mở lại` *(`:567`)* ⛔ thuộc lời owner ⇒ **giữ** bắt buộc.
- ⭐ `fls-ba` đo thêm 02/10 *(chỉ `SELECT` + đọc mã)*: cửa `/so` *(`man_ghep.py:305`, nhánh `else`)* dán bậc **`cung_tien_te`** lên **mọi** dòng toàn sổ khác tiền tệ lệnh — dòng chưa nối **6.165** *(USD 3.766 · VND 2.239 · SGD 140 · HKD 20)* ⇒ với một lệnh VND **3.926** dòng mang nhãn *"cùng đơn vị tiền"*; và `man_f01_ghep.js:428` `BAC[uv.bac] || BAC.cung_tien_te` — bậc lạ **rơi im** về *"cùng đơn vị tiền"*.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(cách màn **in** và **so** chuỗi cửa đã trả + **nghĩa** một trường cửa đọc; ⛔ đổi sổ, ⛔ đổi luật dung sai, ⛔ đổi cửa ghi, ⛔ đổi HTTP)*. `F-2`: `fls-test` hỏi *"chữ `BA-07` hay mã — chọn một"* ⇒ **chọn: giữ trị tuyệt đối của mã, sửa luật `null` của mã** *(lý do ở `BA-07` v3.7 changelog)*. Ô lý do: **lời owner** `QĐ-ITL-149 ⓑ` — ⛔ quyết mới.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | **§5b ⓕ** *(đoạn v4.14 — lệch chỉ khi cùng tiền tệ)* · **ⓘ** *(thêm `.cand-cols`)* · **ⓙ** *(mới — bảng trộn tiền tệ in kèm mã)* · đoạn **Năm trạng thái** dưới bảng §5b *(rỗng của màn)* | ⭐ **v4.14** |
| `02_BA/07_API_CONTRACT.md` | **§4h ⓵** *(dòng `bac` · `lech` · `dien_giai_vi_sao` · `khoa_to` + đoạn luật bài thử)* · **⓵'** *(đoạn v3.7)* · **⓹** dòng *Bậc* · **⓼** *(`reason` tuỳ ý — ⛔ đổi, đọc lại)* | ⭐ **v3.7** |
| `02_BA/13_THUYET_MINH_MAN_HINH.md` | **④ Ngăn kéo *Tìm tiền*** — ba dòng *Bảng ứng viên* · *Σ hai con số* · *Ô vì sao ghép* | ⭐ **v1.6** |
| `01_Orchestrator/handoff/KQ-031-kiem-bg-030.md` | *Phát hiện* `F-1`…`F-4` + lăng kính **Dữ liệu** *(28 cặp hàm × biến, mẫu số)* + 3 bài `xfail(strict)` `test_kq031_*` | — |
| `01_Orchestrator/handoff/KQ-029-kiem-bg-027-bg-028.md` | *Phát hiện* `F-2` · `F-3` | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a) `F-1` — so tiền tệ trước khi trừ** *(§5b ⓕ v4.14)*: `man_f01_lenh.js::_drawer_tim_tien::_tinh` so `u.curr` ↔ `r.curr` *(`trim` + chữ hoa)* **trước** `TP.xu`; khác ⇒ `#sig-l` lớp `note crit` *"tiền lệnh `<số> <mã>` ↔ tiền bank `<số> <mã>` · **khác tiền tệ** ⇒ ⛔ cửa ghi sẽ TỪ CHỐI"*; ô `Lệch` in **`khác tiền tệ`**; ô `Tiền` in **kèm mã** *(§5b ⓙ)*. `F01G.ve_thanh`: nhãn xác nhận cho ứng viên khác tiền tệ nói *"(khác tiền tệ — cửa ghi sẽ từ chối)"*, ⛔ một *"(lệch …)"* | ⛔ đổi cửa ghi `ghep_lenh` / mã `422` · ⛔ thêm nút chặn *(cửa ghi đã chặn — màn chỉ phải **nói đúng**)* · ⛔ quy đổi tỷ giá |
| **(b) `F-2` — `lech` đủ ở mọi cửa khuôn `⓵`** *(`BA-07 §4h ⓵` v3.7)*: `lech = \|amount ứng viên − amount dòng lệnh\|` *(trị tuyệt đối, `Decimal`)* ở **mọi** bậc — `lenh_cho.py:420` *(bậc `ma`)* · `man_ghep.py:306` *(`/so`)* · `xu_ly.py:683` *(`the.gd`)* · `xu_ly.py:717` *(`the.gd_ds`)*, so với dòng lệnh **của chính cửa/thẻ**; khớp ⇒ `0`; **`null` ⇔ khác tiền tệ hoặc thiếu `amount`/`curr`**. Khuyến nghị **một** hàm tính dùng chung *(⛔ bốn bản)*. Màn: `F01L` ô `Lệch` in số ở bậc `ma`; `F01G` nhãn *"(lệch …)"* + khối *"Đang gán"* chip `lệch` hiện ở đúng các ca ấy | ⛔ đổi thứ tự xếp ứng viên *(vẫn theo `lech_tuyet_doi` của SQL bậc tiền)* · ⛔ đổi dấu *(vẫn trị tuyệt đối)* |
| **(c) `F-3` — `khoa_to` trên `gd`/`gd_ds`** *(`⓵` + `⓵'` v3.7)*: hai cửa danh sách `lenh-cho` / `lenh-da-gan` gắn `khoa_to` *(cùng `mg.khoa_bang_chung`)* cho **mọi** `the.gd` và phần tử `the.gd_ds`; khoá **luôn có mặt** *(`[]` khi ⛔ tô)*. Bài `tests/web/test_b3_cuon_va_khoi_dang_gan.py` **thôi tự nhét** `khoa_to` — thân lấy từ cửa thật *(xem (h))* | ⛔ đổi luật `khoa_bang_chung` · ⛔ chuyển tính `khoa_to` xuống JS |
| **(d) Bậc toàn sổ khác tiền tệ** *(`⓹` v3.7)*: `man_ghep.so_theo_lenh` — dòng ⛔ khớp mã, **khác tiền tệ** lệnh ⇒ `bac = 'khac_tien_te'` *(nhớ `BAC_XEP` — `man_ghep.py:307` `.index` sẽ ném nếu thiếu)*; `F01G.BAC` + `F01L.BAC` có mục *"khác tiền tệ"*; ⛔ dòng `man_f01_ghep.js:428` rơi về `cung_tien_te` — bậc lạ in **nguyên tên** | ⛔ lọc bỏ dòng khác tiền tệ khỏi toàn sổ · ⛔ đổi bậc ở hai cửa ứng viên máy đề xuất |
| **(e) Rỗng của màn vẽ được** *(§5b *Năm trạng thái* v4.14)*: `_drawer_tim_tien` khi `d` là `null` ⇒ hộp mở với câu rỗng *"⛔ Không có dòng tiền nào ứng"* *(nhánh `uv.length = 0` đã có)*; `man_f04.js:894` `la_rong` khi `d` là `null` ⇒ câu rỗng của `F04` | ⛔ đổi bốn trạng thái kia · ⛔ đổi cửa *(cửa thật ⛔ trả `data: null`)* |
| **(f) `.cand-cols` có lưới an toàn** *(§5b ⓘ v4.14)*: ô `.cand .amt>span` + nhãn `.cand .amt .lech` mang `title` = đúng chuỗi in | ⛔ đổi bề rộng `160px` *(đo: ô chữ `137px` ≥ 135 ✔)* · ⛔ token mới |
| **(g) Ô lý do ghép tuỳ ý** *(`QĐ-ITL-149 ⓑ` · `BA-07 §4h ⓼` · `BA-13` v1.6)*: ba hộp `man_f01.js:345` *(Ghép)* · `:445` *(Bỏ cả chùm)* · `man_f01_lenh.js:650` *(Ghép)* — ô trống ⇒ **vẫn gửi**, thân ⛔ mang `reason` *(hoặc chuỗi rỗng — cửa điền `(may dien) …`)*; placeholder bỏ *"BẮT BUỘC"*, nói *"tuỳ ý — bỏ trống thì máy ghi lý do mặc định"*; sửa chú thích `man_f01.js:342` | ⛔ đổi hộp `Hoãn` / `Mở lại` *(ngoài lời owner — giữ bắt buộc)* · ⛔ đổi cửa `match-lo` *(vẫn đòi — `WO-003 AC-3`)* |
| **(h) Bài thử** `tests/web/**` + `tests/api/**` — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; ⭐ **thân vẽ màn lấy từ CỬA THẬT trên kho TEST** *(HTTP, `assert current_database() = 'fls_test'`)* — ⛔ một khoá do bài đặt *(trừ thao tác DOM của khung hộp, như `KQ-029`/`KQ-031` đã chấp)*; mở rộng cổng quét khoá của `WO-022` vòng 3 *(`tests/web/test_wo022_v3_tim_tien_cua_that.py`)* sang các hàm `F01G` đọc `uv`/`g`/`the.gd` | ⛔ sửa / gỡ dấu `tests/nghiem_thu/**` *(`fls-test` gỡ ở `KQ` sau — 3 bài `kq031` sẽ `XPASS(strict)` đúng ý)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a)* | Kho TEST: một lệnh VND `<N>` + một dòng tiền **USD** `<N>.00` cùng số chứng từ *(bậc `ma`)*. Hộp *Tìm tiền* thân **từ cửa thật**: chọn ứng viên ⇒ `#sig-l` lớp chứa `crit`, chữ chứa **`khác tiền tệ`** và `TỪ CHỐI`, ⛔ chứa `trong dung sai`, ⛔ chứa `lệch 0`; ô `Lệch` = `khác tiền tệ`; ô `Tiền` = `<N>,00 USD`. Ca cùng tiền tệ của `WO-022` `AC-18` ⛔ đổi *(khớp đúng xu ⇒ `trong dung sai`; lệch `0,40` ⇒ `VƯỢT`)* | bài DOM `man_f01_lenh.js` + `thanh_phan.js` + `hop_thoai.js` **thật**; `pytest --runxfail tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F1_*` ⇒ passed | bỏ phép so mã ⇒ `lệch 0,00 ⇒ trong dung sai` ⇒ **ĐỎ**; in `—` thay `khác tiền tệ` ⇒ **ĐỎ**; ô `Tiền` ⛔ mã ⇒ **ĐỎ** |
| AC-2 *(b · cửa)* | Kho TEST, gọi **HTTP** bốn cửa *(`itl-candidates` · `/so` · `lenh-cho` · `lenh-da-gan`)*: mọi phần tử khuôn `⓵` có `lech` thoả: cùng tiền tệ ∧ hai số có mặt ⇒ `Decimal(lech) == abs(amount − amount lệnh)`; khác tiền tệ ⇒ `lech is None`. In **mẫu số theo cửa**, và mỗi cửa có **≥1** ca bậc `ma` lệch ≠ 0 **và** ≥1 ca khác tiền tệ *(dựng trên kho TEST — `Đ3`)*. `pytest --runxfail …::test_F2_*` ⇒ passed | bài cửa `tests/api/` *(khuôn `test_cua_lenh_cho_pg.py`)* | trả `lenh_cho.py:420` về `lech_tuyet_doi=None` ⇒ **ĐỎ**; để `/so` *(`man_ghep.py:306`)* `None` ⇒ **ĐỎ**; tính lệch qua hai tiền tệ ⇒ **ĐỎ**; tập rỗng ⇒ **ĐỎ** |
| AC-3 *(b · màn)* | Thân từ cửa thật: `F01L` ô `Lệch` bậc `ma` lệch `1.000.000` in `1.000.000`; `F01G.ve_thanh` sau cú bấm thứ nhất trên ứng viên ấy: nhãn chứa `(lệch 1.000.000 VND)`; ứng viên khác tiền tệ: nhãn chứa `khác tiền tệ`, ⛔ chứa `(lệch`; khối *"Đang gán"* có `lech ≠ 0` ⇒ chip `.lech` hiện | bài DOM `man_f01_lenh.js` / `man_f01_ghep.js` thật | màn đọc `lech` mà cửa trả `null` ⇒ `—` ⇒ **ĐỎ** |
| AC-4 *(c)* | Kho TEST qua HTTP: **mọi** `the.gd` *(≠ `null`, ⛔ `loi_nguon`)* và **mọi** phần tử `the.gd_ds` của **cả hai** cửa danh sách có khoá `khoa_to` *(list)*; mẫu số in ra > 0. Dựng một lệnh có diễn giải chứa số chứng từ ⇒ `khoa_to` ∋ số ấy ⇒ `ve_dang_gan` vẽ `<mark>` quanh nó **trên thân cửa thật**. `test_b3_cuon_va_khoi_dang_gan.py` ⛔ còn chuỗi `"khoa_to"` do bài đặt *(`grep`)*. `pytest --runxfail …::test_F3_*` ⇒ passed | bài cửa + bài DOM `man_f01_ghep.js` thật | bỏ gắn `khoa_to` cho `gd` ⇒ **ĐỎ**; bài `b3` nhét lại `khoa_to` ⇒ cổng quét (h) **ĐỎ** |
| AC-5 *(d)* | Kho TEST: lệnh VND + một dòng sổ USD chưa nối ⛔ khớp mã ⇒ `/so` trả dòng ấy `bac = 'khac_tien_te'`; ⛔ dòng khác tiền tệ nào mang `cung_tien_te` *(quét cả trang trả)*. `F01G` chip dòng ấy ~~chữ *"khác tiền tệ"*~~ ⭐ *(đính chính vòng 2, `TL-033 ⓑ`)* ký hiệu **`≠`** ＋ `title` *"khác tiền tệ"* ＋ chú giải hiện **chữ** *"khác tiền tệ"* *(`AC-13`)*; thân với `bac = 'xyz'` ⇒ chip in `xyz`, ⛔ *"cùng đơn vị tiền"* | bài cửa + bài DOM | trả nhánh `else` cũ ⇒ **ĐỎ**; thiếu `khac_tien_te` trong `BAC_XEP` ⇒ cửa `500` ⇒ **ĐỎ**; giữ `\|\| BAC.cung_tien_te` ⇒ **ĐỎ** |
| AC-6 *(e)* | `?gia_lap=rong`: mở hộp *Tìm tiền* ⇒ hộp **mở**, chứa `Không có dòng tiền nào ứng`; tab `④ Nạp sao kê` ⇒ `#nap-chon` có câu rỗng; **0** `Uncaught`/`TypeError` trên console. Bốn chế độ còn lại ⛔ đổi | bài DOM *(nạp chế độ giả lập thật)* + Chrome `AC-10` | trả `man_f01_lenh.js:578` / `man_f04.js:894` cũ ⇒ `TypeError` ⇒ **ĐỎ** |
| AC-7 *(f)* | `hinh.css`: cột số tiền `.cand-cols` ở **cả ba** khai báo *(`:747` + hai `@container`)* trừ `18px` + `5px` ≥ `ceil(18 × 0,6 × fs_than)` *(`fs_than` **đọc** từ `tokens.css`)*; DOM: `.cand .amt>span[title]` = đúng chuỗi in *(`TP.tien(v, c) + ' ' + c`)* trên thân cửa thật | bài đọc nguồn + bài DOM | bỏ `title` ⇒ **ĐỎ**; hạ cột về `150px` ⇒ **ĐỎ** |
| AC-8 *(g)* | Ba hộp *(F01 Ghép · F01 Bỏ cả chùm · F01L Ghép)*: ô lý do trống + bấm nút ⇒ **một** `POST` đi ra; trên kho TEST mỗi cú để lại `fls_queue_event.reason` bắt đầu `"(may dien) "`; placeholder ⛔ chứa `BẮT BUỘC`. Hộp `Hoãn` + `Mở lại` ô trống ⇒ **0** `POST` *(⛔ đổi)* | bài DOM *(đếm lời gọi `FLS.ghi`)* + bài cửa kho TEST | giữ `if (!v) … return false` ở một trong ba ⇒ **ĐỎ**; bỏ chặn ở `Hoãn` ⇒ **ĐỎ** |
| AC-9 ⭐ *(h — thân từ cửa thật)* | ⛔ **khuôn tự nhét**: mọi bài phiếu này thêm/sửa cho `F01L`/`F01G` dựng thân hộp/khối từ **cửa thật trên kho TEST**; cổng quét khoá mở rộng: khoá mà `ve_dang_gan` · `ve_o_gd` · `ve_thanh` · `ve_ung_vien` · `khop_dung_tien` · `_drawer_tim_tien` đọc từ thân ⊆ khoá cửa thật trả *(gọi HTTP kho TEST)*, **và** khoá trong mọi khuôn thử tự dựng cho cùng cửa ở `tests/web/**` ⊆ khoá cửa thật. Mẫu số in ra *(số cặp hàm × biến, số khoá)* ≥ **28** cặp `KQ-031` đã đo | bài quét *(mở rộng `test_wo022_v3_tim_tien_cua_that.py`)* | thêm `"khoa_to": [...]` tự đặt vào một khuôn mà cửa ⛔ trả ⇒ **ĐỎ**; màn đọc một khoá cửa ⛔ trả ⇒ **ĐỎ**; tập rỗng ⇒ **ĐỎ** |
| AC-10 ⭐ *(Chrome bấm thật trên 8099)* | Chrome **1440×900**, máy **8099** dựng `--cho-ghi` trỏ **kho TEST**, **chuột thật** *(`Input.dispatchMouseEvent`)*: ① hộp *Tìm tiền* ca VND↔USD cùng số ⇒ `khác tiền tệ` `crit` · ② ứng viên bậc `ma` lệch ⇒ ô `Lệch` có số · ③ màn ghép `F01G` khối *"Đang gán"* có `<mark>` trên diễn giải · ④ chế độ *Toàn sổ* dòng USD cạnh lệnh VND ⇒ chip *"khác tiền tệ"* · ⑤ `?gia_lap=rong` mở hộp ⇒ câu rỗng · ⑥ Ghép ở hộp *Tìm tiền* **ô lý do trống** ⇒ `200`, `reason` `"(may dien) …"`. Console **0** lỗi. ⭐ Kèm **8088 sổ thật CHỈ ĐỌC**: `PM00329-1` ⇒ hộp nói `khác tiền tệ`; `PM02117-1` hàng `36790` ô `Lệch` = `21.586,78` *(⛔ `—`)* | Chrome CDP; `BG` dán số đo từng ca + bản chụp DOM *(ảnh ⛔ lên git)* | JS trên `HEAD` khi nhận, cùng máy ⇒ ①②③④⑤⑥ sai ít nhất **5/6** |
| AC-11 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai + đúng **3 `XPASS(strict)`** `kq031` *(`F-1`/`F-2`/`F-3` — đúng ý, `fls-test` gỡ dấu)* · `lint-imports` 9/0 · `soi_bang_tuyen` khớp **40** tuyến *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.14** §5b ⓕ/ⓘ/ⓙ + *Năm trạng thái*; `02_BA/13_THUYET_MINH_MAN_HINH.md` **v1.6** ④. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(chỉ đổi **chữ** trong ô đã có + `title`; ⛔ token, ⛔ lớp CSS mới — chip *"khác tiền tệ"* dùng lại tông `lock`/`crit` đã có của `BAC`)*.

| Trạng thái | Hiện gì *(hộp Tìm tiền `F01L` · vùng ứng viên / khối Đang gán `F01G` · `F04`)* |
|---|---|
| tải | ⛔ đổi *(khung chờ, ⛔ số giả)* |
| rỗng | ⭐ `data: null` / thân rỗng ⇒ hộp *Tìm tiền* **mở** với *"⛔ Không có dòng tiền nào ứng"*; `F04` câu rỗng của khối `#nap-chon` — ⛔ `TypeError` |
| lỗi | ⛔ đổi *(hộp lỗi đúng câu cửa trả)* |
| mất kết nối | ⛔ đổi *(câu lỗi + `Thử lại`)* |
| có dữ liệu | ô `Tiền` kèm mã *(ⓙ)*; ô `Lệch` = số *(mọi bậc, cùng tiền tệ)* · `khác tiền tệ` · `—` *(thiếu số)*; câu so `crit` cho khác tiền tệ; khối *"Đang gán"* tô `<mark>` theo `khoa_to`; chip bậc *"khác tiền tệ"* ở *Toàn sổ*; ô chữ tiền vượt ngân sách ⇒ `…` + `title`; ô lý do ghép *tuỳ ý* |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** `fls_itl` / `fls_pm_line` / `fls_moi_noi` qua cửa có sẵn. Cửa **đọc** `lenh-cho` / `lenh-da-gan` / `itl-candidates` / `/so` thêm/đổi **giá trị trường** *(`lech`, `khoa_to`, `bac`)* — ⛔ tuyến mới, ⛔ SQL mới bắt buộc.
- Ghi kho THẬT: **`KHONG`**. Máy **8088** vẫn **CHỈ ĐỌC** *(chỉ `GET` cho `AC-10`)*. Mọi cú ghi *(`AC-8`, `AC-10` ⑥)* trên **kho TEST** qua máy **8099**.
- Số dòng sổ thật **chữ in** sẽ đổi *(đo trước — `KQ-031` qua cửa 8088 + `fls-ba` `SELECT` 02/10)*: ứng viên khác tiền tệ **165 / 5.360** *(rổ `may`, 268 lệnh)* — trong đó **4** lệnh đổi câu *"trong dung sai"* ⇒ *"khác tiền tệ"*; ứng viên bậc `ma` `—` ⇒ số **338 / 448**; `gd` thêm `khoa_to` **768 / 768**; mối nối khác tiền tệ **0 / 2.262** *(⇒ `gd` đã gán ⛔ bao giờ `lech = null` vì tiền tệ hôm nay)*; dòng toàn sổ đổi chip với một lệnh VND tối đa **3.926 / 6.165** *(trang 50 dòng)*.

## Nền khi nhận *(`fls-ba` đo / chép 02/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — commit giấy của `fls-ba` sau `e574a3b` *(`KQ-031`)*; mã `fls/**` cuối = `e0d2a96` *(`WO-022` vòng 3)* | `git log` |
| `pytest` | **`2187 passed, 6 xfailed`** *(`KQ-031` đo cuối lượt; 6 = 3 `kq021` của `WO-023` + 3 `kq031` của phiếu này)* ⇒ sau phiếu: 3 `kq031` thành `XPASS(strict)` *(đúng ý)*, 3 `kq021` **vẫn** `xfail` | `KQ-031` bảng cổng |
| `kiem_so_song` | **44** lệch *(`fls-ba` chạy 02/10 sau tờ giấy `BA-06` v4.14 / `BA-07` v3.7 / `BA-13` v1.6 + ô master §8: `⛔ CONG SO SONG KHONG DAT — 44 lech/khong-do-duoc` — = nền `KQ-031`)* | lệnh |
| `kiem_thuyet_minh` | `31/31` *(`fls-ba` chạy sau `BA-13` v1.6)* | lệnh |
| version spec | `BA-06` **v4.14** · `BA-07` **v3.7** · `BA-13` **v1.6** | header tệp |

## Câu còn treo
- **`Q-TIEN-1`** *(owner — chuyển từ [`WO-022`](WO-022-in-tien-theo-tien-te.md) khi đóng)*: **11** dòng sổ VND *(+ phía lệnh **2** dòng mỗi ảnh, **144** giá trị mọi ảnh; tổng `F03` `1.225.372.960.941,22` · chân màn `F01L` `54.871.038.986,74` — `KQ-029 F-4`)* mang phần lẻ: in **đủ** *(mặc định)* hay **làm tròn** về đồng? **Vì sao phiếu này vẫn làm được:** ⛔ chạm luật in §5b ⓑ; câu trả lời đổi **một** dòng ⓑ + **một** ca `AC-1` của `WO-022` — việc riêng.
- *(⛔ câu treo nào khác.)* Ô lý do tuỳ ý = lời owner `QĐ-ITL-149 ⓑ`; nghĩa `lech` / `khoa_to` / bậc `khac_tien_te` = thẩm quyền spec của `fls-ba`.

## Rủi ro
1. **Bậc mới `khac_tien_te`** chạm mọi chỗ liệt kê bậc *(`BAC_XEP` Python · `BAC`/`THU_TU_BAC` hai tệp JS · bài quét bậc nếu có)* — `grep` cả `fls/` lẫn `tests/` và ghi vào `BG`; thiếu một chỗ ở Python là `500` cho **cả trang** toàn sổ.
2. **Tính `lech` ở bốn chỗ** dễ thành bốn bản luật lệch nhau *(so tiền tệ có `trim`/chữ hoa ở chỗ này mà ⛔ ở chỗ kia)* — một hàm dùng chung; `AC-2` đo **quan hệ** trên cả bốn cửa.
3. **Kho TEST phình** *(bài dựng dữ liệu qua cửa thật)* ⇒ bài `*_pg` có thể đỏ vì `timeout` — dùng tiền ngẫu nhiên + `run_id` `NAP-2000-…` như `KQ-031`, ⛔ nới timeout, ⛔ `TRUNCATE`.

## ⭐ Vòng 2 *(02/10, `fls-ba` — [`TL-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md))*

### Vì sao có vòng 2
- [`HOI-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md): cửa `lenh-da-gan` ⛔ bao giờ trả bậc `ma` *(`xu_ly._bac` thiếu `ma_canon` vì cửa ấy ⛔ chạy `xep_ro`)*. `fls-ba` đo **toàn sổ thật, chỉ đọc**, gọi hàm thật mọi trang: mối nối `gd_ds` khớp mã **2.262 / 2.262** mà cửa trả `ma` **0** *(`tien` 2.128 · `cung_tien_te` 134)*; khối *"✓ Đang gán"* *(`gd`, một mỗi lệnh)* chip `②` **2.121** · `④` **98** · `①` **0 / 2.219**. `BA-07 §4h ⓵'` đã đòi `gd`/`gd_ds` **đúng khuôn `⓵`** ⇒ trong phạm vi `(c)`.
- `BG-034` yếu #7: ký hiệu bậc ở `F01G` chỉ có nghĩa trong `title` — **cả năm** `①②③④≠`, vì chú giải của `BA-06 §4.5 ⓒ ①` *(có trong bản dựng `Artifacts/fls-gan-lenh-chi_10.html:739`)* **⛔ được dựng** *(grep `tlegend`/`chu_giai` ở `fls/web/` + `tests/web/`: **0**)*.
- `BG-034` yếu #8: `man_f04.js` `_ve_thu_tu` `la_rong: d => !d.nguon` — cùng lớp `(e)`.
- ⛔ `BG-034` yếu #3 *(`/so` `500` khi dòng tiền `0`)* — **NGOÀI**, xếp `GAP-API-11` *(`BA-07` v3.8 §7; sổ thật **0 / 8.387**)*.

### Spec phải đọc *(vòng 2)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/07_API_CONTRACT.md` | **§4h ⓵'** đoạn v3.8 *(bậc `gd`/`gd_ds` so với `canon_ref(ref_tho)` của chính dòng lệnh, **cả hai** cửa danh sách)* · **§7** `GAP-API-11` *(đọc để biết NGOÀI)* | ⭐ **v3.8** |
| `02_BA/06_SCREEN_SPEC.md` | **§4.5 ⓒ ①** đoạn v4.15 *(chú giải bậc sinh từ `BAC`)* | ⭐ **v4.15** |
| `02_BA/13_THUYET_MINH_MAN_HINH.md` | `F01G` **ⓑ** Toàn sổ *(bậc `≠`)* | ⭐ **v1.7** |
| `01_Orchestrator/handoff/HOI-033-…md` | `TL-033` ⓐ ⓑ ⓒ ⓓ | — |

### Phạm vi vòng 2
| TRONG | NGOÀI |
|---|---|
| **(i) Bậc `ma` ở cửa `lenh-da-gan`** *(`⓵'` v3.8)*: gắn `ma_canon = canon_ref(ref_tho)` cho từng dòng **trước** `_gan_gd` ⇒ `_bac` trả `ma` cho mối nối khớp mã. ⭐ **Một** chỗ gắn dùng chung với `xep_ro` *(vd. tách dòng `lenh_cho.py:540` thành một hàm cả hai gọi)* — ⛔ bản thứ hai của phép chia `canon_ref` | ⛔ đổi `xep_ro` / bậc của `itl-candidates` + `lenh-cho` *(đã đúng)* · ⛔ đổi thứ tự bậc · ⛔ đổi `/so` |
| **(j) Chú giải bậc ở `F01G`** *(`BA-06 §4.5 ⓒ ①` v4.15)*: **một** dòng chú giải ở thanh tra cứu ứng viên *(chỗ bản dựng v10 `:739` đặt)*, chữ **sinh từ `BAC`** *(mỗi mục `k` ＋ `l`; ⛔ gõ tay)* ⇒ hôm nay 5 mục, có `≠ khác tiền tệ`; hiện ở **cả** *Máy đề xuất* lẫn *Toàn sổ*. Ô `.tg` từng dòng **giữ** ký hiệu ＋ `title` | ⛔ chữ bậc trên từng dòng · ⛔ đổi `.tg 22px` · ⛔ token mới *(⭐ cho phép **một** lớp CSS `.tlegend` lấy từ bản dựng v10, chỉ token có sẵn `--faint`/`--muted`/`--mono`/`--fs-nhan` — ngoại lệ có tên cho dòng "⛔ lớp CSS mới" ở mục *Màn hình*)* |
| **(k) `F04` `_ve_thu_tu` rỗng vẽ được**: `la_rong` khi `d` là `null` ⇒ câu rỗng *"Chưa đo được nguồn nào"* đã khai, ⛔ `TypeError` | ⛔ đổi bốn trạng thái kia của khối |

### Tiêu chí nghiệm thu vòng 2 *(`AC-1`…`AC-11` vòng 1 **vẫn** là đối tượng kiểm; `AC-2` ở cửa `lenh-da-gan` đo **đúng chữ** — phép thay thế của `BG-034` ⛔ được chấp nhận; `AC-5` theo chữ đính chính)*
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-12 *(i)* | **Kho TEST** qua HTTP `lenh-da-gan`: ca `B` của `ca_wo032.py` *(khớp đúng số CT, lệch `500`)* ⇒ `the.gd.bac = 'ma'` · `lech = '500.00'`; **`AC-2` nguyên chữ** ở cửa ấy *(≥1 ca bậc `ma` lệch ≠ 0)*. **Sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, gọi `lc.doc_lenh_da_gan` **mọi trang** + `xu_ly` hàm thật của cửa)*: mọi phần tử `gd`/`gd_ds` có `canon_ref(ref_tho) == canon_ref(doc_no)` ⇒ `bac = 'ma'`; in **mẫu số theo khoá** *(nền `fls-ba` 02/10: `gd_ds` **2.262**, `gd` **2.219**; cửa trả `ma` hôm nay **0**)* — mong **100%**, mẫu số > 0. Cửa `lenh-cho`: phân bố `bac` của `gd` trước/sau **bằng nhau** *(⛔ hồi quy)* | bài cửa `tests/api/` + một phép đo sổ thật chỉ đọc dán vào `BG` | bỏ gắn `ma_canon` ⇒ **ĐỎ**; gắn bằng bản `canon_ref` thứ hai *(vd. regexp)* ⇒ bài quét "một chỗ gắn" **ĐỎ**; tập khớp mã rỗng ⇒ **ĐỎ** |
| AC-13 *(j)* | Thân từ **cửa thật** kho TEST: danh sách ứng viên `F01G` có **đúng 1** chú giải hiện; với **mọi** khoá của `BAC`: `k` và `l` nằm trong **`textContent`** chú giải *(⛔ chỉ `title`)* — hôm nay **5/5**, có `≠` + `khác tiền tệ`; ở **cả hai** chế độ *(Máy đề xuất · Toàn sổ)*. Thêm một bậc giả vào `BAC` trong bài rồi vẽ lại ⇒ chú giải có mục ấy. Chrome `AC-10` ④ thêm: chú giải hiện chữ *"khác tiền tệ"* **⛔ bị cắt** *(`scrollWidth ≤ clientWidth`)* ở **1440×900**, cùng màn với dòng `≠`. `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh | bài DOM `man_f01_ghep.js` thật + Chrome | xoá chú giải ⇒ **ĐỎ**; chú giải gõ tay thiếu bậc mới ⇒ **ĐỎ**; chữ chỉ ở `title` ⇒ **ĐỎ** |
| AC-14 *(k)* | `_ve_thu_tu` nhận thân `null` *(đường thật — `TT.chay` với cửa trả rỗng)* ⇒ câu rỗng *"Chưa đo được nguồn nào"*, **0** `TypeError` | bài DOM `man_f04.js` thật | trả `d => !d.nguon` ⇒ `TypeError` ⇒ **ĐỎ** |
| AC-15 | Cổng như `AC-11` *(⛔ `dong_bo --ghi`)*; `kiem_so_song` tách **nền vòng 2** *(đo ở cổng vào, sau `BA-07` v3.8 / `BA-06` v4.15 / `BA-13` v1.7)* ⟷ đỏ mới loại (c), bảng cộng ra đúng tổng; `soi_bang_tuyen` **40** *(⛔ tuyến mới)* | lệnh + `BG` | — |

### Màn hình *(vòng 2)*
| Trạng thái | Hiện gì *(`F01G` chú giải · khối "Đang gán" · `F04` thứ tự ngày)* |
|---|---|
| tải | ⛔ đổi — chú giải ⛔ hiện khi danh sách đang chờ *(⛔ chú giải cho danh sách chưa có)* |
| rỗng | danh sách ứng viên rỗng ⇒ ⛔ chú giải *(⛔ có ký hiệu nào để giải)*; `F04` `_ve_thu_tu` `null` ⇒ *"Chưa đo được nguồn nào"* |
| lỗi | ⛔ đổi |
| mất kết nối | ⛔ đổi |
| có dữ liệu | chú giải một dòng `① khớp số chứng từ · ② đúng số tiền · ③ gần đúng số tiền · ④ cùng đơn vị tiền · ≠ khác tiền tệ` *(chữ từ `BAC`)*; khối *"Đang gán"* chip `① khớp số chứng từ` cho mối nối khớp mã |

### Dữ liệu *(vòng 2)*
- Ghi kho THẬT: **`KHONG`**. Sổ thật chỉ đọc *(phép đo `AC-12`)*; mọi ca dựng trên kho TEST.
- Chữ in sẽ đổi trên sổ thật *(`fls-ba` 02/10)*: chip khối *"Đang gán"* **2.219 / 2.219** lệnh đã gán → `①` *(từ `②` 2.121 · `④` 98)*.

### Nền khi nhận vòng 2 *(Dev đo lại, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | commit giấy `fls-ba` `TL-033` *(sau `7268e52`)*; mã `fls/**` cuối = `9c100ac` | `git log` |
| `pytest` | **3 failed = 3 `XPASS(strict)` `kq031`, 2208 passed, 3 xfailed** | `BG-034` |
| version spec | `BA-06` **v4.15** · `BA-07` **v3.8** · `BA-13` **v1.7** | header tệp |
| `kiem_so_song` | **49** *(`fls-ba` chạy 02/10 sau tờ giấy vòng 2 + master §8 theo version mới — = nền `BG-034`: 44 + 5 loại (c))* | lệnh |
| `kiem_thuyet_minh` | `31/31` *(sau `BA-13` v1.7)* | lệnh |

### Câu còn treo *(vòng 2)*
- ⛔ câu mới. `Q-TIEN-1` *(owner)* vẫn ⛔ chặn.

## Nghiệm thu PO *(`fls-ba` · 2026-10-02 — đọc `KQ-036` 15/15)*

Đối chiếu **ý owner** *(⛔ chỉ AC)*: phiếu này phải làm cho **màn nói đúng** cái cửa ghi sẽ làm — một cặp khác tiền tệ ⛔ được gọi *"trong dung sai"*, một số lệch ⛔ được giấu thành `—`, bằng chứng trong khối *"Đang gán"* phải tô được, và cú Ghép ⛔ còn đòi lý do *(`QĐ-ITL-149 ⓑ`)*.

| Ý owner / spec | Lời gốc | Đo được *(`KQ-036`)* | Khớp |
|---|---|---|:-:|
| `QĐ-ITL-149 ⓑ` — **"bỏ yêu cầu lý do cho cú Ghép"** | owner 01/10 | 8099 kho TEST, chuột thật + `POST` thật: ba hộp ô lý do trống ⇒ `200` ×3, `reason` bắt đầu `(may dien)`; `Hoãn` / `Mở lại` ô trống ⇒ **0** `POST` *(⛔ thuộc lời owner — giữ bắt buộc)* | ✅ |
| `QĐ-ITL-62` — ngoại tệ ⛔ dung sai; ⛔ so khác tiền tệ | owner 28/08 | 8088 sổ thật `PM00329-1` *(VND ↔ `100.000,00 USD`)* ⇒ `note crit` *"khác tiền tệ ⇒ ⛔ cửa ghi sẽ TỪ CHỐI"*; trước phiếu: *"trong dung sai"* ở **4** lệnh; `/so` khác tiền tệ mang `cung_tien_te` **0 / 552** | ✅ |
| **"Màn nói đúng"** — `lech` có số ở mọi bậc, `null` ⇔ khác tiền tệ *(`BA-07 §4h ⓵` v3.7)* | spec `fls-ba` | **0** sai `lech` / `khoa_to` / bậc `ma` trên **10.909** phần tử khuôn `⓵` của bốn cửa *(oracle `Decimal` độc lập)*; `PM02117-1` ô `Lệch` `21.586,78` *(trước `—`)* | ✅ |
| `B5` — kế toán đi hết một vòng ghép thật | `09` mốc `B` | khối *"Đang gán"* chip `①` **2.219 / 2.219** lệnh đã gán *(trước **0**)*; `<mark>` trên thân cửa thật; chú giải năm bậc hiện chữ *(5 / 5, ⛔ cắt ở 1440×900)* | ✅ |
| `C5` — ⛔ phải mở Excel tra một ô | `09` mốc `C` | ô `Tiền` kèm mã ở bảng trộn tiền tệ *(§5b ⓙ)*; `title` = chữ in **50 / 50** | ✅ |
| `QĐ-ITL-27` — kiểm soát nằm trong máy | owner 22/08 | cổng quét **43** cặp khoá màn ⊆ khoá cửa thật; **12** đột biến của Test, **11** bị bắt, `T12` lấp bằng bài `kq036` | ✅ |
| `QĐ-ITL-150 ⓑⓒ` — ⛔ `dong_bo --ghi` để làm xanh `BG` | owner 01/10 | `kiem_so_song` **49** = nền, tên trùng **49 / 49**, đỏ mới **0** | ✅ |

⇒ **ĐẠT — đóng phiếu.** ⚠ Một chỗ **"màn nói đúng" chưa trọn** mà ⛔ do diff của phiếu này *(`KQ-036 F-6`, ⛔ thuộc phạm vi — `(d)` NGOÀI *"⛔ đổi bậc ở hai cửa ứng viên máy đề xuất"*)*: cột *Giao dịch* in *"đề xuất: …"* một dòng tiền **khác tiền tệ** cho **84 / 268** lệnh rổ `may`, và rổ ấy nói *"máy trả lời được — người chỉ duyệt"*. `fls-ba` đo lại *(hàm thật, chỉ đọc)*: cả **84** lệnh **chỉ** khớp mã ở tiền tệ khác ⇒ lỗi nằm ở **phép chia rổ** *(⛔ đo theo cửa ghi)*, ⛔ ở thứ tự — đảo thứ tự sẽ đưa **45** ứng viên trùng tiền tình cờ lên đầu *(cửa ghi **nhận** ⇒ ghép sai)*. ⇒ `BA-07` **v3.9** `§4g ⓹` ⇒ [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md) *(ưu tiên **CAO**)*. `F-1`/`F-2`/`F-3` *(ca biên mẫu số **0** trên sổ thật)* + phần mã `F-4` *(chữ chú giải **2,17 : 1** ⇒ `NFR-I29`)* cũng vào `WO-037`; `F-5 ⓐ ⓒ` sửa giấy ngay *(`BA-07` v3.9 khai `ma_canon` · `BA-06` v4.16 gạch `.cand .amt .lech`)*; `F-5 ⓑ` ⇒ đính chính dưới.

### Đính chính *(chỉ thêm — `10` §4 luật 3)*
- `AC-4` cột **Chiều ĐỎ** *"bài `b3` nhét lại `khoa_to` ⇒ cổng quét (h) **ĐỎ**"* ⛔ đạt được bằng phép ⊆ khi cửa **đã** trả khoá ấy *(`KQ-036 F-5 ⓑ`, đột biến `T12` sống)*. Chiều ĐỎ đúng: *"bài `b3` tự đặt `khoa_to` ⇒ bài `kq036::test_CANH_bai_b3_KHONG_tu_nhet_khoa_to` ĐỎ"* — `fls-test` đã lấp. Chữ cũ giữ làm biên bản.

## Changelog
- 2026-10-02 · `fls-ba` · `CHO_TEST` vòng 2 → ✅ **`DONG`** — nghiệm thu PO *(bảng trên: 7 ý owner/spec khớp)*. Xếp `KQ-036`: `F-1`/`F-2`/`F-3`/`F-4` *(mã)*/`F-6` ⇒ spec `BA-07` **v3.9** · `BA-06` **v4.16** · `BA-08` **v1.3** ⇒ phát [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md); `F-5 ⓐ ⓒ` sửa giấy; `F-5 ⓑ` đính chính `AC-4`. `Q-TIEN-1` đi tiếp ở `WO-037`.
- 2026-10-02 · `fls-dev` · `DANG_LAM` vòng 2 → **`CHO_TEST`** — [`BG-035`](BG-035-ban-giao-wo-032-vong-2.md) @ `932d8a4`: `(i)` `lenh_cho.gan_ma_canon` — **một** chỗ gắn `ma_canon`, `xep_ro` + `xu_ly.lenh_da_gan` *(trước `_gan_gd`)* cùng gọi ⇒ sổ thật chỉ đọc `gd_ds` `ma` **0 → 2.262 / 2.262**, `gd` **0 → 2.219 / 2.219**, `lenh-cho` `268 / 268` ⛔ đổi; kho TEST ca `B` `bac = 'ma'` · `lech = '500.00'`, `AC-2` đo đúng chữ *(gỡ miễn trừ)* · `(j)` `F01G.ve_chu_giai` — một `.tlegend` sinh từ `Object.keys(BAC)`, cả hai chế độ, ⛔ khi rỗng; Chrome 1440×900 `990 = 990` px, một dòng; mã `363a441` **0** chú giải + chip `④` · `(k)` `F04._ve_thu_tu` `la_rong` chịu `null`. Bài mới **10** *(đỏ 10/10 trên `363a441`)* + **8/8** đột biến ĐỎ. `pytest` **3 failed = 3 `XPASS(strict)` `kq031`, 2218 passed, 3 xfailed** · `kiem_so_song` **49** = nền vòng 2, **0** tên mới · 40 tuyến · 31/31 · lint 9/0.
- 2026-10-02 · `fls-dev` · `MO` vòng 2 → **`DANG_LAM`** — cổng vào: git `363a441` = `origin` · `BA-06` **v4.15** · `BA-07` **v3.8** · `BA-13` **v1.7** khớp `Spec` vòng 2; `WO` đủ trường `10` §3.1. Nền sổ thật *(chỉ đọc, gọi `xu_ly.lenh_da_gan` + `xu_ly.lenh_cho` mọi trang)* khớp `TL-033`: `gd_ds` **2.262** khớp mã, `ma` **0** *(`tien` 2.128 · `cung_tien_te` 134)*; `gd` **2.219** *(`tien` 2.121 · `cung_tien_te` 98 · `ma` 0)*; `lenh-cho` `gd` `ma` **268 / 268**.
- 2026-10-02 · `fls-ba` · `CHO_TEST` → **`MO` vòng 2** — [`TL-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md): ⓐ phương án 2 *(sửa bậc `ma` ở `lenh-da-gan` trong phiếu — toàn sổ thật **0 / 2.262** mối nối khớp mã được trả `ma`; khối *"Đang gán"* `①` **0 / 2.219**)*; `AC-2` **giữ chữ** · ⓑ chip `≠` chưa đủ vì **cả năm** ký hiệu thiếu chú giải ⇒ `(j)` chú giải sinh từ `BAC`, `AC-5` đính chính chữ · ⓒ yếu #8 `F04` ⇒ `(k)`; yếu #3 ⇒ `GAP-API-11`. Spec `BA-07` **v3.8** · `BA-06` **v4.15** · `BA-13` **v1.7**. `BG-034` ⛔ kiểm riêng — `fls-test` kiểm gộp với `BG` vòng 2.
- 2026-10-02 · `fls-dev` · `DANG_LAM` → **`CHO_TEST`** — [`BG-034`](BG-034-ban-giao-wo-032.md) @ `9c100ac`: một hàm `lech_ung_vien` cho bốn cửa khuôn `⓵` *(`null` ⇔ khác tiền tệ / thiếu số)* · bậc `/so` `khac_tien_te` · `gd`/`gd_ds` đủ khuôn + `khoa_to` · hộp *Tìm tiền* so mã trước xu *(`crit` "khác tiền tệ ⇒ cửa ghi sẽ TỪ CHỐI")*, ô `Tiền` kèm mã · rỗng của màn vẽ được *(`F01L` + hai chỗ `F04`)* · `.cand .amt>span[title]` · ba hộp ô lý do tuỳ ý *(`Hoãn`/`Mở lại` giữ)*. `pytest` **3 failed = 3 `XPASS(strict)` `kq031`, 2208 passed, 3 xfailed** · `--runxfail kq031+kq029` **8 passed** · `kiem_so_song` **49 = nền 44 + 5 loại (c)** *(số dòng `fls/api`)* · cổng quét **43** cặp · Chrome 8099 **6/6** *(mã `a718142` cùng kịch bản: sai **6/6**)* · 8097 sổ thật chỉ đọc `PM00329-1` *khác tiền tệ* · `PM02117-1` `21.586,78`. `AC-2` ở `lenh-da-gan` đo *"lệch ≠ 0 cùng tiền tệ"* thay *"bậc `ma`"* ⇒ [`HOI-033`](HOI-033-lenh-da-gan-khong-bao-gio-co-bac-ma.md).
- 2026-10-02 · `fls-dev` · `MO` → **`DANG_LAM`** — cổng vào: git `a718142` = `origin` · `BA-06` **v4.14** · `BA-07` **v3.7** · `BA-13` **v1.6** khớp `Spec`; `WO` đủ trường `10` §3.1; nền `kiem_so_song` **44** *(tên trùng `KQ-031`)*.
- 2026-10-02 · `fls-ba` · phát **`WO-032`** `MO` từ nghiệm thu PO `WO-022`: gom `KQ-031` `F-1`…`F-4` + `KQ-029` `F-2`/`F-3` + hai lỗ `fls-ba` đo khi nghiệm thu *(bậc toàn sổ khác tiền tệ · ba hộp còn đòi lý do trái `QĐ-ITL-149 ⓑ`)*; spec `BA-06` **v4.14** · `BA-07` **v3.7** · `BA-13` **v1.6**. Ưu tiên **TRUNG BÌNH**, thứ tự `WO-032` → `WO-015` → `WO-023`. `Q-TIEN-1` chuyển sang đây, ⛔ chặn.
