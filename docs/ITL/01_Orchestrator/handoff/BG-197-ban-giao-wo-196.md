# BG-197 — Bàn giao WO-196 · ISP Step 27 · DT10 · ảnh IX.DRV + đáp án ATL (604 · 606)

| | |
|---|---|
| Phát bởi | fls-dev #DATA (phiên cloud) · 2026-11-18 · nhánh `isp/DT10` (nền `fba4849`) |
| Gửi | fls-test (R1) |

## Đã làm
Hai khuôn MỚI (tệp riêng, AC-5) + hai ảnh + một tệp bài. **⛔ sửa công cụ chung** `tools/dong_bang_sheet.py` (sha256[:16] `ae917adbf80b1c14` ghim bằng bài) ⇒ mọi ảnh cũ đúng từng byte.
`tools/khuon_dong_bang/ix_drv.py` → `tests/fixture/cau_hinh/ix_drv.json` (235.697 B) · `…/atl.py` → `tests/fixture/dap_an/atl.json` (1.571.277 B ≈ 1,6 MB < 2 MB) · `tests/du_lieu/test_dap_an_atl.py` (29 bài). ⛔ ghi kho thật · ⛔ di trú.

## Nguồn (khoá SA chỉ-đọc, `UNFORMATTED_VALUE`; công thức `FORMULA`) — MỘT ứng viên, ⛔ phải hỏi
Sổ `19NNTbXJ6SmwA8AFnaUQlc0-WKjM_YPAkUaa2-shEU2g` = `[COPY] Report I General Ledger | P&L Report` (khớp tên AP; 1 sổ có chuỗi `P&L Report` trong 200 sổ SA liệt kê (pageSize 200)).
| Vật | Tab · vùng đọc |
|---|---|
| IX.DRV · PD 604 | `Allocation Table \| By NOEM & By GI` (1000×26) `A1:Z35` — GI-PE h3–12 · GI-PM h14–23 · NOEM h25–35 |
| NB theo LE | `Allocation Table \| NB \| By LE` (919×27) `A1:Q918` — BALANCE h5–308 · CREDIT h310–613 · DEBIT h615–918 |
| NOEM (ô cứng) | `[H1.2026][2025]H1000 I HR Report` `A4289:Q4300` |
| ATL · PD 606 | `Report I PLA3 Y H Q M \| PM + HR \| ATL` (1110×196) `B5:BK1110` |
Bản thô `/tmp/dt10` (chmod 600), ⛔ commit; ⛔ đọc Diễn giải / Số chứng từ / Email / tên người.

## DT10-B1 · lưới driver **x/4 × y/8 × z/12** thực đo (Đ4 — mỗi số một nhãn)
AP khai 4 loại × 8 CDT1 × 12 tháng = **384 ô**. Nguồn có **238** ô SỐ ⇒ **3/4 loại × 7/8 CDT1 × 11–12/12 tháng**. **146** ô thiếu, MỖI ô có tên (bảng phụ `o_thieu`, 146 dòng; cổng so HAI chiều):
- **NB_LE 96** = 8 CDT1 × 12 — NB khoá theo LE (`From × To`), ⛔ theo CDT1. Ảnh giữ BALANCE 304 hàng ở phụ `nb_le` (16 From × 19 To); BALANCE = CREDIT − DEBIT lệch lớn nhất 1E-17 (CREDIT/DEBIT ⛔ mang).
- **CMN 36** = 3 driver × 12 — CMN ⇒ SHQ1 theo CDT Correct; ở NOEM headcount CMN (`A4300`) ⛔ vào ô nào, rơi vào phần dư SHQ2 (`=100% − Σ`). **Khuyến nghị orchestrator:** AP §3.2.2 "8 CDT1" nên ghi "7 + CMN gộp".
- **GI 202501 14** = 2 driver (PE · PM) × 7 CDT1 — GI = `SUMIFS` trên `CFA2 | MID 3 | GI Platform Data Ledger` dòng `TOTAL <yyyymm>`, MID3 chỉ có 11 dòng TOTAL (202502…202512) ⇒ `iferror` ⇒ rỗng.
Mẫu số (Đ3): 34 tổng Σ7 CDT1 (NOEM 12 + GI-PE 11 + GI-PM 11) đều = 100 % ±1e-9. Ô `>1` hay `<0` thật: **0** (số `1,88…` thấy lúc đầu là `…E-05` cắt chuỗi). **Chỉ 2025:** tiêu đề 3 bảng + NB đều 2025, `P:Z` hàng 1–35 = 0 ô ⇒ cổng cột `nam`/`ngoai` ĐỎ nếu khác ⇒ 2026 ⛔ có ở nguồn.
Phá nguồn đã chạy: mất ô · lấp ô mong-thiếu · thêm hàng CMN · `nam=2026` · `ngoai=3` · Σ≠100 % · tập rỗng ⇒ ĐỎ có tên (8 bài). Lúc chưa có khuôn/ảnh: **29 failed** (tệp bài viết trước).

## AC-2 · nguồn ô NOEM (phụ `nguon_noem`, 96 dòng = 8 hàng × 12 tháng)
Mỗi dòng: ô (`D27…O34`) · tab · công thức GỐC nguyên chuỗi · ô HR của tử/mẫu · giá trị tử/mẫu. **84** ô trỏ `'[H1.2026][2025]H1000 I HR Report'!$A$4289:$Q$4300`: Group (12) = `GAG`/`GAG`; CVL·COR·CSM·CAH·ASA·SHQ1 (72) = `INDEX/MATCH(LEFT($C,3)…)` ÷ `GAG` (`A4292`), cột tháng khớp tiêu đề `1…12`+`2025` ở hàng 4289 (cột F…Q). `SHQ1` khớp hàng `SHQ` ĐẦU (`A4293`) — hàng `SHQ` thứ hai (`A4294`) = SHQ2 mà ⛔ công thức nào dùng. **12** ô SHQ2 = `100% − SUM(D28:D33)`. Tử/mẫu tái dựng 72 ô NOEM, lệch lớn nhất 4,5E-17. Ô GI: nguồn = `CFA2 | MID 3 | GI Platform Data Ledger` cột O/S·U·W·Y·AA·AC (PE) · P/T·V·X·Z·AB·AD (PM), ghi ở `ghi_chu_khuon`.

## AC-3/4 · ATL (PD 604 · 606)
- **829** hàng dữ liệu (sheet 8…1030) × **57** cột kỳ (2024·2025·2026 × Y·H1·H2·Q1…Q4·M01…M12). Số hàng CÓ giá trị theo kỳ (cổng `MONG_KY`, hai chiều): 2024 = 7×**824** (Y·H1·H2·Q1–4) + 12×**816** (tháng) · 2025 = 19×**824** · 2026 = 7×**824** + 12×**816**. Phá: mất một ô / thêm một ô ⇒ ĐỎ ghi tên cột.
- PD 604 số hàng CDT1 có số theo tháng (phụ `pd604_ky`): NOEM 7 ×12 · GI-PE/PM `0` ở 202501 rồi 7 (Đ3: `0` là kết quả, khớp chéo `ix_drv`).
- **D2:** AS-IS CHƯA phân bổ (`N1` + 8 ô cùng hàng "Cần add Formula Allocate") ⇒ ATL = đáp án khi cờ TẮT; ATL 2026 "chỉ đối chiếu khi cờ tắt (D2)" (ghi ở ảnh + bài).
- **Lỗi ghi NGUYÊN, đếm theo cột, ghim phân bố:** 161 ô = `y2024_y` **77** `#N/A` (đuôi giải thích ghi nguyên) + `y2024_q1…q4` **21** `#VALUE!` mỗi cột; 53 cột còn lại khai `0`. Khối KIỂM sheet 1031…1110 (80 hàng ⇒ phụ `kiem`): **560** `#VALUE!` + **1.997** ô TRUE/FALSE.
- **120** ô gạch `-` (5 hàng 998–1002 × 24 cột) ⇒ RỖNG ở bảng chính + liệt kê ở phụ `o_gach`.
- ⛔ mang: cột `A` (số tổng) · 7 khối 2027…2033 (từ 2028 có 84 ô `#REF!`/khối). Muốn đối chiếu ATL 2027+ ⇒ phiếu mới.
- PII: 0 cột `Email Address`; ảnh chỉ nhãn KRF + số; bài ghim "Email Address" chỉ nhắc 1 lần (câu khai) và 0 ký tự `@`; ca phá `Email Address` ở `cot` ⇒ TỪ CHỐI exit 2, ⛔ in giá trị.

## Kích thước · sàn Q8 · cổng cuối
`ix_drv.json` 235.697 B · `atl.json` 1.571.277 B — đều < 2 MB (nguyên nhân cỡ ATL: 829 × 62 cột + khối KIỂM 80 × 62, mỗi ô nguyên chữ số).
`MONG_PYTEST_TOAN_BO` **3557 → 3588** (+29 bài mới; nền `fba4849` đo thu thập **3559**, tức hằng cũ đã lệch 2 từ trước — nâng về số thu thập của cây) + bài ghim `test_dung_moi_truong_isp.py` cùng commit; web 675 giữ.
`--duong-nen --cong 5437` (một lần, một mình): **ĐẠT** — toàn bộ `12 failed, 3560 passed, 2 xfailed, 14 errors`: tập đỏ + XFAIL 28 = 28 node id (thêm 0 · bớt 0), chạy 3588 (mong ≥ 3588); `tests/web` 3 = 3, chạy 675. `lint-imports` 11 kept / 0 broken. `kiem_tai_lieu` ĐẠT sau khi thoát `\|` ở bảng nguồn (lần đầu ĐỎ K3 3 lỗi — dấu `|` trần).

## Việc cần orchestrator quyết
1. AP §3.2.2 "8 CDT1" ↔ nguồn 7 + CMN gộp SHQ1 (khuyến nghị: sửa chữ AP, giữ cổng).
2. Công cụ chung `LOI_MONG`: thiếu khoá một cột `so!` ⇒ `KeyError` ở dòng tổng kết (`dong_bang_sheet.py:866`, SAU khi ảnh đã ghi) — khuôn `atl` khai đủ 57 cột để tránh; ⛔ sửa công cụ ở bước này. Khuyến nghị: bước nhỏ riêng nếu muốn `.get(c, 0)`.
