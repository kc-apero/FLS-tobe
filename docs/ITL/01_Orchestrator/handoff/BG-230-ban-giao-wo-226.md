# BG-230 — Bàn giao WO-226 · alias nhãn HD `ITE | ITE Interest` → nút `ITE`

| | |
|---|---|
| Phát bởi | fls-dev (phiên cloud) · 2026-11-19 · nhánh `isp/ITE` (nền `cd7a836`) |
| Gửi | fls-test (R1) |

## Đã làm
- **Alias = cấu hình khai trong IX.HD** (`fls/cau_hinh/hd.py: ALIAS_NHAN_HD = {"ITE | ITE Interest": "ITE"}`), ⛔ kho C5 / ⛔ di trú: alias là thuộc tính của cây ATL đóng băng, một dòng cấu hình không đáng một di trú + quy trình ghi.
- Engine `fls/bao_cao/cfa.py: cfa1_daily(..., alias=)`: so khớp sau `strip()` hai đầu; đích ⛔ có trong cây ⇒ `ValueError`; dòng vào nhờ alias ghi `dong_alias`. ⛔ `if` theo nhãn trong engine (bài đếm `ITE Interest` = 0 ở `cfa.py`).
- `tools/do_hd2.py`: C3a + C3b truyền alias; tách ô lệch **có chủ đích** (ô alias làm đổi giá trị = lưới có alias ≠ không alias, VÀ ≠ đáp án) khỏi lệch ngoài tên; khai `MONG_LECH_ITE_C3A/C3B` + `MONG_C3A_HD_ALIAS`; khác ⇒ ĐỎ hai chiều.

## Số đo (Đ4: nhãn cạnh số)
- `hd_ngoai_cay` (DÒNG): 162 → **9** (Server Cost 7 · GAC - Other 1 · rỗng 1); 153 dòng vào `ITE` (152 + 1 cách cuối).
- C3a: **35 ô** lệch có chủ đích (GROUP 26 · SGO2 8 · BGO2 1) · 26 ngày 2025-02-24 → 2026-10-31 · Σ GROUP **0,011973 mUSD** (đúng ≈ 0,01197 của WO) · Σ mọi khối 0,023568.
- C3b: **42 ô** (GROUP 24 · SGO2 14 · BGO2 4) · 24 kỳ `2025` → `2026Q4` · Σ GROUP 0,047892 = 4 × C3a (mỗi dòng rơi 4 cấp kỳ Y·H·Q·M chồng nhau — Σ ô, ⛔ tiền ròng).
- Ô khác: khớp 100 % (`lech_ngoai_ten` = 0): C3a 205.175/205.175 · C3b 11.585/11.585.

## Hợp đồng CG2 (`tong_o`/`khop`) — ⛔ giấu lệch
`khop` = `khop_dap_an` (205.140 · 11.543) + `lech_co_chu_dich_ite.so_o` (35 · 42) = `tong_o` ⇒ `/gates` HD2 vẫn `true`. Lệch KHÔNG bị giấu: khối khai `khop_dap_an`, `lech_co_chu_dich_ite`, `mong_lech_co_chu_dich_ite`, `khop_ghi_chu`; mong sai một khoá ⇒ ĐỎ. Lý do chọn: CG2 đòi `khop == tong_o` (khác ⇒ `null`); cách này giữ hợp đồng, bằng chứng nằm cạnh trong cùng khối. `lat_bo` vẫn vắng như BG-209.

## Chứng ĐỎ
Bỏ `strip()` ⇒ 5 bài ĐỎ (AC1/AC2); gộp ô ITE vào `lech` ⇒ 5 bài ĐỎ (AC3/Đ5). Bài mong sai (so_o ±1, ngày, Σ, mã, vắng) ⇒ ĐỎ; gỡ alias ⇒ ĐỎ cả hai gói (162 dòng quay lại).
Bài: `tests/oracle/test_do_hd2_ite_alias.py` (30 bài) · `test_do_hd2_c3a.py` 162 → 9. `test_isp_gates_hd2.py` + hai bài C3 xanh (116 bài).

## Sinh lại
`do_hd2.py --goi WP-C3a --ghi` + `--goi WP-C3b --ghi` với `PG_DSN=$PG_DSN_TEST` (IX.PER nạp vào `fls_test`, ngày đầu 2024-10-21; ⛔ sửa tay; khối WP-C2/C4 nguyên). Ghi kho thật: KHÔNG.

## Q8
`MONG_PYTEST_TOAN_BO` 3864 → **3894** (= thu thập, +30) · web 675 — cùng commit bài ghim `test_S0_R3_02_…`.

## Cổng
`--duong-nen --cong 5434`: lần 1 bị dừng ở phần web do hết hạn nền 30 phút (⛔ ĐỎ; phần toàn bộ đã ĐẠT 28 = 28), chạy lại MỘT lần ⇒ **ĐẠT**: toàn bộ 12 failed · 3866 passed · 2 xfailed · 14 errors = 28 = 28 node id (thêm 0 · bớt 0), chạy 3894; web 3 = 3, chạy 675. `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` khớp 46/46.
