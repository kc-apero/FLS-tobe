# 03 — PRODUCT LIFECYCLE: milestone `IM0–IM7` + cổng chuyển

**Version:** v0.1 | **Chủ sở hữu:** COO-CFO | **Nguồn:** `NGUỒN-BUILD` §1, §6–§8, §X

Vòng đời = 8 milestone theo 3 phần. Mỗi cổng là **human gate do người vận hành nghiệm thu** (`P-02`), tiêu chí là **đối chiếu với oracle** — sổ `ITL RAW` / `ITL ADJUSTED` cũ (`P-ITL-03`).

> **Từ vựng:** `IM0–IM7` là milestone của **dự án ITL** (`QĐ-ITL-02`). Không lẫn với Module `M0–M6` hay Giai đoạn `GĐ0–GĐ5` của chương trình FIN ERP. Gặp `M0–M7` trong `NGUỒN-BUILD` thì đọc là `IM0–IM7`.

> ⚠ **Đính chính framing (2026-08-24)** — cụm **"thay ~6.843 dòng nhập tay"** ở `IM6` bên dưới là số ô cột `Final` *(AS-IS)*, không phải 6.843 lần người gõ. TO-BE (`QĐ-owner-0820`): bỏ tầng `MID`, `Final` = **kế toán nhập/sửa trực tiếp**; vùng ADJUSTMENT thu về **5 trường trong hợp đồng**; ALLOCATE **máy suy từ `Mapping Master`**. Chi tiết: [`_BA_UPDATE_ROADMAP §3c`](../02_BA/_BA_UPDATE_ROADMAP.md).

---

## 1. Thứ tự & phụ thuộc

```
[A Nền móng]    IM0 Hợp đồng & nền tảng ──> IM1 Lát dọc P100+Cash → ITL
   tuần tự                                        │
                                                  │
[B Mở rộng ∥]   ├─> IM2 Dòng tiền + A-CCR reconcile
   song song    ├─> IM3 HR · H1000
   sau IM1      ├─> IM4 Platform GI/OMC/SC/PS
                └─> IM5 AP/AR (dựng mới — gói riêng, QĐ-ITL-03)
                                                  │
[C Cắt]         IM6 Adjustment + Aggregate ──> IM7 Đối chiếu & Cutover
   tuần tự                                        (engine đọc ITL mới)
```

**Effort `S/M/L` = công tương đối, KHÔNG phải tuần** (tuỳ năng lực đội). `IM1` là mốc chứng minh: đấu engine đọc ITL mới sớm để lộ lệch hợp đồng ngay từ đầu.

## 2. Bảng milestone & cổng

| IM | Effort · dep | Build | Cổng thoát (tiêu chí đo được) | Người nghiệm thu |
|---|---|---|---|---|
| **IM0** Hợp đồng & nền tảng | M · — | `ITL-CONTRACT` (reverse từ reader engine) · `ITL-CANON` 36 cột · target store RAW/ADJUSTED · `MAPPING-MASTER` thành reference data versioned + sign-off · khung DAG/DQ/lineage (stub 1 dòng end-to-end) | Hợp đồng đóng băng **và đã đấu engine đọc thử** (dù subset) · test tương thích engine chạy tự động · stub chạy trọn 1 dòng | COO-CFO + Tech Lead |
| **IM1** Lát dọc mỏng | **L** · IM0 | Adapter **A** (P100: duỗi PE/PI/PM/PC, khớp PM→PI/PE) + **B** (Cash/Bank: 60+ sheet `R \| …`) → S1–S3 → ITL RAW → S5 skeleton (BASE+IMPORT) | Mỗi giao dịch xuất hiện **đúng 1 lần** trong RAW, có ITL id + lineage · **RAW mới khớp `Transaction Mapping L1` cũ theo dòng & tổng** · engine đọc subset chạy không lỗi, CF/P&L subset khớp Gsheet trong dung sai · tỷ lệ `#N/A`/unmatched **được đo & log** | Kế toán trưởng |
| **IM2** Trục dòng tiền + A-CCR | M · IM1 | Adapter **B** đa định dạng (mỗi bank/ví một kiểu) · Adapter **C** A-CCR reconcile tự động thành **DQ gate** ở S2 · khớp cash txn ↔ PM qua reference number, xử interbank | A-CCR balance PASS theo tài khoản/ngày, lệch thì **pipeline dừng & báo** · bảo toàn tiền: tổng vào ITL = tổng statement **net theo tài khoản** · transfer/interbank không đếm 2 lần | Thủ quỹ + Kế toán trưởng |
| **IM3** HR · H1000 | M · IM1 ∥ | Adapter **D** (`1.3 Ledger NISINTCOM/PIT` + `HR Allocate_L500` + `Allocation Driver` + `NOEM PL & COM`) · giữ nguyên allocation HR theo HD/KRF · tự động hoá audit balance HR · ghép `H1000 Ledge` vào S5 | Tổng chi phí HR khớp payroll; phân bổ HD/KRF bảo toàn · **audit balance HR PASS tự động** (2 bước còn `Doing` ở bản cũ) · không dòng lương nào lẫn INS/PIT | HR C&B lead `???` + Kế toán trưởng |
| **IM4** Platform | M · IM1 ∥ | Adapter **E** (`CFA1 Platform Ledger` → `CFA2 MID1/2/3` + `Vendor Mapping`/`Mapping Block`) qua converter định dạng mới · gắn venture/CDT · cô lập nhánh legacy `[FS1]` | Tổng platform khớp nguồn Looker · mapping venture đủ dân số, **không rơi dòng** · không còn phụ thuộc file/nhánh FS1 "ko dùng nữa" | Chủ sở hữu báo cáo platform `???` |
| **IM5** AP/AR (mới) | M · IM1 ∥ | Adapter **F**: AP Ledger (lọc PE, PE&PI chưa PM/PC) + AR Ledger · khử trùng vs `Transaction Original` · audit vs GI & OMC. **Gói riêng, không chặn IM7** (`QĐ-ITL-03`) | Số dư AP/AR khớp đối chiếu · khử trùng với giao dịch tiền **không double-count** · độ phủ accrual đo được (% cam kết chưa thanh toán đã vào sổ) | Kế toán trưởng |
| **IM6** Adjustment + Aggregate | **L** · IM2–IM5 | S5 đầy đủ: union RAW + **bút toán điều chỉnh append-only** (thay ~6.843 dòng nhập tay) + vùng ALLOCATE áp bảng luật (`Need/Method to Allocate to CFA2` + `Code HR`) + vùng AUDIT thành DQ test · **ITL Aggregate quy mô thật** (mắt xích Gsheet đã huỷ) · hoàn thiện lineage | ITL Ledge xuất **đúng 100% `ITL-CONTRACT`** · kết quả rải so được vs vùng ADJUSTMENT/ALLOCATE cũ · Aggregate chạy trọn khối thật, **không timeout/huỷ** · mọi dòng ITL truy được về nguồn | PIC vùng ADJUSTMENT (Lan/Thương) + Kế toán trưởng |
| **IM7** Đối chiếu & Cutover | M · IM6 | Reconcile toàn phần vs Gsheet (dòng + tổng, phân loại lệch thật vs cash-vs-accrual hợp lệ) · **trỏ engine P&L vào ITL mới** · dọn kill-list (Mapping L2, ITL Aggregate cũ, legacy FS1) · bật DAG thay thao tác tay | CF/P&L từ ITL mới **khớp** bản hiện hành; mọi chênh lệch **được giải thích & ký** · engine chạy trên ITL mới ở staging **≥1 kỳ ổn định** · sổ Gsheet chuyển read-only rồi ngưng · thao tác tay chỉ còn nhập liệu & duyệt (maker-checker) | Kế toán trưởng + COO-CFO |

## 3. Thang nghiệm thu bám số thật (áp xuyên các milestone)

Lợi thế lớn nhất của dự án: **`ITL RAW` & `ITL ADJUSTED` cũ vẫn tồn tại** ⇒ đây là **test oracle** sẵn có. 7 bước theo `NGUỒN-BUILD §8`:

| Bước | Làm | IM | Nghiệm thu bằng file thật |
|---|---|---|---|
| 1 | Adapter A + B → S1–S3 | IM1 | ITL RAW mới khớp `Transaction Mapping L1` cũ theo dòng & tổng |
| 2 | A-CCR reconcile (C) làm cổng | IM2 | Balance = `1.2 Ledger 112` / `2.CCR` theo ngày |
| 3 | S5 skeleton + đấu engine đọc thử | IM1→IM2 | Engine chạy; báo cáo subset khớp bản hiện hành |
| 4 | Adapter D (HR) + E (Platform) | IM3, IM4 | Tổng HR khớp payroll; tổng platform khớp Looker |
| 5 | Bảng luật ALLOCATE + ADJUSTMENT append-only | IM6 | So kết quả rải vs vùng ADJUSTMENT/ALLOCATE cũ (~6.843 dòng) |
| 6 | Adapter F (AP/AR mới) | IM5 | Độ phủ accrual; khử trùng không double-count |
| 7 | Reconcile toàn phần → cutover | IM7 | CF/P&L khớp; chênh cash-vs-accrual **giải thích được** |

> **Cấm:** nghiệm thu bằng "chạy không lỗi". Cấm khai tử sổ Gsheet trước khi dùng cạn oracle (`P-ITL-03`).

## 4. Bẫy từng milestone (chép vào agenda gate review)

| IM | Bẫy | Đúng ra |
|---|---|---|
| IM0 | Đóng băng hợp đồng **trên giấy**, chưa đấu engine | Hợp đồng chỉ được frozen sau một lần engine đọc thử thật (`02` §4) |
| IM1 | Khoá ITL/`for_ledger` sai composite | Composite **đúng** — bản cũ từng lệch ~17% khi remap sai. Match-rate LINK là chỉ số nghiệm thu (overlap PE↔txn bản cũ chỉ ~42–46%) |
| IM2 | Ngày chứng từ dạng **text** rơi âm thầm | DQ test parse ngày — bản cũ từng làm ~5.369 dòng rơi `UNMAPPED`. Guard transfer/inflow tránh tràn |
| IM3 | Chi phí HQ giữ được tính nhưng **không trừ PL nào** → EBT khai cao | Kiểu rò HQKEEP đã đo ~1,9 tỷ/năm — đảm bảo mọi khoản HR gánh về đúng PL |
| IM4 | Nguồn đổi định dạng → adapter âm thầm ra 0 dòng | **Fail-loud** khi schema nguồn đổi (đã từng làm 3 sheet ra 0 dòng) |
| IM5 | Code trước khi có nghiệp vụ | Thiết kế nghiệp vụ AP/AR **trước** khi code — phần mới hoàn toàn, dễ trượt nhất (rủi ro #3) |
| IM6 | Đo bảo toàn tiền bằng **cộng dồn cả bảng** → số phồng | Net theo **output-sheet**. Điều chỉnh là journal, **không ghi đè** |
| IM7 | Ép khớp tuyệt đối rồi xoá sổ Gsheet ngay | Chênh cash-vs-accrual giữa kế toán & engine **có thể là ĐÚNG**. Giữ Gsheet read-only để check chéo một thời gian |

## 5. Điều kiện vào đặc biệt

- **Vào IM1 (cứng):** `ITL-CONTRACT` đã đóng băng **và** đã đấu engine đọc thử. Chưa xong → không được code adapter nào. Đây là hàng rào chống rủi ro #1.
- **Vào IM6:** `IM2–IM5` xong hoặc có quyết định owner cho phép bỏ nguồn nào khỏi phạm vi cutover (ghi vào manifest). `IM5` không chặn theo `QĐ-ITL-03`.
- **Vào IM7:** mọi chênh lệch còn lại đã được **phân loại** (lệch thật vs hợp lệ) — không phải đã bằng 0.

## Changelog
- v0.1 (2026-08-18): Khởi tạo — thay `GĐ0–GĐ5` của chương trình bằng `IM0–IM7`; 8 cổng đo được, thang nghiệm thu oracle 7 bước, 8 bẫy có số thật. 2 ô `???` chờ chỉ định người nghiệm thu IM3/IM4.
