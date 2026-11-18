# KQ-135 — biên bản kiểm `BG-133` *(R2 · Step 13 · H4 · WP-C2 — vòng sửa sau `KQ-134`)*

| | |
|---|---|
| **Thuộc** | `BG-133` *(mục "Vòng sửa sau R1")* · `WO-132` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con của orchestrator ISP 3.1.2)* · 2026-11-18 |
| **Đối tượng** | `git diff 131aad3 isp/H4` — `isp/H4` @ `2a68f7b` *(`362eb68` mã+bài · `2d81999` BG · `2a68f7b` BG nguồn số dư)*, cụm PG `5444`, container Linux |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN** *(sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H4.md` v0.2)* |

> Bốn lỗi R1 **đã đóng đúng chỗ đã khai** *(tái đột biến: tất cả ĐỎ)*. Còn lại một lỗ **còn sót ở chính dung sai**: `rtol 1e-9` rộng ≥ 10⁴× noise ⇒ `BM +50 VND` lọt, và `atol` của BQ/BT là mã chết `(H4-R2-01)`. Không chặn *(lỗi lặp nhiều dòng và `BO/BR +9e-7` đều bị cắn)*; đề xuất sửa rẻ ở lúc gộp hoặc trước khi `CG2` ghim hợp đồng.

## Cổng chạy lại
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `dung_moi_truong_isp.sh --cong 5444` | — | `KẾT: ĐẠT` *(26/26 di trú · 11 hợp đồng · HD1 9845/9967 · `fls_itl` 0 dòng)*; chạy lại sau khởi động lại worker: `ĐẠT` | ✅ |
| `python tools/do_hd2.py --goi WP-C2` | `63016/63016` · đáp án 7883 · bỏ 36 · no-op `[]` | y hệt: `63016/63016 (mong 63016 = 8 × 7877)` · `hàng đáp án 7883 (mong 7883)` · `ô đáp án bỏ 36` · `ô lệch ngoài tên 0` · tháng phủ fx `20` · `KẾT: DAT`. `--ghi` trên bản sao ⇒ `hd2_cong.json` **y hệt** bản commit | ✅ |
| `pytest tests/oracle` + `test_dap_an_406_dau_vao` + `test_gl_so_du_dau` + `test_gl_h1_r3` | `27 passed` *(2 tệp)* | **`196 passed`** *(33,8 s)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5444` *(chạy MỘT MÌNH)* | `12 failed · 3111 passed · 2 xfailed · 14 errors`; nền `28 = 28`; chạy `3139` | **y hệt** `12 failed, 3111 passed, 2 xfailed, 14 errors` *(409 s)* · `28 = 28 (thêm 0 · bớt 0)` · chạy `3139 (mong ≥ 3139)` · skipped 0 · web `3 failed, 664 passed` đỏ = nền `3 = 3` · `KẾT: ĐẠT` | ✅ |
| `.venv/bin/lint-imports` | 11 kept | `Contracts: 11 kept, 0 broken.` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `DẠT` *(251 file · 2321 bảng)* | `✅ cong tai lieu DAT` *(251 file · 2325 bảng · 783 ô ngày · 104 mã QĐ — chưa gồm sổ/phiếu R2)* | ✅ |
| `kiem_so_song.py` | — | **bỏ qua** *(đường Windows)* | — |

## Trạng thái lỗi R1 *(tái đột biến trên bản sao `git archive isp/H4`)*
| Mã | Đột biến R2 | Kết | Trạng thái |
|---|---|---|---|
| `H4-R1-01` dung sai | `BO +9e-7` · `BR +9e-7` · `BO +1e-9` · `BO +1e-11` *(ds3000)* | **4/4 ĐỎ** *(`lech=1`)* | **ĐÓNG** *(+ `H4-R2-01` phần dư)* |
| `H4-R1-02` mẫu số | xoá `BO` *(`tong_o 55139`)* · xoá `BP` *(55139)* · xoá 100 `BT` *(62916)* · xoá hàng cuối *(63008)* · nhân đôi hàng · xoá hàng ds6506 | **6/6 ĐỎ**; tắt khoá `mong_tong_o=None` + xoá `BO` ⇒ XANH *(chứng khoá là thứ cắn)* | **ĐÓNG** |
| `H4-R1-03` ô bỏ / no-op | `BM[4962]+1` ⇒ `no_op_lech=[4962,4963]` · `BT[7631]+0,001` ⇒ `[7631]` · `BQ[6073]+0,5` ⇒ `[6073]` · xoá hàng ds6506 ⇒ `[6507]` · `BQ[4961]=BQ[4962]=None` ⇒ ĐỎ | **ĐỎ cả 4 hàng thử** *(≥ 1/6 hàng vỡ là đủ)*; **nhưng** `o_dap_an_bo` chỉ in, ⛔ khoá | **ĐÓNG một phần** ⇒ `H4-R2-02` |
| `H4-R1-04` cột R / D | `"Nguyen Van A …"`⇒ TỪ CHỐI · `#n/a ()` · `#REF! ` · `D="USD\t"` · `D=" USD"` ⇒ TỪ CHỐI; `#N/A ()` ⇒ OK | OK; **nhưng** `#NGUYENVANA0912345678` qua | **ĐÓNG một phần** ⇒ `H4-R2-03` |
| `H4-R1-05` tham chiếu | `grep` mục *Số dư* trên `isp/H4` | vẫn **0** | **MỞ** *(orchestrator gộp)* |

## Bảng AC
| AC | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|
| AC-1 | `63016` ô so = `63016` ô đáp án so được = `7877 × 8`; mẫu số **khai trước** *(`MONG_DONG_SO 7877 · MONG_TONG_O 63016 · MONG_SO_DONG_DAP_AN 7883`, hằng, ⛔ tự đếm)*; bài tautology đã thay | **ĐẠT** |
| AC-2 | đáp án rỗng ⇒ `0 ô` ⇒ ĐỎ *(bài `B2` xanh trong 196)* | **ĐẠT** |
| AC-3 | MONG hai chiều + dung sai THEO CỘT; chứng ĐỎ `BO +9e-7`; ⚠ phần dư rtol | **ĐẠT** *(+ F-1)* |
| AC-4 | `H1-R3-01/02` — không đổi ở R2; 196 xanh | **ĐẠT** |
| AC-5 | sàn `3139` = số chạy đo *(`3139`)*, pin khớp | **ĐẠT** |

## Thử phá R2 *(~30 ca, bản sao `git archive`, ⛔ commit)*
| # | Câu hỏi | Số đo | Kết |
|---|---|---|---|
| 1 | Dung sai mới có **quá chặt** *(ĐỎ giả)*? | gốc xanh ở `atol,rtol ×0,1` và `×0,03`; xanh cả khi chỉ hạ `rtol` xuống `1e-13`. Chạy hai lần ⇒ cùng kết *(xác định)*. Noise lệch thật *(`BM` abs `3,1e-4`; rel max `1,6e-13` BM / `3,2e-12` BQ)* ⇒ biên rộng. Không so khác máy được *(chỉ một máy)* — rủi ro BLAS/thứ tự cộng thấp vì biên ≥ 10×. | **KHÔNG chặt** |
| 2 | Còn **lỗ ở BM** *(rtol 1e-9 × 1e11)*? | `BM +1/+10/+50 VND` ds3000 & ds7890 **ĐẠT**; `+100 VND` ds3000 ĐẠT, ds7890 ĐỎ ⇒ lọt hàng chục VND. `BQ +1e-9` bVND ĐẠT; `BQ/BT` `atol` là mã chết *(rtol·\|BQ\|≈1,4e-7)* | **LỖ** — `H4-R2-01` |
| 3 | `MONG_*` khai trước hay suy từ dữ liệu? | hằng ở đầu `do_hd2.py`; `MONG_TONG_O = 8 * MONG_DONG_SO` chỉ là hằng số học, không đọc ảnh; `tong_o=None` tắt khoá ⇒ xoá `BO` xanh *(⇒ khoá là thứ cắn)*. Không tautology mới | **ĐẠT** |
| 4 | `no_op_lech` ĐỎ khi 1/6 hàng vỡ? | 4 hàng thử khác nhau *(4962 · 7631 · 6073 · xoá 6506)* ⇒ ĐỎ cả 4; cả hai cùng `None` không tạo xanh giả *(mẫu số đỏ)* | **ĐẠT** |
| 5 | `ITL_LOI_RE` chặn nhầm `itl_id` hợp lệ? | ảnh thật 7.883 hàng ⇒ 4 lệch = `#N/A ()` ✔ qua; `#N/A` trần qua; không chặn nhầm. **Nhưng** quá lỏng với chữ HOA | `H4-R2-03` |
| 6 | Nguồn số dư đầu kỳ nhất quán? | 5 hằng ảnh = `CALC_ZONE_406` *(checkout chính)* ✔ ds 24 ×5 ✔; ⛔ đổi hằng. BG nhầm "3 hằng bVND/mUSD" *(thật 2)* | `H4-R2-04` |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | parity thật *(R1 đã chứng)*; mẫu số khoá; dung sai theo cột cắn `BO/BR +9e-7`, còn rộng ở BM/BQ/BT | thử phá 1–4 |
| **Dữ liệu** | ⛔ ghi kho *(`fls_itl` 0 dòng)*; ảnh `9339488011a9358e` ⛔ đổi; ⛔ gọi Drive | 196 passed |
| **Màn hình** | không áp dụng | `git diff --stat` ⛔ chạm `fls/web` |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** `H4-R2-01` | NÊN SỬA *(không chặn)* | `do_hd2.py:120-129` · `hd2_cong.json` | `BM +50 VND` ĐẠT; `rtol 1e-12` vẫn xanh gốc | `DEV` |
| F-2 `H4-R2-02` | GHI NHẬN | `do_hd2.py:299-304` | xoá `BN[4962]` ⇒ `o_dap_an_bo 35`, `dat=True` | `DEV` |
| F-3 `H4-R2-03` | GHI NHẬN | `gl_406_dau_vao.py:97` | R=`#NGUYENVANA0912345678` ⇒ chấp nhận | `DEV` |
| F-4 `H4-R2-04` | GHI NHẬN | `BG-133` | "3 hằng bVND/mUSD" ⇒ 2 | `DEV`/orchestrator |

## Bài thử mới
⛔ Không thêm bài vào `tests/` *(vai KIỂM)*. **Đề xuất cho DEV** *(đã chứng ĐỎ trên mã hiện tại)*: `BM +1 VND` ds3000 ⇒ `len(lech) ≥ 1`; `BQ +1e-9` ⇒ lệch; `chuan_bi` với R=`#NGUYENVANA0912345678` ⇒ `ValueError`; xoá `BN[4962]` ⇒ `phan_xu.dat is False`.

## Hỏi *(chốt orchestrator)*
- **Q1** — `H4-R2-01` có chặn gộp? Khuyến nghị **A: ⛔ chặn** — sửa trước khi `CG2` *(Step 30)* ghim `dung_sai_theo_cot` *(đổi 2 hằng + 2 bài; ngược lại hợp đồng phải đổi lần nữa)*; không chặn nghiệm thu H4. *B: gộp, dồn sau* — rủi ro: hợp đồng bị ghim ở `rtol 1e-9`.
- **Q2** — `H4-R2-02/03/04`: khuyến nghị **A: gom vào cùng lượt sửa nhỏ** *(không cần R3 riêng nếu chỉ đổi hằng/regex; R3 chỉ đo lại)*.
- **Q3** — `H4-R1-05`: khuyến nghị **A: gộp mục *Số dư đầu kỳ* + *Đính chính* của `CALC_ZONE_406.md` cùng H4**.
