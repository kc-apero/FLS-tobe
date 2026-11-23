# KQ-344 — R2b nhẹ STG *(vòng sửa sau R2 `KQ-328` · `WO-325` · `BG-326` §10)*

| | |
|---|---|
| **Phán quyết** | **`TRƯỢT`** — **2 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN** *(`STG-R2b-01…04`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_STG.md` v0.3)* |
| **Kiểm bởi** | `fls-test` *(phiên cloud · cụm PG **5446**)* · 2026-11-23 |
| **Kiểm ở** | `isp/STG` @ `c4a0f39` · cây gộp thử = `origin/main` @ `c5ea872` ⊕ `c4a0f39` *(gộp sạch; commit CỤC BỘ để `git archive HEAD` chạy, ⛔ đẩy)* |
| **Kho thật** | `KHONG_CHAM` — ⛔ GCP · ⛔ `gcloud` thật · ⛔ kho thật |

## ⛔ CHẶN — lỗi THẬT trên GCP (chủ chạy từ `c4a0f39`, orchestrator báo; Test ⛔ đo lại ở GCP)
1. **`STG-R2b-02` · bước 02** (`02_di_tru_phan_quyen.sh:133-140,269`): 23/24 ĐẠT, **1 ĐỎ** — `fls_ghi`/`fls_doc` còn CREATEROLE/CREATEDB (đếm vai = **2**, mong 0); `ALTER ROLE … NOCREATEROLE NOCREATEDB` bị từ chối, script nuốt lỗi rồi chỉ in `⚠`. Giả thuyết *(chưa đo)*: vai tạo bằng `gcloud sql users create`. Rủi ro dữ liệu thật: `fls_doc` lộ mật khẩu ⇒ tự đổi `default_transaction_read_only`. Sửa: tạo vai bằng SQL do `postgres` chạy `NOCREATEDB NOCREATEROLE`; có đường chuyển cho vai đã có.
2. **`STG-R2b-01` · bước 03**: `gcloud builds submit` tải **292**/398 tệp, `lstat /workspace/Dockerfile` ⇒ BUILD FAILURE. Mã: `.gcloudignore` `*` rồi ⛔ `!Dockerfile` *(và `!fls` ⛔ mở lại tệp con theo ngữ nghĩa gitignore ⇒ thiếu 106 tệp)*. Bài gcloud giả ⛔ áp `.gcloudignore` ⇒ xanh giả. Sửa: bỏ `.gcloudignore` khỏi ngữ cảnh / `--ignore-file` rỗng + báo cáo đếm tệp ngữ cảnh = tải lên, có `mong`.

## Bốn mục được giao
| # | Kiểm | Đo được |
|---|---|---|
| 1 | `STG-R2-01` chuỗi D1 hai chiều | `test_04` + `test_uat_doc` **29 passed**; chưa ký ⇒ đỏ đúng tập gói đọc tỷ giá, số lấy từ nguồn `_goi_doc_ty_gia`, mỗi gói một dòng lý do `FX_CHAN`/`ChuaKhai`; ký xong ⇒ `GOI_BIET` gói `0` thoát. **Chứng minh ĐỎ**: bỏ ký 1 tháng ⇒ `chưa ký 1` ⇒ 2 bài ĐỎ ✔ · `chay_chuoi.sh` chạy như script ⇒ 2 bài ĐỎ ✔ — **ĐẠT** |
| 2 | `ky_ty_gia.py` | chỉ `POST /config/fx/{yyyymm}/sign` thân `{}`, actor từ thẻ `/phien.js`, loopback `127.0.0.1`; thẻ ⛔ in; app `doc` ⇒ 405 ⇒ ĐỎ; đột biến thân có `actor` ⇒ bài ĐỎ ✔; chạy lại ⇒ `chưa ký 0`, 0 dòng `ký …: 201` — **ĐẠT** |
| 3 | UAT v0.3 | `[CHỜ I2]` còn **1** chỗ ở changelog *(biên bản)*, ⛔ ở phần khai; U7 *(chuỗi trước ký, ĐỎ)* → U8 *(ký)* → U9 *(chuỗi sau ký)*; số HD2 khớp `hd2_cong.json` ở `origin/main` *(0 dòng lệch)*; chèn lại nhãn / đổi `36→35` ⇒ ĐỎ ✔ — **ĐẠT** |
| 4 | Cây gộp thử + cổng | gộp sạch · thu thập thật **4995** = sàn, web **690**; `--duong-nen --cong 5446` một mình: **`KẾT: ĐẠT`** toàn bộ **28 = 28** *(thêm 0 · bớt 0)* · web **3 = 3**; `kiem_tai_lieu` OK · `lint-imports` 11 kept · `quet_pii_repo` 0 — **ĐẠT** |

## GHI NHẬN *(⛔ chặn)*
- `STG-R2b-03`: `test_04_chay_lai_van_DAT_va_khong_nap_chong` phụ thuộc thứ tự *(ĐỎ khi chạy một mình, xanh trong cả tệp)*.
- `STG-R2b-04`: cây gộp chưa commit ⇒ `03` `git archive HEAD` ⇒ 22 bài `test_03` ĐỎ với thông báo `tar` khó hiểu *(lần chạy cổng đầu ĐỎ vì lý do này; lần 2 ĐẠT sau commit cục bộ)*.

## Kết luận
Phần sửa R2 *(`STG-R2-01/02/05`)* **đúng**, cổng cây gộp **ĐẠT**. Nhưng staging thật **chưa dùng được**: 2 CHẶN từ GCP lọt qua cổng giả ⇒ gửi `DEV` vòng sửa riêng; sau sửa cần R2b lại + chủ chạy lại 02/03 ở GCP.
