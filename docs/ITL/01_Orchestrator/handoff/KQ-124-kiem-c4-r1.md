# KQ-124 — biên bản kiểm `BG-123` *(ISP 3.1.2 · Step 11 · C4 · R1)*

| | |
|---|---|
| **Thuộc** | `BG-123` · `WO-122` *(dải: WO-122 · BG-123 · KQ-124 R1 · KQ-125 R2 · KQ-126 R3)* |
| **Kiểm bởi** | `fls-test` — **R1** *(phiên cloud CON độc lập)* · 2026-11-18 |
| **Đối tượng** | nhánh `isp/C4` @ `5212f25` *(mã `7478e64` + `BG-123`)* · nền `f1dbd00` · cụm PG riêng **5444** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN** *(2 NÊN SỬA → Dev · 3 GHI NHẬN; chi tiết + luật phòng: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C4.md`)* |

> **Điều kiện PUSH** *(ISP mục 8)*: đủ R1 · R2 · R3, chặn = 0. R1 `ĐẠT · 0 chặn`; còn R2 *(KQ-125)* · R3 *(KQ-126)* ⇒ **chưa đủ PUSH**.
> Mọi số R1 tự chạy lại, `PG_DSN=…:5444/fls PG_DSN_TEST=…:5444/fls_test PYTHONUTF8=1`. Đột biến trên **bản sao** `git archive isp/C4` ở `/tmp/r1_c4/mut/` *(⛔ chạm worktree; ⛔ sửa mã hệ thống)*. Câu hỏi "gốc sai cấp" đã chốt **A** *(gộp `HD_CAP_NHAY`)* — R1 ⛔ tính là phát hiện, chỉ xác nhận nó chạy đúng.

## Cổng chạy lại
| Lệnh | `BG-123` nói | R1 đo | Khớp |
|---|---|---|:-:|
| Dựng môi trường *(script S0)* | `KẾT: ĐẠT` | `KẾT: ĐẠT` · 26/26 di trú · pg_verify 25 bảng 0 lệch · `lint-imports 11 kept` · HD1 `9845/9967` · kho `fls_itl = 0` | ✅ |
| `pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py` | `26 passed` | `26 passed in 0.94s` | ✅ |
| `pytest tests/api tests/cau_hinh` | *(BG ⛔ ghi)* | `3 failed, 530 passed, 11 errors` — 14 nút đỏ, **14/14 có trong `duong_nen_bai_do.txt`** *(11 `test_mui_thu_luoi` + 3 `…_pg`)*, ⛔ nút nào của C4 | ✅ |
| `--duong-nen --cong 5444` *(GOC = `…/isp-c4`, chạy MỘT MÌNH)* | `KẾT: ĐẠT` · `28 = 28` · 3093 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `12 failed, 3065 passed, 2 xfailed, 14 errors in 382s` ⇒ `28 = 28 (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 3093 (mong ≥ 3093) · skipped 0 · deselected 0`; web `3 failed, 664 passed` ⇒ `3 = 3 · chạy 667 (mong ≥ 667) · skipped 0` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` | ĐẠT · 42 tuyến | `✅ ban khai KHOP SQL that o ca 42 tuyen` · tuyến mới `TINH […ix_hd_cay.json, …ix_mapping_master.json] · vet 11 ham` | ✅ |
| `kiem_tai_lieu.py` | ĐẠT · 240 file · 2270 bảng | ĐẠT · 241 file · 2273 bảng · 776 ô ngày · 104 mã QĐ *(+1/+3 = chính `BG-123`)* | ✅ |
| `pytest --collect-only` *(Q8)* | 3093 · web 667 | **3093** *(227 tệp)* · web **667** ⇒ hằng `MONG_PYTEST_TOAN_BO`/`MONG_PYTEST_WEB` = thu thập | ✅ |
| `kiem_so_song.py` | ⛔ CHƯA CHẠY *(đường Windows)* | ⛔ chạy được — `tools/kiem_so_song.py:406` gõ `.venv/Scripts/lint-imports.exe` *(1 chỗ, grep `tools/ docs/ITL/_tools/ fls/`)* | — *(→ `C4-R1-05`)* |

## Bảng AC *(mỗi dòng mục 8 + test ID mục 6)*
| AC *(test)* | Mong | R1 đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** `C4-B1` | 74 nút · 6 nhóm · gốc đúng · ⛔ chu trình · cấp = `MONG_CAP` | **Mã R1** *(⛔ gọi lại `hd.py`)* đọc `atl_cay.json`: **74** mã *(74 duy nhất)* · **6** nhóm `HDO·HDH·HDAP·HDT·HDC·HDCI` · cấp `37·23·11·3` *(Σ 74)* · tính lại `cha` *(gần nhất phía trên cấp nhỏ hơn, trong nhóm)* ⇒ lệch **0/74**. Bài Dev + `hd.doc_tep` ⇒ cùng số; ⛔ chu trình. *(Ghi: ảnh để `cap` là CHUỖI `'1'…'4'`; `_cap` nhận — OK. Ảnh là **rừng 37 gốc**, ⛔ một gốc: đúng WO "gốc đúng" theo ảnh)* | **ĐẠT** |
| **AC-2** `C4-B2` | `A→B→A` ⇒ `HD_CHU_TRINH` | Cây tổng hợp của R1: `A→B→A` ⇒ `{HD_CAP_NHAY, HD_CHU_TRINH}` *(3 lỗi, vòng báo **1 lần**)*; vòng 3 nút ⇒ cùng hai tên; cây hợp lệ ⇒ **sạch**. Đột biến **M20/M21** giết; **M1** *(⛔ dừng vòng)* ⇒ `-9` OOM *(giết bằng sập, ⛔ khẳng định)* ⇒ `C4-R1-04` | **ĐẠT** |
| **AC-3** `C4-B3` | cha vắng ⇒ `HD_CHA_VANG`; cấp nhảy ⇒ lỗi có tên | cha trỏ `ZZ` ⇒ `{HD_CHA_VANG}`; con cấp 3 dưới cấp 1 ⇒ `{HD_CAP_NHAY}`; gốc cấp 2 ⇒ `{HD_CAP_NHAY}` *(đúng quyết "A": gộp)*. **M2 · M3 · M4 · M24** giết. Tên lỗi là **hằng chuỗi**; ⛔ `ValueError` trơn **còn ở 3 đường** *(`cap='²'`, `thu_tu` hỏng, JSON hỏng)* ⇒ `C4-R1-01` | **ĐẠT** *(kèm `C4-R1-01`)* |
| **AC-4** `C4-B4` | `200` · 74 · `con_cua`/`la` đúng · 74 **và** 73 · `chenh_mapping_master` · ảnh qua đường truyền vào | **Tuyến THẬT** *(máy HTTP, thẻ HS256, PG 5444)*: `200` · `so_atl=74` · `so_mapping_master=73` · `chenh_mapping_master=['NCF']` · `len(nut)=74` · `len(goc)=37`; `con_cua`/`la` của **74/74 nút** = tính lại của R1 *(lệch 0)*, `la=True` ở **64** nút *(⛔ nhầm nhãn với "64 cột có tên `ITL Ledge`" — Đ4)*. MM đo bằng mã R1: **73** mã *(73 duy nhất, 73/73 có dạng `MÃ ⛔ Tên`)*; `ATL − MM = {NCF}` · `MM − ATL = ∅` *(Đ3, hai chiều)* — khớp `BG-107`. `meta.data_status='flash'`. Đường ảnh: hằng ở `hd.NGUON_*` *(tầng 7 ⛔ gõ lại)*, bài `doc_tep(tmp_path)` đổi đường được | **ĐẠT** |
| **AC-5** *(khuôn C1)* | `?run_id=` ⇒ `400` · `nguon_tinh` · `soi` ĐẠT · BA-07 phủ tuyến | `?run_id=NAP-2026-01-01-X` ⇒ **400** `FLS-BAD-REQUEST` `data=None`; không thẻ ⇒ **401**; `POST` ⇒ **405**; `soi_bang_tuyen` ĐẠT *(42 tuyến, SQL **0 bảng**)*; `test_ba07_phu_het_tuyen` xanh *(trong `tests/api`)*; dòng §4i `/config/hd` hiện còn `⬜ chưa xây` *(orchestrator đổi ✅ lúc gộp — đúng WO)* | **ĐẠT** |
| **AC-6** *(Q8)* | nâng sàn cùng commit theo `--collect-only` | `MONG_PYTEST_TOAN_BO` `3067 → 3093` *(+26 = 16 + 10)* + bài ghim `test_S0_R2_03` **cùng commit `7478e64`**; thu thập thật **3093** · web **667**; `--duong-nen` chạy 3093 ≥ 3093 | **ĐẠT** |
| mục 8 · *"3 vòng review · PUSH"* | — | **chưa** — chờ R2 · R3 | *(ngoài R1)* |
| Ràng buộc WO | ⛔ `cha = Σ con` · ⛔ kho · ⛔ hoà giải · ⛔ sửa ảnh DT3 | `hd.py` ⛔ `psycopg`/`fls.db`; `lint-imports` 11 kept; `cay_hd` ⛔ `sum(` *(0)*; `chenh` chỉ liệt kê *(M29 đổi chiều ⇒ đỏ)*; ảnh gói = ảnh DT3 **từng byte** *(sha256 `504fa53d…` · `3c1f61a2…`)*, `git diff f1dbd00 isp/C4 -- tests/fixture` = **0 dòng** | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | **ĐẠT** | Ba tên lỗi bắt buộc đỏ **riêng** trên cây tổng hợp, cây đúng ⇒ sạch *(Đ5 hai chiều)*; `HD_CHU_TRINH` luôn kéo theo `HD_CAP_NHAY` *(Dev đã khai + ghim `∈`)*. 24/29 đột biến giết; 5 sống đều ở nhánh **lỗi phụ** *(`HD_HONG`, `doc_mm`)* ⇒ `C4-R1-02/03` |
| **Dữ liệu** *(kho thật, chỉ đọc)* | **ĐẠT** | Tuyến TĨNH đọc hai ảnh gói, SQL **0 bảng**; kho `fls_itl = 0`; `FLS_CHO_GHI_THAT` ⛔ đặt. PII: `@` = **0** ở hai ảnh gói và ở trả lời tuyến. Ghi nhận: ảnh MM gói mang bảng phụ `tho` *(84 hàng, 51 hàng có chuỗi ≥ 6 chữ số)* mà C4 ⛔ đọc ⇒ `C4-R1-05` |
| **Màn hình** | **N/A** | WO/ISP: ⛔ có màn cây ở AP v3.1.2 *(cây dùng bởi engine H5)* |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `C4-R1-01` | **NÊN SỬA** | `fls/cau_hinh/hd.py:168-170` · `:220` · `:281`/`:321` | `kiem` với `cap='²'` ⇒ `ValueError`; `thu_tu='abc'` ⇒ `ValueError`, `thu_tu=None` ⇒ `TypeError`; `doc_van_ban('{')` ⇒ `JSONDecodeError`; `cap='١'` được nhận. Vi phạm *"⛔ `ValueError` trơn"* của WO. Hôm nay ⛔ chạm được *(ảnh gói đóng băng)*; hết đóng băng ở C5 | **DEV** |
| `C4-R1-02` | **NÊN SỬA** | `hd.py:310-344` · `tests/cau_hinh/test_hd.py:196` | M27 *(⛔ bắt mã MM trùng)* · M28 *(⛔ bắt MM 0 mã)* ⇒ `26 passed`. Đ5: cổng mới phải chứng minh ĐỎ — `doc_mm` chỉ có bài đường xanh | **DEV** |
| `C4-R1-03` | GHI NHẬN | `hd.py:164,172,195` | M22 *(`cap=0`)* · M23 *(`cap=True`)* · M26 *(cột lạ)* ⇒ `26 passed`; gốc ⇒ `{HD_HONG}`. M22: vẫn bị `HD_CAP_NHAY` chặn *(chỉ đổi tên)* | DEV *(tuỳ)* |
| `C4-R1-04` | GHI NHẬN | `hd.py:245-257` | M1 *(⛔ dừng vòng chu trình)* ⇒ `kill -9` OOM thay vì đỏ khẳng định | DEV *(tuỳ)* |
| `C4-R1-05` | GHI NHẬN | `ix_mapping_master.json` `phu.tho` · `tools/kiem_so_song.py:406` | (a) ảnh MM gói mang cả `tho` *(84 hàng)* trong khi chỉ đọc `hd_code`; (b) `kiem_so_song` gõ đường Windows ⇒ ⛔ chạy ở Linux ⇒ R1 ⛔ có bằng chứng xanh | **orchestrator** |

## Câu hỏi *(kèm khuyến nghị)*
- **Q-C4-1** — `C4-R1-01`/`02` *(2 NÊN SỬA)*: Dev vá ngay trong vòng sửa R1→R2 hay gộp vào `C5` *(kho config chỉ-thêm, lúc đó ảnh hết đóng băng)*? **Khuyến nghị A: vá trong vòng R1→R2** *(5 bài nhỏ, chạm đúng một tệp mã + một tệp bài; ⛔ làm lệch sàn Q8 — nâng `MONG_PYTEST_TOAN_BO` cùng commit)*. B: để `C5` — chỉ khi chấp nhận hai đường lỗi ⛔ có tên tới lúc đó.
- **Q-C4-2** — `C4-R1-05(b)`: sửa đường `lint-imports` của `kiem_so_song.py` theo nền tảng **ngoài** C4 *(phiếu riêng)*? **Khuyến nghị A: phiếu riêng**; ⛔ gộp vào C4 *(ngoài phạm vi WO-122)*.

## Bài thử mới `tests/nghiem_thu/`
*(không)* — 26 bài của Dev phủ 24/29 đột biến; 5 lỗ giao Dev vá ở chính bài `test_hd.py` *(R1 ⛔ sửa bài của Dev, ⛔ sửa mã)*. Bản thử R1 nằm ở `/tmp/r1_c4/` *(`do.py` · `http_probe.py` · `syn.py` · `probe.py` · `mut.py`)* — ⛔ commit.

## Môi trường R1
`tools/dung_moi_truong_isp.sh --cong 5444` *(script S0 bản nhánh)* ⇒ `KẾT: ĐẠT`. Sha: `isp/C4` = `5212f25` *(khớp brief)*. Nhánh đẩy: `claude/bold-galileo-zukpaf-isp/C4`. Lượt đột biến ⛔ chồng lượt `--duong-nen` *(chạy tuần tự: đột biến trước, nền sau, một mình)*.
