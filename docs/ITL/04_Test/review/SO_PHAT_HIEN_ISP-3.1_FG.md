# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `FG` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.3 · **Ngày:** 2026-11-17 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-118` · R2 `KQ-119` · R3 `KQ-120`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 9 · FG** · `WO-116` · `BG-117`

> Vì sao là tệp riêng: cùng lý do `SO_PHAT_HIEN_ISP-3.1_CG1.md` — sổ chung sống ở nhánh khác, ghi thẳng ⇒ xung đột gộp. Orchestrator chép nguyên hàng, giữ mã.
>
> **Thang lớp:** **A1** lỗi mã sửa trong bước · **A2** lỗi mã lớp lặp *(kèm luật phòng)* · **B1** lệch spec / thiếu bài · **B2** spec·ISP sai → orchestrator. **Mức:** CHẶN · NÊN SỬA · GHI NHẬN *(↔ `CHAN` · `NANG` · `NHE`)*. **Sổ CHỈ THÊM:** vòng sau *(R2/R3)* chỉ đổi ô **Trạng thái** + thêm hàng, ⛔ viết lại.
>
> Mọi số R1 **tự đo** trên `isp/FG` @ `243a1ba` *(mã `4933038`, nền `4dfb7bd`)*, cụm PG riêng **5446**; đột biến trên **bản sao** `git archive` ở `/tmp/r1_fg/` *(⛔ chạm worktree; `git diff 4dfb7bd HEAD -- fls` = 0 dòng)*.
>
> **Kết R3: `ĐẠT` — 0 CHẶN · 0 NÊN SỬA mở** *(R3 `KQ-120`: `FG-R2-01`/`02` ĐÃ SỬA — N9/N10/N11 đều GIẾT, trả nguyên ⇒ `3 passed`; 2 GHI NHẬN mới `FG-R3-01`/`02`)* — **Kết R2: `ĐẠT` — 0 CHẶN.** *(R2: `FG-R1-01`/`03` ĐÃ SỬA · `FG-R1-02`/`04` CHẤP NHẬN · 2 phát hiện mới `FG-R2-01` NÊN SỬA · `FG-R2-02` GHI NHẬN)* — **Kết R1: `ĐẠT` — 0 CHẶN.** 4 phát hiện: **1** NÊN SỬA *(`FG-R1-01` — bài FG-F3 mù một hướng tràn; gửi Dev)* · 3 GHI NHẬN *(`FG-R1-02…04`)*.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `FG-R1-01` | FG | R1 | B1 | **NÊN SỬA** | `tests/web/test_isp_f03_hd.py:280` *(`assert hd1[0]["over"] is False`)* · `:252` *(`over: g.scrollWidth > g.clientWidth`)* | **FG-F3 chỉ đo thẻ có tự cuộn không, ⛔ đo thẻ có nằm trong khung nhìn không.** Đột biến **M4** *(bản sao: `.gate{min-width:520px}` thêm vào `hinh.css`)* ⇒ mọi thẻ `sw = cw = 516–518` ở viewport 390 *(thẻ HD1 `cw=518` > 390)*, `over=False` ⇒ **`3 passed`** — bài ⛔ cắn một thẻ rộng hơn màn. Hai đột biến cùng lớp **cắn** *(M3 `white-space:nowrap` ⇒ F3 đỏ; M9 `ly_do` thay dấu cách bằng NBSP ⇒ HD1 `sw=566 > cw=318` ⇒ F3 đỏ)* — vì ở đó nội dung tràn **trong** thẻ. Khi một phần tử ép bề rộng *(min-width, track lưới giãn theo min-content)*, `clientWidth` giãn theo ⇒ `scrollWidth == clientWidth` mãi. Nền thật: thẻ `[35, 355]` trong 390 ⇒ hôm nay đúng; chỉ là bài **yếu một hướng**. AC-3 chữ *"⛔ tràn ngang"* của ISP bị phủ **một nửa** | **Dev** *(làn FE, cùng vòng sửa nếu có R1-sửa/R2)*: thêm vào `_do_tran` `r: g.getBoundingClientRect().right` và khẳng `right ≤ innerWidth` *(và `left ≥ 0`)* cho thẻ HD1; chứng minh ĐỎ bằng M4 *(phá → cắn → trả)*. Rẻ *(2 dòng)*; ⛔ đổi nghĩa AC | Bài "⛔ tràn" phải đo **hai** vế: *nội dung ⛔ vượt thẻ* **và** *thẻ ⛔ vượt khung*; đo một vế thì phép so xanh trên đúng trường hợp thẻ tự giãn *(Đ5: đột biến phải phủ cả hai chiều của lớp lỗi)* | **ĐÃ SỬA** *(R2 `KQ-119`: `ed13520` đo thêm `r ≤ iw` · `l ≥ 0`; M4 ⇒ `right=555 > 390` ĐỎ, trả ⇒ `3 passed`)* |
| `FG-R1-02` | FG | R1 | B2 | GHI NHẬN | `fls/web/tep/man_f03.js` *(vỏ F03)* · `hinh.css` bố cục `.wrap`/rail · ISP Step 9 mục 3 | *(Dev yếu "giới hạn đo được" — R1 **xác nhận ngoài AC-3**)* Ở 390 px **cả trang** F03 tràn ngang: `documentElement.scrollWidth = 692 > 390` *(R1 đo Chromium thật, tuyến thật)*. Phần tử vượt khung đầu tiên: `TABLE`/`THEAD`/`TR` `right = 429` *(bảng mẫu số/độ phủ)*; **9/9 thẻ `.gate` ở `[35, 355]`** — ⛔ thủ phạm. ⇒ nằm **ngoài** câu AC-3 *("lý do 23 kỳ ở 390 px ⛔ tràn")* — AC-3 nói về lý do, ⛔ về trang. Mục 3 ISP *"Loại trừ: màn mới · khoan xuống"* + *"sửa tối thiểu ở `man_f03.js`"* ⇒ ⛔ phải việc của FG. Nhưng đây là **nợ responsive thật** của F03 trên điện thoại, và bài FG-F3 *(xanh)* có thể bị đọc nhầm thành *"F03 ổn ở 390 px"* *(Đ4: nhãn con số)* | **Orchestrator/BA**: ghi một việc responsive F03 *(rail/shell `--rail-w` + bảng 429 px)* vào backlog UIUX nếu 390 px thuộc NFR; docstring bài đã đúng *("CHÍNH thẻ HD1 ⛔ của cả trang")* — giữ nguyên | Bài xanh phải mang **nhãn phạm vi đo** ngay chỗ in *(thẻ HD1, ⛔ trang)*; reviewer ⛔ kết luận "màn ổn ở bề rộng X" từ một bài đo một phần tử | **CHẤP NHẬN** *(orchestrator quyết B — backlog UIUX; R2 `KQ-119`)* |
| `FG-R1-03` | FG | R1 | B1 | GHI NHẬN | `tests/web/test_isp_f03_hd.py:210-233` *(`_pw_index`, `_chromium`, `PW`, `CHROME`)* · `tools/dung_moi_truong_isp.sh:396-402` | *(Q-FG-1 = A, orchestrator đã quyết — R1 **chỉ kiểm hai điều được dặn**.)* **(1) Thiếu Chromium ⇒ bài làm gì:** R1 sao bản thử đổi glob `/opt/pw-browsers/…` thành đường không có ⇒ `2 passed, 1 skipped` *(F3 SKIP, ⛔ xanh)*; đưa dòng tổng kết mẫu `3 failed, 664 passed, 1 skipped` qua đúng đoạn `awk` của `--duong-nen` ⇒ `chạy 667 · skip 1` ⇒ `[ "$n_skip" = 0 ]` sai ⇒ `mau_so_dat` rỗng ⇒ nhánh `do_` **ĐỎ**. Chuỗi *skip ⇒ ĐỎ* **giữ** *(đo từng mắt xích, ⛔ chạy trọn vòng trên môi trường thiếu Chromium)*. **(2) F3 có ĐỎ khi thẻ tràn:** **có** — M3 và M9 giết F3 *(xem `FG-R1-01` cho hướng M4 sót)*. Phụ: đường Chromium **gõ cứng Linux** *(`/opt/node-tools/…`, `/opt/pw-browsers/chromium-*/chrome-linux64/chrome`)* ⇒ trên máy khác *(Windows owner)* F3 **luôn skip** ⇒ `--duong-nen` ĐỎ vĩnh viễn — đúng Đ5, nhưng ⛔ có biến môi trường ghi đè | **Dev** *(nếu muốn)*: cho phép ghi đè `FLS_CHROMIUM`/`FLS_PW_INDEX`; ⛔ chặn bước — script `.sh` vốn chỉ chạy Linux | Một phép pixel gõ cứng đường công cụ phải khai **cách ghi đè** cạnh chỗ gõ cứng *(⛔ chỉ khai "thiếu ⇒ ĐỎ")* | **ĐÃ SỬA** *(R2 `KQ-119`: `FLS_PW_INDEX`/`FLS_CHROMIUM` có tác dụng; rác ⇒ rơi mặc định; thiếu ⇒ skip ⇒ ĐỎ giữ)* |
| `FG-R1-04` | FG | R1 | B2 | GHI NHẬN | `tools/dung_moi_truong_isp.sh:396-402` *(`MONG_PYTEST_TOAN_BO=2496`)* · `duong_nen_bai_do.txt` · `CG1-R1-01` | *(Mang từ `CG1-R1-01`, ⛔ lỗi mới của FG.)* Nhánh FG cắt từ CG1 ⇒ vẫn mang script cổng **yếu hơn S0** *(`-rfE` ⛔ `x`, thiếu 2 dòng `XFAIL`, thiếu che DSN)*; `--duong-nen` toàn bộ ra `12 failed, 2575 passed, 2 xfailed, 14 errors` ⇒ `26 = 26` *(S0: `28 = 28 · XFAIL 2 = 2`)*. Sàn FG `2496 = 2493 + 3` đúng **trên bản script CG1**; lúc gộp, orchestrator lấy bản S0 rồi cộng **+33 +3** *(⛔ chỉ +33)*. Bước FG chỉ đổi **hai số** + chú thích *(đo: `git diff 4dfb7bd isp/FG -- tools` = +6 −2)* | **Orchestrator**: ghi vào việc gộp `CG1-R1-01` *"+3 của FG"* cạnh *"+33 của CG1"* — sàn gộp = S0 `2490` + 33 + 3 = **2526** *(web `664 → 667`)* | Mỗi bước nâng sàn **cùng commit** phải ghi **mức cộng** *(+N)* chứ ⛔ chỉ số tuyệt đối — để gộp nhiều nhánh cộng được | **CHẤP NHẬN** *(việc orchestrator — sàn gộp 2526 · web 667; R2 `KQ-119`)* |
| `FG-R2-01` | FG | R2 | B1 | **NÊN SỬA** | `tests/web/test_isp_f03_hd.py:299-301` *(`hd1[0]` chỉ khẳng `"5/23" in txt`)* · `fls/web/tep/man_f03.js:34-35` | **FG-F3 xanh cả khi thẻ HD1 ⛔ còn mang lý do.** `5/23` nằm ở `da_do` *(`man_f03.js:33`)*, ⛔ ở `ly_do` *(431 ký tự, 18 kỳ đỏ)*. Đột biến **N9** *(bản sao: bỏ cả khối `ly_do` khỏi `_the_cong`)* ⇒ thẻ HD1 còn **112** ký tự *(gốc **543**)*, `ly_do` ⛔ có trong thẻ ⇒ **`3 passed`**; **N11** *(`ly_do.slice(0,40)`)* ⇒ **`3 passed`**. Bài tên *"lý do 23 kỳ ⛔ tràn"* ⇒ xanh trên thẻ ⛔ có lý do 23 kỳ nào *(Đ3: tập đo rỗng)*; ISP §2 *Goal* đòi *"danh sách kỳ đỏ trong lý do"* mà **0** khẳng định nào kiểm nó *(grep `ly_do` trong `test_isp_f03_hd.py`: 1 hit — tên hàm)*. Nền hôm nay ĐÚNG *(thẻ mang đủ 431 ký tự — đo `ly_do_in_card=True`)* — chỉ là bài ⛔ giữ được | **Dev** *(1 dòng)*: trong `test_FG_F3` thêm `assert g_ly_do in hd1[0]["txt"]` với `ly_do` lấy từ `GET /gates` *(CHÍNH chuỗi tuyến, ⛔ hằng số)*; chứng minh ĐỎ bằng N9 + N11 *(phá → cắn → trả)* | Bài đo *"thứ X ⛔ tràn"* phải khẳng định **X có mặt** *(độ dài/nội dung)* trước khi đo tràn *(Đ3: mẫu số ⛔ rỗng)* | **ĐÃ SỬA** *(R3 `KQ-120`: `26fe9a5` — `ly_do in txt` ở F1 + F3, `len ≥ 50`; N9 ⇒ F1+F3 ĐỎ · N11 ⇒ F1+F3 ĐỎ · trả ⇒ `3 passed`)* |
| `FG-R2-02` | FG | R2 | B1 | GHI NHẬN | `fls/web/tep/man_f03.js:50` *(`chip('ok', data.dat …)`)* | Đột biến **N10** *(chip xanh in `data.khong_dat` thay `data.dat`)* ⇒ **`3 passed`**. AC FG-F1 chỉ đòi *"số ‘chưa đo được’ khớp tuyến"* *(đã canh — N8 `chua+1` ⇒ F1 ĐỎ)*; số **đạt**/**không đạt** trên dòng tóm ⛔ có bài. ⛔ phạm vi AC ⇒ ghi nhận | **Dev** *(nếu muốn, rẻ)*: F1 thêm `"%d đạt" % d["dat"] in ve["note"]` *(⛔ thêm bài — cùng bài)* | Dòng tóm ba số ⇒ canh **cả ba** *(Đ4: mỗi số một nhãn)* | **ĐÃ SỬA** *(R3 `KQ-120`: `26fe9a5` — F1 canh cả ba số; N10 ⇒ F1 ĐỎ · trả ⇒ `3 passed`; lưu ý ranh giới ở `FG-R3-01`)* |
| `FG-R3-01` | FG | R3 | B1 | GHI NHẬN | `tests/web/test_isp_f03_hd.py:195-196` *(`("%d đạt" % d["dat"]) in ve["note"]` · `"%d không đạt"`)* | **Khẳng định dòng tóm là phép chứa CHUỖI CON, ⛔ khớp nguyên số.** Nền tuyến trả `dat=1 · khong_dat=2` ⇒ `"1 đạt"` ⊂ `"11 đạt"`, `"2 không đạt"` ⊂ `"12 không đạt"`. Đột biến **N20** *(chip `đạt` in `data.dat + 10`)* ⇒ **`3 passed`**; **N21** *(`khong_dat + 10`)* ⇒ **`3 passed`** *(bản sao `git archive`, `/tmp/r3_fg/`)*. N10 *(R2 thấy sống)* **chết** vì `"2 đạt"` ⊄ `"1 đạt"` — ⛔ nghĩa là phép so đủ cho **mọi** số sai. Lỗi dạng *"thừa một chữ số đứng trước"* *(1→11)* lọt. Đột biến ⛔ thật *(contrived: cộng 10)*; ⛔ chặn | **Dev** *(nếu muốn, rẻ)*: khẳng định có ranh giới `re.search(r"(?<!\d)%d đạt" …)`; hoặc đọc từng chip riêng | Phép *"số N có trên màn"* bằng `in` ⇒ neo ranh giới chữ số *(Đ4: số có nhãn VÀ có biên)* | mở |
| `FG-R3-02` | FG | R3 | B1 | GHI NHẬN | `fls/web/tep/man_f03.js:42` *(`(data.cong \|\| []).forEach`)* · `tests/web/test_isp_f03_hd.py` | Đột biến **N15** *(`.slice(0,-1)` — rớt thẻ cổng CUỐI trong lưới)* ⇒ **SỐNG**: `3 passed` ở `test_isp_f03_hd.py` **và** các bài `tests/web` chứa `f03`/`gate`/`cong` *(50 bài `.`)*. Cổng cuối của `/gates` ⛔ phải `FINAL`/`HD1_THANG` *(bài FG chỉ tìm hai thẻ ấy theo tên)* ⇒ **ngoài phạm vi FG** *(ISP Step 9 mục 3: "hai thẻ mới")*; ⛔ bài nào đếm số thẻ = số cổng tuyến trả | **Orchestrator/Dev** *(backlog)*: một khẳng định `len(cards) == len(data.cong)` ở F1 *(1 dòng)* nếu muốn lưới ⛔ rớt thẻ im lặng; ⛔ chặn FG | Bài kiểm lưới thẻ ⇒ canh **số thẻ = số cổng tuyến trả**, ⛔ chỉ hai thẻ tên | mở *(backlog — ⛔ chặn gộp)* |

## Cổng R1 tự chạy *(so với `BG-117`)*
| Lệnh | `BG-117` nói | R1 đo *(cụm 5446)* | Khớp |
|---|---|---|:-:|
| `pytest tests/web/test_isp_f03_hd.py` | exit 0 · `3 passed` | `3 passed in 2.57s` · `-rs`: 0 skip | ✅ |
| `--duong-nen --cong 5446` *(script NHÁNH · GOC = `isp-fg`)* | `KẾT: ĐẠT` · `26 = 26` · 2603 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `12 failed, 2575 passed, 2 xfailed, 14 errors in 342s` · `26 = 26 (thêm 0 · bớt 0) · chạy 2603 (mong ≥ 2496) · skipped 0` · web `3 failed, 664 passed` · `3 = 3 · chạy 667 (mong ≥ 667) · skipped 0` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | *(BG ⛔ ghi)* | K1–K6 `OK` · `187 file · 1940 bảng · 734 ô ngày · 104 mã QĐ` | ✅ |
| `git diff 4dfb7bd HEAD -- fls` | rỗng | **0 dòng** | ✅ |

## Đột biến *(bản sao `git archive isp/FG`, 9 chỗ; mọi `.orig` đã dọn — `BANG_TEP` cắn tệp lạ)*
| Mã | Phá | Bài đỏ | Kết |
|---|---|---|:-:|
| M1 | `_muc(true)` → lớp `fail` | F1 | giết |
| M2 | `_muc(null)` → lớp `pass unk` *(cổng chưa đo vẫn xanh)* | F2 | giết |
| M3 | `.gate{white-space:nowrap}` | F3 | giết |
| M4 | `.gate{min-width:520px}` *(thẻ rộng hơn màn, ⛔ tự cuộn)* | — | **SỐNG** → `FG-R1-01` |
| M5 | chip `chưa đo được` in `chua+1` | F1 | giết |
| M6 | bỏ `da_do` khỏi thẻ | F1 + F3 | giết |
| M7 | thẻ `HD1_THANG` in chữ `✓ ĐẠT` | F1 + F2 | giết |
| M8 | `_muc(false)` → lớp `pass` | F1 | giết |
| M9 | `ly_do` đổi dấu cách thành NBSP *(chuỗi không ngắt)* | F3 *(`sw 566 > cw 318`)* | giết |

**8/9 giết · 1 sống** *(M4 → `FG-R1-01`)*.

## Cổng R3 tự chạy *(cụm PG 5436 · `isp/FG` @ `a5e876e`)*
| Lệnh | Mong | R3 đo | Khớp |
|---|---|---|:-:|
| `pytest tests/web/test_isp_f03_hd.py` | `3 passed` | `3 passed in 3.43s` | ✅ |
| `pytest tests/web` | `3 failed` *(đường nền)* | `3 failed, 664 passed in 178s` — 3 bài đỏ = bài đỏ CÓ SẴN *(sổ thật 0 giá trị tiền — kho rỗng)* | ✅ |
| `--duong-nen --cong 5436` *(script NHÁNH · GOC = `isp-fg`)* | `KẾT: ĐẠT` | `KẾT: ĐẠT` · toàn bộ `12 failed, 2575 passed, 2 xfailed, 14 errors` ⇒ `26 = 26 (thêm 0 · bớt 0) · chạy 2603` · web `3 = 3 · chạy 667` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `kiem_tai_lieu.py` | K1–K6 OK | K1–K6 `OK` · `190 file · 1963 bảng · 737 ô ngày · 104 mã QĐ` | ✅ |
| `git diff c037297 isp/FG -- fls` | 0 dòng | **0 dòng** *(đổi: 2 tệp — `BG-117` +46, `test_isp_f03_hd.py` +30 −2)* | ✅ |

## Đột biến R3 *(bản sao `git archive isp/FG` @ `a5e876e`, `/tmp/r3_fg/cp_N*`; trả nguyên ⇒ `3 passed`)*
| Mã | Phá | Bài đỏ | Kết |
|---|---|---|:-:|
| N9 | bỏ khối `ly_do` khỏi `_the_cong` *(R2 sống)* | F1 + F3 | giết |
| N10 | chip `đạt` in `data.khong_dat` *(R2 sống)* | F1 | giết |
| N11 | `ly_do.slice(0,40)` *(R2 sống)* | F1 + F3 | giết |
| N12 | bỏ `da_do` | F1 + F3 | giết |
| N13 | `_muc(false)` ⇒ lớp `pass` | F1 | giết |
| N14 | `_muc(null)` ⇒ `✓ ĐẠT` lớp `pass` | F2 | giết |
| N15 | lưới rớt thẻ cổng cuối | — | **SỐNG** → `FG-R3-02` |
| N16 | chip `chưa đo được` in `chua+1` | F1 | giết |
| N17 | chip `không đạt` in `data.dat` | F1 | giết |
| N18 | tiêu đề thẻ in `c.ma` thay `c.ten` | F1 + F2 + F3 | giết |
| N19 | `ly_do` đảo thứ tự kỳ | F1 + F3 | giết |
| N20 | chip `đạt` in `dat+10` *(`11 đạt` ⊃ `1 đạt`)* | — | **SỐNG** → `FG-R3-01` |
| N21 | chip `không đạt` in `khong_dat+10` | — | **SỐNG** → `FG-R3-01` |
| N22 | `ly_do` thêm đuôi ` ⛔` *(chuỗi ⊃ ly_do)* | — | SỐNG *(đúng thiết kế — phép chứa; ⛔ lỗi)* |

**N9/N10/N11 *(ba cái R2 thấy sống)* — cả ba GIẾT.** 8/11 mới giết · 3 sống *(2 phát hiện GHI NHẬN, 1 đúng thiết kế)*.

## Changelog
- **v0.1** *(2026-11-17, `fls-test` R1 của `FG`, `KQ-118`)*: khởi tạo — 4 phát hiện `FG-R1-01…04` *(**0 CHẶN** · 1 NÊN SỬA · 3 GHI NHẬN)*.
- **v0.2** *(2026-11-17, `fls-test` R2 của `FG`, `KQ-119`)*: đổi Trạng thái `FG-R1-01…04` *(2 ĐÃ SỬA · 2 CHẤP NHẬN)*; thêm `FG-R2-01` *(NÊN SỬA — F3 xanh khi `ly_do` vắng, N9/N11 sống)* · `FG-R2-02` *(GHI NHẬN — chip `đạt` ⛔ có bài, N10)*; 11 đột biến mới N1–N11 *(8 giết · 3 sống)*.
- **v0.3** *(2026-11-17, `fls-test` R3 của `FG`, `KQ-120`)*: đổi Trạng thái `FG-R2-01`/`02` *(ĐÃ SỬA)*; thêm `FG-R3-01` *(GHI NHẬN — chip dòng tóm là phép chứa chuỗi con; N20/N21)* · `FG-R3-02` *(GHI NHẬN — lưới rớt thẻ cuối; N15, ngoài phạm vi)*; 12 đột biến N12–N22 *(+N9–N11 dựng lại)*.
