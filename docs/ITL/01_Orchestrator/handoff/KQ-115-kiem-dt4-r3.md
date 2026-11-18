# KQ-115 — biên bản kiểm `BG-112` *(R3 · ISP 3.1.2 · Step 12 · DT4 · xác nhận cuối trước gộp)*

| | |
|---|---|
| **Thuộc** | `BG-112` *(mục "Vòng sửa sau R1")* · `WO-111` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R3)* · 2026-11-18 |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới** *(`DT4-R3-01` · `-02`)*; `DT4-R2-01` · `-02` **giữ GHI NHẬN** *(lý do dưới)*. **Cây gộp thử sạch: 0 xung đột · `KẾT: ĐẠT`** |
| **Cổng vào** | `git rev-parse isp/DT4` = `78470ab` ✅ · `git diff 6516dcb isp/DT4 --stat` = chỉ `KQ-114` + sổ *(⛔ mã đổi sau R2)* ✅ |
| **Sổ phát hiện** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT4.md` *(v0.3)* |

## Cổng chạy lại trên ngọn *(⛔ tin số R2 — tự chạy; `PG_DSN` cổng 5437)*
| Lệnh | R2 nói | Test đo (R3) | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu` | `195 passed` | **`195 passed in 13.31s`** | ✅ |
| `pytest --collect-only` *(toàn bộ · riêng `test_dap_an_406`)* | 2.685 · 32 | **2.685 · 32** *(mẫu số > 0 — Đ3)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(script NHÁNH, log `GOC = …/isp-dt4`, chạy MỘT MÌNH — ⛔ chồng đột biến)* | `KẾT: ĐẠT` · `12 failed, 2657 passed, 2 xfailed, 14 errors` | **`KẾT: ĐẠT`** · **`12 failed, 2657 passed, 2 xfailed, 14 errors in 315.09s`** · **`26 = 26 node id (thêm 0 · bớt 0)`** · `tests/web 3 failed, 661 passed` = **`3 = 3`** | ✅ |
| `lint-imports` | `11 kept, 0 broken` | **`Contracts: 11 kept, 0 broken.`** | ✅ |
| `docs/ITL/_tools/kiem_tai_lieu.py` | ĐẠT *(185 file)* | **`✅ cổng tài liệu ĐẠT`** *(186 file · 1.926 bảng · 732 ô ngày · 104 mã QĐ — +1 file là `KQ-114`)* | ✅ |
| `git diff 6516dcb isp/DT4 --stat` | chỉ phiếu + sổ | **2 tệp** *(`KQ-114` +99 · sổ)* — ⛔ mã, ⛔ ảnh | ✅ |

## Cây gộp thử *(`/tmp/gop_thu` = `origin/lam_viec` @ `571416a` + `merge --no-ff --no-commit isp/DT4`; ⛔ commit, ⛔ push)*
| Bước | Lệnh · kết quả |
|---|---|
| Dựng | `git -C $R worktree add /tmp/gop_thu origin/lam_viec` → `HEAD 571416a` *(nhánh làm việc đã có DT2 + DT3 + FG)* |
| Gộp | `git -C /tmp/gop_thu merge --no-ff --no-commit isp/DT4` ⇒ **`Automatic merge went well`** · **0 xung đột** · 8 tệp vào cây: `gl_406.json` · `gl_406.py` · `dong_bang_sheet.py` · `test_dap_an_406.py` · `BG-112` · `KQ-113` · `KQ-114` · sổ DT4 |
| Sàn *(Đ4 — mỗi số nói nó đếm gì)* | `pytest --collect-only` trên cây gộp = **3.100 bài** *(toàn bộ)* = 3.067 *(sàn hiện ở `lam_viec`)* **+ 33** *(2.652 → 2.685 của DT4)* ✅ khớp; riêng `test_dap_an_406` = **32**. `tests/web` = 667 *(⛔ DT4 thêm bài web)* |
| Ghim | Script `MONG_PYTEST_TOAN_BO=3067` + bài ghim `test_S0_R3_02_…` `== ["3067"]` **KHÔNG nâng** ⇒ bài ghim **ĐỎ** *(`1 failed`)* — đúng luật Q8 *(quên nâng = ĐỎ)* ⇒ trong cây thử nâng **cả hai** `3067 → 3100` *(sửa tay 2 dòng, ⛔ commit)* ⇒ bài ghim `1 passed` |
| `--duong-nen` cây gộp | `env -C /tmp/gop_thu bash /tmp/gop_thu/tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` *(log `GOC = /tmp/gop_thu`)* ⇒ **`12 failed, 3072 passed, 2 xfailed, 14 errors in 361.70s`** · **`28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0)`** · **`chạy 3100 bài (mong ≥ 3100) · skipped 0 · deselected 0`** · `tests/web 3 failed, 664 passed` = **`3 = 3`** · chạy 667 *(mong ≥ 667)* · **`KẾT: ĐẠT`** |

⚠ **Việc cho orchestrator lúc gộp thật:** nâng `MONG_PYTEST_TOAN_BO` **3067 → 3100** *(script)* + bài ghim `"3067" → "3100"` *(`tests/test_dung_moi_truong_isp.py:423`)* **trong cùng commit gộp**; `MONG_PYTEST_WEB=667` giữ.

## Đột biến *(R3 tự dựng — ⛔ trùng `N1…N12` của R2; bản sao `git archive isp/DT4` ở `/tmp/r3_dt4/mut`; chạy tuần tự, sau `--duong-nen`)*
Lệnh mỗi ca: `pytest tests/du_lieu/test_dap_an_406.py -x`. Mẫu số = **15 áp được, 0 vô hiệu**.

| # | Đột biến | Kết |
|---|---|---|
| M1 | `ITL_ID_RE.fullmatch` → `.match` *(ở `itl_lech`)* | **XANH 32/32 ⇒ `DT4-R3-01`** |
| M2 | `_khoa_hop_le` `int(v) >= 1` → `>= 0` | ĐỎ `…khoa_dong_sheet_hop_le` |
| M3 | `LECH_CO_TEN` `202605: 239 → 238` | ĐỎ `…TAI_TAO_dung_tung_byte…` |
| M4 | `so?` thôi đòi SỐ *(`cot_theo_kieu`)* | ĐỎ `…cot_so_opt_BO_RONG_cho_phep_nhung_LOI_thi_DO` |
| M5 | `thieu_lac` `!=` → `<` *(chỉ bắt thiếu, ⛔ thừa)* | ĐỎ `…cong_ky_DO_khi_lech_NGOAI_4_ky_co_ten[them_ky_vang]` |
| M6 | `cot_A_rong is not True` → `is False` | **XANH 32/32 ⇒ `DT4-R3-02`** |
| M7 | bỏ chặn `bool` ở cột `A` | XANH — **⛔ lỗ**: R3 chạy tay `chuan_bi` với `A = True` ⇒ `ky = 189912` ⇒ `thieu_lac` đưa `189912` vào `thieu` ⇒ cổng kỳ ĐỎ *(lớp phòng thủ thứ 2 bắt)* |
| M8 | nhận `values` ⛔ danh sách rỗng | XANH — **⛔ lỗ**: bài `…values_RONG_thi_TU_CHOI` *(exit 2)* vẫn xanh ⇒ lớp chung của công cụ từ chối ảnh rỗng *(kết quả hành vi giữ nguyên)* |
| M9 | `TIEN_TE` bỏ `HKD` | ĐỎ `…TAI_TAO…` |
| M10 | `ky` lệch +1 tháng | ĐỎ `…TAI_TAO…` |
| M11 | `PHU_MONG cong_thuc 1 → 2` | ĐỎ `…TAI_TAO…` |
| M12 | bỏ kiểm `dong_dau_sheet != 10` | XANH — **⛔ lỗ**: kiểm `ds != DONG_DAU_SHEET + i` ở hàng đầu bắt cùng điều kiện *(thừa)* |
| M13 | bỏ soát PII **lần 2** *(sau `chuan_bi`)* | XANH — **⛔ lỗ**: dư *(lần 1 trước khuôn còn)*; mục tiêu chọn kém, R3 ghi nhận trung thực |
| M13b | bỏ cả hai lần soát PII | ĐỎ `…B3_ban_tho_co_cot_Email_thi_TU_CHOI` |
| M14 | bỏ soát PII **lần 1** *(trước khuôn)* | ĐỎ `…B3_ban_tho_co_cot_Email_thi_TU_CHOI` |

**Đếm** *(15 dòng = M1…M14 + M13b)*: **9 ĐỎ** *(M2 · M3 · M4 · M5 · M9 · M10 · M11 · M13b · M14)* · **6 sống** *(M1 · M6 · M7 · M8 · M12 · M13)* = **2 lỗ thật** *(M1 · M6 ⇒ `DT4-R3-01` · `-02`)* + **4 dư/tương đương** *(M7 · M8 · M12 · M13 — mỗi ca có lớp thứ hai chứng minh bằng lệnh)*. 9 + 6 = 15 ✅. *(Đ2: "đột biến sống" ⛔ tự động là lỗ — mỗi ca sống phải hỏi "lớp nào còn canh".)*

## Bảng AC *(+ mục 8 ISP — đối chiếu từng dòng)*
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| mục 8 · `DT4-B1…B3` đúng | ba bài + cổng | B1 *(19 kỳ khớp + 4 lệch có tên; Σ **7.883** dòng; `--mong 7883`)* · B2 *(`…ky_RONG_thi_DO` · `…values_RONG_thi_TU_CHOI`)* · B3 *(0 khoá Diễn giải/Số CT/Email; quét tên + GIÁ TRỊ, mẫu số 2·7.883)* — đều xanh trong `195 passed` | **ĐẠT** |
| mục 8 · "3 vòng review xong" | R1 · R2 · R3 | `KQ-113` · `KQ-114` · **phiếu này** | **ĐẠT** |
| mục 8 · điều kiện PUSH | đủ R1·R2·R3, chặn = 0 | R1 0 · R2 0 · R3 **0** | **ĐẠT** |
| `DT4-B1` | Σ kỳ khớp `phan_bo_ky`, lệch có tên | 19 kỳ khớp + 4 lệch tên *(`202605…08`)*; M3/M5/M10 đột biến ⇒ ĐỎ | **ĐẠT** |
| `DT4-B2` | lát rỗng ⇒ ĐỎ *(Đ3)* | M8 chứng minh lớp chung cũng từ chối rỗng; bài ca phá xanh | **ĐẠT** |
| `DT4-B3` | 0 cột Diễn giải/Số CT | M13b · M14 ĐỎ *(bài PII cắn)*; vùng đọc ⛔ `B`/`C` *(R1·R2 đối chiếu nguồn 2 lần — ⛔ đọc Drive lần 3, đúng chỉ dẫn)* | **ĐẠT** |
| AC-1 | `gl_406.json` 7.883 dòng; 19 kỳ + 4 lệch tên *(WO đính chính "21 → 19")* | khớp *(ở trên)* | **ĐẠT** |
| AC-2 | lát rỗng ĐỎ | như `DT4-B2` | **ĐẠT** |
| AC-3 | 0 PII; máy quét có ca phá | `…may_quet_PII_CAN_ca_pha` + `…GIA_TRI_CAN_ca_pha` xanh; M13b/M14 ĐỎ | **ĐẠT** |
| AC-4 | khuôn riêng; công cụ chung chỉ khi bài đòi; ảnh DT2/DT3 từng byte | `git diff --stat cf5156e isp/DT4 -- tests/fixture/cau_hinh` = **0** dòng *(R3 đo lại)*; công cụ chung đổi `tools/dong_bang_sheet.py` **+31/−6** *(kiểu `dong_sheet` · `so?`, lý do ghi trong mã)*; mọi bài DT2/DT3 xanh *(trong 195)* | **ĐẠT** |
| AC-5 | 9.843 hàng công thức ĐẾM, ⛔ vào bảng; hàng có ngày mà BM…BT lỗi ⇒ ĐỎ | `…khai_9843_hang_cong_thuc` · `…hang_du_lieu_co_loi_BM_thi_DO` xanh; M6 ⇒ `DT4-R3-02` *(chỉ ca `cot_A_rong` thiếu khoá)* | **ĐẠT** |
| AC-6 (Q8) | ghi số `--collect-only` trước → sau | 2.652 → 2.685 *(+33)* ở `BG`; cây gộp = **3.100** *(= 3.067 + 33)*; nâng sàn **lúc gộp** *(việc orchestrator — xem trên)* | **ĐẠT** |

## Xét `DT4-R2-01` · `-02` — có cái nào phải NÊN SỬA không? *(quyết A của orchestrator: giữ GHI NHẬN)*
R3 tự xét độc lập, **kết luận: cả hai GIỮ GHI NHẬN**, ⛔ lên NÊN SỬA:

| | Lý do | Căn cứ đo |
|---|---|---|
| `DT4-R2-01` *(`\d` Unicode)* | NÊN SỬA đòi có **dữ liệu sai đang lọt hoặc bài sai đang xanh trên nguồn thật**. Ở đây: **0 ca** trên nguồn *(R1 + R2 đếm `[0-9]+` ⇒ cũng 4 hàng lệch, `itl_id` hợp lệ 7.879/7.879 duy nhất)*; ảnh **khoá checksum** *(`53a243b42101c314`)* và đã đối chiếu 0 lệch / 86.713 ô ⇒ rò chỉ xảy ra **nếu đóng băng lại từ nguồn đã đổi**, và khi đó `itl_id_lech` vẫn là cổng đếm. R3 đo: `fullmatch` + `\d` nhận `ITL#٣` ⇒ `True`; tương lai ⛔ vô hại cho H4 vì H4 nối bằng `dong_sheet` + `itl_id` | `ITL_ID_RE` — 1 chỗ ở khuôn + 1 chỗ ở bài *(`pat`)* ⇒ vá ≈ 5 phút, **gộp với `DT4-R3-01`** |
| `DT4-R2-02` *(`.strip()`)* | Đột biến bỏ `.strip()` làm cổng **NGHIÊM HƠN** *(`"USD "` ⇒ `D_la` ĐỎ)* ⇒ phía **an toàn** của cổng ⛔ hở; chỉ là hành vi *"đệm được cho qua"* ⛔ ghim. Nguồn thật: `D` 0 đệm | — |

Đề xuất **một việc DEV nhỏ sau gộp** gói 4 ý: `ITL_ID_RE → [0-9]+` *(khuôn + bài)* · ca `ITL#٣`/`ITL#5x`/`ITL#5 ` vào `itl_id_lech_khac_4` · ca `D = "USD "` · ca bỏ khoá `cot_A_rong` ⇒ TỪ CHỐI. **Ảnh ⛔ đổi** *(checksum giữ nguyên)*.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | Đúng spec Step 12 + WO-111; Đ3/Đ5 giữ — cổng khai `mong` *(7883 · 4 · 4 kỳ lệch)* NO cả hai chiều | 15 đột biến: 9 ĐỎ · 2 lỗ thật *(bài ghim)* · 4 dư *(có lớp thứ hai chứng minh bằng lệnh)* |
| **Dữ liệu** *(nguồn SA)* | ⛔ đọc lại — R1 + R2 đã đối chiếu nguồn 2 lần: 0 lệch / 86.713 ô + 4 hàng phụ + 9.843 hàng công thức *(theo chỉ dẫn vòng này)*. R3 chỉ đo **ảnh** đóng băng | `git diff 6516dcb isp/DT4` ⛔ động tới `gl_406.json`; `195 passed` |
| **Màn hình** | N/A — bước dữ liệu | — |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-10** *(`DT4-R3-01`)* | `NHE` | `gl_406.py` `ITL_ID_RE.fullmatch` ↔ bài `itl_id_lech_khac_4` | M1: `fullmatch → match` ⇒ **32/32 XANH**; `match("ITL#5x")`/`("ITL#5 ")` = `True`, `fullmatch` = `False`. Bài chỉ có `ITL#5`-kiểu *(0 lần `ITL#5x`/`ITL#٣` trong tệp bài — `grep -c` = 0)* | `DEV` *(gộp với `-R2-01`)* |
| **F-11** *(`DT4-R3-02`)* | `NHE` | `gl_406.py` `hc.get("cot_A_rong") is not True` ↔ bài `…cot_A_rong_False_thi_TU_CHOI` | M6: `is not True → is False` ⇒ **32/32 XANH**: ⛔ ghim ca thiếu khoá/giá trị lạ | `DEV` |

Không có `CHAN`/`NANG`. Hai ghi nhận ⛔ ảnh hưởng dữ liệu đóng băng hiện tại.

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm *(vai KIỂM ⛔ sửa mã; đột biến chạy trên bản sao)*. Bài đề xuất như mục "Đề xuất" ở trên.

## Câu hỏi cho orchestrator
1. **Gộp `isp/DT4`: (A)** *(khuyên)* gộp **ngay** — chặn = 0, cây gộp thử `KẾT: ĐẠT`; `DT4-R2-01/-02` + `DT4-R3-01/-02` vào **một việc DEV nhỏ** sau gộp. **(B)** vòng sửa trước gộp *(ảnh ⛔ đổi, ≈ 15 phút + R3 lại)* — ⛔ khuyên *(ghi nhận ⛔ ảnh hưởng dữ liệu)*.
2. Lúc gộp thật nhớ nâng sàn **3067 → 3100** *(script + bài ghim `:423`, cùng commit)*; ⛔ nâng thì bài ghim ĐỎ.
3. `DT4-R1-05` *(ISP `:1355` còn "5 tiền tệ")* vẫn mở ở orchestrator.
