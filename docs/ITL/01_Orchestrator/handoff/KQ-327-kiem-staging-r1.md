# KQ-327 — biên bản kiểm `BG-326` *(R1 · `WO-325` — staging bước 02 · 03 · 04 + `Dockerfile` + UAT + README)*

| | |
|---|---|
| **Thuộc** | `BG-326` · `WO-325` |
| **Kiểm bởi** | `fls-test` *(phiên cloud · cụm PG **5447**)* · 2026-11-23 |
| **Phán quyết** | **`TRƯỢT`** — **2 CHẶN · 6 NÊN SỬA · 5 GHI NHẬN** *(13 phát hiện `STG-R1-01…13`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_STG.md`)*; Dev đẩy `d04557a` *(chỉ tài liệu)* đóng `-03` + `-13` ⇒ **còn mở 2 CHẶN · 5 NÊN SỬA · 4 GHI NHẬN** |
| **Kiểm ở** | `isp/STG` @ `65ab287` *(lúc kiểm `BG` ⛔ khai hash: `@@SHA@@` chưa điền — `STG-R1-03`, Dev điền ở `d04557a`: đúng `65ab287`)* · cây gộp thử `origin/claude/bold-galileo-zukpaf` @ `6e68811` ⊕ `65ab287` *(⛔ commit cây thử)* |
| **Kho thật** | `KHONG_CHAM` — ⛔ GCP · ⛔ `gcloud` thật · ⛔ ghi kho thật. Chỉ kho scratch `fls_r1*_<pid>` của cụm phiên, đã dọn |

## Kết luận một dòng
Mã tường quyền **đúng và đã ĐO trên quyền PostgreSQL THẬT** *(`fls_itl` chỉ-THÊM · `fls_doc` chỉ-đọc · cửa loopback · ảnh sạch · khởi động 1,69 s tái lập)* — nhưng **TRƯỢT** vì: **(1)** SA `fls-staging-app` được `secretAccessor` trên **5/5** bí mật *(kể cả `postgres`, `fls_admin`)* ⇒ người có shell trên VM đọc mật khẩu chủ kho ⇒ **vòng quanh cả hai tường vừa đo** *(`STG-R1-01`)*; **(2)** gộp H14 vào ⇒ **2 bài `tests/staging` đỏ** *(ghim cứng "10 gói", tip có 11)* ⇒ `--duong-nen` ĐỎ *(`STG-R1-02`)*. Kèm 6 NÊN SỬA *(chủ yếu: UAT lệch số ở ngọn · U7/U8 đòi `sudo` · cổng 01 ĐẠT khi gán vai hỏng · 04 chết giữa `IX.ALR` ⛔ tự lành · `--kiem` của 02 tạo bảng)*.

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/staging` *(trên `65ab287`)* | 93 bài mới + 3 bước 01 = 96 | **96 passed** · 132 s | ✅ |
| `pytest --collect-only` *(cây gộp)* | sàn 4868 *(nhánh STG)* | **4953** = tip 4857 + 96 · web **690** | ⛔ xung đột sàn ⇒ `STG-R1-09` |
| `dung_moi_truong_isp.sh --duong-nen --cong 5447` *(cây gộp, MỘT lần, một mình)* | "28 = 28 · web 3 = 3" *(BG ⛔ khai cho cây gộp)* | **`KẾT: ĐỎ`** — `36 failed · 4901 passed · 2 xfailed · 14 errors` = 4953 chạy · tập đỏ **52** = 28 cũ + **24** thêm *(22 đồ giả do cây thử ⛔ commit + **2 thật**)* · web **3 = 3** ✔ | ⛔ `STG-R1-02` |
| `kiem_tai_lieu.py` *(cây gộp)* | 0 | **K1–K6 OK** *(492 tệp · 2.984 bảng · 974 ô ngày)* | ✅ |
| `lint-imports` | 11 kept | **11 kept · 0 broken** | ✅ |
| `quet_pii_repo.py` | 0 | **0 chỗ · 0 tệp** | ✅ |
| `docker build` *(thật)* | 373 MB · 5 s có cache | **374 MB** · 11,7 s *(lần đầu, không cache)* | ✅ |
| khởi động ảnh *(đường thật của `vao.sh`)* | 1,7 s · 31 MiB | **1,69 s · 30,43 MiB** · `GET /` 200 · `/gates` không thẻ **401** | ✅ |

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 · bước 02 | `pg_verify: khop`; `fls_itl` chỉ-THÊM; `fls_doc` SELECT + `ALTER ROLE … read_only = on`; BÁO CÁO có `mong` hai chiều; chứng ĐỎ | Quyền **THẬT** tự đo: `fls_ghi` UPDATE/DELETE/TRUNCATE `fls_itl` ⇒ `InsufficientPrivilege` · `fls_doc` `SET … = off` rồi INSERT/UPDATE/CREATE ⇒ từ chối bằng `GRANT` · thành viên `cloudsqlsuperuser` sau 02 = 0 · chạy 2 lần ⇒ exit 0 · 25 hàng/21 có `mong` · đột biến M1 M2 M3 cắn · **nhưng** `--kiem` tạo bảng *(`-08`)* | **ĐẠT có điều kiện** *(NÊN SỬA `-08`)* |
| AC-2 · nơi chạy app | đo trước rồi khuyến nghị; `Dockerfile` + `03`; cửa vẫn TỪ CHỐI | VM + IAP: **tái lập** số đo *(1,69 s · 30 MiB · 401)*; cửa nghe loopback *(đột biến M5 ⇒ cửa tự từ chối `GAP-WEB-01`)*; ảnh **0** `sao_luu`/`hien_vat`/`.env*`/`.git`; uid 10001. **Nhưng** SA quá quyền *(`-01`)* · U7/U8 đòi `sudo` *(`-06`)* · số chuỗi HD2 ở ngọn đã đổi *(`-05`)* | **TRƯỢT** *(CHẶN `-01`)* |
| AC-3 · bước 04 | nạp config bằng công cụ SẴN CÓ; đòi `FLS_CHO_GHI_THAT=1`; `mong` hai chiều + mẫu số ≠ 0 | 9 bảng × 2 + MẪU SỐ · `Email Address` 0 cột · `fls_itl` = 0 · `--nguon-that` từ chối · M6 M7 cắn · gói chạy 11/11 thoát 0 sau nạp *(cây gộp)*. **Nhưng** chết giữa `IX.ALR` ⛔ tự lành *(`-07`)* | **ĐẠT có điều kiện** *(NÊN SỬA `-07`)* |
| AC-4 · kịch bản UAT | số từ `hd2_cong.json` ở ngọn | 36/36 thẻ khớp, **nhưng** thiếu hàng `WP-C5c`, hàng cha `WP-C5` sai ở ngọn, 2/2 số §1·615 sai, U7 "10 dòng" ⇒ 11; bài canh UAT đóng cứng `CHA` ⇒ xanh giả | **TRƯỢT** *(NÊN SỬA `-05`)* |
| AC-5 · README | trình tự 01→UAT, chạy ở đâu · bao lâu · gửi lại | Đúng cách đưa mã *(tự chạy `02` từ cây upload: `KẾT: ĐẠT`)*; đếm lệch *(130 vs 96 · 27 vs 25)* | **ĐẠT** *(GHI NHẬN `-13`)* |
| AC-6 (Q8) | sàn + bài ghim cùng commit; `--duong-nen` ĐẠT 28 = 28 · web 3 = 3; 3 cổng = 0 | Trên **STG riêng**: sàn 4868 = thu thập 96 + 4772 ✔. Trên **cây gộp**: `--duong-nen` **ĐỎ** *(28 + 2 thật)*; `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` = 0 ✔ | **TRƯỢT** *(CHẶN `-02`)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến `INV-I08`)* | Tường quyền ĐÚNG ở tầng PostgreSQL; **bị vòng ở tầng IAM** | `STG-R1-01`: `SECRETS` 5/5 gán `secretAccessor`; app cần ≤ 3. `INV-I08`: `fls_ghi` ⛔ `UPDATE`/`DELETE`/`TRUNCATE`/`DISABLE TRIGGER`/`DROP` `fls_itl` — **6/6 bị từ chối** |
| **Dữ liệu** *(kho scratch, config)* | 9 bảng nạp đúng `mong`; mẫu số ≠ 0; `fls_itl` = 0 *(thiết kế)* | `fls_cau_hinh_ban`: `IX.ALR` v2 (17 + bản KÝ 38 dòng) · 8 bảng còn lại v1; `Email Address` ⛔ vào kho; `actor` ⛔ chứa `@` — **đo bằng BÁO CÁO của `04`** *(đã đột biến M6 cắn)* |
| **Màn hình** *(UAT · loopback · 401)* | Cửa nghe `127.0.0.1` *(đột biến M5 ⇒ cửa tự từ chối)*; 401 không thẻ; ⛔ dựng màn riêng | Ảnh thật: `GET /` 200 8 ms · `/gates` 401 1 ms. UAT lệch số ở ngọn `-05`; ⛔ soát 5 trạng thái màn *(không thuộc WO này)* |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `STG-R1-01` | `CHAN` | `01_dung_staging_gcp.sh:61,151-155` | `grep SECRETS=` ⇒ 5 phần tử; vòng gán SA ⇒ `postgres` + `fls_admin` có trong tầm SA | `DEV` *(+ `HOI` BA nếu tách hai SA)* |
| `STG-R1-02` | `CHAN` | `tests/staging/test_04_nap_du_lieu.py:311,319-320` | cây gộp: `pytest tests/staging` ⇒ 94 pass · 2 fail `assert (11 == 10)` | `DEV` |
| `STG-R1-03` | `NANG` *(đã sửa `d04557a`)* | `BG-326:8,30,35` | `grep -n "@@" BG-326` = 3 | `DEV` |
| `STG-R1-04` | `NANG` | `01_dung_staging_gcp.sh:139-157` | `gcloud` giả `PERMISSION_DENIED` ở `secrets add-iam-policy-binding` ⇒ `KẾT: ĐẠT` exit 0 | `DEV` |
| `STG-R1-05` | `NANG` | `UAT_STAGING_E2E.md:26,44,70` · `test_uat_doc.py:18` | `hd2_cong.json` @ `6e68811`: C5c 86.150 · 615 = 13.760 ≠ 12.380 · Σ chua_co_dau_vao = 5.258 ≠ 6.753 · 11 gói 44,4 s 797 MB | `DEV` / `BA` *(duyệt UAT)* |
| `STG-R1-06` | `NANG` | `UAT:44-45` · `03_dung_app.sh:152` | `grep osAdminLogin` = 0; U7 `sudo docker exec` vs `osLogin` | `BA` *(`HOI`)* + `DEV` |
| `STG-R1-07` | `NANG` | `nap_cau_hinh_ix.py:59,80,89-94` | ngắt giữa `IX.ALR`; chạy lại ×2 ⇒ `IX.ALR` v1 · 17 dòng · exit 1 | `DEV` |
| `STG-R1-08` | `NANG` | `02_di_tru_phan_quyen.sh:221,264` | `GRANT CREATE ON SCHEMA public TO fls_doc` rồi `--kiem` ⇒ bảng `fls_probe_doc_ghi` còn; "làm" ⇒ exit 3 | `DEV` |
| `STG-R1-09` | `NHE` | `dung_moi_truong_isp.sh:420-424` | xung đột sàn 4857 ↔ 4868 ⇒ 4953 | orchestrator |
| `STG-R1-10` | `NHE` | `03_dung_app.sh:171` · `gcloud_gia.py:117-120` | `DO_TRONG` ⛔ bài chạy; stub ⇒ 4 dòng đúng | `DEV` |
| `STG-R1-11` | `NHE` | `01…:110,115,118` · ảnh | `--password="$PW"` ×3; 7 tệp `tools/` mang tên SA cục bộ trong ảnh | `DEV` |
| `STG-R1-12` | `NHE` | `test_04_nap_du_lieu.py:194-202,305-320` | `-k sau_khi_nap` riêng ⇒ đỏ; cả tệp ⇒ xanh | `DEV` |
| `STG-R1-13` | `NHE` *(đã sửa `d04557a`)* | `README.md:4,17` | `--collect-only` = 96 ≠ 130; 02 = 25 hàng ≠ 27 | `DEV` |

## Bài thử mới *(`tests/nghiem_thu/`)*
⛔ Không thêm bài vào `tests/nghiem_thu/` ở R1: các phát hiện `CHAN`/`NANG` là **thiếu bài ở phía Dev** *(ghi "Khuyến nghị" ở sổ: bài đo SA ⛔ có `secretAccessor` trên `postgres`/`fls_admin`; bài `IAM_LOI ⇒ ĐỎ`; bài ngắt giữa `IX.ALR`; bài `--kiem` ⛔ để lại bảng)* — Test ⛔ sửa mã/bài của Dev. Chứng ĐỎ đã làm bằng **8 đột biến `git archive`** *(cả 8 cắn; trả nguyên `diff` = 0)* + 4 phép đo độc lập ở scratchpad phiên. Tái hiện bằng lệnh nằm trong cột "Đo" của sổ.

## Truy vết
`03_TRACEABILITY_GAP_REPORT.md`: ⛔ cập nhật — `WO-325` ⛔ phát sinh dòng spec→bài của `BA-05/09/10/11`.
