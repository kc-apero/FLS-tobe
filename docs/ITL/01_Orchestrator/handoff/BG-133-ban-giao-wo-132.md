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
