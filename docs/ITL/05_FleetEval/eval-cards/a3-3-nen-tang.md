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
| Agent làm gì | Nguồn: GI · OMC từ Looker (Data · AnhTQ); SC (server cost) từ Gsheet *Chi phí Service Apero* (SHQ1 · Luận); PS từ Gsheet *AperoGroup_Payment* (SHQ2 · kế toán) — PD Now 103–106. Dòng ITL đã có PE/PM và đã nối bank ⨝ dòng nguồn theo Combine Code (Vendor-Date-NoTrans) → Mapping Block 1 (ID Vendor ↔ Network-Acc ↔ CDT1) → chia CDT1 × tháng (PD Now 501–507). |
| Lỗi đáng sợ nhất | **Nối nhầm PE** (Combine Code trúng sai) hoặc **chia sai CDT1** ⇒ chi phí nền tảng về sai chủ dự toán, nhìn vẫn cân. |
| Phép kiểm | `a3-3-nen-tang.eval.chia-sai` |

## B. Đầu vào của vòng
| | |
|---|---|
| Bộ ca | 4 sổ Platform Data Ledger H2.2025 (GI · OMC Looker, SC · PS Gsheet) + dòng ITL đã adjust; đáp án = PHÂN BỔ NỀN TẢNG của AS-IS **sau khi người xác nhận** (AS-IS chưa có người kiểm ⇒ phải gán nhãn). Bể: **không giới hạn** (KhanhCQ 06/11). |
| Ca cài sẵn | Combine Code trúng **≥ 2 PE** · trúng **0 PE** · vendor đổi tên · chi phí trả trước / sau tháng · Σ % CDT1 ≠ 100. **Ca chuyển:** vendor mới. |
| Đơn vị (heatmap) | **loại:** OMC · GI · SC · PS — **ca cài sẵn:** trúng nhiều · trúng 0 · lệch kỳ · ca chuyển |
| Persona | P1 · P2 · P3 (gợi ý) |
| Bộ chấm | Rubric 0–2: 0 = nối sai PE / sai giao dịch / Σ chia sai · 1 = nối đúng, % CDT1 sai · 2 = nối đúng + chia đúng + lý do nêu Combine Code. |

## C. Bar, mẫu, nơi nhận
| | |
|---|---|
| Chỉ số + bar | **Tỉ lệ dòng chi phí đúng trọn chuỗi** (PE/PM · giao dịch · CDT1) **không có bar tổng** (KhanhCQ 06/11) — chỉ báo cáo; bar duy nhất: **0** sai trên ca cài sẵn "trúng nhiều / trúng 0 / lệch kỳ". |
| Chênh nhỏ nhất | 1 ca cài sẵn sai. |
| Mẫu *(đề xuất)* | mọi ca cài sẵn + 2 tháng × 4 loại, phân tầng theo vendor × 3 persona. |
| Nơi nhận | Nối nhầm → luật Combine Code / prompt A3.3 · số liệu nguồn sai → chủ sổ (Data cho GI · OMC; Luận cho SC; kế toán cho PS) · ô không có ca → ca kiểm mới. |
