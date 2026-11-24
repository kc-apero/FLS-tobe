# ══════════════════════════════════════════════════════════════════════════════════════════
#  FLS STAGING — ảnh chạy CỬA API + MÀN HÌNH (`tools/chay_cua.py --cho-web`) · WO-325 AC-2
# ══════════════════════════════════════════════════════════════════════════════════════════
#  ⛔ Ảnh này ⛔ chứa bí mật nào: mật khẩu kho + khoá JWT được `tools/staging/app/vao.sh` đọc từ
#     Secret Manager LÚC CHẠY (bằng SA `fls-staging-app` gắn vào VM) và chỉ đưa cho tiến trình cửa.
#  ⛔ Ảnh này ⛔ mở cổng ra ngoài: cửa TỰ TỪ CHỐI `--cho-web` ngoài loopback (`fls.api.cua.kiem_phuc_vu_tep`,
#     `GAP-WEB-01`) ⇒ chạy bằng `--network host` trên VM, nghe 127.0.0.1:8088; người test vào bằng
#     IAP SSH tunnel (xem `tools/staging/README.md`).
#  ⭐ Nội dung ảnh là DANH SÁCH CHO PHÉP (`COPY` từng thư mục) VÀ `.dockerignore` là `*` + ngoại lệ:
#     `sao_luu/` · `hien_vat/` · `Input_Raw/` · `.env*` · `.git/` · `AS-IS system/` ⛔ vào ảnh dù ai đó
#     thêm một `COPY . .` về sau (bài thử `tests/staging/test_03_dung_app.py` quét ảnh thật).
#
#    DOCKER_BUILDKIT=0 docker build -t fls-app:thu <ngữ cảnh>      # ĐÚNG bộ build của Cloud Build `--tag` (⛔ BuildKit)
#    bash tools/staging/thu_dung_anh.sh [--ca <ca.pem>]              # = trên, ngữ cảnh y bước 03, có `mong` (STG-R2b-05)
# ══════════════════════════════════════════════════════════════════════════════════════════
ARG PYTHON_IMAGE=python:3.13-slim
# Cloud SQL Auth Proxy v2 — ghim PHIÊN BẢN (đã kéo thử được 2.15.2); ⛔ `latest`.
ARG PROXY_IMAGE=gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.15.2

FROM ${PROXY_IMAGE} AS proxy

# ── tầng GÓI: cài `psycopg` vào /goi, rồi tầng chạy chỉ CHÉP /goi ─────────────────────────────────────────
# ⭐ `STG-R2b-05` (lỗi THẬT GCP 23/11): bản cũ dùng `RUN --mount=type=secret,id=pipca,…` để đưa CA của proxy
#   máy dev cho `pip` — nhưng `gcloud builds submit --tag` chạy BỘ BUILD CŨ (⛔ BuildKit) ⇒ Cloud Build chết ở
#   Step 9/16 "the --mount option requires BuildKit" (`DOCKER_BUILDKIT=0 docker build` cục bộ tái hiện đúng câu ấy).
#   ⇒ Dockerfile ⛔ còn cú pháp nào đòi BuildKit (bài ghim: `DOCKER_BUILDKIT=0 docker build` phải qua).
#   CA proxy (CHỈ máy dev — Cloud Build ⛔ cần) đi bằng `--build-arg PIP_CA_PEM="$(cat ca.crt)"`: CA là chứng chỉ
#   CÔNG KHAI (⛔ bí mật), và nó chỉ sống ở TẦNG NÀY — tầng chạy ⛔ kế thừa ARG/ENV/tệp của tầng gói
#   ⇒ `docker history` của ảnh cuối ⛔ có nó (bài thử soi).
FROM ${PYTHON_IMAGE} AS goi
ARG PIP_CA_PEM=""
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
# Chỉ gói chạy cần: `psycopg` (⛔ pytest/import-linter — chúng thuộc CI). Lấy dòng từ `requirements.txt` để MỘT nguồn phiên bản.
COPY requirements.txt /tmp/requirements.txt
RUN if [ -n "$PIP_CA_PEM" ]; then printf '%s\n' "$PIP_CA_PEM" > /tmp/pipca.pem; export PIP_CERT=/tmp/pipca.pem; fi; \
    grep -i "^psycopg" /tmp/requirements.txt | xargs pip install --prefix=/goi

# ── tầng CHẠY ─────────────────────────────────────────────────────────────────────────────────────────
FROM ${PYTHON_IMAGE}
ENV PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin fls
WORKDIR /app

COPY --from=goi /goi /usr/local
COPY --from=proxy /cloud-sql-proxy /usr/local/bin/cloud-sql-proxy
COPY fls ./fls
COPY tools ./tools
# `--chown`: `tools/staging/app/chay_chuoi.sh --ghi` (người test bấm "chạy chuỗi") ghi lại `hd2_cong.json` — cửa đọc nó MỖI yêu cầu.
COPY --chown=fls:fls docs/ITL/_tools ./docs/ITL/_tools
# Ảnh đáp án + đầu vào đã đóng băng (đã commit, đã quét PII) — chuỗi HD2 `tools/do_hd2.py` đọc chúng.
COPY tests/fixture ./tests/fixture

USER fls
ENTRYPOINT ["bash", "/app/tools/staging/app/vao.sh"]
