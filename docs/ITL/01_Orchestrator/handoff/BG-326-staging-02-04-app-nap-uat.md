# BG-326 — bàn giao `WO-325` *(STAGING bước 02 · 03 · 04 + kịch bản test e2e bằng người)*

| | |
|---|---|
| **Thuộc** | `WO-325` |
| **Phát bởi** | `fls-dev` làn **HẠ TẦNG** · phiên cloud Sonnet 5.5 · cụm PG **5437** · 2026-11-23 |
| **Nhận** | `fls-test` *(R1 → `KQ-327`, R2 cuối → `KQ-328`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/STG` @ `@@SHA@@` *(đã đẩy)* |
| **Kho thật** | `KHONG_CHAM` — ⛔ vào GCP · ⛔ gcloud thật · ⛔ ghi kho thật. Mọi phép ghi chạy trên kho scratch `fls_stg_*` của cụm PG phiên (dọn xong), `fls`/`fls_test` ⛔ chạm ngoài bộ pytest thường lệ |

## Kết luận một dòng
Bước **02 · 03 · 04** + `Dockerfile` + kịch bản UAT + README trình tự **xong và chứng minh ĐỎ-khi-hỏng** *(93 bài mới ở `tests/staging/`; gcloud + cloud-sql-proxy GIẢ, `psql` · `pg_migrate` · quyền PostgreSQL THẬT)*. ⛔ **chưa chạy thật ở GCP** — bảy giả định về chính GCP ở `tools/staging/README.md` §"Giả định chưa kiểm". **Khuyến nghị nơi chạy app: VM + IAP SSH tunnel** (đo bên dưới); **bốn câu chủ ở §4 — ⛔ tự quyết.** Bảy phát hiện ngoài dự kiến ở §5, trong đó hai cái đổi thiết kế: `actor` mặc định `thu@apero.vn` và "chuỗi HD2 3–5 phút" thật ra ~28 giây.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/staging/02_di_tru_phan_quyen.sh` + `sql/02a_quan_tri.sql` + `sql/02b_phan_quyen.sql` | AC-1: Auth Proxy → đổi chủ kho sang `fls_admin` · `pg_migrate` · `GRANT`/`REVOKE` · BÁO CÁO có `mong` |
| `Dockerfile` · `.dockerignore` · `.gcloudignore` | AC-2: ảnh cửa API + màn hình; **danh sách cho phép** (`*` rồi `!fls` `!tools` `!docs/ITL/_tools` `!tests/fixture`) |
| `tools/staging/app/vao.sh` · `lay_bi_mat.py` · `chay_chuoi.sh` | AC-2/4: điểm vào của ảnh (bí mật từ Secret Manager qua metadata → Auth Proxy → `tools/chay_cua.py --cho-web`); lệnh "chạy chuỗi" HD2 trong container |
| `tools/staging/03_dung_app.sh` · `vm_khoi_dong.sh` | AC-2: Artifact Registry · Cloud Build (`git archive`) · firewall · VM · `--cap-quyen` · BÁO CÁO kể cả đo TRONG VM qua IAP |
| `tools/staging/nap_cau_hinh_ix.py` · `04_nap_du_lieu.sh` | AC-3: trình ĐIỀU PHỐI mỏng gọi các hàm `cau_hinh_repo.nap_*` **sẵn có** (⛔ viết lại) + script bọc |
| `docs/ITL/04_Test/UAT_STAGING_E2E.md` | AC-4: 13 bước người bấm · bảng số 13 hàng từ `hd2_cong.json` · giới hạn O6 |
| `tools/staging/README.md` | AC-5: trình tự 01 → 02 → 03 → 04 → UAT, mỗi bước chạy ở đâu · bao lâu · gửi lại gì · giả định chưa kiểm |
| `tests/staging/*` *(7 tệp)* | 93 bài (xem §2) |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | AC-6: `MONG_PYTEST_TOAN_BO` **4772 → 4865** + bài ghim cùng commit *(đo `pytest --collect-only` = 4865; chứng ĐỎ: để 4772 ⇒ `test_S0_R3_02` đỏ "≠ thu thập 4865 (301 tệp)")* |
| `docs/ITL/03_Dev/06_CICD_PIPELINE.md` (v0.2) · `08_CHANGELOG_RELEASE.md` | hai ô `???` staging có thiết kế; nhật ký |

⛔ **Không sửa**: `fls/**` (0 tệp — Đ1: `git diff 25ab19f -- fls | wc -l` = 0) · `tools/chay_cua.py` · bảng tuyến · luật từ chối của cửa.

@@CONG@@

## 2 · Bằng chứng từng AC
| AC | Mong | Bằng chứng của Dev *(số đo thật, nhãn đếm gì — Đ4)* |
|---|---|---|
@@AC@@

## 3 · Khuyến nghị nơi chạy app — ĐO trước rồi mới khuyến nghị

**Điều kiện cứng đo được từ mã** *(chia khoá cho mọi phương án)*:
- `tools/chay_cua.py --cho-web` **TỪ CHỐI** nghe ngoài loopback: `fls/api/cua.py:369 kiem_phuc_vu_tep` ⇒ `RuntimeError "⛔ dia chi '0.0.0.0' ⛔ khong phai loopback … (GAP-WEB-01)"` *(bài `test_cua_van_TU_CHOI…` đo trên tiến trình thật: exit ≠ 0 + tên `GAP-WEB-01`)*. Vì vỏ màn hình ra TRƯỚC thẻ và `phien.js` phát **một** thẻ `ke_toan` chung — nghe ra mạng là phát thẻ cho người lạ.
- ⇒ **hàng rào truy cập phải nằm NGOÀI ứng dụng** và ứng dụng giữ nghe `127.0.0.1`. `WO` cấm nới luật này.

**Đo ở máy dev** *(container thật `docker run --network host`; kho scratch đã qua 02; ⛔ số GCP — không vào GCP)*:

| Đo | Kết quả | Dùng để |
|---|---|---|
| Ảnh `docker build` | `373 MB` *(`docker images`)*; build 5 giây khi có cache; ⛔ có `sao_luu/` `hien_vat/` `Input_Raw/` `.env*` trong `/app` *(đếm 0)*; chạy `USER fls` *(uid 10001)* | cỡ Artifact Registry; an toàn dữ liệu |
| Khởi động → mở cổng | **1,7 giây** *(từ `docker run -d` tới nối được `127.0.0.1:8088`)* | cold start Cloud Run **không** là rào cản về thời gian |
| RAM nghỉ | **31 MiB** · 3 PID · CPU 0,02 % *(`docker stats`, kho rỗng — ⚠ số trên kho có dữ liệu chưa đo)* | cỡ máy |
| Độ trễ yêu cầu | `GET /` 8 ms · `GET /gates` không thẻ ⇒ **401** 2 ms · có thẻ ⇒ 200 15 ms · `GET /ledger` 12 ms *(kho rỗng)* | giới hạn thời gian yêu cầu |
| **Chuỗi HD2** *(10 gói `do_hd2.py --goi`, kho đã nạp config bước 04)* | **tổng 27,8 giây**; từng gói *(giây · đỉnh RSS MB)*: C2 0,3·62 · C3a 1,2·204 · C3b 1,3·157 · C3c 0,7·137 · **C3d 7,7·628** · C4a 0,3·46 · C4b 0,3·54 · C4c 0,6·123 · **C5a 7,5·630** · **C5b 7,9·630**; 10/10 `KẾT: ĐẠT` | ⚠ **sửa giả thiết của WO**: "~3–5 phút" ⇒ **~28 giây CPU**; và chuỗi là **LỆNH** (`do_hd2.py`), ⛔ yêu cầu HTTP ⇒ ⛔ có giới hạn thời gian yêu cầu của cửa/Cloud Run dính vào |
| Chuỗi khi kho TRẮNG | 7+ gói thoát ≠ 0 với `ChuaKhai: ⛔ bang='IX.…' ⛔ CHƯA có phiên bản nào trong kho config` *(đo: C3c · C3d · C4a · C4b · C4c · C5a · C5b)* | bước 04 **bắt buộc** trước khi "chạy chuỗi" |

**So sánh** *(chi phí = ⚠ ƯỚC từ bảng giá công khai, ⛔ đo được ở đây; chủ kiểm Billing / Pricing Calculator)*:

| | **A · VM Compute Engine + IAP SSH tunnel** *(đã dựng — khuyến nghị)* | B · Cloud Run (service) |
|---|---|---|
| Cỡ máy theo số đo | `e2-small` (2 vCPU chia sẻ · 2 GB): đỉnh chuỗi 630 MB + Docker + hệ điều hành còn dư. `e2-micro` (1 GB) sát — ⛔ chọn | 1 vCPU · 1 GiB là đủ cho đỉnh 630 MB nếu chuỗi chạy bằng **Job** riêng |
| Chi phí/tháng *(⚠ ước)* | VM 24/7 ≈ **15–18 USD** + đĩa 20 GB ≈ **2–3** + IP tạm ≈ **3** ⇒ **~20–24 USD** *(+ Cloud SQL 50–60 đã có)*. **Tắt VM ngoài giờ test ⇒ ≈ 2–3 USD** (đĩa) | scale-về-0 ≈ **0–3 USD**; luôn bật (1 vCPU luôn cấp CPU) ≈ **45+ USD** |
| Cách người test vào | `gcloud compute ssh … --tunnel-through-iap -- -N -L 8088:127.0.0.1:8088` → `http://localhost:8088`; IAM: `osLogin` (VM) + `iap.tunnelResourceAccessor`; có nhật ký ai mở tunnel. **Cần `gcloud` trên máy người test** | `gcloud run services proxy` (cần `run.invoker`) **hoặc** URL công khai sau IAP. **Cả hai ⛔ chạm được loopback của app** |
| Cửa vẫn nghe loopback? | **CÓ** — container `--network host`, cổng `127.0.0.1:8088`; SSH forward đáp vào loopback của VM | **KHÔNG** — Cloud Run đòi nghe `0.0.0.0:$PORT` ⇒ phải **nới luật từ chối** *(⛔ WO)* hoặc thêm một **proxy sidecar tự viết** đứng ngay chỗ ranh giới an ninh |
| Cloud SQL | Auth Proxy trong container + SA `fls-staging-app` (`cloudsql.client`) — *đã đo cục bộ* | Cloud SQL connector kèm Cloud Run (sidecar proxy cũng được) |
| Giới hạn thời gian yêu cầu của chuỗi | **không áp dụng** (chuỗi là lệnh `docker exec`, 28 giây) | không áp dụng nếu chuỗi chạy Job; mặc định 300 s/yêu cầu nếu ai nhét vào HTTP |
| Chạy chuỗi / `--ghi` hd2_cong.json | `docker exec` tại VM (người test có `osLogin`) | cần Cloud Run Job + volume cho tệp ghi lại (hd2_cong.json nằm FS tạm của instance) |
| Rủi ro lớn nhất | một VM = một điểm hỏng; phải tự `stop`/`start` | **sidecar tự viết trong đường an ninh**; mất `hd2_cong.json` khi instance tái chế |

⇒ **Khuyến nghị: A** — duy nhất giữ NGUYÊN luật loopback, danh tính = IAM *(có nhật ký)*, chuỗi chạy cùng chỗ, và chi phí tắt-được. Phương án B rẻ hơn khi bỏ không, nhưng buộc nới/chèn thứ vào ranh giới an ninh mà `WO` cấm.

## 4 · CÂU CHỦ — ⛔ Dev ⛔ tự quyết *(mỗi câu hai phương án + khuyến nghị)*

| # | Câu | Phương án **A** | Phương án **B** | Khuyến nghị |
|---|---|---|---|---|
| **C1** | **Nơi chạy app** | VM `e2-small` + IAP SSH tunnel *(đã dựng, §3)*: ~20–24 USD/tháng bật 24/7, ~3 khi tắt ngoài giờ; giữ luật loopback | Cloud Run + sidecar proxy/IAM: ~0–3 USD khi bỏ không; **phải viết thêm proxy sidecar** hoặc nới luật cửa *(⛔ WO)* | **A** |
| **C2** | **Cách người test vào** | Mỗi người tự mở IAP tunnel: cần cài `gcloud`, tài khoản Google được cấp `osLogin` + `iap.tunnelResourceAccessor` *(`--cap-quyen`)* — độc lập, có nhật ký | "Người cầm lái": một người (chủ) mở tunnel + chia sẻ màn hình; ⛔ cấp IAM cho ai khác — nhanh, nhưng người test ⛔ tự thao tác, ⛔ test song song | **A** nếu ≤ 5 người; **B** chỉ cho buổi thử đầu |
| **C3** | **Dữ liệu: thật hay ẩn danh** | **Ẩn danh** — ⛔ tiền/tên thật lên VM: cần **một WO mới** viết bộ ẩn danh xác định (đổi tên người/TK/Số CT, giữ cấu trúc + tổng) trước khi nạp sổ; trong lúc chờ UAT chạy với **config + sổ rỗng** *(chuỗi HD2 + F03 + ký tỷ giá đủ chạy — đã chứng)* | **Thật** — 1.214 tỷ + tên người trên VM staging: cần chủ ký chấp nhận rủi ro + một WO bọc công cụ nạp nguồn *(`tools/nap_that.py` đòi token Sheets bằng SA cục bộ gắn cứng — ⛔ khoá SA lên Cloud Shell)* + xoá khi xong | **A** (ẩn danh) |
| **C4** | **Ai test** | **Hai người**: một **người ký** *(tên `--nguoi-ky` đứng sau MỌI chữ ký — cửa phát thẻ chung `GAP-WEB-01`)* + một **người soát** chỉ đọc *(chế độ `doc`)* | **Cả nhóm (≥ 3)** mỗi người một lượt, dựng lại app đổi `--nguoi-ky` mỗi lượt (3 lần reset VM) hoặc chấp nhận chữ ký mang tên một người | **A** — vì thẻ chung, ≥ 2 người ký cùng phiên là chữ ký GIẢ |
| *(phụ)* **C5** | Chế độ app khi người ký thử | `doc` suốt UAT; chỉ bật `ghi` khi tới bước U5 *(1 lệnh: `03 --che-do ghi --nguoi-ky <tên>`, reset VM ~3 phút)* | `ghi` ngay từ đầu | **A** *(hẹp nhất: ghi mở = sửa số THẬT của staging)* |

## 5 · Phát hiện *(đo, ⛔ giả định — Đ1: đo ở CẢ HAI nơi)*
| # | Phát hiện | Đo | Hệ quả |
|---|---|---|---|
| 1 | **`actor` mặc định của cửa là `thu@apero.vn`** *(`danh_muc_actor.ACTOR_CHAY_CUA`)* — thẻ phát cho cả phiên ⇒ mọi chữ ký người test mang tên một người thật | `POST /config/fx/202401/sign` trả `"actor": "thu@apero.vn"`; kho: `SELECT actor FROM fls_cau_hinh_ban WHERE bang = 'IX.FX · KY'` = `thu@apero.vn` | **Đã vá ở bước 03**: `--nguoi-ky` + `FLS_STG_ACTOR` → `chay_cua.py --actor`; chế độ `ghi` **đòi** biến; từ chối `thu@apero.vn`; bài đo chữ ký mang `tester.mot` *(ở API và ở cột `actor` của kho)* |
| 2 | **Không có CLI nạp config `IX.*`** — chỉ có hàm `cau_hinh_repo.nap_*`; bài `tests/oracle/` tự ghép | `grep -rn "nap_ix_\|ky_bat_ix_alr" tools --include=*.py` (không kể `tools/staging/`) = **0 lời gọi** — chỉ 3 dòng chú thích ở `tools/do_hd2_c5a.py:18,78,88`; 7/7 gói HD2 cần kho đều dừng `ChuaKhai` trên kho trắng | `nap_cau_hinh_ix.py` (điều phối mỏng; 9 bảng, 10 phiên bản, 1.135 dòng của các bản mới nhất) + bài khoá `mong` hai chiều |
| 3 | **"Chuỗi HD2 ~3–5 phút" ⇒ ~28 giây** và là **lệnh** | §3 bảng đo | không cần Cloud Run Job/timeout đặc biệt |
| 4 | **Cây `STG` chưa có H14 và I2**: `grep -rn "FxKho\|kiem_fx_thang" fls tools` = 0; `hd2_cong.json` mới tới `WP-C5b` ⇒ F03 có **4 thẻ** C2·C3·C4·C5 *(C5 = a+b)*, ⛔ `WP-C5c`/605/615 | đo | UAT gắn nhãn `[CHỜ H14]` `[CHỜ I2]`; **dựng lại ảnh (03) sau khi gộp**; chốt D1 (chưa ký tỷ giá ⇒ chuỗi 0/11) **chưa có** ở đây — U10 ghi rõ |
| 5 | **Bước "ký bản báo cáo" chưa làm được ở cây này**: bản chỉ được tạo bởi engine `dua_ban_ky` (luồng I2); `POST …/report/snapshot/202510/sign` ⇒ 404 *"kỳ 202510 chưa có bản báo cáo nào để ký"* | đo thật | U9 `[CHỜ I2]` |
| 6 | **Công cụ nạp nguồn lấy token Sheets bằng SA cục bộ gắn cứng** (`tools/nap_that.py` · `nap_mapping_master.py`: `gcloud auth print-access-token --account claude-code-access@…`) | đọc mã | ⛔ chạy ở Cloud Shell nếu ⛔ khoá SA ⇒ `04 --nguon-that` luôn từ chối + nói lý do; chờ C3 |
| 7 | **`kiem_so_song.py`/`dong_bo_so_song.py` gọi `.venv/Scripts/lint-imports.exe`** *(đường Windows)* ⇒ `FileNotFoundError` trên Linux; và cả hai đòi **kho có sổ thật** | `tools/kiem_so_song.py:406`; sau khi đặt liên kết `.venv/Scripts/lint-imports.exe → ../bin/lint-imports`: "⛔ không đo được: kho ⛔ không có dấu thời điểm của lần nạp / ảnh chụp" | đỏ-có-sẵn của container (kho rỗng) — ⛔ do WO này |

## 6 · Kho thật
- `KHONG_CHAM`. Cụm PG phiên `localhost:5437`; bài thử tạo kho scratch `fls_stg_<pid>` + vai `fls_admin` `fls_ghi` `fls_doc` `stg_qt_<pid>` (+ `cloudsqlsuperuser` nếu cụm chưa có) và **dọn khi xong**. Đường lùi: `DROP DATABASE … WITH (FORCE)` + `DROP ROLE` đã nằm trong fixture.

## 7 · Cách chạy để xem
- Cục bộ, ĐÚNG đường chạy của ảnh: `docker build --secret id=pipca,src=<ca.crt> -t fls-app:thu .` *(secret chỉ cần khi mạng build đi qua proxy tự ký)*; chạy thử `docker run --network host -e FLS_STG_PROJECT=… -e FLS_STG_CONN=… -e FLS_STG_CHE_DO=doc …` cần máy chủ metadata/Secret Manager (bài `test_03_dung_app.py` dựng bản giả) — cổng `8088`, chế độ `chỉ đọc` (`ghi` đòi `FLS_STG_ACTOR`).
- Xem nhanh nhất: `pytest tests/staging` *(~2 phút)*.

## 8 · Dev tự thấy còn yếu *(Test soi chỗ này trước)*
1. ⛔ **Chưa chạy ở GCP.** Bảy giả định ở README §"Giả định chưa kiểm". Đáng lo nhất: **#1** `GRANT fls_admin TO postgres` + `ALTER DATABASE OWNER` trên Cloud SQL thật · **#3** VM đi ra tới IP công khai của Cloud SQL · **#6** `gcloud compute ssh --tunnel-through-iap --command` từ Cloud Shell.
2. **Tường GRANT, ⛔ tường `default_transaction_read_only`**: `fls_doc` có thể `SET default_transaction_read_only = off` trong phiên (đo: bài `test_quyen_THAT…` làm đúng việc ấy rồi vẫn bị `InsufficientPrivilege` ở INSERT/UPDATE/DELETE/TRUNCATE). `ALTER ROLE` chỉ là mặc định để cửa qua cổng `la_chi_doc` — đúng ý WO, nhưng ai đọc `ALTER ROLE` mà tưởng là hàng rào là sai.
3. **Thẻ chung + `actor` một tên** vẫn là `GAP-WEB-01`: ⛔ giải quyết ở đây — chỉ chặn tên sai. Hai người ký cùng phiên ⇒ cùng một `actor`.
4. **VM có IP tạm + firewall chặn vào** — an toàn nhờ luật `DENY` ưu tiên 900; nếu ai thêm luật `ALLOW` ưu tiên < 900 từ `0.0.0.0/0`, BÁO CÁO 03 báo ĐỎ *(đã chứng)* nhưng ⛔ tự gỡ.
5. **Không đo được kích thước/độ trễ trên kho CÓ dữ liệu** (kho staging rỗng, kho dev rỗng): RAM 31 MiB và độ trễ 8–15 ms là **kho rỗng**; chuỗi HD2 (28 giây · 630 MB) đo trên config thật nhưng **ảnh đáp án đóng băng**, ⛔ trên sổ nạp live.
6. **Bảng chi phí là ước** — ⛔ vào GCP để đo; `e2-small` chọn theo đỉnh RSS 630 MB (chưa có số trên staging).
7. `.dockerignore` kiểu danh sách cho phép + `git archive` chặn dữ liệu gitignore, nhưng `tests/fixture` (126 MB trong repo) **đã commit** và vào ảnh — đã quét PII ở các phiếu DT*, ⛔ quét lại ở đây (`quet_pii_repo` = 0 trên cây).
8. `02` BÁO CÁO "gỡ `cloudsqlsuperuser`/`NOCREATEROLE`" là **làm-hết-sức**: trên Cloud SQL thật có thể ⛔ được; khi đó BÁO CÁO đỏ **đúng hai mục ấy** — chủ gửi lại, ⛔ coi là lỗi script.
