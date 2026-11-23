# -*- coding: utf-8 -*-
"""`WO-011` — thước *"người thật"* đo trên **ĐƯỜNG GHI THẬT** của kho TEST.

⭐ Cùng khuôn bài nghiệm thu `KQ-010` *(`11 §6`: "đo một QUAN HỆ thì gọi chính
hàm thật")*: ghi bằng **chính cửa ghi** *(`ghep_lenh` · `bo_moi_noi` ·
`ghi_but_toan`)*, rồi chạy **chính câu SQL** của cổng với bảng thật bị **thu hẹp
về đúng dòng của bài** bằng một CTE cùng tên. ⭐ Khác `KQ-010`: mỗi bài chạy trong
**một giao dịch rồi LÙI** *(⛔ để lại dòng nào — kho test ⛔ phình, `11 §2`; và
ảnh PM của `AC-7` ⛔ được thành *"ảnh hiệu lực"* của bài khác)*.

Bốn nhóm, mỗi nhóm một `AC` của `WO-011`:
  · `AC-3` actor MỚI ⇒ đếm là người + gọi tên + NO; khai ⇒ im *(`T3`)*;
  · `AC-4` actor MÁY ⇒ mốc `B` đứng, kể cả `B4` *(`T2`, `T5`)*;
  · `AC-6` `khop_owner C8` ⛔ đếm sửa tay UAT / máy *(`T6 ⓐ`)*;
  · `AC-7` `khop_owner B3`/`B4` đếm trên **ảnh PM hiệu lực** *(`T6 ⓑⓒ`)*.
"""
from __future__ import annotations

import ast
import dataclasses
import importlib.util
import json
import pathlib
import sys
import uuid

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import danh_muc_actor as dm
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _mot_dong
from tools import kiem_so_song as kss

pytestmark = pytest.mark.pg

GOC = pathlib.Path(__file__).resolve().parents[2]
MOI = "nguoi-moi@apero.vn"
NGUOI = "ke-toan@apero.vn"            # người mẫu — ⛔ thuộc sổ nào (`HOI-012`)
OWNER = "khanhcq@apero.vn"            # `ACTOR_DA_THAY`
# ⭐ Nền sổ thật 01/10: có ảnh PM ⇒ chỉ `B1` đạt.
NEN = {"anh_chup": 1, "su_kien_cho_nguoi": 0, "moi_noi_da_bo": 0}


@pytest.fixture()
def conn():
    """⭐ Một giao dịch, LÙI ở cuối. Cửa ghi dùng `conn.transaction()` ⇒ điểm lưu."""
    c = psycopg.connect(dsn_test())
    try:
        yield c
    finally:
        c.rollback()
        c.close()


def _sql(khoa: str) -> str:
    """Chính chuỗi SQL của cổng — đọc bằng `ast`, như bài `KQ-010`."""
    cay = ast.parse((GOC / "tools" / "kiem_so_song.py").read_text(encoding="utf-8"))
    tim = [v for n in ast.walk(cay) if isinstance(n, ast.Dict)
           for k, v in zip(n.keys, n.values)
           if isinstance(k, ast.Constant) and k.value == khoa]
    assert len(tim) == 1 and isinstance(tim[0].args[0], ast.Constant)
    return tim[0].args[0].value


def _cte(*itl: int) -> str:
    ds = ", ".join(str(int(i)) for i in itl)
    return ", ".join(
        f"{b} AS (SELECT * FROM public.{b} WHERE itl_id IN ({ds}))"
        for b in ("fls_queue_event", "fls_pm_unlink", "fls_adjustment",
                  "fls_journal", "fls_sua_tay", "fls_may_goi_y"))


def _chay(conn, cau: str, *itl: int):
    return conn.execute("WITH " + _cte(*itl) + " " + cau).fetchall()


def _dem(conn, cau: str, *itl: int) -> int:
    return int(_chay(conn, cau, *itl)[0][0])


def _moc(conn, *itl: int, cau_nguoi: str | None = None) -> tuple[str, str, str]:
    d = kss._cong_moc_b({
        **NEN,
        "su_kien_cho_nguoi": _dem(conn, cau_nguoi or _sql("su_kien_cho_nguoi"), *itl),
        "moi_noi_da_bo": _dem(conn, _sql("moi_noi_da_bo"), *itl)})
    return d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]


# ══ `AC-3` — actor MỚI ═══════════════════════════════════════════════════════
def test_AC3_actor_MOI_dem_la_NGUOI__goi_ten__khai_DA_THAY_thi_im(conn, monkeypatch):
    """Chiều ĐỎ: bỏ dòng báo *(im lặng)* ⇒ ĐỎ; loại actor mới khỏi phép đếm ⇒ ĐỎ."""
    _r, i, ma = _mot_dong(conn)
    assert _moc(conn, i) == ("1", "1", "3"), "⛔ nền sai"
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=MOI, reason=None)

    # ⓐ vẫn được đếm là NGƯỜI ⇒ `B2`·`B3`·`B5` lật
    assert _dem(conn, _sql("su_kien_cho_nguoi"), i) == 1
    assert _moc(conn, i) == ("4", "1", "0")

    # ⓑ cổng GỌI TÊN — một dòng, đúng khuôn, số = 1 thao tác (⛔ 5 dòng bảng)
    ds = _chay(conn, kss._q_actor_moi(), i)
    assert [(a, n) for a, n, _t in ds] == [(MOI, 1)], ds
    bao = kss.canh_actor_moi(ds)
    assert len(bao) == 1 and bao[0].startswith(f"⚠ ACTOR MỚI: {MOI} · 1 dòng"), bao

    # ⓒ khai vào `ACTOR_DA_THAY` ⇒ dòng báo BIẾN MẤT, `B5` VẪN đạt
    monkeypatch.setattr(dm, "ACTOR_DA_THAY", dm.ACTOR_DA_THAY | {MOI})
    assert kss.canh_actor_moi(_chay(conn, kss._q_actor_moi(), i)) == []
    assert _moc(conn, i) == ("4", "1", "0")


def test_AC3_khai_actor_moi_vao_ACTOR_MAY_thi_B5_DUNG(conn):
    """Chiều máy: cùng cú ghép, nếu actor ấy được khai là MÁY ⇒ ⛔ người."""
    _r, i, ma = _mot_dong(conn)
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=MOI, reason=None)
    cau = _sql("su_kien_cho_nguoi")
    cu = dm.sql_ngoai_may("actor")
    assert cau.count(cu) == 1
    cau_may = cau.replace(cu, dm.sql_ngoai_may("actor", dm.ACTOR_MAY | {MOI}))
    assert _moc(conn, i, cau_nguoi=cau_may) == ("1", "1", "3")


def test_AC3_cong_NO_khi_co_actor_moi(monkeypatch, capsys):
    """Trạng thái **NO** của chính `main()` — đo bằng mã ra, ⛔ chữ."""
    monkeypatch.setattr(kss, "do_may", lambda: {
        "actor_moi": json.dumps([[MOI, 1, 5]]), "commit": "x"})
    monkeypatch.setattr(kss, "khai", lambda may, tl: [])
    assert kss.main([]) == 1
    ra = capsys.readouterr().out
    assert f"⚠ ACTOR MỚI: {MOI} · 1 dòng" in ra and "KHONG DAT" in ra
    monkeypatch.setattr(kss, "do_may", lambda: {"actor_moi": "[]", "commit": "x"})
    assert kss.main([]) == 0


# ══ `AC-4` — actor MÁY ═══════════════════════════════════════════════════════
@pytest.mark.parametrize("may", [dm.ACTOR_NHIP, dm.ACTOR_DUNG_LAI_SO,
                                 dm.ACTOR_VERIFY_SUA])
def test_AC4_MAY_ghep_roi_bo_ghep_thi_moc_B_DUNG_ca_B4(conn, may):
    """Chiều ĐỎ: bỏ vạch máy ở `B4` *(như trước `WO-011`)* ⇒ bài này ĐỎ."""
    _r, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=may, reason="may ghep thu")
    gt.bo_moi_noi(conn, pv, i, actor=may, reason="may bo ghep thu")
    assert conn.execute("SELECT count(*) FROM fls_pm_unlink WHERE itl_id=%s",
                        (i,)).fetchone()[0] == 1, "⛔ tập rỗng — Đ3"
    assert _dem(conn, _sql("su_kien_cho_nguoi"), i) == 0
    assert _dem(conn, _sql("moi_noi_da_bo"), i) == 0
    assert _moc(conn, i) == ("1", "1", "3")
    assert kss.canh_actor_moi(_chay(conn, kss._q_actor_moi(), i)) == []


# ══ `AC-6` — `khop_owner C8` ═════════════════════════════════════════════════
def _khop_owner():
    sp = importlib.util.spec_from_file_location(
        "_khop_owner_wo011", GOC / "docs" / "ITL" / "_tools" / "khop_owner.py")
    m = importlib.util.module_from_spec(sp)
    # ⚠ `@dataclass` tra `sys.modules[cls.__module__]` — phải đăng ký trước
    sys.modules[sp.name] = m
    sp.loader.exec_module(m)
    return m


class _BoiHep:
    """`Boi` của `khop_owner` thu về đúng các `itl_id` của bài *(⛔ đọc `.md`)*."""

    def __init__(self, conn, *itl: int) -> None:
        self.conn, self.itl = conn, itl

    def so(self, sql: str, ts=None) -> int:
        r = self.conn.execute("WITH " + _cte(*self.itl) + " " + sql, ts).fetchone()
        return int(r[0])


def test_AC6_C8_UAT_va_MAY_KHONG_lat__NGUOI_lat(conn):
    """Chiều ĐỎ: bỏ lọc UAT ⇒ bước ⓐ ĐỎ; bỏ lọc máy ⇒ bước ⓑ ĐỎ."""
    ko = _khop_owner()
    c8 = next(p for p in ko.PHEP if p.ma == "C8")
    pv = chi_nap_that()
    _r, a, _ = _mot_dong(conn)
    _r, b, _ = _mot_dong(conn)
    _r, c, _ = _mot_dong(conn)

    # ⓐ sửa tay UAT *(⛔ đảo)* — ba biến thể của MỘT luật
    gt.ghi_but_toan(conn, pv, a, "cdt1", "C-UAT", actor=OWNER,
                    reason="uat 02/10 - thu sua tay")
    gt.ghi_but_toan(conn, pv, a, "svc_start", "202410", actor=OWNER,
                    reason="  UAT02/10")
    # ⓑ sửa tay của MÁY *(công cụ đóng vai kế toán trên kho test)*
    gt.ghi_but_toan(conn, pv, b, "cdt1", "C-MAY", actor=dm.ACTOR_VERIFY_SUA,
                    reason="phan loai lai")
    assert conn.execute(
        "SELECT count(*) FROM fls_sua_tay WHERE itl_id IN (%s, %s)",
        (a, b)).fetchone()[0] == 3, "⛔ tập rỗng — Đ3"
    k = c8.fn(_BoiHep(conn, a, b, c))
    assert k.khop is True and k.khop == c8.mong, k

    # ⓒ một cú sửa tay của NGƯỜI ⇒ `C8` lật ⇒ `--kiem` CONG NO
    gt.ghi_but_toan(conn, pv, c, "cdt1", "C-NGUOI", actor=NGUOI,
                    reason="chot cdt1 sau doi chieu")
    k = c8.fn(_BoiHep(conn, a, b, c))
    assert k.khop is False and k.khop != c8.mong, k


# ══ `AC-7` — `khop_owner B3`/`B4` trên ẢNH PM HIỆU LỰC ══════════════════════
class _BoiThang:
    def __init__(self, conn, ko) -> None:
        self.conn = conn
        # ⭐ cùng phép trích bảng của `khop_owner.Boi` — ⛔ đọc `.md`
        self.bang = [v for v in vars(ko.db_schema).values()
                     if hasattr(v, "columns") and hasattr(v, "khau")
                     and hasattr(v, "name")]

    def so(self, sql: str, ts=None) -> int:
        return int(self.conn.execute(sql, ts).fetchone()[0])


def _anh(conn, giay: int, dong: list[tuple[str | None, str | None]]) -> str:
    """Một ảnh PM *(`run_id` hình THẬT)*, đọc **sau** mọi ảnh đang có `giay` giây."""
    r = "NAP-2000-01-01-PMW" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    for k, (pe, pi) in enumerate(dong):
        tho = {"ID PMLine": f"PW-{k}", **({"ID PELine": pe} if pe else {}),
               **({"ID PILine": pi} if pi else {})}
        conn.execute(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, curr,"
            " source_row, read_at, tho, pe_line, pi_line)"
            " SELECT %s, %s, 'PW', 'VND', %s,"
            "  greatest(now(), (SELECT max(read_at) FROM fls_pm_line))"
            "  + make_interval(secs => %s), %s::json, %s, %s",
            (r, f"PW-{k}", 3 + k, giay, json.dumps(tho), pe, pi))
    return r


def _khoi(ko, conn) -> tuple[str, dict]:
    ps = [dataclasses.replace(p) for p in ko.PHEP if p.ma in ("B3", "B4")]
    for p in ps:
        p.ket = p.fn(_BoiThang(conn, ko))
    return ko.bang_md(ps), {p.ma: p.ket for p in ps}


def test_AC7_anh_THU_HAI_cung_noi_dung__khoi_TRUNG_BYTE__ngoai_le_thi_NO(conn):
    """Chiều ĐỎ: đếm lại trên **mọi** ảnh ⇒ khối đổi ở ảnh thứ hai ⇒ ĐỎ."""
    ko = _khop_owner()
    goc = [("PE-1", None), ("PE-2", None), (None, "PI-1")]
    _anh(conn, 1, goc)
    khoi1, k1 = _khoi(ko, conn)
    assert k1["B3"].khop and k1["B4"].khop, k1
    assert "3/3" in k1["B3"].man and "0 ngoai le" in k1["B4"].man, k1

    _anh(conn, 2, goc)                                   # ảnh mới, CÙNG nội dung
    khoi2, k2 = _khoi(ko, conn)
    assert khoi2 == khoi1, "⛔ khối `SINH-KHOP` đổi chỉ vì một ảnh mới cùng nội dung"
    assert "3/3" in k2["B3"].man, k2

    _anh(conn, 3, goc + [("PE-9", "PI-9")])              # 1 dòng HAI cha
    _khoi3, k3 = _khoi(ko, conn)
    b4 = next(p for p in ko.PHEP if p.ma == "B4")
    assert k3["B4"].khop is False and k3["B4"].khop != b4.mong, k3
    assert "1 ngoai le" in k3["B4"].man, k3


class _BoiSo:
    """Trả lần lượt các số đã cho — đo **cả hai nhánh** của cột `kho`."""

    def __init__(self, *so: int) -> None:
        self.ds = list(so)

    def so(self, sql: str, ts=None) -> int:
        return self.ds.pop(0)


def test_T6c_C5b_khoi_chi_mang_QUAN_HE__so_ra_man(conn):
    """`T6 ⓒ` — `C5b` trôi theo ảnh Bank *(đo: `8.366` 01/10 ⇒ `8.370` 02/10,
    ⛔ ai làm gì)* ⇒ cột `kho` ⛔ được mang chữ số; số đi ra **màn**.
    Chiều ĐỎ: trả cột `kho` về `f"{co}/{tong} …"` ⇒ bài này ĐỎ."""
    ko = _khop_owner()
    c5b = next(p for p in ko.PHEP if p.ma == "C5b")
    _mot_dong(conn)                      # sổ ⛔ rỗng (Đ3)
    k = c5b.fn(_BoiThang(conn, ko))
    assert not any(ch.isdigit() for ch in k.kho), k.kho
    assert "/" in k.man and any(ch.isdigit() for ch in k.man), k.man
    # ⭐ cả hai nhánh — có chữ / ⛔ chữ — đều ⛔ mang số vào khối
    for co, tong in ((8370, 8387), (0, 8387)):
        k = c5b.fn(_BoiSo(co, tong))
        assert not any(ch.isdigit() for ch in k.kho), k.kho
        assert f"{co}/{tong}" in k.man, k.man
        assert k.khop is (co > 0)
