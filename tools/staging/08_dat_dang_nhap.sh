#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING · bước 08 — ĐẶT tài khoản ĐĂNG NHẬP chung cho link web (sau Google IAP) · WO-363 bổ sung 24/11
# ══════════════════════════════════════════════════════════════════════════════════════════
#
#  AI CHẠY: CHỦ dự án, trong Google Cloud Shell. ⛔ Claude KHÔNG vào GCP, ⛔ biết mật khẩu.
#
#    bash tools/staging/08_dat_dang_nhap.sh --project <P> --kiem      # chỉ ĐỌC — đã đặt chưa
#    bash tools/staging/08_dat_dang_nhap.sh --project <P>             # hỏi mật khẩu (ẨN) 2 lần ⇒ băm ⇒ Secret Manager
#
#  Tuỳ chọn: --ten (mặc định HondurasGesha) · --bi-mat (mặc định fls-staging-login)
#
#  ⛔⛔ MẬT KHẨU: gõ khi script hỏi — `read -s` (⛔ hiện lên màn, ⛔ vào lịch sử shell, ⛔ argv). Nó chỉ đi qua ỐNG
#     (`printf` là lệnh có sẵn của bash ⇒ ⛔ hiện trong `ps`) vào `dang_nhap.py --bam`, ra BẢN GHI BĂM scrypt —
#     chỉ bản ghi băm lên Secret Manager. ⛔ dán mật khẩu vào chat/phiếu/repo. ⭐ Khuyên đặt mật khẩu MỚI (≥ 12 ký
#     tự), ⛔ dùng lại mật khẩu đã từng gõ ở bất kỳ đâu khác.
#
#  LÀM GÌ (chạy lại được — mỗi lần đặt = một PHIÊN BẢN MỚI của bí mật; phiên bản cũ GIỮ, ⛔ xoá):
#   ① bật API secretmanager
#   ② hỏi mật khẩu 2 lần (ẩn) · ≥ 12 ký tự · ⛔ trùng tên · băm scrypt
#   ③ bí mật chưa có ⇒ `secrets create … --data-file=-`; có ⇒ `secrets versions add … --data-file=-`
#   ④ SA `fls-staging-app` được `secretAccessor` trên ĐÚNG bí mật này (cổng IAP đọc nó lúc chạy)
#   ⑤ BÁO CÁO (⛔ mật khẩu, ⛔ băm): bí mật có · SA đọc được · bản ghi mới nhất ĐÚNG HÌNH (tên mong · `scrypt$…`)
#  Có hiệu lực ≤ 1 phút (cổng đọc lại bí mật mỗi 60 giây) — ⛔ cần dựng lại service. Đổi mật khẩu ⇒ mọi phiên cũ mất.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail

PROJECT="" ; TEN="HondurasGesha" ; BI_MAT="fls-staging-login" ; KIEM=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --ten)     TEN="$2"; shift 2 ;;
    --bi-mat)  BI_MAT="$2"; shift 2 ;;
    --kiem)    KIEM=1; shift ;;
    -h|--help) sed -n 2,28p "$0"; exit 0 ;;
    *) echo "⛔ tham số lạ: $1 (mật khẩu ⛔ đi qua tham số — script sẽ HỎI)" >&2; exit 2 ;;
  esac
done
[ -n "$PROJECT" ] || { echo "⛔ thiếu --project <PROJECT_ID>" >&2; exit 2; }
case "$TEN" in ""|*[!A-Za-z0-9._-]*) echo "⛔ --ten chỉ [A-Za-z0-9._-]" >&2; exit 2 ;; esac
case "$BI_MAT" in ""|*[!a-z0-9-]*) echo "⛔ --bi-mat chỉ [a-z0-9-]" >&2; exit 2 ;; esac
command -v gcloud  >/dev/null || { echo "⛔ không có gcloud — chạy trong Cloud Shell" >&2; exit 2; }
command -v python3 >/dev/null || { echo "⛔ không có python3" >&2; exit 2; }
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SA_EMAIL="fls-staging-app@${PROJECT}.iam.gserviceaccount.com"
G=(gcloud --project="$PROJECT" --quiet)
buoc() { printf '\n── %s\n' "$*"; }
co() { "${G[@]}" "$@" >/dev/null 2>&1; }

if [ "$KIEM" -eq 0 ]; then
  buoc "② mật khẩu cho tài khoản '$TEN' (gõ — ⛔ hiện; Enter để xong)"
  MK="" ; MK2=""
  IFS= read -rs -p "   mật khẩu MỚI (≥ 12 ký tự): " MK; echo
  IFS= read -rs -p "   gõ lại: " MK2; echo
  [ "$MK" = "$MK2" ] || { unset MK MK2; echo "⛔ hai lần gõ KHÁC nhau — ⛔ đổi gì" >&2; exit 2; }
  unset MK2
  BAN_GHI="$(printf '%s' "$MK" | python3 "$GOC/tools/staging/app/dang_nhap.py" --bam --ten "$TEN")" \
    || { unset MK; echo "⛔ mật khẩu ⛔ hợp lệ (xem dòng trên) — ⛔ đổi gì" >&2; exit 2; }
  unset MK

  buoc "① bật API secretmanager"
  "${G[@]}" services enable secretmanager.googleapis.com

  buoc "③ bí mật $BI_MAT (chỉ BẢN GHI BĂM)"
  if co secrets describe "$BI_MAT"; then
    printf '%s' "$BAN_GHI" | "${G[@]}" secrets versions add "$BI_MAT" --data-file=- >/dev/null
    echo "   có rồi ⇒ thêm PHIÊN BẢN mới (phiên bản cũ giữ; cổng dùng bản mới nhất)"
  else
    printf '%s' "$BAN_GHI" | "${G[@]}" secrets create "$BI_MAT" --replication-policy=automatic \
        --labels=app=fls,moi-truong=staging --data-file=- >/dev/null
    echo "   đã tạo"
  fi
  unset BAN_GHI

  buoc "④ SA fls-staging-app đọc được $BI_MAT"
  "${G[@]}" secrets add-iam-policy-binding "$BI_MAT" --member="serviceAccount:$SA_EMAIL" \
      --role=roles/secretmanager.secretAccessor >/dev/null
  echo "   $SA_EMAIL: secretAccessor (chỉ trên $BI_MAT)"
fi

# ══════════════════════════════ BÁO CÁO — gửi lại phần này ══════════════════════════════
buoc "BÁO CÁO (KHÔNG chứa mật khẩu/băm) — chép từ dòng này tới hết, gửi lại"
export PROJECT TEN BI_MAT SA_EMAIL KIEM
export R_CO="$(co secrets describe "$BI_MAT" && echo co || echo khong)"
export R_IAM="$("${G[@]}" secrets get-iam-policy "$BI_MAT" --format=json 2>/dev/null || echo '')"
# Bản ghi mới nhất đi THẲNG vào python qua ống — ⛔ vào biến môi trường, ⛔ in.
PYP="$(mktemp)" ; trap 'rm -f "$PYP"' EXIT
cat > "$PYP" <<'PY'
import json, os, sys
e = os.environ
def js(s):
    try: return json.loads(s) if s.strip() else None
    except ValueError: return None
rec = js(sys.stdin.read())
rec = rec if isinstance(rec, dict) else None
iam = js(e['R_IAM'])
sa = 'serviceAccount:' + e['SA_EMAIL']
doc = None if iam is None else any(b.get('role') == 'roles/secretmanager.secretAccessor' and sa in b.get('members', [])
                                   for b in iam.get('bindings', []))
hang = [
  ('project · bí mật · tên đăng nhập', '%s · %s · %s' % (e['PROJECT'], e['BI_MAT'], e['TEN']), None),
  ('bí mật đăng nhập có', e['R_CO'], 'co'),
  ('SA fls-staging-app đọc được bí mật đăng nhập', doc, True),
  ('bản ghi mới nhất: tên đăng nhập = mong', None if rec is None else rec.get('ten') == e['TEN'], True),
  ('bản ghi mới nhất: băm scrypt (⛔ mật khẩu thô)', None if rec is None else str(rec.get('bam', '')).startswith('scrypt$'), True),
]
do = 0
for ten, gt, mong in hang:
    if mong is None:
        print('   %-60s  %s' % (ten, gt))
    else:
        ok = gt == mong
        do += not ok
        print('   [%s] %-58s  %r  (mong %r)' % ('ĐẠT' if ok else 'ĐỎ', ten, gt, mong))
print("\n   Có hiệu lực ≤ 1 phút. Người test: link → Google → /login với tên %r + mật khẩu (báo riêng, ⛔ chat nhóm)." % e['TEN'])
print('\n══ chế độ: %s · KẾT: %s' % ('--kiem (chỉ đọc)' if e['KIEM'] == '1' else 'đặt',
                                    'ĐẠT' if do == 0 else 'ĐỎ — %d mục khác mong' % do))
raise SystemExit(1 if do else 0)
PY
"${G[@]}" secrets versions access latest --secret="$BI_MAT" 2>/dev/null | python3 "$PYP"
