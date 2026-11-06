# Thẻ eval: `a3-3-nen-tang` — MAPPING PP (3) · chi phí nền tảng ↔ PE/PM ↔ bank txns

Phần chung: `_chung.md`. Trạng thái: nháp.

## Dấu trên sơ đồ
| Dấu | Giá trị |
|---|---|
| Dải | ③ MAPPING (WRITE) |
| Agent | PROPOSED; ⛔ chưa có `v0` mã ⇒ vòng đầu so với **AS-IS** (PHÂN BỔ NỀN TẢNG `[oALL]`) |
| Fleet eval | PROPOSED |
| Người kiểm | **chưa có** (lỗ trên sơ đồ) |
| Người dùng | ThuongCT + kế toán đọc chi phí theo CDT1 · tín hiệu: sửa, khiếu nại |

## A. Cái gì và vì sao
| | |
|---|---|
| Agent làm gì | Chi phí OMC · GI · SC (server cost) · PS từ Looker → Combine Code (Vendor-Date-NoTrans) → PE/PM line → Reference No → giao dịch bank → chia theo CDT1. |
| Lỗi đáng sợ nhất | **Nối nhầm PE** (Combine Code trúng sai) hoặc **chia sai CDT1** ⇒ chi phí nền tảng về sai chủ dự toán, nhìn vẫn cân. |
| Phép kiểm | `a3-3-nen-tang.eval.chia-sai` |

## B. Đầu vào của vòng
| | |
|---|---|
| Bộ ca | File Looker theo tháng + PE/PM + bank txns; đáp án = PHÂN BỔ NỀN TẢNG của AS-IS **sau khi người xác nhận** (AS-IS chưa có người kiểm ⇒ phải gán nhãn). Cỡ bể: **câu hỏi mở**. |
| Ca cài sẵn | Combine Code trúng **≥ 2 PE** · trúng **0 PE** · vendor đổi tên · chi phí trả trước / sau tháng · Σ % CDT1 ≠ 100. **Ca chuyển:** vendor mới. |
| Đơn vị (heatmap) | **loại:** OMC · GI · SC · PS — **ca cài sẵn:** trúng nhiều · trúng 0 · lệch kỳ · ca chuyển |
| Persona | P1 · P2 · P3 (gợi ý) |
| Bộ chấm | Rubric 0–2: 0 = nối sai PE / sai giao dịch / Σ chia sai · 1 = nối đúng, % CDT1 sai · 2 = nối đúng + chia đúng + lý do nêu Combine Code. |

## C. Bar, mẫu, nơi nhận
| | |
|---|---|
| Chỉ số + bar | **Tỉ lệ dòng chi phí đúng trọn chuỗi** (PE/PM · giao dịch · CDT1) ≥ bar tuyệt đối — **câu hỏi mở** (chưa có `v0` để so); **0** sai trên ca cài sẵn "trúng nhiều / trúng 0" *(đề xuất)*. |
| Chênh nhỏ nhất | **câu hỏi mở** — phụ thuộc cỡ bể. |
| Mẫu *(đề xuất)* | mọi ca cài sẵn + 2 tháng × 4 loại, phân tầng theo vendor × 3 persona. |
| Nơi nhận | Nối nhầm → luật Combine Code / prompt A3.3 · CDT1 trên Looker sai → chủ file (DATA / người cập nhật SC · PS) · ô không có ca → ca kiểm mới. |
