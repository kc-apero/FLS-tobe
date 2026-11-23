# WO-196 — ISP 3.1.2 · Step 27 · DT10: ảnh IX.DRV (Allocation Table) + đáp án ATL (PD 604 · 606)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~20:35 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5437** của phiên ấy · nhánh `isp/DT10` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT2…DT5 · DT8 · C11 — công cụ chung `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`) |
| **Dải phiếu** | `BG-197` · `KQ-198` (R1) · `KQ-199` (R2). Số trống kế tiếp: **200** |

## Vì sao
- ISP **Step 27 · DT10** (wave W9) — nguồn sự thật duy nhất. Phụ thuộc Step 8 · DT2 (đã gộp). Đầu ra là đầu vào driver + đáp án cho H12 (AL.KEY).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 27** (· Step 19 DT8 · Step 25 C11 làm khuôn) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.2 IX.DRV · §3.4.2 PD 500 · 511–513 · **604 · 606** | 3.1.2 |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` · `fls/cau_hinh/` (C11 IX.ALR: 17 HD = 4 H1000 + 8 By GI + 5 By NOEM) | khuôn + luật đã gộp | nền |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA
- Sheet **Allocation Table** (IX.DRV) và **ATL** PD 604 · 606 theo tên AP. Tìm bằng `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_ds.py` + `sa_meta.py`; ưu tiên bản `[COPY]`. **Tên không khớp AP, ≥ 2 ứng viên, hoặc 403 ⇒ DỪNG, báo bằng tin nhắn cuối kèm danh sách ứng viên (id + tên + kích thước lưới) và khuyến nghị** — ⛔ đoán.
- Đọc GIÁ TRỊ bằng `UNFORMATTED_VALUE`; công thức bằng `FORMULA` (`sa_cong_thuc.py`) để ghi nguồn ô NOEM.
- ⛔ PII: ⛔ đọc cột Diễn giải · Số chứng từ · Email · tên người · số tài khoản cá nhân. Bản thô chỉ `/tmp` (chmod 600) — ⛔ commit.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT10-B1) | `tests/fixture/cau_hinh/ix_drv.json`: **4** loại driver (NOEM · GI theo PE · GI theo PM · NB theo LE) × **8** CDT1 × **12** tháng 2025 — lệch ⇒ khai CÓ TÊN từng ô thiếu/thừa, ⛔ lấp (Đ4: số nào đếm gì); cổng khẳng định driver chỉ có 2025 | cổng `dong_bang_sheet.py … --mong` + pytest | ảnh chưa có |
| AC-2 | NOEM trỏ ô cứng của H1000: ghi NGUỒN từng ô (tab + địa chỉ + công thức gốc) trong ảnh hoặc BG | pytest + BG | — |
| AC-3 | `tests/fixture/dap_an/atl.json` (604 · 606): số dòng theo kỳ khai MONG trước (Đ5 hai chiều; tập rỗng ⇒ ĐỎ, Đ3); ATL 2026 khai rõ "chỉ đối chiếu khi cờ tắt (D2)" | cổng + pytest | — |
| AC-4 | `#REF!`/`#N/A` ghi NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố (luật `DT5-R1-04`); PII máy quét có ca phá | pytest | — |
| AC-5 | khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; sửa công cụ chung chỉ khi bài đòi (mọi ảnh cũ đúng từng byte) | diff | — |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Ảnh BG ghi kích thước + NGUYÊN NHÂN nếu > 2 MB (luật `DT4-R1-07`).

## Câu còn treo
- không có.
