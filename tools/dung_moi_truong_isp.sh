#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# DỰNG môi trường test của ISP 3.1 ở container cloud — rồi IN ĐƯỜNG NỀN đo thật.
#
#   bash tools/dung_moi_truong_isp.sh              # dựng (chạy lại được) + kiểm nhanh có `mong`
#   bash tools/dung_moi_truong_isp.sh --duong-nen  # như trên + pytest TOÀN BỘ + riêng tests/web
#   bash tools/dung_moi_truong_isp.sh --chi-kiem   # ⛔ dựng gì — chỉ kiểm (đỏ nếu môi trường thiếu)
#
# ⭐ Vì sao có tệp này (ISP 3.1.2 Step 0 · `WO-065`). Đo 16/11: container cloud ⛔ có Docker,
#    ⛔ có pytest ở python hệ thống, ⛔ có `.venv` — nên MỌI bước sau của ISP ⛔ chạy được một
#    bài PG nào. Kho thật `fls-pg-1` nằm trên máy Windows của owner (O4 = A: test ở container,
#    bước tích hợp cuối chạy lại trên máy owner trước merge).
#
# ⛔⛔ Năm luật của tệp này — mỗi luật một cái bẫy đã biết:
#
#  ① CHẠY LẠI ĐƯỢC, ⛔ PHÁ GÌ ĐÃ CÓ. venv có rồi ⇒ chỉ cài phần THIẾU; cụm có rồi ⇒ chỉ khởi động;
#    role/kho có rồi ⇒ bỏ qua. Thư mục dữ liệu tồn tại mà ⛔ phải cụm PG ⇒ TỪ CHỐI, ⛔ xoá.
#    Cổng 5433 đã có người nghe mà ⛔ phải cụm của tệp này ⇒ TỪ CHỐI (trên máy owner đó là
#    `fls-pg-1` — kho THẬT). ⛔ Tệp này ⛔ bao giờ gọi `docker` (⛔ `docker compose down`:
#    `docker-compose.yml` ⛔ khai `volumes:` ⇒ một lệnh `down` là kho rỗng).
#
#  ② ⛔ GHI KHO THẬT. `FLS_CHO_GHI_THAT` đặt ⇒ TỪ CHỐI. `PG_DSN` phải trỏ `localhost`/`127.0.0.1`
#    cổng 5433 — kho `fls` ở đây là kho RỖNG cục bộ chỉ mang di trú; container ⛔ có sổ thật.
#    Kho đích có dòng `fls_itl` ⇒ ⛔ phải kho của tệp này ⇒ TỪ CHỐI di trú. Cụm bị từ chối ⇒ DỪNG
#    chuỗi (⛔ tạo role/kho, ⛔ di trú lên một kho mà tệp này ⛔ dựng).
#
#  ③ venv DÙNG CHUNG ở CHECKOUT CHÍNH, ⛔ ở worktree. Mỗi agent chạy trong một git worktree riêng
#    (`.claude/worktrees/agent-*`), và worktree bị dọn khi bước xong — venv đặt trong đó sẽ mất.
#    ⇒ Tìm gốc checkout chính bằng `git rev-parse --git-common-dir` rồi lấy thư mục cha. Gói `fls`
#    ⛔ cài vào venv: nó luôn lấy từ thư mục làm việc của worktree đang chạy (`cd "$GOC"`).
#
#  ④ `PYTHONUTF8=1` đặt TẠI ĐÂY, ⛔ trông vào shell người gọi. Thiếu nó `lint-imports` giải mã
#    nguồn tiếng Việt bằng trang mã hệ thống và IM LẶNG in 0 byte (CLAUDE.md · Bẫy).
#
#  ⑤ ĐỎ khi ⛔ ĐO ĐƯỢC (Đ5). Mỗi phép kiểm khai `mong` trước; khác ⇒ `[ĐỎ]`; ⛔ chạy được ⇒ `[ĐỎ]`
#    (⛔ phải "không thấy lệch"). Một phép kiểm đỏ ⇒ exit 1. pytest là ĐO ĐƯỜNG NỀN, ⛔ phán:
#    bài đỏ CÓ SẴN ≠ lỗi môi trường — tên từng bài ghi ở `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md`;
#    nhưng pytest ⛔ chạy nổi (mã thoát ∉ {0, 1}) thì vẫn là `[ĐỎ]`.
#
# Biến đổi được (mặc định là sự thật đã đo ở container 16/11):
#   FLS_VENV    venv dùng chung        (mặc định <checkout chính>/.venv)
#   FLS_PGDATA  thư mục dữ liệu cụm    (mặc định /home/user/fls-pg16 — NGOÀI repo)
#   FLS_PGBIN   binary PostgreSQL 16   (mặc định /usr/lib/postgresql/16/bin)
#   PG_DSN      kho `fls` cục bộ       (mặc định postgresql://fls:fls@localhost:5433/fls — trùng fls/db/kho.py)
#   PG_DSN_TEST kho test của MỖI agent (quy ước TIEN_DO.md: …/fls_test_<làn>; bỏ trống ⇒ `fls_test` của kho.py)
set -uo pipefail

CHE_DO="dung"
case "${1:-}" in
  "")            CHE_DO="dung" ;;
  --duong-nen)   CHE_DO="duong_nen" ;;
  --chi-kiem)    CHE_DO="chi_kiem" ;;
  -h|--help)     sed -n '2,8p' "$0"; exit 0 ;;
  *)             echo "⛔ đối số lạ: $1 (xem --help)" >&2; exit 2 ;;
esac

GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# ③ — gốc checkout CHÍNH (nơi đặt venv dùng chung). Ngoài git ⇒ dùng chính GOC.
if CHUNG="$(git -C "$GOC" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; then
  GOC_CHUNG="$(dirname "$CHUNG")"
else
  GOC_CHUNG="$GOC"
fi
VENV="${FLS_VENV:-$GOC_CHUNG/.venv}"
PY="$VENV/bin/python"
PGBIN="${FLS_PGBIN:-/usr/lib/postgresql/16/bin}"
PGDATA_ISP="${FLS_PGDATA:-/home/user/fls-pg16}"
CONG=5433
SOCK=/var/run/postgresql
export PG_DSN="${PG_DSN:-postgresql://fls:fls@localhost:5433/fls}"
# tên kho lấy từ chính PG_DSN (thường là `fls`) — tạo đúng kho mà di trú và các phép kiểm sẽ nối
TEN_KHO="${PG_DSN##*/}"; TEN_KHO="${TEN_KHO%%\?*}"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
cd "$GOC" || exit 2

# Đ5 — bộ đếm ĐỎ dùng chung cho cả DỰNG lẫn KIỂM. ⭐ Bước dựng hỏng cũng là ĐỎ: ⛔ để một phép
# kiểm xanh "nhờ" một cụm/kho KHÁC che đi việc cụm của tệp này ⛔ dựng được (đo 16/11 khi soát lại
# bản đầu: bước cụm bị từ chối mà 6 phép kiểm vẫn ĐẠT vì cụm cũ còn chạy ⇒ exit 0 sai).
DO=0
dat() { printf '  [ĐẠT] %-26s %s\n' "$1" "$2"; }
do_() { printf '  [ĐỎ]  %-26s %s\n' "$1" "$2"; DO=$((DO + 1)); }

# ── ② chốt an toàn — chạy TRƯỚC mọi thứ, kể cả ở chế độ chỉ kiểm.
if [ -n "${FLS_CHO_GHI_THAT:-}" ]; then
  echo "⛔ FLS_CHO_GHI_THAT đang đặt — tệp này ⛔ được chạy cạnh quyền ghi sổ thật. Gỡ biến rồi chạy lại." >&2
  exit 2
fi
case "$PG_DSN" in
  postgresql://*@localhost:5433/*|postgresql://*@127.0.0.1:5433/*) ;;
  *) echo "⛔ PG_DSN=$PG_DSN ⛔ trỏ cụm cục bộ localhost:5433 — từ chối (kho ở đây phải là kho RỖNG cục bộ)." >&2
     exit 2 ;;
esac

# Lệnh của user `postgres`: initdb TỪ CHỐI chạy bằng root (đo 16/11) ⇒ `runuser`.
chay_pg() {
  if [ "$(id -u)" = 0 ]; then runuser -u postgres -- "$@"; else "$@"; fi
}
# psql quản trị qua socket (xác thực `peer` của user postgres) — ⛔ cần mật khẩu.
psql_qt() {
  chay_pg "$PGBIN/psql" -X -v ON_ERROR_STOP=1 -h "$SOCK" -p "$CONG" -d postgres -tA "$@"
}

echo "══ dung_moi_truong_isp · chế độ $CHE_DO · $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "   GOC (mã fls)   = $GOC"
echo "   venv dùng chung = $VENV"
echo "   cụm PG16       = $PGDATA_ISP (cổng $CONG)"
echo "   PG_DSN         = $PG_DSN"
echo "   PG_DSN_TEST    = ${PG_DSN_TEST:-<trống ⇒ fls_test của fls/db/kho.py>}"

# ═════════════════════════════════════════════════════════════════ DỰNG
dung_venv() {
  if [ ! -x "$PY" ]; then
    echo "── venv: chưa có ⇒ tạo $VENV"
    python3 -m venv "$VENV" || { echo "⛔ tạo venv hỏng"; return 1; }
  else
    echo "── venv: đã có ($($PY --version 2>&1)) ⇒ giữ"
  fi
  # ① chỉ cài khi THIẾU — `pip install` ⛔ chạy mỗi lần (đi mạng, chậm, có thể nâng bản ngầm).
  if "$PY" -c "import psycopg, pytest, importlinter" 2>/dev/null; then
    echo "── gói: psycopg · pytest · import-linter đã đủ ⇒ bỏ qua pip"
  else
    echo "── gói: thiếu ⇒ pip install -r requirements.txt"
    "$PY" -m pip install --disable-pip-version-check -q -r "$GOC/requirements.txt" \
      || { echo "⛔ pip install hỏng"; return 1; }
  fi
}

dung_cum() {
  [ -x "$PGBIN/initdb" ] || { echo "⛔ ⛔ thấy $PGBIN/initdb"; return 1; }
  install -d -m 2775 -o postgres -g postgres "$SOCK"
  if [ -s "$PGDATA_ISP/PG_VERSION" ]; then
    echo "── cụm: đã có (PG $(cat "$PGDATA_ISP/PG_VERSION")) ⇒ giữ"
  else
    if [ -e "$PGDATA_ISP" ] && [ -n "$(ls -A "$PGDATA_ISP" 2>/dev/null)" ]; then
      echo "⛔ $PGDATA_ISP có dữ liệu mà ⛔ phải cụm PG — TỪ CHỐI (⛔ xoá hộ ai)."
      return 1
    fi
    echo "── cụm: chưa có ⇒ initdb $PGDATA_ISP"
    install -d -m 700 -o postgres -g postgres "$PGDATA_ISP"
    chay_pg "$PGBIN/initdb" -D "$PGDATA_ISP" -U postgres -E UTF8 --locale=C.UTF-8 \
      --auth-local=peer --auth-host=scram-sha-256 >/dev/null || { echo "⛔ initdb hỏng"; return 1; }
    # cổng 5433 = mặc định của fls/db/kho.py · chỉ nghe localhost · socket ở thư mục chuẩn Debian
    chay_pg sh -c "printf '%s\n' \"# dung_moi_truong_isp.sh\" \"port = $CONG\" \"listen_addresses = 'localhost'\" \"unix_socket_directories = '$SOCK'\" >> '$PGDATA_ISP/postgresql.conf'"
  fi
  if chay_pg "$PGBIN/pg_ctl" -D "$PGDATA_ISP" status >/dev/null 2>&1; then
    echo "── cụm: đang chạy ⇒ giữ"
  else
    # ① cổng đã có người nghe mà ⛔ phải cụm này ⇒ ⛔ chen (trên máy owner đó là kho THẬT).
    if "$PGBIN/pg_isready" -q -h localhost -p "$CONG"; then
      echo "⛔ cổng $CONG đã có một PostgreSQL KHÁC đang nghe — TỪ CHỐI khởi động cụm thứ hai."
      return 1
    fi
    echo "── cụm: đang tắt ⇒ pg_ctl start"
    chay_pg "$PGBIN/pg_ctl" -D "$PGDATA_ISP" -l "$PGDATA_ISP/pg_ctl.log" -w -t 60 start >/dev/null \
      || { echo "⛔ pg_ctl start hỏng — xem $PGDATA_ISP/pg_ctl.log"; return 1; }
  fi
}

dung_role_kho() {
  local co
  co="$(psql_qt -c "select rolcanlogin::int::text || rolcreatedb::int::text from pg_roles where rolname = 'fls'")" \
    || { echo "⛔ ⛔ hỏi được pg_roles"; return 1; }
  case "$co" in
    "")  echo "── role fls: chưa có ⇒ CREATE ROLE fls LOGIN CREATEDB"
         psql_qt -c "CREATE ROLE fls LOGIN CREATEDB PASSWORD 'fls'" >/dev/null || return 1 ;;
    11)  echo "── role fls: đã có LOGIN + CREATEDB ⇒ bỏ qua" ;;
    *)   # ⛔ đổi mật khẩu của một role đã có — chỉ THÊM đúng hai quyền mà tests/conftest.py cần.
         echo "── role fls: có nhưng thiếu quyền (login·createdb = $co) ⇒ ALTER ROLE fls LOGIN CREATEDB"
         psql_qt -c "ALTER ROLE fls LOGIN CREATEDB" >/dev/null || return 1 ;;
  esac
  case "$TEN_KHO" in
    ""|*[!a-z0-9_]*) echo "⛔ tên kho '$TEN_KHO' (từ PG_DSN) ⛔ hợp lệ — chỉ nhận [a-z0-9_]"; return 1 ;;
  esac
  co="$(psql_qt -c "select 1 from pg_database where datname = '$TEN_KHO'")" || return 1
  if [ "$co" = 1 ]; then
    echo "── kho $TEN_KHO: đã có ⇒ bỏ qua"
  else
    echo "── kho $TEN_KHO: chưa có ⇒ CREATE DATABASE $TEN_KHO OWNER fls (RỖNG — chỉ mang di trú)"
    psql_qt -c "CREATE DATABASE \"$TEN_KHO\" OWNER fls" >/dev/null || return 1
  fi
}

dung_di_tru() {
  # ② kho ở đây phải là kho RỖNG cục bộ. Đếm `fls_itl` qua kết nối CHỈ ĐỌC; > 0 dòng ⇒ đây ⛔ phải
  #   kho của tệp này (có thể là một bản chụp sổ thật ai đó nạp vào) ⇒ ⛔ chạm DDL, TỪ CHỐI.
  local n
  n="$("$PY" - <<'PY' 2>&1
import os
from fls.db.kho import noi_chi_doc
c = noi_chi_doc(os.environ["PG_DSN"])
try:
    co = c.execute("select to_regclass('public.fls_itl') is not null").fetchone()[0]
    print(c.execute("select count(*) from fls_itl").fetchone()[0] if co else 0)
finally:
    c.close()
PY
)" || { echo "⛔ ⛔ đếm được fls_itl trước di trú: $(echo "$n" | tail -1)"; return 1; }
  if [ "$n" != 0 ]; then
    echo "⛔ kho $TEN_KHO có $n dòng fls_itl ⇒ ⛔ phải kho RỖNG cục bộ — TỪ CHỐI di trú"
    return 1
  fi
  echo "── di trú: $PY -m fls.db.pg_migrate   (kho $TEN_KHO: 0 dòng fls_itl)"
  "$PY" -m fls.db.pg_migrate 2>&1 | sed 's/^/   │ /'
  local ma="${PIPESTATUS[0]}"
  echo "   └ exit=$ma"
  [ "$ma" = 0 ]
}

if [ "$CHE_DO" != "chi_kiem" ]; then
  echo
  echo "══ DỰNG"
  dung_venv || do_ "dựng · venv" "bước dựng hỏng (xem dòng ⛔ trên)"
  # ⛔ Cụm bị từ chối/hỏng ⇒ DỪNG chuỗi: ⛔ tạo role/kho, ⛔ chạy di trú lên một PG_DSN mà tệp này
  #   ⛔ dựng (bản đầu chạy tiếp cả ba bước — trên máy có `fls-pg-1` ở 5433 thì di trú sẽ đi vào kho THẬT).
  if dung_cum; then
    if dung_role_kho; then
      dung_di_tru || do_ "dựng · di trú" "bước dựng hỏng hoặc bị từ chối (xem dòng ⛔ trên)"
    else
      do_ "dựng · role/kho" "bước dựng hỏng — ⛔ chạy di trú"
    fi
  else
    do_ "dựng · cụm" "bước dựng hỏng hoặc bị từ chối — ⛔ tạo role/kho, ⛔ chạy di trú"
  fi
fi

# ═════════════════════════════════════════════════════════════════ KIỂM (Đ5: `mong` khai trước)
# ⭐ `mong` của lint-imports: 9 hợp đồng cũ + 2 của S0 (`fls.cau_hinh` · `fls.bao_cao`). Bước nào
#    thêm/bớt một hợp đồng tầng thì phải SỬA SỐ NÀY — đó chính là điều Đ5 muốn: đổi một chỗ là ĐỎ.
MONG_LINT_KEPT=11
MONG_LINT_BROKEN=0
# ⭐ `mong` của HD1 (tools/do_voi_so_luong.py · MONG so_dong_so / so_dong_ghep_canon — ghim 16/11).
MONG_HD1_CO=9967
MONG_HD1_CHAY=9845

echo
echo "══ KIỂM"
# K1 · venv có đủ ba gói của requirements.txt
if [ -x "$PY" ] && "$PY" -c "import psycopg, pytest, importlinter" 2>/dev/null; then
  dat "venv + 3 gói" "$("$PY" -c 'import psycopg, pytest, importlib.metadata as m; print("psycopg", psycopg.__version__, "· pytest", pytest.__version__, "· import-linter", m.version("import-linter"))')"
else
  do_ "venv + 3 gói" "mong: $PY import được psycopg · pytest · importlinter — đo: ⛔"
fi

# K2 · cụm nghe ở localhost:5433
if "$PGBIN/pg_isready" -q -h localhost -p "$CONG" 2>/dev/null; then
  dat "cụm PG localhost:$CONG" "pg_isready exit 0"
else
  do_ "cụm PG localhost:$CONG" "mong: pg_isready exit 0 — đo: ⛔ trả lời"
fi

# K3 · role fls đăng nhập được bằng chính PG_DSN và có CREATEDB (conftest DROP + CREATE kho test)
QUYEN="$( [ -x "$PY" ] && "$PY" - <<'PY' 2>/dev/null
import os, psycopg
with psycopg.connect(os.environ["PG_DSN"], connect_timeout=5) as c:
    print(c.execute("select rolcreatedb from pg_roles where rolname = current_user").fetchone()[0])
PY
)"
if [ "$QUYEN" = "True" ]; then
  dat "role fls LOGIN + CREATEDB" "đăng nhập bằng PG_DSN được · rolcreatedb = t"
else
  do_ "role fls LOGIN + CREATEDB" "mong: đăng nhập được + rolcreatedb = t — đo: '${QUYEN:-⛔ nối được}'"
fi

# K4 · di trú áp ĐỦ (số dòng fls_migration = số tệp NNNN_*.sql) + pg_verify khớp — qua kết nối CHỈ ĐỌC
N_TEP=$(ls "$GOC"/fls/db/migrations/[0-9][0-9][0-9][0-9]_*.sql 2>/dev/null | wc -l)
DT="$( [ -x "$PY" ] && "$PY" - <<'PY' 2>&1
import os
from fls.db.kho import noi_chi_doc
from fls.db.pg_verify import so_sanh_voi_db
c = noi_chi_doc(os.environ["PG_DSN"])
try:
    n = c.execute("select count(*) from fls_migration").fetchone()[0]
    lech = so_sanh_voi_db(c)
finally:
    c.close()
print(f"{n} {len(lech)}")
PY
)"
N_AP="$(echo "$DT" | tail -1 | awk '{print $1}')"
N_LECH="$(echo "$DT" | tail -1 | awk '{print $2}')"
if [ "$N_TEP" -gt 0 ] && [ "$N_AP" = "$N_TEP" ] && [ "$N_LECH" = 0 ]; then
  dat "di trú + pg_verify" "$N_AP/$N_TEP di trú áp · pg_verify khớp (0 chỗ lệch)"
else
  do_ "di trú + pg_verify" "mong: áp = tệp > 0 và 0 lệch — đo: áp '${N_AP:-?}' / tệp $N_TEP · lệch '${N_LECH:-?}' · $(echo "$DT" | tail -1 | cut -c1-120)"
fi

# K5 · lint-imports: 11 hợp đồng giữ, 0 vỡ
if [ -x "$VENV/bin/lint-imports" ]; then
  LINT="$("$VENV/bin/lint-imports" 2>&1)"; MA_LINT=$?
  DONG_LINT="$(echo "$LINT" | grep -E 'Contracts: [0-9]+ kept, [0-9]+ broken' | tail -1)"
  if [ "$DONG_LINT" = "Contracts: $MONG_LINT_KEPT kept, $MONG_LINT_BROKEN broken." ] && [ "$MA_LINT" = 0 ]; then
    dat "lint-imports" "$DONG_LINT (exit 0)"
  else
    do_ "lint-imports" "mong: Contracts: $MONG_LINT_KEPT kept, $MONG_LINT_BROKEN broken. — đo: '${DONG_LINT:-⛔ có dòng tổng kết}' (exit $MA_LINT)"
  fi
else
  do_ "lint-imports" "mong: Contracts: $MONG_LINT_KEPT kept, $MONG_LINT_BROKEN broken. — đo: ⛔ có $VENV/bin/lint-imports"
fi

# K6 · HD1 — hàng Σ của tools/do_voi_so_luong.py: cột `có` (dòng sổ) và `chạy` (dòng ghép 1-1)
if [ -x "$PY" ]; then
  HD1="$("$PY" tools/do_voi_so_luong.py 2>&1)"; MA_HD1=$?
  read -r _ HD1_CO HD1_CHAY _ <<<"$(echo "$HD1" | grep -E '^Σ ' | tail -1)"
  if [ "$MA_HD1" = 0 ] && [ "${HD1_CO:-}" = "$MONG_HD1_CO" ] && [ "${HD1_CHAY:-}" = "$MONG_HD1_CHAY" ]; then
    dat "HD1 do_voi_so_luong" "chay $HD1_CHAY / co $HD1_CO (exit 0)"
  else
    do_ "HD1 do_voi_so_luong" "mong: exit 0 · chay $MONG_HD1_CHAY / co $MONG_HD1_CO — đo: exit $MA_HD1 · chay '${HD1_CHAY:-?}' / co '${HD1_CO:-?}'"
  fi
else
  do_ "HD1 do_voi_so_luong" "mong: exit 0 · chay $MONG_HD1_CHAY / co $MONG_HD1_CO — đo: ⛔ có venv"
fi

# ═════════════════════════════════════════════════════════════════ ĐƯỜNG NỀN pytest (đo, ⛔ phán)
chay_pytest() {   # $1 = nhãn · còn lại = đối số pytest
  local nhan="$1"; shift
  local log; log="$(mktemp "${TMPDIR:-/tmp}/fls_isp_pytest.XXXXXX")"
  # ⛔ thêm `-q`: pyproject.toml đã có `-q`, thêm nữa là `-qq` và MẤT dòng tổng kết.
  "$PY" -m pytest -rfE "$@" >"$log" 2>&1
  local ma=$?
  local tong; tong="$(grep -E '^(=+ )?[0-9]+ (passed|failed|error|skipped|deselected|xfailed|xpassed)|^=+ .*(passed|failed|error).* =+$|no tests ran' "$log" | tail -1)"
  echo "  ── pytest $nhan · exit $ma · log $log"
  echo "     $tong"
  grep -E '^(FAILED|ERROR) ' "$log" | sed 's/^/     /'
  case "$ma" in
    0|1) ;;                                      # đo được (1 = có bài đỏ — đường nền, ⛔ lỗi môi trường)
    *)   do_ "pytest $nhan" "mong: chạy nổi (exit 0 hoặc 1) — đo: exit $ma" ;;
  esac
}

if [ "$CHE_DO" = "duong_nen" ]; then
  echo
  echo "══ ĐƯỜNG NỀN pytest (bài đỏ CÓ SẴN ≠ lỗi môi trường — ghi tên ở DUONG_NEN.md, ⛔ sửa)"
  if [ -x "$PY" ]; then
    chay_pytest "toàn bộ"
    chay_pytest "tests/web" tests/web
  else
    do_ "pytest" "mong: có venv — đo: ⛔"
  fi
fi

echo
if [ "$DO" = 0 ]; then
  echo "══ KẾT: ĐẠT — mọi phép kiểm khớp mong"
  exit 0
fi
echo "══ KẾT: ĐỎ — $DO phép kiểm khác mong hoặc ⛔ đo được"
exit 1
