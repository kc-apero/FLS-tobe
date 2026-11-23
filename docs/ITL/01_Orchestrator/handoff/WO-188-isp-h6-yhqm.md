# WO-188 — ISP 3.1.2 · Step 20 · H6: SO Y/H/Q/M theo IX.PER (cổng WP-C3b)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 — **Opus 5.5** medium (bước engine; luật A) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-HC** · cụm PG **5435** · nhánh `isp/H6` |
| **Nền** | ngọn nhánh làm việc (đã gộp H5 — `fls/bao_cao/cfa.py` + WP-C3a + ảnh `gl_cf_dau_vao.json`; C6 — IX.PER `fls/cau_hinh/ky.py` + kho; DT5 — đáp án `cfa1_yhqm.json`) |
| **Dải phiếu** | `BG-189` · `KQ-190` (R1) · `KQ-191` (R2 cuối). Số trống kế tiếp: **192** |

## Spec
ISP **Step 20** (nguồn sự thật) · AP §3.3.1 PD 410 · 411 · IX.PER · khuôn H5 (cổng `do_hd2 --goi WP-C3a`, mẫu số khai trước, lệch có tên = MONG hai chiều, dung sai có căn cứ đo, ⛔ vòng tròn).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 (H6-B1) | Daily 2 ngày T11/2024 tổng hợp ⇒ Y2024 (⛔ 2025); H/Q/M đúng | đơn vị — ĐỎ trước |
| AC-2 (H6-B2) | `do_hd2 --goi WP-C3b`: cuộn Daily (H5) theo IX.PER ⇒ so `tests/fixture/dap_an/cfa1_yhqm.json` (410: 57 cột = 3 năm × 19 Y/H/Q/M; 370 hàng) — mẫu số khai trước (kèm nhãn Đ4: ô so / ô ≠ 0), lệch có tên = MONG | cổng + pytest |
| AC-3 | bỏ tham số ngày đầu tạm của H5 — đọc IX.PER từ kho (C6); 20 mã KPI xử lý NHẤT QUÁN với H5 (loại có khai) | pytest |
| AC-4 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` MỘT lần cuối (ĐỎ ⇒ sửa + chạy lại MỘT lần; ⛔ bàn giao khi tập đỏ ≠ 28) |

## Lưu ý orchestrator
- **411** (CFA3 Daily) bị DT5 LOẠI TRỪ khỏi đóng băng (ISP Step 15) ⇒ WP-C3b chỉ so 410; khai rõ trong BG (errata nếu ISP đòi 411).
- Errata ㉑: Y/H/Q/M 57 = cột kỳ ≤ NĂM đọc (`2026M12` = 0 dòng) ⇒ kỳ chưa tới ⛔ "0 đã chốt".
- Ngày đầu IX.PER kho = 21/10/2024, trục đáp án từ 20/10/2024 ⇒ H6 quyết cách xử lý ngày 20/10 (có dữ liệu thật) — khai trong BG; ⛔ lặng lẽ bỏ.

## Dữ liệu
Ghi kho THẬT: `KHONG`. ⛔ Drive.
