# WO-226 — ISP 3.1.2 · alias nhãn `ITE | ITE Interest` → nút `ITE` (lệch AS-IS có chủ đích)

| | |
|---|---|
| **Trạng thái** | `MO` — giao khi có chỗ (≤ 3 phiên) |
| **Phát bởi** | orchestrator · 2026-11-19 · theo quyết của chủ 19/11 ~04:20 UTC (phương án **A**) |
| **Nhận** | `fls-dev` làn **BE-CF/HC** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/ITE` |
| **Dải phiếu** | `BG-230` · `KQ-231` (R1) · `KQ-232` (R2) |

## Vì sao
- Đo trên `gl_cf_dau_vao.json` (sheet `Report I General Ledger` của CF report, cột V): nhãn `ITE | Interest` (khớp nút cây) 134 dòng 2024-11 → 2025-12; nhãn **`ITE | ITE Interest`** 152 dòng 24/11/2025 → 31/10/2026 + **`ITE | ITE Interest `** (dấu cách cuối) 1 dòng 24/02/2025 ⇒ nhãn nguồn ĐỔI từ 11/2025; CFA1 AS-IS bỏ sót toàn bộ (VND Nợ 8.466.662 · USD Nợ 16.137,66 / Có 4.469,33 · SGD Nợ 25,15 / Có 50; ≈ 0,01197 mUSD ròng). FLS hiện tái lập đúng lỗi ấy (`hd_ngoai_cay` 162 = ITE 153 + Server Cost 7 + GAC - Other 1 + rỗng 1).
- Chủ chọn **A**: thêm alias ⇒ FLS **cố ý lệch** AS-IS ở đúng phần lãi ITE, có khai.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | bảng alias nhãn HD là CẤU HÌNH (kho config chỉ-thêm C5 hoặc khai trong IX.HD — chọn một, khai lý do; ⛔ `if` trong engine); alias so khớp sau chuẩn hoá khoảng trắng hai đầu; nhãn ngoài cây khác (Server Cost 7 · GAC - Other 1 · rỗng 1) GIỮ nguyên `hd_ngoai_cay` | pytest |
| AC-2 | `hd_ngoai_cay` 162 → **9**; 153 dòng ITE vào nút `ITE` | `do_hd2.py` + pytest |
| AC-3 | WP-C3a · WP-C3b: các ô lệch đáp án 409/410 do alias được khai `mong` CÓ TÊN (`lech_co_chu_dich_ite`: số ô · ngày/kỳ · Σ mUSD) — Đ5 hai chiều; ô khác vẫn khớp 100 %; gói vẫn `dat = true` theo hợp đồng CG2 (`tong_o`/`khop` + khoá lệch có chủ đích) | `do_hd2.py --goi WP-C3a/C3b --ghi` + pytest |
| AC-4 | `GET /gates` HD2 vẫn đúng (bài quét `hd2_cong.json` của CG2 xanh) | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ sửa ảnh `tests/fixture/**`. ⛔ di trú mới (nếu dùng kho config — dùng `0027`). Ghi kho THẬT: `KHONG`.
