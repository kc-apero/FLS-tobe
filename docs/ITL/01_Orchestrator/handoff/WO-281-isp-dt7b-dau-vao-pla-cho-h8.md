# WO-281 — ISP 3.1.2 · bổ sung DT7 (DT7b): ảnh ĐẦU VÀO PLA (GL sổ P&L + HR For PL Report, có cột ngày PL) cho H8

| | |
|---|---|
| **Trạng thái** | `MO` — giao 22/11 ~04:50 UTC |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT7B` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT7 — ảnh đáp án PLA 414–419 + `tools/khuon_dong_bang/_pla.py`; DT6 · DT6b · DT6c — khuôn `hr_ledger_2024`/`2025`; ảnh `dau_vao/gl_406_dau_vao` · `gl_cf_dau_vao`) |
| **Dải phiếu** | `BG-282` · `KQ-283` (R1) · `KQ-284` (R2 cuối). Số trống kế tiếp sau dải: **285** |

## Vì sao
- H8 (`WO-277`, Opus) **DỪNG đúng luật AC-2** sau ~2 phút (phiên `session_01Ci2qSLDjoj4JxiT7Kz1z47`, ⛔ commit). Đo của H8:
  - Đáp án PLA1 (414) = `SUMIFS(GL!$BR, GL!$DE, <ngày>, GL!$V, <mã HD>) − SUMIFS(GL!$BS, …)` trên tab `Report I General Ledger` của sổ **P&L Report** (7.883 dòng). Ảnh đầu vào hiện có: `gl_406_dau_vao` chỉ có cột `A·D·E·F·R` (⛔ `V` HD Final · ⛔ `P` LE · ⛔ `DE`); `gl_cf_dau_vao` là sổ **CF** (12.385 dòng), ⛔ `DE`.
  - Dựng lại `DE` từ ITL Ledge (`svc_start` → ngày 1) chỉ khớp **78/1.227** ô ≠ 0 khối GROUP 414; **454/1.227** ô ≠ 0 nằm ở ngày ≠ ngày 1 ⇒ `DE` ⛔ chỉ là "ngày 1 tháng PL start" ⇒ phải đọc từ sổ.
  - HR (416): đọc tab `Report I H1000 Ledge (HR Allocate HD) Y2025 | For PL Report` qua cột `BM`; ảnh `hr_ledger_2025` chỉ có `ky` (tháng cột A), ⛔ `BM`.
- Tiền lệ bước dữ liệu nhỏ mở khi engine thiếu đầu vào: DT8b · DT9b · DT6b · **DT6c** (cho H7).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | đọc CÔNG THỨC (FORMULA, chỉ đọc) trước: `DE10` (+ 2 ô `DE` khác ở hàng ngẫu nhiên có ngày ≠ ngày 1) tab `Report I General Ledger` sổ `[COPY] Report I General Ledger \| P&L Report` `19NNTb…`; `BM10` (+ 2 ô khác) tab HR For PL Report. Chép nguyên văn vào BG; xác định **cột NGUỒN** mà `DE`/`BM` tham chiếu | BG |
| AC-2 | ảnh `tests/fixture/dau_vao/gl_pl_dau_vao.json`: tab GL sổ P&L, hàng dữ liệu đầy đủ (H8 đo 10…7892 — đo lại, khai `mong` số hàng), cột `A·D·E·F·P·R·V` + `BR`·`BS` + **`DE`** + các cột NGUỒN của `DE` (AC-1). MỞ RỘNG khuôn sẵn có của `gl_406_dau_vao` (⛔ chép); mọi ảnh cũ đúng từng byte | cổng `--mong` + pytest |
| AC-3 | ảnh `tests/fixture/dau_vao/hr_pl_dau_vao.json`: tab HR For PL Report, cột `A·V·BA·BB·BM` + LE + cột NGUỒN của `BM`; khuôn mở rộng `hr_ledger_*` (⛔ chép); `mong` số hàng theo kỳ | cổng `--mong` + pytest |
| AC-4 | đối chiếu chỉ để ĐO (⛔ đầu vào): Σ theo (mã HD `V`, ngày `DE`) của `BR − BS` trên ảnh mới so với ô `la` khối GROUP của `pla1_daily` (414) — số ô so · khớp · lệch có tên; tương tự HR (`BM`) với `pla3_hr_daily` (416). Đếm mẫu số trước (Đ3) | BG + pytest |
| AC-5 | PII như DT6b/DT6c: bản đồ cột bằng hàng tiêu đề TRƯỚC; chỉ đọc cột khai ở AC-2/AC-3; ⛔ `Diễn giải` · `Số chứng từ` · tên người · email · ID Payee; TK cá nhân che `R`; ⛔ in giá trị số TK ra log/BG; `python tools/quet_pii_repo.py` = 0 **trên mọi commit đã push** | pytest + công cụ |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- Khoá SA CHỈ-ĐỌC (⛔ ghi/nhận xét file của chủ). Bản thô `/tmp` (chmod 600), xoá sau dùng, ⛔ commit. ⛔ sửa mã engine/khuôn đáp án DT7. Ghi kho THẬT: `KHONG`.
- Luật nguồn: tab ⛔ thấy / ≥ 2 ứng viên ⇒ DỪNG báo ứng viên (⛔ đoán). Ảnh > 2 MB ⇒ khai (`DT4-R1-07`).
- Cột NGUỒN của `DE`/`BM` nằm ở tab/sổ khác ⇒ ghi tên + vùng vào BG, đóng băng nếu cùng sổ và ⛔ PII; khác sổ ⇒ báo, ⛔ tự mở rộng.
