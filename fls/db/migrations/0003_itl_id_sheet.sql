-- 0003_itl_id_sheet
--
-- Owner chot 2026-08-26 (phien /grill-me): luu `ITL#` cua so cu lam THAM CHIEU.
--
-- Can vi do that tren 9.767 dong: 357 dong (3,7%) TRUNG khoa noi dung
-- (ngay + so chung tu + No + Co + tai khoan) va 105 dong KHONG CO so chung tu.
-- Khong co cot nay thi khi cat sang FLS, 3,7% so KHONG chung minh duoc tung
-- dong da chuyen dung -- chi doi soat duoc TONG.
--
-- ⛔ KHONG phai danh tinh. Ma nay sinh tu ="ITL#"&No voi No=ROW() tren bang da
-- SORT theo ngay, nen chen mot dong lui ngay la doi ma hang loat (INV-I04a).
-- Danh tinh van la itl_id do SEQUENCE cap luc `staged`, dong bang.

ALTER TABLE fls_itl ADD COLUMN IF NOT EXISTS itl_id_sheet text;

COMMENT ON COLUMN fls_itl.itl_id_sheet IS
  'ITL# cua so cu — CHI de doi soat, KHONG phai danh tinh';
