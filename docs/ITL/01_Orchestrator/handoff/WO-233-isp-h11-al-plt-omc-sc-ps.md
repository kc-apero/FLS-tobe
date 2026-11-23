# WO-233 — ISP 3.1.2 · Step 35 · H11: AL.PLT · OMC · SC · PS — cổng WP-C4c

| | |
|---|---|
| **Trạng thái** | `MO` — giao khi DT9 đã gộp (19/11) |
| **Phát bởi** | orchestrator · 2026-11-19 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine) · nhánh `isp/H11` |
| **Nền** | ngọn nhánh làm việc (đã gộp H9 · H10 — `fls/bao_cao/phan_bo.py`: `chia_nen_tang` · `chia_theo_cach_tinh` · `pm_tong_thang`; cổng WP-C4a/C4b; DT9 — 9 ảnh `{omc,sc,ps}_mid{1,2,3}.json`) |
| **Dải phiếu** | `BG-235` · `KQ-236` (R1) · `KQ-237` (R2) |

## Vì sao
- ISP **Step 35 · H11** (wave W12). Cùng engine H9/H10, tham số hoá theo sổ (⛔ chép mã). Mở đường H12 (AL.KEY).

## Đã đo (DT9 · `BG-221` · `KQ-222/223`) — thay chữ ISP
- Ba sổ chỉ có tháng 2025 (03/04…12); **⛔ có tháng 2026 ở sổ nào** ⇒ tiêu chí ISP "PS 7 kỳ 03–09/2026 `chua_co_dap_an`" ⛔ áp như chữ. Thay bằng: kỳ ⛔ có đáp án ở bất kỳ sổ nào ⇒ `chua_co_dap_an` CÓ TÊN (⛔ "đạt"); khai tập tháng đo được mỗi sổ.
- SC MID3: 72 hàng Σ chia ≠ O ngay ở nguồn (70 "chưa chia" Σ = 0 · 2 chia lệch thật) — `lac` ghim theo tên ⇒ cổng tách "lệch đáp án nguồn" khỏi "lệch FLS".
- OMC: cờ `nguon_nghi_loi` (lỗi `row[45]` script AS-IS; cận trên 31.150 · 5.880 · 12.600 ô MID1/2/3) ⇒ lệch ở ô có cờ tách riêng, ⛔ tính là FLS sai.
- Vế PM ba MID3: 0 ô ≠ 0 (Đ3 — khai là KẾT QUẢ).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H11-B1 · WP-C4c) | engine H9/H10 (một nguồn sự thật; ⛔ chép) chạy cho 3 sổ; cổng khớp MID3 từng sổ; mẫu số khai TRƯỚC kèm nhãn Đ4 (Vendor-tháng · ô so · ô ≠ 0 · ô ⛔ so được + lý do) mỗi sổ | `tools/do_hd2.py --goi WP-C4c` + pytest |
| AC-2 | lệch tách 3 lớp có tên: FLS (mong 0) · đáp án nguồn (`lac` SC 72) · đáp án nghi lỗi (`nguon_nghi_loi` OMC) — Đ5 hai chiều | pytest |
| AC-3 | khối `WP-C4c` trong `hd2_cong.json` có `tong_o`/`khop` (+ `lech_co_chu_dich` nếu dùng) theo hợp đồng CG2 ⇒ `/gates` `HD2_WP_C4C` hiện đúng; bài quét tệp thật của CG2 xanh | pytest |
| AC-4 | ⛔ vòng tròn: đầu vào MID1 (thượng nguồn — DT9 chứng minh 0 tham chiếu MID2/MID3) + IX.VEN; đột biến 1 ô MID1 ⇒ đúng ô MID3 tương ứng ĐỎ | pytest |
| AC-5 | grep tên vendor trong `fls/bao_cao` = 0 (Đ1) | kiến trúc |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ sửa lỗi `row[45]` của AS-IS. ⛔ di trú. Ghi kho THẬT: `KHONG`.
