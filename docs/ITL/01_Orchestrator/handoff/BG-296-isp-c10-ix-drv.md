# BG-296 — Bàn giao WO-295 · ISP Step 29 · C10 IX.DRV

| | |
|---|---|
| Phát bởi | fls-dev BE-CF · 2026-11-22 · nhánh `isp/C10` (nền `089db1b`) |
| Gửi | fls-test (R1 = `KQ-297` · R2 = `KQ-298`) |

## Đã làm
`fls/cau_hinh/driver.py` (lõi thuần: `kiem` · `dung_tu_anh` · `BangDRV.driver_cua` · `nb_le_cua` · `DrvThieu`) · `nap_ix_drv`/`doc_drv`/`driver_cua(conn, …)` (`cau_hinh_repo.py`, dùng lại `nap` C5) · `GET /api/fls/v1/config/drv` (`cau_hinh_drv`, lọc `?loai=` `?ky=`) · dòng §4i `07_API_CONTRACT` ⬜ (orchestrator lật ✅). ⛔ di trú mới (dùng 0027) · ⛔ sửa ảnh DT10 · ⛔ sửa H12.
⚠ Chữ ký: `driver_cua(loai, cdt1, thang)` ở tầng kho nhận thêm `conn` đầu (khuôn `luat_cua`/`doc_alr`: `fls.cau_hinh` ⛔ biết kho — hợp đồng 10); bản thuần là `BangDRV.driver_cua(loai, cdt1, thang)`.

## AC ↔ bài (ĐỎ trước)
Lệnh đỏ ban đầu: 3 tệp bài mới trước khi có `nap_ix_drv`/tuyến ⇒ 18 failed (lõi thuần cũng đỏ vì lỗi miền `[0,1]` — xem dưới). Sau: **29 passed**.
| AC | Bài | Kết |
|---|---|---|
| C10-B1 | `test_driver_pg.py::test_C10_B1_nap_khu_hoi_kho_238_238_khop_anh` (mẫu số 238 ≠ 0 trước; `NOEM·SHQ1·202503` = ảnh) · đơn vị `test_C10_B1_238_238…` | xanh |
| C10-B2 | `test_driver.py::test_C10_B2_146_o_thieu_nem_DRV_THIEU_co_ten` (146/146, đúng `ly_do` ảnh) · `…_pg::test_C10_B2_146_…` (từ kho) · 2026 ⇒ `DRV_THIEU` ⛔ `0` ⛔ H1000 | xanh |
| AC-3 | `tests/api/test_isp_config_drv.py` (200 · lọc · 400 · 401/405 · 409/404/500 · bảng tuyến) · `soi_bang_tuyen` KHỚP **49** tuyến | xanh |
| AC-4 | `nb_le_cua(from,to,thang)` + `test_C10_AC4_*` (đọc riêng, 304 dòng; ⛔ giả làm lưới CDT1); tuyến chỉ trả `nb_le_so_dong` | xanh |
| AC-5 | `lint-imports` 11 kept/0 broken · 0 di trú mới | xanh |

## Số đo (Đ4 — mỗi số một nhãn)
- **238** ô CÓ SỐ = 21 dòng × 12 tháng − 14 ô `GI 202501`; **146** ô thiếu = `NB_LE` 96 + `CMN` 36 + `GI 202501` 14; **34** tổng Σ7 CDT1 = 1 ± 1e-9; **304** dòng `nb_le`.
- ⚠ Ảnh có số ngoài [0,1] thật: lưới CDT1 có nhiễu **−1,1e-15** (phần dư SHQ2) ⇒ cho dung sai ±1e-9; `NB_LE` có **15/3.648** ô ÂM (min −0,2567) ⇒ chỉ đòi số hữu hạn. Bản đầu của tôi đòi [0,1] ⇒ đỏ — sửa theo dữ liệu, ⛔ theo giả định.
- Đếm `mong` hai chiều (Đ5): ô `null` ⇔ có dòng `o_thieu`; thiếu HAY thừa ⇒ `LoiDRV`.

## Sửa bài cũ (cần orchestrator xem)
`test_kho_cau_hinh_pg.py::test_AC5_chua_nap_…` và `test_C5R1_03_…` dùng `IX.DRV` làm bảng mẫu "chưa nạp" ⇒ ĐỎ khi C10 nạp (đường nền lần 1: thêm 2). Cả **11** `bang` hợp lệ nay đều có người nạp (`IX.TMP` = C13) ⇒ ⛔ đổi sang tên thật; dùng `bang` GIẢ `IX.MAU_CHUA_NAP` qua `monkeypatch` `BANG_HOP_LE` (kho ⛔ có `CHECK` miền `bang`). Sức cắn giữ nguyên.

## Sàn Q8 & cổng cuối
`MONG_PYTEST_TOAN_BO` **4490 → 4519** (+29 = `test_driver.py` 14 · `test_driver_pg.py` 6 · `test_isp_config_drv.py` 9) + bài ghim cùng commit; web 690 giữ.
`--duong-nen --cong 5434` (lần chạy cuối): **ĐẠT** — tập đỏ + XFAIL 28 = 28 (thêm 0 · bớt 0), chạy 4519; web 3 = 3, 690. (Lần 1 ĐỎ: +2 bài C5 nói trên; một lần chạy trước đó bị dừng vì giới hạn thời gian của chính tôi, ⛔ kết quả.) `kiem_tai_lieu` ĐẠT · `pg_migrate` (kho test) khớp.

## Ngoài phạm vi
H12 phải đọc lưới qua `driver_cua` thay vì ảnh (vòng sửa H12). NOEM headcount H1000 `A4289:Q4300`: ⛔ trỏ ô cứng — thiếu ⇒ `DRV_THIEU`.
