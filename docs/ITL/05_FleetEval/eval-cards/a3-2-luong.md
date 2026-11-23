# Thẻ eval: `a3-2-luong` — A3.2 · Filter Fulfill & Adjust · PP (2) · dòng lương H1000 ↔ bank txns

Phần chung: `_chung.md`. Trạng thái: nháp.

## Dấu trên sơ đồ
| Dấu | Giá trị |
|---|---|
| Dải | ③ MAPPING (WRITE) |
| Agent | PROPOSED; ⛔ chưa có `v0` mã ⇒ vòng đầu so với **AS-IS** (H1000 Final) |
| Fleet eval | PROPOSED |
| Người kiểm | **chưa có** — ghi vào sổ chỉ qua fleet eval (lỗ trên sơ đồ) |
| Người dùng | ThuongCT + kế toán; C&B HR · tín hiệu: sửa, khiếu nại |

## A. Cái gì và vì sao
| | |
|---|---|
| Agent làm gì | Nạp thẳng dòng lương H1000 (đã tách HD · CDT1 · pháp nhân) và nối với giao dịch bank theo Số CT (số FT kế toán dán). |
| Lỗi đáng sợ nhất | **Ghi một đợt sai mà không báo**: tháng trùng, tháng thiếu, hoặc Σ Có ≠ Σ Nợ ⇒ chi phí lương ghi hai lần / sai pháp nhân / sai HD. |
| Phép kiểm | `a3-2-luong.eval.noi-sai-dot` |

## B. Đầu vào của vòng
| | |
|---|---|
| Bộ ca | 6 sổ H1000 năm (NIS/INT/COM · PIT, có 2026) + ITL Ledge (AS-IS nối bằng VLOOKUP Số CT ở dòng đảo `[dH1F]`). Mỗi tháng **25 đợt** = 5 pháp nhân × 5 loại `[dPR]`. Bể: **~34 file H1000 đã adjust** (KhanhCQ 06/11). |
| Ca cài sẵn (lỗi thật) | PIT 2025 gọi tháng 6 **hai lần** · NIS 2025 **thiếu** tháng 12 `[dH1000]` · 2025-10 No 4 (INT) lệch **567.500**, No 5 (PIT) lệch **≈ 510,8 tr** vì chưa dán giao dịch gốc `[pTACH]`. **Ca chuyển:** sổ 2026. |
| Đơn vị (heatmap) | **loại đợt:** NIS L1 · NIS L3 · COM L2 · INT · PIT — **ca cài sẵn:** tháng trùng · tháng thiếu · Σ lệch · ca chuyển |
| Persona | P1 · P2 · P3 · **P4 C&B HR** (gợi ý) |
| Bộ chấm | Rubric 0–2: 0 = ghi đợt lỗi / nối sai Số CT · 1 = chặn đúng nhưng lý do sai · 2 = xử lý đúng + lý do nêu được tháng / đợt / số lệch. |

## C. Bar, mẫu, nơi nhận
| | |
|---|---|
| Chỉ số + bar | **Tỉ lệ đợt lỗi bị ghi** trên ca cài sẵn: bar **0** *(đề xuất)*; đợt sạch: dòng lương nối đúng Số CT ≥ AS-IS. |
| Chênh nhỏ nhất | 1 đợt lỗi lọt = chặn. |
| Mẫu *(đề xuất)* | mọi ca cài sẵn + 3 tháng × 25 đợt lấy mẫu phân tầng theo loại × 4 persona. |
| Nơi nhận | Đợt lỗi lọt → luật nạp / prompt A3.2 · lỗi ở chính file lương (tháng trùng) → C&B HR, ⛔ vá trong agent · lý do khó hiểu → mẫu lý do. |
