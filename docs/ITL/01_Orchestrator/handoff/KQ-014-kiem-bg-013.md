# KQ-014 — biên bản kiểm `BG-013` *(`WO-011`: sổ actor một chỗ · UAT một luật · actor mới gọi tên · `B4`/`C8` loại máy + UAT · `khop_owner` trên ảnh hiệu lực · phép so `09` §7 · `--ghi`)*

| | |
|---|---|
| **Thuộc** | `BG-013` · `WO-011` *(vòng 1, bản đính chính `TL-012`)* |
| **Kiểm bởi** | `fls-test` · 2026-10-02 trưa · nhánh `feat/p2-oracle-parity` @ `af34be7` *(mã `88ab178` · `--ghi` `75d9f85` · phiếu `24a8591` · `TL-012` `af34be7`; `HEAD` = `origin` — đã đẩy)* |
| **Phán quyết** | ✅ **ĐẠT** — **10/10** AC đạt; ba lăng kính ⛔ còn `CHAN`/`NANG`. Bốn phát hiện **`NHE`**: `F-1`, `F-2` gửi `DEV` *(ghi nhận — ⛔ đường nào trên kho thật chạm hôm nay)* · `F-3`, `F-4` gửi `BA` |
| **Trạng thái** | ✅ **`DONG`** *(02/10 chiều — `fls-ba` đã trả cả 4 `F`, mục **Trả lời `fls-ba`**; `WO-011` nghiệm thu PO ⇒ `DONG`)* · ~~`MO` — chờ `BA` (nghiệm thu PO `WO-011`; rà câu cạnh số `10 §6 ⓑ`; `F-3`, `F-4`)~~ |

> **Một câu cho owner:** máy nay biết **9** tài khoản ⛔ phải người, và tôi đã thử phá nó trên kho thử bằng chính các nút ghi của hệ: dòng thử `UAT` gõ **10 kiểu** *(hoa/thường, dấu cách đầu, dán từ trình duyệt…)* ⇒ mốc B **đứng yên**; lý do thật **6 kiểu** *(kể cả "uất ức…", "ghi chú UAT…")* ⇒ mốc **nhích**; **9/9** máy bỏ ghép ⇒ `B4` **đứng**; một **máy mới quên khai** ⇒ cổng **gọi đúng tên nó, một dòng**. Sổ thật **⛔ bị chạm**, con số vẫn **`1 · 1 · 3`**, người thật **0**. Còn bốn chỗ nhỏ — hai chỗ chỉ xảy ra với ký tự rất hiếm hoặc hai cú sửa trong cùng một lần ghi *(hôm nay ⛔ đường nào làm được)*, hai chỗ là câu văn/phạm vi cho BA.

```mermaid
flowchart LR
  subgraph KHO_TEST["Kho THỬ — cửa ghi thật, mỗi bài một giao dịch LÙI"]
    U["UAT ×10 biến thể<br/>ghép + bỏ ghép"] --> C{"câu SQL của cổng<br/>(đọc bằng ast)"}
    N["lý do người ×6<br/>(gồm 'uất ức…', NULL)"] --> C
    M["9/9 actor máy<br/>ghép + bỏ ghép"] --> C
    X["máy MỚI chưa khai<br/>3 thao tác"] --> C
  end
  C -- "UAT/máy: +0" --> D["mốc B đứng 1·1·3"]
  C -- "người: +2" --> E["1·1·3 ⇒ 5·0·0"]
  X --> G["⚠ ACTOR MỚI: … · 3 dòng<br/>(MỘT dòng báo) + vẫn đếm là người"]
  T[("Sổ THẬT — chỉ SELECT")] --> R["1·1·3 · người 0 · actor lạ 0<br/>= số máy in"]
```

## Cổng chạy lại *(Test tự chạy, `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`, `PYTHONUTF8=1`, tuần tự)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| Cổng vào: git | `88ab178` + `75d9f85` đã đẩy | `HEAD` = `origin/feat/p2-oracle-parity` = **`af34be7`**; `git show --stat 88ab178` = **21** tệp đúng bảng *Đã đổi*; `75d9f85` = **4** tệp tài liệu; `git diff 27c163a af34be7 -- tests/nghiem_thu/` **rỗng** | ✅ |
| Cổng vào: version spec | `WO-011` *(sửa 02/10)* · `09` **v1.14** · `BA-14` **v0.8** · `10` **v1.1** · master **v0.30** | khớp `WO-011` mục *Spec*; đính chính `TL-012` *(`AC-1` 9 tên, `T2` bản chép bị ép trùng byte)* — kiểm theo bản đính chính | ✅ |
| `python -m pytest` *(@ `af34be7`, trước bài của tôi)* | `2051 passed` | **`2051 passed in 274.97s (0:04:34)`** — ⛔ `xfail`/`skip` | ✅ |
| `python -m pytest` *(+ bài `KQ-014`)* | — | `tests/nghiem_thu/test_kq014_…` **`33 passed`** ×5 lượt *(⛔ chập chờn)* ⇒ bộ **2.084** | ✅ |
| `python tools/kiem_so_song.py` *(11:01, trước ảnh nhịp 11:09)* | `0` lệch · 110 phép | **`✅ cong so song DAT — 110 phep so … (commit 88ab178)`** · `OK mốc · §7 dòng B · phía PM` · mốc B ×3 **OK** · `OK cổng mốc B · actor ngoài sổ (ACTOR_MAY ∪ ACTOR_DA_THAY): 0` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `103 file` | `✅ cong tai lieu DAT — … (103 file, 1239 bang, 644 o ngay, 104 ma QD)` *(`1239` bảng vs `1233` lúc `BG` — đếm sau `24a8591`+`af34be7`, hai commit phiếu)* | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `17/20` · `C1` ĐẠT | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT`; màn: `anh NAP-2026-10-02-PME7F31617: 3820/3820` · `0 ngoai le / 3.820` · `C5b 8370/8387`; `grep -c 196.480 _AUDIT_ALIGNMENT_ROADMAP.md` = **0** | ✅ |
| `python tools/soi_bang_tuyen.py` | `40` | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python tools/kiem_thuyet_minh.py` | `31/31` | `✅ CONG THUYET MINH DAT — 31/31 nut` | ✅ |
| `.venv/Scripts/lint-imports.exe` | `9 kept, 0 broken` | `Contracts: 9 kept, 0 broken.` | ✅ |
| `python -m fls.db.pg_migrate` | ⛔ chưa chạy *(⛔ chạm schema)* | ⛔ **⛔ chạy bản ghi** *(áp lên kho thật — cấm ghi)*. `--status`: mới nhất `0026_dien_giai_sao_ke` đã áp · `pg_verify`: **`khop: 25 bang/view dung nhu khai bao`** | ✅ |

⚠ Sau commit của chính `KQ-014` *(+1 phiếu, +1 tệp bài, +33 phép thử)* `kiem_so_song` đỏ ở nhóm **số tệp / số phép thử** — đo trên cây có bài + phiếu `KQ-014` *(11:18, trước commit)*: **8** lệch *(`2051 → 2084` ×6 nhóm · bài ngoài module · số tệp `103 → 104`)*; ⛔ nhóm mốc B / actor / kho / ảnh nào. `kiem_tai_lieu` ✅ `104 file`. Loại **b/c**, do phiếu kiểm, ⛔ hồi quy. Nhịp chụp ảnh mới *(mỗi giờ :09)* ⇒ nhóm ảnh/PM trôi — loại ⓐ `GAP-CONG-01`. ⛔ Tôi ⛔ chạy `--ghi` *(`10 §6 ⓒ`)*.

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** *(đính chính)* | sổ **9** actor; hằng cũ lấy từ sổ; `grep` chuỗi chỉ còn ở sổ + chuỗi SQL `kiem_so_song.py` | `fls/repo/danh_muc_actor.py`: `ACTOR_MAY` = **9** tên đúng bảng `AC-1`. `grep -rlF '"<actor>"\|'<actor>''` trong `fls/`+`tools/` *(⛔ `__pycache__`)*: mỗi tên **8/9** ⇒ đúng **2** tệp *(sổ + `kiem_so_song.py`)*; `nhip@fls` thêm `tools/soi_nhip.py` — **docstring + chuỗi `print`** *(dòng 10/13/27/235)*, ⛔ hằng chạy — Dev đã khai; `ke-toan@apero.vn` / `ke-toan-2@apero.vn` ⇒ **0** tệp. Chiều ĐỎ *(worktree)*: `K10` thêm `THU_MOI = "thu-moi@fls"` vào `tools/chay_cua.py` ⇒ `test_QUET_MA__…` **1 failed**; `K4` thêm `may-moi@fls` vào sổ ⇒ `kiem_so_song` nổ `⛔ khong do duoc: cau dem su kien NGUOI ⛔ mang DUNG danh sach MAY…`; `K3` xoá `nhip@fls` khỏi **chuỗi SQL** ⇒ nổ cùng câu + bài `KQ-014` `B4[nhip@fls]` đỏ | ✅ ĐẠT |
| **AC-2** | kho thật mốc B `1·1·3`; người **0**; actor lạ **0** | `kiem_so_song`: mốc B ×3 **OK** + `actor ngoài sổ: 0`. **Đếm tay độc lập** *(SQL của tôi, ⛔ mã cổng)*: `fls_queue_event` theo `(evt_type, actor)` = `reason/dung-lai-so` **108.128** · `match/may@fls` **2.219** · `match/khanhcq` **1** · `unmatch/khanhcq` **1** = **110.349**; 4 sự kiện ngoài `reason`: 2.219 máy + 2 lý do `UAT 01/10 …` ⇒ người **0** / mẫu số **2.221**; `fls_pm_unlink` **1** ⇒ `evt 163567` UAT ⇒ `B4` **0** / **1**; `fls_pm_line` **256.928** > 0 ⇒ `B1` ⇒ **`1·1·3`**. Actor ở 3 bảng gốc = {`dung-lai-so`, `may@fls`, `khanhcq`} ⊆ sổ ⇒ **0** lạ | ✅ ĐẠT |
| **AC-3** | actor mới ⇒ đếm người + `⚠ ACTOR MỚI: <tên> · <n>` + NO; khai ⇒ im | Bài Dev `test_AC3_*` ×3 xanh *(`main()` trả `1`)*. ⭐ Bài `KQ-014` `test_MAY_MOI_chua_khai__…`: một **máy mới quên khai** ghép/bỏ/ghép lại qua cửa ghi thật ⇒ người **3** ⇒ mốc `5·0·0` **và** `_q_actor_moi` = `[(may-moi-chua-khai-kq014@fls, 3)]` ⇒ **một** dòng báo bắt đầu `⚠ ACTOR MỚI: … · 3`. Chiều ĐỎ: `K5` `canh_actor_moi` im ⇒ bài đỏ | ✅ ĐẠT |
| **AC-4** | máy ⇒ mốc B đứng, kể cả `B4` | ⭐ `KQ-014` `test_MAY_bo_ghep_qua_cua_that__B4_DUNG[×9]` — **9/9** actor `ACTOR_MAY` ghép + bỏ ghép thật *(`fls_pm_unlink` = 1 mỗi bài — Đ3)* ⇒ `B4` **0**, người **0**, ⛔ báo actor mới. Chiều ĐỎ: `K2` bỏ vạch máy ở `B4` ⇒ **9 failed** | ✅ ĐẠT |
| **AC-5** | UAT một luật, hai mặt trùng trên bảng mẫu | Bài Dev 25 mẫu xanh. ⭐ `KQ-014` qua cửa ghi thật: **10** biến thể UAT *(`'UAT 02/10'`, `'uat …'`, `'  UAT'`, `'UAT02/10'`, `'Uat: …'`, NBSP đầu, `\t` đầu, `'UAT'`, `'UAT_02'`, `'UAT-02/10'`)* ⇒ `B2/3/5` **0** + `B4` **0**; **6** lý do người *(`'ghi chú UAT …'`, `'UATX …'`, `'uất ức …'`, `'UATs …'`, thường, `NULL`⇒`(may dien)`)* ⇒ **2** + **1**. Chiều ĐỎ: `K6` trả `left(…,4) <> 'UAT '` ⇒ **5** biến thể đỏ. ⚠ Quét **mọi** điểm mã ⇒ hai mặt **lệch 7.405 / 1.112.063** ở vị trí *"ký tự sau `UAT`"* — `F-1` *(ngoài bảng mẫu của `AC-5`; chiều ỒN)* | ✅ ĐẠT |
| **AC-6** | `C8`: UAT/máy ⛔ lật, người lật | Bài Dev xanh. ⭐ `KQ-014` `test_C8_…`: `'Uat: …'` · NBSP+`UAT` · actor `nhip@fls` ⇒ `fls_sua_tay` **3** dòng *(Đ3)* ⇒ `khop=True`=`mong`; người `'UATX …'` ⇒ `khop=False` ⇒ CONG NO. Chiều ĐỎ: `K7` bỏ lọc UAT · `K8` bỏ lọc máy ⇒ bài đỏ. Kho thật: `NGUOI chot 0`; 4 dòng `sua_tay` UAT nối nhật ký **4/4** *(đảo 2/2)* | ✅ ĐẠT |
| **AC-7** | `B3`/`B4` trên ảnh hiệu lực; khối ⛔ `196.480` | Kho thật *(SQL độc lập)*: ảnh `NAP-2026-10-02-PME7F31617` **3.820** dòng, **3.820** có cha, **0** ngoại lệ / **3.820** có `tho` = màn in. Trên **mọi** ảnh: **204.120** dòng có `tho` *(⇒ số cũ `196.480` đã trôi `+7.640` = 2 ảnh — `F-3` của `KQ-010` có thật)*; khối ⛔ chứa `196.480`. ⭐ `KQ-014` `test_B3_B4_anh_CU_ban_anh_HIEU_LUC_sach__…`: ảnh cũ **2** ngoại lệ ⇒ `B4` NO; ảnh mới sạch ⇒ `B4` **ĐẠT lại**, `B3` `3/3`. Chiều ĐỎ: `K11` `B4` đếm mọi ảnh · `K12` `B3` đếm mọi ảnh ⇒ bài `KQ-014` **và** bài Dev `AC7` đỏ | ✅ ĐẠT |
| **AC-8** | phép so `09` §7 dòng `B`; hôm nay OK | `OK mốc · §7 dòng B · phía PM`; `58,1%` = 2.219/3.820 · `1.601` = 3.820 − 2.219. Chiều ĐỎ *(worktree)*: `K9` `58,1%`→`58,2%` ⇒ `⛔ mốc · §7 dòng B · phía PM (nhom 1): tài liệu ghi 58,2 · MÁY đo 58,1 ⛔ LỆCH` | ✅ ĐẠT |
| **AC-9** | pytest xanh ⛔ xfail · lint 9/0 · +88 · `nghiem_thu` ⛔ đổi | `2051 passed` = 1.963 + 88; lint `9 kept, 0 broken`; `git diff 27c163a af34be7 -- tests/nghiem_thu/` rỗng | ✅ ĐẠT |
| **AC-10** | `--ghi` xong: `kiem_so_song` 0 · `kiem_tai_lieu` · `khop_owner` ĐẠT · bảng câu | ba cổng ĐẠT *(trên)*; `BG` có bảng **16** chỗ — rà ở mục *Tài liệu* | ✅ ĐẠT |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(`WO-011` đính chính · `09` v1.14 ⓐ…ⓔ · `QĐ-ITL-150 ⓐ` · `TL-012`)* | ✅ **ĐẠT** — người = ⛔ `ACTOR_MAY` ∧ ⛔ UAT ở `B2/3/5`, `B4`, `C8`; actor mới **đếm + gọi tên**; `B3`/`B4` gọi **chính** `anh_pm_hieu_luc(conn, chi_nap_that())`. Hai lỗ **chỉ trên giấy** *(⛔ đường ghi nào hôm nay chạm)* — `F-1`, `F-2` | **Diff `88ab178`** đọc từng dòng: `sql_ngoai_may` sắp xếp ⇒ chuỗi ổn định; `_kiem_hang_may(sql, tien_to)` ép **trùng byte** cả hai mẩu cho `su_kien_cho_nguoi` *(⛔ tiền tố)* và `moi_noi_da_bo` *(`e.`)*; `coalesce(reason,'')` giữ cú `Xong` người; `_q_actor_moi` phủ `fls_queue_event` + `fls_adjustment` + `fls_journal` *(`fls_da_xong` là khung xem trên bảng đầu, `fls_pm_unlink` nối `evt_id`)* — đối chiếu `schema.py`: bảng mang cột `actor` = **5** *(3 bảng trên + `fls_chup`, `fls_khai_cot` — ngoài phạm vi, `F-4`)*; `fls_pm_link` ⛔ có `actor`. **Kịch bản phá trên kho TEST, cửa ghi thật** — 33 bài `KQ-014` *(mục AC-3…AC-7)*. **12 đột biến** *(worktree, mỗi mẫu khớp đúng 1, trả nguyên `sha256` ×12)*: `K1`…`K12` **đều bị bắt**. ⚠ Quét luật UAT **mọi điểm mã** *(kho thật, phiên `READ ONLY`, chỉ literal)*: vị trí *khoảng trắng đầu* · `U` · `A` · `T` — hai mặt **trùng** *(9 · 2 · 2 · 2 điểm mã nhận)*; vị trí *ký tự sau* — **7.405** lệch, **mọi** cái một chiều *(SQL=người)* ⇒ `F-1`. ⚠ `C8` nối nhật ký ⛔ khoá: tái hiện *(kho TEST, giao dịch lùi)* cùng actor sửa `cdt1` UAT rồi sửa **thật** trong **một** giao dịch ⇒ nhật ký khớp **2** dòng ⇒ `NGUOI chot 0` — **chiều IM** ⇒ `F-2`; đường `fls/api/xu_ly.py::sua` ghi **một** bút toán / yêu cầu ⇒ hôm nay **0** đường chạm |
| **Dữ liệu** *(kho thật, chỉ `SELECT`)* | ✅ **ĐẠT** — sổ ⛔ đổi so với `KQ-010`, trừ ảnh nhịp; mốc B máy in = đếm tay | `fls_itl` **8.387** · `fls_pm_link` **2.263** · `fls_pm_unlink` **1** · `fls_may_goi_y` **4.424** · `fls_sua_tay` **0** · `fls_adjustment` **4.428** · `fls_journal` **4.428** · `fls_queue_event` **110.349** — **8/8** khớp `KQ-010`; `max(evt_id)` **163567** · `max(adj_id)` **163571** · `max(link_id)` **163562** ⇒ ⛔ dòng mới. `fls_pm_line` **249.288 → 256.928** *(+2 ảnh × 3.820, 02/10 02:09 + 03:09 UTC)* · **66 → 68** ảnh; `fls_chup` `nhip@fls` **135** + `nhip@fls(tay)` **10** + `tools/chup_sao_ke.py` **2** = **147** *(khớp bản vẽ `135 · 147`)*. `run_id` ⛔ hình thật trong `fls_pm_line`: **0**. ⚠ Đo 11:18: ảnh mới nhất vẫn **10:09** *(03:09 UTC)* — nhịp ⛔ chụp lượt 11:09; ngoài phạm vi `WO-011`, ghi để người đọc số ảnh biết vì sao ⛔ trôi. `fls_dien_giai` **8.370** / **8.387** |
| **Màn hình** | — **⛔ áp dụng** | `WO-011` ⛔ chạm màn/cửa *(Phạm vi NGOÀI: "⛔ màn hình / cửa API đổi hành vi theo actor")*; `88ab178` chỉ đổi hằng ở `fls/repo/may_ghep.py`, `nhip_chup.py`; `soi_bang_tuyen` 40/40. Máy 8088 ⛔ dựng |

## Tài liệu — 16 chỗ `--ghi` đổi *(đọc **câu**, ⛔ chỉ số)*
| Chỗ | Câu đúng chưa? |
|---|---|
| `master:316` · `:325` | ✅ `103` tệp · `46` hiện vật; *"lạc hậu hơn 1.400"* = 2.051 − 548 = **1.503** — vẫn đúng *(hụt)* |
| `master:343` | ✅ số; ⚠ cùng câu *"`lint-imports` **8** kept"* *(thật 9)* + *"chỉ `.py` của **9** module"* *(dashboard ghi **10** module)* — **câu cũ**, ⛔ do `--ghi` ⇒ `F-3` |
| `dash:116`–`118` | ✅ `2051 (1782 + 269)` cộng đúng; `256.928` · `02/10 10:09` = ảnh `PME7F31617` *(03:09 UTC)* |
| `dash:120` · `banve:1395` | ✅ `135 · 147` = sổ thật; câu *"tự lớn lên mỗi cú chụp"* đúng |
| `dash:131` | ✅ `88ab178` = lần sửa `fls/` gần nhất *(`75d9f85`, `24a8591`, `af34be7` chỉ tài liệu)* |
| `dash:139` · `:145` · `banve:1072`–`1073` · `:1097` · `:1202` | ✅ số |
| `roadmap:45` | ✅ số; ⚠ *"`DEV-02` quy ước **v1.0**"* *(thật **v1.2** — `03_Dev/02` dòng 3)* — câu cũ ⇒ `F-3` |
| `banve:1319` chân trang | ✅ *"Sổ bút toán và nhật ký đã có dòng từ 18/09 — nhưng ⛔ chưa một dòng nào của kế toán"* — người thật **0**, `fls_journal` **4.428** = 4.424 máy + 4 UAT; `68 ảnh · 256.928` khớp. *(`KQ-010 F-4 ⓐ` đã sửa)* |
| `banve:1400` | ✅ `68`; câu đã **trỏ** |

⇒ **16/16** câu cạnh số đúng nghĩa. ⚠ Commit `75d9f85` ghi *"ra 11 chỗ"* — `BG` tự đính chính **16**; biên bản, ⛔ sửa lịch sử.

## Yếu điểm Dev tự khai — tôi soi lại
| # | Yếu điểm | Đo được | Mức · gửi |
|--:|---|---|---|
| 1 | chọn thay BA `HOI-012` câu 1 | `TL-012` đã chấp nhận ⇒ đóng | ✅ |
| 2 | chuỗi SQL mang bản chép | `TL-012` chấp nhận; ép trùng byte **đã chứng ĐỎ** cả hai chiều *(`K3`, `K4`)* | ✅ |
| 3 | khoảng trắng / chữ cái Unicode | **thật, đã đo**: chữ cái lệch **7.405** điểm mã; khoảng trắng *(`U+2000`–`U+200A`, `U+2028`, `U+1680`…)* ⛔ trong tập ⇒ **người** ở **cả hai** mặt | `NHE` · `DEV` *(`F-1`)* |
| 4 | `C8` nối ⛔ khoá | **thật, đã tái hiện** — chiều IM; 0 đường hôm nay | `NHE` · `DEV` *(`F-2`)* |
| 5 | số cạnh `⚠ ACTOR MỚI` = "thao tác" | khớp `AC-3` *(`· 1`)*; bài `KQ-014` ghim `· 3` cho 3 thao tác | ✅ |
| 6 | `T3` ⛔ soi `fls_chup`/`fls_khai_cot` | sổ thật: **5** chuỗi ngoài sổ *(`fls_chup` `tools/chup_sao_ke.py` **2** · `fls_khai_cot` `máy · trích dòng 1 (QĐ-ITL-105)` **464**, `khai-thu-tu@apero.vn` **144**, `claude@fls(bo-thu_tu-tu-them)` **12**, `claude@fls(sua-khai-ACB-USD)` **12**)*; 2 chuỗi có trong mã *(`chup_sao_ke.py:85`, `nap_nguon_va_khai.py:67`)* ⛔ dạng `@` ⇒ bài quét ⛔ bắt | `NHE` · `BA` *(`F-4`)* |
| 7 | câu cũ ⛔ cổng canh | thật — `F-3` | `NHE` · `BA` |
| 8 | `kiem_so_song` 0 là ảnh giờ chạy | đúng thiết kế *(`GAP-CONG-01`)*; tôi đo 11:01, trước ảnh 11:09 | ✅ |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** | `NHE` | `fls/repo/danh_muc_actor.py:100`–`117` *(`la_uat` ↔ `_mau_uat`)* | Quét **1.112.063** điểm mã, chuỗi `'UAT' + chr(c) + 'x'`: SQL `[[:alpha:]]` *(`en_US.utf8`)* nhận **7.405** điểm mã là chữ mà `str.isalpha()` ⛔ *(dấu kết hợp mang thuộc tính Alphabetic: `U+0345`, `U+0363`…`U+036F`, dấu Hebrew `U+05B0`…)* ⇒ SQL **người**, Python **UAT**. **Mọi** lệch một chiều *(ỒN)*; `la_uat` Python **⛔ được gọi** ở đường chạy nào *(grep `fls/`+`tools/`+`docs/ITL/_tools/`: chỉ bài thử)* ⇒ 0 tác động hôm nay, nhưng câu *"một luật, hai mặt"* ⛔ đúng trên toàn Unicode. Kèm: tập khoảng trắng khai tay **9** ký tự ⇒ `U+2003 'UAT …'` là **người** ở cả hai mặt *(spec "bỏ khoảng trắng đầu")*. Kịch bản quét: bài `test_luat_UAT_moi_diem_ma__…` *(BMP — ghim chiều)* | `DEV` *(ghi nhận; đổi định nghĩa "chữ cái" cho hai mặt dùng **một** tập, hoặc `BA` chốt "chữ cái = ASCII")* |
| **F-2** | `NHE` | `docs/ITL/_tools/khop_owner.py:515`–`521` *(`_c8`)* | Kho TEST, một giao dịch lùi: cùng actor `ghi_but_toan(cdt1, reason='UAT 02/10 thu')` rồi `ghi_but_toan(cdt1, 'C-THAT', reason='chot that…', force=True)` ⇒ `fls_sua_tay` hiệu lực = **giá trị thật**, phép nối `(itl_id, field, actor, at)` khớp **2** nhật ký *(cùng `now()`)* ⇒ `NGUOI chot 0` — **chiều IM** *(`Đ5`)*. Hôm nay **0** đường: `fls/api/xu_ly.py::sua` một bút toán / yêu cầu. Nối theo `fls_journal.adj_id`/`jrn_id` *(nếu có)* hoặc lấy **dòng nhật ký mới nhất** thì hết | `DEV` *(ghi nhận — khi đụng `_c8` lần sau)* |
| **F-3** | `NHE` | `master:343` *(`lint-imports` **8** kept · *"chỉ `.py` của **9** module"*)* · `roadmap:45` *(`DEV-02` quy ước **v1.0**)* · `master:324` §8 dòng `03_Dev/` *(`02` v1.0)* | Câu **cũ** cạnh số đúng — ⛔ do `--ghi` đổi *(= yếu điểm 7 của `BG`)*; thật: `lint` **9 kept**, `02_REPO_CONVENTIONS` **v1.2**, dashboard **10** module | `BA` *(câu văn)* |
| **F-4** | `NHE` | `WO-011 T3` phạm vi · `tests/repo/test_danh_muc_actor.py` *(quét chỉ chuỗi `@fls`/`@apero.vn`)* | **5** chuỗi actor ngoài sổ trên `fls_chup`/`fls_khai_cot` *(đếm ở yếu điểm 6)* — hôm nay ⛔ cổng *"người đã làm"* nào đọc hai bảng ấy ⇒ 0 tác động. Hai chuỗi máy trong mã ⛔ mang `@` ⇒ lọt bài quét; lưới cuối là `T3` — nhưng `T3` ⛔ soi đúng hai bảng chúng ghi | `BA` *(quyết: mở rộng `T3`/bài quét sang mọi bảng có cột `actor`, hay ghi rõ "ngoài phạm vi vì …")* |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `tests/nghiem_thu/test_kq014_thuoc_nguoi_tren_duong_ghi_that.py` — **33** bài: UAT ×10 + người ×6 qua `ghep_lenh`/`bo_moi_noi` · `B4` máy ×9 · máy mới chưa khai *(đếm + gọi tên một dòng)* · `C8` qua `ghi_but_toan` · luật UAT trên mọi điểm mã BMP ×5 vị trí *(SQL ⛔ bao giờ IM hơn Python; 4 vị trí phải trùng)* · `B3`/`B4` ảnh cũ bẩn – ảnh hiệu lực sạch | 12 đột biến trên worktree *(mỗi mẫu khớp đúng 1, trả nguyên `sha256` ×12)*: `K1` SQL UAT bỏ điều kiện ký tự sau ⇒ **2** đỏ · `K2` `B4` bỏ vạch máy ⇒ **9** · `K3` chuỗi SQL thiếu `nhip@fls` ⇒ **1** + cổng nổ · `K5` báo actor mới im ⇒ **1** · `K6` luật UAT cũ `left(…,4)` ⇒ **5** · `K7` `C8` bỏ lọc UAT ⇒ **1** · `K8` `C8` bỏ lọc máy ⇒ **1** · `K11`/`K12` `B4`/`B3` đếm mọi ảnh ⇒ **1** *(+ bài Dev `AC7` 1)* | ✅ `33 passed` ×5 lượt |

⚠ Lượt đầu, bài máy-mới **chập chờn** do chính tôi: hai `_mot_dong` trong **một** giao dịch mang cùng `read_at` *(`now()`)* ⇒ `anh_pm_hieu_luc` chọn theo `run_id` ngẫu nhiên. Đã sửa bài *(một ảnh, hai dòng sổ)*; ⛔ phải lỗi mã *(nhịp thật mỗi ảnh một giao dịch)*. Worktree + điểm nối `.venv` đã gỡ; kho TEST ⛔ còn dòng nào của bài *(giao dịch lùi — `kq014` actor đếm **0**)*.

## Trả lời `fls-ba` *(02/10 chiều)*
| F | Quyết | Spec / phiếu |
|---|---|---|
| `F-1` | Sửa — "chữ cái" = ASCII khai tường minh hai mặt *(⛔ `isalpha`, ⛔ `[[:alpha:]]`, ⛔ cờ `~*` trên lớp chữ cái — `U+212A`)*; khoảng trắng ngoài tập khai tay ⇒ người, chấp nhận | `09` **v1.15** §2 ⓓ · [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) `T4` — bài `kq014` ⛔ đổi, phải vẫn xanh |
| `F-2` | Sửa — mỗi dòng `fls_sua_tay` nối **đúng một** dòng nhật ký, ≠ 1 ⇒ ⛔ không đo được. ⚠ Gợi ý *"nối theo `adj_id`"* ⛔ dùng được: `fls_journal` ⛔ có `adj_id`, và `ghi_but_toan` để `fls_adjustment.evt_id` **NULL** *(`fls/repo/ghi_tay.py:403`–`447`)* | `09` **v1.15** §2 ⓔ · `WO-015 T5` |
| `F-3` | Sửa ngay + cùng lớp | master **v0.31** *(§10 `lint` 9 · bốn đuôi / 10 module · `5/10`; §8 6 ô version + số tệp)* · roadmap **v1.1** *(`DEV-02` v1.2 · `DEV-12` v0.9)*; gốc ⇒ `WO-015 T6` *(11 phép so mới)* |
| `F-4` | **Mở rộng** `T3` + bài quét — `fls_khai_cot.actor` mang nghĩa *"người đã xác nhận bản khai"* *(`tools/nap_nguon_va_khai.py:62`–`66`)* ⇒ thuộc `QĐ-ITL-150 ⓐ` | `09` **v1.15** §2 ⓐ ⓒ ⓔ · `WO-015 T1`…`T3` |

## Changelog
- 2026-10-02 chiều · `fls-ba` · trả cả 4 `F` ⇒ `KQ-014` **`DONG`**; nghiệm thu PO `WO-011` ⇒ `DONG`; phát `WO-015`.
- 2026-10-02 trưa · `fls-test` · phát `KQ-014` — ✅ **ĐẠT** `WO-011` *(10/10 AC)*; 4 `F` `NHE` *(`F-1`, `F-2` `DEV` ghi nhận · `F-3`, `F-4` `BA`)*; +33 bài `kq014`; đóng `KQ-010` *(`F-2`, `F-3` xử ở `WO-011`; `F-1` đã lấp; `F-4` `BA` đã sửa)*.
