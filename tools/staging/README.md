# FLS staging — trình tự CHỦ chạy (01 → 02 → 03 → 04 → UAT)

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
| **01** dựng Cloud SQL · 3 vai · bí mật · SA | `bash tools/staging/01_dung_staging_gcp.sh --project P --kiem` rồi bỏ `--kiem` | tạo máy Cloud SQL **5–15 phút** (script 01 tự ghi); còn lại < 2 phút | phần BÁO CÁO (12 mục) — cần `KẾT: ĐẠT` mới sang 02 |
| **02** di trú + phân quyền | `bash tools/staging/02_di_tru_phan_quyen.sh --project P --kiem` rồi bỏ `--kiem` | ~1 phút (đo cục bộ: ~3 giây; thêm tạo venv + pip `psycopg` lần đầu ~1 phút, proxy + mạng) | phần BÁO CÁO (mục có `mong`: `fls_itl` chỉ-THÊM · `fls_doc` chỉ SELECT · `pg_verify: khop`…) |
| **03** ảnh + VM chạy app | `bash tools/staging/03_dung_app.sh --project P --kiem` rồi bỏ `--kiem`. Mặc định app **CHỈ ĐỌC**. Muốn người test KÝ: thêm `--che-do ghi --nguoi-ky <tên>`; cấp người vào: `--cap-quyen a@x.com,b@y.com` | Cloud Build **3–6 phút** (đo cục bộ: `docker build` 5 giây khi có cache, ảnh **373 MB**); VM tạo **~1 phút**, boot + cài docker + kéo ảnh **2–4 phút** ⇒ chờ rồi chạy lại `--kiem` để đo | phần BÁO CÁO (19 mục, kể cả ĐO TRONG VM: container sống · cổng 8088 chỉ nghe `127.0.0.1` · gọi không thẻ ⇒ 401) |
| **04** nạp config IX.* đã ký | `FLS_CHO_GHI_THAT=1 bash tools/staging/04_nap_du_lieu.sh --project P --nguoi-nap <tên.người>` (`--kiem` để chỉ đo) | ~1 phút (đo cục bộ: 2 giây) | phần BÁO CÁO (9 bảng × hai chiều + riêng tư + `fls_itl = 0`) |
| **UAT** người test | `docs/ITL/04_Test/UAT_STAGING_E2E.md` — 13 bước, bảng số từ `hd2_cong.json` | ~1–2 giờ/người | bảng đã điền (người test · ngày · ĐẠT/ĐỎ · ghi chú) |

## Mỗi bước: chạy ở đâu · chạy lại được không · gửi lại phần nào

- **Chạy ở**: Cloud Shell, bằng tài khoản **chủ project** (quyền admin). Bước 02/04 dùng Cloud SQL Auth Proxy chạy **trong chính Cloud Shell** (script tự bật/tắt); cần file chạy `cloud-sql-proxy` v2 (script chỉ cách tải nếu thiếu) — chỉ lần đầu.
- **Chạy lại được**: cả bốn bước đều idempotent ("có rồi ⇒ bỏ qua"); `--kiem` luôn CHỈ ĐỌC (bài thử: `--kiem` không đổi một quyền/vai nào).
- **Sau MỖI di trú mới** (migration thêm bảng): chạy lại **02** — bảng mới cố ý ⛔ tự có quyền cho `fls_ghi`/`fls_doc` (xem `sql/02b_phan_quyen.sql`); BÁO CÁO báo ĐỎ "bảng thiếu quyền" cho tới khi chạy.
- **Sau MỖI lần gộp mã mới** (vd H14/I2): chạy lại **03** (build ảnh mới theo `git archive HEAD`, VM tự khởi động lại kéo ảnh mới) và soát các bước UAT gắn `[CHỜ H14]`/`[CHỜ I2]`.
- **Tắt VM ngoài giờ test**: `gcloud compute instances stop fls-staging-app --zone asia-southeast1-b` (bật lại `start` — container tự lên, `--restart=always`).
- **Gửi lại**: dán từ dòng `── BÁO CÁO (KHÔNG chứa mật khẩu/khoá)` tới `══ chế độ: … · KẾT: …`. ⛔ gửi phần phía trên nếu bạn chạy với `bash -x` hay `set -x` (lộ mật khẩu) — script ⛔ bật, đừng bật.

## Người test vào bằng gì (⛔ địa chỉ công khai)

App nghe `127.0.0.1:8088` **trên VM**; cửa tự từ chối nghe ra ngoài (`GAP-WEB-01`). Mỗi người được cấp (`--cap-quyen`) `roles/compute.osLogin` + `roles/iap.tunnelResourceAccessor`, rồi:

```
gcloud compute ssh fls-staging-app --project P --zone asia-southeast1-b --tunnel-through-iap -- -N -L 8088:127.0.0.1:8088
# giữ cửa sổ mở → trình duyệt: http://localhost:8088/
```

⚠ **Một thẻ chung cho cả phiên**: mọi chữ ký mang tên `--nguoi-ky` (cửa ⛔ có đăng nhập từng người; SSO là phase sau). ⛔ để mặc định — script từ chối tên `thu@apero.vn`.

## Dữ liệu nguồn (sổ kế toán) — ⛔ nạp ở đây

Bước 04 chỉ nạp **config** `IX.*`; `fls_itl` = 0 dòng. "Thật hay ẩn danh" là **câu chủ** (BG-326). Công cụ nạp nguồn sẵn có (`tools/nap_that.py`…) lấy token Google Sheets bằng một SA cục bộ gắn cứng trong mã ⇒ ⛔ chạy được ở Cloud Shell nếu chưa có phiếu bọc lại. `04 --nguon-that` luôn từ chối và nói vì sao.

## Chuỗi HD2 trong app

"Chạy chuỗi" là **lệnh**, ⛔ yêu cầu HTTP: `docker exec fls-app bash /app/tools/staging/app/chay_chuoi.sh [--ghi]` (10 gói `do_hd2.py --goi`; đo 23/11 ~**28 giây** CPU, đỉnh **630 MB** RAM trên kho đã nạp config). `--ghi` ghi lại `hd2_cong.json` trong container — cửa đọc nó mỗi yêu cầu nên F03 đổi ngay.

## Giả định chưa kiểm (chỉ lộ ra khi chạy thật ở GCP)

| # | Giả định | Nếu sai, BÁO CÁO nào ĐỎ |
|---|---|---|
| 1 | `postgres` (Cloud SQL) `GRANT fls_admin TO postgres` + `ALTER DATABASE … OWNER TO fls_admin` được | 02: dừng ở bước ② với lỗi PG (script ⛔ che) |
| 2 | gỡ `cloudsqlsuperuser` + `NOCREATEROLE NOCREATEDB` khỏi `fls_ghi`/`fls_doc` được (làm-hết-sức) | 02: mục "thành viên cloudsqlsuperuser" / "siêu quyền" |
| 3 | `cloud-sql-proxy` v2 chạy được trong Cloud Shell, VM có đường ra tới IP công khai của Cloud SQL (IP tạm của VM) | 02/04: "proxy ⛔ lên cổng"; 03 TRONG VM: container ⛔ chạy |
| 4 | Debian 12 cài `docker.io` bằng `apt` lúc boot (VM có đường ra internet) | 03 TRONG VM: "container fls-app" |
| 5 | vai IAM `roles/iap.tunnelResourceAccessor` (cấp ở project) + `roles/compute.osLogin` (cấp ở VM) đủ để `ssh --tunnel-through-iap` | người test ⛔ vào được (U1) |
| 6 | `gcloud compute ssh --tunnel-through-iap --command` chạy được từ Cloud Shell của chủ | 03 mục "TRONG VM" đỏ cả 5 |
| 7 | mạng `default` của project cho phép luật firewall ưu tiên 800/900 như script đặt | 03 mục firewall |
