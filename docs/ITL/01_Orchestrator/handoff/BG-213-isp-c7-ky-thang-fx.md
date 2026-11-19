# BG-213 — Bàn giao WO-212 · ISP Step 33 · C7 · IX.FX ký tháng + CHẶN (D1)

| | |
|---|---|
| Phát bởi | fls-dev #CF (phiên cloud) · 2026-11-19 · nhánh `isp/C7` (nền `4a13162`) |
| Gửi | fls-test (R1 → `KQ-214`) |

## Đã làm
- `POST /api/fls/v1/config/fx/{yyyymm}/sign` → **201** `{bang, yyyymm, trang_thai:'da_ky', actor, ky_luc}`. `actor` = `yc.actor` (TỪ THẺ, `the.kiem` → `Nguoi`); `ky_luc` = `now()` của MÁY. Ký lại ⇒ **409 `FLS-CAUHINH-DA-KY`**; tháng ∉ IX.FX hiện hành ⇒ **404**; `yyyymm` hỏng ⇒ **400**.
- Kho: bảng config MỚI `IX.FX · KY` trong `fls_cau_hinh_ban`/`_dong` (`0027`, ⛔ di trú mới). Mỗi lần ký = một **phiên bản mới** chở mọi chữ ký cũ + chữ ký này (chỉ-thêm, cùng khoá advisory như `nap`). Mỗi chữ ký mang `dau_van_tay` = sha256 của 5 tỷ giá lúc ký.
- `fx.fx_cua(yyyymm, bang, da_ky)` **thuần** + `cau_hinh_repo.fx_cua(conn, yyyymm)`: ném `FxChan` (`ma='FX_CHAN'`, câu có tên tháng) khi tháng ∉ IX.FX *(⛔ rơi về tháng gần nhất)* · trùng dòng · chưa ký · **đổi số sau ký**. `yyyymm` hỏng ⇒ `LoiFX`.
- `GET /config/fx`: dòng đã ký có `trang_thai='da_ky'` + `actor` + `ky_luc`; dòng chưa ký ⛔ đổi byte nào.
- Cửa: `Tuyen.http_ok` (mặc định 200 ⇒ tuyến cũ ⛔ đổi; chỉ tuyến ký khai 201) · mã lỗi mới `FLS-CAUHINH-DA-KY` (`bao.MA_LOI` + câu tiếng Việt ở `goi_cua.js`) · `BANG_CO_VET` thêm `fls_cau_hinh_ban` (cổng `AUD-1`: `actor` NOT NULL + `luc` máy + chỉ-thêm).
- `07_API_CONTRACT.md` → v3.22: dòng §4i POST giữ ⬜ + hợp đồng chi tiết + changelog (orchestrator lật ✅ khi gộp).
- Q8: `MONG_PYTEST_TOAN_BO` 3650 → **3659** + bài ghim cùng commit (web giữ 675).

## C7-B1…B6 ↔ bài (`tests/cau_hinh/test_ky_fx_pg.py`, 9 bài, qua MÁY THẬT + kho TEST)
| | Bài |
|---|---|
| B1 | `test_C7_B1_…201_va_GET_thay_da_ky_voi_actor_tu_THE` (mẫu số: trước ký `chua_ky`; tháng khác ⛔ bị lây) |
| B2 | `…B2_ky_lai_409…KHONG_them_dong` (đếm bản ký trước = sau; người đầu giữ) |
| B3 | `…B3_fx_cua_CHAN…THIEU_han_va_hong` (pg) + `…fx_cua_thuan_…TY_GIA_DOI…` (đơn vị) |
| B4 | `…B4_actor_CHI_tu_the…` |
| B5 | `…B5_khong_the_hoac_the_hong_401…` |
| B6 | `…B6_bang_tuyen_POST_khai_bang_ghi…` + `…B6_kho_chi_them_trigger_0027_giu` + `soi_bang_tuyen` |
Chạy lại được: mỗi lần nạp IX.FX với USD ngẫu nhiên ⇒ dấu vân tháng mới (kho chỉ-thêm ⛔ dọn được).

## ⚠ Lệch / quyết định cần R1 soi
1. **AC-4 chữ vs cửa sẵn có.** AC ghi *"actor trong thân bị BỎ QUA"*; cửa **từ chối 400** `actor` trong thân (`cua.py` `_doc_than`, cố ý: "⛔ im lặng bỏ qua"). Giữ cửa: kết quả AC (⛔ actor giả vào kho) đúng và mạnh hơn; bài ghim cả hai nửa (400 + kho ⛔ thêm dòng; trường khác như `nguoi_ky`/`ky_luc` bị bỏ qua).
2. **Sửa cửa sẵn có (AC-5).** Token rác `rac.rac.rac` làm `the.kiem` nổ `UnicodeDecodeError` (không phải `TheKhongHopLe`) ⇒ máy **đứt kết nối, ⛔ 401** — lỗi CÓ SẴN, lộ ra khi đo B5. Sửa 1 dòng: bắt `ValueError` thay `JSONDecodeError`. Bài B5 ghim.
3. **GET `/config/fx` cộng 2 khoá** (`actor`, `ky_luc`) ở dòng đã ký — AC-1 đòi; ghi trong changelog 07 (không phải đổi hợp đồng cũ cho dòng chưa ký).
4. **Dấu vân là thêm của tôi** (WO chỉ nói "phiên bản mới"): chữ ký ⛔ phủ số đã đổi. Hệ quả/giới hạn: nạp lại IX.FX đổi số một tháng đã ký ⇒ tháng ấy `chua_ky` + `fx_cua` CHẶN, nhưng ký lại với số MỚI được *(dấu vân khác ⇒ ⛔ 409; chữ ký mới thay chữ ký cũ trong bản ký kế tiếp)*; **huỷ ký** vẫn ngoài phạm vi.
5. `tests/api/test_mui_thu_luoi.py` ERROR khi chạy riêng lẻ trên kho fls rỗng (cần dữ liệu ngày) — có sẵn, ⛔ liên quan C7 (đường nền so theo `duong_nen_bai_do.txt`).

## Chỗ engine sẽ nối `fx_cua` sau (⛔ nối ở bước này)
- `fls/bao_cao/gl.py:421` `bang_thang = fx.get(thang)` — engine GL nhận dict tỷ giá từ người gọi; nối: người gọi lấy từ `cau_hinh_repo.fx_cua(conn, thang)` thay vì dict dựng sẵn ⇒ tháng chưa ký ⇒ `FxChan`.
- `tools/do_hd2.py:213` `doc_ix_fx` dựng `{yyyymm: {tiền tệ: Decimal}}` từ ảnh `ix_fx.json` — H4…H9/I2 nối khi chuyển sang đọc kho.
- Engine nên bắt `fx.FxChan` (`.thang`, `.ly_do`) và hiện tên tháng; F5 (Step 37) tiêu thụ tuyến POST; C13 (Step 36) dùng cùng khuôn "người ký từ thẻ".

## Đo (cổng)
- `tests/cau_hinh` + `tests/api` + `tests/web/test_goi_cua_phu_het_ma_loi.py`: xanh (trừ mục 5). `soi_bang_tuyen`: ✅ **46** tuyến khớp SQL thật. `lint-imports`: 11 kept · 0 broken. `kiem_tai_lieu`: ✅.
- Đường nền `--duong-nen --cong 5434`: lần 1 ĐỎ **1** (`test_moi_ma_loi_cua_cua_deu_co_cau_tieng_viet` — thiếu câu cho mã mới ⇒ sửa ở `goi_cua.js`); lần 2 **ĐẠT**: tập đỏ + XFAIL = đường nền 28 = 28 (thêm 0 · bớt 0), chạy **3659** (mong ≥ 3659), skipped 0, deselected 0; lint-imports 11/0.
