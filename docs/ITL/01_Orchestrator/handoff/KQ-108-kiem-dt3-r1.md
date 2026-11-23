# KQ-108 — biên bản kiểm `BG-107` *(R1 · ISP 3.1.2 · Step 10 · `DT3`)*

| | |
|---|---|
| **Thuộc** | `BG-107` · `WO-106` *(⑪ CDT = 13 · ⑫ `AA:AD` ⛔ thuộc RAW)* |
| **Kiểm bởi** | `fls-test` — R1, phiên mới độc lập · 2026-11-17 · cụm PG **5446** · worktree `.claude/worktrees/isp-dt3` |
| **Đối tượng** | `git diff 80496ec isp/DT3` *(mã `2a31f76` + BG `5a96cd9`)* — 10 tệp, +5476 −32 |
| **Phán quyết** | **`TRƯỢT`** — **1 CHẶN** *(`DT3-R1-01` mã băm PII đảo ngược được)* · 1 NÊN SỬA · 5 GHI NHẬN. Phần còn lại *(ba ảnh, đường ống, cổng hồi quy)* **ĐẠT** có bằng chứng |

Sổ phát hiện riêng: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT3.md` *(v0.1, 7 hàng)*.
⛔ Phiếu này ⛔ chứa tên người, số tài khoản cá nhân, chuỗi tên sheet cá nhân hay mã băm của chúng — chỉ số đếm.

## Cổng vào
- git: worktree ở `isp/DT3` @ `5a96cd9`, cây sạch; `git log 80496ec..isp/DT3` = đúng 2 commit `2a31f76` · `5a96cd9` = khớp `BG-107`. ⚠ `BG-107` ghi *"nhánh cục bộ … ⛔ đẩy"* — đo: cả hai commit **đã có trên remote** `origin/isp-chuyen/DT3` và `origin/claude/laughing-bohr-331pt0-isp/DT3` *(đẩy lúc chuyển account 17/11, ⛔ lỗi của Dev — nhưng chạm `DT3-R1-01` ④)*.
- spec: ISP 3.1.2 `## Step 10 · DT3` *(dòng 1182)* · `WO-106` *(ở checkout chính — ⛔ có trên `isp/DT3`, như BG khai)* · `CLAUDE.md` Đ1–Đ5.
- Nguồn đối chiếu: lưới SA orchestrator đọc lại 17/11 03:19 UTC *(`UNFORMATTED_VALUE`)* ở `scratchpad/drive_tho/sa_*.json`; bản thô 16/11 ⛔ chuyển sang *(⛔ dùng)*.

## Cổng chạy lại *(R1 tự chạy — `PG_DSN`/`PG_DSN_TEST` = cổng 5446 đặt trước mọi lệnh)*
| Lệnh | `BG` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/du_lieu/test_anh_cau_hinh.py tests/du_lieu/test_dong_bang_sheet.py` | `128 passed` | exit 0 · `128 passed in 5.48s`; `--collect-only test_anh_cau_hinh.py` = `65 tests collected` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5446` | `KẾT: ĐẠT` *(5436)* | exit 0 · `[ĐẠT]` ×7 kiểm môi trường *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `11 kept, 0 broken` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2590 passed, 2 xfailed, 1 warning, 14 errors in 307.84s` *(mẫu số 12 + 2590 + 2 + 14 = **2618** = số BG)* · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 174.25s` · `[ĐẠT] … 3 = 3 node id (thêm 0 · bớt 0)` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` | ✅ |
| `.venv/bin/lint-imports` | `11 kept, 0 broken` | exit 0 · `Contracts: 11 kept, 0 broken.` | ✅ |
| `python tools/kiem_so_song.py` | ⛔ đo được *(đường Windows)* | exit 1 · `FileNotFoundError … .venv/Scripts/lint-imports.exe` — **⛔ KHÔNG ĐO ĐƯỢC**, y BG | ✅ *(cùng trạng thái)* |
| Đường ống trên lưới SA *(R1 tự chuyển lưới → hình dạng khuôn nhận, meta lấy từ ảnh; `--ra` nháp)* | ảnh = đầu ra công cụ | `atl_cay --mong 74` exit 0 `[ĐẠT] … 74 dòng = mong … phụ dong_trong 1 = mong · phụ nhom 6 = mong` · `mapping_master_cfg --mong 73` exit 0 `[ĐẠT] … phụ bam 7 · loai 0 · tho 84 = mong` · `cdt_correct --mong 13` exit 0 `[ĐẠT] … 13 dòng = mong`; **`cmp` ×3 = ảnh đã commit TRÙNG TỪNG BYTE** ⇒ checksum `77ca9d6c74f4254a` · `e96f6d1a86a03320` · `30aea854bd879f6d` khớp | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` *(sau khi thêm phiếu + sổ)* | — | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (181 file, 1891 bang, 728 o ngay, 104 ma QD)` | — |

## Đối chiếu độc lập ảnh ↔ lưới SA *(mã R1 ở nháp, ⛔ dùng mã tác giả)*
| Ảnh | Mong | R1 đếm trên lưới SA *(nhãn · mẫu số)* | Ô so | Lệch |
|---|---|---|---|---|
| `atl_cay.json` | 74 · 6 | dòng sheet 7…87 = **81** hàng = **74** dòng MÃ *(đúng một ô `B…E` dạng `MÃ \| Tên`, `F` = nhãn ở cả 74)* + **6** tiêu đề nhóm *(hai ô `B` mã · `C` tên: dòng 7·47·52·54·56·80)* + **1** dòng trống *(35)*; hàng 88 rỗng, 89 = `CHECK ZONE` *(ngoài vùng)*. `cha` tính bằng thuật toán KHÁC khuôn *(quét ngược tìm cấp k−1, dừng ở tiêu đề nhóm)*: 0 dòng nhảy cấp | 462 = 74 × 6 *(ma·ten·cha·cap·nhom·dong_sheet)* + 6 × 3 | **0** |
| `mapping_master_cfg.json` | 73 | **73** = ô `H` khác rỗng từ dòng 7 *(đếm thẳng, ⛔ qua `doc_cot`)*, dòng 7…85, trùng 0; bảng phụ `tho` = **84** dòng có ô ở `A:B·D:G` *(tập dòng khớp)*; hàng cá nhân theo luật LE = **7** *(dòng 70…76)* = `phu.bam` | 438 = 73 × 6 *(H…M)* + 504 = 84 × 6 *(A·B·D·E·F·G, ô băm so với băm lại)* | **0** |
| `cdt_correct.json` | 13 | API trả 16 hàng cho 25 hàng hỏi `BR8:BS32`; hàng có ô = 14 = tiêu đề `BR10` + **13** dòng dữ liệu `BR11…BR23` | 26 = 13 × 2 | **0** |

⇒ **1430/1430 ô khớp** · sheet ⛔ đổi giữa 16/11 và 17/11 03:19 trên ba vùng · khuôn ghi đúng nguồn. ⛔ đo được: `Q1:AN120` RỖNG *(⑫)* — lưới SA chỉ đọc `A:P` ⇒ R1 ⛔ xác nhận; ⛔ ảnh hưởng AC *(ảnh ⛔ mang `AA:AD`)*.
*(c)* Bảng chính Mapping Master = đầu ra `doc_cot`: khuôn `import` `doc_cot`/`TRUONG`/`COT` của adapter *(`mapping_master_cfg.py:47-48`)* — ⛔ có luật đọc thứ hai; số đếm độc lập 73 khớp.

## Ca phá *(BẢN SAO bản thô dựng từ lưới SA, `--ra` nháp; ảnh commit ⛔ đụng — `git status` sạch)*
| Ca | Exit | Dòng kết |
|---|:-:|---|
| ATL xoá lá `OTMC` *(d14)* | 1 | `[ĐỎ] cổng --mong 74: 73 dòng ≠ mong 74` |
| ATL xoá `PL8` *(dòng cuối)* | 1 | `73 dòng ≠ mong 74` |
| ATL xoá tiêu đề `HDH` | 1 | `thiếu 1 · phụ nhom 5 dòng ≠ mong 6` |
| ATL mã trùng *(d9 = `GI`)* | 1 | `trùng 1` |
| ATL xoá dòng trống 35 | 1 | `phụ dong_trong 0 dòng ≠ mong 1` |
| ATL đổi `MAC` L3 → L2 | **0** | `[ĐẠT]` — xem `DT3-R1-06` |
| MM xoá d13 | 1 | `72 dòng ≠ mong 73 · phụ tho 83 dòng ≠ mong 84` |
| MM xoá dòng cuối d85 | 1 | `72 ≠ 73 · tho 83 ≠ 84` |
| MM xoá hàng cá nhân d70 | 1 | `72 ≠ 73 · phụ bam 6 dòng ≠ mong 7 · tho 83 ≠ 84` |
| MM `hd` trùng *(d8 = d7)* | 1 | `72 ≠ 73 · phụ loai 1 dòng ≠ mong 0` |
| CDT xoá dòng 5 | 1 | `12 dòng ≠ mong 13` |
| CDT `cdt1_chuan` rỗng d3 | 1 | `ô rỗng 1/13` |
| CDT nguồn có dòng 14 ở BR24, đọc `BR11:BS23` | **0** | `[ĐẠT]` — xem `DT3-R1-02` |
| Trả nguyên ×3 | 0 | `[ĐẠT]`, `cmp` = ảnh commit từng byte ×3 |

## Bảng AC *(`WO-106`)* và mục 6 · 8 của ISP
| Tiêu chí | Mong | Đo được | Phán quyết |
|---|---|---|---|
| AC-1 · `DT3-B1` | 3 ảnh: 74 dòng mã · 6 nhóm · 73 mã hd · 13 dòng, có nhãn Đ4 | 7 bài `DT3_B1` xanh; đối chiếu độc lập 1430/1430 ô; nhãn Đ4 có ở docstring bài `:8-19` + khuôn + BG *(74 = dòng MÃ ⛔ kể 6 + 1; 13 = dòng có dữ liệu `BR11:BS23`)* | **ĐẠT** |
| AC-2 · `DT3-B2` | xoá 1 dòng ở BẢN SAO ⇒ ĐỎ `N−1 ≠ N`, trả nguyên xanh, mỗi ảnh một ca | 3 bài `DT3_B2` xanh; R1 tự phá trên bản sao từ lưới SA: 73≠74 · 72≠73 · 12≠13 exit 1, trả nguyên exit 0 + `cmp` trùng | **ĐẠT** |
| AC-3 · ⛔ PII | 0 tên / Email / Diễn giải / Số chứng từ, máy kiểm, có ca phá | Quét tên RÕ: **0** lần — 7 tên × 10 tệp diff + message 2 commit *(đối chứng dương cùng máy quét trên lưới SA: 14 lần — Đ3)*; số TK cá nhân 0; chuỗi A cá nhân 0; Email/Diễn giải/Số chứng từ: bài `AC3` có ca phá ×5, xanh. **NHƯNG** mã băm của 7 hàng **đảo được** *(7/7 bằng từ điển 200; 4/7 vét cạn mù trong 5 giây)* ⇒ tên người khôi phục được từ repo | **TRƯỢT** *(`DT3-R1-01`)* |
| AC-4 · khuôn = tệp riêng | 3 tệp `tools/khuon_dong_bang/*.py`; sửa công cụ chỉ khi bài đòi + khai | 3 tệp có; công cụ sửa +201 −29, khai lý do *(BG + docstring)*, 20 bài giao kèo đòi; `ix_fx` tái tạo đúng byte *(bài DT2 xanh)*; `merge-tree isp/DT2 isp/DT3`: công cụ tự gộp sạch | **ĐẠT** *(ghi `DT3-R1-07`)* |
| AC-5 · Q8 | — | `MONG_PYTEST_TOAN_BO` ⛔ có trên nhánh *(grep 0; `isp/S0` có 5 dòng)*; orchestrator chấp nhận Q1 = A ⇒ ⛔ tính là phát hiện. ⚠ số: xem `DT3-R1-04` *(+68 trên cây gộp với DT2-R2, ⛔ +65)* | **chấp nhận** *(orchestrator)* |
| ISP mục 8 ① `DT3-B1`, `DT3-B2` xanh/đỏ đúng | — | như AC-1 · AC-2 | **ĐẠT** |
| ISP mục 8 ② 3 vòng review | — | R1 = phiếu này; R2 · R3 chưa | **chưa** |
| ISP mục 8 ③ điều kiện PUSH | R1·R2·R3, CHẶN = 0 | CHẶN = 1 | **TRƯỢT** |

Đ1 *(câu phủ định của BG, grep hai nơi)*: *"⛔ có `MONG_PYTEST` trên nhánh"* — `tools/` 0 dòng, `isp/S0` 5 ⇒ đúng · *"tên người có sẵn ở 6 tệp"* — R1 `git grep -w` 7 tên trên `isp/DT3` = **6 tệp** *(1 di trú `0004` + 5 `docs/`)* ⇒ đúng, ngoài phạm vi · *"MM ⛔ có `NCF`"* — lưới SA cột H: 0 ⇒ đúng. Đ3: CDT in `ô ⛔ số 0/0` — mẫu số 0 được in và khai là kết quả *(⛔ cột số)* ⇒ đúng luật. Đ5: mọi cổng mới có `mong` *(`--mong` + `PHU_MONG`)*, ca phá ở trên chứng minh ĐỎ.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT trừ PII | Đọc toàn bộ diff đối chiếu Step 10 + `WO-106`: ⑪ ⑫ áp đúng; MM = đầu ra `doc_cot`; cha/cấp đúng *(thuật toán khác cho cùng kết quả)*; 4 mục tuỳ chọn của công cụ có bài + đột biến *(BG 26/26)*. Lỗi: `DT3-R1-01` *(CHẶN)*, `-02` *(mất dòng im lặng)*, `-03` · `-06` *(GHI NHẬN)* |
| **Dữ liệu** | ĐẠT | Kho thật ⛔ chạm *(bước ⛔ nối kho)*; dữ liệu = ba ảnh: 1430/1430 ô khớp lưới SA, mỗi số có nhãn + mẫu số ở bảng trên |
| **Màn hình** | N/A | Bước dữ liệu, ⛔ màn *(ISP mục 4 FE: N/A có lý do)* |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Khuyến nghị cụ thể | Gửi |
|---|---|---|---|---|---|
| `DT3-R1-01` *(A2)* | **CHẶN** | `tools/khuon_dong_bang/mapping_master_cfg.py:68-77` · `:137-146` · `tests/fixture/cau_hinh/mapping_master_cfg.json` *(`phu.tho` d70…76 A·B, `ghi_chu_khuon`)* · `tests/du_lieu/test_anh_cau_hinh.py:840` | Muối `MUOI` công khai trong khuôn và trong ảnh ⇒ ai có repo băm ứng viên rồi so. Từ điển 200 tên viết tắt ⇒ **7/7**; vét cạn mù 26⁵ trong 5 s ⇒ **4/7** *(6–7 chữ ≈ 2 phút · ≈ 1 giờ)*; chuỗi A băm lại 7/7 *(1 mẫu tên sheet)*. Bài `:840` ĐÒI `km.bam(gia) ∈ ảnh` | ① LOẠI: A·B của hàng ⛔ thuộc `LE_PHAP_NHAN` ⇒ hằng `"an_danh:tk_ca_nhan"`; bỏ `bam`/`MUOI`/`MA_BAM` + câu muối trong `ghi_chu_khuon`; bảng phụ `bam` → `an_danh` *(mong 7)*. Cần khoá nối ⇒ HMAC khoá ngoài repo *(owner, Q2 = B)*. ② Bài AC-3 R3 → "⛔ chuỗi `sha256_16:` nào + mọi hàng `an_danh` có A = B = hằng"; `:840` → `gia ∉ ảnh`; thêm bài đề xuất R1-01. ③ Đóng băng lại MM, ghim checksum mới *(vá thử của R1 làm đỏ đúng 10 bài ghim ảnh/hash cũ — tác giả cập nhật)*. ④ VIẾT LẠI `2a31f76` *(⛔ commit chồng)*; orchestrator ⛔ gộp `2a31f76`; owner quyết hai nhánh remote | `DEV` · orchestrator *(④ + Q2)* |
| `DT3-R1-02` *(B1)* | **NÊN SỬA** | `tools/khuon_dong_bang/cdt_correct.py:31-41` · `nguon` của ảnh CDT | Lưới SA + dòng 14 ở BR24, đọc `BR11:BS23` ⇒ `[ĐẠT] --mong 13` exit 0 | Khuôn đòi số hàng vùng `BR<a>:BS<b>` > số hàng bản thô *(`ValueError` ⇒ exit 2)*; orchestrator đọc `BR11:BS32`; đóng băng lại | `DEV` · orchestrator |
| `DT3-R1-03` *(B2)* | GHI NHẬN | `tools/khuon_dong_bang/atl_cay.py:10-19` · `:59` · `:91` | Lưới SA hàng 7…88 ⇒ exit 2 `hàng phải đúng ba khoá A · cap_cot · o` | Hợp đồng bản thô = lưới `values`; khuôn nhận lưới; sửa docstring *("MÃ\|Tên" là quy ước bản thô 16/11, ở sheet là hai ô B·C)* | orchestrator · `DEV` |
| `DT3-R1-04` *(B2)* | GHI NHẬN | `BG-107` AC-5 / Q1 | `merge-tree` DT2 @ `f3f2240` + DT3: `tests/du_lieu` 88 → 156 = **+68** | `MONG_PYTEST_TOAN_BO` đo `--collect-only` trên cây gộp | orchestrator |
| `DT3-R1-05` *(B1)* | GHI NHẬN | `tests/du_lieu/test_dong_bang_sheet.py:817-832` | Bản DT3 = cùng hai `assert` với bản DT2-R2-02 ⇒ ⛔ yếu hơn; xung đột gộp chỉ ở tệp này *(docstring)* | Lấy bản DT2 khi gộp *(cây gộp thử `156 passed`)* | orchestrator |
| `DT3-R1-06` *(B1)* | GHI NHẬN | `tools/khuon_dong_bang/atl_cay.py:115-119` | Đổi `MAC` L3 → L2 ⇒ cổng `[ĐẠT]`; pytest bắt *(checksum + cap(cha))* | Tuỳ chọn: mong theo cấp L1…L4 | `DEV` |
| `DT3-R1-07` *(B2)* | GHI NHẬN | `tools/dong_bang_sheet.py` ↔ errata ⑧ | Công cụ sửa +201 −29 *(hợp lệ theo AC-4)* | Tuần tự hoá thay đổi công cụ chung: nền DT4+ = cây gộp DT2+DT3 | orchestrator |

## Bài đề xuất *(⛔ commit — ở nháp R1; tác giả chép vào `tests/du_lieu/test_anh_cau_hinh.py`)*
Tệp: `scratchpad/r1_dt3/bai_de_xuat/test_r1_dt3_de_xuat.py` *(dữ liệu TỔNG HỢP, ⛔ tên thật; dùng lại trợ thủ `_them_hang_gia_lap` · `_tho_cdt_tu_anh` của bài DT3)*.
| Bài | ĐỎ trên `5a96cd9` | XANH sau |
|---|---|---|
| `test_R1_01_hang_ca_nhan_KHONG_dao_nguoc_duoc_bang_tu_dien_200_ten` — hàng tổng hợp `GIALAPX` + 199 mồi; đòi 0 chuỗi rõ khôi phục được bằng hàm/muối trong repo | `AssertionError: 1 chuỗi rõ khôi phục được` | ✅ trên vá thử *(A·B ⇒ hằng)*: `passed` |
| `test_R1_02_cdt_correct_vung_doc_KHONG_du_hang_sau_du_lieu_thi_TU_CHOI` — `BR11:BS23` + 13 hàng ⇒ đòi exit 2 | exit 0 | ✅ trên vá thử *(`chuan_bi` 6 dòng kiểm biên)*: `passed` |
| `test_R1_03_atl_cay_nhan_LUOI_o_cua_sheet_ra_cung_74_dong` — lưới ô *(tiêu đề nhóm = B mã · C tên)* ⇒ đòi exit 0 + cùng `ma·cha·cap·nhom` | exit 2 `hàng phải đúng ba khoá` | chờ quyết định hợp đồng bản thô |

## Kho thật
`KHONG_CHAM` — bước ⛔ nối kho; cụm 5446 chỉ phục vụ cổng `--duong-nen`. Bài chạy riêng lẻ dùng `--giu-kho` *(⛔ DROP kho test khi lượt `--duong-nen` đang chạy)*.
