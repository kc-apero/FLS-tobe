# KQ-271 — R1 `WO-269` / `BG-270` *(ISP 3.1.2 · Step 41 · DT11: ảnh đáp án Daily Report 2 · 3)*

| | |
|---|---|
| **Kết quả** | **TRƯỢT** — **1 CHẶN · 3 NÊN SỬA · 3 GHI NHẬN** |
| **Phát bởi** | `fls-test` *(R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/DT11` `6ed1a29` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT11.md` |

## Đo
- **Đọc lại bằng SA** cả hai tab: DR3 13.706 ô số · DR2 26.272 ô số ⇒ **lệch 0**. DR3 tái đóng băng ra checksum **đúng ghim** `ef1744caf253f3bd`; DR2 `dong` bằng nhau, chỉ trôi 2 ô bool `Y1`·`AA1` *(`TODAY()`, sổ sống)*. Lỗi `#N/A`/`#REF!` chèn vào bản thô ⇒ cổng ĐỎ, ghi nguyên chuỗi, đếm theo cột.
- **CHECK IX.PL** đo lại độc lập: DR3 **29·14·15·163** · DR2 **315·267·48·0** — khớp BG. Ô chữ `AF87`/`AF89` = "không đo được". Dung sai hợp lý *(đạt không đổi qua 0…1000 VND; 1e-12…1e-3 mUSD)*.
- AC-3 `AH12−0.5` xác nhận ở ATL, có tên ở ảnh DR3. AC-6: ảnh cũ nguyên byte, `quet_pii_repo` 0; sàn 4.297 = số thu thập.
- Đột biến **12**: **10 cắn · 2 sống**. `--duong-nen --cong 5446` ĐẠT *(28=28, 4297 bài; web 3=3, 681)*; `lint-imports` 11 kept; `kiem_tai_lieu` ĐẠT.

## Phát hiện cần sửa
1. **`DT11-R1-01` CHẶN** — gate không tính lại `checksum`; đổi 1 ô ngoài 9 dòng CHECK ⇒ 28/28 xanh *(DR3 và DR2)*. Thêm `_checksum_lai` như `atl`/`gi`.
2. **`DT11-R1-02` NÊN SỬA (B2)** — Giả định ① **không đủ H14**: thiếu 607·608·609 *(đáp án của `H14-B2` FS1/FS2/FS3)* và 615 *(A-CCR)*; 614 đã có (`ix_fx`), 616 PDF loại trừ. Cần WO `DT11b` hoặc thu hẹp Step 46. ⛔ tự đóng băng.
3. **`DT11-R1-03` NÊN SỬA** — mọi "đạt ②" là 0=0 *(267/267 · 14/14)*; 0 kỳ cân với số ≠ 0, 63/63 kỳ có số ⛔ cân. Tách nhãn.
4. **`DT11-R1-04` NÊN SỬA** — `AK` là vết kéo công thức *(`AK5` rỗng, "Sat" = serial 0)*, ⛔ ngày 31; 155 ngày-khối = 150 + 5 `AK`; đạt chỉ-ngày-thật 262/310.
- GHI NHẬN: `-05` nhãn 13.541/18.236 · `-06` checksum DR2 trôi theo `TODAY()` · `-07` −0,5 chưa chứng minh lan vào Sign off.

Vòng sửa: Dev sửa `-01` + `-03` + `-04` *(test/nhãn)*; orchestrator quyết `-02`. Sau đó R2 cuối.
