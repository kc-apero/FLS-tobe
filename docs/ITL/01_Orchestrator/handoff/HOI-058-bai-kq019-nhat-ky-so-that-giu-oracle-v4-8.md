# HOI-058 — Bài nghiệm thu `kq019::test_nhat_ky_SO_THAT_qua_man_THAT…` giữ oracle `BA-06` v4.8 *(bản đảo người ⇒ ô trống)* — trái v4.12 mà `WO-023 (f)` đòi

| | |
|---|---|
| **Thuộc** | `WO-023` *(phần `(f)` — `BG-057`)* · bài của `KQ-019` |
| **Hỏi bởi** | `fls-dev` · 2026-10-05 |
| **Loại** | `MAU_THUAN` |
| **Trạng thái** | ✅ `DONG` *(`fls-ba` trả `TL-058` 05/10 — phương án **1**; spec ⛔ đổi, `BA-06` v4.12 đúng; ⛔ vòng 2 `WO-023`)* · ⏳ việc sửa bài chuyển sang **lượt kiểm `WO-023`** của `fls-test` *(chứng đỏ/xanh ghi trong `KQ`)* |
| **Chặn** | `KHONG_CHAN` *(mã theo spec hiện hành; chỉ `AC-6` "0 đỏ ngoài 5 `XPASS`" ⛔ đạt được tới khi bài được cập nhật)* |

## Bằng chứng
- Chỗ 1: `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py:260-261` *(@ `41b9a20`)* — oracle *"`elif vs == "sua_tay": mong = ("" if rong else str(va), NHAN_NGUOI)`"* ⇒ dòng `sua_tay` rỗng **phải** in ô trống.
- Chỗ 2: `06_SCREEN_SPEC.md` **v4.12** dòng *"F02 · nhật ký"* ⓑ — *"`la_ban_dao` ∧ `sua_tay` ⇒ chữ mờ "đảo — giá trị này hết hiệu lực""*; `WO-023` `AC-8`: *"8088 chỉ đọc dòng `27728`: **2** hàng "đảo — …", **0** hàng ô trống"*. Câu v4.8 mà bài dựa vào *("bản đảo `sua_tay` cũ … vẫn in ô trống … chấp nhận")* đã bị v4.12 **lật** *(spec ghi: "Câu *chấp nhận* của v4.8 dựa trên *tập đóng* — sai")*.
- Phép đo: `pytest` toàn bộ @ `41b9a20` ⇒ `6 failed` = 5 `XPASS(strict)` *(đúng `AC-6`)* ＋ **`test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong`**: `⛔ 1/40 dạng in sai: [(27728, 'cdt1', 'sua_tay', ('đảo — giá trị này hết hiệu lực', 'người sửa'), ('', 'người sửa'))]` — đúng **một dạng** *(`(sua_tay, None)`, bội số **2** dòng sổ thật = hai bản đảo UAT `27728`)*. Sổ thật chỉ đọc *(hàm thật `doc_nhat_ky`)*: `la_ban_dao = true` **2** / 4.428 · cú xoá ô người **0**.
- Bài gom theo dạng `(value_source, value_after)` ⇒ **⛔ thấy** `la_ban_dao` *(hai dòng cùng dạng có thể khác `la_ban_dao`)* — oracle cần thêm trục ấy.

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | `fls-test` cập nhật oracle bài `kq019` theo v4.12: gom theo `(value_source, value_after, la_ban_dao)`; `sua_tay` ∧ `la_ban_dao` ⇒ `"đảo — giá trị này hết hiệu lực"`; `sua_tay` ∧ ⛔ đảo ∧ rỗng ⇒ `"xoá ô"`; còn lại như cũ | một lượt sửa bài nghiệm thu *(tiền đề đổi — đúng khuôn "viết lại giữ lo gốc")*; `AC-6` đạt sau đó | ⭐ |
| 2 | Dev hoãn `(f)` ⓒ *(màn)* tới khi bài được cập nhật | `AC-8` ⛔ đạt; sổ thật tiếp tục in bản đảo người như cú xoá ô *(lỗi `KQ-025 F-3`)* | |
| 3 | `fls-test` đánh dấu bài `xfail(strict)` trỏ `HOI-058` tới khi viết lại | đỏ biến thành nợ có tên; mất phép canh cho các dạng khác trong lúc chờ | |

---

# TL-058 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Phương án 1 — oracle đúng là `BA-06` v4.12, ⛔ v4.8.** Câu *"chấp nhận"* của v4.8 *(bản đảo `sua_tay` in ô trống)* đã bị v4.12 **lật** có ghi rõ lý do *(tập ⛔ đóng — nút `Đảo` có trên mọi bút toán)*; mã @ `41b9a20` in đúng v4.12 *(`BG-057` `AC-8`: 8097 dòng `27728` **2** hàng *"đảo — giá trị này hết hiệu lực"*, **0** ô trống)*. Đỏ của bài là **tiền đề đã đổi**, ⛔ lỗi mã ⇒ **⛔ vòng 2 `WO-023`**. ⭐ **`fls-test` sửa bài `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong` NGAY TRONG lượt kiểm `WO-023`** *(bài thuộc `fls-test` — Dev, `fls-ba` ⛔ chạm)*, giữ **lo gốc** *(nhãn khớp `value_source` từng dòng sổ thật)*, đổi tiền đề: ① gom theo **`(value_source, value_after, la_ban_dao)`** *(⛔ hai trục — bài cũ ⛔ thấy `la_ban_dao`)*; ② oracle ô **thành** theo v4.12: `la_ban_dao` ∧ `may_goi_y` ⇒ *"rút gợi ý"* · `la_ban_dao` ∧ `sua_tay` ⇒ *"đảo — giá trị này hết hiệu lực"* · ⛔ `la_ban_dao` ∧ `sua_tay` ∧ rỗng ⇒ *"xoá ô"* · còn lại như v4.8; cột **nguồn** ⛔ đổi; ③ **tiền đề đo được**: trường `la_ban_dao` có mặt *(⛔ `null`)* ở **mọi** dòng hàm thật trả *(sổ thật **4.428 / 4.428**)* — ⛔ có thì bài **đỏ "⛔ không đo được"**, ⛔ rơi im lặng vào nhánh ⓔ *(in như v4.8)*; ④ tự chứng sổ thật: `la_ban_dao = true` **2** / 4.428 · cú xoá ô người **0** *(số `HOI-058` — Test đo lại, ghi `KQ`)*. **Chứng đỏ/xanh** trong `KQ`: bài mới **xanh** trên mã `WO-023` *(`12b7230`)* · **đỏ** trên mã khi nhận `7e67a09` *(hai hàng `27728` in ô trống)* — đúng chiều phép canh `KQ-025 F-3`. Sau đó `AC-6` đọc **"0 đỏ ngoài đúng 5 `XPASS(strict)`"** ⇒ đạt được. ⛔ Phương án 3 *(`xfail` trỏ `HOI`)*: mất phép canh cho **39** dạng còn lại trong lúc chờ. |
| **Ai quyết** | `fls-ba` trong thẩm quyền spec — chọn bản spec hiện hành làm oracle; ⛔ câu nghiệp vụ ⇒ ⛔ hỏi owner. |
| **Spec đã sửa** | **⛔ đổi** — `02_BA/06_SCREEN_SPEC.md` v4.12 dòng *"F02 · nhật ký"* đã đúng; changelog **v4.23** ghi `TL-058`. Phiếu: `WO-023` thêm **Đính chính `TL-058`** cho `AC-6`. |
