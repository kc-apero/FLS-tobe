# BG-052 — bàn giao `WO-023` **phần `(i)`** *(vòng 1)*: lựa chọn ứng viên `F01G` gắn theo `itl_id`, ⛔ theo chỉ số

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — **chỉ phần `(i)`** *(`AC-13`)*. Spec `BA-06` **v4.22** `§4.5 ⓦ` ⑥ · `KQ-050` `F-3` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `bc5e0bc` *(mã + bài)* · `beee117` *(tài liệu Dev)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Nền khi nhận** *(đo lại ở cổng vào)* | git `7e67a09` = `origin` · `BA-06` **v4.22** = phiếu · `BA-07` hiện hành **v3.12** *(⊇ v3.6 phiếu đòi — phần `(i)` ⛔ chạm hợp đồng cửa)* · ⛔ run id |
| **Phần còn lại của `WO-023`** | `(h)` → `(a)(b)` → `(c)(d)` → `(f)(g)` → `(e)(j)` — mỗi phần một `BG` riêng, theo thứ tự điều phối. `WO-023` **giữ `DANG_LAM`** *(⛔ `CHO_TEST` trọn)*; `AC-6` *(5 `XPASS`)* chỉ đủ khi `(a)(b)` + `(h)` ⓔ xong |
| **Câu hỏi mở** | ⛔ không có |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f01_ghep.js` | ⓐ `ST.chon_itl` *(`itl_id` dòng người bấm, `null` = ⛔ chọn — `INV-I16`)* là **danh tính** lựa chọn. ⓑ `ung_vien_chon` thành **phái sinh** *(getter = chỉ số của `chon_itl` trong `ST.ung_vien`, `null` nếu ⛔ có; setter đặt `chon_itl` = `itl_id` của hàng ấy — giữ cho bài cũ tự nạp `ST.ung_vien` rồi đặt chỉ số, kể cả `tests/nghiem_thu/**`)*. ⓒ `_thay_uv(ds)` — chỗ **duy nhất** một lượt ghi `ST.ung_vien`: `itl_id` còn ⇒ giữ, ⛔ còn ⇒ `null`, `xac_nhan = false` **cả hai** ca. ⓓ `_uv_chon()` — **một** phép tra cho `ve_thanh` · `gan` · `Enter`; ⛔ thấy ⇒ `null` ⇒ **0** `POST`. ⓔ `ve_ung_vien` tô theo `itl_id`; bấm hàng đặt / bỏ `chon_itl`. ⓕ Bỏ phép xoá lựa chọn ở **đầu** lượt cùng lệnh *(`mo_lenh`, nay chỉ `if (doi)`)* và đầu lượt chữ *(hẹn giờ ô tìm — `xac_nhan = false` giữ)*; đổi lệnh khác / đổi chip / gán xong vẫn `null` |
| `tests/web/ca_wo023.py` *(mới)* | Ca kho TEST: lệnh `L` VND ＋ 4 dòng tiền tìm được **riêng** bằng số CT và **cùng nhau** bằng chuỗi `h` — `M1` mã của `L` lệch +5.000 *(ngoài dung sai ⇒ `L` ở chip `Chưa gán`; hàng đầu `itl-candidates`)* · `M2` đúng tiền *(bậc `tien` — `Enter` gán được)* · `M3` lệch +500 *(trong dung sai — cửa ghi **nhận**)* · `M4` USD *(⛔ trong `itl-candidates`)*. Ca **nhỏ** — ⛔ làm lệch phân bố `VND` của kho TEST *(`KQ-050 F-4`)* |
| `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py` *(mới)* | 5 bài: `AC-13` ⓐ ⓑ ⓒ ⓓ + mẫu số *"đổi lệnh khác vẫn bỏ chọn"*. Thân cửa **thật** kho TEST *(`_may()` HTTP)*, cửa giả **giữ** *(`khung_giu.py`)*, bấm qua `_bam` *(nút `disabled` ⛔ nhận)*, `Enter` qua trình nghe `document` **thật** *(vỏ có `#man-ghep.on` — ⛔ có thì `Enter` là phím ⛔ ai nghe)* |
| `tests/web/test_b3_fe_bam_thiet_ke.py` | ⚠ **viết lại một bài, giữ lo gốc**: `test_MAY_KHONG_chon_san_ung_vien` đọc mã tìm `ung_vien_chon\s*:\s*null`; tên ấy nay là getter ⇒ ⛔ còn dòng khai để đọc. Phép đo chuyển sang **chỗ khai thật** `chon_itl: null` — lo gốc *("khởi tạo `null`, máy ⛔ chọn sẵn")* **giữ**; bài chạy `test_may_KHONG_chon_san_ung_vien_nao` *(đọc `ung_vien_chon` + `.cand.chon` sau `mo_lenh`)* vẫn xanh, ⛔ sửa. Lý do ghi trong docstring |
| `docs/ITL/03_Dev/12_P6_WEB_PLAN.md` **v0.19** · `08_CHANGELOG_RELEASE.md` | quy ước thứ mười *(lựa chọn theo danh tính hàng, đối chiếu ở cuối lượt)* |
| `WO-023` *(trạng thái `DANG_LAM`)* · dashboard §5 *(hai dòng)* · `handoff/README.md` | phiếu |

⭐ Mọi chỗ ghi `ST.ung_vien` *(`grep -n "ST.ung_vien = \|_thay_uv(" man_f01_ghep.js` @ `bc5e0bc`)*: `:661` *(trong `_thay_uv`)* · `:1047` `doi_chip` *(`ST.ung_vien = []` ＋ `chon_itl = null` — đổi chip, như nay)* · `:1106` `mo_lenh` đổi lệnh / sau lỗi `_thay_uv([])` · `:1118` `mo_lenh` thân `itl-candidates` · `:1168` `_tai_toan_so` thân `/so` *(cả ô tìm lẫn **Toàn sổ tự bật** đi qua đây)*. ⛔ Chỗ nào khác ghi `ST.ung_vien` trong `fls/web/tep/` *(`grep -rn "ung_vien\s*=" fls/web/tep/` — chỉ `man_f01_ghep.js`)*.

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `bc5e0bc` — mã ⛔ đổi ở `beee117`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `1 failed, 2335 passed, 5 xfailed in 400.25s (0:06:40)` — `1 failed` = **đúng** `[XPASS(strict)] KQ-050 F-3` *(`tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon` — đúng mong `AC-13`, `fls-test` gỡ dấu)*. ⛔ đỏ nào khác |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền** `KQ-050` *(55)*; 37 tên nhóm *(bảng tiến độ ×7 · bản vẽ ×13 · master ×7 · roadmap ×4 · kho ×2 · dashboard · nhánh · test · chân trang)* — số trôi theo ảnh nhịp + số bài/dòng, ⛔ loại *(c)* mới do phần này. ⛔ `dong_bo_so_song --ghi`. ⚠ đối chứng tên với nền **chưa chạy được** trên `worktree` mã cũ *(công cụ gọi `.venv` theo đường tương đối — `FileNotFoundError`)* ⇒ chỉ so **số** |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (142 file, 1551 bang, 699 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ này *(cây làm việc gồm tờ `BG-052`, trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` — đo như dòng trên *(gồm tờ `BG-052`)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — phần `(i)` ⛔ chạm schema |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-13** ⓐ *(ô tìm — `itl_id` ⛔ còn)* | `test_AC13a_o_tim_itl_da_chon_KHONG_con__bo_chon__ENTER_va_GAN_khong_POST`: mở `L`, gõ `doc(M3)` ⇒ `[M3]`, gõ `doc(M2)` *(giữ)*, bấm hàng `M3`, thả ⇒ `[M2]`. Mới: `to = []`, `ung_vien_chon = null`, `Gán` `disabled`, `Enter` + 2 cú `Gán` ⇒ **0** `POST`. ⛔ **Đỏ trên `7e67a09`** *(đúng lý do)*: `⛔ MỘT phím Enter đã GHI dòng người ⛔ chọn: [['/queue/2/match', {'pm_line_ids': ['PL387165-1']}]] (đã bấm M3=3, M2=2)` |
| **AC-13** ⓑ *(ô tìm — `itl_id` còn, vị trí khác)* | `test_AC13b_…`: gõ `h` ⇒ bốn dòng, bấm hàng mang `M2` *(vị trí `k > 0`, bài tự chứng)*, gõ `doc(M2)` *(giữ)*, thả ⇒ `[M2]`. Mới: `to = [0]`, `Enter` ⇒ đúng **một** `POST /queue/<M2>/match {pm_line_ids:[L]}` — ⭐ đây cũng là **mẫu số** của ⓐ *(`Enter` qua trình nghe thật **ghi được**)*. ⛔ Đỏ trên `7e67a09`: `('⛔ ⛔ tô hàng mang itl đã chọn', {'uv': [2], 'chon': 1, 'to': [], 'gan_khoa': True, ...})` *(chỉ số `1` ra ngoài danh sách một hàng ⇒ 0 `POST`)*. *"Luôn bỏ chọn"* cũng đỏ ở bài này |
| **AC-13** ⓒ *(ca lệch, `xac_nhan`)* | `test_AC13c_…`: `[M3]`, gõ `h` *(giữ)*, bấm `M3` + `Gán` **một** lần *(nhãn `Xác nhận…`)*, thả ⇒ bốn dòng. Mới: `xac_nhan = false`, nhãn ⛔ còn `Xác nhận`, `to = [j]` *(hàng mang `M3` ở vị trí mới)*, **một** cú bấm ⇒ **0** `POST`. ⛔ Đỏ trên `7e67a09`: `⛔ một cú bấm sau khi danh sách đổi đã GHI: [['/queue/1/match', …]]` *(nhãn "Xác nhận gán <M1>" — một cú là ghi)* |
| **AC-13** ⓓ *(`mo_lenh` mở lại **cùng** lệnh)* | `test_AC13d_…`: `[M4]` *(USD)*, xoá ô tìm ⇒ `mo_lenh(L)` *(giữ — danh sách `[M4]` còn trên màn, bài tự chứng)*, bấm `M4`, thả ⇒ `itl-candidates` *(⛔ có `M4`)*. Mới: `to = []`, `chon = null`, `Gán` khoá, **0** `POST`. ⛔ Đỏ trên `7e67a09`: `⛔ GHI dòng người ⛔ chọn: [['/queue/1/match', …]] (đã bấm M4)` *(gửi `M1`)* |
| **AC-13** — mẫu số dòng cuối bảng `ⓦ` ⑥ | `test_AC13_doi_sang_lenh_KHAC_van_bo_chon` — đổi lệnh ⇒ `null` kể cả khi `itl_id` có lại trong danh sách mới. Xanh **cả** trên mã cũ *(đúng — đó là luật cũ giữ)*; nó đỏ với một bản *"giữ `itl_id` qua mọi lượt"* ngây thơ *(đã thử: bỏ `if (doi) ST.chon_itl = null` ⇒ ⚠ chưa chạy riêng — xem mục yếu 4)* |
| **AC-13** — `kq050::test_F3` | `pytest --runxfail "tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon"` ⇒ **passed**; không `--runxfail` ⇒ `XPASS(strict)` *(dòng `1 failed` của pytest toàn bộ)*. Bài đọc `ST.ung_vien_chon == 0` sau cú bấm và `is None` sau khi danh sách thay — getter phái sinh trả đúng hai giá trị ấy |
| **AC-13** — Chrome **8099** kho TEST *(`--cho-ghi`)* | `node cdp23i.mjs 8099 9223 <L> <doc M3> <doc M2>` *(scratchpad — ⛔ vào `tools/`)*: Chrome `154.0.8037.57` headless, chuột `Input.dispatchMouseEvent` *(tab `②b` · hàng lệnh · ô tìm · hàng `M3`)*, chữ `Input.insertText` sau `Ctrl+A` thật, `Enter` `Input.dispatchKeyEvent`; CDP `Fetch` **giữ** `*/so?q=<doc M2>` ~2 s. **Mã khi nhận** *(`git worktree` @ `7e67a09`, ca `PL3DD048-1`, `M2`=`1259`, `M3`=`1260`)*: bấm `M3` ⇒ `to [0]`; thả ⇒ `uv [1259]`, `to [0]`, gợi ý *"Khớp đúng số tiền — Enter để gán."*; `Enter` ⇒ **`POST /queue/1259/match {"pm_line_ids":["PL3DD048-1"]}` → `200`**; kho TEST `fls_pm_link` `link_id 1263` · `itl_id 1259` — **dòng người ⛔ chọn đã vào sổ chỉ-thêm**. **Mã mới** *(`bc5e0bc`, ca `PL38F197-1`, `M2`=`1269`, `M3`=`1270`)*: bấm `M3` ⇒ `to [0]`; thả ⇒ `uv [1269]`, `to []`, `chon null`, `Gán` `disabled`, *"Chọn một giao dịch bên trên."*; `Enter` ⇒ **0** `POST`; `fls_pm_link` itl `1268…1271` **0** dòng. Console **0** lỗi cả hai lượt |
| **AC-13** — 8097 sổ thật **chỉ đọc** *(⛔ `--cho-ghi`)* | `node cdp23i_doc.mjs 8097 9223`: mở lệnh đầu chip `Chưa gán` *(`PM01698-1`, 50 ứng viên)* bằng chuột, bấm hàng **thứ hai** ⇒ `chon 1`, `to [1]`, `chon_itl 143437`; gõ số CT của chính hàng ấy ⇒ danh sách `[143437]`, `chon 0`, `to [0]`, `chon_itl` **giữ** `143437` *(ca "còn" trên dữ liệu thật)*. **0** `POST`, console **0** lỗi |
| AC-6 *(phần `(i)`)* | `pytest` **0** đỏ ngoài `XPASS(strict)` `kq050::test_F3` *(1 / 5 của `AC-6`; 4 còn lại thuộc `(a)(b)` + `(h)` ⓔ)* · lint 9/0 · 40 tuyến · 31/31 |
| AC-7 *(phần `(i)`)* | `kiem_so_song` **55 = nền 55** *(số; tên ⛔ đối chứng được — xem dòng cổng)*; ⛔ `dong_bo --ghi`; `khop_owner --kiem` **ĐẠT 17/20** đo **sau** khi viết tờ này *(trên cây làm việc gồm tờ, trước commit tờ — tờ chỉ thêm `BG-052` + dòng README/dashboard)* |
| AC-1…AC-5b · AC-8…AC-12 · AC-14 · AC-15 | ⏳ **chưa làm** — các `BG` sau |

## Kho thật
- `KHONG_CHAM`. Kho TEST *(`fls_test`)*: hai ca `dung_ca_wo023` qua Chrome + mỗi lượt `pytest` một ca; **một** mối nối ghi bằng **mã cũ** *(đối chứng — `link_id 1263`, `itl_id 1259`, lệnh `PL3DD048-1`)*. Sổ thật chỉ **đọc** qua 8097 *(`noi_chi_doc`)*.

## Cách chạy để xem
- Kho TEST, có ghi: `PG_DSN=postgresql://fls:fls@localhost:5433/fls_test FLS_JWT_SECRET=<≥32 ký tự> python tools/chay_cua.py --cho-web --cho-ghi --cong 8099` ⇒ tab `②b Gán lệnh chi`; dựng ca: `python -c` ⛔ — dùng `tests/web/ca_wo023.py::dung_ca_wo023` từ một tệp script *(bản phiên: scratchpad `ca23i.py`)*.
- Sổ thật chỉ đọc: `PG_DSN=postgresql://fls:fls@localhost:5433/fls … --cho-web --cong 8097`.
- Đối chứng mã khi nhận: `git worktree add <thư mục> 7e67a09` rồi chạy `chay_cua.py` **từ thư mục ấy** *(`PYTHONUTF8=1`, python của `.venv` repo chính)*.

## Dev tự thấy còn yếu
1. **Bỏ phép xoá ở đầu lượt là một thay đổi hành vi ngoài ca lỗi.** Trước: gõ ô tìm *(hoặc xoá chữ)* ⇒ lựa chọn mất **ngay** khi hẹn giờ nổ; nay giữ tới khi danh sách mới về và chỉ mất nếu `itl_id` ⛔ còn. Spec `ⓦ` ⑥ nói *"lượt mới nhất thay `ST.ung_vien` … còn ⇒ giữ"* — tôi đọc là áp cho **mọi** lựa chọn đang có *(kể cả chọn trước khi gõ)*, ⛔ chỉ lựa chọn bấm giữa lượt. Nếu `fls-ba` muốn *"gõ là bỏ chọn"* ⇒ thêm lại hai dòng; bài ⓑ sẽ phải dựng cú bấm **sau** lúc gõ *(nó đã dựng như vậy)* ⇒ vẫn xanh. Test soi: `test_b3_o_tim_song.py` *(xanh)* có đòi bỏ chọn khi gõ không — tôi đọc là ⛔.
2. **`ung_vien_chon` là accessor trên `ST`** *(getter/setter trong literal)*. Mọi bài đọc/đặt nó vẫn chạy; nhưng một bài **sao** `ST` *(`{...ST}`, `JSON.stringify(ST)`)* sẽ nhận **chỉ số đông cứng** ⛔ setter. `grep` hôm nay: **0** chỗ *(`fls/web/tep` + `tests/web` + `tests/nghiem_thu`)*.
3. **Setter còn sống chỉ để bài cũ đặt chỉ số** *(6 chỗ: `test_b3_man_ghep_chay_duoc.py` ×3 · `test_b3_uiux_vong_hai.py:300` · `test_kq002_than_man_ghep_qua_cua_that.py:58` · …)*. Bài đặt chỉ số **trước** khi nạp `ST.ung_vien` sẽ nhận `null` *(⛔ còn hàng ở chỉ số ấy)* — hôm nay mọi chỗ đều nạp trước.
4. Bài mẫu số `test_AC13_doi_sang_lenh_KHAC_van_bo_chon` **chưa được chứng minh ĐỎ** bằng đột biến riêng *(bỏ `if (doi) ST.chon_itl = null`)* — tôi chỉ suy ra nó sẽ đỏ. Bài dựng *"đổi lệnh"* bằng `ST.mo = null` rồi `mo_lenh(L)` *(cùng `itl-candidates`)* — ⛔ phải hai lệnh thật khác nhau.
5. `ST.dg_mo` *(hàng đang mở rộng diễn giải `đủ ↓`)* **vẫn là chỉ số** ⇒ danh sách bị thay thì hàng mở rộng có thể nhảy sang dòng khác. Chỉ đổi **chữ hiện**, ⛔ chạm ghi; ngoài bảng TRONG của `(i)` ⇒ ⛔ sửa.
6. ⚠ **Phát hiện ngoài phạm vi** *(8097 sổ thật chỉ đọc)*: nút `Gán` của `F01G` **⛔ khoá** ở chế độ chỉ đọc *(`gan: ["Gán", false]`; `nut()` `man_f01_ghep.js:296` ⛔ hỏi `cho_ghi`)* — `BA-06` `ⓦ` ② bảng ghi `Gán` *"khoá + câu `405` như nay"*. Bấm ⇒ cửa trả `405` ⇒ hôm nay `Uncaught` *(chính lỗ `(h)` ⓐ)*. Sau `(h)` ⓐ người sẽ **thấy** dòng lỗi `405`, nhưng nút vẫn bấm được — `fls-ba` xếp: lệch spec ↔ mã hay "như nay" chỉ nói về `F01L`?
7. Chrome chạy **headless** *(`--headless=new`)*, ⛔ cửa sổ hiện — chuột/phím vẫn là sự kiện nhập của trình duyệt *(`Input.*`)*, ⛔ `el.click()` JS.
