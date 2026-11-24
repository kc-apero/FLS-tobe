# FLS staging — trình tự CHỦ chạy (01 → 02 → 03 → 04 → 07 → UAT)

> ⛔ **Claude KHÔNG vào GCP** (quyết chủ 20/11): mọi script ở đây do **chủ** chạy trong **Google Cloud Shell**; chủ gửi lại **chỉ phần `BÁO CÁO`** (từ dòng `── BÁO CÁO` tới hết).
> ⛔ **Chưa script nào chạy thật trên GCP** (đo 23/11). Mỗi script đã được thử với `gcloud` GIẢ + `cloud-sql-proxy` GIẢ + **`psql` · `pg_migrate` · quyền PostgreSQL THẬT** trên kho cục bộ (`tests/staging/`, 96 bài) — nên cú pháp, thứ tự, quyền và BÁO CÁO đã được chứng minh ĐỎ-khi-hỏng; còn những giả định về **chính GCP** ở §"Giả định chưa kiểm" bên dưới sẽ lộ ra ở BÁO CÁO thật.
> Nội dung gửi lại ⛔ chứa mật khẩu/khoá: BÁO CÁO chỉ có tên, cấu hình, số đếm (bài thử quét rò rỉ: 0 chỗ).

Chuẩn bị một lần. Dưới đây viết `P` = `<PROJECT_ID>` (staging thật: `fp-a-project`, instance `fls-staging`, `asia-southeast1`; bước 01 đã ĐẠT 12/12 ngày 23/11).

**Đưa mã lên Cloud Shell** — 02/03/04 cần cây mã (`fls/`, `tools/`, `tools/staging/sql/`, `requirements.txt`, `Dockerfile`, `tests/fixture/cau_hinh/`, và với 03 cả git để `git archive`), ⛔ chỉ mỗi một tệp `.sh`. Cách ngắn nhất, chọn một:
1. `git clone` repo vào `~/fls` rồi `git checkout claude/bold-galileo-zukpaf-isp/STG` (cần quyền đọc repo từ Cloud Shell) — **bắt buộc cho 03** (script đòi `git archive HEAD`).
2. Không có quyền clone: trên máy bạn `git archive --format=tar.gz -o fls.tar.gz HEAD`, **Upload** `fls.tar.gz` lên Cloud Shell, `mkdir ~/fls && tar -xzf fls.tar.gz -C ~/fls && cd ~/fls && git init -q && git add -A && git -c user.email=x -c user.name=x commit -qm snap` (đủ cho 02/04 và cho `git archive` của 03; ⛔ có `sao_luu/` `hien_vat/` vì `git archive` chỉ lấy tệp đã commit).
Script 01 chỉ cần chính nó (đã chạy xong). Script 02/04 tự tạo venv + `pip install psycopg` (cần mạng ra PyPI — Cloud Shell có).

| Bước | Lệnh (Cloud Shell) | Mất bao lâu *(ước — ⛔ đo được ở GCP)* | Gửi lại |
|---|---|---|---|
| **01** dựng Cloud SQL · `fls_admin` · 5 bí mật · SA *(vai app `fls_ghi`/`fls_doc` do **02** tạo bằng SQL — `STG-R2b-02`)* | `bash tools/staging/01_dung_staging_gcp.sh --project P --kiem` rồi bỏ `--kiem` | tạo máy Cloud SQL **5–15 phút** (script 01 tự ghi); còn lại < 2 phút | phần BÁO CÁO (mục có `mong` ĐẠT/ĐỎ, kể cả 3 mục quyền của SA: đọc đúng 3 bí mật app · 0 bí mật quản trị · gán/gỡ không lỗi — chạy lại 01 sẽ GỠ quyền thừa nếu có) — cần `KẾT: ĐẠT` mới sang 02 |
| **02** di trú + phân quyền | `bash tools/staging/02_di_tru_phan_quyen.sh --project P --kiem` rồi bỏ `--kiem` | ~1 phút (đo cục bộ: ~3 giây; thêm tạo venv + pip `psycopg` lần đầu ~1 phút, proxy + mạng) | phần BÁO CÁO (mục có `mong`: `fls_itl` chỉ-THÊM · `fls_doc` chỉ SELECT · `pg_verify: khop`…) |
| **03** ảnh + VM chạy app | `bash tools/staging/03_dung_app.sh --project P --kiem` rồi bỏ `--kiem`. Mặc định app **CHỈ ĐỌC**. Muốn người test KÝ: thêm `--che-do ghi --nguoi-ky <tên>`; cấp người vào: `--cap-quyen a@x.com,b@y.com` | Cloud Build **3–6 phút** (đo cục bộ: `docker build` 5 giây khi có cache, ảnh **373 MB**); VM tạo **~1 phút**, boot + cài docker + kéo ảnh **2–4 phút** ⇒ chờ rồi chạy lại `--kiem` để đo | phần BÁO CÁO (19 mục, kể cả ĐO TRONG VM: container sống · cổng 8088 chỉ nghe `127.0.0.1` · gọi không thẻ ⇒ 401) |
| **04** nạp config IX.* đã ký | `FLS_CHO_GHI_THAT=1 bash tools/staging/04_nap_du_lieu.sh --project P --nguoi-nap <tên.người>` (`--kiem` để chỉ đo) | ~1 phút (đo cục bộ: 2 giây) | phần BÁO CÁO (9 bảng × hai chiều + riêng tư + `fls_itl = 0`) |
| **07** ⭐ LINK WEB sau Google IAP *(`WO-363`)* | `bash tools/staging/07_link_web.sh --project P --kiem` *(trước: mong ĐỎ — chưa có service)* rồi bỏ `--kiem`; cho người test: `--cho-vao a@x.com,b@y.com` *(chạy lại được, ⛔ cần ngay)*; muốn KÝ qua link: `--che-do ghi --nguoi-ky <tên>` | dùng lại ảnh nếu tag đã có; chưa có ⇒ Cloud Build **3–6 phút** như 03; `run deploy` ~1–2 phút *(⛔ đo được ở GCP)*; nhật ký `TU_DO` có thể trễ ~1 phút ⇒ chạy lại `--kiem` | phần BÁO CÁO (**26** mục có `mong` khi dựng · 25 khi `--kiem`: IAP bật · 0 thành viên công khai · ⛔ cookie ⇒ 302 về Google / POST 401 · TRONG container: cửa chỉ nghe 127.0.0.1, cổng chặn yêu cầu ⛔ IAP và JWT giả) + dòng **`⭐ LINK:`** |
| **UAT** người test | `docs/ITL/04_Test/UAT_STAGING_E2E.md` — 13 bước, bảng số từ `hd2_cong.json` | ~1–2 giờ/người | bảng đã điền (người test · ngày · ĐẠT/ĐỎ · ghi chú) |

## Mỗi bước: chạy ở đâu · chạy lại được không · gửi lại phần nào

- **Chạy ở**: Cloud Shell, bằng tài khoản **chủ project** (quyền admin). Bước 02/04 dùng Cloud SQL Auth Proxy chạy **trong chính Cloud Shell** (script tự bật/tắt); cần file chạy `cloud-sql-proxy` v2 (script chỉ cách tải nếu thiếu) — chỉ lần đầu.
- **Chạy lại được**: cả bốn bước đều idempotent ("có rồi ⇒ bỏ qua"); `--kiem` luôn CHỈ ĐỌC (bài thử: `--kiem` không đổi một quyền/vai nào).
- **Sau MỖI di trú mới** (migration thêm bảng): chạy lại **02** — bảng mới cố ý ⛔ tự có quyền cho `fls_ghi`/`fls_doc` (xem `sql/02b_phan_quyen.sql`); BÁO CÁO báo ĐỎ "bảng thiếu quyền" cho tới khi chạy.
- **Sau MỖI lần gộp mã mới** (vd H14/I2): chạy lại **03** (build ảnh mới theo `git archive HEAD`, VM tự khởi động lại kéo ảnh mới) và soát các bước UAT gắn `[CHỜ H14]`/`[CHỜ I2]`.
- **Tắt VM ngoài giờ test**: `gcloud compute instances stop fls-staging-app --zone asia-southeast1-b` (bật lại `start` — container tự lên, `--restart=always`).
- **Gửi lại**: dán từ dòng `── BÁO CÁO (KHÔNG chứa mật khẩu/khoá)` tới `══ chế độ: … · KẾT: …`. ⛔ gửi phần phía trên nếu bạn chạy với `bash -x` hay `set -x` (lộ mật khẩu) — script ⛔ bật, đừng bật.

## Người test vào bằng gì (⛔ địa chỉ công khai KHÔNG xác thực)

### ⭐ Đường chính từ 24/11 — LINK WEB sau Google IAP (bước 07, `WO-363`)

`07_link_web.sh` dựng service Cloud Run `fls-staging-web` từ **cùng ảnh** với VM, bật **IAP tích hợp của Cloud Run** (`--iap`, `--no-allow-unauthenticated`) và in URL `https://fls-staging-web-…run.app`. Người test mở URL ⇒ đăng nhập Google ⇒ màn hình FLS — **⛔ cần gcloud**. Chỉ tài khoản có `roles/iap.httpsResourceAccessor` trên service *(người chạy script + `--cho-vao`)* vào được; IAP chặn mọi lối vào kể cả `run.app` *(tài liệu GCP "Configure IAP for Cloud Run")*.

Trong container *(`tools/staging/app/vao_cloud_run.sh`)*: `vao.sh` **nguyên vẹn** ⇒ cửa vẫn nghe `127.0.0.1:8088` *(`GAP-WEB-01` ⛔ nới)*; thành phần DUY NHẤT nghe ngoài loopback là **`cong_iap.py`** trên `$PORT` — nó **kiểm chữ ký ES256** của header `X-Goog-IAP-JWT-Assertion` *(khoá công khai IAP; thiếu/sai ⇒ 403, ⛔ lấy được khoá ⇒ 503)*, gỡ mọi `X-Goog-*`, chuyển tiếp **nguyên** `Authorization` (thẻ FLS) vào cửa, và ghi nhật ký `IAP_VAO email=… GET /đường mã` *(chỉ để biết AI vào — `actor` của chữ ký vẫn là `--nguoi-ky`)*. Ngoài Cloud Run (⛔ `K_SERVICE`) nó **từ chối khởi động**.

Giới hạn đường link *(đo được từ mã)*: ① "chạy chuỗi" HD2 + `--ghi` vẫn là **lệnh trên VM** (⛔ HTTP) ⇒ F03 trên link đọc `hd2_cong.json` **đóng trong ảnh**, ⛔ thấy lần `--ghi` ở VM (UAT U10 xem qua tunnel) · ② `ky_ty_gia.py` (docker exec) chỉ ở VM; trên link ký tỷ giá bằng màn **F08** khi service ở chế độ `ghi` · ③ VM và link dùng **cùng** Cloud SQL ⇒ chữ ký ở bên nào cũng thấy ở bên kia · ④ `--max-instances 1` *(một thẻ chung, một tiến trình ghi)*. Tắt link: `gcloud run services delete fls-staging-web --region asia-southeast1` *(chủ tự gõ)*.

### Đường dự phòng — đường hầm SSH qua IAP (bước 03)

App nghe `127.0.0.1:8088` **trên VM**; cửa tự từ chối nghe ra ngoài (`GAP-WEB-01`). Mỗi người được cấp (`--cap-quyen`) `roles/compute.osLogin` + `roles/iap.tunnelResourceAccessor`, rồi:

```
gcloud compute ssh fls-staging-app --project P --zone asia-southeast1-b --tunnel-through-iap -- -N -L 8088:127.0.0.1:8088
# giữ cửa sổ mở → trình duyệt: http://localhost:8088/
```

⛔ **Cloud Shell Web Preview ⛔ dùng được cho màn hình FLS** *(chủ đo 23/11 ~10:50)*: tunnel từ Cloud Shell `-L 8080:127.0.0.1:8088` + Web Preview ⇒ vỏ màn hình tải được nhưng **mọi** `fetch` API ⇒ `FLS-MAT-KET-NOI / Failed to fetch`; cùng lúc `curl http://127.0.0.1:8080/api/fls/v1/gates` trong Cloud Shell ⇒ **401** *(app + API đúng)*. Nghi proxy `cloudshell.dev` chặn `fetch` mang `Authorization: Bearer` — **CHƯA đo nguyên nhân**. ⇒ Người test chạy tunnel **từ MÁY MÌNH**: cài Google Cloud CLI → `gcloud auth login` → lệnh trên → mở **http://localhost:8088/**.
Trên Cloud Shell, dòng `bind [::1]:8080: Cannot assign requested address` là **vô hại** *(IPv6; IPv4 vẫn nghe)*.

⚠ **Một thẻ chung cho cả phiên**: mọi chữ ký mang tên `--nguoi-ky` (cửa ⛔ có đăng nhập từng người; SSO là phase sau). ⛔ để mặc định — script từ chối tên `thu@apero.vn`.

## Dữ liệu nguồn (sổ kế toán) — ⛔ nạp ở đây

Bước 04 chỉ nạp **config** `IX.*`; `fls_itl` = 0 dòng. "Thật hay ẩn danh" là **câu chủ** (BG-326). Công cụ nạp nguồn sẵn có (`tools/nap_that.py`…) lấy token Google Sheets bằng một SA cục bộ gắn cứng trong mã ⇒ ⛔ chạy được ở Cloud Shell nếu chưa có phiếu bọc lại. `04 --nguon-that` luôn từ chối và nói vì sao.

## Chuỗi HD2 trong app

"Chạy chuỗi" là **lệnh**, ⛔ yêu cầu HTTP: `sudo docker exec fls-app bash /app/tools/staging/app/chay_chuoi.sh [--ghi]` (**11** gói `do_hd2.py --goi` = `len(GOI_BIET)`; đo 23/11 trên cây đã gộp H14: ~**45 giây** CPU, đỉnh **~800 MB** RAM trên kho đã nạp config). ⛔ **Chỉ CHỦ chạy**: lệnh cần `sudo`, mà `--cap-quyen` chỉ cấp `osLogin` (không có `sudo`) — cấp `osAdminLogin` là cho người test root trên VM (`STG-R1-06`, phương án A). **D1 (I2)**: gói đọc tỷ giá TỪ KHO ⇒ chạy chuỗi khi chưa ký tỷ giá ra **11/11 ĐỎ `FX_CHAN`** — ĐÚNG; người ký ký các tháng bằng `docker exec fls-app python /app/tools/staging/app/ky_ty_gia.py --cong 8088` *(app ở chế độ `ghi`; tuyến `POST /config/fx/{yyyymm}/sign`, tên ký lấy từ thẻ; bỏ qua tháng LẠC)* rồi mới chạy chuỗi ⇒ **11/11 ĐẠT** *(UAT v0.3 · U7–U9)*. `--ghi` ghi lại `hd2_cong.json` trong container — cửa đọc nó mỗi yêu cầu nên F03 đổi ngay.

## Giả định chưa kiểm (chỉ lộ ra khi chạy thật ở GCP)

| # | Giả định | Nếu sai, BÁO CÁO nào ĐỎ |
|---|---|---|
| 1 | `postgres` (Cloud SQL) `GRANT fls_admin TO postgres` + `ALTER DATABASE … OWNER TO fls_admin` được | 02: dừng ở bước ② với lỗi PG (script ⛔ che) |
| 2 | ~~gỡ `cloudsqlsuperuser` + `NOCREATEROLE NOCREATEDB` khỏi `fls_ghi`/`fls_doc` được (làm-hết-sức)~~ — **ĐÃ KIỂM 23/11: SAI** *(02 thật: 23/24, ĐỎ "siêu quyền … = 2")* ⇒ thay bằng #8 (`STG-R2b-02`) | 02: mục "thành viên cloudsqlsuperuser" / "siêu quyền" |
| 3 | `cloud-sql-proxy` v2 chạy được trong Cloud Shell, VM có đường ra tới IP công khai của Cloud SQL (IP tạm của VM) | 02/04: "proxy ⛔ lên cổng"; 03 TRONG VM: container ⛔ chạy |
| 4 | Debian 12 cài `docker.io` bằng `apt` lúc boot (VM có đường ra internet) — **ĐÃ KIỂM 23/11: ĐÚNG** *(bước 03 23/23 ĐẠT sau vá tạm — orchestrator báo)* | 03 TRONG VM: "container fls-app" |
| 5 | vai IAM `roles/iap.tunnelResourceAccessor` (cấp ở project) + `roles/compute.osLogin` (cấp ở VM) đủ để `ssh --tunnel-through-iap` | người test ⛔ vào được (U1) |
| 6 | `gcloud compute ssh --tunnel-through-iap --command` chạy được từ Cloud Shell của chủ — **ĐÃ KIỂM 23/11: ĐÚNG** *(bước 03 23/23 ĐẠT sau vá tạm — orchestrator báo)* | 03 mục "TRONG VM" đỏ cả 5 |
| 7 | mạng `default` của project cho phép luật firewall ưu tiên 800/900 như script đặt | 03 mục firewall |
| 8 | `postgres` (Cloud SQL PG16) chạy được `CREATE ROLE … LOGIN NOCREATEDB NOCREATEROLE PASSWORD '…'` và `DROP ROLE` vai **chính nó tạo**; vai gcloud tạo thì `DROP ROLE` SQL được (giả thuyết H-B — khớp mọi sự thật đo) **hoặc** bị từ chối ⇒ `gcloud sql users delete` (H-A). Script IN lời PG thật + dòng `có ADMIN OPTION=` ⇒ lần chạy đầu phân xử | 02: dừng ở ①b với lỗi CÓ TÊN `VAI_KHONG_XOA_DUOC` / `VAI_KHONG_TAO_DUOC` |
| 9 | `gcloud builds submit` ⛔ `.gcloudignore` + ngữ cảnh ⛔ `.gitignore` ⇒ tải **đủ** ngữ cảnh; gcloud in `Creating temporary archive of N file(s)` | 03: mục "tệp tải lên = tệp ngữ cảnh" (⛔ đọc được dòng ⇒ ĐỎ) |
| 10 | **G-1** IAP cho qua yêu cầu mang `Authorization: Bearer <thẻ FLS>` khi trình duyệt ĐÃ có cookie IAP *(FAQ IAP: yêu cầu có cookie IAP = "browser request"; IAP xác thực với Cloud Run bằng `X-Serverless-Authorization`, ⛔ `Authorization`)* — **chưa đo** | UAT **U1**: màn hiện mà mọi ô dữ liệu lỗi 401 *(`FLS-TRA-LOI-LA`)* ⇒ dùng tunnel; sửa = màn gửi thẻ ở header khác (WO mới) |
| 11 | **G-2** `gcloud run deploy --iap` có ở bản GA *(tài liệu hiện hành ⛔ ghi `beta`)*; GA ⛔ biết ⇒ script tự thử `gcloud beta` | 07: `gcloud run deploy (exit)` |
| 12 | **G-3** `gcloud run services describe --format=json` mang chú thích `run.googleapis.com/iap-enabled: "true"` *(nguồn: blog bên thứ ba; tài liệu Google chỉ nói "Iap Enabled: true")* | 07: mục "IAP bật trên service" ĐỎ dù console báo bật ⇒ gửi `gcloud run services describe fls-staging-web --region asia-southeast1 --format=export \| grep -i iap` |
| 13 | **G-5** mỗi lần deploy Cloud Run khởi động MỘT instance để kiểm revision ⇒ có dòng `TU_DO` mà ⛔ cần ai mở link | 07: mục "TRONG container · dòng TU_DO …" ĐỎ ⇒ mở link một lần rồi `--kiem` |
| 14 | **G-6** IAP, ⛔ cookie: `GET` ⇒ 302 về trang Google · `POST` ⇒ 401 *(FAQ IAP)* | 07: 3 mục `NGOÀI · …` (máy chủ chuyển tới in ở dòng thông tin) |
| 15 | **G-7** project `fp-a-project` thuộc một **tổ chức** Google ⇒ IAP dùng OAuth client do Google quản lý, **chỉ người TRONG tổ chức** đăng nhập được. Người test ngoài tổ chức *(gmail…)* cần **OAuth consent screen "External" + OAuth client riêng** *(console — ⛔ tạo bằng lệnh được, tài liệu GCP)* | kiểm: `gcloud projects describe fp-a-project --format='value(parent.type)'` = `organization`; người ngoài bị Google từ chối ở U1 |
| 16 | **G-8** container Cloud Run ra được Internet tới IP công khai Cloud SQL (Auth Proxy trong ảnh, như VM) và tới khoá IAP `www.gstatic.com` | 07: `TRONG · màn hình …` (cửa chỉ lên khi nối được kho — `kiem_truoc_khi_mo`) · `TRONG · khoá công khai IAP …` |
