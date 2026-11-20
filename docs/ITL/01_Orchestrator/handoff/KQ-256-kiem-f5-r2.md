# KQ-256 — R2 cuối kiểm `BG-254` *(vòng sửa sau `KQ-255`)* · ISP Step 37 · F5 *(SCR-F08 ký tháng tỷ giá)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 1 GHI NHẬN mới** *(`F5-R2-01`, có sẵn từ trước vòng sửa)*. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_F5.md` (v0.2). Đo trên `isp/F5` @ `61fb607`, cụm `5446`, Chromium thật + máy chủ thử + kho TEST. Cây gộp thử `thu/F5` = `origin/claude/bold-galileo-zukpaf` @ `8445324` + `isp/F5`: **gộp sạch, 0 xung đột** *(⛔ commit cây này)*.

## Đóng phát hiện R1 *(kịch bản tự viết, tháng KHÁC bài của Dev)*
| Mã | Kết | Đo |
|---|---|---|
| `F5-R1-01` | **ĐÓNG** | cuộn giữa bảng tới `202603`: `scrollY` **704 → >0** *(không về 0)*; dòng trong khung `top ≥ 0 · bottom ≤ 800`; `activeElement` = `TR` của `202603`; dòng *đã ký · thẻ · ngày*, nút `disabled`, hộp đóng; kho có chữ ký |
| `F5-R1-02` | **ĐÓNG** | người khác ký `202601` *(201, Đ3 — mẫu ≠ rỗng)* ⇒ màn ký ⇒ hộp giữ *"đã được ký rồi"* tiếng Việt, ⛔ mã thô; dòng nền hiện *đã ký · ke.toan.f5@vi-du.invalid · 2026-11-20* + nút khoá; 2 POST *(1 ngoài + 1 màn)* |
| `F5-R1-05` | **ĐÓNG** | `anh_BG-254/f5_sau_ky_cuon.png`: PNG **1100×800**; nhìn thấy dòng `202508` *đã ký · ke.toan.f5@vi-du.invalid · 2026-11-20* + nút xám giữa các dòng `Ký tháng` — khớp mô tả `BG-254` |

## Không hồi quy `F5-F1/F2/F3` *(đo ngoài bài)*
Huỷ ⇒ **0** POST, dòng chưa ký · bấm **đúp** nút xác nhận ⇒ đúng **1** POST, thân `{}` *(⛔ `actor`)* · `test_isp_f08_ky_pg.py` **6/6** xanh trên `isp/F5`.

## Đột biến — **4/4 BẮT** *(bản sao `git archive isp/F5`, mỗi bản đổi **1** dòng `man_f08.js`; nền xanh trước đó)*
| Đột biến | Bài đỏ |
|---|---|
| bỏ `scrollTo(0, y)` | `F5_R1_01` + bài tự viết |
| bỏ tải lại sau 409 | `F5_R1_02` + bài tự viết |
| tải lại **sai dòng** *(`tr[data-thang="202401"]`)* | `F5_R1_01` + bài tự viết |
| bỏ trả tiêu điểm | `F5_R1_01` + bài tự viết |

## Ghi nhận mới
`F5-R2-01` *(B2)*: sau 409, tiêu điểm = `BODY` — đo **cả** trước *(`2366257`)* **và** sau vòng sửa ⇒ có sẵn, thuộc `F5-R1-04`. ⛔ chặn.

## Cổng *(cây gộp thử, `--duong-nen --cong 5446`, MỘT lần, một mình)*
Lần chạy đầu bị công cụ nền ngắt sau khi xong lượt *toàn bộ* *(không phải kết quả)*; **chạy lại trọn một lần**: toàn bộ `12 failed · 4197 passed · 2 xfailed · 14 errors` — tập đỏ **28 = 28** *(thêm 0 · bớt 0, chạy 4225 ≥ 4225)* · `tests/web` `3 failed · 678 passed` — **3 = 3**, chạy 681 ≥ 681 · KẾT ĐẠT. `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT *(402 tệp, 104 mã QĐ)* · `kiem_thuyet_minh` 33/33. Sàn `4225`/`681` = thu thập thật.

## Việc kế
Orchestrator: gộp `isp/F5` theo `isp-gop-buoc` *(0 CHẶN · 0 NÊN SỬA)*; backlog `F5-R1-03/04/06/07` + `F5-R2-01`.
