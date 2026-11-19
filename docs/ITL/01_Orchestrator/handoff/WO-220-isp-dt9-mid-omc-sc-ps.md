# WO-220 — ISP 3.1.2 · Step 34 · DT9: ảnh đáp án MID1–MID3 của OMC · SC · PS

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 19/11 ~02:30 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-19 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5445** · nhánh `isp/DT9` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT8 + DT8b — khuôn MID GI có khoá `vendor`/`thang`; công cụ chung `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`) |
| **Dải phiếu** | `BG-221` · `KQ-222` (R1) · `KQ-223` (R2). Số trống kế tiếp: **224** |

## Vì sao
- ISP **Step 34 · DT9** (wave W11). Phụ thuộc DT8 (đã gộp). Đầu ra là đáp án cho **H11** (AL.PLT · OMC · SC · PS).
- ⭐ Bài học H9/H10: ảnh MID phải mang **khoá Vendor/tháng** (DT8b) và **cột thượng nguồn** đủ cho engine (H10 dùng MID1 cột T làm PE theo CDT1 — chứng minh ⛔ vòng tròn bằng `FORMULA`). Làm ĐÚNG ngay từ đầu cho OMC · SC · PS.

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 34** (· Step 19 DT8 · Step 35 H11 để biết đầu ra dùng làm gì) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.4.1 PD **508–510** · **600–603**; lỗi `row[45]` của script OMC | 3.1.2 |
| `BG-148` · `BG-205` · `BG-217` · khuôn `tools/khuon_dong_bang/` của MID GI | khuôn + bài học | nền |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA
- Tab MID1–MID3 của OMC · SC · PS theo tên AP. Tìm bằng `sa_ds.py` + `sa_meta.py` (`docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/`); ưu tiên bản `[COPY]`. **Tên không khớp AP, ≥ 2 ứng viên, hoặc 403 ⇒ DỪNG, báo ứng viên (id + tên + kích thước lưới) và khuyến nghị** — ⛔ đoán.
- Đọc GIÁ TRỊ bằng `UNFORMATTED_VALUE`; công thức cột thượng nguồn bằng `FORMULA` (`sa_cong_thuc.py`).
- ⛔⛔ PII: lập bản đồ cột bằng hàng tiêu đề TRƯỚC; chỉ đọc cột khoá (Vendor ID · tháng · No · ITL ID) + số tiền + cột thượng nguồn; ⛔ Số CT · Diễn giải · Tài khoản · tên người · email. Bản thô `/tmp` (chmod 600), xoá sau dùng, ⛔ commit.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT9-B1) | `tests/fixture/dap_an/{omc,sc,ps}_mid{1,2,3}.json` (9 ảnh); PS thiếu ĐÚNG 7 tháng 03–09/2026 — cổng IN rõ, ⛔ lấp; còn lại số dòng theo tháng khai MONG (Đ5 hai chiều; rỗng ⇒ ĐỎ, Đ3) | cổng `dong_bang_sheet.py … --mong` + pytest | ảnh chưa có |
| AC-2 | mỗi ảnh MID3 mang khoá **vendor** + **thang** (như DT8b); MID1 mang cột thượng nguồn engine cần + bằng chứng `FORMULA` ⛔ tham chiếu MID2/MID3 (khai trong BG) | pytest + BG | — |
| AC-3 | cờ `nguon_nghi_loi` cho OMC (lỗi `row[45]` của script — AP §3.4.1): đo phạm vi ảnh hưởng (hàng · cột · số ô) và khai | pytest + BG | — |
| AC-4 | `#REF!`/`#N/A` ghi NGUYÊN chuỗi, ĐẾM theo cột (luật `DT5-R1-04`); PM chữ (`Need to manual input`) tách sang cột ghi chú, ⛔ hoá 0 (như DT8b) | pytest | — |
| AC-5 | PII: máy quét có ca phá; lời lỗi ⛔ in giá trị ô; cột vendor chỉ khớp mẫu mã (⛔ tên người) | pytest | — |
| AC-6 | khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; ⛔ sửa công cụ chung trừ khi bài đòi (mọi ảnh cũ đúng từng byte) | diff | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Ảnh BG ghi kích thước + NGUYÊN NHÂN nếu > 2 MB (luật `DT4-R1-07`).

## Câu còn treo
- không có.
