# BG-054 — bàn giao `WO-023` **phần `(a)(b)`** *(vòng 1)*: hộp `HT` là MODAL với bàn phím · hộp đang chờ cửa ⛔ đóng giữa chừng

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — **chỉ phần `(a)` + `(b)`** *(`AC-1` · `AC-2` · `AC-6` đủ **5** `XPASS`)*. Spec `BA-06` **v4.11** `ⓕ1` · `ⓕ2` *(⛔ đổi tới v4.22)* · `KQ-021` `F-1` · `F-2` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `f52dafe` *(mã + bài)* · `954739a` *(tài liệu Dev)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Nền** | `BG-052` `(i)` · `BG-053` `(h)` |
| **Phần còn lại của `WO-023`** | `(c)(d)` → `(f)(g)` → `(e)(j)`. `WO-023` **giữ `DANG_LAM`** |
| **Câu hỏi mở** | ⛔ không có |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/hop_thoai.js` | ⓐ Chú thích đầu tệp: luật ⓒ **đọc lại** theo câu `ⓕ2` *("`Esc` / bấm ngoài đóng hộp khi **chưa** có lượt ghi nào đang bay — và lúc ấy đóng là ⛔ làm gì")*, câu cũ giữ làm bia; thêm luật ⓓ *(modal với bàn phím)*. ⓑ `_nghe(s)` — trình nghe `click` nền + `keydown` gắn ở lần `HT.mo` **đầu tiên**, **kể cả** khi `#scrim` đã có *(bản trước chỉ khi `_khung` tự dựng `#scrim`)*. ⓒ `keydown` nghe ở pha **capture** *(`addEventListener(…, true)`)*: hộp mở ⇒ đánh dấu `e._hop_thoai = true`; `Esc` ⇒ `dong()`. ⓓ `nuot_phim(e)` *(xuất mới — hàm **hỏi**, chỉ-đọc)* = `!!dang_mo \|\| !!e._hop_thoai`. ⓔ `dong()` *(công khai: `Esc` · nền · nút ⛔ hàm · nơi gọi ngoài)* **⛔ đóng** khi một lượt ghi của **chính** hộp đang hiện còn bay *(`_cho === _lan` — mã lượt, ⛔ cờ trần)*; đóng sau khi hàm nút xong đi đường nội `_dong()`. ⓕ Hàm nút trả `Promise` ⇒ thêm `div.note` `Đang ghi vào sổ — chờ máy trả lời.` vào `#dlg-b`, gỡ khi xong; hàm đồng bộ ⇒ ⛔ dòng. Xuất thêm `CAU_CHO`. **Chữ ký `HT.mo` ⛔ đổi; ⛔ hàm dựng hộp mới** |
| `fls/web/tep/man_f01_ghep.js` | trình nghe `document` `_noi_ban_phim` *(`:1336` — sau `#man-ghep.on`)* + trình nghe `keydown` của tay kéo rail `ve_keo` hỏi `HT.nuot_phim(e)` rồi thôi *(có gác `typeof HT` — bài nạp màn ⛔ kèm `hop_thoai.js` chạy như cũ)* |
| `fls/web/tep/man_f02.js` | trình nghe `keydown` của lưới *(`_noi_ban_phim`, `:718`)* hỏi `HT.nuot_phim(e)` đầu tiên |
| `tests/web/test_wo023_ab_hop_modal_va_hop_cho_cua.py` *(mới)* | 27 bài *(tham số hoá)* — `hop_thoai.js` **thật**, ⛔ chép trình nghe nào; mỗi bài phím chạy **hai** thứ tự đăng ký `man_truoc` / `hop_truoc` |
| `docs/ITL/03_Dev/12_P6_WEB_PLAN.md` **v0.21** · `08_CHANGELOG_RELEASE.md` | quy ước thứ mười một |
| `WO-023` *(changelog)* · dashboard §5 · `handoff/README.md` | phiếu |

⭐ Mọi trình nghe phím trong `fls/web/tep/` *(`grep -rn "addEventListener('keydown'" fls/web/tep/` @ `f52dafe`)*: `hop_thoai.js` *(capture — của hộp)* · `man_f01_ghep.js` `_noi_ban_phim` · `man_f01_ghep.js` `ve_keo` *(trên phần tử)* · `man_f02.js` `_noi_ban_phim` — **3 / 3** trình nghe của màn đã hỏi `HT.nuot_phim`. ⛔ Màn nào khác nghe phím.

## ⚠ Cho `fls-test` — đã đổi trình nghe thế nào *(Rủi ro 1 của `WO-023`)*
- Bài `kq021` `F-1`/`F-2` **chép** trình nghe `Esc` *(`NGHE_ESC_HOP`, pha nổi, đăng ký **sau** `F01G.mo_man`)* vì mã khi nhận ⛔ gắn trình nghe khi `#scrim` có sẵn. Mã mới: `HT` **tự** gắn trình nghe `keydown` *(capture)* + `click` nền ở lần `HT.mo` đầu. **Bản chép vẫn chạy được** *(3 bài `XPASS(strict)` với bản chép còn nguyên — cả hai cùng gọi `dong()`, gọi hai lần vô hại)*; gỡ bản chép đi thì trình nghe của `HT` tự lo.
- DOM giả `dom_gia.js::ban` **⛔ có pha capture** *(gọi trình nghe theo thứ tự đăng ký, cờ `true` bị bỏ qua)* ⇒ trong bài, trình nghe của `HT` chạy theo **thứ tự đăng ký**; phép chặn đúng ở cả hai thứ tự là nhờ **dấu** `_hop_thoai` + `HT.nuot_phim` ở trình nghe màn. Trên Chrome thật capture chạy trước *(đo dưới)*.
- Bản chép gọi `HT.dong()` khi `#scrim.on` — `dong()` nay **⛔ đóng** lúc một lượt ghi đang bay *(chính điều `F-2` đòi)*.

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `f52dafe` — mã ⛔ đổi ở `954739a`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `5 failed, 2369 passed, 1 xfailed in 420.40s (0:07:00)` — `5 failed` = **đúng 5** `XPASS(strict)`: `tests/nghiem_thu/test_kq021_bo_gan_vong2.py::test_F1_ESC_tren_hop_hoi__chi_DONG_HOP__lenh_VAN_MO` · `::test_F1_phim_J_khi_hop_MO__KHONG_doi_lenh_sau_lung_hop` · `::test_F2_ESC_khi_GO_CA_N_dang_cho__cua_LOI__nguoi_VAN_THAY_loi` · `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo` · `::test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon`. `1 xfailed` có từ trước. ⛔ đỏ nào khác *(gồm `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền 55**; ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (144 file, 1559 bang, 701 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ *(trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` — đo như dòng trên |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` *(dòng `Đang ghi vào sổ…` là `div.note`, ⛔ nút)* |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — ⛔ chạm schema |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-1** ⓐ `kq021` | `pytest --runxfail "tests/nghiem_thu/test_kq021_bo_gan_vong2.py::test_F1_ESC_tren_hop_hoi__chi_DONG_HOP__lenh_VAN_MO"` + `::test_F1_phim_J_khi_hop_MO__KHONG_doi_lenh_sau_lung_hop` ⇒ **passed** *(cả tệp `kq021` + `kq019` `--runxfail`: `17 passed`)*; không `--runxfail` ⇒ `XPASS(strict)` |
| **AC-1** ⓑ bài Dev, **hai** thứ tự | `test_AC1_ESC_tren_hop__CHI_dong_hop__lenh_van_mo[man_truoc\|hop_truoc]` · `test_AC1_phim_man_khi_hop_MO__nam_im[<j·k·ArrowDown·ArrowUp·Enter·ArrowLeft·/>-<thứ tự>]` *(14 bài: `ST.mo` giữ, hộp vẫn mở, 0 ghi)* · `test_AC1_F02_CTRL_Z_khi_hop_MO__ST_lich_khong_doi[…]` *(ô `CDT-X` + `ST.lich` 1 ⛔ đổi)*. **Mẫu số** *(`Đ3`)*: `test_AC1_MAU_SO_hop_DA_dong__phim_man_van_song[…]` *(hộp đóng ⇒ `j` ⇒ `PWB-2`, `Esc` ⇒ `null`)* · `test_AC1_F02_MAU_SO_khong_hop__CTRL_Z_hoan_tac[…]` |
| **AC-1** chiều ĐỎ | trên mã khi nhận *(`7e67a09`)* **15 / 27** đỏ *(lý do: `⛔ Esc ⛔ đóng hộp` · `⛔ phím 'j' đổi màn sau lưng hộp: 'PWB-2'` · `'ArrowLeft' … None` · `⛔ Ctrl+Z chạy sau lưng hộp`; mẫu số `AC-2` đỏ ở dựng ca vì `Esc` đã đóng lệnh)*. **Đột biến** trên mã mới *(kịch bản phá → chạy → trả nguyên)*: ① bỏ phép hỏi ở `F01G` + `F02` ⇒ **14 failed** *(cả hai thứ tự)* · ② `nuot_phim` bỏ dấu sự kiện ⇒ **2 failed**, **chỉ** `[hop_truoc]` *(= "chặn chỉ đúng một thứ tự ⇒ bài thứ tự kia ĐỎ")* · ③ `nuot_phim` luôn `true` ⇒ **4 failed** = đúng bốn bài **mẫu số** |
| **AC-1** Chrome **8097** sổ thật **chỉ đọc** | `node cdp23ab.mjs 8097 9223 x <man_truoc\|hop_truoc> y` *(scratchpad)*: mở lệnh đầu chip `Chưa gán` bằng chuột *(`PM01698-1`)*, mở một hộp `HT.mo` *(`Runtime`)*, phím **thật** `Input.dispatchKeyEvent`. **Mã mới**, cả hai thứ tự: `j` ⇒ `ST.mo` **giữ** `PM01698-1`, hộp vẫn mở; `Esc` ⇒ hộp đóng, `ST.mo` **giữ**; mẫu số — hộp đóng, `j` ⇒ `PM01089-1`. **Mã khi nhận** *(`worktree` @ `7e67a09`)*, cả hai thứ tự: `j` ⇒ `PM01089-1` **sau lưng hộp**; `Esc` ⇒ hộp đóng **và** `ST.mo = null`. 0 `POST`, console 0 lỗi |
| **AC-2** ⓐ `kq021` | `pytest --runxfail "…::test_F2_ESC_khi_GO_CA_N_dang_cho__cua_LOI__nguoi_VAN_THAY_loi"` ⇒ **passed** |
| **AC-2** ⓑ bài Dev | `test_AC2_GO_CA_N_dang_cho__ESC_va_bam_nen_bi_nuot__loi_hien_TRONG_hop[…]`: `Gỡ cả 2`, cửa `/unmatch` **treo** *(`Promise` chưa giải)* ⇒ `#dlg-b` chứa `Đang ghi vào sổ — chờ máy trả lời.`, hàng nút khoá; `Esc` ⇒ `#scrim.on` **vẫn**; bấm nền *(trình nghe `click` của `#scrim`, `target = #scrim`)* ⇒ **vẫn**; cửa lỗi ⇒ `Không nối được tới máy chủ FLS.` **trong** hộp đang mở, dòng chờ **mất**, nút mở lại, `ST.mo` giữ. **Mẫu số**: `test_AC2_MAU_SO_hop_CHUA_bam_nut__ESC_dong[…]` *(chưa bấm nút ⇒ `Esc` đóng; cửa `200` ⇒ hộp đóng)*. `F01` ⑥ `_bo_ghep` *(cùng khuôn — hàm nút `async` ghi bên trong)*: `test_AC2_F01_bo_ghep_dang_cho__ESC_bi_nuot__loi_trong_hop` |
| **AC-2** chiều ĐỎ | mã khi nhận: dòng chờ ⛔ có *(`('⛔ ⛔ có dòng chờ', …)`)*, `_bo_ghep` hộp đóng. Đột biến: ④ bỏ phép nuốt khi chờ ⇒ **3 failed** *(`GO_CA_N` ×2 + `F01 bo_ghep`)* · ⑤ nuốt `Esc` cả khi ⛔ chờ ⇒ **7 failed** *(gồm mọi bài **mẫu số**)* |
| **AC-2** Chrome **8097** chỉ đọc | cùng kịch bản: hộp có nút `Ghi` mà hàm nút treo bằng `Promise` *(⛔ cửa nào — 0 `POST`)*; **chuột thật** bấm `Ghi`, **`Esc` thật**, **chuột thật** bấm nền `(5, 5)`. **Mã mới**: `#dlg-b` = `y` ＋ `Đang ghi vào sổ — chờ máy trả lời.`, nút `[Thôi, Ghi]` khoá; sau `Esc` hộp **mở**; sau bấm nền **mở**; nhả lỗi ⇒ hộp **mở**, `#dlg-b` có `Không nối được tới máy chủ FLS.`, dòng chờ mất, nút mở lại; `Esc` lần nữa ⇒ đóng *(⛔ còn chờ)*. **Mã khi nhận**: ⛔ dòng chờ; `Esc` ⇒ **đóng** giữa chừng; lỗi viết vào hộp **đã đóng** |
| **AC-6** | `pytest` toàn bộ: **0** đỏ ngoài đúng **5** `XPASS(strict)` *(liệt kê ở dòng cổng)* · lint `9 kept, 0 broken` · `soi_bang_tuyen` 40 tuyến khớp · `kiem_thuyet_minh` 31/31 · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh · `kiem_tai_lieu` — dòng cổng |
| AC-7 *(phần này)* | `kiem_so_song` **55 = nền**; ⛔ `dong_bo --ghi`; `khop_owner --kiem` **ĐẠT 17/20** đo sau khi viết tờ *(trước commit tờ)* |
| AC-3 · AC-4 · AC-5 · AC-5b · AC-8 · AC-9 · AC-15 | ⏳ **chưa làm** — `BG` sau |

## Kho thật
- `KHONG_CHAM`. Chrome trên **8097** *(sổ thật, `noi_chi_doc`, ⛔ `--cho-ghi`)* — 0 `POST`. Bài `(a)(b)` ⛔ chạm kho *(cửa giả)*.

## Cách chạy để xem
- `PG_DSN=postgresql://fls:fls@localhost:5433/fls FLS_JWT_SECRET=<≥32 ký tự> python tools/chay_cua.py --cho-web --cong 8097` ⇒ tab `②b`, mở một lệnh; trong console: `HT.mo('thử', 'x', [['Thôi', null], ['Ghi', () => new Promise(() => {})]])` ⇒ bấm `Ghi`, `Esc`, bấm nền.

## Dev tự thấy còn yếu
1. **Dấu `e._hop_thoai` là một thuộc tính tự đặt lên đối tượng sự kiện của trình duyệt.** Chạy được trên Chrome 154 *(đo trên)*; ⛔ chuẩn nào cấm, nhưng cũng ⛔ chuẩn nào hứa. Phương án khác *(`stopImmediatePropagation` ở pha capture)* chặn **cả** trình nghe trên phần tử bên trong hộp *(ô lý do)* — tôi ⛔ chọn vì ⛔ đo được ảnh hưởng trên mọi hộp.
2. **Mọi phím** khi hộp mở đều ⛔ tới màn — kể cả `Tab`/`Enter` khi con trỏ ở ô lý do của hộp *(chúng vẫn chạy hành vi mặc định: gõ chữ, bấm nút đang focus)*. Một màn mới thêm trình nghe phím mà quên hỏi `HT.nuot_phim` sẽ lọt — ⛔ có cổng quét. Gợi ý cổng *(chưa làm — ngoài bảng TRONG)*: quét `addEventListener('keydown'` trong `fls/web/tep/man_*.js` đòi có `nuot_phim` trong thân.
3. `dong()` công khai nay trả `true/false` *(trước: `undefined`)* — ⛔ nơi gọi nào đọc giá trị *(`grep HT.dong fls/web/tep` — **0** chỗ ngoài `hop_thoai.js`)*.
4. Một hộp **mới** mở trong lúc lượt ghi của hộp **cũ** còn bay *(vd. hàm nút tự gọi `HT.mo`)*: `Esc` đóng được hộp mới *(mã lượt khác)*; khi lượt cũ xong, `_dong()` vẫn đóng hộp **đang hiện** như hành vi cũ *(⛔ đổi)*. ⛔ Có bài cho ca này.
5. `F02` hộp `Đảo` / `Mở lại` / ô lý do: ⛔ đo riêng bằng Chrome — chỉ bài DOM `Ctrl+Z` *(hộp thử)*.
