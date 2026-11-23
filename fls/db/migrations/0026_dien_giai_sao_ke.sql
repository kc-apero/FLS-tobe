-- 0026 · `fls_dien_giai` — DIEN GIAI SAO KE, DEN BANG PHEP NOI
--
-- ⭐⭐⭐ `QĐ-ITL-145` · `2026-09-18`. Owner tra loi **"mo"** cho `GAP-NAP-04`.
--
-- ⛔⛔⛔ **VA PHEP DO TRUOC KHI LAM CHO THAY ⛔ KHONG CO GI DE MO.**
--
-- ── BA DIEU DO DUOC ──────────────────────────────────────────────────
--   ⓐ `QĐ-ITL-128` (17/09) **DA** cho doc `Description`, ca `6/6` truong —
--      `sao_ke.TRUONG_DOC_DUOC == SAU_TRUONG`, ban khai da co no.
--   ⓑ Nhung `fls_itl.memo` van **`0 / 8.387`** va `canon[2]` la `None`.
--      ⇒ **Quyet dinh DA DOI, duong ghi O LAI.** Dung lop loi *"tien de doi
--        o cho khac, phat bieu cu o lai"* — lan nay NGUOC chieu: **quyen da
--        mo ma phan thuc thi dung yen**, va ⛔ khong cong nao thay vi mot cot
--        rong ⛔ khong bao loi.
--   ⓒ ⭐ `fls_chup_dong` — **nhip chup moi gio** — DANG giu no:
--        anh `152380` · `8.592` dong · **`8.589`** dong co `Description`.
--
-- ── VI SAO KHUNG XEM, ⛔ KHONG PHAI NAP LAI hay GHI VAO SO ────────────
--
-- ⛔ **Nap lai ⛔ khong giai quyet gi.** `content_key` ⛔ khong chua dien giai,
--    nen mot luot nap lai bi **bo qua vi trung** va `memo` van rong.
-- ⛔ **`UPDATE fls_itl.memo` thi pham `INV-I08`** — so la sach **chi-them**;
--    ca `verify_cua_ghi.py` lan `test_khong_mot_cot_nao_cua_fls_itl_bi_doi`
--    dung ra de chan dung viec do.
--
-- ⭐ Do phep noi TRUOC khi khai (`18/09`, anh `152380`):
--        noi duoc       8.361 / 8.387 = 99,7%
--        co dien giai   8.358 / 8.387 = 99,7%
--     ⭐ tien te KHOP    8.358        ⇒ noi **DUNG DONG**, ⛔ khong lech hang
--
--    ⚠ Phep kiem thu ba ay la cai dat gia nhat: hai bang deu xep theo
--      `dong_so`, nen mot phep noi **lech mot hang** van tra ve `99,7%` va
--      van **trong hoan toan hop ly** — chi co doi chieu mot truong THU BA
--      (`Currency`) moi phan biet duoc.
--
-- ⛔⛔ **VI SAO PHAI CHON ANH CHUP — va vi sao chon THEO TUNG DONG.**
--    `fls_chup_dong` co **29** anh. Noi ma ⛔ khong chon anh thi mot dong so
--    co **N** dien giai va moi phep dem tren no **phong len N lan** — dung cai
--    bay `(run_id, pm_line_id)` da can HAI lan trong ngay `18/09`.
--    ⚠ Va ⛔ **khong** lay `max(chup_id)` toan cuc: anh `152381` co **0 dong**
--      (nhip vua tao). Mot anh rong toan cuc se lam khung xem **rong sach**.
--    ⇒ `LATERAL ... ORDER BY chup_id DESC LIMIT 1` — anh moi nhat **CO dong
--      ay**, xet theo **tung dong**.
--
-- ⚠ Dong ⛔ **khong** co dien giai thi **VANG** khoi khung xem, ⛔ khong tra
--   chuoi rong: mot o rong noi *"giao dich nay khong co noi dung"*, trong khi
--   su that la *"chua doc duoc"*. Hai cau ay KHAC NHAU (`INV-I16`).

CREATE INDEX IF NOT EXISTS fls_chup_dong_noi_idx
  ON fls_chup_dong (source_id, dong_so, chup_id DESC);

CREATE OR REPLACE VIEW fls_dien_giai AS
SELECT i.itl_id,
       btrim(d.o ->> 'Description') AS dien_giai,
       d.chup_id
FROM fls_itl i
JOIN fls_source s ON s.source_key = i.source_sheet
JOIN LATERAL (
  SELECT dd.o, dd.chup_id
    FROM fls_chup_dong dd
   WHERE dd.source_id = s.source_id
     AND dd.dong_so   = i.source_row
   ORDER BY dd.chup_id DESC
   LIMIT 1
) d ON true
WHERE btrim(coalesce(d.o ->> 'Description', '')) <> '';

COMMENT ON VIEW fls_dien_giai IS
  'Dien giai sao ke cua mot dong so, lay tu anh chup MOI NHAT co dong ay. '
  '⛔ KHONG ghi vao `fls_itl` (INV-I08). Dong khong co dien giai thi VANG '
  'khoi day — o rong va "chua doc duoc" la hai chuyen khac nhau.';
