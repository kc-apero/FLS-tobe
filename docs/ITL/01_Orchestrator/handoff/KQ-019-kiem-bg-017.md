# KQ-019 — biên bản kiểm `BG-017`

| | |
|---|---|
| **Thuộc** | [`BG-017`](BG-017-ban-giao-wo-008.md) · [`WO-008`](WO-008-chu-man-sau-bo-ghep.md) *(đã đính chính theo [`TL-016`](HOI-016-nhat-ky-value-source-la-nguon-truoc-khi-go.md))* |
| **Kiểm bởi** | `fls-test` · 2026-10-02 chiều |
| **Phán quyết** | ⛔ **`TRƯỢT`** — **6/6 AC ĐẠT**, nhưng lăng kính **Màn hình** còn **2 `NANG`** *(`F-1`, `F-2`)* nằm trên **chính** hàm `man_f01_ghep.js::bo_gan` mà Phạm vi `(c)` sửa. Cả hai **có từ trước** *(⛔ do diff `69f03f6` gây ra)* — nhưng luật `10` §3.4 + `CLAUDE.md`: `ĐẠT` chỉ khi ⛔ còn `CHAN`/`NANG`. Chọn sửa trong `WO-008` vòng 2 hay tách phiếu mới là việc của `fls-ba` |

## Cổng vào
| Kiểm | Đo | |
|---|---|---|
| git thật | `HEAD` = `origin/feat/p2-oracle-parity` = `66cda8e` *(`git rev-parse` cả hai)*; `948ffb6` · `69f03f6` · `4b7ebb8` · `66cda8e` đều nằm trên `origin` *(`git branch -r --contains`)*; `git diff 69f03f6 66cda8e -- fls tests tools` **rỗng** ⇒ mã kiểm = mã `BG` | ✅ |
| version spec | `06_SCREEN_SPEC.md:3` **v4.9** · `10_DECISION_TABLE.md:3` **v0.8** · `05_DATA_DICTIONARY_ERD.md:3` **v0.34** — đúng `WO-008` sau `TL-016` | ✅ |
| máy 8088 | phục vụ `man_f02.js` · `man_f01.js` · `man_f01_ghep.js` **trùng `sha256`** với cây `66cda8e` *(3/3)*; `man_f02.js` phục vụ mang `rút gợi ý` **2** chỗ | ✅ |

## Cổng chạy lại *(Test tự chạy, `PG_DSN=…/fls`, tuần tự)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `python -m pytest` | `2095 passed` | `2095 passed in 280.30s` *(trước khi thêm bài `kq019`)* · sau khi thêm: **`+3 passed, +5 xfailed`** trong tệp `kq019` | ✅ |
| `python tools/kiem_so_song.py` | **20** lệch loại (c) | **33** lệch = **20** loại (c) của phiếu *(2084→2095 **×6** · 1782→1793 ×2 · 25.133→25.213 **×5** · web 8.547→8.627 ×2 · bài 448→459 ×2 · hash ×2 · số tệp 105→**108** ×1)* + **13** loại (b) nhịp chụp sau 10:09 *(ảnh 256.928→260.748 ×4 · dấu `10:09→12:09` ×3 · ảnh 68→69 ×2 · ảnh nhịp 135/147→137/149 ×4)*. ⭐ Chạy lại trên **bản sao cây `948ffb6`** *(`T0`)*: **13** lệch — **đúng 13 cái loại (b)**, **0** loại (c) ⇒ nền `T0` = 0 loại (c) **đúng** | ✅ *(⚠ `F-5`: bảng tách trong `BG` cộng ra 18, ⛔ 20)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | ĐẠT · 107 file | `✅ cong tai lieu DAT — … (108 file, 1274 bang, 650 o ngay, 104 ma QD)` *(+1 = `WO-018` của `fls-ba`)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | 17/20 · C1 ĐẠT | `17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT` | ✅ |
| `python tools/soi_bang_tuyen.py` | 40/40 | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | 31/31 | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ✅ |
| `.venv/Scripts/lint-imports.exe` | 9 kept 0 broken | `Contracts: 9 kept, 0 broken.` | ✅ |
| `python -m fls.db.pg_migrate` | ⛔ chưa chạy *(⛔ chạm schema)* | ⛔ chạy — `git diff d761d0f 66cda8e -- fls/db` **rỗng** | — |

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** | 4 loại dòng ⇒ thành `gợi ý: X` · `rút gợi ý` · `X` · trống; nguồn nhãn máy ×2 · `người sửa` ×2 | Bài Dev xanh *(trong 2095)* + đột biến `M1`/`M2` của `KQ-019` *(bản sao cây)* làm bài **sổ thật** của `KQ-019` đỏ. ⭐ **Sổ thật** *(8088, chỉ đọc, Chrome)*: `itl_id 25041` ⇒ 2/2 hàng `gợi ý: SHQ2 \| Headquarters2` / `gợi ý: OGA \| GAC - Other` · nguồn `máy gợi ý · không đổi Final`; `27728` *(UAT)* ⇒ 4/4 nguồn `người sửa`, 2 có giá trị + 2 trống *(nhánh 8 — spec chấp nhận)*. ⭐ **Toàn bộ nhật ký sổ thật** qua **hàm đọc thật** `doc_nhat_ky` vào **màn thật**: mọi dạng `(value_source, value_after)` in đúng luật; hàng `gợi ý:` = **4.424** = số dòng `may_goi_y` có giá trị *(mẫu số 4.424 / **4.428**)* | ✅ ĐẠT |
| **AC-2** | Dòng B qua cửa thật: mọi bản đảo máy in `rút gợi ý`, 0 ô thành trống; hàng người in giá trị người | Máy **8099** *(kho TEST, `--cho-ghi`)*, dòng **B1** *(ghép tay → lớp A → người gõ `hd` → lớp B → **bấm thật** `Bỏ ghép` F01)* ⇒ nhật ký **11** hàng: `rút gợi ý` **5** = **5** bản đảo trong thân trả *(mẫu số 5)*; hàng `may_goi_y` ô thành trống **0**; hàng người `HD-NGUOI-B1` · nguồn `UNMAPPED` *(đã biết — `WO-018`, `TL-016`: ⛔ nâng `F`)* | ✅ ĐẠT |
| **AC-3** | `[cdt1,hd,hd,cdt1]` ⇒ `2 ô` · `4 bút toán`, mỗi tên 1 lần; một lớp ⇒ ⛔ đuôi | Thân **thật** 8099 *(B1, B2, E: `but_toan_dao` = `[cdt1,hd,cdt1,hd,cdt1]`)* ⇒ hộp **thật**: *"↩ Đã rút gợi ý máy trên 2 ô (cdt1, hd) · 5 bút toán, gồm lớp gợi ý cũ bị đè"* — `cdt1` **1**, `hd` **1** lần. Ca **C** *(⛔ người, 3 lớp)* `but_toan_dao` 6 ⇒ ⛔ hộp trên màn ghép *(đúng AC-4)*. Một lớp: bài Dev `::…MOT_lop…` xanh; đột biến `M4` ⇒ bài `kq019` đỏ | ✅ ĐẠT |
| **AC-4** | Màn ghép, 1 lệnh–1 dòng tiền: `bo_qua` có ⇒ **1** hộp, chứa `hd` + giá trị người, nút duy nhất `Đã hiểu`; `bo_qua=[]` ⇒ **0** hộp | 8099, **nút thật** `Bỏ gán`: **B2** ⇒ `REQ /queue/3680/unmatch {}` · `RES 200` · bẫy đếm `HT.mo` *(gọi hàm thật, chỉ ghi lại)* **1** lần · tiêu đề `Đã bỏ ghép` · nút `["Đã hiểu"]` · *"hd = HD-NGUOI-B2"*. **C** *(`bo_qua=[]`)* ⇒ `RES 200` · `HT.mo` **0** lần · `#scrim` ⛔ dựng. Mẫu số: `/unmatch` **1** lượt mỗi ca *(`Đ3`)*. Bài `kq019` với `hop_thoai.js` **thật** *(bài Dev thay `HT.mo` bằng bẫy)*: xanh; `M3`/`M5`/`M6` ⇒ đỏ | ✅ ĐẠT *(phạm vi AC: ca ⛔ chùm)* — ⚠ ca chùm xem `F-1` |
| **AC-5** | pytest 0 đỏ · lint 9/0 · `soi_bang_tuyen` · `kiem_thuyet_minh` · luật ký hiệu | bảng cổng trên — khớp `BG`; `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` trong 2095 xanh | ✅ ĐẠT |
| **AC-6** | `BG` tách nền `T0` (0) ⟷ đỏ mới loại (c); ⛔ `--ghi` lần hai | `BG` tách đúng **tổng** 20, nền `T0` đo lại = 0 loại (c); `--ghi` ⛔ chạy *(`git log 69f03f6..66cda8e` ⛔ commit `dong_bo`)*. ⚠ bảng tách cộng 18 — `F-5` | ✅ ĐẠT |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(`BA-06` v4.9 · `BA-10` v0.8 `DT-I14` · `BA-05` v0.34 `ⓓe`)* | ✅ **ĐẠT** cho phần diff — 3 tệp màn làm đúng ba chỗ chữ; ⚠ đường `bo_gan` có 3 nhánh ⛔ đúng spec **từ trước** *(`F-1` · `F-3` · `F-4`)* | Đọc `git diff d761d0f 69f03f6 -- fls/`: `_nk_thanh` *(chỉ `may_goi_y` đổi chữ; rỗng = `null`/`undefined`/`''`)* · `_nk_nguon` *(`hasOwnProperty` — mã lạ in nguyên)* · `_o_duy_nhat` *(thứ tự xuất hiện đầu)* · khối `bo_qua` thêm `= giá trị` · `bo_gan` đọc thân rồi gọi **chính** `F01._bao_bo_ghep` *(⛔ bản câu thứ hai — `grep "Đã rút gợi ý" fls/web/tep` = **1** chỗ)*. ⛔ Đổi cửa, ⛔ đổi sổ, ⛔ migration. ⭐ **Phát hiện khi đọc**: `man_f01_ghep.js:582` và `:593` gọi `HT.hoi(...)` — `hop_thoai.js` trả `{ mo, dong, loi_trong_hop }`, **⛔ có `hoi`** *(`grep -rn "hoi\s*[:=]\|function hoi" fls/web/tep` = **0**; có từ `45a79e0`/`a09e5a1`)* ⇒ `F-1`. Bài Dev `BAY_HOP` **tự định nghĩa** `HT.hoi` ⇒ che đúng chỗ thiếu *(`11` §6)*. `INV-*` chạm: ⛔ — phiếu chỉ đổi chữ |
| **Dữ liệu** *(kho thật, chỉ `SELECT`)* | ✅ **ĐẠT** — sổ ⛔ đổi so với `KQ-014`; chữ mới chạm đúng số `WO` khai | `fls_itl` **8.387** · `fls_pm_link` **2.263** · `fls_pm_unlink` **1** · `fls_may_goi_y` **4.424** · `fls_sua_tay` **0** · `fls_adjustment` **4.428** · `fls_journal` **4.428** · `fls_queue_event` **110.349** — **8/8** khớp `KQ-014`; `max(evt_id)` **163567** · `max(adj_id)` **163571** · `max(link_id)` **163562** — ⛔ dòng mới, **cả sau** khi máy 8099 chạy *(actor `fls-test@apero.vn` trên kho thật: **0**)*. `fls_journal` theo `value_source`: `may_goi_y` có giá trị **4.424** · rỗng **0** · `sua_tay` có giá trị **2** · rỗng **2** ⇒ chữ `rút gợi ý` trên sổ thật **0** hàng, `gợi ý: X` **4.424**, hộp `(c)` bật **0** lần *(`fls_sua_tay` 0)*. `*_thyt` ≠ NULL: **0 / 8.387** ⇒ ca xấu `HOI-016 ⓑ` *(gợi ý `*_thyt` rồi người gõ)* hôm nay ⛔ xảy ra — thuộc `WO-018`. Tầm `F-1`: lệnh đã gán đi nhánh `HT.hoi` *(chùm ∪ lệnh gắn ≥ 2 giao dịch)* **88 / 2.219** *(4,0%)* — chùm **25 / 2.222** dòng tiền, lệnh ≥ 2 dòng tiền **23** |
| **Màn hình** *(8088 chỉ đọc + 8099 kho TEST; Chrome headless CDP 1440×900)* | ⛔ **TRƯỢT** — phần `WO-008` vẽ đúng; nhưng **2 `NANG`** + **2 `NHE`** trên đường `Bỏ gán` của màn ghép | **8088** `F02` ⑦: `25041` · `27728` như AC-1; nguồn là cột thứ 6 — ở 1440px drawer phải **cuộn ngang** mới thấy *(có từ trước; ô thành đã tự nói "gợi ý:")*. **5 trạng thái** hồi quy `man-f02` + `man-ghep`: **tải** *(khung xương · "Đang hỏi sổ…")* · **rỗng** *("✓ Sổ ITL trống…" · "0 dòng")* · **lỗi** *(`FLS-INTERNAL · HTTP 500` · "⛔ Cửa lỗi: Máy gặp lỗi bên trong.")* · **mất kết nối** *(`FLS-MAT-KET-NOI` · "⛔ Cửa lỗi: Không nối được tới máy chủ FLS.")* · **có dữ liệu** — thanh giả lập ở cả 4; `body` **13,5px**; rộng trang ≤ cửa sổ *(1.424/1.424 · 1.409/1.424)*; lỗi console **0/10**. **8099** *(`chay_cua.py --cho-web --cho-ghi --cong 8099`, `PG_DSN=…/fls_test`, đã tắt — `Get-NetTCPConnection 8099` = **0**)*, 5 dòng dựng bằng cửa ghi thật: **B1** F01 `Bỏ ghép` → hộp lý do `["Thôi","Bỏ cả chùm"]` → hộp **"Đã bỏ ghép"** *(chụp `kq019_f01_3663.png`)*: *"Đã bỏ 1 mối nối… ↩ Đã rút gợi ý máy trên 2 ô (cdt1, hd) · 5 bút toán, gồm lớp gợi ý cũ bị đè · ⚠ ⛔ KHÔNG đảo 1 ô — người đã gõ tay…: hd = HD-NGUOI-B1"*, **một** nút `Đã hiểu`, chữ 13px, hộp 520×297. **B2** màn ghép ⇒ cùng hộp, **1** lần. **C** ⇒ **0** hộp. ⛔ **D** *(chùm 2 lệnh)* ⇒ `GET /chum` 200 rồi `Uncaught (in promise) TypeError: HT.hoi is not a function` — **0** hộp, `/unmatch` **0** lượt, mối nối còn **2** ⇒ `F-1`. ⛔ Sau **B2**/**C**/**E** bỏ gán **200**: thẻ lệnh vẫn `Đã gán`, khối *"✓ Đang gán với giao dịch … bỏ gán"* còn nguyên *(chụp `kq019_ghep_C_1.png`)*; bấm lại ⇒ `RES 409`, `Uncaught LoiCua` — màn ⛔ nói gì ⇒ `F-2`. **E** cắt mạng đúng lượt `/unmatch` *(`Fetch.failRequest`)* ⇒ `Uncaught (in promise) LoiCua: Không nối được tới máy chủ FLS.` — 0 hộp, 0 chữ ⇒ `F-3`. ⚠ Hộp chùm "hỏi rồi báo" *(`BG` yếu #6)* **⛔ nhìn được** — câu hỏi ⛔ bao giờ mở |

## Soi 7 chỗ Dev tự thấy còn yếu
| # | Dev nói | Test đo | Kết luận |
|---|---|---|---|
| 1 | `value_source` của `/adjust` = nguồn trước khi gõ | Kho TEST: hàng người `HD-NGUOI-B1` nguồn `UNMAPPED`; sổ thật `*_thyt` ≠ NULL **0/8.387** | đã biết — `WO-018` *(`TL-016`)*, ⛔ `F` |
| 2 | Nhãn chữ trơn khác spec | `BA-06` v4.9 đã đính chính đúng chữ máy in | ✅ hết lệch |
| 3 | Khối `bo_qua` in giá trị | `BA-06` v4.9 nhận; 8099 in `hd = HD-NGUOI-B2` | ✅ |
| 4 | Câu "rút gợi ý máy" cả khi có bản đảo nhánh 8 | sổ thật `sua_tay` gắn `match` chưa đảo **0** — tập đóng | ✅ chấp nhận *(spec)* |
| 5 | `mo_lenh` ném ⇒ hộp `bo_qua` ⛔ mở | Bài `kq019::test_F4_*` *(cửa ứng viên 500 sau bỏ gán 200)* ⇒ hộp **⛔ mở**, lỗi chỉ ra người gọi | ⛔ **thật** — `F-4` `NHE` |
| 6 | Chùm: hai hộp liền nhau chưa ai nhìn | 8099 dòng **D**: **0** hộp — `HT.hoi` ⛔ tồn tại | ⛔ câu *"đi cùng đường … đúng spec"* **sai** — `F-1` `NANG` |
| 7 | `_Bang` cắt từ "⑦ Nhật ký" | ⑦ vẫn là khối cuối *(8088: khối `.grp` có tiêu đề "Nhật ký" là khối cuối của `#so-panel`)* | ✅ hôm nay |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** | `NANG` | `fls/web/tep/man_f01_ghep.js:582`, `:593` gọi `HT.hoi` · `fls/web/tep/hop_thoai.js` *(trả `{ mo, dong, loi_trong_hop }`)* | Màn ghép, lệnh thuộc **chùm** *(`/chum` `can_hoi=true`)* hoặc gắn **≥ 2** giao dịch ⇒ bấm `Bỏ gán` ⇒ `TypeError: HT.hoi is not a function` *(Chrome 8099, dòng D)* — **0** hộp, **0** lượt `/unmatch`, màn ⛔ nói gì. Sổ thật: **88 / 2.219** lệnh đã gán *(4,0%)* đi nhánh này. Có từ `45a79e0`/`a09e5a1`; mọi bài màn đều tự định nghĩa `HT.hoi` ⇒ ⛔ bài nào thấy. ⚠ `BG-017` yếu #6 khẳng định *"đi cùng đường"* — sai | `DEV` *(thêm `HT.hoi` hay đổi chỗ gọi)* · `BA` *(xếp vào `WO-008` vòng 2 hay phiếu mới)* |
| **F-2** | `NANG` | `fls/web/tep/man_f01_ghep.js::bo_gan` *(`:610`–`:613`)* — sau `/unmatch` chỉ `mo_lenh`, ⛔ làm mới `ST.dong` *(`gd_ds`, `itl_da_gan`, `trang_thai`)* | 8099 dòng C/B2/E: `/unmatch` **200** ⇒ màn vẫn `Đã gán` + *"✓ Đang gán với giao dịch … bỏ gán"*; bấm lại ⇒ `409` im lặng *(console: "Giá trị bạn gõ khác với giá trị nguồn đang có." — câu sai nghĩa)*. Với `bo_qua` rỗng *(hôm nay **100%** cú bỏ gán — `fls_sua_tay` 0)* ⇒ người bấm **⛔ một tín hiệu nào** rằng bỏ gán đã xảy ra. Có từ trước `WO-008`; lý lẽ *"⛔ hộp khi `bo_qua` rỗng"* *(`BA-06` mục ⓔ v4.8)* ngầm giả định màn tự nói | `DEV` · `BA` *(câu "về lệnh như hôm nay" cần khai màn phải hiện gì sau bỏ gán)* |
| **F-3** | `NHE` | `bo_gan` ⛔ bắt lỗi `FLS.ghi` ⇒ lỗi rơi ra trình nghe `click` *(`nut()` ⛔ bọc)* · `WO-008` mục **Màn hình** dòng *lỗi* / *mất kết nối* ghi *"như nay (⛔ Cửa lỗi: …)"* | 8099 dòng E, cắt mạng lượt `/unmatch` ⇒ `Uncaught (in promise) LoiCua` — màn ⛔ hiện chữ nào. Phần AC *(⛔ hộp "Đã bỏ ghép")* đúng; phần "như nay" mô tả một câu lỗi **⛔ có** trên màn ghép | `DEV` · `BA` *(sửa câu "như nay")* |
| **F-4** | `NHE` | `bo_gan` `:611`–`:613` — `await mo_lenh` **trước** khi mở hộp | Bỏ gán **200** với `bo_qua` có giá trị người, rồi `itl-candidates` lỗi ⇒ hộp `bo_qua` **⛔ mở** *(bài `kq019::test_F4_*`)*. `BA-06`: `bo_qua` *"phải hiện"*. `BG` yếu #5 — đúng | `DEV` |
| **F-5** | `NHE` | `BG-017` bảng cổng dòng `kiem_so_song` | Bảng tách ghi `2084→2095 ×5` · `25.133→25.213 ×4` ⇒ cộng **18**, tổng ghi **20**; máy đo `×6` · `×5` ⇒ **20**. Tổng đúng, tách sai | `DEV` *(ghi nhận)* |

⚠ ⛔ **Không** nâng thành `F`: hàng người gõ in nguồn `UNMAPPED` trên kho TEST *(`TL-016` — `WO-018`)*; nhánh 8 in trống + `người sửa` *(spec v4.8/4.9 chấp nhận; sổ thật = 4 dòng UAT `27728`)*.

## Bài thử mới *(`tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py` — 3 xanh · 5 `xfail(strict)`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `::test_bo_gan_bo_qua_CO__HOP_THAT_mot_tieu_de_mot_nut_noi_theo_o` *(`hop_thoai.js` **thật**)* | bản sao cây `66cda8e`, mỗi mẫu khớp **đúng 1**: `M3` bỏ đọc thân · `M4` câu đảo về `dao.map(...)` · `M6` bỏ giá trị người ⇒ **ĐỎ** | ✅ |
| `::test_bo_gan_bo_qua_RONG__HOP_THAT_khong_mo` | `M5` mở hộp cả khi rỗng ⇒ **ĐỎ** | ✅ |
| `::test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong` *(kho thật `noi_chi_doc` + `doc_nhat_ky` thật; đo **quan hệ**, ⛔ hằng số; mẫu số 4.424)* | `M1` ô thành về `TP.chu(value_after)` · `M2` nguồn in mã thô ⇒ **ĐỎ** | ✅ |
| `::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[chum\|da_giao_dich]` | **ĐỎ trên mã hôm nay** *(`HT.hoi is not a function`)* ⇒ `xfail(strict)`; bản sửa mô phỏng `X1` *(thêm `HT.hoi`)* ⇒ **XPASS** ⇒ strict đỏ | ⏳ `F-1` |
| `::test_F2_sau_bo_gan_THANH_CONG__man_khong_con_noi_DANG_GAN` | **ĐỎ hôm nay**; mẫu số: khối *"Đang gán"* có mặt **trước** cú bấm; `X2` *(làm mới lệnh)* ⇒ XPASS | ⏳ `F-2` |
| `::test_F3_bo_gan_cua_LOI__nguoi_THAY_loi` | **ĐỎ hôm nay**; `X3` *(bắt lỗi, mở hộp lỗi)* ⇒ XPASS | ⏳ `F-3` |
| `::test_F4_ve_lai_lenh_LOI_sau_bo_gan__hop_bo_qua_VAN_mo` | **ĐỎ hôm nay**; `X4` *(hộp trước khi vẽ lại)* ⇒ XPASS | ⏳ `F-4` |

⭐ Đột biến *(`scratchpad/kq019_dot_bien.py`, worktree tạm, `sha256` trả nguyên **10/10**, ⛔ chạm cây thật)*: **6/6** `M` bị bắt · **4/4** `X` lật `xfail` ⇒ bài ⛔ phải `xfail` vĩnh viễn.

## Đóng phần màn của `KQ-007`
- `KQ-007 F-1` *(nhật ký "X → trống")* · `F-2` *(tên ô lặp)*: ✅ **vá** `69f03f6` — đo thật 8088 + 8099 ở trên.
- `KQ-007 F-3` *(màn ghép nuốt `bo_qua`)*: ✅ **vá** cho lệnh một dòng tiền *(B2: 1 hộp)*; nhánh chùm/đa giao dịch **⛔ tới được** cú bỏ gán — chuyển sang `KQ-019 F-1`.

## Ghi chú vận hành
- Sau khi thêm bài `kq019` + phiếu này: `pytest` **`2098 passed, 5 xfailed in 290.70s`**; `kiem_tai_lieu` ĐẠT *(**109** file)*. Số phép thử / số tệp vì thế trôi thêm *(loại (c) của `KQ-019`)* — `fls-test` ⛔ chạy `dong_bo_so_song --ghi` *(việc của `fls-dev`, `10` §6)*.
- Kho TEST bị `tests/conftest.py` **dựng lại** ở đầu mỗi phiên `pytest` *(`dung_lai_kho_test`, `GAP-KHO-02`)* ⇒ 5 dòng `NAP-2000-01-01-Q469CC5` dùng trên 8099 **đã mất** sau lượt chạy bài `kq019`; bằng chứng giữ ở thân trả + ảnh chụp ghi trong lượt *(`scratchpad/man/kq019_*.json|png` — ⛔ lên git)*.
