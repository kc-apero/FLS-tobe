-- ══════════════════════════════════════════════════════════════════════════════════════════
--  STAGING bước 02 · phần (b) — CHẠY BẰNG `fls_admin` (chủ kho), SAU `pg_migrate`
-- ══════════════════════════════════════════════════════════════════════════════════════════
--  Biến psql (truyền `-v`): ghi · doc · so (= `fls_itl`) · so_di_tru (= `fls_migration`)
--
--  ⭐ NGUYÊN TẮC: **không cấp thừa rồi thu lại** cho cả kho — cấp từng nhóm, nhóm chỉ-THÊM thu
--  riêng. Và ⛔ KHÔNG `ALTER DEFAULT PRIVILEGES`: bảng mới do di trú sau thêm vào sẽ ⛔ thấy với
--  `fls_ghi`/`fls_doc` cho tới khi chạy LẠI bước 02 — vỡ về phía AN TOÀN, và BÁO CÁO báo ĐỎ
--  ngay (“bảng thiếu quyền ≠ 0”) thay vì để một bảng append-only mới được cấp UPDATE trong im lặng.
--
--  Chạy lại được (GRANT/REVOKE idempotent).
\set ON_ERROR_STOP on

-- ── 0 · gỡ sạch quyền cũ của hai vai ứng dụng rồi cấp lại — để chạy-lại ⇒ quyền = ĐÚNG khai báo,
--        ⛔ cộng dồn với một lần chạy sai trước đó (vd ai đó từng `GRANT UPDATE ON fls_itl`).
REVOKE ALL ON ALL TABLES    IN SCHEMA public FROM PUBLIC, :"ghi", :"doc";
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC, :"ghi", :"doc";
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO :"ghi", :"doc";

-- ── 1 · fls_doc — chỉ ĐỌC: SELECT trên mọi bảng/view/sequence (view nằm trong "ALL TABLES")
GRANT SELECT ON ALL TABLES    IN SCHEMA public TO :"doc";
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO :"doc";

-- ── 2 · fls_ghi — đường GHI của ứng dụng
--   2a · DML trên mọi bảng/view …
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO :"ghi";
--   2b · … TRỪ sổ `fls_itl`: CHỈ-THÊM (`INV-I08`; trigger `INV-I03` chặn thêm một lớp ở dòng đã
--        `raw_frozen`). Thu UPDATE/DELETE ở tầng QUYỀN: một câu UPDATE lạc vào bị từ chối TRƯỚC
--        khi trigger kịp xét. (⛔ TRUNCATE: `GRANT … ALL` không cấp nó, nhưng thu cho rõ.)
REVOKE UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON TABLE :"so" FROM :"ghi";
--   2c · … và sổ di trú `fls_migration`: ứng dụng ⛔ có lý do sửa lịch sử di trú ⇒ chỉ ĐỌC.
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLE :"so_di_tru" FROM :"ghi";
--   2d · sequence (cấp `itl_id`…): dùng được
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO :"ghi";
