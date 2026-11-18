# BG-123 — bàn giao `WO-122` *(ISP 3.1.2 · Step 11 · C4)* — cây IX.HD: nạp ảnh ATL + kiểm cha–con + `GET /api/fls/v1/config/hd`

| | |
|---|---|
| **Thuộc** | `WO-122` |
| **Phát bởi** | `fls-dev` *(làn **BE-CF** · phiên cloud · Opus 4.8)* · 2026-11-18 |
| **Nhận** | `fls-test` — R1 `KQ-124` · R2 `KQ-125` · R3 `KQ-126` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/C4` @ `7478e64` *(mã + bài — một commit)*; phiếu này ở commit kế tiếp *(chỉ giấy)*. Đẩy: `origin claude/bold-galileo-zukpaf-isp/C4` |
| **Nền** | ngọn nhánh làm việc `isp/C4` @ **`f1dbd00`** *(đã gộp C1 — khuôn tuyến `/config/fx`; DT3 — ảnh `atl_cay.json` + `mapping_master_cfg.json`, `KQ-121` ĐẠT)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-c4` · cụm PG riêng cổng **5434** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` §1 · §2.1 · **Step 11 · C4** *(8 trường + Substep 1/2)* · Step 2 · C1 *(mẫu tuyến tĩnh)* · AP §3.2.1 IX.HD · §3.2.4 "cây HD theo vị trí dòng" · §3.2.5 · `07_API_CONTRACT.md` §4i *(dòng `GET /config/hd` ⬜ — orchestrator đổi ✅ lúc gộp)* · `CLAUDE.md` Đ1–Đ5 · Bẫy · Riêng tư · `.claude/agents/fls-dev.md` |

## Cổng vào *(`05` §5)*
- git thật: nền `isp/C4` @ `f1dbd00` — đúng ngọn WO giao; cây sạch khi nhận.
- Dựng môi trường bản S0 *(`tools/dung_moi_truong_isp.sh --cong 5434`)* ⇒ **`KẾT: ĐẠT`** *(26/26 di trú · lint-imports 11 kept · HD1 ĐẠT · kho RỖNG)*.
- WO đủ trường §3.1 *(Màn hình: N/A — ⛔ có màn cây trong AP; Dữ liệu: ghi kho THẬT = `KHONG`)*. Câu còn treo: không có. ⇒ ⛔ mở `HOI`.

## Substep 1 — test chọn · kế hoạch · lệnh · giới hạn
- **Test**: C4-B1 *(nạp ATL)* · C4-B2 *(chu trình)* · C4-B3 *(cha vắng + cấp nhảy)* · C4-B4 *(GET)* — phủ mọi dòng mục 8. FE: N/A *(⛔ màn cây trong AP; cây dùng bởi engine H5)*.
- **Tệp**: `fls/cau_hinh/hd.py` · `fls/api/xu_ly.py` · `fls/api/bang_tuyen.py` · `tests/cau_hinh/test_hd.py` · `tests/api/test_isp_config_hd.py` *(+ ảnh tĩnh `fls/cau_hinh/tinh/ix_hd_cay.json` · `ix_mapping_master.json`; + Q8: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py`)*.
- **Lệnh**: `export PG_DSN=…5434/fls PG_DSN_TEST=…5434/fls_test PYTHONUTF8=1` · `python -m pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py`.
- **Giới hạn**: `74 (ATL) ≠ 73 (MM)` ⇒ trả CẢ HAI số + `chenh_mapping_master` *(⛔ hoà giải)*.

## Substep 2 — ĐỎ trước *(đỏ vì THIẾU hành vi — ⛔ lỗi cú pháp/setup)*
- **RED-A** *(module vắng)*: tạm dời `fls/cau_hinh/hd.py` ⇒ `pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py` ⇒ `2 errors in 0.19s` — `ImportError: cannot import name 'hd' from 'fls.cau_hinh'`. Khôi phục.
- **RED-B** *(module có, tuyến chưa nối)*: `pytest tests/api/test_isp_config_hd.py` ⇒ `7 failed, 3 passed` — tuyến `GET /config/hd` chưa có *(IndexError `_tuyen_hd()[0]`, soi ⛔ thấy `cay_hd`, 404…)*; module `tests/cau_hinh/test_hd.py` ⇒ `16 passed` *(hành vi module đã viết)*.
- **XANH** sau khi nối tuyến: `26 passed in 0.81s`.
- Mỗi lỗi cây mới chứng minh ĐỎ bằng ảnh TỔNG HỢP cố ý hỏng *(C4-B2/B3 + mã trùng + vỏ ô)* và `Đ5` chiều kia *(cây/ô đúng ⇒ ⛔ đỏ nhầm)*.

## Cổng *(kết quả nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py` | **26 passed in 0.81s** |
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` *(một mình)* | **KẾT: ĐẠT** · GOC = `…/isp-c4` · toàn bộ `12 failed, 3065 passed, 2 xfailed, 14 errors` ⇒ tập đỏ **28 = 28** node id *(XFAIL 2=2 · thêm 0 · bớt 0)* · chạy **3093** *(mong ≥ 3093)* · skipped 0 · deselected 0; web `3 failed, 664 passed` ⇒ **3 = 3** · chạy **667** *(mong ≥ 667)* |
| `.venv/bin/lint-imports` | **Contracts: 11 kept, 0 broken. (exit 0)** |
| `python tools/soi_bang_tuyen.py` | **✅ ban khai KHOP SQL that o ca 42 tuyen** *(tuyến mới: `TINH ['…/ix_hd_cay.json', '…/ix_mapping_master.json'] · vet 11 ham`)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | **✅ cong tai lieu DAT** *(240 file · 2270 bảng · 776 ô ngày · 104 mã QĐ)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA CHẠY** — công cụ gọi `.venv/Scripts/lint-imports.exe` *(đường Windows)*; container Linux ⇒ `FileNotFoundError`. ⛔ trong danh sách cổng của `WO-122` §5; `lint-imports` đã chạy riêng ở trên *(11 kept)* |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-1 (C4-B1)** | `test_C4_B1_nap_anh_ATL_74_nut_6_nhom_goc_dung_khong_chu_trinh` — 74 nút · 6 nhóm `HDO·HDH·HDAP·HDT·HDC·HDCI` · **37 gốc** *(ảnh ATL là một RỪNG, mọi gốc `cha=null` ở cấp 1)* · ⛔ chu trình *(nạp sạch)*. `test_C4_B1_cap_L1_L4_khop_MONG_CAP_cua_anh` — `dem_cap() == {1:37,2:23,3:11,4:3}` *(bằng chứng DƯƠNG, `Đ3`)*. `test_C4_B1_con_cua_va_la_dung` — `con_cua('OPC')==('CAC','COS')` · `la('GI')/la('OMC')==True` · 64 lá. Nạp qua **đường TRUYỀN VÀO** *(`doc_van_ban(…, nguon=ANH_ATL)`)*. |
| **AC-2 (C4-B2)** | `test_C4_B2_chu_trinh_A_B_A_loi_HD_CHU_TRINH` — ảnh A→B→A ⇒ `HD_CHU_TRINH ∈ e.ten`, **báo đúng 1 lần** *(⛔ một lần mỗi nút)*. `Đ5` chiều kia: ảnh thật ⛔ chu trình. |
| **AC-3 (C4-B3)** | `test_C4_B3_cha_vang_loi_HD_CHA_VANG` — cha trỏ `MATKHONGCO` ⇒ `HD_CHA_VANG ∈ e.ten`. `test_C4_B3_cap_nhay_con_cap_n_cong_2_loi_HD_CAP_NHAY` — con cấp 3 dưới cha cấp 1 ⇒ `HD_CAP_NHAY`. `test_C4_B3_goc_khong_o_cap_1_cung_la_HD_CAP_NHAY` *(cùng bất biến cấp = độ sâu)*. `Đ5`: cây cấp đúng ⇒ xanh. ⭐ **Tên "cấp nhảy" = `HD_CAP_NHAY`** *(hằng chuỗi — khai ở `hd.py`)*. |
| **AC-4 (C4-B4)** | `test_C4_B4_GET_config_hd_200_DUNG_hop_dong` *(máy THẬT)* — `200`; `so_atl=74` · `so_mapping_master=73` · `chenh_mapping_master=['NCF']` *(CẢ HAI số, ⛔ hoà giải)*; 74 nút với `con_cua`/`la` đúng *(`OPC→[CAC,COS]`, `GI` lá)*; 37 gốc; 6 nhóm; `meta.data_status='flash'`. Ảnh đọc qua **đường TRUYỀN VÀO** *(`hd.doc_tep(duong=NGUON_TINH)` · `doc_mm(duong=NGUON_MM)` — tầng 7 ⛔ gõ cứng)*. |
| **AC-5** | `?run_id=` ⇒ **400 FLS-BAD-REQUEST** *(`test_C4_B4_run_id…`, cùng lý do `C1-R1-07`)*; 401 *(⛔ thẻ)* · 405 *(POST)*. Tuyến khai `nguon_tinh=(NGUON_TINH, NGUON_MM)` *(⛔ `bang`)*; `kiem_bang_tuyen()==[]`; `soi_bang_tuyen` ĐẠT *(42 tuyến; `vet` bám `fls.cau_hinh.hd.`)*. `tests/api/test_ba07_phu_het_tuyen.py` xanh *(dòng §4i `/config/hd` đã có)*. |
| **AC-6 (Q8)** | `MONG_PYTEST_TOAN_BO 3067 → 3093` *(+26 bài)* trong `tools/dung_moi_truong_isp.sh` + bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho` + `test_S0_R3_02` *(thu thập = hằng)* **cùng commit**. Web giữ 667. `--duong-nen`: chạy 3093 ≥ 3093 ✅. |

## Gọi tuyến thật *(qua HTTP, máy test)*
- `GET /api/fls/v1/config/hd` ⇒ **200** · `data.so_atl=74` · `data.so_mapping_master=73` · `data.chenh_mapping_master=['NCF']` · `len(data.nut)=74` · `len(data.goc)=37`.
- `GET /api/fls/v1/config/hd?run_id=NAP-2026-01-01-X` ⇒ **400 FLS-BAD-REQUEST** · `data=None`.

## Kho thật
- `KHONG_CHAM` — tuyến TĨNH đọc hai ảnh đi cùng gói *(bị PostgreSQL chặn ghi; `soi` xác nhận SQL 0 bảng)*. Kho config là `C5`.

## Quyết định thiết kế *(để Test soi)*
1. **Ảnh tĩnh = CHÉP ảnh DT3** vào `fls/cau_hinh/tinh/` *(checksum khớp — `test_anh_tinh_goi_KHOP_anh_DT3_tung_byte`)*. Vì sao: luật đường `nguon_tinh` *(`C1-R1-02`)* đòi tệp **NGAY dưới `fls/cau_hinh/tinh/`**; `tests/fixture/` ⛔ qua được. Chép ⛔ sửa DT3 *(ảnh gốc còn nguyên; cả hai PII-safe — ATL `0` trùng, MM đã ẩn danh)*. `C5` GỠ hai tệp.
2. **Tên lỗi phụ** ngoài 3 bắt buộc: `HD_MA_TRUNG` *(khoá cây ⛔ xác định — `json` giữ bản cuối im lặng)* · `HD_HONG` *(vỏ ô/0 nút — `Đ3` ⛔ xanh trên tập rỗng)*. Gom HẾT lý do rồi NỔ một lần.
3. **Checks ĐỘC LẬP**: một nút trong chu trình cũng vấp `HD_CAP_NHAY` *(chu trình ⇒ ⛔ cấp nhất quán)* — `e.ten` là TẬP, bài so `X ∈ ten`.

## Dev tự thấy còn yếu
1. **`kiem_so_song` ⛔ chạy được** trong container Linux *(đường `.venv/Scripts/lint-imports.exe`)* — ⛔ thuộc C4 nhưng Test nên biết: chưa có bằng chứng `kiem_so_song` xanh cho nhánh này. `lint-imports` đã chạy riêng *(11 kept)*.
2. **`cấp = độ sâu`** là diễn giải của tôi về "cấp nhảy": tôi coi *gốc ⛔ ở cấp 1* cũng là `HD_CAP_NHAY`. ISP chỉ nói "con cấp n+2". Nếu owner/BA muốn tách *(gốc-sai-cấp ≠ cấp-nhảy)* ⇒ một tên lỗi thứ tư; tôi chọn gộp vì cùng một bất biến đo được.
3. **Chu trình ⇒ cũng `HD_CAP_NHAY`**: tôi ⛔ nuốt phép này vào phép kia *(mỗi phép một cổng)*, nên một ảnh chu trình trả HAI tên. Có thể gây bất ngờ khi đọc `e.ten`; đã ghim bằng `test_C4_B2` *(so `∈`, ⛔ `==`)*.
4. **`doc_mm` chỉ lấy MÃ** *(tách `'MÃ | Tên'`)*, ⛔ đọc COA/HR *(⛔ việc C4)*. Nếu `hd_code` một dòng MM ⛔ có ` | ` ⇒ mã = cả chuỗi *(đo DT3: 73/73 có ` | ` — hiện ⛔ ca nào)*.
5. Giới hạn kế thừa `C1-R2-03` *(luật `conn` đo MỘT tầng)* ⛔ đổi — tuyến `cay_hd` ⛔ trao `yc` cho hàm phụ nên ⛔ lọt.

## Câu hỏi
- Không có câu CHẶN. *(Khuyến nghị cho mục "Dev tự thấy còn yếu #2": GỘP — một bất biến "cấp = độ sâu" — trừ khi owner cần phân biệt.)*
