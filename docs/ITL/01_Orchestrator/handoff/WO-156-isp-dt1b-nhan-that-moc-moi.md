# WO-156 — ISP 3.1.2 · Step 5 · DT1b: lượt nhãn THẬT trên MỐC MỚI 18/11 (ảnh 26/08 giữ cho oracle khác)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud **Sonnet 5.5** medium · cụm PG **5437** · nhánh `isp/DT1BM` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT1a · DT1b · DT1BT — `tools/phan_loai_ly_do.py` · `tools/xuat_khoa_dt1b.py`) |
| **Dải phiếu** | `BG-157` · `KQ-158` (R1) · `KQ-159` (R2 cuối). Số trống kế tiếp: **160** |

## Vì sao
- Người dùng 18/11: tệp `[Master] ITL_Ledge_raw.xlsx` (ảnh 26/08) **không còn**; lịch sử phiên bản sổ ADJUSTED gốc chỉ còn từ 02/10 ⇒ chốt **"lấy bản hiện tại, đừng chấp niệm bản cũ"** + **phương án A**: mốc mới CHỈ cho lượt nhãn DT1b; ảnh 26/08 (`tests/fixture/itl_ledge_adjustment.json`, 9.967 dòng — mốc của 28 tệp mã/bài) **giữ nguyên**.
- Người dùng cho orchestrator chạy trên dữ liệu thật; **kết quả gửi người dùng kiểm lại trước khi gộp**.

## Nguồn (khoá SA chỉ-đọc; env `FLS_GSHEETS_SA_JSON_B64`/`FLS_GSHEETS_SA_JSON`; `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`; python `-I`)
| Phía | Nguồn | Đo 18/11 |
|---|---|---|
| **SO** | tệp CSV trên Drive `1U-IQVOXBbGE6X6n0i0mi3IG9VWc9J_Ap` (*"ITL I Input Transaction Ledger File 2_2 (ADJUSTED) - ITL Ledge.csv"*, người dùng tải từ trình duyệt 18/11 09:29) — tải bằng Drive API `files.get?alt=media` scope `drive.readonly` | 10.606.726 B · 12.621 hàng CSV · tiêu đề hàng **7** (`Ngày chứng từ` · `Số chứng từ` · `Diễn giải` · `Đơn vị tiền tệ` · `PS Nợ` · `PS Có` · `Tài khoản` …) · dữ liệu từ hàng **10** |
| **L1** | sổ RAW gốc `1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU`, tab `Transaction Mapping L1` — Sheets API, ĐỌC CHỈ cột `B` `D:G` (⛔ `C` Diễn giải); tiêu đề hàng 3, dữ liệu từ hàng 4 | đọc ~2 s |
- ⛔⛔ PII: bản thô CHỈ ở `/tmp` của phiên (chmod 600), XOÁ khi xong; ⛔ commit; ⛔ in giá trị ô (chỉ số đếm); ⛔ đọc/giữ cột Diễn giải.

## Phạm vi
1. `tools/phan_loai_ly_do.py` (và `xuat_khoa_dt1b.py` nếu cần đọc CSV SO): thêm **mốc tham số** — chạy được với ảnh SO 18/11 thay vì ảnh 26/08; cổng K10/K11 so với **mốc đã khai** (số dòng SO · số dòng tái lập khớp 1-1 · tập dòng thiếu), ⛔ gõ cứng 9.967/9.845/122 cho mốc mới. Mốc 26/08 giữ là mặc định ⇒ mọi bài cũ xanh.
2. Ảnh mốc gọn, ⛔ PII: `tests/fixture/dt1b_moc_20261118.json` (hoặc tên tương đương) — mỗi dòng SO: `dong_sheet` + `khoa_bam` (sha256-16 của 5 trường đã chuẩn hoá, như `phan_loai_ly_do.py`) + cờ khớp 1-1; khai `nguon` (id + tên tệp + thời điểm đọc), `so_dong`, `so_khop`, `so_thieu`.
3. Chạy lượt THẬT: `--khoa` ⇒ đo; `--ghi` ⇒ ghi `docs/ITL/_tools/phan_loai_ly_do.json` (mỗi dòng thiếu ĐÚNG một nhãn trong bảng đóng; máy chặn PII sẵn có phải ĐẠT). Ghim MONG phân bố nhãn + vân tay của mốc mới (Đ5 — khai trước, khác ⇒ ĐỎ).
4. BG kèm **bảng tóm tắt cho người dùng kiểm** (CHỈ số đếm): số dòng SO · số khớp 1-1 · số thiếu · phân bố nhãn · số dòng mang nhãn "chưa rõ"/`KHAC` (nếu có) · 5–10 `dong_sheet` mẫu mỗi nhãn (⛔ giá trị ô) để người dùng mở sheet đối chiếu tay.

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 | mốc 26/08 mặc định: mọi bài `tests/du_lieu` cũ xanh, ảnh cũ đúng từng byte | pytest |
| AC-2 | mốc mới: K10/K11 so với số khai trong ảnh mốc; phá ảnh mốc (thêm/bớt 1 dòng) ⇒ ĐỎ | pytest (dữ liệu tổng hợp) + chạy thật |
| AC-3 | tệp nhãn thật: mỗi dòng thiếu đúng 1 nhãn; máy quét PII ĐẠT; 0 token Số CT/số tiền đầu vào | `python tools/phan_loai_ly_do.py` (cổng) |
| AC-4 | MONG phân bố nhãn ghim; đổi 1 nhãn ⇒ ĐỎ | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` MỘT lần cuối |

## Sau bước
- Người dùng kiểm bảng tóm tắt ⇒ OK ⇒ R2 cuối ⇒ gộp ⇒ mở **H3**. Ảnh 26/08 vẫn là mốc của oracle khác (đổi mốc toàn repo = phương án B, bước riêng nếu người dùng muốn).
