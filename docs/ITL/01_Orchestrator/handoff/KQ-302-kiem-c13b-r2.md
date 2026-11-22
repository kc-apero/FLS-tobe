# KQ-302 — R2 CUỐI `WO-299` / `BG-300` *(ISP 3.1.2 · C13b — `dua_ban_ky`/`ky_ban` trả đúng phiên bản khi song song)*

| | |
|---|---|
| **Kết quả** | **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 5 GHI NHẬN** *(R1-01…03 + R2-01 mở; R1-04 bị R2-01 thay)* |
| **Phát bởi** | `fls-test` *(R2 cuối, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/C13B` `290059c` + cây gộp thử `cff858a` *(⛔ commit)* · cụm 5444 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C13B.md` *(v0.2)* |

## Kết luận
1. **Cây gộp thử** lên ngọn nhánh làm việc mới nhất `cff858a` *(đã có C10 · H12 · H15)*: **2 xung đột** *(script sàn + bài ghim sàn)* ⇒ gộp tay giữ bản nhánh làm việc; thu thập thật **4656** *(= 4653 + 3 bài C13b)*.
2. **Bài** `test_ban_ky_pg.py` + `test_isp_f08_ky_ban_pg.py`: **23 passed** *(2 bài tất định + bài đua)*.
3. **30 lần dưới tải** *(3 tiến trình pytest đồng thời × 10, mỗi tiến trình một kho test)*: **30/30 · 0 đỏ**. *(Lần đo đầu chung `fls_test` ⇒ đỏ do tiến trình drop kho nhau — lỗi hạ tầng đo, loại.)*
4. **4 GHI NHẬN R1**: ⛔ nâng. `-02` đo cho H14: `isolation|REPEATABLE|SERIALIZABLE` = **0** chỗ ở `fls/`+`tools/` · mọi kết nối `autocommit=True` · server `read committed` · bên gọi `ky_ban` = 1 *(`yc.conn`)*, `dua_ban_ky` ngoài định nghĩa = 0 ⇒ rủi ro đo được = 0. `-04` thay bằng `R2-01`.
5. **Đột biến mới** **4/4 cắn** *(đọc sau khối `dua_ban_ky` · `ky_ban` · `[0]` · `ky_ban` trả bản chưa ký)*.
6. **Cổng**: `--duong-nen` ĐỎ có chủ đích — chạy **4656** · skip 0 · deselect 0 · tập đỏ 28 cũ + **1** bài ghim sàn *(`test_S0_R3_02_…`: sàn 4653 ≠ 4656)* · web `3 = 3`. `lint-imports` 11/0 · `kiem_tai_lieu` K1–K6 OK.

## Việc kế
Orchestrator gộp `isp/C13B` *(`isp-gop-buoc`)*: đặt `MONG_PYTEST_TOAN_BO=4656` + dòng gộp trong bài ghim *(sàn = thu thập cây gộp, ⛔ cộng tay)*.
