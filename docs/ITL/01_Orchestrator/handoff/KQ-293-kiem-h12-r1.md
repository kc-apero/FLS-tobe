# KQ-293 — R1 `WO-291` / `BG-292` *(ISP 3.1.2 · Step 42 · H12 — AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS)*

| | |
|---|---|
| **Kết quả** | **ĐẠT CÓ ĐIỀU KIỆN** — **0 CHẶN · 1 NÊN SỬA · 5 GHI NHẬN** ⇒ vòng sửa `H12-R1-01` trước R2 |
| **Phát bởi** | `fls-test` *(R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/H12` `8060878` · cụm 5447 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H12.md` *(v0.1)* |

## Trọng tâm số 1 — phân loại lệch *(Đ5)*
- `lech_co_chu_dich` **5.831** *(đếm ô lệch trong 11.763 ô có số)* = **224** ô chỉnh tay/NB by LE *(AS-IS thật)* + **675** bản dán cũ 2024 *(AS-IS thật, lan từ H8)* + **4.932** ô 2025 gán nhãn *"AS-IS bật phân bổ"* **bằng quy tắc khối × năm**.
- **Bật cờ đúng luật AS-IS 2025** *(kho test, `BangALR` trong bộ nhớ; By GI từ 202501→202502 vì `GI 202501` thiếu driver)*: khớp thật **5.932 → 6.516**/11.764 — chỉ **583**/4.932 ô là `cho_bat_co` thật; **4.349** ô còn lệch vì lá khác nguồn. By NOEM `HCC` `REC` `BON` `OGA`: lá lệch **518 → 0** *(bằng chứng DƯƠNG cho D2 ở 4/5 mã NOEM)*.
- Nguyên nhân còn lại *(thay lá khối CDT 2025 bằng ATL ⇒ cây 2025 khớp **5.932/5.932**, lệch dẫn xuất 100 % do lá)*: By GI driver `PE` ≠ AS-IS `GI khối MID3 / GI GROUP` *(D3 ⛔ khớp ATL; đổi sang tỉ lệ ATL ⇒ lá By GI lệch 0 ⇒ cấu trúc engine đúng)* · `GI` 130 · `OMC` 129 · `PS` 103 · `SC` 113 lá *(⛔ có trong errata `BG-292`)* · `OFR` 114.
- ⇒ `H12-R1-01` **NÊN SỬA**: cổng ĐẠT là thật *(0 lệch FLS, sha ghim cả giá trị engine)* nhưng **⛔ chứng minh parity ATL** — tách lớp có tên, `mong` từng lớp.

## Các trọng tâm khác
1. **H12-B1** 50.616/50.616 ô `==` *(12 × 74 × 57, ⛔ dung sai, Đ3 lưới ≠ 0)* — ĐẠT.
2. **H12-B2** `DRIVER_THIEU` 6/6 ô, ⛔ hoá 0; Σ chia = tiền *(⚠ tautology một phần — `-06`)* — ĐẠT.
3. **Vòng tròn**: đầu vào = `pla_yhqm` H8 trên ảnh DT7b; `atl.json` ở `fls/` 0 tệp, `tools/` chỉ ở bước so — ⛔ vòng tròn.
4. **Cờ** đọc từ kho IX.ALR *(đột biến cờ hằng · đọc ảnh ⇒ ĐỎ)*. **Driver đọc thẳng ảnh** `ix_drv.json` *(C10 chưa có: `driver_cua` 0 tệp)* ⇒ `-04`: chuyển sang `driver_cua` sau `WO-295`.
5. Khối `WP-C5a` theo CG2: `--ghi` ⇒ **0 byte đổi**; `/gates` `HD2_WP_C5A` true + cha `HD2_WP_C5` true *(bài gates xanh)*.
6. Sàn **4556** = thu thập thật; bài C11 xanh cả hai thứ tự, `TU_KY_ALR = 202501` ⛔ giẫm kho.

## Cổng · đột biến
- **12/12** đột biến bị cắn *(baseline xanh trước, kho mới mỗi lần)*; cây sạch.
- `--duong-nen --cong 5447` *(một mình)*: **ĐẠT** — tập đỏ + XFAIL **28 = 28**, chạy **4556** *(mong ≥ 4556)*; web **3 = 3**, 681. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` KHỚP 48.

## GHI NHẬN ⇒ backlog
`-02` D3 By GI ⇒ PE ⛔ khớp công thức ATL *(BA/owner)* · `-03` errata thiếu OMC/PS/SC khối CDT + OFR · `-04` driver ảnh → kho sau C10 · `-05` bài nhánh ĐỎ `if co_alr == 0` · `-06` Σ = tiền tautology.

Việc kế: giao vòng sửa `H12-R1-01` cho `fls-dev` *(⛔ đụng engine — chỉ `do_hd2_c5a*` + `hd2_cong.json` + bài)*; R2 cuối `KQ-294` sau vòng sửa.
