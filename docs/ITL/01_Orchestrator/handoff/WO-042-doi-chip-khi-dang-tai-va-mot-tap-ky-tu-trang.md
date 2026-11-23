# WO-042 — Đổi chip khi danh sách đang tải ⛔ còn trộn hai rổ · chữ `F01L` ⛔ còn hứa *"lệch tiền"* cho cả rổ `may` · một tập ký tự trắng cho mọi phép so tiền tệ

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(05/10 — `fls-ba` nghiệm thu PO: [`KQ-046`](KQ-046-kiem-bg-044.md) ✅ ĐẠT **12/12**, 0 `CHAN` / `NANG`; Chrome chuột thật 8088 sổ thật chip `Đã gán` **2955 → 2219** · `Chưa gán` **1472 → 736** = thân cửa; bảng đối chiếu ý owner ở mục **Nghiệm thu PO** cuối phiếu; `F-1` ⇒ [`WO-047`](WO-047-mot-tap-ky-tu-cho-phep-so-tien-te-con-lai.md) · `F-2` sửa ở tờ này *(mục Đính chính)* · `F-3` ⇒ [`WO-045`](WO-045-luot-tai-moi-nhat-moi-man-va-xem-them-chi-doc.md) ⑤)* · ~~`CHO_TEST`~~ *(`fls-dev` nhận 05/10 @ `77737f7` · bàn giao [`BG-044`](BG-044-ban-giao-wo-042.md) · câu [`HOI-043`](HOI-043-ba-bai-kq041-khong-the-xpass-va-nut-thu-lai.md) ✅ trả `TL-043` 05/10 — đọc AC theo mục **Đính chính `TL-043`** dưới)* · ⭐ **SẴN SÀNG** · ưu tiên **CAO** — làm **TRƯỚC** [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) và [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-05 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md) *(✅ `DONG` 05/10 — phiếu này đứng trên băng `F01L` v4.17, `nguoi_khac_tien_te`, `ma_tien_te`, SQL `btrim` của nó)*. ⭐ **TRƯỚC `WO-015` + `WO-023`** — lý do ở mục **Vì sao ưu tiên CAO** dưới |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết **một vòng ghép thật** — hôm nay đo được **0**)*. Vòng ấy đi qua đúng hai màn phiếu này sửa: danh sách `②b` *(`F01G`, chip `Chưa gán` / `Đã gán`)* và băng *"Việc của bạn hôm nay"* + bảng rổ *(`F01L`)*.
  - ⭐ **`F-3`** *(`KQ-041`, `NANG`)*: bấm chip trong lúc danh sách đang tải *(~1–3 s cửa đang trả — thao tác **thường**)* ⇒ màn in **một con số sai** và **trộn hai rổ**: 8088 sổ thật chỉ đọc, chip `Đã gán` in **`2955 dòng`** = **2.219** đã gán ＋ **736** chưa gán; bấm lại chip đang chọn ⇒ **1.472** = 736 × 2. Người đầu tiên đổi chip sẽ thấy sổ có gần **gấp rưỡi** số lệnh đã gán — và học rằng con số trên chip ⛔ đáng tin.
  - **`F-1`** *(`NHE`)*: ba chỗ của `F01L` hứa *"lệch tiền"* / *"khớp đúng một dòng — người chỉ DUYỆT"* cho cả rổ `may`; sổ thật *"lệch tiền"* đúng **78 / 120**, *"chỉ DUYỆT"* sai **120 / 184**.
  - **`F-2`** *(`NHE`)*: phép so tiền tệ sống ở **bốn** tập ký tự trắng khác nhau *(Python 29 · SQL 4 · JS 25 — `BA-07` v3.11)*; sổ thật **0** ca ⇒ sửa vì **một luật**.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; phiếu này giữ mắt xích **"ghép PM ↔ tiền"** đã chuyển lên FLS **⛔ thua Sheets** — trên Sheets một bộ lọc ⛔ bao giờ đếm một dòng hai lần; `QĐ-ITL-27` *(2–3 kế toán, kiểm soát nằm trong máy)*: một con số máy in sai là dạy người **tự đếm lại**.

### Vì sao ưu tiên CAO *(PO — trên `WO-015` và `WO-023`)*
| Phiếu | Hại hôm nay nếu ⛔ làm | Chạm vòng ghép thật đầu tiên? |
|---|---|:-:|
| ⭐ **`WO-042`** | chip in **2.955** thay **2.219** *(hoặc **1.472** thay **736**)* khi đổi chip lúc đang tải — tái hiện bằng thao tác thường; rổ trộn | ✅ **trực tiếp** — chip là thứ kế toán bấm **đầu tiên** ở `②b` |
| `WO-015` | thước *"người thật"* có bốn lỗ; sổ thật hôm nay **⛔ con số nào đổi** | ⛔ |
| `WO-023` | hộp modal / phím / mã `409`; hôm nay **0** ghi sai *(cửa ghi chặn)* | gián tiếp *(cách hộp đóng mở)* — và cùng tệp `man_f01_ghep.js` ⇒ làm **sau** để bài thử hộp dựng trên `tai_danh_sach` đã chống chồng |

⛔ **Không** xếp trên mức **CAO**: cửa ghi vẫn chặn ⇒ **0** ghi sai *(`KQ-041`: mọi lượt Chrome chặn `GET`, `POST` **0**)*; hại là **đọc sai**, ⛔ sai sổ.

⭐ **Vì sao gom `F-1` + `F-2` vào cùng phiếu** *(⛔ tách ba phiếu)*: ⓐ cả ba nằm trên **hai màn của cùng một vòng ghép** *(`man_f01_ghep.js` + `man_f01_lenh.js`, chung tab `② Hàng chờ`)* và `WO-023` sẽ chạm lại đúng hai tệp ấy ⇒ dọn một lần trước nó; ⓑ `F-1` là **chữ** *(4 chuỗi, spec viết sẵn)*, `F-2` là **một hằng + thay lời gọi** — cả hai ⛔ đủ lớn để thành một vòng `WO → BG → KQ` riêng *(mỗi vòng ~1 lượt `pytest` 6–7 phút + Chrome hai máy)*; ⓒ thứ tự **bên trong** phiếu: `(a)` `F-3` **trước** — nếu `(c)` vướng *(nhập vòng, `lint-imports`)*, Dev mở `HOI` cho `(c)` và bàn giao `(a)` + `(b)` trước, ⛔ giữ `F-3` chờ.

## Căn cứ
- [`KQ-041`](KQ-041-kiem-bg-039-bg-040.md) *(`fls-test` 05/10, ✅ ĐẠT `WO-037` 17/17)* — *Phát hiện*: `F-1` `NHE` `man_f01_lenh.js:308-313` · `:799` · `RO.may` *(`:275`)* · `F-2` `NHE` `lenh_cho.py` `_SQL_ITL_UNG_VIEN` / `_SQL_DEM_CUNG_TE` `btrim(i.curr, E' \t\r\n')` ⟷ `str.strip()` *(PG thật: 6 chuỗi biên lệch **6 / 6**)* · ⭐ `F-3` **`NANG`** `man_f01_ghep.js:890-913` `tai_danh_sach` ⛔ chống tải chồng *(có từ `9ed4d4a` 22/09)*. Ba bài `xfail(strict)` `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py`: `::test_F2_ca_bien_SQL_ve_so_BANG_ma_tien_te` · `::test_F3_doi_chip_KHI_DANG_TAI_danh_sach_KHONG_tron_ro_cu` · `::test_F3_bam_lai_chip_DANG_CHON_khi_dang_tai_KHONG_nhan_doi` ＋ mỏ neo `::test_CANH_doi_chip_SAU_khi_tai_xong_danh_sach_dung_mot_ro`.
- ⭐ **Điều phối quyết 05/10** *(phiên chính, ghi ở `KQ-041` + `WO-037`)*: `F-3` **ngoài phạm vi** `WO-037` *(diff chạm `tai_danh_sach`/`doi_chip` **0** dòng)* ⇒ ⛔ chặn `WO-037`; phát phiếu riêng, ưu tiên **CAO**, làm trước `WO-015`/`WO-023`.
- `fls-ba` đo 05/10 *(đọc mã + chỉ `SELECT`)*: phép so tiền tệ viết tay ngoài `ma_tien_te` — Python **6** chỗ *(`ghi_tay.py:653` · `:744` · `do_mau_so.py:415` · `:417` · `doc_bao_cao.py:373` · `pm_join.py:435`)*, SQL **2** *(`lenh_cho.py:218` · `:225`)*, JS **2** *(`thanh_phan.js:138` · `:192`)*; `fls_itl.curr` ngoài `^[A-Z]{3}$` **0 / 8.387** · `fls_pm_line.curr` **73 / 276.028** *(toàn giá trị `'20'` — ⛔ khoảng trắng)*.
- **`QĐ-ITL-27`** *(2–3 kế toán, kiểm soát trong máy)* · **`QĐ-ITL-62`** *(⛔ so / ghép khác tiền tệ — một tiền tệ phải là **một** mã sau chuẩn hoá)*.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(chữ màn in · hành vi trạng thái màn · tập ký tự của phép chuẩn hoá mã tiền tệ — ⛔ đổi sổ, ⛔ đổi Final, ⛔ tuyến mới, ⛔ khoá cửa mới)*. Cái giá duy nhất ngoài màn: cửa ghi nhận thêm U+FEFF + U+001C–U+001F + U+0085 ở mép mã tiền tệ như khoảng trắng *(sổ thật **0** dòng chạm)*.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | **§4.5 ⓤ** đoạn v4.18 *(bảng bốn chuỗi ⓐ…ⓓ + câu `LY_DO_LO`)* · ⭐ **§4.5 ⓥ** *(đổi chip khi đang tải — bốn luật ①…④)* | ⭐ **v4.18** |
| `02_BA/07_API_CONTRACT.md` | **§4g** đoạn v3.11 sau đoạn v3.10 *"Phép so tiền tệ trong SQL…"* *(bảng luật `TAP_TRANG_TIEN_TE`)* | ⭐ **v3.11** |
| `02_BA/13_THUYET_MINH_MAN_HINH.md` | `F01L ⓪` đoạn v1.9 | ⭐ **v1.9** |
| `01_Orchestrator/handoff/KQ-041-kiem-bg-039-bg-040.md` | *Phát hiện* `F-1` `F-2` `F-3` + lăng kính **Dữ liệu** *(39 lệnh)* + bảng *Bài thử mới* | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| ⭐ **(a) `F-3` lượt tải mới nhất thắng** *(`BA-06` v4.18 `§4.5 ⓥ` ①…④)*: `man_f01_ghep.js` — `tai_danh_sach` · `doi_chip` · `mo_man`. Kết quả của một lượt **đã bị thay** ⛔ vào `ST.dong`, ⛔ đặt `ST.dang_tai = false`, ⛔ đặt `ST.loi`, ⛔ đặt `ST.het`/`ST.con_tro`/`ST.tro`; bấm lại chip **đang chọn** khi đang tải ⇒ ⛔ mở lượt mới *(0 `GET` thêm)*. Cách làm *(số lượt, mã lượt…)* là việc Dev | ⛔ huỷ yêu cầu mạng *(`AbortController`)* · ⛔ đổi `goi_cua.js` / `FLS.doc` · ⛔ đổi `CHIP_CUA` / `TRANG` / `TRAN_DONG` · ⛔ đổi `F01L` `_loc` *(chưa đo có cùng lỗi — xem `(d)`)* |
| **(b) `F-1` bốn chuỗi `F01L`** *(`BA-06` v4.18 `§4.5 ⓤ` bảng ⓐ…ⓓ)*: `man_f01_lenh.js` — ⓐ dòng ghi chú băng · ⓑ `note ok` dưới bảng rổ · ⓒ nhãn thanh lọc `tu_chung === false` · ⓓ `RO.may` *(Nghĩa là gì)*. Câu `LY_DO_LO` là **một** hằng dùng ở ⓐ + ⓑ; số `<t>`, `<c>` lấy từ **cửa** `/lenh-cho/ro` *(như nay)*; bốn chuỗi **0** ký tự `CAM` | ⛔ đổi dòng 1/2/3 của băng · ⛔ đổi hàng `nguoi`/`khong` bảng rổ · ⛔ gỡ ký hiệu ở chỗ khác *(`RO.khong` · dòng 3 băng — nợ `THEO_LUAT`)* · ⛔ lý do **từng hàng** cho 120 lệnh *(`GAP-SCR-34` — khoá cửa mới, phiếu sau)* · ⛔ đổi `Artifacts/Ban-ve-TOBE-Man-Ghep-PM.html` *(biên bản 18/09)* |
| **(c) `F-2` một tập ký tự trắng** *(`BA-07` v3.11)*: **một** hằng `TAP_TRANG_TIEN_TE` *(30 ký tự)*; `ma_tien_te` = `strip(TAP).upper()`; **6** bản viết tay Python thay bằng lời gọi `ma_tien_te` *(giữ đúng nghĩa từng chỗ — vd. `pm_join._cur` vẫn bỏ chuỗi rỗng)*; SQL `_SQL_ITL_UNG_VIEN` + `_SQL_DEM_CUNG_TE` `btrim(i.curr, %(tap)s)` với tham số **từ hằng**; JS **một** hàm mã tiền tệ trên tập ấy *(⛔ `String.trim()`)* cho `ma_te` + `TP.tien` | ⛔ đổi phép chữ hoa *(`upper` ngoài ASCII — sổ thật **0** ca)* · ⛔ chuẩn hoá `curr` lúc nạp *(ghi sổ)* · ⛔ đổi `canon/spec.py:108` *(chữ cột, ⛔ tiền tệ)* · ⛔ đổi luật dung sai |
| **(d) Quét chỗ cùng lớp lỗi `F-3`** — `BG` liệt kê **mọi** hàm trong `fls/web/tep/*.js` có `await` cửa rồi ghi vào trạng thái dùng chung của màn *(tệp:dòng · có chống tải chồng ⛔ / có)* | ⛔ sửa chỗ nào ngoài `(a)` *(thấy ⇒ ghi `BG`, `fls-ba` phát phiếu)* |
| **(e) Bài thử** `tests/api/**` + `tests/web/**` — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; thân màn lấy từ **CỬA THẬT** kho TEST *(HTTP, `assert current_database() = 'fls_test'`)*; cửa chậm dựng bằng **độ trễ có kiểm soát** *(⛔ dựa tốc độ tay)*. Bài `tests/web/test_wo037_v2_bang_f01l_cua_that.py` ghim chữ ghi chú v4.17 ⇒ đổi sang so với **hằng** của màn / chữ v4.18 | ⛔ sửa / gỡ dấu `tests/nghiem_thu/**` *(`fls-test` gỡ ở `KQ` — 3 bài `kq041` sẽ `XPASS(strict)` đúng ý)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a · đổi chip)* | Bài DOM `man_f01_ghep.js` thật, cửa giả **chậm có kiểm soát** *(lượt `Chưa gán` trả **sau** lượt `Đã gán`)*: vào `②b`, đổi sang `Đã gán` khi `Chưa gán` đang tải ⇒ sau khi **cả hai** lượt xong: `ST.dong.length` = số hàng cửa `Đã gán` trả; trạng thái mọi hàng = `da_gan` *(**0** `chua_gan`)*; chip in đúng số ấy. `pytest --runxfail tests/nghiem_thu/test_kq041_*::test_F3_doi_chip_KHI_DANG_TAI_*` ⇒ passed | bài DOM `tests/web/` | `tai_danh_sach` ⛔ kiểm lượt *(mã hôm nay)* ⇒ **ĐỎ** *(`KQ-041`: `['chua_gan','da_gan','chua_gan']`)* |
| AC-2 *(a · bấm lại chip đang chọn)* | Bấm lại chip **đang chọn** khi đang tải ⇒ số lượt gọi cửa **= một lượt** *(đếm `FLS.doc`)*; `ST.dong.length` = số hàng cửa trả *(⛔ × 2)*. `--runxfail …::test_F3_bam_lai_chip_DANG_CHON_*` ⇒ passed | bài DOM | lượt thứ hai mở ⇒ **ĐỎ** *(`n 4 ≠ khac 2`)* |
| AC-3 *(a · trạng thái của lượt cũ)* | Lượt cũ xong **trong khi** lượt mới đang tải ⇒ màn vẫn ở trạng thái **tải** *(`ST.dang_tai === true`, khung *"Đang hỏi sổ…"*)*; lượt cũ **lỗi** ⇒ ⛔ câu lỗi dưới chip mới; lượt **mới** lỗi / mất kết nối ⇒ câu lỗi + `Thử lại` như cũ *(năm trạng thái `ⓥ` ③)* | bài DOM — bốn ca | lượt cũ tắt cờ tải / đặt `ST.loi` ⇒ **ĐỎ** |
| AC-4 *(a · đổi nhanh)* | Đổi chip `Chưa gán → Đã gán → Chưa gán` trong lúc lượt đầu chưa xong ⇒ cuối cùng màn = `Chưa gán`, số dòng = số cửa trả, **0** hàng `da_gan` | bài DOM | ⇒ **ĐỎ** trên mã hôm nay |
| AC-5 ⭐ *(Chrome chuột thật — `F-3`)* | Chrome **1440×900**, **chuột thật** *(`Input.dispatchMouseEvent`)*, độ trễ phản hồi cửa dựng bằng CDP *(`Fetch` giữ ~2 s rồi thả — ⛔ dựa tốc độ tay)*. **8099** `--cho-ghi` trỏ **kho TEST**: ⓐ vào `②b`, bấm `Đã gán` khi `Chưa gán` đang giữ ⇒ chip in **đúng** số hàng cửa `lenh-da-gan` trả *(đếm từ thân cửa thật cùng lượt)*, **0** hàng chưa gán · ⓑ bấm lại `Chưa gán` đang chọn khi đang giữ ⇒ số `GET` = số trang của **một** lượt, số hàng = cửa trả · ⓒ đổi qua lại 3 lần ⇒ chip cuối đúng. **8088 sổ thật CHỈ ĐỌC** *(Chrome chặn ⛔ `GET`)*: lặp ⓐ ⓑ ⇒ chip `Đã gán` = số cửa trả *(mong ≈ **2.219**, ⛔ **2.955**)*; `Chưa gán` = số cửa trả *(mong ≈ **736**, ⛔ **1.472**)*. Console **0** lỗi · **0** `POST`. **Đối chứng** trên `HEAD` khi nhận, cùng máy cùng kịch bản ⇒ tái hiện `2955` / `1472` *(dán vào `BG`)* | Chrome CDP; `BG` dán số đo từng ca *(ảnh ⛔ lên git)* | đối chứng ⛔ tái hiện được ⇒ phép đo ⛔ có giá trị *(`Đ5`)* — ghi `⛔ KHÔNG ĐO ĐƯỢC` |
| AC-6 *(b · chữ, kho TEST)* | Thân `/lenh-cho/ro` **cửa thật** kho TEST *(ca có `tu_chung > 0` và `may − tu_chung > 0`)* vào `man_f01_lenh.js` thật: bốn chuỗi ⓐ ⓑ ⓒ ⓓ **=** `BA-06` v4.18 `§4.5 ⓤ` *(so `textContent`, `<t>`/`<c>` = `TP.so` của thân)*; câu `LY_DO_LO` xuất hiện **giống hệt** ở ⓐ và ⓑ; bốn chuỗi **0** ký tự `CAM`. Quét nguồn `man_f01_lenh.js` *(ngoài chú thích)*: `chỉ LỆCH TIỀN` · `người chỉ DUYỆT` · `khớp đúng một dòng tiền trong sổ` · `lại khớp số chứng từ nhưng` ⇒ **0** | bài DOM `tests/web/` + bài quét | trả lại chữ cũ ở một trong bốn chỗ ⇒ **ĐỎ**; hai bản `LY_DO_LO` lệch một ký tự ⇒ **ĐỎ** |
| AC-7 ⭐ *(Chrome — `F-1`)* | **8088 sổ thật chỉ đọc**, chuột thật: băng ghi chú = chữ v4.18 với `c` = `/ro` `may − tu_chung` *(mong ≈ **120**)*; mở *Số liệu kiểm chứng* ⇒ `note ok` = chữ v4.18 *(`t` ≈ **64**)*, hàng `may` = chữ ⓓ; bấm `Xem <c> dòng` ⇒ nhãn `… · chỉ CHƯA NHẬN THEO LÔ`, số hàng lưới = `c`. **8099** kho TEST cùng bốn chuỗi. Console **0** | Chrome CDP | — |
| AC-8 *(c · một tập)* | ⓘ hằng có **30** ký tự = `{c : c.isspace()}` ∪ `{U+FEFF}` *(so tập)*; ⓘⓘ với **mỗi** ký tự `x` trong tập: `ma_tien_te(x+'vnd'+x) == 'VND'`; PG **kho TEST** `upper(btrim(x‖'vnd'‖x, <tham số hằng>)) = 'VND'`; JS *(node, hàm mã tiền tệ của `TP`)* `== 'VND'` — **30 / 30** ở cả ba; ⓘⓘⓘ ký tự **ngoài** tập `U+200B` ⇒ cả ba **giữ nguyên** *(⛔ gỡ)*; ⓘⓥ tập JS đọc từ nguồn **=** tập Python. `pytest --runxfail …::test_F2_ca_bien_*` ⇒ passed | bài đơn vị + bài PG + bài node | SQL giữ `E' \t\r\n'` ⇒ **ĐỎ** *(26 / 30)*; JS giữ `trim()` ⇒ **ĐỎ** *(U+0085 · U+001C…U+001F)*; thêm U+200B vào tập ⇒ **ĐỎ** |
| AC-9 *(c · một chỗ)* | Quét `fls/` *(ngoài chú thích, ngoài định nghĩa `ma_tien_te` + hàm JS)*: `.strip().upper()` ⇒ chỉ còn `canon/spec.py:108` *(danh sách cho phép, kèm lý do: chữ cột, ⛔ tiền tệ)*; `trim().toUpperCase()` trong `fls/web/` ⇒ **0**; `btrim(i.curr` ⇒ mọi chỗ mang tham số tập, chuỗi `E' \t\r\n'` ⇒ **0**. Bài tự chứng: chèn `(x or "").strip().upper()` vào bản sao một tệp ⇒ bắt **1** | bài quét *(mở rộng bài `AC-15` `WO-037`)* | quét chỉ hai tệp cũ ⇒ bài tự chứng **ĐỎ** |
| AC-10 *(c · đầu-cuối)* | Kho TEST qua **HTTP**: lệnh VND số tiền `X` + dòng tiền chưa nối `curr` = `U+00A0` ＋ `VND` *(NBSP ở mép — viết bằng tên điểm mã, đính chính `KQ-046 F-2`; ⛔ mã khớp)* số tiền `X` ⇒ `itl-candidates` có dòng ấy bậc `tien`, `tong_cung_tien_te` đếm nó; lệnh `curr` = `U+FEFF` ＋ `VND` *(BOM ở mép — viết bằng tên điểm mã)* có mã khớp một dòng `VND` ⇒ rổ `may` *(⛔ `nguoi` khác tiền tệ)*; cửa ghi `POST /queue/{itl_id}/match` cặp ấy ⇒ ⛔ `KhacTienTe` *(tạo ca, ghi kho **TEST**)* | bài cửa `tests/api/` | một trong ba vế *(rổ · `itl-candidates` · cửa ghi)* dùng tập khác ⇒ **ĐỎ** |
| AC-11 *(sổ thật ⛔ đổi)* | **Sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, hàm thật, cùng ảnh — in `run_id`)*: `dem_theo_ro` trước = sau *(cả 6 khoá)*; `curr` chứa ký tự trong tập ở mép: `fls_itl` **0 / 8.387**, `fls_pm_line` **0 / ~276.028** *(in mẫu số — `Đ3`)* | phép đo chỉ đọc *(kịch bản trong `BG`)* | mẫu số `0` ⇒ **ĐỎ** |
| AC-12 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai + đúng **3 `XPASS(strict)`** `kq041` *(`F-2` + `F-3` ×2 — đúng ý; `fls-test` gỡ dấu)*, 3 `kq021` *(`WO-023`)* **vẫn** `xfail` · `lint-imports` **9 / 0** · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.18** `§4.5 ⓤ` *(chữ nguyên văn)* + `§4.5 ⓥ` *(hành vi)*; `BA-13` **v1.9**. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(⛔ token, ⛔ lớp CSS mới — `note warn` / `note ok` / `lbl` / `hint` đang có)*.

| Trạng thái | `F01G` `②b` danh sách *(sau `(a)`)* | `F01L` băng + bảng rổ *(sau `(b)`)* |
|---|---|---|
| tải | khung *"Đang hỏi sổ…"* — giữ tới khi lượt **mới nhất** xong; lượt cũ xong ⛔ tắt nó | ⛔ đổi *(`TT.chay`, khung chờ 3 dòng)* |
| rỗng | câu rỗng của chip **đang chọn** *(⛔ của chip trước)* | ⛔ đổi |
| lỗi | câu lỗi của lượt **mới nhất** + `Thử lại`; lỗi lượt cũ ⛔ hiện | ⛔ đổi |
| mất kết nối | `FLS-MAT-KET-NOI` của lượt **mới nhất** + `Thử lại` | ⛔ đổi |
| có dữ liệu | chỉ hàng của chip đang chọn; chip in **đúng** số hàng cửa trả | ghi chú băng + `note ok` mang câu `LY_DO_LO`; nhãn lọc `chỉ CHƯA NHẬN THEO LÔ`; hàng `may` câu ⓓ |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** `fls_itl.curr` / `fls_pm_line.curr` qua cửa có sẵn. Cửa đọc `itl-candidates` đổi **tập ký tự** của phép so SQL; cửa ghi `ghep_lenh` *(`ghi_tay.py`)* đổi phép chuẩn hoá mã tiền tệ sang `ma_tien_te` — ⛔ tuyến mới, ⛔ khoá mới.
- Ghi kho THẬT: **`KHONG`**. Máy **8088** **CHỈ ĐỌC** *(chỉ `GET` cho `AC-5`/`AC-7`)*. Mọi cú ghi *(dựng ca `AC-10`)* trên **kho TEST** qua máy **8099** / bài thử.
- Số dòng sổ thật đổi *(đã đếm — `fls-ba` 05/10)*: `(a)` **0** dòng sổ — đổi **số in** trên chip khi đổi chip lúc đang tải *(`KQ-041`: `2955 → 2219`, `1472 → 736`)*; `(b)` **4** chuỗi chữ in, số ⛔ đổi; `(c)` **0 / 8.387** dòng `fls_itl`, **0 / 276.028** dòng `fls_pm_line` ⇒ ⛔ rổ nào, ⛔ bậc nào đổi. ⇒ Báo động hiếm: ⛔ áp — ⛔ cảnh báo mới.

## Nền khi nhận *(`fls-ba` đo / chép 05/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — commit giấy `fls-ba` phát phiếu này *(sau `116ba93` `KQ-041`)*; mã `fls/**` cuối = `3c13ce3` *(`WO-037` vòng 2)* | `git log` |
| `pytest` | **`2268 passed, 6 xfailed`** *(`KQ-041` đo cuối lượt; 6 = 3 `kq021` của `WO-023` + 3 `kq041` của phiếu này)* ⇒ sau phiếu: 3 `kq041` thành `XPASS(strict)`, 3 `kq021` **vẫn** `xfail` | `KQ-041` bảng cổng |
| `kiem_so_song` | **50** *(`fls-ba` chạy 05/10 trước tờ giấy này: `⛔ CONG SO SONG KHONG DAT — 50 lech/khong-do-duoc` — = `KQ-041`: nền 49 ＋ 1 chân trang bản vẽ theo đồng hồ)*; sau tờ giấy — nhật ký §5 | lệnh |
| version spec | `BA-06` **v4.18** · `BA-07` **v3.11** · `BA-13` **v1.9** | header tệp |
| sổ thật | `dem_theo_ro` *(ảnh `NAP-2026-10-02-PMA07ED283`, `KQ-041`)*: `may` **184** · `nguoi` **616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601** · `nguoi_khac_tien_te` **84**; `may − tu_chung` **120** *(lệch tiền 78 · nhiều dòng có dòng khớp 3 · một dòng khớp đúng tiền 39 = `chum_lech_tien` 25 ＋ `co_dong_chua_duyet` 14)*; chip `Đã gán` **2.219** · `Chưa gán` **736** | `KQ-041` |

## Câu còn treo
- ⛔ câu mới cho owner. `Q-FX-1` *(84 lệnh trả bằng tiền tệ khác)* và `Q-TIEN-1` vẫn treo — ⛔ chặn: phiếu này ⛔ đổi luật ghép hay luật in tiền, chỉ đổi **cách đếm** và **chữ**.
- `GAP-SCR-34` *(mới 05/10 — hàng của 120 lệnh rổ `may` ⛔ nói vì sao cửa ghi ⛔ nhận theo lô)* là việc **spec** của `fls-ba` *(khoá `vi_sao` mới cho rổ `may`, lấy từ `ds_tu_chung`)* — ⛔ chặn: câu `LY_DO_LO` của phiếu này nói đúng cho **cả nhóm**, hàng nào cũng ⛔ bị nói sai.

## Rủi ro
1. **Nhập vòng / hợp đồng nhập** *(`(c)`)*: `ma_tien_te` hôm nay ở `fls/repo/man_ghep.py`; `pm_join.py` *(`fls/adapters/`)* gọi nó có thể phá `lint-imports` 9/0 ⇒ chỗ đặt hằng + hàm là việc Dev, cổng là `lint-imports` **9 / 0**; vướng ⇒ `HOI`, bàn giao `(a)` + `(b)` trước.
2. **Tái hiện `F-3` phụ thuộc thời gian** — bài thử và Chrome dựng độ trễ **có kiểm soát** *(cửa giả chậm / CDP `Fetch` giữ phản hồi)*; ⛔ một bài *"bấm nhanh rồi mong"* — nó xanh vì may.
3. **Bài cũ ghim chữ v4.17** *(`test_wo037_v2_bang_f01l_cua_that.py:44`)* sẽ đỏ đúng lúc ⇒ đổi sang so với hằng / chữ v4.18 *(`tests/web/` — Dev sở hữu)*; ⛔ sửa `tests/nghiem_thu/**`.

## Đính chính `TL-043` *(2026-10-05, `fls-ba` — ⛔ viết lại dòng trên; đọc các dòng ấy theo bảng này)*
| Chỗ | Viết ở trên | Đọc là | Vì sao |
|---|---|---|---|
| `AC-1` · `AC-2` · `AC-8` cột *Mong* | *"`pytest --runxfail tests/nghiem_thu/test_kq041_*::… ⇒ passed`"* | bài `kq041` **do `fls-test` viết lại** tương ứng ⇒ passed trên `db0adae`; **đỏ đúng lý do** trên `77737f7` | ba gác cũ ⛔ thể qua dưới mã đúng spec: `goi >= 4` đòi điều `ⓥ` ② cấm · `goi >= 3` đòi lượt bị thay xin tiếp *(`BA-06` v4.19 `ⓥ` ①: **được** dừng ngay)* · `F2` so với SQL **của chính bài** |
| `AC-12` | *"đúng **3 `XPASS(strict)`** `kq041`"* | ở `BG-044`: **6 `xfailed`** là đúng nền; ở `KQ`: ba bài viết lại **xanh**, ⛔ còn dấu `xfail`; 3 `kq021` vẫn `xfail` | như trên |
| Phạm vi TRONG `(e)` | *"`fls-test` gỡ ở `KQ` — 3 bài `kq041` sẽ `XPASS(strict)` đúng ý"* | `fls-test` **viết lại** ba bài ở `KQ`, giữ lo gốc *(bảng `TL-043`)* | như trên |
| `AC-3` · bảng *Màn hình* hàng *lỗi* / *mất kết nối* | *"câu lỗi … + `Thử lại`"* | câu lỗi **như cũ** *(`banner crit`)*; thử lại = bấm lại chip đang chọn khi ⛔ đang tải | `②b` **⛔ bao giờ** có nút `Thử lại` *(grep `man_f01_ghep.js` **0**)* — lỗi viết phiếu. Nút mới ⇒ `BA-06` v4.19 `ⓥ` ⑤ ⇒ **`WO-045` `(e)`** |
| Phạm vi NGOÀI `(a)` | *"⛔ đổi `F01L` `_loc` (chưa đo có cùng lỗi — xem `(d)`)"* | `(d)` đã thấy cùng lỗi *(#6)* ⇒ **`WO-045`** ② | `BG-044` `(d)` |
| ⭐ `AC-10` cột *Mong* *(đính chính `KQ-046 F-2`, `fls-ba` 05/10)* | hai chuỗi `curr` mang **ký tự thật** `U+00A0` *(NBSP)* và `U+FEFF` *(BOM)* — trên màn đọc thành một dấu cách và **không gì cả** ⇒ người đọc thấy *"lệnh `curr = 'VND'`"*, sai nghĩa | `curr` = `U+00A0` ＋ `VND` *(dòng tiền)* · `curr` = `U+FEFF` ＋ `VND` *(lệnh)* — **đã thay tại chỗ** bằng tên điểm mã; nghĩa ⛔ đổi *(`AC-10` vẫn đo đúng hai ca ấy — `KQ-046` `AC-10` ✅)* | lỗi soạn của `fls-ba`: dán chuỗi đo vào phiếu mà ⛔ viết bằng tên. Quét `docs/` 05/10 *(**177** tệp `.md`/`.html`/`.json`/`.mmd`/`.css`/`.js`/`.py`…, bộ **96** điểm mã vô hình / điều khiển: mọi C0 trừ `\t\n\r` · C1 `U+007F`…`U+009F` · `U+00A0` · `U+00AD` · `U+1680` · `U+180E` · `U+2000`…`U+200D` · `U+2028`/`9` · `U+202A`…`U+202F` · `U+205F` · `U+2060` · `U+2066`…`U+2069` · `U+3000` · `U+FEFF`)* ⇒ **8** ký tự trong **3** tệp; lỗi soạn **chỉ** chỗ này *(2 ký tự)*; 6 ký tự khác ở `KQ-041:65` · `KQ-046:80,85` là **chuỗi đo dán nguyên văn** của `fls-test` *(cố ý — biên bản, chủ tệp `fls-test`, ⛔ `fls-ba` sửa)* |

## Nghiệm thu PO *(`fls-ba` · 2026-10-05 — đọc `KQ-046` 12/12)*

Đối chiếu **ý owner** *(⛔ chỉ AC)*: phiếu này phải làm cho **con số trên chip là con số cửa trả** — kế toán đổi chip lúc danh sách đang tải *(thao tác thường)* ⛔ còn thấy sổ phồng gấp rưỡi; câu của `F01L` ⛔ hứa điều sổ ⛔ đúng; và mọi phép so tiền tệ dùng **một** luật ký tự.

| Ý owner / spec | Lời gốc | Đo được *(`KQ-046`)* | Khớp |
|---|---|---|:-:|
| ⭐ Chip in **đúng** số cửa trả — ⛔ trộn hai rổ *(`B5` — chip là thứ kế toán bấm **đầu tiên** ở `②b`)* | `BA-06` v4.18 `§4.5 ⓥ` ①…④ · `QĐ-ITL-27` | 8088 sổ thật, Chrome **có cửa sổ** chuột thật, đối chứng **cùng máy**: `Đã gán` **2955 → 2219** = Σ 5 trang cửa · bấm lại `Chưa gán` **1472 → 736** = 500 ＋ 116 ＋ 120, **3** `GET` = một lượt · đổi 3 lần **4356 → 2219**; `POST` **0** | ✅ |
| Lượt bị thay **được dừng ngay**, lỗi lượt cũ ⛔ hiện | `BA-06` v4.19 `ⓥ` đoạn v4.19 | ảnh giữa chừng `dang_tai true · n 0`; `catch` + sau vòng đều `if (!con_la_moi_nhat()) return false`; ⛔ nút `Thử lại` — đúng *"như cũ"* *(nút ⇒ `WO-045 (e)`)* | ✅ |
| Năm trạng thái `②b` giữ nguyên | `10` §3.1 *Màn hình* | tải · rỗng · lỗi · mất kết nối · có dữ liệu — Chrome 8088 `?gia_lap=`, console **0** | ✅ |
| `F01L` ⛔ hứa *"lệch tiền"* / *"chỉ DUYỆT"* | `BA-06` v4.18 `§4.5 ⓤ` | oracle đọc **thẳng** `06_SCREEN_SPEC.md` so `textContent`: 8088 + 8099 **4/4** chuỗi bằng nhau; chữ cũ trong nguồn ngoài chú thích **0** | ✅ |
| **Một** tập ký tự cho phép so tiền tệ | `BA-07` v3.11 `TAP_TRANG_TIEN_TE` | `set(TAP) == isspace ∪ {U+FEFF}`; Python · PG · JS **30/30**; `U+200B` ba vế **giữ**; hàm thật `ung_vien_itl` **8/8** ca. ⚠ **Chưa phủ hết** — chiều ngược `ung_vien_pm` *(`F-1`)* ⇒ `WO-047` | ✅ *(phần phiếu này giao)* |
| Sổ thật ⛔ đổi | `QĐ-ITL-62` · `10` §4.4 | `dem_theo_ro` cũ = mới **6/6** khoá; mép tập **0 / 8.387** · **0 / 276.028**; kho thật đầu lượt = cuối lượt | ✅ |

⇒ **`DONG`**. Ba phát hiện `NHE` xếp: `F-1` *(chiều ngược ⛔ dùng tập — kiểm kê `fls-ba` bỏ sót)* ⇒ phiếu nhỏ mới **`WO-047`** với kiểm kê **đủ** *(`BA-07` v3.12)*; `F-2` ⇒ sửa ở tờ này *(dòng Đính chính trên)*; `F-3` *(tooltip số cứng `1.345`)* ⇒ **`WO-045` ⑤** *(cùng tệp `man_f01.js` mục ③; `BA-06` v4.20 `ⓦ` ③)*.

## Changelog
- 2026-10-05 · `fls-ba` · **nghiệm thu PO** — `KQ-046` ĐẠT 12/12 ⇒ **`DONG`**; mục *Nghiệm thu PO* *(6 ý owner/spec khớp)*. Đính chính `AC-10` *(`KQ-046 F-2`)*: thay `U+00A0` / `U+FEFF` thật bằng tên điểm mã, nghĩa ⛔ đổi. `F-1` ⇒ `WO-047` · `F-3` ⇒ `WO-045` ⑤.
- 2026-10-05 · `fls-ba` · **`TL-043`**: thêm mục *Đính chính* — `AC-1`/`AC-2`/`AC-8`/`AC-12` đo bằng ba bài `kq041` **`fls-test` viết lại** *(⛔ `XPASS`)*; `AC-3` *"+ `Thử lại`"* ⇒ *"như cũ"* *(nút ⇒ `WO-045 (e)`)*; `(d)` + `Xem thêm` bị khoá ⇒ **`WO-045`**. Trạng thái giữ `CHO_TEST`.
- 2026-10-05 · `fls-ba` · phát **`WO-042`** `MO` từ nghiệm thu PO `WO-037` + xếp `KQ-041`: `F-3` `NANG` *(ngoài phạm vi `WO-037` — điều phối quyết 05/10)* ＋ `F-1` ＋ `F-2` gom một phiếu *(lý do ở **Vì sao gom**)*; spec `BA-06` **v4.18** *(`§4.5 ⓤ` v4.18 + `ⓥ` mới)* · `BA-07` **v3.11** · `BA-13` **v1.9**. Ưu tiên **CAO**, thứ tự `WO-042` → `WO-015` → `WO-023`. Thông tin `KQ-041` *(39 lệnh)* ⇒ `GAP-SCR-34` mới *(⛔ chặn)*.
