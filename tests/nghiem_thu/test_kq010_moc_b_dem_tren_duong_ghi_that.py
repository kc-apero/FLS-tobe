"""`KQ-010` — cổng mốc `B` đo trên **ĐƯỜNG GHI THẬT**, ⛔ trên khuôn CTE gõ tay.

⭐ Vì sao bài này tồn tại *(kiểm `BG-009` / `WO-001`)*: chín bài của Dev ở
`tests/test_kiem_so_song.py` chạy **chính** câu SQL của cổng — đúng — nhưng trên
bảng **giả** mà Dev tự gõ từng dòng. Hai đột biến **lọt** qua cả chín bài
*(worktree, `KQ-010` mục Logic)*:

  · `M4` — `B4` lọc theo **ACTOR** *(`e.actor <> 'khanhcq@apero.vn'`)* thay vì
    theo **lý do** ⇒ `30 passed`. Đúng chiều `WO-001 T1b` cấm *("⛔ theo actor —
    owner là người thật, sẽ làm việc thật")*, và bài `B4` của Dev ⛔ bắt vì khuôn
    của nó đặt UAT ở `khanhcq` và người thật ở `ke-toan`.
  · `M5` — bỏ `coalesce` *(`reason not like 'UAT %'`)* ⇒ `30 passed`. Nhưng
    `ghi_tay.danh_dau_xong` ghi `reason = NULL` khi người bấm **Xong** ⛔ gõ lý do
    *(owner 28/08: "ko cần ghi lý do")* ⇒ `NULL NOT LIKE …` = `NULL` ⇒ cú bấm
    **người thật** biến mất khỏi mốc `B` **im lặng**.

⭐ Cách đo *(`11 §6`: "đo một QUAN HỆ thì gọi chính hàm thật")*: ghi bằng
**chính cửa ghi** của hệ *(`ghep_lenh` · `bo_moi_noi` · `danh_dau_xong` ·
`ghi_goi_y_may`)* trên **kho TEST**, rồi chạy **chính câu SQL** của cổng *(đọc bằng
`ast` từ `tools/kiem_so_song.py`)* với bảng thật bị **thu hẹp về đúng dòng của bài**
bằng một CTE cùng tên *(`WITH fls_queue_event AS (SELECT * FROM
public.fls_queue_event WHERE itl_id = …)`)* ⇒ rác của bài khác trong kho test
⛔ làm nhiễu, và cổng **⛔ đổi một chữ**. Cuối cùng đưa số đếm vào **chính**
`_cong_moc_b` trên nền sổ thật hôm nay *(chỉ `B1` đạt)*.
"""
from __future__ import annotations

import ast
import pathlib

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (_mot_dong,  # noqa: F401
                                                        conn)
from tools.kiem_so_song import _cong_moc_b

pytestmark = pytest.mark.pg

GOC = pathlib.Path(__file__).resolve().parents[2]
NGUOI = "ke-toan-kq010@apero.vn"
OWNER = "khanhcq@apero.vn"
# ⭐ Nền sổ thật 01/10 *(KQ-010 mục Dữ liệu)*: có ảnh PM ⇒ chỉ `B1` đạt.
NEN = {"anh_chup": 1, "su_kien_cho_nguoi": 0, "moi_noi_da_bo": 0}


def _sql(khoa: str) -> str:
    cay = ast.parse((GOC / "tools" / "kiem_so_song.py").read_text(encoding="utf-8"))
    tim = [v for n in ast.walk(cay) if isinstance(n, ast.Dict)
           for k, v in zip(n.keys, n.values)
           if isinstance(k, ast.Constant) and k.value == khoa]
    assert len(tim) == 1, f"⛔ không đo được: khoá `{khoa}` khớp {len(tim)} chỗ"
    v = tim[0]
    assert (isinstance(v, ast.Call) and v.args
            and isinstance(v.args[0], ast.Constant)), (
        f"⛔ không đo được: khuôn `dem(<chuỗi>)` của `{khoa}` đã đổi")
    return v.args[0].value


def _dem(conn, khoa: str, *itl: int) -> int:
    """Chạy câu của cổng, bảng thật thu về đúng các dòng sổ của bài."""
    ds = ", ".join(str(int(i)) for i in itl)
    cte = (f"WITH fls_queue_event AS (SELECT * FROM public.fls_queue_event"
           f" WHERE itl_id IN ({ds})),"
           f" fls_pm_unlink AS (SELECT * FROM public.fls_pm_unlink"
           f" WHERE itl_id IN ({ds})) ")
    return int(conn.execute(cte + _sql(khoa)).fetchone()[0])


def _moc(conn, *itl: int) -> tuple[str, str, str]:
    d = _cong_moc_b({**NEN,
                     "su_kien_cho_nguoi": _dem(conn, "su_kien_cho_nguoi", *itl),
                     "moi_noi_da_bo": _dem(conn, "moi_noi_da_bo", *itl)})
    return d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]


def test_NGUOI_ghep_KHONG_ly_do_thi_moc_B_NHICH_roi_bo_ghep_thi_B4_dong(conn):  # noqa: F811
    """Kịch bản ① — người thật bấm `Gán` ⛔ gõ lý do ⇒ máy điền `(may dien) …`
    *(`WO-003`)* ⇒ **vẫn là người** *(`AC-2b`)* ⇒ `B2`·`B3`·`B5` nhảy; bỏ ghép
    ⛔ lý do ⇒ `B4` đóng."""
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    assert _moc(conn, i) == ("1", "1", "3"), "⛔ nền sai — mẫu số rỗng?"
    gt.ghep_lenh(conn, pv, i, [ma], actor=NGUOI, reason=None)
    ly = conn.execute("SELECT reason FROM fls_queue_event WHERE itl_id=%s"
                      " AND evt_type='match'", (i,)).fetchone()[0]
    assert ly.startswith("(may dien)"), f"⛔ tiền đề kịch bản vỡ: reason={ly!r}"
    assert _dem(conn, "su_kien_cho_nguoi", i) == 1
    assert _moc(conn, i) == ("4", "1", "0")
    gt.bo_moi_noi(conn, pv, i, actor=NGUOI, reason=None)
    assert _dem(conn, "moi_noi_da_bo", i) == 1
    assert _moc(conn, i) == ("5", "0", "0")


def test_MAY_ghep_thi_moc_B_DUNG_YEN(conn):  # noqa: F811
    """Kịch bản ② — máy tự ghép *(`ghi_goi_y_may`, actor `MAY`)* ⇒ ⛔ nhích."""
    _r, i, ma = _mot_dong(conn)
    g = ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-M",
                                             "cdt1": "C-M"}])
    assert g["but_toan"], "⛔ tiền đề vỡ: máy ⛔ ghi sự kiện nào (tập rỗng — Đ3)"
    assert conn.execute("SELECT count(*) FROM fls_queue_event WHERE itl_id=%s",
                        (i,)).fetchone()[0] == 1
    assert _dem(conn, "su_kien_cho_nguoi", i) == 0
    assert _moc(conn, i) == ("1", "1", "3")


def test_UAT_ghep_roi_bo_ghep_thi_moc_B_DUNG_YEN(conn):  # noqa: F811
    """Kịch bản ③ — `QĐ-ITL-150 ⓐ`: dòng UAT ⛔ BAO GIỜ là người — kể cả `B4`."""
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=OWNER, reason="UAT 02/10 - thu duong ghi")
    gt.bo_moi_noi(conn, pv, i, actor=OWNER, reason="UAT 02/10 - hoan lai")
    assert conn.execute("SELECT count(*) FROM fls_pm_unlink WHERE itl_id=%s",
                        (i,)).fetchone()[0] == 1, "⛔ tập rỗng — Đ3"
    assert _dem(conn, "su_kien_cho_nguoi", i) == 0
    assert _dem(conn, "moi_noi_da_bo", i) == 0
    assert _moc(conn, i) == ("1", "1", "3")


def test_OWNER_bo_ghep_THAT_thi_B4_DEM__loc_theo_ly_do_khong_theo_actor(conn):  # noqa: F811
    """⛔ Bắt `M4` — `B4` lọc theo ACTOR thì cú bỏ ghép **thật** của owner mất."""
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=OWNER, reason="ghep that sau doi chieu")
    gt.bo_moi_noi(conn, pv, i, actor=OWNER, reason="ghep nham dong, tra lai")
    assert _dem(conn, "moi_noi_da_bo", i) == 1, (
        "⛔ cú bỏ ghép THẬT của owner ⛔ được đếm — B4 đang lọc theo actor")
    assert _dem(conn, "su_kien_cho_nguoi", i) == 2


def test_NGUOI_bam_XONG_khong_ly_do_reason_NULL_van_la_NGUOI(conn):  # noqa: F811
    """⛔ Bắt `M5` — `danh_dau_xong` ghi `reason = NULL`; bỏ `coalesce` thì cú
    bấm ấy rơi khỏi mốc `B` im lặng."""
    _r, i, _ma = _mot_dong(conn)
    gt.danh_dau_xong(conn, chi_nap_that(), i, actor=NGUOI, reason=None)
    ly = conn.execute("SELECT reason FROM fls_queue_event WHERE itl_id=%s"
                      " AND evt_type='done'", (i,)).fetchone()
    assert ly is not None and ly[0] is None, f"⛔ tiền đề vỡ: {ly!r}"
    assert _dem(conn, "su_kien_cho_nguoi", i) == 1, (
        "⛔ cú bấm Xong của NGƯỜI (reason NULL) ⛔ được đếm")
