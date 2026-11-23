# KQ-224 — Kiểm R2b NHẸ · ISP 3.1.2 · Step 26 · C12 (IX.PL) · vòng sửa PL5 = GAG

| | |
|---|---|
| **Từ → Đến** | fls-test (R2b, Sonnet 5.5) → orchestrator |
| **Mã kiểm** | `isp/C12` @ `ad4c4e4` · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C12.md` v0.3 |
| **Kết** | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN *(`C12-R2b-01…03`; `-01` đóng `C12-R2-01`)* |

## 1 · Tái đo nguồn *(khoá SA chỉ-đọc, 19/11; bản thô ở `/tmp`, ⛔ commit; chỉ hàng `GAG` + tiêu đề)*
- `FORMULA` `AG84:AR84`: **12/12** khớp mẫu `sumifs(<F…Q>$18:$26, $A$18:$A$26, "GAG") / SUMIFS(9.2.Exchange Rate) / 10^6 * -1 + <AG…AR>83`, cột `F…Q` ↔ `AG…AR` thẳng hàng.
- Hàng GAG: `A18:B18` = `GAG` · `GAG I Apero Group` *(chữ `GAG` ở `A18:A26`: 1/9 hàng)*; `F18:Q18` = `noem_com_gag.json` **12/12**, 12/12 ≠ 0 *(Đ3: mẫu số 12)*; tiêu đề `2025`×12 · `1…12`.
- Tỷ giá USD `9.2.Exchange Rate` 202501…202512 = `ix_fx.json` **12/12** *(IX.FX đúng tháng, ⛔ hằng)*. Dấu `*-1` ⇒ `PL4 − COM_GAG` đúng; bài `R2_01`: 84/84 phép PL × tháng khớp.
- Giá trị PL5 sheet 12 tháng: 0,34…1,38 *(≠ 0)*; tháng 2024 rỗng ⇒ `PL_THIEU_GIA_TRI` *(bài ghim, ⛔ lấp 0)*.

## 2 · Đột biến *(tệp làm việc, trả nguyên sau mỗi lần)* — **5 giết · 0 sống**
`-`→`+` ⇒ đỏ · bỏ `COM_GAG` ⇒ đỏ · hằng `- 0` ⇒ đỏ · lệch tháng *(đổi chỗ T1↔T2 của ảnh)* ⇒ đỏ `R2_01_…khop_o_AG_AR` · `DAU_VAO_NGOAI` rỗng ⇒ đỏ. Thiếu `COM_GAG` ⇒ `LoiPL` tên `PL_THIEU_GIA_TRI` *(bài `R2_01_PL5_la_PL4_tru…`)*.

## 3 · Cây gộp thử *(`thu/C12` = `origin/claude/bold-galileo-zukpaf` `9bfe992` + `isp/C12`; ⛔ commit)*
- **Xung đột 2** *(`tools/dung_moi_truong_isp.sh` sàn 3754↔3742 · bài ghim)* ⇒ giữ bản nhánh làm việc, sàn = thu thập thật **3797** *(3754 + 43)*.
- `--duong-nen --cong 5446` *(một lần, một mình)*: chạy **3797** · tập đỏ **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · 12 failed + 14 errors = đường nền.
- `lint-imports` 11 kept 0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` 45/45.

## 4 · Ghi nhận
`R2b-02`: phép đổi VND→USD của `COM_GAG` chỉ sống trong bài *(`fls/` 1 tệp, `tools/` 1, `docs/` 1)*; khi nối đầu vào phải dùng `IX.FX` đúng tháng. `R2b-03`: sàn gộp 3797 cho orchestrator.

## Việc kế
Orchestrator gộp `isp/C12` *(sàn 3797)*; DEV vá `C12-R1-03…06` trước H13. Vai KIỂM ⛔ sửa mã.
