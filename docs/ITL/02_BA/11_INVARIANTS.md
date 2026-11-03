# 11 — INVARIANTS: bất biến hệ thống

**Version:** v0.8 | **Chủ sở hữu:** COO-CFO

Bất biến = mệnh đề **luôn đúng**, được **cưỡng chế bằng kiến trúc** chứ không bằng nhắc nhở (`P-03`). Mỗi dòng ghi rõ tầng enforce; không có tầng enforce = chưa phải bất biến, chỉ là mong muốn.

---

| ID | Bất biến | Enforce ở tầng | Vi phạm thì |
|---|---|---|---|
| **INV-I17** ⭐⭐ | **BẢN KHAI RỖNG = MÁY ⛔ KHÔNG BIẾT — ⛔ KHÔNG phải "mọi giá trị đều sai".** Khi một phép kiểm dựa vào một bản khai *(danh mục, bảng ánh xạ)* mà bản khai ấy **chưa được nạp**, máy ⛔ **không được chặn** — nó phải **cho đi qua và nói ra chỗ rỗng**. Chặn hết là cái máy nói **"sai"** trong khi ý nó là **"tôi ⛔ không biết"**, và người dùng ⛔ không có cách nào phân biệt hai câu ấy. ⚠ Đây là `INV-I16` *(khai `UNMAPPED`, cấm mặc định im lặng)* soi từ **phía ngược lại**: `I16` cấm máy **bịa một câu trả lời**; `I17` cấm máy **bịa một lời từ chối** | **Cửa ghi** *(`fls/repo/ghi_tay.py::_kiem_gia_tri`)* — danh mục `0` dòng ⇒ ⛔ không kiểm; **Màn hình** — nói thẳng *"⛔ chưa có danh mục ⇒ cửa ghi ⛔ không kiểm được"* ngay cạnh ô gõ. ✅ **ĐÃ CƯỠNG CHẾ 2026-09-04** — `QĐ-ITL-86`, phép phá *"danh mục rỗng thì chặn hết"* làm **17 bài đỏ** | Chặn ghi **sai** — kế toán ⛔ không nhập được gì cho tới khi ai đó nạp bản khai, mà ⛔ không ai nói cho họ biết vì sao |

| **INV-I19** ⭐⭐ | **MỘT TÍN HIỆU CHỈ ĐÁNG GIÁ BẰNG ĐỘ HIẾM CỦA NÓ ⇒ PHẢI ĐO TẦN SỐ TRƯỚC KHI BẬT.** Trước khi cho một điều kiện bật báo động *(bảng đỏ, chữ đỏ, dấu cảnh)*, phải **đếm nó chạm bao nhiêu dòng trên dữ liệu THẬT**. Nếu nó chạm phần lớn thì đó ⛔ **không phải** báo động — đó là **trạng thái bình thường** bị vẽ sai loại, và nó làm **mọi** báo động khác trên màn nhạt đi. ⚠ Cùng luật ấy áp cho **ký hiệu**: một dấu dùng 111 lần trên một màn ⛔ không còn là tín hiệu. ⭐ Hai lần đo hôm nay: `chưa phân loại` = **76,6%** *(⇒ hạ nhiệt)*; `le != le_payer` = **13,0%** *(⇒ thu hẹp còn 0,8%)* | **Màn hình** — `BA-10 · DT-I11` khai **ba** việc được bật bảng, mỗi việc kèm con số; `tests/web/test_luat_ky_hieu_man_hinh.py` cưỡng chế luật ký hiệu; `test_dong_binh_thuong_thi_KHONG_co_bang_bao_nao` chặn việc bật báo cho trạng thái bình thường. ✅ **ĐÃ CƯỠNG CHẾ 2026-09-04** — `QĐ-ITL-88·89` | Màn hình **lúc nào cũng đang kêu** ⇒ người dùng học cách **⛔ không nhìn**, và khi có chuyện thật thì ⛔ không còn nấc nào cao hơn |
| **INV-I18** ⭐ | **PHÉP KIỂM ⛔ KHÔNG ĐƯỢC VÒNG TRÒN.** Một danh sách **suy từ chính dữ liệu đang có** thì ⛔ **không được** dùng làm luật cưỡng chế cho dữ liệu ấy: danh sách sẽ ⛔ không bao giờ **lớn được** *(giá trị mới ⇒ bị từ chối ⇒ ⛔ không bao giờ vào ⇒ ⛔ không bao giờ có trong danh sách)*, và mọi dòng **bẩn sẵn có thành luật**. ⇒ Cửa chỉ ép nơi có **bản khai thật** *(`hd` ← `fls_mapping_master`, 73 mã)*; ba danh sách **suy** *(`pay_type` · `cdt1` · `id_payee`)* chỉ là **gợi ý trên màn** | **Cửa ghi** ép `hd`; ⛔ **không** ép ba trường suy. **Màn hình** đóng `pay_type` *(ô chọn)* theo quyết định owner, ⛔ không phải theo luật hệ thống | Danh mục **đóng băng vĩnh viễn** ở đúng tập giá trị của ngày bật phép kiểm |

| **INV-I01** | **Bảo toàn tiền.** Tổng tiền vào ITL = tổng statement, đo **net theo output-sheet**, KHÔNG cộng dồn cả bảng | DQ gate S2 (test bắt buộc) | `dq_failed`, dừng pipeline |
| **INV-I02** | **Số dư khớp sổ.** Balance = ledger theo **ngày × tài khoản** (`1.2 Ledger 112` / `2. CCR`). ⚠ **A-CCR sở hữu phép này** (`QĐ-ITL-18`) — ITL **đọc kết quả** làm cổng, không tự tính lại | Adapter C đọc kết quả A-CCR; DQ gate S2 dùng làm điều kiện chặn | `dq_failed` |
| **INV-I03** ✅ | **`ITL RAW` bất biến.** Không có đường code nào `UPDATE`/`DELETE` dòng đã `raw_frozen` | **DB**: quyền ghi chỉ `INSERT`; trigger `trg_fls_itl_inv_i03` chặn `UPDATE` **và** `DELETE`. ✅ **ĐÃ CƯỠNG CHẾ 2026-08-26** — `fls/db/triggers.py`, test `test_inv_i03_raw_frozen_thi_cam_update` + `..._cam_delete` trên **PG 16 thật** | Lỗi tầng DB, không phải tầng app |
| **INV-I04a** ⭐ | **DANH TÍNH — `itl_id` bất biến.** `itl_id` = **số thứ tự cấp một lần khi dòng vào sổ, rồi ĐÓNG BĂNG**. Sửa **bất kỳ** trường nào của dòng *(kể cả `Ngày chứng từ`)* **KHÔNG** được làm đổi `itl_id` | **DB**: PK + trigger `trg_fls_itl_inv_i04a` chặn `UPDATE` cột `itl_id`; sinh bằng **`SEQUENCE`** — `DEFAULT nextval('seq_itl_id')`. ✅ **ĐÃ CƯỠNG CHẾ 2026-08-26** — test `test_inv_i04a_itl_id_khong_bao_gio_doi` + `test_itl_id_tang_don_khong_trung` trên **PG 16 thật**. ⚠ **Sửa**: câu cũ nói sinh atomic *"theo pattern `fps_id_counter` (đã fix bug dup thật)"* là **đọc ngược** — cách FPS *fix* là **bỏ bảng counter** *(`pg_schema.py:9`)*; bảng counter chính là chỗ **từng sinh id trùng**. Xem `GAP-PLAN-02` | Chặn ghi |
| **INV-I04b** ⭐ | **ĐỐI SÁNH — khoá nội dung `UNIQUE`.** `hash(source_system, source_sheet, Ngày chứng từ, PS Nợ, PS Có, Số chứng từ/Reference, seq_trong_nhóm_trùng)`. Dùng để **khử trùng** và **đối sánh với 302.259 dòng log cũ** *(`P100 Bank/Cash ▸ Log`, khuôn `<YYYYMMDD>\|<Debit>\|<Credit>\|<Reference>` đang chạy thật)*. ⛔ **KHÔNG phải danh tính** | **DB**: unique constraint | Chặn ghi |
| **INV-I05** | **Lineage đầy đủ.** Mọi dòng ITL truy được về `source_id` + sheet + dòng nguồn | **DB**: `NOT NULL` trên cột lineage | Chặn ghi |
| **INV-I06** | **Không dòng nào rơi im lặng.** `#dòng nguồn = #staged + #rejected + #unmapped`, mọi vế đếm được và log | DQ gate S1 (đối chiếu row-count) | `dq_failed` |
| **INV-I07** | **Hợp đồng tương thích ngược.** `ITL Ledge` luôn xuất đủ tập cột `ITL-CONTRACT` đang hiệu lực. ⭐ **Diễn giải v0.3 (`QĐ-ITL-42`):** khi nguồn còn là **Sheet** ⇒ khoá theo **VỊ TRÍ** (`POS-13`). Khi nguồn đã là **bảng** *(PG/BQ)* ⇒ `POS-13` **hết hiệu lực**, thay bằng khoá theo **TÊN + ngữ nghĩa**. Đây đúng điều kiện mà `05` §`DD-I04b` tự đặt: *"không đổi vị trí cho tới khi engine chuyển sang đọc theo tên"* | Test tương thích engine, chạy mọi milestone | Chặn merge; CR loại 3 |
| **INV-I08** | **Điều chỉnh là append-only.** Sửa số chỉ bằng bút toán mới; bút toán `posted` không sửa/xoá | **DB**: journal insert-only + trạng thái `reversed` | Lỗi tầng DB |
| **INV-I09** | **Không đếm hai lần.** Transfer/interbank và cặp AP↔tiền không double-count | DQ gate S2 + S1 (adapter F khử trùng) | `dq_failed` |
| **INV-I10** | **LE hợp lệ.** Mọi dòng có `LE` thuộc danh mục pháp nhân; nhãn không-phải-pháp-nhân (vd `USD`, `HotBonus`) gắn `unmapped`, KHÔNG vào hợp nhất | **DB**: FK tới bảng LE + cột `is_entity` | Chặn ghi |
| **INV-I11** | **Ngày phải là ngày.** Không dòng nào vào `raw_frozen` với `Ngày chứng từ` dạng chuỗi hoặc không parse được | DQ gate S1 (parse + kiểu cột DATE ở DB) | `rejected`, đếm được |
| **INV-I12** | **Run ghim version.** Mỗi `run` lưu version của `ITL-CONTRACT`, `ITL-CANON`, `MAPPING-MASTER` đang hiệu lực | **DB**: `NOT NULL` 3 cột version trên bảng run | Chặn ghi |
| **INV-I13** | **Kỳ đã khoá thì bất động.** Dòng thuộc kỳ `locked` không nhận thêm bút toán | **DB**: check constraint theo `period_state` | Chặn ghi |
| **INV-I14** | **Cờ số nhanh.** Dòng/kỳ ở trạng thái `flash` luôn mang cờ; consumer không được trình bày như số đã chốt | Cột `is_flash` bắt buộc trong `ITL-CONTRACT` | Chặn ghi |
| ~~**INV-I15**~~ ✅ | ✅ **ĐÓNG 2026-08-24.** Câu hỏi *"`P` (`LE`) có bằng `BL` (`ENITY`)?"* **đã được trả lời từ 2026-08-20, trong code, kèm số đo**: `P` điền **100%** *(9.872/9.872)*; `BL` **trống 6.379/10.572** và mục ruỗng dần **100% → 31% → 0% tháng 8/2026**; chỗ cả hai tra được thì **612/2.654 dòng lệch**. ⇒ **không phải hai cột chép nhau** ⇒ **owner chốt cột `P` là SSOT**, engine đã đổi sang đọc `P`(15). `BL` vẫn kéo về snapshot **chỉ để đối chiếu về sau**. Cưỡng chế: `test_itl_le_column_ssot.py` + `test_itl_contract_v1_lock.py` | Test khoá vị trí, chạy mọi milestone | Chặn merge |
| **INV-I16** ⭐ | **Máy không được tự trả lời thay người.** Trường nào máy không suy được thì mang trạng thái **`UNMAPPED`** và **có mặt trong hàng chờ** — ⛔ **cấm** thay bằng giá trị mặc định cứng. *(AS-IS đang vi phạm: cờ `Input here` ⇒ `MID` gán `OGA \| GAC - Other` / `SHQ2 \| Headquarters2` / `Nợ hoá đơn`; đo 24/08 trên 2 khối = **7.476 ô**)* | Code: không có nhánh gán mặc định; DQ gate đếm `UNMAPPED` | `dq_failed` nếu số `UNMAPPED` bị **giấu** thay vì báo |

## Bốn bất biến NGHIỆM THU cho việc dựng-lại-từ-nguồn — `QĐ-ITL-41`

★ Luật *"cấm có ngưỡng"* **giữ nguyên**, nhưng **hạt đo khác nhau theo loại việc**:

| Loại việc | Hạt đo | Vì sao |
|---|---|---|
| **A · tái lập công thức của sổ** *(cùng đầu vào, cùng công thức)* | **khớp 100% từng ô** | phép tất định ⇒ đạt được |
| **B · dựng lại từ NGUỒN** *(adapter A–F)* | **4 bất biến dưới đây** | thứ tự dòng, xử `#N/A`, khử trùng interbank, làm tròn ngoại tệ **khác nhau** ⇒ đồng nhất từng ô là **bất khả** |

| # | Bất biến loại B | Enforce | Vi phạm thì |
|--:|---|---|---|
| **ACC-1** | **Bảo toàn số lượng** — mỗi giao dịch xuất hiện **đúng 1 lần** | đếm | chặn |
| **ACC-2** | **Bảo toàn tiền** — tổng theo `(tài khoản × ngày)` khớp **đến đồng** | so số nguyên | chặn |
| **ACC-3** | **Đối chiếu tập khoá** — tập `INV-I04b` của bản mới **bằng** tập của `Transaction Mapping L1` cũ; phần chênh **liệt kê từng dòng** | so tập hợp | chặn |
| **ACC-4** | **`#N/A`/unmatched có TÊN nguyên nhân** — không được để nhóm "khác" | đếm + phân nhóm | chặn |

⛔ **Cấm viết một con số dung sai ở bất kỳ đâu.** *"Dung sai" là chỗ lỗi trốn được* — một `±0,5%` biến 47 dòng sai thành một dấu tích xanh. Chênh thì **liệt kê từng dòng**, không bao giờ gộp thành phần trăm.

⚠ **Hai chỗ khó, không hứa suông:** ⑴ **làm tròn ngoại tệ** — phải đọc công thức của sổ và bắt chước **đúng thứ tự làm tròn**; nếu chính sổ làm tròn **không nhất quán** thì đó là **phát hiện phải báo**, không phải cái để đặt ngưỡng. ⑵ **so P&L** — so **từng dòng đến đồng**, mọi khoản chênh phải có **một nguyên nhân được đặt tên**; ra **biên bản đối chiếu**, không phải đèn xanh/đỏ.

---

## Ghi chú thiết kế bắt buộc — `INV-I04`

**Phát hiện từ file thật:** `ITL Ledge` AS-IS sinh khoá dạng **`ITL#1`, `ITL#2`, `ITL#3`…** — `itl_id = "ITL#" & No`, mà `No = ROW() − ROW(neo) + 1` **trên bảng `Transaction Mapping L1` đã `SORT` theo ngày tăng** *(`FLS-Process-PM-den-ITL` §3 chặng 7)*. Tức khoá **sinh SAU phép ghép** và **bám vị trí dòng**.

Khoá này **không ổn định** theo hai đường đo được:
- **Nhập lùi ngày ⇒ đánh số lại toàn bộ dòng phía sau** — `ITL#1234` hôm nay ≠ hôm qua. Đây là gốc của **1.356 dòng `FALSE`** ở cặp `ITL ID` vùng AUDIT *(không phải lỗi dữ liệu — là khoá tự đổi)*.
- **`No` rỗng khi `Mapping Master` thiếu tài khoản** *(cột `AG`/`LE` rỗng)* ⇒ `itl_id = "ITL#" & ""` = **`ITL#`, mất khoá hoàn toàn**.

⇒ nhiều khả năng cũng là gốc của lớp lỗi remap đã đo ở hệ hiện hành (~17% lệch khi remap sai khoá).

⚠ **Sửa v0.3 (`QĐ-ITL-30` + `QĐ-ITL-43`):** câu dưới đây của v0.1 **đúng một nửa**. Đúng ở chỗ *số thứ tự theo VỊ TRÍ DÒNG* không được làm khoá. **Sai** ở chỗ suy ra rằng khoá phải là **khoá nội dung** — vì khoá nội dung đổi mỗi lần một trường nội dung được sửa, và ***mọi ô người gõ cùng mọi dòng nhật ký sẽ rời khỏi dòng của nó**. ⇒ Lời giải là **hai khoá** (`INV-I04a` danh tính = số thứ tự **cấp khi vào sổ rồi đóng băng**, khác hẳn *số thứ tự theo vị trí dòng*; `INV-I04b` khoá nội dung **chỉ để đối sánh**). Đo kèm: **281 dòng trùng · 103 dòng không có số chứng từ · 31 dòng mã rác `4.36619E+15`** ⇒ khoá nội dung **một mình không đủ làm danh tính**.

~~⇒ **TO-BE không được dùng số thứ tự chạy làm khoá.**~~ ~~`ITL ID` phải là **composite ổn định** suy từ nội dung giao dịch.~~ ⚠ **SỬA v0.5:** câu gạch trên **vẫn sai** — nó gộp danh tính vào khoá nội dung. Đúng là **hai khoá tách hẳn**: `itl_id` *(danh tính)* = **số thứ tự cấp một lần khi dòng vào sổ rồi đóng băng** *(`INV-I04a`)*, **không** suy từ nội dung; còn composite nội dung là **`INV-I04b`, chỉ để đối sánh**. Số thứ tự hiển thị (`No`) giữ làm nhãn cho người đọc, không phải khoá.

★ **Cú lật thứ tự — điểm mấu chốt của TO-BE:**

| | AS-IS | TO-BE |
|---|---|---|
| **Danh tính cấp khi nào** | **SAU mapping** *(ở `Transaction Mapping L1`, bám vị trí dòng đã SORT)* | **TRƯỚC mapping** *(cấp lúc nạp — trạng thái `staged`, `09_STATE_MACHINE` SM-I01)* |
| **Mapping PM làm gì** | *sinh ra* `itl_id` như tác dụng phụ | chỉ **làm giàu** dòng đã có `itl_id`; dòng `unmapped` vẫn giữ khoá |

Việc chốt đúng tập trường tạo **khoá đối sánh `INV-I04b`**: `BA-05` §ITL ID — và phải test bằng oracle (chạy 2 lần, chèn dòng giữa, `itl_id` cũ không đổi).

## Ghi chú thiết kế — lineage PM phải sống sót vào canon (`INV-I05`)

**Phát hiện từ file thật** *(`FLS-Process-PM-den-ITL` §5)*: phép ghép ở `Transaction Mapping L1` *(chặng 7)* kéo 38 cột, nhưng `ITL Ledge` *(chặng 8)* **chỉ giữ 8 dải** ⇒ **12 cột định danh phiếu bị rơi**, gồm `N ID PMLine`, `M ID PMSlip`, `L Pháp nhân thanh toán`. Công gõ `Reference number` được dùng **một lần** để lấp `HDCode`/`CDT1`/đối tác, rồi **khoá bị bỏ đi** — từ `ITL Ledge` trở đi *(kể cả engine)* **không còn đường lần về PM**.

⇒ **TO-BE bắt buộc** *(`QĐ-ITL-20`, hẹp bởi `CR#1`)*: `ITL-CANON` phải mang **`pm_line_id`** *(= `fps_pm_line.line_id` — khoá bền mức LINE)* và **`le_payer`** *(← `fps_pm_slip.payer_id`)* làm cột lineage, để mọi báo cáo nội bộ + drill-through về phiếu **không phải dựng lại từ đầu**. Đây là mở rộng lineage **ngoài** 14 trường `ITL-CONTRACT`, không chặn cutover.

## Ghi chú — `INV-I01` và bẫy "phồng số"

Đo bảo toàn tiền bằng **cộng dồn cả bảng** sẽ làm số phồng do rollup chồng. Cách đo đúng: **net theo output-sheet**. Đây là rủi ro #2 của dự án (`ORC-01` `P-ITL-03`).

## Quan hệ với vùng AUDIT hiện hành

Vùng AUDIT của `ITL Ledge` đang tự báo **6.711 dòng lệch** (`FALSE`: 1356 · 552 · 146 · 2310 · 2308 · 39) khi đối chiếu ngược `Report I General Ledger`. Bộ bất biến trên là để **những dòng đó không sinh ra được nữa**. Còn 6.711 dòng cũ là lỗi dữ liệu hay lỗi công thức audit: `GAP-ITL-11`, chưa đóng — và nó ảnh hưởng trực tiếp tới độ tin của oracle.

## Changelog
- **v0.8** *(2026-09-04, `QĐ-ITL-88·89`)*: ⭐⭐ **`INV-I19` — một tín hiệu chỉ đáng giá bằng độ HIẾM của nó ⇒ phải ĐO TẦN SỐ trước khi bật.** Sinh ra từ hai phép đo cùng ngày: `chưa phân loại` chạm **76,6%** cuốn sổ mà đang được vẽ bằng **ngôn ngữ báo động**; và `US-032` như bản thiết kế viết thì báo trên **13,0%**. ⇒ Cả hai đều ⛔ **không phải** báo động — chúng là **trạng thái bình thường bị vẽ sai loại**, và chúng làm **mọi** báo động khác nhạt đi. ⚠ Cùng luật ấy áp cho **ký hiệu**: dấu `⛔` dùng **111** lần trên một màn thì ⛔ không còn là tín hiệu.
- **v0.7** *(2026-09-04, `QĐ-ITL-83·86·87`)*: ⭐⭐ **Hai bất biến MỚI, cả hai sinh ra từ một lỗ thật vừa vá.** `INV-I17` **bản khai RỖNG = máy ⛔ KHÔNG BIẾT** — ⛔ chứ không phải *"mọi giá trị đều sai"*; chặn hết vì bản khai chưa nạp là cái máy nói **"sai"** trong khi ý nó là **"tôi ⛔ không biết"**, và người dùng ⛔ không có cách nào phân biệt. Đây là `INV-I16` soi từ **phía ngược lại**: `I16` cấm máy **bịa một câu trả lời**, `I17` cấm máy **bịa một lời từ chối**. `INV-I18` **phép kiểm ⛔ không được VÒNG TRÒN** — một danh sách suy từ chính dữ liệu đang có thì ⛔ không được làm luật cưỡng chế cho dữ liệu ấy: nó sẽ ⛔ không bao giờ **lớn được**, và mọi dòng **bẩn sẵn có thành luật**.
- **v0.6 (2026-08-26, sau khi chạy P0): `INV-I03` và `INV-I04a` từ mong muốn → CƯỠNG CHẾ THẬT.** Trigger `trg_fls_itl_inv_i03` *(chặn cả `UPDATE` và `DELETE`)* + `trg_fls_itl_inv_i04a`, 5 test trên **PG 16 container** *(`tests/db/test_invariants_pg.py`)*, không dùng sqlite giả. `INV-I04b` được `content_key UNIQUE` chặn ở DB. ⚠ **Sửa `INV-I04a`**: bỏ *"sinh atomic theo pattern `fps_id_counter`"* → **`SEQUENCE`**; câu cũ đọc ngược bài học FPS *(bảng counter chính là chỗ từng sinh id trùng — `GAP-PLAN-02`)*.
- **v0.5 (2026-08-25):** Rà lại thứ tự danh tính *(`FLS-Process-PM-den-ITL` §3·§5)*. **Sửa ghi chú `INV-I04`**: bỏ hẳn câu "itl_id = composite nội dung" *(mâu thuẫn `INV-I04a`)*; nêu **cơ chế AS-IS** *(`itl_id="ITL#"&No`, `No=ROW()` trên bảng SORT theo ngày ⇒ sinh SAU mapping, bám vị trí dòng)* + hai đường mất-ổn-định *(1.356 `FALSE`; `No` rỗng ⇒ `ITL#` mất khoá)* + **cú lật AS-IS↔TO-BE** *(danh tính cấp TRƯỚC mapping ở `staged`)*. Thêm **ghi chú lineage `INV-I05`**: `pm_line_id` + `le_payer` phải sống sót vào canon *(khoá PM bị vứt ở chặng 8 — `QĐ-ITL-20`/`CR#1`)*.
- **v0.4 (2026-08-24, chiều): `INV-I15` ĐÓNG** — không phải *"chưa đo được"* như v0.3 ghi. Owner đã chốt **cột `P` là SSOT** từ 2026-08-20 sau khi đo `BL` mục ruỗng ba tháng; engine đã đổi. Có 2 file test cưỡng chế.
- **v0.3 (2026-08-24): tách `INV-I04` → `INV-I04a` (danh tính: `itl_id` số thứ tự đóng băng) + `INV-I04b` (đối sánh: khoá nội dung `UNIQUE`)** theo `QĐ-ITL-30`/`QĐ-ITL-43` — sửa suy luận sai của v0.1. Thêm **`INV-I15`** *(hai cột pháp nhân `P` = `BL`, chưa đo được, kèm đường đo đã tìm ra)* và **`INV-I16`** *(máy không được tự trả lời thay người)*. **`INV-I07` diễn giải lại** theo `QĐ-ITL-42`: `POS-13` chỉ áp khi nguồn còn là Sheet. Thêm mục **4 bất biến nghiệm thu `ACC-1..4`** cho việc dựng-lại-từ-nguồn (`QĐ-ITL-41`) — **cấm viết dung sai**.
- v0.2 (2026-08-19): `INV-I02` ghi rõ **A-CCR sở hữu** phép đối soát số dư (`QĐ-ITL-18`); ITL đọc kết quả, không tự tính lại.
- v0.1 (2026-08-18): Khởi tạo — 14 bất biến, mỗi cái có tầng enforce. Phát hiện từ file thật: **ITL ID AS-IS là số thứ tự chạy** (`ITL#n`) ⇒ không ổn định, TO-BE bắt buộc composite.
