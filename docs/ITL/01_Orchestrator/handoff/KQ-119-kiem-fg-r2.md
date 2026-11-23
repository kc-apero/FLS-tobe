# KQ-119 — biên bản kiểm `BG-117` *(R2 · Step 9 · FG · vòng sửa sau `KQ-118`)*

| | |
|---|---|
| **Thuộc** | `BG-117` *(mục "Vòng sửa sau R1")* · `WO-116` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-17 |
| **Phán quyết** | **`ĐẠT`** — 0 CHẶN · **1 NÊN SỬA** *(mới, `FG-R2-01`)* · 1 GHI NHẬN *(mới, `FG-R2-02`)* |

> Nền: `isp/FG` @ `cd2ba0b`, cụm PG riêng **5436**. Phạm vi = `git diff 8aa379d isp/FG` *(2 tệp: `tests/web/test_isp_f03_hd.py` +38 −8 · `BG-117`)*; `git diff 4dfb7bd HEAD -- fls` = **0 dòng**. Đột biến trên **bản sao** `git archive` ở `/tmp/r2_fg/` *(⛔ chạm worktree)*. Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_FG.md` *(v0.2)*.

## Cổng chạy lại *(Test tự chạy — so với `BG-117`)*
| Lệnh | `BG-117` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/web/test_isp_f03_hd.py -rs` | `3 passed` · 0 skip | `3 passed in 3.62s` *(mẫu số 3 bài, 0 skip)* | ✅ |
| `--duong-nen --cong 5436` *(script NHÁNH · `GOC = …/isp-fg` · chạy một mình)* | `KẾT: ĐẠT` · `26 = 26` · 2603 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `12 failed, 2575 passed, 2 xfailed, 14 errors in 332s` · `26 = 26 (thêm 0 · bớt 0) · chạy 2603 (mong ≥ 2496) · skipped 0` · web `3 failed, 664 passed` · `3 = 3 · chạy 667 (mong ≥ 667) · skipped 0` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | K1–K6 OK | K1–K6 `OK` · `189 file · 1.952 bảng · 736 ô ngày · 104 mã QĐ` | ✅ |
| `git diff 4dfb7bd HEAD -- fls` | 0 dòng | **0 dòng** | ✅ |

*(Tập đỏ đường nền `26`/`3` **là nợ có sẵn** — so theo node id, ⛔ do FG.)*

## Bảng AC *(ISP `## Step 9 · FG` §6/§8)*
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| FG-F1 | `FINAL` ĐẠT · `HD1_THANG` KHÔNG ĐẠT `5/23` · số 'chưa đo được' khớp tuyến | `tests/web/test_isp_f03_hd.py` F1 xanh; N8 *(`chua+1`)* ⇒ F1 ĐỎ ⇒ vế số 'chưa đo được' **cắn** | ĐẠT |
| FG-F2 | tệp đo vắng ⇒ hai thẻ `.gate.unk` | F2 xanh; N7 *(`dat !== false` ⇒ null thành xanh)* ⇒ ĐỎ | ĐẠT |
| FG-F3 | lý do 23 kỳ ở 390 px ⛔ tràn ngang | 3 vế đo trên thẻ HD1: `over` · `r ≤ iw` · `l ≥ 0`; **6/6** đột biến *bố cục* giết *(N1–N6)*. ⚠ nhưng xanh cả khi thẻ ⛔ mang `ly_do` *(N9/N11 sống ⇒ `FG-R2-01`)* | ĐẠT *(kèm NÊN SỬA)* |
| FG-F4 | `tests/web` sẵn có xanh | `--duong-nen` web `3 = 3`, 667 bài, skip 0 | ĐẠT |
| Cổng thoát | "3 vòng review" · push cần R1·R2·R3, chặn = 0 | R2 xong, **0 CHẶN** | ĐẠT *(chờ R3)* |

## Xét từng phát hiện R1
| Mã | Quyết | R2 đo | Kết |
|---|---|---|---|
| `FG-R1-01` NÊN SỬA | A — vá | `ed13520`: `_do_tran` trả `iw` + `r`/`l`; F3 thêm `r ≤ iw` · `l ≥ 0`. **N1** `.gate{min-width:520px}` *(chính M4 của R1)* ⇒ `1 failed` · `AssertionError … right=555.0 > innerWidth=390` *(`:307`)* ⇒ **ĐỎ**; bản gốc ⇒ `3 passed` ⇒ **XANH**. Mẫu số của vế ②: HD1 **đúng 1 thẻ** *(`len(hd1)==1` giữ)* | **ĐÃ SỬA** |
| `FG-R1-03` GHI NHẬN | vá | gọi trực tiếp: env **hợp lệ** *(`/bin/true`, `/etc/hostname`)* ⇒ `CHROME=/bin/true · PW=/etc/hostname` *(có tác dụng)*; env **rác** `/KHONG/CO` ⇒ rơi mặc định `/opt/pw-browsers/chromium-1243/…`; `FLS_CHROMIUM=/bin/true` chạy F3 ⇒ **`1 failed`** *(⛔ skip, ⛔ xanh — Chromium giả ⇒ đỏ thật)*; glob mặc định đổi `/opt/KHONG-CO` + env rác ⇒ `2 passed, 1 skipped` ⇒ chuỗi *thiếu ⇒ skip ⇒ `--duong-nen` ĐỎ* giữ *(script `tools/` **0 dòng** đổi so R1 — awk `skipped=0` nguyên)* | **ĐÃ SỬA** |
| `FG-R1-02` *(cả trang tràn 390 px)* | orchestrator B — backlog UIUX | ngoài AC-3; `BG-117` ghi rõ nhãn *"9/9 thẻ `.gate` ⛔ thủ phạm"* | **CHẤP NHẬN** |
| `FG-R1-04` *(sàn lúc gộp)* | orchestrator | sàn `2496/667` giữ; mức cộng FG **+3** *(⛔ đổi)* | **CHẤP NHẬN** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | ĐẠT. Ba mức đo, ⛔ xanh khi chưa đo | N7 ⇒ F2 ĐỎ · M1–M9 của R1 vẫn nằm trong bài *(không đổi)* |
| **Dữ liệu** *(kho thật, chỉ đọc)* | ĐẠT. Thẻ F03 = đúng tuyến `/gates` | `FINAL dat=True`; `HD1_THANG dat=False · 5/23`; `ly_do` = **431** ký tự; thẻ HD1 mang đủ *(`ly_do_in_card=True`, thẻ **543** ký tự)* |
| **Màn hình** *(trạng thái · thiết kế · phím · NFR)* | ĐẠT ở 390 px **cho thẻ**; ⛔ cho trang *(nợ `FG-R1-02`)* | thẻ HD1 `[35, 355]` trong `innerWidth=390`, `sw=cw=318` |

## Đột biến mới *(bản sao `git archive`, 11 chỗ **khác** M1–M9 của R1; mỗi chỗ cp từ bản gốc sạch)*
| Mã | Phá | Bài đỏ | Kết |
|---|---|---|:-:|
| N1 | `.gate{min-width:520px}` | F3 `right=555 > 390` | giết |
| N2 | `.gate{position:relative;left:-60px}` *(thẻ trượt trái)* | F3 `left=-25 < 0` *(vế `l ≥ 0` cắn — ⛔ chỉ `r` mới không thấy)* | giết |
| N3 | `.gate{position:relative;left:60px}` | F3 `right=415 > 390` | giết |
| N4 | `.gate{width:max-content}` | F3 `right=2562.5 > 390` | giết |
| N5 | `.gate{margin-right:-40px}` | F3 `right=395 > 390` *(vượt 5 px — ngưỡng sát)* | giết |
| N6 | `.gate{white-space:pre}` | F3 `sw=2512 > cw=318` *(vế ①)* | giết |
| N7 | `_muc`: `dat === true` → `dat !== false` | F2 | giết |
| N8 | chip 'chưa đo được' in `chua+1` | F1 | giết |
| N9 | bỏ cả khối `ly_do` khỏi `_the_cong` | — *(`3 passed`; thẻ **112** ký tự)* | **SỐNG** → `FG-R2-01` |
| N10 | chip 'đạt' in `data.khong_dat` | — *(`3 passed`)* | **SỐNG** → `FG-R2-02` |
| N11 | `ly_do.slice(0,40)` | — *(`3 passed`)* | **SỐNG** → `FG-R2-01` |

**8/11 giết · 3 sống** *(2 gốc ⇒ `FG-R2-01`, 1 ⇒ `FG-R2-02`)*. Hồi quy so R1: ⛔ tìm thấy — mọi đột biến *bố cục* tràn đều chết; bài **mất** gì sau vòng sửa: không.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `FG-R2-01` | `NANG` *(NÊN SỬA)* | `tests/web/test_isp_f03_hd.py:299-301` · `man_f03.js:34-35` | Bỏ/cắt khối `ly_do` ở `_the_cong` ⇒ `3 passed`. F3 chỉ khẳng `"5/23" in txt` — chuỗi ấy ở `da_do`, ⛔ `ly_do`. Grep `ly_do` trong tệp bài: **1** hit *(tên hàm)*. Đ3: bài *"lý do 23 kỳ ⛔ tràn"* xanh trên thẻ ⛔ có lý do. Sửa 1 dòng: `ly_do` lấy từ `GET /gates` ⊂ `hd1[0]["txt"]` | `DEV` |
| `FG-R2-02` | `NHE` | `man_f03.js:50` | N10 ⇒ `3 passed`; số `đạt`/`không đạt` trên dòng tóm ⛔ có bài *(⛔ thuộc AC)* | `DEV` *(tuỳ)* |

*(Chi tiết + luật phòng: sổ `SO_PHAT_HIEN_ISP-3.1_FG.md` v0.2.)*

## Đ1 · Đ3 · Đ4 · Đ5 *(luật đo)*
- **Đ1:** *"⛔ bài nào khẳng định `ly_do` có mặt"* — grep `ly_do` trong `tests/web/test_isp_f03_hd.py`: **1** hit, là tên hàm `test_FG_F3_ly_do_23_ky…`; trong `fls/` ⛔ cần *(phủ định nằm ở bài)*.
- **Đ3:** mọi phép so `0`/rỗng đã đếm mẫu số: HD1 `len==1`; `ly_do` 431 ký tự ⇒ tập ⛔ rỗng ở nền; N9 chứng minh bài **sẽ** xanh trên tập rỗng.
- **Đ4:** `sw=cw=318` *(thẻ HD1, vế ①)* ⇄ `r=355 ≤ iw=390` *(thẻ trong khung nhìn, vế ②)* ⇄ `documentElement.scrollWidth≈692` *(cả trang — `FG-R1-02`)*: ba số, ba vật.
- **Đ5:** cổng mới *(vế ②)* chứng minh ĐỎ bằng N1–N5; cổng *thiếu Chromium ⇒ ĐỎ* giữ.

## Bài thử mới *(`tests/nghiem_thu/`)*
Không thêm *(KIỂM ⛔ sửa mã; đột biến ở `/tmp/r2_fg/`, đã trả nguyên — worktree `git status` sạch trước commit)*.

## Câu hỏi cho orchestrator *(kèm khuyến nghị)*
- **Q-FG-R2-1:** `FG-R2-01` *(NÊN SỬA)* — gửi Dev vá ngay *(1 dòng, ⛔ đổi mức cộng +3)* hay chấp nhận?
  - **A *(khuyến nghị)*:** gửi Dev vá trước R3 — bài tên "lý do 23 kỳ" mà ⛔ canh lý do có mặt là xanh giả; ⛔ thêm bài *(cùng hàm)*.
  - **B:** ghi nhận, vá ở lượt khác.
- **Q-FG-R2-2:** `FG-R2-02` — A *(khuyến nghị)*: vá cùng lúc với `FG-R2-01` *(1 dòng trong F1)*; B: bỏ.
