# 01 — TESTING FRAMEWORK: FLS

**Version:** v1.0 · **Ngày:** 2026-08-24 · **Chủ sở hữu:** QA
**Thay thế:** v0.1 *(bản copy chương trình)* — đã khai tử.

**Căn cứ:** `11_INVARIANTS` v0.4 · `QĐ-ITL-41` *(4 bất biến `ACC-1…4`, cấm dung sai)* · `QĐ-ITL-36/37` *(oracle)* · `FLS-vs-FPS` §7 *(bài học test của FPS)*.

> ★ Nguyên tắc gốc: **cổng là điều kiện CHẶN, không phải con số để xem** *(`FLS-vs-FPS` §7 mục 3)*. Cổng đỏ ⇒ dừng, không đi tiếp. V0 có `DIF` mà không chặn — đang đỏ −9,53 tỷ mà giai đoạn sau vẫn chạy.

---

## §1 · Bốn cổng CHẶN của FLS — cái nào đo cái gì

| Cổng | Đo | Hạt | Cưỡng chế |
|---|---|---|---|
| **G1 · Hợp đồng** | reader đọc đúng 14 trường theo `ITL-CONTRACT` v1.0 | khoá vị trí | ✅ `test_itl_contract_v1_lock.py` — **đã có, 10 test PASS** |
| **G2 · Tái lập** *(loại A)* | cột **máy tính** khớp ảnh chụp đóng băng | **100% từng ô** — ⛔ cấm ngưỡng | so với oracle `QĐ-ITL-36` |
| **G3 · Dựng lại** *(loại B)* | adapter dựng lại từ nguồn | **`ACC-1…4`** — ⛔ cấm dung sai | 4 bất biến §2 |
| **G4 · Bất biến** | 9 `INV-*` luôn đúng | property-based | Hypothesis + PG container |

★ **G2 và G3 khác nhau về HẠT, giống nhau về LUẬT** *(`QĐ-ITL-41`)*: cả hai **cấm ngưỡng**. Tái lập công thức đạt 100% từng ô; dựng lại từ nguồn không thể đồng nhất từng ô *(thứ tự dòng, `#N/A`, khử trùng, làm tròn khác nhau)* nên đo ở hạt thô hơn **nhưng vẫn chính xác** — chênh **liệt kê từng dòng**, không gộp thành phần trăm.

---

## §2 · `ACC-1…4` CHÍNH LÀ test case — viết được ngay

Bốn bất biến của `QĐ-ITL-41`, mỗi cái là một test chặn:

| Test | Khẳng định | Fail khi |
|---|---|---|
| `test_acc1_count_preserved` | mỗi giao dịch nguồn xuất hiện **đúng 1 lần** trong `fls_itl` | `#dòng nguồn ≠ #staged + #rejected` |
| `test_acc2_money_to_the_dong` | tổng `(tài khoản × ngày)` của FLS **=** tổng của `Transaction Mapping L1` cũ, **đến đồng** | lệch **bất kỳ** đồng nào |
| `test_acc3_keyset_equal` | tập `content_key` của FLS **=** tập của sổ cũ; chênh **in ra từng dòng** | tập lệch |
| `test_acc4_unmatched_named` | mọi `#N/A`/unmatched có **tên nguyên nhân**, không có nhóm "khác" | tồn tại dòng không nhóm |

⛔ **Cấm viết bất kỳ hằng dung sai nào trong 4 test này.** *"Dung sai là chỗ lỗi trốn được"* — một `±0,5%` biến 47 dòng sai thành dấu tích xanh.

---

## §3 · Kim tự tháp

| Tầng | Phạm vi | Công cụ | Cổng CI |
|---|---|---|---|
| Unit | 5 câu `if` của lớp sổ · sinh `itl_id` · `content_key` · parse ngày | pytest | chặn PR |
| Property | 9 `INV-*` — sinh dữ liệu ngẫu nhiên, bất biến phải giữ | Hypothesis | chặn PR |
| Integration | migration · trigger `raw_frozen` · `UNIQUE content_key` · FK `le` — trên **PG container thật** | pytest + testcontainers | chặn PR |
| Contract | G1 — khoá 14 vị trí | pytest | chặn PR, **mọi milestone** *(`INV-I07`)* |
| Parity | G2 + G3 — so với ảnh chụp đóng băng | harness `fls/oracle/` | chặn khi adapter đổi |
| E2E | luồng kế toán trên app *(khi có app)* | Playwright | nightly |

---

## §4 · Năm kỹ thuật bắt buộc *(kế thừa know-how FPS, `FLS-vs-FPS` §7)*

1. **Khoá phải bền + sinh atomic** — test `itl_id`: chạy pipeline **2 lần** → id không đổi; **chèn một dòng ngày cũ** vào nguồn → id các dòng cũ **không đổi**. Đây là oracle của `INV-I04a`.
2. **Không mặc định im lặng** *(`INV-I16`)* — test: dòng thiếu `HDCode` phải ra `work_status='UNMAPPED'` và `hd_thyt IS NULL`, **cấm** ra `OGA | GAC - Other`.
3. **Reject tường minh** — dòng rejected có mặt trong `fls_reject` với **lý do có tên**, không biến mất.
4. **Parity trên cặp** — mọi cột máy tính có ảnh chụp `(đầu vào, đầu ra)` để so; oracle **tự soi** `Final == f(Classifying, U)` trước khi dùng.
5. **State transition** — kỳ `locked` không nhận bút toán *(`INV-I13`)*; `posted` không sửa/xoá *(`INV-I08`)* — mỗi F có test **chặn**.

---

## §5 · Kịch bản độc hại chuẩn — hệ tài chính

| Kịch bản | Kỳ vọng |
|---|---|
| Đọc **bản copy** thay vì file gốc làm oracle | ⛔ oracle **từ chối** — `content_key` khớp nhưng giá trị là mặc định cứng *(bản copy tự sản xuất `OGA/SHQ2/Nợ hoá đơn`, 0 ô lỗi)* ⇒ test tự soi loại chúng |
| Dịch một cột ở nguồn Sheet | dòng **rơi**, đếm được — không đọc lệch im lặng *(đã có test trong G1)* |
| Sửa `doc_date` một dòng cũ | `itl_id` **không đổi**; `content_key` đổi có kiểm soát; nếu suy được thì map cũ→mới, không thì vào hàng chờ `LÝ DO MẤT NEO` |
| Số dư `DIF` đỏ | pipeline **cảnh báo** *(không chặn — `QĐ-ITL-26`)*; nhưng nếu adapter C **không đọc được** kết quả A-CCR ⇒ **chặn** |

---

## §6 · Việc mở

| ID | Việc |
|---|---|
| `GAP-TEST-01` | Ảnh chụp đóng băng làm oracle **chưa đủ 7 khối** *(4/7 đọc được, 3 timeout)* ⇒ G2 chạy được trên phần nào, ghi rõ phần chưa phủ |
| `GAP-TEST-02` | `ACC-2` cần **công thức làm tròn ngoại tệ** của sổ để bắt chước đúng thứ tự — chưa đọc |

---

## Changelog
- **v1.0** (2026-08-24): Viết mới cho FLS. **4 cổng chặn** G1–G4; **`ACC-1…4` thành test case** *(cấm dung sai)*; kim tự tháp gắn với `INV-*` thật; 5 kỹ thuật kế thừa FPS; kịch bản độc hại gồm **bẫy bản copy** và **dịch cột**. G1 **đã có và PASS**.
