# KQ-297 — R1 · ISP 3.1.2 · Step 29 · C10 IX.DRV

| | |
|---|---|
| Phát bởi | fls-test · 2026-11-22 · `isp/C10` = `498bf98` |
| Gửi | orchestrator |
| Về | `WO-295` · `BG-296` · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C10.md` |

## Kết luận: **ĐẠT có điều kiện** — **0 CHẶN · 2 NÊN SỬA · 4 GHI NHẬN** *(AC-1…AC-6 đều đo được xanh)*
| Mức | Mã | Ý |
|---|---|---|
| NÊN SỬA | `C10-R1-01` | `luat_pb.DRIVER` trả `PE`; kho C10 chỉ nhận `GI_PE` ⇒ `DRV_LA` — 0 chỗ nối. Việc của vòng sửa H12 *(hoặc 1 bảng nối)* |
| NÊN SỬA | `C10-R1-02` | `?ky=202603` ⇒ `200` rỗng *(21 hàng `thang:{}`, `o_thieu:[]`)* thay vì nêu tên; `driver_cua` thì ném `DRV_THIEU` 384/384 |
| GHI NHẬN | `-03…-06` | `isdigit` nhận chữ số Ả Rập · `driver_cua(conn)` đọc lại cả bảng mỗi lần (≈5,5 ms) · nạp lại cùng ảnh ⇒ bản mới `khong_doi` (đúng C5) + bản mới nhất thắng một mình · 2 bài C5 chuyển sang bảng giả |

## Số đo
- **B1** độc lập *(script riêng + SQL thô)*: mẫu số **238** ≠ 0; **238/238** khớp, thừa 0.
- **B2**: **146/146** `DRV_THIEU` có tên (`NB_LE` 96 · `GI_PE` 19 · `GI_PM` 19 · `NOEM` 12), 0 trả số; 2026 **384/384**; ô 2025 ngoài ảnh ngoài `o_thieu` = 0.
- Tuyến: 200/400/409/404 có chữ; §4i ⬜; `soi_bang_tuyen` **49** khớp. NB_LE: đường riêng `nb_le_so_dong 304`, ⛔ giả làm lưới CDT1.
- Đột biến **13/13** bị cắn. `--duong-nen --cong 5445`: **28 = 28**, chạy **4519** (≥ sàn 4519), web 3 = 3 / 690. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT.
- Dùng được cho H12: **có** nếu `doc_drv` một lần + `BangDRV.driver_cua`; cần bảng nối `PE→GI_PE` (-01).

## Việc kế
Orchestrator quyết: xử lý `-02` trong vòng sửa C10 *(nhỏ)* hay ghi backlog; `-01` đưa vào `WO` vòng sửa H12.

⚠ Ngoài phạm vi: `khop_owner.py --kiem` báo LỆCH ở `B1` · `C6` *(⛔ C10; có cả trên bản `git archive` `498bf98` ⇒ ⛔ do 2 tệp phiếu/sổ này; chưa đo trước C10)* — orchestrator xem.
