#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# DỰNG môi trường test của ISP 3.1 ở container cloud — rồi IN ĐƯỜNG NỀN đo thật.
#
#   bash tools/dung_moi_truong_isp.sh [--cong N]              # dựng (chạy lại được) + kiểm nhanh có `mong`
#   bash tools/dung_moi_truong_isp.sh [--cong N] --duong-nen  # như trên + pytest TOÀN BỘ + tests/web, SO tập đỏ với đường nền
#   bash tools/dung_moi_truong_isp.sh [--cong N] --chi-kiem   # ⛔ dựng gì — chỉ kiểm (đỏ nếu môi trường thiếu)
#   N ∈ 5433…5437 · 5444…5447 — mỗi agent MỘT cụm theo cổng (TIEN_DO.md); ⛔ --cong ⇒ FLS_PG_PORT ⇒ 5433
#
# ⭐ Vì sao có tệp này (ISP 3.1.2 Step 0 · `WO-065`). Đo 16/11: container cloud ⛔ có Docker,
#    ⛔ có pytest ở python hệ thống, ⛔ có `.venv` — nên MỌI bước sau của ISP ⛔ chạy được một
#    bài PG nào. Kho thật `fls-pg-1` nằm trên máy Windows của owner (O4 = A: test ở container,
#    bước tích hợp cuối chạy lại trên máy owner trước merge).
#
# ⭐ Vì sao MỘT CỤM MỖI CỔNG (S0-Q1 = A, orchestrator chốt 16/11 sau R1). Quy ước đầu là "mỗi
#    agent một KHO `fls_test_<làn>` trên một cụm" — nhưng 24 dòng ở 19 tệp bài ghim `== "fls_test"`
#    (5 tệp trong `tests/nghiem_thu/`) ⇒ lượt toàn bộ đỏ GIẢ thêm 131 bài (DUONG_NEN.md §4.2). Giữ
#    tên kho `fls`/`fls_test`, tách bằng CỔNG: 5433 = cụm gốc của S0 · 5434 BE-CF · 5435 BE-HC ·
#    5436 FE · 5437 DATA · 5444…5447 reviewer theo làn. Thư mục dữ liệu: /home/user/fls-pg16 cho
#    5433 (giữ nguyên cụm đã dựng ở S0), /home/user/fls-pg16-<N> cho cổng khác.
#
# ⛔⛔ Năm luật của tệp này — mỗi luật một cái bẫy đã biết:
#
#  ① CHẠY LẠI ĐƯỢC, ⛔ PHÁ GÌ ĐÃ CÓ. venv có rồi ⇒ chỉ cài phần THIẾU; cụm có rồi ⇒ chỉ khởi động;
#    role/kho có rồi ⇒ bỏ qua. Thư mục dữ liệu tồn tại mà ⛔ phải cụm PG ⇒ TỪ CHỐI, ⛔ xoá.
#    Cổng của lượt đã có người nghe mà ⛔ phải cụm của tệp này ⇒ TỪ CHỐI (trên máy owner 5433 là
#    `fls-pg-1` — kho THẬT). Cụm có sẵn mà khai cổng KHÁC cổng của lượt ⇒ TỪ CHỐI. ⛔ Tệp này ⛔
#    bao giờ gọi `docker` (⛔ `docker compose down`: `docker-compose.yml` ⛔ khai `volumes:` ⇒ một
#    lệnh `down` là kho rỗng).
#
#  ② ⛔ GHI KHO THẬT. `FLS_CHO_GHI_THAT` đặt ⇒ TỪ CHỐI. `PG_DSN` (và `PG_DSN_TEST` nếu đặt) phải
#    khớp NGUYÊN CHUỖI `postgresql://<user>:<pass>@(localhost|127.0.0.1):<cổng của lượt>/<[a-z0-9_]+>`
#    — ⛔ query string, ⛔ host khác, `<user>`/`<pass>` ⛔ chứa `@ / ? #` hay khoảng trắng (MỘT lớp
#    ký tự `LOP_USER`/`LOP_MK` dùng chung với hàm che — S0-R2-02); và ⛔ biến `PGHOST`/`PGHOSTADDR`/`PGPORT`/`PGSERVICE`/
#    `PGSERVICEFILE` nào được đặt. ⛔⛔ Bản đầu so bằng glob `case` (`postgresql://*@localhost:5433/*`)
#    và R1 (`KQ-067` · `S0-R1-01`) đo được BA đường "trông cục bộ mà nối đi chỗ khác":
#      ⓐ `…@localhost:5433/fls?port=5999`              — libpq gộp query string ⇒ nối 127.0.0.1:5999
#      ⓑ `postgresql://x@10.0.0.9:5432/y@localhost:5433/fls` — `*` nuốt cả `/` ⇒ khớp glob,
#                                                         libpq nối 10.0.0.9:5432
#      ⓒ `PGHOSTADDR=10.255.255.1`                      — libpq gộp biến PG* ⇒ nối nơi khác
#    Ở chế độ dựng, chuỗi sẽ chạy `pg_migrate` (DDL) lên đích ấy. ⇒ So ĐÍCH NỐI như libpq hiểu:
#    khuôn nguyên chuỗi chặn mọi chỗ libpq lấy thêm tham số (query · userinfo lạ), từ chối biến
#    PG* chặn chỗ còn lại. Kho đích có dòng `fls_itl` ⇒ ⛔ phải kho của tệp này ⇒ TỪ CHỐI di trú.
#    Cụm bị từ chối ⇒ DỪNG chuỗi (⛔ tạo role/kho, ⛔ di trú lên một kho mà tệp này ⛔ dựng).
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
#    (⛔ phải "không thấy lệch"). Một phép kiểm đỏ ⇒ exit 1. Phép nào ra `0 lệch` phải in MẪU SỐ
#    cạnh nó và đỏ khi mẫu số = 0 (Đ3). pytest: bài đỏ CÓ SẴN ≠ lỗi môi trường, nhưng tập đỏ
#    phải BẰNG tập đã ghi ở `docs/ITL/03_Dev/isp-3.1/duong_nen_bai_do.txt` (node id) — THÊM hay
#    BỚT một bài đều `[ĐỎ]` (S0-R1-02: bản đầu chỉ đỏ khi pytest ⛔ chạy nổi, nên một bài đỏ MỚI
#    vẫn `KẾT: ĐẠT`). pytest ⛔ chạy nổi (mã thoát ∉ {0, 1}) hay ⛔ có dòng tổng kết ⇒ `[ĐỎ]`.
#    ⭐ MẪU SỐ cũng có `mong` (S0-R2-03): `skipped = 0` · `deselected = 0` · số bài CHẠY ≥
#    `MONG_PYTEST_TOAN_BO` / `MONG_PYTEST_WEB`, và pytest chạy với `PYTEST_ADDOPTS` bị GỠ — tập
#    đỏ bằng nhau trên một bộ bài teo (`--lf`: 26/2.460) là xanh giả. ⭐ Phép kiểm định danh đã
#    ĐỎ thì ⛔ bước GHI nào sau nó (S0-R2-04): dựng / K2 / K7 ĐỎ ⇒ ⛔ chạy pytest (conftest DROP +
#    CREATE kho test) — `[ĐỎ] pytest · bỏ qua`.
#    ⭐⭐ `xfailed` cũng là bài ⛔ được đo xanh (S0-R3-01): tệp đường nền khai từng node xfail bằng
#    dòng `XFAIL <id>`, pytest chạy `-rfEx`, và tập so gồm cả LOẠI — thêm/bớt một xfail, hay một
#    node đổi loại (đỏ ⇄ xfail), đều `[ĐỎ]`. Mọi tập "được miễn" phải có `mong` theo TÊN.
#
#  ⛔ In mật khẩu của DSN: mọi chỗ in DSN đều che `://user:***@` (S0-R1-06), kể cả dòng từ chối —
#    tới `@` CUỐI dòng, user ngoài lớp ⇒ `://***@`, `password=` ⇒ che tới hết dòng (S0-R2-02);
#    ⛔ có `://` (lược đồ gõ sai/thiếu) ⇒ che từ `:` ĐẦU tới `@` cuối; dòng từ chối của một giá trị
#    ⛔ có `@` ⇒ ⛔ in giá trị, chỉ in độ dài (S0-R3-03).
#    Ngoại lệ DUY NHẤT: hai dòng `export` cuối lượt in mật khẩu khi nó là mặc định CÔNG KHAI
#    `fls` (`fls/db/kho.py:44` · `CLAUDE.md` §Cổng · `CREATE ROLE … PASSWORD 'fls'` dưới đây) —
#    để agent chép được nguyên dòng; mật khẩu khác ⇒ vẫn che.
#
# Biến đổi được (mặc định là sự thật đã đo ở container 16/11):
#   FLS_PG_PORT      cổng của lượt          (như --cong; cả hai đặt mà khác nhau ⇒ từ chối)
#   FLS_VENV         venv dùng chung        (mặc định <checkout chính>/.venv)
#   FLS_PGDATA       thư mục dữ liệu cụm    (mặc định /home/user/fls-pg16 cho 5433, /home/user/fls-pg16-<N> — NGOÀI repo)
#   FLS_PGBIN        binary PostgreSQL 16   (mặc định /usr/lib/postgresql/16/bin)
#   FLS_DUONG_NEN_DO tệp node id bài đỏ có sẵn + dòng `XFAIL <id>` (mặc định docs/ITL/03_Dev/isp-3.1/duong_nen_bai_do.txt)
#   PG_DSN           kho `fls` cục bộ       (mặc định postgresql://fls:fls@localhost:<N>/fls — trùng fls/db/kho.py ở 5433)
#   PG_DSN_TEST      kho test               (bỏ trống ⇒ `fls_test` cùng cụm, do fls/db/kho.py suy từ PG_DSN)
set -uo pipefail

# Tập cổng của ISP (TIEN_DO.md · Quy ước chạy song song). Thêm agent ⇒ thêm cổng Ở ĐÂY.
CONG_ISP="5433 5434 5435 5436 5437 5444 5445 5446 5447"

# ── CLI · từ chối MỌI đối số ⛔ khai (S0-R1-03: bản đầu chỉ soát `$1` ⇒ `--chi-kiem --la` exit 0,
#    `--duong-nen --chi-kiem` thì DỰNG dù người gọi muốn chỉ kiểm).
#    ⛔⛔ S0-R2-01: `--cong ''` (giá trị RỖNG) bản trước ⛔ từ chối — `CONG_DOI_SO` rỗng ⇒ rơi về
#    FLS_PG_PORT rồi 5433 (cụm gốc S0, của người khác); và chốt "hai lần" hỏi `-n "$CONG_DOI_SO"`
#    nên `--cong '' --cong 5435` lọt. Đường thật: `--cong "$BIEN"` với biến rỗng. ⇒ giá trị rỗng
#    là LỖI ĐẦU VÀO (exit 2), và "đã thấy --cong" là một cờ RIÊNG, ⛔ suy từ giá trị.
CHE_DO=""; CO_CHE_DO=""; CONG_DOI_SO=""; CO_CONG=""; N_DOI_SO=$#
while [ "$#" -gt 0 ]; do
  case "$1" in
    --duong-nen|--chi-kiem)
      if [ -n "$CO_CHE_DO" ]; then
        echo "⛔ hai chế độ cùng lúc ($CO_CHE_DO + $1) — chọn MỘT (xem --help)" >&2; exit 2
      fi
      CO_CHE_DO="$1"
      if [ "$1" = --duong-nen ]; then CHE_DO="duong_nen"; else CHE_DO="chi_kiem"; fi ;;
    --cong)
      if [ -n "$CO_CONG" ]; then echo "⛔ --cong đưa hai lần — từ chối" >&2; exit 2; fi
      if [ "$#" -lt 2 ]; then echo "⛔ --cong thiếu giá trị (xem --help)" >&2; exit 2; fi
      if [ -z "$2" ]; then
        echo "⛔ --cong '' — giá trị RỖNG (biến cổng chưa đặt?) — từ chối, ⛔ rơi về FLS_PG_PORT/5433 (cụm của người khác)" >&2; exit 2
      fi
      CO_CONG=1; CONG_DOI_SO="$2"; shift ;;
    -h|--help)
      if [ "$N_DOI_SO" != 1 ]; then echo "⛔ --help ⛔ đi kèm đối số khác — từ chối" >&2; exit 2; fi
      sed -n '2,8p' "$0"; exit 0 ;;
    *)  echo "⛔ đối số lạ: $1 (xem --help)" >&2; exit 2 ;;
  esac
  shift
done
CHE_DO="${CHE_DO:-dung}"

# ── cổng của lượt: --cong ⇒ FLS_PG_PORT ⇒ 5433; ⛔ thuộc tập ISP ⇒ từ chối.
#    S0-R2-01 (cùng lớp, nguồn thứ hai): FLS_PG_PORT ĐẶT mà RỖNG (`FLS_PG_PORT=$BIEN` với biến
#    rỗng) cũng là lỗi đầu vào — hỏi "có ĐẶT không" (`+x`), ⛔ để `:-` nuốt thành "không đặt".
if [ -n "${FLS_PG_PORT+x}" ] && [ -z "$FLS_PG_PORT" ]; then
  echo "⛔ FLS_PG_PORT đặt mà RỖNG — từ chối, ⛔ rơi về 5433 (cụm của người khác). Gỡ biến hoặc đặt cổng." >&2; exit 2
fi
CONG_BIEN="${FLS_PG_PORT:-}"
if [ -n "$CONG_DOI_SO" ] && [ -n "$CONG_BIEN" ] && [ "$CONG_DOI_SO" != "$CONG_BIEN" ]; then
  echo "⛔ --cong $CONG_DOI_SO ≠ FLS_PG_PORT=$CONG_BIEN — hai nguồn cổng mâu thuẫn, từ chối" >&2; exit 2
fi
CONG="${CONG_DOI_SO:-${CONG_BIEN:-5433}}"
case " $CONG_ISP " in
  *" $CONG "*) ;;
  *) echo "⛔ cổng '$CONG' ⛔ thuộc tập cổng ISP ($CONG_ISP) — từ chối" >&2; exit 2 ;;
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
if [ "$CONG" = 5433 ]; then PGDATA_MAC_DINH=/home/user/fls-pg16; else PGDATA_MAC_DINH="/home/user/fls-pg16-$CONG"; fi
PGDATA_ISP="${FLS_PGDATA:-$PGDATA_MAC_DINH}"
SOCK=/var/run/postgresql
DUONG_NEN_DO="${FLS_DUONG_NEN_DO:-$GOC/docs/ITL/03_Dev/isp-3.1/duong_nen_bai_do.txt}"
export PG_DSN="${PG_DSN:-postgresql://fls:fls@localhost:$CONG/fls}"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8

# ── S0-R2-02 · MỘT lớp ký tự cho userinfo của DSN, DÙNG CHUNG bởi khuôn chốt `RE_DSN` (② dưới)
#    và hàm che `che_dong`. ⛔⛔ R2 (`KQ-068`) đo HAI lớp khác nhau: khuôn nhận mật khẩu `[^@/?#]+`
#    (CÓ khoảng trắng), hàm che dừng ở khoảng trắng `[^@[:space:]]*` ⇒ `fls:bi mat@…` QUA chốt và
#    in nguyên mật khẩu 4 dòng (tiêu đề ×2 · `export` ×2); `fls:ab@cdXYZ@…` bị từ chối nhưng câu
#    từ chối lộ đuôi `cdXYZ`; `password='a b'` ⇒ `password=*** b'`. (Chú thích bản trước còn ghi
#    `[^@]*` trong khi mã là `[^@[:space:]]*` — lệch thêm một lớp nữa.)
#    ⭐ Khoảng trắng nằm NGOÀI lớp (libpq vốn từ chối: psycopg báo `unexpected spaces found`).
#    ⭐ Đọc theo BYTE (`LC_ALL=C`) ở CẢ HAI nơi: Python đặt `LC_CTYPE=C.UTF-8` cho tiến trình con
#       (PEP 538) còn shell container là POSIX — cùng script chạy hai locale; và `sed` ở locale
#       UTF-8 ⛔ khớp `.` qua một byte UTF-8 lẻ ⇒ lọt (đo khi viết bài: `Kq7\xa0Wx9` in nguyên).
LOP_USER='[^:@/?#[:space:]]'   # tên user: ⛔ `:` `@` `/` `?` `#`, ⛔ khoảng trắng
LOP_MK='[^@/?#[:space:]]'      # mật khẩu: ⛔ `@` `/` `?` `#`, ⛔ khoảng trắng
# ── S0-R1-06 · che mật khẩu MỌI chỗ in DSN — kể cả dòng từ chối, nơi giá trị có thể ở NGOÀI lớp:
#    ① user trong lớp ⇒ giữ user, che từ sau `://<user>:` tới `@` CUỐI dòng (`.*@`, ⛔ `[^@]*@`:
#       mật khẩu có `@` thô ⇒ ⛔ lộ đuôi). Mọi mật khẩu khuôn CHẤP NHẬN đều nằm trọn trong đoạn ấy.
#    ② user NGOÀI lớp (khoảng trắng, `@`, `/`…) ⇒ che trọn `://***@` tới `@` cuối (có `:` ở giữa).
#    ③ dạng từ khoá: che từ `password=` tới HẾT dòng (`password='a b'` có nháy + khoảng trắng).
#    `che` (một GIÁ TRỊ): xuống dòng in thành `\n` TRƯỚC khi che — bản trước che theo DÒNG nên
#    `fls:ab<LF>cd@…` lộ nửa đầu. Che thừa (mất host khi dòng có hai `@`) là lỗi an toàn.
#    Dấu phân cách `|`, ⛔ `#`: biểu thức có `#` trong ngoặc vuông.
#    ⛔⛔ S0-R3-03 · ① ② đều neo vào `://` ⇒ R3 (`KQ-069`) đo DSN gõ SAI lược đồ — `fls:<mk>@…` ·
#       `postgresql:/fls:<mk>@…` · `postgresql:fls:<mk>@…` — bị chốt từ chối (đúng) nhưng câu từ
#       chối in NGUYÊN mật khẩu (có từ `fec4dd0`: phép quét 76 ca chỉ biến KÝ TỰ, ⛔ biến CẤU TRÚC).
#    ④ dòng ⛔ khớp ① ② (⛔ `://`, hay `://` mà ⛔ có `:` trước `@`) ⇒ che từ `:` ĐẦU dòng tới `@`
#       CUỐI. Che thừa (`postgresql://fls@h…` ⛔ mật khẩu cũng thành `postgresql:***@h…`) là lỗi an toàn.
che() { local v="${1//$'\n'/\\n}"; printf '%s\n' "${v//$'\r'/\\r}" | che_dong; }
che_dong() {
  LC_ALL=C sed -E \
    -e "s|(://${LOP_USER}*):.*@|\\1:***@|" -e 't tu_khoa' \
    -e 's|://.*:.*@|://***@|' -e 't tu_khoa' \
    -e 's|^([^:@]*):.*@|\1:***@|' \
    -e ':tu_khoa' \
    -e 's/(password[[:space:]]*=).*/\1***/I'
}
# S0-R3-03 · giá trị BỊ TỪ CHỐI là chuỗi HỎNG — ⛔ biết mật khẩu nằm đâu. Mọi luật che neo vào `@`
#   (mật khẩu đứng TRƯỚC `@` cuối); giá trị ⛔ có `@` (gõ `/` thay `@` · dạng từ khoá) ⇒ ⛔ in giá trị,
#   chỉ in độ dài theo byte — đường từ chối an toàn nhất là ⛔ in (luật sổ `S0-R3-03`).
che_tu_choi() {
  case "$1" in
    *@*) che "$1" ;;
    *)   printf '<%s byte · ⛔ có @ ⇒ ⛔ in giá trị (có thể mang mật khẩu)>\n' "${#1}" ;;
  esac
}

# Đ5 — bộ đếm ĐỎ dùng chung cho cả DỰNG lẫn KIỂM. ⭐ Bước dựng hỏng cũng là ĐỎ: ⛔ để một phép
# kiểm xanh "nhờ" một cụm/kho KHÁC che đi việc cụm của tệp này ⛔ dựng được (đo 16/11 khi soát lại
# bản đầu: bước cụm bị từ chối mà 6 phép kiểm vẫn ĐẠT vì cụm cũ còn chạy ⇒ exit 0 sai).
DO=0
dat() { printf '  [ĐẠT] %-26s %s\n' "$1" "$2"; }
do_() { printf '  [ĐỎ]  %-26s %s\n' "$1" "$2"; DO=$((DO + 1)); }
# S0-R2-04 · lý do ⛔ được chạy bước GHI kế tiếp — pytest (`tests/conftest.py` DROP + CREATE kho
#   test). ⛔⛔ Bản trước in `[ĐỎ]` ở dựng/K2 rồi VẪN chạy pytest: R2 đo OID `fls_test` đổi trên
#   một cụm mà K2 vừa chứng minh ⛔ phải của mình — phép kiểm chỉ in mà ⛔ chặn là biên bản.
CHAN_GHI=""
chan_ghi() { CHAN_GHI="${CHAN_GHI:+$CHAN_GHI · }$1"; }

# ── ② chốt an toàn — chạy TRƯỚC mọi thứ (kể cả ở chế độ chỉ kiểm), TRƯỚC dòng tiêu đề.
if [ -n "${FLS_CHO_GHI_THAT:-}" ]; then
  echo "⛔ FLS_CHO_GHI_THAT đang đặt — tệp này ⛔ được chạy cạnh quyền ghi sổ thật. Gỡ biến rồi chạy lại." >&2
  exit 2
fi
# ⓒ — libpq lấy đích từ các biến này khi DSN ⛔ ghi; `hostaddr` còn THẮNG `host`. Hỏi "có ĐẶT
#     không" (`${!v+x}`), ⛔ hỏi giá trị: đặt rỗng cũng từ chối — rẻ hơn đoán libpq hiểu rỗng ra sao.
for BIEN in PGHOST PGHOSTADDR PGPORT PGSERVICE PGSERVICEFILE; do
  if [ -n "${!BIEN+x}" ]; then
    echo "⛔ biến $BIEN đang đặt — libpq sẽ gộp nó vào đích nối của PG_DSN (R1 đo: PGHOSTADDR=10.255.255.1 ⇒ nối 10.255.255.1). Gỡ biến rồi chạy lại." >&2
    exit 2
  fi
done
# ⓐ ⓑ — khuôn NGUYÊN CHUỖI: lớp `LOP_USER`/`LOP_MK` (⛔ `@ / ? #`, ⛔ khoảng trắng — S0-R2-02)
#     chặn `/` trước `@` (ⓑ), `$` sau tên kho chặn query (ⓐ).
RE_DSN="^postgresql://(${LOP_USER}+):(${LOP_MK}+)@(localhost|127\\.0\\.0\\.1):([0-9]+)/([a-z0-9_]+)\$"
kiem_dsn() {   # $1 = tên biến · $2 = giá trị — lệch ⇒ exit 2; khớp ⇒ đặt KHO_DSN = tên kho
  local LC_ALL=C   # đọc theo BYTE như `che_dong` (S0-R2-02) — `local` trả locale cũ khi ra hàm
  if ! [[ $2 =~ $RE_DSN ]]; then
    echo "⛔ $1=$(che_tu_choi "$2") ⛔ khớp NGUYÊN CHUỖI postgresql://<user>:<pass>@(localhost|127.0.0.1):<cổng>/<tên kho [a-z0-9_]> — ⛔ query string, ⛔ host khác, ⛔ khoảng trắng hay @ / ? # trong user/mật khẩu. Từ chối (kho ở đây phải là kho RỖNG cục bộ)." >&2
    exit 2
  fi
  if [ "${BASH_REMATCH[4]}" != "$CONG" ]; then
    echo "⛔ $1 trỏ cổng ${BASH_REMATCH[4]} ≠ cổng của lượt $CONG (--cong / FLS_PG_PORT) — từ chối: dựng cụm này mà di trú/kiểm cụm kia." >&2
    exit 2
  fi
  KHO_DSN="${BASH_REMATCH[5]}"
}
kiem_dsn PG_DSN "$PG_DSN"
TEN_KHO="$KHO_DSN"
# PG_DSN_TEST: `--duong-nen` chạy pytest, và tests/conftest.py DROP + CREATE kho của biến này ⇒ cùng
# lớp rủi ro với PG_DSN ⇒ cùng chốt. Bỏ trống ⇒ fls/db/kho.py suy `fls_test` từ PG_DSN (cùng cụm).
if [ -n "${PG_DSN_TEST:-}" ]; then
  kiem_dsn PG_DSN_TEST "$PG_DSN_TEST"
  DSN_TEST_IN="$PG_DSN_TEST"
else
  DSN_TEST_IN="${PG_DSN%/*}/fls_test"
fi

cd "$GOC" || exit 2

# Lệnh của user `postgres`: initdb TỪ CHỐI chạy bằng root (đo 16/11) ⇒ `runuser`.
chay_pg() {
  if [ "$(id -u)" = 0 ]; then runuser -u postgres -- "$@"; else "$@"; fi
}
# psql quản trị qua socket (xác thực `peer` của user postgres) — ⛔ cần mật khẩu.
psql_qt() {
  chay_pg "$PGBIN/psql" -X -v ON_ERROR_STOP=1 -h "$SOCK" -p "$CONG" -d postgres -tA "$@"
}
# S0-R1-04 · heredoc Python in KẾT QUẢ trên dòng cuối, hoặc đúng MỘT dòng `LOI <Kiểu>: <câu>`
#   (bản đầu lấy `tail -1` của traceback ⇒ in mảnh vụn `áp 'Is' … lệch 'the'`, mất nguyên nhân).
#   Bash đọc dòng `LOI` nếu có, ⛔ thì dòng cuối.
loi_hoac_cuoi() { local l; l="$(printf '%s\n' "$1" | grep -m1 '^LOI ')"; printf '%s\n' "${l:-$(printf '%s\n' "$1" | tail -1)}" | che_dong; }

echo "══ dung_moi_truong_isp · chế độ $CHE_DO · $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "   GOC (mã fls)   = $GOC"
echo "   venv dùng chung = $VENV"
echo "   cụm PG16       = $PGDATA_ISP (cổng $CONG)"
echo "   PG_DSN         = $(che "$PG_DSN")"
echo "   PG_DSN_TEST    = $(if [ -n "${PG_DSN_TEST:-}" ]; then che "$PG_DSN_TEST"; else echo "<trống ⇒ $(che "$DSN_TEST_IN") (fls/db/kho.py suy từ PG_DSN)>"; fi)"

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
    # ① cụm có sẵn mà khai cổng KHÁC ⇒ khởi động nó là dựng một cụm rồi kiểm/di trú ở cổng kia.
    local cong_khai
    cong_khai="$(chay_pg "$PGBIN/postgres" -D "$PGDATA_ISP" -C port 2>/dev/null)"
    if [ "$cong_khai" != "$CONG" ]; then
      echo "⛔ cụm $PGDATA_ISP khai port '${cong_khai:-?}' ≠ cổng của lượt $CONG — TỪ CHỐI (⛔ sửa cấu hình hộ ai)."
      return 1
    fi
  else
    if [ -e "$PGDATA_ISP" ] && [ -n "$(ls -A "$PGDATA_ISP" 2>/dev/null)" ]; then
      echo "⛔ $PGDATA_ISP có dữ liệu mà ⛔ phải cụm PG — TỪ CHỐI (⛔ xoá hộ ai)."
      return 1
    fi
    echo "── cụm: chưa có ⇒ initdb $PGDATA_ISP"
    install -d -m 700 -o postgres -g postgres "$PGDATA_ISP"
    chay_pg "$PGBIN/initdb" -D "$PGDATA_ISP" -U postgres -E UTF8 --locale=C.UTF-8 \
      --auth-local=peer --auth-host=scram-sha-256 >/dev/null || { echo "⛔ initdb hỏng"; return 1; }
    # cổng của lượt (5433 = mặc định của fls/db/kho.py) · chỉ nghe localhost · socket ở thư mục chuẩn
    # Debian — mỗi cổng một tệp socket `.s.PGSQL.<cổng>` nên nhiều cụm dùng chung thư mục được.
    chay_pg sh -c "printf '%s\n' \"# dung_moi_truong_isp.sh\" \"port = $CONG\" \"listen_addresses = 'localhost'\" \"unix_socket_directories = '$SOCK'\" >> '$PGDATA_ISP/postgresql.conf'"
  fi
  if chay_pg "$PGBIN/pg_ctl" -D "$PGDATA_ISP" status >/dev/null 2>&1; then
    echo "── cụm: đang chạy ⇒ giữ"
  else
    # ① cổng đã có người nghe mà ⛔ phải cụm này ⇒ ⛔ chen (trên máy owner 5433 là kho THẬT).
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
  local kq n
  kq="$("$PY" - <<'PY' 2>&1
import os, sys
try:
    from fls.db.kho import noi_chi_doc
    c = noi_chi_doc(os.environ["PG_DSN"])
    try:
        co = c.execute("select to_regclass('public.fls_itl') is not null").fetchone()[0]
        print(c.execute("select count(*) from fls_itl").fetchone()[0] if co else 0)
    finally:
        c.close()
except Exception as e:
    print(f"LOI {type(e).__name__}: {' '.join(str(e).split())[:200]}")
    sys.exit(1)
PY
)" || { echo "⛔ ⛔ đếm được fls_itl trước di trú: $(loi_hoac_cuoi "$kq")"; return 1; }
  n="$(printf '%s\n' "$kq" | tail -1)"
  if [ "$n" != 0 ]; then
    echo "⛔ kho $TEN_KHO có $n dòng fls_itl ⇒ ⛔ phải kho RỖNG cục bộ — TỪ CHỐI di trú"
    return 1
  fi
  echo "── di trú: $PY -m fls.db.pg_migrate   (kho $TEN_KHO: 0 dòng fls_itl)"
  "$PY" -m fls.db.pg_migrate 2>&1 | che_dong | sed 's/^/   │ /'
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
  [ "$DO" = 0 ] || chan_ghi "dựng ĐỎ ($DO bước)"
fi

# ═════════════════════════════════════════════════════════════════ KIỂM (Đ5: `mong` khai trước)
# ⭐ `mong` của lint-imports: 9 hợp đồng cũ + 2 của S0 (`fls.cau_hinh` · `fls.bao_cao`). Bước nào
#    thêm/bớt một hợp đồng tầng thì phải SỬA SỐ NÀY — đó chính là điều Đ5 muốn: đổi một chỗ là ĐỎ.
MONG_LINT_KEPT=11
MONG_LINT_BROKEN=0
# ⭐ `mong` của HD1 (tools/do_voi_so_luong.py · MONG so_dong_so / so_dong_ghep_canon — ghim 16/11).
MONG_HD1_CO=9967
MONG_HD1_CHAY=9845
# ⭐ `mong` MẪU SỐ của đường nền (S0-R2-03) — số bài pytest CHẠY tối thiểu mỗi lượt `--duong-nen`.
#    Đo ở lượt chính thức sau vòng sửa R1 (cây `5be45f5`, 16/11): toàn bộ `12 failed, 2432 passed,
#    2 xfailed, 14 errors` = 2.460 bài (2.430 của §4 DUONG_NEN + 30 bài tests/test_dung_moi_truong_isp.py)
#    · `tests/web` `3 failed, 661 passed` = 664 bài. Mong là "≥" — bước sau THÊM bài vẫn đạt; BỚT
#    (skip · deselect · `--lf` · `-k`) thì ĐỎ. Bước nào XOÁ bài có chủ đích ⇒ sửa số Ở ĐÂY + ghi lý do.
# ⛔⛔ S0-R3-02 · số trên là của vòng R1 và bị ĐỂ LẠI ở vòng R2 (+21 bài ⇒ nhánh thu thập 2.481): R3
#    (`KQ-069`) bỏ IM LẶNG cả `tests/adapters/test_bank.py` (20 bài, ⛔ dòng `deselected`) ⇒ `chạy
#    2461 bài (mong ≥ 2460)` ⇒ `[ĐẠT]`. Q8 = A: hằng = số bài THU THẬP của nhánh (`pytest
#    --collect-only` — đường nền: 0 skipped · 0 deselected ⇒ thu thập = chạy), nâng TRONG CÙNG commit
#    thêm bài; bài `tests/test_dung_moi_truong_isp.py::test_S0_R3_02_…` đòi hằng = thu thập ⇒ quên
#    nâng là ĐỎ. Sau vòng sửa R3: 2.481 + 9 bài mới = 2.490 bài ở 211 tệp · `tests/web` 664 ở 56 tệp.
MONG_PYTEST_TOAN_BO=4653
MONG_PYTEST_WEB=690

echo
echo "══ KIỂM"
# K1 · venv có đủ ba gói của requirements.txt
if [ -x "$PY" ] && "$PY" -c "import psycopg, pytest, importlinter" 2>/dev/null; then
  dat "venv + 3 gói" "$("$PY" -c 'import psycopg, pytest, importlib.metadata as m; print("psycopg", psycopg.__version__, "· pytest", pytest.__version__, "· import-linter", m.version("import-linter"))')"
else
  do_ "venv + 3 gói" "mong: $PY import được psycopg · pytest · importlinter — đo: ⛔"
fi

# K2 · cụm CỦA MÌNH ($PGDATA_ISP) nghe ở localhost:$CONG — ĐỊNH DANH, ⛔ chỉ "có ai trả lời ở cổng".
#   ⛔⛔ S0-R1-10: bản đầu chỉ hỏi `pg_isready` ⇒ R1 cho một cụm KHÁC chiếm 5433 (cụm của mình tắt)
#   mà vẫn `[ĐẠT] cụm PG localhost:5433` — trên máy owner đó là `fls-pg-1`. Nay đòi đủ bốn: ①
#   `pg_ctl -D <thư mục của cổng> status` exit 0 · ② `postmaster.pid` (dòng 4) ghi đúng cổng · ③
#   `pg_isready` ở cổng ấy · ④ tiến trình phục vụ một kết nối bằng PG_DSN là CON của postmaster
#   (dòng 1 của `postmaster.pid`) — tức đích nối của PG_DSN chính là cụm trong thư mục ấy.
K2_LY_DO=""
if ! chay_pg "$PGBIN/pg_ctl" -D "$PGDATA_ISP" status >/dev/null 2>&1; then
  K2_LY_DO="pg_ctl -D $PGDATA_ISP status ≠ 0 (cụm của mình ⛔ chạy)"
else
  PID_CUM="$(sed -n 1p "$PGDATA_ISP/postmaster.pid" 2>/dev/null)"
  CONG_CUM="$(sed -n 4p "$PGDATA_ISP/postmaster.pid" 2>/dev/null)"
  if [ "$CONG_CUM" != "$CONG" ]; then
    K2_LY_DO="cụm $PGDATA_ISP nghe cổng '${CONG_CUM:-?}' ≠ $CONG"
  elif ! "$PGBIN/pg_isready" -q -h localhost -p "$CONG" 2>/dev/null; then
    K2_LY_DO="pg_isready localhost:$CONG ⛔ trả lời"
  elif [ ! -x "$PY" ]; then
    K2_LY_DO="⛔ có venv để hỏi tiến trình phục vụ của PG_DSN"
  else
    CHA="$("$PY" - <<'PY' 2>&1
import os, sys
try:
    import psycopg
    with psycopg.connect(os.environ["PG_DSN"], connect_timeout=5) as c:
        pid = c.execute("select pg_backend_pid()").fetchone()[0]
        # đọc khi kết nối CÒN MỞ — đóng rồi thì tiến trình phục vụ đã thoát
        with open(f"/proc/{pid}/status", encoding="utf-8") as f:
            print(next(d.split()[1] for d in f if d.startswith("PPid:")))
except Exception as e:
    print(f"LOI {type(e).__name__}: {' '.join(str(e).split())[:200]}")
    sys.exit(1)
PY
)"
    CHA_DONG="$(loi_hoac_cuoi "$CHA")"
    [ "$CHA_DONG" = "$PID_CUM" ] \
      || K2_LY_DO="tiến trình phục vụ PG_DSN có cha '$CHA_DONG' ≠ postmaster $PID_CUM của $PGDATA_ISP"
  fi
fi
if [ -z "$K2_LY_DO" ]; then
  dat "cụm PG localhost:$CONG" "cụm CỦA MÌNH: pg_ctl status 0 · postmaster.pid cổng $CONG · pg_isready 0 · PG_DSN phục vụ bởi postmaster $PID_CUM"
else
  do_ "cụm PG localhost:$CONG" "mong: cụm $PGDATA_ISP chạy, nghe $CONG, phục vụ PG_DSN — đo: $K2_LY_DO"
  chan_ghi "K2 ĐỎ (cụm ở cổng $CONG ⛔ chứng minh được là của mình)"
fi

# K3 · role fls đăng nhập được bằng chính PG_DSN và có CREATEDB (conftest DROP + CREATE kho test)
QUYEN="$( [ -x "$PY" ] && "$PY" - <<'PY' 2>&1
import os, sys
try:
    import psycopg
    with psycopg.connect(os.environ["PG_DSN"], connect_timeout=5) as c:
        print(c.execute("select rolcreatedb from pg_roles where rolname = current_user").fetchone()[0])
except Exception as e:
    print(f"LOI {type(e).__name__}: {' '.join(str(e).split())[:200]}")
    sys.exit(1)
PY
)"
QUYEN_DONG="$(loi_hoac_cuoi "$QUYEN")"
if [ "$QUYEN_DONG" = "True" ]; then
  dat "role fls LOGIN + CREATEDB" "đăng nhập bằng PG_DSN được · rolcreatedb = t"
else
  do_ "role fls LOGIN + CREATEDB" "mong: đăng nhập được + rolcreatedb = t — đo: '${QUYEN_DONG:-⛔ có venv}'"
fi

# K4 · di trú áp ĐỦ (số dòng fls_migration = số tệp NNNN_*.sql) + pg_verify khớp N bảng/view, N > 0
#   (S0-R1-05: bản đầu in "0 chỗ lệch" ⛔ mẫu số — Đ3) — qua kết nối CHỈ ĐỌC
N_TEP=$(ls "$GOC"/fls/db/migrations/[0-9][0-9][0-9][0-9]_*.sql 2>/dev/null | wc -l)
DT="$( [ -x "$PY" ] && "$PY" - <<'PY' 2>&1
import os, sys
try:
    from fls.db.kho import noi_chi_doc
    from fls.db.pg_verify import TABLES, so_sanh_voi_db
    c = noi_chi_doc(os.environ["PG_DSN"])
    try:
        n = c.execute("select count(*) from fls_migration").fetchone()[0]
        lech = so_sanh_voi_db(c)
    finally:
        c.close()
    print(f"{n} {len(lech)} {len(TABLES)}")
except Exception as e:
    print(f"LOI {type(e).__name__}: {' '.join(str(e).split())[:200]}")
    sys.exit(1)
PY
)"
DT_DONG="$(loi_hoac_cuoi "$DT")"
read -r N_AP N_LECH N_BANG <<<"$DT_DONG"
if [ "${DT_DONG#LOI }" = "$DT_DONG" ] && [ "$N_TEP" -gt 0 ] && [ "${N_AP:-}" = "$N_TEP" ] \
   && [ "${N_LECH:-}" = 0 ] && [ "${N_BANG:-0}" -gt 0 ] 2>/dev/null; then
  dat "di trú + pg_verify" "$N_AP/$N_TEP di trú áp · pg_verify khớp $N_BANG bảng/view (0 lệch)"
else
  if [ "${DT_DONG#LOI }" = "$DT_DONG" ] && [ -n "$DT_DONG" ]; then DT_DO="áp '${N_AP:-?}' / tệp $N_TEP · lệch '${N_LECH:-?}' · so '${N_BANG:-?}' bảng/view"
  else DT_DO="tệp $N_TEP · ${DT_DONG:-⛔ có venv}"; fi
  do_ "di trú + pg_verify" "mong: áp = tệp > 0 · 0 lệch trên N > 0 bảng/view — đo: $DT_DO"
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

# K7 · kho của PG_DSN RỖNG — `fls_itl` = 0 dòng, đếm qua kết nối CHỈ ĐỌC (S0-R1-10).
#   ⛔⛔ Bản đầu khai "kho `fls` ở đây RỖNG" (BG-066 · DUONG_NEN.md:10) mà ⛔ phép nào canh: đo 16/11
#   trên kho nháp có 1 dòng `fls_itl`, `--chi-kiem` vẫn 6/6 ĐẠT. Bảng chưa có (chưa di trú) ⇒ ⛔ đo
#   được ⇒ ĐỎ (Đ5), ⛔ coi là "0 dòng".
RONG="$( [ -x "$PY" ] && "$PY" - <<'PY' 2>&1
import os, sys
try:
    from fls.db.kho import noi_chi_doc
    c = noi_chi_doc(os.environ["PG_DSN"])
    try:
        if not c.execute("select to_regclass('public.fls_itl') is not null").fetchone()[0]:
            raise LookupError("⛔ có bảng fls_itl (chưa di trú?)")
        print(c.execute("select count(*) from fls_itl").fetchone()[0])
    finally:
        c.close()
except Exception as e:
    print(f"LOI {type(e).__name__}: {' '.join(str(e).split())[:200]}")
    sys.exit(1)
PY
)"
RONG_DONG="$(loi_hoac_cuoi "$RONG")"
if [ "$RONG_DONG" = 0 ]; then
  dat "kho $TEN_KHO RỖNG" "fls_itl = 0 dòng (kết nối chỉ đọc)"
else
  do_ "kho $TEN_KHO RỖNG" "mong: fls_itl = 0 dòng — đo: '${RONG_DONG:-⛔ có venv}'"
  chan_ghi "K7 ĐỎ (kho $TEN_KHO ⛔ chứng minh được là RỖNG)"
fi

# ═════════════════════════════════════════════════════════════════ ĐƯỜNG NỀN pytest (SO tập đỏ)
# ⭐ S0-R1-02 · đường nền là CỔNG chỉ khi có MÁY so tập đỏ hiện tại với tập đã ghi theo node id,
#    đỏ cả hai chiều. Tệp `$DUONG_NEN_DO`: mỗi dòng một node id (đã sắp, ⛔ chú thích) — ghi ở S0
#    từ §4.1 của DUONG_NEN.md (26 bài đọc SỔ THẬT tự đỏ trên kho rỗng). Bảng markdown là BIÊN BẢN.
#    Tách node id từ phần `short test summary info` của `-rfE`: dòng `FAILED <id>[ - <câu>]` /
#    `ERROR <id>[ - <câu>]`; cắt ở ` - ` ĐẦU TIÊN — một node id tự chứa ` - ` sẽ bị cắt sai ⇒ lệch
#    tập ⇒ ĐỎ (lỗi an toàn: đỏ giả, ⛔ xanh giả). (S0-R3-01: nay `-rfEx` + dòng `XFAIL <id>` — dưới.)
# ⭐⭐ S0-R2-03 · cổng so TẬP phải canh cả MẪU SỐ. R2 đo: `PYTEST_ADDOPTS=--lf … --duong-nen` ⇒
#    toàn bộ `12 failed, 14 errors in 0.94s` (26 / 2.460 bài) ⇒ `[ĐẠT] … 26 = 26` · `KẾT: ĐẠT`
#    exit 0; log cùng 26 id mà `2000 skipped` / `2434 deselected` cũng ĐẠT. Cùng lớp: `--deselect
#    <bài vừa đỏ>`, `-k "not …"`, `@pytest.mark.skip` lên bài vừa làm hỏng ⇒ bài ấy ⛔ còn đỏ ⇒ ⛔
#    THÊM ⇒ ĐẠT. ⇒ ĐẠT chỉ khi tập khớp VÀ dòng tổng kết có `skipped = 0` · `deselected = 0` · số
#    bài CHẠY (passed + failed + errors + xfailed + xpassed) ≥ `mong` — in số ấy CẠNH `26 = 26`.
# ⭐⭐ S0-R3-01 · `xfailed` cộng vào "chạy" mà ⛔ có `mong` về SỐ hay TÊN, và `-rfE` ⛔ liệt kê `XFAIL`.
#    R3 (`KQ-069`) đo đầu-cuối: plugin `PYTEST_PLUGINS` làm HỎNG một bài web đang xanh rồi gắn
#    `xfail(strict=True)` — chính thành ngữ "bài đỏ đã biết" của repo — ⇒ toàn bộ `12 failed, 2432
#    passed, 3 xfailed, 14 errors` ⇒ `[ĐẠT] 26 = 26 · chạy 2461` · web `chạy 664 (mong ≥ 664)` ⇒
#    `KẾT: ĐẠT` exit 0 (sàn web KHÍT ⇒ lỗ ⛔ nhờ khoảng dư). Chiều ngược (một xfail biến mất) cũng ĐẠT.
#    ⇒ `-rfEx` (`chay_pytest`); dòng `XFAIL <id>[ - <lý do>]` vào tập đo, GIỮ chữ `XFAIL` làm LOẠI
#    (dòng FAILED/ERROR chỉ còn `<id>`); tệp đường nền khai xfail bằng đúng dòng `XFAIL <id>`. So
#    theo TÊN + LOẠI: thêm/bớt một xfail ⇒ `+ THÊM  XFAIL <id>` / `− BỚT   XFAIL <id>`; một node đổi
#    loại (xfail(strict) tự qua ⇒ pytest in `FAILED … [XPASS(strict)]`; bài đỏ có sẵn bị gắn xfail)
#    ⇒ cùng TÊN mà khác LOẠI ⇒ thêm 1 · bớt 1 ⇒ ĐỎ. ⚠ `x` ⛔ gồm `X`: XPASS ⛔ strict ⛔ có tên ở đây
#    (bài QUA — ⛔ phải hồi quy); một xfail đường nền tự xpass thì BỚT ⇒ vẫn ĐỎ.
so_tap_do() {   # $1 nhãn · $2 log · $3 tiền tố node id (rỗng = toàn bộ) · $4 dòng tổng kết · $5 mong số bài chạy
  local nhan="$1" log="$2" tien_to="$3" tong="$4" mong_chay="$5" hien mong them bot n_hien n_mong
  local n_chay n_skip n_desel mau_so_dat="" n_xf_hien n_xf_mong
  if [ ! -f "$DUONG_NEN_DO" ]; then
    do_ "đường nền $nhan" "mong: có tệp $DUONG_NEN_DO — đo: ⛔ có (⛔ so được = ĐỎ)"; return
  fi
  # mong ⛔ khai / ⛔ phải số dương ⇒ ⛔ so được ⇒ ĐỎ (Đ5), ⛔ coi là "không có ngưỡng"
  if ! [[ ${mong_chay:-} =~ ^[1-9][0-9]*$ ]]; then
    do_ "đường nền $nhan" "mong: số bài chạy tối thiểu là số dương — đo: '${mong_chay:-<trống>}' (⛔ so được = ĐỎ)"; return
  fi
  # Đếm từ dòng tổng kết: `12 failed, 2432 passed, 2 xfailed, 14 errors in 311.47s (0:05:11)` — có
  #   hay ⛔ có viền `=====`; `1 warning` ⛔ phải bài; `no tests ran` ⇒ chạy 0.
  read -r n_chay n_skip n_desel <<<"$(printf '%s\n' "$tong" | awk '{
    for (i = 1; i < NF; i++) {
      v = $(i + 1); gsub(/[,=]/, "", v)
      if ($i !~ /^[0-9]+$/) continue
      if (v ~ /^(passed|failed|errors?|xfailed|xpassed)$/) c += $i
      else if (v == "skipped") s += $i
      else if (v == "deselected") d += $i
    }
    printf "%d %d %d\n", c, s, d }')"
  [ "$n_skip" = 0 ] && [ "$n_desel" = 0 ] && [ "$n_chay" -ge "$mong_chay" ] && mau_so_dat=1
  hien="$(mktemp "${TMPDIR:-/tmp}/fls_isp_hien.XXXXXX")"; mong="$(mktemp "${TMPDIR:-/tmp}/fls_isp_mong.XXXXXX")"
  # S0-R3-01: FAILED/ERROR ⇒ `<id>`; XFAIL ⇒ `XFAIL <id>` (giữ LOẠI) — rồi cắt ` - <câu>`.
  awk '/^=+ short test summary info =+$/ {v = 1; next} v && /^(FAILED|ERROR|XFAIL) /' "$log" \
    | sed -E 's/^(FAILED|ERROR) //; s/ - .*$//' | LC_ALL=C sort -u > "$hien"
  # tiền tố (lượt `tests/web`) so trên node id — dòng khai `XFAIL <id>` so phần sau `XFAIL `
  awk -v p="$tien_to" 'NF && (p == "" || index($0, p) == 1 || index($0, "XFAIL " p) == 1)' "$DUONG_NEN_DO" \
    | LC_ALL=C sort -u > "$mong"
  them="$(LC_ALL=C comm -13 "$mong" "$hien")"; bot="$(LC_ALL=C comm -23 "$mong" "$hien")"
  n_hien=$(wc -l < "$hien"); n_mong=$(wc -l < "$mong")
  n_xf_hien=$(grep -c '^XFAIL ' "$hien"); n_xf_mong=$(grep -c '^XFAIL ' "$mong")
  rm -f "$hien" "$mong"
  if [ -z "$them" ] && [ -z "$bot" ] && [ -n "$mau_so_dat" ]; then
    dat "đường nền $nhan" "tập đỏ + XFAIL = đường nền: $n_hien = $n_mong node id (trong đó XFAIL $n_xf_hien = $n_xf_mong · thêm 0 · bớt 0) · chạy $n_chay bài (mong ≥ $mong_chay) · skipped 0 · deselected 0"
  else
    do_ "đường nền $nhan" "mong: tập đỏ + XFAIL = $n_mong node id (XFAIL $n_xf_mong) của $(basename "$DUONG_NEN_DO")${tien_to:+ (tiền tố $tien_to)} · chạy ≥ $mong_chay bài · skipped 0 · deselected 0 — đo: $n_hien (XFAIL $n_xf_hien) · thêm $(printf '%s' "$them" | grep -c .) · bớt $(printf '%s' "$bot" | grep -c .) · chạy $n_chay · skipped $n_skip · deselected $n_desel"
    [ -z "$them" ] || printf '%s\n' "$them" | sed 's/^/        + THÊM  /'
    [ -z "$bot" ]  || printf '%s\n' "$bot"  | sed 's/^/        − BỚT   /'
  fi
}

chay_pytest() {   # $1 = nhãn · $2 = tiền tố node id (rỗng = toàn bộ) · $3 = mong số bài CHẠY tối thiểu · còn lại = đối số pytest
  local nhan="$1" tien_to="$2" mong_chay="$3"; shift 3
  local log; log="$(mktemp "${TMPDIR:-/tmp}/fls_isp_pytest.XXXXXX")"
  # ⛔ thêm `-q`: pyproject.toml đã có `-q`, thêm nữa là `-qq` và MẤT dòng tổng kết.
  # ⛔⛔ S0-R2-03 · `env -u PYTEST_ADDOPTS`: biến của shell người gọi (`--lf` · `-k` · `--deselect`
  #   · `-x`) đổi BỘ BÀI mà ⛔ hiện trên dòng lệnh — R2 đo `--lf` ⇒ 26/2.460 bài, `KẾT: ĐẠT`.
  # ⛔⛔ S0-R3-01 · câu cũ ở đây viết "cổng mẫu số ở `so_tap_do` vẫn canh mọi đường khác (plugin,
  #   conftest, mark)" — SAI với `xfail`: R3 gắn `xfail(strict)` qua plugin lên một bài vừa làm hỏng
  #   ⇒ `KẾT: ĐẠT`. Đúng sau sửa: đường `env -u` ⛔ chặn (plugin `PYTEST_PLUGINS`, `conftest`, mark)
  #   bị `so_tap_do` bắt KHI nó đổi BỘ BÀI (skip · deselect · bỏ im lặng xuống dưới `mong`) hoặc đổi
  #   TẬP FAILED/ERROR/XFAIL theo TÊN + LOẠI (`-rfEx` — `x` = xfailed). ⛔ bắt: plugin biến đỏ thành
  #   QUA (passed), hay gắn xfail ⛔ strict lên bài vẫn qua (XPASS — `x` ⛔ gồm `X`).
  env -u PYTEST_ADDOPTS "$PY" -m pytest -rfEx "$@" >"$log" 2>&1
  local ma=$?
  local tong; tong="$(grep -E '^(=+ )?[0-9]+ (passed|failed|error|skipped|deselected|xfailed|xpassed)|^=+ .*(passed|failed|error).* =+$|no tests ran' "$log" | tail -1)"
  echo "  ── pytest $nhan · exit $ma · log $log"
  echo "     $tong"
  case "$ma" in
    0|1) ;;                                      # đo được (1 = có bài đỏ — so với đường nền dưới)
    *)   do_ "pytest $nhan" "mong: chạy nổi (exit 0 hoặc 1) — đo: exit $ma"; return ;;
  esac
  if [ -z "$tong" ]; then do_ "pytest $nhan" "mong: có dòng tổng kết — đo: ⛔ có"; return; fi
  so_tap_do "$nhan" "$log" "$tien_to" "$tong" "$mong_chay"
}

if [ "$CHE_DO" = "duong_nen" ]; then
  echo
  echo "══ ĐƯỜNG NỀN pytest (bài đỏ CÓ SẴN ≠ lỗi môi trường — SO theo node id với $(basename "$DUONG_NEN_DO"))"
  if [ -n "${PYTEST_ADDOPTS+x}" ]; then
    echo "  ── PYTEST_ADDOPTS của shell người gọi = '$(che "$PYTEST_ADDOPTS")' ⇒ GỠ cho mọi lượt pytest dưới (S0-R2-03)"
  fi
  # S0-R2-04 · dựng / K2 / K7 ĐỎ ⇒ ⛔ chạy pytest: conftest sẽ DROP + CREATE kho test trên một cụm
  #   (hay cạnh một kho) mà phép kiểm vừa ⛔ chứng minh được là của mình. ĐỎ, ⛔ im lặng bỏ qua.
  if [ -n "$CHAN_GHI" ]; then
    do_ "pytest · bỏ qua" "mong: dựng + K2 + K7 ĐẠT trước khi pytest GHI (tests/conftest.py DROP + CREATE kho test) — đo: $CHAN_GHI ⇒ ⛔ chạy pytest"
  elif [ -x "$PY" ]; then
    chay_pytest "toàn bộ"   ""           "$MONG_PYTEST_TOAN_BO"
    chay_pytest "tests/web" "tests/web/" "$MONG_PYTEST_WEB" tests/web
  else
    do_ "pytest" "mong: có venv — đo: ⛔"
  fi
fi

# ═════════════════════════════════════════════════════════════════ DÙNG (Q1 · in sẵn cho agent)
# Hai dòng export trỏ đúng cụm của lượt: kho `fls` (hoặc kho của PG_DSN) + kho test `fls_test` —
# tên kho test GIỮ vì 19 tệp bài ghim nó. Mật khẩu in rõ CHỈ khi là mặc định công khai `fls`.
in_xuat() { if [[ $1 =~ ^postgresql://fls:fls@ ]]; then printf '%s\n' "$1"; else che "$1"; fi; }
echo
echo "══ DÙNG cụm cổng $CONG — chép vào shell của agent (chạy từ gốc worktree):"
echo "   export PG_DSN='$(in_xuat "$PG_DSN")'"
echo "   export PG_DSN_TEST='$(in_xuat "$DSN_TEST_IN")'"
echo "   export PYTHONUTF8=1"

echo
if [ "$DO" = 0 ]; then
  echo "══ KẾT: ĐẠT — mọi phép kiểm khớp mong"
  exit 0
fi
echo "══ KẾT: ĐỎ — $DO phép kiểm khác mong hoặc ⛔ đo được"
exit 1
