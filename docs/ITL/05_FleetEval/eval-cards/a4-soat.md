# Thẻ eval: `a4-soat` — A4 · Auditor (Compounding Loop) · agent chấm

Phần chung: `_chung.md`. Trạng thái: nháp. **JUDGE**: agent này chấm agent khác ⇒ phải có fleet eval riêng.

## Dấu trên sơ đồ
| Dấu | Giá trị |
|---|---|
| Dải | ④ SOÁT (JUDGE) |
| Agent | PROPOSED · **`gpt-oss-120b` qua API** (khác họ Qwen của các agent nó soát); `v0` mã `fls/kiem/soat_nap.py` (9 luật S1–S8 + S10) BUILT |
| Fleet eval | PROPOSED |
| Người kiểm | kế toán đọc biên bản 9 dòng trên F04 · QUICK · mỗi lô |
| Người dùng | kế toán quyết Nhận lô (S4) · tín hiệu: nhận / không nhận lô |

## A. Cái gì và vì sao
| | |
|---|---|
| Agent làm gì | Soát kết quả A2 · A3 theo 9 luật + 4 vế + Σ PM line + số dư ngày = CCR (DIF = 0) → Đạt · CHẶN · CỜ, biên bản cho kế toán quyết nhận lô. |
| Lỗi đáng sợ nhất | **Bỏ lọt**: lô đáng CHẶN được báo đạt ⇒ dòng sai / mất vào sổ chỉ-thêm, ⛔ xoá được. |
| Phép kiểm | `a4-soat.eval.lot-chan` |

## B. Đầu vào của vòng
| | |
|---|---|
| Bộ ca | Lô thật đã nạp (8.338 dòng, 60 nguồn) + **lô đột biến dựng có đáp án biết trước**: xoá 1 dòng · nhân đôi 1 dòng · đổi dấu Nợ/Có · đổi kiểu ngày giữa sheet · hạ mã xuống `float` · xoá tiền tệ · sửa số dư CCR · hai bản khai trỏ khác cột. |
| Ca cài sẵn (lỗi thật) | **646 dòng bị loại không có bản ghi** (`0020`, 23 nguồn) · **31 mã bị hạ `float`** ở Bank Transactions của AS-IS · **10/60** nguồn rỗng (phải "chưa đo", ⛔ đỏ oan). **Ca chuyển:** nguồn có bố cục cột chưa gặp. |
| Đơn vị (heatmap) | **mất / thừa dòng:** S1 · S7 — **thiếu trường:** S2 · S3 · S4 — **định dạng / nguồn:** S5 · S6 · S8 · S10 — **số dư:** S9 · DIF CCR — **ca chuyển** |
| Persona | P1 · P2 · P3 đọc biên bản: có quyết đúng nhận / không nhận lô không (gợi ý) |
| Bộ chấm | **`Qwen 3.8`** qua API (khác mô hình của A4) · rubric 0–2: 0 = báo đạt ca phải chặn · 1 = chặn đúng, sai hạng (CHẶN ↔ CỜ) hoặc thiếu nguồn dính · 2 = đúng hạng + đúng nguồn + đúng số đo. |

## C. Bar, mẫu, nơi nhận
| | |
|---|---|
| Chỉ số + bar | **Tỉ lệ bỏ lọt** trên lô đột biến: **0** *(đề xuất)*; **tỉ lệ báo động oan** trên lô sạch ≤ `v0`. |
| Chênh nhỏ nhất | 1 ca bỏ lọt = chặn. |
| Mẫu *(đề xuất)* | ≥ 1 lô đột biến cho mỗi luật (≥ 10) + 5 lô sạch + ca chuyển × 3 persona. |
| Nơi nhận | Bỏ lọt → luật soát / prompt A4 · biên bản khó đọc → mẫu biên bản F04 · khuyết tật ở nguồn → kế toán nhập liệu. |
