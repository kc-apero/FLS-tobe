# KQ-010 — biên bản kiểm `BG-009` *(`WO-001`: thước mốc `B` ⛔ đếm máy + UAT · dấu sổ · `khop_owner` · `dong_bo --ghi`)*

| | |
|---|---|
| **Thuộc** | `BG-009` · `WO-001` *(vòng 1)* |
| **Kiểm bởi** | `fls-test` · 2026-10-01 tối · nhánh `feat/p2-oracle-parity` @ `d8b799e` *(mã + tài liệu `6e98796`; `HEAD` = `origin` — đã đẩy)* |
| **Phán quyết** | ✅ **ĐẠT** — **9/9** AC *(`AC-1`…`AC-7`, `AC-1b`, `AC-2b`)* đạt; ba lăng kính ⛔ còn `CHAN`/`NANG`. Bốn phát hiện **`NHE`**: `F-1` gửi `DEV` *(đã lấp bằng bài nghiệm thu, ⛔ cần sửa mã)* · `F-2`, `F-3` gửi `BA` *(phát `WO` cho `DEV`)* · `F-4` gửi `BA` *(câu văn)* |
| **Trạng thái** | ✅ **`DONG`** *(02/10 trưa, `fls-test` — [`KQ-014`](KQ-014-kiem-bg-013.md): `F-2`+`F-3` xử ở `WO-011` @ `88ab178`, ĐẠT; `F-1` đã lấp bằng bài `kq010`; `F-4` `BA` đã sửa câu)* · ~~`MO` — chờ `BA` *(nghiệm thu PO `WO-001`; rà bảng câu cạnh số `10 §6 ⓑ`; `F-2`…`F-4`)*~~ |

> **Một câu cho owner:** con số *"mốc B"* nay nói thật — **`1` đạt · `1` một nửa · `3` chưa**, vì **chưa một kế toán nào bấm thật** trên sổ. Tôi đã thử cả ba chiều trên kho thử bằng chính các nút ghi của hệ: một **người** bấm `Gán` mà ⛔ gõ lý do ⇒ mốc B **nhích** lên `4 · 1 · 0`, bỏ ghép ⇒ `5 · 0 · 0`; **máy** tự ghép ⇒ **đứng yên**; dòng **UAT** ghép rồi bỏ ⇒ **đứng yên**. Sổ thật **⛔ bị chạm**. Còn bốn chỗ nhỏ — hai chỗ thước sẽ **lại** sai khi có tiến trình máy mới hoặc khi nhịp chụp chạy tiếp, và vài câu cũ trong bản vẽ chưa ai sửa.

```mermaid
flowchart LR
  subgraph KHO_TEST["Kho THỬ — ghi bằng chính cửa ghi của hệ"]
    N["Người bấm Gán<br/>(⛔ gõ lý do ⇒ '(may dien) …')"] --> C{"câu SQL<br/>của cổng"}
    M["Máy tự ghép<br/>(actor may@fls)"] --> C
    U["UAT ghép + bỏ<br/>(lý do 'UAT 02/10 …')"] --> C
  end
  C -- "người: +1" --> B1["mốc B 1·1·3 ⇒ 4·1·0<br/>bỏ ghép ⇒ 5·0·0"]
  C -- "máy: +0" --> B2["mốc B đứng 1·1·3"]
  C -- "UAT: +0" --> B3["mốc B đứng 1·1·3"]
  T[("Sổ THẬT — chỉ SELECT<br/>người thật = 0")] --> R["1 · 1 · 3<br/>khớp máy in"]
```

## Cổng chạy lại *(Test tự chạy, `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`, `PYTHONUTF8=1`, tuần tự)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| Cổng vào: git | `6e98796` mã · phiếu ở commit kế | `HEAD` = `origin/feat/p2-oracle-parity` = **`d8b799e`**; `git show --stat 6e98796` = **11** tệp đúng bảng *Đã đổi*; `git diff 5d627c0 6e98796 -- tests/nghiem_thu/` **rỗng** | ✅ |
| Cổng vào: version spec | `WO-001` · `10` **v1.1** · `BA-11` **v0.15** · `Ra-soat` v1.1 | `10_HOP_DONG_AGENT` v1.1 · `BA-11` v0.15 *(chỉ thêm `INV-I22`)* — khớp `WO` | ✅ |
| `python -m pytest` *(@ `d8b799e`, trước khi tôi gỡ dấu)* | `1 failed, 1957 passed` — failed = `XPASS(strict)` bài `KQ-002` | **`1 failed, 1957 passed in 271.62s`** — `FAILED tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay` · `[XPASS(strict)]` | ✅ |
| `python -m pytest` *(sau `KQ-010`: gỡ dấu + 5 bài mới)* | — | **`1963 passed`** *(= 1.958 + 5; ⛔ `xfail` nào còn trong cả bộ)* — số giờ chạy ở dòng §5 dashboard | ✅ |
| `python tools/kiem_so_song.py` @ `d8b799e` | `1` lệch *(`97` vs `98` tệp — chính `BG-009`)* | **`⛔ CONG SO SONG KHONG DAT — 1 lech`**: `master · §8 số file + hiện vật: tài liệu ghi 97 · MÁY đo 98` — đúng một nhóm ấy; mốc B ×3 · dấu sổ · mọi nhóm ảnh **OK** *(nhịp ⛔ chụp ảnh PM mới từ 18:20 ⇒ ⛔ trôi)* | ✅ |
| `kiem_so_song` @ `6e98796` *(worktree, ⛔ repo)* | `0` lệch | **`✅ cong so song DAT — 109 phep so`** | ✅ |
| `kiem_so_song` @ `ee390cb` *(worktree — nền `AC-5`)* | `84` | **`⛔ … 84 lech/khong-do-duoc`**; mốc B ở cả 3 nơi *"tài liệu `4` · MÁY `5`"* = `5·0·0` của `KQ-002 K15` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `97 file` | `✅ cong tai lieu DAT — … (98 file, 1193 bang, 635 o ngay, 104 ma QD)` *(98 = +`BG-009`)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `17/20 khop · 3 lech` · `C1` ĐẠT | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT` | ✅ |
| `python tools/soi_bang_tuyen.py` | `40` tuyến | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | `✅ CONG THUYET MINH DAT — 31/31 nut` | ✅ |
| `.venv/Scripts/lint-imports.exe` | `9 kept, 0 broken` | `Contracts: 9 kept, 0 broken.` | ✅ |
| `python -m fls.db.pg_migrate` | ⛔ chưa chạy *(⛔ chạm schema)* | ⛔ **⛔ chạy bản ghi** *(áp lên kho thật — cấm ghi)*. `--status`: mới nhất `0026_dien_giai_sao_ke` đã áp · `python -m fls.db.pg_verify`: **`khop: 25 bang/view`** | ✅ |

⚠ Sau commit của chính `KQ-010` *(+1 tệp `KQ-010`, +1 tệp bài, +5 phép thử)* `kiem_so_song` sẽ đỏ thêm ở nhóm **số tệp** + **số phép thử** — loại **b/c**, do phiếu kiểm, ⛔ hồi quy của `WO-001`. **Đo trên cây có `KQ-010` *(trước commit)*: `8` lệch** — `1958 → 1963` ×6 nhóm phép thử · `216 → 221` *(bài trong module)* · `97 → 99` tệp; `kiem_tai_lieu` `99 file` ✅. ⛔ Nhóm nào của mốc B / dấu sổ / kho. ⛔ Tôi ⛔ chạy `--ghi` *(cấm — `10 §6 ⓒ`)*.

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** | sau `T1a`: `su_kien_cho_nguoi` = `2` *(chỉ UAT)*; `2.219` sự kiện `may@fls` đóng `0` cổng | **Sổ thật, SQL độc lập** *(⛔ đọc mã cổng)*: sự kiện `evt_type <> 'reason'` = **2.221** *(mẫu số ≠ 0)* · trong đó `actor = 'may@fls'` **2.219** *(`match`, 18/09 09:07)* ⇒ chỉ vạch máy còn **`2`** *(`match` + `unmatch` của `khanhcq@apero.vn`, cả 2 lý do bắt đầu `UAT `)* ⇒ đúng số `AC-1` dù Dev làm `T1a`+`T1b` một câu *(yếu điểm 3)*. Chiều ĐỎ: đột biến `M1` *(bỏ vạch actor)* ⇒ **4** bài đỏ *(3 Dev + `KQ-002`)* + bài `kq010` máy đỏ; `M7` *(hằng `'may@fls2'` lệch `MAY`)* ⇒ cùng 4 bài đỏ *(gồm `test_T1a_cau_SQL_mang_DUNG_hang_MAY`)* | ✅ ĐẠT |
| **AC-2** | mốc B **`1 · 1 · 3`**, khớp bảng `09` | `kiem_so_song` @ `d8b799e`: `OK dashboard · cổng mốc B` · `OK mốc · cổng mốc B` · `OK bản vẽ 13 · tổng kết cổng mốc B` *(tài liệu ghi `1·1·3`)*. **Đếm tay độc lập**: người thật *(actor ≠ `may@fls` **và** lý do ⛔ bắt đầu `UAT `)* = **0** / **110.349** sự kiện ⇒ `B2`·`B3`·`B5` chưa; bỏ ghép người = **0** / **1** `fls_pm_unlink` *(chính `unlink 163568` UAT)* ⇒ `B4` một nửa; `fls_pm_line` **249.288** > 0 ⇒ `B1` đạt ⇒ **`1·1·3`** = máy. Chiều ĐỎ *(kho TEST, cửa ghi thật)*: người `Gán` ⇒ `4·1·0` ✅ | ✅ ĐẠT |
| **AC-3** | dấu sổ = `10/09 HH:MM` | `kiem_so_song`: `OK kho · DẤU THỜI ĐIỂM bản sao sổ`; sổ thật: lượt có dòng `fls_itl` mới nhất = `NAP-2026-09-10-BU1` **10/09 18:54:50** *(1.770 dòng)*; lượt mới nhất bất kỳ = `NAP-2026-10-01-PM3448C611` 01/10 18:20 *(0 dòng sổ)* ⇒ dấu cũ sai, dấu mới đúng. `banve:1078` in *"bản sao nạp 10/09 18:54"*. Chiều ĐỎ: `M6` *(trả `_Q_GIO` câu cũ)* ⇒ `test_T2_dau_SO…` đỏ | ✅ ĐẠT |
| **AC-1b** | bài `KQ-002` xanh, ⛔ dòng nào đổi | `git diff 5d627c0 6e98796 -- tests/nghiem_thu/` **rỗng**; `--runxfail` ⇒ xanh; chạy thường ⇒ **1** `XPASS(strict)`. Chiều ĐỎ: bài ấy **đỏ** trên `tools/kiem_so_song.py` của `ee390cb` *(worktree)*. ⇒ **gỡ dấu** — mục *Bài thử mới* | ✅ ĐẠT |
| **AC-4** | chỉ đỏ đúng 1 `XPASS(strict)`; lint `9/0`; số bài tăng đúng | `1 failed, 1957 passed` *(1.958 = nền 1.949 + 9 bài Dev ở `tests/test_kiem_so_song.py` — `git diff --stat` chỉ một tệp `tests/`)*; lint `9 kept, 0 broken` | ✅ ĐẠT |
| **AC-5** | `BG` phân loại nhóm đỏ a/b/c | `BG` bảng `AC-5`: 17 + 7 + 16 + 2 + 5 + 1 = **48** nhóm / **84** giá trị — tôi đo lại nền @ `ee390cb`: **84** ✅. Phân loại đọc tay *(Dev tự khai, yếu điểm 7)* — tôi ⛔ chia lại, ⛔ thấy nhóm nào xếp sai loại | ✅ ĐẠT |
| **AC-2b** | lọc UAT, ⛔ lọc `(may dien)` | Bài Dev `test_T1b_ly_do_MAC_DINH_may_dien_van_la_NGUOI` *(khuôn CTE)* + ⭐ bài `kq010` ① ghi bằng **chính** `ghep_lenh(reason=None)` ⇒ `reason` thật trong kho bắt đầu `(may dien)` ⇒ đếm **1**. Chiều ĐỎ: `D3` của Dev; lọc theo actor ở `B4` *(`M4`)* — xem `F-1` | ✅ ĐẠT |
| **AC-6** | `B5` đo `BA-06`, `C5` tách, `mong` kèm xuất xứ, `C1` ĐẠT | `✅ B5 … (`06_SCREEN_SPEC.md`)` · `⛔ C5 cột memo` *(mong LỆCH)* · `✅ C5b khung xem` *(8.366/8.387)*; ba `mong` mới đều có câu xuất xứ *(`R-5`, `R-6`, `QĐ-ITL-145`)*. **Chiều ĐỎ** *(worktree)*: `K1` `TEP_B5` ⇒ tệp BIA `12` ⇒ **`16/20 · ⛔ CONG NO`**, mã `1` · `K2` tệp ⛔ tồn tại ⇒ `LoiDo`, **`16/19 (da do 19/20)` · ⛔ CONG NO** *(⛔ "0 lần" xanh)* · `K3` `C5b` `mong` ⇒ `False` ⇒ ⛔ CONG NO. Trả nguyên: byte trùng ×3 | ✅ ĐẠT |
| **AC-7** | `--ghi` xong `kiem_so_song` 0 lệch; mốc B ở `09`, dash §1, bản vẽ 13 = `1·1·3` kèm câu đúng nghĩa | @ `6e98796` **0** lệch *(đo lại, worktree)*; ba chỗ in `1 · 1 · 3` kèm *"thước sửa, ⛔ việc lùi"* *(`09:149`, `dash:121`, `banve:1367`–`1374`)*; mỗi chỗ nói **người thật = 0** *(`09`: "⛔ chưa ai bấm"; dash: "sự kiện người thật = 0"; bản vẽ: UAT "chưa phải việc của kế toán")* ⇒ đúng nghĩa *"chưa kế toán nào bấm thật"*. Câu từng chỗ — mục *Tài liệu* | ✅ ĐẠT |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec `WO-001` · `QĐ-ITL-150 ⓐ` · `10 §6`)* | ✅ **ĐẠT** — ba vạch đúng luật; ⛔ loại nhầm người thật; `B4` ⛔ đếm bỏ ghép UAT; dấu sổ đọc lượt nạp sổ. Hai lỗ **bài thử** *(⛔ lỗ mã)* đã lấp — `F-1` | **Diff `6e98796`** `su_kien_cho_nguoi`: `evt_type <> 'reason' and actor is distinct from 'may@fls' and left(coalesce(reason,''),4) <> 'UAT '` — ⓐ hằng máy **khớp** `fls/repo/may_ghep.py:51` *(`_kiem_hang_may` nổ nếu lệch — `M7` bị bắt)*; ⓑ UAT lọc **lý do ở đầu**, ⛔ actor, ⛔ `'(%'`, ⛔ `'%UAT%'`; ⓒ `coalesce` giữ cú bấm **`Xong`** của người *(`ghi_tay.danh_dau_xong` ghi `reason = NULL` khi ⛔ gõ — `:1121`)*. `moi_noi_da_bo` = `fls_pm_unlink ⋈ fls_queue_event` qua `evt_id` — `evt_id` **NOT NULL** *(schema)*, sổ thật `0` unlink thiếu sự kiện ⇒ phép nối ⛔ rơi dòng. `_Q_GIO` = lượt `fls_run` có dòng `fls_itl`. **Kịch bản phá trên kho TEST bằng cửa ghi thật** *(bài `kq010`, câu SQL của cổng đọc bằng `ast`, bảng thật thu về dòng của bài)*: ① người `ghep_lenh(reason=None)` ⇒ `(may dien) …` ⇒ người **+1** ⇒ `1·1·3 → 4·1·0`; `bo_moi_noi(reason=None)` ⇒ `5·0·0` · ② `ghi_goi_y_may` ⇒ **+0**, đứng `1·1·3` · ③ UAT ghép + bỏ ⇒ người **+0**, bỏ ghép **+0**, đứng `1·1·3` · ④ owner ghép/bỏ **thật** *(lý do ⛔ `UAT`)* ⇒ `B4` **+1**, người **+2** · ⑤ người `Xong` ⛔ lý do *(`reason NULL`)* ⇒ **+1**. **Biên** *(⛔ chèn)*: `'uat 02/10'` *(chữ thường)*, `' UAT …'` *(khoảng trắng đầu)*, `'UAT02/10'` ⇒ cả ba **tính là người** — chiều cổng **xanh sớm** nếu một lượt UAT sau gõ lệch tiền tố *(`F-2` ⓑ)*. **Đột biến** *(worktree)*: `M1` `M2` `M3` `M6` `M7` bị bài Dev bắt; ⛔ **`M4`** *(`B4` lọc theo actor — đúng chiều `T1b` cấm)* và ⛔ **`M5`** *(bỏ `coalesce`)* **lọt** cả 30 bài Dev + `KQ-002` ⇒ `F-1`; bài `kq010` bắt **cả bảy** *(M1·M2·M3·M4·M5·M7 đỏ; `M6` ngoài phạm vi bài; đối chứng `M8` xanh)* |
| **Dữ liệu** *(kho thật, chỉ `SELECT`)* | ✅ **ĐẠT** — số mốc B máy in = số đếm tay; sổ ⛔ đổi so với `KQ-007` | `fls_itl` **8.387** · `fls_pm_link` **2.263** · `fls_pm_unlink` **1** · `fls_may_goi_y` **4.424** · `fls_sua_tay` **0** · `fls_adjustment` **4.428** · `fls_journal` **4.428** · `fls_queue_event` **110.349** — **8/8** khớp `KQ-007`; `max(evt_id)` **163567** · `max(adj_id)` **163571** · `max(link_id)` **163562** ⇒ ⛔ dòng mới. Sự kiện theo `(evt_type, actor)`: `reason/dung-lai-so@apero.vn` **108.128** · `match/may@fls` **2.219** · `match/khanhcq@apero.vn` **1** *(UAT)* · `unmatch/khanhcq@apero.vn` **1** *(UAT)* — tổng **110.349** ✅. `actor` NULL **0**, `reason` NULL **0**. `fls_journal`: `may_goi_y` **4.424** *(có giá trị)* · `sua_tay` **2 + 2 rỗng** *(UAT `27728`)* — khớp câu `09:218` và `BA-06` v4.8. `fls_pm_line` **249.288** dòng / **66** ảnh — ⛔ ảnh mới từ 18:20 |
| **Màn hình** | — **⛔ áp dụng** | `WO-001` ⛔ chạm màn *(`BG` ⛔ có mục *Cách chạy để xem*)*; máy 8088 ⛔ dựng. Phần **hiện** cho owner là giấy/bản vẽ ⇒ soát ở mục *Tài liệu* |

## Tài liệu — 16 câu cạnh số *(đọc **câu**, ⛔ chỉ số — `11 §6`)*
| Chỗ | Câu đúng chưa? |
|---|---|
| `09:147` tiêu đề + `09:149` đính chính | ✅ `1·1·3`; *"từ 18/09 đến 01/10 … in `4·1·0` (rồi máy đo `5·0·0`)"* đúng `KQ-002 K15` + nền @ `ee390cb` *(máy in `5`)* |
| `09:158` `B2` · `09:324` §7 dòng `B` | ✅ *"người thật = 0 (sau khi loại máy + UAT)"* — đo **0** / 110.349 |
| `09:160` `B4` | ✅ *"`fls_pm_unlink` = 1 — chính cú UAT"* — `unlink 163568` → `evt 163567`, lý do `UAT 01/10 - hoan lai…` |
| `09:163` · `09:167` | ✅ *"2.262 mối nối `lan 1` sinh 10/09"* — sổ thật `2026-09-10 lan 1` **2.262** + `2026-10-01` **1** *(UAT)*; *"vỡ lần nữa 18/09"* ✅ |
| `09:218`–`219` | ✅ `4.424` máy + `4` UAT = 4.428 · `108.128 + 2.219 + 2` = 110.349 — cộng đúng, nhãn đúng |
| `dash:121` | ✅ — mọi vế đo lại khớp |
| `master:325` | ✅ *"hơn 1.400"* = 1.958 − 548 = **1.410** |
| `banve:1367`–`1374` | ✅ số + nghĩa. ⚠ khối mang nhãn *"Đính chính 01/10 (fls-ba, …)"* nay chứa câu của `fls-dev` — `F-4` ⓔ |
| `banve:1400` · `:1410` · `:1436` | ✅ *"nay có nhiều"* · `53,4%` = 3.767 / 7.056 *(bảng trần cứng ngay dưới)* · *"Nhiều ảnh … (số ở thẻ …)"* — trỏ, ⛔ chép |
| `banve:1470` · `:1475` | ✅ `3.820 = 2.219 + 1.601` · *"đo 09/09 … chưa đo lại"* nói thật |

⛔ **Chuỗi `4 đạt` / `4 · 1 · 0` / `5·0·0` ngoài biên bản** *(grep `docs/ITL` + `CLAUDE.md`)*: còn ở `09:149`, `dash:121`, `banve:1370` *(đều là câu **đính chính** nói số cũ — đúng `Đ2`)*, `Ra-soat` + phiếu *(biên bản)* và ⚠ **`dash:542`** *(§6 *Việc tiếp theo*, thì hiện tại: "Mốc B ghi **4 đạt** … phải sửa TRƯỚC khi đồng bộ số")* — câu **khai** đã hết đúng ⇒ `F-4` ⓕ. *(`09:60`/`:357`, `dash:120` là mốc **A** `4·1·1` — ⛔ liên quan.)*

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** | `NHE` | `tests/test_kiem_so_song.py` *(9 bài `T1a`/`T1b`/`T2` của `BG-009`)* | Hai đột biến **lọt** cả 30 bài *(Dev + `KQ-002`)*: `M4` — `moi_noi_da_bo` lọc `e.actor <> 'khanhcq@apero.vn'` thay lý do ⇒ `30 passed` *(khuôn của bài `B4` đặt UAT ở `khanhcq`, người ở `ke-toan` ⇒ ⛔ phân biệt được hai luật)*; `M5` — `reason not like 'UAT %'` *(bỏ `coalesce`)* ⇒ `30 passed`, trong khi `danh_dau_xong` ghi `reason = NULL` ⇒ cú `Xong` của người **rơi im lặng**. **Mã hôm nay đúng** cả hai chiều. ⭐ Đã lấp: `tests/nghiem_thu/test_kq010_moc_b_dem_tren_duong_ghi_that.py` bắt cả hai | `DEV` *(ghi nhận — ⛔ phải sửa; khi đụng câu này lần sau, giữ bài `kq010`)* |
| **F-2** | `NHE` | `tools/kiem_so_song.py:493`–`497`, `:384`–`387` · `10 §6` · `QĐ-ITL-150 ⓐ` | = yếu điểm **1** + **2** của `BG`, đo thật: ⓐ actor máy là **danh sách đen một phần tử** — trong mã còn **`dung-lai-so@apero.vn`** *(`tools/dung_lai_so.py:185`, hôm nay chỉ ghi `reason`)*, **`nhip@fls`** / **`nhip@fls(tay)`** *(`fls/repo/nhip_chup.py:48`/`:63`, hôm nay chỉ ghi `fls_chup`)* — ⛔ cổng nào nói *"actor lạ ghi sự kiện ngoài `reason`"*; ⓑ `B4` **⛔ loại `MAY`** *(bất đối xứng với `B2/3/5`)* — hôm nay chỉ `fls/api/xu_ly.py:470` gọi `bo_moi_noi` nên **0** chạm; ⓒ UAT nhận bằng **chữ**: `'uat …'`, `' UAT …'`, `'UAT02/10'` ⇒ **tính người** *(cổng xanh sớm)*; ⓓ luật *"UAT ⛔ bao giờ là người cho **bất kỳ** cổng"* mới vào **một** câu SQL — `khop_owner` `C8` *(`fls_sua_tay > 0` = "người đã chốt")* và thước `G-d` *(`BA-14:279`, `fls_pm_link.hinh='T'` — sổ thật **1**, chính mối nối UAT)* ⛔ loại UAT; hôm nay `C8` = **0** nên ⛔ sai | `BA` *(khai **sổ actor máy** một chỗ + phép đo "actor lạ"; nói `C8`/`G-d` có theo `QĐ-ITL-150 ⓐ` không) ⇒ `WO` cho `DEV`* |
| **F-3** | `NHE` | `docs/ITL/_tools/khop_owner.py:285`, `:294`–`:299` *(`B3`/`B4`)* · khối `SINH-KHOP` `_AUDIT_ALIGNMENT_ROADMAP.md:358`–`359` | = yếu điểm **5**, xác nhận: hai phép đếm trên **mọi ảnh** `fls_pm_line` *(**66** lượt × **3.820** dòng)* ⇒ chữ `196.480` trong khối đổi ở **ảnh PM kế tiếp** ⇒ `--kiem` so **cả khối chữ** *(`:613`–`:620`)* ⇒ **đỏ** mà ⛔ ai làm sai. Hôm nay xanh **chỉ vì** nhịp ⛔ chụp từ 18:20. Cùng lớp `GAP-CONG-01` | `BA` ⇒ `WO` cho `DEV` *(đếm trên ảnh **hiệu lực**, hoặc in quan hệ thay số)* |
| **F-4** | `NHE` | bản vẽ 13 · `09` · `dash` · `FLS-Luong-va-Nut.html` *(chủ câu văn: `fls-ba`)* | Câu **⛔ có cổng canh**, sai cạnh số đúng — ⛔ nằm trong 16 câu của `BG`: ⓐ ⚠ **`banve:1319`** chân trang — `--ghi` đổi *"đo ngày **01/10/2026** … commit `5fbc29c`"* nhưng câu vẫn *"**10.030** dòng sổ thật, **2.745** mối nối … Sổ bút toán và nhật ký **vẫn 0 dòng** — vòng ghi chưa từng chạy trên sổ thật"*; sổ thật **8.387** · **2.262** · `fls_journal` **4.428** *(từ 18/09)* ⇒ dấu ngày mới làm câu cũ thành khai **hôm nay** *(đáng vào bảng `10 §6 ⓑ`)*; ⓑ `banve:1462` *"64,3% … 1.345 dòng / 698 phiếu"* ngay dưới thẻ `58,1%` · `1.601` · `826` *(số cổng)*; cùng chuỗi ở `09:324` và `FLS-Luong-va-Nut.html:317`; ⓒ `banve:1493` *"không phải cả sổ **10.030** dòng"*; ⓓ `09:157` `B1` *"3.772 dòng lệnh, 1.345 chưa có tiền"* cạnh bản vẽ `3.820` *(Dev tự khai, yếu điểm 4)*; ⓔ `banve:1369` khối nhãn *"(fls-ba, …)"* chứa câu `fls-dev` viết; ⓕ `dash:542` §6 *"Mốc B ghi 4 đạt … phải sửa TRƯỚC"* — việc đã làm | `BA` *(sửa câu khi nghiệm thu; ⓐ có thể giao `DEV` theo `10 §6 ⓑ`)* |

## Yếu điểm Dev tự khai — tôi soi lại
| # | Yếu điểm | Đo được | Mức · gửi |
|--:|---|---|---|
| 1 | danh sách đen một phần tử | thật — thêm **3** actor máy khác trong mã *(`F-2 ⓐ`)*; hôm nay ⛔ actor nào lọt *(3 actor trên `fls_queue_event`)* | `NHE` · `BA` |
| 2 | UAT dựa trên chữ `reason` | thật — 3 biến thể tiền tố tính là người *(`F-2 ⓒ`)*; spec `10 §6` khai đúng luật này | `NHE` · `BA` |
| 3 | `AC-1` `= 2` chưa từng in | tôi đo tách: chỉ vạch máy ⇒ **2** đúng mong | ✅ đóng |
| 4 | số ⛔ cổng canh trong câu | thật — và **rộng hơn** Dev nói *(`F-4` ⓐ–ⓒ)* | `NHE` · `BA` |
| 5 | `SINH-KHOP` trôi theo nhịp | thật — `F-3` | `NHE` · `BA` ⇒ `DEV` |
| 6 | `kiem_so_song` 0 lệch là ảnh giờ chạy | đúng thiết kế — lượt này **⛔ trôi** vì ⛔ ảnh mới; ⛔ hồi quy | ✅ ghi nhận *(`GAP-CONG-01`)* |
| 7 | phân loại a/b/c đọc tay | tôi ⛔ thấy nhóm xếp sai; tổng 84 khớp | ✅ |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `tests/nghiem_thu/test_kq010_moc_b_dem_tren_duong_ghi_that.py` *(5 bài: người ghép/bỏ ⛔ lý do ⇒ `4·1·0`/`5·0·0` · máy ghép đứng · UAT ghép+bỏ đứng · owner bỏ ghép **thật** ⇒ `B4` đếm · người `Xong` `reason NULL` ⇒ đếm)* | ⓐ trên `tools/kiem_so_song.py` của **`ee390cb`** *(trước vá, worktree)* ⇒ **2** đỏ *(máy · UAT)* ⓑ đột biến trên `HEAD` *(worktree)*: `M1` · `M2` · `M3` · **`M4`** · **`M5`** · `M7` ⇒ mỗi cái **1** đỏ đúng bài; đối chứng `M8` *(thêm loại `MAY` ở `B4`)* **xanh** | ✅ `5 passed` |
| `tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay` — ⭐ **gỡ dấu `xfail(strict)`** | đỏ trên mã `ee390cb` *(worktree)*; `M1`/`M7` trên `HEAD` ⇒ đỏ lại | ✅ |

⚠ Kịch bản đột biến chạy trong **worktree** ở thư mục tạm *(⛔ trong repo)*, mỗi đột biến `assert` mẫu khớp **đúng 1** lần rồi trả nguyên *(`tra nguyen: True` ×11)*; worktree đã gỡ. Kho TEST: các dòng của bài `kq010` mang `run_id` `NAP-2000-…` *(bản TRẮNG)*; một bản sao kho thử `fls_kq010` dựng thử rồi **xoá** cùng lượt.

## Changelog
- 2026-10-02 trưa · `fls-test` · **đóng** `KQ-010` — `WO-011` *(sinh từ `F-2`/`F-3`)* qua kiểm [`KQ-014`](KQ-014-kiem-bg-013.md) ĐẠT 10/10.
- 2026-10-01 tối · `fls-test` · phát `KQ-010` — ✅ ĐẠT `WO-001` *(9/9 AC)*; 4 `F` `NHE`; gỡ `xfail` bài `KQ-002`; +5 bài `kq010`; đóng `KQ-002` *(F-2 xong — mọi F còn lại đã có trả lời)*, đóng `KQ-007` *(BA đã trả F-1…F-4)*.
