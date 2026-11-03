# Lộ trình cập nhật tài liệu BA theo mục tiêu thiết kế mới

**Version:** v0.1 · **Ngày:** 2026-08-24 · **Loại:** kế hoạch tài liệu (doc-only, Class A)

**Vì sao có bản này:** phiên rà thiết kế 2026-08-24 *(grill)* sinh **10 quyết định** và **một đổi hướng kiến trúc**. Nhiều tài liệu BA đang mô tả kiến trúc **đã bị lật**. Bản này là thứ tự sửa, theo **phụ thuộc**, không theo cảm giác gấp.

---

## §1 · Mười quyết định phải được phản ánh

| ID | Quyết định | Lật / sửa cái gì |
|---|---|---|
| `QĐ-ITL-35` | **Hai đầu ra song song, hai cổng tách rời.** Cột `Final` khớp sổ **100%** *(sản phẩm A)*; cột `*_thật` **không** vào parity — để trống chỗ máy tự bịa, đi vào hàng chờ. ⚠ Bị siết bởi `AUD-12`: `*_thật` **chỉ** biến giá trị **máy tự bịa** thành trống, **không bao giờ** chạm giá trị người nhập | thêm mới |
| `QĐ-ITL-36` | **Oracle = ảnh chụp đóng băng từ FILE GỐC `ITL Ledge`.** ⛔ Loại `ITL_altered` *(sai 680 `HD` + 1.048 `CDT`)*. ⛔ Loại **bản copy** — đã chứng minh nó **tự sản xuất giá trị mặc định**, `0` ô lỗi ⇒ nguy hơn `#REF!` | `GAP-ITL-48` còn **1 tầng**, không phải 3 |
| `QĐ-ITL-37` | **Ảnh chụp tự soi**: kiểm `Final == f(Classifying, U)` từng dòng; dòng không tự nhất quán ⇒ **loại khỏi oracle**. Chụp **cả đầu vào lẫn đầu ra** cùng lần đọc. Không xin cửa sổ đóng băng của kế toán | thêm mới |
| `QĐ-ITL-38` ⭐⭐ | **ĐỔI HƯỚNG ĐẦU RA.** `Cloud SQL Postgres` = **bản ghi chính** · `BigQuery` = **bản sao cho engine P&L** · **APP** = nơi kế toán thao tác *(thay Google Sheets)* · client **tự lưu theo lô** | ⛔ **lật `QĐ-ITL-31`** *(kết quả về Google Sheet máy sở hữu)* · ⛔ **lật phần "sheet gương 3 tab" của `QĐ-ITL-33`** · vượt ranh `INV-13` của A-CCR *(nghiệp vụ thật vẫn trên GS)* |
| `QĐ-ITL-39` | **Lát A** — app cầm **cả sổ**, theo đúng `IM1 → IM7` đã lập. *(Lát B — chỉ 7 trường ADJUSTMENT — đã cân nhắc và bỏ)* | xác nhận `03_PRODUCT_LIFECYCLE` |
| `QĐ-ITL-40` | **Cắt tại MỐC KỲ**, không phải giai đoạn song song. Ba điều kiện: ⑴ parity đạt trên cột **máy tính** · ⑵ **chạy thử di trú `U` khớp 100%** · ⑶ **owner tự** đặt Sheets về chỉ-đọc. **Sửa `D4`**: *chạy song song và khớp* chỉ áp **cột máy tính**; **cột người gõ** dùng cổng **di trú trạng thái** — vì song song ở đó là **bất khả** *(`QĐ-ITL-34` cấm ghi ngược, `QĐ-ITL-32` đã loại gõ đôi)* | sửa luật `D4` |
| `QĐ-ITL-41` | **Giữ "cấm ngưỡng" làm luật, đổi HẠT ĐO cho việc dựng-lại-từ-nguồn.** Bốn bất biến chính xác thay cho dung sai: ⑴ mỗi giao dịch **đúng 1 lần** · ⑵ tổng theo `(tài khoản × ngày)` khớp **đến đồng** · ⑶ **tập khoá** bằng nhau, chênh **liệt kê từng dòng** · ⑷ `#N/A`/unmatched **có tên nguyên nhân** | ⛔ **bỏ chữ "trong dung sai"** khỏi cổng `IM1` |
| `QĐ-ITL-42` | **Đóng băng `ITL-CONTRACT` = 13 trường**; **reader đổi từ đọc-theo-VỊ-TRÍ sang đọc-theo-TÊN** *(`CR` loại 3)*; **khối ADJUSTMENT 6–7 ra khỏi đường P&L** ⇒ việc code hoá gõ tay **7 khối → 5 khối** | `02_VERSION_ORCHESTRATION`, `05_DATA_DICTIONARY_ERD` |
| `QĐ-ITL-43` | **Hai khoá, hai việc.** `INV-I04a` `itl_id` = **số thứ tự cấp khi vào sổ, đóng băng** = danh tính · `INV-I04b` **khoá nội dung có `UNIQUE`** = **chỉ để đối sánh**, không phải danh tính | **tái khẳng định `QĐ-ITL-30`**; rút lại đề xuất "khoá nội dung làm `itl_id`" |
| `QĐ-ITL-44` | **Thứ tự build:** ① đóng băng hợp đồng + đổi reader → ② **adapter A+B → 36 cột canonical** *(toàn bộ việc khó)* → ③ **lớp `ITL Ledge` mỏng** *(6 chép + 1 đánh số + 5 câu `if` + 1 join)* → ④ **cải thiện phép ghép PM** *(bắt đầu từ 158 dòng đã đo, 19,57 tỷ)* | `03_IMPLEMENTATION_PLAN` |

**Kèm `AUD-12`** *(đã áp vào tài liệu)*: mã `FT<yy><ddd>` **không mang ý nghĩa thời gian**; **input trong sheet là SSOT** ⇒ phát hiện *"93% hoán ngày↔tháng"* **rút lại**.

---

## §2 · Phát hiện quan trọng nhất để viết lại tài liệu

★★ **Toàn bộ "logic" của `ITL Ledge` là tầm thường**: 6 phép chép + 1 phép đánh số + **5 câu `if` giống nhau** + 1 phép join. Việc khó nằm **hết ở adapter** — thứ sản xuất ra `Classifying`.

Và **66% dòng phải gõ tay không phải tính chất của `ITL Ledge`** — nó là **hệ quả của PM không ghép được**. Cột `I` trống vì thượng nguồn thiếu `HDCode`.

⇒ Mọi tài liệu đang mô tả *"vùng ADJUSTMENT là chỗ khó"* cần đổi khung: **chỗ khó là phép ghép ở thượng nguồn.**

---

## §3 · Lộ trình — 5 đợt, theo phụ thuộc

### ✅ Đợt 0 · Chốt danh tính quyết định — **XONG 2026-08-24**

| File | Việc | Ước |
|---|---|--:|
| ✅ `00_MASTER_INDEX.md` | **XONG** — thêm `QĐ-ITL-35…44` + `AUD-12`; `QĐ-ITL-31` **⛔ bị lật một phần** *(giữ "chỉ đọc", bỏ "đổ về Google Sheet")*; `QĐ-ITL-33` **⛔ bị lật một phần** *(giữ thứ tự + "không đổi thao tác" cho `IM1–IM5`, bỏ "sheet gương 3 tab", siết lại "cấm ngưỡng")* | ✅ |
| `01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md` | Cập nhật §trạng thái *(đầu ra không còn là Sheet)*; thêm `GAP-ITL-53…59`, `AUD-10/11/12` | S |

### ✅ Đợt 1 · Hợp đồng đầu ra — **XONG 2026-08-24** *(còn nợ đúng 1 việc: test tương thích engine)*

| File | Việc | Ước |
|---|---|--:|
| ✅ `02_BA/05_DATA_DICTIONARY_ERD.md` **v0.4** | **XONG** — `ITL-CONTRACT` **v1.0 ĐÓNG BĂNG** theo TÊN; khối 6–7 ngoài hợp đồng; **§0 trỏ 2 tài liệu FLS** + kế thừa **Nguyên tắc số 1**; `DD-I05` hoà giải hai khoá; **`DD-I06` mới** — chứng cứ đo. 347 → **455 dòng** | ✅ |
| ✅ `01_Orchestrator/02_VERSION_ORCHESTRATION.md` | **XONG** — `v1.0-candidate` → **`v1.0` ĐÓNG BĂNG**; ⛔ còn nợ **test tương thích engine tự động** ⇒ *đóng băng trên giấy, chưa được cưỡng chế* | ✅ |
| ✅ `02_BA/11_INVARIANTS.md` **v0.3** | **XONG** — tách `INV-I04a`/`INV-I04b`; thêm `INV-I15` *(pháp nhân)* + **`INV-I16` mới** *(máy không được tự trả lời thay người)*; `INV-I07` diễn giải lại theo `QĐ-ITL-42`; mục **`ACC-1..4`** — cấm viết dung sai | ✅ |

### ✅ Đợt 2 · Kiến trúc + màn hình — **PHẦN LỚN XONG 2026-08-24**

Ngoài bảng dưới, đã làm thêm *(việc thiết kế trước code)*: ✅ `03_Dev/02_REPO_CONVENTIONS` v1.0 · ✅ `03_Dev/04_DB_IMPLEMENTATION` v1.0 *(schema `fls_itl` 3 lớp)* · ✅ `04_Test/01_TESTING_FRAMEWORK` v1.0.

| File | Việc | Ước |
|---|---|--:|
| ✅ `03_Dev/01_TECH_DESIGN.md` **v1.0** | **XONG** — viết mới cho FLS độc lập; ADR-FLS-01 + 2 phương án loại; repo layer từ ngày 0; cột `*_thyt` + oracle-là-cấu-phần | ✅ |
| ✅ `02_BA/07_API_CONTRACT.md` **v1.0** | **XONG** — prefix `/api/fls/v1/`; ghi = APPEND; chỉ 5 trường ADJUSTMENT + lý do; 409 khi gõ khác nguồn | ✅ |
| ✅ `02_BA/06_SCREEN_SPEC.md` **v1.0** | **XONG** — đóng `GAP-ITL-53`; §1 **8 hành vi Sheets bắt buộc**; 5 màn SCR-F01..F05; SCR-F02 field-level | ✅ |
| `02_BA/04_ROLE_PERMISSION_MATRIX.md` | RBAC **trên app**, không phải trên sheet; `AUD-1` 7 trường + `actor` từ token | M |
| `02_BA/08_NFR.md` | `NFR-07` **độ trễ sync PG→BQ**; thêm **độ trễ gõ ô** *(ràng buộc đã đo: load-job APPEND ~2–4s ⇒ vì sao phải ghi theo lô)* | S |

### Đợt 3 · Nghiệm thu & lộ trình

| File | Việc | Ước |
|---|---|--:|
| `01_Orchestrator/03_PRODUCT_LIFECYCLE.md` | Cổng `IM1`: **bỏ "trong dung sai"**, thay **4 bất biến**. `IM6`: thêm **điều kiện di trú `U` khớp 100%**. `IM7`: **công tắc mốc kỳ + 3 điều kiện** | M |
| `01_Orchestrator/08_MIGRATION_ROADMAP.md` | Viết lại theo `QĐ-ITL-38/39/40` | M |
| `02_BA/Artifacts/Phuong-phap-luan-Codehoa-va-Thiet-ke-TOBE.md` | Sửa `D1`/`D4`; **oracle 3 tầng → 1 tầng**; thêm **loại A / loại B** và hạt đo khác nhau | M |
| `02_BA/Artifacts/Lo-trinh-Chuyen-doi-Gsheet-to-UI.md` | ⛔ **Lật khung** — không còn *"giữ một phần giao diện Gsheet"* | M |

### Đợt 4 · Sửa số sai đã phát hiện

| File | Việc | Ước |
|---|---|--:|
| `02_BA/01_BRD.md` | ⚠ **`6.843` KHÔNG phải "ô nhập tay"** — nó là số ô **còn nguyên cờ `Input here`**, tức **ô bị gán mặc định im lặng** *(bằng chứng: `_GUIDE_00_Inventory` `T3/X3/AB3/AF3/AJ3/AN3/AR3`)*. Đo lại 24/08 trên 2 khối: **7.476 ô**. Nhãn cột "Trường được nhập tay / Số ô" phải đổi | M |
| `02_BA/09_STATE_MACHINE_SPEC.md` | 7 trường → **5 trường trong hợp đồng**; 2 trường còn lại sang adapter F | S |
| `02_BA/Artifacts/UC-US-Ke-toan-PM-den-ITL.md` | `AUD-10` *(§4 ghi "6 UC ★" nhưng đếm được 5)*; `GAP-ITL-56` *(luật 6 nhãn không tái lập được `3.480/92%`)*; `GAP-ITL-57` *(70 hay 158 dòng)*; `US-036`/`US-041` **đã đo** | M |
| `02_BA/10_DECISION_TABLE.md` | ✅ **đã sửa** mục 3 theo `AUD-12` | — |

### Đợt 5 · Còn là bản copy chương trình, chưa dẫn xuất cho ITL

| File | Trạng thái |
|---|---|
| ✅ `02_BA/03_USER_STORY.md` **v1.0** | **XONG** — không lặp 45 US, trỏ SSOT Artifacts, nhóm 6 epic theo phạm vi build; trục = 5 trường ADJUSTMENT. `02_PROCESS_FLOW` vẫn ⏸ |
| ✅ `04_Test/01_TESTING_FRAMEWORK.md` **v1.0** | **XONG** — 4 cổng G1-G4, ACC-1..4 thành test case. `02_TESTCASE`/`03_TRACEABILITY` vẫn ⏸ |

---

## §3b · Cập nhật chiều 2026-08-24 — hai quyết định đổi phạm vi

| ID | Quyết định | Xoá khỏi đường tới hạn |
|---|---|---|
| `QĐ-ITL-45` | **FLS độc lập** code + DB với FPA và P100 | việc port vào `FPA-T4`; ngược lại **thêm** việc tự dựng auth/RBAC/FE/CI |
| `QĐ-ITL-46` | Đích: FPA đọc **một bảng `ITL` trên BQ**; ⏸ **giai đoạn này chưa làm** | ⛔ cách FPA lấy sổ · ⛔ đổi reader sang đọc theo tên *(`QĐ-ITL-42` — hoãn, không bỏ)* · ⛔ mọi việc đấu nối |

⇒ **Giai đoạn này FLS chỉ cần: từ input dựng được sổ `ITL` trong DB của chính nó, đúng `ITL-CONTRACT` 14 trường.**

✅ **Việc ① của `QĐ-ITL-44` XONG**: `test_itl_contract_v1_lock.py` — 10 test PASS, khoá cả 14 vị trí. *(Nằm trong repo `FPA-T4`, chưa commit — chờ anh quyết; nó bảo vệ reader hiện tại khỏi trôi cột im lặng, nên vẫn có giá trị ngay cả khi việc đấu nối hoãn.)*

---

## §3c · Bản đồ ảnh hưởng — phát hiện 64-cột / ALLOCATE / Final=sửa (2026-08-24)

Bốn phát hiện lan ra tài liệu: ⑴ hợp đồng **14 trường** (`le=P`, `+acct`) không phải 13; ⑵ `ITL Ledge` **64 cột, 4 vùng**; ⑶ **ALLOCATE máy suy từ `Mapping Master`**; ⑷ **`Final` = kế toán nhập/sửa**, bỏ tầng `MID`. Rà toàn bộ `.md` — phân ba nhóm:

### ✅ Đã cập nhật theo phát hiện

| File | Sửa |
|---|---|
| `03_Dev/04_DB_IMPLEMENTATION` v1.2 | §0 bản đồ 64 cột · +ALLOCATE/`fls_mapping_master` · §4b cơ chế phân bổ · Final=sửa |
| `02_BA/05_DATA_DICTIONARY_ERD` v0.5 | 14 trường, `le=P`, `DD-I06` chứng cứ |
| `02_BA/11_INVARIANTS` v0.4 | `INV-I04a/b` · `INV-I15` đóng · `INV-I16` |
| `02_BA/09_STATE_MACHINE_SPEC` v0.3 | **Final=kế toán sửa** · bỏ MID · 5 trường hợp đồng · ALLOCATE máy suy |
| `02_BA/Artifacts/FLS-ERD-Full-Detail` | khối hợp đồng **13→14**, `le=P` không `BL`, +ALLOCATE/AUDIT |
| `01_Orchestrator/02_VERSION_ORCHESTRATION` | `ITL-CONTRACT` v1.0, 14 trường |
| `06_SCREEN_SPEC` v1.2 · `FLS-Wireframe.html` v4 | panel 5 nhóm gồm ALLOCATE; sửa payer/payee |
| `00_MASTER_INDEX` | `QĐ-ITL-35…46`, `QĐ-owner-0820`, `AUD-12` |

### ◐→✅ Đã dán banner đính chính framing (2026-08-24)

Sáu file dưới **giữ nguyên số đo** *(bằng chứng tại thời điểm)* nhưng đã thêm **banner đính chính cách gọi tên** *(6.843 = ô cột `Final`, không phải lần gõ; `Input here` thật ≈ 5.018; `Final`=kế toán sửa; bỏ `MID`; 14 trường theo TÊN, `le`=`P`)* trỏ về §3c. Không cần viết lại thân.

| File | Đã làm |
|---|---|
| `02_BA/01_BRD` | +banner · sửa `KPI-I07` từ "13 cột `…BL`" → **14 trường `A–G,P,…`** |
| `01_Orchestrator/03_PRODUCT_LIFECYCLE` | +banner ở đầu *(IM6 giữ nguyên số, đọc kèm banner)* |
| `01_Orchestrator/08_MIGRATION_ROADMAP` · `01_PRINCIPLES` | +banner *(64 cột / ALLOCATE máy-suy · `Final`=sửa)* |
| `Artifacts/Phuong-phap-luan-…` | +banner · sửa mermaid + `D3` "13 cột theo vị trí" → **14 trường** |
| `Artifacts/Lo-trinh-Chuyen-doi-…` | +banner |

### ○ Giữ nguyên — biên bản AS-IS / lịch sử (đúng tại thời điểm, KHÔNG sửa)

`Artifacts/ERD-Full-Detail` *(bản ITL tiền-FLS)* · `Process-PM-den-ITL` · `Ket-qua-*` *(biên bản đo)* · `_GUIDE_*` *(sinh tự động)* · `Ra-soat-doc-lap-Schema-vs-Wireframe`. Các file này ghi lại **cái đã đo/đã thấy**; sửa chúng là viết lại lịch sử. Chỉ trỏ tới bản mới, không đổi nội dung.

★ **Nguyên tắc phân nhóm:** tài liệu **thiết kế TO-BE** phải khớp phát hiện mới nhất *(nhóm ✅/◐)*; tài liệu **biên bản/AS-IS** giữ nguyên *(nhóm ○)* — chúng là bằng chứng, không phải hợp đồng.

---

## §3d · Cập nhật 2026-08-25 — cú lật THỨ TỰ cấp `itl_id`

Rà lại `FLS-Process-PM-den-ITL` §3 chặng 7–8 *(theo câu hỏi owner: "mapping số chứng từ ↔ pm_id ở bước nào, itl_id tạo sau mapping?")* làm nổi một logic **các doc thiết kế đang mô tả sai theo AS-IS**: AS-IS **sinh `itl_id` SAU mapping** *(`"ITL#"&No`, `No=ROW()` trên bảng SORT theo ngày)* — TO-BE phải **cấp TRƯỚC mapping, lúc nạp**. Ba doc đã đồng bộ:

| File | Sửa |
|---|---|
| ✅ `02_BA/09_STATE_MACHINE_SPEC` v0.4 | `SM-I01`: *"sinh ITL ID"* dời `mapped` → **`staged`**; `mapped`/`unmapped` chỉ **làm giàu**, `unmapped` **không mất khoá**; +bảng cú-lật AS-IS↔TO-BE |
| ✅ `02_BA/11_INVARIANTS` v0.5 | Ghi chú `INV-I04`: bỏ câu "itl_id = composite nội dung" *(mâu thuẫn `INV-I04a`)*; +cơ chế AS-IS + 2 đường mất-ổn-định *(1.356 `FALSE`; `No` rỗng ⇒ `ITL#`)*; +ghi chú lineage `INV-I05` *(`pm_line_id`+`le_payer` sống sót vào canon)* |
| ✅ `02_BA/05_DATA_DICTIONARY_ERD` v0.6 | `DD-I05`: +bảng cú-lật thứ tự + yêu cầu lineage `pm_line_id`/`le_payer` ngoài 14 trường hợp đồng |

**Một câu tóm:** AS-IS gán danh tính *sau* khi ghép rồi vứt khoá ghép; TO-BE gán danh tính *lúc nạp* và giữ khoá ghép *(`pm_line_id`)* vĩnh viễn. *(`QĐ-ITL-20` — mang lineage vào canon — vẫn ở dạng đề xuất trong `FLS-Process` §11; đã phản ánh làm ghi chú thiết kế, chưa nâng thành QĐ trong `00_MASTER_INDEX`.)*

---

## §4 · Đường tới hạn

```
Đợt 0  →  Đợt 1  →  ┬─ Đợt 2 (kiến trúc + màn hình)
                    └─ Đợt 3 (nghiệm thu + lộ trình)
Đợt 4 chạy song song, không chặn ai
Đợt 5 làm sau, hoặc bỏ nếu Artifacts đã đủ vai
```

★ **Chặn thật chỉ có hai file**: `05_DATA_DICTIONARY_ERD` *(đóng băng 13 trường)* và `02_VERSION_ORCHESTRATION` *(bump v1.0)*. Xong hai file đó là **code được**.

⚠ **File nguy hiểm nhất nếu bỏ qua**: `06_SCREEN_SPEC`. Nó đang trắng, mà `QĐ-ITL-38` vừa biến màn hình thành **nơi kế toán làm việc**. Không có spec màn hình thì **không có gì để nghiệm thu cái quyết định rủi ro nhất của cả dự án**.

---

## §5 · Việc đo còn treo

| Việc | Trạng thái |
|---|---|
| `INV-I15` — `P` *(LE)* so với `BL` *(ENITY)*, trường thứ 13 vào P&L | ◐ **đang đo** — có `P` *(9.903 dòng)* và `E`; **`BL` trượt 3/3 lần** trên file gốc, phải chạy lại |
| Cổng `Final` — 3 khối còn lại *(`Payment Type` · `Bắt đầu DV` · `Mã đối tác`)* | ⛔ timeout 3/3. ⚠ **`Mã đối tác` nay ngoài hợp đồng** ⇒ chỉ còn **2 khối** cần đo |
| *"Bao nhiêu TIỀN đổi kỳ"* nếu sửa nợ ngày | ⛔ **HUỶ** — `AUD-12` rút lại căn cứ |

---

## Changelog

- **v0.1** (2026-08-24): Khởi tạo sau phiên rà thiết kế. **10 quyết định `QĐ-ITL-35…44`** + `AUD-12`. Lộ trình **5 đợt** theo phụ thuộc; đường tới hạn chỉ **2 file**; file nguy hiểm nhất nếu bỏ qua là **`06_SCREEN_SPEC`**.
