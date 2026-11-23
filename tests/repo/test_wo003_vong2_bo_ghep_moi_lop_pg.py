# -*- coding: utf-8 -*-
"""`WO-003` **vòng 2** — bỏ ghép đảo **MỌI LỚP** gợi ý · `bo_qua` chỉ giá trị
NGƯỜI · ghim ca TRỘN.

⭐⭐⭐ Căn cứ: `KQ-005` *(`fls-test` 01/10 — ⛔ TRƯỢT `AC-7`)* `F-1` · `F-2` ·
`F-3`; spec `BA-10` v0.7 `DT-I14` *(bảng Bỏ ghép nhánh 6–8 · Luật một câu ·
Định nghĩa `bo_qua` · nhánh `5a`)* · `BA-11` v0.15 `INV-I22` · `BA-09` v0.6
`SM-I06` *(chuyển cấm `F-10`, `F-11`)* · `BA-05` v0.33 `DD-I15 ⓓd`.

⛔⛔ **Lỗ ĐÃ ĐO, ⛔ không phải lo xa** *(`KQ-005`, kho TEST, 2/2 kịch bản)*:
vòng 1 chọn thứ cần đảo qua khung xem `fls_may_goi_y` ∪ `fls_sua_tay`. Hai khung
xem ấy *(migration `0025`)* trả lời *"ô này ĐANG là gì"* = **lớp trên cùng**.
Khi `tools/goi_y_lai.py` đã chồng một gợi ý mới lên, bỏ ghép đảo lớp trên, và
**lớp dưới nổi lên lại** thành gợi ý **mồ côi** trên dòng 0 mối nối. Câu đúng
là *"bút toán nào còn căn cứ"* — hỏi thẳng bảng gốc + `reversal_of`.

⭐ Mọi phép đếm ở đây trên **CÙNG một `itl_id`** vừa dựng, và chứng minh mẫu
số ≠ 0 trước khi kết luận *(`Đ3`)*.
"""
from __future__ import annotations

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (ACTOR, LY_DO, _dong_bank,  # noqa: F401
                                                        _lenh, _ma, _mot_dong,
                                                        _run, conn)

pytestmark = pytest.mark.pg

# ⭐ `INV-I22 ⓐ` viết thành SQL: bút toán gợi ý gắn sự kiện `match` của dòng mà
#   ⛔ dòng nào có `reversal_of` trỏ về — đọc **bảng gốc**, ⛔ khung xem.
_SQL_GOI_Y_CHUA_DAO = (
    "SELECT count(*) FROM fls_adjustment a"
    "  JOIN fls_queue_event e ON e.evt_id = a.evt_id"
    " WHERE a.itl_id = %s AND e.evt_type = 'match' AND a.nguon = 'may_goi_y'"
    "   AND NOT EXISTS (SELECT 1 FROM fls_adjustment d"
    "                    WHERE d.reversal_of = a.adj_id)")


def _chua_dao(conn, i: int) -> int:
    return conn.execute(_SQL_GOI_Y_CHUA_DAO, (i,)).fetchone()[0]


def _goi_y(conn, i: int) -> dict:
    return dict(conn.execute("SELECT field, value_after FROM fls_may_goi_y"
                             " WHERE itl_id=%s", (i,)).fetchall())


def _so_ban_dao(conn, i: int) -> dict[int, int]:
    """{adj_id gợi ý gắn `match` → số bản đảo trỏ về nó}."""
    return dict(conn.execute(
        "SELECT a.adj_id, (SELECT count(*) FROM fls_adjustment d"
        "                   WHERE d.reversal_of = a.adj_id)"
        "  FROM fls_adjustment a JOIN fls_queue_event e ON e.evt_id = a.evt_id"
        " WHERE a.itl_id = %s AND e.evt_type = 'match'", (i,)).fetchall())


# ═════════════════════════════ (e) `F-1` — đảo MỌI LỚP · AC-14
def test_BA_lop_goi_y_chong__bo_ghep_dao_CA_BON__moi_cai_DUNG_mot_ban_dao(conn):
    """⭐⭐ AC-14 ⓐⓑⓒ + `WO-003` vòng 2 Rủi ro 2.

    ghép tay *(`hd=HD-A`, `cdt1=C-1`)* → `ghi_goi_y_may` chồng `hd=HD-B` →
    chồng `hd=HD-C` → bỏ ghép. Khung xem chỉ thấy `HD-C` + `C-1`; hai lớp
    `HD-A`, `HD-B` nằm dưới, **chưa đảo** ⇒ phải đảo cả bốn.
    """
    _run_id, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    for hd in ("HD-B", "HD-C"):
        g = ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": hd,
                                                 "cdt1": "C-1"}])
        assert [x["field"] for x in g["but_toan"]] == ["hd"], \
            f"⛔ không đo được: ⛔ chồng được lớp {hd} — {g}"
    assert _goi_y(conn, i) == {"hd": "HD-C", "cdt1": "C-1"}
    # ⓐ mẫu số ≠ 0 (`Đ3`): BỐN bút toán gợi ý chưa đảo, khung xem chỉ trả HAI
    assert _chua_dao(conn, i) == 4

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")

    # ⓑ `INV-I22 ⓐ`: 0 gợi ý chưa đảo, và khung xem — kể cả lớp dưới — rỗng
    assert _chua_dao(conn, i) == 0, "⛔⛔ còn lớp gợi ý chưa đảo sau bỏ ghép"
    assert _goi_y(conn, i) == {}, "⛔⛔ gợi ý lớp dưới NỔI LÊN LẠI (mồ côi)"
    assert len(ra["but_toan_dao"]) == 4, ra["but_toan_dao"]
    # ⓒ mỗi bút toán gợi ý có ĐÚNG 1 bản đảo
    so = _so_ban_dao(conn, i)
    assert len(so) == 4 and set(so.values()) == {1}, so
    # ⭐ Rủi ro 2: bản đảo của lớp dưới mang `value_before` = giá trị CỦA CHÍNH
    #   LỚP ẤY — nhật ký đọc được "rút HD-A", "rút HD-B", "rút HD-C" riêng.
    rut = sorted(r[0] for r in conn.execute(
        "SELECT value_before FROM fls_journal WHERE itl_id=%s"
        "   AND value_after IS NULL AND value_source='may_goi_y'", (i,)))
    assert rut == ["C-1", "HD-A", "HD-B", "HD-C"], rut
    # ⛔ ai gõ ⇒ `bo_qua` rỗng (`F-2`)
    assert ra["bo_qua"] == []


def test_ghep_BO_ghep_lai_BO__KHONG_bao_gio_dao_HAI_lan(conn):
    """⭐ AC-14 ⓓ — `WO-003` vòng 2 Rủi ro 1. Phép chọn mới đọc bảng gốc ⇒ nó
    THẤY cả bút toán vòng ghép trước; bỏ điều kiện *"chưa có bản đảo"* thì vòng
    ghép-lại → bỏ đảo lại bút toán vòng trước *(DT-I14 nhánh 7)*."""
    _run_id, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason=LY_DO)
    r1 = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="ghep sai")
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason=LY_DO)
    assert _chua_dao(conn, i) == 2, "⛔ không đo được: ghép lại ⛔ gợi ý lại"
    r2 = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="ghep sai lan 2")

    assert len(r1["but_toan_dao"]) == 2 and len(r2["but_toan_dao"]) == 2
    so = _so_ban_dao(conn, i)
    assert len(so) == 4, f"⛔ không đo được: mong 4 bút toán gợi ý, thấy {so}"
    hai = {k: v for k, v in so.items() if v >= 2}
    assert not hai, f"⛔⛔ bút toán bị đảo HAI lần: {hai}"
    assert set(so.values()) == {1}, so
    assert _chua_dao(conn, i) == 0 and _goi_y(conn, i) == {}


def test_but_toan_ghep_CU_sua_tay_o_LOP_DUOI_gia_tri_nguoi__van_DAO__nguoi_NGUYEN(conn):
    """`DT-I14` nhánh 8 *(v0.7: "bất kể lớp")*: bút toán ghép **cũ** *(trước
    `WO-003`, `nguon='sua_tay'`, gắn `match`)* bị một giá trị NGƯỜI đè ⇒ khung
    xem `fls_sua_tay` ⛔ trả nó, nhưng nó vẫn chưa đảo ⇒ ĐẢO, bản đảo mang
    `nguon='sua_tay'`. Giá trị người **⛔ chạm** và vẫn là Final.

    ⚠ Kho thật 01/10: **0** dòng như thế *(2 dòng UAT đã đảo)* — dựng tay đúng
    hình dạng lối ghi cũ *(`_them` + sự kiện `match`)*.
    """
    run, i, ma = _mot_dong(conn, hd="HD-CU", cdt1="C-1")
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,5000000.00,'T',%s)", (i, ma, run))
    e = gt._them_su_kien(conn, itl_id=i, evt_type="match", actor=ACTOR,
                         reason="ghep kieu cu (truoc WO-003)")
    cu, _j = gt._them(conn, itl_id=i, field="hd", value_before=None,
                      value_after="HD-CU", actor=ACTOR, value_source="sua_tay",
                      reason="suy tu dong lenh (luat cu)", evt_id=e,
                      nguon="sua_tay")
    gt.ghi_but_toan(conn, chi_nap_that(), i, "hd", "HD-NGUOI",
                    actor="kt2@apero.vn", reason="go lai", force=True)
    assert conn.execute("SELECT adj_id FROM fls_sua_tay WHERE itl_id=%s"
                        " AND field='hd'", (i,)).fetchone()[0] != cu, \
        "⛔ không đo được: bút toán cũ ⛔ nằm DƯỚI giá trị người"

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")

    dao = [x for x in ra["but_toan_dao"] if x["dao_cua"] == cu]
    assert len(dao) == 1, f"⛔⛔ bút toán ghép cũ lớp dưới ⛔ bị đảo: {ra}"
    assert conn.execute("SELECT nguon FROM fls_adjustment WHERE reversal_of=%s",
                        (cu,)).fetchone()[0] == "sua_tay"
    assert dict(conn.execute("SELECT field, value_after FROM fls_sua_tay"
                             " WHERE itl_id=%s", (i,)).fetchall()) == \
        {"hd": "HD-NGUOI"}, "⛔⛔ bỏ ghép đã chạm giá trị NGƯỜI"
    assert [(x["field"], x["nguon"]) for x in ra["bo_qua"]] == [("hd", "sua_tay")]


# ═════════════════════════════ (f) `F-2` — `bo_qua` chỉ giá trị NGƯỜI
def test_bo_qua_moi_O_nhieu_nhat_MOT_muc_va_CHI_gia_tri_nguoi(conn):
    """`DT-I14` *Định nghĩa `bo_qua`*: mục = dòng `fls_sua_tay` ⛔ gắn `match`
    trên ô mà dòng **từng** có bút toán gắn `match`; mỗi ô ≤ 1 mục; mọi mục
    `nguon='sua_tay'`. Hai vòng ghép + người gõ `hd` ⇒ đúng **một** mục `hd`."""
    _run_id, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason=LY_DO)
    gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="ghep sai")
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason=LY_DO)
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-NGUOI", actor="kt2@apero.vn",
                    reason="go lai", force=True)
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-NGUOI-2", actor="kt2@apero.vn",
                    reason="go lai lan 2", force=True)
    ra = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="ghep sai lan 2")

    assert [(x["field"], x["nguon"], x["value_after"]) for x in ra["bo_qua"]] \
        == [("hd", "sua_tay", "HD-NGUOI-2")], ra["bo_qua"]
    dao_ids = {x["dao_cua"] for x in ra["but_toan_dao"]}
    assert not dao_ids & {x["adj_id"] for x in ra["bo_qua"]}, \
        "⛔⛔ một bút toán vừa đảo lại nằm trong bo_qua"
    assert "NGUOI" in ra["bo_qua"][0]["vi_sao"]


def test_bo_qua_KHONG_khai_o_ma_dong_CHUA_tung_co_goi_y(conn):
    """Người gõ `svc_start`… ⛔ phải ô ghép ⇒ ⛔ vào `bo_qua` *(định nghĩa:
    "trên ô mà dòng TỪNG có bút toán gắn `match`")*. Dùng `cdt1` khi cú ghép
    chỉ gợi ý `hd` *(dòng lệnh rỗng `cdt1`)*."""
    run = _run(conn)
    i = _dong_bank(conn, run, "5000000.00")
    ma = _ma()
    _lenh(conn, run, (ma, "5000000.00", "VND", "Approve", "HD-A", ""))
    pv = chi_nap_that()
    ra = gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR, reason=LY_DO)
    assert _goi_y(conn, i) == {"hd": "HD-A"}, f"⛔ không đo được: {ra}"
    gt.ghi_but_toan(conn, pv, i, "cdt1", "C-NGUOI", actor="kt2@apero.vn",
                    reason="go", force=True)
    rb = gt.bo_moi_noi(conn, pv, i, actor=ACTOR, reason="ghep sai")
    assert rb["bo_qua"] == [], rb["bo_qua"]


# ═════════════════════════════ (g) `F-3` — ghim ca TRỘN · AC-16
def test_ca_TRON_dong_rong_hd_va_dong_co_hd__goi_y_gia_tri_co(conn):
    """⭐ AC-16 — `DT-I14` nhánh `5a`: ô RỖNG = **⛔ lên tiếng**, ⛔ phải bất
    đồng ⇒ xử như *"đồng ý `v`"*. Mã đã vậy *(`may_ghep.suy_hd_cdt1`
    `gt.discard("")`)* — bài này **ghim**, ⛔ đổi mã."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    x, y = _ma(), _ma()
    _lenh(conn, run, (x, "60.00", "VND", "Approve", "", "C-1"),
          (y, "40.00", "VND", "Approve", "HD-Y", "C-1"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [x, y], actor=ACTOR, reason=LY_DO)

    assert "hd" not in ra["khong_suy_duoc"], ra
    assert _goi_y(conn, i) == {"hd": "HD-Y", "cdt1": "C-1"}
