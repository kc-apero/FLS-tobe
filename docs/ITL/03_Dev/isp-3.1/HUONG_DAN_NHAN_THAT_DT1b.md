# HƯỚNG DẪN OWNER — chạy lượt gán NHÃN THẬT cho 122 dòng (DT1b · O10)

**Phiên bản:** v1.1 · 2026-11-18 · phiếu `WO-127` / `BG-128` · ISP 3.1.2 · Step 5 · DT1b.
**Dành cho:** owner, chạy trên **máy Windows** có `Input_Raw\[Master] ITL_Ledge_raw.xlsx` (O10).

> **Cách đọc hướng dẫn này.** Mỗi bước có một ô lệnh để chép-dán, một dòng **Mong** (kết quả đúng), và
> một bảng *"Nếu thấy… thì…"*. Hướng dẫn viết chữ thường, không dùng ký hiệu; chỗ nào bảo *đừng* làm gì
> thì nói rõ bằng chữ. Nếu gặp bất kỳ điều gì khác dòng **Mong**, dừng lại và làm theo bảng *"Nếu thấy"*.

---

## Vì sao cần owner chạy tay

Khoá THẬT (Số CT, tiền, TK, tiền tệ) **không đọc được ở container cloud** (`B-DATA-2`): file gốc trả
Permission denied, bản sao ADJUSTED hết giờ. Chỉ máy owner có `[Master] ITL_Ledge_raw.xlsx` và tab
`Transaction Mapping L1`. Hai công cụ đã sẵn trên nhánh làm việc:

- `tools\xuat_khoa_dt1b.py` — đọc 5 cột khoá từ `ITL Ledge` (.xlsx) + `Transaction Mapping L1` (.csv) ra
  một tệp `hien_vat\khoa_dt1b.csv` (nằm trong `.gitignore`, **không lên git**).
- `tools\phan_loai_ly_do.py --khoa` — đọc tệp đó, gán mỗi dòng đúng một nhãn, ghi **khoá đã BĂM**
  (sha256) vào `docs\ITL\_tools\phan_loai_ly_do.json`. Giá trị thô **không bao giờ** vào tệp JSON ấy.

> **Riêng tư.** Cả quy trình không in giá trị ô ra màn; chỉ in **số đếm**. Tệp JSON chỉ mang khoá băm.
> Khi báo kết quả về orchestrator: **chỉ dán mã thoát và bảng đếm nhãn**, đừng dán giá trị khoá.

---

## Chuẩn bị một lần

Mở **PowerShell**, về gốc repo và bật UTF-8 (giữ nguyên cửa sổ này cho mọi bước):

```powershell
cd "C:\Users\0_Apero Project\FLS"
$env:PYTHONUTF8 = "1"
```

> **Dấu ngoặc vuông trong tên file.** Tên thư mục/tệp của owner có dấu `[` `]` (ví dụ `[Master] …`).
> Trong PowerShell, các lệnh `Test-Path`, `Copy-Item`, `Move-Item`, `Remove-Item`, `Resolve-Path`
> **mặc định hiểu `[ ]` là ký tự đại diện** (wildcard), nên với tên có thật chúng có thể trả sai (ví dụ
> `Test-Path` ra `False` dù file có thật). Vì vậy **mọi** lệnh PowerShell chạm một đường có `[` `]` trong
> hướng dẫn này đều dùng **`-LiteralPath`** (đường nguyên văn). Khi tự gõ thêm lệnh, nhớ làm theo.

---

## Bước (0) — kiểm file xlsx có đúng chỗ, và nằm trong hay ngoài repo

Trước khi chạy, xác nhận file xlsx có thật và biết nó nằm **trong** hay **ngoài** thư mục repo. Sửa đường
ở biến `$XLSX` cho đúng máy owner nếu khác:

```powershell
$XLSX = "Input_Raw\[Master] ITL_Ledge_raw.xlsx"
Test-Path -LiteralPath $XLSX                      # mong: True
(Resolve-Path -LiteralPath $XLSX).Path            # in đường đầy đủ của file xlsx
(Resolve-Path -LiteralPath ".").Path              # in đường đầy đủ của gốc repo
```

**Mong:** dòng `Test-Path` ra **True**; hai đường đầy đủ in ra để owner tự so: nếu đường file xlsx **bắt
đầu bằng** đường gốc repo thì file **nằm TRONG repo**, ngược lại là **ngoài repo**.

| Nếu thấy… | thì… |
|---|---|
| `Test-Path -LiteralPath $XLSX` ra **False** | Sai đường file xlsx (hoặc quên `-LiteralPath`). Sửa `$XLSX` cho đúng tên có thật, chạy lại bước (0). |
| file xlsx **nằm TRONG repo** nhưng **không** ở trong thư mục `Input_Raw\` | Chuyển file vào `Input_Raw\` (thư mục này đã nằm trong `.gitignore`, nên sổ thật không lên git). Nếu không chuyển được, báo orchestrator trước khi chạy tiếp. |
| file xlsx **nằm NGOÀI repo** | Không sao — chỉ cần dùng đúng đường đầy đủ ở bước (c) (`--xlsx "<đường đầy đủ>"`, giữ ngoặc kép). |

---

## Bước (a) — lấy nhánh làm việc mới nhất

```powershell
git fetch origin
git checkout claude/bold-galileo-zukpaf
git pull
Test-Path tools\xuat_khoa_dt1b.py      # mong: True (đường này không có dấu [ ], không cần -LiteralPath)
```

**Mong:** nhánh `claude/bold-galileo-zukpaf` đã gộp WO-127, có đủ `tools\xuat_khoa_dt1b.py`.

| Nếu thấy… | thì… |
|---|---|
| `Test-Path` ra **False** | WO-127 chưa gộp vào nhánh làm việc — **dừng**, báo orchestrator (đừng chạy tiếp). |
| `git pull` báo *conflict* | Đừng tự sửa — báo orchestrator kèm nguyên văn dòng lỗi. |

---

## Bước (b) — tải tab `Transaction Mapping L1` về CSV

1. Mở bảng tính RAW: <https://docs.google.com/spreadsheets/d/1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E>
2. Chọn đúng **tab `Transaction Mapping L1`** (ở thanh tab dưới cùng).
3. Menu **Tệp › Tải xuống › Giá trị được phân tách bằng dấu phẩy (.csv)**.
4. Lưu file vừa tải về thành `hien_vat\l1.csv` theo lệnh dưới (lệnh dùng `Move-Item`, **không để lại bản
   sao ở Downloads** — tránh để Số CT + tiền thật nằm lại máy):

```powershell
New-Item -ItemType Directory -Force hien_vat | Out-Null
# CHUYỂN (không chép) file .csv vừa tải về (thường ở Downloads) sang đúng tên:
Move-Item -LiteralPath (Get-ChildItem "$env:USERPROFILE\Downloads\*Transaction Mapping L1*.csv" | Select-Object -First 1).FullName hien_vat\l1.csv
Test-Path hien_vat\l1.csv              # mong: True
```

**Mong:** `hien_vat\l1.csv` có mặt; ở Downloads **không** còn bản `.csv` của tab L1.

| Nếu thấy… | thì… |
|---|---|
| Google tải đúng **một tab** nhưng **sai tab** | Chọn lại đúng tab `Transaction Mapping L1`, tải lại. Tải "cả bảng tính" ra `.xlsx`/`.zip` là **sai** — cần CSV của đúng tab ấy. |
| `Move-Item` báo không thấy file | Mở Downloads, chuyển tay file `.csv` vừa tải thành `hien_vat\l1.csv` (dùng *Cut* rồi *Paste*, đừng *Copy*, để Downloads không còn bản). |
| Downloads có **nhiều** file `*Transaction Mapping L1*.csv` | Xoá các bản cũ ở Downloads trước (chúng mang tiền thật), rồi tải lại một bản mới và chạy lại lệnh. |

---

## Bước (c) — xuất bản đọc khoá

```powershell
.venv\Scripts\python.exe tools\xuat_khoa_dt1b.py --xlsx $XLSX --l1 hien_vat\l1.csv
echo "exit=$LASTEXITCODE"
```

(`$XLSX` là biến đã đặt ở bước (0). Python nhận chuỗi nguyên nên dấu `[ ]` trong đường không gây lỗi.)

**Mong:** `exit=0`, màn in (chỉ số đếm, không có giá trị):

```
✅ xuất hien_vat\khoa_dt1b.csv — SO 9967 hàng · L1 ... hàng (7 cột bang,dong,so_ct,ps_no,ps_co,tk,tien_te)
   hàng có ≥1 ô khoá / hàng 0 ô khoá — SO: 9967 / 0 · L1: ... / ...
   ô rỗng/cột — SO: ...
   ▶ bước kế: python tools/phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv
```

> `SO` nên là **9967 hàng** (đúng số dòng dữ liệu của `ITL Ledge`, hàng 10…9976). Dòng *"hàng 0 ô khoá —
> SO"* nên là **0**: nếu số này **lớn hơn 0**, đuôi sổ có hàng chỉ mang ô công thức ở cột ngoài 5 khoá đã
> bị tính thành "hàng dữ liệu" — xem bảng ở bước (d).

| Nếu thấy… | thì… |
|---|---|
| `exit=2` và *không thấy tệp --xlsx* | Sai đường file xlsx. Quay lại bước (0): kiểm `Test-Path -LiteralPath $XLSX` và sửa `$XLSX`. |
| `exit=1` và *LOI mở tệp … đóng Excel* | File `.xlsx` đang **mở trong Excel** nên Windows khoá. Đóng Excel rồi chạy lại. |
| `exit=1` và *không phải tệp .xlsx hợp lệ* (XML hỏng / không giải nén được) | File xlsx hỏng, hoặc không phải .xlsx thật. Mở lại trong Excel, *Lưu thành* `.xlsx`, rồi chạy lại. Nếu vẫn lỗi, báo orchestrator nguyên văn dòng lỗi (một dòng, không có giá trị ô). |
| `exit=1` và *không thấy tiêu đề cột 'Tài khoản'…* (hay tên cột khác) | Sheet/CSV thiếu đúng cột tiêu đề ấy, hoặc đọc nhầm sheet. Báo orchestrator kèm **tên cột** trong câu lỗi (không có giá trị). |
| `exit=1` và *không thấy sheet 'ITL Ledge'* | File xlsx không có sheet tên `ITL Ledge`. Dán **danh sách tên sheet** mà câu lỗi in ra cho orchestrator. |
| `exit=1` và *CSV không phải UTF-8* | File `hien_vat\l1.csv` không phải CSV UTF-8 (có thể bị xuất từ Excel sang mã khác). Tải lại từ Google Sheets đúng menu ở bước (b), rồi chạy lại. |

---

## Bước (d) — phân loại (ĐO, chưa ghi)

```powershell
.venv\Scripts\python.exe tools\phan_loai_ly_do.py --khoa hien_vat\khoa_dt1b.csv
echo "exit=$LASTEXITCODE"
```

**Mong:** `exit=4` (đo được, nhưng MONG phân bố nhãn **CHƯA GHIM** — đúng như thiết kế vòng này). Bảng in
ra phải có:

- dòng `①`/`②`: **tái lập khoá+seq = 9.845 / 9.845** (K10) — mẫu số `9.845` dòng ghép DT1a tìm lại được;
- cổng K11 (tập `dong_sheet` phía SO = **9.967**) **không kêu lệch**;
- dòng `③`: bảng đếm 4 nhãn `KHONG_CO_SAO_KE · KHOA_LECH · TRUNG_SEQ · KHAC` (tổng = 122);
- cuối: `KẾT: ĐO ĐƯỢC — CHƯA GHIM MONG … (mã 4, chưa phải ĐẠT)`.

| Nếu thấy… | thì… |
|---|---|
| `exit=1` và *tập dong_sheet phía SO ≠ 9.967…* (K11), **và** ở bước (c) dòng *"hàng 0 ô khoá — SO"* **lớn hơn 0** | Đuôi sổ có hàng chỉ mang công thức bị tính thành dòng dữ liệu. **Dừng**, báo orchestrator **hai số**: số ở K11 (thiếu/thừa) và số *"hàng 0 ô khoá — SO"* ở bước (c). Đừng sửa tay `phan_loai_ly_do.py`. |
| `exit=1` và *tập dong_sheet phía SO ≠ 9.967…* (K11), mà *"hàng 0 ô khoá — SO"* = 0 | Bước (c) xuất thiếu/thừa dòng sổ. Dán câu lỗi (số thiếu/thừa) cho orchestrator — đừng sửa tay `phan_loai_ly_do.py`. |
| `exit=1` và *tái lập … ≠ 9.845* (K10) | Chuẩn hoá khoá chưa khớp (Số CT khoa học, tiền có dấu phẩy…). Dán số tái lập đo được cho orchestrator. |
| `exit=3` và *CHƯA ĐO ĐƯỢC* | Không thấy `hien_vat\khoa_dt1b.csv` — bước (c) chưa chạy xong. Quay lại (c). |
| `exit=2` | Sai cách gọi (đường dẫn sai, hay file nằm chỗ không được gitignore). Dán câu lỗi cho orchestrator. |
| `exit=0` | **Bất thường ở vòng này** (MONG lẽ ra chưa ghim). Dừng, báo orchestrator. |

> Nếu mã **khác 4** thì đừng chạy bước (e). Gửi mã thoát và bảng `③④` về orchestrator, chờ hướng dẫn.
> (Dù dừng ở đây, vẫn chạy bước dọn (g) trước khi rời máy.)

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
| **không** thấy dòng `✅ đã ghi phan_loai_ly_do.json (mã 4)` (dù `exit=4`) | Bản mã trên máy khác bản đã xác minh — **dừng**, báo orchestrator (đừng tự sửa `phan_loai_ly_do.py`). |
| `exit=1` | Có cổng ĐỎ thật — không ghi. Dán danh sách lệch (phần lỗi in ra) cho orchestrator. |

---

## Bước (f) — commit đúng MỘT tệp

```powershell
git status
```

**Mong:** chỉ **một** tệp đổi: `docs/ITL/_tools/phan_loai_ly_do.json`. Các tệp thô (`hien_vat\…`,
`Input_Raw\…`) đã nằm trong `.gitignore` nên **không** hiện ở phần *"Changes to be committed"*.

```powershell
git add docs\ITL\_tools\phan_loai_ly_do.json
git commit -m "DT1b: ghi nhãn lý do thật cho 122 dòng sổ (lượt owner O10 · mã 4)"
git push
```

| Nếu thấy… | thì… |
|---|---|
| `git status` liệt kê `hien_vat\…` hoặc `Input_Raw\…` trong *"Changes to be committed"* | **Dừng** — những tệp này mang dữ liệu thật, không được lên git. Báo orchestrator (có thể `.gitignore` thiếu). Chỉ dùng `git add <một tệp>` như trên, **đừng** dùng `git add -A` hay `git add .`. |
| Có tệp khác ngoài `phan_loai_ly_do.json` được tô *"sẽ commit"* | **Dừng** — đừng commit. Báo orchestrator danh sách tệp. |

---

## Bước (g) — DỌN tệp thô (bắt buộc, chạy ở MỌI trường hợp kết thúc)

Dù chạy trót lọt hay **dừng giữa chừng ở bất kỳ bước nào**, trước khi rời máy hãy chạy bước dọn này. Ba
chỗ có thể còn Số CT + tiền thật: tệp xuất, tệp L1 ở thư mục làm việc, và bản tải ở Downloads.

```powershell
# 1) tệp xuất và tệp L1 ở thư mục làm việc:
if (Test-Path -LiteralPath hien_vat\khoa_dt1b.csv) { Remove-Item -LiteralPath hien_vat\khoa_dt1b.csv }
if (Test-Path -LiteralPath hien_vat\l1.csv)        { Remove-Item -LiteralPath hien_vat\l1.csv }
# 2) mọi bản CSV của tab L1 còn sót ở Downloads (nếu bước (b) đã Move-Item thì thường không còn):
Get-ChildItem "$env:USERPROFILE\Downloads\*Transaction Mapping L1*.csv" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -LiteralPath $_.FullName }
# 3) kiểm lại, cả ba phải mất:
Test-Path -LiteralPath hien_vat\khoa_dt1b.csv                             # mong: False
Test-Path -LiteralPath hien_vat\l1.csv                                    # mong: False
(Get-ChildItem "$env:USERPROFILE\Downloads\*Transaction Mapping L1*.csv" -ErrorAction SilentlyContinue).Count   # mong: 0
```

**Mong:** cả ba dòng kiểm ra `False` / `False` / `0`.

> `Remove-Item` xoá thẳng, không vào Thùng rác — đúng ý (dữ liệu thật không nên nằm lại trong Thùng rác).
> File xlsx gốc (`Input_Raw\[Master] …`) là của owner, **không** xoá ở đây.

---

## Báo kết quả về orchestrator

Dán đúng những thứ này (đừng dán giá trị khoá):

1. **Mã thoát** của bước (d) và (e) (`exit=…`).
2. **Bảng đếm nhãn** `③` (4 con số) và **nhãn × kỳ** `④` từ màn hình bước (d)/(e).
3. Dòng `①②` (tái lập 9.845 / mẫu số) và câu cổng K11; nếu K11 lệch, kèm dòng *"hàng 0 ô khoá — SO"* ở (c).
4. Xác nhận bước (f) chỉ commit `phan_loai_ly_do.json`, bước (g) đã dọn (ba dòng kiểm).

Orchestrator sẽ dùng bảng đếm để **ghim MONG** (phân bố + vân tay nhãn) ở vòng sau — đó không phải việc
của owner.
