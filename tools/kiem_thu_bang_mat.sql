-- =====================================================================
-- KIEM CHUNG BANG MAT — doc nguoc tu SO ve TO GIAY
--
--   docker exec -i -e PGPASSWORD=fls fls-pg-1 \
--     psql -U fls -d fls_test -f /dev/stdin < tools/kiem_thu_bang_mat.sql
--
-- ⛔ Doi `fls_test` -> `fls` de soi kho THAT (tep nay CHI DOC, ⛔ khong ghi gi).
-- ⛔ Doi `:RUN` cho khop lo ban muon soi.
--
-- ⚠⚠ HAI CAI BAY DA DO DUOC 17/09 — doc truoc khi tu viet cau hoi:
--
--   ⓐ **LECH MOT DONG.** `fls_chup_dong.dong_so` la **0-based** (0..112),
--      con `fls_itl.source_row` / `fls_reject.source_row` la **1-based**
--      (1..113). ⇒ Noi hai bang PHAI la `d.dong_so = i.source_row - 1`.
--      Noi thang `=` van chay, van tra ve du dong, va **moi dong deu la o
--      BEN CANH** — tien khop nhau tung phan nen mat thuong ⛔ khong thay.
--
--   ⓑ **`fls_run.row_count` ⛔ KHONG phai "so dong DOC VAO".** `dong_run()`
--      ghi de no bang `count(*) FROM fls_itl` luc chot ⇒ no la **so dong DA
--      VAO SO**. Phep can bon duong *(`vao = so + loai + rong + trung`)*
--      ⛔ **khong suy lai duoc tu SQL** — no song trong bien ban ma cua
--      `POST /nap/lo` tra ve. SQL chi kiem duoc `so + loai` vs **anh chup**.
-- =====================================================================
\set RUN 'NAP-2026-09-17-KIEMTHU100'
\pset pager off

\echo '=== [1] CAN LO: anh chup  vs  (vao so + bi loai) ====================='
-- ⭐ Phep kiem quan trong nhat co the lam BANG SQL. Lech = dong bien mat.
WITH nguon AS (
  SELECT DISTINCT i.source_sheet AS k FROM fls_itl i WHERE i.run_id = :'RUN'
  UNION
  SELECT DISTINCT j.source_sheet FROM fls_reject j WHERE j.run_id = :'RUN'
), anh AS (
  SELECT count(*) n FROM fls_chup_dong d
  JOIN fls_source s USING (source_id)
  WHERE d.chup_id = (SELECT chup_id FROM fls_run WHERE run_id = :'RUN')
    AND s.source_key IN (SELECT k FROM nguon)
)
SELECT (SELECT n FROM anh)                                          AS anh_chup,
       (SELECT count(*) FROM fls_itl    WHERE run_id = :'RUN')      AS vao_so,
       (SELECT count(*) FROM fls_reject WHERE run_id = :'RUN')      AS bi_loai,
       (SELECT n FROM anh)
         - (SELECT count(*) FROM fls_itl    WHERE run_id = :'RUN')
         - (SELECT count(*) FROM fls_reject WHERE run_id = :'RUN')  AS lech,
       (SELECT state FROM fls_run WHERE run_id = :'RUN')            AS trang_thai;

\echo ''
\echo '=== [2] 10 DONG SO — doi chieu voi sao ke bang MAT ===================='
-- `source_sheet` + `source_row` = dia chi tren to giay. Mo sheet, nhay toi dong.
SELECT itl_id, doc_date AS ngay, doc_no AS so_ct, curr,
       ps_no AS no_, ps_co AS co_, work_status AS trang_thai,
       source_row AS dong_tren_sheet
FROM fls_itl WHERE run_id = :'RUN'
ORDER BY doc_date DESC, itl_id DESC LIMIT 10;

\echo ''
\echo '=== [3] TONG TIEN theo don vi — so voi so du sao ke =================='
SELECT curr, count(*) AS so_dong,
       sum(ps_no) AS tong_no, sum(ps_co) AS tong_co,
       sum(ps_co) - sum(ps_no) AS rong,
       min(doc_date) AS tu_ngay, max(doc_date) AS den_ngay
FROM fls_itl WHERE run_id = :'RUN' GROUP BY curr ORDER BY curr;

\echo ''
\echo '=== [4] DONG BI LOAI — vi sao, va O NAO tren sheet ==================='
-- ⭐ ⛔ KHONG dong nao bien mat khong dau vet. Moi dong loai mang MOT LY DO.
SELECT source_row AS dong_tren_sheet, left(reason, 95) AS ly_do
FROM fls_reject WHERE run_id = :'RUN' ORDER BY source_row LIMIT 10;

\echo ''
\echo '=== [5] GOM LY DO LOAI — mot lo hong, hay nhieu lo? =================='
SELECT count(*) AS so_dong, left(split_part(reason, ':', 1), 40) AS nhom_ly_do
FROM fls_reject WHERE run_id = :'RUN' GROUP BY 2 ORDER BY 1 DESC;

\echo ''
\echo '=== [6] TRUY NGUOC: dong so  ->  O NGUYEN VAN tren to giay ==========='
-- ⭐⭐ Phep chung minh LINEAGE manh nhat: canh nhau la gia tri engine ghi
--     va gia tri THO truoc khi engine cham vao.
-- ⚠ `- 1` la bay ⓐ o dau tep. ⛔ Bo no di thi moi dong lech sang o BEN CANH.
SELECT i.itl_id, i.doc_date AS engine_doc_ngay,
       d.o->>'Date'   AS tho_ngay,
       i.ps_no, i.ps_co,
       d.o->>'Debit'  AS tho_no,
       d.o->>'Credit' AS tho_co,
       i.source_row
FROM fls_itl i
JOIN fls_run  r ON r.run_id = i.run_id
JOIN fls_source s ON s.source_key = i.source_sheet
JOIN fls_chup_dong d ON d.chup_id  = r.chup_id
                    AND d.source_id = s.source_id
                    AND d.dong_so   = i.source_row - 1   -- ⚠ bay ⓐ
WHERE i.run_id = :'RUN'
ORDER BY i.source_row LIMIT 5;

\echo ''
\echo '=== [7] DONG BI LOAI cung truy nguoc duoc ==========================='
SELECT j.source_row, d.o->>'Date' AS tho_ngay, d.o->>'Credit' AS tho_co,
       left(j.reason, 60) AS ly_do
FROM fls_reject j
JOIN fls_run  r ON r.run_id = j.run_id
JOIN fls_source s ON s.source_key = j.source_sheet
JOIN fls_chup_dong d ON d.chup_id  = r.chup_id
                    AND d.source_id = s.source_id
                    AND d.dong_so   = j.source_row - 1   -- ⚠ bay ⓐ
WHERE j.run_id = :'RUN' ORDER BY j.source_row LIMIT 5;

\echo ''
\echo '=== [8] BAN KHAI: engine doc COT NAO, doc NGAY THE NAO =============='
-- `cot` = cot nao (0-based) · `thu_tu` = `dmy` hay `mdy`.
-- ⛔ `thu_tu` RONG nghia la *nguon CHUA KHAI*, ⛔ KHONG phai "coi nhu dmy".
--   Do la ly do 35 dong o tren bi loai: ngay '07/02/2026' co the la 7 thang 2
--   hoac 2 thang 7, va engine TU CHOI DOAN.
SELECT s.source_key, k.truong, k.cot, k.thu_tu, k.version
FROM fls_khai_cot k JOIN fls_source s USING (source_id)
WHERE s.source_key IN (SELECT DISTINCT source_sheet FROM fls_itl
                       WHERE run_id = :'RUN')
ORDER BY k.truong;

\echo ''
\echo '=== [9] ANH LENH CHI (PM) — ung vien de ghep ========================'
SELECT run_id, count(*) AS so_dong, count(DISTINCT pm_slip_id) AS so_phieu,
       count(pe_line) AS co_cha_PE, count(pi_line) AS co_cha_PI,
       max(read_at) AS anh_doc_luc
FROM fls_pm_line GROUP BY run_id ORDER BY max(read_at) DESC LIMIT 3;

\echo ''
\echo '=== [10] MOI NOI tien <-> lenh chi ================================='
-- ⚠ `POST /nap/lo` ghep PM khi duoc truyen anh PM; `0` mối noi nghia la
--   lo nay nap KHONG kem anh lenh chi — ⛔ khong phai "ghep that bai".
SELECT coalesce(n.hinh, '(chua ghep)') AS hinh,
       count(*) AS so_dong, sum(n.amount) AS tong_tien
FROM fls_itl i LEFT JOIN fls_moi_noi n USING (itl_id)
WHERE i.run_id = :'RUN' GROUP BY 1;

\echo ''
\echo '=== [11] BAT BIEN: so la CHI-THEM =================================='
-- `raw_frozen = true` ⇒ trigger cam `UPDATE`/`DELETE`. Thu sua thi NO.
SELECT raw_frozen, period_state, count(*) FROM fls_itl
WHERE run_id = :'RUN' GROUP BY 1, 2;
