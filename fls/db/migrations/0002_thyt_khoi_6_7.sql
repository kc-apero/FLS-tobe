-- 0002_thyt_khoi_6_7
--
-- LO 2026-08-26. Co che "cho noi that" (QD-ITL-35) ap cho CA BAY khoi cua
-- `ITL Ledge`, va `final_rule.BAY_KHOI` da tinh ra `id_payee_thyt` /
-- `invoice_thyt` tu P1. Nhung schema chi co 5 cot `_thyt` (khoi 1-5), va
-- `repo._COT` cung bo sot ca `id_payee`/`invoice` — hai cot DB DA CO SAN.
--
-- => Bon gia tri lop so tinh ra ROI IM LANG o tang ghi. Khong loi, khong canh
--    bao: `_gia_tri` chi kiem khoa THIEU, khong kiem khoa THUA.
--
-- Phat hien khi owner hoi: "cac entity/table nay da co du schema nhu ggsheet
-- chua?" — cau hoi do sinh ra `fls/oracle/ledge_spec.py` (khai 64 cot sheet ->
-- di dau) va cong `tests/oracle/test_ledge_schema.py`.
--
-- Them cot => khong khoa bang, khong can backfill: gia tri cu dung la NULL,
-- va NULL o cot `_thyt` nghia la "may tu bia" — dung nghia can co cho du lieu
-- nap truoc lan sua nay.

ALTER TABLE fls_itl ADD COLUMN IF NOT EXISTS id_payee_thyt text;
ALTER TABLE fls_itl ADD COLUMN IF NOT EXISTS invoice_thyt  text;

COMMENT ON COLUMN fls_itl.id_payee_thyt IS
  'NULL o cho may tu bia (mac dinh VD0). KHONG vao parity';
COMMENT ON COLUMN fls_itl.invoice_thyt IS
  'NULL o cho may tu bia (mac dinh ''No hoa don''). KHONG vao parity';
