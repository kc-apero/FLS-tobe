# WO-008 — Chữ trên màn sau một cú bỏ ghép: nhật ký ⛔ đọc như "ô bị xoá" · hộp "Đã bỏ ghép" nói theo Ô · màn ghép báo `bo_qua`

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(02/10 khuya — `fls-ba` nghiệm thu PO, xem mục **Nghiệm thu PO**; [`KQ-021`](KQ-021-kiem-bg-020.md) ✅ ĐẠT **8/8** AC vòng 2, `AC-1`…`AC-6` ⛔ hồi quy)* · ~~**`CHO_TEST` — VÒNG 2**~~ *(`fls-dev` 02/10 tối — [`BG-020`](BG-020-ban-giao-wo-008-vong-2.md) @ `9dae3ac` + `dd7c5bb`; `pytest` đỏ **đúng 5** `XPASS(strict)` `kq019` — đúng mong `AC-13`)* · ~~`DANG_LAM` — VÒNG 2~~ *(`fls-dev` nhận 02/10 tối — cổng vào: `HEAD` = `origin` `124a067` · `BA-06` **v4.10** khớp `Spec` vòng 2; mục **Vòng 2** đủ trường `10` §3.1 ⇒ ⛔ `HOI`; nền `kiem_so_song` đầu vòng 2 đo trên `124a067`: **34** lệch = **13** loại (b) + **21** loại (c))* · ~~`MO` — VÒNG 2 · SẴN SÀNG~~ *(`fls-ba` mở lại 02/10 chiều theo [`KQ-019`](KQ-019-kiem-bg-017.md) TRƯỢT — `10 §2` bước ④: cùng hàm `man_f01_ghep.js::bo_gan` của Phạm vi `(c)` ⇒ **cùng** phiếu; việc ở mục **Vòng 2** cuối phiếu; ⭐ làm **TRƯỚC** `WO-018` → `WO-015`)* · vòng 1: ~~**`CHO_TEST`**~~ *(`fls-dev` 02/10 — [`BG-017`](BG-017-ban-giao-wo-008.md) @ `69f03f6`; [`HOI-016`](HOI-016-nhat-ky-value-source-la-nguon-truoc-khi-go.md) ✅ đã trả `TL-016` 02/10 — ⛔ mở lại; Phạm vi (a)(b) + `AC-1` **đính chính**; phần đổi nghĩa cột ghi ⇒ [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md))* · ~~`DANG_LAM`~~ *(`fls-dev` nhận 02/10 — cổng vào: `HEAD` = `origin` `d761d0f` · `BA-06` v4.8 · `BA-10` v0.8 khớp; `T0` xong ở `948ffb6`)* · ~~`MO` · ⭐ **SẴN SÀNG — làm NGAY**~~ *(02/10 chiều: `WO-001` ✅ `DONG` · `WO-011` ✅ `DONG`; rà lại sau `WO-011` — mục **Rà 02/10**)* · ưu tiên **THẤP** *(⛔ chặn gì; sổ thật hôm nay ⛔ dòng nào hiện ra khác)* · ~~làm SAU `WO-001`~~ *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-01 tối |
| **Nhận** | `fls-dev` |
| **Vòng** | `2` · vòng 1 phát 01/10 tối *(`BG-017` · `KQ-019` TRƯỢT: **6/6** AC ĐẠT, **2** `NANG` + **2** `NHE` trên `bo_gan`)* · vòng 2 mở 02/10 chiều |
| **Thứ tự với phiếu khác** | ⭐ **TRƯỚC [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md)**; ~~**SAU `WO-001`**~~ đã thoả *(`WO-001` + `WO-011` đều `DONG`)*. Câu gốc: Lý do: phiếu này thêm bài thử ⇒ số phép thử ghim trôi *(loại c)*; làm trước thì `WO-001 T5` phải chụp lại số, làm sau thì đỏ loại (c) là của **chính** phiếu này và `BG` tách được |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(tác vụ ① mapping)* — cổng `B4` *(bỏ ghép trên sổ thật)*. Người bỏ ghép thật đầu tiên phải **đọc đúng** cái máy vừa làm: rút gợi ý nào, giữ giá trị người nào.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: **"SHQ1 / SHQ2 → chuẩn hoá & mapping"** — ⛔ xoá thêm mắt xích; phiếu này giữ cho mắt xích đã xoá *(ghép/bỏ ghép trên màn FLS — `WO-003`)* **⛔ sinh ra một câu hỏi mới** *("ô của tôi bị xoá à?")* mà người phải đi hỏi ai đó mới trả lời được — đúng rủi ro số một của `QĐ-ITL-27` *(việc phải sống sót khi người rời đi; nhật ký đọc sai = mất vết)*.

## Căn cứ
- [`KQ-007`](KQ-007-kiem-bg-006.md) *(`fls-test` 01/10 tối — `WO-003` vòng 2 ĐẠT)* — ba phát hiện `NHE` gửi `BA`:
  - `F-1`: bản đảo của lớp **⛔ hiệu lực** ghi nhật ký *"X → (trống)"* ⇒ người đọc `F02` ⑦ tưởng ô bị xoá *(đo kho thử `P5`, `P1`)*.
  - `F-2`: hộp *"Đã bỏ ghép"* in tên ô lặp *"cdt1, hd, hd, cdt1"* khi gợi ý chồng lớp.
  - `F-3`: nút `Bỏ gán` của màn ghép **bỏ** thân trả ⇒ `bo_qua` ⛔ hiện; `BA-06:1174` chỉ khai *"phải hiện"* cho `F01`/`F02`.
- `QĐ-ITL-149` *(owner 01/10: hai ô `hd`/`cdt1` khi ghép là **"Máy gợi ý"**)* — căn cứ để nói *"gợi ý máy ⛔ bao giờ là Final"* trên màn.
- Quyết định chữ màn: **`fls-ba` trong thẩm quyền spec** *(chỉ là cách **hiển thị** dữ liệu cửa đã trả — ⛔ đổi cửa, ⛔ đổi sổ, ⛔ đổi "con số đến từ đâu")*.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | §5 dòng *"F02 · nhật ký trong drawer"* *(⭐ v4.8 — `F-1`)* · dòng *"F01/F02 · nút Bỏ ghép"* *(⭐ v4.8 — `F-2`)* · mục ⓔ *Hộp thoại BỎ GÁN* đoạn ⭐ *"v4.8 — BÁO SAU khi bỏ gán"* *(`F-3`)* | **v4.8** |
| `02_BA/10_DECISION_TABLE.md` | `DT-I14` đoạn ⭐ *"Nhật ký của bản đảo — đọc thế nào"* · *Định nghĩa `bo_qua`* | **v0.8** |
| `01_Orchestrator/handoff/KQ-007-kiem-bg-006.md` | `F-1`, `F-2`, `F-3` *(tái hiện + thân trả thật của dòng B)* | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a) `F-1` — nhật ký `F02` ⑦** *(`fls/web/tep/man_f02.js` khối `// ⑦ Nhat ky`, ~`:1764`–`1777`)*: cột **thành** + **nguồn** đọc theo `value_source` của từng dòng — ⓐ `may_goi_y` có giá trị ⇒ *"gợi ý: X"*; ⓑ `may_goi_y` **rỗng** ⇒ *"rút gợi ý"* *(⛔ ô trống)*; ⓒ `sua_tay` ⇒ như nay. Cột nguồn in nhãn: `may_goi_y` ⇒ ~~*"máy gợi ý · ⛔ đổi Final"*~~ ⭐ *"máy gợi ý · không đổi Final"* *(đính chính `TL-016` — luật ký hiệu)* · `sua_tay` ⇒ *"người sửa"* · giá trị khác/rỗng ⇒ in nguyên mã *(⛔ đoán nhãn)* | ⛔ Đổi luật **ghi** nhật ký *(`value_before` = lớp bị rút, `value_after` = `NULL` — `BA-10` v0.8 giữ)*. ⛔ Thêm cột `adj_id`/`reversal_of` vào `fls_journal` *(⛔ migration)*. ⛔ Đổi cửa `GET /ledger/{id}/journal`. ⛔ Ca nhánh 8 *(`sua_tay` cũ dưới người — sổ thật **0**, tập đóng; `BA-06` v4.8 ghi "chấp nhận")* |
| **(b) `F-2` — hộp "Đã bỏ ghép"** *(`fls/web/tep/man_f01.js::_bao_bo_ghep`, ~`:423`–`440`)*: câu đảo nói theo **ô** — *"↩ Đã rút gợi ý máy trên **N ô** (`cdt1, hd`)"*; mỗi tên ô **một lần**, theo thứ tự xuất hiện đầu tiên trong `but_toan_dao`; khi `but_toan_dao.length > N` thêm *"· M bút toán, gồm lớp gợi ý cũ bị đè"*. Khối `bo_qua` *(cảnh báo "người đã gõ tay")* ~~**giữ** như nay~~ ⭐ giữ **câu** cảnh báo, mỗi mục in thêm **giá trị người** *(`hd = HD-K7B`)* *(đính chính `TL-016` ⓐ — khớp `AC-4`)* | ⛔ Đổi thân trả của cửa `unmatch` *(gộp ô là việc của **màn**, cửa vẫn trả từng bút toán — sổ cần từng `adj_id`)* |
| **(c) `F-3` — màn ghép báo `bo_qua`** *(`fls/web/tep/man_f01_ghep.js::bo_gan`, ~`:567`–`600`)*: đọc thân trả của `FLS.ghi('/queue/…/unmatch', {})`; `bo_qua` **⛔ rỗng** ⇒ mở **chính** hộp *"Đã bỏ ghép"* của `F01` *(gọi lại hàm dựng — ⛔ bản câu thứ hai)*, một nút `Đã hiểu`; `bo_qua` **rỗng** ⇒ ⛔ hộp nào, về lệnh như hôm nay. Hàm dựng **đã được xuất** *(`man_f01.js:740` trả `_bao_bo_ghep` — `KQ-007` gọi được `F01._bao_bo_ghep`)* | ⛔ Hộp **hỏi trước** khi bỏ gán *(ca 1 lệnh — `BA-06` mục ⓔ cấm)*. ⛔ Báo `but_toan_dao` trên màn ghép khi `bo_qua` rỗng *(mỗi cú bỏ gán rút 2 gợi ý ⇒ báo mỗi lần = tiếng ồn — `BA-06` v4.8)*. ⛔ `GAP-SCR-33` *(lằn GIÁ TRỊ)* |
| ⭐ **`T0` *(thêm 02/10 — làm ĐẦU TIÊN, commit riêng)***: `tools/dong_bo_so_song.py --ghi` **một lần** trên `HEAD` sạch, **trước** khi sửa mã — dọn đỏ nền loại *b/c* sau `KQ-014` + phiếu `fls-ba` 02/10 *(đo 02/10 chiều: **8** lệch trên **7** phép so — số phép thử `2051 → 2084` ×6 · bài ngoài module `269 → 302` · số tệp `103 → 105`)*; sửa câu cạnh số theo `10 §6 ⓑ`. ⛔ phải *"dọn đỏ của một `BG` khác"* *(`10 §6 ⓒ`)*: `KQ-014` đã ĐẠT, `WO-011` đã `DONG` ⇒ đỏ ấy là **nền chung** | ⛔ Chạy `--ghi` lần thứ hai ở cuối phiếu *(đỏ của chính phiếu này để `BG` tách — `AC-6`)* |
| **Bài thử của Dev** *(`tests/web/**`, `tests/repo/**` — trừ `nghiem_thu/`)*: một bài cho mỗi AC dưới, **chứng minh ĐỎ trước** *(`Đ5`)*. ⭐ Ít nhất **một** bài dựng thân từ **cửa thật** trên kho TEST *(ghép → `ghi_goi_y_may` chồng lớp → người `/adjust` → bỏ ghép)* rồi đưa thân ấy vào màn — ⛔ chỉ khuôn tự nhét *(bài học `11` §6: khuôn thử tự nhét state che chỗ màn ⛔ gọi cửa)* | ⛔ Sửa / thêm bài trong `tests/nghiem_thu/**` — việc của `fls-test` |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a)* | Nhật ký `F02` ⑦ của một dòng có **4** loại dòng *(`may_goi_y` có giá trị · `may_goi_y` rỗng · `sua_tay` có giá trị · `sua_tay` rỗng)* ⇒ ô **thành** lần lượt *"gợi ý: X"* · *"rút gợi ý"* · `X` · trống; ô **nguồn** ~~*"máy gợi ý · ⛔ đổi Final"*~~ ⭐ *"máy gợi ý · không đổi Final"* ×2 · *"người sửa"* ×2. Mẫu số: bảng vẽ ra **4** hàng *(⛔ 0 — `Đ3`)* | bài DOM `tests/web/` *(khuôn `dom_gia.js` + `khung_node.py` như `test_luoi_f02_hanh_vi.py`)*, đọc chữ từng ô | Trả ô thành về `TP.chu(x.value_after)` ⇒ hàng 2 ra rỗng ⇒ **ĐỎ**; in `value_source` thô ⇒ **ĐỎ** |
| AC-2 *(a)* | Trên kho TEST, dòng **B** của `KQ-007` *(ghép tay `hd`+`cdt1` → 2 lớp `ghi_goi_y_may` → người gõ `hd` → bỏ ghép)*: thân `GET /ledger/{id}/journal` đưa vào màn ⇒ **mọi** hàng `value_source='may_goi_y'` có `value_after` rỗng in *"rút gợi ý"*; **0** hàng `may_goi_y` in ô thành trống; hàng người gõ in giá trị người | bài `tests/web/test_vong_f02_pg.py` *(hay tệp mới cùng khuôn)*: đếm hàng theo chữ, mẫu số = số bản đảo trong `fls_adjustment` của dòng *(≥ 4)* | như AC-1 |
| AC-3 *(b)* | Thân trả thật của cú bỏ ghép dòng B *(`but_toan_dao` = `[cdt1, hd, hd, cdt1]`)* ⇒ hộp in *"2 ô"* · *"4 bút toán"*; mỗi chuỗi `cdt1`, `hd` xuất hiện **đúng 1** lần trong câu đảo. Thân một lớp *(`[cdt1, hd]`)* ⇒ *"2 ô"*, ⛔ đuôi *"bút toán"* | bài DOM: gọi `_bao_bo_ghep(than)`, đếm chuỗi trong nốt `↩` | Trả về `dao.map(...).join(', ')` ⇒ `hd` đếm **2** ⇒ **ĐỎ** |
| AC-4 *(c)* | Màn ghép, bấm `Bỏ gán` *(lệnh 1 dòng tiền, ⛔ chùm)*: cửa trả `bo_qua=[{field:'hd', value_after:'HD-K7B'}]` ⇒ **1** hộp mở, chứa `hd` và `HD-K7B`, nút duy nhất `Đã hiểu`; cửa trả `bo_qua=[]` ⇒ **0** hộp *(đếm lần gọi `HT.mo`/`HT.hoi` sau `unmatch`)* | bài DOM trên `man_f01_ghep.js` với `FLS.ghi` giả trả **thân thật** của dòng B *(chép từ AC-2)* | Bỏ đọc thân *(`await FLS.ghi(...)` không gán)* ⇒ 0 hộp khi `bo_qua` ⛔ rỗng ⇒ **ĐỎ**; mở hộp cả khi `bo_qua` rỗng ⇒ **ĐỎ** |
| AC-5 | `pytest` toàn bộ: **0** đỏ ngoài bài mới đã xanh · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp *(⛔ tuyến nào đổi)* · `kiem_thuyet_minh` khớp *(⛔ nút mới — hộp chỉ có `Đã hiểu`)* · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh *(chữ mới ⛔ mang ký hiệu/màu chưa khai)* | lệnh ở `CLAUDE.md` | — |
| AC-6 | `BG` ghi `kiem_so_song`: nền **sau `T0`** *(⭐ phải **0** lệch; ~~sau `WO-001 T5`~~)* ⟷ đỏ **mới** do phiếu này *(loại c — số phép thử)*; ⛔ chạy `dong_bo --ghi` để dọn đỏ của chính phiếu *(`10 §6 ⓒ` — `BG` tách, `fls-ba` quyết lượt `--ghi` kế tiếp)* | đọc `BG` | — |

## Màn hình *(chạm UI)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.8** *(ba chỗ ở bảng Spec)* · bản dựng `SCR-F01`/`SCR-F02` ở `02_BA/Artifacts/` **⛔ đổi** *(chỉ đổi chữ trong ô bảng và nội dung một hộp đã có)*.

| Trạng thái | Hiện gì |
|---|---|
| tải | ⛔ đổi — nhật ký `F02` ⑦ và màn ghép giữ trạng thái tải hiện có *(`WO-003 AC-10`)* |
| rỗng | nhật ký ⛔ dòng ⇒ *"nhật ký trống — chưa ai sửa dòng này"* *(như nay)*; bỏ gán mà `bo_qua` rỗng ⇒ ⛔ hộp |
| lỗi | cửa `unmatch` lỗi ⇒ như nay *(lỗi trong hộp, ⛔ mở hộp "Đã bỏ ghép")* |
| mất kết nối | như nay *(⛔ Cửa lỗi: Không nối được tới máy chủ FLS.)* — ⛔ hộp "Đã bỏ ghép" khi ⛔ có thân trả |
| có dữ liệu | ba chỗ chữ mới ở bảng Phạm vi `(a)`·`(b)`·`(c)` |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** thân cửa `GET /ledger/{id}/journal` *(`fls_journal`)* và `POST /queue/{id}/unmatch` *(kho TEST)*.
- Ghi kho THẬT: **`KHONG`**. Mọi bài chạy kho TEST *(`dsn_test()`)*; máy 8088 vẫn **CHỈ ĐỌC**.
- Số dòng sổ thật chữ mới **sẽ** chạm *(đếm 01/10 tối, chỉ để biết)*: `fls_journal` `may_goi_y` có giá trị **4.424** *(đổi nhãn nguồn + "gợi ý: X")* · `may_goi_y` rỗng **0** · `sua_tay` **4** *(2 có giá trị + 2 rỗng — cả 4 là UAT `27728`)* · `fls_sua_tay` **0** ⇒ hộp `(c)` bật **0** lần hôm nay.

## Câu còn treo
- ⛔ **Không câu nào chặn.** Ba quyết định là **chữ trên màn** của dữ liệu cửa đã trả — `fls-ba` quyết trong thẩm quyền spec *(`BA-06` v4.8)*. Owner muốn câu khác *(vd. ⛔ báo `bo_qua` trên màn ghép)* thì đổi một đoạn spec + một bài — ⛔ chặn phiếu.
- *(ngoài phạm vi, chờ owner)* `GAP-SCR-33` — lằn **GIÁ TRỊ** *(màn hiện gợi ý `hd`/`cdt1` + nút gật)*. Khi mở, nhãn *"gợi ý: X"* của `(a)` là chỗ đặt nút gật tự nhiên.

## Rủi ro
1. **Luật ký hiệu màn:** chữ mới *("⛔ đổi Final", "↩")* phải qua `test_luat_ky_hieu_man_hinh.py` — ký hiệu ngoài danh mục thì dùng chữ trơn, ⛔ thêm ký hiệu mới.
2. **Hai bản câu:** màn ghép phải gọi **chính** hàm dựng hộp của `F01`; chép câu sang `man_f01_ghep.js` là đẻ ra bản thứ hai sẽ già lệch *(`AC-4` dùng chuỗi của `AC-3`)*.
3. **Nhánh 8** vẫn in *"trống"* với nguồn *"người sửa"* trên kho thử — `fls-test` đừng nâng thành `F`: spec v4.8 ghi rõ chấp nhận *(sổ thật 0, tập đóng)*.

## Rà 02/10 chiều *(`fls-ba`, sau `WO-011` `DONG`)*
| Câu hỏi | Đo *(02/10)* | Kết luận |
|---|---|---|
| `WO-011` có chạm tệp màn nào của phiếu này? | `88ab178` đổi hằng ở `fls/repo/may_ghep.py`, `nhip_chup.py` *(`KQ-014` lăng kính Màn hình)*; `git log --since=2026-10-01 -- fls/web` ⇒ chỉ `48fb68f` *(`WO-003`)* | ⛔ chạm |
| Neo dòng trong Phạm vi còn đúng? | `man_f02.js:1764` `// ⑦ Nhat ky` · `man_f01.js:423` `function _bao_bo_ghep` · `:740` xuất `_bao_bo_ghep` · `man_f01_ghep.js:567` `async function bo_gan` | ✅ trùng |
| Spec còn đúng version? | `BA-06` **v4.8** · `BA-10` **v0.8** *(dòng `Version` đầu tệp)* | ✅ |
| Số trong mục Dữ liệu còn đúng? | `fls_journal` **4.428** = 4.424 máy + 4 UAT · `fls_sua_tay` **0** *(`KQ-014` đếm lại 8/8 bảng khớp)* | ✅ — hộp `(c)` vẫn bật **0** lần trên sổ thật |
| Luật *"người thật"* mới có đổi chữ màn? | Hộp `bo_qua` nói *"người đã gõ tay"* theo `value_source = 'sua_tay'` — đó là **nguồn giá trị** trên màn, ⛔ phải cổng *người đã làm* *(`09` §2 ⓔ)* ⇒ ⛔ lọc UAT/máy ở màn | ⛔ đổi phạm vi |
| Nền cổng | `pytest` **2.084** *(`KQ-014`: 2.051 + 33 bài `kq014`)* · `lint-imports` **9 kept 0 broken** · `kiem_so_song` **8** lệch *(7 phép so)* loại b/c *(02/10 chiều, trước commit này; sau commit `fls-ba` số tệp thành **105**)* · `kiem_tai_lieu` ĐẠT · `khop_owner --kiem` **17/20** | ⇒ thêm `T0` |

## Vòng 2 — `KQ-019` `F-1` · `F-2` · `F-3` · `F-4` *(+ đính chính `F-5`)*

**Vì sao mở lại cùng phiếu, ⛔ tách phiếu mới:** cả bốn phát hiện nằm trong **chính** hàm `fls/web/tep/man_f01_ghep.js::bo_gan` mà Phạm vi `(c)` vòng 1 sửa; `10 §2` bước ④ *"TRƯỢT ⇒ mở lại **cùng** WO"*. `F-1` là **lỗi mã** *(gọi một hàm ⛔ có)*; `F-2`/`F-3` có **phần spec** *(câu v4.8 *"về lệnh như hôm nay"* ngầm giả định màn tự nói; dòng *lỗi*/*mất kết nối* của mục **Màn hình** vòng 1 tả một câu ⛔ có trên màn ghép)* ⇒ `fls-ba` sửa spec trước *(`BA-06` **v4.10**)*. Vòng 2 chỉ **thêm** `AC-7`…`AC-14`; `AC-1`…`AC-6` đã phán **ĐẠT** ở `KQ-019` — ⛔ đo lại trừ khi vòng 2 làm chúng đổi *(`AC-4` đo lại qua `AC-9`: hộp `bo_qua` vẫn mở **1** lần)*.

### Căn cứ vòng 2
- [`KQ-019`](KQ-019-kiem-bg-017.md) *(`fls-test` 02/10 chiều)*: `F-1` `NANG` *(`HT.hoi` ⛔ tồn tại ⇒ bỏ gán chùm / đa giao dịch chết im — `TypeError`, **0** hộp, **0** lượt `/unmatch`)* · `F-2` `NANG` *(sau `200` màn vẫn *"Đang gán"*, bấm lại `409` im)* · `F-3` `NHE` *(lỗi cửa chỉ ra console)* · `F-4` `NHE` *(`mo_lenh` ném ⇒ hộp `bo_qua` ⛔ mở)* · `F-5` `NHE` *(bảng tách `BG-017`)*.
- Đo lại 02/10 *(`fls-ba`, kho thật chỉ `SELECT`)*: `fls_moi_noi` **2.262** mối nối / **2.222** dòng tiền / **2.219** lệnh · lệnh gắn ≥ 2 dòng tiền **23** · dòng tiền mang chùm **25** · lệnh đi nhánh hỏi *(hợp hai tập)* **88 / 2.219** *(4,0% — khớp `KQ-019`)* · `fls_sua_tay` **0** ⇒ **100%** cú bỏ gán hôm nay có `bo_qua` rỗng ⇒ ⛔ hộp nào ⇒ ca ③ là **tín hiệu duy nhất** người bấm nhận được.
- `grep -rhno "HT\.[a-z_]*" fls/web/tep/*.js` *(02/10)*: `HT.mo` **21** · `HT.loi_trong_hop` **9** · `HT.hoi` **2** *(`man_f01_ghep.js:582`, `:593`)*; `hop_thoai.js` xuất `{ mo, dong, loi_trong_hop }` ⇒ `HT.hoi` **0** chỗ định nghĩa trong `fls/`. Chỗ che: `tests/web/test_wo008_chu_man_sau_bo_ghep.py:181` *(bẫy `BAY_HOP` tự định nghĩa `HT.hoi`)* — **1** chỗ.
- Quyết định màn: **`fls-ba` trong thẩm quyền spec** *(cách trình bày dữ liệu cửa đã trả — ⛔ đổi cửa, ⛔ đổi sổ)*. ⛔ Câu nào thuộc owner.

### Spec phải đọc *(vòng 2)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | §4.5 mục ⓔ *Hộp thoại BỎ GÁN* — đoạn ⭐⭐ **v4.10 "NĂM ca của nút `Bỏ gán`"** *(bảng ①…⑤ + bảng 5 trạng thái + nợ `409`)* | **v4.10** |
| `fls/web/tep/hop_thoai.js` | chú thích đầu tệp *(ba luật ⓐⓑⓒ)* + chữ ký `mo(tieu_de, than, nut)` *(nút trả `false` ⇒ hộp ở nguyên)* + `loi_trong_hop(e)` | `HEAD` |
| `fls/web/tep/man_f01.js` | ⑥ `_bo_ghep` *(mẫu hộp hỏi gọi cửa **trong** nút, lỗi `HT.loi_trong_hop` + `return false`)* · `_bao_bo_ghep` | `HEAD` |
| `fls/repo/man_ghep.py` | `khuon_the_lenh` *(bộ ba `trang_thai` / `trang_thai_nhan` / `trang_thai_mau`)* | `HEAD` |
| `01_Orchestrator/handoff/KQ-019-kiem-bg-017.md` | `F-1`…`F-4` *(tái hiện 8099)* + bảng *Bài thử mới* | — |

### Phạm vi vòng 2
| TRONG | NGOÀI |
|---|---|
| **(d) `F-1`** — `bo_gan` ca ① *(lệnh ≥ 2 dòng tiền)* + ca ② *(chùm)* dựng hộp bằng **`HT.mo`** đúng `BA-06` v4.10: ① hộp báo một nút `Đã hiểu`, **0** lượt ghi; ② hộp hỏi `Thôi` · `Gỡ cả N`, gọi `/unmatch` **trong** hàm nút, lỗi ⇒ `HT.loi_trong_hop(e)` + `return false`. Gỡ bẫy `HT.hoi` khỏi `tests/web/test_wo008_chu_man_sau_bo_ghep.py` *(bài của Dev — ⛔ `nghiem_thu/`)*; bài nhánh hộp nạp `hop_thoai.js` **THẬT** | ⛔ Thêm hàm `hoi` *(hay hàm hộp nào)* vào `hop_thoai.js`. ⛔ Đổi luật *"chỉ hỏi ở ca chùm"* *(`BA-06` ⓔ — ca 1 lệnh–1 dòng tiền vẫn **⛔ hộp hỏi**)* |
| **(e) `F-2`** — sau `200`: ⓐ thẻ đổi **tại chỗ** theo `da_bo[]` của thân trả *(mọi lệnh có mặt trong `ST.dong`)*, bộ ba trạng thái **trùng** `khuon_the_lenh` cho lệnh ⛔ gán; ⓑ **một dòng tín hiệu** *"↩ Đã bỏ gán khỏi giao dịch #&lt;itl_id&gt; — lệnh về Chưa gán. Sổ giữ lịch sử."* *(chùm: *"· gỡ cả N lệnh chi"*)*; ⓒ hộp `bo_qua` như vòng 1; ⓓ lệnh ở yên chỗ. Nút `Bỏ gán` **khoá** trong lúc chờ cửa | ⛔ Tải lại cả danh sách. ⛔ Hộp báo khi `bo_qua` rỗng *(v4.8 giữ — tín hiệu là một **dòng**, ⛔ hộp)*. ⛔ Đổi cửa `unmatch` / `lenh-da-gan` |
| **(f) `F-3`** — `bo_gan` bắt mọi `LoiCua` của `/chum` + `/unmatch` ngoài hộp ⇒ dòng *"Bỏ gán chưa xảy ra — Cửa lỗi: &lt;e.cau&gt;"* + `e.lam_gi` + `e.chi_tiet` trong khối hành động; thẻ giữ `Đã gán`; **0** `Uncaught` | ⛔ Banner `ST.loi` thay cả màn. ⛔ Đổi câu trong `goi_cua.js` *(nợ `409` sai nghĩa — `BA-06` v4.10, phiếu khác)* |
| **(g) `F-4`** — thứ tự: ⓐⓑⓒ của (e) **trước** lượt đọc lại `itl-candidates`; lượt đọc lỗi ⇒ dòng *"Chưa tải lại được giao dịch gợi ý: &lt;câu&gt;"*, ⛔ nói bỏ gán lỗi | — |
| Bài thử của Dev *(`tests/web/**`)*: một bài cho mỗi AC dưới, **chứng minh ĐỎ trước** *(`Đ5`)*; bài màn nạp `hop_thoai.js` **THẬT** — ⛔ bẫy định nghĩa hàm `HT` mà tệp thật ⛔ xuất *(bài học `11` §6, đúng lớp `KQ-019` bắt)* | ⛔ Sửa / gỡ dấu 5 bài `xfail(strict)` trong `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py` — việc của `fls-test` |

### Tiêu chí nghiệm thu vòng 2
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-7 *(d · ca ②)* | Chùm 2 lệnh *(`/chum` `can_hoi=true`, `so_dong=2`)*: bấm `Bỏ gán` ⇒ **1** hộp thật mở *(`#scrim.on`)*, tiêu đề chứa *"CẢ 2"*, thân chứa **cả 2** mã lệnh, nút đúng `["Thôi", "Gỡ cả 2"]`; `/unmatch` **0** lượt trước khi bấm nút. Bấm `Thôi` ⇒ `/unmatch` **0**, hộp đóng. Bấm `Gỡ cả 2` ⇒ `/unmatch` **1**, rồi hành vi ca ③ *(cả 2 thẻ trong `ST.dong` thành `Chưa gán`)*. `Gỡ cả 2` gặp cửa lỗi ⇒ hộp **ở nguyên**, câu lỗi trong `#dlg-b` | ⓐ `pytest --runxfail "tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[chum]"` **xanh** *(⛔ `--runxfail` ⇒ `XPASS(strict)` đỏ — đúng mong, `fls-test` gỡ dấu)*; ⓑ bài Dev `tests/web/` với `hop_thoai.js` thật: **bấm nút thật** `Thôi` / `Gỡ cả 2` *(gọi `onclick` của phần tử trong `#dlg-f`)*, đếm `_GOI` theo `/unmatch` | Gọi lại `HT.hoi` ⇒ `TypeError` ⇒ **ĐỎ**; gọi `/unmatch` trước khi bấm ⇒ **ĐỎ**; `Thôi` vẫn ghi ⇒ **ĐỎ**; nuốt lỗi trong hộp *(⛔ `return false`)* ⇒ hộp đóng ⇒ **ĐỎ** |
| AC-8 *(d · ca ①)* | Lệnh `itl_da_gan=[4242, 4243]`: **1** hộp, chữ chứa *"2 giao dịch"* và *"Sổ ITL"*, nút đúng `["Đã hiểu"]`; `/chum` **0**, `/unmatch` **0**. ⭐ `grep -rn "HT\.hoi" fls/web/tep` = **0** · định nghĩa `HT.hoi` trong `tests/web/**` = **0** *(hôm nay **2** chỗ gọi · **1** bẫy)* | ⓐ `pytest --runxfail "…::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[da_giao_dich]"` xanh; ⓑ bài Dev; ⓒ hai lệnh `grep` | Gọi `/chum` hay `/unmatch` ở ca ① ⇒ **ĐỎ**; thêm lại bẫy `HT.hoi` ⇒ `grep` ra **1** ⇒ **ĐỎ** |
| AC-9 *(e)* | Lệnh 1 dòng tiền, cửa `200`, `bo_qua=[]`: `#ghep-goc` **⛔ chứa** *"Đang gán với giao dịch"* *(mẫu số: **có** trước cú bấm — `Đ3`)*; **chứa** *"Đã bỏ gán khỏi giao dịch #4242"*; chip thẻ = `trang_thai_nhan` của `khuon_the_lenh` cho lệnh ⛔ gán; nút `Gán` có, nút `Bỏ gán` ⛔ có; hộp **0**; lệnh vẫn là `ST.mo` *(ở yên)*. Với `bo_qua=[hd]`: thêm hộp *"Đã bỏ ghép"* **1** lần *(`AC-4` giữ)* | ⓐ `pytest --runxfail "…::test_F2_sau_bo_gan_THANH_CONG__man_khong_con_noi_DANG_GAN"` xanh; ⓑ bài Dev **đo quan hệ**: gọi **hàm thật** `fls.repo.man_ghep.khuon_the_lenh` với `itl_da_gan=[]` lấy bộ ba, so với bộ ba màn đặt sau bỏ gán *(⛔ chép hằng `"Chưa gán"` vào bài)* | Bỏ bước cập nhật thẻ ⇒ khối *"Đang gán"* còn ⇒ **ĐỎ**; đổi nhãn trong JS khác `khuon_the_lenh` ⇒ bài quan hệ **ĐỎ**; bỏ dòng tín hiệu ⇒ **ĐỎ**; gọi `tai_danh_sach` ⇒ đếm lượt `lenh-da-gan`/`lenh-cho` > 0 ⇒ **ĐỎ** |
| AC-10 *(e · tải)* | Hai cú bấm `Bỏ gán` liền nhau khi cửa **chưa** trả ⇒ `/unmatch` **đúng 1** lượt; nút mang `disabled` trong lúc chờ | bài Dev: cửa giả treo lời *(Promise chưa resolve)*, gọi `bo_gan` hai lần / bấm nút hai lần, đếm `_GOI` | Bỏ khoá ⇒ **2** lượt ⇒ **ĐỎ** |
| AC-11 *(f)* | Cửa `/unmatch` ném `FLS-MAT-KET-NOI` *("Không nối được tới máy chủ FLS.")* và `FLS-INTERNAL` ⇒ `#ghep-goc` chứa *"Bỏ gán chưa xảy ra"* + câu cửa; thẻ giữ `Đã gán`; hộp *"Đã bỏ ghép"* **0**; promise của `bo_gan` **resolve** *(⛔ reject — đại diện cho **0** `Uncaught`)*. `/chum` ném ⇒ cùng hành vi, `/unmatch` **0** | ⓐ `pytest --runxfail "…::test_F3_bo_gan_cua_LOI__nguoi_THAY_loi"` xanh; ⓑ bài Dev hai mã lỗi + `/chum` lỗi, bắt `.catch` của `bo_gan` ⇒ phải **⛔ gọi** | Bỏ `try/catch` ⇒ promise reject ⇒ **ĐỎ**; chỉ `console.error` ⇒ chữ ⛔ có trên màn ⇒ **ĐỎ** |
| AC-12 *(g)* | `200` với `bo_qua=[hd]`, rồi `itl-candidates` lỗi ⇒ hộp *"Đã bỏ ghép"* **mở**, chứa `HD-NGUOI-B2`; `#ghep-goc` chứa *"Đã bỏ gán khỏi giao dịch"* **và** *"Chưa tải lại được giao dịch gợi ý"*; ⛔ chứa *"Bỏ gán chưa xảy ra"* | ⓐ `pytest --runxfail "…::test_F4_ve_lai_lenh_LOI_sau_bo_gan__hop_bo_qua_VAN_mo"` xanh; ⓑ bài Dev đọc chữ màn | Đặt `await mo_lenh` **trước** hộp + thẻ *(như vòng 1)* ⇒ **ĐỎ**; báo *"chưa xảy ra"* khi sổ đã ghi ⇒ **ĐỎ** |
| AC-13 | `pytest` toàn bộ: **0** đỏ **ngoài** đúng **5** `XPASS(strict)` của `test_kq019_*` *(`BG` liệt kê từng tên — chúng đỏ **vì** vòng 2 sửa đúng; `fls-test` gỡ dấu như `KQ-005`/`KQ-007`)* · `pytest --runxfail tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py` **8/8** xanh · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp *(⛔ tuyến đổi)* · `kiem_thuyet_minh` khớp *(cổng đỏ vì nút hộp ⇒ mở `HOI`, ⛔ tự khai thay `fls-ba`)* · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh | lệnh ở `CLAUDE.md` | — |
| AC-14 | `BG` ghi `kiem_so_song`: nền **đầu vòng 2** *(đo trên `HEAD` trước commit mã đầu tiên, tách loại (b) nhịp chụp / (c) phiếu)* ⟷ đỏ **mới** loại (c) do vòng 2 *(số phép thử / số tệp)*; bảng tách **cộng ra đúng tổng** *(bài học `F-5`)*; ⛔ chạy `dong_bo --ghi` | đọc `BG` + `fls-test` chạy lại | — |

### Màn hình vòng 2 *(vùng `Bỏ gán` của màn ghép — `BA-06` v4.10)*
- Thiết kế: bảng ①…⑤ + bảng 5 trạng thái ở `BA-06` v4.10 mục ⓔ. Bản dựng `SCR-F01` ở `02_BA/Artifacts/` **⛔ đổi** *(một dòng chữ trong khối hành động + hai hộp dựng bằng khuôn `HT.mo` đã có)*. Lớp CSS: dòng tín hiệu dùng lớp ghi chú **đã có** *(`note ok` như hộp `F01`)*, dòng lỗi dùng `note crit` *(như `HT.loi_trong_hop`)* — ⛔ token / màu mới.

| Trạng thái | Hiện gì |
|---|---|
| tải | nút `Bỏ gán` khoá trong lúc chờ `/chum` / `/unmatch` *(`AC-10`)* |
| rỗng | lệnh ⛔ gán ⇒ ⛔ nút `Bỏ gán` *(như nay)* · `bo_qua` rỗng ⇒ ⛔ hộp, **chỉ** dòng tín hiệu |
| lỗi | ngoài hộp: *"Bỏ gán chưa xảy ra — Cửa lỗi: …"* trong khối hành động, thẻ giữ `Đã gán` *(`AC-11`)* · trong hộp chùm: `HT.loi_trong_hop`, hộp ở nguyên *(`AC-7`)* |
| mất kết nối | như lỗi, câu *"Không nối được tới máy chủ FLS."* *(`AC-11`)* · ⭐ **đính chính vòng 1** *(⛔ xoá câu cũ)*: dòng *lỗi*/*mất kết nối* của mục **Màn hình** vòng 1 ghi *"như nay (⛔ Cửa lỗi: …)"* — trên màn ghép câu ấy **⛔ có** cho cú bấm *(chỉ có cho lượt tải danh sách)*; `KQ-019 F-3` |
| có dữ liệu | thẻ `Chưa gán` + dòng *"↩ Đã bỏ gán khỏi giao dịch #…"* *(`AC-9`)* · + hộp `bo_qua` khi ⛔ rỗng · + dòng *"Chưa tải lại được…"* khi đọc lại lỗi *(`AC-12`)* |

### Dữ liệu vòng 2
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** thân `GET /queue/{itl_id}/chum` + `POST /queue/{itl_id}/unmatch` *(kho TEST)*.
- Ghi kho THẬT: **`KHONG`**. Máy 8088 vẫn **CHỈ ĐỌC**; bấm thật chỉ trên máy kho TEST *(như `KQ-019`, `--cho-ghi` trên `fls_test`)*.
- Số lệnh sổ thật hành vi mới **sẽ** chạm *(đếm 02/10, chỉ để biết)*: ca ① **23** lệnh · ca ② **25** dòng tiền *(hợp hai ca **88** lệnh)* · ca ③ mọi **2.219** lệnh đã gán *(tín hiệu dòng)* · hộp `bo_qua` bật **0** lần *(`fls_sua_tay` 0)*.

### Câu còn treo vòng 2
- ⛔ **Không câu nào chặn.** Năm ca là cách màn **trình bày** dữ liệu cửa đã trả — `fls-ba` quyết trong thẩm quyền spec *(`BA-06` v4.10)*. Owner muốn khác *(vd. hộp báo sau **mỗi** cú bỏ gán thay dòng tín hiệu)* thì đổi một đoạn spec + một bài, ⛔ chặn phiếu.
- *(ngoài phạm vi — nợ đã ghi `BA-06` v4.10)* `409` của `unmatch` mang mã `FLS-CONFLICT-SOURCE` ⇒ câu *"Giá trị bạn gõ khác với giá trị nguồn đang có."* sai nghĩa cho bỏ gán. Sau vòng 2 lượt bấm thứ hai trên **cùng** màn ⛔ còn xảy ra *(`AC-9` + `AC-10`)*; còn ca **hai người** bỏ gán cùng lúc. Đổi mã = đổi hợp đồng cửa `BA-07` ⇒ phiếu khác khi `fls-ba` xếp.

### Rủi ro vòng 2
1. **Hai bản bộ ba trạng thái** *(`khuon_the_lenh` Python ↔ cập nhật tại chỗ JS)*: đổi nhãn một bên là lệch im lặng ⇒ `AC-9 ⓑ` đo **quan hệ** bằng **hàm thật**, ⛔ chép hằng.
2. **`pytest` đỏ 5 bài `XPASS(strict)`** ngay khi vòng 2 đúng — **đúng mong** *(`AC-13`)*; `BG` phải liệt kê đủ 5 tên để `fls-test` phân biệt với đỏ thật.
3. **Bẫy `HT` trong bài Dev**: bài vòng 1 tự định nghĩa `HT.hoi` nên che `F-1` ⇒ mọi bài nhánh hộp của vòng 2 nạp `hop_thoai.js` thật *(Phạm vi dòng *Bài thử*, `AC-8 ⓒ`)*.

### Đính chính `KQ-019 F-5` *(bảng tách `kiem_so_song` của `BG-017`)*
`BG-017` mục **Cổng** tách **20** lệch loại (c) thành `2084→2095 ×5` · `25.133→25.213 ×4` · … ⇒ cộng ra **18**; máy đo *(`KQ-019`, Test chạy lại)*: `2084→2095` **×6** · `25.133→25.213` **×5** ⇒ cộng **20**. **Tổng 20 đúng, bảng tách sai 2 dòng.** Phiếu `BG` thuộc `fls-dev` và chỉ-thêm *(`10` §4.3)* ⇒ `fls-ba` ghi đính chính **ở đây**, ⛔ sửa `BG-017`; `AC-14` vòng 2 đòi bảng tách **cộng ra đúng tổng**. ⛔ Ảnh hưởng phán quyết `AC-6` *(`KQ-019`: ĐẠT)*.

## Nghiệm thu PO *(`fls-ba` · 2026-10-02 khuya — đọc [`KQ-021`](KQ-021-kiem-bg-020.md) ĐẠT 8/8 + [`KQ-019`](KQ-019-kiem-bg-017.md) 6/6)*

> **Kết luận: ✅ `DONG`.** Ba chỗ chữ của vòng 1 *(nhật ký nói *"gợi ý"* / *"rút gợi ý"*, hộp *"Đã bỏ ghép"* nói theo **ô**, màn ghép báo khi người đã gõ tay)* giữ nguyên; vòng 2 làm nút `Bỏ gán` trên màn ghép **đi được ở cả năm ca** — đo trên **sổ thật chỉ đọc**: **88 / 88** lệnh thuộc hai ca khó mở **đúng** hộp, **0** lượt ghi. Bốn phát hiện mới đều `NHE`, ⛔ cái nào ghi sai sổ ⇒ ⛔ chặn đóng; đã xếp phiếu *(bảng cuối mục)*.

| Ý owner / spec *(nguyên văn · ngày)* | Phiếu làm gì | Đo được *(`KQ-019` · `KQ-021` · sổ thật chỉ `SELECT`)* | Khớp |
|---|---|---|:-:|
| `QĐ-ITL-149` *(01/10)*: hai ô `hd`/`cdt1` khi ghép là **"Máy gợi ý"** — ⛔ Final | `(a)` nhật ký `F02` in *"gợi ý: X"* / *"rút gợi ý"*, nhãn *"máy gợi ý · không đổi Final"* · `(b)` hộp nói *"Đã rút gợi ý máy trên N ô"* | `KQ-019` `AC-1`…`AC-3` ĐẠT *(8088 nhật ký thật mẫu số **4.424**)*; `KQ-021`: ⛔ hồi quy | ✅ |
| `QĐ-ITL-149` *(01/10)*: *"bỏ yêu cầu lý do cho cú Ghép"* — Ghép / Bỏ ghép ⛔ bắt buộc lý do | hộp ② chỉ `Thôi` · `Gỡ cả N`, ⛔ ô lý do; ca ①/③ ⛔ hộp hỏi | `KQ-021` `AC-7`: nút đúng `["Thôi","Gỡ cả 2"]`; ⛔ ô nhập trong hộp | ✅ |
| `QĐ-ITL-148` *(21/09 — `BA-07 §4h ⓻`)*: *"cửa ĐỨNG NGUYÊN, MÀN nói ra thiệt hại"* | ca ② liệt kê **từng** lệnh + số tiền trước khi gỡ cả chùm | 8088 sổ thật: ca ② **65 / 65** hộp *"Bỏ gán sẽ gỡ CẢ N lệnh chi"*; chùm 10 lệnh vừa màn *(520×436)* | ✅ |
| `INV-I16` + `BA-06` v4.10 ① — máy ⛔ chọn hộ | ca ① *(lệnh gắn ≥ 2 giao dịch)* chỉ **báo**, **0** lượt ghi | 8088: ca ① **23 / 23**, `/chum` 0, `POST` 0 | ✅ |
| `QĐ-ITL-27` *(22/08)*: 2–3 kế toán, việc phải **sống sót** khi người rời đi — người bấm phải **thấy** việc đã xảy ra | ca ③ thẻ đổi tại chỗ + *"↩ Đã bỏ gán… Sổ giữ lịch sử."*; ca ⑤ lỗi thành chữ | `KQ-021` `AC-9` · `AC-11`: thẻ `Chưa gán`, dòng tín hiệu; mất mạng ⇒ *"Bỏ gán chưa xảy ra — …"*, **0** `Uncaught` | ✅ |
| `QĐ-ITL-150 ⓐ` *(01/10)*: UAT ⛔ tính người thật | phiếu ⛔ chạm bộ đếm; ⛔ ghi kho thật | sổ thật trước = sau **11 / 11** bảng; actor `fls-test%` **0** | ✅ |
| `QĐ-ITL-150 ⓑⓒ` *(01/10)*: `dong_bo --ghi` chỉ Dev, ⛔ để dọn đỏ của chính `BG` | `T0` đầu vòng 1; ⛔ `--ghi` cuối vòng | `AC-14`: `git log 124a067..929fbd2` ⛔ commit `dong_bo`; bảng tách **34 = 13 + 20 + 1** khớp từng cặp | ✅ |

**Bốn phát hiện `NHE` của `KQ-021` + nợ cũ — `fls-ba` xếp 02/10 khuya:**

| F | Quyết | Ở đâu |
|---|---|---|
| `F-1` phím màn ghép ⛔ nhường hộp | Luật mới `ⓕ1` *(hộp là modal với bàn phím, ⛔ phụ thuộc thứ tự trình nghe; áp cả `F02`)* | `BA-06` **v4.11** ⓔ · [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) `(a)` — **THẤP** |
| `F-2` lỗi vào hộp đã đóng | Hướng spec: hộp có nút **đang chờ cửa** ⛔ đóng bằng `Esc`/bấm ngoài `ⓕ2` + cửa ghi hạn chờ **30 s**, mã màn `FLS-HET-GIO` *(⛔ nói "chưa xảy ra")* `ⓕ3` | `BA-06` **v4.11** · `WO-023` `(b)(c)` — **THẤP** |
| `F-3` `TP.tien` cắt phần lẻ ngoại tệ | ⭐ Nâng ưu tiên **CAO** *(đọc sai tiền ngoại tệ trái `QĐ-ITL-62`)*: luật `UI-F10` + §5b — ISO 4217, ⛔ làm tròn giá trị sổ, tổng/lệch trên số nguyên xu; một câu owner `Q-TIEN-1` *(⛔ chặn)* | `BA-06` **v4.11** §5b · [`WO-022`](WO-022-in-tien-theo-tien-te.md) |
| `F-4` khối `SINH-KHOP` lệch nền `B5` | ✅ sinh lại khối 02/10 khuya *(`khop_owner.py`, ⛔ `--kiem`; rồi `--kiem` **ĐẠT** 17/20 đúng mong)*; gốc *(ô `B5` mang số đếm chữ ⇒ đỏ mỗi lần sửa `BA-06`)* ⇒ khối chỉ mang quan hệ | `WO-023` `(e)` |
| Nợ `409` `FLS-CONFLICT-SOURCE` | Ba mã `409` mới `FLS-DA-GHEP` · `FLS-KHONG-CON-MOI-NOI` · `FLS-CHUA-XONG` *(đo: mã cũ bị **4** lớp lỗi dùng chung ⇒ sai nghĩa ở **3** cửa `match`/`unmatch`/`reopen`, ⛔ chỉ `unmatch`)* | `BA-07` **v3.5** §5 · `BA-06` `ⓕ4` · `WO-023` `(d)` |
| *(yếu #4 Dev)* tín hiệu mất khi rời rồi mở lại cùng lệnh | Chấp nhận — đính chính câu ③ⓑ `ⓕ5` *(bằng chứng bền là thẻ + nhật ký)* | `BA-06` **v4.11** |
| *(ghi nhận, ⛔ `F`)* danh sách *"Chưa gán"* tải **8,6 s** trên sổ thật | ⛔ do `WO-008`; ghi vào dashboard §6 làm việc đo `NFR` khi xếp | dashboard `6.-10` |

## Changelog
- 2026-10-02 khuya · `fls-ba` · nghiệm thu PO ⇒ ✅ **`DONG`** *(7 ý owner / spec khớp — bảng **Nghiệm thu PO**; [`KQ-021`](KQ-021-kiem-bg-020.md) ĐẠT 8/8)*. `KQ-021` `F-1`…`F-4` + nợ `409` xếp: `F-3` ⇒ [`WO-022`](WO-022-in-tien-theo-tien-te.md) *(CAO)*; `F-1`/`F-2`/`F-4` gốc/`409` ⇒ [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(THẤP)*; `F-4` khối sinh lại ngay. Spec `BA-06` **v4.11** · `BA-07` **v3.5**.
- 2026-10-02 tối · `fls-dev` · **vòng 2** → **`CHO_TEST`**: mã `9dae3ac` *(`man_f01_ghep.js::bo_gan` năm ca — ① hộp báo · ② hộp hỏi bằng `HT.mo` · ③ thẻ đổi tại chỗ + dòng tín hiệu · ④ đọc lại lỗi ⛔ nuốt ③ · ⑤ dòng lỗi, 0 `Uncaught`; nút khoá khi chờ)* + `dd7c5bb` *(+1 bài)*; bẫy hàm hỏi trên `HT` gỡ khỏi bài vòng 1 *(đếm xuyên `HT.mo` thật)*; **18** bài mới đỏ **18/18** trên `124a067`, **17/17** đột biến bị bắt; bấm thật Chrome `8099` *(kho TEST)* 6 ca. Phát [`BG-020`](BG-020-ban-giao-wo-008-vong-2.md) — liệt kê **5** bài `XPASS(strict)` cho `fls-test` gỡ dấu. ⛔ `HOI`.
- 2026-10-02 tối · `fls-dev` · nhận **vòng 2** → `DANG_LAM`: cổng vào `HEAD` = `origin` `124a067` · `BA-06` v4.10 · ⛔ `HOI` *(mục **Vòng 2** đủ trường; ⛔ câu chặn)*. Nền `kiem_so_song` đầu vòng 2 *(trên `124a067`, trước commit mã đầu tiên)*: **34** lệch = **13** loại (b) nhịp chụp + **21** loại (c) *(20 của vòng 1 `BG-017` đã trôi thêm theo bài `kq019` + **1** mới `302→310` = bài nghiệm thu `KQ-019`)*.
- 2026-10-02 chiều · `fls-ba` · ⭐ **mở lại — VÒNG 2** theo [`KQ-019`](KQ-019-kiem-bg-017.md) *(TRƯỢT: 6/6 AC ĐẠT, `F-1`/`F-2` `NANG` + `F-3`/`F-4` `NHE` trên `bo_gan`)*: thêm mục **Vòng 2** *(`AC-7`…`AC-14` cho `F-1`…`F-4`; cách đo gồm `pytest --runxfail` 5 bài `kq019`)*; spec `BA-06` **v4.10** *(mục ⓔ — năm ca nút `Bỏ gán`, bảng 5 trạng thái)*; đính chính dòng *lỗi*/*mất kết nối* mục **Màn hình** vòng 1 *(`F-3`)* + bảng tách `BG-017` *(`F-5`)*. Trạng thái `CHO_TEST` → **`MO` vòng 2**. Thứ tự: **trước** `WO-018` → `WO-015`.
- 2026-10-02 · `fls-ba` · trả `HOI-016` *(`TL-016`)*: ⛔ mở lại, vẫn `CHO_TEST` vòng `1`. Đính chính *(⛔ xoá câu cũ)*: Phạm vi (a) + `AC-1` nhãn chữ trơn *"máy gợi ý · không đổi Final"*; Phạm vi (b) khối `bo_qua` in giá trị người. `value_source` của cú `/adjust` = nguồn trước khi gõ ⇒ **lỗi cửa ghi**, ⛔ lỗi màn ⇒ [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md) *(sau phiếu này ĐẠT)*. `fls-test`: hàng người gõ in `UNMAPPED` trên kho TEST là đã biết, ⛔ nâng `F`.
- 2026-10-02 · `fls-dev` · nhận → `DANG_LAM` → **`CHO_TEST`**: `T0` `948ffb6` *(8 lệch ⇒ 0)*; mã + 11 bài `69f03f6`; phát `BG-017` + `HOI-016` *(`KHONG_CHAN`: ⓑ `value_source` cú `/adjust` = nguồn trước khi gõ · ⓐ khối `bo_qua` in giá trị)*.
- 2026-10-02 chiều · `fls-ba` · rà sau `WO-011` `DONG` ⇒ **⛔ đổi** phạm vi / AC `1`…`5` / spec; ⭐ **SẴN SÀNG làm ngay**; thêm `T0` *(`--ghi` dọn nền trước khi code)*; `AC-6` đổi nền `WO-001 T5` ⇒ `T0`; thứ tự: **trước** `WO-015`. Vẫn vòng `1` *(Dev chưa nhận)*.
- 2026-10-01 tối · `fls-ba` · phát `WO-008` *(từ `KQ-007` `F-1`/`F-2`/`F-3`; spec `BA-06` v4.8 · `BA-10` v0.8)* — ưu tiên **thấp**, sau `WO-001`.
