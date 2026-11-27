"""AC-6 · BỘ ĐỘT BIẾN SQL GHI — mỗi câu phải bị chặn ở CẢ HAI lớp, đo RIÊNG từng lớp.

  lớp 1 (ứng dụng) — `chan_sql.kiem` ⇒ `SqlBiChan`.
  lớp 2 (kho)      — `cong_cu.chay_doc` chạy câu TRẦN *(⛔ qua lớp 1)* bằng vai đọc của bài
                     (`GRANT SELECT` + `default_transaction_read_only`) ⇒ `LoiCongCu("KHO_TU_CHOI")`
                     HOẶC (riêng `set_config(... , false)`) tác dụng ⛔ sống qua ROLLBACK.
  hậu kiểm         — sau cả bộ: số dòng `fls_run`/`fls_itl` của lần nạp mẫu ⛔ đổi, bảng vẫn còn.

⭐ `Đ5` — hai bài cuối PHÁ từng lớp ngay trong bài (lớp 1: rỗng danh sách cấm; lớp 2: bỏ `READ ONLY` + dùng
vai CHỦ bảng) và đòi bộ đột biến LỌT ⇒ chứng minh hai bài trên ĐỎ khi lớp tương ứng hỏng.
"""
from __future__ import annotations

import pytest

from fls.mcp import chan_sql
from fls.mcp.cong_cu import LoiCongCu, chay_doc

pytestmark = pytest.mark.pg

# (tên, câu, sqlstate/lời PG mong ở lớp 2 — chuỗi con của chi tiết lỗi)
DOT_BIEN = [
    ("INSERT", "insert into fls_run (run_id, contract_version, canon_version, mapping_version)"
               " values ('NAP-DOT-BIEN','v','v','v')", "25006"),
    ("UPDATE", "update fls_itl set ps_no = 0", "25006"),
    ("DELETE", "delete from fls_itl", "25006"),
    ("DROP", "drop table fls_itl", "25006"),
    ("TRUNCATE", "truncate fls_run cascade", "25006"),
    ("ALTER", "alter table fls_itl add column x int", "25006"),
    ("CREATE", "create table mcp_dot_bien (x int)", "25006"),
    ("GRANT", "grant select on fls_itl to public", "25006"),
    ("COPY_FROM", "copy fls_run from stdin", "42501"),
    ("COPY_TO_TEP", "copy fls_run to '/tmp/fls_mcp_dot_bien'", "42501"),
    ("COPY_TO_STDOUT", "copy fls_run to stdout", "ProgrammingError"),
    ("HAI_CAU", "select 1; delete from fls_itl", "42601"),
    ("HAI_CAU_CHU_THICH", "select 1 /**/; DELETE FROM fls_run", "42601"),
    ("CTE_DML", "with x as (delete from fls_itl returning 1) select * from x", "25006"),
    ("SELECT_INTO", "select * into mcp_dot_bien from fls_run", "25006"),
    ("SET_CONFIG_RO", "select set_config('transaction_read_only','off',true)", "25001"),
    ("SET_CONFIG_PHIEN", "select set_config('default_transaction_read_only','off',false)", None),
    ("SET", "set default_transaction_read_only = off", None),
    ("PG_SLEEP", "select pg_sleep(5)", "57014"),
]
HAN_MS = 1_000


def _dem(conn, run):
    return (conn.execute("select count(*) from fls_run where run_id=%s", (run,)).fetchone()[0],
            conn.execute("select count(*) from fls_itl where run_id=%s", (run,)).fetchone()[0])


@pytest.mark.parametrize("ten,sql,_m", DOT_BIEN, ids=[d[0] for d in DOT_BIEN])
def test_lop1_ung_dung_CHAN(ten, sql, _m):
    with pytest.raises(chan_sql.SqlBiChan):
        chan_sql.kiem(sql)


@pytest.mark.parametrize("ten,sql,mong", DOT_BIEN, ids=[d[0] for d in DOT_BIEN])
def test_lop2_kho_CHAN_khi_lop1_vang(kho_mcp, ten, sql, mong):
    from tests.mcp.conftest import mo_doc_vai
    with mo_doc_vai(kho_mcp["dsn_doc"])() as conn:
        if mong is None:
            # ⛔ PG cho chạy, nhưng tác dụng phải CHẾT cùng giao dịch: ROLLBACK hoàn tác GUC.
            try:
                chay_doc(conn, sql, 10, HAN_MS)
            except LoiCongCu:
                pass                                          # bị từ chối hẳn — càng tốt
            assert conn.execute("show default_transaction_read_only").fetchone()[0] == "on"
            with pytest.raises(LoiCongCu) as e:               # và phiên vẫn CHẶN ghi
                chay_doc(conn, "insert into fls_run (run_id) values ('X')", 1, HAN_MS)
            assert "25006" in e.value.chi_tiet
            return
        with pytest.raises(LoiCongCu) as e:
            chay_doc(conn, sql, 10, HAN_MS)
    assert e.value.ma == "KHO_TU_CHOI" and mong in e.value.chi_tiet, e.value.chi_tiet


def test_hau_kiem_kho_KHONG_DOI_sau_ca_bo(kho_mcp):
    import psycopg
    from tests.mcp.conftest import mo_doc_vai
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        truoc = _dem(c, kho_mcp["run"])
        assert truoc == (1, 3), truoc                     # mẫu số ⛔ rỗng (`Đ3`)
    for _t, sql, _m in DOT_BIEN:
        with mo_doc_vai(kho_mcp["dsn_doc"])() as conn:
            try:
                chay_doc(conn, sql, 10, HAN_MS)
            except LoiCongCu:
                pass
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        assert _dem(c, kho_mcp["run"]) == truoc
        assert c.execute("select to_regclass('mcp_dot_bien')").fetchone()[0] is None


def test_dem_bo_dot_bien():
    """`Đ5` mong: 19 đột biến (9 mục bắt buộc của WO-371 AC-6 + 10 biến thể)."""
    assert len(DOT_BIEN) == 19
    bat_buoc = {"INSERT", "UPDATE", "DELETE", "DROP", "COPY_FROM", "HAI_CAU", "CTE_DML", "SET_CONFIG_RO", "PG_SLEEP"}
    assert bat_buoc <= {d[0] for d in DOT_BIEN}


# ── `Đ5`: chứng minh hai bài trên CẮN khi lớp tương ứng hỏng ──────────────────────────────────────────
def test_PHA_lop1_thi_dot_bien_LOT(monkeypatch):
    monkeypatch.setattr(chan_sql, "TU_CAM", frozenset())
    monkeypatch.setattr(chan_sql, "_HAM_CAM", __import__("re").compile(r"(?!x)x"))
    monkeypatch.setattr(chan_sql, "_KHOA_DONG", __import__("re").compile(r"(?!x)x"))
    lot = []
    for t, sql, _m in DOT_BIEN:
        try:
            chan_sql.kiem(sql)
            lot.append(t)
        except chan_sql.SqlBiChan:
            pass
    # Còn chặn khi đã phá: câu ⛔ bắt đầu bằng SELECT/WITH (12) + nhiều câu (2) ⇒ LỌT đúng 5 — tức bài
    # `test_lop1_ung_dung_CHAN` ĐỎ 5 ô khi danh sách cấm bị rỗng.
    assert sorted(lot) == ["CTE_DML", "PG_SLEEP", "SELECT_INTO", "SET_CONFIG_PHIEN", "SET_CONFIG_RO"], lot


class _BoReadOnly:
    """Kết nối bọc: đổi `BEGIN TRANSACTION READ ONLY` ⇒ `BEGIN` (PHÁ lớp 2)."""

    def __init__(self, c):
        self.c = c

    def execute(self, sql, *a, **k):
        return self.c.execute("BEGIN" if sql.startswith("BEGIN TRANSACTION READ ONLY") else sql, *a, **k)

    def cursor(self):
        return self.c.cursor()


def test_PHA_lop2_thi_dot_bien_LOT(kho_mcp):
    """Vai CHỦ bảng (`fls`) + giao dịch ĐỌC-GHI ⇒ DELETE/CTE_DML CHẠY (rồi ROLLBACK) ⇒ bài lớp 2 sẽ ĐỎ."""
    import psycopg
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        truoc = _dem(c, kho_mcp["run"])
        r = chay_doc(_BoReadOnly(c), "with x as (delete from fls_pm_line where run_id = '"
                     + kho_mcp["run"] + "' returning 1) select count(*) from x", 1, HAN_MS)
        assert r["dong"] == [[2]]                        # LỌT: 2 dòng bị xoá trong giao dịch
        assert _dem(c, kho_mcp["run"]) == truoc          # … và ROLLBACK của `chay_doc` trả lại


_RO = [(t, s) for t, s, m in DOT_BIEN if m == "25006"]


@pytest.mark.parametrize("ten,sql", _RO, ids=[t for t, _ in _RO])
def test_lop2_READ_ONLY_TU_DUNG_VUNG_ca_khi_vai_GHI_duoc(kho_mcp, ten, sql):
    """⛔ dựa vào vai: vai CHỦ bảng + `default_transaction_read_only = off` — chỉ còn `BEGIN … READ ONLY` của
    `chay_doc` chặn. (Đo 27/11 — Đ5 D2: thiếu bài này, bỏ `READ ONLY` khỏi `chay_doc` vẫn 42/42 XANH vì vai
    `fls_doc` tự chặn ⇒ lớp giao dịch ⛔ được canh riêng.)"""
    import psycopg
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        c.execute("SET default_transaction_read_only = off")
        with pytest.raises(LoiCongCu) as e:
            chay_doc(c, sql, 10, HAN_MS)
        assert "25006" in e.value.chi_tiet, e.value.chi_tiet
        assert _dem(c, kho_mcp["run"]) == (1, 3)
