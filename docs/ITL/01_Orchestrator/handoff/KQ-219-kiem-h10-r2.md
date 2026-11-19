# KQ-219 — R2 CUỐI · `H10` (Step 28 · AL.PLT 5 vendor đặc biệt · cổng WP-C4b)

| | |
|---|---|
| **Thuộc** | `WO-216` · `BG-217` *(mục «Vòng sửa sau R1»)* · `KQ-218` · `isp/H10` @ `cfee7e1` · cụm `5444` |
| **Phát bởi** | `fls-test` R2 · 2026-11-19 |
| **Kết luận** | **TRƯỢT TÍCH HỢP** *(vòng sửa R1 ĐẠT)* — **1 CHẶN** `H10-R2-01` *(khối `WP-C4b` ⛔ có `tong_o`/`khop` ⇒ CG2 ĐỎ trên cây gộp)* · 0 NÊN SỬA · 1 GHI NHẬN `-R2-02` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H10.md` v0.2 |

## Số đo *(Đ4 — mỗi số một nhãn)*
| Nhãn | R2 đo |
|---|---|
| Gộp thử `thu/H10` = `9bfe992` + `isp/H10` | xung đột **2 tệp** *(`dung_moi_truong_isp.sh` · `test_dung_moi_truong_isp.py`)* chỉ ở hằng sàn ⇒ giữ bản nhánh làm việc; `do_hd2.py` · `hd2_cong.json` tự gộp *(4 khối `C3a C3b C4a C4b`)*. Sàn = thu thập cây gộp **3801** *(web 675)* = 3754 + 47 |
| (1) `H10-R1-01` đóng | MỘT hàm: `tong_thang_as_is` `phan_bo.py:96` + `pm_tong_thang` `:111`; `chia_nen_tang` `:150,173` và `chia_theo_cach_tinh` `:389,406` cùng gọi. Ca tổng hợp R1 *(`O=100/20/0`)*: cả hai ra `40/20` *(bài `test_H10_R1_01…` xanh)* |
| (1) hai bài H9 đổi | **CÓ căn cứ**: kỳ vọng mới `S10/O10` = AS-IS `P×S10/O10` *(BG-217)*; tính tay `S10=7−4−4+9=8=O10` ⇒ RATE `7/8 · 9/8 · −4/8` — so **bằng nhau tuyệt đối** `Decimal`, ⛔ nới dung sai; lỗi đổi sang `tổng tháng Σ O = 0` *(đúng mẫu số AS-IS)*. ⛔ phải nới bài cho xanh |
| (2) đột biến *(bản sao `git archive isp/H10`; 135 bài `tests/bao_cao` + C4b: nền 135 xanh)* | `M7` kiểu VD62 ⇒ **1 đỏ** · `M9` donor `VD341→VD444` ⇒ **2 đỏ** · `M16` `p>0→p!=0` ⇒ **2 đỏ** *(sed đổi cả dòng 380 lẫn 402)* — cả ba chết |
| (2) `-03` lời sửa | khớp: `vendor.py` chú thích + BG nói kiểu VD62 *theo dòng đầu (`Max`)*, chỉ mượn RATE `VD341` riêng; `M7` ghim nguyên văn mục |
| (3) CG2 trên cây gộp | `hd2_cong.json`: `WP-C4a` có `tong_o 420 · khop 420`; **`WP-C4b` ⛔ có `tong_o`/`khop`** ⇒ `GET /gates`: `HD2_WP_C4B` **null** · `HD2_WP_C4` **null** *(mong true · true)*; `tests/api/test_isp_gates_hd2.py` **8 đỏ** *(bài quét tệp thật `CG2_R2_03` ×2 bắt đúng `{'WP-C4b': ['tong_o','khop']}`)* |
| (4) `do_hd2.py --goi … --dsn $PG_DSN_TEST` *(IX.VEN + IX.PER nạp kho test)* | **C4a** `DAT`: 44 Vendor-tháng · ô so **420** · ⛔ so được 196 · ô ≠ 0 0 · lệch 0 · KS.AL 44 · bỏ qua 15 vendor. **C4b** `DAT`: 209 = 165 + 44 · ô so **1.981** · ⛔ so được 945 · ô ≠ 0 **988** · lệch 0 · KS.AL 209 · bỏ qua 0 — **y hệt** BG/R1 |
| (5) `--duong-nen --cong 5444` *(một mình, cây gộp)* | **ĐỎ**: 20 failed · 3.765 passed · 2 xfailed · 14 errors · chạy **3.801** *(sàn 3.801)* · tập đỏ **36** *(XFAIL 2)* vs mong **28** ⇒ **thêm 8** *(đúng 8 bài CG2 trên)* · bớt 0 · skipped 0 · deselected 0 |
| `lint-imports` · `kiem_tai_lieu` · `soi_bang_tuyen` | 11 kept · 0 broken · ĐẠT *(350 tệp · 2.659 bảng)* · khớp SQL **45/45** tuyến |

## Phát hiện
- **`H10-R2-01` CHẶN** *(tích hợp, ⛔ lỗi của H10 đứng riêng)* — `do_hd2.py` C4b `--ghi` ⛔ ghi `tong_o`/`khop`; CG2 đòi mọi khối gói. Sửa: ghi thêm `tong_o = 1981` · `khop = 1981 − lệch` như C4a, `--goi WP-C4b --ghi`, gộp tay `hd2_cong.json` giữ cả hai gói; sau đó `--duong-nen` mong trở lại 28 và `/gates` ra `HD2_WP_C4B` + `HD2_WP_C4` = true.
- `H10-R2-02` GHI NHẬN — sàn gộp **3801**, ⛔ cộng tay.
- Backlog: `H10-R1-04` *(WP-C4b-PE)* · `-06` · `-07` · `-08`. Đã đóng: `-01 -02 -03 -05`.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM`. Cây gộp thử `thu/H10` ⛔ commit.
