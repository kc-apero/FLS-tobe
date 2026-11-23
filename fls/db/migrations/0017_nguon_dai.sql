-- 0017 · CHO O CHO BAN KHAI THU HAI (`GAP-KHAI-01` · luat soat `S10`).
--
-- ⛔⛔ **He co HAI ban khai cho CUNG MOT phep anh xa, va den 08/09 ⛔ KHONG
--    cong nao so hai cai.**
--
-- ── Phat hien 2026-09-08 ────────────────────────────────────────────────
--
-- Do song ca 68 sheet `R |` + hai bang danh muc:
--
--   ⓐ **Ban khai DONG 1** cua moi sheet — `1`=Date … `6`=Reference number.
--      **FLS doc cai nay** (`fls_khai_cot`, 422 dong).
--
--   ⓑ **`Range_Condition` / `Range_Debit` / `Range_Credit`** o
--      `BankAccountList` / `Cash Ledger List` — vi du `!L3:L` · `!M3:M` ·
--      `!N3:N`, tro dung `Date`/`Debit`/`Credit` cua sheet ay.
--      **Script `Run` cua trang tinh doc cai nay.**
--
-- ⇒ Quet `fls/` `tools/` `tests/` ngay 08/09: **0 tham chieu `Range_`**. Tuc
--   ban khai ma **chinh cai may dang chay** dung thi FLS **chua tung doc**.
--
-- ⭐ Do tay cung ngay: **192 phep so, 0 lech** — hai ban khai dang tro CUNG
--   mot cot. Nhung do la **mot lan chay tay**, ⛔ khong phai mot cong.
--
-- ── Vi sao no nguy, va nguy mot cach IM LANG ───────────────────────────
--
-- Sua dong 1 ma quen danh muc *(hoac nguoc lai)* thi FLS va trang tinh
-- **doc hai cot khac nhau**, va **ca hai deu chay binh thuong**:
--   · ⛔ khong cau lenh nao loi,
--   · ⛔ khong dong nao rot — `S1` van can,
--   · so tong van **trong hop ly**.
-- Cai lech chi lo ra khi co nguoi **doi chieu tung dong** voi sao ke goc.
--
-- ⇒ Day la lop khuyet tat ma **⛔ khong phep kiem nao tren MOT phia bat
--   duoc**. Phai co ca hai phia trong kho thi moi so duoc — do la viec cua
--   bang nay.
--
-- ── Ba luat ────────────────────────────────────────────────────────────
--
--   ⓐ ⛔ CHI-THEM. Danh muc doi ⇒ **them mot dong moi**, ⛔ khong sua dong cu.
--      Cung ky luat `fls_khai_cot`: mot lan nap thang truoc phai giai thich
--      duoc bang **cai da doc luc ay**.
--   ⓑ ⛔ Giu ca `dai_tho` (nguyen van `!L3:L`) LAN `cot` (so 11). Chi giu so
--      thi mat kha nang doi chieu voi mat nguoi; chi giu chuoi thi moi lan so
--      lai phai bóc lai — va **phep boc la cho de lech**.
--   ⓒ ⛔ `dai_tho` co the la mot dai **⛔ khong suy ra duoc mot cot** *(vi du
--      o RONG — do duoc 6 o nhu the o `R | CNC` va `R | Pingpong`)*. Luc ay
--      `cot` = `NULL`, va `S10` phai bao **⛔ KHONG DO DUOC**, ⛔ khong bao
--      "khop". Xanh tren tap rong la **chua do**.

CREATE TABLE IF NOT EXISTS fls_nguon_dai (
  dai_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  truong text NOT NULL,
  cot int,
  dai_tho text NOT NULL,
  danh_muc text NOT NULL,
  doc_luc timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE fls_nguon_dai IS
  'GAP-KHAI-01 — ban khai THU HAI: Range_Condition/Debit/Credit cua danh muc, thu ma script `Run` thuc su doc. Chi-THEM';
COMMENT ON COLUMN fls_nguon_dai.truong IS
  'Date | Debit | Credit — ba truong danh muc khai (⛔ khong phu du 6)';
COMMENT ON COLUMN fls_nguon_dai.cot IS
  'chi so cot 0-based suy tu `dai_tho`. NULL = ⛔ KHONG suy duoc (o rong, hoac dai nhieu cot) — S10 phai bao CHUA DO';
COMMENT ON COLUMN fls_nguon_dai.dai_tho IS
  'nguyen van o danh muc, vi du `!L3:L` — giu de doi chieu duoc bang mat nguoi';
COMMENT ON COLUMN fls_nguon_dai.danh_muc IS
  'BankAccountList | Cash Ledger List — doc tu bang nao';

-- Duong nong: "dai nao dang hieu luc cho nguon nay".
CREATE INDEX IF NOT EXISTS ix_fls_nguon_dai_nguon
  ON fls_nguon_dai (source_id, truong, doc_luc DESC);
