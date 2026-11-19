# BG-235 — bàn giao `WO-233` *(ISP 3.1.2 · Step 35 · H11: AL.PLT · OMC · SC · PS — cổng WP-C4c)*

| | |
|---|---|
| **Trạng thái** | `DUNG` — **thiếu đầu vào cho CẢ BA sổ** ⇒ dừng theo luật phiếu *("đầu vào thiếu cho một sổ ⇒ DỪNG báo ảnh cần thêm; ⛔ đoán, ⛔ đọc đáp án thay")* |
| **Phát bởi** | `fls-dev` làn BE-HC *(phiên cloud con)* · 2026-11-19 · nhánh `isp/H11` *(nền `1882adb`)* |
| **Ghi kho thật** | `KHONG` *(cụm PG 5444 chỉ dựng môi trường, ĐẠT)* |
| **Mã đổi** | **0 tệp** — ⛔ engine, ⛔ cổng `WP-C4c`, ⛔ `hd2_cong.json`, ⛔ nâng `MONG_PYTEST_TOAN_BO` |

## 1 · Vì sao dừng — IX.VEN ⛔ phủ vendor của OMC · SC · PS *(đo 19/11, Đ1: đếm cả hai phía)*
Engine H10 `chia_theo_cach_tinh` *(một nguồn sự thật cho H11)* cần IX.VEN cho MỌI vendor: `ma_cach_tinh` → kiểu PE + **vendor cho mượn RATE** *(`F3!AU`)*; vendor ⛔ có ⇒ `LoiPhanBo` có tên. IX.VEN trong repo/kho = **một** bảng `tests/fixture/cau_hinh/ix_ven.json` *(42 dòng — tab `Vendor & Network Mapping` của sổ **GI**)*.

| Sổ | Vendor khác nhau ở MID1 | Có trong IX.VEN | **Thiếu** *(mẫu)* |
|---|---|---|---|
| OMC | 21 | 9 | **12** *(VD0 · VD108 · VD109 · VD110 · VD512 · VD537 · VD56 · VD59 · VD60 · VD654 …)* |
| SC | 10 | 1 | **9** *(VD0 · VD120 · VD17 · VD258 · VD529 · VD54 · VD55 · VD70 · VD717)* |
| PS | 53 | 0 | **53** |

Coi vendor thiếu là `thường` *(⛔ mượn)* = **đoán** ⇒ ⛔ làm. Grep `fls/` + `tools/` + `tests/fixture/`: **0** ảnh VNM của OMC/SC/PS *(chỉ `ix_ven.json` + khuôn `tools/khuon_dong_bang/ix_ven.py`)*; DT9 `BG-221 §4` đọc `FORMULA` **chỉ MID1** *(cột `F,J,K,M,Q,R,S,T,U,V`)* — công thức MID3 `AU`/`S:T` của ba sổ **chưa ai đọc**.

## 2 · Ảnh cần thêm *(đề xuất một bước DATA, khuôn DT8/DT9)*
1. **`ix_ven_{omc,sc,ps}`** — tab `Vendor & Network Mapping` của 3 sổ `[COPY] … Data Ledger` *(id ở `BG-221 §1`)*, cùng 10 cột khuôn `ix_ven` *(gồm `cach_tinh`)*; + quyết định BA: IX.VEN là **một bảng có cột `so`** hay **ba bảng** *(đổi `BangVen`/kho = di trú ⇒ ngoài phạm vi H11, WO-233 cấm di trú)*.
2. **`FORMULA` MID3 cột `AU` + `S:T`** *(khoá RATE + chia)* cả ba sổ — biết có luật mượn RATE kiểu `F3!AU` của GI hay không *(⛔ suy từ đáp án)*.
3. *(nên)* nguồn **O** của MID3: GI lấy từ CFA1 *(`gi_cfa1.json`, PD 504)*; ba sổ ⛔ có ảnh CFA1. Đo dưới cho thấy Σ MID1 `pe` theo (vendor, tháng, No) ≈ O — cần BA xác nhận là nguồn hợp lệ, hoặc thêm ảnh CFA1 ba sổ.

## 3 · Đã đo *(thông tin cho bước sau — ⛔ dùng làm đầu vào; scratchpad, ⛔ commit mã)*
- **Ghép hàng:** MID3 *(hàng có khoá)* ↔ nhóm MID1 (vendor, tháng, No) theo thứ tự: OMC **890 ↔ 890** · SC **741 ↔ 741** · PS **585** hàng ảnh ↔ **1.215** nhóm *(VD0: 79 No/tháng ở MID1, 9 hàng ở ảnh MID3 × 9 tháng ⇒ **630** nhóm rơi vào 1.476 hàng `ngoai_anh` — O rỗng)*. Mỗi nhóm MID1 = **7** CDT1.
- **O = Σ7 CDT1 MID1 `pe`** *(SHQ2 = 0 nên Σ6 = Σ7)*: OMC **882/890** *(8 hàng lệch, đều `VD61` — vd `202503` No1: O 1.296.816,78 ↔ Σpe 1.296.450,94)* · SC **741/741** · PS **585/585**.
- **P = MID1 `pm`** *(một giá trị/nhóm)*: OMC 559/890 · SC 623/741 · PS 439/585 — phần còn lại là `pm_ghi_chu` chữ ⇒ ô ⛔ so được.
- **PE_cdt = RATE(MID1 Σ pe theo vendor-tháng × 6 CDT1, ⛔ mượn) × O** ↔ MID3: OMC **5.340/5.340** khớp *(890 × 6; 0 lệch)* · SC **4.195** khớp · **251** lệch *(VD55 110 · VD17 60 · VD61 55 · VD120 20 · VD529 5 · VD258 1 — gồm vùng `lac` 72 hàng của `BG-221`)* · PS: MID1 `pe ≠ 0` = **0/8.505** ⇒ tập toàn 0 *(Đ3 — KẾT QUẢ, ⛔ nền)*.
- **Tháng:** OMC `202503…202512` (10) · SC `202504…202512` (9) · PS `202504…202512` (9); `202603…202609` = 0 dòng ở cả ba ⇒ khi chạy cổng sẽ là `chua_co_dap_an` CÓ TÊN *(theo `WO-233` "Đã đo")*.

## 4 · Cổng
- Dựng môi trường `--cong 5444`: **KẾT ĐẠT** *(27/27 di trú · lint 11 kept · kho rỗng)*.
- ⛔ chạy `--duong-nen` / `pytest` toàn bộ: **0** tệp mã đổi ⇒ tập đỏ = nền; sàn `MONG_PYTEST_TOAN_BO` **giữ nguyên**.
- `kiem_tai_lieu.py`: **ĐẠT** *(373 tệp · 2.707 bảng)*.

## 5 · Việc kế
Orchestrator/BA: phát bước DATA cho §2.1–2.2 *(+ §2.3 nếu cần)*; mở lại `WO-233` khi có ảnh. Dự kiến engine **⛔ đổi** *(OMC khớp 0 lệch không cần nhánh mới)*; tham số hoá chỉ ở tầng gọi *(nguồn PE = MID1 theo (vendor, tháng, No); IX.VEN theo sổ)*.
