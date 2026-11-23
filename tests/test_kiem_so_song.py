# -*- coding: utf-8 -*-
"""Phep thu cho cong so song (`tools/kiem_so_song.py`) — cong chung #13.

⛔ Cac bai nay kiem **phan LUAT** (phep so thuan) va **phan KHAI** (danh sach
muc), ⛔ KHONG kiem viec do that: do that can kho PostgreSQL + `git` + bo tai
lieu nam ngoai repo. Khai ra chu ⛔ khong de nguoi doc tu suy.

Cai chung chan:
  · mot mau khop 0 lan (van doi chu, mau vo) ma cong van XANH
  · mot mau khop nhieu lan ma cong tuong minh dang so voi dung mot cho
  · mot muc khai thieu/thua gia tri so voi so nhom cua mau
"""
from __future__ import annotations

import collections
import re

import pytest

from tools.kiem_so_song import Muc, kiem_mot, vn


# ─────────────────────────────────────────────────────── luat ⓐ: DUNG mot lan
def test_KHOP_DUNG_MOT_LAN_va_dung_so_thi_DAT():
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    assert kiem_mot("... `pg_verify` khớp 15 bảng/view ...", m) == []


def test_KHOP_dung_mot_lan_nhung_LECH_so_thi_DO():
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    loi = kiem_mot("khớp 14 bảng/view", m)
    assert len(loi) == 1
    assert "`14`" in loi[0] and "`15`" in loi[0] and "LỆCH" in loi[0]


def test_KHOP_KHONG_LAN_NAO_thi_DO_chu_KHONG_xanh():
    """⛔ Day la nhanh de bi bo qua nhat: mau vo thi 'khong thay loi'."""
    m = Muc("thu", "f.md", r"khớp (\d+) bảng/view", ("15",))
    loi = kiem_mot("cau van da doi, khong con chu nao khop", m)
    assert len(loi) == 1
    assert "khop 0 lan" in loi[0] and "khong do duoc" in loi[0]


def test_KHOP_HAI_LAN_thi_DO_vi_khong_biet_dang_so_voi_cho_nao():
    m = Muc("thu", "f.md", r"\*\*(\d+) kept\*\*", ("7",))
    loi = kiem_mot("**7 kept** ... roi noi khac lai **7 kept**", m)
    assert len(loi) == 1 and "khop 2 lan" in loi[0]


def test_MAU_NHIEU_NHOM_bao_dung_nhom_nao_lech():
    m = Muc("thu", "f.md", r"\*\*([\d.]+) mối nối\*\* \*\(([\d.]+) dòng\)\*",
            ("2.745", "2.427"))
    loi = kiem_mot("**2.745 mối nối** *(2.336 dòng)*", m)
    assert len(loi) == 1 and "nhom 2" in loi[0]
    assert kiem_mot("**2.745 mối nối** *(2.427 dòng)*", m) == []


def test_KHAI_THIEU_GIA_TRI_so_voi_so_nhom_thi_DO():
    """Mot muc khai 1 gia tri cho mau 2 nhom = loi cua NGUOI khai, phai DO."""
    m = Muc("thu", "f.md", r"(\d+) va (\d+)", ("1",))
    loi = kiem_mot("1 va 2", m)
    assert len(loi) == 1 and "nhom" in loi[0]


# ─────────────────────────────────────────────────────── dinh dang so kieu VN
@pytest.mark.parametrize("n,cho", [(0, "0"), (19, "19"), (1200, "1.200"),
                                   (10030, "10.030"), (1234567, "1.234.567")])
def test_dinh_dang_so_kieu_tai_lieu(n, cho):
    assert vn(n) == cho


# ─────────────────────────────────────────────────────── phan KHAI co lanh manh
def test_MOI_MAU_DICH_DUOC_va_so_nhom_khop_so_gia_tri_khai():
    """⛔ Khong chay duoc phep do that thi it nhat phai biet DANH SACH lanh.

    Bai nay chan mot lo that: sua mau ma quen sua so gia tri khai (hay nguoc
    lai) — luc do cong se DO voi ly do 'so nhom' tren MOI lan chay, tuc la
    khong con canh duoc gi.
    """
    from tools.kiem_so_song import khai

    # ⛔ Danh sach khoa CO Y ⛔ khong go tay: go tay thi bai nay do moi lan
    # cong them mot con so do duoc (da xay ra ngay trong buoi dung no —
    # `test_ngoai`). `defaultdict` de bai nay canh dung thu no sinh ra de canh:
    # mau vs so gia tri khai. Khoa go sai se no `KeyError` o lan chay THAT,
    # to va ngay lap tuc.
    may = collections.defaultdict(lambda: "0")

    class _Gia:
        """Tra version gia — bai nay ⛔ khong doc bo tai lieu that."""

        def __truediv__(self, _):
            return self

        def exists(self):
            return True

        def read_text(self, **_):
            return "**Version:** v9.9"

        # ⭐ Them 2026-08-28: `khai()` nay con DEM chinh bo tai lieu (so file
        # `.md` + so hien vat — xem `dem_bo_tai_lieu`). Bai nay ⛔ khong doc bo
        # that, nen tra so gia; no chi kiem MAU vs SO NHOM, ⛔ khong kiem gia tri.
        def is_dir(self):
            return True

        def rglob(self, _):
            return iter(range(99))

        def iterdir(self):
            return iter(range(9))

    muc = khai(may, _Gia())
    assert len(muc) >= 25, "danh sach phep so bi teo di"
    for m in muc:
        r = re.compile(m.mau)              # dich duoc, khong thi nem loi ngay
        assert r.groups == len(m.gia), (
            f"{m.ten}: mau co {r.groups} nhom nhung khai {len(m.gia)} gia tri")
        assert m.ten and m.file


# ── luat dem MOC `B` ────────────────────────────────────────────────────
from tools.kiem_so_song import _cong_moc_b  # noqa: E402

# ⭐ Kho **hom nay**: co dong lenh, ⛔ chua mot cu bam nao tren hang cho.
#
# ⚠ `su_kien_cho` = **moi** dong `fls_queue_event` *(MAY ghi cung vao day)*;
#   `su_kien_cho_nguoi` = chi loai `evt_type <> 'reason'` — xem `_cong_moc_b`.
KHO_NAY = {"anh_chup": 18791, "su_kien_cho": 0, "su_kien_cho_nguoi": 0,
           "moi_noi_da_bo": 0}


def test_moc_B_hom_nay_la_1_dat_1_nua_3_chua():
    d = _cong_moc_b(KHO_NAY)
    assert (d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]) == ("1", "1", "3")


def test_BO_TEST_XANH_khong_dong_duoc_mot_cong_nao():
    """⛔⛔⛔ **Day la ly do luat nay o trong MA.**

    Ngay 10/09 toi viet **ba bai** chung minh duong LUI cua mot LO chay duoc,
    va phan xa dau tien la ghi *"`B4` DAT"*. ⛔ Sai: bai thu chay tren kho
    TEST, con cong hoi *"duong LUI con nguyen"* tren so THAT — va tren so
    that `fls_pm_unlink` = **0**.

    ⇒ Ham nay ⛔ **khong nhan** mot tham so nao ve *"bo test"*, va do la co y:
      ⛔ khong co duong nao de mot bo test xanh doi duoc con so nay.
    """
    assert "test" not in str(_cong_moc_b.__code__.co_varnames)
    # Ma da chung minh nhung so that con `0` ⇒ `B4` la **MOT NUA**
    assert _cong_moc_b(KHO_NAY)["moc_b_nua"] == "1"


def test_MAY_ghi_93k_su_kien_ma_KHONG_dong_duoc_cong_nao():
    """⛔⛔⛔ **Ngay het han cua luat cu DA DEN — 10/09, va no da cắn thật.**

    Ban cu do `su_kien_cho` = `count(*) fls_queue_event`, voi tien de *"chi cua
    hang cho ghi vao day"*. `lo_nap` goi `ghi_ly_do()` cho moi dong bi CO ⇒
    **MAY cung ghi vao bang ay**. Cu dung lai so 10/09 ghi **93.666** su kien
    `reason` mang `actor = dung-lai-so@apero.vn`, va `B2`/`B3`/`B5` **lat sang
    XANH** trong khi ⛔ **0 cu bam cua nguoi**.

    ⇒ Bai nay ghim chieu sua: **so luong ⛔ khong quan trong**, `evt_type` moi
      quan trong. 93.666 su kien MAY phai dong duoc **0** cong.
    """
    d = _cong_moc_b({**KHO_NAY, "su_kien_cho": 93_666,
                     "su_kien_cho_nguoi": 0})
    assert (d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]) == ("1", "1", "3"), (
        "⛔ 93.666 su kien do MAY ghi vua dong duoc mot cong — dung cai loi "
        "ngay 10/09 da cắn: mot cong XANH ma ⛔ chua ai chung minh gi")


def test_MOT_cu_bam_NGUOI_that_lam_BA_cong_nhay():
    """⚠ Luat nay van **tho**, va no van khai ngay han cua chinh no.

    Giay phut `su_kien_cho_nguoi` len `1`, `B2`/`B3`/`B5` **cung nhay**, vi mot
    con so ⛔ khong phan biet duoc *mot vong day du* voi *mot cu bam le*. Bai
    nay ghim hanh vi ay **de no lo ra**, ⛔ khong phai de khen no.
    """
    d = _cong_moc_b({**KHO_NAY, "su_kien_cho_nguoi": 1})
    assert d["moc_b_dat"] == "4", (
        "⛔ neu con so nay ⛔ khong con la `4` thi luat da duoc siet — "
        "hay sua bai nay va bo dong 'ngay het han' trong docstring")


def test_bo_ghep_that_dong_not_B4():
    d = _cong_moc_b({**KHO_NAY, "moi_noi_da_bo": 1})
    assert (d["moc_b_dat"], d["moc_b_nua"]) == ("2", "0")


def test_KHO_RONG_thi_KHONG_cong_nao_dat():
    """⛔ Kho rong ⇒ `0` dat. *"Xanh tren tap rong la CHUA DO"*."""
    d = _cong_moc_b({})
    assert (d["moc_b_dat"], d["moc_b_chua"]) == ("0", "4")


def test_KHOA_SAI_TEN_thi_bai_nay_DO():
    """⛔⛔ Toi da viet `k.get("dong_lenh", 0)` — mot khoa **⛔ KHONG TON TAI**
    trong `kho` *(no chi co trong `khai()`, da qua `vn()` thanh chuoi)*.
    `.get(..., 0)` tra `0` **im lang** ⇒ `B1` bao **CHUA** trong khi no da
    dat. Mot `.get` co gia tri mac dinh la mot cho **xanh/do sai ma ⛔ khong
    ai thay**.

    ⇒ Bai nay ghim **dung ten khoa** ma `_cong_moc_b` doc.
    """
    assert _cong_moc_b({"anh_chup": 1})["moc_b_dat"] == "1"
    # ⛔ Ten cu (`dong_lenh`) ⛔ KHONG duoc lam `B1` dat
    assert _cong_moc_b({"dong_lenh": 18791})["moc_b_dat"] == "0"


# ══ ⭐⭐⭐ `WO-001` `T1a`·`T1b`·`T2` (01/10) — chay CHINH cau SQL cua cong ══
#
# ⛔⛔ **Vi sao cac bai tren ⛔ du.** Chung kiem `_cong_moc_b` — tuc LUAT dem tren
#    mot `dict` da dem san. Nhung cai da vo ngay 18/09 ⛔ phai luat: la **cau
#    SQL** do ra `su_kien_cho_nguoi`. `QĐ-ITL-143` cho may tu ghep ghi **2.219**
#    su kien `match` mang `actor='may@fls'` ⇒ `evt_type <> 'reason'` dem ca
#    chung ⇒ `B2`·`B3`·`B5` DAT tu 18/09 voi **0** ke toan bam *(`KQ-002 F-2`)*.
#    Mot bai chi dua `{"su_kien_cho_nguoi": 0}` vao luat thi ⛔ bao gio thay.
#
# ⭐ Cach do: lay **chinh chuoi SQL** trong `do_may()` *(doc bang `ast` — ⛔ chep
#   tay, cung cach bai nghiem thu `test_kq002_moc_b_khong_dem_may_la_nguoi.py`)*
#   roi chay no tren cac bang **gia bang CTE** *(che bang that cung ten — ⛔ ghi
#   gi, ke ca kho test)*.
import ast as _ast       # noqa: E402
import pathlib as _pl    # noqa: E402

from fls.repo.may_ghep import MAY as _MAY  # noqa: E402

_GOC = _pl.Path(__file__).resolve().parents[1]

# ⭐ Ly do UAT that tren kho 01/10 *(`evt 163561`/`163567`, `itl_id 27728`)* —
#   chep nguyen DAU chuoi de bai do dung hinh dang cua dong that.
_UAT_GHEP = "UAT 01/10 - thu duong ghi man ghep (khanhcq) · ghep 1 dong lenh"
_UAT_BO = "UAT 01/10 - hoan lai cu ghep thu · bo 1 moi noi (PM00338-1)"
# ⭐ Ly do MAC DINH `WO-003` dien khi nguoi bam ⛔ go — van la cu bam NGUOI.
_MAC_DINH = ("(may dien) ghep tren man - nguoi bam khong ghi ly do · "
             "ghep tay 1 dong lenh (X)")


def _L(x: str) -> str:
    """Hang chuoi SQL — ⛔ truyen tham so: cau cua cong duoc phep mang `%`."""
    return "'" + x.replace("'", "''") + "'"


def _sql_khoa(ten: str) -> str:
    cay = _ast.parse((_GOC / "tools" / "kiem_so_song.py").read_text(
        encoding="utf-8"))
    tim = [v for n in _ast.walk(cay) if isinstance(n, _ast.Dict)
           for k, v in zip(n.keys, n.values)
           if isinstance(k, _ast.Constant) and k.value == ten]
    assert len(tim) == 1, f"⛔ khong do duoc: khoa `{ten}` khop {len(tim)} cho"
    v = tim[0]
    assert (isinstance(v, _ast.Call) and v.args
            and isinstance(v.args[0], _ast.Constant)), (
        f"⛔ khong do duoc: khuon `dem(<chuoi>)` cua `{ten}` da doi")
    return v.args[0].value


def _chay_cte(cau: str, bang: dict[str, tuple[str, list[str]]]) -> tuple:
    """Chay `cau` voi moi bang trong `bang` bi che bang mot CTE cung ten.

    `bang[ten] = (khai_cot, [dong_sql, ...])` — `khai_cot` dang `"a, b, c"`,
    moi dong la mot bieu thuc `(...)` da ep kieu. ⛔ Ghi gi, ke ca kho test.
    """
    import psycopg

    from fls.db.kho import dsn_test

    cte = [f"{ten}({cot}) AS (VALUES {', '.join(dong)})"
           for ten, (cot, dong) in bang.items()]
    with psycopg.connect(dsn_test()) as c:
        return c.execute("WITH " + ", ".join(cte) + " " + cau).fetchone()


def _su_kien(*dong: tuple[str, str, str]) -> tuple[str, list[str]]:
    """`(evt_type, actor, reason)` → khuon `fls_queue_event` gia, `evt_id` tu 100."""
    return ("evt_id, itl_id, evt_type, reason, defer_until, actor, at",
            [f"({100 + i}::bigint, 1::bigint, {_L(loai)}::text, {_L(ly)}::text,"
             f" NULL::date, {_L(ai)}::text, now())"
             for i, (loai, ai, ly) in enumerate(dong)])


def _dem_nguoi(*dong: tuple[str, str, str]) -> int:
    return int(_chay_cte(_sql_khoa("su_kien_cho_nguoi"),
                         {"fls_queue_event": _su_kien(*dong)})[0])


@pytest.mark.pg
def test_T1a_su_kien_MATCH_cua_MAY_dem_0_nguoi():
    """`AC-1` chieu DO: mot `match` actor `MAY` ma dem thanh nguoi ⇒ DO."""
    assert _dem_nguoi(("match", _MAY, "may tu ghep 1 dong lenh (PM00001-1)"),
                      ("match", _MAY, "may tu ghep 2 dong lenh (PM00002-1)"),
                      ("reason", "dung-lai-so@apero.vn", "S7 · dong trung")) == 0


@pytest.mark.pg
def test_T1a_MAY_ghi_match_ma_KHONG_dong_duoc_cong_nao():
    """⭐ `AC-1` — mo rong `test_MAY_ghi_93k_…` sang su kien `match` cua MAY.

    Bai `test_MAY_ghi_93k_…` o tren dua thang `su_kien_cho_nguoi: 0` vao luat,
    nen no ⛔ bao gio thay cau SQL dem sai. Bai nay dem bang **chinh cau SQL**
    tren khuon co `match` cua MAY + `reason` cua may, roi dua ket qua vao luat:
    moc B phai giu `1 · 1 · 3`.
    """
    n = _dem_nguoi(("match", _MAY, "may tu ghep 1 dong lenh (PM00001-1)"),
                   ("reason", "dung-lai-so@apero.vn", "S2 · co tien"))
    d = _cong_moc_b({**KHO_NAY, "su_kien_cho": 2, "su_kien_cho_nguoi": n})
    assert (d["moc_b_dat"], d["moc_b_nua"], d["moc_b_chua"]) == ("1", "1", "3"), (
        f"⛔ mot su kien `match` cua MAY (`{_MAY}`) vua dong cong — "
        "dung loi `KQ-002 F-2`")


@pytest.mark.pg
def test_T1b_dong_UAT_dem_0_nguoi():
    """`QĐ-ITL-150 ⓐ`: UAT ⛔ BAO GIO tinh la nguoi that."""
    assert _dem_nguoi(("match", "khanhcq@apero.vn", _UAT_GHEP),
                      ("unmatch", "khanhcq@apero.vn", _UAT_BO)) == 0


@pytest.mark.pg
def test_T1b_ly_do_MAC_DINH_may_dien_van_la_NGUOI():
    """`AC-2b` — loc `reason LIKE '(%'` ⇒ bai nay DO."""
    assert _dem_nguoi(("match", "ke-toan@apero.vn", _MAC_DINH)) == 1


@pytest.mark.pg
def test_T1b_loc_theo_LY_DO_khong_theo_ACTOR():
    """`AC-2b` + `AC-2` chieu DO — loc theo actor `khanhcq@%` ⇒ bai nay DO.

    Owner la mot NGUOI that: ngay owner ghep that *(ly do ⛔ bat dau `UAT `)*
    thi cu bam ay phai dem. Loc theo actor ⇒ cong mu voi chinh owner.
    """
    assert _dem_nguoi(("match", "khanhcq@apero.vn",
                       "ghep that sau khi doi chieu sao ke")) == 1


@pytest.mark.pg
def test_T1b_UAT_phai_o_DAU_ly_do():
    """⛔ `reason LIKE '%UAT%'` qua rong: mot ly do NHAC toi UAT ⛔ phai UAT."""
    assert _dem_nguoi(("match", "ke-toan@apero.vn",
                       "ghep lai dong da thu o buoi UAT 01/10")) == 1


def test_T1a_cau_SQL_mang_DUNG_hang_MAY():
    """⭐ Rui ro 2 cua `WO-001`: hang actor may khai **MOT cho**.

    Cau SQL phai la mot chuoi THUAN *(bai nghiem thu doc no bang `ast`)*, nen no
    ⛔ noi duoc bien `MAY`. ⇒ Ghim: chuoi ay phai mang **dung** `'{MAY}'`, va
    `do_may()` cung tu kiem dieu nay luc chay *(doi `MAY` ma quen cau ⇒ ca hai
    cung DO)*.
    """
    from tools.kiem_so_song import _kiem_hang_may

    assert f"'{_MAY}'" in _sql_khoa("su_kien_cho_nguoi")
    _kiem_hang_may(_sql_khoa("su_kien_cho_nguoi"))
    with pytest.raises(SystemExit, match="MAY"):
        _kiem_hang_may("select count(*) from fls_queue_event"
                       " where actor <> 'may@cu'")


def _bo_ghep(*dong: tuple[int, int]) -> tuple[str, list[str]]:
    """`(unlink_id, evt_id)` → khuon `fls_pm_unlink` gia."""
    return ("unlink_id, link_id, itl_id, evt_id, at",
            [f"({u}::bigint, {u}::bigint, 1::bigint, {e}::bigint, now())"
             for u, e in dong])


@pytest.mark.pg
def test_T1b_bo_ghep_UAT_KHONG_dong_not_B4():
    """`B4` dem `fls_pm_unlink` — dong UAT *(`unlink 163568` → `evt 163567`)*
    ⛔ duoc dong `B4`; mot cu bo ghep NGUOI that thi phai dem."""
    sk = _su_kien(("unmatch", "khanhcq@apero.vn", _UAT_BO),     # evt 100
                  ("unmatch", "ke-toan@apero.vn", "tra lai"))   # evt 101
    cau = _sql_khoa("moi_noi_da_bo")
    assert int(_chay_cte(cau, {"fls_pm_unlink": _bo_ghep((1, 100)),
                               "fls_queue_event": sk})[0]) == 0
    assert int(_chay_cte(cau, {"fls_pm_unlink": _bo_ghep((1, 100), (2, 101)),
                               "fls_queue_event": sk})[0]) == 1


@pytest.mark.pg
def test_T2_dau_SO_la_luot_nap_SO_khong_phai_anh_PM():
    """`AC-3` — luot `fls_run` PM moi hon luot so ⛔ duoc doi dau so.

    Kho that 01/10: luot moi nhat la anh PM *(`NAP-2026-10-01-PM…`, 0 dong
    `fls_itl`)* ⇒ dau cu in `01/10 18:20` canh cau *"8.387 dong so (ban sao
    nap …)"* — trong khi so nap lan cuoi **10/09**.
    """
    from tools.kiem_so_song import _Q_GIO

    run = ("run_id, started_at",
           ["('NAP-2026-09-10-BU1'::text, '2026-09-10 11:54:50+00'::timestamptz)",
            "('NAP-2026-10-01-PMX'::text, '2026-10-01 11:20:53+00'::timestamptz)"])
    itl = ("itl_id, run_id", ["(1::bigint, 'NAP-2026-09-10-BU1'::text)"])
    pm = ("read_at", ["('2026-10-01 11:20:00+00'::timestamptz)"])
    so, anh = _chay_cte(_Q_GIO, {"fls_run": run, "fls_itl": itl,
                                 "fls_pm_line": pm})
    import datetime as _dt
    utc = _dt.timezone.utc
    assert so == _dt.datetime(2026, 9, 10, 11, 54, 50, tzinfo=utc), (
        f"⛔ dau so = {so} — dang lay luot nap BAT KY (anh PM), ⛔ luot nap SO")
    # ⭐ Dau anh PM `dau_anh` GIU NGUYEN (`WO-001 T2`)
    assert anh == _dt.datetime(2026, 10, 1, 11, 20, 0, tzinfo=utc)


# ══ ⭐⭐⭐ `WO-011` `T2`·`T3`·`T4`·`T5`·`T7` (02/10) — sổ actor + UAT một luật ══
#
# ⛔⛔ **Vì sao các bài `T1a`/`T1b` ở trên ⛔ đủ.** Chúng ghim **một** actor máy
#    (`may@fls`) và **một** dạng UAT (`'UAT '`). Đo 01/10 khuya: mã có **8**
#    actor ⛔ phải người *(nay **9** — `HOI-012`)*; UAT gõ `'uat …'`, `' UAT …'`,
#    `'UAT02/10'` thì tính là người *(`KQ-010 F-2`)*. Lần vỡ thứ tư chỉ cần MỘT
#    tiến trình máy mới.
# ⭐ Các bài dưới chạy **chính** câu SQL của cổng *(đọc bằng `ast`)* trên khuôn
#   CTE, lặp qua **cả sổ** — ⛔ gõ lại danh sách trong bài.
from fls.repo import danh_muc_actor as _dm  # noqa: E402

# ⭐ actor người mẫu của các bài — ⛔ thuộc sổ nào *(`HOI-012` câu 1)*
_NGUOI = "ke-toan@apero.vn"


def _su_kien_ly(*dong: tuple[str, str, str | None]) -> tuple[str, list[str]]:
    """Như `_su_kien` nhưng `reason` được phép `None` *(cú `Xong` ⛔ lý do)*."""
    return ("evt_id, itl_id, evt_type, reason, defer_until, actor, at",
            [f"({100 + i}::bigint, 1::bigint, {_L(loai)}::text,"
             f" {'NULL' if ly is None else _L(ly)}::text,"
             f" NULL::date, {_L(ai)}::text, now())"
             for i, (loai, ai, ly) in enumerate(dong)])


@pytest.mark.pg
@pytest.mark.parametrize("may", sorted(_dm.ACTOR_MAY))
def test_T2_MOI_actor_may_trong_SO_dem_0_nguoi(may):
    """`AC-4` — sự kiện `match` của **bất kỳ** actor ∈ `ACTOR_MAY` ⇒ 0 người.

    Chiều ĐỎ: câu cũ *(chỉ `'may@fls'`)* ⇒ 8/9 tham số ĐỎ.
    """
    n = int(_chay_cte(_sql_khoa("su_kien_cho_nguoi"), {
        "fls_queue_event": _su_kien_ly(("match", may, "ghep 1 dong lenh"))})[0])
    assert n == 0, f"⛔ `{may}` (máy) được đếm là NGƯỜI"


@pytest.mark.pg
@pytest.mark.parametrize("ly", [x for x, _m in
                                __import__("tests.repo.test_danh_muc_actor",
                                           fromlist=["BANG_UAT"]).BANG_UAT])
def test_T4_UAT_MOT_luat__cau_cong_TRUNG_la_uat(ly):
    """`AC-5` — cổng `B2`/`B3`/`B5` loại đúng những dòng `la_uat` nói là UAT;
    ⛔ loại dòng nào khác *(`(may dien)`, `'ghi chú UAT'`, `'UATX'`, `NULL`)*."""
    n = int(_chay_cte(_sql_khoa("su_kien_cho_nguoi"), {
        "fls_queue_event": _su_kien_ly(("match", _NGUOI, ly))})[0])
    assert n == (0 if _dm.la_uat(ly) else 1), (
        f"⛔ reason={ly!r}: cổng đếm {n}, luật `la_uat` nói "
        f"{'UAT' if _dm.la_uat(ly) else 'người'}")


def _bo_ghep_ly(*dong: tuple[str, str | None]) -> tuple[dict, int]:
    """`(actor, reason)` của sự kiện `unmatch` → khuôn hai bảng + số dòng."""
    sk = _su_kien_ly(*[("unmatch", ai, ly) for ai, ly in dong])
    return ({"fls_pm_unlink": _bo_ghep(*[(i + 1, 100 + i)
                                         for i in range(len(dong))]),
             "fls_queue_event": sk}, len(dong))


@pytest.mark.pg
@pytest.mark.parametrize("may", sorted(_dm.ACTOR_MAY))
def test_T5_B4_bo_ghep_cua_MAY_dem_0(may):
    """`AC-4` — `B4` **đối xứng** `B2`/`B3`/`B5`: cú bỏ ghép actor máy ⇒ 0.

    Chiều ĐỎ: bỏ vạch máy ở `B4` *(như trước `WO-011`)* ⇒ ĐỎ.
    """
    bang, _ = _bo_ghep_ly((may, "may tu bo ghep"))
    assert int(_chay_cte(_sql_khoa("moi_noi_da_bo"), bang)[0]) == 0


@pytest.mark.pg
def test_T5_B4_UAT_MOT_luat_va_NGUOI_null_van_dem():
    bang, _ = _bo_ghep_ly((_NGUOI, "uat 02/10 - hoan lai"),
                          (_NGUOI, "  UAT02/10"),
                          (_NGUOI, None),                  # người ⛔ lý do
                          (_NGUOI, "ghi chú UAT 02/10"))   # người
    assert int(_chay_cte(_sql_khoa("moi_noi_da_bo"), bang)[0]) == 2


def test_T2_cau_SQL_mang_DUNG_ban_sinh_tu_SO():
    """`HOI-012` câu 2 — câu SQL **thuần** *(bài nghiệm thu đọc bằng `ast`)*
    mang bản chép; bản chép phải **trùng byte** mẩu sinh từ sổ. Sổ đổi mà câu
    ⛔ đổi ⇒ cổng nổ `⛔ khong do duoc` ngay lần chạy."""
    from tools.kiem_so_song import _kiem_hang_may

    for khoa, tt in (("su_kien_cho_nguoi", ""), ("moi_noi_da_bo", "e.")):
        cau = _sql_khoa(khoa)
        assert _dm.sql_ngoai_may(tt + "actor") in cau, khoa
        assert _dm.sql_khong_uat(tt + "reason") in cau, khoa
        assert "left(" not in cau, f"⛔ `{khoa}` còn luật UAT cũ `left(…, 4)`"
        _kiem_hang_may(cau, tt)
    # ⭐ chiều ĐỎ: sổ thêm một máy mà câu ⛔ theo ⇒ NỔ
    them = _dm.ACTOR_MAY | {"may-moi@fls"}
    with pytest.raises(SystemExit, match="MAY"):
        _kiem_hang_may(_sql_khoa("su_kien_cho_nguoi"), "", may=them)


# ── `T3` — actor MỚI ⇒ gọi tên, NO một lần ─────────────────────────────────
def test_T3_canh_actor_moi_GOI_TEN_dung_khuon():
    from tools.kiem_so_song import canh_actor_moi

    assert canh_actor_moi([]) == []
    ra = canh_actor_moi([("nguoi-moi@apero.vn", 1, 5)])
    assert len(ra) == 1 and ra[0].startswith(
        "⚠ ACTOR MỚI: nguoi-moi@apero.vn · 1 dòng"), ra


@pytest.mark.pg
def test_T3_cau_actor_moi_DEM_tren_3_bang_va_BO_actor_trong_so():
    """Câu của cổng chạy trên khuôn CTE: actor trong `ACTOR_MAY ∪ ACTOR_DA_THAY`
    ⛔ hiện; actor lạ hiện với số **thao tác** *(sự kiện + bút toán gõ thẳng —
    bút toán theo sự kiện và nhật ký ⛔ cộng thêm)*."""
    from tools.kiem_so_song import _q_actor_moi

    sk = _su_kien_ly(("match", "nguoi-moi@apero.vn", "ghep"),
                     ("match", "may@fls", "may"),
                     ("unmatch", "khanhcq@apero.vn", "that"))
    adj = ("adj_id, itl_id, field, actor, evt_id",
           ["(1::bigint, 1::bigint, 'hd'::text, 'nguoi-moi@apero.vn'::text, 100::bigint)",
            "(2::bigint, 1::bigint, 'hd'::text, 'go-thang@apero.vn'::text, NULL::bigint)"])
    jr = ("jrn_id, itl_id, field, actor",
          ["(3::bigint, 1::bigint, 'hd'::text, 'nguoi-moi@apero.vn'::text)",
           "(4::bigint, 1::bigint, 'hd'::text, 'go-thang@apero.vn'::text)"])
    import psycopg

    from fls.db.kho import dsn_test
    cte = [f"{t}({c}) AS (VALUES {', '.join(d)})" for t, (c, d) in
           (("fls_queue_event", sk), ("fls_adjustment", adj), ("fls_journal", jr))]
    with psycopg.connect(dsn_test()) as c:
        kq = c.execute("WITH " + ", ".join(cte) + " " + _q_actor_moi()).fetchall()
    assert [tuple(x) for x in kq] == [("go-thang@apero.vn", 1, 2),
                                      ("nguoi-moi@apero.vn", 1, 3)], kq


# ── `T7` — phép so cho `09` §7 dòng `B` (cổng chung #13) ─────────────────────
def test_T7_phep_so_09_muc7_dong_B_CO_va_khop_DUNG_mot_lan():
    """`AC-8` — ba số `58,1%` · `1.601` · `826` có **một** phép so.

    Chiều ĐỎ: sửa `58,1%` ⇒ `58,2%` trong `09` ⇒ phép ĐỎ *(đo trên bản sao chữ)*.
    """
    from tools.kiem_so_song import MOC, TAI_LIEU_MAC_DINH, khai

    may = collections.defaultdict(lambda: "0")
    muc = [m for m in khai(may, TAI_LIEU_MAC_DINH)
           if m.ten == "mốc · §7 dòng B · phía PM"]
    assert len(muc) == 1, "⛔ thiếu phép so `09` §7 dòng `B`"
    m = muc[0]
    assert m.file == MOC
    chu = (TAI_LIEU_MAC_DINH / MOC).read_text(encoding="utf-8")
    khop = list(re.finditer(m.mau, chu))
    assert len(khop) == 1, f"⛔ mẫu khớp {len(khop)} lần trong `09`"
    ty, ranh, phieu = khop[0].groups()
    ok = Muc(m.ten, m.file, m.mau, (ty, ranh, phieu))
    assert kiem_mot(chu, ok) == []
    sai = chu.replace(f"**{ty}%** dòng lệnh đã có tiền",
                      "**99,9%** dòng lệnh đã có tiền")
    assert sai != chu
    loi = kiem_mot(sai, ok)
    assert len(loi) == 1 and "nhom 1" in loi[0] and "LỆCH" in loi[0], loi
