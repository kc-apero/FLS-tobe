# WO-315 — ISP 3.1.2 · Step 47 · I2: Tích hợp HD2 xuyên suốt — config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~15:35 UTC; giao theo tăng tốc ① khi H14 có R1 0 CHẶN (`KQ-313`) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** · nhánh `isp/I2` |
| **Nền** | ngọn nhánh làm việc **+ nhánh `…-isp/H13` và `…-isp/H14`** nếu chưa gộp (tăng tốc ③) · đã gộp: C1 · C5 · C7 (IX.FX ký tháng, `FX_CHAN`) · C10 (IX.DRV) · C11 (IX.ALR) · C12 (IX.PL) · C13 + C13b (IX.TMP bản ký) · CG2 (`/gates` HD2) · F5 · F7 (SCR-F08 ký tháng + ký bản) · I1 · H1…H12 |
| **Dải phiếu** | `BG-316` · `KQ-317` (R1) · `KQ-318` (R2 cuối). Số trống kế tiếp sau dải: **319** |

## Vì sao
- ISP **Step 47 · I2** (wave W17) — **Step CUỐI** của ISP 3.1.2; bài e2e HD2 đầy đủ (chủ hỏi 22/11 "test được full luồng e2e chưa").

## Đã đo — thay chữ ISP
- **Cờ phân bổ:** ISP mục 3 ghi "Loại trừ: bật cờ luật" — **đã bị THAY** bởi quyết chủ 22/11: luật IX.ALR **2025 BẬT** qua kho, ký `KhanhCQ` (`ix_alr_2025_bat.json`, H12). ⇒ I2 nạp đúng config đã ký trong kho (gồm bản bật 2025); cờ tắt chỉ là bài đồng nhất của H12.
- **`mong` từng gói đã khai ở từng bước** (I2-B1 so với chúng, ⛔ khai lại): WP-C2 (H4 …) · WP-C3a…d (H5 · H6 · H7 · H8 — C3d lệch FLS 0, AS-IS 1.791) · WP-C4a…c (H9 · H10 · H11) · WP-C5a (H12 — cờ bật: khớp 6.646/11.764; `loi_as_is` 928 · `lech_D3` 3.099 · `chua_co_dau_vao` 1.091) · WP-C5b (H13) · WP-C5c (H14). Đọc khối `hd2_cong.json` + `mong_lech_co_chu_dich` của từng gói.
- **`FX_CHAN`:** C7 — tháng chưa ký/thiếu tỷ giá CHẶN (D1); ký qua `POST /config/fx/{yyyymm}/sign` (actor từ thẻ).
- **Câu chủ đang mở** (⛔ tự quyết, ghi rõ trong BG): D3 (`lech_D3`) · CHECK IX.PL đỏ có chặn đóng sổ không.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (I2-B1) | `tests/tich_hop/test_hd2_xuyen_suot.py` (pg): nạp config vào kho test → ký tỷ giá các tháng (actor test) → chạy chuỗi CA → SO → AL → RP với `fx_cua()` THẬT → mỗi gói WP-C2…C5: **số ô so = số ô đáp án** (mẫu số in, Đ3/Đ4) và lệch = `mong` đã khai ở bước của gói (theo lớp) | tích hợp pg |
| AC-2 (I2-B2) | bỏ ký **202510** ⇒ `FX_CHAN 202510` xuyên chuỗi; ⛔ số nào ra cho tháng ấy ở mọi tầng; cổng `HD2_WP_C2` `dat = false` | tích hợp lỗi |
| AC-3 (I2-B3) | ký bản **2025-12** từ đầu ra H14 qua `dua_ban_ky` + `ky_ban` ⇒ phiên bản có checksum = checksum JSON ô | tích hợp |
| AC-4 (I2-F1) | F03 sau chuỗi đủ (máy chủ thử, headless THẬT): 4 thẻ HD2 có số; ⛔ "KHÔNG ĐO ĐƯỢC" | tích hợp headless |
| AC-5 (I2-F2) | sau bỏ ký: thẻ `HD2_WP_C2` đỏ có chữ | tích hợp headless |
| AC-6 | báo cáo HD2 theo gói (ô so · khớp · lệch theo lớp · lệch FLS) dán vào BG; toàn bộ cổng `CLAUDE.md` chạy, kết quả thật dán vào BG (đỏ-có-sẵn ghi rõ) | BG |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` (+ `MONG_PYTEST_WEB`) + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ ghi CCR/PDF · ⛔ agent · ⛔ sửa engine/tuyến (bài tích hợp lộ lệch giữa tầng ⇒ ghi phát hiện + báo). Ghi kho THẬT: `KHONG` (kho test; actor test).
- **Điều kiện MERGE của ISP (khác điều kiện xong bước):** chạy lại trên **máy owner** (`fls-pg-1`, chỉ đọc — O4) + **ThuongCT ký** (O6). Orchestrator sẽ hỏi chủ khi I2 qua R2; phiên dev ⛔ tự làm.
