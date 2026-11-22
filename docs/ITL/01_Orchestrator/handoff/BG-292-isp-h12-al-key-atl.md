# BG-292 — bàn giao `WO-291` *(ISP 3.1.2 · Step 42 · H12 — AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2), cổng WP-C5a)*

| | |
|---|---|
| **Thuộc** | `WO-291` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5434** · 2026-11-22 |
| **Nhận** | `fls-test` *(R1 → `KQ-293`, R2 cuối → `KQ-294`)* |
| **Commit** | `isp/H12` ⇒ `claude/bold-galileo-zukpaf-isp/H12` · gộp H8 `ac8ca80` · ① mã + bài + tệp sinh lại ``4f076c9`` · ② BG này |
| **Nền** | `b9d3e46` *(có `WO-291`)* + gộp cục bộ `…-isp/H8` @ `518ea28` *(tăng tốc ③)* — xung đột CHỈ ở sàn *(`tools/dung_moi_truong_isp.sh` + bài ghim)* ⇒ bản nhánh làm việc rồi đặt = thu thập thật cây gộp **4525**; `hd2_cong.json`/`do_hd2.py`/bài gates tự gộp *(⛔ xung đột)*; H8 ⛔ chạm ảnh `dau_vao` DT7b *(0 tệp `tests/fixture/` trong diff gộp)* |

## Kết luận một dòng
**WP-C5a ĐẠT**: **39.843/45.674** ô ATL khớp *(khớp THẬT **5.932/11.763** ô có số · **33.911** ô `0 = 0`)* + **5.831** lệch có chủ đích — **toàn bộ là lệch của AS-IS** · **0** lệch FLS *(ngoài tên)* · `khong_so_duoc` **154** · `atol 1e-12`, `rtol 0`. `/gates`: `HD2_WP_C5A` = `true`, cha `HD2_WP_C5` = `1/1 gói con` *(trước: `null`)*. H12-B1: cờ TẮT ⇒ **50.616/50.616** ô = PLA3 H8 *(đồng nhất từng ô, ⛔ dung sai)*.

## ⚠ Errata v3.1.3 — ATL ⛔ phải "đáp án khi cờ TẮT" *(đo, SA chỉ-đọc `FORMULA` 22/11, `B5:BK1110`)*
`WO-291` + `BG-197` ghi *"AS-IS CHƯA phân bổ (N1 'Cần add Formula Allocate') ⇒ ATL = đáp án khi cờ TẮT"*. **Sai cho 2025**: ô tháng 2025 của 6 khối CDT đã có công thức phân bổ:
| Lớp công thức AS-IS *(đếm ô THÁNG, 36 cột × hàng)* | Ô | Mã |
|---|---|---|
| By GI — `iferror(sumifs(GROUP)×(GI khối / GI GROUP))` | **576** = 8 × 6 × 12 | LC BRC CXP OSF FNS CIO CXB CXO |
| By NOEM — `…×INDEX('[H1.2026][2025]H1000 I HR Report'!…)` | **348** = (5 × 5 + 4) × 12 | BON HCC OFR OGA REC *(CAH ⛔ OFR — ngoại lệ AP §3.2.5)* |
| `GI` khối CDT lấy `CFA2 \| MID 3 \| GI Platform Data Ledger` *(⛔ PLA3)* | **66** = 6 × 11 | GI |
| GROUP `OMC` 2025-02 = `'…PM + HR'!AH12-0.5` *(gõ tay)* | 1 | OMC |
| SGO1 hàng `DC` = PLA3 `+ 'Allocation Table \| NB \| By LE'!…*-1` | 12 | DC |

Đúng tập mã IX.ALR của C11 *(By GI 8 · By NOEM 5)* ⇒ **AS-IS ĐÃ BẬT phân bổ 2025**. FLS giữ cờ TẮT *(D2 — owner ký mới bật)* ⇒ các ô này + mọi ô lan *(Y/H/Q · cây · KPI · NPC hậu tố · dư SHQ2)* khai **lệch AS-IS có tên** *(⛔ chép công thức AS-IS vào engine)*.
Bằng chứng DƯƠNG *(Đ2/Đ3)*: ở **4.932** ô lớp 2025, đáp án 419 *(H8, 20/11)* = engine **4.932/4.932** ⇒ PLA3 đúng, chỉ ATL khác PLA3; ở **675** ô lớp 2024, đáp án 419 cũng ≠ engine — đúng lớp `as_is_truoc_CA` của H8.

## Đầu vào *(⛔ vòng tròn)*
- **PLA3 PM+HR Y/H/Q/M** = `pla.pla_yhqm` của H8 trên ảnh đầu vào DT7b *(`do_hd2_c3d.tinh_luoi`: `gl_pl_dau_vao.json` + `hr_pl_dau_vao.json`; IX.PER từ kho)* — **12 khối × 74 mã × 57 kỳ = 50.616 ô**.
- **Cờ** = `IX.ALR` **ĐỌC TỪ KHO** *(`cau_hinh_repo.doc_alr`, C11; kho test nạp `nap_ix_alr(mapping_master_cfg.json, tu_ky=202410)`, actor `bai-h12`)* — 17 luật, mọi `bat = False`. Kho thiếu ⇒ ĐỎ có tên *(`IX.ALR ⛔ đọc được từ kho: ChuaKhai`)*.
- **Driver** = ảnh `ix_drv.json` *(DT10 — 238 ô số + 146 ô thiếu có tên)*. ⚠ **C10 ⛔ có trong cây** *(grep `IX.DRV` ở `fls/`: 2 tệp — danh sách bảng + docstring; `git log --all` "C10": 0)* ⇒ lưới driver dựng từ ảnh ở tầng gọi *(`do_hd2_c5a.luoi_driver_tu_anh`)*; engine nhận `LuoiDriver`. Cờ TẮT ⇒ driver ⛔ dùng.
- Đáp án `atl.json` chỉ ĐỌC ở bước so *(bài `test_AC4_dap_an_khong_vao_engine`: xoá mọi giá trị ATL ⇒ lưới engine y nguyên)*. Khoá hàng ATL → (khối, mã) dựng từ CHÍNH ảnh ATL *(khối mở ở mỗi hàng `GI`; thứ tự `KHOI_12`)* — trùng `dong_sheet` của ảnh 419 **817/817** hàng.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/phan_bo_khoa.py` *(mới)* | `phan_bo_khoa(kq, alr, cay, ct, khoi_nguon, khoi_cdt, khoi_du, driver)`: cờ = `alr.luat_cua(mã, tháng, cdt1=khối)` *(⛔ mã HD nào gõ cứng — bài grep)*; ⛔ ô chia ⇒ trả bản sao `o` *(đồng nhất)*; chia = GROUP × driver, Y/H/Q = Σ tháng, dư SHQ2 = GROUP − Σ 6 CDT, tong/kpi = `pla.danh_gia` *(dùng lại)*. Lỗi CÓ TÊN `LUAT_THIEU` · `DRIVER_THIEU` *(MỌI ô thiếu + lý do bảng `o_thieu`)* · `KY_LA`. Q3: H1000 ⛔ qua ALLOCATE; ngoại lệ AP ⇒ giữ nguyên |
| `tools/do_hd2_c5a.py` · `tools/do_hd2_c5a_mong.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C5a [--dsn]`; `MONG` khai TRƯỚC *(mẫu số + 2 lớp quy tắc đếm theo khối + sha256 + 224 ô từng ô theo giá trị)*; tham chiếu 604 |
| `docs/ITL/_tools/hd2_cong.json` | khối `WP-C5a`, sinh bằng `do_hd2.py --goi WP-C5a --dsn $PG_DSN_TEST --ghi` *(343 dòng THÊM, 0 dòng xoá — khối cũ nguyên)* |
| `tests/bao_cao/test_phan_bo_khoa.py` *(14)* · `tests/oracle/test_do_hd2_c5a.py` *(17)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | 11 → **12** cổng; `HD2_WP_C5` `null` → `true`; `HD2_WP_C5A` **5.831** lệch có chủ đích; `chua_do_duoc` giảm 4 |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 4481 → **4525** *(gộp H8, = thu thập)* → **4556** *(+31)*, cùng commit |

## Số đo WP-C5a *(Đ4 — mỗi số nói nó đếm gì · `mong` khai TRƯỚC ở `tools/do_hd2_c5a_mong.py`)*
- **Hàng**: ATL 829 = **817** hàng có nhãn + **12** hàng ⛔ nhãn *(hàng con trống dưới `CDC`; **7** ô ≠ 0 — đếm `hang_khong_nhan_khac_0`, ⛔ so)*.
- **`tong_o` 45.674** = ô so *(817 hàng × 57 kỳ, bỏ mã `trong` **741** ô, bỏ ô ⛔ là số **154** — `#N/A`/`#VALUE!` của `y2024_y`/`q1…q4`)* = `o_co_so` **11.763** + `o_0_0` **33.911**.
- **`khop` 39.843** = `khop_co_so` **5.932** + `o_0_0` · `lech_co_chu_dich` **5.831** = mong · `lech_ngoai_ten` **0**. ⚠ Đ4: khớp THẬT chỉ **50,4 %** ô có số — phần còn lại là AS-IS bật phân bổ, ⛔ "gần khớp".
- Dung sai: max|lệch| ô khớp **1,1e-14** ⇒ `atol 1e-12` *(≥ ×88)*.
- **Tham chiếu 604**: `pd604_ky` *(số CDT1 có số theo driver × tháng)* ↔ lưới IX.DRV **36/36**; 34 tổng Σ7 CDT1 = 1 *(±1e-9)*; 238 ô số + 146 ô thiếu.

**Lệch của AS-IS** *(`lech_co_chu_dich` — Đ5 hai chiều)*:
1. **`as_is_bat_phan_bo_2025` — 4.932 ô**: khối CDT ∪ {SHQ2} × kỳ 2025 *(ASA 642 · CAH 700 · COR 722 · CSM 716 · CVL 720 · SHQ1 722 · SHQ2 710)* + sha256 của (ô, engine, ATL).
2. **`as_is_truoc_CA` — 675 ô**: khối CDT ∪ {SHQ2} × kỳ 2024 *(lan từ H8 — 72 cột 2024 của 416 dán cũ)* + sha256.
3. **`o_lech` — 224 ô khai TỪNG Ô theo giá trị** *(`atol_lech 1e-9`)*: GROUP **96** *(`OMC` −0,5 lan `MAC·CAC·OPC` · KPI · NPC hậu tố dọc mọi kỳ trước)* · SGO1 **128** *(NB by LE hàng `DC` lan `COS·OPC` · KPI · NPC)*.
Quy tắc lớp *(`_lop`)*: khối ∈ CDT ∪ {SHQ2} và năm ∈ {2024, 2025}; ô lệch ngoài ⇒ ngoài tên ⇒ ĐỎ *(2026 ⛔ có lớp)*.

## Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 · H12-B1 | `tests/bao_cao/test_phan_bo_khoa.py` viết TRƯỚC engine ⇒ `ModuleNotFoundError: fls.bao_cao.phan_bo_khoa` *(lỗi thu thập, exit 2)*; đột biến **M2** *(cờ tắt mà xoá khối SGO2)* ⇒ 6 ĐỎ | 50.616/50.616 ô `==` *(⛔ dung sai)*; mẫu số khai trước `12×74×57`, Đ3: lưới có ô ≠ 0; `alr=None` ⇒ `LUAT_THIEU` |
| AC-2 · H12-B2 | 7 ĐỎ lượt đầu *(ô tiền 0 cũng đòi driver ⇒ sửa: tiền nguồn 0 ⇒ ⛔ cần driver, ghi đầu tệp)*; **M1** `PE→GI_PM` ⇒ 6 ĐỎ · **M4** bỏ dư SHQ2 ⇒ 2 ĐỎ | By GI `LC`: mỗi CDT = 100 × driver PE; dư SHQ2 = 100 × driver SHQ2 *(≤1e-12)*; Σ = tiền *(≤1e-12)*; By NOEM + ngoại lệ CAH/OFR; H1000 ⛔ chia; driver thiếu `2025M01` *(lý do "MID3…")* / `2026M01` ⇒ `DRIVER_THIEU` liệt kê **6/6** ô |
| AC-3 | `do_hd2.py --goi WP-C5a` khi kho chưa có IX.PER/IX.ALR ⇒ `KHONG DAT` 2 lý do có tên; `mong {}` ⇒ ĐỎ | `KẾT: DAT`; Đ3 ATL rỗng ⇒ ĐỎ; 6 đột biến `mong` *(tong_o · bỏ 224 ô · khai thừa 1 ô · sha · đếm khối · giá trị 1 ô)* + 604 ⇒ ĐỎ |
| AC-4 | — | +1e-6 lá `SGO2#OFR#2025M05` đầu vào PLA3 ⇒ ĐỎ đúng ô ấy *(+ ô lan, chỉ khối SGO2)*; driver `GI_PE\|COR\|202504` +0,01 ⇒ chỉ `COR` + `SHQ2` kỳ chứa tháng 4 đổi *(+ NPC hậu tố)*, Δ = 0,5 |
| AC-5 | **M3** bỏ kiểm `bat` ⇒ **17** ĐỎ | chỉ mã bật mới chia; hiệu lực theo kỳ *(`tu_ky` 202506)*; grep 14 mã HD trong engine = 0; kho hỏng ⇒ 2 lý do; bật mọi cờ trên dữ liệu thật ⇒ `DRIVER_THIEU` *(2024/2026 ⛔ có driver)* |
| AC-6 | sàn 4481 ≠ thu thập | `MONG_PYTEST_TOAN_BO` = **4556** = thu thập *(xem Cổng)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` *(một mình)* | **`KẾT: ĐẠT`** *(trên `4f076c9`)* — toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4556** *(mong ≥ 4556)* · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy 681; di trú 27/27 · `pg_verify` 0 lệch · kho `fls` rỗng |
| `pytest tests/oracle tests/bao_cao tests/api/test_isp_gates_hd2.py tests/du_lieu/test_dap_an_atl.py tests/cau_hinh` | lần đầu **2 failed** / 1046 passed: `test_luat_pb_pg.py::test_C11_B1…` + `::test_C11_B2_B3…` — Ô NHIỄM THỨ TỰ do bài cổng nạp IX.ALR `tu_ky 202410` *(kho config tích luỹ ⇒ C11 thấy 34 luật)* ⇒ đổi `TU_KY_ALR` = **202501** *(cùng khoá bài C11, ghi lý do ở mã)*; chạy lại `test_do_hd2_c5a.py` TRƯỚC `test_luat_pb_pg.py`: **24 passed**; `hd2_cong.json` sinh lại **y nguyên** byte |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | lần đầu ĐỎ K3 *(dấu `|` trần trong ô bảng BG này — thoát)*; sau: `✅ cong tai lieu DAT — va no da do duoc that (441 file, 2864 bang, 934 o ngay, 104 ma QD)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 48 tuyen` |

## Câu hỏi cho orchestrator / chủ sổ
1. **ATL ⛔ phải đáp án cờ tắt** *(errata trên)*. Cổng hiện khai 4.932 ô AS-IS bật phân bổ là lệch có tên. Muốn parity ở cờ BẬT ⇒ cần: owner ký bật cờ trên dữ liệu thật *(D2)* + C10 *(IX.DRV vào kho)* + đầu vào `GI` khối CDT từ MID3 *(ATL ⛔ dùng driver PE chuẩn hoá mà dùng `GI khối / GI GROUP` — tỉ lệ khác IX.DRV)*. Khuyến nghị: giữ cờ tắt ở H12, mở phiếu riêng nếu muốn parity cờ bật.
2. **C10 ⛔ có trong cây** dù `WO-291` ghi "đã gộp" — xác nhận lại.
3. `−0,5` gõ tay ở GROUP `OMC` 2025-02 và NB by LE ở SGO1 `DC` — chủ sổ xác nhận là điều chỉnh có chủ đích?

## Kho thật
`KHONG_CHAM`. IX.PER + IX.ALR nạp vào **`fls_test`** *(actor `bai-h12`)*. SA đọc `FORMULA` ATL *(chỉ-đọc)* 22/11 — bản thô chỉ ở scratchpad phiên, ⛔ commit.

## Dev tự thấy còn yếu
- Lớp quy tắc khai bằng đếm + sha *(như H8)*: ĐỎ chỉ nói "sha khác" — tái tạo chi tiết bằng `so_sanh_c5a(...).lech`.
- `luoi_driver_tu_anh` đọc ảnh — chờ C10 thay bằng đọc kho.
- Tên bài `test_CG2_B1_tep_that_qua_tuyen_9_cong_dung_dat_C5_null` giữ nguyên *(đổi tên = đổi node id của tập đường nền)*; nội dung nay đòi C5 `true`.
