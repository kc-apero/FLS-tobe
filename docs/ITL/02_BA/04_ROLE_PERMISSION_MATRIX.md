# 04 — ROLE & PERMISSION MATRIX

**Version:** v0.3 | **Chủ sở hữu:** COO-CFO | **Nguyên tắc:** tách quyền tạo–duyệt (SoD), đặc biệt ở điều chỉnh ITL & treasury

---

## 0. ⭐⭐ ĐỌC TRƯỚC — ba vai người + một vai máy *(`QĐ-ITL-27`, 22/08)*

> ⛔⛔ **Mục §1–§2 bên dưới mô tả một hệ 10 vai có tách quyền tạo–duyệt. Hệ ấy
> ⛔ KHÔNG TỒN TẠI.** Giữ lại làm **biên bản**, ⛔ không phải làm căn cứ build.

**Lý do khai tử là lý do vận hành, ⛔ không phải lý do thiết kế:** luồng
`PM → ITL` thật sự chỉ có **2–3 kế toán**; kế toán trưởng và CFO-COO **hầu như
không tham gia**. ⇒ Một bước duyệt sẽ **leo vào chỗ trống** — nó trông như
kiểm soát mà ⛔ không ai đứng ở đó.

⇒ **8 vai → 3 vai người + 1 vai MÁY. ⛔ KHÔNG leo cấp.**

| Vai | Người thật | Làm gì | Vai cũ tương ứng |
|---|---|---|---|
| `AC-A` Kế toán tiền | ThomHT · AnhMC · ThuongCT | nạp sao kê · thu chi quỹ · số dư | `RP-I01` · `RP-I06` |
| `AC-B` Kế toán phân loại | **LAN · THƯƠNG** | gõ **7 trường** · xử hàng chờ | `RP-I03` |
| `AC-C` Giữ danh mục | *(kiêm nhiệm)* | tài khoản · quỹ · `Mapping Master` | `RP-I02` |
| **`MÁY`** | hệ thống FLS | ghép · phân loại · cấp `itl_id` · xếp hàng chờ · **nhật ký** · **từ chối giá trị sai** | thay `RP-I04` · `RP-I11` |

⛔ **Ba vai bị khai tử, ⛔ không được hồi sinh:**

| Vai chết | Vì sao |
|---|---|
| `RP-I04` Adjustment checker | `QĐ-ITL-16` — người gõ là người chốt, y như Gsheet |
| `RP-I11` Nhật ký reviewer | `QĐ-ITL-27` — **⛔ không có người soi, và sẽ ⛔ không có**. Nhật ký giữ lại vì một lý do khác: **để việc sống sót khi một người rời đi** |
| `RP-I07` Period signer | ⚠ **Chưa có người nhận, và chưa có nút.** `GAP-PLAN-04`: chốt kỳ ⛔ chưa được đặc tả. Màn `F03` **tự khai** điều này thay vì vẽ một nút chết |

⭐⭐ **Rủi ro số một ⛔ KHÔNG phải gian lận — mà là MỘT NGƯỜI RỜI ĐI.** Đó là
lý do nhật ký `AUD-1` vẫn bắt buộc dù ⛔ không ai soi nó theo nhịp.

### 0b · MÁY kiểm soát bằng gì — *danh sách đo được* `(2026-09-04)`

| Máy chặn cái gì | Cưỡng chế ở đâu | Bằng chứng |
|---|---|---|
| Sổ ⛔ không bị sửa đè | `INV-I03`/`INV-I08` — trigger tầng **DB** | `trg_fls_itl_inv_i03` |
| Ghi mà ⛔ không nói lý do | `INV-I16` — cửa **NO** | `FLS-UNMAPPED-HIDDEN` |
| Mã hợp đồng **bịa ra** | `DT-I09` — cửa ghi tra `Mapping Master` **73 mã** | `FLS-UNKNOWN-CODE` |
| Kỳ dịch vụ sai khuôn | `DT-I09` #6 — khuôn `YYYYMM` | `FLS-BAD-FORMAT` |
| Ghi vào **kỳ đã chốt** | `INV-I13` — kể cả có `force` | `FLS-LOCKED-PERIOD` |
| Gõ **khác nguồn** mà ⛔ không nói | `US-025` — `409` + bắt buộc lý do | `FLS-CONFLICT-SOURCE` |
| Cửa **tự mở đường ghi** | `--cho-ghi` **mặc định TẮT**; kết nối chỉ-đọc ở tầng **PostgreSQL** | `tools/chay_cua.py` |

⚠ **Và máy ⛔ KHÔNG chặn được ba thứ** — khai ra chứ ⛔ không giấu:
`GAP-SCR-09` *(hai người sửa một ô)* · ba danh sách **suy** ⛔ không được ép
*(`INV-I18` — vòng tròn)* · và **danh mục rỗng thì máy ⛔ KHÔNG BIẾT**, ⛔ chứ
không phải *"mọi mã đều sai"* *(`INV-I17`)*.


---

## 1. Vai trò hệ thống *(⛔ BIÊN BẢN — xem §0)*

| ID | Vai | Ai giữ (AS-IS) | Mô tả |
|---|---|---|---|
| `RP-I01` | **Data ingest operator** | Data | Nạp nguồn, chạy lại adapter khi lỗi. Không sửa số |
| `RP-I02` | **Mapping steward** | SHQ1 / SHQ2 | Duy trì `MAPPING-MASTER`: LE, HD/COA, luật phân bổ |
| `RP-I03` | **Adjustment maker** | LAN · THƯƠNG | Nhập giá trị cho trường `needs_input`; tạo bút toán điều chỉnh |
| ~~`RP-I04`~~ | ~~Adjustment checker~~ | — | ⚠ **Vai này BỊ BỎ** theo `QĐ-ITL-16`. Không có bước duyệt riêng cho bút toán điều chỉnh |
| `RP-I11` ⭐ | **Nhật ký reviewer** | `???` `GAP-ITL-24` | **Hậu kiểm**: soi nhật ký thay đổi (`AUD-1`) theo nhịp. Đây là kiểm soát **duy nhất** còn lại — không có người soi thì hậu kiểm vô nghĩa |
| `RP-I05` | **HR ledger owner** | HR | Sở hữu nguồn H1000 + audit balance HR |
| `RP-I06` | **Treasury / reconciler** | Thủ quỹ | Cổng đối soát tiền, xử lệch số dư |
| `RP-I07` | **Period signer** | Kế toán trưởng | Ký chốt kỳ (`SM-I05`: `signed`) |
| `RP-I08` | **Contract owner** | Tech Lead | Sở hữu `ITL-CONTRACT`; bump version |
| `RP-I09` | **Orchestrator** | COO-CFO | Mở lại kỳ đã chốt, duyệt CR, quyết cổng milestone |
| `RP-I10` | **Engine / consumer** | FPA-T4 (hệ thống) | **CHỈ ĐỌC** `ITL Ledge`. Không có quyền ghi ở bất kỳ đường nào |

> ⚠ **`QĐ-ITL-16` giữ nguyên cách làm của Gsheet**: người gõ là người chốt. Lỗ hổng tiền-kiểm **không được bịt bằng bước duyệt** mà bằng **hậu kiểm** — nhật ký `AUD-1` + vai `RP-I11`. Nếu `GAP-ITL-24` không có người nhận, hệ TO-BE **kém an toàn hơn** Gsheet hiện tại (Gsheet còn version history của Google).

## 2. Ma trận quyền × hành động

| Hành động | I01 | I02 | I03 | I04 | I05 | I06 | I07 | I08 | I09 | I10 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Chạy/chạy lại adapter | ✅ | | | | ✅¹ | | | | ✅ | |
| Sửa `MAPPING-MASTER` (tạo version mới) | | ✅ | | | | | | | ✅ | |
| Ký duyệt version `MAPPING-MASTER` | | | | | | | ✅ | | ✅ | |
| Nhập giá trị `needs_input` | | | ✅ | | ✅¹ | | | | | |
| Tạo bút toán điều chỉnh (`draft→submitted`) | | | ✅ | | | ✅² | | | | |
| ~~Duyệt bút toán~~ *(bỏ — `QĐ-ITL-16`)* | | | — | — | | | — | | — | |
| **Soi nhật ký thay đổi** (hậu kiểm) | | | | | | | ✅ | | ✅ | |
| Post bút toán (`submitted→posted`) | | | ✅ | — | | | ✅ | | | |
| Đảo bút toán (`posted→reversed`) | | | ✅ | — | | | ✅ | | ✅ | |
| Xử lệch đối soát tiền | | | | | | ✅ | ✅ | | | |
| Đẩy kỳ `cutoff→flash` | ✅ | | | | | | ✅ | | | |
| Ký chốt kỳ (`→signed`) | | | | | | | ✅ | | | |
| Khoá kỳ (`→locked`) | | | | | | | ✅ | | ✅ | |
| **Mở lại kỳ đã chốt** (`reopened`) | | | | | | | | | ✅ | |
| Bump version `ITL-CONTRACT` | | | | | | | | ✅ | ✅ | |
| Đọc `ITL Ledge` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Ghi vào `ITL Ledge`** | | | | | | | | | | ❌ |

¹ chỉ trong phạm vi nguồn HR · ² chỉ bút toán liên quan tiền/tỷ giá

**Ô ❌ là ràng buộc cứng**, không phải quy ước: `RP-I10` (engine) **không có đường ghi nào** vào `ITL Ledge`.

> Cột `I04` giữ lại để đọc được lịch sử — vai đã bỏ (`QĐ-ITL-16`), mọi ô là `—`. `RP-I03` **được** post bút toán của chính mình; đổi lại mỗi lần post sinh một dòng nhật ký `AUD-1`.

## 3. Ràng buộc bắt buộc — 2 SoD + 1 AUD

| # | Ràng buộc | Enforce |
|---|---|---|
| ~~**SoD-1**~~ | ~~`maker ≠ checker` trên mọi bút toán điều chỉnh~~ | ⚠ **KHÔNG ÁP DỤNG** — `QĐ-ITL-16` chốt giữ như Google Sheets: người nhập là người chốt. **Thay bằng `AUD-1`** dưới đây |
| **SoD-2** | Người sửa `MAPPING-MASTER` ≠ người ký duyệt version đó | DB check constraint |
| **SoD-3** | Chỉ `RP-I09` mở lại được kỳ đã `signed`, và **phải ghi lý do** | DB + trường `reopen_reason NOT NULL` |
| **AUD-1** ⭐ | **Mọi thay đổi bút toán điều chỉnh phải vào nhật ký**: `itl_id` · trường · giá trị **trước→sau** · người · thời điểm · nguồn giá trị (máy suy/người nhập/sửa lại) · **lý do** (bắt buộc khi sửa lại giá trị đã có) | DB: journal insert-only, `NOT NULL` trên 7 trường; UI = `S2` |

## 4. Nguyên tắc đặt tên — không gắn người vào dữ liệu

File AS-IS đang nhúng tên người vào **cấu trúc dữ liệu**: cột `PIC: LAN + THƯƠNG`, `PIC: THƯƠNG` (7 chỗ trong `ITL Ledge`), cột `PIC` ở vùng AUDIT, `Luận's File` trong tên workbook.

**TO-BE:** người là **thuộc tính của hàng chờ việc** (`assignee`, `approver`), không phải **tên cột**. Đổi người phụ trách không được làm đổi schema.

## 5. GAP

| ID | Câu hỏi | Ai đóng |
|---|---|---|
| ~~`GAP-ITL-03`~~ | ~~Ai giữ vai adjustment checker?~~ | **CLOSED** — `QĐ-ITL-16`: không có vai này |
| `GAP-ITL-24` ⭐ | Ai giữ vai `RP-I11` (soi nhật ký) và theo nhịp nào? **Không có người soi thì `AUD-1` vô nghĩa** | COO-CFO |
| `GAP-ITL-13` | Có cần tách quyền theo **pháp nhân** không (người của LE này không thấy dữ liệu LE khác)? | COO-CFO |

## Changelog
- **v0.3** *(2026-09-04, `QĐ-ITL-27`)*: ⭐⭐ **Đóng `GAP-DOC-01`** — bản v0.2 (19/08) viết **trước `QĐ-ITL-27` ba ngày** nên lạc hậu 3 quyết định. Thêm **§0: ba vai NGƯỜI + một vai MÁY**. ⛔ **Lý do khai tử là lý do VẬN HÀNH, ⛔ không phải lý do thiết kế:** luồng `PM → ITL` thật sự chỉ có **2–3 kế toán**; kế toán trưởng và CFO-COO hầu như không tham gia, nên một bước duyệt sẽ **leo vào chỗ trống** — trông như kiểm soát mà ⛔ không ai đứng ở đó. ⇒ `RP-I04` **chết** *(`QĐ-ITL-16`)* · `RP-I11` **chết** *(`QĐ-ITL-27` — ⛔ không có người soi, và sẽ ⛔ không có)* · `RP-I07` **chưa có người nhận VÀ chưa có nút** *(`GAP-PLAN-04`)*. Thêm **§0b**: danh sách **ĐO ĐƯỢC** *"máy kiểm soát bằng gì"* — **7 phép chặn**, kèm **3 thứ máy ⛔ KHÔNG chặn được**, khai thẳng chứ ⛔ không để người đọc tự suy. ⭐ **Rủi ro số một ⛔ không phải gian lận mà là MỘT NGƯỜI RỜI ĐI** — đó là lý do nhật ký `AUD-1` vẫn **bắt buộc** dù ⛔ không ai soi nó theo nhịp. **§1–§2 cũ GIỮ NGUYÊN làm biên bản, ⛔ không xoá**
- v0.2 (2026-08-19): **`QĐ-ITL-16`** — bỏ vai `RP-I04` adjustment checker và ràng buộc `SoD-1`; thêm `AUD-1` (nhật ký thay đổi bắt buộc, 7 trường) + vai `RP-I11` nhật ký reviewer. Kiểm soát chuyển từ tiền kiểm sang hậu kiểm. Mở `GAP-ITL-24`.
- v0.1 (2026-08-18): Khởi tạo — 10 vai, ma trận 16 hành động, 3 ràng buộc SoD, luật cấm nhúng tên người vào schema.
