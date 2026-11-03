# BG-027 — bàn giao `WO-022` *(in tiền theo tiền tệ · tổng / lệch trên số nguyên xu)*

| | |
|---|---|
| **Thuộc** | [`WO-022`](WO-022-in-tien-theo-tien-te.md) *(vòng 1)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`7746e48`** *(đã đẩy — mã + bài + tài liệu Dev + `HOI-026`)*; tờ này + `WO`→`CHO_TEST` + README ở commit giấy ngay sau |
| **Spec** | `BA-06` **v4.12** §5 `UI-F10` + §5b ⓐ…ⓗ *(đọc ở cổng vào — header tệp `v4.12`)* |
| **Câu treo** | `Q-TIEN-1` *(owner chưa trả lời)* ⇒ mã giữ mặc định spec **"in đủ"** — đổi = một nhánh `tien()` *(dòng `else n = LE_KHO;`)* + một ca `AC-1` |
| **Phiếu mở kèm** | [`HOI-026`](HOI-026-cot-so-tien-bang-lenh-108px-cat-chuoi-16-ky-tu.md) `LECH_DU_LIEU` · `KHONG_CHAN` — cột `Số tiền` của **bảng danh sách lệnh** *(`108px`)* cắt chuỗi ≥ 15 ký tự ⇒ `AC-7` **⛔ đạt ở đúng một ô** |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/thanh_phan.js` | ⓐ `TP.SO_LE` *(hằng **một chỗ**, `Object.freeze`: `VND 0` · `USD/SGD/HKD/EUR 2`)* · `TP.tien(v, curr)` **tách chuỗi** *(⛔ `Number`)*: số lẻ cố định cho mã trong bảng; lẻ hơn bảng ⇒ in **đủ** theo thang kho `2` *(§5b ⓑ)*; mã lạ / `null` ⇒ chữ số thật tối thiểu 0 tối đa 2 *(ⓒ)*; `.` nghìn `,` thập phân, số 0 ⛔ mang dấu *(ⓓ)*; mã so sau `trim` + viết hoa. `TP.xu(v[, 'san'])` → số nguyên xu *(làm tròn **một** lần, nửa ra xa 0; `'san'` = cắt — cho dung sai)* · `TP.chuoi_xu(n)`; chú thích đầu hàm giữ câu *"⛔ dùng để TÍNH"* + thêm luật ⓕ/ⓖ + ghi chú Rủi ro ③ *(`fls_tien_te` ra đời ⇒ đọc từ cửa)* |
| `fls/web/tep/man_f01.js` | 8 lời gọi mang `curr`; hộp *Ghép lệnh* `_tinh`: Σ / lệch / dung sai trên **xu** *(dung sai bằng **sàn**)*; số ⛔ đổi được ⇒ *"⛔ không tính được"* + ⛔ cho ghép; đọc ô tích qua `#dlg-b input` + lọc `type`/`checked` *(cùng tập trên trình duyệt; DOM giả đọc được)*; người nghe `change` = `#dlg-b.onchange` *(⛔ `addEventListener` — `#dlg-b` sống qua mọi hộp, cộng dồn thì `_tinh` hộp cũ chạy lại)*; xuất `ve_tom`, `_drawer_ghep` cho bài thử |
| `fls/web/tep/man_f01_ghep.js` | 13 lời gọi mang `curr`; `ve_tong_chum` Σ/lệch trên xu, khớp ⇔ lệch = 0 *(giữ phép `hoặc 0` cũ cho số ⛔ đọc được — ⛔ đổi hành vi ngoài phạm vi)*; `khop_dung_tien` so xu, **hai số thiếu ⛔ còn = khớp** *(cũ: `Number(null) === Number(null)` ⇒ `true`)*; xuất `ve_tong_chum` |
| `fls/web/tep/man_f01_lenh.js` | 10 lời gọi mang `curr`; hộp *Tìm tiền* `_tinh` *(`:653`–`:654` cũ)*: lệch trên xu, dung sai sàn; chọn ô radio qua `#dlg-b input` + lọc; xuất `_drawer_tim_tien` |
| `fls/web/tep/man_f02.js` | 7 lời gọi: `_hien(k, v, curr)` *(lưới + panel ① truyền `r.curr` / `d.curr`)*, dải `Nợ/Có`, chip cả hai vế, mối nối ⑤ `d.curr` *(cửa ghép từ chối khác tiền tệ — `ghi_tay.ghep_lenh` ⓔ)* |
| `fls/web/tep/man_f03.js` | bảng độ phủ `TP.tien(r.tien_cho, r.curr)` |
| `fls/web/tep/man_f04.js` | xem trước sao kê: `TP.tien(v, r.o['Currency'])` — ô `Currency` **của chính dòng**; ô vắng ⇒ nhánh mã lạ ⓒ |
| `tests/web/test_wo022_tien_theo_tien_te.py` | **27** bài: AC-1 *(12 ca từng byte + bảng một chỗ + mã viết thường + chuỗi ⛔ số)* · xu *(tách chuỗi, vượt thang, số rất lớn)* · AC-2 *(quét **theo ngoặc** + bài chứng minh máy đếm cắn)* · AC-4 *(hộp `F01` thật · `ve_tong_chum` · dung sai sàn)* · AC-6 *(sáu màn)* · 3 bài bổ sung sau đột biến |
| `tests/web/test_wo022_tien_theo_tien_te_pg.py` | **2** bài: AC-3 *(ca **U** dựng qua **cửa thật** trên kho TEST, thân `/chum` thật vào hộp ② `HT.mo` thật)* · AC-5 *(khứ hồi **toàn** sổ thật, `noi_chi_doc`, chỉ `SELECT`)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `12_P6_WEB_PLAN.md` *(v0.9 → **v0.10**)* | dòng changelog `WO-022`; ba quy ước tiền cho mọi màn về sau |
| `handoff/HOI-026-…` | xem **Phiếu mở kèm** |

### Danh sách lời gọi `TP.tien` *(máy đếm của bài `AC-2`, đếm theo ngoặc, trên `7746e48`)*
`Đ4`: `WO` ghi **38** = số **dòng** có `TP.tien(` *(`grep -c`)*; số **lời gọi** = **40** *(`man_f01_lenh.js` `:665`+`:666` cũ `:654` · `man_f02.js:1130` mỗi dòng hai lời)*. Đối số thứ hai `null` **tường minh**: **0** chỗ.

| Tệp | Lời gọi | `dòng:đối số 2` |
|---|--:|---|
| `man_f01.js` | 8 | `65:r.curr` · `122:r.curr` · `309:u.curr` · `317:cur` · `382:cur` · `384:cur` · `386:cur` · `387:cur` *(`cur = d.dong_so.curr`)* |
| `man_f01_ghep.js` | 13 | `262:lenh.curr` · `368:g.curr` · `376:g.curr` · `415:lenh.curr` · `419:lenh.curr` · `420:lenh.curr` · `499:uv.curr` · `558:uv.curr` · `560:uv.curr` · `674:d.curr` · `1170:d.curr` · `1178:d.gd.curr` · `1220:d.curr` |
| `man_f01_lenh.js` | 10 | `87:r.curr` · `392:r.curr` · `554:x.curr` · `586:u.curr` · `588:u.curr` · `594:r.curr` · `605:r.curr` · `664:r.curr` · `665:u.curr` · `666:r.curr` |
| `man_f02.js` | 7 | `550:curr` *(`_hien`)* · `585:r.curr` · `586:r.curr` · `1130:r.curr` ×2 · `1133:r.curr` · `1780:d.curr` |
| `man_f03.js` | 1 | `127:r.curr` |
| `man_f04.js` | 1 | `564:r.o['Currency']` |
| **Σ** | **40** | |

### Mọi phép tính tiền khác trên màn *(`grep reduce( · Math.abs( · - bank · Number(…tiền…)` — Phạm vi (c))*
Đã đổi sang xu: `man_f01.js` `_tinh` · `man_f01_ghep.js` `ve_tong_chum` + `khop_dung_tien` · `man_f01_lenh.js` `_tinh`. **⛔ tiền — giữ:** `man_f01.js:643` *(đếm mã lệnh)* · `man_f01_lenh.js:103` *(đếm dòng chưa duyệt)* · `man_f04.js:368/404/406` *(đếm dòng)*. **So với 0 — giữ** *(chính xác với chuỗi thập phân)*: `man_f01_ghep.js` `Number(g.lech) !== 0` · `Number(uv.lech) !== 0` · `man_f02.js` `_co_tien` · lớp `neg`.

## Cổng *(kết quả nguyên văn · `PG_DSN=postgresql://fls:fls@localhost:5433/fls` · `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | **`2166 passed, 3 xfailed in 308.33s (0:05:08)`** *(nền lúc nhận trên `5f8796b`: `2137 passed, 3 xfailed in 308.46s` ⇒ **+29** = đúng 29 bài mới; 3 `xfail(strict)` `kq021` vẫn `xfail` — **0** `XPASS`)* |
| `python tools/kiem_so_song.py` | trên `7746e48` *(mã)*: `⛔ CONG SO SONG KHONG DAT — 43 lech/khong-do-duoc` **= nền**; trên cây giấy cuối *(sau tờ này + `HOI-026` + `DEV-12` v0.10)*: **`⛔ CONG SO SONG KHONG DAT — 44 lech/khong-do-duoc`** — +1 = đỏ **mới** loại (c) của phiếu *(bảng AC-9 dưới)* · ⛔ chạy `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (117 file, 1353 bang, 660 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(cây giấy cuối; trên `7746e48`: 116 file · 1347 bảng)* *(lượt đầu ĐỎ `K3` — dấu `\|` trần trong dòng changelog của chính phiếu này; đã thoát)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` *(đo trên cây làm việc trước commit `7746e48`)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` | `9 passed in 0.85s` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — phiếu ⛔ chạm schema *(`git diff 5f8796b 7746e48 -- fls/db` rỗng)*; lệnh này áp di trú lên kho THẬT |

### AC-9 · `kiem_so_song` tách nền ⟷ sau *(đếm **dòng lệch**, `Đ4`)*
| Loại | Nền đầu phiếu *(`5f8796b`, trước mã đầu tiên)* | Sau *(cây làm việc = `7746e48`)* | Ghi chú |
|---|--:|--:|---|
| (b) nhịp chụp *(ảnh lệnh chi `256.928`, dấu giờ, ảnh nhịp, ảnh lệnh chi khác nhau, `master · kho`)* | **13** | **13** | cả 13 dịch giá trị theo giờ *(`264.568 → 268.388` · `15:09 → 16:09` · `140 → 142` · `70 → 71`)* — ⛔ do phiếu |
| (c) phiếu trước *(commit `88ab178`, DEV-04 `1.16`, số file `105`, `db`/`repo`)* | **13** | **13** | ⛔ đổi |
| (c) số bài / dòng mã *(cũng đã đỏ từ trước)* | **17** | **17** | **dịch giá trị vì phiếu này**: bài `2140 → 2169` *(+29)* · module `1816 → 1845` · dòng `25.426 → 25.635` · `web` `8.787 → 8.996` dòng / `479 → 508` bài |
| **Đỏ MỚI loại (c) của phiếu** | — | **1** | `master · §8 version DEV-12` — tài liệu ghi `0.9` · máy đo `0.10`: chính phiếu này bump `03_Dev/12_P6_WEB_PLAN.md` v0.9 → **v0.10**. Ô ấy ở `00_MASTER_INDEX` §8 *(chủ `fls-ba`; số máy sinh qua `dong_bo --ghi` — `WO` cấm chạy)* ⇒ ⛔ tự sửa. Trên `7746e48` *(trước tờ giấy)* đã đo **43**, tên 28 nhóm trùng nền từng dòng |
| **Σ** | **43** | **44** | nền `13 + 13 + 17 = 43` ✔ · sau `13 + 13 + 17 + 1 = 44` ✔ |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Chiều ĐỎ đã chạy |
|---|---|---|
| **AC-1** | `test_AC1_tien_MUOI_HAI_ca_dung_tung_byte` — 12 ca nguyên văn bảng `WO`, so **từng byte**. Thêm: `…SO_LE_khai_MOT_cho…` *(bảng = 5 mã, `isFrozen`, gán ⛔ ăn)* · `…ma_tien_te_viet_THUONG…` *(`' usd'`, số JS `66923.25`, `1240000000`)* · `…chuoi_KHONG_phai_so…` *(`'1,234.56'` in nguyên văn đã thoát)* | Trên `5f8796b`: **9/12** ca đỏ *(`1.235` · `1.234` · `765` · `0` · `-0` · `13` · `1.565.307` · `1.306.104` · `101`; xanh 3: `39.457.436` · `100` · `—`)*. Đột biến **M1** *(trả `maximumFractionDigits: 0`)* ⇒ 18 bài đỏ · **M2** *(bỏ số lẻ cố định)* ⇒ 11 · **M3** *(làm tròn VND về bảng)* ⇒ 2 *(AC-1 + AC-5)* · **M4** *(mã lạ = VND)* ⇒ 1 |
| **AC-2** | `test_AC2_MOI_loi_goi_TP_tien_co_DUNG_hai_doi_so` — quét 11 tệp `fls/web/tep/*.js`, đếm theo **ngoặc** sau khi bóc chuỗi / chú thích / regex: **40** lời *(≥ 38 ✔)*, **0** lời ≠ 2 đối số, tệp có lời gọi = đúng 6 tệp màn, `null` tường minh = `[]` = danh sách trên. Máy đếm được chứng minh cắn: `test_AC2_may_dem_CAN_…` *(lời gọi xuống dòng · `,` trong chuỗi · `TP.tien(` trong chú thích · regex `/[,)]/` · tập rỗng)* | Trên `5f8796b`: **40/40** lời một đối số ⇒ ĐỎ. **M10** *(một lời `F03` một đối số)* ⇒ ĐỎ; **M12** *(`F04` truyền `null`)* ⇒ ĐỎ |
| **AC-3** | `test_wo022_…_pg.py::test_AC3_ca_U_than_CHUM_THAT__…` — kho TEST: dòng tiền USD `2000.00` ghép **qua `POST /queue/{id}/match` thật** hai lệnh `1234.56` + `765.44`; `GET /chum` thật trả `so_dong 2 · can_hoi true · dong_lenh[{pm_line_id, amount "1234.56", curr "USD"}, …]` ⇒ đưa nguyên thân vào màn ghép *(`hop_thoai.js` thật, `HT.mo` chỉ bọc đếm)*: hộp ② `… — 1.234,56 USD` **và** `… — 765,44 USD`; thẻ `["1.234,56 USD"]`; rail có `1.234,56 USD` + `765,44 USD`; `1.235 USD` / `765 USD` ⛔ ở đâu. Tổng chùm `2.000,00 USD — khớp`: `test_AC3_tong_chum_ca_U_2000_00_USD_khop` *(ca U **đảo chiều** — một lệnh `2000.00` trả bằng hai giao dịch; ⚠ xem "còn yếu" #6)*. ⭐ Chrome 8099 cũng thấy trên cửa thật *(AC-7)* | Trên `5f8796b`: hộp in `PW…-1 — 765 USD<br>PW…-1 — 1.235 USD` ⇒ ĐỎ; tổng chùm `2.000 USD` ⇒ ĐỎ |
| **AC-4** | `F01` hộp **thật** `_drawer_ghep` *(cửa giả trả `dong_so`/`dung_sai "0"`/ứng viên USD; ô tích dựng trong `#dlg-b`; sự kiện qua `#dlg-b.onchange` thật; nút `Ghép` là nút `HT.mo` dựng)*: `0.10 + 0.20` vs `0.30` ⇒ `lệch 0,00`, `khớp — cho ghép`, nút **mở** · `1234.56` vs `1234.16` ⇒ `lệch 0,40`, `crit`, nút khoá · đảo ⇒ `-0,40` · `4.35 + 0.65` vs `5.00` ⇒ khớp · dung sai VND `617.285` ⇒ lệch `617,28` cho, `617,29` **khoá** *(sàn)*. `ve_tong_chum`: `0,30 USD — khớp` · `1.234,56 USD — lệch 0,40 USD so với 1.234,16 USD` · `4.35+0.65` khớp `5,00`. `khop_dung_tien` `[True, False, False, False]` | **M13** *(nguyên khuôn mã cũ: `Σ Number − Number(bank) ≤ Number(ds)`)* ⇒ `…0_10_cong_0_20…` ĐỎ *(đúng chiều `WO`)* · **M6** *(`Number × 100`)* ⇒ 2 đỏ · **M7** *(dung sai làm tròn, ⛔ sàn)* ⇒ 1 · **M8** *(tổng chùm `Number × 100`)* ⇒ 1 *(lượt đầu **sống sót** — `0.1*100 === 10` tình cờ đúng ⇒ thêm ca `4.35+0.65`)* · **M11** *(null = null)* ⇒ 1. Trên `5f8796b`: `Tổng 2 giao dịch: 0 USD`, `lệch -1.234` |
| **AC-5** | `test_AC5_KHU_HOI_moi_ps_no_ps_co_cua_SO_THAT_bang_gia_tri_kho` — `noi_chi_doc(dsn_that())`, chỉ `SELECT`: **8.387** giá trị `ps_no`/`ps_co` ≠ 0, mỗi giá trị qua `TP.tien` thật *(một lượt `node`, dữ liệu qua tệp)* ⇒ bỏ `.` · `,`→`.` ⇒ `Decimal` = kho: **0** lệch. Mẫu số in ra: dòng có phần lẻ USD **2.413** · SGD **74** · HKD **20** · VND **11** *(khớp đếm 02/10 của `WO`; bài chỉ đòi > 0 — ⛔ ghim hằng)* | Trên `5f8796b`: **2.518 / 8.387** giá trị lệch *(≥ 2.500 ✔)* — vd. `SGD 25823.47 → 25.823`, `SGD 0.20 → 0`. **M3** ⇒ ĐỎ *(11 dòng VND)* |
| **AC-6** | `F01` chân màn `Σ 2.000,40` · `F01G` thẻ + rail `1.234,56 USD` · `F01L` chân màn `1.234,56` + hộp *Tìm tiền* `lệch <b>0,40</b>` + `VƯỢT dung sai` · `F02` lưới `1.234,56` + panel `−1.234,56 USD` + `Nợ 100,50 Có 0,25` · `F03` `<td class="r">765,44</td>` · `F04` `66.923,25` + USD số nguyên `5.000,00` *(ô `Currency` `' usd '`)* | Trên `5f8796b` mỗi bài đỏ *(`1.235`, `765`, `66.923`)*; **M9** *(F01L lệch `Number`)* ⇒ ĐỎ |
| **AC-7** | Chrome headless **1440×900**, máy **8099** chỉ đọc trỏ **kho TEST** *(dòng dựng riêng: chùm U `2.260.708,38` = A `2.259.942,94` + B `765,44` USD · lệnh C `2.259.942,94` chưa gán · dòng tiền V `2.259.942,94` chưa nối)*. `scrollWidth / clientWidth`: thẻ **150/150** · rail **117/117** *(+ `765,44 USD` 73/73)* · hộp ② thân **484/484** *(hộp 518/518; tiêu đề `Bỏ gán sẽ gỡ CẢ 2 lệnh chi`)* · lưới `F02` **157/157** · panel `F02` **180/180** ⇒ ⛔ cắt. Trang `scrollWidth 1425 = clientWidth 1425` *(thanh cuộn của Chrome này **15px**; `KQ-021` đo 16px ⇒ 1424)* ⇒ ⛔ tràn ngang. Lỗi console **0**; lượt ⛔ `GET` **0**. ⛔⛔ **Bảng danh sách lệnh** *(view ①, `.mcell.r` cột `108px`)*: chữ **117,2px** > ô **108px** ⇒ in `2.259.942,94 US` — **⛔ ĐẠT** ⇒ [`HOI-026`](HOI-026-cot-so-tien-bang-lenh-108px-cat-chuoi-16-ky-tu.md) *(cùng cột ấy cắt `11.742.361.787 VND` **từ trước** phiếu — tiền đề "18 ký tự đã vừa" sai ở cột này; tầm **27** dòng ngoại tệ mới + **425** VND cũ)*. Ảnh: `scratchpad/man/wo022_{ghep_the_rail,hop_chum,ghep_bang,f02}.png` *(⛔ lên git)* | — |
| **AC-8** | `pytest` `2166 passed, 3 xfailed` *(3 = `kq021` `F-1`×2 + `F-2`)* · `lint-imports` 9/0 · `soi_bang_tuyen` 40/40 *(⛔ tuyến đổi)* · `kiem_thuyet_minh` 31/31 · hai bài ký hiệu / token `9 passed` | — |
| **AC-9** | Bảng tách ở mục **Cổng** — nền **43** = 13 (b) + 30 (c) trên `5f8796b`; sau **44** = nền + **1** đỏ mới loại (c) *(`master · §8 version DEV-12`, do bump `DEV-12` v0.10)*; ⛔ `dong_bo --ghi` | — |

⭐ **13/13 đột biến bị bắt** *(`scratchpad/dot_bien*.py`: sửa tạm → chạy hai tệp bài → trả nguyên, so `sha256` mỗi lượt)*. `M8` **sống sót lượt đầu** ⇒ thêm 3 bài *"bổ sung sau đột biến"*; chạy lại `M6`/`M8`/`M12` ⇒ bị bắt.

## Kho thật
- **`KHONG_CHAM`** *(ghi)*. Chỉ `SELECT` qua `noi_chi_doc` *(bài `AC-5`)* + `docker exec … psql` đếm tầm. Máy **8088** ⛔ chạm, vẫn chạy chỉ đọc.
- Kho **TEST** *(`fls_test`)*: thêm run `NAP-2000-01-01-U26FD99` *(2 dòng tiền USD + 3 dòng lệnh + 1 cú ghép, actor `fls-dev@apero.vn`)* để dựng máy 8099 — kịch bản `scratchpad/wo022_dung_8099.py` *(`dsn_test()` nổ nếu trỏ kho thật)*. Bài `AC-3` mỗi lượt chạy thêm một run `NAP-2000-…-W…` *(khuôn `test_wo003`)*.

## Cách chạy để xem
```bash
export PYTHONUTF8=1 PG_DSN='postgresql://fls:fls@localhost:5433/fls_test' FLS_JWT_SECRET='<>= 32 ký tự>'
python scratchpad/wo022_dung_8099.py            # dựng dòng USD trên KHO TEST, in id
python tools/chay_cua.py --cong 8099 --cho-web  # CHỈ ĐỌC — ⛔ --cho-ghi
node scratchpad/wo022_soi.mjs <S> 8099 <id.json> # đo + chụp; rồi tắt máy 8099
```
Đã tắt máy 8099 sau khi đo.

## Dev tự thấy còn yếu
1. ⚠ **Nhánh ⓑ đọc theo thang kho, ⛔ theo chữ số có nghĩa.** Mã trong bảng mà lẻ hơn bảng ⇒ in **2** chữ số *(`"1306103.80"` VND → `,80`, khớp `AC-1`)*; còn mã **lạ** thì cắt số 0 đuôi *(`"100.50"` → `,5`, cũng khớp `AC-1`)*. Hai nhánh **bất đối xứng** đúng như hai ca spec, nhưng spec ⛔ nói thẳng `"1306103.8"` VND in `,8` hay `,80` — mã in `,80`. Cửa hôm nay luôn trả 2 chữ số *(`numeric(20,2)` ⇒ `Decimal` thang 2)* nên chưa ai thấy khác.
2. ⚠ **AC-4 trên DOM giả, ⛔ bấm thật trên Chrome.** Hộp `F01` *Ghép lệnh* *(hàng chờ ②)* và hộp *Tìm tiền* `F01L` chỉ chạy dưới `node`: ô tích **do bài dựng**, sự kiện **do bài phát**. Tôi đổi cách đọc ô *(`#dlg-b input` + lọc thay `:checked`)* và cách nghe *(`onchange` trên `#dlg-b`)* — tương đương trên trình duyệt theo lý thuyết *(sự kiện `change` nổi bọt)*, nhưng **chưa tích chuột thật** trên 8099. Test nên tích `0.10` + `0.20` trên máy thật.
3. ⚠ `#dlg-b.onchange` **ở lại** sau khi hộp `F01` đóng: hộp khác có ô nhập đổi giá trị ⇒ `_tinh` cũ chạy, gặp `#sig` vắng ⇒ `return` *(chặn bằng một dòng `if (!sig)`)*. `F01L` vẫn `addEventListener` cộng dồn **từ trước** *(⛔ đổi — ngoài phạm vi; `_tinh` của nó có sẵn `if (!s) return`)*.
4. ⚠ **In dung sai ≠ dung sai so.** Dung sai VND `617.285` in `617,29` *(làm tròn — luật in)* nhưng so bằng `61728` xu *(sàn — luật cửa ghi)*. Người đọc thấy *"lệch 617,29 · dung sai 617,29 · ⛔ lệch quá dung sai"* — đúng về tiền, khó hiểu về chữ. Hôm nay chỉ xảy ra khi `0,5% × tiền bank` có ≥ 3 chữ số lẻ **và** lệch rơi đúng khe 1 xu ấy.
5. ⛔ **`AC-7` ⛔ đạt ở bảng danh sách lệnh** *(`HOI-026`)*; ⛔ đo Chrome: bảng hàng chờ `F01` ②, lưới `F01L`, bảng `F03` *(chỉ đo DOM)*; đo `F02` trên dòng V của kho TEST *(⛔ sổ thật)*.
6. ⚠ **"Tổng chùm `2.000,00 USD` + khớp" của `AC-3` là ca U ĐẢO CHIỀU.** Ca U của `KQ-021` là *một dòng tiền ↔ hai lệnh* — `ve_tong_chum` chỉ vẽ khi *một lệnh ↔ ≥ 2 dòng tiền*, nên trên ca U nguyên văn nó **⛔ hiện**. Tôi thử ở bài DOM với lệnh `2000.00` ← hai giao dịch `1234.56` + `765.44`; ⛔ dựng qua cửa thật *(cửa ghép tay chặn N dòng tiền → 1 lệnh vì Σ lệch)*.
7. ⚠ Thẻ lệnh + rail trong bài `AC-3` đọc từ **khuôn `F01G.ST.dong` do bài dựng** *(chỉ thân `/chum` là cửa thật)*; trên Chrome 8099 thẻ / rail đến từ **cửa thật** `/queue/lenh-da-gan` và in đúng `2.259.942,94 USD`.
8. ⚠ `ve_tong_chum` giữ `TP.xu(x) || 0`: một `amount` ⛔ đọc được tính như **0** *(y như `Number(x) || 0` cũ)* ⇒ có thể in *"khớp"* sai nếu cửa trả rác. ⛔ đổi — ngoài phạm vi, nhưng là chỗ nên siết *(như hộp `F01` đã làm: "⛔ không tính được")*.
9. ⚠ `AC-5` đo **khứ hồi** *(in rồi đọc lại = kho)* — nó ⛔ bắt lỗi **thiếu `,00`** *(`1.234` đọc lại vẫn = `1234.00`)*; chỗ ấy chỉ `AC-1` + `AC-6` canh.
