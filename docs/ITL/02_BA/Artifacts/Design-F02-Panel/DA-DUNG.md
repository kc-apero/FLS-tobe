# Đã dựng gì từ bộ giao thiết kế *(2026-09-04)*

**Nguồn:** `design_handoff_f02_panel` — ⚠ bộ giao nằm ở `FLS/hien_vat/`, thư mục
**gitignore** ⇒ nó **⛔ không vào git**, và người sau ⛔ **không thấy nó qua
`git log`**. Tệp này là **cầu nối duy nhất** giữa bộ giao và mã.

**Quyết định:** `QĐ-ITL-88` *(code hoá)* · `QĐ-ITL-89` *(thu hẹp `US-032`)*
**Đặc tả:** `BA-06 · §3c ⑦–⑩` · `BA-10 · DT-I11`/`DT-I12` · `BA-11 · INV-I19`

---

## ✅ Đã dựng

| Bản thiết kế đòi | Đã dựng | Ở đâu |
|---|---|---|
| Cắt ký hiệu khỏi chữ hiện ra màn *(235 → tối đa 1)* | ✅ **235 → 0**, chỉ `✓` còn lại | `man_f02.js` · cổng `tests/web/test_luat_ky_hieu_man_hinh.py` |
| Hạ nhiệt `chưa phân loại` *(76,6% sổ)* | ✅ nền nhạt chữ mờ, hết nền vàng chữ nghiêng | `hinh.css` `td.unmapped` |
| Xếp lại 7 khối theo thứ hạng | ✅ 7 ô gõ lên **đầu** · sổ gốc 38 cột xuống **cuối** | `_than_drawer` |
| Digest **dính**, thấy được khi cuộn | ✅ chín ô chứng từ **hoà tan** vào vùng ⛔ không cuộn | `_vo_panel` · `.dfixed`/`.dref` |
| Số tiền 24px · `+`/`−` · chip hướng tiền | ✅ và **cả hai vế** hiện khi cả hai khác 0 | `.dstrip .amt` |
| ⛔ Tối đa **1** bảng `KIỂM TRA` | ✅ gộp nhiều việc vào **một** bảng, mỗi việc một dòng | `_ve_phan_quyet` · `_viec_kiem` |
| Dòng trạng thái *(xong / còn việc)* | ✅ *"Việc đang chờ, không phải sự cố"* | `.tt-dong` |
| Khối Phân bổ **ba trạng thái ba hình** | ✅ `#N/A` viền đứt · rỗng chữ nghiêng · có giá trị chữ máy | `.na-o` · `.pb-rong` |
| Thẻ `--info` thay dấu 🔒 | ✅ **có chữ** *(màu ⛔ không bao giờ là thứ duy nhất chở nghĩa)* | `.the-may` |
| Nhãn lấy **từ bản khai** *(ràng buộc #12)* | ✅ digest tra `COT_DU()` | ⚠ xem *"tôi tự vấp"* |
| Tiền luôn là **chuỗi** *(#7)* | ✅ giữ nguyên `TP.tien` | — |
| `430px` là **SÀN** *(#11)* | ✅ `clamp(--panel-san, 30vw, --panel-tran)` | `.f02-wrap.split` |
| ⛔ Không mã màu mới *(#10)* | ✅ **0** token thêm | cổng `test_khong_ma_mau_go_tay.py` |

## ⚠ Đã dựng nhưng **SỬA LUẬT** — và con số là lý do

**`US-032`** *(`LE` ≠ `Pháp nhân thanh toán` thì báo đỏ)*. Bản thiết kế viết luật
là `le != le_payer`.

| Đo trên kho thật | Số |
|---|---|
| Luật như bản thiết kế viết | **1.304 dòng · 13,0%** |
| …trong đó `le` là giá trị **⛔ không bao giờ** có ở `le_payer` | **1.175 · 90%** |
| Hai cột trùng từ vựng | **44%** *(23 vs 16 giá trị, chung 12)* |
| ⭐ Luật **thu hẹp** *(cả hai thuộc từ vựng chung)* | **79 dòng · 0,8%** |

⛔⛔ **13% ⛔ không phải *"ít, hiếm và thật"*** — kế toán gặp bảng đỏ **một trên
tám dòng**, tức là ta vừa **tái tạo đúng** cái *"khó nhìn"* vừa cắt. `le` chứa
`Cash Treasury`, `CN`, `HGO1` — ⛔ **không phải mã pháp nhân**; so chúng với
`VGOH` là so **táo với cam**.

⭐ **Phần bị cắt ra ⛔ KHÔNG bị giấu:** nó xuống một dòng ghi chú ngay dưới ô
`Pháp nhân thanh toán`. *"⛔ Không bật bảng báo"* ⛔ không được biến thành *"⛔
không nói gì"* — `INV-I16`.

## ⛔ **CHƯA** dựng — và nói thẳng vì sao

| Bản thiết kế đòi | Vì sao chưa |
|---|---|
| **Khoá kỹ thuật dưới mỗi nhãn** *(`hd`, `pay_type`…)* | Đó là tên cột **trong máy**, ⛔ không phải tên trên **sheet** kế toán dùng *(`Budget Code · Final`)* ⇒ **bảy mẩu chữ nữa** cho một người ⛔ không dùng đến — **đúng lớp lỗi `DOC_NO`/`CURR`/`LE_PAYER`** vừa vá hôm qua. Việc của đợt này là **cắt** chữ. ⭐ **Chờ owner** |
| Nút **"Lưu & sang dòng sau"** | ⛔ Chưa có cửa API. `F02` ⛔ **không có nút *Xong*** — vòng việc đứt hai đầu *(`BA-06 §3c⑧`)* |
| Lưới bên trái *(toolbar · skeleton · grid 8 cột)* | Lưới hiện có **chạy đúng** và bản thiết kế chỉ đổi hình. Đã lấy **một** thứ: cột trạng thái nay là **chip tiếng Việt** thay chữ máy `UNMAPPED`/`ok` |
| Nút bề rộng panel · chip dòng mẫu | Bản thiết kế **tự khai** là *"chỉ có trong bản dựng, ⛔ không đưa vào sản phẩm"* |

## ⚠ Một thứ **MẤT**, ⛔ không giấu

Bỏ dải 8 chip là bỏ **phép NHẢY xuống nhóm**. Bù bằng **xếp lại thứ hạng** *(khối
cần đến nhất nay ở ngay dưới dòng trạng thái)* — nhưng đây là một mất **thật**.

Và với dòng **chưa** phân loại, dòng trạng thái ⛔ **không** còn nhắc *"chưa ghép
lệnh chi"*; tin ấy chỉ còn ở khối `③`.

## ⚠⚠ Bốn chỗ **tôi tự vấp** — và cái gì bắt được

| # | Vấp | Cái gì bắt |
|---|---|---|
| 1 | **Cổng luật ký hiệu bản đầu SAI**, báo **102** vi phạm: nó chỉ bỏ qua chú thích **một dòng** (`//`) nên bắt cả câu tiếng Việt nằm trong khối `/* … */` — thứ ⛔ **không bao giờ** hiện ra màn. **Suýt đi sửa chú thích** để làm xanh một phép đo sai | **Đọc lại mã** ⇒ phép che chú thích ra `tests/web/van_ban_man.py`, **một bản**, chứng minh trên **6 ca** |
| 2 | Rồi **chính cổng ấy còn lỗ thứ hai**: nó lọc theo *"có dấu tiếng Việt"* nên một mảnh như `'⛔ '` **⛔ không có chữ Việt nào** đã **lọt** — trong khi nó được nối chuỗi và hiện nguyên ra màn | **Đọc lại mã**, ⛔ không phải phép thử nào đo |
| 3 | Dựng digest xong **gõ tay** ba nhãn `Tài khoản` · `LE` · `Pháp nhân thanh toán` — **tái phạm đúng ràng buộc #12**, cái vừa bắt lỗi `DOC_NO` hôm qua. ⚠ Và lớp CSS `.dmemo` từng **tự đặt** chữ thường cho `Diễn giải` — một **nguồn sự thật thứ hai** cạnh bản khai `VAN_XUOI` | **Bộ test** *(6 bài đỏ)* |
| 4 | **Hai phép chứng-minh-đỏ của tôi sai**: một phép ⛔ **không hề** phạm tính chất nó tưởng *(đổi nhánh render mà vẫn ra đúng một bảng)*; một phép lộ ra **phép kiểm của tôi quá lỏng** — câu chữ nó tìm **cũng có** ở chân khối, nên bỏ hẳn thẻ vẫn xanh | **Chính phép chứng-minh-đỏ** ⇒ siết phép kiểm lại |

⭐⭐ **Kết:** trong bốn chỗ trên, **hai** chỗ do **đọc lại mã** mà thấy, ⛔ không
phải do một phép thử nào đo. Đó là lý do *"cổng chưa từng thấy đỏ là cổng chưa
biết có sống"* ⛔ **không đủ** — còn phải hỏi **cổng ấy có đang soi đúng chỗ hay
không**.

---

## Cổng ra

| | |
|---|---|
| Phép thử | **1024** *(+8)* · **5 đỏ có sẵn** *(đều `GAP-KHO-02`, kho test phình)* |
| Chứng-minh-đỏ | **13** phép, **tất cả đỏ thật** trước khi tin |
| Ranh giới tầng | `import-linter` **9 kept · 0 broken** *(~~8~~ — đo lại 17/09)* |
| Số sống | `tools/kiem_so_song.py` — **66 phép so**, đạt |
| Cửa | `127.0.0.1:8088` chạy mã mới, `window.FLS_LE_CHUNG` = **12 mã** |
| ⛔ **Chưa đo được** | **`B7 · UAT`** — cảm giác khi gõ · `430px` panel có đủ. **Máy ⛔ không đóng được** |
