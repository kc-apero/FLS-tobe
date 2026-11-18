# BG-128 — bàn giao `WO-127`

| | |
|---|---|
| **Thuộc** | `WO-127` — ISP 3.1.2 · Step 5 · DT1b (tiếp): công cụ XUẤT bản đọc khoá + hướng dẫn owner |
| **Phát bởi** | `fls-dev` (làn DATA · phiên cloud Opus 4.8) · 2026-11-18 |
| **Nhận** | `fls-test` — R1 `KQ-129` · R2 `KQ-130` · R3 `KQ-131` |
| **Nền** | nhánh làm việc `claude/bold-galileo-zukpaf` @ `2b15531` (ngọn khi giao) |
| **Commit** | `claude/bold-galileo-zukpaf-isp/DT1BT` @ `606ad89` *(mã+bài+hướng dẫn+Q8 — đã đẩy)* · BG là commit ② kế tiếp |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/xuat_khoa_dt1b.py` *(mới)* | Công cụ XUẤT: đọc `ITL Ledge` (.xlsx) + `Transaction Mapping L1` (.csv) ⇒ CSV 7 cột `bang,dong,so_ct,ps_no,ps_co,tk,tien_te` cho `phan_loai_ly_do.py --khoa`. CHỈ stdlib (`zipfile`+`xml.etree`, ⛔ openpyxl). Cột theo TÊN tiêu đề (⛔ chữ cái cột), `dong` = hàng Excel/sheet, giá trị THÔ. Số CT số xuất NGUYÊN `<v>` (⛔ qua float). ⛔ in giá trị ô · ra `hien_vat/` · từ chối đường ra trong repo mà ⛔ gitignore (R8, fail-đóng). |
| `tests/du_lieu/test_xuat_khoa_dt1b.py` *(mới)* | 14 bài TDD, xlsx/CSV tổng hợp trong `tmp_path` (⛔ dữ liệu thật) — AC-1…AC-4 + ca phá riêng tư + bài nối. |
| `docs/ITL/03_Dev/isp-3.1/HUONG_DAN_NHAN_THAT_DT1b.md` *(mới)* | Hướng dẫn owner (Windows PowerShell, 7 bước a–g chép-dán) chạy lượt nhãn THẬT (O10), gồm bước (g) dọn tệp thô + bảng "nếu thấy … thì …" mỗi bước. |
| `tools/dung_moi_truong_isp.sh` | Q8: `MONG_PYTEST_TOAN_BO` 3067 → 3081 (+14 bài), cùng commit với bài mới. |
| `tests/test_dung_moi_truong_isp.py` | Bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho`: `== ["3067"]` → `== ["3081"]` + nối chuỗi gộp `isp/DT1BT ⇒ 3081`. |

## Cổng *(kết quả nguyên văn — cụm PG cổng 5437; `PG_DSN=…localhost:5437/fls`)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` | `14 passed` |
| `pytest tests/du_lieu/` *(hồi quy thư mục chạm)* | `316 passed` *(0 lệch so đường nền toàn bộ)* |
| `pytest tests/test_dung_moi_truong_isp.py` | `60 passed` |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` | `KẾT: ĐẠT` — toàn bộ: `12 failed, 3053 passed, 2 xfailed, 14 errors` · đỏ+XFAIL = **28 = 28** đường nền (thêm 0 · bớt 0) · chạy **3081** (mong ≥ 3081) · skipped 0 · deselected 0 · web: `3 failed, 664 passed` · đỏ **3 = 3** · chạy **667** |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT (242 file, 2278 bang, 776 o ngay, 104 ma QD)` |
| `kiem_so_song` · `khop_owner --kiem` · `soi_bang_tuyen` · `kiem_thuyet_minh` · `pg_migrate(schema)` | `⛔ CHƯA CHẠY` — ngoài phạm vi WO-127 (thuần mã + bài tổng hợp, ⛔ chạm kho/tuyến/thuyết minh/schema). Cổng của WO (§Tiêu chí): bài mới + `tests/du_lieu` + `--duong-nen` + `lint-imports` + `kiem_tai_lieu` — đã chạy ở trên. |

## Bằng chứng từng AC *(mọi cổng mới đã chứng minh ĐỎ trước — Đ5)*
| AC | Bằng chứng | ĐỎ-trước |
|---|---|---|
| AC-1 | `test_AC1_xlsx_ra_7_cot_dong_hang_excel_o_tho` (7 cột đúng thứ tự · `dong`=10/11/12 bỏ hàng trống 8·9 · ô thô từng ô · Diễn giải+email biến mất) · `test_AC1_doc_xlsx_ledge_*` · `test_AC1_tim_sheet_theo_ten_*` (decoy `Bìa` đứng trước, cùng 5 tiêu đề) · `test_AC1_thieu_cot_bao_loi_co_ten_ma_khac_0` (exit 1 · stderr `Tài khoản`) · `test_AC1_sheet_sai_ten_bao_loi` | công cụ VẮNG ⇒ 14/14 ĐỎ; PHÁ "số qua float" ⇒ `so_ct` ĐỎ |
| AC-2 | `test_AC2_l1_csv_ra_hang_L1_dong_la_hang_sheet` (`dong`=5/6 hình Sheets · ô thô · Diễn giải bỏ) · `test_AC2_l1_thieu_cot_bao_loi` (exit 1 · `Tài khoản`) | công cụ VẮNG ⇒ ĐỎ |
| AC-3 | `test_AC3_khong_lo_gia_tri_o_stdout_stderr_ca_pha` (9 sentinel ⛔ ra màn, nhưng CÓ trong TỆP RA — ca phá chứng minh phép quét có nghĩa; Diễn giải+email ⛔ cả trong tệp) · `test_AC3_ra_mac_dinh_*` (ra `hien_vat/khoa_dt1b.csv`) · `test_AC3_tu_choi_duong_ra_trong_repo_khong_gitignore` (exit 2 · `TỪ CHỐI` · tệp ⛔ tạo) · `test_AC3_dau_vao_vang_ma_2` | PHÁ "in giá trị ô" ⇒ bài quét ĐỎ; PHÁ "tắt R8" ⇒ bài từ chối ĐỎ |
| AC-4 | `test_AC4_so_ct_so_va_khoa_hoc_gop_cung_khoa` (SO số `4366190000000000` ↔ L1 `4.36619E+15` ⇒ CÙNG khoá qua `phan_loai_ly_do.doc_khoa`; bốn trường còn lại viết khác dạng) · `test_AC4_xuat_roi_phan_loai_chay_duoc` (end-to-end exit ∈ {1,3,4} · ⛔ Traceback) | công cụ VẮNG ⇒ ĐỎ; PHÁ "số qua float" ⇒ nối ĐỎ |
| AC-5 | `HUONG_DAN_NHAN_THAT_DT1b.md` 7 bước PowerShell chép-dán + bước (g) dọn `hien_vat\khoa_dt1b.csv`+`l1.csv`; `kiem_tai_lieu` ĐẠT (K3 bảng · K5 ngày 2026-11-18) | — |
| AC-6 (Q8) | `MONG_PYTEST_TOAN_BO` 3067→3081 + bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho` cùng commit; `--duong-nen` chạy ≥ 3081 | để lại 3067 ⇒ bài ghim ĐỎ (đã chứng minh phá-trả) |

## Kho thật
- `KHONG_CHAM` — thuần mã + bài tổng hợp `tmp_path`; ⛔ đọc kho · ⛔ Drive · ⛔ mạng.

## `--ghi` có ghi ở mã 4 không
- **CÓ** — xác minh TRONG MÃ (⛔ sửa `phan_loai_ly_do.py`): `tools/phan_loai_ly_do.py:716` `if ghi and ma in (DAT, CHUA_GHIM)` với `CHUA_GHIM = 4` (`:145`). ⇒ hướng dẫn owner bước (e) chạy `--ghi` ở mã 4 ghi được `docs/ITL/_tools/phan_loai_ly_do.json`.

## Sàn pytest: cũ → mới
- `MONG_PYTEST_TOAN_BO` **3067 → 3081** (+14 bài `test_xuat_khoa_dt1b.py`) · `MONG_PYTEST_WEB` **667 (⛔ đổi)**. Thu thập (`pytest --collect-only`): **3081** bài · 225 tệp · web **667**.

## Dev tự thấy còn yếu *(Test soi trước)*
- **Định nghĩa "hàng dữ liệu"** của `doc_xlsx_ledge` = mọi hàng Excel sau hàng tiêu đề có ≥1 ô ⛔ rỗng. Sổ thật nếu có hàng tổng/ghi chú ở đuôi sẽ lọt — nhưng cổng **K11** của `phan_loai_ly_do.py` (tập `dong` = 9.967 `dong_sheet` ảnh 26/08) BẮT ngay, và hướng dẫn owner có nhánh "nếu K11 lệch thì". ⛔ đo được trên tệp THẬT ở container (O10).
- **`--sheet` mặc định `"ITL Ledge"`**: tên sheet thật khác (khoảng trắng thừa…) thì owner phải truyền `--sheet`; câu lỗi in DANH SÁCH tên sheet để chẩn (⛔ giá trị).
- Bài tổng hợp phủ kiểu ô `s`/`inlineStr`/`str`/số (đúng những gì 5 cột khoá dùng) — ⛔ phủ `t="b"`, ngày serial, ô `<v>` dạng khoa học của Excel (hiếm; `canon_ref` vẫn gỡ được nếu gặp).

## Câu hỏi cho orchestrator *(kèm khuyến nghị)*
- **Luồng checkout của owner.** Hướng dẫn bước (a) cho owner `git checkout claude/bold-galileo-zukpaf` (nhánh làm việc) — giả định WO-127 ĐÃ gộp vào nhánh ấy trước khi owner chạy. **Khuyến nghị A (mặc định đã viết):** owner chạy SAU khi R1/R2/R3 ĐẠT + orchestrator gộp `…-isp/DT1BT` vào nhánh làm việc. **B:** nếu owner cần chạy TRƯỚC gộp, sửa bước (a) sang `git checkout claude/bold-galileo-zukpaf-isp/DT1BT`. Chọn A/B?
