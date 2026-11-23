# HOI-033 — `AC-2` đòi *"mỗi cửa ≥1 ca bậc `ma` lệch ≠ 0"*, nhưng cửa `lenh-da-gan` ⛔ bao giờ trả bậc `ma`

| | |
|---|---|
| **Thuộc** | [`WO-032`](WO-032-so-tien-khac-tien-te-va-khuon-cua-du-truong.md) `AC-2` |
| **Hỏi bởi** | `fls-dev` · 2026-10-02 |
| **Loại** | `LECH_DU_LIEU` *(spec nói X, đo được Y)* |
| **Trạng thái** | ✅ **`DONG`** *(đã trả)* *(02/10, `fls-ba` — `TL-033` dưới: phương án **2**, `WO-032` vòng 2)* |
| **Chặn** | `KHONG_CHAN` — `WO-032` làm trọn phần còn lại; `AC-2` đo cửa `lenh-da-gan` bằng ca *"lệch ≠ 0 cùng tiền tệ"* *(bậc nào cũng được)* và **khai** chỗ lệch này trong `BG-034` |

## Bằng chứng
- Chỗ 1: `WO-032` `AC-2` cột *Mong* — *"mỗi cửa có **≥1** ca bậc `ma` lệch ≠ 0 **và** ≥1 ca khác tiền tệ"* *(bốn cửa: `itl-candidates` · `/so` · `lenh-cho` · `lenh-da-gan`)*.
- Chỗ 2 — mã: `fls/api/xu_ly.py::_bac` chỉ trả `"ma"` khi `d.get("ma_canon")` có; `ma_canon` do `lc.xep_ro` gắn *(`fls/repo/lenh_cho.py:540`)*, và `xep_ro` **chỉ** chạy trong cửa `lenh_cho` *(`xu_ly.py` hàm `lenh_cho`)* — cửa `lenh_da_gan` gọi `_gan_gd` **⛔ qua** `xep_ro` ⇒ `ma_canon` vắng ⇒ `_bac` ⛔ bao giờ ra `ma` ở cửa ấy.
- Phép đo — **sổ thật, chỉ đọc** *(`noi_chi_doc(dsn_that())`, gọi **hàm thật** `lc.doc_lenh_da_gan` + `xu_ly._gan_gd`, trang đầu `limit=500`)*: **500** hàng lệnh đã gán ⇒ **1.019** phần tử `gd`/`gd_ds` *(`gd` cũng nằm trong `gd_ds` ⇒ đếm hai lần, `Đ4`)*; **1.019 / 1.019** khớp **mã** *(`canon_ref(ref_tho) == canon_ref(doc_no)`)* — vậy mà bậc cửa trả: `tien` **896** · `cung_tien_te` **123** · `ma` **0**.
- Phép đo — kho TEST *(ca `tests/web/ca_wo032.py`, lệnh `B` khớp đúng số CT, lệch `500`)*: `lenh-da-gan` trả `gd.bac = 'cung_tien_te'`, `lech = '500.00'` *(sau `WO-032`)*.

⚠ Đây là lỗi **có từ trước** `WO-032` *(⛔ phiếu này sinh)* và **⛔ nằm trong bảng TRONG** của phiếu *(`WO-032` (d) NGOÀI: *"⛔ đổi bậc ở hai cửa ứng viên máy đề xuất"*; `_bac` của hai cửa danh sách ⛔ được nhắc)*. Hệ quả trên màn: khối *"✓ Đang gán với giao dịch"* `F01G.ve_dang_gan` in chip **`④ cùng đơn vị tiền`** cho **123** phần tử trang đầu mà thật ra là **khớp số chứng từ** — một nhãn yếu hơn sự thật.

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | Giữ mã; `fls-ba` đính chính `AC-2`: cửa `lenh-da-gan` đo bằng *"≥1 ca lệch ≠ 0 cùng tiền tệ"* *(bài `BG-034` đã đo đúng thế)* · mở phiếu riêng cho `_bac` của hai cửa danh sách | Chip khối *"Đang gán"* vẫn nói `④` cho mối nối khớp mã **tới khi** có phiếu riêng; ⛔ con số tiền nào sai | ⭐ |
| 2 | Mở rộng `WO-032`: `xu_ly.lenh_da_gan` gắn `ma_canon` *(gọi `canon_ref(ref_tho)`, ⛔ cả `xep_ro`)* trước `_gan_gd` ⇒ `gd.bac = 'ma'` cho khớp mã | Đổi **chip** người đọc thấy ở **mọi** lệnh đã gán khớp mã *(trang đầu ≥ **896 + 123** phần tử đổi ②/④ → ①)* — một thay đổi hành vi màn **ngoài** bảng TRONG, cần `fls-ba` cân và `Test` đo lại | |
| 3 | Bỏ `lenh-da-gan` khỏi yêu cầu *"bậc `ma`"* mà ⛔ ghi gì | Cổng `AC-2` khai một tập mong mà mã ⛔ thể đạt ⇒ đỏ vĩnh viễn hoặc bị nới im lặng *(`Đ5`)* | |

---

# TL-033 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Phương án 2 — sửa `_bac` ở cửa `lenh-da-gan` NGAY TRONG `WO-032`, vòng 2.** ⛔ **Không** đính chính `AC-2`: chữ `AC-2` *(mỗi cửa ≥1 ca bậc `ma` lệch ≠ 0)* **giữ nguyên**; phép đo thay thế của `BG-034` ở cửa `lenh-da-gan` *(lệch ≠ 0 cùng tiền tệ, bậc nào cũng được)* **⛔ được chấp nhận** — vòng 2 phải đo đúng chữ. Kèm hai quyết cho hai mục yếu của `BG-034` *(xem ⓑ ⓒ dưới)*. |
| **Ai quyết** | `fls-ba` · 2026-10-02 — **trong thẩm quyền spec** *(**nghĩa** một trường cửa đã trả — `bac` của `gd`/`gd_ds` — và cách màn **nói** nghĩa ký hiệu; ⛔ đổi sổ, ⛔ đổi luật xếp bậc, ⛔ đổi cửa ghi, ⛔ đổi HTTP)*. ⛔ Câu nào chờ owner. |
| **Spec đã sửa** | `02_BA/07_API_CONTRACT.md` **v3.7 → v3.8** *(`§4h ⓵'` — `bac` của `gd`/`gd_ds` so với `canon_ref(ref_tho)` của **chính dòng lệnh**, ở **cả hai** cửa danh sách · `§7` `GAP-API-11` mới)* · `02_BA/06_SCREEN_SPEC.md` **v4.14 → v4.15** *(`§4.5 ⓒ ①` — chú giải bậc **sinh từ `BAC`**, có `≠ khác tiền tệ`; hôm nay **0** chú giải trên màn)* · `02_BA/13_THUYET_MINH_MAN_HINH.md` **v1.6 → v1.7** *(`F01G ⓑ` — Toàn sổ có bậc `≠`; khối *"Đang gán"* hôm nay ⛔ bao giờ ①)* · `WO-032` **vòng 2** *(`AC-12`…`AC-15`, đính chính chữ `AC-5`)* |

### ⓐ Vì sao sửa ngay, ⛔ đính chính — số đo **toàn sổ**, ⛔ chỉ trang đầu

`fls-ba` đo lại 02/10 trên **sổ thật, chỉ đọc** *(`noi_chi_doc(dsn_that())`, `current_database() = 'fls'`; gọi **hàm thật** `lc.doc_lenh_da_gan` **mọi trang** `limit=500` + `xu_ly._gan_gd`; luật "đúng" = `canon_ref(ref_tho) == canon_ref(doc_no)` — chính phép `_bac` dùng khi có `ma_canon`)*:

| Đếm gì *(`Đ4`)* | Mẫu số | Cửa trả hôm nay | Đúng khuôn `⓵` |
|---|--:|---|---|
| **Mối nối** — phần tử `gd_ds` *(mỗi dòng tiền đã gán một lần)* | **2.262** | `tien` **2.128** · `cung_tien_te` **134** · `ma` **0** | `ma` **2.262 / 2.262** |
| **Khối *"✓ Đang gán"*** — `gd` *(một mỗi lệnh — đúng cái chip người đọc thấy)* | **2.219** lệnh | chip `② đúng số tiền` **2.121** · `④ cùng đơn vị tiền` **98** · `①` **0** | `① khớp số chứng từ` **2.219 / 2.219** |

⚠ Con số **123 / 1.019** của `HOI` đếm `gd` **và** `gd_ds` cùng lúc trên trang đầu *(một mối nối đếm hai lần — chính `HOI` đã ghi)*; con số đọc được bằng mắt là **98 / 2.219** lệnh mà chip nói `④` cho một mối nối **khớp số chứng từ**. Và **100%** chip khối *"Đang gán"* đang nói một bậc **yếu hơn** sự thật.

Ba lý do chọn sửa ngay:
1. **Nằm TRONG phạm vi `WO-032`, ⛔ ngoài.** `(c)` đòi `gd`/`gd_ds` **"đủ khuôn `⓵`"**; `BA-07 §4h ⓵'` v3.7 viết *"mỗi phần tử `gd`/`gd_ds` là **đúng khuôn `⓵`**"*, và dòng `bac` của `⓵` nói *"`canon_ref` ở **Python**"*. Một `bac` tính **thiếu** vế mã là khuôn `⓵` **sai trường** — đúng lớp lỗi `(c)` đang vá *(`khoa_to` 0 / 768 là "thiếu trường", đây là "trường có mà sai giá trị")*. Dòng NGOÀI của `(d)` — *"⛔ đổi bậc ở hai cửa **ứng viên máy đề xuất**"* — nói `itl-candidates` + `lenh-cho`, ⛔ nói cửa danh sách `lenh-da-gan`; cả hai cửa ấy **đã** chạy `xep_ro` nên bậc `ma` của chúng đúng và vòng 2 ⛔ chạm.
2. **Nhỏ.** Gắn `ma_canon = canon_ref(ref_tho)` cho từng dòng trước `_gan_gd` — đúng dòng đầu của `xep_ro` *(`lenh_cho.py:540`)*. ⛔ Một bản thứ hai của phép ấy: `WO-032` vòng 2 `(i)` đòi **một** chỗ gắn dùng chung.
3. **Mục tiêu của phiếu là màn nói đúng.** `WO-032` sinh ra vì máy nói *"trong dung sai"* sai cho **4** lệnh; để nó đóng mà khối *"Đang gán"* nói sai bậc cho **2.219 / 2.219** lệnh đã gán thì phiếu tự mâu thuẫn. Cái giá Dev nêu *(chip đổi ở mọi lệnh đã gán)* **là chính cái được sửa** — đổi ②/④ → ① là đổi một câu sai thành câu đúng, ⛔ đổi luật: thứ tự bậc `ma › tien › gan_tien › cung_tien_te` đã khai ở `BA-07 §4g ⓹` từ trước.

### ⓑ `BG-034` yếu #7 — chip `≠` ở `F01G`: **chưa đủ**, nhưng sửa bằng **chú giải**, ⛔ bằng chữ trên từng dòng

- Luật: `BA-06 §4.5 ⓒ ①` — bậc nói bằng **ký hiệu tô màu**, *"nghĩa nói **một lần** ở **chú giải** ＋ `title`"*; `§4.5 ⓒ ②` + hợp đồng thiết kế `§6.2` — *"⛔ tooltip ⛔ được là lối **duy nhất**"*.
- Đo *(`Đ1`, grep **cả** `fls/web/` lẫn `tests/web/`, 02/10)*: `tlegend` / `chu_giai` **0** chỗ; chữ *"khớp số chứng từ"* chỉ có ở `BAC` *(`man_f01_ghep.js:62`, đi vào `title`)*. Bản dựng đã duyệt **có** chú giải: `Artifacts/fls-gan-lenh-chi_10.html:739` `.tlegend` *"① khớp số CT · ② đúng số tiền · ③ gần đúng · ④ chỉ cùng đơn vị"* — **bước dựng bỏ rơi nó**. ⇒ ⛔ chỉ `≠`: **cả năm** ký hiệu `①②③④≠` hôm nay chỉ đọc được bằng **di chuột** — người đọc phải học thuộc ký hiệu hoặc rê chuột từng dòng.
- Vì sao ⛔ in chữ *"khác tiền tệ"* trên từng dòng: cột `.tg` `22px` và luật `§4.5 ⓒ ①` *(chip cùng cỡ ở mọi dòng "nhuộm hết màn")* là quyết định thiết kế đã duyệt; đổi riêng `≠` thành chữ là cho **một** bậc một luật khác bốn bậc kia. Và dòng khác tiền tệ **đã** có hai tín hiệu đọc được ⛔ cần chuột: ô `Tiền` in **kèm mã** *(`284.800,00 USD` cạnh lệnh VND — `ⓙ`)* và nhãn thanh hành động *"(khác tiền tệ — cửa ghi sẽ từ chối)"* khi chọn.
- ⇒ **Quyết:** vòng 2 `(j)` dựng **chú giải một dòng**, **sinh từ `BAC`** *(⛔ gõ tay — thêm bậc mà quên chú giải là lỗi im lặng)*, ở thanh tra cứu ứng viên như bản dựng v10. Chữ `AC-5` đính chính: *"chip dòng ấy ký hiệu `≠` ＋ `title` *khác tiền tệ* ＋ chú giải hiện chữ *khác tiền tệ*"*. Cho phép **một** lớp CSS `.tlegend` *(đã có trong bản dựng đã duyệt, chỉ dùng token có sẵn)* — ngoại lệ có tên cho dòng *"⛔ lớp CSS mới"* của `WO-032`.

### ⓒ `BG-034` yếu #3 và #8 *(người gọi gọi là #3, #7)* — xếp chỗ

| Mục | Đo | Xếp | Vì sao |
|---|---|---|---|
| **#3** — `/so` ⛔ lọc `q` trả `500` khi một dòng chưa nối có `ps_no`/`ps_co` đều `0`/rỗng *(`man_ghep.chieu_tien` ném trong khuôn của một **danh sách**)* | sổ thật **0 / 8.387** dòng `fls_itl` hai ô đều `0`/rỗng · **0 / 8.387** hai ô đều ≠ 0 *(`fls-ba` `SELECT` 02/10 — mẫu số 8.387 > 0, `Đ3`)*; kho TEST **11** *(`BG-034`)* | ⭐ **`GAP-API-11`** *(`BA-07 §7` v3.8)* — ⛔ vào `WO-032` | Có từ trước; hôm nay ⛔ chạm người dùng; và cần **một quyết hợp đồng** *(khuôn `⓵` cho một dòng ⛔ có chiều trả gì — hướng đã khai: cùng luật `tach_nguon` 23/09, một dòng hỏng ⛔ được sập trang)*, ⛔ một vá. Ưu tiên **THẤP**, nâng lên **TRƯỚC** lần nạp sao kê có dòng tiền `0` đầu tiên. |
| **#8** — `man_f04.js` `_ve_thu_tu` `la_rong: d => !d.nguon` ném `TypeError` khi `d = null` | chỉ chạy khi bấm một lần đọc; rỗng ⇒ ⛔ có gì để bấm | ⭐ **`WO-032` vòng 2 `(k)` — `AC-14`** | Cùng lớp `(e)` *"rỗng của màn vẽ được"* mà phiếu **đã** sửa ở `:894`; cùng tệp, một dòng — để lại là giữ **một** chỗ thứ ba của đúng lỗi phiếu đóng. |

### ⓓ Hệ quả cho `fls-test`
`BG-034` **⛔ kiểm riêng** — `fls-test` kiểm **gộp** `BG-034` + `BG` vòng 2 *(một `KQ`)*. `AC-1`…`AC-11` vòng 1 vẫn là đối tượng kiểm; `AC-2` ở cửa `lenh-da-gan` đo **đúng chữ**; `AC-5` theo chữ đính chính. `BA-07` đổi ⇒ rà truy vết `04_Test/03` *(dòng `§4h ⓵'` + `GAP-API-11`)*.

⇒ `HOI-033` **`DONG`** *(đã trả — việc tiếp ở [`WO-032`](WO-032-so-tien-khac-tien-te-va-khuon-cua-du-truong.md) vòng 2)*.
