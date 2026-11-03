# 02 — VERSION ORCHESTRATION: trục version của dự án ITL

**Version:** v0.2 | **Chủ sở hữu:** COO-CFO

Khác chương trình FIN ERP: ở đó trục version là "3 kit khớp nhau". Ở ITL, **trục version là 3 hợp đồng dữ liệu** — vì thứ có thể làm gãy dự án không phải doc lệch doc, mà là **schema lệch schema** (rủi ro #1).

---

## 1. Ba hợp đồng được version hoá (trục chính)

| Hợp đồng | Là gì | Nguồn sự thật | Ai đổi được |
|---|---|---|---|
| **`ITL-CONTRACT`** | Tập cột + kiểu + ngữ nghĩa + khoá mà **engine P&L đọc** từ `ITL Ledge`. Reverse-engineer từ reader đang chạy thật (`P-ITL-01`). Phạm vi = **13 trường**: A–F + R + V/Z/AD/AH/AL (`Final` vùng ADJUSTMENT khối 1–5) + BL (vùng AUDIT). ⭐ **v1.0 khai báo theo TÊN** — đọc-theo-vị-trí chỉ còn là **tầng tương thích** trong lúc nguồn còn là Sheet (`INV-I07`, `POS-13`) | `BA-05` §Output Contract | Chỉ qua CR loại 3 (`07`) + test tương thích engine |
| **`ITL-CANON`** | Khuôn giao dịch chuẩn 36 cột (`Transaction Mapping L1`), 5 nhóm BASE(7)/LINK/CLASS/SVC/PARTY. Mọi adapter xuất đúng khuôn này | `BA-05` §Canonical Schema | CR loại 3 |
| **`MAPPING-MASTER`** | Reference data lái chuẩn hoá & phân bổ: khoá nhận diện tài khoản/sheet, chuẩn hoá LE, COA1/COA2, 3 cột `Need to Allocate to CFA2` / `Method to Allocate to CFA2` / `Code HR Allocate` | Bảng trong hệ thống (không phải file doc) | Người nghiệp vụ qua UI + sign-off (`P-05`) |

**Luật vàng:** `MAPPING-MASTER` là **dữ liệu có version trong hệ thống**, KHÔNG version hoá bằng file doc. Doc chỉ mô tả *cấu trúc* của nó. Đổi một dòng mapping ⇒ tạo version mới của bảng, không sửa doc, không sửa code (`P-05`).

## 2. Ba trục phụ

| Trục | Quy ước |
|---|---|
| **Adapter A–F** | Mỗi adapter có version riêng `adapter-<X>-v<n>`; bump khi schema nguồn đổi. Adapter phải khai báo nó xuất theo `ITL-CANON` version nào |
| **File kit** | `v0.x` khi còn GAP mở → `v1.0-frozen` khi đóng băng (chỉ con người đổi tiếp) |
| **Run/snapshot** | Mỗi lần chạy pipeline giữ snapshot + version của cả 3 hợp đồng đang hiệu lực ⇒ tái hiện được kết quả cũ |

## 3. Ma trận khớp version hiện tại

| Thành phần | Version | Ghi chú |
|---|---|---|
| `ITL-CONTRACT` | **v1.0 — ĐÓNG BĂNG** *(`QĐ-ITL-42`, 2026-08-24)* | ✅ Reverse-engineer từ reader đang chạy (`itl_ledge_reader.py::_COLS`), khớp 13/13 dữ liệu thật — `BA-05` §`DD-I04b`. **14 trường** *(sửa chiều 24/08: `le` = `P`(15) không phải `BL`(63); thêm `acct` = `G`(6))*, khai báo **theo TÊN**; bảng map `tên → vị trí` giữ lại làm **tầng tương thích** cho tới khi reader đổi xong. ⛔ **Khối ADJUSTMENT 6–7 (`AP` Mã đối tác · `AT` File đính kèm) NGOÀI hợp đồng** ⇒ sang gói adapter F (`QĐ-ITL-03`: không chặn cutover). ✅ **Điều kiện đóng băng ĐÃ ĐẠT 2026-08-24**: `test_itl_contract_v1_lock.py` (10 test PASS) + `test_itl_le_column_ssot.py` (4 test) |
| `ITL-CANON` | **v0-discovered** | 36 cột đã đọc được từ sheet thật; chưa viết thành spec có version (`BA-05`, sóng S2) |
| `MAPPING-MASTER` | **v0-asis** | Đang là sheet trong `ITL RAW`, chưa có versioning/sign-off |
| Kit Orchestrator (bộ này) | v0.1 | Đang viết (sóng S1) |
| Kit BA | v0.1 (bản copy) | Chưa dẫn xuất — sóng S2–S3 |
| Kit Dev / Test | v0.1 (bản copy) | HOLD tới sau `G-DOC-3` |
| Chốt kế thừa chương trình | 6 khối, xem `../00_MASTER_INDEX §5` | Rà nhịp nào = `GAP-ITL-08` |

## 4. Giao thức đóng băng

1. Kit owner đề xuất frozen → liệt kê GAP còn mở kèm lý do chấp nhận.
2. Orchestrator duyệt tại value review tháng gần nhất.
3. Từ lúc frozen: mọi thay đổi đi qua `07_CHANGE_CONTROL`, tăng minor version, ghi changelog.

**Riêng `ITL-CONTRACT` có thêm 2 điều kiện đóng băng:**
- ✅ **Chứng minh bằng đấu engine đọc thử** — *đạt bằng cách mạnh hơn:* đọc thẳng mã reader đang chạy production, không phải chạy thử.
- ⬜ **Test tương thích chạy tự động** — **CHƯA CÓ**, là việc còn lại duy nhất trước khi frozen.

⚠ **Điều kiện đóng băng thứ 3 (mới):** reader đọc **theo vị trí cột cứng**, nên hợp đồng phải kèm **test khoá vị trí** cho cả 13 cột. Chèn/xoá một cột ở vị trí ≤ BL làm engine đọc lệch âm thầm — xem `BA-05` §`DD-I04b`.

## 5. Manifest mỗi milestone (mẫu)

```
MILESTONE IM<n> — <ngày>
Nguồn được thêm: <adapter> · Bước lắp ráp: <S1..S5>
Mắt xích Gsheet bị cắt: <danh sách> · Dòng nhập tay bị khai tử: <số>
ITL-CONTRACT: v_ · ITL-CANON: v_ · MAPPING-MASTER: v_
Adapter version: A v_ , B v_ , ...
Đối soát oracle: <khớp / chênh + lý do đã ký>
Người vận hành nghiệm thu: <tên + vai> · Ký: <ngày>
```

## 6. Chốt kế thừa từ chương trình

Bộ ITL độc lập (`QĐ-ITL-04`) ⇒ 6 khối nội dung tồn tại 2 bản. Bảng ghim version ở `../00_MASTER_INDEX.md` §5 là **cơ chế phát hiện trôi duy nhất**. Trách nhiệm rà: `???` — chờ owner chốt (`GAP-ITL-08`); đề xuất: COO-CFO rà tại value review tháng.

## Changelog
- v0.2 (2026-08-18): `ITL-CONTRACT` lên **v1.0-candidate** (reverse-engineer từ reader thật, khớp 13/13). Thêm điều kiện đóng băng thứ 3: test khoá vị trí cột.
- v0.1 (2026-08-18): Khởi tạo — đổi trục version từ "3 kit khớp nhau" (chương trình) sang **3 hợp đồng dữ liệu**; thêm 2 điều kiện đóng băng riêng cho `ITL-CONTRACT`; manifest theo milestone.
