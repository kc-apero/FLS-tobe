# KQ-255 — R1 kiểm `WO-253` · `BG-254` · ISP Step 37 · F5 *(SCR-F08 ký tháng tỷ giá)*

**Kết luận: ĐẠT CÓ ĐIỀU KIỆN — 0 CHẶN · 2 NÊN SỬA · 5 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_F5.md` (v0.1). Đo trên `isp/F5` @ `2366257`, cụm `5446`, Chromium thật + máy chủ thử + kho TEST.

## AC
| AC | Kết | Đo |
|---|---|---|
| F5-F1 | ĐẠT | `202510`: hộp mở, **0** POST trước xác nhận; đúng **1** POST thân `{}`; dòng *đã ký · thẻ · ngày*; nút `disabled`; kho `actor` = thẻ |
| F5-F2 | ĐẠT | ký lại ⇒ *"đã được ký rồi"*, ⛔ mã thô; hộp ở nguyên *(nhưng xem `F5-R1-02`)* |
| F5-F3 | ĐẠT | Huỷ ⇒ **0** request POST; Esc / bấm nền cũng **0** |
| AC-4/5/6/7 | ĐẠT | `test_goi_cua_phu_het_ma_loi` xanh; thân POST bắt được `{}` *(⛔ `actor`)*; `actor` trong thân ⇒ cửa 400; thuyết minh 33/33 |

## Tự đo ngoài bài
- **Bấm kép xác nhận** *(3 click, cửa chậm 700 ms)* ⇒ đúng **1** POST; `Esc` lúc đang ghi bị nuốt, hộp hiện *"Đang ghi vào sổ"*. Bấm kép nút dòng ⇒ hộp mở rồi bị click thứ hai đóng, **0** POST.
- **401** *(token hỏng)* ⇒ *"Phiên… hết hạn. Tải lại trang"*, nút **mở lại**, ⛔ treo. **Mạng đứt** ⇒ chữ tiếng Việt + nút mở lại *(kèm "Failed to fetch" thô — `F5-R1-06`)*.
- 390 px: `scrollWidth 390 = clientWidth 390`.
- Ảnh trước/sau *(tự chụp, ⛔ commit)*: trước = 36 nút `Ký tháng`, `202306` chỉ nhãn LẠC; sau = **dòng đã ký nằm ngoài khung** — `scrollY` 554 → 0 *(`F5-R1-01`)*; ảnh `BG-254` *sau* cũng ⛔ thấy dòng ký *(`-05`)*.

## Đột biến — **7/7 BẮT** *(bản sao `git archive`, trả nguyên: `diff` = 0)*
bỏ hộp xác nhận ⇒ 3 đỏ · gửi `actor` ⇒ 3 đỏ · không khoá nút ⇒ 1 · nuốt lỗi 409 ⇒ 1 · POST khi Huỷ ⇒ 1 · nút ở dòng LẠC ⇒ 1 · bỏ vẽ lại ⇒ 1.

## Cổng
`--duong-nen --cong 5446` *(một lần, một mình)*: toàn bộ `12 failed · 4077 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0, chạy 4105 ≥ 4105)*; `tests/web` **3 = 3**, chạy 679 ≥ 679; ĐẠT. `lint-imports` 11/0; `kiem_tai_lieu` ĐẠT; `kiem_thuyet_minh` 33/33.

## Gửi DEV (NÊN SỬA)
`F5-R1-01` giữ vị trí cuộn sau ký · `F5-R1-02` vẽ lại sau 409. GHI NHẬN `-03…07` ⇒ backlog.
