# WO-037 — Đề xuất của máy ⛔ còn là cặp cửa ghi từ chối · rổ `may` đo theo cửa ghi · ba ca biên của bậc · chữ chú giải đọc được

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(05/10 — `fls-ba` nghiệm thu PO: [`KQ-041`](KQ-041-kiem-bg-039-bg-040.md) ✅ ĐẠT **17/17** `AC-1`…`AC-17`, oracle độc lập sổ thật lệch **0 / 1.601**; bảng đối chiếu ý owner ở mục **Nghiệm thu PO** cuối phiếu; `F-1`/`F-2`/`F-3` ⇒ [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md); điều phối quyết `F-3` ngoài phạm vi)* · ~~`CHO_TEST` — vòng 2~~ *(`fls-dev` 05/10 — [`BG-040`](BG-040-ban-giao-wo-037-vong-2.md) @ `3c13ce3`; `fls-test` kiểm **gộp** `BG-039` ＋ `BG-040`)* · ~~`DANG_LAM` — vòng 2~~ *(`fls-dev` nhận 02/10 — cổng vào git `892a315` = `origin`; mã `fls/**` cuối = `4c3b2ae` ✔ · `BA-07` **v3.10** · `BA-06` **v4.17** · `BA-13` **v1.8** · `BA-08` **v1.3** ✔ · `WO` vòng 2 đủ trường)* · ~~`MO` — vòng 2~~ *(`fls-ba` 02/10, [`TL-038`](HOI-038-o-giao-dich-doc-vi-sao-tu-dau-va-cau-nao.md): `(i)` `(j)` `(k)` `(l)` · `AC-11`…`AC-17`; `fls-test` ⛔ kiểm `BG-039` riêng — kiểm **gộp** `BG-039` ＋ `BG` vòng 2)* · ~~`CHO_TEST`~~ *(`fls-dev` 02/10 — [`BG-039`](BG-039-ban-giao-wo-037.md) @ `4c3b2ae`; [`HOI-038`](HOI-038-o-giao-dich-doc-vi-sao-tu-dau-va-cau-nao.md) `KHONG_CHAN` chờ `TL`)* · ~~`DANG_LAM`~~ *(`fls-dev` nhận 02/10 — cổng vào git `8d7bea2` = `origin` · `BA-07` **v3.9** · `BA-06` **v4.16** · `BA-08` **v1.3** ✔ · `WO` đủ trường)* · ~~`MO`~~ · ⭐ **SẴN SÀNG** · ưu tiên **CAO** — làm **TRƯỚC** [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) và [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-02 |
| **Nhận** | `fls-dev` |
| **Vòng** | ⭐ `2` *(`TL-038`)* · ~~`1`~~ |
| **Thứ tự với phiếu khác** | **Sau** [`WO-032`](WO-032-so-tien-khac-tien-te-va-khuon-cua-du-truong.md) *(✅ `DONG` 02/10 — phiếu này đứng trên `lech_ung_vien`, `ma_tien_te`, `gan_ma_canon`, `BAC` + chú giải của nó)*. ⭐ **TRƯỚC `WO-015` + `WO-023`** — lý do ở mục **Vì sao ưu tiên CAO** dưới |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết **một vòng ghép thật** — hôm nay đo được **0**)*. Vòng ghép thật đầu tiên sẽ bắt đầu ở rổ máy nói *"máy trả lời được — người chỉ DUYỆT"* *(`BA-12 §2`; nút hàng `Duyệt`)*. Đo 02/10: **84 / 268** lệnh trong rổ ấy *(**31,3 %**)* có câu trả lời duy nhất của máy là một dòng tiền **khác tiền tệ** — cặp cửa ghi **từ chối**. Người đầu tiên bấm theo máy sẽ gặp ngõ cụt ở gần **một phần ba** rổ dễ nhất, và học rằng *"máy đề xuất"* ⛔ đáng tin — đúng điều `QĐ-ITL-27` cấm *(kiểm soát nằm trong máy; một câu máy nói ngược cửa ghi là dạy người bỏ qua câu máy nói)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; phiếu này giữ cho mắt xích **"ghép PM ↔ tiền"** đã chuyển lên FLS **⛔ thua Sheets**: trên Sheets người nhìn cột tiền tệ cạnh số; ở FLS máy **xếp** và **đề xuất** thay người, nên đề xuất ấy phải là thứ **ghi được**.

### Vì sao ưu tiên CAO *(PO — trên `WO-015` và `WO-023`)*
| Phiếu | Hại hôm nay nếu ⛔ làm | Chạm vòng ghép thật đầu tiên? |
|---|---|:-:|
| ⭐ **`WO-037`** | **84** lệnh *(31,3 % rổ `may`)* đề xuất một cặp bị từ chối; rổ `may` hứa nhiều hơn cái bấm được | ✅ **trực tiếp** — rổ người ta mở **trước tiên** |
| `WO-015` | thước *"người thật"* có bốn lỗ; sổ thật hôm nay **⛔ con số nào đổi** | ⛔ |
| `WO-023` | hộp modal / phím / mã `409`; hôm nay **0** ghi sai *(cửa ghi chặn)* | gián tiếp *(cách hộp đóng mở)* |

⛔ **Không** xếp trên mức **CAO**: cửa ghi đã chặn mọi cặp khác tiền tệ ⇒ **0** ghi sai; hại là **phí cú bấm + mất lòng tin**, ⛔ sai sổ. ⚠ Và ⛔ chọn cách vá *"đưa ứng viên cùng tiền tệ lên đầu"* — cách ấy **biến cú bấm bị từ chối thành cú ghép sai được nhận** *(xem `Căn cứ` ⓑ)*.

## Căn cứ
- [`KQ-036`](KQ-036-kiem-bg-034-bg-035.md) *(`fls-test` 02/10, ✅ ĐẠT `WO-032`, 6 `F` `NHE`)*: `F-1` `xu_ly._bac:764` so tiền tệ ⛔ `trim` — luật thứ hai cạnh `mg.ma_tien_te` *(sổ thật **0** ca)* · `F-2` `_bac` dán `cung_tien_te` lên `gd`/`gd_ds` khác tiền tệ ⛔ khớp mã *(sổ thật **0 / 2.262**)* · `F-3` `ve_dang_gan` *(`man_f01_ghep.js:366`)* bỏ chip bậc lạ im lặng · `F-4` chữ chú giải `--faint` **2,17 : 1** · `F-6` **84 / 268** đề xuất đầu khác tiền tệ. Ba bài `xfail(strict)` `tests/nghiem_thu/test_kq036_bac_gd_khac_tien_te_va_bac_la.py` *(`F-1`/`F-2`/`F-3`)*.
- ⭐ **`fls-ba` đo lại `F-6` 02/10** *(sổ thật **chỉ đọc** — `noi_chi_doc(dsn_that())`, `default_transaction_read_only = on`; gọi **hàm thật** `lc.doc_lenh_cho_theo_ro` + `xu_ly._gan_gd` + `lc.ung_vien_itl`; ảnh PM `NAP-2026-10-02-PMA07ED283`; 83 s)*:
  - ⓐ **84 / 268** lệnh rổ `may` có `the.gd` khác tiền tệ *(lệnh USD 63 · VND 15 · SGD 5 · HKD 1)*; `gd` trùng ứng viên đầu `itl-candidates` **268 / 268** ⇒ cùng một sự thật trên hai cửa. ⭐ Cả **84 / 84** có **mọi** dòng khớp mã **khác tiền tệ** *(0 lệnh có dòng khớp mã cùng tiền tệ)* ⇒ lệnh **chỉ** vào rổ `may` nhờ một cặp cửa ghi từ chối. `tu_chung` trong nhóm **0 / 84**.
  - ⓑ Ứng viên cùng tiền tệ đầu tiên của 84 lệnh: bậc `tien` **45** · `cung_tien_te` **36** · `gan_tien` **3** — khớp mã **0**. **45** lệnh có ứng viên cùng tiền tệ **lệch 0**, nhưng: trung vị **16** dòng cùng đúng số tiền mỗi lệnh *(1 → 19)* · cách dòng khớp mã trung vị **294 ngày** *(≤ 7 ngày **2 / 45**)* · mang mã của một dòng lệnh khác **0 / 45** ⇒ **trùng tiền tình cờ**. Đưa chúng lên đầu = mời một cú ghép **sai mà cửa ghi NHẬN**.
  - ⓒ Tỷ số tiền bank ÷ tiền lệnh của cặp khớp mã: HKD→USD **0,129** · SGD→USD trung vị **0,81** · VND→USD trung vị **1 / 25.400** *(trông như quy đổi ngoại tệ)*; USD→VND trung vị **37.950**, tản **12 → 9,2 triệu** *(lẫn trùng mã)* ⇒ câu owner `Q-FX-1`.
  - ⓓ `dem_theo_ro` hôm nay: `may` **268** · `nguoi` **532** · `khong` **801** · `tu_chung` **64** · `tong` **1.601**.
- ⭐ **`fls-ba` đo `F-4` 02/10** *(công thức WCAG trên `fls/web/tep/tokens.css`)*: `--faint` **2,17** trên `--page` · **2,47** trên `--surface`; `--muted` **4,92** · **5,59**. `.cand .tg` nền `--surface`, màu gốc `--faint` — ô ④ / `≠` *(bậc ⛔ tông, `m: ''`)* rơi về đó.
- **`QĐ-ITL-62`** *(28/08 — ngoại tệ ⛔ dung sai; ⛔ so / ghép khác tiền tệ)* · **`QĐ-ITL-27`** *(2–3 kế toán, kiểm soát trong máy)* · luật đo *"đo theo cửa GHI, ⛔ cửa ĐỌC"* *(`11_BOI_CANH` §6 — `584` → `68`)*.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(nghĩa + thứ tự trường cửa đọc đã trả; rổ theo luật cửa ghi **đã có**; màu từ token có sẵn; ⛔ đổi sổ, ⛔ đổi Final, ⛔ đổi cửa ghi, ⛔ tuyến mới, ⛔ HTTP mới)*.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/07_API_CONTRACT.md` | **§4g ⓹** đoạn v3.9 *(rổ `may` theo cửa ghi — bảng ⓐ…ⓓ + đoạn *"Vì sao ⛔ chọn…"*)* · đoạn v3.9 sau *"Bốn bậc soi gương"* *(thứ tự trong bậc `ma`)* · dòng **`lenh-cho` trả mỗi dòng** + đoạn v3.9 *(`ma_canon`)* · **§4h ⓵** dòng `bac` *(phần v3.9: `F-1` · `F-2` · `F-3`)* · **§4h ⓵'** đoạn v3.9 *(`gd` chưa gán ⛔ khác tiền tệ)* | ⭐ **v3.9** |
| `02_BA/06_SCREEN_SPEC.md` | **§4.5 ⓒ ①** đoạn v4.16 *(màu chú giải + `.tg`)* · **§4.5** đoạn *"Ô `Giao dịch đã gán`"* + câu thứ sáu v4.16 · **§5b ⓘ** *(câu `.cand .amt .lech` đã gạch — ⛔ việc)* | ⭐ **v4.16** |
| `02_BA/08_NFR.md` | **§4b `NFR-I29`** *(ngưỡng tương phản + bảng đo)* | ⭐ **v1.3** |
| `01_Orchestrator/handoff/KQ-036-kiem-bg-034-bg-035.md` | *Phát hiện* `F-1`…`F-4`, `F-6` + lăng kính **Dữ liệu** + 3 bài `xfail(strict)` `test_kq036_*` | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a) Rổ `may` theo cửa ghi** *(`§4g ⓹` ⓐ ⓑ v3.9)*: `lenh_cho.xep_ro` — lệnh vào `may` ⇔ có dòng khớp mã **và** `ma_tien_te(curr) == ma_tien_te(curr lệnh)` *(`chi_muc_ma` đã mang `curr` trong tuple — ⛔ câu SQL mới)*; `ung_vien_itl` chỉ mang dòng khớp mã **cùng** tiền tệ; khớp mã **chỉ** khác tiền tệ ⇒ `ro = 'nguoi'`, `vi_sao` khoá mới `ma_khop_khac_tien_te` *(câu nói **mã tiền tệ thật** của dòng khớp — đặt ở `VI_SAO`, ⛔ gõ ở JS)*. Gọi **cùng** hàm `man_ghep.ma_tien_te` *(⛔ bản so thứ ba)* | ⛔ đổi `tap_tu_chung` / `ds_tu_chung` *(đã đúng — hỏi cửa ghi)* · ⛔ đổi rổ `khong` · ⛔ chip mới · ⛔ đổi `Chưa gán` *(cộng `nguoi` ＋ `may` ⛔ tự chứng — tự bất biến)* |
| **(b) Thứ tự trong bậc `ma`** *(`itl-candidates`, đoạn v3.9)*: `lenh_cho.ung_vien_itl` — khoá xếp `(bậc, khác tiền tệ?, lech, itl_id)` cho bậc `ma`: cùng tiền tệ trước | ⛔ hạ dòng khớp mã khác tiền tệ xuống dưới bậc tiền *(lý do: `Căn cứ` ⓑ)* · ⛔ lọc bỏ nó khỏi danh sách · ⛔ đổi ba bậc tiền |
| **(c) `F-2` bậc `gd`/`gd_ds` khác tiền tệ** *(`§4h ⓵` dòng `bac` v3.9)*: `xu_ly._bac` — `ma` › **khác tiền tệ ⇒ `khac_tien_te`** › `tien` › `cung_tien_te` *(giống `/so`)* | ⛔ đổi `/so` · ⛔ đổi `itl-candidates` *(⛔ sinh `khac_tien_te`)* |
| **(d) `F-1` một phép so tiền tệ**: `_bac` gọi `mg.ma_tien_te` cho cả hai vế | ⛔ đổi SQL `upper(i.curr)` ở `lenh_cho.py:208`/`:215` *(xem `Rủi ro` 2)* |
| **(e) `F-3` bậc lạ ở khối "Đang gán"**: `man_f01_ghep.js::ve_dang_gan` — `BAC[g.bac]` vắng ⇒ chip in **nguyên tên** bậc *(cùng luật `ve_ung_vien` sau `WO-032 (d)`)* | ⛔ đổi `BAC` |
| **(f) `F-4` màu** *(`BA-06 §4.5 ⓒ ①` v4.16 · `NFR-I29`)*: `hinh.css` `.tlegend` chữ nghĩa ⇒ `--muted`; `.cand .tg` màu gốc ⇒ `--muted` *(tông `good`/`info`/`warn` của ①②③ ⛔ đổi)* | ⛔ token mới · ⛔ đổi 20 chỗ `--faint` còn lại *(chưa phân loại — `GAP-NFR-01`)* · ⛔ đổi `--warn` |
| **(g) Ô `Giao dịch đã gán` câu thứ sáu** *(`BA-06 §4.5` v4.16)*: `man_f01_ghep.js::ve_o_gd` — `gd = null` ∧ `vi_sao` có ⇒ in **câu `vi_sao` của cửa**, ⛔ *"— chưa chọn"*; chữ ⛔ `--faint` | ⛔ câu màn tự ghép · ⛔ đổi năm câu kia · ⛔ đổi `F01L` *(đã in `vi_sao` ở `hint`)* |
| **(h) Bài thử** `tests/api/**` + `tests/web/**` — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; ⭐ **thân vẽ màn lấy từ CỬA THẬT trên kho TEST** *(HTTP, `assert current_database() = 'fls_test'`)* — ⛔ một khoá do bài đặt *(luật `BA-07 §4h ⓵`, lớp *"khuôn thử tự nhét"* đã sống sót **ba** lần)*; cổng quét khoá `test_wo032_quet_khoa_cua_that.py` mở rộng sang `ve_o_gd` đọc `vi_sao` | ⛔ sửa / gỡ dấu `tests/nghiem_thu/**` *(`fls-test` gỡ ở `KQ` — 3 bài `kq036` sẽ `XPASS(strict)` đúng ý)* |

⭐ **Đính chính `(g)`** *(`fls-ba` 02/10, [`TL-038`](HOI-038-o-giao-dich-doc-vi-sao-tu-dau-va-cau-nao.md) — `HOI-038` phương án **B**)*: chữ *"`gd = null` ∧ `vi_sao` **có**"* đọc là ***`gd = null` ∧ `the.vi_sao` có***; `the.vi_sao` **chỉ có mặt** ở nhánh khớp mã chỉ khác tiền tệ *(`BA-07` **v3.10** `§4h ⓵'`)* ⇒ **84** ô, ⛔ 616 — đúng `BA-06` v4.16 + mục `Dữ liệu`. Chữ cũ của `(g)` rộng hơn spec: lỗi **phiếu**, ⛔ lỗi Dev.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a · kho TEST)* | Kho TEST qua **HTTP**: lệnh VND mã `<X>` + một dòng tiền **USD** mã `<X>` chưa nối *(⛔ dòng VND mã ấy)* ⇒ `GET lenh-cho/ro?ro=nguoi` **chứa** lệnh, `vi_sao` chứa `USD` + `tiền tệ`; `?ro=may` **⛔ chứa**; `the.gd is None`. Thêm một dòng **VND** mã `<X>` ⇒ lệnh về `ro=may`, `the.gd.curr == 'VND'`. Tiền tệ `' vnd '` *(khoảng trắng)* ⇒ tính là **cùng** VND | bài cửa `tests/api/` *(khuôn `test_cua_lenh_cho_pg.py`)* | `xep_ro` ⛔ so tiền tệ *(mã hôm nay)* ⇒ **ĐỎ**; so ⛔ `trim` ⇒ ca `' vnd '` **ĐỎ**; câu `vi_sao` gõ ở JS ⇒ cổng quét **ĐỎ** |
| AC-2 *(a · sổ thật)* | **Sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, gọi hàm thật như `fls-ba` 02/10 — dán lệnh + kết quả vào `BG`)*: ⓘ lệnh rổ `may` có `the.gd` khác tiền tệ: nền cổng vào *(mong ≈ **84 / 268**)* ⇒ **0**; ⓘⓘ tập lệnh rời `may` **trùng đúng** tập đo ở cổng vào *(so `pm_line_id`, ⛔ chỉ so số đếm)* và **cả tập** vào `nguoi` với `vi_sao = ma_khop_khac_tien_te`; ⓘⓘⓘ `nguoi` ＋ `may` ⛔ tự chứng **bằng nhau trước / sau** *(chip `Chưa gán` ⛔ đổi)*; `khong`, `tu_chung`, `tong` ⛔ đổi. Mẫu số in ra > 0 *(`Đ3`)*. ⚠ Ảnh PM trôi theo nhịp ⇒ đo nền **và** sau trên **cùng** ảnh *(in `run_id`)* | phép đo chỉ đọc *(kịch bản trong `BG`)* | tập rời ≠ tập đo ⇒ **ĐỎ**; `Chưa gán` đổi ⇒ **ĐỎ**; mẫu số 0 ⇒ **ĐỎ** |
| AC-3 *(b)* | Kho TEST: lệnh VND mã `<Y>` + hai dòng chưa nối mã `<Y>`: **USD** `itl_id` nhỏ hơn, **VND** `itl_id` lớn hơn ⇒ `itl-candidates` `ung_vien[0].curr == 'VND'`, `[1].curr == 'USD'`, cả hai `bac = 'ma'`; dòng USD đứng **trước** mọi ứng viên bậc `tien`/`gan_tien`/`cung_tien_te` *(dựng thêm một dòng VND cùng số tiền ⛔ mã)*. Sổ thật chỉ đọc: **0** lệnh rổ `may` có ứng viên mã khác tiền tệ đứng trước ứng viên mã cùng tiền tệ *(mẫu số hôm nay **0** lệnh có cả hai ⇒ in ra và ghi `⛔ tập rỗng — đo ở kho TEST`)* | bài cửa `tests/api/` | xếp theo `itl_id` *(mã hôm nay)* ⇒ **ĐỎ**; hạ dòng mã khác tiền tệ xuống dưới bậc tiền ⇒ **ĐỎ** |
| AC-4 *(c · `F-2`)* | Kho TEST qua HTTP `lenh-da-gan`: mối nối lệnh VND ↔ dòng **USD** mã **khác** *(chèn như `KQ-036 F-2`)* ⇒ `gd_ds[i].bac == 'khac_tien_te'`, `lech is None`; khối *"Đang gán"* chip `≠` + `title` *"khác tiền tệ"*. `pytest --runxfail tests/nghiem_thu/test_kq036_*::test_F2_*` ⇒ passed | bài cửa + bài DOM `man_f01_ghep.js` thật | nhánh cuối `return "cung_tien_te"` cho dòng khác tiền tệ ⇒ **ĐỎ** |
| AC-5 *(d · `F-1`)* | `_bac` với `curr` `' vnd '` ↔ `'VND'` ⇒ cùng tiền tệ *(như `lech_ung_vien`)*. Bài quét: trong `fls/api/xu_ly.py` **0** phép so tiền tệ viết riêng *(mẫu `.upper() ==` trên `curr`)*; mọi chỗ so đi qua `ma_tien_te`. `pytest --runxfail …::test_F1_*` ⇒ passed | bài đơn vị + bài quét mã | thêm lại `str(...).upper() ==` ⇒ **ĐỎ** |
| AC-6 *(e · `F-3`)* | Thân `lenh-da-gan` **cửa thật** kho TEST, đổi **giá trị** `bac` của một `gd` thành `'xyz'` ⇒ khối *"Đang gán"* có chip chữ `xyz`, ⛔ `null`. `pytest --runxfail …::test_F3_*` ⇒ passed | bài DOM `man_f01_ghep.js` thật | `if (b) {…}` bỏ chip ⇒ **ĐỎ** |
| AC-7 *(f · `F-4`)* | Bài đọc nguồn: màu khai cho `.tlegend` *(chữ)* và `.cand .tg` *(gốc)* trong `hinh.css` → tra `tokens.css` → tỷ số WCAG trên nền khai của nó *(`--page` · `--surface`)* ≥ **4,5** và ≥ **3** — mong **4,92** · **5,59**. Chrome `getComputedStyle` 8099 *(1440×900)*: chữ nghĩa chú giải ≥ 4,5 *(5 / 5 mục)*; ô `.tg` của một dòng `≠` ≥ 3. `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh | bài đọc nguồn + Chrome | trả `.tlegend{color:var(--faint)}` ⇒ **ĐỎ** *(2,17)*; `.cand .tg` `--faint` ⇒ **ĐỎ** *(2,47)* |
| AC-8 *(g)* | Thân `lenh-cho` **cửa thật** kho TEST *(ca `AC-1`)*: ô `Giao dịch đã gán` của lệnh ấy chứa đúng câu `vi_sao` của cửa *(so chuỗi)*, ⛔ chứa `đề xuất:`, ⛔ `— chưa chọn`; tương phản chữ ≥ 4,5 | bài DOM `man_f01_ghep.js` thật | in `— chưa chọn` *(mã hôm nay)* ⇒ **ĐỎ**; câu gõ ở JS ⇒ **ĐỎ** |
| AC-9 ⭐ *(Chrome chuột thật 8099)* | Chrome **1440×900**, máy **8099** `--cho-ghi` trỏ **kho TEST**, **chuột thật** *(`Input.dispatchMouseEvent`)*: ① `② Hàng chờ` → chip `Chưa gán` → lệnh ca `AC-1`: nút hàng theo rổ `nguoi` *(⛔ `Duyệt`)*, ô *Giao dịch* in câu `vi_sao` · ② mở lệnh ca `AC-3` ⇒ dòng VND mã khớp trên dòng USD mã khớp, dòng USD trên dòng bậc tiền · ③ chọn dòng USD ⇒ câu *"khác tiền tệ ⇒ cửa ghi sẽ TỪ CHỐI"* *(⛔ hồi quy `WO-032`)*, **0** `POST` · ④ chú giải + ô `≠` đo màu ≥ ngưỡng `AC-7`. Console **0** lỗi. ⭐ Kèm **8088 sổ thật CHỈ ĐỌC**: `PM00329-1` *(VND, mã khớp USD `32700`)* và `PM01089-1` *(HKD → USD)* ⇒ **⛔** ở rổ `may`, ô *Giao dịch* in câu `vi_sao` có `USD`, ⛔ `đề xuất:` | Chrome CDP; `BG` dán số đo từng ca *(ảnh ⛔ lên git)* | JS + Python trên `HEAD` khi nhận, cùng máy ⇒ ①②④ sai **3 / 3**; 8088 hai lệnh vẫn `đề xuất:` USD ⇒ **ĐỎ** |
| AC-10 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai + đúng **3 `XPASS(strict)`** `kq036` *(`F-1`/`F-2`/`F-3` — đúng ý; `fls-test` gỡ dấu)* · `lint-imports` 9/0 · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.16** §4.5 ⓒ ① + ô `Giao dịch đã gán`; `02_BA/08_NFR.md` **v1.3** `NFR-I29`. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(chỉ đổi **màu** từ token có sẵn + **chữ** trong ô đã có; ⛔ token, ⛔ lớp CSS mới)*.

| Trạng thái | Hiện gì *(danh sách lệnh `F01G` · vùng ứng viên · chú giải)* |
|---|---|
| tải | ⛔ đổi *(khung chờ; chú giải ⛔ hiện — `WO-032` `AC-13`)* |
| rỗng | ⛔ đổi *(⛔ chú giải; câu rỗng của danh sách)* |
| lỗi | ⛔ đổi *(câu lỗi đúng câu cửa trả)* |
| mất kết nối | ⛔ đổi *(câu lỗi + `Thử lại`)* |
| có dữ liệu | lệnh khớp mã **chỉ** khác tiền tệ nằm trong `Chưa gán` với nút rổ `nguoi`, ô *Giao dịch* in câu `vi_sao` *(⛔ `đề xuất:`)*; vùng ứng viên: mã cùng tệ › mã khác tệ *(`≠`, câu *"cửa ghi sẽ TỪ CHỐI"*)* › bậc tiền; chú giải + ô `.tg` ⛔ tông đọc được *(≥ ngưỡng `NFR-I29`)*; khối *"Đang gán"* bậc lạ in nguyên tên, khác tiền tệ ⛔ khớp mã ⇒ `≠` |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** `fls_itl` / `fls_pm_line` / `fls_moi_noi` qua cửa có sẵn. Cửa **đọc** `lenh-cho` *(+ `/ro`)* · `lenh-da-gan` · `itl-candidates` đổi **giá trị** `ro` · `vi_sao` · `ung_vien_itl` · `the.gd` · `bac` · **thứ tự** `ung_vien` — ⛔ tuyến mới, ⛔ khoá mới *(ngoài một **giá trị** khoá mới `ma_khop_khac_tien_te` của `vi_sao`)*.
  ⭐ **Đính chính** *(`TL-038`)*: *"⛔ khoá mới"* **sai với chính `(g)`** — `BA-06` v4.16 đòi ô in câu `vi_sao` mà màn đọc `the`, và `the` ⛔ chở nó. ⇒ Phiếu **có** một khoá mới: **`the.vi_sao`** *(chỉ ở nhánh khớp mã khác tiền tệ; giá trị = `vi_sao` của chính hàng — ⛔ sự thật thứ hai)*, nay khai ở `BA-07` **v3.10** `§4h ⓵'`. Vòng 2 thêm **một** khoá nữa: `lenh-cho/ro` `nguoi_khac_tien_te` *(`(i)`)*.
- Ghi kho THẬT: **`KHONG`**. Máy **8088** vẫn **CHỈ ĐỌC** *(chỉ `GET` cho `AC-9`)*. Mọi cú ghi *(dựng ca)* trên **kho TEST** qua máy **8099** / bài thử.
- Số dòng sổ thật **chữ in / rổ** sẽ đổi *(đã đếm — `fls-ba` 02/10, ảnh `NAP-2026-10-02-PMA07ED283`)*: **84** lệnh `may` → `nguoi` *(= 84 ô `đề xuất:` → câu `vi_sao`)*; `nguoi` **532 → 616**, `may` **268 → 184**; `Chưa gán` ⛔ đổi; `gd_ds` khác tiền tệ đổi bậc **0 / 2.262**; thứ tự `itl-candidates` đổi **0** lệnh *(⛔ lệnh nào có cả hai loại dòng khớp mã)*; chú giải + ô `.tg` đổi màu ở **mọi** lượt mở màn ghép. ⇒ Báo động hiếm: chạm **84 / 1.601** lệnh chờ *(5,2 %)*.

## Nền khi nhận *(`fls-ba` đo / chép 02/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — commit giấy `fls-ba` sau `9bea347` *(`KQ-036`)*; mã `fls/**` cuối = `932d8a4` *(`WO-032` vòng 2)* | `git log` |
| `pytest` | **`2224 passed, 6 xfailed`** *(`KQ-036` đo cuối lượt; 6 = 3 `kq021` của `WO-023` + 3 `kq036` của phiếu này)* ⇒ sau phiếu: 3 `kq036` thành `XPASS(strict)` *(đúng ý)*, 3 `kq021` **vẫn** `xfail` | `KQ-036` bảng cổng |
| `kiem_so_song` | **49** *(`fls-ba` chạy 02/10 sau tờ giấy `BA-07` v3.9 / `BA-06` v4.16 / `BA-08` v1.3 + ô master §8: `⛔ CONG SO SONG KHONG DAT — 49 lech/khong-do-duoc` — = nền `KQ-036`; giữa lượt có **1** đỏ mới do chính tờ này *(`master · §8 version BA-08` mẫu khớp 0 lần)*, đã neo lại chữ ô master)* | lệnh |
| rổ sổ thật | `may` **268** · `nguoi` **532** · `khong` **801** · `tu_chung` **64** · `tong` **1.601**; `gd` khác tiền tệ **84 / 268** | `fls-ba` đo, hàm thật |
| version spec | `BA-07` **v3.9** · `BA-06` **v4.16** · `BA-08` **v1.3** | header tệp |

## Câu còn treo
- ⭐ **`Q-FX-1`** *(owner — mới 02/10)*: **84** lệnh chi có số chứng từ khớp một dòng tiền bằng **tiền tệ khác** *(lệnh USD ↔ tiền VND 60 · VND ↔ USD 15 · SGD ↔ USD 5 · USD ↔ SGD 3 · HKD ↔ USD 1)*; phần lớn tỷ số trông như **quy đổi ngoại tệ**. Hôm nay FLS **⛔ ghép được** cặp ấy *(`QĐ-ITL-62` — ⛔ so / ghép khác tiền tệ)*. Kế toán ghi nhận lệnh trả bằng tiền tệ khác thế nào — ghép kèm tỷ giá, ghép không so tiền, hay để ngoài FLS? **Vì sao phiếu này vẫn làm được:** phiếu chỉ dừng máy **nói** nó trả lời được và **đề xuất** cặp bị từ chối; câu trả lời của owner mở một lối ghép **mới** *(việc riêng, đổi cửa ghi)* — lệnh khi ấy rời `nguoi` theo luật mới, ⛔ đụng phần phiếu này sửa.
- `Q-TIEN-1` *(owner, từ `WO-022`/`WO-032`)* vẫn ⛔ chặn.

## Rủi ro
1. **Ảnh PM trôi theo nhịp** *(`11_BOI_CANH` §7)* ⇒ `AC-2` so tập `pm_line_id` trên **cùng** `run_id` nền ↔ sau; ⛔ so với số `84` của tờ này.
2. **Luật so tiền tệ thứ ba còn sống ở SQL** — `lenh_cho.py:208`/`:215` `upper(i.curr) = s.cur` *(⛔ `trim` phía sổ)*: sổ thật **0** giá trị `curr` có khoảng trắng *(`KQ-036` `SELECT`)* ⇒ **NGOÀI** phiếu; ghi vào `BG` nếu Dev đụng tới, ⛔ sửa lẻ.
3. **Kho TEST phình** *(bài dựng ca qua cửa thật)* ⇒ bài `*_pg` có thể đỏ vì `timeout` — tiền ngẫu nhiên + `run_id` `NAP-2000-…` như `KQ-031`/`KQ-036`, ⛔ nới timeout, ⛔ `TRUNCATE`.

## ⭐ Vòng 2 *(02/10, `fls-ba` — [`TL-038`](HOI-038-o-giao-dich-doc-vi-sao-tu-dau-va-cau-nao.md))*

### Vì sao có vòng 2
- [`BG-039`](BG-039-ban-giao-wo-037.md) yếu **#1**: chính vòng 1 làm một câu màn **sai sự thật** — băng *"Việc của bạn hôm nay"* của `F01L` nói *"Chưa có số chứng từ"* cho cả rổ `nguoi`, mà **84 / 616** lệnh trong rổ **có** số chứng từ *(`fls-ba` 02/10, sổ thật chỉ đọc, hàm thật `xep_ro` mọi trang: ⛔ mã **532** ＋ `la_khop_ma_chi_khac_tien_te` **84**)*. Cùng khối, dòng ghi chú *"khớp số chứng từ nhưng **lệch tiền**"* *(`may − tu_chung` = **120**)* đúng cho **78 / 120**: **39** lệnh có **một** dòng cùng tệ **khớp đúng tiền** mà cửa ghi vẫn ⛔ nhận theo lô ＋ **3** lệnh nhiều dòng có dòng khớp tiền.
- yếu **#4**: **3 / 3** câu `lc.VI_SAO` mang ký hiệu cấm *(`⛔` ×1 · ×1 · ×2)* — Chrome vẽ thành biểu tượng tròn đỏ giữa câu ở `F01L` `hint`; ⛔ cổng nào quét chuỗi Python.
- yếu **#3**: SQL `itl-candidates` so `upper(i.curr)` ⛔ `trim` — luật so tiền tệ **thứ ba** còn sống *(sổ thật **0 / 8.387** ca — sửa vì **một** luật, ⛔ vì báo động)*.
- yếu **#7**: bài quét AST `AC-5` chỉ quét `xu_ly.py`, ⛔ `lenh_cho.py`.
- ⛔ NGOÀI: cổng nào của cửa ghi giữ **39** lệnh khớp đúng tiền *(chưa đo — câu mới ⛔ khẳng định)*; đưa `man_f01*.js` vào `THEO_LUAT` *(nợ đã biết, cả tệp)*.

### Spec phải đọc *(vòng 2)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/07_API_CONTRACT.md` | **§4g** đoạn v3.10 sau *"`lenh-cho/ro` — BA RỔ"* *(`nguoi_khac_tien_te`)* · đoạn v3.10 sau bảng ⓐ…ⓓ *(bảng **chữ in** ba câu `VI_SAO` + đoạn SQL `btrim`)* · **§4h ⓵'** hàng **`the.vi_sao`** | ⭐ **v3.10** |
| `02_BA/06_SCREEN_SPEC.md` | **§4.5** đoạn v4.17 *(câu thứ sáu đọc `the.vi_sao`)* · **§4.5 ⓤ** *(chữ nguyên văn băng + bảng rổ `F01L`, năm trạng thái, ca biên)* | ⭐ **v4.17** |
| `02_BA/13_THUYET_MINH_MAN_HINH.md` | `F01L ⓪` đoạn v1.8 | ⭐ **v1.8** |
| `01_Orchestrator/handoff/HOI-038-…md` | `TL-038` + bảng *Bốn mục yếu* | — |

### Phạm vi vòng 2
| TRONG | NGOÀI |
|---|---|
| **(i) Rổ `nguoi` nói hai câu** *(`BA-07` v3.10 `§4g` · `BA-06` v4.17 `§4.5 ⓤ`)*: `dem_theo_ro` ＋ khoá **`nguoi_khac_tien_te`** đếm bằng `lc.la_khop_ma_chi_khac_tien_te` *(⛔ so chuỗi, ⛔ điều kiện thứ hai)*; `man_f01_lenh.js::_ve_viec` dòng 2 *(tiêu đề + `hint` hai câu)* + dòng ghi chú `may − tu_chung` + `RO.nguoi` *(bảng rổ)* = **chữ nguyên văn** `§4.5 ⓤ` | ⛔ đổi dòng 1/dòng 3 của băng, hàng `may`/`khong` của bảng rổ, nút *Bắt đầu tra* · ⛔ đổi rổ nào · ⛔ chip mới · ⛔ gỡ ký hiệu ở chỗ khác của `man_f01*.js` |
| **(j) Ba câu `VI_SAO` ⛔ ký hiệu cấm** *(`BA-07` v3.10 bảng chữ in)*: đổi **chữ** ba giá trị `lc.VI_SAO` đúng nguyên văn; bài cổng mới: mọi giá trị `VI_SAO` *(＋ đầu ra `cau_ma_khop_khac_tien_te`)* có **0** ký tự trong `CAM` của `test_luat_ky_hieu_man_hinh.py` *(dùng lại hằng ấy — ⛔ chép)* | ⛔ đổi khoá · ⛔ đổi tập lệnh mang câu nào · ⛔ đổi `THEO_LUAT` |
| **(k) SQL vế sổ `btrim`** *(`BA-07` v3.10)*: `_SQL_ITL_UNG_VIEN` + `_SQL_DEM_CUNG_TE` so `upper(btrim(i.curr, E' \t\r\n')) = <mã lệnh qua ma_tien_te>` | ⛔ đổi bậc · ⛔ đổi thứ tự · ⛔ SQL mới |
| **(l) Quét so tiền tệ phủ `lenh_cho.py`**: bài quét AST `AC-5` chạy trên **cả** `fls/api/xu_ly.py` **và** `fls/repo/lenh_cho.py`; ＋ ghim: trong `fls/` **0** chuỗi `upper(i.curr)` trần *(mọi vế sổ SQL qua `btrim`)* | ⛔ quét tệp ngoài hai tệp ấy *(mở rộng ⇒ phiếu mới)* |
| **(m) Bài thử** — như `(h)`: thân màn từ **cửa thật** kho TEST; chứng minh ĐỎ trên `4c3b2ae` trước | ⛔ sửa / gỡ dấu `tests/nghiem_thu/**` |

### Tiêu chí nghiệm thu vòng 2 *(`AC-1`…`AC-10` vòng 1 **vẫn** là đối tượng kiểm trên mã vòng 2; `AC-8`/`AC-9` so chuỗi với câu **v3.10**)*
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-11 *(i · cửa)* | Kho TEST qua **HTTP** `GET /queue/lenh-cho/ro`: khoá `nguoi_khac_tien_te` **luôn có**, kiểu `int`; ca `K` *(`ca_wo037`)* ⇒ ≥ 1; **bằng đúng** số hàng `?ro=nguoi` *(mọi trang)* có `the.vi_sao`. **Sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, hàm thật, cùng ảnh — in `run_id`)*: `nguoi_khac_tien_te` = số thẻ `the.vi_sao` trên `?ro=nguoi` *(mong ≈ **84**)*, `≤ nguoi`; `nguoi − nguoi_khac_tien_te` = số hàng `nguoi` có `ma_canon` rỗng *(mong ≈ **532**)*; mẫu số in ra > 0 *(`Đ3`)* | bài cửa `tests/api/` + phép đo chỉ đọc *(kịch bản trong `BG`)* | đếm mọi `nguoi` có `vi_sao` *(⇒ 616)* ⇒ **ĐỎ**; khoá vắng khi `0` ⇒ **ĐỎ** |
| AC-12 *(i · màn)* | Thân `/lenh-cho/ro` **cửa thật** kho TEST vào `man_f01_lenh.js` thật: dòng 2 tiêu đề **=** chữ `§4.5 ⓤ`; `hint` **=** câu ① *(＋ câu ② khi `b > 0`)* với `a`, `b` lấy từ thân; ca `b = 0` *(đổi **giá trị** `nguoi_khac_tien_te` của thân thật về `0`)* ⇒ **chỉ** câu ①; dòng ghi chú **=** chữ `§4.5 ⓤ`, ⛔ còn chữ *"lệch tiền</b> — trả nhiều đợt"* cũ; bảng rổ hàng `nguoi` **=** chữ `§4.5 ⓤ`. Bốn chuỗi ấy **0** ký tự `CAM` | bài DOM `tests/web/` | chữ cũ *"Chưa có số chứng từ"* ⇒ **ĐỎ**; màn tự đếm `b` từ trang ⇒ **ĐỎ** |
| AC-13 *(j)* | Mọi giá trị `lc.VI_SAO` **=** bảng chữ in v3.10 *(so chuỗi)*; mọi giá trị ＋ `cau_ma_khop_khac_tien_te(['USD'])` có **0** ký tự `CAM`; bài cổng tự chứng: chèn `⛔` vào một bản sao giá trị ⇒ bắt **1** | bài đơn vị + bài cổng | trả lại câu v3.9 ⇒ **ĐỎ** |
| AC-14 *(k)* | Kho TEST: lệnh VND số tiền `X` + dòng tiền chưa nối `curr = ' vnd '` *(⛔ mã khớp)* số tiền `X` ⇒ `itl-candidates` có dòng ấy bậc `tien`; `tong_cung_tien_te` đếm nó. Sổ thật: `curr` có khoảng trắng **0 / 8.387** ⇒ ⛔ ca nào đổi *(in mẫu số)* | bài cửa `tests/api/` | bỏ `btrim` ⇒ **ĐỎ** |
| AC-15 *(l)* | Bài quét AST chạy trên `xu_ly.py` **và** `lenh_cho.py` ⇒ **0**; bài tự chứng: mẫu `str(x).strip().upper() == …` chèn vào bản sao nguồn `lenh_cho.py` ⇒ bắt **1**; grep `fls/` chuỗi `upper(i.curr)` ⛔ qua `btrim` ⇒ **0** | bài quét | quét chỉ `xu_ly.py` ⇒ bài tự chứng **ĐỎ** |
| AC-16 ⭐ *(Chrome)* | Chrome **1440×900** chuột thật: **8099** `--cho-ghi` kho TEST ca `ca_wo037` ⇒ `② Hàng chờ` băng dòng 2 in đúng hai câu *(số = thân `/ro`)*, ghi chú đúng chữ; hàng `K` `hint` = câu `ma_khop_khac_tien_te` v3.10, **0** biểu tượng `⛔`; `②b` ô *Giao dịch* hàng `K` = cùng câu. **8097** sổ thật **chỉ đọc** *(⛔ `--cho-ghi`, Chrome chặn ⛔ `GET`)*: băng in `a`/`b`/`c` khớp phép đo `AC-11` cùng ảnh. Console **0** lỗi · **0** lượt ⛔ `GET` phát ra. **8088 ⛔ chạm** | Chrome CDP; `BG` dán số đo | — |
| AC-17 | Cổng `CLAUDE.md` như `AC-10`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai *(3 `XPASS(strict)` `kq036` vẫn đúng ý nếu `fls-test` chưa gỡ dấu)* · `lint-imports` 9/0 · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền vòng 2** ⟷ đỏ mới loại (c); ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

### Màn hình *(vòng 2)*
- Thiết kế: `BA-06` **v4.17** `§4.5 ⓤ` *(chữ nguyên văn)* · `BA-13` **v1.8**. ⛔ token, ⛔ lớp CSS mới — dòng 2 dùng lại `viec` / `hint` / `note warn` đang có.

| Trạng thái | Hiện gì *(`F01L` băng *Việc của bạn hôm nay* · bảng rổ)* |
|---|---|
| tải | ⛔ đổi *(`TT.chay`, khung chờ 3 dòng)* |
| rỗng | ⛔ đổi *(`tong = 0` ⇒ câu rỗng hiện có)* |
| lỗi | ⛔ đổi *(câu lỗi cửa trả)* |
| mất kết nối | ⛔ đổi *(câu lỗi + `Thử lại`)* |
| có dữ liệu | dòng 2 tiêu đề *"CẦN BẠN tra — máy chưa đề xuất được dòng tiền"* · `hint` `a` dòng ⛔ số chứng từ ＋ *(khi `b > 0`)* `b` dòng khớp mã ở tiền tệ khác · ghi chú `c` dòng *cửa ghi chưa nhận theo lô* · hàng `nguoi` bảng rổ câu mới; câu `vi_sao` dưới mã lệnh ⛔ biểu tượng đỏ |

### Dữ liệu *(vòng 2)*
- Bảng/cột chạm: **⛔ bảng nào** — chỉ đọc. Cửa `lenh-cho/ro` ＋ **một** khoá `nguoi_khac_tien_te` *(khai `BA-07` v3.10)*; `lenh-cho` *(+ `/ro`)* / `lenh-da-gan` đổi **chữ** `vi_sao`; `itl-candidates` đổi phép so SQL *(0 ca sổ thật)*.
- Ghi kho THẬT: **`KHONG`**. **8088** ⛔ chạm; ca dựng trên kho TEST.
- Chữ in sẽ đổi trên sổ thật *(`fls-ba` 02/10; `max(run_id)` của `fls_pm_line` lúc đo = `NAP-2026-10-02-PMF7DEEC9F` — ⚠ ảnh đã trôi so với `…PMA07ED283` của vòng 1, số đếm rổ ⛔ đổi)*: câu `vi_sao` của **1.417** lệnh *(`khong` 801 ＋ `nguoi` 616)* đổi chữ, ⛔ đổi nghĩa; băng `F01L` **1** khối *(dòng 2 + ghi chú)*; `itl-candidates` **0** lệnh. ⇒ Báo động hiếm: ⛔ áp — đây là chữ in, ⛔ cảnh báo mới.

### Nền khi nhận vòng 2 *(Dev đo lại, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | commit giấy `fls-ba` `TL-038` *(sau `003af61`)*; mã `fls/**` cuối = `4c3b2ae` | `git log` |
| `pytest` | **3 failed = 3 `XPASS(strict)` `kq036`, 2246 passed, 3 xfailed** | `BG-039` |
| version spec | `BA-07` **v3.10** · `BA-06` **v4.17** · `BA-13` **v1.8** · `BA-08` **v1.3** | header tệp |
| `kiem_so_song` | **49** *(`fls-ba` chạy sau tờ giấy vòng 2 + master §8 theo version mới — nhật ký §5)* | lệnh |
| sổ thật | `dem_theo_ro` `may` **184** · `nguoi` **616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601**; `nguoi` ⛔ mã **532** · khớp mã khác tệ **84**; `may − tu_chung` **120** *(lệch tiền 78 · khớp tiền 42)*; `curr` khoảng trắng **0 / 8.387** | `fls-ba` đo, hàm thật, chỉ đọc |

### Câu còn treo *(vòng 2)*
- ⛔ câu mới. `Q-FX-1` *(owner — 84 lệnh trả bằng tiền tệ khác)* và `Q-TIEN-1` vẫn ⛔ chặn: câu ② của băng nói **sự thật hôm nay** *(cửa ghi chưa ghép hai tiền tệ)*, ⛔ nói kế toán phải làm gì.

### Rủi ro *(vòng 2)*
1. **Chữ `vi_sao` đổi ⇒ bài vòng 1 so chuỗi** *(`AC-8` · `AC-9` · `tests/web/test_wo037_*`)* phải so với hằng `VI_SAO`, ⛔ chuỗi gõ lại — chỗ nào gõ lại sẽ đỏ đúng lúc.
2. **Ảnh PM trôi** — `AC-11`/`AC-16` đo `a`/`b`/`c` trên **cùng** ảnh, ⛔ so với số của tờ này.
3. `dem_theo_ro` đã kéo mọi trang *(~70–90 s sổ thật)* — thêm phép đếm trên **cùng** vòng lặp, ⛔ vòng lặp thứ hai.

## Nghiệm thu PO *(`fls-ba` · 2026-10-05 — đọc `KQ-041` 17/17)*

⭐ **Điều phối quyết** *(phiên chính 05/10 — ghi kèm, ⛔ sửa phán quyết của `fls-test`)*: `WO-037` **ĐẠT**. `F-3` `NANG` nằm **NGOÀI** phạm vi — có từ `9ed4d4a` *(22/09)*, diff `WO-037` chạm `tai_danh_sach`/`doi_chip`/`mo_man` **0** dòng ⇒ ⛔ chặn phiếu; `fls-ba` phát phiếu riêng [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md) *(ưu tiên **CAO**, trước `WO-015`/`WO-023`)*.

Đối chiếu **ý owner** *(⛔ chỉ AC)*: phiếu này phải làm cho **máy gợi ý ⛔ dẫn kế toán vào ngõ cụt** — rổ *"máy trả lời được"* chỉ chứa cặp **cửa ghi nhận**, và màn nói **vì sao** khi máy ⛔ đề xuất được.

| Ý owner / spec | Lời gốc | Đo được *(`KQ-041`)* | Khớp |
|---|---|---|:-:|
| Máy gợi ý ⛔ dẫn vào ngõ cụt *(`B5` — vòng ghép thật đầu tiên mở rổ `may` trước)* | `09` mốc `B` · `QĐ-ITL-27` | rổ `may` có `gd` khác tiền tệ **84 / 268 → 0 / 184**; oracle **độc lập** *(SQL tự viết, cùng ảnh `NAP-2026-10-02-PMA07ED283`)* lệch **0 / 1.601** `pm_line_id`; tập rời = tập nền **84 / 84** | ✅ |
| `QĐ-ITL-62` — ⛔ so / ghép khác tiền tệ | owner 28/08 | 8099 chuột thật: chọn dòng USD ⇒ *"Khác tiền tệ — cửa ghi sẽ từ chối cặp này."*, bấm `Gán` ⇒ hỏi xác nhận, **0** `POST`; thứ tự bậc `ma`: cùng tệ › khác tệ › bậc tiền | ✅ |
| ⛔ đẩy trùng tiền tình cờ lên đầu *(phương án bị loại — `Căn cứ` ⓑ)* | spec `fls-ba` 02/10 | lệnh `nguoi` khớp mã khác tệ ⇒ `gd = null`, ô *Giao dịch* in câu `vi_sao` có mã thật *(`USD` 16,73 : 1)*, ⛔ *"đề xuất:"* | ✅ |
| Màn nói đúng *"vì sao"* — rổ `nguoi` hai câu theo số **cửa** | `BA-06` v4.17 `§4.5 ⓤ` | 8088 băng `532 · 84 · 120` = oracle cùng ảnh; ca `a = 0 ∧ b > 0` trên cửa thật đúng chữ | ✅ |
| `QĐ-ITL-27` — kiểm soát trong máy *(⛔ khuôn thử tự nhét)* | owner 22/08 | thân màn từ **cửa thật** kho TEST; đột biến *"`xep_ro` luật cũ"* / *"đếm mọi `nguoi`"* ⇒ oracle **ĐỎ** | ✅ |
| `NFR-I29` — chữ nghĩa đọc được | `BA-08` v1.3 | chú giải **4,92** *(5/5 · 9/9)* · ô `≠` / `④` **5,59** | ✅ |
| `QĐ-ITL-150 ⓑⓒ` — ⛔ `dong_bo --ghi` để làm xanh `BG` | owner 01/10 | `kiem_so_song` **50** = nền **49** ＋ **1** chân trang theo đồng hồ, tên trùng 33 / 33 | ✅ |

⇒ **ĐẠT — đóng phiếu.** Ba phát hiện của `KQ-041` ⛔ chặn và đã xếp: `F-1` `NHE` *(ba chỗ `F01L` còn hứa *"lệch tiền"* / *"chỉ DUYỆT"* — chữ ngoài phạm vi `(i)`)* ⇒ `BA-06` **v4.18** `§4.5 ⓤ` · `F-2` `NHE` *(tập khoảng trắng SQL hẹp hơn Python — sổ thật **0** ca)* ⇒ `BA-07` **v3.11** · `F-3` `NANG` ngoài phạm vi ⇒ `BA-06` **v4.18** `§4.5 ⓥ` — cả ba ⇒ [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md). Thông tin **39** lệnh khớp đúng tiền mà cửa ghi giữ *(`chum_lech_tien` 25 · `co_dong_chua_duyet` 14)*: màn ⛔ nói lý do **từng hàng** ⇒ `GAP-SCR-34` *(mới)*; câu **chung** sửa trong `WO-042 (b)`.

## Changelog
- 2026-10-02 · `fls-ba` · phát **`WO-037`** `MO` từ nghiệm thu PO `WO-032`: gom `KQ-036` `F-1`/`F-2`/`F-3`/`F-4` *(phần mã)*/`F-6`; spec `BA-07` **v3.9** · `BA-06` **v4.16** · `BA-08` **v1.3**. ⭐ `F-6` đo lại *(hàm thật, chỉ đọc)*: **84 / 84** lệnh chỉ khớp mã ở tiền tệ khác ⇒ sửa **rổ** theo cửa ghi, ⛔ đảo thứ tự *(45 ứng viên lệch 0 là trùng tiền tình cờ)*. Ưu tiên **CAO**, thứ tự `WO-037` → `WO-015` → `WO-023`. Câu owner mới `Q-FX-1` ⛔ chặn.
- 2026-10-05 · `fls-dev` · vòng 2 xong ⇒ **`BG-040`** @ `3c13ce3` *(`(i)` `nguoi_khac_tien_te` + băng `F01L` hai câu · `(j)` `VI_SAO` chữ in v3.10 · `(k)` SQL `btrim` · `(l)` quét phủ `lenh_cho.py`; sổ thật chỉ đọc `nguoi_khac_tien_te` **84** = `the.vi_sao` **84**; `pytest` 3 `XPASS(strict)` `kq036`, 2262 passed, 3 xfailed; `kiem_so_song` 49 = nền)* → `CHO_TEST`.
- 2026-10-02 · `fls-ba` · **`TL-038`** ⇒ phương án **B** *(`the.vi_sao` chỉ ở nhánh khớp mã khác tiền tệ — 84 ô)*; **đính chính** `(g)` + mục `Dữ liệu` *("⛔ khoá mới" sai với chính `(g)`)*; mở **vòng 2** `(i)` `(j)` `(k)` `(l)` từ `BG-039` yếu #1/#4/#3/#7 · `AC-11`…`AC-17`; spec `BA-07` **v3.10** · `BA-06` **v4.17** · `BA-13` **v1.8**. `fls-test` kiểm **gộp** `BG-039` ＋ `BG` vòng 2.
- 2026-10-05 · `fls-ba` · `CHO_TEST` vòng 2 → ✅ **`DONG`** — nghiệm thu PO *(bảng trên: 7 ý owner/spec khớp)*; ghi **điều phối quyết** *(`F-3` `NANG` ngoài phạm vi ⇒ ⛔ chặn)*. Xếp `KQ-041`: `F-1` ⇒ `BA-06` **v4.18** `§4.5 ⓤ` · `F-2` ⇒ `BA-07` **v3.11** · `F-3` ⇒ `BA-06` **v4.18** `§4.5 ⓥ` ⇒ phát [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md); 39 lệnh ⇒ `GAP-SCR-34`. `Q-FX-1` + `Q-TIEN-1` đi tiếp ở `WO-042` *(⛔ chặn)*.
