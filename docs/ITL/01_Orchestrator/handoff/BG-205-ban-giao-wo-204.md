# BG-205 — bàn giao `WO-204` *(DT8b: đầu vào GI cho cổng WP-C4a của H9)*

| | |
|---|---|
| **Thuộc** | `WO-204` · nhánh `isp/DT8B` *(nền `6afb0ce`)* |
| **Phát bởi** | `fls-dev` làn DATA · phiên cloud · 2026-11-18 |
| **Nhận** | `fls-test` R1 `KQ-206` → H9 chạy lại WP-C4a |
| **Ghi kho THẬT** | `KHONG` *(chỉ đọc Sheets bằng khoá SA chỉ-đọc; bản thô ở scratchpad, đã xoá, ⛔ commit)* |

## Kết luận
AC-1…AC-5 xong. **Nhưng WP-C4a "vendor thường" vẫn đo trên tập toàn 0 — đó là KẾT QUẢ (Đ3), ⛔ lỗi nguồn:** `PE = O = P = 0` trên **44/44** Vendor-tháng thường. Có ảnh khoá ⇒ H9 nối được hàng ↔ Vendor-tháng và so O/P/PE từng ô; nhưng ô ≠ 0 của vendor thường = **0**. Khuyến nghị cũ của `BG-201` §3 *(gộp cổng ô-≠-0 sang H10)* **được dữ liệu xác nhận**.

## AC-1 · MID3 thêm cột khoá *(`tests/fixture/dap_an/gi_mid3.json`, checksum `3b93f232a0bedc0a` → `013de4e6e826b096`)*
Bản đồ cột lập bằng hàng tiêu đề 7–8 trước; chỉ đọc cột khoá. 14 cột số + `dong_sheet` + `thu_tu` **đúng từng byte** *(bài ghim sha `285b413dab10123d` trên phần cũ)*.

| Cột thêm | Nguồn | Lý do |
|---|---|---|
| `vendor` | `H` *Mã đối tác (ID Payee)* = Vendor ID, `VD…` | biết hàng nào thuộc Vendor nào / thường hay đặc biệt |
| `thang` | `F` *Thời điểm bắt đầu sử dụng* = `yyyymm` | biết hàng thuộc tháng nào |

⛔ Không lấy: `G` *(= `F` trên 253/253)* · `K L M` = LE · No · **ITL ID — RỖNG cả 264 hàng ⇒ MID3 ⛔ có ITL ID** *(WO "ITL ID nếu có": không có)* · `A:C`, `I:J`, `N` (PII/file đính kèm).
Số đo *(Đ4)*: **209** hàng mang khoá = 19 Vendor × 11 tháng `202502…202512` *(209 cặp duy nhất)*; **44** hàng tổng ⛔ khoá *(vendor/thang rỗng)*; 253 = 209 + 44.

## AC-2 · ảnh CFA1 GI *(`tests/fixture/dau_vao/gi_cfa1.json`, checksum `0e39e49cd95901ed`)*
- **Nguồn:** `[COPY] GI Platform Data Ledger …` id `1rciS4fMaBAWsqfQYVPeCZ45E1PNRP2b0BkWRq6kO1z4` *(sổ DT8)*, tab `CFA1 | GI Platform Data Ledger` *(duy nhất 1 tab khớp)*, **PD 504**, vùng `M,K,Q,T,S,R` hàng 10…417.
- Cột ảnh ← cột nguồn: `vendor`←`M` · `thang`←`K` *(`L`=`K` 408/408)* · `no`←`Q` *No Transactions Per Vendor* · `pe`←`T` *PE Amount* *(`E`=`T`=`U` 408/408)* · `pm`←`S` *PM Amount* · `itl_id`←`R`. Thêm `pm_ghi_chu` *(xem dưới)*.
- **408 dòng** *(đếm dòng ảnh)*; **dòng/tháng** *(MONG, Đ5 hai chiều)*: `202502…202510` = **36** × 9 · `202511` = **42** · `202512` = **42**.
- `S` lẫn chữ: **232** số `0` · **176** chữ `Need to manual input` ⇒ tách `pm_ghi_chu` *(⛔ hoá 0)*. `R`: **232** `ITL#…` · **176** `Ko tìm thấy`.
- **Đối chiếu hai nguồn:** Σ `pe` theo (Vendor, tháng) = `O` của MID3 trên **209/209** *(mẫu số 209 ⛔ rỗng)*.
- Công cụ `dong_bang_sheet.py` ⛔ sửa; hai khuôn: `gi_mid3.py` *(chỉ THÊM khoá)* · `gi_cfa1.py` *(mới)*.

## AC-3 · mẫu số cho WP-C4a *(nhãn Đ4)*
Vendor thường theo IX.VEN = **4** *(VD58 · VD61 · VD113 · VD336)* × **11** tháng = **44 Vendor-tháng**; **55** dòng CFA1.

| Đại lượng *(nguồn)* | Vendor-tháng ≠ 0 / 44 |
|---|---|
| **PE** = Σ `T` theo Vendor-tháng *(CFA1)* | **0** |
| **O** = `pe` MID3 *(đáp án)* | **0** |
| **P** = Σ `S` số *(CFA1)* | **0** — và **28/44** Vendor-tháng có `S` = chữ `Need to manual input` *(P ⛔ xác định, ⛔ hoá 0)* |

⇒ Cổng ô-≠-0 vendor thường vẫn trên tập 0 *(KẾT QUẢ, Đ3)*. Đối chứng vendor đặc biệt *(15 Vendor × 11 tháng = 165 Vendor-tháng, đo trên ảnh CFA1)*: PE ≠ 0 trên **165/165** ⇒ mọi tín hiệu của WP-C4a nằm ở H10; vế PM *(P số)* = 0 trên cả 209.

## AC-4 · PII
Quét tên cột `PM_COT_RIENG_TU`: 0 trùng cả hai ảnh. Ca phá có bài: `Email Address` ⇒ TỪ CHỐI · `cot` ngoài whitelist ⇒ TỪ CHỐI · tên người ở cột Vendor ⇒ `vendor_la@<dong_sheet>` ĐỎ. Mọi lời lỗi **⛔ in giá trị ô** *(bài khẳng định chuỗi nhạy cảm ⛔ có trong stdout/stderr)*.

## AC-5 · Q8
`MONG_PYTEST_TOAN_BO` **3585 → 3602** + bài ghim cùng commit. Đo: nền `6afb0ce` thu thập **3586** *(đã lệch sàn cũ 1)* + 16 bài mới `tests/du_lieu/test_dau_vao_gi.py` = 3602.

## Chứng minh ĐỎ
Mỗi cổng mới được viết bài ĐỎ trước *(24 bài ĐỎ khi chỉ có bài, chưa có khuôn)*, rồi XANH sau khi dựng: khoá Vendor lạ · mất tháng ở hàng có Vendor · đổi tháng một dòng *(tổng giữ 408, `thang_lech@202502`)* · lưới rỗng *(TỪ CHỐI)* · cột PII.

## Cổng
Xem commit; `--duong-nen --cong 5445` · `lint-imports` · `kiem_tai_lieu.py` — kết quả nguyên văn ở tin nhắn bàn giao của phiên.
