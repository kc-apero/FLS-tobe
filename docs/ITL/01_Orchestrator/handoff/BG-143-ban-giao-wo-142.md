# BG-143 — bàn giao `WO-142`

| | |
|---|---|
| **Thuộc** | `WO-142` — ISP 3.1.2 · Step 14 · `C5` *(kho config chỉ-thêm có phiên bản, di trú `0027`)* |
| **Phát bởi** | `fls-dev` *(làn BE-CF · phiên cloud)* · 2026-11-18 |
| **Nhận** | `fls-test` *(R1 · R2 · R3)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/C5` @ `d7e2cd0` *(mã)* · BG commit kế tiếp *(đã đẩy)* |

## Tóm tắt một dòng
Hai tuyến `GET /config/fx` · `GET /config/hd` nay đọc số từ **KHO config chỉ-thêm có
phiên bản** *(di trú `0027`: `fls_cau_hinh_ban` + `fls_cau_hinh_dong`, trigger chặn
`UPDATE`/`DELETE`/`TRUNCATE` có TÊN)* qua `fls/repo/cau_hinh_repo.py` *(chép khuôn
`fls_khai_cot`)*; GỠ ba ảnh tĩnh + mọi tham chiếu; hợp đồng tuyến ⛔ đổi. **AC-8**
*(orchestrator bổ sung, `KQ-125`)*: bịt ba lối exception trơn trong `hd.py` *(cây/MM
hết đóng băng khi đọc từ kho)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/db/migrations/0027_cau_hinh_chi_them.sql` *(mới)* | hai bảng config chỉ-thêm + trigger `BEFORE UPDATE OR DELETE`/`BEFORE TRUNCATE` *(bẫy `0015`)* có TÊN `INV-I08` |
| `fls/db/schema.py` | khai `_FLS_CAU_HINH_BAN`/`_FLS_CAU_HINH_DONG` *(SSOT cho `pg_verify`)*; `CREATE_ORDER` *(cha trước con, trước mọi view)* |
| `fls/db/erd_policy.py` | hai bảng là **đảo** *(⛔ nối `fls_itl`)* ⇒ `ERD_ISLANDS` + `island_reason` |
| `fls/repo/cau_hinh_repo.py` *(mới)* | tầng DUY NHẤT ghi/đọc kho config: `nap`/`_doc_ban` *(generic)* · `nap_ix_fx`/`doc_fx` · `nap_ix_hd`/`doc_hd` · `nap_mapping_master`/`doc_mm`; `BangLa`≠`ChuaKhai`; `khong_doi` theo checksum; `luc` do MÁY |
| `fls/api/xu_ly.py` | `ty_gia`/`cay_hd` đọc KHO *(`yc.conn`)* thay ảnh tĩnh; dịch `ChuaKhai`→409, `BangLa`→404 |
| `fls/api/bang_tuyen.py` | tuyến `/config/fx`·`/config/hd`: `bang=(fls_cau_hinh_ban, fls_cau_hinh_dong)`, GO `nguon_tinh`; `BANG_CHO_PHEP` +2 |
| `fls/api/bao.py` | `MA_LOI` +2: `FLS-CAUHINH-BANG-LA`(404) · `FLS-CAUHINH-CHUA-KHAI`(409) |
| `fls/web/tep/goi_cua.js` | +2 câu tiếng Việt cho hai mã lỗi mới *(cổng `test_moi_ma_loi_cua_cua_deu_co_cau_tieng_viet`)* |
| `fls/cau_hinh/fx.py` | GỠ `NGUON_TINH`/`doc_tep` *(đọc ảnh tĩnh)*; `kiem`/`doc_van_ban` giữ nguyên |
| `fls/cau_hinh/hd.py` | GỠ `NGUON_TINH`/`NGUON_MM`/`doc_tep`/`doc_mm`; **AC-8**: `_so` chặn độ dài trước `int()`, `doc_van_ban`/`doc_mm_van_ban` bắt `ValueError`+`RecursionError`, `_mot_dong` cắt ô dài |
| `tools/sinh_ban_do_tang.py` | `TU_DIEN_THUC_THE` +2 tên nghiệp vụ *(cổng `test_tu_dien_thuc_the`)* |
| `tests/test_ban_do_tang.py` · `test_ban_do_khau.py` | cập nhật đếm thực thể **25→27** · FK **24→25** *(thêm 2 bảng + 1 FK)* |
| `fls/cau_hinh/tinh/ix_fx_mau.json` · `ix_hd_cay.json` · `ix_mapping_master.json` *(xoá)* | AC-6/6b: GỠ ảnh tĩnh |
| `tests/cau_hinh/test_kho_cau_hinh_pg.py` *(mới)* · `tests/db/test_cau_hinh_chi_them_pg.py` *(mới)* | bài kho config *(nạp/đọc/phiên bản/khong_doi/BangLa/ChuaKhai/MM ⛔ bảng phụ)* + trigger chỉ-thêm |
| `tests/api/test_isp_config_fx.py` · `test_isp_config_hd.py` | nạp ảnh DT2/DT3 vào kho; GET đọc kho *(37 dòng/74·73·NCF)*; tuyến khai kho; AC-5 dịch lỗi; GATE `nguon_tinh` chuyển sang tuyến SYNTHETIC |
| `tests/cau_hinh/test_fx.py` · `test_hd.py` · `test_nguon_tinh.py` | gỡ/viết lại các bài đọc ảnh tĩnh *(tiền đề bị `C5` lật)* — giữ nguyên lo qua `kiem`/`doc_van_ban`/`nguon_tinh.giai` *(tmp)* |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3108→3117 *(= `pytest --collect-only`)* + bài ghim |
| ERD-CONTRACT.json/.mmd · ERD-KHAU/TANG.mmd · 05_DATA_DICTIONARY_ERD.md · Ban-do-Kien-truc-7-Tang.html · tests/golden/ddl.sql | hiện vật sinh lại *(máy)* sau khi đổi `schema.py` |

## Cổng *(kết quả nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/cau_hinh/test_kho_cau_hinh_pg.py tests/db/test_cau_hinh_chi_them_pg.py` | `18 passed` |
| `pytest tests/api/test_isp_config_fx.py` | `35 passed` |
| `pytest tests/api/test_isp_config_hd.py` | `10 passed` |
| `pytest tests/cau_hinh` | `133 passed` *(+11 AC-8)* |
| `pytest tests/db` | `250 passed` |
| `pytest tests/test_dung_moi_truong_isp.py` | `60 passed` |
| `--duong-nen` *(một mình)* | `══ KẾT: ĐẠT`. Toàn bộ: `12 failed, 3100 passed, 2 xfailed, 14 errors` · tập đỏ = đường nền `28 = 28 node id (XFAIL 2) · thêm 0 · bớt 0` · chạy **3128** *(mong ≥ 3128)*. tests/web: `3 failed, 664 passed` · nền `3 = 3 · thêm 0 · bớt 0` · chạy 667. **⇒ ⛔ bài nào mới đỏ vì `C5`** *(12+14 đỏ là nền dữ-liệu-thật sẵn có)* |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 42 tuyen` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT` *(K1–K6)* |
| `python tools/kiem_thuyet_minh.py` | `✅ 31/31 nut` |
| `python -m fls.db.pg_migrate` | `da ap 1 migration: [27]` · `pg_verify: khop` |
| `python tools/kiem_so_song.py` · `khop_owner --kiem` | ⛔ **DỮ LIỆU DỰA THẬT** — container cô lập kho RỖNG *(`fls_itl` 0 dòng)* ⇒ nhiều phép đo *"⛔ đo được — sổ RỖNG"*. Đây là nền sẵn có *(⛔ do `C5`)*; xác nhận qua `--duong-nen` *(delta)*. |

## Bằng chứng từng AC
| AC | Bằng chứng | Đỏ-trước |
|---|---|---|
| AC-1 *(C5-B1)* | `test_C5_B1_nap_ix_fx…` + `test_C1_B4_GET_config_fx_200…` ⇒ phiên bản 1 · GET **37 dòng** · `lac=[202306]`. **Đo trên ảnh = ISP** *(37 · 202306)* ⇒ ⛔ dừng | `ImportError: cau_hinh_repo` *(bảng chưa có)* |
| AC-2 *(C5-B2)* | `test_C5_B2_nap_lai_cung_anh…` ⇒ phiên bản +1 · checksum trùng · `khong_doi=True` · 2 bản còn nguyên | — |
| AC-3 *(C5-B3)* | `test_{UPDATE,DELETE}_{ban,dong}_BI_CHAN_co_TEN` + `test_TRUNCATE_BI_CHAN` ⇒ `RaiseException` chứa `INV-I08` + tên bảng | `UndefinedTable: fls_cau_hinh_ban` |
| AC-4 *(C5-B4)* | `test_golden_ddl_khop` *(sau `--update-golden` có chủ đích)* · `pg_verify: khop` · `test_g_erd_1/2/3` xanh · ERD sinh lại | — |
| AC-5 | repo: `test_AC5_chua_nap…`(`ChuaKhai`/409) · `test_AC5_bang_LA…`(`BangLa`/404); handler: `test_AC5_handler_dich_ChuaKhai_409_va_BangLa_404…` ⇒ ⛔ rơi về ảnh tĩnh | — |
| AC-6 | `soi_bang_tuyen` ĐẠT *(tuyến khai `bang` kho)* · `test_C1_B4_bang_tuyen_khai_DUNG_MOT_tuyen_KHO_chi_doc` · `?run_id=` ⇒ 400 *(`test_R1_07…`)* · GỠ `ix_fx_mau.json` + tham chiếu | — |
| AC-6b | `test_AC6b_nap_mm_chi_luu_hd_code_KHONG_bang_phu_tho` ⇒ MM lưu **đúng 73** `hd_code`, ⛔ ô nào của bảng phụ `tho`(84) · GỠ `ix_hd_cay.json`+`ix_mapping_master.json` | — |
| AC-7 *(Q8)* | `MONG_PYTEST_TOAN_BO` **3108→3128** *(cùng commit)* · `test_S0_R3_02_hang_mau_so…` xanh | — |
| AC-8 *(`KQ-125`, orchestrator)* | `test_C4_R2_01_*` ⇒ ô số/JSON dài · lồng sâu ⇒ `LoiHD(HD_HONG)` *(⛔ `ValueError`/`RecursionError`)* · `test_C4_R2_02_*` cắt ô dài trong câu lỗi · `test_C4_R2_03_*` ghim biên `_so` | `ValueError`/`RecursionError` trơn *(đo trực tiếp)* |

## Sàn cũ → mới
- `MONG_PYTEST_TOAN_BO`: **3108 → 3128** *(`MONG_PYTEST_WEB` = 667 ⛔ đổi)*.
- Di trú: **26 → 27** *(0027)*. Bảng/view `pg_verify` *(= thực thể ERD)*: **25 → 27**.
- FK trên bản đồ tầng: **24 → 25** *(`fls_cau_hinh_dong.ban_id`)*. `schema.py` dòng đầu: **18 → 20 bảng** + 7 view.

## Kho thật
- `KHONG_CHAM` — chỉ kho TEST PG *(`fls_test`, cổng 5434)*. `FLS_CHO_GHI_THAT` ⛔ đặt. Kho config chỉ-THÊM *(`INV-I08`)*.

## Hiện vật sinh lại *(máy — CLAUDE.md §Cổng)*
`erd_export --write` → `ERD-CONTRACT.json`/`.mmd`; `sync_erd_doc.py` → `05_DATA_DICTIONARY_ERD.md`; `sinh_ban_do_tang.py` → `ERD-KHAU.mmd`·`ERD-TANG.mmd`·`Ban-do-Kien-truc-7-Tang.html` *(+ bơm TANG/KHAU vào 05_…)*; `pytest tests/db/test_schema_fls_itl.py --update-golden` → `tests/golden/ddl.sql` *(CÓ CHỦ ĐÍCH)*.

## Cách chạy để xem
- N/A — hợp đồng tuyến ⛔ đổi; F4 dùng lại nguyên *(ISP §4 Frontend: N/A)*.

## Dev tự thấy còn yếu
1. **AC-5 qua MÁY THẬT**: 409/404 đo bằng cách **stub ranh giới repo** *(`monkeypatch chc.doc_fx`)*, ⛔ qua HTTP — vì `fls_test` dùng chung đã có `IX.FX`/`IX.HD`, ⛔ dọn được *(kho chỉ-thêm)* để dựng trạng thái RỖNG. Hai loại lỗi đã chứng ở **kho thật** *(`test_AC5_chua_nap`/`test_AC5_bang_LA` trên `IX.PER` chưa nạp)*. Test soi chỗ này.
2. **`thang_dau=202401` TRUYỀN VÀO** `nap_ix_fx` *(⛔ đọc từ ảnh — ảnh DT2 khoá `Month`, ⛔ mang `thang_dau`)*. Là hằng của ảnh DT2 *(cùng khuôn `ix_fx`)*; nếu đổi ảnh thì phải truyền lại. Lưu meta `@thang_dau` trong `fls_cau_hinh_dong` để `doc_fx` dựng lại.
3. **GATE `nguon_tinh`** *(máy canh tuyến tĩnh)* nay ⛔ còn tuyến THẬT dùng — giữ làm **phòng thủ** cho tuyến tĩnh tương lai; các bài đổi sang tuyến SYNTHETIC. Nếu orchestrator muốn GỠ hẳn cơ chế `nguon_tinh` → một `WO` riêng *(ngoài phạm vi C5)*.
4. **`kiem_so_song`/`khop_owner`** ⛔ chạy sạch trong container cô lập *(kho RỖNG)* — ⛔ phải lỗi `C5`; cần kho có dữ liệu để đo thật.
5. **AC-8** nhận từ orchestrator *(`KQ-125`, cross-session)* SAU khi code lõi xong — gộp vào cùng commit `①`. Hằng `_SO_TOI_DA_CHU_SO = 18` *(hd.py)* là chọn phòng thủ *(xa dưới giới hạn 4300 của Python, xa trên cấp 1…n / thứ tự dòng thật)* — ⛔ luật nghiệp vụ; nếu có config số dài hơn thì nâng hằng.
6. **Hồi quy chéo**: thêm 2 bảng ⇒ `--duong-nen` vòng 1 ĐỎ 10 bài đếm/bản-đồ/từ-điển/mã-lỗi; đã bịt hết *(đếm 25→27, FK 24→25, `TU_DIEN_THUC_THE` +2, `goi_cua.js` +2)*. Bài học: một bảng mới chạm **bốn** cổng ngoài schema.

---
_fls-dev · phiên cloud BE-CF_
