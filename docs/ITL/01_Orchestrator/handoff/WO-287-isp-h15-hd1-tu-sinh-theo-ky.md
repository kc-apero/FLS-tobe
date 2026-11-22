# WO-287 — ISP 3.1.2 · Step 43 · H15: HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho các kỳ còn lại)

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~08:00 UTC; giao khi có ô trống (luật D ≤ 3) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **FE ↩ BE-HC** (ISP §2.1 — quyền tệp của làn BE-HC) — phiên cloud Sonnet 5.5 · medium · nhánh `isp/H15` |
| **Nền** | ngọn nhánh làm việc (đã gộp **DT12** — 25 ảnh `tests/fixture/dap_an/itl_ledge_<yyyy-mm>.json` cùng HÌNH ảnh 2026-03 + khuôn `itl_ledge_ky.py`; H3 đóng theo quyết chủ 19/11 "⛔ áp dụng ở mốc 18/11"; đường tự sinh `do_tu_sinh()` trên 2026-03) |
| **Dải phiếu** | `BG-288` · `KQ-289` (R1) · `KQ-290` (R2 cuối). Số trống kế tiếp sau dải: **291** |

## Vì sao
- ISP **Step 43 · H15** (wave W14). Mở đường **I1** (tích hợp HD1 xuyên suốt). Phụ thuộc H3 ✅ (đóng) + DT12 ✅ (gộp 22/11 `11a7f61`).

## Đã đo — thay chữ ISP (đọc `BG-266` · `KQ-267` · `KQ-268` · sổ `SO_PHAT_HIEN_ISP-3.1_DT12.md`)
- **Số kỳ = 26**, ⛔ "22 kỳ còn lại": 25 ảnh mới (`2024-10 … 2026-11`, trừ 2026-03) + ảnh 2026-03 có sẵn. 3 kỳ 2024 = 15 hàng đầu sổ `ITL#1…15` (⛔ "lạc"). 12.049 dòng ở 25 ảnh mới.
- **So ô qua `_chuan`, ⛔ so KIỂU** (`DT12-R2-02`): ô `svc_*` ở ảnh mới 100 % số, ảnh 2026-03 ≈ 68 % chuỗi chữ-số; `_chuan` đưa cả hai về cùng chuỗi (361.470/361.470 ô). Mọi phép so ô của H15 phải đi qua `_chuan` (đường của `do_tu_sinh`); ⛔ `==` thô / `isinstance(str)`.
- **Ảnh 2026-03 chụp sổ CŨ**, lệch sổ hiện tại 6.294/16.184 ô (`DT12-R1-05`) — đóng băng lại là **câu đang chờ chủ** (khuyến nghị: có). Trong bước này: GIỮ ảnh 2026-03 cũ cho hồi quy H15-B2 (584/584); khai trong BG mốc sổ của từng kỳ (25 kỳ đọc 20/11 · 2026-03 đọc mốc cũ), ⛔ trộn hai mốc vào một con số tổng không nhãn (Đ4).
- `#N/A ()` 119 ô / 25 kỳ (91 % ở 2026-09…11) — giữ nguyên chuỗi, đếm theo kỳ.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H15-B1) | `tools/do_voi_so_luong.py` lặp `do_tu_sinh()` theo **mọi kỳ có ảnh** (26) ⇒ `voi_so_luong.json` có `tu_sinh` theo kỳ: mỗi kỳ số HD đo · khớp · lệch (lệch theo lớp có tên); kỳ ⛔ có ảnh / ảnh hỏng ⇒ `chua_do` CÓ TÊN (⛔ "đạt"); DT12 cho 0 kỳ ⇒ ĐỎ có tên (Đ3) | cổng + pytest |
| AC-2 (H15-B2) | kỳ 2026-03: HD **584/584** giữ nguyên (hồi quy, so với kết quả trước bước) | hồi quy |
| AC-3 | `MONG` theo kỳ khai SAU lần đo đầu (Đ5 hai chiều: sửa được 1 kỳ cũng ĐỎ, buộc ghi lại bản khai); phép ⛔ đo được ⇒ ĐỎ | pytest |
| AC-4 | mọi phép so ô qua `_chuan` — bài đột biến: đổi 1 ô `svc_*` của 1 ảnh mới từ số sang chuỗi cùng giá trị ⇒ kết quả **không đổi**; đổi giá trị ⇒ đúng kỳ ấy ĐỎ | pytest |
| AC-5 | đọc `fls/oracle/tu_soi.py` (chỉ đọc, ⛔ sửa ngoài phạm vi); ⛔ sửa lệch MID tự sinh (ISP loại trừ — 4.020/4.088 ở 2026-03 là lớp riêng) | review |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ sửa ảnh DT12 / ảnh 2026-03. ⛔ đọc sheet (ảnh đã đóng băng). Ghi kho THẬT: `KHONG`.
- `quet_pii_repo` = 0. Lệch theo lớp + số đếm kèm nhãn (Đ4) trong BG.
