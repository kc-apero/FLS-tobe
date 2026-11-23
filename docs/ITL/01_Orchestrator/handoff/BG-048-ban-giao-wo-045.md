# BG-048 — bàn giao `WO-045` *(vòng 1)*: lượt tải **mới nhất** thắng ở mọi màn còn lại · `Xem thêm` / `Tìm tiền` `F01L` ⛔ khoá ở chỉ đọc · nút `Thử lại` `②b` · `title` thanh lằn ⛔ số cứng

| | |
|---|---|
| **Thuộc** | `WO-045` *(spec `BA-06` **v4.20** `§4.5 ⓥ` ⑤ · `ⓦ` ①②③)* |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `2b804e3` *(đã đẩy — mã + bài + tài liệu Dev)*; tờ này ở commit kế tiếp |
| **Nền khi nhận** *(đo lại ở cổng vào)* | git `14a4b72` = `origin` · mã `fls/**` = `db0adae` · `pytest` **2302 passed, 4 xfailed** *(375 s)* · `kiem_so_song` **55** — khớp `WO` |
| **Câu hỏi mở** | [`HOI-049`](HOI-049-chu-so-trong-title-va-lop-nut-thu-lai.md) `KHONG_CHAN` — ⓐ `AC-13` *"0 chữ số"* ⟷ chuỗi spec mang `QĐ-ITL-122` · ⓑ `b tiny` ⟷ "cùng dáng `TT.chay`" *(lớp `b`)*; làm theo phương án ⭐ của từng câu |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f01_ghep.js` | ① `mo_lenh` + ô tìm *(`tai_toan_so` / `_tai_toan_so`)* chung **một** bộ đếm `_luot_uv` *(trục lệnh + trục chữ cùng ghi `ST.ung_vien`)*; lượt bị thay ⛔ ghi, ⛔ vẽ, lỗi ⛔ hiện *(lỗi lượt cũ ⛔ ném nữa)*. Đổi lệnh ⇒ danh sách cũ **xoá ngay** + `ST.dang_tai_uv` ⇒ khung `Đang hỏi sổ…` *(chữ + lớp `banner info` của danh sách lệnh)* trong vùng ứng viên, vẽ ngay. Lượt mới nhất lỗi khi danh sách rỗng ⇒ `⛔ Cửa lỗi: <câu>` *(khuôn `②b`)*; lỗi vẫn **ném** cho người gọi như nay *(`bo_gan` đọc nó — bài `test_wo008_v2…AC12` giữ xanh)*. `doi_chip` thay lượt ứng viên đang bay. `(e)` `ST.loi` ⇒ nút `Thử lại` `b tiny` ⇒ `doi_chip(ST.chip)`. |
| `fls/web/tep/man_f01_lenh.js` | ② ⓒ `_nut_doc` *(⛔ `_chan_ghi`)* cho `Xem thêm` + nút mở hộp mỗi hàng; nút `Ghép` trong hộp: `_chan_ghi` **sau** `HT.mo` + gỡ `onclick`. ⓐⓑ `_luot_luoi` — `ve()` + `ve_luoi` tăng; `TT.chay(…, {con_hieu_luc})`; `Xem thêm` khoá nút trong lúc chờ + bỏ kết quả nếu lưới đã đổi. |
| `fls/web/tep/man_f01.js` | ③ `_luot_luoi` cho `ve_luoi` / `_xem_them` *(cùng khuôn)*; nút `Xem thêm` khoá trong lúc chờ. Bảng lưới dựng bằng **cây thẻ** *(cùng thẻ + lớp như chuỗi `innerHTML` cũ — ⛔ `TP.bang`, nó thêm lớp `g`)* vì DOM giả trả `tbody null` ⇒ trước đây ⛔ bài DOM nào vẽ được lưới này. ⑤ `title` `Theo LỆNH CHI` = chuỗi `ⓦ` ③ ⓐ; chú thích bia `7.682 · 1.345 · 69` **giữ**. |
| `fls/web/tep/man_f04.js` | ④ `_luot_chup` *(mở ảnh mới cũng thay lượt thứ tự ngày đang bay)* · `_luot_thu_tu`; cả hai qua `con_hieu_luc`. |
| `fls/web/tep/trang_thai.js` | `TT.chay` nhận tuỳ chọn `con_hieu_luc` — lượt bị thay ⛔ vẽ gì cả *(⛔ `_sach(o)`)*: ô **dùng chung** giữa hai lượt *(`F04` `#nap-xem`)* bị lượt cũ xoá rồi vẽ đè. Màn cũ ⛔ truyền ⇒ y nguyên. |
| `tests/web/khung_giu.py` *(mới)* | Cửa giả **giữ** nuôi bằng **thân cửa thật** *(`_TRA[đường]` = phong bì HTTP nguyên văn)*; khoá đường dựng đúng cách `goi_cua.js`; `_bam` *(nút `disabled` ⛔ nhận cú bấm)*. |
| `tests/web/ca_wo045.py` *(mới)* | Ca kho TEST: `A` USD ↔ `B` VND *(hai tập ứng viên **rời** — bài kiểm rời trước khi tin)* · `N` rổ `nguoi` · `T` tự chứng · 55 lệnh rổ `khong` *(hai trang `F01L`)* · 55 dòng tiền VND *(hai trang `F01`)*. |
| `tests/web/test_wo045_luot_moi_nhat_cua_that.py` *(mới)* | 24 bài `AC-1`…`AC-9` *(pg — thân cửa thật kho TEST)*. |
| `tests/web/test_wo045_thanh_lan_khong_so_cung.py` *(mới)* | 2 bài `AC-13` *(oracle đọc `06_SCREEN_SPEC.md`)*. |
| `tests/web/dom_gia.js` | ＋ `insertAdjacentHTML` *(`F01` gọi ở chỉ đọc + chân lưới hết trang; trước đó ⛔ bài nào vẽ được lằn tiền ở chỉ đọc)* — ⛔ phân tích HTML. |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` · `12_P6_WEB_PLAN.md` *(v0.18 — quy ước thứ chín vế hai)* | tài liệu Dev |
| `handoff/HOI-049-…md` · `WO-045` *(trạng thái + changelog)* · dashboard §5 · `handoff/README.md` | phiếu |

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `2328 passed, 4 xfailed in 384.67s (0:06:24)` *(nền `2302 passed, 4 xfailed`; ＋ 26 bài `wo045`; 4 `xfail` = 3 `kq021` *(`WO-023`)* ＋ `kq046::test_F1_*` *(`WO-047`)* — vẫn `xfail`, ⛔ `XPASS`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **55 = 55 nền** *(đo đầu phiếu, cùng lệnh)* **＋ 0 loại (c) mới**: so từng dòng sau khi bỏ chữ số ⇒ **0** khác; khác chỉ ở **giá trị máy đo** của 14 dòng nền *(số bài `2329 → 2332` · dòng thử `26.415 → 26.619` · web `9.407 → 9.611` / `605 → 608` · tệp `137 → 138` · `DEV-12` `0.17 → 0.18`)* — số của chính phiếu này *(bài + tệp mới)*. ⛔ `dong_bo --ghi`. |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (138 file, 1517 bang, 693 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo @ `2b804e3`; chạy lại sau tờ này: `139 file, 1522 bang` — ＋ chính `BG-048`, vẫn `DAT`)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` *(⛔ tuyến mới)* |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — phiếu ⛔ chạm schema / migration *(`git diff --stat` ⛔ tệp `fls/db/**`)* |

## Bằng chứng AC
**Chiều ĐỎ** của mọi bài: chạy trên **worktree mã khi nhận** *(`git worktree add … 14a4b72`, chỉ chép thêm 4 tệp bài + `dom_gia.js`)* ⇒ **25 failed, 1 passed** *(26 bài)* *(1 xanh = `test_AC6_CO_GHI_tim_tien_va_GHEP_nhu_nay` — bài hồi quy chiều `cho_ghi = true`, đúng phải xanh)*. Năm bài `F01` đỏ trên mã khi nhận vì `tbody null` *(giới hạn DOM giả — ⛔ lý do đúng)* ⇒ chạy lại trên **mã khi nhận ＋ chỉ phép dựng bảng bằng cây thẻ**: `AC-7` ×3 đỏ **đúng lý do**, `AC-6 F01` ×2 *(hồi quy)* xanh, `AC-7[truoc]` xanh *(thứ tự ấy lượt cuối về cuối — mã cũ cũng đúng; giữ làm gác)*.

| AC | Bằng chứng | Đỏ trên mã khi nhận *(nguyên văn rút gọn)* |
|---|---|---|
| AC-1 | `test_AC1_doi_lenh_A_sang_B_luot_A_ve_SAU…` · `…luot_A_ve_TRUOC_khi_B_dang_tai…` · `…dang_tai_lenh_moi_ST_ung_vien_KHONG_con_cua_lenh_truoc` *(phím `j` thật qua trình nghe `document`)* · `…loi_luot_A_CU_KHONG_hien_loi_luot_B_MOI_thi_hien` | `⛔ ứng viên của lệnh A dưới lệnh B: [1]` · `ST.ung_vien mang ứng viên A {'uv': [1], 'dom': 1}` · `⛔ ST.ung_vien còn ứng viên A: [1]` · lượt cũ lỗi ⇒ `['ném: Máy gặp lỗi bên trong.', None]` |
| AC-2 ⭐ | `test_AC2_GAN_sau_khi_doi_lenh_chi_gui_itl_id_cua_B` *(bấm hàng ứng viên đầu + nút `Gán` hai lần — xác nhận lệch tiền)* ⇒ **một** `FLS.ghi('/queue/<X>/match', {pm_line_ids: [B]})`, `X` ∈ ứng viên `B`, ∉ chỉ-`A` · `test_AC2_GAN_luc_lenh_moi_DANG_TAI…` *(⛔ cần lượt muộn — chỉ `j` rồi bấm)* | `⛔ GÁN itl_id 1 của lệnh A kèm lệnh B` · `[['/queue/1/match', {'pm_line_ids': ['PB…-1']}]]` |
| AC-3 | `test_AC3_o_tim_hai_chu_…` — gõ `q1`, chờ `TRE_TIM`+80 ms, gõ `q2`, chờ ⇒ **2** lượt `/so?q=` cùng bay *(kiểm)*; `q2` về trước | `assert [1] == [2]` *(danh sách của chữ cũ)* |
| AC-4 | `test_AC4_doi_ro_…[sau]` · `[truoc]` *(liên kết `Xem <c> dòng` + nút `Bắt đầu tra`)* · `test_AC4_QUAY_LAI_…` | `lưới trộn rổ: ['nguoi', 'may', 'may']` · `['may', 'may', 'nguoi']` · `ma: ['PA…', 'PB…']` sau `Quay lại` |
| AC-5 | `test_AC5_XEM_THEM_bam_hai_lan_…` *(rổ `khong` 55 lệnh, trang kế do cửa cấp)* | `mở lượt thứ hai: [… cursor=VND%3A53, … cursor=VND%3A53]` |
| AC-6 | `test_AC6_CHI_DOC_xem_them_CHAY_den_het` · `…TIM_TIEN_mo_hop_xem_ung_vien_GHEP_khoa_cau_405` *(`Ghép` `disabled` + `title` = câu `405` nguyên văn; `Thôi` bấm được)* · `test_AC6_CO_GHI_…` · `test_AC6_F01_nut_GHI_khoa_dung_che_do[chi_doc]` / `[co_ghi]` *(`Ghép N dòng tự chứng` + `Lý do`/`Hoãn`/`Ghép`/`Xong` — khoá + `405` ở chỉ đọc, mở ở ghi)* | `{'disabled': True, 'title': '⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC…'}` · nút hàng `'disabled': True` ⇒ hộp ⛔ mở |
| AC-7 | `test_AC7_doi_TIEN_TE_…[sau]`/`[truoc]` *(bấm `Xem` thẻ USD)* · `…doi_MUC_PHU_…` *(nút `50%`)* · `test_AC7_XEM_THEM_F01_hai_lan_…` | `⛔ lưới mang hàng VND: 50` · `den_pct=50` mà `ST.dong` = 50 hàng `tất cả` · `mở lượt thứ hai` *(2 `GET` cùng con trỏ)* |
| AC-8 | `test_AC8_mo_hai_anh_chup_…` *(nút `Xem trước` thật của `#nap-doc`; bốn ô + `S.chup` + `S.thu_tu`)* · `test_AC8_thu_tu_ngay_luot_CU_…` | `assert 89 == 90` *(ảnh trước thắng)* · `S.thu_tu [59] == [79, 69]` |
| AC-9 | `test_AC9_loi_danh_sach_co_nut_THU_LAI_…[FLS-INTERNAL]` / `[FLS-MAT-KET-NOI]` — một `banner crit` nguyên câu + nút lớp `b tiny`; bấm **hai** lần ⇒ đúng 2 `GET` *(hai cửa của **một** lượt chip `Chưa gán`)*; danh sách = Σ hàng thân cửa, `ST.loi` `null` | `⛔ ⛔ có nút Thử lại: []` |
| AC-10 ⭐ | **Chrome 154 headless 1440×900, chuột thật** *(`Input.dispatchMouseEvent` trên `getBoundingClientRect`)*, **8097 sổ thật CHỈ ĐỌC** *(⛔ `--cho-ghi`; 8088 ⛔ đụng)*. `/ro` cùng lượt: `{may 184, nguoi 616, khong 801, tu_chung 64, tong 1601, nguoi_khac_tien_te 84}`. **Mã mới**: rổ `may` chưa nhận theo lô *(liên kết `Xem 120 dòng`)* ⇒ `Xem thêm` bấm **2** lần ⇒ **120** hàng = 184 − 64, `pm_line_id` khác nhau 120/120, lưới 120 `tr`; `Bắt đầu tra` *(rổ `nguoi`)* ⇒ **12** lần ⇒ **616** = `/ro`, 616/616 khác; nút `Xem thêm` đầu `{disabled: false, title: ""}`; **0** `POST`; lỗi JS **0** *(1 dòng `Log` mạng `404 favicon.ico` — trình duyệt tự xin)*. | **Đối chứng mã khi nhận** *(worktree, cùng 8097, cùng sổ)*: `may` **50**, `nguoi` **50**, nút đầu `{disabled: true, title: "⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC…"}`, 0 `POST` |
| AC-11 ⭐ | **8099 kho TEST** *(`--cho-ghi`)*, ca `dung_ca_wo045` mới mỗi lượt *(chip `Chưa gán` = `N`, `A`, `B`)*. Chuột bấm hàng `A` *(bảng sổ)*, CDP `Fetch` **giữ** `itl-candidates` của `A` ~2 s, phím `j` ⇒ `B`, thả `A`. **Mã mới**: `ST.mo = B`, ứng viên trên màn = **20** = thân cửa thật của `B` *(cùng thứ tự)*, `A` *(3 itl)* ⛔ một; chuột chọn hàng đầu + `Gán` ×2 ⇒ `POST /queue/150/match {"pm_line_ids":["PB54C686-1"]}` — `150` = dòng khớp mã của **`B`**. | **Đối chứng mã khi nhận**: trước khi thả đúng 20 của `B`; **sau khi thả** ⇒ màn đổi sang **4** ứng viên = thân của **`A`** *(USD)* dưới thẻ `B`; nút đổi thành *"Xác nhận gán 540.150,00 USD (khác tiền tệ — cửa ghi sẽ từ chối) ?"*; `Gán` ⇒ `POST /queue/207/match {"pm_line_ids":["PB57B447-1"]}` — `207` = dòng tiền của **`A`** kèm mã `B` *(cửa ghi trả `422` — khác tiền tệ; một cặp **cùng** tệ trong dung sai sẽ ⛔ bị chặn)* |
| AC-12 | bảng **Cổng** trên | — |
| AC-13 | `test_AC13_title_THEO_LENH_CHI_DUNG_chuoi_spec_v4_20` *(oracle `re` trên `06_SCREEN_SPEC.md`, đòi khớp **đúng 1** lần)* · `test_AC13_title_HAI_nut_KHONG_chu_so_ngoai_ma_quyet_dinh` *(⚠ `HOI-049` câu 1 — bỏ `QĐ-ITL-<n>` rồi đếm; tự chứng chuỗi cũ ⇒ `1345`)* | `'1.345 dòng lệnh …' == 'Lệnh chi đang chờ tiền …'` · `số cứng trong title: {'Theo LỆNH CHI': ['1','3','4','5']}` |

### ① — cú `Gán` sai cặp, tóm một dòng
| Mã | Danh sách sau khi lượt `A` về muộn | Cú `POST /match` của nút `Gán` |
|---|---|---|
| khi nhận *(`db0adae`)* | 4 ứng viên **USD của `A`** dưới thẻ `B` | `/queue/207/match` ← itl của **`A`**, `pm_line_ids: [B]` ⇒ **gửi được** *(cửa từ chối vì khác tệ)* |
| mới | 20 ứng viên = thân cửa của `B` | `/queue/150/match` ← itl khớp mã của **`B`** |

## Kho thật
- **`KHONG_CHAM`**. Sổ thật chỉ qua máy **8097 ⛔ `--cho-ghi`** *(chỉ `GET`, `POST` đếm **0** cả hai lượt)*; 8088 của phiên chính ⛔ đụng. Ghi chỉ ở **kho TEST** *(`fls_test`)*: ca `dung_ca_wo045` *(fixture bài + 3 lượt Chrome)* và hai cú `POST /match` của `AC-11` — **cả hai bị cửa ghi trả `422`** ⇒ **0** mối nối ghi thêm.

## Cách chạy để xem
- Bài: `PYTHONUTF8=1 .venv/Scripts/python.exe -m pytest tests/web/test_wo045_luot_moi_nhat_cua_that.py tests/web/test_wo045_thanh_lan_khong_so_cung.py` *(26 bài, ~10 s)*.
- Sổ thật **chỉ đọc**: `PG_DSN=postgresql://fls:fls@localhost:5433/fls FLS_JWT_SECRET=<≥32 ký tự> python tools/chay_cua.py --cho-web --cong 8097` ⇒ tab `② Hàng chờ · F01` ▸ `Xem 120 dòng` ▸ `Xem thêm` tới hết. Kho TEST: `PG_DSN=…/fls_test … --cho-web --cho-ghi --cong 8099` ⇒ tab `②b Gán lệnh chi`.
- Chrome: `node cdp45.mjs <cổng> <f01l|g> <cổng CDP> [X Y]` — kịch bản đo một lần ở scratchpad phiên *(⛔ vào `tools/`)*: `Fetch` `Request` stage giữ mẫu `*itl-candidates*` của `X`; bấm bằng `Input.dispatchMouseEvent`, phím `j` bằng `Input.dispatchKeyEvent`; thân cửa qua `Network.getResponseBody`; `POST` qua `Network.requestWillBeSent`.
- Đối chứng mã khi nhận: `git worktree add <thư mục> 14a4b72` rồi chạy `chay_cua.py` **từ thư mục ấy**.

## Dev tự thấy còn yếu
1. **Hàm còn ⛔ chống trong 21 của `BG-044` `(d)`**: phiếu vá 8 *(#2 #3 #6 #7 #10 #11 #17 #18)*; còn #4 `gan` · #16 `_ghi_mot_o` · #19 `_soat` · #20 `_nhan` *(bấm GHI hai lần — `WO-023`)* · #8 · #12 *(hộp mở muộn)* · #13 · #21 — **NGOÀI** theo `ⓦ` ①. Thêm một chỗ **ngoài bảng 21** tôi thấy khi làm, ⛔ sửa: `F01` `ve_tom` / `ve_lo` *(thẻ tiền tệ + khối lô)* và `F01L` `ve_viec` / `ve_ro` / `ve_tom` vẽ vào ô **mới** mỗi `ve()` *(lượt cũ vẽ vào ô đã rời cây — vô hại)*, nhưng `_ve_lo` ghi biến mô-đun nào thì tôi ⛔ đọc hết.
2. **Trạng thái tải / lỗi của vùng ứng viên `F01G` là chữ cũ ở chỗ mới**: `Đang hỏi sổ…` *(banner info)* + `⛔ Cửa lỗi: <câu>` *(banner crit)* đặt trong `.cands` — `WO` bảng Màn hình đòi "giữ khung chờ" và "lỗi của lượt mới nhất" nhưng spec ⛔ vẽ khung nào cho **vùng ứng viên**. Tôi ⛔ thêm chữ / lớp mới; vẫn là một lựa chọn trình bày Test/BA nên nhìn bằng mắt *(Chrome AC-11 chỉ đo **số**, ⛔ chụp hình)*.
3. **Lỗi lượt mới nhất của `mo_lenh` vẫn ném** *(như nay — `bo_gan` đọc nó)* ⇒ đổi lệnh bằng `j` gặp cửa lỗi vẫn để lại một `Uncaught (in promise)` trong console *(màn nay **có** nói)*; `gan` lỗi `422` cũng `Uncaught` *(thấy ở cả hai lượt Chrome `AC-11`)* — lớp #4 / `WO-023`.
4. **Ô tìm khi chữ xoá hết** đi `mo_lenh(ST.mo)` *(cùng lệnh ⇒ ⛔ xoá danh sách)* — trong lúc lượt ấy bay, danh sách **toàn sổ** của chữ trước vẫn trên màn *(cùng lệnh, ⛔ sai cặp — nhưng ⛔ phải "Máy đề xuất")*. Hành vi cũ, ⛔ đổi.
5. **`F04` `S.chup` trong lúc ảnh mới đang tải** vẫn là ảnh cũ *(⛔ vẽ, khung tải đang hiện)* — nút `Soát`/`Nhận` đọc `S.chup` nên một cú bấm đúng lúc ấy gửi ảnh **cũ**; `ⓦ` ④ chỉ đòi "màn = ảnh bấm cuối" sau khi xong. Cùng họ với `S.bien_ban` của ảnh trước còn sống khi mở ảnh mới *(#19/#20 — NGOÀI)*.
6. **Chrome headless** — như `BG-044` yếu #4: sự kiện chuột tầng trình duyệt thật nhưng ⛔ cửa sổ hiện hình.
7. `AC-7[truoc]` xanh cả trên mã khi nhận *(lượt cuối về cuối)* — giữ làm gác chiều thứ tự, ⛔ tính là bằng chứng đỏ.
8. `HOI-049` hai câu `KHONG_CHAN` — nếu `fls-ba` chọn phương án 2 của câu 1 *(bỏ mã QĐ khỏi `title`)*, bài `AC-13` vế một đọc spec nên tự theo; vế hai bỏ phép trừ mã QĐ.
