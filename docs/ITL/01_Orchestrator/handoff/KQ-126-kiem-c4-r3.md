# KQ-126 — biên bản kiểm `BG-123` *(ISP 3.1.2 · Step 11 · C4 · R3 — vòng cuối, kiểm toàn cục trước gộp)*

| | |
|---|---|
| **Thuộc** | `BG-123` · `WO-122` *(dải: WO-122 · BG-123 · KQ-124 R1 · KQ-125 R2 · KQ-126 R3)* |
| **Kiểm bởi** | `fls-test` — **R3** *(phiên cloud CON độc lập)* · 2026-11-18 |
| **Đối tượng** | nhánh `isp/C4` @ `5837455` *(khớp brief; mã cuối `d6dea99`)* · phạm vi R3 = `git diff 31509bd isp/C4` *(2 tệp: `KQ-125` + sổ — **0 dòng mã**)* + kiểm toàn cục + cây gộp thử · cụm PG riêng **5446** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(chi tiết: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C4.md` v0.3)* |

> **Kết luận gộp:** **ĐỦ ĐIỀU KIỆN GỘP** `isp/C4` vào nhánh làm việc — R1 `ĐẠT` · R2 `ĐẠT` · R3 `ĐẠT`; **0 CHẶN · 0 NÊN SỬA mở**. Cây gộp thử xanh *(xung đột chỉ ở hai tệp sàn dự kiến; `--duong-nen` `KẾT: ĐẠT`)*. Đi kèm **một việc của orchestrator** *(không chặn)*: `C4-R3-03` — `WO-142` thiếu `AC-8` để mang nợ `C4-R2-01…03`.
> Mọi số R3 tự chạy lại; `PG_DSN=…:5446/fls PG_DSN_TEST=…:5446/fls_test PYTHONUTF8=1`. Đột biến trên **bản sao** `git archive isp/C4` *(⛔ chạm worktree; ⛔ sửa mã hệ thống)*. Container Linux — bỏ qua đường Windows/PowerShell. Cây gộp thử ở `/tmp/r3_c4/gop` *(⛔ commit/push)*.

## Cổng chạy lại *(Test tự chạy — so với `BG-123`/`KQ-125`)*
| Lệnh | Đối chiếu | R3 đo *(nhãn · mẫu số)* | Khớp |
|---|---|---|:-:|
| Dựng môi trường S0 `--cong 5446` *(worktree `isp/C4`)* | `KẾT: ĐẠT` | `KẾT: ĐẠT` · 26/26 di trú · pg_verify 25 bảng 0 lệch · `lint-imports 11 kept` · HD1 `9845/9967` · kho `fls_itl = 0` | ✅ |
| `--duong-nen --cong 5446` *(worktree `isp/C4`, **một mình**)* | `KQ-125`: `28 = 28` · chạy 3108 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `12 failed, 3080 passed, 2 xfailed, 14 errors in 377,6s` ⇒ `28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 3108 (mong ≥ 3108) · skipped 0 · deselected 0`; web `3 failed, 664 passed` ⇒ `3 = 3 · chạy 667 (mong ≥ 667)` | ✅ |
| **Cây gộp thử** `--duong-nen --cong 5446` *(`/tmp/r3_c4/gop`, **một mình**, sau việc trên C4)* | — | `KẾT: ĐẠT` · `12 failed, 3113 passed, 2 xfailed, 14 errors in 383,1s` ⇒ `28 = 28 (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 3141 (mong ≥ 3141) · skipped 0 · deselected 0`; web `3 failed, 664 passed` ⇒ `3 = 3 · chạy 667` | ✅ |
| `lint-imports` *(cây gộp)* | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` *(cây gộp)* | ĐẠT · tuyến `/config/hd` | `OK /api/fls/v1/config/hd` · `TINH […ix_hd_cay.json, …ix_mapping_master.json] · vet 13 ham` · `✅ ban khai KHOP SQL that o ca 42 tuyen` | ✅ |
| `kiem_tai_lieu.py` *(cây gộp)* | ĐẠT | `✅ cong tai lieu DAT` · 253 file · 2336 bảng · 784 ô ngày · 104 mã QĐ | ✅ |
| `pytest --collect-only` *(cây gộp, `-o addopts=''`)* | — | **3141** thu thập *(= `grep -c '::'`)*; `tests/web` **667** *(đếm theo tiền tố `tests/web/`)* | ✅ |
| `kiem_so_song.py` | `C4-R1-05(b)` | ⛔ chạy được — đường Windows `tools/kiem_so_song.py:406` *(backlog, orchestrator đã chốt)* | — |

### Cây gộp thử *(`git worktree add /tmp/r3_c4/gop origin/moi/lam_viec` @ `3cac59f` rồi `merge --no-ff --no-commit isp/C4`)*
| Hạng mục | Kết quả |
|---|---|
| **Tệp xung đột** | **2** — `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(đúng dự kiến — sàn)*. ⛔ tệp nào khác |
| Cách giải | `git checkout --ours` *(giữ bản nhánh làm việc: sàn `3100`)* ⇒ nâng `MONG_PYTEST_TOAN_BO` **3100 → 3141** *(= thu thập cây gộp)* và bài ghim `== ["3141"]` *(`tests/test_dung_moi_truong_isp.py:423`)*; `MONG_PYTEST_WEB=667` giữ *(= thu thập `tests/web`)* |
| Phần C4 vào cây gộp | 11 tệp: `hd.py` *(+385)* · `ix_hd_cay.json` · `ix_mapping_master.json` · `bang_tuyen.py` *(+12)* · `xu_ly.py` *(+41)* · 2 tệp bài · `BG-123` · `KQ-124` · `KQ-125` · sổ — ⛔ chạm `fls/db/`, ⛔ chạm `schema.py` |
| Số thu thập | nhánh làm việc **3100** + C4 **41** *(31 `test_hd` + 10 `test_isp_config_hd`)* = **3141** ✅ |
| `KẾT` | **`ĐẠT`** *(`28 = 28` · chạy 3141 · web `3 = 3`)* |
| Dọn | cây gộp ⛔ commit/push; còn để chờ orchestrator *(`git worktree remove --force /tmp/r3_c4/gop`)* |

## Kiểm các mục orchestrator đã chốt
| Mục | Chốt | Ô **Trạng thái** trong sổ *(sau R3)* | |
|---|---|---|:-:|
| `C4-R1-05(a)` | → `C5` · `WO-142` `AC-6b` | **`chuyển`** *(trước R3: "mở → chuyển" — mơ hồ)* | ✅ đã rõ |
| `C4-R1-05(b)` | → backlog | gộp ở ô trên: `(b) → backlog` | ✅ |
| `C4-R2-01` *(≥ 4.301 chữ số · `RecursionError`)* | → `C5` | **`chuyển C5`** *(trước R3: "mở")* | ✅ đã rõ |
| `C4-R2-02` *(câu lỗi dài)* | → `C5` | **`chuyển C5`** | ✅ |
| `C4-R2-03` *(bài biên `_so`)* | → `C5` | **`chuyển C5`** | ✅ |
| **Chỗ đậu bên `WO-142`** | `AC-6b` + `AC-8` | `AC-6b` **có** *(gỡ hai ảnh tĩnh)*; `AC-8` **⛔ có** — `WO-142` chỉ có `AC-1…AC-7` + `AC-6b` *(grep `AC-8` = 0 · `ValueError`/`RecursionError`/`4300`/`C4-R2` = 0)* | ⛔ → `C4-R3-03` |

## Bảng AC *(toàn cục — mã ⛔ đổi kể từ R1)*
| AC | Mong | R3 đo được | Phán quyết |
|---|---|---|---|
| AC-1 `C4-B1` | nạp ảnh ATL 74 nút · 6 nhóm · 37 gốc | đo lại `python -I`: **74** nút · **74** mã duy nhất · gốc **37** · nhóm `HDO·HDH·HDAP·HDT·HDC·HDCI` · cấp `(1,37)(2,23)(3,11)(4,3)` Σ74 | **ĐẠT** |
| AC-2 `C4-B2` | chu trình ⇒ `HD_CHU_TRINH`, ⛔ treo | `test_hd.py` xanh trong `--duong-nen`; R2 đã đột biến lưới | **ĐẠT** |
| AC-3 `C4-B3` | ô/cây hỏng ⇒ `LoiHD` có tên | lối thường ĐẠT; lối cực đoan ⇒ `C4-R2-01` đã **chuyển** `C5` | **ĐẠT** *(+nợ có chủ)* |
| AC-4 `C4-B4` | `GET /config/hd` 200 · 74 · 73 · `chenh = {NCF}` · `?run_id=` ⇒ 400 | `41 passed`; đo: `ATL−MM = ['NCF']` · `MM−ATL = []` *(`Đ3` cả hai chiều)* · MM **73** mã duy nhất · nút lá **64** *(`Đ4`: lá của cây IX.HD, ⛔ cùng nhãn "64 cột có tên" `ITL Ledge`)*; R3-M1 gỡ cổng `run_id` ⇒ ĐỎ | **ĐẠT** |
| AC-6 *(Q8)* | sàn = thu thập, nâng cùng commit | nhánh C4: 3108 = chạy 3108; cây gộp: **3141 = 3141** | **ĐẠT** |
| Ràng buộc *(e)* | `hd.py` ⛔ `psycopg`/`fls.db`; tuyến ⛔ `sum(`; ⛔ hoà giải `74↔73` | `lint-imports` `11 kept`; `soi_bang_tuyen`: tuyến mới SQL `0` bảng; `chenh_mapping_master` chỉ liệt kê | **ĐẠT** |

## Thử phá — 16 đột biến vùng R1/R2 ít đụng *(tuyến `/config/hd`)*
> Chạy `tests/cau_hinh/test_hd.py` + `tests/api/test_isp_config_hd.py` *(`41 passed` gốc)* trên bản sao; mỗi chỗ trả nguyên *(`md5sum` gốc = bản sao; chạy lại `41 passed`)*. Bảng đầy đủ: sổ v0.3, mục R3.

| Nhóm | Mã | Kết |
|---|---|---|
| `?run_id=` ⇒ 400 | R3-M1 gỡ cổng | giết *(`…run_id_o_tuyen_TINH…400`)* |
| `chenh_mapping_master` | R3-M2 đảo chiều · R3-M3 bỏ `sorted` | M2 giết · **M3 SỐNG** *(tương đương trên ảnh thật: 1 mã chênh)* |
| 74 / 73 / 37 | R3-M4 `so_mapping_master=len(nut)` · M9 `so_atl=len(mm)` · M10 `goc`=mọi nút | cả ba **giết** |
| nhãn `data_status` | R3-M6 `flash`⇒`reconciled` *(`INV-I14`)* | giết |
| lõi MM / nhóm | R3-M7 `_ma_mm` bỏ `strip` · M8 `nhom` sắp xếp | cả hai **giết** |
| trường nút | M5 `la` · M11 `con_cua` đảo · M13 `nguon_mm` · M16 `cap+1` | **giết** cả bốn |
| trường nút *(giá trị)* | **M12 `dong_sheet=ten` · M14 `ten=ma` · M15 `nhom=ten`** | **3 SỐNG** → `C4-R3-01` |

**16 đột biến: 12 giết · 4 sống** — cả 4 sống đều GHI NHẬN, ⛔ chặn gộp.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | **ĐẠT** | 12/16 đột biến giết; 4 sống ở lớp tuyến *(giá trị 3 trường nút + `sorted` tương đương)* — nhẹ; `INV-I14` giữ *(M6 đỏ)* |
| **Dữ liệu** *(kho thật, chỉ đọc)* | **ĐẠT** | tuyến SQL **0** bảng; kho `fls_itl = 0 dòng`; ảnh gói đo lại 74/73/`{NCF}`; email `@` ⛔ có mặt trong trả lời *(R2: 0)* |
| **Màn hình** | **N/A** | C4 ⛔ có màn |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `C4-R3-01` | GHI NHẬN | `xu_ly.py:1083-1085` · `test_isp_config_hd.py:107-138` | R3-M12/M14/M15 ⇒ `41 passed` *(`dong_sheet` · `ten` · `nhom` của nút ⛔ ghim giá trị ở tuyến)* | DEV *(tuỳ, gom `C5`)* |
| `C4-R3-02` | GHI NHẬN | `xu_ly.py:1081` | R3-M3 *(bỏ `sorted`)* ⇒ `41 passed`; ảnh thật chênh 1 mã ⇒ tương đương | DEV *(tuỳ, khi `C5` đổi nguồn)* |
| `C4-R3-03` | GHI NHẬN *(B2)* | `WO-142` *(nhánh làm việc)* | `AC-8` = 0 lần; nợ `C4-R2-01…03` ⛔ có AC mang mã | **ORCHESTRATOR** *(thêm `AC-8` trước giao `C5`)* |

## Câu hỏi *(kèm khuyến nghị)*
- **Q-C4-R3-1** — `C4-R3-03`: thêm `AC-8` vào `WO-142` *(mang `C4-R2-01/02/03`)* **trước khi giao `C5`**, hay chỉ ghi trong `TIEN_DO`? **Khuyến nghị: A — thêm `AC-8` vào `WO-142`** *(`AC-6b` gỡ ảnh nhưng lõi `hd.py` còn; nợ ⛔ AC thì `C5` đọc từ kho sẽ mở lại lối `ValueError`/`RecursionError` mà ⛔ ai đòi vá)*. B: chỉ ghi `TIEN_DO` *(rủi ro rơi nợ)*.
- **Q-C4-R3-2** — `C4-R3-01/02` *(nhẹ)*: gộp cùng `C5` hay bỏ? **Khuyến nghị: A — gộp vào `C5`** *(một nút thật `OPC` ghim `ten`/`nhom`/`dong_sheet`; bài hai mã chênh)*, ⛔ chặn gộp `C4`.

## Bài thử mới `tests/nghiem_thu/`
*(không)* — bản thử R3 ở `/tmp/r3_c4/` *(⛔ commit)*; 41 bài của Dev phủ 12/16 đột biến.

## Môi trường R3
`tools/dung_moi_truong_isp.sh --cong 5446` ⇒ `KẾT: ĐẠT`; worktree `…/.claude/worktrees/isp-c4`; sha `isp/C4` trước phiếu = `5837455` *(khớp brief)*. Nhánh đẩy: `claude/bold-galileo-zukpaf-isp/C4` *(fast-forward)*.
