# WO-101 — ISP 3.1.2 · Step 7 · CG1: cổng HD1 vào `GET /gates` (ô chờ `FINAL` thành số đo + cổng `HD1_THANG`)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **BE-CF** · cụm PG **5434** · worktree `.claude/worktrees/isp-cg1` · nhánh `isp/CG1` |
| **Nền** | `isp/base-w3` @ `575926e` = nhánh làm việc `0296b02` + `isp/S0` @ `fb79f7e` + `isp/DT1A` @ `e8b33b3` + `isp/H2` @ `5e63a90` |
| **Dải phiếu** | `BG-102` (bàn giao) · `KQ-103` (R1) · `KQ-104` (R2) · `KQ-105` (R3) |

## Vì sao
- ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 7 · CG1** — nguồn sự thật duy nhất.
- Chế độ tăng tốc (người dùng 16/11): phụ thuộc H2 đã bàn giao (`BG-091`) + R1 `KQ-092` **0 CHẶN**; DT1a đã R2 ĐẠT (`KQ-083`).

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · Step 7 | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §5.3.1 HD1 · HD5 · §5.3.2 AC10 | 3.1.2 · sha256 `5cf6e576…` |
| `01_Orchestrator/handoff/KQ-092-*.md` (trên `isp/H2`) | `H2-R1-01` · `-02` | R1 H2 |
| `CLAUDE.md` | Đ1–Đ5 · Cổng · Bẫy | — |
| `01_Orchestrator/isp-3.1/TIEN_DO.md` | Quy ước chạy song song | 16/11 |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| `fls/repo/doc_bao_cao.py` (`doc_cong` · `_CHUA_DO_DUOC`): ô chờ `FINAL` ⇒ số đo từ tệp đo; cổng mới `HD1_THANG`; đường dẫn tệp đo **truyền vào** (hợp đồng tầng 7), ⛔ gõ cứng | cổng HD2 (CG2) · thẻ trên màn (FG) · đọc kho sống (HD5 sau) |
| `tests/api/test_isp_gates_hd1.py` (CG1-B1…B4) | sửa `tools/do_voi_so_luong.py` — làn BE-HC đang vá `H2-R1-01/02` song song |

## Hợp đồng với H2 *(orchestrator chốt, vì H2 đang vòng sửa song song)*
- CG1 đọc **chỉ** các khoá: `dat_hd1.so_ky_dat` · `dat_hd1.mau_so.so_ky` · `dat_hd1.theo_ky[k].dat` · `dat_hd1.theo_ky[k].thieu` · `dat_hd1.ky_dat` *(+ khoá ngày ảnh nếu có)*. Vòng sửa H2 được lệnh giữ nguyên các khoá ấy (chỉ THÊM khoá).
- `H2-R1-01` đổi LUẬT phán kỳ (vế ô tính trên MỌI dòng), ⛔ đổi hình dạng — hôm nay vẫn `5/23` (đo R1: cùng 5 kỳ). CG1 ⛔ tự tính lại luật; chỉ đọc `dat`.
- Con số `FINAL` `69.510/69.510 ô` của ISP: **đo lại**, ⛔ tin — lệch ⇒ ghi Đ4 *(nó đếm gì)* trong BG, ⛔ sửa ISP.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (CG1-B1) | `FINAL` dat true · `da_do` số ô đo; `HD1_THANG` dat false · `da_do '5/23 kỳ đạt'` · `ly_do` liệt kê kỳ đỏ + số dòng thiếu + ngày ảnh | pytest qua tuyến thật | ô chờ còn `dat = null` |
| AC-2 (CG1-B2) | tệp đo vắng ⇒ cả hai `dat = null`, `chua_do_duoc` tăng **đúng 2**; ⛔ 200 toàn xanh | pytest | — |
| AC-3 (CG1-B3) | bài `/gates` sẵn có + `tests/api` xanh | pytest | — |
| AC-4 (CG1-B4) | phá MONG trong bài ⇒ ĐỎ, trả nguyên ⇒ xanh | ghi lệnh + exit trong BG | — |
| AC-5 (Q8) | bài mới cộng vào `MONG_PYTEST_TOAN_BO` trong **cùng commit** (`tools/dung_moi_truong_isp.sh`) | `--duong-nen --cong 5434` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Tệp đo là ảnh tĩnh đã commit.

## Câu còn treo
- không có.
