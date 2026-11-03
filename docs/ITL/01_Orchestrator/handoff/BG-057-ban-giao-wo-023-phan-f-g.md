# BG-057 — bàn giao `WO-023` **phần `(f)(g)`** *(vòng 1)*: nhật ký ⑦ phân biệt bản ĐẢO với cú XOÁ Ô · hộp `Đảo` nói hậu quả theo LỚP

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — phần `(f)` *(`AC-8`)* · `(g)` *(`AC-9`)*. Spec `BA-06` **v4.12** dòng *"F02 · nhật ký"* ⓐ…ⓔ + dòng *"F02 · hoàn tác"* ⓐ…ⓒ *(⛔ đổi tới v4.22)* · `BA-07` **v3.6** *(§3 `GET /journal` `la_ban_dao` · `GET /ledger/{itl_id}` `but_toan[].nguon`)* · `KQ-025` `F-3` `F-4` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `41b9a20` *(mã + bài)* · `bc1ac11` *(tài liệu Dev + `HOI-058`)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Nền** | `BG-052` … `BG-055` |
| **Phần còn lại của `WO-023`** | `(e)` *(khối `SINH-KHOP` chỉ mang quan hệ)*. `WO-023` **giữ `DANG_LAM`** |
| **Câu hỏi mở** | [`HOI-058`](HOI-058-bai-kq019-nhat-ky-so-that-giu-oracle-v4-8.md) `MAU_THUAN` `KHONG_CHAN` — bài nghiệm thu `kq019::test_nhat_ky_SO_THAT…` giữ oracle v4.8 *(bản đảo người ⇒ ô trống)* ⇒ đỏ **1** dạng sau phần này; `AC-6` *"0 đỏ ngoài 5 `XPASS`"* ⛔ đạt tới khi `fls-test` cập nhật oracle *(phương án ⭐)* · [`HOI-056`](HOI-056-chu-het-gio-cho-cu-gan.md) còn mở |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/doc_bao_cao.py` | `(f)` ⓐ `doc_nhat_ky` ＋ cột `la_ban_dao` = `EXISTS (fls_adjustment a WHERE a.itl_id = j.itl_id AND a.field = j.field AND a.at = j.at AND a.actor = j.actor AND a.reversal_of IS NOT NULL)` *(docstring ghi vì sao khoá bốn cột ⛔ nhập nhằng)*. `(g)` ⓐ câu `but_toan` ＋ `nguon` |
| `fls/api/bang_tuyen.py` | `(f)` ⓑ tuyến `GET …/journal` khai đọc thêm `fls_adjustment` |
| `fls/web/tep/man_f02.js` | `(f)` ⓒ `_nk_thanh` theo bảng ⓐ…ⓔ *(chữ nguyên văn `đảo — giá trị này hết hiệu lực` · `xoá ô`, lớp `muted` có sẵn; `la_ban_dao` thiếu/`null` ⇒ như hôm nay)*; ⓓ chú thích *"Ca nhánh 8 … spec v4.8 chấp nhận"* đính chính theo v4.12 *(câu cũ giữ gạch)*. `(g)` ⓑ nút `Đảo` ở ⑥ mang `data-nguon` = `nguon` của **chính** bút toán; `onclick` truyền nó cho `_dao(adj_id, itl_id, nguon)`; `_hau_qua_dao` dựng tiêu đề + câu hậu quả **nguyên văn** bảng ⓐ…ⓒ *(mã lạ ⇒ in mã; thiếu ⇒ `—`)*; câu đầu *"Đảo không xoá gì cả…"*, ô lý do, nút, khoá khi chờ **giữ**. `_dao` xuất cho bài thử *(như `_lam_moi`)* |
| `tests/repo/test_wo023_f_la_ban_dao_pg.py` *(mới)* | 3 bài hàm thật `ghi_tay` + `doc_nhat_ky` kho TEST — gồm ca **đảo rồi xoá cùng ô** *(bắt phép nối thiếu `at`)* |
| `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py` *(mới)* | 5 bài: cửa HTTP **thật** kho TEST *(`/adjust` · `/reverse` · `/match` · `/unmatch`)* ⇒ thân `/journal` + `/ledger` ⇒ màn `F02` ⑦ / hộp `Đảo` |
| `docs/ITL/03_Dev/12_P6_WEB_PLAN.md` **v0.23** · `08_CHANGELOG_RELEASE.md` | quy ước thứ mười ba |
| `handoff/HOI-058-…md` *(mới)* · `WO-023` *(changelog)* · dashboard §5 · `handoff/README.md` | phiếu |

## ⭐ `(f)` — chứng minh khoá `(itl_id, field, at, actor)` ⛔ nhập nhằng *(phiếu đòi; mong **0**)*
Mọi đường chèn `fls_adjustment` đi qua **một** hàm `ghi_tay._them` *(cổng quét mã của tệp — `INSERT INTO fls_adjustment` ngoài tệp ⇒ đỏ)*; `at` = `now()` = giờ **bắt đầu** giao dịch ⇒ hai dòng cùng giao dịch cùng `at`. Bốn nơi gọi `_them` @ `41b9a20`:

| Nơi gọi | Chèn gì trong **một** giao dịch | Cùng `(itl_id, field, actor)` có cả bản đảo lẫn thường? |
|---|---|---|
| `ghi_but_toan` `:505` *(`/adjust`)* | **1** bút toán thường | ⛔ *(một dòng)* |
| `dao_but_toan` `:547` *(`/reverse`)* | **1** bản đảo | ⛔ |
| `ghi_goi_y` `:638` — gọi từ `ghep_lenh` *(một giao dịch `:835`)* | bút toán thường `hd` + `cdt1` | ⛔ — hai `field` khác nhau, **cả hai** thường |
| `bo_moi_noi` `:1045` *(một giao dịch `:1032`)* | bản đảo **mọi** lớp gợi ý còn hiệu lực | ⛔ — **toàn** bản đảo |

⇒ **0** đường ghi chèn bản đảo **và** bút toán thường cùng khoá ⇒ ⛔ `HOI`. Đo sổ thật chỉ `SELECT` *(`noi_chi_doc(dsn_that())`)*: `fls_journal` **4.428** dòng · ⛔ nối được **0** · nhập nhằng *(cùng khoá có cả `reversal_of IS NULL` lẫn `IS NOT NULL`)* **0** · `la_ban_dao = true` **2** *(`27728` `cdt1` + `hd`, `sua_tay`)* · cú xoá ô người **0** — khớp số `BA-07` v3.6.

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `41b9a20` — mã ⛔ đổi ở `bc1ac11`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `6 failed, 2386 passed, 1 xfailed in 457.72s (0:07:37)` — **5** = `XPASS(strict)` *(3 `kq021` + 2 `kq050`, như `BG-054`)* ＋ **1** = `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong` — `⛔ 1/40 dạng in sai: [(27728, 'cdt1', 'sua_tay', ('đảo — giá trị này hết hiệu lực', 'người sửa'), ('', 'người sửa'))]`: oracle v4.8 ⟷ spec v4.12 ⇒ **`HOI-058`**. ⛔ sửa bài *(`tests/nghiem_thu/**`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền 55**; ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (148 file, 1574 bang, 703 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ *(trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` — đo như dòng trên |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(đột biến: bỏ `fls_adjustment` khỏi khai ⇒ `GET /api/fls/v1/journal: SQL cham ['fls_adjustment'] ma bang ⛔ khong khai` — rc 1)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — ⛔ chạm schema *(⛔ cột mới, ⛔ migration — đúng phiếu)* |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-8** ⓐ ⓑ ⓓ *(màn, cửa thật)* | `test_AC8_man_F02_7_DAO_nguoi__XOA_O__RUT_GOI_Y__theo_LOP`: kho TEST `M3` — `invoice` `INV-X` rồi `/reverse` ⇒ hàng `đảo — giá trị này hết hiệu lực`, **0** hàng `invoice` ô trống; `cdt1` `C-1` rồi `/adjust value=null` ⇒ hàng `xoá ô`; `id_payee` `PAY-A`, `PAY-B`, đảo `PAY-A` ⇒ hàng đảo in `đảo — …` **và** `GET /ledger/<M3>/fields/id_payee` = `PAY-B`; nguồn hai hàng ấy `người sửa` |
| **AC-8** ⓒ *(mẫu số)* | `test_AC8c_ghep_bo_ghep__RUT_GOI_Y_khong_doi`: `M2` `/match` → `/unmatch` ⇒ **≥ 2** hàng `rút gợi ý`, **0** hàng `đảo — …`/`xoá ô` *(xanh cả trên mã cũ — đúng "⛔ đổi")* |
| **AC-8** ⓔ | `test_AC8e_than_GET_journal__MOI_dong_co_la_ban_dao_BOOL` — **mọi** dòng thân `/journal` *(≥ 10, cả `true` lẫn `false`)* có `la_ban_dao` kiểu bool. Repo: `tests/repo/test_wo023_f_la_ban_dao_pg.py` ×3 *(gõ rồi đảo · **đảo rồi xoá cùng ô** · kiểu bool)* |
| **AC-8** chiều ĐỎ | trên `doc_bao_cao.py` + `bang_tuyen.py` + `man_f02.js` @ `7e67a09` ⇒ **7 / 8** bài đỏ *(`KeyError: 'la_ban_dao'` · hàng đảo in ô trống · `KeyError: 'nguon'`)*; bài ⓒ xanh *(mẫu số)*. Đột biến: nối **thiếu `at`** ⇒ **2 failed** *(gồm `DAO_roi_XOA_cung_o`)* ✅ *(dự đoán của phiếu đúng)* · `la_ban_dao` luôn `false` ⇒ **2 failed** · màn đọc `value_after` rỗng thay `la_ban_dao` ⇒ **1 failed** *(`AC8_man_F02_7…` — cú xoá ô in `đảo`)* |
| **AC-8** sổ thật | chỉ `SELECT`, hàm thật `doc_nhat_ky` trên `noi_chi_doc(dsn_that())`: `la_ban_dao = true` **2** / **4.428** *(mong 2 / 4.428 ✅)*. Chrome **8097** sổ thật chỉ đọc *(⛔ 8088 — luật phiên)*, drawer `27728` ⑦ — **mã mới**: 4 hàng, hai hàng đảo in `đảo — giá trị này hết hiệu lực`, **0** ô trống *(mong 2 / 0 ✅)*; **mã khi nhận** *(`worktree` `7e67a09`)*: hai hàng ấy ô thành **rỗng**. 0 `POST` |
| **AC-9** *(cửa)* | `test_AC9_than_GET_ledger__MOI_but_toan_co_nguon__hai_ma`: `GET /ledger/<M2>` `but_toan` **mọi** phần tử có `nguon`, ⊇ `{may_goi_y, sua_tay}` *(mẫu số ≥ 2, hai mã)* |
| **AC-9** *(hộp)* | `test_AC9_hop_DAO_theo_LOP_cua_CHINH_but_toan__may_duoi_nguoi`: `M2` ghép lần hai ⇒ gợi ý máy `cdt1` **dưới**, người gõ `C-NGUOI-G` **trên** cùng ô. HTML ⑥: nút của bút toán máy `data-nguon="may_goi_y"`, của người `sua_tay`. `F02._dao(<máy>, itl, 'may_goi_y')` ⇒ tiêu đề `Rút gợi ý máy #<adj>`, `#dlg-b` chứa `không đổi Final`, **⛔** `lùi về`; `_dao(<người>, itl, 'sua_tay')` ⇒ `Đảo bút toán #<adj>` + `hết hiệu lực` + `lùi về`; `nguon='xyz'` ⇒ `chưa biết` + `xyz`; câu đầu `Đảo <b>không xoá</b> gì cả` có ở cả ba. Đột biến: một câu cho mọi `nguon` ⇒ **1 failed** · `data-nguon` theo **ô** *(luôn `sua_tay`)* ⇒ **1 failed** *(ca máy-dưới-người — đúng dự đoán phiếu)* |
| **AC-9** Chrome **8097** chỉ đọc | `node cdp23fg.mjs 8097 9223 x 27728 25041`: **chuột thật** bấm nút `Đảo` của bút toán `sua_tay` `#163563` *(dòng `27728`)* ⇒ hộp `Đảo bút toán #163563` · *"Giá trị này hết hiệu lực. Nếu nó đang là Final thì Final lùi về…"*; bút toán `may_goi_y` `#152383` *(dòng `25041`)* ⇒ `Rút gợi ý máy #152383` · *"…Rút nó không đổi Final — Final vẫn là giá trị người đã gõ, hay giá trị của sổ gốc."*; bấm `Thôi` — **0** `POST`. **Mã khi nhận**: cả hai hộp `Đảo bút toán #…` · *"Sau khi đảo, giá trị lùi về bút toán trước đó…"* |
| AC-6 | `pytest`: 5 `XPASS(strict)` đúng + **1** đỏ `kq019` *(⇒ `HOI-058`)* — `AC-6` **⛔ ĐẠT trọn** ở commit này · lint 9/0 · 40 tuyến · 31/31 · luật ký hiệu + token xanh |
| AC-7 *(phần này)* | `kiem_so_song` **55 = nền**; ⛔ `dong_bo --ghi`; `khop_owner --kiem` **ĐẠT 17/20** đo sau khi viết tờ *(trước commit tờ)* |
| AC-5 · AC-5b | ⏳ **chưa làm** — `BG` sau *(`(e)`)* |

## Kho thật
- `KHONG_CHAM` *(chỉ `SELECT` qua `noi_chi_doc`; Chrome trên 8097 ⛔ `--cho-ghi`, 0 `POST`)*. Kho TEST: mỗi lượt `pytest` một ca `dung_ca_wo023` + vài `/adjust`/`/reverse`/`/match`/`/unmatch` thật.

## Cách chạy để xem
- Sổ thật chỉ đọc `--cho-web --cong 8097` ⇒ tab `③ Sổ ITL · F02`; console `F02.mo_drawer(27728)` ⇒ ⑦ hai hàng *"đảo — giá trị này hết hiệu lực"*; `F02.mo_drawer(25041)` ⇒ ⑥ bấm `Đảo` ⇒ *"Rút gợi ý máy #…"* *(bấm `Thôi`)*.

## Dev tự thấy còn yếu
1. **`AC-6` ⛔ trọn** vì bài nghiệm thu `kq019` giữ oracle v4.8 *(`HOI-058`)* — đúng **một** dạng, hai dòng sổ thật. Tôi ⛔ sửa bài `tests/nghiem_thu/**`.
2. **`la_ban_dao` dựa trên `at` trùng giây-micro** giữa `fls_journal` và `fls_adjustment` *(cùng `now()` của giao dịch)*. Một đường ghi tương lai chèn hai bảng ở **hai** giao dịch *(hay `clock_timestamp()`)* sẽ làm cờ **sai lặng** — ⛔ có ràng buộc máy nào canh *(phiếu cấm migration `adj_id`)*. Bài repo `DAO_roi_XOA_cung_o` chỉ canh phép nối, ⛔ canh giờ.
3. Ca ⓒ `nguon` **thiếu** in `(—)` — spec ghi *"(<mã>)"* cho mã lạ, ⛔ nói gì cho thiếu; `—` là chữ tôi chọn.
4. `_dao` xuất ra ngoài để bài DOM gọi *(nút dựng bằng `innerHTML`, DOM giả ⛔ bấm được)* — bài kiểm **thuộc tính nút** + **hàm**, còn đoạn nối *"nút → `onclick` → `_dao`"* chỉ có Chrome đo *(8097, ở trên)*.
5. Nút `Đảo` vẫn hiện trên bút toán **đã bị đảo** *(vd `27728` `#163563` — bấm ⇒ cửa trả lỗi "đã đảo")* — có từ trước, ngoài phạm vi *(`(g)` ⛔ đổi luật ai được đảo dòng nào)*.
