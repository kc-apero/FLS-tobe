# -*- coding: utf-8 -*-
"""`WO-018` `AC-3` — bất biến cặp `fls_journal.value_source = fls_adjustment.nguon`
trên **ĐỦ** các đường ghi đi qua `ghi_tay._them`.

⭐ Spec: `BA-05` **v0.34** `DD-I15 ⓓe` — *"`fls_journal.value_source` **=**
`fls_adjustment.nguon` của bút toán ghi **cùng giao dịch** trong `_them` — mọi
cặp, ⛔ ngoại lệ"*. `value_source` = **lớp của CHÍNH dòng** *(ai nói
`value_after`)*: người ⇒ `sua_tay`, máy ⇒ `may_goi_y`, bản đảo ⇒ lớp của
**dòng bị đảo**.

⛔⛔ **Vì sao phải có bài này** *(`HOI-016` ⓑ, đo 02/10)*: trước `WO-018` một cột
mang **hai nghĩa**. `ghi_goi_y` *(`ghi_tay.py` ~`:571`)* và `bo_moi_noi`
*(~`:973`)* ghi lớp của chính dòng; `ghi_but_toan` *(~`:446`)* ghi **nguồn TRƯỚC
khi gõ** *(`truoc_khi_go`: `UNMAPPED` · `nguon` · `may_goi_y` · `sua_tay`)*; và
`dao_but_toan` *(~`:480`)* ghi cứng `NGUON_TAY` cho **mọi** bản đảo — đảo một
gợi ý máy ⇒ bản đảo rơi vào lằn NGƯỜI *(`fls_adjustment.nguon='sua_tay'`)*.
Sổ thật 02/10: **4.428 / 4.428** cặp bằng nhau — chỉ vì **0** dòng nào đi qua
`/adjust` hay `dao_but_toan`. Cú gõ thật đầu tiên của kế toán sẽ là dòng sai
đầu tiên, nằm **vĩnh viễn** *(nhật ký chỉ-thêm `INV-I08`)*.

⭐ So **ĐA TẬP**, ⛔ nối khoá: `bo_moi_noi` đảo nhiều lớp `hd` trong **một** giao
dịch ⇒ các dòng ấy cùng `(itl_id, field, at, actor)` — nối khoá sẽ nhân cặp.

⚠ Cặp bằng nhau **chưa đủ** bắt lỗi `dao_but_toan`: mã cũ ghi `sua_tay` ở
**cả hai** bảng ⇒ cặp vẫn bằng. Bài thứ hai ghim điều `ⓓe` thật sự nói về bản
đảo: `nguon` của bản đảo **=** `nguon` của dòng bị đảo.
"""
from __future__ import annotations

import uuid
from collections import Counter
from decimal import Decimal as D

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _mot_dong, _run, conn  # noqa: F401

pytestmark = pytest.mark.pg

NGUOI = "ke-toan@apero.vn"
NGUOI_2 = "kt2@apero.vn"


def _dong(conn, run: str, *, hd: str | None = None,
          hd_thyt: str | None = None) -> int:
    """Một dòng sổ của lần nạp `run` — `hd` *(sổ gốc)* và `hd_thyt` *(cột gợi ý
    máy)* tuỳ chọn. ⛔ `UPDATE fls_itl` *(`INV-I08`)* ⇒ dựng bằng `INSERT`."""
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state,"
        " hd, hd_thyt)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-W18','VND',%s,'UNMAPPED','open',%s,%s) RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, D("1000000.00"),
         hd, hd_thyt)).fetchone()[0]


def _adj(conn, i: int, field: str, nguon: str) -> int:
    """adj_id **mới nhất** còn hiệu lực của lớp `nguon` trên ô."""
    r = conn.execute(
        "SELECT max(a.adj_id) FROM fls_adjustment a WHERE a.itl_id=%s"
        " AND a.field=%s AND a.nguon=%s AND a.reversal_of IS NULL"
        " AND NOT EXISTS (SELECT 1 FROM fls_adjustment d"
        "                  WHERE d.reversal_of=a.adj_id)",
        (i, field, nguon)).fetchone()[0]
    assert r is not None, f"⛔ không đo được: ô {i}/{field} ⛔ có lớp {nguon}"
    return r


@pytest.fixture()
def kich_ban(conn):  # noqa: F811
    """Đi qua **đủ** đường ghi; trả `(tap_itl, nhan)` — `nhan[itl_id]` = tên ca."""
    pv = chi_nap_that()
    nhan: dict[int, str] = {}

    # ① ghép TAY (`ghep_lenh` → `ghi_goi_y`, actor = người) · lớp máy
    #   (`ghi_goi_y_may`, actor = `may@fls`) · `dao_but_toan` một dòng
    #   `may_goi_y` · `bo_moi_noi` đảo các lớp còn lại.
    _r, i1, ma = _mot_dong(conn, hd="HD-W", cdt1="CDT-W")
    gt.ghep_lenh(conn, pv, i1, [ma], actor=NGUOI, reason="")
    ghi_goi_y_may(conn, itl_id=i1, lenh=[{"pm_line_id": ma, "hd": "HD-B",
                                          "cdt1": "C-2"}])
    gt.dao_but_toan(conn, pv, _adj(conn, i1, "hd", "may_goi_y"),
                    actor=NGUOI, reason="rut goi y may sai")
    gt.bo_moi_noi(conn, pv, i1, actor=NGUOI, reason="ghep nham")
    nhan[i1] = "ghép tay + máy + đảo dòng máy + bỏ ghép"

    run = _run(conn)
    # ② `ghi_but_toan` trên ô RỖNG cả ba lớp · rồi `dao_but_toan` dòng `sua_tay`
    i2 = _dong(conn, run)
    gt.ghi_but_toan(conn, pv, i2, "cdt1", "CDT-X", actor=NGUOI, reason="go")
    gt.dao_but_toan(conn, pv, _adj(conn, i2, "cdt1", "sua_tay"),
                    actor=NGUOI_2, reason="go nham")
    nhan[i2] = "ô rỗng + đảo dòng người"
    # ③ ô có NGUỒN sổ gốc
    i3 = _dong(conn, run, hd="HD-SO")
    gt.ghi_but_toan(conn, pv, i3, "hd", "HD-TOI", actor=NGUOI,
                    reason="PM xac nhan", force=True)
    nhan[i3] = "ô có nguồn sổ"
    # ④ ô có `*_thyt` *(ca xấu `HOI-016`)*
    i4 = _dong(conn, run, hd_thyt="HD-MAY")
    gt.ghi_but_toan(conn, pv, i4, "hd", "HD-NGUOI", actor=NGUOI,
                    reason="PM xac nhan", force=True)
    nhan[i4] = "ô có *_thyt"
    # ⑤ ô ĐÃ có người *(gõ lần hai đè lần một)*
    i5 = _dong(conn, run)
    gt.ghi_but_toan(conn, pv, i5, "hd", "HD-1", actor=NGUOI, reason="go")
    gt.ghi_but_toan(conn, pv, i5, "hd", "HD-2", actor=NGUOI_2, reason="go lai")
    nhan[i5] = "ô đã có người"
    return sorted(nhan), nhan


def _da_tap(conn, tap: list[int]) -> tuple[Counter, Counter]:
    nk = Counter(conn.execute(
        "SELECT itl_id, field, at, actor, value_source FROM fls_journal"
        " WHERE itl_id = ANY(%s)", (tap,)).fetchall())
    bt = Counter(conn.execute(
        "SELECT itl_id, field, at, actor, nguon FROM fls_adjustment"
        " WHERE itl_id = ANY(%s)", (tap,)).fetchall())
    return nk, bt


def test_AC3_da_tap_nhat_ky_BANG_da_tap_but_toan_tren_moi_duong_ghi(
        conn, kich_ban):  # noqa: F811
    """⭐⭐ Đa tập `(itl_id, field, at, actor, value_source)` của `fls_journal`
    **=** đa tập `(itl_id, field, at, actor, nguon)` của `fls_adjustment`.

    ⛔ Chiều ĐỎ *(chạy thật trên mã trước `WO-018`)*: `ghi_but_toan` ghi
    `value_source = t["value_source"]` ⇒ ca ②③④⑤ lệch *(`UNMAPPED` · `nguon` ·
    `may_goi_y` ⇔ `sua_tay`)* ⇒ ĐỎ.
    """
    tap, nhan = kich_ban
    nk, bt = _da_tap(conn, tap)
    n = sum(bt.values())
    print(f"\n[WO-018 AC-3] mẫu số: {n} cặp bút toán ⇔ {sum(nk.values())} "
          f"dòng nhật ký trên {len(tap)} dòng sổ")
    for i in tap:
        print(f"   itl_id {i} · {nhan[i]}: "
              f"{sum(v for k, v in bt.items() if k[0] == i)} bút toán")
    assert n >= 9, f"⛔ không đo được: mẫu số {n} < 9 (`Đ3`)"
    thieu = nk - bt
    du = bt - nk
    assert not thieu and not du, (
        "⛔⛔ nhật ký ⇔ bút toán lệch (`BA-05` v0.34 `DD-I15 ⓓe`):\n"
        f"   chỉ ở nhật ký: {sorted(thieu.elements(), key=str)}\n"
        f"   chỉ ở bút toán: {sorted(du.elements(), key=str)}")
    # ⭐ đủ đường: ca nào cũng có ít nhất một cặp
    assert {k[0] for k in bt} == set(tap), (set(tap) - {k[0] for k in bt})


def test_AC3_ban_dao_mang_NGUON_cua_dong_bi_dao__ca_dao_tay_lan_bo_ghep(
        conn, kich_ban):  # noqa: F811
    """⭐ `ⓓe`: *"Bản đảo ⇒ lớp của **dòng bị đảo**"* — mọi bản đảo trong kịch
    bản *(`dao_but_toan` + `bo_moi_noi`)*; nhật ký của bản đảo cũng mang lớp ấy.

    ⛔ Chiều ĐỎ: giữ `NGUON_TAY` cứng ở `dao_but_toan` ⇒ bản đảo dòng
    `may_goi_y` của ca ① mang `sua_tay` ⇒ ĐỎ *(cặp vẫn bằng — mã cũ ghi
    `sua_tay` ở cả hai bảng, nên bài trên ⛔ bắt được lỗi này)*.
    """
    tap, _nhan = kich_ban
    dao = conn.execute(
        "SELECT d.adj_id, d.itl_id, d.field, d.nguon, g.nguon, j.value_source,"
        "       d.evt_id IS NULL AS qua_cua_dao"
        "  FROM fls_adjustment d"
        "  JOIN fls_adjustment g ON g.adj_id = d.reversal_of"
        "  JOIN fls_journal j ON j.itl_id = d.itl_id AND j.field = d.field"
        "   AND j.at = d.at AND j.actor = d.actor AND j.value_after IS NULL"
        " WHERE d.itl_id = ANY(%s) ORDER BY d.adj_id", (tap,)).fetchall()
    # ⚠ một `adj_id` có thể nối ≥ 2 dòng nhật ký *(`bo_moi_noi` đảo hai lớp
    #   `cdt1` trong một giao dịch ⇒ cùng khoá)* ⇒ đếm theo `adj_id` riêng.
    loai = Counter((x[4], x[6]) for x in {x[0]: x for x in dao}.values())
    print(f"\n[WO-018 AC-3] bản đảo theo (lớp dòng bị đảo, qua dao_but_toan): "
          f"{dict(loai)}")
    # mẫu số: đủ HAI lớp đảo qua cửa đảo tay, và ≥ 1 bản đảo của bỏ ghép
    assert loai[("may_goi_y", True)] >= 1 and loai[("sua_tay", True)] >= 1, \
        f"⛔ không đo được: thiếu một lớp đảo qua `dao_but_toan` — {dict(loai)}"
    assert sum(v for (lop, tay), v in loai.items() if not tay) >= 1, \
        f"⛔ không đo được: ⛔ có bản đảo nào của `bo_moi_noi` — {dict(loai)}"
    sai = [x for x in dao if not (x[3] == x[4] == x[5])]
    assert sai == [], (
        "⛔⛔ bản đảo ⛔ mang lớp của dòng bị đảo "
        "(adj_id, itl_id, field, nguon bản đảo, nguon dòng gốc, "
        f"value_source nhật ký, qua cửa đảo): {sai}")


def test_them_NO_khi_value_source_KHAC_nguon__khong_ghi_dong_nao(conn):  # noqa: F811
    """⭐ Cửa ghi duy nhất cưỡng chế bất biến: ai truyền `value_source` ≠ `nguon`
    *(nghĩ theo nghĩa cũ "nguồn trước khi gõ")* ⇒ `LoiGhi`, **0** dòng ở cả
    hai bảng. Bỏ trống ⇒ lấy `nguon`.

    ⛔ Chiều ĐỎ: xoá phép so trong `_them` ⇒ ghi được cặp lệch ⇒ ĐỎ.
    """
    i = _dong(conn, _run(conn))
    with pytest.raises(gt.LoiGhi, match="value_source"):
        gt._them(conn, itl_id=i, field="hd", value_before=None,
                 value_after="HD-X", actor=NGUOI, value_source="UNMAPPED",
                 nguon="sua_tay", reason="nghia cu")
    dem = conn.execute(
        "SELECT (SELECT count(*) FROM fls_adjustment WHERE itl_id=%s),"
        "       (SELECT count(*) FROM fls_journal WHERE itl_id=%s)",
        (i, i)).fetchone()
    assert dem == (0, 0), f"⛔ cặp lệch bị NO mà vẫn để lại dòng: {dem}"
    gt._them(conn, itl_id=i, field="hd", value_before=None, value_after="HD-X",
             actor=NGUOI, nguon="may_goi_y", reason="bo trong value_source")
    assert conn.execute("SELECT value_source FROM fls_journal WHERE itl_id=%s",
                        (i,)).fetchall() == [("may_goi_y",)]
