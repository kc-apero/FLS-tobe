# BG-326 — bàn giao `WO-325` *(STAGING bước 02 · 03 · 04 + kịch bản test e2e bằng người)*

| | |
|---|---|
| **Thuộc** | `WO-325` |
| **Phát bởi** | `fls-dev` làn **HẠ TẦNG** · phiên cloud Sonnet 5.5 · cụm PG **5437** · 2026-11-23 |
| **Nhận** | `fls-test` *(R1 → `KQ-327`, R2 cuối → `KQ-328`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/STG` @ `65ab287` *(mã + bài + tài liệu; commit kế tiếp chỉ thêm phiếu này)* — đã đẩy |
| **Kho thật** | `KHONG_CHAM` — ⛔ vào GCP · ⛔ gcloud thật · ⛔ ghi kho thật. Mọi phép ghi chạy trên kho scratch `fls_stg_*` của cụm PG phiên (dọn xong), `fls`/`fls_test` ⛔ chạm ngoài bộ pytest thường lệ |

## Kết luận một dòng
Bước **02 · 03 · 04** + `Dockerfile` + kịch bản UAT + README trình tự **xong và chứng minh ĐỎ-khi-hỏng** *(96 bài mới ở `tests/staging/`; gcloud + cloud-sql-proxy GIẢ, `psql` · `pg_migrate` · quyền PostgreSQL THẬT)*. ⛔ **chưa chạy thật ở GCP** — bảy giả định về chính GCP ở `tools/staging/README.md` §"Giả định chưa kiểm". **Khuyến nghị nơi chạy app: VM + IAP SSH tunnel** (đo bên dưới); **bốn câu chủ ở §4 — ⛔ tự quyết.** Bảy phát hiện ngoài dự kiến ở §5, trong đó hai cái đổi thiết kế: `actor` mặc định `thu@apero.vn` và "chuỗi HD2 3–5 phút" thật ra ~28 giây.

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
| `tests/staging/*` *(8 tệp)* | 96 bài (xem §2) |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | AC-6: `MONG_PYTEST_TOAN_BO` **4772 → 4865** + bài ghim cùng commit *(đo `pytest --collect-only` = 4865; chứng ĐỎ: để 4772 ⇒ `test_S0_R3_02` đỏ "≠ thu thập 4865 (301 tệp)")* |
| `docs/ITL/03_Dev/06_CICD_PIPELINE.md` (v0.2) · `08_CHANGELOG_RELEASE.md` | hai ô `???` staging có thiết kế; nhật ký |

⛔ **Không sửa**: `fls/**` (0 tệp — Đ1: `git diff 25ab19f -- fls | wc -l` = 0) · `tools/chay_cua.py` · bảng tuyến · luật từ chối của cửa.

## 1 · Cổng *(kết quả nguyên văn — đỏ-có-sẵn ghi rõ)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` *(lần 1, trước khi vá hai bài ghim)* | `14 failed, 4835 passed, 2 xfailed, 14 errors in 1042.50s` — **12 failed + 14 errors + 2 xfailed = tập đỏ nền 28**; **2 đỏ MỚI do tôi, đã sửa**: `test_S0_R2_03` (script 4868 ↔ bài ghim 4865 lệch nhau lúc đang chạy) và `test_khong_file_test_nao_doc_PG_DSN_truc_tiep` (`tests/staging/ho_tro.py` đọc `PG_DSN` trực tiếp ⇒ đổi sang `fls.db.kho.dsn_that()`); chạy lại `tests/db/test_khong_ai_tro_lai_kho_that.py tests/test_dung_moi_truong_isp.py tests/staging` ⇒ `159 passed` |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5437` *(MỘT lần, một mình, trên SHA đã đẩy)* | **`KẾT: ĐẠT`** — toàn bộ: `28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 4868 bài (mong ≥ 4868) · skipped 0 · deselected 0`; `tests/web`: `3 = 3 · chạy 690 (mong ≥ 690)`; `lint-imports` 11 kept; di trú 27/27 + `pg_verify` khớp 27 bảng/view |
| `python tools/kiem_so_song.py` | ⛔ **ĐỎ-có-sẵn của container**: `…/.venv/Scripts/lint-imports.exe` (đường Windows ở `tools/kiem_so_song.py:406`) ⇒ `FileNotFoundError`; sau khi đặt liên kết `.venv/Scripts/lint-imports.exe → ../bin/lint-imports`: *"⛔ khong do duoc: kho ⛔ khong co dau thoi diem cua lan nap / anh chup — cong ⛔ khong duoc phep xanh"* (kho cục bộ rỗng; cần kho thật của chủ). ⛔ do WO này |
| `python tools/dong_bo_so_song.py --ghi` | cùng lý do `FileNotFoundError` (`Scripts/lint-imports.exe`); 0 tệp theo dõi bị đổi |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT … (485 file, 2961 bang, 968 o ngay, 104 ma QD)` · K1–K6 OK |
| `python docs/ITL/_tools/khop_owner.py --kiem` | ⛔ **ĐỎ-có-sẵn**: `A1 · B1 · C6 ⛔ DOI TRANG THAI` + `C5b ⛔ KHONG DO DUOC (so RONG)` — **chạy trên commit gốc `25ab19f` (git worktree) ra Y HỆT** ⇒ ⛔ do WO này (`TIEN_DO` 22/11 đã ghi B1·C6 là backlog) |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ ⛔ chạm schema (0 tệp `fls/db` đổi); `--duong-nen` đã chạy di trú + `pg_verify` khớp |
| `python tools/quet_pii_repo.py` | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |


## 2 · Bằng chứng từng AC
| AC | Mong | Bằng chứng của Dev *(số đo thật, nhãn đếm gì — Đ4)* |
|---|---|---|
| AC-1 · bước 02 | `pg_migrate` ⇒ `pg_verify: khop`; `fls_ghi` DML riêng `fls_itl` chỉ-THÊM; `fls_doc` SELECT + `read_only on`; BÁO CÁO có `mong`, exit 1 khi ĐỎ; chứng minh ĐỎ | `tests/staging/test_02_di_tru_phan_quyen.py` **28 bài** + `test_01_iam_lan_truyen.py` 3. ĐÚNG trên kho RỖNG ⇒ `KẾT: ĐẠT`, di trú **27/27** (= số tệp `migrations/*.sql`), `pg_verify: khop`; chạy lại ⇒ `khong co gi de ap`. **15 phá riêng từng mục ⇒ ĐÚNG tập mục ĐỎ** (vd `GRANT UPDATE ON fls_itl TO fls_ghi` ⇒ đúng 2 mục; hạ `default_transaction_read_only` ⇒ đúng 3; mất luật DENY ⇒ 2). Kho rỗng ⇒ ĐỎ (Đ3); `psql` + `python` GIẢ hỏng ⇒ **0 mục ĐẠT** (Đ5). Đo ĐỘC LẬP bằng `psycopg` (không qua script): `UPDATE/DELETE fls_itl` ⇒ `InsufficientPrivilege`; `fls_doc` tự `SET … = off` rồi INSERT/UPDATE/DELETE/TRUNCATE ⇒ vẫn `InsufficientPrivilege`; `kiem_truoc_khi_mo` nhận kết nối `fls_doc`, từ chối `fls_ghi`. 0 mật khẩu giả trong stdout/stderr/log proxy; gcloud chỉ đọc 4 bí mật, 0 lệnh GHI; proxy `127.0.0.1` rồi bị dọn |
| AC-2 · nơi chạy app | đo trước → khuyến nghị; `Dockerfile` + `03_dung_app.sh`; cửa vẫn TỪ CHỐI | §3 (đo thật: ảnh 373 MB · mở cổng 1,7 s · RAM nghỉ 31 MiB · chuỗi 27,8 s/630 MB). `test_03_dung_app.py` **42 bài**: dựng từ trống ⇒ **19/19 mục ĐẠT**; ngữ cảnh build `git archive` **389 tệp**, chim hoàng yến thật (`sao_luu/` `hien_vat/` `Input_Raw/` `.env.*`) **0 lọt**; 17 phá ⇒ đúng mục ĐỎ; `vao.sh` chạy THẬT vào kho scratch: nghe loopback, không thẻ ⇒ **401**, doc ⇒ POST **405**, ghi ⇒ ký **201** với `actor` = người ký; thiếu `FLS_JWT_SECRET` ⇒ cửa exit ≠ 0; `--dia-chi 0.0.0.0` ⇒ từ chối `GAP-WEB-01`; kết nối đọc còn ghi ⇒ `kiem_truoc_khi_mo` nổ. `docker build` + `docker run` thật: xong, xem §3 |
| AC-3 · bước 04 | nạp config IX.* đã ký bằng công cụ SẴN CÓ; `FLS_CHO_GHI_THAT=1`; số dòng có `mong` (Đ3); riêng tư; dữ liệu = câu chủ | `test_04_nap_du_lieu.py` **19 bài**: 9 bảng/10 phiên bản, dòng bản mới nhất khớp `mong` **1.135** dòng (FX 38 · HD 74 · PL 7 · MM 73 · PER 2 · VEN 360 · ORG 72 · ALR 38 · DRV 471); kho trắng ⇒ **0 mục ĐẠT**; đổi `mong` ±1 ⇒ đúng một bảng ĐỎ; thiếu IX.DRV ⇒ đúng IX.DRV ĐỎ; chạy lại ⇒ 9/9 `có rồi`, 0 phiên bản thêm; **`fls_itl` = 0 và `fls_run` không đổi**; cột `Email Address` lọt vào kho ⇒ đúng mục ĐỎ; `actor` chứa `@` ⇒ ĐỎ; thiếu `FLS_CHO_GHI_THAT` / người nạp xấu ⇒ exit 2 *trước khi gọi gcloud*; `--nguon-that` luôn từ chối (kể cả khi đặt `FLS_STG_DU_LIEU=that`). `chay_chuoi.sh`: kho trắng ⇒ ĐỎ nêu `ChuaKhai` (≥ 7/10 gói), sau 04 ⇒ **10/10 ĐẠT**. Dữ liệu thật/ẩn danh: C3 |
| AC-4 · kịch bản người test | từng bước bấm + SỐ từ `hd2_cong.json` + ô ghi + giới hạn O6 | `UAT_STAGING_E2E.md`: **13 bước**, bảng U3 **13 hàng / 36 con số** có thẻ `<!--hd2:…-->`; `test_uat_doc.py` **4 bài** đối chiếu từng số với `hd2_cong.json` (đổi 1 số ở tài liệu hoặc ở tệp cổng ⇒ ĐỎ đúng số); giới hạn O6 (605 · 615 · D3 · CHECK IX.PL) + sổ rỗng + lệch có tên ở §1; `kiem_tai_lieu` ĐẠT. Các bước tôi đã bấm thử thật qua API: ký tháng 202401 ⇒ 201, lần 2 ⇒ **409**, tháng 209912 ⇒ **404**, ký bản kỳ 202510 ⇒ **404** |
| AC-5 · trình tự chủ chạy | 01→02→03→04→UAT: chạy ở đâu · bao lâu · gửi lại | `tools/staging/README.md`: bảng 5 bước + mục "Đưa mã lên Cloud Shell" + "Giả định chưa kiểm" (7). Thời gian GCP là **ước** (⛔ đo được) |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT; `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` = 0 | `4772 → 4865 → 4868` + `test_S0_R3_02` đỏ khi để số cũ (đã chứng) · `--duong-nen` **`KẾT: ĐẠT`** (28 = 28 · web 3 = 3 · chạy 4868/690) · `kiem_tai_lieu` ĐẠT · `lint-imports` 11 kept · `quet_pii_repo` 0 |

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
| Chạy chuỗi / `--ghi` hd2_cong.json | `sudo docker exec` tại VM — **chỉ CHỦ chạy** (người test có `osLogin` = ⛔ `sudo`; sửa theo `STG-R1-06`) | cần Cloud Run Job + volume cho tệp ghi lại (hd2_cong.json nằm FS tạm của instance) |
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

## 5b · Lần chạy THẬT bước 01 — 23/11 *(chủ, Cloud Shell, `fp-a-project`; do orchestrator báo)*
- Lần 1: ①–⑤ xong; **⑥ HỎNG** — `iam service-accounts create` xong rồi `projects add-iam-policy-binding` báo `INVALID_ARGUMENT: Service account … does not exist` (IAM lan truyền trễ) ⇒ `set -e` dừng, ⛔ in BÁO CÁO. Lần 2: **12/12 ĐẠT** (instance `fls-staging` RUNNABLE · kho `fls` · 4 tài khoản · 5 bí mật · SA `fls-staging-app@fp-a-project…` có `cloudsql.client` + `secretAccessor`).
- **Vá (đúng một chỗ, ⛔ đổi hành vi khác):** bước ⑥ thử lại CÓ HẠN (≤ 12 lần × 5 s; `FLS_STG_THU_LAI`/`FLS_STG_CHO_GIAY`); hết hạn ⇒ lỗi CÓ TÊN `IAM_KHONG_LAN_TRUYEN` và **vẫn in BÁO CÁO** (mục "SA có cloudsql.client" ĐỎ). Bài `tests/staging/test_01_iam_lan_truyen.py` (3 bài, gcloud GIẢ): hỏng 2 lần rồi được ⇒ đúng 3 lần gọi + ĐẠT · hỏng mãi ⇒ đúng 5 lần + lỗi có tên + BÁO CÁO + ĐỎ · được ngay ⇒ 1 lần. Sàn pytest 4865 → **4868**.
- ⚠ Mục BÁO CÁO chỉ đo `cloudsql.client`; `secretAccessor` hỏng ⇒ lỗi có tên ở stderr, ⛔ có mục ĐỎ riêng (giữ nguyên báo cáo 12 mục theo yêu cầu).
- Số thật dùng cho 02/03/04: `fp-a-project` · `asia-southeast1` · `fls-staging` · `fp-a-project:asia-southeast1:fls-staging`. Chủ có `roles/owner` + `run.admin` + `artifactregistry.admin` + `storage.admin` ⇒ **Cloud Run + Artifact Registry dùng được** (⇒ B khả thi về quyền; vẫn vướng luật loopback của cửa, §3).
- Cloud Shell chỉ upload từng tệp, ⛔ có repo clone ⇒ README có mục "Đưa mã lên Cloud Shell" (clone nhánh STG, hoặc `git archive` + upload); 03 đòi `git archive` nên cần git repo (snapshot `git init` cũng được).

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

## 9 · Vòng sửa sau R1 (`KQ-327`) — bảng phát hiện → sửa → bằng chứng

*(Dev · 2026-11-23 · cụm PG **5434** · nhánh `claude/bold-galileo-zukpaf-isp/STG` từ ngọn `5dc0b0e`; ⛔ GCP · ⛔ gcloud thật · ⛔ kho thật. Đã GỘP `origin/claude/bold-galileo-zukpaf` — có H14, ⛔ có I2 — ở commit `b642885`.)*

| Phát hiện | Mức | Sửa | Bằng chứng *(chứng ĐỎ = phá nguồn → bài cắn → trả nguyên)* |
|---|---|---|---|
| `STG-R1-01` SA đọc 5/5 bí mật | CHẶN | `01_dung_staging_gcp.sh`: hai mảng `BI_MAT_APP` *(jwt · `fls_ghi` · `fls_doc`)* / `BI_MAT_QUAN_TRI` *(`postgres` · `fls_admin`)*; vòng gán chỉ chạy trên `BI_MAT_APP`; thêm vòng **GỠ** `secretAccessor` của SA trên hai bí mật quản trị nếu đang có *(idempotent: đo bằng `secrets get-iam-policy`, có ⇒ `remove-iam-policy-binding`, ⛔ có ⇒ bỏ qua; ⛔ đo được ⇒ lỗi `GO_QUYEN_THUA_LOI` + ĐỎ)*. BÁO CÁO thêm **3 mục có `mong`**: `SA đọc đúng bí mật app` mong `3/3` · `SA đọc 0 bí mật quản trị` mong `0/2` · `gán/gỡ vai đủ`. Grep chỗ dùng: `vao.sh:43,45` *(jwt + `fls-staging-pg-$VAI`, VAI ∈ {`fls_ghi`,`fls_doc`})* · `chay_chuoi.sh:20` *(`fls_doc`)* ⇒ 3 trên 5 | `tests/staging/test_01_iam_lan_truyen.py`: 5 bài mới/sửa — gán **đúng 3** *(đếm lệnh `add-iam-policy-binding` = 3, 0 lệnh trên `postgres`/`fls_admin`)* · trạng thái THẬT 23/11 *(SA có cả 5)* ⇒ gỡ đúng 2, **chạy lần 2 gỡ 0** · gỡ hỏng ⇒ `'2/2'` ĐỎ + chữ `PERMISSION_DENIED` · `get-iam-policy` hỏng ⇒ `'0/3'` và `'2/2'` ĐỎ *(Đ5: ⛔ đo được = ĐỎ)*. **Chứng ĐỎ:** đổi vòng gán về 5 bí mật + bỏ vòng gỡ ⇒ **4 trên 8 bài đỏ**; trả nguyên ⇒ 8/8 xanh. Bài ghim cũ `:57` *"trên 5 bí mật"* đổi thành *"3 bí mật app (0 bí mật quản trị)"* |
| `STG-R1-02` "10 gói" cứng ⇒ 2 bài đỏ sau H14 | CHẶN | `test_04_nap_du_lieu.py`: số gói + tên + chuỗi `"N gói · ĐỎ 0"` lấy từ `tools.do_hd2.GOI_BIET` *(`len`, và so TÊN theo thứ tự)*, ⛔ hằng số. Gộp `origin/claude/bold-galileo-zukpaf` ở `b642885`. Sàn pytest = thu thập thật *(xem §9.2)* | `pytest tests/staging/test_04_nap_du_lieu.py` = **19 passed** *(trước vòng sửa trên cây gộp: 2 đỏ `assert (11 == 10)`)* ; `GOI_BIET` = 11 *(đo)* |
| `STG-R1-04` 01 ĐẠT khi gán vai hỏng | NÊN SỬA | `IAM_LOI=1` ⇒ mục `gán/gỡ vai đủ` ĐỎ ⇒ `KẾT: ĐỎ` · exit 1; `thu_lai` giữ **dòng lỗi cuối của gcloud** *(trước: `>/dev/null 2>&1` nuốt chữ thật, nhãn "IAM lan truyền" gắn cho cả `PERMISSION_DENIED`)* và in kèm `gcloud nói: …` | bài mới: `secrets add-iam-policy-binding` `PERMISSION_DENIED` mãi ⇒ stderr đúng **3** dòng `IAM_KHONG_LAN_TRUYEN` kèm chữ `PERMISSION_DENIED` · `[ĐỎ] gán/gỡ vai đủ` · `[ĐỎ] … '0/3'` · exit 1 · `KẾT: ĐỎ` *(bị đỏ khi chứng mutation như dòng `-01`)* |
| `STG-R1-05` UAT lệch số + bài canh vẫn xanh | NÊN SỬA | `UAT_STAGING_E2E.md` v0.2: thêm hàng `WP-C5c` *(86.150 / 77.672 / 8.478)* · cha `WP-C5` = a+b+c *(135.926 / 121.407 / 14.519, `dat` true)* · §1·615 sửa **12.380 → 13.760** và **6.753 → 5.258** *(thẻ `hd2x` mới — số lấy từ `hd2_cong.json` `WP-C5c.do_phu.615`)* · U7/U8/U10 = 11 gói · ~45 s · ~800 MB *(đo R1: 44,4 s · 797 MB)* · bỏ nhãn `[CHỜ H14]`; `[CHỜ I2]` **giữ** *(đo: `grep -rln "FxKho\|kiem_fx_thang" fls tools` = 0 — I2 chưa gộp)*. `test_uat_doc.py`: **bỏ** `CHA` đóng cứng, suy cha/con từ khoá trong `hd2_cong.json`; 39 thẻ `hd2` + 3 thẻ `hd2x` + số dòng U7 so với `len(GOI_BIET)` | `pytest tests/staging/test_uat_doc.py` = **5 passed**. **Chứng ĐỎ:** sửa tài liệu `13.760→12.380` · `77.672→77.671` · `11→10 dòng` ⇒ **3 bài đỏ**; trả nguyên ⇒ xanh |
| `STG-R1-06` U7/U8 đòi `sudo`, `osLogin` ⛔ có | NÊN SỬA | **Phương án A** *(⛔ cần `HOI`: chỉ ghi rõ, ⛔ đổi quyền)*: U7/U8 gắn `[chỉ CHỦ chạy — cần sudo]`; `README` §chạy chuỗi + dòng `BG` §3 sửa. ⛔ cấp `osAdminLogin` *(= root trên VM)*. Phương án B *(lệnh bọc `sudoers` hẹp cho người test)* **chưa làm** — chờ chủ/BA nếu muốn người test tự chạy chuỗi | grep `osAdminLogin` trong `docs fls tools tests` = **0** *(giữ nguyên)*; `test_uat_doc` xanh |
| `STG-R1-07` chết giữa `IX.ALR` ⇒ ⛔ tự lành | NÊN SỬA | `nap_cau_hinh_ix.py`: tách `_ky_alr`; vòng nạp tự lành **theo từng bước**: `v==0` ⇒ nền + KÝ · `0<v<2` *(chỉ IX.ALR)* ⇒ **chỉ KÝ** · `v≥2` ⇒ bỏ qua | bài mới `test_chet_giua_IX_ALR_chay_lai_tu_lanh…`: ép `ky_bat_ix_alr` nổ ⇒ exit ≠ 0 và `IX.ALR` = v1 *(mẫu số)*; chạy lại **hai lần**: cả hai `KẾT: ĐẠT`; `IX.ALR` = **2** bản · tổng bản = **10**. **Chứng ĐỎ:** trả mã cũ ⇒ đỏ *(lần 1 `exit 1`)*; mã mới ⇒ xanh |
| `STG-R1-08` `02 --kiem` để lại bảng probe | NÊN SỬA | probe ghi của `fls_doc` bọc `BEGIN; CREATE TABLE …; ROLLBACK;` *(không còn để lại vật)* | bài mới `…KHONG_de_lai_vat…STG_R1_08`: `GRANT CREATE ON SCHEMA public TO fls_doc` + `RESET default_transaction_read_only` ⇒ `--kiem` vẫn **ĐỎ đúng mục** nhưng số bảng `fls_probe_doc_ghi` = **0**; "làm" sau đó exit 0. **Chứng ĐỎ:** trả probe cũ ⇒ `để lại 1 bảng` đỏ; mã mới ⇒ xanh. `pytest tests/staging/test_02…` = **29 passed** |
| `STG-R1-09` xung đột sàn | GHI NHẬN | Giải ở `b642885` rồi đặt sàn = thu thập thật *(§9.2)* — bài ghim cùng commit | — |
| `STG-R1-10` · `-11` · `-12` | GHI NHẬN | **Chưa sửa — để backlog:** `-10` *(bài chạy `DO_TRONG` bằng stub)* · `-11` *(`--password` qua đối số ×3; 7 tệp `tools/` mang tên SA cục bộ trong ảnh ⇒ `.dockerignore`)* · `-12` *(bài chuỗi phụ thuộc thứ tự test)*. Lý do: ngoài phạm vi "2 CHẶN + NÊN SỬA còn mở" của phiếu; `-11a` thấp rủi ro *(Cloud Shell = một người)*; `-11b` ảnh ⛔ có khoá/token *(Test đã đo)* | — |
| `STG-R1-03` · `-13` | — | đã đóng ở `d04557a` | — |

### 9.1 · Khối lệnh GỠ binding thừa cho CHỦ — chạy NGAY trên `fp-a-project` *(binding thừa đang tồn tại từ lần chạy 01 ngày 23/11)*

> ✅ **Chủ ĐÃ chạy 23/11 (~06:10, theo orchestrator):** cả hai lệnh in `Updated IAM policy`. Khối này giữ làm **biên bản** + để kiểm. Bài chứng cho trạng thái SAU gỡ: chạy 01 trên SA sạch ⇒ **0** lệnh `add` cho `postgres`/`fls_admin`, **0** lệnh `remove`, ⛔ lỗi; còn binding thừa ⇒ gỡ; chạy lần 2 ⇒ 0 gỡ.

Chạy trong Cloud Shell, bằng danh tính chủ *(2 lệnh — ⛔ chứa khoá)*:

```bash
gcloud --project=fp-a-project secrets remove-iam-policy-binding fls-staging-pg-postgres \
  --member="serviceAccount:fls-staging-app@fp-a-project.iam.gserviceaccount.com" --role=roles/secretmanager.secretAccessor
gcloud --project=fp-a-project secrets remove-iam-policy-binding fls-staging-pg-fls_admin \
  --member="serviceAccount:fls-staging-app@fp-a-project.iam.gserviceaccount.com" --role=roles/secretmanager.secretAccessor
```

Kiểm *(mong: cả hai lệnh in rỗng)*:

```bash
for s in fls-staging-pg-postgres fls-staging-pg-fls_admin; do
  gcloud --project=fp-a-project secrets get-iam-policy $s --flatten='bindings[].members' \
    --filter='bindings.members:fls-staging-app@' --format='value(bindings.role,bindings.members)'; done
```

Hoặc chạy lại `bash tools/staging/01_dung_staging_gcp.sh --project fp-a-project` (bản mới) — nó tự gỡ và BÁO CÁO phải có `[ĐẠT] SA đọc đúng bí mật app '3/3'` · `[ĐẠT] SA đọc 0 bí mật quản trị '0/2'`. ⚠ Nếu từng có VM chạy app với token cũ: mật khẩu `fls_admin`/`postgres` đã **đọc được** từ VM trong khoảng thời gian đó ⇒ cân nhắc **xoay mật khẩu** hai vai này *(câu chủ — ⛔ Dev tự làm)*.

### 9.2 · Cổng sau vòng sửa

Đo 23/11 trên ngọn `4042079` ⊕ chỉnh tài liệu/bài `f22dcc3` *(cụm PG 5434)*:

| Cổng | Mong | Đo được |
|---|---|---|
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` *(MỘT lần, một mình)* | `KẾT: ĐẠT` | **`KẾT: ĐẠT`** — toàn bộ: `12 failed · 4933 passed · 2 xfailed · 14 errors` ⇒ tập đỏ+XFAIL **28 = 28** node id *(thêm 0 · bớt 0)* · chạy **4.961** bài *(sàn ≥ 4.961)*; web: `3 failed · 687 passed` ⇒ **3 = 3** *(thêm 0 · bớt 0)* · **690** bài *(sàn ≥ 690)* |
| `pytest tests/staging` | — | **104 passed** *(96 + 8 bài mới)* |
| `kiem_tai_lieu.py` | K1–K6 OK | **OK** *(496 tệp · 2.998 bảng · 976 ô ngày · 104 mã QĐ)* |
| `lint-imports` | 11 kept | **11 kept · 0 broken** |
| `quet_pii_repo.py` | 0 | **0 chỗ · 0 tệp** |

⚠ `f22dcc3` chỉ đổi tài liệu + 1 assert của `test_01` *(8/8 xanh sau đổi)*; `--duong-nen` chạy trước commit ấy nhưng thu thập 4.961 vẫn đúng *(bài mới không thêm — chỉ thêm assert)*.

## 10 · Vòng sửa sau R2 (`KQ-328`) — bảng phát hiện → sửa → bằng chứng

*(Dev · 2026-11-23 · cụm PG **5434** · nhánh `claude/bold-galileo-zukpaf-isp/STG` từ ngọn `406c032`; ⛔ GCP · ⛔ gcloud thật · ⛔ kho thật · ⛔ sửa engine/tuyến/luật D1. Việc ĐẦU: **gộp `origin/claude/bold-galileo-zukpaf` @ `05d7a97`** (có I2) vào STG — sàn = thu thập thật cây gộp; xung đột ở `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` giải bằng: giữ phần khai của nhánh làm việc, đặt `MONG_PYTEST_TOAN_BO` = `pytest --collect-only` đo thật.)*

| Phát hiện | Mức | Sửa | Bằng chứng |
|---|---|---|---|
| `STG-R2-01` bài chuỗi ghim hành vi trước I2 | CHẶN | `tests/staging/test_04_nap_du_lieu.py`: thay 2 bài cũ bằng **bốn** bài hai chiều D1: *(a)* kho TRẮNG ⇒ ĐỎ `ChuaKhai`, tập ĐỎ = `set(GOI_BIET)` (đo: **11/11** — `WP-C2` cũng ĐỎ, trước I2 là ĐẠT); *(a')* sau 04 **CHƯA ký** ⇒ tập gói ĐỎ **=** tập gói đọc tỷ giá, tập ấy đo từ NGUỒN bằng `do_hd2.chay_goi` trên kho đã ký *(gói đọc tỷ giá ⇔ `fx_doc ≠ ∅` — ⛔ hằng)*, mỗi gói ĐỎ có một dòng `⛔ … FX_CHAN`; *(b)* người ký ký qua tuyến ⇒ chữ ký mang đúng tên người ký, chuỗi **N/N ĐẠT** (`N = len(GOI_BIET)`); thêm bài chạy-lại (409 bỏ qua, `--kiem` chỉ đọc) và bài app `doc` ⇒ `405`. | `pytest tests/staging` = **107 passed** *(104 + 3 ròng)*. Đột biến đã cắn: gọi chuỗi bằng `python tools/do_hd2.py` ⇒ bài *(a')* ĐỎ `6 ≠ 11`. Đo kho trắng/chưa ký/đã ký: **11/11 ĐỎ · 11/11 ĐỎ · 11/11 ĐẠT** *(số "6/11" của `KQ-328` là cây gộp thử cũ hơn — xem `STG-R2-05`)* |
| `STG-R2-05` *(MỚI, Dev tự thấy khi sửa -01)* CLI nạp đôi module ⇒ 5/11 gói bỏ qua kho | NÊN SỬA | **Gốc của "6/11"**: `python tools/do_hd2.py --goi X` chạy `do_hd2` là `__main__`, các gói con `do_hd2_c3c · c3d · c5a · c5b · c5c` lại `import tools.do_hd2` ⇒ HAI bản module, `_FX_KHO` của bản thứ hai = `None` ⇒ 5 gói đọc ẢNH `ix_fx.json` thay vì kho ⇒ ⛔ bị D1 chặn tháng chưa ký. Sửa **ở chỗ gọi của staging**, ⛔ engine: `chay_chuoi.sh` gọi `main` qua `python -c 'from tools.do_hd2 import main; …'` *(một bản module)*; chú thích nêu bẫy. | Đo: chuỗi cũ chưa ký ⇒ 6 ĐỎ *(C2·C3a·C3b·C4a·C4b·C4c)* · chuỗi mới ⇒ 11 ĐỎ. **Còn mở cho owner engine**: `python tools/do_hd2.py` *(CLI của engine, ngoài staging)* vẫn có lỗi này — đề nghị `HOI` BA/orchestrator: sửa tại `tools/do_hd2.py` *(⛔ phạm vi vòng này)* |
| `STG-R2-02` UAT v0.2 khai "CHƯA có I2" | NÊN SỬA | `UAT_STAGING_E2E.md` **v0.3**: bỏ `[CHỜ I2]`; dòng 7 + §0.3–0.4 + §1 *(hàng D1)* theo I2; **bước ký tỷ giá**: U7 chạy chuỗi **trước ký** ⇒ 11/11 ĐỎ `FX_CHAN` · U8 người ký ký **36** tháng bằng `tools/staging/app/ky_ty_gia.py` · U9 chạy chuỗi **sau ký** ⇒ 11/11 ĐẠT; đánh số lại U1–U14 *(bảng ánh xạ ở changelog)*. C4 *(một ký một soát)* · C5 *(`doc` suốt UAT, `ghi` chỉ lúc ký)* ghi vào §0.3. | Bài `test_uat_doc.py`: +1 bài canh *(I2 có `FxKho` ⇒ UAT ⛔ còn nhãn chờ — đột biến đặt lại `[CHỜ I2]` ⇒ ĐỎ; số tháng cần ký U8 = dòng ảnh − tháng LẠC tính từ `fls.cau_hinh.fx.kiem` = **36**; đánh số liền)* + số gói U7/U9 từ `GOI_BIET`. U9 cũ *(ký bản)*: **0 nơi gọi `dua_ban_ky`** ở `fls/` · `tools/` ngoài định nghĩa ⇒ staging vẫn ⛔ đường tạo bản ⇒ giữ 404 *(không phải lỗi)* |
| **Lệnh mới** `tools/staging/app/ky_ty_gia.py` *(việc 3)* | — | Người ký ký hàng loạt **qua tuyến** `POST /config/fx/{yyyymm}/sign`: thẻ lấy từ `/phien.js` *(chỉ loopback)*, `actor` do cửa lấy TỪ THẺ — lệnh ⛔ gửi `actor`, ⛔ SQL, ⛔ ghi bảng. Bỏ qua tháng **LẠC** *(202306: màn hình ⛔ có nút ký)* và tháng đã ký; chạy lại ⇒ `409` bỏ qua; `--kiem` chỉ đếm; app `doc` ⇒ `405` ⇒ ĐỎ. | 3 bài `test_04` *(ký thật qua `vao.sh` chế độ `ghi` trên kho scratch: chữ ký `actor` = người ký; chạy lại 0 POST; `doc` ⇒ 405)*. Phát hiện trong lúc dựng: bản sao kho phải `OWNER fls_admin`, ⛔ `postgres` *(mất `USAGE` schema `public` ⇒ 500 ở khoá ngoại)* |
| `STG-R2-03` xung đột sàn lần 2 | GHI NHẬN | **Ghi nhận, đã xử lý cho cây này** *(⛔ việc của orchestrator khi gộp thật)*: sàn = `pytest --collect-only` cây gộp đo **4995** *(web **690**)*, ghim cùng commit ở script + `test_S0_R2_03`. Orchestrator đặt lại khi gộp STG vào nhánh làm việc. | — |
| `STG-R2-04` `sa_doc_duoc` chỉ đo binding trực tiếp | GHI NHẬN | **Backlog — chưa sửa**: cần thêm một dòng BÁO CÁO in các vai SA ở cấp project *(căn cứ mã, ⛔ đo ở GCP; số liệu chủ 23/11 khớp phép đo hiện tại)*; ⛔ gcloud thật ở phiên này. | — |

### 10.1 · Cổng — chạy ở cụm 5434 trên cây ĐÃ gộp
| Lệnh | Mong | Đo |
|---|---|---|
| `pytest tests/staging` | 107 | **107 passed** *(~3 phút)* |
| `pytest --collect-only` *(cây gộp)* | = sàn | **4995** *(web 690)* |

| `dung_moi_truong_isp.sh --duong-nen --cong 5434` *(MỘT lần, một mình, 20 phút 42 giây)* | `KẾT: ĐẠT` 28 = 28 · web 3 = 3 | **`KẾT: ĐẠT`** — toàn bộ `12 failed · 4967 passed · 2 xfailed · 14 errors` = **4995 chạy** *(skipped 0 · deselected 0)* ⇒ tập đỏ+XFAIL **28 = 28** *(thêm 0 · bớt 0)* · web `3 failed · 687 passed` = **690 chạy**, tập đỏ **3 = 3** |
| `kiem_tai_lieu.py` · `lint-imports` · `quet_pii_repo.py` | K1–K6 · 11 kept · 0 | **K1–K6 OK** *(502 tệp · 3.018 bảng · 985 ô ngày)* · **11 kept, 0 broken** · **0 chỗ · 0 tệp** |

## 11 · Vòng sửa sau R2b (`KQ-344`) — lỗi thật GCP

*(Dev · 2026-11-23 · cụm PG **5434** · nhánh `claude/bold-galileo-zukpaf-isp/STG` từ ngọn `fa2c07e`; ⛔ gcloud thật · ⛔ kho thật · ⛔ khoá trong repo. Việc ĐẦU: **gộp `origin/claude/bold-galileo-zukpaf` @ `577044e`** *(= main `c5ea872` + AG `8a1eca4` + TIEN_DO)* ⇒ `7cff610`; xung đột changelog *(giữ cả hai)* + sàn *(giữ bản STG rồi đặt = thu thập thật)*. Ba CHẶN là lỗi **chủ gặp khi chạy thật**; mỗi sửa được chứng minh ĐỎ trên mã cũ bằng đồ GIẢ **đã hiệu chỉnh theo hành vi GCP đo được**, rồi ĐẠT trên mã mới.)*

| Phát hiện | Mức | Sửa | Bằng chứng *(ĐỎ trên mã cũ → ĐẠT trên mã mới)* |
|---|---|---|---|
| `STG-R2b-02` bước 02: `fls_ghi`/`fls_doc` còn CREATEROLE/CREATEDB | CHẶN | ⓐ `02`: bước mới **①b** — vai app **tạo bằng SQL** do `postgres` chạy *(`CREATE ROLE … LOGIN NOCREATEDB NOCREATEROLE`, mật khẩu đọc từ Secret Manager, đi qua ống từ `printf` dựng sẵn ⇒ ⛔ `ps`/tệp; `VERBOSITY=terse` + che mật khẩu trong mọi lời PG in ra; bí mật ngoài `[A-Za-z0-9_-]{16,}` ⇒ DỪNG)*. Chưa có ⇒ tạo · SẠCH ⇒ đồng bộ mật khẩu · **bẩn** *(thuộc tính thừa HOẶC thành viên `cloudsqlsuperuser`)* ⇒ **đường chuyển**: in phép đo trước *(`rolcreaterole/rolcreatedb/rolsuper` + `postgres có ADMIN OPTION=`)* → thu mọi quyền bằng `fls_admin` *(`sql/02c_thu_quyen_vai.sql`)* → `DROP ROLE` SQL *(lời PG đầy đủ, kể DETAIL)* → bị từ chối ⇒ `gcloud sql users delete` + kiểm vai đã mất → `CREATE ROLE` bằng SQL → ②–④ cấp lại. Lỗi CÓ TÊN `VAI_THU_QUYEN_LOI` · `VAI_KHONG_XOA_DUOC` · `VAI_KHONG_TAO_DUOC` · `VAI_KHONG_DONG_BO_MK`. Bỏ câu `ALTER ROLE … NOSUPERUSER …` + `REVOKE cloudsqlsuperuser` nuốt lỗi. BÁO CÁO: mục `siêu quyền hay CREATEROLE/CREATEDB (đếm vai)` **giữ nguyên `mong 0`** *(ĐỎ khi `2`, ĐỎ khi ⛔ đo được — bài `vai_ghi_co_CREATEROLE` + `psql` giả hỏng)*; thêm dòng **đo, ⛔ chấm** `vai quản trị có ADMIN OPTION … (đếm vai)`. ⓑ `01`: ⛔ còn `gcloud sql users create/set-password` cho `fls_ghi`/`fls_doc` — chỉ sinh **bí mật** của chúng; mục BÁO CÁO `đủ 4 tài khoản` ⇒ `đủ tài khoản gcloud (postgres · fls_admin)`. | **Mô phỏng Cloud SQL PG16** `H.dung_vai_cloud_sql`: vai quản trị ⛔ SUPERUSER, `CREATEROLE CREATEDB`, ADMIN OPTION thừa kế qua `cloudsqlsuperuser` *(grant `INHERIT FALSE, SET FALSE` — ⛔ thừa kế quyền chủ bảng)*. Fixture `mt` *(mọi bài staging)* = **H-B**. Mã cũ trên H-B ⇒ tái hiện **ĐÚNG** báo cáo GCP: `1 mục khác mong` · `= 2 (mong 0)` · `⚠ không hạ được thuộc tính`. Tệp mới `test_02_chuyen_vai_gcp.py` **8 bài**: mã cũ **8/8 ĐỎ** · mã mới **8/8 ĐẠT** *(H-A từ kho rỗng: 2 lần `gcloud sql users delete`, đúng 2 lời PG `ADMIN option`; trạng thái GCP HIỆN TẠI — 02 cũ đã chạy, quyền đã cấp, vai bẩn — ×H-A/H-B ⇒ `--kiem` trước ĐỎ đúng mục, "làm" ⇒ ĐẠT, đăng nhập bằng mật khẩu bí mật được, `fls_doc` vẫn `read_only on`; gcloud xoá hỏng ⇒ `VAI_KHONG_XOA_DUOC` exit 1, ⛔ BÁO CÁO; PG từ chối tạo ⇒ lời PG ⛔ mang mật khẩu; bí mật có `'` ⇒ DỪNG trước khi chạm vai)*. `test_02_di_tru_phan_quyen.py` **29/29** trên H-B. `test_01` +1: mã cũ ĐỎ *(`sql users create fls_doc`)* · mới ĐẠT |
| `STG-R2b-01` bước 03: `.gcloudignore` lọc mất `Dockerfile` | CHẶN | Ngữ cảnh build tách ra `tools/staging/ngu_canh_build.sh` *(dùng chung 03 + công cụ thử)*: `git archive HEAD -- <danh sách cho phép>` **⛔ `.gcloudignore`**; ngữ cảnh có `.gcloudignore`/`.gitignore` ⇒ `NGU_CANH_CO_TEP_LOC`; cây chưa commit/rỗng ⇒ `NGU_CANH_RONG` *(gộp luôn `STG-R2b-04`)*. **Xoá `.gcloudignore` khỏi repo** *(bài cũ ghim `.gcloudignore == .dockerignore` — chính nó là bẫy; nay ghim "⛔ tồn tại")*. `03`: giữ lời `gcloud builds submit` *(tee)*, đọc dòng `Creating temporary archive of N file(s)`; BÁO CÁO thêm `ngữ cảnh build · tệp ngữ cảnh / tệp gcloud tải lên (đếm)` *(in)* + **`tệp tải lên = tệp ngữ cảnh (≠ 0)` `mong True`** *(⛔ đọc được ⇒ None ⇒ ĐỎ)* + `gcloud builds submit (exit)` `mong 0`; build đỏ ⇒ `BUILD_LOI`, **bỏ ④–⑥** *(⛔ dựng VM cho ảnh ⛔ có)* rồi vẫn in BÁO CÁO. | **Hiệu chỉnh giả trên SỐ ĐO THẬT**: ngữ cảnh `c4a0f39` = **398** tệp; ngữ nghĩa gitignore THUẦN *(`git ls-files --exclude-from`)* cho **1** — ⛔ khớp 292; mô hình "xét từng tiền tố đường dẫn, mẫu khớp cả đường dẫn, `*` ⛔ qua `/`" cho **292 = `fls` 141 + `tools` 150 + `requirements.txt` 1** — khớp ĐÚNG số GCP *(bài `test_gia_gcloudignore_khop_so_do_THAT_GCP_398_ra_292…`)*. `gcloud_gia.py` nay lọc theo mô hình ấy, in dòng `Creating temporary archive…`, ⛔ Dockerfile ⇒ `lstat /workspace/Dockerfile`. Mã cũ ⇒ `test_03` **27 ĐỎ** *(mọi bài dựng ⇒ `lstat`)*; mới ⇒ **49/49**. Phá: gcloud "lọc mất" `Dockerfile` ⇒ `BUILD_LOI` + 3 mục ĐỎ, 0 lệnh tạo VM/firewall; lọc mất MỘT tệp mà build vẫn qua ⇒ **đúng 1** mục ĐỎ *(đếm có răng)* |
| `STG-R2b-05` Cloud Build ⛔ BuildKit — `RUN --mount` | CHẶN | `Dockerfile` **đa tầng**: tầng `goi` cài `psycopg` vào `/goi` *(CA proxy CHỈ máy dev qua `--build-arg PIP_CA_PEM` — CA là chứng chỉ công khai; Cloud Build ⛔ cần)*, tầng chạy `COPY --from=goi /goi /usr/local` ⇒ ⛔ ARG/ENV/tệp CA. ⛔ cú pháp nào đòi BuildKit. Công cụ **`tools/staging/thu_dung_anh.sh`**: ngữ cảnh y bước 03 + `DOCKER_BUILDKIT=0 docker build`, 4 phép có `mong` *(exit 0 · 0 dòng `requires BuildKit` · 0 dòng CA/`PIP_CA_PEM` trong `docker history` ảnh cuối · uid 10001)*; ⛔ dockerd ⇒ ĐỎ. Giả: `builds submit` gặp `RUN --mount` ⇒ đúng câu docker. | `DOCKER_BUILDKIT=0 docker build` *(dockerd cục bộ)* trên Dockerfile cũ ⇒ **`Step 9/16 … the --mount option requires BuildKit`** — đúng câu + đúng bước Cloud Build báo. `thu_dung_anh.sh`: ở `7cff610` **KẾT: ĐỎ — 3 mục** · ở `5e70562` **KẾT: ĐẠT** *(4/4; ảnh: `psycopg 3.3.9`, uid 10001, 0 tệp `pipca*`, env ⛔ `PIP_CERT`)*. Bài tĩnh `test_tinh_Dockerfile_KHONG_cu_phap_doi_BuildKit…` *(luôn chạy)* ĐỎ trên cũ · ĐẠT mới; bài giả `…tu_choi_RUN_mount…` |
| `STG-R2b-04` `git archive` cây chưa commit ⇒ lỗi khó hiểu | GHI NHẬN | Gộp vào `ngu_canh_build.sh`: `NGU_CANH_RONG` có tên; tệp trong danh sách cho phép chưa commit ⇒ `⚠ N tệp … CHƯA commit — ảnh dựng từ HEAD`. | bài `test_ngu_canh_build_repo_CHUA_commit…` |
| `STG-R2b-03` `test_04_chay_lai_van_DAT…` phụ thuộc thứ tự | GHI NHẬN | **⛔ sửa vòng này** *(ngoài 3 CHẶN; bài xanh trong cả tệp — đường nền chạy cả tệp)*. Backlog. | — |

**Hai giả thuyết cho `STG-R2b-02` — CẢ HAI CHƯA đo ở GCP** *(lỗi gốc bị `>/dev/null 2>&1` nuốt)*. Đo trên PG 16 cục bộ 23/11 *(vai ⛔ SUPERUSER)*:
- **H-A** *(phiếu giao việc)* — `postgres` ⛔ ADMIN OPTION trên vai gcloud tạo. PG16 ⇒ `ALTER ROLE x SET …` **cũng** bị từ chối *("Only roles with the CREATEROLE attribute and the ADMIN option on role")*. ⚠ **Mâu thuẫn** với hai sự thật đã đo cùng lần chạy: `fls_doc · ALTER ROLE đã đặt` **ĐẠT** và `chủ kho = fls_admin` **ĐẠT** *(`GRANT fls_admin TO CURRENT_USER` cũng đòi ADMIN OPTION)*.
- **H-B** — `postgres` CÓ ADMIN OPTION; câu cũ bị từ chối CẢ CÂU vì mệnh đề `NOSUPERUSER` *("Only roles with the SUPERUSER attribute may change the SUPERUSER attribute")*; `ALTER ROLE x NOCREATEROLE NOCREATEDB` riêng thì ĐƯỢC. **Khớp mọi sự thật đã đo.**
- Đường chuyển ĐÚNG với cả hai *(đã chứng ở bài)*. Lần chạy 02 của chủ **phân xử**: dòng `đo trước: … có ADMIN OPTION=true|false` và — nếu có — `ⓑ DROP ROLE … PG nói: … DETAIL …`.
- **Chưa đo ở GCP, script in kết quả**: ① `postgres` `CREATE ROLE … PASSWORD` được; ② `DROP ROLE` SQL được *(H-B)* hay phải `gcloud sql users delete` *(H-A)*; ③ `gcloud sql users delete` xoá được vai sau khi đã thu quyền; ④ vai SQL tạo có hiện ở `gcloud sql users list` không *(⛔ chấm ở 01)*; ⑤ `gcloud builds submit` ⛔ `.gcloudignore` tải ĐỦ ngữ cảnh và in đúng dòng `Creating temporary archive of N file(s)` *(⛔ đọc được ⇒ mục ĐỎ có tên — ⛔ xanh giả)*. Ghi ở `tools/staging/README.md` giả định **#8 · #9**; **#2 gạch: ĐÃ KIỂM 23/11 — SAI**.

### 11.1 · Khối lệnh CHỦ chạy lại *(Cloud Shell · `fp-a-project`)*

```bash
cd ~/fls                                   # repo trong Cloud Shell
# ⓪ lấy mã sửa — nhánh MỚI từ origin (commit vá tạm cục bộ ở nhánh cũ được GIỮ, ⛔ xoá):
git fetch origin claude/bold-galileo-zukpaf-isp/STG
git switch -C stg-r2b origin/claude/bold-galileo-zukpaf-isp/STG
git log --oneline -1                       # mong: ngọn nhánh STG (commit BG-326 §11)
test ! -e .gcloudignore && ! grep -n -- '--mount' Dockerfile && echo "cây đúng"   # mong: in "cây đúng"

# ① 02 — ĐƯỜNG CHUYỂN VAI (vai gcloud tạo ⇒ thu quyền → xoá → tạo lại bằng SQL → cấp lại 02b)
bash tools/staging/02_di_tru_phan_quyen.sh --project fp-a-project --kiem   # TRƯỚC: mong ĐỎ đúng 1 mục "siêu quyền … = 2"
bash tools/staging/02_di_tru_phan_quyen.sh --project fp-a-project          # LÀM: ①b in "ĐƯỜNG CHUYỂN" ×2 · KẾT: ĐẠT
#   gửi lại: khối "①b" (dòng "đo trước …", "ⓑ DROP ROLE …" — phân xử H-A/H-B) + BÁO CÁO
#   ⛔ dừng ở VAI_KHONG_TAO_DUOC ⇒ vai đã xoá, app ⛔ nối được: gửi ngay dòng lỗi, ⛔ chạy 03

# ② 03 — ảnh + VM
bash tools/staging/03_dung_app.sh --project fp-a-project
#   mong BÁO CÁO: "tệp tải lên = tệp ngữ cảnh (≠ 0)" ĐẠT · "gcloud builds submit (exit)" 0
#   chờ 2–4 phút (VM cài docker + kéo ảnh) rồi:
bash tools/staging/03_dung_app.sh --project fp-a-project --kiem            # mong KẾT: ĐẠT (kể cả 5 mục TRONG VM)

# (tuỳ) 01 --kiem chỉ đọc: mục "đủ tài khoản gcloud (postgres · fls_admin)"
bash tools/staging/01_dung_staging_gcp.sh --project fp-a-project --kiem
```

### 11.2 · Cổng — chạy ở cụm 5434 trên cây ĐÃ gộp
| Lệnh | Mong | Đo |
|---|---|---|
| `pytest tests/staging` | 124 + 16 mới | ⏳ |
| `pytest --collect-only` *(cây gộp)* | = sàn | **5082** *(= 4995 STG + 71 AG + 16 mới: `test_02_chuyen_vai_gcp` 8 · `test_01` 1 · `test_03` 7)* · web **690** |
| `dung_moi_truong_isp.sh --duong-nen --cong 5434` *(MỘT lần, một mình)* | `KẾT: ĐẠT` 28 = 28 · web 3 = 3 | ⏳ |
| `kiem_tai_lieu.py` · `lint-imports` · `quet_pii_repo.py` | K1–K6 · 11 kept · 0 | ⏳ |
| `thu_dung_anh.sh` *(dockerd cục bộ)* | `KẾT: ĐẠT` | **ĐỎ 3 mục** @ `7cff610` → **ĐẠT 4/4** @ `5e70562` |

### 11.3 · Dev tự thấy còn yếu
- Mô phỏng Cloud SQL là **suy từ sự thật đã đo**, ⛔ đo trực tiếp: nếu GCP thật khác cả H-A lẫn H-B *(vd `postgres` ⛔ `CREATE ROLE` được)* thì 02 dừng ở `VAI_KHONG_TAO_DUOC` **sau khi đã xoá vai** — app ⛔ nối được tới khi sửa. Đã chọn thứ tự này vì `CREATE` trước `DROP` ⛔ được *(trùng tên)*; khối lệnh chủ ghi rõ: dừng ở lỗi ấy ⇒ ⛔ chạy 03.
- Mô hình lọc `.gcloudignore` hiệu chỉnh trên **MỘT** điểm đo *(398 → 292)*; nay ⛔ còn tệp ấy nên mô hình chỉ còn canh lối cũ — chỗ dựa thật cho GCP là mục BÁO CÁO đếm `tải lên = ngữ cảnh`.
- `thu_dung_anh.sh` ⛔ là bài pytest *(đường nền đòi `skipped = 0`, dockerd ⛔ có ở mọi container)*; trong pytest chỉ có bài tĩnh cú pháp + bài giả. Ai đổi Dockerfile nên chạy công cụ ở máy có dockerd *(Cloud Shell có)*.
- `STG-R2b-03` *(bài phụ thuộc thứ tự)* chưa sửa.
