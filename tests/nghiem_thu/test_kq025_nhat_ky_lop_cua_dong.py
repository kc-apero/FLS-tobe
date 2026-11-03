# -*- coding: utf-8 -*-
"""`KQ-025` — kiểm `BG-024` *(`WO-018`)*: nhật ký `value_source` = **lớp của
CHÍNH dòng** trên những đường bài của Dev **⛔ đi qua**.

Spec: `BA-05` **v0.34** `DD-I15 ⓓe` — *"Bản đảo ⇒ lớp của **dòng bị đảo**
(rút một gợi ý máy là `may_goi_y`, đảo một giá trị người là `sua_tay`)"* ·
bất biến `fls_journal.value_source = fls_adjustment.nguon` cùng giao dịch.
`BA-06` v4.9 dòng *"F02 · nhật ký"*: `may_goi_y` rỗng ⇒ *"rút gợi ý"*.

⛔⛔ **Lỗ phủ của bộ bài Dev** *(`BG-024` "còn yếu" #4, đo bằng đọc bài)*:
  ⓐ cửa **`POST /adjustments/{id}/reverse`** *(HTTP thật)* ⛔ bài nào gọi trên
     một dòng **máy** — bài `AC-3` của Dev gọi thẳng hàm repo `dao_but_toan`;
  ⓑ màn `F02` ⑦ cho bản đảo **qua cửa đảo** ⛔ bài nào vẽ — bài màn chỉ có bản
     đảo của `bo_moi_noi`;
  ⓒ đảo một dòng máy **nằm DƯỚI** giá trị người *(ô đã có người gõ đè)* —
     đột biến *"lấy lớp từ ô"* thay vì *"từ dòng bị đảo"* ⛔ bài nào bắt.
Nút `Đảo` ở khối ⑥ `F02` hiện cho **mọi** bút toán ⛔ phải bản đảo — kể cả
**4.424** dòng máy trên sổ thật *(`doc_bao_cao.py:468`–`471` đọc cả
`fls_adjustment`, ⛔ lọc `nguon`)* ⇒ đường ⓐ **tới được từ màn**.

⛔ Chiều ĐỎ *(chạy thật — `KQ-025` mục "Bài thử mới")*: trả `dao_but_toan` về
`NGUON_TAY` cứng *(mã `b065794`)* ⇒ bài ⓐ/ⓑ ĐỎ; lấy lớp theo **ô** ⇒ bài ⓒ ĐỎ;
ghi cứng `NGUON_MAY` ⇒ bài đảo dòng **người** ĐỎ.
"""
from __future__ import annotations

import json
from collections import Counter

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _mot_dong, conn  # noqa: F401
from tests.web.khung_node import _VE, _chay, can_node
from tests.web.test_drawer_f02 import _BAM, DONG_DAY
from tests.web.test_vong_f02_pg import AI, V, _goi, du_lieu, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import (NHAN_MAY, NHAN_NGUOI, RUT,
                                                      _bang_nhat_ky)

pytestmark = pytest.mark.pg


def _doc(sql: str, *tham) -> list[tuple]:
    with psycopg.connect(dsn_test()) as c:
        return c.execute(sql, tham).fetchall()


def _adj_hieu_luc(itl_id: int, field: str, nguon: str) -> int:
    r = _doc(
        "SELECT max(a.adj_id) FROM fls_adjustment a WHERE a.itl_id=%s"
        " AND a.field=%s AND a.nguon=%s AND a.reversal_of IS NULL"
        " AND NOT EXISTS (SELECT 1 FROM fls_adjustment d"
        "                  WHERE d.reversal_of=a.adj_id)",
        itl_id, field, nguon)[0][0]
    assert r is not None, f"⛔ không đo được: ô {itl_id}/{field} ⛔ có lớp {nguon}"
    return r


def _dao_qua_cua(may, adj_id: int) -> dict:  # noqa: F811
    ok, r = _goi(may, f"{V}/adjustments/{adj_id}/reverse", pt="POST",
                 than={"reason": "KQ-025 dao qua cua that"})
    assert ok == 200, r
    return r["data"]


def _ban_dao(adj_goc: int) -> tuple:
    """`(nguon bản đảo, value_source nhật ký của nó, actor)` — nối đúng một."""
    r = _doc(
        "SELECT d.nguon, j.value_source, d.actor FROM fls_adjustment d"
        "  JOIN fls_journal j ON j.itl_id=d.itl_id AND j.field=d.field"
        "   AND j.at=d.at AND j.actor=d.actor AND j.value_after IS NULL"
        " WHERE d.reversal_of=%s", adj_goc)
    assert len(r) == 1, f"⛔ không đo được: bản đảo của #{adj_goc} nối {len(r)} dòng nhật ký"
    return r[0]


def _ve_nhat_ky(itl_id: int) -> list[list[str]]:
    """Thân `GET /journal` THẬT ⇒ màn `F02` ⑦ *(node)*; trả hàng bảng."""
    nk = [dict(zip(("at", "field", "value_before", "value_after", "actor",
                    "value_source", "reason"), x)) for x in _doc(
        "SELECT at, field, value_before, value_after, actor, value_source,"
        " reason FROM fls_journal WHERE itl_id=%s ORDER BY jrn_id", itl_id)]
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
      HT.mo = () => ({dong(){}});
    """ % (json.dumps(DONG_DAY, ensure_ascii=False),
           json.dumps(nk, ensure_ascii=False, default=str))) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    return _bang_nhat_ky(ra)


def _than_journal(may, itl_id: int) -> list[dict]:  # noqa: F811
    ok, nk = _goi(may, f"{V}/journal?itl_id={itl_id}")
    assert ok == 200, nk
    return nk["data"]["rows"]


# ══ ⓐ `/reverse` một dòng MÁY qua cửa thật ══════════════════════════════
@pytest.fixture()
def dao_dong_may(conn, may):  # noqa: F811
    """Ghép tay qua cửa ⇒ 2 gợi ý; người bấm `Đảo` gợi ý `hd` qua cửa đảo."""
    _r, i, ma = _mot_dong(conn, hd="HD-MAY-25", cdt1="C-25")
    ok, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": [ma]})
    assert ok == 200, r
    goc = _adj_hieu_luc(i, "hd", "may_goi_y")
    sua_tay_truoc = _doc("SELECT count(*) FROM fls_sua_tay WHERE itl_id=%s", i)
    than = _dao_qua_cua(may, goc)
    sua_tay_sau = _doc("SELECT count(*) FROM fls_sua_tay WHERE itl_id=%s", i)
    return i, goc, than, sua_tay_truoc, sua_tay_sau


def test_a_reverse_dong_MAY_qua_cua__ban_dao_va_nhat_ky_mang_MAY_GOI_Y(dao_dong_may):
    """`ⓓe`: rút một gợi ý máy là `may_goi_y` — cả `fls_adjustment.nguon`
    **lẫn** `fls_journal.value_source` của bản đảo; `actor` = người bấm;
    Final ⛔ đổi *(`fls_sua_tay` của dòng 0 → 0)*."""
    i, goc, than, st0, st1 = dao_dong_may
    nguon, vs, actor = _ban_dao(goc)
    assert (nguon, vs) == ("may_goi_y", "may_goi_y"), (
        f"⛔⛔ bản đảo của dòng MÁY #{goc} mang nguon={nguon!r} · "
        f"value_source={vs!r} — `BA-05` v0.34 `ⓓe`: lớp của dòng bị đảo")
    assert actor == AI, actor
    assert st0 == st1 == [(0,)], f"⛔ rút gợi ý máy mà Final đổi: {st0} → {st1}"
    assert than["value_before"] == "HD-MAY-25" and than["dao_cua"] == goc, than


@can_node
def test_b_man_F02_ve_ban_dao_qua_cua_la_RUT_GOI_Y__khong_phai_nguoi_sua(
        dao_dong_may, may):  # noqa: F811
    """Màn `F02` ⑦ trên thân `GET /journal` thật: hàng bản đảo `hd` in
    *"rút gợi ý"* + *"máy gợi ý · không đổi Final"*; **0** nhãn *"người sửa"*
    *(dòng này ⛔ ai gõ)*; ⛔ hàng nào ô thành trống."""
    i, *_ = dao_dong_may
    rows = _than_journal(may, i)
    assert len(rows) >= 3, f"⛔ không đo được: {len(rows)} dòng nhật ký (mong ≥ 3)"
    hang = _ve_nhat_ky(i)
    assert len(hang) == len(rows), (len(hang), len(rows))
    dao = [h for h in hang if h[1] == "hd" and h[3] == RUT]
    assert len(dao) == 1, f"⛔ mong đúng 1 hàng 'rút gợi ý' cho ô hd: {hang}"
    assert dao[0][5] == NHAN_MAY, dao
    assert NHAN_NGUOI not in [h[5] for h in hang], (
        "⛔⛔ người chỉ RÚT gợi ý máy mà nhật ký gọi là 'người sửa' — "
        f"hậu kiểm đọc thành người đã chốt giá trị: {hang}")
    assert [h for h in hang if h[3] == ""] == [], f"⛔ ô thành trống: {hang}"


# ══ ⓒ đảo dòng MÁY nằm DƯỚI giá trị người ═══════════════════════════════
def test_c_reverse_dong_MAY_nam_DUOI_gia_tri_NGUOI__lop_lay_tu_DONG_bi_dao(
        conn, may):  # noqa: F811
    """Ô `hd`: gợi ý máy *(ghép)* rồi người gõ đè `HD-NGUOI-25` *(force)* ⇒ lớp
    trên cùng là **người**. Đảo dòng **máy** bên dưới qua cửa ⇒ bản đảo vẫn
    `may_goi_y` *(lớp lấy từ **dòng bị đảo**, ⛔ từ ô)*; Final giữ `HD-NGUOI-25`.
    """
    _r, i, ma = _mot_dong(conn, hd="HD-MAY-C", cdt1="C-C")
    ok, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": [ma]})
    assert ok == 200, r
    goc = _adj_hieu_luc(i, "hd", "may_goi_y")
    ok, r = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-NGUOI-25", "force": True,
                       "reason": "KQ-025 go de"})
    assert ok == 200, r
    _dao_qua_cua(may, goc)
    assert _ban_dao(goc)[:2] == ("may_goi_y", "may_goi_y")
    assert _doc("SELECT value_after FROM fls_sua_tay WHERE itl_id=%s AND"
                " field='hd'", i) == [("HD-NGUOI-25",)], "⛔ Final người bị rút"


# ══ ⓓ `/reverse` một dòng NGƯỜI qua cửa thật ═════════════════════════════
def test_d_reverse_dong_NGUOI_qua_cua__ban_dao_mang_SUA_TAY_va_Final_lui(
        may, du_lieu):  # noqa: F811
    """Đảo một giá trị người là `sua_tay` *(`ⓓe`)*; Final lùi về sổ gốc."""
    i = du_lieu["nguon"]                         # hd sổ gốc = HD-SO-GOC
    ok, r = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-NGUOI-D", "force": True,
                       "reason": "KQ-025 go"})
    assert ok == 200, r
    goc = _adj_hieu_luc(i, "hd", "sua_tay")
    _dao_qua_cua(may, goc)
    assert _ban_dao(goc)[:2] == ("sua_tay", "sua_tay")
    ok, f = _goi(may, f"{V}/ledger/{i}/fields/hd")
    assert ok == 200, f
    assert (f["data"]["gia_tri"], f["data"]["value_source"]) == \
        ("HD-SO-GOC", "nguon"), f["data"]


# ══ ⓔ bất biến cặp trên dữ liệu dựng HOÀN TOÀN qua HTTP ══════════════════
def test_e_bat_bien_cap_tren_moi_dong_dung_QUA_CUA(conn, may, du_lieu):  # noqa: F811
    """Đa tập `(itl_id, field, at, actor, value_source)` nhật ký **=** đa tập
    `(…, nguon)` bút toán trên các dòng chỉ ghi **qua cửa HTTP**: `/adjust`
    ô rỗng · ô có nguồn · ô có `*_thyt` · ô đã có người · xoá giá trị *(null)*
    · `/match` · `/reverse` dòng máy + dòng người · `/unmatch`. Mẫu số ≥ 10."""
    tap = [du_lieu["trong"], du_lieu["nguon"], du_lieu["may"]]
    for i, v in ((du_lieu["trong"], "HD-1"), (du_lieu["trong"], "HD-2"),
                 (du_lieu["nguon"], "HD-X"), (du_lieu["may"], "HD-Y"),
                 (du_lieu["nguon"], None)):
        ok, r = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                     than={"field": "hd", "value": v, "force": True,
                           "reason": "KQ-025 e"})
        assert ok == 200, r
    _dao_qua_cua(may, _adj_hieu_luc(du_lieu["trong"], "hd", "sua_tay"))
    _r, j, ma = _mot_dong(conn, hd="HD-E", cdt1="C-E")
    tap.append(j)
    ok, r = _goi(may, f"{V}/queue/{j}/match", pt="POST",
                 than={"pm_line_ids": [ma]})
    assert ok == 200, r
    _dao_qua_cua(may, _adj_hieu_luc(j, "cdt1", "may_goi_y"))
    ok, r = _goi(may, f"{V}/queue/{j}/unmatch", pt="POST", than={})
    assert ok == 200, r
    nk = Counter(_doc("SELECT itl_id, field, at, actor, value_source FROM"
                      " fls_journal WHERE itl_id = ANY(%s)", tap))
    bt = Counter(_doc("SELECT itl_id, field, at, actor, nguon FROM"
                      " fls_adjustment WHERE itl_id = ANY(%s)", tap))
    n = sum(bt.values())
    print(f"\n[KQ-025 e] mẫu số: {n} bút toán ⇔ {sum(nk.values())} dòng nhật ký"
          f" trên {len(tap)} dòng sổ")
    assert n >= 10, f"⛔ không đo được: mẫu số {n} < 10 (`Đ3`)"
    assert nk == bt, (f"chỉ ở nhật ký: {sorted((nk - bt).elements(), key=str)}"
                      f" · chỉ ở bút toán: {sorted((bt - nk).elements(), key=str)}")
    # ⭐ nhật ký mới ⛔ còn mã nghĩa cũ
    la = _doc("SELECT DISTINCT value_source FROM fls_journal"
              " WHERE itl_id = ANY(%s)", tap)
    assert {x[0] for x in la} <= {"sua_tay", "may_goi_y"}, la
    # ⭐ cặp bằng nhau CHƯA ĐỦ *(`BG-024` yếu #2)*: ghi cùng một lớp sai ở cả
    #   hai bảng vẫn bằng ⇒ canh thẳng *"bản đảo = lớp dòng bị đảo"* — cả bản
    #   đảo qua `/reverse` lẫn qua `/unmatch`.
    dao = _doc("SELECT d.adj_id, d.nguon, g.nguon, d.evt_id IS NULL"
               "  FROM fls_adjustment d JOIN fls_adjustment g"
               "    ON g.adj_id = d.reversal_of WHERE d.itl_id = ANY(%s)", tap)
    loai = Counter((x[2], x[3]) for x in dao)
    print(f"[KQ-025 e] bản đảo theo (lớp gốc, qua /reverse): {dict(loai)}")
    assert loai[("sua_tay", True)] >= 1 and loai[("may_goi_y", True)] >= 1 \
        and loai[("may_goi_y", False)] >= 1, f"⛔ không đo được: {dict(loai)}"
    assert [x for x in dao if x[1] != x[2]] == [], dao
