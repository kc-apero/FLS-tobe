# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `F7` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-275`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 40 · F7 · `WO-273` · `BG-274`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: y như sổ chung. Sổ **chỉ THÊM**.
> Đo trên `isp/F7` @ `0202147`, cụm `5444`, Chromium thật + máy chủ thử + kho TEST; kịch bản ở scratchpad *(⛔ commit)*. Đột biến chạy trên bản sao `git archive`.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `F7-R1-01` | F7 | R1 | A2 | GHI NHẬN | `man_f08.js:_dung_vung_ban` | Thẻ *"Bản Daily Report 3"* đặt **dưới** bảng tỷ giá 37 dòng: ở khung 1100×900 người dùng phải cuộn mới thấy ô kỳ *(ảnh trước ký: thẻ chỉ lộ nửa dưới)*. Hành vi đúng, chỉ khó thấy. | BA quyết thứ tự thẻ ở `§9` field-level F7. | — | MỞ |
| `F7-R1-02` | F7 | R1 | B2 | GHI NHẬN | `man_f08.js:_hoi_ky_ban` | Hộp nêu phiên bản + checksum **chụp lúc mở**, còn tuyến ký phiên bản mới nhất **lúc POST**. Nếu engine đưa bản mới chen giữa, hộp nói bản N nhưng ký bản N+1. *(Đọc mã, **chưa đo** — kỳ vọng hiếm; `409` thì có vẽ lại.)* | Hộp nói "bản mới nhất của kỳ" hoặc tải lại trước khi mở. | — | MỞ |
| `F7-R1-03` | F7 | R1 | B1 | GHI NHẬN | `tests/web/test_isp_f08_fx.py:114` | Bài F4 đổi đếm `button` → `button.nut-ky`: nút khác lớp trên dòng CHẶN/TRÙNG/LẠC sẽ không bị đếm. Đột biến `M10` *(nút ở mọi dòng)* vẫn ĐỎ ⇒ không yếu đi với đường hiện có. | Thêm đếm tổng nút trong bảng tháng. | — | MỞ |
| `F7-R1-04` | F7 | R1 | B1 | GHI NHẬN | `BG-274` Giả định 1–3 | Nợ BA đã tự khai: kỳ nhập tay `yyyymm`; `C13-R1-05` *(§4i chưa ghi thân `{}`)*; `C13-R1-06` *(bản cũ chưa ký hiện `chưa ký` mãi)*. Màn đúng theo hiện trạng. | BA chốt ở `§9`/§4i. | — | MỞ *(backlog BA)* |

## Đo R1 *(mỗi số nói nó đếm gì)*
- **F7-F1 độc lập** *(kỳ 207405, kho TEST)*: GET trước = 2 bản *(1 `da_ky` NGUOI_CU · 2 `chua_ky`)*; ký bản 2 ⇒ GET sau = cả **2/2** `da_ky`, checksum **khác** nhau, bản 1 giữ nguyên **7/7** trường *(người ký, `ky_luc`, checksum…)*; bản 2 người ký = thẻ.
- **POST** *(đếm request mạng)*: Huỷ nút + `Esc` + bấm nền ⇒ **0**; `Enter`×3 + hộp mở ⇒ **1** POST thân `{}` *(⛔ `actor`)*; `dblclick` *(bài tác giả)* ⇒ 1. Sau ký nút `Ký bản` khoá, 1 nút.
- **Đột biến** trên `git archive`: **11/11** cắn *(bỏ hộp · gửi actor · không khoá nút · ký bản cũ · nuốt 409 · POST khi huỷ · bỏ chữ 409 ngữ cảnh · bỏ trả tiêu điểm · rỗng không tên · F4 nút mọi dòng · checksum không cắt)*; bài F5 `test_isp_f08_ky_pg` xanh ở mọi đột biến không chạm F5.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `F7`, `KQ-275`)*: khởi tạo — **4** phát hiện `F7-R1-01…04` *(0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN; lớp A2 ×1 · B1 ×2 · B2 ×1)*.
