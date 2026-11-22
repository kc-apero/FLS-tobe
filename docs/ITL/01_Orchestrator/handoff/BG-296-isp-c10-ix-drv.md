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

## Vòng sửa sau R1 (KQ-297) — 0 CHẶN · 2 NÊN SỬA · 4 GHI NHẬN
- **`C10-R1-01` — ĐỎ trước:** `test_C10R1_01_…` ×2 ĐỎ (`AttributeError`: ⛔ có bảng nối; đo gốc `driver_cua("PE",…)` ⇒ `DRV_LA`). **Sửa phía C10** *(orchestrator quyết; ⛔ sửa engine H12)*: `fls/cau_hinh/driver.py` thêm `NOI_TEN_ENGINE = {PE→GI_PE, PM→GI_PM, NOEM→NOEM}` *(`MONG_NOI = 3` tên ENGINE)* · `khoa_kho_cua(ten)` · `driver_cua_theo_luat(bang, luat, cdt1, thang)` *(`luat` = đối tượng có `.driver` hay chính tên engine)*. Tên lạ *(`GI_PE`, `pe`, `XX`, `None`/H1000, rỗng)* ⇒ `LoiDRV(DRV_LA)` CÓ TÊN, ⛔ đoán. Bài: mọi `luat_pb.DRIVER` ≠ `None` *(mẫu số 2: `PE`, `NOEM`)* nối được ⇒ khoá ∈ `LOAI_SO` và số = `driver_cua` trực tiếp; 3/3 tên nối. `ix_alr_2025_bat.json` của H12 **chưa có** trên nhánh làm việc *(grep `git ls-files`: 0)* ⇒ bài quét ảnh ấy để H12 *(`H12-R1-04`: chuyển sang `driver_cua_theo_luat`; dùng `doc_drv` MỘT lần rồi `BangDRV` — `C10-R1-04`)*.
- **`C10-R1-02` — ĐỎ trước:** `test_C10R1_02_…` ĐỎ (`so_o_thieu 0`, rỗng). **Sửa** `xu_ly.cau_hinh_drv`: `?ky=` ngoài năm lưới ⇒ vẫn `200`, mỗi hàng `luoi` có `thang:{ky:null}` + `o_thieu` một dòng/hàng *(21; `?loai=NOEM` ⇒ 7)* `ly_do` "nguồn ⛔ có driver năm 2026 (ảnh DT10 chỉ có 2025)", `o_thieu_theo_ly_do` {lý do: 21}. **Lý do chọn `o_thieu`** *(⛔ mã lỗi)*: cùng khuôn lọc rỗng-có-tên của các tuyến config; ⛔ phá `200` đang có; `?ky=202503` ⇒ ⛔ đổi. Cập nhật dòng §4i `07_API_CONTRACT`.
- **`-03…-06` ⇒ backlog, ⛔ làm:** `-03` (`isdigit` Ả Rập — chờ khuôn `yyyymm` chung C5) · `-04` (dặn H12 dùng `BangDRV` theo lô — đã ghi ở trên) · `-05` (nạp 2026 phải đủ hai năm/tích luỹ) · `-06` (bài mẫu `ChuaKhai` là tên giả; ai nạp `IX.TMP` biết).
- **Sàn Q8:** `4550` *(bản nhánh làm việc; xung đột script + bài ghim ⇒ giữ bản nhánh làm việc)* → **4582** = thu thập thật cây gộp *(4550 + 29 C10 + 3 mới)*, web 690 giữ; bài ghim cùng commit.
