# -*- coding: utf-8 -*-
"""`WO-051` `AC-4` — sửa tốc độ `doc_hang_cho` mà **kết quả ⛔ đổi một byte**
*(kho TEST)*.

⛔⛔ Rủi ro 1 của phiếu: viết lại câu có **cửa sổ** + `LEFT JOIN` dễ lệch
**một** hàng ở **mép trang** *(cùng lớp `do_phu` ⓐ/ⓑ "lệch đúng một dòng")*.
⇒ So **toàn bộ** danh sách, ⛔ mẫu:

  · **oracle độc lập con trỏ** = câu `_SQL_HANG_CHO` **của mã khi nhận**
    *(`9af99c4`, chép nguyên văn ở `tools/do_trang_hang_cho._ORACLE` — ⛔
    import từ mã mới)*, ⛔ con trỏ, ⛔ `LIMIT` ⇒ danh sách đầy đủ;
  · nối **mọi** trang của `doc_hang_cho` *(mã mới)* với nhiều cỡ trang
    *(`1` · `7` · `50` — `7` rơi mép trang giữa nhóm tiền **bằng nhau**)*;
  · so **từng hàng, mọi cột** *(`itl_id, hang, luy_ke_pct, reason,
    defer_until, defer_count` + cột còn lại)*, cả `next_cursor`.

Ca *(một lần nạp riêng ⇒ `mot_lan_nap(run)`, ⛔ nhiễu từ ca khác)*: ba tiền
tệ **37 · 12 · 1** dòng; **9** dòng cùng **một** số tiền *(thứ tự phải đi theo
`itl_id`)*; dòng có **lý do** *(2 lần — lần sau thắng)*, dòng **hoãn** *(2 lần
⇒ `defer_count=2`)*, một dòng **đã xong** *(phải RỜI hàng chờ, ⛔ đẩy `%`)*.

⛔ Chiều ĐỎ *(chứng ở `BG-064`)*: phá mã mới — bỏ `ORDER BY` trong `trang`
hay nối `fls_queue_state` bằng `JOIN` thường ⇒ bài **ĐỎ**.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import doc_bao_cao as bc
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import mot_lan_nap
from tools.do_trang_hang_cho import oracle_hang_cho

pytestmark = pytest.mark.pg

ACTOR = "ke-toan@apero.vn"


def _hex(n: int = 6) -> str:
    return uuid.uuid4().hex[:n].upper()


def _dong(cur, run: str, curr: str, tien: str) -> int:
    cur.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, curr, ps_co, work_status, doc_date, doc_no)"
        " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,'UNMAPPED','2026-08-01',%s) RETURNING itl_id",
        (uuid.uuid4().hex, run, curr, D(tien), f"CT{_hex()}"))
    return cur.fetchone()[0]


@pytest.fixture(scope="module")
def ca():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        run = "NAP-2000-01-01-W51" + _hex()
        c.execute("INSERT INTO fls_run (run_id, contract_version,"
                  " canon_version, mapping_version)"
                  " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        te = {"A": "A" + _hex(4), "B": "B" + _hex(4), "C": "C" + _hex(4)}
        ids: dict[str, list[int]] = {k: [] for k in te}
        with c.cursor() as cur:
            for j in range(37):
                # 9 dòng đầu CÙNG tiền ⇒ hạng đi theo `itl_id`
                tien = "5000" if j < 9 else str(100 + 37 * j % 991)
                ids["A"].append(_dong(cur, run, te["A"], tien))
            for j in range(12):
                ids["B"].append(_dong(cur, run, te["B"], str(10 ** (j % 6) + j)))
            ids["C"].append(_dong(cur, run, te["C"], "0"))
        pv = mot_lan_nap(run)
        a = ids["A"]
        gt.ghi_ly_do(c, pv, a[3], reason="ly do dau", actor=ACTOR)
        gt.ghi_ly_do(c, pv, a[3], reason="ly do SAU thang", actor=ACTOR)
        gt.ghi_hoan(c, pv, a[8], den_ngay="2026-12-01", reason="cho", actor=ACTOR)
        gt.ghi_hoan(c, pv, a[8], den_ngay="2026-12-31", reason="cho 2", actor=ACTOR)
        gt.ghi_hoan(c, pv, ids["B"][11], den_ngay="2026-11-11", reason="h",
                    actor=ACTOR)
        gt.danh_dau_xong(c, pv, a[20], actor=ACTOR, reason="xong")
        return {"run": run, "te": te, "ids": ids, "xong": a[20]}


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _lat_het(conn, pv, curr, n):
    """⚠ Có **trần** số trang: con trỏ hỏng kiểu `>=` trả lại **chính** hàng
    cuối ⇒ `limit=1` lật mãi một hàng *(đã treo một lượt chứng đỏ 06/10)* ⇒
    vượt trần là **ĐỎ**, ⛔ treo."""
    dong, tro, vet = [], None, []
    for _ in range(200):
        if len(vet) > 100:
            pytest.fail(f"⛔ lật quá 100 trang — con trỏ ⛔ tiến: {vet[-3:]}")
        t = bc.doc_hang_cho(conn, pv, curr=curr, con_tro=tro, limit=n)
        dong += t.dong
        vet.append(t.con_tro)
        tro = t.con_tro
        if not tro:
            return dong, vet


def _hang(d: dict) -> tuple:
    return tuple((k, d[k]) for k in sorted(d))


@pytest.mark.parametrize("n", [1, 7, 50])
@pytest.mark.parametrize("theo", ["A", "B", "C", None])
def test_AC4_moi_trang_noi_lai_BANG_HET_oracle_khong_con_tro(ca, conn, theo, n):
    pv = mot_lan_nap(ca["run"])
    curr = ca["te"][theo] if theo else None
    orc = oracle_hang_cho(conn, pv, curr)
    mong_n = {"A": 36, "B": 12, "C": 1, None: 49}[theo]   # A: 37 − 1 đã xong
    assert len(orc) == mong_n, ("⛔ không đo được: oracle", len(orc))
    dong, vet = _lat_het(conn, pv, curr, n)
    assert [_hang(d) for d in dong] == [_hang(d) for d in orc], (
        f"⛔ lệch oracle (curr={curr}, limit={n}):",
        [d["itl_id"] for d in dong][:20], [d["itl_id"] for d in orc][:20])
    # `next_cursor` = `(curr, hang)` của hàng cuối mỗi trang, trang cuối None
    mong_vet = [f"{orc[k]['curr']}:{orc[k]['hang']}"
                for k in range(n - 1, len(orc) - 1, n)] + [None]
    assert vet == mong_vet, (vet, mong_vet)


def test_AC4_CA_co_du_thu_can_so(ca, conn):
    """Mẫu số *(`Đ3`)*: ca **thật sự** có lý do · hoãn · tiền bằng nhau · đã
    xong — ⛔ thì bài trên so trên tập ⛔ có gì để lệch."""
    pv = mot_lan_nap(ca["run"])
    orc = oracle_hang_cho(conn, pv, ca["te"]["A"])
    theo = {d["itl_id"]: d for d in orc}
    a = ca["ids"]["A"]
    assert theo[a[3]]["reason"] == "ly do SAU thang"
    assert theo[a[8]]["defer_count"] == 2
    assert str(theo[a[8]]["defer_until"]) == "2026-12-31"
    assert ca["xong"] not in theo, "dòng đã xong phải rời hàng chờ"
    bang = [d for d in orc if d["tien"] == D("5000")]
    assert len(bang) == 9 and [d["itl_id"] for d in bang] == sorted(a[:9])
    assert sum(d["reason"] is None and d["defer_count"] is None
               for d in orc) > 0, "phải có dòng ⛔ sự kiện (LEFT, ⛔ JOIN thường)"
    # do_phu dùng CTE chung ⛔ đổi
    dp = {d["curr"]: d for d in bc.do_phu_hang_cho(conn, pv, 90)}
    assert dp[ca["te"]["A"]]["so_dong_cho"] == 36
