-- 0011 · ANH CHUP dong lenh chi — dong `GAP-API-04` bang duong (a) owner chot.
--
-- ⛔⛔ VI SAO. Bo nap ghep PM doc dong lenh tu Google Sheets **luc chay roi khong
-- luu lai gi**. Sau khi nap, kho biet "dong so nay noi voi dong lenh PM00030-2"
-- nhung ⛔ khong biet **dong lenh do la gi** — nen thao tac GHEP TAY o man `F01`
-- (`QĐ-ITL-48`, viec chinh cua man do) ⛔ khong the co danh sach ung vien.
--
-- Duong (b) — doc Sheets SONG trong mot duong HTTP — bi loai: nguon da do duoc la
-- chap chon (timeout 3/3 lan o tab `IMPORTRANGE`), va mot cua treo vi mang la mot
-- cua ke toan se bo.
--
-- ★ Ba luat chong "hai ban su that", khai o `fls/db/schema.py`:
--   ⓐ day la ANH CHUP CUA MOT LAN NAP (`run_id` trong khoa chinh), ⛔ khong phai
--     danh muc; nap lai la THEM anh chup moi, ⛔ khong sua tai cho.
--   ⓑ cua doc PHAI tra `read_at` cung moi danh sach ung vien — cau tra loi cho
--     "ban luu gia di thi sao" la NOI RA no gia bao nhieu.
--   ⓒ `amount` ⛔ KHONG phai can cu ghi so: luc ghep, Σ so voi tien bank THAT.
--
-- ⛔ KHONG mang PII (Timestamp · Email · Ten tai khoan · So tai khoan · Ghi chu ·
-- Dien giai). Hau qua khai thang: xep ung vien CHI theo ma + tien + tien te, ⛔
-- KHONG theo ngay/payee nhu `BA-07` §2 mong (`GAP-JOIN-04`).

CREATE TABLE IF NOT EXISTS fls_pm_line (
  run_id text NOT NULL REFERENCES fls_run(run_id),
  pm_line_id text NOT NULL,
  pm_slip_id text NOT NULL,
  ref_tho text,
  ref_canon text,
  amount numeric(20,2),
  curr text NOT NULL,
  status text,
  hd text,
  cdt1 text,
  source_row integer NOT NULL,
  read_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_pm_line_pk PRIMARY KEY (run_id, pm_line_id),
  CONSTRAINT fls_pm_line_run_id_source_row_uq UNIQUE (run_id, source_row)
);

-- Tra ung vien theo ma da chuan hoa la duong nong nhat cua man `F01`.
CREATE INDEX IF NOT EXISTS ix_fls_pm_line_ref ON fls_pm_line (ref_canon)
  WHERE ref_canon IS NOT NULL;
-- Xep ung vien theo tien, trong tung tien te (khi ma KHONG khop).
CREATE INDEX IF NOT EXISTS ix_fls_pm_line_tien ON fls_pm_line (curr, amount);
-- Gom dong theo phieu khi hien tren man.
CREATE INDEX IF NOT EXISTS ix_fls_pm_line_slip ON fls_pm_line (pm_slip_id);
