# KQ-248 — R2 CUỐI kiểm `H7` *(vòng sửa sau R1 `KQ-247`)* + DT6c

| | |
|---|---|
| **Trả** | `WO-245` / `BG-246` *(mục "Vòng sửa sau R1")* · **Phát bởi** `fls-test` R2 cuối · 2026-11-20 · cụm PG 5435 · `isp/H7` @ `0717aa7` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H7.md` v0.2 |
| **Cây gộp thử** | `thu/H7` = `origin/claude/bold-galileo-zukpaf` @ `8445324` + `--no-ff isp/H7` ⇒ `fcdc962`, **0 xung đột** *(⛔ commit cây này)* |

## Kết luận
**ĐẠT — CHẶN = 0 · NÊN SỬA = 0.** `H7-R1-01` · `-02` **đóng**. Thêm **2 GHI NHẬN** `H7-R2-01` · `-02` ⇒ backlog. Mã ⛔ sửa.

## Đóng `H7-R1-01` *(giá trị từng ô lệch)* — Đ5, bản sao `git archive`
- **3/3 đột biến R1 nay CHẾT**: B1 +1e9 VND PIT kỳ 10 ⇒ ĐỎ `ô lệch cfa3|202510|PIT` · B4 đáp án PIT kỳ 04 `BA` +0,5 ⇒ ĐỎ · B5 đáp án GAH kỳ 10 `BB` ×2 ⇒ ĐỎ. *(Tự dựng lại bằng `so_sanh_c3c`, ⛔ chép bài tác giả.)*
- **8 đột biến dữ liệu MỚI vào ô đã lệch**: chết **6/8** — đáp án GL kỳ 12 INT `BA` +1e-6 · đáp án GAH kỳ 10 `BB` −1e-7 · **hoán** `BB` GAH↔MC kỳ 10 *(cả hai ô lệch)* · +1.000 VND PIT kỳ 10 · hoán `E` hai dòng vào NIS kỳ 03 · xoá 1 dòng vào PIT kỳ 10. **Sống 2**: +1 VND · +0,01 VND ⇒ `atol` 1e-9 mUSD ≈ **25 VND** *(1 VND = 3,9e-11 mUSD)* — dưới đơn vị sổ ⇒ `H7-R2-02` GHI NHẬN.
- **7 đột biến MÃ** *(nhãn mẫu số 835 = khớp thật 216 + 619 · `mong`)*: `ATOL_LECH`→1e-1 · bỏ nhánh "ô mong lệch nay KHỚP" · `ATOL_NHOM`→1 · bỏ `_so_mong` `nhom.lech` · bỏ `_so_mong` `nhom.dong_408_khong_ghep` · `o_co_so = tong_o` · `khop_co_so = khop` ⇒ **7/7 ĐỎ**.

## Đóng `H7-R1-02` *(nhãn Đ4 + cổng nhóm)*
- Khối `WP-C3c`: `tong_o` **888** = `o_co_so` **269** + `o_0_0` **619** · `khop` 835 = `khop_co_so` **216** + 619 · `lech_co_chu_dich` **53** · 216 + 53 = 269 ✔. `/gates` chạy thật: *"835/888 ô đáp án khớp [khớp thật 216/269 ô có số · 619 ô 0 = 0] + 53 lệch có chủ đích"* `dat=true`. Đột biến tệp `hd2_cong.json` *(`khop_co_so` 215 · bỏ `o_0_0` · `o_co_so` 270 · kiểu `str` · `khop` 836)* ⇒ `dat=null`, ⛔ xanh.
- **Cổng nhóm `(kỳ,D,E,F,V)`**: 4.323 nhóm = 7.952 dòng, lệch 0 *(max 3,79e-17)*; `mong` hai chiều — thay từng số của 8 `mong` nhãn/nhóm ⇒ ĐỎ *(bài tác giả chạy lại: 114 xanh)*; đột biến mã bỏ `nhom.lech`/`dong_408_khong_ghep` ⇒ ĐỎ.
- **Tái đo 1.189 vs 1.458** *(Đ1·Đ3 — độc lập, đọc thẳng ảnh JSON)*: 408 không `ky_suy` = **9.410**: trong kỳ so **9.141** *(12 kỳ)* + kỳ 2026-01 **269** ⇒ 9.141 − 7.952 = **1.189** ✔; + 269 = **1.458** ✔ *(R1 đếm cả 269)*. Dòng vào: 10.105 − 462 thiếu D = 9.643 − 7.952 = **1.691** ✔. **Tác giả đúng.**
- `hd2_cong.json` **sinh bằng máy**: `do_hd2.py --goi WP-C3c --ghi` trên cây gộp ⇒ `git diff` = **0** byte *(số không đổi: 888 · 835 · 53 · ngoài tên 0)*.

## Ghim cứng `tests/api/test_isp_gates_hd2.py` *(3 số: 10 · 9 · 7)*
Bài **đọc tập cổng TỪ TỆP** *(`con` từ khoá tệp; `set(h) == mong`)*; 3 số chỉ ghim thêm. Thêm 1 gói con hợp lệ vào tệp ⇒ **9/79 ĐỎ có tên**, ⛔ xanh sai. Đã bump 4 lần *(H9·H10·H11·H7)* ⇒ **ý đồ Đ5**. Mức **GHI NHẬN** `H7-R2-01` *(⛔ NÊN SỬA)*: suy 3 số từ `MONG_THAT` cho gộp sau sửa 1 chỗ.

## Cổng trên cây gộp thử
- `quet_pii_repo.py`: **0** chỗ · 0 tệp *(1.087 tệp)* ✔ · `lint-imports` 11/0 ✔ · `kiem_tai_lieu` ĐẠT *(403 tệp)* ✔ · `soi_bang_tuyen` 46/46 ✔.
- `--duong-nen --cong 5435` *(một mình)*: **ĐẠT** — tập đỏ **28 = 28** *(thêm 0 · bớt 0 · XFAIL 2 = 2)* · chạy **4.261** *(sàn ≥ 4.261 ✔)* · web 3 = 3 *(675)*.
- DT6c: ảnh `hr_ledger_2025.json` PII = 0 *(máy quét sau gộp)*; `DT6C-R1-01` đóng *(máy quét có trên nhánh làm việc, 0 chỗ)*.

## Ghi nhận ⇒ backlog *(⛔ làm)*
`H7-R2-01` *(3 số cứng ở bài gates)* · `H7-R2-02` *(`ATOL_LECH` ≈ 25 VND, ghi vào `dung_sai_lech`)* · còn mở từ R1: `H7-R1-03` *(kỳ 04: nguồn hơn 235.336.036 VND PIT — hỏi chủ sheet)* · `-04` · `-05`.
