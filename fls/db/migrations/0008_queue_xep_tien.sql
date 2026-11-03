-- 0008 · Khung xem xep hang cho theo TIEN (QĐ-ITL-58) — THAY cho phep dan nhan.
--
-- Owner chot 27/08: **BO HAN** trang thai "khong can lenh chi". Moi dong thieu
-- lenh chi deu la `chua biet`. Ly do: `QĐ-ITL-56` — **khong co quy dinh nao**
-- noi khoan nao can lenh chi, nen may dan nhan do la **may tu dat ra quy dinh**
-- (`INV-I16`).
--
-- Van de van that: hang cho 7.682 dong voi 2-3 ke toan. Giai ⛔ khong can quy
-- dinh nao: xep theo TIEN. Khung xem nay ⛔ khong noi dong nao "khong can lenh",
-- no chi noi XEM CAI NAY TRUOC.
--
-- ⛔⛔ PARTITION BY curr — cho de sai nhat. Cong hai so khac don vi tien te ra
-- mot con so TRONG HINH MA VO NGHIA. Do that: hang cho co USD 4.492 dong va VND
-- 2.987 dong; xep theo tong GOP thi VND at het (872 ty vs 302 trieu USD chua doi
-- ty gia) va TOAN BO 4.492 dong USD bi dim xuong duoi — mot khoan 300.000 USD
-- xep sau mot khoan 400.000 dong.
CREATE OR REPLACE VIEW fls_queue_xep_tien AS
SELECT q.itl_id, q.doc_date, q.doc_no, q.curr, q.tien,
       row_number() OVER (PARTITION BY q.curr ORDER BY q.tien DESC, q.itl_id)
         AS hang,
       round(100.0 * SUM(q.tien) OVER (PARTITION BY q.curr
                                       ORDER BY q.tien DESC, q.itl_id
                                       ROWS UNBOUNDED PRECEDING)
             / NULLIF(SUM(q.tien) OVER (PARTITION BY q.curr), 0), 2)
         AS luy_ke_pct
FROM (SELECT itl_id, doc_date, doc_no, curr,
             COALESCE(ps_no, 0) + COALESCE(ps_co, 0) AS tien
      FROM fls_itl
      WHERE work_status = 'UNMAPPED') q;
