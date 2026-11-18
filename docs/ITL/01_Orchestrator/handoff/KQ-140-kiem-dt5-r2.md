# KQ-140 — biên bản kiểm `BG-138` *(R2 · ISP 3.1.2 · Step 15 · DT5 — vòng sửa sau `KQ-139`)*

| | |
|---|---|
| **Thuộc** | `BG-138` §8 · `WO-137` · `KQ-139` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-18 |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới** *(`DT5-R2-01` A2 · `DT5-R2-02` A1)*. `DT5-R1-01/-03/-04` **đã sửa, R2 xác nhận**; `-02` sửa một phần *(phần dư = `R2-01`/`-02`)*; `-05` `-06` giữ *Mở* *(orchestrator: errata ISP · kích thước chấp nhận)* |
| **Cổng vào** | `git rev-parse isp/DT5` = `5b8f7b5` ✅ *(`91a7f1f` mã+bài · `5b8f7b5` BG; R1 = `38bbd8a`)* · `dung_moi_truong_isp.sh --cong 5445` `KẾT: ĐẠT` |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT5.md` *(v0.2)* |

## Cổng chạy lại *(Test tự chạy)*
`PG_DSN=…:5445/fls` · `PG_DSN_TEST=…:5445/fls_test` · `PYTHONUTF8=1`.

| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_cfa1.py` | 31 *(R1: 21 + 10 bài mới)* | **31 passed** | ✅ |
| `pytest tests/du_lieu` | 368 | **368 passed** *(46 s)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5445` *(một mình)* | `KẾT: ĐẠT` · sàn 3133 | toàn bộ: `12 failed, 3105 passed, 2 xfailed, 14 errors` · tập đỏ **28 = 28** *(thêm 0 · bớt 0)* · chạy **3133** *(mong ≥ 3133)* · web **3 = 3** *(667 bài)* · `KẾT: ĐẠT` | ✅ |
| `lint-imports` | 11 kept | **11 kept, 0 broken** | ✅ |
| `kiem_tai_lieu.py` *(trước khi thêm sổ + phiếu này)* | OK | **ĐẠT** *(251 file · 2.325 bảng · 783 ô ngày · 104 mã QĐ)* | ✅ |
| `git diff 38bbd8a isp/DT5 -- tools/dong_bang_sheet.py` · `-- tests/fixture` | 0 dòng · ảnh ⛔ đổi byte | **0 dòng · 0 dòng** | ✅ |

## ĐỎ giả trên lưới THẬT *(trọng tâm 1)*
Đọc lại 2 sheet bằng SA chỉ-đọc *(bản sao CF report `12S0…iU`; `values.get` · `UNFORMATTED_VALUE` · `SERIAL_NUMBER`; bản thô ở `/tmp/r2_dt5/`, ⛔ commit)*: **458 × 818** *(409)* · **458 × 502** *(410)*. Đóng băng bằng `dong_bang_sheet.py` của bản sao `git archive isp/DT5` với `--mong 33355` · `5655`:

| Ảnh | exit | `dong` · `phu` · `checksum_noi_dung` | Byte so với commit |
|---|:-:|---|---|
| Daily *(409)* | 0 `[ĐẠT]` | bằng · bằng · `6e01ee2b0f2207a3` | **giống từng byte** *(`cmp`)* |
| Y/H/Q/M *(410)* | 0 `[ĐẠT]` | bằng · bằng · `ff9e76976cda1401` | **giống từng byte** *(`cmp`)* |

⇒ cổng mới **⛔ ĐỎ giả** trên dữ liệu thật; ảnh ⛔ đổi byte *(mẫu số: 2/2 ảnh · 33.355 + 5.655 dòng)*.

## Đột biến *(BẢN SAO `git archive`, lưới THẬT; ⛔ đụng worktree)* — 43 ca đột biến + 2 baseline
Mỗi dòng `ca → exit`. **Mong** ở cột đầu *(Đ5)*.

| Ca R1 tái đột biến | Mong | Đo |
|---|---|---|
| `D-M2` · `Y-M2` mã hàng toàn-0 → `ZZZ` *(R1: ĐẠT ⛔)* | ĐỎ | **exit 1** · `thiếu 2` ✅ ✅ |
| `D-M1` · `Y-M1` mã hàng CÓ số → `ZZZ` | ĐỎ | exit 1 · `thiếu 3` ✅ ✅ |
| `D-M3` · `Y-M3` vắng + trùng ở hàng toàn-0 *(R1: ĐẠT ⛔)* | ĐỎ | **exit 1** · `thiếu 2` ✅ ✅ *(`D-M3b` xoá nhãn ⇒ exit 2: `73 ≠ 74`)* |
| `D-M5b` · `Y-M5b` `-`→`#REF!` *(R1: ĐẠT ⛔)* | ĐỎ | **exit 1** ✅ ✅ |
| `D-M5c` · `Y-M5c` thêm `#REF!` mới *(26 ô)* · `D-allNA` · `Y-allNA` *(25 `-`→`#N/A`, tổng vẫn 25)* · `D-m24` *(bớt 1)* | ĐỎ | exit 1 *(`26≠25` · `24≠25`)* ✅ ✅ ✅ ✅ ✅ |
| `D-F1` serial `+0.5` *(R1: ĐẠT ⛔)* | TỪ CHỐI | **exit 2** *"serial ngày cột 8 ⛔ nguyên"* ✅ |
| `D-F1b` serial `45586.0` *(float nguyên)* | ĐẠT | exit 0, `cs` y baseline ✅ *(không chặn nhầm)* |
| `D-M16` · `D-M16b` · `D-dowcase` dow sai · `None` · `sun` | TỪ CHỐI | **exit 2** ×3 ✅ |
| `Y-M6` hoán 2 Period tháng · `Y-M6b` hoán `Q1↔Q2` | TỪ CHỐI | **exit 2** *"thứ tự kỳ … vị trí 7 (mong M01)"* · *"vị trí 3 (mong Q1)"* ✅ ✅ |
| `Y-M15` Period 2023 · `-M15b` 13 · `-M15c` `2.5` · `Y-bool` `True` | TỪ CHỐI | **exit 2** ×4 ✅ |
| `Y-yearswap` đổi Year một cột *(2024 giữ 18 cột)* | TỪ CHỐI | exit 2 `18 ≠ 19` ✅ |
| `D-Inf` · `D-NaN` · `D-P7` · `D-P9` trục lẻ · `D-P4` hụt khối LE | TỪ CHỐI | exit 2 ×5 ✅ |
| **Phân luồng quyết A**: lệch phân bố `o_loi` ⇒ ĐỎ exit 1 *(có ghi ảnh cờ)*; lỗi nhãn trục ⇒ TỪ CHỐI exit 2 *(⛔ ghi)* | đúng | **đúng 100 %** *(mẫu số 43)*: 16/16 ca mã HD · `o_loi` · email-làm-mã = exit 1 + CÓ ảnh cờ · 24/24 ca nhãn trục/Period/serial/LE/hằng JSON = exit 2 + ⛔ ảnh · 3/3 ca sống đúng mong *(`D-F1b` · `D-P1` · `Y-P1`: email ở ô số không cấu trúc, exit 0)* |

## `_an_toan` có lộ ô ở nhánh nào khác? *(trọng tâm 2)*
Grep `{…!r}` ở `tools/khuon_dong_bang/_cfa1.py` · `cfa1_*.py`: **4 chỗ** còn `!r`, mọi chỗ là **hằng của mã** *(`LE[bi]`, `list(LE)`)* — ⛔ ô bản thô *(mẫu số: 4/4 đã đọc)*. Ba nhánh R1 *(LE cột A · nhóm · Period)* nay qua `_an_toan`:

| Ca | Ô | Lời lỗi |
|---|---|---|
| `D-P1b` · `Y-P1b` | email giả ở ô A hàng `HDO` | `⟨str·20 ký tự ⛔ hiện⟩` ✅ ✅ |
| `Y-P3` | email giả ở ô Period | `⟨str·20 ký tự ⛔ hiện⟩` ✅ |
| `D-P2` · `D-P7` · `D-P8` | email ở nhóm · Day · dow | không in ô *(chỉ vị trí + serial số)* ✅ ✅ ✅ |
| `D-P10` | một-từ-tên ở ô A hàng `HDO` | **in nguyên** ⛔ ⇒ `DT5-R2-01` |
| `D-P11` | `INV2024-0099` | **in nguyên** ⛔ ⇒ `DT5-R2-01` |
| `D-P5` · `D-P6` | email làm mã HD hàng có số · email ở ô `-` | ĐỎ exit 1, stdout chỉ `thiếu N`; **ảnh cờ** mang chuỗi *(515 · 1 lần)* ⇒ `DT5-R2-02` |

## Bảng AC *(chỉ phần đổi từ R1)*
| AC | Mong | Đo được | Phán quyết |
|---|---|---|---|
| AC-1/2 *(DT5-B1/B2 mã ∈ cây ATL)* | lạ · vắng · trùng ĐỎ kể cả hàng toàn-0 | `D-M2/-M3` · `Y-M2/-M3` ĐỎ; mẫu số hàng toàn-0 = **164** in ở `dai` | **ĐẠT** *(đóng `DT5-R1-01`)* |
| AC-3 *(ô lỗi ⇒ chuỗi + đếm)* | tập giá trị ghim | `#REF!` thêm/đổi/bớt ⇒ ĐỎ 5/5 | **ĐẠT** *(đóng `DT5-R1-04`)* |
| AC-4 *(trục + PII)* | nhãn trục đối chiếu chéo; lời lỗi ⛔ in ô | 24/24 TỪ CHỐI; 3/3 nhánh R1 che; dư `R2-01`/`-02` | **ĐẠT** · ghi nhận |
| AC-5 *(Q8 sàn)* | 3123 → 3133 | chạy 3133 · 28 = 28 · web 3 = 3 | **ĐẠT** |
| Giữ ảnh | ảnh ⛔ đổi byte | `cmp` 2/2 giống · `dong_bang_sheet.py` 0 dòng | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT | 4 lỗi R1 tái đột biến đều cắn; phân luồng A đúng; ⛔ ĐỎ giả |
| **Dữ liệu** *(SA chỉ-đọc)* | ĐẠT | ảnh tái sinh từ lưới thật = ảnh commit *từng byte* *(409 + 410)* |
| **Màn hình** | N/A | bước dữ liệu |

## Phát hiện
| F | Mức | Lớp | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|---|
| `DT5-R2-01` | `NHE` *(GHI NHẬN)* | A2 | `_cfa1.py:80-102` `_O_AN_TOAN` | `D-P10` · `D-P11` ⇒ chuỗi một-từ ≤ 16 ký tự in nguyên trong lời lỗi | `DEV` *(đề xuất tập đóng)* |
| `DT5-R2-02` | `NHE` *(GHI NHẬN)* | A1 | đường ghi ảnh ĐỎ *(quyết A)* | `D-P5` · `D-P6` ⇒ ảnh cờ mang ô thô; mặc định `.DO.json` gitignored, `--ra` tuỳ ý ⛔ chặn | `BA` *(orchestrator quyết chấp nhận / che)* |

**Trạng thái R1:** `-01` đã sửa ✅ · `-02` sửa một phần · `-03` đã sửa ✅ · `-04` đã sửa ✅ · `-05` Mở *(orchestrator ghi errata: mốc 2024-10-20 · 760 = cột ≤ ngày đọc · ngày có số cuối 2026-11-11)* · `-06` Mở *(chấp nhận)*.

## Bài thử mới
Không thêm bài vào `tests/nghiem_thu/` *(đột biến chạy trên bản sao, ⛔ commit — vai KIỂM ⛔ sửa mã/bài của Dev; `10` bài mới của Dev ở `test_dap_an_cfa1.py` đã xanh)*.

## Câu hỏi kèm khuyến nghị *(cho orchestrator)*
- **Q1** `DT5-R2-02`: ảnh ĐỎ ghi giá trị ô thô — chấp nhận *(A)* hay che `o_loi.gia` ngoài tập đóng *(B)*? **Khuyến nghị A** — mặc định ghi `.DO.json` đã `gitignore` *(`.gitignore:21`)*, ảnh XANH sạch.
- **Q2** `DT5-R2-01`: để Dev siết `_an_toan` thành tập đóng ở vòng sau *(B)* hay chấp nhận *(A)*? **Khuyến nghị A** — ô lộ chỉ là ô cấu trúc; siết khi đụng khuôn lần sau.
