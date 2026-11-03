-- 0010 · Khung xem GIA TRI NGUOI GO dang co hieu luc (`P5` — cua GHI).
--
-- ⛔⛔ Day la cho sua mot lech trong `BA-07` §3. Dac ta viet: *"truong hop-dong
-- cap nhat `*_thyt`"*. Lam the la sai HAI luat cung luc:
--
--   ⓐ `INV-I08` — `fls_itl` la APPEND-ONLY. Mot cau UPDATE len no la mot duong
--     xoa lich su, va trigger `INV-I03` da chan san khi `raw_frozen`.
--   ⓑ `QĐ-ITL-35` — cot `*_thyt` la cho MAY tu bia, va no la cot DO PARITY.
--     Ghi gia tri NGUOI GO vao do la BO BAN TAY VAO CAI THUOC: tu do tro di
--     khong ai phan biet duoc "may suy dung" voi "nguoi da sua".
--
-- ⇒ Gia tri nguoi go song trong `fls_adjustment` (THEM dong), va "gia tri hien
--   tai" la mot PHEP TINH: but toan moi nhat cua tung (dong, truong), tru cac
--   but toan da bi dao.
--
-- ★ Dao but toan cung la THEM dong: mot dong co `reversal_of` tro toi but toan
--   bi huy. ⛔ KHONG `UPDATE state` cua dong cu — doi trang thai tai cho thi so
--   nhat ky khong con la so nhat ky.
--
-- ⚠ Khung xem nay KHONG luu gi va khong lam cham duong ghi. No chi la cach
--   duy nhat tra loi cau "gia tri hien tai cua o nay la gi" ma khong can sua
--   mot o nao trong so.
CREATE OR REPLACE VIEW fls_sua_tay AS
SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.actor, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.actor, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1;

-- Tra "but toan cua dong nay" va "cac ban dao" phai nhanh — man hinh mo drawer
-- la doc ngay.
CREATE INDEX IF NOT EXISTS fls_adjustment_itl_field_idx
  ON fls_adjustment (itl_id, field);
CREATE INDEX IF NOT EXISTS fls_adjustment_reversal_idx
  ON fls_adjustment (reversal_of) WHERE reversal_of IS NOT NULL;
CREATE INDEX IF NOT EXISTS fls_journal_itl_idx ON fls_journal (itl_id);
CREATE INDEX IF NOT EXISTS fls_queue_event_itl_idx ON fls_queue_event (itl_id);
