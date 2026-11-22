# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `F7` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.2 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-275` · R2 `KQ-276`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 40 · F7 · `WO-273` · `BG-274`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: y như sổ chung. Sổ **chỉ THÊM**.
> Đo trên `isp/F7` @ `0202147`, cụm `5444`, Chromium thật + máy chủ thử + kho TEST; kịch bản ở scratchpad *(⛔ commit)*. Đột biến chạy trên bản sao `git archive`.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `F7-R1-01` | F7 | R1 | A2 | GHI NHẬN | `man_f08.js:_dung_vung_ban` | Thẻ *"Bản Daily Report 3"* đặt **dưới** bảng tỷ giá 37 dòng: ở khung 1100×900 người dùng phải cuộn mới thấy ô kỳ *(ảnh trước ký: thẻ chỉ lộ nửa dưới)*. Hành vi đúng, chỉ khó thấy. | BA quyết thứ tự thẻ ở `§9` field-level F7. | — | MỞ |
| `F7-R1-02` | F7 | R1 | B2 | GHI NHẬN | `man_f08.js:_hoi_ky_ban` | Hộp nêu phiên bản + checksum **chụp lúc mở**, còn tuyến ký phiên bản mới nhất **lúc POST**. Nếu engine đưa bản mới chen giữa, hộp nói bản N nhưng ký bản N+1. *(Đọc mã, **chưa đo** — kỳ vọng hiếm; `409` thì có vẽ lại.)* | Hộp nói "bản mới nhất của kỳ" hoặc tải lại trước khi mở. | — | MỞ |
| `F7-R1-03` | F7 | R1 | B1 | GHI NHẬN | `tests/web/test_isp_f08_fx.py:114` | Bài F4 đổi đếm `button` → `button.nut-ky`: nút khác lớp trên dòng CHẶN/TRÙNG/LẠC sẽ không bị đếm. Đột biến `M10` *(nút ở mọi dòng)* vẫn ĐỎ ⇒ không yếu đi với đường hiện có. | Thêm đếm tổng nút trong bảng tháng. | — | MỞ |
| `F7-R1-04` | F7 | R1 | B1 | GHI NHẬN | `BG-274` Giả định 1–3 | Nợ BA đã tự khai: kỳ nhập tay `yyyymm`; `C13-R1-05` *(§4i chưa ghi thân `{}`)*; `C13-R1-06` *(bản cũ chưa ký hiện `chưa ký` mãi)*. Màn đúng theo hiện trạng. | BA chốt ở `§9`/§4i. | — | MỞ *(backlog BA)* |
| `F7-R2-01` | F7 | R2 | B2 | **NÊN SỬA** | `man_f08.js:_hoi_ky_ban` ↔ tuyến `POST /report/snapshot/{ky}/sign` | **Nâng `F7-R1-02` từ GHI NHẬN, ĐÃ ĐO.** Kỳ 205509 *(kho TEST)*: mở hộp lúc kỳ có **2** bản ⇒ hộp nói *"Ký phiên bản 2 (checksum 80586d4503b4)"*; engine chèn bản 3 *(`f52be8f555ec`)* SAU khi hộp mở; xác nhận ⇒ **201**, kho: bản 3 `da_ky` bởi thẻ, **bản 2 vẫn `chua_ky`** *(80586d4503b4 không được ký)*. Màn sau ký vẽ lại 3 hàng, **không cảnh báo** — hộp đóng như thường. ⇒ người dùng ký bản họ **chưa xem** *(checksum khác)* mà màn ⛔ báo; niêm phong sai bản. Không phải `409`, nên đường vẽ lại ⛔ chạy. Không bài nào khoá ca này *(5 đột biến khác cắn, ⛔ đột biến "ký bản mới nhất lúc POST" vốn là hành vi hiện tại)*. | Một trong hai: (a) gửi `phien_ban`/`checksum` đã thấy trong thân và tuyến từ chối `409` khi bản mới nhất ≠ — cần BA chốt §4i; (b) tối thiểu phía màn: trước khi ký tải lại `GET` và nếu bản mới nhất ≠ `m.checksum` thì đổi nội dung hộp + ⛔ ký. Thêm bài khoá bằng đúng kịch bản trên. | Mọi hộp xác nhận ký phải **ràng bản đã nêu** với bản bị ký *(so checksum)*, ⛔ chỉ "mới nhất lúc POST". | MỞ |

## Đo R1 *(mỗi số nói nó đếm gì)*
- **F7-F1 độc lập** *(kỳ 207405, kho TEST)*: GET trước = 2 bản *(1 `da_ky` NGUOI_CU · 2 `chua_ky`)*; ký bản 2 ⇒ GET sau = cả **2/2** `da_ky`, checksum **khác** nhau, bản 1 giữ nguyên **7/7** trường *(người ký, `ky_luc`, checksum…)*; bản 2 người ký = thẻ.
- **POST** *(đếm request mạng)*: Huỷ nút + `Esc` + bấm nền ⇒ **0**; `Enter`×3 + hộp mở ⇒ **1** POST thân `{}` *(⛔ `actor`)*; `dblclick` *(bài tác giả)* ⇒ 1. Sau ký nút `Ký bản` khoá, 1 nút.
- **Đột biến** trên `git archive`: **11/11** cắn *(bỏ hộp · gửi actor · không khoá nút · ký bản cũ · nuốt 409 · POST khi huỷ · bỏ chữ 409 ngữ cảnh · bỏ trả tiêu điểm · rỗng không tên · F4 nút mọi dòng · checksum không cắt)*; bài F5 `test_isp_f08_ky_pg` xanh ở mọi đột biến không chạm F5.

## Đo R2 *(mỗi số nói nó đếm gì)*
- **Cây gộp thử** `thu/F7` = `claude/bold-galileo-zukpaf` @ `fd064b1` + `isp/F7` @ `727066e` *(⛔ commit lên nhánh nào)*; xung đột **2 tệp**: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(chỉ ghim sàn)*. Sàn gộp tay = thu thập thật: toàn bộ **4358** *(4351 nhánh làm việc + 7 bài F7)* · `tests/web` **688** *(681 + 7)*.
- **Toàn bộ** `pytest`: **4358** thu thập = 4330 pass + 12 fail + 14 error + 2 xfail; tập đỏ **26** *(12+14)* + 2 xfail = **28** — **giống hệt** 26 bài trên bản sao `git archive` của nhánh làm việc *(thêm 0 · bớt 0; nguyên nhân: kho cụm cloud rỗng, "không đo được: rổ rỗng")*; `tests/web` đỏ **3**.
- Cụm F7+F5+F4+`goi_cua_phu_het_ma_loi`+`test_kiem_thuyet_minh`: **29/29** xanh; `kiem_thuyet_minh` **35/35**.
- **Đột biến** mới trên `git archive` cây gộp thử: **5/5** cắn *(ký `ban[0]` · gửi `actor` · bỏ vẽ lại ở 409 · sàn web 688→687 · sàn toàn bộ 4358→4351)*.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `F7`, `KQ-275`)*: khởi tạo — **4** phát hiện `F7-R1-01…04` *(0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN; lớp A2 ×1 · B1 ×2 · B2 ×1)*.
- **v0.2** *(2026-11-22, `fls-test` R2 của `F7`, `KQ-276`)*: THÊM `F7-R2-01` *(nâng `F7-R1-02`, đã đo: ký bản 3 khi hộp nêu bản 2)* ⇒ **0 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN mở** *(hàng R1 giữ nguyên, sổ chỉ THÊM)* + mục *Đo R2*.
