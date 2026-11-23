# KQ-144 — biên bản kiểm `BG-143` *(R1 · ISP 3.1.2 · Step 14 · C5)*

| | |
|---|---|
| **Thuộc** | `BG-143` · `WO-142` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1 độc lập)* · 2026-11-18 · nhánh `isp/C5` @ `07fae3d` *(mã `d7e2cd0` + `BG-143`; nền C4 `31509bd`)* |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 4 NÊN SỬA · 3 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C5.md`)*. Bất biến chỉ-thêm/đủ-hoặc-không/MÁY đặt phiên bản đều **giữ** khi chạm thật; 4 hàng NÊN SỬA là **bài thiếu** + một cửa ghi công khai chưa kiểm, ⛔ lỗi hành vi hôm nay |

## Cổng chạy lại
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `dung_moi_truong_isp.sh --cong 5446` | dựng kho rỗng | `KẾT: ĐẠT` · 27/27 di trú · `pg_verify` 27 bảng/view · `lint-imports` 11 kept | ✅ |
| `pytest tests/db tests/cau_hinh tests/api` + 3 bài sinh | xanh | `3 failed · 771 passed · 11 errors` — **14 bài đỏ** đều là bài `SO_THAT`/`mui_thu_luoi` đòi **dữ liệu kho THẬT** *(đo: `0 mối nối`, `kho không có dòng nào có ngày`)*; kho dựng riêng `fls_itl = 0` ⇒ **tập RỖNG ⇒ môi trường, ⛔ C5** *(Đ3)*. Khớp đường nền ở dòng dưới | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5446` *(một mình)* | tập đỏ = nền | toàn bộ: **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **3128** bài *(mong ≥ 3128)* · skipped 0 · `tests/web`: **3 = 3** · 667 bài | ✅ |
| `lint-imports` | 11 kept | `Contracts: 11 kept, 0 broken` | ✅ |
| `python tools/soi_bang_tuyen.py` | khớp SQL | `OK /nap · /config/fx · /config/hd` · "khớp SQL thật ở cả **42** tuyến" | ✅ |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | K1–K6 | 6/6 OK *(244 file · 2.289 bảng · 778 ô ngày · 104 mã QĐ)* | ✅ |
| `python -m fls.db.pg_migrate` | — | `fls_test`: "không có gì để áp" · `pg_verify: khớp` | ✅ |
| Sinh lại hiện vật: `erd_export --write` · `sync_erd_doc.py` · `sinh_ban_do_tang.py` | 0 diff | cả ba `không đổi` · `git diff` = **0** dòng | ✅ |

## Bảng AC
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 | nạp `ix_fx.json` ⇒ v1; GET 37 dòng, `lac=[202306]` | kho rỗng ⇒ `ChuaKhai`; nạp ⇒ `phien_ban=1`, **38 hàng** `_dong` = 37 tháng + 1 khoá `@thang_dau`; ảnh tự khai `so_dong=37`·`lac=['202306']`, tuyến trả đúng | ĐẠT |
| AC-2 | nạp lại ⇒ v+1, `khong_doi`, ⛔ ghi đè | bài xanh; đột biến `khong_doi=False` giết; 8 luồng đồng thời ⇒ `[1..8]` | ĐẠT |
| AC-3 | UPDATE/DELETE ⇒ trigger ĐỎ có tên | **12/12** câu *(UPDATE/DELETE/TRUNCATE ×2 bảng · `TRUNCATE CASCADE` ×2 · `ON CONFLICT DO UPDATE` · `MERGE UPDATE/DELETE`)* ⇒ `INV-I08` có tên, trừ `TRUNCATE ban` trần = lỗi FK của PG *(⛔ tên, vẫn ĐỎ)*; vô hiệu từng trigger bằng đột biến SQL ⇒ 3/4 bị giết, 1 dự phòng *(C5-R1-06)* | ĐẠT *(+ `C5-R1-06`)* |
| AC-4 | golden + `pg_verify` + sinh lại ERD | golden diff = **đúng 2 `CREATE TABLE`** *(⛔ trigger — trigger ở di trú)*; `pg_verify` 27/27; sinh lại 0 diff | ĐẠT |
| AC-5 | HD đọc từ kho; rỗng ⇒ `ChuaKhai` ≠ `BangLa` | kho rỗng ⇒ `ChuaKhai`(409); `IX.XXX`·`''`·`ix.fx` ⇒ `BangLa`(404); đột biến đổi mã ⇒ giết; ⛔ rơi về ảnh tĩnh *(ảnh đã gỡ, dưới)* | ĐẠT |
| AC-6 | gỡ `ix_fx_mau.json`; soi XANH; `?run_id=` ⇒ 400 | `git ls-files fls/cau_hinh/tinh` ⇒ **không còn `ix_fx_mau` · `ix_hd_cay` · `ix_mapping_master`**; đột biến bỏ 400 ở cả hai tuyến ⇒ giết | ĐẠT |
| AC-6b | gỡ hai ảnh gói; MM chỉ `hd_code` | khoá `gia_tri` MM đo = `{hd_code, thu_tu}` *(sạch)*; **nhưng bài canh bằng đếm hàng** — đột biến thêm `phu.tho` SỐNG ⇒ `C5-R1-02` | ĐẠT *(bài yếu)* |
| AC-8 | `C4-R2-01/02/03` + `C4-R3-01/02` | R2-01/02/03 có bài, đột biến M16/M17/M18 **bị giết**; **R3-01/02 CHƯA** — M13/M14/M15 SỐNG, Grep `C4-R3` = 0 | **MỘT PHẦN** ⇒ `C5-R1-01` |
| AC-7 | `MONG_PYTEST_TOAN_BO` 3108→3128 | `--duong-nen` chạy **3128** ≥ 3128; bài ghim đổi cùng commit | ĐẠT |

## 8 trọng tâm
| # | Phép thử *(lệnh/đo)* | Kết quả |
|---|---|---|
| 1 | 12 câu phá + đột biến trigger; lối vòng | chặn đủ, có tên. **Lối vòng tồn tại:** chủ bảng `fls` `ALTER … DISABLE TRIGGER <tên>` rồi `DELETE` thành công *(⛔ superuser)*; Grep event-trigger/`DISABLE TRIGGER` = 0 ⇒ `C5-R1-06` *(GHI NHẬN)*. `COPY` chỉ INSERT ⇒ không phải lối sửa |
| 2 | khoá trùng giữa chừng · hàng không serialize · 8 luồng | đếm `(ban,dong)` trước/sau `(1,37)→(1,37)` cả hai ⇒ ⛔ bản dở; 8 luồng ⇒ phiên bản `[1..8]`, 0 lỗi. Bài chỉ bắt ngoại lệ ⇒ `C5-R1-03`; M1 *(bỏ khoá)* SỐNG ⇒ `C5-R1-05` |
| 3 | chữ ký `nap`; checksum | `nap(conn,bang,cap,*,nguon,actor)` — ⛔ tham số `phien_ban`/`luc`; `luc` do `DEFAULT now()`. Checksum `sort_keys` + sắp theo khoá: nạp `[(k,{a,b}),(j,..)]` rồi đảo thứ tự dòng *và* khoá ⇒ **cùng checksum, `khong_doi=True`**. `nguon` ⛔ vào checksum *(nạp lại ảnh khác tên ⇒ `khong_doi`)*; cùng nội dung khác `bang` ⇒ `False`. `actor` rỗng ⇒ `LoiCauHinh` |
| 4 | v1,v2 · bảng lạ · kho rỗng | đọc luôn bản mới nhất *(đột biến ASC bị giết)*; `IX.ALR` chưa nạp ⇒ `ChuaKhai`; `IX.NOPE` ⇒ `BangLa` |
| 5 | so trả lời C4 *(`git archive 31509bd`)* ↔ C5, cùng kho dựng từ ảnh DT3 | `/config/hd`: **khoá giống**, mọi giá trị giống, **chỉ khác `nguon`/`nguon_mm`** *(đường ảnh)*. `/config/fx`: **khoá giống**, khác dữ liệu *(C4 đọc ảnh MẪU 12 dòng; C5 đọc ảnh thật 37 dòng, `lac=[]`→`[202306]`)* — đúng ý AC-1. `?run_id=` ⇒ 400 giữ |
| 6 | golden · `pg_verify` · sinh lại | golden = 2 `CREATE TABLE` ⛔ gì khác; 27/27; 3 công cụ sinh ⇒ 0 diff. Trigger ⛔ vào golden/`pg_verify` ⇒ `C5-R1-06` ⓑ |
| 7 | AC-8 | xem bảng AC: 3/5 làm. Mục còn nợ ⇒ `C5-R1-01` |
| 8 | PII | khoá `gia_tri` đo: MM `{hd_code, thu_tu}` · HD `{cap,cha,dong_sheet,nhom,ten,thu_tu}` · FX `{COP,HKD,SGD,USD,VND}` — ⛔ `tho`, ⛔ tên người; `ĐẾM`: hàng MM có chuỗi ≥ 6 chữ số = **0**. Bài canh yếu ⇒ `C5-R1-02` |
| — | câu tác giả: `thang_dau=202401` | ⛔ gõ cứng ở `fls/`; ảnh `lac=['202306']` khớp ⇒ ⛔ ĐỎ; hằng chép ở 2 tệp bài ⇒ `C5-R1-07` |

## Đột biến *(bản sao `git archive isp/C5`, trả nguyên — 30 chỗ hợp lệ; ⛔ tính M9 tương đương và một lượt M8 lỡ tay là no-op)*
**GIẾT 19 · SỐNG 10.** Giết: ASC-đọc · `khong_doi` luôn False · `_soi_bang` nhận mọi bảng · bỏ kiểm actor · đổi mã ChuaKhai · bỏ 400 `run_id` ×2 · `_so` không giới hạn · `_mot_dong` không cắt · `except` hẹp ở `doc_mm_van_ban` · `nhom` mất khỏi kho · M21 `khong_doi` luôn sai · M22 `thang_dau` đọc lệch · M23 không ánh xạ `Month` · vô hiệu trigger `dong` UPDATE/DELETE · `ban` UPDATE/DELETE · `dong` TRUNCATE · bỏ UNIQUE ×2.
Sống: M1 *(khoá)* · M4 *(so bản đầu)* · M7 *(bỏ giao dịch)* · M8′ *(tho vào `gia_tri`)* · M13/M14/M15 *(ten/nhom/sorted)* · `luc` DEFAULT · vô hiệu trigger `ban` TRUNCATE *(dự phòng)* · M20 *(`doc_mm` sắp theo `thu_tu` — **tương đương** ở tuyến: chỉ dùng độ dài + hiệu tập hợp)*. *(M9 `thang_dau` ở bước kiểm của `nap_ix_fx`: tương đương — giá trị lưu là tham số, ⛔ giá trị kiểm; ⛔ tính.)*

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT | AC-1…7 ✅; AC-8 một phần |
| **Dữ liệu** *(kho dựng riêng từ di trú; ⛔ chạm kho thật)* | ĐẠT | khoá `gia_tri` sạch; `fls_itl=0` ⇒ bài `SO_THAT` đỏ là môi trường *(14, khớp đường nền)* |
| **Màn hình** | N/A | C5 ⛔ đổi màn; `goi_cua.js` +12 dòng ⇒ `tests/web` 667 bài, 3 đỏ = nền |

## Phát hiện *(chi tiết ở sổ)*
| F | Mức | Nơi | Gửi |
|---|---|---|---|
| `C5-R1-01` | NÊN SỬA | `tests/api/test_isp_config_hd.py` — `C4-R3-01/02` chưa | `DEV` |
| `C5-R1-02` | NÊN SỬA | `test_kho_cau_hinh_pg.py:156` — PII canh bằng đếm hàng | `DEV` |
| `C5-R1-03` | NÊN SỬA | `:137` — đủ-hoặc-không chỉ `raises` | `DEV` |
| `C5-R1-04` | NÊN SỬA | `cau_hinh_repo.py:117,241` — `nap` công khai ⛔ kiểm; bản bẩn ⇒ `500 FLS-INTERNAL` | `DEV` |
| `C5-R1-05` | GHI NHẬN | M1 · M4 · `luc` thiếu bài | `DEV` *(tuỳ)* |
| `C5-R1-06` | GHI NHẬN | trigger: lối vòng chủ bảng; `pg_verify` ⛔ trigger | orchestrator |
| `C5-R1-07` | GHI NHẬN | hằng `202401` chép ở 2 tệp bài | `DEV` *(tuỳ)* |

## Bài thử mới
⛔ Không thêm bài vào `tests/` *(vai KIỂM không sửa mã; khuyến nghị ở sổ cho Dev)*. Công cụ thử đặt ở thư mục tạm của phiên, ⛔ vào repo.

## Câu hỏi cho orchestrator
Gộp bốn NÊN SỬA vào một vòng sửa *(chỉ bài + 1 hàm bọc lỗi, ⛔ đổi hợp đồng)* hay chuyển `C5-R1-04` sang `C6`? **Khuyến nghị A:** sửa luôn trong C5 — rẻ, và cửa ghi chỉ-thêm là chỗ duy nhất không có đường lùi.
