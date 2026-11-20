# KQ-267 — R1 kiểm `WO-265` · `BG-266` · ISP Step 38 · DT12 *(ảnh Manual input `ITL Ledge`, kỳ ≠ 2026-03)*

**Kết luận: ĐẠT CÓ ĐIỀU KIỆN — 0 CHẶN · 1 NÊN SỬA · 5 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT12.md` (v0.1). Đo trên `isp/DT12` @ `33ce4b2`, cụm `5437`, đọc lại sổ ADJUSTED bằng khoá SA chỉ-đọc *(⛔ cột `B` · `C`; bản thô đã xoá)*.

## AC
| AC | Kết | Đo |
|---|---|---|
| AC-1 | ĐẠT | **26** kỳ theo cột `A` *(12.655 hàng có ngày)*; 25 ảnh · **12.049** dòng; **25/26** `so_dong` khớp tái đo; so **361.470** ô *(100 %)* lệch **6** — `2026-11` do sổ sống trôi *(`-03`)* |
| AC-2 | ĐẠT | `phan_loai_ky` ⇒ `blocked` có tên; tập rỗng ĐỎ; bài xanh |
| AC-3 | ĐẠT *(cột)* · **NÊN SỬA** *(hình)* | 25/25 cột + thứ tự = ảnh 2026-03; ảnh 2026-03 **0** byte đổi; nhưng khoá cấp trên · bọc `{"chu"}` · `dong_sheet` chuỗi **khác** *(`-01`)* |
| AC-4 | ĐẠT | 0 cột cấm · 0 `@` · 0 email · `quet_pii_repo` = 0 |
| AC-5 | ĐẠT đúng chữ | `_nap` đọc được; nhưng `_chuan` trả `"{'chu': …}"`, `d["ky"]` KeyError ⇒ `-01` |
| AC-6 | ĐẠT | 20.881.876 B · 0 ảnh > 2 MB · đề xuất ở `-04` *(không tách)* |
| AC-7 | ĐẠT | sàn 4267 → 4283 = chạy 4283 *(thu thập = chạy)*, bài ghim cùng commit |

## Tự đo
- **3 kỳ `2024-10/11/12`**: không "lạc" — là 15 hàng đầu sổ `ITL#1…15`, ngày tăng dần *(0 lần lùi / 12.655 hàng)*, Manual 7/7 ⇒ **giữ là đúng**. `#N/A ()` **119/25 kỳ** *(đo lại khớp; 91 % ở 2026-09…11)* ⇒ giữ nguyên, hợp spec. ISP "22" ⇒ 25 (`-02`).
- Ảnh 2026-03 lệch sổ nay *(6.294/16.184 ô theo ITL#)* — xác nhận Giả định 4 của BG *(`-05`)*.

## Đột biến — **13/13 BẮT** + **CLI 4/4** *(bản sao `git archive`, trả nguyên: `diff` = 0)*
bỏ 1 kỳ · đổi 1 ô · thêm `Diễn giải` · thêm `Email Address` · đổi tên cột ảnh · lệch `so_dong` · lệch `cong.mong` · mong số kỳ (manifest) · `MONG_KY_SO` (bài) · 1 byte ảnh 2026-03 · manifest lệch 1 · xoá 1 dòng · ngày sang kỳ khác — mỗi cái ⇒ 1 bài đỏ. CLI: `--mong` ±1 ⇒ exit 1 · tên khối khuôn đổi ⇒ exit 2 · cột cấm ở bản thô ⇒ exit 2 *(đúng mong ⇒ exit 0)*.

## Cổng
`--duong-nen --cong 5437` *(một lần, một mình)*: `12 failed · 4255 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy **4283 ≥ 4283**; `tests/web` **3 = 3**, chạy 681 ≥ 681 ⇒ ĐẠT. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT · `quet_pii_repo` 0 · 15/15 bài DT12 xanh.

## Gửi orchestrator
`DT12-R1-01` *(NÊN SỬA, B2)*: quyết ảnh `{"chu"}` có chuẩn hoá về hình 2026-03 không *(khuyến nghị (a): bộ chuẩn hoá + bài đo giá trị `_chuan`)* — **trước H15**. GHI NHẬN `-02…06` ⇒ backlog; `-05` chủ quyết đóng băng lại 2026-03 trước H15.
