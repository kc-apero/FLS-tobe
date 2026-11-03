# 07 — CHANGE CONTROL: xử lý thay đổi

**Version:** v1.4 · **Cập nhật:** 2026-09-07 | **Chủ sở hữu:** COO-CFO

---

## 1. Phân loại thay đổi — 4 đường khác nhau

| Loại | Ví dụ | Đường xử lý |
|---|---|---|
| **1 · Thay đổi REFERENCE DATA** | thêm mã LE, sửa mapping tài khoản→mã, đổi `Method to Allocate to CFA2`, thêm `Code HR Allocate` | **KHÔNG sửa doc/code** — tạo **version mới của `MAPPING-MASTER`**, người nghiệp vụ thao tác qua UI, có sign-off, hiệu lực từ kỳ được chỉ định (`P-05`). Doc chỉ sửa nếu *cấu trúc* bảng đổi |
| **2 · Thay đổi SPEC/CODE** | thêm adapter, đổi state machine, thêm DQ test, thêm màn hình | Quy trình CR §2 |
| **3 · Thay đổi HỢP ĐỒNG** ⚠ | thêm/bớt/đổi ngữ nghĩa cột trong `ITL-CONTRACT` hoặc `ITL-CANON` | **Loại nặng nhất.** Quy trình CR §2 + **3 điều kiện cứng** §3 |
| **4 · TRÔI KẾ THỪA** | bản chương trình FIN ERP tăng version ở 1 trong 6 khối kế thừa (`../00_MASTER_INDEX §5`) | Mở CR, rà bản chép trong kit ITL, cập nhật version ghim. **Không tự gộp/tự chọn bên nào đúng** — nếu 2 bản đã lệch nội dung thì đó là R-A4: dừng, báo GAP |

## 2. Quy trình CR (loại 2 & 3)

1. **Ghi nhận:** **`CR#<số>`** vào sổ §5, nêu nguồn phát sinh (bug, yêu cầu vận hành, gap review, schema nguồn đổi).
   > ⛔ **Dạng `CR-ITL-<số>` của v0.1 đã khai tử.** Thực tế hai CR đầu được đặt là `CR#1`/`CR#2`, và cái tên đó đã đi vào `00_MASTER_INDEX`, `03_Dev/09`, `03_Dev/10`, **và mã nguồn** *(`fls/contract/itl_contract.py`: `CR_DANG_MO`)* cùng test khoá nó. Giữ hai cách đặt tên song song là dựng sẵn một chỗ lệch — nên **`CR#<số>` là dạng sống**, dạng cũ bỏ.
2. **Đánh giá lan toả:** liệt kê file 3 kit bị ảnh hưởng. Sửa `BA-05` / `BA-09` / `BA-10` / `BA-11` ⇒ **bắt buộc** rà `TEST-03` truy vết.
3. **Duyệt:** chạm hợp đồng hoặc chạm tiền/duyệt/chữ ký → Diễn đàn quản trị; còn lại → COO-CFO.
4. **Thực thi:** sửa **spec trước** → tăng version + changelog → rồi mới sửa code (spec-first).
5. **Đóng:** cập nhật `06` dashboard; nếu chạm truy vết → cập nhật `TEST-03`.

## 3. Ba điều kiện cứng cho CR chạm hợp đồng (loại 3)

Vì lệch hợp đồng là **rủi ro #1** của dự án (cutover gãy), CR loại 3 không được duyệt nếu thiếu bất kỳ điều nào:

| # | Điều kiện |
|---|---|
| **C1** | **Test tương thích engine** chạy PASS — chứng minh engine P&L vẫn đọc được ITL sau thay đổi. Không có test ⇒ không duyệt |
| **C2** | **Đối soát oracle lại** phần dữ liệu bị ảnh hưởng — số không được đổi vì lý do "sửa hợp đồng" mà không giải trình được |
| **C3** | **Bump version `ITL-CONTRACT`** + ghi vào manifest milestone đang chạy (`02` §5). Sửa hợp đồng mà không bump version = vi phạm nặng nhất bộ này |

> Thay đổi hợp đồng **tương thích ngược** (thêm cột mới, không đổi cột cũ) vẫn phải qua C1–C3, chỉ được rút gọn ở bước duyệt (COO-CFO thay vì Diễn đàn QT).

## 4. Xử lý khi schema NGUỒN đổi (tình huống thường gặp nhất)

Không phải CR ngay — trước tiên adapter phải **fail-loud** (`P-06`): dừng, báo, không âm thầm ra 0 dòng.

```
schema nguồn đổi → adapter fail-loud → phân loại:
   ├─ chỉ đổi tên/thứ tự cột nguồn   → sửa map trong adapter, bump adapter version. KHÔNG phải CR
   ├─ nguồn thêm trường ITL cần      → CR loại 3 (đụng ITL-CANON)
   └─ nguồn mất trường ITL đang dùng → CR loại 3 + báo GAP: dữ liệu không còn tồn tại
                                        là vấn đề nghiệp vụ, không phải vấn đề code
```

## 5. Sổ CR

> ⛔⛔ **Sổ này đã già đi trong im lặng hai ngày.** Từ 25/08 tới 27/08 sổ vẫn ghi
> *"chưa có CR nào"* trong khi `CR#1` đã đóng và `CR#2` đã mở **rồi đóng** — cả hai
> sống ở `00_MASTER_INDEX` và ở mã nguồn, **không ở đây**. Đó đúng là kiểu lỗi bộ
> tài liệu này dựng ra để chặn: **một chỗ nói thật, một chỗ nói cũ, và không cái gì
> báo gì.** Điền lại bên dưới, và §7 thêm một cổng để lần sau không lặp.

| ID | Ngày mở | Mô tả | Loại | Ảnh hưởng | Trạng thái |
|---|---|---|---|---|---|
| **`CR#10`** | 2026-09-07 | ⭐⭐⭐ **MỞ PHẠM VI — hai màn NHẬP vào FLS** *(`QĐ-ITL-90`, owner nguyên văn: *"FLS bao gồm các giao diện nhập Bank Transaction và Cash Ledger như trên ggsheet và có thao tác mapping PM với Transactions"*)*. ⛔⛔ **Nó LẬT `QĐ-ITL-23`** — quyết định 22/08 chốt Google Sheets giữ vai nhập liệu thô **VĨNH VIỄN** cho 4 nhóm; nay **2/4 bị lấy lại** *(nạp sao kê · nhập số dư thật)*. Hẹp luật **`T4`**; **hồi sinh màn `S4`** đã BỎ. ⭐ Phần *ghép PM ↔ Transaction* là **xác nhận** *(`QĐ-ITL-48` + `QĐ-ITL-61` + `QĐ-ITL-80` — đã chạy thật)*, ⛔ không phải việc mới | **1** *(chạm **phạm vi** — mức nặng nhất §2)* | `00_MASTER_INDEX` §2 · `BA-01` §4 · `Lo-trinh-Chuyen-doi-Gsheet-to-UI` §0b·§3·§7·§8 · `BA-06` `GAP-SCR-10` · lộ trình **4 → 6 màn** | ⏳ **MỞ** — ⛔ 3 câu chưa ai trả lời: **`GAP-SCOPE-01`** *(tầng sao kê thô **60+ định dạng** có vào phạm vi không — lý do gốc của `T4` ⛔ không biến mất)* · **`GAP-SCOPE-02`** *(P100 còn được ghi nữa không; nếu **có** thì đó là **ghi đôi**, thứ `QĐ-ITL-32` đã bỏ)* · **`GAP-SCR-10`** *(⛔ chưa có `SCREEN_SPEC` cho `F04`/`F05`; ⛔ không bịa — `R-A1`)*. ⛔ **Chưa có gì để nghiệm thu** — 3 câu trên là **nghiệp vụ**, ⛔ không phải việc máy |
| **`CR#9`** | 2026-08-28 | ⛔⛔ **`BA-07` §2 ⛔ KHÔNG có đường nào GỠ một mối nối đã ghép** — nên ghép sai là một dòng **chết cứng**: `POST /match` lần hai trả `409`, và ⛔ không cửa nào bỏ mối nối cũ. Đặc tả tả **một chiều** của thao tác ghép | **2** *(chạm `BA-07` + khuôn kho; ⛔ không chạm hợp đồng 14 trường)* | `BA-07` §2 *(thêm `POST /queue/{itl_id}/unmatch`)* · `DEV-04` *(migration `0013`)* · `GAP-JOIN-05` | ✅ **ĐÓNG 2026-08-28** — chứng cứ: **34 phép thử mới** *(663 xanh)*, `pg_verify` **khớp 17 bảng/view** trên **kho thật**, và **4 cơ chế đã bị phá có chủ ý để xem cổng có ĐỎ thật**. ⚠ Ghi rõ **hai chỗ đặc tả cũ đoán SAI hình dạng**: ⓐ *"thêm một cột `đã bỏ`"* — ⛔ không được, đổi cột ấy cần một câu `UPDATE`; ⓑ khoá `(itl_id, pm_line_id)` — phải **đổi**, vì nó chặn *ghép lại đúng dòng lệnh vừa gỡ* |
| **`CR#8`** | 2026-08-28 | ⛔⛔ **`52 cột` của `CR#7` là THIẾU, số đúng `55`** — và nguyên mẫu in 38 tiêu đề canon bằng **chữ cái**, để **chỉ-đọc**, nên **5/10 trường người gõ** ⛔ không gõ được. Owner báo thiếu 2 trường; đo ra thiếu **5** | **2** *(chạm spec màn hình + nguyên mẫu, ⛔ không chạm hợp đồng/sổ)* | `BA-06` §6b *(khối cảnh báo)* · `GAP-SCR-03`; ⛔ **không** sửa `CR#7` *(sửa chữ trong biên bản là viết lại lịch sử)* | ✅ **ĐÓNG 2026-08-28** — chứng cứ: `tools/do_luoi_f02.py` đo lại ****55 cột** *(38 canon + 14 hợp đồng + **3 trường ghi không có nhà**)* · **748 dòng** một lát · **41.140 ô** · **10/10 trường ghi gõ được** *(bản 27/08 chỉ **5/10**)***; `tools/mui_thu_luoi.py` sinh lại tệp *(748 × 55 = 41.140 ô)*; bài `test_dung_10_cot_sua_duoc` **đổi từ `== 5` sang `== TRUONG_GHI`** nên nó khoá **cả mười** |
| **`CR#7`** | 2026-08-27 | ⛔⛔ **Tiền đề bài toán lưới `F02` bị ĐO LẬT — cả ba con số.** `BA-06` §6b chọn thư viện dựa trên *"~64 cột × vài nghìn dòng, chỉ 5 cột sửa được"*; đo trên kho thật ra **52 cột · 10 cột sửa được · 748 dòng một lát**. ⇒ bài toán là **~39.000 ô**, ⛔ không phải ~192.000, nên **ảo hoá có thể không cần** — mà ảo hoá là lý do CHÍNH để chọn `react-datasheet-grid`. Tiền đề đổ ⇒ **quyết định phải xem lại** | **2** *(chạm spec màn hình, ⛔ không chạm hợp đồng/sổ)* | `BA-06` §6b + `GAP-SCR-01`/`GAP-SCR-03`; ⛔ **không** sửa bảng khảo sát 24/08 *(sửa chữ trong biên bản là viết lại lịch sử)* | ✅ **ĐÓNG 2026-08-27** — chứng cứ: `tools/do_luoi_f02.py` *(đo trên kho thật)* + nguyên mẫu `tools/mui_thu_luoi.py` *(748 × 52 = 38.896 ô, cả 8 hành vi §1, không thư viện)* + **11 phép thử** `tests/api/test_mui_thu_luoi.py` **đã diễn tập đỏ 4 nhánh** |
| **`CR#6`** | 2026-08-27 | ⛔⛔ **`BA-07` §2: thân yêu cầu `/match` là `{pm_id}` — SAI trục.** Đo trên 3.703 dòng lệnh thật: `reference` và tiền sống ở **DÒNG**, và **526 phiếu mang 2–36 reference khác nhau** ⇒ ghép vào phiếu thì **máy phải tự chọn dòng** = máy quyết thay người *(`INV-I16`)*. Thân đổi thành `{pm_line_ids: [...]}`; gửi `{pm_id}` ⇒ **400 kèm lý do**. Cùng loại với `CR#5`: **sửa đặc tả, ⛔ không sửa code cho khớp đặc tả sai** | **3** *(chạm đặc tả cửa)* | `BA-07` §2 · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` — ⛔ **không** chạm sổ, ⛔ không chạm hợp đồng 14 trường | ✅ **ĐÓNG 2026-08-27** — chứng cứ: `526` phiếu đa-reference · bài `test_gui_ma_PHIEU_thay_vi_ma_DONG_thi_400_kem_ly_do` · **14 phép thử** `tests/api/test_cua_ghep_pg.py` · migration `0011` |
| **`CR#5`** | 2026-08-27 | ⛔⛔ **`BA-07` §3: *"trường hợp-đồng cập nhật `*_thyt`"* là SAI.** Sai `INV-I08` *(sổ append-only)* **và** `QĐ-ITL-35` *(`*_thyt` là cột đo parity — ghi giá trị người gõ vào đó là bỏ bàn tay vào cái thước)* | **2** *(spec/code)* | `02_BA/07` §3 → **v1.3** · migration `0010` *(khung xem `fls_sua_tay`)* · `fls/repo/ghi_tay.py` · `02_BA/05` ERD | ✅ **ĐÓNG 27/08** — chứng cứ: `test_khong_mot_cot_nao_cua_fls_itl_bi_doi` *(so 17 cột trước/sau)* + `tools/verify_cua_ghi.py` chạy cả vòng ghi qua HTTP: **sổ không đổi một ô**. ⭐ **Sửa đặc tả, ⛔ không sửa code cho khớp đặc tả sai** |
| **`CR#4`** | 2026-08-27 | ⛔⛔ **Khung xem `fls_queue_xep_tien` *(dựng 27/08, migration `0008`)* ⛔ không mang được PHẠM VI.** Khung xem SQL không nhận tham số; hai đường duy nhất đều sai: **không lọc** ⇒ `hang`/`luy_ke_pct` tính **trước** khi ai kịp lọc *(và lọc ở đầu ra ⛔ không sửa được thứ tự đã xếp sai)* · **nhét bản trắng vào khung xem** ⇒ kho TEST trả rỗng, phép xếp ⛔ không còn bài nào đo được | **2** *(spec/code)* | migration `0009` *(bỏ khung xem)* · `fls/db/schema.py` · `fls/repo/doc_bao_cao.doc_hang_cho()` · `02_BA/05` ERD · `02_BA/06` màn `F01` · `QĐ-ITL-58` | ✅ **ĐÓNG 27/08** — chứng cứ: **492 phép thử**; ⭐ bài `test_dong_cua_run_LA_lam_LECH_luy_ke` cho **hai con số trên CÙNG một dòng sổ**: trong phạm vi **hạng 1 · 70,00%**, đọc cả kho **hạng 2 · 99,97%**. Đây là bài mà khung xem ⛔ **không bao giờ viết được**, và nó là lý do thật của `CR#4` |
| **`CR#1`** | 2026-08-25 | **Mô hình ghép PM** — `reference_number` nằm ở **phiếu** *(không ở dòng)* ⇒ bỏ luật `OP-03` bất khả, thay bằng **slip-join + amount-split + `line_id` làm định danh dòng** | **2** *(spec/code)* | `03_Dev/09_CR1_PM_JOIN_MODEL` v1.0 *(mới)* · `03_Dev/10` · hẹp `GAP-ERD-10` + `GAP-ITL-58` · wireframe `F01` thêm nút **Ghép** *(`QĐ-ITL-48`)* | ✅ **ĐÓNG 25/08** — chứng cứ: `03_Dev/09` v1.0 + **test DOM trên wireframe `F01`** *(5 nút Ghép; `ITL#4471` có `reference` bank ⇒ `PM02279` xếp đầu "ref khớp"; 2 dòng lệnh, Σ = **1.894.982.832** = đúng tiền bank ⇒ nút xác nhận **bật**; dòng lệch Σ ⇒ **chặn**)*, commit `4608869`. ⚠ Nhưng xem hàng dưới: **tiền đề của chính nó bị đo lật ngày 27/08** |
| **`CR#1-a`** | 2026-08-27 | ⛔ **Tiền đề của `CR#1` sai:** `reference` **KHÔNG** ở phiếu, nó ở **DÒNG** — đo được **526/1.468 phiếu mang 2–36 mã KHÁC NHAU**, tiền cũng khác nhau từng dòng *(493/579 phiếu nhiều dòng)*. Kèm rút con số *"289 dòng dư bị bỏ im lặng"* — **không tái lập được** từ nguồn | **2** | `03_Dev/10` lên **v0.2 §1a** *(3 tiền đề bị lật)* · sửa `03_Dev/03` §5.7 · ⛔ **không** làm `T-JOIN-03` *(tách 1 dòng bank thành N dòng sổ **vỡ thế 1–1 sổ↔nguồn** mà mọi cổng đối soát dựa vào, đổi lại 27 dòng)* ⇒ mở `GAP-JOIN-03` | ✅ **ĐÓNG 27/08** *(spec đã sửa, code đã theo spec mới, 26 phép thử)* |
| **`CR#3`** | 2026-08-27 | ⚠ **Tiền đề của `QĐ-ITL-28` bị owner lật.** `QĐ-ITL-28` dựng **ba trạng thái** *(`có lệnh` / `KHÔNG CẦN LỆNH + tên loại` / `chưa biết`)* trên con số *"3.480 dòng / 92% tiền **vốn không cần** lệnh chi"*. `QĐ-ITL-56` *(27/08)*: **không có quy định nào** nói khoản nào cần lệnh chi ⇒ *"vốn không cần"* là **xét đoán của người đo**, và trạng thái giữa **không có nguồn** | **2** *(spec/code)* | `US-KT-036` **khai tử** · tầng `T0` ra khỏi bậc thang ghép · `02_BA/06_SCREEN_SPEC` màn `F01` *(lọc theo nhãn)* · `QĐ-ITL-28` | ✅ **ĐÓNG 27/08** — owner chốt **BỎ HẲN** trạng thái giữa *(`QĐ-ITL-58`)*. Chứng cứ: `work_status` chỉ có **2** giá trị ở tầng kho *(đã khoá bằng test)*; thay thế là khung xem `fls_queue_xep_tien` *(migration `0008`, **370 phép thử**)*; ⭐ **bỏ hẳn không tốn một dòng code nào** vì `INV-I16` đã ngăn máy dán nhãn từ đầu. ⭐ Kèm lối ra ⛔ không cần luật nào: **xếp hàng chờ theo TIỀN** *(đo 27/08: **799 dòng = 10,4%** hàng chờ phủ **90% tiền TRONG TỪNG tiền tệ** — VND 310 · USD 444 · SGD 13 · HKD 32)*. ⚠⚠ **Ô này vừa mang con số SAI suốt một ngày:** *"310 dòng = 4,0%"* là kết quả **cộng lẫn VND với USD**; đợt sửa 27/08 đã sửa con số đó ở **6 file** nhưng **trượt đúng ô này** vì chuỗi ở đây viết khác. ⇒ Bài học: sửa một con số đã công bố thì phải **quét lại theo con số**, ⛔ không theo câu chứa nó |
| **`CR#2`** | 2026-08-26 | **`ITL-CONTRACT v1.0` khai `svc_start`/`svc_end` kiểu `date` — sổ thật là KỲ (tháng) dạng `text`.** Hai phương án: **(a)** nâng hợp đồng lên `v1.1` kiểu `text` · **(b)** thêm trường `svc_ky` riêng, giữ `svc_start` cho một NGÀY thật | **3** ⚠ *(chạm hợp đồng)* | `ITL-CONTRACT` **v1.1** *(bản sống)*, `v1.0` giữ nguyên làm lịch sử · `fls/db/schema.py` + migration `0005` · `02_BA/05` DD · `QĐ-ITL-55` | ✅ **ĐÓNG 27/08** — owner chốt **(a)**. ⛔ **(b)** bị loại **có lý do đo được**: trường mới đó **không có nguồn dữ liệu nào**, dựng cột rỗng để *"sau này có thì điền"* là đúng cái `P-ITL-05` cấm |

### 5.1 · `CR#2` là CR loại 3 đầu tiên — ba điều kiện cứng đối chiếu thật

`CR#2` chạm hợp đồng, nên nó là bài kiểm tra đầu tiên cho `C1`–`C3` của §3. Đối chiếu **bằng cái đo được**, không bằng lời:

| # | Điều kiện | Chứng cứ đo được |
|:--:|---|---|
| **C1** | Test tương thích **PASS** | **308 phép thử xanh** *(27/08)*, trong đó **3 test riêng cho `CR#2`**: `CR#2` đã đóng · `v1.1` **chỉ** đổi đúng 2 trường *(cột Excel ⛔ không đổi)* · cổng đối chiếu schema trỏ tới bản **SỐNG** |
| **C2** | Đối soát oracle lại | Cổng **parity cả sổ** *(`tests/ledger/test_parity_ca_so.py`)* vẫn xanh sau khi đổi kiểu: **69.510/69.510 ô · 23 kỳ · 0 ô lệch**. ⚠ Nói cho đúng phạm vi: cổng này chứng minh **luật `Final` không đổi**; nó ⛔ **không** đo được *"kiểu `text` có làm mất nghĩa gì không"* — chỗ đó dựa vào `LECH_V1_V1_1` khai **đổi cái gì** |
| **C3** | **Bump version** hợp đồng | `VERSION_SONG = "v1.1"` trong `fls/contract/itl_contract.py`; `ITL_CONTRACT_V1` **không đổi một byte** và cổng khoá `v1.0` **vẫn chạy** — không ai lặng lẽ sửa lịch sử cho test xanh lại |

⭐ **Cái đáng giữ từ ca này:** đường sai là *lặng lẽ sửa chữ `date` thành `text`* trong một hợp đồng đã đóng băng. Đường đã đi: **giữ nguyên hợp đồng, khai lệch ra** `LECH_HOP_DONG_V1` **kèm con số đã đo**, mở CR, và có test **chặn** việc thêm một lệch mới mà không khai. ⇒ Lệch **tồn tại và đang được đếm**, ⛔ không bị ẩn.

## 6. Quan hệ với bộ doc P100 và A-CCR

- **P100:** ITL **đọc** đầu ra P100 (`PM_Unpivot`, PE/PI, Bank/Cash Ledger) qua adapter A/B. Spec P100 vẫn là SSOT của riêng P100; ITL không chép, chỉ khai báo hợp đồng đọc trong `BA-05`. P100 đổi schema đầu ra ⇒ đi đường §4.
- **A-CCR:** sở hữu cổng đối soát tiền. Adapter C **đọc** kết quả đối soát, không dựng lại (chờ chốt `GAP-ITL-04`). Thay đổi chạm ranh giới này = CR loại 2 và phải thông báo chủ sở hữu A-CCR.

## 7. Cổng chống chính sổ này già đi

Sổ CR đã già hai ngày mà không ai biết (§5). Sáu điều dưới đây là để lần sau nó **tự tố**:

| # | Luật | Vì sao |
|:--:|---|---|
| **1** | **Mở CR thì ghi vào §5 TRƯỚC**, rồi mới đi làm | Mở CR ở chỗ khác *(dashboard, master index, docstring)* nghĩa là §5 sai ngay từ giây đầu |
| **2** | **`00_MASTER_INDEX` và §5 phải khớp SỐ LƯỢNG CR** | Hai chỗ chép cùng một danh sách thì phải có một phép đếm nối chúng, không thì chúng lệch |
| **3** | ⛔ **CR đóng mà không ghi chứng cứ đo được thì chưa đóng** | *"Đã xử lý"* không phải chứng cứ. `CR#2` đóng kèm 3 test + 1 cổng parity + 1 hằng số version — đó mới là chứng cứ |
| **4** | ⭐ **Tiền đề của một CR bị đo lật ⇒ mở CR con, ⛔ không sửa lặng lẽ CR cũ** | `CR#1` nói `reference` ở phiếu; đo ra ở dòng. Sửa chữ trong `CR#1` là **viết lại lịch sử** — nên có `CR#1-a`, và cả hai cùng đứng trong sổ |
| **5** | ⭐ ⛔ **Không tài liệu nào được ghi một ngày CHƯA XẢY RA** | Cả đợt `P4`+`P5` bị dán ngày **28/08** ở **54 chỗ / 16 file** — kể cả header sổ này và ngày đóng `CR#4`/`CR#5` — trong khi `git log` nói rõ **27/08 13:56–17:49**. Bốn luật trên **xanh suốt**, vì không luật nào kiểm ngày. Ngày là **trục nhân–quả** của cả bộ tài liệu: mất nó thì không truy được điều gì gây ra điều gì |
| **6** | ⭐⭐ ⛔ **Con số SỐNG phải do MÁY so, ⛔ không chép tay** *(cổng chung #13)* | Đợt 27/08 đi sửa 4 file mang số sống; **19 giờ sau** đo lại thì **20 con số đã lệch** — kể cả file vừa lên `v0.7` *chính vì* lạc hậu, và mục vừa viết lại *vì nói ngược sự thật*. ⇒ cái sai ⛔ không phải *"quên"* mà là **cách sửa**. Một con số chép tay **già đi theo giờ**, và nó già **không có tiếng động** |

### 7.1 ⭐ · Năm luật đầu **đã thành một lệnh chạy được**

```
python docs/ITL/_tools/kiem_tai_lieu.py
```

| Phép | Đo gì | Sinh ra từ lỗ nào |
|:--:|---|---|
| **K1** | version ở **header** so với version cao nhất trong **changelog** | ⛔ `08_MIGRATION_ROADMAP` header đứng ở `v0.1` trong khi changelog đã tới `v0.4` — **ba lần bump chỉ ghi ở changelog**. Mọi file trỏ tới đó đều trích sai version *(sửa 27/08 → `v0.5`)*. Quét cả bộ ra thêm **4 file** cùng bệnh |
| **K2** | **số lượng CR** khớp giữa `00_MASTER_INDEX` và §5 | ⛔ Chính §5 này từng ghi *"chưa có CR nào"* suốt **hai ngày** |
| **K3** | bảng markdown **không lệch cột** | ⛔ **8 dòng** trong `06_ORCHESTRATOR_DASHBOARD` vỡ cột vì dấu `\|` **trần** trong ô *(`P100 \| Cash Ledger` · `Copy of R \| VND_HotBonus` · `R \| …`)*, một dòng còn **thiếu hẳn 2 ô**. ★ Loại lỗi này **mắt thường đọc qua không thấy** — bảng vẫn trông như bảng, chỉ là các ô **dịch sang một cột** |
| **K4** | CR ghi **ĐÓNG** phải có **chứng cứ đo được** *(con số, hoặc trỏ tay tới test/cổng/migration)* | ⛔ Chạy lần đầu nó **đỏ ngay**: `CR#1` ghi *"ĐÓNG 25/08"* mà **không có chứng cứ nào** trong ô trạng thái. Đã điền: test DOM trên `F01`, `Σ = 1.894.982.832` khớp đúng tiền bank, commit `4608869` |
| **K5** | ⛔ không **dòng đường-dẫn-chứng** nào *(header · dòng changelog · dòng số `QĐ` / `CR`)* ghi ngày **chưa xảy ra**; soi **240 ô ngày** | ⛔ 54 chỗ ghi `28/08` cho việc làm **27/08**. ⛔⛔ **Cổng này đỏ giả rồi xanh giả trước khi sống:** lần đầu nó đỏ **30 lỗi** — toàn là **ngày trong DỮ LIỆU mà tài liệu trích dẫn** *(`09/13/2025` là ô sổ kế toán)*, nên phép đo phải thu hẹp lại và bỏ hẳn dạng `dd/mm/yyyy`; rồi nó **xanh** khi tôi đặt ngày tương lai vào **đúng ô đã lệch thật** — mẫu đòi `**Cập nhật:**` còn file ghi `**Cập nhật lần cuối:**`. Sống sau khi **4 nhánh đều diễn tập thấy đỏ** |

⭐ **Cả bốn đã thấy đỏ có chủ ý** *(27/08)*: hạ header `07` về `v0.1` → `K1` đỏ · xoá một dòng CR khỏi §5 → `K2` đỏ *(báo đúng `CR#1-a` chỉ còn ở một bên)* · bỏ dấu thoát của một `|` → `K3` đỏ *(chỉ đúng dòng 142)* · và `K4` đã đỏ **thật**, không phải diễn. Hoàn nguyên → xanh lại.

⛔ **Cổng mặc định KHÔNG ĐẠT** *(`03_Dev/03` §5.10 cổng #7)*: không đọc được file `.md` nào, hoặc không tìm thấy CR nào ở **cả hai** file ⇒ **đỏ**, ⛔ không phải *"không thấy lỗi nên xanh"*. Và nó **in ra đã đo được gì** — số file, số bảng, số ô ngày nó thật sự soi — chứ không chỉ in *"pass"*. ⚠ Câu này **cố ý ⛔ không chép con số**: bản trước ghi `60 file · 638 bảng` và đã lạc hậu; chép lại `643 bảng` thì nó lạc hậu **ngay trong cùng buổi** *(thêm §7.2 là 644)*. Chỗ nào ⛔ không cần con số thì ⛔ đừng chép con số vào — đó là nửa còn lại của cổng chung #13.

⚠ **Điều cổng này ⛔ KHÔNG làm được:** nó kiểm **hình thức** *(version có khớp không, bảng có vỡ không, ô trạng thái có con số không)*. Nó ⛔ **không biết con số đó có đúng hay không** — chỗ đó vẫn là việc của người. `K4` chống được *"đã xử lý"* rỗng, nó ⛔ không chống được **một con số bịa**.


### 7.2 ⭐⭐⭐ · Luật 6 **cũng đã thành một lệnh chạy được** — và nó ở repo `FLS`

```
python tools/kiem_so_song.py          # trong repo FLS
```

⛔ **Vì sao ⛔ KHÔNG đặt ở bộ tài liệu.** Câu cuối §7.1 tự khai: cổng tài liệu *"⛔ không biết con số đó có đúng hay không"*. Đúng vậy, và nó ⛔ **không thể biết** — nó chỉ đọc **giấy**: ⛔ không chạy được `pytest`, ⛔ không mở được kho PostgreSQL, ⛔ không biết `git` đang ở commit nào. ⇒ Phép so phải đặt ở **nơi đo được**, tức là trong repo `FLS`. Đây là chỗ **duy nhất** trong bộ luật này mà cổng nằm ngoài bộ tài liệu, và lý do là vậy.

| | |
|---|---|
| Nó so gì | **43 phép so** trên **4 file** *(`06_DASHBOARD` · `08_ROADMAP` · `00_MASTER_INDEX` · bản vẽ kiến trúc)* |
| Số đến từ đâu | `pytest` · `tools/tien_do.py` · `lint-imports` · **kho PostgreSQL thật** · `git rev-parse` — ⛔ không con số nào gõ vào cổng |
| Luật ⓐ | mỗi mẫu phải khớp **ĐÚNG MỘT LẦN**. Khớp **0** lần *(câu văn đổi ⇒ mẫu vỡ)* là **ĐỎ**, ⛔ không phải *"không thấy lỗi"*. Khớp **≥2** lần cũng **ĐỎ** — cổng ⛔ không biết nó đang so với chỗ nào |
| Luật ⓑ | **đo không được thì ĐỎ**: kho không mở được · thiếu `git` · thiếu file tài liệu ⇒ **không đạt** |
| Luật ⓒ | cổng CHỈ canh **số SỐNG** *(trạng thái hôm nay)*. ⛔ Nó ⛔ không canh số trong **changelog / dòng đường-dẫn-chứng** — ở đó **số cũ là ĐÚNG**, vì đó là **biên bản** |
| Luật ⓓ ⭐⭐ | con số đến **TỪ SỔ** phải mang **DẤU THỜI ĐIỂM** đi kèm *(`10.030 dòng sổ` **(bản sao nạp 27/08 13:42)**)*, và cổng so **cả cái dấu ấy**. ⛔ Ghi **dấu thời điểm**, ⛔ **không** ghi *"tuổi"*: tuổi là con số **động** *(nhích từng phút)* nên chép vào tài liệu là sai ngay hôm sau; dấu thời điểm là một **sự kiện**, nó ⛔ không già đi. Người đọc tự trừ ra tuổi |
| Đã thấy đỏ | **cả 4 nhánh**: lệch số *(20 lần, lần chạy đầu)* · mẫu khớp **0** lần · mẫu khớp **4** lần · **kho không mở được** |

⛔ **Một hướng đã bị LOẠI, ghi lại để đừng thử lại.** Hướng đầu là phép kiểm **thuần giấy**: *bảng nào có dòng `TỔNG` thì các dòng trên nó phải cộng đúng*. Chạy trên 60 file: **5 chỗ đỏ, 4 là đỏ GIẢ** — hai bảng ERD đang **ghi lại con số SAI của `v0.1`** *(cộng lệch chính là điều bảng muốn nói)*, và một bảng có dòng tổng là **tổng của 6 trên 8 dòng**, có chủ ý. ★ Lý do sâu hơn con số: trên giấy thì ⛔ **không phân biệt được** *tài liệu đang KHAI một con số* với *tài liệu đang GHI LẠI con số của người khác*. Đúng cùng cái bệnh làm `K5` đỏ giả 30 lần hôm 27/08.

⛔⛔ **Giới hạn LỚN NHẤT, và nó ⛔ không đóng được bằng cổng này:** cổng chứng minh *"tài liệu khớp **KHO**"*, nó ⛔ **KHÔNG** chứng minh *"kho khớp **SỔ SỐNG**"*. Kho là một **bản sao** *(nạp 27/08 13:42; ảnh chụp dòng lệnh đọc 27/08 19:07)*, còn sổ Google Sheets **chạy tiếp mỗi ngày** — kế toán thêm dòng, sửa ô, và ⛔ **không có ai báo**. ⇒ Nếu sổ đã thêm dòng thì `10.030` **đang cũ đi trong im lặng**, và ⛔ **cổng này không bắt được**. Chữa được **một nửa** bằng luật ⓓ: con số nào từ sổ thì **mang dấu thời điểm**, để người đọc thấy nó **cũ bao nhiêu** thay vì tưởng nó là hôm nay — đúng nguyên tắc đã áp cho ảnh chụp dòng lệnh *(câu trả lời cho "bản lưu già đi thì sao" ⛔ không phải "nó không già" mà là **nói ra nó già bao nhiêu**)*. Nửa còn lại — **so trực tiếp với sổ sống** — cần nguồn Google Sheets **đủ tin cậy để đọc theo lệnh** *(lần thử trước timeout 3/3)*, nên nó là **một quyết định riêng**, ⛔ không gài lặng vào cổng.

⚠ **Điều cổng này ⛔ KHÔNG làm được** *(`GAP-DOC-05`)*: nó chỉ canh **những chỗ người đã khai**. Một con số sống xuất hiện ở **file thứ năm**, hay trong một **câu văn mới** của 4 file ấy, thì ⛔ không cổng nào canh — và nó lại già trong im lặng. ⇒ Luật kèm theo: **viết thêm một câu mang số sống thì phải thêm một phép so**; luật này hiện ⛔ **chưa có máy cưỡng chế**.

## Changelog
- **v1.4** *(2026-09-07, `CR#10`)*: ⭐⭐⭐ **CR loại 1 ĐẦU TIÊN của dự án — một CR chạm PHẠM VI, ⛔ không phải chạm spec hay hợp đồng.** `QĐ-ITL-90` đưa hai màn nhập `Bank Transaction` *(`F04`)* + `Cash Ledger` *(`F05`)* vào FLS. ⛔⛔ **Và nó lật `QĐ-ITL-23`** ở **2/4 nhóm** — một quyết định từng mang chữ **“vĩnh viễn”** và **sống được 16 ngày**. ⭐ **Vì sao phải là CR chứ ⛔ không phải sửa thẳng:** §1 xếp *thay đổi phạm vi* là thứ lan sang **4 tệp trục cùng lúc**; sửa lặng lẽ thì bộ này mất **dấu vết vì sao ranh giới đổi** — và đúng cái đó là thứ `R-A4` cấm. ⚠ CR để **MỞ**: ⛔ chưa có gì để nghiệm thu, vì cả 3 câu chặn *(`GAP-SCOPE-01`/`02`, `GAP-SCR-10`)* đều là câu **nghiệp vụ**, ⛔ không phải việc máy.
- **v1.3** (2026-08-28): thêm **`CR#9`** — `BA-07` §2 ⛔ không có đường nào GỠ một mối nối đã ghép; sửa đặc tả bằng `POST /queue/{itl_id}/unmatch` *(`QĐ-ITL-69`)*.
- v1.2 (2026-08-28): **Mở và đóng `CR#8`** — `52 cột` của `CR#7` là **thiếu**, số đúng **55**; và nguyên mẫu in 38 tiêu đề canon bằng **chữ cái** rồi để **chỉ-đọc**, nên **5/10 trường người gõ** ⛔ không gõ được. ⛔ `CR#7` **giữ nguyên** *(luật §7-4: tiền đề bị đo lật ⇒ mở CR con)*. ★ Điều đáng ghi: phát hiện đến từ **owner mở tệp 30 giây**, ⛔ không phải từ 11 phép thử của máy — vì mũi thử đo **hình dạng** *(bao nhiêu cột, rộng bao nhiêu)* mà ⛔ chưa đo **gõ được vào đúng trường hay không**.
- v1.1 (2026-08-28): ⭐⭐ **§7.2 thêm luật ⓓ — con số đến TỪ SỔ phải mang DẤU THỜI ĐIỂM**, và cổng so cả cái dấu ấy *(nay **48 phép so**)*. ⛔ Ghi **dấu thời điểm**, ⛔ không ghi *"tuổi"*: tuổi nhích từng phút nên chép vào tài liệu là sai ngay hôm sau; dấu thời điểm là một **sự kiện**, nó ⛔ không già đi. ⛔⛔ Kèm **khai ranh giới lớn nhất của cổng**: nó chứng minh *tài liệu khớp **KHO***, ⛔ **không** chứng minh *kho khớp **SỔ SỐNG*** — kho là bản sao *(nạp 27/08 13:42 · ảnh chụp đọc 27/08 19:07)* còn sổ Gsheet **chạy tiếp mỗi ngày**. Nửa còn lại *(so trực tiếp sổ sống)* cần nguồn đọc được theo lệnh *(lần thử trước timeout 3/3)* ⇒ **quyết định riêng**.
- v1.0 (2026-08-28): ⭐⭐⭐ **Thêm luật 6 + §7.2 — con số SỐNG phải do MÁY so, ⛔ không chép tay.** Sinh ra từ một lỗ đo được: **20 con số lệch trên 4 file chỉ sau 19 giờ**, và cả 4 file ấy **đều nằm trong đợt sync hôm trước** — nên cái sai ⛔ không phải *"quên"* mà là **cách sửa** *(chép tay)*. Cơ chế: `tools/kiem_so_song.py` trong repo `FLS` *(⛔ không đặt ở bộ tài liệu — cổng tài liệu chỉ đọc giấy, ⛔ không chạy được `pytest`, ⛔ không mở được kho, ⛔ không biết `git` ở commit nào)*. Đóng `GAP-DOC-04`; mở `GAP-DOC-05` *(cổng chỉ canh chỗ đã khai)*.
- v0.9 (2026-08-27): **Mở và đóng `CR#7`** — tiền đề bài toán lưới `F02` bị đo lật **cả ba con số** (**52** cột *(38 canon + 14 hợp đồng)* · **10** cột sửa được · **748** dòng một lát *(kỳ dày nhất)* · **705 byte/dòng** · **36,1%** ô rỗng). Ảo hoá có thể không cần ⇒ quyết định thư viện phải xem lại; xuất hiện ứng viên **bảng HTML trần** với nguyên mẫu chạy được. ⛔ **Bảng khảo sát 24/08 giữ nguyên** — sửa chữ trong biên bản là viết lại lịch sử; cảnh báo đặt **ở đầu mục**, đúng luật §7-4 *(tiền đề bị lật ⇒ mở CR, ⛔ không sửa lặng lẽ)*.
- v0.8 (2026-08-27): **Mở và đóng `CR#6`** — `BA-07` §2 `/match {pm_id}` sai trục *(phiếu thay vì dòng)*; **526 phiếu mang 2–36 reference khác nhau** nên ghép vào phiếu là **máy quyết thay người** *(`INV-I16`)*. Thân đổi thành `{pm_line_ids}`. ⭐ Cùng đợt: owner chốt **`QĐ-ITL-61`** *(lưu ảnh chụp dòng lệnh vào kho — đóng `GAP-API-04`)*; mở `GAP-JOIN-04` *(⛔ không xếp được ứng viên theo ngày/payee — ảnh chụp không mang PII)*, `GAP-JOIN-05` *(⛔ chưa có đường BỎ mối nối để ghép lại)* và **`GAP-CR1-04`** *(dung sai 1.000 VND tuyệt đối làm **hai** bài test xanh SAI: nó cho ghép 100 VND với 1.099 VND = lệch 999%)*.
- v0.7 (2026-08-27, đợt đồng bộ tiến độ): ⭐ **Thêm luật 5 vào §7 + phép kiểm `K5` vào §7.1** — ⛔ không tài liệu nào được ghi một **ngày chưa xảy ra**. Sinh ra từ **54 chỗ / 16 file** ghi `28/08` cho việc mà `git log` nói làm **27/08 13:56–17:49**, gồm cả **header của chính sổ này**. ⛔ Bốn luật cũ **xanh suốt** vì không luật nào kiểm ngày. ⭐ Hệ quả đo được: `CR#4` ghi khung xem *"sống một ngày"* — thực tế **1 giờ 48 phút** *(dựng `13:56`, bỏ `15:44`)*; đã sửa ở 3 file. ⛔⛔ `K5` **đỏ giả 30 lỗi rồi xanh giả một lần** trước khi sống — chi tiết ở §7.1.
- v0.6 (2026-08-27): **Mở và đóng `CR#5`** — `BA-07` §3 *("trường hợp-đồng cập nhật `*_thyt`")* sai `INV-I08` **và** `QĐ-ITL-35`. Giá trị người gõ chuyển sang `fls_adjustment` + khung xem `fls_sua_tay` *(migration `0010`)*; ⭐ **sửa đặc tả, ⛔ không sửa code cho khớp đặc tả sai**. **548 phép thử**.
- v0.5 (2026-08-27): **Mở và đóng `CR#4`** — bỏ khung xem `fls_queue_xep_tien` *(migration `0009`)*: khung xem SQL ⛔ không nhận tham số nên không mang được **phạm vi**, và lọc ở đầu ra ⛔ không sửa được một thứ tự đã xếp sai. Phép xếp chuyển vào câu **có tham số**. ⚠⚠ Kèm **sửa một con số còn sót**: ô `CR#3` vẫn ghi *"310 dòng = 4,0%"* — con số **cộng lẫn VND với USD** — suốt một ngày sau khi đã sửa ở 6 file khác, vì đợt sửa đó khớp theo **câu** chứ không theo **con số**.
- v0.4 (2026-08-27): **Đóng `CR#3`** — owner chốt **BỎ HẲN** trạng thái *"không cần lệnh chi"* *(`QĐ-ITL-58`)*. ⭐ Bỏ hẳn **không tốn một dòng code nào**: `INV-I16` đã ngăn máy dán nhãn từ đầu nên trạng thái giữa **chưa bao giờ ăn vào code hay kho**. Thay bằng khung xem xếp hàng chờ theo **tiền**, `PARTITION BY` tiền tệ. ⚠ Kèm sửa một con số **tôi đã công bố sai** *(cộng lẫn VND với USD)*.
- v0.3 (2026-08-27): Mở **`CR#3`** — `QĐ-ITL-56` *(owner: **không có quy định** nào nói khoản nào cần lệnh chi)* **lật tiền đề** của `QĐ-ITL-28`, nên trạng thái giữa *"KHÔNG CẦN LỆNH"* mất nguồn. ⭐ Đây là ca đầu tiên **luật 4 của §7 chạy thật**: tiền đề bị lật ⇒ **mở CR con**, ⛔ không sửa chữ trong quyết định cũ. Kèm lối ra ⛔ không cần luật nào *(xếp hàng chờ theo tiền — 4% hàng chờ phủ 90% tiền)*.
- v0.2 (2026-08-27): ⛔⛔ **Điền sổ CR — §5 từng ghi "chưa có CR nào" trong hai ngày** mà `CR#1` đã đóng và `CR#2` đã mở rồi đóng *(cả hai chỉ sống ở `00_MASTER_INDEX` và mã nguồn)*. Thêm **`CR#1-a`**: tiền đề *"`reference` nằm ở phiếu"* của `CR#1` **bị đo lật** — nó nằm ở **dòng** *(526/1.468 phiếu mang 2–36 mã khác nhau)*, và con số *"289 dòng dư"* **rút vì không tái lập được**. Thêm **§5.1** đối chiếu `C1`–`C3` thật cho `CR#2` *(CR loại 3 đầu tiên)*. Thêm **§7** bốn luật chống sổ già — và **§7.1**: cả bốn nay là **một lệnh chạy được** `_tools/kiem_tai_lieu.py` *(quét 60 file · 638 bảng)*, **cả bốn đã thấy đỏ có chủ ý**, và `K4` đỏ **thật** ngay lần đầu: `CR#1` ghi *ĐÓNG* mà không có chứng cứ nào ⇒ đã điền *(test DOM `F01`, Σ = 1.894.982.832, commit `4608869`)*. Kèm sửa **8 dòng bảng vỡ cột** ở `06` + **4 header version lạc hậu** ở `02_BA` mà cổng `K1`/`K3` quét ra. Chốt dạng ID **`CR#<số>`**, khai tử `CR-ITL-<số>`.
- v0.1 (2026-08-18): Khởi tạo — 4 loại thay đổi (thêm loại 3 hợp đồng với 3 điều kiện cứng C1–C3, thêm loại 4 trôi kế thừa); §4 xử lý schema nguồn đổi.
