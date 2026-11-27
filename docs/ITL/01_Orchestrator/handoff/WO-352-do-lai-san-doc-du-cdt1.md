# WO-352 — Đo lại sàn cổng đọc-đủ (`NGUONG_SAN`) trên nguồn sống — quyết chủ 23/11

| | |
|---|---|
| **Trạng thái** | `MO` — 23/11 ~11:30 UTC |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn DATA — phiên sửa NAP đang chạy (`session_01Ci2qSLKnx19FQtRUvjhYGj`), commit RIÊNG sau khi `--duong-nen` hiện tại xong · nhánh `claude/bold-galileo-zukpaf-isp/STG-NAP` |
| **Dải phiếu** | `BG` = mục trong `BG-335` · R = trong `KQ-337` (R2 cuối NAP). Số trống kế tiếp: **353** |

## Vì sao
- Quyết chủ 23/11 ~11:25 (TIEN_DO hàng "Quyết của chủ (~11:25)", commit `577f706`): *"CDT1 đo lại sàn"*.
- `fls/oracle/doc_du.py:96-107` — sàn đặt 2026-08-27 = **làm tròn XUỐNG hàng trăm** của số đo (3.344 → 3.300 · 3.339 → 3.300 · 2.370 → 2.300 · 430 → 400). Nguồn sống 23/11 (BG-335 §3): `T · CDT1` **3.056** < 3.300 ⇒ cổng chặn ghi sổ.
- ⚠ Chú thích mã: *"nguồn lớn dần nên số ô chỉ tăng · ⛔ ai hạ con số này để cho qua là đang tắt cổng"* — CDT1 **giảm 283 ô** (3.339 → 3.056) trong khi số dòng nguồn TĂNG (L1 10.100 → 14.265). Chủ đã quyết đo lại; BG phải ghi rõ con số giảm này để chủ thấy (⛔ che).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 | Đo 6 cột trên nguồn sống (theo HÀNG = theo CỘT); áp ĐÚNG luật cũ (làm tròn xuống hàng trăm) cho cả 6 ⇒ `NGUONG_SAN` mới; chú thích mỗi dòng: `do <số mới> (23/11) · cũ <số cũ> (27/08)` + dòng đầu khối ghi quyết chủ 23/11 | diff + BG |
| AC-2 | Cột nào số đo mới **thấp hơn** số đo 27/08 ⇒ liệt kê có tên trong BG (cột · cũ · mới · chênh), ⛔ im lặng | BG |
| AC-3 | Cổng ĐỎ hai chiều với sàn mới (nguồn giả: = sàn ⇒ ĐẠT; sàn − 1 ⇒ ĐỎ có tên cột) | pytest |
| AC-4 | Lượt live chỉ-đọc mới với sàn mới: cổng đọc-đủ ĐẠT/ĐỎ thật — dán BÁO CÁO (chỉ số đếm) vào BG-335 | BG |
| AC-5 | `--duong-nen` ĐẠT (sàn pytest = thu thập thật) | `--duong-nen` |

## Ràng buộc
- ⛔ đổi luật làm tròn; ⛔ đổi cổng khác. ⛔ ghi sheet · ⛔ ghi kho THẬT · ⛔ nội dung thật trong repo/chat.
