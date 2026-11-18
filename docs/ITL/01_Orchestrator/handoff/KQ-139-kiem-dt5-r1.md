# KQ-139 — biên bản kiểm `BG-138` *(R1 · ISP 3.1.2 · Step 15 · DT5)*

| | |
|---|---|
| **Thuộc** | `BG-138` · `WO-137` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-18 |
| **Phán quyết** | **`TRƯỢT`** *(nhẹ)* — **0 CHẶN · 1 NÊN SỬA** `F-1` · 5 GHI NHẬN. Lý do duy nhất: `F-1` *(cổng "mã HD ∈ cây ATL" **mù trên 164/370 hàng HD** — mã lạ/vắng/trùng ở hàng toàn-0 đi qua ĐẠT)*. **Dữ liệu khớp nguồn: 0 lệch / 281.200 + 21.090 ô lưới** *(mọi khối LE · cột đầu/cuối trục)* |
| **Cổng vào** | `git rev-parse isp/DT5` = `d0e0559` ✅ *(mã+bài+ảnh `dc6b16f` + `BG-138`; nền `a8367ed`)* · `dung_moi_truong_isp.sh --cong 5445` `KẾT: ĐẠT` |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT5.md` *(v0.1 · `DT5-R1-01…06`)* |

## Đối chiếu ĐỘC LẬP với nguồn *(lưới SA tự đọc — mã của R1, ⛔ dùng khuôn tác giả)*
Bản sao `[COPY] Report I General Ledger | CF report` *(id `12S0…iU`)* · sheet `Report I CFA1 Daily` + `Report I CFA1 Y H Q M` · Sheets API v4 `values.get` · `UNFORMATTED_VALUE` · `SERIAL_NUMBER` · khoá SA chỉ-đọc *(⛔ in khoá)*. Hai lưới đọc về: **458 × 818** *(409)* · **458 × 502** *(410)* — **đúng** kích thước `BG-138`. Bản thô ở `/tmp/r1_dt5/` ⛔ commit.

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| **409** — mỗi ô lưới `(LE, mã HD, ngày)` của **370 hàng × 760 cột** so ảnh *(toàn bộ, ⛔ mẫu; R1 tự dò hàng HD theo nhãn, khối LE theo hàng `HDO`)* | **281.200** ô lưới = 254.625 ô có giá trị *(254.600 số + 25 `-`)* + 26.575 ô rỗng | **0 lệch**: 33.355 ô ≠ 0 khớp `Decimal` từng chữ số · 0 ô ảnh thừa · 0 ô 0 lọt · 25/25 `o_loi` khớp |
| **410** — `(LE, mã HD, kỳ)` của **370 × 57** | **21.090** ô = 19.120 có giá trị *(19.095 số + 25 `-`)* + 1.970 rỗng | **0 lệch**: 5.655 ô ≠ 0 · 0 thừa · 25/25 `o_loi` |
| Cột tương lai *(52 cột Daily · 133 cột Y/H/Q/M)* | mọi hàng HD × cột tương lai | **0 ô ≠ 0** ⇒ cắt an toàn *(Đ3: mẫu số = 52 × 370 · 133 × 370)* |
| Đóng băng LẠI từ lưới của R1 qua `dong_bang_sheet cfa1_daily/cfa1_yhqm … --mong` | — | `[ĐẠT]` exit 0; `dong` · `phu` **đúng từng phần tử** ↔ ảnh commit; Daily `checksum_noi_dung` = `6e01ee2b0f2207a3` ✅ *(Y/H/Q/M khác chỉ vì chuỗi `nguon` R1 gõ — `dong`/`phu` bằng nhau)* |

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
Mọi lệnh với `PG_DSN=…:5445/fls` · `PG_DSN_TEST=…:5445/fls_test` · `PYTHONUTF8=1`.

| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_cfa1.py` | 21 passed | **21 passed** | ✅ |
| `pytest tests/du_lieu` | 358 passed | **358 passed** *(38,5 s)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5445` *(một mình)* | `KẾT: ĐẠT` · 12 failed · 3095 passed · 2 xfailed · 14 errors · tập đỏ 28 = 28 · web 3 = 3 · chạy 3123 | **`KẾT: ĐẠT`** · `12 failed, 3095 passed, 2 xfailed, 14 errors` · **28 = 28** *(thêm 0 · bớt 0)* · web **3 = 3** *(664 passed)* · chạy **3123** *(mong ≥ 3123)* · skipped 0 · deselected 0 | ✅ |
| `lint-imports` | 11 kept | **11 kept, 0 broken** | ✅ |
| `kiem_tai_lieu.py` *(trước khi thêm sổ + KQ này)* | K1–K6 OK *(248 file · 2309 bảng)* | **ĐẠT** *(249 file · 2.314 bảng · 104 mã QĐ)* — số lệch nhẹ vì `BG` đếm trước khi nó được đếm | ✅ |
| `git diff a8367ed isp/DT5 -- tools/dong_bang_sheet.py` | 0 dòng | **0 dòng** *(công cụ chung ⛔ đụng)* | ✅ |

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 *(DT5-B1 mã ∈ cây ATL)* | mọi mã HD ∈ cây ATL 74 | Ảnh thật: `phu.hd` = 370 = 5 × 74, tập mã == cây ATL ✅. **Cổng lúc đóng băng** chỉ đo trên ô ≠ 0 ⇒ **164/370 hàng ⛔ được canh** *(`F-1`)* | **ĐẠT** *(ảnh)* · cổng ⇒ `F-1` |
| AC-1 *(DT5-B1 số cột ngày)* | số cột ngày = số ngày mốc → ngày đọc | **760** cột ngày LIÊN TỤC 2024-10-20 … 2026-11-18 *(R1: 760 = 2026-11-18 − 2024-10-20 + 1)*; mốc sai/hụt lát ⇒ TỪ CHỐI ✅ | **ĐẠT** |
| AC-2 *(DT5-B2 phá mã lạ · trả nguyên)* | ĐỎ rồi đúng từng byte | `GI→ZZZ` ở hàng có số ⇒ exit 1 ✅ *(`D-M1`, R1 trên lưới THẬT)*; trả nguyên ⇒ byte baseline ✅. Mã lạ ở hàng toàn-0 ⇒ **exit 0** *(`D-M2`)* | **ĐẠT** *(đường tác giả)* · lỗ ⇒ `F-1` |
| AC-3 *(ô lỗi ⇒ chuỗi + đếm)* | giữ chuỗi, ⛔ hoá 0 | 25/25 `"-"` ở `phu.o_loi` cả hai ảnh; ⛔ vào dòng chính; `"-"`→số ⇒ ĐỎ ✅; đổi `"-"`→`#REF!` ⇒ vẫn ĐẠT *(`F-4`)* | **ĐẠT** |
| AC-4 *(lát hỏng ⇒ ĐỎ)* | trục ⛔ liên tục · mốc sai · tương lai ≠ 0 · thiếu LE · lưới rỗng | 7/7 TỪ CHỐI trên lưới thật *(`D-M6` `-M6b` `-M10` `-M7` `-M12` `-M13` + `-M15` hụt cột)* | **ĐẠT** |
| AC-4 *(PII)* | 0 cột Diễn giải/Số CT/Email; lời lỗi ⛔ in giá trị | Ảnh: 0 khớp *(mẫu số = tên khoá + chữ ≫ 3 × số dòng)* ✅; `Email Address` ở 4 vị trí xa ⇒ TỪ CHỐI, ⛔ in ✅ *(hoa/đệm khoảng trắng cũng cắn)*; **lời lỗi ở 2 nhánh khác in lại ô bản thô** *(`F-2`)* | **ĐẠT** *(đường Email)* · `F-2` |
| AC-5 *(Q8 sàn)* | 3100 → 3123 cùng commit | `MONG_PYTEST_TOAN_BO = 3123` *(`tools/dung_moi_truong_isp.sh:420`)* · chạy 3123 ✅ | **ĐẠT** |
| Giữ ảnh cũ | ix_fx · 3 ảnh DT3 · gl_406 đúng từng byte | `dong_bang_sheet.py` 0 dòng đổi; bài `…giu_anh_DT2_DT3_DT4…` xanh | **ĐẠT** |

## Sáu trọng tâm thử phá
| # | Trọng tâm | Lệnh / phép đo | Kết quả |
|---|---|---|---|
| 1 | **Đúng nguồn từng ô** | tự đọc lại 2 sheet bằng SA *(`/tmp/r1_dt5/`)*, so **toàn bộ** *(⛔ mẫu 20 %)*, 5/5 khối LE, cột đầu 2024-10-20 và cột cuối 2026-11-18 | **0 lệch / 281.200 + 21.090 ô** *(bảng trên)* |
| 2 | **Trục ngày** | 812 cột sheet; 760 ≤ ngày đọc; liên tục = True; 52 cột tương lai: 0 ô ≠ 0; **ngày có ≥ 1 ô ≠ 0 cuối = 2026-11-11** | liên tục ✅ · cột tương lai ≠ 0 ⇒ TỪ CHỐI ✅ *(`D-M7`)*. **760 đếm *cột ≤ ngày đọc***, ⛔ đếm ngày có số: 7 cột cuối toàn 0 *(753/760 có số)* ⇒ `F-5` |
| 3 | **Y/H/Q/M** | 190 cột sheet = 10 năm × 19; giữ 57 = 2024·2025·2026 × 19 *(Y·H1·H2·Q1…Q4·M1…M12)* | nhãn kỳ khớp từng cột *(0 lệch)*; mỗi năm ≠ 19 cột ⇒ TỪ CHỐI ✅ *(`Y-M5` `-M7`)*; **ảnh ⛔ tự tính lại** *(không có `sum(` ở khuôn; đổi giá trị 1 ô ⇒ ảnh đổi y vậy, ⛔ kiểm Σ — `Y-M13` exit 0; đúng thiết kế "chỉ đóng băng")*. Info: Y = ΣM = 59,62152845106544 cho một hàng mẫu |
| 4 | **Cổng Đ5 hai chiều + Đ3** | 39 đột biến *(mục dưới)* | mã lạ ở hàng có số ⇒ ĐỎ ✅; LE lạ/thiếu ⇒ TỪ CHỐI ✅; lưới rỗng ⇒ TỪ CHỐI ✅; `-` ≠ 25 ⇒ ĐỎ ✅; **mã lạ/vắng/trùng ở hàng toàn-0 ⇒ ĐẠT ⛔** `F-1` *(mẫu số hàng toàn-0 = 164)* |
| 5 | **PII** | quét ảnh + đột biến `Email Address` ×4 vị trí + giả-email ở ô cấu trúc | ảnh 0 cột Diễn giải/Số CT/Email ✅; `Email Address` ⇒ TỪ CHỐI, ⛔ in ✅; **lời lỗi in lại ô** ở `_cfa1.py:132` · `cfa1_yhqm.py:81` ⇒ `F-2` |
| 6 | **Kích thước 6,8 MB** | đo từng khoá trong `dong` | **⛔ dữ liệu thừa**: ảnh giữ 33.355/281.200 ô *(11,9 %)*; 147 B/dòng; `o_id` dẫn xuất 23 %; không thụt −34 % ⇒ `F-6` *(B2, chấp nhận)* |

## Đột biến tự dựng *(trên BẢN SAO `git archive isp/DT5`, lưới THẬT; chạy `dong_bang_sheet.py` của bản sao — ⛔ đụng worktree)*
**39** ca *(20 Daily + 14 Y/H/Q/M + 5 bổ sung)*. Bản sao baseline = ảnh commit ✅.

| Nhóm | Ca | Kết quả mong → đo |
|---|---|---|
| **Giết được** *(đúng mong)* | mã có số → `ZZZ` *(D · Y)*; xoá hàng *(73)*; nhân hàng *(75)*; `-`→số; serial lệch/trùng/hụt cột; cột tương lai ≠ 0 *(D · Y)*; cột đầu bị cắt *(mốc)*; `doc_luc` sớm/muộn *(D · Y)*; LE → `XXX`; `values=[]` *(D · Y)*; `Email Address` ×4 vị trí *(hoa · đệm)*; Period lạ `Q9`; hụt 1 cột kỳ; cột kỳ gắn sai năm; hai cột trùng nhãn kỳ *(ĐỎ `trùng 5`)*; năm tương lai ≠ 0 | ĐỎ / TỪ CHỐI ✅ |
| **Sống — ⛔ nên chặn** | mã hàng toàn-0 → `ZZZ` *(D `-M2` · Y `-M2`)*; ATL vắng + trùng *(D `-M3`)* | **exit 0 ⛔** ⇒ `F-1` |
| **Sống — ghi nhận** | `-`→`#REF!` *(`D-M5b`)* ⇒ `F-4`; `dow` sai *(`D-M16`)* · serial `+0.5` *(`D-F1`)* · hoán nhãn tháng *(`Y-M6`)* · `Period` năm = 2023 ⇒ khoá `2024M2023` *(`Y-M15`)* ⇒ `F-3`; lời lỗi in ô *(`D-P1` · `Y-P3`)* ⇒ `F-2` | exit 0 / lộ ô |
| **Sống — đúng thiết kế** | nhân đôi giá trị 1 ô *(`D-M8` · `Y-M13`)*; phá nhãn Y/H/Q/M ở 4 hàng đầu Daily *(`D-F3`)*; "Diễn giải" ở ô cấu trúc *(`D-M11b`, ⛔ thuộc `PM_COT_RIENG_TU`)* | exit 0 — ảnh là đáp án đóng băng, ⛔ kiểm giá trị; checksum + bài ghim canh sau khi đóng băng |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | ĐẠT trừ `F-1` | Trục/LE/lát hỏng/PII-Email/`o_loi` đều có cổng cắn; cổng mã HD mù hàng toàn-0 |
| **Dữ liệu** *(nguồn SA, chỉ đọc)* | **ĐẠT — 0 lệch** | 281.200 + 21.090 ô lưới, so toàn bộ, 5/5 LE |
| **Màn hình** | N/A | bước dữ liệu, ⛔ có màn |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** | **`NANG`** *(NÊN SỬA)* | `tools/khuon_dong_bang/_cfa1.py:214-240` *(`cong_hd` đo `dong` ≠ 0)* | đổi mã hàng toàn-0 `MC`→`ZZZ` ở lưới thật ⇒ `[ĐẠT]` exit 0; hàng CÓ số ⇒ ĐỎ. **164/370** hàng toàn-0 | `DEV` |
| F-2 | `NHE` | `_cfa1.py:132` · `cfa1_yhqm.py:81` | giả-email ở ô A của `HDO` / ô `Period` ⇒ lời lỗi chứa chuỗi | `DEV` |
| F-3 | `NHE` | `cfa1_daily.py:73,93` · `cfa1_yhqm.py:48-58` | `dow` sai · serial `.5` · `Period=2023` ⇒ `2024M2023` · hoán tháng ⇒ exit 0 | `DEV` |
| F-4 | `NHE` | `cfa1_daily.py:54` · `cfa1_yhqm.py:44` | `-`→`#REF!` ⇒ vẫn 25 ⇒ `[ĐẠT]` | `DEV` |
| F-5 | `NHE` | ISP Step 15 §6 · AP §3.5.1 · `BG-138` §2 | 760 = cột ≤ ngày đọc; số cuối 2026-11-11; 7 cột cuối toàn 0; mốc 20/10 *(quyết A)* | `BA` *(orchestrator)* |
| F-6 | `NHE` | `cfa1_daily.json` 6,83 MB | đo từng khoá; không thừa dữ liệu | `BA` *(chấp nhận)* |

## Bài thử mới *(`tests/nghiem_thu/`)*
⛔ Không thêm bài vào repo ở vòng R1 này: 39 đột biến chạy bằng script tạm trên bản sao `git archive` *(⛔ commit)*. Đề xuất cho vòng sửa `DEV` *(`F-1`)*: bài phá "mã hàng toàn-0 → lạ" và "hai hàng cùng mã" trên lưới tổng hợp của `test_dap_an_cfa1.py` *(chứng minh ĐỎ trước khi vá)*.

## Câu hỏi cho orchestrator
1. `F-1` *(NÊN SỬA)* — gửi `DEV` vá trước R2 *(khuyến nghị **A**)* hay chấp nhận ghi nhận và vá sau gộp *(**B**)*? Ảnh thật đúng nên chỉ ảnh hưởng lần đóng băng sau; nhưng ISP DT5-B2 viết "mã lạ ⇒ ĐỎ" không giới hạn hàng có số ⇒ **A**.
2. `F-5` — ghi errata ISP/AP: mốc 2024-10-20 *(đã chốt A)* + 760 = cột ≤ ngày đọc, ngày có số cuối 2026-11-11 *(khuyến nghị **A**, vì H5/H6 so cột "chưa có số" với số 0)*.
