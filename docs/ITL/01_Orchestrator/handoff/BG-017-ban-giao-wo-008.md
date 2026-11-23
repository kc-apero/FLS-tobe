# BG-017 — bàn giao `WO-008` *(vòng 1)*

| | |
|---|---|
| **Thuộc** | `WO-008` — chữ trên màn sau một cú bỏ ghép *(`KQ-007` `F-1`…`F-3`)* |
| **Phát bởi** | `fls-dev` · 2026-10-02 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`948ffb6`** *(`T0` — `dong_bo_so_song --ghi`, commit riêng, **trước** mã)* → **`69f03f6`** *(mã + 11 bài + `HOI-016` + changelog)* — **đã đẩy**. Phiếu này + `WO` `CHO_TEST` + nhật ký + `README` ở commit kế tiếp *(⛔ chạm `fls/`, `tests/`)* |
| **Spec** | `BA-06` **v4.8** *(`:878` mục ⓔ đoạn v4.8 · `:1179` dòng "F01/F02 · nút Bỏ ghép" · `:1190` dòng "F02 · nhật ký trong drawer")* · `BA-10` **v0.8** `DT-I14` *(`:97` định nghĩa `bo_qua` · `:99` "Nhật ký của bản đảo — đọc thế nào")* — dòng `Version` đầu tệp khớp |

## Cổng vào
| Kiểm | Đo | |
|---|---|---|
| git thật | `HEAD` = `origin/feat/p2-oracle-parity` = `d761d0f` *(`git rev-parse` cả hai)* | ✅ |
| version hợp đồng | `06_SCREEN_SPEC.md:3` **v4.8** · `10_DECISION_TABLE.md:3` **v0.8** = `WO` | ✅ |
| run id | `WO` ⛔ nói "đã chạy" | — |
| `WO` đủ trường `10` §3.1 | đủ | ✅ ⇒ ⛔ `HOI` chặn |

## `T0` — dọn nền trước khi sửa mã *(`948ffb6`)*
`kiem_so_song` trên `d761d0f` sạch: `⛔ CONG SO SONG KHONG DAT — 8 lech/khong-do-duoc` trên **7** phép *(phép thử `2051 → 2084` ×6 · bài ngoài module `269 → 302` · số tệp `103 → 105`)* — **đúng** số `WO` đo. `dong_bo_so_song --ghi` **một lần** ⇒ `7 muc soan · 0 muc BO QUA` ⇒ `✅ cong so song DAT — 110 phep so … (commit 88ab178)`.

Câu cạnh số *(`10 §6 ⓑ`)* — rà từng chỗ, **⛔ câu nào phải sửa**:
| Chỗ | Số đổi | Câu cạnh |
|---|---|---|
| master §8 tiêu đề | `103 → 105` file `.md` | ✅ chỉ là số |
| master §8 ô `04_Test/` | `2051 → 2084 test` | ✅ *"lạc hậu hơn 1.400 phép thử"* so với `548` — `2084 − 548 = 1.536` ⇒ vẫn đúng |
| master §10 · roadmap · dashboard §1 | `2051 → 2084` · `269 → 302` | ✅ chỉ là số |
| bản vẽ thẻ + chân trang | `2051 → 2084` | ⚠ chân trang ghi *"commit `88ab178`"* cạnh `2084` — hash là phép so riêng của công cụ *(nhóm "nhánh · commit" = lần sửa `fls/` gần nhất)*, ⛔ đổi ở `T0` vì `fls/` chưa đổi từ `88ab178`. Lượt `--ghi` kế tiếp sẽ đổi cả hai |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f02.js` | `F-1`: bảng ⑦ gọi `_nk_thanh(x)` + `_nk_nguon(value_source)` *(mới, ngay trên `_nhom`)*. `may_goi_y` có giá trị ⇒ `gợi ý: <b>X</b>`; rỗng *(`null`/`''`)* ⇒ `rút gợi ý`; mã khác ⇒ như cũ. Nhãn: `may_goi_y` ⇒ **"máy gợi ý · không đổi Final"** · `sua_tay` ⇒ "người sửa" · khác ⇒ in nguyên mã *(tra bằng `hasOwnProperty` — ⛔ mã như `constructor` lọt nhãn)* |
| `fls/web/tep/man_f01.js` | `F-2`: `_o_duy_nhat(dao)` — tên ô theo thứ tự xuất hiện đầu; câu *"↩ Đã rút gợi ý máy trên **N ô** (cdt1, hd)"* + *"· M bút toán, gồm lớp gợi ý cũ bị đè"* khi `M > N`. Khối `bo_qua` in thêm `= giá trị` *(`HOI-016` ⓐ)* |
| `fls/web/tep/man_f01_ghep.js` | `F-3`: `bo_gan` giữ thân `unmatch`; sau `mo_lenh` — `bo_qua` ⛔ rỗng ⇒ `F01._bao_bo_ghep(than)` *(chính hàm dựng của `F01`, ⛔ bản câu thứ hai)* |
| `tests/web/test_wo008_chu_man_sau_bo_ghep.py` | **8** bài DOM *(khuôn `khung_node`)*: `AC-1` ×3 · `AC-3` ×2 · `AC-4` ×3 *(có mục · rỗng · cửa lỗi)* |
| `tests/web/test_wo008_than_that_bo_ghep_pg.py` | **3** bài: dòng **B** dựng **qua cửa HTTP thật** trên kho TEST *(`match` → `ghi_goi_y_may` lớp A → `/adjust` người `HD-K7B` force → `ghi_goi_y_may` lớp B → `unmatch` → `GET /journal`)*, rồi đưa **chính thân trả** vào `F02` ⑦ *(`AC-2`)*, hộp `F01` *(`AC-3`)*, màn ghép *(`AC-4`)* |
| `handoff/HOI-016-…` | `KHONG_CHAN` — ⓑ `value_source` của cú `/adjust` = nguồn **trước** khi gõ · ⓐ khối `bo_qua` in giá trị |
| `03_Dev/08_CHANGELOG_RELEASE.md` | dòng `WO-008` |

## Cổng *(kết quả nguyên văn, `PG_DSN=…/fls`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` *(cây `69f03f6`)* | `2095 passed in 282.50s (0:04:42)` — ⛔ `xfail`, ⛔ `XPASS`, ⛔ `skipped`. Nền `KQ-014` **2.084** ⇒ **+11** = 8 + 3 bài mới |
| `python tools/kiem_so_song.py` — sau `T0` *(`948ffb6`)* | `✅ cong so song DAT — 110 phep so, moi phep khop DUNG mot lan va khop dung con so MAY do (commit `88ab178`)` ⇒ **nền 0 lệch** |
| `python tools/kiem_so_song.py` — `69f03f6` + khung `BG-017` | `⛔ CONG SO SONG KHONG DAT — 20 lech/khong-do-duoc` — **cả 20 là loại (c) của chính phiếu này**: phép thử `2084 → 2095` ×5 · trong module `1782 → 1793` ×2 · dòng `fls/` `25.133 → 25.213` ×4 · module `web` dòng `8.547 → 8.627` ×2 · bài `448 → 459` ×2 · hash `88ab178 → 69f03f6` ×2 · số tệp `105 → 107` ×1 *(`HOI-016` + `BG-017`)*. ⛔ chạy `--ghi` *(`AC-6`, `10 §6 ⓒ`)* — `fls-ba` quyết lượt kế tiếp |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (106 file, 1262 bang, 648 o ngay, 104 ma QD)` *(trước khi viết thân `BG-017`)* ⇒ chạy lại sau khi viết `BG-017` + `WO`/`README`/dashboard: `✅ cong tai lieu DAT — … (107 file, 1268 bang, 648 o ngay, 104 ma QD)`; `kiem_so_song` lúc ấy vẫn **20** lệch *(cùng 20 dòng)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến nào đổi)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` *(⛔ nút mới — hộp chỉ có `Đã hiểu`)* |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — phiếu ⛔ chạm schema *(`git diff d761d0f 69f03f6 -- fls/db` rỗng)*; `WO` cấm migration |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Chiều ĐỎ *(đã chạy)* |
|---|---|---|
| **AC-1** | `test_wo008_chu_man_sau_bo_ghep.py::test_AC1_nhat_ky_BON_loai_dong__…` — bảng ⑦ đọc bằng `HTMLParser` từng ô, mẫu số **4** hàng: thành `["gợi ý: HD-A", "rút gợi ý", "C-NGUOI", ""]` · nguồn `[máy…×2, người sửa ×2]`. Kèm `::…NGUON_LA_thi_in_NGUYEN_MA…` *(`UNMAPPED`, rỗng ⇒ in nguyên)* + `::…rong_van_noi_nhat_ky_trong` | **Mã cũ** `d761d0f`: ĐỎ `['HD-A', '', 'C-NGUOI', '']`. Đột biến `M1` *(thành về `TP.chu(value_after)`)* + `M2` *(nguồn in mã thô)* ⇒ mỗi cái đỏ **2** bài *(AC-1 + AC-2)* |
| **AC-2** | `test_wo008_than_that_bo_ghep_pg.py::test_AC2_…` — kho TEST, dòng B qua cửa thật: **5** bản đảo trong `fls_adjustment` *(mẫu số ≥ 4)*, nhật ký có đúng **5** dòng `may_goi_y` rỗng; màn in `rút gợi ý` **5/5**, hàng `may_goi_y` ô thành trống **0**; hàng người `HD-K7B` | Mã cũ: ĐỎ `assert 0 == 5` *(đếm "rút gợi ý")*; `M1`/`M2` đỏ |
| **AC-3** | `::test_AC3_hop_bo_ghep_HAI_lop__…` *(thân `KQ-007` `[cdt1, hd, hd, cdt1]`)* ⇒ `2 ô` · `4 bút toán` · `cdt1`, `hd` mỗi chuỗi **1** lần, `cdt1` trước `hd`. `::…MOT_lop…` *(`[cdt1, hd]`)* ⇒ `2 ô`, ⛔ "bút toán". Thân **thật** *(`_pg::test_AC3_…`)*: `but_toan_dao` = `[cdt1, hd, cdt1, hd, cdt1]` *(5)* ⇒ `2 ô` · `5 bút toán` | Mã cũ: ĐỎ `'Đã đảo 4 bút toán …: cdt1, hd, hd, cdt1'`. `M3` *(trả về `dao.map(...)`)* ⇒ đỏ 2 bài |
| **AC-4** | `::test_AC4_bo_gan_bo_qua_CO_muc__…` — `unmatch` gọi **1** lần, **1** hộp `Đã bỏ ghép`, nút `["Đã hiểu"]`, chứa `hd` **và** `HD-K7B`. `::…bo_qua_RONG__KHONG_hop_nao` ⇒ `[]` *(đếm cả `HT.mo` lẫn `HT.hoi`)*. `::…cua_unmatch_LOI…` ⇒ lỗi ném lên, ⛔ hộp. Thân **thật** dòng B *(`_pg::test_AC4_…`)*: `bo_qua` = `[(hd, HD-K7B)]` ⇒ 1 hộp | Mã cũ: ĐỎ `assert 0 == 1`. `M4` *(bỏ đọc thân)* ⇒ đỏ 2 bài; `M5` *(mở hộp cả khi rỗng)* ⇒ đỏ `…RONG__KHONG_hop_nao` |
| **AC-5** | bảng cổng trên: `pytest` **0** đỏ · lint **9/0** · `soi_bang_tuyen` 40/40 · `kiem_thuyet_minh` 31/31 · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh *(trong `2095`)* | — |
| **AC-6** | nền sau `T0` **0** lệch ⟷ đỏ mới **20** loại (c) *(bảng cổng)*; ⛔ chạy `--ghi` lần hai | — |

⭐ **Đột biến** *(`scratchpad/dot_bien_wo008.py`: mỗi mẫu khớp **đúng 1** lần, chạy 11 bài, trả nguyên + kiểm `sha256`)* ⇒ **5/5 bị bắt**; `tra nguyen: byte khop 5/5`; `git status` sau đó chỉ còn các tệp đã sửa có chủ đích.

## Kho thật
- **`KHONG_CHAM`** *(ghi)*. Chỉ `SELECT` qua `noi_chi_doc` để đo cho `HOI-016`: `fls_journal` `may_goi_y` có giá trị **4.424** · `sua_tay` có giá trị **2** · `sua_tay` rỗng **2** · `fls_sua_tay` **0** · 7 cột `*_thyt` khác `NULL` **0** / **8.387** dòng `fls_itl`. ⇒ Trên sổ thật hôm nay: **4.424** dòng nhật ký đổi nhãn sang *"gợi ý: X · máy gợi ý · không đổi Final"*; *"rút gợi ý"* **0** dòng; hộp `(c)` bật **0** lần.

## Cách chạy để xem
- Đã tự xem đường phục vụ: `PG_DSN=…/fls_test python tools/chay_cua.py --cho-web --cong 8099` *(chỉ đọc, kho TEST)* ⇒ `man_f02.js` · `man_f01.js` · `man_f01_ghep.js` **200**; tệp phục vụ mang `rút gợi ý` *(2 chỗ)* và `F01._bao_bo_ghep(than)` *(1)*; máy đã tắt *(`curl` sau đó ⇒ `000`)*. ⛔ chạm `8088`.
- Muốn thấy hộp `(c)` trên màn thật cần `--cho-ghi` trên kho TEST + dựng dòng B như bài `_pg` — Dev **⛔ làm** *(⛔ chụp màn)*.

## Dev tự thấy còn yếu
1. ⭐⭐ **`HOI-016` ⓑ là thật và rộng hơn `F-1`**: `fls_journal.value_source` của cú gõ NGƯỜI là nguồn **trước** khi gõ. Hệ quả đo được trên kho TEST: dòng người gõ đầu tiên in nguồn `UNMAPPED` *(⛔ "người sửa")*. Hệ quả **chưa dựng bài**: ô có `*_thyt` ≠ NULL, người gõ đè ⇒ màn in *"gợi ý: X · máy gợi ý · không đổi Final"* cho giá trị **người**, **là Final** — đúng chiều ngược của `F-1`. Sổ thật hôm nay **0** ô như vậy. Test nên dựng ca này *(`UPDATE fls_itl SET hd_thyt` trên kho TEST rồi `/adjust`)* để có số.
2. **Chữ khác spec một chỗ:** spec viết *"máy gợi ý · ⛔ đổi Final"*; `man_f02.js` nằm trong `test_luat_ky_hieu_man_hinh.py` *(⛔ cấm `⛔` trong văn bản)* ⇒ mã in **"không đổi Final"** theo `WO-008` Rủi ro 1. Bài thử khai hằng `NHAN_MAY` một chỗ.
3. **Khối `bo_qua` đổi một chút** *(in `hd = HD-K7B`)* trong khi Phạm vi (b) nói "giữ như nay" — làm để thoả `AC-4` nguyên văn; `HOI-016` ⓐ. Nếu `fls-ba` chọn phương án 2 thì gỡ một biểu thức.
4. **Câu đảo nói "rút gợi ý máy"** cả khi `but_toan_dao` chứa bản đảo nhánh 8 *(`sua_tay` cũ)* — spec v4.8 khai câu này, nhánh 8 sổ thật 0 + tập đóng. Ca ấy câu hơi sai danh *(đó là bút toán `sua_tay` kiểu cũ)*.
5. **Thứ tự hộp trên màn ghép:** hộp mở **sau** `mo_lenh` *(vẽ lại lệnh)* và qua `setTimeout(60)` của `_bao_bo_ghep`. Nếu `mo_lenh` ném *(cửa ứng viên lỗi)* thì hộp `bo_qua` **⛔ mở** dù bỏ gán đã xong. Chưa dựng bài cho ca này; đổi thứ tự = hộp nằm trên một màn chưa vẽ lại.
6. **`AC-4` chỉ đo ca 1 lệnh — 1 dòng tiền.** Ca chùm *(`can_hoi`)* đi cùng đường *(hộp hỏi trước → `unmatch` → báo sau)* nhưng ⛔ có bài riêng; nếu `bo_qua` ⛔ rỗng thì người thấy **hai** hộp liền nhau *(hỏi rồi báo)* — đúng spec *(một hỏi trước cho chùm, một báo sau)*, chưa ai nhìn bằng mắt.
7. Bài DOM đọc bảng ⑦ bằng **cắt chuỗi từ "⑦ Nhật ký"** trong `textContent` của panel *(DOM giả ⛔ phân tích HTML)* — nếu sau này có khối nào nằm **sau** ⑦ mà cũng có `<tbody>`, `_Bang` sẽ gom cả hàng của nó. Hôm nay ⑦ là khối cuối.
