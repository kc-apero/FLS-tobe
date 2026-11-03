-- 0019 · THU TU NGAY do NGUON khai (`QĐ-ITL-113` · `BA-07` §4d · `GAP-NAP-02`).
--
-- ⛔⛔ **Mot cot, vi mot phep do — ⛔ khong vi mot y tuong.**
--
-- ── Phep do 2026-09-08, tren anh chup THAT `chup_id 23719` (8.368 dong) ──
--
--   o `Date` la SO (seri Google, ⛔ khong mo ho) : 4.175
--   o `Date` la CHUOI                           : 4.193
--   ⛔ MO HO (ca hai phan <= 12)                 : ⛔ 1.894 dong = **22,6%**
--   ⇒ trai tren                                  : ⛔ **29/60 nguon**
--
-- ⇒ `GAP-NAP-02` ghi *"lo that gan nhu chac chan co ngay mo ho"* — do that ra
--   ⛔ khong phai *"gan nhu"* ma la **phan lon cua lo**.
--
-- ── ⭐⭐⭐ VA PHEP DO LAT DUNG CAI MAC DINH MA AI CUNG SE CHON ────────────
--
--   Nguon suy duoc thu tu tu CHINH NO (co >=1 dong phan nao > 12) : 29/29
--   ⛔ Nguon MAU THUAN (co ca bang chung `dmy` lan `mdy`)          : ⛔ 0
--   Nguon chac chan **`dmy`** (ngay/thang — kieu VN)               : ⛔⛔ 0
--   Nguon chac chan **`mdy`** (thang/ngay)                         : ⭐ 29/29
--   Nguon tron ca ngay-so lan ngay-chuoi (⇒ luat `S6` dung)        : ⛔ 0/50
--
-- ⇒ ⭐⭐ **Mot mac dinh `dmy` "vi day la Viet Nam" se HOAN ngay<->thang tren
--   1.894 dong** — dung lop loi `QĐ-ITL-17` (**93%** dong tung bi hoan,
--   **~181 ty** sai ky). Cac nguon ay la **OCBC Singapore** va **TCB USD**:
--   sao ke nuoc ngoai, `mm/dd/yyyy` la **DUNG**.
--
-- ⭐ Va mot nguon DOC LAP xac nhan: `tools/dung_lai_bank_transactions.py:50`
--   ghi *"chuoi o day la `mm/dd/yyyy` — doc duoc tu chinh `Bank
--   Transactions`"*. Hai phep do doc lap, cung ket luan.
--
-- ── Vi sao o `fls_khai_cot` chu ⛔ khong mot bang moi ───────────────────
--
-- `fls_khai_cot` da la **MOT DONG MOI TRUONG**: khoa `(source_id, version,
-- truong)`, va `cot` tra loi *"doc cot nao"*. `thu_tu` tra loi *"doc THE
-- NAO"* — **cung ban chat**, cung mot truong, va duoc **`version` +
-- `actor`** mien phi (chi-them, truy vet duoc ai khai luc nao).
--
-- ⭐ No cung bien nhan xet cua `GAP-CHUP-04` tu *"sai mo hinh"* thanh *"mo
--   hinh per-field la DUNG"*.
--
-- ⛔⛔ `CHECK` la bat buoc, ⛔ khong phai trang tri: mot `thu_tu` dat tren
--    dong `Debit` ⛔ khong co nghia gi, va mot cot nullable ⛔ khong ai canh
--    thi som muon co nguoi ghi vao do. `CHECK` khien cai vo nghia thanh **⛔
--    KHONG GHI DUOC**.
--
-- ⛔ ⛔ **`NULL` ⛔ KHONG co nghia "coi nhu `dmy`"** — no co nghia *"nguon nay
--    ⛔ chua khai"*, va luc ay ngay mo ho **van bi loai** kem ly do. Quyen an
--    dinh ky ke toan **o NGUOI** (`QĐ-ITL-113`): may **de xuat kem bang
--    chung**, ke toan **bam khai**.

ALTER TABLE fls_khai_cot
    ADD COLUMN IF NOT EXISTS thu_tu text;

-- ⛔ Hai rang buoc, va chung do HAI thu khac nhau:
--   ⓐ chi `Date` moi duoc mang `thu_tu`;
--   ⓑ gia tri chi duoc la `dmy` hoac `mdy` — ⛔ khong `DMY`, ⛔ khong `d/m/y`.
--     Mot cot text tu do la mot cot se co **ba cach viet cho mot y**.
ALTER TABLE fls_khai_cot
    DROP CONSTRAINT IF EXISTS fls_khai_cot_thu_tu_ck;
ALTER TABLE fls_khai_cot
    ADD CONSTRAINT fls_khai_cot_thu_tu_ck CHECK (
        thu_tu IS NULL
        OR (truong = 'Date' AND thu_tu IN ('dmy', 'mdy'))
    );
