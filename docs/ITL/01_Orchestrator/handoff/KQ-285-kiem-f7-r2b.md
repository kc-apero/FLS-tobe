# KQ-285 — R2b NHẸ kiểm `F7` · ISP Step 40 *(SCR-F08 ký bản Daily Report 3)* · sau `KQ-276`

**Kết luận: **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới** *(tổng 5 GHI NHẬN mở)*** *(sổ `04_Test/review/SO_PHAT_HIEN_ISP-3.1_F7.md` v0.3)*. Chỉ soát vòng sửa `F7-R2-01` + cây gộp thử; phần R1/R2 đã ĐẠT ⛔ soát lại. Đo trên **cây gộp thử** `thu/F7` = `claude/bold-galileo-zukpaf` @ `773ae68` + `isp/F7` @ `618358a` *(⛔ commit)*, cụm `5444`, Chromium + máy chủ thử + kho TEST.

## Vòng sửa `F7-R2-01` — tái lập độc lập *(script riêng ở scratchpad, ⛔ commit; mỗi số = số request `POST` ở trình duyệt)*
| Kịch bản | POST | Hộp | Kho sau |
|---|---|---|---|
| Bản 3 chèn sau mở hộp, xác nhận lần 1 | **0** | nêu *bản 3* + `Đã có phiên bản mới hơn — kiểm lại trước khi ký` · 3 hàng | — |
| …xác nhận lần 2 | **1** `{}` | đóng | `[da_ky, chua_ky, da_ky]` |
| Bản 4 chèn SAU khi hộp vẽ lại bản 3: lần 2 | **0** | nêu *bản 4* · 4 hàng | — |
| …lần 3 | **1** `{}` | đóng | `[da_ky, chua_ky, chua_ky, da_ky]` |
| Bản 3 bị người khác ký ngoài | **0** | chữ *"(bản mới nhất đã được ký rồi)"* | `[da_ky, chua_ky, da_ky]` |
| Lỗi mạng ở GET tải lại | **0** | chữ lỗi Việt | `[da_ky, chua_ky]` |
| Ca thường + `dblclick` | **1** `{}` | đóng | `[da_ky, da_ky]` |
| Huỷ · Esc | **0** · **0** | đóng | không đổi |
- F5 *(`test_isp_f08_ky_pg`)* + F4 *(`f08_fx`)* + F7: **20/20** xanh. Thân POST vẫn `{}`; diff `fls/` của `isp/F7` **chỉ** `man_f08.js` ⇒ hợp đồng tuyến ⛔ đổi.
- **Đột biến** `man_f08.js`: **4/5** cắn *(bỏ GET tải lại · POST khi GET lỗi · bản mới vẫn POST · hộp lồng nêu bản cũ)*; **1 sống, tương đương** *(so `phiên bản` thay checksum: kho chỉ-THÊM ⇒ cùng phiên bản = cùng checksum)*. Trả nguyên sau mỗi lần.

## Phát hiện mới: **0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN** *(→ backlog)*
- `F7-R2b-01` *(B1)*: bài khoá ca bản 4 + ca "bản mới nhất đã ký ngoài" chưa có *(grep tệp F7 = 0)*; hành vi đúng.
- `F7-R2b-02` *(A2)*: `loi_trong_hop` cộng dồn khối lỗi *(3 lần xác nhận ⇒ 3 khối)*; hộp dùng chung, có từ trước.
- Khe ms giữa tải lại và POST: BA chốt ràng checksum ở tuyến *(`BG-274` câu hỏi 2)* ⇒ ⛔ phạm vi vòng này.

## Cây gộp thử
| Mục | Kết quả |
|---|---|
| Xung đột | **2 tệp** `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(chỉ dòng sàn + bài ghim; giữ bản nhánh làm việc rồi đặt = thu thập)* |
| Sàn *(thu thập thật cây gộp)* | toàn bộ **4459** *(4450 + 9 bài F7)* · `tests/web` **690** *(681 + 9)* |

## Cổng
- `--duong-nen --cong 5444` *(một lần, một mình, trên cây gộp thử)*: **ĐẠT** — toàn bộ tập đỏ+XFAIL **28 = 28** *(thêm 0 · bớt 0; nguyên nhân: kho cụm cloud rỗng)*, chạy **4459** ≥ 4459; `tests/web` **3 = 3**, chạy **690** ≥ 690; skipped 0 · deselected 0. Pytest toàn bộ: 12 fail + 14 error + 2 xfail = 28, 4431 pass.
- `lint-imports` **11 kept / 0 broken** · `kiem_tai_lieu` **ĐẠT** *(435 tệp · 2843 bảng)* · `kiem_thuyet_minh` **35/35**.

## Việc kế
Orchestrator gộp `isp/F7` *(sàn **4459 / 690** của cây gộp thử)*; 5 GHI NHẬN mở ⇒ backlog. ⛔ cây gộp thử chưa đẩy.
