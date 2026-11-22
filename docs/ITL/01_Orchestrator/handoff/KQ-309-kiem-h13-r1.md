# KQ-309 — R1 `WO-307` / `BG-308` *(ISP 3.1.2 · Step 44 · H13 — SO.PLA3-ATL + IX.PL CHECK, WP-C5b)*

| | |
|---|---|
| **Kết quả** | **ĐẠT CÓ SỬA — 0 CHẶN · 1 NÊN SỬA · 2 GHI NHẬN** |
| **Phát phiếu** | `fls-test` *(R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/H13` `ca5f7ae` · cụm 5447 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H13.md` *(v0.1)* |

## Kết luận từng trọng tâm
1. **Lan nhãn**: **32/32** ô đúng *(tự dựng bằng tay, ⛔ qua `_thua_ke`)*; toàn **923/923** nhãn ⊂ lớp lá + hồi phục; bỏ `lech_D3` khỏi 1 lá ⇒ ô đổi nhãn đúng *(2/2; ca còn lá D3 khác giữ nhãn)*; giấu lớp ⇒ `lech_FLS` ĐỎ; `+1e-3` vào lá khớp ⇒ ĐỎ đúng 7 ô. Lệch FLS trốn trong lớp: **0**.
2. **PL5 252**: ⛔ đồng nhất. 7 ô GROUP Y/H/Q 2025 **đo được mà bị bỏ** *(cộng tháng: 4 khớp + 3 lệch đúng 0,5 = OMC M02)*; 14 ô GROUP 2024/2026 là lệch định nghĩa AS-IS *(ATL PL5 = 0 vs PL4 ≠ 0)*; 231 ô CDT: chỉ 75 cần COM CDT1, 156 có PL5 = PL4. ⇒ `-02`.
3. **CHECK**: `dat_co_so = 0` đúng dữ liệu ở ② *(214/214 đỏ, chênh nhỏ nhất 2,6e-5)*; kỳ tổng hợp cân ⇒ ② `dat_co_so` ✔. **① không thể ra `dat_co_so`** *(mã duy nhất `NB`)*: 537 `dat_0_0` = 481 rỗng + **56** có dữ liệu cân ⇒ `-01` NÊN SỬA.
4. **Vòng tròn**: `dong_pl_atl` ⛔ có tham số ATL; xoá 4.960 ô PL của ATL ⇒ engine y nguyên, cổng ĐỎ `tong_o=0`. IX.PL hằng ↔ kho: `pl`·`lech`·`hd2_cong` y hệt. Dùng lại `dong_pl.py`, ⛔ chép.
5. **WP-C5b**: `--ghi` ⇒ **0 byte đổi**; `/gates` 13 cổng 0 null, `HD2_WP_C5B` đạt, cha C5 `2/2` *(79 bài xanh)*.
6. **Sàn 4650** = thu thập thật *(4650 collected)*; đột biến 4649 ⇒ ĐỎ.

## Đột biến · cổng
- Đột biến **14/15** cắn *(sống: M3 "tập nhỏ nhất" ⇒ `-03`)*; baseline 168 bài xanh.
- `--duong-nen --cong 5447` **ĐẠT**: tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)* · chạy **4650** · web **3 = 3**/690 · `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT *(460 tệp · 2.898 bảng)* · `soi_bang_tuyen` KHỚP 48 tuyến.

## Việc kế
Dev sửa `-01` *(① đếm `dat_co_so` khi `NB=0` có dữ liệu, `mong` ① = 56, sửa câu BG)*; `-02` `-03` ⇒ backlog. Sau đó R2 cuối `KQ-310`.
