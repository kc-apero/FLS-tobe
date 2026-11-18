# BG-133 — bàn giao `WO-132` (ISP 3.1.2 · Step 13 · H4)

| | |
|---|---|
| **Thuộc** | `WO-132` — KS.CA · parity CA.GL ↔ đáp án 406 (cổng HD2 đầu tiên) |
| **Phát bởi** | `fls-dev` (phiên cloud · làn BE-HC) · 2026-11-18 |
| **Nhận** | `fls-test` (R1 `KQ-134` · R2 `KQ-135` · R3 `KQ-136`) |
| **Nền** | `a8367ed6ec0bc5a31c92bb34bdf70d736cbc9a65` *(ngọn `claude/bold-galileo-zukpaf`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/H4` — ⓪ `07d9709` *(H1-R3)* · ① `1ade00c` *(H4)* · ② *(BG này)* **(đã đẩy)** |

> `git ls-remote origin claude/bold-galileo-zukpaf-isp/H4` → cập nhật ở TIN NHẮN CUỐI.

## Tóm tắt một dòng
Engine `tinh_gl` (H1) chạy trên **tiền nguyên tệ E·F đọc ĐỘC LẬP** từ sheet 406 + `ix_fx` + **gieo số dư đầu kỳ gõ tay (5 ô hàng 24)** tái hiện **63 016/63 016 ô** của 8 cột `BM…BT` khớp đáp án 406 trong dung sai số thực; 0 ô lệch ngoài tên; lệch có tên đúng MONG.

## Vì sao có khuôn DATA mới (quyết định orchestrator B′, 18/11)
- ISP Step 13 *"chạy H1 trên dòng sổ"* cần **tiền NGUYÊN TỆ** `E` (PS Nợ) · `F` (PS Có). Repo **⛔ có ảnh nào mang E/F** — `O10` (ISP §2): cột PS Nợ/Có · TK · tiền tệ đã bị bỏ khỏi ảnh (đo lại 18/11: grep `ps_no|ps_co` ở `fls/`+`tools/`+`tests/fixture/` = 0 ảnh money; kho `fls_itl` cụm 5435 = 0 dòng).
- Phương án A *(tái dựng Nợ/Có từ `BO`/`BP` của đáp án)* = **VÒNG TRÒN** (BO/BP tự khớp) ⇒ orchestrator bác. B′ = đọc cột đầu vào `D·E·F` của chính sheet 406 bằng khoá SA chỉ-đọc (A·D·E·F·R hàng 10..7892; **⛔ phủ B:C** = Số CT/Diễn giải), đóng băng thành ảnh đầu vào ⇒ `BO`/`BP` thành **phép kiểm thật**.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/gl.py` | ⓪ `ThieuTyGia`·`TienKhongHuuHan` giữ trường + `__reduce__` (pickle/copy, `H1-R3-01`); ① `SoDuDau` + tham số tuỳ chọn `tinh_gl(…, so_du_dau=…)` gieo số dư đầu kỳ (mặc định ⛔ có ⇒ H1 cũ ⛔ đụng) |
| `tools/do_hd2.py` | **mới** — cổng parity `--goi WP-C2 [--ghi]` |
| `tools/khuon_dong_bang/gl_406_dau_vao.py` | **mới** — khuôn đóng băng ảnh đầu vào (khuôn DATA, hợp đồng lưới SA như `gl_406`) |
| `tests/fixture/dap_an/gl_406_dau_vao.json` | **mới** — ảnh đầu vào 7883 dòng + `so_du_dau` 5 ô + `itl_id_lech` 4 (checksum `9339488011a9358e`) |
| `docs/ITL/_tools/hd2_cong.json` | **mới** — hợp đồng cho `CG2` (Step 30) |
| `tests/oracle/test_do_hd2_ca.py` | **mới** — H4-B1/B2/B3 (8 bài) |
| `tests/bao_cao/test_gl_so_du_dau.py` | **mới** — `so_du_dau` engine (5 bài) |
| `tests/du_lieu/test_dap_an_406_dau_vao.py` | **mới** — ảnh đầu vào (8 bài) |
| `tests/bao_cao/test_gl_h1_r3.py` | **mới** (⓪) — `H1-R3-01/02` (6 bài) |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3100→3106 (⓪)→3128 (①) |

## Đỏ-trước (strict TDD)
- **⓪ `H1-R3-01`**: `tests/bao_cao/test_gl_h1_r3.py::test_R3_01_…` ĐỎ trước — `pickle.loads(pickle.dumps(loi))` ⇒ `TypeError: ThieuTyGia.__init__() missing 3 required positional arguments` (và `TienKhongHuuHan` thiếu 2). Sau sửa: 6 passed.
- **① H4**: `tests/oracle/test_do_hd2_ca.py` ĐỎ trước — `ImportError: cannot import name 'do_hd2'` (exit 2). Sau viết `do_hd2.py`: 8 passed.
- **Cổng mới chứng ĐỎ (Đ5)**: `test_H4_B2_dap_an_rong_thi_DO_0_o` (đáp án rỗng ⇒ 0 ô ⇒ ĐỎ, Đ3) · `test_H4_B3a_mot_o_lech_NGOAI_ten_thi_DO` · `test_H4_B3b_tap_lech_co_ten_KHAC_mong_thi_DO` (Đ5 cả hai chiều) · `test_H4_B1_THIEU_gieo_so_du_dau_thi_DO_tu_ds24` (bỏ gieo số dư ⇒ >1000 ô lệch, chỉ cột lũy kế/đánh giá lại, từ ds24 — phá nguồn → cắn → trả nguyên).

## Bằng chứng từng AC (mục 8 của Step 13)
| AC | Bằng chứng |
|---|---|
| **AC-1 (H4-B1)** | `python tools/do_hd2.py --goi WP-C2` → `ô so/khớp 63016/63016` (= số ô đáp án so được 63016) · 0 ô lệch ngoài tên · KẾT `DAT`. Bài: `test_H4_B1_so_o_so_lon_hon_0_va_bang_so_o_dap_an_so_duoc`, `…_ca_8_cot_khop_trong_dung_sai`. Lệch liệt kê theo (kỳ, dòng, cột) + tên. |
| **AC-2 (H4-B2)** | `test_H4_B2_dap_an_rong_thi_DO_0_o`: đáp án rỗng ⇒ `tong_o=0` ⇒ `PhanXu` ⛔ đạt, lý do mang "0 o" (Đ3). |
| **AC-3 (H4-B3)** | MONG lệch có tên khai TRƯỚC (`MONG_THIEU_D/ITL_NA/KY_VANG/THANG_THIEU_TY_GIA`). `test_H4_B3a` (ô lệch ngoài tên ⇒ ĐỎ) + `test_H4_B3b` (tập lệch-có-tên ≠ mong ⇒ ĐỎ) ⇒ cả hai chiều. Dung sai khai trong `DungSai` (atol 1e-6 · rtol 1e-9 — BT theo độ lớn lũy kế). |
| **AC-4** | `H1-R3-01/02` sửa, bài ĐỎ-trước (trên). |
| **AC-5 (Q8)** | `MONG_PYTEST_TOAN_BO` 3128 = số thu thập (pin `test_S0_R2_03_…` + `test_S0_R3_02_…`), cùng commit thêm bài. |

### Số ô so / lệch theo tên / kỳ
- **Ô so:** 63 016 (7 877 dòng × 8 cột; bỏ 6 hàng thiếu D). **Khớp:** 63 016. **Lệch ngoài tên:** 0.
- **Lệch CÓ TÊN:**
  - `thieu_tien_te_D` = **6** (ds 4962·4963·6073·6507·6949·7631) — AS-IS `BO`/`BP` rỗng; FLS ⛔ dựng dòng (tiền tệ ngoài 5 cột); no-op cho tồn luỹ kế ⇒ bỏ ⛔ lệch dòng sau.
  - `itl_id_na` = **4** (ds 6684·6836·7500·7832) — nối bằng `dong_sheet`, vẫn SO được.
  - `ky_vang_406` = **4** (`202605` 239/537 · `202606`·`07`·`08` vắng) — sổ (`itl_ledge_adjustment` 9967) vượt bản sao 406.
  - `thang_thieu_ty_gia` = **0** / mẫu số **20** tháng phủ `ix_fx` (Đ3 — dải 202410..202605 đều có tỷ giá; 0 tháng ném `ThieuTyGia`).
- **Số dư đầu kỳ (5 ô hàng 24):** gieo `USD +1 242 689` · `SGD +985 537` · `VND +6 653 796 781` · `bvnd_ton +56.842628558` · `musd_ton +2.267718` (công thức FORMULA verbatim trong ảnh). Thiếu gieo ⇒ chênh ~56.84e9 bVND từ ds24 (đo độc lập 18/11 TRƯỚC khi orchestrator đọc công thức — khớp đúng).

## Cổng (kết quả nguyên văn)
| Lệnh | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --duong-nen --cong 5435` | **KẾT: ĐẠT** — toàn bộ `12 failed, 3100 passed, 2 xfailed, 14 errors`; tập đỏ+XFAIL = đường nền `28 = 28` (+0 −0); chạy 3128 (mong ≥ 3128) · skipped 0 · deselected 0. web `3 failed, 664 passed`; đỏ = đường nền `3 = 3`. *(bài đỏ/errors CÓ SẴN = đường nền, ⛔ do H4)* |
| `pytest tests/oracle/test_do_hd2_ca.py tests/bao_cao/test_gl_so_du_dau.py tests/bao_cao/test_gl_h1_r3.py tests/du_lieu/test_dap_an_406_dau_vao.py` | `27 passed` |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT` (248 file · 2309 bảng · 781 ô ngày · 104 mã QĐ) |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 41 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut` |
| `python -m fls.db.pg_migrate` | `26/26 di tru · pg_verify khớp (0 lệch)` *(⛔ chạm schema — chỉ xác nhận)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | **⛔ PRE-EXISTING** — `A1·B1·C6 DOI TRANG THAI` lệch Y HỆT trên nền `a8367ed` (chạy lại ở main checkout để xác nhận); audit roadmap đang chạy; diff H4 ⛔ chạm tệp `.md` nào ⇒ ⛔ phải do H4 |
| `python tools/kiem_so_song.py` | **⛔ CHƯA CHẠY** — gọi `.venv/Scripts/lint-imports.exe` (đường Windows; container Linux). `fls-dev.md` cho bỏ qua đường Windows; hợp đồng import đã kiểm trực tiếp bằng `.venv/bin/lint-imports` (11 kept) |

## Kho thật
- `KHONG_CHAM` — ghi kho: KHÔNG (`WO-132 Dữ liệu`). `tinh_gl` thuần (tham số); `do_hd2` chỉ đọc ảnh/ix_fx; cụm 5435 `fls_itl` = 0 dòng. Drive: chỉ ĐỌC (SA chỉ-đọc), ⛔ ghi; bản thô chỉ ở `/tmp/h4`.

## Giới hạn / Dev tự thấy còn yếu
1. **FLS CHƯA có khái niệm số dư đầu kỳ** (errata ⑳). H4 GIEO 5 ô gõ tay hàng 24 đúng như sheet để parity về 0, nhưng nguồn chính thức của số dư ấy là **câu hỏi cho BA/owner** — chưa có bản khai nghiệp vụ. `hd2_cong.json` + docstring khai rõ. Test soi: nếu owner xác nhận cách khác, `so_du_dau` là tham số tường minh, đổi một chỗ.
2. **Dung sai parity** (atol 1e-6 · rtol 1e-9) chừa ~300× trên lệch tối đa đo được (rel 3.2e-12 ở BQ/BT). Số dư đầu kỳ `BT24=…+2.267718` là hằng 6 chữ số gõ tay ⇒ BT24 khớp đúng theo hằng ấy (⛔ suy lại). Test chưa ghim riêng từng ngưỡng theo cột — dùng một `DungSai` chung.
3. **`BO`/`BP` round-trip?** KHÔNG (đây là điểm B′ sửa so với A): `E`/`F` đọc độc lập ⇒ `BO`/`BP` là phép kiểm thật (7877/7877 khớp từ dữ liệu ĐỘC LẬP, ⛔ từ chính BO/BP).
4. **`gl_406_dau_vao.json` tái tạo từ công cụ?** Chỉ kiểm bằng checksum tái tính (`AnhChup`) — ⛔ chạy lại tool từ ảnh được (cột `A` ngày ⛔ vào ảnh, chỉ `ky` ⇒ ⛔ suy ngược serial). Bản thô ở `/tmp` (⛔ commit).

## Câu hỏi cho orchestrator / BA
- **Q1 (errata ⑳):** Số dư đầu kỳ (USD 1 242 689 · SGD 985 537 · VND 6 653 796 781 @ 202412) — nguồn nghiệp vụ chính thức? Hiện gieo y sheet (5 ô gõ tay) để parity; TO-BE cần một bản khai số dư đầu kỳ có chủ (owner ký) thay vì hằng trong ô.
- **Q2:** `khop_owner --kiem` A1·B1·C6 đang vỡ trên NỀN (⛔ do H4) — có chặn PUSH H4 không, hay thuộc audit roadmap riêng?

---

## Vòng sửa sau R1 (KQ-134)

| | |
|---|---|
| **Phiên** | `fls-dev` cloud con *(Opus 4.8 · làn BE-HC)* · 2026-11-18 · cụm PG **5435** · nhánh `isp/H4` |
| **Nền vòng sửa** | `131aad3` *(② BG gốc)* |
| **R1 `KQ-134`** | ĐẠT · 0 CHẶN · **2 NÊN SỬA** `H4-R1-01/02` · **3 GHI NHẬN** `-03/-04/-05` |
| **Làm** | sửa `-01`·`-02` *(NÊN SỬA)* + `-03`·`-04` *(GHI NHẬN)*; `-05` ⛔ chạm *(orchestrator lo lúc gộp)* |
| **Commit** | ③ mã + bài · ④ BG này — sha ở TIN NHẮN CUỐI |

### Tóm tắt một dòng
Thay dung sai `atol 1e-6` chung bằng **dung sai THEO CỘT có căn cứ đo** *(BM rtol; 7 cột nhỏ atol 1e-12/1e-11)*, **khoá mẫu số bằng hằng khai trước** *(`MONG_TONG_O 63.016` · `MONG_SO_DONG_DAP_AN 7.883`)*, và biến **no-op + 36 ô bỏ** từ LỜI thành ĐO; parity thật vẫn `63016/63016` ĐẠT, 5 đột biến từng XANH nay ĐỎ.

### Phát hiện đã sửa
| Phát hiện | Mức | ĐÃ SỬA *(tệp)* | Bằng chứng mới | Đỏ-trước *(mã cũ `131aad3`)* |
|---|---|---|---|---|
| `H4-R1-01` dung sai | NÊN SỬA | `do_hd2.py` `DungSaiCot` + `DUNG_SAI_COT` *(theo cột)* · `hd2_cong.json` `dung_sai_theo_cot` | `BO +9e-7` *(900 VND)* ở ds2073 ⇒ **ĐỎ**; `BO +1 VND` ở hàng `BO=0` ⇒ **ĐỎ** | `atol 1e-6` cũ ⇒ cả hai **XANH** *(bài `_mong_atol_cu_bo` chứng trong chính test)* |
| `H4-R1-02` mẫu số | NÊN SỬA | `do_hd2.py` `MONG_TONG_O/MONG_DONG_SO/MONG_SO_DONG_DAP_AN` + khoá ở `_phan_xu`; bài tautology → `tong_o == 8×dong_so` | xoá `BO/BP` ⇒ `tong_o 47262` **ĐỎ** · xoá 100 `BT` ⇒ `62916` **ĐỎ** · xoá hàng cuối ⇒ `so_dong 7882` **ĐỎ** · nhân đôi ⇒ `7884` **ĐỎ** | cả 4 ⇒ `dat=True` **ĐẠT** *(đo lại trên `131aad3`)* |
| `H4-R1-03` ô bỏ/no-op | GHI NHẬN | `do_hd2.py` `o_dap_an_bo` + `no_op_lech` *(in + `hd2_cong.json`)* | `ô đáp án bỏ = 36` *(6 hàng × 6 ô khác rỗng)* in ra; đổi `BM[4962]` ⇒ `no_op_lech=[4962]` **ĐỎ** | `BM[4962]` lệch hàng trên ⇒ `dat=True` *(cổng ⛔ kiểm)* |
| `H4-R1-04` cột R mở | GHI NHẬN | `gl_406_dau_vao.py` `ITL_LOI_RE` *(tập đóng lỗi Sheets)* + từ chối `D` đuôi trắng · `test_DV_B4` ghim | chuỗi tự do `"Nguyen Van A …"` ở R ⇒ **TỪ CHỐI** · `D="USD "` ⇒ **TỪ CHỐI** · `#N/A ()` ⇒ OK | khuôn cũ nhận chuỗi tự do nếu đủ 4 hàng ⇒ **ĐẠT** *(R1 đo)* |
| `H4-R1-05` tham chiếu | GHI NHẬN | ⛔ chạm *(mục "Số dư đầu kỳ" của `CALC_ZONE_406.md` ở nhánh làm việc — orchestrator gộp)* | — | — |

### Dung sai THEO CỘT — căn cứ ĐO *(18/11, 7.877 dòng; engine ↔ đáp án, KHÔNG áp dung sai)*
| cột | đơn vị | max\|lệch\| thật | max rel | ngưỡng atol | biên atol/noise | ghi chú |
|---|---|---|---|---|---|---|
| **BM** | VND ~2,98e11 | 3,14e-04 *(float-ulp)* | 1,60e-13 | 1e-3 *(sàn gần-0)* | — | **rtol 1e-9 canh** *(≈57 VND ở đuôi)*; `\|exp\|≥6e7` ⇒ `rtol·\|exp\|≥0,06 ≫ noise` |
| BN | mUSD ~11,5 | 1,22e-14 | 1,60e-13 | **1e-12** | ×82 | |
| **BO** | bVND ~115,6 | 1,00e-14 | 3,03e-16 | **1e-12** | ×100 | ← đột biến `+9e-7 (900 VND)` nay cắn |
| BP | bVND ~128,9 | 1,27e-14 | 2,38e-16 | **1e-12** | ×79 | |
| BQ | bVND ~296,3 | 1,09e-12 | 3,19e-12 | **1e-11** | ×9 | cộng dồn — noise sát 1e-12 ⇒ nới 1 bậc |
| BR | mUSD ~4,5 | 1,00e-15 | 3,38e-16 | **1e-12** | ×1000 | |
| BS | mUSD ~5,1 | 1,00e-15 | 3,72e-16 | **1e-12** | ×1000 | |
| BT | mUSD ~11,5 | 7,35e-14 | 2,04e-12 | **1e-12** | ×14 | cộng dồn |

- **Sàn cũ → mới:** `atol 1e-6` CHUNG *(rộng ~10⁶× lệch thật ở 7/8 cột)* → `atol` **THEO CỘT** `1e-12` *(6 cột)* · `1e-11` *(BQ)* · `1e-3` *(BM, chỉ sàn gần-0; rtol 1e-9 canh độ lớn)*. `rtol 1e-9` giữ nguyên *(chỉ cắn ở BM ~1e11)*.
- **Sửa câu SAI** *(Đ4)*: docstring + `hd2_cong.json` cũ ghi *"BT theo độ lớn lũy kế (rtol)"* — **sai**: `rtol·\|BT\|≈2e-9 ≪ atol` ⇒ BT do **atol** quyết định; chỉ **BM** *(VND 1e11)* mới do rtol. Đã sửa cả hai chỗ.

### Mẫu số khai TRƯỚC *(Đ2/Đ5 — cổng ⛔ tự đếm rồi tự so với chính nó)*
`MONG_DONG_SO = 7877` *(= 7883 − 6 hàng thiếu D)* · `MONG_TONG_O = 8 × 7877 = 63016` · `MONG_SO_DONG_DAP_AN = 7883`. `_phan_xu` ĐỎ khi `dong_doc`/`tong_o`/`so_dong_dap_an` ≠ mong. Bài tautology `tong_o == so_o_dap_an_so_duoc` *(hai biến tăng cùng chỗ)* → `tong_o == 8 × dong_so == 63016`.

### Nguồn gốc `phu.so_du_dau` *(chốt orchestrator — trả lời Q1 của BG gốc; ⛔ đổi mã/hằng)*
5 hằng số dư đầu kỳ *(hàng 24 = ngày **2024-12-31**)* = số dư 31/12/2024 của tab `2. CCR` + `2. CCR Cash`, **LOẠI pháp nhân VVOO** *(số dư VVOO = lũy kế dòng sổ hàng 10…24 = 184.184.303)*; 3 hằng bVND/mUSD = 3 hằng tiền tệ × tỷ giá 2024-12 *(khớp từng đồng; lệch chỉ do làm tròn + VND gõ thừa 2)*. Chi tiết soát: `CALC_ZONE_406.md` mục *"Đính chính + soát logic từng ô hàng 24"* *(nhánh làm việc — chờ gộp cùng H4, như `H4-R1-05`)*. **GIỮ 5 hằng y sheet 406** *(parity AS-IS)*; H4 ⛔ đổi mã/hằng ở vòng sửa này.

### H4-R1-03 — ô bỏ + no-op thành phép ĐO
`ô đáp án bỏ = 36` *(6 hàng thiếu D, mỗi hàng 6 ô khác rỗng `BM·BN·BQ·BR·BS·BT`; tổng ô đáp án khác rỗng `63052` − so `63016` = `36`)* in ở `_in_bao` + `hd2_cong.json`. No-op đo: `BM·BQ·BT[ds] == [ds−1]` ở **6/6** hàng *(BR=0)* ⇒ `no_op_lech=[]`; lệch ⇒ ĐỎ.

### Q8 — sàn pytest
`MONG_PYTEST_TOAN_BO` **3128 → 3139** *(+11 = 8 `test_do_hd2_ca` + 3 `test_dap_an_406_dau_vao`; bài de-tautology thay bài cũ ⇒ +0)*; bài ghim `test_S0_R2_03_hang_mau_so_khai_MOT_cho` nâng cùng commit *(= số `pytest --collect-only` = 3139)*.

### Cổng (kết quả nguyên văn — cụm 5435)
| Lệnh | Kết quả |
|---|---|
| `tools/do_hd2.py --goi WP-C2` | `63016/63016` *(mẫu số mong 63016 = 8 × 7877)* · hàng đáp án `7883` · ô đáp án bỏ `36` · no-op lệch `[]` · 0 lệch ngoài tên · **KẾT: DAT** · exit 0 |
| `pytest tests/oracle/test_do_hd2_ca.py tests/du_lieu/test_dap_an_406_dau_vao.py` | `27 passed` |
| `dung_moi_truong_isp.sh --duong-nen --cong 5435` *(chạy MỘT MÌNH)* | **KẾT: ĐẠT** — `12 failed, 3111 passed, 2 xfailed, 14 errors`; đỏ+XFAIL = nền `28 = 28` *(+0 −0)* · chạy `3139 (mong ≥ 3139)` · skipped 0 · web `3 = 3` |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT` *(251 file · 2321 bảng)* |

### Giới hạn còn lại *(Dev tự thấy)*
1. **BQ/BT cộng dồn**: độ nhạy bị `rtol` giới hạn ở đuôi *(lệch dưới ~1.000 VND không cắn — như R1 đã khai)*; đã nới `atol BQ` lên `1e-11` vì noise cộng dồn sát `1e-12`. Nếu ảnh đáp án tái sinh *(checksum đổi)*, cần đo lại biên.
2. **`hd2_cong.json` đổi cấu trúc** `dung_sai` → `dung_sai_theo_cot` *(⛔ "chỉ THÊM")* — làm TRƯỚC khi `CG2` *(Step 30)* ghim hợp đồng, đúng khuyến nghị A của `KQ-134 Q1`.
3. **`H4-R1-04`** chỉ ghim tập đóng ở **khuôn** *(bảo vệ lần đóng băng sau)* + `test_DV_B4` *(bảo vệ ảnh đã commit)*; ảnh hiện `9339488011a9358e` ⛔ đổi *(4 giá trị vẫn `#N/A ()`)*.
