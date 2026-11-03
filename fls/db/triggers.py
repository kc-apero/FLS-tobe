"""Cuong che bat bien o tang DB. Doc: 04_DB_IMPLEMENTATION §5."""

from __future__ import annotations

TRIGGER_DDL: tuple[str, ...] = (
    # INV-I03: raw_frozen la diem khong quay lui
    """
CREATE OR REPLACE FUNCTION fls_chan_sua_dong_dong_bang() RETURNS trigger AS $$
BEGIN
  IF OLD.raw_frozen THEN
    RAISE EXCEPTION 'INV-I03: itl_id % da raw_frozen, sua chi bang but toan moi', OLD.itl_id;
  END IF;
  IF TG_OP = 'DELETE' THEN
    RETURN OLD;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;""",
    """
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i03 ON fls_itl;""",
    """
CREATE TRIGGER trg_fls_itl_inv_i03 BEFORE UPDATE OR DELETE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_sua_dong_dong_bang();""",
    # INV-I04a: danh tinh dong bang
    """
CREATE OR REPLACE FUNCTION fls_chan_doi_itl_id() RETURNS trigger AS $$
BEGIN
  IF NEW.itl_id <> OLD.itl_id THEN
    RAISE EXCEPTION 'INV-I04a: itl_id dong bang, khong duoc doi (% -> %)',
      OLD.itl_id, NEW.itl_id;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;""",
    """
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i04a ON fls_itl;""",
    """
CREATE TRIGGER trg_fls_itl_inv_i04a BEFORE UPDATE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_doi_itl_id();""",
)
