# BÁO CÁO TOÀN DIỆN LUỒNG FLS (FINANCE LEDGER SYSTEM) & THINKING STEPS
**Kỳ dữ liệu:** 01/10/2026 – 07/10/2026  
**Đơn vị áp dụng:** Tập đoàn đa pháp nhân (HQ1, SG2)  
**Quy chuẩn tiền tệ & Tỷ giá:** VND = 1, USD = 26,300 VND.

---

# PHẦN I. THINKING STEPS & PHÂN TÍCH TỪNG AGENT

## 1. Agent 1 · Thu thập & Kiểm định Nguồn (Collect Raw Data)
- **Tách thông tin sheet:**
  - `S1`: `R | 112001_ACB VND_HQ1` $\rightarrow$ TK `112001`, Ngân hàng `ACB`, Cur `VND`, LE `HQ1`.
  - `S2`: `R | 112002_VCB USD_HQ1` $\rightarrow$ TK `112002`, Ngân hàng `VCB`, Cur `USD`, LE `HQ1`.
  - `S3`: `R | 112003_TCB VND_SG2` $\rightarrow$ TK `112003`, Ngân hàng `TCB`, Cur `VND`, LE `SG2`.
  - `S4`: `R | 111001_QUY VND_HQ1` $\rightarrow$ TK `111001`, Ngân hàng `QUY`, Cur `VND`, LE `HQ1`.
- **So khớp cột với Bản khai chuẩn (`ban_khai_cot.csv`):**
  - Bản khai chuẩn gồm: `STT`, `Ngày`, `Số CT`, `Diễn giải`, `PS Nợ`, `PS Có`, `Reference number`, `Reference number_adjust`.
  - Sheet `S1`: Khớp đúng 100% về tập tên và thứ tự $\rightarrow$ Danh sách thay đổi: `[]`.
  - Sheet `S2`: Tiêu đề là `STT, Ngày, Diễn giải, Số CT, PS Nợ, PS Có, Reference number, Reference number_adjust` (hoán đổi vị trí giữa `Diễn giải` và `Số CT`), tập tên đầy đủ $\rightarrow$ Ghi nhận `{"loai": "doi_vi_tri", "cot": "*"}`.
  - Sheet `S3`: Có thêm cột `Ghi chú` $\rightarrow$ Ghi nhận `{"loai": "them", "cot": "Ghi chú"}`.
  - Sheet `S4`: Khớp đúng 100% $\rightarrow$ `[]`.
- **Đếm số dòng phát sinh có tiền (`PS Nợ` $\neq 0$ hoặc `PS Có` $\neq 0$):**
  - `S1`: Tổng 61 dòng, dòng `STT 46` là dòng trống (0/0) $\rightarrow$ Đếm 60 dòng.
  - `S2`: 12 dòng đều có tiền $\rightarrow$ Đếm 12 dòng.
  - `S3`: Tổng 30 dòng, dòng `STT 5` là dòng trống $\rightarrow$ Đếm 29 dòng.
  - `S4`: 9 dòng đều có tiền $\rightarrow$ Đếm 9 dòng.
- **Đếm các bảng nguồn phụ trợ:**
  - `pe_lines`: 79 dòng.
  - `pi_lines`: 48 dòng.
  - `pm_lines`: 79 dòng.
  - `h1000`: 12 dòng.
  - `plt`: 14 dòng.

---

## 2. Agent 2 · Dựng Sổ Cái & Khớp Đối Chiếu (Generate Group Ledger & Matching)
- **Lọc dòng hợp lệ:**
  - Bỏ dòng 0 ở cả 2 phía: `S1-46` và `S3-5`.
  - Khử trùng: Dòng `S1-26` giống hệt `S1-22` (Ngày `2026-10-03`, Số CT `CT754752`, Diễn giải `PHI DICH VU SMS BANKING`, Có `11000`, Ref rỗng) $\rightarrow$ Giữ `S1-22`, loại `S1-26` và đẩy `S1-26` vào lỗi `TRUNG` tại Agent 4.
  - Xác định mã tham chiếu `ref`: Ưu tiên lấy `Reference number_adjust` nếu có, ngược lại lấy `Reference number`.
    - Ví dụ `S1-7`: Ref ban đầu là `FT26SAI346`, Ref adjust là `FT26311539594510` $\rightarrow$ Lấy `FT26311539594510`.
    - Ví dụ `S1-45`: Ref là `4366190000000000` (được bảo toàn dạng nguyên khi chuẩn hóa số mũ khoa học từ PM `4.36619E+15`).
- **Chuẩn hóa mã (`canon_ref`):**
  - Xóa toàn bộ ký tự phân tách (`-`, `_`, `.`, `,`, `/`, `\`, khoảng trắng), chuyển thành chữ in hoa và xử lý số khoa học.
- **Phân loại hình khớp (Matching Topology):**
  - **Hình A (1 Bank $\times$ 1 Nguồn):** Phần lớn các giao dịch PM khớp 1-1 chính xác số tiền.
  - **Hình B (1 Bank $\times$ N Nguồn):**
    - `S1-16` khớp 3 dòng PM của `PE-0022` ($60.250.000 + 60.750.000 + 65.250.000 = 186.250.000$, bank thanh toán $186.250.600$, chênh lệch 600 VND nằm trong dung sai $\leq 1.000$ VND, phân bổ vào dòng cuối cùng).
    - `S1-25` (SVC-20261003-1) khớp 2 dòng PLT ($2.250.000 + 46.250.000 = 48.500.000$).
    - `S1-43` (Chi lương HQ1) khớp 5 dòng H1000 ($779M + 222M + 809M + 94M + 822M = 2.726.000.000$).
    - `S1-44` (Nộp thuế TNCN) khớp 2 dòng H1000 ($69M + 35M = 104.000.000$).
    - `S2-3` (STO-20261002-1) khớp 4 dòng PLT thu ($7122.54 + 1619.47 + 5827.41 + 537.91 = 15107.33$).
    - `S2-6` (ADS-20261004-1) khớp 3 dòng PLT chi ($289.9 + 1303.8 + 6103.1 = 7696.8$).
    - `S2-8` (CLO-20261005-1) khớp 2 dòng PLT chi ($4418.62 + 6292.12 = 10710.74$).
    - `S2-10` (STO-20261006-1) khớp 3 dòng PLT thu ($5232.63 + 2632.89 + 1691.21 = 9556.73$).
    - `S3-23` (Chi lương SG2) khớp 5 dòng H1000 ($450M + 123M + 761M + 311M + 242M = 1.887.000.000$).
  - **Hình C (N Bank $\times$ 1 Nguồn):**
    - Mã `FT26313227239234` có 2 dòng Bank (`S1-23` chi 200M và `S1-33` chi 280M), khớp đúng 1 dòng PM của `PE-0032` (480M).
  - **Hình D (N Bank $\times$ M Nguồn):**
    - Mã `FT26315401451956` có 2 dòng Bank (`S3-21` và `S3-22`, mỗi dòng 30M) và 2 dòng PM (`PM-0053-1` và `PM-0053-2`, mỗi dòng 30M). Theo quy tắc, không đoán chia $\rightarrow$ Gán hình `D`.
  - **Hình E (Lệch tiền tệ):**
    - Mã `FT26316880287270`: Dòng Bank `S1-53` có tiền tệ VND ($17.509.488$), dòng PM `PM-0064-1` có tiền tệ USD ($665.76$) $\rightarrow$ Gán hình `E`.
  - **Hình F (Lệch tiền vượt dung sai):**
    - Mã `FT26314147506944`: Dòng Bank `S3-17` là $7.750.000$ VND, trong khi PM `PM-0042-1` là $5.750.000$ VND $\rightarrow$ Lệch $2.000.000 > 1.000$ dung sai $\rightarrow$ Gán hình `F`.
  - **Hình KHONG_GHEP:**
    - Chỉ có ở Bank hoặc chỉ có ở PM (như phí ngân hàng, nộp thuế TNDN, chuyển tiền nội bộ, lãi tiền gửi, hoặc các mã PM ngày 07/10 chưa thanh toán qua bank).

---

## 3. Agent 3 · Dựng Sổ ITL Hiệu Lực (ITL Adjust)
- **Áp quy tắc Classifying (S) & Manual Input (T):**
  - Các dòng khớp nguồn (Hình A, B, C) nhận giá trị S từ PE/PI/PLT/H1000, T để trống.
  - Các dòng không có nguồn (bao gồm Hình D, E, F và Không ghép) có $S = \text{Need to manual input}$. Xét Diễn giải của Bank:
    - Chứa `CHUYEN NOI BO` $\rightarrow$ `NB | Lưu chuyển nội bộ`, `Chuyển nội bộ`, `SHQ2 | Headquarters2`.
    - Chứa `PHI DICH VU` $\rightarrow$ `BF | Bank Fee`, `Phí ngân hàng`, `SHQ2 | Headquarters2`.
    - Chứa `LAI TIEN GUI` $\rightarrow$ `FI | Financial Income`, `Thu khác`, `SHQ2 | Headquarters2`.
    - Chứa `NOP THUE TNDN` $\rightarrow$ `CIT | Corporate Income Tax`, `Nộp thuế`, `SHQ2 | Headquarters2`.
    - Khớp mã Vendor trong `lich_su_vendor.csv`:
      - `S4-1` (VDX002) $\rightarrow$ `LC`, `SHQ2`.
      - `S1-15` (VDX017) $\rightarrow$ `LC`, `CAH`.
      - `S4-2` (VDX006) $\rightarrow$ `API`, `CVL`.
      - `S4-3` (VDX006) $\rightarrow$ `API`, `CVL`.
      - `S3-17` (VDX001) $\rightarrow$ `SC`, `CMN`.
      - `S4-4` (VDX012) $\rightarrow$ `SC`, `ASA`.
      - `S1-42` (VDX002) $\rightarrow$ `LC`, `SHQ2`.
      - `S4-6` (VDX001) $\rightarrow$ `SC`, `CMN`.
      - `S1-53` (VDX011) $\rightarrow$ `API`, `ASA`.
      - `S4-7` (VDX003) $\rightarrow$ `LC`, `CAH`.
      - `S4-9` (VDX003) $\rightarrow$ `LC`, `CAH`.
    - Không khớp quy tắc / Không có căn cứ:
      - `S3-12` (Diễn giải `CK VDX036 THANH TOAN` - VDX036 không có trong lịch sử) $\rightarrow$ T = `Input here` $\rightarrow$ V = Default (`OGA | GAC - Other`).
      - `S3-21`, `S3-22` (Diễn giải `TT VDX035...` - VDX035 không có trong lịch sử) $\rightarrow$ T = `Input here` $\rightarrow$ V = Default (`OGA | GAC - Other`).
      - `S3-27` (Diễn giải `CK VDX039 THANH TOAN` - VDX039 không có trong lịch sử) $\rightarrow$ T = `Input here` $\rightarrow$ V = Default (`OGA | GAC - Other`).
      - `S4-8` (Diễn giải `CHI TIEN MAT TIEP KHACH` - không có mã vendor) $\rightarrow$ T = `Input here` $\rightarrow$ V = Default (`OGA | GAC - Other`).
- **Xác định Vùng Allocate & Hàng chờ:**
  - Các dòng có Hình `D`, `E`, `F` hoặc không có nguồn mà T của hd = `Input here` sẽ bị đưa vào `A3_HANG_CHO` và set `work_status = UNMAPPED`.
  - Tra mã HD trên `mapping_master.csv`: Dòng `S1-35` có HD `XYZ | Hạng mục chưa khai` không tìm thấy trong Master $\rightarrow$ `AV = #N/A`, `AW = #N/A`.

---

## 4. Tính toán Chỉ số & Báo cáo CCR Daily
- **Công thức chuyển đổi:**  
  $$\text{bVND} = \frac{\text{Tỷ giá} \times \text{Số tiền}}{10^9}$$  
  $$\text{mUSD} = \frac{\text{bVND} \times 10^3}{\text{Tỷ giá USD}} = \frac{\text{Tỷ giá} \times \text{Số tiền}}{26,300,000}$$
  Giá trị luồng tiền: $v = \text{mUSD}(\text{PS Nợ}) - \text{mUSD}(\text{PS Có})$.
- **Kiểm tra R1_SO_DU:**
  Mọi tài khoản từ ngày 01 đến 07/10 đều có $\text{cuoi\_ky} = \text{ccr\_go} \rightarrow \text{dif} = 0$.
- **Đối chiếu R2_CF & R3_PL:**
  - Nhóm `NB` triệt tiêu khi cộng toàn tập đoàn.
  - Dòng `XYZ` loại khỏi P&L vì không có trong Mapping Master.
  - Các cấp PL được tính lũy kế theo đúng quy ước dấu âm.

---

## 5. Agent 4 · Kiểm toán (Auditor)
- Phát hiện 1 dòng trùng: `S1-26`.
- Phát hiện 1 dòng HD không có trong Master: `S1-35` (`XYZ | Hạng mục chưa khai`).
- Phát hiện 3 mã ghép lệch cần xử lý ngoại lệ: `FT26314147506944` (Hình F), `FT26315401451956` (Hình D), `FT26316880287270` (Hình E).
- Không có lỗi `DIF` số dư ngân hàng.

---

# PHẦN II. CHÍN KHỐI KẾT QUẢ ĐẦU RA CHUẨN ĐỊNH DẠNG FLS

### A1_KIEM_NGUON
```json
{
  "sheet": [
    {
      "ma_sheet": "S1",
      "tk": "112001",
      "ngan_hang": "ACB",
      "cur": "VND",
      "le": "HQ1",
      "thay_doi": [],
      "so_dong": 60
    },
    {
      "ma_sheet": "S2",
      "tk": "112002",
      "ngan_hang": "VCB",
      "cur": "USD",
      "le": "HQ1",
      "thay_doi": [
        {"loai": "doi_vi_tri", "cot": "*"}
      ],
      "so_dong": 12
    },
    {
      "ma_sheet": "S3",
      "tk": "112003",
      "ngan_hang": "TCB",
      "cur": "VND",
      "le": "SG2",
      "thay_doi": [
        {"loai": "them", "cot": "Ghi chú"}
      ],
      "so_dong": 29
    },
    {
      "ma_sheet": "S4",
      "tk": "111001",
      "ngan_hang": "QUY",
      "cur": "VND",
      "le": "HQ1",
      "thay_doi": [],
      "so_dong": 9
    }
  ],
  "pe_lines": 79,
  "pi_lines": 48,
  "pm_lines": 79,
  "h1000_lines": 12,
  "plt_lines": 14
}
```

### A2_LEDGER
```csv
id,ngay,tk,le,cur,ps_no,ps_co,ref
S1-1,2026-10-01,112001,HQ1,VND,0,81000000,FT26311945029001
S1-2,2026-10-01,112001,HQ1,VND,0,44750000,FT26311783040802
S1-3,2026-10-01,112001,HQ1,VND,0,51500000,FT26311428206803
S1-4,2026-10-01,112001,HQ1,VND,0,6250000,FT26311255320604
S1-5,2026-10-01,112001,HQ1,VND,0,65250000,FT26311724690505
S1-6,2026-10-01,112001,HQ1,VND,0,11000,
S1-7,2026-10-01,112001,HQ1,VND,0,51500000,FT26311539594510
S1-8,2026-10-01,112001,HQ1,VND,0,59000000,FT26311596037311
S1-9,2026-10-02,112001,HQ1,VND,0,87500000,FT26312522852413
S1-10,2026-10-02,112001,HQ1,VND,0,70000000,FT26312461807714
S1-11,2026-10-02,112001,HQ1,VND,0,39000000,FT26312141612915
S1-12,2026-10-02,112001,HQ1,VND,0,24500000,FT26312119893116
S1-13,2026-10-02,112001,HQ1,VND,0,38250000,FT26312869733017
S1-14,2026-10-02,112001,HQ1,VND,0,11000,
S1-15,2026-10-02,112001,HQ1,VND,0,49000000,FT26312221436222
S1-16,2026-10-02,112001,HQ1,VND,0,186250600,FT26312784968823
S1-17,2026-10-03,112001,HQ1,VND,0,64500000,FT26313207523124
S1-18,2026-10-03,112001,HQ1,VND,0,91250000,FT26313976987225
S1-19,2026-10-03,112001,HQ1,VND,0,64250000,FT26313995920026
S1-20,2026-10-03,112001,HQ1,VND,0,50500000,FT26313757920427
S1-21,2026-10-03,112001,HQ1,VND,0,15500000,FT26313566465428
S1-22,2026-10-03,112001,HQ1,VND,0,11000,
S1-23,2026-10-03,112001,HQ1,VND,0,200000000,FT26313227239234
S1-24,2026-10-03,112001,HQ1,VND,0,500000000,NB-20261003-1
S1-25,2026-10-03,112001,HQ1,VND,0,48500000,SVC-20261003-1
S1-27,2026-10-04,112001,HQ1,VND,0,23500000,FT26314394058035
S1-28,2026-10-04,112001,HQ1,VND,0,95500000,FT26314244677536
S1-29,2026-10-04,112001,HQ1,VND,0,1000000,FT26314451780637
S1-30,2026-10-04,112001,HQ1,VND,0,8250000,FT26314532901538
S1-31,2026-10-04,112001,HQ1,VND,0,59750000,FT26314102877139
S1-32,2026-10-04,112001,HQ1,VND,0,11000,
S1-33,2026-10-04,112001,HQ1,VND,0,280000000,FT26313227239234
S1-34,2026-10-04,112001,HQ1,VND,0,50000000,NB-20261004-2
S1-35,2026-10-04,112001,HQ1,VND,0,81750000,FT26314138373745
S1-36,2026-10-05,112001,HQ1,VND,0,63500000,FT26315330493746
S1-37,2026-10-05,112001,HQ1,VND,0,87250000,FT26315859448247
S1-38,2026-10-05,112001,HQ1,VND,0,87750000,FT26315884482548
S1-39,2026-10-05,112001,HQ1,VND,0,26250000,FT26315520002049
S1-40,2026-10-05,112001,HQ1,VND,0,11500000,FT26315628558650
S1-41,2026-10-05,112001,HQ1,VND,0,11000,
S1-42,2026-10-05,112001,HQ1,VND,0,98000000,FT26315535529555
S1-43,2026-10-05,112001,HQ1,VND,0,2726000000,FT26315985095257
S1-44,2026-10-05,112001,HQ1,VND,0,104000000,FT26315267602159
S1-45,2026-10-05,112001,HQ1,VND,0,45500000,4366190000000000
S1-47,2026-10-06,112001,HQ1,VND,0,15000000,FT26316287582560
S1-48,2026-10-06,112001,HQ1,VND,0,47750000,FT26316796706461
S1-49,2026-10-06,112001,HQ1,VND,0,22750000,FT26316818722162
S1-50,2026-10-06,112001,HQ1,VND,0,31750000,FT26316723291063
S1-51,2026-10-06,112001,HQ1,VND,0,21750000,FT26316169504864
S1-52,2026-10-06,112001,HQ1,VND,0,11000,
S1-53,2026-10-06,112001,HQ1,VND,0,17509488,FT26316880287270
S1-54,2026-10-06,112001,HQ1,VND,0,300000000,FT26316416799871
S1-55,2026-10-07,112001,HQ1,VND,0,16750000,FT26317435484172
S1-56,2026-10-07,112001,HQ1,VND,0,80500000,FT26317832864473
S1-57,2026-10-07,112001,HQ1,VND,0,71000000,FT26317884407474
S1-58,2026-10-07,112001,HQ1,VND,0,13250000,FT26317899491475
S1-59,2026-10-07,112001,HQ1,VND,0,22500000,FT26317649688276
S1-60,2026-10-07,112001,HQ1,VND,0,11000,
S1-61,2026-10-07,112001,HQ1,VND,1234567,0,
S2-1,2026-10-01,112002,HQ1,USD,0,4179.03,FT26311593441909
S2-2,2026-10-02,112002,HQ1,USD,0,2115.22,FT26312195469721
S2-3,2026-10-02,112002,HQ1,USD,15107.33,0,STO-20261002-1
S2-4,2026-10-03,112002,HQ1,USD,0,134.32,FT26313775423332
S2-5,2026-10-04,112002,HQ1,USD,0,3009.69,FT26314256857243
S2-6,2026-10-04,112002,HQ1,USD,0,7696.8,ADS-20261004-1
S2-7,2026-10-05,112002,HQ1,USD,0,3546.26,FT26315336308454
S2-8,2026-10-05,112002,HQ1,USD,0,10710.74,CLO-20261005-1
S2-9,2026-10-06,112002,HQ1,USD,0,722.42,FT26316578736068
S2-10,2026-10-06,112002,HQ1,USD,9556.73,0,STO-20261006-1
S2-11,2026-10-06,112002,HQ1,USD,0,5.0,
S2-12,2026-10-07,112002,HQ1,USD,0,3547.76,FT26317720388480
S3-1,2026-10-01,112003,SG2,VND,0,42000000,FT26311413104306
S3-2,2026-10-01,112003,SG2,VND,0,96500000,FT26311979553507
S3-3,2026-10-01,112003,SG2,VND,0,95500000,FT26311121890508
S3-4,2026-10-01,112003,SG2,VND,0,44750000,FT26311819708612
S3-6,2026-10-02,112003,SG2,VND,0,72250000,FT26312930893018
S3-7,2026-10-02,112003,SG2,VND,0,24750000,FT26312759067519
S3-8,2026-10-02,112003,SG2,VND,0,34750000,FT26312790564920
S3-9,2026-10-03,112003,SG2,VND,0,35750000,FT26313102719329
S3-10,2026-10-03,112003,SG2,VND,0,99750000,FT26313629494830
S3-11,2026-10-03,112003,SG2,VND,0,1500000,FT26313134372631
S3-12,2026-10-03,112003,SG2,VND,0,49500000,FT26313366914133
S3-13,2026-10-03,112003,SG2,VND,500000000,0,NB-20261003-1
S3-14,2026-10-04,112003,SG2,VND,0,42750000,FT26314145981540
S3-15,2026-10-04,112003,SG2,VND,0,10250000,FT26314986028041
S3-16,2026-10-04,112003,SG2,VND,0,50500000,FT26314760189042
S3-17,2026-10-04,112003,SG2,VND,0,7750000,FT26314147506944
S3-18,2026-10-05,112003,SG2,VND,0,31250000,FT26315298465451
S3-19,2026-10-05,112003,SG2,VND,0,59000000,FT26315422285352
S3-20,2026-10-05,112003,SG2,VND,0,2250000,FT26315469254753
S3-21,2026-10-05,112003,SG2,VND,0,30000000,FT26315401451956
S3-22,2026-10-05,112003,SG2,VND,0,30000000,FT26315401451956
S3-23,2026-10-05,112003,SG2,VND,0,1887000000,FT26315174432358
S3-24,2026-10-06,112003,SG2,VND,0,91750000,FT26316410484565
S3-25,2026-10-06,112003,SG2,VND,0,81500000,FT26316860547366
S3-26,2026-10-06,112003,SG2,VND,0,26500000,FT26316570016267
S3-27,2026-10-06,112003,SG2,VND,0,43250000,FT26316148758569
S3-28,2026-10-07,112003,SG2,VND,0,12500000,FT26317398689977
S3-29,2026-10-07,112003,SG2,VND,0,80750000,FT26317517806778
S3-30,2026-10-07,112003,SG2,VND,0,29250000,FT26317444896479
S4-1,2026-10-01,111001,HQ1,VND,0,1200000,
S4-2,2026-10-02,111001,HQ1,VND,0,1850000,
S4-3,2026-10-03,111001,HQ1,VND,0,400000,
S4-4,2026-10-04,111001,HQ1,VND,0,1900000,
S4-5,2026-10-04,111001,HQ1,VND,50000000,0,NB-20261004-2
S4-6,2026-10-05,111001,HQ1,VND,0,1450000,
S4-7,2026-10-06,111001,HQ1,VND,0,400000,
S4-8,2026-10-06,111001,HQ1,VND,0,1500000,
S4-9,2026-10-07,111001,HQ1,VND,0,1650000,
```

### A2_GHEP
```csv
ma,nguon,so_bank,so_nguon,hinh
4366190000000000,PM,1,1,A
ADS202610041,PLT,1,3,B
CLO202610051,PLT,1,2,B
FT26311121890508,PM,1,1,A
FT26311255320604,PM,1,1,A
FT26311413104306,PM,1,1,A
FT26311428206803,PM,1,1,A
FT26311539594510,PM,1,1,A
FT26311593441909,PM,1,1,A
FT26311596037311,PM,1,1,A
FT26311724690505,PM,1,1,A
FT26311783040802,PM,1,1,A
FT26311819708612,PM,1,1,A
FT26311945029001,PM,1,1,A
FT26311979553507,PM,1,1,A
FT26312119893116,PM,1,1,A
FT26312141612915,PM,1,1,A
FT26312195469721,PM,1,1,A
FT26312221436222,,1,0,KHONG_GHEP
FT26312461807714,PM,1,1,A
FT26312522852413,PM,1,1,A
FT26312759067519,PM,1,1,A
FT26312784968823,PM,1,3,B
FT26312790564920,PM,1,1,A
FT26312869733017,PM,1,1,A
FT26312930893018,PM,1,1,A
FT26313102719329,PM,1,1,A
FT26313134372631,PM,1,1,A
FT26313207523124,PM,1,1,A
FT26313227239234,PM,2,1,C
FT26313366914133,,1,0,KHONG_GHEP
FT26313566465428,PM,1,1,A
FT26313629494830,PM,1,1,A
FT26313757920427,PM,1,1,A
FT26313775423332,PM,1,1,A
FT26313976987225,PM,1,1,A
FT26313995920026,PM,1,1,A
FT26314102877139,PM,1,1,A
FT26314138373745,PM,1,1,A
FT26314145981540,PM,1,1,A
FT26314147506944,PM,1,1,F
FT26314244677536,PM,1,1,A
FT26314256857243,PM,1,1,A
FT26314394058035,PM,1,1,A
FT26314451780637,PM,1,1,A
FT26314532901538,PM,1,1,A
FT26314760189042,PM,1,1,A
FT26314986028041,PM,1,1,A
FT26315174432358,H1000,1,5,B
FT26315267602159,H1000,1,2,B
FT26315298465451,PM,1,1,A
FT26315330493746,PM,1,1,A
FT26315336308454,PM,1,1,A
FT26315401451956,PM,2,2,D
FT26315422285352,PM,1,1,A
FT26315469254753,PM,1,1,A
FT26315520002049,PM,1,1,A
FT26315535529555,,1,0,KHONG_GHEP
FT26315628558650,PM,1,1,A
FT26315859448247,PM,1,1,A
FT26315884482548,PM,1,1,A
FT26315985095257,H1000,1,5,B
FT26316148758569,,1,0,KHONG_GHEP
FT26316169504864,PM,1,1,A
FT26316287582560,PM,1,1,A
FT26316410484565,PM,1,1,A
FT26316416799871,,1,0,KHONG_GHEP
FT26316570016267,PM,1,1,A
FT26316578736068,PM,1,1,A
FT26316723291063,PM,1,1,A
FT26316796706461,PM,1,1,A
FT26316818722162,PM,1,1,A
FT26316860547366,PM,1,1,A
FT26316880287270,PM,1,1,E
FT26317219237181,PM,0,1,KHONG_GHEP
FT26317306912483,PM,0,1,KHONG_GHEP
FT26317398689977,PM,1,1,A
FT26317435484172,PM,1,1,A
FT26317444896479,PM,1,1,A
FT26317517806778,PM,1,1,A
FT26317649688276,PM,1,1,A
FT26317720388480,PM,1,1,A
FT26317832864473,PM,1,1,A
FT26317884407474,PM,1,1,A
FT26317899491475,PM,1,1,A
FT26317980644782,PM,0,1,KHONG_GHEP
NB202610031,,2,0,KHONG_GHEP
NB202610042,,2,0,KHONG_GHEP
STO202610021,PLT,1,4,B
STO202610061,PLT,1,3,B
SVC202610031,PLT,1,2,B
```

### A3_ITL
```csv
itl_id,ngay,tk,le,cur,ps_no,ps_co,nguon,hd_T,hd_V,pay_type_T,pay_type_V,cdt1_T,cdt1_V,svc_start_T,svc_start_V,svc_end_T,svc_end_V,id_payee_T,id_payee_V,invoice_T,invoice_V,AU,AV,AW,work_status
S1-1,2026-10-01,112001,HQ1,VND,0,81000000,PM,,OMC | Online Marketing Cost,,Tạm ứng (Advance),,CSM | Studio M,,202610,,202611,,VDX036,,Chưa có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S1-2,2026-10-01,112001,HQ1,VND,0,44750000,PM,,SC | Server Cost,,Thanh toán (Regular),,CAH | Apps Hub,,,,,,VDX023,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-3,2026-10-01,112001,HQ1,VND,0,51500000,PM,,API | API,,Khẩn (Urgent),,CAH | Apps Hub,,202610,,202610,,VDX019,,Có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-4,2026-10-01,112001,HQ1,VND,0,6250000,PM,,API | API,,Thanh toán (Regular),,SHQ2 | Headquarters2,,,,,,VDX032,,,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-5,2026-10-01,112001,HQ1,VND,0,65250000,PM,,SC | Server Cost,,Thanh toán (Regular),,CMN | Media Network,,202607,,202607,,VDX001,,Có hoá đơn,CMN | Media Network,CMN | Media Network,No need,ok
S1-6,2026-10-01,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-7,2026-10-01,112001,HQ1,VND,0,51500000,PM,,OGA | GAC - Other,,Khẩn (Urgent),,CAH | Apps Hub,,202608,,202610,,VDX038,,Chưa có hoá đơn,CAH | Apps Hub,Need to Allocate to CFA2,By NOEM,ok
S1-8,2026-10-01,112001,HQ1,VND,0,59000000,PM,,LC | License Cost,,Khẩn (Urgent),,CAH | Apps Hub,,202607,,202607,,VDX003,,Có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S2-1,2026-10-01,112002,HQ1,USD,0,4179.03,PM,,API | API,,Thanh toán (Regular),,ASA | Asia Studio,,,,,,VDX029,,,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-1,2026-10-01,112003,SG2,VND,0,42000000,PM,,OMC | Online Marketing Cost,,Tạm ứng (Advance),,CSM | Studio M,,,,,,VDX033,,,CSM | Studio M,CSM | Studio M,No need,ok
S3-2,2026-10-01,112003,SG2,VND,0,96500000,PM,,OMC | Online Marketing Cost,,Tạm ứng (Advance),,CSM | Studio M,,,,,,VDX033,,,CSM | Studio M,CSM | Studio M,No need,ok
S3-3,2026-10-01,112003,SG2,VND,0,95500000,PM,,LC | License Cost,,Thanh toán (Regular),,CAH | Apps Hub,,202609,,202609,,VDX003,,Có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-4,2026-10-01,112003,SG2,VND,0,44750000,PM,,LC | License Cost,,Tạm ứng (Advance),,CAH | Apps Hub,,,,,,VDX017,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S4-1,2026-10-01,111001,HQ1,VND,0,1200000,,LC | License Cost,LC | License Cost,Thanh toán (Regular),Thanh toán (Regular),SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX002,VDX002,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-9,2026-10-02,112001,HQ1,VND,0,87500000,PM,,SC | Server Cost,,Khẩn (Urgent),,COR | Core Apps,,202610,,202610,,VDX037,,Có hoá đơn,COR | Core Apps,COR | Core Apps,No need,ok
S1-10,2026-10-02,112001,HQ1,VND,0,70000000,PM,,API | API,,Thanh toán (Regular),,ASA | Asia Studio,,202610,,202610,,VDX011,,Chưa có hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S1-11,2026-10-02,112001,HQ1,VND,0,39000000,PM,,API | API,,Thanh toán (Regular),,SHQ2 | Headquarters2,,202608,,202609,,VDX032,,Có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-12,2026-10-02,112001,HQ1,VND,0,24500000,PM,,LC | License Cost,,Tạm ứng (Advance),,CVL | Venture Lab,,202609,,202611,,VDX020,,Có hoá đơn,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-13,2026-10-02,112001,HQ1,VND,0,38250000,PM,,API | API,,Thanh toán (Regular),,CSM | Studio M,,202608,,202608,,VDX028,,Có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S1-14,2026-10-02,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-15,2026-10-02,112001,HQ1,VND,0,49000000,,LC | License Cost,LC | License Cost,Thanh toán (Regular),Thanh toán (Regular),CAH | Apps Hub,CAH | Apps Hub,Input here,202610,Input here,202610,VDX017,VDX017,Input here,Nợ hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-16.1,2026-10-02,112001,HQ1,VND,0,60250000,PM,,MC | Marketing Cost,,Thanh toán (Regular),,CSM | Studio M,,,,,,VDX035,,,CSM | Studio M,Need to Allocate to CFA2,By GI,ok
S1-16.2,2026-10-02,112001,HQ1,VND,0,60750000,PM,,MC | Marketing Cost,,Khẩn (Urgent),,CSM | Studio M,,202610,,202612,,VDX035,,Có hoá đơn,CSM | Studio M,Need to Allocate to CFA2,By GI,ok
S1-16.3,2026-10-02,112001,HQ1,VND,0,65250600,PM,,MC | Marketing Cost,,Tạm ứng (Advance),,ASA | Asia Studio,,202610,,202611,,VDX035,,Chưa có hoá đơn,ASA | Asia Studio,Need to Allocate to CFA2,By GI,ok
S2-2,2026-10-02,112002,HQ1,USD,0,2115.22,PM,,LC | License Cost,,Thanh toán (Regular),,SHQ2 | Headquarters2,,202607,,202608,,VDX030,,Chưa có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S2-3.1,2026-10-02,112002,HQ1,USD,7122.54,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CMN | Media Network,,202609,,202609,,PLT-STORE-A,,,CMN | Media Network,CMN | Media Network,No need,ok
S2-3.2,2026-10-02,112002,HQ1,USD,1619.47,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CMN | Media Network,,202609,,202609,,PLT-STORE-A,,,CMN | Media Network,CMN | Media Network,No need,ok
S2-3.3,2026-10-02,112002,HQ1,USD,5827.41,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CVL | Venture Lab,,202609,,202609,,PLT-STORE-A,,,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S2-3.4,2026-10-02,112002,HQ1,USD,537.91,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CSM | Studio M,,202609,,202609,,PLT-STORE-A,,,CSM | Studio M,CSM | Studio M,No need,ok
S3-6,2026-10-02,112003,SG2,VND,0,72250000,PM,,SC | Server Cost,,Thanh toán (Regular),,ASA | Asia Studio,,202608,,202609,,VDX012,,Có hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-7,2026-10-02,112003,SG2,VND,0,24750000,PM,,MC | Marketing Cost,,Thanh toán (Regular),,COR | Core Apps,,,,,,VDX018,,,COR | Core Apps,Need to Allocate to CFA2,By GI,ok
S3-8,2026-10-02,112003,SG2,VND,0,34750000,PM,,OMC | Online Marketing Cost,,Thanh toán (Regular),,COR | Core Apps,,,,,,VDX016,,,COR | Core Apps,COR | Core Apps,No need,ok
S4-2,2026-10-02,111001,HQ1,VND,0,1850000,,API | API,API | API,Thanh toán (Regular),Thanh toán (Regular),CVL | Venture Lab,CVL | Venture Lab,Input here,202610,Input here,202610,VDX006,VDX006,Input here,Nợ hoá đơn,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-17,2026-10-03,112001,HQ1,VND,0,64500000,PM,,OGA | GAC - Other,,Khẩn (Urgent),,CMN | Media Network,,202608,,202609,,VDX008,,Có hoá đơn,CMN | Media Network,Need to Allocate to CFA2,By NOEM,ok
S1-18,2026-10-03,112001,HQ1,VND,0,91250000,PM,,MC | Marketing Cost,,Thanh toán (Regular),,COR | Core Apps,,202609,,202610,,VDX018,,Chưa có hoá đơn,COR | Core Apps,Need to Allocate to CFA2,By GI,ok
S1-19,2026-10-03,112001,HQ1,VND,0,64250000,PM,,API | API,,Khẩn (Urgent),,ASA | Asia Studio,,,,,,VDX011,,,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S1-20,2026-10-03,112001,HQ1,VND,0,50500000,PM,,SC | Server Cost,,Tạm ứng (Advance),,CMN | Media Network,,202610,,202610,,VDX001,,Có hoá đơn,CMN | Media Network,CMN | Media Network,No need,ok
S1-21,2026-10-03,112001,HQ1,VND,0,15500000,PM,,LC | License Cost,,Tạm ứng (Advance),,CVL | Venture Lab,,,,,,VDX020,,,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-22,2026-10-03,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-23,2026-10-03,112001,HQ1,VND,0,200000000,PM,,LC | License Cost,,Thanh toán (Regular),,SHQ2 | Headquarters2,,202610,,202611,,VDX002,,Chưa có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-24,2026-10-03,112001,HQ1,VND,0,500000000,,NB | Lưu chuyển nội bộ,NB | Lưu chuyển nội bộ,Chuyển nội bộ,Chuyển nội bộ,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-25.1,2026-10-03,112001,HQ1,VND,0,2250000,PLT,,PS | Platform Service,,Thanh toán (Regular),,CAH | Apps Hub,,202609,,202609,,PLT-SVC-B,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-25.2,2026-10-03,112001,HQ1,VND,0,46250000,PLT,,PS | Platform Service,,Thanh toán (Regular),,CAH | Apps Hub,,202609,,202609,,PLT-SVC-B,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S2-4,2026-10-03,112002,HQ1,USD,0,134.32,PM,,LC | License Cost,,Tạm ứng (Advance),,CAH | Apps Hub,,202607,,202609,,VDX003,,Có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-9,2026-10-03,112003,SG2,VND,0,35750000,PM,,API | API,,Thanh toán (Regular),,CAH | Apps Hub,,,,,,VDX019,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-10,2026-10-03,112003,SG2,VND,0,99750000,PM,,OMC | Online Marketing Cost,,Khẩn (Urgent),,SHQ2 | Headquarters2,,202609,,202611,,VDX025,,Có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S3-11,2026-10-03,112003,SG2,VND,0,1500000,PM,,API | API,,Khẩn (Urgent),,ASA | Asia Studio,,202610,,202611,,VDX029,,Có hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-12,2026-10-03,112003,SG2,VND,0,49500000,,Input here,OGA | GAC - Other,Input here,Thanh toán (Regular),Input here,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX036,VDX036,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,UNMAPPED
S3-13,2026-10-03,112003,SG2,VND,500000000,0,,NB | Lưu chuyển nội bộ,NB | Lưu chuyển nội bộ,Chuyển nội bộ,Chuyển nội bộ,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S4-3,2026-10-03,111001,HQ1,VND,0,400000,,API | API,API | API,Thanh toán (Regular),Thanh toán (Regular),CVL | Venture Lab,CVL | Venture Lab,Input here,202610,Input here,202610,VDX006,VDX006,Input here,Nợ hoá đơn,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-27,2026-10-04,112001,HQ1,VND,0,23500000,PM,,OMC | Online Marketing Cost,,Thanh toán (Regular),,CSM | Studio M,,202608,,202609,,VDX033,,Có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S1-28,2026-10-04,112001,HQ1,VND,0,95500000,PM,,SC | Server Cost,,Thanh toán (Regular),,CAH | Apps Hub,,,,,,VDX023,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-29,2026-10-04,112001,HQ1,VND,0,1000000,PM,,API | API,,Thanh toán (Regular),,CVL | Venture Lab,,202610,,202611,,VDX006,,Có hoá đơn,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-30,2026-10-04,112001,HQ1,VND,0,8250000,PM,,SC | Server Cost,,Tạm ứng (Advance),,CMN | Media Network,,202609,,202610,,VDX001,,Chưa có hoá đơn,CMN | Media Network,CMN | Media Network,No need,ok
S1-31,2026-10-04,112001,HQ1,VND,0,59750000,PM,,MC | Marketing Cost,,Thanh toán (Regular),,ASA | Asia Studio,,,,,,VDX039,,,ASA | Asia Studio,Need to Allocate to CFA2,By GI,ok
S1-32,2026-10-04,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-33,2026-10-04,112001,HQ1,VND,0,280000000,PM,,LC | License Cost,,Thanh toán (Regular),,SHQ2 | Headquarters2,,202610,,202611,,VDX002,,Chưa có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-34,2026-10-04,112001,HQ1,VND,0,50000000,,NB | Lưu chuyển nội bộ,NB | Lưu chuyển nội bộ,Chuyển nội bộ,Chuyển nội bộ,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-35,2026-10-04,112001,HQ1,VND,0,81750000,PM,,XYZ | Hạng mục chưa khai,,Tạm ứng (Advance),,CAH | Apps Hub,,,,,,VDX027,,,CAH | Apps Hub,#N/A,#N/A,ok
S2-5,2026-10-04,112002,HQ1,USD,0,3009.69,PM,,MC | Marketing Cost,,Khẩn (Urgent),,ASA | Asia Studio,,202608,,202610,,VDX039,,Có hoá đơn,ASA | Asia Studio,Need to Allocate to CFA2,By GI,ok
S2-6.1,2026-10-04,112002,HQ1,USD,0,289.9,PLT,,OMC | Online Marketing Cost,,Thanh toán (Regular),,CSM | Studio M,,202609,,202609,,PLT-ADS-C,,,CSM | Studio M,CSM | Studio M,No need,ok
S2-6.2,2026-10-04,112002,HQ1,USD,0,1303.8,PLT,,OMC | Online Marketing Cost,,Thanh toán (Regular),,CVL | Venture Lab,,202609,,202609,,PLT-ADS-C,,,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S2-6.3,2026-10-04,112002,HQ1,USD,0,6103.1,PLT,,OMC | Online Marketing Cost,,Thanh toán (Regular),,COR | Core Apps,,202609,,202609,,PLT-ADS-C,,,COR | Core Apps,COR | Core Apps,No need,ok
S3-14,2026-10-04,112003,SG2,VND,0,42750000,PM,,LC | License Cost,,Thanh toán (Regular),,CAH | Apps Hub,,202610,,202610,,VDX003,,Chưa có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-15,2026-10-04,112003,SG2,VND,0,10250000,PM,,API | API,,Khẩn (Urgent),,CSM | Studio M,,202607,,202609,,VDX028,,Chưa có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S3-16,2026-10-04,112003,SG2,VND,0,50500000,PM,,OMC | Online Marketing Cost,,Khẩn (Urgent),,SHQ2 | Headquarters2,,,,,,VDX025,,,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S3-17,2026-10-04,112003,SG2,VND,0,7750000,,SC | Server Cost,SC | Server Cost,Thanh toán (Regular),Thanh toán (Regular),CMN | Media Network,CMN | Media Network,Input here,202610,Input here,202610,VDX001,VDX001,Input here,Nợ hoá đơn,CMN | Media Network,CMN | Media Network,No need,UNMAPPED
S4-4,2026-10-04,111001,HQ1,VND,0,1900000,,SC | Server Cost,SC | Server Cost,Thanh toán (Regular),Thanh toán (Regular),ASA | Asia Studio,ASA | Asia Studio,Input here,202610,Input here,202610,VDX012,VDX012,Input here,Nợ hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S4-5,2026-10-04,111001,HQ1,VND,50000000,0,,NB | Lưu chuyển nội bộ,NB | Lưu chuyển nội bộ,Chuyển nội bộ,Chuyển nội bộ,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-36,2026-10-05,112001,HQ1,VND,0,63500000,PM,,SC | Server Cost,,Thanh toán (Regular),,CAH | Apps Hub,,202609,,202611,,VDX034,,Chưa có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-37,2026-10-05,112001,HQ1,VND,0,87250000,PM,,API | API,,Tạm ứng (Advance),,CVL | Venture Lab,,,,,,VDX015,,,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S1-38,2026-10-05,112001,HQ1,VND,0,87750000,PM,,API | API,,Tạm ứng (Advance),,SHQ2 | Headquarters2,,202609,,202610,,VDX026,,Chưa có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-39,2026-10-05,112001,HQ1,VND,0,26250000,PM,,API | API,,Tạm ứng (Advance),,SHQ2 | Headquarters2,,,,,,VDX024,,,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-40,2026-10-05,112001,HQ1,VND,0,11500000,PM,,MC | Marketing Cost,,Khẩn (Urgent),,CAH | Apps Hub,,202610,,202610,,VDX035,,Chưa có hoá đơn,CAH | Apps Hub,Need to Allocate to CFA2,By GI,ok
S1-41,2026-10-05,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-42,2026-10-05,112001,HQ1,VND,0,98000000,,LC | License Cost,LC | License Cost,Thanh toán (Regular),Thanh toán (Regular),SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX002,VDX002,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S1-43.1,2026-10-05,112001,HQ1,VND,0,779000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,SHQ2 | Headquarters2,,202609,,202609,,,,Bỏ qua,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,ok
S1-43.2,2026-10-05,112001,HQ1,VND,0,222000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,CSM | Studio M,,202609,,202609,,,,Bỏ qua,CSM | Studio M,Need to Allocate to CFA2,By NOEM,ok
S1-43.3,2026-10-05,112001,HQ1,VND,0,809000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,CVL | Venture Lab,,202609,,202609,,,,Bỏ qua,CVL | Venture Lab,Need to Allocate to CFA2,By NOEM,ok
S1-43.4,2026-10-05,112001,HQ1,VND,0,94000000,H1000,,INT | Insurance,,Lương (Payroll),,ASA | Asia Studio,,202609,,202609,,,,Bỏ qua,ASA | Asia Studio,Need to Allocate to CFA2,By NOEM,ok
S1-43.5,2026-10-05,112001,HQ1,VND,0,822000000,H1000,,COM | Commission,,Lương (Payroll),,CAH | Apps Hub,,202609,,202609,,,,Bỏ qua,CAH | Apps Hub,Need to Allocate to CFA2,By NOEM,ok
S1-44.1,2026-10-05,112001,HQ1,VND,0,69000000,H1000,,PIT | Personal Income Tax,,Lương (Payroll),,CVL | Venture Lab,,202609,,202609,,,,Bỏ qua,CVL | Venture Lab,Need to Allocate to CFA2,By NOEM,ok
S1-44.2,2026-10-05,112001,HQ1,VND,0,35000000,H1000,,PIT | Personal Income Tax,,Lương (Payroll),,COR | Core Apps,,202609,,202609,,,,Bỏ qua,COR | Core Apps,Need to Allocate to CFA2,By NOEM,ok
S1-45,2026-10-05,112001,HQ1,VND,0,45500000,PM,,SC | Server Cost,,Tạm ứng (Advance),,COR | Core Apps,,202609,,202609,,VDX037,,Chưa có hoá đơn,COR | Core Apps,COR | Core Apps,No need,ok
S2-7,2026-10-05,112002,HQ1,USD,0,3546.26,PM,,OMC | Online Marketing Cost,,Tạm ứng (Advance),,CSM | Studio M,,202608,,202609,,VDX033,,Chưa có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S2-8.1,2026-10-05,112002,HQ1,USD,0,4418.62,PLT,,SC | Server Cost,,Thanh toán (Regular),,CAH | Apps Hub,,202609,,202609,,PLT-CLOUD-D,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S2-8.2,2026-10-05,112002,HQ1,USD,0,6292.12,PLT,,SC | Server Cost,,Thanh toán (Regular),,ASA | Asia Studio,,202609,,202609,,PLT-CLOUD-D,,,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-18,2026-10-05,112003,SG2,VND,0,31250000,PM,,API | API,,Khẩn (Urgent),,CSM | Studio M,,,,,,VDX028,,,CSM | Studio M,CSM | Studio M,No need,ok
S3-19,2026-10-05,112003,SG2,VND,0,59000000,PM,,API | API,,Thanh toán (Regular),,SHQ2 | Headquarters2,,,,,,VDX032,,,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S3-20,2026-10-05,112003,SG2,VND,0,2250000,PM,,OGA | GAC - Other,,Tạm ứng (Advance),,CAH | Apps Hub,,202610,,202612,,VDX038,,Chưa có hoá đơn,CAH | Apps Hub,Need to Allocate to CFA2,By NOEM,ok
S3-21,2026-10-05,112003,SG2,VND,0,30000000,,Input here,OGA | GAC - Other,Input here,Thanh toán (Regular),Input here,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX035,VDX035,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,UNMAPPED
S3-22,2026-10-05,112003,SG2,VND,0,30000000,,Input here,OGA | GAC - Other,Input here,Thanh toán (Regular),Input here,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX035,VDX035,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,UNMAPPED
S3-23.1,2026-10-05,112003,SG2,VND,0,450000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,CSM | Studio M,,202609,,202609,,,,Bỏ qua,CSM | Studio M,Need to Allocate to CFA2,By NOEM,ok
S3-23.2,2026-10-05,112003,SG2,VND,0,123000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,ASA | Asia Studio,,202609,,202609,,,,Bỏ qua,ASA | Asia Studio,Need to Allocate to CFA2,By NOEM,ok
S3-23.3,2026-10-05,112003,SG2,VND,0,761000000,H1000,,NIS | Net Income Salary,,Lương (Payroll),,SHQ2 | Headquarters2,,202609,,202609,,,,Bỏ qua,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,ok
S3-23.4,2026-10-05,112003,SG2,VND,0,311000000,H1000,,INT | Insurance,,Lương (Payroll),,SHQ2 | Headquarters2,,202609,,202609,,,,Bỏ qua,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,ok
S3-23.5,2026-10-05,112003,SG2,VND,0,242000000,H1000,,COM | Commission,,Lương (Payroll),,COR | Core Apps,,202609,,202609,,,,Bỏ qua,COR | Core Apps,Need to Allocate to CFA2,By NOEM,ok
S4-6,2026-10-05,111001,HQ1,VND,0,1450000,,SC | Server Cost,SC | Server Cost,Thanh toán (Regular),Thanh toán (Regular),CMN | Media Network,CMN | Media Network,Input here,202610,Input here,202610,VDX001,VDX001,Input here,Nợ hoá đơn,CMN | Media Network,CMN | Media Network,No need,ok
S1-47,2026-10-06,112001,HQ1,VND,0,15000000,PM,,API | API,,Khẩn (Urgent),,CSM | Studio M,,202609,,202611,,VDX010,,Chưa có hoá đơn,CSM | Studio M,CSM | Studio M,No need,ok
S1-48,2026-10-06,112001,HQ1,VND,0,47750000,PM,,OGA | GAC - Other,,Tạm ứng (Advance),,ASA | Asia Studio,,202610,,202610,,VDX004,,Có hoá đơn,ASA | Asia Studio,Need to Allocate to CFA2,By NOEM,ok
S1-49,2026-10-06,112001,HQ1,VND,0,22750000,PM,,API | API,,Tạm ứng (Advance),,ASA | Asia Studio,,202608,,202610,,VDX029,,Chưa có hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S1-50,2026-10-06,112001,HQ1,VND,0,31750000,PM,,SC | Server Cost,,Thanh toán (Regular),,COR | Core Apps,,,,,,VDX014,,,COR | Core Apps,COR | Core Apps,No need,ok
S1-51,2026-10-06,112001,HQ1,VND,0,21750000,PM,,SC | Server Cost,,Khẩn (Urgent),,CAH | Apps Hub,,,,,,VDX034,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S1-52,2026-10-06,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-53,2026-10-06,112001,HQ1,VND,0,17509488,,API | API,API | API,Thanh toán (Regular),Thanh toán (Regular),ASA | Asia Studio,ASA | Asia Studio,Input here,202610,Input here,202610,VDX011,VDX011,Input here,Nợ hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,UNMAPPED
S1-54,2026-10-06,112001,HQ1,VND,0,300000000,,CIT | Corporate Income Tax,CIT | Corporate Income Tax,Nộp thuế,Nộp thuế,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S2-9,2026-10-06,112002,HQ1,USD,0,722.42,PM,,LC | License Cost,,Khẩn (Urgent),,SHQ2 | Headquarters2,,202610,,202611,,VDX030,,Có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S2-10.1,2026-10-06,112002,HQ1,USD,5232.63,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,COR | Core Apps,,202609,,202609,,PLT-STORE-E,,,COR | Core Apps,COR | Core Apps,No need,ok
S2-10.2,2026-10-06,112002,HQ1,USD,2632.89,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CMN | Media Network,,202609,,202609,,PLT-STORE-E,,,CMN | Media Network,CMN | Media Network,No need,ok
S2-10.3,2026-10-06,112002,HQ1,USD,1691.21,0,PLT,,GI | Gross Inflow,,Thu từ nền tảng,,CVL | Venture Lab,,202609,,202609,,PLT-STORE-E,,,CVL | Venture Lab,CVL | Venture Lab,No need,ok
S2-11,2026-10-06,112002,HQ1,USD,0,5.0,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S3-24,2026-10-06,112003,SG2,VND,0,91750000,PM,,OGA | GAC - Other,,Khẩn (Urgent),,ASA | Asia Studio,,,,,,VDX004,,,ASA | Asia Studio,Need to Allocate to CFA2,By NOEM,ok
S3-25,2026-10-06,112003,SG2,VND,0,81500000,PM,,OMC | Online Marketing Cost,,Khẩn (Urgent),,CAH | Apps Hub,,,,,,VDX021,,,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-26,2026-10-06,112003,SG2,VND,0,26500000,PM,,API | API,,Thanh toán (Regular),,ASA | Asia Studio,,,,,,VDX029,,,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-27,2026-10-06,112003,SG2,VND,0,43250000,,Input here,OGA | GAC - Other,Input here,Thanh toán (Regular),Input here,SHQ2 | Headquarters2,Input here,202610,Input here,202610,VDX039,VDX039,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,UNMAPPED
S4-7,2026-10-06,111001,HQ1,VND,0,400000,,LC | License Cost,LC | License Cost,Thanh toán (Regular),Thanh toán (Regular),CAH | Apps Hub,CAH | Apps Hub,Input here,202610,Input here,202610,VDX003,VDX003,Input here,Nợ hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S4-8,2026-10-06,111001,HQ1,VND,0,1500000,,Input here,OGA | GAC - Other,Input here,Thanh toán (Regular),Input here,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By NOEM,UNMAPPED
S1-55,2026-10-07,112001,HQ1,VND,0,16750000,PM,,MC | Marketing Cost,,Khẩn (Urgent),,COR | Core Apps,,202609,,202611,,VDX018,,Có hoá đơn,COR | Core Apps,Need to Allocate to CFA2,By GI,ok
S1-56,2026-10-07,112001,HQ1,VND,0,80500000,PM,,API | API,,Tạm ứng (Advance),,ASA | Asia Studio,,,,,,VDX011,,,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S1-57,2026-10-07,112001,HQ1,VND,0,71000000,PM,,OGA | GAC - Other,,Thanh toán (Regular),,CMN | Media Network,,,,,,VDX008,,,CMN | Media Network,Need to Allocate to CFA2,By NOEM,ok
S1-58,2026-10-07,112001,HQ1,VND,0,13250000,PM,,OGA | GAC - Other,,Tạm ứng (Advance),,ASA | Asia Studio,,,,,,VDX004,,,ASA | Asia Studio,Need to Allocate to CFA2,By NOEM,ok
S1-59,2026-10-07,112001,HQ1,VND,0,22500000,PM,,API | API,,Tạm ứng (Advance),,CMN | Media Network,,202610,,202612,,VDX009,,Chưa có hoá đơn,CMN | Media Network,CMN | Media Network,No need,ok
S1-60,2026-10-07,112001,HQ1,VND,0,11000,,BF | Bank Fee,BF | Bank Fee,Phí ngân hàng,Phí ngân hàng,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,Need to Allocate to CFA2,By LE,ok
S1-61,2026-10-07,112001,HQ1,VND,1234567,0,,FI | Financial Income,FI | Financial Income,Thu khác,Thu khác,SHQ2 | Headquarters2,SHQ2 | Headquarters2,Input here,202610,Input here,202610,Input here,VD0,Input here,Nợ hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S2-12,2026-10-07,112002,HQ1,USD,0,3547.76,PM,,API | API,,Tạm ứng (Advance),,SHQ2 | Headquarters2,,202610,,202610,,VDX024,,Có hoá đơn,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S3-28,2026-10-07,112003,SG2,VND,0,12500000,PM,,SC | Server Cost,,Tạm ứng (Advance),,ASA | Asia Studio,,202610,,202611,,VDX012,,Chưa có hoá đơn,ASA | Asia Studio,ASA | Asia Studio,No need,ok
S3-29,2026-10-07,112003,SG2,VND,0,80750000,PM,,OMC | Online Marketing Cost,,Tạm ứng (Advance),,CAH | Apps Hub,,202608,,202608,,VDX021,,Chưa có hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
S3-30,2026-10-07,112003,SG2,VND,0,29250000,PM,,OMC | Online Marketing Cost,,Thanh toán (Regular),,SHQ2 | Headquarters2,,,,,,VDX025,,,SHQ2 | Headquarters2,SHQ2 | Headquarters2,No need,ok
S4-9,2026-10-07,111001,HQ1,VND,0,1650000,,LC | License Cost,LC | License Cost,Thanh toán (Regular),Thanh toán (Regular),CAH | Apps Hub,CAH | Apps Hub,Input here,202610,Input here,202610,VDX003,VDX003,Input here,Nợ hoá đơn,CAH | Apps Hub,CAH | Apps Hub,No need,ok
```

### A3_HANG_CHO
```csv
itl_id,ly_do
S3-12,khong_can_cu
S3-17,F
S3-21,D
S3-22,D
S1-53,E
S3-27,khong_can_cu
S4-8,khong_can_cu
```

### R1_SO_DU
```csv
tk,ngay,dau_ky,ps_no,ps_co,cuoi_ky,ccr_go,dif
112001,2026-10-01,20000000000,0,359261000,19640739000,19640739000,0
112001,2026-10-02,19640739000,0,494511600,19146227400,19146227400,0
112001,2026-10-03,19146227400,0,1034511000,18111716400,18111716400,0
112001,2026-10-04,18111716400,0,599761000,17511955400,17511955400,0
112001,2026-10-05,17511955400,0,3249761000,14262194400,14262194400,0
112001,2026-10-06,14262194400,0,456520488,13805673912,13805673912,0
112001,2026-10-07,13805673912,1234567,204011000,13602897479,13602897479,0
112002,2026-10-01,850000.00,0.00,4179.03,845820.97,845820.97,0.00
112002,2026-10-02,845820.97,15107.33,2115.22,858813.08,858813.08,0.00
112002,2026-10-03,858813.08,0.00,134.32,858678.76,858678.76,0.00
112002,2026-10-04,858678.76,0.00,10706.49,847972.27,847972.27,0.00
112002,2026-10-05,847972.27,0.00,14257.00,833715.27,833715.27,0.00
112002,2026-10-06,833715.27,9556.73,727.42,842544.58,842544.58,0.00
112002,2026-10-07,842544.58,0.00,3547.76,838996.82,838996.82,0.00
112003,2026-10-01,5000000000,0,278750000,4721250000,4721250000,0
112003,2026-10-02,4721250000,0,131750000,4589500000,4589500000,0
112003,2026-10-03,4589500000,500000000,186500000,4903000000,4903000000,0
112003,2026-10-04,4903000000,0,111150000,4791850000,4791850000,0
112003,2026-10-05,4791850000,0,2039600000,2752250000,2752250000,0
112003,2026-10-06,2752250000,0,243000000,2509250000,2509250000,0
112003,2026-10-07,2509250000,0,122500000,2386750000,2386750000,0
111001,2026-10-01,200000000,0,1200000,198800000,198800000,0
111001,2026-10-02,198800000,0,1850000,196950000,196950000,0
111001,2026-10-03,196950000,0,400000,196550000,196550000,0
111001,2026-10-04,196550000,50000000,1900000,244650000,244650000,0
111001,2026-10-05,244650000,0,1450000,243200000,243200000,0
111001,2026-10-06,243200000,0,1900000,241300000,241300000,0
111001,2026-10-07,241300000,0,1650000,239650000,239650000,0
```

### R2_CF
```csv
le,hd,2026-10-01,2026-10-02,2026-10-03,2026-10-04,2026-10-05,2026-10-06,2026-10-07,tong
HQ1,API | API,-0.00235741,-0.00411597,-0.00244297,-0.00003802,-0.00765209,-0.00293192,-0.00738698,-0.02692536
HQ1,BF | Bank Fee,-0.00000042,-0.00000042,-0.00000042,-0.00000042,-0.00000042,-0.00000542,-0.00000042,-0.00000794
HQ1,CIT | Corporate Income Tax,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,-0.01140684,0.00000000,-0.01140684
HQ1,COM | Commission,0.00000000,0.00000000,0.00000000,0.00000000,-0.03125475,0.00000000,0.00000000,-0.03125475
HQ1,FI | Financial Income,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,0.00004694,0.00004694
HQ1,GI | Gross Inflow,0.00000000,0.01510733,0.00000000,0.00000000,0.00000000,0.00955673,0.00000000,0.02466406
HQ1,INT | Insurance,0.00000000,0.00000000,0.00000000,0.00000000,-0.00357414,0.00000000,0.00000000,-0.00357414
HQ1,LC | License Cost,-0.00228897,-0.00405202,-0.00832879,-0.01064639,-0.00372624,-0.00073763,-0.00006274,-0.02984278
HQ1,MC | Marketing Cost,0.00000000,-0.00708177,-0.00346958,-0.00528182,-0.00043726,0.00000000,-0.00063688,-0.01690731
HQ1,NB | Lưu chuyển nội bộ,0.00000000,0.00000000,-0.01901141,0.00000000,0.00000000,0.00000000,0.00000000,-0.01901141
HQ1,NIS | Net Income Salary,0.00000000,0.00000000,0.00000000,0.00000000,-0.06882129,0.00000000,0.00000000,-0.06882129
HQ1,OGA | GAC - Other,-0.00195817,0.00000000,-0.00245247,0.00000000,0.00000000,-0.00187262,-0.00326046,-0.00954372
HQ1,OMC | Online Marketing Cost,-0.00307985,0.00000000,0.00000000,-0.00858999,-0.00354626,0.00000000,0.00000000,-0.01521610
HQ1,PIT | Personal Income Tax,0.00000000,0.00000000,0.00000000,0.00000000,-0.00395437,0.00000000,0.00000000,-0.00395437
HQ1,PS | Platform Service,0.00000000,0.00000000,-0.00184411,0.00000000,0.00000000,0.00000000,0.00000000,-0.00184411
HQ1,SC | Server Cost,-0.00418251,-0.00332700,-0.00191992,-0.00394487,-0.01955708,-0.00203422,0.00000000,-0.03496560
HQ1,XYZ | Hạng mục chưa khai,0.00000000,0.00000000,0.00000000,-0.00310837,0.00000000,0.00000000,0.00000000,-0.00310837
HQ1,TOTAL,-0.01386733,-0.00348585,-0.03947007,-0.03160988,-0.13852360,-0.00942690,-0.01130010,-0.28768373
SG2,API | API,0.00000000,0.00000000,-0.00141635,-0.00038973,-0.00343156,-0.00100760,0.00000000,-0.00624524
SG2,COM | Commission,0.00000000,0.00000000,0.00000000,0.00000000,-0.00920152,0.00000000,0.00000000,-0.00920152
SG2,INT | Insurance,0.00000000,0.00000000,0.00000000,0.00000000,-0.01182510,0.00000000,0.00000000,-0.01182510
SG2,LC | License Cost,-0.00533270,0.00000000,0.00000000,-0.00162548,0.00000000,0.00000000,0.00000000,-0.00695818
SG2,MC | Marketing Cost,0.00000000,-0.00094106,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,-0.00094106
SG2,NB | Lưu chuyển nội bộ,0.00000000,0.00000000,0.01901141,0.00000000,0.00000000,0.00000000,0.00000000,0.01901141
SG2,NIS | Net Income Salary,0.00000000,0.00000000,0.00000000,0.00000000,-0.05072243,0.00000000,0.00000000,-0.05072243
SG2,OGA | GAC - Other,0.00000000,0.00000000,-0.00188213,0.00000000,-0.00236692,-0.00513308,0.00000000,-0.00938213
SG2,OMC | Online Marketing Cost,-0.00526616,-0.00132129,-0.00379278,-0.00191992,0.00000000,-0.00309886,-0.00418251,-0.01958152
SG2,SC | Server Cost,0.00000000,-0.00274715,0.00000000,-0.00029468,0.00000000,0.00000000,-0.00047529,-0.00351712
SG2,TOTAL,-0.01059886,-0.00500951,0.01192015,-0.00422981,-0.07754753,-0.00923954,-0.00465780,-0.09934890
```

### R3_PL
```csv
dong,2026-10-01,2026-10-02,2026-10-03,2026-10-04,2026-10-05,2026-10-06,2026-10-07,tong
GI,0.00000000,0.01510733,0.00000000,0.00000000,0.00000000,0.00955673,0.00000000,0.02466406
OMC,-0.00834601,-0.00132129,-0.00379278,-0.01050991,-0.00354626,-0.00309886,-0.00418251,-0.03479762
API,-0.00235741,-0.00411597,-0.00385932,-0.00042776,-0.01108365,-0.00393952,-0.00738698,-0.03317060
SC,-0.00418251,-0.00607414,-0.00191992,-0.00423954,-0.01955708,-0.00203422,-0.00047529,-0.03848270
LC,-0.00762167,-0.00405202,-0.00832879,-0.01227186,-0.00372624,-0.00073763,-0.00006274,-0.03680095
PS,0.00000000,0.00000000,-0.00184411,0.00000000,0.00000000,0.00000000,0.00000000,-0.00184411
HR,0.00000000,0.00000000,0.00000000,0.00000000,-0.17975449,0.00000000,0.00000000,-0.17975449
MC,0.00000000,-0.00802283,-0.00346958,-0.00528182,-0.00043726,0.00000000,-0.00063688,-0.01784837
GAC,-0.00195817,0.00000000,-0.00433460,0.00000000,-0.00236692,-0.00700570,-0.00326046,-0.01892585
FI,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,0.00004694,0.00004694
BF,-0.00000042,-0.00000042,-0.00000042,-0.00000042,-0.00000042,-0.00000542,-0.00000042,-0.00000794
CIT,0.00000000,0.00000000,0.00000000,0.00000000,0.00000000,-0.01140684,0.00000000,-0.01140684
PL2,-0.00834601,0.01378604,-0.00379278,-0.01050991,-0.00354626,0.00645787,-0.00418251,-0.01013356
PL3,-0.02250760,-0.00045609,-0.01790081,-0.02744907,-0.03791323,-0.00025350,-0.01210752,-0.11858781
PL4,-0.02250760,-0.00045609,-0.01974492,-0.02744907,-0.03791323,-0.00025350,-0.01210752,-0.12043192
PL5,-0.02250760,-0.00045609,-0.01974492,-0.02744907,-0.21766772,-0.00025350,-0.01210752,-0.30018641
PL6,-0.02446619,-0.00847934,-0.02754952,-0.03273131,-0.22047232,-0.00726462,-0.01595788,-0.33692107
PL8,-0.02446619,-0.00847934,-0.02754952,-0.03273131,-0.22047232,-0.01867146,-0.01595788,-0.34832791
```

### A4_AUDIT
```json
{
  "loi": [
    {"loai": "TRUNG", "khoa": "S1-26"},
    {"loai": "HD_LA", "khoa": "S1-35"},
    {"loai": "GHEP_LECH", "khoa": "FT26314147506944"},
    {"loai": "GHEP_LECH", "khoa": "FT26315401451956"},
    {"loai": "GHEP_LECH", "khoa": "FT26316880287270"}
  ]
}
```