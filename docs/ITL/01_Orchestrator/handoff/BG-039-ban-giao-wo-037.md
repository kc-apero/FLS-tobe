# BG-039 — bàn giao `WO-037`

| | |
|---|---|
| **Thuộc** | [`WO-037`](WO-037-de-xuat-dau-khong-khac-tien-te-va-ba-ca-bien-bac.md) vòng **1** · kèm [`HOI-038`](HOI-038-o-giao-dich-doc-vi-sao-tu-dau-va-cau-nao.md) *(`KHONG_CHAN` — làm theo phương án **B**)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`4c3b2ae`** *(mã + bài + giấy `03_Dev` + `HOI-038`, đã đẩy)* · tờ này + `WO`/README/dashboard ở commit giấy ngay sau |
| **Nền khi nhận** | git `8d7bea2` = `origin` ✔ · `BA-07` **v3.9** · `BA-06` **v4.16** · `BA-08` **v1.3** ✔ *(header khớp `Spec`)* · `WO` đủ mọi trường `10` §3.1 ✔ · ⭐ nền sổ thật đo lại ở cổng vào, **cùng ảnh** `fls-ba` *(`NAP-2026-10-02-PMA07ED283`)*: `may` **268** · `nguoi` **532** · `khong` **801** · `tu_chung` **64** · `tong` **1.601**; rổ `may` có `the.gd` khác tiền tệ **84 / 268** — khớp từng số `WO` |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/lenh_cho.py` | `(a)` `xep_ro`: lệnh vào `may` ⇔ có dòng khớp mã **và** `ma_tien_te(curr) == ma_tien_te(curr lệnh)` *(tuple `chi_muc_ma` đã mang `curr` — ⛔ SQL mới)*; khớp mã **chỉ** khác tiền tệ ⇒ `ro = 'nguoi'`, `vi_sao` = khoá mới **`ma_khop_khac_tien_te`** *(câu có chỗ trống `{ma}` ở `VI_SAO`, gắn bằng `cau_ma_khop_khac_tien_te` — mã tiền tệ **thật** của dòng khớp)*, `ung_vien_itl = []`, `tu_chung = False`; `ung_vien_itl` của rổ `may` chỉ mang dòng mã **cùng** tiền tệ. Hàm mới `la_khop_ma_chi_khac_tien_te(d)` *(đúng nhánh của `xep_ro`)*. `(b)` `ung_vien_itl()`: khoá xếp `(bậc, khác tiền tệ?, lech, itl_id)`; `cur_lenh` qua `ma_tien_te` *(bỏ bản `strip().upper()` tay)*. `ma_tien_te` nhập **trong hàm** *(`man_ghep` nhập `lenh_cho` ở đầu tệp — vòng nhập)* |
| `fls/api/xu_ly.py` | `(c)(d)` `_bac`: `ma` › **khác tiền tệ ⇒ `khac_tien_te`** › `tien` › `cung_tien_te` *(giống `/so`)*, so bằng `mg.ma_tien_te` *(KQ-036 `F-1`/`F-2`)*. `(g)` `_gd_vao_the`: `the.vi_sao` **chỉ có** khi `gd = null` ∧ `lc.la_khop_ma_chi_khac_tien_te(d)` — `HOI-038` B |
| `fls/web/tep/man_f01_ghep.js` | `(e)` `ve_dang_gan`: bậc lạ ⇒ chip **nguyên tên** *(cùng luật `ve_ung_vien`)*; bậc vắng *(`loi_nguon`)* ⇒ ⛔ chip. `(g)` `ve_o_gd`: `!gd ∧ d.vi_sao` ⇒ in **đúng câu cửa** + `title`, chữ thường của bảng *(⛔ lớp `none` = `--faint`)*; chú thích *"năm câu"* → *"sáu câu"* |
| `fls/web/tep/hinh.css` | `(f)` `.tlegend` chữ ⇒ `--muted` · `.cand .tg` gốc ⇒ `--muted` *(⛔ token mới, ⛔ lớp mới; tông `.cand.good/.info/.warn .tg` ⛔ đổi)* |
| `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py` *(mới, 14)* | `AC-1` ×4 *(HTTP kho TEST)* · `AC-3` · `AC-4` *(HTTP)* · `AC-5` ×4 tham số + quét AST `xu_ly.py` + bài quét tự chứng bắt được mẫu cũ · `the.vi_sao` chỉ-có-ở-nhánh · ⭐ `AC-2` **sổ thật chỉ đọc** |
| `tests/web/test_wo037_man_cua_that.py` *(mới, 7)* · `tests/web/ca_wo037.py` *(mới)* | `AC-8` ×2 *(câu thứ sáu · hồi quy `đề xuất:`)* · `AC-4` DOM · `AC-6` · `AC-7` ×2 + cổng tương phản tự chứng *(`--faint` 2,17 / 2,47; `--muted` 4,92)*. Ca chung sáu lệnh `K W S Y G M` *(một lần nạp, kho TEST, tiền + mã ngẫu nhiên)* |
| `tests/web/test_wo032_quet_khoa_cua_that.py` · `tests/web/ca_wo032.py` | `(h)` mở rộng cổng quét: ⭐ bản đồ `GHEP` **thiếu** đường `ro=nguoi` dù chip `Chưa gán` gọi nó *(`CHIP_CUA`)* — lộ ra khi lệnh `X` rời `may`; thêm `GHEP_NGUOI` + bài `test_WO037_ve_o_gd_doc_VI_SAO_va_CUA_THAT_tra_no_o_the` *(mẫu số in: **1** thẻ cửa thật mang `the.vi_sao`)* |
| `tests/api/test_wo032_khuon_cua_pg.py` | `test_AC2_lech_BON_cua…` **viết lại MỘT vế** — tiền đề đổi theo `BA-07` v3.9 §4h ⓵' *(`the.gd` chưa gán ⛔ bao giờ khác tiền tệ ⇒ cửa `lenh-cho` ⛔ còn ca khác tiền tệ)*: vế mẫu số `c >= 1` của `lenh-cho` **đảo** thành `c == 0`; nhánh `null` vẫn đo ở ba cửa kia, quan hệ `lech` vẫn chạy trên **mọi** phần tử bốn cửa. Lý do ghi trong docstring *(tiền lệ `test_nut_GOP_…`)*; đột biến `T15` ⇒ ĐỎ |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `12_P6_WEB_PLAN.md` **v0.15** | dòng nhật ký · *quy ước thứ tám* *(đề xuất của máy phải là thứ cửa ghi nhận; khi ⛔ đề xuất, cửa nói vì sao, màn chỉ in)* |
| `handoff/HOI-038-…` *(mới)* | `MAU_THUAN` + `THIEU`: `(g)` *"`vi_sao` có"* ⟷ `BA-06` v4.16 *"`vi_sao = ma_khop_khac_tien_te`"* + `Dữ liệu` **84**; màn đọc `the` mà `the` ⛔ có `vi_sao` |

## Cổng *(kết quả nguyên văn, `PG_DSN='postgresql://fls:fls@localhost:5433/fls'`, `PYTHONUTF8=1`, mã `4c3b2ae`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `3 failed, 2246 passed, 3 xfailed in 333.93s (0:05:33)` — **3 failed = đúng 3 `[XPASS(strict)]` `kq036`** *(`test_F1_bac_gd_so_tien_te_CUNG_LUAT…` · `test_F2_gd_ds_KHAC_tien_te…` · `test_F3_khoi_DANG_GAN_bac_LA…` — đúng ý, `fls-test` gỡ dấu)*; 3 `xfailed` = 3 `kq021` *(`WO-023`)* ⛔ đổi. ⭐ `pytest --runxfail tests/nghiem_thu/test_kq036_bac_gd_khac_tien_te_va_bac_la.py` ⇒ `6 passed in 2.40s` |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 49 lech/khong-do-duoc` — **nền đầu phiếu `49`** *(`WO` bảng nền)* ⟷ **đỏ mới loại (c): `0`** — so **tên** 49 dòng lệch với danh sách nền `KQ-036` *(`kss_sau.ten`)*: chỉ-ở-nền **0**, chỉ-ở-mới **0** ⇒ `49 + 0 = 49`. ⚠ Chạy kèm trên worktree `8d7bea2` ⛔ được *(tiến trình con gọi đường `.venv` tương đối ⇒ `FileNotFoundError`)* — đối chiếu tên thay cho chạy song song. ⛔ `dong_bo --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (128 file, 1432 bang, 679 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(trước tờ này)* · chạy lại sau tờ này + `WO`/README/dashboard: `(129 file, 1439 bang, 679 o ngay, 104 ma QD)` ✅; `khop_owner --kiem` + `kiem_so_song` chạy lại: ⛔ đổi *(C1 ĐẠT · 49)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` *(= nền)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến mới)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — phiếu ⛔ chạm schema *(0 tệp `fls/db/**`, 0 migration)* |

⭐ **Đột biến** *(kịch bản `scratchpad/dot_bien.py`, áp → chạy bài đích → trả nguyên, `bytes ==` ✓)*: **15 / 15** bị bắt — T1 `xep_ro` ⛔ so tiền tệ *(2 failed)* · T2 so ⛔ `trim` · T3 sắp ⛔ khoá tiền tệ · T4 hạ mã khác tệ dưới bậc tiền · T5 `_bac` bỏ nhánh `khac_tien_te` *(2)* · T6 `_bac` `.upper()` ⛔ trim *(3)* · T7 `the.vi_sao` cho mọi hàng · T8 chở câu dưới tên `ly_do` *(3 — gồm cổng quét)* · T9 `ve_dang_gan` bỏ chip bậc lạ *(+ `kq036 F-3` quay về `xfailed`)* · T10 `ve_o_gd` ⛔ nhánh `vi_sao` · T11 câu gõ ở JS · T12 câu lớp `none` *(faint)* · T13 `.tlegend` `--faint` · T14 `.cand .tg` `--faint` · T15 bài `WO-032 AC-2` viết lại.

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Chiều ĐỎ đã chạy |
|---|---|---|
| **AC-1** *(a · kho TEST)* | `test_AC1_khop_ma_CHI_khac_tien_te_vao_ro_NGUOI_kem_vi_sao_ma_tien_te` *(lệnh VND `K` ↔ USD mã `K`: `?ro=nguoi` chứa, `?ro=may` ⛔ chứa, `vi_sao` = `cau_ma_khop_khac_tien_te(['USD'])` ∋ `USD` + `tiền tệ`, `the.gd is None`)* · `…them_dong_VND_cung_ma_thi_lenh_VE_ro_MAY…` *(thêm VND mã `W` ⇒ `may`, `ung_vien_itl == [id VND]`, `gd.curr == 'VND'`)* · `…KHOANG_TRANG_la_CUNG_tien_te` *(`' vnd '` ⇒ `may`)* · `…dem_theo_ro_KHEP…` *(`/lenh-cho/ro` = hai danh sách)*. ⚠ rổ `may` = **hợp** `tu_chung=0` ＋ `=1` *(lệnh `S` là tự chứng)* | mã `8d7bea2` ⇒ `K` ∈ `may` ĐỎ · `W` ⛔ ở `nguoi` ĐỎ · T1 · T2 ⇒ ĐỎ |
| **AC-2** *(a · sổ thật CHỈ ĐỌC)* | Kịch bản `scratchpad/do_ac2.py` *(`noi_chi_doc(dsn_that())`, `SHOW default_transaction_read_only` = `on`; gọi **hàm thật** `lc.dem_theo_ro` + `xu_ly.lenh_cho` mọi trang `ro=may`/`ro=nguoi` + `lc.ung_vien_itl` ×N)* chạy **nền** *(mã `8d7bea2`, 93,8 s)* và **sau** *(mã mới, 69,8 s)* — **cùng ảnh** `NAP-2026-10-02-PMA07ED283` *(in ở cả hai)*. Kết quả dưới. ⭐ Kèm bài `test_AC2_SO_THAT_chi_doc_ro_MAY_KHONG_de_xuat_dong_khac_tien_te` *(in: `may 184 · gd khác tiền tệ 0 · nguoi 616` · `nguoi mang vi_sao ma_khop_khac_tien_te 84`)* | mã `8d7bea2` ⇒ bài ĐỎ `84 lệnh rổ may đề xuất dòng khác tiền tệ: ['PM01089-1', 'PM01689-1', …]` |
| **AC-3** *(b)* | `test_AC3_bac_MA_cung_tien_te_TRUOC_khac_tien_te_TRUOC_bac_tien` *(lệnh `Y`: USD mã `itl_id` nhỏ · VND mã `itl_id` lớn · VND ⛔ mã đúng tiền ⇒ `[ma VND, ma USD, tien VND]`)*. Sổ thật: lệnh rổ `may` có **cả hai** loại dòng mã **0** *(nền 0 / 268, sau 0 / 184)* ⇒ `⛔ tập rỗng — đo ở kho TEST` *(`Đ3`)* | mã `8d7bea2` ⇒ `[4, 5, 6] != [5, 4, 6]` ĐỎ · T3 · T4 ⇒ ĐỎ |
| **AC-4** *(c · `F-2`)* | HTTP: `test_AC4_gd_ds_KHAC_tien_te_khong_khop_ma_la_bac_KHAC_TIEN_TE` *(mối nối VND ↔ USD mã khác: `gd_ds.bac == 'khac_tien_te'`, `lech is None`; `gd` cũng)* · DOM thân cửa thật: `test_AC4_khoi_DANG_GAN…` *(chip `≠ khác tiền tệ`, `title` `khác tiền tệ`)* · `--runxfail …::test_F2_*` ⇒ passed | mã `8d7bea2` ⇒ `'cung_tien_te' == 'khac_tien_te'` ĐỎ · T5 ⇒ ĐỎ |
| **AC-5** *(d · `F-1`)* | `test_AC5_bac_so_tien_te_CUNG_LUAT…` ×4 *(`' vnd '`↔`VND` ⇒ `tien`, ăn khớp `lech_ung_vien`)* · `test_AC5_QUET_xu_ly_KHONG_co_phep_so_tien_te_viet_rieng` *(AST: mọi `Compare ==/!=` có vế `.upper()/.lower()/.casefold()` ⇒ 0; ∋ `mg.ma_tien_te(`)* · `test_AC5_QUET_bat_duoc_mau_cu` *(mẫu nguyên văn `KQ-036 F-1` ⇒ bắt 1)* · `--runxfail …::test_F1_*` ⇒ passed | mã `8d7bea2` ⇒ 3/4 tham số ĐỎ + quét bắt `xu_ly.py:764` · T6 ⇒ ĐỎ |
| **AC-6** *(e · `F-3`)* | `test_AC6_khoi_DANG_GAN_bac_LA_in_NGUYEN_TEN` *(thân `lenh-da-gan` cửa thật, đổi **giá trị** `bac` ⇒ `'xyz'`: chip chứa `xyz`, `title` `xyz`)* · `--runxfail …::test_F3_*` ⇒ passed | T9 ⇒ ĐỎ *(chip `null`)* |
| **AC-7** *(f · `F-4`)* | `test_AC7_tuong_phan…DAT_NFR_I29` ×2 — đọc `hinh.css` → `tokens.css` → WCAG: `.tlegend --muted trên --page = 4.92 : 1 (ngưỡng 4.5)` · `.cand .tg --muted trên --surface = 5.59 : 1 (ngưỡng 3.0)`; `test_AC7_cong_tuong_phan_BAT_DUOC_faint` *(2,17 / 2,47 / 4,92)*. Chrome 8099 `getComputedStyle`: chú giải **9 / 9** phần tử *(5 mục + 4 dấu `·`)* `rgb(92,107,104)` trên `rgb(238,241,241)` = **4,92** · ô `.tg` `④` **5,59** · ô `≠` *(Toàn sổ)* **5,59**. `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh *(trong `pytest` trọn)* | T13 · T14 ⇒ ĐỎ; 8098 *(mã cũ, cùng ca)*: chú giải **2,17**, ô `④`/`≠` **2,47** |
| **AC-8** *(g)* | `test_AC8_o_GIAO_DICH_lenh_khop_ma_khac_tien_te_in_DUNG_cau_vi_sao_cua_cua` *(thân `lenh-cho` cửa thật: ô = **đúng** chuỗi `vi_sao`, ⛔ `đề xuất:`, ⛔ `chưa chọn`, ⛔ lớp `none`, `title` = câu)* · `…nam_cau_cu_KHONG_doi` *(lệnh `M` rổ `may` ⇒ vẫn `đề xuất: …`)*. Tương phản Chrome 8099: `rgb(20,32,30)` trên trắng **16,73** | mã `8d7bea2` ⇒ `K` ⛔ ở `nguoi` ĐỎ · T10 · T11 · T12 ⇒ ĐỎ |
| **AC-9** ⭐ *(Chrome chuột thật)* | Kịch bản `scratchpad/wo037/soi_test.mjs` *(1440×900, `Input.dispatchMouseEvent`)* trên ca kho TEST `NAP-2000-01-01-T376AEE4D`, **cùng ca** trên hai máy: **8099** `--cho-ghi` mã `4c3b2ae` ⟷ **8098** `--cho-ghi` worktree `8d7bea2`. Bảng dưới. Sổ thật: `soi_that.mjs` trên **8097** *(mã mới, ⛔ `--cho-ghi`, Chrome chặn mọi lượt ⛔ `GET`)* ⟷ **8096** *(worktree `8d7bea2`, cùng chế độ)*. **8088 ⛔ chạm** *(PID 15148 nghe trước và sau)*. Bốn máy **đã tắt** sau đo | 8098: ①②④ sai **3 / 3** + chip `G` sai; 8096: hai lệnh vẫn `đề xuất:` USD |
| **AC-10** | Bảng cổng trên | — |

### AC-2 — sổ thật chỉ đọc, nền ⟷ sau *(ảnh `NAP-2026-10-02-PMA07ED283` ở **cả hai**)*
| Đo gì | Nền *(mã `8d7bea2`)* | Sau *(mã `4c3b2ae`)* |
|---|---|---|
| `dem_theo_ro` | `may` **268** · `nguoi` **532** · `khong` **801** · `tu_chung` **64** · `tong` **1.601** | `may` **184** · `nguoi` **616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601** |
| ⓘ lệnh rổ `may` có `the.gd` khác tiền tệ *(mẫu số = số hàng `may`)* | **84 / 268** | **0 / 184** |
| ⓘⓘ tập rời `may` *(nền)* ⟷ tập `nguoi` mang câu `ma_khop_khac_tien_te` *(sau)*, so **`pm_line_id`** | 84 | 84 — **trùng đúng**: `nền − sau` **0** · `sau − nền` **0**; cả 84 `gd = null`, `ung_vien_itl = []` |
| ⓘⓘⓘ `Chưa gán` = `may` ＋ `nguoi` | **800** | **800** ⛔ đổi |
| mã tiền tệ trong câu `vi_sao` *(của dòng khớp)* | — | VND **60** · USD **21** · SGD **3** *(= `Q-FX-1`: USD→VND 60 · VND/SGD/HKD→USD 15+5+1 · USD→SGD 3)* |
| `nguoi` có `gd` khác tiền tệ | 0 | 0 |
| `the.vi_sao` có mặt *(mọi hàng `may` ＋ `nguoi`)* | 0 | **84** — đúng tập trên |
| `AC-3` sổ thật: lệnh `may` có cả hai loại dòng mã · sai thứ tự | 0 · 0 | 0 · 0 *(⛔ tập rỗng — đo ở kho TEST)* |

### AC-9 — Chrome
| Ca | **8099** *(mã mới · kho TEST)* | **8098** *(mã `8d7bea2` · cùng ca)* |
|---|---|---|
| ① `② Hàng chờ` → chọn `VND` → lệnh `K` | nút hàng **`Tra tiền`** *(rổ `nguoi`)*, `hint` = câu `vi_sao` *(USD)* | `Mở để chia` *(rổ `may`)*, ⛔ `hint` |
| ① `②b Gán lệnh chi` → chip `Chưa gán` → hàng `K`, ô *Giao dịch đã gán* | **đúng câu** `số chứng từ khớp một dòng tiền bằng USD — cửa ghi ⛔ không ghép hai tiền tệ; ⛔ không ghép theo một số tiền trùng` · `title` = câu · `rgb(20,32,30)` / trắng **16,73** | `đề xuất: ⛔ chưa đọc được nội dung OCBC · ••4321 · K376…` · `--warn` **3,35** |
| hồi quy: hàng `M` *(rổ `may`)* | `đề xuất: …` *(⛔ đổi)* | như bên trái |
| ② mở `Y` *(chuột)* — 3 ứng viên đầu | `① ma VND` › `① ma USD` › `② tien VND` | `① ma USD` › `① ma VND` › `② tien VND` |
| ③ bấm ô `.tg` dòng USD, rồi `Gán` một lần | thanh: `Khác tiền tệ — cửa ghi sẽ từ chối cặp này.` → `Xác nhận gán 243.503,00 USD (khác tiền tệ — cửa ghi sẽ từ chối) ?` · **0** lượt ⛔ `GET` | như bên trái *(⛔ hồi quy `WO-032`)* |
| ④ chú giải *(9 phần tử)* · ô `.tg` `④` · ô `≠` *(Toàn sổ, gõ mã ca)* | **4,92** · **5,59** · **5,59** *(`≠` `title` `khác tiền tệ`)* | **2,17** · **2,47** · **2,47** |
| ⑤ chip `Đã gán` → `G` | `≠ khác tiền tệ` | `④ cùng đơn vị tiền` |
| console · lượt ⛔ `GET` | **0** · **0** | 0 · 0 |

| Sổ thật | **8097** *(mã mới, chỉ đọc)* | **8096** *(mã `8d7bea2`, chỉ đọc)* |
|---|---|---|
| `PM00329-1` *(VND)* — rổ · ô *Giao dịch* | `nguoi` · `số chứng từ khớp một dòng tiền bằng USD — …` · `gd null` · `the.vi_sao` có | `may` · `đề xuất: Bank fee - PAYMENT CONTRACT …` *(USD)* |
| `PM01089-1` *(HKD)* | `nguoi` · cùng câu *(USD)* | `may` · `đề xuất: BANK FEE 2025-09-29 · OCBC …` *(USD)* |
| mở `PM00329-1` — ứng viên đầu | `① ma USD` ×2 › `② tien VND` ×2 *(⛔ đổi — dòng mã khác tệ vẫn trên bậc tiền, `BA-07` v3.9)* | như bên trái |
| `F01G` chip `Chưa gán` · cửa `?ro=may` / `?ro=nguoi` *(lật trang)* | 736 hàng · **184** / **616** | 736 · 268 / 532 |
| console · Chrome chặn ⛔ `GET` · phát ra ⛔ `GET` | 0 · 0 · 0 | 0 · 0 · 0 |

## Kho thật
- **`KHONG_CHAM`** — ⛔ ghi. Chỉ đọc: ⓐ `do_ac2.py` nền + sau *(`noi_chi_doc`, `read_only = on` được assert)*; ⓑ bài `test_AC2_SO_THAT_chi_doc_…`; ⓒ máy **8097** + **8096** *(⛔ `--cho-ghi`, Chrome chặn mọi lượt ⛔ `GET` — bị chặn **0**, phát ra **0**)*, **đã tắt**. **8088 ⛔ chạm**. Mọi ca dựng ở **kho TEST** `fls_test` *(run `NAP-2000-01-01-T37…`)*.

## Cách chạy để xem *(chạm UI)*
- Kho TEST, ghi được: `PG_DSN=…/fls_test` + `FLS_JWT_SECRET` ⇒ `python tools/chay_cua.py --cong 8099 --cho-web --cho-ghi`; ca: `tests/web/ca_wo037.dung_ca_wo037` trên kho TEST *(in mã lệnh `K W S Y G M`)*. `②b Gán lệnh chi` → `Chưa gán` → hàng `K` *(ô Giao dịch = câu)* · mở `Y` *(thứ tự ứng viên; bấm ô `.tg` dòng USD)* · `Đã gán` → `G` *(chip `≠`)*.
- Sổ thật chỉ đọc: `python tools/chay_cua.py --cong 8097 --cho-web` *(⛔ `--cho-ghi`)* — `②b` → `Chưa gán` → `PM00329-1` / `PM01089-1`.

## Dev tự thấy còn yếu
1. ⭐ **`HOI-038` — `the.vi_sao` là một khoá MỚI trong `the`**, trái chữ *"⛔ khoá mới"* của `WO-037 Dữ liệu`; tôi chọn phương án **B** *(chỉ có ở nhánh khớp-mã-khác-tiền-tệ ⇒ đúng **84** ô như `BA-06` v4.16)* thay vì đọc nguyên văn `(g)` *(**616** ô)*. `BA-07` chưa khai khoá ấy. Nếu `TL-038` chọn A/C: đổi **một** `if` ở `_gd_vao_the` + một dòng JS.
2. ⭐ **Thẻ rổ `nguoi` ở `F01L` giờ nói sai cho 84 lệnh** — `F01L` *"CẦN BẠN tra bằng tiền + ngày — ⛔ Chưa có số chứng từ. Đây là việc thật của kế toán."* *(ảnh Chrome 8099)*: rổ `nguoi` nay có **84 / 616** lệnh **có** số chứng từ. `WO` NGOÀI *"⛔ đổi `F01L`"* ⇒ tôi ⛔ sửa; **câu cho `fls-ba`**. Tương tự: hàng ⚠ *"Còn N dòng khớp số chứng từ nhưng lệch tiền"* của thẻ rổ `may` — chưa soi nó đếm thế nào sau đổi rổ.
3. **SQL bậc tiền vẫn so `upper(i.curr) = s.cur` ⛔ `trim`** *(`lenh_cho.py` `_SQL_ITL_UNG_VIEN` / `_SQL_DEM_CUNG_TE` — `WO` Rủi ro 2, NGOÀI)*. Hệ quả **suy từ mã, ⛔ đo**: một dòng `' vnd '` ⛔ khớp mã sẽ ⛔ bao giờ hiện ở ba bậc tiền của `itl-candidates` cho lệnh VND *(SQL ⛔ trim)*, trong khi rổ + bậc `ma` *(Python)* coi nó là VND. Sổ thật **0** giá trị `curr` có khoảng trắng *(`KQ-036`)* ⇒ 0 ca hôm nay.
4. **Câu `vi_sao` mang hai dấu `⛔`** *(theo chữ `BA-07` §4g ⓹ ⓐ + giọng `VI_SAO` cũ)*. `F01L` vẽ `⛔` thành biểu tượng tròn đỏ giữa câu *(ảnh Chrome 8099 `hint`)*; `man_f01*.js` **ngoài** `THEO_LUAT` của `test_luat_ky_hieu_man_hinh.py` nên ⛔ cổng nào canh. Câu ⛔ thuộc thẩm quyền Dev.
5. **`AC-1` *"rổ `may`"* = hợp hai danh sách `tu_chung=0` ＋ `=1`** — chip `Chưa gán` của `F01G` chỉ gọi `tu_chung=0`; lệnh tự chứng *(`S`)* ⛔ hiện ở màn ghép *(như trước phiếu)*. Bài đo đúng rổ, ⛔ đúng màn.
6. `kiem_so_song` nền đo bằng **đối chiếu tên** với danh sách `KQ-036` *(`kss_sau.ten`)*, ⛔ chạy song song trên `8d7bea2` *(worktree ⛔ chạy được — xem bảng cổng)*. Hai danh sách trùng 49/49, nhưng danh sách nền là của **lượt `KQ-036`**, ⛔ của giờ nhận phiếu.
7. `ma_tien_te` nhập **trong hàm** ở hai chỗ `lenh_cho.py` *(vòng nhập `man_ghep` ↔ `lenh_cho`)*. Đúng một hàm, nhưng một người sau có thể *"gọn lại"* bằng `strip().upper()` tại chỗ — bài quét AST `AC-5` chỉ quét `xu_ly.py`, ⛔ quét `lenh_cho.py` *(đột biến T2 vẫn bị `AC-1` bắt bằng hành vi)*.
