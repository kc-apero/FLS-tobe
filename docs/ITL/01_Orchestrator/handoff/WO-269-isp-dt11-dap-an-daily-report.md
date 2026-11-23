# WO-269 — ISP 3.1.2 · Step 41 · DT11: ảnh đáp án Daily Report 2 · 3 (PD 607–616)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 20/11 |
| **Phát bởi** | orchestrator *(tài khoản mới)* · 2026-11-20 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT11` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` *(đã gộp DT2 — `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`)* |
| **Dải phiếu** | `BG-270` · `KQ-271` (R1) · `KQ-272` (R2 cuối, cây gộp thử) |

## Vì sao
- ISP **Step 41 · DT11** (wave W13). Phụ thuộc DT2 — đã gộp. Đầu ra là đáp án của **H14** (Step 46, engine Daily Report) → **I2**.
- Review theo **luật B của chủ (18/11)**: 2 vòng.

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 41** |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.3.2 PD **605–617** · §3.5.3 **D5** *(bản A-CCR)* · IX.PL `CHECK` |
| `tools/khuon_dong_bang/*.py` · `BG-193` (DT6) · `BG-221` (DT9) | khuôn đóng băng |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA *(CHỈ-ĐỌC)*
Tên theo AP §3.3.2 *(đối chiếu tên thật)*:

| PD | Sổ › tab |
|---|---|
| 605 | P&L Report › `[MID][FS1][PLA5]5. Daily Report 3 (Sign off)` |
| 607 · 608 · 609 | P&L Report › `[FS2]5. Daily Report 3` · … · `5. Daily Report 3` *(bản chính 609)* |
| 610 | CF report › `5. Daily Report 2` |
| 614 · 615 · 616 | `A-CCR_V2_Working` › `9.2.Exchange Rate` · `5. Daily Report` · `6. CCR I DEL I W I Pdf` |

- `daily_report_3.json` = bản **[MID][FS1][PLA5] Sign off** *(ISP mục 3)*; `daily_report_2.json` = Daily Report 2. Bản A-CCR (D5) dùng để **đối chiếu** — khai số ô khớp/lệch giữa bản gốc và A-CCR nếu đọc được, ⛔ đóng băng thành ảnh thứ ba nếu không cần.
- **Không tìm thấy / ≥ 2 ứng viên / 403 ⇒ DỪNG**, báo tin nhắn cuối kèm ứng viên *(id + tên tab + kích thước lưới)* + khuyến nghị — ⛔ đoán. *(Tiền lệ 20/11: DT7 dừng vì 6 tab PLA không có trong 67 sổ SA thấy.)*
- `UNFORMATTED_VALUE`; công thức hàng mẫu ghi nguyên văn vào BG. Bản thô `/tmp` (chmod 600), xoá sau dùng.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 | 2 ảnh `tests/fixture/dap_an/daily_report_2.json` · `daily_report_3.json` theo **(dòng PL, ngày/kỳ)**; số dòng · cột · ô ≠ 0 khai `mong` trước (Đ5; tập rỗng ⇒ ĐỎ, Đ3); nhãn từng số (Đ4) | cổng + `tests/du_lieu/test_dap_an_report.py` | ảnh chưa có |
| AC-2 (DT11-B1) | hai phép **CHECK của IX.PL** trên chính đáp án: `NB = 0` và `NIS + INT + PIT + COM = CXA + GAH + DC + MC` — **số kỳ đạt** đo lần đầu rồi khai `mong`, liệt kê kỳ không đạt *(kỳ · chênh)* | pytest | đột biến 1 ô ⇒ ĐỎ *(chứng minh, ghi BG)* |
| AC-3 | ô ATL `AH12` "− 0.5" chỉnh tay ⇒ ghi là **ô chỉnh tay** có tên trong ảnh *(⛔ config)* | pytest | — |
| AC-4 | dải ngày/kỳ thật của nguồn khai trong ảnh + BG; kỳ thiếu ⇒ `chua_co_du_lieu` có tên | pytest | — |
| AC-5 | `#REF!`/`#N/A` ghi NGUYÊN chuỗi, ĐẾM theo cột (luật `DT5-R1-04`); lời lỗi ⛔ in giá trị ô | pytest | — |
| AC-6 | khuôn mới = tệp riêng; mọi ảnh cũ đúng từng byte; `python tools/quet_pii_repo.py` = 0 | diff + công cụ | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` | — |

## Ràng buộc
- ⛔ engine RP (H14) · ⛔ PDF. Ghi kho THẬT: `KHONG`.
- Chỗ mơ hồ ngoài các mục trên ⇒ phương án hẹp nhất + "Giả định" kèm khuyến nghị vào BG; chỉ DỪNG ở trường hợp nguồn.
