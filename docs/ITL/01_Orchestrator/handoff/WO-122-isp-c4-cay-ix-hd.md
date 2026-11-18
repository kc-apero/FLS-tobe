# WO-122 — ISP 3.1.2 · Step 11 · C4: IX.HD cây — nạp + kiểm cha–con + `GET /config/hd` (tĩnh từ ảnh)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-CF** — **phiên cloud** (model Opus 4.8 · medium) · cụm PG **5434** của phiên ấy · nhánh `isp/C4` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp C1 — khuôn tuyến `/config/fx` · `fls/cau_hinh/` · `nguon_tinh`; DT3 — ảnh `tests/fixture/cau_hinh/atl_cay.json` + `mapping_master_cfg.json`) |
| **Dải phiếu** | `BG-123` (bàn giao) · `KQ-124` (R1) · `KQ-125` (R2) · `KQ-126` (R3). Số trống kế tiếp: **127** |

## Vì sao
- ISP **Step 11 · C4** — nguồn sự thật duy nhất. Phụ thuộc DT3: đã gộp vào nhánh làm việc 18/11 (R3b `KQ-121` ĐẠT 0 · 0).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 11** (· Step 2 C1 làm mẫu tuyến tĩnh) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.1 IX.HD · §3.2.5 (cây ATL) · §3.2.4 "cây HD theo vị trí dòng" · WP-C1 | 3.1.2 |
| `02_BA/07_API_CONTRACT.md` | §4i dòng `GET /api/fls/v1/config/hd` (⬜ — orchestrator đổi ✅ lúc gộp) | v3.16 |
| `tests/fixture/cau_hinh/atl_cay.json` · `mapping_master_cfg.json` | ảnh DT3: cây **74** dòng mã · **6** nhóm (`HDO · HDH · HDAP · HDT · HDC · HDCI`) · `MONG_CAP` 37 · 23 · 11 · 3 (L1…L4); MM **73** mã `hd` (ATL − MM = `{NCF}` theo `BG-107`) | DT3 |
| `fls/cau_hinh/fx.py` · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `tools/soi_bang_tuyen.py` | khuôn tuyến tĩnh C1 (`nguon_tinh`, `?run_id=` ⇒ 400, cổng ⓔ của `soi`) | nhánh làm việc |
| `CLAUDE.md` | Đ1–Đ5 · Bẫy · Riêng tư | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (C4-B1) | nạp ảnh ATL ⇒ **74** nút · **6** nhóm · gốc đúng · ⛔ chu trình · cấp L1…L4 khớp `MONG_CAP` của ảnh | `tests/cau_hinh/test_hd.py` | module chưa có |
| AC-2 (C4-B2) | cây tổng hợp có chu trình A→B→A ⇒ lỗi có tên `HD_CHU_TRINH` | đơn vị | — |
| AC-3 (C4-B3) | cha vắng ⇒ lỗi có tên `HD_CHA_VANG`; cấp nhảy (con cấp n+2) ⇒ lỗi có tên (Goal: "cấp nhảy") | đơn vị | — |
| AC-4 (C4-B4) | `GET /api/fls/v1/config/hd` ⇒ `200`, 74 nút, `con_cua`/`la` đúng; trả **cả hai số** 74 (ATL) · 73 (MM) + `chenh_mapping_master` liệt kê mã chênh (⛔ hoà giải); ảnh đọc qua đường dẫn TRUYỀN VÀO (tầng 7, ⛔ gõ cứng) | `tests/api/test_isp_config_hd.py` + máy chủ thử | tuyến chưa có |
| AC-5 | theo khuôn C1: `?run_id=` ⇒ `400` (bảng tĩnh); tuyến khai `nguon_tinh` qua `fls/cau_hinh/tinh/` hoặc đường ảnh tương đương; `tools/soi_bang_tuyen.py` ĐẠT; bài BA-07 phủ tuyến (`tests/api/test_ba07_phu_het_tuyen.py`) xanh với dòng §4i hiện có | pytest + `soi` | — |
| AC-6 (Q8) | nhánh có `MONG_PYTEST_TOAN_BO` (nền = nhánh làm việc) ⇒ nâng cùng commit + bài ghim `tests/test_dung_moi_truong_isp.py` | `--duong-nen` | — |

## Ràng buộc
- ⛔ cha = Σ con (việc engine H5). ⛔ kho (C5). ⛔ hoà giải 74 ↔ 73 (chỉ liệt kê chênh). ⛔ sửa ảnh DT3.
- Lỗi cây có TÊN (hằng chuỗi), ⛔ `ValueError` trơn.

## Dữ liệu
- Ghi kho THẬT: `KHONG`.

## Câu còn treo
- không có.
