# WO-070 — ISP 3.1.2 · Step 1 · H1: CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD)

| | |
|---|---|
| **Trạng thái** | `MO` *(→ `DANG_LAM` khi orchestrator giao)* |
| **Phát bởi** | orchestrator (phiên điều phối ISP, thay `fls-ba` phát phiếu) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **BE-HC** · cụm PostgreSQL riêng cổng **5435** |
| **Dải phiếu** | `BG-071` (bàn giao) · `KQ-072` (R1) · `KQ-073` (R2) · `KQ-074` (R3) |
| **Phụ thuộc** | S0 — phải `done` (3 vòng review + gộp) trước khi giao |

## Vì sao
- ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 1 · H1** — nguồn sự thật duy nhất của phiếu này (8 trường + Substep 1/2).
- Goal: `tinh_gl(dong, fx)` trả, cho mỗi dòng, Nợ/Có tách theo 5 tiền tệ, bVND = tỷ giá × tiền / 10⁹ và mUSD = bVND ÷ USD × 10³ — đúng tay tính trên 6 dòng tổng hợp.

## Căn cứ
- Người dùng 16/11: *"Xác nhận các recommend. Xác nhận ISP. Bắt đầu triển khai"* · *"Tự chạy theo wave"*.
- Traceability: AP v3.1.2 §3.3.1 PD 406 · 412 · §3.5.4 WP-C2 · AC9 (engine đọc config, ⛔ gõ lại).

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1.3 · §2.1 · Step 1 · H1 | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | theo Traceability | 3.1.2 · sha256 `5cf6e576…` |
| `04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` | cột **luật phòng tái phạm** | sống |
| `01_Orchestrator/isp-3.1/TIEN_DO.md` | Quy ước chạy song song | sống |
| `CLAUDE.md` | Đ1–Đ5 · Cổng · Bẫy | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| `fls/bao_cao/gl.py` thuần; tỷ giá vào bằng THAM SỐ (dict tháng → tiền tệ) — ⛔ đọc kho; tồn luỹ kế theo thứ tự dòng đưa vào (giữ hành vi AS-IS, ghi rõ) | dữ liệu thật (H4); dòng HR (H7) |

Khái niệm mới duy nhất: engine quy đổi GL · mock/static: 6 dòng tổng hợp + tỷ giá tổng hợp · tệp chạm: `fls/bao_cao/gl.py` · `tests/bao_cao/test_gl.py`.

## Tiêu chí nghiệm thu *(= test ID của ISP mục 6; exit criteria = mục 8)*
| AC | Mong *(đo được)* | Cách đo | Vì sao đỏ trước thay đổi |
|---|---|---|---|
| AC-1 (`H1-B1`) | bVND 2,5 · mUSD 98,039… | dòng VND Nợ 2.500.000.000, tỷ giá USD 25.500 · đơn vị | module chưa có |
| AC-2 (`H1-B2`) | tách đúng cột Có; tồn = tồn trước − Có | dòng USD Có · đơn vị | — |
| AC-3 (`H1-B3`) | ném lỗi có tên (⛔ trả 0 — chính lỗi SUMIFS = 0 của AS-IS) | tháng ⛔ có tỷ giá · đơn vị | — |
| AC-4 (`H1-B4`) | `fls/bao_cao` ⛔ chạm DB | lint-imports · kiến trúc | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG` (container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt).

## Câu còn treo
- không có.

## Rủi ro
1. Giới hạn đã khai ở ISP: chưa so với đáp án 406 — H4.
2. Chạy song song với hai làn khác — chỉ chạm tệp của làn mình (`TIEN_DO.md` §Quy ước); ⛔ sửa `08_CHANGELOG_RELEASE.md`, dashboard (orchestrator ghi lúc gộp).
