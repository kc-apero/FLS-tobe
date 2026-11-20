# KQ-237 — biên bản kiểm R2 *(CUỐI)* `BG-235` mục "Vòng sửa sau R1" *(ISP 3.1.2 · Step 35 · H11 + DT9b)*

| | |
|---|---|
| **Thuộc** | `KQ-236` · `BG-235` · `WO-233` · `BG-242` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2; ⛔ sửa mã)* · 2026-11-19 · `isp/H11` @ `d929b0d` · cây gộp thử `thu/H11` *(⛔ commit)* · cụm `5444` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H11.md` v0.3)* |

## Cây gộp thử *(`origin/claude/bold-galileo-zukpaf` @ `7cc8d04` + `isp/H11`)*
Xung đột **2 tệp**: `tools/dung_moi_truong_isp.sh` *(`MONG_PYTEST_TOAN_BO` 4101 ↔ 4202)* · `tests/test_dung_moi_truong_isp.py` *(bài ghim + câu lịch sử)*. Gộp tay: sàn = **thu thập thật** = **4.219** *(4.101 + DT9b 25 + H11 77 + vòng sửa 16)*; `hd2_cong.json` · `do_hd2.py` · `07_API_CONTRACT` tự gộp *(giữ cả hai)*.

## Cổng *(trên cây gộp thử)*
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5444` *(một lần, một mình)* | `KẾT: ĐẠT` · `12 failed · 4191 passed · 2 xfailed · 14 errors` = nền **28 = 28** *(thêm 0 · bớt 0)* · chạy **4219** *(mong ≥ 4219)* · skipped 0 · deselected 0 |
| `do_hd2.py --goi WP-C4a / C4b / C4c --dsn $PG_DSN_TEST` | cả ba `DAT` · C4a 0/196 · C4b 0/945 · C4c `khop/tong_o 19591/19894` · lệch FLS 0 · `hd2_cong.json` ⛔ đổi *(git sạch)* |
| pytest `luat_so_du_lieu_tong_hop` · `c4a/b/c` · `isp_gates_hd2` · `dung_moi_truong_isp` | **276 passed** *(kho test nạp IX.VEN 359 dòng + IX.PER 21/10/2024)* |
| `lint-imports` · `kiem_tai_lieu.py` · `soi_bang_tuyen.py` | 11 kept 0 broken · ĐẠT *(388 tệp · 2.736 bảng)* · KHỚP SQL **46** tuyến |

## Soát
1. **`H11-R1-01` ĐÓNG.** Bản sao `git archive` + bỏ bài ghim dict `test_LUAT_SO_khai_dung_FORMULA_BG242`: 5 cờ `LUAT_SO` R1 + bỏ nhánh `tt` + `doc_ven(so="GI")` ⇒ **7/7 CHẾT** *(mỗi cái ĐỎ ở bài dữ liệu tổng hợp hoặc bài C4c; trước R1: 7 sống)*.
2. **`H11-R1-02` ĐÓNG.** `doc_cong_hd2(hd2_cong.json)`: `HD2_WP_C4C` `dat=True` · *"19591/19894 ô đáp án khớp + 303 lệch có chủ đích"* · `lech_co_chu_dich=303` *(SC 251 · OMC 52, khớp `mong`)*; khối JSON `o_trong_dap_an` **8.611** *(1.650 · 2.575 · 4.386)* + nhãn `o_trong_dap_an_nhan`; `HD2_WP_C4` cha *"3/3 gói con đạt … Σ 21992/22295 + 303"*. Bài CG2 xanh. `hd2_cong.json` = đầu ra `do_hd2.py` *(chạy lại ⇒ git sạch)*. Phần nhãn còn thiếu ⇒ `H11-R2-01` *(GHI NHẬN)*.
3. **`H11-R1-04` ĐÓNG.** Đột biến `doc_ven(c, so="GI")` ở `chay_wp_c4c` ⇒ bài đường đọc kho CLI ĐỎ *(`1 failed`, 89 passed)*.
4. **Đột biến mới 5, SỐNG 1** *(cùng bộ bài, bỏ bài dict)*: bỏ tên `644` khỏi `LAC_OMC` · `khop += lech` · bỏ kiểm `lech != mong_lech` ở `doc_bao_cao` · `o_trong_dap_an ≡ 0` ⇒ **CHẾT 4/4**; bỏ `lech_nghi_loi` khỏi `mong_ten` ⇒ **SỐNG** *(mong nghi-lỗi = 0 mọi sổ ⇒ tương đương trên dữ liệu thật)* ⇒ `H11-R2-02`.

## Ghi nhận mới *(→ backlog; cùng `H11-R1-03` · `DT9B-R1-01/02` còn mở)*
`H11-R2-01` nhãn `/gates` ⛔ in 8.611 ô rỗng / 1.276 ô ≠ 0 *(Đ4)* · `H11-R2-02` thành phần nghi-lỗi của `mong_ten` ⛔ bài ép *(Đ5)*.
