# WO-137 — ISP 3.1.2 · Step 15 · DT5: ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Opus 4.8 · medium) · cụm PG **5436** · nhánh `isp/DT5` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT2 · DT3 · DT4 — công cụ đóng băng + khuôn, hợp đồng bản thô = LƯỚI SA) |
| **Dải phiếu** | `BG-138` · `KQ-139` (R1) · `KQ-140` (R2) · `KQ-141` (R3). Số trống kế tiếp: **142** |

## Vì sao
- ISP **Step 15 · DT5** — nguồn sự thật duy nhất (Goal · Scope · DT5-B1/B2 · mục 8). Phụ thuộc DT3: đã gộp.

## Spec phải đọc
| Tệp | Mục |
|---|---|
| ISP v3.1.2 | §1 · §2.1 · **Step 15** (· Step 10 DT3 · Step 12 DT4 làm mẫu) |
| AP v3.1.2 | §3.3.x PD 409–411 (CFA1 Daily · Y/H/Q/M) — xác định sheet NGUỒN chính xác trước khi đọc |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` (`gl_406.py`, `atl_cay.py`) | khuôn mẫu: lưới SA, đọc theo lát, `mong`, bảng phụ, quét PII |
| `tests/fixture/cau_hinh/atl_cay.json` | cây ATL 74 dòng mã — DT5-B1 đòi mọi mã HD ∈ cây |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư |

## Nguồn (người dùng duyệt 17/11: phiên cloud DATA tự đọc bằng khoá SA chỉ-đọc)
- Bản sao `[COPY] Report I General Ledger | P&L Report` · id `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` — các sheet `Report I PLA1/PLA3 … Daily …` · `… Y H Q M …` (đo 17/11: lưới ~1.027 × 502). Xác định đúng 409/410/411 theo AP trước; ⛔ đoán — mơ hồ ⇒ hỏi kèm khuyến nghị.
- Khoá ở `FLS_GSHEETS_SA_JSON_B64`/`FLS_GSHEETS_SA_JSON` (⛔ in); Sheets API v4 `UNFORMATTED_VALUE` · `SERIAL_NUMBER`; script mẫu `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_lay.py`; bản thô chỉ ở `/tmp` (⛔ commit); ⛔ đọc cột/ô mang tên người, email, Diễn giải, Số chứng từ.

## Tiêu chí nghiệm thu
| AC | Mong |
|---|---|
| AC-1 (DT5-B1) | `tests/fixture/dap_an/cfa1_daily.json` (HD × ngày) + `cfa1_yhqm.json` (HD × kỳ Y/H/Q/M); mọi mã HD ∈ cây ATL; số cột ngày = số ngày từ 21/10/2024 tới ngày đọc (khai ngày đọc) |
| AC-2 (DT5-B2) | phá: đổi 1 mã HD lạ ở BẢN SAO ⇒ ĐỎ; trả nguyên ⇒ xanh, đúng từng byte |
| AC-3 | ô công thức lỗi ở nguồn (`#REF!`, `#N/A`…) ghi nguyên dạng chuỗi, ĐẾM + khai, ⛔ đổi thành 0 |
| AC-4 | đọc theo lát; lát rỗng/hỏng ⇒ ĐỎ; quét PII có ca phá |
| AC-5 (Q8) | sàn + bài ghim cùng commit |

## Dữ liệu
- Ghi kho THẬT: `KHONG`.
