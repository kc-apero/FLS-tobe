# KQ-247 — R1 kiểm `H7` *(CA.GL dòng HR + SO.CFA3, WP-C3c)* + DT6c

| | |
|---|---|
| **Trả** | `WO-245` / `BG-246` · `WO-249` / `BG-250` · **Phát bởi** `fls-test` R1 · 2026-11-19 · cụm PG 5435 · `isp/H7` @ `a6631c8` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H7.md` v0.1 |

## Kết luận
**ĐẠT có điều kiện — CHẶN = 0** · **2 NÊN SỬA** *(`H7-R1-01` · `-02`)* · **4 GHI NHẬN** *(`H7-R1-03/04/05` · `DT6C-R1-01`)*. Tái hiện `WP-C3c` đúng *(888 · 835 · 53 · ngoài tên 0)*. Mã ⛔ sửa.

## Số theo mức *(Đ4 — nhãn từng số)*
- **888 ô** = GL 240 *(12 kỳ × 10 nhãn V × {BA,BB}, tổng theo (kỳ,V))* + CFA3 648 *(54 mã × 12 tháng; 240 ô KPI loại)*. ⛔ so từng dòng: 408 có **9.410** dòng có ngày, **240** ô.
- 835 khớp = **619** ô `0 = 0` + **216** khớp ≠ 0. Ô có số thật **269** ⇒ khớp thật **216/269 = 80,3%**; lệch 53 *(47 cả hai ≠ 0 · 5 GL + 1 CFA3 đáp án 0 mà engine ≠ 0 · 1 CFA3 đáp án ≠ 0 mà engine 0)*.
- Phần ⛔ so *(đếm)*: **2.302** dòng `ky_suy` · **269** dòng 408 kỳ 2026-01 · **17** ô tháng CFA3 + **5** ô `-` ngoài kỳ · **240** ô KPI · **462** dòng đầu vào thiếu D. Có đếm, có `mong`.
- R1 so thêm ở mức nhóm `(kỳ,D,E,F,V)`: **4.323** nhóm = **7.952** dòng *(82,5% dòng vào engine)* ⇒ **0** lệch; phần dư giải thích đúng **80/80** ô GL lệch. Engine đúng ở mức dòng cho phần ghép được.

## Lệch theo lớp *(mong hai chiều)*
`dap_an_khac_nguon` *(53: GL 20 · CFA3 33; kỳ 02·04·06·08·09·10·12)* — Đ5 ĐỎ **chiều đếm** ✔ *(mong 7→6 ⇒ ĐỎ)*; chiều **giá trị** ✘ `H7-R1-01` *(3/3 đột biến trong ô đã lệch ⇒ ĐẠT)*. `chua_co_dau_vao` *(2026-01: 269 · 17 · 5)* · `ky_suy` *(2.302 · Σ F 6.763.528.503 · BA/BB rỗng 2.302)* · OGA 20 · `cdt_la` 659: có `mong`, bài ghim ✔. **2025-04**: lệch **đã khai** `mong` *(GL 2 · CFA3 3)* ⇒ ⛔ chặn; nguyên nhân "chia lại" ⛔ đúng — nguồn hơn **235.336.036 VND** PIT *(`H7-R1-03`)*.

## Vòng tròn · một nguồn · CG2
Đầu vào = `hr_ledger_2025` *(khoá cột 12, ⛔ V·BA·BB)*; vòng `feed` ⛔ đọc `gl`/`cfa3`. Đột biến đầu vào ⇒ đúng ô GL + lá + tổ tiên CFA3 đỏ ✔ *(B3 đối chứng ĐỎ)*. Engine H1/H4/H5 dùng lại, ⛔ chép *(trừ phép đổi ngày — `H7-R1-05`)*. CDT qua `cdt_cua`, lạ ⇒ `CdtLaHR` ✔. Khối `WP-C3c` đúng CG2; `/gates` `HD2_WP_C3C` + cha, 87 bài *(gates + C3c + gl_hr)* xanh.

## Đột biến · DT6c · cổng
- Đột biến mã **9/11** bị bắt *(M8 IX.ORG đọc ảnh · M10 chốt khối SỐNG)* + 3 đột biến dữ liệu lọt *(B1 · B4 · B5)* ⇒ **tổng 9/14**.
- **DT6c tái đo**: 33 hàng *(2/kỳ NIS 24 + 3/kỳ PIT 9; seed 7)*, khoá SA chỉ-đọc, cột `A·D·E·F·G·H·S·T·AG` ⛔ PII: `ky·D·E·F·G·hd·cdt1·le` **33/33** khớp ảnh. Bản thô `/tmp`, ⛔ commit. PII ảnh mới: 0 ✔; máy quét ⛔ có trên nhánh ⇒ chạy bản nhánh làm việc: tệp có sẵn ĐỎ 216/15, H7/DT6c 0 *(`DT6C-R1-01`)*.
- `--duong-nen --cong 5435` *(một mình)*: **ĐẠT** — tập đỏ 28 = 28 *(thêm 0 · bớt 0)* · chạy **4111** · web 3 = 3 *(675)*. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT *(381 tệp)* · `soi_bang_tuyen` 46/46.
