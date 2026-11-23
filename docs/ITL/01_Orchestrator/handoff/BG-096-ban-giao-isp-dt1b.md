# BG-096 — bàn giao *(ISP 3.1.2 · Step 5 · DT1b)* — HD1 · gán LÝ DO cho 122 dòng sổ chưa 1-1 bằng khoá đọc ở nguồn *(khoá băm, ⛔ commit giá trị)*

| | |
|---|---|
| **Thuộc** | `WO-095` *(dải phiếu orchestrator cấp; phiếu WO orchestrator ghi sau — spec là ISP Step 5)* |
| **Phát bởi** | `fls-dev` *(làn **DATA**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-097` · R2 `KQ-098` · R3 `KQ-099` |
| **Commit** | nhánh **cục bộ** `isp/DT1B` @ `7b340c2` *(mã + bài thử)* — tách từ nền `2664e25`; ⛔ đẩy theo O2 = A *(orchestrator gộp sau R3)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-dt1b` · cụm PG riêng cổng **5437** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 5 · DT1b** *(`:772`–`:853`, 8 trường + Substep 1/2)* · ISP 3.1.1 `:685` *(nghĩa từng nhãn — 3.1.2 ⛔ khai lại)* · `BG-081` · `KQ-082` · `SO_PHAT_HIEN_ISP-3.1.md` + `SO_PHAT_HIEN_ISP-3.1_DT1a.md` *(cột luật phòng tái phạm — 19 hàng)* · fixture `classifying_vs_canon.json` *(`ghep_bang` · `ban_xuat_lam_hong`)* · `fls/oracle/nguon.py` · `fls/canon/spec.py` · `BA-05` DD-I04 *(cột B·D·E·F·G của `ITL Ledge`)* · `CLAUDE.md` Đ1–Đ5 |

## Quyết định orchestrator áp vào bước này *(LỆCH CHỮ ISP — ghi lại để R1 ⛔ đọc nhầm là lấn phạm vi)*
| # | ISP 3.1.2 ghi | Orchestrator chốt | Ở bước này |
|---|---|---|---|
| 1 | `:788` *"chế độ `--khoa` của tool DT1a … điền `nhan` trong `phan_loai_dong_thieu.json`"* · `:797` · `:824` · `:836` | **Q2 của DT1a = A**: nhãn ra **tệp RIÊNG** `docs/ITL/_tools/phan_loai_ly_do.json`, khoá `dong_sheet` + hai vân tay tập dòng DT1a *(vân tay khác ⇒ ĐỎ)*; công cụ là **tệp MỚI** `tools/phan_loai_ly_do.py` | `tools/phan_loai_dong_thieu.py` · `phan_loai_dong_thieu.json` · bài DT1a: **⛔ chạm** *(`git diff --stat 2664e25` chỉ 2 tệp mới + phiếu này)*. ⚠ Bảng tệp làn DATA *(ISP `:94`)* vẫn ⛔ có `tools/phan_loai_ly_do.py` / `phan_loai_ly_do.json` — đúng `DT1a-R1-08`, cần vá ISP |
| 2 | `:799` "Integrations: Google Sheets RAW qua orchestrator, hoặc tệp xlsx trên máy owner (O10)" | Khoá THẬT ⛔ đọc được ở container (`B-DATA-2`, đo 16/11: RAW gốc `1md85t…` ⇒ Permission denied; bản sao ADJUSTED ⇒ `get_values` hết giờ 60 s — `GAP-ORA-08`) ⇒ bước này dựng công cụ + bài trên dữ liệu **TỔNG HỢP**; lượt THẬT do owner chạy | ⓐ định dạng đầu vào khoá khai ở §Định dạng · ⓑ §Hướng dẫn owner · ⓒ công cụ ⛔ ghi khoá thô — chỉ băm sha256 16 ký tự *(bộ 5 trường)* · ⓓ ⛔ đầu vào ⇒ mã **3** `⛔ CHƯA ĐO ĐƯỢC`. `docs/ITL/_tools/phan_loai_ly_do.json` **⛔ sinh** ở container |
| 3 | *(⛔ có — ISP ⛔ khai khuôn tệp nhãn)* | **HỢP ĐỒNG tệp nhãn** *(orchestrator, giữa phiên — H2 đã bàn giao, `tools/do_voi_so_luong.py` ĐỌC tệp này; khác khuôn ⇒ đỏ lúc gộp)*: `{"van_tay": {"thieu", "nguoc"}, "dong_thieu": [{"dong_sheet": int, "nhan": chuỗi \| null}]}` — khuôn của `phan_loai_dong_thieu.json`; vân tay = tính lại từ ảnh; `dong_sheet` ⛔ `True`; khoá thừa được phép; thêm một bài đọc tệp ra theo đúng khuôn | khuôn đổi *(`dong` → `dong_thieu`, `nguon.van_tay` → `van_tay` gốc)*; phép **K4b** `dong_sheet` int ⛔ bool; bài `…tep_ra_DUNG_KHUON_hop_dong_ma_H2_doc` *(máy đọc RIÊNG của bài)*; **đọc thử bằng chính `_doc_nhan` của H2** — §Đối chiếu H2 |
| 4 | — | công cụ có **chốt riêng tư RIÊNG** cho khoá thô *(Số CT · Diễn giải · email)*, ⛔ dựa `KHOA_CAM` của DT1a | phép **R6** `KHOA_CAM_RIENG` *(tên khoá ở mọi tầng, bỏ dấu)* + R3 email + R5 token Số CT thô + K12 chặn cột `Diễn giải` ở đầu vào — ⛔ import gì từ `tools/phan_loai_dong_thieu.py` *(grep `phan_loai_dong_thieu` trong công cụ: **7** dòng = 5 chú thích/docstring + 2 đường dẫn JSON · **0** `import`)* |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` ở worktree trước khi làm = `2664e25 KQ-082: R1 kiểm BG-081 …` — đúng nền orchestrator giao; nhánh `isp/DT1B`; `git status` sạch.
- version: ISP 3.1.2 *(tệp `IncrementalStepPlan-FLS-Voi_v3.1.2.md`, Step 5 `:772`)*. Run id: ⛔ phiếu nói "đã chạy" ⇒ ⛔ cần.
- `WO-095` chưa có tệp *(orchestrator ghi sau)* ⇒ tôi ⛔ mở `HOI`: phiếu giao của orchestrator có đủ phạm vi · tệp được ghi · cấm · việc; chỗ mơ hồ ghi ở **§Câu hỏi** *(`KHONG_CHAN` cả bốn)*.
- `WO` · `handoff/README.md` · `08_CHANGELOG_RELEASE.md` · Dashboard · `TIEN_DO.md` · ISP: **⛔ chạm** — ngoài danh sách tệp của phiếu giao *(`S0-R1-08`)*.
- Môi trường: sau khi container khởi động lại *(orchestrator báo — cụm 5437 bật lại)* `pg_isready -h localhost -p 5437` ⇒ `accepting connections`; worktree còn nguyên 2 tệp chưa commit.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(mục 6 của Step 5, phủ mọi dòng mục 8)*: `DT1b-B1` → AC-1 · `DT1b-B2` → AC-2 · `DT1b-B3` → AC-3 · `DT1b-B4` → AC-4. FE: **N/A** — bước dữ liệu, đầu ra là tệp nhãn + cổng exit code *(ISP mục 4)*.
2. **Kế hoạch tối thiểu** *(⛔ đụng mã nghiệp vụ, ⛔ đụng kho, ⛔ đụng tool/JSON/bài DT1a)*: `tools/phan_loai_ly_do.py` *(mới — hai chế độ: ĐO `--khoa <bản đọc>` · CỔNG `[--tep <tệp nhãn>]`)* · `tests/du_lieu/test_phan_loai_ly_do.py` *(mới, dữ liệu TỔNG HỢP đủ cỡ thật)* · phiếu này. Chuẩn hoá **mượn** ba hàm công khai đã có *(`canon_ref` · `parse_so` · `ma_tien_te`)* + `la_o_loi` — ⛔ viết bản thứ hai.
3. **Lệnh** *(từ gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5437/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5437/fls_test' PYTHONUTF8=1`)*: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/du_lieu/test_phan_loai_ly_do.py` · `… -m pytest tests/du_lieu` *(hồi quy DT1a)* · `…/python tools/phan_loai_ly_do.py` *(cổng — ở container mong **3**)* · `.venv/bin/lint-imports` · `bash tools/dung_moi_truong_isp.sh --cong 5437 --duong-nen`.
4. **Giới hạn — phần ⛔ đo được ở container** *(nói thẳng)*:
   - **⛔ một nhãn THẬT nào** được gán ở bước này. Mọi con số nhãn trong phiếu là của bản đọc **TỔNG HỢP** do bài thử dựng — chúng chứng minh **công cụ đúng thiết kế**, ⛔ nói gì về 122 dòng thật.
   - `MONG["phan_bo_nhan"] = None` — ⛔ phép đo độc lập nào có trước lượt thật *(Đ1, grep 16/11: ba nhãn `KHONG_CO_SAO_KE`/`KHOA_LECH`/`TRUNG_SEQ` xuất hiện **11** dòng ở **3** tệp ngoài hai tệp mới — ISP 3.1.1 · ISP 3.1.2 · `sinh_isp_voi.py` — **0** dòng mang một con số phân bố)*. Ghim sau lượt thật; tới lúc ấy công cụ trả **4**, ⛔ bao giờ **0**.
   - Thuật toán nhãn là **dựng lại** quy tắc ghép gốc từ một câu của fixture *(`ghep_bang`)* — mã ghép tạo ra 9.845 **⛔ có trong repo** *(`BG-081` §Substep 1.4)*. Cổng **TÁI LẬP** *(K10)* là chỗ đo xem bản dựng lại có khớp mã gốc không — và nó chỉ đo được trên dữ liệu thật.
   - ISP §7 *"bảng nhãn × kỳ dán vào BG"*: bảng dưới là của bản **TỔNG HỢP**; bảng thật đến từ lượt của owner.

## Định dạng đầu vào khoá *(khai ở docstring công cụ — đây là bản chép để owner đọc)*
Một tệp **CSV UTF-8** *(BOM được)*, **hai bảng xếp chồng**, đúng **7 cột** *(thứ tự cột tự do; cột thừa/thiếu/lặp ⇒ ĐỎ — `Diễn giải`, email ⛔ đi cùng được)*:

| Cột | `bang = SO` *(sổ `ITL Ledge` của `Input_Raw/[Master] ITL_Ledge_raw.xlsx`)* | `bang = L1` *(`Transaction Mapping L1` của RAW `1md85t…` — `nguon.py` `BAN_SAO_RAW`)* |
|---|---|---|
| `bang` | `SO` | `L1` |
| `dong` | **số hàng Excel** — CÙNG hệ `dong_sheet` của ảnh 26/08: hàng dữ liệu đầu **10**, cuối **9976**, đủ **9.967** hàng *(công cụ đòi tập này = tập của ảnh — K11)* | số hàng của sheet *(dữ liệu từ hàng 5)* — **chỉ để định danh**, phải khác nhau; ⛔ bao giờ dùng để ghép |
| `so_ct` | cột **B** `Số chứng từ` | cột **B** `Số chứng từ` |
| `ps_no` | cột **E** `PS Nợ` | cột **E** `PS Nợ` |
| `ps_co` | cột **F** `PS Có` | cột **F** `PS Có` |
| `tk` | cột **G** `Tài khoản` | cột **G** `Tài khoản` |
| `tien_te` | cột **D** `Đơn vị tiền tệ` | cột **D** `Đơn vị tiền tệ` |

*(chữ cột: `BA-05` DD-I04 — `ITL Ledge` A–G lấy đúng A–G của `Transaction Mapping L1`; tên trường nguyên văn `fls/canon/spec.py`.)* Giá trị xuất **thô như ô hiện** — công cụ tự chuẩn hoá: Số CT dạng khoa học → trơn *(`canon_ref`)* · tiền `'2,730,128.00'` → `2730128`, trống ≡ `0` *(`parse_so`)* · tiền tệ một tập ký tự trắng + chữ hoa *(`ma_tien_te`)* · ô lỗi Sheets ở cột tiền ⇒ khoá HỎNG ⇒ `KHAC · KHOA_HONG:<cột>`.

## Thuật toán nhãn *(chi tiết + lý do: docstring `tools/phan_loai_ly_do.py:37-49`)*
Khoá k = 5 trường đã chuẩn hoá; ghép gốc = khoá + *"seq trùng"* ⇒ làm theo **nhóm khoá**, ⛔ theo vị trí. Với dòng thiếu d *(o(k) = số dòng sổ ĐÃ ghép mang k)*: ô tiền hỏng ⇒ `KHAC · KHOA_HONG` · L1 có k và còn chỗ ⇒ `KHAC · KHOP_KHI_GHEP_LAI` *(khoá ghép được mà mã gốc ⛔ ghép — ứng viên lớp lỗi MÃ cho H3)* · L1 có k, hết chỗ ⇒ `TRUNG_SEQ` · L1 ⛔ có k nhưng có dòng L1 **chưa ai ghép** trùng Số CT *(≠ rỗng)* hoặc trùng cả bốn trường còn lại ⇒ `KHOA_LECH` + `lech` *(tên các trường khác)* · còn lại ⇒ `KHONG_CO_SAO_KE`. **TÁI LẬP** = Σₖ min(o(k), số dòng L1 của k) phải = **9.845**.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/phan_loai_ly_do.py` *(mới, 657 dòng)* | Chế độ **ĐO** đọc bản đọc khoá *(định dạng đóng)* + JSON DT1a + tập `dong_sheet` của ảnh sổ; chuẩn hoá *(mượn 3 hàm công khai)*; phân loại theo nhóm khoá; băm sha256-16 **cả bộ** khoá; `MONG` khai trong tệp *(122 · 9.967 · 9.845 · hai vân tay — mỗi số trỏ nơi ghi; `phan_bo_nhan = None`)*; in **mẫu số trước tỷ lệ**; ghi **tệp tạm + `os.replace`** chỉ khi ⛔ ĐỎ. Chế độ **CỔNG** kiểm một tệp nhãn đã có *(mặc định tệp của repo)*. **12** phép K *(+ K4b · K5b)* + **6** phép R + phân bố M — mỗi phép trỏ ca phá của nó, K5b khai **phòng thủ chồng** *(docstring `:63-92`)*. Khuôn ra = **hợp đồng H2** *(docstring `:31-35`)*. Mã thoát 0 · 1 · 2 · **3** `⛔ CHƯA ĐO ĐƯỢC` · **4** CHƯA GHIM |
| `tests/du_lieu/test_phan_loai_ly_do.py` *(mới, 667 dòng)* | **48** bài *(22 hàm `def test_`; ca phá tệp nhãn × 24 · sai định dạng × 4 ⇒ 22 − 2 + 28 = 48)*: `DT1b-B1` ×6 · `DT1b-B2` ×3 · `DT1b-B3` ×3 · `DT1b-B4` ×35 · CLI ×1. Bộ dựng `_dung` sinh bản đọc **đủ cỡ thật** *(9.967 dòng sổ trên đúng tập `dong_sheet` thật + 10.185 dòng L1, ⛔ một giá trị thật)*, viết HAI phía KHÁC DẠNG ở mọi dòng ghép, xáo thứ tự L1; nhãn mong đợi của **từng** dòng do bài tự định |
| `docs/ITL/01_Orchestrator/handoff/BG-096-ban-giao-isp-dt1b.md` *(mới)* | phiếu này |

## Cổng *(kết quả nguyên văn — `PG_DSN=…:5437/fls` · `PG_DSN_TEST=…:5437/fls_test` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/du_lieu/test_phan_loai_ly_do.py` | exit 0 · `48 passed in 11.14s` *(trên mã = `7b340c2`)* |
| `python -m pytest tests/du_lieu` *(hồi quy DT1a)* | exit 0 · `64 passed in 11.44s` *(16 DT1a + 48 DT1b)* |
| `bash tools/dung_moi_truong_isp.sh --cong 5437 --duong-nen` — **lượt 1** *(mã TRƯỚC hợp đồng tệp nhãn — 43 bài)* | exit 0 · 7/7 `[ĐẠT]` môi trường · `12 failed, 2491 passed, 2 xfailed, 1 warning, 14 errors in 333.26s (0:05:33)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 180.86s (0:03:00)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` |
| ↳ **lượt 2** *(trên đúng `7b340c2` — 48 bài)* | exit 0 · 7/7 `[ĐẠT]` · `12 failed, 2496 passed, 2 xfailed, 14 errors in 327.94s (0:05:27)` *(mẫu số **2.524** = 12 + 2.496 + 2 + 14; 2.496 = 2.448 nền + 48 bài mới)* · `26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 181.46s (0:03:01)` · `3 = 3` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. Hai bài chập chờn `test_wo032_man_cua_that.py::test_AC3_…/test_AC7_…`: grep `wo032_man_cua_that` trong log = **0** ở **cả hai** lượt ⇒ ⛔ đỏ, ⛔ cần chạy lại. `tests/du_lieu` trong tập đỏ: **0** cả hai lượt |
| `python tools/phan_loai_ly_do.py` *(cổng của bước, tệp repo)* | exit **3** · `⛔ CHƯA ĐO ĐƯỢC — ⛔ có tệp nhãn 'phan_loai_ly_do.json': lượt gán nhãn THẬT chưa chạy (khoá thật chỉ có trên máy owner — O10 · B-DATA-2)` — đúng mong ở container |
| `python tools/do_voi_so_luong.py` *(tiền điều kiện — ảnh fixture ⛔ đổi)* | exit 0 · `Σ          9967   9845    3341    2700  30756  22290    112   13  69510/69510` |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-dt1b/.venv/Scripts/lint-imports.exe'` — đỏ của đường nền *(`DUONG_NEN.md:432`: gọi cứng đường Windows)*; ⛔ do bước này |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (177 file, 1874 bang, 725 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(chạy khi đã có phiếu này — 9 bảng của phiếu nằm trong 1.874)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` · `B3` `B4` `C5` `C5b` *KHONG DO DUOC* · `A1` `B1` `C6` *DOI TRANG THAI* — **trùng khít** đường nền `DUONG_NEN.md:434` *(kho rỗng)*; ⛔ phép nào đọc tệp của bước này |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` *(container: `bin/`, ⛔ `Scripts/*.exe`)* | exit 0 · `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ chạm schema ⇒ ⛔ bắt buộc; chạy: exit 0 · `khong co gi de ap` · `pg_verify: khop` |

## Bằng chứng từng AC *(48 bài PASSED trên `7b340c2`; mọi con số nhãn dưới đây là bản đọc TỔNG HỢP)*
| AC | Mong *(ISP mục 6)* | Bằng chứng *(bài · lệnh · dòng nguyên văn)* | Kết |
|---|---|---|---|
| **AC-1** · `DT1b-B1` | Σ nhãn = 122; mỗi dòng đúng 1 nhãn; bảng đếm nhãn có MONG | `…B1_moi_dong_DUNG_mot_nhan_va_DUNG_thiet_ke_TUNG_dong` — 122 dòng, 122 `dong_sheet` khác nhau = đúng tập DT1a, **từng dòng** `(nhan, lech, ghi_chu)` = thiết kế bộ dựng *(⛔ chỉ tổng — Đ4)*, `dem_nhan` = `{KHONG_CO_SAO_KE 60 · KHOA_LECH 30 · TRUNG_SEQ 20 · KHAC 12}` · `…MONG_khai_TRONG_tool_va_phan_bo_CHUA_GHIM_la_ma_4` *(MONG tool = MONG độc lập của bài; `phan_bo_nhan is None` ⇒ exit **4**, ⛔ `KẾT: ĐẠT`)* · `…MONG_phan_bo_KHAC_thi_DO_va_KHONG_ghi` *(tổng vẫn 122, phân bố 59/13 ⇒ exit 1, ⛔ ghi)* · `…bang_nhan_theo_ky_va_MAU_SO_in_TRUOC_ty_le` *(18 kỳ, kỳ = kỳ DT1a, bảng = đếm lại; `9.967 dòng sổ` · `122 dòng sổ thiếu` · `9.845 dòng ghép` · `10.185 dòng L1` đứng TRƯỚC ký tự `%` đầu)* · `…TAI_LAP_khoa_seq_DUNG_9845_dong_ghep` · `…tep_ra_DUNG_KHUON_hop_dong_ma_H2_doc` *(hợp đồng H2: `van_tay` = `18047e0eb0319ea1`/`6ac2463a190ff631` = bài tự băm tập 122 dòng; `dong_thieu` 122 dòng, `type(dong_sheet) is int`, `nhan` ∈ bảng đóng)*. CLI: `③ nhãn của 122 dòng sổ thiếu (đếm DÒNG): KHONG_CO_SAO_KE 60 · KHOA_LECH 30 · TRUNG_SEQ 20 · KHAC 12` | đạt *(trên tổng hợp)* |
| **AC-2** · `DT1b-B2` | Số CT `4.36619E+15` và tiền `'2,730,128.00'`: chuẩn hoá trước khi băm; khớp bản số thường | `…B2_so_ct_khoa_hoc_va_tien_phan_cach_bam_BANG_ban_so_thuong` — `chuan_hoa_khoa("4.36619E+15", "2,730,128.00", "", "1121", "VND") == chuan_hoa_khoa("4366190000000000", "2730128", "0", "1121", " vnd ") == ("4366190000000000", "2730128", "0", "1121", "VND")`, hai băm bằng nhau, băm THÔ *(bài tự băm)* khác nhau; đổi **một** trường bất kỳ ⇒ băm khác *(5/5)*. `…bo_chuan_hoa_thi_TAI_LAP_roi_va_cong_DO` — thay chuẩn hoá bằng chuỗi thô ⇒ `tái lập …: đo 0 · mong 9845` exit 1 *(đúng bẫy fixture 98,8 % → 16,6 %)*. `…ghep_theo_KHOA_khong_theo_VI_TRI` — hai bản đọc xáo khác nhau *(hạt 7 / 11)* ⇒ `dong` · `dem_nhan` · `nhan_theo_ky` · `mau_so` **bằng nhau** | đạt |
| **AC-3** · `DT1b-B3` | quét tệp ra: 0 Số CT thô · 0 Diễn giải | `…B3_tep_ra_0_so_ct_tho_0_tien_0_dien_giai` — máy quét **riêng của bài**: tập cấm = **≥ 9.967** Số CT thô + dạng trơn của Số CT khoa học + **≥ 9.967** số tiền ≥ 6 chữ số ⇒ giao với token tệp ra = **∅**; khoá tên `dien_giai`/`so_chung_tu`/`so_ct`/`email`: **0** trên ≥ 732 khoá *(Đ3)*; mỗi dòng đúng 6 khoá, `khoa_bam` 16 hex, 122 băm khác nhau. `…B3_dau_vao_mang_cot_Dien_giai_bi_TU_CHOI_va_KHONG_ghi` — một dòng `LOI LoiDauVao: cột của bản đọc ⛔ đúng định dạng đóng …: thừa ['Diễn giải'] …`, exit 1, ⛔ ghi. `…B3_chot_rieng_tu_NOI_vao_duong_do_that` *(luật `DT1a-R1-01`)* — kỳ của dòng thiếu đầu trong **bản sao** JSON DT1a bị thay bằng ① Số CT thô của chính dòng ấy · ② một email ⇒ exit 1, ⛔ ghi, `riêng tư: Số chứng từ của bản đọc lọt vào tệp ra ở …` / `riêng tư: email ở …` | đạt |
| **AC-4** · `DT1b-B4` | phá: gán 2 nhãn cho 1 dòng *(bản sao)* ⇒ ĐỎ rồi trả nguyên | `…B4_hai_nhan_cho_MOT_dong_tren_BAN_SAO_thi_DO_roi_tra_nguyen` — đối chứng 0 → ① `nhan` = danh sách 2 nhãn ⇒ 1 `dòng 744 mang 2 nhãn …` → ② dòng 744 lặp với nhãn khác ⇒ 1 `dòng 744 mang 2 nhãn (dòng lặp 2 lần)` → ③ trả nguyên ⇒ 0. **24** ca phá bản sao khác *(`…moi_bat_bien_cua_tep_nhan_CAN_tren_ban_sao[…]`)* — mỗi ca đối chứng 0 trước, rồi 1 + đúng câu. Vân tay *(cho TỪNG tập — luật `DT1a-R1-02`)*: `…van_tay_DT1a_lech_thi_DO_cho_TUNG_tap`. Thiếu đầu vào: `…thieu_dau_vao_la_CHUA_DO_DUOC_ma_3` *(subprocess: exit **3**, ⛔ `KẾT: ĐẠT`)* · `…tep_nhan_THAT_cua_repo_vang_la_3_co_thi_khong_DO`. CLI thật: xem §Chứng minh ĐỎ | đạt |

## Log ĐỎ → XANH
**① Đỏ thật trước khi có mã** *(`…/python -m pytest tests/du_lieu/test_phan_loai_ly_do.py -rA`)*:
- Lượt 1 *(37 bài)*: `37 failed in 1.30s` · exit 1. Lý do đếm theo dòng `E`: **34** × `AssertionError: ⛔ chưa có tools/phan_loai_ly_do.py — hành vi DT1b chưa có` *(bài trong tiến trình — `_tool()` khẳng định trong THÂN bài ⇒ FAILED, ⛔ ERROR dựng)* · **2** × `assert 2 == 3` *(subprocess: python thoát 2 "can't open file", bài đòi 3)* · **1** × CLI `returncode 2` nhưng **thiếu câu** `--ghi chỉ đi cùng --khoa` *(bẫy DT1a: bài chỉ đòi `== 2` sẽ XANH GIẢ — bài này đòi cả câu)*. `^ERROR ` = **0**.
- Lượt 2 *(thêm 2 ca phá `o_loi_nhung_ma` · `mau_so_khai_lech` cho đủ ca riêng mỗi phép — luật `DT1a-R1-03`)*: `39 failed in 0.97s` — 36 + 2 + 1, cùng lý do.

**② Lần chạy đầu của công cụ**: `24 failed, 15 passed in 13.80s`. Nguyên nhân gốc **một**: câu `khong_mang_PII` của chính công cụ chép nguyên chuỗi `Did not find value` ⇒ phép R4 ĐỎ trên chính bản khai *(`riêng tư: ô lỗi nhúng mã giao dịch ở /khong_mang_PII`)*. Sửa câu khai *(mô tả phép mà ⛔ chép chuỗi kích hoạt — bia ghi ở `tools/phan_loai_ly_do.py:173-174`)* ⇒ `39 passed in 6.27s`.

**③ Đột biến lượt 1** *(46 đột biến trên bản sao `git archive` + 2 tệp, `--noconftest`)*: **41/46** bị bắt; **5 sống** — M15/M16/M17 *(nhãn mang `lech`/`ghi_chu` ⛔ thuộc về nó)* · M27 *(dòng thiếu DT1a ⛔ có phía SO — vẫn ĐỎ nhưng vì `KeyError`, ⛔ câu có tên)* · M43 *(băm chỉ trường đầu)*. Thêm 3 ca phá + 1 bài + 1 vế bài B2; thêm kịch bản *"chung Số CT với dòng L1 ĐÃ có chủ"* *(5/60 dòng `KHONG_CO_SAO_KE`)* để chốt luật chỉ-xét-dòng-L1-chưa-ai-ghép. ⇒ `43 passed in 8.65s`.

**④ HỢP ĐỒNG tệp nhãn** *(orchestrator, giữa phiên)* — bài trước: đổi khuôn trong bài + bài hợp đồng + 2 ca phá *(`dong_sheet_bool` · `khoa_cam_Dien_giai`)* ⇒ `21 failed, 25 passed in 8.64s` *(18 × `KeyError: 'dong_thieu'` · 2 × `KeyError: 'van_tay'` · R6 chưa có ⇒ ca `khoa_cam_Dien_giai` exit 0)* ⇒ sửa công cụ ⇒ `46 passed in 8.70s`.

**⑤ ⚠ ĐÍNH CHÍNH đột biến — máy đột biến của CHÍNH tôi đã đếm sai hai lần** *(R1 nên tự đột biến lại, ⛔ tin số dưới)*:
- Lượt 1 → 4 ghi *"41/46"* rồi *"46/46"* — **sai**: 10 đột biến *(M02–M04 · M11 · M12 · M19 · M22–M25)* thay `so(tên, đo, mong)` bằng `loi.count(tên, đo, mong)` ⇒ `TypeError: count() takes exactly one argument` ⇒ bài đỏ vì **SẬP**, ⛔ vì phép kiểm. Lượt 3 còn nhiễm: tệp nhãn khuôn cũ sót trong bản sao làm bài `…tep_nhan_THAT…` đỏ *(đối chứng sau trả nguyên FAILED — chính đối chứng ấy làm lộ)*.
- Sửa máy: thay bằng `(lambda *a: None)(…)` *(⛔ sập)*, in `⚠ SẬP` khi bài đỏ vì `TypeError`/`NameError`/`SyntaxError`, xoá tệp sót + đối chiếu JSON DT1a bản sao = worktree *(`cmp`)*.
- Lượt 5 *(thật)*: **46/50**, sống M11 · M12 · M22 · M23 ⇒ ca `dem_nhan_lech` đổi thành GIỮ Σ 122 *(KHAC +1 · KHONG_CO_SAO_KE −1)*; thêm `mau_so_khai_thieu` · `mau_so_khai_so`; M12 *(Σ = 122)* ⛔ chứng minh riêng được ⇒ khai **K5b phòng thủ chồng** trong công cụ ⇒ `48 passed in 11.14s`.
- Lượt 6 *(cuối, trên mã = `7b340c2`)*: **49/50 bắt · 0 `⚠ SẬP`** · sống đúng M12 · đối chứng sau trả nguyên `48 passed`.

## Chứng minh ĐỎ
**A. CLI THẬT** *(bản sao `git archive HEAD` + 2 tệp, `cmp` công cụ bản sao ↔ worktree = giống byte; bản đọc tổng hợp 20.152 hàng dữ liệu sinh bằng chính bộ dựng của bài — ⛔ chạm `docs/ITL/_tools/` của worktree)*:

| Kịch bản | Lệnh | Kết quả nguyên văn |
|---|---|---|
| ⓪ tệp nhãn vắng | `phan_loai_ly_do.py` | `⛔ CHƯA ĐO ĐƯỢC — ⛔ có tệp nhãn 'phan_loai_ly_do.json': lượt gán nhãn THẬT chưa chạy …` · `exit=3` |
| ① bản đọc vắng | `--khoa …/khong_co.csv` | `⛔ CHƯA ĐO ĐƯỢC — ⛔ có bản đọc khoá 'khong_co.csv' …` · `exit=3` |
| ② sai cách gọi | `--ghi` | `⛔ TỪ CHỐI: --ghi chỉ đi cùng --khoa …` · `exit=2` |
| ③ đo + ghi | `--khoa ban_doc_tong_hop.csv --ghi` | `② tái lập khoá+seq: 9.845 / 9.845 dòng ghép DT1a = 100,00 % …` · `KẾT: ĐO ĐƯỢC — ⛔ CHƯA GHIM MONG phân bố nhãn (mã 4, ⛔ phải ĐẠT) …` · `✅ đã ghi phan_loai_ly_do.json (mã 4)` · `exit=4` |
| ④ đối chứng cổng | `--tep <tệp vừa ghi>` | `exit=4` |
| ⑤ **2 nhãn cho 1 dòng** | dòng `744` `KHONG_CO_SAO_KE` → `[KHONG_CO_SAO_KE, KHAC]` | `⛔ PHÂN LOẠI LÝ DO ĐỎ — 3 chỗ khác MONG (⛔ ghi JSON):` · `dòng 744 mang 2 nhãn ['KHONG_CO_SAO_KE', 'KHAC'] — mỗi dòng ĐÚNG một` · `exit=1` |
| ⑥ trả nguyên | chép lại tệp gốc | `exit=4` |
| ⑦ **vân tay lệch** | bản sao JSON DT1a: `dong_thieu[0].dong_sheet 744 → 10` *(tổng vẫn 122)* | `vân tay tập thiếu của DT1a (sha256 của 122 dong_sheet đã sắp): đo '91987d4c0009289f' · mong '18047e0eb0319ea1'` · `vân tay ghi trong tệp nhãn (van_tay): …` · `tái lập …: đo 9844 · mong 9845` · `exit=1` |
| ⑧ trả nguyên | chép lại JSON DT1a | `exit=4` · sha256 bản sao trước = sau `df7facae8ea6f035` |

**B. Đột biến công cụ** *(50 — mỗi phép K/R/M + các luật chuẩn hoá/phân loại + hợp đồng; kịch bản `scratchpad/data_dt1b/dot_bien.py`, ngoài repo; xem đính chính §Log ⑤)*: lượt cuối **49/50 bắt, 0 sập** — sống **M12** = K5b *(khai phòng thủ chồng)*. Bắt: K1–K12 *(M02–M11 · M13–M27)* · R1–R5 *(M01 · M28–M31)* · R6 *(M47)* · K4b *(M48)* · khuôn hợp đồng *(M49 `van_tay` đổi tên · M50 `dong_thieu` → `dong`)* · M *(M32)* · ghi khi ĐỎ *(M33)* · Số CT ⛔ `canon_ref` *(M34)* · trống ≢ 0 *(M35)* · đảo `TRUNG_SEQ`↔`KHOP` *(M36)* · `KHOA_LECH` xét mọi dòng L1 *(M37)* · tái lập đếm cả dòng thiếu *(M38)* · ứng viên một vế *(M39 · M40)* · ô lỗi tiền ≡ 0 *(M41)* · tiền tệ ⛔ `ma_tien_te` *(M42)* · băm một trường *(M43)* · `--ghi` ⛔ cần `--khoa` *(M44)* · thiếu bản đọc ⇒ 3 *(M45)* · ghi tệp tạm ⛔ thay đích *(M46)*.

**C. Đối chiếu H2 — hai nguồn** *(hợp đồng tệp nhãn)*: tệp nhãn công cụ này ghi *(bản sao, bản đọc tổng hợp, mã 4)* được đọc bằng **chính hàm `_doc_nhan`** của H2 *(`isp-h2` @ `33d333b`, `tools/do_voi_so_luong.py:174-212`, chỉ import — ⛔ sửa)* ⇒ `lỗi H2: []` · `H2 đọc được nhãn cho 122 / 122 dòng · {'KHONG_CO_SAO_KE': 60, 'KHOA_LECH': 30, 'TRUNG_SEQ': 20, 'KHAC': 12}`; phá `dong_sheet = True` ⇒ H2: `tệp nhãn: dong_thieu[0] cần dong_sheet là số nguyên — có True`.

## Bảng nhãn × kỳ *(⚠ BẢN ĐỌC TỔNG HỢP — ⛔ dữ liệu thật; nguyên văn CLI ③ trên bản sao. Kỳ là kỳ THẬT của DT1a; nhãn gán theo thứ tự `dong_sheet` nên dồn khối theo kỳ — ⛔ mang nghĩa nghiệp vụ)*
| kỳ | Σ | KHONG_CO_SAO_KE | KHOA_LECH | TRUNG_SEQ | KHAC |
|---|---|---|---|---|---|
| 2025-01 | 1 | 1 | 0 | 0 | 0 |
| 2025-02 | 2 | 2 | 0 | 0 | 0 |
| 2025-05 | 1 | 1 | 0 | 0 | 0 |
| 2025-06 | 3 | 3 | 0 | 0 | 0 |
| 2025-07 | 4 | 4 | 0 | 0 | 0 |
| 2025-08 | 4 | 4 | 0 | 0 | 0 |
| 2025-09 | 4 | 4 | 0 | 0 | 0 |
| 2025-10 | 9 | 9 | 0 | 0 | 0 |
| 2025-11 | 14 | 14 | 0 | 0 | 0 |
| 2025-12 | 5 | 5 | 0 | 0 | 0 |
| 2026-01 | 4 | 4 | 0 | 0 | 0 |
| 2026-02 | 5 | 5 | 0 | 0 | 0 |
| 2026-03 | 5 | 4 | 1 | 0 | 0 |
| 2026-04 | 8 | 0 | 8 | 0 | 0 |
| 2026-05 | 5 | 0 | 5 | 0 | 0 |
| 2026-06 | 12 | 0 | 12 | 0 | 0 |
| 2026-07 | 23 | 0 | 4 | 19 | 0 |
| 2026-08 | 13 | 0 | 0 | 1 | 12 |
| **Σ 18 kỳ** | **122** | **60** | **30** | **20** | **12** |

`KHAC` theo ghi chú: `KHOA_HONG:ps_no` 2 · `KHOP_KHI_GHEP_LAI` 10 ‖ `KHOA_LECH` theo trường lệch: `ps_no` 15 · `so_ct` 15. Mẫu số: `9.967 dòng sổ · 10.185 dòng L1 · 122 dòng sổ thiếu · 9.845 dòng ghép` · Số CT dạng khoa học: sổ 0 · L1 1.417.

## Kho thật
- `KHONG_CHAM`. Công cụ ⛔ mở kết nối PG, ⛔ đọc Drive/mạng; chỉ đọc JSON DT1a + ảnh `tests/fixture/itl_ledge_adjustment.json` *(cột `dong_sheet`)* + bản đọc khoá được trao. `FLS_CHO_GHI_THAT` ⛔ đặt. `docs/ITL/_tools/phan_loai_ly_do.json` **⛔ sinh** ở container *(`git status` chỉ 2 tệp mới + phiếu)*.

## Cách chạy để xem
- N/A — ⛔ chạm UI. Xem bằng `…/python tools/phan_loai_ly_do.py` *(cổng)* hoặc `--khoa <bản đọc>` *(in bảng ①–④)*.

## Hướng dẫn owner chạy lượt thật *(máy Windows có `Input_Raw/[Master] ITL_Ledge_raw.xlsx` — O10)*
**Điều kiện:** repo ở commit đã gộp có `tools/phan_loai_ly_do.py`; dùng `.venv\Scripts\python.exe`. Bản đọc khoá mang **Số CT + tiền THẬT** ⇒ đặt ở `hien_vat\dt1b_khoa.csv` *(`hien_vat/` bị `.gitignore` — ⛔ bao giờ lên git, ⛔ gửi đi)*.

1. **Dựng bản đọc** *(một sổ Excel MỚI — chỉ ĐỌC/chép giá trị, ⛔ sửa tệp nguồn)*: hàng 1 = `bang,dong,so_ct,ps_no,ps_co,tk,tien_te`.
   - Phía **SO**: mỗi hàng `r` = **10 … 9976** của sheet `ITL Ledge` *(đủ 9.967 hàng)* ⇒ `SO`, `r`, cột **B**, **E**, **F**, **G**, **D**.
   - Phía **L1**: sheet `Transaction Mapping L1` của RAW `1md85t…` *(dữ liệu từ hàng 5)* — mọi hàng có dữ liệu ⇒ `L1`, số hàng, cột **B**, **E**, **F**, **G**, **D**.
   - ⚠ **Cột `so_ct` đặt định dạng *Text* TRƯỚC khi dán *(Paste Special → Values)*** — nếu ⛔, Excel ghi Số CT dài thành `4.36619E+15` *(mất chữ số)*. Tiền để nguyên như ô hiện *(có dấu phân cách cũng được)*.
   - Lưu: *Save As → **CSV UTF-8 (Comma delimited)*** ⇒ `hien_vat\dt1b_khoa.csv`.
2. **Lệnh một dòng** *(PowerShell, từ gốc repo)*:
   `$env:PYTHONUTF8=1; .\.venv\Scripts\python.exe tools\phan_loai_ly_do.py --khoa hien_vat\dt1b_khoa.csv --ghi; "exit=$LASTEXITCODE"`
3. **Kiểm đầu ra** *(mỗi dòng một điều mong — khác ⇒ dừng, gửi nguyên văn màn hình; câu lỗi chỉ mang số hàng / tên cột, ⛔ giá trị)*:
   | Dòng in | Mong |
   |---|---|
   | `exit=` | **`4`** *(lần đầu: `KẾT: ĐO ĐƯỢC — ⛔ CHƯA GHIM …` — ⛔ phải lỗi)*. `1` = ĐỎ *(xem stderr)* · `3` = ⛔ thấy tệp |
   | `① MẪU SỐ:` | `9.967 dòng sổ` · phía L1 **≥ 9.992** dòng L1 *(ảnh 26/08 có 9.992; bản sống có thể nhiều hơn)* · `122 dòng sổ thiếu` · `9.845 dòng ghép (DT1a)` |
   | `② tái lập khoá+seq:` | **`9.845 / 9.845 dòng ghép DT1a = 100,00 %`** — thấp hơn ⇒ ĐỎ *(K10)*: chuẩn hoá ≠ mã ghép gốc **hoặc** bản L1 đã đổi sau 26/08 ⇒ gửi dòng ②, ⛔ sửa tay |
   | `② … Số CT dạng khoa học: sổ` | **`0`** — khác 0 ⇒ bước 1 đã làm hỏng cột B ⇒ xuất lại cột dạng *Text* |
   | `③ nhãn của 122 dòng sổ thiếu` | bốn số cộng lại = **122** |
   | `✅ đã ghi phan_loai_ly_do.json (mã 4)` | có |
   | `.\.venv\Scripts\python.exe tools\phan_loai_ly_do.py; "exit=$LASTEXITCODE"` *(cổng trên tệp vừa ghi)* | `exit=4` |
   | `Select-String -Path docs\ITL\_tools\phan_loai_ly_do.json -Pattern '@' \| Measure-Object` | `Count : 0` |
4. **Gửi về** orchestrator: tệp `docs\ITL\_tools\phan_loai_ly_do.json` + **toàn bộ màn hình** ①–④. ⛔ gửi `hien_vat\dt1b_khoa.csv`.
5. Sau đó *(⛔ việc của owner)*: một `WO` nhỏ làn DATA ghim `MONG["phan_bo_nhan"]` = dòng ③ *(nguồn: lượt owner + `nguon.ban_doc_sha256_16`)* và đổi bài `…phan_bo_CHUA_GHIM_la_ma_4` — từ đó cổng trả **0**, và mọi thay đổi nhãn về sau *(H3 sửa mã)* đều ĐỎ cho tới khi ghi lại bản khai.

## Dev tự thấy còn yếu
1. **⛔ một nhãn THẬT nào.** Toàn bộ bằng chứng là dữ liệu tổng hợp do chính tôi dựng — nó chứng minh công cụ làm **đúng thiết kế**, ⛔ chứng minh **thiết kế đúng nghiệp vụ**. Phần chỉ lượt thật trả lời được: TÁI LẬP có ra 9.845 không *(tức bản dựng lại quy tắc ghép khớp mã gốc không có trong repo)*.
2. **Nghĩa nhãn là tôi DỰNG** từ một câu ISP 3.1.1 `:685` + một câu fixture `ghep_bang`. Hai lựa chọn là của tôi, ⛔ của spec: ⓐ `KHOA_LECH` = có dòng L1 **chưa ai ghép** trùng Số CT *(≠ rỗng)* **hoặc** trùng cả bốn trường còn lại — trên sổ thật, tiền tròn *(vd. `1.000.000` cùng TK, cùng VND)* có thể làm một dòng `KHONG_CO_SAO_KE` thành `KHOA_LECH` giả; `lech` chỉ nói ứng viên GẦN NHẤT, ⛔ nói có bao nhiêu ứng viên *(mơ hồ bị giấu)*. ⓑ dòng L1 **đã có chủ** ⛔ là ứng viên *(chốt bằng 5 dòng tổng hợp + đột biến M37)*.
3. **Luật NỚI ngoài ghi chú fixture**: *trống ≡ 0* ở cột tiền và *ô lỗi Số CT ⇒ rỗng* *(ghép được với Số CT rỗng)*. Lý lẽ đơn điệu *(nới chỉ làm TÁI LẬP tăng — `tools/phan_loai_ly_do.py:58-61`)* là toán đúng, nhưng nới có thể biến một dòng thật sự `KHONG_CO_SAO_KE` thành `KHAC · KHOP_KHI_GHEP_LAI` *(vd. hai dòng ⛔ Số CT, cùng tiền)*.
4. **Số CT dạng khoa học phía SO chỉ là CHẨN ĐOÁN** *(`dang_khoa_hoc.SO`)*, ⛔ cổng: nếu bản xuất làm hỏng cột B, hai Số CT khác nhau chung 6 chữ số đầu gộp làm một khoá ⇒ `TRUNG_SEQ`/`KHOP` giả mà công cụ vẫn `4`. Hiện chỉ có hướng dẫn owner *(mong = 0)* — xem Q4.
5. **K10 TÁI LẬP = 9.845 là ĐÚNG BẰNG** — nếu bản sao L1 13/11 đã sửa cột B/D–G của dòng đã ghép, lượt thật ĐỎ và ⛔ ghi JSON; owner chỉ còn màn hình ①–④ để gửi. Tôi chọn chặt *(Đ5)* — xem Q1.
6. **Băm ≠ ẩn danh.** `khoa_bam` = sha256-16 ⛔ muối của bộ 5 trường. Một trường đơn lẻ dò ngược được ngay *(nên tôi ⛔ băm từng trường)*; cả bộ thì khó hơn nhưng Số CT ngân hàng có cấu trúc *(`FT` + năm-ngày + số thứ tự)* — người có sẵn tiền + TK của một dòng có thể dò lại Số CT. Đúng chữ phiếu giao *("chỉ băm sha256 16 ký tự")*; ghi để R1 biết giới hạn.
7. **R5 chỉ so token ≥ 6 ký tự** — Số CT / tiền ngắn hơn ⛔ được quét *(để ⛔ va với `dong_sheet` ≤ 4 chữ số và số đếm ≤ 5)*. Bù lại: tệp ra có lược đồ ĐÓNG *(R1)* — đường duy nhất đưa chuỗi tự do vào là trường `ky` của JSON DT1a, đúng đường bài `…NOI_vao_duong_do_that` đi.
8. `_van_tay` **chép 1 dòng** từ `tools/phan_loai_dong_thieu.py:115-116` thay vì import *(tệp ấy đang được phiên khác sửa)* — hai bản một luật; lệch thì K1/K2 ĐỎ ngay *(ồn, ⛔ im lặng)*.
9. **`fls/oracle/nguon.py:53` `CAM_MO` ghi `[Master] ITL_Ledge_raw.xlsx` là "tuyệt đối ⛔ mở"** *(~84 dòng mất mã `ITL#`)* và `11_BOI_CANH_TU_MEMORY.md` §3 *"bản xuất .xlsx ⛔ dùng cho giá trị"* — trong khi O10 bảo owner chạy trên chính tệp ấy. Khoá của bước này ⛔ dùng ngày, ⛔ dùng `ITL#`, và phép ghép gốc tạo ra 9.845 cũng đọc tệp ấy *(fixture `nguon`)* — nhưng mâu thuẫn chữ vẫn còn — xem Q3.
10. MONG số dòng/vân tay có **hai bản** *(công cụ ↔ bài)* — cố ý để bài ⛔ chép công cụ *(như DT1a)*; giá: sửa một bên phải sửa bên kia.
11. Câu lỗi `dòng {d} mang {len} nhãn [...]` khi `nhan` là danh sách **một** phần tử in *"mang 1 nhãn"* — phán ĐỎ đúng *(sai kiểu)*, chữ đọc lạ.
12. **Máy đột biến của tôi đã đếm sai hai lần** *(§Log ⑤)* — số cuối 49/50 là sau khi sửa máy và thêm phép dò `⚠ SẬP`, nhưng vẫn là máy của tác giả: R1 nên tự đột biến lại.
13. **Lược đồ tệp ra ĐÓNG** *(R1)* trong khi hợp đồng H2 cho *"khoá thừa được phép"* — tệp của bước này chặt hơn hợp đồng *(để ⛔ chuỗi tự do nào lọt vào)*. Nếu bước sau muốn thêm trường vào tệp nhãn thì phải sửa `KHOA_DONG`/`KHOA_TRAN` của công cụ, ⛔ chỉ hợp đồng.
14. R6 *(tên khoá cấm)* chồng một phần lên R1: ở các dict đã đóng lược đồ, R1 cắn trước; R6 là chốt duy nhất ở dict **mở** *(`mau_so.khoa_hong`, `mau_so.dang_khoa_hoc`, `dem_nhan`, `nhan_theo_ky`)* — ca phá đặt đúng vào `khoa_hong`.

## Câu hỏi *(gửi orchestrator — `KHONG_CHAN` cả bốn; mỗi câu một khuyến nghị)*
- **Q1 · Lượt thật mà TÁI LẬP < 9.845 thì sao?** ⓐ *(đã làm — khuyến nghị)* giữ ĐỎ, ⛔ ghi JSON; owner gửi màn hình ①–④ *(đủ để orchestrator quyết, ⛔ PII)* — giá: có thể cần lượt thứ hai · ⓑ cho ghi với mã riêng khi tái lập ≥ một ngưỡng — giá: ngưỡng là **chế spec**, cổng thành mềm · ⓒ owner xuất phía L1 từ bản đúng ngày 26/08 nếu còn — giá: có thể ⛔ còn bản ấy.
- **Q2 · Ai ghim `MONG["phan_bo_nhan"]`, ở phiếu nào?** ⓐ *(khuyến nghị)* `WO` nhỏ làn DATA sau lượt owner: ghim dòng ③ + sửa bài `…CHUA_GHIM…`, nguồn = lượt owner + `ban_doc_sha256_16` — giá: thêm một vòng phiếu · ⓑ thêm cờ `--ghim` cho công cụ tự ghim — giá: MONG tự chép từ chính lần đo *(đúng thứ Đ5 cấm)*.
- **Q3 · `CAM_MO` (`nguon.py:53`) ↔ O10.** ⓐ *(khuyến nghị)* ghi vào `WO-095` một ngoại lệ có phạm vi: owner chỉ ĐỌC cột B·D·E·F·G *(⛔ ngày, ⛔ `ITL#`)* của `ITL Ledge` trong tệp ấy — cùng nguồn với phép ghép gốc · ⓑ đọc phía SO từ ADJUSTED sống — giá: `GAP-ORA-08` *(hết giờ 60 s)* và hàng có thể ⛔ cùng hệ `dong_sheet` của ảnh 26/08 *(K11 sẽ ĐỎ)*.
- **Q4 · Nâng "Số CT dạng khoa học phía SO = 0" thành cổng K13?** ⓐ *(khuyến nghị — ở vòng sửa sau R1 nếu orchestrator nhận)* thêm một phép + một ca phá *(~10 dòng)* — chặn bản xuất hỏng thay vì nhắc · ⓑ giữ chẩn đoán + hướng dẫn owner — giá: dựa vào mắt người đọc dòng ②.
- *(ghi nhận, ⛔ hỏi)* ISP `:94` / `:141` / `:788` / `:836` vẫn ghi tệp cũ — vá ISP theo `DT1a-R1-08` là việc `fls-ba` / orchestrator.

## Vòng sửa sau R1 *(KQ-097)* — chỉ THÊM
*(`fls-dev`, làn DATA, phiên cloud CON ngoài máy orchestrator · sau R1 `KQ-097` · trước R2 `KQ-098`. Phạm vi: **5 NÊN SỬA** `DT1b-R1-01 · -02 · -04 · -05 · -06` + GHI NHẬN rẻ **`-03` · `-10` · `-11`**. ⛔ chạm `WO` · dashboard · `TIEN_DO.md` · changelog · sổ phát hiện — R2/orchestrator đổi trạng thái sổ. Mọi lệnh ở worktree `isp-dt1b`, cụm PG 5437, venv `/home/user/FLS-tobe/.venv`, `PYTHONUTF8=1`.)*

### Đã đổi *(2 tệp mã + tệp bài mới)*
| Tệp | Vì sao |
|---|---|
| `tools/phan_loai_ly_do.py` *(+~60 dòng)* | **R7** *(`-04`)*: `kiem()` đóng cả GIÁ TRỊ — mọi LÁ = hằng *(`_vi_sao` · `khong_mang_PII` · `nguon.tep_dt1a`/`anh_so`)* · mẫu *(`nguon.ban_doc_sha256_16` hex16)* · tập đóng + int ≥ 0 *(`mau_so.khoa_hong` · `dang_khoa_hoc`)* · int *(5 số đếm `mau_so`)*; câu lỗi nêu TÊN LÁ, **⛔ in giá trị**. **K13** *(`-05`)*: `MONG["van_tay_nhan"]` + `_van_tay_nhan()` = sha256-16 của tập `[dong_sheet, nhan, lech, ghi_chu]` đã sắp; `None` ⇒ góp mã 4 *(cùng cơ chế `phan_bo_nhan`)*. **R8** *(`-06`)*: `_trong_repo_khong_ignore()` — bản đọc khoá trong repo mà ⛔ bị `.gitignore` ⇒ **mã 2**. **`-11`**: đường dẫn là thư mục ⇒ mã 2 *(⛔ 3)*; câu mã 3 in **đường tuyệt đối**. **`-03`**: khai D27 *"phòng thủ chồng"* ở docstring `_ghi`. Hai hằng `NGUON_TEP_DT1A`/`NGUON_ANH_SO` (một nguồn cho `do()` + R7). `import subprocess` |
| `tests/du_lieu/test_phan_loai_ly_do.py` *(+~40 dòng)* | `_chay_trong` ghim `van_tay_nhan` CÙNG lượt `phan_bo_nhan` *(K13 — nếu hằng độc lập sai thì MỌI bài happy ĐỎ, cổng hai nguồn)*; hằng `VT_NHAN_TONG_HOP = c5c55c272e02b414`; bài `…R1_05_van_tay_nhan_TONG_HOP_dung_thiet_ke` *(tự tính lại từ thiết kế `_dung`, ⛔ chép công cụ)*; bài `…R1_11_duong_dan_la_thu_muc_la_2`; sửa `…tep_nhan_THAT…` *(`-10`: tệp thật có mà chưa ghim ⇒ `pytest.fail`, ⛔ `xfail`)* |
| `tests/du_lieu/test_phan_loai_ly_do_vong_sua_r1.py` *(mới, 26 bài)* | `KQ-097` §Bài thử đề xuất ①–⑭ *(17 `test_R1_*` giết đột biến + 8 `test_R1_DE_XUAT_*` phát hiện)* + bài `-06` `git init`. ⚠ **Lệch CÓ Ý** §KQ-097: ⑬ lá `ban_doc_sha256_16` dùng mã `FT25123456789` *(có chữ ⇒ ⛔ hex16)* thay `4366191234567890` — số 16 chữ số thập phân KHỚP `^[0-9a-f]{16}$` nên cổng mẫu ⛔ bắt *(xem §Giới hạn còn lại)* |

### Bằng chứng từng phát hiện *(ĐỎ-trước đo trên `8a18599`, mã Dev)*
| Mã | Kết | Bằng chứng *(lệnh · exit · dòng)* | ĐỎ-trước |
|---|---|---|:-:|
| `-01` | **ĐẠT** | 6 bài đơn vị gọi thẳng `phan_loai` *(①–⑥)*. Đột biến BIÊN trên tool MỚI *(`/tmp/mut_dt1b`, trả nguyên)*: **10/10** CHẾT — D01·D02 *(①)* · D04 *(②)* · D07·D08 *(③, 6/6 `PYTHONHASHSEED` 0–5)* · D0506·D11 *(④)* · D15 *(⑤)* · D13·D14 *(⑥)*, mỗi killer `rc=1 FAILED` | có *(mã cũ các killer XANH — mã ĐÚNG; thiếu là bài)* |
| `-02` | **ĐẠT** | 3 bài R5 qua đường đo thật *(⑦)* + 3 ca `PHA` *(⑧)*. Đột biến: **6/6** CHẾT — D17 *(⑦ tien)* · D19 *(⑦ thô)* · D18 *(⑦ chuẩn hoá)* · D20 *(⑧ Số CT)* · D21 *(⑧ email)* · D22 *(⑧ email ở TÊN khoá)* | có |
| `-03` | **ĐẠT** | 5 bài ⑨–⑫ *(D23·D24·D28·D30·D31)* + khai D27 phòng thủ chồng ở docstring `_ghi`. Các bài này XANH trên mã cũ *(giết đột biến)* | n/a *(giết đột biến)* |
| `-04` | **ĐẠT** | `…DE_XUAT_la_chuoi_TU_DO_bi_chan` **7/7** ĐỎ trên `8a18599` *(exit 0)* → XANH sau R7 *(exit 1)*; thêm `assert` giá trị *(SO_CT·DG)* **⛔** trong stderr | **ĐỎ × 7** → XANH |
| `-05` | **ĐẠT** | `…DE_XUAT_doi_nhan_HAI_dong_cung_ky` ĐỎ trên `8a18599` *(đổi chỗ nhãn 2 dòng cùng kỳ `2026-07` giữ nguyên số đếm ⇒ exit 0)* → exit 1 `vân tay danh tính nhãn (K13)` sau sửa | **ĐỎ** → XANH |
| `-06` | **ĐẠT** | `…ban_doc_khoa_trong_repo_khong_gitignore` ĐỎ trên `8a18599` *(CSV ở gốc repo ⇒ exit 0)* → exit **2** `bị .gitignore` sau R8; CSV ở `hien_vat/` ⇒ đo bình thường. CLI thật: `--khoa <thư mục>` exit 2, `--khoa /tmp/…/khong_co.csv` mã 3 in đường tuyệt đối | **ĐỎ** → XANH |
| `-10` | **ĐẠT** | `…tep_nhan_THAT…`: tệp thật có mà `MONG` chưa ghim ⇒ `pytest.fail` *(⛔ `xfail` — `S0-R3-01`)*; container `RA_THAT` vắng ⇒ exit 3 *(⛔ đổi)* | — |
| `-11` | **ĐẠT** | `…duong_dan_la_thu_muc_la_2` ĐỎ trên `8a18599` *(thư mục ⇒ 3)* → exit **2** sau sửa; câu mã 3 in đường tuyệt đối | **ĐỎ** → XANH |

### Đính chính *(chỉ THÊM — ⛔ sửa dòng gốc)*
- **`BG-096:176`** *(§Hướng dẫn owner bước 5)* — câu *"từ đó cổng trả 0, và **mọi** thay đổi nhãn về sau (H3 sửa mã) đều ĐỎ cho tới khi ghi lại bản khai"* **đúng một nửa khi viết**: với CHỈ `phan_bo_nhan` ghim, một thay đổi **giữ số đếm** *(đổi chỗ nhãn hai dòng cùng kỳ — `DT1b-R1-05`)* vẫn XANH. ⇒ `-05` thêm **K13 `van_tay_nhan`** *(ghim CÙNG lượt, cùng nguồn với `phan_bo_nhan`)*; từ nay câu ấy ĐÚNG — mọi thay đổi danh tính nhãn, kể cả giữ tổng, đều ĐỎ. Bước ghim của owner *(bước 5)* nay ghim **cả hai** `phan_bo_nhan` + `van_tay_nhan` *(cùng dòng ③ + tập `[dong_sheet, nhan, lech, ghi_chu]`)*.
- **Va chạm tên `K13`:** `BG-096` **Q4** đề xuất *"cổng K13"* cho *"Số CT dạng khoa học phía SO = 0"*; sổ phát hiện `-05` *(fls-test)* đặt *"phép K13"* cho **vân tay nhãn**. Vòng này theo sổ ⇒ **K13 = vân tay danh tính nhãn**. Nếu orchestrator nhận Q4, cổng Số CT khoa học nên đánh số **K14** để ⛔ trùng.

### Giới hạn còn lại *(nói thẳng — Đ1/Đ5)*
1. **`ban_doc_sha256_16` chỉ canh được MẪU hex16 ở chế độ cổng** *(⛔ tái tính sha ở `--tep` — ⛔ có bản đọc thô)*: một Số CT **16 chữ số thập phân** vẫn khớp `^[0-9a-f]{16}$` ⇒ ⛔ phân biệt được với sha. Chế độ ĐO *(`--khoa`)* ⛔ dính *(R5 `quet_token` quét cả lá này với tập Số CT thật của bản đọc)* — rủi ro chỉ ở tệp owner gửi về bị sửa tay. Các lá còn lại *(6/7 của ⑬)* đóng bằng HẰNG / tập đóng / int — ⛔ dính.
2. **Câu `so()` *(K1·K2·K3·K5·K9·K10)* vẫn in `đo {co!r}`** — R7 đã chặn PII ở 7 lá tự do + guard kiểu `khoa_hong`/`dang_khoa_hoc`; nhưng nếu một giá trị lạ lọt vào `dem_nhan`/`nhan_theo_ky`/`van_tay` *(đều int/hex ở tệp hợp lệ)* và vượt được guard thì `so()` in lại. Sạch hoàn toàn `so()` sẽ bớt chẩn đoán cho lệch vân tay thật — để orchestrator cân *(⛔ trong ⑬)*.

### GHI NHẬN ⛔ sửa vòng này *(lý do)*
- **`-07`** *(DEV·orch)* — ① chẩn đoán "cắt 6 chữ số" ở dòng ② + ② ca tổng hợp **mất chữ số**: sửa bộ dựng `_dung` để sinh mã 16 chữ số mất chữ số **thật** đụng nhãn mong của 20 `TRUNG_SEQ` + 10 `KHOP` *(đang dựa `(100000+d)×10¹⁰` khớp lại được)* ⇒ rủi ro cả suite B1/B2/B3, **> 15 dòng**, lấn phạm vi; ③ cần orchestrator trả nghĩa *"khớp bản số thường"* *(ISP `:814`)*. Chuyển orchestrator / `WO` riêng.
- **`-08`** *(DEV)* — đếm ô tiền mơ hồ `^\d{1,3},\d{3}$` in ở dòng ② đụng chuỗi mà bài `…MAU_SO_in_TRUOC_ty_le` canh; hướng dẫn owner là chữ BG; lõi *(`parse_so` locale VN)* ở làn **BE-HC** *(nhiều nơi dùng — ⛔ sửa)*. Giá trị thấp vòng này ⇒ để `WO` riêng.
- **`-09`** *(orch·BA)* HMAC khoá owner · **`-12`** *(orch)* ghi `WO-095` + vá ISP — **⛔ việc DEV**.

### Q8 — số bài thu thập *(nhánh `isp/DT1B` tách TRƯỚC S0 ⇒ ⛔ có `MONG_PYTEST_TOAN_BO`; orchestrator đặt sàn lúc gộp)*
`python -m pytest --collect-only` toàn bộ: **TRƯỚC** vòng sửa `2.524` → **SAU** `2.552` *(+28 = 26 tệp mới + 2 bài thêm ở tệp cũ; đo bằng tổng dòng `tệp: n` của `--collect-only -q`)*. `tests/du_lieu`: `64` → `92`. `tests/du_lieu/test_phan_loai_ly_do.py`: `48` → `50`.

### Xác minh cuối *(nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_phan_loai_ly_do_vong_sua_r1.py tests/du_lieu/test_phan_loai_ly_do.py` | `76 passed` *(mã đã sửa)* |
| `pytest tests/du_lieu` *(hồi quy DT1a + DT1b)* | `92 passed` |
| đột biến `/tmp/mut_dt1b` *(tool MỚI + killer mới, trả nguyên)* | `16/16` đột biến BIÊN CHẾT · tool trả nguyên khớp byte |
| `bash …/isp-s0/tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` *(từ worktree `isp-dt1b`)* | *(ghi ở báo cáo phiên — đường nền của script S0 vs nhánh tách-trước-S0)* |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python tools/phan_loai_ly_do.py` *(cổng mặc định)* | exit **3** *(câu mặc định byte y nguyên — ⛔ đổi `_che_do_cong`)* |

## Vòng sửa sau R2 *(KQ-098)* — chỉ THÊM
*(`fls-dev`, làn DATA, phiên cloud CON ngoài máy orchestrator · sau R2 `KQ-098` · trước R3. Phạm vi: **2 NÊN SỬA** `DT1b-R2-01 · -02` + **`-03`** *(gộp vào vòng này — orchestrator quyết)* + GHI NHẬN rẻ **`-04` · `-05`**. ⛔ chạm `WO` · dashboard · `TIEN_DO.md` · changelog chung · sổ phát hiện — R3/orchestrator đổi trạng thái sổ. Mọi lệnh ở worktree `isp-dt1b`, cụm PG 5437, venv `/home/user/FLS-tobe/.venv`, `PYTHONUTF8=1`.)*

### Đã đổi *(1 tệp mã + 1 tệp bài mới)*
| Tệp | Vì sao |
|---|---|
| `tools/phan_loai_ly_do.py` *(+~12 dòng)* | **R7 trần độ lớn** *(`-01`)*: thêm hằng `TRAN_DEM = 10 ** DAI_TOI_THIEU` *(= 1.000.000)*; `kiem()` đòi mọi LÁ SỐ của `mau_so` *(`khoa_hong.SO/L1` · `dang_khoa_hoc.SO/L1` · 5 số đếm gồm `so_dong_l1`)* thoả `0 ≤ n < TRAN_DEM`, ⛔ chỉ `type is int`. Vì sao con số: số đếm dòng lớn nhất đo được là `so_dong_so` = 9.967 *(≈ 10⁴)*; một token ≥ `DAI_TOI_THIEU` chữ số là Số CT / tiền *(luật R5 cấm)*, ⛔ phải số đếm ⇒ Số CT 16 chữ số DẠNG INT *(`4366191234567890`)* nay bị chặn ở cổng `--tep`. Câu lỗi nêu TÊN LÁ + ngưỡng, **⛔ in giá trị**. **R8 fail-đóng** *(`-03`)*: `_trong_repo_khong_ignore()` — `except OSError` nay `return True` *(⛔ `False`)*: tệp TRONG repo mà `git` ⛔ chạy được ⇒ ⛔ chứng minh được `.gitignore` che ⇒ TỪ CHỐI *(mã 2)*, Đ5. Docstring R7 + R8 cập nhật *(chỉ THÊM ý "trần độ lớn" · "fail-đóng")* |
| `tests/du_lieu/test_phan_loai_ly_do_vong_sua_r2.py` *(mới, 14 bài)* | 2 `test_R2_DE_XUAT_*` *(phát hiện `-01` · `-03` — ĐỎ trên `4a45173`)* + 12 `test_R2_*` *(giết đột biến BIÊN của `-02` nhánh phan_xu/R8, `-04` mẫu hex16 + `sorted`, `-05` lech `tien_te`)*. ⛔ chạm tệp bài R1 *(sổ luật: vòng sau thêm tệp/hàng, ⛔ sửa)* |

### Bằng chứng từng phát hiện *(ĐỎ-trước đo trên `4a45173`, mã R2)*
| Mã | Mức | Kết | Bằng chứng *(lệnh · exit · dòng)* | ĐỎ-trước |
|---|---|---|---|:-:|
| `-01` | NÊN SỬA | **ĐÃ SỬA** | `…DE_XUAT_la_so_nguyen_co_tran_do_lon` **5/5** lá *(so_dong_l1 · khoa_hong.SO/L1 · dang_khoa_hoc.SO/L1)* ĐỎ trên `4a45173` *(Số CT 16 chữ số dạng int ⇒ exit 0)* → XANH sau trần *(exit 1 `/mau_so/…`)*; `assert str(SO_CT_INT) not in err` *(⛔ in giá trị)*. `…tran_do_lon_dung_nguong`: lá = `TRAN_DEM` ⇒ ĐỎ · = `TRAN_DEM − 1` ⇒ qua *(cô lập `so_dong_l1` ⛔ bị MONG ghim)*. Đột biến: bỏ trần *(chỉ `int`)* 2 vế CHẾT · `<`→`<=` CHẾT | **ĐỎ × 6** → XANH |
| `-02` | NÊN SỬA | **ĐÃ SỬA** *(3 bài khoá hành vi đúng)* | *(a)* `…phan_bo_ghim_van_tay_nhan_None_la_ma_4`: chỉ `phan_bo_nhan` ghim, `van_tay_nhan=None` ⇒ **mã 4** *(⛔ 0)*; đột biến `if mong is None or mong_vt is None` → bỏ `or mong_vt is None` CHẾT. *(b)* `…R8_duong_TUONG_DOI…`: `monkeypatch.chdir(repo)` + đường tương đối ⇒ **mã 2**; đột biến bỏ `.resolve()` *(ValueError ⇒ lọt)* CHẾT. *(c)* `…R8_khong_phai_git_repo_tra_128…`: thư mục ⛔ git ⇒ check-ignore 128 ⇒ **mã 2**; đột biến `!= 0` → `== 1` CHẾT | n/a *(giết đột biến; mã đúng, thiếu bài)* |
| `-03` | GHI NHẬN *(gộp)* | **ĐÃ SỬA** | `…DE_XUAT_git_khong_chay_duoc_la_TU_CHOI`: `PATH=/nonexistent` + CSV tổng hợp trong `docs/ITL/_tools/` ⇒ **mã 2** sau sửa *(trên `4a45173`: OSError→False ⇒ mã 0, ghi ra — ĐỎ-trước)*; đột biến `return True` → `return False` CHẾT | **ĐỎ** → XANH |
| `-04` | GHI NHẬN | **ĐÃ SỬA** *(rẻ)* | `…khoa_bam_MAU_hex16_neo_hai_dau`: khoa_bam 17 ký tự *(bỏ `$`)* · hex chữ HOA *(thêm `re.I`)* ⇒ exit 1; đột biến tương ứng **2/2** CHẾT. `…van_tay_nhan_doc_lap_thu_tu_dong`: `_van_tay_nhan(dong) == _van_tay_nhan(reversed)`; đột biến bỏ `sorted` CHẾT. *(Trần `DAI_TOI_THIEU` 6→8 ở ngưỡng token-cấm `doc_khoa` — chế độ ĐO — còn khai GHI NHẬN, xem §Giới hạn)* | n/a *(giết đột biến)* |
| `-05` | GHI NHẬN | **ĐÃ SỬA** *(rẻ)* | `…KHOA_LECH_truong_tien_te`: hai khoá chỉ khác `tien_te` cùng Số CT ⇒ `lech == ['tien_te']`; đột biến `range(5)` → `range(4)` *(bỏ `tien_te`)* CHẾT | n/a *(giết đột biến)* |

### Chứng minh đột biến *(sao lưu tool → vá → chạy bài đích → trả nguyên; `cmp` khớp byte sau mỗi lượt)*
**11/11** đột biến BIÊN CHẾT *(`rc=1 FAILED` ở đúng bài đích)*: R2-02a·b·c · R2-03 · R2-01 *(bỏ trần `khoa_hong` · bỏ trần `so_dong_l1` · `<`→`<=`)* · R2-04 *(bỏ `$` · thêm `re.I` · bỏ `sorted`)* · R2-05 *(`range(5)`→`range(4)`)*. Tool trả nguyên khớp byte sau cả 11 lượt.

### GHI NHẬN ⛔ sửa vòng này *(lý do)*
- **`-06`** *(orch·BA)* — cổng Số CT dạng khoa học phía SO **K14** *(ISP đánh số)* chưa có mã: dựng K14 là **TÍNH NĂNG MỚI** *(cổng + `MONG` khai trước)*, và phụ thuộc orchestrator trả nghĩa *"khớp bản số thường"* *(ISP `:814`, còn mở ở `-07`)* ⇒ **lấn phạm vi**. Chuyển orchestrator *(cùng `-07`)*.
- **`-04` phần còn lại** — `DAI_TOI_THIEU` 6→8 ở ngưỡng token-cấm của `doc_khoa` *(cam_ct/cam_tien, chế độ ĐO)*: giết cần ca token Số CT 6–7 ký tự qua đường đo thật, chồng lớp với `-07` *(bộ dựng `_dung`)*; `MAU_HEX16` ở `ban_doc_sha256_16` *(giới hạn #1 R1 — ⛔ phân biệt được sha với 16 chữ số thập phân ở cổng)* ⛔ đóng thêm được ở chế độ cổng. Để GHI NHẬN.
- **`-07`** *(duong-nen nhạy tải)* — ⛔ lỗi mã DT1b; nhắc R3/orchestrator chạy `--duong-nen` **một mình** trên cụm *(⛔ chồng pytest khác dùng chung `fls_test`)*. Vòng này đã chạy một mình *(xem §Xác minh cuối)*.

### Q8 — số bài thu thập *(nhánh `isp/DT1B` ⛔ có `MONG_PYTEST_TOAN_BO`; orchestrator đặt sàn lúc gộp)*
`python -m pytest --collect-only` toàn bộ: **TRƯỚC** vòng sửa R2 `2.552` → **SAU** `2.566` *(+14 = tệp bài mới; đo bằng tổng dòng `tệp: n` của `--collect-only -q`)*. `tests/du_lieu`: `92` → `106`. `tests/du_lieu/test_phan_loai_ly_do_vong_sua_r2.py`: `14`.

### Xác minh cuối *(nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_phan_loai_ly_do_vong_sua_r2.py` | `14 passed` |
| `pytest tests/du_lieu` *(hồi quy DT1a + DT1b)* | `106 passed` |
| đột biến *(sao lưu tool, vá, trả nguyên)* | `11/11` đột biến BIÊN CHẾT · tool trả nguyên khớp byte |
| `bash …/isp-dt1b/tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` *(script NHÁNH, chạy MỘT MÌNH)* | `26 = 26` node id *(toàn bộ · thêm 0 · bớt 0)* · `3 = 3` node id *(tests/web)* · `KẾT: ĐẠT` *(chạy MỘT MÌNH trên cụm — log `12 failed, 2538 passed, 2 xfailed, 14 errors`; đỏ CÓ SẴN = đường nền)* |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `K1` ĐỎ **ở tệp ngoài lane Dev** *(`SO_PHAT_HIEN_ISP-3.1_DT1b.md` header `v0.1` < changelog `v0.2` — fls-test R2, có từ `4a45173`, Dev ⛔ đụng)*; `K2`–`K6` ĐẠT. Xem §Câu hỏi cho orchestrator |

### Câu hỏi cho orchestrator
- **Q(R2)-1 — K1 doc-gate ĐỎ ở sổ phát hiện của fls-test.** `kiem_tai_lieu.py` K1 báo `SO_PHAT_HIEN_ISP-3.1_DT1b.md`: header `**Version:** v0.1` *(:3)* < changelog `v0.2` *(:39)*. Có từ commit `4a45173` *(KQ-098, trước vòng này)*; Dev ⛔ sửa tệp này *(ngoài lane · sổ luật: fls-test/orchestrator đổi)*. **Khuyến nghị A** *(nên)*: fls-test / orchestrator bump header tệp sổ lên `v0.2` *(một dòng)* để cổng xanh. **B**: orchestrator ghi lý do chấp nhận K1 ĐỎ tạm cho tệp sổ-riêng *(chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*. Dev chờ chỉ dẫn, ⛔ tự đụng tệp sổ.
