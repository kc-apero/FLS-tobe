-- 0007 · Bang noi mot dong so <-> N dong lenh chi (GAP-JOIN-03).
--
-- Vi sao: phep ghep do duoc 6 hinh dang. `A` (1 bank x 1 PM) va `C` (N bank x
-- 1 PM) moi dong chi tro toi MOT dong lenh nen mot cot du. Hinh `B` (mot lan
-- chuyen tra N dong lenh) thi KHONG — 27 dong hinh `B` truoc day phai vao hang
-- cho KEM LY DO CO TEN thay vi dau duoc.
--
-- ⛔ Cai KHONG lam: tach mot dong bank thanh N dong so (`T-JOIN-03` spec v0.1).
-- Tach nhu the vo the 1-1 giua so va nguon ma ca bon duong doi soat dua vao.
--
-- Buoc 3 CHUYEN 2.650 moi noi dang nam o `fls_itl.pm_line_id` sang bang moi,
-- roi buoc 4 BO cot do — de moi noi chi con MOT cho. Giu ca hai la hai ban su
-- that, dung cai benh khuon `fls/db/` nay dung ra de chua.

CREATE TABLE IF NOT EXISTS fls_pm_link (
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  pm_line_id text NOT NULL,
  amount numeric(20,2) NOT NULL,
  hinh text NOT NULL,
  run_id text NOT NULL REFERENCES fls_run(run_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_pm_link_pk PRIMARY KEY (itl_id, pm_line_id)
);

COMMENT ON COLUMN fls_pm_link.itl_id IS
  'dong so. ⛔ KHONG cascade — so la append-only (INV-I08)';
COMMENT ON COLUMN fls_pm_link.pm_line_id IS
  'fps_pm_line.line_id — dinh danh muc DONG. ⛔ KHONG FK (QĐ-ITL-45)';
COMMENT ON COLUMN fls_pm_link.amount IS
  'PHAN tien cua dong so nay quy cho dong lenh nay. Σ theo itl_id PHAI bang tien dong bank';
COMMENT ON COLUMN fls_pm_link.hinh IS 'A|B|C — ghep BANG CACH NAO';
COMMENT ON COLUMN fls_pm_link.run_id IS 'lan nap sinh ra moi noi (INV-I05 lineage)';

-- Tra nguoc tu dong lenh ve cac dong so: man F01 se can.
CREATE INDEX IF NOT EXISTS fls_pm_link_line_idx ON fls_pm_link (pm_line_id);

-- Chan trung `fls_reject` o TANG KHO (GAP-DB-P0-03).
-- Truoc day rang buoc nay ⛔ khong ton tai: khuon `fls/db/model.py` chua khai
-- duoc khoa NHIEU COT, nen lop chan duy nhat la `WHERE NOT EXISTS` trong cau
-- INSERT. Da hong THAT: mot lan chay lai nhan ban thanh 76 dong cho 19 dong
-- loai that.
ALTER TABLE fls_reject
  ADD CONSTRAINT fls_reject_run_id_source_row_uq UNIQUE (run_id, source_row);

-- Chuyen moi noi cu sang bang moi. Tien = tien cua chinh dong bank do
-- (`ps_no + ps_co`, mot trong hai luon la 0) — dung dinh nghia ma phep ghep
-- dung (`_bank_tu_canon`). Voi hinh `A`/`C` moi dong bank duoc quy TRON VEN cho
-- mot dong lenh, nen Σ theo `itl_id` tu khop.
INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh, run_id)
SELECT itl_id, pm_line_id,
       COALESCE(ps_no, 0) + COALESCE(ps_co, 0),
       COALESCE(pm_hinh, 'A'),
       run_id
FROM fls_itl
WHERE pm_line_id IS NOT NULL
ON CONFLICT DO NOTHING;

ALTER TABLE fls_itl DROP COLUMN IF EXISTS pm_line_id;
