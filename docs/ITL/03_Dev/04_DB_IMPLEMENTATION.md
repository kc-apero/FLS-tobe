# 04 — DB IMPLEMENTATION: schema FLS + kỷ luật migration

**Version:** v1.18 · **Ngày:** 2026-10-06 · **Chủ sở hữu:** Tech Lead
**Thay thế:** v0.1 *(bản copy chương trình)* — đã khai tử.

**Căn cứ:** `01_TECH_DESIGN` v1.0 · `11_INVARIANTS` v0.4 · `05_DATA_DICTIONARY_ERD` v0.5 · `QĐ-ITL-35/42/43/45`.
**DB:** PostgreSQL — dev Docker $0, prod Cloud SQL PITR. Tên bảng/trường theo `BA-05` *(`R-A2`: giữ nguyên văn nguồn)*.

> ⛔ **Đây là điều kiện vào của việc ② `QĐ-ITL-44`** — adapter phải biết ghi vào đâu. Không có schema này thì adapter viết ra rồi phải sửa lại chỗ ghi.

---

## §0 · ⭐ Toàn bộ layout `ITL Ledge` — 64 cột, 4 vùng (đọc live `A7:BI8` + `_GUIDE_04`)

⚠ **Sửa v1.1 (owner 2026-08-24):** schema v1.0 CHỈ cover vùng hợp đồng + canonical — **bỏ sót vùng ALLOCATE và AUDIT**. Đây là bản đồ đầy đủ, đọc trực tiếp header `A7:BI8` của sổ thật.

| Vùng | Cột | Trường | TO-BE |
|---|---|---|---|
| **BASE + IMPORT** | `A–Q` | Ngày CT·Số CT·Diễn giải·ĐVT·PS Nợ·PS Có·Tài khoản·Payment Type·HDCode·CDT1·bắt đầu DV·kết thúc DV·ID Payee·Hoá đơn·Khác·**LE**·No | kéo một chiều từ nguồn — `<f>_import` (máy gợi ý gốc) |
| **ADJUSTMENT** | `R`; `S–AT` | `R` **ITL ID**; 7 khối × 4 tầng `Classifying→Manual→MID→Final`: ①HDCode `S-V` ②Payment Type `W-Z` ③CDT1 `AA-AD` ④bắt đầu DV `AE-AH` ⑤kết thúc DV `AI-AL` ⑥ID Payee `AM-AP` ⑦Hoá đơn `AQ-AT` | mỗi khối rút còn **2 tầng**: `<f>_classify` (máy gợi ý, đọc) + `<f>` (**Final = kế toán nhập/sửa**, engine đọc). ⛔ bỏ tầng `MID` (mặc định cứng = "máy tự bịa", `INV-I16`) |
| **ALLOCATE** ⭐ | `AU–AW` | `AU` CDT1 **CFA1** = `AD` *(CDT1 Final)* · `AV` **CFA2** = `VLOOKUP(HDCode, Mapping Master H→K)` · `AW` **Method** = `VLOOKUP(HDCode, Mapping Master H→L)` | ⭐ **DẪN XUẤT, chỉ đọc** — máy suy từ `Mapping Master` tra theo `HDCode Final`. Không phải ô kế toán gõ. `cdt1_cfa1`=`cdt1`; `cdt1_cfa2`/`alloc_method`=join Mapping Master |
| **AUDIT** ⭐ | `AX–BL` | 6 cặp `VALUE / "FALSE=n"` đối chiếu ngược: `AX/AY` ITL ID *(FALSE=10.571)* · `AZ/BA` HD CODE · `BB/BC` Loại GD · `BD/BE` PL Time start · `BF/BG` PL Time end · `BH/BI` ID Vendor; rồi `BJ` **PIC** · `BK` **Trạng thái** · `BL` **ENITY** | ⭐ **THÊM** — vùng đối chiếu là **DQ gate của máy** (không lưu cặp VALUE/FALSE thành cột; sinh khi chạy). Giữ `pic` · `work_status` · lưu ý `BL ENITY` KHÔNG dùng (owner: `le`=`P`, không phải `BL`) |

★ **Hệ quả quan trọng:** `ITL Ledge` (64 cột, layout này) **KHÁC** `Transaction Mapping L1` (36 cột `ITL-CANON`). Schema v1.0 nhầm hai cái — cột `canon jsonb` giữ 36 cột `Transaction Mapping L1`, còn bảng phải model theo **4 vùng của `ITL Ledge`** ở trên. Cả hai đều cần: canonical là đầu vào adapter, `ITL Ledge` là sổ kế toán làm việc.

⛔ **Engine chỉ đọc 14 trường** (`A–F, P, R, V, Z, AD, AH, AL` + `G`) — nhưng **kế toán cần thấy/sửa cả 4 vùng** để đối soát. Schema lưu đủ; hợp đồng chỉ là tập con engine đọc.

---

## §1 · Ba lớp của bảng `fls_itl`

Bảng sổ mang **ba lớp**, không chỉ 14 trường hợp đồng:

| Lớp | Nội dung | Vì sao bắt buộc |
|---|---|---|
| **A · Hợp đồng** | 14 trường `ITL-CONTRACT` | đầu ra cho FPA |
| **B · Canonical** | 36 cột `ITL-CANON` | `01_PRINCIPLES`: *"cấm tạo tập cột mới cho gọn"* — giữ đủ để truy vết và để adapter khác dùng lại |
| **C · Danh tính + truy vết + song song** | khoá, lineage, run, cột `*_thật` | 5 bất biến enforce ở tầng DB |

★ Ba lớp **một bảng**, không tách — vì mọi truy vấn của app và của oracle đều theo dòng, tách bảng là tự thêm join.

---

## §2 · DDL — lớp C (danh tính, truy vết, song song)

```sql
CREATE TABLE fls_itl (
  -- ── ĐỊNH DANH (INV-I04a): số thứ tự cấp khi vào sổ, ĐÓNG BĂNG ──
  itl_id           bigint      PRIMARY KEY,           -- sinh atomic, KHÔNG theo vị trí dòng
  -- ── ĐỐI SÁNH (INV-I04b): khoá nội dung UNIQUE ──
  content_key      text        NOT NULL UNIQUE,       -- hash(source_system,source_sheet,
                                                      --   Ngày CT, PS Nợ, PS Có, Số CT/Ref, seq_trùng)
  -- ── LINEAGE (INV-I05): NOT NULL ──
  source_system    text        NOT NULL,              -- 'P100' | 'Cash' | 'A-CCR' | 'HR' | 'Platform'
  source_sheet     text        NOT NULL,
  source_row       int         NOT NULL,
  -- ── RUN (INV-I12): NOT NULL, ghim version ──
  run_id           text        NOT NULL,
  contract_version text        NOT NULL,              -- 'v1.0'
  canon_version    text        NOT NULL,
  mapping_version  text        NOT NULL,
  -- ── BẤT BIẾN TRẠNG THÁI ──
  raw_frozen       boolean     NOT NULL DEFAULT false,-- INV-I03: true ⇒ cấm UPDATE/DELETE
  is_flash         boolean     NOT NULL DEFAULT true, -- INV-I14: số chưa chốt luôn mang cờ
  period_state     text        NOT NULL DEFAULT 'open', -- INV-I13: open|locked
  created_at       timestamptz NOT NULL DEFAULT now(),
  ...  -- lớp A và B ở §3, §4
);
```

---

## §3 · DDL — lớp A (14 trường hợp đồng `ITL-CONTRACT` v1.0)

⚠ Đọc **theo TÊN**; cột Excel + index ghi kèm chỉ để đối chiếu reader thật *(`_COLS`)*.

```sql
  doc_date    date,           -- A(0)   Ngày chứng từ.  INV-I11: date, không phải chuỗi
  doc_no      text,           -- B(1)   Số chứng từ.    AUD-12: KHÔNG mang nghĩa thời gian
  memo        text,           -- C(2)   Diễn giải
  curr        text,           -- D(3)   Đơn vị tiền tệ
  ps_no       numeric(20,2),  -- E(4)   PS Nợ
  ps_co       numeric(20,2),  -- F(5)   PS Có
  acct        text,           -- G(6)   Tài khoản  ← engine CÓ đọc (owner 2026-08-20)
  le          text,           -- P(15)  LE — pháp nhân, SSOT (KHÔNG dùng BL). INV-I10 → FK
  -- itl_id đã ở lớp C = R(17)
  hd          text,           -- V(21)  Final khối 1 — Budget Code (HDCode)
  pay_type    text,           -- Z(25)  Final khối 2 — Loại giao dịch
  cdt1        text,           -- AD(29) Final khối 3 — Chủ dự toán (CDT1)
  svc_start   date,           -- AH(33) Final khối 4. date ĐẦU KỲ, UI sửa/hiện yyyymm (KHÔNG áp INV-I11 — cái đó chỉ cho doc_date). ⚠ spike kiểm kiểu ô sống
  svc_end     date,           -- AL(37) Final khối 5. như svc_start
```

★ **Khối 6–7 ngoài hợp đồng P&L — nhưng kế toán VẪN sửa tại Final** *(`AP` Mã đối tác · `AT` Hoá đơn)*. Engine P&L **không đọc**, nên **không** có ở lớp A (hợp đồng); nhưng đây là mặt sổ kế toán đối chiếu/adjust ⇒ có **cột editable + nhật ký** ở lớp A' *(không `*_thyt`/parity vì ngoài P&L)*. `QĐ-owner-0824` *(owner: kế toán sửa tay tại Final cho **cả 7 khối + phân bổ**, không chỉ 5 khối engine đọc)*. Nguồn gợi ý qua adapter F *(`QĐ-ITL-42`)*.

---

## §4 · DDL — lớp A' (cột song song `*_thật` — `QĐ-ITL-35`) + lớp B

```sql
  -- ── SONG SONG (QĐ-ITL-35): 5 trường Final có bản "sự thật" ──
  hd_thyt        text,   -- NULL ở chỗ máy tự bịa (cờ Input here). KHÔNG vào parity
  pay_type_thyt  text,
  cdt1_thyt      text,
  svc_start_thyt date,
  svc_end_thyt   date,
  work_status    text NOT NULL DEFAULT 'ok',  -- 'ok' | 'UNMAPPED' | 'rejected'  (INV-I16)
  -- ── KHỐI 6–7 NGOÀI HỢP ĐỒNG P&L — kế toán sửa Final + nhật ký, KHÔNG parity (QĐ-owner-0824) ──
  id_payee          text,   -- AP  Final khối 6 — Mã đối tác (ID Payee). Gợi ý ĐỌC TỪ canon[Y], không cột classify (QĐ grill #5)
  invoice           text,   -- AT  Final khối 7 — link Hoá đơn (đính kèm tay, không gợi ý)
  -- ── ALLOCATE (AU-AW) — máy suy từ Mapping Master làm GỢI Ý; kế toán override tại Final + nhật ký (QĐ-owner-0824) ──
  cdt1_cfa1          text,  -- AU  CFA1  (Final; gợi ý = cdt1)
  cdt1_cfa2          text,  -- AV  CFA2  (Final; gợi ý = VLOOKUP Mapping Master)
  alloc_method       text,  -- AW  Method(Final; gợi ý = VLOOKUP Mapping Master)
  cdt1_cfa2_classify    text,  -- SNAPSHOT gợi ý CFA2 lúc override (Mapping Master đổi được ⇒ chụp lại; US-025)
  alloc_method_classify text,  -- SNAPSHOT gợi ý Method lúc override
  -- ── PHÁP NHÂN TRẢ (QĐ-ITL-10) — nguồn: canon cột L "Pháp nhân thanh toán" ──
  le_payer        text REFERENCES fls_le(le_code),  -- ai THỰC trả; NULL nếu nguồn thiếu. Đối chiếu pm_le_code sau (GAP-ERD-10)
  is_intercompany boolean GENERATED ALWAYS AS
                    (le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer) STORED,
                    -- le (cột P)=pháp nhân sở hữu; khác payer ⇒ A trả hộ B. Cấm nhập tay (máy suy)
  -- ── AUDIT/WORKFLOW (BJ-BK) — cột người, không phải cặp VALUE/FALSE (DQ sinh khi chạy) ──
  pic            text,   -- BJ  người phụ trách dòng (giữ cột, CHƯA lên UI — QĐ grill)
  audit_status   text,   -- BK  Trạng thái đối chiếu (hiện ở drawer bối cảnh, khác work_status)
  -- ── CANONICAL (lớp B): 36 cột ITL-CANON, giữ đủ để truy vết ──
  canon          jsonb NOT NULL,  -- 36 cột nguyên văn; 4 cột AH–AK trùng tên ⇒ jsonb theo
                                  --   VỊ TRÍ (khuyết tật đặt tên #1, DD-I01), không theo key
```

⚠ **Vì sao `canon` là `jsonb` theo vị trí:** `ITL-CANON` có **4 cột trùng tên hệt** (`MID I DoubleCheck LE`, AH–AK) và **W/X ≡ AB/AC** *(cùng tên, khác nguồn PE vs PI)*. Lưu theo key sẽ **mất cột**. Lưu `jsonb` mảng-36 theo vị trí giữ trọn, và **không** dùng làm khoá tra.

⚠ **`*_thyt`** = viết tắt "thật" không dấu, tránh cột tiếng Việt có dấu trong DDL.

---

## §4b · ALLOCATE là vùng MÁY SUY — nguồn `Mapping Master` (đọc công thức thật)

```
AU (CFA1)   = AD                         # = cdt1 (Chủ dự toán Final) — chủ trực tiếp
AV (CFA2)   = if( VLOOKUP(hd, MappingMaster[H→K]) = "Need to Allocate to CFA2",
                  "Need to Allocate to CFA2",  cfa1 )     # cần phân bổ thì đánh dấu, không thì = CFA1
AW (Method) = VLOOKUP(hd, MappingMaster[H→L])  |  "No need"
```

⇒ **ALLOCATE máy suy từ `HDCode` + `Mapping Master`** làm **GỢI Ý mặc định** *(lưu vào `*_classify`)*. ⭐ **Sửa `QĐ-owner-0824`:** không còn "chỉ đọc" — kế toán **override được tại Final** *(`cdt1_cfa2`/`alloc_method`)*, y hệt cơ chế 4-tầng của 7 khối: máy gợi ý → người sửa thắng → **vào nhật ký** *(`fls_journal`)*, override khác gợi ý ⇒ **KÊU** *(`US-025`)*. Đây là **chệch có chủ ý khỏi AS-IS** *(AS-IS: AU/AV/AW là công thức thuần, không tầng tay)* — ghi rõ để không nhầm là bug. Khi máy chạy lại: **Final tay thắng**, không bị VLOOKUP đè.

**Cần bảng danh mục `fls_mapping_master`** *(AC-C giữ — `US-018`)*:

| Cột nguồn *(Mapping Master)* | `fls_mapping_master` | Vai |
|---|---|---|
| `H` HD Code | `hd_code` **PK** | khoá tra theo `HDCode Final` |
| `K` Need to Allocate to CFA2 | `need_cfa2` | cờ cần phân bổ |
| `L` Method to Allocate to CFA2 | `method_cfa2` | cách phân bổ *(vd "Theo doanh thu")* |
| `M` Code HR Allocate | `code_hr` | khoá phân bổ HR |
| `I`/`J` COA1/COA2 | `coa1`/`coa2` | tài khoản kế toán |

⚠ **Phụ thuộc dây chuyền:** ALLOCATE tra theo `HDCode`. `HDCode` còn `UNMAPPED` ⇒ CFA2/Method **không tính được** ⇒ phân bổ kẹt. DQ gate phải đếm *"dòng có tiền, `HDCode` trống, đáng ra phải phân bổ CFA2"* — đây là chỗ tiền lọt khỏi P&L theo venture.

---

## §5 · Năm bất biến → cưỡng chế PG

| INV | Hiện thực |
|---|---|
| **I03** `ITL RAW` bất biến | `REVOKE UPDATE, DELETE ON fls_itl FROM fls_app`; trigger `BEFORE UPDATE/DELETE`: `raw_frozen=true` ⇒ `RAISE EXCEPTION`. Sửa số **chỉ** bằng bút toán mới ở bảng `fls_adjustment` *(insert-only, `INV-I08`)* |
| **I04a** danh tính | `itl_id bigint PRIMARY KEY DEFAULT nextval('seq_itl_id')` — **SEQUENCE, ⛔ KHÔNG dùng bảng counter**; trigger `trg_fls_itl_inv_i04a` chặn `UPDATE` cột `itl_id`. ⚠ **Sửa 2026-08-26**: câu cũ dẫn *"pattern `fps_id_counter` — đã fix bug dup thật ở FPS"* là **đọc ngược bài học** — cách FPS *fix* là **bỏ bảng counter đi** *(`P100-R/fps-backend/fps/db/pg_schema.py:9`: "UPDATE+SELECT 2 round-trip, 36% độ trễ, streaming-buffer trùng ID → THAY bằng SEQUENCE + DEFAULT")*. Xem `GAP-PLAN-02` |
| **I04b** đối sánh | `content_key text NOT NULL UNIQUE` |
| **I05** lineage | `source_system/sheet/row` đều `NOT NULL` |
| **I10** LE hợp lệ | `le` → FK tới `fls_le(le_code)` + cột `is_entity`; nhãn không-phải-pháp-nhân *(`USD`, `HotBonus`)* ⇒ `work_status='UNMAPPED'`, **không vào hợp nhất** |
| **I11** ngày là ngày | cột kiểu `date` *(không `text`)*; ô không parse được ⇒ `rejected` ở DQ gate S1, đếm được |
| **I12** run ghim version | 4 cột version `NOT NULL` |
| **I13** kỳ khoá bất động | `CHECK`/trigger theo `period_state` |
| **I14** cờ số nhanh | `is_flash NOT NULL DEFAULT true` |

⭐ **`INV-I16` (không mặc định im lặng)** cưỡng chế ở tầng **code + DQ**, không phải DDL: adapter **cấm** nhánh gán giá trị cứng; chỗ không suy được ⇒ `hd_thyt = NULL`, `work_status='UNMAPPED'`, và DQ gate **đếm** — giấu số `UNMAPPED` thay vì báo ⇒ `dq_failed`.

---

## §6 · Bảng phụ

| Bảng | Vai | Bất biến |
|---|---|---|
| ~~`fls_id_counter`~~ | ⛔ **KHAI TỬ 2026-08-26** — thay bằng `CREATE SEQUENCE seq_itl_id` + `DEFAULT nextval(...)`. Lý do: FPS đã bỏ pattern này vì nó **sinh id trùng** ở streaming-buffer, và `itl_id` là danh tính đóng băng nên trùng id là hỏng khoá cả sổ | I04a |
| `fls_adjustment` | bút toán điều chỉnh, **insert-only**; `posted` không sửa/xoá, chỉ `reversed` | I08 |
| `fls_journal` | nhật ký 7 trường `AUD-1`: `itl_id · trường · trước→sau · người · thời điểm · nguồn giá trị · lý do` — ⭐ *(v1.17, `WO-018`)* **nguồn giá trị** = **lớp của CHÍNH dòng** *(`sua_tay` người · `may_goi_y` máy · bản đảo mang lớp dòng bị đảo)* **=** `fls_adjustment.nguon` cùng giao dịch, `ghi_tay._them` cưỡng chế | insert-only |
| `fls_le` | danh mục pháp nhân + `is_entity` | I10 (FK) |
| `fls_run` | mỗi lần chạy: `run_id`, 3 version, thời điểm, số dòng | I12 |
| `fls_reject` | dòng bị loại + **lý do có tên** *(`ACC-4`)* | I06 |
| `fls_mapping_master` | danh mục HD → phân bổ CFA2/Method/Code HR *(AC-C giữ, `US-018`)* — nguồn của vùng ALLOCATE | đọc-chỉ khi tính |
| `fls_khai_cot` ⭐⭐ | **BẢN KHAI ÁNH XẠ CỘT** *(`DD-I10`, migration `0016`; + cột `thu_tu` ở `0019` — `QĐ-ITL-113`, **`CHECK` đầu tiên của cả kho**)* — ⛔ **không lưu dữ liệu, lưu CÁCH ĐỌC dữ liệu**. Chỗ ở mới cho thứ kế toán đã tự duy trì ở **dòng 1 của mỗi sheet `R \|`** *(68/68 khai đủ, **19 bố cục cột**)*. **CHỈ-THÊM**: sửa khai = `version` mới | I08 |
| `fls_nguon_dai` ⭐ | **BẢN KHAI THỨ HAI** — `Range_*` của danh mục *(migration `0017`, `GAP-KHAI-01`)*: thứ mà script `Run` của trang tính **thật sự đọc**. Luật `S10` so **hai** bản khai ⇒ chúng phải trỏ **CÙNG một cột** | `S10` |
| `fls_chup` ⭐⭐ | **một LẦN ĐỌC vùng CHUẨN** *(migration `0018`, `QĐ-ITL-110`)* — `doc_luc` · workbook · lằn · `giay` · `actor`. ⛔ Sinh ra vì `xem-truoc`/`nap` đòi người gọi **đưa sẵn `dong`** ⇒ hệ ⛔ **không có đường vào nào** | ② `F04` |
| `fls_chup_nguon` ⭐ | **một nguồn trong một lần đọc** + `khai_version` đã dùng. ⭐⭐ Nguồn đọc ra **0 dòng** **VẪN CÓ MẶT** — suy tập nguồn từ *dữ liệu* thì sheet rỗng **biến mất**, đúng điểm mù `S8` từng tự lộ | ② |
| `fls_chup_dong` ⭐ | **một dòng vùng CHUẨN**, ô để **`jsonb` theo TÊN trường**, **NGUYÊN VĂN trước `chuyen()`**. ⛔ Ép về `text` là dựng lại đúng cái bẫy đã cắn **hai lần** *(seri ngày thành `"45586"`)* | ② |
| `fls_source` ⭐ | **manifest pipeline** *(hậu thân `RAW ITLData Management`, `DD-I07`)* — nguồn·trạng thái·độ trễ. **Pipeline ghi, F06 đọc** *(không phải danh mục kế toán sửa — `QĐ-ITL-34`)*. ⭐ **Từ `0016` bảng này THÔI LÀ ĐẢO**: `fls_itl` → `fls_run.khai_id` → `fls_khai_cot.source_id` → đây | — |
| `fls_queue_event` ⭐ | **append-only** hành động hàng chờ: lý do *(`US-045`)* · hoãn *(`US-040`)*. + view trạng thái + view đếm | I08 |

### §6b · DDL ba phần mới *(QĐ grill 2026-08-25)*

```sql
-- ② fls_source — manifest pipeline (DD-I07), F06 đọc chỉ
CREATE TABLE fls_source (
  source_id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_key     text NOT NULL UNIQUE,       -- 'R | HoangACB' | 'file▸sheet'
  src_type       text NOT NULL,              -- Bank|Cash|CCR|Platform|Mapping
  file           text NOT NULL,
  sheet          text,  cell text,  note text,
  start_date     date,  cutoff_date date,     -- Cut-off Date = kỳ chốt nguồn
  data_lag_days  integer,                     -- độ trễ so hôm nay (cột F06)
  n_transactions integer,
  status         text NOT NULL DEFAULT 'active',  -- active|slow|declared_not_built|retired
  link_flags     jsonb,                       -- {id_pc,id_pm,id_pe,id_pi,hd_krf,id_vendor}
  last_loaded_at timestamptz,
  updated_at     timestamptz NOT NULL DEFAULT now()
);

-- ③ fls_queue_event — append-only hành động hàng chờ
CREATE TABLE fls_queue_event (
  event_id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  itl_id      bigint NOT NULL REFERENCES fls_itl(itl_id),
  event_type  text   NOT NULL CHECK (event_type IN ('reason','defer')),
  reason      text,                           -- lý do (US-045 đếm) / lý do hoãn
  defer_until date,                           -- chỉ khi event_type='defer' (US-040)
  actor       text   NOT NULL,                -- từ token, không tự khai
  at          timestamptz NOT NULL DEFAULT now()
);
REVOKE UPDATE, DELETE ON fls_queue_event FROM fls_app;   -- append-only (INV-I08)

CREATE VIEW fls_queue_state AS                -- trạng thái hiện tại mỗi dòng → F01
SELECT DISTINCT ON (itl_id)
       itl_id, reason, defer_until, at AS last_at,
       (SELECT count(*) FROM fls_queue_event d
          WHERE d.itl_id = e.itl_id AND d.event_type='defer') AS defer_count
FROM fls_queue_event e ORDER BY itl_id, at DESC;   -- defer_count>=3 ⇒ đổi màu, không leo cấp

CREATE VIEW fls_queue_reason_weekly AS        -- US-045: 4 tuần = 0 ⇒ cổng chết
SELECT date_trunc('week', at) AS week,
       count(DISTINCT itl_id) FILTER (WHERE event_type='reason') AS rows_with_reason
FROM fls_queue_event GROUP BY 1;
```

*① `le_payer` + `is_intercompany` đã ở trong `CREATE TABLE fls_itl` §4 (lớp A').*

---

## §7 · Kỷ luật migration

✅ **ĐÃ CÓ CƯỠNG CHẾ 2026-08-26** *(`fls/db/migration_runner.py` + `pg_migrate.py`, đóng `GAP-DB-P0-02`)*.

**Hai nguồn sự thật và cổng nối chúng** — phải hiểu chỗ này trước khi sửa schema:

| Thứ | Là gì | Ai dùng |
|---|---|---|
| `fls/db/schema.py` | **TRẠNG THÁI MONG ĐỢI** | sinh ERD; là thước đo của `pg_verify` |
| `fls/db/migrations/NNNN_*.sql` | **ĐƯỜNG ĐI** tới trạng thái đó. Text **đóng băng**, ⛔ không sinh ra | runner áp lên DB |
| ⭐ **Cổng nối** | schema PG **trống** → áp hết migration → `pg_verify` **phải xanh** | `test_migration_toi_dung_schema_khai_bao` |

⛔ **Thiếu cổng nối thì hai nguồn sẽ trôi khỏi nhau** — đó là lý do nó chạy trên một PG schema **rỗng thật**, không phải trên DB dev đã có sẵn bảng.

- **Forward-only**; ⛔ **không sửa migration đã deploy** — cưỡng chế bằng `checksum` sha256 lưu trong sổ `fls_migration`; sửa file đã áp thì runner **NỔ**, không âm thầm chạy lại. *(Đã diễn tập: sửa `0002` sau khi áp → `migration 0002 DA BI SUA sau khi ap (checksum DB=38b0b262… code=f697d698…)`.)*
- Số thứ tự phải **tăng đơn, không hở, không trùng**. Migration biến mất khỏi code mà còn trong sổ ⇒ **NỔ**.
- Sau khi áp, runner **tự chạy `pg_verify`**; lệch ⇒ `exit 1` kèm câu *"áp xong nhưng DB VẪN LỆCH schema khai báo — thiếu migration?"*. *(Đã diễn tập: thêm cột vào `schema.py` mà không viết migration → nổ đúng chỗ.)*
- `--status` *(đã áp gì / còn thiếu gì)* · `--dry-run` *(in offline)* · `--adopt-baseline` *(DB đã đúng sẵn: **verify TRƯỚC**, lệch thì từ chối, khớp thì chỉ ghi vào sổ)*.
- Bảng lớn: `add column → backfill → constraint` *(non-locking)*.
- Bảng `fls_migration` là **bootstrap** — runner tự tạo **TRƯỚC** migration đầu tiên, nên cố ý **không** nằm trong `CREATE_ORDER`. Mọi tên trong tập `BOOTSTRAP` phải có lý do bằng chữ *(cùng luật với `ERD_ISLANDS`)*.
- ⭐ **Cột song song `*_thyt` và `canon` phải có trong migration ĐẦU TIÊN** — thêm sau là migration trên bảng đã đầy dữ liệu, đúng thứ `01_TECH_DESIGN` §5 cảnh báo. **Có test khoá**: `test_baseline_co_du_cot_thyt_va_canon`.
- `btree_gist` không cần *(FLS không có ràng buộc khoảng thời gian chồng như Core)*.

---

## §8 · Việc mở

| ID | Việc |
|---|---|
| `GAP-DB-01` | Chốt **thành phần chính xác** của `content_key` — `05` §`DD-I05` đề xuất, cần khoá lại bằng test *(chạy 2 lần → key không đổi; sửa 1 trường nội dung → key đổi có kiểm soát)* |
| `GAP-DB-02` | `period_state` khoá theo kỳ nào — nối với cut-off `pm_settled_through` |
| `GAP-DB-03` | `fls_le` nạp từ đâu — danh mục pháp nhân hiện nằm rải ở nhiều nguồn |
| `GAP-DB-05` | `fls_mapping_master` nạp từ file/sheet nào, nhịp nào — `Mapping Master` hiện có `IMPORTRANGE` sang một file COA khác (`_GUIDE_04:89`) |
| `HOI-063` | ⭐ *(06/10, `WO-051`)* view `fls_queue_state` *(bản sống ở `fls/db/schema.py` `_V_QUEUE_STATE` — ⚠ khác bản `DISTINCT ON` vẽ ở §6b trên)* lấy lý do bằng `ARRAY_AGG(reason ORDER BY at DESC)[1]` **⛔ khoá phụ** ⇒ sổ thật **8.387 / 8.387** dòng có ≥ 2 sự kiện `reason` cùng `at` lớn nhất *(dựng lại 10/09 — một giao dịch)*, **8.256** mang ≥ 2 chuỗi khác nhau ⇒ *"lý do mới nhất"* đổi theo **kế hoạch truy vấn** *(đo: 398 / 8.387 hàng khác giữa gom cả bảng ↔ gom từng `itl_id`)*. Đề xuất: khoá phụ `evt_id DESC` *(migration — chờ `TL-063`)* |

---

## Changelog
- **v1.18** *(2026-10-06, `WO-051` · `HOI-063`)*: ⛔ **Không migration, không đổi bảng** — §8 thêm `HOI-063` *(view `fls_queue_state` ⛔ xác định "lý do mới nhất" khi nhiều sự kiện cùng `at`)*. Câu đọc hàng chờ `doc_bao_cao._SQL_HANG_CHO` gom view **một lần** mỗi trang *(`MATERIALIZED`)* thay vì để bộ lập kế hoạch tính lại nó theo vòng nối *(trang 2 `VND` sổ thật **~100 s** ⇒ **~0,07 s**)* — chú thích tại chỗ giữ số đo + lý do ⛔ dùng `LATERAL`.
- **v1.17** *(2026-10-02, `WO-018` · `BA-05` v0.34 `DD-I15 ⓓe` · `TL-016`)*: ⭐⭐ **`fls_journal.value_source` = lớp của CHÍNH dòng — một nghĩa, cửa ghi cưỡng chế.** ⛔ **Không migration, không đổi cột** — đổi **luật ghi**. Trước: cột mang **hai nghĩa** — dòng máy *(`ghi_goi_y`)* và bản đảo bỏ ghép *(`bo_moi_noi`)* ghi lớp của chính dòng, còn cú `/adjust` *(`ghi_but_toan`)* ghi **nguồn TRƯỚC khi gõ** *(`UNMAPPED` · `nguon` · `may_goi_y` · `sua_tay`)*; và `dao_but_toan` ghi cứng `sua_tay` cho **mọi** bản đảo. Nay: `_them` lấy `value_source` = `nguon` *(bỏ trống ⇒ lấy `nguon`; truyền khác ⇒ `LoiGhi`, **0** dòng)*; `ghi_but_toan` ghi `sua_tay`; `dao_but_toan` chép `nguon` của dòng bị đảo. Thân trả `/adjust` *(`KetQuaGhi.value_source`)* **giữ** nghĩa *"nguồn trước khi gõ"* *(`US-025`)*. Chú thích cột `schema.py` đổi ⇒ `Ban-do-Kien-truc-7-Tang.html` sinh lại *(DDL ⛔ mang chú thích ⇒ golden ⛔ đổi)*. Sổ thật *(chỉ `SELECT`)*: **4.428 / 4.428** cặp bằng nhau trước và sau ⇒ ⛔ dòng nào mang nghĩa cũ. ⚠ ⛔ `CHECK` trên `value_source`: kho TEST còn dòng cũ `nguon`/`UNMAPPED`.
- **v1.16** *(2026-09-18, `QĐ-ITL-145`)*: ⭐⭐⭐ **Migration `0026` — `fls_dien_giai`, và nó ⛔ KHÔNG nạp thêm gì cả.** Owner duyệt *"mở phạm vi nạp cột diễn giải"*; mở mã ra thì thấy **⛔ không có gì để mở**: `QĐ-ITL-128` *(17/09)* **đã** cho đọc `Description` và nhịp chụp mỗi giờ **đang giữ nó** *(`8.589/8.592`)* — chỉ là `fls_itl.memo` vẫn `0/8.387`. ⇒ ⭐⭐ **Quyết định đã đổi, đường ghi ở lại** — lớp lỗi cũ, **ngược chiều**, và ⛔ không cổng nào thấy vì **một cột rỗng ⛔ không bao giờ báo lỗi**. ⛔⛔ Hai đường sai đều bị loại bằng phép đo: **nạp lại** ⛔ vô ích *(`content_key` ⛔ không chứa diễn giải ⇒ bỏ qua vì trùng)*; **`UPDATE memo`** ⛔ phạm `INV-I08`. ⇒ Khung xem nối `(source_key, dong_so)` ↔ `(source_sheet, source_row)`, lấy **ảnh mới nhất CÓ dòng ấy** *(`LATERAL`, ⛔ không `max(chup_id)` toàn cục — ảnh `152381` có **0 dòng**)*. Đo: nối **8.361**, có chữ **8.358 = 99,7%**, ⭐ **tiền tệ khớp 8.358** — phép kiểm thứ ba là thứ đắt nhất vì hai bảng cùng xếp theo `dong_so`, nên nối **lệch một hàng** vẫn ra `99,7%` và vẫn **trông hợp lý**. ⚠ Dòng ⛔ không có chữ thì **vắng** khỏi khung xem, ⛔ không trả chuỗi rỗng. ⭐ Cổng hình học bắt bản vẽ **tràn khung** khi tầng ① thêm một ô ⇒ sửa **GỐC**: `sinh_ban_do_tang` biết **xuống hàng** *(nới khung chỉ đủ tới lần thêm sau)*. ⛔ Và một bài của tôi **đo sai thứ**: `count(memo)==0` trên kho TEST bắt oan vì bài khác có quyền chèn `memo` ⇒ đổi sang **quét mã nguồn** tìm `UPDATE fls_itl … memo`.
- **v1.15** *(2026-09-18 tối muộn, `QĐ-ITL-143` — owner chốt **phương án B**)*: ⭐⭐⭐ **Migration `0025` — `fls_adjustment.nguon`, và nó vá một chỗ ⛔ KHÔNG AI NHÌN THẤY.** Bảng **GIÁ TRỊ** *(`fls_adjustment`)* ⛔ **không có** cột nguồn; `value_source` chỉ sống ở **sổ NHẬT KÝ** *(`fls_journal`)*. Mà khung xem trả lời câu *"ô này đang là gì"* — `fls_sua_tay` — đọc **bảng giá trị**. ⇒ Một gợi ý của MÁY ghi vào đó sẽ hiện ra **y hệt** một con số NGƯỜI đã chốt, `_hieu_luc()` lấy nó làm `value_before` cho lần gõ sau, và `truoc_khi_go()` in nó ra như *"giá trị đang có"* — ⛔ **không một chỗ nào** trong đường ĐỌC phân biệt được. Đó đúng là `INV-I16`. ⭐⭐ **Cách xử ⛔ KHÔNG phải thêm một cột vào `fls_sua_tay`:** khung xem ấy đang trả lời **MỘT** câu — *"NGƯỜI đã chốt gì"* — và `bang_tuyen.py` có **8 tuyến** đọc nó với đúng nghĩa ấy; nhét gợi ý vào rồi bắt mọi chỗ tự lọc là **đổi nghĩa một khung xem đang chạy**, và chỗ nào quên lọc thì ⛔ không báo lỗi, chỉ **trả sai**. ⇒ `fls_sua_tay` **giữ nguyên nghĩa**, nay lọc thẳng `nguon='sua_tay'`; gợi ý của máy đi **lối RIÊNG** — khung xem mới **`fls_may_goi_y`** *(thực thể `23 → 24`)*. ⭐⭐⭐ **Và đường MÁY ghép nay gợi ý `hd`/`cdt1`** *(`fls/repo/may_ghep.py` + `chay_nap._goi_y_sau_ghep`)* — phép suy **DÙNG CHUNG** với đường ghép tay *(`suy_hd_cdt1`)*, ⛔ không viết bản thứ hai: hai bản là hai chỗ để chúng lệch nhau, và cái lệch ấy hiện ra dưới dạng *"ghép tay ra một số, máy nạp ra số khác"* mà ⛔ không cổng nào bắt được. ⚠ **Một lỗ tôi suýt bỏ sót:** `_goi_y_sau_ghep` chỉ chạm mối nối **sinh ra trong lần nạp đó**; nạp lại thì dòng cũ bị bỏ qua vì trùng `content_key` ⇒ **2.262** mối nối cũ sẽ ⛔ **không bao giờ** được gợi ý ⇒ thêm `tools/goi_y_lai.py` *(xem trước / `--ghi`)*. Chạy thật `18/09`: **4.424** bút toán trên **2.219** dòng — hiệu lực **`hd` 2.209 · `cdt1` 2.215**, và **12** trường máy **⛔ từ chối suy** *(N dòng lệnh nói N thứ — `INV-I16`)*. ⛔ **Ba bất biến giữ nguyên sau khi ghi**: `fls_sua_tay` **0** *(⛔ không lọt sang lằn người)* · `fls_itl.hd` vẫn **0/8.387** *(`INV-I08` — sổ ⛔ không đổi một ô)* · nhật ký khớp **4.424**. ⭐ Cổng bắt được tôi: `khop_owner C6` **đổi trạng thái** *(mong LỆCH, đo được KHỚP)* ⇒ ghi lại `mong` **và** thêm phép **`C8`** canh đúng ranh giới MÁY↔NGƯỜI; và `kiem_so_song` *"bút toán sửa THẬT"* **hỏng đúng ngày con số thôi là `0`** — mẫu `(\d+)` ⛔ không nhận `4.424` *(dấu chấm kiểu VN)*, đúng cái bẫy mà chú thích **ngay dưới nó** đã cảnh báo.
- **v1.14** *(2026-09-18, `CR#12` · `GAP-ERD-P0-02`)*: ⭐ **Migration `0024` — `fls_pm_link.run_pm`.** Một mối nối nay **neo được** vào **ảnh lệnh chi** đã dùng lúc ghép. ⛔⛔ **Vì sao cần một cột RIÊNG:** `run_id` sẵn có mang **HAI nghĩa** tuỳ đường ghi — `chay_nap.chen_moi_noi` ghi lần **NẠP**, `ghi_tay` ghi ảnh **LỆNH CHI**; đo kho thật: cả **2.262** dòng đều là lần NẠP *(chưa ai ghép tay, `hinh='T'` = 0)*. ⛔ **Cái giá của việc thiếu nó, đo được:** `fls_pm_line` khoá chính **ghép đôi** `(run_id, pm_line_id)` — **22** ảnh PM giữ 22 bản của cùng một dòng lệnh ⇒ nối bằng khoá **đơn** làm mọi phép đếm **phồng đúng bằng số ảnh**: `2.262` → **`49.764`**, câu SQL vẫn **chạy trót lọt** và con số vẫn **trông hợp lý**. ⭐ **`FK → fls_run` thì CÓ** *(miễn phí — mọi dòng cũ `NULL`)*; **`FK → fls_pm_line` thì ⛔ KHÔNG đặt được**: khoá ghép đôi bên ấy đòi backfill bằng một phép **suy** ảnh PM hiệu lực `10/09`, và phép suy ⛔ không được hoá thành ràng buộc cứng *(`INV-I16`)* ⇒ thay bằng một **câu đếm** trong `tests/db/test_moi_noi_neo_anh_pm.py`. ⚠ ⛔ **KHÔNG backfill** — `NULL` ở đây có nghĩa **thật**: *"mối nối sinh trước 18/09"*. ⭐ Bốn cổng bắt được tôi trong lượt này: parity `schema.py`↔migration *(khai `fk` mà ⛔ chưa tạo)* · golden DDL · hai hiện vật ERD · và **hai bài ghim số khoá ngoại** `23 → 24` — chỗ để tuyên bố *"tôi biết mình vừa thêm một khoá"*.
- **v1.13** (2026-09-17 — **BẮT KỊP BỐN MIGRATION `0020`…`0023`, và đây là lần TỤT LẠI THỨ HAI**): ⛔⛔ Tệp này đứng ở `v1.12` *(migration `0019`, 08/09)* trong khi kho đã đi tới **`0023`**. ⭐ `v1.12` đã đặt tên cho đúng bệnh này — *"bắt kịp ba migration, và nói ra vì sao nó tụt lại"* — nên lần này ⛔ **không** ghi lại lời hứa, mà ghi **con số**: `04_DB` tụt **`3` migration** *(07/09)* rồi **`4` migration** *(17/09)*; ⛔ **không cổng nào canh khoảng cách ấy** — `pg_verify` so **kho ↔ bản khai**, ⛔ không so **bản khai ↔ tệp này**.
  - ⛔⛔⛔ **`0020` — `fls_reject` đổi khoá sang `(run_id, source_sheet, source_row)`. ĐÂY LÀ MỘT ĐƯỜNG MẤT DỮ LIỆU ĐÃ CHẠY THẬT, ⛔ không phải một cải tiến.** Khoá cũ `UNIQUE (run_id, source_row)` sinh ở `0007` vì một lỗi thật *(chạy lại nhân bản `fls_reject` thành **76** dòng cho **19** dòng loại thật)*, và lúc ấy nó **đúng**: *một lần nạp = MỘT nguồn*. ⭐ `QĐ-ITL-111` (08/09) dựng **cửa nạp CẢ LÔ** — *một* `run_id` cho **59 nguồn** — **tiền đề biến mất, và ⛔ không ai sửa khoá**. `source_row` chỉ là chỉ số dòng **trong một sheet**, nên dòng `0` của 59 sheet là 59 lần **cùng một giá trị** ⇒ chỉ nguồn **đến trước** được ghi, 58 nguồn còn lại bị `WHERE NOT EXISTS` **nuốt trong im lặng** *(`rowcount` 0, ⛔ không lỗi)*. **Đo 10/09 trên ảnh THẬT `chup_id 24033`:** ảnh **8.406** dòng · vào sổ **6.617** · ghi được vào `fls_reject` **1.143** · ⛔ **BỊ LOẠI MÀ ⛔ KHÔNG CÓ BẢN GHI NÀO: 646 dòng**, trải trên ⛔ **23 nguồn** *(chỉ **11** nguồn có bản ghi)*. ⇒ Vi phạm thẳng **cổng chung #3 *"0 dòng rơi im lặng"*** — và nó lọt vì cổng đếm **bốn đường** ở tầng nạp, ⛔ không đếm **dòng thực nằm trong `fls_reject`**.
  - **`0021` — `fls_pm_line.tho`: GIỮ LẠI DÒNG THÔ của lằn `PM`.** Sửa một **bất đối xứng có thật** *(đo 11/09)*: lằn `Bank` **7.454.400** dòng thô trong `fls_chup_dong`, lằn `PM` ⛔ **0**. Khai cũ *("`fls_pm_line` CHÍNH LÀ bảng dòng của lằn này")* **đúng về thiết kế**, nhưng kéo theo hệ quả ⛔ không ai nói ra: nó chỉ giữ **8 trường đã phân tích** ⇒ **20 cột còn lại của `PM_Unpivot` biến mất ngay lúc đọc**, và thêm một cột về sau thì ⛔ **không bù ngược được**. ★ Từ đây, thêm một trường hiển thị = **đọc lại `tho`**, ⛔ không phải chụp lại. ⚠ `NULL` có nghĩa THẬT *("ảnh chụp TRƯỚC 11/09")* ⇒ ⛔ **không** `DEFAULT '{}'`: một dấu ngoặc rỗng trông như *"đọc được 0 cột"*, và hai chuyện ấy khác nhau *(`INV-I16`)*.
  - **`0022` — `tho`: `jsonb` → `json`, để GIỮ THỨ TỰ CỘT của ggsheet.** `jsonb` **⛔ không giữ thứ tự khoá** *(nó chuẩn hoá và sắp lại theo độ dài rồi byte)* ⇒ thứ tự cột của tờ giấy **chết ngay lúc ghi**. Với một cột mà **toàn bộ công dụng là HIỆN RA CHO NGƯỜI ĐỌC**, thứ tự **là một phần của dữ liệu** — kế toán đọc `PM_Unpivot` hằng ngày và trí nhớ vị trí của họ là một công cụ thật. ⚠ **Cái giá, khai ra chứ ⛔ không giấu:** `json` ⛔ không có toán tử `?`/`@>` và ⛔ không đánh chỉ mục `GIN` được; quét mã 11/09: **0** câu trong `fls/` dùng toán tử `jsonb` trên cột này. ⛔ `USING tho::text::json` — đi qua `text` là **CỐ Ý**: `jsonb::json` chỉ đổi nhãn kiểu trên một giá trị **đã bị sắp lại**.
  - **`0023` — bảy khoá `PE`/`PI` LÊN CỘT CÓ KIỂU** *(owner chốt 17/09)*: `pe_slip` · `pe_line` · `pe_loai` · `pi_slip` · `pi_line` ⇒ `fls_pm_line` **12 → 18 cột**. **Đo trước khi khai** *(26.404 dòng có `tho`)*: `PE` cặp **3.500** lệch `0` · `PI` cặp **22.904** lệch `0` · `Advance` 3.381 + `Urgent` 119 = 3.500 · một dòng có **ĐÚNG MỘT cha**, ngoại lệ `0`. ⛔⛔ **Ba bất biến ấy CỐ Ý ⛔ KHÔNG thành `CHECK`** — trừ `pe_loai`: phép chèn chạy **một giao dịch cho cả lần nạp**, nên một `CHECK` biến *một dòng lạ* thành *đổ cả lượt nạp*. `pe_loai` an toàn vì giá trị do **mã của ta** sinh ra ⇒ nguồn ⛔ không thể làm nó vỡ. Đây là `CHECK` **thứ hai** của cả kho *(sau `thu_tu`)*. ⚠ **52.808/79.212** dòng mang `NULL` vì nạp **trước 11/09** — **sự thật**, ⛔ không phải thiếu sót.
- **v1.12** (2026-09-08 — **BẮT KỊP BA MIGRATION, và nói ra vì sao nó tụt lại**): ⛔⛔ **Tài liệu này đứng ở `v1.11` ngày 07/09 trong khi kho đã đi tới migration `0019`** — tức nó lạc hậu **BA** migration *(`0017` dải đọc · `0018` ảnh chụp · `0019` thứ tự ngày)*, và ⛔ **không cổng nào thấy**. ⛔⛔ **Và lý do KHÔNG phải cái tôi tưởng — ghi lại làm bia:** tôi viết *"`kiem_so_song` ⛔ không ghim `DEV-04`"* rồi cổng **đỏ ngay** — nó ghim ở **HAI** chỗ. Tôi **suy** từ bốn cái tên tình cờ thấy trong một lượt đỏ trước đó thay vì **đo**. ⭐ Nguyên nhân thật đáng ghi hơn: cổng so phiên bản ở `MASTER_INDEX` §8 / roadmap với phiên bản ở **đầu chính tệp này** — cả hai đều nói `1.11` nên **chúng KHỚP** ⇒ cổng canh **TÍNH NHẤT QUÁN**, ⛔ **không** canh **TÍNH CẬP NHẬT**. Một tài liệu **nhất quán với chính nó** mà **lạc hậu ba migration** thì ⛔ không phép đo nào hỏi tới. Đúng lớp `QĐ-ITL-103` — **một con số ĐÚNG nằm trong một câu SAI**. ⇒ Thêm **4 bảng** vào §6 *(`fls_nguon_dai` · `fls_chup` · `fls_chup_nguon` · `fls_chup_dong`)* + cột `fls_khai_cot.thu_tu`. ⚠ Mở `GAP-DOC-10` *(cần một phép so **`fls/db/migrations/*.sql` ↔ migration được nhắc trong tệp này**)*.
- **v1.11** (2026-09-07, `CR#11` — `P7` task `1`): ⭐⭐⭐ **Migration `0016` — bảng `fls_khai_cot`, BẢN KHAI ÁNH XẠ CỘT** *(`DD-I10`)*. ⛔⛔ **Bảng này ⛔ không lưu dữ liệu — nó lưu CÁCH ĐỌC dữ liệu.** Lý do tồn tại: `QĐ-ITL-105` bỏ Google Sheets khỏi đường nạp, mà **bản khai tốt nhất của cả hệ AS-IS đang sống ở dòng 1 của mỗi sheet `R \|`** *(kế toán tự duy trì, **68/68** khai đủ trên **9** bố trí cột)* ⇒ không dựng chỗ ở mới thì **nó bị vứt theo**, và FLS phải **đoán vị trí cột** — thứ `sao_ke.py` cấm thẳng *(“đoán ⛔ không phải kém chính xác, nó là **sai tiền**”)*. ⭐ Khoá duy nhất **`(source_id, version, truong)`** — `version` **nằm TRONG khoá** để luật **chỉ-thêm** sống được, và `hieu_luc_tu` **⛔ không nằm trong khoá** *(mốc thời gian không lặp ⇒ ràng buộc sẽ luôn đúng, tức một cổng xanh vì ⛔ không đo gì)*. ⭐ `fls_run` thêm **đúng 1 cột** `khai_id` **nullable** — lô `NAP-2026-08-27-RAW` *(**10.030** dòng)* **có trước** bảng này, bịa một `khai_id` cho quá khứ là trái `R-A1`; đo lại sau khi áp: `khai_id` = **NULL**, **10.030 dòng nguyên vẹn**. ⚠ **Miền giá trị *(`truong` ∈ `SAU_TRUONG` · `cot ≥ 0`)* CỐ Ý ⛔ không cưỡng chế bằng `CHECK`** — cả repo ⛔ không có lấy một `CHECK` nào *(`work_status` · `period_state` · `src_type` · `evt_type` đều là lời văn + chặn ở tầng ghi)*; thêm `CHECK` ở đây là **chỗ khai thứ hai** cho `sao_ke.SAU_TRUONG`. Chỗ chặn là `fls/repo/khai_cot.py` *(task `2`)*, và phải chặn lúc **GHI**. ⭐⭐ **Hệ quả ngoài lề, đáng giá:** `fls_source` **thôi là ĐẢO** — nay đi bộ được `fls_itl.run_id` → `fls_run.khai_id` → `fls_khai_cot.source_id` → `fls_source`, tức *“dòng sổ này đến từ NGUỒN này, đọc bằng BẢN KHAI này”* ⇒ `ERD_ISLANDS` **3 → 2 tên**. ⛔⛔ Và chuyện đó lộ ra một cổng **chỉ hỏi một chiều**: `G-ERD-3` xưa nay chỉ hỏi *“có bảng nào mồ côi mà CHƯA khai không?”*, ⛔ **không bao giờ** hỏi *“có tên nào ĐÃ khai là đảo mà thực tế đã nối được rồi không?”* ⇒ một ngoại lệ **sống sót qua cả lý do sinh ra nó**. Thêm cổng **chiều ngược** + một bài **chứng minh nó cắn thật**. Đã áp **kho thật** + kho test, `pg_verify` **khớp 19 bảng/view**; golden DDL + ERD sinh lại bằng lệnh. **1.125 phép thử xanh** *(+21)*.
- **v1.10** (2026-08-28, `QĐ-ITL-71`): ⭐⭐ **Migration `0014` — khung xem `fls_da_xong`** *(đóng `GAP-JOIN-06`)*. ⛔ **Không thêm cột nào, ⛔ không bảng nào**: *"dòng này xong chưa"* là sự kiện **mới nhất** trong hai loại `done`/`reopen` của `fls_queue_event` — cùng thang thuốc với `fls_sua_tay` và `fls_moi_noi`. ⇒ `evt_type` nay là `reason|defer|match|unmatch|done|reopen`. Có **index riêng** *(`itl_id, evt_id DESC` lọc theo hai loại ấy)* vì hàng chờ đọc khung xem này trên **mọi lượt**. ⛔ **Lý do phải có khung xem thay vì một cột `da_xong`:** đổi một cột cần câu `UPDATE` lên `fls_itl` — đúng thứ `INV-I08` cấm, và trigger `INV-I03` đã chặn sẵn. Đã áp **kho thật** + kho test, `pg_verify` **khớp 18 bảng/view**; golden DDL + ERD sinh lại bằng lệnh.
- **v1.9** (2026-08-28, `QĐ-ITL-69`): ⭐⭐ **Migration `0013` — đường BỎ MỐI NỐI**. Ba việc: ⓐ `fls_pm_link` có **danh tính riêng** `link_id` + số `lan`; khoá chính đổi từ `(itl_id, pm_line_id)` sang `(link_id)`, khoá duy nhất thành `(itl_id, pm_line_id, lan)` — vì khoá cũ chặn **ghép lại đúng dòng lệnh vừa gỡ**, đúng việc phổ biến nhất sau khi gỡ. ⓑ bảng **`fls_pm_unlink`** *(một dòng cho mỗi mối nối bị bỏ, `UNIQUE(link_id)`)* — CỐ Ý ⛔ không chứa `actor`/`reason`: *ai bỏ* và *vì sao* sống ở `fls_queue_event` `evt_type='unmatch'`, **một chỗ**. ⓒ **`fls_adjustment.evt_id`** — *bút toán này sinh ra bởi THAO TÁC nào*; ⛔ không có cột này thì cách duy nhất nhận ra bút toán của phép ghép là **đối chuỗi `reason`**. ⓓ khung xem **`fls_moi_noi`** = mối nối **đang có hiệu lực**; `fls_pm_link` từ đây là **lịch sử**. ⛔ Đã áp **kho thật** + kho test, `pg_verify` **khớp 17 bảng/view**; golden DDL + ERD sinh lại bằng lệnh. ⚠ **Một hệ quả đáng ghi:** khoá chính `fls_pm_link` nay ⛔ **không drop được nữa** *(FK từ `fls_pm_unlink` trỏ vào)* — ràng buộc mạnh hơn, nhưng nó làm bài `test_pg_verify_BAT_DUOC_khoa_bi_bo` phải **đổi nạn nhân** sang `fls_pm_unlink`.
- **v1.8** (2026-08-28, `QĐ-ITL-65`): ⛔ **Migration `0012` — BỎ 5 cột vùng `ALLOCATE`** khỏi `fls_itl` *(`cdt1_cfa1` · `cdt1_cfa2` · `cdt1_cfa2_classify` · `alloc_method` · `alloc_method_classify`)*. Lý do: ba ô ấy là **công thức**, suy lại được 100% từ `cdt1` + `hd` + `fls_mapping_master` K/L *(`fls/ledger/allocate.py`)*; `AU` chỉ là **bản sao của `cdt1`**; và `QĐ-ITL-64` chốt kế toán ⛔ không sửa vùng này nên hai cột `*_classify` ⛔ hết nghĩa. ⭐ **0 dòng có giá trị** trước khi bỏ ⇒ ⛔ không mất dữ liệu. Đã áp **kho thật** + `pg_verify` **khớp 15 bảng/view**; golden DDL + ERD sinh lại bằng lệnh. ⭐ Có bài test **khoá chiều quay lại** *(một cột bị bỏ rất dễ mọc lại)* — thông báo đòi **mở lại `QĐ-ITL-64`/`QĐ-ITL-65`** trước.
- **v1.7** (2026-08-27): **Năm migration mới kể từ v1.6, và hai trong đó đáng đọc lý do.** `0006` cột `pm_line_id` → `0007` **BỎ cột đó** chuyển sang bảng nối `fls_pm_link` *(một cột giữ được MỘT mối nối, hình `B` không đậu)*. ⛔⛔ `0008` dựng khung xem `fls_queue_xep_tien` rồi `0009` **BỎ nó sau 1 giờ 48 phút** — khung xem SQL ⛔ không nhận tham số nên ⛔ không mang được **phạm vi đọc**, và **lọc ở đầu ra ⛔ không sửa được một thứ tự đã xếp sai** *(`CR#4`)*. `0010` khung xem `fls_sua_tay` *(`CR#5`)*. ⭐ `0011` bảng **`fls_pm_line`** — **ẢNH CHỤP** dòng lệnh chi, ⛔ không phải danh mục: `run_id` nằm **trong khoá chính** nên nạp lại là **thêm ảnh mới** *(`QĐ-ITL-61`, chi tiết ở `BA-05` §`DD-I08`)*. Kho nay **15 bảng/view**, `pg_verify` khớp.
- **v1.6** (2026-08-26): **§7 kỷ luật migration từ nguyên tắc → CƯỠNG CHẾ THẬT** *(đóng `GAP-DB-P0-02`)*. Sổ ghi `fls_migration` + `checksum` chống sửa lịch sử + số thứ tự tăng đơn + **runner tự chạy `pg_verify` sau khi áp**. Nói rõ **hai nguồn sự thật** *(`schema.py` = trạng thái mong đợi · `migrations/` = đường đi)* và **cổng nối** chúng *(schema trống → áp hết → verify xanh)*. Thêm bảng `fls_migration` *(bootstrap, có lý do)* và tập `BOOTSTRAP`. Cả hai cổng **đã diễn tập thấy đỏ**.
- **v1.5** (2026-08-26, sau khi chạy P0): ⛔ **Khai tử `fls_id_counter`** → `CREATE SEQUENCE seq_itl_id` + `DEFAULT nextval(...)`. Câu cũ ở §5 dẫn *"pattern `fps_id_counter` — đã fix bug dup thật ở FPS"* là **đọc ngược bài học**: cách FPS *fix* chính là **bỏ bảng counter** *(`pg_schema.py:9`)*. Đóng `GAP-PLAN-02`. Bất biến `INV-I03`/`INV-I04a` **đã có cưỡng chế thật** — trigger `trg_fls_itl_inv_i03`/`trg_fls_itl_inv_i04a` trong `fls/db/triggers.py`, 5 test trên PG 16 container *(`tests/db/test_invariants_pg.py`)*. Migration chạy 2 lượt cho cùng kết quả.
- **v1.4** (2026-08-25, rà ERD↔màn hình + grill): **① `le_payer` (FK→`fls_le`) + `is_intercompany` (GENERATED STORED)** — nền cho US-032 + phát hiện intercompany *(`QĐ-ITL-10`; nguồn canon cột L, đối chiếu `pm_le_code` sau — `GAP-ERD-10`)*. **② bảng `fls_source`** *(manifest pipeline, F06 đọc)*. **③ bảng `fls_queue_event` append-only + 2 view** *(lý do US-045 · hoãn US-040)*. Bỏ `id_payee_classify` *(gợi ý khối 6–7 đọc từ canon)*; giữ 2 snapshot ALLOCATE. Sửa comment `svc_start/end`: kiểu `date` đầu kỳ + UI yyyymm, **không** áp `INV-I11` *(chỉ cho `doc_date`)* — ⚠ mở spike kiểm kiểu ô sống. `pic` giữ cột, chưa lên UI.
- **v1.3** (2026-08-24, `QĐ-owner-0824`): **Mở mặt kế toán sửa từ 5 → 7 khối + phân bổ.** Thêm cột `id_payee`/`id_payee_classify`/`invoice` *(khối ⑥⑦, editable + nhật ký, KHÔNG parity)* và `cdt1_cfa2_classify`/`alloc_method_classify` *(gợi ý ALLOCATE)*. §4b: ALLOCATE **không còn "chỉ đọc"** — máy suy làm **gợi ý mặc định**, kế toán **override tại Final**, máy chạy lại không đè *(chệch có chủ ý khỏi AS-IS công-thức-thuần)*. Engine P&L vẫn chỉ đọc 5 khối hợp đồng.
- **v1.2** (2026-08-24): §4b — **ALLOCATE là vùng MÁY SUY** (đọc công thức thật `AU/AV/AW`): `CFA1`=`cdt1`; `CFA2`/`Method`=`VLOOKUP(HDCode, Mapping Master)`. Thêm bảng `fls_mapping_master` (nguồn phân bổ, AC-C giữ). ⚠ Phụ thuộc dây chuyền: `HDCode` UNMAPPED ⇒ phân bổ kẹt. Mở `GAP-DB-05`.
- **v1.1** (2026-08-24): ⭐ **Thêm §0 — bản đồ đầy đủ 64 cột `ITL Ledge`, 4 vùng** (đọc live `A7:BI8`). Sửa thiếu sót v1.0: **thêm vùng ALLOCATE** (`cdt1_cfa1`/`cdt1_cfa2`/`alloc_method` — phân bổ venture) và **cột workflow** (`pic`/`audit_status`). Làm rõ `ITL Ledge` (64 cột) ≠ `Transaction Mapping L1` (36 canonical). Đính chính owner: **Final = kế toán nhập/sửa**, không phải công thức; bỏ tầng MID.
- **v1.0** (2026-08-24): Viết mới cho FLS. Schema `fls_itl` **ba lớp** *(14 hợp đồng + 36 canonical `jsonb` theo vị trí + lineage/run/song song)*; **5 cột `*_thyt`** và `canon` bắt buộc trong migration đầu *(`QĐ-ITL-35`)*; 9 bất biến `INV-*` → cưỡng chế PG; 6 bảng phụ gồm `fls_id_counter` *(pattern `fps_id_counter`)* và `fls_journal` 7 trường `AUD-1`. `le` = cột `P` *(SSOT, không dùng `BL`)*; khối 6–7 ngoài bảng.
