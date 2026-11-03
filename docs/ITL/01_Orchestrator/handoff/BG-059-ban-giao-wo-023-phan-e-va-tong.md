# BG-059 — bàn giao `WO-023` **phần `(e)`** + **tờ tổng** *(vòng 1)*: khối `SINH-KHOP` chỉ mang QUAN HỆ · cả mười phần của phiếu đã giao

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — phần `(e)` *(`AC-5` · `AC-5b`)* + **tổng** `AC-6` · `AC-7` cho cả phiếu. Spec: `WO-023` `(e)` + mở rộng *(khuôn `WO-011 T6 ⓒ`)* · `KQ-021 F-4` · `KQ-025 F-1` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `aa292e5` *(mã + khối sinh lại + bài)* · `205ffdd` *(changelog Dev)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Các `BG` của phiếu** | [`BG-052`](BG-052-ban-giao-wo-023-phan-i.md) `(i)` · [`BG-053`](BG-053-ban-giao-wo-023-phan-h.md) `(h)` · [`BG-054`](BG-054-ban-giao-wo-023-phan-a-b.md) `(a)(b)` · [`BG-055`](BG-055-ban-giao-wo-023-phan-c-d-j.md) `(c)(d)(j)` · [`BG-057`](BG-057-ban-giao-wo-023-phan-f-g.md) `(f)(g)` · **tờ này** `(e)` ⇒ `WO-023` → **`CHO_TEST`** |
| **Ngoài phần đã giao** | `(h)` ⓓ *(`GAP-SCR-35` `F04` — "tuỳ, Dev gom nếu rẻ")* **⛔ gom** *(`BG-053` mục yếu 5)* |
| **Câu hỏi mở** | [`HOI-056`](HOI-056-chu-het-gio-cho-cu-gan.md) `KHONG_CHAN` *(chữ hết giờ cho `Gán`)* · [`HOI-058`](HOI-058-bai-kq019-nhat-ky-so-that-giu-oracle-v4-8.md) `KHONG_CHAN` *(bài `kq019` giữ oracle v4.8 ⇒ `AC-6` ⛔ trọn)* |

## Đã đổi *(phần `(e)`)*
| Tệp | Vì sao |
|---|---|
| `docs/ITL/_tools/khop_owner.py` | hàm `_co(n)` *(`co` / `⛔ khong co` — ⛔ chữ số)*; sáu phép `_t2` · `_b5` · `_c2` · `_c3` · `_c4` *(phần `n_td`)* · `_c7` đặt ô **tài liệu** bằng quan hệ, số đếm vào `Ket.man` *(in ra **màn** — khuôn `B3`/`B4`)*. `B5`: tên tệp neo *(mang chữ số `06`)* ra khỏi ô *(`AC-5`: ô `B5` **0** chữ số)*, vào màn. Số đếm **từ mã** *(`len(BANG_COT)`, `CANON_COLS`, `nen`/`cn`)* **giữ** trong khối. `mong` của **mọi** phép ⛔ đổi. Chú thích bia đặt trên `_t1` |
| `docs/ITL/_AUDIT_ALIGNMENT_ROADMAP.md` *(khối `SINH-KHOP` — sinh máy)* | chạy `khop_owner.py` *(⛔ `--kiem`)* **một** lần ⇒ `lo trinh: DA GHI` *(6 dòng đổi, đúng sáu phép)*; rồi `--kiem` ĐẠT. ⛔ chạm chữ nào ngoài khối |
| `tests/test_wo023_e_khoi_sinh_khop_chi_quan_he.py` *(mới)* | 14 bài: hàm thật trên `Boi` thật *(đọc toàn bộ `.md`)* — ô ⛔ chữ số *(ngoài chính cụm `«…»`)* · màn có số · thêm một lần cụm ⇒ ô ⛔ đổi, màn đổi · xoá mọi lần cụm `B5`/`C3` ⇒ `khop` lật |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | dòng `(e)` |

⭐ `grep -n "b\.dem\|b\.dem_tep" docs/ITL/_tools/khop_owner.py` @ `aa292e5`: `_t2` *(`dem_tep`)* · `_t3` *(`b.dem("| Tên đang lưu hành …") > 0` — **đã** là quan hệ, ⛔ đổi)* · `_b5` · `_c2` · `_c3` · `_c4` · `_c7` ⇒ đúng sáu phép phiếu kê, ⛔ phép thứ bảy.

| Phép | Ô tài liệu **trước** *(khối @ `090bd1e`)* | Ô tài liệu **sau** | Màn *(sau)* |
|---|---|---|---|
| `T2` | `3 tep KHAI ten tep AS-IS (⛔ tru lo trinh)` | `tep KHAI ten tep AS-IS (⛔ tru lo trinh): co` | `3 tep KHAI ten tep AS-IS (⛔ tru lo trinh)` |
| `B5` | `` `06_SCREEN_SPEC.md` (`BA-06`) nhac co che de xuat 61 lan `` | `` tep spec man hinh (`BA` man) nhac co che de xuat: co `` | `` `06_SCREEN_SPEC.md`: «đề xuất» 20 + «gợi ý» 41 = 61 lan `` |
| `C2` | `«64 cột» xuat hien 30 lan` | `«64 cột» co trong tai lieu: co` | `«64 cột» xuat hien 30 lan` |
| `C3` | `«7 trường» xuat hien 60 lan` | `«7 trường» co trong tai lieu: co` | `«7 trường» xuat hien 60 lan` |
| `C4` | `khai «52 cột» (27 cho, phan lon la BIEN BAN)` | `khai «52 cột» (phan lon la BIEN BAN): co` | `«52 cột» 27 cho` |
| `C7` | `khai «24 nen + 28 canon» 1 cho` | `khai «24 nen + 28 canon»: co` | `«24 cột nền» 1 · «28 vị trí canon» 1 ⇒ min 1 cho` |

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `aa292e5` — mã ⛔ đổi ở `205ffdd`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `6 failed, 2400 passed, 1 xfailed in 458.40s (0:07:38)` — **5** = `XPASS(strict)` đúng `AC-6`: `tests/nghiem_thu/test_kq021_bo_gan_vong2.py::test_F1_ESC_tren_hop_hoi__chi_DONG_HOP__lenh_VAN_MO` · `::test_F1_phim_J_khi_hop_MO__KHONG_doi_lenh_sau_lung_hop` · `::test_F2_ESC_khi_GO_CA_N_dang_cho__cua_LOI__nguoi_VAN_THAY_loi` · `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo` · `::test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon` ＋ **1** = `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong` *(oracle v4.8 ⟷ spec v4.12 — `HOI-058`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền 55** *(`KQ-050`)*, ⛔ đổi suốt phiếu; ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (149 file, 1579 bang, 703 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ + sửa README/dashboard/`WO-023` *(trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | @ `aa292e5` *(trước tờ)*: `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)`; đo lại sau khi viết tờ *(cây làm việc gồm tờ)*: `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT …` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — cả phiếu ⛔ chạm schema |

## Bằng chứng từng AC *(phần `(e)` + tổng)*
| AC | Bằng chứng của Dev |
|---|---|
| **AC-5** *(e)* | `khop_owner.py --kiem` ĐẠT *(dòng cổng)*; ô `B5` trong khối = `` tep spec man hinh (`BA` man) nhac co che de xuat: co `` — **0** chữ số; màn in `«đề xuất» 20 + «gợi ý» 41 = 61 lan`. **Bản sao tạm** *(`fls/` + `tools/` + `docs/ITL/` chép vào thư mục tạm, chạy `khop_owner.py --kiem` của bản sao — ⛔ chạm repo)*: ⓐ thêm **một** `gợi ý` vào `BA-06` ⇒ `--kiem` **rc 0** *(vẫn ĐẠT)* — **mã cũ** cùng lượt ⇒ **rc 1** `khoi trong lo trinh LECH`; ⓑ xoá **mọi** `đề xuất`/`gợi ý` khỏi `BA-06` ⇒ `B5 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH` ⇒ **rc 1** *(cổng NO, `mong=True`)* |
| **AC-5b** *(e mở rộng)* | bảng `phép · ô trước · ô sau` ở trên. Bản sao tạm: thêm **một** lần **mỗi** cụm *(`gợi ý` vào `BA-06` + tệp mới chứa `64 cột · 7 trường · 52 cột · 24 cột nền · 28 vị trí canon · File 1_2`)* ⇒ **mã mới** `--kiem` **rc 0**. ⭐ Dự đoán của phiếu *("khối còn số ở một phép ⇒ lượt thêm chữ ĐỎ đúng ở phép ấy")* đo trên **mã cũ**, mỗi cụm **một** lượt riêng ⇒ dòng khối đổi: `File 1_2` ⇒ `['T2']` · `gợi ý` ⇒ `['B5']` · `64 cột` ⇒ `['C2']` · `7 trường` ⇒ `['C3']` · `52 cột` ⇒ `['C4']` · `24 cột nền 28 vị trí canon` ⇒ `['C7']` — **6 / 6** đúng phép. Xoá **mọi** `7 trường` ⇒ `C3 ⛔ DOI TRANG THAI … LECH` ⇒ **rc 1**. Bài `tests/test_wo023_e_…` **14** xanh trên mã mới, **14** đỏ trên `khop_owner.py` @ `090bd1e` |
| **AC-6** *(tổng)* | `pytest` toàn bộ: **5** `XPASS(strict)` đúng tên *(dòng cổng)* ＋ **1** đỏ ngoài dự kiến — bài nghiệm thu `kq019` giữ oracle v4.8 mà `(f)` *(spec v4.12)* buộc đổi ⇒ **`HOI-058`** *(⛔ sửa bài `tests/nghiem_thu/**`)*. Lint 9/0 · `soi_bang_tuyen` 40 tuyến · `kiem_thuyet_minh` 31/31 · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh · `kiem_tai_lieu` ĐẠT ⇒ `AC-6` **⛔ ĐẠT trọn** tới khi `HOI-058` được trả |
| **AC-7** *(tổng)* | `kiem_so_song`: nền đầu phiếu **55** ⟷ mọi `BG` **55** — ⛔ đỏ mới loại *(c)*; ⛔ `dong_bo --ghi` suốt phiếu. `khop_owner --kiem` mỗi `BG` đo **sau** khi viết tờ *(cây làm việc gồm tờ, trước commit tờ)*; tờ này: dòng cổng |
| AC-1 … AC-4 · AC-8 … AC-15 | ở các `BG` từng phần *(bảng đầu tờ)* |

## Kho thật
- `KHONG_CHAM` cả phiếu *(chỉ `SELECT` qua `noi_chi_doc`; Chrome trên **8097** ⛔ `--cho-ghi`, 0 `POST`; ⛔ chạm 8088)*. `(e)` đọc kho thật chỉ-đọc như mọi lượt `khop_owner`.

## Cách chạy để xem
- `python docs/ITL/_tools/khop_owner.py --kiem` ⇒ dòng `· …` dưới mỗi phép là số đếm *(màn)*; khối trong `_AUDIT_ALIGNMENT_ROADMAP.md` chỉ còn `co` / `⛔ khong co`.

## Dev tự thấy còn yếu
1. **`AC-6` ⛔ trọn** *(`HOI-058`)* — phiếu đóng được chỉ khi `fls-test` cập nhật oracle `kq019` theo `la_ban_dao`, hoặc `fls-ba` chọn phương án khác.
2. Trên mã cũ, bài `test_AC5_XOA_moi_lan_cum__khop_LAT` đỏ **vì chữ** *(`⛔ khong co` chưa có trong ô)* chứ ⛔ vì `khop` — `khop` lật được cả ở mã cũ. Lo của bài là *"phép vẫn đo sau khi bỏ số"*; chiều đỏ thật của lo ấy là đột biến *"`khop=True` hằng"* — **chưa chạy**.
3. Ô `B5` bỏ hẳn tên tệp neo *(để đạt "0 chữ số")* — người đọc khối mất tên tệp, phải nhìn màn. Nếu `fls-ba` muốn giữ tên tệp trong ô, `AC-5` phải đổi thành *"0 chữ số đếm"*.
4. Khối `SINH-KHOP` vẫn còn **chữ số** ở các ô **khác** *(cột `Phát biểu`, `CHUẨN`, `Mã nguồn` — vd `` `len(BANG_COT)` = 52 ``)*: đó là số **từ mã / khai** *(phiếu: giữ)*, nhưng một phép nào **sau này** đọc số đếm chữ vào cột `Mã nguồn` sẽ lọt — ⛔ có cổng quét.
5. Bản sao tạm chép `fls/` + `tools/` + `docs/ITL/` — `khop_owner` còn đọc gì ngoài ba thư mục ấy thì lượt thử đã ⛔ thấy *(lần đầu thiếu `tools/` ⇒ `T3` ⛔ đo được — đã thêm)*.
