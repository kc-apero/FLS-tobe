# WO-208 — ISP 3.1.2 · Step 30 · CG2: cổng HD2 theo gói WP-C2…C5 vào `GET /gates`

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~23:00 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **FE** (quyền tệp BE-CF — ISP §2.1) — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5446** · nhánh `isp/CG2` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp CG1 · H4 · H5 · H6 — `tools/do_hd2.py` ghi `hd2_cong.json` cho gói `WP-C2` · `WP-C3a` · `WP-C3b`) |
| **Dải phiếu** | `BG-209` · `KQ-210` (R1) · `KQ-211` (R2). Số trống kế tiếp: **212** |

## Vì sao
- ISP **Step 30 · CG2** (wave W10) — nguồn sự thật duy nhất. Phụ thuộc CG1 · H4 (đã gộp). Khái niệm mới: không (khuôn CG1).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 30** (· Step 7 CG1 làm khuôn) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §5.3.1 HD2 · §3.5.4 | 3.1.2 |
| `tools/do_hd2.py` (`GOI_BIET`, khối ghi `hd2_cong.json`) · `fls/repo/doc_bao_cao.py` · `fls/api/bang_tuyen.py` · bài CG1 · `cong_parity.PhanXu` | hợp đồng + khuôn | nền |
| `CLAUDE.md` | Đ1–Đ5 | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (CG2-B1) | tệp chỉ có WP-C2 ⇒ WP-C2 theo `PhanXu`; các gói khác `dat = null` ("chưa đo") | `tests/api/test_isp_gates_hd2.py` | cổng chưa có |
| AC-2 (CG2-B2) | gói có `lat_bo > 0` ⇒ `dat = false` (⛔ "100%") | API | — |
| AC-3 (CG2-B3) | tệp vắng / hỏng ⇒ mọi cổng HD2 `dat = null` + lý do có tên (⛔ "0 lệch") | API lỗi | — |
| AC-4 | **danh sách gói**: ISP nói "4 cổng WP-C2…C5" nhưng tệp thật đã có gói con (`WP-C3a` · `WP-C3b`; sắp có `WP-C3c` H7 · `WP-C4a` H9). Cổng = HỢP của gói khai sẵn (`WP-C2` · `WP-C3` · `WP-C4` · `WP-C5` mức gói) và gói con có trong tệp; gói cha `dat` = gộp gói con (một con `false` ⇒ `false`; còn con `null` ⇒ `null`). Gói con mới tự hiện, ⛔ sửa mã. Khai cách gộp trong BG (Đ4: số cổng đếm gì) | API | — |
| AC-5 | `soi_bang_tuyen.py` ĐẠT; hợp đồng `GET /gates` cũ giữ (chỉ THÊM phần tử) | `soi` + pytest | — |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- ⛔ khoan xuống từng ô lệch. ⛔ sửa `tools/do_hd2.py` ngoài việc đọc hằng (nếu cần xuất `GOI_BIET` ⇒ khai). ⛔ di trú. Ghi kho THẬT: `KHONG`.

## Câu còn treo
- không có.
