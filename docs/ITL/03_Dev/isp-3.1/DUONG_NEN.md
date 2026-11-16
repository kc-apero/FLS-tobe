# ĐƯỜNG NỀN ISP 3.1 — môi trường test ở container cloud

**Version:** v0.3 · **Ngày:** 2026-11-16 · **Chủ sở hữu:** `fls-dev` *(làn BE-CF)* · **Phiếu:** `WO-065` → `BG-066` *(+ vòng sửa sau R1 `KQ-067` + vòng sửa sau R2 `KQ-068`)*

> Ghi THẬT kết quả mọi cổng chạy được ở container cloud, ngay sau bước `S0` của
> `IncrementalStepPlan-FLS-Voi_v3.1.2.md` — **kể cả bài đỏ có sẵn** *(ghi TÊN, ⛔ sửa — ISP Step 0 §3 Loại trừ)*.
> Mọi bước sau của ISP so với **tệp máy-đọc** [`duong_nen_bai_do.txt`](duong_nen_bai_do.txt) *(26 node id — §4.3)*:
> `bash tools/dung_moi_truong_isp.sh --duong-nen` so tập `FAILED`/`ERROR` của lượt với tệp ấy và **ĐỎ cả hai chiều** —
> một bài đỏ **mới** là lỗi của bước ấy; một bài tự xanh *(BỚT)* là tin tốt cần **ghi lại** vào tệp, ⛔ im lặng.
> Bảng §4.1/§4.2 là **biên bản** 16/11, ⛔ phải cổng *(`S0-R1-02`)*.
>
> ⛔ Đây ⛔ phải kho THẬT `fls-pg-1` của owner (O4 = A). Kho `fls` ở đây **RỖNG** — chỉ mang 26 di trú.
> Bước tích hợp cuối (`I2`) chạy lại trên máy owner trước merge.

## 1. Dùng lại — lệnh cho mọi agent của ISP

```bash
# chạy từ gốc worktree của mình (mã `fls` lấy từ thư mục làm việc, ⛔ cài vào venv)
# ⭐ MỖI AGENT MỘT CỤM THEO CỔNG (S0-Q1 = A · TIEN_DO.md): 5433 gốc S0 · 5434 BE-CF · 5435 BE-HC ·
#    5436 FE · 5437 DATA · 5444…5447 reviewer theo làn của bước đang kiểm. Tên kho GIỮ `fls` / `fls_test`.
bash tools/dung_moi_truong_isp.sh --cong <N>              # dựng (chạy lại được) + 7 phép kiểm có `mong`
bash tools/dung_moi_truong_isp.sh --cong <N> --duong-nen  # + pytest toàn bộ + tests/web, SO tập đỏ với duong_nen_bai_do.txt + MẪU SỐ (§4.3)
bash tools/dung_moi_truong_isp.sh --cong <N> --chi-kiem   # ⛔ dựng gì — chỉ kiểm
#   (thay --cong <N> bằng FLS_PG_PORT=<N>; bỏ cả hai ⇒ 5433). Cuối mỗi lượt script IN SẴN hai dòng:
export PG_DSN='postgresql://fls:fls@localhost:<N>/fls'
export PG_DSN_TEST='postgresql://fls:fls@localhost:<N>/fls_test'
export PYTHONUTF8=1
/home/user/FLS-tobe/.venv/bin/python -m pytest <đường dẫn>     # ⛔ thêm -q (pyproject.toml đã có)
/home/user/FLS-tobe/.venv/bin/lint-imports
/home/user/FLS-tobe/.venv/bin/python -m fls.db.pg_migrate
/home/user/FLS-tobe/.venv/bin/python tools/do_voi_so_luong.py
```

⚠ ~~`PG_DSN_TEST=…:5433/fls_test_<làn>`~~ — bỏ *(S0-Q1 = A)*: 19 tệp bài ghim tên kho `== "fls_test"` ⇒ lượt TOÀN BỘ đỏ thêm 131 bài ⛔ phải lỗi mã *(§4.2)*. Cụm theo cổng giữ tên `fls_test`, ⛔ sửa bài nào *(§6.1)*.

| Thứ | Ở đâu | Ghi chú |
|---|---|---|
| venv dùng chung | `/home/user/FLS-tobe/.venv` *(checkout chính, `gitignore`)* | Python 3.13.18 · `psycopg` 3.3.9 · `pytest` 9.2.0 · `import-linter` 2.16 *(`requirements.txt` chỉ ghi cận dưới `>=` — bản cài là bản PyPI mới nhất ngày 16/11)* |
| cụm PostgreSQL 16 | dữ liệu `/home/user/fls-pg16` cho `5433` · `/home/user/fls-pg16-<N>` cho cổng khác *(NGOÀI repo)* · chỉ nghe `localhost` · socket chung `/var/run/postgresql` *(mỗi cổng một tệp `.s.PGSQL.<N>`)* | `initdb` chạy bằng user `postgres` *(từ chối root)*; xác thực socket `peer`, TCP `scram-sha-256`. 16/11 đang chạy: **5433** · **5434** · **5435** |
| role / kho | mỗi cụm: role `fls` mật khẩu `fls` *(trùng mặc định `fls/db/kho.py`)* `LOGIN CREATEDB` · kho `fls` RỖNG chủ `fls` | `tests/conftest.py` DROP + CREATE kho test đầu mỗi phiên ⇒ cần `CREATEDB` |
| khởi động lại cụm | `bash tools/dung_moi_truong_isp.sh --cong <N>` *(thấy cụm tắt ⇒ chỉ `pg_ctl start`)* | tay: `runuser -u postgres -- /usr/lib/postgresql/16/bin/pg_ctl -D <thư mục của cổng> -l <thư mục của cổng>/pg_ctl.log -w start` |

⛔ Script **từ chối ngay** *(exit 2, trước mọi bước, trước cả dòng tiêu đề)* khi: `FLS_CHO_GHI_THAT` đặt · một trong `PGHOST`/`PGHOSTADDR`/`PGPORT`/`PGSERVICE`/`PGSERVICEFILE` **được đặt** *(kể cả rỗng)* · `PG_DSN` *(và `PG_DSN_TEST` nếu đặt)* ⛔ khớp **nguyên chuỗi** `postgresql://<user>:<pass>@(localhost|127.0.0.1):<cổng của lượt>/<[a-z0-9_]+>` *(⛔ query string, ⛔ host khác, cổng phải là cổng của lượt; `<user>` ⛔ chứa `:` `@` `/` `?` `#` hay khoảng trắng, `<pass>` ⛔ chứa `@` `/` `?` `#` hay khoảng trắng — **một** lớp ký tự `LOP_USER`/`LOP_MK` dùng chung với hàm che, đọc theo byte `LC_ALL=C` — v0.3 · `S0-R2-02`)* · cổng ⛔ thuộc tập ISP · đối số ⛔ khai *(hai chế độ, `--cong` thiếu/hai lần/**rỗng**, `FLS_PG_PORT` đặt mà **rỗng**, `--help` kèm đối số khác — v0.3 · `S0-R2-01`)*. ⛔⛔ Bản v0.1 viết *"khi `PG_DSN` ⛔ trỏ `localhost`/`127.0.0.1:5433`"* — **sai** với ba dạng R1 đo được *(`…/fls?port=5999` · `postgresql://x@10.0.0.9:5432/y@localhost:5433/fls` · `PGHOSTADDR=…`)*: chốt glob cũ cho cả ba qua *(§3.3)*. Nó **dừng chuỗi dựng** *(`[ĐỎ] dựng · …`, exit 1, ⛔ tạo role/kho, ⛔ di trú)* khi thư mục dữ liệu có thứ ⛔ phải cụm PG, khi cụm có sẵn khai cổng khác cổng của lượt, khi cổng của lượt đã có một PostgreSQL KHÁC nghe *(trên máy owner 5433 là `fls-pg-1`)*, và **từ chối di trú** khi kho đích có dòng `fls_itl`. Ở `--duong-nen`, dựng **hoặc** K2 *(cụm của mình)* **hoặc** K7 *(kho rỗng)* ĐỎ ⇒ **⛔ chạy pytest** *(`[ĐỎ] pytest · bỏ qua` — `tests/conftest.py` sẽ DROP + CREATE kho test; v0.3 · `S0-R2-04`)*. ⛔ Nó ⛔ bao giờ gọi `docker`. Mọi chỗ in DSN che mật khẩu: dạng URI che từ sau `://<user>:` tới `@` **cuối** dòng *(mật khẩu có `@` thô ⛔ lộ đuôi)*, user ngoài lớp ⇒ che trọn `://***@`, dạng từ khoá che từ `password=` tới **hết** dòng, giá trị có xuống dòng in thành `\n` trước khi che *(v0.3 · `S0-R2-02` — v0.2 viết "`://user:***@`" nhưng hàm che dừng ở khoảng trắng mà khuôn lại nhận khoảng trắng)* — trừ hai dòng `export` cuối lượt khi mật khẩu là mặc định công khai `fls`.

## 2. Pha ĐỎ — trước khi dựng *(16/11, `39524c5`)*

```text
$ python3 -m pytest --version
/usr/local/bin/python3: No module named pytest
exit=1
$ ls /home/user/FLS-tobe/.venv/bin/python
ls: cannot access '/home/user/FLS-tobe/.venv/bin/python': No such file or directory
exit=2
$ /usr/lib/postgresql/16/bin/pg_isready -h localhost -p 5433
localhost:5433 - no response
exit=2
$ python3 -m fls.db.pg_migrate
ModuleNotFoundError: No module named 'psycopg'
exit=1
$ command -v lint-imports
exit=1
$ grep -c "^\[importlinter:contract:" .importlinter
9
```

`bash tools/dung_moi_truong_isp.sh --chi-kiem` trước khi dựng — **6/6 ĐỎ, exit 1**, mỗi dòng vì THIẾU môi trường *(⛔ lỗi cú pháp)*:

```text
  [ĐỎ]  venv + 3 gói              mong: /home/user/FLS-tobe/.venv/bin/python import được psycopg · pytest · importlinter — đo: ⛔
  [ĐỎ]  cụm PG localhost:5433    mong: pg_isready exit 0 — đo: ⛔ trả lời
  [ĐỎ]  role fls LOGIN + CREATEDB  mong: đăng nhập được + rolcreatedb = t — đo: '⛔ nối được'
  [ĐỎ]  di trú + pg_verify        mong: áp = tệp > 0 và 0 lệch — đo: áp '?' / tệp 26 · lệch '?' ·
  [ĐỎ]  lint-imports               mong: Contracts: 11 kept, 0 broken. — đo: ⛔ có /home/user/FLS-tobe/.venv/bin/lint-imports
  [ĐỎ]  HD1 do_voi_so_luong        mong: exit 0 · chay 9845 / co 9967 — đo: ⛔ có venv
══ KẾT: ĐỎ — 6 phép kiểm khác mong hoặc ⛔ đo được
```

Dựng lần đầu *(chưa có hai gói)* — **5 ĐẠT · 1 ĐỎ, exit 1**; cái đỏ là đúng cái phải đỏ:

```text
── di trú: /home/user/FLS-tobe/.venv/bin/python -m fls.db.pg_migrate
   │ da ap 26 migration: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
   │ pg_verify: khop
   └ exit=0
  [ĐỎ]  lint-imports               mong: Contracts: 11 kept, 0 broken. — đo: 'Contracts: 9 kept, 0 broken.' (exit 0)
```

⭐ `S0-B4` **xanh sẵn** — ⛔ phá mã để có đỏ *(ISP Substep 2 ③)*: `do_voi_so_luong.py` là Python thuần đọc ảnh `tests/fixture/`, chạy được cả bằng `python3` hệ thống TRƯỚC khi có venv — exit 0, hàng `Σ  9967  9845 …`. Đánh giá phủ: chính công cụ tự ĐỎ *(exit 1, `⛔ VOI SỐ LƯỢNG ĐỎ`)* khi bất kỳ số nào khác `MONG` *(`so_dong_so` 9967 · `so_dong_ghep_canon` 9845 · `parity_o` 69510/69510 · …)*; script S0 kiểm thêm hai cột `có`/`chạy` của hàng `Σ`.

## 3. Pha XANH — 6 phép kiểm có `mong`

| Phép | `mong` *(khai trong script)* | Đo 16/11 |
|---|---|---|
| venv + 3 gói | import được `psycopg` · `pytest` · `importlinter` | ĐẠT — 3.3.9 · 9.2.0 · 2.16 |
| cụm PG | `pg_isready -h localhost -p 5433` exit 0 | ĐẠT |
| role `fls` | đăng nhập bằng `PG_DSN` + `rolcreatedb = t` | ĐẠT |
| di trú + `pg_verify` | dòng `fls_migration` = số tệp `NNNN_*.sql` > 0 · 0 chỗ lệch *(kết nối CHỈ ĐỌC)* | ĐẠT — **26/26** di trú áp · `pg_verify: khop` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` · exit 0 | ĐẠT — **11 kept, 0 broken** *(9 cũ + `fls.cau_hinh` + `fls.bao_cao`; 105 tệp, 349 phụ thuộc)* |
| HD1 | `do_voi_so_luong.py` exit 0 · hàng `Σ`: `chạy` 9845 · `có` 9967 | ĐẠT — `chay 9845 / co 9967` |

⚠ **Nhãn (Đ4):** `9845` = **dòng** FLS ghép 1-1 với dòng sổ; `9967` = **dòng** sổ AS-IS `ITL Ledge` *(23 kỳ)*. Chuỗi nguyên văn `chay 9845 / co 9967` của ISP/WO ⛔ có trong output công cụ *(grep `fls/`+`tools/` = **0**; 4 lần, đều ở tài liệu spec)* — công cụ in **hàng `Σ`** của bảng, cột 2 = `có`, cột 3 = `chạy`; script S0 đọc hàng ấy rồi in lại theo khuôn spec.

⭐ **Chạy lại được** *(lần hai, cùng ngày)*: mọi bước in `đã có ⇒ giữ` / `bỏ qua`; di trú `khong co gi de ap` · `pg_verify: khop`; `KẾT: ĐẠT`, exit 0. Tắt cụm bằng `pg_ctl stop` rồi chạy lại ⇒ `── cụm: đang tắt ⇒ pg_ctl start` · `KẾT: ĐẠT`.

Hai chốt từ chối ngay *(exit 2)*:

```text
$ FLS_CHO_GHI_THAT=1 bash tools/dung_moi_truong_isp.sh
⛔ FLS_CHO_GHI_THAT đang đặt — tệp này ⛔ được chạy cạnh quyền ghi sổ thật. Gỡ biến rồi chạy lại.
exit=2
$ PG_DSN=postgresql://fls:fls@10.0.0.9:5433/fls bash tools/dung_moi_truong_isp.sh --chi-kiem
⛔ PG_DSN=postgresql://fls:fls@10.0.0.9:5433/fls ⛔ trỏ cụm cục bộ localhost:5433 — từ chối (kho ở đây phải là kho RỖNG cục bộ).
exit=2
```

### 3.1 Phép PHÁ THỬ hai hợp đồng mới *(S0-B3 · AC-3 · Đ5)*

Thêm tạm một dòng `import <module cấm>` vào `__init__.py` của từng gói, chạy `lint-imports`, trả nguyên, so sha256:

```text
$ echo 'import psycopg' >> fls/bao_cao/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 92bffa198321c599 → 92bffa198321c599
$ echo 'import fls.repo' >> fls/bao_cao/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 92bffa198321c599 → 92bffa198321c599
$ echo 'import fls.db' >> fls/bao_cao/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 92bffa198321c599 → 92bffa198321c599
$ echo 'import psycopg' >> fls/cau_hinh/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.cau_hinh la config thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 b85bbac23dc8aeba → b85bbac23dc8aeba
$ echo 'import fls.repo' >> fls/cau_hinh/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.cau_hinh la config thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 b85bbac23dc8aeba → b85bbac23dc8aeba
$ echo 'import fls.db' >> fls/cau_hinh/__init__.py && lint-imports  ⇒  exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.cau_hinh la config thuan, khong duoc biet tang kho BROKEN; · trả nguyên sha256 b85bbac23dc8aeba → b85bbac23dc8aeba
$ lint-imports   (sau khi trả nguyên cả hai gói)
exit=0 · Contracts: 11 kept, 0 broken.
```

**6/6** lượt phá ⇒ đúng **một** hợp đồng vỡ, và là hợp đồng của chính gói bị phá; 6/6 trả nguyên byte-đúng-byte.

### 3.2 Hai lỗi của chính script — tìm ra khi soát lại bản đầu, vá, rồi chứng minh ĐỎ

Bản đầu *(log §2 và lượt 1 của §4 chạy bằng bản này)*: ⓐ một bước dựng hỏng chỉ in một dòng `⛔`, và nếu sáu phép kiểm vẫn xanh *(nhờ một cụm cũ còn chạy)* thì script **exit 0** — báo ĐẠT sai; ⓑ cụm bị từ chối mà vẫn chạy tiếp role/kho/di trú lên `PG_DSN`. Bản vá *(lượt 2 + đối chứng của §4 chạy bằng bản này)*: bước dựng hỏng là `[ĐỎ]`; cụm hỏng ⇒ dừng chuỗi; di trú đếm `fls_itl` qua kết nối CHỈ ĐỌC, > 0 ⇒ từ chối; tên kho tạo lấy từ `PG_DSN`.

```text
$ FLS_PGDATA=<scratchpad>/khong_phai_cum bash tools/dung_moi_truong_isp.sh      # thư mục chứa ghi_chu.txt
⛔ <scratchpad>/khong_phai_cum có dữ liệu mà ⛔ phải cụm PG — TỪ CHỐI (⛔ xoá hộ ai).
  [ĐỎ]  dựng · cụm            bước dựng hỏng hoặc bị từ chối — ⛔ tạo role/kho, ⛔ chạy di trú
══ KẾT: ĐỎ — 1 phép kiểm khác mong hoặc ⛔ đo được
exit=1                                                                            # ghi_chu.txt còn nguyên
$ PG_DSN=…/fls_thu_bao_ve bash tools/dung_moi_truong_isp.sh                       # kho nháp: tạo + 26 di trú
══ KẾT: ĐẠT — mọi phép kiểm khớp mong
$ (chèn 1 dòng fls_itl vào fls_thu_bao_ve) ; PG_DSN=…/fls_thu_bao_ve bash tools/dung_moi_truong_isp.sh
⛔ kho fls_thu_bao_ve có 1 dòng fls_itl ⇒ ⛔ phải kho RỖNG cục bộ — TỪ CHỐI di trú
  [ĐỎ]  dựng · di trú          bước dựng hỏng hoặc bị từ chối (xem dòng ⛔ trên)
══ KẾT: ĐỎ — 1 phép kiểm khác mong hoặc ⛔ đo được
exit=1                                                                            # rồi DROP DATABASE fls_thu_bao_ve
```

Chốt *"cổng 5433 đã có PostgreSQL KHÁC nghe"* — tắt cụm của script, dựng tạm một cụm khác trên 5433:

```text
$ bash tools/dung_moi_truong_isp.sh
── cụm: đã có (PG 16) ⇒ giữ
⛔ cổng 5433 đã có một PostgreSQL KHÁC đang nghe — TỪ CHỐI khởi động cụm thứ hai.
  [ĐỎ]  dựng · cụm            bước dựng hỏng hoặc bị từ chối — ⛔ tạo role/kho, ⛔ chạy di trú
  [ĐỎ]  role fls LOGIN + CREATEDB  mong: đăng nhập được + rolcreatedb = t — đo: '⛔ nối được'
  [ĐỎ]  di trú + pg_verify        mong: áp = tệp > 0 và 0 lệch — đo: … password authentication failed …
══ KẾT: ĐỎ — 3 phép kiểm khác mong hoặc ⛔ đo được
exit=1
── trả nguyên: tắt + gỡ cụm khác, chạy lại script
── cụm: đang tắt ⇒ pg_ctl start
══ KẾT: ĐẠT — mọi phép kiểm khớp mong
exit=0
```

⇒ **3/3** chốt dựng/di trú đã thấy ĐỎ *(thư mục lạ · cổng có PG khác · kho có `fls_itl`)*, cộng **2/2** chốt exit 2 ở §3 *(`FLS_CHO_GHI_THAT` · `PG_DSN` lạ)*.

### 3.3 Vòng sửa sau R1 *(`KQ-067` — 2 NÊN SỬA + 6 GHI NHẬN + S0-Q1 = A)* — ĐỎ trên bản cũ trước, rồi mới sửa

Bản cũ = `tools/dung_moi_truong_isp.sh` @ `afb9e3a` *(chạy TẠI CHỖ trong worktree trước khi sửa, hoặc `git show HEAD:… > tools/_cu_tam.sh` rồi xoá — script lấy `GOC` theo vị trí tệp, nên bản sao đặt ngoài repo đo sai)*. Mỗi dòng: lệnh · exit · dòng nguyên văn.

| Mã | Bản cũ *(ĐỎ = lọt / sai)* | Bản mới |
|---|---|---|
| `S0-R1-01` ⓐ | `PG_DSN='…@localhost:5433/fls?port=5999' … --chi-kiem` ⇒ **exit 1** · qua chốt, K4 `áp 'Is' / tệp 26 · lệch 'the'` | **exit 2** · `⛔ PG_DSN=postgresql://fls:***@localhost:5433/fls?port=5999 ⛔ khớp NGUYÊN CHUỖI …` |
| `S0-R1-01` ⓑ | `PG_DSN='postgresql://x@10.0.0.9:5432/y@localhost:5433/fls'` ⇒ **exit 1** · qua chốt, K4 `áp 'before' / … lệch 'or'` | **exit 2** · cùng câu từ chối |
| `S0-R1-01` ⓒ | `PGHOSTADDR=10.255.255.1` ⇒ **exit 1** · qua chốt, K2 + K3 + K4 nối `10.255.255.1` | **exit 2** · `⛔ biến PGHOSTADDR đang đặt — libpq sẽ gộp nó vào đích nối của PG_DSN …` |
| `S0-R1-03` | `--chi-kiem --la` ⇒ **exit 0** · `KẾT: ĐẠT` | **exit 2** · `⛔ đối số lạ: --la`; `--duong-nen --chi-kiem` ⇒ exit 2 `⛔ hai chế độ cùng lúc` |
| `S0-R1-04` | `PG_DSN=…/postgres --chi-kiem` *(⛔ có `fls_migration`)* ⇒ K4 `đo: áp '^' / tệp 26 · lệch '?'` | K4 `đo: tệp 26 · LOI UndefinedTable: relation "fls_migration" does not exist …` *(một dòng)* |
| `S0-R1-05` | phá thử: `sitecustomize.py` tạm *(scratchpad)* làm rỗng `fls.db.pg_verify.TABLES` ⇒ `[ĐẠT] … pg_verify khớp (0 chỗ lệch)` · `KẾT: ĐẠT` — **xanh trên tập rỗng** *(Đ3)* | `[ĐỎ] … đo: áp '26' / tệp 26 · lệch '0' · so '0' bảng/view` · `KẾT: ĐỎ`; trả nguyên ⇒ `[ĐẠT] 26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` |
| `S0-R1-06` | dòng tiêu đề `PG_DSN = postgresql://fls:fls@…` · dòng từ chối in nguyên mật khẩu | `PG_DSN = postgresql://fls:***@localhost:5433/fls`; dòng từ chối `fls:***@` *(bài `test_S0_R1_06_…`: mật khẩu `bimat123` ⛔ xuất hiện)* |
| `S0-R1-10` K2 | tắt cụm mình, cụm LẠ `initdb` chiếm 5433 ⇒ `[ĐẠT] cụm PG localhost:5433    pg_isready exit 0` | `[ĐỎ] … đo: pg_ctl -D /home/user/fls-pg16 status ≠ 0 (cụm của mình ⛔ chạy)`; dựng ⇒ `⛔ cổng 5433 đã có một PostgreSQL KHÁC đang nghe`; `FLS_PGDATA=/home/user/fls-pg16 --cong 5434` ⇒ K2 `nghe cổng '5433' ≠ 5434`, dựng ⇒ `⛔ cụm … khai port '5433' ≠ cổng của lượt 5434 — TỪ CHỐI`; nhánh ④ *(cha của tiến trình phục vụ)*: thư mục giả `/home/user/fls-pg16-thu-gia` có `postmaster.pid` ghi PID postmaster của cụm **5435** + cổng 5433 ⇒ `pg_ctl status` báo `server is running (PID: 6989)`, ①②③ qua, K2 `[ĐỎ] … tiến trình phục vụ PG_DSN có cha '6769' ≠ postmaster 6989` *(thư mục giả đã gỡ)* |
| `S0-R1-10` K7 | kho nháp `fls_thu_k7` + 1 dòng `fls_itl` ⇒ `--chi-kiem` **6/6 ĐẠT** · exit 0 | `[ĐỎ] kho fls_thu_k7 RỖNG  mong: fls_itl = 0 dòng — đo: '1'` · exit 1 *(kho nháp đã DROP)* |

Bài thử máy cho chốt + CLI: `tests/test_dung_moi_truong_isp.py` *(30 bài, tất định, ⛔ cần PG — mọi ca chạy trong môi trường GIẢ VẮNG)*. Trên bản cũ: **`20 failed, 10 passed in 149.57s`** *(exit 1; 10 bài xanh là các ca bản cũ vốn từ chối được, hoặc từ chối nhầm lý do — `--cong` là đối số lạ)*; trên bản mới: **`30 passed in 0.85s`**. ⚠ Lượt đỏ ấy để lại một pytest TOÀN BỘ mồ côi *(ca `--duong-nen --chi-kiem` lọt chốt CLI ⇒ dựng + pytest; `timeout` chỉ giết `bash`)* — đã `pkill`; từ đó mọi ca của tệp đều chạy với venv ở `/proc/…` *(⛔ tạo nổi)* nên chốt nào hồi quy cũng chỉ ĐỎ nhanh.

### 3.4 Vòng sửa sau R2 *(`KQ-068` — 1 NÊN SỬA + 4 GHI NHẬN)* — ĐỎ trên bản cũ trước, rồi mới sửa

Bản cũ = script @ `fec4dd0` *(chạy TẠI CHỖ trước khi sửa; bài mới chạy thêm trên bản xuất nguyên `git archive fec4dd0` ở scratchpad)*. Cụm **5433** *(cụm gốc S0)*. Log ở scratchpad phiên *(⛔ commit)*.

| Mã | Bản cũ *(ĐỎ = lọt / sai)* | Bản mới |
|---|---|---|
| `S0-R2-01` | `--cong '' --chi-kiem` ⇒ **exit 1** *(chạy cổng 5433)* · `--cong '' --cong 5435` ⇒ chạy 5435 · `FLS_PG_PORT='' … --chi-kiem` ⇒ **exit 1** | cả ba **exit 2** TRƯỚC dòng tiêu đề · `⛔ --cong '' — giá trị RỖNG (biến cổng chưa đặt?) — từ chối, ⛔ rơi về FLS_PG_PORT/5433 …` · `⛔ FLS_PG_PORT đặt mà RỖNG — từ chối …`; "đã thấy `--cong`" là cờ riêng `CO_CONG` |
| `S0-R2-02` | `PG_DSN='postgresql://fls:bi mat9@localhost:5433/fls_thu'` ⇒ QUA chốt, `bi mat9` in ở tiêu đề ×2 + `export` ×2; `fls:ab@cdXYZ@…` ⇒ `fls:***@cdXYZ@localhost…`; `password='a b9Q'` ⇒ `password=*** b9Q'`; phép quét **76** ca *(33 ký tự ⛔ chữ/số + `\t` `\n` `\r` NBSP byte-lẻ-`0xA0`, ở mật khẩu rồi ở tên user)* ⇒ **lộ 15** | khoảng trắng ra NGOÀI lớp ⇒ cả năm DSN trên **exit 2**, câu từ chối `postgresql://fls:***@localhost…` · `password=***` · `postgresql://***@localhost…`; phép quét 76 ca ⇒ **lộ 0** |
| `S0-R2-03` | `PYTEST_ADDOPTS=--lf bash tools/dung_moi_truong_isp.sh --duong-nen` ⇒ toàn bộ `12 failed, 14 errors in 0.97s` ⇒ `[ĐẠT] … 26 = 26` · web `3 failed in 0.45s` ⇒ `[ĐẠT] 3 = 3` · **`KẾT: ĐẠT` exit 0** | `env -u PYTEST_ADDOPTS` ⇒ cùng lệnh chạy ĐỦ bộ bài *(§4.3 lượt chính thức)*; mẫu số có `mong`: phá bằng plugin `PYTEST_PLUGINS` *(đường `env -u` ⛔ chặn)* bỏ chọn mọi bài trừ 26 node ⇒ `12 failed, 2455 deselected, 14 errors` ⇒ `[ĐỎ] … — đo: 26 · thêm 0 · bớt 0 · chạy 26 · skipped 0 · deselected 2455` · web `[ĐỎ] … chạy 3 · deselected 661` · `KẾT: ĐỎ` exit 1 |
| `S0-R2-04` | `FLS_PGDATA=<thư mục ⛔ phải cụm> PYTEST_ADDOPTS=--lf … --duong-nen` ⇒ `[ĐỎ] dựng · cụm` + K2 `[ĐỎ]` mà `── pytest toàn bộ · exit 1` + `── pytest tests/web · exit 1` vẫn chạy; OID `fls_test` @5433 `56552 → 57351` | cùng lệnh ⇒ `[ĐỎ] pytest · bỏ qua  mong: dựng + K2 + K7 ĐẠT trước khi pytest GHI … — đo: dựng ĐỎ (1 bước) · K2 ĐỎ (…) ⇒ ⛔ chạy pytest` · `KẾT: ĐỎ` exit 1; OID `58151 → 58151` |

Bài thử máy: `tests/test_dung_moi_truong_isp.py` **51** bài *(30 cũ + 21 mới)* — trên bản cũ **`20 failed, 31 passed`** *(tại chỗ 2,52 s; bản xuất nguyên `fec4dd0` 2,18 s — cùng 20 node)*; bản mới **`51 passed`**. Bài nghiệm thu ĐỀ XUẤT của R2 *(scratchpad R2, 4 ca, ⛔ commit — làn Dev ⛔ ghi `tests/nghiem_thu/**`)*: `fec4dd0` ⇒ `4 failed` · bản mới ⇒ `4 passed`.

## 4. Đường nền pytest — hai lượt *(S0-B1 · AC-1 · S0-F1 · AC-5)*

Mẫu số *(Đ4 — hai số đếm hai vật khác nhau)*: grep `def test_` trong `tests/**/*.py` = **2.044 hàm** ở **210 tệp** *(khớp ISP §1)*; pytest **thu thập** = **2.430 bài** *(hàm có tham số nhân lên)* — cùng số ở cả ba lượt dưới.

| Lượt | Lệnh *(qua `bash tools/dung_moi_truong_isp.sh --duong-nen`)* | Kho test | Exit | Dòng tổng kết *(nguyên văn)* |
|---|---|---|---|---|
| 1 · toàn bộ | `…/python -m pytest -rfE` | `fls_test_cf` *(quy ước TIEN_DO)* | 1 | `16 failed, 2271 passed, 2 xfailed, 1 warning, 141 errors in 247.09s (0:04:07)` |
| 1 · web | `…/python -m pytest -rfE tests/web` | `fls_test_cf` | 1 | `6 failed, 583 passed, 75 errors in 127.40s (0:02:07)` |
| 2 · toàn bộ | `…/python -m pytest -rfE` | `fls_test` *(mặc định `kho.py`)* | 1 | `12 failed, 2402 passed, 2 xfailed, 14 errors in 304.14s (0:05:04)` |
| 2 · web | `…/python -m pytest -rfE tests/web` | `fls_test` | 1 | `3 failed, 661 passed in 174.51s (0:02:54)` |
| đối chứng · toàn bộ | `…/python -m pytest -rfE -p no:cacheprovider` trên bản **xuất nguyên `39524c5`** *(`git archive`, ⛔ có thay đổi nào của S0)* | `fls_test` | 1 | `12 failed, 2402 passed, 2 xfailed, 1 warning, 14 errors in 304.26s (0:05:04)` |

⭐ **Đọc bảng:** lượt 2 là **đường nền thật** của container. Mọi bài đỏ ở lượt 2 cũng đỏ ở lượt đối chứng trên `39524c5` *(so từng node id: **26 = 26**, chỉ ở một bên = **0**)* ⇒ **đỏ CÓ SẴN, ⛔ do S0**. Lượt 1 đỏ thêm **131** bài — nguyên nhân là TÊN kho test, ⛔ phải mã *(§4.2)*.

⚠ `1 warning` = `SyntaxWarning: invalid escape sequence '\|'` tại `tools/sinh_ban_do_tang.py:214` — Python 3.13 cảnh báo **lúc biên dịch**, nên chỉ in ở lượt biên dịch mới *(lượt 1 và lượt đối chứng trên cây xuất mới)*; lượt 2 đọc `.pyc` nên ⛔ in. Có sẵn, ⛔ sửa.

Bảng dưới **máy sinh** từ hai log `-rfE` *(nhóm theo hai dòng `E` đầu của khối lỗi)* — ⛔ chép tay. Tổng **157** = 16 + 141 của lượt 1 = **26** *(§4.1)* + **131** *(§4.2)*.

### 4.1 Đỏ ở CẢ HAI lượt — **26** bài: sổ thật RỖNG, bài tự ĐỎ đúng luật *(Đ3/Đ5)*

Kho `fls` ở container **RỖNG** *(0 dòng `fls_itl` — chỉ mang di trú)*. Các bài này đọc **sổ thật** *(kho của `PG_DSN`: 12/26 tên bài mang `SO_THAT`/`so_that`, 11 ở `test_mui_thu_luoi.py` "cần kho để lấy dữ liệu thật", 3 ở `test_g_mod_3_…` gọi `dsn_that()`)* và **tự ĐỎ khi tập rỗng** — dòng `E` của cả 26 đều là *"⛔ không đo được: …"* / *"⛔ KHONG DAT — kho khong co dong nao…"* / *"0 khoá `tho` — … TẬP RỖNG"*. Đúng hành vi; sẽ xanh lại khi chạy trên máy có `fls-pg-1` *(bước `I2`, O4)*. Theo nhóm: **11** `tests/api/test_mui_thu_luoi.py` *(ERROR — `kho khong co dong nao co ngay`)* · **3** `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py` *(ERROR — `0 khoá tho`)* · **12** FAILED *(`⛔ không đo được: …`)*.

| # | Bài (pytest node id) | Lượt 1 `fls_test_cf` | Lượt 2 `fls_test` |
|---|---|---|---|
| A1 | `tests/api/test_wo032_v2_bac_da_gan_pg.py::test_AC12_SO_THAT_chi_doc_moi_moi_noi_khop_so_CT_la_MA_hai_cua_danh_sach` | FAILED | FAILED |
| A2 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC2_SO_THAT_chi_doc_ro_MAY_KHONG_de_xuat_dong_khac_tien_te` | FAILED | FAILED |
| A3 | `tests/api/test_wo037_v2_ro_nguoi_hai_cau_pg.py::test_AC11_SO_THAT_chi_doc_nguoi_khac_tien_te_khop_the_vi_sao` | FAILED | FAILED |
| A4 | `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong` | FAILED | FAILED |
| A5 | `tests/nghiem_thu/test_kq021_bo_gan_vong2.py::test_SO_THAT__moi_lenh_ca_1_ca_2__bo_gan_THAT_mo_DUNG_hop` | FAILED | FAILED |
| A6 | `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py::test_CANH_ORACLE_ro_WO037_so_that_khop_tung_pm_line_id` | FAILED | FAILED |
| A7 | `tests/repo/test_wo051_trang_hang_cho_so_that_pg.py::test_AC5_SO_THAT_trang_2_tien_te_NHIEU_DONG_NHAT_trong_2s` | FAILED | FAILED |
| A8 | `tests/repo/test_wo051_trang_hang_cho_so_that_pg.py::test_AC5_SO_THAT_trang_2_MOI_tien_te_co_trang_2_trong_2s` | FAILED | FAILED |
| A9 | `tests/repo/test_wo051_trang_hang_cho_so_that_pg.py::test_AC5_SO_THAT_view_GOM_DUNG_MOT_LAN_moi_trang` | FAILED | FAILED |
| A10 | `tests/web/test_wo022_tien_theo_tien_te_pg.py::test_AC5_KHU_HOI_moi_ps_no_ps_co_cua_SO_THAT_bang_gia_tri_kho` | FAILED | FAILED |
| A11 | `tests/web/test_wo022_v2_o_tien_pg.py::test_AC11_chuoi_o_tien_DAI_NHAT_tren_so_THAT_vua_ngan_sach` | FAILED | FAILED |
| A12 | `tests/web/test_wo042_mot_tap_ky_tu_trang.py::test_AC11_SO_THAT_khong_curr_nao_mang_ky_tu_cua_TAP_o_mep` | FAILED | FAILED |
| A13 | `tests/api/test_mui_thu_luoi.py::test_1_dieu_huong_ban_phim__ca_nam_phim` | ERROR | ERROR |
| A14 | `tests/api/test_mui_thu_luoi.py::test_2_dan_mot_vung__tach_ca_tab_LAN_newline` | ERROR | ERROR |
| A15 | `tests/api/test_mui_thu_luoi.py::test_3_keo_xuong` | ERROR | ERROR |
| A16 | `tests/api/test_mui_thu_luoi.py::test_4_hoan_tac__co_LICH_SU_chu_khong_chi_mot_buoc` | ERROR | ERROR |
| A17 | `tests/api/test_mui_thu_luoi.py::test_5_filter_view__AN_dong_chu_khong_XOA_dong` | ERROR | ERROR |
| A18 | `tests/api/test_mui_thu_luoi.py::test_6_dong_cung_CA_tieu_de_VA_cot_khoa__left_la_TONG_DUNG` | ERROR | ERROR |
| A19 | `tests/api/test_mui_thu_luoi.py::test_7_so_kieu_ke_toan__tabular_nums_va_am_MAU_DO` | ERROR | ERROR |
| A20 | `tests/api/test_mui_thu_luoi.py::test_8_luu_khong_can_bam__gom_lo_va_KHONG_co_nut_Luu` | ERROR | ERROR |
| A21 | `tests/api/test_mui_thu_luoi.py::test_dung_7_cot_sua_duoc__khong_5_khong_10` | ERROR | ERROR |
| A22 | `tests/api/test_mui_thu_luoi.py::test_o_CHI_DOC_khong_bao_gio_mang_lop_sua` | ERROR | ERROR |
| A23 | `tests/api/test_mui_thu_luoi.py::test_tep_TU_CHUA__khong_mang_khong_thu_vien` | ERROR | ERROR |
| A24 | `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py::test_vu_tru_dung_28_cot_co_ten` | ERROR | ERROR |
| A25 | `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py::test_G_MOD_3_ba_ro_PHAN_HOACH_dung_vu_tru` | ERROR | ERROR |
| A26 | `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py::test_ban_CAM_that_su_KHONG_co_trong_kho` | ERROR | ERROR |

### 4.2 Đỏ CHỈ ở lượt 1 — **131** bài: ghim tên kho `== "fls_test"`

**127** ERROR ở setup + **4** FAILED. Đo: `grep -rn '== "fls_test"' tests` = **24** dòng *(không kể dòng `ten_kho(...)` ở `tests/db/test_kho.py:17`)* trên **19** tệp — **5** tệp trong `tests/nghiem_thu/` *(của `fls-test`)*; cộng `tests/db/test_kho.py::test_dsn_test_mac_dinh_la_kho_khac_kho_that` đọc biến môi trường `PG_DSN_TEST`. Dòng `E` đều là `assert '<kho>' == 'fls_test'` hoặc *"⛔ ca này chỉ dựng trên kho TEST, gặp 'fls_test_cf'"*. ⇒ Quy ước *"mỗi agent một kho `fls_test_<làn>`"* (`TIEN_DO.md`) **⛔ dùng được cho lượt toàn bộ** khi chưa đổi 19 tệp này — chuyển orchestrator *(BG-066 · câu Q1)*. ⛔ Sửa ở S0 *(ISP Step 0 §3 Loại trừ; 5 tệp `nghiem_thu` ngoài quyền Dev)*.

| # | Bài (pytest node id) | Lượt 1 `fls_test_cf` | Lượt 2 `fls_test` |
|---|---|---|---|
| B1 | `tests/db/test_kho.py::test_dsn_test_mac_dinh_la_kho_khac_kho_that` | FAILED | pass |
| B2 | `tests/web/test_b3_cuon_va_khoi_dang_gan.py::test_KHOI_DANG_GAN_TO_BANG_CHUNG_nhu_dong_ung_vien` | FAILED | pass |
| B3 | `tests/web/test_wo023_cd_het_gio_va_cau_409.py::test_AC3_rui_ro_3_het_gio_roi_BAM_LAI__409_moi_noi_dung_chuyen` | FAILED | pass |
| B4 | `tests/web/test_wo042_mot_tap_ky_tu_trang.py::test_AC8_PG_30_tren_30_tham_so_TU_HANG_va_GIU_U200B` | FAILED | pass |
| B5 | `tests/api/test_wo023_d_ma_409_pg.py::test_AC4_BON_ca_409_BON_ma_qua_cua_that` | ERROR | pass |
| B6 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC2_lech_BON_cua_la_tri_tuyet_doi_moi_bac_null_CHI_khi_khac_tien_te` | ERROR | pass |
| B7 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC2_bac_MA_lech_DUNG_1_trieu_o_ung_vien_va_toan_so` | ERROR | pass |
| B8 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC4_khoa_to_LUON_CO_tren_moi_gd_va_gd_ds_hai_cua_danh_sach` | ERROR | pass |
| B9 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC4_gd_DA_GAN_dien_giai_chua_so_CT_thi_khoa_to_CHUA_so_ay` | ERROR | pass |
| B10 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC5_toan_so_dong_USD_canh_lenh_VND_la_KHAC_TIEN_TE` | ERROR | pass |
| B11 | `tests/api/test_wo032_khuon_cua_pg.py::test_AC5_KHONG_dong_khac_tien_te_nao_mang_cung_tien_te_ca_trang_toan_so` | ERROR | pass |
| B12 | `tests/api/test_wo032_v2_bac_da_gan_pg.py::test_AC12_lenh_da_gan_ca_B_khop_so_CT_la_bac_MA_lech_500` | ERROR | pass |
| B13 | `tests/api/test_wo032_v2_bac_da_gan_pg.py::test_AC12_lenh_da_gan_MOI_phan_tu_khop_so_CT_la_MA_va_co_ca_MA_lech_khac_0` | ERROR | pass |
| B14 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC1_khop_ma_CHI_khac_tien_te_vao_ro_NGUOI_kem_vi_sao_ma_tien_te` | ERROR | pass |
| B15 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC1_them_dong_VND_cung_ma_thi_lenh_VE_ro_MAY_de_xuat_VND` | ERROR | pass |
| B16 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC1_tien_te_co_KHOANG_TRANG_la_CUNG_tien_te` | ERROR | pass |
| B17 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC1_dem_theo_ro_KHEP_va_khop_danh_sach` | ERROR | pass |
| B18 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC3_bac_MA_cung_tien_te_TRUOC_khac_tien_te_TRUOC_bac_tien` | ERROR | pass |
| B19 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_AC4_gd_ds_KHAC_tien_te_khong_khop_ma_la_bac_KHAC_TIEN_TE` | ERROR | pass |
| B20 | `tests/api/test_wo037_ro_may_theo_cua_ghi_pg.py::test_THE_vi_sao_CHI_CO_khi_khop_ma_chi_khac_tien_te` | ERROR | pass |
| B21 | `tests/api/test_wo037_v2_ro_nguoi_hai_cau_pg.py::test_AC11_ro_tra_NGUOI_KHAC_TIEN_TE_dem_dung_the_vi_sao` | ERROR | pass |
| B22 | `tests/api/test_wo037_v2_ro_nguoi_hai_cau_pg.py::test_AC14_dong_tien_te_KHOANG_TRANG_vao_BAC_TIEN_va_dem_cung_te` | ERROR | pass |
| B23 | `tests/api/test_wo042_mot_tap_cua_that_pg.py::test_AC10_1_dong_NBSP_VND_vao_BAC_TIEN_va_dem_cung_te_THEO_ma_tien_te` | ERROR | pass |
| B24 | `tests/api/test_wo042_mot_tap_cua_that_pg.py::test_AC10_2_lenh_BOM_VND_khop_ma_dong_VND_vao_RO_MAY` | ERROR | pass |
| B25 | `tests/api/test_wo042_mot_tap_cua_that_pg.py::test_AC10_3_cua_GHI_nhan_cap_BOM_VND_khong_KhacTienTe` | ERROR | pass |
| B26 | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_khoi_DANG_GAN_doc_khoa_gd_CUA_THAT_tru_khoa_to` | ERROR | pass |
| B27 | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F3_gd_hai_cua_danh_sach_MANG_khoa_to_ma_khoi_dang_gan_doc` | ERROR | pass |
| B28 | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F2_ung_vien_bac_MA_tien_LECH_thi_lech_KHONG_null` | ERROR | pass |
| B29 | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F1_CANH_cua_ghi_TU_CHOI_cap_khac_tien_te` | ERROR | pass |
| B30 | `tests/nghiem_thu/test_kq031_khoa_man_ghep_va_tien_te.py::test_F1_tim_tien_KHAC_TIEN_TE_cung_so_KHONG_noi_trong_dung_sai` | ERROR | pass |
| B31 | `tests/nghiem_thu/test_kq036_bac_gd_khac_tien_te_va_bac_la.py::test_F2_gd_ds_KHAC_tien_te_khong_khop_ma_KHONG_mang_nhan_CUNG_tien_te` | ERROR | pass |
| B32 | `tests/nghiem_thu/test_kq036_bac_gd_khac_tien_te_va_bac_la.py::test_CANH_khoi_DANG_GAN_bac_MA_than_cua_that_co_chip_1` | ERROR | pass |
| B33 | `tests/nghiem_thu/test_kq036_bac_gd_khac_tien_te_va_bac_la.py::test_F3_khoi_DANG_GAN_bac_LA_in_NGUYEN_TEN` | ERROR | pass |
| B34 | `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py::test_CANH_ca_thuong_dong_tien_vao_BAC_TIEN_qua_ham_that` | ERROR | pass |
| B35 | `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py::test_F2_ca_bien_HAM_THAT_ung_vien_itl_BANG_ma_tien_te` | ERROR | pass |
| B36 | `tests/nghiem_thu/test_kq046_chieu_nguoc_ung_vien_pm_mot_tap.py::test_CANH_chieu_nguoc_ca_thuong_vao_BAC_TIEN` | ERROR | pass |
| B37 | `tests/nghiem_thu/test_kq050_cap_sai_cung_tien_te.py::test_kq050_GAN_sau_khi_luot_lenh_TRUOC_ve_muon_KHONG_mang_itl_ma_cua_lenh_truoc` | ERROR | pass |
| B38 | `tests/nghiem_thu/test_kq050_cap_sai_cung_tien_te.py::test_kq050_SU_THAT_cua_ghi_NHAN_cap_sai_cung_te_trong_dung_sai` | ERROR | pass |
| B39 | `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo` | ERROR | pass |
| B40 | `tests/nghiem_thu/test_kq050_vung_ung_vien_luot_tim.py::test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon` | ERROR | pass |
| B41 | `tests/repo/test_wo023_f_la_ban_dao_pg.py::test_AC8_go_roi_DAO__ban_dao_la_ban_dao_TRUE__cu_go_FALSE` | ERROR | pass |
| B42 | `tests/repo/test_wo023_f_la_ban_dao_pg.py::test_AC8_DAO_roi_XOA_cung_o__cu_xoa_la_ban_dao_FALSE` | ERROR | pass |
| B43 | `tests/repo/test_wo023_f_la_ban_dao_pg.py::test_AC8_MOI_dong_nhat_ky_co_la_ban_dao_kieu_BOOL` | ERROR | pass |
| B44 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[A-1]` | ERROR | pass |
| B45 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[A-7]` | ERROR | pass |
| B46 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[A-50]` | ERROR | pass |
| B47 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[B-1]` | ERROR | pass |
| B48 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[B-7]` | ERROR | pass |
| B49 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[B-50]` | ERROR | pass |
| B50 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[C-1]` | ERROR | pass |
| B51 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[C-7]` | ERROR | pass |
| B52 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[C-50]` | ERROR | pass |
| B53 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[None-1]` | ERROR | pass |
| B54 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[None-7]` | ERROR | pass |
| B55 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro[None-50]` | ERROR | pass |
| B56 | `tests/repo/test_wo051_phan_trang_khong_doi_pg.py::test_AC4_CA_co_du_thu_can_so` | ERROR | pass |
| B57 | `tests/web/test_wo022_tien_theo_tien_te.py::test_AC6_man_f01_lenh_CHAN_MAN_va_hop_TIM_TIEN_lech_0_40` | ERROR | pass |
| B58 | `tests/web/test_wo022_v3_tim_tien_cua_that.py::test_AC16_tim_tien_THAN_CUA_THAT_khop_DUNG_xu_la_TRONG_dung_sai` | ERROR | pass |
| B59 | `tests/web/test_wo022_v3_tim_tien_cua_that.py::test_AC16_MOI_khoa_F01L_doc_tu_than_cua_DEU_CO_trong_CUA_THAT` | ERROR | pass |
| B60 | `tests/web/test_wo022_v3_tim_tien_cua_that.py::test_AC16_KHUON_THU_tu_nhet_cho_itl_candidates_CUNG_phai_la_khuon_cua_that` | ERROR | pass |
| B61 | `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py::test_AC8e_than_GET_journal__MOI_dong_co_la_ban_dao_BOOL` | ERROR | pass |
| B62 | `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py::test_AC8_man_F02_7_DAO_nguoi__XOA_O__RUT_GOI_Y__theo_LOP` | ERROR | pass |
| B63 | `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py::test_AC8c_ghep_bo_ghep__RUT_GOI_Y_khong_doi` | ERROR | pass |
| B64 | `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py::test_AC9_than_GET_ledger__MOI_but_toan_co_nguon__hai_ma` | ERROR | pass |
| B65 | `tests/web/test_wo023_fg_nhat_ky_va_hop_dao_pg.py::test_AC9_hop_DAO_theo_LOP_cua_CHINH_but_toan__may_duoi_nguoi` | ERROR | pass |
| B66 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC10_GAN_cua_tra_422_THAT__dong_loi_trong_khoi_hanh_dong__0_Uncaught` | ERROR | pass |
| B67 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC10_GAN_khi_cua_TREO__nut_khoa__bam_them_0_POST` | ERROR | pass |
| B68 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC11_phim_J_mo_lenh_KE_cua_LOI__vung_ung_vien_noi__0_Uncaught` | ERROR | pass |
| B69 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC11_bam_CHUOT_lai_CUNG_lenh_cua_LOI__man_noi__0_Uncaught` | ERROR | pass |
| B70 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC12_THU_LAI_o_tim_RONG__mot_luot_itl_candidates__danh_sach_ve` | ERROR | pass |
| B71 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC12_THU_LAI_o_tim_CO_CHU__mot_luot_so_q_chu_giu` | ERROR | pass |
| B72 | `tests/web/test_wo023_h_loi_cu_bam_f01g.py::test_AC14_tim_LOI_khi_lenh_moi_dang_tai__khung_ha__cau_loi__thu_lai` | ERROR | pass |
| B73 | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py::test_AC13a_o_tim_itl_da_chon_KHONG_con__bo_chon__ENTER_va_GAN_khong_POST` | ERROR | pass |
| B74 | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py::test_AC13b_o_tim_itl_da_chon_CON__giu_dung_hang_moi__ENTER_mot_POST_dung_itl` | ERROR | pass |
| B75 | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py::test_AC13c_ca_lech_da_bam_GAN_mot_lan_roi_danh_sach_thay__xac_nhan_ve_false` | ERROR | pass |
| B76 | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py::test_AC13d_mo_lenh_mo_lai_CUNG_lenh_itl_da_chon_KHONG_con__0_POST` | ERROR | pass |
| B77 | `tests/web/test_wo023_i_chon_ung_vien_theo_itl.py::test_AC13_doi_sang_lenh_KHAC_van_bo_chon` | ERROR | pass |
| B78 | `tests/web/test_wo032_man_cua_that.py::test_AC1_tim_tien_VND_USD_cung_so_noi_KHAC_TIEN_TE_crit` | ERROR | pass |
| B79 | `tests/web/test_wo032_man_cua_that.py::test_AC3_tim_tien_bac_MA_lech_1_trieu_o_Lech_CO_SO` | ERROR | pass |
| B80 | `tests/web/test_wo032_man_cua_that.py::test_AC3_F01G_nhan_xac_nhan_bac_MA_co_LECH_va_khac_tien_te_KHONG_lech` | ERROR | pass |
| B81 | `tests/web/test_wo032_man_cua_that.py::test_AC3_AC4_khoi_DANG_GAN_than_cua_that_co_chip_LECH_va_MARK_so_CT` | ERROR | pass |
| B82 | `tests/web/test_wo032_man_cua_that.py::test_AC5_toan_so_dong_USD_canh_lenh_VND_chip_KHAC_TIEN_TE_va_bac_la_in_nguyen_ten` | ERROR | pass |
| B83 | `tests/web/test_wo032_man_cua_that.py::test_AC6_tim_tien_RONG_mo_hop_voi_cau_rong_KHONG_TypeError` | ERROR | pass |
| B84 | `tests/web/test_wo032_man_cua_that.py::test_AC7_o_tien_ung_vien_co_TITLE_dung_chuoi_in_than_cua_that` | ERROR | pass |
| B85 | `tests/web/test_wo032_man_cua_that.py::test_AC8_BA_hop_ghep_O_LY_DO_TRONG_van_GUI_va_cua_ghi_may_dien` | ERROR | pass |
| B86 | `tests/web/test_wo032_quet_khoa_cua_that.py::test_AC9_MOI_khoa_F01L_F01G_doc_tu_than_cua_DEU_CO_trong_CUA_THAT` | ERROR | pass |
| B87 | `tests/web/test_wo032_quet_khoa_cua_that.py::test_AC9_KHUON_THU_tu_dung_trong_tests_web_CUNG_la_khuon_cua_that` | ERROR | pass |
| B88 | `tests/web/test_wo032_quet_khoa_cua_that.py::test_WO037_ve_o_gd_doc_VI_SAO_va_CUA_THAT_tra_no_o_the` | ERROR | pass |
| B89 | `tests/web/test_wo032_v2_chu_giai_bac_va_f04.py::test_AC13_chu_giai_MAY_DE_XUAT_dung_mot_va_du_moi_bac_tu_BAC` | ERROR | pass |
| B90 | `tests/web/test_wo032_v2_chu_giai_bac_va_f04.py::test_AC13_chu_giai_TOAN_SO_dung_mot_co_KHAC_TIEN_TE_bang_CHU` | ERROR | pass |
| B91 | `tests/web/test_wo032_v2_chu_giai_bac_va_f04.py::test_AC13_them_BAC_GIA_thi_chu_giai_CO_bac_ay` | ERROR | pass |
| B92 | `tests/web/test_wo032_v2_chu_giai_bac_va_f04.py::test_AC13_danh_sach_RONG_thi_KHONG_chu_giai` | ERROR | pass |
| B93 | `tests/web/test_wo037_man_cua_that.py::test_AC8_o_GIAO_DICH_lenh_khop_ma_khac_tien_te_in_DUNG_cau_vi_sao_cua_cua` | ERROR | pass |
| B94 | `tests/web/test_wo037_man_cua_that.py::test_AC8_o_GIAO_DICH_nam_cau_cu_KHONG_doi` | ERROR | pass |
| B95 | `tests/web/test_wo037_man_cua_that.py::test_AC4_khoi_DANG_GAN_dong_USD_khac_ma_duoi_lenh_VND_chip_KHAC_TIEN_TE` | ERROR | pass |
| B96 | `tests/web/test_wo037_man_cua_that.py::test_AC6_khoi_DANG_GAN_bac_LA_in_NGUYEN_TEN` | ERROR | pass |
| B97 | `tests/web/test_wo037_v2_bang_f01l_cua_that.py::test_AC12_bang_F01L_DUNG_chu_v4_17_so_tu_CUA` | ERROR | pass |
| B98 | `tests/web/test_wo037_v2_bang_f01l_cua_that.py::test_AC12_b_BANG_0_chi_cau_MOT` | ERROR | pass |
| B99 | `tests/web/test_wo037_v2_bang_f01l_cua_that.py::test_AC12_a_BANG_0_van_in_cau_MOT` | ERROR | pass |
| B100 | `tests/web/test_wo037_v2_bang_f01l_cua_that.py::test_AC12_so_LA_DOC_TU_THAN_cua` | ERROR | pass |
| B101 | `tests/web/test_wo042_bon_chuoi_f01l_cua_that.py::test_AC6_bon_chuoi_F01L_DUNG_chu_v4_18_so_tu_CUA` | ERROR | pass |
| B102 | `tests/web/test_wo042_bon_chuoi_f01l_cua_that.py::test_AC6_LY_DO_LO_GIONG_HET_o_a_va_b_va_bang_hang_man` | ERROR | pass |
| B103 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC1_doi_lenh_A_sang_B_luot_A_ve_SAU_ung_vien_la_cua_B` | ERROR | pass |
| B104 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC1_luot_A_ve_TRUOC_khi_B_dang_tai_KHONG_ve_danh_sach_A` | ERROR | pass |
| B105 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC1_dang_tai_lenh_moi_ST_ung_vien_KHONG_con_cua_lenh_truoc` | ERROR | pass |
| B106 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC1_loi_luot_A_CU_KHONG_hien_loi_luot_B_MOI_thi_hien` | ERROR | pass |
| B107 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC2_GAN_sau_khi_doi_lenh_chi_gui_itl_id_cua_B` | ERROR | pass |
| B108 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC2_GAN_luc_lenh_moi_DANG_TAI_KHONG_gui_itl_id_lenh_truoc` | ERROR | pass |
| B109 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC3_o_tim_hai_chu_luot_chu_CU_ve_SAU_ung_vien_la_cua_chu_MOI` | ERROR | pass |
| B110 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC4_doi_ro_khi_luoi_dang_tai_luoi_CHI_hang_ro_dang_chon[sau]` | ERROR | pass |
| B111 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC4_doi_ro_khi_luoi_dang_tai_luoi_CHI_hang_ro_dang_chon[truoc]` | ERROR | pass |
| B112 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC4_QUAY_LAI_khi_luoi_dang_tai_luot_cu_KHONG_do_hang` | ERROR | pass |
| B113 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC5_XEM_THEM_bam_hai_lan_khi_luot_dau_con_bay_MOT_GET_khong_hang_lap` | ERROR | pass |
| B114 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC6_CHI_DOC_xem_them_CHAY_den_het` | ERROR | pass |
| B115 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC6_CHI_DOC_TIM_TIEN_mo_hop_xem_ung_vien_GHEP_khoa_cau_405` | ERROR | pass |
| B116 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC6_CO_GHI_tim_tien_va_GHEP_nhu_nay` | ERROR | pass |
| B117 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC6_F01_nut_GHI_khoa_dung_che_do[chi_doc]` | ERROR | pass |
| B118 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC6_F01_nut_GHI_khoa_dung_che_do[co_ghi]` | ERROR | pass |
| B119 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC7_doi_TIEN_TE_khi_luoi_dang_tai_luoi_la_loc_CUOI[sau]` | ERROR | pass |
| B120 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC7_doi_TIEN_TE_khi_luoi_dang_tai_luoi_la_loc_CUOI[truoc]` | ERROR | pass |
| B121 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC7_doi_MUC_PHU_khi_luoi_dang_tai_luoi_la_loc_CUOI` | ERROR | pass |
| B122 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC7_XEM_THEM_F01_hai_lan_MOT_GET_khong_hang_trung` | ERROR | pass |
| B123 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC8_mo_hai_anh_chup_anh_DAU_ve_SAU_man_la_anh_CUOI` | ERROR | pass |
| B124 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC8_thu_tu_ngay_luot_CU_ve_SAU_KHONG_de_S_thu_tu` | ERROR | pass |
| B125 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC9_loi_danh_sach_co_nut_THU_LAI_bam_tai_lai_MOT_luot[FLS-INTERNAL-M\xe1y g\u1eb7p l\u1ed7i b\xean trong.]` | ERROR | pass |
| B126 | `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC9_loi_danh_sach_co_nut_THU_LAI_bam_tai_lai_MOT_luot[FLS-MAT-KET-NOI-Kh\xf4ng n\u1ed1i \u0111\u01b0\u1ee3c t\u1edbi m\xe1y ch\u1ee7 FLS.]` | ERROR | pass |
| B127 | `tests/web/test_wo051_xem_them_khung_cho.py::test_AC6_XEM_THEM_dang_tai_nut_KHOA_chu_DANG_TAI_THEM_hang_GIU` | ERROR | pass |
| B128 | `tests/web/test_wo051_xem_them_khung_cho.py::test_AC7_XEM_THEM_loi_hang_GIU_cau_loi_va_THU_LAI_dung_con_tro[FLS-INTERNAL-M\xe1y g\u1eb7p l\u1ed7i b\xean trong.]` | ERROR | pass |
| B129 | `tests/web/test_wo051_xem_them_khung_cho.py::test_AC7_XEM_THEM_loi_hang_GIU_cau_loi_va_THU_LAI_dung_con_tro[FLS-MAT-KET-NOI-Kh\xf4ng n\u1ed1i \u0111\u01b0\u1ee3c t\u1edbi m\xe1y ch\u1ee7 FLS.]` | ERROR | pass |
| B130 | `tests/web/test_wo051_xem_them_khung_cho.py::test_AC7_THU_LAI_lai_loi_MOT_dong_loi_khong_chong` | ERROR | pass |
| B131 | `tests/web/test_wo051_xem_them_khung_cho.py::test_AC7_doi_tien_te_khi_XEM_THEM_dang_tai_loi_cu_KHONG_hien` | ERROR | pass |

### 4.3 Tệp máy-đọc `duong_nen_bai_do.txt` — cổng của đường nền *(`S0-R1-02`)*

⛔⛔ Bản v0.1 hứa *"một bài đỏ mới ⛔ có tên ở §4 là lỗi của bước ấy"* nhưng ⛔ máy nào so: `--duong-nen` chỉ `[ĐỎ]` khi pytest ⛔ chạy nổi *(exit ∉ {0, 1})* ⇒ một bài đỏ MỚI vẫn `KẾT: ĐẠT` exit 0; R1 phải tự dựng `comm` trên bảng markdown để so 26 = 26.

- [`duong_nen_bai_do.txt`](duong_nen_bai_do.txt): **26** dòng = 26 node id của §4.1 *(máy trích từ bảng: `awk` khối §4.1 · `sed` cột 2 · `LC_ALL=C sort -u`)*, đã sắp, ⛔ chú thích, ⛔ dòng trống; **3** dòng mang tiền tố `tests/web/` *(A10 · A11 · A12)*.
- `--duong-nen` tách node id từ khối `short test summary info` của `-rfE` *(dòng `FAILED`/`ERROR`, cắt ở ` - ` đầu tiên)*, rồi `comm` với tệp: lượt **toàn bộ** so cả 26; lượt **`tests/web`** so các dòng mang tiền tố `tests/web/`. **THÊM** hay **BỚT** một node ⇒ `[ĐỎ] đường nền …` + in từng node chênh *(`+ THÊM` / `− BỚT`)*. Tệp vắng ⇒ `[ĐỎ]` *(⛔ so được)*; pytest ⛔ có dòng tổng kết ⇒ `[ĐỎ]`. Đổi tệp bằng `FLS_DUONG_NEN_DO=<tệp>` *(dùng cho phép phá thử — ⛔ sửa tệp thật)*.
- Bước nào làm một bài ở đây tự xanh *(BỚT)* hay chấp nhận một bài đỏ mới *(THÊM — cần lý do, ⛔ "có sẵn" khi nó ⛔ đỏ ở bản gốc)* thì **sửa tệp này trong cùng commit** và ghi lý do vào phiếu — đó là điều Đ5 muốn.
- ⚠ Đo *(Đ4)*: tập so là **node id**, ⛔ số bài — lượt sau vòng sửa thu thập **2.460** bài *(2.430 của 16/11 + 30 bài mới của `tests/test_dung_moi_truong_isp.py`)*; tổng thay đổi mà tập đỏ vẫn 26 = 26.
- ⭐ *(v0.3 · `S0-R2-03`)* **MẪU SỐ cũng là cổng.** Tập đỏ bằng nhau trên một bộ bài TEO là xanh giả: R2 đo `PYTEST_ADDOPTS=--lf` ⇒ 26 / 2.460 bài chạy mà `KẾT: ĐẠT`. Nay: ① mọi lượt pytest chạy với `env -u PYTEST_ADDOPTS` *(dòng `── PYTEST_ADDOPTS của shell người gọi = '…' ⇒ GỠ …` khi biến có đặt)*; ② `[ĐẠT] đường nền …` chỉ khi tập khớp **và** dòng tổng kết có `skipped = 0` · `deselected = 0` · số bài **chạy** *(passed + failed + errors + xfailed + xpassed)* ≥ `MONG_PYTEST_TOAN_BO = 2460` / `MONG_PYTEST_WEB = 664` *(hằng khai MỘT chỗ ở script, cạnh `MONG_LINT_KEPT`; `≥` vì bước sau THÊM bài; bước nào XOÁ bài có chủ đích thì sửa hằng + ghi lý do)* — số ấy in **cạnh** `26 = 26`: `tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0) · chạy N bài (mong ≥ 2460) · skipped 0 · deselected 0`. Lệch ⇒ `[ĐỎ]` kèm `chạy · skipped · deselected` đo được. Đường `env -u` ⛔ chặn *(plugin qua `PYTEST_PLUGINS`, `conftest`, `@pytest.mark.skip`)* vẫn bị ② bắt — phá thử ở §3.4.
- ⭐ *(v0.3 · `S0-R2-04`)* Dựng **hoặc** K2 **hoặc** K7 ĐỎ ⇒ **⛔ chạy pytest** *(`[ĐỎ] pytest · bỏ qua`)*: lượt pytest là một bước GHI *(conftest DROP + CREATE kho test)*, ⛔ được chạy trên cụm mà phép kiểm định danh vừa ⛔ chứng minh được là của mình.

**Chứng minh ĐỎ** *(Đ5 — cả hai chiều; tệp thật sha256 `b4e310ea…` trước = sau)*. Tệp TẠM = tệp thật **bỏ** `tests/repo/test_g_mod_3_phan_hoach_truong_pm.py::test_vu_tru_dung_28_cot_co_ten` và **cài** id giả `tests/web/test_khong_ton_tai_pg.py::test_id_GIA_cai_vao_de_thay_BOT`; chạy trên cụm 5434:

```text
$ FLS_DUONG_NEN_DO=<tệp tạm> bash tools/dung_moi_truong_isp.sh --cong 5434 --duong-nen
  ── pytest toàn bộ · exit 1
     13 failed, 2431 passed, 2 xfailed, 14 errors in 313.31s (0:05:13)
  [ĐỎ]  đường nền toàn bộ mong: tập đỏ = 26 node id của duong_nen_tam.txt — đo: 27 · thêm 2 · bớt 1
        + THÊM  tests/db/test_khong_ai_tro_lai_kho_that.py::test_khong_file_test_nao_ghi_cung_dia_chi_kho_that
        + THÊM  tests/repo/test_g_mod_3_phan_hoach_truong_pm.py::test_vu_tru_dung_28_cot_co_ten
        − BỚT   tests/web/test_khong_ton_tai_pg.py::test_id_GIA_cai_vao_de_thay_BOT
  ── pytest tests/web · exit 1
     3 failed, 661 passed in 177.19s (0:02:57)
  [ĐỎ]  đường nền tests/web  mong: tập đỏ = 4 node id của duong_nen_tam.txt (tiền tố tests/web/) — đo: 3 · thêm 0 · bớt 1
        − BỚT   tests/web/test_khong_ton_tai_pg.py::test_id_GIA_cai_vao_de_thay_BOT
══ KẾT: ĐỎ — 2 phép kiểm khác mong hoặc ⛔ đo được
exit=1
```

⭐ **Đỏ THẬT, ngoài kế hoạch** — dòng `+ THÊM tests/db/test_khong_ai_tro_lai_kho_that.py::…` ở trên ⛔ phải do tệp tạm: cùng lúc, lượt 5433 với **tệp thật** cũng ĐỎ đúng một node:

```text
$ bash tools/dung_moi_truong_isp.sh --duong-nen          # 5433, tệp thật, TRƯỚC khi sửa docstring
  [ĐỎ]  đường nền toàn bộ mong: tập đỏ = 26 node id của duong_nen_bai_do.txt — đo: 27 · thêm 1 · bớt 0
        + THÊM  tests/db/test_khong_ai_tro_lai_kho_that.py::test_khong_file_test_nao_ghi_cung_dia_chi_kho_that
  [ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)
══ KẾT: ĐỎ — 1 phép kiểm khác mong hoặc ⛔ đo được
```

— docstring bài mới của chính vòng sửa trích nguyên DSN của R1 *(`postgresql://x@10.0.0.9:5432/y@localhost:5433/fls`)*, và cổng quét mã nguồn cấm chuỗi DSN tận cùng `/fls` trong `tests/`. Cổng đúng ⇒ sửa **docstring** *(viết `/<kho>`)*, ⛔ sửa cổng. Đây đúng loại lỗi bản v0.1 để lọt: bài đỏ **mới** trong lượt toàn bộ — v0.1 sẽ in `KẾT: ĐẠT`.

**Lượt chính thức** *(5433, MỘT MÌNH trên máy, cây cuối — sha256 script/bài/tệp đường nền đo trước lượt = sau)*: chạy **hai** lần, ghi cả hai.

| Lượt | pytest toàn bộ | so tập đỏ toàn bộ | pytest `tests/web` | so tập đỏ web | KẾT |
|---|---|---|---|---|---|
| chính thức 1 | `14 failed, 2430 passed, 2 xfailed, 14 errors in 306.48s (0:05:06)` | `[ĐỎ]` 28 · thêm 2 · bớt 0 — `+ THÊM tests/web/test_wo032_man_cua_that.py::test_AC3_tim_tien_bac_MA_lech_1_trieu_o_Lech_CO_SO` · `+ THÊM …::test_AC7_o_tien_ung_vien_co_TITLE_dung_chuoi_in_than_cua_that` | `3 failed, 661 passed in 176.22s (0:02:56)` | `[ĐẠT]` 3 = 3 | `ĐỎ` · exit 1 |
| chính thức 2 | `12 failed, 2432 passed, 2 xfailed, 14 errors in 304.96s (0:05:04)` | `[ĐẠT]` 26 = 26 *(thêm 0 · bớt 0)* | `3 failed, 661 passed in 174.95s (0:02:54)` | `[ĐẠT]` 3 = 3 | **`ĐẠT` · exit 0** |

⚠ **Lượt 1 đỏ vì một bài CHẬP CHỜN có sẵn, ⛔ do S0** *(đo được, ⛔ đoán)*: hai node ấy XANH ở lượt `tests/web` ngay sau, ở hai lượt toàn bộ trước *(5433 + 5434)* và ở lượt 2. Lỗi: `tests/web/khung_node.py:217` `json.loads(r.stdout.strip().splitlines()[-1])` ⇒ `JSONDecodeError`, mảnh cuối bắt đầu giữa chuỗi HTML *(`</td><td class=\"r num\">2.597.094…`)*. Chuỗi nhân quả: `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py:81` chèn vào `fls_test` dòng `curr = "VND" + chr(0x85)`, số tiền NGẪU NHIÊN *(`:105` `random.randint(10_000, 89_999) * 1000`)*; tệp ấy chạy TRƯỚC `tests/web` trong lượt toàn bộ *(⛔ có trong lượt `tests/web` riêng)*; khi dòng ấy lọt danh sách ứng viên, `JSON.stringify` để nguyên U+0085 *(node 22 đo: `JSON.stringify({curr:"VND\u0085"})` còn mã `85`)* còn `str.splitlines()` tách ở U+0085 *(Python đo: `'{"curr":"VND\x85"}'.splitlines()` ⇒ 2 mảnh; `.split("\n")` ⇒ 1)*. ⛔ Thêm hai node vào tệp đường nền *(đúng khuôn "danh sách miễn trừ để cổng xanh" — cấm)*, ⛔ sửa bài có sẵn *(ngoài phạm vi S0)* ⇒ chuyển orchestrator *(`BG-066` Q7)*. Đến khi sửa gốc: lượt toàn bộ đỏ **chỉ** ở hai node này ⇒ chạy lại và ghi cả hai lượt.

**Lượt chính thức sau vòng sửa R2** *(v0.3 · 5433 · cây code = commit vòng sửa R2 — sha256 script/bài/tệp đường nền trước lượt = sau, cả hai lượt; máy KHÔNG một mình: hai làn khác chạy pytest trên 5434/5436, load 1,1–1,3)*. Mẫu số mới *(Đ4)*: **2.481** bài thu thập = 2.460 + 21 bài mới của `tests/test_dung_moi_truong_isp.py`.

| Lượt | pytest toàn bộ | so tập đỏ + mẫu số toàn bộ | pytest `tests/web` | so tập đỏ + mẫu số web | KẾT |
|---|---|---|---|---|---|
| chính thức 1 · `bash tools/dung_moi_truong_isp.sh --duong-nen` *(08:30–08:38 UTC)* | `12 failed, 2453 passed, 2 xfailed, 14 errors in 315.33s (0:05:15)` | `[ĐẠT]` 26 = 26 *(thêm 0 · bớt 0)* · chạy **2481** bài *(mong ≥ 2460)* · skipped 0 · deselected 0 | `3 failed, 661 passed in 181.60s (0:03:01)` | `[ĐẠT]` 3 = 3 · chạy **664** *(mong ≥ 664)* · skipped 0 · deselected 0 | **`ĐẠT` · exit 0** |
| 2 · `PYTEST_ADDOPTS=--lf bash tools/dung_moi_truong_isp.sh --duong-nen` *(08:39–08:47 UTC — lệnh tái hiện của R2)* | `── PYTEST_ADDOPTS của shell người gọi = '--lf' ⇒ GỠ …` · `12 failed, 2453 passed, 2 xfailed, 14 errors in 312.32s (0:05:12)` | `[ĐẠT]` 26 = 26 · chạy **2481** · skipped 0 · deselected 0 | `3 failed, 661 passed in 179.75s (0:02:59)` | `[ĐẠT]` 3 = 3 · chạy **664** | **`ĐẠT` · exit 0** |

⇒ Cùng lệnh `PYTEST_ADDOPTS=--lf`, bản cũ chạy **26** bài *(0,97 s)* rồi `KẾT: ĐẠT`; bản mới chạy **2.481**. Hai bài chập chờn Q7 *(`test_wo032_man_cua_that.py::test_AC3_…` · `::test_AC7_…`)* ⛔ xuất hiện ở **2/2** lượt.

## 5. Cổng CLAUDE.md ở container *(16/11, sau khi có hai gói)*

`export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1` · chạy bằng `/home/user/FLS-tobe/.venv/bin/python`.

| Lệnh | Exit | Kết quả *(nguyên văn, rút đuôi)* | Đọc |
|---|---|---|---|
| `python tools/kiem_so_song.py` | 1 | `FileNotFoundError: [Errno 2] No such file or directory: '…/agent-a73f7b4b46d6c57c4/.venv/Scripts/lint-imports.exe'` | **⛔ CHƯA ĐO ĐƯỢC** ở container: `tools/kiem_so_song.py:406` gọi cứng đường Windows `GOC/.venv/Scripts/lint-imports.exe`; và nó đọc **kho THẬT** *(số sống của sổ)* — kho ở đây rỗng. Chạy được trên máy owner |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | 0 | `✅ cong tai lieu DAT — va no da do duoc that (168 file, 1810 bang, 719 o ngay, 104 ma QD)` | ĐẠT *(K1–K6)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | 1 | `⇒ 11/16 khop · 5 lech (da do 16/20 phep)` · `B3`/`B4`/`C5`/`C5b` *KHONG DO DUOC* *(sổ rỗng / ⛔ ảnh PM)* · `A1`/`B1`/`C6` *DOI TRANG THAI* | **ĐỎ do kho rỗng**: `A1` đếm `fls_source`, `B1` đếm `fls_pm_line`, `C6` đếm `fls_adjustment`+`fls_journal` — cả ba đọc kho; ⛔ phép nào đọc `.importlinter` hay hai gói mới |
| `python tools/soi_bang_tuyen.py` | 0 | `✅ ban khai KHOP SQL that o ca 40 tuyen` | ĐẠT *(CLAUDE.md ghi "37 tuyến" — máy đo **40** dòng `Tuyen(`, khớp ISP §1)* |
| `python tools/kiem_thuyet_minh.py` | 0 | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` | ĐẠT |
| `.venv/bin/lint-imports` | 0 | `Contracts: 11 kept, 0 broken.` | ĐẠT *(CLAUDE.md ghi "9 hợp đồng tầng" — nay 11)* |
| `python -m fls.db.pg_migrate` | 0 | `khong co gi de ap` · `pg_verify: khop` | ĐẠT *(26/26)* |

## 6. Kho test riêng theo agent chạy SONG SONG *(AC-6)*

```text
$ grep -c 'def test_' tests/db/test_invariants_pg.py
6
$ (PG_DSN_TEST=…/fls_test_a pytest tests/db/test_invariants_pg.py) & (PG_DSN_TEST=…/fls_test_b pytest tests/db/test_invariants_pg.py) & wait
05:25:37.145278233
05:25:37.687040594
lượt A (fls_test_a): exit=0 · 6 passed in 0.31s
lượt B (fls_test_b): exit=0 · 6 passed in 0.29s
$ runuser -u postgres -- psql -h /var/run/postgresql -p 5433 -l   (lọc fls*)
    Name     |  Owner   | Encoding | Locale Provider | Collate |  Ctype  | ICU Locale | ICU Rules |   Access privileges
 fls         | fls      | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           |
 fls_test    | fls      | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           |
 fls_test_a  | fls      | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           |
 fls_test_b  | fls      | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           |
 fls_test_cf | fls      | UTF8     | libc            | C.UTF-8 | C.UTF-8 |            |           |
$ đếm dòng fls_itl của mỗi kho (mỗi lượt chèn dòng của riêng nó)
  fls_test_a: 6 dòng fls_itl · 26 di trú
  fls_test_b: 6 dòng fls_itl · 26 di trú
```

**Đối chứng** *(⛔ phải AC — chứng minh phép đo ⛔ rỗng nghĩa)*: cùng lệnh, hai lượt **chung** một kho `fls_test_chung`:

```text
lượt C1: exit=0 · 6 passed in 0.28s
lượt C2: exit=1 · 3 failed, 3 passed in 0.19s
⛔ khong dung duoc kho TEST: duplicate key value violates unique constraint "pg_database_datname_index"
```

⇒ cách khởi chạy này **thật sự chồng thời gian** *(hai `CREATE DATABASE` va nhau)*, và kho riêng là thứ làm hai lượt ⛔ giẫm nhau. ⚠ Tệp chọn cho AC-6 **⛔ ghim** tên kho; với 19 tệp ở §4.2, kho `fls_test_<làn>` ⛔ đủ — xem BG-066 Q1 *(phép thử phương án "cụm/cổng riêng, giữ tên `fls_test`" đã chạy: hai cụm 5433 + 5434 song song, `tests/repo/test_wo023_f_la_ban_dao_pg.py` `3 passed` ×2; cùng tệp với `fls_test_x` ⇒ `3 errors`; cụm thử đã gỡ)*.

### 6.1 Cụm theo CỔNG — S0-Q1 = A *(vòng sửa sau R1)*

Dựng hai cụm bằng chính script, **song song** *(`--cong 5434` · `FLS_PG_PORT=5435`)*: mỗi lượt `── cụm: chưa có ⇒ initdb /home/user/fls-pg16-<N>` · `CREATE ROLE fls LOGIN CREATEDB` · `CREATE DATABASE fls` · `da ap 26 migration` · **7/7 `[ĐẠT]`** *(K2: `postmaster.pid cổng 5434 · … PG_DSN phục vụ bởi postmaster 6988`; 5435: postmaster `6989`)* · exit 0 cả hai; cuối lượt in `export PG_DSN='postgresql://fls:fls@localhost:5434/fls'` · `export PG_DSN_TEST='postgresql://fls:fls@localhost:5434/fls_test'`.

Phép thử: **một tệp GHIM tên kho** *(`tests/repo/test_wo023_f_la_ban_dao_pg.py:36` `== "fls_test"` — tệp từng `3 errors` với `fls_test_x`)* + `tests/db/test_invariants_pg.py` *(6 bài, ghi `fls_itl`)* — **9** bài; mỗi lượt đặt `PG_DSN` + `PG_DSN_TEST` vào cổng của mình:

```text
lượt cf (5434): bắt đầu 07:15:15.294197063 · 9 passed in 0.43s · exit=0
lượt hc (5435): bắt đầu 07:15:15.294120809 · 9 passed in 0.42s · exit=0
cụm 5434: kho fls fls_test · fls_test: fls_itl = 9 · fls_migration = 26 · current_database = fls_test
cụm 5435: kho fls fls_test · fls_test: fls_itl = 9 · fls_migration = 26 · current_database = fls_test
```

**Đối chứng** *(⛔ phải AC — chứng minh phép đo ⛔ rỗng nghĩa)*: cùng 9 bài, hai lượt **chung cổng 5434**, lặp **3** vòng — **3/3** vòng giẫm nhau:

```text
vòng 1: 2 failed, 6 passed, 1 error in 0.41s (exit 1)  |  9 passed in 0.54s (exit 0)
vòng 2: 9 passed in 0.42s (exit 0)                      |  2 failed, 6 passed, 1 error in 0.33s (exit 1)
vòng 3: 2 failed, 6 passed, 1 error in 0.34s (exit 1)  |  9 passed in 0.43s (exit 0)
E  psycopg.errors.UndefinedTable: relation "fls_run" does not exist        (3 lần)
E  psycopg.errors.UndefinedTable: relation "fls_sua_tay" does not exist    (6 lần)
```

⇒ cụm riêng theo cổng là thứ làm hai lượt ⛔ giẫm nhau, **kể cả với tệp ghim `fls_test`** — điều kho `fls_test_<làn>` ⛔ làm được *(§4.2)*. Cụm **5434** *(BE-CF)* · **5435** *(BE-HC)* **để nguyên, đang chạy**; trên 5433 đã DROP `fls_test_a` · `fls_test_b` · `fls_test_cf` *(+ kho nháp `fls_thu_k7` của vòng sửa)* — còn `fls` · `fls_test`.

## 7. Giới hạn và chuyển orchestrator

- Kho test là cụm cục bộ, ⛔ phải `fls-pg-1` *(O4)*; 26 bài ở §4.1 chỉ đo được trên máy owner.
- `requirements.txt` chỉ ghi cận dưới `>=` ⇒ venv dựng ngày khác có thể lấy bản mới hơn *(16/11: psycopg 3.3.9 · pytest 9.2.0 · import-linter 2.16)*.
- pytest ở container chậm hơn CLAUDE.md ghi *(~4 phút)*: 4–5 phút toàn bộ — phần lớn là bài web chờ hẹn giờ *(mỗi tiến trình `node` của `man_f02.js` ~2 s, CPU ~2%)*.
- Sau khi gộp S0: `lint-imports` **11 kept** ≠ số ghim **9 kept** ở `06_ORCHESTRATOR_DASHBOARD.md:137` và `08_MIGRATION_ROADMAP.md:45` ⇒ `kiem_so_song` *(máy owner)* sẽ ĐỎ hai phép `cong · lint-imports` · `roadmap · lint-imports` cho tới khi `dong_bo_so_song --ghi` soạn lại *(`10` §6 — người chạy là Dev, nhưng hai tệp ấy nay orchestrator ghi)*; `CLAUDE.md` *"9 hợp đồng tầng"* cũng lệch.
- ⭐ *(v0.2 · `S0-R1-07`)* Chỗ **khai** thứ tư — **SPEC** của `fls-ba`: `docs/ITL/02_BA/08_NFR.md:51` `NFR-I16` *"**9** hợp đồng `import-linter`, **0** vi phạm"* ⇒ cũng lệch sau gộp *(nâng → 11 là việc của `fls-ba`, qua orchestrator; Dev ⛔ sửa `02_BA/**`)*. Đo lại 16/11 *(Đ1 · Đ2)*: grep `9 hợp đồng\|9 kept` trong `fls/`+`tools/`+`tests/`+`CLAUDE.md` = **2** dòng — `CLAUDE.md:73` *(khai)* · `tools/dung_moi_truong_isp.sh` *(chú thích "9 hợp đồng cũ + 2 của S0" — biên bản)*; trong `docs/` = **65** tệp, phần lớn biên bản *(sổ `QĐ`, changelog, phiếu)*. ⇒ Bốn chỗ khai: dashboard:137 · `01_Orchestrator/08_MIGRATION_ROADMAP.md:45` · `CLAUDE.md:73` · `02_BA/08_NFR.md:51`.

## Changelog
- **v0.3** *(2026-11-16, `fls-dev` làn BE-CF, vòng sửa sau R2 `KQ-068`)*: câu chốt §1 `:43` khớp mã *(lớp ký tự dùng chung `S0-R2-02` · `--cong ''`/`FLS_PG_PORT` rỗng `S0-R2-01` · pytest bị chặn khi dựng/K2/K7 ĐỎ `S0-R2-04` · cách che mật khẩu)*; §3.4 ĐỎ bản cũ → XANH bản mới cho `S0-R2-01…04`; §4.3 thêm cổng MẪU SỐ *(`S0-R2-03`)* + lượt chính thức sau vòng sửa R2. Phần v0.1/v0.2 giữ nguyên *(biên bản)*.
- **v0.2** *(2026-11-16, `fls-dev` làn BE-CF, vòng sửa sau R1 `KQ-067`)*: đầu trang trỏ tệp máy-đọc; §1 cụm theo CỔNG *(S0-Q1 = A)* + câu chốt viết lại *(câu v0.1 sai với ba dạng DSN của `S0-R1-01`)*; §3.3 ĐỎ bản cũ → XANH bản mới cho `S0-R1-01/03/04/05/06/10`; §4.3 `duong_nen_bai_do.txt` + máy so tập đỏ *(`S0-R1-02`)*; §6.1 hai cụm 5434 · 5435 song song + đối chứng chung cổng; §7 thêm `NFR-I16` *(`S0-R1-07`)*. Bảng §2–§6 của v0.1 giữ nguyên *(biên bản 16/11)*.
- **v0.1** *(2026-11-16, `fls-dev` làn BE-CF, `WO-065`)*: khởi tạo — lệnh dựng, pha đỏ/xanh, phá thử hai hợp đồng, pytest hai lượt + lượt đối chứng `39524c5`, cổng CLAUDE.md, AC-6.
