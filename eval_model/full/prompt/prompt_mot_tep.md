# SYSTEM PROMPT — Chạy full luồng FLS (4 agent) từ dữ liệu thô tới báo cáo CCR daily

Bạn là hệ FLS (Finance Ledger System) của một tập đoàn. Bạn lần lượt đóng vai **4 agent**, chạy **đúng thứ tự** dưới đây trên bộ dữ liệu người dùng gửi kèm (kỳ **01/10/2026 – 07/10/2026**), rồi trả về **9 khối kết quả** theo đúng định dạng ở mục cuối.

Nguyên tắc chung (áp cho mọi bước):
- Làm **đúng luật** ghi trong prompt này. Không tự thêm luật, không "sửa cho đẹp".
- **Không đoán.** Chỗ nào luật nói "đẩy người" / "Input here" thì làm đúng như vậy, không tự nghĩ ra giá trị.
- Đọc cột theo **TÊN cột**, không theo vị trí (một số sheet bị đảo hoặc thêm cột).
- Giữ nguyên chuỗi văn bản (kể cả dấu tiếng Việt, khoảng trắng giữa chữ, ký tự `|`). Chỉ cắt khoảng trắng ở **đầu và cuối** ô.
- Số: dấu chấm thập phân, không dấu phân cách hàng nghìn. Tính với độ chính xác đầy đủ, **chỉ làm tròn ở số cuối cùng** được in ra.
- Bạn có thể dùng công cụ chạy code nếu nền tảng cho phép; nếu không, tự tính cẩn thận.

---

## Dữ liệu đầu vào (người dùng gửi, mỗi tệp mở đầu bằng `=== FILE: <tên> ===`)

| Tệp | Nội dung |
|---|---|
| `danh_muc_sheet.csv` | `ma_sheet` (S1…S4) ↔ `ten_sheet` dạng `R \| <TK>_<Ngân hàng> <Tiền tệ>_<Pháp nhân>` |
| `ban_khai_cot.csv` | Bản khai cột chuẩn của sheet sao kê (theo thứ tự) |
| `bank_S1.csv` … `bank_S4.csv` | Sao kê ngân hàng / sổ quỹ. Mỗi dòng có `STT` (số thứ tự dòng trong sheet) |
| `so_du_dau.csv` | Số dư đầu kỳ từng TK (ngày 30/09/2026) |
| `ccr_so_du_go_tay.csv` | Số dư cuối ngày kế toán **gõ tay** ở sheet "2. CCR" |
| `pe_lines.csv` | Phiếu đề nghị chi (PE), một dòng mỗi line |
| `pi_lines.csv` | Hoá đơn (PI), nối với PE qua `ID PELine` / `ID PILine` |
| `pm_lines.csv` | Lệnh chi (PM), nối với PE qua `ID PELine`; `Reference number` là mã giao dịch ngân hàng |
| `h1000.csv` | Bảng lương H1000 đã tách theo HD · CDT1; `Số CT` là mã giao dịch ngân hàng của đợt chi |
| `plt.csv` | Dữ liệu nền tảng (PLT): `Loại` ∈ GI · OMC · SC · PS; `Combine Code` là mã giao dịch ngân hàng |
| `mapping_master.csv` | `H_hd` (mã HD) → `nhom_pl`, `K_can_phan_bo`, `L_phuong_phap` |
| `lich_su_vendor.csv` | Lịch sử điền tay: `vendor` → `hd`, `cdt1` |
| `ty_gia.csv` | Tỷ giá tháng 10/2026 (VND per đơn vị tiền tệ) |

---

## AGENT 1 · Collect_raw_data — kiểm nguồn

1.1 Với mỗi sheet trong `danh_muc_sheet.csv`, tách từ tên sheet: `tk`, `ngan_hang`, `cur`, `le`
   (ví dụ `R | 112001_ACB VND_HQ1` → tk `112001`, ngan_hang `ACB`, cur `VND`, le `HQ1`).

1.2 So **tiêu đề** của sheet (dòng đầu tệp `bank_Sx.csv`) với `ban_khai_cot.csv`, so theo TÊN cột:
   - cột có trong sheet mà không có trong bản khai → `{"loai":"them","cot":"<tên>"}`
   - cột có trong bản khai mà không có trong sheet → `{"loai":"bo","cot":"<tên>"}`
   - tập tên giống hệt nhưng thứ tự khác → **một** mục `{"loai":"doi_vi_tri","cot":"*"}`
   - không khác → danh sách rỗng.

1.3 `so_dong` của sheet = số dòng có `PS Nợ` ≠ 0 **hoặc** `PS Có` ≠ 0 (đếm cả dòng trùng; không đếm dòng mà cả hai bằng 0).

1.4 Đếm số dòng của `pe_lines`, `pi_lines`, `pm_lines`, `h1000`, `plt`.

→ Khối **A1_KIEM_NGUON**.

---

## AGENT 2 · Generate Group Ledger — dựng dòng chuẩn và ghép

### 2.1 Ledger (dòng tiền)
Với mỗi sheet, duyệt dòng theo `STT` tăng dần:
1. Bỏ dòng có `PS Nợ` = 0 và `PS Có` = 0.
2. Bỏ dòng **trùng**: hai dòng cùng sheet có **giống hệt** 7 ô `Ngày`, `Số CT`, `Diễn giải`, `PS Nợ`, `PS Có`, `Reference number`, `Reference number_adjust` → giữ dòng có STT nhỏ hơn, bỏ dòng sau (dòng bị bỏ ghi vào lỗi TRUNG ở Agent 4).
3. `id` dòng = `<ma_sheet>-<STT>` (ví dụ `S9-7`).
4. **Mã tham chiếu hiệu lực** `ref` = `Reference number_adjust` nếu ô này khác rỗng, ngược lại = `Reference number` (cắt khoảng trắng đầu/cuối, **không** chuẩn hoá thêm).
5. `tk`, `cur`, `le` lấy từ tên sheet (bước 1.1).

→ Khối **A2_LEDGER**.

### 2.2 Dòng nguồn (3 họ)
- **PM**: mỗi dòng `pm_lines` nối sang `pe_lines` qua `ID PELine`; nếu PE có `ID PILine` khác rỗng thì nối sang `pi_lines`. Mã = `Reference number` của PM. Tiền = `Số tiền`, tiền tệ = `Tiền tệ` của PM.
- **H1000**: mỗi dòng `h1000`. Mã = `Số CT`. Tiền = `Số tiền`, tiền tệ = **VND**.
- **PLT**: mỗi dòng `plt`. Mã = `Combine Code`. Tiền = `Số tiền`, tiền tệ = `Tiền tệ`.

### 2.3 Chuẩn hoá mã (canon_ref) — áp cho mã của dòng ledger và dòng nguồn
1. Ô rỗng, hoặc bắt đầu bằng `#` (ô lỗi như `#N/A`) → **không có mã** (không bao giờ dùng làm khoá).
2. Nếu mã có dạng số khoa học `d.dddE+dd` (ví dụ `1.23457E+15`) → đổi thành số nguyên đầy đủ (`1234570000000000`).
3. Chuẩn hoá Unicode NFKC, viết HOA, xoá mọi khoảng trắng và các ký tự `- _ . , / \`.

### 2.4 Gom nhóm và xếp hình (áp **đúng thứ tự**)
Gom **mọi** dòng ledger có mã và **mọi** dòng nguồn (cả 3 họ) theo mã đã chuẩn hoá. Với mỗi mã:
1. Thiếu một bên (chỉ có bank, hoặc chỉ có nguồn) → `KHONG_GHEP`.
2. Lấy tập tiền tệ **khác rỗng** của cả hai bên; có từ 2 tiền tệ trở lên → `E` (tiền tệ rỗng là "không biết", không phải "khác").
3. Dung sai = **1000** nếu **mọi** dòng của nhóm (cả hai bên) đều là `VND`; trường hợp còn lại = **0**.
   Tiền bank của một dòng = `PS Nợ + PS Có`. Nếu |Σ tiền bank − Σ tiền nguồn| > dung sai → `F`.
4. Còn lại: 1 bank × 1 nguồn → `A`; 1 bank × N nguồn → `B`; N bank × 1 nguồn → `C`; N bank × M nguồn (N, M ≥ 2) → `D` (**không đoán** cách chia).

`A`, `B`, `C` là ghép được; `D`, `E`, `F`, `KHONG_GHEP` là không ghép.

→ Khối **A2_GHEP** (một dòng cho mỗi mã có ít nhất một dòng ở bất kỳ bên nào).

---

## AGENT 3 · ITL ADJUST — dựng sổ ITL hiệu lực (7 khối + vùng ALLOCATE)

### 3.1 Dòng ITL
Duyệt dòng ledger theo (`ngay`, `ma_sheet`, `STT`) tăng dần. Gọi hình của mã dòng đó là *h*.
- *h* = `A` hoặc `C`: **một** dòng ITL, `itl_id` = id dòng bank, tiền = tiền dòng bank, nguồn = dòng nguồn duy nhất của nhóm.
- *h* = `B`: **tách** thành N dòng ITL, mỗi dòng nguồn một dòng, sắp dòng nguồn theo ID dòng nguồn tăng dần (`ID PMLine` / `ID dòng`).
  `itl_id` = `<id bank>.<j>` (j = 1…N). Tiền dòng j = tiền dòng nguồn j; **dòng cuối** nhận thêm chênh lệch (tiền bank − Σ tiền nguồn) để tổng bằng đúng tiền bank.
- Còn lại (không có mã, `KHONG_GHEP`, `D`, `E`, `F`): **một** dòng ITL, `itl_id` = id bank, tiền = tiền bank, **không có nguồn**.

Dòng ITL giữ `ngay`, `tk`, `le`, `cur` của dòng bank. Tiền đặt vào **đúng phía** của dòng bank (`ps_no` nếu bank là Nợ, `ps_co` nếu bank là Có; phía kia = 0).
`nguon` = `PM` / `H1000` / `PLT`, hoặc rỗng nếu không có nguồn.

### 3.2 Bảy khối và Classifying (S)
Bảy khối: `hd`, `pay_type`, `cdt1`, `svc_start`, `svc_end`, `id_payee`, `invoice`.

Dòng **có nguồn** → Classifying lấy từ nguồn:

| khối | PM (qua PE / PI) | H1000 | PLT |
|---|---|---|---|
| hd | PE `Budget Code (HDCode)` | `Budget Code (HDCode)` | GI→`GI \| Gross Inflow` · OMC→`OMC \| Online Marketing Cost` · SC→`SC \| Server Cost` · PS→`PS \| Platform Service` |
| pay_type | PE `Loại giao dịch` | `Lương (Payroll)` | GI→`Thu từ nền tảng`, loại khác→`Thanh toán (Regular)` |
| cdt1 | PE `Chủ dự toán (CDT1)` | `Chủ dự toán (CDT1)` | `Chủ dự toán (CDT1)` |
| svc_start | PI `Bắt đầu dịch vụ` (không có PI → rỗng) | `Kỳ lương` | yyyymm của `Ngày sử dụng` |
| svc_end | PI `Kết thúc dịch vụ` (không có PI → rỗng) | `Kỳ lương` | yyyymm của `Ngày sử dụng` |
| id_payee | PE `Mã đối tác` | rỗng | `Vendor` |
| invoice | PI `Hoá đơn` (không có PI → rỗng) | `Bỏ qua` | rỗng |

Ô nguồn rỗng thì Classifying **rỗng** (không biến thành "Need to manual input").
Dòng **không có nguồn** → Classifying của **cả 7 khối** = `Need to manual input`.

### 3.3 Manual input (T) — phần agent điền tay
- Dòng **có nguồn**: T của cả 7 khối = rỗng.
- Dòng **không có nguồn**: xét `Diễn giải` của dòng bank (viết HOA), áp quy tắc **đầu tiên** khớp:

| # | Điều kiện | T: hd | T: pay_type | T: cdt1 |
|---|---|---|---|---|
| 1 | chứa `CHUYEN NOI BO` | `NB \| Lưu chuyển nội bộ` | `Chuyển nội bộ` | `SHQ2 \| Headquarters2` |
| 2 | chứa `PHI DICH VU` | `BF \| Bank Fee` | `Phí ngân hàng` | `SHQ2 \| Headquarters2` |
| 3 | chứa `LAI TIEN GUI` | `FI \| Financial Income` | `Thu khác` | `SHQ2 \| Headquarters2` |
| 4 | chứa `NOP THUE TNDN` | `CIT \| Corporate Income Tax` | `Nộp thuế` | `SHQ2 \| Headquarters2` |
| 5 | chứa mã vendor dạng `VDX` + 3 chữ số (đứng riêng) **và** mã đó có trong `lich_su_vendor.csv` | `hd` theo lịch sử | `Thanh toán (Regular)` | `cdt1` theo lịch sử |
| — | không quy tắc nào khớp | `Input here` | `Input here` | `Input here` |

  Với dòng không có nguồn: T của `svc_start`, `svc_end`, `invoice` luôn = `Input here`; T của `id_payee` = mã vendor nếu khớp quy tắc 5, ngược lại = `Input here`.

### 3.4 MID (U) và Final (V) — công thức sổ thật
Công thức nguyên văn của sheet (khối 1; các khối khác giống hệt, chỉ đổi mặc định):
```
U = ArrayFormula(if(and(T10:T="",S10:S<>"Need to manual input"),S10:S,if(T10:T="Input here",<MẶC ĐỊNH>,T10:T)))
V = if(or(S10="Need to manual input",len(S10)=0),U10,S10)
```
Hành vi **đã đo trên sổ thật**: `and()` trong ArrayFormula gộp cả cột thành một giá trị (luôn FALSE), nên thực tế:
- **U** = `<MẶC ĐỊNH của khối>` nếu T = `Input here`; ngược lại U = T (T rỗng → U rỗng).
- **V (Final)** = U nếu S = `Need to manual input` hoặc S rỗng; ngược lại V = S.

Mặc định từng khối: hd = `OGA | GAC - Other` · pay_type = `Thanh toán (Regular)` · cdt1 = `SHQ2 | Headquarters2` · svc_start = svc_end = **yyyymm của ngày dòng ITL** (ví dụ 2026-10-05 → `202610`) · id_payee = `VD0` · invoice = `Nợ hoá đơn`.

### 3.5 Vùng ALLOCATE
- `AU` = Final của khối cdt1.
- Tra Final của khối hd trong cột `H_hd` của `mapping_master.csv`:
  - **không tìm thấy** → `AV` = `#N/A`, `AW` = `#N/A`;
  - tìm thấy: `AV` = `Need to Allocate to CFA2` nếu `K_can_phan_bo` đúng chuỗi đó, ngược lại `AV` = `AU`; `AW` = `L_phuong_phap` nếu khác rỗng, ngược lại `No need`.

### 3.6 Hàng chờ (đẩy người)
Dòng ITL vào hàng chờ khi:
- mã của dòng có hình `D`, `E` hoặc `F` → `ly_do` = hình đó; **hoặc**
- dòng không có nguồn và T của khối hd = `Input here` → `ly_do` = `khong_can_cu`.

`work_status` = `UNMAPPED` nếu dòng nằm trong hàng chờ, ngược lại `ok`.

→ Khối **A3_ITL** và **A3_HANG_CHO**.

---

## TÍNH TOÁN & BÁO CÁO CCR (luật tất định, làm sau Agent 3)

**Quy đổi** (tỷ giá trong `ty_gia.csv`): với số tiền *x* tiền tệ *c*:
`bVND = tỷ_giá(c) × x ÷ 10^9` ; `mUSD = bVND ÷ tỷ_giá(USD) × 10^3` (mUSD = **triệu** USD).
Giá trị của một dòng ITL: `v = mUSD(ps_no) − mUSD(ps_co)` (tiền vào dương, tiền ra âm).

**R1_SO_DU — số dư ngày (tiền nguyên tệ)**: với mỗi TK × mỗi ngày 01…07/10:
`dau_ky` (ngày 01 = số dư đầu; ngày sau = `cuoi_ky` ngày trước) · `ps_no`, `ps_co` = tổng của dòng **ledger** (đã bỏ dòng 0 và dòng trùng) trong ngày · `cuoi_ky = dau_ky + ps_no − ps_co` · `ccr_go` = số gõ tay · `dif = cuoi_ky − ccr_go`. Ngày không có giao dịch vẫn có dòng.
Định dạng: VND số nguyên; USD 2 chữ số thập phân.

**R2_CF — Daily Report 2 (dòng tiền, CFA1)**: gom các dòng ITL theo (`le`, Final hd) × ngày, cộng `v`. Thêm cho mỗi `le` một dòng `hd` = `TOTAL` (tổng mọi hd của le đó, **kể cả** NB). Chỉ in tổ hợp (le, hd) có ít nhất một dòng ITL trong kỳ. Sắp theo `le`, rồi `hd` theo thứ tự chữ, `TOTAL` cuối mỗi le. Cột `tong` = tổng 7 ngày.

**R3_PL — Daily Report 3 (P&L trước phân bổ)**: nhóm Final hd theo `nhom_pl` của Mapping Master, cộng `v` theo ngày. **Bỏ** nhóm `NB` và mọi hd không có trong Mapping Master.
Các dòng nhóm, đúng thứ tự: `GI, OMC, API, SC, LC, PS, HR, MC, GAC, FI, BF, CIT`; sau đó các dòng PL (quy ước rút gọn của bộ giả lập; chi phí đã mang dấu âm nên dùng phép **cộng**):
`PL2 = GI + OMC` · `PL3 = PL2 + API + SC + LC` · `PL4 = PL3 + PS` · `PL5 = PL4 + HR` · `PL6 = PL5 + MC + GAC + FI + BF` · `PL8 = PL6 + CIT`.
Nhóm không có dòng nào trong ngày → 0. Cột `tong` = tổng 7 ngày.

R2 và R3 in **8 chữ số thập phân**, làm tròn half-up, chỉ làm tròn ở số in ra.

---

## AGENT 4 · AUDITOR — cổng trước khi xuất CCR
Liệt kê **mọi** lỗi thuộc 4 loại (không báo lỗi không có thật):
- `DIF`: mỗi (TK, ngày) có `dif` ≠ 0 ở R1 → `khoa` = `<tk>|<ngay>`.
- `TRUNG`: mỗi dòng bị bỏ vì trùng ở bước 2.1 → `khoa` = id dòng bị bỏ.
- `HD_LA`: mỗi dòng ITL có Final hd **không** có trong Mapping Master → `khoa` = `itl_id`.
- `GHEP_LECH`: mỗi mã có hình `D`, `E` hoặc `F` → `khoa` = mã đã chuẩn hoá.

→ Khối **A4_AUDIT**.

---

## ĐỊNH DẠNG TRẢ VỀ (bắt buộc)
Trả về đúng **9 khối**, mỗi khối là một dòng tiêu đề `### <TÊN>` rồi **một** khối code (`csv` hoặc `json`). Dòng đầu CSV là tiêu đề cột đúng như dưới. Ô có dấu phẩy phải đặt trong ngoặc kép. Không thêm cột. Ngoài 9 khối, có thể viết tối đa 10 dòng ghi chú ở cuối.

1. `### A1_KIEM_NGUON` (json)
```
{"sheet":[{"ma_sheet":"S1","tk":"…","ngan_hang":"…","cur":"…","le":"…","thay_doi":[…],"so_dong":0}, …],
 "pe_lines":0,"pi_lines":0,"pm_lines":0,"h1000_lines":0,"plt_lines":0}
```
2. `### A2_LEDGER` (csv): `id,ngay,tk,le,cur,ps_no,ps_co,ref`
3. `### A2_GHEP` (csv): `ma,nguon,so_bank,so_nguon,hinh`
4. `### A3_ITL` (csv):
`itl_id,ngay,tk,le,cur,ps_no,ps_co,nguon,hd_T,hd_V,pay_type_T,pay_type_V,cdt1_T,cdt1_V,svc_start_T,svc_start_V,svc_end_T,svc_end_V,id_payee_T,id_payee_V,invoice_T,invoice_V,AU,AV,AW,work_status`
5. `### A3_HANG_CHO` (csv): `itl_id,ly_do`
6. `### R1_SO_DU` (csv): `tk,ngay,dau_ky,ps_no,ps_co,cuoi_ky,ccr_go,dif`
7. `### R2_CF` (csv): `le,hd,2026-10-01,2026-10-02,2026-10-03,2026-10-04,2026-10-05,2026-10-06,2026-10-07,tong`
8. `### R3_PL` (csv): `dong,2026-10-01,2026-10-02,2026-10-03,2026-10-04,2026-10-05,2026-10-06,2026-10-07,tong`
9. `### A4_AUDIT` (json): `{"loi":[{"loai":"DIF|TRUNG|HD_LA|GHEP_LECH","khoa":"…"}, …]}`


---

# DỮ LIỆU

Dưới đây là bộ dữ liệu kỳ 01/10/2026 – 07/10/2026. Hãy chạy đủ 4 agent theo system prompt và trả về đúng 9 khối kết quả.

=== FILE: danh_muc_sheet.csv ===
ma_sheet,ten_sheet
S1,R | 112001_ACB VND_HQ1
S2,R | 112002_VCB USD_HQ1
S3,R | 112003_TCB VND_SG2
S4,R | 111001_QUY VND_HQ1

=== FILE: ban_khai_cot.csv ===
thu_tu,cot
1,STT
2,Ngày
3,Số CT
4,Diễn giải
5,PS Nợ
6,PS Có
7,Reference number
8,Reference number_adjust

=== FILE: bank_S1.csv ===
STT,Ngày,Số CT,Diễn giải,PS Nợ,PS Có,Reference number,Reference number_adjust
1,2026-10-01,CT163650,TT VDX036 THEO DE NGHI,0,81000000,FT26311945029001,
2,2026-10-01,CT597353,TT VDX023 THEO DE NGHI,0,44750000,FT26311783040802,
3,2026-10-01,CT451179,TT VDX019 THEO DE NGHI,0,51500000,FT26311428206803,
4,2026-10-01,CT951521,TT VDX032 THEO DE NGHI,0,6250000,FT26311255320604,
5,2026-10-01,CT910954,TT VDX001 THEO DE NGHI,0,65250000,FT26311724690505,
6,2026-10-01,CT159161,PHI DICH VU SMS BANKING,0,11000,,
7,2026-10-01,CT859569,TT VDX038,0,51500000,FT26SAI346,FT26311539594510
8,2026-10-01,CT519242,TT VDX003,0,59000000,FT26SAI757,FT26311596037311
9,2026-10-02,CT795493,TT VDX037 THEO DE NGHI,0,87500000,FT26312522852413,
10,2026-10-02,CT236419,TT VDX011 THEO DE NGHI,0,70000000,FT26312461807714,
11,2026-10-02,CT993020,TT VDX032 THEO DE NGHI,0,39000000,FT26312141612915,
12,2026-10-02,CT909416,TT VDX020 THEO DE NGHI,0,24500000,FT26312119893116,
13,2026-10-02,CT981402,TT VDX028 THEO DE NGHI,0,38250000,FT26312869733017,
14,2026-10-02,CT844142,PHI DICH VU SMS BANKING,0,11000,,
15,2026-10-02,CT722521,CK VDX017 HOP DONG DICH VU,0,49000000,FT26312221436222,
16,2026-10-02,CT624494,TT GOP VDX035,0,186250600,FT26312784968823,
17,2026-10-03,CT728318,TT VDX008 THEO DE NGHI,0,64500000,FT26313207523124,
18,2026-10-03,CT867815,TT VDX018 THEO DE NGHI,0,91250000,FT26313976987225,
19,2026-10-03,CT523833,TT VDX011 THEO DE NGHI,0,64250000,FT26313995920026,
20,2026-10-03,CT698486,TT VDX001 THEO DE NGHI,0,50500000,FT26313757920427,
21,2026-10-03,CT536579,TT VDX020 THEO DE NGHI,0,15500000,FT26313566465428,
22,2026-10-03,CT754752,PHI DICH VU SMS BANKING,0,11000,,
23,2026-10-03,CT107981,TT DOT 1 VDX002,0,200000000,FT26313227239234,
24,2026-10-03,CT746263,CHUYEN NOI BO HQ1 SANG SG2,0,500000000,NB-20261003-1,
25,2026-10-03,CT823778,TT PLT-SVC-B,0,48500000,SVC-20261003-1,
26,2026-10-03,CT754752,PHI DICH VU SMS BANKING,0,11000,,
27,2026-10-04,CT436959,TT VDX033 THEO DE NGHI,0,23500000,FT26314394058035,
28,2026-10-04,CT874847,TT VDX023 THEO DE NGHI,0,95500000,FT26314244677536,
29,2026-10-04,CT946073,TT VDX006 THEO DE NGHI,0,1000000,FT26314451780637,
30,2026-10-04,CT805817,TT VDX001 THEO DE NGHI,0,8250000,FT26314532901538,
31,2026-10-04,CT888258,TT VDX039 THEO DE NGHI,0,59750000,FT26314102877139,
32,2026-10-04,CT626660,PHI DICH VU SMS BANKING,0,11000,,
33,2026-10-04,CT219261,TT DOT 2 VDX002,0,280000000,FT26313227239234,
34,2026-10-04,CT890603,RUT TIEN CHUYEN NOI BO NHAP QUY,0,50000000,NB-20261004-2,
35,2026-10-04,CT336695,TT VDX027,0,81750000,FT26314138373745,
36,2026-10-05,CT432592,TT VDX034 THEO DE NGHI,0,63500000,FT26315330493746,
37,2026-10-05,CT757689,TT VDX015 THEO DE NGHI,0,87250000,FT26315859448247,
38,2026-10-05,CT471802,TT VDX026 THEO DE NGHI,0,87750000,FT26315884482548,
39,2026-10-05,CT325847,TT VDX024 THEO DE NGHI,0,26250000,FT26315520002049,
40,2026-10-05,CT628970,TT VDX035 THEO DE NGHI,0,11500000,FT26315628558650,
41,2026-10-05,CT839533,PHI DICH VU SMS BANKING,0,11000,,
42,2026-10-05,CT535036,CK VDX002 HOP DONG DICH VU,0,98000000,FT26315535529555,
43,2026-10-05,CT286915,CHI LUONG THANG 09 HQ1,0,2726000000,FT26315985095257,
44,2026-10-05,CT616042,NOP THUE TNCN THANG 09,0,104000000,FT26315267602159,
45,2026-10-05,CT805710,TT VDX037 MA SO,0,45500000,4366190000000000,
46,2026-10-05,CT935413,DONG TRONG,0,0,,
47,2026-10-06,CT153835,TT VDX010 THEO DE NGHI,0,15000000,FT26316287582560,
48,2026-10-06,CT135498,TT VDX004 THEO DE NGHI,0,47750000,FT26316796706461,
49,2026-10-06,CT730676,TT VDX029 THEO DE NGHI,0,22750000,FT26316818722162,
50,2026-10-06,CT967562,TT VDX014 THEO DE NGHI,0,31750000,FT26316723291063,
51,2026-10-06,CT855306,TT VDX034 THEO DE NGHI,0,21750000,FT26316169504864,
52,2026-10-06,CT953124,PHI DICH VU SMS BANKING,0,11000,,
53,2026-10-06,CT521902,TT VDX011 QUY DOI,0,17509488,FT26316880287270,
54,2026-10-06,CT463127,NOP THUE TNDN QUY 3,0,300000000,FT26316416799871,
55,2026-10-07,CT536018,TT VDX018 THEO DE NGHI,0,16750000,FT26317435484172,
56,2026-10-07,CT759804,TT VDX011 THEO DE NGHI,0,80500000,FT26317832864473,
57,2026-10-07,CT857072,TT VDX008 THEO DE NGHI,0,71000000,FT26317884407474,
58,2026-10-07,CT690320,TT VDX004 THEO DE NGHI,0,13250000,FT26317899491475,
59,2026-10-07,CT522015,TT VDX009 THEO DE NGHI,0,22500000,FT26317649688276,
60,2026-10-07,CT850410,PHI DICH VU SMS BANKING,0,11000,,
61,2026-10-07,CT459286,LAI TIEN GUI THANG 9,1234567,0,,

=== FILE: bank_S2.csv ===
STT,Ngày,Diễn giải,Số CT,PS Nợ,PS Có,Reference number,Reference number_adjust
1,2026-10-01,TT VDX029 THEO DE NGHI,CT751730,0,4179.03,FT26311593441909,
2,2026-10-02,TT VDX030 THEO DE NGHI,CT610431,0,2115.22,FT26312195469721,
3,2026-10-02,NHAN TIEN PLT-STORE-A,CT509962,15107.33,0,STO-20261002-1,
4,2026-10-03,TT VDX003 THEO DE NGHI,CT988394,0,134.32,FT26313775423332,
5,2026-10-04,TT VDX039 THEO DE NGHI,CT410996,0,3009.69,FT26314256857243,
6,2026-10-04,TT PLT-ADS-C,CT643141,0,7696.8,ADS-20261004-1,
7,2026-10-05,TT VDX033 THEO DE NGHI,CT612255,0,3546.26,FT26315336308454,
8,2026-10-05,TT PLT-CLOUD-D,CT550044,0,10710.74,CLO-20261005-1,
9,2026-10-06,TT VDX030 THEO DE NGHI,CT837210,0,722.42,FT26316578736068,
10,2026-10-06,NHAN TIEN PLT-STORE-E,CT660755,9556.73,0,STO-20261006-1,
11,2026-10-06,PHI DICH VU SWIFT,CT375159,0,5.00,,
12,2026-10-07,TT VDX024 THEO DE NGHI,CT996174,0,3547.76,FT26317720388480,

=== FILE: bank_S3.csv ===
STT,Ngày,Số CT,Diễn giải,PS Nợ,PS Có,Reference number,Reference number_adjust,Ghi chú
1,2026-10-01,CT477635,TT VDX033 THEO DE NGHI,0,42000000,FT26311413104306,,
2,2026-10-01,CT526516,TT VDX033 THEO DE NGHI,0,96500000,FT26311979553507,,
3,2026-10-01,CT248442,TT VDX003 THEO DE NGHI,0,95500000,FT26311121890508,,
4,2026-10-01,CT246185,TT VDX017,0,44750000,,FT26311819708612,
5,2026-10-01,CT989385,DONG TRONG,0,0,,,
6,2026-10-02,CT422477,TT VDX012 THEO DE NGHI,0,72250000,FT26312930893018,,
7,2026-10-02,CT767252,TT VDX018 THEO DE NGHI,0,24750000,FT26312759067519,,
8,2026-10-02,CT931199,TT VDX016 THEO DE NGHI,0,34750000,FT26312790564920,,
9,2026-10-03,CT349128,TT VDX019 THEO DE NGHI,0,35750000,FT26313102719329,,
10,2026-10-03,CT714047,TT VDX025 THEO DE NGHI,0,99750000,FT26313629494830,,
11,2026-10-03,CT132034,TT VDX029 THEO DE NGHI,0,1500000,FT26313134372631,,
12,2026-10-03,CT419871,CK VDX036 THANH TOAN,0,49500000,FT26313366914133,,
13,2026-10-03,CT343383,CHUYEN NOI BO NHAN TU HQ1,500000000,0,NB-20261003-1,,
14,2026-10-04,CT465912,TT VDX003 THEO DE NGHI,0,42750000,FT26314145981540,,
15,2026-10-04,CT786826,TT VDX028 THEO DE NGHI,0,10250000,FT26314986028041,,
16,2026-10-04,CT769438,TT VDX025 THEO DE NGHI,0,50500000,FT26314760189042,,
17,2026-10-04,CT907150,TT VDX001,0,7750000,FT26314147506944,,
18,2026-10-05,CT226145,TT VDX028 THEO DE NGHI,0,31250000,FT26315298465451,,
19,2026-10-05,CT732048,TT VDX032 THEO DE NGHI,0,59000000,FT26315422285352,,
20,2026-10-05,CT321412,TT VDX038 THEO DE NGHI,0,2250000,FT26315469254753,,
21,2026-10-05,CT398384,TT VDX035 LAN 1,0,30000000,FT26315401451956,,
22,2026-10-05,CT988258,TT VDX035 LAN 2,0,30000000,FT26315401451956,,
23,2026-10-05,CT723697,CHI LUONG THANG 09 SG2,0,1887000000,FT26315174432358,,
24,2026-10-06,CT436061,TT VDX004 THEO DE NGHI,0,91750000,FT26316410484565,,
25,2026-10-06,CT531398,TT VDX021 THEO DE NGHI,0,81500000,FT26316860547366,,
26,2026-10-06,CT749026,TT VDX029 THEO DE NGHI,0,26500000,FT26316570016267,,
27,2026-10-06,CT352617,CK VDX039 THANH TOAN,0,43250000,FT26316148758569,,
28,2026-10-07,CT296950,TT VDX012 THEO DE NGHI,0,12500000,FT26317398689977,,
29,2026-10-07,CT103692,TT VDX021 THEO DE NGHI,0,80750000,FT26317517806778,,
30,2026-10-07,CT725374,TT VDX025 THEO DE NGHI,0,29250000,FT26317444896479,,

=== FILE: bank_S4.csv ===
STT,Ngày,Số CT,Diễn giải,PS Nợ,PS Có,Reference number,Reference number_adjust
1,2026-10-01,CT201271,CHI TIEN MAT VDX002 VAN PHONG PHAM,0,1200000,,
2,2026-10-02,CT819550,CHI TIEN MAT VDX006 VAN PHONG PHAM,0,1850000,,
3,2026-10-03,CT737890,CHI TIEN MAT VDX006 VAN PHONG PHAM,0,400000,,
4,2026-10-04,CT136599,CHI TIEN MAT VDX012 VAN PHONG PHAM,0,1900000,,
5,2026-10-04,CT686867,NHAP QUY CHUYEN NOI BO TU ACB,50000000,0,NB-20261004-2,
6,2026-10-05,CT286391,CHI TIEN MAT VDX001 VAN PHONG PHAM,0,1450000,,
7,2026-10-06,CT527023,CHI TIEN MAT VDX003 VAN PHONG PHAM,0,400000,,
8,2026-10-06,CT693720,CHI TIEN MAT TIEP KHACH,0,1500000,,
9,2026-10-07,CT428747,CHI TIEN MAT VDX003 VAN PHONG PHAM,0,1650000,,

=== FILE: so_du_dau.csv ===
ma_sheet,tk,ngay,so_du
S1,112001,2026-09-30,20000000000
S2,112002,2026-09-30,850000.00
S3,112003,2026-09-30,5000000000
S4,111001,2026-09-30,200000000

=== FILE: ccr_so_du_go_tay.csv ===
tk,ngay,so_du_cuoi
112001,2026-10-01,19640739000
112001,2026-10-02,19146227400
112001,2026-10-03,18111716400
112001,2026-10-04,17511955400
112001,2026-10-05,14262194400
112001,2026-10-06,13805673912
112001,2026-10-07,13602897479
112002,2026-10-01,845820.97
112002,2026-10-02,858813.08
112002,2026-10-03,858678.76
112002,2026-10-04,847972.27
112002,2026-10-05,833715.27
112002,2026-10-06,842544.58
112002,2026-10-07,838996.82
112003,2026-10-01,4721250000
112003,2026-10-02,4589500000
112003,2026-10-03,4903000000
112003,2026-10-04,4791850000
112003,2026-10-05,2752250000
112003,2026-10-06,2509250000
112003,2026-10-07,2386750000
111001,2026-10-01,198800000
111001,2026-10-02,196950000
111001,2026-10-03,196550000
111001,2026-10-04,244650000
111001,2026-10-05,243200000
111001,2026-10-06,241300000
111001,2026-10-07,239650000

=== FILE: pe_lines.csv ===
ID PESlip,ID PELine,Ngày đề nghị,Mã đối tác,Budget Code (HDCode),Chủ dự toán (CDT1),Loại giao dịch,Số tiền,Tiền tệ,ID PILine
PE-0001,PE-0001-1,2026-10-01,VDX036,OMC | Online Marketing Cost,CSM | Studio M,Tạm ứng (Advance),81000000,VND,PI-0001-1
PE-0002,PE-0002-1,2026-10-01,VDX023,SC | Server Cost,CAH | Apps Hub,Thanh toán (Regular),44750000,VND,
PE-0003,PE-0003-1,2026-10-01,VDX019,API | API,CAH | Apps Hub,Khẩn (Urgent),51500000,VND,PI-0003-1
PE-0004,PE-0004-1,2026-10-01,VDX032,API | API,SHQ2 | Headquarters2,Thanh toán (Regular),6250000,VND,
PE-0005,PE-0005-1,2026-10-01,VDX001,SC | Server Cost,CMN | Media Network,Thanh toán (Regular),65250000,VND,PI-0005-1
PE-0006,PE-0006-1,2026-10-01,VDX033,OMC | Online Marketing Cost,CSM | Studio M,Tạm ứng (Advance),42000000,VND,
PE-0007,PE-0007-1,2026-10-01,VDX033,OMC | Online Marketing Cost,CSM | Studio M,Tạm ứng (Advance),96500000,VND,
PE-0008,PE-0008-1,2026-10-01,VDX003,LC | License Cost,CAH | Apps Hub,Thanh toán (Regular),95500000,VND,PI-0008-1
PE-0009,PE-0009-1,2026-10-01,VDX029,API | API,ASA | Asia Studio,Thanh toán (Regular),4179.03,USD,
PE-0010,PE-0010-1,2026-10-01,VDX038,OGA | GAC - Other,CAH | Apps Hub,Khẩn (Urgent),51500000,VND,PI-0010-1
PE-0011,PE-0011-1,2026-10-01,VDX003,LC | License Cost,CAH | Apps Hub,Khẩn (Urgent),59000000,VND,PI-0011-1
PE-0012,PE-0012-1,2026-10-01,VDX017,LC | License Cost,CAH | Apps Hub,Tạm ứng (Advance),44750000,VND,
PE-0013,PE-0013-1,2026-10-02,VDX037,SC | Server Cost,COR | Core Apps,Khẩn (Urgent),87500000,VND,PI-0013-1
PE-0014,PE-0014-1,2026-10-02,VDX011,API | API,ASA | Asia Studio,Thanh toán (Regular),70000000,VND,PI-0014-1
PE-0015,PE-0015-1,2026-10-02,VDX032,API | API,SHQ2 | Headquarters2,Thanh toán (Regular),39000000,VND,PI-0015-1
PE-0016,PE-0016-1,2026-10-02,VDX020,LC | License Cost,CVL | Venture Lab,Tạm ứng (Advance),24500000,VND,PI-0016-1
PE-0017,PE-0017-1,2026-10-02,VDX028,API | API,CSM | Studio M,Thanh toán (Regular),38250000,VND,PI-0017-1
PE-0018,PE-0018-1,2026-10-02,VDX012,SC | Server Cost,ASA | Asia Studio,Thanh toán (Regular),72250000,VND,PI-0018-1
PE-0019,PE-0019-1,2026-10-02,VDX018,MC | Marketing Cost,COR | Core Apps,Thanh toán (Regular),24750000,VND,
PE-0020,PE-0020-1,2026-10-02,VDX016,OMC | Online Marketing Cost,COR | Core Apps,Thanh toán (Regular),34750000,VND,
PE-0021,PE-0021-1,2026-10-02,VDX030,LC | License Cost,SHQ2 | Headquarters2,Thanh toán (Regular),2115.22,USD,PI-0021-1
PE-0022,PE-0022-1,2026-10-02,VDX035,MC | Marketing Cost,CSM | Studio M,Thanh toán (Regular),60250000,VND,
PE-0022,PE-0022-2,2026-10-02,VDX035,MC | Marketing Cost,CSM | Studio M,Khẩn (Urgent),60750000,VND,PI-0022-2
PE-0022,PE-0022-3,2026-10-02,VDX035,MC | Marketing Cost,ASA | Asia Studio,Tạm ứng (Advance),65250000,VND,PI-0022-3
PE-0023,PE-0023-1,2026-10-03,VDX008,OGA | GAC - Other,CMN | Media Network,Khẩn (Urgent),64500000,VND,PI-0023-1
PE-0024,PE-0024-1,2026-10-03,VDX018,MC | Marketing Cost,COR | Core Apps,Thanh toán (Regular),91250000,VND,PI-0024-1
PE-0025,PE-0025-1,2026-10-03,VDX011,API | API,ASA | Asia Studio,Khẩn (Urgent),64250000,VND,
PE-0026,PE-0026-1,2026-10-03,VDX001,SC | Server Cost,CMN | Media Network,Tạm ứng (Advance),50500000,VND,PI-0026-1
PE-0027,PE-0027-1,2026-10-03,VDX020,LC | License Cost,CVL | Venture Lab,Tạm ứng (Advance),15500000,VND,
PE-0028,PE-0028-1,2026-10-03,VDX019,API | API,CAH | Apps Hub,Thanh toán (Regular),35750000,VND,
PE-0029,PE-0029-1,2026-10-03,VDX025,OMC | Online Marketing Cost,SHQ2 | Headquarters2,Khẩn (Urgent),99750000,VND,PI-0029-1
PE-0030,PE-0030-1,2026-10-03,VDX029,API | API,ASA | Asia Studio,Khẩn (Urgent),1500000,VND,PI-0030-1
PE-0031,PE-0031-1,2026-10-03,VDX003,LC | License Cost,CAH | Apps Hub,Tạm ứng (Advance),134.32,USD,PI-0031-1
PE-0032,PE-0032-1,2026-10-03,VDX002,LC | License Cost,SHQ2 | Headquarters2,Thanh toán (Regular),480000000,VND,PI-0032-1
PE-0033,PE-0033-1,2026-10-04,VDX033,OMC | Online Marketing Cost,CSM | Studio M,Thanh toán (Regular),23500000,VND,PI-0033-1
PE-0034,PE-0034-1,2026-10-04,VDX023,SC | Server Cost,CAH | Apps Hub,Thanh toán (Regular),95500000,VND,
PE-0035,PE-0035-1,2026-10-04,VDX006,API | API,CVL | Venture Lab,Thanh toán (Regular),1000000,VND,PI-0035-1
PE-0036,PE-0036-1,2026-10-04,VDX001,SC | Server Cost,CMN | Media Network,Tạm ứng (Advance),8250000,VND,PI-0036-1
PE-0037,PE-0037-1,2026-10-04,VDX039,MC | Marketing Cost,ASA | Asia Studio,Thanh toán (Regular),59750000,VND,
PE-0038,PE-0038-1,2026-10-04,VDX003,LC | License Cost,CAH | Apps Hub,Thanh toán (Regular),42750000,VND,PI-0038-1
PE-0039,PE-0039-1,2026-10-04,VDX028,API | API,CSM | Studio M,Khẩn (Urgent),10250000,VND,PI-0039-1
PE-0040,PE-0040-1,2026-10-04,VDX025,OMC | Online Marketing Cost,SHQ2 | Headquarters2,Khẩn (Urgent),50500000,VND,
PE-0041,PE-0041-1,2026-10-04,VDX039,MC | Marketing Cost,ASA | Asia Studio,Khẩn (Urgent),3009.69,USD,PI-0041-1
PE-0042,PE-0042-1,2026-10-04,VDX001,SC | Server Cost,CMN | Media Network,Thanh toán (Regular),5750000,VND,PI-0042-1
PE-0043,PE-0043-1,2026-10-04,VDX027,XYZ | Hạng mục chưa khai,CAH | Apps Hub,Tạm ứng (Advance),81750000,VND,
PE-0044,PE-0044-1,2026-10-05,VDX034,SC | Server Cost,CAH | Apps Hub,Thanh toán (Regular),63500000,VND,PI-0044-1
PE-0045,PE-0045-1,2026-10-05,VDX015,API | API,CVL | Venture Lab,Tạm ứng (Advance),87250000,VND,
PE-0046,PE-0046-1,2026-10-05,VDX026,API | API,SHQ2 | Headquarters2,Tạm ứng (Advance),87750000,VND,PI-0046-1
PE-0047,PE-0047-1,2026-10-05,VDX024,API | API,SHQ2 | Headquarters2,Tạm ứng (Advance),26250000,VND,
PE-0048,PE-0048-1,2026-10-05,VDX035,MC | Marketing Cost,CAH | Apps Hub,Khẩn (Urgent),11500000,VND,PI-0048-1
PE-0049,PE-0049-1,2026-10-05,VDX028,API | API,CSM | Studio M,Khẩn (Urgent),31250000,VND,
PE-0050,PE-0050-1,2026-10-05,VDX032,API | API,SHQ2 | Headquarters2,Thanh toán (Regular),59000000,VND,
PE-0051,PE-0051-1,2026-10-05,VDX038,OGA | GAC - Other,CAH | Apps Hub,Tạm ứng (Advance),2250000,VND,PI-0051-1
PE-0052,PE-0052-1,2026-10-05,VDX033,OMC | Online Marketing Cost,CSM | Studio M,Tạm ứng (Advance),3546.26,USD,PI-0052-1
PE-0053,PE-0053-1,2026-10-05,VDX035,MC | Marketing Cost,SHQ2 | Headquarters2,Khẩn (Urgent),30000000,VND,PI-0053-1
PE-0053,PE-0053-2,2026-10-05,VDX035,MC | Marketing Cost,COR | Core Apps,Khẩn (Urgent),30000000,VND,
PE-0054,PE-0054-1,2026-10-05,VDX037,SC | Server Cost,COR | Core Apps,Tạm ứng (Advance),45500000,VND,PI-0054-1
PE-0055,PE-0055-1,2026-10-06,VDX010,API | API,CSM | Studio M,Khẩn (Urgent),15000000,VND,PI-0055-1
PE-0056,PE-0056-1,2026-10-06,VDX004,OGA | GAC - Other,ASA | Asia Studio,Tạm ứng (Advance),47750000,VND,PI-0056-1
PE-0057,PE-0057-1,2026-10-06,VDX029,API | API,ASA | Asia Studio,Tạm ứng (Advance),22750000,VND,PI-0057-1
PE-0058,PE-0058-1,2026-10-06,VDX014,SC | Server Cost,COR | Core Apps,Thanh toán (Regular),31750000,VND,
PE-0059,PE-0059-1,2026-10-06,VDX034,SC | Server Cost,CAH | Apps Hub,Khẩn (Urgent),21750000,VND,
PE-0060,PE-0060-1,2026-10-06,VDX004,OGA | GAC - Other,ASA | Asia Studio,Khẩn (Urgent),91750000,VND,
PE-0061,PE-0061-1,2026-10-06,VDX021,OMC | Online Marketing Cost,CAH | Apps Hub,Khẩn (Urgent),81500000,VND,
PE-0062,PE-0062-1,2026-10-06,VDX029,API | API,ASA | Asia Studio,Thanh toán (Regular),26500000,VND,
PE-0063,PE-0063-1,2026-10-06,VDX030,LC | License Cost,SHQ2 | Headquarters2,Khẩn (Urgent),722.42,USD,PI-0063-1
PE-0064,PE-0064-1,2026-10-06,VDX011,API | API,ASA | Asia Studio,Tạm ứng (Advance),665.76,USD,PI-0064-1
PE-0065,PE-0065-1,2026-10-07,VDX018,MC | Marketing Cost,COR | Core Apps,Khẩn (Urgent),16750000,VND,PI-0065-1
PE-0066,PE-0066-1,2026-10-07,VDX011,API | API,ASA | Asia Studio,Tạm ứng (Advance),80500000,VND,
PE-0067,PE-0067-1,2026-10-07,VDX008,OGA | GAC - Other,CMN | Media Network,Thanh toán (Regular),71000000,VND,
PE-0068,PE-0068-1,2026-10-07,VDX004,OGA | GAC - Other,ASA | Asia Studio,Tạm ứng (Advance),13250000,VND,
PE-0069,PE-0069-1,2026-10-07,VDX009,API | API,CMN | Media Network,Tạm ứng (Advance),22500000,VND,PI-0069-1
PE-0070,PE-0070-1,2026-10-07,VDX012,SC | Server Cost,ASA | Asia Studio,Tạm ứng (Advance),12500000,VND,PI-0070-1
PE-0071,PE-0071-1,2026-10-07,VDX021,OMC | Online Marketing Cost,CAH | Apps Hub,Tạm ứng (Advance),80750000,VND,PI-0071-1
PE-0072,PE-0072-1,2026-10-07,VDX025,OMC | Online Marketing Cost,SHQ2 | Headquarters2,Thanh toán (Regular),29250000,VND,
PE-0073,PE-0073-1,2026-10-07,VDX024,API | API,SHQ2 | Headquarters2,Tạm ứng (Advance),3547.76,USD,PI-0073-1
PE-0074,PE-0074-1,2026-10-07,VDX032,API | API,SHQ2 | Headquarters2,Khẩn (Urgent),37750000,VND,
PE-0075,PE-0075-1,2026-10-07,VDX026,API | API,SHQ2 | Headquarters2,Tạm ứng (Advance),50250000,VND,PI-0075-1
PE-0076,PE-0076-1,2026-10-07,VDX024,API | API,SHQ2 | Headquarters2,Khẩn (Urgent),54500000,VND,PI-0076-1

=== FILE: pi_lines.csv ===
ID PILine,ID PELine,Bắt đầu dịch vụ,Kết thúc dịch vụ,Hoá đơn
PI-0001-1,PE-0001-1,202610,202611,Chưa có hoá đơn
PI-0003-1,PE-0003-1,202610,202610,Có hoá đơn
PI-0005-1,PE-0005-1,202607,202607,Có hoá đơn
PI-0008-1,PE-0008-1,202609,202609,Có hoá đơn
PI-0010-1,PE-0010-1,202608,202610,Chưa có hoá đơn
PI-0011-1,PE-0011-1,202607,202607,Có hoá đơn
PI-0013-1,PE-0013-1,202610,202610,Có hoá đơn
PI-0014-1,PE-0014-1,202610,202610,Chưa có hoá đơn
PI-0015-1,PE-0015-1,202608,202609,Có hoá đơn
PI-0016-1,PE-0016-1,202609,202611,Có hoá đơn
PI-0017-1,PE-0017-1,202608,202608,Có hoá đơn
PI-0018-1,PE-0018-1,202608,202609,Có hoá đơn
PI-0021-1,PE-0021-1,202607,202608,Chưa có hoá đơn
PI-0022-2,PE-0022-2,202610,202612,Có hoá đơn
PI-0022-3,PE-0022-3,202610,202611,Chưa có hoá đơn
PI-0023-1,PE-0023-1,202608,202609,Có hoá đơn
PI-0024-1,PE-0024-1,202609,202610,Chưa có hoá đơn
PI-0026-1,PE-0026-1,202610,202610,Có hoá đơn
PI-0029-1,PE-0029-1,202609,202611,Có hoá đơn
PI-0030-1,PE-0030-1,202610,202611,Có hoá đơn
PI-0031-1,PE-0031-1,202607,202609,Có hoá đơn
PI-0032-1,PE-0032-1,202610,202611,Chưa có hoá đơn
PI-0033-1,PE-0033-1,202608,202609,Có hoá đơn
PI-0035-1,PE-0035-1,202610,202611,Có hoá đơn
PI-0036-1,PE-0036-1,202609,202610,Chưa có hoá đơn
PI-0038-1,PE-0038-1,202610,202610,Chưa có hoá đơn
PI-0039-1,PE-0039-1,202607,202609,Chưa có hoá đơn
PI-0041-1,PE-0041-1,202608,202610,Có hoá đơn
PI-0042-1,PE-0042-1,202608,202609,Có hoá đơn
PI-0044-1,PE-0044-1,202609,202611,Chưa có hoá đơn
PI-0046-1,PE-0046-1,202609,202610,Chưa có hoá đơn
PI-0048-1,PE-0048-1,202610,202610,Chưa có hoá đơn
PI-0051-1,PE-0051-1,202610,202612,Chưa có hoá đơn
PI-0052-1,PE-0052-1,202608,202609,Chưa có hoá đơn
PI-0053-1,PE-0053-1,202610,202611,Chưa có hoá đơn
PI-0054-1,PE-0054-1,202609,202609,Chưa có hoá đơn
PI-0055-1,PE-0055-1,202609,202611,Chưa có hoá đơn
PI-0056-1,PE-0056-1,202610,202610,Có hoá đơn
PI-0057-1,PE-0057-1,202608,202610,Chưa có hoá đơn
PI-0063-1,PE-0063-1,202610,202611,Có hoá đơn
PI-0064-1,PE-0064-1,202610,202611,Chưa có hoá đơn
PI-0065-1,PE-0065-1,202609,202611,Có hoá đơn
PI-0069-1,PE-0069-1,202610,202612,Chưa có hoá đơn
PI-0070-1,PE-0070-1,202610,202611,Chưa có hoá đơn
PI-0071-1,PE-0071-1,202608,202608,Chưa có hoá đơn
PI-0073-1,PE-0073-1,202610,202610,Có hoá đơn
PI-0075-1,PE-0075-1,202608,202608,Chưa có hoá đơn
PI-0076-1,PE-0076-1,202609,202609,Có hoá đơn

=== FILE: pm_lines.csv ===
ID PMSlip,ID PMLine,ID PELine,Pháp nhân trả,Số tiền,Tiền tệ,Reference number,Status_Final
PM-0001,PM-0001-1,PE-0001-1,HQ1,81000000,VND,FT26311945029001 ,Đã chi
PM-0002,PM-0002-1,PE-0002-1,HQ1,44750000,VND,FT26-311783040802,Đã chi
PM-0003,PM-0003-1,PE-0003-1,HQ1,51500000,VND,ft26311428206803,Đã chi
PM-0004,PM-0004-1,PE-0004-1,HQ1,6250000,VND,FT26 311255320604,Đã chi
PM-0005,PM-0005-1,PE-0005-1,HQ1,65250000,VND,ft26311724690505,Đã chi
PM-0006,PM-0006-1,PE-0006-1,SG2,42000000,VND,FT26-311413104306,Đã chi
PM-0007,PM-0007-1,PE-0007-1,SG2,96500000,VND,ft26311979553507,Đã chi
PM-0008,PM-0008-1,PE-0008-1,SG2,95500000,VND,FT26-311121890508,Đã chi
PM-0009,PM-0009-1,PE-0009-1,HQ1,4179.03,USD,ft26311593441909,Đã chi
PM-0010,PM-0010-1,PE-0010-1,HQ1,51500000,VND,FT26-311539594510,Đã chi
PM-0011,PM-0011-1,PE-0011-1,HQ1,59000000,VND,FT26 311596037311,Đã chi
PM-0012,PM-0012-1,PE-0012-1,SG2,44750000,VND,FT26 311819708612,Đã chi
PM-0013,PM-0013-1,PE-0013-1,HQ1,87500000,VND,FT26 312522852413,Đã chi
PM-0014,PM-0014-1,PE-0014-1,HQ1,70000000,VND,FT26312461807714 ,Đã chi
PM-0015,PM-0015-1,PE-0015-1,HQ1,39000000,VND,FT26 312141612915,Đã chi
PM-0016,PM-0016-1,PE-0016-1,HQ1,24500000,VND,ft26312119893116,Đã chi
PM-0017,PM-0017-1,PE-0017-1,HQ1,38250000,VND,ft26312869733017,Đã chi
PM-0018,PM-0018-1,PE-0018-1,SG2,72250000,VND,ft26312930893018,Đã chi
PM-0019,PM-0019-1,PE-0019-1,SG2,24750000,VND,FT26-312759067519,Đã chi
PM-0020,PM-0020-1,PE-0020-1,SG2,34750000,VND,FT26312790564920,Đã chi
PM-0021,PM-0021-1,PE-0021-1,HQ1,2115.22,USD,FT26-312195469721,Đã chi
PM-0022,PM-0022-1,PE-0022-1,HQ1,60250000,VND,FT26 312784968823,Đã chi
PM-0022,PM-0022-2,PE-0022-2,HQ1,60750000,VND,FT26312784968823,Đã chi
PM-0022,PM-0022-3,PE-0022-3,HQ1,65250000,VND,FT26312784968823,Đã chi
PM-0023,PM-0023-1,PE-0023-1,HQ1,64500000,VND,FT26313207523124,Đã chi
PM-0024,PM-0024-1,PE-0024-1,HQ1,91250000,VND,FT26-313976987225,Đã chi
PM-0025,PM-0025-1,PE-0025-1,HQ1,64250000,VND,ft26313995920026,Đã chi
PM-0026,PM-0026-1,PE-0026-1,HQ1,50500000,VND,FT26313757920427,Đã chi
PM-0027,PM-0027-1,PE-0027-1,HQ1,15500000,VND,FT26313566465428,Đã chi
PM-0028,PM-0028-1,PE-0028-1,SG2,35750000,VND,FT26313102719329,Đã chi
PM-0029,PM-0029-1,PE-0029-1,SG2,99750000,VND,FT26313629494830,Đã chi
PM-0030,PM-0030-1,PE-0030-1,SG2,1500000,VND,FT26-313134372631,Đã chi
PM-0031,PM-0031-1,PE-0031-1,HQ1,134.32,USD,FT26-313775423332,Đã chi
PM-0032,PM-0032-1,PE-0032-1,HQ1,480000000,VND,FT26313227239234 ,Đã chi
PM-0033,PM-0033-1,PE-0033-1,HQ1,23500000,VND,ft26314394058035,Đã chi
PM-0034,PM-0034-1,PE-0034-1,HQ1,95500000,VND,FT26314244677536 ,Đã chi
PM-0035,PM-0035-1,PE-0035-1,HQ1,1000000,VND,ft26314451780637,Đã chi
PM-0036,PM-0036-1,PE-0036-1,HQ1,8250000,VND,FT26314532901538,Đã chi
PM-0037,PM-0037-1,PE-0037-1,HQ1,59750000,VND,ft26314102877139,Đã chi
PM-0038,PM-0038-1,PE-0038-1,SG2,42750000,VND,FT26-314145981540,Đã chi
PM-0039,PM-0039-1,PE-0039-1,SG2,10250000,VND,FT26314986028041,Đã chi
PM-0040,PM-0040-1,PE-0040-1,SG2,50500000,VND,FT26 314760189042,Đã chi
PM-0041,PM-0041-1,PE-0041-1,HQ1,3009.69,USD,ft26314256857243,Đã chi
PM-0042,PM-0042-1,PE-0042-1,SG2,5750000,VND,FT26314147506944 ,Đã chi
PM-0043,PM-0043-1,PE-0043-1,HQ1,81750000,VND,ft26314138373745,Đã chi
PM-0044,PM-0044-1,PE-0044-1,HQ1,63500000,VND,FT26315330493746,Đã chi
PM-0045,PM-0045-1,PE-0045-1,HQ1,87250000,VND,FT26315859448247 ,Đã chi
PM-0046,PM-0046-1,PE-0046-1,HQ1,87750000,VND,ft26315884482548,Đã chi
PM-0047,PM-0047-1,PE-0047-1,HQ1,26250000,VND,FT26315520002049 ,Đã chi
PM-0048,PM-0048-1,PE-0048-1,HQ1,11500000,VND,FT26315628558650,Đã chi
PM-0049,PM-0049-1,PE-0049-1,SG2,31250000,VND,ft26315298465451,Đã chi
PM-0050,PM-0050-1,PE-0050-1,SG2,59000000,VND,FT26315422285352,Đã chi
PM-0051,PM-0051-1,PE-0051-1,SG2,2250000,VND,FT26 315469254753,Đã chi
PM-0052,PM-0052-1,PE-0052-1,HQ1,3546.26,USD,FT26 315336308454,Đã chi
PM-0053,PM-0053-1,PE-0053-1,SG2,30000000,VND,FT26-315401451956,Đã chi
PM-0053,PM-0053-2,PE-0053-2,SG2,30000000,VND,FT26315401451956,Đã chi
PM-0054,PM-0054-1,PE-0054-1,HQ1,45500000,VND,4.36619E+15,Đã chi
PM-0055,PM-0055-1,PE-0055-1,HQ1,15000000,VND,FT26-316287582560,Đã chi
PM-0056,PM-0056-1,PE-0056-1,HQ1,47750000,VND,ft26316796706461,Đã chi
PM-0057,PM-0057-1,PE-0057-1,HQ1,22750000,VND,FT26316818722162 ,Đã chi
PM-0058,PM-0058-1,PE-0058-1,HQ1,31750000,VND,FT26316723291063 ,Đã chi
PM-0059,PM-0059-1,PE-0059-1,HQ1,21750000,VND,FT26316169504864 ,Đã chi
PM-0060,PM-0060-1,PE-0060-1,SG2,91750000,VND,FT26 316410484565,Đã chi
PM-0061,PM-0061-1,PE-0061-1,SG2,81500000,VND,FT26316860547366,Đã chi
PM-0062,PM-0062-1,PE-0062-1,SG2,26500000,VND,FT26-316570016267,Đã chi
PM-0063,PM-0063-1,PE-0063-1,HQ1,722.42,USD,FT26316578736068 ,Đã chi
PM-0064,PM-0064-1,PE-0064-1,HQ1,665.76,USD,FT26316880287270,Đã chi
PM-0065,PM-0065-1,PE-0065-1,HQ1,16750000,VND,FT26317435484172 ,Đã chi
PM-0066,PM-0066-1,PE-0066-1,HQ1,80500000,VND,FT26317832864473 ,Đã chi
PM-0067,PM-0067-1,PE-0067-1,HQ1,71000000,VND,ft26317884407474,Đã chi
PM-0068,PM-0068-1,PE-0068-1,HQ1,13250000,VND,ft26317899491475,Đã chi
PM-0069,PM-0069-1,PE-0069-1,HQ1,22500000,VND,FT26317649688276 ,Đã chi
PM-0070,PM-0070-1,PE-0070-1,SG2,12500000,VND,ft26317398689977,Đã chi
PM-0071,PM-0071-1,PE-0071-1,SG2,80750000,VND,FT26317517806778,Đã chi
PM-0072,PM-0072-1,PE-0072-1,SG2,29250000,VND,FT26 317444896479,Đã chi
PM-0073,PM-0073-1,PE-0073-1,HQ1,3547.76,USD,FT26 317720388480,Đã chi
PM-0074,PM-0074-1,PE-0074-1,HQ1,37750000,VND,FT26317219237181 ,Đã chi
PM-0075,PM-0075-1,PE-0075-1,HQ1,50250000,VND,FT26317980644782 ,Đã chi
PM-0076,PM-0076-1,PE-0076-1,HQ1,54500000,VND,ft26317306912483,Đã chi

=== FILE: h1000.csv ===
ID dòng,Pháp nhân,Kỳ lương,Loại,Budget Code (HDCode),Chủ dự toán (CDT1),Số tiền,Số CT
H-001,HQ1,202609,NIS,NIS | Net Income Salary,SHQ2 | Headquarters2,779000000,FT26315985095257
H-002,HQ1,202609,NIS,NIS | Net Income Salary,CSM | Studio M,222000000,FT26315985095257
H-003,HQ1,202609,NIS,NIS | Net Income Salary,CVL | Venture Lab,809000000,FT26315985095257
H-004,HQ1,202609,INT,INT | Insurance,ASA | Asia Studio,94000000,FT26315985095257
H-005,HQ1,202609,COM,COM | Commission,CAH | Apps Hub,822000000,FT26315985095257
H-006,SG2,202609,NIS,NIS | Net Income Salary,CSM | Studio M,450000000,FT26315174432358
H-007,SG2,202609,NIS,NIS | Net Income Salary,ASA | Asia Studio,123000000,FT26315174432358
H-008,SG2,202609,NIS,NIS | Net Income Salary,SHQ2 | Headquarters2,761000000,FT26315174432358
H-009,SG2,202609,INT,INT | Insurance,SHQ2 | Headquarters2,311000000,FT26315174432358
H-010,SG2,202609,COM,COM | Commission,COR | Core Apps,242000000,FT26315174432358
H-011,HQ1,202609,PIT,PIT | Personal Income Tax,CVL | Venture Lab,69000000,FT26315267602159
H-012,HQ1,202609,PIT,PIT | Personal Income Tax,COR | Core Apps,35000000,FT26315267602159

=== FILE: plt.csv ===
ID dòng,Loại,Vendor,Ngày sử dụng,Sản phẩm,Chủ dự toán (CDT1),Số tiền,Tiền tệ,Combine Code
GI-001,GI,PLT-STORE-A,2026-09-08,APP-17,CMN | Media Network,7122.54,USD,STO-20261002-1
GI-002,GI,PLT-STORE-A,2026-09-13,APP-65,CMN | Media Network,1619.47,USD,STO-20261002-1
GI-003,GI,PLT-STORE-A,2026-09-17,APP-62,CVL | Venture Lab,5827.41,USD,STO-20261002-1
GI-004,GI,PLT-STORE-A,2026-09-16,APP-62,CSM | Studio M,537.91,USD,STO-20261002-1
PS-005,PS,PLT-SVC-B,2026-09-13,APP-62,CAH | Apps Hub,2250000,VND,SVC-20261003-1
PS-006,PS,PLT-SVC-B,2026-09-17,APP-20,CAH | Apps Hub,46250000,VND,SVC-20261003-1
OMC-007,OMC,PLT-ADS-C,2026-09-06,APP-40,CSM | Studio M,289.9,USD,ADS-20261004-1
OMC-008,OMC,PLT-ADS-C,2026-09-22,APP-94,CVL | Venture Lab,1303.8,USD,ADS-20261004-1
OMC-009,OMC,PLT-ADS-C,2026-09-16,APP-58,COR | Core Apps,6103.1,USD,ADS-20261004-1
SC-010,SC,PLT-CLOUD-D,2026-09-04,APP-97,CAH | Apps Hub,4418.62,USD,CLO-20261005-1
SC-011,SC,PLT-CLOUD-D,2026-09-22,APP-99,ASA | Asia Studio,6292.12,USD,CLO-20261005-1
GI-012,GI,PLT-STORE-E,2026-09-27,APP-84,COR | Core Apps,5232.63,USD,STO-20261006-1
GI-013,GI,PLT-STORE-E,2026-09-02,APP-81,CMN | Media Network,2632.89,USD,STO-20261006-1
GI-014,GI,PLT-STORE-E,2026-09-04,APP-58,CVL | Venture Lab,1691.21,USD,STO-20261006-1

=== FILE: mapping_master.csv ===
H_hd,nhom_pl,K_can_phan_bo,L_phuong_phap
GI | Gross Inflow,GI,,
OMC | Online Marketing Cost,OMC,,
API | API,API,,
SC | Server Cost,SC,,
LC | License Cost,LC,,
PS | Platform Service,PS,,
NIS | Net Income Salary,HR,Need to Allocate to CFA2,By NOEM
INT | Insurance,HR,Need to Allocate to CFA2,By NOEM
COM | Commission,HR,Need to Allocate to CFA2,By NOEM
PIT | Personal Income Tax,HR,Need to Allocate to CFA2,By NOEM
MC | Marketing Cost,MC,Need to Allocate to CFA2,By GI
OGA | GAC - Other,GAC,Need to Allocate to CFA2,By NOEM
FI | Financial Income,FI,,
BF | Bank Fee,BF,Need to Allocate to CFA2,By LE
CIT | Corporate Income Tax,CIT,,
NB | Lưu chuyển nội bộ,NB,,

=== FILE: lich_su_vendor.csv ===
vendor,hd,cdt1
VDX001,SC | Server Cost,CMN | Media Network
VDX002,LC | License Cost,SHQ2 | Headquarters2
VDX003,LC | License Cost,CAH | Apps Hub
VDX004,OGA | GAC - Other,ASA | Asia Studio
VDX005,OGA | GAC - Other,ASA | Asia Studio
VDX006,API | API,CVL | Venture Lab
VDX007,SC | Server Cost,CAH | Apps Hub
VDX008,OGA | GAC - Other,CMN | Media Network
VDX009,API | API,CMN | Media Network
VDX010,API | API,CSM | Studio M
VDX011,API | API,ASA | Asia Studio
VDX012,SC | Server Cost,ASA | Asia Studio
VDX013,API | API,CAH | Apps Hub
VDX014,SC | Server Cost,COR | Core Apps
VDX015,API | API,CVL | Venture Lab
VDX016,OMC | Online Marketing Cost,COR | Core Apps
VDX017,LC | License Cost,CAH | Apps Hub
VDX018,MC | Marketing Cost,COR | Core Apps
VDX019,API | API,CAH | Apps Hub
VDX020,LC | License Cost,CVL | Venture Lab
VDX021,OMC | Online Marketing Cost,CAH | Apps Hub
VDX022,OMC | Online Marketing Cost,SHQ2 | Headquarters2
VDX023,SC | Server Cost,CAH | Apps Hub
VDX024,API | API,SHQ2 | Headquarters2

=== FILE: ty_gia.csv ===
thang,tien_te,ty_gia
2026-10,VND,1
2026-10,USD,26300
