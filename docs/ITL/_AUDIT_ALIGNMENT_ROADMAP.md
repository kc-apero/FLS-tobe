# _AUDIT_ALIGNMENT_ROADMAP — Lộ trình audit bộ tài liệu về đúng **bốn module** của owner

**Version:** v0.10 · **Ngày:** 2026-09-17 · **Chủ sở hữu:** COO-CFO · **Loại:** kế hoạch tài liệu *(doc-only)*

> ⭐⭐⭐ **`C0` ĐÃ ĐÓNG cùng ngày** — owner trả lời cả ba câu chặn, và câu ⓵ **đổi SSOT của cuộc audit**: chuẩn ⛔ không còn là *"bốn phát biểu của owner"* mà là **bộ ERD của hệ ggsheet hiện có**. Xem **`§0b`**.

**Vì sao có bản này:** owner đọc lại bộ `BA` + `TECH` ngày 17/09 và báo **drift đáng kể so với hình dung về hệ thống**, kèm **bốn phát biểu**:

> ⓵ Hệ có các module: **nạp data → ghép lệnh chi (PM & Transaction Reference) → ITL (1/2) → ITL adjust (2/2)**
> ⓶ Nạp data gồm: **PE · PI · PM · Bank Transaction · Cash Ledger**
> ⓷ Ghép lệnh chi: màn danh sách PM, transaction, **cơ chế đề xuất**, UIUX thân thiện và hợp nghiệp vụ; **đủ các trường như trong ggsheet**
> ⓸ ITL adjust: **đủ các trường như trong ggsheet**

---

## §0 · ⭐⭐⭐ Bốn phát biểu ấy ⛔ KHÔNG phải bốn câu hỏi — chúng là bốn **CỔNG**

Mỗi câu owner viết đều **đo được**, và vì thế mỗi câu đều **gác được**. Đó là lý do lộ trình này ⛔ không dừng ở *"sửa tài liệu cho khớp"*: sửa xong mà ⛔ không có cổng thì bộ tài liệu **già lại trong im lặng** — đúng cái `doc-set-silent-drift-gate` đã ghi và đúng cái vừa xảy ra.

⛔⛔ **Bằng chứng rằng «tìm ra» ⛔ KHÔNG bằng «sửa được».** `GAP-SPEC-03` — *"lưới 52 cột" là con số chưa ai đo, thật ra `23`* — được tìm ra **03/09**, ghi vào `QĐ-ITL-81`, ghi vào `06_ORCHESTRATOR_DASHBOARD` ba chỗ. Hôm nay **17/09**, sau **14 ngày**, con số `52` **vẫn còn trong tài liệu** *(`21` lần)*. ⇒ ⛔ Một phát hiện ⛔ không tự đi sửa; chỉ **cổng** mới làm việc đó.

---

## §0b · ⭐⭐⭐ BA CÂU CHẶN ĐÃ CÓ TRẢ LỜI *(owner, 17/09)* — và câu ⓵ **đổi chuẩn của cả cuộc audit**

| # | Owner trả lời | Hệ quả |
|--:|---|---|
| `Q1` | **⛔ KHÔNG** — *"tôi muốn thiết kế **bám sát bộ ERD của hệ thống ggsheet hiện có**, trong đó có **bước** ITL (1/2)"* | ⭐⭐ **SSOT của audit đổi**: chuẩn ⛔ không phải bốn phát biểu, mà là **bộ ERD ggsheet**. «ITL (1/2)» là **BƯỚC** trong ERD ấy, ⛔ không phải module thứ tư ⇒ trục `khau` **`3` giữ nguyên**, ⛔ không khai lại `23/23` |
| `Q2` | **Đi nhờ `PM_Unpivot`**, ⛔ nhưng **`PE` · `PI` · `PM` là các entity KHÁC NHAU** | `LAN` giữ **`3`** *(đường vào)*; **Đường vào ≠ thực thể** — đây là hai thứ bộ tài liệu đang trộn. ⛔⛔ **VẾ SAU BỊ LẬT TRONG CÙNG NGÀY — giữ làm bia, ⛔ không xoá.** Nguyên văn đã bỏ: ~~*«ERD phải có 3 thực thể ⇒ ⛔ không được gộp `PE`/`PI` vào `fls_pm_line`»*~~. Chiều `17/09` owner chốt tiếp: *«`PE`/`PI` **cột có kiểu** trong `fls_pm_line`, chưa cần làm bảng riêng»* ⇒ migration `0023`, **5 cột**, phép **`B3` ✅**. ⭐ Hai câu ⛔ **không** mâu thuẫn về **nguyên tắc** *(`PE`·`PI`·`PM` vẫn là **ba thực thể**)* — chúng khác ở **cách hiện thực**: ba thực thể ⛔ **không** bắt buộc thành ba **bảng**. ⚠ Nhưng câu cũ **đọc như một lệnh cấm**, và một lệnh cấm bị lật mà ⛔ không ai đánh dấu là chỗ người sau sẽ **dựng lại hai bảng thừa** |
| `Q3` | Tệp ở `AS-IS system/Accounting_Files/RAW`; **trước mắt chỉ cần data sample**, chưa migrate toàn bộ | Mẫu số đo được **offline**, ⛔ không cần sheet sống — trừ đúng một chỗ, xem `⛔` cuối mục này |

### Tên module của owner **chính là tên tệp**

```
ITL I Input Transaction Ledger File 1_2 (RAW).xlsx        ⇒ «ITL (1/2)»
ITL I Input Transaction Ledger File 2_2 (ADJUSTED).xlsx   ⇒ «ITL adjust (2/2)»
```

Owner ⛔ không đặt ra hai cái tên mới — owner **đọc tên hệ đang chạy**.

> ⛔⛔⛔ **CÂU CŨ Ở ĐÂY SAI, và cổng `C1` bắt được nó trong vài phút — xem `§0d`.**
> Nguyên văn đã bỏ: ~~*"Bộ tài liệu ⛔ chưa bao giờ đọc TÊN TỆP như một lời khai"*~~.
> Đo được: `BA-05` dòng **39** và **130** khai **đúng cả hai tên tệp**, kèm tab và số hàng tiêu đề. ⇒ Phần còn lại của `D1` **⛔ không phải** *"tài liệu không biết tên tệp"* mà hẹp hơn: **tên tệp được khai làm NGUỒN, ⛔ chưa bao giờ làm DANH TÍNH của khâu** — và `09_MILESTONES_**HAI_TAC_VU**.md` vẫn mang con số `HAI` ngay trong tên *(phép `T3`)*.

### Năm tệp nguồn — kiểm kê

| Tệp | Tab | Vai trò |
|---|--:|---|
| `ITL … File 1_2 (RAW)` | **16** | ⭐ ERD của **nạp + ghép + ITL(1/2)** |
| `ITL … File 2_2 (ADJUSTED)` | **12** | ⭐ ERD của **ITL adjust (2/2)** |
| `AperoGroup_Payment` | **136** | nguồn `PE→PI→PM→PC` |
| `P100 _ Bank Transactions` | **66** *(60 tab `R \|`)* | lằn `Bank` |
| `P100 _ Cash Ledger` | **25** | lằn `Cash` |

### ⭐⭐⭐ MẪU SỐ — đo được, lần đầu

**`Transaction Mapping L1`** *(tiêu đề **hàng 3**)* — **`38` vị trí · `36` có tên**.

⇒ ⭐ **Khớp CHÍNH XÁC khuôn canon của FLS** *(`fls/canon/spec.py`: "38 VI TRI (A..AL), 36 TRUONG", hai cột trống `Z`/`AA`)*. ⇒ Con số `38`/`36` **⛔ không phải phát minh của FLS** — nó là **hình dạng của sổ thật**, và nó **đúng**. *(Cũng là chỗ agent rà soát độc lập đã báo sai — xem `BA-05 §DD-I11 §E`.)*

**`ITL Ledge`** *(tiêu đề cho NGƯỜI ở **hàng 7**, ⛔ không phải hàng 1)* — **`69` vị trí**, và nó có **BỐN VÙNG**:

| Hàng | Nó là gì |
|--:|---|
| `1` | ⭐ **tên VÙNG** — `ADJUSTMENT ZONE` *(`R`)* · `ALLOCATE ZONE` *(`AU`)* · `AUDIT ZONE` *(`AX`)*, kèm **PIC** từng dải |
| `2` | ⭐⭐ **sổ TỰ KHAI NGUỒN**: `File = ITL … File 1/2` · `Sheet = Transaction Mapping L1` |
| `3` | `# Input here` **`297·179·1210·22·22·1624·3489`** ⇒ **`6.843`** |
| `5` | **chữ cái tham chiếu NGƯỢC** về `L1` — `A..H · S · T · AB · AC · Y · AD · AE · AG · AL` = **`17`** cột kéo sang |
| `7` | tiêu đề người: `17` cột kéo sang · `R` = **`ITL ID`** · **`7` dải ADJUSTMENT** · `2` ô ALLOCATE · `8` ô AUDIT |

> ⛔⛔⛔ **CÂU DẪN CŨ Ở ĐÂY SAI — xem `§0d`.** Nguyên văn đã bỏ: ~~*"Ba điều bộ tài liệu đang nói mà **chưa ai nối được về nguồn**"*~~. Sự thật: **`BA-05 §DD-I04` đã khai TRỌN cấu trúc này** — từng hàng `1`→`8` và `10+`, ba vùng, *"7 khối"*, hàng `5` là **hàng ánh xạ cột nguồn**, hàng `7` là **tên cột thật**, kèm cả bảng `A`–`Q` ánh xạ về `L1`. Nó còn khai **hàng `8`** *(tên cột con của các khối 4 cột)* mà tôi ⛔ **không hề nhắc**. ⇒ Ba mục dưới đây là **XÁC NHẬN LẠI**, ⛔ không phải phát hiện.

⭐ **Ba điều nay được xác nhận từ nguồn** *(và `BA-05 §DD-I04` đã khai trước)*:
- **«sửa `7` trường»** *(`QĐ-ITL-64`)* — ⭐ **ĐÚNG, và nó đến từ đây**: `ADJUSTMENT ZONE` có đúng **`7` dải** *(`Budget Code` · `Loại giao dịch` · `Chủ dự toán (CDT1)` · `TĐ bắt đầu` · `TĐ kết thúc` · `Mã đối tác` · `File đính kèm: Hoá đơn`)*.
- **`6.843` ô *"Input here"*** — tổng của **`7` bộ đếm** ở hàng `3`, **mỗi dải một bộ**. ⇒ con số ấy ⛔ không phải một phép đếm của FLS; **chính sổ tự đếm**, và nó đếm **số lần đã dùng mặc định**.
- ⛔⛔ **`CR#8` nói ba trường *"⛔ không có ở đâu cả"* — SAI khi đo trên AS-IS.** `cdt1_cfa1`/`cdt1_cfa2` **có nhà**: `AU`/`AV` = `Chủ dự toán (CDT1) CFA1`/`CFA2`, tức **`ALLOCATE ZONE`**; `alloc_method` cũng có: `Mapping Master` cột `K`/`L` = `Need to Allocate to CFA2` / `Method to Allocate to CFA2`. ⇒ Câu của `CR#8` đúng về **bề mặt đã khai của FLS** *(`38` canon + `14` hợp đồng)*, ⛔ **sai** về **hệ đang chạy** — và từ `Q1` thì **hệ đang chạy mới là chuẩn**.

### ⛔⛔ MỘT CHỖ SAMPLE ⛔ KHÔNG TRẢ LỜI ĐƯỢC — và phải nói thẳng

| Tab | Vị trí | Tiêu đề đọc được |
|---|--:|---|
| `ImportrangePE_Unpivot` | 26 | ⛔ **`#REF!`** |
| `ImportrangePI_Unpivot` | 26 | ⛔ **`#REF!`** |
| `ImportrangePM_Unpivot` | **29** | ⛔ **`#REF!`** |
| `ImportrangePC11_Entry Data` | 23 | ⛔ **`#REF!`** |

Bản `.xlsx` xuất offline **⛔ không mang theo `Importrange`** ⇒ **bề rộng còn, TÊN CỘT mất**. Và đây là **đúng ba thực thể `Q2` vừa chốt**, cũng là **nơi duy nhất** trong cả `5` tệp có chúng.

⇒ ⭐ **Mẫu số của ⓸ *(adjust)* đã có: `69`. Mẫu số của ⓷ *(ghép)* thì CHƯA** — ta biết FLS đọc **`8`** cột và `PM_Unpivot` rộng **`29`** vị trí, ⛔ nhưng ⛔ không biết **`29` cột ấy TÊN gì**. Cần **một** trong hai: ⓐ một bản xuất `PM_Unpivot` *(có giá trị, ⛔ không cần đủ dòng — sample là đủ)*, hoặc ⓑ đọc qua **cửa sống** của FLS.

> ✅ **ĐÃ GIẢI cùng ngày bằng đường ⓐ** — owner tải `A _ PAY100 _ PM11 Entry Data`, xem **`§0c`**. ⛔ Mục này giữ nguyên làm **bia**: bốn tab `Importrange*` **vẫn** ra `#REF!` trong bản `File 1_2`, nên ai đọc lại tệp ấy sẽ gặp lại đúng chỗ tắc này.

⚠ **Và một ranh giới phải giữ suốt cuộc audit:** bản `.xlsx` offline dùng được để đọc **HÌNH DẠNG** *(tên cột, thứ tự, vùng)*, ⛔ **không** dùng để đọc **GIÁ TRỊ** — đã chứng minh nó **phá huỷ ngày** *(chỉ còn `2,7%` đúng)*. Mọi con số tiền/ngày vẫn phải đo trên **kho** hoặc **nguồn sống**.

---

## §0c · ⭐⭐⭐ `M1` ĐÓNG — owner tải `A _ PAY100 _ PM11 Entry Data`, ba thực thể **đo được hết**

Tệp có **9 tab**, và trong đó có đủ **`PE_Unpivot` · `PI_Unpivot` · `PM_Unpivot`** — ⭐ đúng ba thực thể `Q2` chốt, lần này **có giá trị**, ⛔ không `#REF!`.

✅ **Tệp an toàn:** `.gitignore:13` phủ cả `AS-IS system/Accounting_Files/RAW/`, và nó **chưa vào index**. ⚠ Nó mang `Email Address` · `Tên tài khoản` · `Số tài khoản` ⇒ ⛔ **đừng gỡ dòng ignore ấy**.

### Mẫu số — ba thực thể

| Thực thể | Tiêu đề ở hàng | Vị trí | **Có tên** | Sample |
|---|--:|--:|--:|--:|
| `PE_Unpivot` | 2 | 27 | **23** | ~3.130 dòng |
| `PI_Unpivot` | 2 | 26 | **24** | ~4.010 dòng |
| ⭐ `PM_Unpivot` | **2** | 29 | **28** | ~3.773 dòng |
| `PM11_Entry Data` | 2 | 30 | 30 | ~16.535 dòng *(khác hạt — sổ nhập)* |

### ⭐⭐ Hợp đồng `PM_COT` của FLS: **`8/8` KHỚP**

Lần đầu `PM_TIEU_DE_MONG_DOI` được so với một bản **ngoài kho** — cả 8 vị trí *(`cur` `tien` `slip` `line` `hd` `cdt1` `status` `ref`)* trùng **từng ký tự**, và hàng tiêu đề đúng là **hàng 2** như `PM_DONG_TIEU_DE` khai. ⇒ Đường nạp PM **⛔ không đọc lệch một cột nào**.

### ⭐⭐⭐ Và bức tranh đảo chiều: **`tho` đã giữ `27/28` trường**

| Đo | Kết quả |
|---|--:|
| Khoá khác nhau trong `fls_pm_line.tho` | **27** |
| `PM_Unpivot` có tên | **28** |
| Thiếu đúng một | ⛔ **`Email Address`** |
| Dòng có `tho` | **26.404 / 79.212** *(33%)* |

⇒ ⭐ **`PM_COT_RIENG_TU` hoạt động đúng như khai** — bản cấm ⛔ không vào kho, đo được.
⇒ ⭐⭐ **«Đủ trường như ggsheet» ⛔ KHÔNG phải bài toán NẠP — dữ liệu đã ở trong kho.** Nó là bài toán **ĐẶT KIỂU + BÀY RA**, cộng một phép **nạp bù** cho `52.808` dòng cũ *(có trước `tho`, thêm 11/09)*.

### ⭐⭐⭐ Quan hệ `PE`/`PI`/`PM` — phân hoạch **TUYỆT ĐỐI**, `0` ngoại lệ

| Dòng PM có cha là | Số dòng |
|---|--:|
| **chỉ `PI`** | **22.904** *(86,7%)* |
| **chỉ `PE`** | **3.500** *(13,3%)* |
| cả hai | ⭐ **0** |
| ⛔ không cha | ⭐ **0** |

⇒ **Một dòng lệnh chi có ĐÚNG MỘT cha, hoặc `PI` hoặc `PE`** — đo trên `26.404` dòng, ⛔ không một ngoại lệ. ⭐ Đây là một **bất biến ứng viên** sẵn sàng thành `CHECK`, và bộ schema hiện chỉ có **`1` CHECK** cho cả `18` bảng.

### `20` trường FLS **chưa đặt kiểu** — owner quyết theo NHÓM, ⛔ không theo từng dòng

| Nhóm | Trường |
|---|---|
| ⭐⭐ **Khoá `PE`/`PI`** *(7)* — **chính là câu ⓶ của bạn** | `ID PELine - Nội dung PE (Advance)` · `(Urgent)` · `ID PILine - Nội dung PI` · `ID PESlip` · `ID PELine` · `ID PISlip` · `ID PILine` |
| **Nhận dạng khoản tiền** *(6)* | `Nội dung giao dịch nhập khi lập lệnh ở bank` · `Ngân hàng` · `Chi nhánh` · `Số tài khoản` · `Tên tài khoản` · `Ghi chú (nếu có)` |
| **Đối soát pháp nhân** *(1)* | `Pháp nhân thanh toán` ⇒ đúng cái `06_SCREEN_SPEC §3` gọi là *"đối soát LE-vs-pháp-nhân-trả"* |
| **Phân loại** *(2)* | `Loại giao dịch (Payment Type)` · `Chủ dự toán *` |
| **Vết & kiểm** *(4)* | `Timestamp` · `Status_Log` · `Check trùng ID PMLine` · ⛔ `Email Address` **giữ nguyên CẤM** |

### ⛔⛔ Một phép đo của tôi HỎNG, và nó lộ ra chỗ nặng hơn

Tôi đã thử nối *"cơ chế đề xuất"*: `Nội dung giao dịch nhập khi lập lệnh ở bank` là chuỗi **người gõ vào bank khi lập lệnh** ⇒ lẽ ra nó **quay về** trong `Diễn giải` của sao kê. Phép so ra **`0` khớp**, và tôi suýt kết luận *"⛔ không phải khoá ghép"*.

⛔ **Sai.** `fls_itl.memo` **NULL trên `8.387/8.387`** ⇒ phép so **xanh trên tập rỗng**. Trạng thái thật của sổ:

| Trường | Có giá trị |
|---|--:|
| `doc_date` · `curr` | **8.387** *(100%)* |
| `doc_no` | 8.383 |
| `ps_co` · `ps_no` | 7.558 · 4.520 |
| ⛔ `memo` · `acct` · `le` | ⭐ **0** |

⇒ ⭐⭐ **`Diễn giải` — tín hiệu ghép GIÀU NHẤT của sao kê, cột `C` của canon — ⛔ KHÔNG có trong kho.** Mọi cơ chế đề xuất dựa trên diễn giải hiện **⛔ không đo được**, ⛔ không phải *"đã thử và không hiệu quả"*.

⭐ Còn phía PM thì tín hiệu **có thật**: **`5.901 / 26.404` = `22,3%`** dòng mang mã dạng `PI…`/`PE…` ngay trong nội dung bank *(ví dụ `TT CP teabreak 202412 **PI00108**`)*. ⇒ Đây là nửa còn thiếu của **`US-KT-037`** *(«mã lệnh trong diễn giải», mở từ 27/08)*, và nửa kia **chặn ở `memo` rỗng**.

---

## §0d · ⛔⛔⛔ CỔNG `C1` BẮT MỘT CÂU SAI CỦA CHÍNH TÔI — trong vài phút sau khi nó được dựng

Phép `T2` khai `mong=LỆCH` kèm câu *"bộ tài liệu ⛔ chưa bao giờ đọc TÊN TỆP như một lời khai"*. Cổng chạy ra **KHỚP** ⇒ **đổi trạng thái** ⇒ **NO**. Truy ra: **câu của tôi sai**, ⛔ không phải cổng sai.

### Ba chỗ tôi báo là *phát hiện* mà bộ tài liệu **đã có**

| Tôi viết | Sự thật đo được |
|---|---|
| *"tài liệu chưa bao giờ đọc tên tệp"* | `BA-05:39` + `BA-05:130` khai **đúng cả hai tên tệp**, kèm tab và hàng tiêu đề |
| *"cấu trúc 4 vùng của `ITL Ledge` chưa ai nối được về nguồn"* | `BA-05 §DD-I04` khai **từng hàng `1`→`8` và `10+`**, ba vùng, *"`7` khối × `4` cột"*, khuôn `Classifying → Manual input → MID → Final` — **chi tiết hơn tôi** |
| *"`6.843` là con số sổ tự đếm"* | Đúng, ⛔ nhưng ⛔ không mới: `QĐ-ITL-05` **18/08** đã có, và còn đi xa hơn — `6.843` chỉ là **31%** của **22.360** ô nhập tay toàn hệ |

### ⭐⭐⭐ Cái còn lại **thật sự mới** — và nó vẫn đáng

| # | Đo được lần đầu |
|--:|---|
| ① | `PE_Unpivot` **27/23** · `PI_Unpivot` **26/24** — ⛔ chưa tệp nào ghi. ⚠ ⛔ **Nhưng `PM` thì KHÔNG mới**: `FLS-Process-PM-den-ITL.md:186` đã ghi *«dải `!A1:AB` (**28 cột**)»*, và `pm_join.py:192` cũng vậy. ⇒ **Lần thứ ba tôi nhận nhầm công trong một buổi** — xem cảnh báo cuối mục |
| ② | `PM_COT` **khớp `8/8`** với một bản **ngoài kho** — `BA-05` **khai**, phép này **kiểm** |
| ③ | `tho` giữ **27/28** trên **26.404/79.212** dòng |
| ④ | `PE`/`PI` **phân hoạch tuyệt đối** — `22.904`/`3.500`, **`0`** ngoại lệ |
| ⑤ | `fls_itl.memo` **`0`/8.387** — và phép đo hỏng đã lộ ra nó |
| ⑥ | `ITL Ledge` bề rộng **`69`** |

### ⭐⭐ Bài học — và nó **về phương pháp của tôi**, ⛔ không về bộ tài liệu

> Tôi đo **nguồn** rất kỹ, rồi **grep** tài liệu tìm **mẫu lệch** *(đếm `"52 cột"`, đếm `"đề xuất"`)* — ⛔ nhưng **⛔ không ĐỌC** đúng mục tài liệu nói về **cùng một vật**.

⇒ Kết quả: tôi tưởng mình bù một lỗ hổng, thật ra đang **viết lại một mục đã có, kém hơn bản gốc**.

⛔⛔⛔ **Và nó lặp lại LẦN THỨ BA trong cùng buổi** *(`PM_Unpivot` 28 cột — đã có ở `FLS-Process-PM-den-ITL.md:186` và `pm_join.py:192`)*. ⇒ Luật cho mọi câu *«⛔ chưa ai ghi X»* trong tệp này: **grep cả `docs/` LẪN `fls/`+`tools/` trước khi viết**, vì một sự thật đã đo có thể sống trong **chú thích mã** thay vì trong tài liệu — và ở repo này, chú thích mã **thường là nơi nó sống**. Đây đúng lớp `measure-old-system-before-declaring-new`, chỉ đổi chỗ: lần này thứ tôi quên đo **chính là bộ tài liệu đang audit**.

⛔⛔ **Hệ quả cho kết luận của `v0.1`: `D4` phải đọc lại.** `BA-05` **⛔ không** drift về cấu trúc AS-IS — nó là một trong những mục **bám nguồn chắc nhất** của cả bộ. Cái drift thật của `D4` hẹp hơn: **năm con số cùng mô tả một vật vẫn lưu hành**, và `52` — **đã bị bác từ 03/09** — vẫn còn.

⭐ **Và đây là lý lẽ mạnh nhất cho `C4`**, mạnh hơn mọi câu tôi viết ở `§0`: cổng vừa dựng đã **bắt tác giả của chính nó**, ở lượt chạy **đầu tiên**.

---

## §0e · ⛔⛔⛔ `D4` PHẢI VIẾT LẠI — **hai con số tôi gọi là lệch thì CHÍNH TÔI đo sai**

Vào `C3` *(sửa tài liệu)*, việc đầu là đọc `19` chỗ ghi `"52 cột"` để tách **tệp KHAI** khỏi **tệp CHÉP**. Đọc xong thì cả hai cáo buộc của `v0.1` đổ.

### ⓵ `64` **ĐÚNG** — `69` của tôi là phép đo quá thô

| Đo | |
|---|--:|
| bề rộng hàng `ITL Ledge` | 69 |
| ⭐ **cột CÓ TÊN** *(hàng `7` **+ hàng `8`**)* | **64** |
| cột có dữ liệu | 62 |

⇒ `64` đếm **cột có tên**; `69` của tôi đếm cả **đuôi rỗng**. ⛔ Và hàng `8` — thứ tôi bỏ sót, `BA-05 §DD-I04` **đã khai** — chính là nửa còn lại của con số. **Tài liệu đúng, tôi sai.**

### ⓶ `52` **ĐÚNG** — `GAP-SPEC-03` là **ảnh chụp của 03/09**

```
len(fls/api/cot_so.BANG_COT) = 52     ⇐ đo thẳng ở mã, 17/09
```

Ngày `03/09` lưới thật có `23` cột và `GAP-SPEC-03` **đúng lúc ấy**. Sau đó **`CANON_LEN_LUOI` lên lưới** ⇒ `52`. ⇒ **GAP mô tả một tình trạng ⛔ không còn**, và ⛔ không cổng nào thấy vì cổng canh **số**, ⛔ không canh **tuổi của một câu trạng thái**.

### ⭐⭐⭐ Chỗ sai THẬT — và nó hẹp, chính xác, và đẹp

| | Cách cộng |
|---|---|
| ⛔ `BA-06` khai | `38` canon + `14` hợp đồng |
| ⭐ Đo ở mã | **`24` nền + `28` vị trí canon** |

> **Cả hai đều ra `52`.** Đó là lý do ⛔ không ai bắt được trong **20 ngày**: cổng nào canh **tổng** cũng xanh.

⇒ Lưới **⛔ không** lấy cả `38` vị trí canon — nó **cố ý bỏ `9`** *(`A·B·C·D·E·F·G·L·AG`)* vì chúng **đã là cột nền**, lý do có sẵn trong `cot_so.py`. Và **⛔ không có** khối *"14 cột hợp đồng"* nào trên lưới. ✅ **Đã sửa `06_SCREEN_SPEC §6`**, phép `C7` nay canh chỗ ấy.

### ⛔ `18/19` chỗ ghi `52` là **BIÊN BẢN** — xoá chúng là **viết lại lịch sử**

Sổ quyết định *(`QĐ-ITL-66`·`81`, `CR#7`·`8`)* · changelog · mô tả `GAP` · và các câu về **NGUYÊN MẪU** `748 × 52 = 38.896` ô *(một phép đo có thật của `tools/mui_thu_luoi.py`)*. Ở đó **số cũ là ĐÚNG**. Chỗ thứ `19` — `06_SCREEN_SPEC §6` — là câu nói về **hiện tại**, và đó là chỗ duy nhất phải sửa.

### ⭐⭐⭐ Luật rút ra — và nó **cắn hai lần trong một giờ**

> **Phép ĐẾM CHỮ ⛔ KHÔNG phân biệt được tài liệu đang KHAI với tài liệu đang GHI LẠI.**

Phép `C4` của tôi đếm `"52 cột"` và đòi `= 0`. Sửa xong, tôi viết `C7` đếm `"38 cột canon"` và đòi `= 0` — **lệch mãi**, vì chính **câu đính chính** phải trích lại chuỗi sai để nói *"chỗ này từng ghi thế"*. ⇒ **Lặp lại đúng lớp lỗi vừa học, trong cùng một giờ.**

⭐ **Chữa, hai bước:**
- ⓐ **so HAI NGUỒN**, ⛔ đừng đếm chữ — đúng khuôn **cổng chung `#13`**;
- ⓑ hỏi *"**câu ĐÚNG có chưa**"* **⛔ không** hỏi *"chuỗi sai còn không"*. Bằng chứng **dương** ⛔ không bị biên bản làm nhiễu; bằng chứng **âm** thì bị.

⇒ ⛔⛔ **`D4` viết lại:** ⛔ **không** phải *"năm con số cho một vật"*. Mỗi con số đếm **một vật khác nhau** và **phần lớn đều đúng** — `38`/`36` khuôn canon · `52` lưới `F02` · `64` cột có tên `ITL Ledge` · `23` lưới **ngày 03/09**. Cái thiếu là: **⛔ không chỗ nào nói NÓ ĐẾM GÌ** — đúng bài `một con số in ra phải nói nó đếm gì, ngay tại chỗ in`. Đó là `G-MOD-4`, và nay nó có **lý lẽ đo được**.

---

## §1 · ĐO TRƯỚC KHI KHAI — bốn chỗ lệch, đo hôm nay trên **kho THẬT** và **mã nguồn**

> ⛔ Lộ trình dựng trên phỏng đoán thì chính nó là lớp drift kế tiếp. Mọi số dưới đây đo ngày **17/09**, ⛔ không chép lại từ tài liệu.

### `D1` · Số KHÂU — tài liệu nói **BA**, owner nói **BỐN**

| Nguồn | Nói gì |
|---|---|
| `01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md` *(v1.12, owner chốt 09/09)* | **mốc `A`** *(đường LẤY dữ liệu)* · **tác vụ ①** *(mapping)* · **tác vụ ②** *(adjust)* ⇒ **3** |
| `fls/db/schema.py` · trục `khau` *(khai 16/09)* | `A-nap` · `B-ghep` · `C-sua` + `S-so`/`V-viec`/`H-ha-tang` ⇒ **3 khâu chuỗi** |
| ⭐ **owner 17/09** | nạp · ghép · **ITL (1/2)** · **ITL adjust (2/2)** ⇒ **4** |

⛔⛔ **Chỗ lệch có TÊN: module «ITL (1/2)» — bước DỰNG SỔ — ⛔ không có tên ở đâu cả.** Bộ tài liệu coi việc sinh `itl_id` là một **chặng kỹ thuật** nằm bên trong đường nạp *(`S3` của `02_PROCESS_FLOW`)*; trục `khau` tôi khai hôm qua đẩy `fls_itl` vào **`S-so`** — *"trục chung, cả ba khâu đều chạm"* — tức cũng ⛔ **không cho nó một khâu**.

⇒ Đây là drift **sâu nhất**, vì nó nằm ở **xương sống**: số `HAI` nằm ngay trong **TÊN TỆP** `09_MILESTONES_HAI_TAC_VU.md`, và trục `khau` đã khai lên **23/23** đối tượng.

### `D2` · Lằn NẠP — máy khai **BA**, owner nói **NĂM**

```
fls/repo/chup.py:69 →  LAN = ("Bank", "Cash", "PM")
```

| Đo | Kết quả |
|---|---|
| `fls_source.src_type` | `Bank` **65** · `Cash` **8** · `PM` **1** · `Mapping` **1** |
| `fls_chup.lan` *(ảnh đã chụp)* | `Bank` **24** · `PM` **24** · ⛔ `Cash` **0** |
| `PE` · `PI` là một lằn nạp? | ⛔ **KHÔNG**. Trong toàn bộ `73` tệp, `PE`/`PI` chỉ xuất hiện như **cột tra cứu** đi nhờ `[Importrange]PM_Unpivot` *(cột `I`/`J`/`K` — `ID PELine` · `ID PILine`)*, ⛔ chưa một dòng nào khai chúng là **nguồn có đường vào** |

⇒ Hai lệch con, và chúng **⛔ không cùng loại**:
- ⓐ **`PE`/`PI` ⛔ không tồn tại như lằn** — cần owner nói rõ: nạp **thẳng từ P100**, hay tiếp tục **đi nhờ** `PM_Unpivot`? Hai câu trả lời ra hai schema khác nhau.
- ⓑ **`Cash` khai rồi nhưng ⛔ CHƯA CHỤP LẦN NÀO** — `0` ảnh. Tài liệu ghi *"⛔ chưa mở"* ở `09 §1`, nên chỗ này tài liệu **đúng**; cái sai là nó ⛔ không nói rằng một lằn khai-mà-rỗng sẽ làm **mọi cổng độ phủ xanh giả**.

### `D3` · Màn GHÉP — **cơ chế đề xuất ⛔ vắng mặt ở đúng tệp chuyên trách**

| Tệp | Số lần nói *"đề xuất"* / *"gợi ý"* |
|---|--:|
| ⛔ `02_BA/12_BA_MAN_GHEP_PM.md` — **tệp BA viết riêng cho màn này** | **0** |
| `02_BA/06_SCREEN_SPEC.md` | 15 |
| `02_BA/13_THUYET_MINH_MAN_HINH.md` | 1 |

⇒ Cơ chế đề xuất **có sống**, nhưng nó sống ở `SCR-F01` như một *drawer gợi ý* *(`QĐ-ITL-48`)* — ⛔ **không** ở tệp mà người sau sẽ mở khi hỏi *"màn ghép được đặc tả ở đâu"*.

**Và chuyện trường:**

```
fls/adapters/pm_join.py:61 →  PM_COT = {cur, tien, slip, line, hd, cdt1, status, ref}   ⇒ 8 cột
```

`12_BA_MAN_GHEP_PM.md §3` đã tự khai đúng chỗ đau — tiêu đề nguyên văn: *"Điểm ③ — FLS đọc **8 cột**, và ⛔ không giữ lại gì để bù"*. Owner đòi **đủ các trường như trong ggsheet**.

⛔⛔ **Nhưng MẪU SỐ ⛔ CHƯA AI ĐO:** ⛔ không một tệp nào trong `73` tệp ghi *`PM_Unpivot` có bao nhiêu cột*. ⇒ Phát biểu ⓷ hiện **⛔ không audit được** — ⛔ không phải vì khó, mà vì **thiếu một phép đếm chưa ai chạy**.

### `D4` · ITL ADJUST — **năm con số cho một vật**, và module có **`0` dòng**

| Con số | Nó mô tả vật nào | Nguồn |
|--:|---|---|
| **23** | cột **lưới** `F02` trả về thật | `fls/api/cot_so.py` |
| **38** | **vị trí** khuôn canon *(`A`..`AL`)*, trong đó **36** có tên | `fls/canon/spec.py` |
| ⛔ **52** | **đã bị chứng minh SAI 03/09** — vẫn còn **21** lần trong tài liệu | `GAP-SPEC-03` |
| **55** | `38` canon + `14` hợp đồng + `3` trường ⛔ không có nhà | `CR#8` |
| **64** | *"output cuối — ITL adjust như trong Excel"* | `09_MILESTONES` §0 |

| Bảng của khâu adjust | Số dòng trong kho |
|---|--:|
| `fls_adjustment` | ⛔ **0** |
| `fls_journal` | ⛔ **0** |

⇒ ⭐⭐ **Module mà owner gọi là ĐẦU RA CUỐI CÙNG ⛔ chưa chạy một lần nào.** Mọi câu *"đủ trường"* về nó hiện là **phát biểu về bản vẽ**, ⛔ không phải về hệ đang chạy. Và như `D3`, **mẫu số ⛔ chưa ai đo**: ⛔ không tệp nào ghi *sổ `ITL Ledge` sống có bao nhiêu cột* — con số `64` đến từ **ước lượng trên tài liệu AS-IS**, và `CR#7` đã một lần bị đo lật vì đúng thói quen ấy.

### Diện tích phải rà — đo bằng số tệp bị chạm

| Khâu | Số tệp `.md` có nhắc |
|---|--:|
| ghép lệnh chi | **54** / 73 |
| nạp data | **51** / 73 |
| ITL *(sinh `itl_id`)* | **47** / 73 |
| adjust | **40** / 73 |

⛔⛔ **Đừng đọc bảng này thành «phải sửa 54 tệp».** Nó nói điều khác và quan trọng hơn: **⛔ không có tệp nào là biên giới** — mỗi khâu rải trên ~2/3 bộ tài liệu. ⇒ Sửa tay từng tệp là **cầm chắc drift lần sau**. Chặng `C3` xử đúng chỗ này.

---

## §1b · ⭐⭐⭐ BẢNG ĐỐI CHIẾU GỐC — `C1`, **sinh bằng máy**

> `python docs/ITL/_tools/khop_owner.py` *(thêm `--kiem` để chỉ kiểm — cổng CI)*
>
> ⭐ **Bốn cột:** *phát biểu* · **CHUẨN** *(đo từ ERD ggsheet)* · **tài liệu** nói gì · **mã nguồn** nói gì · **kho** nói gì. Ba cột sau đọc **thẳng từ nguồn**, ⛔ không một ô nào gõ tay — vì một bảng gõ tay **chính là thứ vừa drift**.
>
> ⛔⛔ **Cổng NO khi kết quả KHÁC `mong` — cả hai chiều.** Sửa được một chỗ ⇒ **ĐỎ**, buộc người sửa **ghi lại** vào bản khai. Một chỗ đang khớp bị vỡ ⇒ **ĐỎ** ngay. Một cổng chỉ báo *"có lệch"* thì nó **xanh mãi mãi** và ⛔ không ai biết khi nào có gì đổi.

<!-- SINH-KHOP:BAT-DAU -->

| # | Khâu | Phát biểu | CHUẨN *(ERD ggsheet)* | Tài liệu | Mã nguồn | Kho | |
|---|---|---|---|---|---|---|:--:|
| `T1` | truc | So khau chuoi cua he | `3` — owner `Q1` | — | 3 khau chuoi: A-nap, B-ghep, C-sua | — | ✅ |
| `T2` | truc | Tai lieu KHAI ten tep AS-IS *(⭐ cong bat mot cau SAI cua toi — `BA-05` dong 39 + 130 khai du)* | `File 1_2` · `File 2_2` | tep KHAI ten tep AS-IS (⛔ tru lo trinh): co | — | — | ✅ |
| `T3` | truc | ⭐ TU DIEN TEN — moi khau co ten o CA BA xuat xu *(⭐ owner chot 17/09: ten CHUAN la ten TAC VU ⇒ ⛔ KHONG doi ten tep)* | `3`/3 xuat xu | bang tu dien CO trong tai lieu | 12 ten · du ca 3 xuat xu | — | ✅ |
| `A1` | Ⓐ nap | So duong vao nap | `3` | — | `chup.LAN` = 3 (Bank, Cash, PM) | 3 loai nguon | ✅ |
| `A2` | Ⓐ nap | Lan `Cash` da co anh chup *(lan khai ma RONG ⇒ moi cong do phu xanh gia)* | `>=1` | — | `Cash` co trong `LAN` | 0 anh chup lan `Cash` | ⛔ |
| `B1` | Ⓑ ghep | ⭐ `G-MOD-3` — ⛔ KHONG cot nao ROI khoi ba ro *(nguon them cot ⇒ DO cho den khi co nguoi phan loai + ghi ly do)* | `0` cot roi | — | 14 dat kieu + 1 cam + 13 khai-chua-dat = 28 | vu tru 28 cot · **0 cot roi khoi moi ro** | ✅ |
| `B6` | Ⓑ ghep | Da DAT KIEU du truong `PM_Unpivot` chua *(⛔ tach khoi `B1`: het lo im lang ⛔ KHONG nghia la du truong)* | `28`/28 | — | 14/28 cot nguon da doc co kieu | 13 cot con nam trong `tho`, chua co kieu | ⛔ |
| `B2` | Ⓑ ghep | Hop dong tieu de PM khop AS-IS | `8` | — | 14/14 vi tri khop AS-IS tung ky tu | — | ✅ |
| `B3` | Ⓑ ghep | `PE`/`PI` co COT CO KIEU trong `fls_pm_line` *(⭐ owner chot 17/09 — chua can bang rieng; migration `0023`)* | `5` cot | — | 5/5 cot co kieu (pe_line, pe_loai, pe_slip, pi_line, pi_slip) | moi dong anh PM hieu luc co cha PE hoac PI | ✅ |
| `B4` | Ⓑ ghep | Dong lenh chi co DUNG MOT cha `PE\|PI` *(bat bien ung vien ⇒ `CHECK`)* | `0` ngoai le | — | ⛔ ⛔ khong CHECK nao canh | 0 ngoai le trong anh PM hieu luc | ✅ |
| `B5` | Ⓑ ghep | Tep BA man ghep dac ta co che DE XUAT *(⭐ neo lai 01/10: `BA-06` (⛔ `12` — BIA tu 18/09, `R-5`))* | `>=1` | tep spec man hinh (`BA` man) nhac co che de xuat: co | — | — | ✅ |
| `C1` | Ⓒ ITL | Khuon canon khop `Transaction Mapping L1` | `38` vi tri · `36` ten | — | `CANON_COLS` 38 vi tri · `CANON_36` 36 ten | — | ✅ |
| `C2` | Ⓒ ITL | So cot co ten cua `ITL Ledge` *(⭐ `64` cua tai lieu DUNG — `69` cua toi la phep do qua tho)* | `64` (hang 7+8) | «64 cột» co trong tai lieu: co | — | — | ✅ |
| `C3` | Ⓒ ITL | So truong adjust | `7` dai | «7 trường» co trong tai lieu: co | — | — | ✅ |
| `C4` | Ⓒ ITL | So cot luoi `F02`: tai lieu vs MA *(⭐ `GAP-SPEC-03` «that ra 23» DA CU — do lai 17/09)* | `52` = `len(BANG_COT)` | khai «52 cột» (phan lon la BIEN BAN): co | `len(BANG_COT)` = 52 | — | ✅ |
| `C7` | Ⓒ ITL | CACH CONG ra `52` ma tai lieu khai *(⭐ SUA 17/09 — tong tung DUNG ma cach cong SAI; hai phep cong cung ra 52 nen ⛔ khong ai bat duoc)* | `24` nen + `28` canon | khai «24 nen + 28 canon»: co | 24 nen + 28 canon | — | ✅ |
| `C5` | Ⓒ ITL | `Dien giai` co trong COT so `fls_itl.memo` *(cot rong tu nap 10/09 — `INV-I08` ⛔ cho `UPDATE`; xem `C5b`)* | `>0` | — | `memo` = cot `C` cua canon | 0/8387 dong co `memo` | ⛔ |
| `C5b` | Ⓒ ITL | `Dien giai` co trong KHO (khung xem `fls_dien_giai`) *(⭐ co tu 18/09 (`QĐ-ITL-145`, migration `0026`) — tin hieu ghep giau nhat nay DO DUOC)* | `>0` | — | `fls_dien_giai` = so ⋈ anh chup moi nhat | CO dong so mang `Dien giai` (so o man) | ✅ |
| `C6` | Ⓒ ITL | Khau adjust da chay lan nao *(⭐ DAT 18/09 — 4.424 but toan GOI Y cua may (`QĐ-ITL-143`))* | `>=1` | — | — | `fls_adjustment` 4428 · `fls_journal` 4428 | ✅ |
| `C8` | Ⓒ ITL | ⭐ NGUOI da chot o nao chua *(⛔ `fls_sua_tay` van 0: may GOI Y, nguoi CHOT — `INV-I16`)* | `0` — chua ai | `0` — ⛔ chua ai go | `may_ghep` vs `ghi_tay` | may goi y 4424 · NGUOI chot 0 (⛔ dem may + UAT) | ✅ |

**17/20 khớp · 3 lệch.** ⛔ Bảng này **sinh bằng máy** — ⛔ không một ô nào gõ tay. Đổi một con số `CHUẨN` thì phải **đo lại và ghi xuất xứ** *(`docs/ITL/_tools/khop_owner.py`)*.

<!-- SINH-KHOP:KET-THUC -->

---

## §2 · Vì sao cổng hiện có ⛔ KHÔNG bắt được loại lệch này

`docs/ITL/_tools/kiem_tai_lieu.py` gác **`K1`–`K5`**:

| Cổng | Canh gì |
|---|---|
| `K1` | version header khớp changelog |
| `K2` | số `CR` khớp giữa hai tệp |
| `K3` | bảng markdown lệch cột |
| `K4` | `CR` đóng mà ⛔ không có chứng cứ |
| `K5` | ⛔ không tài liệu nào mang một **ngày chưa xảy ra** |

⇒ **Cả năm đều canh VỆ SINH, ⛔ không canh CẤU TRÚC.** Một bộ tài liệu mô tả **sai hệ thống** vẫn đi qua `K1`–`K5` **sạch bong** — và nó **đã đi qua**: `109/109` số sống, `K1`–`K5` xanh, `31/31` thuyết minh, `37/37` bảng tuyến, trong khi owner mở ra và thấy drift ở **xương sống**.

⭐ Đây đúng lớp lỗi `GAP-DOC-08` đã ghi — *cổng canh **SỐ**, ⛔ không canh **CÂU*** — chỉ là ở bậc cao hơn: cổng canh **số** và **câu**, ⛔ không canh **DANH SÁCH MODULE**.

---

## §3 · LỘ TRÌNH — năm chặng, và **thứ tự là kết luận**, ⛔ không phải sở thích

### `C0` · CHỐT TRỤC — **owner** · ✅ **ĐÃ ĐÓNG 17/09** *(trả lời ở `§0b`)*

⛔⛔ **⛔ Không được bắt đầu `C1` trước khi câu này có trả lời**, vì mọi thứ sinh ra ở `C1`–`C4` đều **khoá theo danh sách module**. Sửa trục sau khi đã sinh artifact = làm lại từ đầu.

> ✅ **Đã có trả lời** ⇒ `C1` mở. ⭐ Và trả lời `Q1` làm **`C1` đổi hình**: bảng đối chiếu ⛔ không so với *"phát biểu của owner"* nữa mà so với **bộ ERD ggsheet** — tức **cột chuẩn của bảng nay ĐO ĐƯỢC**, ⛔ không còn là một câu người viết.

| # | Câu hỏi chặn | Vì sao ⛔ không đoán được |
|--:|---|---|
| `Q1` | **«ITL (1/2)» có phải một module riêng ⛔ không?** Nếu có: nó bắt đầu ở đâu và kết thúc ở đâu — *sinh `itl_id`*, hay *cả việc làm giàu `S3`*? | Tài liệu đang coi đây là **chặng kỹ thuật bên trong đường nạp**. Nếu nó là module thì `09_MILESTONES_HAI_TAC_VU.md` **sai từ TÊN TỆP**, và trục `khau` phải thêm giá trị thứ tư ⇒ **23/23** đối tượng khai lại |
| `Q2` | **`PE`/`PI` nạp THẲNG, hay đi nhờ `PM_Unpivot` như hiện nay?** | Hai câu trả lời ra **hai schema khác nhau**. Nạp thẳng ⇒ thêm `2` lằn vào `LAN`, thêm bảng, thêm ảnh chụp. Đi nhờ ⇒ ⛔ không thêm gì, nhưng tài liệu phải **nói thẳng** rằng `PE`/`PI` ⛔ không phải nguồn của FLS |
| `Q3` | **«đủ trường như ggsheet» — ggsheet NÀO, tab nào?** | `PM_Unpivot` sống ở bản `Importrange` trong `ITL RAW` *(`QĐ-ITL-14`)*; sổ `ITL Ledge` có **bản gốc** và **bản sao `1md85t…`** *(`QĐ-ITL-50`)*. Đo nhầm bản = đo nhầm mẫu số, và bản `.xlsx` đã một lần **phá huỷ ngày** |

**Đầu ra `C0`:** một quyết định `QĐ-ITL-…` ghi **danh sách module chính thức** + trả lời `Q2`/`Q3`. ⛔ Không cần dài; cần **ký**.

### `C1` · BẢNG ĐỐI CHIẾU GỐC — *máy* · ✅ **XONG 17/09** *(`docs/ITL/_tools/khop_owner.py` · `16` phép · bảng ở `§1b`)*

Một tệp duy nhất `docs/ITL/_tools/khop_owner.py` + bảng sinh ra, mỗi phát biểu của owner **một dòng**, **bốn cột**:

| phát biểu | **tài liệu** nói gì | **mã nguồn** nói gì | **kho** nói gì |

⛔ Ba cột sau **⛔ không gõ tay** — đọc thẳng từ `fls/`, từ `docs/`, từ `psql`. Lý do: bảng gõ tay chính là thứ vừa drift.

⭐ Đây thành **SSOT của cuộc audit**. Mọi chặng sau **sửa cho đến khi bốn cột bằng nhau**, ⛔ không sửa cho đến khi *"đọc thấy hợp lý"*.

### `C2` · ĐO CÁI CHƯA AI ĐO — **hai mẫu số**, chặn `D3` + `D4`

| # | Phép đo | Mở khoá |
|--:|---|---|
| `M1` | Đọc tiêu đề `PM_Unpivot` ⇒ *`29` cột ấy **tên** gì* | ✅ **XONG 17/09** *(`§0c`)* — owner tải `A _ PAY100 _ PM11 Entry Data`: `28` có tên, `PM_COT` khớp **`8/8`**, và `tho` hoá ra **đã giữ `27/28`** |
| `M2` | Đọc tiêu đề sổ `ITL Ledge` | ✅ **XONG 17/09**: **`69` vị trí**, tiêu đề người ở **hàng 7**, **4 vùng**. Con số `64` *(ước lượng từ AS-IS)* nay **có số đo thay thế** |

⭐⭐ **Đo bằng CỬA THẬT của FLS** *(`fls/oracle/nguon.py` + lằn `do_hinh_dang`)*, ⛔ không bằng một lần mở sheet bằng mắt và cũng ⛔ không bằng bản `.xlsx`. Hai lý do đều đã có bia: `measure-by-write-door-rule` *(đo sai **8,6 lần** vì đo ở cửa đọc)* và `itl-xlsx-export-destroys-dates` *(bản `.xlsx` chỉ còn **2,7%** ngày đúng)*.

⚠ `M1`+`M2` là chỗ **lộ trình này có thể đắt hơn dự kiến** — nếu mẫu số ra rất lớn thì ⓷/⓸ ⛔ không còn là *"bổ sung vài trường"* mà là **một quyết định phạm vi**, và nó quay lại bàn owner.

### `C3` · SỬA TÀI LIỆU — tách **tệp KHAI** khỏi **tệp CHÉP**

> ◐ **ĐANG CHẠY 17/09** — mục ④ *(màn adjust)* **xong**: đọc `19` chỗ ghi `52` ⇒ `18` là **biên bản** *(giữ)*, sửa đúng **`1`** câu nói hiện tại; và hai cáo buộc `64`/`52` của `v0.1` **đổ vì phép đo của tôi** — xem `§0e`. ⛔ Còn mục ① *(từ điển tên module)* · ② *(lằn nạp `PE`/`PI`)* · ③ *(màn ghép)*.

⛔⛔ **⛔ Đừng mở `54` tệp.** Việc đầu của `C3` là chia bộ tài liệu làm hai loại:

- **Tệp KHAI** — nơi một sự thật được **tuyên bố lần đầu** *(`09_MILESTONES`, `02_PROCESS_FLOW`, `05_DATA_DICTIONARY_ERD`, `06_SCREEN_SPEC`, `12_BA_MAN_GHEP_PM`, `fls/db/schema.py`)*.
- **Tệp CHÉP** — nơi nó được **nhắc lại** *(dashboard, artifact, changelog, bản đồ sinh máy)*.

⇒ Sửa **tệp KHAI** bằng tay; **tệp CHÉP** thì hoặc **sinh lại bằng máy** *(bản đồ `tầng`/`khâu` đã là vậy — `4` artifact)*, hoặc **gác bằng cổng** ở `C4`. ⛔ Một sự thật được gõ tay ở `54` chỗ thì nó sẽ lệch ở `54` chỗ.

**Thứ tự sửa, theo phụ thuộc:**

| # | Sửa gì | Điều kiện |
|--:|---|---|
| ① | Trục module: `09_MILESTONES…` + trục `khau` trong `fls/db/schema.py` | cần `Q1` |
| ② | Lằn nạp: `LAN` trong `chup.py` + `02_PROCESS_FLOW` + `05_DD_ERD` | cần `Q2` |
| ③ | Màn ghép: đưa **cơ chế đề xuất** vào `12_BA_MAN_GHEP_PM` + bảng trường so với `M1` | cần `M1` |
| ④ | Màn adjust: **xoá con số `52`** *(`GAP-SPEC-03`, nợ 14 ngày)* + bảng trường so với `M2` | cần `M2` |

### `C4` · BỐN CỔNG CẤU TRÚC — phần làm cho nó **ở lại**

> ◐ **ĐANG CHẠY 17/09.** ✅ **`G-MOD-3` XONG** — `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py`, **`5` bài**, và **`4` nhánh NO đã chứng minh ĐỎ**. ⛔ `G-MOD-1`/`G-MOD-2` **đã bị `C1` nuốt** *(phép `T1`·`T2`·`T3`·`A1`)* ⇒ ⛔ đừng dựng lại. ⛔ `G-MOD-4` còn — ⛔ **nhưng ⛔ đừng làm nó bằng phép quét văn xuôi**: đó là `Đ2`, và nó sẽ đỏ giả trên mọi câu đính chính. Hướng đúng: **sổ đăng ký con số** *(`CHUAN` của `khop_owner.py` đã là mầm — mỗi mục đã mang **xuất xứ**)*.

| Cổng | NO khi | Chống lại |
|---|---|---|
| `G-MOD-1` | danh sách module trong tài liệu ⛔ không khớp danh sách đã ký ở `C0` | drift `D1` quay lại |
| `G-MOD-2` | `LAN` trong mã ⛔ không khớp danh sách lằn đã ký | drift `D2` quay lại |
| `G-MOD-3` | một trường có trong mẫu số *(`M1`/`M2`)* mà ⛔ không xuất hiện ở **một trong hai**: bảng trường của tài liệu, **hoặc** danh sách *"cố ý ⛔ không đọc"* | trường rơi **im lặng** — đúng lớp lỗi `PM_COT` |
| `G-MOD-4` | một con số cột ⛔ không nói **nó đếm vật nào** | năm con số `23/38/52/55/64` cùng một chỗ |

⭐⭐⭐ **Mỗi cổng phải được CHỨNG MINH ĐỎ trước khi được tin** — phá nguồn cho sai, chạy cổng, xem nó cắn, rồi trả nguyên. ⛔ Một cổng chưa từng thấy đỏ là một cổng chưa biết có sống. *(Lằn này đã chạy thật cho `3` cổng bản đồ `khâu` hôm 16/09.)*

⚠ `G-MOD-3` là cổng **đắt nhất và đáng nhất**: nó biến *"đủ trường như ggsheet"* từ một **cảm giác** thành một **phép trừ tập hợp**.

---

## §4 · Cái lộ trình này ⛔ KHÔNG giải

| # | ⛔ Không giải | Nó thuộc về đâu |
|--:|---|---|
| ⓐ | **Xây** module «ITL (1/2)» nếu `Q1` trả lời *có* | đây là doc-only; xây là việc của `03_IMPLEMENTATION_PLAN` |
| ⓑ | **UIUX thân thiện** ở ⓷ — audit đo được *đủ trường* và *có đề xuất ⛔ không*, ⛔ không đo được *thân thiện* | một buổi ngồi cùng kế toán; `GAP-SCR-03` đã mở sẵn đúng việc này |
| ⓒ | `fls_adjustment`/`fls_journal` **`0` dòng** — tài liệu mô tả đúng thì nó vẫn `0` | cần **một kế toán bấm thật**, ⛔ không cần thêm chữ |
| ⓓ | Câu chặn `5` story: *lớp trạng thái công việc treo vào `pm_line_id` ⛔ không* | vẫn chờ owner, `BA-05 §DD-I11 §H` |

---

## §5 · Changelog

- **v0.10** *(2026-09-17)*: ⛔⛔ **SỬA MỘT CON SỐ TÔI ĐÃ ĐƯA VÀO `QĐ-ITL-128`.** Tôi gọi `4,8%` *(tên người trong `Description`)* là **«sàn dưới»** — **quá tự tin**. Đầu dò là `Tên tài khoản` của lằn `PM`, và đo lại: **`44`/`408` = `10,8%` mục của đầu dò là BẨN** *(tên cột lọt vào ô dữ liệu)* ⇒ nó **thổi con số lên**; đồng thời đầu dò ⛔ không phủ hết tên người ⇒ nó cũng **hụt xuống**. ⇒ Sai số **hai chiều**, ⛔ không phải một cận. Ước lượng sau khi trừ phần bẩn: **~`4,3%`**. ⭐ **Quyết định ⛔ không đổi** *(`4,3%` hay `4,8%` đều ⛔ không lật cán cân với `23,0%`)* — ⛔ nhưng câu chữ trong sổ quyết định **phải đúng**, và nó đã được sửa. ⚠ Cách nó lộ ra: tôi quét PII một tệp lạ và ra **`1` khớp**; soi kỹ thì cái *«tên»* ấy là **`FILE ĐÍNH KÈM`** — một **tên cột**. ⇒ Một dương tính giả trên một tệp đã kéo ra một **sai số trong một quyết định đã ký**. ⛔ Và tôi lại **quét một tệp ⛔ không phải của mình vào commit** *(`FLS-Duong-nap-Gsheet-vao-kho.html`, tạo lúc `17:38`)* — đúng lỗi tôi đã tự nêu với `ap-status-check.py`. Đã đo: tệp **⛔ không mang dữ liệu người** *(email `0` · số `9`–`12` chữ số `0` · tên người `0` sau khi loại dương tính giả)*, nên tôi **giữ nguyên** thay vì gỡ mất việc của người khác — ⛔ nhưng **chờ owner nói**.
- **v0.9** *(2026-09-17)*: ⭐⭐ **`T3` GIẢI — TỪ ĐIỂN TÊN.** Owner chốt: tên **CHUẨN là tên TÁC VỤ**; hai bộ kia là **bí danh** ⇒ ⛔ **KHÔNG đổi tên tệp** `09_MILESTONES_HAI_TAC_VU.md` — nó **đang đúng**, và phép đo cũ của tôi *(đòi tên ấy biến mất)* **đo sai thứ**. ⛔⛔ Cái thiếu suốt ⛔ **không phải** *«tài liệu chưa đọc tên tệp»* — mà là **CÂU NỐI**: ⛔ không dòng nào nói `File 1_2` **là** cái mà `09_MILESTONES` gọi là *«mốc `A`»*. `TU_DIEN_TEN` khai **12** tên trên **3 xuất xứ** *(tài liệu · lời owner · tệp AS-IS)*, sinh thành bảng trong `BA-05` cùng khối với bản đồ khâu, **⛔ không bản khai thứ hai**. ⚠ Ghi thẳng một sự thật ⛔ không được làm tròn: **«ITL (1/2)» trỏ tới HAI khâu** *(Ⓐ + Ⓑ)* vì nó là một **TỆP** chứa cả `Transaction Original` lẫn `Transaction Mapping L1` — chính vì thế `Q1` trả lời *«nó là một BƯỚC»*. `7` bài mới, **4 nhánh NO chứng minh ĐỎ**. ⭐⭐ **Và phép chứng minh ĐỎ bắt một bài XANH GIẢ của chính tôi**: bản đầu chỉ hỏi *«có tên nào trỏ >1 khâu ⛔ không»* — luôn được thoả bởi dòng `mã nguồn` *(liệt kê cả ba)*, kể cả khi «ITL (1/2)» đã bị bóp về một khâu. Phải thử phá **ba lần** mới lộ ⇒ bài viết lại để ghim **đúng cặp khâu của đúng cái tên**. ⛔ Và tôi cắn lại **lần thứ ba** cái bẫy `
` qua **hai lớp shell** *(đã có trong `CLAUDE.md`)* — vá bằng `Edit`, ⛔ không heredoc. Cổng `C1`: **`18` phép · `13` khớp · `5` lệch** *(từ `12/18`)*. Bộ thử **1.691** *(+7)*.
- **v0.8** *(2026-09-17)*: ⭐⭐⭐ **`C5` GIẢI — owner mở lại `QĐ-ITL-92` *(`QĐ-ITL-128`)*: `Description` ĐƯỢC ĐỌC, cả `6/6` trường.** Đo **cả hai vế trước khi quyết** *(58/60 sheet `R |` · **7.712** ô có chữ)*: **vế A — dữ liệu người** tên NGƯỜI **4,8%** *(sàn dưới)* · doanh nghiệp 5,2% · điện thoại 2,3% · dạng giấy tờ 9,5% *(**trần trên** — số tài khoản cũng 9/12 chữ số)* · email 0,1%; **vế B — tín hiệu ghép** mã `PI…/PE…/PM…` **23,0%**, **gấp ~4,8 lần** tỉ lệ tên người. ⛔ Chân ⓐ của lệnh cấm **vẫn đúng** *(nó THẬT SỰ mang tên người — một cá nhân xuất hiện 62 dòng)*; chân ⓑ **đã đổi** *(`F04` ⛔ không cần, **màn ghép** cần)*. Owner được nêu rõ nó **ngược tiền lệ `QĐ-ITL-107`** và **vẫn chọn hình rộng nhất** — đã ghi vào sổ quyết định kèm cả ba hình bị loại. ⭐ Đổi ở **một dòng khai** *(`sao_ke.TRUONG_DOC_DUOC`)*; cửa chặn tự mở đúng chỗ vì nó trừ theo bản khai ấy, và **`QĐ-ITL-107` ⛔ không bị mở theo** *(có bài ghim)*. Cả `1.682` cổng chỉ ra **đúng `2`** chỗ còn lại — cả hai là bài **ghim lệnh cấm**, và chúng ⛔ **không bị xoá** mà bị **đảo chiều**, giữ nguyên nỗi lo gốc. ⚠⚠ **`C5` vẫn LỆCH và đó là sự thật**: lệnh cấm cũ ⛔ không lưu gì để nạp bù ⇒ **`8.387` dòng sổ đang có VẪN `memo = NULL`**; chỉ **ảnh chụp MỚI** mới mang diễn giải. ⛔ Và phép đo PII đầu tiên của tôi ra bảng toàn `0` — hàng `1` mang số **thực** (`2.0`) chứ ⛔ không phải chuỗi `"2"` ⇒ khớp `0/60` sheet; `Đ3` giữ tôi lại, và tôi đã **thêm chốt chặn vào chính công cụ đo** *(0 sheet ⇒ NO, ⛔ không in bảng `0`)*. Bộ thử **1.684** *(+2)*.
- **v0.7** *(2026-09-17)*: ⭐⭐⭐ **`G-MOD-3` XONG — *«đủ trường như ggsheet»* nay là MỘT PHÉP TRỪ TẬP HỢP.** Vũ trụ = **`28`** cột có tên của `PM_Unpivot`, **đo từ KHO** *(khoá `tho` + bản cấm)*, ⛔ không gõ tay. Ba rổ phải **phân hoạch đúng**: `PM_COT` **`14`** *(đặt kiểu)* + `PM_COT_RIENG_TU` **`1`** *(cấm)* + ⭐ `PM_COT_CHUA_DAT_KIEU` **`13`** *(mới — mỗi trường **một LÝ DO bắt buộc**)* = **`28`**. ⇒ Nguồn thêm một cột thì cổng **ĐỎ** cho tới khi có người **phân loại và ghi lý do** — chặn đúng cái đã xảy ra: `tho` chỉ có từ 11/09, trước đó **20 cột biến mất ngay lúc đọc**. `5` bài, và **cả `4` nhánh NO đã chứng minh ĐỎ** *(cột rơi khỏi ba rổ · bản khai nhắc cột kho ⛔ không có · trường thiếu lý do · bản **CẤM** lọt vào kho)*.
  ⭐⭐ **Tách `B1` làm HAI dòng, cố ý**: `B1` = *"⛔ không còn lỗ im lặng"* **(✅ khớp)** · `B6` = *"đã đặt kiểu đủ trường chưa"* **(⛔ `14`/28)**. Gộp hai câu vào một dòng là **cách dễ nhất để một khoảng trống biến mất sau một dấu tick**.
  ⚠ **Và phép chứng minh ĐỎ của tôi hỏng một nhánh trước khi đúng**: bài `import` tên vào module của nó nên vá ở `pm_join` ⛔ không tới ⇒ nhánh *"bản CẤM lọt"* báo **"vẫn xanh"**. Đó là **phép chứng minh hỏng**, ⛔ không phải cổng chết — đúng `Đ3`: *một kết quả âm từ một phép đo hỏng ⛔ không phải bằng chứng*. Vá đúng chỗ ⇒ **cắn thật**.
  Cổng `C1`: **`18` phép · `12` khớp · `6` lệch** *(từ `11/17`)*. Bộ thử **1.682** *(+5)*.
- **v0.6** *(2026-09-17)*: ⭐⭐⭐ **Owner chốt `B3`: `PE`/`PI` là CỘT CÓ KIỂU trong `fls_pm_line`, ⛔ chưa cần bảng riêng** ⇒ đã dựng *(migration `0023`)*: `5` cột, hợp đồng cột lằn `PM` mở **`8` → `14`** vị trí *(`PM_KHAI_VERSION` `1`→`2`)*, **cả 14 đo lại trên bản ngoài kho: lệch `0`**; nạp bù từ `tho` — `PE` **3.500** · `PI` **22.904** · `Advance` **3.381** + `Urgent` **119**, `pg_verify` **khớp**. ⭐⭐ **Ba bất biến đo được, chỉ MỘT thành `CHECK`**: *một dòng có đúng một cha* và hai cặp `slip`/`line` **cố ý ⛔ KHÔNG** thành `CHECK` — phép chèn chạy **trong MỘT giao dịch** cho cả lần nạp nên một `CHECK` biến **một dòng lạ** thành **đổ cả lượt nạp**; thay vào đó máy **đếm và nêu tên** (`INV-I16`). Quyết định ấy **ghim bằng bài thử**, vì *«0 ngoại lệ/26.404»* mời người sau thêm cho chắc. `BA-05` **v0.27** *(`DD-I12`)*. ⛔⛔ **Và một cảnh báo về chính tôi, lần thứ BA trong buổi**: câu *«⛔ không tệp nào ghi bề rộng `PM_Unpivot`»* **SAI** — `FLS-Process-PM-den-ITL.md:186` và `pm_join.py:192` đều đã ghi **28 cột**. ⇒ Luật: mọi câu *«chưa ai ghi X»* phải grep **cả `docs/` LẪN `fls/`+`tools/`**, vì ở repo này một sự thật đã đo **thường sống trong chú thích mã**. Cổng `C1`: **`17` phép · `11` khớp · `6` lệch** *(từ `10/17`)*. Bộ thử **1.677** *(+7)* · số sống **109/109** · `lint-imports` 9/0 · bảng tuyến 37/37 · thuyết minh 31/31.
- **v0.5** *(2026-09-17)*: ⛔⛔⛔ **`D4` VIẾT LẠI — hai con số tôi gọi là lệch thì CHÍNH TÔI đo sai.** ⓵ **`64` ĐÚNG**: `ITL Ledge` có **`64`** cột **có tên** đếm trên **hàng `7` + hàng `8`** *(`69` của tôi là bề rộng kể cả đuôi rỗng; hàng `8` là thứ tôi bỏ sót mà `BA-05 §DD-I04` đã khai)*. ⓶ **`52` ĐÚNG**: `len(cot_so.BANG_COT)` = **`52`** đo thẳng ở mã ⇒ `GAP-SPEC-03` *(«thật ra 23»)* là **ảnh chụp của 03/09**, trước khi `CANON_LEN_LUOI` lên lưới — đã ghi lại ở **cả hai** chỗ chép GAP, **chờ owner đóng**. ⭐⭐⭐ **Chỗ sai THẬT rất hẹp: TỔNG đúng, CÁCH CỘNG sai** — `BA-06` khai *«38 canon + 14 hợp đồng»*, đo ở mã là **`24` nền + `28` vị trí canon**, và **cả hai đều ra `52`** nên mọi cổng canh **tổng** đều xanh suốt **20 ngày**. ✅ Đã sửa `06_SCREEN_SPEC §6` + dòng `12_P6_WEB_PLAN:157`. ⛔ **`18/19` chỗ ghi `52` là BIÊN BẢN** *(sổ `QĐ`/`CR`, changelog, mô tả GAP, và các câu về **nguyên mẫu** `748 × 52`)* — xoá chúng là **viết lại lịch sử**; chỉ **`1`** câu nói hiện tại phải sửa. ⭐⭐⭐ **Luật rút ra, và nó cắn HAI LẦN TRONG MỘT GIỜ**: *phép ĐẾM CHỮ ⛔ không phân biệt được tài liệu đang **KHAI** với tài liệu đang **GHI LẠI*** — `C4` đếm `"52 cột"` đòi `=0`, sửa xong tôi viết `C7` đếm `"38 cột canon"` đòi `=0` và nó **lệch mãi** vì chính **câu đính chính** phải trích lại chuỗi sai. ⇒ Chữa: **so HAI NGUỒN** *(cổng chung `#13`)*, và hỏi *"**câu ĐÚNG có chưa**"* ⛔ không hỏi *"chuỗi sai còn không"* — **bằng chứng dương** ⛔ không bị biên bản làm nhiễu. ⇒ `D4` nay đọc là: mỗi con số đếm **một vật khác nhau** và **phần lớn đều đúng**; cái thiếu là **⛔ không chỗ nào nói NÓ ĐẾM GÌ** ⇒ lý lẽ đo được cho `G-MOD-4`. Cổng `C1`: **`17` phép · `10` khớp · `7` lệch** *(từ `7/16`)*.
- **v0.4** *(2026-09-17)*: ⭐⭐ **`C1` XONG** — `docs/ITL/_tools/khop_owner.py`, **`16` phép** trên **3 nguồn** *(tài liệu · mã nguồn · kho)*, bảng sinh vào `§1b` giữa mốc `SINH-KHOP`, có `--kiem`. Kết quả **`7` khớp · `9` lệch**. ⭐ Cổng NO khi kết quả **khác `mong`** *(cả hai chiều)* — sửa được một chỗ cũng **ĐỎ**, buộc ghi lại bản khai; và phép ⛔ **không đo được** *(kho tắt · mẫu khớp `0` hoặc `≥2` · tập rỗng)* là **ĐỎ**, ⛔ không phải *"không thấy lệch"*. ⛔⛔⛔ **Và nó BẮT MỘT CÂU SAI CỦA CHÍNH TÔI ở lượt chạy ĐẦU TIÊN** ⇒ **`§0d`**: ba thứ tôi báo là *phát hiện* thì `BA-05` **đã có** — `§DD-I04` khai **trọn** cấu trúc `ITL Ledge` *(từng hàng `1`→`8`, ba vùng, "`7` khối × `4` cột", khuôn `Classifying → Manual input → MID → Final`, kể cả hàng `8` tôi ⛔ không nhắc)*, hai tên tệp khai ở `BA-05:39`+`130`, và `6.843` có từ `QĐ-ITL-05` **18/08** *(còn đi xa hơn: nó chỉ là **31%** của **22.360** ô)*. ⇒ **`D4` phải đọc lại — `BA-05` ⛔ KHÔNG drift về cấu trúc AS-IS**; drift thật hẹp hơn: **năm con số cùng mô tả một vật vẫn lưu hành**. ⭐ Cái còn lại **thật mới**: bề rộng ba thực thể `PM`/`PE`/`PI` · `PM_COT` **kiểm** `8/8` · `tho` **27/28** · phân hoạch `PE`/`PI` **`0`** ngoại lệ · `memo` **`0`/8.387** · `ITL Ledge` **`69`**. ⚠ Bài học **về phương pháp của tôi**: đo nguồn rất kỹ, grep tài liệu tìm **mẫu lệch**, ⛔ nhưng ⛔ **không ĐỌC** mục tài liệu nói về **cùng một vật** — lớp `measure-old-system-before-declaring-new`, lần này thứ quên đo **chính là bộ tài liệu đang audit**. ⭐ Thêm phép `T3` *(tên tệp mang số khâu — `09_MILESTONES_HAI_TAC_VU.md`)*, là phần **còn lại** của `D1`.
- **v0.3** *(2026-09-17)*: ⭐⭐⭐ **`M1` ĐÓNG** — owner tải `A _ PAY100 _ PM11 Entry Data` *(9 tab, có đủ `PE_Unpivot`·`PI_Unpivot`·`PM_Unpivot` **có giá trị**)*. Mẫu số: `PE` **27/23** · `PI` **26/24** · `PM` **29/28**, tiêu đề **hàng 2**. ⭐⭐ **Hợp đồng `PM_COT` khớp `8/8`** — lần đầu so với bản ngoài kho, ⛔ không lệch một cột. ⭐⭐⭐ **Bức tranh đảo chiều: `fls_pm_line.tho` ĐÃ giữ `27/28` trường** *(thiếu đúng `Email Address` — bản cấm, ⇒ `PM_COT_RIENG_TU` **hoạt động đúng như khai**)* trên **`26.404/79.212`** dòng ⇒ *«đủ trường như ggsheet»* ⛔ **không phải bài toán NẠP** mà là **ĐẶT KIỂU + BÀY RA** + nạp bù `52.808` dòng cũ. ⭐⭐⭐ **Quan hệ `PE`/`PI` là phân hoạch TUYỆT ĐỐI**: `22.904` chỉ `PI` · `3.500` chỉ `PE` · **`0`** cả hai · **`0`** không cha ⇒ **bất biến ứng viên** *(schema hiện chỉ có `1` CHECK cho `18` bảng)*. `20` trường chưa đặt kiểu, gom **5 nhóm** để owner quyết theo nhóm. ⛔⛔ **Một phép đo của tôi HỎNG và đã sửa**: thử nối *"nội dung gõ ở bank"* với `Diễn giải` sao kê ⇒ ra `0`, suýt kết luận *"⛔ không phải khoá ghép"* — thật ra **`fls_itl.memo` NULL trên `8.387/8.387`**, tức **xanh trên tập rỗng**. Trạng thái thật của sổ: `doc_date`·`curr` **8.387** · `doc_no` 8.383 · `ps_co` 7.558 · `ps_no` 4.520 · ⛔ `memo`·`acct`·`le` **`0`** ⇒ **tín hiệu ghép giàu nhất ⛔ KHÔNG có trong kho**. Phía PM thì tín hiệu **có thật**: **`5.901/26.404` = `22,3%`** dòng mang mã `PI…`/`PE…` trong nội dung bank ⇒ nửa còn thiếu của **`US-KT-037`**. ✅ Tệp mới **an toàn**: `.gitignore:13` phủ cả `RAW/`, chưa vào index.
- **v0.2** *(2026-09-17)*: ⭐⭐⭐ **`C0` ĐÓNG — owner trả lời cả ba câu, và `Q1` đổi SSOT của audit**: chuẩn là **bộ ERD ggsheet hiện có**, ⛔ không phải bốn phát biểu ⇒ «ITL (1/2)» là **BƯỚC**, ⛔ không phải module ⇒ trục `khau` **giữ `3`**, ⛔ không khai lại `23/23`. `Q2`: **đường vào ≠ thực thể** — `LAN` giữ `3`, ERD phải có `PE`·`PI`·`PM` **riêng**. `Q3`: tệp ở `AS-IS system/Accounting_Files/RAW`, **chỉ cần sample**. ⭐⭐ **Tên module của owner CHÍNH LÀ TÊN TỆP** *(`File 1_2 (RAW)` · `File 2_2 (ADJUSTED)`)* — bộ tài liệu ⛔ chưa bao giờ đọc tên tệp như một lời khai, và đó là gốc của `D1`. ⭐⭐ **`M2` XONG**: `ITL Ledge` = **`69` vị trí**, tiêu đề người ở **hàng 7**, **4 vùng** *(`ADJUSTMENT` `7` dải · `ALLOCATE` · `AUDIT`)*, hàng `2` **tự khai nguồn** là `Transaction Mapping L1` của File 1/2, hàng `3` mang `7` bộ đếm `# Input here` cộng ra **`6.843`**. `Transaction Mapping L1` = **`38` vị trí · `36` có tên** ⇒ **khớp chính xác** khuôn canon FLS. ⛔⛔ **`CR#8` nói `cdt1_cfa1`/`cdt1_cfa2`/`alloc_method` *"⛔ không có ở đâu cả"* — SAI trên AS-IS**: hai cái đầu là `AU`/`AV` *(`ALLOCATE ZONE`)*, cái thứ ba là `Mapping Master` `K`/`L`. ⛔ **`M1` CÒN CHẶN**: cả `4` tab `Importrange*` ra **`#REF!`** trong bản offline ⇒ bề rộng còn *(`PM` = **`29`**)*, **tên cột mất** — cần một bản xuất `PM_Unpivot` có giá trị, hoặc đọc qua cửa sống.
- **v0.1** *(2026-09-17)*: Viết mới sau khi owner báo drift và nêu **bốn phát biểu**. Đo trước khi khai: `D1` số khâu **3 vs 4** *(module «ITL (1/2)» ⛔ không có tên ở đâu)* · `D2` lằn nạp **3 vs 5** *(`PE`/`PI` chỉ là cột tra cứu; `Cash` khai mà **`0`** ảnh)* · `D3` `12_BA_MAN_GHEP_PM` có **`0`** lần *"đề xuất"*, `PM_COT` đọc **`8`** cột và **mẫu số chưa ai đo** · `D4` **năm** con số cột cho một vật *(`52` đã bị chứng minh sai **14 ngày** trước, vẫn còn **21** lần)* và cả hai bảng của khâu adjust đều **`0`** dòng. Đo cổng hiện có: `K1`–`K5` canh **vệ sinh**, ⛔ không canh **cấu trúc** ⇒ bộ tài liệu sai hệ thống vẫn đi qua sạch. Lộ trình **`C0`→`C4`**, trong đó `C0` là **ba câu hỏi chặn** của owner và `C4` là **bốn cổng** phải chứng minh ĐỎ.
