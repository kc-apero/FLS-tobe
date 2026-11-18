# BG-185 — Bàn giao WO-184 · ISP 3.1.2 · Step 26 · C12 (IX.PL)

| | |
|---|---|
| **Từ → Đến** | fls-dev (làn BE-CF, Sonnet 5.5) → fls-test (R1) |
| **Nhánh** | `isp/C12` ⇒ `claude/bold-galileo-zukpaf-isp/C12` · commit ① mã+bài `11effec` |
| **Kết** | mã xong; 3 bài AC xanh; `--duong-nen` ĐẠT (tập đỏ 28 = 28) |

## Làm gì
- `fls/cau_hinh/dong_pl.py`: bộ phân tích `+ − ( )` + dấu đơn ngôi (token→cây→cộng/trừ, ⛔ `eval`/`exec`/`compile` — bài quét AST). `DINH_NGHIA` (PL2…PL8, bản ATL), `tinh_pl`, `check_pl`, `kiem_dinh_nghia`, `CHENH_VOI_MM`. Lỗi có TÊN, gom hết: `PL_CU_PHAP · PL_MA_LA · PL_CHU_TRINH · PL_THIEU_GIA_TRI` (thiếu giá trị ⇒ lỗi, ⛔ ngầm 0).
- `fls/repo/cau_hinh_repo.py`: `nap_ix_pl`/`doc_pl` + `_kiem_pl` trong `_kiem_noi_dung` (kiểm TRƯỚC khi ghi, luật `C5-R1-04`). Dùng bảng `IX.PL` đã có trong `BANG_HOP_LE`, di trú `0027` có sẵn ⇒ ⛔ di trú mới.
- Q8: `MONG_PYTEST_TOAN_BO` 3466 → **3500** (+ bài ghim, cùng commit).

## AC — đỏ trước
Lệnh đỏ: `pytest tests/cau_hinh/test_dong_pl.py tests/cau_hinh/test_dong_pl_pg.py` → exit 2, `ImportError: cannot import name 'dong_pl'` (thiếu module = thiếu hành vi, ⛔ lỗi cú pháp/setup). Sau mã: 34 xanh.

| ID | Bài | Đỏ trước | Nay |
|---|---|---|---|
| C12-B1 | `test_C12_B1_*` (7 dòng tay tính 900/840/800/750/700/640/600 · cú pháp · định nghĩa ∈ cây 74 nút · CHÊNH) | ĐỎ | xanh |
| C12-B2 | `test_C12_B2_*` (18 mẫu độc hại `__import__`… · mã lạ · chu trình · thiếu giá trị · AST) | ĐỎ | xanh |
| C12-B3 | `test_C12_B3_*` (cân ⇒ cả hai đúng · NB lệch 1 ⇒ phép NB · GAH lệch 1 ⇒ phép 2, chênh −1 · thiếu giá trị) | ĐỎ | xanh |
| kho | `test_dong_pl_pg.py` (3: nạp/đọc 7 dòng · biểu thức hỏng ⇒ không thêm phiên bản · mã lạ) | ĐỎ | xanh |

Đ5 — phá thử 3 nhánh, bài ĐỎ rồi trả nguyên: bỏ kiểm mã∈cây (1 đỏ) · `dat=True` (2 đỏ) · bỏ dò chu trình (1 đỏ). Đ3: mọi phép có mẫu số ≠ 0 (7 dòng · 2 phép · vế 125 ≠ 0).

## Cổng cuối
- `--duong-nen --cong 5446`: chạy 3500 bài (mong ≥ 3500) · 12 failed + 14 errors + 2 xfail ⇒ **tập đỏ 28 = 28 node id** (thêm 0 · bớt 0) ⇒ ĐẠT.
- `lint-imports`: 11 kept, 0 broken · `soi_bang_tuyen`: 44/44 ĐẠT · `kiem_tai_lieu`: ĐẠT (không tuyến mới ⇒ ⛔ chạm `07_API_CONTRACT.md`).

## Cho R1 / owner (giới hạn — ⛔ tự hoà giải)
1. **Nguồn `DINH_NGHIA`**: ảnh ATL chỉ giữ LỜI MÔ TẢ chữ (`ten`); công thức mã lấy từ hàng "606" của ISP/AP (PL2 = GI−OMC · PL3 = PL2−API−SC−LC · …). **Chưa đối chiếu với công thức ô ATL gốc** — cần owner/BA xác nhận.
2. **Chênh ATL ↔ MM (1 mục)**: `PL3` có `LC` ở ATL; mô tả MM ("server, API.. + Tools") ⛔ nêu License. Liệt kê ở `CHENH_VOI_MM`.
3. Chưa nối engine H13 / tuyến; `nap_ix_pl` chưa được gọi từ đâu ngoài bài (đúng phạm vi mục 7).

## Vòng sửa sau R1 (KQ-186)

Orchestrator chốt **A: theo NGUỒN AS-IS**. Đo lại công thức ô bằng SA chỉ-đọc *(sheet `[COPY] Report I General Ledger · P&L Report` · tab `Report I PLA3 Y H Q M | PM + HR | ATL` · `A7:AZ90` · `FORMULA` + `UNFORMATTED_VALUE`; bản thô ở `/tmp`, ⛔ commit; cột G, giống nhau ở 46/46 cột có công thức)*.

| Dòng sheet | Công thức gốc *(cột G)* | `DINH_NGHIA` mã HD *(sau sửa)* | Trước |
|---|---|---|---|
| 81 PL2 | `=G8+G12` | `GI + OMC` | `GI - OMC` |
| 82 PL3 | `=G81+G18+G19+G20` | `PL2 + API + SC + LC` | `PL2 - …` |
| 83 PL4 | `=G82+G17` | `PL3 + PS` | `PL3 - PS` |
| 84 PL5 | ⛔ **không có** *(N:Y rỗng; G84 = `sumifs` vùng rỗng)* | `PL4 + COM` *(lời mô tả sheet "PL4 − COM" dưới dấu âm)* | `PL4 - COM` |
| 85 PL6 | `=G83+G13+G14+G21+G22` | `PL4 + MC + OTMC + DC + CSO` *(⛔ qua PL5)* | `PL5 - …` |
| 86 PL7 | `=G85+G23+G34+G43` | `PL6 + GAC + CDC + ITE` | `PL6 - …` |
| 87 PL8 | `=G86+G57` | `PL7 + TAC` *(dòng 57, ⛔ `CIT` dòng 58)* | `PL7 - CIT` |

- **R1-01:** khớp công thức ô **6/6** dòng có công thức *(PL2–4, 6–8)*; PL5 ⛔ có nguồn công thức ⇒ ghim lời mô tả, nêu rõ trong chú thích. Bài `test_C12_R1_01_*` ghim chuỗi số hạng từng dòng = ô gốc *(dịch dòng→mã bằng `atl_cay.json`)*.
- **R1-02 dấu:** HD mang dấu sheet — chi phí ÂM, CỘNG. Đo: `tinh_pl` trên 46 cột sheet nguyên dấu *(28 cột ≠ 0)* ⇒ lệch max PL2 · PL3 · PL4 · PL6 · PL7 · PL8 = **0**; PL5 = 1,214 *(sheet PL5 ≡ 0, ⛔ công thức)*. Bài `test_C12_R1_02_*` ghim dấu *(⛔ `-` trong 6 dòng; chi phí dương ⇒ PL2 > GI)*.
- Bài CHECK `C12-B3` đổi sang bộ số riêng `HD_CHECK` *(CHECK ngoài phạm vi)*; CHECK `==` tuyệt đối *(`-06`)* vẫn mở.
- `-03…-06`: GHI NHẬN ⇒ backlog, ⛔ làm.
- Q8: `MONG_PYTEST_TOAN_BO` **3500 → 3503** *(+3 bài `test_dong_pl.py`)* + bài ghim `test_dung_moi_truong_isp.py:423`, cùng commit.
