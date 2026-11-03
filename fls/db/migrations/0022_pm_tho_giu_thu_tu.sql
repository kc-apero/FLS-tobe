-- 0022 · `fls_pm_line.tho` : `jsonb` → `json` — GIU THU TU COT CUA GGSHEET
--
-- ⛔⛔⛔ **Vi sao doi kieu, va vi sao `jsonb` la lua chon SAI o day.**
--
-- `jsonb` **⛔ khong giu thu tu khoa** — no chuan hoa va sap lai *(theo do dai
-- roi byte)*. `loc_tho()` dung `dict` theo **dung thu tu cot cua to giay**,
-- nhung thu tu ay **chet ngay khi ghi xuong** `jsonb`.
--
-- Owner 11/09: *"sap xep thu tu cot giong trong GGSheet"*. ⇒ Voi mot cot ma
-- **toan bo cong dung la HIEN RA CHO NGUOI DOC**, thu tu **la mot phan cua du
-- lieu**, ⛔ khong phai chi tiet trinh bay: ke toan doc `PM_Unpivot` hang ngay
-- va tri nho vi tri cua ho la mot cong cu that.
--
-- ★ `json` giu **nguyen van** van ban, ke ca thu tu khoa.
--
-- ⚠ **Cai gia, khai ra chu ⛔ khong giau:** `json` ⛔ **khong** co toan tu
--   `?` / `@>` va ⛔ **khong** danh chi muc `GIN` duoc. Quet ma nguon 11/09:
--   **0** cau trong `fls/` dung toan tu `jsonb` tren cot nay — no chi duoc
--   `SELECT` nguyen cuc roi day ra man hinh. Neu mot ngay nao do can TRA theo
--   noi dung ben trong, hay doi lai `jsonb` **va** luu thu tu cot o mot cho
--   khac, ⛔ dung vua doi kieu vua hy vong thu tu con.
--
-- ⛔ `USING tho::text::json` — di qua `text` la CO Y: `jsonb::json` chi doi
--   nhan kieu tren mot gia tri **da bi sap lai**, tuc thu tu **da mat roi**.
--   Di qua `text` cung ⛔ khong cuu duoc thu tu cu *(no mat luc GHI)*, nhung
--   no lam ro rang la: **phai CHUP LAI** thi thu tu moi dung.
ALTER TABLE fls_pm_line
  ALTER COLUMN tho TYPE json USING tho::text::json;

COMMENT ON COLUMN fls_pm_line.tho IS
  'Ca hang tho cua PM_Unpivot, khoa theo TEN COT va GIU DUNG THU TU COT cua '
  'to giay (kieu `json`, ⛔ KHONG `jsonb` — `jsonb` sap lai khoa). NULL = anh '
  'chup truoc 2026-09-11. ⛔ KHONG chua `Email Address`.';
