# HOI-012 — `ke-toan@apero.vn` là MÁY *(AC-1)* hay NGƯỜI *(bài `KQ-002`)*? · và câu SQL cổng mốc `B` buộc phải là chuỗi THUẦN

| | |
|---|---|
| **Thuộc** | `WO-011` *(vòng 1)* |
| **Hỏi bởi** | `fls-dev` · 2026-10-02 |
| **Loại** | `MAU_THUAN` *(hai chỗ spec + bài nghiệm thu nói khác nhau)* |
| **Trạng thái** | ✅ **`DONG`** *(02/10 — `TL-012` bên dưới: chấp nhận ⭐ cả hai câu; `WO-011` ⛔ mở lại)* |
| **Chặn** | `KHONG_CHAN` — Dev làm theo phương án ⭐ của từng câu, ghi trong `BG`; `fls-ba` lật được bằng một `TL` *(đổi đúng một hằng / một câu, ⛔ đổi kiến trúc)* |

## Câu 1 — `ke-toan@apero.vn`

### Bằng chứng
- Chỗ 1: `WO-011` `AC-1` *(dòng 47)* — *"Sổ actor có **đủ 8** actor ⛔ phải người … `ke-toan@apero.vn`"*; `Dữ liệu` *(dòng 62)* — *"`tools/verify_sua_duoc_gi.py:30` `ke-toan@apero.vn`"*. ⇒ `ke-toan@apero.vn` ∈ `ACTOR_MAY` ⇒ `T2` **⛔ đếm** sự kiện của nó.
- Chỗ 2: `tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py:86` *(bài nghiệm thu — Dev ⛔ được sửa; `AC-9` đòi nó **⛔ đổi một dòng và vẫn xanh**)*:
  `assert _dem([("match", "ke-toan@apero.vn", "ghep tay tu man F01"), …]) == 1` — chiều đối chứng *"một cú bấm **NGƯỜI** thật thì cổng đếm được"*.
- Phép đo *(grep 02/10, chỉ đọc)*: `ke-toan@apero.vn` là **actor người mẫu** của **6** tệp bài ngoài `nghiem_thu/` + bài `KQ-002`; trong `fls/`+`tools/` nó có ở **2** chỗ: `tools/verify_sua_duoc_gi.py:30` *(công cụ chạy **kho TEST**, đóng vai kế toán để trả lời *"kế toán sửa được gì"*)* và `tools/demo_dong.py:697` *(một dòng chữ minh hoạ trong bản demo: cú `Xong` của **người** ghi `actor='ke-toan@apero.vn'`)*. Trên kho THẬT: **0** dòng *(`fls_queue_event` · `fls_adjustment` · `fls_journal` · `fls_chup` · `fls_khai_cot` — đếm theo actor 02/10)*. Cùng công cụ còn có `ke-toan-2@apero.vn` *(`verify_sua_duoc_gi.py:105`)* — `WO` ⛔ liệt kê, nhưng bài quét `T1` sẽ bắt nó.
- ⇒ Làm đúng `AC-1` thì bài `KQ-002 test_DOI_CHUNG…` **ĐỎ** *(`0 ≠ 1`)* ⇒ trái `AC-9`. Một chuỗi đang mang **hai nghĩa**.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | **Tách nghĩa:** công cụ `verify_sua_duoc_gi.py` đổi actor sang tên máy riêng `verify-sua-duoc-gi@fls` + `verify-sua-duoc-gi-2@fls` *(khai vào `ACTOR_MAY`)*; `ke-toan@apero.vn` giữ nghĩa **người mẫu** của bài thử, ⛔ vào sổ nào; dòng demo đổi chữ thành `actor='<email người bấm>'` *(⛔ còn một email bịa trong `tools/`)* | `ACTOR_MAY` có **9** phần tử thay **8** *(bảng `AC-1` lệch tên một dòng)*; công cụ chỉ chạy kho TEST nên ⛔ dữ liệu nào đổi; bài `KQ-002` + 6 tệp bài ⛔ đổi nghĩa | ⭐ |
| 2 | Giữ `AC-1` nguyên văn *(`ke-toan@apero.vn` ∈ `ACTOR_MAY`)*; `fls-test` sửa bài `KQ-002` sang một actor người khác | trái `AC-9`; Dev ⛔ được chạm `tests/nghiem_thu/`; 6 tệp bài của Dev phải đổi actor người mẫu; một tên **giống kế toán** bị khai là máy — đúng loại nhãn đánh lừa mà cột `actor` cấm *(`nap_nguon_va_khai.py:60` "⛔ mượn tên một người")* | |
| 3 | Khai `ke-toan@apero.vn` vào `ACTOR_DA_THAY` *(⛔ máy, đã thấy)*; ⛔ đổi công cụ | `ACTOR_DA_THAY` vốn là sổ actor **đã xuất hiện trên kho thật** — nay chứa một tên **chưa từng** xuất hiện; một ngày nó lên kho thật *(ai đó chạy công cụ sai kho)* thì được đếm là người **⛔ một tiếng báo** | |

## Câu 2 — `T2` *"⛔ gõ lại danh sách trong SQL"* vs bài nghiệm thu đọc câu SQL bằng `ast`

### Bằng chứng
- Chỗ 1: `WO-011 T2` — *"đếm sự kiện … `actor` ⛔ thuộc `ACTOR_MAY` (đủ 8, đọc từ sổ `T1` — **⛔ gõ lại danh sách trong SQL**)"*; `T4` — *"một hàm Python + **một mẩu SQL**"*.
- Chỗ 2: `tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py:52` và `test_kq010_moc_b_dem_tren_duong_ghi_that.py:57` — giá trị của khoá `su_kien_cho_nguoi` / `moi_noi_da_bo` phải là `dem(<ast.Constant>)`: **chuỗi THUẦN** trong mã nguồn *(⛔ f-string, ⛔ biến)*, và hai bài **chạy chính chuỗi ấy** trên kho thử.
- ⇒ Danh sách actor máy + mẩu UAT **buộc phải nằm nguyên văn** trong chuỗi ấy. ⛔ Có cách nào để chuỗi thuần *"đọc từ sổ"* lúc chạy mà hai bài vẫn chạy được nó *(đã thử ý dùng `current_setting(...)` — bài chạy trên phiên riêng ⇒ danh sách `NULL` ⇒ đếm `0` ⇒ `KQ-002 test_DOI_CHUNG` đỏ)*.

### Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | Chuỗi thuần **mang bản chép** danh sách + mẩu UAT, nhưng bản chép **bị máy ép bằng sổ**: `do_may()` nổ `⛔ khong do duoc` nếu chuỗi ⛔ chứa **đúng** `sql_ngoai_may('actor')` + `sql_khong_uat('reason')` sinh từ sổ *(mở rộng `_kiem_hang_may` của `WO-001`)*; một bài thử ghim cùng điều ấy | `grep` chuỗi actor trong `fls/`+`tools/` ra **2** tệp *(sổ + `kiem_so_song.py`)*, ⛔ **1** như `AC-1` viết; thêm một actor máy mà quên chuỗi ⇒ cổng **ĐỎ ngay lần chạy** *(⛔ lặng lẽ)* | ⭐ |
| 2 | `fls-test` đổi hai bài nghiệm thu để chấp nhận câu SQL **dựng** từ sổ *(gọi một hàm thay vì đọc `ast`)* | Dev ⛔ được chạm `tests/nghiem_thu/`; phải chờ `fls-test` | |

---

# TL-012 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | **Câu 1 — chấp nhận phương án ⭐1** *(tách nghĩa)*: `ke-toan@apero.vn` là **người mẫu của bài thử**, ⛔ thuộc sổ nào; công cụ `verify_sua_duoc_gi.py` mang tên máy `verify-sua-duoc-gi@fls` + `verify-sua-duoc-gi-2@fls` *(∈ `ACTOR_MAY`)* ⇒ `ACTOR_MAY` **9** phần tử *(⛔ 8)*. **Câu 2 — chấp nhận phương án ⭐1**: câu SQL cổng là chuỗi thuần **mang bản chép** danh sách máy + mẩu UAT; bản chép **bị máy ép trùng byte** với mẩu sinh từ sổ *(`_kiem_hang_may` nổ `⛔ khong do duoc` khi lệch)*. ⇒ **`WO-011` ⛔ mở lại** — đính chính câu chữ `AC-1`/`T2`/`T1`, vẫn vòng `1`, vẫn `CHO_TEST`. |
| **Ai quyết** | `fls-ba` · 2026-10-02 — trong thẩm quyền spec *(chọn cách khai một hằng / một câu chữ của phiếu, ⛔ câu nghiệp vụ, ⛔ hỏi owner)* |
| **Spec đã sửa** | [`WO-011`](WO-011-thuoc-nguoi-ban-trang-va-anh-hieu-luc.md) — `AC-1` *(`8` → **`9`**, danh sách tên, cách đo `grep`)* · `T2` *(câu *"⛔ gõ lại danh sách trong SQL"* → *"bản chép bị máy ép trùng byte"*)* · `T1` *(chuỗi `verify_sua_duoc_gi.py:30`)* · `Dữ liệu` *(chú đính chính)* · Changelog. **Đính chính bằng gạch + ⭐**, ⛔ xoá chữ cũ. ⛔ tệp `02_BA` nào đổi *(luật `09` v1.14 ⓐ…ⓔ nói *"mọi actor ⛔ phải người"*, ⛔ đếm cứng 8)*. |

### Vì sao — câu 1 *(đo 02/10, chỉ đọc)*
- **Nghĩa của luật, ⛔ nghĩa của chữ.** `AC-1` liệt kê `ke-toan@apero.vn` vì 01/10 nó là **chuỗi máy ghi** *(công cụ đóng vai kế toán)* — ⛔ vì `fls-ba` khẳng định *"tài khoản tên kế toán là máy"*. Điều `AC-1` canh là **mọi actor của công cụ/tiến trình ở một sổ**; phương án ⭐1 giữ đúng điều đó *(công cụ vẫn ∈ `ACTOR_MAY`, chỉ đổi tên)*.
- **Một công cụ ⛔ mượn tên giống người** — cùng luật `tools/nap_nguon_va_khai.py` *(chú thích cột `actor`)*. Khai `ke-toan@apero.vn` là máy *(phương án 2)* = dựng sẵn một cái bẫy cho ngày có kế toán thật đăng nhập bằng email gần giống; khai vào `ACTOR_DA_THAY` *(phương án 3)* = làm bẩn sổ *"đã thấy trên kho thật"* bằng một tên **chưa từng** thấy.
- **Kho THẬT ⛔ đổi**: `fls_queue_event` theo actor = `dung-lai-so@apero.vn` **108.128** · `may@fls` **2.219** · `khanhcq@apero.vn` **2**; `fls_adjustment` = `may@fls` **4.424** · `khanhcq@apero.vn` **4**; `fls_journal` cùng như `fls_adjustment` ⇒ **0** dòng `ke-toan*` / `verify-sua-duoc-gi*` *(đếm 02/10 sau `75d9f85`)*. Công cụ chỉ chạy kho TEST.
- Bài nghiệm thu giữ nguyên: `git diff 27c163a -- tests/nghiem_thu/` **rỗng**; chạy lại 02/10 `tests/repo/test_danh_muc_actor.py` + `test_kq002_…` + `test_kq010_…` + các bài `_kiem_hang_may` trong `tests/test_kiem_so_song.py` ⇒ **39 passed**.
- ⚠ Còn `ke-toan@apero.vn` trong **chú thích** *(⛔ hằng)* ở `fls/repo/danh_muc_actor.py:64` và `tools/verify_sua_duoc_gi.py:32` — ghi vết vì sao đổi; bài quét `T1` đọc hằng bằng `ast` nên ⛔ bắt. **Chấp nhận** — chú thích lịch sử, ⛔ giá trị chạy.

### Vì sao — câu 2
- **Ý của `T2`** là *"danh sách máy ⛔ được trôi khỏi sổ"* *(Rủi ro 2 `WO-001`: *"khai một chỗ, có bài ghim"*)*. Nguyên văn *"⛔ gõ lại"* là **cách** `fls-ba` hình dung, ⛔ là mục đích. Với hai bài nghiệm thu đọc câu bằng `ast` rồi chạy *(Dev ⛔ được sửa — `AC-9`)*, cách duy nhất còn lại là **bản chép bị máy ép**: thêm/bớt một máy ở sổ mà quên câu ⇒ `do_may()` **nổ ngay lần chạy** *(⛔ lặng lẽ)*. Hai bài ghim: `test_T2_cau_SQL_mang_DUNG_ban_sinh_tu_SO` *(cả `su_kien_cho_nguoi` lẫn `moi_noi_da_bo`, có chiều đỏ `may-moi@fls`)* + bài `WO-001` cũ.
- Phương án 2 *(`fls-test` đổi bài nghiệm thu sang gọi hàm)* tốn một vòng phiếu để đổi **hình thức**, ⛔ thêm độ an toàn nào ⇒ bỏ.
- Hệ quả câu chữ: `grep` một chuỗi actor máy trong `fls/`+`tools/` ra **2** tệp *(sổ + `tools/kiem_so_song.py`)*, ⛔ **1** — `AC-1` sửa theo.

### Việc của ai sau `TL`
- `fls-dev`: ⛔ việc gì *(đã làm đúng phương án ⭐)*.
- `fls-test`: kiểm `BG-013` theo `AC-1` **đã đính chính** *(9 tên; `grep` = sổ + `kiem_so_song.py`)*; `T2` theo câu mới — chiều đỏ: xoá một tên khỏi chuỗi SQL **hoặc** thêm một tên vào sổ ⇒ `kiem_so_song` nổ `⛔ khong do duoc`.

**Trạng thái `HOI-012`: `DONG`** *(02/10, `fls-ba`)*.
