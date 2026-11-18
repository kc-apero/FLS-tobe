# KQ-134 — biên bản kiểm `BG-133` *(R1 · Step 13 · H4 · WP-C2)*

| | |
|---|---|
| **Thuộc** | `BG-133` · `WO-132` *(ISP 3.1.2 Step 13)* |
| **Kiểm bởi** | `fls-test` *(phiên cloud con của orchestrator ISP 3.1.2, Sonnet)* · 2026-11-18 |
| **Đối tượng** | toàn bộ `git diff a8367ed isp/H4` — `isp/H4` @ `fc88cc6` *(⓪ `07d9709` · ① `1ade00c` · ② `fc88cc6`)*, cụm PG `5435`, container Linux |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 2 NÊN SỬA · 3 GHI NHẬN** *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H4.md` v0.1)* |

> **Parity có THẬT** — đầu vào so *(E/F nguyên tệ + `ix_fx` + 5 hằng)* độc lập với đáp án; ⛔ đường nào đọc `BM…BT` làm đầu vào. Nhưng **cổng còn hai chỗ lỏng** *(dung sai atol · mẫu số tự đếm)* mà đột biến nhỏ/xoá-ô **sống** ⇒ 2 NÊN SỬA *(⛔ chặn: lỗi lệch lớn/lặp đều bị cắn 100 %)*. Đề xuất DEV sửa ở lượt R2.

## Cổng chạy lại *(Test tự chạy — so với `BG-133`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `bash tools/dung_moi_truong_isp.sh --cong 5435` *(Bước 0)* | — | `KẾT: ĐẠT` *(26/26 di trú · 11 hợp đồng · HD1 9845/9967 · kho `fls_itl` 0 dòng)* | ✅ |
| `python tools/do_hd2.py --goi WP-C2` | `63016/63016` ô · 7.877 dòng × 8 cột · 0 lệch ngoài tên | `63016/63016` *(= ô đáp án so được `63016`)* · `ô lệch ngoài tên: 0` · `thieu_tien_te_D 6 · itl_id_na 4 · ky_vang_406 4 · thang_thieu_ty_gia 0` · mẫu số tháng `20` · `KẾT: DAT` · exit 0 · 0,39 s | ✅ |
| `pytest` 4 tệp bài mới + `tests/oracle` | `27 passed` *(4 tệp)* | **`185 passed`** *(4 tệp + toàn `tests/oracle`; 26,2 s)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5435` *(chạy MỘT MÌNH, sau mọi đột biến)* | `12 failed · 3100 passed · 2 xfailed · 14 errors`; đỏ = nền `28 = 28`; chạy `3128` | **y hệt**: `12 failed, 3100 passed, 2 xfailed, 14 errors` *(405,6 s)* · `28 = 28 (thêm 0 · bớt 0)` · chạy `3128 (mong ≥ 3128)` · skipped 0 · deselected 0 · web đỏ = nền · `KẾT: ĐẠT` | ✅ |
| `.venv/bin/lint-imports` | 11 kept | `Contracts: 11 kept, 0 broken.` | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `DẠT` *(248 file · 2309 bảng)* | `✅ cong tai lieu DAT` *(249 file · 2313 bảng · 781 ô ngày · 104 mã QĐ — +1 file/+4 bảng = sổ H4 của R1)* | ✅ |
| `python tools/soi_bang_tuyen.py` | 41 tuyến | `✅ ban khai KHOP SQL that o ca 41 tuyen` | ✅ |
| `python docs/ITL/_tools/khop_owner.py --kiem` | A1·B1·C6 lệch *(có sẵn)* | A1 · B1 · C6 `DOI TRANG THAI` + khối lộ trình lệch — **y hệt nền**; diff H4 ⛔ chạm `.md` nào ⇒ ⛔ thuộc H4, ⛔ chặn *(theo orchestrator đã đo)* | ✅ |
| `python tools/kiem_so_song.py` | chưa chạy *(đường Windows)* | **bỏ qua** *(đường Windows/`.venv/Scripts` — theo lời giao)* | — |

## Bảng AC *(`WO-132` · ISP Step 13)*
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** H4-B1 | số ô so > 0, = ô đáp án so được; 8 cột khớp trong dung sai | `63016` ô so = `63016` ô đáp án so được = `7.877 × 8` ✔ *(`7.883 − 6 hàng thiếu D = 7.877`)*; 0 lệch ngoài tên. ⚠ mẫu số **⛔ khoá** `8×dong_so` *(`H4-R1-02`)* | **ĐẠT** *(+ F-1)* |
| **AC-2** H4-B2 | đáp án rỗng ⇒ ĐỎ `0 ô` *(Đ3)* | R1 đo lại: xoá `BM…BT` mọi hàng ⇒ `tong_o=0` ⇒ ĐỎ `chi so duoc 0 o`; `fx` thiếu `202501` ⇒ ĐỎ `0 ô` + `ThieuTyGia` | **ĐẠT** |
| **AC-3** H4-B3 | `MONG` khai trước; lệch ngoài tên ⇒ ĐỎ; tập có tên ≠ mong ⇒ ĐỎ *(cả hai chiều)* | mong bớt `7631` ⇒ ĐỎ `thừa [7631]`; thêm `itl_na 1` ⇒ ĐỎ `thiếu [1]`; thêm `ky_vang 202609` ⇒ ĐỎ; thêm 1 hàng thiếu `D` vào ảnh ⇒ ĐỎ `thừa [3010]`; 1 ô lệch ⇒ ĐỎ. ⚠ dung sai `atol` quá rộng *(`H4-R1-01`)* | **ĐẠT** *(+ F-2)* |
| **AC-4** H1-R3-01/02 | bài ĐỎ-trước; sửa | trên bản sao với `gl.py` @ `a8367ed`: **2 FAILED** `test_R3_01_…[ThieuTyGia]` *(`TypeError: __init__() missing 3 required positional arguments`)* · `[TienKhongHuuHan]` *(missing 2)*; sau ⓪ `6 passed`. `R3-02` GHIM hành vi sẵn có *(xanh trước, đúng như bài tự khai)* | **ĐẠT** |
| **AC-5** Q8 | sàn `3128` = số thu thập | `3128` chạy = mong; pin `test_dung_moi_truong_isp.py` khớp | **ĐẠT** |

## Kết quả BẢY trọng tâm thử phá
| # | Câu hỏi | Lệnh / kịch bản | Số đo *(nhãn · mẫu số)* | Kết |
|---|---|---|---|---|
| **1** | Parity có THẬT *(⛔ vòng tròn)*? | Đọc `so_sanh()`: `feed` dựng **chỉ** từ `anh_dau_vao` `{ky, D, E, F}` + `fx` + `so_du_dau`; `anh_dap_an` chỉ cung `exp` *(`_so(a.get(c))`)*. Đột biến: đổi 1 `E`/`F` trong bản sao ảnh đầu vào; đổi **mọi** `BO`,`BP` đáp án thành rác `999` | `E` **hàng cuối** `ds7892` `+1e8` ⇒ đúng **6 ô** ĐỎ ở chính hàng ấy `(BM·BN·BP·BQ·BS·BT)` *(7.877−1 hàng còn lại 0 lệch)*; `E`/`F` hàng giữa ⇒ ĐỎ ở chính hàng + mọi ô luỹ kế phía sau *(`BM·BN·BQ·BT`, đúng nghĩa luỹ kế)*; swap `E↔F` ⇒ `31.092` ô, đủ 8 cột; `BO/BP` rác ⇒ `15.754` ô ĐỎ chỉ ở `BO·BP` *(⇒ BO/BP **không** là đầu vào)*; đổi `D` ⇒ ĐỎ. ⛔ đường nào đọc `BM…BT` làm đầu vào. `dong_sheet·ky·itl_id·D` của ảnh đầu vào ↔ đáp án **0 lệch** *(bài `DV_B5`, 7.883 hàng)* | **ĐẠT** — parity THẬT |
| **2** | 5 hằng số dư đầu kỳ | ở đâu? đối chiếu CALC_ZONE; bỏ gieo; `tinh_gl` gọi không số dư | 5 hằng ở **ảnh đầu vào** `phu.so_du_dau` *(công thức VERBATIM + `hang_so`; bài `DV_B3` ghim)* → `_doc_seed` → tham số **tường minh** `tinh_gl(…, so_du_dau=…)`; ⛔ `grep` hằng `1242689/6653796781/56842628558/2.267718` ở `fls/`+`tools/` ngoài khuôn/`do_hd2` = **0** *(chỉ trong docstring `gl.py:276-278`)* ⇒ ⛔ gõ ngầm. Đối chiếu `CALC_ZONE_406.md:37-48` *(checkout chính)*: `AX24 =+1235500+7189`⇒**1.242.689** ✔ · `BA24 985537` ✔ · `BG24 +6653796781` ✔ · `BQ24 +56842628558/10^9`=**56,842628558** ✔ · `BT24 +2,267718` ✔. Bỏ gieo (**M2**) ⇒ **31.452** ô ĐỎ, cột `{BM,BN,BQ,BT}`, tất cả `ds ≥ 24` *(tác giả `> 1000` ✔)*. Mỗi hằng `+1e-3` ⇒ ĐỎ *(USD 27 ô · SGD 1 · bvnd 7.863 · musd 7.863)*; `VND +1e-3` ⇒ xanh *(1/1000 VND — dưới rtol BM)*, `+1` ⇒ ĐỎ. Đột biến engine: bỏ `bvnd_ton` ⇒ ĐỎ `7.863`; đặt số dư lệch 1 dòng ⇒ ĐỎ `4`. `tinh_gl` không truyền / `None` / `{}` ⇒ y hệt H1 *(bài `test_default_None_y_het_khong_truyen`, đã chạy xanh)* | **ĐẠT** |
| **3** | Dung sai atol 1e-6 · rtol 1e-9 | đo lệch tối đa thật bằng `DungSai(0,0)`; đo phần ô mà atol quyết định; đột biến nhỏ nhất | lệch thật tối đa: abs `BM 3,1e-4` *(giá trị `~10¹¹`, rel `1,6e-13`)* · `BQ 1,1e-12` · `BT 7,4e-14` · `BN 1,2e-14` · `BO/BP/BR/BS ≤ 1e-14`; rel tối đa `BQ 3,2e-12` ✔ *(khớp tác giả)*. **atol quyết định `100%` ô** ở `BN BO BP BQ BR BS BT` *(7.883 · 7.877 · 7.877 · 7.883 · …)*, **chỉ `BM` dùng rtol** ⇒ câu *"BT theo độ lớn lũy kế (rtol)"* **sai** *(`BT≈2,3`: `rtol·BT≈2e-9 ≪ atol`)*. Đột biến sống: engine `G4` `BR +9e-7` một dòng · `G5` `BO +9e-7` *(=900 VND)* một dòng ⇒ **ĐẠT**; đáp án `BO/BS/BT +1e-6` ⇒ 0 lệch; bị cắn từ `+1e-4` *(BO,BT)* · `+1e-3` *(BS)*. `atol 1e-12` ⇒ cổng gốc vẫn xanh · cắn `BO +1e-9` *(1 VND)* | **NÊN SỬA** `H4-R1-01` |
| **4** | Đ5 hai chiều | MONG khai trước? lệch ngoài tên? tập ≠ mong? rỗng? mẫu số nhãn? | MONG khai ở đầu `do_hd2.py:` *(`MONG_THIEU_D` 6 · `MONG_ITL_NA` 4 · `MONG_KY_VANG` 4 · `MONG_THANG_THIEU_TY_GIA` 0)* ✔; **ngoài tên ⇒ ĐỎ** ✔ *(mọi đột biến lệch)*; **bớt / thêm / lạ** ở cả 3 tập ⇒ ĐỎ *(4/4 ca thử: bớt D · thêm itl_na · thêm kỳ · thêm 1 hàng thiếu D)* ✔; **rỗng** `tong_o=0` ⇒ ĐỎ ✔ *(Đ3)*; `tong_o` in kèm nhãn `ô so / khớp : 63016/63016 (= số ô đáp án so được 63016)` ✔. **Lỗ:** mẫu số **tự đếm rồi tự so** — xoá `15.754` ô `BO/BP`, `100` ô `BT`, 10 hàng đáp án cuối, nhân đôi hàng ⇒ vẫn **ĐẠT** *(ở `tong_o` = `47.262/62.916/62.936/63.016`)*; bài `…bang_so_o_dap_an_so_duoc` **tautology** | **NÊN SỬA** `H4-R1-02` |
| **5** | 6 hàng thiếu D · 4 `itl_id_na` · mẫu số | đếm `7.883 − 6 = 7.877`; `× 8`; ô đáp án bị bỏ; `itl_id_na` có bị loại? | `7.883 − 6 = 7.877` ✔ · `7.877 × 8 = 63.016` ✔ · 4 `itl_id_na` **⛔ bị loại** *(vẫn so được, `7.877` gồm cả 4 — chỉ khai tên)*. **Nhưng** đáp án có `63.052` ô khác rỗng ⇒ **36 ô** *(6 hàng × `BM·BN·BQ·BR·BS·BT`)* bỏ khỏi mẫu số mà ⛔ đếm ở chỗ in. R1 kiểm lời *"no-op"*: ở cả 6 hàng `BM·BQ·BT = hàng trên` *(6/6)* ✔ — đúng, chỉ là chưa thành phép đo | **GHI NHẬN** `H4-R1-03` |
| **6** | PII | ảnh có `B`/`C`? vùng đọc? `R` PII? máy quét có ca phá? | ảnh `cot=["ky","itl_id","D","E","F"]` + `phu` `{itl_id_lech, so_du_dau}`: ⛔ `B`,`C`,`Số chứng từ`,`Diễn giải`,`Email Address` *(bài `DV_B2` + R1 quét ảnh: 0)*; vùng đọc `A·D·E·F·R` ⛔ phủ `B:C`. `R` = `ITL#n` hoặc 4 `#N/A ()` — ⛔ PII. Ca phá *(khuôn `dong_bang_sheet gl_406_dau_vao` trên bản thô dựng lại, 8 ca)*: thêm cột `B` ⇒ `TỪ CHỐI` · ô thứ 7 ⇒ `TỪ CHỐI` · chữ ở `E` ⇒ ĐỎ `ô ⛔ số 1/23.649` · chữ ở `D` ⇒ ĐỎ · chữ ở `R` hàng thường ⇒ ĐỎ `phụ 5 ≠ 4` — **BỊ GIẾT 5/5**. **Sống:** chữ tự do thay `#N/A ()` ở **một trong 4** hàng `itl_id_na` ⇒ `ĐẠT`, ghi nguyên văn vào ảnh *(+ `D="USD "` ĐẠT)* | **GHI NHẬN** `H4-R1-04` |
| **7** | H1-R3-01/02 đỏ-trước thật | `git show a8367ed:fls/bao_cao/gl.py` đặt vào bản sao, chạy `test_gl_h1_r3.py`; trả `gl.py` mới | trước: `2 FAILED` *(`R3_01[ThieuTyGia]`: `missing 3 required positional arguments: tien_te, vi_tri, ly_do` · `[TienKhongHuuHan]`: `missing 2`)*; `R3_02` xanh *(GHIM — như bài khai)*; sau: `6 passed`. Không `git stash` *(dùng bản sao)* | **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | `tinh_gl` đúng công thức 406 *(8 cột `BM…BT` khớp 63.016/63.016)*; `so_du_dau` là tham số tường minh, mặc định giữ hành vi H1; cổng HD2 chưa khoá mẫu số + dung sai quá rộng | trọng tâm 1·2·3·4 |
| **Dữ liệu** *(kho thật, chỉ đọc)* | Kho `fls_itl` = 0 dòng trong container *(cụm 5435; `fls_itl` chỉ-THÊM không bị đụng)*; H4 ⛔ ghi kho — đọc ảnh đóng băng `tests/fixture/dap_an/*.json` + `ix_fx.json`. ⛔ cần Drive: R1 **⛔ gọi SA** — kiểm trên ảnh đã commit *(checksum ảnh đầu vào `9339488011a9358e` tái tính ✔ bài `DV_B1`; cross-check ảnh vào ↔ đáp án 0 lệch)* | `pytest tests/du_lieu/test_dap_an_406_dau_vao.py` 8 passed |
| **Màn hình** | Không áp dụng — H4 ⛔ chạm `fls/web` | `git diff --stat` |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| **F-1** `H4-R1-01` | NÊN SỬA | `tools/do_hd2.py:80-92` | `atol` quyết định 7/8 cột; engine `BO +9e-7` một dòng (`900 VND`) ⇒ `63016/63016` ĐẠT; `atol 1e-12` cắn `BO +1e-9` và cổng gốc vẫn xanh | `DEV` |
| **F-2** `H4-R1-02` | NÊN SỬA | `tools/do_hd2.py:233-253` · `tests/oracle/test_do_hd2_ca.py:67` | xoá `BO/BP` toàn đáp án ⇒ `47.262` ô `ĐẠT`; xoá hàng đáp án cuối ⇒ `63.008` `ĐẠT`; bài `tong_o == so_o_dap_an_so_duoc` tautology | `DEV` |
| F-3 `H4-R1-03` | GHI NHẬN | `tools/do_hd2.py:201-203` | 36 ô đáp án (6 hàng thiếu D) bỏ ⛔ đếm; no-op đúng nhưng ⛔ đo | `DEV` |
| F-4 `H4-R1-04` | GHI NHẬN | `khuon_dong_bang/gl_406_dau_vao.py:188` | chữ tự do thay `#N/A ()` ở 1/4 hàng ⇒ ĐẠT | `DEV` |
| F-5 `H4-R1-05` | GHI NHẬN | tham chiếu `CALC_ZONE_406.md` | mục "Số dư đầu kỳ" chỉ ở checkout chính; gộp cùng H4 | orchestrator |

## Bài thử mới *(`tests/nghiem_thu/`)*
⛔ Không thêm bài vào `tests/` ở vòng này *(lời giao: chỉ phiếu + sổ; vai KIỂM ⛔ sửa mã)*. Kịch bản đột biến **~50 ca** chạy trên **bản sao** `git archive isp/H4` *(scratchpad R1, ⛔ commit)*; **ĐỀ XUẤT cho DEV** *(chép vào `tests/oracle/test_do_hd2_ca.py` ở lượt sửa R2)* — mỗi bài đã **chứng ĐỎ trên mã hiện tại**:

| Bài đề xuất | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `test_H4_R1_01_BO_lech_1_VND_thi_DO` — đáp án `BO[ds3000] + 1e-9` ⇒ `len(lech) ≥ 1` | trên mã hiện tại `atol 1e-6` ⇒ `0 lệch` *(đo)* ⇒ bài ĐỎ; với `atol 1e-12` ⇒ `1 lệch` | sau sửa `DungSai` |
| `test_H4_R1_02_tong_o_bang_8_nhan_dong_so` — `tong_o == 8 * dong_so == 63016` và xoá `BO`/`BP`/hàng đáp án ⇒ `phan_xu.dat is False` | trên mã hiện tại `tong_o=47.262 … dat=True` ⇒ ĐỎ | sau thêm `MONG_TONG_O` |
| `test_H4_R1_03_sau_hang_no_op_BM_BQ_BT_bang_hang_tren` | thay đáp án `BM[4962]` khác `BM[4961]` ⇒ hiện **không** ĐỎ | sau thêm kiểm |
| `test_H4_R1_04_itl_id_tho_chi_la_loi_Sheets` — `itl_id_tho ∈ {"#N/A ()"}` | thay 1 giá trị bằng chuỗi tự do ⇒ khuôn hiện ĐẠT | sau ghim |

## Hỏi *(chốt orchestrator)*
- **Q1** — hai NÊN SỬA có chặn **gộp H4** không? Khuyến nghị **A: ⛔ chặn gộp; DEV sửa `H4-R1-01/02` ở lượt sửa rồi R2** — hai lỗ cùng chỗ, sửa rẻ *(đổi 1 hằng dung sai + thêm `MONG_TONG_O` + 4 bài)*; `H4` là cổng HD2 ĐẦU TIÊN, `CG2` *(Step 30)* sẽ khoá hợp đồng `hd2_cong.json` ⇒ sửa trước khi hợp đồng đóng. *B: gộp, dồn việc DEV sau* — rủi ro: `dung_sai` trong `hd2_cong.json` bị `CG2` ghim.
- **Q2** — `khop_owner --kiem` A1·B1·C6: khuyến nghị **A: ⛔ thuộc H4, ⛔ chặn** *(R1 đo: y hệt nền)*.
- **Q3** — nguồn chính thức của số dư đầu kỳ *(errata ⑳, câu hỏi Q1 của `BG-133`)*: khuyến nghị **A: giữ bản gieo hằng + chuyển BA/owner** *(⛔ phạm vi H4)*.
