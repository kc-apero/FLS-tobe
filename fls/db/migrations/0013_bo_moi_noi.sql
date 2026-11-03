-- 0013 · DUONG BO MOI NOI (`GAP-JOIN-05`) — va cai lo no lam lo ra.
--
-- ⛔⛔ **Vi sao phai co.** Tu 27/08 ke toan ghep duoc tien voi dong lenh
-- (`ghep_lenh`, `QĐ-ITL-48`) nhung ⛔ KHONG co duong nao GO mot moi noi ghep
-- sai. Chinh `ghep_lenh` phai NO ra cau do: *"muon ghep lai thi phai bo moi
-- noi cu, va ⛔ chua co duong nao lam viec do (`GAP-JOIN-05`)"*. ⇒ Mot dong
-- ghep sai la mot dong **chet cung**: ⛔ khong go, ⛔ khong ghep lai.
--
-- ★ **Bo mot moi noi cung la THEM mot dong** (`INV-I08`, luat ⓐ cua
--   `fls/repo/ghi_tay.py`): ⛔ khong `DELETE`, ⛔ khong `UPDATE`. Cung thuoc
--   thang voi `fls_adjustment` -> `fls_sua_tay`: **gia tri hien tai la mot
--   PHEP TINH**, ⛔ khong phai mot o bi ghi de.
--
-- ⇒ Ba viec o day:
--
--   ⓐ `fls_pm_link` co **danh tinh RIENG** (`link_id`) + so **`lan`**.
--      ⛔ Vi sao phai doi khoa: khoa cu la `(itl_id, pm_line_id)`, tuc mot dong
--      so noi voi mot dong lenh **nhieu nhat MOT lan trong DOI**. Voi khoa do
--      thi *"bo roi ghep lai dung dong lenh ay"* — ca ly do chinh de bo — bi kho
--      CHAN bang mot loi trung khoa. ⇒ khoa chinh la `link_id`, va khoa duy
--      nhat la `(itl_id, pm_line_id, lan)`: **mot LAN ghep** la duy nhat, con
--      ghep lai la `lan = 2`.
--
--   ⓑ Bang `fls_pm_unlink` — mot dong cho MOI moi noi bi bo. Bang nay ⛔ khong
--      chua `actor`/`reason`: ai bo va vi sao song o `fls_queue_event`
--      (`evt_type='unmatch'`), va **mot cho** thi ⛔ khong lech duoc.
--
--   ⓒ Khung xem `fls_moi_noi` = moi noi **DANG CO HIEU LUC**. Tu day moi cho
--      DOC phai doc khung xem nay; `fls_pm_link` chi con la **lich su**.
--
-- ⭐ Va them mot cot nho ma phep bo BUOC phai co: `fls_adjustment.evt_id` —
--   *but toan nay sinh ra boi THAO TAC nao*. Phep ghep tu suy `hd`/`cdt1` tu
--   dong lenh; bo moi noi thi **can cu cua phep suy ay mat**, nen phai dao
--   dung nhung but toan do. ⛔ Khong co cot nay thi cach duy nhat de nhan ra
--   chung la **doi chuoi `reason`** — mot phep nhan dang vo tay lam vo.
--   ⚠ Cot nay chi ghi luc `INSERT`, ⛔ khong bao gio `UPDATE`.

-- ── ⓐ danh tinh rieng cho moi noi ────────────────────────────────────────
ALTER TABLE fls_pm_link ADD COLUMN IF NOT EXISTS link_id bigint;
UPDATE fls_pm_link SET link_id = nextval('seq_itl_id') WHERE link_id IS NULL;
ALTER TABLE fls_pm_link ALTER COLUMN link_id SET NOT NULL;
ALTER TABLE fls_pm_link ALTER COLUMN link_id SET DEFAULT nextval('seq_itl_id');

ALTER TABLE fls_pm_link ADD COLUMN IF NOT EXISTS lan smallint NOT NULL DEFAULT 1;

ALTER TABLE fls_pm_link DROP CONSTRAINT IF EXISTS fls_pm_link_pk;
ALTER TABLE fls_pm_link ADD CONSTRAINT fls_pm_link_pk PRIMARY KEY (link_id);
ALTER TABLE fls_pm_link DROP CONSTRAINT IF EXISTS fls_pm_link_lan_uq;
ALTER TABLE fls_pm_link ADD CONSTRAINT fls_pm_link_lan_uq
  UNIQUE (itl_id, pm_line_id, lan);

COMMENT ON COLUMN fls_pm_link.link_id IS
  'danh tinh cua MOT LAN ghep. Co no thi bo duoc mot moi noi ma khong xoa dong nao';
COMMENT ON COLUMN fls_pm_link.lan IS
  'lan ghep thu may cua cap (dong so, dong lenh). Bo roi ghep lai => lan+1';

-- ── ⓑ so ghi cac lan BO moi noi ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fls_pm_unlink (
  unlink_id bigint NOT NULL DEFAULT nextval('seq_itl_id'),
  link_id bigint NOT NULL REFERENCES fls_pm_link(link_id),
  itl_id bigint NOT NULL REFERENCES fls_itl(itl_id),
  evt_id bigint NOT NULL REFERENCES fls_queue_event(evt_id),
  at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT fls_pm_unlink_pk PRIMARY KEY (unlink_id),
  CONSTRAINT fls_pm_unlink_link_uq UNIQUE (link_id)
);

COMMENT ON COLUMN fls_pm_unlink.link_id IS
  'moi noi bi bo. UNIQUE: mot moi noi chi bo duoc MOT lan (bo hai lan la mot lo dem)';
COMMENT ON COLUMN fls_pm_unlink.evt_id IS
  'thao tac bo (fls_queue_event evt_type=unmatch) — AI bo va VI SAO song o do, MOT cho';

CREATE INDEX IF NOT EXISTS fls_pm_unlink_itl_idx ON fls_pm_unlink (itl_id);

-- ── ⓒ but toan sinh ra boi thao tac nao ──────────────────────────────────
ALTER TABLE fls_adjustment ADD COLUMN IF NOT EXISTS evt_id bigint
  REFERENCES fls_queue_event(evt_id);
COMMENT ON COLUMN fls_adjustment.evt_id IS
  'thao tac sinh ra but toan nay (vd phep ghep suy hd/cdt1). Chi ghi luc INSERT, ⛔ KHONG UPDATE';
CREATE INDEX IF NOT EXISTS fls_adjustment_evt_idx
  ON fls_adjustment (evt_id) WHERE evt_id IS NOT NULL;

-- ── ⓓ moi noi DANG CO HIEU LUC ───────────────────────────────────────────
CREATE OR REPLACE VIEW fls_moi_noi AS
SELECT l.link_id, l.itl_id, l.pm_line_id, l.amount, l.hinh, l.lan, l.run_id,
       l.created_at
FROM fls_pm_link l
WHERE NOT EXISTS (SELECT 1 FROM fls_pm_unlink u WHERE u.link_id = l.link_id);
