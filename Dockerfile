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
#    docker build -t fls-app:thu .
# ══════════════════════════════════════════════════════════════════════════════════════════
ARG PYTHON_IMAGE=python:3.13-slim
# Cloud SQL Auth Proxy v2 — ghim PHIÊN BẢN (đã kéo thử được 2.15.2); ⛔ `latest`.
ARG PROXY_IMAGE=gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.15.2

FROM ${PROXY_IMAGE} AS proxy

FROM ${PYTHON_IMAGE}
ENV PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin fls
WORKDIR /app

# Chỉ gói chạy cần: `psycopg` (⛔ pytest/import-linter — chúng thuộc CI). Lấy dòng từ `requirements.txt`
# để MỘT nguồn phiên bản.
COPY requirements.txt /tmp/requirements.txt
#   `pipca` = bí mật BuildKit TUỲ CHỌN (`docker build --secret id=pipca,src=<ca.crt>`): chỉ cần khi mạng build đi qua
#   một proxy tự ký (vd môi trường cloud của dev). ⛔ nằm trong ảnh — mount tạm lúc `pip`, rồi mất.
RUN --mount=type=secret,id=pipca,required=false \
    sh -c 'if [ -f /run/secrets/pipca ]; then export PIP_CERT=/run/secrets/pipca; fi; \
           grep -i "^psycopg" /tmp/requirements.txt | xargs pip install' \
 && rm /tmp/requirements.txt

COPY --from=proxy /cloud-sql-proxy /usr/local/bin/cloud-sql-proxy
COPY fls ./fls
COPY tools ./tools
COPY docs/ITL/_tools ./docs/ITL/_tools
# Ảnh đáp án + đầu vào đã đóng băng (đã commit, đã quét PII) — chuỗi HD2 `tools/do_hd2.py` đọc chúng.
COPY tests/fixture ./tests/fixture

USER fls
ENTRYPOINT ["bash", "/app/tools/staging/app/vao.sh"]
