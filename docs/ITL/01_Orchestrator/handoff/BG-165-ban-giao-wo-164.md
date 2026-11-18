# BG-165 — bàn giao `WO-164` *(ISP 3.1.2 · Step 16 · H5 — SO.CFA1 Daily, cổng WP-C3a)*

| | |
|---|---|
| **Thuộc** | `WO-164` |
| **Phát bởi** | `fls-dev` · 2026-11-18 *(phiên cloud, làn BE-HC, cụm PG 5435)* |
| **Nhận** | `fls-test` *(R1 → `KQ-166`, R2 cuối → `KQ-167`)* |
| **Commit** | `isp/H5` ⇒ đẩy lên `claude/bold-galileo-zukpaf-isp/H5` *(sha ở tin nhắn cuối / `git log`)* |

## Kết luận một dòng
WP-C3a **ĐẠT**: **205.175/205.175** ô khớp *(mẫu số khai trước)* · **0** lệch ngoài tên · lệch có tên = MONG ·
dung sai `atol 1e-14` *(≥10× lệch đo: lá 1,0e-15 · cha 7,5e-16)*.

## Nguồn đầu vào — errata ㉓ *(⛔ ở Step 15: Step 16 cần ảnh đầu vào GL của CF report)*
- Lượt đầu H5 **DỪNG đúng luật**: 17 ảnh `tests/fixture/` ⛔ ảnh nào mang LE + ngày + HD Final + tiền theo dòng
  *(chỉ 2 ảnh có LE — đều là đáp án)*; kho 5435 có 0 dòng `fls_itl`.
- Orchestrator đọc CÔNG THỨC `Report I CFA1 Daily` *(SA 18/11)*: lá GROUP = `SUMIFS(GL!BR, GL!A, ngày, GL!V, nhãn) −
  SUMIFS(GL!BS, …)`; khối LE thêm `GL!P = mã LE`; cha `=sum(con)`. `GL` = sheet `Report I General Ledger` **của bản
  sao CF report** `12S00…` *(⛔ bản sao 406 của H4)*. ⇒ WO-168 *(ảnh ITL Ledge)* bỏ.
- Phiên này đóng băng `tests/fixture/dap_an/gl_cf_dau_vao.json` *(khuôn mới `gl_cf_dau_vao`)*: SA chỉ-đọc, 5 lượt
  `A10:A` · `D10:F` · `P10:P` · `R10:R` · `V10:V` *(⛔ B:C·G)*; **12.385** dòng *(hàng 10…12394, liên tục)*;
  checksum `705ba01386f4875a`. Bản thô chỉ ở `/tmp` phiên.
- ⚠ Cột `P` có **24** giá trị, trong đó TÊN NGƯỜI viết tắt ⇒ ảnh CHỈ giữ `le` ∈ {SGO2 · SGO1 · HGO6 · BGO2}, còn lại
  `null` + đếm ở bảng phụ `le_lop` *(SGO2 3871 · SGO1 715 · HGO6 94 · BGO2 118 · `#N/A` 109 · khác 7478)*.
- BR/BS do `tinh_gl` *(H4)* tính lại từ E/F + `ix_fx` — ⛔ đọc BR/BS của sheet *(vòng tròn)*. **5 số dư đầu kỳ của H4:
  KHÔNG dùng** — CFA1 Daily là phát sinh theo ngày, ⛔ tồn luỹ kế.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/cfa.py` *(mới)* | `cfa1_daily(dong, cay, ngay, khoi)`: lá = Σ(musd_no − musd_co) theo (khối, nhãn HD, ngày) — GROUP ⛔ lọc LE, khối LE lọc `le`; cha = Σ con theo cây *(hậu thứ tự)*; nhãn so NGUYÊN `"MÃ \| Tên"` ⛔ phân biệt hoa thường *(SUMIFS)*; dòng ngoài cây / gán nút cha / ngoài trục ⇒ ĐẾM, ⛔ rơi im lặng |
| `tools/do_hd2.py` | gói `WP-C3a`: `so_sanh_c3a` *(tinh_gl → cfa1_daily → so từng ô)* · MONG mẫu số + lệch có tên · dung sai theo khối `la`/`cha` · `--ghi` CHỈ THÊM *(WP-C2 giữ ở gốc, WP-C3a vào khoá `"WP-C3a"`)* |
| `docs/ITL/_tools/hd2_cong.json` | thêm khoá `WP-C3a` *(WP-C2 y nguyên)* |
| `tools/khuon_dong_bang/gl_cf_dau_vao.py` *(mới)* + `tests/fixture/dap_an/gl_cf_dau_vao.json` *(mới, 3,2 MB)* | ảnh đầu vào *(trên)*; lớp `loi_sheets` dùng `fls.canon.o_loi.la_o_loi` *(1 bản khai luật ô lỗi)* |
| `tests/bao_cao/test_cfa1.py` · `tests/oracle/test_do_hd2_c3a.py` · `tests/du_lieu/test_dap_an_gl_cf_dau_vao.py` *(mới)* | 6 + 11 + 6 = 23 bài |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` **3399 → 3423** *(+23 bài + 1 bài tham số khuôn `test_R2_02_…[gl_cf_dau_vao]`)* |

## Số đo WP-C3a *(mỗi số một vật — Đ4)*
| Vật | Thực | Mong |
|---|---|---|
| dòng ảnh đầu vào | 12.385 | 12.385 |
| dòng vào `tinh_gl` *(bỏ 12 thiếu D)* | 12.373 | 12.373 |
| ô SO *(5 khối × 54 mã × 760 ngày − 25 ô `-`)* | **205.175** | 205.175 |
| ô khớp | **205.175** | = ô so |
| ô KPI loại *(20 mã × 5 × 760)* | 76.000 | 76.000 |
| ô `-` đáp án loại *(phu.o_loi)* | 25 | 25 |
| hàng đáp án *(ô ≠ 0)* | 33.355 | 33.355 |
| trục ngày | 2024-10-20 · 760 cột | 45585 · 760 |
| ngày có số cuối | 2026-11-11 *(7 cột cuối CHƯA CÓ SỐ, ⛔ "0 đã chốt")* | 46337 |

**Lệch có tên** *(Đ5 — khác MONG ⇒ ĐỎ cả hai chiều)*:
- `thieu_tien_te_D` — **12** dòng *(ds 4957 · 4958 · 6068 · 6502 · 6944 · 7626 · 8026 · 8593 · 8649 · 8999 · 9071 ·
  9380)*: ⛔ quy đổi được ⇒ ⛔ vào engine *(AS-IS BR/BS rỗng ⇒ SUMIFS bỏ — khớp 0 lệch xác nhận)*.
- `hd_ngoai_cay` — **162** dòng nhãn V ⛔ khớp nút nào: `ITE | ITE Interest` 152 · `ITE | ITE Interest ` 1 ·
  `Server Cost` 7 · `GAC - Other` 1 · rỗng 1. AS-IS SUMIFS cũng ⛔ cộng ⇒ dòng RƠI ở cả hai — ⚠ **153 dòng ITE bị
  CFA1 AS-IS bỏ sót** *(nhãn ≠ `ITE | Interest` của cây)* — câu hỏi nghiệp vụ cho BA/owner.
- `hd_khac_hoa_thuong` — **5** dòng *(4 `oga | GAC - Other` → OGA · 1 `ofR | Office Rental Cost` → OFR)*.
- `dong_nhan_cha` **0** · `dong_ngoai_truc` **0**.
- **20 mã KPI** *(EBITDA · EBIT · EBT · NP · NPC · NCF · NCFO · CRO · COO · NCFI · COI · NCFF · CRF · COF · PL2 · PL3 ·
  PL4 · PL6 · PL7 · PL8)*: hàng công thức CHÉO *(`=H8+H9+H23`, `NPC` luỹ kế…)* ⛔ "cha = Σ con" ⇒ LOẠI khỏi so,
  đếm 76.000 ô — việc của bước sau. 7 hàng TRỐNG *(AR · CP1.1 (PL2) · CP1.2 · CP2 · CP3 · CFO · PL5)* VẪN so *(0 ↔ 0)*.

**Dung sai theo khối** *(đo trên 205.175 ô, KHÔNG áp dung sai)*: lá 178.575 ô max|lệch| 1,0e-15 · cha 26.600 ô
7,51e-16 ⇒ `atol 1e-14` *(≥ ×10)*, `rtol 0` *(|exp| ≤ 6,1)*. Chứng ĐỎ: +1 nguyên tệ một dòng ⇒ đúng lá + mọi tổ
tiên ĐỎ ở GROUP và khối LE; +1e-12 một ô đáp án ⇒ đúng ô ấy ĐỎ.

## Bằng chứng từng AC *(ĐỎ trước — lệnh + kết quả)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 *(H5-B1)* | `pytest tests/bao_cao/test_cfa1.py` ⇒ exit 2 `ModuleNotFoundError: No module named 'fls.bao_cao.cfa'` | 6 passed — cây `P ← {A, B}`: cha = Σ con do engine; dòng gán nút cha ⛔ cộng + đếm |
| AC-2 *(H5-B2)* | `pytest tests/oracle/test_do_hd2_c3a.py` ⇒ exit 1 `2 failed, 9 errors` `AttributeError: module 'tools.do_hd2' has no attribute 'ANH_GL_CF'`; lần chạy cổng thật đầu tiên ⇒ exit 1 `lệch có tên hd_khac_hoa_thuong ≠ mong: thực 5 · mong 4` *(Đ5 cắn thật — bản khai sửa theo số đo, ⛔ nới)* | `do_hd2 --goi WP-C3a` ⇒ `KẾT: DAT` · 205175/205175 |
| AC-3 | *(cùng lượt đỏ AC-2)* | `test_H5_AC3_dot_bien_mot_dong_so_…` *(lá + mọi tổ tiên, 2 khối)* · `test_H5_AC3_dung_sai_theo_khoi_co_so_do` |
| AC-4 | *(cùng lượt đỏ AC-2)* | đáp án `gt` ⇒ 0 hết: lưới engine Y NGUYÊN, cổng ĐỎ · tỷ giá 202410 ×2 ⇒ lưới đổi |
| ảnh đầu vào | `pytest tests/du_lieu/test_dap_an_gl_cf_dau_vao.py` ⇒ exit 2 `ImportError: cannot import name 'gl_cf_dau_vao'` | 6 passed · `dong_bang_sheet.py gl_cf_dau_vao … --mong 12385` ⇒ `[ĐẠT]` |
| AC-5 *(Q8)* | — | `MONG_PYTEST_TOAN_BO` 3423 = `--collect-only` *(3.423 bài · web 667)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(một lần, cuối)* | **[ĐỎ] — 1 bài thêm** trên commit `3540495`: toàn bộ `13 failed, 3394 passed, 2 xfailed, 14 errors` *(chạy 3423 = mong ≥ 3423 · skipped 0 · deselected 0)*; tập đỏ 29 vs đường nền 28 ⇒ `+ THÊM tests/canon/test_o_loi.py::test_CHI_MOT_BAN_KHAI_trong_ca_he` *(khuôn mới tự viết luật ô lỗi `startswith("#")`)*. Sửa ở commit kế: khuôn gọi `fls.canon.o_loi.la_o_loi` *(ảnh tái đóng băng: checksum Y NGUYÊN `705ba01386f4875a`)*; chạy riêng `test_o_loi.py` + 3 tệp chạm ⇒ `128 passed`. ⛔ chạy lại đường nền *(luật MỘT lần)* — R1 nên chạy. `tests/web` `[ĐẠT]` 3 failed = đường nền 3 · chạy 667. |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — … 293 file, 2533 bang, 823 o ngay, 104 ma QD` |
| `python tools/do_hd2.py --goi WP-C3a` | `KẾT: DAT` · 205175/205175 · chạy ~1 giây |
| `python tools/do_hd2.py --goi WP-C2` | *(trong bộ pytest — `tests/oracle/test_do_hd2_ca.py` xanh)* |

## Kho thật
- `KHONG_CHAM`. ⛔ Drive. Khoá SA chỉ-đọc: 7 lượt `values.get` *(5 lát GL + tiêu đề `A6:V9` + `F8:F19` của CFA1 để
  xác nhận nhãn hàng là `"MÃ | Tên"`)* + 1 lượt FORMULA `F53:H93` *(nhận dạng hàng KPI)*. ⛔ in giá trị ô.

## Chênh trục ngày 20/21 *(errata ㉑)*
Trục TẠM lấy từ ảnh đáp án *(cột đầu 2024-10-20 · CN)*; spec/C6 lưu 21/10. Dòng sổ sớm nhất 2024-10-21 ⇒ cột
20/10 toàn 0 ở engine *(đáp án: 5 ô `-` + 0)* — không ảnh hưởng parity hôm nay. H6 đọc IX.PER thì phải chọn mốc.

## Dev tự thấy còn yếu
- 20 mã KPI **chưa có engine** — WP-C3a hôm nay so 54/74 mã. Cần bước riêng *(công thức chéo hàng là khái niệm mới)*.
- 153 dòng `ITE | ITE Interest` rơi khỏi CFA1 ở cả AS-IS lẫn FLS — parity đúng nhưng **số có thể sai nghiệp vụ**.
- Ảnh đầu vào là MỘT lần đọc 18/11 của bản sao CF report; nguồn chính thức cho LE theo dòng *(cột P)* trong FLS
  chưa có — câu hỏi cho BA *(map từ Tài khoản? IX.ORG?)*.
