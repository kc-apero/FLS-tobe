# BG-028 — bàn giao `WO-022` **vòng 2** *(ô tiền theo ngân sách ký tự · một luật số lẻ · dung sai in = dung sai so)*

| | |
|---|---|
| **Thuộc** | [`WO-022`](WO-022-in-tien-theo-tien-te.md) — ⭐ **vòng 2 của `WO-022`** *(`AC-10`…`AC-15`; vòng 1 = [`BG-027`](BG-027-ban-giao-wo-022.md) @ `7746e48`, giữ làm bằng chứng `AC-1`…`AC-9` — `fls-test` **kiểm gộp**)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`3173d7f`** *(đã đẩy — mã + bài + tài liệu Dev)*; tờ này + `WO`→`CHO_TEST` + README + dashboard ở commit giấy ngay sau |
| **Spec** | `BA-06` **v4.13** §5b ⓒ *(viết lại)* · ⓕ *(câu dung sai)* · ⓘ *(mới)* — header tệp `v4.13` ✔ ở cổng vào · `HOI-026` `TL-026` *(số đo)* |
| **Cổng vào** | git `a7fd01f` = `origin/feat/p2-oracle-parity` ✔ · `BA-06` v4.13 ✔ · nền `kiem_so_song` đầu vòng 2 *(trên `a7fd01f`, trước mã)*: **44** |
| **Câu treo** | `Q-TIEN-1` *(owner)* vẫn treo ⇒ mặc định **"in đủ"** giữ. Sau vòng 2, đổi theo owner *"làm tròn VND"* = sửa nhánh `that <= bang ? bang : LE_KHO` cho riêng mã **trong** bảng *(mã lạ vẫn `LE_KHO`)* + một ca `AC-1` + hai ca `AC-13` |
| **HOI mở kèm** | **không** |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/hinh.css` | ⓔ `.mcols` vệt 6 *(`Số tiền`)* `108px → 136px` · vệt 11 *(`Số tiền GD`)* `116px → 136px` *(§5b ⓘ: `ceil(18 × 0,6 × 12.5) = 135` ⇒ `136`)*; chú thích `.mcols` ghi vì sao 136 + số đo `HOI-026`/`TL-026`. Lưới an toàn: `.mtable .mcell.r{white-space:nowrap;text-overflow:ellipsis}` — **lớp ô đã có** *(chỉ hai ô tiền của bảng dùng `oc('r', …)`; bài canh đúng **2** chỗ)*, ⛔ lớp mới, ⛔ token mới |
| `fls/web/tep/man_f01_ghep.js` | `ve_bang`: hai ô tiền mang `title` = **đúng** chuỗi in *(`TP.tien(v, curr) + ' ' + curr`)*; ô `Số tiền GD` rỗng *(`—`)* ⛔ mang `title` |
| `fls/web/tep/thanh_phan.js` | ⓕ `TP.tien`: mã lạ / thiếu ⇒ bảng số lẻ coi là **0** *(⛔ nhánh riêng)*: `n = that <= bang ? bang : LE_KHO` cho **mọi** mã ⇒ `("100.50","20")→"100,50"` *(vòng 1 `100,5`)*. Chú thích ⓒ ghi lý do *(hai nhánh bất đối xứng — yếu #1 `BG-027`)* + tầm sổ **0** dòng. `TP.xu` ⛔ đổi |
| `fls/web/tep/man_f01.js` | ⓖ hộp *Ghép lệnh* `_drawer_ghep`: in dung sai = `TP.tien(TP.chuoi_xu(ds_xu), cur)` *(`ds_xu = TP.xu(ds, 'san')` — **chính** số `_tinh` đem so)*; `ds_xu` ⛔ đổi được ⇒ in chuỗi cửa trả *(`TP.tien` in nguyên văn đã thoát)* và hộp đã ⛔ cho ghép *(`hong`)* |
| `fls/web/tep/man_f01_lenh.js` | ⓖ hộp *Tìm tiền* — dòng *"dung sai Σ cho tiền tệ này"*: cùng phép sàn; ⛔ đổi được ⇒ chuỗi cửa trả |
| `tests/web/test_wo022_v2_o_tien_va_mot_luat_so_le.py` | **11** bài: `AC-10` ×3 *(cổng đọc `hinh.css` + `tokens.css` + `COT_BANG`; bài chứng minh cổng cắn **trên nguồn thật đã phá trong bộ nhớ**: `108px` · `--fs-than:13px` · chèn cột thiếu vệt · vệt co giãn; tách vệt ⛔ vỡ `minmax(…, …)`)* · `AC-12` ×2 *(luật CSS lưới an toàn + DOM `title` hai ô)* · `AC-13` ×2 *(6 ca từng byte + **quan hệ**: mã lạ / `null` / `undefined` / `''` / `' xyz '` in **y hệt** VND trên 16 giá trị)* · `AC-14` ×4 *(hộp `F01` `617.285` ⇒ `617,28`, lệch `617,29` crit / `617,28` khớp · `F01` `1000` ⇒ `1.000` · hộp `F01L` `617,28` + `1.000` · quét: tập tệp đọc `dung_sai` = đúng danh sách có bài hành vi)* |
| `tests/web/test_wo022_v2_o_tien_pg.py` | **1** bài `AC-11` *(sổ thật, `noi_chi_doc`, chỉ `SELECT`)* |
| `tests/web/test_wo022_tien_theo_tien_te.py` | ⭐ **ca thứ 10 của `AC-1` đổi** `("100.50","20")`: ~~`"100,5"`~~ ⇒ **`"100,50"`** — theo `AC-13` *(spec đổi: `BA-06` v4.13 ⓒ viết lại)*, ⛔ "sửa bài cho xanh": **lo gốc** của ca giữ nguyên *(mã lạ ⛔ bị đoán là VND ⇒ `101`/`100`)*, ghi chú tại ca. **11** ca còn lại ⛔ đổi một byte |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `12_P6_WEB_PLAN.md` *(v0.10 → **v0.11**)* | dòng changelog vòng 2; quy ước thứ tư *(ô tiền bề rộng theo ngân sách ký tự đo trên sổ thật)* |

### Mọi chỗ in `dung_sai` *(`grep dung_sai fls/web/tep/*.js` — Phạm vi (g))*
| Tệp:dòng | Chỗ | Trước *(vòng 1)* | Sau |
|---|---|---|---|
| `man_f01.js:358` | đọc `d.dung_sai` | — | — |
| `man_f01.js:362`–`:373` | `ds_xu` *(so)* · `ds_in` *(in)* | in `TP.tien(ds, cur)` *(làm tròn)* | in `TP.tien(TP.chuoi_xu(ds_xu), cur)` *(sàn)* |
| `man_f01.js:396` | chữ *"dung sai"* của `#sig` | `TP.tien(ds, cur)` | `ds_in` |
| `man_f01_lenh.js:604`–`:609` | gợi ý *"dung sai Σ cho tiền tệ này"* | `TP.tien(d.dung_sai, r.curr)` | sàn xu *(nhánh ⛔ đổi được: chuỗi cửa trả)* |
| `man_f01_lenh.js:663` | `_tinh` so | `TP.xu(d.dung_sai, 'san')` | ⛔ đổi *(đã đúng)* |
| `goi_cua.js:90` | câu lỗi chung *"…lệch ngoài dung sai"* | chữ, ⛔ số | ⛔ đổi |

Tập tệp đọc `dung_sai` = **2** *(`man_f01.js`, `man_f01_lenh.js`)* — bài `test_AC14_moi_tep_doc_dung_sai_DA_LIET_KE_…` khoá đúng tập này.

### Lời gọi `TP.tien` sau vòng 2 *(máy đếm theo ngoặc của bài `AC-2`)*
**42** lời *(vòng 1: 40)* — +1 `man_f01.js` *(`ds_in` có hai nhánh)* · +1 `man_f01_lenh.js:608`/`:609` *(hai nhánh)*. Mọi lời **2** đối số; `null` tường minh **0** chỗ. `AC-2` xanh *(≥ 38)*.

## Cổng *(kết quả nguyên văn · `PG_DSN=postgresql://fls:fls@localhost:5433/fls` · `PYTHONUTF8=1` · cây làm việc = `3173d7f`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | **`2178 passed, 3 xfailed in 315.47s (0:05:15)`** *(nền `BG-027`: `2166 passed, 3 xfailed` ⇒ **+12** = đúng 12 bài mới; 3 `xfail(strict)` `kq021` *(`F-1`×2 · `F-2`, của `WO-023`)* vẫn `xfail` — **0** `XPASS`)*. ⚠ Lượt **đầu** ra `1 failed, 2177 passed, 3 xfailed in 308.54s` — `tests/api/test_cua_chup_pg.py::test_nguon_CHUA_AI_KHAI_van_CO_MAT_voi_khai_version_null` nổ `UndefinedTable: relation "fls_source" does not exist` trên **kho TEST**, vì tôi chạy các cổng khác **song song** với `pytest`; chạy riêng tệp ấy `30 passed`, chạy lại **toàn bộ** một mình ⇒ số trên. ⛔ do mã vòng 2 *(tệp ấy ⛔ chạm `fls/web`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 44 lech/khong-do-duoc` **= nền đầu vòng 2** *(bảng tách dưới)* · ⛔ chạy `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (117 file, 1357 bang, 662 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(trên cây mã; cây giấy cuối *(sau tờ này + `WO` + README + dashboard)*: `✅ cong tai lieu DAT — va no da do duoc that (118 file, 1363 bang, 662 o ngay, 104 ma QD)…`; `kiem_so_song` trên cây giấy cuối vẫn **44**; `khop_owner --kiem` vẫn `✅ cong C1 DAT`)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech   (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến đổi)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` | `9 passed in 0.65s` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — vòng 2 ⛔ chạm schema *(`git diff a7fd01f 3173d7f -- fls/db` rỗng)*; lệnh này áp di trú lên kho THẬT |

### AC-15 · `kiem_so_song` tách nền đầu vòng 2 ⟷ sau *(đếm **dòng** `⛔ LỆCH`, `Đ4`)*
| Loại | Nền đầu vòng 2 *(`a7fd01f`, trước mã)* | Sau *(cây = `3173d7f`)* | Ghi chú |
|---|--:|--:|---|
| (b) nhịp chụp *(`kho · anh chup dong lenh` · ba `DẤU THỜI ĐIỂM` · `master · kho` · `roadmap · ảnh chụp` · `bản vẽ · ảnh chụp lệnh chi` ×2 · `bản vẽ 13 · ảnh nhịp` ×2 · `bản vẽ 13 · ảnh lệnh chi khác nhau` · `dashboard · ảnh nhịp trên tổng ảnh` ×2)* | **13** | **13** | ⛔ do phiếu — giá trị ⛔ dịch giữa hai lượt đo |
| (c) phiếu trước *(commit, `DEV-04` ×2, số file `105`, `db`/`repo` ×6, thanh repo)* | **13** | **13** | ⛔ đổi |
| (c) số bài / dòng mã *(đã đỏ từ trước)* | **17** | **17** | **dịch giá trị vì phiếu này**: bài `2169 → 2181` *(+12)* · module `1845 → 1857` · dòng `25.635 → 25.689` · `web` `8.996 → 9.050` dòng / `508 → 520` bài |
| (c) `master · §8 version DEV-12` | **1** | **1** | **cùng dòng**, giá trị dịch `0.10 → 0.11` *(phiếu bump `DEV-12` v0.11; ô ở `00_MASTER_INDEX` §8 là của `fls-ba`, số sinh qua `dong_bo --ghi` — `WO` cấm chạy)* |
| **Đỏ MỚI loại (c) của vòng 2** | — | **0** | `diff` tên 44 dòng nền ⟷ sau *(bỏ giá trị máy đo)*: **trùng từng dòng** |
| **Σ** | **44** | **44** | `13 + 13 + 17 + 1 = 44` ✔ cả hai cột |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Chiều ĐỎ đã chạy |
|---|---|---|
| **AC-10** | `test_AC10_hai_cot_tien_mcols_du_NGAN_SACH_18_ky_tu` — **đọc** `--fs-than` *(`12.5`)* từ `tokens.css`, vị trí cột từ `COT_BANG` *(`so_tien` = **6**, `gd_tien` = **11** — ⛔ ghim)*, vệt từ **đúng một** luật `.mcols` *(0 hay ≥ 2 ⇒ nổ)*: `136px` ≥ `ceil(18 × 0,6 × 12.5) = 135` ở cả hai; số vệt = số cột | Trên `a7fd01f`: ĐỎ *(`108px`/`116px` < 135, hai lỗi)*. Bài `…cong_CAN__108px__fs_13px__chen_cot…` chạy ba chiều đỏ của `WO` trên **nguồn thật đã phá trong bộ nhớ**: `108px` ⇒ lỗi `so_tien` · `--fs-than:13px` ⇒ **2** lỗi *(140,4 > 136)* · chèn `['moi','Mới']` trước `Số tiền` ⇒ lỗi *"11 vệt ≠ 12 cột"* · vệt `minmax(140px,1fr)` ⇒ *"⛔ phải px cố định"*. Đột biến trên tệp thật **M1** *(108)* · **M1b** *(GD 116)* · **M2** *(`tokens.css` 13px)* · **M3** *(chèn cột)* ⇒ cả bốn ĐỎ |
| **AC-11** | `test_wo022_v2_o_tien_pg.py::test_AC11_…` — `noi_chi_doc(dsn_that())`, phạm vi **mặc định của cửa** `chi_nap_that()`, gọi **hàm repo của cửa** `lenh_cho.doc_lenh_cho` + `doc_lenh_da_gan` *(lật hết trang, `TRANG_TOI_DA`)* — ⛔ SQL chọn run; `Decimal` ⇒ chuỗi bằng **chính** `bao._thuong` của cửa; chuỗi ô = **đúng hai biểu thức** của `ve_bang` qua `TP.tien` **thật** *(`node`)*. In ra *(02/10)*: lệnh **3.820** — `USD` 1.030 · dài nhất `103.950.000,00 USD` **18** · `VND` 2.721 · `5.000.000.000 VND` 17 · `SGD` 57 · 16 · `HKD` 10 · 14 · `EUR` 1 · `20` 1; sổ **8.387** — `VND` 4.242 · **18** *(`11.500.000.000 VND`; `11.742.361.787 VND` cũng 18)* · `USD` 3.980 · 16 · `HKD` 20 · 16 · `SGD` 145 · 14. **0** chuỗi > 18 ⇒ xanh. Mẫu số **⛔ ghim** — chỉ đòi > 0 | **M11** *(ngân sách tạm `17`)* ⇒ ĐỎ. Tập rỗng ⇒ hai `assert … "⛔ không đo được"`. ⚠ Bài này **xanh trên `a7fd01f`** — đúng: nó đo **dữ liệu**, ⛔ đo mã *(đỏ thật về sau = dữ liệu vượt ⇒ việc của `fls-ba`)* |
| **AC-12** | Chrome headless **1440×900**, máy **8099** chỉ đọc *(`chay_cua.py --cho-web`, ⛔ `--cho-ghi`)* trỏ **kho TEST**; dữ liệu dựng riêng *(run `NAP-2000-01-01-WE578E7`)*: lệnh **X** `103.950.000,00 USD` *(chưa gán — chip `Không gán được`)* · lệnh **Y** VND `11.742.361.787` gán dòng tiền VND `11.742.361.787` *(chip `Đã gán`)* · lệnh **Z** `100.000.000.000 VND` *(19 ký tự)*. Đo trên **ô thật** của bảng *(view ①)*: **Y** `Số tiền` `11.742.361.787 VND` — `scrollWidth 136 ≤ clientWidth 136` ✔ · `Số tiền GD` `11.742.361.787 VND` — **136 ≤ 136** ✔ · **X** `103.950.000,00 USD` — **136 ≤ 136** ✔ · cột `Nội dung` `clientWidth` **200** *(≥ 160 ✔)* ở cả ba hàng · trang `scrollWidth 1440 ≤ clientWidth 1440` ✔ ở cả ba lượt · **Z** ô `textOverflow = 'ellipsis'` ✔, `whiteSpace = 'nowrap'`, `title = '100.000.000.000 VND'` ✔, `scrollWidth 139 > clientWidth 136` *(cắt có `…` — ảnh)*. Lỗi console **0**; lượt ⛔ `GET` tới `/api` **0**. Ảnh *(⛔ lên git)*: `scratchpad/man/w22v2_bang_da_gan_Y.png` · `w22v2_bang_X.png` · `w22v2_bang_Z.png`; số đo thô `scratchpad/v2w22_soi.json` | Cùng máy, cùng hàng **Y**, đè `<style>` tạm *(⛔ sửa tệp)* trả vệt `108px`/`116px` + `text-overflow:clip`: `11.742.361.787 VND` — `scrollWidth 132 > clientWidth 108` **cắt** · cột GD **132 > 116** **cắt** ⇒ ĐỎ; ảnh `w22v2_DO_vet_cu_Y.png`. Ở DOM giả: **M4** *(bỏ `text-overflow`)* · **M5** *(bỏ `title`)* ⇒ ĐỎ. Đã tắt máy 8099 sau khi đo *(8088 ⛔ chạm — vẫn chạy)* |
| **AC-13** | `test_AC13_mot_luat_so_le_SAU_ca_dung_tung_byte` — 6 ca nguyên văn `WO`, so từng byte. `test_AC13_ma_LA_va_THIEU_cung_luat…` — **quan hệ**: trên 16 giá trị *(gồm `-0.00`, `0.05`, số JS `7`/`66923.25`, `999999999999.99`)* chữ in của `'20'` · `null` · `undefined` · `''` · `' xyz '` **= VND**. `AC-1` 12 ca: **11** ⛔ đổi + ca 10 theo `AC-13` | Trên `a7fd01f`: cả hai ĐỎ *(`100,5` · `12,5` · `0,5`)*. **M6** *(trả đúng nhánh vòng 1: mã lạ cắt 0 đuôi)* ⇒ 3 bài ĐỎ · **M7** *(mã lạ cố định 2 ⇒ `100,00`)* ⇒ 3 ĐỎ · **M8** *(mã lạ làm tròn 0 lẻ ⇒ `101`)* ⇒ 3 ĐỎ. ⚠ Lượt đầu tôi viết M6 thành `SO_LE[ma] : null` — **sống sót**, vì `that <= null` ⇔ `that <= 0` trong JS *(đột biến tương đương với mã mới, ⛔ là mã vòng 1)*; viết lại đúng nhánh vòng 1 ⇒ bị bắt |
| **AC-14** | `F01` hộp **thật** `_drawer_ghep` *(khuôn bài `AC-4`)*, VND, `dung_sai "617.285"`: chữ `dung sai <b class="num">617,28</b>` ở **cả hai** ca; lệch `617,29` ⇒ `crit` + nút Ghép **khoá**; lệch `617,28` ⇒ `khớp — cho ghép` + nút **mở**. `dung_sai "1000"` ⇒ `1.000`. `F01L` hộp **thật** `_drawer_tim_tien`: `dung sai Σ cho tiền tệ này: <b>617,28</b>` *(⛔ `617,29` ở đâu trong hộp)* · `"1000"` ⇒ `<b>1.000</b>` | Trên `a7fd01f`: `F01` ĐỎ *(`617,29`)* · `F01L` ĐỎ *(`617,29`)* — **cả hai** hộp. **M9** *(F01 in `TP.tien(ds, cur)`)* ⇒ ĐỎ · **M10** *(F01L in `TP.tien(d.dung_sai, r.curr)`)* ⇒ ĐỎ · **M12** *(thêm `TP.tien(x.dung_sai, …)` vào `man_f02.js`)* ⇒ bài quét ĐỎ |
| **AC-15** | Mục **Cổng** trên: `pytest` **2178 passed, 3 xfailed** · `lint-imports` 9/0 · `soi_bang_tuyen` 40/40 · `kiem_thuyet_minh` 31/31 · hai bài ký hiệu / token `9 passed` · `kiem_so_song` **44 = 44**, đỏ mới (c) **0**, bảng cộng ra đúng tổng; ⛔ `dong_bo --ghi` | — |

⭐ **13/13 đột biến bị bắt** *(`scratchpad/dot_bien_v2.py`: sửa tạm → chạy hai tệp bài DOM (M11: tệp `_pg`) → trả nguyên, so `sha256` mỗi lượt; kết quả `scratchpad/dot_bien_v2.txt`)*: M1 · M1b · M2 · M3 *(AC-10)* · M4 · M5 *(AC-12)* · M6 · M7 · M8 *(AC-13)* · M9 · M10 · M12 *(AC-14)* · M11 *(AC-11)*. Bài mới chạy trên mã `a7fd01f` *(`git stash` riêng `fls/web/tep`)*: **9 failed, 30 passed** — 8 bài mới + ca 10 `AC-1`.

## Kho thật
- **`KHONG_CHAM`** *(ghi)*. Chỉ `SELECT` qua `noi_chi_doc` *(bài `AC-11` + `AC-5` cũ)*. Máy **8088** ⛔ chạm, vẫn chạy chỉ đọc.
- Kho **TEST** *(`fls_test`)*: thêm hai run `NAP-2000-01-01-W4DEDFE` *(lượt đầu — `source_sheet` `L1` sai khuôn ⇒ ô GD `loi_nguon` `—`, ⛔ dùng)* + `NAP-2000-01-01-WE578E7` *(dùng đo)*: mỗi run 3 dòng lệnh + 1 dòng tiền VND + 1 cú ghép, actor `fls-dev@apero.vn` — kịch bản `scratchpad/v2w22_dung_8099.py` *(`dsn_test()` + `assert …endswith("fls_test")`)*.

## Cách chạy để xem
```bash
export PYTHONUTF8=1 PG_DSN='postgresql://fls:fls@localhost:5433/fls_test' FLS_JWT_SECRET='<>= 32 ký tự>'
python scratchpad/v2w22_dung_8099.py             # dựng X/Y/Z trên KHO TEST, in id
python tools/chay_cua.py --cong 8099 --cho-web   # CHỈ ĐỌC — ⛔ --cho-ghi
node scratchpad/v2w22_soi.mjs <S> 8099 <id.json> # đo + chụp; rồi tắt máy 8099
```
Màn `②b Gán lệnh chi` → chip `Đã gán` *(hàng Y)* / `Không gán được` *(hàng X, Z)*, ⛔ mở lệnh nào *(view ① bảng)*.

## Dev tự thấy còn yếu
1. ⚠ **Phông đo ⛔ phải phông rộng nhất.** Máy đo *(Windows 11)* ra `Cascadia Mono` — `11.742.361.787 VND` rộng **132px** *(7,33 px/ký tự)*, tức ô `136px` thừa 4px. Trên máy có **`IBM Plex Mono`** chuỗi 18 ký tự rộng **135px** — vừa, sát 1px. ⛔ có máy nào cài `IBM Plex Mono` để tôi đo thật; con số 0,600em lấy từ `TL-026`. Test nên soi trên máy kế toán.
2. ⚠ **`AC-10` dùng `0,6em` là HẰNG trong bài** *(`EM_MONO_RONG_NHAT`)* — bài **đọc** `--fs-than` nhưng ⛔ đọc chuỗi phông `--mono`. Đổi phông `--mono` sang một phông rộng hơn thì cổng **vẫn xanh** — kể cả khi phông mới rộng hơn 0,6em. Canh phông đòi đo bề rộng glyph — ngoài tầm một bài đọc nguồn.
3. ⚠ **`AC-11` đọc tập lệnh của phạm vi mặc định `chi_nap_that()` của chip `Tất cả` *(hai rổ)*** — ⛔ đọc theo từng rổ `ro=nguoi` / `ro=may` / `ro=khong` *(cùng tập gộp lại, theo `lenh_cho` docstring "hai rổ khép về tổng")*. Cột `Số tiền GD` tôi đo trên **mọi** `ps_no`/`ps_co ≠ 0` của sổ *(đúng `WO`)*, ⛔ trên đúng các `gd.amount` mà cửa gắn vào hàng — tập sổ là **siêu tập**, nên an toàn về phía đỏ.
4. ⚠ **Bảng `F01L` / hộp ② / thẻ / rail / lưới `F02`** ⛔ đo lại ở vòng 2 — vòng 2 ⛔ chạm chúng *(chỉ `.mcols`)*; số đo vòng 1 ở `BG-027` `AC-7`. Chuỗi 18 ký tự ở thẻ / rail **chưa** đo trên Chrome *(vòng 1 đo chuỗi 16 ký tự)* — `TL-026` nói chúng vừa, tôi ⛔ tự đo.
5. ⚠ **Lưới an toàn `…` chỉ ở bảng lệnh.** §5b ⓘ nói *"mọi ô tiền có bề rộng cố định"* — hôm nay tôi chỉ thấy `.mcols`; ⛔ quét hết `hinh.css` tìm ô tiền `px` cố định khác *(bảng `F01L` dùng `<table>` tự giãn)*.
6. ⚠ **`title` ⛔ đọc được bằng bàn phím / máy đọc màn.** Chuỗi > 18 ký tự *(hôm nay 0)* chỉ lộ đủ khi **di chuột** — người dùng bàn phím *(`NFR-I24`)* ⛔ thấy. Hàng mở ra *(rail + vùng ghép)* vẫn in đủ, nên ⛔ mất số, chỉ mất ở bảng.
7. ⚠ Nhánh *"dung sai ⛔ đổi được sang xu ⇒ in chuỗi cửa trả"* ⛔ có bài thử riêng *(cửa hôm nay luôn trả chuỗi số)*; hộp `F01` ở nhánh ấy đã ⛔ cho ghép *(bài vòng 1)*, hộp `F01L` cũng *(`hong`)*.
8. ⚠ Bài quét `test_AC14_moi_tep_doc_dung_sai_DA_LIET_KE…` **xanh trên `a7fd01f`** — nó ⛔ phải bằng chứng `AC-14` *(hai bài hành vi mới là)*; nó chỉ chặn **chỗ in mới** chưa có bài *(M12)*.
