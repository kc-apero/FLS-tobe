# Checklist `G7` — đọc Google Sheets live, từng ô một

**Version:** v0.2 · **Ngày:** 2026-08-20 · **Bước:** `G7` của `_PLAN_Guide-Nghiep-vu-Ke-toan.md`
**Trạng thái:** ✅ **9 mục ĐÃ ĐÓNG** — kết quả ở [Ket-qua-G7-Live-ITL-Ledge.md](Ket-qua-G7-Live-ITL-Ledge.md) · ⛔ phần còn lại chặn ở quyền file, xem §1.1

**Đóng khoá cho:** 8 mục `[G7]` ở §8 của [Process-PM-den-ITL.md](Process-PM-den-ITL.md) · `GAP-GUIDE-03` · `GAP-ITL-11`

---

## §0 · Đã lấy được ngay — không cần buổi live

> **Đã hợp nhất** vào [Process-PM-den-ITL.md](Process-PM-den-ITL.md) v1.0 (SSOT). Giữ ở đây vì script ở §3 cần các ID này. Riêng cảnh báo §0.4 **đã có đáp án** — xem §7.5 của process map.


Tôi vào được Google Drive của bạn. Bốn thứ sau **đã xác nhận**, không cần chờ ai:

### 0.1 · Ba file ID thật (đóng một phần `GAP-GUIDE-03`)

| File | Spreadsheet ID | Chủ sở hữu | Sửa lần cuối | Cỡ |
|---|---|---|---|--:|
| `A \| PAY100 \| PM11 Entry Data` | `1U8tDdaBVrgCFZLuxBUkgttyFvhHLpF1cXYg7N_sgn0M` | **finance@apero.vn** | 2026-08-20 | 1,69 MB |
| `ITL I Input Transaction Ledger File 1/2 (RAW)` | `1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU` | **lanptn@apero.vn** | 2026-08-19 | 2,79 MB |
| `ITL I Input Transaction Ledger File 2/2 (ADJUSTED)` | `1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA` | **lanptn@apero.vn** | 2026-08-19 | 0,92 MB |

> ⚠ Có **bản sao** `Bản sao của ITL … 2/2 (ADJUSTED)` — ID `1Pqg_G81xQKKP-tyR8IFFcnaimT2oZ22e-Tq_mewxbN0`, chủ **dungtt1@apero.vn**, sửa lần cuối 2026-06-29. Bản sao của sổ xương sống nằm ngoài tầm kiểm soát ⇒ phải đưa vào kill-list hoặc khai báo rõ mục đích.

**Sửa lại `_GUIDE_01` §2:** hai cạnh trước đây ghi *"`ITL … Fi…` ▸ `RAW ITLData Management`"* bị cắt tên nên không rõ file nào. Nay giải được — **hai nửa của cùng một bảng đo, soi gương nhau**:

| File | Tự tính | Nhập từ |
|---|---|---|
| **RAW** (`1xaD1…`) | `J6:R` — 4 trường P100 (`ID PC`/`PM`/`PE`/`PI`) từ `Transaction Mapping L1` | `S6:AB77` ← **ADJUSTED** |
| **ADJUSTED** (`1r4We…`) | `S6:AB` — 5 trường báo cáo từ `ITL Ledge` | `J6:R` ← **RAW** |

### 0.2 · Tên thật 9 cột đo của `[RAW ITL] Data Management`

Bản offline để trống hết tiêu đề (cột L…AB `*(trống)*`). Bản live có tên đầy đủ — **đây là bộ chỉ số sức khoẻ của toàn luồng**:

| Nhóm | Trường đo | Đo ở đâu |
|---|---|---|
| **P100 Data (Data filtering)** | `ID PC` · **`ID PM`** · `ID PE` · `ID PI` | `Transaction Mapping L1` (file RAW) |
| **Data Reporting** | `HD/KRF Code` · `ID Vendor` · `Service Execution Time (PL Date)` · `Type of Transaction (Regular or Advance)` · `PI Attached` | `ITL Ledge` (file ADJUSTED) |

Mỗi trường một cặp cột `Yes` / `No`. Nhóm 2 còn cột `Need to manual input`.

⇒ **Bốn trường đầu chính là bốn chặng của P100** (`PC`, `PM`, `PE`, `PI`). Bảng này trả lời đúng câu *"dòng tiền nào chưa nối được về phiếu nào"* — tách riêng từng loại phiếu, không gộp.

### 0.3 · Cột `AL` của sổ đăng ký `Index` = **Accounting Layer**

Header live: `Folder | File | Sheet | AL | Source | Sheet | Cell | Flow`.
Cột `AL` mang giá trị `CFA1` / `CFA2` / `CFA3` / `PLA1` / `PLA2` / `PLA3` — **lớp kế toán**, không phải nhãn tự do. `Flow` = `I` (input) / `O` (output). Xác nhận 18 dòng đăng ký đúng như §3 chặng 4 của process map, và bổ sung: **cột `C` (RAW) / `D` (ADJUSTED) = `AL`** — chỗ này process map v0.1 chưa ghi.

### 0.4 · ⚠ Số live **khác** số offline — phải xem lại một khẳng định của tôi

Bản live của `[RAW ITL] Data Management` (file ADJUSTED) cho:

| Chỉ số | Giá trị live |
|---|---|
| Tổng giao dịch `All` | **9.627** |
| Nhóm `Statement` | **7.717** |
| Tỷ lệ có `ID PC` / `ID PM` / `ID PE` / `ID PI` | **100% / 0%** ở **mọi** nguồn được liệt kê |
| `Cut-off Date` | có thật, ví dụ `17-Aug-2026`, `13-Aug-2026`, `5-Aug-2026` |
| `Data Lag` | phần lớn **2–15 ngày**; hai nguồn chết: `R \| 03501371992992_MSB USD_VGO1` **407 ngày** (1 giao dịch) · `R \| 501810899401_OCBC USD_SGO2` **264 ngày** (11 giao dịch) |

**Nghĩa là:** bản offline `.xlsx` toàn `#REF!` là **lỗi xuất file**, không phải luồng gãy — đúng như luật `gsheet-offline-export-artifacts`.

> ⚠ **Tôi phải sửa lại điều đã nói.** Ở lần trả lời trước tôi nói cột `M` chỉ ra *"tài khoản đang hụt `Reference number` ở PM"*. Bản live báo **0% hụt** ở mọi nguồn. Hai khả năng, chưa phân biệt được: (a) ghép PM **thực sự đã đủ**, hoặc (b) mẫu số `I8` đang sai nên bảng đo **luôn cho 100%**. Phải kiểm bằng `G7-07` + `G7-22` trước khi dùng con số này.
>
> Hai điều **không** thay đổi vì chúng là chuyện cấu trúc, không phải chuyện tỷ lệ: **12 cột PM/PE/PI bị rơi ở chặng 8** (§5 process map) và **6.843 ô gõ tay** ở `ITL Ledge`.
>
> ✅ **ĐÃ TRẢ LỜI bằng `G7-22`**: đáp án là **(b) — bảng đo hỏng**. Tử số đếm dòng trong `ITL Ledge`, mẫu số `I8` lấy từ ô `V2` của **sheet ngân hàng nguồn** ⇒ hai tổng thể khác nhau, tỷ lệ vô nghĩa; và ô **để trống** cũng được tính là `Yes`. Chi tiết [Ket-qua-G7-Live-ITL-Ledge.md](Ket-qua-G7-Live-ITL-Ledge.md) §5. Con số **6.843 cũng phải đọc lại**: nó là số lần **đã dùng giá trị mặc định**, không phải số ô chưa làm.

---

## §1.1 · ✅ ĐÃ CHẠY — 9 mục đóng bằng service account có sẵn

Không cần đăng nhập gì thêm: SA **`claude-code-access@fpa-t-494007.iam.gserviceaccount.com`** (đã có trong `gcloud auth list`) **sẵn quyền Viewer trên file ADJUSTED**. Đọc được `valueRenderOption=FORMULA`.

| Đóng | Chặn |
|---|---|
| `G7-16` `G7-17` `G7-18` `G7-19` `G7-20` `G7-21` `G7-22` `G7-25` `G7-26` | mọi mục file **RAW** (`G7-01..15`) và **PM** (`G7-27..30`) — SA báo **403** |

**Mở phần còn lại chỉ cần MỘT việc:** chia sẻ **file RAW** cho email SA, quyền **Người xem**:

- ★ `ITL I Input Transaction Ledger File 1/2 (RAW)` — `1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU`

*Tuỳ chọn* — `A | PAY100 | PM11 Entry Data` (`1U8tDda…`): theo xác nhận của owner, `PM_Unpivot` chỉ là **dữ liệu PM thô, không có logic**; mọi hoạt động mapping nằm ở `Transaction Mapping L1` **trong file RAW**. Mức hụt ghép cũng đo được từ `Mapping L1!N:N`.

⛔ **Đừng đi đường ADC của `thanhnc@apero.vn`**: gcloud báo Google **sắp chặn** scope `spreadsheets.readonly` / `drive.readonly` với client ID mặc định của gcloud. Đường SA bền hơn.

⛔ **Đọc GIÁ TRỊ (`FORMATTED_VALUE`) không được**: timeout cả với dải 3 ô và cả với sheet nhẹ ⇒ **cả workbook phải tính lại**. Chỉ lấy được **công thức**.

**Script đã chạy:** `AS-IS system/Accounting_Files/_tools/read_live_cells.py` (bản ADC) và `sa2.py` (bản SA, dùng `gcloud auth print-access-token --account=<SA> --scopes=…spreadsheets.readonly`).

---

## §1 · Giới hạn công cụ — vì sao vẫn cần một lượt Sheets API

| Cần gì | Drive connector làm được? | Ghi chú |
|---|:--:|---|
| Giá trị ô | **Có** | nhưng bảng bị làm phẳng thành markdown, **lệch cột** ở dòng có ô trống |
| **Công thức ô** | **KHÔNG** | connector trả *kết quả đã tính*. Cần `valueRenderOption=FORMULA` |
| Đọc sheet thứ 2 trở đi của file lớn | **KHÔNG** | thử đọc file PM: bị **cắt ở sheet đầu** (`Draft_Hippo`, 287 nghìn ký tự), không tới được `PM_Unpivot` |
| Chỉ định dải cụ thể | **KHÔNG** | không có tham số range ⇒ luôn kéo cả file |

⇒ **Sáu mục quan trọng nhất đều là công thức.** Bắt buộc một lượt Sheets API `batchGet`.

**Chặn hiện tại:** không tìm thấy service-account key trên máy (`FPA-T DB key.json` không có ở `C:\Users\0_Apero Project`). Cần một trong hai:

```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets.readonly,https://www.googleapis.com/auth/cloud-platform
```

hoặc đặt SA key vào `.secrets/sheets-ro.json` và **chia sẻ 4 file trên cho email của SA** (quyền Viewer là đủ).

---

## §2 · Checklist — 32 mục, ghi rõ ô nào đọc kiểu gì

Cột **Kiểu**: `F` = đọc công thức (`FORMULA`) · `V` = đọc giá trị (`FORMATTED_VALUE`) · `F+V` = cả hai.

### A · File RAW — `1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU`

| # | Sheet | Dải | Kiểu | Lấy về để làm gì | Mở khoá |
|--:|---|---|:--:|---|---|
| `G7-01` | `Index` | `A1:O20` | `F+V` | chốt 18 dòng đăng ký + cột `AL` + ma trận `Flow`; xem ô D/E/F có phải hằng hay công thức | chặng 4 |
| ⛔`G7-02` | **`Transaction Mapping L1`** | **`A5:AL5`** | **`F`** | ★ **công thức ghép PM↔tiền — mục quan trọng nhất của cả bước G7** | chặng 7 · khoá §4 #8 |
| `G7-03` | `Transaction Mapping L1` | `A6:AL6` + `A500:AL500` | `F` | đối chiếu: công thức dòng 5 có giống dòng giữa bảng không (bẫy công thức bị ghi đè tay) | `INV` mới |
| `G7-04` | `Transaction Mapping L1` | `A3:AL4` | `V` | tên cột thật 2 dòng header (offline dòng 4 chưa đọc được) | `BA-05` |
| `G7-05` | `Transaction Original` | `A2:G3` | `F+V` | xác nhận `QUERY({112;111})` và thứ tự xếp | chặng 6 |
| `G7-06` | `Mapping Master` | `A3:P6` | `F+V` | 16 cột: `Bank Sheet → LE · HD · COA1 · COA2 · Need to Allocate to CFA2 · Method · Code HR Allocate` | khoá §4 #10 |
| `G7-07` | **`RAW ITLData Management`** | **`A3:AB15`** | **`F+V`** | ★ mẫu số `I8` lấy từ đâu, `COUNTIFS` đếm cột nào — **kiểm nghi vấn 100% ở §0.4** | `GAP-ITL-11` |
| ⛔`G7-08` | **`ImportrangePM_Unpivot`** | **`A1:AB3`** | **`V`** *(chỉ lấy TÊN CỘT — sheet không có logic)* | ★ **28 tên cột của PM** — đọc từ bản bake, **không cần mở file PM** | §8 mục 2 |
| `G7-09` | `ImportrangePM_Unpivot` | `A1` | `F` | xác nhận `IMPORTRANGE(Index!D8, Index!E8&Index!F8)` | chặng 5 |
| `G7-10` | `ImportrangePE_Unpivot` | `A1:W2` | `V` | 23 tên cột PE | §5 process map |
| `G7-11` | `ImportrangePI_Unpivot` | `A1:X2` | `V` | 24 tên cột PI | idem |
| `G7-12` | `ImportrangePC11_Entry Data` | `A1:T2` | `V` | 20 tên cột PC | idem |
| `G7-13` | `Export Log` | `A1:G30` | `V` | lần refresh gần nhất + số dòng/cột từng sheet ⇒ so với live để biết có lệch | `OP-20` |
| `G7-14` | `Check list mapping` | `A1:F12` | `V` | 7 sự cố kế toán tự ghi — đọc **trọn văn** cột `Vấn đề`/`Giải pháp` (offline bị cắt) | `BA-10` 4 phép kiểm |
| `G7-15` | `SGO1Transaction Mapping L1` | `A1:A5` | `F+V` | ô `A1` giữ mã LE nào ⇒ cơ chế lát theo pháp nhân | khoá §4 #11 |

### B · File ADJUSTED — `1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA`

| # | Sheet | Dải | Kiểu | Lấy về để làm gì | Mở khoá |
|--:|---|---|:--:|---|---|
| ✅`G7-16` | **`ITL Ledge`** | **`B1:B3`** | **`V`** | ★ `$B$1` = ID file nguồn · `$B$2` = **tên sheet nguồn** · `$B$3` = **mốc ngày lọc** | §8 mục 3+4 |
| `G7-17` | `ITL Ledge` | `A1:BL9` | `V` | 4 băng vùng, nhãn `PIC:`, dòng đếm `# Input here` **hiện tại** (offline là 6.843 — xem đã đổi chưa) | `OP-07` |
| ✅`G7-18` | **`ITL Ledge`** | **`A8,G8,I8,K8,M8,N8,P8,Q8`** | **`F`** | ★ 8 công thức `filter(IMPORTRANGE(...))` — chứng minh **12 cột bị rơi** hay bản live đã bổ sung | **§5 process map** |
| `G7-19` | `ITL Ledge` | `R8:AT8` | `F` | công thức 7 khối × 4 cột `Classifying → Manual → MID → Final`; **`Classifying` quyết định khi nào gọi người** | `DT-I02`, `DT-I08` |
| `G7-20` | `ITL Ledge` | `AU8:AW8` | `F` | vùng ALLOCATE: `CDT1 CFA1` · `CDT1 CFA2` · `Method` | `GAP-ERD` phân bổ |
| ✅`G7-21` | **`ITL Ledge`** | **`AX1:BI4`** | **`F+V`** | ★ `$AX$2`/`$AX$3` = **nguồn `Report I General Ledger`** + 6 cặp `VALUE`/`FALSE` hiện tại | **`GAP-ITL-11`** |
| `G7-22` | `RAW ITLData Management` | `A3:AB15` | `F+V` | nửa `S:AB` — `COUNTIFS('ITL Ledge'!T:T,"Input here",…)/I8`; kiểm mẫu số | `GAP-ITL-11` |
| `G7-23` | `ITL Ledge` | `A10:BL13` | `V` | **4 dòng dữ liệu thật với NGÀY ĐÚNG** — bản `.xlsx` chỉ còn 2,7% ô ngày nguyên vẹn | `itl-date-daymonth-swap` |
| `G7-24` | `ITL Ledge` | `BJ1:BL10` | `V` | ai đang gánh cột `PIC` / `Trạng thái` của vùng AUDIT | `GAP-ITL-24` |
| `G7-25` | `Index` | `A4:Q22` | `V` | 3 ô `Q12:Q14` *"Tạo vùng ADJUSTMENT ZONE từ cột R"* + 9 chặng khai mà không tồn tại | chặng 4 |
| `G7-26` | `Daily RP test` | `A1:Z20` | `F+V` | sheet **không có trong bản offline** — chưa biết là gì | `GAP` mới |

### C · File PM — `1U8tDdaBVrgCFZLuxBUkgttyFvhHLpF1cXYg7N_sgn0M` (chủ: finance@apero.vn)

| # | Sheet | Dải | Kiểu | Lấy về để làm gì | Mở khoá |
|--:|---|---|:--:|---|---|
| `G7-27` | `PM_Unpivot` | `A1:AB2` | `V` | 28 tên cột gốc — **đối chiếu với `G7-08`**, lệch = bản bake đã cũ | §8 mục 2 |
| `G7-28` | **`PM_Unpivot`** | **`A1:AB1`** | **`V`** | ★ **cột nào giữ `Reference number`** | khoá §4 #2 |
| `G7-29` | `PM_Unpivot` | `<cột Ref>2:<cột Ref>` | `V` | đếm ô **rỗng** ⇒ **số dòng PM thật sự còn thiếu mã** — kiểm chéo nghi vấn 100% ở §0.4 | **chặng 2** |
| `G7-30` | *(liệt kê sheet)* | — | — | file có sheet `Draft_Hippo` chứa dữ liệu **PI**, không phải PM ⇒ cần bản đồ sheet của chính file PM | `GAP` mới |

### D · File A-CCR + P100 — cần tra ID trước

| # | File | Sheet | Dải | Kiểu | Lấy về để làm gì |
|--:|---|---|---|:--:|---|
| `G7-31` | `A-CCR_V2_Working` | `1.2 Ledger 112` · `1.1 Ledger 111` | `A2:H3` | `F` | công thức `FILTER(SORT(...))` đảo cột + `REGEXEXTRACT` tách `Tài khoản` |
| `G7-32` | `P100 _ Bank Transactions` | `Note` | `A1:B41` | `V` | ★ **41 dòng hướng dẫn do kế toán tự viết** — offline chỉ chụp được 3 ô. Đây là bản mô tả quy trình bằng lời của chính người làm |

**Phụ:** `A-CCR ▸ 0. CCR Flow-use!A1:AC32` (`V`) — sơ đồ quy trình vẽ bằng ô, đọc trọn thay vì suy từ mẫu.

---

## §3 · Cách chạy — một lượt, ghi ra JSON

```python
# _tools/read_live_cells.py — chạy sau khi có credential ở §1
import json, pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = pathlib.Path(".secrets/sheets-ro.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
svc = build("sheets", "v4",
            credentials=service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES))

PLAN = {
    "RAW": ("1xaD1RRAeqYsbDyzUhS0EuM4gGAmED9zajUT421PvtZU", [
        "Index!A1:O20",
        "Transaction Mapping L1!A3:AL6",
        "Transaction Mapping L1!A500:AL500",
        "Transaction Original!A2:G3",
        "Mapping Master!A3:P6",
        "RAW ITLData Management!A3:AB15",
        "ImportrangePM_Unpivot!A1:AB3",
        "ImportrangePE_Unpivot!A1:W2",
        "ImportrangePI_Unpivot!A1:X2",
        "ImportrangePC11_Entry Data!A1:T2",
        "Export Log!A1:G30",
        "Check list mapping!A1:F12",
        "SGO1Transaction Mapping L1!A1:A5",
    ]),
    "ADJUSTED": ("1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA", [
        "ITL Ledge!A1:BL13",
        "ITL Ledge!AX1:BI4",
        "RAW ITLData Management!A3:AB15",
        "Index!A4:Q22",
        "Daily RP test!A1:Z20",
    ]),
    "PM": ("1U8tDdaBVrgCFZLuxBUkgttyFvhHLpF1cXYg7N_sgn0M", [
        "PM_Unpivot!A1:AB2",
    ]),
}

out = {}
for tag, (sid, ranges) in PLAN.items():
    out[tag] = {"spreadsheet_id": sid}
    # đọc CÔNG THỨC và GIÁ TRỊ riêng — đây là điểm cốt tử, connector không làm được
    for mode in ("FORMULA", "FORMATTED_VALUE"):
        r = svc.spreadsheets().values().batchGet(
            spreadsheetId=sid, ranges=ranges, valueRenderOption=mode).execute()
        out[tag][mode] = {v["range"]: v.get("values", []) for v in r.get("valueRanges", [])}
    # bản đồ sheet — trả lời G7-30
    meta = svc.spreadsheets().get(spreadsheetId=sid, fields="sheets.properties").execute()
    out[tag]["sheets"] = [s["properties"]["title"] for s in meta["sheets"]]

pathlib.Path("live_cells.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("xong:", {k: len(v["sheets"]) for k, v in out.items()})
```

**Thứ tự ưu tiên nếu chỉ chạy được một phần:** `G7-02` → `G7-18` → `G7-16` → `G7-08` → `G7-21` → `G7-07`. Sáu mục này đóng được **cả 8 câu hỏi** ở §8 của process map.

---

## §4 · Bốn câu không nằm trong ô nào — phải hỏi người

| # | Câu hỏi | Hỏi ai | Vì sao ô không trả lời được |
|--:|---|---|---|
| 1 | **Ai** gõ `Reference number` vào `PM_Unpivot`, theo nhịp nào? | `???` — file PM chủ là **finance@apero.vn** (hộp chung, không phải người) | ô chỉ chứa kết quả, không chứa người |
| 2 | `Bản sao của ITL … 2/2 (ADJUSTED)` của **dungtt1@apero.vn** dùng làm gì, còn dùng không? | dungtt1 | quyết định kill-list |
| 3 | Vùng AUDIT lệch — **lỗi số liệu hay lỗi công thức đối chiếu**? Có kỳ nào sạch làm chuẩn? | Kế toán trưởng | `GAP-ITL-11`, ảnh hưởng độ tin của oracle |
| 4 | Sổ đăng ký khai `CFA2/CFA3/PLA1-3` — **đã bỏ, hay đang định làm**? | lanptn (chủ cả 2 file ITL) | quyết định phạm vi TO-BE |

---

## §5 · Đọc xong ghi vào đâu

| Kết quả | Ghi vào | Sửa mục nào |
|---|---|---|
| Công thức ghép `Mapping L1` (`G7-02`) | `Process-PM-den-ITL.md` §3 chặng 7 | thay `???` |
| 8 công thức import `ITL Ledge` (`G7-18`) | `Process-PM-den-ITL.md` §5 | **xác nhận hoặc bác** kết luận "12 cột bị rơi" |
| 28 tên cột PM (`G7-08`/`G7-27`) | `Process-PM-den-ITL.md` §3 chặng 5 | thay `???` |
| `$B$2`/`$B$3` (`G7-16`) | `Process-PM-den-ITL.md` §3 chặng 8 | thay `???` |
| Nguồn `Report I General Ledger` (`G7-21`) | `BA-05` + `ERD-Full-Detail.md` | dựng `RCN` |
| Mẫu số bảng đo (`G7-07`/`G7-22`) | `Process-PM-den-ITL.md` §0.4 mới | **kết luận 100% là thật hay giả** |
| Tên cột `Transaction Mapping L1` (`G7-04`) | `BA-05` §DD | bộ cột canonical |
| 41 dòng `Note` (`G7-32`) | `_GUIDE_09` §2 | bổ sung `OP-xx` |
| Bản đồ sheet 3 file (`G7-30`) | `_GUIDE_00_Inventory.md` | so với bản offline |

---

## Changelog

- **v0.2** (2026-08-20): Chạy thật 9 mục qua SA `claude-code-access@fpa-t-494007` (sẵn quyền trên file ADJUSTED). Kết quả ở `Ket-qua-G7-Live-ITL-Ledge.md`. Ghi rõ chặn còn lại = **quyền 2 file RAW + PM**, và **không đọc được giá trị** (timeout do cả workbook phải tính lại). Trả lời nghi vấn 100% ở §0.4: **bảng đo hỏng**.
- **v0.1** (2026-08-20): Khởi tạo. 32 mục `G7-01..32` chia 4 nhóm file, mỗi mục ghi rõ sheet + dải + đọc công thức hay giá trị. §0 ghi 4 thứ **đã lấy được live**: 3 file ID thật + 1 bản sao ngoài kiểm soát · tên 9 cột đo `[RAW ITL] Data Management` · cột `AL` = Accounting Layer · **số live 100% ghép PM, trái với suy luận từ bản offline — đã đánh dấu phải kiểm lại**. §1 ghi giới hạn: Drive connector **không trả công thức** và **cắt ở sheet đầu** với file lớn ⇒ bắt buộc một lượt Sheets API.
