# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `C13B` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-301`)* · **Nguồn:** `WO-299` · `BG-300` · `BG-258` (C13) · sổ `C13` mục `C13-R1-02`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: **y như** §1 sổ chung. Sổ **chỉ THÊM**.
> Kiểm `isp/C13B` @ `e3c68be` trên **cây gộp thử** `origin/claude/bold-galileo-zukpaf` @ `ad9b70f` + `isp/C13B` *(⛔ commit; vai KIỂM ⛔ sửa mã — đột biến chỉ trên bản sao `git archive`)*.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `C13B-R1-01` | C13B | R1 | B2 | GHI NHẬN | `tests/cau_hinh/test_ban_ky_pg.py:317-350` *(`test_C13_R1_02_…` song song)* | **Bài song song BẮT lỗi rất hiếm — bài tất định mới mới là lưới chính.** Đo dưới tải 3 tiến trình pytest độc lập: mã CŨ đỏ **2/100** lần *(không tải: đã xanh khi dev đo)*; mã MỚI **0/100**. Phép đo CÓ răng *(Đ3/Đ5: mã cũ đỏ ≥ 1)* nhưng tỉ lệ thấp ⇒ ⛔ dựa riêng bài song song. | Giữ bài tất định `test_C13B_AC1/AC2_…` làm cổng; bài song song chỉ là bằng chứng bổ sung. | Bài phát hiện lỗi phải có phiên bản **ép đua tất định** *(khe `IDLE` giữa khoá và đọc)* | mở *(GHI NHẬN ⇒ backlog)* |
| `C13B-R1-02` | C13B | R1 | B1 | GHI NHẬN | `fls/repo/cau_hinh_repo.py:823-860` *(`dua_ban_ky`/`ky_ban`)* | **Đúng đắn dựa vào mức cô lập `READ COMMITTED` mặc định + kết nối `autocommit`** — ⛔ đổi mã nào. Đo: `grep isolation\|REPEATABLE\|SERIALIZABLE` trên `fls/` = **0** chỗ; mọi kết nối mở ở `fls/db/kho.py` là `autocommit=True` *(xu_ly.py:1140 dùng `yc.conn`)*. Người gọi truyền kết nối `REPEATABLE READ` đã mở snapshot *trước* khoá ⇒ `_sk_ban_ky` đọc cũ ⇒ `UNIQUE(bang,phien_ban)` nổ. Hiện ⛔ có người gọi như vậy. | Một dòng chú thích ở docstring hai hàm: "giả định READ COMMITTED". | — | mở *(GHI NHẬN ⇒ backlog)* |
| `C13B-R1-03` | C13B | R1 | B1 | GHI NHẬN | `fls/repo/cau_hinh_repo.py:63-67` *(`BANG_HOP_LE` có `IX.TMP`)* · `nap` | **`nap(conn,"IX.TMP",…)` công khai vẫn chạy được**: đo trên kho TEST `nap(c,"IX.TMP",[("x",1)],nguon="tay",actor="kiem")` ⇒ nhận, cấp phiên bản **74** *(mẫu số 1)*. Cùng khoá advisory `hashtext('IX.TMP')` nên ⛔ phá đua; `_sk_ban_ky` lọc theo `nguon IN ('ban:','ky:')` nên ⛔ nhìn thấy dòng ấy ⇒ vô hại với C13b, chỉ tốn một số phiên bản. Có từ trước C13b. | BA/Dev cân nhắc loại `IX.TMP` khỏi `nap` chung. | — | mở *(GHI NHẬN ⇒ backlog)* |
| `C13B-R1-04` | C13B | R1 | B2 | GHI NHẬN | `tools/dung_moi_truong_isp.sh:420-424` · `tests/test_dung_moi_truong_isp.py:420-430` | **Xung đột sàn ở cây gộp thử** *(nhánh làm việc `4621` ↔ `isp/C13B` `4537`)* ⇒ gộp tay: giữ bản nhánh làm việc, đặt sàn = thu thập thật cây gộp **4.624** *(= 4.621 + 3 bài C13b; web 690)*. Đường nền: 4.624 bài chạy · 0 skip · 0 deselect · tập đỏ 28 = 28 · web 3 = 3. | Orchestrator gộp `isp/C13B` theo `isp-gop-buoc`: sàn **4624**. | Sàn = số thu thập CÂY GỘP, ⛔ cộng tay | mở *(GHI NHẬN ⇒ backlog)* |

## Đo R1 *(mỗi số nói nó đếm gì)*
- **Bài tất định** *(`test_C13B_AC2_dua_ban_ky…` · `test_C13B_AC1_ky_ban…`)*: mã MỚI xanh **14/14** `test_ban_ky_pg.py`; mã CŨ *(`git archive` `ad9b70f` + tệp bài mới)* **2 failed · 1 passed** *(bài thứ ba `khong_doi` xanh vì không đụng khe)*. Mẫu số: hook CHÈN thật **1 lần** từ kết nối `c2` khác vào khe `IDLE` ở mã cũ *(`da_chen=[1]`, kho 3 bản)*; mã mới không có khe ⇒ `da_chen=[]`, kho 2 bản.
- **Tải độc lập** *(lệnh: `tai.sh` — 3 vòng lặp `pytest tests/cau_hinh tests/api` mỗi vòng một kho `fls_test_t1..3`, song song với 100 lần `pytest tests/cau_hinh/test_ban_ky_pg.py -k test_C13_R1_02` ở kho `fls_test_m`; mỗi lần = 2 bài)*: **mã cũ 2/100 đỏ** *(lần 27 · 40)* · **mã mới 0/100** *(100/100 `2 passed`)*.
- **`ky_ban`** cùng mẫu đã sửa: trả đúng bản vừa ký `(phiên bản 1, checksum bản 1, da_ky)` dù luồng khác chèn bản `n+1` ngay sau khối; `dua_ban_ky` nhánh `khong_doi` ⇒ đúng bản, `True`; nhánh `DaKy`/`ThangKhongCo` ném trong khối *(⛔ đọc lại)*.
- **Khe khác** *(đọc `cau_hinh_repo.py:790-860`)*: mọi đọc `_sk_ban_ky` của hai hàm ghi đều TRONG `with conn.transaction()` sau `pg_advisory_xact_lock` ⇒ ⛔ còn khe; `_them_su_kien` đọc `max(phien_ban)` trong khoá. Còn lại: `-02` *(cô lập)*, `-03` *(nap chung)*.
- **Tuyến/hợp đồng**: ⛔ đổi `report/snapshot` · tuyến · di trú *(diff nhánh chỉ 3 tệp: mã · bài · BG)*. F7 `test_isp_f08_ky_ban_pg.py` + C13 cũ xanh **83 passed** cùng `test_dung_moi_truong_isp.py`.
- **Đột biến `git archive`** *(6 chỗ, tập `test_ban_ky_pg.py` + F7, 23 bài)*: **6/6 cắn** — M1 hoàn nguyên `dua_ban_ky` *(1 đỏ)* · M2 hoàn nguyên `ky_ban` *(1 đỏ)* · M3 bỏ khoá advisory `dua_ban_ky` *(1 đỏ)* · M4 `[0]` thay `[-1]` *(5 đỏ)* · M5 `ky_ban` trả bản chưa ký *(2 đỏ)* · M6 `khong_doi=False` *(2 đỏ)*.
- **Cổng**: `--duong-nen --cong 5444` một mình **KẾT: ĐẠT** — `12 failed, 4596 passed, 2 xfailed, 14 errors` = **4.624** · tập đỏ 28 = 28 · web `3 = 3` / 690 · `lint-imports` 11 kept · 0 broken.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `C13B`, `KQ-301`)*: khởi tạo — **4** phát hiện `C13B-R1-01…04` *(0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN)*.
