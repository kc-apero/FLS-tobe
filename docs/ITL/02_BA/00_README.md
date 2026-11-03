# 00 — README: BA Kit ITL (AI-first)

**Dự án:** ITL — Input Transaction Ledger | **Phiên bản bộ:** v0.1 | **Chủ sở hữu (BA/PO):** COO-CFO

Bộ spec nghiệp vụ của dự án ITL, tối ưu cho AI đọc và thực thi: **mọi tài liệu ở dạng bảng có ID + version**. Nguồn nghiệp vụ gốc là 6 tài liệu lớp nguồn (xem `../00_MASTER_INDEX.md` §6) — bộ này *cấu trúc hoá* chúng thành spec thực thi được, không thay thế chúng.

---

## 1. Cấu trúc bộ (**14 file** + `Artifacts/`, 4 lớp)

> ⚠ **SỬA 17/09:** tiêu đề cũ ghi *"12 file"* — đếm thật trong thư mục là **14** tệp đánh số `00`…`13` *(cộng `_BA_UPDATE_ROADMAP.md` và thư mục `Artifacts/`)*. `12_BA_MAN_GHEP_PM` và `13_THUYET_MINH_MAN_HINH` thêm sau khi tiêu đề này được viết, và ⛔ không ai sửa con số.

### Lớp 1 — Bối cảnh nghiệp vụ
| File | Vai trò | Độ chín |
|---|---|---|
| `01_BRD.md` | Bài toán 3 con số, 7 khối nhập tay, goal, phạm vi, KPI | ● nội dung thật |
| `02_PROCESS_FLOW.md` | AS-IS 6 pha → TO-BE 5 tầng, dây chuyền S1–S5, chu trình vận hành | ● nội dung thật |

### Lớp 2 — Yêu cầu chức năng
| File | Vai trò | Độ chín |
|---|---|---|
| `03_USER_STORY.md` | Epic theo adapter/vùng; story chi tiết chỉ `IM0–IM2` (JIT) | ⏳ sóng S3 |
| `Artifacts/UC-US-Ke-toan-PM-den-ITL.md` **v0.3** | **22 UC · 45 US của đội kế toán** trong luồng `PM → ITL`; **3 vai người + 1 vai MÁY** *(v0.1 dựng 8 vai — hư cấu)*; trạng thái ●/◐/○ | ● nội dung thật |
| `Artifacts/Process-PM-den-ITL.md` **v1.5** | ⭐ **SSOT của luồng `PM → ITL`** — 5 giai đoạn / 10 chặng · 28 khoá nối · 36 chỗ gãy · công thức nguyên văn đọc live | ● đọc từ sổ sống |
| `Artifacts/Lo-trinh-Chuyen-doi-Gsheet-to-UI.md` **v0.2** | **§0b ranh giới Google Sheets ↔ Hệ thống** *(chặng 1 không có giao diện mới nào; 4 nhóm ở lại Sheets vĩnh viễn)* · 4 pha · **4 màn hình** *(không phải 7)* | ● nội dung thật |
| `04_ROLE_PERMISSION_MATRIX.md` | 10 vai, ma trận 16 hành động, 3 ràng buộc SoD | ● nội dung thật |

### Lớp 3 — Đặc tả chi tiết
| File | Vai trò | Độ chín |
|---|---|---|
| `05_DATA_DICTIONARY_ERD.md` | **File lõi** — 36 cột canonical, `ITL Ledge` 4 vùng, `MAPPING-MASTER`, schema 8 nguồn | ● đọc từ file thật |
| `06_SCREEN_SPEC.md` | 4 màn hình lõi | ⏳ sóng S3 |
| `07_API_CONTRACT.md` | Quy ước + endpoint `IM0–IM2` | ⏳ sóng S3 |

### Lớp 4 — Ràng buộc & quy tắc lõi
| File | Vai trò | Độ chín |
|---|---|---|
| `08_NFR.md` | Khối lượng thật, thời gian chạy, idempotency, cửa sổ reprocess | ⏳ sóng S3 |
| `09_STATE_MACHINE_SPEC.md` | 5 máy trạng thái | ● nội dung thật |
| `10_DECISION_TABLE.md` | 9 bảng quyết định + thứ tự áp bắt buộc | ● nội dung thật |
| `11_INVARIANTS.md` | 14 bất biến, mỗi cái có tầng enforce | ● nội dung thật |
| `12_BA_MAN_GHEP_PM.md` | BA lại màn ghép `PM ↔ Giao dịch` — lộ trình `G1…G5`, **đã xong** | ● nội dung thật |
| ⭐ `13_THUYET_MINH_MAN_HINH.md` | **Từng nút, từng ô, và `US` nào đứng sau** — đọc từ **mã đang chạy**, ⛔ không từ đặc tả. Có cổng `tools/kiem_thuyet_minh.py` canh: thêm một nút mà ⛔ không giải thích ⇒ **⛔ không qua** | ● nội dung thật |

## 2. Chuỗi truy vết

```
Bài toán ITL → IM (milestone) → Adapter/Zone → US-8xx → Spec (SM/DT/INV/RP/DD/SCR/API) → Code → TC
```

Mỗi story phải trace về **một milestone** và **một adapter hoặc một vùng** của `ITL Ledge`. Không trace được = việc thừa.

## 3. Thứ tự soạn thảo (đã áp dụng ở sóng S2)

1. `01`+`02` chốt bài toán → 2. `09`+`11` mô hình hoá entity trung tâm → 3. `10`+`04` quy tắc + quyền → 4. `05` data dictionary → 5. `03`+`06`+`07` theo epic (JIT từng IM) → 6. `08` NFR → 7. bàn giao Testing Kit.

## 4. Quy tắc bất di bất dịch

`R-A1..R-A5` — xem `../00_MASTER_INDEX.md` §7. Riêng bộ này nhấn hai điều:

- **R-A2 tuyệt đối ở `05`:** tên trường chép **nguyên văn từ file thật**, kể cả lỗi chính tả của nguồn (`ENITY`, `filetring`, `(yyyymm` thiếu ngoặc) và các tên trùng nhau. Đổi tên là việc của `ITL-CONTRACT` qua CR loại 3.
- **R-A1:** 7 ô `???` đang mở trong bộ này, mỗi ô có owner + GAP id.

**Prefix ID** (`QĐ-ITL-01`): `US-8xx` · `SCR-I0x` · `DD-Ix` · `DT-Ixx` · `INV-Ixx` · `RP-Ix` · `API-Ix` · `NFR-Ix` · `GAP-ITL-xx`.

## Changelog
- v0.1 (2026-08-18): Khởi tạo cho ITL — 7/12 file có nội dung thật (sóng S2); 5 file còn lại JIT ở sóng S3.
