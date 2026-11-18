# WO-200 — ISP 3.1.2 · Step 24 · H9: AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P) — cổng WP-C4a

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~21:25 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-HC** — **phiên cloud** (Opus 5.5 · medium — bước engine khó, quyết của chủ 18/11) · cụm PG **5444** của phiên ấy · nhánh `isp/H9` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp H4 · DT8 · C9 · H5 · H6 · C11) |
| **Dải phiếu** | `BG-201` · `KQ-202` (R1) · `KQ-203` (R2). Số trống kế tiếp: **204** |

## Vì sao
- ISP **Step 24 · H9** (wave W9) — nguồn sự thật duy nhất. Phụ thuộc H4 · C9 · DT8 (đều đã gộp). Khái niệm mới duy nhất: **phân bổ nền tảng theo tỷ lệ**. Mở đường H10 → H11 → H12.

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 24** (· Step 19 DT8 · Step 21 C9 · Step 28 H10 để biết ranh giới) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.4.1 PD 501–507 · §3.5.4 WP-C4 | 3.1.2 |
| `tests/fixture/cau_hinh/ix_ven.json` (DT8: 36 dòng Block 1 × 7 CDT1, cột "cách tính", 5 vendor đặc biệt VD341 · VD444 · VD428 · 'Max' · VD62) · `tests/fixture/dap_an/gi_mid1.json` · `gi_mid2.json` · `gi_mid3.json` | đầu vào + đáp án | nền |
| `fls/cau_hinh/` IX.VEN (C9, đọc từ kho) · `tools/do_hd2.py` (khuôn cổng WP-C3a/b của H5 · H6) | đường đọc + khuôn cổng | nền |
| `CLAUDE.md` | Đ1–Đ5 | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (H9-B1) | `chia_nen_tang(pe, o, p, ven)`: RATE = PE của CDT1 ÷ Σ PE các CDT1 theo Vendor-tháng; Σ chia = O (và = P) từng Vendor-tháng | `tests/bao_cao/test_phan_bo.py` | chưa có |
| AC-2 (H9-B2) | O = 0 ∧ P > 0 ⇒ chia theo tổng tháng | đơn vị | — |
| AC-3 (KS.AL) | Σ chia ≠ tiền ⇒ lỗi CÓ TÊN (Vendor · tháng · lệch); Σ PE = 0 ⇒ lỗi có tên, ⛔ chia 0 im | đơn vị | — |
| AC-4 (H9-B3 · WP-C4a) | cổng khớp MID3 GI cho vendor thường; mẫu số khai TRƯỚC kèm nhãn (Đ4: ô so / ô ≠ 0 / ô không so được + lý do); lệch khai `mong` (Đ5 hai chiều); vendor đặc biệt bỏ qua ĐẾM = **5 mã** có tên (⛔ im) | `tools/do_hd2.py` + pytest | — |
| AC-5 | ⛔ vòng tròn: đầu vào từ IX.VEN (kho) + đầu vào GI, ⛔ đọc MID3 đáp án làm đầu vào; đột biến 1 ô đầu vào ⇒ đúng các ô Vendor-tháng ấy ĐỎ | pytest | — |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- ⛔ 5 vendor đặc biệt (H10). ⛔ di trú. ⛔ đổi hợp đồng tuyến. Ghi kho THẬT: `KHONG`.
- Số CDT1 thực (AP nói 6; DT8 đo 7 cột) — đo và khai nhãn Đ4, ⛔ ép.

## Câu còn treo
- không có.
