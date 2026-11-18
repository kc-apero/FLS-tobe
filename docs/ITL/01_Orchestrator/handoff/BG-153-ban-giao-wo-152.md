# BG-153 — bàn giao `WO-152` (ISP 3.1.2 · Step 17 · C6 · IX.PER)

| | |
|---|---|
| **Thuộc** | `WO-152` |
| **Phát bởi** | `fls-dev` (phiên cloud con) · 2026-11-18 |
| **Nhận** | `fls-test` (R1) |
| **Commit** | `isp/C6` → `claude/bold-galileo-zukpaf-isp/C6` · mã `492eb9e` + sửa sau đường nền *(sha cuối: xem `git ls-remote`)* |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/cau_hinh/ky.py` *(mới)* | `ky_cua` · `chon_luat` · `ngay_ghi_nhan` · `kiem` · `LoiKy{LUAT_CHUA_KY, PER_HONG}` |
| `fls/repo/cau_hinh_repo.py` | `nap_ix_per` · `doc_per` — qua `0027` có sẵn, ⛔ di trú mới; kiểm bằng `ky.kiem` TRƯỚC khi ghi |
| `fls/api/xu_ly.py` · `bang_tuyen.py` · `bao.py` | `GET /config/per` *(`cau_hinh_per`)* · tuyến thứ 43 · mã HTTP `FLS-CAUHINH-LUAT-CHUA-KY` (409) |
| `fls/web/tep/goi_cua.js` | câu tiếng Việt cho mã mới *(cổng `test_goi_cua_phu_het_ma_loi`)* |
| `tests/cau_hinh/test_ky.py` · `tests/api/test_isp_config_per.py` *(mới)* | AC-1…AC-4 |
| `tests/cau_hinh/test_kho_cau_hinh_pg.py` | bài "chưa nạp" dùng `IX.PER` làm mẫu rỗng ⇒ đổi `IX.DRV` *(C6 nạp `IX.PER`)* |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3296 → **3325** cùng commit |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5434` *(một lần, một mình)* | **KẾT: ĐẠT** · toàn bộ 28=28 đỏ nền · chạy 3325 · web 3=3 · chạy 667. *(Lượt đầu ĐỎ do 2 lỗi của tôi — mã `LUAT_CHUA_KY` thiếu câu VN; `IX.PER` làm mẫu rỗng — đã sửa.)* |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | `khớp SQL thật ở cả 43 tuyến` · `OK /config/per` |
| `kiem_tai_lieu.py` | ⛔ **1 lỗi K3 sẵn từ nền**: `TIEN_DO.md:155 cột 4 != 2` — tệp ⛔ được sửa, ⛔ do C6 |
| `kiem_so_song` · `khop_owner` · `kiem_thuyet_minh` · `pytest` đủ ~4 phút ngoài đường nền | ⛔ CHƯA CHẠY *(WO chỉ định bộ trên)* |

## Bằng chứng từng AC *(đỏ-trước)*
Đỏ trước: `pytest tests/cau_hinh/test_ky.py tests/api/test_isp_config_per.py` ⇒ `ImportError: cannot import name 'ky' from 'fls.cau_hinh'` *(2 lỗi thu thập)*.
| AC | Bài · đo |
|---|---|
| AC-1 | `test_ky.py::test_C6_B1_…` ⇒ `2026-11-05` = Y2026·H2·Q4·M11 + 6 ca ranh giới |
| AC-2 | `test_C6_B2_…` ⇒ `2024-12-31` = Y2024·H2·Q4·M12 |
| AC-3 | `test_C6_B3_…` ⇒ luật `B` ⇒ `LoiKy.ma == LUAT_CHUA_KY` *(cả `chon_luat`, `ngay_ghi_nhan`, `kiem`, `nap_ix_per` — nạp bị từ chối ⇒ kho ⛔ đổi)*; A: `2026-03-15` → `2026-03-01` |
| AC-4 | `test_isp_config_per.py` ⇒ `GET /config/per` 200 · `ngay_dau=2024-10-21` · luật A từ KHO · `?run_id=` 400 · 401 · 405 · kho chưa nạp 409 · bản hỏng 500 có tên · `soi` bám `cau_hinh_repo` |
| AC-5 | pin `3325` ĐỎ trước *(2 bài ghim fail khi script còn 3296)* ⇒ xanh sau; `--duong-nen` ĐẠT |

## Kho thật
`KHONG_CHAM` — chỉ cụm cổng 5434 `fls_test`.

## Khác biệt 20/21 *(H5 đối chiếu)*
Ngày đầu là **giá trị cấu hình do người nạp khai** *(bài nạp `2024-10-21` theo ISP)*; mã ⛔ gõ cứng. Errata ㉑: trục CFA1 bắt đầu `2024-10-20`.

## Dev tự thấy còn yếu
- `07_API_CONTRACT.md` ⛔ sửa theo lệnh: dòng `/config/per` + mã `FLS-CAUHINH-LUAT-CHUA-KY` *(409)* chờ orchestrator.
- Mã HTTP đặt `FLS-CAUHINH-LUAT-CHUA-KY` *(khuôn họ `FLS-CAUHINH-*` + cổng web đòi tiền tố `FLS-`)*; tên `LUAT_CHUA_KY` giữ ở `LoiKy.ma` và trong `chi_tiet`.
- Chưa có đường nạp `IX.PER` từ ngoài *(chỉ hàm repo)* — ngoài phạm vi WO.
