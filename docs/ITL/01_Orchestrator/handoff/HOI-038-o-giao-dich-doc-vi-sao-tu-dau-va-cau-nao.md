# HOI-038 — Ô `Giao dịch đã gán` *(câu thứ sáu)* đọc `vi_sao` từ đâu, và **câu `vi_sao` nào** được in thay *"— chưa chọn"*?

| | |
|---|---|
| **Thuộc** | [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md) `(g)` · `AC-8` |
| **Hỏi bởi** | `fls-dev` · 2026-10-02 |
| **Loại** | `MAU_THUAN` *(phiếu nói một tập, spec + phần `Dữ liệu` của chính phiếu nói tập khác)* ＋ `THIEU` *(⛔ chỗ nào nói màn lấy `vi_sao` ở đâu)* |
| **Trạng thái** | ✅ `DONG` *(`fls-ba` trả `TL-038` 02/10 — phương án **B**; phần yếu `BG-039` #1/#3/#4/#7 ⇒ `WO-037` vòng 2)* · ~~`MO` — chờ `TL-038`~~ |
| **Chặn** | `KHONG_CHAN` — `fls-dev` làm theo **phương án B** *(đề xuất dưới)* trong `BG-039`; đổi sang A hay C là **một** nhánh `if` ở `xu_ly._gd_vao_the` + một dòng JS, ⛔ đụng phần khác của phiếu |

## Bằng chứng
- **Chỗ 1 — phiếu** `WO-037` bảng TRONG `(g)`: *"`ve_o_gd` — `gd = null` ∧ `vi_sao` **có** ⇒ in câu `vi_sao` của cửa, ⛔ *"— chưa chọn"*"* ⇒ đọc nguyên văn: **mọi** câu `vi_sao` khác rỗng.
- **Chỗ 2 — spec** `BA-06` **v4.16** §4.5 *(đoạn sau *"Ô `Giao dịch đã gán` nói năm câu"*)*: *"**Câu thứ sáu:** dòng `gd = null` mang `vi_sao = ma_khop_khac_tien_te` ⇒ ô in chính câu `vi_sao` của cửa … đó là **84** lệnh sổ thật hôm nay"* ⇒ **chỉ** câu `ma_khop_khac_tien_te`. Cùng chiều: `WO-037` NGOÀI `(g)` *"⛔ đổi năm câu kia"* + mục `Dữ liệu` *"**84** lệnh `may` → `nguoi` (= 84 ô `đề xuất:` → câu `vi_sao`)"*.
- **Chỗ 3 — thiếu:** màn `F01G` vẽ bảng từ **`the`** *(`man_f01_ghep.js::the_lenh` trả `r.the`, bỏ hàng thô)*; `vi_sao` chỉ sống ở **hàng** cửa `lenh-cho`, ⛔ trong `the` *(`man_ghep.khuon_the_lenh` — 17 khoá, ⛔ `vi_sao`)*. `BA-07` v3.9 ⛔ nói `the` chở `vi_sao`; `WO-037` mục `Dữ liệu` nói *"⛔ khoá mới (ngoài một **giá trị** khoá mới `ma_khop_khac_tien_te` của `vi_sao`)"*.
- **Phép đo — sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, gọi `xu_ly.lenh_cho` mọi trang, ảnh PM `NAP-2026-10-02-PMA07ED283`, mã sau vá)*: rổ `nguoi` **616** hàng, `gd = null` **616 / 616**; câu `vi_sao`: `ma_khop_khac_tien_te` **84** *(mã tiền tệ trong câu: VND 60 · USD 21 · SGD 3)* · `khong_co_so_chung_tu` *("⛔ chưa có số chứng từ ⇒ phải tra bằng TIỀN + NGÀY")* **532**. Rổ `khong` *(chip `Không gán được`)* ô đã có câu riêng *"sổ không có số tiền này"* — ⛔ thuộc câu hỏi này.
  ⇒ Đọc theo **chỗ 1**: **616** ô đổi *(84 + 532)*; theo **chỗ 2**: **84** ô đổi. Hai tập lệch **532** ô *(33,2 % trong 1.601 lệnh chờ — ⛔ còn là báo động hiếm)*.

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| **B** | Cửa chở `the.vi_sao` **CHỈ CÓ** khi lệnh ở nhánh *"khớp mã chỉ ở tiền tệ khác"* *(`lc.la_khop_ma_chi_khac_tien_te` — đúng nhánh của `xep_ro`, ⛔ so chuỗi câu)*, **vắng** ở mọi hàng khác — cùng kiểu *"vắng mặt ở ca thường"* của `loi_nguon` / `dien_giai_vi_sao` *(`BA-07` §4h ⓵)*. JS: `!gd ∧ d.vi_sao` ⇒ in câu | ⓐ **một khoá mới trong `the`** *(`the.vi_sao`)* — trái chữ *"⛔ khoá mới"* của `WO-037` `Dữ liệu`; giá trị của nó = `vi_sao` của chính hàng *(⛔ sự thật thứ hai)*, cùng tiền lệ `the.gd` *(`xu_ly._gd_vao_the`: *"màn đọc `the`, ⛔ hàng thô"*)* · ⓑ `BA-07` phải khai khoá ấy · ⓒ **84** ô đổi — khớp `BA-06` v4.16 + `Dữ liệu` | ⭐ |
| A | Cửa chép `vi_sao` vào `the` cho **mọi** hàng `lenh-cho`; JS in khi `!gd ∧ vi_sao ∧ trang_thai ≠ khong_gan_duoc` *(nguyên văn `(g)`)* | **616** ô đổi — **532** lệnh ⛔ số chứng từ đổi *"— chưa chọn"* thành *"⛔ chưa có số chứng từ ⇒ phải tra bằng TIỀN + NGÀY"* *(câu ấy đã in ở `F01L` `hint`)*; trái `BA-06` v4.16 + NGOÀI *"⛔ đổi năm câu kia"* + con số **84** của `Dữ liệu`. Cũng là khoá mới `the.vi_sao` | |
| C | ⛔ khoá mới: JS `the_lenh` giữ `r.vi_sao` của hàng, rồi màn tự quyết *"câu nào là câu thứ sáu"* | Màn phải **nhận ra** câu `ma_khop_khac_tien_te` ⇒ so chuỗi hay chép lại điều kiện `ro = nguoi ∧ có mã` ở JS — **luật thứ hai** ở màn *(đúng thứ `BA-06 §4.5 ⓟ` cấm: *"bậc tính ở tầng cửa, ⛔ ở JS"*)*; cổng quét khoá `test_wo032_quet_khoa_cua_that.py` phải được nới để chấp `d.vi_sao` ⛔ có trong `the` | |

⚠ **Đã đo kèm** *(⛔ thuộc câu hỏi, ghi để `fls-ba` biết khi trả)*: cổng quét khoá `WO-032 AC-9` **⛔ có** đường `ro=nguoi` trong bản đồ *(`GHEP = (GHEP_MAY, GHEP_DA_GAN)`)* dù chip `Chưa gán` gọi **cả** `ro=nguoi` *(`CHIP_CUA`)* — lỗ ấy chỉ lộ khi lệnh `X` của ca `ca_wo032.py` rời rổ `may`. `BG-039` thêm đường `GHEP_NGUOI` *(`fls-dev` sở hữu `tests/web/**`)*.

---

# TL-038 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Phương án B** — giữ đúng mã `fls-dev` đã làm ở `BG-039` *(`4c3b2ae`)*: `the.vi_sao` **chỉ có mặt** khi `gd = null` ∧ `lc.la_khop_ma_chi_khac_tien_te(dòng)`; màn in khi `!gd ∧ d.vi_sao`. Tập **84** ô sổ thật, ⛔ 616. ⛔ A *(532 lệnh ⛔ số chứng từ mất *"— chưa chọn"* — câu ấy **đúng** cho cột *Giao dịch* của chúng; câu vì sao của chúng đã ở `F01L`)* · ⛔ C *(luật thứ hai ở JS — `BA-06 §4.5 ⓟ` cấm)*. ⭐ **Lỗi là của phiếu, ⛔ của Dev:** `WO-037 (g)` viết *"`vi_sao` có"* rộng hơn `BA-06` v4.16, và mục `Dữ liệu` viết *"⛔ khoá mới"* trong khi spec đòi màn in một câu mà `the` ⛔ chở — hai câu của chính `fls-ba` ⛔ đứng được cùng nhau. ⇒ **đính chính** cả hai ở `WO-037` *(dòng đính chính, ⛔ xoá chữ cũ)*. |
| **Ai quyết** | `fls-ba` trong thẩm quyền spec — **khai** một khoá cửa đọc đã chạy + **tập** ô của một câu spec đã chốt *(`BA-06` v4.16 đã nói **84**)*. ⛔ Câu nghiệp vụ: con số trên màn vẫn là `vi_sao` máy sinh, ⛔ đổi nguồn. ⛔ Hỏi owner. |
| **Spec đã sửa** | `02_BA/07_API_CONTRACT.md` **v3.9 → v3.10** — `§4h ⓵'` hàng **`the.vi_sao`** *(ở đâu · là gì · bẫy A/C)*; kèm *(từ bốn mục yếu `BG-039`)* `§4g` `lenh-cho/ro` ＋ **`nguoi_khac_tien_te`** · bảng chữ in **ba câu `VI_SAO` ⛔ ký hiệu cấm** · SQL `itl-candidates` vế sổ **`btrim`** · `02_BA/06_SCREEN_SPEC.md` **v4.16 → v4.17** — `§4.5` câu thứ sáu đọc `the.vi_sao` + **`§4.5 ⓤ`** chữ nguyên văn băng `F01L` · `02_BA/13_THUYET_MINH_MAN_HINH.md` **v1.7 → v1.8**. |

### Bốn mục yếu của `BG-039` *(ngoài câu hỏi — `fls-dev` nêu, `fls-ba` xếp cùng lượt)*

| # `BG-039` | Đo *(`fls-ba` 02/10, sổ thật **chỉ đọc**: `noi_chi_doc(dsn_that())` `read_only = on`, gọi hàm thật `dem_theo_ro` + `xep_ro` mọi trang; `dem_theo_ro` = `may` 184 · `nguoi` 616 · `khong` 801 · `tu_chung` 64 · `tong` 1.601)* | Quyết | Về đâu |
|---|---|---|---|
| **#1** thẻ rổ `nguoi` ở `F01L` *"Chưa có số chứng từ"* | `nguoi` **616** = ⛔ mã **532** ＋ `la_khop_ma_chi_khac_tien_te` **84** ⇒ câu sai **84 / 616**. ⭐ Đo kèm dòng ⚠ *"khớp số chứng từ nhưng **lệch tiền**"* *(`may − tu_chung` **120**)*: một dòng cùng tệ lệch tiền **52** · ≥ 2 dòng, mọi dòng lệch **26** · **một dòng cùng tệ KHỚP đúng tiền mà cửa ghi vẫn ⛔ nhận theo lô 39** · ≥ 2 dòng có dòng khớp tiền **3** ⇒ *"lệch tiền"* đúng **78 / 120** | Sửa — chính phiếu này làm câu sai *(84 lệnh vừa vào rổ)* ⇒ cùng phiếu. Cửa `/ro` ＋ `nguoi_khac_tien_te`; băng + bảng rổ in **hai câu** theo số cửa; dòng ghi chú ⛔ còn hứa *"lệch tiền"*. Chữ nguyên văn `BA-06` v4.17 `§4.5 ⓤ` | `WO-037` vòng 2 **`(i)`** |
| **#3** SQL bậc tiền `upper(i.curr)` ⛔ `trim` | sổ thật `curr` có khoảng trắng **0 / 8.387** · chữ thường **0 / 8.387** *(mẫu số 8.387 > 0 — `Đ3`)* ⇒ **0** ca hôm nay | Sửa — **một** luật so tiền tệ *(cùng lớp `F-1`)*, cùng tệp `lenh_cho.py` phiếu đã chạm, giá nhỏ. ⛔ vì báo động | `WO-037` vòng 2 **`(k)`** |
| **#4** câu `vi_sao` mang `⛔`, vẽ thành biểu tượng đỏ giữa câu | `lc.VI_SAO` **3 / 3** câu mang ký hiệu cấm *(1 · 1 · 2)*; cổng ký hiệu chỉ quét `man_f02.js`/`man_f04.js`, ⛔ quét chuỗi Python | Sửa — câu cửa trả để màn in theo **cùng** luật ký hiệu màn: chữ in mới ba câu *(`BA-07` v3.10)*, khoá + tập ⛔ đổi; cổng mới quét `VI_SAO` | `WO-037` vòng 2 **`(j)`** |
| **#7** quét AST so tiền tệ ⛔ phủ `lenh_cho.py` | `lenh_cho.py` hôm nay: phép so có `.upper()/.lower()/.casefold()` ngoài chú thích **0** *(grep: 2 lần chữ `strip().upper()` đều trong chú thích)* | Mở rộng bài quét sang `lenh_cho.py` ＋ ghim **0** chuỗi SQL `upper(i.curr)` trần | `WO-037` vòng 2 **`(l)`** |
| #2 *(phần sau)* · #5 · #6 | #2 dòng ⚠ ⇒ gộp vào #1 trên · #5 `AC-1` *"rổ `may`"* = hợp `tu_chung` 0 ＋ 1 — bài đo đúng **rổ**, đúng ý `AC-1` · #6 nền `kiem_so_song` đối chiếu tên `KQ-036` | ⛔ việc mới — `fls-test` soi #5/#6 khi kiểm gộp | — |

⭐ **Có vòng 2.** `WO-037` → `MO` vòng 2 *(`(i)` `(j)` `(k)` `(l)` · `AC-11`…`AC-17`)*. ⛔ **`fls-test` ⛔ kiểm `BG-039` riêng** — kiểm **gộp** `BG-039` ＋ `BG` vòng 2 trong **một** `KQ` *(như `KQ-036` gộp `BG-034`+`BG-035`)*: vòng 2 đổi chữ ba câu `vi_sao` mà `AC-8`/`AC-9` của vòng 1 so chuỗi ⇒ kiểm `BG-039` bây giờ là kiểm một bản chữ sắp đổi. Mọi `AC-1`…`AC-10` vòng 1 **vẫn** phải ĐẠT trên mã vòng 2. |
