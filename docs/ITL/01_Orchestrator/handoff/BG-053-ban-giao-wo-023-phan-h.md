# BG-053 — bàn giao `WO-023` **phần `(h)`** *(vòng 1)*: lỗi một cú bấm `F01G` nói với người, ⛔ rơi ra console

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — **chỉ phần `(h)`** *(`AC-10` · `AC-11` · `AC-12` · `AC-14`)*. Spec `BA-06` **v4.21** `§4.5 ⓦ` ④ ⑤ ⓐ ⓑ · **v4.22** `ⓦ` ④ hàng lỗi *(`(h)` ⓔ — `KQ-050 F-2`)* · `TL-049` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `5f7dd5f` *(mã + bài)* · `6e39187` *(tài liệu Dev)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Nền** | `BG-052` *(phần `(i)`, `bc5e0bc`)* — phần này dựng **trên** nó *(`_thay_uv` · `_uv_chon`)* |
| **Phần còn lại của `WO-023`** | `(a)(b)` → `(c)(d)` → `(f)(g)` → `(e)(j)`. `WO-023` **giữ `DANG_LAM`**. `(h)` ⓓ *(`GAP-SCR-35` `F04`)* **⛔ gom** *(tuỳ — xem mục yếu 5)* |
| **Câu hỏi mở** | ⛔ không có |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f01_ghep.js` | ⓐ `gan` *(`:747`)* ⛔ bao giờ ném: `try` quanh **đúng** `FLS.ghi('/queue/<itl>/match')`; lỗi ⇒ `ST.loi_gan = {ma, cau, lam_gi, chi_tiet}` ⇒ `ve_dong_gan` *(`:716`, khuôn ca ⑤ `ve_dong_bo_gan`)* in `Gán chưa xảy ra — Cửa lỗi: <cau>` ＋ `lam_gi` ＋ `chi_tiet`; `ST.dang_gan` khoá nút *(`ve_thanh`: `!uv \|\| ST.dang_gan`)* và chặn `Enter`; `loi_gan` mất khi mở lệnh **khác**. Ghi xong ⇒ `lenh_ke_tiep` ở **ngoài** `try` *(qua `_nguoi_mo`)* — lượt đọc lệnh kế lỗi ⛔ được nói *"Gán chưa xảy ra"*. ⓑ `_nguoi_mo(p)` *(`:783`)*: nơi gọi `mo_lenh` từ phím *(`:1296` `ArrowRight`/`Enter` ở bảng · `:1413` `doi_lenh` `j`/`k`/`↓`/`↑`)*, chuột *(`:1570` hàng rail · `:1614` hàng bảng)*, ô tìm *(`:1398` xoá chữ)*, gán xong *(`:773`)* — lỗi lượt mới nhất mà màn chưa in ⇒ in *(`_loi_uv`)*; `mo_lenh` **vẫn ném** *(`bo_gan` `_sau_bo_gan` đọc)*. ⓒ `thu_lai_uv` *(`:794`)* + nút `Thử lại` `b tiny` ngay dưới `⛔ Cửa lỗi:` *(`:1796`)*: ô tìm rỗng ⇒ `mo_lenh(ST.mo)`; có chữ ⇒ `_luot_chu` *(tra lại chữ ấy, khung `Đang hỏi sổ…` trong lúc chờ)*. ⓔ `_tai_toan_so` lỗi lượt **mới nhất** ⇒ `_loi_uv(e)` *(hạ `dang_tai_uv`, đặt câu)* rồi vẫn ném *(cho `mo_lenh` Toàn sổ tự bật)*; trình nghe ô tìm gọi `_luot_chu` *(`:1397`)* — ⛔ `await` trần trong `setTimeout(async …)`. ⓕ `_loi_uv` nay **xoá** danh sách *(`_thay_uv([])`)* — câu lỗi **thay** danh sách trên màn, nên một lựa chọn trên hàng ⛔ còn hiện mà `Gán` vẫn bấm được là đúng lỗ `(i)` |
| `tests/web/khung_node.py` | bẫy `process.on('unhandledRejection')` — **chỉ khi kịch bản bật** `globalThis._BAT_TU_CHOI = []` ⇒ ghi mã/câu lỗi để bài **đếm**; ⛔ bật ⇒ ném tiếp *(hành vi cũ: `node` sập ⇒ bài đỏ)*. ⛔ Bật mặc định: một bẫy toàn cục nuốt lỗi làm **mọi** bài đang dựa vào cú sập xanh lặng |
| `tests/web/ca_wo023.py` | ＋ lệnh thứ hai `L2` *(cùng mã `M1`, lệch +7.000)* — `/queue/lenh-cho` chỉ đọc lần nạp **mới nhất** ⇒ ca một lệnh cho `ST.dong` **1** hàng *(đo 05/10)* ⇒ phím `j`/`k` ⛔ có lệnh kề. Bài `(i)` vẫn xanh |
| `tests/web/test_wo023_h_loi_cu_bam_f01g.py` *(mới)* | 7 bài `AC-10` ×2 · `AC-11` ×2 · `AC-12` ×2 · `AC-14`. Thân `422` **từ cửa thật** kho TEST *(`POST /queue/<M4 USD>/match {pm_line_ids:[L VND]}` ⇒ `422 FLS-DQ-FAILED`, bài tự chứng `fls_pm_link` itl `M4` **0** dòng)*; `fetch` giả trả nguyên văn thân ấy cho **`goi_cua.js` thật** dựng `LoiCua` |
| `docs/ITL/03_Dev/12_P6_WEB_PLAN.md` **v0.20** · `08_CHANGELOG_RELEASE.md` | quy ước thứ mười vế hai *(hàm gắn vào cú bấm ⛔ ném; lỗi là chữ)* |
| `WO-023` *(changelog)* · dashboard §5 · `handoff/README.md` | phiếu |

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `5f7dd5f` — mã ⛔ đổi ở `6e39187`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `2 failed, 2342 passed, 4 xfailed in 410.78s (0:06:50)` — `2 failed` = **đúng** hai `XPASS(strict)` `kq050`: `test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo` *(phần này)* + `test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon` *(`BG-052`)*. `4 xfailed` = 3 `kq021` *(phần `(a)(b)`)* ＋ 1 có từ trước. ⛔ đỏ nào khác |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền** 55 *(`KQ-050` · `BG-052`)*; ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (143 file, 1555 bang, 700 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ này *(cây làm việc gồm tờ, trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` — đo như dòng trên |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — phần `(h)` ⛔ chạm schema |

## Bằng chứng từng AC
⭐ Chiều ĐỎ: cả 7 bài chạy trên **`man_f01_ghep.js` @ `7e67a09`** *(mã khi nhận — `git show 7e67a09:… >` tệp, chạy, chép lại bản mới)* **và** trên `bc5e0bc` *(sau `(i)`, trước `(h)`)* — **7 failed** cả hai, cùng lý do:

| AC | Bằng chứng của Dev |
|---|---|
| **AC-10** *(ⓐ — `422` thật)* | `test_AC10_GAN_cua_tra_422_THAT__dong_loi_trong_khoi_hanh_dong__0_Uncaught`: mở `L` *(chuột)*, gõ `doc(M4)`, bấm hàng, `Gán` ×2 *(ca lệch)* ⇒ **một** `POST`, `422` thật. Mới: `#ghep-goc` chứa `Gán chưa xảy ra — Cửa lỗi: Cổng kiểm chất lượng không đạt nên máy chặn phép ghi này.` ＋ `lam_gi`, `_BAT_TU_CHOI = []`, nút mở lại. ⛔ Đỏ cũ: `⛔ lỗi chưa bắt (Uncaught in promise): ['FLS-DQ-FAILED']` |
| **AC-10** *(ⓐ — cửa treo)* | `test_AC10_GAN_khi_cua_TREO__nut_khoa__bam_them_0_POST`: `[M2]` đúng tiền, cửa ghi **treo**, bấm `Gán` + 2 cú + `Enter` ⇒ **1** `POST`, nút `disabled` trong lúc chờ. ⛔ Đỏ cũ: `⛔ bấm khi cửa đang chờ ⇒ 4 POST` |
| **AC-10** — Chrome **8099** kho TEST *(`--cho-ghi`)* | `node cdp23h.mjs 8099 9223 <L> <doc M4> x` *(scratchpad)*: chuột mở `L`, `Ctrl+A` + `insertText` số CT `M4`, chuột hàng, `Gán` ×2. **Mã khi nhận** *(`worktree` @ `7e67a09`, ca `PL3D85F4-1`)*: `POST /queue/8/match` → **`422`**; khối hành động **0** dòng lỗi, nút còn *"Xác nhận gán 6.487,00 USD (khác tiền tệ — cửa ghi sẽ từ chối) ?"*; console `Runtime.exceptionThrown` **`Uncaught (in promise)`** `goi_cua.js:220` *(`goi`)*. **Mã mới** *(`5f7dd5f`, ca `PL3657A3-1`)*: `POST /queue/12/match` → **`422`**; dòng `Gán chưa xảy ra — Cửa lỗi: Cổng kiểm chất lượng không đạt nên máy chặn phép ghi này.` ＋ `Mở màn “Cổng hôm nay” xem cổng nào đỏ.` ＋ chi tiết `dong so la 'USD' nhung dong lenh la ['VND'] — ⛔ khong cong hai don vi khac nhau`; console **0** lỗi |
| **AC-11** *(ⓑ — phím)* | `test_AC11_phim_J_mo_lenh_KE_cua_LOI__vung_ung_vien_noi__0_Uncaught`: mở `L` bằng chuột, `itl-candidates` lệnh kề **giữ**, phím `j`/`k` qua trình nghe `document` **thật** *(`L` có thể đứng cuối — bài chọn chiều có lệnh kề)*, `_no` `FLS-INTERNAL` ⇒ vùng ứng viên `⛔ Cửa lỗi: Máy gặp lỗi bên trong.`, `_BAT_TU_CHOI = []`. ⛔ Đỏ cũ: `⛔ lỗi chưa bắt: ['FLS-INTERNAL']`. Mẫu số *(`mo_lenh` vẫn ném cho `bo_gan`)*: `test_wo008_v2_nam_ca_bo_gan.py::test_AC12_doc_lai_ung_vien_LOI__hop_bo_qua_VAN_mo__tin_hieu_va_dong_loi_doc` **xanh** *(trong pytest toàn bộ)* |
| **AC-11** *(ⓑ — chuột, mở lại cùng lệnh)* | `test_AC11_bam_CHUOT_lai_CUNG_lenh_cua_LOI__man_noi__0_Uncaught`: bấm lại hàng rail `L` *(danh sách cũ còn khi lượt bay)*, lỗi `FLS-MAT-KET-NOI` ⇒ `⛔ Cửa lỗi: Không nối được tới máy chủ FLS.` + **1** nút `Thử lại`, `Gán` khoá, 0 lỗi chưa bắt. ⛔ Đỏ cũ: `⛔ lỗi chưa bắt: ['FLS-MAT-KET-NOI']` *(danh sách cũ đứng im như thể lượt đã thành)* |
| **AC-12** *(ⓒ — ô tìm rỗng)* | `test_AC12_THU_LAI_o_tim_RONG__mot_luot_itl_candidates__danh_sach_ve`: đổi lệnh, `itl-candidates` lỗi ⇒ **1** nút lớp `b tiny`, anh em **ngay trước** là câu `⛔ Cửa lỗi:`; bấm ⇒ **1** lượt `itl-candidates`; về ⇒ `ST.ung_vien` = thân cửa thật, `loi_uv null`, ⛔ còn câu lỗi. ⛔ Đỏ cũ: `('⛔ ⛔ có nút Thử lại dưới câu lỗi', {'n': 0, …})` |
| **AC-12** *(ⓒ — ô tìm có chữ)* | `test_AC12_THU_LAI_o_tim_CO_CHU__mot_luot_so_q_chu_giu`: gõ `doc(M2)`, `/so` lỗi ⇒ câu lỗi; `Thử lại` ⇒ đúng **`[/queue/lenh/<L>/so?q=<doc M2>]`**, **0** `itl-candidates`, `ST.tim` **giữ**, danh sách `[M2]`. ⛔ Đỏ cũ: ⛔ câu lỗi *(danh sách chữ cũ còn trên màn)*, ⛔ nút. Chiều *"nút gọi `mo_lenh` khi có chữ"* ⇒ ĐỎ ở `uv == 0` |
| **AC-14** *(ⓔ — `KQ-050 F-2`)* | `test_AC14_tim_LOI_khi_lenh_moi_dang_tai__khung_ha__cau_loi__thu_lai`: `mo_lenh(L)` giữ ⇒ khung `Đang hỏi sổ…`; gõ chữ, `/so` lỗi, thả lượt lệnh *(đã bị thay)* ⇒ `dang_tai_uv false`, ⛔ còn khung, `⛔ Cửa lỗi: Máy gặp lỗi bên trong.`, `Thử lại` ⇒ **1** `/so?q=<chữ>`, 0 lỗi chưa bắt. ⛔ Đỏ cũ: `⛔ lỗi chưa bắt: ['FLS-INTERNAL']`. ⭐ `pytest --runxfail "tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo"` ⇒ **passed**; không `--runxfail` ⇒ `XPASS(strict)` |
| AC-6 *(phần `(i)` + `(h)`)* | `pytest` **0** đỏ ngoài **2** `XPASS(strict)` `kq050` *(`F-2` · `F-3`)* — 2 / 5 của `AC-6`; 3 `kq021` thuộc `(a)(b)` · lint 9/0 · 40 tuyến · `kiem_thuyet_minh` 31/31 |
| AC-7 *(phần `(h)`)* | `kiem_so_song` **55 = nền**; ⛔ `dong_bo --ghi`; `khop_owner --kiem` **ĐẠT 17/20** đo sau khi viết tờ *(trước commit tờ)* |
| AC-1…AC-5b · AC-8 · AC-9 · AC-15 | ⏳ **chưa làm** — `BG` sau |

## Kho thật
- `KHONG_CHAM`. Kho TEST: mỗi lượt `pytest` một ca `dung_ca_wo023` *(4 dòng tiền + 2 lệnh)* + một cú `POST` bị từ chối `422` *(⛔ ghi)*; Chrome hai ca *(một mỗi mã)*, mỗi ca một `POST` `422` *(⛔ ghi)*.

## Cách chạy để xem
- Như `BG-052`: kho TEST `--cho-web --cho-ghi --cong 8099` ⇒ tab `②b`; mở lệnh ca, gõ số CT của `M4` *(USD)* vào ô tìm, bấm hàng, `Gán` hai lần ⇒ dòng lỗi dưới nút. `Thử lại`: tắt máy giữa chừng *(hoặc CDP `Fetch.failRequest`)* rồi bấm hàng lệnh khác.

## Dev tự thấy còn yếu
1. **`xac_nhan` giữ sau khi cú ghi bị từ chối** *(Chrome mã mới: nhãn vẫn *"Xác nhận gán … ?"*)* ⇒ **một** cú bấm nữa là gửi lại *(cửa sẽ từ chối lại, cùng lý do)*. Spec `ⓦ` ⑤ ⓐ ⛔ nói gì về `xac_nhan` sau lỗi; ⛔ tự thử lại *(`(c)`)* là **máy** tự gửi — đây là **người** bấm. Tôi để nguyên; `fls-ba` xếp nếu muốn về `Gán`.
2. **`_loi_uv` nay xoá danh sách** *(cả ở `mo_lenh` mở lại cùng lệnh qua chuột — trước `(h)` danh sách cũ ở lại, lỗi ném ra console)*. Đúng `ⓦ` ④ *("lỗi = câu `⛔ Cửa lỗi:`")* và an toàn với `(i)`, nhưng là thay đổi: người đang đọc danh sách cũ, bấm lại hàng lệnh, mạng chớp ⇒ danh sách biến mất, chỉ còn câu lỗi + `Thử lại`. `bo_gan` *(gọi `mo_lenh` trực tiếp)* **giữ** danh sách cũ như trước *(bài `wo008_v2 AC12` xanh)*.
3. **`lam_gi` của `FLS-DQ-FAILED` nói sai việc** cho ca khác tiền tệ: *"Mở màn “Cổng hôm nay” xem cổng nào đỏ."* — cổng ⛔ đỏ; lý do thật nằm ở `chi_tiet` *(`dong so la 'USD' nhung dong lenh la ['VND']`)*. Chữ thuộc `BA-07` §5 / `goi_cua.js::CAU` — ngoài `(h)` *(⛔ đổi câu)*; báo `fls-ba`.
4. `_nguoi_mo` in lỗi **chỉ khi** `ST.loi_uv` còn trống — nếu một lỗi cũ còn đó *(lượt trước lỗi, chưa `Thử lại`)* và lượt mới lỗi khác mã, màn giữ câu **cũ**. `mo_lenh` mở đầu bằng `ST.loi_uv = null` nên ca này chỉ tới được nếu một lượt chữ chen giữa — chưa dựng bài.
5. `(h)` ⓓ *(`GAP-SCR-35` — `F04` `S.chup = null` khi mở ảnh mới)* **⛔ gom**: phiếu ghi *"tuỳ — Dev gom nếu rẻ"*; nó chạm `man_f04.js` + nút `Soát`/`Nhận` *(một cú ghi khác)* và cần bài riêng; tách khỏi `BG` này để `(h)` chỉ một màn.
6. Đính chính `BG-052` mục yếu 4: đã chạy đột biến *(bỏ `if (doi) ST.chon_itl = null`)* ⇒ bài mẫu số `test_AC13_doi_sang_lenh_KHAC_van_bo_chon` **vẫn xanh** — dòng ấy **thừa**: `mo_lenh` đổi lệnh còn gọi `_thay_uv([])` ⇒ `null` ở đó. Bài mẫu số **⛔ cắn** đột biến này; nó chỉ cắn bản *"giữ itl_id qua mọi lượt"* nếu bản ấy bỏ **cả** `_thay_uv([])`.
7. Bẫy `_BAT_TU_CHOI` của `khung_node.py` chỉ thấy lời hứa bị từ chối **⛔ ai bắt** — một lỗi **đồng bộ** ném trong trình nghe `click` của DOM giả *(`_bam` gọi thẳng)* sẽ làm sập bài thay vì được đếm. Hôm nay mọi hàm của `F01G` gắn vào nút đều `async`.
