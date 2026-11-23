# Sổ đối chiếu AS-IS ↔ FLS — vật mang của phép đo tính khớp

**Version:** v1.2 | **Ngày:** 2026-09-07 | **Chủ sở hữu:** BA
**Bước:** `Đ1` + `Đ2` của lộ trình `Đ1…Đ6` — xem `Do-tinh-khop-ASIS-FLS.html`
**Nguồn AS-IS:** `FIN-ERP/AS-IS system/Accounting_Files/RAW_guide` — 11 tệp, 5.773 dòng, **chụp 2026-08-18**
**Nguồn FLS:** mã tại mốc `17df1d9` — 17 tuyến API · 18 bảng/view · **1.027** phép thử

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
| `OP-21` | Duy trì **danh mục tài khoản** + dải đọc Nợ/Có | ⛔ chưa dựng ở FLS — nguồn là `BankAccountList`, ~~3.003~~ ⭐ **70 dòng thật** | `K1` | ⚠ **⛔ KHÔNG chặn `F04`** *(sửa 07/09)*: danh mục **đọc được**, và nó ⭐⭐ **tự khai DẢI ĐỌC** `Range_Condition`/`Range_Debit`/`Range_Credit` *(vd `!L3:L`·`!M3:M`·`!N3:N`)* cho từng tài khoản — **hợp đồng đọc-được-bằng-máy THỨ HAI** của hệ, sau bản khai dòng 1. Còn có cột tự đối soát `Check vs Bank Transactions`. `3.003` là **ô LƯỚI** |
| `OP-22` | Duy trì **danh mục quỹ** + số dư đầu kỳ | ⛔ chưa dựng ở FLS — nguồn là `Cash Ledger List`, ~~997~~ ⭐ **15 dòng thật** | `K1` | ⚠ **⛔ KHÔNG chặn `F05`** *(sửa 07/09)*: cùng khuôn với `OP-21`, có `Check vs Cash Ledger`. `997` là **ô LƯỚI** — lần thứ **năm** trong một ngày |
| `OP-23` | Ghi nhận & theo dõi **sự cố dữ liệu** | ⛔ **chưa có** | `K0` | `Check list mapping`. ⚠ ⛔ Chưa ai hỏi *có cần không* |
| `OP-24` | Duy trì sổ đăng ký file HR theo tháng | ⛔ **ngoài phạm vi** | `K0` | Thuộc `H1000` |

**Đếm theo bậc:** `K0` **13** · `K1` **6** · `K2` **5** · `K3` **0** · `K4` **0**.

> ⚠ **Con số trên là của `Đ1` *(24 dòng `L4` thao tác)* và ⛔ KHÔNG đổi** — `Đ2`–`Đ6` ⛔ chưa chạm dòng `L4` nào, vì 17/24 ô *Ai* còn `???`. Bậc đã lên nằm ở `L1`/`L3`/`L5`; toàn sổ **46 dòng** nay có **`K4` = 8** *(§13)*.

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
| 5 | ~~`DIF = 0` **đúng từng đồng**~~ → ⭐ **`\|DIF\| < 1.000 VND`**, dòng `226` | ⭐ **ĐÃ ĐO** *(§11)*: **595/596 = 99,8% đạt**. ⛔ Luật cũ *"đúng từng đồng"* **bất khả** vì bảng có nhân tỷ giá | ⭐ **`K3`** |

⭐ **Hai dòng `K4` là hai chỗ duy nhất trong cả sổ đạt bậc cao nhất** — và ⛔ không phải ngẫu nhiên:
cả hai đều là luật **owner chốt bằng một câu**, rồi **thành một cổng đã thấy đỏ** trong cùng ngày.
Đó là hình dạng mà 44 dòng còn lại cần đi tới.

---

## §5 · `L5` · Bất biến ngầm — danh sách **CHƯA ĐÓNG**

> ⛔⛔ **Loại nguy hiểm nhất, và là loại duy nhất ⛔ không tự lộ ra.** ⛔ Không có bản khai để so —
> phải **đi tìm**. Năm mục dưới là thứ đã **nhìn thấy** khi rà, ⛔ chưa cái nào được giải thích.

| # | Thứ nhìn thấy | Quy mô | Vì sao đáng ngờ |
|:--:|---|--:|---|
| 1 | ~~`P100 Bank ▸ Log`~~ | ~~171.358~~ → ⛔ **4.399 dùng được** | ⭐ **Khuôn khoá ĐÚNG** *(4 mảnh, 100% dòng dùng được có đủ)*. ⛔⛔ Nhưng `302.259` là **ô LƯỚI**, và **51.178** dòng mang khoá **hỏng** `NaNNaNNaN\|\|\|` *(quỹ hỏng **99,6%**)* ⇒ chỉ **4.399** dùng được, phủ **50,2%** sổ bank. Xem §12 |
| 2 | ~~Cột `Check trùng` và `Num`~~ | 2 cột — **giải xong** | ⭐⭐ **`Num` = THỨ TỰ lần xuất hiện của mã, khớp `8.331/8.331` = 100,0%** ⇒ phép chống trùng AS-IS **đã chạy đúng tuyệt đối**, `F04` chỉ phải **giữ**. ⛔ `Check trùng` khớp **92,1%** và **luôn đếm thiếu** ⇒ ⛔ không dùng |
| 3 | ~~Sheet `Bank Transactions_Filter`~~ | **8.338** = **bằng** bản gốc | ⛔ *"To hơn bản gốc"* **SAI** — đếm bằng ô lưới. ⭐⭐ Và nó ⛔ **không phải bộ lọc**: cột `H..L` là khối `DD/MM/YYYY · Diễn giải · PS Nợ · PS Có · Tài Khoản` = **đúng 5 cột sổ kế toán** ⇒ nó là **CÁI CẦU** bank → sổ kế toán |
| 4 | ~~`P100 Cash ▸ [CA]Nhật ký xử lý Giao dịch`~~ | **50** dòng đã xoá | ⭐ **Đúng, và đo được**: **50** dòng xoá được **giữ nguyên cả dòng** + **lý do** + **ngày** *(3 lý do)*, giữ lại **48** mã giao dịch ⇒ đó **chính là hình** của `INV-I03`; `F04` nên **kế thừa** |
| 5 | ~~Chênh **tầng nhập ↔ tầng gộp**~~ | ~~16.625 → 9.331~~ | ⭐⭐ **ĐÓNG bởi `Đ3` — chênh ⛔ KHÔNG TỒN TẠI.** Đo sống: **8.338 → 8.338**, 50/50 tài khoản khớp từng dòng. `7.294` là hệ quả của việc **đếm bằng ô lưới**. Xem §9 |

---

## §9 · ⭐⭐⭐ KẾT QUẢ `Đ3` — chênh **7.294 dòng KHÔNG TỒN TẠI** *(2026-09-07)*

**Công cụ:** `tools/do_chenh_lech.py` · đọc **sống**.

### Trước hết: **đo lại tiền đề**, ⛔ không phân loại ngay

Cả hai con số `16.625 → 9.331` của `Đ1` đều đến từ **bản chụp offline**. Luật
`Đ-1` nói so với bản chụp thì một lệch tìm được *có thể là FLS sai*, cũng *có
thể là sổ đã đổi sau khi chụp* — **hai thứ đó trông y hệt nhau**. Nên `Đ3` đo
lại **cả hai đầu** trên nguồn sống trước.

| | `Đ1` *(bản chụp)* | `Đ3` *(sống)* |
|---|--:|--:|
| Tầng nhập | 16.625 | **8.338** dòng thật *(lưới khai 16.298)* |
| Tầng gộp | 9.331 | **8.338** dòng thật *(lưới khai 8.341)* |
| Chênh | **7.294 (44%)** | ⭐ **0** |

⇒ ⛔⛔ **`Đ1` đếm bằng LƯỚI ở đầu này và bằng thứ khác ở đầu kia.** Ô lưới trống
⛔ không phải dòng. Cả *"44% sổ có thể mất"* là **báo động giả**, và nó đã đứng
trong tài liệu **một ngày** với tư cách rủi ro lớn nhất của bộ AS-IS.

### ⭐⭐ Hai thứ khiến phép đo này làm được điều `Đ1` ⛔ không làm được

| | Là gì | Vì sao quan trọng |
|:--:|---|---|
| ⓵ | **Cột `G = Source`** của `Bank Transactions` ghi **tên đúng sheet `R \|`** mà mỗi dòng đến từ đó | Tầng gộp **tự khai xuất xứ từng dòng** ⇒ chênh tách được **theo từng tài khoản**, ⛔ không cần ghép mờ |
| ⓶ | **Dòng 1** của `Bank Transactions` là một **bộ đếm sống** *(`8331` mã · `8339` xuất xứ)* | Cái sổ **tự đếm chính nó** ⇒ có thể **đối chứng phép đếm của ta với phép đếm của nó** — và hai phép đếm khớp |

### Phân loại chênh *(`Đ-4`: lệch phải PHÂN LOẠI được)*

| Nhóm | Kết quả |
|---|---|
| `B1` **đếm khác đơn vị** *(ô lưới vs dòng thật)* | **7.963 ô** — ⭐ **toàn bộ** cái gọi là chênh nằm ở đây |
| `B2` **nguồn chết** *(có ở nhập, 0 lên gộp)* | ⭐ **0** sheet |
| `B3` **xuất xứ lạ** *(có ở gộp, ⛔ không ứng sheet nào)* | ⭐ **0** |
| `B4` **lệch từng tài khoản** | ⭐ **0** hụt · **0** dư |
| `B5` **khớp đúng từng dòng** | ⭐ **50 / 50** tài khoản · **8.338** dòng |
| `B6` sheet `R \|` **rỗng cả hai đầu** | **10** *(tài khoản đã mở nhưng chưa/không dùng)* |

⭐ Và **phân bố theo NĂM trùng khít cả ba năm** — `2024`=13 · `2025`=4.251 ·
`2026`=4.074 ở **cả hai tầng**. Đó là bằng chứng mạnh hơn hẳn một tổng khớp:
tổng khớp có thể do bù trừ, phân bố khớp thì ⛔ không.

### Đối **TẬP KHOÁ**, ⛔ không chỉ đối số đếm

Cùng số lượng ⛔ chưa phải cùng những dòng ấy. Đối `Reference number`:

| | Tầng nhập | Tầng gộp |
|---|--:|--:|
| Số mã | 8.331 | 8.331 |
| Mã **khác nhau** | 7.905 | ⭐ **7.905** |
| Lệch hai chiều | — | **31 dòng** *(4 tài khoản)* |

### ⛔⛔ Và **một dụng cụ của TÔI lại sai — lần thứ hai trong hai bước**

Bản đầu tôi đọc cột mã bằng `FORMATTED_VALUE` và báo **1.468 dòng bị đổi mã**
trên **18 tài khoản**. ⛔ **Sai.** Sheets hiển thị mã số dài kiểu **SỐ** bằng
**ký hiệu khoa học** *(`1.23E+15`)*, làm **1.468 mã gộp lại thành 294**. Đọc
bằng giá trị **thô** thì số mã khác nhau ở tầng gộp là **7.905 — đúng bằng tầng
nhập**, và lệch còn **31**.

⚠ `Đ2` tôi đo phải **giả định** của mình; `Đ3` tôi đo phải **dụng cụ** của
mình. Cả hai đều là `Đ-3`. ⇒ Ghi thẳng vào `doc_cot()`: **cột MÃ phải đọc thô,
cột NGÀY phải đọc đã định dạng** — ⛔ không có mặc định nào đúng cho cả hai.

### ⛔ Khuyết tật CÒN LẠI — nhỏ, nhưng **nằm đúng trên cái KHOÁ** `INV-I04b` sẽ dựa vào

| # | Thứ đo được | Quy mô | Vì sao đáng kể |
|:--:|---|--:|---|
| 1 | ⛔⛔ Mã lưu **kiểu SỐ** ở tầng gộp | **3.774 / 8.331** *(45%)* | Bản thô thì nguyên vẹn, nhưng **mọi đường đi qua bản HIỂN THỊ** — `.xlsx` xuất ra · chép-dán · `VLOOKUP` với khoá **chữ** — đều thấy `1.23E+15` ⇒ **1.468 dòng đổ vào 294 mã đụng nhau** |
| 2 | Mã bị **trùng** | **280 mã / 706 dòng** | Cột `Check trùng` của chính sheet rất có thể đang đếm đúng thứ này |
| 3 | Dòng **có ngày, ⛔ không mã** | **7** | Khoá đối sánh ⛔ không tồn tại ⇒ `INV-I04b` phải có đường xử riêng |
| 4 | Mã đổi **kiểu** `int`→`float` | **31** | Chính là toàn bộ lệch hai chiều còn lại |
| 5 | Dòng **cụt** ở tầng gộp *(có xuất xứ, ⛔ không ngày ⛔ không mã)* | **1** | Đúng dòng 3, ngay dưới tiêu đề |

⭐⭐ **Một giả thuyết đáng theo, ⛔ chưa phải kết luận:** memory
`itl-mapping-l1-join-logic-and-33pct` ghi phép ghép `Mapping L1` là `VLOOKUP`
trên **Reference number** và chỉ ghép được **33,8%**. Nếu 45% mã phía gộp là
**kiểu số** còn phía `PM_Unpivot` là **chữ**, thì chúng ⛔ **không bao giờ
khớp**. ⇒ Việc phải làm ở `Đ4`: đo kiểu của khoá ở **cả hai phía** phép ghép.

### Bậc sau `Đ3`

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| §5 mục 5 *(chênh tầng nhập ↔ gộp)* | `K0` | ⭐ **`K3`** | Đo được, **phân loại được**, có công cụ chạy lại; ⛔ chưa thành cổng ⇒ chưa `K4` |
| `Bank Transactions` *(P100)* | `K1` | ⭐ **`K2`** | Đối được **tập khoá** hai chiều, ⛔ không chỉ hình dạng |
| Archetype 67 `R \|` | `K2` | `K2` | ⛔ chưa đổi — vẫn chưa có cổng |

⇒ ⭐ **Đóng §5 mục 5.** ⛔ **Mở `GAP-ORA-10`:** khoá `Reference number` ở tầng
gộp **45% lưu kiểu SỐ** ⇒ mọi phép ghép qua bản hiển thị đều hỏng im lặng.
`F04` phải **ép về chuỗi** khi nạp, và điều đó cần **một cổng**, ⛔ không phải
một dòng ghi chú.

---

## §10 · ⭐⭐ KẾT QUẢ `Đ4-a` — giả thuyết của chính tôi **CHẾT**, và `33,8%` là **gần KỊCH TRẦN** *(2026-09-07)*

**Công cụ:** `tools/do_khoa_ghep.py` · đọc **sống**.

`Đ3` sinh ra một giả thuyết: *45% mã lưu kiểu SỐ ⇒ `VLOOKUP` của `Mapping L1`
âm thầm trượt ⇒ đó là lý do tỷ lệ ghép chỉ **33,8%***. Công cụ này dựng ra để
**thử nó**, ⛔ không phải để xác nhận nó.

### Đường ghép thật *(đo được, ⛔ không suy)*

`Transaction Mapping L1` cột **1** `Số chứng từ` ──`VLOOKUP`──▸
`[Importrange]PM_Unpivot` cột **25** `Reference number` *(= cột `Z`)*

### Ba phép đếm — và phải phân biệt cho rõ

| Phép đếm | Nghĩa | Kết quả |
|---|---|--:|
| `M_chuỗi` | cùng mã **nếu ép cả hai về chuỗi** ⇒ **đạt được** | **3.412** *(33,5%)* |
| `M_kiểu` | cùng mã **và cùng kiểu ô** ⇒ **Sheets thấy** | **3.412** *(33,5%)* |
| `M_thật` | dòng thật sự có `ID PMLine` ⇒ **đang có** | **3.405** *(33,4%)* |

⇒ ⭐⭐ **`M_chuỗi − M_kiểu = 0`.** ⛔ **Không một dòng nào** mất vì kiểu ô.
**Giả thuyết chết** — và cái chết ấy là một kết quả, ⛔ không phải một thất bại.

Kiểm thêm hai chiều nữa để chắc là ⛔ không phải phép đo của tôi cứu nó:
kiểu ô hai đầu *(bank `chữ` 5.416 / `số` 4.778 · PM `chữ` 2.885 / `số` 352)*
**có lệch thật**, nhưng ⛔ **không lệch ở những mã cả hai đầu cùng có**. Và
chuẩn hoá bỏ khoảng trắng + viết HOA chỉ đưa `3.412 → 3.416`, tức **+4 dòng**.

### ⭐⭐⭐ Điều thật sự lật: `33,8%` ⛔ **không phải một phép ghép hỏng**

| | Số |
|---|--:|
| Mã phía **bank** *(`Mapping L1`)* | **10.194** |
| Mã phía **PM** *(`PM_Unpivot`)* | **3.237** |

⇒ **Trần của phép ghép này là ~3.237.** Ghép được **3.412** *(bank có mã trùng
nhau nên vượt nhẹ số mã PM)* nghĩa là nó **gần kịch trần**. **6.782 dòng**
*(66,5%)* ⛔ không ghép được vì `PM_Unpivot` **⛔ không hề có** mã ấy — đó là
**giao dịch ngân hàng thật chưa có đề nghị thanh toán tương ứng**. Đó là
**nghiệp vụ**, ⛔ không phải lỗi kỹ thuật.

⚠ ⇒ **Sửa lại cách hiểu đã ghi:** `33,8%` từng được ghi như một **triệu chứng
hỏng**. Nó ⛔ không phải. Con số phải theo dõi ⛔ không phải *"tỷ lệ ghép"* mà
là ***"mã bank có, PM không"*** — và câu hỏi đúng để hỏi kế toán là *"6.782
giao dịch ấy đáng lẽ phải có đề nghị thanh toán ⛔ hay không"*.

### ⛔ Khuyết tật thật tìm được ở đây

⛔⛔ **`Mapping L1` cột 13 chứa `7.372` ô `#N/A`** *(68,4% của 10.778 ô)*.
`#N/A` là một **giá trị hiển thị**, ⛔ không phải ô trống ⇒ **nhìn bằng mắt thì
cột ấy trông ĐÃ ĐẦY**. Bất cứ thứ gì đọc xuôi cột này — bản xuất `.xlsx`,
`IMPORTRANGE`, một phép gộp — đều nhận `#N/A` **như dữ liệu**.

### ⛔ Và **dụng cụ của tôi sai lần thứ BA trong một phiên**

Bản đầu tôi đếm `M_thật` bằng *"ô ⛔ không rỗng"* và ra **10.777 / 10.194 =
`105,7%`**. Một tỷ lệ ghép **⛔ không thể có** — và đó là **dấu hiệu duy nhất**
cho thấy phép đếm sai. Nếu con số ấy rơi vào khoảng 60–70% thì tôi đã ⛔ không
nghi gì và **ghi thẳng vào tài liệu**.

⚠ ⇒ Luật rút ra, đã ghi vào `Đ-3`: **mỗi tỷ lệ phải có một khoảng hợp lệ khai
trước**, và phép đo phải **tự đỏ** khi rơi ra ngoài. `Đ2` tôi đo phải **giả
định**; `Đ3` đo phải **cách hiển thị**; `Đ4-a` đo phải **`#N/A`**. Ba lần, cùng
một họ: **đo phải dụng cụ, ⛔ không phải cái sổ.**

### Bậc sau `Đ4-a`

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| Phép ghép `Mapping L1` | `K0` | ⭐ **`K3`** | Đường ghép **đo được**, ba phép đếm **phân biệt được**, công cụ chạy lại được |
| `GAP-ORA-10` *(mã kiểu SỐ)* | mở | ⚠ **hẹp lại** | ⛔ **KHÔNG** phá phép ghép này *(chứng minh: `M_chuỗi = M_kiểu`)*. Vẫn là hiểm hoạ thật trên **đường HIỂN THỊ** *(`.xlsx` · chép-dán · khoá chữ)* — nhưng ⛔ không được nói nó đang phá `Mapping L1` |

---

## §11 · ⭐⭐⭐ KẾT QUẢ `Đ5-a` — **TRỌNG TÀI SỐ DƯ**, đo được lần đầu *(2026-09-07)*

**Công cụ:** `tools/do_trong_tai.py` · owner chia quyền `A-CCR_V2_Working` sáng nay.

Dòng `226` của `2. CCR` là **thước đo duy nhất** của cả lằn nhập: cuối ngày, số
dư **Treasury** *(ngân hàng báo)* phải bằng số dư **Accounting** *(sổ kế toán
cộng ra)*. Bộ tài liệu ghi luật ấy và xếp bậc `K0` — ⛔ **chưa ai đo lần nào**.

### Hình dạng thật *(đọc được từ công thức, ⛔ không suy)*

`2. CCR` **229 dòng × 655 cột**, ⭐ **mỗi cột = MỘT NGÀY** *(từ `31-Dec-24`)*.

| Dòng | Là gì |
|:--:|---|
| `5` | **ngày** · `6..9` tỷ giá USD/SGD/HKD |
| `30` | `EBTS` Ending Cash Balance **TREASURY** — chi tiết ở `32..123` |
| `125` | `EBA` Ending Cash Balance **ACCOUNTING** — tổng ở `127` |
| **`226`** | `DIF` = **`Σ(32..123 quy VND) − 127`** |

### ⛔⛔ BA cái bẫy — và tôi mắc **cả ba**, mỗi cái ra một con số sai to

| # | Đếm ngây thơ | Sự thật |
|:--:|---|---|
| ⓵ | *"**412/644** ô khác 0"* — nghe như thảm hoạ | Phần lớn là **bụi dấu phẩy động** *(`1.52587890625e-05` = 2⁻¹⁶)* sinh từ chính phép **nhân tỷ giá**. ⛔ Không phải tiền |
| ⓶ | *"**49 ngày** vượt dung sai"* | Một lệch kéo dài qua nhiều ngày là **MỘT sự kiện**, ⛔ không phải N. Gom lại còn **2** |
| ⓷ | ⛔⛔ *"lệch **9,53 tỷ** kéo dài 48 ngày"* | **Tệp này là BẢN CHỤP.** Đó là **đuôi đông cứng**, ⛔ không phải tiền mất |

### ⭐⭐⭐ Bẫy ⓷ là bẫy đáng sợ nhất, và nó có tên

`Bank Transactions` và `Cash Ledger Transactions` **trong chính tệp A-CCR** đều
dừng ở **19/08/2026**, trong khi `P100` sống chạy tới **06/09/2026**.

⛔ Nhưng cột ngày của `2. CCR` **dựng sẵn tới `6-Oct-2026`**, và ô nào cũng có
số — vì công thức **chuyển tiếp** giá trị hôm trước *(`WJ32 = WI32`)*.

⇒ ⛔⛔ **Mở tệp ra hôm nay sẽ thấy cột của NGÀY HÔM NAY đầy số — và những số ấy
19 NGÀY TUỔI.** Không có một dấu hiệu nào trên màn hình nói điều đó.

⚠ Cùng một họ với `#N/A` trông như *"đã đầy"* ở `Đ4-a`: **dữ liệu cũ trình bày
y hệt dữ liệu hiện tại**. ⇒ Luật cho FLS: **mọi cửa đọc phải trả TUỔI của số,
⛔ không chỉ trả số.**

### Kết quả sau khi **cắt đuôi đông cứng**

| | Ngày | % |
|---|--:|--:|
| `= 0` đúng từng đồng | 232 | 38,9% |
| bụi dấu phẩy động *(< 1 VND)* | 363 | 60,9% |
| trong dung sai *(< 1.000 VND)* | **0** | 0,0% |
| ⛔ **vượt dung sai** | **1** | 0,2% |
| ⭐ **ĐẠT luật** | **595 / 596** | ⭐ **99,8%** |

### Hai điều phải ghi

⛔ **① Luật như đã ghi là SAI.** *"`DIF = 0` đúng từng đồng"* ⛔ không đúng:
**363/596 ngày** mang bụi khác 0. Đòi *"đúng từng đồng"* trên một bảng có
**nhân tỷ giá** là **bất khả** — đó là tính chất của số dấu phẩy động, ⛔ không
phải lỗi kế toán. ⇒ Luật đúng: **`|DIF| < 1.000 VND`** *(`QĐ-ITL-57`, dùng
chung một thước với cả bộ)*.

⭐ **② Và theo thước ĐÚNG thì trọng tài GIỮ.** `595/596`, và ⛔ **không một
ngày nào** rơi vào khoảng giữa `1` và `1.000 VND` ⇒ phân bố **sạch**: hoặc là
**bụi**, hoặc là **tỷ**. Ngày duy nhất vượt — `19/08/2026`, `+302.187.656` —
**chính là ngày cuối của tệp**, nhiều khả năng **chưa chốt xong**.

⇒ ⭐⭐ **Đây là kết quả TỐT, và là kết quả TỐT ĐẦU TIÊN của cả `Đ`:** phép đối
soát số dư của kế toán **thật sự chạy**, suốt **596 ngày**.

### Bậc sau `Đ5-a`

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| `L3` mục 5 *(`DIF = 0` dòng `226`)* | `K0` | ⭐ **`K3`** | Đo được, **phân loại được**, công cụ chạy lại được; luật đã **sửa cho đo được**. ⛔ Chưa `K4` vì ⛔ chưa thành cổng |
| `GAP-ORA-09` | mở | ⛔ **vẫn mở** | Tệp được chia là **bản chụp 19 ngày tuổi** ⇒ ⛔ **chưa** đo được trọng tài **sống** |

---

## §12 · ⭐⭐ KẾT QUẢ `Đ5-b` — **4 mục `L5` cuối**, và đối chiếu **ERD** *(2026-09-07)*

**Công cụ:** `tools/do_bat_bien_ngam.py` · đọc **sống**.

### ⭐⭐⭐ Kết quả lớn nhất: **nhật ký thay đổi đã tồn tại — nhưng phần lớn là RÁC**

| | Ghi trong `DD-I05` | Đo sống |
|---|--:|--:|
| `P100 Bank ▸ Log` | 171.358 | **10.994** dòng có dữ liệu |
| `P100 Cash ▸ Log` | 130.901 | **44.583** |
| **Tổng** | **302.259** | **55.577** |
| ⛔ khoá **HỎNG** `NaNNaNNaN\|\|\|` | — | ⛔⛔ **51.178** |
| ⭐ **dùng được** | — | ⛔ **4.399** *(bank 4.200 · quỹ **199**)* |

⛔ **Hai lỗi chồng nhau.** ⓵ `302.259` là **ô LƯỚI** — cùng cái bẫy `Đ3` đã dập.
⓶ Và **92% phần còn lại là rác**: kịch bản dựng khoá làm phép **ngày** trên thứ
⛔ không phải ngày ⇒ `NaN`, ba trường sau **rỗng**. Sổ quỹ hỏng **99,6%**, chỉ
còn **69 khoá khác nhau** trên 44.583 dòng.

⭐ **Nhưng khuôn khoá thì ĐÚNG** — `<YYYYMMDD>\|<Nợ>\|<Có>\|<Ref>`, **100%**
dòng dùng được có đủ 4 mảnh. ⇒ Cái sai là **quy mô bằng chứng**, ⛔ không phải
thiết kế. Đo phủ: log chạm **4.183 / 8.338 = 50,2%** sổ bank.

⇒ ⛔ Điều kiện nghiệm thu của `INV-I04b` — *"đối sánh được với 302.259 dòng log
cũ"* — **⛔ không còn là một phép kiểm mạnh**. `GAP-ITL-14` đánh dấu ⚠.

### ⭐⭐ `Num` — phép chống trùng của AS-IS **đã chạy đúng tuyệt đối**

Hai cột `Num` / `Check trùng` ⛔ chưa ai nói là gì. Thử **hai giả thuyết**:

| Giả thuyết | Khớp |
|---|--:|
| `Check trùng` = **số lần** mã xuất hiện | ⛔ **92,1%** — và **luôn đếm THIẾU** *(mẫu nhiều nhất: ghi `1`, thực `2`)* |
| ⭐⭐ `Num` = **thứ tự lần xuất hiện** của mã | ⭐ **8.331 / 8.331 = 100,0%** |

⇒ `F04` ⛔ **không phải phát minh lại** phép chống trùng — chỉ phải **giữ** cái
đang chạy. ⛔ Và ⛔ không được dùng `Check trùng`.

### ⭐ `Bank Transactions_Filter` ⛔ **không phải bộ lọc** — nó là **CÁI CẦU**

Cột `A..G` y hệt `Bank Transactions`; cột `H..L` là **khối thứ hai**:
`DD/MM/YYYY · Diễn giải · PS Nợ (Nguyên tệ) · PS Có (Nguyên tệ) · Tài Khoản`
— **đúng 5 cột của sổ kế toán** `1.1/1.2 Ledger 111/112`.

Số dòng: **8.338** — ⭐ **đúng bằng** bản gốc. ⇒ `§5` ghi *"nhiều hơn 98 dòng"*
là **sai**, do đếm ô lưới. **Gọi sai tên thì ⛔ không bao giờ hỏi đúng câu hỏi.**

### ⭐ Kho xoá-có-vết **đã có sẵn**

`[CA]Nhật ký xử lý Giao dịch`: **50 dòng** bị xoá được **giữ nguyên cả dòng**,
kèm **lý do** + **ngày** *(`Đã xóa ngày 13/10//2025` ×23 · `Giao dịch trùng với
GD đã xoá` ×23 · `-` ×4)*, và **48 mã giao dịch** giữ lại. ⇒ Kế toán **đã có**
thói quen ấy; đó **chính là hình** của `INV-I03`.

### Đối chiếu **ERD** — ghi ở `05_DATA_DICTIONARY_ERD` §`DD-I09` *(v0.19)*

| | Chênh |
|:--:|---|
| ⛔⛔ | `302.259` → **4.399** ⇒ `INV-I04b` hẹp lại, `GAP-ITL-14` ⚠ |
| ⛔ | 3 số `DD-I05` hẹp lại: `281`→**280 mã/706 dòng** · `103`→⭐**7** · **`31` dòng "mã rác" ⛔ KHÔNG phải rác** |
| ⛔ | **3 mắt xích ERD chưa hề nhắc**: **bản khai dòng 1** của 68 sheet `R \|` · **`Bank Transactions_Filter` = cái cầu** · **kho xoá-có-vết** |
| ⛔ | `2. CCR` tả đúng ma trận nhưng **bỏ mất dòng `226` `DIF`** — trọng tài |
| ⚠ | `Bank Transactions` `7.715`→**8.338**, dữ liệu từ dòng **3** ⛔ không phải 4; sheet trùng tên ở `A-CCR` `7.484`→**7.961** và **dừng 19/08** |
| ✅ | ERD **đúng**: khuôn ma trận `2. CCR` · khuôn khoá 4 mảnh · `GAP-DOC-07` · luật *map theo TÊN* |

### Bậc sau `Đ5-b`

| Chỗ | Trước | Sau |
|---|:--:|:--:|
| `L5` mục 1 *(`Log`)* | `K0` | ⭐ **`K3`** |
| `L5` mục 2 *(`Num`/`Check trùng`)* | `K0` | ⭐ **`K3`** |
| `L5` mục 3 *(`_Filter`)* | `K0` | ⭐ **`K3`** |
| `L5` mục 4 *(kho xoá)* | `K0` | ⭐ **`K2`** *(đo được, ⛔ chưa hỏi kế toán quy trình)* |

⇒ ⭐⭐ **`§5` ĐÓNG cả 5 mục.** ⛔ Nhưng ⛔ **không mục nào lên `K4`** — vẫn vì
`Đ6` chưa làm: chúng **chạy bằng tay**.

---

## §13 · ⭐⭐⭐ `Đ6` — **CƯỠNG CHẾ**: 5 phép đo thành **cổng chung #17** *(2026-09-07)*

**Chạy:** `PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/kiem_nguon_song.py`
*(~25 giây, đọc **sống**)*

Năm phép đo `Đ2`–`Đ5-b` đã lật ba báo động giả và tìm ra bốn thứ AS-IS làm
đúng. Nhưng cả năm **chạy bằng tay** ⇒ ⛔ **không dòng nào lên được `K4`**, vì
`K4` đòi *"có cổng chạy tự động, **và cổng ấy đã thấy đỏ**"*.
**Một phép đo ⛔ không tự đỏ thì nó chưa canh gì cả.**

### Kiến trúc — ⛔ và vì sao ⛔ KHÔNG nhét vào `pytest`

| Ở đâu | Là gì |
|---|---|
| `fls/kiem/nguon_song.py` | **7 luật THUẦN** — vào là dữ liệu, ra là verdict. ⛔ Không chạm mạng |
| `tests/kiem/test_nguon_song.py` | **25 bài, chạy offline** — mỗi luật có ca **XANH**, ca **ĐỎ thật**, và ca **RỖNG** |
| `tools/kiem_nguon_song.py` | **cổng #17** — chỉ là cái vỏ I/O, đọc sống rồi gọi 7 luật |

⇒ Một cổng đọc mạng thì ⛔ **không tự chứng minh được là nó đỏ được** — muốn
thấy nó đỏ thì phải **làm hỏng sổ thật**. Tách ra thì chứng minh được **offline**.

### Bảy luật — mỗi luật là một câu khẳng định về **cái SỔ**, ⛔ không phải về FLS

| | Luật | Sinh từ | Đo được |
|:--:|---|:--:|--:|
| `L1` | mọi sheet `R \|` khai **đủ 6 trường** ở dòng 1 | `Đ2` | **60** sheet |
| `L2` | tầng **NHẬP = GỘP**, theo **từng tài khoản** | `Đ3` | **50** tài khoản |
| `L3` | mọi dòng gộp có xuất xứ ứng một sheet `R \|` | `Đ3` | **8.338** dòng |
| `L4` | ⛔ **không** dòng nào mất vì **KIỂU Ô** | `Đ4-a` | **10.194** khoá |
| `L5` | `\|DIF\| < 1.000 VND` mọi ngày có dữ liệu | `Đ5-a` | **595** ngày |
| `L6` | `Num` = **thứ tự** lần xuất hiện của mã | `Đ5-b` | **8.331** dòng |
| `L7` | cái cầu `_Filter` **bằng đúng** bản gốc | `Đ5-b` | **8.338** dòng |

⇒ ⭐ **7/7 ĐẠT**, và mỗi luật **in ra nó đã đo bao nhiêu thứ**.

### ⛔⛔ Luật chung: **đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT** — và nó **cứu ngay lần chạy đầu**

Nhà này đã có tiền lệ: hai cổng `RUN_ATOMIC` **xanh suốt hai tháng** trên **28
vi phạm**, vì chúng lọc `IS NOT NULL` trên **chính cột chúng canh** ⇒ **chưa
từng có khả năng đỏ**. Nên mỗi luật ở đây trả về cả `da_do`, và `da_do == 0`
là **ĐỎ**.

⭐⭐ **Và lần chạy đầu tiên của cổng, `L6` ĐỎ đúng vì lẽ đó.** Nguyên nhân là
lỗi trong **chính cái cổng**: `doc_cot()` **ép mọi ô về chuỗi**, nên `Num` hết
là số và luật đếm được **0 dòng**. ⛔ Không có luật *"đo 0 ⇒ đỏ"* thì nó đã
**XANH GIẢ** — báo đạt trên một phép đo **chưa từng chạy**.

### Bậc sau `Đ6`

| Chỗ | Trước | Sau | Cổng canh |
|---|:--:|:--:|---|
| Archetype 67 sheet `R \|` | `K2` | ⭐ **`K4`** | `L1` |
| `Bank Transactions` *(P100)* | `K2` | ⭐ **`K4`** | `L2` + `L3` |
| `L5` mục 5 — chênh nhập ↔ gộp | `K3` | ⭐ **`K4`** | `L2` + `L3` |
| Phép ghép `Mapping L1` | `K3` | ⭐ **`K4`** | `L4` |
| `L5` mục 2 — `Num` | `K3` | ⭐ **`K4`** | `L6` |
| `L5` mục 3 — cái cầu `_Filter` | `K3` | ⭐ **`K4`** | `L7` |
| `L3` mục 5 — **trọng tài số dư** | `K3` | ⛔ **`K3`** *(giữ nguyên)* | `L5` |

⛔⛔ **Vì sao trọng tài ⛔ KHÔNG được lên `K4` dù có cổng canh.** Cổng đang đọc
**bản chụp A-CCR 19 ngày tuổi**. Một cổng canh một tệp **đông cứng** thì nó
**⛔ không bao giờ đỏ được vì sổ trôi** — nó chỉ đỏ nếu ai sửa bản chụp. ⚠
**Cổng trên nguồn chết là cổng ⛔ không bắn được.** ⇒ Giữ `K3` cho tới khi
`GAP-ORA-09` đóng *(cần link `A-CCR` **đang chạy**)*.

⇒ ⭐⭐ **`K4` đi từ `2/46` lên `8/46`.** Sáu dòng lên bậc cao nhất trong một đợt
— nhiều hơn cả bốn tháng trước cộng lại.

---

## §14 · ⭐⭐⭐ OWNER CHỐT 2 VIỆC — và quyết định thứ hai hoá ra **tốt hơn** *(2026-09-07)*

| | Owner chốt | Đóng gì |
|:--:|---|---|
| ⓵ | **Thay CÚ ĐẨY** *(⛔ không thay `P100`)* | ⭐ **`GAP-SCOPE-02` ĐÓNG** |
| ⓶ | **⛔ Không cần `A-CCR` sống — tận dụng dữ liệu hiện có** | ⭐ **`GAP-ORA-09` ĐÓNG** *(⛔ không theo đuổi)* |

### ⓵ Thay cú đẩy — hạ nguồn ⛔ **không đổi một dòng nào**

`QĐ-ITL-99` đo được: `1.1`/`1.2 Ledger` đọc **sheet cùng workbook `A-CCR`**, và
`A-CCR ▸ Bank Transactions` là **giá trị đã dán**. ⇒ FLS chỉ cần **thay khâu
đẩy** `P100` → `A-CCR`. `A-CCR` vẫn nhận `Bank Transactions` như cũ — chỉ khác
là **từ FLS**, và **⛔ không trễ 19 ngày**. ⛔ Không ai phải sửa công thức nào.

### ⓶ ⭐⭐ Quyết định *"tận dụng dữ liệu hiện có"* ⛔ **không phải nhượng bộ**

Trọng tài số dư **đã có sẵn và đang SỐNG** trong `P100`, đo được từ công thức:

| Cột `BankAccountList` | Công thức | Là gì |
|:--:|---|---|
| `9`/`10` | `SUMIFS(INDIRECT($D3&G3), INDIRECT($D3&$F3),"<>")` | tổng Nợ/Có đọc **thẳng từ sheet `R \|`** ⇒ phía **SAO KÊ** |
| `12`/`13` | `SUMIFS('Bank Transactions'!D:D, …$G:$G, $D3)` | tổng Nợ/Có ở **tầng gộp** ⇒ phía **SỔ** |
| `14`/`15` | `=J3=M3` · `=K3=N3` | ⭐ **cờ đúng/sai cho TỪNG tài khoản** |

⇒ ⭐⭐⭐ **Mạnh hơn hẳn dòng `226` của `2. CCR`:** bên kia là **MỘT con số tổng**
toàn công ty trên một **bản chụp chết**; bên này là **N lá cờ**, trên dữ liệu
**sống**, và so **đúng cặp** `R \|` *(sao kê)* ↔ `Bank Transactions` *(sổ)* mà
`Đ3` đã đo. ⇒ `L5` **đổi nguồn** về `P100`; thêm `L8` *(cờ của chính kế toán)*
và `L9` *(danh mục ↔ sheet)*. Cổng #17 **7 → 12 phép so**.

### ⛔⛔ Và cổng ĐỎ NGAY — **4 phát hiện thật, trên dữ liệu hôm nay**

| Luật | Phát hiện |
|---|---|
| ⛔ `L5-CSH` | **4/28** vượt dung sai — nặng nhất `R \| PO BGO1` **Nợ −42.164.521 VND** |
| ⛔ `L8-CSH` | **2/14** quỹ `Active` ⛔ không khớp: **`R \| PO BGO1`** · **`R \| Pingpong`** |
| ⛔ `L9-BNK` | **2/52** tài khoản `Active` ⛔ **không có sheet**: `R \| PO7_Payoneer USD_CGO1` · `R \| 1132000050920_MauBank USD_MGO1` |
| ⛔ `L9-CSH` | **6/19** — gồm **5 dòng đánh `Active` mà ⛔ KHÔNG có tên tài khoản** *(dòng 8–12)* + `R \| PO BGO1` |

⭐ **Một chuỗi nhân quả khép kín:** danh mục dòng `14` trỏ tới sheet
`R \| PO BGO1` **⛔ không tồn tại** ⇒ `INDIRECT` hỏng ⇒ phía **sao kê đọc được
0** ⇒ lệch đúng **42,16 triệu** so với phía sổ ⇒ cờ `False`. **Ba luật cùng
chỉ vào một nguyên nhân.**

⛔ **⛔ Không nới cổng cho xanh** *(`R-A5`)*. Bốn cái đỏ này là **việc của kế
toán**, ⛔ không phải lỗi của FLS.

### ⛔ Và **một lỗi nữa của tôi** — bắt được vì hai phép đếm ⛔ không khớp

Bản đầu tôi khoá dict bằng **TÊN tài khoản**. Tên thì **có trùng và có rỗng**
⇒ dict **âm thầm nuốt dòng**: `L8-CSH` báo **9** tài khoản `Active` trong khi
đo thẳng ra **19**. ⚠ **Một phép đếm trên dict khoá bằng dữ liệu người gõ là
một phép đếm ⛔ không đáng tin.** ⇒ Khoá nay mang **số dòng**.

### Bậc sau §14

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| `L3` mục 5 — **trọng tài số dư** | `K3` | ⭐ **`K4`** | Nguồn nay **SỐNG** *(`P100`)*, cổng canh nó, và **đã ĐỎ THẬT** — đúng định nghĩa `K4` |

⇒ ⭐ **`K4` = 9/46.**

---

## §15 · ⭐⭐⭐ `F04` CHẶNG 2 — **SOÁT**, và nó lật **BA** kết luận *(2026-09-07)*

Chặng 1 trả lời *"FLS dựng ra có **ĐÚNG** không?"* — **8.338/8.338**. Chặng 2 hỏi một câu **khác hẳn**:

> ⭐ *"FLS bắt được cái gì mà chặng **`Run`** của trang tính ⛔ **KHÔNG** bắt?"*

⛔⛔ **Và tôi ⛔ không được đoán danh sách ấy rồi viết luật.** Bài học `Đ2` *(phép kiểm đầu tiên ở đó **mã hoá giả định của tôi** và báo oan 8 sheet)* ⇒ dựng `tools/do_soat_nap.py` **đo trước** trên một lần nạp thật, rồi mới viết luật cho những gì **có mặt**.

### ⭐⭐⭐ Lật ⓵ — **thủ phạm làm hỏng 31 mã là chính chặng `Run`**

`Đ4-a` đếm **31** mã bị hạ xuống kiểu `float` ở `Bank Transactions` *(`4366185033872500.0`)*. Đo lại ở **nguồn** `R |`:

| Đo ở đâu | Mã hỏng |
|---|:--:|
| `Bank Transactions` *(sau `Run`)* | **31** |
| 60 sheet `R \|` *(nguồn)* | ⭐ **0 / 8.338** |

⇒ ⛔ **Nguồn SẠCH. Phép nạp của trang tính mới là nơi mã bị hỏng.** Trước đây tôi chỉ dám viết *"bản FLS trung thực hơn"*; nay nó là **một câu có nguyên nhân**, ⛔ không còn là một quan sát.

### ⭐⭐ Lật ⓶ — `GAP-KT-03` bị **chẩn đoán SAI**, và cổng #17 ⛔ không thể tự thấy

Cổng #17 `L9` nhìn **một chiều** *(danh mục → sheet)* và kết luận **2 tài khoản `Active` ⛔ không có sheet**. Cổng soát nhìn **chiều ngược lại** *(sheet → danh mục)* và thấy **2 sheet đang nạp mà ⛔ không có trong danh mục**. Ghép hai đầu:

| Danh mục khai | Sheet thật | Chênh |
|---|---|---|
| `R \| 1132000050920_MauBank USD_MGO1` | `R \| 132000050920_MauBank USD_MGO1` | danh mục **thừa `1`** *(giống 98,5%)* |
| `R \| PO7_Payoneer USD_CGO1` | `R \| PO_Payoneer USD_CGO1` | danh mục **thừa `7`** *(giống 98,0%)* |

⇒ ⛔⛔ **⛔ KHÔNG thiếu sheet nào. Đây là HAI LỖI GÕ MỘT KÝ TỰ trong danh mục.** Cả hai sheet **tồn tại và có dữ liệu**. Hệ quả thật: hai cột đối soát của hai tài khoản ấy trỏ vào **vùng rỗng** ⇒ ⛔ **chưa từng đối soát**, và ⛔ **không ai biết**.

> ⭐ **Bài học phương pháp:** một cổng nhìn **một chiều** chẩn được **triệu chứng** *("thiếu sheet")*, ⛔ **không** chẩn được **bệnh** *("gõ nhầm")*. Hai đầu soi vào nhau mới đọc ra.

### ⛔ Lật ⓷ — **cổng soát tự lộ điểm mù của chính nó, ngay lần chạy đầu**

`S8` bản đầu suy tập nguồn từ **các dòng đã nạp**. Nó báo **1** sheet lạ, trong khi phép đo riêng chỉ ra **2**. Chênh ở đâu? Sheet thứ hai ra **0 dòng** ⇒ ⛔ **không dòng nào mang tên nó** ⇒ nó **biến mất khỏi chính phép kiểm sinh ra để tìm nó**.

⭐ **Cùng một lớp lỗi với vụ *"khoá dict bằng TÊN tài khoản"* ở cổng #17**: **suy một tập từ DỮ LIỆU thay vì lấy từ ĐẦU VÀO ĐÃ KHAI** thì cái vắng mặt sẽ **vắng mặt lần thứ hai, trong im lặng**. ⇒ `S8` nay nhận **tập 60 sheet đã nạp**.

### Tám luật — và **BA HẠNG**, ⛔ không phải nới cổng

⛔⛔ **Phân hạng trả lời một câu KHÁC hẳn *"đạt hay không"*: khuyết tật này là CỦA AI?**

| Hạng | Nghĩa | Xử |
|---|---|---|
| **`CHẶN`** | **lỗi của FLS** | ⛔ ĐỎ **và chặn** lô |
| **`CỜ`** | **khuyết tật có sẵn trong sổ kế toán** | ⛔ ĐỎ, **báo to**, ⛔ **không chặn** — những dòng ấy là **TIỀN THẬT**; vứt đi là vi phạm *"⛔ 0 dòng rơi im lặng"* ⇒ chúng thuộc **hàng chờ có lý do** |
| **`CANH`** | hiện **sạch** | giữ để bắt trôi |

| Luật | Hạng | Kết quả sống |
|---|:--:|---|
| `S1` ba đường cân — ⛔ 0 dòng rơi im lặng | `CHẶN` | ⭐ **ĐẠT** — 60 sheet · 8.341 dòng vào, cân hết |
| `S8` xuất xứ phải có trong danh mục | `CỜ` | ⛔ **2/60** — chính là **hai lỗi gõ** ở lật ⓶ |
| `S2` có tiền thì phải có **MÃ** | `CỜ` | ⛔ **7/8.338** — ⛔ không ghép PM được |
| `S3` mỗi dòng phải có **TIỀN** | `CỜ` | ⛔ **2/8.338** |
| `S4` mỗi dòng phải có **TIỀN TỆ** | `CỜ` | ⛔ **12/8.338** — số trần ⛔ không quy đổi được |
| `S7` dòng **trùng HOÀN TOÀN** *(⛔ không tính `Num`)* | `CỜ` | ⛔ **26 khoá · 92 dòng** — cần **NGƯỜI** xem, ⛔ không tự kết luận |
| `S5` mã ⛔ không bị hạ kiểu `float` | `CANH` | ⭐ **ĐẠT** — 0/8.338 *(lật ⓵)* |
| `S6` một sheet chỉ **một** kiểu ngày | `CANH` | ⭐ **ĐẠT** — 50/50 |

⭐ **`S7` mang một bài kiểm soát THIẾT KẾ:** khoá trùng **⛔ CỐ Ý không chứa `Num`**, vì `Num` do **chính FLS** sinh — đưa nó vào khoá thì mọi dòng đều khác nhau và phép kiểm **⛔ không bao giờ đỏ được nữa**. `test_S7_DO_du_Num_KHAC_nhau` giữ đúng chỗ ấy.

### ⛔ Và **hai lỗi nữa của tôi**, cả hai đều do máy bắt

| | Lỗi | Bắt bởi |
|:--:|---|---|
| ⓵ | Xếp `S8` vào hạng **`CHẶN`** — trong khi định nghĩa `CHẶN` do **chính tôi** viết là *"lỗi của FLS"*, mà thứ `S8` bắt được lại là **lỗi gõ của kế toán** ⇒ **tự mâu thuẫn** | lần chạy thật đầu tiên |
| ⓶ | Tạo **BA bản sao** của bản khai ánh xạ *(`soat_nap.py` · `nap_sao_ke.py` · `do_soat_nap.py`)* | ⭐⭐ `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` — **một bài tôi viết ở chặng 1 để bắt chính mình ở chặng 2**. ⇒ Khai thêm `TRUONG_DOC_DUOC` + 8 chỉ số cột ở **một chỗ** *(`sao_ke.py`)* |

⚠ **Một sửa hạ tầng cùng đợt:** `nap()` gọi API **60 lượt** cho đúng việc mà `doc_cot` **đã biết gộp 60 vùng một lượt** ⇒ **cạn hạn mức thật** *(`429` nổ sau cả 4 lần lui-và-thử-lại)*. Nay gộp: ~300 vùng ⇒ **~5 lượt**, giảm **12 lần**. ⛔ Hạn mức đọc là **tài nguyên dùng CHUNG với owner** đang mở chính file đó.

### Bậc sau §15

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| `L1` mục 3 — **hình dạng tầng nhập** | `K3` | ⭐ **`K4`** | `S6` canh nó **tự động**, và luật ⛔ không bao giờ xanh trên tập rỗng |
| `L2` mục 2 — **phép chống trùng** | `K3` | ⭐ **`K4`** | `S7` **đã ĐỎ THẬT** *(26 khoá)*, ⛔ không phải một cổng chưa từng đỏ |

⇒ ⭐ **`K4` = 11/46.**

---

## §16 · ⭐⭐⭐ ĐỐI CHIẾU **ERD MODULE MAPPING** ↔ GSheet/Excel *(2026-09-18, `CR#12`)*

**Nguồn đo:** `PE-PI-PM_Unpivot_20260910.xlsx` *(tab `PM_Unpivot`)* · `[Master] ITL_Ledge_raw_20260910.xlsx` *(tab `ITL Ledge`, dòng 2 khai `Sheet = Transaction Mapping L1`)* · và **ảnh chụp LIVE** của chính FLS *(`NAP-2026-09-18-PMA3C8ACDB`)*.

⚠ **Ranh giới tin cậy của bản xuất `.xlsx`** *(`gsheet-offline-export-artifacts`)*: dùng cho **CẤU TRÚC** *(tên tab · tên cột · vùng)* và cho **trạng thái `#N/A` tại thời điểm xuất`10/09`*. ⛔ **Không** dùng cho giá trị ngày tháng *(`itl-xlsx-export-destroys-dates`)*. Phía `PM` được **đối chứng chéo** bằng ảnh chụp live của FLS.

### ⓐ Vật ↔ vật

| AS-IS *(GSheet)* | FLS | Khớp |
|---|---|:--:|
| `PM_Unpivot` — **3.772** dòng × **28** cột | `fls_pm_line` — giữ **27/28** cột | ⭐ **✅** |
| `Transaction Mapping L1` · vùng **NỀN** *(17 cột, mỗi cột khai một chữ cái nguồn `A`…`AL`)* | `fls_itl` *(6 canon + provenance)* | ◐ |
| `Transaction Mapping L1` · vùng **ADJUSTMENT** *(cột 21–45)* | `fls_adjustment` | ⛔ |
| `Transaction Mapping L1` · vùng **ALLOCATE** *(`CDT1 CFA1` · `CFA2`)* | ⛔ **⛔ KHÔNG có vật tương ứng** | ⛔ |
| `Transaction Mapping L1` · vùng **AUDIT** *(`ITL ID` · `PIC` · `Trạng thái`)* | `fls_journal` · `fls_queue_event` | ◐ |
| ⭐ **phép `VLOOKUP`** trên `PM_Unpivot!Reference number` | ⭐ **bảng** `fls_pm_link` | ⛔ **khác BẢN CHẤT** |

⭐ **Cột duy nhất FLS ⛔ không giữ là `Email Address`** — và đó là **quyết định có chủ ý** *(owner `17/09`: *"⛔ không lưu dữ liệu cá nhân"*, `NFR-I13`)*, ⛔ không phải một lỗ.

### ⓑ ⭐⭐⭐ Khác biệt BẢN CHẤT — và nó giải thích `GAP-ERD-P0-03`

```
AS-IS :  ghép = COPY một GIÁ TRỊ vào cột S/T của CHÍNH dòng sổ  (VLOOKUP)
FLS   :  ghép = THÊM một DÒNG vào bảng riêng `fls_pm_link`
```

| | AS-IS | FLS |
|---|---|---|
| Đọc sổ có thấy chủ dự toán ⛔không | ⭐ **CÓ** — nằm ngay cột `T` | ⛔ **KHÔNG** — `fls_itl.cdt1` = **0/8.387** |
| Ghép sai thì gỡ được ⛔không | ⛔ **không** *(ghi đè)* | ⭐ **có** — `fls_pm_unlink`, chỉ-thêm |
| Có lịch sử ghép ⛔không | ⛔ **không** | ⭐ **có** |
| Một dòng tiền gánh nhiều lệnh | ⛔ **không** *(một ô một giá trị)* | ⭐ **có** — `lan` |

> ⚰⚰⚰ **ĐÍNH CHÍNH `18/09` — `QĐ-ITL-141`. Đoạn ngay dưới đây SAI, giữ nguyên chữ làm bia.**
> Tôi gọi `fls_itl.cdt1 = 0/8.387` là một **bước lùi** so với bảng tính. Đọc mã thì ⛔ không phải: `NGUON_MAY = "may_goi_y"  # chi co goi y *_thyt` — máy **chỉ được gợi ý**, ⛔ **không** được ghi vào trường hợp đồng *(`QĐ-ITL-35`)*. Sổ hiện chủ dự toán **chỉ khi một NGƯỜI đã duyệt** — **cố ý**. ⇒ Phép so của tôi ⛔ **không công bằng**: `VLOOKUP` của bảng tính cho ra giá trị mà ⛔ **không có ai trong vòng lặp**, đúng thứ `INV-I16` dựng ra để chặn. **`GAP-ERD-P0-03` ĐÓNG — ⛔ không phải lỗi.**

⛔⛔ **⇒ Ở đúng việc module này sinh ra để làm — *gán chi phí vào đúng chủ dự toán* — AS-IS làm được, FLS ⛔ CHƯA.** `GAP-ERD-P0-03` ⛔ không còn là một nhận xét kiến trúc; nó là một **bước lùi đo được** so với thứ đang chạy.

### ⓒ Tỷ lệ ghép — hai hệ **cùng một bệnh**

| | AS-IS *(xuất `10/09`)* | FLS *(kho, `18/09`)* |
|---|--:|--:|
| Dòng sổ | **10.468** | **8.387** |
| Ghép được | **3.405** *(32%)* | **2.222** *(26,5%)* |
| ⛔ Ghép ⛔ không được | **7.060** *(67%)* `#N/A` | **6.165** *(73,5%)* |

⚠ Chênh `10.468` ↔ `8.387` phần lớn là **`1.919` dòng của 8 sheet owner chốt BỎ ngày `10/09`** *(`so-fls-nap-sai-tang-va-8-sheet-chet`)*, ⛔ không phải mất dữ liệu.

⭐ `32%` khớp con số **`33,8%` gần KỊCH TRẦN** đã đo ở `§10` — hai phép đo độc lập, cùng kết luận: **khoá `Reference number` chỉ với được tới một phần ba sổ.**

### ⓓ ⭐⭐⭐ `"Need to manual input"` — **7.060 ô**, và ⛔ chưa ai nhập

Đọc **công thức** *(⛔ không đọc giá trị)* vùng `ADJUSTMENT`:

| Cột | Ô có chữ | Công thức | Gõ tay |
|---|--:|--:|--:|
| `21` Budget Code | 10.373 | **0** | **10.373** |
| `26` Chủ dự toán | 10.463 | **0** | **10.463** |

⛔ Nhưng *"gõ tay"* ⛔ **không** nghĩa là *"có người quyết"*. Phân bố giá trị cột `26`:

| Giá trị | Ô | % |
|---|--:|--:|
| ⛔ **`Need to manual input`** | **7.060** | **67%** |
| `SHQ2 \| Headquarters2` | 2.051 | 19% |
| `SHQ1 \| Headquarters1` | 737 | 7% |

⭐⭐⭐ **`7.060` — ĐÚNG BẰNG số `#N/A` ở cột nền.** Tức AS-IS **đã có sẵn** một chỗ ghi *"cần người nhập"*, nó **đếm được**, và **⛔ chưa ai nhập**.

⛔⛔ ⇒ **Hàng chờ ⛔ không có lối ra *(`INV-I20`)* ⛔ KHÔNG phải bệnh của FLS — nó là bệnh KẾ THỪA, và FLS mới chỉ code hoá nó.** `US-045` *(«4 tuần ⛔ không ai gõ = cổng chết»)* hoá ra đã đúng từ trước khi FLS tồn tại.

### ⓔ Và mã ngân sách lớn nhất là **thùng rác**

Cột `21` có **37** giá trị khác nhau; đứng đầu:

| Mã | Ô | % |
|---|--:|--:|
| ⚠ **`OGA \| GAC - Other`** | **1.781** | **17%** |
| `LC \| License Cost` | 1.612 | 15% |
| `NB \| Lưu chuyển nội bộ` | 1.274 | 12% |

⇒ Khớp `gac-oth-catchall-nonopex`: `GAC-OTH` hứng gần như mọi thứ ⛔ không phân loại được. **Một trong sáu đồng chi phí đang mang nhãn *"khác"*.**

### ⓕ Ba việc tệp này KHAI RA, ⛔ không tự giải

| # | Việc | Ai quyết |
|:-:|---|---|
| ⓵ | `fls_itl.hd`/`cdt1`/`le` **phải được GHI** khi ghép — bằng ⛔ không thì FLS thua AS-IS ở đúng việc của nó *(`GAP-ERD-P0-03`)* | Tech Lead |
| ⓶ | Vùng **ALLOCATE** *(`CFA1`/`CFA2`)* ⛔ **không có** vật trong FLS — trong phạm vi hay ⛔ không? | **Owner** |
| ⓷ | `7.060` ô `"Need to manual input"` — **di trú sang FLS** thành rổ *cần người*, hay **bỏ**? | **Owner** |

---

## §6 · Cái sổ này CỐ Ý ⛔ không chứa

| Không chứa | Vì sao |
|---|---|
| **≈96 sheet Tầng A còn lại** *(trích được 43, kiểm kê ước 102)* | Nằm ngoài đường FLS đi qua ⇒ `K0` **đúng theo thiết kế**. Đưa vào chỉ làm loãng |
| **444 sheet toàn hệ** | `_PLAN` §5 đã phân tầng; Tầng C là kill-list |
| `H1000` lương · 4 ledger nền tảng | `QĐ-ITL-05` có trong phạm vi ITL nhưng **chưa tới lượt** |
| Ô `???` của bộ AS-IS | `Đ-5` — ⛔ không lấp bằng suy đoán. Đóng bằng **18 câu phỏng vấn** `_GUIDE_09` §6 |

---

## §8 · ⭐ KẾT QUẢ `Đ2` — đo hình dạng, đọc SỐNG *(2026-09-07)*

**Công cụ:** `tools/do_hinh_dang.py` · **Nguồn:** đọc **sống** qua Sheets API,
⛔ không dùng bản chụp *(bản chụp có tuổi **31–48 ngày** và đã chứng minh trôi
thật: `[Importrange]1.2 Ledger 112` chụp 7.626 → sống **9.148**)*.

### ⭐⭐⭐ Phát hiện lớn nhất: sheet `R |` có **BA tầng**, ⛔ không phải một

| Dòng | Là gì |
|:--:|---|
| **1** | ⭐⭐ **BẢN KHAI ÁNH XẠ** — các số `1..6` đánh dấu **cột nào giữ trường nào**, kèm chốt `KHÔNG XOÁ NHÉ`. `1`=Date · `2`=Description · `3`=Currency · `4`=Debit · `5`=Credit · `6`=Reference number — **khớp đúng thứ tự 6 cột của `Bank Transactions`** |
| **2** | Tiêu đề, **HAI VÙNG**: vùng **THÔ** *(tên nguyên bản của ngân hàng — khác nhau hoàn toàn)* + vùng **CHUẨN** `Date · Debit · Credit · Currency · Số bút toán/Ref` — **giống hệt nhau ở mọi bank** |
| **3+** | Dữ liệu |

⇒ ⭐⭐⭐ **Kế toán ĐÃ TỰ CHUẨN HOÁ.** Mỗi sheet mang sẵn một **hợp đồng đọc được
bằng máy**, do người **duy trì bằng tay**, và ⛔ **chưa tài liệu nào của ITL
nhắc đến nó**. `F04` ⛔ không phải phát minh lại phép chuẩn hoá — nó phải
**ĐỌC LẤY bản khai ở dòng 1**.

### Số đo trên **68/68** sheet `R |`

| Đo | Kết quả |
|---|---|
| Sheet khai **đủ 6 trường** | ⭐ **68 / 68** — đúng **MỘT** archetype |
| Bố trí cột khác nhau | **9** cách trên 68 sheet |
| Sheet có `#REF!` / `#N/A` ở dòng tiêu đề | ⛔ **12** |

⛔⛔ **`_GUIDE_09` §5 ghi CHỈ MỘT sheet hỏng** *(`R | BGO1`)*. Đo sống ra
**12**. ⇒ Con số trong guide **lạc hậu 12 lần**, và đó là hệ quả trực tiếp của
việc `G7` *(pass live)* ⛔ chưa bao giờ chạy.

⭐ **Và một cái bẫy đã ghi trong guide hoá ra ĐÃ ĐƯỢC GIẢI:** `R | HoangACB`
có **hai cột ngày** *(`Ngày hiệu lực` / `Ngày giao dịch`)* — `_GUIDE_09` §5
cảnh báo *"chọn sai là sai kỳ"*. Bản khai dòng 1 của chính sheet ấy chỉ thẳng
`Date` = cột **10** ⇒ **kế toán đã trả lời câu hỏi đó rồi**. Máy chỉ cần đọc.

### ⛔ Một phép kiểm của TÔI đã sai — ghi lại để không lặp

Bản đầu tôi kiểm `Date < Debit < Credit` và báo **8 sheet "thứ tự lạ"**.
⛔ **Sai.** Thứ tự cột khác nhau là **bình thường** — và đó **chính là lý do
bản khai tồn tại**. Một phép kiểm mã hoá giả định của người viết rồi gọi kết
quả là *"bất thường"* thì nó đang đo **giả định**, ⛔ không đo **sự thật**
*(`Đ-3`)*. Đã đổi thành **thống kê**, ⛔ không phải cảnh báo.

### Bậc sau `Đ2`

| Chỗ | Trước | Sau | Vì sao |
|---|:--:|:--:|---|
| `Bank Transactions` *(P100)* | `K0` | `K1` | Đo được hình dạng sống **8.341 dòng × 10 cột**; ⛔ chưa có bản khai phía FLS để so hai chiều |
| `Cash Ledger Transactions` | `K0` | `K1` | như trên |
| **Archetype 67 `R \|`** | `K0` | ⭐ `K2` | **68/68 khai đủ 6 trường**, có công cụ chạy lại được; ⛔ chưa thành cổng ⇒ chưa `K3` |
| `2. CCR` dòng `226` | `K0` | `K0` | ⛔ **`A-CCR_V2_Working` chưa có quyền đọc sống** — chỉ có bản chụp 28/07 |

⇒ **`GAP-ASIS-01` đóng được phần *hình dạng***: bảng lệch định dạng từng ngân
hàng nay **có, và sinh bằng lệnh** thay vì chép tay. ⛔ Còn mở phần *giá trị*.

⛔ **Mở mới — `GAP-ORA-09`:** `A-CCR_V2_Working` ⛔ chưa chia quyền cho máy đọc,
nên trọng tài số dư *(`2. CCR` dòng `226`)* — **thước chuẩn của cả lằn nhập**
theo `QĐ-ITL-91`… xin lỗi, theo bản vẽ kiến trúc §05 — ⛔ **chưa đo được lần
nào**.

---

## §7 · Việc kế tiếp *(cập nhật 2026-09-07 sau **`F04` chặng 1**)*

### ⭐ Đã xong — **5 phép đo, cả 5 chạy trên nguồn SỐNG**

| Bước | Việc | Kết quả |
|:--:|---|---|
| `Đ1` | Dựng sổ đối chiếu **46 dòng** | `K4` = **2/46**, ⛔ **0/24** thao tác kế toán đạt `K4` |
| `Đ2` | Hình dạng tầng nhập | ⭐ **68/68** sheet **một khuôn**; dòng 1 là **bản khai ánh xạ** *(§8)* |
| `Đ3` | Chênh tầng nhập ↔ tầng gộp | ⭐⭐ **KHÔNG TỒN TẠI** — `8.338 → 8.338` *(§9)* |
| `Đ4-a` | Khoá ghép `Mapping L1` | ⭐⭐ `33,8%` là **gần KỊCH TRẦN**, ⛔ không phải hỏng *(§10)* |
| `Đ5-a` | **Trọng tài số dư** dòng `226` | ⭐⭐ **GIỮ — 595/596 (99,8%)**; luật cũ **sai như đã ghi** *(§11)* |
| `Đ5-b` | **4 mục `L5` cuối** + đối chiếu **ERD** | ⭐⭐ Log **302.259 → 4.399** dùng được; `Num` khớp **100,0%**; `_Filter` là **cái cầu** *(§12)* |
| `Đ6` | **Cưỡng chế** — 5 phép đo thành cổng | ⭐⭐⭐ **Cổng chung #17**, 9 luật thuần + **32 phép thử**, và **ĐỎ NGAY** với 4 khuyết tật thật *(§13)* |
| `F04`-1 | **Dựng lại `Bank Transactions`** từ 60 sheet `R \|` | ⭐⭐⭐ **8.338/8.338 = 100,00%**, ⛔ 0 thừa 0 thiếu; **31 mã FLS trung thực hơn sheet** *(§14)* |

### ⛔ Chặn ở phía OWNER — ⛔ tôi ⛔ không tự gỡ được

| # | Cần gì | Mở khoá cái gì |
|:--:|---|---|
| ~~1~~ | ~~**Link `A-CCR` ĐANG CHẠY**~~ | ✅ **ĐÓNG 07/09 — `QĐ-ITL-101`**, và quyết định ấy hoá ra **TỐT HƠN**: trọng tài số dư **đã sống sẵn** trong `P100 ▸ BankAccountList` dưới dạng **cờ đúng/sai TỪNG TÀI KHOẢN** — mạnh hơn một con số toàn công ty trên bản chụp chết. ⇒ Cổng #17 lên **12 phép kiểm** và bắt ngay **4 khuyết tật** |
| **1b** ⛔⛔ ⭐ **MỚI** | **DUYỆT cú GHI của `F04` chặng 3** vào `A-CCR ▸ Bank Transactions` | `GAP-PLAN-05`. Chặng 1 đã chứng minh FLS **dựng ra đúng thứ đó**; nhưng *dựng đúng* ⛔ **không** phải *được phép ghi* — đây là **sổ kế toán đang sống**, cú ghi **khó đảo**. ⛔ Tôi ⛔ không suy quyền ghi ra từ `QĐ-ITL-100` |
| **1c** ⛔ ⭐ **MỚI** | **Chuyển kế toán 4 khuyết tật** `GAP-KT-01..04` | Nặng nhất **`R \| PO BGO1`**: danh mục trỏ vào sheet ⛔ **không tồn tại** ⇒ **−42.164.521 đ ⛔ chưa từng được đối soát**. ⛔ FLS ⛔ không tự sửa dữ liệu của họ *(`QĐ-ITL-34`)* |
| 2 | **18 câu phỏng vấn** `_GUIDE_09` §6 → Lan·Thương / ThomHT·AnhMC / ThươngCT / Hoài / KTT | `Đ4` — **24/46 dòng** của sổ. **17/24** ô *Ai* còn `???`, và `Đ-5` cấm lấp bằng suy đoán |
| 3 | Một câu trả lời: ***6.782** giao dịch ngân hàng ⛔ chưa có đề nghị thanh toán — đáng lẽ phải có ⛔ hay không?* | Biến `QĐ-ITL-94` từ *"đã đo"* thành *"đã hiểu"*. Đây là con số phải theo dõi, ⛔ không phải *"tỷ lệ ghép"* |

### ⭐ Làm được NGAY, ⛔ không chờ ai

| Bước | Việc | Vì sao đáng làm trước |
|:--:|---|---|
| ~~`Đ5-b`~~ | ⭐ **XONG** — `§5` đóng cả 5 mục; ERD đối chiếu ở `DD-I09` *(§12)* | ⭐ Log **302.259 → 4.399**; `Num` khớp **100,0%**; `_Filter` là **cái cầu** |
| ~~`Đ6`~~ | ⭐ **XONG** — **cổng chung #17**: ~~7 luật, 7/7~~ ⭐ **9 luật / 12 phép kiểm**, nay **8 đạt · ⛔ 4 ĐỎ**, 25 giây *(§13)* | ⭐ `K4` **2/46 → 8/46**. ⛔⛔ **4 đỏ là ĐỎ THẬT** *(`GAP-KT-01..04`)* — một cổng **chưa từng đỏ** thì mới là cổng ⛔ chưa được chứng minh |
| ~~`F04`-1~~ | ⭐⭐⭐ **XONG — DỰNG.** FLS dựng lại `Bank Transactions`: **8.338/8.338 = 100,00%** *(§14)* | ⭐ Đây là **phép chứng minh** cho `QĐ-ITL-100`: muốn **thay** cú đẩy thì phải **dựng ra đúng thứ nó đang chở** |
| ~~`F04`-2~~ | ⭐⭐⭐ **XONG — SOÁT.** 8 luật `S1`…`S8` chạy trên **dữ liệu vừa nạp**; lật **3** kết luận *(§15)* | ⭐ `S1` **ĐẠT** ⇒ ⛔ **0 lỗi nào của FLS**; **5 cờ** là khuyết tật **có sẵn trong sổ**. ⭐⭐ Và nó chứng minh **thủ phạm 31 mã hỏng là chặng `Run`** *(nguồn `R \|` sạch 0/8.338)*. ⚠ Phần **màn hình** vẫn bị `GAP-SCR-10` chặn |
| ⛔⛔ **`F04`-3** | **ĐẨY** — ghi thật vào `A-CCR ▸ Bank Transactions` | ⛔ **⛔ KHÔNG làm được ngay — chặn ở owner** *(`GAP-PLAN-05`)*. Xếp ở đây để ⛔ **không ai tưởng** nó thuộc nhóm *"làm được ngay"* chỉ vì chặng 1 và 2 thuộc nhóm ấy |

---

---

## Changelog
- **v1.2** *(2026-09-07, `F04` chặng 2 — SOÁT)*: ⭐⭐⭐ **Thêm `§15`.** Tám luật `S1`…`S8` *(`fls/kiem/soat_nap.py`, **31 phép thử** offline)* + cổng `tools/soat_nap_sao_ke.py`. **`S1` ĐẠT ⇒ ⛔ 0 lỗi nào CỦA FLS**; **5 cờ** là khuyết tật có sẵn trong sổ. ⭐⭐ **Ba cái bị lật:** ⓵ **thủ phạm làm hỏng 31 mã là chính chặng `Run`** *(nguồn `R |` sạch **0/8.338**)*; ⓶ **`GAP-KT-03` chẩn đoán SAI** — ⛔ không thiếu sheet nào, mà là **HAI lỗi gõ MỘT ký tự trong danh mục** *(thừa `1` · thừa `7`, giống 98%)*, và cổng #17 ⛔ **không thể tự thấy** vì nó chỉ nhìn **một chiều**; ⓷ **`S8` tự lộ điểm mù của chính nó** — suy tập nguồn từ *dữ liệu* nên sheet ra **0 dòng** biến mất khỏi phép kiểm sinh ra để tìm nó. ⛔ **Hai lỗi của tôi, cả hai do MÁY bắt**: xếp `S8` vào `CHẶN` *(tự mâu thuẫn với định nghĩa tôi tự viết)*, và **ba bản sao** của bản khai ánh xạ *(bắt bởi chính bài tôi viết ở chặng 1)*. ⇒ `K4` **9/46 → 11/46**.
- **v1.1** *(2026-09-07, đồng bộ §7 với chính thân sổ)*: ⛔⛔ **§7 đang mâu thuẫn với §12–§14 của chính nó** — tiêu đề còn ghi *"sau `Đ5-a`"*, bảng *Đã xong* dừng ở `Đ5-a` **dù `Đ5-b`/`Đ6`/`F04`-1 đã xong và đã viết ở §12/§13/§14**, và **mục chặn số `1` *(`GAP-ORA-09`)* vẫn nằm đó dù changelog `v1.0` ngay bên dưới đã ghi nó ĐÓNG**. ⇒ Bổ **4 dòng đã xong**, gạch mục `1`, thêm **`1b`** *(⛔ **owner duyệt cú GHI** — `GAP-PLAN-05`)* và **`1c`** *(chuyển kế toán `GAP-KT-01..04`)*, thêm **`F04`-2 SOÁT** vào nhóm *làm được ngay* và **`F04`-3 ĐẨY** vào nhóm *⛔ không*. ⭐ **Bài học:** một sổ ghi *"việc kế tiếp"* ⛔ **không tự già đi cùng nhịp với thân nó** — nên phần *kế tiếp* phải sửa **cùng lượt** với phần *kết quả*, ⛔ không để lượt sau.
- **v1.0** *(2026-09-07, owner chốt 2 việc)*: ⭐ **`GAP-SCOPE-02` ĐÓNG** *(thay **CÚ ĐẨY**, ⛔ không thay `P100` ⇒ hạ nguồn ⛔ không đổi một dòng)* và ⭐ **`GAP-ORA-09` ĐÓNG** *(⛔ không theo đuổi `A-CCR` sống)*. ⭐⭐⭐ **Quyết định thứ hai hoá ra TỐT HƠN**: trọng tài số dư **đã có sẵn và đang SỐNG** ở `P100 ▸ BankAccountList` — **N lá cờ per-tài-khoản** thay vì **một con số tổng trên bản chụp chết**. ⇒ `L5` đổi nguồn, thêm `L8` *(cờ của chính kế toán)* + `L9` *(danh mục ↔ sheet)*; cổng #17 **7 → 12 phép so**. ⛔⛔ **Và cổng ĐỎ NGAY 4 chỗ, thật**: `R \| PO BGO1` lệch **−42.164.521 VND** · `R \| Pingpong` lệch · **2** tài khoản bank `Active` ⛔ không có sheet · **5** dòng quỹ đánh `Active` mà ⛔ không có tên. ⭐ Ba luật cùng chỉ vào **một nguyên nhân**: danh mục trỏ tới sheet ⛔ không tồn tại ⇒ `INDIRECT` hỏng ⇒ sao kê đọc **0**. ⛔ **⛔ Không nới cổng** *(`R-A5`)*. ⛔ Và **một lỗi nữa của tôi**: khoá dict bằng **tên** *(có trùng, có rỗng)* ⇒ **nuốt dòng** — `9` vs `19`; khoá nay mang **số dòng**. ⇒ trọng tài `K3`→⭐`K4`, **`K4` = 9/46**.
- **v0.9** *(2026-09-07, rà chặn)*: ⚠ **`OP-21`/`OP-22` ⛔ KHÔNG chặn `F04`/`F05`** như sổ đã ghi. Hai danh mục **đọc được ngay**, và nhỏ hơn sổ ghi rất nhiều: `BankAccountList` ~~3.003~~ ⭐ **70 dòng thật**, `Cash Ledger List` ~~997~~ ⭐ **15**. ⛔ Cả hai con số cũ là **ô LƯỚI** — **lần thứ NĂM** cùng một cái bẫy trong một ngày. ⭐⭐ Và `BankAccountList` **tự khai DẢI ĐỌC** `Range_Condition`/`Range_Debit`/`Range_Credit` cho từng tài khoản ⇒ **hợp đồng đọc-được-bằng-máy THỨ HAI** của hệ *(sau bản khai dòng 1)*; kèm cột tự đối soát `Check vs Bank Transactions`. ⇒ `K0`→`K1` cả hai.
- **v0.8** *(2026-09-07, `Đ6` cưỡng chế)*: ⭐⭐⭐ **5 phép đo thành CỔNG CHUNG #17** — 7 luật, **7/7 đạt**, chạy **25 giây** trên nguồn **sống**. Kiến trúc 3 lớp: **luật thuần** *(`fls/kiem/nguon_song.py`)* · **25 bài đỏ-thử offline** *(mỗi luật có ca XANH + ĐỎ thật + RỖNG)* · **vỏ I/O** *(`tools/kiem_nguon_song.py`)* — vì một cổng đọc mạng ⛔ không tự chứng minh được là **đỏ được**. ⛔⛔ **Luật chung *"đo được 0 thứ ⇒ ĐỎ"* cứu ngay lần chạy đầu**: `L6` đỏ vì `doc_cot()` **ép mọi ô về chuỗi** ⇒ `Num` hết là số, luật đếm được **0 dòng** — ⛔ không có luật ấy thì cổng đã **XANH GIẢ** trên một phép đo **chưa từng chạy**. ⇒ ⭐⭐ **`K4` đi từ `2/46` lên `8/46`**. ⛔ Trọng tài số dư **giữ `K3`**: cổng đang canh **bản chụp 19 ngày tuổi**, mà **cổng trên nguồn chết là cổng ⛔ không bắn được**.
- **v0.7** *(2026-09-07, `Đ5-b` + đối chiếu ERD)*: ⭐⭐ **`§5` ĐÓNG cả 5 mục.** ⛔⛔ Nặng nhất: nhật ký thay đổi **đã tồn tại** nhưng **`302.259` → chỉ `4.399` dùng được** — `302.259` là **ô LƯỚI**, và **51.178** dòng mang khoá **hỏng** `NaNNaNNaN|||` *(sổ quỹ hỏng **99,6%**, còn **69** khoá khác nhau)* ⇒ điều kiện nghiệm thu `INV-I04b` **hẹp lại**. ⭐ Khuôn khoá thì **đúng**. ⭐⭐ **`Num` = thứ tự lần xuất hiện của mã, khớp `8.331/8.331` = 100,0%** ⇒ phép chống trùng AS-IS **đã chạy đúng tuyệt đối**; `Check trùng` **92,1%** và luôn đếm thiếu ⇒ ⛔ không dùng. ⭐⭐ `Bank Transactions_Filter` ⛔ **không phải bộ lọc** — nó là **CÁI CẦU** bank→sổ kế toán, và **bằng** bản gốc 8.338 dòng *(*"+98"* là ô lưới)*. ⭐ Kho **xoá-có-vết** đã có sẵn *(50 dòng, 3 lý do)* = hình của `INV-I03`. ⇒ Ghi toàn bộ chênh vào `05_DATA_DICTIONARY_ERD` §**`DD-I09`** *(v0.19)*, kèm **3 mắt xích ERD chưa hề nhắc**.
- **v0.6** *(2026-09-07)*: Cập nhật **§7** cho khớp thực tế — 5 phép đo đã chạy; tách rõ **3 việc chặn ở owner** *(link `A-CCR` sống · 18 câu phỏng vấn · câu hỏi 6.782 giao dịch)* khỏi **2 việc làm được ngay** *(`Đ5-b` 4 mục `L5`, `Đ6` cưỡng chế)*. ⭐ Nói thẳng vì sao `K4` **vẫn 2/46**: sáu dòng đã rời `K0` nhưng ⛔ không dòng nào lên `K4`, vì cả 4 công cụ **chạy bằng tay** — **một phép đo ⛔ không tự đỏ thì chưa canh gì cả**.
- **v0.5** *(2026-09-07, `Đ5-a` — trọng tài số dư, đo được lần đầu)*: ⭐⭐ **Kết quả TỐT đầu tiên của cả `Đ`: trọng tài GIỮ — `595/596` ngày đạt (99,8%)**, và ⛔ **không** ngày nào rơi giữa `1` và `1.000 VND` ⇒ phân bố **sạch**. ⛔ Nhưng **luật như đã ghi là SAI**: *"`DIF = 0` đúng từng đồng"* ⛔ không đúng — **363/596** ngày mang **bụi dấu phẩy động** *(2⁻¹⁶)* sinh từ phép **nhân tỷ giá**; luật đúng là **`|DIF| < 1.000 VND`**. ⛔⛔ **Ba cái bẫy, tôi mắc cả ba**: *412 ô khác 0* → bụi; *49 ngày lệch* → **2 sự kiện**; *lệch 9,53 tỷ 48 ngày* → ⛔⛔ **tệp là BẢN CHỤP**. ⭐⭐⭐ Cả hai sổ giao dịch trong A-CCR dừng ở **19/08**, nhưng cột ngày **dựng sẵn tới 6-Oct** và công thức **chuyển tiếp** ⇒ **mở ra hôm nay thấy cột HÔM NAY đầy số, mà số ấy 19 NGÀY TUỔI**, ⛔ không một dấu hiệu nào báo. ⇒ Luật cho FLS: **mọi cửa đọc phải trả TUỔI của số**. `L3` mục 5 `K0`→⭐`K3`; ⛔ `GAP-ORA-09` **vẫn mở**.
- **v0.4** *(2026-09-07, `Đ4-a`)*: ⭐⭐ **Giả thuyết `Đ3` sinh ra đã CHẾT — và cái chết ấy lật một con số đã tin bấy lâu.** `M_chuỗi = M_kiểu = 3.412` ⇒ ⛔ **0 dòng** mất vì kiểu ô. ⭐⭐⭐ **`33,8%` ⛔ không phải phép ghép hỏng: trần của nó là 3.237** vì `PM_Unpivot` chỉ có từng ấy mã, nên ghép `3.412/10.194` là **gần kịch trần**. **6.782 dòng** *(66,5%)* là **giao dịch ngân hàng chưa có đề nghị thanh toán** — **nghiệp vụ**, ⛔ không phải lỗi. ⛔⛔ Khuyết tật thật: cột 13 có **7.372 ô `#N/A`** *(68,4%)* trông như **đã đầy**. ⛔ Và **dụng cụ của tôi sai lần thứ BA trong một phiên** — đếm `#N/A` là *có giá trị* ra `105,7%`; tỷ lệ **không thể có** ấy là dấu hiệu **duy nhất**. ⇒ Luật mới: **mỗi tỷ lệ phải khai khoảng hợp lệ trước, và tự đỏ khi rơi ra ngoài**. ⚠ Hẹp lại `GAP-ORA-10`.
- **v0.3** *(2026-09-07, `Đ3` chạy thật)*: ⭐⭐⭐ **Chênh `7.294` dòng ⛔ KHÔNG TỒN TẠI.** Đo sống: tầng nhập **8.338** dòng thật → tầng gộp **8.338**, **50/50** tài khoản khớp **đúng từng dòng**, phân bố theo **năm trùng khít cả ba năm**, và đối **tập khoá** cho **7.905 = 7.905** mã khác nhau. ⛔⛔ `Đ1` đã **đếm bằng LƯỚI** ở một đầu — ô lưới trống ⛔ không phải dòng ⇒ *"44% sổ có thể mất"* là **báo động giả** đứng trong tài liệu một ngày. ⭐⭐ Hai thứ làm được điều đó: cột **`Source`** ghi **xuất xứ từng dòng**, và **dòng 1 là bộ đếm sống** để đối chứng phép đếm của ta. ⛔⛔ **Dụng cụ của tôi lại sai — lần thứ hai trong hai bước**: đọc mã bằng `FORMATTED_VALUE` sinh **1.468 dòng lệch GIẢ** *(ký hiệu khoa học)*; đọc thô còn **31**. ⛔ Khuyết tật còn lại nằm đúng trên **cái khoá**: **45% mã lưu kiểu SỐ** · 280 mã trùng/706 dòng · 7 dòng không mã · 1 dòng cụt. ⭐ Đóng **§5 mục 5**; mở **`GAP-ORA-10`**.
- **v0.2** *(2026-09-07, `Đ2` chạy thật)*: ⭐⭐⭐ **Sheet `R |` có BA tầng, ⛔ không phải một** — dòng 1 là **bản khai ánh xạ** do kế toán tự duy trì, dòng 2 có **vùng CHUẨN giống hệt nhau ở mọi bank**. ⇒ Kế toán **đã tự chuẩn hoá**; `F04` phải **đọc lấy** bản khai, ⛔ không phát minh lại. Đo **68/68** sheet khai **đủ 6 trường** ⇒ đúng **MỘT** archetype *(9 bố trí cột)*. ⛔⛔ **12 sheet có `#REF!`/`#N/A`** trong khi `_GUIDE_09` §5 ghi **chỉ 1** — lạc hậu **12 lần**, hệ quả của việc `G7` ⛔ chưa chạy. ⭐ Bẫy `R | HoangACB` *(hai cột ngày)* **đã được giải sẵn** bởi chính bản khai. ⛔ Và **một phép kiểm của tôi đã sai** — `Date < Debit < Credit` là **giả định của tôi**, ⛔ không phải sự thật của sổ *(`Đ-3`)*. Mở `GAP-ORA-09` *(`A-CCR` ⛔ chưa có quyền đọc sống)*.
- **v0.1** *(2026-09-07)*: Khởi tạo — bước `Đ1`. **46 dòng** *(24 `L4` + 6 `L1` + 6 `L2` + 5 `L3` + 5 `L5`)*, trích bằng máy phần trích được *(24 `OP` từ `_GUIDE_09` · 17 tuyến · 18 bảng · 43 sheet Tầng A)*. ⛔⛔ **Kết quả đáng nói nhất: `K4` = 2/46, và ⛔ KHÔNG một thao tác kế toán nào đạt `K4`** — nghĩa là **phép đo chưa tồn tại**, ⛔ không phải FLS sai. ⭐ Sáu dòng `K1` là chỗ FLS **cố ý ⛔ không khớp** AS-IS, mỗi chỗ có một quyết định đứng sau; ⛔ chúng ⛔ không được âm thầm kéo lên `K3`.
