# Thẻ eval: `a3-1-ref` — MAPPING PP (1) · bank txns ↔ lệnh chi theo Reference No

Phần chung: `_chung.md`. Trạng thái: nháp.

## Dấu trên sơ đồ
| Dấu | Giá trị |
|---|---|
| Dải | ③ MAPPING (WRITE) |
| Agent | PROPOSED (bản LLM); `v0` mã `fls/adapters/pm_join.py` BUILT |
| Fleet eval | PROPOSED |
| Người kiểm | kế toán ghép / sửa trên F01 (S5) · MEDIUM · mỗi dòng hàng chờ |
| Người dùng | ThuongCT + kế toán đọc sổ hiệu lực / báo cáo daily CCR · tín hiệu: duyệt, sửa, khiếu nại |

## A. Cái gì và vì sao
| | |
|---|---|
| Agent làm gì | Nhận dòng tiền hai vế + dòng lệnh PM/PC → xếp L1 (nối) · L2 (FPS có, bank chưa) · L3 (bank có, FPS không) + gợi ý HD/CDT1; kế toán dựa vào đó để chốt chiều chi phí. |
| Lỗi đáng sợ nhất | **Nối chắc chắn nhưng sai** một PM line (hoặc nối ca phải để người) ⇒ HD/CDT1 sai, kế toán tin vì mối nối trông như đã khớp; sai lan vào báo cáo theo chủ dự toán. |
| Phép kiểm | `a3-1-ref.eval.ghep-sai` |

## B. Đầu vào của vòng
| | |
|---|---|
| Bộ ca | Giao dịch bank đã có mối nối do người chốt ở ITL Ledge Final của AS-IS. Bể đã đo theo hình ghép (`pm_join.py:26–31`): A 1×1 **2.256 mã** · B 1×N **27** · C N×1 **80 mã / 394 dòng** · D N×M **5 mã / 27 dòng** · E khác tiền tệ **119 mã / 199 dòng** · F Σ lệch **325 mã / 452 dòng**; L3 có mã trong diễn giải (US-KT-037): mã rỗng **60** · diễn giải ghi mã khác **136**. |
| Ca cài sẵn | toàn bộ D (phải từ chối) · Ref trùng bị dùng lại (AS-IS VLOOKUP lấy dòng đầu) · Ref do người đè ở `_adjust` · phí bank cùng mã với khoản chính (F). **Ca chuyển:** tháng mới nhất chưa dùng khi tinh chỉnh. |
| Đơn vị (heatmap) | **phải nối:** A · B · C — **phải để người:** D · E · F — **L3:** không Ref · diễn giải mã khác · ca chuyển |
| Persona | P1 · P2 · P3 (gợi ý) |
| Bộ chấm | Rubric 0–2: 0 = nối sai / nối ca phải để người / rỗng · 1 = đúng lớp, sai PM line hoặc thiếu lý do · 2 = đúng lớp, đúng PM line, lý do nêu được khoá đã so. Giải thích lại 0–3. |

## C. Bar, mẫu, nơi nhận
| | |
|---|---|
| Chỉ số + bar | **Tỉ lệ nối sai** = (nối sai PM line + nối ca phải-để-người) ÷ số ca agent nối. Bar *(đề xuất)*: **0** trên ca cài sẵn nhóm "phải để người"; tổng ≤ `v0`; không tệ hơn bản trước. |
| Chênh nhỏ nhất đáng kể | 1 ca nối sai ở nhóm "phải để người" = chặn. |
| Mẫu mỗi vòng *(đề xuất)* | ~60 ca: toàn bộ D (5 mã) + 10 E + 10 F + 10 C + 5 B + 10 A + 10 L3 (+ ca chuyển) × 3 persona × 1 lần. |
| Nơi nhận phát hiện | Nối sai → luật ghép / prompt A3.1 (phiếu `WO` cho fls-dev) · lý do F01 người mới không dùng được → mẫu lý do F01 (`fls-ba`) · Ref gõ sai từ nguồn → người nhập (CA), ⛔ vá trong agent · ô không có ca → ca kiểm mới. |
