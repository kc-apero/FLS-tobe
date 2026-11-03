# 01 — BRD: Business Requirements Document (dự án ITL)

**Version:** v0.6 *(⛔ header từng đứng ở v0.2 trong khi changelog đã tới v0.4 — sửa 27/08)* | **Chủ sở hữu:** COO-CFO | **Nguồn:** `NGUỒN-ASIS`, `NGUỒN-BUILD`, `NGUỒN-FILES` (đọc cấu trúc thật 2026-08-18)

> ⚠ **Đính chính framing (2026-08-24)** — con số **"6.843 ô nhập tay"** trong file này là số ô cột `Final` của 7 khối `Classifying→Manual→MID→Final` *(AS-IS)*, **không** = 6.843 lần người thật gõ; ô còn cờ `Input here` thật ≈ **5.018**, và engine P&L chỉ đọc **5 trường trong hợp đồng**. **TO-BE (`QĐ-owner-0820`):** bỏ tầng `MID`; `Final` = **kế toán nhập/sửa trực tiếp** *(không phải công thức)*; hợp đồng ra = **14 trường theo TÊN** *(`le`=`P`, không phải "13 cột theo vị trí"/`BL`)*. Số đo bên dưới giữ nguyên làm bằng chứng; chỉ **cách gọi tên** được đính chính. Chi tiết: [`_BA_UPDATE_ROADMAP §3c`](_BA_UPDATE_ROADMAP.md).

---

## 1. Bài toán

Sổ giao dịch trung tâm của toàn bộ hệ tài chính — `ITL` (Input Transaction Ledger) — đang chạy trên Google Sheets bằng tay. Bốn con số đo được:

| Số | Nguồn đo | Ý nghĩa |
|---|---|---|
| **72/116 bước (62%)** thủ công | `NGUỒN-ASIS` §00 | Kế toán nhấn nút / nhập tay / chạy Gscript |
| **6.843 ô nhập tay** trong `ITL Ledge` | đếm trực tiếp R3 sheet `ITL Ledge` | 7 khối × 1 trường, 2 người gõ (xem §2) |
| **6.711 dòng lệch audit** | đếm trực tiếp R8 vùng AUDIT | Số dòng `FALSE` khi đối chiếu ngược `Report I General Ledger` |

**Con số cuối là phát hiện mới của phiên đọc dữ liệu thật** và chưa từng có trong tài liệu nguồn nào. Vùng AUDIT của `ITL Ledge` tự báo cáo 6 cột lệch: `1356 · 552 · 146 · 2310 · 2308 · 39`. Nghĩa là **sổ hiện hành đang biết mình lệch nhưng không ai đóng được** — đây vừa là lý do phải code hoá, vừa là rủi ro: oracle không sạch 100%.

## 2. Bảy khối nhập tay — đã giải mã

`~6.843 dòng` không phải con số mơ hồ. Đọc từ `ITL Ledge` R1/R3/R7/R8: đó là **7 trường**, mỗi trường một khối 4 cột theo khuôn `Classifying → Manual input → MID → Final`.

| # | Cột | Trường được nhập tay | Số ô | PIC |
|---|---|---|---|---|
| 1 | S–V | `Budget Code (HDCode)` | **297** | LAN + THƯƠNG |
| 2 | W–Z | `Loại giao dịch (Payment Type)` | **179** | THƯƠNG |
| 3 | AA–AD | `Chủ dự toán (CDT1)` | **1.210** | THƯƠNG |
| 4 | AE–AH | `Thời điểm bắt đầu sử dụng dịch vụ` | **22** | THƯƠNG |
| 5 | AI–AL | `Thời điểm kết thúc sử dụng dịch vụ` | **22** | THƯƠNG |
| 6 | AM–AP | `Mã đối tác (ID Payee)` | **1.624** | THƯƠNG |
| 7 | AQ–AT | `File đính kèm: Hóa đơn` | **3.489** | THƯƠNG |
| | | **Tổng** | **6.843** | |

### 2b · Nhưng `ITL Ledge` chỉ là 31% — khối lượng thật là 22.360 ô

Kiểm kê `_GUIDE_00_Inventory` (2026-08-18) cộng mọi ô nhập tay **do chính file khai báo**:

| Workbook ▸ Sheet | Ô nhập tay | % |
|---|--:|--:|
| `ITL ADJUSTED` ▸ `ITL Ledge` (7 khối) | 6.843 | 31% |
| `GI` ▸ `CFA1` (173+173) + `CFA2 MID1` (4.689) | 5.035 | 23% |
| `PS` ▸ `CFA1` (333+333) + `CFA2 MID1` (3.755) | 4.421 | 20% |
| `SC` ▸ `CFA1` (327+327) + `CFA2 MID1` (3.730) | 4.384 | 20% |
| `OMC` ▸ `CFA1` (301+301) + `CFA2 MID1` (1.075) | 1.677 | 8% |
| **TỔNG** | **22.360** | 100% |

**Điểm nóng thật là các sheet `CFA2 MID1`** — 13.249 ô (59% toàn hệ) chỉ ở 4 sheet. Chúng nằm ở tầng L4 (phân bổ venture), **ngoài phạm vi IN hiện tại** của dự án ITL (§4).

✅ **Owner đã quyết mở phạm vi (`QĐ-ITL-05`, 2026-08-18):** ITL bao trọn vùng nhập tay của cả 4 ledger nền tảng. Đích khối lượng chính thức = **22.360 ô**. `GAP-ITL-17` **CLOSED**.

**Hệ quả kỹ thuật của quyết định này** — phải lan tiếp ở sóng S3:
- **Adapter E phình ra:** không chỉ *đọc* platform ledger mà còn *thay* vùng ADJUSTMENT/ALLOCATE của chúng.
- **Tầng L4 vào phạm vi:** 13.249 ô ở 4 sheet `CFA2 MID1` là logic **phân bổ venture**, tức ITL chạm L4 chứ không dừng ở L2 ⇒ `BA-02` §4 và `ORC-03` `IM4`/`IM6` cần cập nhật.
- **Kill-list dài thêm:** vùng ADJUSTMENT của 4 ledger nền tảng vào danh sách khai tử.

### 2c · Phân loại lại theo "có tới engine hay không" (sau khi đọc reader thật)

`DD-I04b` cho biết engine P&L **chỉ đọc `Final` của khối 1–5**. Khối 6 và 7 **không được đọc**. Chia lại 6.843 ô:

| Nhóm | Khối | Ô | % | Giá trị của việc gõ |
|---|---|--:|--:|---|
| **Tới engine** — sai là **sai P&L** | 1 HD · 2 Loại GD · 3 CDT1 · 4–5 ngày DV | **1.730** | 25% | Độ chính xác báo cáo |
| **Không tới engine** — phục vụ truy vết chứng từ | 6 Mã đối tác · 7 File hoá đơn | **5.113** | **75%** | Truy vết & kiểm toán, KHÔNG ảnh hưởng P&L |

**Hai kết luận đổi cách ưu tiên:**
1. **Ưu tiên đúng-đắn:** 1.730 ô của khối 1–5 là chỗ sai sẽ làm sai báo cáo ⇒ tự động hoá ở đây phải **đúng trước nhanh**, có đối soát oracle từng ô.
2. **Ưu tiên tiết-kiệm-công:** 5.113 ô của khối 6–7 tốn công người nhất nhưng **không rủi ro P&L** ⇒ được phép "đủ tốt", và là chỗ thu hồi công sức nhanh nhất. Cả hai đều là tra cứu (kéo link từ PI/PE, tra bảng đối tác) nên khả thi cao.

**Ý nghĩa cho thiết kế:** 3 khối lớn nhất (đính kèm hoá đơn 3.489 · mã đối tác 1.624 · chủ dự toán 1.210 = **93% khối lượng**) đều là **tra cứu/phân loại**, không phải phán đoán kế toán. Ngược lại 2 khối ngày dịch vụ chỉ 22 ô mỗi cái — nhỏ, có thể giữ nhập tay.

## 3. Mục tiêu (Goal)

| ID | Goal | Đo bằng |
|---|---|---|
| **G-I01** | Sổ ITL chạy tự động, không phụ thuộc thao tác tay | % bước thủ công: 62% → `???` (`GAP-ITL-10`) |
| **G-I02** | Mọi con số truy được về nguồn | % dòng ITL có lineage đầy đủ = 100% |
| **G-I03** | Engine P&L đọc ITL mới **không sửa code** | Số dòng code engine phải sửa khi cutover = 0 |
| **G-I04** | Sổ tự biết mình đúng/sai, không cần người soi | 6.711 dòng lệch audit → 0 hoặc **có lý do đã ký** |
| **G-I05** | Người vận hành làm việc phán đoán, không làm việc gõ | 6.843 ô nhập tay → chỉ còn phần *không suy được thành luật* |

Chuỗi truy ngược lên chương trình FIN ERP: `G-I01..G-I05` phục vụ **`G-03`** (số liệu đáng tin) và **`G-04`** (nhìn thấy sớm). ITL là bước "dữ liệu sạch" mà `P-01` nói tới — không có nó thì mọi phân tích phía sau là cát.

## 4. Phạm vi

**IN**

| Hạng mục | Chi tiết |
|---|---|
| 6 adapter nguồn | A P100 Payment · B Cash/Bank · C A-CCR reconcile · D HR/H1000 · E Platform (GI/OMC/SC/PS) · F AP/AR (dựng mới, gói riêng — `QĐ-ITL-03`) |
| Dây chuyền S1–S5 | adapters → `Transaction Original` → `Transaction Mapping L1` → `ITL RAW` → `ITL Ledge` |
| 3 hợp đồng dữ liệu | `ITL-CONTRACT` · `ITL-CANON` (36 cột) · `MAPPING-MASTER` |
| 4 vùng của `ITL Ledge` | BASE+IMPORT · ADJUSTMENT · ALLOCATE · AUDIT |
| ⭐ **Hai màn NHẬP sổ nguồn** *(`QĐ-ITL-90`, 2026-09-07)* | **`F04`** `P100 \| Bank Transactions` ▸ `Bank Transactions` *(**7.715 dòng × 10 cột**, hdr dòng **2**, dữ liệu từ dòng **4**)* — ⚠ **sửa 07/09:** `7.484` là sheet **TRÙNG TÊN** bên `A-CCR_V2_Working`. ⭐ Tầng kế toán **GÕ VÀO** là **67 sheet `R \|`** *(**16.625 dòng**)*; sheet này là **đầu ra của máy** · **`F05`** `P100 \| Cash Ledger` ▸ `Cash Ledger Transactions` *(**1.847 dòng**, hdr dòng 2)* — *"như trên ggsheet"*. ⛔⛔ **Lật 2/4 nhóm của `QĐ-ITL-23`**; xem ghi chú dưới bảng |
| ⭐ **Ghép `PM ↔ Transaction`** *(`QĐ-ITL-48`)* | ⚠ **Đã có, ⛔ không phải việc mới:** `POST /match` + `/pm-candidates` chạy thật trên sổ thật *(`QĐ-ITL-61`)*, màn `F01` xong *(`QĐ-ITL-80`)*, đường **bỏ ghép** có *(`QĐ-ITL-69`)* |
| Hạ tầng | orchestration (DAG) · DQ gate · lineage · versioning/snapshot |

> ⭐⭐⭐ **Mở phạm vi 2026-09-07 — `QĐ-ITL-90` / `CR#10` loại 1.** Owner chốt: *"FLS bao gồm các giao diện nhập Bank Transaction và Cash Ledger như trên ggsheet và có thao tác mapping PM với Transactions"*.
>
> ⛔⛔ **Phải nói thẳng cái bị lật, ⛔ không sửa lặng lẽ:** `QĐ-ITL-23` *(22/08)* chốt Google Sheets giữ vai **nhập liệu thô VĨNH VIỄN** cho **4 nhóm**. Nay **2 nhóm bị lấy lại** — *nạp sao kê* và *nhập số dư thật*; **2 nhóm ở lại** — *lệnh chi (Google Form)* và *bảng danh mục*. Luật **`T4`** *(dữ liệu thô từ ngoài ⇒ giữ Sheets lâu nhất)* **hẹp lại**, và màn **`S4` Nạp sao kê** — bị **BỎ** 22/08 vì đúng luật `T4` — nay **sống lại**.
>
> ⛔ **Lý do gốc của `T4` ⛔ KHÔNG biến mất:** *60+ ngân hàng, mỗi bank một định dạng, chưa có API*. Nó ⛔ không chặn quyết định này vì đây là **hai tầng khác nhau** — 60+ sheet `R \| <tài khoản>` là nơi **sao kê thô** rơi xuống, còn `Bank Transactions` là **bảng đã gộp, một khuôn duy nhất**. `QĐ-ITL-90` lấy **tầng đã gộp**. ⇒ Tầng thô **chưa được quyết**: `GAP-SCOPE-01`.
>
> ⛔⛔ **Và một câu phải trả lời TRƯỚC khi gõ dòng code nào — `GAP-SCOPE-02`:** kế toán gõ vào FLS rồi thì **sheet trên P100 còn được ghi nữa không?** *Không* ⇒ P100 mất một nguồn đang chảy. *Có* ⇒ ta vừa dựng lại đúng **"ghi đôi"** mà `QĐ-ITL-32` đã bỏ. ⛔ ⛔ Không tự chọn (`R-A4`).

**OUT**

| Không làm | Vì sao |
|---|---|
| Viết lại engine P&L (L3–L5) | Đã chạy thật trên BigQuery. ITL là **producer**, engine là **consumer read-only** (`P-04`) |
| Sổ thuế / phần mềm kế toán pháp định | ITL là sổ quản trị |
| OCR hoá đơn đại trà | Khối 3.489 ô đính kèm giải bằng tra cứu link, không bằng OCR |
| Báo cáo/dashboard mới | `L5 không được tạo số mới` — trình bày không thuộc phạm vi ITL |
| Dựng lại cổng đối soát tiền | A-CCR đã sở hữu; adapter C **đọc** (chờ `GAP-ITL-04`) |

## 5. Thước đo thành công

| ID | Thước đo | Đích |
|---|---|---|
| `KPI-I01` | Dòng ITL RAW khớp `Transaction Mapping L1` cũ | 100% theo dòng & tổng (dung sai = 0 cho `IM1`) |
| `KPI-I02` | Ô nhập tay còn lại **trong phạm vi ITL** | 6.843 → phần không suy được thành luật; công bố tỷ lệ tự động hoá từng khối |
| `KPI-I02b` | Ô nhập tay còn lại **toàn hệ** (chính thức, `QĐ-ITL-05`) | 22.360 → phần không suy được thành luật; công bố tỷ lệ tự động hoá từng ledger |
| `KPI-I03` | Dòng lệch vùng AUDIT | 6.711 → 0 **hoặc** mỗi dòng còn lại có lý do đã ký |
| `KPI-I04` | Bước thủ công trong luồng | 62% → `???` |
| `KPI-I05` | Mắt xích Gsheet bị cắt | Theo kill-list mỗi milestone (`ORC-03`) |
| `KPI-I06` | Số kỳ chạy song song ổn định trước cutover | ≥ 1 kỳ (`IM7`) |
| `KPI-I07` | Số dòng code engine phải sửa khi cutover | **0** — đo được: engine đọc đúng **14 trường** `A–G,P,R,V,Z,AD,AH,AL` *(`le`=`P` không `BL`)* (`DD-I04b`) |

## 6. Bối cảnh: đánh giá kiến trúc AS-IS

`NGUỒN-ASIS` chấm hệ hiện tại hạng **B−** — *ý tưởng đúng, thi công quá tải*. Giữ lại 5 điểm mạnh, sửa 3 gốc rối:

**Giữ:** xương sống ITL thật · tách RAW ↔ ADJUSTED · tư duy đa chiều (làn CFA/PLA, chiều Venture/LE/KRF) · kỷ luật ELT theo pha · kiểm soát cài sẵn (A-CCR balance theo ngày).

**Sửa:** đặt tên hỗn tạp (trộn mã, ngôn ngữ, phiên bản, **tên người** — `Luận's File`, `PIC: LAN + THƯƠNG`) · pha chồng lấn (Calculate/Allocate/Report cùng ghi một file) · chạm trần công cụ (2 mắt xích lõi bị **huỷ** vì Gsheet không kham bảng lớn).

## 7. Decision log

Quyết định dự án ghi ở `../00_MASTER_INDEX.md` §3: `QĐ-ITL-01` namespace · `QĐ-ITL-02` `IM0–IM7` · `QĐ-ITL-03` AP/AR gói riêng · `QĐ-ITL-04` bộ tài liệu độc lập.

Quyết định chương trình kế thừa (ghim program `BA-01` v0.2) có liên quan trực tiếp: `QĐ-VOI-02` ingest file-first có contract gate · `QĐ-VOI-06` đa tiền tệ + tag intercompany là thuộc tính bậc nhất từ schema đầu tiên.

## 8. GAP mở của file này

| ID | Câu hỏi | Ai đóng |
|---|---|---|
| **`GAP-SCOPE-01`** ⛔⛔ | **Tầng sao kê THÔ có vào phạm vi không?** `QĐ-ITL-90` lấy **tầng đã gộp** *(`Bank Transactions`, một khuôn)*; còn **60+ sheet `R \| <tài khoản>`** — mỗi bank một định dạng, ⛔ chưa có API — **⛔ chưa ai quyết**. Đây chính là lý do gốc của luật `T4`, và nó ⛔ **không biến mất** | COO-CFO |
| **`GAP-SCOPE-02`** ⛔⛔ | **Gõ vào FLS rồi thì P100 còn được ghi nữa không?** *Không* ⇒ `QĐ-ITL-38` *(Postgres = bản ghi chính)* nay áp cả cho `STM`, và **P100 mất một nguồn đang chảy**. *Có* ⇒ ta vừa dựng lại đúng **"ghi đôi"** mà `QĐ-ITL-32` đã bỏ. ⛔ **Chặn việc code** `F04`/`F05` | COO-CFO + Kế toán |
| **`GAP-SCR-10`** ⛔ | **`F04`/`F05` ⛔ chưa có `SCREEN_SPEC`.** `BA-06` mới có `F01`·`F02`·`F03`·`F06`. ⛔ Tôi ⛔ không bịa hình dạng một màn rồi gọi đó là đặc tả *(`R-A1`)* | BA |
| `GAP-ITL-10` | Đích cho `KPI-I01`/`KPI-I04`: giảm thủ công xuống bao nhiêu % là "đạt"? | COO-CFO |
| ~~`GAP-ITL-17`~~ | ~~Mở phạm vi sang 4 ledger nền tảng?~~ | **CLOSED** 2026-08-18 — `QĐ-ITL-05` **CÓ** |
| `GAP-ITL-18` | `QĐ-ITL-05` đưa L4 (phân bổ venture) vào phạm vi ⇒ ranh giới ITL ↔ engine ACA v2 (đang làm phân bổ trên BigQuery) ở đâu? | COO-CFO + Tech Lead |
| `GAP-ITL-11` | **6.711 dòng lệch audit** là lỗi dữ liệu cũ hay lỗi công thức audit? Nếu là lỗi dữ liệu, oracle không sạch ⇒ phải chọn kỳ chuẩn khác để đối chiếu | Kế toán trưởng + PIC ADJUSTMENT |

## Changelog
- **v0.6** *(2026-09-07, rà AS-IS)*: ⛔ **Sửa con số `F04` trong §4** — `7.484` là sheet **TRÙNG TÊN** bên `A-CCR_V2_Working`; bản `P100` là **7.715 dòng × 10 cột** *(hdr dòng 2, dữ liệu dòng 4)*. ⭐ Ghi thêm: tầng kế toán **gõ vào** là **67 sheet `R \|`** *(**16.625 dòng**)*, sheet `Bank Transactions` là **đầu ra của máy**.
- **v0.5** *(2026-09-07, `QĐ-ITL-90` / `CR#10`)*: ⭐⭐⭐ **MỞ PHẠM VI — FLS cầm luôn hai màn NHẬP `Bank Transaction` + `Cash Ledger`.** §4 thêm hai hạng mục `IN` *(`F04` **7.715** dòng · `F05` 1.847 dòng)* + một hạng mục **xác nhận** *(ghép `PM ↔ Transaction` đã có từ `QĐ-ITL-48`, ⛔ không phải việc mới)*. ⛔⛔ **Nó lật `QĐ-ITL-23`** — quyết định 22/08 chốt Google Sheets giữ vai nhập liệu thô **VĨNH VIỄN** cho 4 nhóm; nay **2/4 bị lấy lại**. Hẹp luật **`T4`**, hồi sinh màn **`S4`** đã BỎI. ⛔ **Ba câu chưa ai trả lời**, ghi ra chứ ⛔ không tự chọn *(`R-A4`)*: `GAP-SCOPE-01` *(tầng sao kê thô 60+ định dạng)* · `GAP-SCOPE-02` *(P100 còn được ghi nữa không — nếu có thì đó là **ghi đôi**)* · `GAP-SCR-10` *(⛔ chưa có `SCREEN_SPEC`)*
- v0.4 (2026-08-18): Thêm §2c — sau khi đọc reader thật: **75% ô nhập tay (5.113) KHÔNG tới engine**, chỉ 1.730 ô ảnh hưởng P&L ⇒ đổi cách ưu tiên tự động hoá.
- v0.3 (2026-08-18): Owner phê **`QĐ-ITL-05` mở phạm vi** — đóng `GAP-ITL-17`, `KPI-I02b` thành đích chính thức, mở `GAP-ITL-18` (ranh giới với engine ACA v2 ở tầng L4).
- v0.2 (2026-08-18): **Sửa con số lõi** sau kiểm kê 11 workbook: nhập tay toàn hệ = **22.360 ô**, `ITL Ledge` chỉ 31%. Thêm §2b, `KPI-I02b`, `GAP-ITL-17` (phạm vi 4 ledger nền tảng).
- v0.1 (2026-08-18): Khởi tạo — bài toán 3 con số, **giải mã 7 khối nhập tay từ file thật**, 5 goal, phạm vi IN/OUT, 7 KPI. Phát hiện mới: 6.711 dòng lệch vùng AUDIT (`GAP-ITL-11`).
