# WO-075 — ISP 3.1.2 · Step 2 · C1: IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx

| | |
|---|---|
| **Trạng thái** | `MO` *(→ `DANG_LAM` khi orchestrator giao)* |
| **Phát bởi** | orchestrator (phiên điều phối ISP, thay `fls-ba` phát phiếu) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **BE-CF** · cụm PostgreSQL riêng cổng **5434** |
| **Dải phiếu** | `BG-076` (bàn giao) · `KQ-077` (R1) · `KQ-078` (R2) · `KQ-079` (R3) |
| **Phụ thuộc** | S0 — phải `done` (3 vòng review + gộp) trước khi giao |

## Vì sao
- ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 2 · C1** — nguồn sự thật duy nhất của phiếu này (8 trường + Substep 1/2).
- Goal: Gọi `GET /api/fls/v1/config/fx` → `{bang:'IX.FX', nguon, ky:[{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}], thieu:[yyyymm], trung:[yyyymm], lac:[yyyymm]}` trả bảng tỷ giá từ nguồn tĩnh, và tháng thiếu/trùng/lạc hiện ra trong trường riêng thay vì im lặng thành 0.

## Căn cứ
- Người dùng 16/11: *"Xác nhận các recommend. Xác nhận ISP. Bắt đầu triển khai"* · *"Tự chạy theo wave"*.
- Traceability: AP v3.1.2 §3.2.1 IX.FX · §3.2.4 dòng 'bảng tỷ giá' · §3.5.3 D1 · AC9.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1.3 · §2.1 · Step 2 · C1 | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | theo Traceability | 3.1.2 · sha256 `5cf6e576…` |
| `04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` | cột **luật phòng tái phạm** | sống |
| `01_Orchestrator/isp-3.1/TIEN_DO.md` | Quy ước chạy song song | sống |
| `CLAUDE.md` | Đ1–Đ5 · Cổng · Bẫy | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| `fls/cau_hinh/fx.py`: nạp + kiểm (một dòng/tháng, VND = 1, 5 tiền tệ, thiếu/trùng/lạc); tuyến GET đọc nguồn tĩnh `fls/cau_hinh/tinh/ix_fx_mau.json` (4 tháng TỔNG HỢP, ⛔ số thật); khai tuyến + bảng ở `soi_bang_tuyen` | kho (C5); ký tháng (C7); ảnh thật (DT2 — C5 nối) |

Khái niệm mới duy nhất: miền config `fls/cau_hinh` (nạp + kiểm thuần) · mock/static: nguồn tĩnh 4 tháng tổng hợp · tệp chạm: `fls/cau_hinh/fx.py` · `fls/cau_hinh/tinh/ix_fx_mau.json` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_fx.py` · `tests/api/test_isp_config_fx.py`.

## Tiêu chí nghiệm thu *(= test ID của ISP mục 6; exit criteria = mục 8)*
| AC | Mong *(đo được)* | Cách đo | Vì sao đỏ trước thay đổi |
|---|---|---|---|
| AC-1 (`C1-B1`) | 4 dòng, VND = 1, `thieu = trung = lac = []` | nạp 4 tháng hợp lệ · đơn vị | module chưa có |
| AC-2 (`C1-B2`) | `trung = ['202407']`; ⛔ cộng đôi | tháng 202407 có hai dòng · đơn vị | — |
| AC-3 (`C1-B3`) | `thieu = ['202408']` | thiếu 202408 giữa dải · đơn vị | — |
| AC-4 (`C1-B4`) | 200, đúng hợp đồng; `soi_bang_tuyen` xanh với tuyến mới | GET qua máy chủ thử · API | tuyến chưa có |
| AC-5 (`C1-B5`) | `fls/cau_hinh` ⛔ import psycopg/repo/db | lint-imports · kiến trúc | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG` (container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt).

## Câu còn treo
- không có.

## Rủi ro
1. Giới hạn đã khai ở ISP: số trả về là tổng hợp cho tới C5 — FE vẫn dựng được trên hợp đồng.
2. Chạy song song với hai làn khác — chỉ chạm tệp của làn mình (`TIEN_DO.md` §Quy ước); ⛔ sửa `08_CHANGELOG_RELEASE.md`, dashboard (orchestrator ghi lúc gộp).
