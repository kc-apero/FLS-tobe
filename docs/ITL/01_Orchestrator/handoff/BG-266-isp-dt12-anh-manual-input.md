# BG-266 — Bàn giao WO-265 · ISP Step 38 · DT12 · ảnh Manual input của `ITL Ledge` (kỳ ≠ 2026-03)

| | |
|---|---|
| Phát bởi | fls-dev #DATA (phiên cloud) · 2026-11-20 · nhánh `isp/DT12` (nền `d9ac21f`) |
| Gửi | fls-test (R1 → `KQ-267`) |
| Ghi kho THẬT | `KHONG` · ⛔ chạy tự sinh (H15) · ⛔ sửa ảnh 2026-03 |

## Kết luận
**25 kỳ đọc được · 0 kỳ hỏng · 1 kỳ bỏ qua (2026-03, ảnh có sẵn)** = 26 kỳ của sổ. 12.049 dòng. Cổng `--mong` ĐẠT ở cả 25.

## Nguồn *(khoá SA chỉ-đọc · ⛔ ghi/nhận xét)*
- Sổ `ITL I Input Transaction Ledger File 2/2 (ADJUSTED)` · id `1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA` *(⛔ bản `[COPY]`)* · tab `ITL Ledge` *(duy nhất, lưới 12.684 × 69)*.
- Vùng đọc: cột `A` *(ngày)* + `R:AT` *(ITL ID + 28 cột)*, hàng `10…12684`; hàng `7·8` chỉ để lấy **tên** cột. Đọc theo lát 1.500 hàng, `UNFORMATTED_VALUE` + `SERIAL_NUMBER`, mỗi lát ≤ 3 lần thử. ⛔ cột `B` Số chứng từ · `C` Diễn giải.
- 42 hàng cuối + hàng 9 có `R` (công thức ITL ID) mà `A` rỗng ⇒ ⛔ tính là dòng dữ liệu (đếm: **43** hàng `A` rỗng / **12.633** hàng có ngày).

## Số kỳ *(Đ4: mỗi số đếm MỘT vật)*
- **26 kỳ** theo cột ngày `A`: `2024-10 … 2026-11` — ⛔ phải 23 như ISP *(22 + 2026-03)*. Lý do: **3 kỳ `2024-10/11/12` (6 · 3 · 6 = 15 hàng lạc ở đầu sổ)** ngoài dải `2025-01…2026-11` (23 tháng). Giữ cả 3 *(⛔ ép về 22)* vì `đọc được + hỏng = số kỳ của sổ`; orchestrator quyết có loại 3 kỳ ấy khỏi H15 hay không.
- Bỏ 2026-03 ⇒ **25** ảnh · mong `--mong-ky 26`.

## Dòng theo kỳ *(đếm độc lập trên cột `A` ⇒ pin ở `MONG` của bài; ảnh `so_dong` = số ấy)*
| Kỳ | Dòng | Hàng sheet | `itl_id` = `#N/A ()` | Byte | checksum |
|---|---|---|---|---|---|
| 2024-10 | 6 | 10…15 | 0 | 12,443 | `42be93a5618d36f4` |
| 2024-11 | 3 | 16…18 | 0 | 7,280 | `cb1eb227df517d0b` |
| 2024-12 | 6 | 19…24 | 0 | 12,434 | `cc171dd3f506982d` |
| 2025-01 | 748 | 25…772 | 0 | 1,257,585 | `888e3fa40bd2c195` |
| 2025-02 | 283 | 773…1055 | 0 | 477,992 | `a4268fc55c80dbcd` |
| 2025-03 | 297 | 1056…1352 | 0 | 482,092 | `211e71d545a9b867` |
| 2025-04 | 332 | 1353…1684 | 0 | 548,233 | `563eab98883aa1a5` |
| 2025-05 | 408 | 1685…2092 | 0 | 649,605 | `b8e94ba589572282` |
| 2025-06 | 348 | 2093…2440 | 0 | 586,744 | `9113d66b3bb512f8` |
| 2025-07 | 546 | 2441…2986 | 0 | 956,129 | `4b73312b2cdfab99` |
| 2025-08 | 537 | 2987…3523 | 0 | 926,512 | `853a733c023dc17e` |
| 2025-09 | 501 | 3524…4024 | 0 | 877,034 | `8caf00d18f9b0291` |
| 2025-10 | 487 | 4025…4511 | 0 | 856,007 | `59a383f029e74e13` |
| 2025-11 | 477 | 4512…4988 | 2 | 836,903 | `3a290605a5cac7a0` |
| 2025-12 | 566 | 4989…5554 | 0 | 984,266 | `9981c74cb2e6b5d5` |
| 2026-01 | 471 | 5555…6025 | 0 | 830,314 | `4c0e262cb8eb7fd0` |
| 2026-02 | 439 | 6026…6464 | 1 | 771,924 | `2d916d9b2f568eba` |
| 2026-04 | 600 | 7049…7648 | 1 | 1,054,055 | `dd5ba3ad2517d100` |
| 2026-05 | 537 | 7649…8185 | 1 | 939,254 | `c561fe05684c2b33` |
| 2026-06 | 613 | 8186…8798 | 2 | 1,070,168 | `b9ae8898a5fe65bf` |
| 2026-07 | 686 | 8799…9484 | 3 | 1,199,145 | `5133b774e0963193` |
| 2026-08 | 724 | 9485…10208 | 0 | 1,265,343 | `2b6e9e9e23153f09` |
| 2026-09 | 737 | 10209…10945 | 35 | 1,299,284 | `ab94e45031f2e272` |
| 2026-10 | 1038 | 10946…11983 | 47 | 1,826,670 | `1e4e21409740a433` |
| 2026-11 | 659 | 11984…12642 | 27 | 1,154,460 | `9035a581129ed2d1` |
| **Σ 25 kỳ** | **12.049** | | **119** | **20.881.876** | |

## Kỳ hỏng
**0.** Cơ chế có sẵn *(bài `test_AC2_…`)*: kỳ đọc hỏng sau 3 lần thử ⇒ `blocked` **có tên** trong cổng + manifest `itl_ledge_cac_ky.json` → `hong`; tập kỳ rỗng ⇒ ĐỎ *(Đ3)*; `đọc được + hỏng ≠ mong` ⇒ ĐỎ.

## Kích thước *(AC-6)*
Tổng **20.881.876 byte (≈ 19,9 MB)**; lớn nhất `2026-10` = 1.826.670 byte ⇒ **0 ảnh > 2 MB** *(luật `DT4-R1-07`)*. Ảnh to hơn ảnh 2026-03 (702 KB / 584 dòng ≈ 1,2 KB/dòng) vì khuôn công cụ bọc mỗi ô chữ thành `{"chu": …}` *(≈ 1,7 KB/dòng)*.

## PII *(AC-4)*
Ảnh chỉ có `dong_sheet` + `itl_id_sheet` + `ngay` + 28 cột; ⛔ `Diễn giải` · `Số chứng từ` · `Email Address` · tên người *(bài quét tên cột + cấy 3 cột cấm ⇒ exit 2)*. `python tools/quet_pii_repo.py` = **0 chỗ · 0 tệp**. Bản thô ở `/tmp/dt12_tho` (chmod 600) **đã xoá**, ⛔ commit. Dữ liệu ở lượt đọc chỉ ĐẾM.

## Đã làm
- `tools/khuon_dong_bang/itl_ledge_ky.py` — khuôn MỚI *(tệp riêng; ⛔ sửa `dong_bang_sheet.py`)*: 30 cột = đúng khoá dòng ảnh 2026-03; ánh xạ theo **tên** cột hàng 7+8 *(lệch 1 tên ⇒ TỪ CHỐI)*.
- `tools/doc_itl_ledge_ky.py` — vòng đọc sổ → bản thô theo kỳ → cổng `dong_bang_sheet.py itl_ledge_ky … --mong <số đếm ở cột A> --ra …/itl_ledge_<kỳ>.json` → manifest.
- `tests/fixture/dap_an/itl_ledge_<kỳ>.json` ×25 + `itl_ledge_cac_ky.json`.
- `tests/du_lieu/test_anh_manual_input.py` — 15 bài. **Q8:** `MONG_PYTEST_TOAN_BO` 4267 → **4283** *(đo `--collect-only`)* + bài ghim cùng commit; `MONG_PYTEST_WEB` 681 giữ.
- Ảnh 2026-03 và mọi ảnh cũ: **đúng từng byte** *(sha256 ảnh 2026-03 ghim trong bài; `git diff --stat` chỉ thêm tệp mới + 2 dòng sàn)*.

## Đỏ trước *(TDD — bài thật, đỏ vì THIẾU ảnh/khuôn)*
Lệnh: `python -m pytest tests/du_lieu/test_anh_manual_input.py` trước khi có khuôn/ảnh ⇒ **exit 1 · 11 failed, 2 passed** *(2 bài xanh = bài canh `MONG` ≠ rỗng + ảnh 2026-03 nguyên byte)*; sau: **15 passed**. Bản ghi `exit=1` lưu ở lượt làm.
Chiều ĐỎ chứng minh: đổi 1 tên cột · cấy `Diễn giải`/`Số chứng từ`/`Email Address` · lỗi `#REF!` · `--mong` lệch 1 ⇒ cổng cắn.
Một lỗi đã cắn trong lượt: `test_CHI_MOT_BAN_KHAI_trong_ca_he` đỏ vì khuôn tự viết `startswith("#")` ⇒ đổi sang `fls.canon.o_loi.la_o_loi` *(một bản khai)*.

## Cổng cuối
`quet_pii_repo.py` 0 · `lint-imports` 11 kept 0 broken · `kiem_tai_lieu.py` ĐẠT · `--duong-nen --cong 5437`: **ĐẠT** ở lần chạy thứ 2 *(lần 1 ĐỎ: 1 bài mới `test_CHI_MOT_BAN_KHAI_trong_ca_he` — đã sửa, xem trên)*; toàn bộ 28 = 28 node đỏ có sẵn · thêm 0 · chạy **4283** (mong ≥ 4283); `tests/web` 3 = 3 · chạy 681

## Giả định *(phương án hẹp nhất; khuyến nghị kèm theo)*
1. **Hình ảnh = khuôn `dong_bang_sheet`** *(checksum · `{"chu": …}` · `thu_tu` · `cong`)*, ⛔ JSON thô `{nguon, ky, dong}` của ảnh 2026-03 — ảnh 2026-03 không có checksum/cổng. H15 cần **bộ đọc ảnh mới** *(`_nap` chỉ `json.loads`; AC-5 đo đúng điều ấy)* hoặc quyết định đóng băng lại 2026-03 theo khuôn mới — **khuyến nghị: ⛔ đổi 2026-03, viết bộ đọc `{"chu"}` ở H15**.
2. **Ô số của 28 cột ghi thành CHỮ số thập phân** *(`202603.0` ⇒ `"202603"`)*: cột `svc_*` lẫn số lẫn chữ (đo: `svc_start_manual` 10.611 số + 1.396 chữ + 626 rỗng) mà công cụ đòi một kiểu/cột. `_chuan` của `do_voi_so_luong` chuẩn hoá về chuỗi nên không mất tin.
3. **`itl_id_sheet = "#N/A ()"` giữ nguyên** *(119 ô / 25 kỳ — hàng chưa gán ITL ID; ảnh 2026-03 cũng giữ 4/584)*; tập đóng 1 giá trị, lỗi khác ở bất kỳ ô ⇒ TỪ CHỐI.
4. **Ảnh 2026-03 LỆCH sổ hiện tại**: sổ đã bị sửa sau khi đóng băng — kỳ 2026-03 nay ở hàng `6465…7048` *(ảnh cũ `6470…7053`: dịch 5 hàng)*, cùng 584 dòng, nhưng **7.430/16.352 ô** của 28 cột khác ảnh *(vd dòng đầu: `hd_manual` ảnh = `SC | Server Cost`, sổ nay = `OMC | Online Marketing Cost`)*. ⛔ đụng *(WO)*; ảnh các kỳ khác phản ánh sổ **ngày 20/11**. **Khuyến nghị:** orchestrator hỏi chủ — đóng băng lại 2026-03 từ sổ hiện tại, hay giữ.
5. **Nguồn sống**: sổ ADJUSTED còn đang sửa; mốc đọc `ngay_dong_bang = 2026-11-20` ghi trong từng ảnh. Kỳ `2026-10`/`2026-11` có nhiều `#N/A ()` nhất *(47 · 27)* — kỳ gần nhất, chưa đóng sổ.
6. Sổ **chưa có** `Manual input` thật ở mọi dòng: cột `*_manual` rỗng nhiều *(vd `hd_manual` rỗng 832/12.633 hàng của 26 kỳ)* — H15 lọc theo kỳ/khối, ⛔ việc của bước này.
