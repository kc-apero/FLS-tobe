# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `F4` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.2 · **Ngày:** 2026-11-18 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-162`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 18 · F4 · `WO-160` · `BG-161`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: y như sổ chung. Sổ **chỉ THÊM**.
> Mọi số R1 **tự đo** trên `isp/F4` @ `d6a91ec`, cụm `5444`, Chromium thật *(Playwright)*; kịch bản ở scratchpad *(⛔ commit)*. Đột biến chạy trên **bản sao** `git archive`, ⛔ chạm worktree. Mẫu số in kèm nhãn *(Đ4)*.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `F4-R1-01` | F4 | R1 | A2 | **NÊN SỬA** | `fls/web/tep/man_f08.js:88-98` *(`TP.el('table')` ⛔ bọc cuộn)* | **Ở 390 px trang TRÀN NGANG.** Chromium thật, tab ⑥ trên kho có ảnh FX đủ 37 hàng: `documentElement.scrollWidth = 475` so `clientWidth = 390` *(dư 85 px)*; bảng `width = 473,6` px, mép phải `474,6` > khung nhìn `390`. Đối chứng ở 1280 px: `1280 = 1280` *(không tràn)*. Bảng 7 cột *(tháng · 5 tiền · trạng thái)* không có vùng cuộn riêng. `BG-161` tự khai *"chưa đo 390 px"*; `WO-160` không có AC bề rộng nên không CHẶN, nhưng đây là điều kiện orchestrator giao đo. | Bọc bảng trong khung `overflow-x:auto` *(dùng lớp có sẵn nếu có)* hoặc rút cột ở màn hẹp; thêm bài Chromium đo `scrollWidth ≤ clientWidth` ở 390 *(mẫu `_do_tran` của `test_isp_f03_hd.py`)*. | Màn có bảng ≥ 6 cột phải có phép đo bề rộng 390 px bằng trình duyệt thật. | **ĐÃ ĐÓNG** *(R2 `KQ-163`: `man_f08.js` bọc `div.ngang`; Chromium 390 px `sw 390 = cw 390`, 37 hàng, khung `overflow-x:auto`; tái đột biến ⇒ ĐỎ)* |
| `F4-R1-02` | F4 | R1 | B1 | GHI NHẬN | `tests/web/test_isp_f08_fx.py` *(mọi bài)* · `man_f08.js:73` | **Đột biến M5 SỐNG:** thay `lac.has(t)` bằng `lac.has(t) && t < '202401'` ⇒ `33 passed` *(bài F08 + token)*. Chỉ có một mẫu `lac = [202306]` ⇒ phép *"màn đọc `lac[]`, ⛔ tự suy"* của spec §9 chưa bị bài nào ép *(một tháng lạc nằm SAU dải, vd `202701`, không có bài)*. 9/10 đột biến còn lại BỊ BẮT *(xem KQ)*. | Thêm bài nuôi `lac=[202701]` *(và `lac=[]` với `202306` có trong `ky`)* ⇒ nhãn theo mảng. | Bài phải đổi mẫu *(đủ hai phía)* cho mọi nhãn lấy từ mảng của tuyến *(Đ5)*. | MỞ |
| `F4-R1-03` | F4 | R1 | B1 | GHI NHẬN | `man_f08.js:109-118` *(`ve` ⛔ truyền `con_hieu_luc`)* | `TT.chay` có tuỳ chọn `con_hieu_luc` *(WO-045: lượt cũ về sau xoá lượt mới)*; F08 ⛔ dùng. Mở tab ⑥ hai lần nhanh ⇒ hai lượt ghi cùng `#than-f08`. Rủi ro THẤP *(bảng chỉ đọc, cùng dữ liệu)*; ⛔ đã đo bằng bài. | Truyền `con_hieu_luc` theo số lượt, như F04. | Màn dùng `TT.chay` truyền `con_hieu_luc` nếu có thể mở lại khi lượt trước chưa xong. | MỞ |
| `F4-R1-04` | F4 | R1 | B2 | GHI NHẬN | `fls/web/tep/index.html:52` · `tests/web/test_isp_f08_fx.py:105` | Nhỏ: tab `⑥ Cấu hình` đứng TRƯỚC `⑤ Danh mục` *(đang `disabled`)* — thứ tự số ⛔ đúng. ISP Step 18 ghi tệp bài `test_isp_f08_fx_pg.py`, thực tế `test_isp_f08_fx.py` *(Dev đã ghi đúng ở BG)*. Bài `AC1` so ô USD bằng `in` sau khi bỏ `.`/`,` ⇒ lỏng *(không so cả 5 tiền)*. | Đổi nhãn/thứ tự tab khi tiện; so đủ 5 cột ở AC-1. | — | MỞ |

## Changelog
- **v0.1** *(2026-11-18, `fls-test` R1 của `F4`, `KQ-162`)*: khởi tạo tệp riêng — **4** phát hiện `F4-R1-01…04` *(0 CHẶN · **1** NÊN SỬA · 3 GHI NHẬN; lớp A2 ×1 · B1 ×2 · B2 ×1)*.
- **v0.2** *(2026-11-18, `fls-test` R2 của `F4`, `KQ-163`)*: `F4-R1-01` ⇒ ĐÃ ĐÓNG. ⛔ phát hiện mới; `F4-R1-02…04` giữ MỞ *(backlog)*.
