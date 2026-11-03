-- 0021 · `fls_pm_line.tho` — GIU LAI DONG THO cua lan `PM`
--
-- ⛔⛔⛔ **Vi sao co migration nay, va no sua mot BAT DOI XUNG co that.**
--
-- Do 2026-09-11:
--     lan `Bank` : 14 anh · 65 nguon · 7.454.400 dong tho trong `fls_chup_dong`
--     lan `PM`   : 14 anh ·  1 nguon ·         0 dong tho
--
-- `chay_nap.nap_anh_pm` khai thang dieu do: *"⛔ khong mot dong nao vao
-- `fls_chup_dong`: `fls_pm_line` CHINH LA bang dong cua lan nay"*. Khai ay
-- **dung ve thiet ke** — nhung no keo theo mot he qua ⛔ khong ai noi ra:
-- `fls_pm_line` chi giu **8 truong da phan tich**, nen **20 cot con lai cua
-- `PM_Unpivot` bien mat ngay luc doc**, va them mot cot ve sau thi
-- ⛔ **khong bu nguoc duoc** cho 3.772 dong dang co — phai doi cu chup ke tiep.
--
-- ⇒ Owner chot 11/09: **CO LUU dong tho**. Cot nay giu **ca hang** duoi dang
--   `{ten cot: gia tri}` — khoa theo **TEN**, ⛔ khong theo vi tri: cot xe dich
--   thi ban khai vi tri lech, con ten thi ⛔ khong.
--
-- ★ Tu day, them mot truong hien thi = **doc lai `tho`**, ⛔ khong phai chup lai.
--
-- ⚠ `NULL` duoc, va no co nghia THAT: *"anh nay chup TRUOC 11/09"*. ⛔ Dung
--   `DEFAULT '{}'` — mot dau ngoac rong trong nhu *"doc duoc 0 cot"*, va hai
--   chuyen ay khac nhau (`INV-I16`).
ALTER TABLE fls_pm_line ADD COLUMN IF NOT EXISTS tho jsonb;

COMMENT ON COLUMN fls_pm_line.tho IS
  'Ca hang tho cua PM_Unpivot, khoa theo TEN COT. NULL = anh chup truoc '
  '2026-09-11. ⛔ KHONG chua cot `Email Address` (xem PM_COT_RIENG_TU).';
