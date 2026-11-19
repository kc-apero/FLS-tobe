# KQ-231 — Kiểm R1 · ISP 3.1.2 · WO-226 *(alias nhãn HD `ITE | ITE Interest` → nút `ITE`)*

| | |
|---|---|
| **Từ → Đến** | fls-test (R1, Sonnet 5.5) → orchestrator |
| **Mã kiểm** | `isp/ITE` @ `851537d` *(nền `cd7a836`)* · `BG-230` · sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_ITE.md` v0.1 |
| **Kết** | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **1 NÊN SỬA** *(`ITE-R1-01`)* · 1 GHI NHẬN *(`ITE-R1-02`)* |

## 1 · Trọng tâm
1. **`khop = khop_dap_an + lệch có chủ đích` có giấu lệch khỏi `/gates`? — CÓ, ở lời `da_do` *(NÊN SỬA)*.** Gọi thật `doc_cong_hd2(hd2_cong.json)`: `HD2_WP_C3A` ⇒ `205175/205175 ô đáp án khớp` *(thật 205.140 + 35 lệch)* · `C3B` `11585/11585` *(11.543 + 42)* · cha `C3` `Σ 216760/216760` *(216.683 + 77)* — `dat=True`, `ly_do` rỗng. `Cong` ⛔ có trường nào cho lệch có chủ đích; grep `lech_co_chu_dich`/`khop_dap_an` ở `fls/` = **0**, `tests/api/` = **0**. Phán quyết `true` đúng theo quyết A; **lời in** sai 35/42/77 ô. Khuyến nghị: **THÊM** `Cong.lech_co_chu_dich` + `da_do` nói hai số, ⛔ cộng vào tử số; bài ghim ở `test_isp_gates_hd2.py`.
2. **Alias là cấu hình, ⛔ `if` theo nhãn — ĐẠT.** `cfa.py` có `ITE Interest` = **0** lần; bảng ở `hd.py:387`; so khớp `strip()` hai đầu; đích ⛔ có trong cây ⇒ `ValueError`. Đột biến: gỡ alias · bỏ `strip` · alias nuốt mọi nhãn · thêm `Server Cost→ITE` ⇒ ĐỎ. Nhãn `Server Cost 7 · GAC - Other 1 · rỗng 1` = **9** ⛔ bị nuốt. ITE là lá ⛔ cha ⇒ ⛔ ô tổ tiên đổi. *(Ghi nhận `-02`: chỉ dụng cụ đo truyền `alias`; mặc định `None`.)*
3. **Σ tái tính độc lập — KHỚP.** Từ `gl_cf_dau_vao.json` + `ix_fx`, ⛔ qua engine: **153** dòng *(152 + 1 cách cuối)*; VND Nợ 8.466.662 · USD 16.137,66 / 4.469,33 · SGD 25,15 / 50 *(đúng số WO)*; Σ = **0,011973111599 mUSD** = khối khai, 12/12 chữ số; 26 ngày `2025-02-24 → 2026-10-31`. C3b 0,047892446397 = 4 × C3a.
4. **`mong` hai chiều — ĐẠT.** Đổi `so_o` ±1 · ngày · Σ · mã · vắng ⇒ ĐỎ *(bài `test_D5_*`)*; một ô SGO1/GI lệch 1e-12 ⇒ vào `lech` ngoài tên, ĐỎ, `lech_ite` vẫn 35; đột biến "mọi ô lệch coi là ITE" ⇒ ĐỎ.
5. **Sinh lại bằng máy — ĐẠT.** `do_hd2.py --goi WP-C3a/C3b --ghi` *(IX.PER 21/10 nạp vào `fls_test`)* ⇒ diff 2 dòng, đều là nhãn nguồn IX.PER do R1 nạp; mọi số y nguyên.

## 2 · Đột biến — **12/12 ĐỎ** *(bản sao `git archive 851537d`, `-x`)*
gỡ alias · bỏ `strip` · alias nuốt mọi nhãn · `khop` ⛔ cộng lệch ITE · tắt `_so_mong_ite` · mọi ô coi là ITE · `so_o` 35→34 · đích `ITE→GI` · alias thừa `Server Cost→ITE` · sửa tay JSON `so_o` · `hd_ngoai_cay` 7→8 · `_o_chiu_alias` rỗng. *(3 ca cấu hình chết ở bài ghim chữ `ALIAS_NHAN_HD == {…}`.)*

## 3 · Cổng
Bốn bộ liên quan **116 passed** *(`test_do_hd2_ite_alias` 30 + c3a + c3b + `test_isp_gates_hd2`)*. **`--duong-nen --cong 5434` MỘT lần, một mình ⇒ ĐẠT**: toàn bộ 12 failed · 3866 passed · 2 xfailed · 14 errors = 28 = 28 node id *(thêm 0 · bớt 0)*, chạy 3894 ≥ 3894; web 3 = 3, chạy 675 ≥ 675. `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` 46/46.

## 4 · Giao
`DEV` sửa `ITE-R1-01` *(trước khi gộp hoặc phiếu CG2 riêng)*; `ITE-R1-02` ⇒ backlog *(khi dựng báo cáo CFA1 thật)*.
