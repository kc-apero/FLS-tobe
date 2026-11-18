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

---

## Vòng sửa sau R1 (KQ-129) — `fls-dev` (phiên cloud con · 2026-11-18)

**Nền:** `isp/DT1BT` @ `5f5d3b4` (ngọn khi giao — gồm commit mã `606ad89` + `KQ-129`/sổ). Orchestrator chốt
R1 `KQ-129`: **0 CHẶN · 6 NÊN SỬA · 3 GHI NHẬN**, người dùng duyệt. Vòng này làm **cả 9** phát hiện.

### Đã sửa (theo quyết của orchestrator)
| Phát hiện | Quyết | Đã làm | Bằng chứng (bài) · ĐỎ-trước |
|---|---|---|---|
| `DT1BT-R1-01` *(rels tuyệt đối ⇒ `xl/xl/…`)* | A: sửa ngay | Thêm `_chuan_dich_rels`: đích **tuyệt đối** (`/xl/…`) bỏ `/` đầu · **tương đối** nối `xl/`. | `test_DT1BT_R1_01_rels_tuyet_doi_va_tuong_doi` (CẢ HAI dạng) · `test_DT1BT_R1_01_chuan_dich_rels_don_vi`. **ĐỎ-trước:** phục bản cũ ⇒ `[rels_tuyet_doi]` ĐỎ (`xl/xl/…` exit 1), `[rels_tuong_doi]` xanh. |
| `DT1BT-R1-02` *(định nghĩa "hàng dữ liệu")* | Cả hai | GIỮ định nghĩa (≥1 ô bất kỳ) · THÊM in **số đếm** `hàng có ≥1 ô khoá / hàng 0 ô khoá` cho SO+L1 (chỉ số, không giá trị) · hướng dẫn owner thêm hàng (d): K11 lệch mà "hàng 0 khoá" > 0 ⇒ dừng, báo hai số. | `test_DT1BT_R1_02_in_so_dem_hang_khoa_khong_lo_gia_tri` (hàng chỉ-công-thức ngoài khoá ⇒ `SO: 1 / 1`; giá trị `FORMULA_SECRET` không lên màn). |
| `DT1BT-R1-03` *(quét giá trị ô đường LỖI)* | NÊN SỬA | Bài quét sentinel cho mọi đường lỗi (XML workbook/worksheet hỏng · zip hỏng · thiếu sheet · thiếu cột · CSV không UTF-8 · CSV có NUL). | `test_DT1BT_R1_03_duong_loi_khong_lo_gia_tri_o` (7 ca). **ĐỎ-trước:** M6 *(câu lỗi nối hàng dữ liệu)* ⇒ `[thieu_cot]` ĐỎ (sentinel lọt) · M14 *(nhánh in giá trị)* ⇒ `[thieu_cot]` ĐỎ. ⇒ M6·M14 nay **CHẾT**. |
| `DT1BT-R1-04` *(tệp hỏng ⇒ một dòng, không Traceback)* | GHI NHẬN, làm | Bọc `ET.fromstring` (`_parse_xml`) · bọc đọc rels KeyError · bọc đọc CSV `UnicodeDecodeError`/`csv.Error` · chặn NUL minh bạch ⇒ `LoiDoc` **một dòng có tên**, mã 1. `UnicodeDecodeError` **không** in byte/vị trí (`from None`, không `str(e)`). | `test_DT1BT_R1_04_tep_hong_mot_dong_khong_traceback` (8 ca: không "Traceback", stderr một dòng, exit 1) · `test_DT1BT_R1_04_unicode_khong_lo_byte_vi_tri`. **ĐỎ-trước:** gỡ `_parse_xml` ⇒ 3 ca XML ĐỎ (Traceback) · in `str(e)` ⇒ unicode ĐỎ (lộ byte). |
| `DT1BT-R1-05` *(ghim đột biến sống)* | GHI NHẬN, làm | Bài ghim M8 *(tiêu đề 2 hàng)* · M12 *(đường ra là thư mục ⇒ exit 2)* · M16 *(khoảng trắng tiêu đề CSV — `strip()` tiêu đề, khai ở đây)*. | `test_DT1BT_R1_05_M8_…` · `_M12_…` · `_M16_…`. **ĐỎ-trước:** `max→min` ⇒ M8 ĐỎ · bỏ chốt thư mục ⇒ M12 ĐỎ · bỏ `.strip()` tiêu đề L1 ⇒ M16 ĐỎ. |
| `DT1BT-R1-06` *(PowerShell `-LiteralPath`)* | NÊN SỬA | Hướng dẫn: **mọi** lệnh chạm đường có `[ ]` dùng `-LiteralPath` (13 chỗ) · thêm **bước (0)**: `Test-Path -LiteralPath $XLSX` ⇒ True + `Resolve-Path -LiteralPath` so tiền tố để biết xlsx trong/ngoài repo. | Hướng dẫn `HUONG_DAN_NHAN_THAT_DT1b.md` v1.1. *(Hành vi PowerShell: không đo được ở container Linux — kiến thức.)* |
| `DT1BT-R1-07` *(dọn tệp thô mọi nhánh)* | NÊN SỬA | `Copy-Item → Move-Item` *(không để bản ở Downloads)* · bước (g) là **lệnh** `Remove-Item -LiteralPath` cho tệp xuất + L1 ở thư mục làm việc + bản Downloads · khung "chạy (g) ở MỌI trường hợp kết thúc, kể cả dừng giữa chừng" + ba dòng kiểm `mong: False/False/0`. | Hướng dẫn v1.1 bước (b) + (g). |
| `DT1BT-R1-08` *(bỏ ký hiệu nội bộ)* | NÊN SỬA | Bỏ **toàn bộ** ký hiệu `⛔` trong hướng dẫn (còn 0) · viết "không"/"đừng" chữ thường · sửa hàng bảng (e) khớp dòng **Mong** ("**không** thấy dòng `✅ đã ghi…` dù exit=4"). | Hướng dẫn v1.1 (`grep -c ⛔` = 0). |
| `DT1BT-R1-09` *(Input_Raw gitignore)* | GHI NHẬN, làm | Thêm `Input_Raw/` vào `.gitignore` (cùng tinh thần `sao_luu/`, `hien_vat/`) + bài `git check-ignore` · hướng dẫn bước (0) nói trong/ngoài repo, bước (f) chỉ đổi `phan_loai_ly_do.json`. | `test_DT1BT_R1_09_input_raw_bi_gitignore`. |

### Tệp đổi (vòng này)
| Tệp | Đổi |
|---|---|
| `tools/xuat_khoa_dt1b.py` | `_chuan_dich_rels` (-01) · `_parse_xml` + bọc rels/CSV + chặn NUL (-04) · `_dem_khoa` + in số đếm hàng-khoá (-02). |
| `tests/du_lieu/test_xuat_khoa_dt1b.py` | +24 bài `DT1BT-R1-01…05` · `-09` (14 → 38). Thêm tham số `rels_ledge_tuyet_doi` cho `_lam_xlsx`. |
| `docs/ITL/03_Dev/isp-3.1/HUONG_DAN_NHAN_THAT_DT1b.md` | v1.1: bước (0), `-LiteralPath`, `Move-Item`, bước (g) lệnh + khung mọi-nhánh, bỏ `⛔`, hàng (e), trong/ngoài repo (-06·-07·-08·-09·-02). |
| `.gitignore` | `Input_Raw/` (-09). |
| `tools/dung_moi_truong_isp.sh` | `MONG_PYTEST_TOAN_BO` 3081 → **3105** (+24 bài). |
| `tests/test_dung_moi_truong_isp.py` | Bài ghim `== ["3081"]` → `== ["3105"]` + narrative. |

### Cổng (cụm PG cổng 5437)
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` | `38 passed` |
| `pytest tests/test_dung_moi_truong_isp.py` | `60 passed` |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(chạy MỘT MÌNH)* | `KẾT: ĐẠT` — toàn bộ `12 failed, 3077 passed, 2 xfailed, 14 errors in 432.16s` · đỏ+XFAIL **28 = 28** node id *(XFAIL 2=2 · thêm 0 · bớt 0)* · chạy **3105** (mong ≥ 3105) · skipped 0 · deselected 0 · web `3 failed, 664 passed` · đỏ **3 = 3** · chạy **667**. (+24 bài mới đều XANH: passed 3053 → 3077.) |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT (245 file, 2291 bang, 778 o ngay, 104 ma QD)` |

### Sàn pytest: cũ → mới
- `MONG_PYTEST_TOAN_BO` **3081 → 3105** (+24 bài) · `MONG_PYTEST_WEB` **667 (không đổi)**. Thu thập (`pytest --collect-only`): **3105**.

### Kho thật
- `KHONG_CHAM` — thuần mã + bài tổng hợp `tmp_path`; không đọc kho · không Drive · không mạng.

### Còn để lại cho vòng/owner sau *(không đo được ở container Linux)*
- `-06`/`-07`: hành vi PowerShell `-LiteralPath`, `Move-Item`, `Remove-Item` là **kiến thức** — cần owner xác nhận trên Windows (container không có `pwsh`).
- `-01`/`-02`: chỉ **đo thật** được khi owner chạy trên `[Master] ITL_Ledge_raw.xlsx` (O10): nhà sinh xlsx thật, và "hàng 0 khoá" thật so với mẫu số 9.967 ở K11.

---

## Vòng sửa sau R2 (KQ-130) — `fls-dev` (phiên cloud con · 2026-11-18)

**Nền:** `isp/DT1BT` @ `29db42b` (ngọn khi giao — gồm vòng sửa R1 + `KQ-130`/sổ v0.2). Orchestrator chốt
R2 `KQ-130`: **0 CHẶN · 3 NÊN SỬA** (`-01` · `-04` · `-05`, đều ở hướng dẫn) · **3 GHI NHẬN** (`-02` · `-03` · `-06`),
người dùng duyệt. Chốt Q1 = A (sửa hướng dẫn) · Q2 = A (sửa mã `-02`+`-03` cùng vòng) · Q3 = A (owner chạy
**sau** khi nhánh này gộp vào nhánh làm việc ⇒ giữ bước (a) `git pull`). Vòng này làm **cả 6** phát hiện R2.

### Đã sửa (theo quyết của orchestrator)
| Phát hiện | Quyết | Đã làm | Bằng chứng (bài) · ĐỎ-trước |
|---|---|---|---|
| `DT1BT-R2-01` *(hướng dẫn chưa nói (0)/(g) chưa thử trên Windows)* | A (NÊN SỬA) | Thêm khung ⚠ đầu hướng dẫn + ghi chú ở (0) và (g): *"(0)/(g) chưa thử trên Windows; chạy thử trước khi chạy thật, khác Mong ⇒ DỪNG, chỉ gửi True/False/số, không gửi nội dung tệp"*. | Hướng dẫn v1.2 (chữ — hành vi PowerShell không đo được ở container Linux). |
| `DT1BT-R2-02` *(rels `xl/`-tiền-tố ⇒ `xl/xl/…`; `../`·`./`·`%20` chưa chuẩn hoá)* | A (GHI NHẬN) | `_chuan_dich_rels`: `unquote` (`%20`) · tiền tố `xl/` sẵn ⇒ ⛔ nối lần nữa · `posixpath.normpath` gộp `./`·`../`·`//`, chặn thoát gốc gói (`..`) ⇒ `LoiDoc`. | `test_DT1BT_R2_02_chuan_dich_rels_dang_ngoai` (7 khẳng định) · `test_DT1BT_R2_02_rels_dang_ngoai_doc_duoc` (3 ca nối: `xl/`-tiền-tố · `./` · `../xl/`). **ĐỎ-trước:** bản cũ nối `xl/` cứng ⇒ 4/4 ĐỎ (đo trước khi sửa: 6 FAILED). |
| `DT1BT-R2-03` *(`zlib.error` luồng nén ⇒ Traceback — lớp lỗi lặp của R1-04)* | A (GHI NHẬN) | Helper `_doc_phan_zip` bọc **mọi** `z.read(phần)` trong `(BadZipFile, zlib.error, EOFError)` ⇒ `LoiDoc` một dòng (workbook · rels · sharedStrings · worksheet). `BadZipFile` xưa chỉ bắt lúc **mở**, nay cả lúc **đọc**. | Ca `zlib_hong` (lật 8 byte giữa luồng nén worksheet) thêm vào `_CA_RORI` (7→8) + `_CA_HONG` (8→9) ⇒ chạy qua `test_DT1BT_R1_03`/`_R1_04`; thêm `test_DT1BT_R2_03_zlib_luong_nen_mot_dong`. **ĐỎ-trước:** `[zlib_hong]` ĐỎ (Traceback `zlib.error: Error -3 … invalid distance too far back`). Thoả gợi ý "quét chung mọi ngoại lệ đọc ⇒ một dòng" qua `_CA_HONG`. |
| `DT1BT-R2-04` *(bước (g) đường tương đối, không `cd` ⇒ xanh giả cửa sổ mới)* | A (NÊN SỬA) | Khai `$REPO` ở *Chuẩn bị*; **mọi** bước mở đầu `Set-Location -LiteralPath $REPO` (tự đủ), đặc biệt (g); (g) thêm `Get-ChildItem -LiteralPath hien_vat` liệt kê còn lại; Mong "False/False/0 + hien_vat không còn khoa_dt1b.csv/l1.csv". | Hướng dẫn v1.2 (`grep -c 'Set-Location -LiteralPath \$REPO'` = 12; bare `cd` = 0). |
| `DT1BT-R2-05` *(cổng (f) viết "Changes to be committed" — không bao giờ có trước `add`)* | A (NÊN SỬA) | Cổng (f) đổi sang `git status --porcelain`, Mong **một dòng** `?? docs/ITL/_tools/phan_loai_ly_do.json` (hoặc ` M` nếu đã theo dõi); nói rõ trước `add` không có "Changes to be committed", tệp ở "Untracked files"/"Changes not staged"; bảng "Nếu thấy" theo dòng porcelain. | Hướng dẫn v1.2. Đo container: `git ls-files` ⇒ json **chưa theo dõi** ⇒ `??`. |
| `DT1BT-R2-06` *(ví dụ Mong tương đối vs thật tuyệt đối · "9.967" vs `9967` · `Move-Item` thiếu `-Force`)* | A (GHI NHẬN) | (c) Mong in **đường đầy đủ** như công cụ (`C:\Users\...\hien_vat\khoa_dt1b.csv`) + chú "chỉ cần `SO 9967 hàng`"; (d) đổi "9.967"→`9967` (công cụ in không dấu chấm); (b) `Move-Item -Force` + hàng "đích đã tồn tại ⇒ chạy (g) rồi làm lại (b)". | Hướng dẫn v1.2. |

### Tệp đổi (vòng này)
| Tệp | Đổi |
|---|---|
| `tools/xuat_khoa_dt1b.py` | `_chuan_dich_rels` chuẩn hoá `unquote`+`normpath`+tiền tố `xl/` (-02) · helper `_doc_phan_zip` bọc đọc zip `(BadZipFile, zlib.error, EOFError)` ở 4 chỗ đọc (-03) · import `posixpath`, `zlib`, `urllib.parse.unquote`. |
| `tests/du_lieu/test_xuat_khoa_dt1b.py` | +7 node: `R2_02` đơn vị + 3 ca nối (thêm tham số `rels_ledge_tgt` cho `_lam_xlsx`) · `_xlsx_lat_byte_nen` + `_ca_zlib_hong` vào `_CA_RORI`/`_CA_HONG` + `R2_03` riêng (38 → 45). |
| `docs/ITL/03_Dev/isp-3.1/HUONG_DAN_NHAN_THAT_DT1b.md` | v1.2: khung chạy thử (0)/(g) (-01) · `$REPO` + `Set-Location` mỗi bước (-04) · cổng (f) `git status --porcelain` (-05) · Mong đường đầy đủ + `9967` + `Move-Item -Force` (-06). |
| `tools/dung_moi_truong_isp.sh` | `MONG_PYTEST_TOAN_BO` 3105 → **3112** (+7 bài). |
| `tests/test_dung_moi_truong_isp.py` | Bài ghim `== ["3105"]` → `== ["3112"]` + narrative vòng R2. |

### Cổng (cụm PG cổng 5437)
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_xuat_khoa_dt1b.py` | `45 passed` |
| `pytest tests/du_lieu/` | `347 passed` (340 → 347, +7) |
| `pytest tests/test_dung_moi_truong_isp.py` | `60 passed` |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(chạy MỘT MÌNH)* | `KẾT: ĐẠT` — toàn bộ `12 failed, 3084 passed, 2 xfailed, 14 errors in 375.55s` · đỏ+XFAIL **28 = 28** node id *(XFAIL 2=2 · thêm 0 · bớt 0)* · chạy **3112** (mong ≥ 3112) · skipped 0 · deselected 0 · web `3 failed, 664 passed` · đỏ **3 = 3** · chạy **667**. (+7 bài mới đều XANH: passed 3077 → 3084.) |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ DAT (246 file, 2303 bảng, 779 ô ngày, 104 mã QĐ)` |

### Sàn pytest: cũ → mới
- `MONG_PYTEST_TOAN_BO` **3105 → 3112** (+7 bài `DT1BT-R2-02` · `-03`) · `MONG_PYTEST_WEB` **667 (không đổi)**.

### Kho thật
- `KHONG_CHAM` — thuần mã + bài tổng hợp `tmp_path`; không đọc kho · không Drive · không mạng.

### ĐỎ-trước (chứng minh Đ5)
- `R2-02`+`R2-03`+bài ghim: trước khi sửa, chạy 6 node R2 trên mã cũ ⇒ **6 FAILED** (3 R2-02 nối + R2-02 đơn vị + R2-03 + `R1_04[zlib_hong]`); bài ghim lùi sàn về 3105 ⇒ **FAILED**, trả 3112 ⇒ XANH. Sau sửa: 45 passed.
