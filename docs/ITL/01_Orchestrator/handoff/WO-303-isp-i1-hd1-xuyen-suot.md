# WO-303 — ISP 3.1.2 · Step 45 · I1: Tích hợp HD1 xuyên suốt — ảnh → ghép → cổng theo kỳ → `GET /gates` → F03

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~10:50 UTC; giao khi có ô trống (luật D ≤ 3) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/I1` |
| **Nền** | ngọn nhánh làm việc (đã gộp **H15** — `do_voi_so_luong.py` tự sinh 26 kỳ, `tu_sinh` theo kỳ trong `voi_so_luong.json`; H3 đóng theo quyết chủ 19/11; **CG1** — cổng HD1 vào `GET /gates` (`FINAL` · `HD1_THANG`); **FG** — F03 'Cổng hôm nay' hiện cổng HD1; DT1a · DT1b — nhãn lý do) |
| **Dải phiếu** | `BG-304` · `KQ-305` (R1) · `KQ-306` (R2 cuối). Số trống kế tiếp sau dải: **307** |

## Vì sao
- ISP **Step 45 · I1** (wave W15) — một trong hai bài tích hợp cuối (I1 = HD1; I2 = HD2). Phụ thuộc H15 ✅ (gộp 22/11) · H3 (đóng) · CG1 ✅ · FG ✅. Là phụ thuộc của **I2**.

## Đã đo — thay chữ ISP
- **Số kỳ = 26** (⛔ "x/23" như ISP I1-F1): H15 đo 26/26 kỳ `tu_sinh` · 0 `chua_do` · HD 12.633/12.633 · ô Final 88.339/88.431 (92 lệch có tên ở 8 kỳ: 2025-02·03·05·10·11·12 · 2026-01·07) · 2026-03 584/584 (`BG-288` · `KQ-289` · `KQ-290`).
- **Mốc sổ hai lớp** (Đ4): 25 kỳ đọc 20/11 · ảnh 2026-03 mốc cũ (đóng băng lại là câu chờ chủ `DT12-R1-05`) — mọi số in ra phải mang nhãn mốc; ISP "số là của ảnh 26/08" là lỗi thời.
- So ô qua `_chuan`, ⛔ so kiểu (`DT12-R2-02`).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (I1-B1) | `tests/tich_hop/test_hd1_xuyen_suot.py`: cổng `do_voi_so_luong.py` → `voi_so_luong.json` → `GET /gates` → cùng **số kỳ đạt** + **danh sách kỳ đỏ** ở 3 tầng; nhãn lý do DT1b có trong `ly_do`; `tu_sinh` theo kỳ đi tới `/gates` (hoặc khai rõ tầng nào ⛔ mang và vì sao) | tích hợp |
| AC-2 (I1-B2) | tệp đo vắng ⇒ `/gates` `FINAL` + `HD1_THANG` `dat = null` (⛔ `false`, ⛔ `true`); API trả theo hợp đồng CG1 (503 nếu hợp đồng nói vậy — đọc `07_API_CONTRACT`) | tích hợp lỗi |
| AC-3 (I1-F1) | F03 qua máy chủ thử (headless THẬT): thẻ `HD1_THANG` ghi đúng **x/26** như cổng | tích hợp headless |
| AC-4 (I1-F2) | đường lỗi ⇒ thẻ "KHÔNG ĐO ĐƯỢC" (⛔ xanh, ⛔ trống) | tích hợp headless |
| AC-5 | sổ lý do có chữ ký GIẢ trong bài (biên ghi rõ, ⛔ chữ ký thật — O8) ⇒ kỳ đổi xanh ở cả 3 tầng; gỡ chữ ký ⇒ đỏ lại | tích hợp |
| AC-6 | bảng AC10/AC11 theo kỳ (26 hàng, có nhãn mốc sổ) dán vào BG; toàn bộ cổng `CLAUDE.md` chạy, kết quả thật dán vào BG | BG |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` (+ `MONG_PYTEST_WEB` nếu thêm bài web) + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ chữ ký thật (O8) · ⛔ đọc kho sống (HD5 ngoài ISP) · ⛔ sửa engine H15/CG1/FG (bài tích hợp phát hiện lệch ⇒ ghi phát hiện + báo, ⛔ sửa ngầm). Ghi kho THẬT: `KHONG`.
