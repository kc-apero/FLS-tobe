# BG-009 — bàn giao `WO-001` *(thước mốc `B` ⛔ đếm máy + UAT là người · dấu sổ · `khop_owner` · `dong_bo --ghi`)*

| | |
|---|---|
| **Thuộc** | `WO-001` *(vòng 1)* |
| **Phát bởi** | `fls-dev` · 2026-10-01 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`6e98796`** *(đã đẩy — mã + bài thử + `--ghi` + câu cạnh số + changelog)*; phiếu này + nhật ký nằm ở commit kế tiếp |
| **Spec đã đọc** | `WO-001` *(bản rà sau `KQ-007`)* · `Ra-soat-tai-lieu-2026-10-01` v1.1 `R-1`…`R-6`, `R-25` · `09_MILESTONES` §2 *(bảng `09:157`–`161` sau sửa)* · `10_HOP_DONG_AGENT` **v1.1** §1, §6 · `QĐ-ITL-150` · `BA-11` v0.15 `INV-I08` · `KQ-002 F-2` |

> **Một câu cho owner:** con số *"mốc B"* trên dashboard, `09` và bản vẽ 13 nay là **`1` đạt · `1` một nửa · `3` chưa** thay vì `4·1·0` — **thước sửa, ⛔ việc lùi**: trước đây máy coi **2.219** cú ghép tự động của chính nó và **2** dòng thử UAT của owner là *"người bấm"*; nay chỉ cú bấm của **người thật** được đếm, và hôm nay con số ấy là **0**.

```mermaid
flowchart LR
  E[("fls_queue_event<br/>110.349 dòng")] --> R{"evt_type = 'reason'?"}
  R -- "108.128 · máy" --> X1["⛔ không đếm"]
  R -- "2.221" --> M{"actor = may@fls?<br/>(hằng may_ghep.MAY)"}
  M -- "2.219 · máy tự ghép 18/09" --> X2["⛔ không đếm"]
  M -- "2" --> U{"reason bắt đầu 'UAT '?"}
  U -- "2 · UAT 01/10" --> X3["⛔ không đếm"]
  U -- "0" --> N["sự kiện NGƯỜI = 0<br/>⇒ B2·B3·B5 CHƯA"]
```

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/kiem_so_song.py` | **`T1a`** `su_kien_cho_nguoi` thêm `actor is distinct from 'may@fls'` — chuỗi **thuần** *(bài `KQ-002` đọc bằng `ast`, đòi `ast.Constant`)*, nên gọi qua `dem_nguoi` ⇒ `_kiem_hang_may` **nổ** `SystemExit` nếu chuỗi ⛔ mang đúng `'{may_ghep.MAY}'` *(Rủi ro 2: khai hằng một chỗ, có soi)*. **`T1b`** thêm `left(coalesce(reason,''),4) <> 'UAT '` ở `su_kien_cho_nguoi`; `moi_noi_da_bo` = `fls_pm_unlink ⋈ fls_queue_event` qua `evt_id` loại cùng luật *(`left` thay `LIKE` — `dem()` gọi `execute` ⛔ tham số)*. **`T2`** câu dấu thời điểm dời ra hằng `_Q_GIO`: dấu sổ = `started_at` của lượt `fls_run` **có dòng `fls_itl`**; dấu ảnh PM giữ. Thêm: mẫu `master · số phép so của cổng` neo `\*\*…\*\*` *(xem "Cổng")*. Chú thích `_cong_moc_b` ghi lần vỡ thứ ba |
| `tests/test_kiem_so_song.py` | **`T3`** — **9** bài mới chạy **chính** chuỗi SQL của cổng *(đọc bằng `ast`)* trên CTE giả `fls_queue_event` / `fls_pm_unlink` / `fls_run` / `fls_itl` / `fls_pm_line` *(⛔ ghi gì, kể cả kho test)* |
| `docs/ITL/_tools/khop_owner.py` | **`T4`** `B5` neo `TEP_B5 = "06_SCREEN_SPEC.md"` *(tệp neo khớp ≠ 1 ⇒ `LoiDo`)*, `mong` `False ⇒ True` kèm xuất xứ `R-5`; `C5` tách: `C5` = cột `fls_itl.memo` *(mong LỆCH, giữ)* · **`C5b`** = khung xem `fls_dien_giai` *(mong KHỚP — `QĐ-ITL-145`, `R-6`)*. ⛔ Đổi tiền tố mã *(`R-7`)* |
| `docs/ITL/_AUDIT_ALIGNMENT_ROADMAP.md` | chỉ khối máy sinh `SINH-KHOP` *(`khop_owner.py` ⛔ `--kiem`)* — **17/20 khớp · 3 lệch** |
| `00_MASTER_INDEX.md` · `06_ORCHESTRATOR_DASHBOARD.md` · `08_MIGRATION_ROADMAP.md` · `09_MILESTONES_HAI_TAC_VU.md` · `02_BA/Artifacts/Ban-ve-Kien-truc-TOBE.html` | **`T5`** `dong_bo_so_song --ghi` *(47 mục soạn · 1 bỏ qua — xem "Cổng")* + câu cạnh số *(bảng dưới)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | dòng 2026-10-01 `WO-001` |

⛔ **Không** đổi schema · ⛔ **không** chạm `fls/**` *(⇒ mốc commit của cổng số sống vẫn `5fbc29c`)* · ⛔ **không** chạm `tests/nghiem_thu/**` *(`git diff 5d627c0 -- tests/nghiem_thu/` = rỗng)* · `--ghi` chạy **một** lần.

### Câu cạnh số đã sửa *(`10 §6 ⓑ` — `fls-ba` rà lại khi nghiệm thu)*

| Tệp:dòng *(sau sửa)* | Cũ → mới |
|---|---|
| `09:149` *(mới, ngay dưới tiêu đề mốc `B`)* | — → *"⚠ 01/10 (`WO-001`): **THƯỚC SỬA, ⛔ VIỆC LÙI** … `4 · 1 · 0` (rồi máy đo `5 · 0 · 0`) vì phép đếm coi 2.219 `match` của `may@fls` và 2 dòng UAT là người … nay `1 · 1 · 3`"* |
| `09:158` `B2` | *"`fls_queue_event` = `0` ⇒ chưa ai bấm"* → *"sự kiện **người thật** trên `fls_queue_event` = `0` (sau khi loại máy + UAT)"* *(bảng thật `110.349`)* |
| `09:160` `B4` | *"`fls_pm_unlink` = `0` trên sổ thật"* → *"`fls_pm_unlink` = `1` — chính cú bỏ ghép UAT 01/10, ⛔ tính ⇒ việc thật = `0`"* |
| `09:163` | *"⛔ không một cửa GHI nào … từng được dùng trên sổ thật"* → thêm *"(ngoài cú UAT 01/10 — ròng `0`, ⛔ tính người)"* |
| `09:167` | *"`evt_type <> 'reason'` = việc người làm …"* → giữ, thêm *"Tiền đề ấy vỡ LẦN NỮA 18/09 … từ 01/10 loại thêm `may@fls` + `UAT `"* |
| `09:218`–`219` *(bút toán / sự kiện)* | `4.428` / `110.349` → thêm cắt nghĩa *"(`4.424` máy gợi ý · `4` UAT — người thật `0`)"* / *"(`108.128` reason + `2.219` match máy + `2` UAT — người thật `0`)"* — tiêu đề *"con số của tác vụ ② là một số KHÔNG"* nay đúng theo nghĩa **người** |
| `09:324` *(bảng mốc, dòng `B`)* | *"`fls_queue_event` = `0`"* → *"sự kiện **người thật** … = `0` (loại máy + UAT)"* |
| `dash:121` | thêm *"⚠ từ `4 · 1 · 0`: **thước sửa, ⛔ việc lùi**"* · *"`fls_pm_unlink` = `0`"* → *"= `1`, chính cú UAT ⛔ tính"* · *"`108.128` dòng … `evt_type <> 'reason'` = `0`"* → *"`110.349` dòng: `108.128` reason + `2.219` match máy + `2` UAT ⇒ người thật = `0`"* |
| `master:325` | *"lạc hậu 326 phép thử"* *(sai từ trước: `1903 − 548`)* → *"lạc hậu hơn 1.400 phép thử (đo 01/10; câu cũ ghi "326")"* |
| `banve:1369` *(thẻ mốc 2)* | *"con số trên là máy đếm, và từ 18/09 máy đếm 2.219 … ⇒ theo đúng nghĩa cổng … là 1 · 1 · 3"* → *"từ 18/09 đến 01/10 máy đếm … in 4 · 1 · 0; từ 01/10 (WO-001) … máy in đúng nghĩa 1 · 1 · 3 — thước sửa, ⛔ việc lùi"* |
| `banve:1400` *(thẻ ảnh lệnh chi `66`)* | *"nay có **hai**"* → *"nay có **nhiều** — nhịp nạp mỗi giờ, số ở trên"* |
| `banve:1410` *(thẻ trần cũ `53,4%`)* | *"trên **8.246** dòng tiền … vượt **47,4%**"* → *"trên dòng tiền (mẫu số ở bảng trần cứng) … vượt con số trên (câu cũ ghi 8.246 · 47,4% — số của 09/09)"* |
| `banve:1436` *(cổng `A3`)* | *"**1** ảnh lằn lệnh chi · **2** ảnh khác nhau · 3.820"* → *"Nhiều ảnh … (số ở thẻ "Ảnh lệnh chi khác nhau"; câu cũ ghi 1 · 2) · 3.820"* |
| `banve:1470` *(bảng phía PM)* | `3.772` → **`3.820`** *(= 2.219 + 1.601 ngay dưới — hàng ⛔ có cổng nên `--ghi` ⛔ chạm)* |
| `banve:1475` | *"Tiền của 1.345 dòng ấy"* → *"Tiền của dòng chưa có tiền (đo 09/09 trên 1.345 dòng — ⛔ chưa đo lại)"* |

## Cổng *(kết quả nguyên văn, chạy với `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`, `PYTHONUTF8=1`, trên cây đã commit `6e98796`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `1 failed, 1957 passed in 269.42s` — ⭐ **1** failed **duy nhất** = `[XPASS(strict)]` `tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay` *(đúng mong `AC-1b`/`AC-4` — chờ `fls-test` gỡ dấu)*. Nền `1948 passed, 1 xfailed` = **1.949** ⇒ nay **1.958** = **+9** bài mới |
| `pytest tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py --runxfail` | `2 passed in 0.76s` *(trước vá: `1 failed, 1 passed`)* |
| `python tools/kiem_so_song.py` | `✅ cong so song DAT — 109 phep so, moi phep khop DUNG mot lan va khop dung con so MAY do (commit `5fbc29c`)` *(trước: `⛔ CONG SO SONG KHONG DAT — 84 lech/khong-do-duoc`)* |
| `python tools/dong_bo_so_song.py --ghi` *(một lần)* | `47 muc soan · 1 muc BO QUA (cong ⛔ khong do duoc)` — bỏ qua = `master · số phép so của cổng: mau khop 2 lan` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (97 file, 1187 bang, 635 o ngay, 104 ma QD), khong chi 'khong thay loi'` |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech   (da do 20/20 phep)` · `✅ cong `C1` DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` *(trước: `15/19 khop · 4 lech` + `⛔ CONG NO: khoi trong lo trinh LECH`)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — ⛔ chạm schema |

⚠ **Nhóm duy nhất `--ghi` ⛔ dọn được, và vì sao:** mẫu `cổng số sống (\d+)/(\d+)` ở `00_MASTER_INDEX` khớp **2** lần — lần thứ hai là sổ `QĐ-ITL-150` *(`fls-ba`, `c1fb250`)* ghi *"nhóm lệch của cổng số sống **01/10**"* — một **NGÀY** mà mẫu đọc như `phép/tổng`. Công cụ đúng luật ⓒ bỏ qua. Sửa **mẫu** *(chủ `tools/**`)*: neo `\*\*cổng số sống (\d+)/(\d+)\*\*` ⇒ khớp đúng 1 chỗ *(`master:343` "**cổng số sống 109/109**")*. ⛔ Sửa câu của sổ `QĐ` *(biên bản)*.

⚠⚠ **Đỏ lại SAU KHI viết chính phiếu này — `1` lệch, có chủ ý ⛔ dọn:** chạy lại `kiem_so_song` trên cây có `BG-009` + nhật ký ⇒ `⛔ master · §8 số file + hiện vật (nhom 1): tài liệu ghi `97` · MÁY đo `98` ⛔ LỆCH` · `⛔ CONG SO SONG KHONG DAT — 1 lech/khong-do-duoc`. Tệp thứ **98** chính là `BG-009` *(`kiem_tai_lieu` cùng lúc: `98 file`)*. ⛔ Chạy `--ghi` lần hai để dọn nó *(mỗi phiếu thêm một tệp ⇒ lặp vô hạn; `10 §6 ⓒ`)* — `fls-test` đo ở commit phiếu sẽ thấy đúng **1** lệch này *(+ số trôi theo nhịp nếu đo muộn — yếu điểm 6)*.

⚠ **Nhóm hash** *(`nhanh · commit`, `ban ve · chan trang`)*: đo `git log -1 -- fls/`. Lượt này ⛔ chạm `fls/` ⇒ commit `6e98796` và commit phiếu kế tiếp ⛔ làm nó đỏ lại. Một `WO` sau chạm `fls/` thì hai nhóm này **sẽ** đỏ — loại **c**, đúng thiết kế, ⛔ dọn bằng `--ghi` lần hai của phiếu này.

### `AC-5` — `kiem_so_song` tách theo nền
| | Trước *(@ `ee390cb`, đo lại đầu lượt)* | Sau *(@ `6e98796`)* |
|---|--:|--:|
| Tổng | **84** giá trị lệch trong **48** nhóm | **0** · **0** nhóm |
| ⓐ số trôi theo ảnh/nhịp — `kho · anh chup dong lenh` · `kho · DẤU ảnh chụp` · `master · DẤU`¹ · `roadmap · DẤU`¹ · `roadmap · ảnh chụp` · `§1 · mẫu số tác vụ ①` · `master · kho` · `bản vẽ · ảnh chụp lệnh chi` · `dashboard · ảnh nhịp` · 8 nhóm `bản vẽ 13 · …` *(ảnh nhịp, ảnh lệnh chi, trần, trần cứng, `A3`, phía PM ×3)* | **17** nhóm | 0 |
| ⓑ version tài liệu + số tệp — `master · §8 version BA-05/06/07/08/10/11` · `master · §8 số file + hiện vật` | **7** nhóm | 0 |
| ⓒ số phép thử / dòng mã / commit / ngày — `test · tong va trong module` · `nhanh · commit` · `ban ve · chan trang` · `roadmap/master/bản vẽ · phép thử + dòng` · `bảng tiến độ · dòng TỔNG/repo/api/web` · `master · §8 test` · `bản vẽ · thanh repo/api` · 3 `caption` | **16** nhóm | 0 |
| UAT 01/10 *(số tăng thật vì cú UAT — `Ra-soat` §1.1 loại "8 UAT")* — `mốc · bút toán sửa THẬT` *(4.424 ⇒ 4.428)* · `mốc · sự kiện hàng chờ THẬT` *(110.347 ⇒ 110.349)* | **2** nhóm | 0 |
| ⭐ **của chính `WO-001`** — mốc `B` ×3 *(`dashboard` · `mốc` · `bản vẽ 13`; máy cũ `5·0·0`, nay `1·1·3`)* + dấu sổ `T2` *(`kho · DẤU bản sao sổ` · `bản vẽ · DẤU`; ¹ hai nhóm `DẤU` ở ⓐ mang cả dấu sổ lẫn dấu ảnh)* | **5** nhóm | 0 |
| ⛔ không đo được — `master · số phép so của cổng` *(mẫu khớp 2 lần)* | **1** nhóm | 0 *(sửa mẫu)* |

⚠ Số nhóm ⓐ/ⓑ/ⓒ tôi phân bằng **đọc tên nhóm** trong đầu ra *(`kss_truoc`)* — ⛔ có máy phân loại; người kiểm có thể chia khác 1–2 nhóm.

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-1** | Kho thật *(chỉ `SELECT`)*: `match/may@fls` **2.219** · `match/khanhcq` **1** · `unmatch/khanhcq` **1** · `reason/dung-lai-so` **108.128**; cổng nay in mốc B **`1·1·3`** ⇒ `su_kien_cho_nguoi` = **`0`** *(⛔ `2` như `AC-1` dự — vì `T1b` cùng lượt loại luôn 2 dòng UAT; nếu chỉ `T1a` thì là `2`)*. Bài `test_T1a_su_kien_MATCH_cua_MAY_dem_0_nguoi` + `test_T1a_MAY_ghi_match_ma_KHONG_dong_duoc_cong_nao` *(mở rộng `test_MAY_ghi_93k_…`: đếm bằng **chính SQL** rồi đưa vào `_cong_moc_b` ⇒ `1·1·3`)*. **Chiều ĐỎ:** trước vá **2 bài đỏ** `assert 2 == 0` · đột biến `D1` *(trả câu cũ)* ⇒ 5 đỏ · `D5` *(bỏ vạch actor)* ⇒ 4 đỏ |
| **AC-2** | `kiem_so_song` *(sau vá, trước `--ghi`)*: `dashboard · cổng mốc B (nhom 1): tài liệu ghi `4` · MÁY đo `1`` · `(nhom 3): … `0` · MÁY đo `3`` ⇒ máy đo **`1 · 1 · 3`**; khớp bảng `09:157`–`161` *(B1 ✅ · B2/B3/B5 ⛔ · B4 ◐)*. **Chiều ĐỎ:** `test_T1b_ly_do_MAC_DINH_may_dien_van_la_NGUOI` + `test_T1b_loc_theo_LY_DO_khong_theo_ACTOR` — một `match` người, reason ⛔ bắt đầu `UAT` ⇒ đếm **1** ⇒ `B5` lật đạt *(cổng ⛔ mù với người thật)* |
| **AC-3** | `kho · DẤU THỜI ĐIỂM bản sao sổ: … MÁY đo `10/09 18:54`` *(trước vá: `01/10 18:20`)* — `NAP-2026-09-10-BU1` `started_at` 11:54:50 UTC. Bài `test_T2_dau_SO_la_luot_nap_SO_khong_phai_anh_PM` *(khuôn có lượt PM mới hơn, 0 dòng sổ)* — trước vá **đỏ** `dau so = 2026-10-01 11:20:53+00:00`. Dấu ảnh `01/10 18:20` giữ *(cùng bài)* |
| **AC-1b** | `--runxfail` ⇒ `2 passed`; chạy thường ⇒ **1** `XPASS(strict)` *(tên ở "Cổng")*; `git diff 5d627c0 -- tests/nghiem_thu/` **rỗng**. **Chiều ĐỎ:** đột biến `D1` *(trả câu cũ)* ⇒ bài ấy đỏ lại *(`dot_bien` D1 liệt kê `test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay`)* |
| **AC-4** | `1957 passed` + **1** `XPASS(strict)` của `AC-1b`, ⛔ bài nào khác; `lint-imports` `9 kept, 0 broken`; **+9** bài *(1.949 ⇒ 1.958)* = 9 bài mới ở `tests/test_kiem_so_song.py`. Ba bài `kq005` đã gỡ dấu từ `KQ-007` ✅ |
| **AC-5** | bảng *"`AC-5`"* trên |
| **AC-2b** | `test_T1b_ly_do_MAC_DINH_may_dien_van_la_NGUOI` *(reason `"(may dien) ghep tren man - nguoi bam khong ghi ly do · ghep tay 1 dong lenh (X)"` ⇒ **1**)*. **Chiều ĐỎ:** đột biến `D3` *(lọc `'('` đầu chuỗi)* ⇒ đúng bài này đỏ · `D2` *(lọc actor `khanhcq@`)* ⇒ `test_T1b_loc_theo_LY_DO_khong_theo_ACTOR` đỏ · `D4` *(`UAT` bất kỳ chỗ)* ⇒ `test_T1b_UAT_phai_o_DAU_ly_do` đỏ. `B4`: `D6` *(đếm trần `fls_pm_unlink`)* ⇒ `test_T1b_bo_ghep_UAT_KHONG_dong_not_B4` đỏ |
| **AC-6** | `khop_owner --kiem` ⇒ `17/20 … ✅ cong C1 DAT`; bảng sinh: `B5 … 06_SCREEN_SPEC.md (BA-06) nhac co che de xuat 44 lan … ✅` · `C5 … 0/8387 dong co memo … ⛔` · `C5b … 8366/8387 dong co Dien giai … ✅`. **Chiều ĐỎ:** đổi `TEP_B5` về `12_BA_MAN_GHEP_PM.md` ⇒ mã ra `1`, `B5 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH — mot cho DANG KHOP vua vo` *(trả nguyên: byte trùng)* |
| **AC-7** | `kiem_so_song` **ĐẠT 0 lệch**; mốc B ở `09:147`, `dash:121`, `banve:1367` = **`1 · 1 · 3`** kèm câu *"thước sửa, ⛔ việc lùi"* *(bảng câu trên)*. Chiều ĐỎ: `T5` chạy **sau** `T1a`+`T1b`+`T2` xanh *(trình tự: vá → pytest 1957+1 XPASS → `--ghi`)*; bài `KQ-002` canh chiều `5·0·0` |

Kịch bản đột biến *(tệp tạm, ⛔ trong repo)*: thay câu SQL trong `tools/kiem_so_song.py` → chạy `tests/test_kiem_so_song.py` + bài `KQ-002` `--runxfail` → trả nguyên *(`tra nguyen: True`)*. Kết nguyên văn: `D1 5 failed` · `D2 1 failed` · `D3 1 failed` · `D4 1 failed` · `D5 4 failed` · `D6 1 failed`.

## Kho thật
- `KHONG_CHAM` — chỉ `SELECT` *(đếm `fls_queue_event` theo `evt_type`/`actor`, `fls_pm_unlink ⋈ fls_queue_event`, `fls_run` có/không dòng `fls_itl`, `fls_journal`/`fls_adjustment` theo actor)*. Máy 8088 ⛔ chạm.

## Dev tự thấy còn yếu
1. **Lọc actor vẫn là danh sách đen một phần tử.** Một tiến trình máy **mới** mang actor khác `may@fls` ghi `match`/`unmatch`/`done` sẽ lại được đếm là người *(lần vỡ thứ tư)*. `_kiem_hang_may` chỉ canh **đổi giá trị** `MAY`, ⛔ canh **thêm** actor máy. Hôm nay đo: actor trên `fls_queue_event` chỉ có `dung-lai-so@apero.vn` *(chỉ `reason`)*, `may@fls`, `khanhcq@apero.vn` — đủ, nhưng ⛔ có cổng nào nói *"actor lạ xuất hiện"*.
2. **Luật UAT dựa trên chữ `reason`.** Ai gõ tay lý do bắt đầu `UAT ` cho việc thật sẽ bị loại; một lượt UAT sau quên tiền tố sẽ được tính là người. Spec *(`10 §6`)* khai đúng luật này — tôi theo spec, ⛔ có ràng buộc máy nào buộc lượt UAT mang tiền tố.
3. **`AC-1` nói `su_kien_cho_nguoi = 2` sau `T1a`** — tôi làm `T1a`+`T1b` trong **một** câu, nên ⛔ có lúc nào kho in `2`; bằng chứng `2` chỉ là đếm tay `2.221 − 2.219`. Nếu `fls-test` muốn đo `T1a` tách riêng thì phải đột biến bỏ vạch UAT.
4. **Câu cạnh số tôi sửa ở `banve:1470`/`1475`, `09:218`–`219` mang số ⛔ có cổng canh** *(`3.820`, `4.424`/`4`, `108.128`/`2.219`/`2`)* — chúng sẽ già trong im lặng như chính lỗi `GAP-DOC-08`. Tôi chọn ghi số vì câu cũ **tự mâu thuẫn** với hàng ngay dưới; cách đúng hơn *(trỏ, ⛔ chép)* là việc của `fls-ba`. `09:157` `B1` vẫn ghi *"3.772 dòng lệnh, 1.345 chưa có tiền"* *(cũ — ⛔ cạnh số `--ghi` đổi, nên tôi ⛔ sửa)*; `11_BOI_CANH_TU_MEMORY:87` vẫn ghi *"khop_owner 15/19"* *(biên bản ngày)*; lộ trình audit `:162` vẫn câu *"`Diễn giải` ⛔ KHÔNG có trong kho"* *(`R-6` vế câu — chủ `fls-ba`)*.
5. **Khối `SINH-KHOP` mang số trôi theo nhịp** *(`B3`/`B4` đếm `fls_pm_line`: `105.616` ⇒ `196.480` trong lượt này)* ⇒ `khop_owner --kiem` sẽ **đỏ lại** sau vài giờ nhịp chạy, ⛔ vì ai làm sai. Có từ trước phiếu này; tôi ⛔ đổi — đáng một `WO` *(ghim quan hệ, ⛔ ghim số — cùng lớp `GAP-CONG-01`)*.
6. **`kiem_so_song` `0` lệch là ảnh chụp giờ chạy** *(đo ~19:00 01/10)*: 26 nhóm loại ⓐ trôi theo nhịp mỗi giờ ⇒ `fls-test` chạy lại sau một cú chụp sẽ thấy đỏ ở nhóm ảnh/PM — ⛔ phải hồi quy của `WO-001`. Nhóm mốc `B` + dấu sổ thì ⛔ trôi *(dấu sổ chỉ đổi khi nạp sổ)*.
7. Phân loại ⓐ/ⓑ/ⓒ ở `AC-5` là đọc tay tên nhóm *(xem ghi chú dưới bảng)*.
