# WO-307 — ISP 3.1.2 · Step 44 · H13: SO.PLA3-ATL + IX.PL CHECK — cổng WP-C5b

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~12:35 UTC; giao sau khi gộp H12 qua `--duong-nen` |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-HC** — phiên cloud **Opus 5.5 · medium** (bước engine, luật A) · nhánh `isp/H13` |
| **Nền** | ngọn nhánh làm việc (đã gộp **H12** — AL.KEY `fls/bao_cao/phan_bo_khoa.py`, WP-C5a, IX.ALR 2025 BẬT (`ix_alr_2025_bat.json`, ký `KhanhCQ`); **C12** — IX.PL `fls/cau_hinh/dong_pl.py` (dòng PL là biểu thức trên cây HD + 2 phép CHECK); H8 · DT7 · DT7b · DT10 (`atl.json`)) |
| **Dải phiếu** | `BG-308` · `KQ-309` (R1) · `KQ-310` (R2 cuối). Số trống kế tiếp sau dải: **311** |

## Vì sao
- ISP **Step 44 · H13** (wave W15) — **đường găng** H12 ✅ → **H13** → H14 → I2.

## Đã đo — thay chữ ISP (đọc `BG-292` + `KQ-293` + `KQ-294` (H12) · BG của C12 · `BG-270` + `KQ-271/272/286` (DT11))
- **ATL của FLS** = đầu ra AL.KEY (H12) ở **cờ 2025 BẬT**. Lệch ATL đã phân lớp ở WP-C5a: `loi_as_is` 928 · `lech_D3` 3.099 · `chua_co_dau_vao` 1.091 · lệch FLS 0 ⇒ dòng PL tính trên ATL sẽ **thừa kế** các lớp này — WP-C5b phải lan nhãn lớp từ ô lá sang dòng PL (một dòng PL lệch vì lá `lech_D3` là `lech_D3`, ⛔ "lệch FLS"); ⛔ gán lớp bằng quy tắc khối × năm (bài học `H12-R1-01`).
- **Hai phép CHECK IX.PL** (C12): ① `NB = 0` · ② `NIS + INT + PIT + COM = CXA + GAH + DC + MC`. DT11 đo trên đáp án Daily Report: ② **0 kỳ cân có số ≠ 0** (mọi kỳ "đạt" là 0 = 0) ⇒ ở H13 tách đếm `dat_co_so` / `dat_0_0` / `do` / `khong_do_duoc`, ⛔ gọi 0 = 0 là "đạt" trơn (Đ3).
- Đáp án dòng PL = các hàng PL2…PL8 (+ KPI) trong `atl.json` (PD 606) — kiểm khoá/nhãn trước khi so.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (H13-B1 · WP-C5b) | dòng PL2…PL8 tính từ IX.PL (C12, ⛔ chép biểu thức) trên ATL của FLS; so dòng PL đáp án theo ô; mẫu số khai TRƯỚC kèm nhãn Đ4 (ô so · khớp · lệch theo lớp THỪA KẾ từ lá · lệch FLS); lệch `mong` hai chiều (Đ5) | `do_hd2.py --goi WP-C5b` + pytest |
| AC-2 | hai phép CHECK chạy MỖI kỳ; in kỳ nào CHECK đỏ có tên (kỳ · phép · chênh); đếm `dat_co_so` · `dat_0_0` · `do` · `khong_do_duoc` | pytest |
| AC-3 | "chứng minh đỏ": đột biến 1 ô lá ATL ⇒ đúng dòng PL + đúng phép CHECK của kỳ ấy ĐỎ; đổi biểu thức IX.PL ⇒ ĐỎ | pytest |
| AC-4 | khối `WP-C5b` trong `hd2_cong.json` theo hợp đồng CG2 (`khop` = ô khớp THẬT, `lech_co_chu_dich` theo lớp), sinh bằng `do_hd2.py --ghi`; `/gates` `HD2_WP_C5B` + cha `HD2_WP_C5`; bài CG2 + `tests/api/test_isp_gates_hd2.py` xanh | pytest |
| AC-5 | chênh định nghĩa PL ATL ↔ Mapping Master (ISP mục 3) hiện có tên trong báo cáo cổng | pytest / BG |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ đọc đáp án làm đầu vào · ⛔ sửa engine H12/C12 (dùng lại) · ⛔ báo cáo trình bày (H14). Ghi kho THẬT: `KHONG`.
- Thiếu đầu vào ⇒ DỪNG báo cần ảnh nào (tiền lệ DT7b). AP/ISP sai dữ liệu ⇒ đo trước, errata v3.1.3 vào BG.
