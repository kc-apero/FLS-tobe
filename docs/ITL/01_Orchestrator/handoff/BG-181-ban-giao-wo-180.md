# BG-181 — Bàn giao WO-180 · ISP Step 25 · C11 IX.ALR

| | |
|---|---|
| Phát bởi | fls-dev BE-CF · 2026-11-18 · nhánh `isp/C11` (nền `a1b2444`) |
| Gửi | fls-test (R1) |

## Đã làm
`fls/cau_hinh/luat_pb.py` (lõi kiểm thuần: `kiem` · `dung_tu_mm` · `BangALR.luat_cua(hd, ky, cdt1=)`) · `nap_ix_alr`/`doc_alr` (`cau_hinh_repo.py`, khoá kho `hd@tu_ky`) · `GET /api/fls/v1/config/alr` (`cau_hinh_alr`, bảng tuyến → 45 tuyến-đo, soi KHỚP SQL). ⛔ di trú mới · ⛔ tuyến bật cờ · ⛔ sửa `07_API_CONTRACT.md`/TIEN_DO/WO.

## AC ↔ bài · ĐỎ trước
Lệnh đỏ: `pytest tests/cau_hinh/test_luat_pb.py tests/cau_hinh/test_luat_pb_pg.py tests/api/test_isp_config_alr.py` (PG 5434) ⇒ **exit 2**, `ImportError: cannot import name 'luat_pb' from 'fls.cau_hinh'` — đỏ vì THIẾU module (⛔ cú pháp/setup). Sau cài đặt: **54 passed** (+ `test_kho_cau_hinh_pg.py` 72 xanh cùng lượt).

| AC | Bài | Kết |
|---|---|---|
| C11-B1 | `test_luat_pb_pg.py::test_C11_B1_nap_17_luat_4_8_5_H1000_khong_qua_allocate_100pct_bat_false` (+ đơn vị `…_17_luat_4_8_5…`, `…_PM_H1000_mang_khong_qua_allocate_Q3`, đếm `mong` hai chiều ×4, D2 `bat`≠False ×5) · tuyến `test_isp_config_alr.py` | xanh |
| C11-B2 | `test_luat_pb.py::test_C11_B2_OFR_cua_CAH_khong_by_NOEM` (+ CDT1 khác · thiếu cdt1 ⇒ `CAN_CDT1` · HD NOEM khác) · `test_luat_pb_pg.py::test_C11_B2_B3_tren_kho_THAT…` | xanh |
| C11-B3 | `test_luat_pb.py::test_C11_B3_by_GI_driver_la_PE` | xanh |
Lỗi có tên ↔ bài: `ALR_HONG` · `KY_HONG` (7 ca) · `CAN_CDT1` · `BanHong` (SQL tay) · 409/404/500 tuyến.

## Số đo (Đ4 — mỗi số một nhãn)
- **21** mã có `method_cfa2` (By GI 8 · By NOEM 5 · H1000 Ledger 4 · GI/OMC/PS/SC Ledger 1+1+1+1) ⇒ **17** là HD CÓ LUẬT; 4 `X Ledger` = sổ nền tảng, ⛔ luật. **2** mã `need` mà `method` rỗng ⇒ ⛔ luật (bẫy `VLOOKUP` còn nguyên: ô rỗng hiện `0`, có bài ghim).
- Đ3: bảng `fls_mapping_master` ở cụm đo **0 dòng** ⇒ nguồn nạp = ảnh DT3 `mapping_master_cfg.json` (đường truyền vào), mẫu số 17 ≠ 0.
- Ảnh ⛔ mang ngày hiệu lực ⇒ `tu_ky` là THAM SỐ khai ở lúc nạp (⛔ gõ cứng).

## Quyết định cần orchestrator xem
1. Hiểu "17 HD = 4+8+5": 4 `H1000 Ledger` (PM, Q3 `khong_qua_allocate`) + 8 By GI + 5 By NOEM; 4 `X Ledger` ngoài. Khuyến nghị: giữ.
2. `luat_cua(hd, ky)` thêm `cdt1=` keyword: HD có ngoại lệ (OFR×CAH, AP §3.2.5) mà ⛔ khai cdt1 ⇒ `CAN_CDT1`, ⛔ đoán By NOEM. OFR của CAH trả `phuong_phap=None`, `ngoai_le="CAH"`. Khuyến nghị: giữ.
3. Sửa **một bài cũ** `test_C5R1_05` (`test_kho_cau_hinh_pg.py`): bảng mẫu `IX.ALR` → `IX.TMP` (hợp lệ, chưa kiểm riêng; grep `tests/`+`fls/`+`tools/` ngoài danh mục: 0 dòng). Sức cắn `khong_doi` so bản ĐẦU giữ nguyên.

## Sàn Q8 & cổng cuối
`MONG_PYTEST_TOAN_BO` **3466 → 3520** (+54) + bài ghim cùng commit; web 675 giữ.
`--duong-nen --cong 5434` (một lần): **ĐẠT** — tập đỏ + XFAIL 28 = 28 (thêm 0 · bớt 0), chạy 3520 · web 3 = 3, 675. `lint-imports` 11 kept/0 broken · `soi_bang_tuyen` KHỚP 45 tuyến · `kiem_tai_lieu` ĐẠT.

## Vòng sửa sau R1 (KQ-182)
R1 = 0 CHẶN · 1 NÊN SỬA · 2 GHI NHẬN; người dùng đã duyệt sửa. Bài ĐỎ trước, XANH sau.
- **`C11-R1-01` (NÊN SỬA) — ĐÃ SỬA.** `nap_ix_alr` nay TÍCH LUỸ: bản mới = dòng bản liền trước + dòng lần này (cùng `hd@tu_ky` ⇒ bản mới thắng, ⛔ nhân đôi). Kho vẫn chỉ-thêm, ⛔ di trú. Bản liền trước đọc KHÔNG ra *(SQL tay)* ⇒ ⛔ chở theo, bản tốt kế tiếp thắng. Bài `test_C11_R1_01_hieu_luc_TICH_LUY_…` đi qua `nap` 2 lần *(202501 → 202507)*: đỏ trước đúng kịch bản R1 *(`tu_ky` chỉ còn `{202507}`)*; xanh sau: `luat_cua("LC", 202503)` = bản 202501, `("LC", 202508)` = bản 202507, 34 dòng *(17 HD × 2 mốc)*.
- **`C11-R1-03` (GHI NHẬN, làm kèm) — ĐÃ SỬA.** `cdt1` rỗng/khoảng trắng = THIẾU ⇒ `CAN_CDT1`; `kiem` từ chối `ngoai_le` ≠ [] ở HD ngoài `NGOAI_LE_AP` *(chỉ `OFR`)* — lỗi có tên. 9 bài mới, 7 ca đỏ trước.
- **`C11-R1-02` (GHI NHẬN) — ⇒ backlog** *(Scope "ghi chú ATL B2:C4": orchestrator bỏ hoặc giao bước sau)*.
- **Sàn Q8:** `MONG_PYTEST_TOAN_BO` **3520 → 3530** (+10 = 9 `test_luat_pb.py` + 1 `test_luat_pb_pg.py`) + bài ghim cùng commit; web 675 giữ.
- **Cổng:** `--duong-nen --cong 5434` (một lần): **ĐẠT** — tập đỏ + XFAIL 28 = 28 (thêm 0 · bớt 0), chạy 3530; web 3 = 3, 675. `lint-imports` 11 kept/0 broken.
