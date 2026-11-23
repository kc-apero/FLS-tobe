# BG-217 — bàn giao `WO-216` *(H10 · AL.PLT · 5 vendor đặc biệt theo mã 'cách tính' — cổng WP-C4b)*

| | |
|---|---|
| **Thuộc** | `WO-216` (ISP 3.1.2 · Step 28 · H10) |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · 2026-11-19 · cụm PG 5444 |
| **Nhận** | `fls-test` R1 `KQ-218` → R2 `KQ-219` |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/H10` *(nền `617992c`)* — ① mã + bài · ② BG này |
| **Ghi kho THẬT** | `KHONG` *(Sheets đọc bằng khoá SA chỉ-đọc `FORMULA`; bản thô ở `/tmp`, ⛔ commit; ⛔ đọc cột PII `A:C · G · N:O`)* |

## Kết luận
**AC-1 … AC-7 xong. WP-C4b `DAT`** — lần ĐẦU RATE được chứng minh trên số thật: **988** ô ≠ 0 *(tập KHÔNG rỗng, Đ3)*, lệch **0**, vendor bỏ qua **0**.
⭐ Phát hiện chính: phép tính riêng của 5 mã nằm ở **hai tầng** — **PE theo CDT1 từ Looker** *(MID1/CFA1 cột `E` — 4 kiểu hàm)* và **khoá RATE ở `[Formula] MID3` cột `AU`** *(chỉ mã `VD62` — mượn RATE `VD341`)*. Vendor `thường` có PE = 0 **vì công thức** *(nhánh cuối `…,0)`)* — đó là gốc của "44/44 Vendor-tháng thường toàn 0" *(BG-205)*.

## Nguồn PE theo CDT1 *(theo "orchestrator chốt" ①)* + bằng chứng ⛔ vòng tròn
- Đầu vào = ảnh **MID1** `tests/fixture/dap_an/gi_mid1.json` cột `pe` *(= sheet `T` = `ArrayFormula(iferror(E10:E,"Need to manual input"))`)*, gộp mọi No theo `(vendor, tháng, CDT1)` = đúng `M2!E = SUMIFS(MID1!E; M; K; J)`.
- ⛔ vòng tròn — **đo bằng `FORMULA`** 19/11: `MID1!E` chỉ tham chiếu `'Source (Looker)'` + `'Vendor & Network Mapping'` *(công thức dưới)* — **0** tham chiếu MID2/MID3. RATE tính LẠI từ MID1 *(⛔ đọc `M2!AA`)*; MID3 chỉ là đáp án.
- ⛔ đủ ⇒ DỪNG *(②)*: **không xảy ra** — MID1 mang đủ 6 CDT1 × 209 Vendor-tháng. `pe` rỗng *(`iferror` rỗng ⇒ SUMIFS = 0)*: **77** dòng *(66 ở 6 CDT1 + 11 ở SHQ2)* — ĐẾM ở `mid1_pe_rong`.
- Bài **AC-6**: nhân 3 một ô `pe` MID1 *(CVL của Vendor-tháng đặc biệt đầu tiên có O ≠ 0)* ⇒ lệch **chỉ** ở các ô `*_pe` của đúng Vendor-tháng ấy; xoá trắng đáp án MID3 ⇒ engine y nguyên *(988 ô lệch = đúng 988 ô ≠ 0)*.

## Công thức AS-IS nguyên văn *(sổ `[COPY] GI Platform Data Ledger`, đọc `FORMULA` 19/11)*
Viết tắt: `L` = `'Source (Looker)'` · `VNM` = `'Vendor & Network Mapping'` · `M2` = `'CFA2 | MID 2 | GI Allocated Ledger'` · `F3` = `'[Formula] CFA2 | MID 3 | GI Platform Data Ledger'`.

**① PE theo CDT1 — `MID1!E10`** *(CFA1 `E10` giống hệt, ⛔ có `L!S:S,J10`, VNM `$N$4:$O$39`)*:
```
=iferror(if(or(M10="VD444",M10="VD341"),SUMIFS('Source (Looker)'!$K:$K,'Source (Looker)'!$I:$I,VLOOKUP($M10,{'Vendor & Network Mapping'!$N$4:$N$35,'Vendor & Network Mapping'!$O$4:$O$35},2,FALSE),'Source (Looker)'!$Q:$Q,$Q10,'Source (Looker)'!$O:$O,$K10,'Source (Looker)'!S:S,J10),if(and(VLOOKUP(M10,{'Vendor & Network Mapping'!$N$4:$N$35,'Vendor & Network Mapping'!$O$4:$O$35},2,FALSE)="Max",Q10=1),sumifs('Source (Looker)'!$K:$K,'Source (Looker)'!$I:$I,VLOOKUP(M10,{'Vendor & Network Mapping'!$N$4:$N$35,'Vendor & Network Mapping'!$O$4:$O$35},2,FALSE),'Source (Looker)'!O:O,K10,'Source (Looker)'!S:S,J10)*VLOOKUP(M10,{'Vendor & Network Mapping'!$N$4:$N$35,'Vendor & Network Mapping'!$Q$4:$Q$35},2,FALSE),if(and(M10="VD428",Q10=1),SUMIFS('Source (Looker)'!$K:$K,'Source (Looker)'!$I:$I,"Apple_store",'Source (Looker)'!$O:$O,K10,'Source (Looker)'!S:S,J10),if(and(M10="VD428",Q10=2),SUMIFS('Source (Looker)'!$K:$K,'Source (Looker)'!$I:$I,"IAP_tracking",'Source (Looker)'!$O:$O,K10,'Source (Looker)'!S:S,J10),0)))))
```
**② RATE — `M2!AA11`** `=T11/sum(T11:T16)` *(6 CDT1, hàng SHQ2 = đầu khối ⛔ vào)*.
**③ Chia — `F3!S11` (PE) · `F3!T11` (PM)** *(một hàng = một dòng CFA1; `O = C1!E`, `P = C1!S`, `L = C1!Q`)*:
```
=iferror(sumifs(M2!$AA:$AA,M2!$M:$M,$AU11,M2!$K:$K,$F11,M2!$J:$J,S$7)*$O11)
=iferror(if(and($O11=0,$P11>0),$P11*S10/O10, sumifs(M2!$AA:$AA,M2!$M:$M,$AU11,M2!$K:$K,$F11,M2!$J:$J,T$7)*$P11))
```
với `S10 = sum(S11:S46)` · `O10 = sum(O11:O46)` *(khối THÁNG = mọi dòng CFA1 của tháng)*.
**④ Khoá RATE — `F3!AU11`** `=if(H11<>"VD62",H11,VLOOKUP(AQ11,AR11:AT12,3,FALSE))`; `AQ = H&"-"&L`; `AR11:AR12 = 'VD62-1' · 'VD62-2'`; `AS11 = SUMIFS(P11:P46,AQ11:AQ46,AR11)`; `AT11 = if(AS11>AS12,"VD341","VD62")`; `AT12 = if(AT11="VD341","VD62","VD341")` *(lặp 11 khối tháng — đo 408/408 hàng mang cùng mẫu `AU`)*.
**⑤ MID3 hiển thị** = `sumifs(F3!…; F3!$F:$F,$F24; F3!$H:$H,$H24)` ⇒ khoá `(vendor, tháng)`.

| Mã | Kiểu hàm *(`CACH_TINH` → `HAM_PE`)* | Tóm tắt | Khoá RATE |
|---|---|---|---|
| `Max` | `mang_ty_le_no1` | No = 1: Σ Looker[I = network dòng đầu, O = tháng, S = CDT1] × `%` dòng đầu; No ≠ 1 ⇒ 0 | chính nó |
| `VD341` · `VD444` | `mang_theo_no` | Σ Looker[I = network **dòng đầu**, **Q = No**, O, S] | chính nó |
| `VD428` | `mang_dong_no` | Σ Looker[I = network của dòng IX.VEN (vendor, No), O, S] *(= `Apple_store`/`IAP_tracking` dòng 22·23)*; No 3 network rỗng ⇒ 0 | chính nó |
| `VD62` | `khong` *(⛔ nhánh PE riêng — PE theo nhãn dòng ĐẦU = `Max`)* | — | No có ΣP **lớn hơn** mượn RATE `VD341`; hoà ⇒ No sau mượn |
| `thường` | `khong` | 0 *(nhánh cuối)* | chính nó |

Engine: `fls/bao_cao/phan_bo.py` — `HAM_PE` *(khoá = KIỂU)* · `ma_cach_tinh` *(mã lạ / kiểu lạ / hai nguồn mượn ⇒ `LoiPhanBo` có tên)* · `pe_tu_looker` · `chia_theo_cach_tinh` *(mọi vendor một đường; `bo_qua` 5 khoá rỗng)*. Tên mã chỉ ở config `fls/cau_hinh/vendor.py::CACH_TINH`.

## AC-2 · grep tên vendor *(Đ1 — `\b(VD341|VD444|VD428|Max|VD62)\b`, `*.py`)*
| Thư mục | Lần / tệp |
|---|---|
| **`fls/bao_cao`** | **0 / 0** *(docstring H9 cũ có 2 dòng tên — đã viết lại bằng nhãn)* |
| `fls/` | 46 / 2 — `fls/cau_hinh/vendor.py` *(config)* · `fls/api/bang_tuyen.py:709` *(chuỗi mô tả tuyến)* |
| `tools/` | 61 / 2 — `tools/do_hd2.py` *(`MongC4a`)* · `tools/khuon_dong_bang/ix_ven.py` *(khuôn suy nhãn)* |
Bài `test_H10_B2_…` đếm `fls/bao_cao` = 0 **và** đối chứng dương `fls/cau_hinh` > 0 *(Đ3: grep ⛔ mù)*.

## Mẫu số WP-C4b — khai TRƯỚC *(`MongC4b`, nhãn Đ4)*
Đo độc lập trước khi chạy engine *(nguyên mẫu scratchpad + đếm thẳng trên ảnh)*: 1.254/1.254 ô PE_cdt lệch ≤ `8,3e-10`.

| Nhãn | Mong = Đo |
|---|---|
| Vendor-tháng *(khoá MID3)* = đặc biệt + thường | **209 = 165 + 44** |
| dòng CFA1 vào engine *(Vendor × tháng × No)* · dòng MID1 đọc | 408 · 2.856 |
| ô so *(209 × 14 − ô ⛔ so được)* | **1.981** |
| ô ⛔ so được — 135 Vendor-tháng có dòng P = chữ `Need to manual input` × 7 *(⛔ hoá 0)* · đáp án ≠ 0 trong số ấy | 945 · 0 |
| **ô ≠ 0** *(đáp án hay engine)* = 823 PE_cdt + 165 O — tất cả ở vendor đặc biệt | **988** *(đặc biệt 988)* |
| lệch *(TOL `1e-6`)* | **0** |
| KS.AL Vendor-tháng *(Σ chia = O; = P khi P số)* · trong đó đặc biệt | 209 · **165** |
| **vendor bỏ qua** | **0** |
| Vendor-tháng theo kiểu PE: `khong` 44 · `mang_dong_no` 11 · `mang_theo_no` 22 · `mang_ty_le_no1` 132 | — |
| dòng mượn RATE · **có O ≠ 0** · dòng theo tổng tháng | 11 · **0** · 0 |
Hợp đồng: `docs/ITL/_tools/hd2_cong.json` khoá `WP-C4b` *(chỉ THÊM; gói cũ y nguyên)*. Lệnh: `python tools/do_hd2.py --goi WP-C4b --dsn "$PG_DSN_TEST"` ⇒ `DAT`.

## Lệch / giới hạn *(nói thẳng — Đ3)*
- **Lệch đo: 0.**
- Ba luật **⛔ chạm được bằng số thật** ⇒ chỉ bài tổng hợp chứng minh: ⓐ **luật mượn RATE** — 11 dòng mượn *(No 2 mỗi tháng, ΣP hoà 0 = 0)* đều có O = 0 ⇒ ghim `muon_o_khac_0 = 0` *(bỗng ≠ 0 ⇒ ĐỎ)*; ⓑ **4 hàm PE từ Looker** — ⛔ có ảnh Looker *(PD 502)*, PE vào từ MID1 đã tính; ⓒ **tổng tháng** — P số = 0 trên 408/408 dòng ⇒ 0 dòng `O = 0 ∧ P > 0`.
- `VLOOKUP` AS-IS ở MID1 dùng `VNM!$N$4:$N$35`, CFA1 dùng `$N$4:$N$39`, IX.VEN có 42 dòng *(4…45)* ⇒ vendor chỉ ở dòng 36…45 rơi `iferror` ⇒ rỗng. Engine dùng toàn bộ IX.VEN *(TO-BE)*; trên ảnh hiện tại ⛔ đổi kết quả *(lệch 0)*.

## Trả lời backlog H9
- **`H9-R1-03`** *(nguồn PE theo CDT1)*: đóng bằng MID1 cột T *(trên)*.
- **`H9-R1-04`** — ⓐ AS-IS "tổng tháng" = `$P*S10/O10`: **Σ chia PE_cdt của MỌI dòng CFA1 trong khối tháng *(kể cả vendor đặc biệt)* ÷ Σ O khối tháng** — ⛔ phải "Σ PE_cdt ÷ Σ PE" như `chia_nen_tang` H9. Hai cơ sở bằng nhau khi O = Σ 6 PE_cdt của Vendor-tháng: đo **209/209** *(lệch ≤ `4,7e-9`)* ⇒ trên ảnh hiện tại ⛔ khác. `chia_theo_cach_tinh` theo đúng `S10/O10` *(bài `test_H9_R1_04_a_…`)*; `chia_nen_tang` H9 ⛔ sửa *(ngoài phạm vi; ghi cho R1)*. ⓑ `and($O=0,$P>0)` ⇒ **P < 0 đi nhánh RATE riêng**; Σ PE = 0 ⇒ `M2!AA` `#DIV/0!` ⇒ `iferror` ⇒ **0 IM** ở AS-IS. TO-BE giữ **lỗi CÓ TÊN** *(bài `test_H9_R1_04_b_…`)*. Số thật: P số < 0 = **0** dòng.
- **`H9-R1-05`**: WP-C4b so GIÁ TRỊ mọi ô vendor đặc biệt — đổi `pe` một dòng CFA1 đặc biệt ⇒ ĐỎ *(bài `test_H9_R1_05_…`)*.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/cau_hinh/vendor.py` | `CACH_TINH` — mã → (kiểu hàm PE, vendor cho mượn RATE) + công thức nguồn |
| `fls/bao_cao/phan_bo.py` | công thức AS-IS ở docstring; `DongLooker` · `DongCFA1` · `KetQuaCachTinh` · `HAM_PE` · `ma_cach_tinh` · `pe_tu_looker` · `chia_theo_cach_tinh`; `ks_al` bỏ qua vế PM khi P = chữ *(None)* |
| `tools/do_hd2.py` | gói `WP-C4b` *(`MongC4b`, `so_sanh_c4b`, `chay_wp_c4b`)*; gói cũ ⛔ đổi |
| `docs/ITL/_tools/hd2_cong.json` | thêm khoá `WP-C4b` |
| `tests/bao_cao/test_vendor_dac_biet.py` *(13)* · `tests/oracle/test_do_hd2_c4b.py` *(30)* | AC-1…AC-6 |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` **3699 → 3742** *(= thu thập, +43)* cùng commit |

## Chứng minh ĐỎ
- Bài viết trước mã: `pytest tests/bao_cao/test_vendor_dac_biet.py` ⇒ exit 2 *(`ImportError: CACH_TINH` — thiếu hành vi)*.
- Phá nguồn `phan_bo.py` → chạy → trả *(bài H10 · cổng)*: M1 bỏ mượn RATE ⇒ 1 bài đỏ · cổng **DAT** *(ⓐ)*; M2 đảo No mượn ⇒ 4 đỏ · cổng ĐỎ *(lệch 63, `muon_o_khac_0` 11)*; M3 bỏ lọc No ⇒ 1 đỏ · cổng DAT *(ⓑ)*; M4 nhãn dòng cuối ⇒ 2 đỏ · cổng ĐỎ *(`kieu_vm`)*; M5 tổng tháng ⇒ 1 đỏ · cổng DAT *(ⓒ)*; M6 RATE sai mẫu ⇒ 32 đỏ · cổng ĐỎ *(KS.AL 165 lỗi)*. Phá config *(bỏ mượn)* ⇒ `muon: đo 0 ≠ mong 11`.
- Đ5 hai chiều: 11 trường `mong` × (−1, +1) ⇒ 22 bài ĐỎ có tên.

## Cổng
Chạy MỘT lần, một mình, trên cây commit ①:
- `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5444` ⇒ **`KẾT: ĐẠT`** — toàn bộ `12 failed, 3714 passed, 2 xfailed, 14 errors`: tập đỏ + XFAIL = đường nền **28 = 28** node id *(thêm 0 · bớt 0)* · chạy **3742** bài *(mong ≥ 3742)*; `tests/web` `3 failed, 672 passed`: **3 = 3** · 675 *(mong ≥ 675)*.
- `lint-imports` ⇒ `Contracts: 11 kept, 0 broken`.
- `kiem_tai_lieu.py` ⇒ `cong tai lieu DAT` *(343 file, 2647 bảng, 859 ô ngày, 104 mã QĐ)*.

## Vòng sửa sau R1 (KQ-218)

*(Thêm 19/11 — orchestrator chốt; R1 = 0 CHẶN · 1 NÊN SỬA · 7 GHI NHẬN. Phần trên giữ nguyên.)*

- **`H10-R1-01` — MỘT nguồn "tổng tháng".** `chia_nen_tang` *(WP-C4a)* từng chia tổng tháng theo `Σ PE_cdt ÷ Σ PE`, `chia_theo_cach_tinh` *(WP-C4b)* theo `S10/O10` — lệch ở ca `O ≠ Σ PE` *(R1: PM VD336 `30/30` vs `40/20`)*. Nay cả hai gọi chung `tong_thang_as_is` *(S10_c = Σ RATE×O, O10 = Σ O mọi dòng tháng)* + `pm_tong_thang` *(= AS-IS `P×S10/O10`)* ở `fls/bao_cao/phan_bo.py`. Bài ĐỎ trước *(`test_H10_R1_01_MOT_nguon_tong_thang_…`: ca tổng hợp `O=100/20/0`, PE `30/10`·`10/30`, P `60` ⇒ cả hai hàm phải ra `40/20`)*; hai bài H9 cũ *(`rate` tổng tháng; lỗi `Σ PE tổng tháng = 0`)* đổi theo cơ sở AS-IS *(`S10/O10`; lỗi nay là `tổng tháng Σ O = 0`)*.
- **Cổng sau sửa** *(chạy lại `do_hd2.py --goi …`, ⛔ `--ghi` — số ⛔ đổi nghĩa)*: WP-C4a `420` ô so · `196` ⛔ so được · ô ≠ 0 `0` · lệch `0` · KS.AL `44` — **y hệt** khối cũ; WP-C4b `1981` ô so · `945` ⛔ so được · ô ≠ 0 `988` · lệch `0` · KS.AL `209` · tổng tháng `0` — **y hệt**. Trên ảnh thật `O = Σ PE_cdt` (209/209) nên hai cơ sở trùng — đúng như R1 đo.
- **Đột biến sống nay chết** *(bản sao cây, phá → chạy `tests/bao_cao` + 2 bài oracle → trả)*: `M7` *(kiểu `VD62` `khong` → `mang_theo_no`)* ⇒ 1 đỏ · `M9` *(donor `VD341` → `VD444`)* ⇒ 2 đỏ · `M16` *(`p > 0` → `p != 0`)* ⇒ 1 đỏ.
- **`H10-R1-03` — chọn SỬA LỜI, ⛔ gỡ mã:** mục `CACH_TINH["VD62"][0] = "khong"` là **nhãn khai** — kiểu PE thật của `VD62` lấy theo nhãn dòng IX.VEN **đầu** *(= `Max` ⇒ `mang_ty_le_no1`)*; chỉ phần MƯỢN RATE `VD341` là riêng. **Đính chính bảng 5 mã ở trên:** dòng `VD62` ⇒ «kiểu theo dòng đầu *(`Max`)*; mượn RATE `VD341`». Chú thích `vendor.py` đã sửa; bài `test_H10_R1_03_M7_…` ghim nguyên văn mục + hành vi.
- **Còn lại ⇒ backlog:** `H10-R1-04` *(gói `WP-C4b-PE`)* · `-06` *(`mong` PE kiểu `khong`)* · `-07` *(3 mẫu RATE `AA`)* · `-08` *(ghim nhãn `Max` ⇔ network)*.
- **Q8:** `MONG_PYTEST_TOAN_BO` **3742 → 3746** *(= thu thập, +4)* cùng commit ① với bài ghim.

## Sửa tích hợp với CG2 (WP-C4b · H10-R2-01)

*(R2 `KQ-219`: chặn tích hợp — cùng kiểu `CG2-R2-03` đã sửa cho `WP-C4a` ở `BG-209`.)*

- **Lỗi:** khối `WP-C4b` trong `docs/ITL/_tools/hd2_cong.json` thiếu `tong_o`/`khop` ⇒ trên cây gộp `GET /gates` ra `HD2_WP_C4B` = null · `HD2_WP_C4` = null; 8 bài `tests/api/test_isp_gates_hd2.py` đỏ *(bài quét tệp thật báo `{'WP-C4b': ['tong_o','khop']}`)*.
- **Sửa (TDD — 2 bài oracle đỏ `KeyError` trước):** `tools/do_hd2.py` `so_sanh_c4b` xuất thêm `tong_o` = `o_so` = **1.981** *(Đ4: ô SO ĐƯỢC, ⛔ tính 945 ô P chữ)* và `khop` = `o_so − lech` = **1.981**; mọi khoá cũ giữ nguyên nghĩa. Khối sinh lại bằng `do_hd2.py --goi WP-C4b --dsn $PG_DSN_TEST --ghi` *(⛔ sửa tay)* — diff tệp JSON = đúng 2 dòng thêm, khối khác y từng byte.
- **Bài mới:** `test_CG2_H10_R2_01_khoi_WP_C4b_khai_tong_o_va_khop_theo_hop_dong_H4` · `test_CG2_H10_R2_01_khop_giam_dung_so_o_lech` *(đột biến 1 ô đáp án MID3 ⇒ `khop` = `tong_o − 1` = 1.980; ⛔ đột biến đầu vào CFA1 vì một ô lan ra 6 ô PE ⇒ lệch 6)*.
- **Ghim CG2 cập nhật cùng commit:** các bài `test_isp_gates_hd2.py` ghim thế giới 7 cổng *(trước H10)*; tệp thật nay có `WP-C4b` ⇒ 8 cổng, `HD2_WP_C4` = «2/2 gói con đạt (WP-C4a · WP-C4b) · Σ 2401/2401 ô» *(= 420 + 1.981)*, `HD2_WP_C4B` true; dat − 6 → 7. Không nới điều kiện nào — chỉ thêm C4b vào mong.
- **Q8:** `MONG_PYTEST_TOAN_BO` **3772 → 3821** = số THU THẬP thật của cây gộp *(`pytest --collect-only`; web giữ 675)*. Xung đột khi gộp: `dung_moi_truong_isp.sh` + bài ghim `test_S0_R2_03` ⇒ lấy bản nhánh làm việc rồi đặt = số thu thập.
