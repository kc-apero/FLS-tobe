# BG-372 — bàn giao `WO-371` · cổng **MCP FLS** CHỈ ĐỌC cho tài khoản Claude của chủ

| | |
|---|---|
| **Thuộc** | `WO-371` |
| **Phát bởi** | `fls-dev` · 2026-11-27 *(phiên cloud · cụm PG **5437**)* |
| **Nhận** | `fls-test` *(R1 `KQ-373` · R2 cuối `KQ-374`)* + **chủ** *(chạy `10` trên `fp-a-project` — §A)* |
| **Commit** | ngọn nhánh `claude/bold-galileo-zukpaf-isp/MCP` *(nền = nhánh làm việc `0164173` — đã có tệp `WO-371`)*. ⚠ **CHƯA** có `isp/STG-WEB` *(orchestrator đang gộp — xem §F `MCP-D-02`)* |
| **Trạng thái** | `CHO_TEST` |

## Kết luận một dòng
Gói `fls/mcp/` (SDK chính thức `mcp` **2.3.0**) chạy **một mã** cho stdio *(Claude Code, `.mcp.json`)* lẫn Streamable HTTP *(connector claude.ai)*; **6 công cụ CHỈ ĐỌC**; SQL chặn **hai lớp** — **19/19** đột biến ghi bị chặn ở **cả hai** lớp đo RIÊNG; xác thực = **OAuth 2.1 do chính FLS phát** (DCR · PKCE · `aud` = URL MCP), đăng nhập **uỷ Google**, chỉ email trong bí mật mới lấy được token; hạ tầng `10_mcp.sh` (service + SA riêng, `cloudsql.client` **có điều kiện**). **+146 bài**, 12 chỗ phá nguồn đều bị bắt; ảnh Docker dựng + chạy thật cục bộ ⇒ bộ đo BÁO CÁO ra đủ `mong`. ⛔ chưa chạy ở GCP — 8 giả định có tên (§E).

## A · Chủ làm gì, theo thứ tự *(~15 phút)*

**① Đưa mã lên Cloud Shell** *(PowerShell trên máy bạn — như README staging cách 2)*:
```powershell
cd C:\Users\Admin\Downloads\FLS-i2
git fetch origin claude/bold-galileo-zukpaf-isp/MCP
git archive --format=tar.gz -o $HOME\Downloads\fls-mcp.tar.gz FETCH_HEAD
```
Cloud Shell › **Upload** `fls-mcp.tar.gz`, rồi:
```bash
rm -rf ~/fls-mcp && mkdir ~/fls-mcp && tar -xzf ~/fls-mcp.tar.gz -C ~/fls-mcp && cd ~/fls-mcp \
  && git init -q && git add -A && git -c user.email=x -c user.name=x commit -qm snap
test -f tools/staging/10_mcp.sh && echo "cây đúng"
bash tools/staging/10_mcp.sh --project fp-a-project --kiem     # ĐO NỀN, ⛔ đổi gì
#   mong: KẾT: ĐỎ (chưa có service). Chép 2 dòng "URL MCP" + "redirect URI …" — dùng ở ② và ④.
```

**② Tạo OAuth client Google** *(Console › **Google Auth Platform**; bấm tay — gcloud ⛔ tạo được client OAuth "Web")*:
1. Nếu dự án chưa có màn đồng ý: **Branding** điền tên `FLS MCP` + email hỗ trợ; **Audience** chọn **Internal** *(chỉ tài khoản trong tổ chức Google Workspace — thêm một lớp chặn; nếu tài khoản của bạn là Gmail cá nhân thì chọn External + thêm chính bạn vào Test users)*. **Data access**: chỉ `openid` + `.../auth/userinfo.email`.
2. **Clients › Create client › Web application** · tên `fls-staging-mcp` · **Authorized redirect URIs** = đúng dòng `redirect URI` ở ① *(dạng `https://fls-staging-mcp-<SỐ>.asia-southeast1.run.app/oauth/google/callback`)* · **Create** — giữ cửa sổ có Client ID + Client secret.

**③ Dựng** *(Cloud Shell)*:
```bash
bash tools/staging/10_mcp.sh --project fp-a-project --oauth-nhap
#   script HỎI Client ID (hiện) + Client secret (gõ ẨN) ⇒ vào bí mật fls-staging-mcp-oauth (⛔ lịch sử shell, ⛔ dòng lệnh)
#   tag ảnh = SHA của "snap" ⇒ Cloud Build 3–6 phút lần đầu
#   mong: KẾT: ĐẠT — 39 mục · gửi lại: TOÀN BỘ từ "── BÁO CÁO" tới "KẾT: …" (⛔ có email/khoá — script ⛔ in)
#   ĐỎ "NGOÀI · …" ngay sau deploy ⇒ chờ 30 giây rồi chạy lại với --kiem (khởi động lạnh)
```

**④ Thêm connector trên claude.ai** *(§B)* ⇒ hỏi Claude *"liệt kê bảng FLS"*.

**⑤ (khi cần)** đổi danh sách người được kết nối: `bash tools/staging/10_mcp.sh --project fp-a-project --cho-phep a@apero.vn,b@apero.vn` *(GHI ĐÈ danh sách — nhớ giữ email của bạn; ⚠ service chỉ đọc danh sách lúc khởi động ⇒ lượt chạy này cũng deploy lại)*.
**Tắt**: `gcloud run services delete fls-staging-mcp --region asia-southeast1`. **Cắt mọi phiên đang mở**: `python3 -c 'import secrets;print(secrets.token_hex(64),end="")' | gcloud secrets versions add fls-staging-mcp-khoa --data-file=-` rồi chạy lại ③ (⛔ `--oauth-nhap`).

## B · Thêm connector trên claude.ai *(tài liệu claude.com, đọc 27/11/2026)*
1. claude.ai › **Settings › Connectors** › **Add custom connector** *(gói Team/Enterprise: **Owner** thêm ở cài đặt tổ chức rồi từng người **Connect**; Free chỉ được 1 connector tuỳ chỉnh)*.
2. **Name** `FLS` · **URL** = dòng `⭐ URL MCP` của BÁO CÁO *(đuôi `/mcp`, đúng nguyên văn — `resource` phải bằng URL người nhập)*.
3. **Advanced / OAuth client**: **ĐỂ TRỐNG** — máy chủ FLS hỗ trợ đăng ký động (DCR). ⚠ *"You can't change authentication settings after you add a connector"* — gõ sai thì xoá connector, thêm lại.
4. **Add** › **Connect** ⇒ trang Google ⇒ chọn tài khoản trong danh sách ⇒ quay về claude.ai *(callback `https://claude.ai/api/mcp/auth_callback`)*. Người ngoài danh sách thấy trang *"Tài khoản này ⛔ có trong danh sách…"* (HTTP 403), ⛔ có token.
5. Trong hội thoại bật công cụ `FLS`. Claude Code cục bộ thì ⛔ cần bước này: `.mcp.json` ở gốc repo tự khai máy chủ stdio (đọc `PG_DSN` cục bộ).

## C · AC → bằng chứng

| AC | Kết quả | Bằng chứng |
|---|---|---|
| AC-1 · máy chủ MCP | **ĐẠT** | `fls/mcp/` *(chọn trong `fls/`, ⛔ `tools/mcp_fls/`: nó DÙNG LẠI tuyến `fls.api` nên là một TẦNG như `fls.api` và phải chịu luật tầng — `fls.mcp` thêm vào hợp đồng 1 ⛔ `psycopg` + bài AST `test_mcp_tang.py` ⛔ `fls.db/repo/web`; vẫn **11 kept**)*. Kết nối TRUYỀN VÀO từ `tools/chay_mcp.py` *(y `chay_cua.py`; tự nổ nếu kết nối ghi được)*. stdio: bài `test_STDIO_tien_trinh_that_dung_lenh_cua_mcp_json` *(tiến trình con thật, SDK `StdioServerParameters`)*; HTTP: uvicorn thật ở `test_xac_thuc_http.py` + ảnh Docker thật (§D). Nguồn tra §G. |
| AC-2 · công cụ CHỈ ĐỌC | **ĐẠT** | 6 công cụ, chú thích `readOnlyHint=True · destructiveHint=False`. `liet_ke_bang` khớp `count(*)` trực tiếp *(27 bảng/view)*; `mo_ta_bang` khớp `information_schema` *(fls_pm_line 18 cột)*; `truy_van_doc` tiền = CHUỖI thập phân, trần 1.000 dòng + 1 MB, `bi_cat`; hết hạn 5 s ⇒ `57014`; `liet_ke_tuyen` = **31** tuyến `GET` ⛔ ghi (tên hàm duy nhất); `goi_tuyen` = kết quả gọi THẲNG `HAM[...]` *(bài so `mot_dong` + `hang_cho_tom`)*, tuyến ghi `sua` ⇒ `KHONG_CO_TUYEN`; `cong` = `GET /gates`. `Email Address`: **0 cột *email*/208 cột · 0/2 dòng PM** *(mẫu số ≠ 0 — Đ3)*, đo QUA MCP. 15 bài `test_cong_cu_pg.py`. |
| AC-3 · xác thực | **ĐẠT** *(cục bộ)* | §3 thiết kế. Bài `test_xac_thuc_http.py` *(20)*: client OAuth **của SDK** đi trọn DCR → `/authorize` → Google GIẢ (RS256 thật) → gọi về → đổi mã PKCE ⇒ 6 công cụ; người ngoài ⇒ **403**, ⛔ mã; Google nói dối ×5 *(khoá lạ · `aud` · `nonce` · chưa xác minh · hết hạn)* ⇒ **401**; ⛔ token ⇒ **401** + `resource_metadata`; `aud` sai · hết hạn · khoá khác · token Google trần ⇒ **401**; token thật của người ngoài / vừa bị gỡ ⇒ **403**; `Origin` lạ ⇒ **403**; redirect lạ khi đăng ký ⇒ **400**; `--http` thiếu biến ⇒ máy **từ chối chạy** ("authless"). Email ⛔ ghim: danh sách từ `FLS_MCP_CHO_PHEP` ⇐ bí mật. |
| AC-4 · hạ tầng | **ĐẠT** *(gcloud GIẢ)* · số THẬT **chờ chủ** | `tools/staging/10_mcp.sh` + `app/vao_mcp.sh` + `app/do_mcp.py`. 14 bài `tests/staging/test_10_mcp.py` trên `gcloud_gia_mcp.py` *(chính sách IAM dự án CÓ điều kiện mặc định; lệnh lạ ⇒ exit 99)*: dựng đủ ⇒ **39/39 ĐẠT**; SA đọc ĐÚNG 4 bí mật; binding dự án của SA = **1** `cloudsql.client` điều kiện `resource.name == "projects/P/instances/fls-staging"`; ⛔ `delete`/`remove`/`set-iam-policy`/`update`; mọi `secrets …` chỉ `fls-staging-*`; email/secret ⛔ ở dòng lệnh, ⛔ ở BÁO CÁO; 6 chỗ phá ⇒ ĐỎ **đúng mục**. Bộ đo `do_mcp.py` chạy vào máy chủ THẬT *(`tests/mcp/test_do_mcp.py`)*: 401 · 403 người ngoài · 200 chủ · INSERT `chan` · số bảng > 0 — ĐỎ khi khoá sai / chủ bị gỡ. |
| AC-5 · nhật ký + giới hạn | **ĐẠT** | Một dòng JSON stderr / lời gọi (Cloud Run ⇒ Cloud Logging): `{"severity","message":"FLS_MCP_GOI","ai","cong_cu","sql_bam"(SHA-256 16 hex),"so_dong","ms","ket_qua"}` — bài đòi ĐÚNG 6 trường, ⛔ chuỗi kho/câu SQL trong vết. Đăng nhập Google cũng ghi (`dang_nhap_google`; người ngoài ⇒ `ai=null`). Trần **60 lời gọi/người/60 s** (cửa sổ trượt; người khác ⛔ liên luỵ). |
| AC-6 · bài | **ĐẠT** | **146** bài mới *(tests/mcp 132 + tests/staging/test_10_mcp.py 14)*; bảng đột biến §D; Đ5 §D.2 — 12 chỗ phá nguồn, mỗi chỗ ≥ 1 bài ĐỎ. |
| AC-7 | xem §D.3 | `requirements.txt` + `mcp>=2.3.0,<3`; `Dockerfile` cài `psycopg` + `mcp`; `lint-imports` 11 kept · `quet_pii_repo` 0 · `kiem_tai_lieu` ĐẠT; sàn 5389 → **5535** = thu thập thật *(bài ghim cùng commit)*. |

## 3 · Thiết kế xác thực *(vì sao ⛔ IAP, ⛔ token Google trần)*
- **IAP ⛔ đứng trước MCP**: connector claude.ai gọi từ hạ tầng Anthropic *("Anthropic's outbound traffic to your server originates from `160.79.104.0/21`")*, ⛔ có cookie/đăng nhập Google của trình duyệt ⇒ IAP chặn nó. IAP **giữ nguyên** cho web app (`07`, `fls-staging-web`); MCP là service **riêng** `fls-staging-mcp`, Cloud Run `allUsers` (bắt buộc để claude.ai chạm được), và **⛔ authless ở tầng ứng dụng**.
- **Google ⛔ làm máy chủ uỷ quyền MCP trực tiếp được**: discovery Google ⛔ có `registration_endpoint`; token Google ⛔ gắn được `aud` = URL MCP (⛔ tìm thấy hỗ trợ RFC 8707) trong khi đặc tả đòi máy chủ *"MUST validate that access tokens were issued specifically for them"* và *"MUST NOT accept or transit any other tokens"*.
- ⇒ **FLS phát token riêng**: `fls1.<payload>.<HMAC-SHA256>` *(khoá 64 byte trong `fls-staging-mcp-khoa`)*, `aud` = `https://…/mcp`, sống 1 giờ *(làm mới 30 ngày)*; Google OIDC chỉ để **biết ai bấm** — `id_token` kiểm chữ ký RS256 theo JWKS · `iss` · `aud` = client id Google của FLS · `exp` · `nonce` · `email_verified`; PKCE S256 ở CẢ hai chặng.
- **Không trạng thái** (Cloud Run scale-về-0): `client_id` = bản ký metadata client; `client_secret` = HMAC(client_id) ⇒ connector ⛔ phải kết nối lại sau mỗi lần service ngủ. Chỉ mã uỷ quyền (5 phút) ở RAM.
- **Danh sách cho phép** kiểm LẠI ở **mỗi** yêu cầu ⇒ gỡ email ⇒ token đang sống của người ấy ⇒ **403** ngay lượt sau. Hai lớp: SDK `required_scopes` + `nguoi_tu_token` kiểm phạm vi.
- `redirect_uri` ⛔ tuỳ ý: `https://claude.ai/api/mcp/auth_callback` (tài liệu) · `https://claude.com/api/mcp/auth_callback` *(⚠ M-4)* · vòng lặp `localhost`.
- **Host/Origin**: `TransportSecuritySettings` chỉ nhận Host = host URL tất định; Origin (nếu có) ∈ {URL, `https://claude.ai`, `https://claude.com`}.

## D · Bằng chứng đo

### D.1 · Bảng đột biến SQL *(`tests/mcp/test_chan_sql_dot_bien.py` — vai đọc dựng như `02b` §1 + `02a`)*

| # | Đột biến | Lớp 1 ứng dụng | Lớp 2 kho *(câu TRẦN, ⛔ qua lớp 1)* |
|---|---|---|---|
| 1 | `INSERT` | `KHONG_PHAI_SELECT` | `25006` read-only |
| 2 | `UPDATE` | `KHONG_PHAI_SELECT` | `25006` |
| 3 | `DELETE` | `KHONG_PHAI_SELECT` | `25006` |
| 4 | `DROP TABLE` | `KHONG_PHAI_SELECT` | `25006` |
| 5 | `TRUNCATE` | `KHONG_PHAI_SELECT` | `25006` |
| 6 | `ALTER TABLE` | `KHONG_PHAI_SELECT` | `25006` |
| 7 | `CREATE TABLE` | `KHONG_PHAI_SELECT` | `25006` |
| 8 | `GRANT` | `KHONG_PHAI_SELECT` | `25006` |
| 9 | `COPY … FROM STDIN` | `KHONG_PHAI_SELECT` | `42501` ⛔ quyền |
| 10 | `COPY … TO '/tmp/…'` | `KHONG_PHAI_SELECT` | `42501` |
| 11 | `COPY … TO STDOUT` | `KHONG_PHAI_SELECT` | `ProgrammingError` *(psycopg từ chối)* |
| 12 | `select 1; delete …` | `NHIEU_CAU` | `42601` *(giao thức mở rộng — thiếu `prepare=True` thì PG chạy CẢ HAI, đo 27/11)* |
| 13 | `select 1 /**/; DELETE …` | `NHIEU_CAU` | `42601` |
| 14 | `WITH x AS (DELETE … RETURNING) SELECT` | `TU_KHOA_CAM` | `25006` |
| 15 | `SELECT … INTO bảng` | `TU_KHOA_CAM` | `25006` |
| 16 | `set_config('transaction_read_only','off',true)` | `HAM_CAM` | `25001` |
| 17 | `set_config('default_transaction_read_only','off',false)` | `HAM_CAM` | chạy nhưng **ROLLBACK hoàn tác** — sau đó `SHOW …` = `on` và `INSERT` ⇒ `25006` |
| 18 | `SET default_transaction_read_only = off` | `KHONG_PHAI_SELECT` | như 17 |
| 19 | `pg_sleep(5)` *(hạn 1 s)* | `HAM_CAM` | `57014` huỷ |

**19/19 chặn ở cả hai lớp**; hậu kiểm: `fls_run`/`fls_itl` của lần nạp mẫu = (1, 3) trước và sau cả bộ, ⛔ bảng `mcp_dot_bien`. Thêm 10 bài: lớp `READ ONLY` **tự đứng vững** khi vai GHI được (vai chủ bảng + `default_transaction_read_only=off` ⇒ 10 câu `25006`). Lớp 1 thuần: 32 bài (10 câu vô hại đi qua — kể cả `'%delete%'` trong chuỗi, `$$…$$`, chú thích lồng; 22 câu chặn có mã — kể cả `"set_config"(…)` trong ngoặc kép, `U&"\0073et_config"`, `FOR SHARE`, chuỗi/chú thích chưa đóng).

### D.2 · Đ5 — phá nguồn, chạy, xem cắn, trả nguyên *(27/11, `git checkout` sau mỗi lần; `git status` sạch)*

| # | Phá | Bài | Kết quả |
|---|---|---|---|
| D1 | bỏ kiểm `aud` | `test_xac_thuc_http.py` | 1 ĐỎ |
| D2 | `BEGIN READ ONLY` ⇒ `BEGIN` | `test_chan_sql_dot_bien.py` | lượt đầu **42/42 XANH** ⇒ thêm 10 bài vai-ghi-được ⇒ **10 ĐỎ** (`MCP-D-01`) |
| D3 | bỏ `prepare=True` | đột biến | 2 ĐỎ *(hai câu)* |
| D4 | danh sách cho phép = mọi email | xác thực | 3 ĐỎ |
| D5 | bỏ kiểm `nonce` | xác thực | 1 ĐỎ |
| D6 | `redirect_uri` tuỳ ý | xác thực | 1 ĐỎ |
| D7 | bỏ `statement_timeout` | đột biến + công cụ | 2 ĐỎ |
| D8 | tắt bảo vệ Host/Origin | xác thực | 1 ĐỎ |
| D9 | `required_scopes=None` | xác thực + bộ đo | 4 ĐỎ *(người ngoài vào được — lớp `nguoi_tu_token` vẫn chặn công cụ, nhưng mã HTTP sai)* |
| D10 | lộ tuyến GHI cho `goi_tuyen` | công cụ | 2 ĐỎ |
| D11 | nhật ký ghi câu SQL | công cụ | 1 ĐỎ |
| D12 | bỏ trần tốc độ | công cụ | 1 ĐỎ |
| +6 | 10_mcp.sh: SA đọc `jwt` · `cloudsql.client` ⛔ điều kiện · đo người ngoài 200 · INSERT lọt · email 0/3 · bộ đo chết | `test_10_mcp.py::test_PHA_…` | 6/6 ĐỎ **đúng mục** |
| +3 | lớp 1 rỗng danh sách cấm | `test_PHA_lop1_…` | lọt ĐÚNG 5 *(CTE_DML · PG_SLEEP · SELECT_INTO · SET_CONFIG ×2)* |

### D.3 · Ảnh Docker THẬT *(cục bộ, `DOCKER_BUILDKIT=0`, ngữ cảnh `ngu_canh_build.sh`)*
Dựng ĐẠT *(cần `--build-arg HTTPS_PROXY` ở container phiên — `MCP-D-03`)*, **471 MB** *(cũ 373)*, uid **10001**. Chạy `tools/chay_mcp.py --http` trong ảnh *(mạng host, kho cục bộ)*: nghe sau **1,71 s**; `do_mcp.py` ⇒ `khong_token=401 · www_resource_metadata=co · prm/as khớp · dang_ky_redirect_la=400 · token_khoa_gia/aud_sai/het_han=401 · nguoi_ngoai=403 · chu_khoi_tao=200 · chu_so_bang=27 · chu_insert=chan · rieng_tu_email=0/0 · chu_cong=23`; nhật ký `FLS_MCP_GOI` đúng khuôn.

### D.4 · Cổng *(§12 cập nhật sau `--duong-nen`)*
`lint-imports` **11 kept, 0 broken** · `quet_pii_repo` **0** · `kiem_tai_lieu` **ĐẠT** · `tests/mcp` + `test_10_mcp.py` **146 passed**.

## E · Giả định CHƯA kiểm *(chỉ lộ ra ở GCP — BÁO CÁO mục nào ĐỎ)*

| # | Giả định | Nếu sai |
|---|---|---|
| M-1 | Cloud Run có URL **tất định** `https://<service>-<số project>.<vùng>.run.app` cho service mới *(⛔ tra lại trong phiên — từ hiểu biết sẵn)* | `URL tất định có trong URL của service` ĐỎ + mọi mục NGOÀI `000` ⇒ đổi `URL_MONG` theo `status.url` |
| M-2 | Chính sách tổ chức cho `allUsers` gọi Cloud Run *(fps-v35 FE công khai ⇒ nhiều khả năng ĐƯỢC)* | `gcloud run deploy (exit)` ĐỎ hoặc `allUsers run.invoker` ĐỎ |
| M-3 | Điều kiện IAM `resource.name == "projects/P/instances/fls-staging"` cho `cloudsql.client` đủ cho connector Cloud Run *(⛔ tra trong phiên)* | `chu_so_bang` = `loi:…`; nhật ký service báo lỗi nối Cloud SQL |
| M-4 | `https://claude.com/api/mcp/auth_callback` — để sẵn, ⛔ thấy trên trang hiện hành | ⛔ hại: thừa một redirect hợp lệ thuộc miền Anthropic |
| M-5 | claude.ai (spec ≤ 2025-11-25) chạy được với máy chủ SDK 2.3.0 chế độ không trạng thái + JSON *(bài đã chạy client SDK `mode="legacy"` + bộ đo bắt tay `2025-06-18`)* | ④ báo lỗi sau Connect ⇒ gửi ảnh chụp |
| M-6 | Khởi động lạnh trên Cloud Run (đọc 4 bí mật + import) < **10 s** claude.ai chờ *(cục bộ 1,71 s ⛔ gồm bí mật; `--cpu-boost`)* | lần Connect đầu báo hết giờ ⇒ bấm lại; kéo dài ⇒ `--min-instances=1` *(tốn tiền)* |
| M-7 | `lay_bi_mat.py` (metadata server) chạy trên Cloud Run như trên VM/07 | service ⛔ Ready, nhật ký `⛔ không lấy được token SA` |
| M-8 | Màn đồng ý **Internal** khả dụng (tài khoản chủ thuộc Workspace) | Google báo `org_internal` ⇒ chọn External + Test users |

**Giới hạn đã biết** *(⛔ lỗi — thiết kế)*: token làm mới ⛔ thu hồi riêng được (không trạng thái) ⇒ cắt bằng xoay khoá *(§A ⑤)*; mã uỷ quyền + trần tốc độ ở RAM *(một instance — `max-instances=1`)*; `revoke` tắt.

## F · Sổ phát hiện *(10 cột như sổ chung — dev tự phát hiện, chờ `fls-test` xác nhận)*

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `MCP-D-01` | MCP | dev | A2 | NÊN SỬA | `tests/mcp/test_chan_sql_dot_bien.py` | Đ5 D2: bỏ `READ ONLY` khỏi `chay_doc` ⇒ 42/42 XANH — vai `fls_doc` tự chặn nên lớp giao dịch ⛔ được canh riêng | thêm bài chạy bằng vai CHỦ bảng + `default_transaction_read_only=off` | mỗi lớp của "hai lớp" phải có bài TỰ đứng khi lớp kia vắng | ĐÃ SỬA (10 bài) |
| `MCP-D-02` | MCP × STG-WEB | dev | B1 | NÊN SỬA | `tests/staging/test_iam_dieu_kien.py` *(nhánh STG-WEB, chưa gộp)* | bài tĩnh của STG-WEB đòi MỌI `projects add-iam-policy-binding` mang `--condition=None` và chỉ ở `01`/`03`; `10_mcp.sh` cố ý có MỘT binding `--condition=expression=…` (AC-4) ⇒ khi gộp hai nhánh bài ấy ĐỎ | lúc gộp: mở rộng bài — cho phép `10_mcp.sh` với `--condition=expression=` đúng `cloudsql.client`, giữ `--condition=None` cho mọi binding còn lại | luật tĩnh phải phân biệt "⛔ điều kiện" với "điều kiện TƯỜNG MINH" | MỞ — chờ gộp |
| `MCP-D-03` | MCP | dev | B2 | GHI NHẬN | `tools/staging/thu_dung_anh.sh:24` | trong container phiên, `docker build` ⛔ ra PyPI nếu ⛔ truyền proxy (`pip … from versions: none`); `--ca ca-bundle.crt` ⇒ `Argument list too long` | dựng tay với `--network host --build-arg HTTPS_PROXY=…` + `agent-proxy-ca.crt` (cách đã dùng ở D.3) | — | GHI NHẬN |
| `MCP-D-04` | MCP | dev | A2 | GHI NHẬN | `fls/mcp/cong_cu.py` `chay_doc` | `COPY … TO STDOUT` làm hỏng kết nối psycopg (ROLLBACK lỗi) | một kết nối MỖI lời gọi (đã làm) | — | GHI NHẬN |
| `MCP-D-05` | MCP | dev | A2 | GHI NHẬN | `fls/mcp/chan_sql.py` | `pg_advisory_lock` chạy được trong giao dịch READ ONLY — CHỈ lớp 1 chặn | giữ lớp 1; kết nối đóng sau mỗi lời gọi nhả khoá | — | GHI NHẬN |

## G · Nguồn tài liệu đã tra *(27/11/2026)*
- MCP spec **2026-07-28** (bản `latest`): `modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http` *(một endpoint POST; Origin ⛔ hợp lệ ⇒ 403; bỏ phiên giao thức)* · `…/basic/authorization` + `security-considerations` *(RFC 9728 PRM; `WWW-Authenticate … resource_metadata`; RFC 8414/OIDC; CIMD SHOULD, DCR MAY-deprecated; `aud` MUST; ⛔ token passthrough; PKCE S256)*.
- SDK `mcp` **2.3.0** (PyPI 2026-10-02) — mã nguồn gói đã cài + `py.sdk.modelcontextprotocol.io/v2/migration/` *(`FastMCP` → `MCPServer`; `Client`; `streamable_http_client`)*; `mcp_types.version.HANDSHAKE_PROTOCOL_VERSIONS` = 2024-11-05…2025-11-25.
- Claude connectors: `claude.com/docs/connectors/building.md` · `…/building/authentication.md` · `…/custom/add-unlisted.md` *(Streamable HTTP; spec auth 2025-03-26/06-18/11-25; DCR + CIMD mặc định; "Use your own OAuth client"; callback `https://claude.ai/api/mcp/auth_callback`; "A `401` is required"; "first entry in … `authorization_servers`"; `resource` = URL nhập; chờ 10 s; egress `160.79.104.0/21`; Owner thêm ở Team/Enterprise)* · bài hỗ trợ 11175166 *(kết nối từ hạ tầng đám mây Anthropic)*.
- Google: `accounts.google.com/.well-known/openid-configuration` *(đọc trực tiếp: ⛔ `registration_endpoint`; S256 có)* · `developers.google.com/identity/openid-connect/openid-connect` *(`aud`, `iss` hai dạng, `email_verified`)*.

## H · Câu cho chủ *(⛔ dev tự quyết)*
- **C1** — Danh sách email được kết nối: mặc định **CHỈ tài khoản đang chạy 10** (đọc `gcloud config get-value account`). Thêm ai? *(lệnh §A ⑤)*
- **C2** — Xác nhận: mọi dữ liệu Claude đọc qua MCP (tên người · tiền · số TK — dữ liệu THẬT staging) **vào ngữ cảnh hội thoại** của tài khoản Claude đó *(và theo chính sách lưu hội thoại của gói Claude bạn dùng)*.

## 12 · `--duong-nen` *(MỘT lần, một mình, cổng 5437)*
- **Lượt 1** @ `a6c5787` — **ĐỎ**: 28 + **1 THÊM** `tests/db/test_khong_ai_tro_lai_kho_that.py::test_khong_file_test_nao_ghi_cung_dia_chi_kho_that` — bài mới `tests/staging/test_10_mcp.py` gõ chuỗi DSN giả có tên kho `fls` *(bài canh làm ĐÚNG việc)*. Sửa @ `e0077a6`: bài dùng `FLS_STG_KHO=kho_thu` (biến sẵn có của `vao_mcp.sh`).
- **Lượt 2** @ `e0077a6` — **`KẾT: ĐẠT`**: toàn bộ `12 failed, 5507 passed, 2 xfailed, 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)* · chạy **5535** (mong ≥ 5535) · skipped 0 · deselected 0; `tests/web` **3 = 3** · chạy **690**; `lint-imports` 11 kept; di trú 27/27 · `pg_verify` 0 lệch; HD1 `9845 / 9967`. `git status --porcelain` sau = **0**.
