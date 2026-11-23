# KQ-159 — kiểm `BG-157` vòng sửa (`WO-156`, DT1b nhãn thật mốc 18/11) · R2 CUỐI

| | |
|---|---|
| **Thuộc** | `WO-156` · `BG-157` @ `fce2ace` (nhánh `isp/DT1BM`) · sau `KQ-158` |
| **Phát bởi** | `fls-test` (phiên cloud con, R2) · 2026-11-18 |
| **Kết luận** | **ĐẠT — ĐỦ ĐIỀU KIỆN GỘP** · 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN ⇒ backlog · `DT1BM-R1-01` đóng |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1BM.md` v0.2 |

## 1 · Tái lập độc lập *(mã tự viết, ⛔ gọi `phan_loai_ly_do.py`; SO Drive `1U-IQVO…` 10.606.726 B · L1 `UNFORMATTED_VALUE` cột `B` `D:G`)*
| Phép đo | Kết quả | Đếm gì |
|---|---|---|
| SO · L1 dòng dùng | **12.590 · 12.590** | hàng có ≥1 ô khoá *(mẫu số > 0)* |
| **Làm tròn 2 số lẻ `ROUND_HALF_UP`, hai phía** | khớp **12.590** · thiếu **0** | multiset khoá `(Số CT, tiền tệ, Nợ, Có, TK)` |
| **Không làm tròn** | khớp **12.571** · thiếu **19** | đúng tập `dong_sheet` cũ *(12 Số CT rỗng · 7 `ps_co`)* |
| Cặp có **Số CT rỗng** | **100 / 12.590** *(0,8 %)* | cả 100 khớp; 100/100 tiền ≠ 0; **0 cặp khác TK/tiền tệ** *(khoá đã gồm cả hai)*; **2 nhóm = 4 dòng** SO y hệt ⇒ ghép tuỳ ý *(đếm không đổi)* — `R2-01` |
| 19 dòng thiếu cũ | 12 Số CT rỗng · 7 Số CT có | tiền tệ: USD 8 · VND 7 · HKD 4 |
| **Làm tròn nuốt lệch thật?** | **KHÔNG** | 12.590 cặp: **0 cặp chênh ≥ 0,005** ở mọi tiền tệ *(VND 5.721 · USD 6.505 · SGD 228 · HKD 124 · rỗng 12)*; Δ tối đa USD `1e-9` · HKD `2e-11`; **chỉ 6 cặp VND** Δ ≈ `3,3e-3` — `R2-02` |
⇒ khớp BG-157 vòng sửa **từng số**. "0 thiếu" là KẾT QUẢ trên mẫu số 12.590 > 0 *(Đ3)*, ⛔ tập rỗng.

## 2 · Cổng `so_thieu = 0` ⛔ xanh trên tập rỗng — đột biến thật, bản sao `git archive`, **8/8 ĐỎ**, nền trả nguyên ĐẠT
| Phá | Kết |
|---|---|
| SO = 0 dòng *(CSV khoá chỉ có L1)* | ĐỎ `mẫu số = 0` *(Đ3)* |
| SO := bản sao L1 *(đọc nhầm nguồn ⇒ 0 thiếu giả)* | ĐỎ *(2 chỗ khác MONG)* |
| SO bớt 1 dòng cuối · đổi 1 ô tiền +1 | ĐỎ *(5 · 11 chỗ)* |
| ảnh mốc: lật 1 `khop` · bớt 1 dòng *(khai nhất quán)* | ĐỎ *(3 · 8 chỗ)* |
| `--khoa` không `--moc` | ĐỎ |
| mã: `DO_CHINH_XAC_TIEN_MOC = None` | ĐỎ *(`do_chinh_xac_tien ≠ 2` + 19 thiếu)* |
Bản thô → `phan_loai_ly_do.py --khoa … --moc …` trên dữ liệu thật: `KẾT: ĐẠT — 0 dòng sổ thiếu` *(mã 0)*.
**PII:** 16.149 token ≥5 chữ số từ SO — trong 9 tệp đổi từ R1: **0** thật; trùng = `dong_sheet` 10.000–12.621 + 9 hằng tổng hợp của bài/chú thích *(`1234.57`, `300.00`, ví dụ `4.36619E+15`)*.

## 3 · Cây gộp thử *(`/tmp/r2_dt1bm/gop` = `b851e6f` + `merge --no-ff --no-commit isp/DT1BM`; ⛔ commit/push; đã gỡ)*
- **2 xung đột** *(script · bài ghim)* ⇒ `--ours`. Sàn: `pytest --collect-only -q` = **3.365** *(ours 3343 < 3365)* ⇒ nâng `MONG_PYTEST_TOAN_BO` **3343 → 3365** + bài ghim `["3365"]` ở cây gộp — `R2-03`.
- `--duong-nen --cong 5447` **ĐẠT**: tập đỏ = nền **28 = 28** *(thêm 0 · bớt 0 · XFAIL 2 = 2)* · chạy **3365** (≥ 3365) · skipped 0 · deselected 0 · `tests/web` **3 = 3 · 667**. *(Lần 1 bị khung chạy nền cắt ở bước web, toàn bộ đã ĐẠT; chạy lại trọn một lần.)*
- `lint-imports` **11 kept 0 broken** · `kiem_tai_lieu.py` K1–K6 **OK** *(K3 xanh: lỗi `TIEN_DO.md:155` đã sửa ở nhánh làm việc)*.

## 4 · Việc kế
Gộp `isp/DT1BM` ⇒ nâng sàn 3343→3365 + bài ghim cùng commit gộp. Ghi nhận `R1-02…04` · `R2-01…03` ⇒ backlog. Bản thô `/tmp/r2_dt1bm/` **đã xoá**.
