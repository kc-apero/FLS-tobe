# BG-024 — bàn giao `WO-018` *(nhật ký `value_source` = lớp của chính dòng)*

| | |
|---|---|
| **Thuộc** | [`WO-018`](WO-018-nhat-ky-value-source-la-lop-cua-dong.md) vòng 1 *(từ `HOI-016` ⓑ · `TL-016`)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 khuya |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`25f4b91`** *(mã + bài + hiện vật + changelog `03_Dev` + `WO` nhận)* — **đã đẩy**. Phiếu này + `WO` `CHO_TEST` + nhật ký §5 + `README` ở commit kế tiếp *(chỉ giấy)* |
| **Spec** | `BA-05` **v0.34** `DD-I15 ⓓe` *(`05_DATA_DICTIONARY_ERD.md:852`)* · `BA-06` đang **v4.11** — dòng *"F02 · nhật ký"* *(`06_SCREEN_SPEC.md:1261`)* chỉ mang dấu `v4.8`/`v4.9` *(đếm: `v4.8` ×1 · `v4.9` ×2 · `v4.10`/`v4.11` ×0)* ⇒ chữ spec `WO` trỏ tới ⛔ đổi ⇒ ⛔ `HOI` |

## Cổng vào
| Kiểm | Đo | |
|---|---|---|
| git thật | `HEAD` = `origin/feat/p2-oracle-parity` = `b065794` *(`git rev-parse` cả hai)* | ✅ |
| version hợp đồng | `BA-05` v0.34 = `WO`; `BA-06` v4.11 ≠ v4.9 của `WO` nhưng v4.10/v4.11 ⛔ chạm dòng nhật ký *(trên)* | ✅ |
| run id | `WO` ⛔ nói "đã chạy" | — |
| `WO` đủ trường `10` §3.1 | Vì sao · Căn cứ · Spec · Phạm vi TRONG/NGOÀI · AC đo được + chiều ĐỎ · Màn hình 5 trạng thái · Dữ liệu *(ghi kho thật **KHONG**)* · Câu treo *(⛔)* · Rủi ro | ✅ ⇒ ⛔ `HOI` |
| nền `kiem_so_song` lúc nhận *(trên `b065794`, trước dòng mã đầu tiên)* | `⛔ CONG SO SONG KHONG DAT — 34 lech/khong-do-duoc` | ✅ đã chụp |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/ghi_tay.py` `_them` | **`T1`** — cửa ghi duy nhất cưỡng chế bất biến: `value_source` **bỏ trống ⇒ lấy `nguon`**; truyền **≠ `nguon` ⇒ `LoiGhi`**, **0** dòng ở cả hai bảng *(phép so đứng trước `INSERT`)*. ⭐ **Cách chọn** *(`WO` cho Dev chọn)*: **giữ tham số + NO**, ⛔ bỏ tham số — vì bài nghiệm thu `tests/nghiem_thu/test_kq007_bo_ghep_moi_lop_pha_them.py:175` gọi `gt._them(value_source="sua_tay", nguon="sua_tay")` để dựng hình dạng lối ghi cũ *(bỏ tham số ⇒ `TypeError`, mà `tests/nghiem_thu/` ⛔ sửa được)*; và một chỗ gọi truyền **hai giá trị khác nhau** là dấu người gọi đang nghĩ theo nghĩa cũ ⇒ nổ to tốt hơn ghi im |
| `fls/repo/ghi_tay.py` `ghi_but_toan` | **`T2`** — nhật ký cú gõ người ghi `nguon=NGUON_TAY` ⇒ `value_source='sua_tay'`. Thân trả `KetQuaGhi.value_source` **giữ** `t["value_source"]` *(nguồn trước khi gõ — `US-025`)* |
| `fls/repo/ghi_tay.py` `dao_but_toan` | **`T3`** — đọc kèm `nguon` của dòng bị đảo, bản đảo ghi `nguon=lop` *(⇒ `value_source` cùng)*; trước: cứng `NGUON_TAY`. `KetQuaGhi.value_source` của cửa đảo = `lop` *(cửa `/reverse` ⛔ trả trường này — `xu_ly.py:251`, thân cửa ⛔ đổi)* |
| `fls/repo/ghi_tay.py` khối `NGUON_*` | chú thích: bốn mã là câu của `truoc_khi_go`/thân trả; nhật ký mới chỉ mang `sua_tay`/`may_goi_y` |
| `fls/db/schema.py:180` | **`T4`** — chú thích cột `"nguon goi y luc go"` ⇒ *"lop cua chinh dong: sua_tay = NGUOI · may_goi_y = MAY; = fls_adjustment.nguon cung giao dich (DD-I15 ⓓe)"* + khối chú thích vì sao. ⛔ DDL *(chú thích ⛔ vào `COMMENT ON` — golden ⛔ đổi, `pg_verify` khớp)* |
| `docs/ITL/02_BA/Artifacts/Ban-do-Kien-truc-7-Tang.html` | **sinh lại** bằng `tools/sinh_ban_do_tang.py` *(1 dòng: chú thích cột trên)*. `erd_export --write` / `sync_erd_doc` / `--update-golden` chạy: **⛔ đổi** byte nào |
| `tools/demo_dong.py:884` | **`T4`** — log nhật ký in `value_source='sua_tay'`; thêm một dòng log thân trả `/adjust` mang `nguon`/`UNMAPPED` |
| `tests/repo/test_wo018_bat_bien_cap_nhat_ky_pg.py` *(mới)* | **3** bài — `AC-3` đa tập cặp · bản đảo mang lớp dòng bị đảo · `_them` NO khi lệch |
| `tests/web/test_wo018_nhat_ky_nguoi_sua_pg.py` *(mới)* | **2** bài — `AC-1` qua HTTP thật trên kho TEST ⇒ màn `F02` ⑦ |
| `tests/repo/test_ghi_tay_pg.py` | **`T5`** — 1 `assert` + 1 docstring *(dưới)* |
| `tests/web/test_vong_f02_pg.py` | **`T5`** — 1 `assert` |
| `tests/web/test_wo008_than_that_bo_ghep_pg.py` | **`T5`** — 2 `assert` *(`AC-2`)* |
| `docs/ITL/03_Dev/04_DB_IMPLEMENTATION.md` | **v1.16 → v1.17**: dòng `fls_journal` + changelog |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | dòng `WO-018` |

### `T5` — từng `assert` đã đổi *(`tệp:dòng · cũ → mới`)*
| Tệp:dòng | Cũ | Mới | Lo gốc giữ |
|---|---|---|---|
| `tests/repo/test_ghi_tay_pg.py:136→143` | `d["value_source"] == gt.NGUON_TRONG   # cdt1 rong ca ba nguon` | `d["value_source"] == gt.NGUON_TAY` | nhật ký đủ 7 trường, `value_source` ⛔ rỗng |
| `tests/repo/test_ghi_tay_pg.py:168` *(docstring, ⛔ assert)* | *"nhat ky noi thang UNMAPPED"* | *"cua noi thang UNMAPPED"* + đoạn `WO-018` | `assert k.value_source == gt.NGUON_TRONG` **⛔ đổi** — nó canh thân trả |
| `tests/web/test_vong_f02_pg.py:237→242` | `rows[0]["value_source"] == "nguon"` | `rows[0]["value_source"] == "sua_tay"` | `value_before == "HD-SO-GOC"` *(giá trị cũ đọc lại được)* ⛔ đổi |
| `tests/web/test_wo008_than_that_bo_ghep_pg.py:107→112` | `[(h[3], h[5]) for h in nguoi] == [("HD-K7B", "UNMAPPED")]` | `== [("HD-K7B", NHAN_NGUOI)]` | hàng người in **giá trị người**, ⛔ "gợi ý:", ⛔ nhãn máy |
| `tests/web/test_wo008_than_that_bo_ghep_pg.py:108→113` | `NHAN_NGUOI not in {h[5] for h in hang}` | `[h[5] for h in hang].count(NHAN_NGUOI) == 1` | đổi chiều đúng như `WO` `AC-2` *"nhãn người sửa xuất hiện đúng 1 lần"*; số hàng *"rút gợi ý"* = số bản đảo *(≥ 4)* ⛔ đổi |

## Chứng minh ĐỎ *(`Đ5`)* — `scratchpad/dot_bien.py`: sửa `ghi_tay.py` thật → chạy 6 tệp bài → chép trả *(nội dung trả **trùng byte**, `assert` trong kịch bản)*
| Đột biến | Kết quả nguyên văn |
|---|---|
| **M0** — mã **trước `WO-018`** *(`git show b065794:fls/repo/ghi_tay.py`)* | `8 failed, 76 passed` — **5/5** bài mới + **3/3** `assert` `T5` *(`test_AC3_da_tap…` · `test_AC3_ban_dao…` · `test_them_NO…` · `test_AC1_cu_go…` · `test_AC1_man_F02…` · `test_AC2_nhat_ky_THAT…` · `test_force_KEM_ly_do…` · `test_nhat_ky_du_BAY_truong`)* |
| **M1** — `ghi_but_toan` trả `value_source=t["value_source"]` + bỏ phép so `_them` *(chiều ĐỎ của `AC-1`/`AC-2`/`AC-3`)* | `7 failed, 77 passed` — `AC-3` đa tập · `_them NO` · `AC-1` ×2 · `AC-2` · `test_force_KEM…` · `test_nhat_ky_du_BAY…` |
| **M2** — `dao_but_toan` ghi cứng `NGUON_TAY` *(chiều ĐỎ thứ hai của `AC-3`)* | `1 failed, 83 passed` — `test_AC3_ban_dao_mang_NGUON_cua_dong_bi_dao…` |
| **M3** — bỏ phép so `value_source ≠ nguon` trong `_them` | `1 failed, 83 passed` — `test_them_NO_khi_value_source_KHAC_nguon…` |
| **M4** — thân trả `/adjust` đổi thành `NGUON_TAY` *(chiều ĐỎ `AC-4`)* | `4 failed, 80 passed` — `test_cua_ghi_pg.py::test_go_mot_truong_va_no_ra_o_LAN_DOC_SAU` *(`:241`)* · `test_ghi_tay_pg` ×2 · `test_AC1_cu_go…` |

Lý do đỏ đúng chỗ *(M0, nguyên văn)*: `AC-3` — *"chỉ ở nhật ký: (…'UNMAPPED'), (…'nguon'), (…'may_goi_y'), (…'UNMAPPED') · chỉ ở bút toán: (…'sua_tay') ×4"*; bản đảo — `(51, 39, 'hd', 'sua_tay', 'may_goi_y', 'sua_tay', True)`; `AC-1` màn — `['…', 'hd', 'HD-MAY', 'gợi ý: HD-NGUOI', 'lan@apero.vn', 'máy gợi ý · không đổi Final', …]` *(đúng ca xấu `HOI-016`)*.

## Cổng *(kết quả nguyên văn, trên cây = `25f4b91`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `2132 passed, 3 xfailed in 305.31s (0:05:05)` — 3 `xfail` = 3 `xfail(strict)` có sẵn của `fls-test` *(`kq021`, chờ `WO-022`/`WO-023`)*; **⛔ XPASS**; bài mới ⛔ `xfail` |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 43 lech/khong-do-duoc` — **nền 34** *(lúc nhận)* + **9** loại (c) **mới** của phiếu: `roadmap · DEV-04 version` `1.16→1.17` · `master · §8 version DEV-04` `1.16→1.17` *(bump `04_DB`)* · `bản vẽ · thanh repo` `568→571` · `bảng tiến độ · repo` ×2 `7.150→7.194`/`568→571` · `bảng tiến độ · db` `1.906→1.915` · `bản vẽ · caption khối 1 (db)` · `caption khối 6 (repo)` ×2 *(dòng `schema.py`/`ghi_tay.py` + bài mới)*. 22 mục nền khác **giữ nhóm**, chỉ số trôi *(bài `2130→2135`, dòng `25.373→25.426`, web `477→479`)*. ⛔ `dong_bo --ghi` *(`10 §6 ⓒ`)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (113 file, 1322 bang, 656 o ngay, 104 ma QD), khong chi 'khong thay loi'` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech   (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` *(chú thích `schema.py`)* | `khong co gi de ap` · `pg_verify: khop` |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-1** | `tests/web/test_wo018_nhat_ky_nguoi_sua_pg.py` — dòng `hd_thyt='HD-MAY'` *(fixture `du_lieu["may"]` của `test_vong_f02_pg`)*, `POST /ledger/{id}/adjust {hd: HD-NGUOI, force, reason}` qua HTTP thật trên kho TEST ⇒ ⓐ `test_AC1_cu_go…`: nhật ký trước **0** dòng, sau **đúng 1** `('hd', 'HD-NGUOI', 'sua_tay')`; thân trả `value_source='may_goi_y'` · `value_before='HD-MAY'` *(nghĩa cũ giữ)*; ⓑ `test_AC1_man_F02…`: thân `GET /journal` thật ⇒ màn: **1** hàng `('hd', 'HD-NGUOI', 'người sửa')`, **0** hàng chứa *"gợi ý: HD-NGUOI"*, **0** nhãn máy. Đỏ ở M0/M1 |
| **AC-2** | `test_wo008_than_that_bo_ghep_pg.py::test_AC2…` *(diff ở bảng `T5`)* — hàng người `("HD-K7B", "người sửa")`; *"rút gợi ý"* = số bản đảo *(`so_dao >= 4`, assert ⛔ đổi)*; nhãn *"người sửa"* **đúng 1** lần. Đỏ ở M0/M1 |
| **AC-3** | `tests/repo/test_wo018_bat_bien_cap_nhat_ky_pg.py` — kịch bản đủ đường ghi: ① ghép tay `ghep_lenh` *(→ `ghi_goi_y`, actor người)* + lớp máy `ghi_goi_y_may` + **`dao_but_toan` một dòng `may_goi_y`** + `bo_moi_noi`; ② `ghi_but_toan` ô **rỗng** + **`dao_but_toan` dòng `sua_tay`**; ③ ô có **nguồn sổ**; ④ ô có **`*_thyt`**; ⑤ ô **đã có người**. In nguyên văn: `mẫu số: 14 cặp bút toán ⇔ 14 dòng nhật ký trên 5 dòng sổ` *(8 · 2 · 1 · 1 · 2)*; bản đảo theo *(lớp dòng gốc, qua cửa đảo)*: `{('may_goi_y', True): 1, ('may_goi_y', False): 3, ('sua_tay', True): 1}`. So **đa tập** `Counter` *(⛔ nối khoá)*: lệch **0**. ⚠ Bài thứ hai *(bản đảo mang `nguon` dòng gốc)* có vì chiều ĐỎ *"giữ `NGUON_TAY` cứng ⇒ cặp lệch"* của `WO` **⛔ đúng nguyên văn**: mã cũ ghi `sua_tay` ở **cả hai** bảng ⇒ cặp vẫn bằng — M2 chỉ bài thứ hai bắt *(xem "còn yếu")* |
| **AC-4** | `pytest tests/api/test_cua_ghi_pg.py` xanh *(trong lượt toàn bộ)*; `git diff b065794 -- tests/api/test_cua_ghi_pg.py` **rỗng** *(0 dòng)*. M4 đỏ `:241`. ⚠ `:292` **⛔ đỏ** ở M4 — nó là cửa `before-edit` *(`GET …/fields/hd` → `truoc_khi_go`)*, ⛔ đi qua `KetQuaGhi`; muốn nó đỏ phải phá `truoc_khi_go`, ngoài `T2` |
| **AC-5** | Kho THẬT, chỉ `SELECT` qua `noi_chi_doc(dsn_that())`, chạy **trước** mã và **sau** `pytest` — hai lần ra **y hệt**: <br>`SELECT count(*), count(a.adj_id), count(*) FILTER (WHERE a.nguon = j.value_source) FROM fls_journal j LEFT JOIN fls_adjustment a ON a.itl_id = j.itl_id AND a.field = j.field AND a.at = j.at AND a.actor = j.actor` ⇒ `(4428, 4428, 4428)` <br>khoá `(itl_id, field, at, actor)` trùng trên `fls_adjustment` ⇒ `0` · đa tập hai chiều `EXCEPT ALL` ⇒ `0` <br>`SELECT value_source, count(*) FROM fls_journal GROUP BY 1` ⇒ `('may_goi_y', 4424)` · `('sua_tay', 4)` <br>`fls_adjustment` theo `(nguon, là bản đảo)` ⇒ `('may_goi_y', False, 4424)` · `('sua_tay', False, 2)` · `('sua_tay', True, 2)` · `max(fls_journal.at)` = `2026-10-01 09:06:40 UTC` ⇒ ⛔ dòng mới, ⛔ dòng `/adjust` nào |
| **AC-6** | `pytest` `2132 passed, 3 xfailed` *(3 = `xfail(strict)` có sẵn của Test, ⛔ của phiếu)* · `lint-imports` `9 kept, 0 broken` · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh *(trong lượt toàn bộ)* · `git diff b065794 -- tests/nghiem_thu/ fls/web/` **rỗng** · `kiem_so_song` nền **34** ⟷ sau **43** = +**9** loại (c) *(liệt kê ở mục Cổng)* · ⛔ `dong_bo --ghi` |

## Kho thật
- **`KHONG_CHAM`** — chỉ `SELECT` *(AC-5)*. `FLS_CHO_GHI_THAT` ⛔ đặt. Mọi bài chạy `dsn_test()`.

## Cách chạy để xem *(màn ⛔ đổi mã; chữ đổi vì dữ liệu)*
- ⛔ dựng máy trong lượt này *(8088 chỉ đọc đang chạy; sổ thật **0** dòng `/adjust` ⇒ 8088 ⛔ có gì mới để xem)*. Muốn xem `F02` ⑦ đổi: `tools/chay_cua.py --cho-web --cho-ghi` trên **kho TEST** cổng **8099**, gõ một ô `hd` có `hd_thyt` *(dòng kiểu `du_lieu["may"]`)* với `force`, mở nhật ký ⇒ hàng ấy in *"người sửa"*; tắt máy sau khi xem.

## Dev tự thấy còn yếu
1. **Kho TEST còn dòng nghĩa cũ.** Nhật ký `/adjust` ghi trước `25f4b91` trên kho TEST mang `UNMAPPED`/`nguon`/`may_goi_y` — cột hai nghĩa **theo thời gian** ở đó *(sổ thật **0** — AC-5)*. ⛔ `CHECK` *(NGOÀI phạm vi)* ⇒ ⛔ gì ngăn một đường ghi **ngoài `_them`** ghi lại nghĩa cũ ngoài bài quét mã đã có *(`tests/repo/test_chi_mot_cho_ghi_tay.py` — `INSERT INTO fls_journal` chỉ trong `ghi_tay.py`)*; trong `ghi_tay.py` thì `_them` NO.
2. **`AC-3` chiều ĐỎ của `WO` cho `dao_but_toan` ⛔ đúng nguyên văn.** *"Giữ `NGUON_TAY` cứng ⇒ cặp của bản đảo dòng máy lệch"* — sai: mã cũ ghi `sua_tay` ở **cả** `fls_adjustment.nguon` **và** `value_source` ⇒ cặp **bằng**. Lỗi thật là **cặp đúng nhưng cả hai sai lớp**. Tôi thêm bài thứ hai *(bản đảo mang `nguon` dòng gốc)* để bắt — Test soi xem bài ấy có đúng ý `ⓓe` *"Bản đảo ⇒ lớp của dòng bị đảo"* không, và có nên ghi lại chiều ĐỎ trong `WO`.
3. **`AC-4` chiều ĐỎ chỉ đúng một nửa** — đổi `KetQuaGhi.value_source` chỉ làm đỏ `:241`; `:292` là cửa `before-edit`, ⛔ chạm. Hai bài vẫn **xanh ⛔ sửa chữ nào** *(phần "mong" của AC-4 đạt)*.
4. **`dao_but_toan` đảo dòng máy giờ ghi bản đảo `nguon='may_goi_y'`** — đúng `ⓓe`, nhưng **chưa ai đo** màn `F02` ⑦ cho bản đảo **qua cửa `/reverse`** *(bài màn chỉ có bản đảo của `bo_moi_noi`)*. Màn đọc theo `value_source` ⇒ sẽ in *"rút gợi ý"* *(như bản đảo bỏ ghép)*; trước đây in *"người sửa"* + ô trống. Sổ thật **0** bản đảo qua đường này. Ai được đảo dòng máy qua `/reverse` là luật `SM-I03` *(NGOÀI)*.
5. **`KetQuaGhi.value_source` của `dao_but_toan` đổi** `sua_tay` → lớp dòng gốc. Cửa `/reverse` ⛔ trả trường này *(`xu_ly.py:251`)* ⇒ thân cửa ⛔ đổi; nhưng gọi trực tiếp tầng repo sẽ thấy khác. `grep` `tests/` + `fls/` + `tools/`: **0** chỗ đọc `.value_source` của kết quả `dao_but_toan`.
6. **9 lệch mới `kiem_so_song`** là loại (c) của chính phiếu *(gồm 2 do bump `04_DB` v1.17)* — để `fls-ba`/phiên `dong_bo --ghi` sau; ⛔ chạy ở đây theo `AC-6`.
