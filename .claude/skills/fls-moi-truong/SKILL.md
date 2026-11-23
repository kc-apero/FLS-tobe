---
name: fls-moi-truong
description: Dựng hoặc bật lại môi trường chạy FLS trong container cloud — cụm PostgreSQL 16 theo cổng, venv, biến PG_DSN, khoá SA Google chỉ-đọc, cổng hồi quy `--duong-nen`. Dùng khi chủ hoặc phiên nói "dựng môi trường", "bật lại PG", "container khởi động lại", "Connection refused", "chạy đường nền", "duong-nen", "cổng hồi quy", "kiểm khoá SA", "đọc sheet bằng SA", hoặc TRƯỚC mọi pytest ở một container mới.
---

# fls-moi-truong — môi trường FLS trên container cloud

Nguồn: `docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-19.md` §4 · `CLAUDE.md` (Đ1–Đ5 · Bẫy · Riêng tư).
Mọi câu báo kết quả mang **con số đo được** và **nhãn nó đếm gì** (Đ4).

## 1. Dựng mới một cụm (chạy lại được, ⛔ phá gì đã có)

```bash
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
bash tools/dung_moi_truong_isp.sh --cong <N>
```
- `<N>`: **5433** = cụm orchestrator · **5434–5437, 5444–5447** = mỗi phiên con song song một cổng khác.
- Script tự: tạo `.venv` + `pip install -r requirements.txt` · `initdb /home/user/fls-pg16[-<N>]` · role `fls` · kho `fls` RỖNG · di trú + `pg_verify`. Mong: `KẾT: ĐẠT` (7 phép kiểm, kể cả `lint-imports` **11 kept**).
- Từ worktree: `env -C <worktree> bash <worktree>/tools/dung_moi_truong_isp.sh --cong <N>` (⛔ `cd`).

## 2. Container khởi động lại ⇒ cụm TẮT ⇒ bật lại TRƯỚC mọi pytest

Bài pg đỏ "Connection refused" là **môi trường**, ⛔ lỗi mã. Dán nguyên:
```bash
mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql
for d in /home/user/fls-pg16 /home/user/fls-pg16-*; do p=$(basename $d | sed 's/fls-pg16-\?//'); p=${p:-5433}
  if [ -f $d/postmaster.pid ]; then pid=$(head -1 $d/postmaster.pid); ps -o args= -p $pid 2>/dev/null | grep -q "$d" || rm -f $d/postmaster.pid; fi
  l=/var/run/postgresql/.s.PGSQL.$p.lock; if [ -f $l ]; then pid=$(head -1 $l); ps -o args= -p $pid 2>/dev/null | grep -q "$d" || rm -f $l /var/run/postgresql/.s.PGSQL.$p; fi
  runuser -u postgres -- /usr/lib/postgresql/16/bin/pg_ctl -D $d -l $d/pg_ctl.log -w -t 60 start >/dev/null 2>&1; echo -n "$p:$? "; done; echo
```
Mỗi cổng in `:0` là bật được. ⛔ `docker compose down` (máy Windows của chủ — kho trên volume vô danh).

## 3. Biến luôn export
```bash
export PYTHONUTF8=1
export PG_DSN='postgresql://fls:fls@localhost:<N>/fls'
export PG_DSN_TEST='postgresql://fls:fls@localhost:<N>/fls_test'
```
`pytest` ⛔ thêm `-q` (pyproject đã có — thêm nữa mất dòng tổng kết).

## 4. Cổng hồi quy `--duong-nen` (luật C: MỘT lần cuối phiên, chạy MỘT mình)
```bash
bash tools/dung_moi_truong_isp.sh --duong-nen --cong <N>      # ~15–25 phút ⇒ chạy nền
```
- Mong: `KẾT: ĐẠT` — tập đỏ + XFAIL **=** `duong_nen_bai_do.txt` theo node id (hiện **28** toàn bộ · **3** web; thêm 0 · bớt 0) và số bài chạy ≥ sàn `MONG_PYTEST_TOAN_BO` / `MONG_PYTEST_WEB` (dòng 420–421 script, ghim ở `tests/test_dung_moi_truong_isp.py`).
- Bài mới ⇒ nâng sàn = **số thu thập thật** + bài ghim **cùng commit** (Q8).

## 5. Khoá SA Google (đọc Sheets/Drive — CHỈ-ĐỌC)
- Biến: **`FLS_GSHEETS_SA_JSON_B64`** (base64 của JSON) hoặc `FLS_GSHEETS_SA_JSON` ở *environment secrets*.
- Kiểm có mặt: `test -n "$FLS_GSHEETS_SA_JSON_B64" && echo co` — ⛔ `echo` giá trị, ⛔ in log, ⛔ ghi tệp repo, ⛔ dán chat.
- Thiếu ⇒ báo chủ đặt secret + mở mạng `sheets.googleapis.com` · `oauth2.googleapis.com` · `www.googleapis.com`. Bước DATA cần sheet ⇒ chờ.
- `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`. Công cụ: `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_*.py` (chạy `.venv/bin/python -I`). Tên tab có `/` `|` `[` ⇒ `urllib.parse.quote` cả vùng.
- Dữ liệu thô chỉ ở scratchpad/`/tmp` (chmod 600), xoá sau dùng. Dò tiêu đề: chỉ in **tên cột**; dữ liệu chỉ **ĐẾM** — ⛔ in giá trị, ⛔ in số TK dù vài chữ số.

## 6. Cổng khác (CLAUDE.md)
`python docs/ITL/_tools/kiem_tai_lieu.py` · `.venv/bin/lint-imports` (11 kept) · `python tools/soi_bang_tuyen.py` · `python tools/kiem_thuyet_minh.py` · `python tools/quet_pii_repo.py` (0 ⇒ ĐẠT) · `python -m fls.db.pg_migrate` (tự `pg_verify`).
