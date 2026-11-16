# BG-107 — bàn giao `WO-106` *(ISP 3.1.2 · Step 10 · `DT3`)* — ba ảnh nguồn `IX.HD` · `IX.ORG`: cây ATL · Mapping Master · CDT Correct

| | |
|---|---|
| **Thuộc** | `WO-106` *(quyết định ⑪ CDT Correct `mong = 13` · ⑫ `AA:AD` ⛔ thuộc RAW)* |
| **Phát bởi** | `fls-dev` — agent làn **FE ↩ DATA** *(phiên mới)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-108` · R2 `KQ-109` · R3 `KQ-110` *(dải của `WO-106`)* |
| **Commit** | nhánh **cục bộ** `isp/DT3` @ **`2a31f76`** *(mã + bài + ảnh)* — tách từ `80496ec`. ⚠ `2a31f76` = `amend` của `78baa20` *(chưa đẩy)*: đúng MỘT dòng docstring công cụ `13 bài` → `20 bài` — đếm lại theo node id khi soạn phiếu *(số cũ đếm DÒNG thông báo lỗi, ⛔ đếm bài — Đ4)*; ⛔ đẩy *(lời giao: ⛔ push; orchestrator gộp sau R3)*. Phiếu này ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-dt3` · cụm PG cổng **5436** |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` mục **`## Step 10 · DT3`** *(dòng 1182–1257)* · AP v3.1.2 §3.2.1 hàng `IX.HD` · `IX.ORG` · §3.2.4 · §3.2.5 *(bảng cây HD 6 nhóm)* · `fls/adapters/mapping_master.py` *(`doc_cot` · `COT` · `TRUONG` · `DONG_DAU = 7` · docstring đo 28/08)* · `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/ix_fx.py` *(khuôn mẫu DT2)* · `BG-086` · `CLAUDE.md` Đ1–Đ5 · Riêng tư |

## Cổng vào *(`05` §5)*
- **git thật**: worktree ở `isp/DT3`, `git log -1` = `80496ec BG-086: mục "Vòng sửa sau R1 (KQ-087)" …` — khớp lời giao *(= `isp/DT2`)*. Cây sạch khi nhận.
- **version**: ISP 3.1.2 · AP v3.1.2 · `WO-106` *(commit `ead0eef` ở nhánh làm việc của orchestrator)*. ⚠ `WO-106` **⛔ có trên `isp/DT3`** *(nhánh tách từ `isp/DT2`, trước `ead0eef`)* ⇒ trạng thái `WO` · dòng nhật ký · `handoff/README.md` là việc của orchestrator khi gộp — tiền lệ `BG-086` *(`WO-085` "orchestrator ghi sau")*. Run id: ⛔ cần *(bước ⛔ nói "đã chạy")*.
- **Nguồn thô**: ba tệp orchestrator đọc bằng connector 16/11 *(⛔ agent gọi Drive — O7)*: `atl_cay_A7_F88.json` *(81 hàng `{A, cap_cot, o}`)* · `mapping_master_A1_P120.json` *(85 hàng lưới thô, khoá `canh_bao_rieng_tu`)* · `cdt_correct_BR11_BS23.json` *(`{cot, dong}`, 13 dòng)*. ⛔ commit tệp thô.
- **Spec lệch đo** *(đã chốt trong `WO-106`, ⛔ mở `HOI`)*: ISP/AP ghi CDT Correct **"18 dòng (BR11:BS28)"** = khoảng Ô ⇒ theo ⑪ `mong = 13`; ISP ghi `mapping_master_cfg.json (A:B · AA:AD · D:L)` ⇒ theo ⑫ ⛔ `AA:AD` *(RAW `Q1:AN120` rỗng)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/dong_bang_sheet.py` *(+201 −29)* | ⚠ **Sửa công cụ chung — bài đòi** *(AC-4 cho phép "khai lý do")*: ba nguồn DT3 là bảng **CHỮ**, bản DT2 chỉ biết khoá `yyyymm` và đòi mọi ô cột chọn là SỐ — 20 bài giao kèo ĐỎ `KIEU_KHOA='ma' ⛔ thuộc ['yyyymm']`; cây ATL *(hàng `{A, cap_cot, o}`)* và Mapping Master *(lưới A…P)* ⛔ ở hình `{cot, dong}`. Thêm **bốn mục TUỲ CHỌN** của giao kèo khuôn: `KIEU_KHOA = "ma"` *(khoá chữ; trùng so sau khi gộp khoảng trắng)* · `KIEU_COT = {cột: "chu" \| "chu?"}` *(+ đếm "ô ⛔ chữ", mỗi phép đếm ô có mẫu số riêng — Đ4)* · `chuan_bi(tho)` *(bản thô hình dạng orchestrator → bảng; `ValueError` ⇒ TỪ CHỐI exit 2, nổ/sai hình ⇒ LỖI exit 3)* + **bảng phụ** `phu.<tên>` *(vào ảnh **và vào checksum**)* · `PHU_MONG` *(Đ5 cho bảng phụ)*. Soát riêng tư phủ tên cột bảng phụ, và bản thô có `cot` thì soát TRƯỚC `chuan_bi`. Khuôn ⛔ khai mục nào ⇒ chạy **y như DT2**: `ix_fx.json` tái tạo **đúng từng byte** *(sha256 `e2c9fdd028bd3286` = `BG-086`)*, 63/63 bài DT2 xanh. Chính chú thích cũ của `KIEU_KHOA_BIET` đã hẹn *"Kiểu khác ⇒ thêm khi có bước cần"* |
| `tools/khuon_dong_bang/atl_cay.py` *(mới, 147 dòng)* | Khuôn cây ATL → `IX.HD`: `chuan_bi` phân ba dạng nhãn *(`MÃ \| Tên` = dòng mã · `MÃ\|Tên` = tiêu đề nhóm · `""` = dòng trống; dạng khác ⇒ TỪ CHỐI)*, **cấp = `cap_cot` + 1**, **cha** = dòng mã gần nhất phía trên có cấp nhỏ hơn TRONG nhóm *(ngăn xếp; tiêu đề nhóm xoá ngăn, dòng trống ⛔ đụng)*. Cột `A` *(số mUSD đã định dạng)* **⛔ vào ảnh**. `NHOM` = 6 nhóm của AP §3.2.5 khai một chỗ; `PHU_MONG = {nhom: 6, dong_trong: 1}`; `thieu_lac`: nhóm khai ⛔ dòng mã ⇒ thiếu ⇒ ĐỎ, nhóm ⛔ khai ⇒ ⛔ đo được ⇒ ĐỎ. ⛔ kiểm cha–con/chu trình *(C4)* |
| `tools/khuon_dong_bang/mapping_master_cfg.py` *(mới, 153 dòng)* | Khuôn Mapping Master → `IX.HD · IX.ORG`. Bảng chính = **đầu ra `doc_cot`** *(GỌI hàm thật trên `H…M`; `KHOA`/`COT` lấy từ `TRUONG` của adapter — ⛔ khuôn đọc thứ hai)*; bảng phụ `tho` = cột **`A:B · D:G` THÔ** *(⑫)*, `bam` *(hàng đã băm)*, `loai` *(dòng `doc_cot` gạt — mong 0)*. **Riêng tư đóng KHI LẠ**: từ dòng 4, hàng có `B` ⛔ thuộc 21 pháp nhân/nhãn quỹ đã khai ⇒ `A` và `B` thay bằng `sha256_16:<16 hex>` *(muối công khai `MUOI`, khai trong khuôn + `ghi_chu_khuon` của ảnh)*; dòng 1…3 của `A:B` phải đúng bản đo *(khác ⇒ TỪ CHỐI)*. ⛔ mang `C · N · O · P` *(O lặp LE — mang tên người)* |
| `tools/khuon_dong_bang/cdt_correct.py` *(mới, 41 dòng)* | Khuôn CDT Correct → `IX.ORG`: bản thô đã `{cot, dong}` ⇒ ⛔ `chuan_bi`; khoá `cdt_nguon` · `cdt1_chuan` chữ **⛔ được rỗng** *(rỗng = đường "CDT lạ rơi im lặng về SHQ2" AP §3.2.4 gọi tên)*; thiếu/lạc **⛔ áp dụng** cho bảng ánh xạ — `dai` nói rõ |
| `tests/fixture/cau_hinh/atl_cay.json` *(sinh máy, 1.296 dòng, sha256 `f32f7e7fb2b64e34…`)* | 74 dòng mã + `phu.nhom` 6 + `phu.dong_trong` 1 · `checksum_noi_dung` **`77ca9d6c74f4254a`** |
| `tests/fixture/cau_hinh/mapping_master_cfg.json` *(sinh máy, 2.419 dòng, sha256 `452d0063441a89bb…`)* | 73 mã `hd` + `phu.tho` 84 · `phu.bam` 7 · `phu.loai` 0 · `checksum_noi_dung` **`e96f6d1a86a03320`** |
| `tests/fixture/cau_hinh/cdt_correct.json` *(sinh máy, 146 dòng, sha256 `1b1fde6770f5e5d9…`)* | 13 dòng · `checksum_noi_dung` **`30aea854bd879f6d`** |
| `tests/du_lieu/test_anh_cau_hinh.py` *(mới, 938 dòng, **65 bài**)* | 21 giao kèo *(khuôn giả lập)* · 7 `DT3-B1` *(3 ảnh + tái tạo đúng từng byte ×3 + quan hệ cha)* · 3 `DT3-B2` *(ca phá mỗi ảnh)* · 8 `AC-3` *(máy quét PII + ca phá)* · 4 `AC-4` · 22 chốt khuôn *(atl 12 · mm 6 · cdt 4)* |
| `tests/du_lieu/test_dong_bang_sheet.py` *(+12 −3)* | ⚠ **Viết lại MỘT bài DT2**: `test_KHUON_ix_fx_la_mot_tep_…` ghim `danh_sach_khuon() == ['ix_fx']` — ĐỎ khi thêm ba tệp khuôn *(`1 failed, 104 passed` · `['atl_cay', …] == ['ix_fx']`)*: tiền đề "chỉ một khuôn" hết đúng, mà thêm khuôn = thêm TỆP chính là điều bài canh. **Lo gốc giữ**: `ix_fx` được tìm thấy · công cụ thấy ĐÚNG tập tệp khuôn của thư mục *(⛔ sót, ⛔ thừa)* · mã công cụ ⛔ mang dữ liệu khuôn. Lý do ghi trong docstring bài |

## TDD — ĐỎ trước *(Substep 2.3)*
| Lượt | Lệnh · exit · dòng tổng kết | Đỏ vì |
|---|---|---|
| **Đỏ 1** *(42 bài đầu, trước mọi dòng mã)* | `.venv/bin/python -m pytest tests/du_lieu/test_anh_cau_hinh.py -rf` · exit **1** · `34 failed, 8 errors in 1.33s` | THIẾU hành vi, ⛔ lỗi cú pháp *(đếm theo node id: 20 + 10 + 4 = 34 failed · 8 errors)*: 20 bài giao kèo ⇒ `` ⛔ TỪ CHỐI: khuôn `gia_chu` (gia_chu.py) sai giao kèo: KIEU_KHOA='ma' ⛔ thuộc ['yyyymm'] `` *(exit 2 thay 0/1/3)* · 10 bài ảnh *(4 `DT3-B1` · 3 tái tạo · 3 `DT3-B2`)* ⇒ `FileNotFoundError: …/tests/fixture/cau_hinh/atl_cay.json` *(và `mapping_master_cfg.json` · `cdt_correct.json`)* · 4 bài AC-4 ⇒ `` khuôn `atl_cay` ⛔ có ở khuon_dong_bang/ (có: ['ix_fx']) `` · 8 lỗi fixture `km` ⇒ `FileNotFoundError: …/tools/khuon_dong_bang/mapping_master_cfg.py` |
| Xanh 1 *(công cụ)* | `pytest tests/du_lieu/test_dong_bang_sheet.py` ⇒ `63 passed in 4.97s` · `pytest … -k GIAO_KEO` ⇒ `3 failed, 20 passed` *(3 = AC-4 chưa có khuôn — đúng chờ)* | — |
| Xanh 2 *(3 khuôn + 3 ảnh)* | `pytest tests/du_lieu/test_anh_cau_hinh.py` ⇒ `42 passed in 1.84s` | — |
| **Đỏ 2** *(bài DT2 cũ)* | `pytest tests/du_lieu` ⇒ exit **1** · `1 failed, 104 passed in 5.77s` · `assert ['atl_cay', '...g_master_cfg'] == ['ix_fx']` | tiền đề "một khuôn" hết đúng ⇒ viết lại giữ lo gốc *(xem "Đã đổi")* ⇒ `105 passed` |
| Bài viết SAU mã *(23 bài: 22 chốt khuôn + `test_GIAO_KEO_ban_tho_CO_cot_RIENG_TU_…`)* | chứng minh ĐỎ bằng **đột biến** *(bảng dưới)* — ⚠ ⛔ đỏ-trước-mã | bài học `DT2-R1-04`: chốt chạy đúng mà ⛔ bài canh |

### Đột biến — mỗi chốt mới bị phá MỘT lần, chạy `pytest tests/du_lieu`, trả nguyên *(kịch bản `try/finally`, ⛔ commit)*
**26/26 bị cắn.** Lượt đầu **25/26** — `C1` *(`KIEU_COT = {"cdt1_chuan": "chu?"}`)* **SỐNG** `124 passed` ⇒ thêm 4 bài `test_KHUON_cdt_correct_moi_chot_CAN` ⇒ chạy lại `1 failed, 127 passed`, trả nguyên `128 passed`. Tương tự `A3` *(tiêu đề nhóm ⛔ xoá ngăn)* sẽ SỐNG trên dữ liệu thật *(mọi nhóm mở bằng dòng L1)* ⇒ bài `test_KHUON_atl_cay_tieu_de_nhom_XOA_ngan_…` viết TRƯỚC lượt đột biến.

| # | Phá | Kết *(dòng tổng kết `tests/du_lieu`)* |
|---|---|---|
| T1 | bỏ cổng `PHU_MONG` | `4 failed, 120 passed` |
| T2 | bảng phụ ⛔ vào checksum | `6 failed, 118 passed` |
| T3 | khoá `ma` luôn hợp lệ | `2 failed, 122 passed` |
| T4 | trùng ⛔ gộp khoảng trắng | `1 failed, 123 passed` |
| T5 | bỏ đếm ô ⛔ chữ | `2 failed, 122 passed` |
| T6 | ⛔ soát tên cột bảng phụ | `1 failed, 123 passed` |
| T7 | `ValueError` của `chuan_bi` ⇒ LỖI thay TỪ CHỐI | `14 failed, 110 passed` |
| T8 | ⛔ so bảng phụ với `PHU_MONG` | `1 failed, 123 passed` |
| T9 | ⛔ kiểm `KIEU_COT` lúc nạp | `2 failed, 122 passed` |
| T10 | `chu?` cũng ⛔ được rỗng | `7 failed, 117 passed` |
| T11 | ⛔ soát `cot` bản thô trước `chuan_bi` | `1 failed, 123 passed` |
| T12 | `PHU_MONG` mà ⛔ `chuan_bi` vẫn nhận | `1 failed, 123 passed` |
| A1 | tiêu đề nhóm ở cột bất kỳ | `1 failed, 123 passed` |
| A2 | nhóm ⛔ khai ⇒ ⛔ đỏ | `1 failed, 123 passed` |
| A3 | tiêu đề nhóm ⛔ xoá ngăn | `1 failed, 123 passed` |
| A4 | dòng trống xoá ngăn | `2 failed, 122 passed` |
| A5 | cấp = `cap_cot` *(⛔ +1)* | `3 failed, 121 passed` |
| A6 | ⛔ kiểm vùng đọc bắt đầu cột A | `1 failed, 123 passed` |
| A7 | ⛔ thiếu nhóm | `1 failed, 123 passed` |
| M1 | ⛔ băm | `2 failed, 122 passed` |
| M2 | ⛔ kiểm tiêu đề `A:B` dòng 1…3 | `2 failed, 122 passed` |
| M3 | LE so ⛔ `strip` *(`'Cash Treasury '` bị băm)* | `3 failed, 121 passed` |
| M4 | băm từ dòng 1 | `3 failed, 121 passed` |
| M5 | chỉ băm `B` *(`A` rõ)* | `3 failed, 121 passed` |
| M6 | ⛔ kiểm ô chuỗi | `1 failed, 123 passed` |
| C1 | `cdt1_chuan` được rỗng | `1 failed, 127 passed` *(sau khi thêm bài)* |

## Cổng *(kết quả nguyên văn — cụm 5436, venv `/home/user/FLS-tobe/.venv`, `PG_DSN`/`PG_DSN_TEST` = 5436 đặt trước mọi lệnh)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/du_lieu` *(bài của bước + hồi quy thư mục chạm tới)* | exit 0 · `128 passed in 7.87s` trên `78baa20` · `128 passed in 7.31s` trên **`2a31f76`** *(= 63 DT2 + 65 DT3)* |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5436` · **lượt 1** *(cây làm việc = đúng nội dung `78baa20`, chạy ngay trước commit)* | exit 0 · `[ĐẠT]` ×7 kiểm môi trường *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `Contracts: 11 kept, 0 broken. (exit 0)` · `chay 9845 / co 9967 (exit 0)` · `fls_itl = 0 dòng (kết nối chỉ đọc)`)* · toàn bộ `12 failed, 2590 passed, 2 xfailed, 14 errors in 318.65s (0:05:18)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 181.62s (0:03:01)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. Mẫu số: 12 + 2590 + 2 + 14 = **2618** = `--collect-only`; bài `tests/du_lieu` trong tập đỏ **0**; `skipped`/`deselected` **0** |
| `… --duong-nen --cong 5436` · **lượt 2** *(trên **`2a31f76`**, cây sạch trừ phiếu này chưa commit)* | exit 0 · `[ĐẠT]` ×7 kiểm môi trường *(như lượt 1)* · toàn bộ `12 failed, 2590 passed, 2 xfailed, 14 errors in 321.72s (0:05:21)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 179.86s (0:02:59)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong`. `tests/du_lieu` trong tập đỏ **0**; `skipped`/`deselected` **0** |
| `.venv/bin/lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` *(`tools/` ngoài `root_package = fls`)* |
| `python -m fls.db.pg_migrate` | exit 0 · `khong co gi de ap` · `pg_verify: khop` *(⛔ chạm schema)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-dt3/.venv/Scripts/lint-imports.exe'` *(gọi cứng đường Windows — y hệt `BG-066` · `BG-086`)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | *(đo SAU khi có phiếu này — xem dòng cuối mục "Cổng (sau phiếu)")* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — trùng nguyên văn đường nền `BG-066` · `BG-086` *(kho rỗng)*; công cụ đọc `docs/**.md` + kho, bước này ⛔ chạm |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 41 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Kết |
|---|---|---|
| **AC-1** *(DT3-B1)* — 3 ảnh, mỗi số có nhãn Đ4 | **Lượt đóng băng thật** *(bản thô orchestrator, đường mặc định — chỉ ghi khi ĐẠT)*: `python tools/dong_bang_sheet.py atl_cay $THO/atl_cay_A7_F88.json --mong 74` ⇒ exit 0 · `bản thô    : 81 hàng ⇒ chuan_bi dựng bảng 6 cột = khoá 1 + chọn 5 + ⛔ chọn 0 · 74 dòng + bảng phụ 7 dòng` · `[ĐẠT] cổng --mong 74: 74 dòng = mong · trùng 0 · thiếu 0 · khoá hỏng 0 · ô rỗng 0/296 · ô ⛔ số 0/148 · ô ⛔ chữ 0/222 · phụ dong_trong 1 = mong · phụ nhom 6 = mong` · `… mapping_master_cfg … --mong 73` ⇒ exit 0 · `85 hàng ⇒ … 73 dòng + bảng phụ 91 dòng` · `[ĐẠT] cổng --mong 73: 73 dòng = mong · … ô ⛔ chữ 0/365 · phụ bam 7 = mong · phụ loai 0 = mong · phụ tho 84 = mong` · `… cdt_correct … --mong 13` ⇒ exit 0 · `[ĐẠT] cổng --mong 13: 13 dòng = mong · … ô ⛔ chữ 0/13`. **Nhãn Đ4** *(ở docstring bài + khuôn)*: **74** = dòng MÃ *(nhãn `MÃ \| Tên`)*, ⛔ kể 6 tiêu đề nhóm + 1 dòng trống — 81 hàng đọc `A7:F87` = 74 + 6 + 1 · **6** = dòng tiêu đề nhóm `HDO · HDH · HDAP · HDT · HDC · HDCI` · **73** = mã `hd` mà `doc_cot` trả *(⛔ 85 hàng của lưới)* · **13** = dòng CÓ DỮ LIỆU ở `BR11:BS23` *(⑪ — ⛔ 18 = khoảng Ô)*. **Bài**: `test_DT3_B1_anh_cay_ATL_74_dong_MA_6_NHOM_dung_cay_AP_3_2_5` *(từng nhóm mang ĐÚNG các mã của AP §3.2.5, đúng thứ tự — 38 · 4 · 1 · 1 · 23 · 7 = 74; dòng sheet 7…87 phủ kín)* · `…_cay_ATL_cha_va_cap_suy_tu_THUT_COT_dung_nhom` *(mọi `cap(cha) = cap − 1`, cùng nhóm, đứng trên; L1–L4 đều có; `OMC→MAC` · `COT→CAC` · `OSF→CXI` · `CXP→CDC` · `CRO→NCFO` · `CFO→NCFF` · `CXA→GAC`)* · `…_anh_Mapping_Master_73_ma_hd_la_DAU_RA_doc_cot` *(chính `tom_tat` của adapter trên dòng ảnh = số đo **28/08**: `ma 73 · can_phan_bo 23 · co_phuong_phap 21 · method_rong 52 · co_coa1 0 · co_coa2 0`; ATL − MM = `{NCF}`)* · `…_anh_CDT_Correct_13_dong_co_du_lieu` · `…_anh_TAI_TAO_dung_tung_byte_tu_cong_cu[×3]` *(bản thô tái tạo đúng hình dạng orchestrator từ ảnh ⇒ chạy lại ⇒ đúng từng byte)*. Checksum ghim + tính lại bằng `AnhChup` | đạt |
| **AC-2** *(DT3-B2)* — xoá 1 dòng ở BẢN SAO ⇒ ĐỎ `N−1 ≠ N`, trả nguyên ⇒ xanh, mỗi ảnh một ca | **Trên bản sao bản thô THẬT** *(nháp `scratchpad/fe_dt3/`, ⛔ commit)*: cây ATL xoá dòng sheet 14 *(`OTMC`, lá)* ⇒ `python tools/dong_bang_sheet.py atl_cay <bản sao> --mong 74 --ra <nháp>/do_atl_cay.json` ⇒ exit **1** · `[ĐỎ] cổng --mong 74: 73 dòng ≠ mong 74 — ảnh đã ghi ĐÚNG NGUỒN, ⛔ sửa; ⛔ dùng ảnh này khi cổng chưa đạt`; trả nguyên ⇒ exit **0** · `[ĐẠT] …` · `cmp` = ảnh đã commit **từng byte**. Mapping Master xoá dòng sheet 13 ⇒ exit **1** · `` [ĐỎ] cổng --mong 73: 72 dòng ≠ mong 73 · phụ `tho` 83 dòng ≠ mong 84 — … ``; trả nguyên ⇒ exit 0 · `cmp` khớp. CDT Correct xoá dòng 5 ⇒ exit **1** · `[ĐỎ] cổng --mong 13: 12 dòng ≠ mong 13 — …`; trả nguyên ⇒ exit 0 · `cmp` khớp. Ảnh đã commit ⛔ bị đụng *(`git status` sạch phần `tests/fixture`)*. **Bài**: `test_DT3_B2_xoa_mot_dong_o_BAN_SAO_thi_DO_N_tru_1_khac_N_tra_nguyen_thi_XANH[atl_cay\|mapping_master_cfg\|cdt_correct]` *(trên bản thô tái tạo — vì bản thô thật ⛔ commit)* | đạt |
| **AC-3** — ⛔ PII: quét ảnh ⇒ 0 tên người / Email / Diễn giải / Số chứng từ, máy kiểm, có ca phá | **Máy quét** `quet_pii` *(trong bài)*, bốn luật: R1 ⛔ khoá/tên cột thuộc `PM_COT_RIENG_TU` ∪ {`Diễn giải`, `Số chứng từ`} *(gộp khoảng trắng, ⛔ hoa thường)*; R2 ⛔ chuỗi dạng email; **R3 ⛔ chuỗi RÕ của giá trị đã băm** — băm cả chuỗi và từng từ *(nguyên · viết hoa)* rồi so với 14 mã băm có trong ảnh: **⛔ cần biết tên, ⛔ tên nào nằm trong bài**; R4 bảng phụ `tho` từ dòng 4: `B` ∈ 21 pháp nhân đã khai hoặc là mã băm, `B` băm thì `A` băm. `test_AC3_ba_anh_quet_PII_bang_0_tren_mau_so_KHAC_0` ⇒ 0 vi phạm trên 3 ảnh; mẫu số: **14** mã băm *(7 hàng × A·B)* · **76** dòng có LE *(4…79)* · khoá/chuỗi > 0. **Ca phá** `test_AC3_ca_pha_may_quet_CAN_tung_luat[R1_khoa_Email_Address · R1_cot_Dien_giai · R2_email · R3_ten_ro_lot_vao_ANH_KHAC]` + `…_R4_LE_ro_KHONG_khai…` *(B rõ ⛔ khai · A rõ ở hàng băm)*. **Đóng khi lạ**: `test_AC3_khuon_BAM_moi_LE_KHONG_khai_dong_khi_la_va_cong_DO_8_khac_7` — một hàng tổng hợp LE `GIALAPX` ⇒ bị băm ⛔ ai khai trước, chuỗi rõ ⛔ có trong ảnh/stdout/stderr, `` phụ `bam` 8 dòng ≠ mong 7 `` ⇒ exit 1. **Quét tệp**: `test_AC3_tep_ma_va_anh_cua_DT3_KHONG_mang_chuoi_ro_…` — R3 trên MỌI từ của 9 tệp DT3 *(công cụ · 3 khuôn · 2 tệp bài · 3 ảnh; > 10.000 từ)* ⇒ 0. **Đo NGOÀI repo** *(danh sách 7 tên lấy từ `canh_bao_rieng_tu` của bản thô, ⛔ in)*: `0 lần xuất hiện tên` ở cả 11 tệp `tests/fixture/cau_hinh/*.json` · `tools/khuon_dong_bang/*.py` · `tools/dong_bang_sheet.py` · `tests/du_lieu/test_anh_cau_hinh.py`; số tài khoản cá nhân trong ảnh MM: **0**; phiếu này + message hai commit: soát cùng cách ⇒ 0 *(xem "Cổng (sau phiếu)")*. Khoá `canh_bao_rieng_tu`/`ghi_chu` của bản thô ⛔ bao giờ vào ảnh *(`_chuan_bi` chỉ chép `nguon · doc_luc · cach_doc`)* | đạt |
| **AC-4** — khuôn mới = tệp riêng; ⛔ sửa công cụ trừ khi bài đòi | 3 tệp `tools/khuon_dong_bang/{atl_cay,mapping_master_cfg,cdt_correct}.py`; `test_AC4_ba_khuon_DT3_la_ba_TEP_RIENG_va_cong_cu_KHONG_mang_du_lieu_cua_chung` *(hằng chuỗi ngoài docstring của công cụ ∩ {`IX.HD` · `IX.ORG` · `hd_code` · `cdt_nguon` · `HDO` · đường ảnh · `sha256_16:` …} = ∅)* · `test_AC4_khuon_KHAI_duong_anh_va_qua_giao_keo_luc_nap[×3]`. **Công cụ CÓ sửa** — lý do + đo ĐỎ ở dòng `tools/dong_bang_sheet.py` mục "Đã đổi" và docstring công cụ *(mục "⭐⭐ DT3 — bốn mục TUỲ CHỌN")*; mọi mục là tuỳ chọn ⇒ `ix_fx` y nguyên *(63/63 bài DT2 · tái tạo đúng từng byte · sha256 ảnh = `BG-086`)* | đạt *(có sửa công cụ, đã khai)* |
| **AC-5** *(Q8)* — bài mới cộng vào `MONG_PYTEST_TOAN_BO` cùng commit | ⚠ **`MONG_PYTEST_TOAN_BO` ⛔ có trên `isp/DT3`**: biến sinh ở `isp/S0` @ `1291ad5` *(vòng sửa R2 của S0, `= 2460`)*, sau điểm tách `3d8318c` của `isp/DT2` ⇒ `grep -n MONG_PYTEST tools/dung_moi_truong_isp.sh` = 0 dòng; `--duong-nen` ở nhánh này so TẬP ĐỎ *(⛔ đếm mẫu số tối thiểu)*. ⇒ ⛔ nâng được trong cùng commit; ⛔ tự chép cơ chế của S0 *(đụng phần S0, xung đột khi gộp)*. **Số để orchestrator cộng khi gộp**: `pytest --collect-only` **2553 → 2618** *(+65 — đúng bằng `--collect-only tests/du_lieu/test_anh_cau_hinh.py` = `65 tests collected`; `test_dong_bang_sheet.py` giữ `63`)*; lượt `--duong-nen` CHẠY 12 + 2590 + 2 + 14 = 2618. Câu hỏi Q1 dưới | **⛔ làm được trên nhánh** — chờ quyết định |

## Kho thật
- `KHONG_CHAM`. Công cụ + khuôn ⛔ nối kho *(`WO-106`: "Ghi kho THẬT: `KHONG`")*; cụm 5436 chỉ phục vụ `--duong-nen` + cổng. `FLS_CHO_GHI_THAT` ⛔ đặt.

## Cách chạy để xem
- N/A — bước dữ liệu, ⛔ màn. Đóng băng lại *(cần bản thô ở scratchpad orchestrator)*: `python tools/dong_bang_sheet.py atl_cay <thô> --mong 74` · `… mapping_master_cfg <thô> --mong 73` · `… cdt_correct <thô> --mong 13` ⇒ ghi `tests/fixture/cau_hinh/<khuôn>.json` *(cổng ĐỎ ⛔ `--ra` ⇒ tệp cạnh `<khuôn>.DO.json`, ⛔ đè)*.

## Dev tự thấy còn yếu *(Test soi chỗ này trước)*
1. **Sửa công cụ CHUNG, ⛔ chỉ thêm khuôn.** Bốn mục tuỳ chọn *(+201 −29 dòng)* là thay đổi lớn hơn tinh thần "khuôn mới = một tệp". Đã chặn hồi quy bằng: 63/63 bài DT2 xanh, `ix_fx.json` tái tạo đúng từng byte, câu `khong_mang_PII`/dòng `[ĐẠT]` của khuôn ⛔ khai mục mới giữ từng chữ. ⚠ Chỗ nghi: `doc_ban_tho` ⛔ còn kiểm `cot`/`dong` — phép kiểm dời sang `_kiem_bang` *(gọi đầu `dong_bang`, cùng lời)*; ai gọi thẳng `doc_ban_tho` rồi tự đọc `tho["cot"]` sẽ ⛔ được chặn *(grep: chỉ `main` gọi)*.
2. **Checksum ghim SAU lượt đóng băng đầu**, ⛔ khai trước như DT2 *(`CHECKSUM_IX_FX` tính độc lập trước khi có công cụ)*. Phép so độc lập của DT3 là `CAY_AP` *(AP §3.2.5)* + `TOM_TAT_28_08` *(docstring adapter)* + tái tạo đúng từng byte — đủ cho CẤU TRÚC, nhưng ⛔ có bản thứ hai của phép suy `cha` *(bài kiểm `cap(cha) = cap − 1` + 7 quan hệ đọc từ AP)*.
3. **Muối CÔNG KHAI ⇒ mã băm DÒ NGƯỢC được.** Tên viết tắt 5–7 chữ cái hoa ⇒ vét cạn tính bằng phút. Băm ở đây đạt "⛔ chép tên vào repo" + "nối được", **⛔ đạt "giấu"** — đã ghi thẳng trong khuôn và `ghi_chu_khuon`. Câu hỏi Q2.
4. **Luật băm dựa trên danh sách 21 LE đo 16/11** *(`LE_PHAP_NHAN`)* — đóng khi lạ *(LE mới ⇒ bị băm + cổng `bam` ĐỎ)*, nên lỗi chỉ có thể là **báo động giả** *(pháp nhân mới bị băm)*, ⛔ lọt tên. ⚠ Nhưng cột `D:G` *(và `A` của hàng có LE đã khai)* ⛔ được soát nội dung — chỉ R3 *(chuỗi rõ của giá trị ĐÃ băm)* canh; một tên MỚI chưa từng bị băm mà nằm ở `D:G` thì ⛔ máy nào bắt *(đo 16/11: `D:G` chỉ có `x` + 6 cặp tiêu đề nhóm + nhãn dòng 1…6)*.
5. **`A` của hàng LE đã khai giữ RÕ** — gồm số tài khoản **công ty** *(đã có ở repo: `Ra-soat-Cau-truc-R-va-ERD.md:33` …)* và một tên sheet mang **mảnh tên riêng** *(dòng sheet 45, LE `CN`; chuỗi ấy đã có ở **21 tệp** trước bước này — `git grep -l` trên `2a31f76` = 22 trừ ảnh MM của bước: `fls/db/schema.py` · 3 fixture `tests/fixture/*.json` · 17 tài liệu `docs/` — ⚠ bản nháp phiếu ghi "schema.py + 3 tệp docs", đếm lại mới thấy 21 — Đ1)*. Theo tiền lệ repo ⇒ giữ. Câu hỏi Q3.
6. **Tên người CÓ SẴN trong repo** *(⛔ do bước này)*: `git grep` 7 tên ⇒ có ở **6 tệp** *(1 di trú `0004` + 5 tài liệu)* — ngoài phạm vi, chỉ ghi số đếm.
7. **Hai `mong` giòn có chủ ý**: `phu.dong_trong = 1` và `phu.tho = 84` — bố cục sheet đổi một dòng là ĐỎ. Đúng Đ5 *(`dong_sheet` phía sau trượt theo)* nhưng sẽ kêu ở lượt đọc lại kế tiếp nếu kế toán dọn dòng trống.
8. **`thieu_lac` "⛔ áp dụng"** cho Mapping Master và CDT Correct *(trả rỗng, `dai` nói lý do)* — cổng của hai bảng = `--mong` + khoá + ô + bảng phụ. CDT Correct ⛔ đóng *(`SHQ1 \| Headquarters1` · `ASA \| Super App` chỉ có ở cột chuẩn)* — ghi ở docstring, để C8.
9. **`cap_cot` tin theo orchestrator** *(cột nhãn `B…E` ⇒ 0…3)* — ⛔ đọc lại sheet được để kiểm phép chuyển ấy. CDT Correct in `ô ⛔ số: 0/0` *(⛔ cột số — mẫu số 0 là KẾT QUẢ, Đ3)*.
10. **Một bài DT2 bị viết lại** *(`test_KHUON_ix_fx_la_mot_tep_…`)* — lý do ở docstring bài; R1 nên đối chiếu lo gốc.
11. **AC-5 ⛔ làm được trên nhánh** *(biến ⛔ có)* — Q1.

## Câu hỏi còn treo *(gửi orchestrator — ⛔ chặn R1)*
- **Q1 · Q8 trên nhánh ⛔ có `MONG_PYTEST_TOAN_BO`.** **A *(khuyến nghị)*** — orchestrator đặt số khi gộp `isp/S0` + các nhánh: `MONG_PYTEST_TOAN_BO` = số của S0 + Δ từng nhánh *(Δ DT3 = **+65**, đếm `--collect-only` trước/sau)*. Được: ⛔ xung đột, một chỗ ghi; mất: R1 của DT3 ⛔ thấy cổng số bài. · **B** — tôi chép cơ chế `MONG_PYTEST_*` của `isp/S0` vào nhánh này. Được: AC-5 làm được tại chỗ; mất: đụng phần S0 đang ở R3, xung đột chắc chắn khi gộp.
- **Q2 · Muối của mã băm.** **A *(khuyến nghị cho DT3)*** — giữ muối công khai *(tái tạo được, bài canh được, nối được; repo vốn đã có 7 tên ở 6 tệp)*. · **B** — muối BÍ MẬT ngoài repo *(biến môi trường)* trước C8: giấu thật, nhưng ảnh ⛔ tái tạo được ở máy ⛔ có muối và bài R3 phải đọc muối từ môi trường. Quyết định của owner.
- **Q3 · Tên sheet mang mảnh tên riêng ở `A` *(LE công ty)*.** **A *(khuyến nghị)*** — giữ *(đã có ở 21 tệp của repo — `fls/db/schema.py` + fixture + `docs/`; ⛔ phải tài khoản cá nhân)*. · **B** — băm thêm theo danh sách khai tay *(⛔ đóng khi lạ — cần ai đó liệt kê)*.

## Cổng (sau phiếu)
| Lệnh | Kết quả |
|---|---|
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (179 file, 1882 bang, 726 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo lần cuối trên bản phiếu được commit; lần đầu, trước khi thêm hàng lượt 2: `179 file, 1881 bang`)* |
| Soát tên người — đo NGOÀI repo *(7 tên + 7 số tài khoản cá nhân lấy từ bản thô, ⛔ in)* | `BG-107: 7 tên → 0 lần · 7 số TK cá nhân → 0 lần` · `message 78baa20: 7 tên → 0 lần · 7 số TK cá nhân → 0 lần` · `message 2a31f76: 7 tên → 0 lần · 7 số TK cá nhân → 0 lần` *(BG-107 đo lại sau khi thêm hàng lượt 2: vẫn 0 · 0)*; message commit phiếu soát cùng cách trước khi commit ⇒ 0 |
