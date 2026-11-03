-- 0012 · BO 5 cot vung ALLOCATE khoi `fls_itl` — owner chot 2026-08-28
-- (`QĐ-ITL-65`, sau `QĐ-ITL-64`).
--
-- ⛔⛔ VI SAO BO, va vi sao bo la dung chu khong phai tiec. Owner dua NGUYEN VAN
-- ba cong thuc cua vung ALLOCATE tren `ITL Ledge`:
--
--     AU  =ArrayFormula(AD7:AD)
--     AV  =ArrayFormula(if(VLOOKUP(V7:V,{MM!H:H,MM!K:K},2,FALSE)
--                          ="Need to Allocate to CFA2",
--                          "Need to Allocate to CFA2", AU7:AU))
--     AW  =ArrayFormula(if(VLOOKUP(V7:V,{MM!H:H,MM!L:L},2,FALSE)<>"",
--                          VLOOKUP(V7:V,{MM!H:H,MM!L:L},2,FALSE), "No need"))
--
-- ⇒ Ca ba o la CONG THUC, va chung SUY LAI DUOC 100% tu:
--       `cdt1` (=AD) + `hd` (=V) + `fls_mapping_master.need_cfa2 / method_cfa2`
--   Phep suy da ma hoa: `fls/ledger/allocate.py` (+9 phep thu).
--   ⇒ Quyet dinh phan bo ⛔ KHONG nam o dong so — no nam o **Mapping Master**.
--
-- ⇒ Va owner chot 2026-08-28 (`QĐ-ITL-64`): ke toan **⛔ KHONG sua** vung nay
--   (*"ho ko sua, chi sua cac truong da liet ke truoc do"*). Nen:
--     · `cdt1_cfa1` la BAN SAO cua `cdt1`             ⇒ HAI BAN SU THAT
--     · `cdt1_cfa2` va `alloc_method` suy lai duoc    ⇒ HAI BAN SU THAT
--     · `cdt1_cfa2_classify` / `alloc_method_classify` la **anh chup goi y luc
--       NGUOI ghi de** — ma nay ⛔ khong ai ghi de ⇒ chung ⛔ khong con nghia gi
--
-- ★ Luat cua du an: cai gi suy lai duoc thi ⛔ KHONG luu. Giu lai la de mot cot
--   thu hai canh mot con so, roi mot ngay hai cot noi hai chuyen khac nhau ma
--   ⛔ khong cong nao bat — dung benh `=L130` cua so P100.
--
-- ⛔ MAT GI. ⛔ Khong mat gi do duoc: ca 5 cot deu **0 dong co gia tri** tren kho
-- that (do 2026-08-28), vi bo nap chi doc `Transaction Mapping L1` con vung
-- ALLOCATE nam o so ADJUSTED. Tuc day la bo mot cot RONG, ⛔ khong phai bo du
-- lieu. Va con so ay se **hien lai** o man hinh khi `fls_mapping_master` co bo
-- nap — luc do no la mot **phep tinh**, ⛔ khong phai mot cot.
--
-- ⚠ Chieu nguoc lai (rollback): xem `0001_baseline.sql` de biet dinh nghia cu.
-- ⛔ Nhung ⛔ dung khoi phuc chung ma khong mo lai `QĐ-ITL-64`/`QĐ-ITL-65`.

ALTER TABLE fls_itl
    DROP COLUMN IF EXISTS cdt1_cfa1,
    DROP COLUMN IF EXISTS cdt1_cfa2,
    DROP COLUMN IF EXISTS cdt1_cfa2_classify,
    DROP COLUMN IF EXISTS alloc_method,
    DROP COLUMN IF EXISTS alloc_method_classify;
