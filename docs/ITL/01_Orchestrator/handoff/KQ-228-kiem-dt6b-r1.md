# KQ-228 — Kiểm R1 · ISP Step 23 · DT6b (Y2024 HR từ file gốc + gán kỳ 2.302 hàng)

| | |
|---|---|
| Phát bởi | fls-test (R1) · 2026-11-19 · `isp/DT6B` @ `08d64a6` |
| Gửi | orchestrator |
| Kết | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · **6 GHI NHẬN** *(→ backlog)* |

- **Tái đo bằng SA chỉ-đọc** *(file gốc `1YEyGxBY…`)*: **1.381/1.381** hàng, khoá 2 chiều thiếu 0 · thừa 0, **12.429** ô *(9 trường)* **0** lệch; số hàng/kỳ NIS 165·536·268 · PIT 200·212 và Σ PS Có 4 kỳ **= BG**; `H`: 6 ô dãy số ↔ 6 `R` ở ảnh.
- **Gán kỳ ĐÚNG định nghĩa**: 12/12 đoạn *(408 + 413)* kỳ = kỳ hàng liền trên *(liền kề `dong_sheet − 1`)*; 566·335·322·538·276·265 = 2.302, Σ PS Có 6.763.528.503, PS Nợ 0, `BA·BB` rỗng 2.302/2.302; hàng có ngày == ảnh cũ **9.410/9.410** · **10.785/10.785**. ⚠ Kỳ ấy là cận dưới: hàng liền DƯỚI luôn cách 2 kỳ ở 6/6 đoạn (`DT6B-R1-01`).
- **PII**: 3 ảnh 0 `@` · 0 tên · 0 ô chữ ≥ 6 chữ số ở MỌI cột; `R` hằng ⇒ không đảo được; mã/bài/BG 0 chuỗi TK. 6 ô `H` còn nằm ở **3 tệp BA có sẵn** *(5 chỗ, ⛔ do DT6b)* ⇒ `DT6B-R1-05` chuyển orchestrator.
- **Đột biến 9** trên `git archive`: **7 cắn** *(liền dưới · gan_ky +1 · bỏ `mUSD_rong@` · mất cờ · ΣF làm tròn · offset hàng · gỡ che `H`)*; **sống 2** *(`EPOCH` +1 ngày — tương đương trên dữ liệu thật; nhánh đoạn-đầu của `chuan_bi`)* ⇒ `-02`·`-03`.
- **Câu treo ĐÃ ĐO**: 2.302 hàng **không** nằm ở đuôi 407 *(cột `A·F·G·I·J·P` của 407 dài đúng 9.421, từ hàng 9431 rỗng; bộ giá trị: hàng có ngày 9.410/9.410 có ở 407, hàng gán kỳ 293/2.302 trùng ngẫu nhiên)* — `DT6B-R1-04`.
- **Ảnh khác**: `git diff --stat 213a40a HEAD -- tests/fixture` = 3 tệp ⇒ 407 · `cfa3` · `gl_406` · DT2…DT10 · DT8b 0 byte lệch.
- **`--duong-nen --cong 5436` MỘT lần: ĐẠT** — tập đỏ + XFAIL **28 = 28** *(12 đỏ + 14 lỗi + 2 XFAIL; thêm 0 · bớt 0)*, chạy **3792** (mong ≥ 3792), skipped 0; `lint-imports` 11 kept/0 broken · `kiem_tai_lieu` ĐẠT.
- Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT6B.md` v0.1.
