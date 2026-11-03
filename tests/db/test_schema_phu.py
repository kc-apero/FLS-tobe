from fls.db.schema import CREATE_ORDER, TABLES

MONG_DOI = {"fls_le", "fls_itl", "fls_adjustment", "fls_journal", "fls_run",
            "fls_reject", "fls_mapping_master", "fls_source", "fls_queue_event",
            "fls_queue_state", "fls_queue_reason_weekly"}


def test_du_bang_va_view():
    assert MONG_DOI <= set(TABLES)


def test_journal_du_7_truong_AUD_1():
    cols = {c.name for c in TABLES["fls_journal"].columns}
    assert {"itl_id", "field", "value_before", "value_after",
            "actor", "at", "value_source", "reason"} <= cols


def test_hai_view_co_view_sql():
    for n in ("fls_queue_state", "fls_queue_reason_weekly"):
        assert TABLES[n].kind == "view"
        assert TABLES[n].view_sql.strip(), n


def test_create_order_cha_truoc_con():
    for name in CREATE_ORDER:
        t = TABLES[name]
        if t.kind == "view":
            continue
        for c in t.columns:
            if c.fk:
                parent = c.fk.split(".")[0]
                assert CREATE_ORDER.index(parent) <= CREATE_ORDER.index(name), (
                    f"{name}.{c.name} tro toi {parent} nhung {parent} tao sau")


def test_view_tao_sau_moi_bang():
    ten_view = [n for n in CREATE_ORDER if TABLES[n].kind == "view"]
    ten_bang = [n for n in CREATE_ORDER if TABLES[n].kind == "table"]
    assert max(CREATE_ORDER.index(v) for v in ten_view) > max(
        CREATE_ORDER.index(b) for b in ten_bang)


def test_run_id_co_FK_ve_fls_run():
    """GAP-ERD-P0-01 (owner chot 2026-08-26): go sai run_id phai bi CHAN,
    khong duoc de dong so mat lineage trong im lang (INV-I05)."""
    col = {c.name: c for c in TABLES["fls_itl"].columns}["run_id"]
    assert col.fk == "fls_run.run_id", "run_id phai FK ve fls_run"
    assert col.null is False


def test_fls_run_va_fls_reject_khong_con_la_island():
    """Them FK run_id lam 2 bang nay noi lien fls_itl => bo khoi ERD_ISLANDS."""
    from fls.db.erd_policy import ERD_ISLANDS
    assert "fls_run" not in ERD_ISLANDS
    assert "fls_reject" not in ERD_ISLANDS


def test_create_order_phu_het_TABLES_tru_BOOTSTRAP():
    """Lo im lang: bang co trong TABLES ma khong co trong CREATE_ORDER thi
    KHONG BAO GIO duoc tao, va khong test nao cu bat duoc."""
    from fls.db.schema import BOOTSTRAP
    thieu = set(TABLES) - set(CREATE_ORDER) - BOOTSTRAP
    assert not thieu, f"bang trong TABLES nhung khong ai tao: {sorted(thieu)}"
    du = set(CREATE_ORDER) - set(TABLES)
    assert not du, f"CREATE_ORDER nhac ten khong co trong TABLES: {sorted(du)}"


def test_moi_bang_BOOTSTRAP_phai_co_ly_do():
    from fls.db.schema import BOOTSTRAP
    for n in BOOTSTRAP:
        assert TABLES[n].island_reason.strip(), f"{n} bootstrap nhung khong co ly do"
