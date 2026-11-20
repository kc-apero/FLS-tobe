# BG-242 — bàn giao `WO-241` *(ISP 3.1.2 · DT9b: IX.VEN thêm cột `so` + vendor OMC · SC · PS — đầu vào cho WP-C4c của H11)*

| | |
|---|---|
| **Trạng thái** | `CHO_KIEM` — Dev xong 19/11 · nhánh `isp/DT9B` *(nền `06db9f9`)* · chưa R1 |
| **Phát bởi** | `fls-dev` làn DATA *(phiên cloud con)* |
| **Ghi kho thật** | `KHONG` *(cụm PG 5445 chỉ chạy đường nền / bài `pg` trên `fls_test`)* |
| **Mã H11** | **0 tệp** *(⛔ `fls/bao_cao/*`, ⛔ `hd2_cong.json`)*; ⛔ di trú mới |

## 1 · Ảnh `ix_ven.json` — MỘT bảng có cột `so` *(AC-1)*
Nguồn *(khoá SA chỉ-đọc, 19/11; bản thô `/tmp` chmod 600 đã xoá, ⛔ commit)*: GI giữ nguyên · OMC `Vendor & Channel Mapping` **R4:X92** · SC `Vendor & Network Mapping` **N4:T96** · PS `Vendor & Network Mapping` **M4:S138** — Block 1 liền từ hàng 4, ô vendor tiếp theo rỗng.

| `so` | DÒNG *(đếm dòng ảnh — Đ4)* | VENDOR khác nhau | Phủ MID3 *(vendor MID3 có dòng / vendor MID3)* | `cach_tinh` |
|---|---|---|---|---|
| GI | **42** *(từng byte như cũ, chỉ thêm `so`)* | 19 | — *(DT8)* | Max 12 · VD341 12 · VD444 8 · VD428 3 · VD62 1 · thường 6 |
| OMC | **89** | **21** | **21/21** | VD341 3 · VD62 2 · VD428 2 · thường 82 |
| SC | **93** | **10** | **10/10** | thường 93 |
| PS | **135** | **53** | **53/53** | thường 135 |
| Σ | **359** | | | cổng `--mong 359` ĐẠT *(khoá hỏng 0 · trùng 0 · thiếu 0 · ô rỗng 0/2154)* |

- `cach_tinh` = **cùng luật suy của DT8/C9** *(network `Max` ⇒ `Max`; vendor ∈ {VD341,VD428,VD444,VD62} ⇒ chính mã; còn lại `thường`)* — ⛔ ba sổ mới ⛔ có cột 'cách tính' trong sheet. 5 nhãn riêng cả bảng = `{Max,VD341,VD428,VD444,VD62}` *(Đ5 hai chiều)*.
- Khoá kho `dong_sheet`: GI = số hàng *(NGUYÊN)*; OMC/SC/PS = `<SO>!<hàng>` *(số hàng sheet trùng giữa các sổ)*. Khoá nghiệp vụ `(so, vendor, No)` duy nhất. Checksum ảnh `77f81455901c3667` → **`0f2d9287d332d698`** *(ĐỔI CÓ CHỦ ĐÍCH: thêm cột + 317 dòng)*; 42 dòng GI ghim sha `eb2b497da051e6f9` *(JSON chuẩn, ⛔ cột `so`)*.
- **PII:** cột `vendor` chỉ mã `VD<số>` *(khuôn TỪ CHỐI tên, ⛔ in giá trị ô)*. ⛔ đọc `account` ở OMC/SC/PS *(OMC `U` · SC `Q` · PS `P` — cột KHÔNG tiêu đề; PS `P` = `COUNTIF(N:N,N4)`; không xác định được cột có tên/số TK ⇒ không đọc)* ⇒ `null`. ⛔ đọc `network` ở SC/PS *(cột `P` SC = ghép Provider+tên đơn vị · cột `O` PS = tên vendor; không có tiêu đề)* ⇒ `null`; OMC `network` = cột `channel` *(14 tên kênh, không PII)*. `pct` · `cashin_month` · `cashin_day` *(số cấu hình, không PII)* đọc vì `vendor.kiem` bắt buộc. `tools/quet_pii_repo.py`: **không có** trong cây này *(Đ1: 0 tệp)* ⇒ AC-4 chỉ bằng bài.
- ⚠ `network` OMC `VD428` (2 dòng) **rỗng** ⇒ `_pe_mang_dong_no` *(`mang_dong_no`)* sẽ ra PE 0 nếu H11 gọi cho OMC — việc H11 quyết, DT9b ⛔ đoán.

## 2 · Mã *(AC-2)*
- `vendor.py`: `DongVen.so` *(mặc định `GI` — bản kho DT8 cũ vẫn đọc)* · `SO_HOP_LE` · khoá `(so,vendor,No)` · `BangVen.theo_so()` *(sổ lạ/0 dòng ⇒ `LoiVen`, Đ3)* · `cashin_month` nhận **0…12** *(SC `VD529`: cùng tháng `0`, ngày `2` — đo 19/11; trước là 1…12)*.
- `cau_hinh_repo`: `nap_ix_ven` đọc `so`; `doc_ven(conn, so=None)` *(`None` = cả 4 sổ; `so="GI"` = engine H9/H10 — `do_hd2.py` + 3 bài oracle/phan_bo gọi `so="GI"` ⇒ WP-C4a/C4b ra đúng số cũ)*.
- `/config/ven`: **chỉ THÊM** trường `so` mỗi dòng; `so_dong` 42 → **359**. `soi_bang_tuyen.py`: ĐẠT *(46 tuyến)*.
- Công cụ chung `tools/dong_bang_sheet.py` **ĐỔI** *(khai)*: thêm kiểu khoá `so_dong_sheet`; sha ghim `ae917adbf80b1c14` → `2d8c1724f8403608` ở `test_dap_an_atl.py` *(kiểu khoá cũ ⛔ đổi nhánh)*.
- Bài mới: `tests/du_lieu/test_ix_ven_da_so.py` **14** · `test_vendor.py` **+9** · `test_vendor_pg.py` **+2**. **ĐỎ trước** *(ảnh · khuôn · `vendor.py` chưa có)*: `test_ix_ven_da_so.py` và `test_vendor.py` bài `DT9b_*` đỏ; sau mã: xanh. Phá *(đều ĐỎ)*: bỏ một dòng OMC · vendor là tên người *(không in giá trị)* · `so` lạ · mất nhãn `VD341`.
- Q8: `MONG_PYTEST_TOAN_BO` **4034 → 4059** *(= số thu thập; web giữ 675)* + bài ghim cùng commit.

## 3 · `FORMULA` MID3 — `AU` · `S:T` *(AC-3; đọc nguyên văn 19/11, hàng 10…; đếm theo hàng KHOÁ = hàng có `H` = `VD…`)*
Tab `CFA2 | MID 3 | … Platform Data Ledger`. Hàng khoá: **OMC 890 · SC 741 · PS 983** *(PS: 585 hàng trong ảnh + hàng ngoài ảnh)*. `AU11` mọi sổ **y hệt**: `=if(H11<>"VD62",H11,VLOOKUP(AQ11,AR11:AT12,3,FALSE))` *(mini-bảng `AQ:AT` hàng 11–12: `AT11 =if(AS11>AS12,"VD341","VD62")`)* — đúng luật mượn RATE của GI.

| Sổ | `AU` trên hàng khoá | `S` *(PE_CDT1 đầu)* | `T` *(PM)* | Tiêu chí vendor ở `SUMIFS` |
|---|---|---|---|---|
| **OMC** | **21** CT · 869 rỗng *(chỉ mini-bảng, ⛔ theo hàng)* | **890/890** CT, 1 mẫu | **890/890** CT, 1 mẫu | **`$H`** *(vendor thật)* ⇒ **⛔ mượn RATE** dù có 20 hàng `VD62` + 30 hàng `VD341` |
| **SC** | **549** CT · 192 rỗng | **550** CT *(549 mẫu `$AU` + 1 hàng tổng-tháng `=sum(S506:S566)` ở hàng 505)* · 191 rỗng | như `S` | **`$AU`** *(mượn RATE qua `AU`)*; **0** hàng `VD62`/`VD341` ⇒ `AU ≡ H`, mượn **vô hiệu** |
| **PS** | **983/983** CT | **983/983** CT, 1 mẫu | **983/983** CT, 1 mẫu | **`$AU`**; **0** hàng `VD62`/`VD341` ⇒ vô hiệu |

Mẫu nguyên văn *(hàng 11; `AA` = RATE ở `CFA2 | MID2`)*:
- OMC `S11`: `=iferror(SUMIFS('CFA2 | MID2 | OMC Allocated Ledger'!$AA:$AA,'…'!$K:$K,$F11,'…'!$J:$J,S$7,'…'!$M:$M,$H11)*$O11)`
- OMC `T11`: `=iferror(if(and($O11=0,$P11>0),$P11*S10/O10,SUMIFS('CFA2 | MID2 | OMC Allocated Ledger'!$AA:$AA,'…'!$K:$K,$F11,'…'!$J:$J,T$7,'…'!$M:$M,$H11)*$P11))` — có nhánh `O=0 ∧ P>0 ⇒ P×S10/O10` *(= `pm_tong_thang` của H10)*.
- SC · PS `S11`: `=iferror(sumifs('CFA2 | MID 2 | <SC|PS> Allocated Ledger'!$AA:$AA,'…'!$M:$M,$AU11,'…'!$K:$K,$F11,'…'!$J:$J,S$7)*$O11)`; `T11` cùng dạng `*$P11`, **⛔ có** nhánh `O=0 ∧ P>0`.
- Hàng tổng-tháng: `=sum(S11:S99)` *(OMC 10 · SC 10 · PS 8)*.
- ⚠ **Hệ quả cho H11:** luật `VD62` mượn RATE `VD341` của GI **⛔ áp ở OMC** theo công thức *(OMC dùng `$H`)*; ở SC/PS luật có mặt nhưng **không có hàng** nào kích hoạt. Đo **công thức**, ⛔ so đáp án.

## 4 · Nguồn **O** *(AC-3 — ⛔ đổi nguồn O)*
MID3 `O` = **`CFA1!F`** *(`O11 ='CFA1 | … Platform Data Ledger'!F10`; `P ← S`, `F ← K`, `H ← M`)* — cả ba sổ **có tab CFA1** *(OMC 899×63 · SC 760×63 · PS 1224×63)*, không phải chỉ GI. Đối chiếu *(đọc `M,K,Q,F`; ⛔ A:C · G · N:O; **ảnh CFA1 chưa đóng băng** — ⛔ quyết mới)*:
| Sổ | `CFA1.F` = `O` MID3 *(theo thứ tự trong vendor-tháng)* | `CFA1.F` = Σ`pe` MID1 theo (vendor,tháng,No) |
|---|---|---|
| OMC | **890/890** | **882/890** — 8 lệch |
| SC | **741/741** | **741/741** |
| PS | **585/585** | **585/1.215**; 630 còn lại = `CFA1.F` **rỗng** ∧ Σ`pe` = 0 *(0/1.215 nhóm có Σ≠0 ngoài 585 — Đ3: tập toàn 0)* |
⇒ Nguồn O của H11 *(Σ`pe` MID1)* khớp `CFA1.F` y như đã đo ở BG-235; chênh chỉ ở 8 hàng OMC dưới.

**8 hàng OMC lệch** *(MID3 `dong_sheet` · vendor · tháng · No1 · `O`=CFA1.F ↔ Σ`pe` MID1)* — ⚠ **không phải cả 8 là `VD61`: 7 `VD61` + 1 `VD654`** *(Đ1)*:
`14` VD61 202503 · 1.296.816,78 ↔ 1.296.450,94 · `104` VD61 202504 · 1.315.319,86 ↔ 1.314.083,96 · `194` VD61 202505 · 933.548,25 ↔ 933.546,91 · `284` VD61 202506 · 809.920,98 ↔ 809.439,96 · `374` VD61 202507 · 861.156,62 ↔ 860.508,44 · `380` **VD654** 202507 · 3.185.863,78 ↔ 3.185.572,18 · `464` VD61 202508 · 546.849,12 ↔ 545.666,06 · `644` VD61 202510 · 357.441,08 ↔ 357.374,15.
Khai `lac` CÓ TÊN *(8 `dong_sheet`: 14·104·194·284·374·380·464·644)* — ⛔ lấp; gốc lệch *(MID1 `pe` ≠ CFA1 `F`)* ⛔ truy được từ SA.

## 5 · Không làm
⛔ ảnh CFA1 ba sổ *(chờ quyết)* · ⛔ sửa `fls/bao_cao` · ⛔ đổi `hd2_cong.json` · ⛔ di trú · ⛔ ghi kho thật.

## 6 · Cổng cuối
`--duong-nen --cong 5445` *(một lần, một mình)*: **KẾT ĐẠT** — toàn bộ `12 failed · 4031 passed · 2 xfailed · 14 errors` = tập đỏ nền 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **4059** bài; `tests/web` `3 failed · 672 passed` = nền 3 = 3 *(675)* · `lint-imports` 11 kept · `kiem_tai_lieu.py` ĐẠT · `soi_bang_tuyen.py` ĐẠT.
