# BG-201 — bàn giao `WO-200` *(DỪNG MỘT PHẦN: AC-4 · WP-C4a CHẶN vì thiếu ảnh đầu vào)*

| | |
|---|---|
| **Thuộc** | `WO-200` (ISP 3.1.2 · Step 24 · H9 — AL.PLT · GI vendor thường + KS.AL, cổng WP-C4a) |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · 2026-11-18 |
| **Nhận** | orchestrator *(quyết ảnh đầu vào)* → rồi `fls-test` R1 `KQ-202` |
| **Commit** | `claude/bold-galileo-zukpaf-isp/H9` — ① mã + bài · ② BG này |

## Kết luận
- **AC-1 · AC-2 · AC-3 · AC-5 · AC-6: xong** trên đầu vào TỔNG HỢP *(15 bài, `tests/bao_cao/test_phan_bo.py`)*.
- **AC-4 (WP-C4a): ⛔ dựng — DỪNG theo luật WO** *("đầu vào GI ⛔ có trong ảnh ⇒ DỪNG, ⛔ đoán, ⛔ đọc đáp án thay")*. Ba chặn, mỗi chặn một số đo:

| # | Chặn | Số đo *(Đ4 — nhãn)* |
|---|---|---|
| ① | **MID3 ⛔ mang khoá Vendor-tháng** — ảnh `gi_mid3` chỉ có `dong_sheet` + 14 cột số *(A:N bị loại vì PII)* ⇒ ⛔ biết hàng nào là vendor nào, vendor thường hay đặc biệt | `253` hàng số · cột `vendor`/`thang` = `0` |
| ② | **O · P theo Vendor-tháng (CFA1 · PD 504) ⛔ có ảnh**. O/P chỉ nằm trong MID3 = ĐÁP ÁN; P *(PM = VLOOKUP ITL ID × 10⁶)* ⛔ có ở MID1/MID2 | ảnh CFA1 GI = `0` tệp; MID3 vế PM ô ≠ 0 = `0/1.771` *(BG-148)* |
| ③ | **Vendor THƯỜNG có PE = 0 trên mọi ô** ⇒ WP-C4a "vendor thường" đo trên tập toàn 0 *(Đ3)* | vendor thuần `thường` theo IX.VEN = **4** *(VD58 · VD61 · VD113 · VD336)*; ô PE MID2 của 4 mã = `308` *(4 × 11 tháng × 7 CDT1)*, ô ≠ 0 = **`0`** *(= đúng `308` ô RATE `#DIV/0!` của MID2)* |

⭐ Đo phụ *(dò cấu trúc, ⛔ dùng làm đầu vào)*: mỗi khối tháng MID3 = 22 hàng = 1 tổng tháng + 1 tổng nhóm `Max` + 12 hàng nhóm `Max` *(RATE chung, khớp RATE MID2 của 12 vendor ấy tới `1e-9`)* + 1 tổng nhóm VD341·VD428·VD444 + 3 hàng ấy + **4 hàng O = 0** *(chính 4 vendor thường)*. ⇒ Mọi ô ≠ 0 của MID3 thuộc vendor **đặc biệt** *(H10)*.

## Mẫu số WP-C4a khai TRƯỚC *(nếu có ảnh — Đ4)*
| Nhãn | Giá trị |
|---|---|
| Vendor-tháng vendor thường | `4 × 11 = 44` |
| ô so được | `44 × (O + P + 6×2)` = **`616`** |
| ô ≠ 0 | **`0`** *(đo MID2 PE; P toàn 0)* ⇒ cổng xanh trên tập 0 = ⛔ bằng chứng |
| ô ⛔ so được | toàn bộ MID3 ở hiện trạng — lý do ① |

## Vendor đặc biệt bỏ qua *(ĐẾM, ⛔ im — `kq.bo_qua` luôn đủ 5 khoá)*
`Max` · `VD341` · `VD428` · `VD444` · `VD62` — **5 mã nhãn**; trên IX.VEN kho: **15** vendor mang nhãn ≠ `thường` *(12 qua `Max`, VD62 ở cả `Max` lẫn `VD62`, VD57 ở cả `Max` lẫn `thường` ⇒ xếp đặc biệt)*, **4** vendor thường; tổng **19** = đúng 19 vendor của MID2.

## Số CDT1 thực *(Đ4)*
- IX.VEN / MID1 / MID2: **7** CDT1 *(MID1 `408 × 7`, MID2 `209 × 7`)*.
- MID3: **6** cặp cột *(CVL · COR · SHQ1 · CSM · CAH · ASA — ⛔ SHQ2)* ⇒ engine nhận `cdt1=` từ tầng gọi; bài kho chia trên 6 = 7 − SHQ2.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/phan_bo.py` *(mới)* | `chia_nen_tang(pe, o, p, ven, cdt1=)` thuần *(IX.VEN = `BangVen` từ kho)*; RATE theo Vendor-tháng; O = 0 ∧ P > 0 ⇒ tổng tháng *(mọi vendor của tháng)*; Σ PE = 0 mà tiền ≠ 0 ⇒ `LoiPhanBo` có tên; `ks_al` đo lại Σ chia = O/P *(TOL 1e-6)*, trả mẫu số, 0 ⇒ ĐỎ |
| `tests/bao_cao/test_phan_bo.py` *(15)* | AC-1/2/3/5 tổng hợp · 1 bài PG đọc IX.VEN từ kho test · 2 bài GHIM chặn ①③ *(Đ5: ảnh mới khác ⇒ ĐỎ ⇒ xét lại)* |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3585 → **3600** *(+15)* cùng commit |

**Chứng minh ĐỎ** *(phá → chạy → trả)*: bỏ vế PM khỏi `ks_al` ⇒ 1 đỏ; tắt luật tổng tháng ⇒ 2 đỏ; xếp vendor `Max`+`thường` về thường ⇒ 4 đỏ.

## Khuyến nghị *(cần ảnh nào)*
1. **Ảnh `CFA1 | GI Platform Data Ledger` (PD 504)** cột KHÔNG PII: `Vendor ID · tháng · No · PE Amount · PM Amount · ITL ID` — đầu vào O/P theo Vendor-tháng-No.
2. **Bổ sung khoá cho MID3**: đọc lại `O10:AF273` kèm cột Vendor ID + tháng của chính sheet MID3 *(chỉ 2 cột mã, ⛔ PII)*, khoá `(vendor, thang)` ⇒ so từng ô.
3. **Quyết của chủ/BA**: vì vendor thường có PE = 0 ở mọi tháng, WP-C4a "vendor thường" ⛔ chứng minh được gì trên dữ liệu thật ⇒ đề nghị gộp cổng ô-≠-0 sang H10 *(vendor đặc biệt)*, giữ H9 ở mức engine + KS.AL tổng hợp.

## Lệch
- Không có lệch ĐO *(chưa đo được — xem chặn)*. Engine chưa có CLI/`do_hd2 --goi WP-C4a` — chờ ảnh.

## Sau DT8b *(chỉ THÊM — gộp `claude/bold-galileo-zukpaf-isp/DT8B` @ `833a273`, BG-205; orchestrator chốt 18/11)*
Chặn ① ② gỡ: MID3 có khoá `(vendor, thang)` *(209 hàng)*, ảnh `tests/fixture/dau_vao/gi_cfa1.json` *(PD 504, 408 dòng)* cho O = Σ `pe`, P = Σ `pm` số theo Vendor-tháng. Chặn ③ là **KẾT QUẢ** *(Đ3)*, ⛔ lỗi.

**Cổng WP-C4a = `python tools/do_hd2.py --goi WP-C4a --dsn "$PG_DSN_TEST"` ⇒ `DAT`** *(IX.VEN đọc TỪ KHO test; kho chưa khai ⇒ ĐỎ có tên; ⛔ ghi kho thật)*. Hợp đồng ở `docs/ITL/_tools/hd2_cong.json` khoá `WP-C4a`. Mong khai TRƯỚC *(`MongC4a`, lấy từ số đo BG-205)* — đo ra **khớp cả 8**:

| Nhãn *(Đ4)* | Đo | Mong |
|---|---|---|
| Vendor-tháng thường *(4 vendor × 11 tháng)* | 44 | 44 |
| ô so *(44 × 14 − ô PM ⛔ so được)* | 420 | 420 |
| ô ⛔ so được — P = chữ `Need to manual input` *(⛔ hoá 0)*: 28 Vendor-tháng × (P + 6 PM_cdt) | 196 | 196 |
| **ô ≠ 0** — **tập toàn 0: đo được nhưng ⛔ chứng minh RATE** | **0** | 0 |
| lệch | 0 | 0 |
| bỏ qua có tên: `Max` 132 · `VD341` 11 · `VD428` 11 · `VD444` 11 · `VD62` 11 Vendor-tháng | 5 nhãn · **15** vendor | 5 · 15 |

**Đ5 hai chiều** *(bài `tests/oracle/test_do_hd2_c4a.py`, 12)*: một Vendor-tháng thường bỗng ≠ 0 ở đầu vào ⇒ engine `LoiPhanBo` *(PE theo CDT1 — Looker PD 502 — ⛔ có ảnh)* ⇒ ĐỎ buộc khai lại; một ô đáp án đổi ⇒ ĐÚNG ô ấy lệch + `o_khac_0` ≠ mong ⇒ ĐỎ; mỗi `mong` sai ⇒ ĐỎ; bỏ chữ P ⇒ ô so 616 ≠ 420 ⇒ ĐỎ; MID3 mất khoá ⇒ ĐỎ có tên. Phá nguồn *(⛔ đếm ô ≠ 0 · ⛔ loại ô PM chữ)* ⇒ mỗi lần 1 bài ĐỎ, trả nguyên.

**KS.AL trên ảnh thật** *(chỉ báo)*: đo **44** Vendor-tháng thường, lệch 0, nhưng tiền ≠ 0 = 0 *(tập 0)*. **165** Vendor-tháng đặc biệt *(15 vendor)*: engine ⛔ áp *(bỏ qua theo nhãn; thiếu PE theo CDT1)* ⇒ KS.AL ⛔ chạy — việc H10.

**Chuyển H10** *(câu cho WO H10)*: phép so ô ≠ 0 của RATE *(MID3 ô ≠ 0 đều ở vendor đặc biệt — PE ≠ 0 165/165, BG-205)* + đầu vào **PE theo CDT1** *(Source Looker PD 502, hoặc chốt dùng MID1 cột T làm đầu vào)* — ⛔ có ảnh thì RATE ⛔ đo được ở bất kỳ vendor nào.

Bài ghim cũ `test_H9_B3_CHAN_MID3_khong_mang_khoa_vendor_thang` ĐỎ sau gộp *(Đ5 cắn đúng)* ⇒ khai lại thành `…_sau_DT8b_MID3_CO_khoa_vendor_thang_209_hang`. Q8: sàn 3602 *(DT8b)* + 15 *(H9 ①)* = 3617 ở commit gộp → **3629** *(+12 bài C4a)*.
