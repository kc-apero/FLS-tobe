# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `I1` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-305`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 45 · I1 · `WO-303` · `BG-304` *(`isp/I1` @ `a4dff50`)*

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: y như §1 sổ chung. Sổ **chỉ THÊM**. Vai KIỂM: ⛔ sửa mã.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nhị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `I1-R1-01` | WO-303 | R1 | B1 | **NÊN SỬA** | `fls/repo/doc_bao_cao.py:1017-1062` *(`_cong_hd1`)* · `tools/do_voi_so_luong.py:426` | **Cổng `HD1_THANG` phán 23 kỳ, ⛔ 26** *(xác nhận `I1-P1` bằng đo)*: mẫu số = `dat_hd1.mau_so.so_ky` = 23 *(ảnh sổ 26/08)*; `tu_sinh` = 26 kỳ, 3 kỳ `2026-09·10·11` chỉ ở `tu_sinh`. `fls/` đọc `tu_sinh` **0** chỗ *(grep `fls/`+`tools/` ngoài `do_voi_so_luong.py`; `do_voi_so_luong.py` 24 chỗ)*. `WO-303` AC-3 "x/26" ⛔ thoả. ⚠ `tu_sinh.theo_ky` chỉ có `o·hd·mid·lech_*·o_loi`, ⛔ có vế *dòng ghép 1-1* ⇒ 3 kỳ mới ⛔ thể phán ĐẠT; đúng luật Đ5 là `không đo được`, ⛔ ĐẠT. | Bước sửa riêng (⛔ lane I1): H2/CG1 thêm phán theo kỳ cho 26 kỳ; kỳ thiếu vế dòng ⇒ `null`. Bài ghim `test_P1_…` đỏ ⇒ khai lại `MONG_SO_KY_CONG`. | Đ5: mẫu số của cổng phải = số kỳ có ảnh, so với `len(tu_sinh.theo_ky)` | Mở |
| `I1-R1-02` | WO-303 | R1 | B1 | **NÊN SỬA** | `fls/repo/doc_bao_cao.py:1052-1062` · ISP Step 45 I1-B1 | **`ly_do` ⛔ mang TÊN nhãn DT1b — kể cả khi nhãn CÓ**: `grep "theo_nhan\|DT1b"` trong `doc_bao_cao.py` = **0**. Đo: dựng tệp nhãn GIẢ *(tmp)* ⇒ `dat_hd1.theo_nhan` có 3 nhãn *(`so_dong` 23/99/36)* nhưng `"TONG_HOP" in ly_do` = **False**. ⇒ không phải chỉ do tệp nhãn vắng ở cloud. | Cổng in thêm *nhãn: số dòng* theo kỳ đỏ, hoặc BA đổi chữ ISP I1-B1. Thêm bài có tệp nhãn tmp. | Đ3: bài "nhãn có trong ly_do" phải dựng nhãn trước | Mở |
| `I1-R1-03` | WO-303 | R1 | B1 | **NÊN SỬA** | `BG-304` §Bảng AC10/AC11 | **Gán cột AC10/AC11 sai AP §5.3.2**: AP — **AC10** = dòng ghép 1-1 **và** ô mapping Final 7 khối, "đạt khi cả hai 100 %", cả chế độ tự sinh; **AC11** = riêng ô khối HD *(đọc MID sổ `9.930/9.930` · tự sinh)*. BG gán AC10 = ô HD, AC11 = Final 7 khối ⇒ **đảo**; và AC10 thiếu cột *dòng 1-1* *(đo `dat_hd1`: `dong_100` **5**/23 · `o_100` **22**/23 — ⛔ 23/23, `2026-07` ô ⛔ 100 %)*. | Dán lại bảng: AC10 = dòng 1-1 + Final 7 khối; AC11 = HD; kỳ ngoài cổng ghi "dòng: không đo". | Đ4: nhãn cột theo định nghĩa AP | Mở |
| `I1-R1-04` | WO-303 | R1 | B2 | GHI NHẬN | `docs/ITL/_tools/khop_owner.py --kiem` · `tools/kiem_so_song.py` | Môi trường cloud: `khop_owner --kiem` ĐỎ *(C5·C5b·B3·B4 "không đo được" vì `fls_itl` = 0 dòng)*; `kiem_so_song` lỗi `.venv/Scripts/lint-imports.exe`. Đo: `git diff 800c050 HEAD` = 5 tệp *(tests + sàn + BG)*, ⛔ chạm `fls/` hay `docs/_tools` ⇒ có sẵn ở nền. | Backlog môi trường *(đường `.venv/bin`)* | — | Ghi |
| `I1-R1-05` | WO-303 | R1 | B2 | GHI NHẬN | `BG-304` bảng 26 hàng, cột cuối | Cột "HD1_THANG kỳ" ⛔ mang nhãn mốc *(là ảnh **26/08**, khác cột mốc 20/11 bên cạnh)*; đặt cạnh nhau `2025-03` ĐẠT mà Final `2077/2079` ⇒ trông mâu thuẫn *(hai mốc khác nhau — chính là `I1-R1-01`)*. `2026-03` mốc CŨ ⛔ lẫn cột cổng. | Thêm nhãn mốc cho từng cột | Đ4 | Ghi |
| `I1-R1-06` | WO-303 | R1 | B2 | GHI NHẬN | `tests/tich_hop/test_hd1_xuyen_suot.py:132-141, 156` | Độc lập tầng: ③-vm dùng cửa giả `FLS.doc` *(chỉ Chromium fetch thật)*; ③ so "chuỗi ly_do của ②" ⇒ ③ ⛔ độc lập với ②; ①↔② bóc `ky_do` bằng regex trên văn bản. Đột biến M1 *(tool)* & M6 *(sổ lý do thật)* đỏ nhờ cổng nội tại công cụ, ⛔ nhờ assert bài. Chữ ký giả: `TONG_HOP_TEST` chỉ ở bài/BG/`test_do_voi_hd1`/`KQ-092`; `so_ly_do_hd1.json` `chu_ky == []`. | Backlog | — | Ghi |
| `I1-R1-07` | WO-303 | R1 | B2 | GHI NHẬN | `test_B2_…` | B2 chỉ phủ tệp **vắng**; tệp hỏng/khối hỏng ⛔ trong I1 *(đã ở CG1)*. | Backlog | — | Ghi |

## Đo R1 *(mỗi số nói nó đếm gì)*
- **Đo lại độc lập 5/23**: `theo_ky` của `dat_hd1` đạt **5** *(2024-10·11·12 · 2025-03·04)* · đỏ **18** · Σ dòng thiếu **122** = `phan_loai_dong_thieu.json` **122** *(khớp từng kỳ)*; ③ tầng chạy lại sống = tệp commit; đỏ ⇒ `thieu>0` cả 18, đạt ⇒ `thieu=0` cả 5.
- **Ba tầng thật**: ① `do()` sống → JSON tạm · ② HTTP thật · ③ vm + Chromium thật *(11/11, 0 skip)*. Lan truyền: bật `2025-01` xanh ở công cụ ⇒ ① 6/23 · ② 6/23, `2025-01` rời danh sách đỏ · ③ "6/23".
- **Đột biến** *(bản sao `git archive`)*: **8/8 đỏ** — M1 công cụ · M2 cổng `dat` · M3 bỏ kỳ đỏ cuối · M4 vắng→false · M5 F03 fail→pass · M6 chữ ký vào sổ thật · M7 tệp commit lệch · M8 nhãn mốc.
- **Sàn**: `--collect-only` **4.561** *(= 4.550 + 11)* · web **690**.
- **Cổng**: `--duong-nen --cong 5446` MỘT lần **ĐẠT** *(28 = 28, thêm 0 · bớt 0; chạy 4.561; web 3 = 3, 690)* · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT *(454 tệp · 2.885 bảng)* · `kiem_thuyet_minh` 35/35.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `I1`, `KQ-305`)*: khởi tạo — **7** phát hiện *(0 CHẶN · 3 NÊN SỬA · 4 GHI NHẬN)*.
