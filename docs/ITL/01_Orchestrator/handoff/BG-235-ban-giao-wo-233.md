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

## Sau DT9b *(chỉ THÊM; gộp `isp/DT9B` @ `0b88ca2` + ngọn `claude/bold-galileo-zukpaf` — merge, ⛔ rebase)*
**Trạng thái mới: `CHO_KIEM`** — đầu vào đủ *(`BG-242`: IX.VEN một bảng có cột `so`, 359 dòng; FORMULA `AU`·`S:T`)*. Commit mã `b010054`.

### Mã *(một nguồn sự thật — engine H10, ⛔ chép)*
- `fls/cau_hinh/vendor.py`: `LUAT_SO` *(GI/OMC/SC/PS → `muon_rate` · `pm_tong_thang`, nguồn FORMULA `BG-242 §3`: OMC `S/T` theo `$H` ⇒ ⛔ mượn; SC/PS ⛔ nhánh `O=0∧P>0`)* + `cach_tinh_cua_so(so)`.
- `fls/bao_cao/phan_bo.py` `chia_theo_cach_tinh`: + kw `pm_tong_thang_bat` *(mặc định `True` = H10)* + trường `chia_dong` *(chia TỪNG dòng; gộp lại = `chia` — bài ghim trên GI 408 dòng)*. Grep `VD\d+` ở `fls/bao_cao` = **0** *(AC-5)*.
- `tools/do_hd2.py --goi WP-C4c`: đầu vào **MID1** *(O = Σ`pe` nhóm (vendor,tháng,No) — orchestrator chốt; P = `pm` số chung, cả 7 dòng chữ ⇒ None; PE theo CDT1 = Σ`pe` theo (vendor,tháng), ⛔ SHQ2)* + IX.VEN kho `so=`; so hàng MID3 có khoá ↔ nhóm theo thứ tự × 14 cột. Ô MID3 rỗng *(iferror)* ⇒ 0, ĐẾM.

### WP-C4c *(mẫu số khai TRƯỚC — `MONG_C4C`, nhãn Đ4)*
| Sổ | Vendor-tháng | dòng engine *(so · ngoài ảnh)* | ô so | ô ⛔ so *(P chữ ×7)* | ô ≠ 0 | ô rỗng đáp án | lệch FLS · nguồn *(hàng)* · nghi lỗi |
|---|---|---|---|---|---|---|---|
| OMC | 210 | 890 *(890 · 0)* | **8.547** | 3.913 | 363 | 1.650 | **0** · 52 *(8 = `LAC_OMC`: 7 `VD61` + 1 `VD654`)* · **0** |
| SC | 87 | 741 *(741 · 0)* | **6.230** | 4.144 *(gồm 102 nhóm MID1 chữ ∧ MID3 số)* | 1.216 | 2.575 | **0** · 251 *(69 = mọi hàng khoá của `lac`; 3 hàng tổng ⛔ khoá)* · **0** |
| PS | 477 | 1.215 *(585 · 630)* | **5.117** | 3.073 | **0** ⚠ | 4.386 | **0** · 0 · **0** |
- ⚠ Đ3: PS `o_khac_0 = 0` *(MID1 `pe ≠ 0`: 0/8.505)* ⇒ tập toàn 0 là KẾT QUẢ, ⛔ chứng minh RATE ở PS. 630 nhóm ngoài ảnh: engine ra 0 ở mọi ô *(`ngoai_anh_khac_0` mong 0)*.
- `chua_co_dap_an` *(CÓ TÊN, ⛔ "đạt")*: OMC `202603…202609` · SC/PS `202503` + `202603…202609`.
- Kiểm chéo độc lập: SC 251 = nguyên mẫu §3; `o_so` = 14 × dong_so − 7 × hàng P chữ.
- Khối `hd2_cong.json` `WP-C4c`: **`khop`/`tong_o` = 19.591/19.591** · `o_so` 19.894 · `lech_co_ten` 303 *(NGOÀI `tong_o`, ⛔ trong `khop`)*. ⚠ Nền này ⛔ có ITE ⇒ ⛔ dùng khoá `lech_co_chu_dich` *(hợp đồng cũ đòi `khop == tong_o`)*; khi ITE gộp: đổi sang `tong_o = o_so` + `lech_co_chu_dich = mong = 303`.
- `/gates`: **9 cổng**, `HD2_WP_C4C` = true *("19591/19591 ô")*, `HD2_WP_C4` "3/3 gói con đạt".

### Bài *(TDD — ĐỎ trước)* + cổng
- `tests/oracle/test_do_hd2_c4c.py` **77** bài: mẫu số · Đ5 ±1 trên 10 trường × 3 sổ · 3 lớp lệch *(đổi 1 ô SC ngoài lac ⇒ FLS; OMC ⇒ nghi lỗi; mất cờ ⇒ FLS; bỏ/thêm tên lac ⇒ ĐỎ)* · AC-4 đột biến 1 ô MID1 ⇒ chỉ Vendor-tháng ấy ĐỎ; đổi O MID3 ⇒ chỉ ô O · bật mượn RATE cho OMC ⇒ ĐỎ. ĐỎ trước: 3 failed *(khối tệp chưa ghi · fixture thiếu GI · đột biến rơi vào hàng lac)* ⇒ sửa ⇒ 77 passed.
- `test_isp_gates_hd2.py` cập nhật 8 → 9 cổng; `test_do_hd2_c4b.py` giữ kwarg mới khi monkeypatch `__kwdefaults__`.
- Q8: `MONG_PYTEST_TOAN_BO` **4.059 → 4.136** *(+77)* cùng commit.
- `--duong-nen --cong 5444` *(một lần, một mình)*: **KẾT ĐẠT** — `12 failed · 4108 passed · 2 xfailed · 14 errors` = tập đỏ nền 28 = 28 *(thêm 0 · bớt 0)*, chạy 4.136; web 3 = 3 *(675)*. `lint-imports` 11 kept · 0 broken.

## Vòng sửa sau R1 *(KQ-236 · chỉ THÊM · merge `claude/bold-galileo-zukpaf` vào `isp/H11` @ `a6e09fc`)*
**Gộp:** xung đột `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` ⇒ bản nhánh làm việc, sàn = thu thập thật; `hd2_cong.json` · `do_hd2.py` · `07_API_CONTRACT` tự gộp *(giữ cả hai)*. Mã `7c5c9c3`.

| Mã | Đã làm | ĐỎ trước *(đột biến R1 trên bản sao, ⛔ bài dict `LUAT_SO`)* |
|---|---|---|
| `H11-R1-01` | `tests/bao_cao/test_luat_so_du_lieu_tong_hop.py` **13** bài, dữ liệu tổng hợp tay tính: ca `O=0∧P>0` *(PM `P×S10/O10` = 118,75 · 31,25 ở GI·OMC; `RATE×P` = 112,5 · 37,5 ở SC·PS; ca RATE rỗng: GI·OMC cho qua, SC·PS lỗi có tên)* · ca `VD62` mượn `VD341` *(PE CVL 25 / COR 5 ở GI·SC·PS; 30 / 0 ở OMC — `$H` ⛔ mượn)*. Kỳ vọng GÕ TAY, ⛔ đọc `LUAT_SO`. Mẫu số ca ≠ rỗng có bài ghim *(Đ3)*. | `SC.pm=True` · `PS.pm=True` · `SC.muon=False` · `PS.muon=False` · `OMC.pm=False` · bỏ nhánh `tt` của engine · `doc_ven(so="GI")` ở `chay_wp_c4c` ⇒ **7/7 ĐỎ** *(trước: 5 sống + 2 sống)* |
| `H11-R1-02` | Khối `WP-C4c` theo hợp đồng ITE: `khop` **19.591** *(ô khớp THẬT)* · `tong_o` **19.894** *(= ô so)* · `lech_co_chu_dich` **303** *(52 OMC + 251 SC)* · `mong_lech_co_chu_dich` **303** *(Σ mong lớp nguồn + nghi lỗi, khai trước)* · `o_trong_dap_an` **8.611** *(OMC 1.650 · SC 2.575 · PS 4.386; nằm TRONG `khop`, ⛔ "có số khớp")*. Sinh lại `do_hd2.py --goi WP-C4c --ghi` *(⛔ sửa tay)*. Bài `±1` mong ⇒ ĐỎ hai chiều. | 7 failed trước khi sửa mã |
| `H11-R1-04` | `test_R1_04_duong_doc_kho_cua_CLI…` chạy CHÍNH `chay_wp_c4c(dsn_test())`: `dat` + khối == tệp thật. | *(đột biến `doc_ven(so="GI")` ở trên)* |
| `H11-R1-03` · `DT9B-R1-01/02` | ⇒ **backlog** *(không làm vòng này)*. | |

**`/gates`** `HD2_WP_C4C` = `true` — *"19591/19894 ô đáp án khớp + 303 lệch có chủ đích"*; `HD2_WP_C4` cha `lech_co_chu_dich` = 303. Bài CG2 xanh *(`test_isp_gates_hd2.py` 73)*.
**Q8:** `MONG_PYTEST_TOAN_BO` 4.084 *(nhánh làm việc)* → **4.202** = thu thập thật *(4.084 + DT9b 25 + H11 77 + 16 bài vòng sửa)*; web 675.
**Cổng:** `--duong-nen --cong 5444` *(một lượt dừng giữa chừng vì hết giới hạn nền, ⛔ ĐỎ; chạy lại một lần)*: **ĐẠT** — `12 failed · 4174 passed · 2 xfailed · 14 errors` = nền **28 = 28** *(thêm 0 · bớt 0)*, chạy 4.202; web 3 = 3 *(675)* · `lint-imports` 11 kept · 0 broken · `soi_bang_tuyen` **46** tuyến khớp SQL · `kiem_tai_lieu` ĐẠT.
