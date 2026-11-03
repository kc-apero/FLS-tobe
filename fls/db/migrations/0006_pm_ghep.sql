-- 0006_pm_ghep
--
-- Moi noi bank <-> lenh chi PM chua co CHO DAU. `fls/ledger/build.py` khai
-- `_PM_LINE = 13` tu P1 kem ghi chu *"lineage phai song sot (QD-ITL-20/CR#1)"*
-- — roi **khong ai dung**. Mot hang so treo la mot loi hua chua tra.
--
-- ⓵ `pm_line_id` — dinh danh muc DONG cua lenh chi.
--    ⛔ KHONG dung cot "ID PMLine" go tay trong sheet (day `#N/A`).
--    ⛔ KHONG co FK: `fps_*` la he KHAC va FLS chi DOC no (QD-ITL-45). Khai
--       tuong minh la dao (ERD_ISLANDS) kem ly do, khong de FK gia.
--
-- ⓶ `pm_hinh` — GHEP BANG CACH NAO. Mot chu: A/B/C.
--    ★ Vi sao phai luu cach ghep chu khong chi luu ket qua: ba hinh co do tin
--      khac nhau va cach doi soat khac nhau —
--        A  1 bank × 1 PM        2.256 dong
--        B  1 bank × N PM        27 dong   (mot lan chuyen tra nhieu dong lenh)
--        C  N bank × 1 PM        394 dong  (mot dong lenh tra nhieu lan)
--      Khong luu thi ve sau khong ai tra loi duoc *"dong nay ghep kieu gi"*, va
--      moi phep doi soat tong deu phai doan lai.
--
-- ⚠ Ca hai de NULL: 6.637/9.973 dong khong ghep duoc (khong co ma, khong thay
--   ma PM, hoac tien khong khop). NULL o day la **cau tra loi**, khong phai
--   thieu du lieu — va `work_status='UNMAPPED'` la cho noi that di kem.

ALTER TABLE fls_itl ADD COLUMN IF NOT EXISTS pm_line_id text;
ALTER TABLE fls_itl ADD COLUMN IF NOT EXISTS pm_hinh    text;

COMMENT ON COLUMN fls_itl.pm_line_id IS
  'fps_pm_line.line_id — dinh danh muc DONG. KHONG FK: fps_* la he khac, FLS chi doc';
COMMENT ON COLUMN fls_itl.pm_hinh IS
  'ghep bang cach nao: A 1x1 · B 1 bank x N PM (chia tien) · C N bank x 1 PM (tra nhieu lan)';
