-- 0023 · `fls_pm_line` : BAY KHOA `PE`/`PI` LEN KIEU
--
-- ⭐⭐⭐ Owner chot 2026-09-17: *"PE/PI cot CO KIEU trong `fls_pm_line`,
-- chua can lam bang rieng"*.
--
-- ⛔⛔ **DUONG VAO ≠ THUC THE.** Ca ba di nho MOT duong nap (`PM_Unpivot`)
-- — do la cau tra loi `Q2` cua owner cho cau *"PE/PI nap thang hay di
-- nho"*. ⛔ Nhung `PE` · `PI` · `PM` la **ba thuc the khac nhau**, va
-- truoc hom nay bay khoa noi chung lai voi nhau chi song trong cot `tho`
-- (JSON): kho **CO du lieu ma ⛔ KHONG co kieu** ⇒ ⛔ khong tra duoc,
-- ⛔ khong noi duoc, ⛔ khong canh duoc.
--
-- ── DO TRUOC KHI KHAI (26.404 dong co `tho`, 2026-09-17) ─────────────────
--     PE slip+line di CAP      3.500 · lech 0
--     PI slip+line di CAP     22.904 · lech 0
--     Advance 3.381 + Urgent 119 = 3.500 · trung 0 · sot 0
--     mot dong co DUNG MOT cha        · ngoai le 0
--
-- ⛔⛔⛔ **BA BAT BIEN AY CO Y ⛔ KHONG THANH `CHECK` — tru `pe_loai`.**
--
-- `chay_nap.chen_anh_pm` chen **ca lan nap trong MOT giao dich**, va chinh
-- ham do da ghi ly do: *"nem loi la huy ca lan nap chi vi mot dong lenh
-- thieu ma"*. ⇒ Mot `CHECK` tren khoa `PE`/`PI` bien **mot dong la** thanh
-- **do ca luot nap**: no ⛔ khong bao tin, no chan cua. Ba bat bien ay
-- duoc **DEM va NEU TEN** luc nap (`INV-I16`) va co bai ghim do tren kho.
--
-- ★ Rieng `pe_loai` thi an toan lam `CHECK`: gia tri ay do **MA CUA TA**
--   sinh ra tu viec cot nao co chu (`(Advance)` / `(Urgent)`), ⛔ khong
--   phai mot o nguon chep thang ⇒ nguon ⛔ khong the lam no vo.
--
-- ⚠ **NAP BU tu `tho`, ⛔ khong doi cu chup ke tiep.** 26.404/79.212 dong
--   dang co `tho`; 52.808 dong con lai nap TRUOC 11/09 nen ⛔ khong co
--   `tho` va se giu `NULL` — do la **su that**, ⛔ khong phai thieu sot:
--   chung duoc doc bang mot ban khai cot chi co 8 vi tri.
--
-- ⛔ `UPDATE` o day ⛔ KHONG pham `INV-I08`: `INV-I08` la luat cua `fls_itl`
--   (so cai). `fls_pm_line` la **ANH CHUP theo `run_id`** — va phep nap bu
--   nay ⛔ khong doi mot gia tri nao da co, no chi **do day cot vua sinh**.

ALTER TABLE fls_pm_line
  ADD COLUMN pe_slip text,
  ADD COLUMN pe_line text,
  ADD COLUMN pe_loai text,
  ADD COLUMN pi_slip text,
  ADD COLUMN pi_line text;

COMMENT ON COLUMN fls_pm_line.pe_slip IS
  '''ID PESlip''. Do 17/09: 3.500/26.404 dong';
COMMENT ON COLUMN fls_pm_line.pe_line IS
  '''ID PELine''. Di CAP voi pe_slip — do 26.404 dong: 0 lech';
COMMENT ON COLUMN fls_pm_line.pe_loai IS
  'MA SINH RA tu hai cot nguon rieng: (Advance) 3.381 · (Urgent) 119 = 3.500, trung 0';
COMMENT ON COLUMN fls_pm_line.pi_slip IS
  '''ID PISlip''. Do 17/09: 22.904/26.404 dong';
COMMENT ON COLUMN fls_pm_line.pi_line IS
  '''ID PILine''. Mot dong co DUNG MOT cha: PI 22.904 · PE 3.500 · ca hai 0 · khong cha 0';

-- ⭐ Nap bu tu `tho`. ⛔ `nullif(btrim(...), '')` — chuoi rong la KHONG BIET,
--   ⛔ khong phai mot gia tri (`INV-I16`); de nguyen '' thi moi phep dem sau
--   nay deu sai mot cach im lang.
UPDATE fls_pm_line SET
  pe_slip = nullif(btrim(tho->>'ID PESlip'), ''),
  pe_line = nullif(btrim(tho->>'ID PELine'), ''),
  pi_slip = nullif(btrim(tho->>'ID PISlip'), ''),
  pi_line = nullif(btrim(tho->>'ID PILine'), ''),
  pe_loai = CASE
    WHEN nullif(btrim(tho->>'ID PELine - Nội dung PE (Advance)'), '') IS NOT NULL
      THEN 'Advance'
    WHEN nullif(btrim(tho->>'ID PELine - Nội dung PE (Urgent)'), '') IS NOT NULL
      THEN 'Urgent'
    END
WHERE tho IS NOT NULL;

-- ⛔ Rang buoc DUY NHAT cua nhom nay, va no phai CO TEN: `pg_verify` doi
--   chieu **theo ten**, nen mot rang buoc Postgres tu dat ten la mot rang
--   buoc ⛔ khong cong nao goi dung duoc.
ALTER TABLE fls_pm_line
  ADD CONSTRAINT fls_pm_line_pe_loai_ck
  CHECK (pe_loai IS NULL OR (pe_line IS NOT NULL
                             AND pe_loai IN ('Advance', 'Urgent')));

-- ⭐ Chi muc cho hai khoa se duoc TRA thuong xuyen (man ghep tra nguoc tu
--   mot dong lenh ve PE/PI). ⛔ Khong danh chi muc cho `pe_slip`/`pi_slip`:
--   chung chi de GOM khi hien, ⛔ khong phai truc tra — cung ly le da ghi
--   cho `pm_slip_id`.
CREATE INDEX IF NOT EXISTS ix_pm_line_pe_line ON fls_pm_line (pe_line)
  WHERE pe_line IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_pm_line_pi_line ON fls_pm_line (pi_line)
  WHERE pi_line IS NOT NULL;
