# FLS staging — trình tự CHỦ chạy (01 → 02 → 03 → 04 → 05 → UAT)

> ⛔ **Claude KHÔNG vào GCP** (quyết chủ 20/11): mọi script ở đây do **chủ** chạy trong **Google Cloud Shell**; chủ gửi lại **chỉ phần `BÁO CÁO`** (từ dòng `── BÁO CÁO` tới hết).
> ⛔ **Chưa script nào chạy thật trên GCP** (đo 23/11). Mỗi script đã được thử với `gcloud` GIẢ + `cloud-sql-proxy` GIẢ + **`psql` · `pg_migrate` · quyền PostgreSQL THẬT** trên kho cục bộ (`tests/staging/`, 130 bài) — nên cú pháp, thứ tự, quyền và BÁO CÁO đã được chứng minh ĐỎ-khi-hỏng; còn những giả định về **chính GCP** ở §"Giả định chưa kiểm" bên dưới sẽ lộ ra ở BÁO CÁO thật.
> Nội dung gửi lại ⛔ chứa mật khẩu/khoá: BÁO CÁO chỉ có tên, cấu hình, số đếm (bài thử quét rò rỉ: 0 chỗ).

Chuẩn bị một lần. Dưới đây viết `P` = `<PROJECT_ID>` (staging thật: `fp-a-project`, instance `fls-staging`, `asia-southeast1`; bước 01 đã ĐẠT 12/12 ngày 23/11).

**Đưa mã lên Cloud Shell** — 02/03/04 cần cây mã (`fls/`, `tools/`, `tools/staging/sql/`, `requirements.txt`, `Dockerfile`, `tests/fixture/cau_hinh/`, và với 03 cả git để `git archive`), ⛔ chỉ mỗi một tệp `.sh`. Cách ngắn nhất, chọn một:
1. `git clone` repo vào `~/fls` rồi `git checkout claude/bold-galileo-zukpaf-isp/STG` (cần quyền đọc repo từ Cloud Shell) — **bắt buộc cho 03** (script đòi `git archive HEAD`).
2. Không có quyền clone: trên máy bạn `git archive --format=tar.gz -o fls.tar.gz HEAD`, **Upload** `fls.tar.gz` lên Cloud Shell, `mkdir ~/fls && tar -xzf fls.tar.gz -C ~/fls && cd ~/fls && git init -q && git add -A && git -c user.email=x -c user.name=x commit -qm snap` (đủ cho 02/04 và cho `git archive` của 03; ⛔ có `sao_luu/` `hien_vat/` vì `git archive` chỉ lấy tệp đã commit).
Script 01 chỉ cần chính nó (đã chạy xong). Script 02/04 tự tạo venv + `pip install psycopg` (cần mạng ra PyPI — Cloud Shell có).

| Bước | Lệnh (Cloud Shell) | Mất bao lâu *(ước — ⛔ đo được ở GCP)* | Gửi lại |
|---|---|---|---|
| **01** dựng Cloud SQL · 3 vai · bí mật · SA | `bash tools/staging/01_dung_staging_gcp.sh --project P --kiem` rồi bỏ `--kiem` | tạo máy Cloud SQL **5–15 phút** (script 01 tự ghi); còn lại < 2 phút | phần BÁO CÁO (12 mục) — cần `KẾT: ĐẠT` mới sang 02 |
| **02** di trú + phân quyền | `bash tools/staging/02_di_tru_phan_quyen.sh --project P --kiem` rồi bỏ `--kiem` | ~1 phút (đo cục bộ: ~3 giây; thêm tạo venv + pip `psycopg` lần đầu ~1 phút, proxy + mạng) | phần BÁO CÁO (27 mục: `fls_itl` chỉ-THÊM · `fls_doc` chỉ SELECT · `pg_verify: khop`…) |
| **03** ảnh + VM chạy app | `bash tools/staging/03_dung_app.sh --project P --kiem` rồi bỏ `--kiem`. Mặc định app **CHỈ ĐỌC**. Muốn người test KÝ: thêm `--che-do ghi --nguoi-ky <tên>`; cấp người vào: `--cap-quyen a@x.com,b@y.com` | Cloud Build **3–6 phút** (đo cục bộ: `docker build` 5 giây khi có cache, ảnh **373 MB**); VM tạo **~1 phút**, boot + cài docker + kéo ảnh **2–4 phút** ⇒ chờ rồi chạy lại `--kiem` để đo | phần BÁO CÁO (22 mục, kể cả ĐO TRONG VM: container sống · cổng 8088 chỉ nghe `127.0.0.1` · gọi không thẻ ⇒ 401) |
| **04** nạp config IX.* đã ký | `FLS_CHO_GHI_THAT=1 bash tools/staging/04_nap_du_lieu.sh --project P --nguoi-nap <tên.người>` (`--kiem` để chỉ đo) | ~1 phút (đo cục bộ: 2 giây) | phần BÁO CÁO (9 bảng × hai chiều + riêng tư + `fls_itl = 0`) |
| **05** nạp DỮ LIỆU NGUỒN THẬT *(quyết chủ 23/11: dữ liệu THẬT)* | `FLS_CHO_GHI_THAT=1 bash tools/staging/05_nap_nguon_that.sh --project P --nguoi-nap <tên.người> <CÁCH CẤP QUYỀN ĐỌC SHEET>` — `--kiem` để chỉ ĐỌC nguồn + in số đếm (⛔ ghi một dòng). Cách cấp quyền, chọn MỘT: `--sa-json-tep <tệp khoá SA đọc-sheet>` · `--adc` · `--token-gcloud` (§"Quyền đọc sheet" dưới) | 4 bước nạp, đo cục bộ: **sổ+PM ~1–2 phút** + chụp 60 sheet vài giây — ⚠ workbook nguồn "nguội" có thể chậm hơn (đo 23/11: lượt đọc tiêu đề đầu tiên 30 giây) | phần BÁO CÁO (số đếm nguồn · số đếm kho · CŨ ↔ HIỆN TẠI · riêng tư) — `KẾT: ĐẠT` hoặc ĐỎ **có tên** (⛔ ĐỎ không phải lỗi script: nó là tín hiệu về NGUỒN, xem BG-335) |
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

## Dữ liệu nguồn (sổ kế toán) — bước 05 `WO-334`

Quyết chủ 23/11: staging dùng **dữ liệu THẬT** (chủ chấp nhận rủi ro tên người + tiền thật). `05_nap_nguon_that.sh` điều phối `tools/staging/nap_nguon_that.py`, gọi **đúng các công cụ nạp sẵn có** theo thứ tự phụ thuộc:
① `nap_nguon_va_khai` (dòng chảy `R |` Bank + Quỹ + bản khai) → ② `nap_mapping_master` → ③ `nap_that.chay_that` (sổ `fls_itl` + `fls_reject` + PM `fls_pm_line`) → ④ `chup_sao_ke` (ảnh chụp các sheet `R |` của sổ Bank). Token Sheets đi qua `tools/staging/cred_sheets.py` (⛔ SA gắn cứng như trước).

### Quyền đọc sheet — chủ cấp MỘT trong ba cách (⛔ khoá trong repo/chat; ⛔ ghi sheet — `QĐ-ITL-34`)
| Cách | Lệnh | Ghi chú |
|---|---|---|
| `--sa-json-tep` | tải tệp khoá SA lên Cloud Shell, `chmod 600`, truyền đường dẫn; **xoá sau khi nạp** | SA phải được **chia sẻ "Người xem"** trên cả **ba** workbook: RAW `1md85t…` (sổ · PM · Mapping Master), sổ Bank `1zJA0M…`, sổ Quỹ **gốc** `1QSYSz…` (⛔ bản copy `1RmmkO…` — 403). Thiếu một ⇒ BÁO CÁO mục "HTTP đọc workbook …" ĐỎ **403** và phần dùng workbook đó DỪNG (phần khác vẫn chạy) |
| `--adc` | `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/spreadsheets.readonly,https://www.googleapis.com/auth/drive.metadata.readonly` | dùng tài khoản của chủ (phải xem được 3 workbook) hoặc SA gắn với máy |
| `--token-gcloud` | script tự gọi `gcloud auth print-access-token --scopes=…readonly` | token ~60 phút; hết ⇒ chạy lại (công cụ chạy lại được) |

### Đọc BÁO CÁO
- **Σ nguồn = Σ kho**: `mong` = số vừa đọc từ nguồn ở chính lượt này (đếm: dòng sheet · canon · loại · rỗng · PM · 68 dòng chảy · 60 sheet chụp). `fls_itl` chỉ-THÊM ⇒ chạy lại ⛔ nhân đôi; Σ so **sau** nạp.
- **NGUỒN SỬA SAU ẢNH** *(chủ quyết 23/11 ~07:25: **nguồn SỐNG là chuẩn cho mọi kỳ**, kể cả kỳ đã chốt)*: so nguồn sống với ảnh đóng băng `tests/fixture/pm_join.json` *(9.992 dòng bank-canon · 3.703 dòng PM)* và với số cũ theo kỳ `voi_so_luong.theo_ky[k].co` *(23 kỳ, in từng kỳ)* — khối có tên, **chỉ ĐẾM**, ⛔ ĐỎ, ⛔ chặn nạp.
- **ĐỐI CHIẾU KHO** `--doi-chieu` *(CHỈ ĐỌC; đòi `PG_DSN`)*: đọc nguồn sống rồi ĐẾM kho đã nạp — sổ L1 · PM · Mapping · dòng chảy · **từng** sheet chụp; kho nhiều hơn hay ít hơn nguồn đều ĐỎ ⇒ đổi một dòng nguồn sau nạp là ĐỎ.
- **Cổng đọc-đủ** của `nap_that` (sàn đo 27/08) ĐỎ ⇒ sổ ⛔ ghi một dòng nhưng nguồn vẫn được ĐO. ⛔ Hạ sàn để "cho qua": việc của BA/chủ, có bản khai.
- **Riêng tư**: `PM_COT_RIENG_TU = {"Email Address"}` ⛔ vào kho (BÁO CÁO đếm cột tên có "email" + khoá `Email Address` trong `fls_pm_line.tho`, kèm mẫu số). `Tên tài khoản` GIỮ (quyết 11/09). BÁO CÁO chỉ SỐ ĐẾM.
- **Ngoài phạm vi 05** *(`NAP-R1-06`, Đ1: `grep -rl nap_nguon_dai docs fls tools tests`)*: `tools/nap_nguon_dai.py` — bản khai THỨ HAI `Range_*` → `fls_nguon_dai` (7 tệp `fls/` dùng; tuyến `bang_tuyen` đọc). Sau 05 `fls_nguon_dai` = **0 dòng** ⇒ tuyến ấy rỗng, ĐÚNG; việc của backlog `NAP-BL-01` *(BG-335 §1)*.
- Hết nạp: `rm -f <tệp khoá SA>` nếu đã tải lên.

⚠ **Dùng `fls_ghi`** (đã được cấp INSERT trên `fls_itl`, ⛔ UPDATE/DELETE) — ⛔ cần vai khác. Hạn chế đã đo: **H1000 · nền tảng (CCR/Platform) · FPS không có công cụ nạp trong repo** (BG-335 AC-1) ⇒ bước 05 ⛔ nạp chúng.

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
