# WO-319 — ISP 3.1.2 · bổ sung (DT13): đóng băng ĐẦU VÀO còn thiếu cho WP-C5a · C5b · C5c (H12 · H13 · H14)

| | |
|---|---|
| **Trạng thái** | `MO` — giao 22/11 ~16:15 UTC |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT13` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT7 · DT7b · DT8/DT8b · DT9/DT9b · DT10 · DT11 · H12; khuôn đóng băng `tools/khuon_dong_bang/*`) |
| **Dải phiếu** | `BG-320` · `KQ-321` (R1) · `KQ-322` (R2 cuối). Số trống kế tiếp sau dải: **323** |

## Vì sao — các bước engine đã DỪNG đúng luật vì thiếu ảnh (đo được)
| Bước | Ô `chua_co_dau_vao` / ô so = 0 | Nguồn AS-IS chưa đóng băng (theo FORMULA bước đã đọc) |
|---|---|---|
| H12 · WP-C5a | **1.091** ô (lá CDT 2025: GI 69 · OMC 70 · PS 51 · SC 57 ô/mã) | hàng `TOTAL <yyyymm>` của `CFA2 \| MID 3 \| GI Platform Data Ledger` (PM gõ tay) · tab `FS1 Daily Report 3` (`BG-292`) |
| H13 · WP-C5b | PL5 chỉ đo GROUP × 12 tháng 2025 — **252** ô PL5 ngoài mẫu số | ảnh COM theo từng khối CDT (`BG-308`) |
| H14 · WP-C5c | 608 · 609 luỹ kế FS1 **8.421 + 8.402** ô · 610 `hr` **1.537** ô · **605 (DR3 Sign off) ô so = 0** (13.706 ô số) · **615 (A-CCR — bản CHÍNH THỨC theo D5) ô so = 0** (48.021 ô số) | 605: nguồn FS1/PLA5 + đường VND · 615: số dư tiền theo LE × ngày · luỹ kế FS1 · HR của DR2 (`BG-312`) |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | **Bước 1 = ĐO, chưa đóng băng:** đọc FORMULA (chỉ đọc) các ô đại diện của từng dòng bảng trên (≥ 3 ô mỗi nguồn) ⇒ bảng "ô đáp án → sổ · tab · vùng nguồn" trong BG; xếp mỗi nguồn: (a) đóng băng được (cùng tài khoản SA, ⛔ PII) · (b) nguồn là bảng gõ tay/ngoài hệ ⇒ đóng băng giá trị có tên · (c) nằm ở sổ ⛔ đọc được ⇒ DỪNG phần ấy, báo | BG |
| AC-2 | đóng băng các nguồn (a)/(b) thành ảnh `tests/fixture/dau_vao/*.json` bằng KHUÔN (mở rộng khuôn sẵn có, ⛔ chép); mỗi ảnh khai `mong` số hàng/ô (Đ5), nhãn từng số (Đ4), checksum TÍNH LẠI; ảnh cũ đúng từng byte | cổng `--mong` + pytest |
| AC-3 | đối chiếu chỉ để ĐO (⛔ đầu vào): với mỗi ảnh mới, dựng lại ≥ 1 nhóm ô đáp án theo công thức đọc được ⇒ khớp/lệch có tên (mẫu số trước — Đ3) — chứng minh ảnh đủ cho bước engine tiêu thụ | BG + pytest |
| AC-4 | PII: bản đồ cột bằng tiêu đề TRƯỚC; ⛔ `Diễn giải` · `Số chứng từ` · tên người · email · ID Payee; số TK cá nhân (gồm dạng `<số>_PO USD_<tên>` — xem `DT11-R2-02`) che `TK_CA_NHAN_n`; ⛔ in số TK; `python tools/quet_pii_repo.py` = 0 trên MỌI commit đã push | pytest + công cụ |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét file của chủ). Bản thô `/tmp` chmod 600, xoá sau, ⛔ commit. ⛔ sửa engine H12/H13/H14 (vòng sau). Ghi kho THẬT: `KHONG`.
- Luật nguồn: tab ⛔ thấy / ≥ 2 ứng viên ⇒ DỪNG báo ứng viên. Phạm vi lớn ⇒ ưu tiên theo thứ tự **615 (A-CCR) → 605 → MID3 TOTAL → luỹ kế FS1 → HR DR2 → COM theo CDT**; hết thời gian ⇒ bàn giao phần đã xong + bảng phần còn lại (⛔ làm dở im lặng).
