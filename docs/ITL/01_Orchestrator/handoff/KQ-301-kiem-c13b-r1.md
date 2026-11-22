# KQ-301 — R1 `WO-299` / `BG-300` *(ISP 3.1.2 · C13b — `dua_ban_ky`/`ky_ban` trả đúng phiên bản khi chạy song song)*

| | |
|---|---|
| **Kết quả** | **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN** |
| **Phát bởi** | `fls-test` *(R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/C13B` `e3c68be` + cây gộp thử *(⛔ commit)* · cụm 5444 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C13B.md` *(v0.1)* |

## Kết luận từng trọng tâm
1. **Bài tất định ép đua thật**: hook chèn bản từ kết nối `c2` khác vào khe `IDLE` *(1 lần, kho 3 bản)*. Mã cũ **2 đỏ · 1 xanh** · mã mới **14/14 xanh**.
2. **Dưới tải độc lập** *(3 tiến trình pytest + 100 lần `test_C13_R1_02`)*: mã cũ **2/100 đỏ** *(phép đo có răng)* · mã mới **0/100**.
3. **`ky_ban`** sửa đúng; `khong_doi` · `DaKy` · `ThangKhongCo` đúng bản/đúng lỗi.
4. ⛔ đổi tuyến/hợp đồng `report/snapshot`; C13 + F7 **83 passed**.
5. **Khe khác**: ⛔ còn khe sau khoá; giả định `READ COMMITTED` + `autocommit` ⇒ `-02`.
6. **Sàn** cây gộp thử: xung đột script + bài ghim ⇒ gộp tay = thu thập thật **4.624**; `--duong-nen` ĐẠT *(28=28 · web 3=3)* · lint 11/0.
7. **Đột biến** **6/6** cắn.

## GHI NHẬN ⇒ backlog
`C13B-R1-01` bài song song chỉ bắt 2/100 dưới tải (lưới chính = bài tất định) · `-02` đúng đắn dựa READ COMMITTED + autocommit · `-03` `nap` chung nhận `IX.TMP` · `-04` sàn gộp = **4624**.

Việc kế: orchestrator gộp `isp/C13B` *(`isp-gop-buoc`; sàn 4624)*.
