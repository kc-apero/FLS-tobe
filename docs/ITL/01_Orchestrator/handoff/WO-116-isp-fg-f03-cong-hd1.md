# WO-116 — ISP 3.1.2 · Step 9 · FG: F03 "Cổng hôm nay" hiện cổng HD1 (đọc tuyến thật)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 17/11 |
| **Phát bởi** | orchestrator (phiên điều phối ISP, account mới) · 2026-11-17 |
| **Nhận** | `fls-dev` làn **FE** — **phiên cloud** (model Opus 4.8 · medium) · cụm PG **5436** của phiên ấy · nhánh `isp/FG` |
| **Nền** | `isp/CG1` @ `4dfb7bd` (= `isp/base-w3` [nhánh làm việc cũ + S0 `fb79f7e` + DT1a `e8b33b3` + H2 `5e63a90`] + CG1 mã `d6d50f4` + BG + phiếu R1) |
| **Dải phiếu** | `BG-117` (bàn giao) · `KQ-118` (R1) · `KQ-119` (R2) · `KQ-120` (R3). Số trống kế tiếp: **121** |

## Vì sao
- ISP **Step 9 · FG** — nguồn sự thật duy nhất. Phụ thuộc CG1: bàn giao `BG-102` + R1 `KQ-103` **0 CHẶN** (chế độ tăng tốc). S0 (bộ test web) đã gộp.

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 9** (· Step 7 CG1 để biết `/gates`) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §5.2 UF-2 · §5.3.1 HD1 · Hình 5.3.3 | 3.1.2 |
| `fls/web/tep/man_f03.js` | `_muc`, lớp `.gate.unk` (ba trạng thái đã vẽ) | nền |
| `BG-102` · `KQ-103` | hợp đồng `/gates` của CG1: `FINAL` `DAT 69.510/69.510 ô` (Đ4: 7 khối × 9.930 dòng giữ sau tự soi) · `HD1_THANG` `KHÔNG ĐẠT 5/23 kỳ đạt`; `--tep-do ''` ⇒ +2 `chua_do_duoc` | nền |
| `CLAUDE.md` | Đ1–Đ5 · Bẫy · Riêng tư | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (FG-F1) | mở F03 qua máy chủ thử `fls/web/phuc_vu.py` với tệp đo THẬT (`docs/ITL/_tools/voi_so_luong.json` của nền) ⇒ thẻ `FINAL` ĐẠT; `HD1_THANG` KHÔNG ĐẠT kèm `5/23`; số "chưa đo được" trên màn = số tuyến trả | `tests/web/test_isp_f03_hd.py` (node headless `tests/web/khung_node.py` + `dom_gia.js`) | thẻ chưa có |
| AC-2 (FG-F2) | tệp đo vắng ⇒ hai thẻ lớp `.gate.unk` "KHÔNG ĐO ĐƯỢC", ⛔ xanh | cùng tệp bài | — |
| AC-3 (FG-F3) | lý do 23 kỳ ở bề rộng **390 px** ⇒ ⛔ tràn ngang (gấp/mở trong thẻ nếu cần — sửa TỐI THIỂU `man_f03.js`) | DOM | — |
| AC-4 (FG-F4) | `tests/web` sẵn có xanh (token màu, một bản mẫu, phím) — tập đỏ web = đường nền | `--duong-nen` | — |
| AC-5 (Q8) | nhánh có `MONG_PYTEST_TOAN_BO`/`MONG_PYTEST_WEB` của bản CG1 ⇒ nâng cùng commit theo số `--collect-only` của nhánh; orchestrator đặt lại = thu thập cây gộp lúc gộp | BG | — |

## Ràng buộc
- ⛔ sửa tuyến `/gates`, `fls/repo/doc_bao_cao.py` (CG1 — dùng, ⛔ sửa). ⛔ màn mới. ⛔ khoan xuống từng dòng.
- Hợp đồng H2 ↔ CG1 (orchestrator 17/11): FG chỉ đọc khoá mà `/gates` trả; ⛔ đọc thẳng `voi_so_luong.json`.

## Dữ liệu
- Ghi kho THẬT: `KHONG`.

## Câu còn treo
- không có.
