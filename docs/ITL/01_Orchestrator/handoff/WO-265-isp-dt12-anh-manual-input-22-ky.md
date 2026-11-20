# WO-265 — ISP 3.1.2 · Step 38 · DT12: ảnh Manual input của ITL Ledge — 22 kỳ còn lại

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 20/11 |
| **Phát bởi** | orchestrator *(tài khoản mới)* · 2026-11-20 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT12` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` *(đã gộp DT2 — `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`)* |
| **Dải phiếu** | `BG-266` · `KQ-267` (R1) · `KQ-268` (R2 cuối, cây gộp thử) |

## Vì sao
- ISP **Step 38 · DT12** (wave W12). Phụ thuộc DT2 — đã gộp. Đầu ra là đầu vào của **H15** (Step 43, chế độ tự sinh theo kỳ) → **I1**.
- Review theo **luật B của chủ (18/11)**: 2 vòng *(chữ "R1 · R2 · R3" của ISP là bản cũ)*.

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 38** *(· Step 43 H15 — bên tiêu thụ)* |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §5.3.2 AC10 · AC11 · §5.3.1 HD1 |
| `tests/fixture/itl_ledge_2026_03.json` | **khuôn** — 28 cột của 7 khối + ngày + `itl_id`; ⛔ `Diễn giải`, ⛔ `Số CT`; khoá `nguon · ky · dong_du_lieu_bat_dau · so_dong · ghi_chu · dong` |
| `tools/do_voi_so_luong.py` *(dòng ~596, `_nap("itl_ledge_2026_03.json")`)* | bên đọc ảnh — ảnh mới phải đọc được bằng đúng đường này |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư *(`Email Address` CẤM vào kho/ảnh)* |

## Nguồn — phiên cloud TỰ đọc bằng khoá SA *(CHỈ-ĐỌC)*
- Sổ **ITL Input Transaction Ledger (ADJUSTED)** — tab `ITL Ledge` *(HANDOFF §4.2: SA có quyền Editor ở `1r4Wem…` — vẫn dùng **CHỈ-ĐỌC**, ⛔ ghi/nhận xét)*. Tìm id đầy đủ bằng `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_ds.py`.
- Tab lớn (cỡ 10⁴ dòng; GAP-ORA-08 hết giờ đọc) ⇒ đọc **theo lát hàng**, mỗi lát ≤ 3 lần thử; `UNFORMATTED_VALUE` (⛔ `FORMATTED_VALUE` — bài học DT1b); ngày theo serial → khuôn ngày của ảnh 2026-03.
- **Tên tab/cột khác khuôn, ≥ 2 ứng viên, 403 ⇒ DỪNG**, báo tin nhắn cuối kèm ứng viên *(id + tên tab + kích thước lưới)* + khuyến nghị — ⛔ đoán.
- Bản thô chỉ `/tmp` (chmod 600), xoá sau dùng, ⛔ commit. Dò tiêu đề chỉ in **tên cột**; dữ liệu chỉ ĐẾM.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT12-B1) | ảnh `tests/fixture/dap_an/itl_ledge_<ky>.json` cho các kỳ ≠ 2026-03 *(ISP: 22 kỳ — **đo** số kỳ thật của sổ trước, khai `mong`; khác 22 ⇒ ghi lý do, ⛔ ép)*; **số kỳ đọc được + số kỳ hỏng = số kỳ của sổ**; mỗi kỳ `so_dong` = phân bố kỳ đếm độc lập trên cột ngày của sổ | cổng `dong_bang_sheet.py … --mong` + `tests/du_lieu/test_anh_manual_input.py` | ảnh chưa có |
| AC-2 | kỳ đọc hỏng sau 3 lần thử ⇒ `blocked` **có tên** trong cổng + BG *(⛔ bỏ im, ⛔ ảnh rỗng)*; tập rỗng ⇒ ĐỎ (Đ3) | pytest | — |
| AC-3 | khuôn cột = đúng ảnh 2026-03 *(cùng 28 cột + ngày + `itl_id`, cùng thứ tự/khoá)*; ảnh 2026-03 hiện có **đúng từng byte** | pytest + diff | đổi 1 tên cột ⇒ ĐỎ |
| AC-4 | PII: ảnh ⛔ `Diễn giải` · `Số CT` · `Email Address` · tên người; `python tools/quet_pii_repo.py` = 0 | pytest + công cụ | cấy 1 cột cấm ⇒ ĐỎ |
| AC-5 | `tools/do_voi_so_luong.py` đọc được ít nhất 1 ảnh mới bằng `_nap` *(⛔ chạy tự sinh — việc của H15)* | pytest | — |
| AC-6 | kích thước: tổng ảnh ghi vào BG; ảnh > 2 MB ⇒ nguyên nhân (luật `DT4-R1-07`) | BG | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` | — |

## Ràng buộc
- ⛔ chạy tự sinh / so khớp engine (H15) · ⛔ sửa ảnh 2026-03. Ghi kho THẬT: `KHONG`.
- Chỗ mơ hồ ngoài các mục trên ⇒ phương án hẹp nhất + "Giả định" kèm khuyến nghị vào BG; chỉ DỪNG ở trường hợp nguồn.
