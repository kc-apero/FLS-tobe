# WO-204 — ISP 3.1.2 · bổ sung DT8 (DT8b): đầu vào GI cho cổng WP-C4a của H9

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~22:15 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5445** · nhánh `isp/DT8B` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (DT8 đã gộp: `tests/fixture/dap_an/gi_mid1.json` · `gi_mid2.json` · `gi_mid3.json` · `tests/fixture/cau_hinh/ix_ven.json`) |
| **Dải phiếu** | `BG-205` · `KQ-206` (R1) · `KQ-207` (R2). Số trống kế tiếp: **208** |

## Vì sao
- H9 (`BG-201`, nhánh `isp/H9` @ `5a127c6`) dựng xong `chia_nen_tang` + KS.AL nhưng cổng **WP-C4a đo được 0/616 ô**:
  ① ảnh MID3 ⛔ có cột Vendor/tháng (DT8 loại trọn `A:N` vì PII) ⇒ ⛔ biết hàng nào thuộc Vendor-tháng nào;
  ② ⛔ có ảnh **CFA1 GI (PD 504)** ⇒ thiếu O/P theo Vendor-tháng (đầu vào RATE);
  ③ PE = 0 ở 308/308 ô MID2 của vendor thường (Đ3: tập toàn 0).
- Orchestrator chốt: bổ sung ảnh (bước dữ liệu nhỏ, ⛔ đổi ảnh DT8 đã có ngoài việc THÊM cột khoá), rồi H9 chạy lại cổng.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 | MID3: THÊM cột khoá **Vendor ID** + **tháng** (và ITL ID nếu có) từ vùng `A:N` của `'CFA2 \| MID 3 \| GI Platform Data Ledger'` — lập bản đồ cột bằng hàng tiêu đề TRƯỚC; chỉ đọc đúng các cột khoá ⛔ PII (⛔ Số CT · Diễn giải · Tài khoản · tên người). Các cột cũ đúng từng byte; khai lý do mỗi cột thêm | pytest + diff | khoá chưa có |
| AC-2 | ảnh mới `tests/fixture/dau_vao/gi_cfa1.json` (PD 504 `CFA1 \| GI Platform Data Ledger`): Vendor · tháng · No · PE · PM · ITL ID (đúng tên cột nguồn), ⛔ cột PII; số dòng theo tháng khai MONG (Đ5 hai chiều; rỗng ⇒ ĐỎ, Đ3) | cổng `dong_bang_sheet.py … --mong` + pytest | ảnh chưa có |
| AC-3 | đo và IN: số Vendor-tháng vendor thường có PE ≠ 0 / P ≠ 0 / O ≠ 0 trên ảnh mới (mẫu số cho WP-C4a, nhãn Đ4) — nếu = 0 thì ghi rõ là KẾT QUẢ (Đ3) | BG | — |
| AC-4 | PII: máy quét có ca phá; lời lỗi ⛔ in giá trị ô | pytest | — |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- Khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; sửa khuôn MID3 chỉ để THÊM cột khoá. ⛔ sửa mã H9. Ghi kho THẬT: `KHONG`.

## Câu còn treo
- không có.
