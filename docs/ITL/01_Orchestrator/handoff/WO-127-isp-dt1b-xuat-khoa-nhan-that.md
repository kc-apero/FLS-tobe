# WO-127 — ISP 3.1.2 · Step 5 · DT1b (tiếp): công cụ XUẤT bản đọc khoá + hướng dẫn owner chạy lượt nhãn THẬT

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **DATA** — **phiên cloud** (Opus 4.8 · medium) · cụm PG **5437** · nhánh `isp/DT1BT` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp DT1a + DT1b: `tools/phan_loai_ly_do.py` có `--khoa` · `--ghi`, MONG nhãn chưa ghim ⇒ mã 4) |
| **Dải phiếu** | `BG-128` · `KQ-129` (R1) · `KQ-130` (R2) · `KQ-131` (R3). Số trống kế tiếp: **132** |

## Vì sao
- DT1b đã gộp với công cụ đo + cổng, nhưng **lượt nhãn THẬT chưa chạy**: ISP Goal Step 5 (122 dòng mỗi dòng đúng 1 nhãn từ khoá ĐỌC Ở NGUỒN) chưa đạt ⇒ **H3 bị chặn**.
- Nguồn đo 17/11 (orchestrator, khoá SA): `Transaction Mapping L1` (RAW gốc `1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E`) đọc được; `ITL Ledge` của bản sao ADJUSTED **hết giờ 120 s** và đã xê dịch hàng so với ảnh **26/08** ⇒ phía SO phải là **`Input_Raw/[Master] ITL_Ledge_raw.xlsx` trên máy owner** (O10) — đúng tệp nguồn của ảnh `tests/fixture/itl_ledge_adjustment.json` (9.967 `dong_sheet`, hàng 10…9976).
- **Người dùng 18/11:** *"Đưa hướng dẫn, tôi chạy"* ⇒ owner tự chạy trên máy (Windows, repo `C:\Users\0_Apero Project\FLS`, venv `.venv\Scripts\python.exe`).

## Phạm vi
1. **`tools/xuat_khoa_dt1b.py`** — CHỈ thư viện chuẩn (`zipfile` + `xml.etree` — ⛔ `openpyxl`, ⛔ cài gói mới):
   - đọc sheet `ITL Ledge` của tệp xlsx (đường dẫn truyền vào) — tìm cột theo **tên tiêu đề** nguyên văn `Số chứng từ` · `PS Nợ` · `PS Có` · `Tài khoản` · `Đơn vị tiền tệ` (`fls/canon/spec.py`), ⛔ gõ cứng chữ cái cột; `dong` = số hàng Excel; xuất ĐỦ mọi hàng dữ liệu (để cổng K11 của `phan_loai_ly_do.py` tự so với 9.967 `dong_sheet`);
   - đọc `Transaction Mapping L1` từ tệp **CSV owner tải về** (Google Sheets › Tệp › Tải xuống › CSV của tab ấy) — tìm cột theo tên tiêu đề như trên; `dong` = số hàng sheet;
   - ghi CSV UTF-8 đúng **7 cột** `bang,dong,so_ct,ps_no,ps_co,tk,tien_te` (`bang` ∈ `SO` · `L1`), giá trị **thô như ô hiện** (chuẩn hoá là việc của `phan_loai_ly_do.py`); ⛔ cột nào khác — ⛔ `Diễn giải`, ⛔ email;
   - ⛔ in giá trị ô (chỉ in số đếm: số hàng SO · L1, số ô rỗng mỗi cột); đường ra mặc định trong `hien_vat/` (gitignore — đúng R8 của `phan_loai_ly_do.py`); từ chối ghi vào chỗ trong repo mà ⛔ gitignore.
   - TDD bằng xlsx/CSV TỔNG HỢP dựng trong bài (`tmp_path`, `zipfile`) — gồm: Số CT dạng khoa học `4.36619E+15` và ô chuỗi/số; tiền `'2,730,128.00'`; sharedStrings + inlineStr; ô trống; tiêu đề lệch vị trí; thiếu cột ⇒ lỗi có tên; ⛔ giá trị nào lọt ra stdout/stderr (bài quét). Ca nối: xuất ⇒ `phan_loai_ly_do.py --khoa` trên dữ liệu tổng hợp chạy được (mã 1/3/4 tuỳ dữ liệu — ⛔ đòi 0).
2. **Hướng dẫn owner** `docs/ITL/03_Dev/isp-3.1/HUONG_DAN_NHAN_THAT_DT1b.md` — từng lệnh PowerShell chép-dán được, theo thứ tự: `git pull` nhánh làm việc · tải CSV `Transaction Mapping L1` (đường dẫn link trực tiếp tới tab, tên tệp gợi ý) · chạy `xuat_khoa_dt1b.py` ra `hien_vat\khoa_dt1b.csv` · chạy `tools\phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv` (đọc kết quả: mã thoát + bảng đếm nhãn) · nếu mã 4 (MONG chưa ghim — mong đợi) chạy lại với `--ghi` · kiểm `git status` chỉ đổi `docs/ITL/_tools/phan_loai_ly_do.json` · commit + push (lệnh cụ thể) · **xoá** `hien_vat\khoa_dt1b.csv` và tệp CSV L1 tải về. Mỗi bước: kết quả mong đợi + nếu sai thì làm gì (mã 1/2/3, K10 tái lập ≠ 9.845, K11 tập dòng lệch). `$env:PYTHONUTF8=1`.
   - Kiểm xem `--ghi` có ghi khi mã 4 không (đọc mã) — nếu KHÔNG, ghi rõ trong hướng dẫn và ⛔ sửa `phan_loai_ly_do.py` (ngoài phạm vi; hỏi orchestrator).
3. ⛔ ghim MONG nhãn, ⛔ K14 — việc của vòng SAU khi owner đã commit tệp nhãn thật (WO riêng).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 | xlsx tổng hợp ⇒ CSV 7 cột đúng từng ô thô, `dong` đúng hàng Excel; thiếu cột ⇒ lỗi có tên, mã ≠ 0 | pytest |
| AC-2 | CSV L1 tổng hợp (định dạng Google Sheets tải về) ⇒ hàng `L1` đúng | pytest |
| AC-3 | 0 giá trị ô trên stdout/stderr (bài quét có ca phá) · ra mặc định trong `hien_vat/` · từ chối đường trong repo ⛔ gitignore | pytest |
| AC-4 | ca nối với `phan_loai_ly_do.py --khoa` chạy được trên dữ liệu tổng hợp | pytest |
| AC-5 | hướng dẫn: mỗi lệnh chép-dán được trên Windows PowerShell; có bước dọn tệp thô | đọc + `kiem_tai_lieu` |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. ⛔ Drive (bước này thuần mã + bài tổng hợp).
