-- ══════════════════════════════════════════════════════════════════════════════════════════
--  STAGING bước 02 · phần (a) — CHẠY BẰNG vai quản trị Cloud SQL (`postgres`)
-- ══════════════════════════════════════════════════════════════════════════════════════════
--  Biến psql (truyền `-v`): kho · admin · ghi · doc
--
--  ⭐ Vì sao phải có phần này TRƯỚC khi di trú. `gcloud sql databases create` tạo kho do
--     `postgres` sở hữu; PG15+ đã thu `CREATE` trên schema `public` khỏi PUBLIC ⇒ `fls_admin`
--     (người sẽ chạy `pg_migrate`) ⛔ có quyền tạo bảng, và di trú đỏ ngay `CREATE SEQUENCE`.
--     ⇒ đổi chủ kho sang `fls_admin` *(muốn đổi chủ, người đổi phải là THÀNH VIÊN của vai nhận —
--     PG đòi thế ở vai không-siêu-cấp, Cloud SQL cũng vậy; nên cấp `fls_admin` cho `postgres`)*.
--
--  ⛔ Tệp này ⛔ chạm bảng nào (kho còn có thể rỗng). Chạy lại được: mọi câu đều idempotent.
\set ON_ERROR_STOP on

GRANT :"admin" TO CURRENT_USER;
ALTER DATABASE :"kho" OWNER TO :"admin";

-- Đường vào: PUBLIC ⛔ được nối kho này; chỉ ba vai của ứng dụng.
REVOKE ALL ON DATABASE :"kho" FROM PUBLIC;
GRANT CONNECT ON DATABASE :"kho" TO :"admin", :"ghi", :"doc";

-- ⭐ Đường ĐỌC của cửa API: `tools/chay_cua.py` TỪ CHỐI chạy nếu kết nối còn ghi được
--   (`fls.api.cua.kiem_truoc_khi_mo` → `fls.repo.doc_bao_cao.la_chi_doc` đọc đúng
--   `SHOW default_transaction_read_only`). Đặt MẶC ĐỊNH ở tầng vai ⇒ mọi phiên mới của `fls_doc`
--   đều `on`, ⛔ tin vào kỷ luật của máy khách.
--   ⚠ Đây là MẶC ĐỊNH, ⛔ phải tường thành: một phiên có thể `SET … = off`. Tường thật là
--   `GRANT` — không INSERT/UPDATE/DELETE trên bảng nào (xem `02b_phan_quyen.sql` + BÁO CÁO).
ALTER ROLE :"doc" SET default_transaction_read_only = on;
