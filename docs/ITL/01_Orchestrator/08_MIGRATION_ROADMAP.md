# 08 — MIGRATION ROADMAP: di trú tài liệu nguồn vào kit ITL

**Version:** v1.0 · **Cập nhật:** 2026-09-03 | **Chủ sở hữu:** COO-CFO

File này trả lời một câu: **nội dung nào của `Brainstorming/` và `AS-IS system/` đi vào file nào của kit, và cái gì ở lại làm nguồn.**

**Luật nền:** tài liệu nguồn **không bị xoá, không bị sửa** — chúng ở lại làm lớp nguồn (`../00_MASTER_INDEX §6`). Kit là bản **dẫn xuất có ID + version**; nguồn là bản **thảo luận**. Hai thứ khác vai, không thay nhau.

> ⚠ **Đính chính framing (2026-08-24)** — chỗ nhắc `ITL Ledge` "4 vùng + ~6.843 dòng nhập tay" phản ánh khung cũ. Đã chốt: `ITL Ledge` = **64 cột, 4 vùng** *(BASE+IMPORT · ADJUSTMENT · ALLOCATE · AUDIT)*; **ALLOCATE máy suy từ `Mapping Master`**; hợp đồng ra = **14 trường theo TÊN**. Chi tiết: [`_BA_UPDATE_ROADMAP §3c`](../02_BA/_BA_UPDATE_ROADMAP.md).

---

## 1. Bản đồ di trú

| Nguồn | Nội dung | Đi vào file kit | Sóng |
|---|---|---|---|
| `FS2-Architecture-Review.md` §00–02 | 116 bước · 62% thủ công · 5 nguồn domain · 2 làn CFA/PLA trên cùng sổ | `BA-01` (bài toán), `BA-02` (AS-IS) | S2 |
| `FS2-Architecture-Review.md` §02–03 | 5 tầng L0–L5 · ánh xạ 6 pha AS-IS → 5 tầng · ranh giới lẫn Calculate/Allocate/Report | `BA-02` (TO-BE) | S2 |
| `FS2-Architecture-Review.md` §04–05 | Mạnh/yếu · bảng điểm 8 tiêu chí | `BA-01` §bối cảnh + `06` §nợ | S2 |
| `FS2-Architecture-Review.md` §06 kill list | 309 Mapping L2 (huỷ) · 319 ITL Aggregate (huỷ) · 103/104 GI/OMC legacy · 601 · 507–510/615 dính FS1 · template 607–611 trùng | `03` `IM6`/`IM7` (dọn kill-list) + `BA-01` §OUT | ✅ S1 (một phần) |
| `FS2-Architecture-Review.md` §07 | Từ điển thuật ngữ (ITL, CFA, PLA, PE/PI/PM/PC, HD/KRF, CDT, LE, NOEM, MID, ASD, PD5xx…) | `BA-05` §từ điển | S2 |
| `FS2-DataFlow.html` | Sơ đồ tương tác 116 bước | Giữ nguyên làm nguồn tra cứu; `BA-02` trỏ tới | — |
| `BuildPlan_P100_to_ITL.md` §0, §X | Contract-first · strangler-fig · 5 trụ xuyên suốt | ✅ `01` (`P-ITL-01..05`), `04` §3 | ✅ S1 |
| `BuildPlan_P100_to_ITL.md` §1, M0–M7, §8 | 8 milestone · cổng · nghiệm thu 7 bước · bẫy | ✅ `03` toàn bộ | ✅ S1 |
| `BuildPlan_P100_to_ITL.md` §2 | 10 file nguồn thật → vai trò | ✅ `../00_MASTER_INDEX §6` + `BA-05` §nguồn | S2 |
| `BuildPlan_P100_to_ITL.md` §3 | **36 cột canonical** 5 nhóm | `BA-05` §`ITL-CANON` — **hạng mục quan trọng nhất** | S2 |
| `BuildPlan_P100_to_ITL.md` §4 | `Mapping Master` — cột điều khiển | `BA-05` §`MAPPING-MASTER` + `BA-10` (luật) | S2 |
| `BuildPlan_P100_to_ITL.md` §5 | `ITL Ledge` 4 vùng + ~6.843 dòng nhập tay | `BA-05` §layout + `BA-06` (màn hình) + `04` §4 | S2–S3 |
| `BuildPlan_P100_to_ITL.md` §6 | 6 adapter A–F + gotcha từng nguồn | `BA-03` (epic theo adapter) + `BA-10` | S3 |
| `BuildPlan_P100_to_ITL.md` §7 | Dây chuyền S1–S5 + Done từng bước | `BA-09` (state machine) + `BA-11` (invariant) | S2 |
| `Kien_truc_TO-BE.md` (chính) | Stack chốt PG/BQ · 2 mặt phẳng | `DEV-01` | HOLD |
| `Kien_truc_TO-BE.md` Phụ lục A | 6 tầng + 7 trụ trung lập công nghệ | `BA-02` §TO-BE + `BA-08` (trụ DQ/lineage/observability) | S2–S3 |
| `Blueprint_va_Phuong_phap_luan.md` Phần 0 | 10 điều kiện quản trị ĐK1–ĐK10 | `BA-01` (phần liên quan ITL) + `BA-11` | S2 |
| `AS-IS system/Accounting_Files/_LOGIC_Flow-Tinh-PnL-tu-Ledger.md` | Logic 3 ledger GI/OMC/PS → 3 dòng P&L; Source→CFA1→CFA2/MID→GL | `BA-02` + `BA-10` (routing) | S2 |
| `AS-IS system/Accounting_Files/_TRACE_VD341-xuyen-suot.md` | Trace một chứng từ xuyên hệ | `TEST-02` (test case mẫu) | HOLD |
| `NGUỒN-FILES` (12 workbook kế toán thật) | Cấu trúc sheet thật + **oracle** | `BA-05` (mọi tên trường lấy nguyên văn từ đây — R-A2) | S2 |

## 2. Bốn bước di trú

| Bước | Việc | Trạng thái |
|---|---|---|
| **1** | Khai báo lớp nguồn + luật "trỏ, không chép nội dung thảo luận" | ✅ xong (`../00_MASTER_INDEX §6`) |
| **2** | Di trú phần **điều phối** (nguyên tắc, milestone, cổng, vai) | ✅ xong (sóng S1 — bộ này) |
| **3** | Di trú phần **spec nghiệp vụ** (36 cột, Mapping Master, 4 vùng, adapter, luật) | ◐ **S2 xong** (`BA-01/02/04/05/09/10/11`); còn story/màn hình/NFR ở S3 |
| **4** | Di trú phần **kỹ thuật** (stack, schema DB, DAG, test) | ◐ **ĐANG CHẠY** (27/08) — `DEV-01` stack v1.0 · `DEV-02` quy ước v1.0 · `DEV-04` schema **v1.10** · `DEV-09` mô hình ghép PM v1.0 · `DEV-10` spec adapter ghép **v0.8** · `DEV-11` spec đọc thước chuẩn **v1.3** · `DEV-03` roadmap 7 pha **v2.9** · ⭐ `DEV-12` kế hoạch chi tiết 4 màn **v0.6**. ⭐⭐ **Từ tài liệu sang CODE THẬT, và code đã chạy trên NGUỒN THẬT** — repo `FLS`: **P0·P1·P2 xong + P3 lõi + `P4` cửa ĐỌC + `P5` cửa GHI *(đủ cả đường LÙI: bỏ mối nối — `QĐ-ITL-69`)***, **1024 phép thử**, **8.590 dòng** `fls/` + **~8.200 dòng** `tests/` + **1.900 dòng** `tools/`, **16 cổng chung**, `lint-imports` **8 kept 0 broken**. Kho PostgreSQL có **10.030 dòng sổ thật** *(run `NAP-2026-08-27-RAW`, **đã dựng lại** sau khi dọn 1.204 dòng dấu test — `GAP-KHO-01`)* + **2.745 mối nối lệnh chi** trong `fls_pm_link` + ⭐ **ảnh chụp 3.703 dòng lệnh** trong `fls_pm_line` *(mở được thao tác ghép tay — `QĐ-ITL-61`)*. ⚠ Cả ba con số trên là **BẢN SAO**, và chúng mang dấu thời điểm: *(bản sao nạp 27/08 13:42 · ảnh chụp đọc 27/08 19:07)* — sổ Google Sheets có thể đã chạy tiếp từ lúc đó, và cổng số sống ⛔ **không** so được với sổ sống, nó chỉ so tài liệu với **kho**. ⭐ `fls_adjustment` và `fls_journal` **= 0 dòng** — vòng ghi `P5` **chưa từng chạy trên sổ thật**, cố ý: nó để lại dòng vĩnh viễn trong hai bảng **không có `run_id`**, nên cổng kho-sạch ⛔ không bao giờ thấy được dấu vết đó ⇒ lệnh sang sổ thật là **quyết định của chủ sổ**. ⛔ Từ 27/08 có **hai kho** *(`fls` thật · `fls_test` cho bộ test — cổng chung #10)*. ⭐ Danh mục **quyết định phân bổ** đã nạp: **73 mã `hd`** *(`QĐ-ITL-70`)* ⇒ vùng `ALLOCATE` suy được trên **3.339 dòng sổ**. Tiến độ theo khối lượng việc **82%**, chặng **5/7** — **5/9 module xong hẳn**. ⛔⛔ **Còn — và một mục trong đó vừa thành lệch ĐÁNG KỂ:** `DEV-05` API IMPLEMENTATION vẫn là **bản copy chương trình chưa dẫn xuất**, trong khi cửa API **đã xây 75% và đã chạy thật qua HTTP** *(`GAP-DOC-03`)* — code đi trước tài liệu đúng một pha. Cùng `DEV-06..08` *(CI/runbook/release)* + Test 4 file |

### 2.1 ⭐ · Chiều NGƯỢC của di trú: code chạy thật **sửa lại tài liệu**

Bước 4 khai là *"di trú tài liệu sang kỹ thuật"* — một mũi tên **một chiều**. Thực tế 26–27/08 cho thấy mũi tên **có chiều về**, và chiều về ấy mang thông tin đắt hơn:

| Tài liệu nói | Code chạy thật đo được | Kết quả |
|---|---|---|
| `DEV-10` v0.1: `reference` nằm ở **phiếu** | Nằm ở **DÒNG** — **526/1.468 phiếu mang 2–36 mã khác nhau** | Spec lên **v0.2 §1a**, mở `CR#1-a` |
| `ledge_spec`: 7 cột `Classifying` *"suy lại được từ `<cột canon>`"* | `<cột canon>` là một **chỗ trống** — một lời hứa **không có địa chỉ**. Đo **mọi ứng viên**: `68.915 ô · 7/7 khối · 100,0000%` | `QĐ-ITL-53` điền địa chỉ thật |
| `ITL-CONTRACT v1.0`: `svc_*` kiểu **`date`** | Sổ thật là **KỲ dạng text** *(`'tháng 5'` · `'2025.07'` · `'TPCI'`)* | `CR#2` → hợp đồng **v1.1** |
| `FLS-Process`: ghép **33,5%** | Ghép **đúng** *(qua cổng tiền)* chỉ **26,79%** — **968 dòng** mà cách cũ báo đã ghép thì **không khớp tiền** | `QĐ-ITL-54`, và con số công bố **kèm cả hai cách đếm** |

⇒ **Luật rút ra:** một mục tài liệu **chưa được code chạy thật đi qua** thì chưa biết nó đúng. Nên bước 4 ⛔ **không phải** *"chép tài liệu thành code"* mà là **hai chiều**, và mỗi lần chiều về lật một tiền đề thì **mở CR con** *(`07_CHANGE_CONTROL` §7 luật 4)*, ⛔ không sửa lặng lẽ bản cũ.

## 3. Ba điều KHÔNG di trú

| Không di trú | Vì sao |
|---|---|
| `FS2 PD Now.xlsx` | Bản gốc AS-IS — chỉ đọc, không sửa, không chuyển đổi |
| Nội dung thảo luận/lập luận trong `Brainstorming/` | Kit chỉ nhận **kết luận có ID**, không nhận quá trình suy nghĩ. Muốn biết "vì sao" thì đọc nguồn |
| Quyết định chiến lược cấp chương trình (`Decision_Playbook`, `Ban_do_Gia_tri_Quyet_dinh`, `Feature_Catalog`) | Thuộc chương trình FIN ERP, không thuộc ITL. ITL chỉ nhận phần chạm L1–L2 |

## 4. Mâu thuẫn nguồn đã biết — cần xử khi di trú

| Mâu thuẫn | Xử |
|---|---|
| `Ban_do_Gia_tri_Quyet_dinh` chốt chiến lược **VALUE-FIRST**: "xây L3–L5 đọc thẳng sheet sẵn có, **HOÃN code hoá L0–L2**" — tức hoãn đúng phần việc của ITL | **Không phải mâu thuẫn kỹ thuật mà là mâu thuẫn ưu tiên.** Cần owner xác nhận: mở dự án ITL nghĩa là **đảo lại** quyết định hoãn đó, hay ITL chạy song song ở nền sau? ⇒ mở `GAP-ITL-09` |
| `NGUỒN-BUILD` dùng `M0–M7`; kit dùng `IM0–IM7` | Đã xử bằng `QĐ-ITL-02` — đọc `M0–M7` ở nguồn là `IM0–IM7` |
| Vài nguồn nói kiến trúc "6 tầng L0–L5", vài nguồn nói "5 tầng" | Cùng thứ, khác cách đếm (có/không tách Bronze/Silver). `BA-02` phải chốt **một** cách đếm rồi dùng nhất quán (R-A4: không tự chọn nếu còn nghi ⇒ đã chọn 5 tầng theo `NGUỒN-ASIS`, ghi rõ trong `BA-02`) |

## Changelog
- **v1.0** (2026-09-03, `QĐ-ITL-76`…`81`): bước 4 cập nhật — **977 phép thử** · **8.464 dòng** `fls/` · tiến độ **82%** · **16 cổng chung** · `DEV-12` **v0.1**→**v0.6**. ⭐⭐ **Chặng 6 đã CHẠY, ⛔ không còn là kế hoạch**: `B2` bộ xương · `B3` màn `F03` · `B4` màn `F01` hàng chờ · `B5` màn `F02` sổ ITL *(màn **đắt nhất** — **8 hành vi Sheets chạy thật** dưới `node`, và **lưu theo lô** có đủ ba ca lỗi)*. ⚠ Mở **`GAP-SCR-09`** *(cửa ghi ⛔ không thấy hai người sửa một ô)*, **`GAP-SPEC-02`**/**`GAP-SPEC-03`** *(đặc tả lệch cửa thật)*; đóng **`GAP-SCR-07`** + **`GAP-API-05`**. ⛔ **`B6` BỊ CHẶN** bởi `GAP-SPEC-01`.
- **v0.9** (2026-08-28, `QĐ-ITL-69`/`QĐ-ITL-70`): bước 4 cập nhật — **663 phép thử** · **7.187 dòng** `fls/` · tiến độ **67%** · **5/9 module xong hẳn** · `DEV-03` **v2.8** · `DEV-04` **v1.9**. ⭐⭐ **Chặng 6 ⛔ không còn gì chặn**: đường **BỎ mối nối** đã có *(`GAP-JOIN-05` đóng)* và **danh mục phân bổ 73 mã** đã vào kho. ⚠ Mở **`GAP-JOIN-06`** *(hàng chờ ⛔ không tự nhả một dòng đã chữa xong — cần câu trả lời nghiệp vụ)*.

- **v0.8** (2026-08-28): ⛔⛔ **File này lạc hậu LẦN THỨ HAI trong hai ngày** — `v0.7` sinh ra hôm 27/08 *chính vì* bước 4 lạc hậu 9 con số, và **hôm sau** nó lại lệch **4 con số** *(**589**→**612** phép thử · `DEV-03` **v2.3**→**v2.6** · `DEV-04` **v1.6**→**v1.7** · `DEV-10` **v0.5**→**v0.6**)*. ⇒ Bước 4 nay ⛔ **không còn được chép tay**: **7 con số** trong đó do `tools/kiem_so_song.py` so với máy mỗi lần chạy *(cổng chung #13, `GAP-DOC-04` đóng)*.
- **v0.7** (2026-08-27, sau khi ghép lệnh chạy thật): Bước 4 cập nhật số đo *(**589 phép thử · 6.328 dòng `fls/` · 64% · chặng 5/7**)* và ghi thêm **ảnh chụp 3.703 dòng lệnh** trong kho. ⭐ Chặng lên **5/7** vì `P5` nay xong **kể cả `/match`** — thao tác `QĐ-ITL-48` coi là việc chính của màn `F01` đã có cửa. ⛔ **Vẫn ⛔ không làm tròn lên 5,5**: `P6` chưa mở một dòng, và nó còn hai thứ phải giải trước *(mũi thử lưới bảng `GAP-SCR-03` · đường BỎ mối nối `GAP-JOIN-05`)*.
- **v0.6** (2026-08-27, đợt đồng bộ tiến độ): **Bước 4 lạc hậu 9 con số cùng lúc** — nó còn ghi `360 phép thử · 3.778 dòng · 10 cổng · lint 6 kept · kho 9.973 dòng · 2.650 mối nối · 49% · `DEV-04` v1.5 · `DEV-03` v1.8`, trong khi số thật là **548 · 5.780 · 12 · 7 kept · 10.030 · 2.745 · 63% · v1.6 · v2.3**. ⛔ **Lý do lệch không phải "quên"** mà là **chỗ ghi**: hai đợt `P4`/`P5` cập nhật `06_DASHBOARD` + `DEV-03` + bản vẽ, ⛔ **không ai trỏ tới file này** — nó không nằm trong danh sách file mà đợt sync đi qua, và ⛔ **không cổng nào so số giữa hai file**. ⇒ Nay thêm luôn **cổng `K5`** *(`_tools/kiem_tai_lieu.py`)*: ⛔ **không tài liệu nào được ghi một ngày CHƯA XẢY RA**. Cổng đó sinh ra vì cùng đợt này bắt được **54 chỗ ghi `28/08`** cho việc mà `git log` nói rõ làm lúc **27/08 13:56–17:49** — cả `P4`, `P5`, hai cổng chung #11/#12 đều bị dán sai ngày **về tương lai**, và cổng tài liệu 4/4 vẫn **xanh** vì nó ⛔ chưa từng kiểm ngày. ⭐ Kèm hệ quả: câu *"khung xem sống được **một ngày**"* là **sai** — nó sống **1 giờ 48 phút** *(dựng `13:56`, bỏ `15:44`)*. ⭐ Và ghi thẳng một mục **code đi trước tài liệu đúng một pha**: `DEV-05` API vẫn là bản copy chương trình trong khi cửa API đã chạy thật *(`GAP-DOC-03`)*.
- **v0.5** (2026-08-27): ⛔ **Sửa luôn một lệch có sẵn trong chính file này:** header ghi `v0.1` trong khi changelog đã lên tới `v0.4` — ba lần bump chỉ ghi ở changelog mà không ai sửa header, nên mọi file trỏ tới đây đều trích sai version. Nay header là **v0.5**. Bước **4** cập nhật số thật *(v0.1 còn dừng ở "9 commit, 34 test xanh" của 26/08)* — nay **P0·P1·P2 + P3 lõi**, **308 phép thử**, **9 cổng chung**, kho **9.973 dòng sổ** + **2.650 mối nối**, tiến độ **48%**. ⭐ Thêm **§2.1 — chiều NGƯỢC của di trú**: bốn ca code-chạy-thật **sửa lại tài liệu** *(spec ghép PM · 7 cột `Classifying` · kiểu `svc_*` · tỷ lệ ghép)*, kèm luật **mở CR con** thay vì sửa lặng lẽ bản cũ.
- **v0.4 (2026-08-26): Bước 4 đã sang code thật** — plan P0 chạy xong trong repo `FLS` *(9 commit, 34 test, 4 cổng ERD sống)*. Di trú không còn là chép tài liệu mà là **schema khai báo một lần rồi sinh ra cả DDL lẫn ERD**.
- **v0.3 (2026-08-26): Bước 4 từ ⏸ HOLD → ◐ ĐANG CHẠY** — 6 file Dev đã viết thật *(stack · quy ước · schema · mô hình ghép PM · spec adapter ghép · roadmap 7 pha + plan P0)*. Còn `DEV-05..08` và bộ Test.
- v0.2 (2026-08-18): Bước 3 chuyển ◐ sau sóng S2.
- v0.1 (2026-08-18): Khởi tạo — bản đồ 19 nguồn → file kit, 4 bước di trú (2 bước xong), 3 điều không di trú, 3 mâu thuẫn nguồn (mở `GAP-ITL-09`).
