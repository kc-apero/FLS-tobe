# Sổ đối chiếu AS-IS ↔ FLS — vật mang của phép đo tính khớp

**Version:** v0.1 | **Ngày:** 2026-09-07 | **Chủ sở hữu:** BA
**Bước:** `Đ1` của lộ trình `Đ1…Đ6` — xem `Do-tinh-khop-ASIS-FLS.html`
**Nguồn AS-IS:** `FIN-ERP/AS-IS system/Accounting_Files/RAW_guide` — 11 tệp, 5.773 dòng, **chụp 2026-08-18**
**Nguồn FLS:** mã tại mốc `17df1d9` — 17 tuyến API · 18 bảng/view · 1.024 phép thử

---

## §0 · Đọc sổ này thế nào

> ⛔⛔ **Đây ⛔ KHÔNG phải bản đánh giá.** Nó là **vật mang**: một dòng cho một đơn vị logic.
> Mọi bước `Đ2…Đ6` chỉ làm **một việc** — đổi cột `Bậc` của những dòng ở đây.
> Dòng nào ⛔ chưa có phép so chạm tới thì **mặc định `K0`**, ⛔ không phải "chắc là ổn".

**Thang bậc** *(`Do-tinh-khop-ASIS-FLS.html` §02)*

| Bậc | Nghĩa |
|:--:|---|
| `K0` | **chưa đo** — ⛔ không phép so nào chạm tới |
| `K1` | **biết lệch** — đã đo, lệch, **và phân loại được nguyên nhân** |
| `K2` | **khớp có điều kiện** — khớp trong phạm vi đã khai *(một kỳ / một lát / một sheet)* |
| `K3` | **khớp đầy đủ** — khớp toàn tập, có phép thử khoá lại |
| `K4` | **khớp + cưỡng chế** — có cổng chạy tự động, **và cổng ấy đã thấy đỏ** |

**Năm loại logic** — `L1` hình dạng · `L2` phép tính · `L3` luật nghiệp vụ · `L4` thao tác · `L5` bất biến ngầm.

**Số dòng của sổ này — khai ra để lần sau đếm lại được:**

| Nhóm | Dòng | Ghi chú |
|---|--:|---|
| `L4` thao tác `OP-01…OP-24` | **24** | trích bằng máy từ `_GUIDE_09` §2 |
| `L1` hình dạng — 6 chỗ trong phạm vi | **6** | `Do-tinh-khop-ASIS-FLS.html` §05 |
| `L2` phép tính | **6** | |
| `L3` luật nghiệp vụ | **5** | |
| `L5` bất biến ngầm đã nhìn thấy | **5** | ⛔ danh sách **chưa đóng** — `Đ5` sẽ mở rộng |
| **TỔNG** | **46** | |

---

## §1 · `L4` · Hai mươi bốn thao tác kế toán

> Trích bằng máy từ `_GUIDE_09` §2 — **24/24**, mỗi cái có bằng chứng là một ô thật.
> ⚠ **17/24 còn `???` ở cột *Ai*** và **4/24 ở cột *Khi nào*** trong chính bộ AS-IS.
> ⛔ Sổ này **⛔ không lấp** những ô ấy *(`Đ-5`)* — chúng đóng bằng **18 câu phỏng vấn** đã soạn ở `_GUIDE_09` §6.

| `OP` | Thao tác | Chỗ tương ứng trong FLS | Bậc | Căn cứ / vì sao |
|---|---|---|:--:|---|
| `OP-01` | Điền sao kê vào sheet `R \| <tài khoản>` | ⛔ **chưa có** — sẽ là `F04` | `K0` | `CR#10`. ⛔ Chặn: `GAP-ASIS-01` *(`_GUIDE_08` ⛔ không tồn tại)* |
| `OP-02` | Gõ `Reference number` vào PM | ⛔ **ở lại Google Form** *(`QĐ-ITL-90` ⛔ không đụng)* | `K2` | Ở lại có chủ ý ⇒ khớp **theo định nghĩa**, nhưng phạm vi hẹp |
| `OP-03` | Luật **1 khoá = 1 mã** `ID PMLine ↔ Reference` | `POST /queue/{id}/match` + `fls_pm_link` | `K1` | ⛔⛔ **Luật AS-IS SAI**: `CR#1-a` đo **526 phiếu mang 2–36 reference** ⇒ FLS ghép theo **DÒNG**, ⛔ không theo phiếu |
| `OP-04` | Nhập thu chi từng sheet rồi chạy script | ⛔ **chưa có** — sẽ là `F05` | `K0` | `CR#10` |
| `OP-05` | Nạp sổ ngân hàng **trước 11:00** | ⛔ **chưa có** | `K0` | `ArchitecturePack` §4.2 đã thiết kế `TST.sla`, ⛔ chưa dựng |
| `OP-06` | Điền `HD code` nếu chưa có | `F02` + `POST /adjust`, khoá bởi `FLS-UNKNOWN-CODE` | `K2` | `QĐ-ITL-86` — 73 mã `fls_mapping_master`; ⛔ chưa UAT |
| `OP-07` | Gõ tay **7 trường** vùng ADJUSTMENT | `F02` panel + `POST /adjust` | `K2` | `QĐ-ITL-68` kế toán 2/2 xác nhận đủ trường; ⛔ chưa UAT *(`B7`)* |
| `OP-08` | Gõ tay ADJUSTMENT **4 ledger nền tảng** | ⛔ **chưa có** | `K0` | `QĐ-ITL-05` đưa vào phạm vi; chặn `GAP-ITL-18` |
| `OP-09` | Bấm `Run` đẩy dữ liệu qua từng chặng | `tools/nap_that.py` + `chay_nap.py` — **chỉ phần đuôi** | `K1` | FLS thay `Run` **từ `Transaction Mapping L1` trở đi**; chặng gộp `R \|` → `Bank Transactions` ⛔ vẫn là `Run` thủ công |
| `OP-10` | Kiểm kê + **ký xác nhận quỹ** cuối tháng | ⛔ **cố ý ⛔ không dựng** | `K1` | `QĐ-ITL-27`: kế toán trưởng ⛔ không tham gia ⇒ màn `S7` **BỎ**, chữ ký sẽ là **chữ ký giả** |
| `OP-11` | Lập biên bản chốt quỹ / tháng | ⛔ **cố ý ⛔ không dựng** | `K1` | như `OP-10` |
| `OP-12` | Đối chiếu ngược `ITL Ledge` ↔ `Report I General Ledger` | ⛔ **⛔ không dựng** | `K1` | `QĐ-ITL-52`: lệch giữa hai sổ là **điều MONG ĐỢI**, nó đo khối lượng đã sửa. `GAP-ITL-11` 6.711 dòng |
| `OP-13` | Xoá giao dịch + ghi nhật ký xoá | `POST /unmatch` + `fls_journal` — **⛔ không xoá, chỉ thêm bút toán** | `K1` | `INV-I08` sổ chỉ-thêm. **Cơ chế khác hẳn AS-IS** ⇒ ⛔ không thể "khớp", chỉ có thể **thay thế được hay không** |
| `OP-14` | Áp tỷ lệ chia lợi nhuận từng đối tác | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06`: chuỗi tính ở `AperoGroup_Payment` **ở ngoài** |
| `OP-15` | Chuyển lỗ luỹ kế sang tháng sau | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06` |
| `OP-16` | Cộng dồn khoản chưa trả | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06` |
| `OP-17` | Đánh dấu ngừng hợp tác → dừng chi | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06` |
| `OP-18` | Xác nhận số với đối tác trước khi chi | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06` |
| `OP-19` | Chốt Audit theo tháng × 3 kênh | ⛔ **ngoài phạm vi** | `K0` | `QĐ-ITL-06` |
| `OP-20` | Xuất/refresh ITL + ghi log dòng-cột | `fls_run` + `row_count` | `K2` | Cơ chế tương đương; ⛔ chưa đối chiếu với `Export Log` **9.784 dòng** |
| `OP-21` | Duy trì **danh mục tài khoản** + dải đọc Nợ/Có | ⛔ **chưa có** — `BNK`, 3.003 dòng | `K0` | ⛔ Chặn `F04`. `ArchitecturePack` §2 đã thiết kế |
| `OP-22` | Duy trì **danh mục quỹ** + số dư đầu kỳ | ⛔ **chưa có** — `CSH`, 997 dòng | `K0` | ⛔ Chặn `F05` |
| `OP-23` | Ghi nhận & theo dõi **sự cố dữ liệu** | ⛔ **chưa có** | `K0` | `Check list mapping`. ⚠ ⛔ Chưa ai hỏi *có cần không* |
| `OP-24` | Duy trì sổ đăng ký file HR theo tháng | ⛔ **ngoài phạm vi** | `K0` | Thuộc `H1000` |

**Đếm theo bậc:** `K0` **13** · `K1` **6** · `K2` **5** · `K3` **0** · `K4` **0**.

> ⛔⛔ **Đọc con số ấy cho đúng.** **`K4` = 0** nghĩa là **⛔ chưa một thao tác kế toán nào**
> có cổng tự động chứng minh FLS thay thế được nó. Đó ⛔ **không** nói FLS sai — nó nói
> **phép đo ⛔ chưa tồn tại**. Đúng thứ `Đ4` sinh ra để làm.
>
> ⭐ Và **6 dòng `K1`** là phần **đáng đọc nhất**: cả sáu là chỗ FLS **cố ý ⛔ không khớp**
> AS-IS, mỗi chỗ có một quyết định đứng sau. ⛔ Chúng ⛔ **không được** âm thầm bị kéo lên `K3`.

---

## §2 · `L1` · Hình dạng — 6 chỗ trong phạm vi

| # | Sheet | Hình dạng AS-IS *(đo 18/08)* | Chỗ trong FLS | Bậc |
|:--:|---|---|---|:--:|
| 1 | `Transaction Mapping L1` | hdr dòng **3**, dữ liệu từ dòng **5** *(dòng 4 TRỐNG)* | `fls/adapters/bank.py` · `nguon.BAN_SAO_RAW` | `K3` |
| 2 | `ITL Ledge` | hdr dòng **10** | `fls/oracle/` · `SO_GOC_ADJUSTED` | `K3` |
| 3 | `Mapping Master` | 73 mã `hd` | `fls_mapping_master` | `K3` |
| 4 | `2. CCR` dòng `226` | ma trận — **một cột một ngày** | ⛔ **chưa đọc** | `K0` |
| 5 | `Bank Transactions` *(**P100**)* | hdr dòng **2**, dữ liệu dòng **4**, **7.715** × **10** cột | ⛔ **chưa có** → `F04` | `K0` |
| 6 | `Cash Ledger Transactions` | hdr dòng **2**, **1.847** dòng | ⛔ **chưa có** → `F05` | `K0` |

⚠ **Bẫy đã ghi lại:** có **hai sheet TRÙNG TÊN** `Bank Transactions` —
bản `P100` **7.715 dòng** *(dòng 5 ở trên)* và bản `A-CCR_V2_Working` **7.484 dòng**.
Nhầm hai bản này đã làm **5 chỗ tài liệu sai** ngày 06/09.

---

## §3 · `L2` · Phép tính

| # | Phép tính AS-IS | Chỗ trong FLS | Bậc | Ghi chú |
|:--:|---|---|:--:|---|
| 1 | `Classifying = iferror(<ô canon>, 'Need to manual input')` — 7 khối | `fls/ledger/classifying.py` | `K3` | `QĐ-ITL-53`; đo **68.915 ô** khớp 100% |
| 2 | Vùng `ALLOCATE` — `AU`/`AV`/`AW` | `fls/ledger/allocate.py` | `K3` | `QĐ-ITL-65`: cả ba **suy lại được** ⇒ ⛔ không lưu cột |
| 3 | Cột `Final` 7 khối | thước chuẩn `fls/oracle/` | `K3` | parity **69.510/69.510 ô**, 23 kỳ, ⛔ không dung sai |
| 4 | `112!A3 = FILTER(SORT(…))` — **đảo cột** `Reference` → `Số chứng từ` | ⛔ **chưa tái lập** | `K0` | Nằm ở chặng 3, thượng nguồn chỗ FLS bắt đầu |
| 5 | `112!H3 = REGEXEXTRACT(…"\|\s*([A-Z0-9]+)_")` — tách `Tài khoản` từ `Source` | ⛔ **chưa tái lập** | `K0` | Cần cho `F04` — `Source` mang mã sheet tài khoản |
| 6 | Phép **gộp** `R \|` → `Bank Transactions` *(`OP-09` bấm Run)* | ⛔ **chưa tái lập** | `K0` | ⛔⛔ **Đây là phép đo số 1 của `Đ3`** — xem §5 |

---

## §4 · `L3` · Luật nghiệp vụ

| # | Luật AS-IS | Trạng thái ở FLS | Bậc |
|:--:|---|---|:--:|
| 1 | `OP-03` **1 khoá = 1 mã** `Reference number` | ⛔ **LUẬT AS-IS SAI** — đo **526 phiếu** mang 2–36 reference ⇒ ghép theo **DÒNG** | `K1` |
| 2 | Nạp sổ **trước 11:00** hằng ngày | ⛔ chưa có phép đo nào | `K0` |
| 3 | Dung sai ghép Σ = **1.000 VND** *(và ≤ 0,5%, lấy cái nhỏ hơn)* | `QĐ-ITL-57` + `QĐ-ITL-63`, có cổng | `K4` |
| 4 | **Ngoại tệ ⛔ không có dung sai** | `QĐ-ITL-62`, có cổng | `K4` |
| 5 | `DIF = 0` **đúng từng đồng**, đọc ở dòng `226` | ⛔ chưa đọc `2. CCR` | `K0` |

⭐ **Hai dòng `K4` là hai chỗ duy nhất trong cả sổ đạt bậc cao nhất** — và ⛔ không phải ngẫu nhiên:
cả hai đều là luật **owner chốt bằng một câu**, rồi **thành một cổng đã thấy đỏ** trong cùng ngày.
Đó là hình dạng mà 44 dòng còn lại cần đi tới.

---

## §5 · `L5` · Bất biến ngầm — danh sách **CHƯA ĐÓNG**

> ⛔⛔ **Loại nguy hiểm nhất, và là loại duy nhất ⛔ không tự lộ ra.** ⛔ Không có bản khai để so —
> phải **đi tìm**. Năm mục dưới là thứ đã **nhìn thấy** khi rà, ⛔ chưa cái nào được giải thích.

| # | Thứ nhìn thấy | Quy mô | Vì sao đáng ngờ |
|:--:|---|--:|---|
| 1 | `P100 Bank ▸ Log` — `Action \| Composite Key` | **171.358** dòng | ⛔⛔ **Một nhật ký thay đổi ĐÃ TỒN TẠI**, ⛔ chưa tài liệu ITL nào nhắc. Khoá dạng `20250211\|\|66923.25\|FT25042584880113` — **rất giống** khoá đối sánh `INV-I04b` mà bộ này đang tự thiết kế |
| 2 | Cột `Check trùng` và `Num` ở `Bank Transactions` | 2 cột | ⛔ Chưa ai nói chúng làm gì. `Check trùng` **rất có thể** là phép chống trùng mà `F04` phải thay |
| 3 | Sheet `Bank Transactions_Filter` | **7.813** × 12 cột | ⛔⛔ **Nhiều hơn bản gốc 98 dòng và thừa 2 cột.** Một bản lọc mà **to hơn** thứ nó lọc |
| 4 | `P100 Cash ▸ CANhật ký xử lý Giao dịch` | **1.015** dòng | Ghi *"Đã xóa ngày 13/10/…"* ⇒ có **quy trình xoá có vết** đang chạy |
| 5 | Chênh **tầng nhập ↔ tầng gộp** | **16.625 → 9.331** | **7.294 dòng (44%)** ⛔ chưa phân loại. Có thể là bộ lọc ngày · nguồn chết · đếm khác đơn vị — hoặc **mất thật** |

---

## §6 · Cái sổ này CỐ Ý ⛔ không chứa

| Không chứa | Vì sao |
|---|---|
| **≈96 sheet Tầng A còn lại** *(trích được 43, kiểm kê ước 102)* | Nằm ngoài đường FLS đi qua ⇒ `K0` **đúng theo thiết kế**. Đưa vào chỉ làm loãng |
| **444 sheet toàn hệ** | `_PLAN` §5 đã phân tầng; Tầng C là kill-list |
| `H1000` lương · 4 ledger nền tảng | `QĐ-ITL-05` có trong phạm vi ITL nhưng **chưa tới lượt** |
| Ô `???` của bộ AS-IS | `Đ-5` — ⛔ không lấp bằng suy đoán. Đóng bằng **18 câu phỏng vấn** `_GUIDE_09` §6 |

---

## §7 · Việc kế tiếp

| Bước | Việc | Chặn gì |
|:--:|---|---|
| `Đ2` | Đối chiếu hình dạng 6 chỗ §2 | ⛔ `GAP-ASIS-01` chặn chỗ 5–6 *(`_GUIDE_08` ⛔ không tồn tại)* |
| `Đ3` | **Phép đo số 1: phân loại 7.294 dòng chênh** *(§5 mục 5)* | ⛔ cần đọc live — máy hiện ⛔ không có mạng |
| `Đ4` | Kéo 24 dòng `L4` từ `K0`/`K1` lên | ⛔ 17/24 ô *Ai* còn `???` ⇒ cần **18 câu phỏng vấn** |
| `Đ5` | Đóng 5 mục §5 | ⛔ cần kế toán trả lời |
| `Đ6` | Cưỡng chế | sau cùng |

---

## Changelog
- **v0.1** *(2026-09-07)*: Khởi tạo — bước `Đ1`. **46 dòng** *(24 `L4` + 6 `L1` + 6 `L2` + 5 `L3` + 5 `L5`)*, trích bằng máy phần trích được *(24 `OP` từ `_GUIDE_09` · 17 tuyến · 18 bảng · 43 sheet Tầng A)*. ⛔⛔ **Kết quả đáng nói nhất: `K4` = 2/46, và ⛔ KHÔNG một thao tác kế toán nào đạt `K4`** — nghĩa là **phép đo chưa tồn tại**, ⛔ không phải FLS sai. ⭐ Sáu dòng `K1` là chỗ FLS **cố ý ⛔ không khớp** AS-IS, mỗi chỗ có một quyết định đứng sau; ⛔ chúng ⛔ không được âm thầm kéo lên `K3`.
