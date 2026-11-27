# BG-364 — bàn giao `WO-363` · staging có LINK WEB `https://…run.app` sau Google IAP

| | |
|---|---|
| **Thuộc** | `WO-363` |
| **Phát bởi** | `fls-dev` · 2026-11-24 *(phiên cloud · cụm PG **5434**)* |
| **Nhận** | `fls-test` *(R1 `KQ-365` · R2 cuối `KQ-366`)* + **chủ** *(chạy `07` trên `fp-a-project`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/STG-WEB` — link web `997f4d2` · BG v1 `0942e3e` · **đăng nhập FLS + BG v2: ngọn nhánh** *(đã đẩy; SHA ở dòng nhật ký cuối của `WO-363`)* |
| **Bổ sung giữa chừng** | orchestrator 24/11 ~03:45 theo lời chủ *"tạo 1 tài khoản để đăng nhập chung"*: màn `/login` FLS, MỘT tài khoản `HondurasGesha`, SAU IAP — §2 AC-6. `--duong-nen` lượt 1 bị DỪNG giữa chừng (mã sắp đổi), chạy lại MỘT lần ở cuối |

## ⭐ Chủ làm gì, theo thứ tự *(Cloud Shell · `fp-a-project` · ~10 phút)*

> ⚠ **Sau R1 `KQ-365` (25/11): khối lệnh mới nhất ở §12.1** — số mục BÁO CÁO đổi (08: 8 mục · 07: 35/34 mục) và lần dựng đầu của 07 ĐỎ đúng 1 mục `aud ĐO` cho tới khi có người mở link. Khối dưới đây là bản 24/11, giữ làm biên bản.

```bash
cd ~/fls
git fetch origin claude/bold-galileo-zukpaf-isp/STG-WEB
git switch -C stg-web origin/claude/bold-galileo-zukpaf-isp/STG-WEB
git log --oneline -1                                    # mong: ngọn nhánh STG-WEB (commit BG-364)
test -f tools/staging/07_link_web.sh && echo "cây đúng" # mong: in "cây đúng"

# ① ĐO TRƯỚC — chỉ đọc, ⛔ đổi gì
bash tools/staging/07_link_web.sh --project fp-a-project --kiem
#   mong: KẾT: ĐỎ — 28 mục khác mong (chưa có service, chưa đặt đăng nhập) · "⭐ LINK: — (chưa có service)"
#   gửi lại: CHỈ dòng "KẾT: …" (để biết gcloud đọc được project)

# ①b ĐẶT TÀI KHOẢN ĐĂNG NHẬP CHUNG — script HỎI mật khẩu 2 lần, gõ ẨN (⛔ hiện, ⛔ lịch sử shell)
bash tools/staging/08_dat_dang_nhap.sh --project fp-a-project
#   ⭐ đặt mật khẩu MỚI ≥ 12 ký tự; ⛔ dán vào chat/phiếu — báo người test RIÊNG
#   mong: KẾT: ĐẠT (4 mục) · gửi lại: phần BÁO CÁO (⛔ chứa mật khẩu hay băm)

# ② DỰNG — app CHỈ-ĐỌC (vai fls_doc), chỉ tài khoản của bạn vào được
bash tools/staging/07_link_web.sh --project fp-a-project
#   ảnh: tag = SHA ngắn của HEAD; CHƯA có trong Artifact Registry ⇒ Cloud Build 3–6 phút (như bước 03)
#   mong: KẾT: ĐẠT (29 mục) · dòng "⭐ LINK: https://fls-staging-web-….run.app"
#   gửi lại: TOÀN BỘ phần từ "── BÁO CÁO" tới "KẾT: …" (⛔ có email/mật khẩu/khoá — script ⛔ in)
#   ĐỎ ở các mục "TRONG …" ngay sau deploy ⇒ chờ 1 phút rồi chạy lại ① (--kiem) — nhật ký Cloud Run trễ (G-5)

# ③ MỞ URL bằng trình duyệt (máy bạn) — đây là phép đo G-1
#   mong: trang đăng nhập Google → đăng nhập tài khoản đang dùng gcloud → màn /login FLS
#         → HondurasGesha + mật khẩu ①b → màn FLS, F03 hiện SỐ (⛔ ô lỗi)
#   gửi lại: 1 câu "F03 hiện số" HOẶC ảnh chụp nếu ô báo FLS-TRA-LOI-LA / FLS-MAT-KET-NOI
#   (thử thêm: <link>/logout ⇒ về /login; gõ sai ⇒ "Sai tên đăng nhập hoặc mật khẩu")

# ④ (khi có danh sách người test) — chạy lại được, ⛔ dựng lại ảnh
bash tools/staging/07_link_web.sh --project fp-a-project --cho-vao a@apero.vn,b@apero.vn
```

- Muốn người test **KÝ** qua link *(U5/U8)*: thêm `--che-do ghi --nguoi-ky <tên.người.ký>` vào ②, ký xong chạy lại ② **không** có hai cờ ấy *(về `doc`)*.
- **Tắt link** khi không test: `gcloud run services delete fls-staging-web --region asia-southeast1` *(script ⛔ xoá gì; chạy lại ② là có lại)*. Scale-về-0 nên để nguyên cũng ≈ 0 USD.
- VM `fls-staging-app` + đường hầm SSH **⛔ đổi** — vẫn là chỗ "chạy chuỗi" HD2 + dự phòng. Có thể `stop` VM khi không chạy chuỗi.

## Kết luận một dòng
Đường **(a) Cloud Run + IAP tích hợp** — ⛔ tên miền, ⛔ đụng cửa: cửa vẫn nghe `127.0.0.1:8088`, thành phần DUY NHẤT nghe ngoài là `cong_iap.py` *(kiểm chữ ký IAP ES256 — 403 khi thiếu/giả; rồi **đăng nhập FLS** `/login` tài khoản chung `HondurasGesha` — băm scrypt, khoá tạm, cookie phiên an toàn)*; +81 bài, 27/27 đột biến bị bắt; ⛔ chưa chạy ở GCP — 7 giả định có tên, bước ③ ở trên đo giả định lớn nhất (G-1).

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/staging/07_link_web.sh` *(mới)* | Script CHỦ chạy: bật API `run`·`iap` → tạo tác tử IAP (`gcloud services identity create`) → dùng lại ảnh (tag có) / dựng y bước 03 → `gcloud run deploy --iap --no-allow-unauthenticated --max-instances=1 --port=8080 --command=bash --args=…/vao_cloud_run.sh` (SA `fls-staging-app` có sẵn — ⛔ cấp thêm quyền) → tác tử IAP `run.invoker` + GỠ `allUsers`/`allAuthenticatedUsers` nếu có → `iap.httpsResourceAccessor` cho người chạy + `--cho-vao` → BÁO CÁO 29 mục `mong` *(28 khi `--kiem`; gồm 3 mục đăng nhập — dòng bổ sung dưới)* + `⭐ LINK`. `--iap` GA ⛔ biết ⇒ tự thử `gcloud beta` một lần (G-2). ⛔ in email. |
| `tools/staging/app/cong_iap.py` *(mới)* | Cổng `$PORT` → `127.0.0.1:8088`. Kiểm `X-Goog-IAP-JWT-Assertion`: chữ ký ES256 (P-256 thuần Python — ảnh chỉ có `psycopg`) theo khoá công khai IAP · `iss` · `exp`/`iat` · `email` · `aud` nếu ghim (`FLS_IAP_AUD`). Thiếu/sai ⇒ **403** (cửa ⛔ bị chạm) · ⛔ lấy được khoá ⇒ **503** (ĐÓNG) · ⛔ `K_SERVICE` ⇒ từ chối khởi động · gỡ `X-Goog-*` + `X-Serverless-Authorization` · `Authorization` NGUYÊN VẸN · nhật ký `IAP_VAO email=… <PT> <đường> <mã>` (⛔ thẻ/JWT/chuỗi truy vấn) + một dòng `IAP_AUD …`. `--tu-do` in dòng `TU_DO …`; `--doi-cua` chờ một câu trả lời HTTP. |
| `tools/staging/app/vao_cloud_run.sh` *(mới)* | Điểm vào Cloud Run: `vao.sh` NGUYÊN VẸN (cửa 127.0.0.1:8088) → chờ cửa trả lời → `cong_iap.py` → dòng `TU_DO` → một tiến trình chết ⇒ exit 1. `PORT` = cổng cửa ⇒ từ chối. ENTRYPOINT ảnh (đường VM) ⛔ đổi. |
| `tools/staging/app/dang_nhap.py` *(mới — bổ sung)* | Băm **scrypt** (`hashlib.scrypt`, N=2^14 r=8 p=1, muối 16 B) — lý do: có trong thư viện chuẩn (ảnh chỉ có `psycopg`, ⛔ thêm `argon2-cffi`/`bcrypt` vào ảnh + `requirements.txt`), tốn bộ nhớ 16 MiB/lần như argon2, OWASP chấp nhận khi ⛔ có argon2id. So khớp `hmac.compare_digest` (tên + băm); tên sai vẫn chạy scrypt. `KhoaSai`: 5 lần sai / 15 phút ⇒ khoá 15 phút **theo email IAP**. `Phien`: cookie `__Host-fls_phien` = `v1.<hết hạn>.<email>.<HMAC>` · HttpOnly · Secure · SameSite=Strict · Path=/ · Max-Age 8 giờ; gắn email IAP; khoá HMAC suy từ bản ghi băm (đổi mật khẩu ⇒ phiên cũ mất); `/logout` thu hồi. Màn `/login` tự chứa (⛔ script, ⛔ phản chiếu chữ gõ). CLI `--bam` đọc mật khẩu từ STDIN. |
| `tools/staging/app/cong_iap.py` *(bổ sung)* | Sau JWT IAP: `/login` · `/logout` do cổng xử lý; mọi đường khác đòi phiên — thiếu ⇒ API `401 FLS-CHUA-DANG-NHAP`, trang `303 /login`, cửa ⛔ bị chạm (kể cả `phien.js` ⇒ thẻ `ke_toan` chỉ ra SAU đăng nhập). Gỡ `Cookie` trước khi chuyển tiếp. Bí mật `fls-staging-login` đọc bằng `lay_bi_mat.py`, giữ 60 giây (chưa đặt ⇒ `/login` 503, ⛔ ai vào). Nhật ký `DANG_NHAP email=… dung \| sai n/5 \| khoa \| dang_xuat` — ⛔ mật khẩu. `TU_DO` thêm `dang_nhap=san_sang\|chua_dat`. |
| `tools/staging/08_dat_dang_nhap.sh` *(mới — bổ sung)* | CHỦ đặt mật khẩu: `read -rs` ×2 (khớp · ≥ 12 · ⛔ trùng tên) → `printf … \| dang_nhap.py --bam` → `secrets create/versions add --data-file=-` (chỉ BẢN GHI BĂM) → SA `secretAccessor` trên ĐÚNG bí mật ấy → BÁO CÁO 4 mục. ⛔ xoá phiên bản cũ. |
| `tools/staging/07_link_web.sh` *(bổ sung)* | +3 mục BÁO CÁO: bí mật đăng nhập có · SA đọc được · `TRONG · tài khoản đăng nhập FLS lúc khởi động` ⇒ **29** mục khi dựng (28 `--kiem`). |
| `tests/staging/gcloud_gia.py` · `tests/staging/curl_gia.py` *(mới)* | Nhánh Cloud Run · IAP · logging + mặt NGOÀI service — mô phỏng hành vi có thể làm HỎNG script (xem §2 AC-3). |
| `tests/staging/test_07_link_web.py` *(37 bài)* · `tests/staging/test_cong_iap.py` *(31 bài)* · `tests/staging/test_08_dat_dang_nhap.py` *(13 bài)* | §2. |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Sàn `MONG_PYTEST_TOAN_BO` 5082 → **5168** = thu thập thật *(nền `3223419` đo = 5087 — `KQ-351` thêm 5; + 81)*; web **690** giữ. |
| `tools/staging/README.md` | Bước 07 trong bảng; §"Người test vào bằng gì": link web là đường chính, tunnel dự phòng; 4 giới hạn đường link; giả định **#10–#16 (G-1…G-8)**. |
| `docs/ITL/04_Test/UAT_STAGING_E2E.md` **v0.5** | §0.1 + U1 theo link web → Google → `/login` (U1 = phép đo G-1); U10 xem F03 qua tunnel. |
| `tools/staging/README.md` *(bổ sung)* | Bước **08** (chạy TRƯỚC 07); đoạn đăng nhập FLS ở §"Người test vào bằng gì". |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | Dòng 24/11. |

## 1 · Cổng *(kết quả nguyên văn — cụm 5434)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/staging` | **205 passed** in 297 s *(124 cũ + 81 mới)* — lượt trước bổ sung: 179 passed |
| `pytest --collect-only` | **5168** tests collected · `tests/web` **690** |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5434` *(MỘT lần, một mình)* | **`KẾT: ĐẠT`** — 28 = 28 · web 3 = 3 · chạy 5168 / 690 *(§1.1)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — … (516 file, 3062 bang, 989 o ngay, 104 ma QD)` |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python tools/quet_pii_repo.py` | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `python -m fls.db.pg_migrate` | `khong co gi de ap` · `pg_verify: khop` *(⛔ chạm schema)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | ⛔ **ĐỎ CÓ SẴN** — `B1` · `C6 ⛔ DOI TRANG THAI: mong KHOP, do duoc LECH`. Đo ở nền `3223419` *(worktree)*: **ĐỎ** `A1` · `B1` · `C6` ⇒ ⛔ do WO này *(kho cục bộ rỗng; WO ⛔ chạm tài liệu audit)* |
| `python tools/kiem_so_song.py` | ⛔ **ĐỎ CÓ SẴN** — `FileNotFoundError: …/.venv/Scripts/lint-imports.exe` *(đường Windows gắn cứng)*; nền `3223419` cùng lỗi |
| `docker compose down` | ⛔ ⛔ chạy *(container cloud ⛔ Docker; luật CLAUDE.md)* |

### 1.1 · `--duong-nen`
**`KẾT: ĐẠT`** @ `86a5003` *(chạy MỘT lần, một mình, cụm 5434; lượt trước ở `0942e3e` bị DỪNG giữa chừng vì phần bổ sung đăng nhập)*:
- toàn bộ: `12 failed, 5140 passed, 2 xfailed, 14 errors in 1705.25s (0:28:25)` ⇒ `[ĐẠT] tập đỏ + XFAIL = đường nền: 28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 5168 bài (mong ≥ 5168) · skipped 0 · deselected 0`
- `tests/web`: `3 failed, 687 passed in 210.12s` ⇒ `[ĐẠT] … 3 = 3 node id (thêm 0 · bớt 0) · chạy 690 bài (mong ≥ 690)`
- 7 phép kiểm môi trường ĐẠT *(27/27 di trú · `pg_verify` 0 lệch · lint 11 kept · HD1 `chay 9845 / co 9967` · `fls_itl` = 0)* ⇒ **0** bài `tests/staging` trong tập đỏ.

## 2 · Bằng chứng từng AC

| AC | Bằng chứng |
|---|---|
| **AC-1** thiết kế | §3 — so (a)/(b) có số; chọn **(a)**. Tra tài liệu GCP hiện hành 24/11 *(nguồn ở §3)*. |
| **AC-2** luật cửa | ⓐ `chay_cua.py` · `fls/api/cua.py` · `vao.sh` · `Dockerfile` **⛔ đổi một dòng** (`git diff 3223419 -- fls tools/chay_cua.py tools/staging/app/vao.sh Dockerfile` = 0 dòng). ⓑ Bài THẬT `test_vao_cloud_run_cua_that_TU_DO_dung_mong_va_cua_van_gac_the` *(cửa thật + kho scratch)*: `nghe_tren(cổng cửa) == ["127.0.0.1:<cổng>"]` · `nghe_tren(cổng IAP) == ["0.0.0.0:<cổng>"]` · qua cổng với JWT IAP ĐÚNG mà ⛔ thẻ FLS ⇒ **401** · có thẻ ⇒ 200 · thẻ FLS mà ⛔ JWT IAP ⇒ **403** · cửa chết ⇒ container thoát ≠ 0 *(10/10 lượt ĐẠT sau sửa bài — §5)*. ⓒ `test_cong_khong_JWT_hay_JWT_gia_thi_403_va_CUA_KHONG_bi_cham`: 5 kiểu ⛔ hợp lệ ⇒ 403 và cửa giả ghi **0** yêu cầu. ⓓ ES256: vectơ RFC 6979 §A.2.5 *(2 thông điệp)* ĐẠT, lệch 1 bit ⇒ False; đối chiếu `openssl dgst -sha256 -sign` *(khoá prime256v1 sinh mới)* ⇒ True, thông điệp khác ⇒ False. ⓔ 11 cách giả JWT *(alg none · HS256 · kid lạ · khoá khác · iss · hết hạn · iat tương lai · aud ghim · thiếu email · sửa thân · ⛔ JWT)* ⇒ đúng lý do. ⓕ `actor` = `--nguoi-ky` (bài `test_che_do_ghi_dat_actor_NGUOI_KY`); email IAP CHỈ vào nhật ký (`test_cong_JWT_dung_…_ghi_ai_vao`). ⓖ **Đo trên GCP** = 7 mục BÁO CÁO: `NGOÀI · GET / ⛔ cookie ⇒ 302` · `⇒ trang Google` · `GET API ⇒ 302` · `POST API ⇒ 401` · `đường vào ⛔ qua IAP (đếm) = 0` · `TRONG · cổng: yêu cầu ⛔ JWT ⇒ 403` · `JWT chữ ký GIẢ ⇒ 403`. |
| **AC-3** script | `test_07_link_web.py` 37 bài trên gcloud + curl GIẢ: dựng từ trống ⇒ ĐẠT **29/29** mục `mong` + `⭐ LINK`; lệnh GHI ⊆ 8 loại cho phép, **0** lệnh `compute`/`firewall`/`sql users`/`delete`; tác tử IAP TẠO trước khi gán quyền; deploy có `--iap` `--no-allow-unauthenticated` `--max-instances=1` …, ⛔ `--allow-unauthenticated`; `--kiem` **0** lệnh ghi + trạng thái y nguyên; chạy lại được; tag chưa có ⇒ dựng ảnh *(ngữ cảnh chứa `cong_iap.py` + `vao_cloud_run.sh`)*; build hỏng ⇒ `BUILD_LOI` + ⛔ deploy; GA ⛔ biết `--iap` ⇒ beta ⇒ ĐẠT; `allUsers` cũ ⇒ `--kiem` ĐỎ 2 mục, dựng ⇒ GỠ ⇒ ĐẠT; **14 phép phá** ⇒ ĐÚNG tập mục ĐỎ *(so bằng `==`)*; project trống ⇒ **0** mục ĐẠT, 28 ĐỎ; 7 tham số xấu ⇒ exit 2, 0 lệnh gcloud; đầu ra ⛔ email. **Giả mô phỏng hành vi GCP có thể làm hỏng script** (bài học 23/11): tác tử IAP chưa tồn tại ⇒ "does not exist" *(bài `test_gia_tac_tu_IAP_chua_tao…` chứng giả có răng)* · `--iap` chỉ ở beta · `--no-allow-unauthenticated` ⛔ gỡ `allUsers` cũ *(bi quan — G-4)* · deploy ảnh chưa có ⇒ đỏ · `.gcloudignore`/BuildKit giữ nguyên mô hình cũ. |
| **AC-4** dữ liệu | Cùng Cloud SQL `fls-staging`, cùng SA `fls-staging-app`, cùng `vao.sh` (bí mật từ Secret Manager LÚC CHẠY; `doc` ⇒ `fls_doc`, `ghi` ⇒ `fls_ghi`). 07 ⛔ gọi lệnh `sql users` / `secrets` / `projects add-iam-policy-binding` nào *(bài lệnh GHI)*; biến môi trường service ⛔ có khoá nào khớp `secret\|pass\|jwt\|dsn` *(bài `test_che_do_ghi…`)*. |
| **AC-5** | README + UAT **v0.5**; cổng §1; `--duong-nen` §1.1. |
| **AC-6** *(bổ sung 24/11)* đăng nhập FLS | `test_cong_iap.py` ⓔ 10 bài, cổng THẬT + Secret Manager giả mang bản ghi băm: ⛔ phiên ⇒ API **401** `FLS-CHUA-DANG-NHAP`, `/` + `/phien.js` ⇒ **303 `/login`**, POST ghi ⇒ 401, cookie giả ⇒ 303, `/login` ⛔ JWT IAP ⇒ 403 (đăng nhập nằm SAU IAP), cửa ghi **0** yêu cầu · đúng ⇒ 303 `/` + `Set-Cookie` đủ `HttpOnly` `Secure` `SameSite=Strict` `Path=/` `Max-Age=28800`, đi qua 207, `Cookie` ⛔ tới cửa · cookie ⛔ dùng được cho email IAP khác · `/logout` ⇒ `Max-Age=0` + thu hồi (dùng lại ⇒ 401) · sai ⇒ **401**, tên sai ⇒ 401, lần 5 ⇒ **429** + `Retry-After`, mật khẩu ĐÚNG lúc khoá ⇒ vẫn 429, email IAP khác vẫn vào · chưa đặt tài khoản ⇒ `/login` 503, ⛔ ai vào · nhật ký ⛔ mật khẩu (kể cả mật khẩu sai) · scrypt đúng/sai/bản ghi hỏng (N quá lớn ⇒ từ chối) · khoá theo email + hết khoá + cửa sổ trượt · phiên: email khác · sửa chữ ký · đổi mật khẩu · hết hạn · thu hồi · `TU_DO dang_nhap` đúng HAI chiều. Bài cửa-thật: chưa đăng nhập ⇒ `/phien.js` 303; sau đăng nhập 200. `test_08_dat_dang_nhap.py` 13 bài: chỉ băm lên bí mật · mật khẩu ⛔ trong đầu ra / argv gcloud · gõ lại khác · ngắn · trùng tên ⇒ exit 2 + 0 lệnh ghi · chạy lại = phiên bản mới, ⛔ xoá cũ · `--kiem` chỉ đọc + ĐỎ 4 mục có tên khi chưa đặt · bản ghi thô ⇒ ĐỎ đúng 1 mục · tĩnh: `read -rs` ×2, ⛔ `echo $MK`. `test_07`: chưa chạy 08 ⇒ ĐỎ đúng 3 mục đăng nhập. |

**Đột biến (Đ5 — phá, chạy, xem cắn, trả nguyên; nền `test_07` lúc đo có 1 bài chờ commit):** `kiem_es256 → True` ⇒ 5 ĐỎ · bỏ kiểm "thiếu JWT" ⇒ 2 · bỏ kiểm `alg` ⇒ 2 · bỏ chặn ⛔ `K_SERVICE` ⇒ 1 · ⛔ gỡ `X-Goog-*` ⇒ 1 · khoá hỏng trả 403 thay 503 ⇒ 1 · `wait -n` → `wait $CONG` ⇒ 1 · deploy ⛔ `--iap` ⇒ 22 · bỏ tạo tác tử IAP ⇒ 22 · bỏ gỡ `allUsers` ⇒ 1 · `--max-instances=3` ⇒ 22 · bỏ thử beta ⇒ 1 · mục "cửa CHỈ nghe" đọc hằng ⇒ 3 · ⛔ cấp IAP cho người chạy ⇒ 22. **14/14 bị bắt.**
**Đột biến phần đăng nhập:** `khop → True` ⇒ 2 · ⛔ khoá sau 5 lần ⇒ 2 · ⛔ so email phiên ⇒ 2 · ⛔ xét thu hồi ⇒ 2 · cookie ⛔ `HttpOnly` ⇒ 1 · ⛔ xét hết hạn ⇒ 1 · cổng ⛔ đòi phiên ⇒ 4 · chuyển tiếp `Cookie` ⇒ 1 · ⛔ xét khoá trước so khớp ⇒ 1 · `TU_DO dang_nhap` gắn cứng ⇒ **lọt** bài cũ ⇒ thêm `test_tu_do_bao_dang_nhap_DUNG_ca_hai_chieu` ⇒ 1 · 08 ⛔ cấp SA ⇒ 4 · 08 ⛔ hỏi lại ⇒ 2 · 08 ⛔ so hai lần gõ ⇒ 1. **13/13 bị bắt** *(sau khi vá lỗ hổng bài)*. Tổng **27/27**.

## 3 · Thiết kế — so (a) / (b), ĐO + tra tài liệu rồi mới chọn *(AC-1)*

**Nguồn GCP *(tra 24/11)*:** [Configure IAP for Cloud Run](https://docs.cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run) *(lệnh `gcloud run deploy --iap`, `gcloud iap web add-iam-policy-binding --resource-type=cloud-run`, tác tử IAP cần `run.invoker`, IAP chặn "mọi lối vào kể cả URL `run.app`")* · [Enable IAP for Cloud Run](https://docs.cloud.google.com/iap/docs/enabling-cloud-run) *(khuyên bật IAP **trực tiếp** trên Cloud Run; LB chỉ khi nhiều vùng; LB cần "tên miền trỏ về địa chỉ LB"; OAuth client do Google quản lý ⇒ chỉ người trong tổ chức; IAP gọi Cloud Run bằng `X-Serverless-Authorization`)* · [IAP FAQ](https://docs.cloud.google.com/iap/docs/faq) *(yêu cầu có cookie IAP = "browser request"; POST ⛔ cookie ⇒ 401)* · [Programmatic authentication](https://docs.cloud.google.com/iap/docs/authentication-howto) *(app dùng `Authorization` thì công cụ dùng `Proxy-Authorization`)*. Chú thích `run.googleapis.com/iap-enabled`: chỉ thấy ở [một blog bên thứ ba](https://dev.classmethod.jp/articles/iap-for-cloud-run-googlecloudnext/) ⇒ G-3.

| Tiêu chí | **(a) Cloud Run + IAP tích hợp** ⭐ | (b) HTTPS LB + IAP trước VM hiện có |
|---|---|---|
| Thành phần nghe ngoài loopback | `cong_iap.py` trong container (đã viết, kiểm chữ ký) | **cũng cần** một proxy trên VM nghe IP nội bộ (LB ⛔ chạm loopback) + firewall cho dải LB `130.211.0.0/22` · `35.191.0.0/16` |
| Bước chủ | **2 lệnh** (`07 --kiem`, `07`) + mở URL; console **0** bước nếu người test trong tổ chức *(G-7)* | ≥ **9** tài nguyên gcloud *(nhóm instance + cổng tên · health check · backend service + IAP · URL map · target HTTPS proxy · chứng chỉ · IP toàn cục · forwarding rule · firewall LB)* + **bản ghi DNS ở nhà đăng ký tên miền** + chờ chứng chỉ Google 15–60 phút *(⚠ số chờ: kinh nghiệm phổ biến, ⛔ đo)* |
| Tên miền / chứng chỉ | ⛔ cần — URL `*.run.app` | **cần** *(tài liệu: "A domain name registered to the address of your load balancer")* — chủ chưa khai tên miền ⇒ chặn |
| Chi phí/tháng *(⚠ ƯỚC từ bảng giá công khai, ⛔ đo; chủ kiểm Billing)* | scale-về-0, tính tiền theo yêu cầu: UAT vài giờ/ngày ⇒ **≈ 0–3 USD** *(nằm trong hạn miễn phí 180.000 vCPU-giây/tháng nếu ít người)*; IAP ⛔ thu thêm | forwarding rule ≈ **18 USD** + VM luôn bật ≈ **20–24 USD** *(BG-326 §3)* ⇒ **≈ 40 USD** |
| Cloud SQL | Auth Proxy trong ảnh (`vao.sh` y VM), SA có `cloudsql.client` — ⛔ đổi | ⛔ đổi |
| Thời gian yêu cầu | `--timeout=300` s/yêu cầu; API đo cục bộ ≤ 0,11 s *(BG-326 §3, `WO-051`)*; **chuỗi HD2 ~45 s là LỆNH**, ⛔ HTTP ⇒ ⛔ dính | LB mặc định 30 s backend timeout — vẫn đủ |
| Chạy chuỗi / `--ghi` `hd2_cong.json` | ⚠ **giới hạn**: vẫn ở VM ⇒ F03 trên link đọc tệp **trong ảnh** | giữ nguyên (`docker exec` trên VM) |
| Giữ luật cửa | **CÓ** | **CÓ** |
| Cold start | lần đầu sau nghỉ: bí mật + Auth Proxy + cửa *(cục bộ 1,7 s tới mở cổng — BG-326 §3; GCP ⛔ đo)* | ⛔ có (VM luôn bật) |

⇒ **Chọn (a)**: duy nhất ⛔ cần tên miền, rẻ hơn ≈ 40 USD/tháng, ít bước nhất, cùng mức giữ luật cửa; đổi lại một giới hạn có tên (F03 trên link ⛔ thấy `chạy chuỗi --ghi` ở VM) — UAT U10 xem qua tunnel.

## 4 · Giả định CHƯA đo ở GCP *(mỗi cái: lộ ở đâu)*
| # | Giả định | Lộ ở |
|---|---|---|
| **G-1** ⭐ | Trình duyệt đã có cookie IAP gửi `fetch` kèm `Authorization: Bearer <thẻ FLS>` ⇒ IAP dùng cookie, cho `Authorization` đi qua *(FAQ: có cookie = browser request; IAP gọi Cloud Run bằng `X-Serverless-Authorization`)*. Bối cảnh đáng ngại: Cloud Shell Web Preview 23/11 ⇒ `Failed to fetch` mọi API *(nguyên nhân chưa đo)* | bước **③** / UAT U1. SAI ⇒ màn hiện, ô dữ liệu lỗi 401 *(`FLS-TRA-LOI-LA`)*; đường lùi = tunnel; sửa = màn gửi thẻ ở header khác + cổng đổi về `Authorization` *(đổi `goi_cua.js` — WO mới, ⛔ làm ở đây vì chưa có bằng chứng cần)* |
| G-2 | `--iap` có ở `gcloud run` GA | `gcloud run deploy (exit)`; script tự lùi về beta |
| G-3 | chú thích `run.googleapis.com/iap-enabled: "true"` | mục "IAP bật …" — ĐỎ mà console báo bật ⇒ gửi `… --format=export \| grep -i iap` |
| G-4 | `--no-allow-unauthenticated` ⛔ gỡ binding `allUsers` cũ *(giả bi quan)* | script GỠ tường minh — đúng cả hai chiều |
| G-5 | deploy khởi động một instance ⇒ có `TU_DO` mà ⛔ cần ai mở link | mục "TRONG container · dòng TU_DO …" |
| G-6 | ⛔ cookie: GET ⇒ 302 về Google, POST ⇒ 401 | 4 mục `NGOÀI · …` (máy chủ chuyển tới in ra) |
| G-7 | `fp-a-project` thuộc tổ chức; người test trong tổ chức | người ngoài bị Google từ chối ở ③ ⇒ cần OAuth consent "External" + client riêng *(console)* |
| G-8 | container ra được Cloud SQL (IP công khai) + `www.gstatic.com` | `TRONG · màn hình …` *(cửa chỉ lên khi nối được kho)* · `TRONG · khoá công khai IAP …` |

## 5 · Phát hiện trong lúc làm
- **Bài chập chờn là của BÀI** *(Đ3)*: bài cửa-thật bản đầu ĐỎ **4/10** lượt với `TU_DO man_hinh=000`. Dò 3 bước *(① giả thuyết TCP tự-nối ⇒ đo `getsockname == getpeername` = False ở mọi lượt ⇒ BÁC; ② in người trả lời ⇒ cửa thật trả 200 cho `--doi-cua`; ③ thứ tự)*: bài gọi rồi **giết cửa** trước khi `TU_DO` *(khởi động python + lấy khoá)* kịp đo. Sửa bài: chờ dòng `TU_DO` rồi mới gọi/giết ⇒ **10/10** ĐẠT. `--doi-cua` đổi sang chờ câu trả lời HTTP *(chặt hơn TCP — giữ)*.
- `khop_owner --kiem` / `kiem_so_song` ĐỎ có sẵn ở nền — §1.

## 6 · Kho thật
- `KHONG_CHAM` — ⛔ kho THẬT, ⛔ gcloud thật, ⛔ GCP. Bài dùng kho scratch `fls_stg_<pid>` trên cụm 5434 *(dọn khi xong)*.

## 7 · CÂU CHỦ
| # | Câu | Khuyến nghị |
|---|---|---|
| **W1** | Người test có tài khoản **trong tổ chức** Google của `fp-a-project` không? | Có ⇒ ⛔ làm gì thêm. Không ⇒ cần OAuth consent "External" + OAuth client riêng *(console, ~10 phút — Dev soạn hướng dẫn khi chủ trả lời)* |
| **W2** | Giữ VM chạy 24/7 hay tắt ngoài giờ? Link ⛔ phụ thuộc VM | Tắt VM (`stop`) ngoài lúc "chạy chuỗi" ⇒ ≈ 2–3 USD/tháng (đĩa) |
| **W4** | Mật khẩu chung `HondurasGesha` báo người test qua kênh nào? | Kênh riêng từng người (⛔ chat nhóm, ⛔ phiếu); đổi mật khẩu = chạy lại 08 (≤ 1 phút, mọi phiên cũ mất) khi có người rời nhóm |
| **W3** | **SSO theo người (phase sau)**: IAP đã biết email người vào ⇒ có thể phát thẻ FLS **theo email IAP** thay thẻ chung — đóng `GAP-WEB-01` ở staging. Đổi luật ký ⇒ cần BA/PO + WO riêng | Chưa làm (WO cấm đổi luật ký); ghi backlog sau UAT |

## 8 · Cách chạy để xem *(⛔ GCP)*
- `bash tools/staging/07_link_web.sh --project du-an-gia --tag thu-tag` với `PATH` trỏ `gcloud`/`curl` giả + `FLS_GIA_TRANG_THAI` *(xem `Gcp` trong `tests/staging/test_07_link_web.py`)*.
- Cổng cục bộ: `K_SERVICE=x PORT=8080 bash tools/staging/app/vao_cloud_run.sh` cùng biến của `vao.sh` *(bài `test_vao_cloud_run_cua_that…`)*.

## 9 · Dev tự thấy còn yếu *(Test soi chỗ này trước)*
- **Đăng nhập** *(bổ sung)*: ① thời gian hằng chỉ canh bằng bài TĨNH (`compare_digest` có mặt) + thiết kế "tên sai vẫn chạy scrypt" — ⛔ đo thời gian; lần tên sai ĐẦU TIÊN của một instance tốn thêm một lần scrypt (sinh bản ghi mồi). ② khoá tạm + thu hồi phiên sống trong BỘ NHỚ của instance — Cloud Run dựng instance mới *(scale-về-0, revision mới)* ⇒ đếm sai về 0 và phiên đã `/logout` (cookie đã xoá ở trình duyệt) về lý thuyết dùng lại được tới hết hạn nếu ai giữ bản sao cookie. `--max-instances=1` nên ⛔ có hai bộ đếm song song. ③ khoá theo email IAP ⇒ một người có NHIỀU tài khoản Google được cấp IAP thì đoán được 5 lần × số tài khoản / 15 phút. ④ ⛔ nút đăng xuất trên màn hình FLS (⛔ đổi `fls/web/tep`) — người test gõ `/logout`. ⑤ `/login` ⛔ CSRF token — dựa `SameSite=Strict` + IAP.
- **G-1 là rủi ro lớn nhất** và ⛔ thử được ngoài GCP: bài chỉ chứng `Authorization` đi qua **cổng của ta**, ⛔ chứng IAP cho nó qua. Nếu SAI, link chỉ còn vỏ màn hình.
- **ES256 tự viết** *(~40 dòng toán)*: ghim bằng 2 vectơ RFC + `openssl` + 11 cách giả — nhưng ⛔ thời gian hằng *(chỉ KIỂM khoá công khai, ⛔ ký — ⛔ rò bí mật)*; khoá cache 1 giờ, IAP đổi khoá giữa chừng ⇒ tối đa 1 giờ 403 *(kid lạ)* — chưa có "kid lạ ⇒ lấy lại khoá ngay".
- `aud` ⛔ ghim mặc định *(chưa biết khuôn `aud` của Cloud Run IAP)*: cổng in `IAP_AUD …` lần đầu ⇒ sau lần chạy thật nên ghim `FLS_IAP_AUD` *(một `--update-env-vars`)*. Không ghim thì JWT IAP của **service khác cùng project/khoá Google** vẫn qua chữ ký — chỉ khi kẻ ấy đã qua IAP của service khác *và* tới được cổng này mà ⛔ qua IAP của nó (IAP chặn mọi lối vào ⇒ chưa thấy đường).
- Chi phí (a)/(b) là **ước**, ⛔ đo.
- `TU_DO` lấy dòng MỚI NHẤT trong 7 ngày và so `revision` — instance cũ của cùng revision in lại cũng khớp *(đúng ý)*; nhưng nếu Cloud Logging trễ > thời gian chủ chờ ⇒ ĐỎ giả, chạy lại `--kiem`.
- Chế độ `ghi` trên Cloud Run: `--max-instances=1` nhưng Cloud Run có thể **tạm có 2 instance** khi chuyển revision *(chưa đo)* — cùng một thẻ chung, cùng một `actor`, nên ⛔ lệch chữ ký; chỉ là hai tiến trình ghi cùng lúc trong vài giây.

## Đường nền
Xem §1.1 — `KẾT: ĐẠT` @ `86a5003`.

## 12 · Vòng sửa sau R1 (`KQ-365`) — 3 NÊN SỬA + 4/5 GHI NHẬN

*(Dev · 2026-11-25 · cụm PG **5434** · nhánh `claude/bold-galileo-zukpaf-isp/STG-WEB` từ ngọn `78424fa` (KQ-365); ⛔ GCP · ⛔ gcloud thật · ⛔ mật khẩu/băm/khoá thật. Mỗi sửa được chứng minh ĐỎ bằng đột biến — §12.2.)*

| Phát hiện | Mức | Sửa | Bằng chứng *(ĐỎ khi phá → ĐẠT)* |
|---|---|---|---|
| `STG-WEB-R1-01` `aud` ⛔ ghim | NÊN SỬA | Tra tài liệu ["Securing your app with signed headers"](https://docs.cloud.google.com/iap/docs/signed-headers-howto): `aud` Cloud Run = **`/projects/PROJECT_NUMBER/locations/REGION/services/SERVICE_NAME`** ⇒ `07` TÍNH và ghim `FLS_IAP_AUD` ngay ở `run deploy` *(⛔ chờ nhật ký — ⛔ vòng gà-trứng)*. Cổng in `IAP_AUD <aud>` khi khớp và **`IAP_AUD <aud> lech`** khi bị từ chối vì khác aud ghim *(mỗi aud một lần)* ⇒ khuôn sai lộ ra trong nhật ký dù mọi yêu cầu 403. `TU_DO` thêm `aud=ghim\|chua_ghim`. BÁO CÁO 07 +3 mục `mong`: *aud ghim trong service = khuôn* · *TRONG · cổng chạy với aud ghim* · *aud IAP ĐO trong nhật ký = aud ghim* *(chưa ai vào ⇒ giá trị "chưa đo" ⇒ **ĐỎ có tên** — Đ5)*. | `test_aud_GHIM_thieu_aud_cung_403_va_aud_LECH_duoc_ghi_nhat_ky` *(JWT IAP **thiếu** aud ⇒ 403 · aud **app khác** ⇒ 403 · aud đúng ⇒ 200 · nhật ký có dòng `lech`)* · `test_dung_lan_DAU_chua_ai_vao_thi_DO_DUNG_1_muc_aud_do__mo_link_roi_kiem_DAT` · 2 phép phá 07 *(aud ⛔ ghim ⇒ ĐỎ đúng 2 mục · aud đo lệch ⇒ ĐỎ đúng 1 mục)* · deploy có `FLS_IAP_AUD=/projects/…/services/fls-staging-web`. Đột biến: bỏ `FLS_IAP_AUD` khỏi deploy ⇒ **30** ĐỎ; mục "aud ĐO" luôn True ⇒ 1 ĐỎ. |
| `STG-WEB-R1-02` thu hồi + khoá tạm chỉ ở bộ nhớ | NÊN SỬA | **Giải pháp thật** *(⛔ đường lùi `PHIEN_GIAY ≤ 1h + min-instances=1`)*: bí mật RIÊNG **`fls-staging-phien`** = JSON `{khoa, the_he, sai, khoa_toi}`. Cookie `v2.<thế hệ>.<hết hạn>.<email>.<HMAC>`; `/logout` ⇒ `the_he[email] += 1` ⇒ **mọi** cookie cũ của email ấy mất, **kể cả sau khi Cloud Run dựng lại instance**; bộ đếm sai + mốc khoá cũng ghi ở đó. Ghi = `secrets/…:addVersion` (REST, SA) rồi **huỷ** phiên bản vừa đọc *(⛔ dồn phiên bản)*; ghi luôn đọc MỚI trước *(⛔ đè lần xoay khoá của 08)*; đọc giữ 30 s. Đọc hỏng ⇒ ⛔ ai vào (503 · ĐÓNG); ghi hỏng ⇒ vẫn áp trong instance + `⛔ DANG_NHAP_GHI_LOI`. `08` tạo/xoay bí mật này mỗi lần đặt mật khẩu *(khoá mới ⇒ mọi phiên cũ mất, mọi khoá tạm gỡ)* + cấp SA `secretAccessor` + **`secretVersionManager` CHỈ trên bí mật này**. `lay_bi_mat.py` thêm `lay_kem_ten` · `them_phien_ban` · `huy_phien_ban`. | `test_dang_xuat_va_khoa_tam_BEN_qua_KHOI_DONG_LAI__STG_WEB_R1_02` *(Secret Manager GIẢ có ghi, sống ngoài tiến trình cổng: đăng xuất → **giết cổng** → cổng mới ⇒ cookie cũ **401**, cookie "máy thứ hai" cùng email **401**, email đang khoá vẫn **429**, đăng nhập lại **303**; sau 6 lần ghi còn đúng **1** phiên bản chưa huỷ; bí mật ⛔ chứa mật khẩu/băm)* · `test_ghi_trang_thai_HONG…` · `test_CHUA_co_trang_thai_phien_thi_KHONG_ai_vao__DONG` · 08: khoá đổi giữa hai lần đặt, khoá ⛔ trong đầu ra/argv. Đột biến: `dang_xuat` ⛔ tăng thế hệ ⇒ 3 ĐỎ · đăng xuất ⛔ ghi ⇒ 2 · khoá tạm chỉ ghi bộ nhớ ⇒ 1 · ⛔ huỷ phiên bản cũ ⇒ 1 · 08 ⛔ xoay khoá ⇒ 1 · 08 ⛔ cấp `secretVersionManager` ⇒ 4. |
| `STG-WEB-R1-03` `--condition=None` ⛔ bài canh | NÊN SỬA | `gcloud_gia.py`: **mặc định** mô phỏng chính sách dự án CÓ điều kiện *(như `fp-a-project` đo 24/11)* — `projects add-iam-policy-binding` thiếu `--condition` ⇒ exit 1 với lời gcloud *"…policy containing conditions is prohibited in non-interactive mode. Run the command again with `--condition=None`"*. Đồ giả bash của `test_01` cùng hành vi *(⛔ tính là lần thử lan truyền)*. Bài mới `test_iam_dieu_kien.py`: TĨNH — mọi `projects add/remove-iam-policy-binding` trong `tools/staging/*.sh` *(gộp dòng `\`)* có `--condition=None`, tập ≠ rỗng *(đếm **2**: 01 · 03)*, ⛔ script nào khác; ĐỘNG — giả cắn đúng lời, có cờ thì cho qua. | Đột biến R1 từng SÓT: bỏ cờ ở **03** ⇒ **1** ĐỎ *(trước: 49/49 xanh)* · ở **01** ⇒ **4** ĐỎ *(trước: 9/9 xanh)*. |
| `STG-WEB-R1-04` 3 đột biến sót | GHI NHẬN → **sửa** | Tách `DN.kiem_dang_nhap(ten, mk, tk)`: luôn đúng **1** lần scrypt *(bản ghi mồi tính SẴN lúc nạp)*, so cả hai bằng `compare_digest`. Bài đếm lần gọi `hashlib.scrypt` = 1 cho 4 ca *(đúng · sai mật khẩu · sai tên · rỗng)* + AST cấm `==`/`!=` giữa dữ liệu bí mật trong `kiem_dang_nhap` · `khop` · `phien_hop_le`; bài nhật ký ⛔ chứa nửa băm. | (a) `ten == …` ⇒ 1 ĐỎ · (b) in băm vào nhật ký ⇒ 1 ĐỎ · (c) tên sai bỏ scrypt ⇒ 1 ĐỎ *(cả ba từng 81/81 xanh)*. |
| `STG-WEB-R1-05` đọc thân trước JWT | GHI NHẬN → **sửa** | Thứ tự mới: JWT → `Transfer-Encoding: chunked` ⇒ **411** → `Content-Length` > 1 MiB ⇒ **413** → mới đọc thân; từ chối trước khi đọc ⇒ đóng kết nối. `/login` vẫn > 4 KiB ⇒ 413. | `test_than_KHONG_LO_khong_JWT_bi_tu_choi_NGAY…` *(`Content-Length: 50000000`, gửi 3 byte: ⛔ JWT ⇒ **403 < 1 s** · có JWT ⇒ **413 < 1 s** · chunked ⇒ **411**; cửa chạm 0)*. Đột biến đọc thân trước ⇒ 1 ĐỎ. |
| `STG-WEB-R1-06` khoá HMAC suy từ băm | GHI NHẬN → **sửa** | Khoá = 32 byte ngẫu nhiên ở `fls-staging-phien` *(§ `-02`)*. Giới hạn CÒN LẠI *(ghi rõ)*: ai **đọc được `fls-staging-phien`** vẫn rèn được cookie — nhưng đọc `fls-staging-login` (băm) thì ⛔ còn đủ. | `test_khoa_HMAC_KHONG_suy_tu_ban_ghi_bam__STG_WEB_R1_06` *(cookie ký bằng `sha256("fls-phien-v1\|"+băm)` hay bằng băm ⇒ ⛔ hợp lệ)*. Đột biến khoá cố định ⇒ 1 ĐỎ. |
| `STG-WEB-R1-07` khoá chỉ theo email | GHI NHẬN → **sửa** | Thêm bộ đếm toàn cục `*`: **20** lần sai / 15 phút bất kể email ⇒ khoá CHUNG 15 phút. | bài đơn vị: 19 email × 1 lần ⇒ chưa khoá; lần 20 ⇒ email MỚI cũng bị khoá. Đột biến bỏ bộ đếm toàn cục ⇒ 1 ĐỎ. |
| `STG-WEB-R1-08` W4 gọi tên là "mật khẩu" | GHI NHẬN | **Đính chính W4** *(⛔ sửa dòng cũ — biên bản)*: `HondurasGesha` là **TÊN TÀI KHOẢN**. Câu đúng: *"Tên tài khoản chung `HondurasGesha` + mật khẩu chủ đặt ở 08 — báo người test qua kênh nào?"* — khuyến nghị giữ: kênh riêng từng người. | — |

### 12.1 · Khối lệnh CHỦ *(thay khối đầu phiếu)*
```bash
cd ~/fls && git fetch origin claude/bold-galileo-zukpaf-isp/STG-WEB
git switch -C stg-web origin/claude/bold-galileo-zukpaf-isp/STG-WEB && git log --oneline -1   # mong: commit "BG-364 §12"

bash tools/staging/07_link_web.sh --project fp-a-project --kiem   # mong: KẾT: ĐỎ — 34 mục (chưa có gì) — gửi dòng KẾT
bash tools/staging/08_dat_dang_nhap.sh --project fp-a-project      # HỎI mật khẩu MỚI 2 lần, ẩn · mong: KẾT: ĐẠT (8 mục) — gửi BÁO CÁO
bash tools/staging/07_link_web.sh --project fp-a-project           # mong: KẾT: ĐỎ — ĐÚNG 1 mục "aud IAP ĐO … (mở link 1 lần rồi --kiem)"
#   ⇒ mở ⭐ LINK bằng trình duyệt: Google → /login (HondurasGesha + mật khẩu) → F03 hiện SỐ   (phép đo G-1)
bash tools/staging/07_link_web.sh --project fp-a-project --kiem   # mong: KẾT: ĐẠT (34 mục) — gửi BÁO CÁO
#   nếu mục "aud IAP ĐO" ĐỎ với dòng thông tin "… lech": khuôn aud khác tài liệu ⇒ gửi dòng "aud IAP đo trong nhật ký"
```

### 12.2 · Đột biến *(phá → chạy → trả nguyên; `git status` sạch sau mỗi lượt)*
**14/14 bị bắt**: bỏ `FLS_IAP_AUD` ở deploy ⇒ 30 · mục aud ĐO luôn True ⇒ 1 · `dang_xuat` ⛔ tăng thế hệ ⇒ 3 · khoá tạm chỉ ghi bộ nhớ ⇒ 1 · đăng xuất ⛔ ghi ⇒ 2 · tên sai bỏ scrypt ⇒ 1 · `ten ==` ⇒ 1 · in băm vào nhật ký ⇒ 1 *(lượt đầu đột biến hỏng cú pháp ⇒ lỗi import, ⛔ tính; chạy lại đúng ⇒ 1 ĐỎ)* · đọc thân trước JWT ⇒ 1 · bỏ bộ đếm toàn cục ⇒ 1 · khoá HMAC cố định ⇒ 1 · 08 ⛔ cấp `secretVersionManager` ⇒ 4 · 08 ⛔ xoay trạng thái ⇒ 1 · ⛔ huỷ phiên bản cũ ⇒ 1. **Cộng 2 đột biến `--condition=None`** *(03 ⇒ 1 · 01 ⇒ 4)* ⇒ **16/16**.

### 12.3 · Cổng *(cụm 5434 — ⛔ 5433)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/staging` | **219 passed** in 335 s *(205 + 14)* |
| `pytest --collect-only` | **5182** · web **690** — sàn `MONG_PYTEST_TOAN_BO` 5168 → **5182** *(bài ghim cùng commit)* |
| `--duong-nen --cong 5434` *(MỘT lần, một mình)* | **`KẾT: ĐẠT`** @ `ffc2d3a` — toàn bộ `12 failed, 5154 passed, 2 xfailed, 14 errors in 1654.48s` ⇒ tập đỏ + XFAIL **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **5182** *(mong ≥ 5182)* · skipped 0 · deselected 0; web `3 failed, 687 passed` ⇒ **3 = 3** · chạy **690**; 7 phép kiểm môi trường ĐẠT |
| `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` · `test_uat_doc` | ĐẠT *(519 file)* · 11 kept 0 broken · 0 chỗ · 6 passed |

### 12.4 · Dev tự thấy còn yếu
- **Ghi Secret Manager từ cổng** là hành vi GCP CHƯA đo: REST `:addVersion` / `:destroy` bằng token metadata của SA, vai `secretVersionManager` đủ cho cả hai *(theo tài liệu vai; ⛔ đo)*. Sai ⇒ nhật ký `⛔ DANG_NHAP_GHI_LOI` và đăng xuất/khoá tạm chỉ còn hiệu lực trong instance (= hành vi trước vòng sửa) — ⛔ mở cửa. **Giả định G-9** — thêm vào README.
- Mỗi lần sai mật khẩu = 1 lần ghi bí mật *(+1 phiên bản rồi huỷ bản cũ)* — vài chục lần/ngày, chi phí Secret Manager ≈ 0; nhưng kẻ đã qua IAP gõ sai liên tục bị chặn ở lần 5 (email) / 20 (toàn cục) nên số lần ghi bị chặn trên.
- Trạng thái đọc giữ 30 s: đổi mật khẩu bằng 08 thì phiên cũ còn sống tối đa 30 s (khoá cũ còn trong bộ nhớ cổng).
- Đọc được `fls-staging-phien` = rèn được cookie *(giới hạn còn lại của `-06`)*; IAM của bí mật này chỉ SA app + chủ.

## 13 · Vòng sửa tích hợp sau gộp thử (orchestrator 27/11)

*(Dev · 2026-11-27 · cụm PG **5434** · nhánh `claude/bold-galileo-zukpaf-isp/STG-WEB` từ ngọn `bcb01d0` (`KQ-366` R2 cuối ĐẠT).)*

**Vì sao.** Orchestrator gộp thử `isp/STG-WEB` @ `e821562` (+`KQ-366`) vào nhánh làm việc @ `6f996cf` *(đã có AG3: `tools/staging/06_vertex_agent.sh` — 2 binding mức dự án, cả hai `--condition=None`, `KQ-361/362` đã soát)* ⇒ `--duong-nen` **ĐỎ**: tập đỏ 29 = 28 + **1 THÊM** `test_iam_dieu_kien.py::test_tinh_MOI_binding_muc_du_an_co_condition_None` — bài ghim CỨNG tập `{01, 03}` trong câu assert, nên một script ĐÚNG luật (06) cũng làm nó đỏ. Lỗi của BÀI, ⛔ của 06.

| Việc | Làm | Bằng chứng |
|---|---|---|
| ① gộp | `git merge origin/claude/bold-galileo-zukpaf` (@ `6f996cf`) vào `isp/STG-WEB`. 6 xung đột, giải **y cách orchestrator**: sàn ⇒ thu thập thật · `WO-363` ⇒ bản nhánh này · changelog ⇒ giữ CẢ HAI · UAT đầu bảng ⇒ v0.5 của nhánh này · `tools/staging/README.md` ⇒ tiêu đề `01 → 02 → 03 → 04 → 05 → 08 → 07 → UAT` + giữ dòng **05** VÀ dòng **08/07**. Giải từng khối *(⛔ lấy nguyên tệp một bên)* | `grep '<<<<<<<'` = 0 |
| ② sửa bài ĐÚNG ý | Ý bài = *mọi binding mức dự án có `--condition=None`* + *danh sách script có binding mức dự án KHAI ở MỘT chỗ*. Nay: hằng **`KHAI_BINDING_DU_AN`** (kèm lý do từng dòng) = `01` *(cloudsql.client)* · `03` *(iap.tunnelResourceAccessor)* · **`06_vertex_agent.sh`** *(AG3 · `WO-359`, `KQ-361/362`: `roles/aiplatform.user` / `roles/claude.user`)*. Bài kiểm 3 chiều: thiếu cờ · script CHƯA khai · khai THỪA (script ⛔ còn binding). Thêm bài **`test_script_MOI_co_binding_ma_CHUA_khai_thi_DO`** — chứng minh ĐỎ THƯỜNG TRỰC trên bản chép `tools/staging/*.sh` + một script mới *(chưa khai ⇒ cắn; thiếu cờ ⇒ cắn)*. | Chứng minh ĐỎ trên cây THẬT: thêm `tools/staging/99_tam_pha.sh` có binding `--condition=None` mà chưa khai ⇒ **2 ĐỎ** đúng lý do (`CHƯA khai …: ['99_tam_pha.sh']` · `nền phải sạch trước khi phá`); xoá tệp ⇒ **3 passed**; `git status` ⛔ còn tệp tạm |
| ③ môi trường | `pip install -r requirements.txt` *(venv có `anthropic` 2.14.0 cho AG3)*; cụm 5434 bật lại *(container khởi động lại)*; `pg_migrate` ⇒ `khong co gi de ap` · `pg_verify: khop` | — |
| ④ sàn | thu thập cây gộp **5485** = 5484 *(số gộp thử của orchestrator)* + 1 bài mới · web **690**; `MONG_PYTEST_TOAN_BO` = **5485**, bài ghim cùng commit | `tests/test_dung_moi_truong_isp.py` 60 passed |

### 13.1 · Cổng
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5434` *(MỘT lần, một mình; ⛔ 5433)* | *(điền sau khi chạy)* |

