# _DOC_REWRITE_ROADMAP — Lộ trình viết lại bộ tài liệu dự án ITL

**Version:** v0.4 | **Chủ sở hữu:** COO-CFO | **Ngày:** 2026-08-18
**Phạm vi lộ trình:** `01_Orchestrator/` → `02_BA/` (Dev/Test hoãn theo JIT, xem §7)
**Trạng thái:** ✅ **S0** · ✅ **S1** (8 file Orchestrator) · ✅ **S2** (7 file BA lõi, đọc từ 12 workbook thật) · ⏭ tiếp theo: **S3 BA JIT**

> Đây là **kế hoạch viết lại**, không phải file SSOT.
> Phương pháp kế thừa precedent A-CCR (`../A-CCR/02_BA/_BA_REFACTOR_PLAN.md`): **giữ khung, tái dẫn xuất nội dung từ dữ liệu thật, không churn ID.**

---

## §0 · Dự án ITL là gì (một câu)

> **Số hoá toàn bộ luồng tài liệu và thao tác kế toán từ `P100` đến `ITL Ledge`** — thay sổ Google Sheets đang chạy tay bằng pipeline code hoá, để **engine P&L hiện tại đọc thẳng ITL mới mà không sửa một dòng code**.

Ba con số định nghĩa bài toán (từ `FS2-Architecture-Review.md`, đọc từ `AS-IS system/FS2 PD Now.xlsx`):

| Số | Ý nghĩa |
|---|---|
| **116 bước · 43 đối tượng · 31 luồng** | quy mô luồng AS-IS đang vận hành trên Google Sheets |
| **62% bước còn thủ công** | 72/116 bước = "kế toán nhấn nút / nhập tay / chạy Gscript" |
| **~6.843 dòng nhập tay** | vùng ADJUSTMENT của `ITL Ledge`, 2 người gõ (khối 297·179·1210·22·22·1624·3489) — nghẽn cổ chai lớn nhất |

**Quan hệ với chương trình FIN ERP:** ITL là **sub-project** (như A-CCR), không phải chương trình song song. Nó hiện thực hoá tầng **L2 CANONICAL SPINE** của kiến trúc 5 tầng — mắt xích mà `FS2-Architecture-Review` §04 gọi là "xương sống thật" của cả hệ.

---

## §1 · Năm luật viết lại (áp cho mọi file)

| # | Luật | Vì sao |
|---|---|---|
| **W1** | **Giữ khung, đổi nội dung.** Giữ đúng 34 file, đúng tên file, đúng prefix ID, đúng R-A1..R-A5. Không thêm/bớt file (trừ `ORC-08`, xem S1). | Đội đã quen; churn cấu trúc = mất truy vết, đúng bài học A-CCR |
| **W2** | **Độc lập + chốt kế thừa có version** (đổi ở v0.2 theo `QĐ-ITL-04`). Bộ ITL **tự chứa** mọi nội dung, kể cả phần kế thừa (P-01..P-08, ĐK1–ĐK10, QĐ-VOI, G/Q, R-A1..A5) — không tham chiếu chéo sang `0. Standard Documentation/`. **Bù lại, bắt buộc:** mỗi khối kế thừa ghim version nguồn trong bảng `00_MASTER_INDEX §5`, và `ORC-07` bắt mở CR rà lại khi bản chương trình tăng version. | Owner chốt "đọc một chỗ là đủ". Nhưng 2 bản cùng nội dung **sẽ** trôi — ghim version là cơ chế duy nhất biến trôi âm thầm thành trôi phát hiện được (tránh bẫy R-A4) |
| **W3** | **Tái dẫn xuất từ dữ liệu thật, không từ trí nhớ.** Mọi bảng trường/luật/khối lượng phải trace về sheet thật trong 10 file `Input_Raw/Reference/Accounting_Files` hoặc `FS2 PD Now.xlsx`. | Bài học `apr-code-old-wrong-value-column`, `itl-altered-composite-key-fix` |
| **W4** | **Contract-first trong tài liệu.** File đầu tiên có nội dung thật phải là **ITL Ledge Output Contract** (36 cột canonical + 4 vùng). Mọi file sau khớp hợp đồng đó. | `BuildPlan §0`: lệch hợp đồng = cutover gãy. Rủi ro #1 |
| **W5** | **JIT — chỉ viết chi tiết cho IM0–IM2.** IM3–IM7 giữ mức khung + `???`. AI không tự điền `???`. | P-08 + R-A1 |

---

## §2 · Trạng thái đầu vào — phân loại 34 file

`diff -rq "0. Standard Documentation" "FIN-ERP_Project/ITL"` → **không lệch một byte**. Toàn bộ 34 file đang là nội dung **chương trình FIN ERP**, chưa có chữ nào về ITL. Ba cách xử lý:

| Xử lý | Nghĩa | Số file |
|---|---|---|
| **✅ DONE** | Đã viết lại ở S0 | 1 (`00_MASTER_INDEX`) |
| **🔁 REWRITE** | Viết lại nội dung theo scope ITL, tự chứa (W2), giữ khung | 20 + 1 mới = **21** |
| **⏸ HOLD** | Giữ bản copy, **đã dán banner `⏸ chưa dẫn xuất cho ITL`**, viết sau `G-DOC-3` | 13 (Dev 9 + Test 4) |

> v0.2: hạng mục `🔗 THIN+LINK` **bị xoá** — `QĐ-ITL-04` chọn bộ độc lập, nên 7 file định trỏ về program giờ viết đầy đủ tự chứa (có ghim version kế thừa).
> Banner `⏸` đã dán vào **33 file** (mọi file trừ `00_MASTER_INDEX` và file này) — gỡ dần khi từng file được viết lại.

> **Cập nhật v0.4:** 16 file đã ✅ xong — `00_MASTER_INDEX` + `ORC-00..08` (S0+S1) + `BA-00/01/02/04/05/09/10/11` (S2). Còn `BA-03/06/07/08` (S3) và Dev 9 + Test 4 (HOLD).

| File | Xử lý | Ghi chú |
|---|---|---|
| `00_MASTER_INDEX.md` | ✅ | **XONG S0** — danh tính ITL, QĐ-ITL-01..04, namespace, 6 nguồn, chốt kế thừa có version, 5 luật R-A |
| `ORC-00_README` | 🔁 | Vai bộ Orchestrator cho ITL; khác biệt: cổng = **đối soát oracle**, không phải go-live-thay-Excel chung |
| `ORC-01_PRINCIPLES` | 🔁 | Chép P-01..P-08 (ghim program v0.1) + **thêm P-ITL-01..05** (§S1) |
| `ORC-02_VERSION_ORCHESTRATION` | 🔁 | Trục version đổi hẳn: pin **Output Contract** + canonical schema + Mapping Master, không pin 3 kit |
| `ORC-03_PRODUCT_LIFECYCLE` | 🔁 | Thay GĐ0–GĐ5 bằng **IM0–IM7** + cổng đối soát oracle |
| `ORC-04_DEVELOPMENT_LOOP` | 🔁 | Vòng lặp theo **adapter**, không theo story; golden-run vs oracle |
| `ORC-05_ROLES_HANDOFF` | 🔁 | Vai thật của luồng kế toán (Data/SHQ1/SHQ2/HR, PIC vùng ADJUSTMENT) |
| `ORC-06_DASHBOARD` | 🔁 | Trạng thái ITL thật (§S1) — hiện đang là ảnh chụp chương trình ngày 2026-07-20, lệch 1 tháng |
| `ORC-07_CHANGE_CONTROL` | 🔁 | Thêm 2 đường: **CR chạm Output Contract** = loại nặng nhất, buộc test tương thích engine · **CR trôi kế thừa** (bản chương trình tăng version → rà bảng ghim `00 §5`) |
| `ORC-08_MIGRATION_ROADMAP` | ➕ MỚI | Bản đồ di trú `Brainstorming/` + `AS-IS system/` vào kit (theo mẫu A-CCR ORC-08) |
| `BA-01_BRD` | 🔁 | Goal/scope/KPI của ITL |
| `BA-02_PROCESS_FLOW` | 🔁 | AS-IS 116 bước/6 pha → TO-BE 5 tầng L0–L5 |
| `BA-05_DATA_DICTIONARY_ERD` | 🔁 | **File nặng nhất**: 36 cột canonical + Mapping Master + ITL Ledge 4 vùng |
| `BA-09_STATE_MACHINE_SPEC` | 🔁 | Vòng đời dòng ITL + bút toán điều chỉnh + run/batch + chốt kỳ |
| `BA-10_DECISION_TABLE` | 🔁 | Luật chuẩn hoá LE, parse ngày, khử trùng, Need/Method allocate, cash-vs-accrual |
| `BA-11_INVARIANTS` | 🔁 | Bất biến tiền/append-only/lineage/hợp đồng |
| `BA-00_README` | 🔁 | Cập nhật độ chín + thứ tự soạn thảo cho ITL; chép chuỗi truy vết + prefix ID mới (`US-8xx`, `DD-Ix`…) |
| `BA-03_USER_STORY` | 🔁 (JIT) | Chỉ IM0–IM2 chi tiết; IM3–IM7 khung |
| `BA-04_ROLE_PERMISSION_MATRIX` | 🔁 | SoD tạo–duyệt điều chỉnh ITL |
| `BA-06_SCREEN_SPEC` | 🔁 (JIT) | 4 màn hình lõi (§S3) |
| `BA-07_API_CONTRACT` | 🔁 (JIT) | Chép quy ước API chung + endpoint ITL theo IM0–IM2 |
| `BA-08_NFR` | 🔁 | Khối lượng/thời gian chạy/idempotency/cửa sổ reprocess — đo được |
| `03_Dev/*` (9), `04_Test/*` (4) | ⏸ | HOLD tới sau cổng BA-DoD (§7) |

---

## §3 · Nguồn dẫn xuất bắt buộc (không được viết ngoài 6 nguồn này)

| Ký hiệu | Nguồn | Cung cấp gì |
|---|---|---|
| `NGUỒN-ASIS` | `AS-IS system/FS2-Architecture-Review.md` + `FS2-DataFlow.html` | AS-IS 116 bước, 5 tầng sạch, kill list, từ điển thuật ngữ, bảng điểm |
| `NGUỒN-XLSX` | `AS-IS system/FS2 PD Now.xlsx` | Bản gốc — **chỉ đọc, không sửa** |
| `NGUỒN-BUILD` | `Brainstorming/3_Lo_trinh/BuildPlan_P100_to_ITL.md` | IM0–IM7, adapter A–F, dây chuyền S1–S5, 36 cột, 4 vùng, §8 nghiệm thu |
| `NGUỒN-TOBE` | `Brainstorming/2_Kien_truc/Kien_truc_TO-BE.md` | Kiến trúc đích + 6 tầng L0–L5 + 7 trụ A–G |
| `NGUỒN-FILES` | **12 workbook thật** `AS-IS system/Accounting_Files/RAW` | Cấu trúc sheet thật + **test oracle** (ITL RAW & ITL ADJUSTED cũ) |
| `NGUỒN-PROG` | `0. Standard Documentation/` (34 file) | Hiến pháp chương trình — trỏ, không chép (W2) |

⚠ **Cảnh báo dữ liệu đã biết, phải mang vào doc chứ không được để AI phát hiện lại:** bản `.xlsx` export phá huỷ ngày (chỉ 2,7% ô ngày nguyên vẹn) · ITL "Ngày chứng từ" hoán ngày↔tháng ~93% dòng · ~5.369 dòng ngày dạng chuỗi → UNMAPPED · `ITL_altered` map sai 680 HD + 1048 CDT. Đọc GS live qua Sheets API, **không** đánh giá bằng file offline.

---

## §4 · Lộ trình 4 sóng

```
S0 Danh tính & namespace  ──>  S1 Orchestrator (8 file)  ──>  S2 BA lớp 1+4 (lõi)  ──>  S3 BA lớp 2+3 (JIT)
   1 phiên                      3 phiên                        4 phiên                   4 phiên
   cổng: owner chốt 3 QĐ        cổng: IM0–IM7 + dashboard      cổng: hợp đồng đóng băng  cổng: BA-DoD → mở Dev/Test
```

Effort tính bằng **phiên AI** (1 phiên = 1 file hoặc 1 cụm file, reset context giữa các phiên — P-07), không phải tuần.

### S0 · Danh tính & namespace — ✅ **XONG** (2026-08-18)

Owner đã chốt 4 quyết định nền:

| QĐ | Quyết định | Ghi chú |
|---|---|---|
| **QĐ-ITL-01** | Namespace `US-8xx` · `SCR-I0x` · `DD-Ix` · `DT-Ixx` · `INV-Ixx` · `GAP-ITL-xx` · `QĐ-ITL-xx` | A-CCR đã chiếm dải `7xx`/`*-Ax` |
| **QĐ-ITL-02** | Milestone ITL đổi `M0–M7` → **`IM0–IM7`** trong toàn bộ tài liệu ITL | Dứt loạn ký hiệu M; gặp `M0–M7` ở `NGUỒN-BUILD` thì đọc là `IM` |
| **QĐ-ITL-03** | AP/AR (adapter F) thuộc ITL, **gói riêng, không chặn cutover IM7** | Rủi ro #3 không nằm trên đường tới hạn |
| **QĐ-ITL-04** | Bộ tài liệu ITL **độc lập hoàn toàn**, tự chứa phần kế thừa | Đổi luật W2; bù bằng **chốt kế thừa có version** (`00 §5`) |

**Đã làm:** `00_MASTER_INDEX.md` viết lại (danh tính · phạm vi IN/OUT · decision log · quy ước ký hiệu IM/adapter/S1–S5/L0–L5 · chốt kế thừa 6 khối có ghim version · 6 nguồn dẫn xuất · 4 nợ dữ liệu đã biết · 5 luật R-A · chuỗi truy vết) · dán banner `⏸` vào **33 file** còn lại · lộ trình này lên v0.2.

**Còn nợ ở S0:** không. `GAP-ITL-01` đóng bởi `QĐ-ITL-01/02`; phát sinh `GAP-ITL-08` (nhịp rà trôi kế thừa) chuyển sang S1.

### S1 · Orchestrator — ✅ **XONG** (2026-08-18, 8 file v0.1)

**Đã giao:** `ORC-00` vai bộ + 2 khác biệt so với chương trình · `ORC-01` chép `P-01..P-08` (ghim program v0.1) + **`P-ITL-01..05`** · `ORC-02` **đổi trục version sang 3 hợp đồng dữ liệu** (`ITL-CONTRACT` / `ITL-CANON` / `MAPPING-MASTER`) + 2 điều kiện đóng băng riêng + manifest theo IM · `ORC-03` **`IM0–IM7`** 8 cổng đo được + thang nghiệm thu oracle 7 bước + 8 bẫy có số thật + 3 điều kiện vào · `ORC-04` vòng trong **theo adapter** (6 bước) + 7 luật pipeline tài chính + vòng lặp riêng cho vùng ADJUSTMENT · `ORC-05` **bảng "ranh giới hệ thống đang là con người"** (5 mắt xích phải xoá theo milestone) + RACI theo 3 hợp đồng + 3 việc verify trước khi tin handoff · `ORC-06` dashboard trạng thái **thật** (5 hệ nền đang chạy, 5 nợ dữ liệu, 9 GAP, nhật ký handoff) · `ORC-08` **MỚI** bản đồ 19 nguồn → file kit + 4 bước di trú + 3 mâu thuẫn nguồn.

**Phát sinh:** `GAP-ITL-09` — mâu thuẫn ưu tiên với chiến lược VALUE-FIRST (chặn `IM0`, không chặn viết doc). Còn **13 ô `???`**, trong đó 5 ô là chỉ định nhân sự ở `ORC-05`.

<details><summary>Kế hoạch gốc của S1 (đã thực hiện)</summary>

| Phiên | File | Nội dung phải có |
|---|---|---|
| **1.1** | `ORC-01`, `ORC-02`, `ORC-07` | **P-ITL-01 Contract-first** (đóng băng Output Contract trước mọi code) · **P-ITL-02 Strangler-fig** (chạy song song Gsheet, cắt ở IM7) · **P-ITL-03 Oracle-first** (nghiệm thu bằng đối chiếu từng dòng với ITL RAW/ADJUSTED cũ) · **P-ITL-04 Append-only** (điều chỉnh là bút toán thêm, RAW bất biến) · **P-ITL-05 Không phát minh schema** (dùng đúng 36 cột `Transaction Mapping L1`). `ORC-02`: trục version = Output Contract vX + canonical schema vX + Mapping Master vX. `ORC-07`: thêm đường CR-chạm-hợp-đồng |
| **1.2** | `ORC-03`, `ORC-04` | `ORC-03`: bảng **IM0–IM7** (3 phần A/B/C, IM2–IM5 song song) × cổng thoát × người nghiệm thu — cổng lấy nguyên văn `NGUỒN-BUILD §8` (7 bước nghiệm thu bám số thật) + 4 bẫy. `ORC-04`: vòng lặp **theo adapter** — adapter → DQ test row-count → đối soát vs oracle → merge; luật "0 dòng rơi im lặng" |
| **1.3** | `ORC-05`, `ORC-06`, `ORC-08` | `ORC-05`: ranh giới hệ thống AS-IS là **con người** (Data/SHQ1/SHQ2/HR) → khai báo rồi thay dần bằng interface; PIC vùng ADJUSTMENT phải ký. `ORC-06`: **trạng thái ITL thật** — engine FPA-T4 đã đọc `ITL_altered`, A-CCR ở P3.2, 3 nợ dữ liệu ngày, `ITL_altered` rebuild 116 dòng COC. `ORC-08`: di trú `Brainstorming/` + `AS-IS system/` → kit |

**DoD:** IM0–IM7 có cổng đo được; `ORC-06` phản ánh đúng ngày viết, không phải ảnh chụp 2026-07-20. → **ĐẠT.**

</details>

### S2 · BA lớp 1 + 4 — ✅ **XONG** (2026-08-18, 7 file v0.1)

**Đã giao:** `BA-01` bài toán 3 con số + **giải mã 7 khối nhập tay** + 5 goal + 7 KPI · `BA-02` AS-IS 6 pha → TO-BE 5 tầng + S1–S5 + chu trình vận hành · `BA-09` **5 máy trạng thái** (`SM-I02` dẫn xuất trực tiếp từ khuôn 4 cột có thật) · `BA-11` **14 bất biến**, mỗi cái có tầng enforce · `BA-10` **9 bảng quyết định** + thứ tự áp bắt buộc + xếp hạng ROI 7 khối · `BA-04` 10 vai + ma trận 16 hành động + 3 SoD · `BA-05` **từ điển dữ liệu đầy đủ** đọc từ 12 workbook thật.

**5 phát hiện chỉ có được nhờ đọc file thật** (không có trong tài liệu nguồn nào): 7 khối nhập tay = 7 trường cụ thể · **6.711 dòng lệch vùng AUDIT** · `ITL ID` AS-IS là số thứ tự chạy (không ổn định) · 2 lệch schema thật (A-CCR đảo cột G/H; H1000 lệch Y/Z/AA/AL) · sổ đăng ký nguồn `RAW ITLData Management` đang `#REF!`.

**Phát sinh:** `GAP-ITL-10..16`.

**Cổng `G-DOC-2` CHƯA qua:** ứng viên `ITL-CONTRACT` đã đặc tả (`BA-05` §DD-I04) nhưng **chưa xác nhận với reader engine thật** (`GAP-ITL-16`) — đúng luật `ORC-02` §4: không đóng băng hợp đồng trên giấy.

<details><summary>Kế hoạch gốc của S2 (đã thực hiện)</summary>

#### S2 · BA lớp 1 + 4 — lõi hợp đồng — `4 phiên · dep: S1`

Theo đúng thứ tự soạn thảo mà `BA-00` đã quy định (`01+02 → 09+11 → 10+04 → 05`).

| Phiên | File | Nội dung phải có |
|---|---|---|
| **2.1** | `BA-01`, `BA-02` | `BA-01`: Goal ITL trace về `G-03` (số đáng tin) + `G-04`; scope **IN** = adapter A–F + S1–S5 + Output Contract + vùng ADJUSTMENT/ALLOCATE/AUDIT; **OUT** = viết lại engine P&L (ITL là *producer*, engine là *consumer* read-only), sổ thuế, OCR. KPI đo được: 62%→? thủ công · 6.843→0 dòng tay · % dòng khớp oracle · số kỳ chạy song song. `BA-02`: AS-IS 6 pha (ranh giới lẫn: Calculate/Allocate/Report cùng ghi 1 file) → TO-BE 5 tầng + luật **"L5 không được tạo số mới"** |
| **2.2** | `BA-09`, `BA-11` | `BA-09`: 4 máy trạng thái — (1) dòng ITL: `raw → mapped → adjusted → allocated → audited → locked`; (2) bút toán điều chỉnh: `draft → submitted → approved → posted → reversed`; (3) run/batch: `queued → running → dq_failed → reconciled → published`; (4) chốt kỳ. `BA-11`: `INV-I01` bảo toàn tiền (net theo output-sheet, **không** cộng dồn — rủi ro #2) · `INV-I02` A-CCR balance=0 theo ngày/tài khoản · `INV-I03` RAW bất biến · `INV-I04` ITL id unique + composite đúng · `INV-I05` mọi dòng có lineage source→ITL · `INV-I06` không dòng nào rơi im lặng · `INV-I07` Output Contract tương thích ngược |
| **2.3** | `BA-10`, `BA-04` | `BA-10`: bảng quyết định từ `Mapping Master` thật — chuẩn hoá LE (nguồn bẩn nhiều biến thể) · COA1/COA2 · 3 cột `Need to Allocate to CFA2` / `Method to Allocate to CFA2` / `Code HR Allocate` = mầm bảng luật L4 · parse ngày (gồm luật xử ngày hoán & ngày chuỗi) · khử trùng PE/PI vs Transaction Original · routing cash-vs-accrual. `BA-04`: SoD tạo–duyệt điều chỉnh ITL & treasury |
| **2.4** | `BA-05` | **File nặng nhất.** 36 cột canonical 5 nhóm BASE(7)/LINK/CLASS/SVC/PARTY — lấy **nguyên văn tên cột file thật** (R-A2) · `Mapping Master` · `ITL Ledge` 4 vùng (BASE+IMPORT A–Q / ADJUSTMENT R+ / ALLOCATE AU+ / AUDIT AX+) · bảng oracle · ERD RAW ↔ ADJUSTED ↔ journal điều chỉnh |

**Cổng S2 (quan trọng nhất cả lộ trình):** `BA-05` §36-cột + `ORC-02` được owner **đóng băng thành Output Contract v1.0**. Chưa đóng băng → không mở S3.

</details>

### S3 · BA lớp 2 + 3 — JIT cho IM0–IM2 — `4 phiên · dep: cổng S2`

| Phiên | File | Nội dung |
|---|---|---|
| **3.1** | `BA-03` | Epic theo adapter A–F + zone; story chi tiết **chỉ** IM0 (hợp đồng, canonical, Mapping Master versioned, DAG stub) + IM1 (lát dọc P100+Cash) + IM2 (dòng tiền + A-CCR gate). IM3–IM7 = 1 dòng epic + `???`. AC dạng Given/When/Then chạy được như test |
| **3.2** | `BA-06` | 4 màn hình lõi: (a) **nhập/duyệt bút toán điều chỉnh** — thứ thay 6.843 dòng gõ tay; (b) **DQ & reconcile board** (balance, row-count, match-rate LINK, `#N/A`); (c) **Mapping Master admin** có version + sign-off; (d) **lineage drill** source→ITL |
| **3.3** | `BA-07`, `BA-08` | `BA-07`: endpoint theo IM0–IM2. `BA-08`: khối lượng thật (60+ sheet bank, 108 sheet H1000, ~6.843 dòng adjustment), thời gian chạy trọn khối, idempotency, cửa sổ reprocess, fail-loud khi schema nguồn đổi |
| **3.4** | rà chéo | Truy vết `G → Q → US → SM/DT/INV/DD/SCR/API`; xuất `GAP_REPORT` các `???` còn mở kèm owner + cách đóng |

**DoD BA (chuẩn "spec xong", theo A-CCR):** mỗi US có AC chạy được như test · mỗi giá trị là số cụ thể (provisional có nhãn) HOẶC `???` kèm owner+nguồn+cách đóng · mỗi field màn hình trace 1 field `BA-05` · mỗi US trace về 1 IM · mỗi INV chỉ rõ tầng enforce.

---

## §5 · GAP-ITL mở ngay từ S0 (AI không tự đóng — R-A1)

| ID | Câu hỏi | Ai đóng | Chặn sóng nào |
|---|---|---|---|
| ~~`GAP-ITL-01`~~ | ~~Namespace ID + đổi `M0–M7` → `IM0–IM7`?~~ | **CLOSED 2026-08-18** — `QĐ-ITL-01/02` | — |
| `GAP-ITL-08` | Trôi kế thừa: `QĐ-ITL-04` chọn bộ độc lập ⇒ 6 khối nội dung tồn tại 2 bản. Ai rà bảng ghim `00 §5`, nhịp nào? | COO-CFO | S1 (`ORC-02`/`ORC-07`) |
| `GAP-ITL-09` ⚠ | **(MỚI, phát sinh ở S1)** Mâu thuẫn ưu tiên: chiến lược VALUE-FIRST (`Ban_do_Gia_tri_Quyet_dinh`, 2026-08-07) chốt **HOÃN code hoá L0–L2** — đúng phần việc của ITL. Mở ITL là đảo lại quyết định đó, hay ITL chạy nền sau? | **COO-CFO** | Chặn `IM0` (không chặn viết doc) |
| `GAP-ITL-02` | Google Sheets còn giữ vai **nhập liệu** sau cutover, hay thay bằng UI? Quyết định này định hình `BA-06` | Kế toán trưởng + COO | S3 |
| `GAP-ITL-03` | Ai ký duyệt bút toán điều chỉnh ITL sau khi code hoá (hiện là 2 PIC gõ tay, không có bước duyệt)? | Kế toán trưởng | S2 (`BA-04`/`BA-09`) |
| `GAP-ITL-04` | Ranh giới ITL ↔ A-CCR: adapter C chỉ **đọc** kết quả đối soát A-CCR, hay ITL dựng lại cổng đối soát? | COO-CFO | S2 |
| `GAP-ITL-05` | Nợ dữ liệu ngày (93% hoán ngày↔tháng, 5.369 dòng ngày chuỗi) — sửa **trong** dự án ITL hay là điều kiện tiên quyết do kế toán làm trước? | Kế toán trưởng + ThanhNC | S2 (`BA-10`) |
| `GAP-ITL-06` | Nghiệp vụ AP/AR (adapter F) chưa tồn tại — ai đặc tả? | COO-CFO | S3 (IM5, không chặn cutover) |
| `GAP-ITL-07` | Số tuyệt đối cho ngưỡng DQ fail-loud (bao nhiêu % lệch thì dừng pipeline)? | Diễn đàn QT | S2 (`BA-08`) |

---

## §6 · Cổng & người phê

| Cổng | Sau sóng | Tiêu chí | Ai ký |
|---|---|---|---|
| ~~**G-DOC-0**~~ | S0 | 4 quyết định danh tính chốt | ✅ **QUA** 2026-08-18 (COO-CFO) |
| ~~**G-DOC-1**~~ | S1 | IM0–IM7 có cổng đo được; `ORC-06` đúng thực tế | ✅ **QUA** 2026-08-18 (COO-CFO) |
| **G-DOC-2** | S2 | **Output Contract v1.0 đóng băng** + 7 INV enforce được ở tầng DB | COO-CFO + Kế toán trưởng |
| **G-DOC-3** | S3 | DoD BA đạt; `GAP_REPORT` có owner cho từng `???` | Kế toán trưởng (người vận hành nghiệm thu, P-02) |

---

## §7 · Việc KHÔNG làm trong lộ trình này

- **Không viết `03_Dev/` và `04_Test/`** — mở sau `G-DOC-3`. Viết trước = spec chết trên kệ (P-08); và Dev không thể viết trước khi Output Contract đóng băng.
- **Không sửa `AS-IS system/FS2 PD Now.xlsx`** — bản gốc chỉ đọc.
- **Không sửa `0. Standard Documentation/`** — mọi thay đổi chương trình đi qua `ORC-07` bằng CR riêng.
- **Không viết code** — lộ trình này thuần tài liệu.
- **Không viết chi tiết IM3–IM7** (HR, Platform, AP/AR, Aggregate, Cutover) ở sóng này.

---

## §8 · Hai điểm cần owner biết trước khi duyệt

1. **Rủi ro trôi kế thừa — owner đã chọn và đã chấp nhận.** `QĐ-ITL-04` chốt bộ ITL độc lập, nên 6 khối nội dung (P-01..P-08, ĐK1–ĐK10, R-A1..A5, G/Q, QĐ-VOI, vai+RACI) tồn tại **2 bản**: một ở `0. Standard Documentation/`, một trong bộ này. Đây là rủi ro thật, không phải giả định: hôm nay 33/34 file còn giống hệt từng byte bản chương trình. Cơ chế kiểm soát duy nhất là **bảng ghim version ở `00_MASTER_INDEX §5`** + đường CR "trôi kế thừa" ở `ORC-07` + nhịp rà (`GAP-ITL-08`, chờ owner chốt ở S1). Nếu bảng ghim không được rà, R-A4 sẽ nổ vào ngày một bên sửa mà bên kia không.

2. **Dự án này không bắt đầu từ 0.** FPA-T4 **đã** đọc `ITL_altered` và xuất P&L thật; A-CCR đã xong BE P3.2. Nghĩa là một phần IM1/IM2 đã có tiền lệ chạy được, và Output Contract phải reverse-engineer từ **reader đang chạy thật**, không phải thiết kế mới. `ORC-06` phải ghi rõ điều này, nếu không phiên AI sau sẽ dựng lại thứ đã có.

## Changelog
- v0.4 (2026-08-18): **S2 xong** — 7 file BA lõi v0.1, dẫn xuất từ 12 workbook thật. Mở `GAP-ITL-10..16`. `G-DOC-2` chưa qua (chờ `GAP-ITL-16` xác nhận reader engine).
- v0.3 (2026-08-18): **S1 xong** — 8 file Orchestrator v0.1 (`ORC-08` là file mới). `G-DOC-1` qua. Mở `GAP-ITL-09` (mâu thuẫn ưu tiên VALUE-FIRST, chặn `IM0`).
- v0.2 (2026-08-18): **S0 xong.** Owner chốt `QĐ-ITL-01..04`. Đổi luật **W2** (độc lập + chốt kế thừa có version) theo `QĐ-ITL-04` ⇒ xoá hạng mục `🔗 THIN+LINK`, 7 file chuyển sang `🔁` tự chứa. Đóng `GAP-ITL-01`, mở `GAP-ITL-08` (nhịp rà trôi kế thừa). Dán banner `⏸` 33 file.
- v0.1 (2026-08-18): Khởi tạo — 4 sóng (S0→S3), 12 phiên, 7 GAP-ITL, 4 cổng G-DOC.
