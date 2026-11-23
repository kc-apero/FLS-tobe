# KQ-318 — R2 cuối kiểm `I2` · `WO-315` · `BG-316` *(vòng sửa sau `KQ-317` — Step 47, bước CUỐI)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_I2.md` v0.2. Đo trên **cây gộp thử** *(⛔ commit)* = nhánh làm việc `1ce3a80` + `isp/H14` `854550b` + `isp/I2` `fc744a8` — gộp sạch, 0 xung đột; cụm PG riêng cổng 5446. Vai KIỂM: ⛔ sửa mã.

| # | Việc | Kết |
|---|---|---|
| 1 | **D1 `-01`** *(đo độc lập; ô số = Σ khoá số của khối **và** đếm đệ quy mọi lá số)* | bỏ ký **202510** ⇒ **0/11** gói ra số, 11/11 `FX_CHAN 202510` · bỏ ký **202503** ⇒ **0/11**, 11/11 `FX_CHAN 202503`; `GET /gates` 15 cổng `dat=false` có chữ `FX_CHAN` *(gồm `HD2_WP_C4` + C4a/b/c)*; ký lại ⇒ 11 gói `dat=true`, mọi khoá số = `hd2_cong.json` **0 lệch** |
| 2 | Engine AL tối thiểu | diff vòng sửa: **0 tệp `fls/`**; `tools/do_hd2.py` chỉ thêm `FxKho` · `ty_gia_kho` · `kiem_fx_thang` · `chay_goi` *(+ `main` gọn lại)*, ⛔ đổi phép tính. Kho đủ ký: `--goi WP-C4a·b·c --ghi` ⇒ `KẾT: DAT` ×3, `hd2_cong.json` đổi **0 byte** |
| 3 | `-02` `fx_cua` ở mã sản phẩm | bài 0 chỗ vá `nap_fx`; 5 chỗ gọi `nap_fx` ở `tools/` qua `FxKho`. Đột biến USD ×100 / mọi tiền tệ ×100: C2 đổi số; C4a·b·c giữ |
| 4 | `-03` gói ⛔ phụ thuộc tỷ giá | lời giải thích **ĐÚNG**: C4 đọc CFA1/MID đã có số, đường dữ liệu C4 ⛔ chạm tỷ giá *(0 chỗ `fx` trong khối C4 ngoài `kiem_fx_thang`)*; tháng MID3 ⊆ MID1/CFA1 ⇒ phủ đủ; ×100 giữ C4 — bài ghim `MONG_DOI_USD` 8/11 · `MONG_DOI_DEU` 3/11 xanh. Giới hạn *(kho ký sai GIÁ TRỊ ⇒ C4 vẫn xanh)* còn trong backlog |
| 5 | `-05` lệnh máy chủ | đọc kỹ: ⛔ ghi `fls` · ⛔ `FLS_CHO_GHI_THAT` · `.venv\Scripts` · `docker start fls-pg-1` · `FLS_PW_INDEX`/`FLS_CHROMIUM` đúng. Bản tương đương cloud ⇒ **28 passed** *(128 s, 0 skipped)* = mong 28; nhánh `27 + 1 skipped` chỉ đọc mã *(`I2-R2-04`)* |
| 6 | F03 Chromium thật 390 px | đủ ký: C2 ✓ · C3 ✓ · C4 ✓ *(3/3)* · C5 **— KHÔNG ĐO ĐƯỢC** *(605)*; bỏ ký 202510: C2 · C3 · C4 · C5 **✗ KHÔNG ĐẠT** có chữ `FX_CHAN 202510` |
| 7 | Đột biến mới (4) | **4/4 đỏ**: `kiem_fx_thang` no-op ⇒ 3 đỏ · chỉ tháng đầu ⇒ đỏ · `fx_cua` bỏ chặn ⇒ 2 đỏ · `ty_gia_kho` no-op ⇒ 20 lỗi *(canh ảnh)* |
| 8 | Cổng | `--duong-nen --cong 5446` MỘT lần, một mình: **ĐẠT** — tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy **4.871** = mong, skipped 0; web **3 = 3**, 690 · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT *(489 tệp · 974 ô ngày)* · `kiem_thuyet_minh` 35/35 · `soi_bang_tuyen` 49/49 · bài liên quan 377 passed |

**GHI NHẬN** *(⛔ chặn)*: `I2-R2-01` `--ghi` vẫn đè khi ĐỎ, nay dễ cắn hơn vì CLI mặc định đọc kho *(⛔ chạy `--ghi` ở `fls`)* · `-02` D1 chặn theo THÁNG GÓI ĐỌC: bỏ ký 202607 ⇒ chỉ 3/11 chặn *(C3a · C3b · C5c)* · `-03` C4 nhạy GIÁ TRỊ tỷ giá chốt bằng đo · `-04` lời BG về `FLS_*` thiếu. R1 `-01 -02 -03 -04 -05` ĐÃ sửa đúng; `-06` giữ nhãn.

## Điều kiện MERGE còn lại *(ngoài phạm vi KIỂM)*
1. **Chủ chạy lại trên `fls-pg-1`** theo mục *"Lệnh chạy lại trên máy chủ"* của `BG-316` *(`docker start fls-pg-1` — ⛔ `docker compose down`)*: `pytest tests/tich_hop/test_hd2_xuyen_suot.py -p no:cacheprovider` ⇒ mong **`28 passed`** *(có Chromium)* hoặc `27 passed, 1 skipped` *(không có — chấp nhận)*; ⛔ chạy `do_hd2.py … --ghi` ở `fls` *(`I2-R2-01`)*.
2. **ThuongCT ký `O6`** *(605 · `WP-C5c` — đến lúc đó thẻ F03 C5 = KHÔNG ĐO ĐƯỢC, `dat` null)*.
3. **`isp/H14` gộp vào nhánh làm việc TRƯỚC** `isp/I2` *(`isp/I2` đã mang gộp H14 `854550b` — gộp sau H14 ⇒ sạch; H14 R2b ĐẠT, chờ chủ ký 605)*; sàn sau gộp = **4.871 · web 690** *(đo, cây gộp thử)*.
