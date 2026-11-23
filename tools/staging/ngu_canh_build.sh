#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — dựng NGỮ CẢNH BUILD ảnh app: `git archive HEAD -- <danh sách cho phép>` ⇒ chỉ tệp ĐÃ COMMIT
# ══════════════════════════════════════════════════════════════════════════════════════════
#    bash tools/staging/ngu_canh_build.sh <gốc repo> <thư mục đích RỖNG>     → in "ngữ cảnh: N tệp, commit <sha>"
#
#  Dùng chung bởi `03_dung_app.sh` (Cloud Build) và `thu_dung_anh.sh` (bộ build CŨ cục bộ) ⇒ hai đường dựng MỘT ngữ cảnh.
#
#  ⭐ `STG-R2b-01` (lỗi THẬT GCP 23/11, bước 03): danh sách cũ có `.gcloudignore` (`*` rồi `!fls !tools …`) ⇒
#    `gcloud builds submit` áp nó lên ngữ cảnh: 398 tệp ngữ cảnh, **292** tải lên (= fls 141 + tools 150 +
#    requirements.txt 1 — đếm lại từ `c4a0f39`), ⛔ `Dockerfile` ⇒ Cloud Build `lstat /workspace/Dockerfile`.
#    Ngữ cảnh ĐÃ LÀ danh sách cho phép ⇒ `.gcloudignore` thừa và nguy hiểm ⇒ bỏ khỏi danh sách VÀ khỏi repo.
#    ⚠ Đo: ngữ nghĩa gitignore THUẦN cho 1/398 tệp (⛔ khớp 292) ⇒ gcloud xét TỪNG TIỀN TỐ đường dẫn, mẫu khớp
#      CẢ đường dẫn, `*` ⛔ qua `/` (mô hình này cho đúng 292 — `tests/staging/gcloud_gia.py` theo nó).
#  ⭐ `STG-R2b-04`: cây chưa commit/`HEAD` hỏng ⇒ `git archive` rỗng ⇒ trước đây `tar` báo lỗi khó hiểu ⇒ nay lỗi CÓ TÊN.
# ══════════════════════════════════════════════════════════════════════════════════════════
set -euo pipefail
GOC="${1:?gốc repo}" ; DICH="${2:?thư mục đích}"
DANH_SACH=(Dockerfile .dockerignore requirements.txt fls tools docs/ITL/_tools tests/fixture)
[ -d "$DICH" ] && [ -z "$(ls -A "$DICH")" ] || { echo "⛔ NGU_CANH_DICH_BAN: $DICH phải là thư mục RỖNG" >&2; exit 2; }
SHA="$(git -C "$GOC" rev-parse --verify --short HEAD 2>/dev/null)" \
  || { echo "⛔ NGU_CANH_RONG: $GOC ⛔ có HEAD (repo chưa commit nào?)" >&2; exit 2; }
git -C "$GOC" archive --format=tar HEAD -- "${DANH_SACH[@]}" | tar -x -C "$DICH" \
  || { echo "⛔ NGU_CANH_RONG: git archive HEAD hỏng (cây đang gộp dở / thiếu tệp trong danh sách?)" >&2; exit 2; }
N="$(find "$DICH" -type f | wc -l | tr -d ' ')"
[ "$N" -gt 0 ] && [ -f "$DICH/Dockerfile" ] \
  || { echo "⛔ NGU_CANH_RONG: ngữ cảnh $N tệp, Dockerfile $([ -f "$DICH/Dockerfile" ] && echo có || echo THIẾU) — commit cây trước" >&2; exit 2; }
for an in .gcloudignore .gitignore; do
  [ ! -e "$DICH/$an" ] || { echo "⛔ NGU_CANH_CO_TEP_LOC: $an trong ngữ cảnh — gcloud sẽ LỌC thêm (STG-R2b-01)" >&2; exit 2; }
done
BAN="$(git -C "$GOC" status --porcelain -- "${DANH_SACH[@]}" | wc -l | tr -d ' ')"
[ "$BAN" -eq 0 ] || echo "   ⚠ $BAN tệp trong danh sách cho phép CHƯA commit — ảnh dựng từ HEAD $SHA, ⛔ gồm chúng" >&2
echo "   ngữ cảnh: $N tệp, commit $SHA"
