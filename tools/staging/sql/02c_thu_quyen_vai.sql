-- ══════════════════════════════════════════════════════════════════════════════════════════
--  STAGING bước 02 · phần (c) — THU MỌI QUYỀN của MỘT vai ứng dụng trước khi `DROP ROLE` nó
--  CHẠY BẰNG vai `fls_admin` (chủ kho + chủ mọi bảng ⇒ là người đã cấp, nên thu được)
-- ══════════════════════════════════════════════════════════════════════════════════════════
--  Biến psql (truyền `-v`): kho · vai
--
--  ⭐ Vì sao có tệp này (`STG-R2b-02`, lỗi THẬT GCP 23/11). Vai `fls_ghi`/`fls_doc` do
--     `gcloud sql users create` tạo mang CREATEROLE + CREATEDB, và `postgres` ⛔ hạ được
--     (`ALTER ROLE … NOSUPERUSER …` bị từ chối). Đường chuyển: thu quyền (tệp này) → `DROP ROLE`
--     → tạo lại bằng SQL (`CREATE ROLE … NOCREATEDB NOCREATEROLE`) → `02a` + `02b` cấp lại.
--     `DROP ROLE` ⛔ chạy được khi vai còn được cấp quyền trên bất kỳ đối tượng nào
--     ("role … cannot be dropped because some objects depend on it") ⇒ phải thu SẠCH trước.
--
--  Chạy lại được: thu quyền ⛔ có ⇒ PG chỉ cảnh báo. ⛔ chạm DỮ LIỆU nào.
\set ON_ERROR_STOP on

REVOKE ALL ON ALL TABLES    IN SCHEMA public FROM :"vai";
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM :"vai";
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM :"vai";
REVOKE ALL ON SCHEMA public FROM :"vai";
REVOKE ALL ON DATABASE :"kho" FROM :"vai";
