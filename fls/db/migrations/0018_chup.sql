-- 0018 · CHO O CHO VUNG CHUAN (`QĐ-ITL-110` · `BA-07` §4c · `CR#11` task `9`).
--
-- ⛔⛔ **Ba bang nay sinh ra vi mot PHEP DO, ⛔ khong vi mot y tuong.**
--
-- ── Phat hien 2026-09-08 ────────────────────────────────────────────────
--
-- Soi man `F04` xuong bang tuyen THAT (`tools/soi_bang_tuyen.py`, **20**
-- tuyen). Man can **5 cua**, va:
--
--   ⛔ `GET /sources`                — trang thai ①  ⇒ ⛔ KHONG TON TAI
--   ⛔ mot duong doc **vung CHUAN**  — trang thai ②  ⇒ ⛔ KHONG TON TAI
--   ⛔ `GET .../khai-cot`            — trang thai ③  ⇒ chi co `POST`
--   ✅ `POST /nap/xem-truoc`         — trang thai ④
--   ✅ `POST /nap`                   — trang thai ⑤
--
-- ⛔⛔ **Va hai cua CO van ⛔ KHONG CHAY DUOC.** Ca hai doi nguoi goi **dua
--    san `dong`** vao than yeu cau. Ly do viet trong chinh ma nguon:
--    *"doc `.xlsx`/`.csv` la viec cua **man hinh** — no da cam tep trong tay
--    nguoi dung"*. Cau ay dung tren **`QĐ-ITL-105` ⓷** (*duong vao = TAI
--    TEP + khai cot*), thu ma **`QĐ-ITL-109` da LAT**: `F04` ⛔ khong co mot
--    o nhap nao, cu chi `Ctrl+V` **o lai Google Sheets**.
--
-- ⇒ Trinh duyet ⛔ khong doc duoc Sheets; cua thi ⛔ khong tu doc.
--   ⇒ **⛔ KHONG CO duong nao dua du lieu that vao kho.**
--
-- ⚠ Noi thang cho dau: task `4` da duoc khai **XONG** voi cau *"HE CO CUA
--   VAO"* trong khi he ⛔ khong co duong vao nao. Cung lop loi voi viec ban
--   dau cua `§2b` xep `3` truoc `7` (cong cua `3` ⛔ khong chay duoc):
--   **mot task tuyen bo xong tren mot tien de ⛔ chua ai do.**
--
-- ── Vi sao ANH CHUP, va ⛔ KHONG phai vi TOC DO ─────────────────────────
--
-- ⚠⚠ **Lap luan dau tien la SAI — giu lai lam bia.** Toi dan `GAP-API-04`
--    (*"nguon chap chon, timeout 3/3"*) de chong duong doc song. Phep do ay
--    chay tren workbook **`ADJUSTED`** (day `IMPORTRANGE`), ⛔ **khong** tren
--    `R |`. Do chinh `R |` ngay 08/09: **1,8s** liet ke sheet + **2,7s** doc
--    & chuyen = **4,4 giay / 60 sheet / 8.365 dong** — thua suc trong han cho
--    **10s** cua client. ⇒ Mot con so DUNG cua so KHAC dem lam bang chung
--    cho so nay.
--
-- ⭐⭐ **Ly do THAT nam o `BA-07` §4b ⓶:** no hua *"xem truoc cho ra DUNG THU
--    nap se ghi"*. Neu moi cua tu doc Sheets **song** thi hai cua doc sheet o
--    **hai thoi diem khac nhau** ⇒ loi hua **vo trong im lang**, ma nguoi
--    dung tin **cai ho vua nhin thay**. Cung mot `chup_id` thi loi hua ay
--    dung **bang CAU TRUC**, ⛔ khong bang ky luat nguoi viet.
--
-- ⚠ Cong mot rang buoc da do: han muc doc Sheets la **tai nguyen dung CHUNG
--   voi owner dang mo chinh file do** — da an `429` THAT khi goi 60 lot thay
--   vi gop. Mot man doc song moi lan bam la mot man **tieu han muc cua nguoi
--   khac**.
--
-- ── Ba luat cua bang ───────────────────────────────────────────────────
--
--   ⓐ ⛔ CHI-THEM. Chup lai ⇒ **`chup_id` MOI**; anh cu ⛔ khong doi mot o.
--      Cung ky luat `fls_khai_cot` va `fls_pm_line` (`QĐ-ITL-61`).
--
--   ⓑ ⛔ **`o` la `jsonb`, ⛔ KHONG `text`** — va day la lan thu BA cung cai
--      bay. Ep moi o ve chuoi lam se-ri ngay thanh `"45586"`
--      (`QĐ-ITL-102` ⓶) va lam `L6` cua cong #17 do duoc **0 dong** ⇒ do.
--      Anh chup phai giu **KIEU** dung nhu sheet tra ve: so la so, chuoi la
--      chuoi. Va no giu **o NGUYEN VAN TRUOC `chuyen()`** — nho vay
--      `KHUON_RA` / luat `Num` / `GAP-CANON-02` (quy 11 cot) ⛔ khong bi chep
--      thanh ban thu hai o tang kho.
--
--   ⓒ ⛔ **⛔ KHONG luu `so_dong`/`so_nguon` o bang dau.** Ca hai **suy duoc**
--      tu hai bang duoi, va mot cai dau ghi `so_dong = 8365` canh mot bang
--      dong **RONG** la **mot loi noi doi ma ⛔ khong cong nao thay** — dung
--      luat nen *"do duoc 0 thu ⇒ ⛔ KHONG DAT"*. `giay` thi GIU, vi no ⛔
--      khong suy duoc tu dau.
--
-- ⭐⭐ **Vi sao co `fls_chup_nguon` rieng thay vi suy tu `fls_chup_dong`:**
--    mot nguon doc ra **0 dong** thi no **bien mat** khoi bang dong — dung
--    diem mu ma `S8` tung tu lo ra (*"sheet ra 0 dong bien mat khoi chinh
--    phep kiem sinh ra de tim no"*). Bang nay lam no **CO MAT**, kem ca
--    `khai_version` da dung.
--
-- ⛔ `Description` ⛔ **KHONG co mat trong anh chup** (`QĐ-ITL-92`/`107`) —
--   5/6 truong, cuong che o `sao_ke.TRUONG_DOC_DUOC`.

CREATE TABLE IF NOT EXISTS fls_chup (
  chup_id bigint NOT NULL DEFAULT nextval('seq_itl_id') PRIMARY KEY,
  doc_luc timestamptz NOT NULL DEFAULT now(),
  spreadsheet_id text NOT NULL,
  lan text NOT NULL,
  giay numeric(8,2),
  actor text NOT NULL
);

COMMENT ON TABLE fls_chup IS
  'QĐ-ITL-110 — dau ANH CHUP vung CHUAN: mot dong = mot LAN DOC. Chi-THEM';
COMMENT ON COLUMN fls_chup.doc_luc IS
  '★ DAU THOI DIEM. Trang thai ② cua F04 hien con so nay — ⛔ KHONG hien "tuoi": tuoi la mot phep tru, dau thoi diem la mot su that';
COMMENT ON COLUMN fls_chup.spreadsheet_id IS
  'doc workbook NAO — hai lan chup tu hai file la hai thu khac nhau';
COMMENT ON COLUMN fls_chup.lan IS
  'Bank | Cash — hai lan khac khuon RA (GAP-CANON-02: bank 10 cot, quy 11) nen ⛔ khong duoc lan vao nhau';
COMMENT ON COLUMN fls_chup.giay IS
  'phep doc mat bao lau. ⛔ KHONG suy duoc tu dau nen phai luu; do that 08/09: 4,4s cho 60 sheet';
COMMENT ON COLUMN fls_chup.actor IS
  'chup la HANH VI, phai co ten — cung luat fls_khai_cot.actor';

CREATE TABLE IF NOT EXISTS fls_chup_nguon (
  chup_id bigint NOT NULL REFERENCES fls_chup(chup_id),
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  khai_version int NOT NULL,
  PRIMARY KEY (chup_id, source_id)
);

COMMENT ON TABLE fls_chup_nguon IS
  'QĐ-ITL-110 — mot NGUON trong mot lan doc. ⭐ Nho bang nay ma nguon doc ra 0 DONG van CO MAT (diem mu S8). Chi-THEM';
COMMENT ON COLUMN fls_chup_nguon.khai_version IS
  'ban khai DA DUNG de doc nguon nay — ghim ket qua doc_khai(tai=doc_luc) de doi chieu duoc, ⛔ khong de thay no';

CREATE TABLE IF NOT EXISTS fls_chup_dong (
  chup_id bigint NOT NULL REFERENCES fls_chup(chup_id),
  source_id bigint NOT NULL REFERENCES fls_source(source_id),
  dong_so int NOT NULL,
  o jsonb NOT NULL,
  PRIMARY KEY (chup_id, source_id, dong_so)
);

COMMENT ON TABLE fls_chup_dong IS
  'QĐ-ITL-110 — mot dong vung CHUAN, o NGUYEN VAN TRUOC chuyen(). Chi-THEM';
COMMENT ON COLUMN fls_chup_dong.dong_so IS
  'thu tu dong TRONG VUNG DOC (0-based) — de truy nguoc ve sheet';
COMMENT ON COLUMN fls_chup_dong.o IS
  '{ten truong: gia tri NGUYEN VAN}, 5/6 truong (⛔ khong Description). ⛔ KHONG text: ep ve chuoi la dung lai cai bay lam se-ri ngay thanh "45586"';

-- Duong nong: "anh chup nay co nhung dong nao cua nguon nay", theo thu tu.
CREATE INDEX IF NOT EXISTS ix_fls_chup_dong_nguon
  ON fls_chup_dong (chup_id, source_id, dong_so);

-- Duong nong cua trang thai ②: "anh chup moi nhat cua lan nay".
CREATE INDEX IF NOT EXISTS ix_fls_chup_moi
  ON fls_chup (lan, doc_luc DESC);

-- ⭐⭐ `fls_run.chup_id` — NULLABLE **CO CHU DICH**, cung ly do `khai_id` cua
--    migration `0016`: mot lo vao bang duong `dong` (test / phep do doi
--    chung) **PHAI HIEN RA** la `chup_id = NULL`, tuc *"⛔ khong co anh chup
--    nao dung sau no"*. Khai `NOT NULL` la buoc phai **bia** mot anh chup
--    cho moi lo test — tuc lam ban dung cai cot dung ra de noi that
--    (`R-A1`, va cung benh ma `INV-I16` chua: NULL trung thuc hon mot ma bia).
ALTER TABLE fls_run ADD COLUMN IF NOT EXISTS chup_id bigint
  REFERENCES fls_chup(chup_id);

COMMENT ON COLUMN fls_run.chup_id IS
  'QĐ-ITL-110: anh chup vung CHUAN ma lo nay doc. NULL = lo vao bang duong `dong` (test/doi chung), ⛔ KHONG co anh chup dung sau — ⛔ khong bia (R-A1)';
