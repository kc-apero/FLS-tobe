# KQ-187 — Kiểm R2 · ISP 3.1.2 · Step 26 · C12 (IX.PL) · vòng sửa sau `KQ-186`

| | |
|---|---|
| **Từ → Đến** | fls-test (R2, Sonnet 5.5) → orchestrator / BA |
| **Mã kiểm** | `isp/C12` @ `b17b221` · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C12.md` v0.2 |
| **Kết** | **ĐẠT** — 0 CHẶN · **1 NÊN SỬA** *(`C12-R2-01` PL5 — câu cho BA, ⛔ chặn push)* · 2 GHI NHẬN |

## 1 · Tái đo công thức ô *(độc lập, khoá SA chỉ-đọc, `FORMULA`+`UNFORMATTED_VALUE`, tab `…PLA3…ATL` `A7:AZ90`; bản thô ở `/tmp`)*
Mẫu số *(Đ3)*: **46 cột** có công thức dòng 81; **28** cột `GI ≠ 0`. Dịch dòng→mã bằng `atl_cay.json`.
- **6/7 khớp** — PL2 `GI+OMC` · PL3 `PL2+API+SC+LC` · PL4 `PL3+PS` · PL6 `PL4+MC+OTMC+DC+CSO` · PL7 `PL6+GAC+CDC+ITE` · PL8 `PL7+TAC`: chuỗi số hạng **trùng chữ**, công thức giống nhau **46/46** cột; `tinh_pl` trên số sheet nguyên dấu ⇒ lệch max **0** ở cả 6 *(28 cột ≠ 0)*. Dấu âm-cộng đúng.
- **PL5 — claim "sheet ⛔ có công thức" SAI.** Dòng 84: **33 ô công thức** *(21 `sumifs` gộp kỳ + 12 ô tháng `AG:AR`)*; `N:Y` rỗng **12/12**. 12 ô `AG:AR` = `sumifs('[2025][RPT] NOEM PL & COM'!x$18:x$26, A18:A26, "GAG") / tỷ giá / 10^6 * -1 + <PL4>` ⇒ COM lấy từ **tab ngoài, hàng `GAG` (Apero Group)**, ⛔ dòng 51 `COM Total`. Dấu `+` khớp; nguồn số khác: `PL5−(PL4+COM₅₁)` max **0,0593** *(12 cột)*; `tinh_pl` PL5 lệch max **1,2144** *(19/46 cột ≠ 0)*. PL6 qua PL4 ⇒ không lan.
- **Câu cho BA:** PL5 = COM cấp nhóm `GAG` (tab ngoài) hay `COM Total` (dòng 51 cây)? ⇒ `C12-R2-01`.

## 2 · Đột biến *(bản sao `git archive b17b221`)* — **12 giết · 0 sống**
Dấu: `GI + OMC`→`-` *(4 đỏ)* · PL4 `+PS`→`-` · PL3 `+API`→`-` · PL5 `+COM`→`-` · bỏ `LC` · bỏ `CSO` · bỏ `ITE` · PL6 qua PL5 · PL8 `TAC`→`CIT` · đảo dấu hai ngôi · đảo dấu đơn ngôi · `dat=True`. Bài ghim dấu thật cắn. `37 passed` gốc.

## 3 · Cây gộp thử *(`thu/C12` = `24380b8` + `isp/C12`; ⛔ commit)*
- **Xung đột:** 2 *(`tools/dung_moi_truong_isp.sh`, `tests/test_dung_moi_truong_isp.py` — sàn 3503 ↔ 3493)* ⇒ lấy bản nhánh làm việc, đặt sàn **3530** + bài ghim `:423` *(`C12-R2-02`)*.
- `--duong-nen --cong 5446` *(một lần, một mình)*: chạy **3530** · tập đỏ 29 = 28 + 1 *(duy nhất `test_S0_R3_02_…THU_THAP`, sàn 3493 < 3530 — hết đỏ khi đặt 3530, `60 passed`)*; còn lại **28 = 28** *(XFAIL 2)* · `tests/web` **3 = 3** · 675.
- `lint-imports` 11 kept 0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` 44/44.

## Việc kế
BA trả lời câu PL5 *(⛔ chặn push)*; orchestrator gộp C12 theo `R2-02` *(sàn 3530)*; DEV vá `C12-R1-03…06` trước H13. Vai KIỂM ⛔ sửa mã.
