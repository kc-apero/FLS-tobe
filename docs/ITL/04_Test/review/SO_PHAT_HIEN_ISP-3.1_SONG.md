# Sổ phát hiện ISP-3.1 · bước `SONG` *(`WO-345` · R1 `KQ-347` · 23/11/2026)*

Cây gộp thử = `origin/claude/bold-galileo-zukpaf` `577044e` + `26edcf1` *(⛔ commit; 3 xung đột: changelog giữ cả hai · sàn script + bài ghim = **4961** = 4958 + 3, thu thập thật 4961)*.

| Mã | Mức | Phát hiện | Bằng chứng đo | Gửi |
|---|---|---|---|---|
| `SONG-R1-01` | **CHẶN** | Bài DT13 mới đòi tệp `tests/fixture/dau_vao/ccr_daily_report_2_20261123.DO.json` *(sha256 ghim)*, nhưng `.gitignore:26` cấm commit `*.DO.json` ⇒ tệp ⛔ có trong repo ⇒ cây sạch ĐỎ | `git ls-files tests/fixture \| grep -c DO` = 0 · `git check-ignore -v` ⇒ `.gitignore:26` · `pytest tests/du_lieu/test_dau_vao_dt13.py` trên checkout sạch: **1 failed, 42 passed** `FileNotFoundError` · `--duong-nen`: thêm node `test_AC2_anh_cu_va_cong_cu_chung_dung_tung_byte` | DEV |
| `SONG-R1-02` | **CHẶN** | Số HD1 đổi *(`voi_so_luong.json` 2026-11 659→748 dòng …)* làm **hỏng bản ghi PHÁT LẠI** của chuỗi agent `WO-329`: `KhongCoBanGhi: A3_SI_ITL.json ⛔ có lượt cho yêu cầu 19d358a5b379ca84` ⇒ 5 bài `tests/agent/test_chuoi.py` ĐỎ trên cây gộp | nhánh nền `577044e`: `test_chuoi.py` **13 passed**; cây gộp thử: **5 failed** *(`test_AC2_thu_tu_skill_va_agent` · `test_AC5_phat_lai__KET_DAT_lech_0` · `test_AG_R1_05_…` · `test_AG_R1_06_…` · `test_report_html_khop_tep_trong_repo`)* ⇒ `--duong-nen` toàn bộ: tập đỏ **34** (XFAIL 2) vs mong **28** · thêm **6** · bớt 0 | DEV *(ghi lại bản ghi A3 + report HTML theo số mới — cần quyết chủ, vì chạm số ký)* |
| `SONG-R1-03` | NÊN SỬA | BG §2/AC-3 nói đo lại "11 gói = `hd2_cong.json` mới", nhưng `docs/ITL/_tools/hd2_cong.json` chỉ mang **MỘT gói `WP-C2`** *(lần `--ghi` cuối)* ⇒ 10 gói còn lại ⛔ có tệp số để so | `hd2_cong.json` `goi` = `WP-C2` · `tong_o` 63.016 *(khớp tự đo)*; 10 gói kia đối chiếu bằng bảng BG ↔ `tools/do_tren_anh_song.py` | DEV |
| `SONG-R1-04` | GHI NHẬN | `BG-346` lúc giao còn `__SHA__` · `__CONG__`; Dev điền ở `85138dd` *(cổng Dev: `--duong-nen` ĐẠT 28 = 28 trên cây SONG riêng — ⛔ mâu thuẫn `SONG-R1-01/02`: hai lỗi chỉ lộ ở cây sạch / cây gộp)* | `git diff 26edcf1..85138dd` | — |
| `SONG-R1-05` | GHI NHẬN | Phạm vi R1 đã đo: DT12 **5/26 kỳ** tự đọc lại *(3 kỳ đổi + 2 kỳ ≡)*; **52 ảnh HD2** ⛔ đọc lại từ nguồn *(khuôn dựng ở scratchpad Dev — BG tự khai)* ⇒ chỉ chứng bằng cổng + `quet_pii_repo`; đột biến ≥ 6 ⛔ chạy *(phiếu giao 5 mục kiểm, không có mục này)* | — | ORC |
| `SONG-R1-06` | GHI NHẬN | Ảnh CŨ↔MỚI HD2: **10/11 gói giống từng số**; `WP-C5c` đọc ảnh số dư MỚI ⇒ `khop` 77.593 *(cũ 77.672)* · lệch FLS **79** *(lớp lệch thời điểm — Dev khai G3, cổng giữ ảnh 22/11)* — số tự đo trùng BG | `do_tren_anh_song.py --anh cu/moi` | CHỦ *(C3)* |

## R2 cuối `KQ-354` *(24/11/2026)* — ĐẠT 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN
Cây gộp thử = `bold-galileo-zukpaf` `bd3d27a` + `054e067` *(⛔ commit; sàn 4.997 → 5.033 = thu thập thật)*.

| Mã | Mức | Phát hiện | Bằng chứng đo | Gửi |
|---|---|---|---|---|
| `SONG-R2-01` | GHI NHẬN | `do_tren_anh_song.py --anh cu` đo `WP-C5c` ra đúng số ảnh MỚI vì `do_hd2_c5c` đọc thẳng `TEP_LUOT_C5C` *(`_20261123`)* ⇒ công cụ ⛔ tái hiện số CŨ 77.672 | `--anh cu` · `--anh moi` đều `khop` 77.663 · 8.487 | DEV |
| `SONG-R2-02` | GHI NHẬN | khuôn 615 `_song` bỏ khoá `Daily Transactions:No` *(1 hàng · 7 ô)* + `daily_transactions: 0` khỏi `mong` — nguồn đổi, có chú thích; ít hơn 1 hạng mục canh | `ccr_daily_report_song.py` · `test_do_hd2_c5c.py` | ORC |
| `SONG-R2-03` | GHI NHẬN | nguồn sống TIẾP TỤC trôi: tab `5. Daily Report` 24/11 03:06Z = **2.553** hàng ≠ khuôn **2.566** *(23/11 12:11Z)* ⇒ khuôn TỪ CHỐI đúng; ảnh 615 ⛔ đọc lại từng byte được. Giờ đọc từng tab chỉ ở văn bản `BG-346` *(ảnh chỉ mang ngày)*. 6/7 ảnh khác đọc lại ≡ | `dong_bang_sheet ccr_daily_report_song` exit 2 | ORC |


## R2b NHẸ `KQ-354b` *(24/11/2026)* — vòng sửa tích hợp `BG-346` @ `f9b2456` — ĐẠT 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN
Cây gộp thử = `origin/claude/bold-galileo-zukpaf` `ab0f1d0` + `f9b2456` *(⛔ commit)*. *(Sổ này ⛔ có dòng `Version` để bump; các mục trên giữ cột cũ — mục R2b dùng đủ 10 cột sổ chung.)*

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `SONG-R2b-01` | SONG | R2b | A2 | GHI NHẬN | `docs/ITL/04_Test/UAT_STAGING_E2E.md:27` · `tests/staging/test_uat_doc.py` | Số HD2 **⛔ thẻ** ⛔ được canh: đột biến `lech_ban_ccr_vs_cf` 680→681 ở dòng 27 ⇒ `test_uat_doc.py` **6 passed** *(⛔ đỏ)* · `kiem_tai_lieu` ĐẠT. Số không thẻ trong UAT *(đếm 4 số có nguồn trong `hd2_cong.json`: 680 · 35 `ite_alias` · 3.099 `lech_D3` · 7.877 dòng sổ C2 — đều khớp 4/4 hôm nay)* trôi lần sau sẽ xanh. Chính chỗ 671→680 là ca đã trôi | Thêm thẻ `hd2x:615.lech_ban_ccr_vs_cf` + `ite_alias` + `lech_D3` *(Dev sửa bài)*, hoặc bài đếm mọi số ≥ 3 chữ số ⛔ thẻ ở §1/U3 | Đ2/Đ5: mỗi số trong UAT có thẻ hoặc có bài canh; chứng minh ĐỎ bằng đột biến | MỞ → backlog |
| `SONG-R2b-02` | SONG | R2b | A2 | GHI NHẬN | `KQ-354` bảng ký lại hàng 6 · `BG-346:292` | 615 `lech_ban_ccr_vs_cf` **671→680** là số **đo** *(KQ-314 `-02`; `TIEN_DO` 22/11 18:00)*, ⛔ có hàng riêng trong bảng chủ/ThuongCT ký *(hàng 6 chỉ ký `WP-C5c` 77.672→77.663 · 8.478→8.487; 680 là lớp con nằm TRONG lệch 8.487)* ⇒ số 671 ⛔ phải là số đã ký riêng; 680 được phủ gián tiếp bằng việc ký lại hàng 6 | Orchestrator liệt kê 680 *(+9, bản A-CCR đổi từ 22/11)* cạnh hàng 6 khi đưa chủ ký lại | Đ4: số ký ghi rõ nó đếm gì | MỞ → ORC |

**Đo R2b:** (1) 39/39 thẻ `hd2` + 3/3 `hd2x:615` = `hd2_cong.json` *(tự tính lại, cha C3/C4/C5 = Σ con)*; + 4/4 số không thẻ có nguồn ⇒ **46/46**, sai 0. (3) đột biến 1 số không thẻ ⇒ 0 bài đỏ *(`-01`)*. (4) cây gộp thử, `--duong-nen --cong 5444` MỘT lần: `12 failed, 5134 passed, 2 xfailed, 14 errors` ⇒ **28 = 28** *(thêm 0 · bớt 0 · chạy 5.162 ≥ 5.162)* · web **3 = 3** *(690)* · `KẾT: ĐẠT` · `kiem_tai_lieu` 530 tệp ĐẠT · `lint-imports` 11 kept, 0 broken.
