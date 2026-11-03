"""⛔ CONG `GAP-API-05`: ban khai cua bang tuyen phai KHOP SQL that.

⛔⛔ **Vi sao cong nay ton tai — bang chung, ⛔ khong phai lo xa.** Ngay `03/09`
mot agent kiem doc lap soi 17 tuyen va bat duoc **4 tuyen khai thieu bang**;
nang nhat la `GET /ledger/{itl_id}` khai **2** bang trong khi SQL doc **8**.
`kiem_bang_tuyen` — **cong lon nhat cua `P4`** — van **XANH** suot thoi gian do,
vi no doc `Tuyen.bang` *(nguoi go)* chu ⛔ khong doc cau SQL *(o tep khac)*.

★ Do la "cong xanh vi ⛔ khong do dung thu can do" — luat so mot cua du an.

⚠ Bai o day kiem **ca hai chieu**: cong phai XANH tren bang that, va phai **DO**
khi bi pha co chu dich. Mot cong chua tung thay do la mot cong chua biet co song.
"""
from __future__ import annotations

import re

import pytest

from fls.api import bang_tuyen
from fls.api.bang_tuyen import Tuyen
from tools import soi_bang_tuyen as sbt


# ── ⓐ cong XANH tren bang that ────────────────────────────────────────────
def test_ban_khai_that_KHOP_sql_that():
    loi, _ = sbt.soi()
    assert loi == [], "⛔ ban khai lech SQL:\n  - " + "\n  - ".join(loi)


def test_soi_het_moi_tuyen_khong_bo_sot():
    _, do = sbt.soi()
    assert len(do) == len(bang_tuyen.BANG_TUYEN)


# ── ⓑ ⛔⛔ phep do PHAI thuc su doc duoc, ⛔ khong tra rong ────────────────
#
# Neu `sql_cua_tuyen` tra rong voi moi thu thi bai ⓐ xanh **vi ⛔ khong do duoc
# gi**, ⛔ khong phai vi sach. Do dung la loi ma cong nay sinh ra de chan.
@pytest.mark.parametrize("ham,phai_co", [
    ("cong", {"fls_itl", "fls_moi_noi", "fls_run"}),
    ("mot_dong", {"fls_itl", "fls_pm_link", "fls_sua_tay"}),
    ("hang_cho", {"fls_itl", "fls_da_xong"}),
    ("do_phu", {"fls_itl", "fls_da_xong"}),
    ("ghep", {"fls_pm_link", "fls_pm_line"}),
])
def test_phep_do_that_su_bam_duoc_sang_tang_kho(ham, phai_co):
    cham, _, vet = sbt.sql_cua_tuyen(ham)
    assert phai_co <= cham, f"⛔ {ham}: thieu {sorted(phai_co - cham)}"
    assert any(v.startswith("fls.repo.") for v in vet), (
        f"⛔ {ham}: do thi goi ⛔ khong sang duoc tang kho — vet={vet}")


def test_phep_do_bat_duoc_ca_phep_GHI():
    _, ghi, _ = sbt.sql_cua_tuyen("sua")
    assert {"fls_adjustment", "fls_journal"} <= ghi


def test_khong_tuyen_nao_GHI_that_vao_so():
    """⭐⭐ Phep kiem ma cong cu ⛔ KHONG THE lam: no chi doc duoc dong KHAI.

    Mot cau `INSERT INTO fls_itl` that ma nguoi viet quen sua dong khai thi
    `kiem_bang_tuyen` **im**, va `INV-I08` bi pha trong im lang.
    """
    for t in bang_tuyen.BANG_TUYEN:
        _, ghi, _ = sbt.sql_cua_tuyen(t.ham)
        assert "fls_itl" not in ghi, f"⛔ {t.duong} GHI THAT vao so"


# ── ⓒ ⛔⛔ PHA CO CHU DICH — cong phai DO ─────────────────────────────────
def _mot(t: Tuyen) -> tuple:
    return (t,)


def _tuyen(ham: str) -> Tuyen:
    return next(t for t in bang_tuyen.BANG_TUYEN if t.ham == ham)


def test_cong_DO_khi_ban_khai_THIEU_mot_bang():
    """⭐ Tai hien **dung** lo 03/09: `/gates` bo sot `fls_moi_noi`."""
    t = _tuyen("cong")
    hong = Tuyen(t.phuong_thuc, t.duong, t.ham,
                 tuple(b for b in t.bang if b != "fls_moi_noi"),
                 mo_ta=t.mo_ta)
    loi, _ = sbt.soi(_mot(hong))
    assert any("fls_moi_noi" in x and "khong khai" in x for x in loi)


def test_cong_DO_khi_ban_khai_THUA_mot_bang():
    """⛔ Ban do ve mot duong ⛔ khong co that cung la mot ban do sai."""
    t = _tuyen("cong")
    hong = Tuyen(t.phuong_thuc, t.duong, t.ham,
                 t.bang + ("fls_reject",), mo_ta=t.mo_ta)
    loi, _ = sbt.soi(_mot(hong))
    assert any("fls_reject" in x and "khong cham" in x for x in loi)


def test_cong_DO_khi_co_cau_GHI_THAT_vao_so():
    """⭐⭐ Nhanh quan trong nhat — bom phep do gia de no CHAY duoc."""
    t = _tuyen("sua")

    def _gia(_ham):
        return set(t.bang), {"fls_itl", "fls_journal"}, ["gia"]

    loi, _ = sbt.soi(_mot(t), do_sql=_gia)
    assert any("GHI THAT" in x and "fls_itl" in x for x in loi)


def test_cong_DO_khi_GHI_that_ma_bang_ghi_khong_khai():
    t = _tuyen("sua")

    def _gia(_ham):
        return set(t.bang), {"fls_adjustment", "fls_journal", "fls_sua_tay"}, []

    loi, _ = sbt.soi(_mot(t), do_sql=_gia)
    assert any("fls_sua_tay" in x and "bang_ghi" in x for x in loi)


def test_cong_DO_khi_tuyen_tro_toi_mot_ham_khong_co():
    hong = Tuyen("GET", "/api/fls/v1/ma", "ham_khong_co_that", ("fls_itl",),
                 mo_ta="tuyen ma")
    loi, _ = sbt.soi(_mot(hong))
    assert any("khong co ham" in x for x in loi)


# ── ⓓ ⚠ hai lop BAO DONG GIA da gap, ghim lai de ⛔ khong quay lai ────────
def test_docstring_nhac_ten_bang_KHONG_bi_doc_thanh_SQL():
    """⚠ `doc_bao_cao` co chu thich *"`fls_moi_noi`, ⛔ KHONG `fls_pm_link`"*.

    Doc ca docstring thi cong se bao `/gates` cham `fls_pm_link` — mot bao dong
    **GIA**, va mot cong keu sai la mot cong nguoi ta se **go ra**.
    """
    cham, _, _ = sbt.sql_cua_tuyen("cong")
    assert "fls_pm_link" not in cham


def test_chu_thich_SQL_bi_bo_truoc_khi_quet():
    """`-- … fls_x …` trong cau SQL ⛔ khong duoc tinh la mot phep cham bang."""
    assert sbt.CHU_THICH_SQL.sub(" ", "SELECT 1 -- doc fls_bia_dat\nFROM x") \
        .find("fls_bia_dat") == -1


def test_quet_bang_bat_dung_ten():
    assert set(sbt.BANG.findall(
        "FROM fls_itl i JOIN fls_moi_noi k")) == {"fls_itl", "fls_moi_noi"}


@pytest.mark.parametrize("cau,cho_doi", [
    ("INSERT INTO fls_journal (a) VALUES (1)", "fls_journal"),
    ("update fls_queue_state set x=1", "fls_queue_state"),
    ("DELETE FROM fls_pm_link WHERE 1=0", "fls_pm_link"),
])
def test_quet_phep_GHI_bat_dung_muc_tieu(cau, cho_doi):
    m = sbt.GHI.search(cau)
    assert m and next(x for x in m.groups() if x) == cho_doi


def test_SELECT_khong_bi_doc_nham_thanh_GHI():
    assert sbt.GHI.search("SELECT * FROM fls_itl") is None


# ── ⓔ hai cong phai DUNG CHUNG mot ban khai ───────────────────────────────
def test_cong_cu_van_XANH_sau_khi_sua_ban_khai():
    """⛔ Sua `bang` cho khop SQL ⛔ khong duoc lam vo cong cu (`INV-I08`,
    `QĐ-ITL-45`, luat mang vet)."""
    assert bang_tuyen.kiem_bang_tuyen() == []


def test_moi_bang_moi_them_deu_nam_trong_BAN_TRANG():
    """⛔ `QĐ-ITL-45`: FLS chi doc kho rieng. Ban khai rong ra ⛔ khong duoc keo
    theo mot ten bang ngoai `fls_*`."""
    for t in bang_tuyen.BANG_TUYEN:
        la = [b for b in t.bang if b not in bang_tuyen.BANG_CHO_PHEP]
        assert la == [], f"⛔ {t.duong} cham bang ngoai ban trang: {la}"


def test_ten_bang_trong_ban_khai_deu_co_that_trong_kho():
    """⛔ Mot ten go sai *(`fls_da_xongg`)* se lam cong nay xanh gia mai mai."""
    from fls.db import schema

    co = set(schema.TABLES)          # `TABLES` la dict: ten -> khai bao
    for t in bang_tuyen.BANG_TUYEN:
        la = [b for b in t.bang if b not in co]
        assert la == [], f"⛔ {t.duong} khai bang ⛔ khong co trong kho: {la}"


def test_ma_nguon_cong_khong_go_cung_danh_sach_bang():
    """⚠ Cong phai tim bang bang MAU, ⛔ khong bang mot danh sach chep tay —
    mot danh sach chep tay se lac hau y het cai no dang canh."""
    with open(sbt.__file__, encoding="utf-8") as f:
        ma = f.read()
    assert re.search(r"BANG\s*=\s*re\.compile", ma)
    assert "fls_da_xong" not in ma.split('"""', 2)[2], (
        "⛔ than cong ⛔ khong duoc go cung ten bang nao")
