# -*- coding: utf-8 -*-
"""`KQ-014` — kiểm `BG-013` / `WO-011`: thước *"người thật"* đo trên **ĐƯỜNG GHI
THẬT** và trên **MỌI điểm mã** của luật UAT.

⭐ Vì sao bài này tồn tại *(cái mà bài Dev ⛔ phủ)*:

  ⓐ Bài Dev chạy biến thể UAT trên **bảng mẫu gõ tay** *(CTE)*; qua **cửa ghi
    thật** chỉ một biến thể mỗi hướng. Ở đây **mọi** biến thể `AC-5` đi qua
    `ghep_lenh` + `bo_moi_noi` *(cả `B2/B3/B5` lẫn `B4`)* và `ghi_but_toan`
    *(`C8`)* — đo trên chính `reason` mà cửa ghi để lại trong kho.
  ⓑ Bài Dev ghim actor máy ở `B4` qua cửa ghi cho **3/9** actor ⇒ ở đây **9/9**.
  ⓒ ⭐ Hở *danh sách đen* *(`WO-011` Rủi ro 1)*: một tiến trình **máy mới chưa
    khai** ghi thật ⇒ phải **vừa** được đếm là người **vừa** bị gọi tên — đúng
    **một** dòng báo cho N thao tác.
  ⓓ ⭐ Luật UAT *"một luật, hai mặt"* *(`WO-011 T4`)* — Dev ghim **25** mẫu. Tôi
    quét **mọi** điểm mã Unicode *(kho THẬT, phiên `READ ONLY`, chỉ literal —
    `KQ-014` mục Logic)*: hai mặt **lệch 7.405 / 1.112.063** điểm mã ở vị trí
    *"ký tự sau `UAT`"* *(dấu kết hợp mang thuộc tính Alphabetic — `U+0345`,
    `U+0363`…`U+036F`, dấu Hebrew `U+05B0`…: `[[:alpha:]]` của `en_US.utf8`
    nhận là chữ, `str.isalpha()` ⛔)* — **mọi** lệch cùng một chiều: SQL nói
    *"người"*, Python nói *"UAT"*. Chiều ấy là chiều **ỒN** *(cổng nhích để có
    người nhìn)*. Bài này ghim **chiều**: mặt SQL *(cái cổng thật dùng)* ⛔ bao
    giờ gọi UAT một chuỗi mà luật Python gọi là người — chiều **IM** ⛔ được
    phép xuất hiện. Vị trí khoảng trắng đầu + ba chữ `U`/`A`/`T` phải **trùng**.

Mỗi bài chạy trong **một giao dịch rồi LÙI** *(kho TEST ⛔ phình — `11 §2`)*.
"""
from __future__ import annotations

import ast
import importlib.util
import pathlib
import sys

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import danh_muc_actor as dm
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _dong_bank, _mot_dong
from tools import kiem_so_song as kss

pytestmark = pytest.mark.pg

GOC = pathlib.Path(__file__).resolve().parents[2]
OWNER = "khanhcq@apero.vn"                 # ∈ ACTOR_DA_THAY ⇒ ⛔ bị gọi tên
NGUOI = "ke-toan-kq014@apero.vn"           # người mẫu — ⛔ thuộc sổ nào
MAY_MOI = "may-moi-chua-khai-kq014@fls"    # tiến trình máy MỚI, quên khai sổ
NEN = {"anh_chup": 1, "su_kien_cho_nguoi": 0, "moi_noi_da_bo": 0}
BANG = ("fls_queue_event", "fls_pm_unlink", "fls_adjustment", "fls_journal",
        "fls_sua_tay", "fls_may_goi_y")


@pytest.fixture()
def conn():
    c = psycopg.connect(dsn_test())
    try:
        yield c
    finally:
        c.rollback()
        c.close()


def _sql(khoa: str) -> str:
    """Chính chuỗi SQL của cổng *(đọc bằng `ast`, như `KQ-002`/`KQ-010`)*."""
    cay = ast.parse((GOC / "tools" / "kiem_so_song.py").read_text(encoding="utf-8"))
    tim = [v for n in ast.walk(cay) if isinstance(n, ast.Dict)
           for k, v in zip(n.keys, n.values)
           if isinstance(k, ast.Constant) and k.value == khoa]
    assert len(tim) == 1, f"⛔ không đo được: khoá `{khoa}` khớp {len(tim)} chỗ"
    v = tim[0]
    assert isinstance(v, ast.Call) and isinstance(v.args[0], ast.Constant), (
        f"⛔ không đo được: khuôn `dem(<chuỗi>)` của `{khoa}` đã đổi")
    return v.args[0].value


def _cte(*itl: int) -> str:
    ds = ", ".join(str(int(i)) for i in itl)
    return "WITH " + ", ".join(
        f"{b} AS (SELECT * FROM public.{b} WHERE itl_id IN ({ds}))" for b in BANG)


def _dem(conn, khoa: str, *itl: int) -> int:
    return int(conn.execute(_cte(*itl) + " " + _sql(khoa)).fetchone()[0])


def _moc(conn, *itl: int) -> tuple[str, str, str]:
    d = kss._cong_moc_b({**NEN,
                         "su_kien_cho_nguoi": _dem(conn, "su_kien_cho_nguoi", *itl),
                         "moi_noi_da_bo": _dem(conn, "moi_noi_da_bo", *itl)})
    return d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]


# ══ ⓐ biến thể UAT qua CỬA GHI THẬT — `B2/B3/B5` và `B4` ══════════════════
UAT = ["UAT 02/10 - thu", "uat 02/10 - thu", "  UAT 02/10", "UAT02/10",
       "Uat: thu duong ghi", " UAT 02/10 (dan tu trinh duyet)",
       "\tUAT 02/10", "UAT", "UAT_02", "UAT-02/10"]
NGUOI_LY_DO = ["ghi chú UAT 02/10", "UATX 02/10", "uất ức vì lệch tiền",
               "UATs dot 2", "doi chieu xong", None]


@pytest.mark.parametrize("ly_do", UAT)
def test_UAT_ghep_roi_bo_ghep_qua_cua_that__moc_B_DUNG(conn, ly_do):
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=OWNER, reason=ly_do)
    gt.bo_moi_noi(conn, pv, i, actor=OWNER, reason=ly_do)
    luu = [r[0] for r in conn.execute(
        "SELECT reason FROM fls_queue_event WHERE itl_id=%s ORDER BY evt_id",
        (i,)).fetchall()]
    assert len(luu) == 2, f"⛔ tập rỗng/sai — Đ3: {luu!r}"
    assert all(dm.la_uat(x) for x in luu), f"⛔ tiền đề: cửa ghi đổi lý do {luu!r}"
    assert conn.execute("SELECT count(*) FROM fls_pm_unlink WHERE itl_id=%s",
                        (i,)).fetchone()[0] == 1, "⛔ tập rỗng — Đ3"
    assert _dem(conn, "su_kien_cho_nguoi", i) == 0, f"UAT {ly_do!r} bị đếm là NGƯỜI"
    assert _dem(conn, "moi_noi_da_bo", i) == 0, f"UAT {ly_do!r} đóng `B4`"
    assert _moc(conn, i) == ("1", "1", "3")


@pytest.mark.parametrize("ly_do", NGUOI_LY_DO)
def test_NGUOI_ghep_roi_bo_ghep_qua_cua_that__moc_B_NHICH(conn, ly_do):
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=OWNER, reason=ly_do)
    gt.bo_moi_noi(conn, pv, i, actor=OWNER, reason=ly_do)
    assert _dem(conn, "su_kien_cho_nguoi", i) == 2, f"{ly_do!r} ⛔ được đếm là người"
    assert _dem(conn, "moi_noi_da_bo", i) == 1
    assert _moc(conn, i) == ("5", "0", "0")


# ══ ⓑ `B4` loại MỌI actor máy — 9/9 qua cửa ghi thật ══════════════════════
@pytest.mark.parametrize("may", sorted(dm.ACTOR_MAY))
def test_MAY_bo_ghep_qua_cua_that__B4_DUNG(conn, may):
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=may, reason="may thu")
    gt.bo_moi_noi(conn, pv, i, actor=may, reason="may bo thu")
    assert conn.execute("SELECT count(*) FROM fls_pm_unlink WHERE itl_id=%s",
                        (i,)).fetchone()[0] == 1, "⛔ tập rỗng — Đ3"
    assert _dem(conn, "moi_noi_da_bo", i) == 0, f"máy {may} đóng `B4`"
    assert _dem(conn, "su_kien_cho_nguoi", i) == 0
    assert kss.canh_actor_moi(
        conn.execute(_cte(i) + " " + kss._q_actor_moi()).fetchall()) == []


# ══ ⓒ máy MỚI quên khai sổ ⇒ ĐẾM là người VÀ bị GỌI TÊN đúng MỘT dòng ═════
def test_MAY_MOI_chua_khai__dem_la_NGUOI_va_bi_GOI_TEN_mot_dong(conn):
    pv = chi_nap_that()
    # ⚠ MỘT ảnh PM: hai `_mot_dong` trong cùng giao dịch mang cùng `read_at`
    #   (`now()`) ⇒ ảnh hiệu lực chọn theo `run_id` NGẪU NHIÊN ⇒ bài chập chờn.
    #   ⇒ dòng sổ thứ hai cùng lần nạp, ghép lại CÙNG dòng lệnh sau khi bỏ.
    run, i, ma = _mot_dong(conn)
    j = _dong_bank(conn, run, "5000000.00")
    gt.ghep_lenh(conn, pv, i, [ma], actor=MAY_MOI, reason="tu ghep dem")
    gt.bo_moi_noi(conn, pv, i, actor=MAY_MOI, reason="tu bo dem")
    gt.ghep_lenh(conn, pv, j, [ma], actor=MAY_MOI, reason="tu ghep dem")
    # ⓐ ⛔ loại khỏi phép đếm — hở danh sách đen phải làm mốc NHÍCH (ồn)
    assert _dem(conn, "su_kien_cho_nguoi", i, j) == 3
    assert _moc(conn, i, j) == ("5", "0", "0")
    # ⓑ gọi tên: MỘT dòng cho actor ấy, số = 3 thao tác *(⛔ số dòng bảng)*
    ds = conn.execute(_cte(i, j) + " " + kss._q_actor_moi()).fetchall()
    assert [(a, n) for a, n, _t in ds] == [(MAY_MOI, 3)], ds
    bao = kss.canh_actor_moi(ds)
    assert len(bao) == 1 and bao[0].startswith(f"⚠ ACTOR MỚI: {MAY_MOI} · 3"), bao


# ══ `C8` — sửa tay UAT / máy ⛔ lật; người lật — qua `ghi_but_toan` ═══════
def _khop_owner():
    sp = importlib.util.spec_from_file_location(
        "_khop_owner_kq014", GOC / "docs" / "ITL" / "_tools" / "khop_owner.py")
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    sp.loader.exec_module(m)
    return m


class _Boi:
    def __init__(self, conn, *itl: int) -> None:
        self.conn, self.itl = conn, itl

    def so(self, sql: str, ts=None) -> int:
        return int(self.conn.execute(_cte(*self.itl) + " " + sql, ts).fetchone()[0])


def test_C8_UAT_bien_the_va_MAY_trong_so_KHONG_lat__NGUOI_lat(conn):
    ko = _khop_owner()
    c8 = next(p for p in ko.PHEP if p.ma == "C8")
    pv = chi_nap_that()
    itl = [_mot_dong(conn)[1] for _ in range(4)]
    gt.ghi_but_toan(conn, pv, itl[0], "cdt1", "C-U1", actor=OWNER,
                    reason="Uat: thu sua tay")
    gt.ghi_but_toan(conn, pv, itl[1], "cdt1", "C-U2", actor=NGUOI,
                    reason=" UAT 02/10")
    gt.ghi_but_toan(conn, pv, itl[2], "cdt1", "C-M", actor=dm.ACTOR_NHIP,
                    reason="nhip sua")
    n = conn.execute("SELECT count(*) FROM fls_sua_tay WHERE itl_id = ANY(%s)",
                     (itl,)).fetchone()[0]
    assert n == 3, f"⛔ tập rỗng — Đ3 ({n})"
    k = c8.fn(_Boi(conn, *itl))
    assert k.khop is True and k.khop == c8.mong, k
    gt.ghi_but_toan(conn, pv, itl[3], "cdt1", "C-N", actor=NGUOI,
                    reason="UATX khong phai thu")
    k = c8.fn(_Boi(conn, *itl))
    assert k.khop is False and k.khop != c8.mong, k


# ══ ⓓ luật UAT trên MỌI điểm mã BMP — chiều lệch duy nhất được phép là ỒN ═
_CPS = [c for c in range(1, 0x10000) if not 0xD800 <= c <= 0xDFFF]
_MAU = {
    "sau":  ("'UAT' || chr(c) || 'x'", lambda ch: "UAT" + ch + "x"),
    "dau":  ("chr(c) || 'UAT 1'",       lambda ch: ch + "UAT 1"),
    "u":    ("chr(c) || 'AT 1'",        lambda ch: ch + "AT 1"),
    "a":    ("'U' || chr(c) || 'T 1'",  lambda ch: "U" + ch + "T 1"),
    "t":    ("'UA' || chr(c) || ' 1'",  lambda ch: "UA" + ch + " 1"),
}


@pytest.mark.parametrize("vi_tri", sorted(_MAU))
def test_luat_UAT_moi_diem_ma__SQL_khong_bao_gio_IM_hon_Python(conn, vi_tri):
    bt, py = _MAU[vi_tri]
    s_sql = {r[0] for r in conn.execute(
        "SELECT c FROM generate_series(1, 65535) c"
        " WHERE NOT (c BETWEEN 55296 AND 57343) AND "
        + dm.sql_la_uat("(" + bt + ")")).fetchall()}
    s_py = {c for c in _CPS if dm.la_uat(py(chr(c)))}
    assert s_py, "⛔ tập rỗng — Đ3"
    im = sorted(s_sql - s_py)
    assert not im, (f"⛔ SQL gọi UAT (⛔ đếm người) mà luật Python gọi NGƯỜI ở "
                    f"{len(im)} điểm mã: {[hex(c) for c in im[:20]]}")
    if vi_tri != "sau":
        # khoảng trắng đầu + ba chữ U/A/T: hai mặt phải TRÙNG
        assert s_sql == s_py, sorted(s_py - s_sql)[:20]


# ══ `B3`/`B4` của `khop_owner` — ảnh CŨ bẩn, ảnh HIỆU LỰC sạch ⇒ theo ảnh hiệu lực ═
#
# ⭐ Bài Dev `AC-7` đi chiều *"ảnh mới bẩn ⇒ NO"* — chiều ấy **cũng** xanh nếu
#   phép đếm trên MỌI ảnh *(ngoại lệ vẫn còn trong tổng)*. Và cột `kho` nay chỉ
#   mang quan hệ ⇒ khối ⛔ đổi dù đếm sai phạm vi. Chiều NGƯỢC mới phân biệt
#   được: một ngoại lệ đã **được sửa** ở ảnh mới thì `B4` phải ĐẠT lại.
class _BoiThang:
    def __init__(self, conn, ko) -> None:
        self.conn = conn
        self.bang = [v for v in vars(ko.db_schema).values()
                     if hasattr(v, "columns") and hasattr(v, "khau")
                     and hasattr(v, "name")]

    def so(self, sql: str, ts=None) -> int:
        return int(self.conn.execute(sql, ts).fetchone()[0])


def _anh(conn, giay: int, dong: list) -> str:
    import json
    import uuid
    r = "NAP-2000-01-01-PMK" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    for k, (pe, pi) in enumerate(dong):
        tho = {"ID PMLine": f"PK-{k}", **({"ID PELine": pe} if pe else {}),
               **({"ID PILine": pi} if pi else {})}
        conn.execute(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, curr,"
            " source_row, read_at, tho, pe_line, pi_line)"
            " SELECT %s, %s, 'PK', 'VND', %s,"
            "  greatest(now(), (SELECT max(read_at) FROM fls_pm_line))"
            "  + make_interval(secs => %s), %s::json, %s, %s",
            (r, f"PK-{k}", 3 + k, giay, json.dumps(tho), pe, pi))
    return r


def test_B3_B4_anh_CU_ban_anh_HIEU_LUC_sach__DAT_theo_anh_hieu_luc(conn):
    ko = _khop_owner()
    b3 = next(p for p in ko.PHEP if p.ma == "B3")
    b4 = next(p for p in ko.PHEP if p.ma == "B4")
    _anh(conn, 1, [("PE-1", "PI-1"), (None, None), ("PE-2", None)])   # bẩn
    k4 = b4.fn(_BoiThang(conn, ko))
    assert k4.khop is False and "2 ngoai le / 3" in k4.man, k4         # Đ3: bắt được
    r2 = _anh(conn, 2, [("PE-1", None), (None, "PI-1"), ("PE-2", None)])  # sạch
    k4 = b4.fn(_BoiThang(conn, ko))
    assert r2 in k4.man and "0 ngoai le / 3 " in k4.man, k4
    assert k4.khop is True and k4.khop == b4.mong, k4
    k3 = b3.fn(_BoiThang(conn, ko))
    assert r2 in k3.man and "3/3" in k3.man and k3.khop, k3
