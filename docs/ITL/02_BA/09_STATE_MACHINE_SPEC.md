# 09 — STATE MACHINE SPEC

**Version:** v0.7 | **Chủ sở hữu:** COO-CFO | **Nguồn:** cấu trúc thật `ITL Ledge` (khuôn 4 cột `Classifying → Manual input → MID → Final`), `NGUỒN-BUILD` §7

> ⛔ **SỬA 2026-08-24 (owner + rà độc lập):** ⑴ **`Final` = ô kế toán NHẬP/SỬA**, không phải "giá trị kéo thẳng" — máy chỉ **gợi ý** vào Final ở chỗ chắc. ⑵ **Bỏ tầng `MID`** (áp mặc định cứng = "máy tự bịa", `INV-I16`). ⑶ ⭐ **`QĐ-owner-0824`:** máy trạng thái *(gợi ý → Final người sửa)* áp cho **cả 7 khối** *(gồm ⑥ `ID Payee`, ⑦ `Hoá đơn`)* **và vùng ALLOCATE** — kế toán sửa tay tại Final tất cả. Chỉ **5 khối** *(hd·pay_type·cdt1·svc_start·svc_end)* vào **hợp đồng P&L** *(có `*_thyt`/parity)*; khối ⑥⑦ + phân bổ sửa được nhưng **ngoài P&L**. ⑷ Vùng **ALLOCATE** (`CFA1/CFA2/Method`) máy **gợi ý** từ `Mapping Master` theo `HDCode`; kế toán **override** được, máy chạy lại **không đè** Final tay *(chệch có chủ ý khỏi AS-IS công-thức-thuần)*.

Năm máy trạng thái trung tâm. Tên trạng thái là **hợp đồng** — code lấy nguyên văn, không sáng tác biến thể (R-A2).

---

## SM-I01 · Dòng ITL (`itl_row`)

```
staged ──> mapped ──> raw_frozen ──> adjusted ──> allocated ──> audited ──> locked
   │          │                          │
   └─ rejected└─ unmapped                └─ reversed ──> adjusted
```

| Trạng thái | Nghĩa | Vào bằng |
|---|---|---|
| `staged` | Adapter đã xuất ra 36 cột canonical + ⭐ **cấp `itl_id` đóng băng (`INV-I04a`) và `content_key` (`INV-I04b`) NGAY LÚC NÀY** — danh tính có **TRƯỚC** khi join; chưa join LINK | S1 |
| `mapped` | Đã lookup LINK (PM/PI/PE) + chuẩn hoá LE — ⭐ **làm giàu dòng ĐÃ CÓ `itl_id`; KHÔNG sinh danh tính mới** | S3 |
| `unmapped` | Không lookup được khoá LINK bắt buộc — **giữ nguyên `itl_id` đã cấp ở `staged`**, không im lặng bỏ, phải đếm được | S3, `INV-I06`/`INV-I16` |
| `rejected` | DQ gate chặn (parse ngày lỗi, số dư lệch, thiếu trường bắt buộc) | S1–S2 |
| `raw_frozen` | Đã kết tinh vào `ITL RAW` — **bất biến từ đây** | S4, `INV-I03` |
| `adjusted` | Đã áp bút toán điều chỉnh (append-only, không ghi đè) | S5 |
| `allocated` | Đã áp bảng luật vùng ALLOCATE (`CDT1 CFA1` → `CDT1 CFA2`) | S5 |
| `audited` | Đã qua DQ test vùng AUDIT (đối chiếu `Report I General Ledger`) | S5 |
| `locked` | Kỳ đã ký chốt — không sửa được nữa | `SM-I05` |

**Luật:** `raw_frozen` là điểm không quay lui. Sửa sau điểm này **chỉ bằng bút toán mới**, không bằng sửa dòng cũ.

> ⭐ **Thứ tự danh tính — cú lật lõi so với AS-IS** *(rà 2026-08-25, `FLS-Process-PM-den-ITL` §3 chặng 7–8, `INV-I04a`):*
>
> | | AS-IS *(Gsheet)* | TO-BE *(FLS)* |
> |---|---|---|
> | **`itl_id` cấp khi nào** | **SAU mapping** — ở `Transaction Mapping L1`, `itl_id = "ITL#" & No`, mà `No = ROW()` trên bảng đã `SORT` theo ngày | **TRƯỚC mapping** — cấp ở `staged` lúc dòng vào sổ, rồi đóng băng |
> | **Hệ quả** | nhập lùi ngày ⇒ **đánh số lại toàn bộ** *(gốc 1.356 `FALSE` ở AUDIT)*; `No` rỗng khi thiếu tài khoản ⇒ `itl_id = "ITL#"` **mất khoá** | danh tính **bất động** với mọi sửa/sắp lại; dòng `unmapped` vẫn có khoá |
>
> ⇒ Trong máy trạng thái: **`staged` (nạp) là nơi sinh danh tính, KHÔNG phải `mapped` (ghép).** `mapped`/`unmapped` chỉ *làm giàu* dòng đã có `itl_id`. Đây là lý do `unmapped` không mất khoá — khác hẳn AS-IS.

## SM-I02 · Trường cần bổ sung (`itl_field`) — dẫn xuất từ khuôn thật

`ITL Ledge` AS-IS đã có sẵn máy trạng thái này dưới dạng 4 cột lặp lại 7 lần: `Classifying | Manual input | MID | Final`. Giá trị `Classifying` quan sát được trong file thật: `"Need to manual input"`. TO-BE giữ nguyên ngữ nghĩa, đặt tên rõ ràng:

```
inherited ────────────────────────────────> final
    │
needs_input ──> proposed_by_rule ──> approved ──> final
    │                                    ↑
    └────────> proposed_by_human ────────┘
```

| Trạng thái | Nghĩa | Tương đương AS-IS |
|---|---|---|
| `inherited` | Máy **gợi ý** từ nguồn (Classifying có giá trị) — kế toán không cần sửa | cột `Classifying` |
| `needs_input` | Nguồn không có giá trị — phải bổ sung | `Classifying` = `"Need to manual input"` |
| `proposed_by_rule` | Máy suy được từ bảng luật | *(chưa tồn tại AS-IS — đây là phần code hoá cứu được)* |
| `proposed_by_human` | Người nhập qua UI | cột `Manual input` |
| ~~`approved`~~ | ~~Người thứ hai duyệt (maker-checker)~~ | ⚠ **BỎ** theo `QĐ-ITL-16` — không có bước duyệt riêng. Từ `proposed_*` đi thẳng `final`, **kèm ghi nhật ký `AUD-1`** |
| `final` | Giá trị chốt, engine đọc — **kế toán nhập/sửa trực tiếp ở đây** (owner 2026-08-24) | cột `Final` |

**Áp cho 5 trường TRONG hợp đồng** (engine đọc — `QĐ-ITL-42`): `Budget Code (HDCode)` · `Loại giao dịch (Payment Type)` · `Chủ dự toán (CDT1)` · `Thời điểm bắt đầu dịch vụ` · `Thời điểm kết thúc dịch vụ`. ⛔ **Hai khối NGOÀI hợp đồng** — `Mã đối tác (ID Payee)` · `File đính kèm: Hoá đơn` — vẫn có máy trạng thái nhập tay nhưng thuộc gói adapter F, engine không đọc.

> ✅ **`QĐ-ITL-16` chốt giữ đúng như AS-IS**: người gõ là người chốt, không thêm bước duyệt. Bù lại **bắt buộc nhật ký thay đổi** (`BA-04` `AUD-1`). Máy trạng thái thành: `needs_input → proposed_by_rule|proposed_by_human → final`, mỗi chuyển đổi sinh 1 dòng nhật ký.

## SM-I03 · Bút toán điều chỉnh (`adjustment_entry`)

```
draft ──> submitted ──> approved ──> posted ──> reversed
   │          │
   └──────────┴──> withdrawn
```

| Chuyển | Điều kiện |
|---|---|
| `draft → submitted` | Đủ trường bắt buộc + trỏ đúng 1 `itl_id` tồn tại |
| ~~`submitted → approved`~~ | ⚠ **BỎ** (`QĐ-ITL-16`) — không có bước duyệt riêng |
| `submitted → posted` | Ghi vào journal — **append-only**, kỳ chưa `locked`, **bắt buộc sinh nhật ký `AUD-1`** |
| `posted → reversed` | Chỉ bằng **bút toán đảo mới**; bản gốc giữ nguyên. Nhật ký ghi `lý do` bắt buộc |

**Không có trạng thái `deleted`.** Không có đường nào từ `posted` về `draft`.

## SM-I04 · Lần chạy pipeline (`run`)

```
queued ──> running ──> dq_passed ──> reconciling ──> reconciled ──> published
              │            │                             │
              └─ failed    └─ dq_failed                  └─ discrepancy_open
                                                                │
                                                    (giải trình + ký) ──> reconciled
```

| Trạng thái | Nghĩa |
|---|---|
| `dq_failed` | Cổng chất lượng chặn — **pipeline dừng, báo người**, không chạy tiếp (`P-06`) |
| `discrepancy_open` | Đối soát oracle lệch, chưa phân loại xong. **Lệch cash-vs-accrual là hợp lệ** nhưng vẫn phải ghi lý do |
| `published` | Kết quả engine được phép đọc |
| `superseded` | Bị thay bởi run mới hơn cùng phạm vi — giữ lại để tái hiện, không xoá |

Mỗi `run` ghim version của cả 3 hợp đồng (`ORC-02` §1) ⇒ tái hiện được kết quả cũ.

## SM-I05 · Kỳ báo cáo (`period`)

```
open ──> cutoff ──> flash ──> reconciled ──> signed ──> locked
                       │           │
                       └───────────┴──> reopened (chỉ COO-CFO, ghi lý do)
```

| Trạng thái | Nghĩa |
|---|---|
| `cutoff` | Hết nhận giao dịch mới cho kỳ; nguồn chốt theo `Cut-off Date` (sheet `RAW ITLData Management` có sẵn cột này) |
| `flash` | Số nhanh, chưa đối soát đủ — **phải gắn cờ, không được trình bày như số chốt** |
| `signed` | Người có thẩm quyền ký (`RP-I*`) |
| `locked` | Mọi dòng ITL của kỳ chuyển `locked`; sửa chỉ bằng bút toán kỳ sau |

## SM-I06 · Mối nối tiền ↔ lệnh chi (`moi_noi`) — ghép / bỏ ghép *(mới v0.5, 2026-10-01 — `KQ-002 F-7`, `QĐ-ITL-149`)*

⛔ Trước bản này tệp ⛔ khai chuyển trạng thái nào cho ghép / bỏ ghép *(grep `ghép\|match` = **1** câu ghi chú)*, trong khi đường ghi ấy **đã chạy trên kho thật** *(UAT 01/10, itl `27728`)* ⇒ Test ⛔ có danh sách chuyển **cấm** để thử phá. Trạng thái ở đây là **PHÉP TÍNH** trên bảng chỉ-thêm *(`INV-I08`)* — ⛔ cột trạng thái nào được `UPDATE`.

Trạng thái của **một dòng tiền** *(`itl_id`)* về mặt mối nối:

```
                 ghép TAY (match, hinh='T')
 chua_ghep ─────────────────────────────────> da_ghep_tay ──┐
     │  ↑                                                    │ bỏ ghép (unmatch)
     │  └────────────────────────────────────────────────────┤ = THÊM fls_pm_unlink cho CẢ CHÙM
     │   máy ghép lúc nạp (hinh A/B/C)                       │
     └──────────────────────────────────────> da_ghep_may ───┘
```

| Trạng thái | Tính bằng | Đo 01/10 *(kho thật)* |
|---|---|--:|
| `chua_ghep` | ⛔ có dòng nào trong khung xem `fls_moi_noi` | `8.387 − 2.222` = **6.165** dòng tiền |
| `da_ghep_may` | có mối nối hiệu lực, mọi mối nối `hinh ∈ {A,B,C}` | **2.222** |
| `da_ghep_tay` | có mối nối hiệu lực `hinh='T'` | **0** *(1 cú UAT đã bỏ)* |

| Chuyển | Cửa | Điều kiện | Ghi *(một giao dịch)* |
|---|---|---|---|
| `chua_ghep → da_ghep_tay` | `POST /queue/{itl_id}/match` *(`BA-07 §3`)* · `match-lo` | kỳ ⛔ `locked` · Σ dòng lệnh khớp tiền bank trong dung sai `QĐ-ITL-63` · cùng tiền tệ · mã dòng lệnh có trong **ảnh PM hiệu lực** · `status='Approve'` *(hoặc `force`)* | `fls_pm_link` *(`hinh='T'`, `run_pm`)* + `fls_queue_event` `match` *(`actor` = người, `reason` hay lý do mặc định `(may dien)` — `BA-07 §4h ⓼`)* + ⭐ **gợi ý** `hd`/`cdt1` *(`SM-I02` ⇒ `proposed_by_rule`, `nguon='may_goi_y'` — `BA-05 DD-I15 ⓓd`)* |
| `chua_ghep → da_ghep_may` | lượt nạp *(`chay_nap.chen_moi_noi`)* | tự chứng *(`QĐ-ITL-57`)* | mối nối `hinh ∈ {A,B,C}` + gợi ý máy *(`may_ghep.ghi_goi_y_may`, actor `may@fls`)* |
| `da_ghep_* → chua_ghep` | `POST /queue/{itl_id}/unmatch` | kỳ ⛔ `locked` · có ≥1 mối nối hiệu lực | `fls_pm_unlink` cho **mọi** mối nối của dòng + `fls_queue_event` `unmatch` + **đảo** mọi bút toán gắn sự kiện `match` của dòng **chưa có bản đảo** — ⭐ **mọi lớp**, ⛔ chỉ lớp khung xem `fls_may_goi_y` đang trả *(v0.6 — `BA-10` v0.7 `DT-I14` nhánh 6–8, `INV-I22`; `BA-05 DD-I15 ⓓd`)*; ⛔ đảo giá trị **người** — khai `bo_qua` *(chỉ giá trị người — định nghĩa ở `DT-I14`)* |

⛔ **Chuyển CẤM** *(mỗi dòng là một bài thử phá cho `fls-test`)*:

| # | Chuyển cấm | Máy phải | Hôm nay |
|---|---|---|---|
| `F-1` | ghép một dòng **đã** ghép | `409 DaGhep` kèm mối nối đang có — muốn đổi thì bỏ cả chùm rồi ghép lại *(`QĐ-ITL-69`)* | ✅ mã |
| `F-2` | bỏ **lẻ** một mối nối trong chùm | cửa ⛔ nhận `pm_line_ids` ⇒ `400` | ✅ mã |
| `F-3` | ghép / bỏ ghép trong kỳ `locked` | `409` — ⛔ kể cả `force` *(`INV-I13`)* | ✅ mã |
| `F-4` | bỏ ghép dòng **chưa** ghép | `409 KhongCoMoiNoi` *(cố ý **khác** `DaGhep`)* | ✅ mã |
| `F-5` | ghép khi Σ lệch / khác tiền tệ | `422`, ⛔ ghi gì *(⛔ chia bừa)* | ✅ mã |
| `F-6` | `UPDATE`/`DELETE` một dòng `fls_pm_link`/`fls_pm_unlink`/`fls_adjustment` | ⛔ đường mã nào làm | ⚠ **chỉ giữ bằng mã** — ⛔ trigger *(`GAP-DB-06`, `BA-08 NFR-I01`)* |
| `F-7` | ⭐ cú ghép làm **đổi Final** `hd`/`cdt1` *(ghi `nguon='sua_tay'`)* | gợi ý đi `fls_may_goi_y`; `fls_sua_tay` ⛔ tăng | ⛔ **mã đang vi phạm** — sửa ở `WO-003` · ✅ `KQ-005 AC-5` *(vòng 1, mã `48fb68f`)* |
| `F-8` | bỏ ghép **đảo giá trị người** đã gõ sau cú ghép | ⛔ đảo, khai `bo_qua` | ✅ mã |
| `F-9` | thiếu `reason` ⇒ từ chối `match`/`unmatch` | nhận, điền lý do mặc định `(may dien)` | ⛔ **mã đang vi phạm** *(`KQ-002 F-1`)* — `WO-003` · ✅ `KQ-005 AC-1/AC-2` *(vòng 1)* |
| ⭐ `F-10` *(v0.6)* | bỏ ghép để lại **gợi ý mồ côi** — một lớp gợi ý bị đè **nổi lên lại** trên dòng **0** mối nối | đảo **mọi lớp** chưa đảo ⇒ `fls_may_goi_y` của dòng = **0** *(`INV-I22`)* | ⛔ **mã đang vi phạm** *(`KQ-005 F-1`, 2/2 kịch bản kho TEST; sổ thật **0** ca)* — `WO-003` vòng 2 · ✅ **đã chặn** *(v0.7 — mã `5fbc29c`, `KQ-007` ĐẠT `AC-13`/`AC-14`: bài `test_kq005_bo_ghep_dao_ca_goi_y_chong.py` gỡ `xfail`, `test_kq007_bo_ghep_moi_lop_pha_them.py`)* |
| ⭐ `F-11` *(v0.6)* | `bo_qua` chứa bút toán **máy** *(đã đảo lượt trước)* ⇒ màn nói *"người đã gõ tay"* khi ⛔ ai gõ | `bo_qua` = **chỉ** giá trị người | ⛔ **mã đang vi phạm** *(`KQ-005 F-2`)* — `WO-003` vòng 2 · ✅ **đã chặn** *(v0.7 — mã `5fbc29c`, `KQ-007` ĐẠT `AC-15`: bài `test_kq005_bo_qua_chi_la_gia_tri_nguoi.py` gỡ `xfail`)* |

⚠ Trạng thái **hàng chờ** *(`fls_queue_state`, `S1`…`S7`)* là **phép tính khác** — nó ⛔ được khai ở đây.

## Ma trận trạng thái × quyền

Ai được đẩy trạng thái nào: xem `04_ROLE_PERMISSION_MATRIX.md`. Ràng buộc enforce ở tầng DB: xem `11_INVARIANTS.md`.

## Changelog
- **v0.7** (2026-10-01 tối, `fls-ba`, `KQ-007 F-4 ⓑ`): cột trạng thái `F-10`, `F-11` thêm **✅ đã chặn** *(`WO-003` vòng 2, mã `5fbc29c`, `KQ-007` ĐẠT)*; chữ *"⛔ mã đang vi phạm"* **giữ** làm biên bản *(`Đ2`)* như `F-7`/`F-9`.
- **v0.6** (2026-10-01 tối, `fls-ba`, `KQ-005`): chuyển `da_ghep_* → chua_ghep` nay đảo **mọi lớp** bút toán gắn `match` chưa đảo *(`F-1`)*; thêm chuyển cấm **`F-10`** *(gợi ý mồ côi sau bỏ ghép — `INV-I22`)* và **`F-11`** *(`bo_qua` mang bút toán máy)* — cả hai **mã đang vi phạm** ⇒ `WO-003` vòng 2. `F-7`/`F-9` đạt ở vòng 1 *(`KQ-005`)*. Cột *Hôm nay* của `F-7`/`F-9` giữ chữ v0.5 làm biên bản, thêm phán quyết `KQ-005`.
- **v0.5** (2026-10-01, `fls-ba`, `KQ-002 F-7` + `QĐ-ITL-149`): ⭐⭐ **Thêm `SM-I06` — mối nối tiền ↔ lệnh chi:** 3 trạng thái *(phép tính trên `fls_moi_noi`, đo 01/10: `6.165` · `2.222` · `0`)*, 3 chuyển hợp lệ, **9 chuyển CẤM** `F-1`…`F-9` cho `fls-test` thử phá — `F-7` *(cú ghép đổi Final)* và `F-9` *(thiếu `reason` ⇒ từ chối)* là chỗ **mã đang vi phạm** quyết định owner 01/10 ⇒ `WO-003`. Gợi ý `hd`/`cdt1` từ cú ghép nối vào `SM-I02` ở trạng thái `proposed_by_rule`, ⛔ `final`.
- **v0.4** (2026-08-25): Rà lại thứ tự danh tính từ `FLS-Process-PM-den-ITL` §3 chặng 7–8. **`SM-I01` sửa lỗi logic AS-IS**: *"sinh ITL ID"* dời từ trạng thái `mapped` (SAU mapping) → `staged` (lúc nạp, TRƯỚC mapping) theo `INV-I04a`; `mapped`/`unmapped` chỉ **làm giàu** dòng đã có `itl_id`, nên `unmapped` **không mất khoá**. Thêm bảng cú-lật AS-IS↔TO-BE + bằng chứng *(1.356 `FALSE`, `No` rỗng ⇒ `ITL#` mất khoá)*.
- **v0.3** (2026-08-24): Đính chính owner + rà độc lập — **`Final` = kế toán nhập/sửa** (không phải kéo thẳng); **bỏ tầng MID**; áp cho **5 trường trong hợp đồng** (khối 6–7 ngoài); ghi **ALLOCATE máy suy từ Mapping Master**.
- v0.2 (2026-08-19): **`QĐ-ITL-16`** — bỏ trạng thái `approved` khỏi `SM-I02` và `SM-I03`; mọi chuyển đổi bắt buộc sinh nhật ký `AUD-1`.
- v0.1 (2026-08-18): Khởi tạo — 5 máy trạng thái. `SM-I02` **dẫn xuất trực tiếp từ khuôn 4 cột có thật** trong `ITL Ledge`; phát hiện AS-IS thiếu bước `approved` (`GAP-ITL-03`).
