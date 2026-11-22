# KQ-276 — R2 CUỐI kiểm `F7` · ISP Step 40 *(SCR-F08 ký bản Daily Report 3)* · sau `KQ-275`

**Kết luận: TRƯỢT — 0 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN mở** *(sổ `04_Test/review/SO_PHAT_HIEN_ISP-3.1_F7.md` v0.2)*. Đo trên **cây gộp thử** `thu/F7` = `claude/bold-galileo-zukpaf` @ `fd064b1` + `isp/F7` @ `727066e` *(⛔ commit)*, cụm `5444`, Chromium + máy chủ thử + kho TEST.

## `F7-R1-02` → **NÊN SỬA** `F7-R2-01` *(ĐÃ ĐO, không còn là đọc mã)*
Kịch bản: mở hộp ký ở kỳ 205509 *(2 bản)*, rồi engine chèn bản 3 vào kho TEST, rồi bấm xác nhận.
- Hộp nói **"Ký phiên bản 2 (checksum `80586d4503b4`)"** · POST **1** thân `{}` ⇒ `201`.
- Kho sau: bản 1 `da_ky` NGUOI_CU · **bản 2 `chua_ky`** · **bản 3 (`f52be8f555ec`) `da_ky` bởi thẻ**. Hộp đóng bình thường, màn vẽ lại 3 hàng, **⛔ cảnh báo nào**.
⇒ Ký **bản KHÁC bản người dùng thấy** mà ⛔ báo ⇒ nâng NÊN SỬA *(đúng ngưỡng orchestrator đặt)*. Không có bài khoá ca này. Sửa: ràng checksum đã nêu *(tuyến từ chối 409 nếu ≠ bản mới nhất — BA chốt §4i)* hoặc tối thiểu tải lại trước khi ký và đổi hộp nếu bản mới nhất ≠ `m.checksum`; thêm bài từ đúng kịch bản trên. → vòng sửa Dev.

## Cây gộp thử
| Mục | Kết quả |
|---|---|
| Xung đột | **2 tệp**: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(chỉ dòng sàn + chú thích sàn; gộp tay, giữ cả chuỗi lịch sử + thêm `isp/F7`)*. Mọi tệp khác gộp tự động |
| Sàn *(thu thập thật `pytest --collect-only` cây gộp)* | toàn bộ **4358** *(4351 nhánh làm việc + 7 bài F7)* · `tests/web` **688** *(681 + 7)*. Số F7 cũ 4285/688 không dùng |
| Bài trọng tâm | F7 `ky_ban_pg` + F4 `f08_fx` + F5 `f08_ky_pg` + `goi_cua_phu_het_ma_loi` + `test_kiem_thuyet_minh`: **29/29**; `tools/kiem_thuyet_minh.py` **ĐẠT 35/35** |
| `pytest` toàn bộ | 4358 = 4330 pass + 12 fail + 14 error + 2 xfail. Tập đỏ **26** *(+2 xfail = 28)* **giống hệt** 26 bài chạy trên `git archive` nhánh làm việc *(thêm 0 · bớt 0; kho cloud rỗng ⇒ bài "số thật" đỏ)*; `tests/web` đỏ **3** |
| Đột biến mới | **5/5** cắn *(ký `ban[0]` · gửi `actor` · bỏ vẽ lại ở 409 · sàn web 688→687 · sàn toàn bộ 4358→4351)* |
| `lint-imports` · `kiem_tai_lieu` | 11 kept/0 broken · ĐẠT *(429 tệp · 2827 bảng)* |

## Cổng
- `--duong-nen --cong 5444` *(một lần, một mình, trên cây gộp thử)*: **ĐẠT** — toàn bộ tập đỏ+XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4358** ≥ 4358; `tests/web` **3 = 3**, chạy **688** ≥ 688; skipped 0 · deselected 0.
- `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` khớp 48 tuyến.

## Việc kế
Vòng sửa Dev cho `F7-R2-01` *(+ bài khoá kịch bản chèn bản 3)* → R2 lại phần F7. 3 GHI NHẬN `F7-R1-01/03/04` ⇒ backlog BA/Test. Khi gộp: sàn **4358 / 688** là của cây gộp thử *(cộng thêm bài của vòng sửa)*; ⛔ cây gộp thử chưa đẩy.
