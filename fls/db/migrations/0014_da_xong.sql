-- 0014 · NGUOI BAM "XONG" moi roi hang cho (`GAP-JOIN-06`, `QĐ-ITL-71`).
--
-- ⛔⛔ **Lo duoc dong o day.** `work_status` bi **DONG BANG luc nap**
-- (`fls/ledger/build.py`) va ⛔ KHONG co gi tinh lai no — moi cua ghi deu
-- ⛔ khong dung vao `fls_itl` (dung `INV-I08`). ⇒ Ke toan chua xong du 5 truong
-- hop dong cua mot dong thi dong ay **VAN nam trong hang cho, mai mai**.
--
-- Do 28/08 tren kho that: **0 dong bi mac** *(vong ghi chua tung chay tren so
-- that)* ⇒ day la **co che thieu, chua phai thiet hai**. Nhung no hien ra
-- **ngay dau tien** ke toan dung man hinh.
--
-- ★★ **Owner chot: NGUOI BAM "XONG"** *(⛔ khong phai may tu nha khi thay du 5
-- truong)*. Can cu la mot cau hoi nghiep vu, ⛔ khong phai mot lua chon ky
-- thuat: may tu nha thi ke toan **mat cho danh dau viec dang lam do**, con
-- nguoi bam thi hang cho dai hon nhung **dung y nguoi**.
--
-- ⇒ Cach lam, va no ⛔ KHONG dong den mot o nao cua `fls_itl`:
--   ⓐ mot **su kien** `done` trong `fls_queue_event` — cung bang da mang
--     `reason`/`defer`, cung mang `actor`/`at`/`reason`
--   ⓑ bam nham thi **`reopen`** — cung la THEM mot su kien, ⛔ khong xoa
--   ⓒ *"dong nay da xong chua"* la mot **PHEP TINH**: su kien MOI NHAT trong
--     hai loai ay. Cung thang thuoc voi `fls_sua_tay` va `fls_moi_noi`.
--
-- ⚠ Va mot dieu phai khai: bam "xong" khi con thieu truong la **NGUOI ghi de
--   len ket luan cua may**. ⛔ Khong chan viec do *(co the la mot khoan phi bank
--   that su khong can 5 truong)*, nhung khi ay **ly do la BAT BUOC** va so
--   dong nhu the duoc **dem rieng** — ⛔ khong de no lot vao im lang.

CREATE OR REPLACE VIEW fls_da_xong AS
SELECT z.itl_id, z.evt_id, z.actor, z.at, z.reason
FROM (SELECT e.itl_id, e.evt_id, e.actor, e.at, e.reason, e.evt_type,
             row_number() OVER (PARTITION BY e.itl_id
                                ORDER BY e.evt_id DESC) AS rn
      FROM fls_queue_event e
      WHERE e.evt_type IN ('done', 'reopen')) z
WHERE z.rn = 1 AND z.evt_type = 'done';

-- Hang cho doc khung xem nay tren MOI luot, nen phep loc phai nhanh.
CREATE INDEX IF NOT EXISTS fls_queue_event_xong_idx
  ON fls_queue_event (itl_id, evt_id DESC)
  WHERE evt_type IN ('done', 'reopen');

COMMENT ON VIEW fls_da_xong IS
  'QĐ-ITL-71: dong da duoc NGUOI bam xong (su kien done/reopen moi nhat). Hang cho tru khung xem nay';
