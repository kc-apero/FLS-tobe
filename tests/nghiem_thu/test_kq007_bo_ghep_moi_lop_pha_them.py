"""`KQ-007` — kịch bản PHÁ THÊM cho `WO-003` vòng 2 *(`BG-006`, mã `5fbc29c`)*.

⭐ Ba ca `BG-006` ⛔ có bài riêng, đo được 01/10/2026 tối trên kho TEST
*(`fls-test`, `scratchpad/pha_wo003_v2.py` P1–P4)*:

  ① **≥ 3 lớp gợi ý + NGƯỜI gõ giữa chừng** rồi bỏ ghép — cả đường TAY lẫn
     dòng MÁY ghép `hinh='A'`. Spec: `BA-10` v0.7 `DT-I14` *Luật một câu*
     *(đảo mọi bút toán gắn `match` chưa có bản đảo, ⛔ chạm giá trị người)* +
     `BA-11` v0.15 `INV-I22 ⓐ`.
  ② **ghép → bỏ → ghép lại (+ lớp `goi_y_lai` chồng) → bỏ → ghép lại → bỏ** —
     ba vòng, ⛔ bút toán nào bị đảo hai lần *(`DT-I14` nhánh 7)*.
  ③ ⭐ `BG-006` "Dev tự thấy còn yếu" mục 1: bút toán ghép `sua_tay` **CŨ**
     nằm **TRÊN** giá trị người ⇒ sau khi đảo, giá trị người phải hiện trong
     `bo_qua` *(định nghĩa `bo_qua`, `DT-I14` v0.7 — mục = dòng khung xem
     `fls_sua_tay` ⛔ gắn `match`, trên ô từng có bút toán `match`)*. Dev chọn
     đọc khung xem **SAU** khi đảo; bài này ghim lựa chọn ấy.

⭐⭐ **Chứng minh ĐỎ** *(`Đ5`)*: cả ba bài chạy trên **worktree `38a6b08`**
*(mã vòng 1 — chọn tập đảo qua khung xem, dựng `bo_qua` TRƯỚC khi đảo)* ⇒
**ĐỎ** đúng lý do; xanh trên `5fbc29c`. Biên bản: `KQ-007` mục *Bài thử mới*.
"""
from __future__ import annotations

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (ACTOR, D, _mot_dong,  # noqa: F401
                                                        conn)

pytestmark = pytest.mark.pg

NGUOI = "kt2@apero.vn"


def _goi_y(conn, i: int) -> dict:
    return dict(conn.execute("SELECT field, value_after FROM fls_may_goi_y"
                             " WHERE itl_id=%s", (i,)).fetchall())


def _sua(conn, i: int) -> dict:
    return dict(conn.execute("SELECT field, value_after FROM fls_sua_tay"
                             " WHERE itl_id=%s", (i,)).fetchall())


def _chua_dao(conn, i: int) -> int:
    """`INV-I22 ⓐ` đọc BẢNG GỐC: bút toán gợi ý gắn `match` chưa có bản đảo."""
    return conn.execute(
        "SELECT count(*) FROM fls_adjustment a"
        "  JOIN fls_queue_event e ON e.evt_id = a.evt_id"
        " WHERE a.itl_id=%s AND e.evt_type='match' AND a.nguon='may_goi_y'"
        "   AND NOT EXISTS (SELECT 1 FROM fls_adjustment d"
        "                    WHERE d.reversal_of = a.adj_id)", (i,)).fetchone()[0]


def _so_ban_dao(conn, i: int) -> dict[int, int]:
    return dict(conn.execute(
        "SELECT a.adj_id, (SELECT count(*) FROM fls_adjustment d"
        "                   WHERE d.reversal_of = a.adj_id)"
        "  FROM fls_adjustment a JOIN fls_queue_event e ON e.evt_id = a.evt_id"
        " WHERE a.itl_id=%s AND e.evt_type='match'", (i,)).fetchall())


def _bo_qua_chi_nguoi(conn, ra: dict) -> list:
    """Mọi mục `bo_qua`: `nguon='sua_tay'`, bút toán ⛔ gắn `match`, chưa đảo,
    ⛔ nằm trong `but_toan_dao`, ≤ 1 mục/ô. Trả danh sách VI PHẠM."""
    sai = []
    o = [x["field"] for x in ra["bo_qua"]]
    if len(o) != len(set(o)):
        sai.append(("o_lap", o))
    dao = {x["dao_cua"] for x in ra["but_toan_dao"]}
    for x in ra["bo_qua"]:
        r = conn.execute(
            "SELECT a.nguon, e.evt_type, (SELECT count(*) FROM fls_adjustment d"
            "  WHERE d.reversal_of = a.adj_id) FROM fls_adjustment a"
            "  LEFT JOIN fls_queue_event e ON e.evt_id = a.evt_id"
            " WHERE a.adj_id=%s", (x["adj_id"],)).fetchone()
        if (r[0] != "sua_tay" or r[1] == "match" or r[2] != 0
                or x["adj_id"] in dao or x.get("nguon") != "sua_tay"):
            sai.append((x, r))
    return sai


# ═══════════════ ① ≥ 3 lớp + người gõ giữa chừng
def test_TAY_ba_lop_goi_y_NGUOI_go_giua_chung__bo_ghep_dao_HET_lop_may_nguoi_NGUYEN(conn):  # noqa: F811
    _r, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason="")
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-B",
                                         "cdt1": "C-1"}])
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-NGUOI", actor=NGUOI,
                    reason="go tay", force=True)
    g3 = ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-C",
                                              "cdt1": "C-2"}])
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-D",
                                         "cdt1": "C-3"}])
    # mẫu số (`Đ3`): HD-A, HD-B, C-1, C-2, C-3 — người đã chốt hd nên HD-C/D ⛔ ghi
    assert g3["nguoi_da_chot"] == ["hd"]
    assert _chua_dao(conn, i) == 5, "⛔ không đo được: ⛔ dựng được 5 lớp"
    assert _goi_y(conn, i) == {"hd": "HD-B", "cdt1": "C-3"}

    ra = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="")

    assert _chua_dao(conn, i) == 0, "⛔⛔ còn lớp gợi ý chưa đảo (INV-I22 ⓐ)"
    assert _goi_y(conn, i) == {}, f"⛔⛔ gợi ý MỒ CÔI: {_goi_y(conn, i)}"
    assert len(ra["but_toan_dao"]) == 5
    assert set(_so_ban_dao(conn, i).values()) == {1}
    assert _sua(conn, i) == {"hd": "HD-NGUOI"}, "⛔⛔ bỏ ghép chạm giá trị NGƯỜI"
    assert gt.truoc_khi_go(conn, pv, i, "hd")["gia_tri"] == "HD-NGUOI"
    assert [(x["field"], x["value_after"]) for x in ra["bo_qua"]] == \
        [("hd", "HD-NGUOI")], ra["bo_qua"]
    assert _bo_qua_chi_nguoi(conn, ra) == []


def test_MAY_ghep_hinh_A_ba_lop_NGUOI_go_cdt1__bo_ghep_ve_0(conn):  # noqa: F811
    run, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i, ma, D("5000000.00"), run))
    for hd, cd in (("HD-A", "C-1"), ("HD-B", "C-2")):
        ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": hd,
                                             "cdt1": cd}], run_pm=run)
    gt.ghi_but_toan(conn, chi_nap_that(), i, "cdt1", "C-NGUOI", actor=NGUOI,
                    reason="go tay", force=True)
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-C",
                                         "cdt1": "C-3"}], run_pm=run)
    assert _chua_dao(conn, i) == 5, "⛔ không đo được"

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="")

    assert _chua_dao(conn, i) == 0 and _goi_y(conn, i) == {}, \
        f"⛔⛔ dòng máy ghép còn gợi ý sau bỏ ghép: {_goi_y(conn, i)}"
    assert _sua(conn, i) == {"cdt1": "C-NGUOI"}
    assert [(x["field"], x["value_after"]) for x in ra["bo_qua"]] == \
        [("cdt1", "C-NGUOI")], ra["bo_qua"]
    assert _bo_qua_chi_nguoi(conn, ra) == []


# ═══════════════ ② ba vòng ghép/bỏ, có lớp chồng ở vòng giữa
def test_BA_vong_ghep_bo_co_lop_chong__moi_but_toan_DUNG_mot_ban_dao(conn):  # noqa: F811
    _r, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    pv = chi_nap_that()
    rs = []
    for vong in range(3):
        gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason="")
        if vong == 1:
            ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-X",
                                                 "cdt1": "C-X"}])
        rs.append(gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason=""))
        assert _goi_y(conn, i) == {}, \
            f"⛔⛔ vòng {vong + 1}: gợi ý MỒ CÔI sau bỏ ghép: {_goi_y(conn, i)}"

    so = _so_ban_dao(conn, i)
    # 2 (vòng 1) + 2 + 2 lớp chồng (vòng 2) + 2 (vòng 3)
    assert len(so) == 8, f"mong 8 bút toán gắn match, thấy {so}"
    assert set(so.values()) == {1}, f"⛔⛔ bút toán ⛔ đúng một bản đảo: {so}"
    assert [len(x["but_toan_dao"]) for x in rs] == [2, 4, 2]
    assert _chua_dao(conn, i) == 0 and _goi_y(conn, i) == {}
    assert all(x["bo_qua"] == [] for x in rs), \
        f"⛔⛔ ⛔ ai gõ mà bo_qua có mục: {[x['bo_qua'] for x in rs]}"


# ═══════════════ ③ `BG-006` yếu #1 — bút toán ghép sua_tay CŨ nằm TRÊN người
def test_but_toan_ghep_CU_sua_tay_o_TREN_gia_tri_nguoi__bo_qua_HIEN_nguoi(conn):  # noqa: F811
    run, i, ma = _mot_dong(conn, hd="HD-CU", cdt1="C-1")
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,5000000.00,'T',%s)", (i, ma, run))
    pv = chi_nap_that()
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-NGUOI", actor=NGUOI,
                    reason="go tay truoc", force=True)
    # ⚠ hình dạng lối ghi CŨ (trước `WO-003`): bút toán `sua_tay` gắn `match`
    e = gt._them_su_kien(conn, itl_id=i, evt_type="match", actor=ACTOR,
                         reason="ghep kieu cu (truoc WO-003)")
    cu, _j = gt._them(conn, itl_id=i, field="hd", value_before="HD-NGUOI",
                      value_after="HD-CU", actor=ACTOR, value_source="sua_tay",
                      reason="suy tu dong lenh (luat cu)", evt_id=e,
                      nguon="sua_tay")
    assert conn.execute("SELECT adj_id FROM fls_sua_tay WHERE itl_id=%s"
                        " AND field='hd'", (i,)).fetchone()[0] == cu, \
        "⛔ không đo được: bút toán cũ ⛔ nằm TRÊN giá trị người"

    ra = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="")

    assert [x["dao_cua"] for x in ra["but_toan_dao"]] == [cu]
    assert _sua(conn, i) == {"hd": "HD-NGUOI"}
    assert [(x["field"], x["nguon"], x["value_after"]) for x in ra["bo_qua"]] \
        == [("hd", "sua_tay", "HD-NGUOI")], (
        f"⛔⛔ giá trị NGƯỜI lộ ra sau khi đảo mà ⛔ vào bo_qua: {ra['bo_qua']} — "
        f"màn F01 sẽ ⛔ báo 'người đã gõ tay', kế toán tưởng bỏ ghép đã dọn sạch")
