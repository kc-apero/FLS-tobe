# WO-241 — ISP 3.1.2 · bổ sung DT9 (DT9b): đầu vào OMC · SC · PS cho cổng WP-C4c của H11

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 19/11 ~08:20 UTC |
| **Phát bởi** | orchestrator · 2026-11-19 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT9B` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT8 · DT8b · C9 IX.VEN · DT9 9 ảnh MID) |
| **Dải phiếu** | `BG-242` · `KQ-243` (R1) · `KQ-244` (R2) |

## Vì sao
- H11 (`BG-235` §2, nhánh `isp/H11` @ `4218c2a`) DỪNG: IX.VEN chỉ chứa vendor GI — OMC thiếu 12/21 vendor · SC 9/10 · PS 53/53; engine `chia_theo_cach_tinh` cần 'cách tính' của MỌI vendor. Coi vendor thiếu là `thường` = đoán.

## Orchestrator CHỐT
1. **IX.VEN = MỘT bảng có cột `so`** (`GI` · `OMC` · `SC` · `PS`) — một nguồn sự thật; dòng GI hiện có gán `so = GI` (đúng từng byte giá trị cũ), ⛔ ba bảng.
2. **Nguồn O** = Σ `pe` MID1 theo (vendor, tháng) — H11 đo khớp OMC 882/890 · SC 741/741 · PS 585/585; 8 hàng OMC `VD61` lệch ⇒ khai `lac` CÓ TÊN (⛔ lấp). Nếu sổ có tab CFA1 tương ứng (như GI PD 504) ⇒ đóng băng thêm và đối chiếu, khai kết quả (⛔ đổi nguồn O nếu chưa có quyết mới).
3. **Luật mượn RATE:** đọc `FORMULA` cột `AU` và `S:T` của MID3 ba sổ — ghi nguyên văn mẫu công thức (đếm mẫu khác nhau theo hàng) vào BG; ⛔ suy.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | ảnh `tests/fixture/cau_hinh/ix_ven.json` THÊM cột `so` + dòng OMC · SC · PS từ tab `Vendor & Network Mapping` (OMC: `Vendor & Channel Mapping`) của ba sổ DT9; mọi vendor xuất hiện ở MID3 ba sổ có dòng (đếm: OMC 21 · SC 10 · PS 53 — hoặc số đo được, khai); cột 'cách tính' đúng mã của C9/H10; dòng GI đúng từng byte | cổng `--mong` + pytest |
| AC-2 | C9 nạp IX.VEN mới vào kho (chỉ-thêm, phiên bản mới) — bài C9/H9/H10 xanh; `/config/ven` hợp đồng chỉ THÊM trường `so` | pytest + `soi_bang_tuyen.py` |
| AC-3 | BG ghi: mẫu `FORMULA` AU · S:T (đếm theo mẫu) mỗi sổ; nguồn O + 8 hàng `VD61` | BG |
| AC-4 | PII: cột vendor chỉ mã; ⛔ tên người/email; máy quét `tools/quet_pii_repo.py` (nếu đã gộp) ĐẠT | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- Khoá SA CHỈ-ĐỌC; bản thô `/tmp` (chmod 600), ⛔ commit. ⛔ sửa mã H11. ⛔ di trú mới. Ghi kho THẬT: `KHONG`.
