# KQ-079 — biên bản kiểm `BG-076` *(ISP 3.1.2 · Step 2 · `C1` · vòng **R3** — vòng xác nhận cuối; CHỈ quét phần đổi sau R2: `9feb114..6cd017b`)*

| | |
|---|---|
| **Thuộc** | [`BG-076`](BG-076-ban-giao-wo-075.md) mục *"Vòng sửa sau R2 (KQ-078)"* · [`WO-075`](WO-075-isp-c1-ix-fx-doc-tinh.md) · căn cứ R2 [`KQ-078`](KQ-078-kiem-c1-r2.md) · R1 [`KQ-077`](KQ-077-kiem-c1-r1.md) |
| **Kiểm bởi** | `fls-test` *(R3 — phiên mới, độc lập; ⛔ đọc log nào của tác giả, mọi số dưới là R3 tự đo)* · 2026-11-17 · cụm reviewer **5445** |
| **Phán quyết** | **`ĐẠT`** *(thang lệnh giao R3: được gộp khi **0 CHẶN và 0 NÊN SỬA còn mở**)* — **5/5 AC ĐẠT** · **5/5** phát hiện R2 đã xử: **4 ĐÃ SỬA** *(`C1-R2-01` NÊN SỬA · `-02` · `-03` · `-04`, mỗi cái tái hiện trên bản cũ `9feb114` rồi bị bắt trên `a0ff60f`)* · **1 CHẤP NHẬN** *(`-05` — việc orchestrator/BA theo lệnh giao)* · **0** CHƯA SỬA · **0** hồi quy · `--duong-nen` 5445 **`KẾT: ĐẠT`** exit 0. **1** phát hiện mới: **0** CHẶN · **0** NÊN SỬA · **1** GHI NHẬN *(`C1-R3-01`)* |
| **Sổ phát hiện** | [`docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C1.md`](../../04_Test/review/SO_PHAT_HIEN_ISP-3.1_C1.md) **v0.3** *(đổi 5 ô Trạng thái `C1-R2-*` + thêm `C1-R3-01`; đo máy: 12 hàng cũ giữ nguyên mọi ô trừ ô cuối, 12 ô/hàng)* |
| **Phạm vi R3** | `git diff 9feb114 isp/C1` = `a0ff60f` *(mã + bài: 5 tệp `+216 −1`)* + `6cd017b` *(phiếu `BG-076`: `+53 −0`, chỉ THÊM)*. ⛔ quét lại phần R1/R2 đã quét |

## Cổng vào
| Kiểm | Kết quả |
|---|---|
| git | `isp/C1` HEAD = `6cd017b` ← `a0ff60f` *(cha `9feb114` = `KQ-078`)*. WIP `37772f3` tồn tại, `git diff --numstat 37772f3 a0ff60f` = **0** dòng — khớp `BG`. `git status --short` = **0** dòng trước lượt R3 *(mọi phép phá trên BẢN SAO `git archive` ở nháp)*. Nhánh cục bộ, ⛔ đẩy |
| spec | `git diff 9feb114 isp/C1 -- docs/ITL/02_BA` = **0** dòng *(vòng sửa ⛔ chạm spec; ISP v3.1.2 Step 2 · C1 = bản `WO-075`)* |
| làn | **6/6** tệp diff: `fls/cau_hinh/fx.py` *(chỉ chú thích, +4)* · `fls/api/bang_tuyen.py` *(chỉ chú thích, +5)* · `tools/soi_bang_tuyen.py` *(ⓔ4: 8 dòng mã + 10 chú thích)* · `tests/cau_hinh/test_fx.py` · `tests/api/test_isp_config_fx.py` — làn **BE-CF** — + phiếu `BG-076` của tác giả. Bài cũ: dòng **xoá** trong `tests/` = **1** *(`(202409, {"USD": "-5"}, "USD"),  # tỷ giá ≤ 0` — chỉ gỡ nhãn cuối dòng, ca giữ nguyên)* ⇒ ⛔ kỳ vọng nào đổi. ⛔ refactor; ⛔ chạm bước khác |
| môi trường | venv Python 3.13.18 · `PG_DSN=…5445/fls` · `PG_DSN_TEST=…5445/fls_test` · `PYTHONUTF8=1` · `PYTEST_ADDOPTS` **gỡ** · `pg_isready -p 5445` accepting. Phép phá chạy **offline** *(`--noconftest -m "not pg"`, DSN trỏ cổng chết `:1` ⇒ ⛔ chạm cụm nào)*. Log + kịch bản: `scratchpad/r3_c1/` |
| ⚠ kịch bản `--duong-nen` | Lệnh giao nói *"`tools/dung_moi_truong_isp.sh` ⛔ có trên `isp/C1`"* — **sai** *(Đ1)*: `git ls-files` ⇒ có, từ `d895878` · `5be45f5` *(S0 trước R2)*; bản này ⛔ có `MONG_PYTEST_*` *(đúng Q8)*. Bản của `isp-s0` đặt `GOC` = thư mục chứa script *(`:137` · `cd "$GOC"` `:249`)* ⇒ chạy nó từ worktree `isp-c1` vẫn đo **mã S0**, ⛔ mã C1. R3 chạy **bản của chính `isp/C1`** từ worktree `isp-c1` *(log in `GOC (mã fls) = …/isp-c1`)*. Sàn mẫu số tự đo thay hằng thiếu: `skipped`/`deselected` trong log = **0** dòng; mẫu số **2.585** ≥ sàn S0 `2490` |
| ký tự vô hình · PII · bí mật | **269** dòng THÊM của diff: **0** ký tự vô hình *(NBSP · BOM · U+200B–D · U+2000–200A · U+2028/9 · U+202F · U+205F · U+3000 · NEL · U+001C–1F · VT · FF)* · **0** email *(4 khớp thô = `@pytest.mark.parametrize`)* · **0** `Email Address`/`Diễn giải`/`Số chứng từ` · **0** mẫu bí mật · **0** dãy ≥ 7 chữ số |

## Cổng chạy lại *(R3 tự chạy từ worktree `isp-c1`, cây `6cd017b` — so với `BG-076` mục vòng sửa R2 @ `a0ff60f`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/cau_hinh tests/api/test_isp_config_fx.py tests/api/test_bang_tuyen.py tests/api/test_soi_bang_tuyen.py tests/api/test_ba07_phu_het_tuyen.py` | `172 passed in 2.02s` *(156 → 172)* | exit **0** · `172 passed in 1.96s` — thu thập theo tệp: `test_fx` **61** · `test_nguon_tinh` 29 · `test_isp_config_fx` **35** · `test_bang_tuyen` 20 · `test_soi_bang_tuyen` 25 · `test_ba07_phu_het_tuyen` 2 *(= 172)*; bản `9feb114`: `test_fx` 53 · `test_isp_config_fx` 27 ⇒ **+16** | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5445` *(bản `isp/C1` — xem Cổng vào)* | *(5434)* `12 failed, 2557 passed, 2 xfailed, 14 errors` · 26 = 26 · web 3 = 3 · `KẾT: ĐẠT` | exit **0** · 7/7 `[ĐẠT]` *(`26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · `11 kept` · `chay 9845 / co 9967` · `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2557 passed, 2 xfailed, 14 errors in 302.51s` *(mẫu số **2.585** = 12 + 2557 + 2 + 14)* ⇒ `[ĐẠT] … 26 = 26 node id (thêm 0 · bớt 0)` · `tests/web` `3 failed, 661 passed in 173.58s` *(**664**)* ⇒ `[ĐẠT] 3 = 3` · **`══ KẾT: ĐẠT — mọi phép kiểm khớp mong`** | ✅ |
| `/home/user/FLS-tobe/.venv/bin/lint-imports` | `11 kept, 0 broken` | exit **0** · `Contracts: 11 kept, 0 broken.` · `fls.cau_hinh la config thuan, khong duoc biet tang kho KEPT` *(vòng này ⛔ đổi import — chú thích + ⓔ4 ở `tools/`)* | ✅ |
| `python tools/soi_bang_tuyen.py` | exit 0 · 41 `OK` | exit **0** · **41** dòng `OK` · `OK /api/fls/v1/config/fx` · `TINH : ['fls/cau_hinh/tinh/ix_fx_mau.json'] · vet 10 ham` · `✅ ban khai KHOP SQL that o ca 41 tuyen` | ✅ |
| ↳ **phá** đầu-cuối ⓔ4 *(bản sao: chèn hằng `"fls/cau_hinh/tinh/ix_fx_mau.json"` vào hàm của tuyến KHO `/queue/coverage`, `nguon_tinh=()`)* | — | CLI exit **1** · đúng **1** câu `GET /api/fls/v1/queue/coverage: ham trong vet (3 ham) mang duong tinh '…ix_fx_mau.json' ma \`nguon_tinh\` ⛔ khai` | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `pg_verify: khop` | *(bước dựng của `--duong-nen`)* exit **0** · y như `BG` | ✅ |
| `python tools/kiem_thuyet_minh.py` | exit 0 · 31/31 | exit **0** · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `11/16 khop · 5 lech` | exit **1** · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — kho `fls` cụm 5445 rỗng, y `BG`/R1/R2 | ✅ *(đỏ do kho rỗng)* |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC | exit **1** · `FileNotFoundError: …/isp-c1/.venv/Scripts/lint-imports.exe` *(đường Windows cứng — ngoài ISP)* | ✅ *(khớp; tính **⛔ ĐO ĐƯỢC** — Đ5)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `178 file` | xem §Cổng ra *(chạy SAU khi thêm phiếu này)* | ✅ |

## Bảng AC *(`WO-075` = ISP mục 6 — vòng sửa R2 ⛔ chạm mã chạy của `fx.py`/`xu_ly.py`/`bang_tuyen.py`, chỉ chú thích)*
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 · `C1-B1` | 4 dòng, VND = 1, `thieu = trung = lac = []` | bài `C1_B1` xanh trong 172; đột biến `R3-f4` *(ngưỡng `> 0` → `> 1`)* ⇒ `test_C1_B1_…` đỏ *(VND = 1 bị từ chối — bài thật sự đi qua `_so`)* | **ĐẠT** |
| AC-2 · `C1-B2` | `trung = ['202407']`; ⛔ cộng đôi | bài xanh *(mã `kiem` ⛔ đổi vòng này; R2 đã chứng minh M7/N5 bị bắt)* | **ĐẠT** |
| AC-3 · `C1-B3` | `thieu = ['202408']` | bài xanh + `test_R1_01a/b` ×4 xanh | **ĐẠT** |
| AC-4 · `C1-B4` | 200 đúng hợp đồng; `soi` xanh với tuyến mới | 4 bài `pg` của `test_isp_config_fx.py` xanh trên cụm 5445 *(trong 172)*; `soi` 41/41 + ⓔ4 mới xanh trên bảng thật *(mẫu số **1/41** tuyến mang chuỗi dưới `fls/cau_hinh/tinh/` — Đ3, ≠ rỗng)*; `xu_ly.py` · `cua.py` **0** dòng đổi ⇒ 12 lượt HTTP của R2 còn hiệu lực | **ĐẠT** |
| AC-5 · `C1-B5` | `fls/cau_hinh` ⛔ import psycopg/repo/db | `11 kept`; `fx.py` vòng này chỉ +4 dòng chú thích *(`git diff` ⇒ 0 dòng `import`)* | **ĐẠT** |

## Đối chiếu mục 8 *(Exit criteria)*
| Dòng mục 8 | Đo | Kết |
|---|---|---|
| `C1-B1…B5` xanh, đỏ trước khi có mã | xanh `172 passed`. "Đỏ trước" của **16** bài vòng sửa R2: ⓔ4 là TDD thật — bài mới trên mã `9feb114` ⇒ `2 failed, 166 passed` *(đúng 2 ca `test_R2_04_soi_DO…`)*; 14 bài còn lại ghim mã vốn đúng ⇒ đỏ-trước = đột biến SỐNG trên bài cũ, CHẾT trên bài mới *(bảng dưới: **7/8** mẫu R2 sống trên bộ cũ — riêng E3 vốn bị 1 bài bắt, nay 3 — và **8/8** bị bắt trên bộ mới)* | **ĐẠT** |
| regression `tests/api` xanh | `--duong-nen` toàn bộ 26 = 26 · web 3 = 3 *(tập đỏ = đường nền, thêm 0 · bớt 0)* | **ĐẠT** |
| 3 vòng review xong | R1 `KQ-077` ✓ · R2 `KQ-078` ✓ · R3 = phiếu này ✓ | **ĐẠT** |
| điều kiện PUSH: đủ R1 · R2 · R3, chặn = 0 | CHẶN mở = **0**; NÊN SỬA mở = **0** *(`C1-R1-01` · `-02` · `C1-R2-01` đều ĐÃ SỬA)*; GHI NHẬN mở: `C1-R3-01` *(⇒ trước `C4`)* + các hàng chấp nhận chuyển orchestrator | **ĐẠT** *(push = việc orchestrator)* |

## Trạng thái phát hiện R2 *(bản cũ = `9feb114` · bản mới = `a0ff60f`; bản sao `git archive`, bộ 5 tệp offline: cũ `152 passed`, mới `168 passed` + 4 `pg` deselected)*
| F R2 | Mức | Trạng thái R3 | Bản cũ *(tái hiện)* | Bản mới *(đo)* |
|---|---|---|---|---|
| `C1-R2-01` | **NÊN SỬA** | **ĐÃ SỬA** | `R2-f7` `d <= 0 → d < 0` · `R2-f9` gỡ chốt ⇒ `152 passed` SỐNG ×2 *(cả trên `9feb114` lẫn bài cũ + mã mới)*; `R2-fP` *(phẩy → chấm)* SỐNG | f7 ⇒ `6 failed` · f9 ⇒ `6 failed` *(6 ca `test_R2_01_…BANG_0…`: 4 chuỗi + `int` + `Decimal`)* · fP ⇒ `1 failed` *(`…DAU_PHAY…`)* · **R3-f5** đổi câu `"⛔ > 0"` ⇒ `6 failed` *(bài hỏi LÝ DO — đúng luật `C1-R2-01`)*. Dò biên 0 trên mã: **19/19** lối vào bằng 0 bị từ chối *(`'0'` · `'-0'` · `'+0'` · `'0E0'` · `'0e-5'` · `' 0 '` · `'\t0\n'` · `'٠'` · `'０'` · `'-0.0'` · `'00000.0000'` · `'0.'` · `'.0'` · `'0,0'` · `0` · `-0` · `D('-0')` · `D('0E+3')` · `D('0.0000')` — 18 câu `> 0`, `'0,0'` câu "phải số")*; qua `doc_van_ban` JSON `0` · `0.0` · `-0` · `0e0` · `"0"` ⇒ **5/5** `LoiFX`; chiều kia: `'0.0000001'` · `1` · `'1'` được NHẬN. Ca `"-5"` vẫn xanh dưới f7/f9 ⇒ chú thích mới nói đúng |
| `C1-R2-02` | GHI NHẬN | **ĐÃ SỬA** | `R2-g1` · `R2-s1` · `R2-g2` · `R2-f2` · `R2-f3` ⇒ `152 passed` SỐNG ×5 | bị bắt **5/5**: `2 · 2 · 1 · 1 · 1 failed` *(`02a[None]`/`[list_rong]` · `02b` · `02c`)*. ⚠ Luật của hàng này bị tái phạm ở chốt ⓔ4 ⇒ `C1-R3-01` |
| `C1-R2-03` | GHI NHẬN | **ĐÃ SỬA** *(vế ghim giới hạn)* | `R2-E3` gỡ ⓔ3 ⇒ `1 failed` | E3 ⇒ `3 failed` *(+ `test_R2_03[xem_truoc]` · `[lo_xem_truoc]`)*. Mẫu số đo độc lập: `len(HAM)` **41** · ⛔ gọi tên `conn` tầng đầu **3/41** `['lo_xem_truoc', 'ty_gia', 'xem_truoc']` · hai hàm khai tĩnh ⇒ `kiem_bang_tuyen` **0** câu · `soi` **3** câu — khớp chú thích `bang_tuyen.py:810-814` |
| `C1-R2-04` | GHI NHẬN | **ĐÃ SỬA** | bài mới trên mã cũ ⇒ `2 failed, 166 passed` *(TDD thật)* | xanh; 8 đột biến ⓔ4 *(bảng dưới)*: **6** bị bắt · **2 SỐNG** ⇒ `C1-R3-01`; bảng thật **1/41** tuyến mang chuỗi dưới `THU_MUC/`, hằng `THU_MUC` trần nằm ở đúng tuyến ấy ⇒ phép so tiền tố `+ "/"` là cần *(R3-s2 bị bắt 3 bài)*; phá đầu-cuối CLI exit 1 |
| `C1-R2-05` | GHI NHẬN | **CHẤP NHẬN** *(việc orchestrator/BA — lệnh giao R3)* | — | `07_API_CONTRACT.md:850` vẫn `⬜` và ⛔ có câu `?run_id= ⇒ 400` *(đo)* ⇒ gộp cùng `C1-R1-03` lúc gộp |

**Hồi quy do chính vòng sửa: 0** — toàn bộ 26 = 26 · web 3 = 3 · `soi` 41/41 · `lint` 11/11 · bài cũ ⛔ đổi kỳ vọng · `fx.py`/`bang_tuyen.py` chỉ đổi chú thích.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + AP §3.2.4)* | **ĐẠT** — NÊN SỬA duy nhất của R2 đã đóng ở đúng biên *(tỷ giá 0 ⇒ `SUMIFS = 0`)*; ⓔ4 làm cổng `nguon_tinh` đỏ đủ hai chiều *(Đ5)*. Còn 1 GHI NHẬN về độ phủ của ⓔ4 | **23** đột biến R3 *(15 tự dựng `R3-*` + 8 mẫu R2 dựng lại)*, mỗi mẫu khớp đúng 1 lần, trả nguyên so sha256 — xem bảng dưới. Sống trên bộ mới: `R3-f3` *(tương đương)* · `R3-f6` *(đảo thứ tự `> 0` ↔ khuôn — chỉ đổi lý do của số ÂM, ca `"-5"` cố ý ⛔ hỏi lý do, `BG` yếu #4 ⇒ ⛔ tính)* · `R3-s5` · `R3-s8` *(⇒ `C1-R3-01`)* |
| **Dữ liệu** *(kho thật chỉ đọc)* | **N/A — bước ⛔ đọc/ghi kho**, vòng sửa ⛔ đổi luật nhận số | `fls-pg-1` ⛔ có ở máy này *(O4 = A)*; kho `fls` cụm 5445 `fls_itl = 0 dòng` *(kết nối chỉ đọc, bước kiểm của `--duong-nen`)*. Luật biên 0 chỉ từ chối thêm giá trị = 0 — ảnh `DT2` R2 đo **185/185** ô dương, khớp khuôn ⇒ 0 ô thật bị từ chối thêm |
| **Màn hình** | **N/A** *(ISP mục 6: FE = N/A; màn ở `F4`)* | `fls/web` · `cua.py` · `xu_ly.py` **0** dòng đổi vòng này; cửa trả khuôn đã R2 đo 12 lượt — còn hiệu lực |

## Phép phá R3 *(bản sao `git archive`; bộ 5 tệp offline; kịch bản `scratchpad/r3_c1/dot_bien_r3.py` · `dot_bien_r2_lai.py`, log `dot_bien_r3.log` · `dot_bien_r2_lai.log`)*
| Mã | Đột biến | Bài MỚI *(`a0ff60f`, nền 168)* | Bài CŨ + mã mới *(nền 152)* |
|---|---|---|---|
| `R3-f1` | `d <= 0 → d < 0` | `6 failed` — bắt | 152 passed — sống |
| `R3-f2` | gỡ chốt `> 0` | `6 failed` — bắt | sống |
| `R3-f3` | `d <= 0 → d == 0` | sống — **tương đương** *(âm do khuôn bắt)* | sống |
| `R3-f4` | `d <= 0 → d <= 1` *(Đ5 chiều kia)* | `13 failed` — bắt | `12 failed` — bắt |
| `R3-f5` | đổi câu lý do `"⛔ > 0"` | `6 failed` — bắt | sống |
| `R3-f6` | đảo thứ tự: khuôn trước `> 0` | sống *(chỉ đổi lý do của số âm — ⛔ tính, xem Logic)* | sống |
| `R3-f7` | `.replace(",", ".")` trước `Decimal` | `1 failed` — bắt | sống |
| `R3-s1` | tắt ⓔ4 | `2 failed` — bắt | sống |
| `R3-s2` | tiền tố `THU_MUC` ⛔ `/` | `3 failed` — bắt | `2 failed` — bắt |
| `R3-s3` | bỏ `and x not in nt` | `3 failed` — bắt | `2 failed` — bắt |
| `R3-s4` | `isinstance(nt, tuple)` → `nt` *(bỏ tuyến `nt=()`)* | `1 failed` — bắt | sống |
| `R3-s5` | `isinstance(nt, tuple)` → `True` | **sống** ⇒ `C1-R3-01` | sống |
| `R3-s6` | ⓔ4 đọc `chuoi_cua_tuyen` thay `do_chuoi` | `2 failed` — bắt | sống |
| `R3-s7` | ⓔ4 chạy mà ⛔ báo | `2 failed` — bắt | sống |
| `R3-s8` | ⓔ4 chỉ chuỗi `.json` | **sống** ⇒ `C1-R3-01` | sống |

Tổng R3 tự dựng: **15** mẫu × bộ mới ⇒ **11 bị bắt · 4 sống** *(1 tương đương · 1 ⛔ tính · 2 ⇒ `C1-R3-01`)* · **0** ⛔ đo được. Bộ cũ ⇒ **3** bị bắt *(f4 · s2 · s3)* · **12** sống — **8** chốt nay mới có bài *(f1 · f2 · f5 · f7 · s1 · s4 · s6 · s7)*.

## Phát hiện *(chi tiết + luật phòng tái phạm ở sổ riêng)*
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `C1-R3-01` | GHI NHẬN *(`NHE`)* | `tools/soi_bang_tuyen.py:360` *(`if isinstance(nt, tuple):` của ⓔ4)* · `:361-363` *(lọc `startswith(THU_MUC + "/")`)* · lời hứa ở chú thích `:355-356` *("Áp cho MỌI tuyến … `nt` sai kiểu ⇒ bỏ qua — giữ MỘT câu")* | Bản sao `a0ff60f`: **R3-s5** `isinstance(nt, tuple)` → `True` ⇒ `168 passed`; dưới nó tuyến `/config/fx` với `nguon_tinh=None` ⇒ `soi` **NỔ** `TypeError: argument of type 'NoneType' is not iterable` *(hôm nay: đúng 1 câu "kieu NoneType")*, `nguon_tinh=[]` ⇒ **2** câu *(hôm nay 1)*. `test_R2_02a` dùng tuyến `so` — đồ thị ⛔ mang chuỗi dưới `THU_MUC/` ⇒ ⛔ chạm vế này. **R3-s8** lọc thêm `.endswith('.json')` ⇒ `168 passed` — mọi ca ⓔ4 đều `.json`. **Tái phạm luật `C1-R2-02`** trong chính vòng sinh luật ấy *(vòng sửa chạy E4a/b/c, ⛔ chạy vế `isinstance`)*. Hậu quả hôm nay **0**: bảng thật `soi()` = `[]`, 1/41 tuyến mang chuỗi dưới `THU_MUC/`; đột biến s5 làm cổng NỔ *(ồn)*, ⛔ xanh giả | `DEV` *(trước `C4` — người dùng thứ hai của `nguon_tinh`)*: thêm ca tuyến `/config/fx` với `nguon_tinh ∈ {None, []}` ⇒ `soi` đúng **1** câu, ⛔ ngoại lệ; và ca đường không `.json` dưới `THU_MUC/` trong đồ thị tuyến kho ⇒ ⓔ4 đỏ |

## Bài thử mới *(`tests/nghiem_thu/`)*
⛔ — lệnh giao R3 giới hạn commit vào **phiếu + sổ riêng**. Hai ca của `C1-R3-01` đã chứng minh trên bản sao *(`scratchpad/r3_c1/do_s5.py`: mã thật 1 câu/ca · dưới `R3-s5` NỔ/2 câu)*; tác giả chép vào `tests/api/test_isp_config_fx.py` khi làm `C4`.

## Cổng ra *(phần R3 làm trong lượt này)*
- Phiếu này + sổ riêng v0.3 commit lên nhánh **cục bộ** `isp/C1` *(⛔ đẩy)*. `kiem_tai_lieu.py` chạy lại SAU khi thêm phiếu — kết quả ghi ở commit message.
- ⛔ chạm `03_TRACEABILITY_GAP_REPORT.md` · `handoff/README.md` · dashboard · `WO-075` · `tests/nghiem_thu/` — orchestrator ghi lúc gộp.

## Ghi chú cho orchestrator lúc gộp
1. **Q8**: sàn `MONG_PYTEST_TOAN_BO` của cây gộp = số thu thập lúc gộp; `C1` đóng góp **+95** so với nền `2490` *(R3 đo toàn bộ **2.585** trên `isp/C1`, khớp `BG`)*.
2. `C1-R1-03` + `C1-R2-05`: một lần sửa `BA-07:850` — đổi `⬜` → `✅` **và** ghi `?run_id= ⇒ 400 FLS-BAD-REQUEST`.
3. `C1-R3-01` *(GHI NHẬN)* mang sang phiếu `C4`, ⛔ chặn gộp.
