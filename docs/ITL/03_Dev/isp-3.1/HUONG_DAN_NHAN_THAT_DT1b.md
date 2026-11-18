# HƯỚNG DẪN OWNER — chạy lượt gán NHÃN THẬT cho 122 dòng (DT1b · O10)

**Phiên bản:** v1.0 · 2026-11-18 · phiếu `WO-127` / `BG-128` · ISP 3.1.2 · Step 5 · DT1b.
**Dành cho:** owner, chạy trên **máy Windows** có `Input_Raw\[Master] ITL_Ledge_raw.xlsx` (O10).

---

## Vì sao cần owner chạy tay

Khoá THẬT (Số CT · tiền · TK · tiền tệ) **⛔ đọc được ở container cloud** (`B-DATA-2`): file gốc trả
Permission denied, bản sao ADJUSTED hết giờ. Chỉ máy owner có `[Master] ITL_Ledge_raw.xlsx` và tab
`Transaction Mapping L1`. Hai công cụ đã sẵn trên nhánh làm việc:

- `tools\xuat_khoa_dt1b.py` — đọc 5 cột khoá từ `ITL Ledge` (.xlsx) + `Transaction Mapping L1` (.csv) ⇒
  một tệp `hien_vat\khoa_dt1b.csv` (nằm trong `.gitignore`, **⛔ lên git**).
- `tools\phan_loai_ly_do.py --khoa` — đọc tệp đó, gán mỗi dòng đúng một nhãn, ghi **khoá đã BĂM**
  (sha256) vào `docs\ITL\_tools\phan_loai_ly_do.json`. Giá trị thô **⛔ bao giờ** vào tệp JSON ấy.

> ⛔ **Riêng tư.** Cả quy trình ⛔ in giá trị ô ra màn; chỉ in **số đếm**. Tệp JSON chỉ mang khoá băm.
> Khi báo kết quả về orchestrator: **chỉ dán mã thoát + bảng đếm nhãn**, ⛔ dán giá trị khoá.

---

## Chuẩn bị một lần

Mở **PowerShell**, về gốc repo và bật UTF-8 (giữ nguyên cửa sổ này cho mọi bước):

```powershell
cd "C:\Users\0_Apero Project\FLS"
$env:PYTHONUTF8 = "1"
```

---

## Bước (a) — lấy nhánh làm việc mới nhất

```powershell
git fetch origin
git checkout claude/bold-galileo-zukpaf
git pull
```

**Mong:** nhánh `claude/bold-galileo-zukpaf` đã gộp WO-127, có đủ `tools\xuat_khoa_dt1b.py`.
Kiểm nhanh:

```powershell
Test-Path tools\xuat_khoa_dt1b.py      # mong: True
```

| Nếu thấy… | thì… |
|---|---|
| `Test-Path` ra **False** | WO-127 chưa gộp vào nhánh làm việc — **dừng**, báo orchestrator (⛔ chạy tiếp). |
| `git pull` báo *conflict* | ⛔ tự sửa — báo orchestrator kèm nguyên văn dòng lỗi. |

---

## Bước (b) — tải tab `Transaction Mapping L1` về CSV

1. Mở bảng tính RAW: <https://docs.google.com/spreadsheets/d/1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E>
2. Chọn đúng **tab `Transaction Mapping L1`** (ở thanh tab dưới cùng).
3. Menu **Tệp › Tải xuống › Giá trị được phân tách bằng dấu phẩy (.csv)**.
4. Lưu file vừa tải về thành: `hien_vat\l1.csv` (tạo thư mục `hien_vat` nếu chưa có).

```powershell
New-Item -ItemType Directory -Force hien_vat | Out-Null
# chép file .csv vừa tải (thường ở thư mục Downloads) vào đúng tên:
Copy-Item "$env:USERPROFILE\Downloads\*Transaction Mapping L1*.csv" hien_vat\l1.csv
Test-Path hien_vat\l1.csv              # mong: True
```

| Nếu thấy… | thì… |
|---|---|
| Google tải đúng **một tab** nhưng **sai tab** | Chọn lại đúng tab `Transaction Mapping L1`, tải lại. Tải "cả bảng tính" ra `.xlsx`/`.zip` là **sai** — cần CSV của đúng tab ấy. |
| `Copy-Item` ⛔ thấy file | Mở Downloads, chép tay file `.csv` vừa tải thành `hien_vat\l1.csv`. |

---

## Bước (c) — xuất bản đọc khoá

Đường tới file xlsx có dấu `[` `]` và khoảng trắng ⇒ **để trong ngoặc kép**:

```powershell
.venv\Scripts\python.exe tools\xuat_khoa_dt1b.py --xlsx "Input_Raw\[Master] ITL_Ledge_raw.xlsx" --l1 hien_vat\l1.csv
echo "exit=$LASTEXITCODE"
```

**Mong:** `exit=0`, màn in (chỉ số đếm, ⛔ giá trị):

```
✅ xuất hien_vat\khoa_dt1b.csv — SO 9967 hàng · L1 ... hàng (7 cột bang,dong,so_ct,ps_no,ps_co,tk,tien_te)
   ô rỗng/cột — SO: ...
   ▶ bước kế: python tools/phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv
```

> `SO` nên là **9967 hàng** (đúng số dòng dữ liệu của `ITL Ledge`, hàng 10…9976). Lệch số này thì bước
> (d) sẽ bắt ở cổng K11 — xem bảng bên dưới.

| Nếu thấy… | thì… |
|---|---|
| `exit=2` · *⛔ thấy tệp --xlsx* | Sai đường file xlsx. Kiểm `Test-Path "Input_Raw\[Master] ITL_Ledge_raw.xlsx"`; sửa đường cho đúng (giữ ngoặc kép). |
| `exit=1` · *LOI mở tệp … đóng Excel* | File `.xlsx` đang **mở trong Excel** ⇒ Windows khoá. Đóng Excel rồi chạy lại. |
| `exit=1` · *⛔ thấy tiêu đề cột 'Tài khoản'…* (hay tên cột khác) | Sheet/CSV thiếu đúng cột tiêu đề ấy, hoặc đọc nhầm sheet. Báo orchestrator kèm **tên cột** trong câu lỗi (⛔ giá trị). |
| `exit=1` · *⛔ thấy sheet 'ITL Ledge'* | File xlsx ⛔ có sheet tên `ITL Ledge`. Dán **danh sách tên sheet** mà câu lỗi in ra cho orchestrator. |

---

## Bước (d) — phân loại (ĐO, chưa ghi)

```powershell
.venv\Scripts\python.exe tools\phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv
echo "exit=$LASTEXITCODE"
```

**Mong:** `exit=4` (đo được, nhưng MONG phân bố nhãn **CHƯA GHIM** — đúng như thiết kế vòng này). Bảng in ra
phải có:

- dòng `①`/`②`: **tái lập khoá+seq = 9.845 / 9.845** (K10) — mẫu số `9.845` dòng ghép DT1a tìm lại được;
- cổng K11 (tập `dong_sheet` phía SO = **9.967**) **⛔ kêu lệch**;
- dòng `③`: bảng đếm 4 nhãn `KHONG_CO_SAO_KE · KHOA_LECH · TRUNG_SEQ · KHAC` (tổng = 122);
- cuối: `KẾT: ĐO ĐƯỢC — ⛔ CHƯA GHIM MONG … (mã 4, ⛔ phải ĐẠT)`.

| Nếu thấy… | thì… |
|---|---|
| `exit=1` · *tập dong_sheet phía SO ≠ 9.967…* (K11) | Bước (c) xuất **thiếu/thừa dòng** sổ. Dán câu lỗi (số thiếu/thừa) cho orchestrator — **⛔ sửa tay** `phan_loai_ly_do.py`. |
| `exit=1` · *tái lập … ≠ 9.845* (K10) | Chuẩn hoá khoá chưa khớp (Số CT khoa học, tiền có dấu phẩy…). Dán số tái lập đo được cho orchestrator. |
| `exit=3` · *⛔ CHƯA ĐO ĐƯỢC* | ⛔ thấy `hien_vat\khoa_dt1b.csv` — bước (c) chưa chạy xong. Quay lại (c). |
| `exit=2` | Sai cách gọi (đường dẫn sai, hay file nằm chỗ ⛔ gitignore). Dán câu lỗi cho orchestrator. |
| `exit=0` | **Bất thường ở vòng này** (MONG lẽ ra chưa ghim). Dừng, báo orchestrator. |

> ⛔ Nếu mã **≠ 4** đừng chạy bước (e). Gửi mã thoát + bảng `③④` về orchestrator, chờ hướng dẫn.

---

## Bước (e) — ghi tệp nhãn (chỉ khi bước (d) ra mã 4)

`--ghi` ghi tệp JSON **cả khi mã 4** — đã **xác minh trong mã** (`tools\phan_loai_ly_do.py`: `if ghi and ma
in (DAT, CHUA_GHIM)` với `CHUA_GHIM = 4`). Nên bước này ghi được dù MONG chưa ghim.

```powershell
.venv\Scripts\python.exe tools\phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv --ghi
echo "exit=$LASTEXITCODE"
```

**Mong:** `exit=4`, và dòng cuối: `✅ đã ghi phan_loai_ly_do.json (mã 4)`.

| Nếu thấy… | thì… |
|---|---|
| ⛔ dòng `✅ đã ghi…` dù mã 4 | Bản mã trên máy khác bản đã xác minh — **dừng**, báo orchestrator (⛔ tự sửa `phan_loai_ly_do.py`). |
| `exit=1` | Có cổng ĐỎ thật — ⛔ ghi. Dán danh sách lệch (stderr) cho orchestrator. |

---

## Bước (f) — commit đúng MỘT tệp

```powershell
git status
```

**Mong:** chỉ **một** tệp đổi: `docs/ITL/_tools/phan_loai_ly_do.json`.

```powershell
git add docs\ITL\_tools\phan_loai_ly_do.json
git commit -m "DT1b: ghi nhãn lý do thật cho 122 dòng sổ (lượt owner O10 · mã 4)"
git push
```

| Nếu thấy… | thì… |
|---|---|
| `git status` liệt kê **`hien_vat\...`** | ⛔ `git add` chúng. Chúng đã ở `.gitignore` nên ⛔ hiện ở "Changes to be committed" — chỉ cần ⛔ `git add -A`. |
| Có tệp khác ngoài `phan_loai_ly_do.json` được tô "sẽ commit" | **Dừng** — ⛔ commit. Báo orchestrator danh sách tệp. |

---

## Bước (g) — DỌN tệp thô (bắt buộc)

Hai tệp này mang Số CT + tiền thật — xoá ngay sau khi xong:

```powershell
Remove-Item hien_vat\khoa_dt1b.csv
Remove-Item hien_vat\l1.csv
```

**Mong:** cả hai biến mất (`Test-Path` ra `False`). Nếu Downloads còn bản `.csv` của tab L1, xoá luôn.

---

## Báo kết quả về orchestrator

Dán đúng những thứ này (⛔ giá trị khoá):

1. **Mã thoát** của bước (d) và (e) (`exit=…`).
2. **Bảng đếm nhãn** `③` (4 con số) và **nhãn × kỳ** `④` từ màn hình bước (d)/(e).
3. Dòng `①②` (tái lập 9.845 / mẫu số) và câu cổng K11.
4. Xác nhận bước (f) chỉ commit `phan_loai_ly_do.json`, bước (g) đã dọn.

Orchestrator sẽ dùng bảng đếm để **ghim MONG** (phân bố + vân tay nhãn) ở vòng sau — **⛔ phải việc của owner**.
