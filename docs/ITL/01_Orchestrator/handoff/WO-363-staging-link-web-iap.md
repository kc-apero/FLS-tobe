# WO-363 — Staging có LINK WEB (`https://…`) cho FE + BE, sau đăng nhập Google (IAP) — thay đường hầm SSH

| | |
|---|---|
| **Trạng thái** | `CHO_TEST` — 24/11 *(bàn giao [`BG-364`](BG-364-staging-link-web-iap.md); trước: `MO` 24/11 ~03:40 UTC → `DANG_LAM`)* |
| **Phát bởi** | orchestrator · 2026-11-24 |
| **Nhận** | `fls-dev` — phiên cloud Opus 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/STG-WEB` (nền = ngọn `isp/STG` `3223419`, staging đã chạy THẬT 01–04) |
| **Dải phiếu** | `BG-364` · `KQ-365` (R1) · `KQ-366` (R2 cuối). Số trống kế tiếp sau dải: **367** |

## Vì sao — lời chủ 24/11 ~03:35
> *"mở hẳn link web staging như https://fps-v35-staging-fe-b5zad5vm5q-as.a.run.app/login"*
- Hiện: app (FE + BE) chạy trên VM `fls-staging-app`, nghe `127.0.0.1:8088`; vào bằng tunnel IAP SSH từ máy có gcloud; Cloud Shell Web Preview ⛔ dùng được (đo 23/11).
- ⛔⛔ **Ràng buộc an toàn cứng:** FLS ⛔ có đăng nhập từng người — vỏ màn hình phát MỘT thẻ `ke_toan` chung (`GAP-WEB-01`, `fls/api/cua.py:369`), và staging chứa **dữ liệu THẬT** (tên người · tiền · số TK). ⇒ link công khai không xác thực = ⛔ TUYỆT ĐỐI. Orchestrator chọn: **Google IAP** đứng trước (chỉ tài khoản Google được cấp mới vào; như đăng nhập), app vẫn ⛔ mở ra Internet trực tiếp.

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 · thiết kế (đo trước, khuyến nghị) | so 2 đường, chọn 1, ghi số: **(a) Cloud Run + IAP** (URL `*.run.app`, tích hợp IAP của Cloud Run — tra tài liệu GCP hiện hành) với proxy trong container `$PORT` → `127.0.0.1:8088`; **(b) HTTPS Load Balancer + IAP trước VM hiện có** (cần tên miền/chứng chỉ?). Tiêu chí: số bước chủ bấm · chi phí/tháng · Cloud SQL connector · thời gian yêu cầu (chuỗi HD2 ~45 s chạy bằng lệnh, ⛔ HTTP) · giữ được luật cửa | BG |
| AC-2 · luật cửa | cửa `chay_cua.py` vẫn TỪ CHỐI nghe ngoài loopback (`GAP-WEB-01` ⛔ nới); chỉ thành phần proxy/IAP nghe ngoài; **yêu cầu ⛔ qua IAP ⇒ 401/403/302 tới Google login** (đo trên GCP bằng BÁO CÁO); actor chữ ký vẫn `--nguoi-ky` (đọc thêm header danh tính IAP chỉ để GHI NHẬT KÝ ai vào — ⛔ đổi luật ký, ghi câu chủ cho SSO sau) | bài + BÁO CÁO |
| AC-3 · script CHỦ chạy | `tools/staging/07_link_web.sh --project fp-a-project [--kiem] [--cho-vao email1,email2]`: dựng theo đường đã chọn; cấp `roles/iap.httpsResourceAccessor` cho tài khoản chủ + `--cho-vao`; in **URL**; BÁO CÁO có `mong` ĐỎ hai chiều: URL trả về trang đăng nhập Google khi ⛔ cookie · app sau IAP trả `/` 200 + API ⛔ thẻ 401 · 0 đường vào không qua IAP · ảnh đúng tag | gcloud GIẢ mô phỏng hành vi GCP (học 3 lỗi thật 23/11) + BG |
| AC-4 · dữ liệu + Cloud SQL | dùng lại Cloud SQL `fls-staging`, vai `fls_doc` (đọc) / `fls_ghi` (chỉ khi chế độ `ghi` ở bước ký UAT), bí mật từ Secret Manager — ⛔ đổi quyền 02 | bài |
| AC-5 | README + UAT v0.5: người test mở URL, đăng nhập Google, ⛔ cần gcloud; `--duong-nen` ĐẠT (sàn = thu thập thật); `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` 0 | `--duong-nen` |

## Ràng buộc
- ⛔ URL công khai không xác thực · ⛔ nới luật cửa · ⛔ khoá trong repo/chat · ⛔ gcloud thật (CHỦ chạy) · ⛔ ghi kho THẬT · ⛔ `docker compose down`.

## Nhật ký
| Lúc | Ai | Việc |
|---|---|---|
| 24/11 | `fls-dev` | `MO` → `DANG_LAM`: đọc WO + `BG-326` §3 · §11 + `KQ-327/328/344/351`; tra tài liệu GCP hiện hành *(Cloud Run IAP tích hợp · IAP FAQ · programmatic auth)* |
| 24/11 | `fls-dev` | `DANG_LAM` → `CHO_TEST`: `BG-364` — đường **(a) Cloud Run + IAP**; `07_link_web.sh` + `cong_iap.py` + `vao_cloud_run.sh`; +55 bài; sàn 5142 |
| 24/11 | `fls-dev` | Bổ sung theo orchestrator (lời chủ ~03:45 "tạo 1 tài khoản để đăng nhập chung"): màn `/login` FLS sau IAP, tài khoản `HondurasGesha`, băm scrypt ở Secret Manager `fls-staging-login` (`08_dat_dang_nhap.sh`); +26 bài; sàn 5168; `BG-364` cập nhật (AC-6) |
| 24/11 | `fls-dev` | `--duong-nen` @ `86a5003`: **KẾT: ĐẠT** (28 = 28 · web 3 = 3 · chạy 5168) — ghi vào `BG-364` §1.1 |
