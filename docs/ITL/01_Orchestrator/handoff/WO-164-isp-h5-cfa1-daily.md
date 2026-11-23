# WO-164 — ISP 3.1.2 · Step 16 · H5: SO.CFA1 Daily — Σ theo (HD, ngày) trên cây IX.HD (cổng WP-C3a)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 — **Opus 5.5** (`claude-opus-5-5`) medium: bước engine khó (luật A, người dùng 18/11) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-HC** · cụm PG **5435** · nhánh `isp/H5` |
| **Nền** | ngọn nhánh làm việc (đã gộp H4 — `tinh_gl` + `do_hd2.py` WP-C2; C4 — cây `fls/cau_hinh/hd.py`; C5 — kho config; DT5 — đáp án `cfa1_daily.json`) |
| **Dải phiếu** | `BG-165` · `KQ-166` (R1) · `KQ-167` (R2 cuối). Số trống kế tiếp: **168** |

## Spec
ISP **Step 16** (nguồn sự thật) · AP §3.3.1 PD 409 · §3.2.4 "cây HD theo vị trí dòng, cha = SUM con" · WP-C3 · khuôn H4 (`tools/do_hd2.py --goi WP-C2`, `docs/ITL/_tools/hd2_cong.json`, dung sai theo cột có căn cứ đo, MONG khai trước, mẫu số khoá).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 (H5-B1) | cây 3 nút tổng hợp ⇒ cha = Σ hai con (engine tính, ⛔ đọc cha từ đáp án) | đơn vị — ĐỎ trước |
| AC-2 (H5-B2) | `do_hd2 --goi WP-C3a`: ô lá = Σ mUSD Nợ − Σ mUSD Có theo (LE, HD Final, ngày); ô cha = Σ con theo cây ⇒ so với `tests/fixture/dap_an/cfa1_daily.json` (370 hàng = 5 LE × 74 mã · 760 cột ngày); **mẫu số khai trước** (ô so > 0, Đ3), lệch có tên = MONG (Đ5 hai chiều) | cổng + pytest |
| AC-3 | dung sai theo cột/khối có CĂN CỨ ĐO (luật `H4-R1-01`/`R2-01`): khai số đo; đột biến 1 ô lá ⇒ đúng ô ấy + các cha ĐỎ | pytest |
| AC-4 | ⛔ vòng tròn: đầu vào chỉ là dòng sổ (CA.GL của H4) + cây C4 + tỷ giá; đáp án 409 chỉ cấp giá trị mong | pytest đột biến đầu vào |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` MỘT lần cuối |

## Lưu ý orchestrator
- **Trục ngày:** errata ㉑ — đáp án 409 bắt đầu **2024-10-20** (⛔ 21/10); 760 = cột ≤ ngày đọc; ngày có số cuối 2026-11-11 (7 cột cuối là "chưa có số", ⛔ "0 đã chốt"). ISP: ngày đầu lấy TẠM từ tham số tới H6 (C6 lưu 21/10 trong kho) ⇒ H5 đọc mốc từ ảnh đáp án; khai rõ chênh 20/21 trong BG.
- **Đầu vào theo dòng** (HD Final, LE, ngày, tiền): ưu tiên ảnh đã có trong repo (`gl_406_dau_vao.json` của H4 · `itl_ledge_adjustment.json` · `gl_406.json`). Nếu thiếu trường nào để nối dòng ↔ (LE, HD) mà KHÔNG dùng đáp án ⇒ **DỪNG, báo** bằng số đếm (⛔ đoán, ⛔ đọc đáp án làm đầu vào).
- 5 số dư đầu kỳ (H4) chỉ áp cho tồn GL; CFA1 Daily là phát sinh theo ngày — khai rõ có/không dùng.

## Dữ liệu
Ghi kho THẬT: `KHONG`. ⛔ Drive (đáp án đã đóng băng trong repo).
