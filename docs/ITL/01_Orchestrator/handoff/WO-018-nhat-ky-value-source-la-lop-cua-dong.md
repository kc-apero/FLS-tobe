# WO-018 — Nhật ký ghi `value_source` = **lớp của chính dòng** *(ai nói `value_after`)*, ⛔ nguồn trước khi gõ — cú `/adjust` của người và bản đảo tay

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(02/10 khuya — `fls-ba` nghiệm thu PO: [`KQ-025`](KQ-025-kiem-bg-024.md) ✅ ĐẠT **6/6 AC**, 0 `CHAN`/`NANG`; bảng đối chiếu ý owner ở mục **Nghiệm thu PO** cuối phiếu; `F-2` đính chính ở mục **Đính chính**)* · ~~⭐ **`CHO_TEST`**~~ *(02/10 khuya — [`BG-024`](BG-024-ban-giao-wo-018.md) @ `25f4b91`; `pytest` `2132 passed, 3 xfailed` *(3 = `xfail(strict)` có sẵn của Test)*)* · ~~`DANG_LAM`~~ *(02/10 khuya — `fls-dev` nhận: cổng vào git `b065794` = origin · `BA-05` v0.34 ✔ · `BA-06` đang **v4.11** ⇒ v4.10/v4.11 chỉ chạm `Bỏ gán` + in tiền, dòng *"F02 · nhật ký"* vẫn đúng chữ v4.9 ⇒ ⛔ `HOI`)* · ~~`MO`~~ · ưu tiên **THẤP-VỪA** *(sổ thật hôm nay **0** dòng sai; nhưng dòng sai đầu tiên sẽ nằm **vĩnh viễn** — nhật ký chỉ-thêm `INV-I08`)* *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Vòng** | `1` |
| **Phát bởi** | `fls-ba` · 2026-10-02 |
| **Nhận** | `fls-dev` |
| **Thứ tự với phiếu khác** | ⭐ **SAU [`WO-008`](WO-008-chu-man-sau-bo-ghep.md) ĐẠT** *(phiếu này lật **một** `assert` trong bài của chính `WO-008` — `tests/web/test_wo008_than_that_bo_ghep_pg.py` ~`:107`; làm trước khi `fls-test` kiểm `BG-017` là đổi thước dưới chân người kiểm)* · ⭐ **TRƯỚC [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md)** *(lý do: lỗ của `WO-015` là **cổng đếm** — tính lại được bất cứ lúc nào; lỗ của phiếu này là **dòng nhật ký** — ghi sai thì ⛔ sửa được. Hai phiếu đều thêm bài ⇒ nối đuôi để `BG` tách đỏ loại c)* |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(tác vụ ① mapping)* — cú sửa tay thật đầu tiên của kế toán trên `F02` *(lằn người, cổng `C8` *"người đã chốt ô nào"*)*. Người ấy mở nhật ký ⑦ ngay sau khi gõ: hôm nay màn in nguồn **`UNMAPPED`** *(ô rỗng trước khi gõ)* hay **`nguon`** *(ô có sổ gốc)* thay cho *"người sửa"*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ phiếu này **⛔ xoá thêm** mắt xích. Nó giữ đúng cái đã thay người kiểm thứ hai: `QĐ-ITL-16`/`QĐ-ITL-27` bỏ bước duyệt, **thay bằng nhật ký `AUD-1`** *(hậu kiểm)*. Nhật ký gọi sai *"người hay máy nói con số này"* là hậu kiểm đọc sai — đúng rủi ro số một của `QĐ-ITL-27`.

## Căn cứ
- [`HOI-016`](HOI-016-nhat-ky-value-source-la-nguon-truoc-khi-go.md) ⓑ *(`fls-dev` 02/10)* + `TL-016` *(`fls-ba` 02/10)* — một cột hai nghĩa: dòng máy *(`ghi_tay.py:571`)* và bản đảo bỏ ghép *(`:973`)* ghi **lớp của chính dòng**; cú `/adjust` *(`:446`)* ghi **nguồn trước khi gõ**.
- `AUD-1` *(`BA-04`, `QĐ-ITL-16` — owner)*: nhật ký phải có *"nguồn giá trị (máy suy/người nhập/sửa lại)"* — nguồn của giá trị **được ghi**.
- `INV-I21` *(`BA-11` v0.14, `QĐ-ITL-143`/`QĐ-ITL-149` — owner 01/10: *"Máy gợi ý"*)*: *"ai bấm"* *(`actor`)* và *"ai nói con số"* *(`nguon`)* là **hai câu**.
- Quyết: **`fls-ba` trong thẩm quyền spec** — phiếu này ⛔ đổi *"con số trên màn đến từ đâu"*; nó đưa cửa ghi về **định nghĩa owner đã chốt** *(`AUD-1`)*.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/05_DATA_DICTIONARY_ERD.md` | `DD-I15 ⓓe` *"`fls_journal.value_source` nghĩa là gì"* *(mới)* · `ⓓd` dòng *"`actor` là ai"* | ⭐ **v0.34** |
| `02_BA/06_SCREEN_SPEC.md` | §5 dòng *"F02 · nhật ký trong drawer"* — đoạn ⭐⭐ *v4.9* | ⭐ **v4.9** |
| `01_Orchestrator/handoff/HOI-016-…md` | ⓑ *(bằng chứng + ca xấu)* · `TL-016` | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **`T1` — cửa ghi duy nhất `_them`** *(`fls/repo/ghi_tay.py` ~`:290`–`:330`)*: `fls_journal.value_source` **=** `nguon` của bút toán chèn cùng giao dịch. Dev chọn cách *(bỏ tham số `value_source` và ghi `nguon` · hay giữ tham số mà **NO** khi `value_source != nguon`)*; `BG` ghi cách và vì sao | ⛔ Migration *(cột `adj_id` trong `fls_journal`, `CHECK` trên `value_source`)* — kho TEST cũ còn mã `nguon`/`UNMAPPED`; muốn `CHECK` thì phiếu riêng |
| **`T2` — `ghi_but_toan`** *(`:444`–`:449`)*: dòng nhật ký của cú gõ người ⇒ `value_source = 'sua_tay'`. ⭐ Thân trả của cửa *(`KetQuaGhi.value_source`, `fls/api/xu_ly.py:239`)* **GIỮ** nghĩa *"nguồn đang có trước khi gõ"* — đó là câu của cửa `before-edit`/modal `409` *(`US-025`)*, ⛔ của nhật ký | ⛔ Đổi thân trả cửa `/adjust`, `before-edit`, `GET /journal` *(`BA-07` ⛔ đổi)* |
| **`T3` — `dao_but_toan`** *(`:478`–`:485`, ghi cứng `NGUON_TAY`)*: bản đảo mang `nguon` **và** `value_source` **bằng dòng bị đảo** — như `bo_moi_noi` đã làm *(`:969`–`:973`)*. Hôm nay đảo một dòng `may_goi_y` qua cửa đảo sẽ ghi bản đảo `nguon='sua_tay'` | ⛔ Đổi luật **ai được đảo dòng nào** *(`SM-I03`)* |
| **`T4` — chú thích cột** `fls/db/schema.py:180` *(`"nguon goi y luc go"`)* ⇒ nghĩa mới *(lớp của chính dòng = `fls_adjustment.nguon` cùng giao dịch)*; chuỗi log `tools/demo_dong.py:884` *(`value_source='nguon'/'UNMAPPED'`)*. Chú thích chảy vào hiện vật ERD thì sinh lại *(cổng `G-ERD-1`)* | ⛔ Sửa tay `ERD-*.mmd`/`ERD-CONTRACT.json` |
| **`T5` — bài thử** *(`tests/repo/**`, `tests/web/**`, `tests/api/**` — ⛔ `tests/nghiem_thu/`)*: bài mới cho mỗi AC, **chứng minh ĐỎ trước** *(`Đ5`)*. Sửa bài đang **ghim nghĩa cũ**: `tests/repo/test_ghi_tay_pg.py:136` *(`NGUON_TRONG`)* · `tests/web/test_vong_f02_pg.py:237` *(`"nguon"`)* · `tests/web/test_wo008_than_that_bo_ghep_pg.py` ~`:98`–`:110` *(ghim `("HD-K7B", "UNMAPPED")`)*. `BG` liệt kê từng `assert` đã đổi: `tệp:dòng · cũ → mới` | ⛔ Sửa dòng nhật ký **cũ** trên bất kỳ kho nào *(`INV-I08` — chỉ thêm)* · ⛔ đổi mã màn `fls/web/**` *(`BA-06` v4.9: màn đúng khi cửa ghi đúng)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(ca xấu `HOI-016`)* | Kho TEST: một dòng có `hd_thyt = 'HD-MAY'`; người `/adjust` `hd = 'HD-NGUOI'` *(`force` + lý do)* ⇒ **đúng 1** dòng nhật ký mới, `value_source = 'sua_tay'`; thân `GET /journal` thật đưa vào màn `F02` ⑦ ⇒ hàng ấy ô **thành** = `HD-NGUOI`, ô **nguồn** = *"người sửa"*; **0** hàng chứa *"gợi ý: HD-NGUOI"* | bài `tests/web/` khuôn `test_wo008_than_that_bo_ghep_pg.py` *(cửa thật trên kho TEST ⇒ màn)* | trả `:446` về `value_source=t["value_source"]` ⇒ hàng in *"gợi ý: HD-NGUOI"* · *"máy gợi ý · không đổi Final"* ⇒ **ĐỎ** |
| AC-2 *(dòng B `KQ-007`)* | Dòng B *(ghép → 2 lớp gợi ý → người gõ `hd = HD-K7B` → bỏ ghép)*: hàng người in `("HD-K7B", "người sửa")`; số hàng *"rút gợi ý"* vẫn = số bản đảo *(≥ 4)*; nhãn *"người sửa"* xuất hiện **đúng 1** lần | `test_AC2…` của `WO-008` — đổi **đúng** phần ghim nguồn *(`BG` dán diff)* | như AC-1 ⇒ hàng người ra `UNMAPPED` ⇒ **ĐỎ** |
| AC-3 *(bất biến cặp)* | Kho TEST, một kịch bản đi qua **đủ** đường ghi: `ghi_but_toan` trên ô rỗng · ô có nguồn sổ · ô có `*_thyt` · ô đã có người; `ghi_goi_y` *(ghép tay)*; `bo_moi_noi`; `dao_but_toan` trên một dòng `sua_tay` **và** một dòng `may_goi_y` ⇒ đa tập `(itl_id, field, at, actor, value_source)` của `fls_journal` **=** đa tập `(itl_id, field, at, actor, nguon)` của `fls_adjustment` trên các dòng của kịch bản. Mẫu số **≥ 9** cặp, in ra *(`Đ3` — 0 cặp ⇒ ⛔ không đo được)* | bài `tests/repo/` mới *(so **đa tập**, ⛔ nối khoá — bỏ ghép đảo 2 lớp `hd` trong **một** giao dịch ⇒ khoá 4 cột trùng)* | giữ `NGUON_TAY` cứng ở `dao_but_toan` ⇒ cặp của bản đảo dòng máy lệch ⇒ **ĐỎ**; trả `:446` như cũ ⇒ **ĐỎ** |
| AC-4 *(cửa ⛔ đổi)* | Thân trả `/adjust` vẫn mang `value_source` = **nguồn trước khi gõ**: `tests/api/test_cua_ghi_pg.py:241` *(`"UNMAPPED"`)* và `:292` *(`"nguon"`)* xanh **⛔ sửa một chữ** | `pytest tests/api/test_cua_ghi_pg.py` + `git diff <nền> -- tests/api/test_cua_ghi_pg.py` rỗng | đổi luôn `KetQuaGhi.value_source` thành `sua_tay` ⇒ hai bài **ĐỎ** |
| AC-5 *(sổ thật ⛔ đổi)* | Kho THẬT *(chỉ `SELECT`)*: phép đếm cặp của AC-3 trên toàn sổ ra **N / N** bằng nhau *(02/10: **4.428 / 4.428**)*; `fls_journal` theo `value_source` ⛔ đổi *(02/10: `may_goi_y` **4.424** · `sua_tay` **4**)* | câu `SELECT` dán nguyên văn + kết quả vào `BG` | — *(phép đo, ⛔ bài)* |
| AC-6 | `pytest` toàn bộ xanh *(⛔ `xfail`)* · `lint-imports` **9 kept 0 broken** · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh · `git diff <nền> -- tests/nghiem_thu/ fls/web/` **rỗng** · `kiem_so_song`: `BG` ghi nền lúc nhận ⟷ đỏ **mới** loại c của phiếu; ⛔ `dong_bo --ghi` *(`10 §6 ⓒ`)* | lệnh ở `CLAUDE.md` | — |

## Màn hình
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.9** dòng *"F02 · nhật ký"* — **⛔ đổi mã màn**; chữ trên màn đổi vì **dữ liệu** cửa trả đổi.

| Trạng thái | Hiện gì |
|---|---|
| tải | ⛔ đổi |
| rỗng | ⛔ đổi — *"nhật ký trống — chưa ai sửa dòng này"* |
| lỗi | ⛔ đổi |
| mất kết nối | ⛔ đổi |
| có dữ liệu | hàng của cú gõ **người** từ nay in nguồn *"người sửa"* *(trước: `UNMAPPED` / `nguon` / *"máy gợi ý · không đổi Final"* tuỳ ô trước khi gõ)*; hàng máy và bản đảo ⛔ đổi |

## Dữ liệu
- Bảng/cột chạm: `fls_journal.value_source` *(giá trị ghi **mới**)* · `fls_adjustment.nguon` của bản đảo qua `dao_but_toan`. ⛔ Cột mới, ⛔ migration.
- Ghi kho THẬT: **`KHONG`**. Mọi bài chạy kho TEST *(`dsn_test()`)*.
- Số dòng sổ thật chạm *(đếm 02/10, chỉ `SELECT`)*: **0** — `fls_journal` **4.428** dòng, ⛔ dòng nào từ `/adjust` *(4.424 máy `may@fls` + 4 UAT đường ghép cũ)*; `fls_adjustment` ⛔ bản đảo nào qua `dao_but_toan`. Ô `*_thyt` ≠ `NULL`: **0** / 8.387 dòng `fls_itl`.

## Câu còn treo
- ⛔ **Không câu nào chặn.** Nghĩa cột đã có định nghĩa owner chốt *(`AUD-1`)*; phiếu đưa mã về đúng định nghĩa.

## Rủi ro
1. **Cột hai nghĩa theo thời gian** — chỉ xảy ra trên kho có dòng `/adjust` cũ. Sổ thật **0** *(AC-5)* ⇒ ⛔ xảy ra; kho TEST dựng lại mỗi lượt. Nếu trước khi phiếu này `DONG` kế toán đã gõ thật trên `F02` ⇒ `BG` đếm lại, báo `fls-ba` *(dòng ấy mang nghĩa cũ vĩnh viễn — ghi tên vào `BA-05 ⓓe`)*.
2. **Mất *"nguồn trước khi gõ"* trong một dòng nhật ký** — chấp nhận *(`BA-05 ⓓe`)*: đọc lại từ dòng nhật ký trước của cùng ô, hay sổ gốc. ⛔ Nhét nó vào `reason`.
3. **Bài `WO-008` đang ghim nghĩa cũ** — sửa **đúng** `assert` ấy, ⛔ xoá bài; `BG` dán diff.

## Đính chính *(`KQ-025 F-2` — chỉ THÊM; bảng AC ở trên giữ nguyên làm biên bản)*

`fls-test` đo bằng đột biến *(worktree tạm, `KQ-025` mục *Soi 6 chỗ Dev tự thấy còn yếu* #2, #3)*: **hai vế** của cột *"Chiều ĐỎ"* trong bảng AC viết **sai** — mã và bài của Dev **đúng**, chữ của phiếu sai. Ai đọc lại phiếu này sẽ tưởng bài đa tập canh được bản đảo.

| AC | Chữ phiếu đã viết | Đo được *(`KQ-025`)* | Đọc đúng là |
|---|---|---|---|
| `AC-3` vế `dao_but_toan` | *"giữ `NGUON_TAY` cứng ở `dao_but_toan` ⇒ cặp của bản đảo dòng máy lệch ⇒ **ĐỎ**"* | đột biến `T1` *(giữ `NGUON_TAY` cứng)* ⇒ `test_AC3_da_tap…` **XANH**: mã cũ ghi `sua_tay` ở **cả hai** bảng *(`fls_adjustment.nguon` lẫn `fls_journal.value_source`)* nên cặp vẫn **bằng nhau** — phép so đa tập **⛔ thấy** lỗi này | Phép so đa tập chỉ canh **cặp nhất quán** *(hai bảng nói cùng một lớp)*. Lỗi *"bản đảo mang sai lớp"* là lỗi **so với dòng bị đảo** ⇒ phải có bài **riêng** so lớp bản đảo với lớp **dòng gốc**: bài thứ hai của Dev *(đỏ ở `T1`, `T2`, `T4`)* + `kq025::test_c_*` *(bắt `T3` — lấy lớp theo **ô** thay vì theo **dòng**, bộ bài Dev sống sót)* |
| `AC-4` vế `:292` | *"đổi luôn `KetQuaGhi.value_source` thành `sua_tay` ⇒ **hai** bài ĐỎ"* | đột biến *thân trả `ghi_but_toan` ⇒ `NGUON_TAY`* ⇒ `3 failed` = `test_cua_ghi_pg::…:241` + `test_ghi_tay_pg` ×2; `:292` **XANH** | `:292` canh cửa `before-edit` *(`truoc_khi_go`)*, ⛔ đi qua `KetQuaGhi` ⇒ chiều ĐỎ của `AC-4` là **`:241`** *(và hai bài `test_ghi_tay_pg`)*, ⛔ *"hai bài `:241` + `:292`"*. Phần **mong** *(cả hai xanh, ⛔ sửa chữ nào)* vẫn đúng và đã ĐẠT |

⇒ Bài học cho các `WO` sau *(luật `Đ5`)*: một dòng *"Chiều ĐỎ"* là một **dự đoán**; `fls-ba` viết nó mà ⛔ chạy đột biến ⇒ ghi rõ *"chưa chứng minh"*, để `BG`/`KQ` đo thay vì tin.

## Nghiệm thu PO *(`fls-ba` · 2026-10-02 khuya — đọc `KQ-025` ĐẠT 6/6)*

Đối chiếu **ý owner** *(⛔ chỉ AC)*: phiếu này phải làm cho nhật ký nói đúng *"ai nói con số này"* — người hay máy — vì nhật ký là thứ **thay người kiểm thứ hai**.

| Ý owner / spec | Lời gốc | `KQ-025` đo | Khớp |
|---|---|---|:-:|
| `QĐ-ITL-149` — `hd`/`cdt1` khi ghép là **máy gợi ý**, Final ⛔ đổi | owner 01/10: *"Máy gợi ý"* | 8099 chuột thật `Đảo` dòng máy ⇒ ⑦ *"rút gợi ý · máy gợi ý · không đổi Final"*, `fls_sua_tay` **0 → 0**; bản đảo dòng máy mang `may_goi_y` *(`kq025::test_a_*`, `::test_c_*`)* | ✅ |
| `QĐ-ITL-16` `AUD-1` — nhật ký có *"nguồn giá trị (máy suy/người nhập/sửa lại)"* | `BA-04` `AUD-1` | người gõ đè ô có `*_thyt` ⇒ đúng 1 dòng `sua_tay`, ⑦ in *"người sửa"*, **0** hàng *"gợi ý: HD-NGUOI"* *(`AC-1`, 8099 **B**)*; cặp bút toán ⇔ nhật ký **10/10** qua cửa HTTP *(`kq025::test_e_*`)* | ✅ |
| `TL-016` ⓑ — nghĩa cột = **lớp của chính dòng**; thân trả `/adjust` **giữ** *"nguồn trước khi gõ"* | `fls-ba` 02/10 | `_them` là **chỗ duy nhất** chèn `fls_journal` và **NO** khi `value_source ≠ nguon` *(grep toàn repo)*; thân trả 8099 `value_source='may_goi_y'` *(nguồn trước khi gõ)*; `test_cua_ghi_pg.py` diff **0** dòng | ✅ |
| `INV-I08` — nhật ký chỉ-thêm; ⛔ sửa dòng cũ | `BA-11` | sổ thật trước/sau **11/11** trùng `KQ-021`; cặp **4.428 / 4.428** *(`may_goi_y` 4.424 · `sua_tay` 4)* | ✅ |
| `QĐ-ITL-27` — 2–3 kế toán, kiểm soát nằm trong máy | owner 22/08 | luật nằm ở **cửa ghi** *(cưỡng chế)*, ⛔ ở lời dặn; 6 đột biến của Test bị bắt, `T3` nhờ bài `kq025` | ✅ |
| `QĐ-ITL-150 ⓑⓒ` — ⛔ `dong_bo --ghi` để làm xanh một `BG` | owner 01/10 | `git log b065794..803889e` = 2 commit, ⛔ commit `dong_bo`; `kiem_so_song` 43 = nền 34 + 9 loại c *(`fls-ba` đo lại 02/10 khuya: **43**)* | ✅ |

⇒ **ĐẠT — đóng phiếu.** Bốn `F` `NHE` của `KQ-025` ⛔ lỗi của diff này: `F-2` sửa ngay ở mục **Đính chính** trên · `F-1` ⇒ khối `SINH-KHOP` sinh lại ngay + mở rộng [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) **(e)** · `F-3` + `F-4` ⇒ `BA-06` **v4.12** + `BA-07` **v3.6** ⇒ [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) **(f)** + **(g)**.

## Changelog
- 2026-10-02 khuya · `fls-ba` · ✅ **`DONG`** — nghiệm thu PO từ `KQ-025` ĐẠT 6/6 *(6 ý owner/spec khớp)*; thêm mục **Đính chính** cho chiều ĐỎ `AC-3`/`AC-4` *(`KQ-025 F-2`)* — bảng AC giữ nguyên làm biên bản.
- 2026-10-02 · `fls-ba` · phát từ `TL-016` ⓑ *(`HOI-016`, thuộc `WO-008`)*: phần **đổi nghĩa cột ghi** tách khỏi `WO-008` *(màn ⛔ đổi)*; thứ tự sau `WO-008` ĐẠT, trước `WO-015`.
